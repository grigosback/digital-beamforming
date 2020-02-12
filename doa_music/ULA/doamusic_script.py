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

#%% Definición de funciones
def doamusic_samples(Fc,s_amp,s_freq,t,t0,d,theta,M,D,SNR):
    # Definición de señales y muestras
    # Genero la matriz F de tamaño (D,N)
    lambda_c = c / Fc
    K = 2 * np.pi / (lambda_c)
    F = np.asmatrix(np.empty((D, N)))
    for i in range(0, D):
        F[i,:] = s_amp[i] * np.cos(2 * np.pi * s_freq[i] * (t+t0))

    # Genero la matriz A de tamaño (M,D) considerando $g(\theta)=1 \quad \forall \  \theta$
    A = np.asmatrix(np.empty((M, D), dtype='complex'))
    if D == 1:
        for i in range(0, M):
                A[i] = np.e ** (-1j * i * K * d * np.cos(theta))
    else:
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
    W = np.asmatrix(np.random.normal(mean_nu, std_nu, size=(M,N)))

    # Genero el vector de muestras $X=A \times F + W$ de tamaño (M,1,N)
    X = np.asmatrix(np.empty((M,N),dtype=complex))
    X_matrix = np.asmatrix(np.empty((M,1)),dtype=complex)
    for n in range (0,N):
        F_matrix = F[:,n]
        W_matrix = W[:,n]
        X_matrix = A @ F_matrix + W_matrix
        X[:, n] = X_matrix

    return X

    
def doamusic_estimation(X, K_est, theta_est):
    M = X.shape[0]
    N = X.shape[1]
    S = np.asmatrix(np.empty((M,M),dtype=complex))

    #%% Calculo el vector de covarianza S
    for n in range (0,N):
        X_matrix=np.asmatrix(X[:,n])
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
    a = np.asmatrix(np.empty((M, 1), dtype=complex))

    
    if str(type(K_est)) == "<class 'numpy.ndarray'>":
        P_MU = np.empty((theta_est.size, K_est.size), dtype=complex)
        for i in range (0, K_est.size):
            for j in range(0, theta_est.size):
                for k in range(0,M):
                    a[k] = np.e ** (-1j * k * K_est[i] * d * np.cos(theta_est[j]))
                    P_MU[j, i] = 1 / (a.H @ EN @ EN.H @ a)
    else:
        P_MU = np.empty((theta_est.size), dtype=complex)
        for j in range(0, theta_est.size):
            for k in range(0,M):
                a[k] = np.e ** (-1j * k * K_est * d * np.cos(theta_est[j]))
                P_MU[j] = 1 / (a.H @ EN @ EN.H @ a)
                
    return P_MU

def plotanim(Data,X,step=0.02,ylim=[]):
    plt.ion()
    fig, ax = plt.subplots(1,1)
    plt.ylim((10 ** -3, Data.max()))
    plt.yscale('log')
    line, = ax.plot(X,Data[:,0])
    fig.canvas.draw()
    for i in range(Data.shape[1]):
        plt.pause(step)
        line.set_ydata(Data[:,i])
        fig.canvas.draw()
    plt.ioff()

#%% Definición de constantes y unidades
kHz = 10 ** 3
MHz = 10 ** 6
GHz = 10 ** 9
ms = 10 ** -3
c = 3 * 10 ** 8
km = 10 ** 3

#%% Definición de variables
M = 8  # Número de sensores
D = 3  # Número de señales
fs = 64 * MHz
N = 100 # Número de snapshots
T = 2 * ms # Tiempo de toma de muestras

theta_deg = np.array([30,90,120])  #DOA en grados
theta = theta_deg * np.pi / 180           #DOA en radianes

# Defición de señal y array de sensores
Fc = np.array([1.5* GHz, 1.5* GHz, 1.5 * GHz]) # Frecuencia de portadora de la señal transmitida 1
lambda_c = c / Fc
d = lambda_c[0] / 2  #Separación entre sensores


s_amp = np.array([30, 30, 30])
s_freq = np.array([440, 3500, 40000])

SNR = 7
#%% Generación del vector de muestras X
t = np.random.randint(0, int(T * fs), size=N) * 1 / fs  # Vector de tiempos de muestreo (tomas de snapshots)
X = doamusic_samples(Fc, s_amp, s_freq, t,0, d, theta, M, D, SNR)

#%%
#fc_est = np.linspace(1 * GHz, 2 * GHz,num=20)
#fc_est = np.array([1.5 *GHz])
fc_est = Fc[0]
K_est = 2 * np.pi * fc_est/c
theta_est = np.linspace(0, np.pi ,num=1000)
P_MU = doamusic_estimation(X, K_est, theta_est)

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

#%% Tracking de objeto moviéndose
# Definición de variables
M = 8  # Número de sensores
D = 1  # Número de señales
fs = 64 * MHz
N = 1000 # Número de snapshots
T = 2 * ms # Tiempo de toma de muestras

dist = 100  # Distancia en metros entre el emisor y la antena receptora
Tx_time = np.linspace(0, 15, num=1000)  # Tiempo del tracking
Tx_vel = 50 * km /3600 # Velocidad del transmisor en m/s
Tx_x = -100 + Tx_vel*Tx_time # Posición x del transmisor
Tx_y = 100  # Posición y del transmisor

theta_deg = 90 + np.arctan(Tx_x / Tx_y)*180/np.pi  #DOA en grados
theta = theta_deg * np.pi / 180           #DOA en radianes

# Defición de señal y array de sensores
Fc = 1.5* GHz # Frecuencia de portadora de la señal transmitida 1
lambda_c = c / Fc
d = lambda_c / 2  #Separación entre sensores

t = np.random.randint(0, int(T * fs), size=N) * 1 / fs  # Vector de tiempos de muestreo (tomas de snapshots)
s_amp = np.array([10])
s_freq = np.array([40000])

SNR = 7

fc_est = Fc
K_est = 2 * np.pi * fc_est/c
theta_est = np.linspace(0, np.pi ,num=180)
P_MU = np.empty((180,1000),dtype='complex')
#%%
for i in range (0,theta.size):
    X = doamusic_samples(Fc, s_amp, s_freq, t, Tx_time[i], d, theta[i], M, D, SNR)
    P_MU[:,i] = doamusic_estimation(X, K_est, theta_est)


#%%


'''plt.figure()
plt.plot(theta_est * 180 / np.pi, np.abs(np.array(P_MU[:,0])))
plt.yscale('log')
plt.show()'''

#%%
plotanim(np.abs(np.array(P_MU)), theta_est * 180 / np.pi, step=1/60)


#%%
np.abs(np.array(P_MU)).max()

#%%
