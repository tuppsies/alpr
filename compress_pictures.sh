# Resources:
#https://www.digitalocean.com/community/tutorials/how-to-use-sshfs-to-mount-remote-file-systems-over-ssh
#http://www.raspberrypi-spy.co.uk/2014/05/how-to-mount-a-usb-flash-disk-on-the-raspberry-pi/

#!/bin/bash

# this line stops the program reading it as literally *.jpg
shopt -s nullglob

while true;
do
    sleep 1
    for f in *.jpg
    do
        ffmpeg -loglevel quiet -i $f -r 1 /media/laptop/home/joshua/Desktop/Raspberry_Pi_Images/$f
        rm $f
        echo Compressed picture!
    done
done
