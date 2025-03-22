import sys
sys.path.insert(0, '/home/dan/git/AK4-Nettverk2/python/venv/lib/python3.11/site-packages')
import serial
baud = 9600
databits = serial.EIGHTBITS
paritybits = serial.PARITY_NONE
stop = serial.STOPBITS_ONE
flowcontrol = False
ser = serial.Serial('/dev/ttyACM0', baudrate=baud, bytesize=databits, parity=paritybits, stopbits=stop, xonxoff=flowcontrol, timeout=0)
ser.write(b'en\r')
#in_waiting.get()
#print(readBytes)
