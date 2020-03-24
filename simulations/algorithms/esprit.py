#%%
import sys
from inits.initialization import *

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")


#%%
def doaesprit_estimation(x, rx, k=np.pi / rx.d):
    m = x.shape[0]

    # Singular value decomposition of matrix "X"
    [u, s, v] = np.linalg.svd(x)

    # Get multiplicity 'q' of the minimun eigenvalue using histogram method
    aval_min = s[0]
    bins_n = 100
    bins_aval = np.histogram(s, bins=bins_n)
    count = 0
    for i in range(0, bins_n):
        if bins_aval[0][i] == 0 or count < 30:
            if bins_aval[0][i] == 0:
                count += 1
        else:
            umbral = bins_aval[1][i]
            break
    q = 0

    for i in range(0, s.size):
        if s[i] < umbral:
            q += 1

    # Number of signals impinging on the array
    d = s.size - q

    # Signal subspace matrix
    us = u[:, 0:d]

    if rx.mx == 1 or rx.my == 1:
        # 1-D case
        u1 = us[0 : m - 1, :].reshape(m - 1, d)
        u2 = us[1:m, :].reshape(m - 1, d)
        [uu, ss, vv] = np.linalg.svd(np.append(u1, u2, axis=1), full_matrices=False)
        vv = vv.T

        vv12 = vv[0:d, d : 2 * d]
        vv22 = vv[d : 2 * d, d : 2 * d]

        # Calculate the eigenvalues of Psi
        psi = -vv12 @ np.linalg.inv(vv22)
        [phi, psi_avec] = np.linalg.eig(psi)
        # DOA estimation
        theta = np.zeros(d)
        for i in range(d):
            theta[i] = np.arcsin(np.angle(phi[i]) / (k * rx.d))

        return theta

    else:
        # 2-D case
        u1_x = np.zeros(((rx.mx - 1) * rx.my, d), dtype=complex)
        u2_x = np.zeros(((rx.mx - 1) * rx.my, d), dtype=complex)
        u1_y = np.zeros(((rx.my - 1) * rx.mx, d), dtype=complex)
        u2_y = np.zeros(((rx.my - 1) * rx.mx, d), dtype=complex)

        for i in range(d):
            us_aux = us[:, i].reshape(rx.mx, rx.my)
            u1_x[:, i] = us_aux[0 : rx.mx - 1, :].reshape((rx.mx - 1) * rx.my)
            u2_x[:, i] = us_aux[1 : rx.mx, :].reshape((rx.mx - 1) * rx.my)
            u1_y[:, i] = us_aux[:, 0 : rx.my - 1].reshape((rx.my - 1) * rx.mx)
            u2_y[:, i] = us_aux[:, 1 : rx.my].reshape((rx.my - 1) * rx.mx)

        [uu_x, ss_x, vv_x] = np.linalg.svd(
            np.append(u1_x, u2_x, axis=1), full_matrices=False
        )
        vv_x = vv_x.T

        vv12_x = vv_x[0:d, d : 2 * d]
        vv22_x = vv_x[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi_x = -vv12_x @ np.linalg.inv(vv22_x)
        [phi_x, psi_avec] = np.linalg.eig(psi_x)

        [uu_y, ss_y, vv_y] = np.linalg.svd(
            np.append(u1_y, u2_y, axis=1), full_matrices=False
        )
        vv_y = vv_y.T

        vv12_y = vv_y[0:d, d : 2 * d]
        vv22_y = vv_y[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi_y = -vv12_y @ np.linalg.inv(vv22_y)
        [phi_y, psi_avec] = np.linalg.eig(psi_y)

        # DOA estimation
        az = np.arctan2(np.angle(phi_y), np.angle(phi_x))

        el = np.arccos(
            np.sqrt((np.angle(phi_x) ** 2 + np.angle(phi_y) ** 2) / ((k * rx.d) ** 2))
        )

        return [az, el]
