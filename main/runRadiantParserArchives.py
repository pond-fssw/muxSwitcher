from ParseRadiantOP import RadiantParser

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

class parserWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/runDataParser.ui", self)
        
        self.runParser.clicked.connect(self.analyseData)

    def analyseData(self):
        self.done.setText("No")
        
        newFolderDirectory = str(self.outputResultPath.displayText())
        newFolderName = str(self.newFolderName.displayText())
        rawResultFolder = str(self.rawDataPath.displayText())

        RadiantParser(newFolderDirectory, newFolder=newFolderName, rawResultFolder=rawResultFolder)

        self.done.setText("Yes")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = parserWindow()
    window.show()
    app.exec_()