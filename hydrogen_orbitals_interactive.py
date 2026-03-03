#!/usr/bin/env python3
"""
hydrogen_orbitals_interactive.py
=================================
Interactive viewer for hydrogen-like atom orbital probability densities.

A dark-themed control panel (left) lets you adjust quantum numbers and
display settings; the orbital cross-section (right) updates instantly.

Controls
--------
  n, ℓ, m  Integer sliders.  ℓ is clamped to [0, n−1] and m to [0, ℓ]
            automatically when you reduce n or ℓ.
  Z        Nuclear charge (1 = H, 2 = He⁺, …).
  γ        Display gamma: < 1 compresses the colour scale so diffuse
            outer lobes stay visible.  Try 0.2–0.5 for most orbitals.
  Colormap Radio buttons for five perceptually-uniform palettes.

Performance note
----------------
  GRID_SIZE controls the plot resolution.  300 is comfortable on most
  machines; raise it to 500–600 for high-quality screenshots.

Usage
-----
    python hydrogen_orbitals_interactive.py

Dependencies
------------
    numpy, scipy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from scipy.special import factorial, genlaguerre, sph_harm

# ── tuneable ─────────────────────────────────────────────────────────────────
GRID_SIZE = 300       # grid points per axis; raise for higher quality

# ── colour palette ────────────────────────────────────────────────────────────
PANEL_BG  = '#0f1017'
PANEL_FG  = '#d8ddf0'
ACCENT    = '#7eb8f7'
DIM       = '#505570'
SLIDER_C  = '#1e4070'
SEP_CLR   = '#1e2030'

CMAPS = ['inferno', 'plasma', 'viridis', 'magma', 'hot']

# ── subshell labels ───────────────────────────────────────────────────────────
SUBSHELL = {0: 's', 1: 'p', 2: 'd', 3: 'f', 4: 'g'}


# ──────────────────────────────────────────────────────────────────────────────
# Physics  (same normalisation as hydrogen_orbitals.py)
# ──────────────────────────────────────────────────────────────────────────────

def radial_wavefunction(n, l, r, Z=1):
    """Normalised radial wavefunction R_nl(r) in atomic units (a₀ = 1)."""
    r = np.asarray(r, dtype=float)
    rho = 2.0 * Z * r / n
    norm = np.sqrt(
        (2.0 * Z / n) ** 3
        * factorial(n - l - 1)
        / (2.0 * n * factorial(n + l))
    )
    L = genlaguerre(n - l - 1, 2 * l + 1)
    return norm * np.exp(-rho / 2.0) * rho**l * L(rho)


def prob_density_xz(n, l, m, extent, Z=1):
    """Return |ψ_nlm|² on a GRID_SIZE × GRID_SIZE grid in the xz-plane."""
    x = np.linspace(-extent, extent, GRID_SIZE)
    z = np.linspace(-extent, extent, GRID_SIZE)
    X, Zg = np.meshgrid(x, z)
    r = np.sqrt(X**2 + Zg**2)
    theta = np.where(r > 0, np.arccos(np.clip(Zg / r, -1.0, 1.0)), 0.0)
    R = radial_wavefunction(n, l, r, Z)
    Y = sph_harm(m, l, 0.0, theta)
    return np.abs(R * Y) ** 2


# ──────────────────────────────────────────────────────────────────────────────
# Figure & control-panel layout
# ──────────────────────────────────────────────────────────────────────────────

plt.style.use('dark_background')

fig = plt.figure(figsize=(13, 8), facecolor=PANEL_BG)
try:
    fig.canvas.manager.set_window_title('Hydrogen-like Orbital Viewer')
except AttributeError:
    pass

# ── control-panel cosmetic backdrop ──────────────────────────────────────────
ax_panel = fig.add_axes([0.0, 0.0, 0.215, 1.0])
ax_panel.set_facecolor(PANEL_BG)
ax_panel.set_xticks([]); ax_panel.set_yticks([])
for sp in ax_panel.spines.values():
    sp.set_visible(False)
# right-edge separator line
ax_panel.plot([1, 1], [0, 1], color=SEP_CLR, lw=2,
              transform=ax_panel.transAxes, clip_on=False)

# ── header text ──────────────────────────────────────────────────────────────
fig.text(0.107, 0.965, 'Hydrogen-like\nOrbital Viewer',
         ha='center', va='top', fontsize=12, fontweight='bold',
         color=ACCENT, family='monospace')

fig.text(0.107, 0.880,
         r'$|\psi_{n\,\ell\,m}|^2$ — xz cross-section',
         ha='center', va='top', fontsize=8, color=DIM)

# ── divider helper ────────────────────────────────────────────────────────────
def _hdivider(y):
    """Draw a faint horizontal rule across the control panel."""
    fig.add_artist(plt.Line2D([0.008, 0.207], [y, y],
                              transform=fig.transFigure,
                              color=SEP_CLR, lw=1, zorder=5))

_hdivider(0.850)

# ── section label helper ──────────────────────────────────────────────────────
def _section(y, text):
    fig.text(0.018, y, text, fontsize=6.5, color=DIM,
             fontweight='bold', va='top', family='monospace')

_section(0.838, 'QUANTUM NUMBERS')

# ── integer sliders ───────────────────────────────────────────────────────────
_skw = dict(color=SLIDER_C)    # bar fill colour; compatible with all mpl versions

def _make_slider(rect, label, lo, hi, init, step=None):
    ax = fig.add_axes(rect)
    ax.set_facecolor('#161824')
    kw = dict(**_skw)
    if step is not None:
        kw['valstep'] = step
    s = Slider(ax, label, lo, hi, valinit=init, **kw)
    s.label.set_color(PANEL_FG);  s.label.set_fontsize(9.5)
    s.valtext.set_color(ACCENT);  s.valtext.set_fontsize(9.5)
    return s

# n, ℓ, m — quantum numbers
# ℓ and m start with range [0, 0] matching the initial n=1, ℓ=0 state.
# Their ranges expand automatically as n and ℓ are increased.
s_n = _make_slider([0.030, 0.778, 0.165, 0.030], 'n',  1,  4, 1, step=1)
s_l = _make_slider([0.030, 0.710, 0.165, 0.030], 'ℓ',  0,  0, 0, step=1)
s_m = _make_slider([0.030, 0.642, 0.165, 0.030], 'm',  0,  0, 0, step=1)

_hdivider(0.615)
_section(0.603, 'ATOM')

# Z — nuclear charge
s_Z = _make_slider([0.030, 0.540, 0.165, 0.030], 'Z',  1, 20, 1, step=1)

_hdivider(0.513)
_section(0.501, 'DISPLAY')

# γ — brightness/gamma compression
s_gm = _make_slider([0.030, 0.437, 0.165, 0.030], 'γ', 0.10, 1.0, 0.35)

_hdivider(0.408)
_section(0.396, 'COLORMAP')

# ── colormap radio buttons ────────────────────────────────────────────────────
ax_radio = fig.add_axes([0.020, 0.200, 0.180, 0.190])
ax_radio.set_facecolor(PANEL_BG)
for sp in ax_radio.spines.values():
    sp.set_visible(False)

radio = RadioButtons(ax_radio, CMAPS, active=0, activecolor=ACCENT)
for lbl in radio.labels:
    lbl.set_fontsize(9)
    lbl.set_color(PANEL_FG)

_hdivider(0.196)

# ── current-orbital readout ───────────────────────────────────────────────────
fig.text(0.107, 0.100, 'Current orbital',
         ha='center', va='top', fontsize=7, color=DIM)
state_text = fig.text(0.107, 0.073, '1s   m = 0',
                      ha='center', va='top',
                      fontsize=13, color=ACCENT,
                      family='monospace', fontweight='bold')


# ──────────────────────────────────────────────────────────────────────────────
# Main plot
# ──────────────────────────────────────────────────────────────────────────────

ax = fig.add_axes([0.250, 0.075, 0.690, 0.890])
ax.set_facecolor('#07080f')

# Seed imshow with a placeholder; real data filled in replot()
im = ax.imshow(np.zeros((2, 2)), origin='lower', aspect='equal',
               interpolation='bilinear', cmap='inferno', vmin=0, vmax=1)

ax.set_xlabel(r'$x\ (a_0)$', fontsize=10, color=PANEL_FG, labelpad=6)
ax.set_ylabel(r'$z\ (a_0)$', fontsize=10, color=PANEL_FG, labelpad=6)
ax.tick_params(colors=PANEL_FG, labelsize=8)
for sp in ax.spines.values():
    sp.set_edgecolor(SEP_CLR)

# Faint crosshairs at the nucleus
ax.axhline(0, color='white', lw=0.6, alpha=0.20)
ax.axvline(0, color='white', lw=0.6, alpha=0.20)

plot_title = ax.set_title('', fontsize=12, color=PANEL_FG, pad=10)

cbar = fig.colorbar(im, ax=ax, fraction=0.028, pad=0.018)
cbar.set_label('Relative probability density  (γ-scaled)',
               fontsize=7.5, color=DIM, labelpad=8)
cbar.ax.tick_params(colors=DIM, labelsize=7)


# ──────────────────────────────────────────────────────────────────────────────
# Update logic
# ──────────────────────────────────────────────────────────────────────────────

_busy = False   # re-entrancy guard: set_val() triggers on_changed recursively


def _set_slider_range(s, lo, hi):
    """Update a Slider's valid range and clamp its current value.

    Matplotlib's Slider doesn't expose a public API for resizing after
    construction, but the three attributes below are all it uses internally.
    A tiny epsilon is added when lo == hi so the slider track never has
    zero width (which would cause a division-by-zero in the draw path).
    """
    eps = 0.01 if lo == hi else 0.0
    s.valmin = lo
    s.valmax = hi + eps
    s.ax.set_xlim(lo - eps, hi + eps)
    s.set_val(int(np.clip(s.val, lo, hi)))


def replot():
    """Recompute and redraw the orbital for the current slider values."""
    n  = int(s_n.val)
    l  = int(s_l.val)
    m  = int(s_m.val)
    Z  = int(s_Z.val)
    gm = float(s_gm.val)
    cmap = radio.value_selected

    extent = 5.0 * n**2 / Z    # a₀ — generous but compact

    prob = prob_density_xz(n, l, m, extent, Z=Z)
    peak = prob.max()
    if peak > 0:
        prob = prob / peak      # normalise to own peak

    im.set_data(prob ** gm)
    im.set_extent([-extent, extent, -extent, extent])
    im.set_cmap(cmap)
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)

    sub    = SUBSHELL.get(l, str(l))
    z_sfx  = f'  —  Z = {Z}' if Z != 1 else ''
    plot_title.set_text(
        rf'$|\psi_{{{n},{l},{m}}}|^2$   ({n}{sub},  m = {m}){z_sfx}'
    )
    state_text.set_text(f'{n}{sub}   m = {m}')
    fig.canvas.draw_idle()


def on_n_changed(val):
    """Resize ℓ to [0, n−1] and m to [−ℓ, +ℓ], then replot."""
    global _busy
    if _busy:
        return
    _busy = True
    n = int(s_n.val)
    _set_slider_range(s_l, 0, n - 1)
    l = int(s_l.val)
    _set_slider_range(s_m, -l, l)
    _busy = False
    replot()


def on_l_changed(val):
    """Resize m to [−ℓ, +ℓ], then replot."""
    global _busy
    if _busy:
        return
    _busy = True
    l = int(s_l.val)
    _set_slider_range(s_m, -l, l)
    _busy = False
    replot()


def on_any_changed(val):
    """Generic handler for sliders/radio that have no inter-dependencies."""
    if _busy:
        return
    replot()


s_n.on_changed(on_n_changed)
s_l.on_changed(on_l_changed)
s_m.on_changed(on_any_changed)
s_Z.on_changed(on_any_changed)
s_gm.on_changed(on_any_changed)
radio.on_clicked(on_any_changed)

replot()      # draw the initial 1s orbital
plt.show()
