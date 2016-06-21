#!/bin/python
from mpl import plot_config
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.special import erfc
from scipy.optimize import curve_fit
plot_config()

IL, PL = np.genfromtxt("./measurements/1_pi_laser.csv", delimiter=',',
                         usecols=(0,1), skip_header=20, unpack=True)
IPL, PPL= np.genfromtxt("./measurements/2_pi_pumplaser.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, unpack=True)
#P = np.sort(P)
#I = np.sort(I)
def linearFit(x, a, b):
    return a * x + b       

def lasingFit(x, a, b, c):
    return (a * x + b)/2 + np.sqrt(c * x + (a * x + b)**2)/2
    """ ts: speed of transition from 1 to 2 
        return (a * x + b)/2 + np.sqrt(c * x + (a * x + b)**2)/2    
    """
    
#plt.subplot(111)
plt.xlabel("Pumpstrom in \\si{\\milli\\ampere}")
plt.ylabel("Laserleistung in \\si{\\milli\\watt}")
plt.errorbar(IL, PL, xerr=10, yerr=2, fmt='.')
#plt.subplot(211)
plt.figure()
po2, co2 = curve_fit(linearFit, IPL, PPL)
powerPumplaser = lambda I: linearFit(I, *po2)
plt.xlabel("Pumpstrom in \\si{\\milli\\ampere}")
plt.ylabel("Pumplaserleistung in \si{\\milli\\watt}")
plt.errorbar(IPL, PPL, xerr=10, yerr=2, fmt='.')
plt.plot(IPL, linearFit(IPL, *po2))

plt.figure()
PPL = powerPumplaser(IL)
plt.xlabel("Pumplaserleistung in \\si{\\milli\watt}")
plt.ylabel("Laserleistung in \\si{\\milli\\watt}")
po, co = curve_fit(lasingFit, PPL, PL, p0=[60./200.,-15, 1 ])
X = np.linspace(0, 1300, 100)
plt.plot(X, lasingFit(X, *po))
plt.errorbar(PPL, PL, fmt='.', yerr=2, xerr=10*po2[0])

plt.figure()
po2, co2 = curve_fit(linearFit, IPL, PPL)
powerPumplaser = lambda I: linearFit(I, *po2)
plt.xlabel("Pumpstrom in \\si{\\milli\\ampere}")
plt.ylabel("Pumplaserleistung in \si{\\milli\\watt}")
plt.errorbar(IPL, PPL, xerr=10, yerr=2, fmt='.')
plt.plot(IPL, linearFit(IPL, *po2))