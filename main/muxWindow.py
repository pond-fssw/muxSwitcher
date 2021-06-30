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

    def runExperiment(self):
        numSweeps = int(self.numSweeps.displayText())
        # port = str(self.portName.displayText())
        port = "USB0::0x0957::0x0507::MY44004129::INSTR"

        sweeper = Mux(port)
        sweeper.sweepPlate(numSweeps)

        self.testDone.setStyleSheet("background-color: orange")
        
        self.analyseData()

    def analyseData(self):
        parentDirectory = str(self.filePath.displayText())
        newFolderName = str(self.folderName.displayText())
        rawResultFolder = str(self.rawResults.displayText())

        RadiantParser(filePath=parentDirectory, newFolder=newFolderName, rawResultFolder=rawResultFolder)

        self.testDone.setStyleSheet("background-color: lightgreen")

app = QtWidgets.QApplication(sys.argv)
window = muxWindow()
window.show()
app.exec_()

