#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
from inits.initialization import *


#%%
def doaesprit_estimation(x, rx):
    m = x.shape[0]

    [u, s, v] = np.linalg.svd(x)

    aval_min = s[0]
    # Get multiplicity 'q' of the minimun eigenvalue
    bins_aval = np.histogram(s, bins=200)
    for i in range(0, s.size):
        if bins_aval[0][i] == 0:
            umbral = bins_aval[1][i]
            break
    q = 0

    for i in range(0, m):
        if s[i] < umbral:
            q += 1
    d = m - q

    us = u[:, 0:d]

    if rx.mx == 1 or rx.my == 1:
        u1 = us[0 : m - 1, :].reshape(m - 1, d)
        u2 = us[1:m, :].reshape(m - 1, d)
        [uu, ss, vv] = np.linalg.svd(np.append(u1, u2, axis=1), full_matrices=False)
        vv = vv.T

        vv12 = vv[0:d, d : 2 * d]
        vv22 = vv[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi = -vv12 @ np.linalg.inv(vv22)
        [phi, psi_avec] = np.linalg.eig(psi)
        theta = np.zeros(d)
        for i in range(d):
            theta[i] = np.arcsin(np.angle(phi[i]) / (np.pi))

        return theta

    else:
        u1_x = np.zeros(((rx.mx - 1) * rx.my, d), dtype=complex)
        u2_x = np.zeros(((rx.mx - 1) * rx.my, d), dtype=complex)
        u1_y = np.zeros(((rx.my - 1) * rx.mx, d), dtype=complex)
        u2_y = np.zeros(((rx.my - 1) * rx.mx, d), dtype=complex)

        for i in range(d):
            us_aux = us[:, i].reshape(rx.mx, rx.my)
            u1_x[:, i] = us_aux[0 : rx.mx - 1, :].reshape((rx.mx - 1) * rx.my)
            u2_x[:, i] = us_aux[1 : rx.mx, :].reshape((rx.mx - 1) * rx.my)
            u1_y[:, i] = us_aux[:, 0 : rx.my - 1].reshape((rx.my - 1) * rx.mx)
            u2_y[:, i] = us_aux[:, 1 : rx.my].reshape((rx.my - 1) * rx.mx)

        [uu_x, ss_x, vv_x] = np.linalg.svd(
            np.append(u1_x, u2_x, axis=1), full_matrices=False
        )
        vv_x = vv_x.T

        vv12_x = vv_x[0:d, d : 2 * d]
        vv22_x = vv_x[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi_x = -vv12_x @ np.linalg.inv(vv22_x)
        [phi_x, psi_avec] = np.linalg.eig(psi_x)

        [uu_y, ss_y, vv_y] = np.linalg.svd(
            np.append(u1_y, u2_y, axis=1), full_matrices=False
        )
        vv_y = vv_y.T

        vv12_y = vv_y[0:d, d : 2 * d]
        vv22_y = vv_y[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi_y = -vv12_y @ np.linalg.inv(vv22_y)
        [phi_y, psi_avec] = np.linalg.eig(psi_y)

        az = np.arctan2(np.angle(phi_y), np.angle(phi_x))

        el = np.arccos(
            np.sqrt((np.angle(phi_x) ** 2 + np.angle(phi_y) ** 2) / (np.pi ** 2))
        )

        return [az, el]


# %%


# Transmitter definition
x_start = np.array([15, 15, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 400
s = Sine_Wave(amp, freq)
tx0 = Transmitter(x_start, v, t, fc, s)

x_start = np.array([-15, -15, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 337
s = Sine_Wave(amp, freq)
tx1 = Transmitter(x_start, v, t, fc, s)

x_start = np.array([-15, 15, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 500
s = Sine_Wave(amp, freq)
tx2 = Transmitter(x_start, v, t, fc, s)

x_start = np.array([15, -15, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 700
s = Sine_Wave(amp, freq)
tx3 = Transmitter(x_start, v, t, fc, s)

txs = []
txs.append(tx0)
# txs.append(tx1)
# txs.append(tx2)
# txs.append(tx3)

# Simulation parameters
n = 1000  # Snapshots number
d = len(txs)  # Number of signals/transmitters
fs = 64 * MHz  # Sampling frequency
fc = rx.fc
sampling_time = 5 * ms  # Sampling time
snr = 2  # Signal-to-noise ratio in dB
simulation = Simulation(n, d, fs, fc, sampling_time, snr)

# Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
rx = PhasedArray(mx, my, txs[0].fc, origin)

#%%
for i in range(10):
    [s, x] = doamusic_samples(txs, rx, simulation)
    [az, el] = doaesprit_estimation(x, rx)

    for i in range(d):
        print(r"Tx[" + str(i) + "] - az=" + str(np.degrees(az[i])))
        # print(r"Tx[" + str(i) + "] - el=" + str(np.degrees(el[i])))

    # for i in range(d):
    #    print(r"Tx[" + str(i) + "] - az=" + str(np.degrees(txs[i].doa.az)))
    #    print(r"Tx[" + str(i) + "] - el=" + str(np.degrees(txs[i].doa.el)))


# %%
