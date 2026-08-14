# Handout compliance — every requirement, and where it is met

*Checked against `handouts/quantum_researcher 4.pdf` (8 pages) on 2026-08-13.*
*Companion to `Code_Walkthrough_Components_1_to_3.md` (what each cell does) and
`Findings_and_Corrections.md` (the errors found along the way).*

This file exists so that "does the work meet the brief?" has a written answer rather than a verbal
one. Every lettered sub-task in the handout appears below with where it is satisfied. Four items were
**not** met when this audit was run and have since been added; they are marked **[added 2026-08-13]**.
Five places where the work **deliberately differs** from the handout are listed at the end with the
reasoning, because those are the ones worth raising in the meeting rather than hoping go unnoticed.

> **A presentation check worth repeating before any submission.** Requirements are graded per
> lettered sub-task, so each one needs a **visible markdown header** — not just correct code. On
> 2026-08-14 three labels were found wrong by reading the rendered notebook rather than the code:
> `(b)` in both Component 1 Task 3 and Task 4 existed only as a `# (b)` comment inside a code cell,
> and a duplicate `(e)` had been introduced in Component 2 Task 3. In every case the *work* was
> present and correct; only the label was missing, which is exactly the kind of thing that costs
> marks for no reason. Scan the headers, not the code.

---

## Research Component 1 — Classical data generation

### Task 1 — Energy and phase space

| | Requirement | Where |
|---|---|---|
| (a) | State classical energy `E(x,p)` in terms of x, p, m, ω | markdown before the `energy()` cell; `energy(x, p)` |
| (b) | Derive EOM from Hamilton's equations; combine to the 2nd-order equation | Task 1(b) markdown — full derivation, ending at `ẍ = −ω²x` |
| (c) | Contour or density plot of `E(x,p)`; explain the constant-energy curves | `fig_c1_energy_contours.png` + caption |

### Task 2 — Dynamics and trajectories

| | Requirement | Where |
|---|---|---|
| (a) | Solve the EOM, one initial condition, phase-space plot, mark the initial point | `fig_c1_single_trajectory.png`; start marked with a crimson dot |
| (b) | Repeat for random initial conditions, all on one axis, explain dependence on energy | `fig_c1_many_trajectories.png`, coloured by conserved energy |

*Extra beyond the brief:* the numerical trajectory is checked against the exact analytic solution
(max deviation 6.7e-9) and energy conservation is asserted (drift 1.9e-9).

### Task 3 — Cosine potential

| | Requirement | Where |
|---|---|---|
| (a) | EOM from Hamilton's; identify the new term; explain how it changes the restoring force | Task 3(a) markdown; the new term is `−V₀k sin(kx)` |
| (b) | Several initial energies, phase-space trajectories on the same axes | `fig_c1_cosine_trajectories.png` — **header added 2026-08-14**: the work was there but `(b)` existed only as a code comment, so the rendered notebook read (a) → figure → (c) |
| (c) | Band `[E_ref−ΔE, E_ref+ΔE]`, colour/transparency encoding initial energy | `fig_c1_cosine_energy_band.png`, viridis + colorbar |

### Task 4 — Two coupled oscillators

| | Requirement | Where |
|---|---|---|
| (a) | Derive EOM for `(x₁,p₁)` and `(x₂,p₂)` | Task 4(a) markdown; `rhs_coupled` |
| (b) | Four 2-D projections at fixed `E₀` | `fig_c1_coupled_projections.png` — **header added 2026-08-14**, same issue as Task 3(b) |
| (b) | **"Repeat for several values of E₀ and describe how the structure changes"** | **[added 2026-08-13]** `fig_c1_coupled_projections_energies.png` — the same four projections at `E₀ = 1, 3, 12`, with the trend described and energy conservation asserted at each |
| (c) | Energy band, `(x₁,p₁)` on one figure and `(x₂,p₂)` on another, colour = energy | `fig_c1_coupled_energy_band.png` (two panels, shared colorbar) |
| (d) | Poincaré maps, at least two energies, discuss regular / quasiperiodic / chaotic | `fig_c1_coupled_poincare.png` at `E = 1` and `E = 12`; discussion + Lyapunov measurement |

---

## Research Component 2 — Quantum data generation

### Task 1 — Operators and energy spectrum

| | Requirement | Where |
|---|---|---|
| (a) | Build `x̂`, `p̂`, `Ĥ` in QuTiP; `imshow` the absolute matrix elements | `fig_c2_operator_matrices.png` |
| (b) | Eigenvalues of `Ĥ`, plot vs `n`, compare to `Eₙ = ℏω(n+½)` | `fig_c2_energy_spectrum.png`; max error 5.3e-15 over the lowest 15 of N = 30 |
| (c) | Explain what changed and what stayed the same, classical → quantum | Task 1(c) markdown |

### Task 2 — State dynamics and phase space

| | Requirement | Where |
|---|---|---|
| (a) | `sesolve` for `|n⟩`, `(|0⟩+|1⟩)/√2`, and a coherent state; store states | Task 2(a) cell, `options={"store_states": True}` |
| (b) | Wigner function at `t = 0` for each | `fig_c2_wigner_t0.png` |
| (c) | Movie for each, **fixed colour scale** | `movies/wigner_{fock,superposition,coherent}.gif` via `wigner_gif()` |
| (d) | `⟨x̂⟩(t)`, `⟨p̂⟩(t)`; plot `⟨p̂⟩` vs `⟨x̂⟩`; overlay classical from the same start; discuss | `fig_c2_expectation_vs_classical.png` + discussion cell |
| (e) | One-page reflection on what each representation tells you | Task 2(e) markdown |

*Note on (c):* the fixed colour scale is genuine and was a bug once — passing `levels=80` with
`vmin`/`vmax` silently rescales every frame, because matplotlib ignores `vmin`/`vmax` when `levels`
is an integer. The helper now passes an explicit level array.

### Task 3 — Fluxonium

| | Requirement | Where |
|---|---|---|
| (a) | State `Ĥ`; explain similarity to the classical Task 3; identify kinetic / harmonic / nonlinear terms | Task 3(a) markdown, term by term |
| (b) | First **four** eigenstates via scqubits; plot energies and wavefunctions | `fig_c2_fluxonium_spectrum.png`, `evals_count=4` |
| (c) | Normalized packet at `φ₀`; grid plot of the packet at `t = 0` | top row of `fig_c2_fluxonium_sweep.png` |
| (d) | `sesolve`; compute `⟨φ̂⟩(t)`, `⟨n̂⟩(t)` and `⟨Ĥ⟩(t)` | `e_ops=[phi_op, n_op, H_flux]`; `⟨Ĥ⟩` conserved to 2.1e-7 |
| (e) | **Compute the classical energy `E₀ = H(x₀,p₀)`**; overlay classical vs quantum; discuss | **[added 2026-08-13]** `E_classical()` prints `E₀` for every launch against the barrier height, so "trapped" vs "can cross" is stated numerically rather than inferred |
| (f) | Repeat (c)–(e) for several `φ₀`; grid plots of packet, expectation trajectories, classical overlays | `fig_c2_fluxonium_sweep.png` (2 × 5 grid) |

*Truncation:* the handout suggests 40–60 states. This uses **110** in Component 2 and **80** in
Component 3 (one `sesolve` per sample there, so speed matters). Both are above the suggestion, and
the 80 is verified against 110 across the full sampling window — they agree to 8.2e-7 rad.

---

## Research Component 3 — ML training

### Task 1 — Classical-to-quantum regression

| | Requirement | Where |
|---|---|---|
| (a) | Shared parameter module so both simulations use consistent values; random `(φ₀,n₀)` per sample | section (a) cell: classical `m`, `ω`, `V₀` are *derived from* the quantum `E_C`, `E_L`, `E_J` |
| (b) | `N_s` quantum trajectories; `Bᵢ ∈ R^{2N_t}`; `t_final` covering ≥ one full cycle | `quantum_sample()`; `N_s = 300`, `t_final = 1.5 T_class` |
| (c) | Classical dataset, same random initial conditions, same time grid | `classical_sample()`; shared `tlist`; asserted `A[:,0] == φ₀` |
| (d) | MLP, 2 hidden layers, ReLU, MSE, Adam, 80/20 split, mini-batches | `class MLP`, `nn.MSELoss`, `torch.optim.Adam`, `DataLoader(batch_size=32)` |
| (d) | Monitor training **and** validation loss each epoch | `train_hist`, `val_hist`; `fig_c3_loss_curve.png` |
| (d) | **"Explore hidden widths d₁,d₂ together with learning rate, mini-batch size, and epochs"** | **[added 2026-08-13]** widths {64,128,256} × lr {3e-4,1e-3,3e-3} grid, then batch {16,32,64} at the best cell. Epoch count is chosen by early stopping rather than swept by hand |
| (d) | Report validation MSE; optionally relative or component-wise errors | best validation MSE reported; component-wise RMS in `⟨φ̂⟩` and `⟨n̂⟩` reported separately for all four models |

*Beyond the brief:* three baselines (copy-classical, k-NN, linear regression) scored on the same
split, and prediction error measured against a physical axis on two datasets — which is what turns
the loss number into a result.

---

## Best practices

| Requirement | Status |
|---|---|
| Readable code, descriptive names, short functions, comment every non-obvious step | Followed; every notebook cell is also explained line by line in the code walkthrough |
| All code in Jupyter notebooks | Yes — three notebooks; `shared/` holds only reusable helpers |
| Shared GitHub repo, PI as collaborator, pushed regularly | Repo is `quantum-research`; **pushing is the one item this audit cannot verify** |
| Every axis labelled with units (or "dimensionless") | Yes |
| Every curve in the legend | Yes |
| Every figure has a caption stating the takeaway | Yes — a markdown caption cell follows every figure |
| Perceptually uniform colormaps | viridis / plasma throughout. **One deliberate exception:** the Wigner plots use the diverging `RdBu_r`, because that data is *signed* and the sign is the whole point; a sequential map would hide it |
| Font sizes legible when scaled to a slide | Set once in `shared/group_plot_style.py` |
| **Annotate key features directly on the figures** | **[added 2026-08-13]** — see the deviation note below |
| Slides: one idea per slide, full-sentence takeaway titles | Yes, all 29 |
| Slides: Context → Results → Open questions | Slides 2, 3–27, 28–29 |
| Slides: every sub-task with a figure appears in the deck | Yes — 21 of 21 figures used |

---

## Points in the handout worth checking with the PI

*These came out of verifying the handout's equations rather than assuming them. In every case the
notebooks already do the right thing — but the reasons are worth being able to state, because two of
them explain deviations that would otherwise look like mistakes on my side. Each was checked
numerically; the script is in the session notes.*

### 1. `V₀ ↔ E_J` does not hold at the recommended half-flux point

The handout (p. 6) gives the correspondence `x ↔ φ − φ_ext`, `V₀ ↔ E_J`, `k = 1` between

`Ĥ = 4E_C n̂² + ½E_L(φ̂ − φ_ext)² − E_J cos φ̂`  and  `H = p²/2m + ½mω²x² − V₀cos(kx)`.

Substituting `φ = x + φ_ext` gives `U(x) = ½E_L x² − E_J cos(x + φ_ext)`. That matches
`−V₀cos(kx)` with `V₀ = +E_J` **only when `φ_ext = 0`** — which I verified is exact to machine
precision. At the handout's own recommended `φ_ext = π`, `cos(x+π) = −cos(x)`, so the potential is
`½E_L x² + E_J cos x`, i.e. **`V₀ = −E_J`**. Measured discrepancy between the two forms: **10.0 E_C**
(= 2E_J), so this is a sign error rather than a rounding detail.

**Why it matters:** with the sign flipped the system is a **double well**, not the single-well cosine
oscillator of Component 1 Task 3. The handout describes them as "structurally similar", which is true
of the *form* but not of the physics at half flux — the double well is what produces the tunneling
doublet, which has no counterpart in the Task 3 oscillator. The notebooks already say this (the
"quantum twin caveat"); this is the quantitative version.

### 2. The handout's two coordinate conventions contradict each other

- p. 7 (e) and p. 8 (a): *"the classical simulation uses `(x₀,p₀) = (φ₀ − φ_ext, n₀)`"*
- p. 8 (b): *"`Bᵢ = (⟨x⟩(t₁), …)`, where **`x ≡ φ`**"*

So the **classical** trajectory is launched in a coordinate shifted by `φ_ext`, while the **quantum**
target is recorded unshifted. Following both literally pairs each classical trajectory with a quantum
one half a flux quantum away. I measured the effect: the apparent classical–quantum gap inflates from
**1.19 rad to 3.20 rad — a factor of 2.7** — purely from the mismatch.

**This is the origin of `Findings_and_Corrections.md` #1.** The bug was not a misreading of the
handout; it was following it. The fix is to pick one coordinate and use it on both sides — this
project uses `scqubits`' (unshifted `φ`), because that is the potential the eigenstates are actually
solved in. Worth confirming with the PI which convention he wants reported, since the well positions
differ (±2.85 in scqubits' vs 0.29/5.99 in the handout's).

### 3. `E_L = Φ₀²/L` is missing a factor of `(2π)²`

The standard definition is `E_L = (Φ₀/2π)²/L = φ₀²/L`, with `φ₀ = ℏ/2e` the *reduced* flux quantum.
As written the handout is short by `(2π)² ≈ 39.5`, unless `Φ₀` is meant as the reduced quantum — the
handout does use "reduced" for `φ_ext` on the same line, so it is probably shorthand.
**No effect on any result here**, since everything is computed in ratios to `E_C`.

### 4. "∼40–60 charge states" describes the wrong basis

`scqubits.Fluxonium` is diagonalized in a **harmonic-oscillator** basis; its `cutoff` argument counts
those states, not charge states. (Charge states are the natural basis for a transmon / Cooper-pair
box.) The intent — keep enough basis states — is met and exceeded: 110 in Component 2 and 80 in
Component 3, with the 80 verified against 110 to 8.2e-7 rad.

### 5. The suggested Poincaré condition is not the right test here

p. 4 suggests recording crossings "where `x₂ = 0` with `p₂ > 0`". With momentum coupling the crossing
direction is `dx₂/dt = p₂/m + λp₁`, which does not share the sign of `p₂`. Filtering on `p₂ > 0`
admitted 3.2% of crossings in the wrong direction (158 of 4,971 when reproduced). The notebook filters on `dx₂/dt` instead. (For a
system with the coupling in the *positions* the handout's condition would be correct.)

---

## Deliberate deviations — raise these rather than hope they pass

**1. The fluxonium coordinate convention.** The handout writes
`Ĥ = 4E_C n̂² + ½E_L(φ̂ − φ_ext)² − E_J cos φ̂` with `x ↔ φ − φ_ext`. `scqubits` writes
`½E_L φ̂² − E_J cos(φ̂ + φ_ext)` with **no shift**. These are the same physics in coordinates that
differ by `φ_ext`, but they are *not interchangeable*: in the handout's coordinate the wells sit at
`0.29` and `5.99`, in scqubits' at `±2.85`. This notebook follows scqubits throughout, because that
is the potential the eigenstates are actually solved in. Mixing the two is a real bug that happened
here and cost a factor of nine in model accuracy — `Findings_and_Corrections.md` #1.

**2. The Poincaré section condition.** The handout suggests recording crossings with `p₂ > 0`. With
momentum coupling the crossing direction is `dx₂/dt = p₂/m + λp₁`, which does **not** share the sign
of `p₂`. Filtering on `p₂ > 0` admitted 3.2% of crossings in the wrong direction (158 of 4,971 when reproduced) and smeared two
different sections together. The notebook filters on the sign of `dx₂/dt` instead.

**3. The `φ₀` sweep values.** The handout suggests `φ₀ ∈ {−π, −π/2, 0, π/2, π}`. Those are values in
the handout's coordinate; in scqubits' coordinate the equivalent well-to-well sweep is
`{−2.85, −1.43, 0, 1.43, 2.85}`, which places the endpoints exactly at the two minima and the middle
panel exactly on the barrier top. Same intent, expressed in the coordinate actually being used.

**4. Truncation of 80–110 rather than 40–60.** Above the suggested range, and justified: the
Component 3 value of 80 is verified against 110 across the whole sampling window (agreement 8.2e-7).

**5. Annotations on figures vs commentary in slide text.** The handout asks for key features to be
annotated directly on the figures. The deck previously put that commentary in the slide text instead,
because an earlier `make_slide_figures.py` re-plotted every figure with annotations, drifted out of
sync with the notebooks, and had to be patched separately when a plotting bug was fixed. The
resolution: annotations are now drawn **inside the notebook cells**, so the notebook's own PNG
carries them and the deck still embeds that PNG unmodified. One source of truth, and the handout's
requirement met. Annotated: the Poincaré map, the energy spectrum, the fluxonium spectrum, the loss
curve, and the breakdown figure.

**6. Two sub-tasks are in the notebooks but not on a slide of their own.** The handout asks for the
deck to hold "your latest calculations… your most recent results as polished plots", one idea per
slide — a selection, not a mirror of every sub-task. Every sub-task that *produces a figure* is now
on a slide (21 of 21 figures used, checked mechanically). The two that are not are written
reflections with no figure: **C2 Task 1(c)** (what changed going classical → quantum) and **C2 Task
2(e)** (what each representation tells you). Both are markdown in `component2_quantum.ipynb`.
**C2 Task 2(c)**, the three Wigner movies, is named on slide 17 with the file paths — a GIF cannot
play in an exported deck, so the slide points at `movies/` instead.

> **This is worth a sentence in the meeting.** Not because it is a gap — it isn't — but because
> "everything with a figure is in the deck; the two reflection-only sub-tasks are in the notebook"
> is a better answer than being asked and having to work it out live.
