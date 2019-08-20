#%% Librerías utilizadas
%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def functionJ(z, w):
    N = len(z)
    M = len(w)
    S = np.zeros((N, 2*M),dtype=complex)
    for m in range (0,M):
        for n in range(0, N):
            S[n, m] = np.cos(n * w[m])
            S[n, m + 2] = np.sin(n * w[m])

    J = np.dot(np.dot(np.dot(z.transpose(), S), np.linalg.inv(np.dot(S.transpose(), S))), np.dot(S.transpose(), z))
    
    return np.abs(J)

#%%
# Definición de constantes y unidades
kHz = 10 ** 3
MHz = 10 ** 6
GHz = 10 ** 9

c = 3 * 10 ** 8

#%%
# Definición de variables
N = 8                       #Número de sensores
M = 2                       #Número de sinusoides
theta = np.pi / 7           #DOA

# Definición de ruido
mean = 0
std = 0.001
Nu = np.random.normal(mean, std, size=N)

# Defición de señal y array de sensores
f1 = 1.7 * GHz  #Frecuencia de la señal transmitida 2
f2 = 900 * MHz  #Frecuencia de la señal transmitida 2
f=np.array([f1,f2])
a1 = 1  #Amplitud de la señal transmitida 1
a2 = 2
a=np.array([a1,a2])
lambda1 = c / f1            #Longitud de onda de la señal transmitida
d = lambda1 / 2             #Separación entre sensores
phi1 = (2 * np.pi * f1 / c) * d * np.sin(theta)  #Fase entre sensores para la f1
phi2 = (2 * np.pi * f2 / c) * d * np.sin(theta)  #Fase entre sensores para la f2
phi=np.array([phi1,phi2])
Ts = d * np.sin(theta)/c  #Período de muestreo por la separación de los sensores
fs = 1 / Ts
w1 = f1 * np.pi / (fs / 2) #Frecuencia discreta normalizada 1
w2 = f2 * np.pi / (fs / 2)  #Frecuencia discreta normalizada 2
w=np.array([w1,w2])


#%% Definición del vector de muestras Z
Z = np.zeros(N,dtype=complex)
A1 = a1 * np.cos(phi1)
A2 = a2 * np.cos(phi2)
B1 = -a1 * np.sin(phi1)
B2 = -a2 * np.sin(phi2)
Alpha = np.array([A1,A2,B1,B2])
S = np.zeros((N, 2*M),dtype=complex)
for m in range (0,M):
    for n in range(0, N):
        S[n, m] = np.cos(n * w[m])
        S[n, m+2] = np.sin(n * w[m])
Z = np.dot(S, Alpha) + Nu

#%% Estimación de w1 y w2
w1est = np.linspace(w1 - 2, w1 + 2, 5)
w2est = np.linspace(w2 - 2, w2 + 2, 5)

J=np.zeros((len(w1est),len(w2est)),dtype=float)

for i in range(0, len(w1est)):
    for j in range(0, len(w2est)):
        west=np.array([w1est[i],w2est[j]])
        J[i,j]=functionJ(Z,west)

#%% Ploteo de J
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(w1est, w2est)
ax.plot_surface(X, Y, J, cmap='viridis')
ax.set_xlabel(r'$\omega_1$')
ax.set_ylabel(r'$\omega_2$')
ax.set_zlabel('J')
plt.show()

#%%
