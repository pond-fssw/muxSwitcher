from ParseRadiantOP import RadiantParser
from ParseArchivedRadiantOP import RadiantArchiveParser
import datetime

now = datetime.datetime.now()
new = "h10"
# parse = RadiantParser("C:/Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\muxSwitcher\main", "Test"+ str(now.second), "C:/Users/Pond Posaphiwat/OneDrive - Frore Systems/Documents/muxSwitcher/main/testDocs")
RadiantArchiveParser("C:/Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents\mux_testOP", newFolder=new, rawResultFolder="C:/Users\Pond Posaphiwat\Frore Systems\RnD - Characterization\PZT testing/212701/2D/After Poling/Radiant")