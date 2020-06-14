# %%
import numpy as np
from scipy.signal import hilbert

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
