#%% Librerías y funciones utilizadas
#%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import inv,eig
from numpy import dot
import matplotlib.style as style
from scipy import signal
style.use('default')
###############################################################################
def GaussianNoise(SNR,Ps,M,N):
    """
    Recibe una potencia de señal Ps y una relación señal-ruido deseada
    SNR y retorna un vector Nu correspondiente a muestras del ruido 
    blanco gaussiano a sumarle a la señal
    """
    mean_nu = 0
    var_nu = Ps/(10**(SNR/10))
    std_nu = np.sqrt(var_nu) # sigma_n
    Nu = np.random.normal(mean_nu, std_nu, size=(M,N))
    return (Nu)

def filter(X, Wn, filtertype):
    order = 4
    [b, a] = signal.butter(order, Wn, btype=filtertype)  #coeficientes del filtro butterworth utilizado
    Y = signal.lfilter(b, a, X)  #filtro la señal para limitar el ruido
    return Y

def getS(X):
    X=np.matrix(X)
    M = X.shape[0]
    N = X.shape[1]
    S=np.zeros((M,M),dtype='complex')
    for n in range(0, N):
        S_aux = (1 / N) * (X[:, n] @ X[:, n].conj().T)
        S = S + S_aux
    return S


#%%
# Definición de constantes y unidades
kHz = 10 ** 3
MHz = 10 ** 6
GHz = 10 ** 9
c = 3 * 10 ** 8

#%%
# Definición de variables
M = 8  # Número de sensores
D = 2  # Número de señales
N = 10 # Número de snapshots
theta_deg = np.array([-60,35])  #DOA en grados
theta = theta_deg * np.pi / 180           #DOA en radianes

# Defición de señal y array de sensores
F1 = 1.5 * GHz  # Frecuencia de la señal transmitida 1
F2 = 1.5 * GHz  # Frecuencia de la señal transmitida 2
# BW = 4 * GHz
fs = 4 * GHz
lambda_signal = c / F1
d = lambda_signal / 2  #Separación entre sensores
f1 = F1 / fs  # Frecuencia discreta normalizada 1
w1 = 2 * np.pi * f1
f2 = F2 / fs  # Frecuencia discreta normalizada 2
w2 = 2 * np.pi * f2

f = np.array([F1, F2])
w = np.array([w1, w2])
lambda_f = c / f  # Longitud de onda de la señal transmitida
a = np.array([10,20])  # Amplitud de la señal transmitida
K = 2 * np.pi / lambda_f
l=np.array([1000.1265478945,1521.654879841321])

A=np.zeros((M,D),dtype='complex')
for i in range(0, M):
    for j in range(0, D):
        A[i, j] = np.e ** (-1j * i * K[j] * d * np.cos(theta[j]))

F=np.zeros((D,N),dtype='complex')
for i in range(0, D):
    for n in range (0,N):
        F[i, n] = a[i] * np.e ** (-1j * (K[i] * l[i] + w[i] * n))
        
    
X = np.dot(A, F)
SNR = 30
Ps = (a[0]**2+a[1]**2)/4
W = GaussianNoise(SNR, Ps, M, N)
X = X + W

#%%
S=getS(X)





#%%



#SNR = np.arange(0, 30) #Vector de valores de SNR
SNR=30
f_est = np.zeros(2)
a_est = np.zeros(2)
theta_deg_est = np.zeros(2)

#for i in range(10, len(SNR)):
#    print(str(i)+" : "+str(SNR[i]))
#    [f_est[i,:],a_est[i,:],theta_deg_est[i,:],var_nu_est[i]]=doa(a, f, theta, d, N, SNR[i])

M = f.size
phi1 = (2 * np.pi * f1 / c) * d * np.sin(theta[0])  #Fase entre sensores para la f1
phi2 = (2 * np.pi * f2 / c) * d * np.sin(theta[1])  #Fase entre sensores para la f2
Ts = d * np.sin(theta[0])/c  #Período de muestreo por la separación de los sensores
fs = 1 / Ts
w1 = f[0] * np.pi / (fs / 2) #Frecuencia discreta normalizada 1
w2 = f[1] * np.pi / (fs / 2)  #Frecuencia discreta normalizada 2
W=[w1,w2]
# Definición del ruido y del vector de muestras X
X = np.zeros(N)
A1 = a1 * np.cos(phi1)
A2 = a2 * np.cos(phi2)
B1 = -a1 * np.sin(phi1)
B2 = -a2 * np.sin(phi2)
Alpha = np.array([A1,A2,B1,B2])
S = np.zeros((N, 2*M))
for m in range (0,M):
    for n in range(0, N):
        S[n, m] = np.cos(n * W[m])
        S[n, m+2] = np.sin(n * W[m])
X = np.dot(S, Alpha)
Ps = np.mean(X ** 2)
W=GaussianNoise(SNR,Ps)
X = np.dot(S, Alpha) + W # Vector de muestras recibidas

#%% Step 0: Collect data and form S
S= getS(X)

#%%
X @ X.conj().T

#%%
A=np.array([3,2,1])
A=np.matrix(A)
#%%
A.T@A

#%%
X=np.matrix(X)

#%%
S

#%%
[w, v] = eig(S)

#%%
wabs=np.abs(w)

#%%
min(wabs)

#%%
np.where(wabs==min(wabs))

#%%
w[3]*v[3]

#%%
X=np.matrix(X)
X[:, 3] @ X[:, 3].conj().T

#%%
a=X[:, 3]

#%%
b=X[:, 3].conj().T

#%%
a@b.conj()

#%%
