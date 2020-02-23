#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from matplotlib import pyplot as plt


#%%
t = np.linspace(0, sampling_time, int(sampling_time * simulation.fs))

# %%
sine = txs[0].s.amp * np.cos(2 * np.pi * txs[0].s.freq * (t))
sine2 = txs[0].s.amp * np.cos(2 * np.pi * txs[0].s.freq * simulation.t)

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


# %%
len(sine2[::20])

# %%
sine[::6400]

# %%
