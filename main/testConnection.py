from MuxChannelControl import MuxChannelController
import time

mux = MuxChannelController("USB0::0x0957::0x0507::MY44004129::INSTR")
mux.makeContact(1, 913)
mux.makeContact(1, 923)

# Problem: bridge not closing properly... channel 913 and 923
# FIXED

time.sleep(10)
mux.breakContact(1,913)
mux.breakContact(1,923)