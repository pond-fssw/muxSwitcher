import time
import visa 

class MuxChannelController:
    def __init__(self, port):
        # Initialize system
        rm = visa.ResourceManager()
        mux = rm.open_resource(port)
        self.mux = mux

        self.resetMux()
        time.sleep(.1)

        self.closeBridgeInit()
        time.sleep(.1)

    # Close bridge as part of measurement protocol
    def closeBridgeInit(self):
        mux = self.mux
        self.makeContact(1, 913)
        self.makeContact(1, 923)

    def resetMux(self):
        mux = self.mux

        mux.write('*CLS')
        mux.write('*RST')

    # Closes corresponding channel (rol and col maps to electrode)
    def makeContact(self, row, col):
        mux = self.mux

        if col < 10:
            mux.write('ROUTe:CLOSe (@%d00%d)'%(row,col))
        elif col >= 10 and col < 100:
            mux.write('ROUTe:CLOSe (@%d0%d)'%(row,col))
        elif col >= 100:
            mux.write('ROUTe:CLOSe (@%d%d)'%(row,col))
    
    # Opens corresponding channel (rol and col maps to electrode)
    def breakContact(self, row, col):
        mux = self.mux

        if col < 10:
            mux.write('ROUTe:OPEN (@%d00%d)'%(row,col))
        elif col >= 10 and col < 100:
            mux.write('ROUTe:OPEN (@%d0%d)'%(row,col)) 
        elif col >= 100:
            mux.write('ROUTe:OPEN (@%d%d)'%(row,col))\

    # Break contact with all channels
    def breakContactAll(self):
        mux = self.mux
        mux.write("ROUTe:OPEN:ALL")
        time.sleep(.1)

    # Make proper shut down function (check documentation)