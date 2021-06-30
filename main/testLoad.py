from FormatRadiantOP import RadiantOPFormatter
from DataSetFormat import DataSetFormatter

import matplotlib.pyplot as plt
import numpy as np

testDoc = "testDocs/test_group_3.txt"

formatter = RadiantOPFormatter(testDoc)

list = formatter.returnDataSets()

setNumber = 16

data = list[setNumber]
field, polarization = data.returnFields(), data.returnPolarizations()
x = field
y = polarization

plt.figure()

# Test out quad and cubic
minPoint = np.argmin(field)
curveDownE, curveUpE = field[:minPoint], field[minPoint:]
curveDownPol, curveUpPol = polarization[:minPoint], polarization[minPoint:]

down = np.polyfit(curveDownE, curveDownPol, 5)
up = np.polyfit(curveUpE, curveUpPol, 5)

yInt = np.polyval(up, 0)
plt.scatter(0, yInt, marker='x', s=20, c='r')

plt.scatter(x, y, marker='x', s=3, c='m')
plt.plot(curveDownE, np.polyval(down, curveDownE))
plt.plot(curveUpE, np.polyval(up, curveUpE))
plt.show()

# Loop area calc
a, b = field[minPoint], 0

antiDerDown = np.polyint(np.poly1d(down))
antiDerUp = np.polyint(np.poly1d(up))

intDown = np.polyval(antiDerDown, b) - np.polyval(antiDerDown, a)
intUp = np.polyval(antiDerUp, b) - np.polyval(antiDerUp, a)

area = abs(intDown - intUp)

print("Area = " + str(area))