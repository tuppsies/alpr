# Resources
# https://raspberrypi.stackexchange.com/questions/22040/take-images-in-a-short-time-using-the-raspberry-pi-camera-module
# http://picamera.readthedocs.io/en/release-1.10/api_camera.html

import cProfile
import shutil
import os
import io
import time
import picamera
import paramiko
from ffmpy import FFmpeg
from time import strftime


with picamera.PiCamera() as camera:

    # begin image compressor and transfer program
    #os.system("./compress_pictures.sh &")

    numPhotos = 10 # the number of photos that we want the camera to take in a single go
    print("Setting up camera")
    #camera.resolution = (2592, 1944) # works fine for 5 megapixels
    camera.resolution = (3266,2450)
    camera.framerate = 30
    time.sleep(2)

    cameraCapture = open("cameraCapture.txt", "w")
    totalPhotos = 0
    cameraStart = time.time()

    imageCounter = 0 # used to create the image names
    while(True):
        
        outputs = [io.BytesIO() for i in range(numPhotos)]
        
        # using the video port below brings out worse quality
        print("Beginning capture")
        
        startTimeString = strftime("%Y-%m-%d %H:%M:%S")        
        start = time.time()
        camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
        endTimeString = strftime("%Y-%m-%d %H:%M:%S")
        finish = time.time()

        timeInterval = (finish-start)/10
        print("time interval is: " + str((finish-start)/10))
        photoTimes = []
        for i in range(1, numPhotos):
            photoTimes.append(start + (i * timeInterval))
        # print the array
        for i in range(1, numPhotos):
            print("Time for photo " + str(i) + " was " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(photoTimes[i-1])))

        # How fast were we?
        print('Captured ' + str(numPhotos) + ' images at %.2ffps' % (numPhotos / (finish - start)))
        print('Capture time was: ' + str(finish-start))

        totalPhotos += numPhotos


        # PROCESSING TIME IS HUGE IF IT HAS TO REWRITE THE FILES - maybe?
        fileLocation = "/media/laptop/home/joshua/Desktop/Raspberry_Pi_Images/"
        print("Processing images from buffer")
        processingStart = time.time()
        for x in range(0, numPhotos):

            with open(str(imageCounter) +".jpg", "wb") as f:
                #print("made it here")
                outputs[x].seek(0)
                #f.write(outputs[x].getvalue()) # this takes longer than shutil
                shutil.copyfileobj(outputs[x],f)
                #ff = FFmpeg(inputs={str(imageCounter)+".jpg":None},outputs={"result_"+str(imageCounter)+".jpg":'-r 1'})
                #ff.run()
                print("Writing to file " + str(f))
            imageCounter += 1
        print("In processing time")
        processingEnd = time.time()
        print("Processing time was " + str(processingEnd - processingStart))

        cameraEnd = time.time()
        cameraTimeSoFar = cameraEnd - cameraStart
        #print("capture time " + str(cameraTimeSoFar/totalPhotos))
