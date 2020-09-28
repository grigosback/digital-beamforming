#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from matplotlib import pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import time

import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")


#%% 1D
"""n_theta = 200
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
plt.figure(figsize=(16, 9), dpi=200)
plt.plot(theta * 180 / np.pi, p_mu)
plt.plot([-45, -45], [0, p_mu.max() * 1.1], "r", linestyle="--")
plt.plot([0, 0], [0, p_mu.max() * 1.1], "r", linestyle="--")
plt.plot([45, 45], [0, p_mu.max() * 1.1], "r", linestyle="--")
plt.yscale("log")
plt.xticks([-75, -45, -25, 0, 25, 45, 75])
plt.xlabel(r"$\theta$ [°]", size=20)
plt.ylim(p_mu.min() * 0.9, p_mu.max() * 1.1)
plt.ylabel("$|P_{MU}|$", size=20)
plt.grid()
# plt.savefig("sim_music_spectrum1d.png", dpi=200, bbox_inches="tight")
plt.show()"""

#%% 2D
# %% Transmitter definition
x_start = np.array([0, -15, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 400
s = Sine_Wave(amp, freq)
tx0 = Transmitter(x_start, v, t, fc, s)

x_start = np.array([15, 15, 30])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq)
tx1 = Transmitter(x_start, v, t, fc, s)

x_start = np.array([0, 15, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 3300
s = Sine_Wave(amp, freq)
tx2 = Transmitter(x_start, v, t, fc, s)

txs = []
txs.append(tx0)
txs.append(tx1)
txs.append(tx2)

# %% Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)
# %%
if rx.mx == 1 or rx.my == 1:
    theta = np.linspace(-np.pi / 2, np.pi / 2, num=100)
    lambda_c = c / rx.fc
    k = 2 * np.pi / (lambda_c)
    a = np.empty((rx.m, theta.size), dtype=complex)
    for ax in range(theta.size):
        for i in range(rx.m):
            a[i, ax] = np.e ** (-1j * i * k * rx.d * np.cos(theta[ax]))

else:
    el = np.linspace(0, np.pi / 2, num=100)
    az = np.linspace(-np.pi, np.pi, num=200)
    lambda_c = c / rx.fc
    k = 2 * np.pi / (lambda_c)
    a = np.empty((rx.m, el.size, az.size), dtype=complex)

    for ax in range(el.size):
        for ay in range(az.size):
            for i in range(rx.mx):
                for j in range(0, rx.my):
                    a[rx.mx * i + j, ax, ay] = np.e ** (
                        -1j
                        * (
                            i * k * rx.d * np.cos(el[ax]) * np.cos(az[ay])
                            + j * k * rx.d * np.cos(el[ax]) * np.sin(az[ay])
                        )
                    )


# %%
s = doamusic_samples(txs, rx, simulation)
#%%
p_mu = doamusic_estimation(s, a)

# %%
y = el * 180 / np.pi
x = az * 180 / np.pi
plt.figure(figsize=(16, 9), dpi=200)
plt.imshow(
    np.log10(abs(p_mu)),
    extent=(x.min(), x.max(), y.max(), y.min()),
    cmap="jet",
    aspect="auto",
)
plt.ylabel(r"Elevation [°]", size=20)
plt.xlabel(r"Azimuth [°]", size=20)
# plt.savefig("sim_music_spectrum2d.png", dpi=200, bbox_inches="tight")
plt.show()

print("El0 = " + str(tx0.doa.el * 180 / np.pi))
print("Az0 = " + str(tx0.doa.az * 180 / np.pi))
print("El1 = " + str(tx1.doa.el * 180 / np.pi))
print("Az1 = " + str(tx1.doa.az * 180 / np.pi))
print("El2 = " + str(tx2.doa.el * 180 / np.pi))
print("Az2 = " + str(tx2.doa.az * 180 / np.pi))

#%% Time measurement
time_array = np.zeros(20)
m_array = np.zeros(20)
for i in range(1, 21):
    print(i ** 2)
    mx = i  # Number of sensors in direction X
    my = i  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].fc, origin)

    if rx.mx == 1 or rx.my == 1:
        theta = np.linspace(-np.pi / 2, np.pi / 2, num=100)
        lambda_c = c / rx.fc
        k = 2 * np.pi / (lambda_c)
        a = np.empty((rx.m, theta.size), dtype=complex)
        for ax in range(theta.size):
            for i in range(rx.m):
                a[i, ax] = np.e ** (-1j * i * k * rx.d * np.cos(theta[ax]))

    else:
        el = np.linspace(0, np.pi / 2, num=100)
        az = np.linspace(-np.pi, np.pi, num=200)
        lambda_c = c / rx.fc
        k = 2 * np.pi / (lambda_c)
        a = np.empty((rx.m, el.size, az.size), dtype=complex)

        for ax in range(el.size):
            for ay in range(az.size):
                for i in range(rx.mx):
                    for j in range(0, rx.my):
                        a[rx.mx * i + j, ax, ay] = np.e ** (
                            -1j
                            * (
                                i * k * rx.d * np.cos(el[ax]) * np.cos(az[ay])
                                + j * k * rx.d * np.cos(el[ax]) * np.sin(az[ay])
                            )
                        )

    s = doamusic_samples(txs, rx, simulation)
    start = time.time()
    p_mu = doamusic_estimation(s, a)
    stop = time.time()

    time_array[i] = stop - start
    m_array[i] = rx.m


# %%
plt.figure()
plt.plot(m_array, time_array)
plt.yscale("log")
plt.show()

# %%
