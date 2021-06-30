# Only use sweepPlate! Can you even make methods private on Python?

from MuxChannelControl import MuxChannelController
from glob import glob
import time
from fileCreator import writeTextFile, numFilesIn
import numpy as np

class Mux:
    def __init__(self, port):
        self.muxController = MuxChannelController(port)

    def sweepPlate(self, numSweeps):
        self.closeBridges()
        self.dischargePlate()

        testCount = 0

        for electrodeID in (np.arange(50) + 1):
            self.startThisElectrode(electrodeID)    # Connects to this electrode.

            for sweepNumber in (np.arange(numSweeps) + 1):
                testCount += 1
                self.dischargeChannel()

                print("At electrode #" + str(electrodeID) + ", sweep #" + str(sweepNumber) + ", overall test #" + str(testCount))
                self.triggerRadiantToStart()

                # While sweep is not done, keep progress in this loop.
                while not self.isRadiantSweepDone():
                    print("Sweep in progress.")
                    time.sleep(2)

                print("Sweep #" + str(sweepNumber) + " complete.")
                
                # While it has not been reset, wait in loop.
                while not self.isRadiantReset():
                    print("Waiting for Radiant to reset.")
                    time.sleep(1)

                print("Radiant is reset.")
            
            self.doneWithElectrode(electrodeID)

        self.shutDownProtocol()

    def dischargePlate(self):
        mux = self.muxController
        print("Discharge protocol in progress.")
        
        mux.makeContact(1, 70)
        time.sleep(1)
        mux.breakContact(1, 70)

        print("Plate discharged.")

    def dischargeChannel(self):
        mux = self.muxController
        
        mux.makeContact(1, 70)
        time.sleep(0.5)
        mux.breakContact(1, 70)

        print("Channel discharged.")

    # Returns 1 if Radiant has been reset!
    def isRadiantReset(self):
        if (numFilesIn(r'C:\Users\anant\Desktop\Radiant Slave') == 0):
            return 1
        return 0

    def closeBridges(self):
        mux = self.muxController

        mux.breakContactAll()
        mux.makeContact(1, 913)
        mux.makeContact(1, 923)
        print("Woah! Bridge Closed")

    # Electrode ID corresponds to its column in MuxChannelControl
    def startThisElectrode(self, electrodeID):
        mux = self.muxController
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

    def shutDownProtocol(self):
        mux = self.muxController
        mux.breakContactAll()

        print("All contact points open. Close down complete.")