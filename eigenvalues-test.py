#%%
import numpy as np
import matplotlib.pyplot as plt
from numpy import loadtxt
import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

# load array
#%%
data = loadtxt("eigenbalues.csv", delimiter=",")
idx = np.asarray(np.where(data[:, 2] == 1)).flatten()
signal = data[idx, :]
idx = np.asarray(np.where(data[:, 2] == 0)).flatten()
noise = data[idx, :]
# %%
np.random.shuffle(signal)
np.random.shuffle(noise)
plt.figure()
plt.plot(signal[::50, 1], -signal[::50, 0], "o")
plt.plot(noise[::200, 1], -noise[::200, 0], "x")
plt.xlabel(r"$\lambda$")
plt.ylabel(r"SNR [dB]")
plt.show()
# %%
np.random.shuffle(signal)

# %%
signal
# %%
