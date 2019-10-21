#%% Librerías utilizadas
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import inv,eig
from numpy import dot
import matplotlib.style as style
from scipy import signal
import pandas as pd
style.use('default')

#%% Funciones
def print_matrix(list_of_list):
    number_width = len(str(max([max(i) for i in list_of_list])))
    cols = max(map(len, list_of_list))
    output = '+'+('-'*(number_width+2)+'+')*cols + '\n'
    for row in list_of_list:
        for column in row:
            output += '|' + ' {:^{width}d} '.format(column, width = number_width)
        output+='|\n+'+('-'*(number_width+2)+'+')*cols + '\n'
    return output

def doamusic_samples(Fc,s_amp,s_freq,t,d,theta,M,D,SNR):
    # Definición de señales y muestras
    # Genero la matriz F de tamaño (D,1,N)
    lambda_c = c / Fc
    K = 2 * np.pi / (lambda_c)
    F = np.zeros((D, 1, N))
    for i in range(0, D):
        F[i,0,:] = s_amp[i] * np.cos(2 * np.pi * s_freq[i] * t)

    # Genero la matriz A de tamaño (M,D) considerando $g(\theta)=1 \quad \forall \  \theta$
    A=np.asmatrix(np.zeros((M,D),dtype='complex'))
    for i in range(0, M):
        for j in range(0, D):
            A[i, j] = np.e ** (-1j * i * K[j] * d * np.cos(theta[j]))

    # Genero el vector W de tamaño (M,1,N) de ruido $W\sim N(0,1)$
    mean_nu = 0
    Ps = 0
    for i in range(0,D):
        Ps = Ps + (s_amp[i]**2)/2
    var_nu = Ps/(10**(SNR/10))
    std_nu = np.sqrt(var_nu)
    W = np.random.normal(mean_nu, std_nu, size=(M,1,N))

    # Genero el vector de muestras $X=A \times F + W$ de tamaño (M,1,N)
    X = np.zeros((M,1,N),dtype=complex)
    X_matrix = np.asmatrix(np.zeros((M,1)),dtype=complex)
    for n in range (0,N):
        F_matrix = np.asmatrix(F[:,:,n])
        W_matrix = np.asmatrix(W[:,:,n])
        X_matrix = A @ F_matrix + W_matrix
        X[:, :, n] = X_matrix
    
    return X

    #%% Calculo el vector de covarianza S
def doamusic_estimation(X, K_est, theta_est):
    M = X.shape[0]
    N = X.shape[2]
    S = np.asmatrix(np.zeros((M,M),dtype=complex))

    for n in range (0,N):
        X_matrix=np.asmatrix(X[:,:,n])
        S = S + (1/N)*(X_matrix @ X_matrix.H)

    # Encuentro autovalores y autovectores S y el autovalor mínimo $\lambda_{min}$ tal que $|S-\lambda_{min}\cdot S_0|=0$
    [aval, avec] = eig(S)
    S0 = np.identity(M)
    p = aval.argsort()
    aval=np.abs(aval[p])
    avec=avec[:,p]
    aval_min = aval[0]

    # Encuentro la multiplicidad Q de $\lambda_min$ y el número estimado de señales $\hat{D}$
    Q = 0
    umbral = 0.5 * aval_min
    for i in range (0,M):
        if aval[i]-aval_min<umbral:
            Q += 1
    D_est = M - Q

    # Formo la matriz de subespacio de ruido $E_N$
    EN = np.asmatrix(avec[:,0:Q])

    #%% Evalúo la función $P_{MU}$ para distintas frecuencias de portadora y distintos ángulos de arribo
    a = np.asmatrix(np.zeros((M, 1), dtype=complex))

    P_MU = np.asmatrix(np.zeros((theta_est.size, K_est.size), dtype=complex))
    if K_est.size == 1:
        for j in range(0, theta_est.size):
            for k in range(0,M):
                a[k] = np.e ** (-1j * k * K_est * d * np.cos(theta_est[j]))
                P_MU[j] = 1 / (a.H @ EN @ EN.H @ a)
    else:
        for i in range (0, K_est.size):
            for j in range(0, theta_est.size):
                for k in range(0,M):
                    a[k] = np.e ** (-1j * k * K_est[i] * d * np.cos(theta_est[j]))
                    P_MU[j, i] = 1 / (a.H @ EN @ EN.H @ a)
                
    return [P_MU, D_est]

#%% Definición de constantes y unidades
kHz = 10 ** 3
MHz = 10 ** 6
GHz = 10 ** 9
ms = 10 ** -3
c = 3 * 10 ** 8

#%% Definición de variables
M = 8  # Número de sensores
D = 3  # Número de señales
fs = 64 * MHz
N = 1000 # Número de snapshots
T = 2 * ms # Tiempo de toma de muestras

theta_deg = np.array([30,90,120])  #DOA en grados
theta = theta_deg * np.pi / 180           #DOA en radianes

# Defición de señal y array de sensores
Fc = np.array([1.5* GHz, 1.5* GHz, 1.5 * GHz]) # Frecuencia de portadora de la señal transmitida 1
lambda_c = c / Fc
d = lambda_c[0] / 2  #Separación entre sensores

t = np.random.randint(0, int(T * fs), size=N) * 1 / fs  # Vector de tiempos de muestreo (tomas de snapshots)
s_amp = np.array([10, 20, 30])
s_freq = np.array([440, 3500, 40000])

SNR = 7
#%%
X = doamusic_samples(Fc, s_amp, s_freq, t, d, theta, M, D, SNR)

#%%
#fc_est = np.linspace(1 * GHz, 2 * GHz,num=20)
#fc_est = np.array([1.5 *GHz])
fc_est = Fc[0]
K_est = 2 * np.pi * fc_est/c
theta_est = np.linspace(0, np.pi ,num=1000)
[P_MU, D_est] = doamusic_estimation(X, K_est, theta_est)

#%%
plt.figure()
plt.plot(theta_est * 180 / np.pi, np.abs(np.array(P_MU)))
plt.yscale('log')
plt.show()


#%%
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(K_est*c/(2*np.pi), theta_est*180/np.pi)
ax.plot_surface(X, Y, np.abs(P_MU), cmap='viridis')
ax.set_xlabel(r'$f_{est}$')
ax.set_ylabel(r'$\theta_{est}$')
ax.set_zlabel(r'$P_{MU}$')
plt.show()