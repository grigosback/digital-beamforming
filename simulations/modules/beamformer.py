#%%
import numpy as np


def beamformer(x, rx, doa, fc):
    c = 3e8
    k = 2 * np.pi * fc / c
    beta_vec = np.empty((rx.mx, 1), dtype=complex)
    gamma_vec = np.empty((rx.my, 1), dtype=complex)

    [beta, gamma] = [
        np.e ** (1j * k * rx.d * np.cos(doa[1]) * np.cos(doa[0])),
        np.e ** (1j * k * rx.d * np.cos(doa[1]) * np.sin(doa[0])),
    ]

    for i in range(rx.mx):
        beta_vec[i] = beta ** (-i)

    for j in range(rx.my):
        gamma_vec[j] = gamma ** (-j)

    a = np.kron(beta_vec, gamma_vec).ravel()

    s = np.zeros(x.shape[1], dtype=complex)

    for i in range(s.size):
        x_n = x[:, i] * a.conj()
        s[i] = np.average(x_n)

    return s
