# Resources
# https://raspberrypi.stackexchange.com/questions/22040/take-images-in-a-short-time-using-the-raspberry-pi-camera-module
# http://picamera.readthedocs.io/en/release-1.10/api_camera.html


import io
import time
import picamera

with picamera.PiCamera() as camera:
    # Set the camera's resolution to VGA @40fps and give it a couple
    # of seconds to measure exposure etc.
    #camera.resolution = (2592, 1944) # works fine for 5 megapixels
    camera.resolution = (3266,2450)
    camera.framerate = 30
    time.sleep(2)

    print("Beginning program")
    # Set up 40 in-memory streams
    outputs = [io.BytesIO() for i in range(15)]
    start = time.time()

    # using the video port below brings out worse quality
    camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
    finish = time.time()
    # How fast were we?
    print('Captured x images at %.2ffps' % (40 / (finish - start)))


    # then send the data over ssh to main computer

    with open("data.jpg", "wb") as f:
        f.write(outputs[0].getvalue())

    print("Program complete")
