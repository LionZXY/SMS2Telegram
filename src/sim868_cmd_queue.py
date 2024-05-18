import threading
from queue import Queue, Empty

import serial
from termcolor import colored

from src.conf import SERIAL_PORT

to_request_queue = Queue()
received_response_queue = Queue()

request_check_message_event = threading.Event()


def __read_all_income_text(ser: serial.Serial):
    line = ser.readline()
    while len(line) != 0:
        print("Answer from SIM868:", colored(line, color="green"))
        line_decoded = line.decode()
        if line_decoded.startswith("+CMTI"):
            request_check_message_event.set()
        else:
            received_response_queue.put(line_decoded)
        line = ser.readline()


def __send_one_request(ser: serial.Serial):
    try:
        to_request = to_request_queue.get(block=False)
        print("Request to SIM868:", colored(to_request, color="cyan"))
        ser.write((to_request + "\n").encode())
    except Empty:
        pass


def receive_cmd_loop():
    ser = serial.Serial(SERIAL_PORT, timeout=1, write_timeout=1)
    while True:
        __read_all_income_text(ser)
        __send_one_request(ser)
