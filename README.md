# Data processor

## Requirements 

### 1. Bitalino
>pip3 install bitalino

### 2. Pybluez
>pip3 install pybluez

### 3. Osc4py3 
>pip3 install osc4py3

The aforementioned requirements are for linux users, other os might need other dependecies. Also sudo might be required depending on user.


## Running at boot time

Move launcher.sh to 
>/home/pi/Desktop/

Change current folder to
>cd /home/pi/Desktop/

Make launcher.sh executable
>chmod 755 launcher.sh 

Edit crotnab:
>sudo crontab -e 

Add the line:
>@reboot sh /home/pi/Desktop/launcher.sh >/home/pi/Desktop/logs/cronlog 2>&1