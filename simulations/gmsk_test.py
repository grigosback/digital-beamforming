#%%
import sys
import matplotlib
import matplotlib.pyplot as plt
from scipy import signal

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")

from modules.gmsk_modem import *

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

#%%
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


#%%
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


# %%
x = np.tile(np.array([1, 1, 1, 1, 0, 0, 0, 0]), 10)
# x = np.array([1, 0, 1, 0, 1, 0, 1])
# x = np.random.randint(2, size=100)
# x = np.arange(10)%2
Rb = 4800
fs = 100 * Rb
# nc = 3
nc = 4
h = 1 / 2
alpha = 0.5
fc = nc * Rb / 4
f1 = fc + h * Rb / 2
f2 = fc - h * Rb / 2

s_msk, t = gmsk_modulator(x, Rb, nc, h, fs, 0.3)
s_gmsk, _ = gmsk_modulator(x, Rb, nc, h, fs, alpha, 0)
f = np.fft.fftshift(np.fft.fftfreq(len(s_gmsk), 1 / fs))

plt.figure()
plt.plot(t, s_msk)
plt.plot(t, s_gmsk)
plt.xticks(np.arange(len(x)) / Rb)
plt.yticks([-1, 0, 1])
plt.grid()
plt.show()

#%%
plt.figure()
plt.plot(f, np.abs(np.fft.fftshift(np.fft.fft(s_msk))))
plt.plot(f, np.abs(np.fft.fftshift(np.fft.fft(s_gmsk))))
plt.grid()
plt.show()

#%%

#%%
I = s_gmsk * np.cos(2 * np.pi * fc * t)
Q = s_gmsk * np.sin(2 * np.pi * fc * t)
f = np.fft.fftshift(np.fft.fftfreq(len(I), 1 / fs))
I = lpfilter(I, fs, fc)
Q = lpfilter(Q, fs, fc)

plt.figure()
plt.subplot(211)
plt.plot(t, I)
plt.grid()
plt.subplot(212)
plt.plot(t, Q)
# plt.xticks(np.arange(len(x)) / Rb)
# plt.yticks([-1, 0, 1])
plt.grid()
plt.show()

#%%

plt.figure()
plt.subplot(211)
plt.plot(f, np.abs(np.fft.fftshift(np.fft.fft(I))))
plt.grid()
plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(np.fft.fft(Q))))
plt.grid()
plt.show()

#%%
x_det = gmsk_detector(s_gmsk, fs, Rb, nc)
np.cumsum(np.abs(x - x_det))[-1]
#%%
# order = 4
# Wn = (fc / 2) / (fs / 2)  # frecuencia normalizada del filtro
# [b, a] = signal.butter(order, Wn)
# I = signal.lfilter(b, a, I)
# Q = signal.lfilter(b, a, Q)
phi_det = np.arctan2(I, Q)
x_diff = np.diff(phi_det, 1)
idx = np.where(np.abs(x_diff) > np.pi)
for i in range(len(idx)):
    x_diff[idx[i]] = x_diff[idx[i] - 1]
#%%
"""plt.figure()
plt.plot(phi_det)
plt.xticks(np.arange(len(x)) / Rb)
plt.grid()
plt.show()"""

plt.figure()
plt.plot(t[0 : len(x_diff)], x_diff / max(x_diff))
plt.xticks(np.arange(len(x)) / Rb)
plt.grid()
plt.show()

"""plt.figure()
plt.plot(I / Q)
plt.xticks(np.arange(len(x)) / Rb)
plt.grid()
plt.show()"""
#%%
x_det = np.zeros(len(x))
for i in range(len(x)):
    if x_diff[i * 100 + 50] < 0:
        x_det[i] = 0
    else:
        x_det[i] = 1
np.cumsum(np.abs(x - x_det))[-1]
#%%
x_diff[140] - x_diff[139] - np.pi * 2
# %%
# x = np.array([1, 1, 0, 1, 0, 0, 0])
x = np.random.randint(2, size=10000)
# x = np.arange(10)%2

Rb = 4800
fs = 10 * Rb
# nc = 3
nc = 4
h = 1 / 2
alpha = 0.3

s_msk, t = gmsk_modulator(x, Rb, nc, h, fs)
x_det_msk = gmsk_detector(s_msk, fs, Rb, nc)
n_errors_msk = np.cumsum(np.abs(x - x_det_msk))[-1]


s_gmsk, _ = gmsk_modulator(x, Rb, nc, h, fs, alpha, 0)
x_det_gmsk = gmsk_detector(s_gmsk, fs, Rb, nc)
n_errors_gmsk = np.cumsum(np.abs(x - x_det_gmsk))[-1]


print(n_errors_msk)

print(n_errors_gmsk)


# %%
np.cumsum(t - np.arange(len(s_msk)))

# %%
