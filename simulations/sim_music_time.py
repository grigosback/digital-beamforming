#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from matplotlib import pyplot as plt
from IPython import get_ipython
import time

get_ipython().run_line_magic("matplotlib", "qt")

#%%
x_start = np.array([-15, 0, 200])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq, fc)
tx = Transmitter(x_start, v, t, s)

# %% Test
s = doamusic_samples(txs, rx, simulation)
#%%
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
                    a[rx.mx * j + i, ax, ay] = np.e ** (
                        -1j
                        * (
                            i * k * rx.d * np.cos(el[ax]) * np.cos(az[ay])
                            + j * k * rx.d * np.cos(el[ax]) * np.sin(az[ay])
                        )
                    )

#%% MUSIC test
p_mu = doamusic_estimation(s, a)

#%%
rx.my
#%%
rx.mx == 1 or rx.my == 1
#%%

plt.figure()
plt.plot(theta, np.log10(abs(p_mu)))
plt.show()

#%%
p_mu.shape

# %%
y = el * 180 / np.pi
x = az * 180 / np.pi
plt.figure()
plt.imshow(
    np.log10(abs(p_mu)),
    extent=(x.min(), x.max(), y.max(), y.min()),
    cmap="jet",
    aspect="auto",
)
plt.ylabel(r"Elevation")
plt.xlabel(r"Azimuth")
plt.show()

print("El0 = " + str(tx0.doa.el * 180 / np.pi))
print("Az0 = " + str(tx0.doa.az * 180 / np.pi))
print("El1 = " + str(tx1.doa.el * 180 / np.pi))
print("Az1 = " + str(tx1.doa.az * 180 / np.pi))


# %%
#%% Time measurement
time_array = np.zeros(20)
m_array = np.zeros(20)
for L in range(20):
    print(L ** 2)
    mx = L + 2  # Number of sensors in direction X
    my = L + 2  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].s.fc, origin)

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
                        a[rx.mx * j + i, ax, ay] = np.e ** (
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

    time_array[L] = stop - start
    m_array[L] = rx.m


# %%
plt.figure(figsize=(16, 9), dpi=100)
plt.plot(m_array, time_array)
plt.yscale("log")
plt.xlabel("# Elementos", size=20)
plt.ylabel("Tiempo [s]", size=20)
plt.grid()
plt.savefig("sim_music_time.png", dpi=200, bbox_inches="tight")
plt.show()

# %%
for i in range(20):
    print(i)

# %%
rx.m

# %%
