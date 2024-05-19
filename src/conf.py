import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv(raise_error_if_not_found=True))

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
SERIAL_PORT = os.getenv("SERIAL_PORT")
GPIOCHIP = os.getenv("GPIOCHIP")
SMSC = os.getenv("SMSC")
REPORT_TIMEZONE = os.getenv("REPORT_TIMEZONE")
