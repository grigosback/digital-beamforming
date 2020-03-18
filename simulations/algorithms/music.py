# As seen in "Multiple emitter location and signal parameter estimation"
#%%
import numpy as np

#%%
def doamusic_estimation(s, a):
    m = s.shape[0]
    # Eigenvalues and eigenvalues of S
    [aval, avec] = np.linalg.eig(s)
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

    # Noise subspace matrix
    en = np.asmatrix(avec[:, 0:q])
    if len(a.shape) == 2:
        p_mu = np.empty((a.shape[1]), dtype=complex)
        for i in range(p_mu.size):
            a_matrix = np.asmatrix(a[:, i])
            a_matrix = a_matrix.T
            p_mu[i] = 1 / (a_matrix.H @ en @ en.H @ a_matrix)
    else:
        p_mu = np.empty((a.shape[1], a.shape[2]), dtype=complex)
        for i in range(p_mu.shape[0]):
            for j in range(p_mu.shape[1]):
                a_matrix = np.asmatrix(a[:, i, j])
                a_matrix = a_matrix.T
                p_mu[i, j] = 1 / (a_matrix.H @ en @ en.H @ a_matrix)
    return p_mu
