"""

Call plot_pressure_maps_timeseries.py to make pressure figures

"""

import numpy as np
from matplotlib import pyplot as plt

from plot_pressure_maps_separate_timeseries import plot_pressure_maps_timeseries
import defaults

t_ticks = [1 + 4/12, 1 + 6/12, 1 + 8/12, 1 + 10/12]
# t_ticklabels = ['4', '6', '8', '10']
t_ticklabels = ['May', 'July', 'Sep', 'Nov']
t_lim = [t_ticks[0], t_ticks[-1]]
t_xlabel = 'Month'
"""
## Case 00: Flat topo, synthetic forcing
cases = [1, 2, 3, 4, 5]
fnames = ['../glads/00_synth_forcing/RUN/output_%03d_seasonal.nc'%caseid for caseid in cases]
figname = '00_pressure_seasonal.png'
fig_00 = plot_pressure_maps_timeseries(fnames, figname, melt_forcing='SHMIPadj', Qmin=1, Qmax=100,
    t_ticklabels=t_ticklabels[:-1], t_xlabel=t_xlabel, t_ticks=t_ticks[:-1], t_lim=[1 + 3/12, 1 + 9/12])

plt.show()

## Case 00a: Flat topo, standard SHMIP forcing
cases = [1, 2, 3, 4, 5]
fnames = ['../glads/00a_shmip_forcing/RUN/output_%03d_seasonal.nc'%caseid for caseid in cases]
figname = '00_pressure_seasonal_shmip_forcing.png'
fig_00 = plot_pressure_maps_timeseries(fnames, figname, Qmin=10, Qmax=200, melt_forcing='SHMIP',
    t_ticklabels=t_ticklabels[:-1], t_xlabel=t_xlabel, t_ticks=t_ticks[:-1], t_lim=[1 + 3/12, 1 + 9/12])

"""
## Case 00b: Flat topo, higher basal melt rate
cases = [1, 2, 3, 4, 5]
fnames = ['../glads/00b_synth_forcing_winter/RUN/output_%03d_seasonal.nc'%caseid for caseid in cases]
figname = '00b_pressure_seasonal.png'
fig_00 = plot_pressure_maps_timeseries(fnames, figname, melt_forcing='SHMIPadj', Qmin=1, Qmax=100,
    t_ticklabels=t_ticklabels[:-1], t_xlabel=t_xlabel, t_ticks=t_ticks[:-1], t_lim=[1 + 3/12, 1 + 9/12])

"""
## Case 01: Flat topo, KAN_L forcing
cases = [1, 2, 3, 4, 5]
pattern = '../glads/01_kan_forcing/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '01_pressure_seasonal.png'
fig_01 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, Qmax=100, melt_forcing='KAN',
     t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
     ff_ylim=[0, 1.75], ff_yticks=[0, 0.5, 1, 1.5])
"""

"""
## Case 01: Flat topo, higher alpha
cases = [3, 6, 2, 4, 5]
pattern = '../glads/01_kan_forcing/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '01_pressure_seasonal_alpha.png'
labels = ['Laminar 3', 'Laminar 4', 'Turbulent 3/2', 'Transition 5/4', 'Transition 3/2']
colors = np.zeros((5, 4))
colors[0] = defaults.colors[2]
# colors[1] = np.array([0.51, 0.21, 0.71, 1])
colors[1] = np.array([0.2, 0.15, 0.8, 1])
colors[2] = defaults.colors[1]
colors[3:] = defaults.colors[3:]
lws = [0.75, 1.25, 1.25, 2.5, 1.25]
zorders = [5, 2, 2, 2, 2]
lss = ['dashed', 'solid', 'solid', 'solid', 'solid']
fig_01 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, Qmax=100, melt_forcing='KAN',
     t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
     ff_ylim=[0, 1.75], ff_yticks=[0, 0.5, 1, 1.5], labels=labels,
     lws=lws, linestyles=lss, colors=colors, zorders=zorders)

plt.show()
"""
"""
## Case 01a: KAN increased forcing
cases = [1, 2, 3, 4, 5]
pattern = '../glads/01a_kan_adj_forcing/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname ='01a_pressure_seasonal.png'
fig_01 = plot_pressure_maps_timeseries(fnames, figname, Qmin=10, Qmax=200, melt_forcing='KANadj',
     t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
     ff_ylim=[0, 2.25], ff_yticks=[0, 0.5, 1, 1.5, 2])

## Case 01b: Flat topo, KAN_L forcing, reduced e_v
cases = [1, 2, 3, 4, 5]
pattern = '../glads/01b_kan_forcing_ev/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '01b_pressure_seasonal_ev.png'
fig_01 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, Qmax=100, melt_forcing='KAN',
     t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
     ff_ylim=[0, 2.25], ff_yticks=[0, 0.5, 1, 1.5, 2])
"""

"""
## Case 01c: KAN with diurnals
cases = [1, 2, 3, 4, 4]
pattern = '../glads/01c_kan_diurnal/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '01c_pressure_diurnal.png'
doy = defaults.tslice;
tstep = 145 + (doy-145)*6 + 4
fig_01 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, Qmax=100, melt_forcing='KAN',
     t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim, tslice=tstep,
     ff_ylim=[0, 2.25], ff_yticks=[0, 0.5, 1, 1.5, 2])
"""

"""
## Case 02a: Trough topo, synthetic forcing
cases = [1, 2, 3, 4, 5]
pattern = '../glads/02a_synth_forcing_trough/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '02a_pressure_seasonal_trough.png'
fig_02 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, Qmax=100, melt_forcing='SHMIPadj',
    t_ticklabels=t_ticklabels[:-1], t_xlabel=t_xlabel, t_ticks=t_ticks[:-1], t_lim=[1+3/12, 1+9/12],
    ff_ylim=[0,1.75], ff_yticks=[0, 0.5, 1, 1.5])

## Case 02b: Valley topo, synthetic
cases = [1, 2, 3, 4, 5]
pattern = '../glads/02b_synth_forcing_valley/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '02b_pressure_seasonal_valley.png'
fig_02 = plot_pressure_maps_timeseries(fnames, figname, Qmin=10, Qmax=200, melt_forcing='SHMIPadj',
    t_ticklabels=t_ticklabels[:-1], t_xlabel=t_xlabel, t_ticks=t_ticks[:-1], t_lim=[1+3/12, 1+9/12],
    ff_ylim=[0,1.75], ff_yticks=[0, 0.5, 1, 1.5])

## Case 03a: Trough topo, KAN forcing
cases = [1, 2, 3, 4, 5]
pattern = '../glads/03a_kan_forcing_trough/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '03a_pressure_seasonal_trough.png'
fig_03 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, melt_forcing='KAN',
    t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
    ff_ylim=[0,1.75], ff_yticks=[0, 0.5, 1, 1.5])

## Case 03b: Valley topo, KAN forcing
cases = [1, 2, 3, 4, 5]
pattern = '../glads/03b_kan_forcing_valley/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '03b_pressure_seasonal_valley.png'
fig_03 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, melt_forcing='KAN',
    t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
    ff_ylim=[0,1.75], ff_yticks=[0, 0.5, 1, 1.5])

"""
cases = [1, 2, 3, 4, 5]
pattern = '../glads/_dev_03c_kan_forcing_trough2/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '03c_pressure_seasonal_trough2.png'
fig_03c = plot_pressure_maps_timeseries(fnames, figname, Qmin=10, Qmax=200, melt_forcing='SHMIPadj',
    t_ticklabels=t_ticklabels[:-1], t_xlabel=t_xlabel, t_ticks=t_ticks[:-1], t_lim=[1+3/12, 1+9/12],
    ff_ylim=[0,1.75], ff_yticks=[0, 0.5, 1, 1.5])

"""

## Case S01: Parameter sensitivity
cases = [1, 2, 3, 4, 5]
pattern = '../glads/S01a_parameter_sensitivity/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = 'S01_pressure_seasonal_params.png'
fig_01 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, Qmax=100, melt_forcing='KAN',
     t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
     ff_ylim=[0, 1.75], ff_yticks=[0, 0.5, 1, 1.5])

## Case S01: Parameter sensitivity
cases = [1, 2, 3, 4, 5]
pattern = '../glads/S01b_parameter_sensitivity/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = 'S01b_pressure_seasonal_params.png'
fig_01 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, Qmax=100, melt_forcing='KAN',
     t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim,
     ff_ylim=[0, 1.75], ff_yticks=[0, 0.5, 1, 1.5])
"""
