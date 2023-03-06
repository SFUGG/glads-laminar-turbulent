"""

Call plot_pressure_maps_timeseries.py to make pressure figures

"""

from matplotlib import pyplot as plt

from plot_pressure_maps_timeseries import plot_pressure_maps_timeseries

t_ticks = [1 + 4/12, 1 + 6/12, 1 + 8/12, 1 + 10/12]
t_ticklabels = ['4', '6', '8', '10']
t_lim = [t_ticks[0], t_ticks[-1]]
t_xlabel = 'Month'

## Case 00: Flat topo, SHMIP forcing
cases = [1, 2, 3, 4, 5]
fnames = ['../glads/_00_shmip_forcing_shmip_topo/RUN/output_%03d_seasonal.nc'%caseid for caseid in cases]
figname = '00_pressure_seasonal.png'
fig_00 = plot_pressure_maps_timeseries(fnames, figname, Qmin=1, melt_forcing='SHMIP',
    t_ticklabels=t_ticklabels[:-1], t_xlabel=t_xlabel, t_ticks=t_ticks[:-1], t_lim=[1 + 3/12, 1 + 9/12])

## Case 01: Flat topo, KAN_L forcing
KAN_tslice = 569
cases = [101, 102, 103, 104, 105]
pattern = '../glads/01_kan_l_forcing_shmip_topo/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '01_pressure_seasonal.png'
fig_01 = plot_pressure_maps_timeseries(fnames, figname, tslice=KAN_tslice, Qmin=1, melt_forcing='KAN',
    t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim)

## Case 03: Trough topo, KAN_L forcing
cases = [101, 102, 103, 104, 105]
pattern = '../glads/03_kan_l_forcing_synth_topo/RUN/output_%03d_seasonal.nc'
fnames = [pattern % caseid for caseid in cases]
figname = '03_pressure_seasonal.png'
fig_03 = plot_pressure_maps_timeseries(fnames, figname, tslice=KAN_tslice, Qmin=1, melt_forcing='KAN',
    t_ticklabels=t_ticklabels, t_xlabel=t_xlabel, t_ticks=t_ticks, t_lim=t_lim)

plt.show()
