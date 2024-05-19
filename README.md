# SIM868 Raspberry Pi 5 SMS Forwarder

Dockerised Python script for Raspberry PI (including 5) to send sms from SIM868 to Telegram

## Installation

1) Install SIM868 in Raspberry Pi GPIO 40-pin port
2) Set the jumper to B as below

![](docs/jumper_set.png)

3) Enable serial on Raspberry Pi: `sudo raspi-config` -> Interfaces Options -> Serial -> No -> Yes

TODO

## Envs and examples

TG_TOKEN=
TG_CHAT_ID=
SERIAL_PORT=/dev/ttyAMA0
GPIOCHIP=/dev/gpiochip4
SMSC=+99599599999
REPORT_TIMEZONE="Europe/London"

## Spreadsheet

- Enable PDU Mode: `AT+CMGF=0`
- Enable Text Mod: `AT+CMGF=1`
- Set SMSC to +99599599999: `AT+CSCA="+99599599999"`
- Switch to PDU mode: `AT+CMGF=0`
- Receive all unread messages (PDU Mode only): `AT+CMGL=0`
- Receive all messages (PDU Mode only): `AT+CMGL=4`
- Receive all messages (TEXT mode only: `AT+CMGL="ALL"`
- Read message with index 1: `AT+CMGR=1`
- Delete message with index 1: `AT+CMGD=1`