
from ffmpy import FFmpeg
import os

storageLocation = "/media/laptop/home/joshua/Desktop/Raspberry_Pi_Images/"

for fileName in os.listdir():
    if fileName.endswith(".jpg"):
        print("Compressing and saving a photo")
        ff = FFmpeg(inputs={fileName:None},outputs={storageLocation+fileName:'-loglevel -8 -r 1'})
        ff.run()
print("Completed program")
