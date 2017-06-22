# Written by Joshua Cahill

# arg1 - directory location where images are stored

from openalpr import Alpr
import time
import os
import sys
import datetime
from datetime import datetime

primaryLanguageList=['au','auwide']
secondaryLanguageList=['eu','gb','kr''mx','sg','us']

# setup outputs files
debug = open(str((sys.argv)[1]) + "/debug.txt", 'w')
results = open(str((sys.argv)[1]) + "/results.txt", 'w')

# print date information to the files
date = str(time.strftime("%Y-%m-%d"))
print(str(datetime.now()), file = debug)
print(str(datetime.now()), file = results)

# define the image directory
imageDirectory = str((sys.argv)[1])


NOPLATE = "NO PLATE FOUND" # this should be a constant
finalPlate = NOPLATE
finalConfidence = 0
finalLanguage = "NO LANGUAGE"

def main():

    # declare global variables that we are going to use
    global finalPlate
    global finalConfidence
    global finalLanguage


    # TODO assert that we have been given an argument
    
    deli = " " # delimter for printing to files

    numFiles = calculate_num_files(imageDirectory)
    print("Number of files is: " + str(numFiles), file = debug)

    percentageComplete = 0

    counter = 0
    for fileName in os.listdir(imageDirectory):
        if fileName.endswith(".jpg"):
            finalPlate = NOPLATE
            finalConfidence = 0;
            finalLanguage = "NO LANGUAGE"
            check_primary_plate((imageDirectory + fileName),fileName)
            if(finalPlate != NOPLATE):
                print(str(finalPlate) + deli + str(finalLanguage) + deli + str(fileName), file = results)  
            counter += 1
            percentageComplete = round(counter/numFiles*100, 2)
            print("Completed: " + str(counter) + '/' + str(numFiles) + "   " + str(percentageComplete) + "%", end = '\r')
            


def check_primary_plate(fileLocation, fileName):
    print("-----Checking file: " + str(fileName) + "-----", file = debug)

    global finalConfidence
    global finalPlate
    global finalLanguage

    for language in primaryLanguageList:
        print("Checking language: " + language, file = debug)
        alpr = Alpr(language, "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
        alpr.set_top_n(6)
        results = alpr.recognize_file(fileLocation)
        
        for plate in results['results']:
            for candidate in plate['candidates']:
                currentPlate = candidate['plate']
                currentConfidence = candidate['confidence']
                print(str(currentPlate) + "\t" + str(currentConfidence), file = debug) # print each plate and its confidence level

                if currentConfidence > finalConfidence and validPlate(currentPlate):
                    finalPlate = currentPlate
                    finalConfidence = currentConfidence
                    finalLanguage = language
                    print("Plate is now " + str(finalPlate) + " with confidence " + str(finalConfidence), file = debug)


# check to see if a plate is valid
def validPlate(plate):
    valid = True
    if len(plate) > 6:
        valid = False
    return valid

# calculate the number of files in a given directory
def calculate_num_files(directory):
    counter = 0
    for file in os.listdir(directory):
        if file.endswith(".jpg"):
            counter+=1
    return counter


main()
