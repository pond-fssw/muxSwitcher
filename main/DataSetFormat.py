import numpy as np

class DataSetFormatter:
    def __init__(self, numPoints):
        self.Point = np.zeros(numPoints)
        self.Time = np.zeros(numPoints)
        self.Field = np.zeros(numPoints)
        self.Polarization = np.zeros(numPoints)

        self.nextPointIndex = 0

    def addDataPoint(self, point, time, field, polarization):
        i = self.nextPointIndex

        self.Point[i] = point
        self.Time[i] = time
        self.Field[i] = field
        self.Polarization[i] = polarization

        self.nextPointIndex += 1
    
    def returnPoints(self):
        return self.Point

    def returnTimes(self):
        return self.Time

    def returnFields(self):
        return self.Field

    def returnPolarizations(self):
        return self.Polarization

    def addOffset(self, offset):
        self.Polarization += offset

    def length(self):
        return self.Time.size