#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
#%%
from inits.initialization import *
from math import floor

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


# %%

for i in range(100):
    # Transmitter definition
    x_start = np.array([-15, 0, 15])  # Start coordinate for the transmitter in m
    v = np.array([1, 0, 0])  # Transmitter velocity in m/s
    t = 0
    fc = 436 * MHz
    amp = 10
    freq = 400
    s = Sine_Wave(amp, freq)
    tx0 = Transmitter(x_start, v, t, fc, s)

    x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
    v = np.array([1, 0, 0])  # Transmitter velocity in m/s
    t = 0
    fc = 436 * MHz
    amp = 10
    freq = 337
    s = Sine_Wave(amp, freq)
    tx1 = Transmitter(x_start, v, t, fc, s)

    x_start = np.array([30, 0, 15])  # Start coordinate for the transmitter in m
    v = np.array([1, 0, 0])  # Transmitter velocity in m/s
    t = 0
    fc = 436 * MHz
    amp = 10
    freq = 1300
    s = Sine_Wave(amp, freq)
    tx2 = Transmitter(x_start, v, t, fc, s)

    x_start = np.array([-30, 0, 15])  # Start coordinate for the transmitter in m
    v = np.array([1, 0, 0])  # Transmitter velocity in m/s
    t = 0
    fc = 436 * MHz
    amp = 10
    freq = 4100
    s = Sine_Wave(amp, freq)
    tx3 = Transmitter(x_start, v, t, fc, s)

    txs = []
    txs.append(tx0)
    txs.append(tx1)
    txs.append(tx2)
    txs.append(tx3)

    k = [2 * np.pi * txs[0].fc / c]

    # Phased array definition
    mx = 16  # Number of sensors in direction X
    my = 1  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].fc, origin)

    # Simulation parameters
    n = 1000  # Snapshots number
    d = len(txs)  # Number of signals/transmitters
    fs = 64 * MHz  # Sampling frequency
    fc = rx.fc
    sampling_time = 5 * ms  # Sampling time
    snr = 10  # Signal-to-noise ratio in dB
    simulation = Simulation(n, d, fs, fc, sampling_time, snr)

    [s, x] = doamusic_samples(txs, rx, simulation)
    print(np.sort(np.degrees(doaesprit_estimation(x, rx))))

