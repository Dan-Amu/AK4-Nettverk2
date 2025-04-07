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

```bash
# Example
npm install -g project-dependency
