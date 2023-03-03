"""

Plot floatation fraction maps and timeseries

"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib.tri import Triangulation
import netCDF4 as nc

import cmocean
from palettes.code import palettes, tools

import GladsPlot as gplt

import helpers
import defaults


figsize=(7, 6)

gs_kwargs=dict(wspace=0.05, hspace=0.2, 
        width_ratios = (100, 30, 115), 
        left=0.1, right=0.97, bottom=0.08)



def plot_pressure_maps_timeseries(fnames, figname, tslice=defaults.tslice, 
    x_bands=defaults.x_bands, band_width=defaults.band_width, 
    figsize=figsize, gs_kwargs=gs_kwargs, labels=defaults.labels, 
    colors=defaults.colors, map_cmap=defaults.cmaps['floatation'],
    line_cmap=defaults.cmaps['Q'], Qmin=10, Qmax=100,
    tlim=[1, 2], t_ticks=[1.0, 1.25, 1.5, 1.75, 2], ff_ylim=[0, 1.5],
    melt_forcing='SHMIP', fill_between=False):
    """
    Plot 2D floatation fraction maps and timeseries.

    [More description]

    Inputs:
    --------
    fnames : Iterable of str
        List of paths to model outputs for a simulation case
    
    figname : str
        Path to save figure
    
    Options:
    --------
    tslice : int
        Time index for 2D pressure maps
    
    x_bands : Array-like of floats
        x distances in km for timeseries. Timeseries are computed for mean
        floatation fraction in bands [xb-band_width/2, xb+band_width/2]
        for xb in x_bands.
    
    band_width : float
        Width of bands for band-averaging
    
    figsize : (width, height) = (6, 7)
        Tuple in inches of figure size. 
    
    gs_Kwargs : dict
        Dictionary of options passed to gridspec.GridSpec for global config
    
    labels : list of str
        List of strings specifying labels for legend
    
    colors : (M, 3) or (M, 4) array-like of rgb or rgba values

    map_cmap : LinearSegmentedColormap 
        Colormap object for tripcolor panels
    
    line_cmap : LinearSegmentedColormap
        Colormap object for plotting channel discharge
    
    Qmin, Qmax : float
        Min and max discharge for channel discharge colorbar
    
    tlim : (tmin, tmax)
        x-axis bounds for timeseries panels
    
    t_ticks : Array-like
        x-axis ticks for timeseries panels

    ff_ylim : (ymin, ymax) for ff panels
    
    Returns:
    --------
        fig : matplotlib figure object
    
    """ 
    ## CONFIG

    n_cases = len(fnames)

    # Sort out melt forcing
    if melt_forcing=='SHMIP':
        tt_temp = np.loadtxt('../../data/AWS_GEUS/KAN_L_2014_temp_clipped.txt', delimiter=',')
        tt_days = tt_temp[:, 0]
        temp_sl = tt_temp[:, 1]
        temp_fun = lambda t: np.interp(t, tt_days/365, temp_sl, left=0, right=0)
    elif melt_forcing=='KAN':
        temp_fun = lambda t: -16*np.cos(2*np.pi*t) - 5

    ## Start the figure
    fig = plt.figure(figsize=figsize)

    # A global gridspec giving two columns to work with
    global_gs = gridspec.GridSpec(1, 3, **gs_kwargs)

    # Left column: 3 timeseries panels
    gs_timeseries = gridspec.GridSpecFromSubplotSpec(len(x_bands), 1, 
        subplot_spec=global_gs[:, 2])

    # Right column: 5 maps with space for colorbars
    hratios = 100*np.ones(n_cases+2)
    hratios[0] = 8
    hratios[-1] = 150
    gs_maps = gridspec.GridSpecFromSubplotSpec(n_cases+2, 2, 
        subplot_spec=global_gs[:, 0], width_ratios=(100, 5), height_ratios=hratios,
        hspace=0.04, wspace=0.1)

    # Initialize axes
    axs_timeseries = np.array([fig.add_subplot(gs_timeseries[i, 0]) for i in range(len(x_bands))])
    axs_maps = np.array([fig.add_subplot(gs_maps[i+1, 0]) for i in range(n_cases)])
    ax_scatter = fig.add_subplot(gs_maps[-1, 0])

    # Set style for panel labels
    time_alphabet = ['g', 'h', 'i']
    map_alphabet = ['a', 'b', 'c', 'd', 'e', 'f']
    text_args = {'fontweight':'bold'}

    # Start reading the data
    for ii in range(n_cases):
        fname = fnames[ii]
        print(fname)

        out = nc.Dataset(fname, 'r')
        nodes = out['nodes'][:].data.T
        connect = out['connect'][:].data.T.astype(int) - 1
        connect_edge = out['connect_edge'][:].data.T.astype(int) - 1

        # Channel fields
        Q = np.abs(out['Q'][:, :].data.T)

        # Get floatation fraction
        phi = out['phi'][:, :].data.T
        N = out['N'][:, :].data.T
        phi_0 = 9.81*1000*np.vstack(out['bed'][:].data)
        pw = phi - phi_0
        ff = pw/(N + pw)

        tt = out['time'][:].data/86400/365 - 100

        # Initialize triangulation for faster plotting
        mtri = Triangulation(nodes[:, 0]/1e3, nodes[:, 1]/1e3, connect)
        
        # Map panel
        mapax = axs_maps[ii]
        fcolor = mapax.tripcolor(mtri, ff[:, tslice], cmap=map_cmap, vmin=0, vmax=1)
        mapax.set_aspect('equal')
        mapax.set_xlim([0, 100])
        mapax.set_ylim([0, 25])
        mapax.set_yticks([0, 12.5, 25])

        lc = gplt.plot_edge_data(nodes/1e3, connect_edge, Q[:, tslice],
            line_cmap, vmin=Qmin, vmax=Qmax)
        mapax.add_collection(lc)

        if ii<n_cases:
            mapax.set_xticklabels([])
        
        mapax.text(0.025, 0.95, map_alphabet[ii], transform=mapax.transAxes,
            va='top', ha='left', **text_args)
        xmid, ff_avg = helpers.width_average(nodes, ff[:, tslice])

        quantile_95 = lambda x: np.quantile(x, 0.95)
        _, ff_upper= helpers.width_average(nodes, ff[:, tslice], metric=lambda x: np.quantile(x, 0.975))
        _, ff_lower = helpers.width_average(nodes, ff[:, tslice], metric=lambda x: np.quantile(x, 0.025))

        if fill_between:
            ax_scatter.fill_between(xmid/1e3, ff_lower, ff_upper, facecolor=colors[ii], alpha=0.33,
                edgecolor=None)
        ax_scatter.plot(xmid/1e3, ff_avg, color=colors[ii], label=labels[ii])
        ax_scatter.set_ylim(ff_ylim)
        ax_scatter.set_xlim([0, 100])
        ax_scatter.grid()

        if ii==0:
            ax_scatter.set_xlabel('x (km)')

        # Timeseries
        for j, xb in enumerate(x_bands):
            xmin = xb - band_width/2
            xmax = xb + band_width/2
            node_mask = np.logical_and(nodes[:, 0]/1e3>=xmin, nodes[:, 0]/1e3<xmax)
            f_mean = np.mean(ff[node_mask, :], axis=0)
            f_lower = np.quantile(ff[node_mask, :], 0.025, axis=0)
            f_upper = np.quantile(ff[node_mask, :], 0.975, axis=0)
            timeax = axs_timeseries[j]

            if fill_between:
                timeax.fill_between(tt, f_lower, f_upper, facecolor=colors[ii], alpha=0.3)

            timeax.plot(tt, f_mean, label=labels[ii], color=colors[ii], linewidth=1)

            mapax.axvline(xb, color='w', linewidth=0.5)
            timeax.axvline(tslice/365, color='k', linewidth=0.5)

            timeax.text(0.025, 0.95, time_alphabet[j], transform=timeax.transAxes,
            va='top', ha='left', **text_args)

            if melt_forcing:
                melt = temp_fun(tt)
                ax_right = timeax.twinx()
                ax_right.plot(tt, melt, color='k', linewidth=0.5)

            timeax.set_zorder(3)
            ax_right.set_zorder(2)
            timeax.patch.set_visible(False)



    ax_scatter.set_ylabel(r'$p_{\rm{w}}/p_{\rm{i}}$')
    ax_scatter.text(0.025, 0.95, map_alphabet[n_cases], transform=ax_scatter.transAxes,
        va='top', ha='left', **text_args)

    axs_maps[2].set_ylabel('y (km)')

    cax1 = fig.add_subplot(gs_maps[1:6, 1])
    cax2 = fig.add_subplot(gs_maps[0, 0])

    fig.colorbar(fcolor, cax=cax1, extend='max')
    fig.colorbar(lc, cax=cax2, orientation='horizontal', extend='both')

    cax1.xaxis.tick_top()
    cax1.xaxis.set_label_position('top')

    cax2.set_xticks([Qmin, 20, 40, 60, 80, 100])

    cax2.xaxis.tick_top()
    cax2.xaxis.set_label_position('top')

    cax1.text(0, 1.1, r'$p_{\rm{w}}/p_{\rm{i}}$', transform=cax1.transAxes)
    cax2.set_xlabel(r'$Q~(\rm{m}^3~\rm{s}^{-1})$')

    axs_timeseries[0].legend(bbox_to_anchor=[0, 1.02, 1., 0.102], loc='lower left',
        ncol=2, mode='expand', borderaxespad=0.05, frameon=False, borderpad=0)
    for j, xb in enumerate(x_bands):
        axi = axs_timeseries[j]
        if j<len(x_bands)-1:
            axi.set_xticklabels([])
        axi.set_xlim(tlim)
        axi.set_ylim(ff_ylim)
        axi.set_xticks(t_ticks)
        axi.grid()

    axs_timeseries[-1].set_xlabel('Time (a)')
    axs_timeseries[1].set_ylabel(r'$p_{\rm{w}}/p_{\rm{i}}$')

    fig.savefig(figname, dpi=600)
    return fig
