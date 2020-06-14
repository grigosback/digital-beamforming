#%%
from scipy.io import wavfile
import time
import matplotlib
from scipy import signal
from matplotlib import pyplot as plt
from modules.ramdom_sampler import *
from modules.beamformer import *
from modules.gmsk_modem import *
from algorithms.esprit import carrieresprit_estimation
from algorithms.esprit import doaesprit_estimation
from algorithms.music import doamusic_estimation
from inits.initialization import *
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

# %%
n_iterations = 10
ber = np.zeros(n_iterations)

for i in range(n_iterations):
    x_bits = np.random.randint(2, size=10000)
    Rb = 4800
    fs = 10 * Rb
    nc = 4
    h = 1 / 2

    s_raw, t_signal = gmsk_modulator(x_bits, Rb, nc, h, fs)
    s_filtered, _ = gmsk_modulator(x_bits, Rb, nc, h, fs, 0.5, 0)

    # Transmitter definition
    x_raw = Signal(fs, s_raw)
    x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
    v = np.array([1, 0, 0])  # Transmitter velocity in m/s
    t = 0
    fc = 436 * MHz
    tx0 = Transmitter(x_start, v, t, fc, x_raw)
    txs = []
    txs.append(tx0)

    # Phased array definition
    mx = 4  # Number of sensors in direction X
    my = 4  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].fc, origin)

    # Simulation parameters
    n = 1000  # Snapshots number
    d = len(txs)  # Number of signals/transmitters
    snr = 0 + i  # Signal-to-noise ratio in dB
    simulation = Simulation(n, d, snr)

    [s, x] = doa_samplesgen(txs, rx, simulation)

    x_rs, _ = random_sampler(x, simulation.n)
    doa = doaesprit_estimation(x_rs, rx)
    x_beamformer = np.real(beamformer(x, rx, doa, fc))

    x_det = gmsk_detector(x_beamformer, fs, Rb, nc)
    n_errors = np.cumsum(np.abs(x_bits - x_det))[-1]
    print(n_errors)
    ber[i] = n_errors / len(x_bits)

#%%
plt.figure()
plt.plot(np.arange(10), ber)
plt.yscale("Log")
plt.ylim(0.01, 0.2)
plt.grid()
plt.show()

# %%
