#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")
from inits.initialization import *
from algorithms.music import doamusic_estimation
from algorithms.esprit import *
from modules.beamformer import *

from matplotlib import pyplot as plt

#%%
# Phased array definition
mx = 4  # Number of sensors in direction X
my = 4  # Number of sensors in direction Y
origin = np.array([0, 0, 0])  # Axis origin
fc_nom = 436 * MHz
rx = PhasedArray(mx, my, fc_nom, origin)

# Simulation parameters
n = 1024  # Snapshots number
d = 1  # Number of signals/transmitters
snr = 7  # SNR in dB
simulation = Simulation(n, d, snr)

# Transmitter definition
x_start = np.array([15, 15, 36.74234614])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
amp = 10
freq = 1300
fs = 48 * kHz  # Sampling frequency
t_max = 1  # Sampling time
sine = Sine_Wave(amp, freq, fs, t_max, n)

#%%
n = 100
n_error = 10
doa_est = np.zeros((2, n))
error_az = np.zeros(n)
error_el = np.zeros(n)
fc_array = np.zeros(n)

for i in range(n):
    fc = 436 * MHz + i * 0.1 * MHz
    fc_array[i] = fc
    tx0 = Transmitter(x_start, v, t, fc, sine)
    txs = []
    txs.append(tx0)
    doa = np.degrees([txs[0].doa.az, txs[0].doa.el])

    [s, x] = doa_samplesgen(txs, rx, simulation)
    for j in range(n_error):
        doa_est[:, i] = doaesprit_estimation(x, rx)
        doa_est[:, i] = np.degrees(doa_est[:, i])
        error_az[i] = error_az[i] + (1 / n_error) * (doa_est[0, i] - doa[0]) ** 2

        error_el[i] = error_el[i] + (1 / n_error) * (doa_est[1, i] - doa[1]) ** 2

# %%
plt.figure(figsize=(16, 9), dpi=100)
plt.plot((fc_array - 436 * MHz) / MHz, error_az ** 0.5 * 100 / doa[0])
plt.plot((fc_array - 436 * MHz) / MHz, error_el ** 0.5 * 100 / doa[1])
plt.xlabel("Corrimiento Doppler [MHz]")
plt.ylabel("Error porcentual [%]")
plt.legend(["Azimut", "Elevación"])
plt.grid()
plt.savefig("images/sim_esprit_doppler.png", dpi=100, bbox_inches="tight")
plt.show()
#%%
doa_est[1, :]
#%%
doa_est[0, -1]
# %%
# Transmitter definition
x_start = np.array([15, 15, 36.74234614])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
amp = 10
freq = 1300
fs = 48 * kHz  # Sampling frequency
t_max = 0.1  # Sampling time
n = 1024
sine = Sine_Wave(amp, freq, fs, t_max, n, 0)
fc = 436 * MHz
k = 2 * np.pi * fc / c
tx0 = Transmitter(x_start, v, t, fc, sine)
txs = []
txs.append(tx0)
#%%

[s, x] = doa_samplesgen(txs, rx, simulation)
#%%
x_rs, _ = random_sampler(x, n, rx.m)
#%%
x_rs.shape
#%%
doa_est = doaesprit_estimation(x_rs, rx, k)
y = beamformer(x, rx, doa_est, fc)
fc_est = carrieresprit_estimation(y, rx)
print(fc_est)
#%%
x[:, 0]
#%%
k = 2 * np.pi * fc_est / c
[s, x] = doamusic_samples(txs, rx, simulation)
fc_est = carrieresprit_estimation(x, rx, doa_est)

k = 2 * np.pi * fc_est / c
[s, x] = doamusic_samples(txs, rx, simulation)
doa_est = doaesprit_estimation(x, rx, k)

print(np.degrees(doa_est))
print(fc_est)


# %%
n = 300
fc_est = np.zeros(n)
doa_est = np.zeros((2, n))

[s, x] = doamusic_samples(txs, rx, simulation)
doa_est[:, -1] = doaesprit_estimation(x, rx)

for i in range(n):
    print(i)
    [s, x] = doamusic_samples(txs, rx, simulation)
    fc_est[i] = carrieresprit_estimation(x, rx, doa_est[:, i - 1])
    k = 2 * np.pi * fc_est[i] / c

    [s, x] = doamusic_samples(txs, rx, simulation)
    doa_est[:, i] = doaesprit_estimation(x, rx, k)


# %%
fc_est

# %%
plt.figure(figsize=(16, 9), dpi=100)
plt.plot(fc_est / 10 ** 6)
plt.plot([0, 300], [fc / 10 ** 6, fc / 10 ** 6], linestyle="--")
plt.legend([r"$\hat{f_c}$", r"$f_c$"])
plt.xlabel("Iteraciones")
plt.ylabel("Frecuencia [MHz]")
plt.savefig("images/sim_esprit_carrierest.png", dpi=200, bbox_inches="tight")
plt.show()

# %%
fc

# %%
tx0 = Transmitter(x_start, v, t, fc, s)
# %%
tx0.x.data.size
# %%
