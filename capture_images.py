# this program uses the raspberry pi camera to capture images
# Created by Joshua Cahill on 3/6/2017

import picamera
from time import sleep

def main():
    camera = picamera.PiCamera()


    # take a picture unless interrupted
    while(true):
        sleep(1)
        print("potato")




main()
