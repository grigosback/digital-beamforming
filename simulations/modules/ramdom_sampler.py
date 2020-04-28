#%%
import numpy as np


def random_sampler(x, n, m=4):
    if len(x.shape) != 1:
        ns = x.shape[1]
        idx = np.random.choice(ns, n, replace=False)
        idx.sort()
        x_rs = x[:, idx]
    else:
        ns = len(x)
        idx = np.random.choice(ns, n, replace=False)
        idx.sort()
        if (idx[-1] + m) >= ns:
            idx[-1] = ns - m - 1
        x_rs = np.empty((m, n), dtype=complex)
        for i in range(n):
            for j in range(m):
                x_rs[j, i] = x[idx[i] + j]
    return x_rs, idx
