#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from algorithms.esprit import doaesprit_estimation
from algorithms.esprit import carrieresprit_estimation
from modules.beamformer import *
from modules.random_sampler import *
from matplotlib import pyplot as plt
import matplotlib
import time
from scipy.io import wavfile


matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")


def oversample(data, fs, factor):
    n = len(fs)
    if n == 1:
        data_os = np.repeat(data, factor)
        fs = fs * factor
    else:
        fs = fs * factor
        data_os = np.empty(n, data.shape[1] * factor)
        for i in range(n):
            data_os[i, :] = np.repeat(data[i, :], factor)

    return [data_os, fs]


#%%
# Transmitter definition
fs0, data0 = wavfile.read("../beacons/aistechsat3.wav")
fs1, data1 = wavfile.read("../beacons/beesat_9.wav")

data0 = data0[0 : min([data0.size, data1.size])]
data1 = data1[0 : min([data0.size, data1.size])]

# Oversample
factor = 10
fs0 = fs0 * factor
fs1 = fs1 * factor
data0 = np.repeat(data0, factor)
data1 = np.repeat(data1, factor)

# Modulation
fc_rem = 47535  # Hz
t0 = np.arange(len(data0)) / fs0
data0 = data0 * np.cos(2 * np.pi * fc_rem * t0)
t1 = np.arange(len(data1)) / fs1
data1 = data1 * np.cos(2 * np.pi * fc_rem * t1)


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
snr_array = np.linspace(-5, 15, 21)
# snr = 7
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
simulation = Simulation(n, d, snr)

#%% Carrier Est vs SNR
error_array = np.zeros(snr_array.size)
fc_est = np.zeros(snr_array.size)
for i in range(snr_array.size):
    n_error = 10
    error = 0
    snr = snr_array[i]
    simulation = Simulation(n, d, snr)
    _, x = doa_samplesgen(txs, rx, simulation)
    x_rs, idx = random_sampler(x, simulation.n)
    doa = doaesprit_estimation(x_rs, rx, [], simulation.d)
    print(np.degrees(doa))
    x_beamformer = beamformer(x, rx, doa, fc)
    for j in range(n_error):
        m = 30
        x_rs, _ = random_sampler(x_beamformer, simulation.n, m)
        fc_est[i] = carrieresprit_estimation(x_rs, fs1)
        error = error + (1 / n_error) * (fc_rem - fc_est[i]) ** 2
        print(fc_est[i])
    # print(error)
    error_array[i] = error / (fc_rem) ** 2
    print(error_array[i])

#%%
plt.figure(figsize=(16, 9), dpi=100)
plt.subplot(211)
plt.grid()
plt.plot(snr_array, fc_est)
plt.plot([snr_array[0], snr_array[-1]], [[fc_rem], [fc_rem]], color="r", linestyle="--")
plt.xlabel("SNR [dB]")
plt.ylabel(r"$f_c$ [Hz]")
plt.legend([r"$\hat{f_c}$", r"$f_c$"])
plt.subplot(212)
plt.grid()
plt.plot(snr_array, error_array * 100)
plt.xlabel("SNR [dB]")
plt.ylabel(r"Error [%]")
plt.savefig("images/sim_esprit_carrierest.png", dpi=200, bbox_inches="tight")
plt.show()

# %%
#%% Carrier Est vs M
m_array = np.array([4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200])
error_array = np.zeros(m_array.size)
fc_est = np.zeros(m_array.size)
snr = -5
simulation = Simulation(n, d, snr)
_, x = doa_samplesgen(txs, rx, simulation)
x_rs, idx = random_sampler(x, simulation.n)
doa = doaesprit_estimation(x_rs, rx, [], simulation.d)
print(np.degrees(doa))
x_beamformer = beamformer(x, rx, doa, fc)

for i in range(m_array.size):
    n_error = 20
    error = 0
    m = m_array[i]
    for j in range(n_error):
        x_rs, _ = random_sampler(x_beamformer, simulation.n, m)
        fc_est[i] = carrieresprit_estimation(x_rs, fs1)
        error = error + (1 / n_error) * (fc_rem - fc_est[i]) ** 2
        print(fc_est[i])
    # print(error)
    error_array[i] = error / (fc_rem) ** 2
    print(error_array[i])

# %%
plt.figure(figsize=(16, 9), dpi=100)
plt.subplot(211)
plt.grid()
plt.plot(m_array, fc_est)
plt.plot([m_array[0], m_array[-1]], [[fc_rem], [fc_rem]], color="r", linestyle="--")
plt.xlabel("M")
plt.ylabel(r"$f_c$ [Hz]")
plt.legend([r"$\hat{f_c}$", r"$f_c$"])
plt.subplot(212)
plt.grid()
plt.plot(m_array, error_array * 100)
plt.xlabel("M")
plt.yscale("Log")
plt.ylabel(r"Error [%]")
plt.savefig("images/sim_esprit_carrierest_vs_m.png", dpi=200, bbox_inches="tight")
plt.show()

# %%
tx0.x.data

# %%
