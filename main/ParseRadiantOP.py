from DataSetFormat import DataSetFormatter
from FormatRadiantOP import RadiantOPFormatter
from analyseSweep import sweepAnalyser

import matplotlib.pyplot as plt
import numpy as np
import csv
import os

class RadiantParser:
    def __init__(self, filePath, newFolder, rawResultFolder, data, numSweeps):
        # Make directories
        self.parseJson(data, numSweeps)
        # parentDir = filePath
        # directory = newFolder
        # path = os.path.join(parentDir, directory)
        # os.mkdir(path)
        # self.directory = parentDir + "/" + directory + "/"
        self.directory = filePath + '/'
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

        dataSets, names = self.compile(rawResultFolder)
        self.analyse(dataSets)

        print("Analysis complete. file.csv made in location")

    def parseJson(self, data, numSweeps):
        self.numSweeps = numSweeps
        self.groups = data["Groups"]
        self.electrodes = data["Electrodes"]

    def compile(self, rawResultFolder):
        # File path of data for each group
        print("Analysis start.")
        print("Compiling...")

        dataFiles = []
        names = []
        for entry in os.scandir(rawResultFolder):
            if (entry.path.endswith(".txt") and entry.is_file()):
                name = str(entry.path).replace(rawResultFolder, '')
                name = str(name).replace('.txt', '')
                name = str(name).replace("\\", '')
                print(name)
                dataFiles.append(entry.path)
                dataFiles.sort()
                names.append(name)

        dataSets = []
        for dataFile in dataFiles:
            formatter = RadiantOPFormatter(dataFile)
            dataSets.append(formatter.returnDataSets())

        print("Done compiling data.")
        
        return dataSets, names

    def analyse(self, dataSets):
        print("Analysis started.")

        for dataSet, group in zip(dataSets, self.groups):
            self.analysePerGroup(dataSet, group)
    
    # Write header if it is the first of its group.
    def analysePerGroup(self, dataSets, groupNumber):
            numSweepsTotal = len(dataSets)
            numElectrodes = numSweepsTotal//self.numSweeps

            for electrodeNumber in np.arange(numElectrodes):
                start = electrodeNumber * self.numSweeps
                sweepsOfThisElectrode = np.arange(start, start+self.numSweeps)

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
        electrodeName = self.electrodes[self.electrodeNumber]
        self.writeResults(electrodeName, groupNumber, electrodeNumber, processedResults, yInt, polMaxE, loopArea)
        self.electrodeNumber += 1

        filePath = self.directory + "/plots/" + str(groupNumber) + "no" + str(electrodeNumber) + ".png"
        self.plotAndSave(fields, polarizations, filePath, groupNumber, electrodeNumber)

    def writeResults(self, electrodeName, group, channel, processedResults, yInt, polMaxE, loopArea):
        writer = self.writer

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

        for i in np.arange(len(field)):
            plt.plot(field[i], polarization[i], label=("Sweep " + str(i+1)), linewidth=1)

        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Electron from " + str(groupNum) + ", Number " + str(electrodeNum))
        plt.legend()

        plt.savefig(filePath, bbox_inches='tight', dpi=1200)