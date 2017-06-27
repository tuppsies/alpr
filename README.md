# alpr


How the program works:

Raspberry Pi takes pictures and stores them

Program searches through all programs looking at images and scanning for license plates
If it locates a license plate and that license plate is valid (yet to impleent with data) then put
it into the database



INSTALLATION:

ALPR:
# Must install Alpr software via apt-get this installation includes the python package


PYTHON PACKAGES:
# Installing Paramiko
sudo apt-get install libffi6 libffi-dev
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo pip install cryptography
sudo pip3 install paramiko
sudo apt-get --reinstall install python-pyasn1 python-pyasn1-modules
#Installing ffmpy
sudp pip3 install ffmpy


RASPBERRY PI MEMORY:
sudo raspi-config
#Change "Advanced" -> "Memory Split" to 256

SCP:
#must install openssh-server on the receiving computer to perform scp
sudo apt-get install openssh-server
