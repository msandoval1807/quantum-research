# Code Walkthrough — Components 1, 2 & 3

**Author:** Marcos Sandoval Lucas
**Project:** AI Design of Quantum Processors — Mondragon-Shem Quantum Group, UIC College of Engineering

This guide explains **every cell** of `component1_classical.ipynb`, `component2_quantum.ipynb`, and
`component3_ml.ipynb` — what the text is saying, what each line of code does, what every function
means, *why* it is there, and how to read each plot. It assumes **no prior Python knowledge**.

> **Sources & conventions.** The quantum physics matches the group's assigned text, **Essler's
> *Lecture Notes for Quantum Mechanics*** (cross-references are in the companion
> `Classical_and_Quantum_Mechanics_Study_Guide.md`). Components 1 and 2 work in **natural units**
> ℏ = m = ω = 1, which makes the numbers clean (energy levels come out 0.5, 1.5, 2.5, …).
> Component 3 works in fluxonium units where `E_C = 1`.

---

## How to read this document

It is in the order the work was actually built, and each part assumes only the parts before it:

| Part | What it covers | Read it when |
|---|---|---|
| **1** | Python from zero — every language feature the notebooks use | First. Nothing else makes sense without it. |
| **2** | The `shared/` helper modules | Before opening any notebook — every one starts by importing them. |
| **3** | Component 1, Tasks 1 → 4 in order | Alongside `component1_classical.ipynb`. |
| **4** | Component 2, Tasks 1 → 3 in order | Alongside `component2_quantum.ipynb`. |
| **5** | Component 3, every cell | Alongside `component3_ml.ipynb`. |
| **6** | Quick reference — every function in one table | As a lookup, once you are working. |
| **7** | Change log | Only if you are wondering why something differs from an older version. |

Within Parts 3–5 the tasks run **1, 2, 3, 4** with no detours. A task added later to a notebook is
documented in that notebook's own part, in task order — not appended at the end.

---

# PART 1 — Python from zero

Everything the three notebooks use, in the order it becomes necessary. Each idea is shown with a
line taken from the actual project code, so nothing here is abstract.

## 1.1 What a notebook is

A Jupyter notebook is a document made of **cells** stacked top to bottom. There are two kinds:

- **Markdown cells** — formatted text and equations. The explanation. They do not compute anything.
- **Code cells** — Python that runs when you tell it to, printing its output and drawing its plots
  directly underneath itself.

You run the selected cell with **Shift+Enter**. Cells run **in order, top to bottom**, and they
share one memory: a variable created in cell 3 still exists in cell 20. This is why "Restart Kernel
and Run All Cells" is the only trustworthy way to check a notebook — running cells out of order can
produce results that depend on something you have since changed.

> **The gotcha that will bite you.** If a notebook file was edited on disk while an old tab was
> open in your browser, the old tab overwrites the file when it saves. Close the tab **without
> saving**, reopen it, then Restart & Run All.

## 1.2 A variable is a labelled box

```python
m = 1.0
```

"Make a box called `m`, put the number 1.0 in it." Afterwards, writing `m` anywhere means "whatever
is in that box." The `=` is not the equals sign of mathematics — it is an instruction, "put the
right-hand side into the left-hand name." That is why this is legal and sensible:

```python
best_val = np.inf        # start with infinity
best_val = va_loss       # later, replace it with something smaller
```

Names may contain letters, numbers and underscores, and are case-sensitive: `A` and `a` are two
different boxes. (Component 3 relies on this — `A` is the classical data, `a` is nothing.)

## 1.3 The kinds of value a box can hold

| Kind | Example from the project | What it is |
|---|---|---|
| integer (`int`) | `N_t = 40` | a whole number |
| float (`float`) | `E_J = 5.0` | a number with a decimal part |
| string (`str`) | `"copy-classical"` | text, in quotes |
| boolean (`bool`) | `True`, `False` | a yes/no value |
| complex | `1j`, `3 + 4j` | a complex number — Python writes `i` as `j` |
| `None` | `best_state = None` | "deliberately nothing here yet" |

`1.0` and `1` behave differently in some places, which is why the code writes `E_C = 1.0` rather
than `E_C = 1` — it keeps every downstream calculation in decimals.

Arithmetic is ordinary, with two operators worth knowing:

```python
p**2          # p squared      ** means "to the power of"
N // 2        # whole-number division: 30 // 2 is 15, and 31 // 2 is also 15
```

## 1.4 Comments and docstrings

```python
E_C = 1.0     # charging energy -- everything is measured in units of this
```

Everything after a `#` is a note for humans; Python ignores it entirely. A triple-quoted string
just under a `def` line is a **docstring** — a description of what a function does:

```python
def wave_packet(phi0, n0):
    """Gaussian packet centered at (phi0, n0): a coherent state of the fluxonium LC mode."""
```

## 1.5 Printing, and f-strings

`print(...)` displays things. The useful form is the **f-string** — a string with an `f` in front,
where anything inside `{curly braces}` is replaced by its value:

```python
print(f"dataset shapes:  A {A.shape}  B {B.shape}")
```

The colon inside the braces controls **formatting**, which is why the project's output lines up so
neatly:

| Written | Means | Example output |
|---|---|---|
| `{val:.4f}` | 4 digits after the decimal point | `1.0666` |
| `{val:.2e}` | scientific notation, 2 digits | `1.47e-04` |
| `{val:>10}` | pad on the left to 10 characters wide | `      MLP` |
| `{val:<24}` | pad on the right to 24 characters wide | `MLP                     ` |
| `{val:>8.4f}` | both at once — 8 wide, 4 decimals | `  1.0666` |

That is the whole trick behind the results tables in Component 3: `{name:<24}` for the label column
and `{rms:>17.4f}` for the numbers.

## 1.6 Functions — reusable machines

A function takes **inputs** in parentheses and hands back an **output**.

```python
def energy(x, p, m=m, omega=omega):
    """Classical energy (Hamiltonian) of the harmonic oscillator."""
    kinetic = p**2 / (2.0 * m)
    potential = 0.5 * m * omega**2 * x**2
    return kinetic + potential
```

- `def` starts the definition; `energy` is the name; `x, p, m, omega` are the **parameters**.
- **Indentation is the syntax.** The indented lines are the function's body. Python has no braces —
  the indentation *is* what says "this belongs inside." Getting it wrong is a real error, not a
  style issue.
- `m=m, omega=omega` are **default values**: if you do not supply them, the outer `m` and `omega`
  are used. So `energy(1.0, 0.0)` works and quietly uses the defaults.
- `return` hands the answer back. Without it a function returns `None`.

Calling it: `energy(1.0, 0.0)` feeds 1.0 in as `x` and 0.0 as `p`. You can also name the arguments
at the call, in any order, which is what the plotting code does constantly:

```python
ax.plot(x, p, color="crimson", lw=2.5, label="numerical")
```

`color=`, `lw=` and `label=` are **keyword arguments** — they say which slot each value goes into,
so you do not have to remember the order.

## 1.7 Imports — borrowing other people's code

```python
import numpy as np
from scipy.integrate import solve_ivp
```

- `import numpy as np` — load the whole NumPy toolbox and call it `np` for short. Afterwards
  everything from it is reached as `np.something`.
- `from scipy.integrate import solve_ivp` — reach into SciPy and pull out just the one tool, so it
  can be written as `solve_ivp` with no prefix.

The five libraries this project uses:

| Library | Short name | What it does here |
|---|---|---|
| **NumPy** | `np` | fast arrays and maths |
| **Matplotlib** | `plt` | every plot |
| **SciPy** | — | `solve_ivp`, the classical differential-equation solver; `spearmanr`, a statistics test |
| **QuTiP** | `qt` | quantum objects: operators, states, `sesolve`, Wigner functions |
| **scqubits** | `scq` | the real fluxonium qubit Hamiltonian |
| **PyTorch** | `torch` | the neural network |

Plus your own `shared/` modules (Part 2), imported the same way: `from oscillator import setup`.

## 1.8 Arrays — the single most important idea

A NumPy **array** is a row (or grid) of numbers treated as one object.

```python
tlist = np.linspace(0.0, t_final, N_t)     # N_t evenly spaced numbers from 0 to t_final
```

Common ways to make one:

```python
np.linspace(-3, 3, 400)     # 400 evenly spaced numbers from -3 to 3 (both ends included)
np.arange(N)                # whole numbers 0, 1, 2, ... N-1
np.zeros((N_s, 2 * N_t))    # a grid of zeros, N_s rows by 2*N_t columns
```

**Maths on an array happens to every element at once.** This is the thing to internalise:

```python
E_grid = energy(X, P)       # evaluates the energy at all 160,000 grid points in one line
analytic = hbar * omega * (n_index + 0.5)   # the exact formula at all 30 levels at once
```

No loop is needed, and this is both shorter and far faster than writing one. Two arrays can also be
combined element by element, provided their shapes match:

```python
err = B_hat - B[va]         # subtract two 60x80 grids -> a 60x80 grid of differences
```

## 1.9 Indexing and slicing — reaching into an array

Positions are counted **from zero**.

```python
eigvals[0]        # the first entry (the ground-state energy)
val_hist[-1]      # the LAST entry -- negative counts from the end
val_hist[149]     # the 150th entry, because counting starts at 0
```

A **slice** takes a range, written `start:stop`, and the `stop` is **not included**:

```python
eigvals[:6]           # the first six:  positions 0,1,2,3,4,5
err[:, :N_t]          # see below
B[va][j][:N_t]        # the first N_t entries -- the <phi> half of a trajectory
B[va][j][N_t:]        # from N_t to the end -- the <n> half
```

Leaving a side blank means "all the way." `[:6]` is "from the start to 6", `[N_t:]` is "from N_t to
the end", and `[:]` is everything.

For a 2-D array the two axes are separated by a comma — **`[rows, columns]`**:

```python
err[:, :N_t]      # ALL rows, and only the first N_t columns
A[:, 0]           # ALL rows, column 0 only -- the starting phi of every sample
(H - H_ladder).full()[:block, :block]    # the top-left block x block corner
```

`A[:, 0]` is worth staring at: `:` means every one of the 300 trajectories, `0` means the first
time-point of each. The result is 300 numbers — the starting position of every sample. That is
exactly how the code recovers `phi0` in Component 3.

## 1.10 Shape, and the `axis` argument

Every array knows its own dimensions:

```python
A.shape        # (300, 80) -- 300 rows, each 80 numbers long
```

When you summarise an array, `axis` says **which direction to collapse**:

```python
err.mean()             # one number: the average of everything
err.mean(axis=0)       # average DOWN the rows -> one number per column (80 of them)
err.mean(axis=1)       # average ACROSS the columns -> one number per row (300 of them)
```

The rule that makes it stick: **`axis` names the direction that disappears.** `axis=1` collapses
the columns, so what is left is one value per row. That is how Component 3 gets one error number
per trajectory: `.mean(axis=1)` over an array whose rows are trajectories.

## 1.11 Comparisons and boolean masks

A comparison on an array is applied to every element and gives back an array of `True`/`False`:

```python
which == b              # -> [False, True, True, False, ...] one per trajectory
```

That array of yes/nos is a **mask**, and it can be used as an index to keep only the `True` ones:

```python
s["per_traj"][which == b]        # only the errors of trajectories in bin b
s["per_traj"][which == b].mean() # ...and their average
```

This is how the binned table in Component 3 is built, and it replaces what would otherwise be a
loop with an `if` inside it.

## 1.12 Loops and `range`

```python
for i in range(N_s):
    phi0 = rng.uniform(phi_min - PHI_HALFWIDTH, phi_min + PHI_HALFWIDTH)
    A[i] = classical_sample(phi0, n0)
```

- `range(N_s)` produces 0, 1, 2, … up to `N_s - 1`.
- `for i in ...:` runs the indented block once per value, with `i` holding the current one.
- The indented body is the loop; the indentation is again the syntax.

You can also loop directly over the contents of a thing, without indices:

```python
for xb, yb in train_dl:          # each pass hands back one mini-batch of inputs and targets
for name, s in scores.items():   # each pass hands back one name and its scores
```

`zip` walks two lists side by side, one item from each per pass:

```python
for ax, op, name in zip(axes, [x_op, p_op, H], ["x", "p", "H"]):
```

That is "give me the first panel with the first operator and the first name, then the second of
each, …" — the standard way to fill a row of subplots.

## 1.13 List comprehensions — a loop written on one line

```python
means = np.array([s["per_traj"][which == b].mean() for b in range(N_BINS)])
```

Read it right-to-left: *for each `b` in `range(N_BINS)`, compute that average, and collect the
results into a list.* It is exactly equivalent to building an empty list and appending in a loop,
just shorter. The square brackets are what make it a list.

## 1.14 Dictionaries — lookup by name instead of by number

A list is indexed by position; a **dictionary** is indexed by a label you choose.

```python
scores = {}                                    # start empty
scores["copy-classical"] = dict(rms_phi=1.07, rms_n=0.36)
scores["copy-classical"]["rms_phi"]            # -> 1.07
```

Written out in full, with `{key: value}` pairs:

```python
states = {"Fock |1>": psi_fock, "Coherent": psi_coh}
```

Useful things to do with one:

```python
scores.items()      # walk through name-and-value pairs together
scores.keys()       # just the names
```

Dictionaries keep their insertion order, which is why the Component 3 results table always prints
copy-classical first and the MLP last — that is the order they were added.

## 1.15 Tuples and unpacking

Several values on one line, separated by commas, are a **tuple**, and they can be handed out to
several names at once:

```python
x0, p0 = 2.0, 0.0            # two boxes filled in one line
x, p = state                 # take a 2-element input apart into two names
best_val, best_epoch, best_state = np.inf, 0, None
r, p = trend[name]           # a function returned two things; name them both
```

A `*` swallows "everything else", which is how the code ignores the parts of a result it does not
need:

```python
W_lin, *_ = np.linalg.lstsq(X_tr, B_n[tr], rcond=None)
```

`lstsq` returns four things; this keeps the first and discards the rest. The underscore is a
conventional name meaning "I am deliberately not using this."

## 1.16 Objects, methods and dot notation

`a.b` means "the `b` belonging to `a`". Two flavours:

```python
sol.y            # an ATTRIBUTE: a piece of data stored inside sol
a.dag()          # a METHOD: an action you ask a to perform -- note the parentheses
```

Parentheses are the difference: `.shape` is a stored fact, `.mean()` is a computation you are
requesting. Methods can be chained left to right:

```python
(basis(N,0) + basis(N,1)).unit()      # add two states, then normalise the result
A[tr].mean(0)                          # take the training rows, then average them
```

## 1.17 Classes — a blueprint for an object

This is the one piece of "real programming" in the project, and it appears exactly once:

```python
class MLP(nn.Module):
    def __init__(self, d_in, d_h1, d_h2, d_out):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, d_h1), nn.ReLU(),
            nn.Linear(d_h1, d_h2), nn.ReLU(),
            nn.Linear(d_h2, d_out),
        )
    def forward(self, x):
        return self.net(x)
```

- `class MLP(nn.Module):` — define a new kind of object called `MLP`. The `(nn.Module)` means it
  **inherits** from PyTorch's `nn.Module`: it starts with all of that thing's abilities (tracking
  weights, moving to a GPU, switching between train and eval mode) already built in, for free.
- `def __init__(self, ...)` — the **constructor**, run once when you write `MLP(...)`. Its job is to
  set the object up. The double underscores mark it as a name Python treats specially.
- `self` — the object being built, passed in automatically. `self.net = ...` stores something
  **inside this particular object** so other methods can reach it later.
- `super().__init__()` — "run the parent's set-up first." PyTorch requires this; skipping it breaks
  the weight tracking silently.
- `def forward(self, x)` — the method PyTorch calls to push data through the network. You define
  what happens; you never call it directly.

Then `model = MLP(d_in, 128, 128, d_out)` builds one, and `model(xb)` runs data through it. The
line `model(xb)` looks like calling a function because `nn.Module` arranges for it to route to
`forward` — that is the convenience the inheritance buys.

## 1.18 `with` blocks — do something in a temporary mode

```python
with torch.no_grad():
    tr_loss = loss_fn(model(A_tr_t), B_tr_t).item()
```

"For the length of this indented block, turn off gradient tracking; turn it back on afterwards."
PyTorch normally records every operation so it can compute gradients for learning. When you are
only **measuring** performance, that recording is wasted work and memory, so it is switched off.
The block ends when the indentation ends.

## 1.19 `assert` — the check that stops you being wrong

```python
assert np.allclose(phi0_all, A[:, 0], atol=1e-9), "A[:,0] is not the sampled phi0"
```

"I claim this is true. If it is not, stop immediately and print that message." This is the project's
golden rule turned into code: never trust a number you cannot check. An assert that never fires
costs nothing; the one time it fires, it saves you from a plausible-looking wrong figure.

`np.allclose(a, b, atol=...)` is "are these two arrays equal to within this tolerance" — the right
way to compare decimals, since exact equality on floating-point numbers is unreliable.

## 1.20 `lambda` — a function with no name

```python
to_t = lambda x: torch.tensor(x, dtype=torch.float32)
```

Identical in effect to `def to_t(x): return torch.tensor(x, dtype=torch.float32)`, just written on
one line. Used when the function is a one-liner not worth a full definition.

## 1.21 The ten lines that unlock most of the code

If only a few things stick, make it these:

```python
x = 5                       # a labelled box
def f(a, b): return a + b   # a reusable machine
np.linspace(0, 1, 40)       # 40 evenly spaced numbers
arr[0]      arr[-1]         # first entry, last entry
arr[:10]    arr[10:]        # first ten, everything from ten on
grid[:, 0]                  # every row, first column
arr.mean(axis=1)            # collapse the columns -> one value per row
arr[mask]                   # keep only where mask is True
for i in range(n):          # repeat n times
d = {"name": value}         # look things up by label
```

---

# PART 2 — The `shared/` helper modules

Every notebook starts with the same two lines:

```python
from oscillator import setup
setup()
```

`oscillator` is the file `shared/oscillator.py`. The `shared/` folder is registered with the
project's virtual environment (via a `.pth` file in site-packages), so anything in it can be
imported from **any** assignment folder without copying it around. See `shared/README.md`.

There are three files.

### `group_plot_style.py` — `apply_group_style()`

Sets matplotlib's *defaults* once, so every plot follows the group's standards without configuring
each one: larger fonts (legible on a slide), `viridis` as the default colormap, viridis-sampled line
colours, thicker lines, a faint grid, high resolution on save. A one-line "make all my plots
consistent and slide-ready" switch.

### `output_routing.py` — `route_outputs()`

Makes saved files **sort themselves** into subfolders by type, so nothing is left loose at the top
level:

- `.png .jpg .pdf .svg` → `figures/`
- `.npy .npz .csv` → `data/`
- `.gif .mp4 .mov` → `movies/`

It does this by quietly wrapping `plt.savefig`, `np.save` and `imageio.mimsave` so that a **bare**
filename like `"energy.png"` gets the right folder prepended. A filename that already names a folder
is left alone, and missing folders are created. So you never edit your save lines — they land in
the right place on their own. This is why every `savefig` in the notebooks uses a bare name.

### `oscillator.py` — the physics and setup helpers

- **`setup()`** — calls `apply_group_style()` *and* `route_outputs()` together. One line at the top
  of a notebook does all styling and file routing.
- **`energy(x, p)`** — the classical energy `p²/2m + ½mω²x²`.
- **`hamilton_rhs(t, state)`** — the right-hand side of Hamilton's equations, `[p/m, −mω²x]`, in the
  shape `solve_ivp` expects.
- **`analytic_xp(t, x0, p0)`** — the exact classical solution, used to check the solver.
- **`build_operators(N)`** — builds the truncated quantum operators, returns `(a, adag, x, p, H)`.
- **`wigner_gif(states, tlist, fname, …)`** — turns a sequence of quantum states into an animated
  GIF of the Wigner function. The colour scale is genuinely fixed across frames via an explicit
  `np.linspace(-wmax, wmax, 81)` level array; passing `levels=80` with `vmin`/`vmax` does **not**
  work, because matplotlib ignores `vmin`/`vmax` when `levels` is an integer and rescales to each
  frame's own data. Frame delay is in **milliseconds** (imageio ≥ 2.28).

Running `python shared\oscillator.py` on its own executes a self-check that verifies the classical
solver against the analytic solution, energy conservation, the Wigner colour-scale invariant, and
the quantum spectrum against `Eₙ = ℏω(n+½)`. It prints PASS. **Run it after touching that file.**

**What the notebooks import versus define.** The notebooks import only `setup` (all three) and
`wigner_gif` (Component 2). The physics functions — `energy`, `hamilton_rhs`, the operator
construction — are **written out inline in the cells** so the work is visible and a reader can see
the physics rather than a black box. The same functions also live in `oscillator.py` as reusable
helpers. Same maths: written out where it is worth seeing, kept in `shared/` where it is worth
reusing.

---

# PART 3 — Component 1: `component1_classical.ipynb`

**Goal:** simulate a mass on a spring (the classical harmonic oscillator), then two harder versions
of it, and produce the *classical inputs* for the eventual machine-learning model.

The notebook has four tasks and they build on each other:

| Task | System | New idea |
|---|---|---|
| 1 | perfect spring | energy as a map over phase space |
| 2 | perfect spring | motion — integrating Hamilton's equations |
| 3 | spring + cosine term | the potential stops being a parabola |
| 4 | two coupled oscillators | four dimensions, Poincaré maps, and testing for chaos |

Study Guide §2.1–2.10 covers the concepts in the same order.

## 3.1 Task 1 — energy, and phase space

### Cell 1 (markdown) — Title and overview
States the goal (generate classical baseline data) and the four tasks. The key line is the project's
rule, *"never trust a number that cannot be verified"* — which is why the harmonic oscillator is
used at all: it has exact formulas to check against.

### Cell 2 (markdown) — Setup and conventions
Explains **natural units** ℏ = m = ω = 1, and notes a consequence: the energy contours, which are
ellipses in real units, become **circles** here.

### Cell 3 (code) — Imports and one-line setup
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
- The three `import` lines bring in NumPy (`np`), Matplotlib (`plt`) and the `solve_ivp` solver.
- `from oscillator import setup` pulls the `setup` helper out of your shared `oscillator.py`.
- `m = 1.0`, `omega = 1.0` fix the mass and frequency to 1. These boxes are reused throughout.
- `setup()` applies the group plot style **and** turns on output routing, so figures save into
  `figures/` and data into `data/` from bare filenames.

*Why:* loads the tools and fixes every convention in one line, so the rest of the notebook is
nothing but physics.

### Cell 4 (markdown) — Task 1(a): the energy function
States `E(x,p) = p²/2m + ½mω²x²` and names its two pieces: kinetic energy (motion) and potential
energy (spring).

### Cell 5 (code) — Define the energy and test it
```python
def energy(x, p, m=m, omega=omega):
    '''Classical energy (Hamiltonian) of the harmonic oscillator.'''
    kinetic = p**2 / (2.0 * m)
    potential = 0.5 * m * omega**2 * x**2
    return kinetic + potential

print("E(x=1, p=0) =", energy(1.0, 0.0), " (expected 0.5)")
print("E(x=0, p=1) =", energy(0.0, 1.0), " (expected 0.5)")
```
- `def energy(x, p, m=m, omega=omega):` defines the energy machine (§1.6). `**` is "to the power
  of", so `p**2` is `p²`.
- The `kinetic`/`potential` lines compute the two pieces; `return` hands back their sum.
- The two `print` lines test it against a case you can do in your head: at `(x=1, p=0)` all the
  energy is potential, `½·1·1²= 0.5`; at `(x=0, p=1)` it is all kinetic, `1²/2 = 0.5`. Seeing 0.5
  twice confirms the formula was typed correctly.

*Why:* this function is reused to draw the map (Cell 8) and to check energy conservation (Cell 17).

### Cell 6 (markdown) — Task 1(b): deriving Hamilton's equations
Pure maths. Shows how the energy generates motion through `ẋ = ∂H/∂p` and `ṗ = −∂H/∂x`, which here
become `ẋ = p/m` and `ṗ = −mω²x`. These are exactly what the solver in Task 2 uses.

### Cell 7 (markdown) — Task 1(c): what phase space is
Explains phase space — the plane of position against momentum, where one point is the entire state.

### Cell 8 (code) — Draw the energy map (contour plot)
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
- `np.linspace(-3,3,400)` makes the two axes; `np.meshgrid` combines them into a full 2-D grid;
  `energy(X, P)` evaluates the energy at all 160,000 points **at once** (§1.8).
- `ax.contourf(...)` draws the filled colour map; `ax.contour(..., colors="white")` overlays white
  lines at specific energies; `ax.clabel(...)` writes the value on each line.
- `fig.colorbar(..., shrink=0.82, pad=0.02)` adds the colour scale; `shrink` makes the bar shorter
  so its top number sits **below** the title instead of colliding with it.
- `set_aspect("equal")` makes one unit of x the same length on screen as one unit of p, so circles
  actually look circular.
- `plt.savefig("fig_c1_energy_contours.png", …)` — a **bare** filename, so output routing sends it
  to `figures/`.

**How to read this plot.** Axes are position and momentum; colour is total energy (dark = low,
yellow = high). The white rings are constant-energy curves — circles centred on the origin. An
oscillator with a given energy is locked onto its ring. A bigger ring means more energy. This is
energy conservation drawn as a picture.

### Cell 9 (markdown) — Caption
States the takeaway (constant-energy curves are closed loops the system cannot leave) and why they
are circles in natural units.

## 3.2 Task 2 — motion

### Cell 10 (markdown) — Task 2(a): a single trajectory
The contours show *where* the system can be; now compute *how it moves* by integrating Hamilton's
equations.

### Cell 11 (code) — Solve and plot one trajectory (with an exact check)
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
```
- `def hamilton_rhs(...)` is the "rule of motion". `solve_ivp` calls it over and over; it unpacks the
  current `state = [x, p]` (§1.15) and returns the two rates of change.
- `T = 2*np.pi/omega` is one full period; `t_span` runs for two; `t_eval` is the 600 times to
  record. The `*` in `np.linspace(*t_span, 600)` **unpacks** the pair into two separate arguments.
- `sol = solve_ivp(...)` marches the motion forward. Afterwards `sol.t` holds the times, `sol.y[0]`
  the positions and `sol.y[1]` the momenta. `rtol`/`atol` set how accurate to be.
- The `x_exact`/`p_exact` lines compute the known pen-and-paper answer, and `max_dev` is the largest
  gap between computed and exact. It comes out ≈ 7e-9 — the solver is verified, not assumed.

**How to read this plot.** The solid blue curve is the computed orbit — a closed circle, so the
oscillator returns to its start each period. The dashed white line (the exact formula) lies right on
top of it: visual proof the simulation is right. The red dot marks the start.

### Cell 12 (markdown) — Caption
One start point traces one closed loop — deterministic, energy-conserving motion.

### Cell 13 (markdown) — Task 2(b): many trajectories
We launch many starts at once to reveal the nested structure, and save the data for Component 3.

### Cell 14 (code) — Many random trajectories + save data
```python
rng = np.random.default_rng(42)
n_traj = 12
trajectories = []

for k in range(n_traj):
    x0 = rng.uniform(-2.5, 2.5)
    p0 = rng.uniform(-2.5, 2.5)
    sol = solve_ivp(hamilton_rhs, (0, T), [x0, p0], t_eval=np.linspace(0, T, 400),
                    method="RK45", rtol=1e-9, atol=1e-9)
    E0 = energy(x0, p0)
    color = cmap(E0 / 6.0)
    ax.plot(sol.y[0], sol.y[1], color=color, lw=1.6)
    trajectories.append(np.vstack([sol.t, sol.y[0], sol.y[1]]).T)

np.save("classical_trajectories.npy", data_array)
```
- `rng = np.random.default_rng(42)` creates a random generator **seeded** with 42, so the "random"
  starts are identical every run. Reproducibility is a group standard.
- `for k in range(n_traj):` repeats twelve times (§1.12). Each pass picks a random start, solves the
  orbit, computes its energy, picks a colour scaled by that energy, plots it, and appends
  `[time, x, p]` to the list.
- `ScalarMappable` + `colorbar` build the energy colour scale.
- `np.save("classical_trajectories.npy", …)` — a bare `.npy` name, so routing sends it to `data/`.
  The array is plain `float64` with shape `(12, 400, 3)` = (trajectory, time step, `[t, x, p]`), and
  an `assert` checks both. It used to be built with `dtype=object` under a "ragged array" comment,
  but every trajectory shares the same `t_eval` grid, so the stack is rectangular; the object
  version forced `allow_pickle=True` on every load for no reason.

**How to read this plot.** Nested circles, each coloured by its conserved starting energy. Orbits
never cross — a state has a unique future — and bigger energy means a bigger circle.

### Cell 15 (markdown) — Caption
Restates: nested, non-crossing circles whose size is set by energy.

### Cell 16 (markdown) — Sanity-check intro
We are about to verify that energy is genuinely conserved along a trajectory.

### Cell 17 (code) — Energy-conservation check
```python
sol = solve_ivp(hamilton_rhs, (0, 4*T), [1.5, 0.5], t_eval=np.linspace(0, 4*T, 2000),
                method="RK45", rtol=1e-10, atol=1e-10)
E_t = energy(sol.y[0], sol.y[1])
drift = E_t.max() - E_t.min()
assert drift < 1e-6, "Energy not conserved -> tighten solver tolerances!"
print("PASS: energy is conserved -> the numerical pipeline is trustworthy.")
```
- Solve one orbit for four periods at tight tolerances, compute the energy at every recorded time,
  and take `drift` = max − min: how far it wandered when it should not have moved at all.
- `assert drift < 1e-6, "..."` is the automatic check (§1.19). It passes at ≈ 1.9e-9.

### Cell 18 (markdown) — Takeaways for Tasks 1–2
Summarises Tasks 1–2 and names the outputs. It hands off to **Tasks 3–4 below**, not to Component 2
— the notebook continues.

## 3.3 Task 3 — the cosine (nonlinear) oscillator

The potential gains a cosine term: `H = p²/2m + ½mω²x² − V₀cos(kx)`. It is no longer a parabola, so
the orbits are no longer ellipses. Study Guide §2.9.

- `energy_cos`, `rhs_cos` — the energy and Hamilton's equations for the new potential. The only new
  piece against Task 1 is the `V₀ k sin(kx)` force term, which is the cosine's contribution to
  `−dU/dx`.
- **(b)** loops over several starting energies, integrates each with `solve_ivp`, and overlays the
  orbits coloured by energy → `fig_c1_cosine_trajectories.png`.
- `p_from_energy` — inverts the energy formula to place a start point at a chosen `(x, E)`, so a
  trajectory can be launched onto a specific energy contour rather than wherever it happens to land.
- **(c)** draws many initial conditions inside an energy band and colours them with a `viridis`
  colorbar → `fig_c1_cosine_energy_band.png`.

## 3.4 Task 4 — two coupled oscillators and Poincaré maps

Two oscillators pushed together with a `λ p₁p₂` coupling. The state is now four numbers,
`[x1, p1, x2, p2]`, so phase space is 4-D and cannot be drawn directly. Study Guide §2.10.

- `energy_coupled`, `rhs_coupled` — energy and equations of motion for the pair.
- `solve_p1` — given `(x1, x2, p2)` and a target energy, solves the resulting quadratic for `p1`, so
  every trajectory can be started exactly **on** the chosen energy surface.
- **(b)** integrates one trajectory and plots the four 2-D projections of the 4-D phase space →
  `fig_c1_coupled_projections.png`.
- **(c)** overlays `(x1,p1)` and `(x2,p2)` for an energy band, coloured by energy →
  `fig_c1_coupled_energy_band.png`.
- **(b continued)** A second projection figure at **three** energies, `E₀ = 1, 3, 12` →
  `fig_c1_coupled_projections_energies.png`. The handout asks for the projections to be repeated
  across energies with the trend described, not just drawn once. Each row asserts energy conservation
  (`np.ptp(...) < 1e-6`) before plotting, so a row that silently drifted off its energy surface would
  stop the notebook rather than produce a misleading panel. **What it shows:** the accessible region
  grows with `E₀` in all four projections — fastest in `(p1,p2)`, since the coupling acts through the
  momenta — while the curves stay smooth and nested at every energy. That is the visual counterpart
  of the Lyapunov result in (d).
- **(d)** `poincare_section` — launches many trajectories at one energy and records `(x1,p1)` every
  time the orbit crosses `x2 = 0` **going one way**, using `solve_ivp`'s event mechanism →
  `fig_c1_coupled_poincare.png`.

Three things here were got wrong first and are worth understanding, because they are the kind of
mistake that produces a believable figure:

- *A proper Poincaré map needs several initial conditions per energy.* A single trajectory draws one
  curve and hides all the structure.
- *And it needs one consistent crossing direction.* The event uses `direction = 1`, i.e.
  `dx2/dt > 0`. That is **not** the same as `p2 > 0` here, because the coupling is in the momenta:
  `dx2/dt = p2/m + λp1`. Filtering on `p2 > 0` instead let 3.2% of crossings through in the
  opposite direction (158 of 4,971, measured across both energies), overlaying two different sections and smearing the curves.
- **What the figure actually shows.** Nested tori at *both* `E = 1` and `E = 12` — regular motion,
  **not** an order-to-chaos transition. That was checked with the maximal Lyapunov exponent
  (`λ_max ≈ 0.004–0.007`, i.e. zero within the `log t / t` convergence floor), not by eye. The
  nonlinearity is a bounded cosine while the harmonic term grows without limit, so higher energy
  makes this system *more* nearly integrable. Chaos does appear if the **coupling** is raised
  instead: `λ = 0.8, V₀ = 8, E = 12` gives `λ_max = 0.11`. See Study Guide §2.10 and
  `Findings_and_Corrections.md` §2.

---

# PART 4 — Component 2: `component2_quantum.ipynb`

**Goal:** compute the *quantum* version of the same oscillator — its allowed energies and how its
states move in time — with QuTiP, checked against exact formulas. These are the *prediction targets*
for Component 3.

> **New idea:** position and momentum become **operators** (matrices), and a quantum **state** is a
> column of numbers (a vector). QuTiP handles these as objects, so the code stays readable.

| Task | What it produces | New idea |
|---|---|---|
| 1 | the energy spectrum | operators, eigenvalues, truncation |
| 2 | three evolving states + Wigner movies | the Schrödinger equation, quasi-probability |
| 3 | the real fluxonium qubit | a system with no exact answer to check against |

## 4.1 Task 1 — operators and the energy spectrum

### Cell 1 (markdown) — Title and overview
States the goal and the big shift: classically the oscillator is a point on an ellipse;
quantum-mechanically it is a fuzzy blob and energy comes in fixed steps.

### Cell 2 (markdown) — Setup and conventions
Same natural units, and introduces **truncation**: keep the lowest `N` energy levels so every
operator is a finite `N×N` matrix.

### Cell 3 (code) — Imports and one-line setup
```python
import qutip
from qutip import destroy, basis, coherent, sesolve, wigner   # only what this notebook uses
from oscillator import setup

hbar = 1.0; m = 1.0; omega = 1.0
N = 30                       # number of energy levels kept (Hilbert-space truncation)
setup()
```
- The `from qutip import ...` line pulls in exactly the quantum tools used: `destroy` (the
  annihilation operator), `basis`/`coherent` (states), `sesolve` (the Schrödinger solver) and
  `wigner`.
- `N = 30` keeps the lowest 30 energy levels, so every operator becomes a 30×30 matrix. This is the
  truncation from Study Guide §4.8 — the infinite ladder cut off somewhere a computer can handle.

### Cell 4 (code) — Environment check
```python
qutip.about()
```
Prints the QuTiP / NumPy / SciPy versions and the install path. Pure diagnostics, no figure.

### Cell 5 (markdown) — Task 1(a): building the operators
Gives the formulas for `x̂, p̂, Ĥ` from the ladder operators `â` and `â†`; in natural units the
prefactor is `1/√2`.

### Cell 6 (code) — Build x̂, p̂, Ĥ and verify them
```python
a = destroy(N)
adag = a.dag()
x_op = (a + adag) / np.sqrt(2)
p_op = -1j * (a - adag) / np.sqrt(2)
H = p_op**2 / (2*m) + 0.5 * m * omega**2 * x_op**2
H_ladder = hbar * omega * (adag * a + 0.5)
block = N // 2
diff_low = np.abs((H - H_ladder).full()[:block, :block]).max()
```
- `a = destroy(N)` builds the **annihilation operator** `â` as a 30×30 matrix. Everything else is
  assembled from it. `a.dag()` is the **creation operator** `â†` (dagger = conjugate-transpose).
- `x_op`, `p_op` — position and momentum built from the ladder operators. `1j` is Python's `i`.
- `H` is the Hamiltonian assembled from `x̂` and `p̂`; `H_ladder` is the same Hamiltonian written the
  elegant way, `ℏω(â†â + ½)`. Both are built **specifically so they can be compared** — this is the
  golden rule again.
- `block = N // 2` is whole-number division → 15. `(H - H_ladder).full()[:block, :block]` compares
  the two only on the trustworthy lower 15×15 corner (§1.9) and prints ~0. The full-matrix
  difference prints 15, which comes entirely from the truncation edge and is reported honestly
  rather than hidden.

> **Concepts (Study Guide):** what it means for `x̂` and `p̂` to *be operators* rather than numbers;
> why `â`/`â†` form a *ladder*; what the *Fock basis* is.

### Cell 7 (code) — Picture the operator matrices
```python
for ax, op, name in zip(axes, [x_op, p_op, H], [r"$|\hat x|$", r"$|\hat p|$", r"$|\hat H|$"]):
    im = ax.imshow(np.abs(op.full()), cmap="viridis")
```
- `plt.subplots(1, 3, …)` makes three side-by-side panels; the `zip` loop (§1.12) fills them.
- `ax.imshow(np.abs(op.full()), …)` draws the matrix as an image — one coloured pixel per entry,
  brightness set by that entry's size. `.full()` converts the QuTiP object into a plain grid.

**How to read this plot.** Each panel is a 30×30 grid; bright means large, dark purple means zero.
**Ĥ (right)** has colour only on the diagonal → each level has one definite energy. **x̂ and p̂
(left, middle)** have colour only just off the diagonal → they connect a level only to its immediate
neighbours. That off-diagonal stripe *is* the ladder, drawn.

### Cell 8 (markdown) — Caption
Explains the diagonal-versus-off-diagonal structure and what it means physically.

### Cell 9 (markdown) — Task 1(b): the energy spectrum
The allowed energies are the eigenvalues of `Ĥ`, with exact answer `Eₙ = ℏω(n+½)`.

### Cell 10 (code) — Compute and plot the energy levels
```python
eigvals = H.eigenenergies()
n_index = np.arange(N)
analytic = hbar * omega * (n_index + 0.5)
```
- `H.eigenenergies()` asks QuTiP for the **eigenvalues** of the Hamiltonian — the allowed energies
  (§1.16 for the method call; Study Guide §3.4 for what an eigenvalue is).
- `np.arange(N)` is the level numbers 0…29, and `analytic` evaluates the exact formula at all of
  them in one line (§1.8).

**How to read this plot.** Horizontal is level number, vertical is energy. The blue circles sit
exactly on the red line for low levels → the code is correct. The line is straight and evenly
stepped (energies are discrete and equally spaced), and the lowest point is at 0.5, not 0 — the
zero-point energy.

### Cell 11 (code) — Spectrum sanity checks
```python
print(f"Ground-state energy E_0 = {eigvals[0]:.6f}  (expected 0.5 -> zero-point energy)")
spacing = np.diff(eigvals[:6])
n_reliable = N // 2
max_err_low = np.max(np.abs(eigvals[:n_reliable] - analytic[:n_reliable]))
assert abs(eigvals[0] - 0.5) < 1e-6, "ground state should be the zero-point energy 1/2"
assert max_err_low < 1e-6, "low spectrum should match exactly"
```
- `eigvals[0]` is the ground state (should be 0.5). `np.diff(eigvals[:6])` lists the gaps between
  the first six levels (should all be 1.0).
- `max_err_low` checks the lowest half against the exact formula, and the two asserts enforce it.
  High-`n` drift is expected truncation, and the final print says so rather than leaving you to
  wonder.

### Cell 12 (markdown) — Convergence-check intro
Explains the rule: always check convergence in `N`.

### Cell 13 (code) — Demonstrate truncation/convergence
```python
for N_test in [10, 30, 50]:
    a_t = destroy(N_test)
    ...
    err_t = np.abs(H_t.eigenenergies() - (np.arange(N_test) + 0.5))
    ax.semilogy(np.arange(N_test), err_t + 1e-18, marker="o", ms=3, label=f"N = {N_test}")
```
- Rebuild the operators at three truncation sizes and compute each level's error against the exact
  formula.
- `ax.semilogy(...)` plots on a **logarithmic** vertical axis, because the errors span 1e-16 to 1
  and a linear axis would show nothing. The `+ 1e-18` avoids taking the log of exactly zero.

**How to read this plot.** Each curve is one `N`. They sit near zero for low levels then shoot up
near the top of each truncation. Bigger `N` stays accurate further right (N=10→5, 30→15, 50→25 good
levels). The lesson: raise `N` until the levels you care about are well below the threshold.

### Cell 15 (markdown) — Task 1(c): what changed classical → quantum
A written comparison: same energy form and same ω, but energy became discrete with a nonzero floor,
and the point became a spread-out state.

## 4.2 Task 2 — evolving states and the Wigner function

### Cell 16 (markdown) — Task 2(a): three states and the Schrödinger equation
Introduces `iℏ d|ψ⟩/dt = Ĥ|ψ⟩` and the three states to evolve.

### Cell 17 (code) — Define the three states and evolve them
```python
psi_fock  = basis(N, 1)
psi_super = (basis(N, 0) + basis(N, 1)).unit()
psi_coh   = coherent(N, 1.5)

states = {"Fock |1>": psi_fock, "Superposition (|0>+|1>)/sqrt2": psi_super,
          f"Coherent |a={alpha}>": psi_coh}

for name, psi0 in states.items():
    res = sesolve(H, psi0, tlist, e_ops=[x_op, p_op], options={"store_states": True})
```
- `basis(N, 1)` is the pure level-1 state `|1⟩`. `(basis(N,0)+basis(N,1)).unit()` is the
  superposition, with `.unit()` rescaling so the total probability is 100% (§1.16 — method chaining).
- `coherent(N, 1.5)` is the classical-like coherent state.
- `states = {...}` is a **dictionary** (§1.14) pairing each name with its state, so the loop can
  carry the names along with the data.
- `sesolve(H, psi0, tlist, e_ops=[x_op, p_op], options={"store_states": True})` is the
  **Schrödinger-equation solver** — the quantum twin of `solve_ivp`. `e_ops` tells it to record the
  averages `⟨x̂⟩, ⟨p̂⟩` at each time (into `res.expect[0]`, `res.expect[1]`); `store_states` keeps
  the full state at each time (into `res.states`), which the movies need.

### Cell 18 (markdown) — Task 2(b): the Wigner function at t=0
Explains that the Wigner function draws a quantum state in the same `(x,p)` plane as the classical
data, and can go negative — the fingerprint of "non-classical".

### Cell 19 (code) — Wigner snapshots at t=0
```python
W = wigner(psi0, xvec, pvec)
wmax = np.abs(W).max()
cf = ax.contourf(xvec, pvec, W, levels=80, cmap="RdBu_r", vmin=-wmax, vmax=wmax)
```
- `wigner(psi0, xvec, pvec)` asks QuTiP for the Wigner quasi-probability over the grid.
- `wmax` sets a **symmetric** colour scale so that zero sits exactly at white. The colormap is
  **diverging** (`RdBu_r`: red positive, white zero, blue negative) — the one deliberate exception
  to the group's viridis rule, used because this data is *signed* and the sign is the whole point.

**How to read this plot.** **Coherent (right):** a single red Gaussian, no blue → the most classical
state. **Fock |1⟩ (left):** a red ring around a deep **blue** (negative) centre → strongly
non-classical. **Superposition (middle):** two lobes with alternating red/blue **interference
fringes** between them → proof of a true superposition rather than a random mixture.

### Cell 21 (markdown) — Task 2(c): animations
We animate each state over one period with the colour scale held fixed across frames, so that a
change in shape or sign is real and not a rescaling artefact.

### Cell 22 (code) — Wigner movies via the shared `wigner_gif()` helper
```python
from oscillator import wigner_gif
for name, res in results.items():
    safe = name.split()[0].lower()          # 'fock', 'superposition', 'coherent'
    path = wigner_gif(res.states, tlist, f"movies/wigner_{safe}.gif",
                      xvec=xvec, pvec=pvec, title=name)
```
- **This is where the shared helper earns its place.** Instead of ~30 lines of frame-rendering code
  in the notebook, the work lives in `shared/oscillator.py`.
- `name.split()[0].lower()` turns `"Fock |1>"` into the filename piece `"fock"`: `.split()` breaks
  the string at spaces into a list, `[0]` takes the first piece (§1.9), `.lower()` lowercases it.
- Internally `wigner_gif` samples ~40 time steps, computes the Wigner function at each, finds **one
  global maximum** so the colour scale is fixed across all frames, renders each frame, and stitches
  them with `imageio.mimsave`.

**How to read these animations.** **Coherent:** the blob orbits the centre like a classical
particle. **Fock |1⟩:** the ring rotates onto itself, so it looks unchanged — a *stationary* state.
**Superposition:** the fringes rotate, sweeping the lobes back and forth, which is the oscillation
of `⟨x̂⟩` that the next cell quantifies.

### Cell 25 (code) — Compare quantum averages to classical orbits
```python
for ax, (name, res) in zip(axes, results.items()):
    xq, pq = res.expect[0], res.expect[1]            # quantum averages over time
    x0, p0 = xq[0], pq[0]                             # matching classical start point
    csol = solve_ivp(classical_rhs, (0, T), [x0, p0], t_eval=tlist, rtol=1e-9, atol=1e-9)
```
- `res.expect[0]`, `res.expect[1]` are the quantum **averages** `⟨x̂⟩(t)`, `⟨p̂⟩(t)` recorded earlier
  by `sesolve`. `x0, p0` is the average at `t=0`, and the classical orbit is launched from exactly
  there so the comparison is fair.

**How to read this plot.** **Coherent (right):** dashed blue lands exactly on the red circle → the
quantum average moves like a classical particle (Ehrenfest's theorem). **Superposition (middle):** a
smaller circle driven by interference. **Fock |1⟩ (left):** just a dot at the origin, since its
average position and momentum are zero for all time. Notice what the averages hide: all the ringed
structure the Wigner plot showed is gone. That is the point of the following discussion cell.

### Cells 26–28 (markdown) — Discussion, reflection, takeaways
When quantum motion looks classical (coherent states, via Ehrenfest), what averaging throws away
(spread, uncertainty, interference), the one-page written reflection, and the list of outputs.

## 4.3 Task 3 — the fluxonium qubit

The step from a textbook oscillator to a **real superconducting qubit**. Tasks 1–2 had an exact
formula behind every number; this one does not, which is why it comes last — the confidence built
earlier is what makes it defensible. Study Guide §4.13.

```python
fluxonium = scq.Fluxonium(EJ=E_J, EC=E_C, EL=E_L, flux=flux_frac, cutoff=110)
H_flux = qt.Qobj(fluxonium.hamiltonian())
```
- `scq.Fluxonium(...)` builds the qubit with **scqubits**; `.hamiltonian()`, `.phi_operator()` and
  `.n_operator()` are wrapped as QuTiP `Qobj`s so the same objects serve both the spectrum and the
  dynamics.

**Coordinate convention — the thing to get right.** `scqubits` uses
`U(φ) = ½E_L φ² − E_J cos(φ + φ_ext)`, so at half flux the wells sit at `φ ≈ ±2.85` and **`φ = 0` is
the barrier top**. The cell computes `phi_min` by minimising `fluxonium.potential(...)`, and
everything downstream — the plotted curve, the classical trajectory, the packet centres, the sweep —
is expressed in that same `φ`. Writing the potential as `½E_L(φ − φ_ext)² − E_J cos φ` instead is the
same physics in a coordinate shifted by `φ_ext`; mixing the two silently compares a classical
trajectory against a quantum state half a flux quantum away. This was a real bug —
`Findings_and_Corrections.md` §1.

- **(b)** `fluxonium.wavefunction(esys, which=j, phi_grid=...)` plots the eigen-wavefunctions over
  the potential → `fig_c2_fluxonium_spectrum.png`: a double well with a tunneling doublet.
- `wave_packet(phi0, n0)` — a Gaussian packet, i.e. a coherent state of the fluxonium's LC mode,
  displaced so `⟨φ⟩ = phi0` and `⟨n⟩ = n0`.
- `classical_traj` — the matching classical trajectory, `dφ/dt = 8E_C n` and
  `dn/dt = −(E_L φ + E_J sin(φ + φ_ext))`. That second term is `−dU/dφ` for **scqubits' own**
  potential, which is what makes this the classical limit of `H_flux` rather than a shifted copy.
- **(d)** `qt.sesolve(H_flux, packet, tlist, e_ops=[phi_op, n_op, H_flux])` evolves the packet and
  returns `⟨φ̂⟩(t), ⟨n̂⟩(t), ⟨Ĥ⟩(t)`, plotted against the classical trajectory →
  `fig_c2_fluxonium_dynamics.png` (`⟨Ĥ⟩` conserved to 2.1e-7). The packet starts at the well minimum
  **with a charge kick `n0_kick = 0.5`** — at the minimum with `n0 = 0` the classical particle sits
  at an equilibrium point and never moves, which would make the comparison meaningless. The two
  agree for about half a period and then separate, and the reason is Ehrenfest's theorem losing its
  condition (Study Guide §4.11), not vague "packet spreading".
- **(e continued)** `E_classical(phi0, n0)` computes the classical energy `E₀ = H(x₀,p₀)` the handout
  asks for, and prints it for every launch alongside the barrier height, so "trapped in one well" vs
  "can cross" is a printed comparison rather than something inferred from the picture. Only the
  `φ₀ = 0` launch clears the barrier — which is exactly why its classical partner sweeps a
  figure-eight in the next figure while the others stay put. Note the coordinate: the handout writes
  `x₀ = φ₀ − φ_ext`, which belongs to *its* convention; in scqubits' coordinate the matching classical
  start is `x₀ = φ₀` with **no shift**. Using the handout's formula with scqubits' Hamiltonian is
  precisely the bug in `Findings_and_Corrections.md` §1.
- **(f)** sweeps `phi0` from one well, across the barrier, to the other —
  `{−2.85, −1.43, 0, 1.43, 2.85}` in scqubits' coordinate, same charge kick throughout →
  `fig_c2_fluxonium_sweep.png`. The middle panel (`phi0 = 0`, the barrier top) is the striking one:
  the classical point sweeps a figure-eight through both wells while the quantum packet splits and
  stays put. There is no classical version of that.

---

# PART 5 — Component 3: `component3_ml.ipynb`

**Goal:** train a neural network to predict the **quantum** fluxonium trajectory from the matching
**classical** one. This is the payoff: Components 1 and 2 make the data, this one learns the map.

Study Guide Part 5 explains every machine-learning term in plain words. This part explains the code.

**The shape of the whole notebook**, so the cells have somewhere to sit:

| Section | What happens |
|---|---|
| (a) | fix the fluxonium parameters, and derive the matching classical ones |
| (b, c) | generate 300 paired trajectories: classical `A` in, quantum `B` out |
| (d) | standardize, split into train/validation, define the MLP |
| training | train to early stopping, keeping the best weights |
| results | loss curve, one example prediction |
| (e) | **baselines** — three simpler methods scored the same way |
| (f) | **error against a physical axis** — where does the map fail? |

Sections (e) and (f) are what turn a loss number into a result. Without them, "validation MSE
9.3e-4" is a number with nothing to compare against.

## 5.1 Cells 1–2 (markdown) — Title, goal, and the data-source note

States the goal and records where each side of the data comes from. The important claim: `A` and `B`
share the same Hamiltonian, the same coordinate and the same starting point, and differ **only** in
classical versus quantum. That is what makes whatever the network learns *the quantum correction*
and nothing else.

## 5.2 Cell 3 (code) — Imports and setup

```python
import scqubits as scq          # fluxonium Hamiltonian (quantum targets)
import qutip as qt              # Schrodinger solver (sesolve)
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from oscillator import setup

setup()
torch.manual_seed(0)            # reproducible weights and shuffling
rng = np.random.default_rng(0)  # reproducible random initial conditions
```
- `torch` is PyTorch; `torch.nn` holds the neural-network building blocks and is conventionally
  shortened to `nn`.
- `TensorDataset` and `DataLoader` wrap arrays as tensors and serve them in shuffled mini-batches.
- **Two separate random seeds, on purpose.** `torch.manual_seed(0)` fixes PyTorch's randomness (the
  starting weights, the batch shuffling); `default_rng(0)` fixes NumPy's (the random initial
  conditions). They are independent streams, so both must be pinned for a run to be reproducible.

> **A tensor** is PyTorch's version of a NumPy array. Same idea — a grid of numbers — with two
> additions: it can live on a GPU, and it can remember the operations performed on it so gradients
> can be computed. Converting between the two is `torch.tensor(...)` one way and `.numpy()` back.

## 5.3 Cells 4–5 (markdown + code) — Shared parameters

```python
E_C = 1.0
E_J = 5.0 * E_C          # Josephson energy   (E_J/E_C ~ 5)
E_L = 0.5 * E_C          # inductive energy   (E_L/E_C ~ 0.5)
flux_frac = 0.5          # half-flux sweet spot
phi_ext = 2*np.pi*flux_frac

m     = 1.0 / (8.0 * E_C)
omega = np.sqrt(8.0 * E_C * E_L)
V0    = E_J; k = 1.0
```
Everything is measured in units of `E_C`, so `E_C = 1.0` by definition and the other energies are
ratios of it. The classical parameters are **derived from** the quantum ones rather than typed in
separately — one source of truth, so the two simulations cannot drift apart.

```python
fluxonium = scq.Fluxonium(EJ=E_J, EC=E_C, EL=E_L, flux=flux_frac, cutoff=80)
H_flux  = qt.Qobj(fluxonium.hamiltonian())
phi_op  = qt.Qobj(fluxonium.phi_operator())
n_op    = qt.Qobj(fluxonium.n_operator())
DIM     = H_flux.shape[0]
phi_zpf = abs(fluxonium.phi_operator()[0, 1])
```
- The fluxonium is built **once**, outside the loop. Building it 300 times would be the single
  slowest possible way to write this notebook.
- `cutoff=80` here against `110` in Component 2 Task 3: this notebook runs one `sesolve` per sample,
  hundreds of times, so it trades a little basis headroom for speed. 80 is still far above the 40–60
  the handout asks for, and the low levels that matter are converged.
- `phi_zpf` is the zero-point scale — the natural "size" of the ground-state blob — read off the
  `[0, 1]` entry of the φ matrix (§1.9: row 0, column 1). It is needed to build packets of the right
  width.

```python
_scan   = np.linspace(0, 6, 60001)
phi_min = _scan[np.argmin(fluxonium.potential(_scan))]     # right-hand well minimum (~2.85)
PHI_HALFWIDTH = 1.0
```
- **This is the one-source-of-truth fix in action.** Rather than writing `phi_min = 2.85` from
  memory, the code evaluates scqubits' *own* potential on a fine grid and finds where it is
  smallest. `np.argmin` returns the **position** of the smallest value (not the value itself), and
  that position is used to index back into `_scan` (§1.9).
- The leading underscore in `_scan` is a convention meaning "a throwaway working variable."

```python
N_t     = 40
T_class = 2.0 * np.pi / omega
t_final = 1.5 * T_class
tlist   = np.linspace(0.0, t_final, N_t)
```
40 time points per trajectory, running to 1.5 classical periods, on a **shared** time grid — the
classical and quantum runs are recorded at exactly the same instants, which is what allows them to
be paired element by element.

## 5.4 Cells 6–7 (markdown + code) — Generate the paired dataset

```python
def wave_packet(phi0, n0):
    """Gaussian packet centered at (phi0, n0): a coherent state of the fluxonium LC mode."""
    return qt.coherent(DIM, phi0/(2*phi_zpf) + 1j*n0/(2*n_zpf))
```
Builds the starting quantum state: a blob centred at `(phi0, n0)`. The argument is a **complex
number** — real part sets the phase position, imaginary part sets the charge — which is why `1j`
appears. Study Guide §4.10 on coherent states.

```python
def classical_sample(phi0, n0):
    def rhs(t, s):
        ph, nn = s
        return [8*E_C*nn, -(E_L*ph + E_J*np.sin(ph + phi_ext))]
    sol = solve_ivp(rhs, (0, t_final), [phi0, n0], t_eval=tlist, rtol=1e-9, atol=1e-9)
    return np.concatenate([sol.y[0], sol.y[1]])
```
- A function **defined inside** another function. `rhs` exists only while `classical_sample` runs,
  which is exactly right — nothing else needs it.
- The returned pair is Hamilton's equations for the fluxonium: `dφ/dt = 8E_C n` and
  `dn/dt = −(E_L φ + E_J sin(φ + φ_ext))`. That second term is `−dU/dφ` for **scqubits' own**
  potential. Writing it any other way would silently make this a different system.
- `np.concatenate([...])` glues the 40 φ values and the 40 n values into **one flat vector of 80
  numbers**. The network wants a flat list, not a 2-D structure — this is where that flattening
  happens, and it is why every later slice uses `[:N_t]` for φ and `[N_t:]` for n (§1.9).

```python
def quantum_sample(phi0, n0):
    res = qt.sesolve(H_flux, wave_packet(phi0, n0), tlist, e_ops=[phi_op, n_op])
    return np.concatenate([np.real(res.expect[0]), np.real(res.expect[1])])
```
The same 80-number layout, from the real Schrödinger solver. `np.real(...)` discards a numerically
tiny imaginary residue that expectation values of Hermitian operators pick up from rounding — they
are real in exact arithmetic.

```python
N_s = 300
A = np.zeros((N_s, 2 * N_t))    # classical inputs
B = np.zeros((N_s, 2 * N_t))    # quantum targets
phi0_all = np.zeros(N_s)        # starting position of each sample -- the physical axis below
for i in range(N_s):
    phi0 = rng.uniform(phi_min - PHI_HALFWIDTH, phi_min + PHI_HALFWIDTH)
    n0   = rng.uniform(-0.5, 0.5)
    phi0_all[i] = phi0
    A[i] = classical_sample(phi0, n0)
    B[i] = quantum_sample(phi0, n0)
```
- **Pre-allocate, then fill.** `np.zeros((300, 80))` reserves the whole grid up front and the loop
  writes row `i` each pass. This is the standard NumPy pattern.
- `phi0_all` records where each sample started. It is not used by the network at all — it exists
  purely so section (f) can plot error against a physical axis. Recording it during generation is
  much safer than trying to reconstruct it later.
- `phi0` is drawn from **inside a well** (`phi_min ± 1.0`). The earlier window `(−1.5, 1.5)` looked
  like it sat around a minimum, but in scqubits' coordinate it is centred on the **barrier top**, so
  every packet was launched where it splits and tunnels instead of orbiting. Fixing it roughly
  halved the classical-versus-quantum RMS error (≈2.1 → ≈1.05 rad).

```python
assert np.allclose(phi0_all, A[:, 0], atol=1e-9), "A[:,0] is not the sampled phi0"
```
**The golden rule as one line of code.** The classical trajectory starts at `phi0`, so column 0 of
`A` must *be* `phi0` (§1.9 — every row, first column). If input and label ever drift apart, this
stops the notebook instead of letting a plausible-looking wrong figure through.

## 5.5 Cells 8–9 (markdown + code) — Standardize, split, define the MLP

```python
n_train = int(0.8 * N_s)
perm = rng.permutation(N_s)
tr, va = perm[:n_train], perm[n_train:]
```
- `rng.permutation(300)` shuffles the numbers 0…299 into random order, and the slice splits them
  240/60 (§1.9). `tr` and `va` are **lists of row numbers**, so `A[tr]` means "the 240 training rows"
  and `A[va]` "the 60 validation rows."
- Shuffling first matters: taking the first 240 rows in order would work here only because the
  samples were already generated randomly, and relying on that is the kind of assumption that breaks
  silently later.

```python
A_mean, A_std = A[tr].mean(0), A[tr].std(0) + 1e-8
B_mean, B_std = B[tr].mean(0), B[tr].std(0) + 1e-8
A_n = standardize(A, A_mean, A_std)
B_n = standardize(B, B_mean, B_std)
```
- **Standardizing** means rescaling each of the 80 columns to have average 0 and spread 1, so no
  column dominates the loss just because its numbers happen to be bigger. Networks train far better
  on inputs of comparable size.
- `.mean(0)` averages **down the rows** (§1.10), giving one number per column — the average value at
  each time point.
- **The statistics come from the training rows only** (`A[tr]`), then are applied to everything.
  Using all 300 rows to compute them would leak information about the validation set into the
  preparation, and the validation score would flatter the model.
- The `+ 1e-8` guards against dividing by zero if some column never varies.

```python
to_t = lambda x: torch.tensor(x, dtype=torch.float32)
train_dl = DataLoader(TensorDataset(to_t(A_n[tr]), to_t(B_n[tr])), batch_size=32, shuffle=True)
```
- `to_t` is a one-line converter from NumPy to PyTorch (§1.20). `float32` is deliberate: NumPy
  defaults to 64-bit, PyTorch expects 32-bit, and mixing them raises an error.
- `TensorDataset` pairs each input row with its target row. `DataLoader(..., batch_size=32,
  shuffle=True)` hands them out 32 at a time in a fresh random order each pass. Updating the weights
  on small batches rather than all 240 rows at once is both faster and better for learning.

The `class MLP(nn.Module)` definition is dissected line by line in §1.17. In shape: 80 numbers in →
128 → 128 → 80 numbers out, with `nn.ReLU()` between the layers. ReLU ("rectified linear unit")
replaces negatives with zero; without something like it, stacking linear layers would collapse into
a single linear layer and the network could only ever learn straight-line maps.

## 5.6 Cells 10–11 (markdown + code) — Training with early stopping

This is the cell that changed most recently, so it is worth reading closely.

```python
loss_fn   = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

MAX_EPOCHS = 4000       # a ceiling, not a target -- early stopping decides when to quit
PATIENCE   = 400        # stop after this many epochs with no new validation minimum
```
- `nn.MSELoss()` is mean-squared error: average of (prediction − truth)². It is the number being
  minimised.
- `Adam` is the optimizer — the algorithm that decides how to nudge the weights given the gradients.
  `lr=1e-3` is the learning rate, i.e. how big a nudge.
- `model.parameters()` hands the optimizer every weight in the network. This works without you
  listing them because `nn.Module` tracked them all (§1.17).

```python
train_hist, val_hist = [], []
best_val, best_epoch, best_state = np.inf, 0, None
for epoch in range(MAX_EPOCHS):
    model.train()
    for xb, yb in train_dl:
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        optimizer.step()
```
- **An epoch** is one complete pass over all the training data. The inner loop walks the mini-batches
  within it, so there are two nested loops.
- The four lines inside are the heart of all neural-network training, in a fixed order:
  1. `optimizer.zero_grad()` — clear the gradients left over from last time. PyTorch **accumulates**
     gradients by default, so forgetting this silently adds every batch's gradient to the last one's.
  2. `loss = loss_fn(model(xb), yb)` — run the batch through the network and measure how wrong it is.
  3. `loss.backward()` — work backwards through the network computing, for every weight, which
     direction would reduce the loss.
  4. `optimizer.step()` — actually move the weights that way.
- `model.train()` puts the network in training mode. It matters for layers like dropout that behave
  differently while learning; this network has none, but the pairing with `model.eval()` is a habit
  worth keeping.

```python
    model.eval()
    with torch.no_grad():
        tr_loss = loss_fn(model(A_tr_t), B_tr_t).item()
        va_loss = loss_fn(model(A_va_t), B_va_t).item()
    train_hist.append(tr_loss); val_hist.append(va_loss)
```
- `model.eval()` + `with torch.no_grad():` (§1.18) — we are **measuring**, not learning, so gradient
  tracking is switched off. It is faster and makes the intent explicit.
- `.item()` pulls the single number out of a one-element tensor into an ordinary Python float.
- `.append(...)` adds to the end of a list, building the loss curves one epoch at a time.

```python
    if va_loss < best_val:
        best_val, best_epoch = va_loss, epoch
        best_state = {k: v.clone() for k, v in model.state_dict().items()}
    if epoch - best_epoch >= PATIENCE:
        print(f"early stop at epoch {epoch+1}: no improvement for {PATIENCE} epochs")
        break
```
**This is early stopping, and it is the answer to "how many epochs?"**

- Whenever the validation loss sets a new record low, save a **copy** of every weight.
  `model.state_dict()` is a dictionary of the network's weights; the comprehension (§1.13, applied to
  a dictionary) copies each one with `.clone()`. The `.clone()` is essential — without it you would
  store a reference to weights that keep changing, and end up saving the final state rather than the
  best one.
- `if epoch - best_epoch >= PATIENCE:` — if 400 epochs have passed since the last record, further
  training is not helping. `break` exits the loop immediately.
- The old version of this cell ran a fixed 150 epochs. The validation loss was still falling at 150,
  so the model was reported while **under-trained**. Early stopping removes the guess: training runs
  until improvement genuinely stops.

```python
model.load_state_dict(best_state)
```
**Load the best weights back in.** Training ran to epoch 2010 but the best model was at epoch 1610,
and those are two different networks. Without this line the notebook would report the epoch-1610
score while actually holding the epoch-2010 weights — the score and the model would disagree.

The prints then report the best validation MSE (1.47e-4 at epoch 1610), the training loss at that
same epoch, the train/validation gap, and — for comparison — what the old fixed 150-epoch cutoff
would have given (9.34e-4, i.e. 6.4× worse).

> **A caveat stated rather than buried.** The stopping epoch is chosen by looking at the validation
> set, so that set has now been used to make a decision and is no longer a completely untouched
> test. The honest name for 1.47e-4 is "best validation score", not "test score". A three-way
> train/validation/test split would remove the caveat at the cost of training on fewer samples.

## 5.6b The hyperparameter sweep — the handout's "explore" requirement

```python
SWEEP_MAX, SWEEP_PAT = 800, 150      # reduced ceiling: ranks configs without a 40-minute run

def train_cfg(width, lr, batch, seed=0):
    """Train one configuration to early stopping. Returns (best val MSE, best epoch)."""
```
The handout asks for the hidden widths to be explored *together with* learning rate, batch size and
epoch count. Epochs are already handled — early stopping picks them. This cell sweeps the other three.

Three design choices worth understanding:

- **One function, every configuration.** Identical split, identical early-stopping rule, identical
  scoring. The only thing that varies is the hyperparameter, so a difference cannot be an artefact of
  how it was measured.
- **A reduced ceiling (800 epochs, patience 150).** Enough to *rank* configurations in a few minutes;
  the absolute numbers come out slightly worse than the full run. So the sweep is used to **choose**,
  and the chosen setting is reported from the full early-stopped run.
- **One-factor-at-a-time, not a full grid.** Widths × learning rate first, then batch size at the
  winner. With 300 samples the split-to-split scatter is ~12%, so a finer grid would be reading noise.

**What it returned** (validation MSE at the 800-epoch ceiling; `@` is the best epoch):

| width \ lr | 3e-4 | 1e-3 | 3e-3 |
|---|---|---|---|
| 64 | 5.74e-4 @789 | 3.07e-4 @763 | 4.44e-4 @378 |
| **128** | 3.17e-4 @798 | **2.33e-4 @646** | 3.53e-4 @336 |
| 256 | 2.81e-4 @776 | 2.96e-4 @326 | 5.37e-4 @122 |

Batch size at width 128, lr 1e-3: **16 → 3.50e-4**, **32 → 2.33e-4**, **64 → 2.79e-4**.

**How to read it, and what it is honestly worth:**

- **Learning rate dominates.** At 3e-3 every width is worse, and the best epoch collapses (122 at
  width 256) — the optimizer is bouncing rather than converging. At 3e-4 the runs are still improving
  when the 800-epoch ceiling hits (best epochs 776–798), so those cells are under-trained rather than
  genuinely bad.
- **Width barely matters** over this range. That is the signature of a problem that is not
  capacity-limited — unsurprising when linear regression alone reaches 0.026 rad.
- **The spread across the whole grid is only 2.5×**, against a ~12% split-to-split scatter. So the
  broad shape (lr matters, width doesn't) is real; neighbouring cells are not meaningfully different.
- **The pre-existing configuration — 128 wide, lr 1e-3, batch 32 — came out best.** That is the useful
  outcome: the setting was already right, and now that is a measurement rather than an assumption.

## 5.7 Cells 12–13 — Loss curve and one example prediction

```python
n_run = len(train_hist)                     # epochs actually run, not MAX_EPOCHS
ax.semilogy(range(1, n_run + 1), train_hist, label="training MSE")
ax.axvline(best_epoch + 1, color="0.35", ls="--", lw=1.5, label=f"early stop: best epoch {best_epoch+1}")
ax.axvline(150, color="#d62728", ls=":", lw=1.5, label="old fixed cutoff (150)")
```
- `len(train_hist)` is used rather than `MAX_EPOCHS` because early stopping means the loop usually
  ends sooner. Hard-coding the ceiling here would draw an axis longer than the data.
- `semilogy` again for the logarithmic vertical axis — the loss falls by four orders of magnitude.
- The two `axvline` calls mark the new stopping point and the old one, so the plot itself shows why
  the change was needed.

**How to read this plot.** Both curves fall, with training falling faster, so a gap opens. A gap
alone is normal — what matters is whether the **validation** curve is still improving. At the red
dotted line (epoch 150) it clearly still is: that is what "under-trained" looks like. The spikes
later in the run are Adam taking a step that briefly breaks the fit; they recover within a few epochs
and never beat the minimum, which is exactly why the *best* weights are stored rather than the final
ones. A `ReduceLROnPlateau` scheduler would smooth them.

The prediction plot un-standardizes one held-out sample (`B_pred = B_pred_n * B_std + B_mean` —
multiplying and adding back exactly what standardizing divided and subtracted) and overlays the
classical input, the true quantum target and the MLP's prediction in phase space.

> ## Where the handout stops
>
> `quantum_researcher 4.pdf` assigns **Component 3 = Task 1, parts (a)–(d)** and ends there
> (p. 8 of 8). Everything from here on — walkthrough sections 5.7b through 5.10 — covers work
> that was **not** assigned. The notebook marks the same boundary with a full-width divider, and
> the four extras are named *Beyond the brief 1–4* rather than *(e), (f), (g)*, because the old
> lettering read as a continuation of the handout's own sub-tasks.

## 5.7b Beyond the brief 1 — the "which curve is the truth" figure

This section exists because of a question asked in the meeting, and the question was a fair one.
Component 2's fluxonium figure shows classical and quantum wildly apart; Component 3's prediction
figure shows the prediction sitting exactly on the quantum. Read side by side those look like
contradictory claims, and nothing on either figure said otherwise.

The code is short, and almost all of the work is in three lines.

```python
gap_phys  = float(np.sqrt(((Ain[:, :N_t]    - Btrue[:, :N_t]) ** 2).mean()))
gap_model = float(np.sqrt(((B_pred[:, :N_t] - Btrue[:, :N_t]) ** 2).mean()))
j = int(np.argsort(rms_per)[len(rms_per) // 2])
```

- **`gap_phys`** is the RMS distance between the *classical input* and the quantum truth. It comes
  out at **1.067 rad** — and that is not a coincidence, it is numerically identical to the
  `copy-classical` baseline in §5.8, because they are the same quantity computed the same way. The
  baseline is this gap as a number; panel (a) is this gap as a picture.
- **`gap_model`** is the RMS distance between the *prediction* and the same truth: **0.0057 rad**.
- **`j`** picks the **median** trajectory by error, via `argsort(...)[len//2]`. Using `argmin` would
  be cherry-picking, and a reader is entitled to assume you did unless the code says otherwise.

The plotting trick that makes the argument work is a single shared window:

```python
padx = 0.10 * (allx.max() - allx.min()); pady = 0.14 * (ally.max() - ally.min())
XL = (allx.min() - padx, allx.max() + padx); YL = (ally.min() - pady, ally.max() + pady)
...
a.set_xlim(*XL); a.set_ylim(*YL)      # identical limits on BOTH panels
```

Limits are computed once across all three curves and applied to panel (a) and panel (b) alike. If
matplotlib were left to autoscale, each panel would fit its own data and the two would end up at
different zoom levels — which would destroy the comparison, because the whole argument is *these are
the same window, look how differently they behave*.

Panel (c) then plots `resid[j] * 1000`. The `* 1000` converts radians to milliradians, and it is
doing real work: at 0.0057 rad the residual is invisible on any axis that also has to show a 1.8 rad
orbit. Rescaling the axis is what turns "the error is asserted in the text" into "the error is
visible in the figure", and the title states the magnification (186×) so nobody mistakes the
zoomed panel for a different measurement.

**The lesson worth keeping.** Two figures can each be individually correct and still mislead when
placed side by side, because a figure carries no statement about what it is *not* showing. The fix
is not a better caption — it is a figure whose axes make the comparison for the reader.

## 5.8 Beyond the brief 2 — the honest baselines

A validation MSE on its own means nothing: 9.3e-4 is small compared to *what*? A number becomes a
result only when something else is measured the same way on the same data.

```python
scores = {}

def score(B_hat, name):
    err      = B_hat - B[va]
    per_traj = np.sqrt((err[:, :N_t] ** 2).mean(axis=1))
    rms_phi  = np.sqrt((err[:, :N_t] ** 2).mean())
    rms_n    = np.sqrt((err[:, N_t:] ** 2).mean())
    mse_std  = (((B_hat - B_mean) / B_std - B_n[va]) ** 2).mean()
    scores[name] = dict(rms_phi=rms_phi, rms_n=rms_n, mse_std=mse_std, per_traj=per_traj)
    return scores[name]
```
- **One scoring function used for every model**, so no method can be flattered by being measured
  differently. `B_hat` is always in physical units.
- `err[:, :N_t]` is the `⟨φ̂⟩` half of every held-out row; `err[:, N_t:]` is the `⟨n̂⟩` half (§1.9).
  They are reported separately because averaging them together would hide *which* observable is
  being missed.
- `per_traj` uses `.mean(axis=1)` — collapse the columns, leaving **one error number per
  trajectory** (§1.10). Section (f) needs exactly that.
- `rms_phi` uses `.mean()` with no axis — collapse everything to a single number.
- **RMS**, root-mean-square, is square-root-of-the-average-of-the-squares: the typical size of the
  miss, in radians. Squaring first stops positive and negative errors cancelling.
- The results go into a dictionary keyed by model name (§1.14), which is what lets the table at the
  end print every model in one loop.

**Baseline 1 — copy the classical trajectory.**
```python
score(A[va], "copy-classical")
```
The do-nothing answer: hand back the classical input and call it the quantum prediction. Its error
*is* the size of the quantum correction — the very thing the project exists to predict. A model that
cannot beat this has learned nothing. It scores **1.067 rad**, matching the ≈1.02 rad recorded
independently in the research notes.

**Baseline 2 — linear regression.**
```python
X_tr = np.hstack([A_n[tr], np.ones((len(tr), 1))])
W_lin, *_ = np.linalg.lstsq(X_tr, B_n[tr], rcond=None)
lin_pred = np.hstack([A_n[va], np.ones((len(va), 1))]) @ W_lin
score(lin_pred * B_std + B_mean, "linear regression")
```
- `np.hstack([...])` glues arrays side by side; the column of ones it adds is the **intercept**, the
  constant offset the fit is allowed to add.
- `np.linalg.lstsq` solves the least-squares problem **exactly** — no training loop, no learning
  rate, no random seed, nothing to tune. `W_lin, *_ =` keeps the solution and discards the three
  extra diagnostics it returns (§1.15).
- `@` is matrix multiplication: apply the fitted map to the held-out inputs.
- **This is the strong baseline, and the interesting one.** It scores **0.026 rad** — a plain
  straight-line fit recovers most of the map. That makes physical sense: inside one well the motion
  is nearly harmonic, and the harmonic classical→quantum map really is linear. So the network's real
  job is the *nonlinear remainder*, and the honest claim for the MLP is that it beats linear
  regression by 4.5× **on RMS**.

  That qualifier matters, and the error-distribution figure is what exposed it. RMS squares before
  averaging, so it sits above the typical case by however far the tail pulls it: the straight-line
  fit's RMS is **3.6× its own median**, the network's only **1.3×**. Compare medians instead and the gap is
  **1.7×**; compare worst cases and it is **6.3×**. The network's real advantage is that it **fails less
  badly**, which a single number cannot show.

**Baseline 3 — k-nearest-neighbours.**
```python
dist2 = ((A_n[va][:, None, :] - A_n[tr][None, :, :]) ** 2).sum(-1)
nearest = np.argsort(dist2, axis=1)
for K in (1, 3, 5, 10):
    pred = B_n[tr][nearest[:, :K]].mean(axis=1) * B_std + B_mean
```
- The first line computes the distance from every held-out row to every training row at once. The
  `None` entries insert a length-1 axis so that a 60×80 array and a 240×80 array line up into a
  60×240×80 comparison — NumPy **broadcasting**. It is dense, but it replaces a double loop over
  14,400 pairs.
- `np.argsort` returns the **positions** that would sort each row, so `nearest[:, :K]` is the `K`
  closest training rows for each held-out row.
- Then average those neighbours' quantum answers. Pure lookup — no learned function at all.
- `K` is swept and the best kept, which deliberately makes this baseline as strong as it can be. An
  unfair baseline would produce a fake win. Best is `k=1` at **0.077 rad**, and it gets *worse* as
  `k` grows — which says the map is smooth and worth fitting rather than looking up, and that the
  MLP is not merely memorising training rows.

The final table prints all four models with RMS in φ, RMS in n, the standardized MSE, and the ratio
against copy-classical. The MLP wins at **0.0057 rad**, 186× better than copying.

## 5.9 Beyond the brief 3 — error against a physical axis

An average error says the model works *on average*. It does not say **where** — and "where" is the
actual scientific question.

```python
from scipy.stats import spearmanr
dist_va = np.abs(phi0_all[va] - phi_min)
N_BINS  = 5
edges   = np.linspace(dist_va.min(), dist_va.max(), N_BINS + 1)
which   = np.clip(np.digitize(dist_va, edges) - 1, 0, N_BINS - 1)
```
- `dist_va` is the physical axis: how far each held-out trajectory **started** from the bottom of
  the well. Near the minimum the potential is nearly a parabola and Ehrenfest's theorem is nearly
  exact, so classical and quantum should agree; further out the cosine bends the potential and they
  should diverge. Study Guide §4.11.
- `np.digitize` says which bin each value falls into, `−1` shifts to zero-based numbering, and
  `np.clip` pins the extreme values into the valid range so the topmost point does not fall off the
  end.
- `which` is then used as a mask (§1.11): `s["per_traj"][which == b]` is "the errors of the
  trajectories in bin `b`".

```python
trend = {name: spearmanr(dist_va, s["per_traj"]) for name, s in scores.items()}
```
**This line is the point of the whole cell.** A rising line in a plot is easy to see even when there
is no real trend, and this project has already been caught once claiming a trend that measurement
did not support (`Findings_and_Corrections.md` §2, the chaos claim). So the trend gets a number.

- **Spearman's rank correlation** `ρ` runs from −1 to +1: `+1` means the error climbs steadily with
  distance, `0` means no relationship at all.
- The **p-value** is the probability of seeing a correlation at least this large from pure noise.
  Below 0.05 the trend is worth believing; above it, the line in the plot is not evidence.

**What it actually returned:**

| model | ρ | p | verdict |
|---|---|---|---|
| copy-classical | +0.254 | 0.051 | not significant (marginal) |
| linear regression | −0.059 | 0.654 | not significant |
| k-NN | +0.077 | 0.559 | not significant |
| MLP | +0.077 | 0.559 | not significant |

**So the result is a null, and the figure title says so.** The first draft of this plot was titled
"prediction error grows with distance from the well bottom"; the measurement does not support that,
so it was retitled. Inside the sampled window every model is flat.

The reason is in the last two printed lines: the barrier top sits at `φ = 0`, which is 2.85 rad from
the minimum, and this dataset only samples out to 1.00 rad — **35% of the way there**. The breakdown
region was never in the data. Widening `PHI_HALFWIDTH` is the experiment that would locate the
boundary, and it should be run as a *separate* dataset so these numbers stay comparable.

The one trend that is nearly significant belongs to copy-classical — which measures the **size of
the quantum correction itself**, not any model's skill. It grows from 0.95 to 1.16 rad, exactly as
Ehrenfest's argument predicts. The network is simply still able to keep up with it.

## 5.10 Beyond the brief 4 — widening the window to the barrier (steps g1–g3)

Section (f) named the experiment it needed; this section runs it. Three cells.

### (g1) — the second dataset, and re-justifying the truncation

```python
rng_w = np.random.default_rng(1)          # separate stream; the narrow run keeps seed 0
PHI_LO_W, PHI_HI_W = 0.0, phi_min         # 0.0 = barrier top, phi_min ~ 2.85 = well minimum
```
- A **separate RNG stream** so the narrow dataset is bit-for-bit unchanged. Reusing `rng` would have
  advanced it and altered every later draw.
- Sampling is **one-sided**, `[0, φ_min]`, which fixes both flaws in (f): it reaches the barrier, and
  it makes the axis monotone instead of folding two regimes onto the same number (§5.9).

```python
flux_hi = scq.Fluxonium(..., cutoff=110)
...
assert worst < 5e-3, "cutoff=80 is not converged over the wider window -- raise it"
```
**This assert is the most important line in the cell.** The narrow run justified `cutoff=80` for
packets sitting near a well bottom. These packets start *higher* in the potential, where more of the
basis is occupied, so the old justification does not carry over — it has to be re-earned. The cell
rebuilds the fluxonium at `cutoff=110` and compares five trajectories spanning the window; they agree
to **8.2e-7 rad**. Had this failed, every number in (g2) and (g3) would have been an artifact of the
basis size rather than physics.

### (g2) — one protocol, both datasets

```python
def run_pipeline(A_raw, B_raw, seed):
    """Standardize -> 80/20 split -> MLP to early stopping -> score all four models."""
```
Cells (d)–(f) wrapped into a function, then called twice. The point is that a difference between the
two datasets **cannot be an artefact of how they were measured** — same standardization, same split
fraction, same architecture, same early-stopping rule, same scoring code.

> **A subtlety that was initially written up wrongly.** The function re-splits using its own seed, so
> its "narrow" numbers are a *fresh run*, not a replay of (e). The markdown first claimed they would
> "come back out unchanged"; they do not. Copy-classical moves 0.5 % but the MLP moves **12 %**
> (0.0057 → 0.0050). That is not a bug — it is the **split-to-split scatter**, and quoting it is more
> useful than the false reproducibility claim would have been: it tells you how big a difference has
> to be before it means anything.

### (g3) — the physical axis, done properly

```python
dist_w = phi_min - phi0_w[va_w]          # monotone: 0 = well bottom, phi_min = barrier top
```
Signed and one-directional, unlike (f)'s `np.abs(...)`.

```python
ax.set_yscale("log")                     # BEFORE any annotation
ax.text(..., transform=ax.transAxes)     # axes-fraction, immune to the scale change
```
These two lines are a bug fix worth understanding. The first version placed labels using
`ax.get_ylim()` while the axis was still **linear**, then switched to log. Those data coordinates
became meaningless, and `bbox_inches="tight"` expanded the saved canvas to include them — producing a
**1262 × 202,783 pixel** PNG that no image viewer will open. Nothing raised an error. Setting the
scale first and positioning text in axes fractions (0–1 across the axes, regardless of scale) makes
the placement immune.

**What the cell prints, and what it means:**

| model | well bottom | barrier | growth | ρ | p |
|---|---|---|---|---|---|
| copy-classical | 1.040 | 2.483 | 2.4× | +0.862 | 8.5e-19 |
| linear regression | 0.079 | 0.140 | 1.8× | +0.285 | 0.027 |
| k-NN | 0.085 | 0.152 | 1.8× | +0.229 | 0.079 |
| **MLP** | **0.0071** | **0.0372** | **5.2×** | **+0.399** | **0.0016** |

**(f)'s null was a limitation of the sampling, not a property of the map.** With the window reaching
the barrier the trend is significant for three of the four models. Note two things: copy-classical's
2.4× growth is the **quantum correction itself** getting larger (not any model failing), and the MLP
degrades *fastest* in relative terms while remaining by far the most accurate — its advantage is
biggest exactly where the physics is easiest.

## 5.11 Final cell (markdown) — Takeaways

The pipeline, the six-fold improvement from early stopping, the four-model comparison table, the
physical-axis result across both datasets, and the caveats stated out loud rather than buried.

---

# PART 6 — Quick reference

**Your shared modules (`shared/`):**
- `setup()` *(oscillator)* — group plot style + output routing, in one call.
- `energy(x, p)` *(oscillator)* — classical energy `p²/2m + ½mω²x²`.
- `hamilton_rhs(t, state)` *(oscillator)* — classical equations of motion, shaped for `solve_ivp`.
- `analytic_xp(t, x0, p0)` *(oscillator)* — exact classical `x(t), p(t)`, for checking.
- `build_operators(N)` *(oscillator)* — returns `(a, adag, x, p, H)` for an N-level oscillator.
- `wigner_gif(states, tlist, fname, …)` *(oscillator)* — animated Wigner GIF with a colour scale
  fixed across frames (explicit level array — an integer `levels` ignores `vmin`/`vmax`) and a frame
  delay in **milliseconds**.
- `apply_group_style()` *(group_plot_style)* — matplotlib defaults to the group's standards.
- `route_outputs()` *(output_routing)* — auto-sort saved files into `figures/ data/ movies/`.

**NumPy (`np`)** — arrays and maths:
`linspace`, `arange`, `zeros`, `array`, `meshgrid`, `concatenate`, `hstack`, `vstack`/`.T`,
`cos`/`sin`/`sqrt`/`abs`/`hypot`, `max`/`min`/`mean`/`std`/`diff`/`round`, `argmin`/`argmax`/
`argsort`, `digitize`, `clip`, `allclose`, `real`, `inf`, `save`, `linalg.lstsq`,
`random.default_rng` → `.uniform`/`.permutation`.

**Matplotlib (`plt` / `ax`)** — plotting:
`subplots`, `plot`, `scatter`, `contourf`/`contour`, `clabel`, `imshow`, `semilogy`, `axhline`/
`axvline`, `set_xlabel`/`set_ylabel`/`set_title`, `set_yscale`, `suptitle`, `legend`, `grid`,
`set_aspect`, `set_xlim`/`set_ylim`, `colorbar`/`set_label`, `cm.ScalarMappable`/`Normalize`,
`tight_layout`, `savefig`, `show`.

**SciPy** — `solve_ivp(rule, time_span, start, …)` steps a differential equation forward in time;
`stats.spearmanr(a, b)` returns the rank correlation and its p-value.

**QuTiP (`qt`)** — `about()`, `destroy(N)`/`create(N)`, `.dag()`, `basis(N, n)`, `.unit()`,
`coherent(N, alpha)`, `Qobj(...)`, `H.eigenenergies()`, `.full()`, `.norm()`,
`sesolve(H, psi0, tlist, e_ops=[...], options={...})`, `wigner(state, xvec, pvec)`, `expect`.

**scqubits (`scq`)** — `Fluxonium(EJ, EC, EL, flux, cutoff)`, `.hamiltonian()`, `.phi_operator()`,
`.n_operator()`, `.potential(...)`, `.eigenvals()`, `.eigensys()`, `.wavefunction(...)`, `Grid1d`.

**PyTorch (`torch` / `nn`)** — `manual_seed`, `tensor`, `no_grad()`, `nn.Module`, `nn.Sequential`,
`nn.Linear`, `nn.ReLU`, `nn.MSELoss`, `optim.Adam`, `.parameters()`, `.state_dict()`,
`.load_state_dict()`, `.clone()`, `.item()`, `.train()`/`.eval()`, `zero_grad()`, `backward()`,
`step()`, `TensorDataset`, `DataLoader`.

**IPython.display** — `display(...)`, `Image(filename=...)` to show the Wigner GIFs inline.

**Plain Python** — `def name(args):` … `return`; `class Name(Parent):`; `for x in things:`;
`if condition:`; `break`; `with ...:`; `{key: value}`; `[f(x) for x in things]`;
`lambda x: ...`; `print(...)`; `assert claim, "msg"`; `#` comment; `'''docstring'''`.

---

# PART 7 — Change log

*The two errors behind most of these changes are written up in `Findings_and_Corrections.md`.*

### 2026-08-13 — Component 3 baselines, early stopping, and this restructure

| Area | Was | Now |
|---|---|---|
| Document structure | Python crash course was 25 lines; Component 1 Tasks 3–4 and the fluxonium sat in a "NEW TASKS" appendix after Component 2 | Part 1 is a full Python primer; every task is documented in its own component's part, in task order |
| Component 3 depth | ~8 lines per cell group | line-by-line, matching Components 1–2 |
| Training | fixed 150 epochs | early stopping on the validation minimum, best weights restored (best epoch 1610, val MSE 1.47e-4 — 6.4× better) |
| Scoring | validation MSE alone | four models scored identically: copy-classical 1.067, k-NN 0.077, linear regression 0.026, MLP 0.0057 rad |
| Physical axis | not measured | error against `\|φ₀ − φ_min\|`, with Spearman ρ and p-values — a **null** inside the sampled window, because it reaches only 35% of the way to the barrier |
| `phi0` | not recorded | stored during generation as `phi0_all`, with an assert against `A[:, 0]` |

### 2026-07-29 — Reconciled with the code after the July audit

| Area | Was stale | Now |
|---|---|---|
| Component 1 intro | described "the two tasks" | four tasks; 3–4 are the nonlinear and coupled extensions |
| Trajectory saving | `dtype=object` "ragged array" | plain `float64`, shape `(12, 400, 3)`, loads without `allow_pickle` |
| Tasks 1–2 takeaways | handed off to Component 2 mid-notebook | hands off to Tasks 3–4, which follow |
| Poincaré section | crossings filtered on `p2 > 0` | event `direction = 1` (`dx2/dt > 0`) — the two differ when the coupling is in the momenta |
| Poincaré result | "regular tori (low E) vs. a chaotic sea (high E)" | regular at both energies, confirmed by Lyapunov exponent; chaos needs stronger coupling, not higher energy |
| `wigner_gif` | "fixed color scale" | explicit level array; frame delay in milliseconds |
| Fluxonium coordinate | `½E_L(φ−φ_ext)² − E_J cos φ` | scqubits' `½E_L φ² − E_J cos(φ+φ_ext)` throughout |
| Fluxonium dynamics | packet at `φ₀ = π/2`, no kick | starts at the well minimum with `n0_kick = 0.5` |
| Component 3 inputs | "the Component 1 Task 3 oscillator" | the classical limit of the *same* fluxonium Hamiltonian, same coordinate |
| Component 3 sampling | `φ₀ ∈ (−1.5, 1.5)` | `φ_min ± 1.0` — the old window was centred on the barrier top |
