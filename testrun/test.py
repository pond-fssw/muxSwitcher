import numpy as np
test = "Points: 2019                                        "
print(int(test[8:]))

offset = float("Offset (µC/cm2):	-4.05e+00                      "[17:])
print(offset)

area = float("Sample Area (cm2):	5.31e-02"[18:])
print(area)

i = np.argmin(np.array([2, 2, 4.1, 1.2]))
print(i)