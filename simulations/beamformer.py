#%%
import sys

#%%
sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
#%%
from inits.initialization import *
from algorithms.esprit import doaesprit_estimation

#%%
# def beamformer(x,doa,fc):

#%%
# Transmitter definition
x_start = np.array([15, 15, 36.74234614])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
t = 0
fc = 436 * MHz
amp = 10
freq = 40000
s = Sine_Wave(amp, freq)
tx0 = Transmitter(x_start, v, t, fc, s)

txs = []
txs.append(tx0)

#%%
[s, x] = doamusic_samples(txs, rx, simulation)
doa = doaesprit_estimation(x, rx)
