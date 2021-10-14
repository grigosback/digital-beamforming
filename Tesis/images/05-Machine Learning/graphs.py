#%%
import numpy as np
import time
from scipy.io import wavfile
from matplotlib import pyplot as plt
import scipy

import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

#%%
def phasedarray(x, mx, my, theta, phi, d_error, snr):
    m = mx * my
    n = x.size
    theta = np.radians(theta)
    phi = np.radians(phi)
    if d_error > 1:
        d_error = 1
    elif d_error <= 0:
        d_error = 0
    c = 299792458
    idx_x = np.repeat(np.arange(mx), my) + np.random.normal(0, d_error, m)
    idx_y = np.arange(m) % my + np.random.normal(0, d_error, m)
    a = np.exp(
        -1j * np.pi * np.cos(theta) * (np.cos(phi) * idx_x + np.sin(phi) * idx_y)
    )
    a = a.reshape(m, 1)
    sigma = np.sqrt(np.mean(x ** 2) / (10 ** (snr / 10)))
    w = np.random.normal(0, sigma, (m, n)) + 1j * np.random.normal(0, sigma, (m, n))
    x = x.reshape(1, n)
    X = a * x + w
    return X


def random_sampler(x, n):
    ns = x.shape[1]
    idx = np.random.choice(ns, n, replace=False)
    idx.sort()
    x_rs = x[:, idx]
    return x_rs


def esprit(Es, mx, my):
    D = Es.shape[1]
    E1_x = np.zeros(((mx - 1) * my, D), dtype="complex")
    E2_x = np.zeros(((mx - 1) * my, D), dtype="complex")
    E1_y = np.zeros(((my - 1) * mx, D), dtype="complex")
    E2_y = np.zeros(((my - 1) * mx, D), dtype="complex")

    for i in range(D):
        Es_aux = Es[:, i].reshape(mx, my)
        E1_x[:, i] = Es_aux[0 : mx - 1, :].reshape((mx - 1) * my)
        E2_x[:, i] = Es_aux[1:mx, :].reshape((mx - 1) * my)
        E1_y[:, i] = Es_aux[:, 0 : my - 1].reshape((my - 1) * mx)
        E2_y[:, i] = Es_aux[:, 1:my].reshape((my - 1) * mx)

    _, _, V_x = np.linalg.svd(np.append(E1_x, E2_x, axis=1), full_matrices=False)
    V_x = V_x.T
    V12_x = V_x[0:D, D : 2 * D]
    V22_x = V_x[D : 2 * D, D : 2 * D]

    psi_x = -V12_x @ np.linalg.inv(V22_x)
    phi_x, _ = np.linalg.eig(psi_x)

    _, _, V_y = np.linalg.svd(np.append(E1_y, E2_y, axis=1), full_matrices=False)
    V_y = V_y.T
    V12_y = V_y[0:D, D : 2 * D]
    V22_y = V_y[D : 2 * D, D : 2 * D]

    psi_y = -V12_y @ np.linalg.inv(V22_y)
    phi_y, _ = np.linalg.eig(psi_y)

    theta_esprit = np.zeros(D)
    phi_esprit = np.zeros(D)

    for i in range(D):
        arg = (np.angle(phi_x[i]) ** 2 + np.angle(phi_y[i]) ** 2) / (np.pi ** 2)
        if abs(arg) <= 1:
            phi_esprit[i] = np.arctan2(np.angle(phi_y[i]), np.angle(phi_x[i]))
            theta_esprit[i] = np.arccos(np.sqrt(arg))
    return np.degrees(theta_esprit), np.degrees(phi_esprit)


c = 299792458
mx = 4
my = 4
m = mx * my
#%% Generate x
fc = 436e6
d = 2
d_error = 0
fs, data = wavfile.read("../03-DOAEst/gomx-1.wav")
data = data - np.average(data)
x1 = data[40000:50000] / max(data[40000:50000])

fs, data = wavfile.read("../03-DOAEst/aistechsat3.wav")
data = data - np.average(data)
x2 = data[40000:50000] / max(data[40000:50000])
x2 = x2
# %%
snr = 10
theta_1 = np.random.rand() * 70 + 10
phi_1 = np.random.rand() * 340 - 170
X1 = phasedarray(x1[0:5000], mx, my, theta_1, phi_1, d_error, snr)

theta_2 = np.random.rand() * 70 + 10
phi_2 = np.random.rand() * 340 - 170
X2 = phasedarray(x2[0:5000], mx, my, theta_2, phi_2, d_error, snr)
X = (X1 + X2) / 2

p = 0.1
N = X.shape[1]
x_rs = random_sampler(X, int(p * N))
E, S, _ = np.linalg.svd(x_rs)

#%%
Es = np.asmatrix(E[:, 0:d].reshape(m, 2))
theta_est_rs, phi_est_rs = esprit(Es, mx, my)

# %%
plt.figure(figsize=(10, 5), dpi=100)
plt.stem(np.arange(m), np.abs(S), "k", markerfmt="ro")
plt.plot([1.5, 1.5], [0, max(S)], "b", linestyle="--")
plt.xticks(np.arange(m))
plt.xlabel(r"$m$")
plt.ylabel(r"$|\lambda_m|$")
plt.annotate(
    "",
    [0.5, 17.5],
    xycoords="data",
    xytext=[2.5, 17.5],
    fontsize=12,
    arrowprops=dict(arrowstyle="<->", linestyle="-", color="b"),
)
plt.annotate(r"$\lambda_{\hat{S}}$", (0.5, 18.5), fontsize=12, color="b")
plt.annotate(r"$\lambda_{\hat{N}}$", (2.1, 18.5), fontsize=12, color="b")
plt.savefig("ml_aval.png", dpi=300, bbox_inches="tight")
plt.show()
# %%
# s_flip = np.abs(S[::-1])
plt.figure(figsize=(10, 5), dpi=100)
plt.stem(np.arange(m - 1) + 1, scipy.diff(S[::-1]), "k", markerfmt="ro")
plt.xticks(np.arange(m))
plt.xlabel(r"$m$")
plt.ylabel(r"$\partial|\lambda_m|$")
plt.savefig("ml_derivada.png", dpi=300, bbox_inches="tight")
plt.show()

# %%
scipy.diff(s_flip).argmax() + 1
# %%
scipy.diff(s_flip)
# %%
plt.figure()
plt.subplot(211)
plt.plot(x1)
plt.subplot(212)
plt.plot(x2)
plt.show()
# %%
sigmoid = lambda z: 1 / (1 + np.exp(-z))
# %%
x = np.linspace(-5, 5, 101)
y = sigmoid(x)


# %%
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(x, y, "r")
plt.xlabel(r"$z$")
plt.ylabel(r"$g(z)$")
plt.yticks([0, 0.25, 0.5, 0.75, 1])
plt.grid()
plt.savefig("ml_sigmoid.png", dpi=300, bbox_inches="tight")
plt.show()
# %%
x1 = np.linspace(-3, 3, 51)
y1 = -np.log(1 / (1 + np.exp(-x1)))
x2 = np.array([-3, 1, 3])
y2 = np.array([2.6, 0, 0])

plt.figure(figsize=(6, 3), dpi=100)
plt.plot(x1, y1, "k")
plt.plot(x2, y2, "r")
plt.legend([r"$-\log \frac{1}{1+e^{-z}}$", r"$\mathrm{cost}_1 (z)$"])
plt.xlabel(r"$z$")
plt.grid()
plt.savefig("ml_cost1.png", dpi=300, bbox_inches="tight")
plt.show()
# %%
x1 = np.linspace(-3, 3, 51)
y1 = -np.log(1 - 1 / (1 + np.exp(-x1)))
x2 = np.array([-3, -1, 3])
y2 = np.array([0, 0, 2.6])

plt.figure(figsize=(6, 3), dpi=100)
plt.plot(x1, y1, "k")
plt.plot(x2, y2, "r")
plt.legend([r"$-\log \left(1- \frac{1}{1+e^{-z}}\right)$", r"$\mathrm{cost}_0 (z)$"])
plt.xlabel(r"$z$")
plt.grid()
plt.savefig("ml_cost0.png", dpi=300, bbox_inches="tight")
plt.show()
# %%
