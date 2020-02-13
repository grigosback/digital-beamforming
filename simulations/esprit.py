#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
#%%
from inits.initialization import *

#%%
def doaesprit_estimation(s, a):
    m = s.shape[0]
    # Eigenvalues and eigenvalues of S
    [aval, avec] = np.linalg.eig(s)
    s0 = np.identity(m)
    p = aval.argsort()
    aval = np.abs(aval[p])
    avec = avec[:, p]
    aval_min = aval[0]
    # Get multiplicity 'q' of the minimun eigenvalue
    bins_aval = np.histogram(aval, bins=200)
    for i in range(0, aval.size):
        if bins_aval[0][i] == 0:
            umbral = bins_aval[1][i]
            break
    q = 0

    for i in range(0, m):
        if aval[i] < umbral:
            q += 1
    d = m - q

    # Subspace noise matrix
    us = np.asmatrix(avec[:, q:])
    return p_mu


#%%
s = doamusic_samples(txs, rx, simulation)
m = s.shape[0]
# Eigenvalues and eigenvalues of S
[aval, avec] = np.linalg.eig(s)
s0 = np.identity(m)
p = aval.argsort()
aval = np.abs(aval[p])
avec = avec[:, p]
aval_min = aval[0]
# Get multiplicity 'q' of the minimun eigenvalue
bins_aval = np.histogram(aval, bins=200)
for i in range(0, aval.size):
    if bins_aval[0][i] == 0:
        umbral = bins_aval[1][i]
        break
q = 0

for i in range(0, m):
    if aval[i] < umbral:
        q += 1
d = m - q

# Subspace noise matrix
us = avec[:, q:]

# %%
u1 = us[0 : m - 1, :]
u2 = us[1:m, :]

# %%
[ll, ss, uu] = np.linalg.svd(np.append(u1, u2, axis=1))
# %%
uu12 = uu[0:d, d : 2 * d]
uu22 = uu[d : 2 * d, d : 2 * d]
# %%
psi = -uu12 @ np.linalg.inv(uu22)

# %%
[phi_aval, phi_avec] = np.linalg.eig(psi)

# %%
u2 @ psi

# %%
u1

#%%
lambda_c = c / rx.fc
k = 2 * np.pi / (lambda_c)
#%%
np.arccos(1 / (k * rx.d) * np.angle(phi_aval))

# %%
