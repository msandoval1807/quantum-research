# shared/ — reusable code for every assignment

Modules placed here can be imported from **any** notebook in this repository — in any assignment folder — without copying the file around.

## How it works

A small file named `quantum_research_shared.pth` lives in the virtual environment's
site-packages folder (`.venv/Lib/site-packages/`). It contains the absolute path to this
`shared/` folder. Python reads `.pth` files automatically at startup and adds the listed
folder to its import path, so anything in `shared/` becomes importable everywhere in the
project's `.venv`.

A notebook in any assignment can therefore simply do:

```python
from oscillator import setup
setup()
```

and it resolves to `shared/oscillator.py`, no matter which assignment folder the
notebook is saved in.

## Important

After the `.pth` file is created or changed, **restart the Jupyter kernel** (Kernel →
Restart) so Python re-reads it. The `.pth` only takes effect at interpreter startup.

## Adding more shared code later

Drop a new `.py` file in this folder and import it the same way. For example, a future
`quantum_helpers.py` would be used as:

```python
from quantum_helpers import some_function
```

## Files

- `oscillator.py` — the main module the notebooks import. Provides **`setup()`** (one call = group plot style + output routing) plus reusable physics helpers: `energy(x, p)`, `hamilton_rhs(t, state)`, `analytic_xp(t, x0, p0)`, `build_operators(N)`, and `wigner_gif(states, tlist, fname, …)`.

  **Run it directly to verify it:**

  ```
  python shared/oscillator.py
  ```

  It checks four things against exact formulas and prints `PASS`: the numerical solver against the
  analytic classical solution, energy conservation along a trajectory, the Wigner colour-scale
  invariant, and the quantum spectrum against `Eₙ = ℏω(n+½)`. Run it after touching this file.

  Two details in `wigner_gif` that are easy to get wrong and are deliberate: the colour scale is
  fixed across frames by passing an explicit `np.linspace(-wmax, wmax, 81)` level array — an integer
  `levels` makes matplotlib ignore `vmin`/`vmax` and rescale every frame — and `duration` is in
  **milliseconds** (imageio ≥ 2.28).
- `group_plot_style.py` — the group's matplotlib plotting standards; call `apply_group_style()` once near the top of a notebook. (`setup()` calls this for you.)
- `output_routing.py` — auto-sorts saved files into `figures/`, `data/`, `movies/` by file type. Call `route_outputs()` once (or just use `setup()`, which calls it):

  ```python
  from output_routing import route_outputs
  route_outputs()
  ```

  After that, `plt.savefig("x.png")` lands in `figures/`, `np.save("x", arr)` in `data/`, `imageio.mimsave("x.gif", ...)` in `movies/` — without editing any save lines. Works in every assignment folder.

## Portability note

The `.pth` file lives inside `.venv/`, which is not committed to git. If this repo is ever
cloned onto another computer, recreate it once: put a file `quantum_research_shared.pth`
in that machine's `.venv/Lib/site-packages/` containing the absolute path to this `shared/`
folder. (The notebooks also keep an inline fallback style, so plotting still works even if
the `.pth` is missing.)
