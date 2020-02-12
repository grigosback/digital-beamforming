# This script returns an array of signals for each element of a given URA
#%% Libraries
import numpy as np
from matplotlib import pyplot as plt

#%% Functions declaration
def phasedarray_gen(mx, my, d, origin):
    """
    This function generates a position array for each element of a given URA
    with mx * my elements and separation distance 'd'.
    """
    r = np.empty((mx, my), dtype=np.ndarray)
    for i in range(mx):
        for j in range(my):
            r[i, j] = origin + np.array([i * d, j * d, 0])
    return r


def gaussiannoise(snr, ps, m, n):
    """
    This function receives a signal power value 'ps' and a signal-to-noise
    ratio 'snr' and returns a matrix 'w' with size (m,n) corresponding to a 
    white gaussian noise with mean 0 and variance 'ps / (10 ** (snr / 10))'
    """
    mean_w = 0
    var_w = ps / (10 ** (snr / 10))
    std_w = np.sqrt(var_w)
    w = np.random.normal(mean_w, std_w, size=(m, n))
    return w


def transmitter_pos(x_start, v, t):
    # This function generates a position vector "r" with size "N" for a moving
    # transmitter with velocity "v", start coordinate "x_start" and stop
    # coordinate "x_stop"
    r = x_start + v * t
    return r


def doamusic_samples(txs, rx, simulation):
    """
    This function generates a matrix with size (rx.m,simulation.n) with the
    samples for each element of a  receiver 'rx' for each given transmitters
    'tx'.
    """
    d = len(txs)
    n = simulation.n
    c = 3e8
    lambda_c = np.empty(d)

    for i in range(d):
        lambda_c[i] = c / txs[i].s.fc

    K = 2 * np.pi / (lambda_c)
    f = np.empty((d, n))

    for i in range(d):
        f[i, :] = txs[i].s.amp * np.cos(2 * np.pi * txs[i].s.freq * (simulation.t))

    a = np.empty((rx.m, d), dtype="complex")

    for i in range(rx.mx):
        for j in range(rx.my):
            for k in range(d):
                a[rx.mx * j + i, k] = np.e ** (
                    -1j
                    * (
                        i * K[k] * rx.d * np.cos(txs[k].doa.el) * np.cos(txs[k].doa.az)
                        + j
                        * K[k]
                        * rx.d
                        * np.cos(txs[k].doa.el)
                        * np.sin(txs[k].doa.az)
                    )
                )

    ps = 0

    for i in range(d):
        ps = ps + (txs[i].s.amp ** 2) / 2  # Signal power

    w = gaussiannoise(snr, ps, rx.m, simulation.n)

    # x = np.asmatrix(np.empty((rx.m, n), dtype=complex))
    x = np.zeros(rx.m, dtype=complex)
    s = np.zeros((rx.m, rx.m), dtype=complex)

    for i in range(n):
        x = np.asmatrix(a @ f[:, i] + w[:, i])
        x = x.T
        s = s + (1 / n) * (x @ x.H)

    return s


#%%
class Sine_Wave:
    def __init__(self, amp, freq):
        self.amp = amp  # Sine signal amplitude
        self.freq = freq  # Sine signal frequency
        self.fc = fc  # Carrier frequency


class Transmitter:
    def __init__(self, x_start, v, t, s):
        self.s = s
        self.r = transmitter_pos(x_start, v, t)  # Transmitter position in time t
        self.doa = DoA(self.r)  #


class PhasedArray:
    def __init__(self, mx, my, fc, origin):
        c = 3e8
        self.mx = mx  # Numbers of elements in x
        self.my = my  # Numbers of elements in y
        self.m = mx * my
        self.fc = fc
        lambda_c = c / self.fc
        self.d = lambda_c / 2  # Elements separation distance
        self.origin = origin
        self.r = phasedarray_gen(mx, my, self.d, origin)


class Simulation:
    def __init__(self, n, d, fs, sampling_time, snr):
        self.n = n  # Number of sampling times
        self.d = d  # Number of transmitters/signals
        self.fs = fs  # Sampling frequency
        self.t = (
            np.random.randint(0, int(sampling_time * fs), size=n) * 1 / fs
        )  # Random sampling time vector
        self.snr = snr


class DoA:
    def __init__(self, r):
        # Calculation of elevation angle and azimuth using tan^-1
        self.el = np.arctan2(r[2], np.sqrt(r[0] ** 2 + r[1] ** 2))
        # self.az = np.arctan2(r[1] / r[0]) * 180 / np.pi
        self.az = np.arctan2(r[1], r[0])


#%% Units definition
kHz = 1e3
MHz = 1e6
GHz = 1e9
ms = 1e-3
c = 3e8
km = 1e3

# %% Transmitter definition
# x_stop = np.array([7, -5, 10])  # End coordinate for the transmitter in m
# n = 20  # Number of transmitter path points
# d = 1  # Number of signals

x_start = np.array([-10, 0, 10])  # Start coordinate for the transmitter in m
v = np.array([1, 1, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 440
s = Sine_Wave(amp, freq)
tx0 = Transmitter(x_start, v, t, s)

x_start = np.array([15, 0, 200])  # Start coordinate for the transmitter in m
v = np.array([1, 1, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 1300
s = Sine_Wave(amp, freq)
tx1 = Transmitter(x_start, v, t, s)

txs = []
txs.append(tx0)
txs.append(tx1)

# %% Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].s.fc, origin)

# Calculation of elevation angle and azimuth using tan^-1
# doa_real = DoA(txs[0].r)

#%% Simulation parameters
n = 1000  # Snapshots number
d = 2  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
sampling_time = 5 * ms  # Sampling time
snr = 100  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, fs, sampling_time, snr)


# %%
s = doamusic_samples(txs, rx, simulation)

#%%
"""
# %%
d = len(txs)
n = simulation.n
c = 3e8

lambda_c = np.empty(d)

for i in range(d):
    lambda_c[i] = c / txs[i].s.fc

K = 2 * np.pi / (lambda_c)

f = np.empty((d, n))

#%%
for i in range(d):
    f[i, :] = txs[i].s.amp * np.cos(2 * np.pi * txs[i].s.freq * (simulation.t))


#%%
plt.figure()
plt.plot(simulation.t, f[0, :],'o')
plt.show()


#%%
a = np.empty((rx.m, d), dtype="complex")

for i in range(0, rx.mx):
    for j in range(0, rx.my):
        for k in range(0, d):
            a[rx.mx * j + i, k] = np.e ** (
                -1j
                * (
                    i * K[k] * rx.d * np.cos(txs[k].doa.el) * np.cos(txs[k].doa.az)
                  + j * K[k] * rx.d * np.cos(txs[k].doa.el) * np.sin(txs[k].doa.az)
                )
            )

#%%
a[:,0]
#%%
ps = 0

for i in range(0, d):
    ps = ps + (txs[i].s.amp ** 2) / 2  # Signal power

w = gaussiannoise(snr, ps, rx.m, simulation.n)

#%%

# x = np.asmatrix(np.empty((rx.m, n), dtype=complex))
x = np.zeros(rx.m, dtype=complex)
x = np.asmatrix(x)
s = np.zeros((rx.m, rx.m), dtype=complex)

for i in range(n):
    x = a @ f[:, i] + w[:, i]
    s = s + (1/n) * (x @ x.H)

#%%
x = np.zeros(rx.m, dtype=complex)
x = np.asmatrix(x)
s2 = np.zeros((rx.m, rx.m), dtype=complex)

for i in range(n):
    x = np.asmatrix(a @ f[:, i] + w[:, i])
    x = x.T
    s2 = s2 + (1 / n) * (x @ x.H)
    

#%%
x = np.asmatrix(a @ f[:, 0] + w[:, 0])
x = x.T

#%%
s3 = x @ x.H
#%%
"""


# %%


# %%
