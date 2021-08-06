# Initializing formatter stores all available data in array. 
# API: returnDataSets returns a list of dataSet objects.
# Values can be returned using dataSetObj.returnPoints, etc.
import numpy as np
from DataSetFormat import DataSetFormatter

class RadiantOPFormatter:
    def __init__(self, dataFileDirectory, sweepType):
        self.sweepType = sweepType
        self.file = open(dataFileDirectory, "r")
        self.dataSets = []
        self.offsets = []
        self.parseResults()
        self.area

    def parseResults(self):
        thisIsData = False
        areaNotFound = True

        for line in self.file:
            if thisIsData == True:
                if line.isspace():
                    thisIsData = False
                    self.dataSets.append(thisDataSet)
                else:
                    self.saveDataPoints(thisDataSet, line)
            elif areaNotFound:
                areaFound = self.findArea(line)
                if areaFound:
                    areaNotFound = False
            elif self.findOffset(line):
                continue
            elif self.findNumPoints(line):
                continue
            elif line.strip() == 'Point	Time (ms)	Field (kV/cm)	Measured Polarization':
                thisIsData = True
                thisDataSet = DataSetFormatter(self.nextSetNumPoints)

        print("Done classifying.")

        if self.sweepType is "Monopolar":
            for dataSet, offset in zip(self.dataSets, self.offsets):
                dataSet.addOffset(offset)

        print("Done applying offset.")

    def saveDataPoints(self, thisDataSet, line):
        p, t, f, pol = line.split(maxsplit=4)
        thisDataSet.addDataPoint(p, t, f, pol)

    def findNumPoints(self, line):
        result = line.find("Points:")

        if result != -1: 
            numPoints = int(line[8:])
            self.nextSetNumPoints = numPoints
            return True
        
        return False

    def findArea(self, line):
        result = line.find("Sample Area (cm2):")

        if result != -1:
            area = float(line[18:])
            self.area = area
            return True
        
        return False

    def findOffset(self, line):
        result = line.find("Offset")

        if result != -1:
            offset = float(line[17:])
            self.offsets.append(offset)
            return True 

        return False

    def returnDataSets(self):
        return self.dataSets

    def returnArea(self):
        return self.area

