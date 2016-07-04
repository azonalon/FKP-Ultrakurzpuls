#!/bin/python
import matplotlib.pyplot as plt
import numpy as np
# import scipy.constants
# import scipy.optimize as opt
# from matplotlib import *
# from matplotlib.pyplot import *
palette=['#4c72b0', '#c44e52', '#55a868', '#8172b2', '#ccb974', '#64b5cd']

def plotf(f, a, b, *args, N=100, popt=None, ax=None, X=None, **kwargs):
    ax = plt if ax is None else ax
    X = np.linspace(a, b, N) if X is None else X
    Y = f(X) if popt is None else f(X, *popt)
    ax.plot(X, Y, *args, **kwargs)

def plot_config(filetype='ps'):
    from cycler import cycler
    import matplotlib
    params = {
        'image.cmap': 'jet',
        'text.usetex': True,
        'figure.figsize': (6.7, 4.14),
        'text.latex.unicode': True,
        'figure.dpi': 300,
        'lines.linewidth': 1.0,
        'savefig.bbox': 'tight',
#        'savefig.dpi': 300,
        'legend.frameon': False,
        'savefig.format': filetype,
        'axes.titlesize': 'medium',
        'axes.labelsize': 'medium',
        'axes.labelweight': 'normal',
#        'ps.fonttype': 42,
        'axes.prop_cycle':  cycler('color', ['#4c72b0', '#c44e52', '#55a868',
                                             '#8172b2', '#ccb974', '#64b5cd']) +
                            cycler('linestyle', ['-', '-', '-',
                                                 '-', '-', '-']),
        # 'svg.fonttype': 'svgfont',
        # 'axes.labelsize': 8, # fontsize for x and y labels (was 10)
        # 'axes.titlesize': 8,
        # 'text.fontsize': 8, # was 10
        # 'legend.fontsize': 8, # was 10
        # 'xtick.labelsize': 8,
        # 'ytick.labelsize': 8,
        # 'figure.figsize': [fig_width,fig_height],
        'font.family': 'serif',
        'text.latex.preamble': [r'\usepackage[]{siunitx}'
                                # r'\sisetup{text-angstrom = \AA}'
#                                r'\usepackage[]{mhchem}'
                                r'\usepackage[bitstream-charter]{mathdesign}'
                                ],
    }
    matplotlib.style.use('bmh')
    matplotlib.rcParams.update(params)
    # matplotlib.style.use('seaborn-paper')
    # matplotlib.style.use('seaborn-dark-palette')

    matplotlib.rc('axes', facecolor='white')
    matplotlib.rc('grid', linestyle='-', alpha=0.0)
    # matplotlib.lines.lineStyles
    # markers=[',', '+', '-', '.', 'o', '*']
    # matplotlib.lines.lineMarkers
    # matplotlib.rcParams
