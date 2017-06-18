# Resources
# https://raspberrypi.stackexchange.com/questions/22040/take-images-in-a-short-time-using-the-raspberry-pi-camera-module
# http://picamera.readthedocs.io/en/release-1.10/api_camera.html

import os
import io
import time
import picamera
import paramiko

with picamera.PiCamera() as camera:

    # begin image compressor and transfer program
    os.system("./compress_pictures.sh &")


    #camera.resolution = (2592, 1944) # works fine for 5 megapixels
    camera.resolution = (3266,2450)
    camera.framerate = 30
    time.sleep(2)

    print("Beginning capture")
    # Set up 40 in-memory streams
    numPhotos = 100
    outputs = [io.BytesIO() for i in range(numPhotos)]


    start = time.time()

    # using the video port below brings out worse quality
    camera.capture_sequence(outputs, 'jpeg', use_video_port=False)
    finish = time.time()
    # How fast were we?
    print('Captured ' + str(numPhotos) + ' images at %.2ffps' % (numPhotos / (finish - start)))
    print('Time was: ' + str(finish-start))

    # create SSH connection
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('192.168.43.132', username='joshua')


    

    # then send the data over ssh to main computer
    # PROCESSING TIME IS HUGE IF IT HAS TO REWRITE THE FILES
    fileLocation = "/media/laptop/home/joshua/Desktop/Raspberry_Pi_Images/"
    print("Processing images from buffer")
    processingStart = time.time()
    for x in range(0, numPhotos -1):
        with open(str(x) +".jpg", "wb") as f:
            print("Completed an image")
            f.write(outputs[x].getvalue())

    processingEnd = time.time()
    print("Processing time was " + str(processingEnd - processingStart))
