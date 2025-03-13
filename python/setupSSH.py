import sys
from time import sleep
sys.path.insert(0, '/home/dan/git/AK4-Nettverk2/python/venv/lib/python3.11/site-packages')
import serial

baud = 9600
databits = serial.EIGHTBITS
paritybits = serial.PARITY_NONE
stop = serial.STOPBITS_ONE
flowcontrol = False

def writeToDevice(content)
    if ser:
        ser.write(content)
        sleep(0.05)
        return 0
    else:
        print("serial device not initialized")
        return 1

ser = serial.Serial('/dev/ttyACM0', baudrate=baud, bytesize=databits, parity=paritybits, stopbits=stop, xonxoff=flowcontrol)
print(ser.name)


writeToDevice(b'en')
writeToDevice(b'conf t')
#router stuff
#writeToDevice(b'interface Gig0/0')
#writeToDevice(b'ip address 192.168.17.2 255.255.255.0')
#writeToDevice(b'no shutdown')
#writeToDevice(b'exit')
#writeToDevice(b'interface Gig0/1')
#writeToDevice(b'ip address 192.168.0.2 255.255.255.0')
#writeToDevice(b'no shutdown')
#writeToDevice(b'exit')
#writeToDevice(b'hostname RG1')
writeToDevice(b'hostname SG1e')
writeToDevice(b'interface vlan 1')
writeToDevice(b'ip address 192.168.99.3')
writeToDevice(b'no shutdown')
writeToDevice(b'exit')
writeToDevice(b'ip domain-name Gronn.local')
writeToDevice(b'crypto key generate rsa')
writeToDevice(b'1024')
sleep(5)
writeToDevice(b'line vty 0 4')
writeToDevice(b'login local')
writeToDevice(b'transport input ssh')
writeToDevice(b'username cisco privilege 15 password cisco')


ser.close()

