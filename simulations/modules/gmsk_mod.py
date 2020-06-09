# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

# %%
Hz = 1e3
MHz = 1e6
GHz = 1e9
ms = 1e-3
c = 3e8
km = 1e3

# %%
# bit_stream = np.array([1, 1, 0, 1, 0, 0, 0])
x = np.array([1, 0, 1, 1, 0, 1, 0])
nb = len(x)
Rb = 4800
Tb = 1 / Rb

nc = 3
fc = nc * Rb / 4

h = 1 / 2
# h = 2 / 3
f1 = fc + h * Rb / 2
f2 = fc - h * Rb / 2


fs = 100 * fc

T_max = len(x) / Rb
Ns = int(T_max * fs)
Nb = int(fs / Rb)
t = np.linspace(0, T_max, Ns)

#%%
# %%
# phi1 = np.sqrt(2 / Tb) / 2 * (np.cos(2 * np.pi * f1 * t) + np.cos(2 * np.pi * f2 * t))
# phi2 = np.sqrt(2 / Tb) / 2 * (-np.cos(2 * np.pi * f1 * t) + np.cos(2 * np.pi * f2 * t))

phi_e = np.sqrt(2 / Tb) / 2 * (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t))
phi_o = np.sqrt(2 / Tb) / 2 * (np.sin(2 * np.pi * f1 * t) - np.sin(2 * np.pi * f2 * t))

# %%
plt.figure()
plt.subplot(211)
plt.plot(t, phi_e)
plt.subplot(212)
plt.plot(t, phi_o)
plt.show()


#%%
x_nrz = 2 * (x - 0.5)
x_e = np.zeros(nb)
x_o = np.zeros(nb)

#%%
for i in range(nb):
    x_e[i] = x_nrz[i - (i - 1) % 2]
    x_o[i] = x_nrz[i - i % 2]

#%%
a = np.zeros(Ns)
a_o = np.ones(Ns)
a_e = np.ones(Ns)

for i in range(nb):
    a[i * Nb : (i + 1) * Nb] = x[i]
    a_o[i * Nb : (i + 1) * Nb] = x_o[i]
    a_e[i * Nb : (i + 1) * Nb] = x_e[i]

xticks = Tb * np.arange(nb)
#%%
plt.figure()
plt.xticks(xticks)
plt.subplot(311)
plt.plot(t, a)
plt.grid(axis="x")
plt.subplot(312)
plt.plot(t, a_e)
plt.plot(t, phi_e / max(phi_e))
plt.grid(axis="x")
plt.subplot(313)
plt.plot(t, a_o)
plt.plot(t, phi_o / max(phi_o))
plt.grid(axis="x")
plt.show()

# %%
s_e = a_e * phi_e
s_o = a_o * phi_o
s = s_e + s_o
# %%
plt.figure()
plt.plot(t, s)
plt.xticks(xticks)
plt.grid(axis="x")
plt.show()
