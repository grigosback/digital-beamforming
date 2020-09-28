#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")
#%%
from inits.initialization import *
from math import floor

#%%
def doaesprit_estimation(x, rx, k):
    m = x.shape[0]

    # Eigenvalues and eigenvalues of S
    [aval, avec] = np.linalg.eig(s)
    aval = np.abs(aval)
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

    # Signal subspace matrix
    es = avec[:, q:]
    # if np.imag(es[-1]) == 0:
    # es = np.flipud(es)"""
    if rx.mx == 1 or rx.my == 1:
        # Decompose Ex and Ey
        ex = es[0 : m - 1, :]
        ey = es[1:m, :]

        # Create Exy = [Ex|Ey]
        exy = np.append(ex, ey, axis=1)

        # Find E with the eigendecomposition of Exy*@Exy
        [e_aval, e] = np.linalg.eig(exy.H @ exy)

        # Find E12 and E22
        e12 = e[0:d, d : 2 * d]
        e22 = e[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi = -e12 @ np.linalg.inv(e22)
        [phi, psi_avec] = np.linalg.eig(psi)

        # DOA calculation
        # print(d)
        theta = np.zeros(d)
        for i in range(d):
            theta[i] = np.arcsin(np.angle(phi) / (k[i] * rx.d))
        # print(es)
        # print(np.angle(es))
        return theta

    else:
        # Signal subspace matrix
        print(es)
        es = es.reshape(rx.mx, rx.my)

        # Decompose Ex and Ey
        ex = es[0 : rx.mx - 1, :]
        ex = ex.reshape((rx.mx - 1) * rx.my, 1)
        ey = es[1 : rx.mx, :]
        ey = ey.reshape((rx.mx - 1) * rx.my, 1)

        # Create Exy = [Ex|Ey]
        exy_x = np.append(ex, ey, axis=1)

        # Find E with the eigendecomposition of Exy*@Exy
        [e_aval, e_x] = np.linalg.eig(exy_x.H @ exy_x)

        # Find E12 and E22
        e12 = e_x[0:d, d : 2 * d]
        e22 = e_x[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi_x = -e12 @ np.linalg.inv(e22)
        [phi_x, psi_avec] = np.linalg.eig(psi_x)

        # Decompose Ex and Ey
        es = es.T
        ex = es[0 : rx.my - 1, :]
        ex = ex.reshape((rx.my - 1) * rx.mx, 1)
        ey = es[1 : rx.my, :]
        ey = ey.reshape((rx.my - 1) * rx.mx, 1)

        #%%
        # Create Exy = [Ex|Ey]
        exy_y = np.append(ex, ey, axis=1)

        # Find E with the eigendecomposition of Exy*@Exy
        [e_aval, e_y] = np.linalg.eig(exy_y.H @ exy_y)

        # Find E12 and E22
        e12 = e_y[0:d, d : 2 * d]
        e22 = e_y[d : 2 * d, d : 2 * d]

        # Calculate the engenvalues of Psi
        psi_y = -e12 @ np.linalg.inv(e22)
        [phi_y, psi_avec] = np.linalg.eig(psi_y)

        # DOA calculation
        az = np.zeros(d)
        el = np.zeros(d)
        for i in range(d):
            az[i] = np.arctan(np.angle(phi_y) / np.angle(phi_x))
            el[i] = np.arccos(
                np.sqrt((np.angle(phi_x) ** 2 + np.angle(phi_y) ** 2) / (np.pi ** 2))
            )
        print(exy_x)
        print(exy_y)
        return [az, el]


# %%
for i in range(10):
    k = [2 * np.pi * txs[0].fc / c]

    # Transmitter definition
    x_start = np.array([-15, 0, 15])  # Start coordinate for the transmitter in m
    v = np.array([1, 0, 0])  # Transmitter velocity in m/s
    t = 0
    fc = 436 * MHz
    amp = 10
    freq = 400
    s = Sine_Wave(amp, freq)
    tx0 = Transmitter(x_start, v, t, fc, s)
    txs = []
    txs.append(tx0)

    # Phased array definition
    mx = 16  # Number of sensors in direction X
    my = 1  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].fc, origin)

    # Simulation parameters
    n = 1000  # Snapshots number
    d = len(txs)  # Number of signals/transmitters
    fs = 64 * MHz  # Sampling frequency
    fc = rx.fc
    sampling_time = 5 * ms  # Sampling time
    snr = 10  # Signal-to-noise ratio in dB
    simulation = Simulation(n, d, fs, fc, sampling_time, snr)

    [s, x] = doamusic_samples(txs, rx, simulation)

    [u, s, v] = np.linalg.svd(x)

    us = u[:, 0]
    u1 = us[0 : rx.mx - 1].reshape(rx.mx - 1, 1)
    u2 = us[1 : rx.mx].reshape(rx.mx - 1, 1)
    [uu, ss, vv] = np.linalg.svd(np.append(u1, u2, axis=1))
    vv = vv.T
    vv12 = vv[0:d, d : 2 * d]
    vv22 = vv[d : 2 * d, d : 2 * d]

    # Calculate the engenvalues of Psi
    psi = -vv12 @ np.linalg.inv(vv22)
    [phi, psi_avec] = np.linalg.eig(psi)

    theta = np.zeros(d)
    for i in range(d):
        theta[i] = np.arcsin(np.angle(phi) / (k[i] * rx.d))

    print(np.degrees(theta))
#%%
uu22
#%%
for j in range(10):
    k = [2 * np.pi * txs[0].fc / c]

    # Transmitter definition
    x_start = np.array([15, 0, 15])  # Start coordinate for the transmitter in m
    v = np.array([1, 0, 0])  # Transmitter velocity in m/s
    t = 0
    fc = 436 * MHz
    amp = 10
    freq = 4000
    s = Sine_Wave(amp, freq)
    tx0 = Transmitter(x_start, v, t, fc, s)
    txs = []
    txs.append(tx0)

    # Phased array definition
    mx = 9  # Number of sensors in direction X
    my = 1  # Number of sensors in direction Y
    origin = np.array([0, 0, 0])  # Axis origin
    rx = PhasedArray(mx, my, txs[0].fc, origin)

    # Simulation parameters
    n = 1000  # Snapshots number
    d = len(txs)  # Number of signals/transmitters
    fs = 64 * MHz  # Sampling frequency
    fc = rx.fc
    sampling_time = 5 * ms  # Sampling time
    snr = 10  # Signal-to-noise ratio in dB
    simulation = Simulation(n, d, fs, fc, sampling_time, snr)

    [s, x] = doamusic_samples(txs, rx, simulation)

    print(np.degrees(doaesprit_estimation(s, rx, k)))


# %%
90 - np.degrees(txs[0].doa.el)

#%%
k = [2 * np.pi * txs[0].fc / c]
m = s.shape[0]
# Eigenvalues and eigenvalues of S
[aval, avec] = np.linalg.eig(s)
aval = np.abs(aval)
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

# Signal subspace matrix
es = avec[:, q:]

# np.random.shuffle(es)
# es = np.flipud(es)
# idx = np.arange(4)
# np.random.shuffle(idx)
# es = np.flipud(es_wrong)
print(np.degrees(np.angle(es)))
# Decompose Ex and Ey
ex = es[0 : m - 1, :]
ey = es[1:m, :]

# Create Exy = [Ex|Ey]
exy = np.append(ex, ey, axis=1)

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e] = np.linalg.eig(exy.H @ exy)

# Find E12 and E22
e12 = e[0:d, d : 2 * d]
e22 = e[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi = -e12 @ np.linalg.inv(e22)
[phi, psi_avec] = np.linalg.eig(psi)

# DOA calculation
theta = np.zeros(d)
for i in range(d):
    theta[i] = np.arcsin(np.angle(phi) / (k[i] * rx.d))
np.degrees(theta)

#%%
es
#%%
es_new = np.zeros(4, dtype=complex)
#%%
es_new[0] = es[2]
es_new[1] = es[1]
es_new[2] = es[0]
es_new[3] = es[3]
#%%
np.degrees(np.angle(es))
#%%
es_ok = es
#%%
es_wrong = es
#%%
es_wrong[np.random.randint(4)]
#%%
print(np.random.shuffle(np.arange(4)))
#%%
arr = np.arange(4)
np.random.shuffle(arr)

#%%
np.abs(es_wrong[idx])
#%%
np.degrees(np.angle(es_ok))
#%%
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

# Signal subspace matrix
es = avec[:, q:]

# Decompose Ex and Ey
idx_x = (
    np.arange(rx.m)
    .reshape(rx.mx, rx.my)[0 : rx.mx - 1, 0 : rx.my - 1]
    .reshape((rx.mx - 1) * (rx.my - 1))
)
idx_y = np.arange(rx.m).reshape(rx.mx, rx.my)[1 : rx.mx, :].reshape((rx.mx - 1) * rx.my)

ex = es[idx_x]
ey = es[idx_y]

# Create Exy = [Ex|Ey]
exy = np.append(ex, ey, axis=1)

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e] = np.linalg.eig(exy.H @ exy)

# Find E12 and E22
e12 = e[0:d, d : 2 * d]
e22 = e[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi = -e12 @ np.linalg.inv(e22)
[phi_x, psi_avec] = np.linalg.eig(psi)


#%%
#%%

idx_x = (
    np.arange(rx.m).reshape(rx.mx, rx.my)[:, 0 : rx.my - 1].reshape(rx.mx * (rx.my - 1))
)
idx_y = np.arange(rx.m).reshape(rx.mx, rx.my)[:, 1 : rx.my].reshape(rx.mx * (rx.my - 1))

ex = es[idx_x]
ey = es[idx_y]

# Create Exy = [Ex|Ey]
exy = np.append(ex, ey, axis=1)

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e] = np.linalg.eig(exy.H @ exy)


# Find E12 and E22
e12 = e[0:d, d : 2 * d]
e22 = e[d : 2 * d, d : 2 * d]


# Calculate the engenvalues of Psi
psi = -e12 @ np.linalg.inv(e22)
[phi_y, psi_avec] = np.linalg.eig(psi)

#%%
# Calculate de DOA
np.degrees(np.arcsin(np.angle(phi_x) / (k * rx.d)))

# %%
np.degrees(np.arctan(np.angle(phi_y) / np.angle(phi_x)))

# %%
k = 2 * np.pi * txs[0].fc / c
np.degrees(
    np.arcsin(
        np.sqrt((np.angle(phi_x) ** 2 + np.angle(phi_y) ** 2) / ((k * rx.d) ** 2))
    )
)

# %%
np.sqrt((np.angle(phi_x) ** 2 + np.angle(phi_y) ** 2) / ((k * rx.d) ** 2))

# %%
(k * rx.d) ** 2

# %%
(np.angle(phi_x) ** 2 + np.angle(phi_y) ** 2)


# %%
k = [2 * np.pi * txs[0].fc / c]
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

# Signal subspace matrix
es = avec[:, q:]

# Decompose Ex and Ey

p = rx.mx
q = rx.my

j1 = np.append(np.identity((p - 1) * q), np.zeros(((p - 1) * q, q)), axis=1)
j2 = np.append(np.zeros(((p - 1) * q, q)), np.identity((p - 1) * q), axis=1)

es1 = j1 @ es
es2 = j2 @ es

# Create Exy = [Ex|Ey]
exy_1 = np.append(es1, es2, axis=1)

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e_1] = np.linalg.eig(exy_1.H @ exy_1)

# Find E12 and E22
e12_1 = e_1[0:d, d : 2 * d]
e22_1 = e_1[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi_1 = -e12_1 @ np.linalg.inv(e22_1)
# [phi_x, psi_avec] = np.linalg.eig(psi)


#%%
# Decompose Ex and Ey
j3_p = np.append(np.identity(q - 1), np.zeros((q - 1, 1)), axis=1)
j3 = np.kron(np.identity(p), j3_p)

j4_p = np.append(np.zeros((q - 1, 1)), np.identity(q - 1), axis=1)
j4 = np.kron(np.identity(p), j4_p)

es3 = j3 @ es
es4 = j4 @ es

# Create Exy = [Ex|Ey]
exy_2 = np.append(es3, es4, axis=1)

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e_2] = np.linalg.eig(exy_2.H @ exy_2)

# Find E12 and E22
e12_2 = e_2[0:d, d : 2 * d]
e22_2 = e_2[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi_2 = -e12_2 @ np.linalg.inv(e22_2)
# [phi_y, psi_avec] = np.linalg.eig(psi)


#%%
psi = psi_1 + 1j * psi_2

# %%
[psi_aval, psi_avec] = np.linalg.eig(psi)

# %%
psi_aval

# %%
u = 2 * np.arctan(np.real(psi_aval))
v = 2 * np.arctan(np.imag(psi_aval))


# %%
np.degrees(np.arccos(np.sqrt(u ** 2 + v ** 2) / (k[0] * rx.d)))


# %%
np.degrees(np.arctan(v / u))

#%%
##############################################################################
s = doamusic_samples(txs, rx, simulation)
k = 2 * np.pi * txs[0].fc / c
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

# Signal subspace matrix
es = avec[:, q:]

# Decompose Ex and Ey

J = np.zeros(((rx.mx - 1) * (rx.my - 1), rx.m, 3))
d_j = np.array([0, 1, rx.mx])
for i in range((rx.mx - 1) * (rx.my - 1)):
    for j in range(rx.m):
        for k in range(3):
            if j == i + floor((i - 1) / (rx.mx - 1)) + d_j[k]:
                J[i, j, k] = 1
            else:
                J[i, j, k] = 0


es1 = J[:, :, 0] @ es
es2 = J[:, :, 1] @ es
es3 = J[:, :, 2] @ es

# Create Exy = [Ex|Ey]
exy = np.append(es1, es2, axis=1)

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e] = np.linalg.eig(exy.H @ exy)

# Find E12 and E22
e12 = e[0:d, d : 2 * d]
e22 = e[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi_x = -e12 @ np.linalg.inv(e22)
[phi_x, psi_avec] = np.linalg.eig(psi_x)


# %%
# Create Exy = [Ex|Ey]
exy = np.append(es1, es3, axis=1)

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e] = np.linalg.eig(exy.H @ exy)

# Find E12 and E22
e12 = e[0:d, d : 2 * d]
e22 = e[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi_y = -e12 @ np.linalg.inv(e22)
[phi_y, psi_avec] = np.linalg.eig(psi_y)


# %%
psi = psi_x + 1j * psi_y

# %%
[psi_aval, psi_avec] = np.linalg.eig(psi)

# %%
psi_aval

# %%
u = 2 * np.arctan(np.real(psi_aval))
v = 2 * np.arctan(np.imag(psi_aval))


# %%
np.degrees(np.arccos(np.sqrt(u ** 2 + v ** 2) / (k * rx.d)))

# %%
np.degrees(np.arctan(v / u))

# %%
exy.H @ exy

# %%
##############################################################################
d = len(txs)
c = 3e8
lambda_c = np.empty(d)
for i in range(d):
    lambda_c[i] = c / txs[i].fc
K = 2 * np.pi / (lambda_c)
beta = np.empty((rx.mx, 1), dtype=complex)
gamma = np.empty((rx.my, 1), dtype=complex)
a = np.empty((rx.m, d), dtype="complex")

for k in range(d):
    [beta_k, gamma_k] = [
        np.e ** (1j * K[k] * rx.d * np.cos(txs[k].doa.el) * np.cos(txs[k].doa.az)),
        np.e ** (1j * K[k] * rx.d * np.cos(txs[k].doa.el) * np.sin(txs[k].doa.az)),
    ]
    for i in range(rx.mx):
        beta[i] = beta_k ** (-i)

    for j in range(rx.my):
        gamma[j] = gamma_k ** (-j)

    a[:, k] = np.kron(beta, gamma).ravel()

A = a.reshape(rx.mx, rx.my)
# %%
a_mx = np.zeros((rx.mx, 1), dtype=complex)
a_my = np.zeros((rx.my, 1), dtype=complex)

for i in range(rx.mx):
    a_mx[i] = np.e ** (
        -1j * i * K * rx.d * np.cos(txs[k].doa.el) * np.cos(txs[k].doa.az)
    )

for i in range(rx.my):
    a_my[i] = np.e ** (
        -1j * i * K * rx.d * np.cos(txs[k].doa.el) * np.sin(txs[k].doa.az)
    )


A2 = a_mx @ a_my.T

# %%
A - A2

# %%
n = rx.mx
pi_n = np.flipud(np.identity(n))

#%%
pi_n @ a_my

# %%
a_mx

# %%
a_my

# %%
def q_gen(n):
    if n % 2 == 0:
        k = int(n / 2)
        pi_k = np.flipud(np.identity(k))
        q_n = np.append(np.identity(k), 1j * np.identity(k), axis=1)
        q_n = (1 / np.sqrt(2)) * np.append(
            q_n, np.append(pi_k, -1j * pi_k, axis=1), axis=0
        )
    else:
        k = int(n / 2)
        q_n = np.zeros((n, n), dtype=complex)
        q_n[0:k, 0:k] = np.identity(k)
        q_n[0:k, k + 1 : n] = 1j * np.identity(k)
        q_n[k, k] = np.sqrt(2)
        q_n[k + 1 : n, 0:k] = np.flipud(np.identity(k))
        q_n[k + 1 : n, k + 1 : n] = -1j * np.flipud(np.identity(k))
        q_n = 1 / np.sqrt(2) * q_n

    return np.asmatrix(q_n)


# %%
q_mx = np.asmatrix(q_gen(rx.mx))
q_my = np.asmatrix(q_gen(rx.my))

# %%
y = np.kron(q_my.H, q_mx.H) @ x

#%%

u, s, vh = np.linalg.svd(np.append(np.real(y), np.imag(y), axis=1), full_matrices=True)
es = u[:, 0]
#%%
s
# %%
j1 = np.identity(rx.mx)[0 : rx.mx - 1, :]
j2 = np.identity(rx.mx)[1 : rx.mx, :]
# %%
q_mx_1 = q_gen(rx.mx - 1)
q_mx = q_gen(rx.mx)
k1 = np.real(q_mx_1.H @ j2 @ q_mx)
k2 = np.imag(q_mx_1.H @ j2 @ q_mx)

q_my_1 = q_gen(rx.my - 1)
q_my = q_gen(rx.my)
k3 = np.real(q_my_1.H @ j2 @ q_my)
k4 = np.imag(q_my_1.H @ j2 @ q_my)

ku1 = np.kron(np.identity(rx.my), k1)
ku2 = np.kron(np.identity(rx.my), k2)

kv1 = np.kron(k3, np.identity(rx.mx))
kv2 = np.kron(k4, np.identity(rx.mx))
# %%
(ku1 @ es) / (ku2 @ es)

# %%
ku2 @ es * -0.5037130822832463

# %%
-0.13581665 / 2.69630976e-01

# %%
############################################################
[s, x] = doamusic_samples(txs, rx, simulation)
k = [2 * np.pi * txs[0].fc / c]
m = s.shape[0]
#%%
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

# Signal subspace matrix
# avec_angle = np.angle(avec[:, q:])
# p = avec_angle.ravel().argsort()
# es = np.sort(avec[:, q:])
# es = np.flipud(es[p])
es = avec[:, q:]

#%%
es = es.reshape(rx.mx, rx.my)
#%%
# Decompose Ex and Ey
ex = es[0 : rx.mx - 1, :]
ex = ex.reshape((rx.mx - 1) * rx.my, 1)
ey = es[1 : rx.mx, :]
ey = ey.reshape((rx.mx - 1) * rx.my, 1)

#%%
# Create Exy = [Ex|Ey]
exy = np.append(ex, ey, axis=1)

#%%
exy

#%%

# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e] = np.linalg.eig(exy.H @ exy)

# Find E12 and E22
e12 = e[0:d, d : 2 * d]
e22 = e[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi_1 = -e12 @ np.linalg.inv(e22)
[phi_1, psi_avec] = np.linalg.eig(psi_1)


#%%
es = es.T
#%%
# Decompose Ex and Ey
ex = es[0 : rx.my - 1, :]
ex = ex.reshape((rx.my - 1) * rx.mx, 1)
ey = es[1 : rx.my, :]
ey = ey.reshape((rx.my - 1) * rx.mx, 1)

#%%
# Create Exy = [Ex|Ey]
exy = np.append(ex, ey, axis=1)

#%%
exy
#%%
es.reshape(16, 1)
#%%
# Find E with the eigendecomposition of Exy*@Exy
[e_aval, e] = np.linalg.eig(exy.H @ exy)

# Find E12 and E22
e12 = e[0:d, d : 2 * d]
e22 = e[d : 2 * d, d : 2 * d]

# Calculate the engenvalues of Psi
psi_2 = -e12 @ np.linalg.inv(e22)
[phi_2, psi_avec] = np.linalg.eig(psi_2)

#%%
np.degrees(np.arctan(np.angle(phi_2) / np.angle(phi_1)))

# %%
np.degrees(
    np.arccos(np.sqrt((np.angle(phi_1) ** 2 + np.angle(phi_2) ** 2) / np.pi ** 2))
)

# %%
