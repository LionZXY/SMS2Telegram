import threading
from queue import Queue, Empty

from parse import parse

from src.conf import SMSC
from src.sim868_cmd_queue import to_request_queue, received_response_queue, antenna_signal_queue

from smspdudecoder.easy import read_incoming_sms

from src.telegram_bot import send_sms_message, send_message


def __send_cmd(cmd: str) -> str:
    to_request_queue.put(cmd)
    response = received_response_queue.get()
    if response == cmd + "\r\n":  # ignore echo
        response = received_response_queue.get()
    return response


async def setup_module():
    response = __send_cmd('AT+CSCA="' + SMSC + '"')
    if response != "OK\r\n":
        raise Exception("Set SMSC failed with response " + response)
    response = __send_cmd('AT+CMGF=0')  # Enable PDU mod
    if response != "OK\r\n":
        raise Exception("Set PDU mod failed with response " + response)
    response = __send_cmd('AT+CANT=1,1,10')  # Enable autodetecting for antennas
    if response != "OK\r\n":
        raise Exception("Autodetecting for antennas failed command, but receive " + response)
    response = antenna_signal_queue.get()  # Waiting for antenna status
    if not response.startswith("+CANT:"):
        raise Exception("Antennas command not receive status, but receive " + response)
    antenna_info = parse("+CANT: {status:d}\r\n", response)
    status_text = "Unknown"
    match antenna_info['status']:
        case 0:
            status_text = "Connected normally"
        case 1:
            status_text = "Connected to GND"
        case 2:
            status_text = "Connected to other power source"
        case 3:
            status_text = "Not connected"
    await send_message("Antenna status is: " + status_text)
    to_request_queue.put('AT+CANT=1,0,10')  # Disable antenna notification
    try:
        while True:
            received_response_queue.get(timeout=10)  # Clean queue
    except Empty:
        pass
    response = __send_cmd("AT+CSQ")  # Request signal quality report
    if not response.startswith("+CSQ:"):
        raise Exception("Signal quality report not received")
    signal_info = parse("+CSQ: {strength:d},{}\r\n", response)
    strength = signal_info["strength"]
    strength_text = "Unknown"
    if strength < 2:
        strength_text = "Extremely bad"
    elif strength < 10:
        strength_text = "Marginal"
    elif strength < 15:
        strength_text = "OK"
    elif strength < 20:
        strength_text = "Good"
    else:
        strength_text = "Excellent"

    await send_message("Signal quality is: " + strength_text)


def __remove_message_with_id(id: int):
    print("Remove message with id " + str(id))
    to_request_queue.put("AT+CMGD=" + str(id))


async def check_unread_message():
    to_request_queue.put("AT+CMGL=4")
    pending_messages = {}
    response = received_response_queue.get()
    while True:
        if response.startswith("+CMGL"):
            meta_info = parse("+CMGL: {index:d},{is_read:d},{},{length:d}\r\n", response)
            print(meta_info)
            message_pdu = received_response_queue.get(timeout=10)
            sms_data = read_incoming_sms(message_pdu)
            print(sms_data)

            partial_data = sms_data['partial']
            if partial_data != False:
                reference = partial_data['reference']
                parts = pending_messages.get(reference, [None for i in range(partial_data['parts_count'])])
                sms_data['message_index'] = meta_info['index']
                parts[partial_data['part_number'] - 1] = sms_data
                pending_messages[reference] = parts

                if None not in parts:
                    await send_sms_message(
                        sender=sms_data['sender'],
                        time=sms_data['date'],
                        text=''.join(data['content'] for data in parts)
                    )
                    for data in parts:
                        index = data['message_index']
                        __remove_message_with_id(index)
            else:
                await send_sms_message(
                    sender=sms_data['sender'],
                    time=sms_data['date'],
                    text=sms_data['content']
                )
                __remove_message_with_id(meta_info['index'])
        try:
            response = received_response_queue.get(timeout=10)
        except Empty:
            return
