#%%
import numpy as np


def track_gen(x_start, x_stop, v, n):
    # This function generates a position vector "r" with size "N" for a moving
    # transmitter with velocity "v", start coordinate "x_start" and stop
    # coordinate "x_stop"
    d = x_stop - x_start  # Distance vector
    v_vector = (d / np.linalg.norm(d)) * v

    t = np.linalg.norm(d) / v  # Simulation time
    step = t / (n - 1)  # Simulation step

    r = np.empty((n, d.size))
    for i in range(n):
        r[i] = x_start + v_vector * i * step
    return r


#%% Simulation parameters
N = 20
v = 1  # Transmitter's velocity in m/s
x_start = np.array([-10, 0, 10])  # Start coordinate for the transmitter in m
x_stop = np.array([7, 5, 30])  # End coordinate for the transmitter in m

#%% Test
track_gen(x_start, x_stop, v, N)
