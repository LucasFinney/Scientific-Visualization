#!/usr/bin/env python3
"""
hydrogen_orbitals.py
====================
Generates 2D cross-sectional plots of the electron probability density
|ψ_nlm(x, 0, z)|² for hydrogen-like atoms.

The plots show the xz-plane (y = 0).  Because the φ-dependence of ψ_nlm
is a pure phase factor (e^{imφ}), the probability density |ψ|² is the
same on every half-plane containing the z-axis — so this cross-section
is representative of the full 3D density.

All lengths are in Bohr radii (a₀).  Atomic units are used throughout
(a₀ = 1, ℏ = 1, mₑ = 1).

Usage
-----
    python hydrogen_orbitals.py              # default set of orbitals
    python hydrogen_orbitals.py --Z 2        # helium-like ion (He⁺)
    python hydrogen_orbitals.py --save       # save PNG instead of (or as well as) showing
    python hydrogen_orbitals.py --cmap magma --gamma 0.4
    python hydrogen_orbitals.py --help       # full option list

Dependencies
------------
    numpy, scipy, matplotlib
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import factorial, genlaguerre, sph_harm


# ---------------------------------------------------------------------------
# Wavefunction physics
# ---------------------------------------------------------------------------

def radial_wavefunction(n, l, r, Z=1):
    """Normalized radial wavefunction R_nl(r) for a hydrogen-like atom.

    Derived from the exact solution of the Schrödinger equation:

        R_nl(ρ) = N · e^{-ρ/2} · ρ^l · L_{n-l-1}^{2l+1}(ρ)

    where ρ = 2Zr/n and L_p^q is the generalized Laguerre polynomial.
    The normalization N is chosen so that ∫|R_nl|² r² dr = 1.

    Parameters
    ----------
    n : int
        Principal quantum number (n ≥ 1).
    l : int
        Azimuthal quantum number (0 ≤ l < n).
    r : array-like
        Radial distance(s) in Bohr radii (a₀).
    Z : int
        Nuclear charge (1 = hydrogen, 2 = He⁺, …).

    Returns
    -------
    ndarray
        R_nl(r).
    """
    r = np.asarray(r, dtype=float)
    rho = 2.0 * Z * r / n

    norm = np.sqrt(
        (2.0 * Z / n) ** 3
        * factorial(n - l - 1)
        / (2.0 * n * factorial(n + l))
    )

    L = genlaguerre(n - l - 1, 2 * l + 1)   # L_{n-l-1}^{2l+1}
    return norm * np.exp(-rho / 2.0) * rho**l * L(rho)


def prob_density_xz(n, l, m, extent, grid_size=600, Z=1):
    """Compute |ψ_nlm|² on a 2D grid covering the xz-plane.

    Parameters
    ----------
    n, l, m  : int    Quantum numbers.
    extent   : float  Half-width of the square grid in a₀.
    grid_size: int    Number of grid points along each axis.
    Z        : int    Nuclear charge.

    Returns
    -------
    x, z : 1D ndarray   Axis coordinates (a₀).
    prob : 2D ndarray   |ψ_nlm|² on the (z, x) grid (row = z, col = x).
    """
    x = np.linspace(-extent, extent, grid_size)
    z = np.linspace(-extent, extent, grid_size)
    X, Z_grid = np.meshgrid(x, z)

    r = np.sqrt(X**2 + Z_grid**2)

    # Polar angle θ: 0 at +z axis, π at −z axis.
    # np.clip guards against floating-point values just outside [−1, 1].
    theta = np.where(r > 0, np.arccos(np.clip(Z_grid / r, -1.0, 1.0)), 0.0)

    R = radial_wavefunction(n, l, r, Z)

    # scipy.special.sph_harm(m, l, azimuthal_angle, polar_angle)
    # — note scipy swaps the conventional θ/φ labels relative to physics.
    # Setting the azimuthal argument to 0 gives the xz cross-section.
    # The resulting |Y_l^m|² is the same for any azimuthal angle anyway.
    Y = sph_harm(m, l, 0.0, theta)

    return x, z, np.abs(R * Y) ** 2


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

_SUBSHELL = {0: 's', 1: 'p', 2: 'd', 3: 'f', 4: 'g'}


def _title(n, l, m):
    sub = _SUBSHELL.get(l, str(l))
    return rf'$n={n},\; \ell={l}\,({sub}),\; m={m}$'


def plot_orbital(ax, n, l, m, Z=1, grid_size=600, gamma=0.35, cmap='inferno'):
    """Render |ψ_nlm|² for one orbital onto *ax*.

    The density is normalized to its own peak before display so that the
    colorscale highlights structure rather than absolute magnitude.  A
    power-law (gamma) compression is then applied so that the diffuse
    outer lobes remain visible alongside the dense inner region.

    Parameters
    ----------
    ax       : matplotlib Axes
    n, l, m  : int    Quantum numbers.
    Z        : int    Nuclear charge.
    grid_size: int    Grid resolution.
    gamma    : float  Display exponent; < 1 compresses bright regions.
    cmap     : str    Matplotlib colormap name.
    """
    extent = 5.0 * n**2 / Z   # in a₀; captures the bulk of every orbital
    x, z, prob = prob_density_xz(n, l, m, extent, grid_size=grid_size, Z=Z)

    peak = prob.max()
    if peak > 0:
        prob = prob / peak

    ax.imshow(
        prob ** gamma,
        origin='lower',
        extent=[-extent, extent, -extent, extent],
        cmap=cmap,
        aspect='equal',
        interpolation='bilinear',
        vmin=0, vmax=1,
    )

    ax.set_title(_title(n, l, m), fontsize=10, pad=5)
    ax.set_xlabel(r'$x\;(a_0)$', fontsize=8)
    ax.set_ylabel(r'$z\;(a_0)$', fontsize=8)
    ax.tick_params(labelsize=7)
    # Faint crosshairs at the nucleus
    ax.axhline(0, color='white', lw=0.4, alpha=0.4)
    ax.axvline(0, color='white', lw=0.4, alpha=0.4)


def make_figure(orbitals, Z=1, grid_size=600, gamma=0.35,
                cmap='inferno', ncols=3):
    """Build and return a figure with one panel per orbital.

    Parameters
    ----------
    orbitals : list of (n, l, m) tuples
    Z        : int    Nuclear charge.
    grid_size: int    Grid resolution per panel.
    gamma    : float  Display gamma (< 1 compresses highlights).
    cmap     : str    Matplotlib colormap name.
    ncols    : int    Number of columns.

    Returns
    -------
    matplotlib Figure
    """
    nrows = (len(orbitals) + ncols - 1) // ncols
    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(3.8 * ncols, 3.8 * nrows),
        constrained_layout=True,
    )
    axes = np.asarray(axes).flatten()

    for ax, (n, l, m) in zip(axes, orbitals):
        plot_orbital(ax, n, l, m, Z=Z, grid_size=grid_size,
                     gamma=gamma, cmap=cmap)

    for ax in axes[len(orbitals):]:
        ax.set_visible(False)

    label = f'Z = {Z}' if Z != 1 else 'Hydrogen (Z = 1)'
    fig.suptitle(
        rf'Electron Probability Density $|\psi_{{n\ell m}}|^2$'
        f'\n{label} — xz cross-section, colour scaled per orbital',
        fontsize=12,
    )
    return fig


# ---------------------------------------------------------------------------
# Default orbital set
# ---------------------------------------------------------------------------

DEFAULT_ORBITALS = [
    (1, 0,  0),   # 1s
    (2, 0,  0),   # 2s
    (2, 1,  0),   # 2p, m=0  (lobes along z)
    (2, 1,  1),   # 2p, m=±1 (toroidal; same |ψ|² for m=−1)
    (3, 0,  0),   # 3s
    (3, 1,  0),   # 3p, m=0
    (3, 2,  0),   # 3d, m=0  (z² shape)
    (3, 2,  1),   # 3d, m=±1
    (3, 2,  2),   # 3d, m=±2
]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description='Plot hydrogen-like orbital probability densities.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument('--Z', type=int, default=1,
                   help='nuclear charge')
    p.add_argument('--cmap', default='inferno',
                   help='matplotlib colormap')
    p.add_argument('--gamma', type=float, default=0.35,
                   help='display gamma (< 1 compresses highlights)')
    p.add_argument('--grid', type=int, default=600,
                   help='grid resolution per panel')
    p.add_argument('--ncols', type=int, default=3,
                   help='number of columns in the figure')
    p.add_argument('--save', action='store_true',
                   help='save the figure to --outfile')
    p.add_argument('--outfile', default='hydrogen_orbitals.png',
                   help='output filename (used with --save)')
    p.add_argument('--dpi', type=int, default=150,
                   help='resolution of saved figure (used with --save)')
    return p.parse_args()


def main():
    args = parse_args()
    fig = make_figure(
        DEFAULT_ORBITALS,
        Z=args.Z,
        grid_size=args.grid,
        gamma=args.gamma,
        cmap=args.cmap,
        ncols=args.ncols,
    )
    if args.save:
        fig.savefig(args.outfile, dpi=args.dpi, bbox_inches='tight')
        print(f'Saved → {args.outfile}')
    plt.show()


if __name__ == '__main__':
    main()
