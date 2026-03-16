#!/usr/bin/env python3
"""
mirror_ray_tracing.py
=====================
Interactive ray-tracing diagram for plane, concave, and convex mirrors.

A dark-themed control panel (left) lets you choose the mirror type and
adjust object distance, object height, and focal length; the ray diagram
(right) updates instantly, showing principal rays, the image, and key
optical points (F, C).

Ray-tracing rules (paraxial approximation)
------------------------------------------
  Concave (converging) mirror, f > 0:
      1. Parallel ray → reflects through F
      2. Focal ray (through F) → reflects parallel
      3. Centre ray (through C) → reflects back on itself

  Convex (diverging) mirror, f < 0:
      1. Parallel ray → reflects as if diverging from virtual F
      2. Ray aimed at virtual F → reflects parallel
      3. Ray aimed at virtual C → reflects back on itself

  Plane mirror:
      Angle of incidence = angle of reflection.
      Image is always virtual, upright, same size, at equal distance behind.

Mirror equation:  1/f = 1/dₒ + 1/dᵢ

Usage
-----
    python mirror_ray_tracing.py

Dependencies
------------
    numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# ── colour palette ────────────────────────────────────────────────────────────
PANEL_BG  = '#0f1017'
PANEL_FG  = '#d8ddf0'
ACCENT    = '#7eb8f7'
DIM       = '#505570'
SLIDER_C  = '#1e4070'
SEP_CLR   = '#1e2030'

RAY_COLORS = ['#ff6b6b', '#4ecdc4', '#ffe66d']  # parallel, focal, centre
OBJ_CLR    = '#7eb8f7'
IMG_REAL   = '#f07878'
IMG_VIRT   = '#c084fc'
MIRROR_CLR = '#8899bb'

# ── physics ───────────────────────────────────────────────────────────────────

def compute_image(do, f, mirror_type):
    """Return image distance dᵢ, magnification M, and descriptors.

    Sign convention (distances measured from mirror surface):
      - dₒ > 0 always (real object in front of mirror)
      - dᵢ > 0 → real image (in front of mirror)
      - dᵢ < 0 → virtual image (behind mirror)
      - f > 0 for concave, f < 0 for convex
    """
    if mirror_type == 'Plane':
        return dict(di=-do, M=1.0, real=False, inverted=False)

    if abs(do - f) < 0.15:
        return dict(di=float('inf'), M=float('inf'), real=False, inverted=False)

    di = (f * do) / (do - f)
    M  = -di / do
    real     = di > 0
    inverted = M < 0
    return dict(di=di, M=M, real=real, inverted=inverted)


def mirror_arc(f, mirror_type, h):
    """Return (x, y) arrays for drawing the mirror surface.

    h is the half-height of the mirror.
    """
    y = np.linspace(-h, h, 200)
    if mirror_type == 'Plane':
        return np.zeros_like(y), y
    R = 2.0 * abs(f)
    y_clip = np.clip(y, -R + 0.01, R - 0.01)
    sag = R - np.sqrt(R**2 - y_clip**2)
    if mirror_type == 'Concave':
        return sag, y        # opens toward negative x (toward object)
    else:  # Convex
        return -sag, y       # opens toward positive x (behind mirror)


# ──────────────────────────────────────────────────────────────────────────────
# Figure & control-panel layout
# ──────────────────────────────────────────────────────────────────────────────

plt.style.use('dark_background')

fig = plt.figure(figsize=(13, 8), facecolor=PANEL_BG)
try:
    fig.canvas.manager.set_window_title('Mirror Ray Tracing')
except AttributeError:
    pass

# ── control-panel backdrop ────────────────────────────────────────────────────
ax_panel = fig.add_axes([0.0, 0.0, 0.215, 1.0])
ax_panel.set_facecolor(PANEL_BG)
ax_panel.set_xticks([]); ax_panel.set_yticks([])
for sp in ax_panel.spines.values():
    sp.set_visible(False)
ax_panel.plot([1, 1], [0, 1], color=SEP_CLR, lw=2,
              transform=ax_panel.transAxes, clip_on=False)

# ── header ────────────────────────────────────────────────────────────────────
fig.text(0.107, 0.965, 'Mirror\nRay Tracing',
         ha='center', va='top', fontsize=12, fontweight='bold',
         color=ACCENT, family='monospace')

fig.text(0.107, 0.890,
         'Interactive optics diagram',
         ha='center', va='top', fontsize=8, color=DIM)

# ── helpers ───────────────────────────────────────────────────────────────────
def _hdivider(y):
    fig.add_artist(plt.Line2D([0.008, 0.207], [y, y],
                              transform=fig.transFigure,
                              color=SEP_CLR, lw=1, zorder=5))

def _section(y, text):
    fig.text(0.018, y, text, fontsize=6.5, color=DIM,
             fontweight='bold', va='top', family='monospace')

_skw = dict(color=SLIDER_C)

def _make_slider(rect, label, lo, hi, init, step=None):
    ax_s = fig.add_axes(rect)
    ax_s.set_facecolor('#161824')
    kw = dict(**_skw)
    if step is not None:
        kw['valstep'] = step
    s = Slider(ax_s, label, lo, hi, valinit=init, **kw)
    s.label.set_color(PANEL_FG);  s.label.set_fontsize(9.5)
    s.valtext.set_color(ACCENT);  s.valtext.set_fontsize(9.5)
    return s

# ── mirror type ───────────────────────────────────────────────────────────────
_hdivider(0.860)
_section(0.848, 'MIRROR TYPE')

ax_radio = fig.add_axes([0.020, 0.720, 0.180, 0.120])
ax_radio.set_facecolor(PANEL_BG)
for sp in ax_radio.spines.values():
    sp.set_visible(False)

radio = RadioButtons(ax_radio, ['Concave', 'Convex', 'Plane'],
                     active=0, activecolor=ACCENT)
for lbl in radio.labels:
    lbl.set_fontsize(9)
    lbl.set_color(PANEL_FG)

# ── parameter sliders ────────────────────────────────────────────────────────
_hdivider(0.700)
_section(0.688, 'PARAMETERS')

s_do = _make_slider([0.055, 0.635, 0.140, 0.030], r'$d_o$',  1, 30, 12, step=0.5)
s_ho = _make_slider([0.055, 0.580, 0.140, 0.030], r'$h_o$',  0.5, 5, 2, step=0.25)
s_f  = _make_slider([0.055, 0.525, 0.140, 0.030], r'$f$',    2, 15, 5, step=0.5)

# ── image properties info ────────────────────────────────────────────────────
_hdivider(0.495)
_section(0.483, 'IMAGE PROPERTIES')

info_text = fig.text(0.024, 0.450, '', fontsize=8.5, color=PANEL_FG,
                     va='top', family='monospace', linespacing=1.6)

# ── equation readout ─────────────────────────────────────────────────────────
_hdivider(0.250)
_section(0.238, 'MIRROR EQUATION')

eq_text = fig.text(0.107, 0.200, '', ha='center', va='top',
                   fontsize=9, color=ACCENT, family='monospace')


# ──────────────────────────────────────────────────────────────────────────────
# Main plot axes
# ──────────────────────────────────────────────────────────────────────────────

ax = fig.add_axes([0.280, 0.08, 0.680, 0.870])
ax.set_facecolor('#07080f')
ax.set_xlabel('Distance (arbitrary units)', fontsize=9, color=PANEL_FG, labelpad=6)
ax.set_ylabel('Height', fontsize=9, color=PANEL_FG, labelpad=6)
ax.tick_params(colors=PANEL_FG, labelsize=8)
for sp in ax.spines.values():
    sp.set_edgecolor(SEP_CLR)


# ──────────────────────────────────────────────────────────────────────────────
# Drawing logic
# ──────────────────────────────────────────────────────────────────────────────

_busy = False


def _arrow(x, y0, y1, color, ls='-', lw=2.0):
    """Draw a vertical arrow from (x, y0) to (x, y1)."""
    dy = y1 - y0
    if abs(dy) < 0.01:
        return
    hw = max(0.15, abs(dy) * 0.08)
    hl = max(0.25, abs(dy) * 0.12)
    ax.annotate('', xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, linestyle=ls,
                                mutation_scale=15))


def _draw_hatch(mirror_x, y_arr, mirror_type):
    """Draw hatch marks on the non-reflecting side of the mirror."""
    n_marks = 12
    idx = np.linspace(0, len(y_arr) - 1, n_marks, dtype=int)
    for i in idx:
        y0 = y_arr[i]
        mx = mirror_x[i] if hasattr(mirror_x, '__len__') else mirror_x
        hlen = 0.4
        if mirror_type == 'Convex':
            ax.plot([mx - hlen, mx], [y0 - hlen * 0.5, y0 + hlen * 0.5],
                    color=MIRROR_CLR, lw=0.7, alpha=0.5)
        else:  # Concave or Plane — hatch on right (behind mirror)
            ax.plot([mx, mx + hlen], [y0 - hlen * 0.5, y0 + hlen * 0.5],
                    color=MIRROR_CLR, lw=0.7, alpha=0.5)


def draw_diagram():
    """Clear and redraw the entire ray diagram."""
    ax.cla()
    ax.set_facecolor('#07080f')
    ax.tick_params(colors=PANEL_FG, labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor(SEP_CLR)

    mirror_type = radio.value_selected
    do = float(s_do.val)
    ho = float(s_ho.val)
    f  = float(s_f.val)

    # Adjust f sign for convex
    f_signed = f if mirror_type == 'Concave' else -f

    img = compute_image(do, f_signed, mirror_type)
    di = img['di']
    M  = img['M']

    # ── determine view bounds ─────────────────────────────────────────────
    x_obj = -do
    mirror_h = ho * 1.8

    if mirror_type == 'Plane':
        x_img = do  # behind mirror (positive x)
        hi = ho
        x_min = x_obj - 3
        x_max = x_img + 3
    elif abs(di) == float('inf'):
        hi = 0
        x_img = None
        x_min = x_obj - 3
        x_max = abs(2 * f) + 5
    else:
        hi = M * ho  # signed: negative if inverted
        if di > 0:
            x_img = -di  # real image, same side as object
        else:
            x_img = abs(di)  # virtual image, behind mirror
        x_min = min(x_obj, -2 * f if mirror_type == 'Concave' else 0,
                    x_img if x_img is not None else 0) - 3
        x_max = max(0, 2 * f if mirror_type == 'Convex' else 0,
                    x_img if x_img is not None else 0) + 3

    y_bound = max(abs(ho), abs(hi) if hi != 0 else ho, mirror_h) + 2
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-y_bound, y_bound)
    ax.set_aspect('equal', adjustable='datalim')

    # ── principal axis ────────────────────────────────────────────────────
    ax.axhline(0, color='white', lw=0.6, alpha=0.20)

    # ── mirror surface ────────────────────────────────────────────────────
    mx, my = mirror_arc(f, mirror_type, mirror_h)
    ax.plot(mx, my, color=MIRROR_CLR, lw=3, solid_capstyle='round')
    _draw_hatch(mx, my, mirror_type)

    # ── F and C markers ───────────────────────────────────────────────────
    if mirror_type != 'Plane':
        if mirror_type == 'Concave':
            xF, xC = -f, -2 * f
        else:
            xF, xC = f, 2 * f
        ax.plot(xF, 0, 'o', color=ACCENT, ms=6, zorder=5)
        ax.text(xF, -0.8, 'F', ha='center', va='top',
                color=ACCENT, fontsize=10, fontweight='bold')
        ax.plot(xC, 0, 's', color=DIM, ms=5, zorder=5)
        ax.text(xC, -0.8, 'C', ha='center', va='top',
                color=DIM, fontsize=10, fontweight='bold')

    # ── object arrow ──────────────────────────────────────────────────────
    _arrow(x_obj, 0, ho, OBJ_CLR)
    ax.plot(x_obj, 0, 'o', color=OBJ_CLR, ms=4)
    ax.text(x_obj, ho + 0.4, 'Object', ha='center', va='bottom',
            color=OBJ_CLR, fontsize=8)

    # ── draw rays ─────────────────────────────────────────────────────────
    _draw_rays(do, ho, f, f_signed, di, hi, mirror_type, x_img)

    # ── image arrow ───────────────────────────────────────────────────────
    if x_img is not None and abs(di) != float('inf'):
        is_virtual = not img['real']
        clr = IMG_VIRT if is_virtual else IMG_REAL
        ls  = '--' if is_virtual else '-'
        _arrow(x_img, 0, hi, clr, ls=ls)
        ax.plot(x_img, 0, 'o', color=clr, ms=4)
        label = 'Virtual\nimage' if is_virtual else 'Real\nimage'
        y_label = hi + (0.5 if hi >= 0 else -0.5)
        va = 'bottom' if hi >= 0 else 'top'
        ax.text(x_img, y_label, label, ha='center', va=va,
                color=clr, fontsize=7.5)

    # ── title ─────────────────────────────────────────────────────────────
    ax.set_title(f'{mirror_type} Mirror — Ray Diagram',
                 fontsize=12, color=PANEL_FG, pad=10)

    # ── update info text ──────────────────────────────────────────────────
    _update_info(img, mirror_type, do)

    fig.canvas.draw_idle()


def _draw_rays(do, ho, f, f_signed, di, hi, mirror_type, x_img):
    """Draw the principal rays on the diagram."""
    x_obj = -do
    tip = (x_obj, ho)  # top of object

    if mirror_type == 'Plane':
        _draw_plane_rays(do, ho)
        return

    is_concave = mirror_type == 'Concave'

    # Focal and centre positions on the axis
    if is_concave:
        xF, xC = -f, -2 * f
    else:
        xF, xC = f, 2 * f  # behind mirror (virtual)

    # ── Ray 1: Parallel ray ───────────────────────────────────────────────
    # Incoming: horizontal from object tip to mirror
    ax.plot([x_obj, 0], [ho, ho], color=RAY_COLORS[0], lw=1.5, zorder=3)
    # Arrowhead on incoming
    ax.annotate('', xy=(0, ho), xytext=(x_obj, ho),
                arrowprops=dict(arrowstyle='->', color=RAY_COLORS[0],
                                lw=0, mutation_scale=12))

    if is_concave:
        # Reflects through F: from (0, ho) toward (-f, 0) and beyond
        if abs(do - f) < 0.15:
            # Object at F → reflected ray is parallel (horizontal)
            ax.plot([0, x_obj - 5], [ho, ho], color=RAY_COLORS[0],
                    lw=1.5, zorder=3)
        else:
            dx = xF - 0
            dy = 0 - ho
            t_end = 3.0  # extend well past F
            x_end = 0 + dx * t_end
            y_end = ho + dy * t_end
            ax.plot([0, x_end], [ho, y_end], color=RAY_COLORS[0],
                    lw=1.5, zorder=3)
    else:
        # Convex: reflects as if diverging from virtual F behind mirror
        # Direction: from virtual F (xF, 0) through reflection point (0, ho)
        dx = 0 - xF
        dy = ho - 0
        t_end = 3.0
        x_end = 0 + dx * t_end / np.sqrt(dx**2 + dy**2) * max(do, f) * 1.5
        y_end = ho + dy * t_end / np.sqrt(dx**2 + dy**2) * max(do, f) * 1.5
        ax.plot([0, x_end], [ho, y_end], color=RAY_COLORS[0],
                lw=1.5, zorder=3)
        # Dashed extension behind mirror toward virtual F
        ax.plot([0, xF], [ho, 0], color=RAY_COLORS[0],
                lw=1.0, ls='--', alpha=0.5, zorder=2)

    # ── Ray 2: Focal ray ─────────────────────────────────────────────────
    if is_concave:
        if abs(do - f) < 0.15:
            # Object at F → ray through F to mirror; reflects parallel
            ax.plot([x_obj, 0], [ho, 0], color=RAY_COLORS[1],
                    lw=1.5, zorder=3)
            ax.plot([0, x_obj - 5], [0, 0], color=RAY_COLORS[1],
                    lw=1.5, zorder=3, alpha=0.7)
        else:
            # Ray from object tip through F to mirror
            # Find where ray from tip toward F hits the mirror (x=0)
            dx_tf = xF - x_obj
            dy_tf = 0 - ho
            if abs(dx_tf) > 0.01:
                t_mirror = (0 - x_obj) / dx_tf
                y_at_mirror = ho + dy_tf * t_mirror
            else:
                y_at_mirror = ho

            ax.plot([x_obj, 0], [ho, y_at_mirror], color=RAY_COLORS[1],
                    lw=1.5, zorder=3)
            # Reflects parallel (horizontal) from mirror
            ax.plot([0, x_obj - 5], [y_at_mirror, y_at_mirror],
                    color=RAY_COLORS[1], lw=1.5, zorder=3)
    else:
        # Convex: ray aimed at virtual F behind mirror
        # Incoming: from tip toward virtual F
        dx_tf = xF - x_obj
        dy_tf = 0 - ho
        if abs(dx_tf) > 0.01:
            t_mirror = (0 - x_obj) / dx_tf
            y_at_mirror = ho + dy_tf * t_mirror
        else:
            y_at_mirror = ho

        ax.plot([x_obj, 0], [ho, y_at_mirror], color=RAY_COLORS[1],
                lw=1.5, zorder=3)
        # Reflects parallel (horizontal) away from mirror
        ax.plot([0, -(do + 5)], [y_at_mirror, y_at_mirror],
                color=RAY_COLORS[1], lw=1.5, zorder=3)
        # Dashed extension behind mirror toward virtual F
        ax.plot([0, xF], [y_at_mirror, 0], color=RAY_COLORS[1],
                lw=1.0, ls='--', alpha=0.5, zorder=2)

    # ── Ray 3: Centre ray (through C) ────────────────────────────────────
    if is_concave:
        # From tip through C to mirror, reflects back on itself
        dx_tc = xC - x_obj
        dy_tc = 0 - ho
        if abs(dx_tc) > 0.01:
            t_mirror = (0 - x_obj) / dx_tc
            y_at_mirror = ho + dy_tc * t_mirror
        else:
            y_at_mirror = ho

        ax.plot([x_obj, 0], [ho, y_at_mirror], color=RAY_COLORS[2],
                lw=1.5, zorder=3)
        # Reflects back on itself — same line back
        t_back = 3.0
        x_back = 0 + (x_obj - 0) * t_back
        y_back = y_at_mirror + (ho - y_at_mirror) * t_back
        ax.plot([0, x_back], [y_at_mirror, y_back], color=RAY_COLORS[2],
                lw=1.5, zorder=3)
    else:
        # Convex: ray aimed at virtual C behind mirror
        dx_tc = xC - x_obj
        dy_tc = 0 - ho
        if abs(dx_tc) > 0.01:
            t_mirror = (0 - x_obj) / dx_tc
            y_at_mirror = ho + dy_tc * t_mirror
        else:
            y_at_mirror = ho

        ax.plot([x_obj, 0], [ho, y_at_mirror], color=RAY_COLORS[2],
                lw=1.5, zorder=3)
        # Reflects back on itself
        t_back = 3.0
        x_back = 0 + (x_obj - 0) * t_back
        y_back = y_at_mirror + (ho - y_at_mirror) * t_back
        ax.plot([0, x_back], [y_at_mirror, y_back], color=RAY_COLORS[2],
                lw=1.5, zorder=3)
        # Dashed extension behind mirror toward virtual C
        ax.plot([0, xC], [y_at_mirror, 0], color=RAY_COLORS[2],
                lw=1.0, ls='--', alpha=0.5, zorder=2)

    # ── Virtual ray extensions for concave virtual image (do < f) ─────────
    if is_concave and do < f and abs(do - f) >= 0.15:
        # Extend reflected rays backward (behind mirror) as dashed lines
        # to show virtual image location
        if x_img is not None:
            # Ray 1 backward: from (0, ho) extend reflected direction behind mirror
            dx1 = xF - 0
            dy1 = 0 - ho
            norm1 = np.sqrt(dx1**2 + dy1**2)
            if norm1 > 0:
                # The reflected ray goes toward (xF, 0) and beyond — but for
                # virtual image, it diverges. Extend backward (opposite direction).
                ax.plot([0, -dx1 * 2.5 / norm1 * f + 0],
                        [ho, -dy1 * 2.5 / norm1 * f + ho],
                        color=RAY_COLORS[0], lw=1.0, ls='--', alpha=0.5, zorder=2)

            # Ray 2 backward: from (0, y_at_mirror_ray2), the horizontal
            # ray extended behind mirror
            # (already drawn as solid going left; dashed behind mirror = right)
            pass  # horizontal ray already visible


def _draw_plane_rays(do, ho):
    """Draw rays for a plane mirror."""
    x_obj = -do
    x_img = do  # virtual image behind mirror

    # Ray 1: perpendicular to mirror (horizontal)
    ax.plot([x_obj, 0], [ho, ho], color=RAY_COLORS[0], lw=1.5, zorder=3)
    ax.plot([0, x_obj - 3], [ho, ho], color=RAY_COLORS[0], lw=1.5, zorder=3)
    ax.plot([0, x_img], [ho, ho], color=RAY_COLORS[0],
            lw=1.0, ls='--', alpha=0.5, zorder=2)

    # Ray 2: angled ray
    y_hit = 0  # hits mirror at axis level
    ax.plot([x_obj, 0], [ho, y_hit], color=RAY_COLORS[1], lw=1.5, zorder=3)
    # Reflected with equal angle (symmetric about normal = horizontal)
    ax.plot([0, x_obj - 3], [y_hit, -ho], color=RAY_COLORS[1],
            lw=1.5, zorder=3)
    # Virtual extension behind mirror
    ax.plot([0, x_img], [y_hit, ho], color=RAY_COLORS[1],
            lw=1.0, ls='--', alpha=0.5, zorder=2)

    # Ray 3: another angled ray at different angle
    y_hit2 = ho * 0.5
    ax.plot([x_obj, 0], [ho, y_hit2], color=RAY_COLORS[2], lw=1.5, zorder=3)
    # Reflect: incident angle relative to normal (horizontal)
    dy_in = y_hit2 - ho
    dy_out = -dy_in  # reflected angle
    t_ext = 2.5
    ax.plot([0, -do * t_ext], [y_hit2, y_hit2 + dy_out * t_ext],
            color=RAY_COLORS[2], lw=1.5, zorder=3)
    # Virtual extension behind mirror
    ax.plot([0, x_img], [y_hit2, ho], color=RAY_COLORS[2],
            lw=1.0, ls='--', alpha=0.5, zorder=2)


def _update_info(img, mirror_type, do):
    """Update the info text block and equation readout."""
    di = img['di']
    M  = img['M']

    if abs(di) == float('inf'):
        lines = [
            'Type:    --',
            'Orient:  --',
            'Size:    --',
            f'M:       \u221e',
            f'd\u1d62:      \u221e',
            '',
            'Object at focal point',
            'Image at infinity',
        ]
    else:
        typ    = 'Real' if img['real'] else 'Virtual'
        orient = 'Inverted' if img['inverted'] else 'Upright'
        absM   = abs(M)
        if abs(absM - 1.0) < 0.05:
            size = 'Same size'
        elif absM > 1.0:
            size = 'Magnified'
        else:
            size = 'Diminished'

        lines = [
            f'Type:    {typ}',
            f'Orient:  {orient}',
            f'Size:    {size}',
            f'M:       {M:+.2f}',
            f'd\u1d62:      {di:+.1f}',
        ]

    info_text.set_text('\n'.join(lines))

    # Equation readout
    if mirror_type == 'Plane':
        eq_text.set_text(f'd\u1d62 = d\u2092 = {do:.1f}')
    elif abs(di) == float('inf'):
        eq_text.set_text('1/f = 1/d\u2092 + 1/\u221e')
    else:
        f_val = img.get('_f', None)
        eq_text.set_text(f'1/d\u2092 + 1/d\u1d62 = 1/f\n'
                         f'{1/do:.3f} + {1/di:.3f} = {1/do + 1/di:.3f}')


# ──────────────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────────────

def on_any_changed(val):
    if _busy:
        return
    draw_diagram()

def on_mirror_changed(label):
    if _busy:
        return
    draw_diagram()


s_do.on_changed(on_any_changed)
s_ho.on_changed(on_any_changed)
s_f.on_changed(on_any_changed)
radio.on_clicked(on_mirror_changed)

draw_diagram()
plt.show()
