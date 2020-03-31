# This script returns an array of signals for each element of a given URA
#%% Libraries
import numpy as np

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
    std_w = np.sqrt(var_w / 2)
    w_re = np.random.normal(mean_w, std_w, size=(m, n))
    w_im = np.random.normal(mean_w, std_w, size=(m, n))
    w = w_re + 1j * w_im
    return w


def transmitter_pos(x_start, v, t):
    # This function generates a position vector "r" with size "N" for a moving
    # transmitter with velocity "v", start coordinate "x_start" and stop
    # coordinate "x_stop"
    r = x_start + v * t
    return r


def doamusic_samples(txs, rx, simulation, rs=True):
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
    n = simulation.n
    c = 3e8
    lambda_c = np.empty(d)

    for i in range(d):
        lambda_c[i] = c / txs[i].fc

    K = 2 * np.pi / (lambda_c)
    f = np.empty((d, n))

    if rs:
        for i in range(d):
            # f[i, :] = txs[i].s.amp * np.cos(2 * np.pi * txs[i].s.freq * (simulation.t))
            f[i, :] = txs[i].x.data[np.random.randint(0, txs[i].x.data.size, size=n)]
    else:
        for i in range(d):
            f[i, :] = txs[i].x.data[: txs[i].x.data.size / n :]

    a = np.empty((rx.m, d), dtype="complex")
    if rx.mx == 1 or rx.my == 1:
        for i in range(rx.m):
            for k in range(d):
                a[i, k] = np.e ** (1j * i * K[k] * rx.d * np.sin(txs[k].doa.theta))
    else:
        beta = np.empty((rx.mx, 1), dtype=complex)
        gamma = np.empty((rx.my, 1), dtype=complex)

        for k in range(d):
            [beta_k, gamma_k] = [
                np.e
                ** (1j * K[k] * rx.d * np.cos(txs[k].doa.el) * np.cos(txs[k].doa.az)),
                np.e
                ** (1j * K[k] * rx.d * np.cos(txs[k].doa.el) * np.sin(txs[k].doa.az)),
            ]
            for i in range(rx.mx):
                beta[i] = beta_k ** (-i)

            for j in range(rx.my):
                gamma[j] = gamma_k ** (-j)

            a[:, k] = np.kron(beta, gamma).ravel()

        """a[rx.my * j + i, k] = np.e ** (
            -1j
            * (
                i
                * K[k]
                * rx.d
                * np.cos(txs[k].doa.el)
                * np.cos(txs[k].doa.az)
                + j
                * K[k]
                * rx.d
                * np.cos(txs[k].doa.el)
                * np.sin(txs[k].doa.az)
            )
        )"""

    ps = 0

    for i in range(d):
        # ps = ps + (txs[i].s.amp ** 2) / 2  # Signal power
        ps = ps + (txs[i].x.data.max() ** 2) / 2  # Signal power

    w = gaussiannoise(simulation.snr, ps, rx.m, simulation.n)

    # x = np.asmatrix(np.empty((rx.m, n), dtype=complex))
    x = np.zeros(rx.m, dtype=complex)
    x_matrix = np.zeros((rx.m, n), dtype=complex)
    s = np.zeros((rx.m, rx.m), dtype=complex)

    for i in range(n):
        x = np.asmatrix(a @ f[:, i] + w[:, i])
        x = x.T
        s = s + (1 / n) * (x @ x.H)
        x_matrix[:, i] = np.ravel(x)

    return [s, x_matrix]


#%%
class Sine_Wave:
    def __init__(self, amp, freq, fs, t_max):
        self.amp = amp  # Sine signal amplitude
        self.freq = freq  # Sine signal frequency
        self.fs = fs  # Sampling frequency
        n = int(t_max * fs)
        t = np.arange(n) / fs  # Sampling time vector
        self.t = t
        data = amp * np.cos(2 * np.pi * freq * (t))
        data = data / max(data)
        self.data = data


class Signal:
    def __init__(self, fs, data):
        self.fs = fs  # Sampling frequency
        n = data.size
        t = np.arange(n) / fs  # Sampling time vector
        self.t = t
        data = data - np.average(data)
        data = data / max(data)
        self.data = data


class Transmitter:
    def __init__(self, x_start, v, t, fc, x):
        self.x = x
        self.r = transmitter_pos(x_start, v, t)  # Transmitter position in time t
        self.doa = DoA(self.r)  #
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
    def __init__(self, r):
        # Calculation of elevation angle and azimuth using tan^-1
        self.el = np.arctan2(r[2], np.sqrt(r[0] ** 2 + r[1] ** 2))
        # self.az = np.arctan2(r[1] / r[0]) * 180 / np.pi
        self.az = np.arctan2(r[1], r[0])
        self.theta = np.arcsin(r[0] / (np.sqrt(r[0] ** 2 + r[1] ** 2 + r[2] ** 2)))
