
global tasks
tasks = []

def getInput():
    while True:
        print("What tasks do you want to perform?")
        print("1. Configure an interface.           2. ")
        selectedOption = input("Select option:")
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
            case _:
                print("Unknown option selected\n")

        break

def inputConfigureInt():
    while True:
        intToConfigure = input("Select Interface type: 1. FastEthernet 2. GigabitEthernet")
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
        print("selected: ", subjectInterface)
        subjectIntNumber = input("Enter interface number")



getInput()
