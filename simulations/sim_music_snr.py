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
fc = rx.fc
sampling_time = 5 * ms  # Sampling time
snr = 7  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, fs, fc, sampling_time, snr)

n_theta = 200

theta = np.linspace(-np.pi / 2, np.pi / 2, num=n_theta)
lambda_c = c / rx.fc
k = 2 * np.pi / (lambda_c)


#%%
a = np.empty((rx.m, theta.size), dtype=complex)

for ax in range(theta.size):
    for i in range(rx.m):
        a[i, ax] = np.e ** (1j * i * k * rx.d * np.sin(theta[ax]))


s = doamusic_samples(txs, rx, simulation)
p_mu = doamusic_estimation(s, a)


#%%
x_start = np.array([-15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq, fc)
tx0 = Transmitter(x_start, v, t, s)

x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq, fc)
tx1 = Transmitter(x_start, v, t, s)

x_start = np.array([0, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq, fc)
tx2 = Transmitter(x_start, v, t, s)

txs1 = []
txs1.append(tx0)
txs1.append(tx1)
txs1.append(tx2)

x_start = np.array([-15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 400
s = Sine_Wave(amp, freq, fc)
tx0 = Transmitter(x_start, v, t, s)

x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq, fc)
tx1 = Transmitter(x_start, v, t, s)

x_start = np.array([0, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 3300
s = Sine_Wave(amp, freq, fc)
tx2 = Transmitter(x_start, v, t, s)

txs2 = []
txs2.append(tx0)
txs2.append(tx1)
txs2.append(tx2)


# %%
def image_array(snr):
    print(snr)
    simulation = Simulation(n, d, fs, fc, sampling_time, snr)

    s1 = doamusic_samples(txs1, rx, simulation)
    p_mu1 = doamusic_estimation(s1, a)
    s2 = doamusic_samples(txs2, rx, simulation)
    p_mu2 = doamusic_estimation(s2, a)

    fig, axs = plt.subplots(1, 2, figsize=(20, 9), frameon=False, dpi=200)
    for ax in axs:
        ax.set_yscale("log")
        ax.set_ylabel(r"$|P_{MU}|$", size=15)
        ax.set_xlabel(r"$\theta$ [°]")
        ax.set_xticks([-75, -45, -25, 0, 25, 45, 75])
        ax.set_yticks([])
        ax.minorticks_off()

        at = AnchoredText(
            "SNR = %i dB" % (snr), prop=dict(size=15), frameon=True, loc="upper right"
        )
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        ax.add_artist(at)

    axs[0].plot((0, 0), (0, p_mu1.max() * 1.05), linestyle="--", color="r", linewidth=2)
    axs[0].plot(
        (45, 45), (0, p_mu1.max() * 1.05), linestyle="--", color="r", linewidth=2
    )
    axs[0].plot(
        (-45, -45), (0, p_mu1.max() * 1.05), linestyle="--", color="r", linewidth=2
    )
    axs[0].set_ylim((p_mu1.min(), p_mu1.max() * 1.05))
    axs[0].plot(theta * 180 / np.pi, p_mu1)
    axs[0].set_title("Señales coherentes", size=20)

    axs[1].plot((0, 0), (0, p_mu2.max() * 1.05), linestyle="--", color="r", linewidth=2)
    axs[1].plot(
        (45, 45), (0, p_mu2.max() * 1.05), linestyle="--", color="r", linewidth=2
    )
    axs[1].plot(
        (-45, -45), (0, p_mu2.max() * 1.05), linestyle="--", color="r", linewidth=2
    )
    axs[1].set_ylim((p_mu2.min(), p_mu2.max() * 1.05))
    axs[1].plot(theta * 180 / np.pi, p_mu2)
    axs[1].set_title("Señales no coherentes", size=20)

    fig.canvas.draw()  # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


#%%
snr = np.linspace(10, -10, 21)
#%%

kwargs_write = {"fps": 10.0, "quantizer": "nq"}
imageio.mimsave("./sim_music_snr.gif", [image_array(snr_i) for snr_i in snr], fps=1)


#%%
x_start = np.array([-15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 400
s = Sine_Wave(amp, freq, fc)
tx = Transmitter(x_start, v, t, s)


#%%
snr = np.linspace(10, -20, 100)
n_error = 10
error_array = np.zeros(len(snr))
for i in range(len(snr)):
    error = 0
    for j in range(n_error):
        simulation = Simulation(n, d, fs, fc, sampling_time, snr[i])
        s = doamusic_samples(tx, rx, simulation)
        p_mu = doamusic_estimation(s, a)
        idx = np.argmax(p_mu)
        theta_est = theta[idx]
        error = error + (1 / n_error) * (theta_est - tx.doa.theta) ** 2
    error_array[i] = error


# %%
plt.figure()
plt.plot(snr, error_array)
plt.yscale("log")
plt.show()

# %%
