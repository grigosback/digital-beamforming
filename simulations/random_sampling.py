#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from matplotlib import pyplot as plt


#%%
sampling_time = 0.5 * ms
fs = 48 * kHz
t = np.linspace(0, sampling_time, int(sampling_time * fs))
amp = 10
freq = 1300
sine = amp * np.cos(2 * np.pi * freq * (t))
# sine2 = amp * np.cos(2 * np.pi * freq * simulation.t)

# %%
plt.figure(figsize=(16, 9), dpi=200)
plt.subplot(211)
plt.plot(t * 1000, sine)
plt.stem(t[::6400] * 1000, sine[::6400])
plt.xlabel("Tiempo [ms]", size=20)
plt.yticks([])
plt.subplot(212)
plt.plot(t * 1000, sine)
plt.stem(simulation.t[::20] * 1000, sine2[::20])
plt.xlabel("Tiempo [ms]", size=20)
plt.yticks([])
plt.savefig("sim_random_sampling.png", dpi=200, bbox_inches="tight")
plt.show()

# %%
plt.figure(figsize=(16, 9), dpi=100)
plt.plot(t * 1000, sine)
plt.stem(t * 1000, sine)
plt.xlabel("Tiempo [ms]", size=20)
plt.yticks([])
plt.savefig("images/sim_esprit_carrier_diagram.png", dpi=100, bbox_inches="tight")
plt.show()

# %%
len(sine2[::20])

# %%
sine[::6400]

# %%
