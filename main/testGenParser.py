from ParseRadiantOP import RadiantParser
from ParseArchivedRadiantOP import RadiantArchiveParser
import datetime
import json

f = open("masks/Mask 1.json")
data = json.load(f)

now = datetime.datetime.now()
new = "test4"
destination = "C:/Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\mux_testOP"
raw = "C:/Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\sampleRadiantOP"
# parse = RadiantParser("C:/Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\muxSwitcher\main", "Test"+ str(now.second), "C:/Users/Pond Posaphiwat/OneDrive - Frore Systems/Documents/muxSwitcher/main/testDocs")
RadiantParser(destination, newFolder=new, rawResultFolder=raw, data=data, numSweeps=3)