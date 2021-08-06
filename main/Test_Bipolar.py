from Mux import Mux
from ParseRadiantOP import RadiantParser

import sys, os, json

def parseJson(self, switcherORparser):
    if switcherORparser=="Switcher":
        
        maskIndex = self.maskOptionSwitcher.currentIndex()
    else:
        maskIndex = self.maskOptionParser.currentIndex()

    maskFile = "./masks/" + self.maskOptions[maskIndex - 1]

    f = open(maskFile)
    data = json.load(f)
    
    return data

newFolderName = ""

rawResultFolder = r"C:\Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\Mux Switcher Test\Radiant Output\bipolar2"
newFolderDirectory = r"C:\Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\Mux Switcher Test\Mux Output\bTest2"

# rawResultFolder = r"C:\Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\Mux Switcher Test\Radiant Output\monpolar"
# newFolderDirectory = r"C:\Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\Mux Switcher Test\Mux Output\mTest"

rawResultFolder = str(rawResultFolder)
newFolderDirectory = str(newFolderDirectory)

f = open("masks/(Test) Manual - Bipolar.json")
maskData = json.load(f)

RadiantParser(filePath=newFolderDirectory, newFolder=newFolderName, rawResultFolder=rawResultFolder, data=maskData, numSweeps=6)
