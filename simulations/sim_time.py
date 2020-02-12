#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")

#%%
from inits.initialization import *

#%%
from algorithms.music import doamusic_estimation
from matplotlib import pyplot as plt
from IPython import get_ipython

get_ipython().run_line_magic("matplotlib", "qt")


# %% Test
s = doamusic_samples(txs, rx, simulation)
el = np.linspace(0, np.pi / 2, num=100)
az = np.linspace(-np.pi, np.pi, num=200)
lambda_c = c / rx.fc
k = 2 * np.pi / (lambda_c)
a = np.empty((rx.m, el.size, az.size), dtype=complex)

for ax in range(el.size):
    for ay in range(az.size):
        for i in range(rx.mx):
            for j in range(0, rx.my):
                a[rx.mx * j + i, ax, ay] = np.e ** (
                    -1j
                    * (
                        i * k * rx.d * np.cos(el[ax]) * np.cos(az[ay])
                        + j * k * rx.d * np.cos(el[ax]) * np.sin(az[ay])
                    )
                )

#%% MUSIC test
p_mu = doamusic_estimation(s, a)


# %%
y = el * 180 / np.pi
x = az * 180 / np.pi
plt.figure()
plt.imshow(
    np.log10(abs(p_mu)),
    extent=(x.min(), x.max(), y.max(), y.min()),
    cmap="jet",
    aspect="auto",
)
plt.ylabel(r"Elevation")
plt.xlabel(r"Azimuth")
plt.show()

print("El0 = " + str(tx0.doa.el * 180 / np.pi))
print("Az0 = " + str(tx0.doa.az * 180 / np.pi))
print("El1 = " + str(tx1.doa.el * 180 / np.pi))
print("Az1 = " + str(tx1.doa.az * 180 / np.pi))


# %%
