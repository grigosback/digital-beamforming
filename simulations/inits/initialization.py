#%%
import numpy as np
from inits.samples_generator import *

#%% Units definition
kHz = 1e3
MHz = 1e6
GHz = 1e9
ms = 1e-3
c = 3e8
km = 1e3


# %% Transmitter definition
fs = 64 * MHz  # Sampling frequency
t_max = 5 * ms  # Sampling time


amp = 10
freq = 40000
x = Sine_Wave(amp, freq, fs, t_max, 1, 0)
x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx0 = Transmitter(x_start, v, t, fc, x.data)


amp = 10
freq = 1300
x = Sine_Wave(amp, freq, fs, t_max, 1, 0)
x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx1 = Transmitter(x_start, v, t, fc, x.data)

amp = 10
freq = 3300
x = Sine_Wave(amp, freq, fs, t_max, 1, 0)
x_start = np.array([0, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx2 = Transmitter(x_start, v, t, fc, x.data)

txs = []
txs.append(tx0)
# txs.append(tx1)
# txs.append(tx2)

# %% Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)

#%% Simulation parameters
n = 124  # Snapshots number
d = len(txs)  # Number of signals/transmitters
snr = 7  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, snr)
