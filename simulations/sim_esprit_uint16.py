#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from algorithms.esprit import doaesprit_estimation
from modules.beamformer import *
from modules.ramdom_sampler import *
from matplotlib import pyplot as plt
import matplotlib
import time
from scipy.io import wavfile


matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

#%%
# Transmitter definition
fs0, data0 = wavfile.read("../beacons/aistechsat3.wav")
fs1, data1 = wavfile.read("../beacons/beesat_9.wav")
data0 = data0[0 : min([data0.size, data1.size])]
data1 = data1[0 : min([data0.size, data1.size])]

x_raw = Signal(fs0, data0)
x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx0 = Transmitter(x_start, v, t, fc, x_raw)


x_raw = Signal(fs1, data1)
x_start = np.array([15, 15, 36.74234614])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx1 = Transmitter(x_start, v, t, fc, x_raw)


txs = []
# txs.append(tx0)
txs.append(tx1)


# Phased array definition
M = 4
mx = M  # Number of sensors in direction X
my = M  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)

# Simulation parameters
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
snr = 7  # SNR in dB
simulation = Simulation(n, d, snr)

[s, x] = doamusic_samples(txs, rx, simulation)
x = x + abs(x).min()
x = x / (abs(x).max())
x = (np.real(x) * 65535).astype("uint16") + 1j * (np.imag(x) * 65535).astype("uint16")
x = x.astype("complex64")
x = x - x.mean()

#%%
x_rs = random_sampler(x, simulation.n)
doa = doaesprit_estimation(x_rs, rx)
print(np.degrees(doa))
x_beamformer = beamformer(x, rx, doa, fc)


# %%
plt.figure()
plt.grid()
plt.plot(txs[0].x.t, txs[0].x.data)
plt.plot(txs[0].x.t, x_beamformer)
# plt.plot(np.fft.fftshift(np.fft.fft(txs[1].x.data)))
plt.xlabel("Tiempo [s]")
plt.ylabel("x(t)")
plt.show()
