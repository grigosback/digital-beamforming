#%%
import sys
from inits.initialization import *
from algorithms.music import doamusic_estimation
from algorithms.esprit import doaesprit_estimation
from matplotlib import pyplot as plt
import matplotlib
import time
from scipy.io import wavfile

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
# matplotlib.use("Agg")
# get_ipython().run_line_magic("matplotlib", "qt")

#%%
# Transmitter definition
fs, data = wavfile.read("../beacons/aistechsat3.wav")
x_raw = Signal(fs, data)
x_start = np.array([15, 15, 36.74234614])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx0 = Transmitter(x_start, v, t, fc, x_raw)

fs = 64 * MHz  # Sampling frequency
t_max = 5 * ms  # Sampling time

fs, data = wavfile.read("../beacons/beesat_9.wav")
x_raw = Signal(fs, data)
x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx1 = Transmitter(x_start, v, t, fc, x_raw)


txs = []
txs.append(tx0)
txs.append(tx1)


# Phased array definition
M = 4
mx = M  # Number of sensors in direction X
my = M  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)

# Simulation parameters
n = 124  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
fc = rx.fc
sampling_time = 5 * ms  # Sampling time
snr = 7  # SNR in dB
simulation = Simulation(n, d, snr)

[s, x] = doamusic_samples(txs, rx, simulation)
print(np.degrees(doaesprit_estimation(x, rx)))


# %%
plt.figure()
plt.grid()
# plt.plot(txs[1].x.t, txs[1].x.data)
# plt.plot(np.fft.fftshift(np.fft.fft(txs[1].x.data)))
plt.xlabel("Tiempo [s]")
plt.ylabel("x(t)")
plt.show()


# %%
np.average(txs[0].x.data)

# %%
