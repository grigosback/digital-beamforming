#%%
import numpy as np
import time
from matplotlib import pyplot as plt
import scipy

from numpy import loadtxt
import matplotlib

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")


def d_estimator(x, y, M):
    d_est = M - scipy.diff(x).argmax() - 1
    y_est = np.zeros(M)
    y_est[0:d_est] = 1

    return y_est


def model_accuracy(y, y_est):
    error = np.mean((y_est != y).astype(int))
    print("Accuracy on full set =  %.2lf" % ((1 - error) * 100))
    return error


#%%
data_full = loadtxt("eigenvalues_4signals.csv", delimiter=",")
X = data_full[:, 0]
Y = data_full[:, 2]

# %%
N = int(data_full.shape[0] / 16)
y_est = np.zeros(data_full.shape[0])
M = 16

for i in range(N):
    print(i)
    x = data_full[M * i : M * (i + 1), 0][::-1]
    y = data_full[M * i : M * (i + 1), 2][::-1]
    y_est[M * i : M * (i + 1)] = d_estimator(x, y, M)

# %%
error = model_accuracy(Y, y_est)

# %%
