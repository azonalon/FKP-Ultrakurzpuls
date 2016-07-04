#!/bin/python
from mpl import plot_config, palette, plotf
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc
from scipy.optimize import curve_fit
plot_config('pdf')


def linearFit(x, a, b):
    return a * x + b

def lasingFit(x, a, b, c, x0=0):
    return (a * (x-x0) + b)/2 + np.sqrt(c * (x-x0) + (a * (x-x0) + b)**2)/2
    """ ts: speed of transition from 1 to 2
        return (a * x + b)/2 + np.sqrt(c * x + (a * x + b)**2)/2
    """

    #%%
plt.figure(figsize=(4,3))
plt.xticks([])
plt.yticks([])
plt.ylim(0, .3)
plt.xlabel("Pumpleistung")
plt.ylabel("Ausgangsleistung")
for c in np.linspace(1, 0, 5):
    plotf(lasingFit, 0, 1.2, popt=[1, -1, c**3/10], label='$%3.3g$' % (c**3/10))
plt.legend(title='$P_\\text{vac}$ in willk. einh.', loc='best')
plt.savefig("./figures/lasing_pvac")

#%% P-I Diagrams with high reflective mirror

IL, PL = np.genfromtxt("./measurements/1_pi_laser.csv", delimiter=',',
                         usecols=(0,1), skip_header=20, unpack=True)
IPL, PPL= np.genfromtxt("./measurements/2_pi_pumplaser.csv", delimiter=',',
                         usecols=(0,1), skip_header=1, unpack=True)
Tauskoppel_P_I = np.genfromtxt("./measurements/3_pi_auskoppel.csv", delimiter=',',
                         usecols=(0,1,2), skip_header=1)

## mainlaser P-I
plt.figure(figsize=(6.7,6.7))
plt.subplot2grid((2,2), (0, 0))
plt.title("Hauptlaser")
plt.xlabel("Pumpstrom in \\si{\\milli\\ampere}")
plt.ylabel("Leistung in \\si{\\milli\\watt}")
plt.errorbar(IL, PL, xerr=10, yerr=2, fmt='.', color=palette[1])
#plt.savefig("./figures/pi_laser")

## pumplaser P-I
plt.subplot2grid((2,2), (0, 1))
plt.title("Pumplaser")
po2, co2 = curve_fit(linearFit, IPL, PPL)
powerPumplaser = lambda I: linearFit(I, *po2)
plt.xlabel("Pumpstrom in \\si{\\milli\\ampere}")
#plt.ylabel("Pumplaserleistung in \si{\\milli\\watt}")
plt.plot(IPL, linearFit(IPL, *po2), label='Schwellstrom \n %.3g mA' % (po2[1]/po2[0]))
plt.errorbar(IPL, PPL, xerr=10, yerr=2, fmt='.')
plt.legend(loc='upper left')
#plt.savefig("./figures/pi_pumplaser")

## slope efficiency
plt.subplot2grid((2,2), (1, 0), colspan=2)
plt.title("Differentieller Wirkungsgrad")
PPL = powerPumplaser(IL)
plt.xlabel("Pumplaserleistung in \\si{\\milli\watt}")
plt.ylabel("Laserleistung in \\si{\\milli\\watt}")
po, co = curve_fit(lasingFit, PPL, PL, p0=[60./200.,-15, 1])
a, b, c = po
label = '$\\frac{%3.3g P \\SI{%.3g}{\\milli\\watt}+\\sqrt{%3.3g P + (%.3g P \\SI{%.3g}{\\milli\\watt})^2}}{2}$' % (a, b, c, a, b)
X = np.linspace(0, 1300, 100)
plt.plot(X, lasingFit(X, *po), label=label)
plt.errorbar(PPL, PL, fmt='.', yerr=2, xerr=10*po2[0])
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("./figures/slope_efficiency")

### findley clay plots
#%%
plt.figure()
plt.subplot(1, 2, 1)
plt.xlabel("Pumpleistung in \\si{\\milli\\watt}")
plt.ylabel("Laserleistung in \\si{\\milli\\watt}")
arr = Tauskoppel_P_I
Ts = np.unique(arr[:,0])
ls = []
rs = [4, 6, 6, 6]
colors = ['r', 'g', 'b', 'y']
for i, T in enumerate(Ts):
#    plt.subplot(2,2,i+1)
#    plt.figure()
    TIP = arr[arr[:,0]==T][:,1:]
#    def fit(x, a, b, c):
#        return a*x**2 + b*x + c
    def fit(x, a, b):
        return a*x + b

        #    print(T, TIP)
    I, P = np.transpose(TIP)
    PP = powerPumplaser(I)
    popt, pcov = curve_fit(fit, PP[rs[i]:], P[rs[i]:])
    plt.ylim(0,250)
    plt.xlim(200, 1200)
#    plt.title("%2.2f" % T)
#    plt.plot(PP, P, yerr=10, xerr=20, fmt='.',label="%2.1f" % T)
    plt.plot(PP, P, 'd', label="%2.1f  \\si{\\percent}" % Ts[i],
             color=palette[i])

    XFit = np.linspace(200, 1200)
    plt.plot(XFit, fit(XFit, *popt), color=palette[i]
    #, label="%2.1f fit" % Ts[3-i]
    )
    plt.legend(loc='upper left', title='Transmissionsrate', numpoints=1)
#    ls.append(-popt[1]/popt[0]) # laserschwelle
#    a, b, c = popt
#    q = c/a
#    p = b/a
#    ns = -p/2 + np.sqrt(p**2/4 - q)
#    ns = minimize_scalar(lambda x: fit(x, *popt), bounds=[200, 400]).x
    a, b = popt
    ns = -b/a
    ls.append(ns) # laserschwelle
#    print('zero?' , fit(ns, *popt))
#plt.savefig("./figures/auskoppel")


plt.subplot(1, 2, 2)
plt.xlabel("$-\\log R$")
plt.ylabel("Laserschwelle in \\si{\\milli\\watt}")
lnRs = -np.log(1-Ts/100)
po, pc = curve_fit(linearFit, lnRs[1:], ls[1:])
XFit = np.linspace(0, .11, 100)
plt.plot(XFit, linearFit(XFit, *po), label="$\\SI{%.3g}{\\milli\\watt}(-\\log R) + \\SI{%.3g}{\\milli\\watt}$ \n \\SI{%2.1f}{\\percent} Verluste" % (po[0], po[1], 100*po[0]/po[1] ))
plt.plot(lnRs, ls, 's')
plt.legend()
plt.tight_layout()
plt.savefig("./figures/findlay_clay")
#%%
# Relaxation oscillations
Irs, Trs, Urs = np.genfromtxt("./measurements/4_relaxationsschwingung.csv", delimiter=',',
                         usecols=(0,1,2), skip_header=1, unpack=True)
frs = 1/Trs
Ufrs = np.abs(1/(Trs - Urs) - 1/(Trs + Urs))/2
plt.figure(figsize=(4,4))
Prs = powerPumplaser(Irs)

def polyFit(x, a, b, c=0):
    return a + b * x + c * x**2

po, pc = curve_fit(polyFit, Prs, frs, sigma=Ufrs, p0=[0, 0])

plt.xlabel("Pumplaserleistung in \\si{\\milli\\watt}")
plt.ylabel("Periodendauer in \\si{\\micro\\second}")
plotf(polyFit, 300, 1200, popt=po)
plt.errorbar(Prs, frs, yerr=Ufrs, fmt='.', xerr = 10)
plt.savefig("./figures/relaxationsschwingung")

#%% razor blade plots

def Erfc(x, a, invw, x0, c=0):
    return a * erfc((x - x0)*invw)/2 + c

#def waist(z, z0, a, b):
#    return a * np.sqrt(1 + (z-z0)**2 * b**2)

ZXI = np.genfromtxt("./measurements/10_razorblade_40mm_x.csv", delimiter=',',
                         usecols=(0,1,2), skip_header=1)
ZYI = np.genfromtxt("./measurements/10_razorblade_40mm_y.csv", delimiter=',',
                         usecols=(0,1,2), skip_header=1)



#%% angle dependence
plt.figure(figsize=(3.3, 3.3))
F, Q, I = np.genfromtxt("./measurements/8_angle_frequencydoubling.csv", delimiter=',',
                         usecols=(0,1,2), skip_header=71, unpack=True)
plt.xlabel("Winkel in \\si{\\degree}")
plt.ylabel('Intensit\\"at in willk. einh.')
plt.ylim(0, 140)
plt.plot(Q - 254, I, 'd', color=palette[1])
plt.savefig('./figures/angle_shg')


#%%
colors = ['r', 'g', 'b', 'y']
j=0
fig, axes = plt.subplots(2, 2, sharex='col', figsize=(8,6))
axes[1, 0].set_xlabel("Normierte Klingenposition in \\si{\\milli\\metre}")
axes[0, 0].set_ylabel("Laserleistung in \\si{\\milli\\watt}")
axes[0, 0].set_title("x-Achse")
axes[1, 0].set_title("y-Achse")
axes[1, 1].set_xlabel("z-Abstand zu der Linse in \\si{\\milli\\metre}")
axes[0, 1].set_ylabel("Strahlradius in \\si{\\milli\\metre}")

for a0, ZAI, axis in [(3, ZXI, 'x'), (13.5, ZYI, 'y')]:
    axpr = axes[j, 0]
    axdiv = axes[j, 1]
    Z = np.unique(ZAI[:,0])
    invws = np.empty(4)
    for i, z in enumerate(Z):

        zAI = ZAI[ZAI[:,0]==z]
        A, I = np.transpose(zAI)[[1,2]]
        po, pc = curve_fit(Erfc, A, I, p0=[0, 20, a0, 0])
        axpr.plot(A - po[2], I, '.', color = palette[i], label='\\SI{%2d}{\\milli\\metre}' % z)
        po[2] = 0
        axpr.set_xlim(-1.5, 1.5)
        axpr.set_ylim(0, 70)
        plotf(Erfc, -2, 2, ax=axpr, popt=po, color=palette[i])
        invws[i] = po[1]
    axpr.legend(loc='lower right', title='$z$-Position',
                numpoints=1, frameon=False)
    ws = 1/invws
    po, pc = curve_fit(polyFit, Z, ws, p0=[0,0])
    plotf(polyFit, 5, 30, popt=po, ax=axdiv, label="$\\SI{%.3g}{\\milli\\metre} - %.3g \\, z$ \n $w_0=\\SI{%.2g}{\\micro\\metre}$" % (po[0], -po[1], -1064e-3/po[1]/np.pi))
    axdiv.plot(Z, ws, 's')
    axdiv.legend(loc='best', frameon=False)
    j+=1
plt.tight_layout()
# hide tick and tick label of the big axes
fig.savefig("./figures/beam_div")
