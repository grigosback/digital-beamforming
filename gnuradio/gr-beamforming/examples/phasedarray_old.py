# This script returns an array of signals for each element of a given URA
#%% Libraries
import numpy as np

# from modules.random_sampler import *

# Functions declaration
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


def transmitter_pos(x_start, v, t):
    # This function generates a position vector "r" with size "N" for a moving
    # transmitter with velocity "v", start coordinate "x_start" and stop
    # coordinate "x_stop"
    r = x_start + v * t
    return r


def doa_samplesgen(txs, rx, simulation, n=[]):
    """
    This function generates a matrix with size (rx.m,simulation.n) with the
    samples for each element of a  receiver 'rx' for each given transmitters
    'tx'.
    """
    if str(type(txs)) != "<class 'list'>":
        txs_list = []
        txs_list.append(txs)
        txs = txs_list
    d = len(txs)
    if n == []:
        n = txs[0].x.data.size
    c = 3e8
    lambda_c = np.empty(d)

    for i in range(d):
        lambda_c[i] = c / txs[i].fc

    K = 2 * np.pi / (lambda_c)
    f = np.empty((d, n), dtype=complex)

    for i in range(d):
        # f[i, :] = txs[i].s.amp * np.cos(2 * np.pi * txs[i].s.freq * (simulation.t))
        f[i, :] = txs[i].x.data[0:n]

    a = np.empty((rx.m, d), dtype=complex)
    if rx.mx == 1 or rx.my == 1:
        for i in range(rx.m):
            for k in range(d):
                a[i, k] = np.e ** (1j * i * K[k] * rx.d * np.sin(txs[k].doa.theta))
    else:
        beta = np.empty(rx.mx, dtype=complex)
        gamma = np.empty(rx.my, dtype=complex)

        for k in range(d):
            beta_k = np.e ** (
                1j * K[k] * rx.d * np.cos(txs[k].doa.el) * np.cos(txs[k].doa.az)
            )

            gamma_k = np.e ** (
                1j * K[k] * rx.d * np.cos(txs[k].doa.el) * np.sin(txs[k].doa.az)
            )

            for i in range(rx.mx):
                beta[i] = beta_k ** (-i)

            for j in range(rx.my):
                gamma[j] = gamma_k ** (-j)

            a[:, k] = np.kron(beta, gamma).ravel()

    # x = np.asmatrix(np.empty((rx.m, n), dtype=complex))
    x = np.zeros(rx.m, dtype=complex)
    x_matrix = np.zeros((rx.m, n), dtype=complex)
    s = np.zeros((rx.m, rx.m), dtype=complex)

    for i in range(n):
        x = np.asmatrix(a @ f[:, i])
        x = x.T
        x_matrix[:, i] = np.ravel(x)

    return x_matrix, a


class Signal:
    def __init__(self, fs, data):
        self.fs = fs  # Sampling frequency
        n = data.size
        t = np.arange(n) / fs  # Sampling time vector
        self.t = t
        # data = data - np.average(data)
        # data = data / max(data)
        self.data = data


class Transmitter:
    def __init__(self, doa, fc, x):
        self.x = x
        # self.r = transmitter_pos(x_start, v, t)  # Transmitter position in time t
        self.doa = doa  #
        self.fc = fc  # Carrier frequency


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
    def __init__(self, n, d, snr):
        self.n = n  # Number of sampling times
        self.d = d  # Number of transmitters/signals
        self.snr = snr


class DoA:
    def __init__(self, el, az):
        # Calculation of elevation angle and azimuth using tan^-1
        self.el = np.radians(el)
        # self.az = np.arctan2(r[1] / r[0]) * 180 / np.pi
        self.az = np.radians(az)


#
x = Signal(32e3, np.array(range(10), dtype=complex))
doa = DoA(30, 60)
fc = 436e6
tx0 = Transmitter(doa, fc, x)
txs = []
txs.append(tx0)

# Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)

# Simulation parameters
n = 10  # Snapshots number
d = 1  # Number of signals/transmitters
snr = 999  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, snr)


# %%
x, a = doa_samplesgen(txs, rx, simulation)

#%%
x[:, 7]

# %%
