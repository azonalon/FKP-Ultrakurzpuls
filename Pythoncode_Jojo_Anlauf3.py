# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 12:20:59 2016

@author: Jonathan
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def linearFit(x, a, b):
    return a * x + b
#%%
def autokorrFit(x, a, invw, x0):
    return a*((invw*(x-x0) - 1)*np.exp(4*invw*(x-x0)) + ( (x-x0)*invw+1)*np.exp(2*(x-x0)*invw) )/(np.exp(2*(x-x0)*invw-1)-1)**3

def gaussFit(x, a, b, c, mu):
    return a*np.exp(-(x+b)**2 / mu**2)

autokorrFit(DL, *p0)
#%%
IL, PL = np.genfromtxt("./measurements/5_pi_qs_ml.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, unpack=True)
IL2, UO = np.genfromtxt("./measurements/6_freq_pulse_amplitude.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, unpack=True)
IL3, PL3 = np.genfromtxt("./measurements/5_pi_qs_ml.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, skip_footer=18, unpack=True)


fig = plt.figure()
plt.title('Hauptlaser gepulster Betrieb')
ax = fig.add_subplot(111)
ax.plot(IL, PL, '.')
ax2 = ax.twinx()
ax2.plot(IL2, UO, '.')
ax.set_xlabel("Punpstrom in mA")
ax.set_ylabel("Leistung in mW")
ax2.set_ylabel("Spannung in mV")
ax.errorbar(IL, PL, xerr=10, yerr=1, fmt='ro')
ax2.errorbar(IL2, UO, xerr=10, yerr=10, fmt='bs')

#%%
plt.figure()

parameters = curve_fit(linearFit, IL3, PL3)
[a, b] = parameters[0]
x1 = np.arange(0, 3000, 500)
plt.plot(IL, PL, '.')
plt.title('Schwellenstrom')
plt.xlabel("Punpstrom in mA")
plt.ylabel("Leistung in mW")
Fit1 = plt.plot(x1, a*x1+b, label='Schwellenstrom=725.17 mA')
plt.legend(loc='upper left')

#%%

plt.figure()

IL4, GP = np.genfromtxt("C:/Users/Jonathan/Desktop/FKP-Ultrakurzpuls/measurements/6_freq_pulse_amplitude.csv", delimiter=',',
                         usecols=(0,2), skip_header=1, skip_footer=13, unpack=True)

plt.plot(IL4, 1/GP, '.')
plt.title('Frequenz der Riesenpulse')
plt.xlabel('Stromstärke in mA')
plt.ylabel('Frequenz in MHz')
plt.errorbar(IL4, 1/GP, xerr=10, fmt='.')

#%%

plt.figure()
DL, AM = np.genfromtxt("./measurements/11_auto_correlation.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, skip_footer=2, unpack=True)
                         
parameters2 = curve_fit(gaussFit, DL, AM)
[a2, b2, c2, d2] = parameters2[0]
x2 = np.arange(0, 3.4, 0.1)
plt.plot(DL, AM, '.')
plt.plot(x2, gaussFit(x2, a2, b2, c2, d2))
plt.title('Autokorrelationsfunktion im gepulsten Betrieb')
plt.xlabel('Verschiebung in mm')
plt.ylabel('Amplitude in mV')


#%%




