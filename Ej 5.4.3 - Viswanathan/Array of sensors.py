#%% Librerías utilizadas
#%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import inv
from numpy import dot

def GaussianNoise(SNR,Ps):
    mean_nu = 0
    var_nu = Ps/(10**(SNR/10))
    std_nu = np.sqrt(var_nu) #sigma_n
    Nu = np.random.normal(mean_nu, std_nu, size=N)
    return (Nu,var_nu)

def functionJ(Z, W):
    N = len(Z)
    M = len(W)
    S = np.zeros((N, 2*M))
    for m in range (0,M):
        for n in range(0, N):
            S[n, m] = np.cos(n * W[m])
            S[n, m + 2] = np.sin(n * W[m])

    #J = np.dot(np.dot(np.dot(Z.transpose(), S), np.linalg.inv(np.dot(S.transpose(), S))), np.dot(S.transpose(), Z))
    J = dot(Z.transpose(), S)
    Sinv = dot(S.transpose(), S)
    det = np.linalg.det(Sinv)
    if det < 1:
        J = 0
    else:
        Sinv=inv(Sinv)
        J = dot(J, Sinv)
        J= dot(J,dot(S.transpose(),Z))
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
theta_deg = 60              #DOA en grados
theta = theta_deg * np.pi / 180           #DOA en radianes

# Defición de señal y array de sensores
f1 = 900 * MHz  #Frecuencia de la señal transmitida 2
f2 = 1.7 * GHz  #Frecuencia de la señal transmitida 2
f=np.array([f1,f2])
a1 = 10  #Amplitud de la señal transmitida 1
a2 = 20  #Amplitud de la señal transmitida 
a=np.array([a1,a2])
lambda1 = c / f1  #Longitud de onda de la señal transmitida
lambda2 = c / f2  #Longitud de onda de la señal transmitida
d = lambda2 / 2             #Separación entre sensores
phi1 = (2 * np.pi * f1 / c) * d * np.sin(theta)  #Fase entre sensores para la f1
phi2 = (2 * np.pi * f2 / c) * d * np.sin(theta)  #Fase entre sensores para la f2
phi=np.array([phi1,phi2])
Ts = d * np.sin(theta)/c  #Período de muestreo por la separación de los sensores
fs = 1 / Ts
w1 = f1 * np.pi / (fs / 2) #Frecuencia discreta normalizada 1
w2 = f2 * np.pi / (fs / 2)  #Frecuencia discreta normalizada 2
W=np.array([w1,w2])


#%% Definición del ruido y del vector de muestras Z
Z = np.zeros(N)
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

SNR=-8
Z = np.dot(S, Alpha)
Ps = np.mean(Z ** 2)
[Nu,var_nu]=GaussianNoise(SNR,Ps)
Z = np.dot(S, Alpha) + Nu

#%% Estimación de w1 y w2
#W1_est = np.linspace(w1 - 1, w1 + 1, 50)
#W2_est = np.linspace(w2 - 1, w2 + 1, 50)
W1_est = np.linspace(0, np.pi, 100)
W2_est = np.linspace(0, np.pi, 100)

J=np.zeros((len(W1_est),len(W2_est)))

for i in range(0, len(W1_est)):
    for j in range(0, len(W2_est)):
        W_est=np.array([W1_est[i],W2_est[j]])
        J[i,j]=functionJ(Z,W_est)

#%% Ploteo de J en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(W1_est, W2_est)
ax.plot_surface(X, Y, J, cmap='viridis')
ax.set_xlabel(r'$\omega_1$')
ax.set_ylabel(r'$\omega_2$')
ax.set_zlabel('J')
plt.show()

#%% Busco el máximo de la función
idx=np.unravel_index(np.argmax(J, axis=None), J.shape)
idx2 = np.where(J == J.max())
w1_est = W1_est[idx[0]]
w2_est = W2_est[idx[1]]
W_est=np.array([w1_est,w2_est])
f1_est = w1_est * (fs / 2) / np.pi
f2_est = w2_est * (fs / 2) / np.pi
print("f1_est=" + str(f1_est) + "\nf2_est=" + str(f2_est))

#%% Habiendo encontrado el máximo hago una búsqueda más fina con mayor resolución
W1_est = np.linspace(w1_est - 0.05, w1_est + 0.05, 50)
W2_est = np.linspace(w2_est - 0.05, w2_est + 0.05, 50)

J=np.zeros((len(W1_est),len(W2_est)))

for i in range(0, len(W1_est)):
    for j in range(0, len(W2_est)):
        W_est=np.array([W1_est[i],W2_est[j]])
        J[i,j]=functionJ(Z,W_est)

#%%Busco nuevamente el máximo
idx=np.unravel_index(np.argmax(J, axis=None), J.shape)
#idx = np.where(J == J.max())
w1_est = W1_est[idx[0]]
w2_est = W2_est[idx[1]]
W_est=np.array([w1_est,w2_est])
f1_est = w1_est * (fs / 2) / np.pi
f2_est = w2_est * (fs / 2) / np.pi
print("f1_est=" + str(f1_est) + "\nf2_est=" + str(f2_est))

#%% Defino la matriz S con las frecuencias estimadas
S_est = np.zeros((N, 2*M))
for m in range (0,M):
    for n in range(0, N):
        S_est[n, m] = np.cos(n * W_est[m])
        S_est[n, m + 2] = np.sin(n * W_est[m])
        
#%%Calculo el vector Alpha estimado y los valores am_est y phim_est
Alpha_est = inv(dot(S_est.transpose(), S_est))
Alpha_est = dot(Alpha_est, dot(S_est.transpose(), Z))
A1_est,A2_est,B1_est,B2_est=Alpha_est[0],Alpha_est[1],Alpha_est[2],Alpha_est[3]
a1_est = np.sqrt(A1_est ** 2 + B1_est ** 2)
phi1_est = np.arctan(-1*B1_est / A1_est)
if phi1_est < 0:
        phi1_est=phi1_est+np.pi
a2_est = np.sqrt(A2_est** 2 + B2_est** 2)
phi2_est = np.arctan(-1*B2_est / A2_est)
if phi2_est < 0:
        phi2_est=phi2_est+np.pi
print("a1_est=" + str(a1_est) + "\tphi1_est=" + str(phi1_est) + "\na2_est=" + str(a2_est) + "\tphi2_est=" + str(phi2_est))

#%% Obtengo el ángulo de arribo estimado
theta1_est = np.arcsin(phi1_est / (d * 2 * np.pi * f1_est / c))
theta2_est = np.arcsin(phi2_est / (d * 2 * np.pi * f2_est / c))
theta_est = np.average([theta1_est, theta2_est])
theta_deg_est= theta_est*180/np.pi
print("Direction of arrival = "+str(theta_deg_est)+"°")


#%% Obtengo la varianza del ruido
var_nu_est = Z - dot(S_est, Alpha_est)
var_nu_est= np.sqrt(1/N * dot(var_nu_est.transpose(),var_nu_est))
print("Varianza del ruido = "+str(var_nu_est))


#%%
phi1_est / (d * 2 * np.pi * f1_est / c)

