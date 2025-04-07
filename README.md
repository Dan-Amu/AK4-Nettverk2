# AK4-Nettverk2

This repository contains a python script to automatically configure Cisco routers and switches to the point where they can be accessed by SSH (so Ansible can do further configuration).
It also contains Ansible scripts to further configure Cisco routers and switches. The current Ansible files are set up to create a specific network, but should be easy to edit for other setups.

![NettverkBildeAK4](https://github.com/user-attachments/assets/0be62baa-86c6-4df0-b500-a0e93055036c)

The ansible scripts are named corresponding to the names in this image.

## Table of Contents
- [Description](#description)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

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


![bilde](https://github.com/user-attachments/assets/55457f5f-7d6f-4341-941f-c38d6e306aab)




