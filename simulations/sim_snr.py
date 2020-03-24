#%%
import sys
from inits.initialization import *
from algorithms.music import doamusic_estimation
from algorithms.esprit import doaesprit_estimation
from matplotlib import pyplot as plt
import matplotlib

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
# matplotlib.use("Agg")
# get_ipython().run_line_magic("matplotlib", "qt")

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

# Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)

# Simulation parameters
n = 124  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
fc = rx.fc
sampling_time = 5 * ms  # Sampling time


# %%
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

# %%
# snr_array = np.linspace(-5, 15, 21)
snr_array = np.linspace(0, 10, 11)
el_music_est = np.zeros(snr_array.size)
az_music_est = np.zeros(snr_array.size)
el_esprit_est = np.zeros(snr_array.size)
az_esprit_est = np.zeros(snr_array.size)
error_az_music = np.zeros(snr_array.size)
error_el_music = np.zeros(snr_array.size)
error_az_esprit = np.zeros(snr_array.size)
error_el_esprit = np.zeros(snr_array.size)
n_error = 10

for i in range(snr_array.size):
    for j in range(n_error):
        snr = snr_array[i]
        simulation = Simulation(n, d, fs, fc, sampling_time, snr)
        [s, x] = doamusic_samples(txs, rx, simulation)
        p_mu = doamusic_estimation(s, a)
        idx = np.unravel_index(np.argmax(p_mu, axis=None), p_mu.shape)
        el_music_est[i] = np.degrees(el_music[idx[0]])
        az_music_est[i] = np.degrees(az_music[idx[1]])
        [az_esprit_est[i], el_esprit_est[i]] = np.degrees(doaesprit_estimation(x, rx))
        error_az_music[i] = (
            error_az_music[i]
            + (1 / n_error) * (az_music_est[i] - np.degrees(txs[0].doa.az)) ** 2
        )

        error_el_music[i] = (
            error_el_music[i]
            + (1 / n_error) * (el_music_est[i] - np.degrees(txs[0].doa.el)) ** 2
        )

        error_az_esprit[i] = (
            error_az_esprit[i]
            + (1 / n_error) * (az_esprit_est[i] - np.degrees(txs[0].doa.az)) ** 2
        )

        error_el_esprit[i] = (
            error_el_esprit[i]
            + (1 / n_error) * (el_esprit_est[i] - np.degrees(txs[0].doa.el)) ** 2
        )
# %%
plt.figure()
plt.subplot(211)
plt.grid()
plt.plot(snr_array, el_music_est)
plt.plot(snr_array, el_esprit_est)
plt.plot(
    [snr_array[0], snr_array[-1]],
    [np.degrees(txs[0].doa.el), np.degrees(txs[0].doa.el)],
    "r",
    linestyle="--",
)
plt.legend(["MUSIC", "ESPRIT", "Real"])
plt.xlabel("SNR")
plt.ylabel(r"Elevación [°]")
plt.ylim(55, 65)

plt.subplot(212)
plt.grid()
plt.plot(snr_array, az_music_est)
plt.plot(snr_array, az_esprit_est)
plt.plot(
    [snr_array[0], snr_array[-1]],
    [np.degrees(txs[0].doa.az), np.degrees(txs[0].doa.az)],
    "r",
    linestyle="--",
)
plt.legend(["MUSIC", "ESPRIT", "Real"])
plt.xlabel("SNR")
plt.ylabel(r"Azimut [°]")
plt.ylim(40, 50)
plt.show()
# %%
plt.figure()
plt.subplot(211)
plt.grid()
plt.plot(snr_array, error_el_music * 100 / np.degrees(txs[0].doa.el))
plt.plot(snr_array, error_el_esprit * 100 / np.degrees(txs[0].doa.el))
plt.legend(["MUSIC", "ESPRIT"])
plt.xlabel("SNR")
plt.ylim(0, 3)
plt.ylabel(r"Error porcentual elevación [%]")

plt.subplot(212)
plt.grid()
plt.plot(snr_array, error_az_music * 100 / np.degrees(txs[0].doa.az))
plt.plot(snr_array, error_az_esprit * 100 / np.degrees(txs[0].doa.az))
plt.legend(["MUSIC", "ESPRIT"])
plt.xlabel("SNR")
plt.ylabel(r"Error porcentual azimut [%]")
plt.ylim(0, 3)
plt.show()
# %%
error_az_music * 100 / np.degrees(txs[0].doa.az)

# %%
az_music_est[i] - txs[0].doa.az

# %%
error_az_music[i] + (1 / n_error) * (az_music_est[i] - np.degrees(txs[0].doa.az)) ** 2

# %%
