from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

def regenerator(Th, Tc, sigma, omega_C, nT, nX, Tg, Tm, effi_A):
    dT = 1/nT
    dX = 1/nX

    par_a = sigma * dX
    par_b = omega_C * dT
    # Main loop
    A = np.array([[1+par_a/2,-par_a/2],[-par_b/2,1+par_b/2]])
    effi_A = 0
    for i in range(0,nT-1):
        for j in range(0,nX-1):
            b = ([[Tg[i+1,j]*(1-par_a/2) + Tm[i+1,j]*par_a/2],[Tm[i,j+1]*(1-par_b/2) + Tg[i,j+1]*par_b/2]])
            T = np.dot(inv(A),b)
            Tg[i+1,j+1] = T[0,0]
            Tm[i+1,j+1] = T[1,0]
        effi = (Th-Tg[i+1,nX-1])/(Th-Tc)
        effi_A = effi_A+effi*(dT)
#    for i in range(0,nT-1,10):
#        plt.plot(np.linspace(0,1,nX),Tm[i,:],np.linspace(0,1,nX),Tg[i,:])
#        plt.plot(np.linspace(0,1,nX),Tm[i,:])
#plt.legend()
#    plt.show()
#    print("tau/sigma=%f effi=%f" %(omega_C/sigma,(Th-Tg[nT-1,nX-1])/(Th-Tc)))
    print("effi=%f"%effi_A)

#sigma = h*Ah*l/(w*Cp_g)
#omega_C = h*Ah*tr/(rho_m*Cm)

sigma = 80
omega_C = 48

print("sigma=%f, omega_C=%f" %(sigma,omega_C))

nT = 800
nX = 800

# Basic data container for gas and mesh
Tg = np.zeros((nT,nX))
Tm = np.zeros((nT,nX))
Th = 300
Tc = 80
effi_A=0
par_b = omega_C / nT
# Boundary cond. for gas
Tg[:,0] = Th
# Initial cond. for gas
Tg[0,:] = np.linspace(Th,Tc,nX)
# Initial cond. for mesh
Tm[0,:] = np.linspace(Th,Tc,nX)
# Boundary cond. for mesh
for i in range(0,nT-1):
    Tm[i+1,0] = Tm[i,0] - par_b*(Tm[i,0] - Tg[i,0])
regenerator(Th,Tc,sigma,omega_C,nT,nX,Tg,Tm,effi_A)

for bb in range(0,30,1):
    Tg = np.flipud(np.fliplr(Tg))
    Tm = np.flipud(np.fliplr(Tm))
    cont = Tc
    Tc = Th
    Th = cont
    Tg[:,0] = Th
#    Tg[0,:] = np.linspace(Th,Tc,nX)
    for i in range(0,nT-1):
        Tm[i+1,0] = Tm[i,0] - par_b*(Tm[i,0] - Tg[i,0])
    regenerator(Th,Tc,sigma,omega_C,nT,nX,Tg,Tm,effi_A)

for i in range(0,nT-1,10):
    plt.plot(np.linspace(0,1,nX),Tm[i,:],'b',np.linspace(0,1,nX),Tg[i,:],'r')
#        plt.plot(np.linspace(0,1,nX),Tm[i,:])
#plt.legend()
plt.show()

