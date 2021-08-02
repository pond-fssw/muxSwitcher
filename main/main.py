from Mux import Mux
from ParseRadiantOP import RadiantParser

import sys, os, json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

class muxWindow(QtWidgets.QMainWindow):
    # C:\Users\Pond Posaphiwat\Frore Systems\RnD - Characterization\PZT testing\212701\2D\After Poling\Radiant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/muxWindow.ui", self)
        
        self.init_ui()

    def init_ui(self):
        self.pushRun.clicked.connect(self.runExperiment)
        self.runParser.clicked.connect(self.analyseDataOnlyParse)
        self.generateDropdown()

    def analyseDataOnlyParse(self):
        self.runParser.setEnabled(False)
        self.numSweepsInt = int(self.numSweeps_parser.value())
        self.analyseData()

    def generateDropdown(self):
        self.maskOptions = os.listdir("./masks/")
        for maskJson in self.maskOptions:
            maskJson = maskJson.replace(".json", "")
            self.maskOptionSwitcher.addItem(maskJson)
            self.maskOptionParser.addItem(maskJson)

    def runExperiment(self):
        checked = self.automaticallyParse.isChecked()
        maskData = self.parseJson("Switcher")
        self.numSweepsInt = int(self.numSweeps.value())
        port = "USB0::0x0957::0x0507::MY44004129::INSTR"

        self.pushRun.setEnabled(False)
        sweeper = Mux(maskData)
        sweeper.sweepPlate(self.numSweeps)

        if checked:
            self.analyseData()
        self.pushRun.setEnabled(True)

    def parseJson(self, switcherORparser):
        if switcherORparser=="Switcher":
            maskIndex = self.maskOptionSwitcher.currentIndex()
        else:
            maskIndex = self.maskOptionParser.currentIndex()

        maskFile = "./masks/" + self.maskOptions[maskIndex - 1]

        f = open(maskFile)
        data = json.load(f)
        
        return data

    def analyseData(self, auto=False):
        newFolderName = ""
        rawResultFolder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder With Raw Results')
        newFolderDirectory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder to Put Analysis')
        rawResultFolder = str(rawResultFolder)
        newFolderDirectory = str(newFolderDirectory)

        maskData = self.parseJson("Parser")
        RadiantParser(filePath=newFolderDirectory, newFolder=newFolderName, rawResultFolder=rawResultFolder, data=maskData, numSweeps=self.numSweepsInt)
        self.runParser.setEnabled(True)

    def setNotice(self, notification):
        self.notice.setText(notification)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = muxWindow()
    window.show()
    app.exec_()

