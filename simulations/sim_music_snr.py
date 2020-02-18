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
plt.figure()
plt.plot(theta * 180 / np.pi, np.log10(abs(p_mu)))
plt.show()


#%%
step = 0.02
plt.ion()
fig, ax = plt.subplots(1, 1)
plt.ylim((0, track[1, :].max() * (1 + 0.3)))
plt.xlim((track[0, :].min() * 1.1, track[0, :].max() * 1.1))
# plt.yscale("log")
line, = ax.plot(track[0, 0], track[1, 0], "o")
arrow = ax.arrow(0, 0, track[0, 0], track[1, 0], width=1)
fig.canvas.draw()
for i in range(p_mu.shape[1]):
    plt.pause(step)
    line.set_xdata(track[0, i])
    line.set_ydata(track[1, i])
    arrow.set_xy([[0, 0], [track[0, i] * 0.9, track[1, i] * 0.9]])
    arrow.set_linewidth(10)
    fig.canvas.draw()
plt.ioff()

#%%


# %%
def image_array(i):
    n = 1000  # Snapshots number
    d = len(txs)  # Number of signals/transmitters
    fs = 64 * MHz  # Sampling frequency
    fc = rx.fc
    sampling_time = 5 * ms  # Sampling time
    snr = -13  # Signal-to-noise ratio in dB
    simulation = Simulation(n, d, fs, fc, sampling_time, snr)

    s = doamusic_samples(txs, rx, simulation)
    p_mu = doamusic_estimation(s, a)

    fig, ax = plt.subplots(figsize=(16, 9), frameon=False)
    # ax.grid()
    ax.set_ylim((p_mu.min(), p_mu.max()))
    # ax.set_yscale("log")
    ax.set_ylabel(r"$|P_{MU}|$", size=15)
    ax.set_xlabel(r"$\theta$ [°]")
    ax.set_xticks([-75, -45, -25, 0, 25, 45, 75])
    ax.set_yticks([])
    ax.plot(theta * 180 / np.pi, p_mu)

    idx = np.argmax(p_mu)
    ax.plot((0, 0), (0, p_mu.max()), linestyle="--", color="r", linewidth=2)
    ax.plot((45, 45), (0, p_mu.max()), linestyle="--", color="r", linewidth=2)
    ax.plot((-45, -45), (0, p_mu.max()), linestyle="--", color="r", linewidth=2)

    fig.canvas.draw()  # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


#%%
kwargs_write = {"fps": 10.0, "quantizer": "nq"}
imageio.mimsave("./sim_tracking.gif", [image_array(i) for i in range(n_time)], fps=10)


#%%
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
fc = rx.fc
sampling_time = 5 * ms  # Sampling time
snr = 0  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, fs, fc, sampling_time, snr)

s = doamusic_samples(txs, rx, simulation)
p_mu = doamusic_estimation(s, a)


fig, ax = plt.subplots(figsize=(16, 9), frameon=False)
# ax.grid()
ax.set_ylim((p_mu.min(), p_mu.max() * 1.05))
ax.set_yscale("log")
ax.set_ylabel(r"$|P_{MU}|$", size=15)
ax.set_xlabel(r"$\theta$ [°]")
ax.set_xticks([-75, -45, -25, 0, 25, 45, 75])
ax.set_yticks([])
ax.plot(theta * 180 / np.pi, p_mu)

idx = np.argmax(p_mu)
ax.plot((0, 0), (0, p_mu.max() * 1.05), linestyle="--", color="r", linewidth=2)
ax.plot((45, 45), (0, p_mu.max() * 1.05), linestyle="--", color="r", linewidth=2)
ax.plot((-45, -45), (0, p_mu.max() * 1.05), linestyle="--", color="r", linewidth=2)
# ax.annotate(
#    "%.2f°" % (theta[idx] * 180 / np.pi),
#    xy=(theta[idx] * 180 / np.pi + 3, 10 ** 3),
#    size=15,
# )

fig.canvas.draw()  # draw the canvas, cache the renderer
# image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
# image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))


# %%

