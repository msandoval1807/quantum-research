# Setup guide

Everything needed to get this repository running from a clean machine. It takes about ten minutes,
most of which is `pip` downloading PyTorch.

If you only want to *read* the results, you do not need any of this — the notebooks are committed
with their outputs, and every figure is in `Assignment 1/figures/`. GitHub renders them in the
browser. Setup is for running and changing things.

---

## 1. Prerequisites

| | Version | Check with | If missing |
|---|---|---|---|
| **Python** | 3.12 or newer (developed on 3.14) | `python --version` | [python.org/downloads](https://www.python.org/downloads/) — on Windows tick **"Add Python to PATH"** in the installer |
| **git** | any recent | `git --version` | [git-scm.com](https://git-scm.com/downloads) |

Nothing else. No CUDA, no GPU — everything here runs on CPU in minutes.

> **Windows note.** The commands below are written for **PowerShell**. If a `python` command is not
> found but you installed Python from the Microsoft Store, use `py` instead of `python`.

---

## 2. Clone and create the environment

```powershell
git clone https://github.com/msandoval1807/quantum-research.git
cd quantum-research
python -m venv .venv
```

Activate it. **You must do this in every new terminal** — the prompt shows `(.venv)` when it worked:

```powershell
.venv\Scripts\Activate.ps1          # PowerShell
```

<details>
<summary>Other shells</summary>

```bash
.venv/Scripts/activate              # Windows, Git Bash
source .venv/bin/activate           # macOS / Linux
```
</details>

If PowerShell refuses with an execution-policy error, allow scripts for your user once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## 3. Install the dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` is a full lockfile — exact pinned versions of everything, including transitive
dependencies — so you get the same environment the results were produced in. The ones that matter:

| Package | What it does here |
|---|---|
| **numpy**, **scipy** | arrays, and `solve_ivp` for the classical trajectories |
| **matplotlib** | every figure |
| **qutip** 5.3 | quantum operators, Schrödinger evolution, Wigner functions |
| **scqubits** 4.3.1 | the fluxonium qubit — its Hamiltonian, spectrum and eigenstates |
| **torch** 2.13 (CPU) | the neural network in Component 3 |
| **jupyterlab** | the notebook interface |
| **imageio** | writes the Wigner animations as GIFs |

This step downloads a few hundred MB, mostly PyTorch. It is the slow part.

---

## 4. Make `shared/` importable — **do not skip this**

Every notebook starts with `import oscillator`, which lives in `shared/`. Python will not find it
unless you tell the environment where to look. The mechanism is a `.pth` file: a plain text file in
the environment's `site-packages` containing one directory path, which Python adds to its import
path at startup.

Run this from the repository root — it computes the absolute path for **your** clone, so it works
wherever you put the repo:

```powershell
python -c "import sysconfig, pathlib, os; p = pathlib.Path(sysconfig.get_paths()['purelib']) / 'quantum_research_shared.pth'; p.write_text(os.path.abspath('shared')); print('wrote', p, '->', os.path.abspath('shared'))"
```

<details>
<summary>Why a .pth file rather than editing PYTHONPATH</summary>

A `.pth` file lives inside the virtual environment, so it applies automatically to the notebooks,
the terminal, and anything else that uses this interpreter — with no per-terminal setup and nothing
to remember. It also disappears when you delete `.venv`, so it leaves no trace on your system.

The path inside it is absolute and machine-specific, which is exactly why it is **not** committed:
the copy on someone else's machine would point at a directory you do not have.
</details>

---

## 5. Verify

```powershell
python shared\oscillator.py
```

Expected output, exactly:

```
PASS: classical solver, energy conservation, Wigner scale, quantum spectrum.
```

That one command checks four independent things: the numerical solver against the exact analytic
solution, energy conservation over several periods, the Wigner colour-scale invariant, and the
quantum spectrum against `Eₙ = ℏω(n+½)`. **If it prints PASS, your environment is correct.**

If it fails, see [Troubleshooting](#8-troubleshooting).

---

## 6. Launch Jupyter Lab

```powershell
jupyter lab
```

A browser tab opens. Navigate to `Assignment 1/` and open the notebooks.

To run one: **Kernel → Restart Kernel and Run All Cells**. Runtimes on a normal laptop:

| Notebook | Runtime | Why |
|---|---|---|
| `component1_classical.ipynb` | ~20 s | ODE integration only |
| `component2_quantum.ipynb` | ~30 s | plus three Wigner animations |
| `component3_ml.ipynb` | **~11 min** | trains ~14 neural networks, not one |

Component 3 is slow on purpose: the main model runs to early stopping, then a 3×3 width/learning-rate
sweep, then three batch sizes, then the whole pipeline again on a second dataset. It is working, not
hung — figures appear as it goes.

> **Do not edit a notebook on disk while a Jupyter tab has it open.** The tab overwrites the file
> when it saves. Close the tab *without saving* first, then reopen.

---

## 7. What to read, in order

1. **[`reference/PROJECT_CONTEXT.md`](reference/PROJECT_CONTEXT.md)** — what the project is and why.
2. **The three notebooks**, in order. Component 1 makes the classical data (model inputs),
   Component 2 makes the quantum data (model targets), Component 3 learns the map between them.
3. **[`Assignment 1/Code_Walkthrough_Components_1_to_3.md`](Assignment%201/Code_Walkthrough_Components_1_to_3.md)**
   — every cell explained, including a Python-from-zero section.
4. **[`Assignment 1/Classical_and_Quantum_Mechanics_Study_Guide.md`](Assignment%201/Classical_and_Quantum_Mechanics_Study_Guide.md)**
   — the physics from first principles. Assumes no formalism background.
5. **[`Assignment 1/Findings_and_Corrections.md`](Assignment%201/Findings_and_Corrections.md)** — the
   errors found during review and how each was caught. Read this before trusting any number.

`Assignment 1/Handout_Compliance.md` maps every assignment requirement to where it is satisfied.

**One convention worth knowing before you change anything:** the notebooks are the source of truth.
`Assignment 1/figures/` contains *only* files written by a notebook cell — never anything hand-made.
The slide deck embeds those PNGs unmodified and is rebuilt with `node build_deck.js` in
`Assignment 1/slides/` (needs Node.js and `npm install pptxgenjs`). Do not create a second copy of
plotting code.

---

## 8. Troubleshooting

**`ModuleNotFoundError: No module named 'oscillator'`**
Step 4 was skipped, or you created the `.pth` while a different environment was active. Confirm the
file exists and holds the right path:

```powershell
python -c "import sysconfig, pathlib; p = pathlib.Path(sysconfig.get_paths()['purelib']) / 'quantum_research_shared.pth'; print(p.exists() and p.read_text())"
```

It must print the absolute path to *your* `shared/` directory. If it prints someone else's path, or
`False`, re-run step 4.

**`ModuleNotFoundError` for numpy, torch, qutip …**
The environment is not active — check for `(.venv)` in your prompt — or step 3 did not finish.

**Jupyter cannot find the packages, but the terminal can**
Jupyter is using a different kernel. With the environment active:

```powershell
python -m ipykernel install --user --name quantum-research
```

Then in the notebook: **Kernel → Change Kernel → quantum-research**.

**PowerShell: "running scripts is disabled on this system"**
See the `Set-ExecutionPolicy` command in step 2.

**`pip install` fails on torch**
The pinned CPU build may not exist for your platform. Install it separately, then re-run step 3:

```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Component 3 seems frozen**
Give it ~11 minutes. It trains roughly fourteen models. Watch `Assignment 1/figures/` — file
timestamps update as it progresses.

**A notebook shows different numbers than the committed version**
Expected, within limits. Train/validation splits are random, so the MLP's error moves about **12%**
run to run. A difference smaller than that is noise, not a change. Everything with an exact formula
behind it — spectra, energy conservation, the well positions — should reproduce to the digits shown.

---

## 9. Quick reference

```powershell
.venv\Scripts\Activate.ps1                 # activate (every new terminal)
python shared\oscillator.py                # verify the environment -> PASS
jupyter lab                                # open the notebooks
cd "Assignment 1\slides"; node build_deck.js   # rebuild the slide deck
```
