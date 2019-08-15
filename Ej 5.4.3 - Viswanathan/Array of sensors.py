#%% Librerías utilizadas
import numpy as np
import matplotlib.pyplot as plt

#%%
#Definición de constantes y unidades
kHz = 10 ** 3
MHz = 10 ** 6
GHz = 10 ** 9

c = 3 * 10 ** 8


#Definición de variables
N = 8                       #Número de sensores
M = 1                       #Número de sinusoides
theta = np.pi / 6           #DOA

#Definición de ruido
mean = 0
std = 1
nu = np.random.normal(mean, std, size=N)

#Defición de señal y array de sensores
a0 = 1                      #Amplitud de la señal transmitida
f0 = 432.49       #Frecuencia de la señal transmitida
w0 = 2 * np.pi * f0
psi0 = 0                    #Fase de la señal transmitida
lambda0 = c / f0            #Longitud de onda de la señal transmitida
d = lambda0 / 2             #Separación entre sensores

phi = (w0 / c) * d * np.sin(theta)  #Fase entre sensores

#%%Definición del vector de muestras Z
Z = np.zeros(N)
A = a0 * np.cos(phi)
B = -a0 * np.sin(phi)
Alpha = np.array([A, B])
S = np.matrix([np.cos(w0 *N )])