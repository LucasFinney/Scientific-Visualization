# Scientific-Visualization

A collection of scripts for programmatic graphs and scientific visualizations, primarily used in BoosterPrep lectures.

Tools used: Python, Mathematica, and whatever else is relevant.

## hydrogen_orbitals.py
====================
Generates 2D cross-sectional plots of the electron probability density
|ψ_nlm(x, 0, z)|² for hydrogen-like atoms.

The plots show the xz-plane (y = 0).  Because the φ-dependence of ψ_nlm
is a pure phase factor (e^{imφ}), the probability density |ψ|² is the
same on every half-plane containing the z-axis — so this cross-section
is representative of the full 3D density.

All lengths are in Bohr radii (a₀).  Atomic units are used throughout
(a₀ = 1, ℏ = 1, mₑ = 1).
