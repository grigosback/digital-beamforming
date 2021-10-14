#%%
from matplotlib import pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")

us = 1e-6
ms = 1e-3
kHz = 1e3
MHz = 1e6

#%%
n_rs = 25
T = 200 * us
fs = 1 * MHz
N = int(T * fs)
f_real = 100 * fs
t = np.linspace(0, T, N)
t_real = np.linspace(0, T, int(T * f_real))
amp_a = 10
freq_a = 5 * kHz
sine_a_samples = amp_a * np.cos(2 * np.pi * freq_a * (t))
sine_a_real = amp_a * np.cos(2 * np.pi * freq_a * (t_real))
amp_b = 10
freq_b = 7 * kHz
sine_b_samples = amp_b * np.cos(2 * np.pi * freq_b * (t))
sine_b_real = amp_b * np.cos(2 * np.pi * freq_b * (t_real))

#%%
plt.figure(figsize=(10, 5), dpi=100)
# plt.plot(t_real / us, (sine_a_real+sine_b_real), "r")
plt.stem(t / us, (sine_a_samples + sine_b_samples), "r", markerfmt="ro")
plt.plot(t_real / us, sine_a_real, "k")
plt.plot(t_real / us, sine_b_real, "b")
plt.xlabel(r"Tiempo [$\mu$s]")
plt.legend([r"$s_A(t)$", r"$s_B(t)$", r"$s_A[n]+s_B[n]$"])
plt.yticks([])
plt.savefig("sa_sb.png", dpi=300, bbox_inches="tight")
plt.show()
#%%
plt.figure(figsize=(10, 5), dpi=100)
plt.stem(
    t[0:n_rs] / us,
    (sine_a_samples[0:n_rs] + sine_b_samples[0:n_rs]),
    "r",
    markerfmt="ro",
)
plt.plot(t_real[0 : n_rs * 100] / us, sine_a_real[0 : n_rs * 100], "k")
plt.plot(t_real[0 : n_rs * 100] / us, sine_b_real[0 : n_rs * 100], "b")
plt.xlabel(r"Tiempo [$\mu$s]")
plt.legend([r"$s_A(t)$", r"$s_B(t)$", r"$s_A[n]+s_B[n]$"])
plt.yticks([])
plt.savefig("sa_sb_15.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
idx = np.random.choice(t.size, n_rs, replace=False)
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(t_real / us, (sine_a_real + sine_b_real), "r", linestyle="--")
plt.stem(t[idx] / us, (sine_a_samples[idx] + sine_b_samples[idx]), "r", markerfmt="ro")
plt.plot(t_real / us, sine_a_real, "k")
plt.plot(t_real / us, sine_b_real, "b")
plt.xlabel(r"Tiempo [$\mu$s]")
plt.legend([r"$s_A(t)+s_B(t)$", r"$s_A(t)$", r"$s_B(t)$"])
plt.yticks([])
plt.savefig("rs_random_sampling_sine.png", dpi=300, bbox_inches="tight")
plt.show()
# %%

t = np.linspace(0, 10 * 2 * np.pi, 1000)
x1 = np.cos(2 * np.pi * t)
x2 = np.cos(2 * np.pi * t * 1.1)
plt.figure()
plt.plot(t, x1, t, x2)
plt.plot(t, x1 * x2)
plt.show()

Rxy = lambda x, y, N, mask: np.sum(x[mask][:N] * y[mask][:N]) / N
#%%
plt.figure(figsize=(10, 5), dpi=100)
for p in np.linspace(0.2, 1, 4):
    mask = np.random.rand(len(t)) >= 1 - p
    R = [Rxy(x1, x2, N, mask) for N in range(len(mask))]
    plt.plot(t, R, label=r"$p= {p:.1f}$".format(p=p))
plt.legend()
plt.grid()
plt.xlabel(r"$T$")
plt.ylabel(r"$\mathbf{R}_{xy}$")
plt.xticks([])
plt.savefig("rs_rxy.png", dpi=300, bbox_inches="tight")

plt.show()
# %%
