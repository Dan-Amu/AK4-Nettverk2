# AK4-Nettverk2

This repository contains a python script to automatically configure Cisco routers and switches to the point where they can be accessed by SSH (so Ansible can do further configuration).
It also contains Ansible scripts to further configure Cisco routers and switches. The current Ansible files are set up to create a specific network, but should be easy to edit for other setups.

![NettverkBildeAK4](https://github.com/user-attachments/assets/0be62baa-86c6-4df0-b500-a0e93055036c)

The ansible scripts are named corresponding to the names in this image.

## Table of Contents
- [Description](#description)
- [Prerequisites](#prerequisites)
- [Usage](#usage)

## Description

A more detailed description of the project, how it works, and any background information. Mention any notable features or technologies used.

## Prerequisites
### Python
- Python 3
- Pyserial package

Can be installed by a package manager like apt
```bash
sudo apt install python3 python-serial
```
Other ways to install can be found here: ![https://pyserial.readthedocs.io/en/latest/pyserial.html#installation](https://pyserial.readthedocs.io/en/latest/pyserial.html#installation)

### Ansible
- Ansible itself
- Paramiko package
Ansible will need a Linux version to run it. A WSL distro will work. (make sure to set WSL version to 1)

Ansible and Paramiko can either be directly installed onto your linux distro with a package manager like apt:
```bash
sudo apt install ansible
sudo apt install paramiko
```

Or you can create a python virtual env:
```bash
pip install virtualenv
python3 -m venv venv
source ./venv/bin/activate
pip install ansible paramiko
```
You will have to run the source command every time you want to use ansible if you choose this method.

## Usage

### Python
The main python program is setupSSH.py.
The when running the python script, you have to provide an argument with the path to your serial device file, or COM port name if you are on Windows.
![bilde](https://github.com/user-attachments/assets/cb8da34f-e488-4034-ba4b-d73ae0e20fa6)

When you run the python script, it will take a moment to test the connection to the device and retrieve information.
It will then display this menu. Enter the number next to the option, and the script will ask you for necessary information.
![bilde](https://github.com/user-attachments/assets/b12f1b72-b2ab-4669-a852-fdf9b3a4683e)


Here is an example that sets up an access-port and SVI(Switched VLAN Interface) on a switch.
![bilde](https://github.com/user-attachments/assets/55457f5f-7d6f-4341-941f-c38d6e306aab)

To prepare a device for Ansible configuration, you will need to configure a port to access the device through, a user, a vlan interface(on switches), and the ssh server.
If you want the device to be reachable through a router you may need a static route.

No configuration will be applied to the device before you select option 9.
The script will then apply all configuration.

### Ansible

Check that the paths in your ansible.cfg file match where you downloaded the repository.
![ansible cfgpaths](https://github.com/user-attachments/assets/c4bfe476-106b-4a72-95fb-343936fcab02)


Every device you want to configure with Ansible will have to have an entry with its IP-address in the hosts file.
![bilde](https://github.com/user-attachments/assets/bcc448e4-2801-4c7b-ae90-694f5b7350f1)

All you have to do is add an entry with the device's IP address in the hosts file, and then put the name you assigned on the line above into the ansible script:
![ansible hostsinscript](https://github.com/user-attachments/assets/88e6f8f0-d9dc-4f4c-b537-b1f3e77b8423)

You can then run any ansible script with the ansible-playbook command. 
The -K flag may be necessary, if it is enter the enable password.
```bash
ansible-playbook accessScript.yaml -K
```
Example:

![bilde](https://github.com/user-attachments/assets/49f80bd7-3056-4881-b1d5-a0c0015877a1)


The scripts included in this reposiory are:
- L3switch.yaml
  Configures a Layer 3 switch with three routing ports to connect a managemnt PC and the two routers, and configures OSPF to route between these.
- router1.yaml and router2.yaml
  Configures a router with a connection to the L3 switch, as well as a connection down to the core switch and VLAN 10 and 99 for management. Also configures HSRP between routers.
