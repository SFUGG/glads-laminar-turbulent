"""
Plot floatation fraction for turbulent, laminar, and transition models

"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.tri import Triangulation
import netCDF4 as nc

import cmocean
from palettes.code import palettes, tools

import GladsPlot as gplt

# Define fnames
fname_pattern = '../RUN/output_%03d_seasonal.nc'
cases = [911, 912, 913]
n_cases = 3
figname = 'floatation_91X.png'

tslices = [int(1.5*365), 730-1]
tlabels = [1.5, 2]
n_times = len(tslices)

# Define the figure
fig = plt.figure(figsize=(8, 6))
gs = GridSpec(n_cases+2, n_times,
    wspace=0.1, hspace=0.05,
    left=0.1, right=0.95, top=0.9, bottom=0.1,
    height_ratios=([8] + n_cases*[100] + [150]),
    width_ratios=(100, 100))

axs = np.array([[fig.add_subplot(gs[i+1, j]) for j in range(n_times)] for i in range(n_cases)])
print(axs.shape)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f']

axs_scatter = np.array([fig.add_subplot(gs[n_cases+1, j]) for j in range(n_times)])
labels = ['Turbulent', 'Laminar', 'Transition']

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# Start reading the data
for ii in range(n_cases):
    fname = fname_pattern % cases[ii]
    print(fname)

    out = nc.Dataset(fname, 'r')
    nodes = out['nodes'][:].data.T
    connect = out['connect'][:].data.T.astype(int) - 1
    connect_edge = out['connect_edge'][:].data.T.astype(int) - 1

    Q = np.abs(out['Q'][tslices, :].data.T)

    phi = out['phi'][tslices, :].data.T
    N = out['N'][tslices, :].data.T
    
    phi_0 = 0
    pw = phi - phi_0
    ff = pw/(N + pw)

    mtri = Triangulation(nodes[:, 0]/1e3, nodes[:, 1]/1e3, connect)

    for jj in range(n_times):
        ax = axs[ii, jj]
        fcolor = ax.tripcolor(mtri, ff[:, jj], cmap=cmocean.cm.dense, vmin=0, vmax=1)
        ax.set_aspect('equal')
        ax.set_xlim([0, 100])
        ax.set_ylim([0, 25])
        ax.set_yticks([0, 12.5, 25])

        lc = gplt.plot_edge_data(nodes/1e3, connect_edge, Q[:, jj],
            palettes.get_cmap('BrownYellow'), vmin=10, vmax=100)
        ax.add_collection(lc)
        
        if ii==0:
            ax.text(95, 23, 't = %s a' % tlabels[jj], ha='right', color='w',
                fontweight='bold', va='top')
        if jj==1:
            ax.text(95, 2, labels[ii], ha='right', color='w', fontweight='bold')

        if jj==1:
            ax.set_yticklabels([])

        if ii<n_cases:
            ax.set_xticklabels([])
        
        ax.text(-0.05, 1.05, alphabet[ii*n_times + jj], transform=ax.transAxes, fontweight='bold')
        
        axs_scatter[jj].scatter(nodes[:, 0]/1e3, ff[:, jj], 5, alpha=0.5, color=colors[ii],
            label=labels[ii])
        axs_scatter[jj].set_ylim([0, 1])
        axs_scatter[jj].set_xlim([0, 100])
        axs_scatter[jj].grid()

        if ii==0:
            axs_scatter[jj].set_xlabel('x (km)')

axs_scatter[0].legend(markerscale=3)
axs_scatter[0].set_ylabel(r'$p_{\rm{w}}/p_{\rm{i}}$')

axs_scatter[1].set_yticklabels([])

cax2 = fig.add_subplot(gs[0, 0])
cax1 = fig.add_subplot(gs[0, 1])

fig.colorbar(fcolor, cax=cax1, orientation='horizontal')
fig.colorbar(lc, cax=cax2, orientation='horizontal', extend='both')

cax1.xaxis.tick_top()
cax1.xaxis.set_label_position('top')

cax2.set_xticks([10, 20, 40, 60, 80, 100])

cax2.xaxis.tick_top()
cax2.xaxis.set_label_position('top')

cax1.set_xlabel(r'$p_{\rm{w}}/p_{\rm{i}}$')
cax2.set_xlabel(r'$Q~(\rm{m}^3~\rm{s}^{-1})$')

fig.savefig(figname, dpi=600)
plt.show()
