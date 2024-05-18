import asyncio

import gpiod
from gpiozero import LED
import time
import serial

from src.conf import SERIAL_PORT
from src.sim868_cmd import send_ping
from src.telegram_bot import send_message


def __check_gsm_module() -> bool:
    print("Start checking module")
    ser = serial.Serial(SERIAL_PORT, timeout=10, write_timeout=10)
    print(ser)
    try:
        send_ping(ser)
    except Exception as error:
        print("Can't send ping because error", error)
        return False
    finally:
        ser.close()
    return True


def power_on_sim868():
    print("Try power on/off SIM868")
    led = LED(pin=4) # GPIO4, PIN 7 (https://gpiozero.readthedocs.io/en/latest/recipes.html#pin-numbering)
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
        is_loaded = __check_gsm_module()
    await send_message("SIM868 загружен, пинг прошел успешно")
