#%%
from scipy.io import wavfile
import time
import matplotlib
from scipy import signal
from matplotlib import pyplot as plt
from modules.random_sampler import *
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


def ber_calculator(x_bits, Rb, nc, h, msk, alpha, snr):
    signal, _ = gmsk_modulator(x_bits, Rb, nc, h, fs, alpha, msk)

    # Transmitter definition
    x_raw = Signal(fs, signal)
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
    simulation = Simulation(n, d, snr)

    [s, x] = doa_samplesgen(txs, rx, simulation)

    x_rs, _ = random_sampler(x, simulation.n)
    doa = doaesprit_estimation(x_rs, rx)
    x_beamformer = np.real(beamformer(x, rx, doa, fc))

    x_det = gmsk_detector(x_beamformer, fs, Rb, nc)
    n_errors = np.cumsum(np.abs(x_bits - x_det))[-1]
    ber = n_errors / len(x_bits)
    return ber


# %%
n_iterations = 14
ber_msk = np.zeros(n_iterations)
ber_gmsk = np.zeros(n_iterations)

Rb = 4800
fs = 10 * Rb
nc = 4
h = 1 / 2
alpha = 0.3
x_bits = np.random.randint(2, size=100000)
snr = np.zeros(n_iterations)
for i in range(n_iterations):
    snr[i] = i - n_iterations + 5
    ber_msk[i] = ber_calculator(x_bits, Rb, nc, h, 1, alpha, snr[i])
    print("ber_msk = " + str(ber_msk[i]))
    ber_gmsk[i] = ber_calculator(x_bits, Rb, nc, h, 0, alpha, snr[i])
    print("ber_gmsk = " + str(ber_gmsk[i]))

#%%
plt.figure()
plt.plot(snr[0 : n_iterations - 6], ber_msk[0 : n_iterations - 6])
plt.plot(snr, ber_gmsk)
plt.yscale("Log")
plt.title("sim_ber.py")
plt.xlabel("SNR [dB]")
plt.ylabel("BER")
plt.legend(["MSK", "GMSK"])
plt.grid()
plt.savefig("images/sim_ber/sim_ber.png", dpi=200, bbox_inches="tight")
plt.show()

# %%
ber[-1]

# %%
n_errors

# %%
len(x_bits)

# %%
plt.figure()
plt.plot(t, s)
plt.plot(t, s_filtered)
plt.xticks(np.arange(len(x)) / Rb)
plt.yticks([-1, 0, 1])
plt.grid()
plt.show()
