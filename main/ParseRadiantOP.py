from DataSetFormat import DataSetFormatter
from FormatRadiantOP import RadiantOPFormatter
from analyseSweep import sweepAnalyser

import matplotlib.pyplot as plt
import numpy as np
import csv
import os

class RadiantParser:
    def __init__(self, parentDirectory, newFolder, rawResultFolder):
        # Make directories
        parentDir = parentDirectory
        directory = newFolder
        path = os.path.join(parentDir, directory)
        os.mkdir(path)
        self.directory = parentDir + "/" + directory + "/"

        plotPath = os.path.join(self.directory, "plots")
        os.mkdir(plotPath)

        f = open(self.directory + "Test_Data.csv", mode='a')
        self.writer = csv.writer(f, delimiter=',')
        # self.writer.writerow(["Electrode Name", "Group", "Electrode Number", "Delta Charge Mean", "Delta Charge SD", "Polarization at Max E Mean", "Polarization at Max E SD", "Loop Area Mean", "Loop Area SD", "Derivative Up", "Derivative Down", "Loop Overlap 1-2", "Loop Overlap 2-3", "Loop Overlap 1-3"])
         
        self.writer.writerow(["Electrode Name", "Group", "Electrode Number",
        "Delta Charge 1", "Delta Charge 2", "Delta Charge 3", "Delta Charge Mean", "Delta Charge SD", 
        "Polarization at Max E 1", "Polarization at Max E 2", "Polarization at Max E 3", "Polarization at Max E Mean", "Polarization at Max E SD", 
        "Loop Area 1", "Loop Area 2", "Loop Area 3", "Loop Area Mean", "Loop Area SD", "Derivative Up", "Derivative Down", 
        "Loop Overlap 1-2", "Loop Overlap 2-3", "Loop Overlap 1-3"]) 
    
        self.electrodeNumber = 0
        self.mask = self.getElectrodeNamesMask1()

        dataSetGroup1, dataSetGroup2, dataSetGroup3, dataSetGroup4 = self.compile(rawResultFolder)
        self.analyse([dataSetGroup1, dataSetGroup2, dataSetGroup3, dataSetGroup4])

        print("Analysis complete. file.csv made in location")

    def compile(self, rawResultFolder):
        # File path of data for each group
        print("Analysis start.")
        print("Compiling...")

        dataGroup1 = rawResultFolder + "/group1_data.txt"
        dataGroup2 = rawResultFolder + "/group2_data.txt"
        dataGroup3 = rawResultFolder + "/group3_data.txt"
        dataGroup4 = rawResultFolder + "/group4_data.txt"

        formatterGroup1 = RadiantOPFormatter(dataGroup1)
        formatterGroup2 = RadiantOPFormatter(dataGroup2)
        formatterGroup3 = RadiantOPFormatter(dataGroup3)
        formatterGroup4 = RadiantOPFormatter(dataGroup4)

        dataSetGroup1 = formatterGroup1.returnDataSets()
        dataSetGroup2 = formatterGroup2.returnDataSets()
        dataSetGroup3 = formatterGroup3.returnDataSets()
        dataSetGroup4 = formatterGroup4.returnDataSets()

        print("Done compiling data.")
        
        return dataSetGroup1, dataSetGroup2, dataSetGroup3, dataSetGroup4

    def analyse(self, dataSets):
        print("Analysis started.")
        groupNumber = 1

        for dataSet in dataSets:
            self.analysePerGroup(dataSet, groupNumber)
            groupNumber += 1
    
    # Write header if it is the first of its group.
    def analysePerGroup(self, dataSets, groupNumber):
            numSweepsTotal = len(dataSets)
            numElectrodes = numSweepsTotal//3

            for electrodeNumber in np.arange(numElectrodes):
                start = electrodeNumber * 3
                sweepsOfThisElectrode = [start, start+1, start+2]

                # This is for each electrode (per 3 sweeps)
                self.analyseElectrode(sweepsOfThisElectrode, dataSets, groupNumber, electrodeNumber)
    
    def analyseElectrode(self, sweepIndices, dataSets, groupNumber, electrodeNumber):
        electrodeResults = []
        fields = []
        polarizations = []

        for index in sweepIndices:
            sweepDataSet = dataSets[index]
            sweep = sweepAnalyser(sweepDataSet)
            sweepResults = sweep.getResults()

            fields.append(sweepDataSet.Field)
            polarizations.append(sweepDataSet.Polarization)
            electrodeResults.append(sweepResults)

        processedResults, yInt, polMaxE, loopArea = self.compileResults(electrodeResults)
        electrodeNumber = electrodeNumber + 1
        electrodeName = self.mask[self.electrodeNumber]
        self.writeResults(electrodeName, groupNumber, electrodeNumber, processedResults, yInt, polMaxE, loopArea)
        self.electrodeNumber += 1

        filePath = self.directory + "/plots/" + str(groupNumber) + "no" + str(electrodeNumber) + ".png"
        self.plotAndSave(fields, polarizations, filePath, groupNumber, electrodeNumber)

    def writeResults(self, electrodeName, group, channel, processedResults, yInt, polMaxE, loopArea):
        writer = self.writer

#        self.writer.writerow(["Electrode Name", "Group", "Electrode Number",
#        "Delta Charge 1", "Delta Charge 2", "Delta Charge 3", "Delta Charge Mean", "Delta Charge SD", 
#        "Polarization at Max E Mean", "Polarization at Max E SD", 
#        "Loop Area Mean", "Loop Area SD", "Derivative Up", "Derivative Down", 
#        "Loop Overlap 1-2", "Loop Overlap 2-3", "Loop Overlap 1-3"]) 

        data = [electrodeName, group, channel, 
        yInt[0], yInt[1], yInt[2], processedResults[0], processedResults[1], 
        polMaxE[0], polMaxE[1], polMaxE[2], processedResults[2], processedResults[3], 
        loopArea[0], loopArea[1], loopArea[2], processedResults[4], processedResults[5], 
        processedResults[6], processedResults[7]]

        writer.writerow(data)

    def compileResults(self, electrodeResults):
        yInt, polMaxE, loopArea, derUp, derDown = [], [], [], [], []
        
        # [self.yInt, self.polMaxE, self.loopArea, self.derUp, self.derDown]
        for sweepResults in electrodeResults:
            yInt.append(sweepResults[0])
            polMaxE.append(sweepResults[1])
            loopArea.append(sweepResults[2])
            derUp.append(sweepResults[3].tolist())
            derDown.append(sweepResults[4].tolist())

        yIntMean, polMaxEMean, loopAreaMean = np.mean(yInt), np.mean(polMaxE), np.mean(loopArea)
        yIntSD, polMaxESD, loopAreaSD = np.std(yInt), np.std(polMaxE), np.std(loopArea)

        return [yIntMean, yIntSD, polMaxEMean, polMaxESD, loopAreaMean, loopAreaSD, derUp, derDown], yInt, polMaxE, loopArea

    def plotAndSave(self, field, polarization, filePath, groupNum, electrodeNum):
        plt.clf()

        plt.plot(field[0], polarization[0], color='b', label="Sweep 1")
        plt.plot(field[1], polarization[1], color='g', label="Sweep 2")
        plt.plot(field[2], polarization[2], color='r', label="Sweep 3")

        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Electron from Group " + str(groupNum) + ", Number " + str(electrodeNum))
        plt.legend()

        plt.savefig(filePath, bbox_inches='tight')

    def getElectrodeNamesMask1(self):
        electrodes = ["'1-1", "'1-2", "'1-3", "'1-4",
        "'2-2", "'2-4", "'3-1", "'3-2", "'3-3", "'3-4", "'4-2", "'4-4",
        "K1-1", "K1-2", "K2-1", "K2-2",
        "F-1", "F-2", "F-3", "F-4", "F-5", "F-6", "F-7", "F-8", "F-9", "F-10",
        "F-11", "F-12", "F-13", "F-14", "F-15", "F-16", "F-17", "F-18",
        "UC-1L", "UC-1R", "UC-2L", "UC-2R", "UC-3L", "UC-3R", "UC-4L", "UC-4R",
        "UC-5L", "UC-5R", "UC-6L", "UC-6R", "UC-7L", "UC-7R", "UC-8L", "UC-8R"]

        print(len(electrodes))

        return electrodes