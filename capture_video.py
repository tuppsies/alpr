# Python script to capture images

import picamera
import sys

def main():

    camera = picamera.PiCamera()
    camera.resolution = (1920, 1080)

    try:
        print("Beginning recording")
        camera.start_recording("myvideo.h264")
        # currently make a really long video until we are interrupted
        camera.wait_recording(3600)
        camera.stoprecording()
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
        print("Stopping video")
        camera.stoprecording()
        sys.exit()

main()
