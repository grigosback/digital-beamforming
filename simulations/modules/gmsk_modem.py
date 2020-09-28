# %%
import numpy as np
from scipy.signal import hilbert

#%%
def gmsk_modulator(x, Rb, nc, h, fs, alpha=0.5, msk=1):
    n = len(x)
    fc = nc * Rb / 4

    t_max = n / Rb
    ns = int(t_max * fs)  # number of samples
    nspb = int(fs / Rb)  # samples per bit
    t = np.linspace(0, t_max, ns)

    x_nrz = np.zeros(ns)

    for i in range(n):
        x_nrz[i * nspb : (i + 1) * nspb] = 2 * (x[i] - 0.5)

    phi = np.cumsum(np.concatenate(([0], x_nrz)))[0:ns]
    phi = (phi) / nspb * np.pi / 2

    if msk == 0:
        PHI = np.fft.fft(phi) / ns
        # PHI = PHI / max(abs(PHI))
        f = np.fft.fftfreq(len(PHI), 1 / fs)

        W = alpha * Rb
        H = np.exp((-np.log(2) / 2) * (f / W) ** 2)

        PHI_filtered = PHI * H

        phi = np.real(np.fft.ifft(PHI_filtered)) * ns
        # phi = phi / max(phi)*np.pi

    s = np.cos(2 * np.pi * fc * t + phi)

    return s, t


def gmsk_detector(y, fs, Rb, nc):
    ns = len(y)
    nspb = int(fs / Rb)
    n = int(ns / nspb)

    t = np.arange(ns) / fs
    fc = nc * Rb / 4
    I = y * np.cos(2 * np.pi * fc * t)
    Q = y * np.sin(2 * np.pi * fc * t)
    I = lpfilter(I, fs, fc)
    Q = lpfilter(Q, fs, fc)

    phi = np.arctan2(I, Q)
    x_diff = np.diff(phi, 1)
    idx = np.where(np.abs(x_diff) > np.pi)
    for i in range(len(idx)):
        x_diff[idx[i]] = x_diff[idx[i] - 1]

    x_diff = x_diff / max(x_diff)
    x = np.zeros(n, dtype=int)
    for i in range(n):
        if x_diff[i * nspb + int(nspb / 2)] > 0:
            x[i] = 1
        else:
            x[i] = 0
    return x


def lpfilter(x, fs, f_lp):
    n = len(x)
    f = np.fft.fftfreq(n, 1 / fs)
    for i in range(n):
        if np.abs(f[i]) > f_lp:
            f[i] = 0
        else:
            f[i] = 1
    X = np.fft.fft(x) / n
    X = X * f
    x = np.real(np.fft.ifft(X)) * n
    return x


"""def gmsk_detector(y, fs, Rb, nc):
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
    return instantaneous_frequency"""
