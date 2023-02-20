#%%
import numpy as np
import matplotlib.pyplot as plt
import math


SRATE = 44100
dur = 1

#%%
#Ejercicio2
def osc(f, d):
    x = np.linspace(0, 1, SRATE * d)
    return np.sin(2 * np.pi * f * x)

def square(f, d):
    x = np.full((int)(SRATE * d / f / 2), 1)
    x2 = np.concatenate((x, -x))
    return np.tile(x2, f)

#%%
#Ejercicio 1

v = np.random.random(size = SRATE * dur) * 2 - 1

plt.plot(v, linewidth=0.5)

plt.show()
#%%
#Ejercicio3

plt.plot(square(8, 4))

#plt.plot(v, linewidth=0.5)

 #%%

# %%
