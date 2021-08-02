# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 20:44:17 2021

@author: Nicolas Madhavapeddy
"""

import matplotlib.pyplot as plt
from scipy.stats import linregress


file = open('testg1.txt', 'r')
point = []
time = []
field = []
polarization = []

flag = False
index = False
number_of_rows = ''
count = 0
for line in file:
    count = count + 1
    if line.strip() == '»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»» Data «««««««««««««««««««««««««««««««««««««««':
        index = True
        continue
    if index == True:
        temp = line.strip()
        for i in temp:
            if i.isdigit() == True:
                number_of_rows = number_of_rows + i
        number_of_rows = int(number_of_rows)
        count = -4
        index = False
        continue
    if line.strip() == 'Point	Time (ms)	Field (kV/cm)	Measured Polarization':
        point.append([])
        time.append([])
        field.append([])
        polarization.append([])
        flag = True
        continue
    
    if flag == False:
        continue

    if count > number_of_rows:
        flag = False
        number_of_rows = ''
        continue
    
    p, t, f, pol = line.split(maxsplit=4)
    point[-1].append(float(p))
    time[-1].append(float(t))
    field[-1].append(float(f))
    polarization[-1].append(float(pol))
    

for loop in range(len(field)):
    slope, intercept, temp1, temp2, temp3 = linregress(field[loop][-100::], polarization[loop][-100::])
    step = abs(field[loop][-1] - field[loop][-2]) * 0.05
    while True:
        flag = 999
        if field[loop][-1] >= 0:
            field[loop].pop(-1)
            continue
        if field[loop][-1] < 0:
            x = field[loop][-1] + step
            if abs(x) < step:
                field.append(0)
                polarization.append(polarization[loop][-1])
                break
            y = slope * x + intercept
            field[loop].append(x)
            polarization[loop].append(y)

plt.plot(field[0], polarization[0])
plt.show()
plt.plot(field[1], polarization[1])
plt.show()
plt.plot(field[2], polarization[2])
plt.show()