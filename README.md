# Scientific-Visualization

A collection of scripts for programmatic graphs and scientific visualizations, primarily used in BoosterPrep lectures.

Tools used: Python, Mathematica, and whatever else is relevant.

---

## Scripts

### Hydrogen-like Atom Orbitals

**Dependencies:** `numpy`, `scipy`, `matplotlib`

#### `hydrogen_orbitals.py` — Static multi-panel figure

Generates a publication-ready figure of electron probability densities |ψ_nlm|² in the xz cross-section, grouped by principal quantum number n (one row per n, centred):

```
Row 1 (n=1):  1s
Row 2 (n=2):  2s   2p(m=0)   2p(m=1)
Row 3 (n=3):  3s   3p(m=0)   3p(m=1)   3d(m=0)   3d(m=1)   3d(m=2)
```

```bash
python hydrogen_orbitals.py              # display
python hydrogen_orbitals.py --save       # save to hydrogen_orbitals.png
python hydrogen_orbitals.py --Z 2        # helium-like ion (He⁺)
python hydrogen_orbitals.py --cmap magma --gamma 0.4
python hydrogen_orbitals.py --help       # full option list
```

#### `hydrogen_orbitals_interactive.py` — Interactive viewer

Dark-themed GUI with live controls. Adjust any parameter and the plot updates instantly.

| Control | Range | Description |
|---------|-------|-------------|
| n | 1 – 4 | Principal quantum number |
| ℓ | 0 – n−1 | Azimuthal quantum number (range updates with n) |
| m | −ℓ – +ℓ | Magnetic quantum number (range updates with ℓ) |
| Z | 1 – 20 | Nuclear charge (1 = H, 2 = He⁺, …) |
| γ | 0.1 – 1.0 | Display gamma — lower values reveal diffuse outer lobes |
| Colormap | — | inferno / plasma / viridis / magma / hot |

```bash
python hydrogen_orbitals_interactive.py
```

> **Note:** Grid resolution is set by `GRID_SIZE` at the top of the file (default 300). Increase to 500–600 for higher-quality screenshots; decrease if updates feel sluggish.

#### `hydrogen_orbitals.html` — Zero-install web applet

The same interactive viewer reimplemented in pure HTML + JavaScript — no Python, no installation, no server. Open it directly in any browser, or share the URL if you enable GitHub Pages.

**To run locally:** just double-click the file (or drag it into a browser tab).

**To share via GitHub Pages:**
1. Go to your repo → **Settings → Pages**
2. Set source to **main branch, / (root)**
3. Link directly to `https://lucasfinney.github.io/Scientific-Visualization/hydrogen_orbitals.html`

All physics (Laguerre polynomials, associated Legendre polynomials, normalization) is implemented from scratch in JavaScript and rendered pixel-by-pixel into an HTML5 Canvas. Controls and behaviour are identical to the Python version.
