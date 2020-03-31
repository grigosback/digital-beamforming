#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")

from inits.initialization import *
from algorithms.esprit import doaesprit_estimation
from modules.beamformer import *
from matplotlib import pyplot as plt

#%%
# Transmitter definition
x_start = np.array([15, 15, 36.74234614])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 400
s = Sine_Wave(amp, freq)
tx0 = Transmitter(x_start, v, t, fc, s)

txs = []
txs.append(tx0)

# Simulation parameters
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
fc = rx.fc
sampling_time = 5 * ms  # Sampling time
snr = 7  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, fs, fc, sampling_time, snr)

#%%
[s, x] = doamusic_samples(txs, rx, simulation)
doa = doaesprit_estimation(x, rx)
s = beamformer(x, rx, doa, fc)

#%%
plt.figure()
plt.plot(simulation.t, s, "o")
plt.show()
