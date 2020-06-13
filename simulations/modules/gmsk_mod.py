# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import hilbert
import scipy.signal as signal

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

#%%
def gmsk_modulator(x, Rb, nc, h, fs, alpha=0.5, msk=1):
    n = len(x)
    fc = nc * Rb / 4

    x_nrz = 2 * (x - 0.5)

    t_max = n / Rb
    ns = int(t_max * fs)  # number of samples
    nspb = int(fs / Rb)  # samples per bit
    t = np.linspace(0, t_max, ns)

    phi_t = np.zeros(ns)
    for i in range(n):
        if i == n - 1:
            phi_t[i * nspb + 1 : (i + 1) * nspb] = (
                phi_t[i * nspb] + x_nrz[i] * (np.pi * h * Rb) * t[1:nspb]
            )
        else:
            phi_t[i * nspb + 1 : (i + 1) * nspb + 1] = (
                phi_t[i * nspb] + x_nrz[i] * (np.pi * h * Rb) * t[1 : nspb + 1]
            )

    s = np.cos(2 * np.pi * fc * t + phi_t)

    if msk == 1:
        return s, t
    else:
        S = np.fft.fft(s)
        S = S / max(abs(S))
        f = np.fft.fftfreq(len(S), 1 / fs)

        W = alpha * Rb
        H = np.exp((-np.log(2) / 2) * (f / W) ** 2)

        S_filtered = S * H

        s_filtered = np.real(np.fft.ifft(S_filtered))
        s_filtered = s_filtered / max(s_filtered)
        return s_filtered, t


def gmsk_detector(y, fs, Rb, nc):
    fc = nc * Rb / 4
    nspb = int(fs / Rb)
    n = int(len(y) / nspb)
    x_det = np.zeros(n, dtype=int)
    for i in range(n):
        inst_freq = instfreq(y[i * nspb : (i + 1) * nspb], fs)
        if inst_freq[int(nspb / 2)] >= fc:
            x_det[i] = 1
        else:
            x_det[i] = 0
    return x_det


def instfreq(signal, fs):
    analytic_signal = hilbert(signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi) * fs
    return instantaneous_frequency


# %%
x = np.array([1, 1, 0, 1, 0, 0, 0])
# x = np.array([1, 0, 1, 0, 1, 0, 1])
# x = np.random.randint(2, size=100)
# x = np.arange(10)%2
Rb = 4800
fs = 100 * Rb
# nc = 3
nc = 4
h = 1 / 2
fc = nc * Rb / 4
f1 = fc + h * Rb / 2
f2 = fc - h * Rb / 2

s, t = gmsk_modulator(x, Rb, nc, h, fs)
s_filtered, _ = gmsk_modulator(x, Rb, nc, h, fs, 0.5, 0)

plt.figure()
plt.plot(t, s)
plt.plot(t, s_filtered)
plt.xticks(np.arange(len(x)) / Rb)
plt.yticks([-1, 0, 1])
plt.grid()
plt.show()

# %%
# x = np.array([1, 1, 0, 1, 0, 0, 0])
x = np.random.randint(2, size=1000000)
# x = np.arange(10)%2

Rb = 4800
fs = 10 * Rb
# nc = 3
nc = 4
h = 1 / 2

s, t = gmsk_modulator(x, Rb, nc, h, fs)
s_filtered, _ = gmsk_modulator(x, Rb, nc, h, fs, 0.5, 0)

x_det = gmsk_detector(s_filtered, fs, Rb, nc)

n_errors = np.cumsum(np.abs(x - x_det))[-1]
print(n_errors)


# %%
