# Project Context — AI Design of Quantum Processors

*An onboarding file so a collaborator can understand the whole project quickly. Last updated: 2026-07-29.*

> **Companion documents.** `Assignment 1/Findings_and_Corrections.md` records two errors found
> during the July review, how each was caught, and what changed as a result — worth reading
> alongside this file.
> `Research_ClassicalToQuantum_ML.md` surveys the literature and lays out the roadmap for improving
> the Component 3 model.

---

## 1. Who and what

- **Person:** Marcos Sandoval Lucas (two last names: "Sandoval Lucas"), research intern.
- **Group:** Mondragon-Shem Quantum Group, University of Illinois Chicago (UIC), College of Engineering.
- **Project:** "AI **Design of** Quantum Processors."

### The true purpose (read this first — it is often misread)
The goal is **NOT** "use quantum computing to make AI faster." It is the reverse:

> **Use ordinary (classical) machine learning, running on a normal computer, to predict the properties of quantum hardware — so the expensive quantum calculation need not be run every time.**

AI is the *tool*; the quantum processor is the *thing being studied*. The deeper scientific question: **how much about a quantum system can be predicted from classical information alone, and where does that prediction break down?** That breakdown point is where the interesting physics lives.

The **harmonic oscillator** (mass on a spring; physically, an LC circuit) is the test system because it is solvable **exactly** both classically and quantum-mechanically — giving a built-in answer key. Golden rule: *never trust a numerical result that cannot be checked against an exact formula.*

---

## 2. The three components (the pipeline)

```
Component 1            Component 2              Component 3
CLASSICAL  ───────►    QUANTUM       ───────►   MACHINE LEARNING
(the INPUTS)           (the TARGETS)            (learn: inputs → targets)
cheap to compute       expensive to compute     predicts the expensive
                                                 answer from the cheap input
```

- **Component 1 — Classical data generation.** Simulate the oscillator with Newton's / Hamilton's equations. Energy contours, phase-space trajectories, energy conservation. Produces the ML **inputs**. **STATUS: Tasks 1–4 built and verified; re-run cleanly from a fresh kernel on 2026-07-29.** **Task 3 — Nonlinear (cosine) oscillator:** add `−V₀cos(kx)` to the potential; equations of motion, phase-space trajectories at several energies, and an energy-band set of initial conditions. **Task 4 — Two coupled oscillators:** two cosine oscillators with momentum–momentum coupling `λ p₁p₂`; derive EOM, plot the four 2-D projections of the 4-D phase space, and build **Poincaré maps** to look for regular/quasiperiodic/chaotic motion.
- **Component 2 — Quantum data generation.** Build quantum operators in QuTiP, compute the energy spectrum (eigenvalues), solve the Schrödinger equation (`sesolve`), visualize with Wigner functions. Produces the ML **targets** — specifically the expectation-value trajectories ⟨φ̂⟩(t), ⟨n̂⟩(t). The spectrum and the Wigner data are context and evidence, **not** model inputs or targets. **STATUS: Tasks 1–3 built and verified; re-run cleanly on 2026-07-29 in the corrected coordinate.** **Task 3 — Fluxonium dynamics:** build the fluxonium Hamiltonian `Ĥ = 4E_C n̂² + ½E_L φ̂² − E_J cos(φ̂+φ_ext)` (scqubits' convention — see §11) with **scqubits**, get its spectrum/wavefunctions, make localized wave packets, evolve them with QuTiP `sesolve`, and overlay ⟨φ̂⟩(t),⟨n̂⟩(t) against the matched classical trajectory. Mapping: **x↔φ (no shift)**, p↔n, k=1, m=1/(8E_C), ω=√(8E_C E_L). See §11 for the coordinate convention — getting this wrong was the July 28 bug.
- **Component 3 — ML training.** **NEW: Task 1 — Fluxonium classical-to-quantum regression.** Generate `N_s` paired trajectories: classical input `Aᵢ = [x(t₁…t_Nt), p(t₁…t_Nt)]` and quantum target `Bᵢ = [⟨x⟩(t₁…t_Nt), ⟨p⟩(t₁…t_Nt)]` (x≡φ, p≡n) from the same random initial packets. Train a **PyTorch** MLP (2 hidden layers, ReLU) `f_θ: Aᵢ ↦ B̂ᵢ` with MSE loss, Adam, 80/20 train/val split, mini-batches; report validation MSE and sweep widths/learning-rate/batch/epochs. **STATUS: complete as of 2026-08-13.** Trained to **early stopping** on the validation minimum (best epoch 1610, val MSE **1.47e-4**, gap 4.5×) — 6.4× better than the old fixed 150 epochs. Scored against three honest baselines on the same held-out split (RMS in `⟨φ̂⟩`, rad): copy-classical 1.067, k-NN 0.077, linear regression 0.026, **MLP 0.0057**. The meaningful comparison is the 4.5× over linear regression, since inside one well the map is near-linear. Prediction error was then measured against a physical axis on a second, wider dataset spanning the well bottom to the barrier top: the MLP's error climbs **5.2×** (Spearman ρ=+0.40, p=0.0016) and the quantum correction itself climbs **2.4×** (ρ=+0.86, p=8.5e-19) — the classical→quantum breakdown, located. A narrow-window run had found no trend; that null was a sampling artifact (`Assignment 1/Findings_and_Corrections.md` §3).**

---

## 3. Repository layout

Canonical repo: **`C:\Users\galli\quantum-research`** (this is the git repo — commit from here).
**What is deliberately NOT in this repo** (it is shared with the group on GitHub, so everything here
is something the PI can read):

| Excluded | Why |
|---|---|
| `CLAUDE.md`, `.claude/`, `.cursor/`, copilot instructions | AI-tooling files. **Physically absent, not merely gitignored** — the `.gitignore` entries are only a backstop. |
| `reference/WORKING_PREFERENCES.md` | How I like to be worked with — not something the group needs. |
| `reference/Session_Context.md` | Handoff notes between working sessions. |
| `Assignment 1/slides/Meeting_Script.md` | My speaking notes for the meeting. |
| `Assignment 1/slides/Slide_by_Slide.md` | What each slide shows and why it is in the deck. |
| The textbook and lecture-note PDFs | Copyrighted; cite page and equation numbers instead. |

All of these live in the OneDrive folder only. Everything in the repo is mirrored to OneDrive; the
reverse is not true. **The project's own AI/ML content is not "AI tooling"** — Component 3 is the
research deliverable and belongs here.

A **copy** of the Assignment 1 deliverables also lives in OneDrive at
`C:\Users\galli\OneDrive\Documents\Research Internship\Quantum Research Internship\` (NOT the git repo; kept in sync manually).

```
quantum-research/
├── README.md                  repo structure + conventions (root, for GitHub)
├── requirements.txt           pinned deps (pip install -r requirements.txt)
├── .venv/                     virtual environment (not committed)
├── shared/                    reusable code, importable from any assignment
│   ├── oscillator.py          setup() + physics helpers
│   ├── group_plot_style.py    apply_group_style(): group plotting standards
│   └── output_routing.py      route_outputs(): auto-sort saved files
├── reference/
│   ├── PROJECT_CONTEXT.md               this file
│   └── Research_ClassicalToQuantum_ML.md  literature survey + ML roadmap
└── Assignment 1/
    ├── component1_classical.ipynb
    ├── component2_quantum.ipynb
    ├── component3_ml.ipynb
    ├── Classical_and_Quantum_Mechanics_Study_Guide.md   concept guide + ML/AI primer + Q&A
    ├── Code_Walkthrough_Components_1_to_3.md           cell-by-cell code explanation
    ├── Findings_and_Corrections.md   two errors found in review, and how each was caught
    ├── handouts/  the PI's task handouts (quantum_researcher 2.pdf, 4.pdf)
    ├── figures/   generated plots -- everything here is written by a notebook cell
    ├── data/      classical_trajectories.npy, fluxonium_pairs_A.npy, fluxonium_pairs_B.npy
    ├── movies/    Wigner animation GIFs (fock / superposition / coherent)
    └── slides/    Components_1_3_Update.pptx/.pdf (23 slides, all three components), assets/
```

> **Folder casing — resolved 2026-07-29.** Git had the folder committed as `Shared/` (capital S)
> while the working tree read `shared/`. Windows ignores the difference; Git and GitHub do not, so a
> collaborator cloning on Linux or macOS would have got `Shared/` and every path in these docs would
> have been wrong for them. Fixed with a two-step rename — Git will not record a case-only rename in
> one go — and the committed tree now reads `shared/` throughout.
> ```powershell
> git mv Shared shared_tmp
> git mv shared_tmp shared
> ```

---

## 4. Key helper functions (`shared/oscillator.py`)

- `setup()` — applies group plot style + turns on output routing, in one call. Notebooks run this once.
- `energy(x, p)` — classical energy `p²/2m + ½mω²x²`.
- `hamilton_rhs(t, state)` — RHS of Hamilton's equations for `solve_ivp`.
- `analytic_xp(t, x0, p0)` — exact classical `x(t), p(t)` for checking.
- `build_operators(N)` — returns `(a, adag, x, p, H)` for an N-level oscillator.
- `wigner_gif(states, tlist, fname, …)` — animated Wigner GIF, ~40 frames, with a color scale genuinely fixed across frames (an explicit `np.linspace(-wmax, wmax, 81)` level array — `levels=80` plus `vmin`/`vmax` does *not* work, matplotlib ignores `vmin`/`vmax` when `levels` is an integer). Frame delay is in **milliseconds** (imageio ≥ 2.28).
- **Self-check:** `python shared/oscillator.py` verifies the classical solver against the exact solution, energy conservation, the Wigner color scale, and the quantum spectrum against `Eₙ = ℏω(n+½)`. Run it after touching this file.

**Important design choice:** the physics (energy, hamilton_rhs, operator construction) is written **inline** in the notebook cells so the work is visible to the PI, AND also kept in `oscillator.py` for reuse. Same math, two homes. Notebooks import only `setup` (both) and `wigner_gif` (Component 2).

---

## 5. Conventions

- **Natural units:** ħ = m = ω = 1 everywhere.
- **Truncation:** quantum Hilbert space truncated at N = 30 levels; only the lowest ~N/2 eigenvalues are trustworthy (finite-truncation drift at the top is expected).
- **Shared import:** works via a `.pth` file `quantum_research_shared.pth` in `.venv/Lib/site-packages/` pointing at the `shared/` folder — so `from oscillator import setup` works from any assignment folder.
- **Output routing:** `route_outputs()` monkeypatches savefig/np.save/imageio so bare filenames auto-sort into `figures/`, `data/`, `movies/` by extension.
- **New tasks go into the existing component notebooks:** new Component 1 tasks are appended to `Assignment 1/component1_classical.ipynb`, new Component 2 tasks to `Assignment 1/component2_quantum.ipynb` (one notebook per component, not per task). **Component 3 (ML) has its own notebook, `Assignment 1/component3_ml.ipynb`.**
- **Keep the companion docs in sync:** whenever notebook code changes or a task is added, update BOTH `Classical_and_Quantum_Mechanics_Study_Guide.md` and `Code_Walkthrough_Components_1_to_3.md` in `Assignment 1/`.
- **Always organize into folders — never leave loose files at a folder root.** Every kind of output gets its own subfolder (`figures/`, `data/`, `movies/`, `slides/`, `reference/`, etc.). New categories of file get a new folder rather than sitting loose. This includes docs like this one, which lives in `reference/`.
- **Plot labeling (strict):** every axis labeled with units (or "dimensionless"); every curve has a legend entry; every figure has a caption stating the takeaway. Perceptually-uniform colormaps (viridis/plasma) for unsigned data; diverging (RdBu_r) only for signed data like Wigner functions. Fonts sized to stay legible on slides.
- **Meeting slides:** three exact sections — **Context → Results → Open Questions**. Slide titles are complete sentences stating the main takeaway; one idea per slide. Slide figures are the notebook PNGs from `figures/`, embedded **unmodified** — commentary goes in the slide text, not baked into the image. This is stricter provenance than re-plotting with a separate script, and avoids keeping a second copy of the plotting code that can drift.

---

## 6. Sources the work aligns to

- **Essler, *Lecture Notes for Quantum Mechanics* (Oxford)** — the group's assigned text. Ladder operators (eq. 230), spectrum (eq. 246), coherent states ("Aside 4"), length scale ℓ = √(ħ/2mω). NOTE: the **Wigner function is NOT in Essler** — it comes from the project handout (Essler uses |ψₙ(x)|² instead, his §6.4).
- **Griffiths & Schroeter, *Introduction to Quantum Mechanics*, 3rd ed. (Cambridge)** — recommended by the PI (Teams, 2026-07-24) as the book to actually learn from; Essler stays the group's reference for conventions. PDF in the OneDrive `Books/` folder. Study guide **Part 8** has an ordered reading path plus a concept → Essler → Griffiths cross-reference. The two sections that matter most for this project: **§2.3.1** (ladder operators, = Component 2 Task 1) and **Problem 3.42** (coherent states, = Task 2 and all of Component 3).
- **PennyLane superconducting-qubits tutorial** (pennylane.ai/demos/tutorial_sc_qubits) — hardware context: LC circuit = oscillator; Josephson junction adds anharmonicity → transmon qubit.
- Files in the OneDrive folder: `Quantum Mechanics Lecture Notes.pdf` (Essler), `Research Opportunity Handout.pdf`.
- **`reference/Research_ClassicalToQuantum_ML.md`** — literature survey + concrete techniques for improving the classical→quantum ML model (classical shadows, provably-efficient ML, neural operators, physics-informed learning, staged roadmap).

---

## 7. Environment & how to run

- **Python 3.14**, venv at `.venv/`. Key libs: numpy 2.4, scipy 1.17, matplotlib 3.10, **qutip 5.3.0**, jupyterlab 4.5, imageio 2.37, **scqubits 4.3.1** (superconducting-qubit library, for fluxonium), and **torch 2.13.0+cpu** (PyTorch, the ML framework — CPU build, which is all the small MLP needs). Both installed 2026-07-23. After any new install, regenerate `requirements.txt` with `pip freeze > requirements.txt` (repo root) and copy it to the OneDrive mirror.
- **Launch JupyterLab (PowerShell) — one line:**
  ```powershell
  cd ~\quantum-research; .venv\Scripts\activate; jupyter lab
  ```
- **Always run notebooks via Kernel → Restart Kernel and Run All Cells** (top to bottom). Running cells out of order causes "name 'X' is not defined" errors.

---

## 8. Known gotchas (things that have bitten us)

- **Stale Jupyter tabs clobber disk edits.** If a notebook was edited on disk while an old tab is open, the tab can overwrite it on save. Fix: close the tab WITHOUT saving → reopen → Restart & Run All.
- **OneDrive-synced Markdown + large Write/Edit → null bytes / truncation.** When editing big files in the OneDrive copy, prefer appending via shell heredoc and verify with `wc -l` and a null-byte check. The canonical repo copy (non-OneDrive) is safer to edit.
- **matplotlib mathtext** does not support `\tfrac` / `\frac12`; use `\frac{1}{2}`.
- **Spectrum assertion** fails for high N — only check the lowest ~N/2 levels.
- **`group_plot_style` "No module found"** — resolved by the `shared/` + `.pth` setup; the module must be reachable on the path.

---

---

## 9. Repository status

- `.gitignore` covers `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `desktop.ini`.
- All three notebooks were re-run from a fresh kernel on 2026-07-29: every code cell carries an
  execution count, none error, and every figure, data file and movie they declare is on disk.
- `figures/` contains only notebook output. Hand-made teaching figures live in
  `Assignment 1/slides/assets/` alongside the annotated talk figures.

## 10. Verification

Run `python shared/oscillator.py` at any time. It checks, against exact formulas:

| Check | Result |
|---|---|
| `solve_ivp` vs the analytic classical solution | agrees to 6.7e-9 |
| Energy conservation over four periods | drift 1.9e-9 |
| Wigner colour scale symmetric about zero | invariant holds |
| Quantum spectrum vs `Eₙ = ℏω(n+½)` | max error 5.3e-15 over the lowest 15 of N = 30 |

The golden rule for this project: *never trust a numerical result that cannot be checked against an
exact formula.* `Assignment 1/Findings_and_Corrections.md` is what happened the two times a result had no such check.
