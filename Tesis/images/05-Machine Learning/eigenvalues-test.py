#%%
import numpy as np
import matplotlib.pyplot as plt
from numpy import loadtxt
import random
import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

# load array
#%%
data = loadtxt("eigenvalues4.csv", delimiter=",")
# %%
data[2, :]
# %%
idx = np.asarray(np.where(data[:, 2] == 1)).flatten()
signal = data[idx, :]
# %%
signal
# %%
idx = np.asarray(np.where(data[:, 2] == 0)).flatten()
noise = data[idx, :]
# %%
noise
# %%
signal_idx = random.choices(np.arange(signal.shape[0]), k=1000)
noise_idx = random.choices(np.arange(noise.shape[0]), k=1000)
plt.figure()
plt.plot(signal[signal_idx, 1], signal[signal_idx, 0], "o")
plt.plot(noise[noise_idx, 1], noise[noise_idx, 0], "x")
plt.xlabel(r"$\lambda$")
plt.ylabel(r"SNR [dB]")
plt.show()
# %%
