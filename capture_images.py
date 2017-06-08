# this program uses the raspberry pi camera to capture images
# Created by Joshua Cahill on 3/6/2017

import sys
import picamera
import os
from time import sleep


def main():

    # start the transfer shell script
    os.system("./transfer_pictures.sh &")

    camera = picamera.PiCamera()
    camera.resolution = (3264, 2448)

    # take a picture unless interrupted
    i = 0
    while(True):
        i += 1
        sleep(2)
        #print("Capturing image")
        camera.capture(str(i)+".jpg")



main()
