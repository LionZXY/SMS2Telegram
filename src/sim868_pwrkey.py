import asyncio

import gpiod
from gpiozero import LED
import time
import serial
from termcolor import colored

from src.conf import SERIAL_PORT
from src.telegram_bot import send_message


def __send_cmd(ser: serial.Serial, cmd: str) -> str:
    print("Request to SIM868:", colored(cmd, color="cyan"))
    ser.write((cmd + "\n").encode())
    ser.flush()
    line = ser.readline()
    if line.decode() != cmd + "\r\n":
        raise Exception("Failed send command " + cmd)
    line = ser.readline()
    line_decoded = line.decode()
    print("Answer from SIM868:", colored(line, color="green"))
    return line_decoded


def __send_ping(ser: serial.Serial):
    line = __send_cmd(ser, "AT")
    if line != "OK\r\n":
        raise Exception("Module not available")


def __check_gsm_module() -> bool:
    print("Start checking module")
    ser = serial.Serial(SERIAL_PORT, timeout=10, write_timeout=10)
    print(ser)
    try:
        __send_ping(ser)
    except Exception as error:
        print("Can't send ping because error", error)
        return False
    finally:
        ser.close()
    return True


def power_on_sim868():
    print("Try power on/off SIM868")
    led = LED(pin=4)  # GPIO4, PIN 7 (https://gpiozero.readthedocs.io/en/latest/recipes.html#pin-numbering)
    print(led)
    led.off()
    print("Sleep 4 seconds")
    time.sleep(4)
    led.on()
    print("Finish waiting")


async def check_and_enable_gsm_module():
    is_loaded = __check_gsm_module()
    while not is_loaded:
        await send_message("SIM868 не загружен, пытаюсь включить...")
        power_on_sim868()
        time.sleep(30)
        is_loaded = __check_gsm_module()
    await send_message("SIM868 загружен, пинг прошел успешно")
