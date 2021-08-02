import matplotlib.pyplot as plt
from newFig import newFigure

x = [0, 1, 2]
y1 = [1, 2, 3]
y2 = [2, 3, 4]
y3 = [3, 4, 5]

plt.plot(x, y1, color='b', label='Sweep 1')
plt.plot(x, y2, color='r', label='Sweep 2')
plt.plot(x, y3, color='g', label='Sweep 3')
  
# Naming the x-axis, y-axis and the whole graph
plt.xlabel("Angle")
plt.ylabel("Magnitude")
plt.title("Sine and Cosine functions")
  
# Adding legend, which helps us recognize the curve according to it's color
plt.legend()
  
# To load the display window
plt.savefig("bruh.png", bbox_inches='tight')

plt.clf()
plt.plot([0, 1], [1, 0])
plt.savefig("sds.png")