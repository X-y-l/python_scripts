import matplotlib.pyplot as plt
import numpy as np

# http://www.3d-meier.de/tut19/Seite0.html

def gingerbreadman_map(x, y):
    x_next = 1 - y + abs(x)
    y_next = x
    return x_next, y_next


def burgers_map(x, y, a=1.5, b=0.85):
    x_next = (1-a)*x - y**2
    y_next = (1+b)*y + x*y
    return x_next, y_next


def wu_yang_map(x, y, r=1.18):
    x_next = r*(3*y+1)*x*(1-x)
    y_next = r*(3*x_next+1)*y*(1-y) 
    return x_next, y_next


def get_period(x, y, max_iters, map, tolerance=0.02, max_range = 10):
    x_start, y_start = x, y

    for i in range(max_iters):
        if map == "gingerbreadman":
            x, y = gingerbreadman_map(x, y)
        elif map == "burgers":
            x, y = burgers_map(x, y)
        elif map == "wu yang":
            x, y = wu_yang_map(x, y)

        if abs(x) > max_range or abs(y) > max_range:
            return max_iters

        elif np.abs(x - x_start) < tolerance and np.abs(y - y_start) < tolerance:
            return i + 1
    
    return max_iters


def plot_periods(grid_size, max_iterations, radius, x0, y0):
    x = np.linspace(-radius+x0, radius+x0, grid_size)
    y = np.linspace(-radius+y0, radius+y0, grid_size)
    X, Y = np.meshgrid(x, y)

    periods = np.zeros((grid_size, grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            periods[i, j] = get_period(X[i, j], Y[i, j], max_iterations, "wu yang")

    plt.imshow(periods, extent=(-radius, radius, -radius, radius))
    plt.colorbar()
    plt.show()

plot_periods(200, 2000, 0.75, 0.5, 0.5)