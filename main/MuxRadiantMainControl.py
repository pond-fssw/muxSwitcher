from Mux import Mux
from ParseRadiantOP import RadiantParser

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

class muxWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/muxWindow.ui", self)
        
        self.testDone.setStyleSheet("background-color: red")
        self.pushRun.clicked.connect(self.runExperiment)
        self.numSweeps.setValidator(QtGui.QIntValidator())
        self.runParser.clicked.connect(self.analyseData)

    def runExperiment(self):
        numSweeps = int(self.numSweeps.displayText())
        # port = str(self.portName.displayText())
        port = "USB0::0x0957::0x0507::MY44004129::INSTR"
        dataFile = self.getJsonFile_Switcher()

        sweeper = Mux(port)

        if dataFile != 0:
            sweeper.sweepPlate(numSweeps)
            self.testDone.setStyleSheet("background-color: lightgreen")

    def analyseData(self):
        newFolderDirectory = str(self.filePath.displayText())
        newFolderName = str(self.folderName.displayText())
        rawResultFolder = str(self.rawResults.displayText())

        dataFile = self.getJsonFile_Parser()
        
        if dataFile != 0:
            RadiantParser(filePath=newFolderDirectory, newFolder=newFolderName, rawResultFolder=rawResultFolder)

    def getJsonFile_Parser(self):
        if self.dataMask1.isChecked():
            return "mask1.json"
        elif self.dataMask2.isChecked():
            return "mask2.json"
        elif self.dataMisc.isChecked():
            return "manualMask.json"
        else:
            self.setNotice_Parser("Please choose the appropriate mask option.")
            return 0

    def getJsonFile_Switcher(self):
        if self.switchMask1.isChecked():
            return "mask1.json"
        elif self.switchMask2.isChecked():
            return "mask2.json"
        elif self.switchMandual.isChecked():
            return "maskManual.json"
        else:
            self.setNotice_Switcher("Please choose the appropriate mask option.")

    def setNotice_Parser(self, notification):
        self.parserNotice.setText(notification)

    def setNotice_Switcher(self, notification):
        self.switchNotice.setText(notification)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = muxWindow()
    window.show()
    app.exec_()

