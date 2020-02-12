#%%
from samples_generator import *


#%% Units definition
kHz = 1e3
MHz = 1e6
GHz = 1e9
ms = 1e-3
c = 3e8
km = 1e3

# %% Transmitter definition
x_start = np.array([-10, 0, 10])  # Start coordinate for the transmitter in m
v = np.array([1, 1, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 440
s = Sine_Wave(amp, freq, fc)
tx0 = Transmitter(x_start, v, t, s)

x_start = np.array([15, 0, 200])  # Start coordinate for the transmitter in m
v = np.array([1, 1, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq, fc)
tx1 = Transmitter(x_start, v, t, s)

txs = []
txs.append(tx0)
txs.append(tx1)

# %% Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].s.fc, origin)

#%% Simulation parameters
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
sampling_time = 5 * ms  # Sampling time
snr = 10  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, fs, sampling_time, snr)

