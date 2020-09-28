# %%
from scipy.io import wavfile
import time
import matplotlib
from scipy import signal
from matplotlib import pyplot as plt
from modules.random_sampler import *
from modules.beamformer import *
from algorithms.esprit import carrieresprit_estimation
from algorithms.esprit import doaesprit_estimation
from algorithms.music import doamusic_estimation
from inits.initialization import *
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")


matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

# %%
# Transmitter definition
# fs0, data0 = wavfile.read("../beacons/aistechsat3.wav")
fs1, data1 = wavfile.read("../beacons/gomx-1.wav")
# fs2, data2 = wavfile.read("../beacons/beesat_9.wav")
fs0, data0 = wavfile.read("../beacons/beesat_9.wav")

data0 = data0[0 : min([data0.size, data1.size])]
data1 = data1[0 : min([data0.size, data1.size])]
# data1 = data1[60000:]

"""# Oversample
factor = 10
fs0 = fs0 * factor
fs1 = fs1 * factor
data0 = np.repeat(data0, factor)
data1 = np.repeat(data1, factor)

f0 = np.fft.fftshift(np.fft.fftfreq(len(data0), 1 / fs0))
f1 = np.fft.fftshift(np.fft.fftfreq(len(data1), 1 / fs1))

# Modulation
fc = 47535  # Hz
t0 = np.arange(len(data0)) / fs0
data0 = data0 * np.cos(2 * np.pi * fc * t0)
t1 = np.arange(len(data1)) / fs1
data1 = data1 * np.cos(2 * np.pi * fc * t1)
"""
# data0, _ = random_sampler(data0, 1000, 1)
# data1, _ = random_sampler(data1, 1000, 1)

x_raw = Signal(fs0, data0)
x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx0 = Transmitter(x_start, v, t, fc, x_raw)


x_raw = Signal(fs1, data1)
# Start coordinate for the transmitter in m
x_start = np.array([15, 15, 36.74234614])
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
snr = 0  # SNR in dB
simulation = Simulation(n, d, snr)

[s, x] = doa_samplesgen(txs, rx, simulation)
x_rs, _ = random_sampler(x, 1024, 1)
# %%
# x_rs, _ = random_sampler(x, simulation.n)
doa = doaesprit_estimation(x_rs, rx)
print(np.degrees(doa))
x_beamformer = beamformer(x, rx, doa, fc)
# %%

# %% Plot temporal
plt.figure(figsize=(16, 9), dpi=100)
plt.grid()
plt.plot(txs[0].x.t, txs[0].x.data)
plt.plot(txs[0].x.t, x_beamformer)
plt.xlabel("Tiempo [s]")
plt.ylabel("x(t)")
plt.xlim(1, 1.01)
plt.legend(["GOMX-1", "Salida Beamformer"])
plt.savefig("./images/sim_esprit_beacons.png", dpi=100, bbox_inches="tight")
plt.show()


# %% Plot espectral
plt.figure()
plt.grid()
plt.plot(f1, np.fft.fftshift(np.fft.fft(txs[0].x.data)))
plt.plot(f1, np.fft.fftshift(np.fft.fft(x_beamformer)))
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("X(f)")
plt.show()


# %%
M = 3
# N = int((len(x_beamformer) - M + 1)/100)
N = int((len(x_beamformer) - M + 1))
x_windowed = np.zeros((M, N))

for i in range(N):
    x_windowed[:, i] = x_beamformer[i : i + M]

# %%
x_windowed.shape
# %%
carrieresprit_estimation(x_windowed, fs1)


# %%
x_beamformer_rs, _ = random_sampler(x_beamformer, simulation.n)

M = 3
# N = int((len(x_beamformer) - M + 1)/100)
N = simulation.n
x_windowed = np.zeros((M, N))

for i in range(N):
    x_windowed[:, i] = x_beamformer_rs[i : i + M]

# %%
carrieresprit_estimation(x_windowed, fs1)

###############################################################################
# %%
# Transmitter definition
fs0, data0 = wavfile.read("../beacons/gomx-1.wav")

x_raw = Signal(fs0, data0)
# Start coordinate for the transmitter in m
x_start = np.array([15, 15, 36.74234614])
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
tx0 = Transmitter(x_start, v, t, fc, x_raw)

txs = []
txs.append(tx0)


# Phased array definition
M = 4
mx = M  # Number of sensors in direction X
my = M  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)

# Simulation parameters
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
snr = -1  # SNR in dB
simulation = Simulation(n, d, snr)

[s, x] = doa_samplesgen(txs, rx, simulation)

# %%
x_rs, _ = random_sampler(x, simulation.n)
doa = doaesprit_estimation(x_rs, rx, k=[], d=1)
print(np.degrees(doa))
x_beamformer = beamformer(x, rx, doa, fc)

# %% LPF
fc = 10 * kHz
wn = fc / (fs0 / 2)  # frecuencia normalizada del filtro
order = 4
[b, a] = signal.butter(order, wn)
x_beamformer = signal.lfilter(b, a, x_beamformer)


# %%
# scaled = np.int16(x_beamformer / np.max(np.abs(x_beamformer)) * 32767)
scaled = np.real(x_beamformer / np.max(np.abs(x_beamformer)))
wavfile.write("../beacons/gomx-1_beamformer.wav", fs0, scaled)
fs0_bf, data0_bf = wavfile.read("../beacons/gomx-1_beamformer.wav")

# %% Plot temporal
plt.figure()
plt.grid()
plt.plot(txs[0].x.t, txs[0].x.data)
plt.plot(txs[0].x.t, data0_bf)
plt.xlabel("Tiempo [s]")
plt.ylabel("x(t)")
plt.show()

# %% Plot espectral
f0 = np.fft.fftshift(np.fft.fftfreq(len(data0), 1 / fs0))
plt.figure()
plt.grid()
plt.plot(f0, np.fft.fftshift(np.fft.fft(data0_bf)))
plt.plot(f0, np.fft.fftshift(np.fft.fft(x_beamformer)))
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("X(f)")
plt.show()


# %%
np.real(x_beamformer / np.max(np.abs(x_beamformer)))


# %%
