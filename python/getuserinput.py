import re
ip_regex = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")
#ip_regex = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[0-9]|)\d)\.?\b){4}$")
username_regex = re.compile(r"[^a-z]+g")

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
    global portLayout

    interfaceTypes = ['Ethernet', 'FastEthernet', 'GigabitEthernet', 'TenGigabitEthernet', 'Serial']
    #    ser.write(b'en\r\n')
    #    ser.write(b'show run\r\n')
#        output = []
#        while ser.in_waiting > 0:
#            line = ser.readline().decode('utf-8').strip()
#            output.append(line)

    #remove "interface " from start of every line
    actualInterfaces = []
    for line in cfg:
        actualInterfaces.append(line[10:])

    #filter for the interfaces in interfaceTypes and remove last number
    interfacelist = []
    for inter in actualInterfaces:
        #print(inter)
        for inty in interfaceTypes:
            #print(re.split(r'(\d+)', inter))
            if re.split(r'(\d+)', inter)[0] == inty:
                #print(inter)
                
            #if f"interface {iface}" in line:
                prefix, delim, intnum = inter.rpartition("/")
                interfacelist.append(prefix+delim)
                if intnum == "0":
                    print(inter, "0")
                    interfacelist[-1] = interfacelist[-1]+'0'

    
    #print(interfacelist)
    
    intgroups = {}
    groupswithzero = [] 
    for zz in interfacelist:
        if zz[-1] == '0':
            after = zz[:-1]
            groupswithzero.append(after)
        else:
            after = zz

        if after in intgroups:
            intgroups[after] = intgroups[after] + 1
        else: 
            intgroups[after] = 1
    keys_intgroups = list(intgroups.keys())
    real_intgroups = []
    for i in range(0, len(intgroups)):
        real_intgroups.append([keys_intgroups[i], intgroups[keys_intgroups[i]]])

    #print(real_intgroups, groupswithzero)

    #for infa in actualInterfaces:
    #    prefix, delim, intnum = infa.rpartition("/")
    #    if prefix+delim not in intgroups[0]:
    #       intgroups[0].append(prefix+delim)
    #       intgroups[1].append(1) 
    #    else: intgroups[
    #    print(prefix, intnum)
    switchports = {"portType":"FastEthernet", "count":24, "layout":"0/0"}
    uplinks = {"portType":"GigabitEthernet", "count":4, "layout":"0/1"}
    portLayout = {"switchports":switchports, "uplinks":uplinks} 

    #return portLayout
    return [real_intgroups, groupswithzero]

def getInput(pl=0):
    tasks = []
    while True:
        print(" ")
        print("What tasks do you want to perform?")
        print("1. Configure a physical interface.          2. Create user")
        print("3. Set up vlan interface (switch mgmt)      4. Configure static route")
        print("5. Set up ssh server for management.")
        print("9. Apply configuration")
        selectedOption = input("Select option [1-9]: ")
        print("\n")
        
        try:
            selectedOption = int(selectedOption)
        except:
            print("Invalid input. Enter the number next to the task.\n")
            continue
        match selectedOption:
            case 1:
                var1 = inputConfigureInt(pl)
                tasks.append(var1)
            case 2:
                var2 = createUser()
                tasks.append(var2)
            case 3:
                var3 = setupmgmt()
                tasks.append(var3)
            case 4:
                var4 = setupStaticRoute()
                tasks.append(var4)
            case 5:
                var5 = setupSSH()
                tasks.append(var5)
            case 9:
                break
            case _:
                print("Unknown option selected\n")
    return tasks

def inputConfigureInt(portLayout):
    while True:
        numOfPortgroups = len(portLayout[0])
        listPortLayout = list(portLayout[0])
        #print(listPortLayout)
        if numOfPortgroups <= 0:
            print("Something has gone very wrong, script found no ports to configure. Exiting.")
            exit()
        if numOfPortgroups == 1:
            print("Ports found: ", listPortLayout[0][0], "   Amount: ", listPortLayout[0][1])
            selectedPortgroup = 0
        else:
            increment = 1
            print("Port groups:")
            for thing in listPortLayout:
                print(str(increment)+". "+thing[0]+"x", end="   ")
                increment = increment + 1
            print("\n")
            selectedPortgroup = getNumberInput(1, numOfPortgroups, f"Multiple port groups found. Select which you want to configure. [1, {numOfPortgroups}]: ")
            selectedPortgroup = selectedPortgroup - 1

        maxIntNum = listPortLayout[selectedPortgroup][1]
        if listPortLayout[selectedPortgroup][0] in portLayout[1]:
            #print("yuh")
            firstInt = 0
            maxIntNum = str(maxIntNum - 1)
        else:
            #print("nah")
            firstInt = 1
            maxIntNum = str(maxIntNum)
        subjectIntNumber = getNumberInput(firstInt, listPortLayout[selectedPortgroup][1], f"Enter interface number. [{firstInt}-"+maxIntNum+"] : ") 
        #intToConfigure = input(select
       # intToConfigure = input("Select Interface type: 1. FastEthernet 2. GigabitEthernet [1, 2] :")
       # try:
       #     intToConfigure = int(intToConfigure)
       # except:
       #     print("Invalid Input. Enter the number next to the type.\n")
       #     continue

       # if intToConfigure == 1:
       #     subjectInterface = "FastEthernet" 
       # elif intToConfigure == 2:
       #     subjectInterface = "GigabitEthernet"
       # else:
       #     print("Invalid Input. Enter the number next to the type.\n")
       #     continue
       # print("selected: ", subjectInterface, "\n")
       # subjectIntNumber = getNumberInput(1, portLayout["switchports"]["count"], "Enter interface number. [1-"+str(portLayout["switchports"]["count"])+"] : ") 
       # print("selected: ", subjectIntNumber, "\n")
        while True:
            portMode = input("Select port mode: 1. Trunk 2. Access 3. Routing [1, 2, 3]: ")
            try:
                portMode = int(portMode)
            except:
                print("Invalid Input. Enter the number next to the mode.\n")
                continue
            portCFG= ["", "", ""]
            if portMode == 1:
                portCFG[0] = "trunk" 
            elif portMode == 2:
                portCFG[0] = "access"
            elif portMode == 3:
                portCFG[0] = "router"
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
            print("selected: ", portCFG[0], "\n")

            if portCFG[0] == "router":
                while True:
                    portCFG[1] = input("Enter IP address of routing interface. [*.*.*.*] : ")
                    portCFG[1] = portCFG[1].replace(",",".")
                    if ip_regex.match(portCFG[1]):
                        break 
                    else:
                        print("Not a valid IP address.\n")
                routerportCIDR = getNumberInput(1, 31, "Enter subnet mask size [1-31] : ")
                portCFG[2] = CIDRtoMask(routerportCIDR)
            break        

        currentInterface = listPortLayout[selectedPortgroup][0]+str(subjectIntNumber)
        #print(editedLayout)
        #currentInterface = subjectInterface+editedLayout+str(subjectIntNumber)
        print("Selected interface:", currentInterface)
        print("Options:",portCFG)
        break
    retval = [currentInterface, portCFG]
    return ["configureInterface", currentInterface, portCFG]

def something():
    pass

def setupmgmt():
    vlan = getNumberInput(1, 4094, "Enter management VLAN number. [1-4094] : ")
    print("\n")

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

        break
    print("Selected vlan:", vlan)
    print("Address:", ipAddress, subnetMask)
    return ["confmgmt", vlan, ipAddress, subnetMask]
        
def createUser():
    while True:
        username = input("Enter username: ") ##TODO: REGEX BROKEN
        #print((len(username) < 33) , username_regex.match(username))
        if len(username) < 33 and len(username) > 0: # and username_regex.match(username):
            print("Accepted.\n")
        else:
            print("Failed to create user. Try again.\n")
            continue
        password = input("Enter password: ")
        password2 = input("Enter password again: ")
        if len(password) < 33 and len(password) > 0 and password == password2:
            print("Accepted Password.")
        else:
            print("Failed to create user. Try again.\n")
            continue
        break
    print("\nAdding user:", username)
    return ["adduser", username, password]

def setupSSH():
    hostName = input("Enter device hostname: ")
    domainName = input("Enter domain name: ")
    print("\nSetting up SSH server")
    return ["setupssh", hostName, domainName]

def setupStaticRoute():
    while True:
        destPrefix = input("Enter route destination prefix [*.*.*.*] : ")
        destPrefix = destPrefix.replace(",",".")
        if ip_regex.match(destPrefix):
            break
        else:
            print("Invalid IP address")
    while True:
        destMask = input("Enter route destination mask [*.*.*.*] : ")
        destMask = destMask.replace(",",".")
        if ip_regex.match(destMask):
            break
        else:
            print("Invalid subnet mask")
    while True:
        nextHop = input("Enter next hop address [*.*.*.*] :")
        nextHop = nextHop.replace(",",".")
        if ip_regex.match(nextHop):
            break
        else:
            print("Invalid IP address")
    print("Creating static route: ", destPrefix, destMask, nextHop)
    return ["staticroute", destPrefix, destMask, nextHop]


if __name__ == '__main__':

    portLayout = getConfig(['interface GigabitEthernet1/0/1', 'interface GigabitEthernet0/0/0', 'interface GigabitEthernet0/0/1', 'interface VirtualServiceEngine0/1'])
    tasks = getInput()

    print(tasks)
