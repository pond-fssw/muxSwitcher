from DataSetFormat import DataSetFormatter
from FormatRadiantOP import RadiantOPFormatter
from analyseSweep import sweepAnalyser

import matplotlib.pyplot as plt
import numpy as np
import csv
import os

class RadiantParser:
    def __init__(self, filePath, newFolder, rawResultFolder, data, numSweeps):
        self.parseJson(data, numSweeps)
        self.directory = filePath + '/'
        self.plotPath = os.path.join(self.directory, "Plots")
        os.mkdir(self.plotPath)

        f = open(self.directory + "Test_Data.csv", mode='a', newline='')
        self.writer = csv.writer(f)

        if self.sweepType == "Monopolar":
            monopolarHeader = ["Electrode Name", "Group", "Electrode Number",
            "Delta Charge 1", "Delta Charge 2", "Delta Charge 3", "Delta Charge Mean", "Delta Charge SD", 
            "Polarization at Max E 1", "Polarization at Max E 2", "Polarization at Max E 3", "Polarization at Max E Mean", "Polarization at Max E SD", 
            "Loop Area 1", "Loop Area 2", "Loop Area 3", "Loop Area Mean", "Loop Area SD", "Derivative Up", "Derivative Down", 
            "Loop Overlap 1-2", "Loop Overlap 2-3", "Loop Overlap 1-3"]
            self.analyseMonopolar(monopolarHeader, rawResultFolder)
        elif self.sweepType == "Bipolar":
            print("it is")
            bipolarHeader = self.bipolarHeader()
            self.analyseBipolar(bipolarHeader, rawResultFolder)

        print("Analysis complete. file.csv made in location")

    def analyseMonopolar(self, header, rawFolder):
        self.writer.writerow(header)
        self.electrodeNumber = 0
        dataSets, names = self.compile(rawFolder)
        self.analyse(dataSets)

    def analyseBipolar(self, header, rawFolder):
        print("yo")
        self.writer.writerow(header)
        self.electrodeNumber = 0
        dataSets, names = self.compile(rawFolder)
        self.analyse(dataSets)
    
    def bipolarHeader(self):
        self.driveFields = ["50 kV/cm", "100 kV/cm", "150 kV/cm", "200 kV/cm", "250 kV/cm", "300 kV/cm"]
        featuredProperties = ["Pr Max", "Pr+", "Pr-", "Ec+", "Ec-", "Imprint", "Loop Area"]
        bipolarHeader = ["Electrode Name"]
        
        for driveField in self.driveFields:
            props = [driveField]
            props += featuredProperties
            bipolarHeader += props

        return bipolarHeader

    def parseJson(self, data, numSweeps):
        self.numSweeps = numSweeps
        self.groups = data["Groups"]
        self.electrodes = data["Electrodes"]
        self.sweepType = data["Type"]   # Monopolar or Bipolar

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
            formatter = RadiantOPFormatter(dataFile, self.sweepType)
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
                if self.sweepType == "Monopolar":
                    self.analyseElectrode(sweepsOfThisElectrode, dataSets, groupNumber, electrodeNumber)
                elif self.sweepType == "Bipolar":
                    self.analyseElectrodeBipolar(sweepsOfThisElectrode, dataSets, groupNumber, electrodeNumber)
    
    def analyseElectrodeBipolar(self, sweepIndices, dataSets, groupNumber, electrodeNumber):
        electrodeResults = []
        fields = []
        polarizations = []

        for index in sweepIndices:
            sweepDataSet = dataSets[index]
            sweep = sweepAnalyser(sweepDataSet, self.sweepType)
            sweepResults = sweep.getResultsBipolar()

            fields.append(sweepDataSet.Field)
            polarizations.append(sweepDataSet.Polarization)
            electrodeResults.append(sweepResults)
####################################################
        electrodeNumber = electrodeNumber + 1
        electrodeName = self.electrodes[self.electrodeNumber]
        self.writeResultsBipolar(electrodeName, groupNumber, electrodeNumber, electrodeResults)
        self.electrodeNumber += 1

        filePath = 0
        self.plotAndSave(fields, polarizations, filePath, groupNumber, electrodeNumber, electrodeResults)
        # filePath = self.plotPath + str(groupNumber) + "no" + str(electrodeNumber) + ".png"
        # self.plotAndSave(fields, polarizations, filePath, groupNumber, electrodeNumber)

    def analyseElectrode(self, sweepIndices, dataSets, groupNumber, electrodeNumber):
        electrodeResults = []
        fields = []
        polarizations = []

        for index in sweepIndices:
            sweepDataSet = dataSets[index]
            sweep = sweepAnalyser(sweepDataSet, self.sweepType)
            sweepResults = sweep.getResults()

            fields.append(sweepDataSet.Field)
            polarizations.append(sweepDataSet.Polarization)
            electrodeResults.append(sweepResults)

        processedResults, yInt, polMaxE, loopArea = self.compileResults(electrodeResults)
        electrodeNumber = electrodeNumber + 1
        electrodeName = self.electrodes[self.electrodeNumber]
        self.writeResults(electrodeName, groupNumber, electrodeNumber, processedResults, yInt, polMaxE, loopArea)
        self.electrodeNumber += 1

        filePath = self.plotPath + str(groupNumber) + "no" + str(electrodeNumber) + ".png"
        self.plotAndSave(fields, polarizations, filePath, groupNumber, electrodeNumber)

    def writeResults(self, electrodeName, group, channel, processedResults, yInt, polMaxE, loopArea):
        writer = self.writer

        data = [electrodeName, group, channel, 
        yInt[0], yInt[1], yInt[2], processedResults[0], processedResults[1], 
        polMaxE[0], polMaxE[1], polMaxE[2], processedResults[2], processedResults[3], 
        loopArea[0], loopArea[1], loopArea[2], processedResults[4], processedResults[5], 
        processedResults[6], processedResults[7]]

        writer.writerow(data)

    def writeResultsBipolar(self, electrodeName, group, channel, results):
        row = [electrodeName]
        for sweepData in results:
            row += " "
            #####################################
            row += sweepData
        print(len(row))
        self.writer.writerow(row)

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

    def plotAndSave(self, field, polarization, filePath, groupNum, electrodeNum, results=0):
        plt.clf()

        if self.sweepType == "Monopolar":
            for i in np.arange(len(field)):
                plt.plot(field[i], polarization[i], label=("Sweep " + str(i+1)), linewidth=1)

            plt.xlabel("Field Applied [kV/cm]")
            plt.ylabel("Measured Polarization")
            plt.title("Electron from " + str(groupNum) + ", Number " + str(electrodeNum))
            plt.legend()

            plt.savefig(filePath, bbox_inches='tight', dpi=1200)

        elif self.sweepType == "Bipolar":
            # Make this electrode's plot directory
            dirName = str(groupNum) + "-" + str(electrodeNum)
            electrodePlotDir = os.path.join(self.plotPath, dirName)
            os.mkdir(electrodePlotDir)

            self.makeBipolarPlots(field, polarization, electrodePlotDir, results)

    def makeBipolarPlots(self, field, polarization, electrodePlotDir, results):
        driveFields = [50, 100, 150, 200, 250, 300]
        # Plot the following against the drive field
        plt.clf()

        # All sweeps
        pngFile = "/Complete.png"
        for i, driveField in zip(np.arange(len(field)), driveFields):
            plt.plot(field[i], polarization[i], label=(str(driveField) + "kV/cm Drive Field"), linewidth=1)

        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Test Results")
        plt.legend()

        plt.savefig(electrodePlotDir + pngFile, bbox_inches='tight', dpi=1200)
        
        # Ref: ["Pr Max", "Pr+", "Pr-", "Ec+", "Ec-", "Imprint", "Loop Area"]
        pr_max = []
        pr_p = []
        pr_n = []
        ec_p = []
        ec_n = []
        imprint = []
        loopArea = []
    
        for sweepData in results:
            pr_max.append(sweepData[0])
            pr_p.append(sweepData[1])
            pr_n.append(sweepData[2])
            ec_p.append(sweepData[3])
            ec_n.append(sweepData[4])
            imprint.append(sweepData[5])
            loopArea.append(sweepData[6])

        # Pr+ and Pr-
        plt.clf()
        pngFile = "/Pr.png"
        
        plt.scatter(driveFields, pr_p, label="Pr+")
        plt.scatter(driveFields, pr_n, label="Pr-")
        
        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Test Results")
        plt.legend()

        plt.savefig(electrodePlotDir + pngFile, bbox_inches='tight', dpi=1200)

        # Ec+ and Ec- 
        plt.clf()
        pngFile = "/Ec.png"
        
        plt.scatter(driveFields, ec_p, label="Ec+")
        plt.scatter(driveFields, ec_n, label="Ec-")
        
        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Test Results")
        plt.legend()

        plt.savefig(electrodePlotDir + pngFile, bbox_inches='tight', dpi=1200)

        # Pmax
        plt.clf()
        pngFile = "/Pr Max.png"
        
        plt.scatter(driveFields, pr_max, label="Ec+")
        
        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Test Results")
        #plt.legend()

        plt.savefig(electrodePlotDir + pngFile, bbox_inches='tight', dpi=1200)

        # Loop Area
        plt.clf()
        pngFile = "/Loop Area.png"
        
        plt.scatter(driveFields, loopArea, label="")
        
        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Test Results")
        #plt.legend()

        plt.savefig(electrodePlotDir + pngFile, bbox_inches='tight', dpi=1200)

        # Imprint (Ec+ - Ec-)/2
        plt.clf()
        pngFile = "/Imprint.png"
        
        plt.scatter(driveFields, imprint, label="")
        
        plt.xlabel("Field Applied [kV/cm]")
        plt.ylabel("Measured Polarization")
        plt.title("Test Results")
        #plt.legend()

        plt.savefig(electrodePlotDir + pngFile, bbox_inches='tight', dpi=1200)
