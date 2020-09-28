#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from matplotlib import pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

from PIL import Image, ImageDraw, ImageFilter
import imageio
import math
import matplotlib
from matplotlib.offsetbox import AnchoredText

# matplotlib.use("Agg")

# get_ipython().run_line_magic("matplotlib", "qt")


#%%
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
fc = rx.fc * 1.1
sampling_time = 5 * ms  # Sampling time
snr = 7  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, fs, fc, sampling_time, snr)

n_theta = 200

theta = np.linspace(-np.pi / 2, np.pi / 2, num=n_theta)
lambda_c = c / simulation.fc
k = 2 * np.pi / (lambda_c)


#%%
a = np.empty((rx.m, theta.size), dtype=complex)

for ax in range(theta.size):
    for i in range(rx.m):
        a[i, ax] = np.e ** (1j * i * k * rx.d * np.sin(theta[ax]))


s = doamusic_samples(tx, rx, simulation)
p_mu = doamusic_estimation(s, a)


#%%
x_start = np.array([-15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq, fc)
tx = Transmitter(x_start, v, t, s)


#%%

n_error = 10
error_array = np.zeros(100)
for K in range(100):
    error = 0
    for j in range(n_error):
        fc = rx.fc * (1 + 0.005 * K)
        simulation = Simulation(n, d, fs, fc, sampling_time, snr)
        lambda_c = c / simulation.fc
        k = 2 * np.pi / (lambda_c)
        for ax in range(theta.size):
            for i in range(rx.m):
                a[i, ax] = np.e ** (1j * i * k * rx.d * np.sin(theta[ax]))
        s = doamusic_samples(tx, rx, simulation)
        p_mu = doamusic_estimation(s, a)
        idx = np.argmax(p_mu)
        theta_est = theta[idx]
        error = error + (1 / n_error) * (theta_est - tx.doa.theta) ** 2
    error_array[K] = error / tx.doa.theta


# %%
plt.figure(figsize=(16, 9), dpi=200)
plt.plot(rx.fc * (1 + np.arange(100) * 0.005) / 10 ** 6, abs(error_array * 100))
plt.yscale("log")
plt.xlabel(r"$\hat{f}_c$ [MHz]", size=20)
plt.ylabel("Error relativo [%]", size=20)
plt.grid()
plt.savefig("sim_music_fc.png", dpi=200, bbox_inches="tight")
plt.show()

# %%
simulation.fc

# %%

error
# %%
tx.doa.theta

# %%
(theta_est - tx.doa.theta) ** 2

# %%
