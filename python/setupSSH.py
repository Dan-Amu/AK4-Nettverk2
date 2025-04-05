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

global tasks

def writeToDevice(content, delay=0.5):
    output = []
    if filewrite_mode or ser:
        content = content + '\r\n'
        if filewrite_mode == True:
            file.write(content)
            file.flush()
            sleep(delay)
        else:
            content = content.encode('utf-8')
            ser.write(content)
            ser.flush()
            sleep(delay)
            while ser.in_waiting > 0 and filewrite_mode == False:
                line = ser.readline().decode('utf-8').strip()
                if not output[-1] == line:
                    output.append(line)
            return output
    else:
        print("serial device not initialized")
        return 1

def configureTasks(tasks):
    for task in tasks:
        commandsToRun = ["conf term"]
        
        match task[0]:
            case "configureInterface":
                commandsToRun.append(f"interface {task[1]}")
                if task[2][0] == "access":
                    commandsToRun.append("switchport mode access")
                    commandsToRun.append(f"switchport access vlan {task[2][1]}")
                    completedTask = "Access port configured"
                elif task[2][0] == "trunk":
                    commandsToRun.append("switchport mode trunk")
                    commandsToRun.append(f"switchport trunk allowed vlan {task[2][1]}")
                    completedTask = "Trunk port configured"
                elif task[2][0] == "router":
                    commandsToRun.append("no switchport")
                    commandsToRun.append(f"ip address {task[2][1]} {task[2][2]}")
                    commandsToRun.append("no shutdown")
                    completedTask = "Router port configured"
                commandsToRun.append("end")
            case "confmgmt":
                commandsToRun.append(f"interface vlan{task[1]}")
                commandsToRun.append(f"ip address {task[2]} {task[3]}")
                commandsToRun.append("no shutdown")
                commandsToRun.append("exit")
                commandsToRun.append(f"vlan {task[1]}")
                commandsToRun.append("end")
                completedTask = "Management VLAN interface configured"
            case "adduser":
                commandsToRun.append(f"username {task[1]} privilege 15 secret {task[2]}")
                commandsToRun.append("end")
                completedTask = "User added"
            case "setupssh":
                commandsToRun.append(f"hostname {task[1]}")
                commandsToRun.append(f"ip domain name {task[2]}")
                commandsToRun.append("longDelayForKeygen") #insert magic string to tell loop that it should increase the delay on next write
                commandsToRun.append("crypto key generate rsa gen mod 1024")
                commandsToRun.append("line vty 0 4")
                commandsToRun.append("login local")
                commandsToRun.append("transport input ssh")
                commandsToRun.append("end")
                completedTask = "SSH configured"
            case "staticroute":
                commandsToRun.append(f"ip route {task[1]} {task[2]} {task[3]}")
                commandsToRun.append("end")
                completedTask = "Static route created"
            case _:
                completedTask = "nothing"
                pass

        longDelayForKeygen = False
        for lines in commandsToRun:
            if lines == "longDelayForKeygen":
                longDelayForKeygen = True
            else:
                if longDelayForKeygen == True:
                    writeToDevice(lines, delay=10)
                else:
                    writeToDevice(lines)
                longDelayForKeygen = False
                print("!", end="")
        print("\n", completedTask)
            
try:
    serialDevice = sys.argv[1]
except IndexError:
    print(f"Enter the serial device as first argument. E.g. \'python3 {sys.argv[0]} /dev/ttyACM0\' ")
    exit()
except:
    print("Something went wrong. Exiting.")
    exit()

filewrite_mode = False
while True:
    connection = input("How are you connected to the device? [1 for RS232, 2 for USB] :")
    if connection == "2":
        connType = "USB"
        skip_serial = False
        print("USB connections can be slow, you may have to be patient.")
        break
    elif connection == "1":
        connType = "RS232"
        skip_serial = False
        break
    elif connection == "debug" or connection == "noserial":
        skip_serial = True
        break
    elif connection == "debug_filewrite":
        connType = "file"
        filewrite_mode = True
        skip_serial = False
        break
    else:
        print("Invalid option")
        continue

if not skip_serial:
    print("does this get run? skip_serial")
    if not filewrite_mode:
        ser = serial.Serial(serialDevice, baudrate=starting_baud, bytesize=databits, parity=paritybits, stopbits=stop, xonxoff=flowcontrol, timeout=5)
    else:
        file = open(serialDevice, "a")
    print("connected to ", serialDevice)

    writeToDevice('')
    writeToDevice('en')
    writeToDevice('terminal length 0')
    if connType == "RS232":
        #writeToDevice('terminal speed 115200', delay=0)
        #ser.baudrate = 115200

        output = writeToDevice('show run | inc interface', delay=1)
    elif connType == "USB":
        output = writeToDevice('show run | inc interface', delay=10)

# if output is not set (in skip_serial or debug_filewrite mode), set it to placeholder data
try: 
    output=output
except:
    output = ['show run | inc interface', 'interface GigabitEthernet5/0/1', 'interface GigabitEthernet5/0/2', 'interface GigabitEthernet5/0/3', 'interface GigabitEthernet5/0/4', 'interface GigabitEthernet5/0/5', 'interface GigabitEthernet5/0/6', 'interface GigabitEthernet5/0/7', 'interface GigabitEthernet5/0/8', 'interface GigabitEthernet5/0/9', 'interface GigabitEthernet5/0/10', 'interface GigabitEthernet5/0/11', 'interface GigabitEthernet5/0/12', 'interface GigabitEthernet5/0/13', 'interface GigabitEthernet5/0/14', 'interface GigabitEthernet5/0/15', 'interface GigabitEthernet5/0/16', 'interface GigabitEthernet5/0/17', 'interface GigabitEthernet5/0/18', 'interface GigabitEthernet5/0/19', 'interface GigabitEthernet5/0/20', 'interface GigabitEthernet5/0/21', 'interface GigabitEthernet5/0/22', 'interface GigabitEthernet5/0/23', 'interface GigabitEthernet5/0/24', 'interface GigabitEthernet5/0/25', 'interface GigabitEthernet5/0/26', 'interface GigabitEthernet5/0/27', 'interface GigabitEthernet5/0/28', 'interface Vlan1', 'monitor session 1 source interface Gi5/0/1 - 13', 'monitor session 1 destination interface Gi5/0/16', 'GigaSwitch#', 'GigaSwitch#']
portLayout = getuserinput.getConfig(output)

tasks = getuserinput.getInput()
#print(tasks)
if not skip_serial:
    configureTasks(tasks)


if not skip_serial and not filewrite_mode:
    writeToDevice('end')
    writeToDevice('write memory')
#    writeToDevice(f"terminal speed {starting_baud}")
    ser.close()
if filewrite_mode and not skip_serial:
    writeToDevice('----------end of program run marker----------')
    file.close()
print("Done!")
