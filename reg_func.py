from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

def fuckup(sigma, omega_C, nT, nX):
    # Time and space division
    Th = 300
    Tc = 80

    # Basic data container for gas and mesh
    Tg = np.zeros((nT,nX))
    Tm = np.zeros((nT,nX))
    dT = 1/nT
    dX = 1/nX

    par_a = sigma * dX
    par_b = omega_C * dT
    # Boundary cond. for gas
    Tg[:,0] = Th
    # Initial cond. for gas
    Tg[0,:] = np.linspace(Th,Tc,nX)
    # Initial cond. for mesh
    Tm[0,:] = np.linspace(Th,Tc,nX)
    # Boundary cond. for mesh
    for i in range(0,nT-1):
        Tm[i+1,0] = Tm[i,0] - par_b*(Tm[i,0] - Tg[i,0])

    # Main loop
    A = np.array([[1+par_a/2,-par_a/2],[-par_b/2,1+par_b/2]])
    for i in range(0,nT-1):
        for j in range(0,nX-1):
            b = ([[Tg[i+1,j]*(1-par_a/2) + Tm[i+1,j]*par_a/2],[Tm[i,j+1]*(1-par_b/2) + Tg[i,j+1]*par_b/2]])
            T = np.dot(inv(A),b)
            Tg[i+1,j+1] = T[0,0]
            Tm[i+1,j+1] = T[1,0]

#    for i in range(0,nT-1,10):
#        plt.plot(np.linspace(0,1,nX),Tm[i,:],np.linspace(0,1,nX),Tg[i,:])
#plt.legend()
#    plt.show()
#    print("tau/sigma=%f effi=%f" %(omega_C/sigma,(Th-Tg[nT-1,nX-1])/(Th-Tc)))
    print(omega_C/sigma,(Th-Tg[nT-1,nX-1])/(Th-Tc))

# heat transfer coef. (w/m^2K)
h = 5500
# Heat transfer area per unit volume (m^2/m^3)
Ah = 65000
# Gas specific heat (J/kgK)
Cp_g = 5200
# Mesh specific heat (J/kgK)
Cm = 380
# Gas density (kg/m^3)
rho_g = 2.2
# Mesh density (kg/m^3)
rho_m = 8800
# Gas flow rate per unit area (kg/m^2s)
w = 9.02
# Regenerator length (m)
l = 0.103
# Time scale
tr = 0.5

sigma = h*Ah*l/(w*Cp_g)
omega_C = h*Ah*tr/(rho_m*Cm)
print("sigma=%f, omega_C=%f" %(sigma,omega_C))
for i in range(1,30,1):
    fuckup(sigma,omega_C*i/20,500,500)
