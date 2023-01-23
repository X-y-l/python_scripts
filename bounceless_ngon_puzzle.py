import numpy as np
import matplotlib.pyplot as plt
import math

x_vals = np.arange(5,100,1)
y_vals = np.zeros(len(x_vals))

def bounce_time(x):
  total = 0
  for i in range(0,int(x)):
    total += math.pow(math.cos(2*math.pi/x), -i)
  return total

for i, x in enumerate(x_vals):
  y_vals[i] = bounce_time(x)

min_y = np.min(y_vals)
min_x = x_vals[np.where(y_vals == min_y)[0]]
print(min_x)

plt.scatter(x_vals, y_vals)
plt.scatter(min_x, min_y)
plt.show()
