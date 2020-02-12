#%%
from samples_generator import *

#%%
import matplotlib.pyplot as plt
from IPython import get_ipython

get_ipython().run_line_magic("matplotlib", "qt")
#%%
def doamusic_estimation(s, a):
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
    en = np.asmatrix(avec[:, 0:q])
    p_mu = np.empty((a.shape[1], a.shape[2]), dtype=complex)
    for i in range(p_mu.shape[0]):
        for j in range(p_mu.shape[1]):
            a_matrix = np.asmatrix(a[:, i, j])
            a_matrix = a_matrix.T
            p_mu[i, j] = 1 / (a_matrix.H @ en @ en.H @ a_matrix)
    return p_mu


# %% Test
el = np.linspace(0, np.pi / 2, num=100)
az = np.linspace(-np.pi, np.pi, num=200)
lambda_c = c / rx.fc
k = 2 * np.pi / (lambda_c)
a = np.empty((rx.m, el.size, az.size), dtype=complex)


#%%
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
#%%
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

# %%
print("El0 = " + str(tx0.doa.el * 180 / np.pi))
print("Az0 = " + str(tx0.doa.az * 180 / np.pi))
print("El1 = " + str(tx1.doa.el * 180 / np.pi))
print("Az1 = " + str(tx1.doa.az * 180 / np.pi))
