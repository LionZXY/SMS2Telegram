from parse import parse

response = "+CSQ: 0,0\r\n"

signal_info = parse("+CSQ: {strength:d},{}\r\n", response)
print(signal_info)