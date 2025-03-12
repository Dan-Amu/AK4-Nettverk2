import sys
sys.path.insert(0, '/home/dan/git/AK4-Nettverk2/python/venv/lib/python3.11/site-packages')
import serial
baud = 9600
databits = serial.EIGHTBITS
paritybits = serial.PARITY_NONE
stop = serial.STOPBITS_ONE
flowcontrol = False
ser = serial.Serial('/dev/ttyACM0', baudrate=baud, bytesize=databits, parity=paritybits, stopbits=stop, xonxoff=flowcontrol)
print(ser.name)

ser.write(b'en')
ser.write(b'conf t')
#router stuff
#ser.write(b'interface Gig0/0')
#ser.write(b'ip address 192.168.17.2 255.255.255.0')
#ser.write(b'no shutdown')
#ser.write(b'exit')
#ser.write(b'interface Gig0/1')
#ser.write(b'ip address 192.168.0.2 255.255.255.0')
#ser.write(b'no shutdown')
#ser.write(b'exit')
#ser.write(b'hostname RG1')
ser.write(b'hostname SG1e')
ser.write(b'interface vlan 1')
ser.write(b'ip address 192.168.99.3')
ser.write(b'no shutdown')
ser.write(b'exit')
ser.write(b'ip domain-name Gronn.local')
ser.write(b'crypto key generate rsa')
ser.write(b'1024')
ser.write(b'line vty 0 4')
ser.write(b'login local')
ser.write(b'transport input ssh')
ser.write(b'username cisco privilege 15 password cisco')


ser.close()

