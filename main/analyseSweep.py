from DataSetFormat import DataSetFormatter

import numpy as np
import matplotlib.pyplot as plt

# add bipolar analysis here!
# .getResults returns [self.yInt, self.polMaxE, self.loopArea, self.derUp, self.derDown]
class sweepAnalyser:
    def __init__(self, sweepDataSet, sweepType):
        self.field, self.polarization = sweepDataSet.returnFields(), sweepDataSet.returnPolarizations()
        if sweepType == "Monopolar":
            self.analysePerSweepMonopolar()
        elif sweepType == "Bipolar":
            print("SHAPE:")
            print(np.shape(self.polarization))
            # self.applyBipolarOffset()
            self.analysePerSweepBipolar()
            pass

##########################################################
    def analysePerSweepBipolar(self):
        minPoint = np.argmin(self.field)
        maxPoint = np.argmax(self.field)
        print("minPoint = "+ str(minPoint))
        print("maxPoint = "+ str(maxPoint))
        print("Total data pts = " + str(len(self.field)))

        curve1E, curve1P = self.field[:minPoint], self.polarization[:minPoint]
        curve2E, curve2P = self.field[minPoint:maxPoint], self.polarization[minPoint:maxPoint]
        curve3E, curve3P = self.field[maxPoint:], self.polarization[maxPoint:]

        # BEST SO FAR: 15th deg polynomial
        fitDeg = 15
        curve1 = np.polyfit(curve1E, curve1P, fitDeg)
        curve2 = np.polyfit(curve2E, curve2P, fitDeg)
        curve3 = np.polyfit(curve3E, curve3P, fitDeg)

        print("===================")
        print(curve1)
        print(curve2)
        print(curve3)
        print("===================")

        self.edges = [[0, minPoint], [minPoint, maxPoint], [maxPoint, -1]]
        
        step = 1
        minE = self.field[minPoint]
        maxE = self.field[maxPoint]
        print("minE")
        print(minE)
        print("maxE")
        print(maxE)

        x1 = np.flip(np.arange(minE, self.field[0], step))
        x2 = np.arange(minE, maxE, step)
        x3 = np.flip(np.arange(self.field[-1], maxE, step))

        print("===================")
        print(x1)
        print(x2)
        print(x3)
        print("===================")
        
        plt.clf()
        curve1 = np.poly1d(curve1)
        curve2 = np.poly1d(curve2)
        curve3 = np.poly1d(curve3)
        
        plt.plot(x1, curve1(x1), 'bo')
        plt.plot(x2, curve2(x2), 'ro')
        plt.plot(x3, curve3(x3), 'go')

        intw = np.random.randint(10, size=1)
        plt.savefig(r"C:\Users\Pond Posaphiwat\OneDrive - Frore Systems\Documents/cap" +str(intw[0])+ ".png", bbox_inches='tight', dpi=1200)
        #######################################

        pr_max = max(abs(self.polarization))
        
        pr_p = np.polyval(curve3, 0)
        pr_n = np.polyval(curve2, 0)
        ec_p = np.roots(curve2)
        ec_n = np.roots(curve1)

        # a[ (3>a[:,1]) & (a[:,1]>-6) ]
        
        ec_p = ec_p[np.isreal(ec_p)]
        ec_n = ec_n[np.isreal(ec_n)]
        real_ec_p = []
        real_ec_n = []
        for ec, realpart in zip([ec_p, ec_n], [real_ec_p, real_ec_n]):
            for val in ec:
                realpart.append(np.real(val))
        real_ec_p = np.array(real_ec_p)
        real_ec_n = np.array(real_ec_n)

        real_ec_p = real_ec_p[(0 < real_ec_p) & (maxE > real_ec_p)]
        real_ec_n = real_ec_n[(minE < real_ec_n) & (0 > real_ec_n)]

        print("Ec+ = ")
        print(real_ec_p)
        print("Ec- = ")
        print(real_ec_n)


        #########################################
        ###PLACE HOLDER FOR Ec+ AND Ec-##########
        tick1 = 0
        tick2 = 0
        if not real_ec_p.size:
            ec_p = 0
        else:
            ec_p = real_ec_p[0]
            tick1 = 1

        if not real_ec_p.size:
            ec_n = 0
        else:
            ec_n = real_ec_n[0]
            tick2 = 1
        #########################################
        
        if tick1 & tick2:
            imprint = (ec_p - ec_n)/2.0
        else: 
            imprint = 0

        loopArea_12 = self.getLoopArea(curve1, curve2, minE, 0)
        loopArea_23 = self.getLoopArea(curve1, curve2, 0, maxE)
        loopArea = loopArea_12 + loopArea_23

        self.bipolarData = [pr_max, pr_p, pr_n, ec_p, ec_n, imprint, loopArea]

        print(self.bipolarData)
        print("Data analysed.")

    def applyBipolarOffset(self):
        pOffset = (max(self.polarization) - min(self.polarization))/2.0
        self.polarization = np.array(self.polarization)
        self.polarization = self.polarization - pOffset
        print("Offset applied.")

    def analysePerSweepMonopolar(self):
        minPoint = np.argmin(self.field)
        curveDownE, curveUpE = self.field[:minPoint], self.field[minPoint:]
        curveDownPol, curveUpPol = self.polarization[:minPoint], self.polarization[minPoint:]

        down = np.polyfit(curveDownE, curveDownPol, 5)
        up = np.polyfit(curveUpE, curveUpPol, 5)

        # Y-intercept of return curve
        self.yInt = np.polyval(up, 0)
        
        # Polarization at max |E| (minE)
        self.polMaxE = self.polarization[minPoint]

        # Find embedded area of hysteresis
        self.loopArea = self.getLoopArea(down, up, self.field[minPoint], 0)

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

    def getResultsBipolar(self):
        return self.bipolarData

    def getField(self):
        return self.field

    def getPol(self):
        return self.polarization

    def getBipolarCurves(self):
        return self.curves, self.edges