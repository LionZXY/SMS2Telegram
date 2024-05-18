import serial
from termcolor import colored


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


def send_ping(ser: serial.Serial):
    line = __send_cmd(ser, "AT")
    if line != "OK\r\n":
        raise Exception("Module not available")
