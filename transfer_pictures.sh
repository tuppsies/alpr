#!/bin/bash

# without this line choas would break loose
shopt -s nullglob

while true; do
    for f in *.jpg
    do
        scp $f joshua@192.168.43.132:/home/joshua/Desktop/
        rm $f
    done
done
