#!/bin/bash

# without this line choas would break loose
shopt -s nullglob

while true; do

    #rsync -v --remove-source-files -e ssh *.jpg joshua@192.168.43.132:/home/joshua/Desktop/raspberry_pi_pictures/

    for f in *.jpg
    do
        rsync -v -e ssh $f joshua@192.168.43.132:/home/joshua/Desktop/raspberry_pi_pictures/
        rm $f
    done

done
