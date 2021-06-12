# Only use sweepPlate! Can you even make methods private on Python?

from MuxChannelControl import MuxChannelController
from glob import glob
import time
from fileCreator import writeTextFile, numFilesIn
import numpy as np
import os

class Mux:
    def __init__(self, port):
        self.muxController = MuxChannelController(port)

    def sweepPlate(self, numSweeps):
        # Initial text file to trigger start.

        for electrodeID in (np.arange(50) + 1):
            self.startThisElectrode(electrodeID)    # Connects to this electrode.

            for sweepNumber in (np.arange(numSweeps) + 1):
                print("At electrode #" + str(electrodeID) + ", sweep #" + str(sweepNumber))
                self.triggerRadiantToStart()

                # While sweep is not done, keep progress in this loop.
                while not self.isRadiantSweepDone():
                    print("Sweep in progress.")
                    time.sleep(2)

                print("Sweep #" + str(sweepNumber) + " complete.")
                
                print("Waiting for Radian to reset.")
                time.sleep(10)
            
            self.doneWithElectrode(electrodeID)

    # Electrode ID corresponds to its column in MuxChannelControl
    def startThisElectrode(self, electrodeID):
        mux = self.muxController

        mux.breakContactAll() # Just as a precaution
        mux.makeContact(1, electrodeID)

    # Look for Radiant's file after it has been made.
    def isRadiantSweepDone(self):
        # If number of files more than original, return 1. If not, return 0.
        if (numFilesIn(r'C:\Users\anant\Desktop\Radiant Slave') > 0):
            return 1
        return 0

    def triggerRadiantToStart(self):
        writeTextFile(r'C:\DataSets\StartTest', 'Start', 'ready')

    def doneWithElectrode(self, electrodeID):
        mux = self.muxController
        mux.breakContact(1, electrodeID)

