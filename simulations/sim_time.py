#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
from inits.initialization import *
from algorithms.music import doamusic_estimation
from algorithms.esprit import doaesprit_estimation
from matplotlib import pyplot as plt
import matplotlib
import time


# matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

#%%
# Transmitter definition
x_start = np.array([15, 15, 36.74234614])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 40000
s = Sine_Wave(amp, freq)
tx0 = Transmitter(x_start, v, t, fc, s)

txs = []
txs.append(tx0)

# Simulation parameters
n = 124  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
fc = rx.fc
sampling_time = 5 * ms  # Sampling time
snr = 7  # SNR in dB
simulation = Simulation(n, d, fs, fc, sampling_time, snr)

#%%
N = 20
time_music_array = np.zeros(N)
time_esprit_array = np.zeros(N)
el_music_est = np.zeros(N)
az_music_est = np.zeros(N)
el_esprit_est = np.zeros(N)
az_esprit_est = np.zeros(N)
m_array = np.zeros(N)

#%%
for L in range(N):
    print(L)
    # Phased array definition
    mx = L + 2  # Number of sensors in direction X
    my = L + 2  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].fc, origin)

    [s, x] = doamusic_samples(txs, rx, simulation)

    el_music = np.linspace(0, np.pi / 2, num=200)
    az_music = np.linspace(-np.pi, np.pi, num=200)
    a = np.empty((rx.m, el_music.size, az_music.size), dtype=complex)

    for ax in range(el_music.size):
        for ay in range(az_music.size):
            for i in range(rx.mx):
                for j in range(0, rx.my):
                    a[rx.mx * i + j, ax, ay] = np.e ** (
                        -1j
                        * (
                            i * np.pi * np.cos(el_music[ax]) * np.cos(az_music[ay])
                            + j * np.pi * np.cos(el_music[ax]) * np.sin(az_music[ay])
                        )
                    )

    start = time.time()
    p_mu = doamusic_estimation(s, a)
    idx = np.unravel_index(np.argmax(p_mu, axis=None), p_mu.shape)
    el_music_est[L] = np.degrees(el_music[idx[0]])
    az_music_est[L] = np.degrees(az_music[idx[1]])
    stop = time.time()
    time_music_array[L] = stop - start

    start = time.time()
    [az_esprit_est[L], el_esprit_est[L]] = np.degrees(doaesprit_estimation(x, rx))
    stop = time.time()
    time_esprit_array[L] = stop - start
    m_array[L] = rx.m

#%%
plt.figure(figsize=(16, 9), dpi=100)
plt.grid()
plt.plot(m_array, time_music_array)
plt.plot(m_array, time_esprit_array)
plt.legend(["MUSIC", "ESPRIT"])
plt.xlabel("M")
plt.ylabel(r"Tiempo [s]")
plt.savefig("images/sim_time.png", dpi=200, bbox_inches="tight")
plt.show()

# %% Only ESPRIT
for L in range(N):
    print(L)
    # Phased array definition
    mx = L + 2  # Number of sensors in direction X
    my = L + 2  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].fc, origin)

    [s, x] = doamusic_samples(txs, rx, simulation)

    start = time.time()
    [az_esprit_est[L], el_esprit_est[L]] = np.degrees(doaesprit_estimation(x, rx))
    stop = time.time()
    time_esprit_array[L] = stop - start
    m_array[L] = rx.m

#%%
plt.figure(figsize=(16, 9), dpi=100)
plt.grid()
# plt.plot(m_array, time_music_array)
plt.plot(m_array, time_esprit_array)
plt.title("ESPRIT")
plt.xlabel("M")
plt.ylabel(r"Tiempo [s]")
plt.savefig("images/sim_esprit_time.png", dpi=200, bbox_inches="tight")
plt.show()

#%%
az_esprit_est

# %%
el_esprit_est

# %%
