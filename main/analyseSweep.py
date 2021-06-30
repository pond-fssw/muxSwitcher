from DataSetFormat import DataSetFormatter

import numpy as np

# .getResults returns [self.yInt, self.polMaxE, self.loopArea, self.derUp, self.derDown]
class sweepAnalyser:
    def __init__(self, sweepDataSet):
        self.analysePerSweep(sweepDataSet)

    def analysePerSweep(self, data):
        field, polarization = data.returnFields(), data.returnPolarizations()
        self.field = field
        self.polarization = polarization

        minPoint = np.argmin(field)
        curveDownE, curveUpE = field[:minPoint], field[minPoint:]
        curveDownPol, curveUpPol = polarization[:minPoint], polarization[minPoint:]

        down = np.polyfit(curveDownE, curveDownPol, 5)
        up = np.polyfit(curveUpE, curveUpPol, 5)

        # Y-intercept of return curve
        self.yInt = np.polyval(up, 0)
        
        # Polarization at max |E| (minE)
        self.polMaxE = polarization[minPoint]

        # Find embedded area of hysteresis
        self.loopArea = self.getLoopArea(down, up, field[minPoint], 0)

        # Find derivative
        self.derDown, self.derUp = self.getDerivative(down, up)

    def getLoopArea(self, down, up, a, b):
        antiDerDown = np.polyint(np.poly1d(down))
        antiDerUp = np.polyint(np.poly1d(up))

        intDown = np.polyval(antiDerDown, b) - np.polyval(antiDerDown, a)
        intUp = np.polyval(antiDerUp, b) - np.polyval(antiDerUp, a)

        area = abs(intDown - intUp)

        return area

    def getDerivative(self, down, up):
        derDown = np.polyder(down)
        derUp = np.polyder(up)
        return derDown, derUp

    def getResults(self):
        return [self.yInt, self.polMaxE, self.loopArea, self.derUp, self.derDown]

    def getField(self):
        return self.field

    def getPol(self):
        return self.polarization