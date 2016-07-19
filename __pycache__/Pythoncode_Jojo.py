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

def autokorrFit(x, a, b):
    return 16*(a*x+b-1)*np.exp(4*(a*x+b)+(a*x+b+1)*np.exp(2*(a*x+b)))/((np.exp(2*(a*x+b))-1)**3)

IL, PL = np.genfromtxt("C:/Users/Jonathan/Desktop/FKP-Ultrakurzpuls/measurements/5_pi_qs_ml.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, unpack=True)
IL2, UO = np.genfromtxt("C:/Users/Jonathan/Desktop/FKP-Ultrakurzpuls/measurements/6_freq_pulse_amplitude.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, unpack=True)
IL3, PL3 = np.genfromtxt("C:/Users/Jonathan/Desktop/FKP-Ultrakurzpuls/measurements/5_pi_qs_ml.csv", delimiter=',',
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

parameters = curve_fit(linearFit, IL3, PL3)
[a, b] = parameters[0]
x1 = np.arange(0, 3000, 500)
plt.plot(IL, PL, '.')
plt.title('Schwellenstrom')
plt.xlabel("Punpstrom in mA")
plt.ylabel("Leistung in mW")
Fit1 = plt.plot(x1, a*x1+b, label='Schwellenstrom=725.17 mA')
plt.legend(loc='upper left')

DL, AM = np.genfromtxt("C:/Users/Jonathan/Desktop/FKP-Ultrakurzpuls/measurements/11_auto_correlation.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, skip_footer=2, unpack=True)
parameters2 = curve_fit(autokorrFit, DL, AM)
[a2, b2] = parameters2[0]
x2 = np.arange(0.2, 3.4, 0.2)                         
plt.plot(DL, AM, '.')
Fit2 = plt.plot(x2, 16*(a2*x2+b2-1)*np.exp(4*(a2*x2+b2)+(a2*x2+b2+1)*np.exp(2*(a2*x2+b2)))/((np.exp(2*(a2*x2+b2))-1)**3))
plt.show()