import re
ip_regex = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")
username_regex = re.compile(r"[^a-z]+g")
global tasks
tasks = []

def getNumberInput(lowNum, highNum, InputString):
    while True:
        inNum = input(InputString)
        try:
            inNum = int(inNum)
        except:
            print("Invalid input. Enter the number next to the option.")
            continue
        if inNum >= lowNum and inNum <= highNum:
            return inNum
        else:
            print("Invalid input. Enter the number next to the option.")
def CIDRtoMask(CIDR):
    reversePowersOf2 = [ 2 ** x for x in range(7, 0, -1) ]
    fullOctets = CIDR//8
    finalOctet = CIDR%8
     
    inputSubnetMask = []
    octetsFinished = 0

    for i in range(0, fullOctets):
        inputSubnetMask.append("255")
        octetsFinished = octetsFinished+1

    inputSubnetMask.append(0)
    for u in range(0, finalOctet):
        inputSubnetMask[octetsFinished] += reversePowersOf2[u]
    inputSubnetMask[octetsFinished] = str(inputSubnetMask[octetsFinished]) 

    if len(inputSubnetMask) < 4:
        for yuh in range(0, 4-len(inputSubnetMask)):
            inputSubnetMask.append("0")
    subnetMask = '.'.join(inputSubnetMask)
    return subnetMask

def getConfig(cfg):
    #    ser.write(b'en\r\n')
    #    ser.write(b'show run\r\n')
#        output = []
#        while ser.in_waiting > 0:
#            line = ser.readline().decode('utf-8').strip()
#            output.append(line)
    for line in cfg:
        if "interface" in line:
            print(line)
    switchports = {"portType":"FastEthernet", "count":24, "layout":"0/0/0"}
    uplinks = {"portType":"GigabitEthernet", "count":4, "layout":"0/1"}
    portLayout = {"switchports":switchports, "uplinks":uplinks} 

    return portLayout

def getInput():
    while True:
        print("What tasks do you want to perform?")
        print("1. Configure an interface.           2. Something")
        print("3. Set up management interface       4. Create user")
        print("5. Run commands for ssh setup.")
        print("9. Finish")
        selectedOption = input("Select option [1-9]: ")
        print("\n")
        
        try:
            selectedOption = int(selectedOption)
        except:
            print("Invalid input. Enter the number next to the task.\n")
            continue
        match selectedOption:
            case 1:
                inputConfigureInt()
            case 2:
                something()
            case 3:
                setupmgmt()
            case 4:
                createUser()
            case 5:
                setupSSH()
            case 9:
                break
            case _:
                print("Unknown option selected\n")

def inputConfigureInt():
    global tasks
    while True:
        intToConfigure = input("Select Interface type: 1. FastEthernet 2. GigabitEthernet [1, 2] :")
        try:
            intToConfigure = int(intToConfigure)
        except:
            print("Invalid Input. Enter the number next to the type.\n")
            continue

        if intToConfigure == 1:
            subjectInterface = "FastEthernet" 
        elif intToConfigure == 2:
            subjectInterface = "GigabitEthernet"
        else:
            print("Invalid Input. Enter the number next to the type.\n")
            continue
        print("selected: ", subjectInterface, "\n")
        subjectIntNumber = getNumberInput(1, portLayout["switchports"]["count"], "Enter interface number. [1-"+str(portLayout["switchports"]["count"])+"] : ") 
        print("selected: ", subjectIntNumber, "\n")
        while True:
            portMode = input("Select port mode: 1. Trunk 2. Access [1, 2]: ")
            try:
                portMode = int(portMode)
            except:
                print("Invalid Input. Enter the number next to the mode.\n")
                continue
            portCFG= ["", ""]
            if portMode == 1:
                portCFG[0] = "trunk" 
            elif portMode == 2:
                portCFG[0] = "access"
            else:
                print("Invalid Input. Enter the number next to the mode.\n")
                continue
            if portCFG[0] == "trunk":
#                while True:
                 portCFG[1] = input("what vlans should be allowed on the trunk? [number, numbers separated by comma or all] : ")
#                    if not portCFG[1] == "all":
#                        vlanNumbers = portCFG[1].split(",") # TODO this does not work 
#                        print(vlanNumbers)
#                        for vNum in vlanNumbers:
#                            if int(vNum) >= 4094 or int(vNum) <= 1:
#                                print("One or more of the Vlan numbers were invalid")
#                                magicA = 1
#                                break
#                    if magicA == 0 or portCFG[1] == "all":
#                        break
#
            if portCFG[0] == "access":
                portCFG[1] = getNumberInput(1, 4094, "Enter Access Port VLAN: ")
            print("selected: ", portCFG, "\n")
            break
        editedLayout = portLayout["switchports"]["layout"]
        editedLayout = editedLayout[:-1]
        currentInterface = subjectInterface+editedLayout+str(subjectIntNumber)
        print(currentInterface)
        print(portCFG)
        break
    retval = [currentInterface, portCFG]
    tasks.append(["configureInterface", currentInterface, portCFG])
    return [currentInterface, portCFG]

def something():
    pass

def setupmgmt():
    global tasks
    vlan = getNumberInput(1, 4094, "Enter management VLAN number. [1-4094] : ")
    print("\n")

    #reversePowersOf2 = [ 2 ** x for x in range(7, 0, -1) ]
    while True:
        while True:
            ipAddress = input("Enter IP address of VLAN interface. [*.*.*.*] : ")
            ipAddress = ipAddress.replace(",",".")
            if ip_regex.match(ipAddress):
                break 
            else:
                print("Not a valid IP address.\n")
        CIDR = getNumberInput(1, 31, "Enter subnet mask size [1-31] : ")
        subnetMask = CIDRtoMask(CIDR)
        print(subnetMask)

        break
    tasks.append(["confmgmgt", vlan, ipAddress, subnetMask])
        
def createUser():
    while True:
        username = input("Enter username: ") ##TODO: REGEX BROKEN
        print((len(username) < 33) , username_regex.match(username))
        if len(username) < 33 and username_regex.match(username):
            print("Accepted:")
            break
        else:
            continue
        password = input("enter password: ")
        if len(password) < 33:
            print("Accepted")
            break
    tasks.append(["adduser", username, password])

def setupSSH():
    hostName = input("Enter device hostname: ")
    domainName = input("Enter domain name: ")

    tasks.append(["setupssh", hostName, domainName])

def staticRoute():
    while True:

        destPrefix = input("Enter route destination prefix: ")
        if ip_regex.match(destPrefix):
            print("Invalid IP address")
            continue
        break
    while True:
        destMask = input("Enter route destination mask: ")
        if ip_regex.match(destMask):
            print("Invalid subnet mask")
            continue
        break


if __name__ == '__main__':

    portLayout = getConfig()
    getInput()

    print(tasks)
