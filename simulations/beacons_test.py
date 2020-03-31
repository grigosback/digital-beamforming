#%%
from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

#%%
fs, x = wavfile.read("../beacons/beesat_9.wav")
t = np.arange(len(x)) / fs
X = np.fft.fftshift(np.fft.fft(x))
f = np.fft.fftshift(np.fft.fftfreq(len(x), 1 / fs))

# %%
plt.figure()
plt.grid()
plt.plot(t, x)
plt.xlabel("Tiempo [s]")
plt.ylabel("x(t)")
plt.show()

# %%
plt.figure()
plt.grid()
plt.plot(f / 1000, X)
plt.xlabel("Frecuencia [kHz]")
plt.ylabel("X(f)")
plt.show()
# %%


# %%
fs

# %%
