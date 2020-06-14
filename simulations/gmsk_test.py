#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
sys.path.insert(0, "${workspaceRoot}/modules/")

from modules.gmsk_modem import *

# %%
x = np.array([1, 1, 0, 1, 0, 0, 0])
# x = np.array([1, 0, 1, 0, 1, 0, 1])
# x = np.random.randint(2, size=100)
# x = np.arange(10)%2
Rb = 4800
fs = 100 * Rb
# nc = 3
nc = 4
h = 1 / 2
fc = nc * Rb / 4
f1 = fc + h * Rb / 2
f2 = fc - h * Rb / 2

s, t = gmsk_modulator(x, Rb, nc, h, fs)
s_filtered, _ = gmsk_modulator(x, Rb, nc, h, fs, 0.5, 0)

plt.figure()
plt.plot(t, s)
plt.plot(t, s_filtered)
plt.xticks(np.arange(len(x)) / Rb)
plt.yticks([-1, 0, 1])
plt.grid()
plt.show()

# %%
# x = np.array([1, 1, 0, 1, 0, 0, 0])
x = np.random.randint(2, size=10000)
# x = np.arange(10)%2

Rb = 4800
fs = 10 * Rb
# nc = 3
nc = 4
h = 1 / 2

s, t = gmsk_modulator(x, Rb, nc, h, fs)
s_filtered, _ = gmsk_modulator(x, Rb, nc, h, fs, 0.5, 0)

x_det = gmsk_detector(s_filtered, fs, Rb, nc)

n_errors = np.cumsum(np.abs(x - x_det))[-1]
print(n_errors)


# %%
