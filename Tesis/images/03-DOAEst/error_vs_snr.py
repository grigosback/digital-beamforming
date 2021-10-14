#%%
import numpy as np
import time
from scipy.io import wavfile
from matplotlib import pyplot as plt

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


def music(En, A, theta_array, phi_array):
    P_mu = np.empty((A.shape[1], A.shape[2]), dtype="complex")
    for i in range(P_mu.shape[0]):
        for j in range(P_mu.shape[1]):
            a = np.asmatrix(A[:, i, j])
            a = a.T
            P_mu[i, j] = 1 / (a.H @ En @ En.H @ a)
    idx = np.unravel_index(np.argmax(P_mu, axis=None), P_mu.shape)
    theta_est = np.degrees(theta_array[idx[1]])
    phi_est = np.degrees(phi_array[idx[0]])

    return P_mu, theta_est, phi_est


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

theta_array = np.radians(np.linspace(0, 90, 181))
phi_array = np.radians(np.linspace(-180, 180, 721))
A = np.empty((m, phi_array.size, theta_array.size), dtype="complex")

for ay, theta in enumerate(theta_array):
    for ax, phi in enumerate(phi_array):
        for idx_x in range(mx):
            for idx_y in range(my):
                A[idx_x * mx + idx_y, ax, ay] = np.exp(
                    -1j
                    * np.pi
                    * np.cos(theta)
                    * (np.cos(phi) * idx_x + np.sin(phi) * idx_y)
                )
#%% Generate x
fc = 436e6
d = 1
d_error = 0
fs, data = wavfile.read("gomx-1.wav")
data = data - np.average(data)
x = data / max(data)
#%%
theta_0 = 45
phi_0 = 30
# theta_0 = np.random.randint(0, 90)
# phi_0 = np.random.randint(-180, 180)
snr_array = np.array([-10, -5, 0, 10])
P_mu = np.empty((A.shape[1], A.shape[2], snr_array.size), dtype="complex")
for i, snr in enumerate(snr_array):
    X = phasedarray(x, mx, my, theta_0, phi_0, d_error, snr)
    n_rs = int(x.size / 100)
    x_rs = random_sampler(X, n_rs)

    E, S, _ = np.linalg.svd(x_rs)
    Es = np.asmatrix(E[:, 0].reshape(m, d))
    En = np.asmatrix(E[:, 1:].reshape(m, m - d))

    P_mu[:, :, i], theta_music, phi_music = music(En, A, theta_array, phi_array)
    print(theta_music, phi_music)

# %%
plt.figure(figsize=(7.5, 3.75), dpi=300)
plt.imshow(
    10 * np.log10(abs(P_mu[:, :, 0]).T),
    extent=(
        np.degrees(phi_array.min()),
        np.degrees(phi_array.max()),
        np.degrees(theta_array.max()),
        np.degrees(theta_array.min()),
    ),
    cmap="jet",
    aspect="auto",
)
plt.ylabel(r"$\hat{\theta}$ [°]", size=15)
plt.xlabel(r"$\hat{\varphi}$ [°]", size=15)
plt.colorbar()
plt.savefig("p_mu_-10.png", dpi=300, bbox_inches="tight")
plt.show()
#%%
plt.figure(figsize=(7.5, 3.75), dpi=300)
plt.imshow(
    10 * np.log10(abs(P_mu[:, :, 1]).T),
    extent=(
        np.degrees(phi_array.min()),
        np.degrees(phi_array.max()),
        np.degrees(theta_array.max()),
        np.degrees(theta_array.min()),
    ),
    cmap="jet",
    aspect="auto",
)
plt.ylabel(r"$\hat{\theta}$ [°]", size=15)
plt.xlabel(r"$\hat{\varphi}$ [°]", size=15)
plt.colorbar()
plt.savefig("p_mu_-5.png", dpi=300, bbox_inches="tight")
plt.show()
#%%
plt.figure(figsize=(7.5, 3.75), dpi=300)
plt.imshow(
    10 * np.log10(abs(P_mu[:, :, 2]).T),
    extent=(
        np.degrees(phi_array.min()),
        np.degrees(phi_array.max()),
        np.degrees(theta_array.max()),
        np.degrees(theta_array.min()),
    ),
    cmap="jet",
    aspect="auto",
)
plt.ylabel(r"$\hat{\theta}$ [°]", size=15)
plt.xlabel(r"$\hat{\varphi}$ [°]", size=15)
plt.colorbar()
plt.savefig("p_mu_0.png", dpi=300, bbox_inches="tight")
plt.show()
#%%
plt.figure(figsize=(7.5, 3.75), dpi=300)
plt.imshow(
    10 * np.log10(abs(P_mu[:, :, 3]).T),
    extent=(
        np.degrees(phi_array.min()),
        np.degrees(phi_array.max()),
        np.degrees(theta_array.max()),
        np.degrees(theta_array.min()),
    ),
    cmap="jet",
    aspect="auto",
)
plt.ylabel(r"$\hat{\theta}$ [°]", size=15)
plt.xlabel(r"$\hat{\varphi}$ [°]", size=15)
plt.colorbar()
plt.savefig("p_mu_10.png", dpi=300, bbox_inches="tight")
plt.show()
#%%
##############################################################################
# Error vs SNR
d_error = 0
mx = 4
my = 4
m = mx * my
start = -20
stop = 20
N = stop - start + 1
snr_array = np.linspace(start, stop, N)
theta_music_array = np.zeros(N)
phi_music_array = np.zeros(N)
theta_esprit_array = np.zeros(N)
phi_esprit_array = np.zeros(N)
rmse_music_array = np.zeros(N)
rmse_esprit_array = np.zeros(N)
n_sims = 10

# sumar la iteración sobre el mismo snr para promediar
for i, snr in enumerate(snr_array):
    j = 0
    while j != n_sims:
        print("snr = ", snr)
        theta = np.random.rand() * 70 + 10
        phi = np.random.rand() * 340 - 170
        X = phasedarray(x, mx, my, theta, phi, d_error, snr)
        n_rs = int(x.size / 100)
        x_rs = random_sampler(X, n_rs)
        E, S, _ = np.linalg.svd(x_rs)
        Es = np.asmatrix(E[:, 0].reshape(m, d))
        En = np.asmatrix(E[:, 1:].reshape(m, m - d))

        theta_esprit_array[i], phi_esprit_array[i] = esprit(Es, mx, my)
        if theta_esprit_array[i] != 0 or phi_esprit_array[i] != 0:
            _, theta_music_array[i], phi_music_array[i] = music(
                En, A, theta_array, phi_array
            )

            rmse_music_array[i] = rmse_music_array[i] + (
                (theta - theta_music_array[i]) ** 2 + (phi - phi_music_array[i]) ** 2
            )

            rmse_esprit_array[i] = rmse_esprit_array[i] + (
                (theta - theta_esprit_array[i]) ** 2 + (phi - phi_esprit_array[i]) ** 2
            )
            j += 1


rmse_music_array = np.sqrt(rmse_music_array / (n_sims))
rmse_esprit_array = np.sqrt(rmse_esprit_array / (n_sims))

# %%
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(snr_array, rmse_music_array, "k")
plt.plot(snr_array, rmse_esprit_array, "r")
plt.ylabel(r"RMSE($\hat{\theta},\hat{\phi}$) [°]")
plt.xlabel(r"SNR [dB]")
plt.legend(["MUSIC", "ESPRIT"])
plt.yscale("log")
plt.grid()
plt.savefig("error_vs_snr.png", dpi=300, bbox_inches="tight")
plt.show()
#%%

# %%
##############################################################################
# Error vs array
snr = 10
mx = 4
my = 4
m = mx * my
d_array = np.array([0, 1, 5, 10, 15, 20, 30]) / 100
N = d_array.size
theta_music_array = np.zeros(N)
phi_music_array = np.zeros(N)
theta_esprit_array = np.zeros(N)
phi_esprit_array = np.zeros(N)
rmse_music_array = np.zeros(N)
rmse_esprit_array = np.zeros(N)
n_sims = 20


for i, d_error in enumerate(d_array):
    j = 0
    while j != n_sims:
        print("d_error = ", d_error)
        theta = np.random.rand() * 70 + 10
        phi = np.random.rand() * 340 - 170
        X = phasedarray(x, mx, my, theta, phi, d_error, snr)
        n_rs = int(x.size / 100)
        x_rs = random_sampler(X, n_rs)
        E, S, _ = np.linalg.svd(x_rs)
        Es = np.asmatrix(E[:, 0].reshape(m, d))
        En = np.asmatrix(E[:, 1:].reshape(m, m - d))

        theta_esprit_array[i], phi_esprit_array[i] = esprit(Es, mx, my)
        if theta_esprit_array[i] != 0 or phi_esprit_array[i] != 0:
            _, theta_music_array[i], phi_music_array[i] = music(
                En, A, theta_array, phi_array
            )

            rmse_music_array[i] = rmse_music_array[i] + (
                (theta - theta_music_array[i]) ** 2 + (phi - phi_music_array[i]) ** 2
            )

            rmse_esprit_array[i] = rmse_esprit_array[i] + (
                (theta - theta_esprit_array[i]) ** 2 + (phi - phi_esprit_array[i]) ** 2
            )
            j += 1


rmse_music_array = np.sqrt(rmse_music_array / (n_sims))
rmse_esprit_array = np.sqrt(rmse_esprit_array / (n_sims))

# %%
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(d_array * 100, rmse_music_array, "k")
plt.plot(d_array * 100, rmse_esprit_array, "r")
plt.ylabel(r"RMSE($\hat{\theta},\hat{\phi}$) [°]")
plt.xlabel(r"$\frac{\sigma_d}{d}$ [%]")
plt.legend(["MUSIC", "ESPRIT"])
plt.yscale("log")
plt.grid()
plt.savefig("error_vs_d_error.png", dpi=300, bbox_inches="tight")
plt.show()
#%%
# %%
##############################################################################
# Error vs N
n_array = np.array([10, 100, 1000, 5000, 10000])
N = n_array.size
snr = 10
d_error = 0
snr = 10
mx = 4
my = 4
m = mx * my
theta_music_array = np.zeros(N)
phi_music_array = np.zeros(N)
theta_esprit_array = np.zeros(N)
phi_esprit_array = np.zeros(N)
rmse_music_array = np.zeros(N)
rmse_esprit_array = np.zeros(N)
n_sims = 10

for i, n_rs in enumerate(n_array):
    j = 0
    while j != n_sims:
        print("n_rs = ", n_rs)
        theta = np.random.rand() * 70 + 10
        phi = np.random.rand() * 340 - 170
        X = phasedarray(x, mx, my, theta, phi, d_error, snr)
        x_rs = random_sampler(X, n_rs)
        E, S, _ = np.linalg.svd(x_rs)
        Es = np.asmatrix(E[:, 0].reshape(m, d))
        En = np.asmatrix(E[:, 1:].reshape(m, m - d))

        theta_esprit_array[i], phi_esprit_array[i] = esprit(Es, mx, my)
        if theta_esprit_array[i] != 0 or phi_esprit_array[i] != 0:
            _, theta_music_array[i], phi_music_array[i] = music(
                En, A, theta_array, phi_array
            )

            rmse_music_array[i] = rmse_music_array[i] + (
                (theta - theta_music_array[i]) ** 2 + (phi - phi_music_array[i]) ** 2
            )

            rmse_esprit_array[i] = rmse_esprit_array[i] + (
                (theta - theta_esprit_array[i]) ** 2 + (phi - phi_esprit_array[i]) ** 2
            )
            j += 1


rmse_music_array = np.sqrt(rmse_music_array / (n_sims))
rmse_esprit_array = np.sqrt(rmse_esprit_array / (n_sims))

# %%
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(n_array, rmse_music_array, "k")
plt.plot(n_array, rmse_esprit_array, "r")
plt.ylabel(r"RMSE($\hat{\theta},\hat{\phi}$) [°]")
plt.xlabel(r"N")
plt.legend(["MUSIC", "ESPRIT"])
plt.xscale("log")
plt.yscale("log")
plt.grid()
plt.savefig("error_vs_n.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
###############################################################################
# Tiempo vs M
snr = 10
d_error = 0
m_array = np.arange(11) * 2 + 2

N = m_array.size
theta_music_array = np.zeros(N)
phi_music_array = np.zeros(N)
theta_esprit_array = np.zeros(N)
phi_esprit_array = np.zeros(N)
time_esprit = np.zeros(N)
time_music_05 = np.zeros(N)
time_music_10 = np.zeros(N)
time_music_20 = np.zeros(N)
time_music_50 = np.zeros(N)

n_sims = 5

for i, m_i in enumerate(m_array):
    mx = m_i
    my = m_i
    m = mx * my
    print("m = ", m)

    for j in range(n_sims):

        theta = np.random.rand() * 90
        phi = np.random.rand() * 360 - 180
        X = phasedarray(x, mx, my, theta, phi, d_error, snr)
        n_rs = int(x.size / 100)
        x_rs = random_sampler(X, n_rs)
        E, S, _ = np.linalg.svd(x_rs)
        Es = np.asmatrix(E[:, 0].reshape(m, d))
        En = np.asmatrix(E[:, 1:].reshape(m, m - d))

        start = time.time()
        theta_esprit_array[i], phi_esprit_array[i] = esprit(Es, mx, my)
        stop = time.time()
        time_esprit[i] = time_esprit[i] + (stop - start) / n_sims

        theta_array = np.radians(np.linspace(0, 90, 181))
        phi_array = np.radians(np.linspace(-180, 180, 721))

        A = np.empty((m, phi_array.size, theta_array.size), dtype="complex")

        for ay, theta in enumerate(theta_array):
            for ax, phi in enumerate(phi_array):
                for idx_x in range(mx):
                    for idx_y in range(my):
                        A[idx_x * mx + idx_y, ax, ay] = np.exp(
                            -1j
                            * np.pi
                            * np.cos(theta)
                            * (np.cos(phi) * idx_x + np.sin(phi) * idx_y)
                        )

        start = time.time()
        _, theta_music_array[i], phi_music_array[i] = music(
            En, A, theta_array, phi_array
        )
        stop = time.time()
        time_music_05[i] = time_music_05[i] + (stop - start) / n_sims

        theta_array = np.radians(np.linspace(0, 90, 91))
        phi_array = np.radians(np.linspace(-180, 180, 361))

        A = np.empty((m, phi_array.size, theta_array.size), dtype="complex")

        for ay, theta in enumerate(theta_array):
            for ax, phi in enumerate(phi_array):
                for idx_x in range(mx):
                    for idx_y in range(my):
                        A[idx_x * mx + idx_y, ax, ay] = np.exp(
                            -1j
                            * np.pi
                            * np.cos(theta)
                            * (np.cos(phi) * idx_x + np.sin(phi) * idx_y)
                        )

        start = time.time()
        _, theta_music_array[i], phi_music_array[i] = music(
            En, A, theta_array, phi_array
        )
        stop = time.time()
        time_music_10[i] = time_music_10[i] + (stop - start) / n_sims

        theta_array = np.radians(np.linspace(0, 90, 46))
        phi_array = np.radians(np.linspace(-180, 180, 181))

        A = np.empty((m, phi_array.size, theta_array.size), dtype="complex")

        for ay, theta in enumerate(theta_array):
            for ax, phi in enumerate(phi_array):
                for idx_x in range(mx):
                    for idx_y in range(my):
                        A[idx_x * mx + idx_y, ax, ay] = np.exp(
                            -1j
                            * np.pi
                            * np.cos(theta)
                            * (np.cos(phi) * idx_x + np.sin(phi) * idx_y)
                        )

        start = time.time()
        _, theta_music_array[i], phi_music_array[i] = music(
            En, A, theta_array, phi_array
        )
        stop = time.time()
        time_music_20[i] = time_music_20[i] + (stop - start) / n_sims

        theta_array = np.radians(np.linspace(0, 90, 19))
        phi_array = np.radians(np.linspace(-180, 180, 73))

        A = np.empty((m, phi_array.size, theta_array.size), dtype="complex")

        for ay, theta in enumerate(theta_array):
            for ax, phi in enumerate(phi_array):
                for idx_x in range(mx):
                    for idx_y in range(my):
                        A[idx_x * mx + idx_y, ax, ay] = np.exp(
                            -1j
                            * np.pi
                            * np.cos(theta)
                            * (np.cos(phi) * idx_x + np.sin(phi) * idx_y)
                        )

        start = time.time()
        _, theta_music_array[i], phi_music_array[i] = music(
            En, A, theta_array, phi_array
        )
        stop = time.time()
        time_music_50[i] = time_music_50[i] + (stop - start) / n_sims


# %%
my_data = np.genfromtxt("times_vs_m.csv", delimiter=",")
m_array = my_data[:, 0] ** 0.5
time_esprit = my_data[:, 1]
time_music_05 = my_data[:, 2]
time_music_10 = my_data[:, 3]
time_music_20 = my_data[:, 4]
time_music_50 = my_data[:, 5]

plt.figure(figsize=(10, 5), dpi=100)
plt.plot(m_array ** 2, time_music_05, "k")
plt.plot(m_array ** 2, time_music_10, "b")
plt.plot(m_array ** 2, time_music_20, "g")
plt.plot(m_array ** 2, time_music_50, "m")
plt.plot(m_array ** 2, time_esprit, "r")
plt.ylabel(r"Tiempo [s]")
plt.xlabel(r"M")
plt.legend(
    [
        r"MUSIC ($\mathfrak{R}=0,5^{\circ}$)",
        r"MUSIC ($\mathfrak{R}=1^{\circ}$)",
        r"MUSIC ($\mathfrak{R}=2^{\circ}$)",
        r"MUSIC ($\mathfrak{R}=5^{\circ}$)",
        "ESPRIT",
    ],
    loc="best",
    bbox_to_anchor=(0.5, 0.0, 0.45, 0.5),
)
plt.yscale("log")
plt.grid()
plt.savefig("time_vs_m.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
times_csv = np.append(
    (m_array ** 2).reshape(m_array.size, 1),
    time_esprit.reshape(m_array.size, 1),
    axis=1,
)
times_csv = np.append(times_csv, time_music_05.reshape(m_array.size, 1), axis=1)
times_csv = np.append(times_csv, time_music_10.reshape(m_array.size, 1), axis=1)
times_csv = np.append(times_csv, time_music_20.reshape(m_array.size, 1), axis=1)
times_csv = np.append(times_csv, time_music_50.reshape(m_array.size, 1), axis=1)
np.savetxt(
    "times_vs_m.csv",
    times_csv,
    delimiter=",",
    header="m,esprit,music_05,music_10,music_20,music_50",
)
#%%
#########################################################################
# SVD vs m
p_array = (np.arange(50) + 1) * 100
time_matmul = np.zeros(p_array.size)

for i, p in enumerate(p_array):
    print(i)
    Z = np.asmatrix(np.random.random((p, p)))
    Y = np.asmatrix(np.random.random((p, p)))
    start = time.time()
    O = Z @ Y
    stop = time.time()
    print(O)
    time_matmul[i] = stop - start

# %%
plt.figure()
plt.plot(p_array, time_matmul)
plt.plot(p_array, p_array.astype("float") ** 2.7 / 10 ** (10.5))
plt.grid()
plt.yscale("log")
plt.xscale("log")
plt.show()
# %%
p_array ** 3
# %%
# Tiempo vs M
snr = 10
d_error = 0
m_array = np.array([7, 13, 15, 20, 25])
N = m_array.size
time_svd_m = np.zeros(N)
n_sims = 10

for i, m_i in enumerate(m_array):
    mx = m_i
    my = m_i
    m = mx * my
    print("m = ", m)

    for j in range(n_sims):
        theta = np.random.rand() * 90
        phi = np.random.rand() * 360 - 180
        X = phasedarray(x, mx, my, theta, phi, d_error, snr)
        n_rs = 100
        x_rs = random_sampler(X, n_rs)
        start = time.time()
        E, S, _ = np.linalg.svd(x_rs)
        stop = time.time()
        time_svd_m[i] = stop - start

# Tiempo vs N
n_array = np.array([50, 150, 300, 450, 600])
N = n_array.size
snr = 10
d_error = 0
snr = 10
mx = 10
my = 10
m = mx * my
time_svd_n = np.zeros(N)
n_sims = 10

for i, n_rs in enumerate(n_array):
    print("n_rs=", n_rs)
    for j in range(n_sims):
        theta = np.random.rand() * 90
        phi = np.random.rand() * 360 - 180
        X = phasedarray(x, mx, my, theta, phi, d_error, snr)
        x_rs = random_sampler(X, n_rs)
        start = time.time()
        E, S, _ = np.linalg.svd(x_rs)
        stop = time.time()
        time_svd_n[i] = stop - start


# %%
fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
ax.plot(n_array, time_svd_n, "r", label="SVD vs. N")
ax.plot(m_array ** 2, time_svd_m, "k", label="SVD vs. M")
ax.legend()
ax.set_ylabel(r"Tiempo [s]")
ax.set_xlabel(r"N")
ax.set_yscale("log")
ax.grid()


def forward(x):
    return x


def inverse(x):
    return x


secax = ax.secondary_xaxis("top", functions=(forward, inverse))
secax.set_xlabel("M")
plt.savefig("svd_vs_n_m", dpi=300, bbox_inches="tight")
plt.show()
# %%
# %%
# Tiempo vs N
n_array = np.array([10, 30, 100, 300, 1000, 3000, 10000])
N = n_array.size
snr = 10
d_error = 0
snr = 10
mx = 4
my = 4
m = mx * my
time_svd_n = np.zeros(N)
n_sims = 10

for i, n_rs in enumerate(n_array):
    print("n_rs=", n_rs)
    for j in range(n_sims):
        theta = np.random.rand() * 90
        phi = np.random.rand() * 360 - 180
        X = phasedarray(x, mx, my, theta, phi, d_error, snr)
        x_rs = random_sampler(X, n_rs)
        start = time.time()
        E, S, _ = np.linalg.svd(x_rs)
        stop = time.time()
        time_svd_n[i] = stop - start
# %%
fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
ax.plot(n_array[2:], time_svd_n[2:], "r", label="SVD vs. N")
# ax.legend()
ax.set_ylabel(r"Tiempo [s]")
ax.set_xlabel(r"N")
# ax.ser_xticks([0,500,1000,3000,])
ax.set_yscale("log")
ax.set_xscale("log")
ax.grid()
plt.savefig("svd_vs_n_16", dpi=300, bbox_inches="tight")
plt.show()
# %%
##############################################################################
#%% Generate x
fc = 436e6
d = 2
d_error = 0
fs, data = wavfile.read("gomx-1.wav")
data = data - np.average(data)
x1 = data / max(data)

fs, data = wavfile.read("aistechsat3.wav")
data = data - np.average(data)
x2 = data / max(data)

x2 = x1[30000:31000]
x1 = x1[30500:31500]
#%%
t = np.linspace(0, np.pi, 5000)
x1 = np.cos(2 * np.pi * t)
x2 = np.cos(2 * np.pi * t * 1.1)

# Error vs N
p = np.linspace(0.04, 1, 25)
n_array = (p * x1.size).astype("int")
N = n_array.size
snr = 10
d_error = 0
snr = 10
mx = 4
my = 4
m = mx * my
rmse_rs_array = np.zeros(N)
rmse_cont_array = np.zeros(N)
n_sims = 10

for i, n_rs in enumerate(n_array):
    j = 0
    while j != n_sims:
        print("n_rs = ", n_rs)
        theta_1 = np.random.rand() * 70 + 10
        phi_1 = np.random.rand() * 340 - 170
        X1 = phasedarray(x1, mx, my, theta_1, phi_1, d_error, snr)

        theta_2 = np.random.rand() * 70 + 10
        phi_2 = np.random.rand() * 340 - 170
        X2 = phasedarray(x2, mx, my, theta_2, phi_2, d_error, snr)
        X = X1 + X2

        E, S, _ = np.linalg.svd(X[:, 0:n_rs])
        Es = np.asmatrix(E[:, 0:d].reshape(m, d))
        En = np.asmatrix(E[:, d:].reshape(m, m - d))
        theta_est_cont, phi_est_cont = esprit(Es, mx, my)

        x_rs = random_sampler(X, n_rs)
        E, S, _ = np.linalg.svd(x_rs)
        Es = np.asmatrix(E[:, 0:d].reshape(m, d))
        En = np.asmatrix(E[:, d:].reshape(m, m - d))
        theta_est_rs, phi_est_rs = esprit(Es, mx, my)

        if (
            (theta_est_rs[0] != 0 or phi_est_rs[0] != 0)
            and (theta_est_rs[1] != 0 or phi_est_rs[1] != 0)
            and (theta_est_cont[0] != 0 or phi_est_cont[0] != 0)
            and (theta_est_cont[1] != 0 or phi_est_cont[1] != 0)
        ):
            rmse_cont_array[i] = rmse_cont_array[i] + (
                (theta_1 + theta_2 - theta_est_cont[0] - theta_est_cont[1]) ** 2
                + (phi_1 + phi_2 - phi_est_cont[0] - phi_est_cont[1]) ** 2
            )

            rmse_rs_array[i] = (
                rmse_rs_array[i]
                + (max([theta_1, theta_2]) - max(theta_est_rs)) ** 2
                + (min([theta_1, theta_2]) - min(theta_est_rs)) ** 2
                + (max([phi_1, phi_2]) - max(phi_est_rs)) ** 2
                + (min([phi_1, phi_2]) - min(phi_est_rs)) ** 2
            )

            j += 1

rmse_rs_array = np.sqrt(rmse_rs_array / (4 * n_sims))
rmse_cont_array = np.sqrt(rmse_cont_array / (4 * n_sims))

# %%
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(p[1:], rmse_rs_array[1:], "r")
plt.plot(p[1:], rmse_cont_array[1:], "k")
plt.ylabel(r"RMSE($\hat{\theta},\hat{\phi}$) [°]")
plt.xlabel(r"$p$")
# plt.xscale("log")
plt.yscale("log")
plt.legend(
    ["Muestreo aleatorio", "Muestreo continuo",]
)
plt.grid()
plt.savefig("../04-Random Sampling/rs_vs_p.png", dpi=300, bbox_inches="tight")
plt.show()
# %%
plt.figure()
plt.plot(t[0 : n_array[2]], x1[0 : n_array[2]])
# plt.plot(t,x1)
plt.show()
# %%
#%%
t = np.linspace(0, np.pi, 5000)
x1 = np.cos(2 * np.pi * t)
x2 = np.cos(2 * np.pi * t * 1.1)

#%%
#%% Generate x
fc = 436e6
d = 2
d_error = 0
fs, data = wavfile.read("gomx-1.wav")
data = data - np.average(data)
x1 = data / max(data)

fs, data = wavfile.read("aistechsat3.wav")
data = data - np.average(data)
x2 = data / max(data)
x2 = x2[0 : x1.size]
#%%

# Error vs N
# T = np.linspace(0,10*2*np.pi, 10000)
n_array = np.linspace(1000, 10000, 20).astype("int")
N = n_array.size
snr = 10
d_error = 0
snr = 10
mx = 4
my = 4
m = mx * my

n_sims = 5

p_array = np.array([0.01, 0.1, 0.2, 0.3, 0.5])
rmse_rs_array = np.zeros((N, p_array.size))
rmse_cont_array = np.zeros(N)


for i, n in enumerate(n_array):
    j = 0
    while j != n_sims:
        print("n = ", n)

        theta_1 = np.random.rand() * 70 + 10
        phi_1 = np.random.rand() * 340 - 170
        X1 = phasedarray(x1[0:n], mx, my, theta_1, phi_1, d_error, snr)

        theta_2 = np.random.rand() * 70 + 10
        phi_2 = np.random.rand() * 340 - 170
        X2 = phasedarray(x2[0:n], mx, my, theta_2, phi_2, d_error, snr)
        X = X1 + X2

        E, S, _ = np.linalg.svd(X[:, 0:n])
        Es = np.asmatrix(E[:, 0:d].reshape(m, d))
        theta_est_cont, phi_est_cont = esprit(Es, mx, my)

        if (theta_est_cont[0] != 0 or phi_est_cont[0] != 0) and (
            theta_est_cont[1] != 0 or phi_est_cont[1] != 0
        ):

            rmse_cont_array[i] = (
                rmse_cont_array[i]
                + (max([theta_1, theta_2]) - max(theta_est_cont)) ** 2
                + (min([theta_1, theta_2]) - min(theta_est_cont)) ** 2
                + (max([phi_1, phi_2]) - max(phi_est_cont)) ** 2
                + (min([phi_1, phi_2]) - min(phi_est_cont)) ** 2
            )

            for k, p in enumerate(p_array):
                x_rs = random_sampler(X, int(p * n))
                E, S, _ = np.linalg.svd(x_rs)
                Es = np.asmatrix(E[:, 0:d].reshape(m, d))
                theta_est_rs, phi_est_rs = esprit(Es, mx, my)

                if (theta_est_rs[0] != 0 or phi_est_rs[0] != 0) and (
                    theta_est_rs[1] != 0 or phi_est_rs[1] != 0
                ):

                    rmse_rs_array[i, k] = (
                        rmse_rs_array[i, k]
                        + (max([theta_1, theta_2]) - max(theta_est_rs)) ** 2
                        + (min([theta_1, theta_2]) - min(theta_est_rs)) ** 2
                        + (max([phi_1, phi_2]) - max(phi_est_rs)) ** 2
                        + (min([phi_1, phi_2]) - min(phi_est_rs)) ** 2
                    )
                    if k == p_array.size - 1:
                        j += 1

rmse_rs_array = np.sqrt(rmse_rs_array / (n_sims))
rmse_cont_array = np.sqrt(rmse_cont_array / (n_sims))
# %%
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(n_array / fs * 1000, rmse_cont_array, "k")
for i in range(p_array.size):
    plt.plot(n_array / fs * 1000, rmse_rs_array[:, i])
plt.ylabel(r"RMSE($\hat{\theta},\hat{\phi}$) [°]")
plt.xlabel(r"$T$ [ms]")
# plt.xscale("log")
plt.yscale("log")
# plt.xticks([])
plt.legend(
    [
        "Muestreo ideal ($p=1$)",
        r"$p=0,01$",
        r"$p=0,1$",
        r"$p=0,2$",
        r"$p=0,3$",
        r"$p=0,5$",
    ]
)
# plt.legend(
#    ["Muestreo aleatorio", "Muestreo continuo",]
# )
plt.grid()
plt.savefig("../04-Random Sampling/rs_vs_T.png", dpi=300, bbox_inches="tight")
plt.show()
# %%

