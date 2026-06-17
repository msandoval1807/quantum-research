# Code Walkthrough — Components 1 & 2

**Author:** Marcos Sandoval Lucas
**Project:** AI Design of Quantum Processors — Mondragon-Shem Quantum Group, UIC College of Engineering

This guide explains **every cell** of `component1_classical.ipynb` and `component2_quantum.ipynb` — what the text (markdown) is saying, what each line of code does, what every function means, *why* it's there, and how to read each plot. It assumes **no prior Python knowledge** and is meant to be read alongside the notebooks. It also documents the reusable code in the **`shared/` folder** that the notebooks import.

> **Sources & conventions.** The quantum physics matches the group's assigned text, **Essler's *Lecture Notes for Quantum Mechanics*** (cross-references appear in the companion `Classical_and_Quantum_Mechanics_Study_Guide.md`, Part 6; the hardware connection is its Part 7). All work is in **natural units** ℏ = m = ω = 1, which makes the numbers clean (energy levels come out 0.5, 1.5, 2.5, …).

---

## Part 0 — Crash course: how to read any of this code

Before the cells, here are the only ideas needed. Everything else is built from these.

**A notebook is made of cells.** Two kinds: *markdown cells* (formatted text and equations — the explanation) and *code cells* (Python that runs and shows its output/plots right below it). A cell is run with Shift+Enter; cells are run top to bottom.

**A variable is a labeled box.** `m = 1.0` means "make a box named `m` holding 1.0." Later, writing `m` means "whatever is in that box."

**A comment starts with `#`.** Everything after `#` on a line is a note for humans; Python ignores it.

**A function is a reusable machine.** It takes *inputs* in parentheses and gives back an *output*. Example: `energy(1.0, 0.0)` feeds 1.0 and 0.0 into the machine named `energy` and gets a result. We *define* our own with `def name(inputs):` and *call* ready-made ones from libraries.

**A library is a toolbox someone else wrote;** `import` brings it in. This project uses four standard ones plus its own helper files:

- **NumPy** (`np`) — fast math and arrays (long lists of numbers).
- **Matplotlib** (`plt`) — makes every plot.
- **SciPy** — scientific algorithms; we use `solve_ivp` (a differential-equation solver) for the classical motion.
- **QuTiP** — the quantum toolbox: operators, states, the Schrödinger solver, Wigner functions.
- **Project helper modules** in `shared/` — `oscillator`, `group_plot_style`, `output_routing`. These are *your own* reusable code, imported the same way as a library (e.g. `from oscillator import setup`). Part 1 below explains them.

**An array is a row/grid of numbers.** `np.linspace(-3, 3, 400)` makes 400 evenly spaced numbers from −3 to 3. Math on arrays happens to every number at once.

**Dot notation `a.b` means "the b belonging to a."** E.g. `sol.y` = the `y` data inside the result object `sol`; `a.dag()` = run the `dag` operation on operator `a`.

**`print(...)`** shows text/numbers. **`assert claim, "msg"`** is a safety check: "I claim this is true; stop with an error if it isn't." We use asserts as automatic sanity checks.

That's the whole vocabulary. Now the shared code, then the cells.

---

## Part 1 — The `shared/` helper modules

Both notebooks begin with one line:

```python
from oscillator import setup
setup()
```

`oscillator` is a file at `shared/oscillator.py`. The `shared/` folder is registered with the project's virtual environment, so anything in it can be imported from **any** assignment folder (see `shared/README.md`). There are three helper files:

### `group_plot_style.py` — `apply_group_style()`
Sets matplotlib's *default* settings once, so every plot automatically follows the group's standards without configuring each one. Calling it makes: larger fonts (legible on a slide), `viridis` as the default colormap, viridis-sampled line colors, thicker lines, a faint grid, and high resolution when saving. In short, a one-line "make all my plots consistent and slide-ready" switch.

### `output_routing.py` — `route_outputs()`
Makes saved files **sort themselves** into subfolders by file type, so nothing is left loose at the top level:

- `.png .jpg .pdf .svg` → `figures/`
- `.npy .npz .csv` → `data/`
- `.gif .mp4 .mov` → `movies/`

It does this by quietly wrapping `plt.savefig`, `np.save`, and `imageio.mimsave` so that a **bare** filename (like `"energy.png"`) gets the right folder prepended (→ `"figures/energy.png"`). A filename that already names a folder is left alone, and the folders are created automatically. So you never edit your save lines — they just land in the right place.

### `oscillator.py` — the physics + setup helpers
This is the file the notebooks import. It holds:

- **`setup()`** — calls `apply_group_style()` *and* `route_outputs()` together, so one line at the top of a notebook does all the styling and file-routing. This replaces the longer setup block the notebooks used to have.
- **`energy(x, p)`** — the classical energy `p²/2m + ½mω²x²`.
- **`hamilton_rhs(t, state)`** — the right-hand side of Hamilton's equations, `[dx/dt, dp/dt] = [p/m, −mω²x]`, in the form `solve_ivp` wants.
- **`analytic_xp(t, x0, p0)`** — the exact classical solution `x(t), p(t)`, used to check the numerical solver.
- **`build_operators(N)`** — builds the truncated quantum operators and returns `(a, adag, x, p, H)`.
- **`wigner_gif(states, tlist, fname, …)`** — turns a sequence of quantum states into an animated GIF of the Wigner function with a fixed color scale.

**An important note on what the notebooks import vs. define.** The notebooks import only `setup` (both) and `wigner_gif` (Component 2) from `oscillator`. The physics functions — `energy`, `hamilton_rhs`, the operator construction — are **written out inline in the notebook cells** so the work is visible (your PI can see the physics, not a black box). The same functions also live in `oscillator.py` as reusable helpers, available for future work (e.g. Component 3) without copy-pasting. Same math: defined inline where it's worth seeing, and kept in `shared/` where it's worth reusing.

---

# COMPONENT 1 — `component1_classical.ipynb`

Goal: simulate a mass on a spring (the classical harmonic oscillator) and produce the energy map and motion trajectories — the *classical inputs* for the eventual machine-learning model.

## Cell 1 (markdown) — Title and overview
States the notebook's goal (generate classical baseline data) and the two tasks. The key line is the project's rule, *"never trust a number that cannot be verified"* — which is why the harmonic oscillator is used (it has exact formulas to check against).

## Cell 2 (markdown) — Setup and conventions
Explains **natural units** ℏ = m = ω = 1 (clean numbers) and notes a consequence: the energy contours, which are ellipses in real units, become **circles** here.

## Cell 3 (code) — Imports and one-line setup
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from oscillator import setup     # shared helper module (lives in shared/, importable anywhere)

# --- Natural units: hbar = m = omega = 1 ---
m = 1.0       # mass (dimensionless)
omega = 1.0   # angular frequency (dimensionless)

setup()       # group plot style + output routing (figures/ data/ movies/) in one call
```
Line by line:
- The three `import` lines bring in NumPy (`np`), Matplotlib (`plt`), and the `solve_ivp` solver from SciPy.
- `from oscillator import setup` — pull the `setup` helper out of your shared `oscillator.py`.
- `m = 1.0`, `omega = 1.0` — fix the mass and frequency to 1 (natural units). These boxes are reused throughout.
- `setup()` — the one call that applies the group plot style **and** turns on output routing (so figures save into `figures/`, data into `data/`). This single line replaces the longer block the notebook used to have.

*Why:* loads the tools and fixes all conventions in one line, so the rest of the notebook stays focused on physics.

## Cell 4 (markdown) — Task 1(a): the energy function
States `E(x,p) = p²/2m + ½mω²x²` and names its two pieces: kinetic energy (motion) and potential energy (spring).

## Cell 5 (code) — Define the energy and test it
```python
def energy(x, p, m=m, omega=omega):
    '''Classical energy (Hamiltonian) of the harmonic oscillator.'''
    kinetic = p**2 / (2.0 * m)
    potential = 0.5 * m * omega**2 * x**2
    return kinetic + potential

print("E(x=1, p=0) =", energy(1.0, 0.0), " (expected 0.5)")
print("E(x=0, p=1) =", energy(0.0, 1.0), " (expected 0.5)")
```
- `def energy(x, p, m=m, omega=omega):` — define the energy machine. `**` means "to the power of," so `p**2` is `p²`.
- `kinetic`/`potential` lines compute the two energy pieces; `return` hands back their sum.
- The two `print` lines test it: at (x=1, p=0) all energy is potential = ½; at (x=0, p=1) all energy is kinetic = ½. Seeing 0.5 confirms it.

*Why:* this energy function is reused to draw the map (Cell 8) and to check energy conservation (Cell 17). (The same function also lives in `shared/oscillator.py` for reuse elsewhere; here it is written out so the formula is visible.)

## Cell 6 (markdown) — Task 1(b): deriving Hamilton's equations
Pure math. Shows how the energy generates motion via `ẋ = ∂H/∂p`, `ṗ = −∂H/∂x`, which here become `ẋ = p/m` and `ṗ = −mω²x`. These are exactly what the solver in Task 2 uses.

## Cell 7 (markdown) — Task 1(c): what phase space is
Explains phase space — the plane of position (x) vs momentum (p), where one point is the whole state. Sets up the next plot.

## Cell 8 (code) — Draw the energy map (contour plot)
```python
x_vals = np.linspace(-3, 3, 400)
p_vals = np.linspace(-3, 3, 400)
X, P = np.meshgrid(x_vals, p_vals)
E_grid = energy(X, P)

fig, ax = plt.subplots(figsize=(6.2, 5.4))
filled = ax.contourf(X, P, E_grid, levels=30, cmap="viridis")
lines = ax.contour(X, P, E_grid, levels=[0.5, 1.5, 3.0, 4.5], colors="white", linewidths=1.2)
ax.clabel(lines, inline=True, fontsize=9, fmt="E=%.1f")
cbar = fig.colorbar(filled, ax=ax, shrink=0.82, pad=0.02)
cbar.set_label("Energy E  (dimensionless)")
ax.set_xlabel("Position x  (dimensionless)")
ax.set_ylabel("Momentum p  (dimensionless)")
ax.set_title("Constant-energy contours are circles in natural units", fontsize=13, pad=12)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("fig_c1_energy_contours.png", dpi=150, bbox_inches="tight")
plt.show()
```
- `np.linspace(-3,3,400)` makes the x and p axes; `np.meshgrid` combines them into a full 2-D grid; `energy(X, P)` evaluates the energy at all 160,000 points at once.
- `ax.contourf(...)` draws the filled color map (`viridis`); `ax.contour(..., colors="white")` overlays white lines at specific energies; `ax.clabel(...)` writes the value on each line.
- `fig.colorbar(..., shrink=0.82, pad=0.02)` adds the color scale; `shrink=0.82` makes the bar a bit shorter so its top number sits **below** the title (preventing overlap).
- `set_title(..., fontsize=13, pad=12)` gives the title a smaller size and extra headroom so it clears the colorbar.
- `set_aspect("equal")` makes one unit of x the same length as one of p, so circles look circular.
- `plt.savefig("fig_c1_energy_contours.png", …)` — note the **bare filename**; because `setup()` turned on output routing, this lands in `figures/` automatically.

**How to read this plot.** Axes are position (x) and momentum (p); color is total energy (dark = low, yellow = high). The white rings are constant-energy curves — circles centered at the origin. An oscillator with a given energy is locked on its ring; a bigger ring = more energy. This is energy conservation drawn as a picture.

## Cell 9 (markdown) — Caption
States the takeaway (constant-energy curves are closed loops the system can't leave) and why they're circles in natural units.

## Cell 10 (markdown) — Task 2(a): a single trajectory
Sets up the idea: the contours show *where* the system can be; now compute *how it moves* by integrating Hamilton's equations.

## Cell 11 (code) — Solve and plot one trajectory (with an exact check)
```python
def hamilton_rhs(t, state, m=m, omega=omega):
    '''Right-hand side of Hamilton's equations for solve_ivp.'''
    x, p = state
    dxdt = p / m
    dpdt = -m * omega**2 * x
    return [dxdt, dpdt]

T = 2 * np.pi / omega
t_span = (0.0, 2 * T)
t_eval = np.linspace(*t_span, 600)
x0, p0 = 2.0, 0.0
sol = solve_ivp(hamilton_rhs, t_span, [x0, p0], t_eval=t_eval, method="RK45", rtol=1e-9, atol=1e-9)

x_exact = x0*np.cos(omega*sol.t) + (p0/(m*omega))*np.sin(omega*sol.t)
p_exact = -m*omega*x0*np.sin(omega*sol.t) + p0*np.cos(omega*sol.t)
max_dev = np.max(np.hypot(sol.y[0]-x_exact, sol.y[1]-p_exact))
print(f"Max numerical-vs-analytic deviation = {max_dev:.2e}  (should be ~0 -> solver is correct)")

fig, ax = plt.subplots(figsize=(5.6, 5.4))
ax.plot(sol.y[0], sol.y[1], color="#1f77b4", lw=2.5, label="numerical (solve_ivp)")
ax.plot(x_exact, p_exact, "--", color="white", lw=1.2, label="analytic check")
ax.plot(x0, p0, "o", color="crimson", ms=9, label="start $(x_0,p_0)$")
ax.set_xlabel("Position x  (dimensionless)")
ax.set_ylabel("Momentum p  (dimensionless)")
ax.set_title("A classical orbit is a closed loop in phase space")
ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.legend(loc="lower left")
plt.tight_layout()
plt.savefig("fig_c1_single_trajectory.png", dpi=150, bbox_inches="tight")
plt.show()
```
- `def hamilton_rhs(...)` — the "rule of motion." `solve_ivp` calls it repeatedly; it unpacks the current `state = [x, p]` and returns the rates `[p/m, −mω²x]`.
- `T = 2*np.pi/omega` is one full period; `t_span` simulates two periods; `t_eval` is 600 times to record.
- `x0, p0 = 2.0, 0.0` — released from x=2 at rest.
- `sol = solve_ivp(...)` — the solver marches the motion forward. `sol.t` = times, `sol.y[0]` = positions, `sol.y[1]` = momenta. `rtol/atol` set accuracy.
- The `x_exact`/`p_exact` lines compute the known pen-and-paper answer; `max_dev` is the biggest gap between computed and exact (≈7e-9 → solver verified).
- The plot draws the numerical path (blue), the exact answer dashed on top (white), and the start dot (crimson). `ax.legend(loc="lower left")` places the legend in the lower-left corner (out of the way of the orbit). The save uses a bare name → routes to `figures/`.

**How to read this plot.** The solid blue curve is the computed orbit — a closed circle, so the oscillator returns to its start each period. The dashed line (exact formula) lies right on top of it — visual proof the simulation is correct. The red dot marks the start.

## Cell 12 (markdown) — Caption
States the takeaway: one start point traces one closed loop — deterministic, energy-conserving motion.

## Cell 13 (markdown) — Task 2(b): many trajectories
Explains we'll launch many starts at once to reveal the nested structure and save the data for Component 3.

## Cell 14 (code) — Many random trajectories + save data
```python
rng = np.random.default_rng(42)
n_traj = 12
trajectories = []

fig, ax = plt.subplots(figsize=(7.4, 5.8))
cmap = plt.cm.plasma
for k in range(n_traj):
    x0 = rng.uniform(-2.5, 2.5)
    p0 = rng.uniform(-2.5, 2.5)
    sol = solve_ivp(hamilton_rhs, (0, T), [x0, p0], t_eval=np.linspace(0, T, 400),
                    method="RK45", rtol=1e-9, atol=1e-9)
    E0 = energy(x0, p0)
    color = cmap(E0 / 6.0)
    ax.plot(sol.y[0], sol.y[1], color=color, lw=1.6)
    ax.plot(x0, p0, "o", color=color, ms=5)
    trajectories.append(np.vstack([sol.t, sol.y[0], sol.y[1]]).T)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 6))
cbar = fig.colorbar(sm, ax=ax, shrink=0.82, pad=0.02); cbar.set_label("Initial energy E  (dimensionless)")
ax.set_xlabel("Position x  (dimensionless)")
ax.set_ylabel("Momentum p  (dimensionless)")
ax.set_title("Larger starting energy gives a larger, non-crossing orbit", fontsize=13, pad=12)
ax.set_aspect("equal"); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("fig_c1_many_trajectories.png", dpi=150, bbox_inches="tight")
plt.show()

data_array = np.array(trajectories, dtype=object)
np.save("classical_trajectories.npy", data_array)
print(f"Saved {n_traj} trajectories to classical_trajectories.npy")
```
- `rng = np.random.default_rng(42)` — a random generator seeded with 42 (so the "random" starts are the same every run = reproducible).
- `for k in range(n_traj):` — repeat 12 times. Each loop picks a random start, solves the orbit, computes its energy `E0`, picks a color from `plasma` scaled by energy, plots the orbit and start dot, and appends `[time, x, p]` to `trajectories`.
- `ScalarMappable` + `colorbar` build the energy color scale (shrunk to clear the title).
- `np.save("classical_trajectories.npy", …)` — a **bare** `.npy` name, so output routing sends it to `data/`. This file is the classical input dataset for Component 3.

**How to read this plot.** Nested circles, each colored by its (conserved) starting energy. Orbits never cross (a state has a unique future) and bigger energy = bigger circle. This nested structure is the "feature space" the ML model will learn from.

## Cell 15 (markdown) — Caption
Restates: nested, non-crossing circles whose size is set by energy.

## Cell 16 (markdown) — Sanity-check intro
Explains we'll verify energy is truly conserved along a trajectory.

## Cell 17 (code) — Energy-conservation check
```python
sol = solve_ivp(hamilton_rhs, (0, 4*T), [1.5, 0.5], t_eval=np.linspace(0, 4*T, 2000),
                method="RK45", rtol=1e-10, atol=1e-10)
E_t = energy(sol.y[0], sol.y[1])
drift = E_t.max() - E_t.min()
print(f"Energy min/max over 4 periods: {E_t.min():.10f} / {E_t.max():.10f}")
print(f"Total energy drift: {drift:.2e}  (should be ~1e-8 or smaller -> conserved)")
assert drift < 1e-6, "Energy not conserved -> tighten solver tolerances!"
print("PASS: energy is conserved -> the numerical pipeline is trustworthy.")
```
- Solve one orbit for four periods at tight tolerances; compute the energy at every time step; `drift` is how much it wandered (max − min).
- `assert drift < 1e-6, "..."` — the automatic check: if energy drifted too much, Python stops with that message. It passes (drift ≈ 2e-9), so the pipeline is trustworthy.

## Cell 18 (markdown) — Takeaways
Summarizes Component 1 and names its outputs (`data/classical_trajectories.npy` and the figures), then points to Component 2.

---


# COMPONENT 2 — `component2_quantum.ipynb`

Goal: compute the *quantum* version of the same oscillator — its allowed energies and how its states move in time — with QuTiP, checked against exact formulas. These are the *prediction targets* for Component 3.

> **New idea:** position and momentum become **operators** (matrices); a quantum **state** is a column of numbers (a vector). QuTiP handles these as objects so the code looks ordinary.

## Cell 1 (markdown) — Title and overview
States the goal and the big shift: classically the oscillator is a point on an ellipse; quantum-mechanically it's a fuzzy blob and energy comes in fixed steps.

## Cell 2 (markdown) — Setup and conventions
Same natural units, and introduces **truncation**: keep the lowest `N` energy levels so every operator is a finite `N×N` matrix.

## Cell 3 (code) — Imports and one-line setup
```python
import numpy as np
import matplotlib.pyplot as plt
import qutip
from qutip import destroy, basis, coherent, sesolve, wigner   # only what this notebook uses
from oscillator import setup     # shared helper module (lives in shared/, importable anywhere)

# --- Natural units: hbar = m = omega = 1 ---
hbar = 1.0; m = 1.0; omega = 1.0
N = 30                       # number of energy levels kept (Hilbert-space truncation)

setup()       # group plot style + output routing (figures/ data/ movies/) in one call
print("QuTiP", qutip.__version__, "| truncation N =", N, "| units: hbar=m=omega=1")
```
- `import qutip` + the `from qutip import ...` line pull in the quantum tools used: `destroy` (the annihilation operator), `basis`/`coherent` (states), `sesolve` (the Schrödinger solver), and `wigner` (the Wigner function). The import lists only what the notebook actually uses.
- `from oscillator import setup` + `setup()` — the same one-line setup as Component 1 (group style + output routing).
- `N = 30` — keep the lowest 30 energy levels; every operator becomes a 30×30 matrix.
- The `print` confirms the QuTiP version and settings.

## Cell 4 (code) — Environment check
```python
import qutip
qutip.about()
```
Prints the QuTiP / NumPy / SciPy versions and the install path — a quick confirmation the quantum toolbox is installed and which version you're on. Pure diagnostics; it produces no figure.

## Cell 5 (markdown) — Task 1(a): building the operators
Gives the formulas for x̂, p̂, Ĥ from the ladder operators â (annihilation) and â† (creation); in natural units the prefactor is 1/√2.

## Cell 6 (code) — Build x̂, p̂, Ĥ and verify them
```python
a = destroy(N)
adag = a.dag()
x_op = (a + adag) / np.sqrt(2)
p_op = -1j * (a - adag) / np.sqrt(2)
H = p_op**2 / (2*m) + 0.5 * m * omega**2 * x_op**2
H_ladder = hbar * omega * (adag * a + 0.5)
block = N // 2
diff_low = np.abs((H - H_ladder).full()[:block, :block]).max()
print(f"Difference on the low-energy block = {diff_low:.2e}  (~0 -> the algebra checks out)")
print(f"Full-matrix difference = {float((H - H_ladder).norm()):.2f}  (nonzero only at the truncation edge)")
print("Hamiltonian is", H.shape[0], "x", H.shape[1])
```
- `a = destroy(N)` — the **annihilation operator** â as a 30×30 matrix (the foundation; everything is built from it). `a.dag()` — the **creation operator** â† (dagger = conjugate-transpose).
- `x_op`, `p_op` — position and momentum operators from the ladder ops; `1j` is the imaginary unit `i`.
- `H` — the Hamiltonian assembled from x̂, p̂. `H_ladder` — the same Hamiltonian written the elegant way, ℏω(â†â + ½); we build both to cross-check.
- `block = N // 2` (`//` is whole-number division → 15). `(H - H_ladder).full()[:block, :block]` compares the two only on the trustworthy lower-left 15×15 corner; it prints ~0 (they agree). The full-matrix difference prints 15 — that's only from the truncation edge, printed honestly.
- (`shared/oscillator.py`'s `build_operators(N)` does this same construction; here it's written out so the operator definitions are visible.)

> **Concepts (Study Guide):** what it means for x̂ and p̂ to *be operators* instead of numbers → Q7; why â/â† form a *ladder* and what “adding one quantum of energy” means → Q14; what the *Fock basis* is → Q15.

## Cell 7 (code) — Picture the operator matrices
```python
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
for ax, op, name in zip(axes, [x_op, p_op, H], [r"$|\hat x|$", r"$|\hat p|$", r"$|\hat H|$"]):
    im = ax.imshow(np.abs(op.full()), cmap="viridis")
    ax.set_title(name); ax.set_xlabel("column index n"); ax.set_ylabel("row index m")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
fig.suptitle("Operator matrices in the energy (Fock) basis", y=1.02)
plt.tight_layout()
plt.savefig("fig_c2_operator_matrices.png", dpi=150, bbox_inches="tight")
plt.show()
```
- `plt.subplots(1, 3, …)` makes three side-by-side panels. The `for … zip(...)` loop draws each operator in turn.
- `ax.imshow(np.abs(op.full()), …)` shows the matrix as an image: each cell is a colored pixel sized by that entry's magnitude (`.full()` converts the QuTiP object to a plain number grid).

**How to read this plot.** Each panel is a 30×30 grid; bright = large entry, dark purple = zero. **Ĥ (right)** has color only on the diagonal → each level has one definite energy. **x̂ and p̂ (left, middle)** have color only just off the diagonal → they connect a level only to its immediate neighbors (the ladder structure).

> **Concepts (Study Guide):** how an operator becomes a grid of numbers `⟨m|Â|n⟩` you can plot as a heatmap → Q15.


## Cell 8 (markdown) — Caption
Explains the diagonal-vs-off-diagonal structure and what it means physically.

## Cell 9 (markdown) — Task 1(b): the energy spectrum
States the allowed energies are the eigenvalues of Ĥ, with exact answer Eₙ = ℏω(n+½).

## Cell 10 (code) — Compute and plot the energy levels
```python
eigvals = H.eigenenergies()
n_index = np.arange(N)
analytic = hbar * omega * (n_index + 0.5)

fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.plot(n_index, analytic, "-", color="crimson", lw=2, label=r"analytic  $E_n=\hbar\omega(n+\frac{1}{2})$")
ax.plot(n_index, eigvals, "o", color="#1f77b4", ms=6, mfc="none", label="QuTiP eigenvalues")
ax.set_xlabel("Level index n  (dimensionless)")
ax.set_ylabel("Energy $E_n$  (dimensionless)")
ax.set_title("Quantized, evenly spaced energy levels")
ax.legend(loc="upper left"); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("fig_c2_energy_spectrum.png", dpi=150, bbox_inches="tight")
plt.show()
```
- `H.eigenenergies()` — asks QuTiP for the **eigenvalues** of the Hamiltonian: the allowed energies. `np.arange(N)` is the level numbers 0…29; `analytic` is the exact formula at each.
- The two `ax.plot` lines draw the exact formula (red line) and QuTiP's values (hollow blue circles). `ax.legend(loc="upper left")` puts the legend in the empty upper-left (above the rising line).

**How to read this plot.** Horizontal = level number n; vertical = energy. The blue circles sit exactly on the red line for low levels → the code is correct. The line is straight and evenly stepped (energies are discrete and equally spaced), and the lowest point is at 0.5, not 0 — the zero-point energy.

> **Concepts (Study Guide):** why a measurement can only return these discrete *eigenvalues* → Q7 & Q13; discrete *energies* vs. the continuous *set of states* built from them → Q9; what energy we are actually measuring, and why it is the *same* quantity as the classical case → Q17 & Q18.


## Cell 11 (code) — Spectrum sanity checks
```python
print(f"Ground-state energy E_0 = {eigvals[0]:.6f}  (expected 0.5 -> zero-point energy)")
spacing = np.diff(eigvals[:6])
print(f"Spacing between low levels = {np.round(spacing, 6)}  (expected all 1.0)")
n_reliable = N // 2
max_err_low = np.max(np.abs(eigvals[:n_reliable] - analytic[:n_reliable]))
print(f"Max error over the lowest {n_reliable} levels = {max_err_low:.2e}")
assert abs(eigvals[0] - 0.5) < 1e-6, "ground state should be the zero-point energy 1/2"
assert max_err_low < 1e-6, "low spectrum should match exactly"
print("PASS: low spectrum matches the exact formula -> operators are correct.")
print("(High-n levels drift on purpose: that is truncation. Increase N to push it up.)")
```
- `eigvals[0]` is the ground-state energy (should be 0.5). `np.diff(eigvals[:6])` lists the gaps between the first six levels (should all be 1.0).
- `max_err_low` checks the lowest half against the exact formula; the two `assert` lines enforce ground state = 0.5 and low levels exact, then PASS prints. The last line reminds you high-n drift is expected truncation.

## Cell 12 (markdown) — Convergence-check intro
Explains the rule "always check convergence in N" — higher N keeps more levels accurate.

## Cell 13 (code) — Demonstrate truncation/convergence
```python
fig, ax = plt.subplots(figsize=(6.8, 4.6))
for N_test in [10, 30, 50]:
    a_t = destroy(N_test)
    x_t = (a_t + a_t.dag()) / np.sqrt(2)
    p_t = -1j * (a_t - a_t.dag()) / np.sqrt(2)
    H_t = p_t**2 / 2 + x_t**2 / 2
    err_t = np.abs(H_t.eigenenergies() - (np.arange(N_test) + 0.5))
    ax.semilogy(np.arange(N_test), err_t + 1e-18, marker="o", ms=3, label=f"N = {N_test}")
ax.axhline(1e-6, ls="--", color="k", alpha=0.6, label="1e-6 threshold")
ax.set_xlabel("Level index n  (dimensionless)")
ax.set_ylabel("Eigenvalue error  (dimensionless)")
ax.set_title("Higher truncation N extends the trustworthy energy range")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig("fig_c2_convergence.png", dpi=150, bbox_inches="tight")
plt.show()
```
- `for N_test in [10, 30, 50]:` — rebuild the operators (same inline construction as Cell 6) at three truncation sizes, then compute each level's error vs. the exact formula.
- `ax.semilogy(...)` plots error vs. level on a **log** vertical axis (errors span 1e-16 to 1, so only a log scale shows them); `+ 1e-18` avoids log of zero. `ax.axhline(1e-6, …)` draws the "trust threshold."
- `ax.set_ylabel("Eigenvalue error  (dimensionless)")` — a short label so it doesn't run off the page. `ax.legend(loc="lower right")` puts the legend in the empty lower-right so it doesn't cover the N=10/N=30 lines.

**How to read this plot.** Horizontal = level number; vertical = how wrong that level is (log scale, lower = better). Each colored curve is one N. They sit near zero for low levels, then shoot up near the top of each truncation. Bigger N stays accurate farther right (N=10→5, 30→15, 50→25 exact levels). Lesson: raise N until the levels you care about are well below the threshold.

## Cell 14 (markdown) — Convergence caption
Restates: increase N until results stop changing.

## Cell 15 (markdown) — Task 1(c): what changed classical → quantum
A written comparison: same energy form and ω; but energy became discrete, with a nonzero zero-point floor, and the point became a spread-out state.

## Cell 16 (markdown) — Task 2(a): three states and the Schrödinger equation
Introduces the Schrödinger equation (iℏ d|ψ⟩/dt = Ĥ|ψ⟩) and the three states to evolve.

## Cell 17 (code) — Define the three states and evolve them
```python
psi_fock  = basis(N, 1)
psi_super = (basis(N, 0) + basis(N, 1)).unit()
alpha = 1.5
psi_coh   = coherent(N, alpha)

states = {"Fock |1>": psi_fock, "Superposition (|0>+|1>)/sqrt2": psi_super,
          f"Coherent |a={alpha}>": psi_coh}

T = 2 * np.pi / omega
tlist = np.linspace(0, T, 200)

results = {}
for name, psi0 in states.items():
    res = sesolve(H, psi0, tlist, e_ops=[x_op, p_op], options={"store_states": True})
    results[name] = res
    print(f"Evolved {name}: stored {len(res.states)} states.")
```
- `basis(N, 1)` — the pure level-1 state |1⟩ (a Fock state). `(basis(N,0)+basis(N,1)).unit()` — the superposition, with `.unit()` rescaling so total probability = 100%. `coherent(N, 1.5)` — the classical-like coherent state.
- `states = {...}` — a **dictionary** pairing each name with its state, so we can loop with names attached.
- `tlist` — 200 time points across one period.
- `sesolve(H, psi0, tlist, e_ops=[x_op, p_op], options={"store_states": True})` — the **Schrödinger-equation solver** (the quantum twin of `solve_ivp`). `e_ops=[x_op, p_op]` tells it to record the averages ⟨x̂⟩, ⟨p̂⟩ at each time (`res.expect[0]`, `res.expect[1]`); `store_states` keeps the full state at each time (`res.states`).

> **Concepts (Study Guide):** the states `|ψ⟩` evolved here are *kets* (vectors) living in *Hilbert space* → Q8 & Q10; how *bras*, the *inner product / overlap*, and measurement *probabilities* (the Born rule) work → Q11–Q13.


## Cell 18 (markdown) — Task 2(b): the Wigner function at t=0
Explains the Wigner function draws a quantum state in the same (x,p) plane and can go negative (the fingerprint of "non-classical").

## Cell 19 (code) — Wigner snapshots at t=0
```python
xvec = np.linspace(-4, 4, 200)
pvec = np.linspace(-4, 4, 200)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
for ax, (name, psi0) in zip(axes, states.items()):
    W = wigner(psi0, xvec, pvec)
    wmax = np.abs(W).max()
    cf = ax.contourf(xvec, pvec, W, levels=80, cmap="RdBu_r", vmin=-wmax, vmax=wmax)
    ax.set_title(name); ax.set_xlabel("x  (dimensionless)")
    ax.set_ylabel("p  (dimensionless)"); ax.set_aspect("equal")
    fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04, label="W(x,p)")
fig.suptitle("Wigner functions at t = 0  (blue = negative = non-classical)", y=1.03)
plt.tight_layout()
plt.savefig("fig_c2_wigner_t0.png", dpi=150, bbox_inches="tight")
plt.show()
```
- `xvec`, `pvec` — the phase-space grid. `wigner(psi0, xvec, pvec)` asks QuTiP for the Wigner quasi-probability over that grid.
- `wmax` sets a **symmetric** color scale so zero sits at white. `ax.contourf(..., cmap="RdBu_r", vmin=-wmax, vmax=wmax)` draws it with a **diverging** colormap (red = positive, white = zero, blue = negative) — used here on purpose because the data is signed.

**How to read this plot.** Three panels in the (x,p) plane. **Coherent (right):** a single red Gaussian, no blue → most classical. **Fock |1⟩ (left):** a red ring around a deep **blue** (negative) center → strongly non-classical. **Superposition (middle):** two lobes with alternating red/blue **interference fringes** between them → proof of a true superposition.

> **Concepts (Study Guide):** why a quantum state shows up as a *blob* (not a point) in the (x,p) plane — the uncertainty principle that forbids knowing x and p exactly at once → Q16.


## Cell 20 (markdown) — Caption
Explains the three shapes and why a diverging colormap is used here (the one exception to viridis, because values are signed).

## Cell 21 (markdown) — Task 2(c): animations
Explains we'll animate each state over one period with a fixed color scale.

## Cell 22 (code) — Wigner movies via the shared `wigner_gif()` helper
```python
from oscillator import wigner_gif
from IPython.display import Image as IPyImage, display

gif_paths = {}
for name, res in results.items():
    safe = name.split()[0].lower()          # 'fock', 'superposition', 'coherent'
    path = wigner_gif(res.states, tlist, f"movies/wigner_{safe}.gif",
                      xvec=xvec, pvec=pvec, title=name)
    gif_paths[name] = path
    print("Saved", path)

for name, path in gif_paths.items():
    print(name)
    display(IPyImage(filename=path))
```
- `from oscillator import wigner_gif` — **this is where the shared helper is used.** Instead of ~30 lines of frame-rendering code in the notebook, the heavy lifting lives in `shared/oscillator.py`.
- The loop calls `wigner_gif(...)` once per state, passing the stored states (`res.states`), the times (`tlist`), an output filename, the grid, and a title. `name.split()[0].lower()` turns "Fock |1>" into a tidy filename piece "fock."
- **What `wigner_gif` does internally** (from Part 1): it samples ~40 time-steps, computes the Wigner function at each, finds one global maximum so the color scale is **fixed** across all frames (otherwise the flicker would be meaningless), renders each frame, and stitches them into a GIF with `imageio.mimsave`. It returns the filename.
- `display(IPyImage(filename=path))` shows each finished GIF inline in the notebook.

**How to read these animations.** Same red/blue phase-space picture, moving over one period. **Coherent:** the blob orbits the center like a classical particle. **Fock |1⟩:** the ring rotates onto itself (looks unchanged → a *stationary* state). **Superposition:** the fringes rotate, sweeping the lobes back and forth — which is the oscillation of ⟨x̂⟩ quantified next.

## Cell 23 (markdown) — Note
Tells you what to look for in each animation.

## Cell 24 (markdown) — Task 2(d): averages vs. classical motion
Explains we'll plot the quantum average path and overlay the classical orbit from the same start.

## Cell 25 (code) — Compare quantum averages to classical orbits
```python
from scipy.integrate import solve_ivp
def classical_rhs(t, s):                 # same Hamilton's equations as Component 1
    x, p = s
    return [p/m, -m*omega**2*x]

fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
for ax, (name, res) in zip(axes, results.items()):
    xq, pq = res.expect[0], res.expect[1]            # quantum averages over time
    x0, p0 = xq[0], pq[0]                             # matching classical start point
    csol = solve_ivp(classical_rhs, (0, T), [x0, p0], t_eval=tlist, rtol=1e-9, atol=1e-9)
    ax.plot(csol.y[0], csol.y[1], "-", color="crimson", lw=3, alpha=0.6, label="classical")
    ax.plot(xq, pq, "--", color="#1f77b4", lw=2, label=r"quantum $\langle\hat x\rangle,\langle\hat p\rangle$")
    ax.plot(x0, p0, "ko", ms=6)
    ax.set_title(name, fontsize=12); ax.set_xlabel("x"); ax.set_ylabel("p")
    ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.legend(fontsize=9, loc="upper right")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
fig.suptitle(r"Quantum averages vs. classical orbits", y=1.03)
plt.tight_layout()
plt.savefig("fig_c2_expectation_vs_classical.png", dpi=150, bbox_inches="tight")
plt.show()
```
- `classical_rhs` — the same classical equations of motion as Component 1 (so we can draw the matching classical orbit).
- `res.expect[0]`, `res.expect[1]` — the recorded quantum **averages** ⟨x̂⟩(t), ⟨p̂⟩(t) (stored earlier by `sesolve` via `e_ops`). `x0, p0` is the average at t=0; the classical orbit starts there.
- The plot overlays the classical orbit (thick red) and the quantum-average path (dashed blue). `ax.legend(fontsize=9, loc="upper right")` keeps the legend in the upper-right corner of each panel.

**How to read this plot.** **Coherent (right):** dashed blue lands exactly on the red circle → the quantum average moves like a classical particle (Ehrenfest's theorem). **Superposition (middle):** a smaller circle driven by interference. **Fock |1⟩ (left):** just a dot at the origin — its average position/momentum are zero for all time. The averages hide the ringed structure the Wigner plot showed — the point of the next cell.

## Cell 26 (markdown) — Discussion
Explains when quantum motion looks classical (coherent, via Ehrenfest) and what averaging throws away (spread, uncertainty, interference) — which is why the Wigner function, not the average, is the ML target.

## Cell 27 (markdown) — Task 2(e): one-page reflection
The written deliverable: what each representation (energy contours, operator matrices, eigenvalues, Wigner functions, expectation plots) tells you and leaves out.

## Cell 28 (markdown) — Takeaways
Summarizes Component 2 and lists outputs (spectrum, expectation trajectories, Wigner data, figures, and the `movies/` GIFs).

---

# Quick reference — every function used, in one place

**Your shared modules (`shared/`):**
- `setup()` *(oscillator)* — apply group plot style + turn on output routing, in one call.
- `energy(x, p)` *(oscillator)* — classical energy `p²/2m + ½mω²x²`.
- `hamilton_rhs(t, state)` *(oscillator)* — classical equations of motion for `solve_ivp`.
- `analytic_xp(t, x0, p0)` *(oscillator)* — exact classical `x(t), p(t)` for checking.
- `build_operators(N)` *(oscillator)* — returns `(a, adag, x, p, H)` for an N-level oscillator.
- `wigner_gif(states, tlist, fname, …)` *(oscillator)* — animated Wigner GIF with a fixed color scale.
- `apply_group_style()` *(group_plot_style)* — set matplotlib defaults to the group's standards.
- `route_outputs()` *(output_routing)* — auto-sort saved files into `figures/ data/ movies/` by type.

**NumPy (np):** `linspace`, `arange`, `meshgrid`, `cos`/`sin`/`sqrt`/`abs`/`max`/`diff`/`round`/`hypot`, `array`, `any`, `argmax`, `vstack`/`.T`, `save`, `random.default_rng`/`.uniform`.

**Matplotlib (plt / ax):** `subplots`, `plot`, `contourf`/`contour`, `clabel`, `imshow`, `semilogy`, `axhline`, `set_xlabel`/`ylabel`/`title`, `suptitle`, `legend`, `grid`, `set_aspect`, `set_xlim`/`ylim`, `colorbar`/`set_label`, `cm.ScalarMappable`/`Normalize` (for the energy color scale), `tight_layout`, `savefig`, `show`.

**SciPy:** `solve_ivp(rule, time_span, start, …)` — numerically steps a differential equation forward in time (the ODE-solver sense of “integrate”: advancing the state through time).

**QuTiP:** `qutip.about()` (environment check), `destroy(N)`/`create(N)` (ladder operators), `.dag()`, `basis(N, n)`, `.unit()`, `coherent(N, alpha)`, `H.eigenenergies()`, `.full()`, `.norm()`, `sesolve(H, psi0, tlist, e_ops=[...], options={...})`, `wigner(state, xvec, pvec)`.

**IPython.display:** `display(...)`, `Image(filename=...)` — show the saved Wigner GIFs inline in the notebook.

**Plain Python:** `def name(args):` … `return` (define a function); `for x in things:` (loop); `{key: value}` (dictionary); `print(...)`; `assert claim, "msg"`; `#` comment; `'''...'''` docstring.
