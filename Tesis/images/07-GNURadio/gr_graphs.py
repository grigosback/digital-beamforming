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
amp_b = 3
freq_b = 7 * kHz
sine_b_samples = amp_b * np.cos(2 * np.pi * freq_b * (t))
sine_b_real = amp_b * np.cos(2 * np.pi * freq_b * (t_real))
amp_c = 7
freq_c = 16 * kHz
sine_c_samples = amp_c * np.cos(2 * np.pi * freq_c * (t))
sine_c_real = amp_c * np.cos(2 * np.pi * freq_c * (t_real))
amp_d = 3
freq_d = 9 * kHz
sine_d_samples = amp_d * np.cos(2 * np.pi * freq_d * (t))
sine_d_real = amp_d * np.cos(2 * np.pi * freq_d * (t_real))

signal_real = sine_a_real + sine_b_real + sine_c_real + sine_d_real
signal_samples = sine_a_samples + sine_b_samples + sine_c_samples + sine_d_samples

#%%
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(t_real / us, signal_real)
plt.yticks([])
plt.xticks([])
plt.savefig("gr_analog.svg", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 5), dpi=100)
plt.stem(t[::10] / us, signal_samples[::10])
plt.yticks([])
plt.xticks([])
plt.savefig("gr_digital.svg", dpi=300, bbox_inches="tight")
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
# plt.savefig("sa_sb_15.png", dpi=300, bbox_inches="tight")
plt.show()
# %%
