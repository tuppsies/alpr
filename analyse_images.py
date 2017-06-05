# This program was written by Joshua Cahill to recognise license plate numbers

from openalpr import Alpr
import time
import os
import sys
import datetime
from datetime import datetime


global languageListSuccess
global languageList
global invalidPlates
languageListSuccess= [0] * 12
invalidPlates= ['POLICE', 'P0LICE']
languageList= ['au', 'br', 'fr', 'kr2', 'mx', 'us', 'auwide', 'eu', 'gb', 'kr', 'sg', 'vn2']

# change the debug files depending on whether we are using video or photo analyser
if(str((sys.argv)[2]) == "v"):
    debug = open('/home/pi/LicensePlateRecognition/videoAnalysis/data/debug.txt', 'w')
    results = open('/home/pi/LicensePlateRecognition/videoAnalysis/data/results.txt', 'w')
elif(str((sys.argv)[2]) == "p"):
    debug = open('/home/pi/LicensePlateRecognition/photoAnalysis/data/debug.txt', 'w')
    results = open('/home/pi/LicensePlateRecognition/photoAnalysis/data/results.txt', 'w')

# print the date information to the files
date = str(time.strftime("%Y-%m-%d"))
print(str(datetime.now()), file = debug)
print(str(datetime.now()), file = results)

def main():

    # TO DO assert that we have been given an arguement
    imageDirectory = str((sys.argv)[1])
    print("Image directory is: " + imageDirectory, file = debug)

    numFiles = calculate_num_files(imageDirectory)
    print("Number of files is: " + str(numFiles), file = debug)

    i = 0
    percentageComplete = 0
    for file in os.listdir(imageDirectory):
        if file.endswith(".jpg"):
            imageLocation = imageDirectory + "/" + file
            get_oz_plate(imageLocation, file)
        i+=1
        percentageComplete = round(i/numFiles*100, 2)
        print("Completed: " + str(i) + '/' + str(numFiles) + "   " + str(percentageComplete) + "%", end = '\r')
    print_language_success()
    print("\n")
    print(str(datetime.now()), file = debug)
    print(str(datetime.now()), file = results)
    results.close()
    debug.close()

def get_oz_plate(imageLocation, fileName):
    print("-----Checking file: " + str(fileName) + "-----", file = debug)
    finalLanguage = ""
    finalPlate = "NO PLATE FOUND"
    finalConfidence = 0

    for language in "au", "auwide":
        print("Checking language: " + language, file = debug)
        alpr = Alpr(language, "/etc/openalpr/openalpr.conf", "/usr/local/share/openalpr/runtime_data")
        alpr.set_top_n(6)
        results = alpr.recognize_file(imageLocation)
        for plate in results['results']:
            for candidate in plate['candidates']:
                currentPlate = candidate['plate']
                currentConfidence = candidate['confidence']
                print(str(currentPlate) + "\t" + str(currentConfidence), file = debug)

                if len(currentPlate) == 6 and currentConfidence > finalConfidence and validPlate(currentPlate):
                   finalLanguage = language 
                   finalPlate = currentPlate
                   finalConfidence = currentConfidence
                   print("Plate is now " + str(finalPlate) + " with confidence " + str(finalConfidence), file = debug)

    if finalLanguage == "au":
        check_plate(finalPlate, 0, fileName)
    elif finalLanguage == "auwide":
        check_plate(finalPlate, 6, fileName)
    else:
        get_world_plate(imageLocation, fileName)
	

def get_world_plate(imageLocation, fileName):

    finalPlate = "NO PLATE FOUND"
    finalPlateConfidence = 0
    languageCounter = 0
    selectedLanguage = 0
    
    for language in languageList:
        if language == "au" or language == "auwide":
           continue

        print("Checking language: " + str(language), file = debug)      
        alpr = Alpr(language, "/etc/openalpr/openalpr.conf", "/usr/local/share/openalpr/runtime_data")
        alpr.set_top_n(6)    
        results = alpr.recognize_file(imageLocation)


        for plate in results['results']:
            for candidate in plate['candidates']:
                currentPlate = candidate['plate']
                currentConfidence = candidate['confidence']
                print(str(currentPlate) + "\t" + str(currentConfidence), file = debug)

                if len(currentPlate) == 6 and currentConfidence > finalPlateConfidence and validPlate(currentPlate):
                    finalPlateConfidence = currentConfidence
                    finalPlate = currentPlate
                    selectedLanguage = languageCounter

        languageCounter += 1

        
    alpr.unload()

    check_plate(finalPlate, selectedLanguage, fileName)

    
# if the plate is found in the text file then it returns 1
def validPlate(licensePlate):
    licensePlateList = open('/home/pi/LicensePlateRecognition/licensePlateList.txt', 'r')
    licensePlate = str(licensePlate)
    for line in licensePlateList:
        if licensePlate in line:
            licensePlateList.close()
            return True
    licensePlateList.close()
    return False        


# assert that the plate is legit
def check_plate(licensePlate, countryNum, fileName):
    delim = "\t"
    if len(licensePlate) > 6:
        return

    # if the plate is one that can be commonly mistaken
    if licensePlate in invalidPlates:
        return

    # increase the count of successfu locks
    languageListSuccess[countryNum] += 1
    

    print(str(licensePlate) + delim + str(languageList[countryNum]) + delim + str(fileName), file = results)
    print("%s%12s" % (licensePlate, fileName), file = debug)


def print_language_success():
    print("---------------", file = debug)
    i = 0
    for language in languageList:
        print(language + "\t" + str(languageListSuccess[i]), file = debug)
        i+=1

def calculate_num_files(directory):
    counter = 0
    for file in os.listdir(directory):
        counter+=1
    return counter

main()
