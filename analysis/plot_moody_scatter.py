"""

Plot Moody diagram using Colebrook equation

"""

import numpy as np

from scipy.optimize import newton
from scipy import interpolate

from matplotlib import pyplot as plt
import netCDF4 as nc

import defaults

# pattern = '../glads/00_shmip_forcing_shmip_topo/RUN/output_%03d_seasonal.nc'
# cases = [201, 202, 203, 204, 205]

# pattern = '../glads/_00_shmip_forcing_shmip_topo/RUN/output_%03d_seasonal.nc'
# cases = [1, 2, 3, 4, 5]


models = ['Turbulent 5/4', 'Turbulent 3/2', 'Laminar', 'Transition 5/4', 'Transition 3/2']

def plot_moody(fnames, figname, colors=defaults.colors, omega=1/2000,
    nu=1.79e-6, k_lam=0.1, h_0=0.5, rhow=1000, models=models):

    # fig, ax_scatter = plt.subplots()
    fig, (ax_theory, ax_scatter) = plt.subplots(figsize=(7, 3.5), nrows=1, ncols=2)


    # Define Roughnesses
    # eps_d = np.logspace(-4, -1, 7)
    eps_d = np.array([1e-3, 5e-3,
            1e-2, 2e-2, 5e-2, 1e-1, 2e-1, 5e-1])

    eps_d_label_indices = [0, 2, 5, 7]
    eps_d_labels = [r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$0.5$']

    # Reynolds number for computation
    Re = np.logspace(3 + 0, 8, 101)

    # Compute friction factor as function of Re
    darcy_friction = np.zeros((len(eps_d), len(Re)))
    for ii in range(len(eps_d)):
        eps = eps_d[ii]
        x0 = -2*np.log10(eps/3.7)*np.ones(Re.shape)

        obj = lambda x: x + 2*np.log10(2.51*x/Re + eps/3.7)
        ff = newton(obj, x0)

        friction = 1/ff**2
        darcy_friction[ii] = friction

    Re_laminar = np.logspace(2, 3, 21)
    laminar_friction = 64/Re_laminar

    Re_transition = np.logspace(3, 3 + np.log10(3), 5)
    laminar_transition = 64/Re_transition

    # fig, ax_theory = plt.subplots(figsize=(8, 6))
    ax_theory.loglog(Re, darcy_friction.T, color='k')
    ax_theory.loglog(Re_laminar, laminar_friction, color='k')
    ax_theory.loglog(Re_transition, laminar_transition, color='k', linestyle='--')
    ax_theory.grid(linestyle=':')

    ax_theory.set_yticks(list(np.arange(1e-2, 1e-1, 1e-2/2)) + list(np.arange(1e-1, 1e0 + 1e-1/2, 1e-1/2)))
    ax_theory.set_ylim([1e-2, 1e0])
    ax_theory.set_xlim([Re_laminar[0], Re[-1]])

    ax_theory.fill_betweenx([1e-2, 1e0], [1000, 1000], [3000, 3000], facecolor='grey', alpha=0.7, zorder=10)

    ax_theory.set_xlabel(r'$\rm{Re} = \frac{VD}{\nu}$')
    ax_theory.set_ylabel(r'Friction factor $f_{\rm{D}}$', labelpad=0)# = \frac{h_{\rm{f}}}{\left(\frac{L}{D}\right) \frac{V^2}{2g}}$')
    ax_theory.text(-0.2, 1, 'a', transform=ax_theory.transAxes, fontweight='bold')

    ax_right = ax_theory.twinx()
    ax_right.set_ylim(ax_theory.get_ylim())
    ax_right.set_yscale('log')

    ax_right.set_yticks(darcy_friction[eps_d_label_indices, -1])
    ax_right.set_yticklabels(eps_d_labels)
    ax_right.set_ylabel(r'Roughness $\frac{\epsilon}{D}$', labelpad=0)


    for ii in range(len(fnames)):
        out = nc.Dataset(fnames[ii], 'r')

        # Read parameters
        k = out['para/cond_s'][:].data

        h = out['h_sheet'][:].data.T
        qxy = out['qs'][:].data.T
        qs = np.sqrt(qxy[:, 0]**2 + qxy[:, 1]**2)
        Re = qs/nu
        nodes = out['nodes'][:].data.T
        elements = out['elements'][:].data.T
        h_node = out['h_sheet'][:].data.T
        interpolator = interpolate.LinearNDInterpolator(nodes, h_node)
        hs = interpolator(elements)
        
        if models[ii]=='Turbulent 5/4':
            gradphi = (qs/k/hs**(5/4))**2

            h_bed = float(out['para/h_bed'][:].data)
            max_f_D = h_bed**0.5 / rhow / k**2
        elif models[ii]=='Turbulent 3/2':
            gradphi = (qs/k/hs**(3/2))**2
        elif models[ii]=='Laminar':
            gradphi = (qs/k/hs**(3))**1
        elif models[ii]=='Transition 5/4':
            h_bed = float(out['para/h_bed'][:].data)
            gradphi = ((qs + omega/nu * (hs/h_bed)**(1/2) * qs**2)/k/hs**(3))**1
        elif models[ii]=='Transition 3/2':
            gradphi = ((qs + omega/nu * qs**2)/k/hs**(3))**1

        f_D = hs**3*gradphi/rhow/Re**2/nu**2

        step = 5
        f_D = f_D[::step, ::step].flatten()
        Re = Re[::step, ::step].flatten()

        ax_scatter.scatter(Re.flatten(), f_D.flatten(), color=colors[ii], label=models[ii], s=0.5, alpha=0.5, zorder=10)

    ax_scatter.set_xscale('log')
    ax_scatter.set_yscale('log')
    ax_scatter.set_xlim([1e-3, 1e5])

    ax_scatter.grid(linestyle=':', zorder=0)

    ax_scatter.set_xlabel(r'${\rm{Re}} = \frac{q}{\nu}$')
    # ax_scatter.set_ylabel(r'$f_{\rm{D}} = \frac{h^3 |\nabla \phi|}{\rho_{\rm{w}} \nu^2 {\rm{Re}}^2}$', fontsize=12)
    ax_scatter.set_ylabel(r'Friction factor $f_{\rm{D}}$', labelpad=0)
    # ax_scatter.legend(markerscale=5, loc='upper right', framealpha=1, edgecolor='none')
    ax_scatter.text(-0.2, 1, 'b', transform=ax_scatter.transAxes, fontweight='bold')

    ax_scatter.legend(bbox_to_anchor=[0.1, 0.78, 0.8, 0.2],
        ncol=2, mode='expand', borderaxespad=0.05, frameon=True, borderpad=0,
        markerscale=5, handletextpad=0.1, handlelength=1,
        facecolor=(1, 1, 1, 0.5), edgecolor='none', fancybox=False, fontsize=8)

    fig.subplots_adjust(wspace=0.45, bottom=0.15, left=0.09, right=0.97, top=0.95)
    ax_scatter.set_ylim([1e-2, 1e9])
    ax_theory.tick_params(labelsize=8)
    ax_scatter.tick_params(labelsize=8)
    ax_right.tick_params(labelsize=8)

    # ax_scatter.legend(bbox_to_anchor=[-0.125, 1.02, 1.125, 0.102], loc='lower left',
    #     ncol=2, mode='expand', borderaxespad=0.05, frameon=False, borderpad=0,
    #     markerscale=5)
    # fig.subplots_adjust(wspace=0.6, bottom=0.2, left=0.1, right=0.95, top=0.8)


    ax_scatter.axvline(1/omega, color='k', linewidth=1)
    # ax_scatter.axhline(max_f_D, color='k', linewidth=1)
    # plt.tight_layout()

    fig.savefig(figname, dpi=600)

# plt.show()

if __name__=='__main__':
    cases = [1, 2, 3, 4, 5]
    fnames = ['../glads/00_synth_forcing/RUN/output_%03d_seasonal.nc'%caseid for caseid in cases]
    models = ['Turbulent 5/4', 'Turbulent 3/2', 'Laminar', 'Transition 5/4', 'Transition 3/2']
    figname = '00_moody_composite_scatter.png'
    plot_moody(fnames, figname, models=models)

    cases = [1, 2, 3, 4, 5]
    fnames = ['../glads/01_kan_forcing/RUN/output_%03d_seasonal.nc'%caseid for caseid in cases]
    models = ['Turbulent 5/4', 'Turbulent 3/2', 'Laminar', 'Transition 5/4', 'Transition 3/2']
    figname = '01_moody_composite_scatter.png'
    plot_moody(fnames, figname, models=models)