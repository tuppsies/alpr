
import requests
import logging
from bs4 import BeautifulSoup
import sys
from datetime import datetime


def main():
    
    siteURL = "https://my.service.nsw.gov.au/MyServiceNSW/index#/rms/freeRegoCheck/details"
    print("###Requesting site map access")
    siteMapSourceCode = requests.get(siteURL)
    siteMapPlainText = siteMapSourceCode.text
    siteMapSoup = BeautifulSoup(siteMapPlainText, "html.parser")
    print("Site map accessed")
    print(siteMapSoup)

main()
