import sys
from time import sleep
#sys.path.insert(0, '/home/dan/git/AK4-Nettverk2/python/venv/lib/python3.11/site-packages')
import serial
import getuserinput

starting_baud = 9600
databits = serial.EIGHTBITS
paritybits = serial.PARITY_NONE
stop = serial.STOPBITS_ONE
flowcontrol = False

def writeToDevice(content, delay=0.5):
    if ser:
        content = content + '\r\n'
        content = content.encode('utf-8')
        ser.write(content)
        ser.flush()
        sleep(delay)
        output = []
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            output.append(line)
        return output
    else:
        print("serial device not initialized")
        return 1

while True:
    connection = input("How are you connected to the device? [1 for RS232, 2 for USB] :")
    if connection == 1:
        connType = "USB"
        print("USB connections can be slow, you may need to be patient.")
        break
    elif connection == 2:
        connType = "RS232"
        break
    else:
        print("Invalid option")
        continue

ser = serial.Serial('/dev/ttyACM0', baudrate=starting_baud, bytesize=databits, parity=paritybits, stopbits=stop, xonxoff=flowcontrol, timeout=5)
print(ser.name)


writeToDevice('')
writeToDevice('en')
writeToDevice('terminal length 0')
if connType == "RS232":
    writeToDevice('terminal speed 115200', delay=0)
    ser.baudrate = 115200
    output = writeToDevice('show run | inc interface', delay=1)
else:
    output = writeToDevice('show run | inc interface', delay=1)
print(output)
getuserinput.getConfig(output)

writeToDevice('end')
writeToDevice('terminal speed 9600')
ser.close()

