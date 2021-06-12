from Mux import Mux
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

class muxWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/muxWindow.ui", self)

        self.pushRun.clicked.connect(self.runExperiment)
        self.numSweeps.setValidator(QtGui.QIntValidator())
        self.analyseOutput.clicked.connect(self.analyseData)

    def runExperiment(self):
        numSweeps = int(self.numSweeps.displayText())
        port = str(self.portName.displayText())

        sweeper = Mux(port)
        sweeper.sweepPlate(numSweeps)

        self.testDone.setStyleSheet("background-color: lightgreen")

    def analyseData(self):
        # TO DO: Call on ParseRadiantOP to do backend analysis on the data.
        return 0

app = QtWidgets.QApplication(sys.argv)
window = muxWindow()
window.show()
app.exec_()

