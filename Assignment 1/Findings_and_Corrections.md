# Findings — two errors, how they were caught, and what they changed

*Marcos Sandoval Lucas · AI Design of Quantum Processors, Mondragon-Shem Quantum Group (UIC)*
*Written 2026-07-29. Companion to `component1_classical.ipynb`, `component2_quantum.ipynb` and
`component3_ml.ipynb` in this folder; see also `Code_Walkthrough_Components_1_to_3.md` for the
cell-by-cell explanation and `../reference/PROJECT_CONTEXT.md` for the project overview.*

Both of these were mine, both survived a first pass because the code ran without complaint, and
both were caught the same way: by checking a result against something external rather than against
what I expected to see. I am keeping the record because the *how* is more transferable than the
fix.

---

## 1. The fluxonium coordinate convention

**The bug.** `scqubits` defines the fluxonium potential as

```python
# scqubits/core/fluxonium.py
return 0.5 * self.EL * phi * phi - self.EJ * np.cos(phi + 2.0 * np.pi * self.flux)
```

i.e. `U(φ) = ½E_L φ² − E_J cos(φ + φ_ext)`, with the **inductive term centred on φ = 0**. At half
flux this puts the two wells at **φ = ±2.852** and makes **φ = 0 the barrier top** (7.76 E_C above
the well bottoms).

Components 2 and 3 instead wrote `U(φ) = ½E_L(φ − φ_ext)² − E_J cos φ`. That is the *same physics
in a coordinate shifted by φ_ext* — wells at 0.289 and 5.994. Both forms are individually correct;
the mistake was using one for the classical trajectory and the plotted curve while `scqubits` used
the other for the Hamiltonian, operators and eigenstates.

**What it broke.**

1. `fig_c2_fluxonium_spectrum.png` drew the potential π away from the wavefunctions plotted over it — the |1⟩ lobe at φ ≈ 2.85 sat on the barrier top of the drawn curve.
2. The classical trajectory in `fig_c2_fluxonium_dynamics.png` and `fig_c2_fluxonium_sweep.png` was not the classical limit of the Hamiltonian being solved.
3. Component 3 paired every quantum trajectory with a classical trajectory from a different part of the potential.
4. The sampling window `φ₀ ∈ (−1.5, 1.5)`, chosen believing it straddled the well minimum at 0.289, actually sits **centred on the barrier top** and never enters a well. Every training packet was launched where it splits and tunnels.

**The fix.** Take the potential from `fluxonium.potential(...)` — one source of truth — and integrate
the classical equations in the same φ:

```python
dφ/dt = 8 E_C n
dn/dt = -(E_L*φ + E_J*np.sin(φ + φ_ext))
```

No `− φ_ext` shift is applied to either side's output: scqubits' φ *is* the coordinate. Component 3
now samples `φ₀ = φ_min ± 1.0` (inside a well, φ_min ≈ 2.852) and Component 2 Task 3 starts its
headline packet at `φ_min` and sweeps well → barrier → well.

**How it was caught.** Reproducing the spectrum cell against `scqubits.Fluxonium.potential` and
checking where `fluxonium.wavefunction(...)` actually puts its probability (φ ≈ ±2.93, matching
scqubits' wells, not the drawn ones). Confirmed against the scqubits documentation, which gives
`H = -4E_C ∂_φ² - E_J cos(φ - φ_ext) + ½E_L φ²`.

**Outcome (2026-07-29 re-run).** Component 3's validation MSE went from 8.4e-3 to **9.3e-4**, a
9× improvement, with the train/val gap dropping from 13.7× to 1.7×. Physically consistent pairs are
what made the map learnable. The spectrum figure now shows the potential aligned with its states.

**Equilibrium-point fix (same day).** The Task 3 packet had been started at exactly `phi_min` with
`n0 = 0`, which is an **equilibrium point** — the classical particle never moves, so the dynamics figure
compared a moving quantum average against a flat line and the `φ₀ = 0` sweep panel was the barrier's
unstable fixed point on a 1e-8 axis. Both cells now apply `n0_kick = 0.5`. Re-run and the physics reads
properly: quantum and classical agree until t ≈ 0.7 then separate, and the barrier panel shows the
classical point sweeping a figure-eight through both wells while the packet splits and stays put.

**Markdown sweep (2026-07-29).** The notebook prose had drifted badly behind the code. Fixed: both
"What you will do here" lists stopped at Task 2 (C1 was missing Tasks 3–4, C2 was missing Task 3);
the "Component 1/2 — takeaways" sections sat mid-notebook still saying "next: Component 2", stranding
the later tasks; C2 Task 3 and C3 both still printed the pre-fix Hamiltonian and the `x ↔ φ − φ_ext`
mapping; the Task 3 captions still quoted `φ₀ = π/2` and `φ₀ ∈ {−π…π}`, and one of them called
`φ₀ = π` "the barrier top" when the barrier is at `φ = 0`. All corrected, plus the "quantum twin"
caveat (the cosine flips sign at half flux, so C1 Task 3's single well is not this double well).

---

## 2. The chaos that was not there

**What I had said.** "At E = 12 the phase space is mixed: a few surviving islands embedded in a
chaotic sea." **Not supported.**

**How it was checked.** Maximal Lyapunov exponent, the standard quantitative test (Goldstein
§11.2–11.6): positive means chaos, zero means regular. At the notebook's parameters
(`lam = 0.3`, `V0 = 1`): `λ_max ≈ 0.004` at E = 1, `0.007` at E = 12, `0.005` at E = 30 — all at or
below the `log t / t` convergence floor, which is what zero looks like numerically. The Poincaré
sections agree: nested tori at both energies.

**Why the intuition was backwards.** The nonlinear term is a cosine, so it is **bounded**
(`|V0 cos(kx)| ≤ V0`) however large the energy. The harmonic term grows without limit. Raising the
energy therefore makes this system *more* nearly harmonic — closer to integrable, not further. KAM
tori survive because the perturbation stays small in the sense the theorem requires.

**Where the chaos actually is.** Coupling strength and well depth, not energy:
`lam = 0.8, V0 = 8, E = 12` gives `λ_max = 0.11`; `lam = 0.8, V0 = 15, E = 25` gives `0.34`. Both
firmly chaotic. Worth asking the PI whether Task 4 should be re-run in that regime.

**Separate bug in the same cell.** The Poincaré event used `direction = 0` and filtered on
`p2 > 0`. But the crossing direction is `dx2/dt = p2/m + lam*p1`, which does not share the sign of
`p2` when the coupling is in the momenta — about **5% of recorded crossings ran the wrong way**,
overlaying two different sections. Now `direction = 1`, with the launch condition matched.

**What the textbooks suggested afterwards.** Goldstein Ch. 6 (small oscillations, principal-axis
transformation) and a footnote in Griffiths' coupled-oscillator problem both say to start by
decoupling into normal modes. Doing that for this Hamiltonian — a 45° canonical rotation
`X± = (x₁±x₂)/√2`, `P± = (p₁±p₂)/√2` — is **exact** (verified to 1e-16) and shows the momentum
coupling is not really a coupling at all: it only gives the two modes different effective masses,
`1/m± = 1/m ± λ`, with frequencies `ω± = ω√(1±λm)`. The one term that genuinely couples the modes,
and the only thing making the system non-integrable, is the cosine cross-term
`−2V₀cos(kX₊/√2)cos(kX₋/√2)`. Without the cosine this problem separates and is exactly solvable.
That is a far better framing for Task 4 than "two oscillators with momentum coupling," and it makes
Goldstein's KAM condition (incommensurate frequencies) directly checkable — at λ = 0.3 the ratio is
1.363, consistent with the surviving tori.

**A hypothesis I tested and rejected.** Those ratios hit exact low-order resonances at λ = 0.6 (2:1)
and λ = 0.8 (3:1), so I guessed resonance explained the chaos onset. It does not: λ = 0.5, off
resonance, is equally chaotic at V₀ = 8. At that well depth the cosine is not a small perturbation,
so KAM does not apply and the frequency condition is irrelevant. Recording the failed hypothesis
because the reasoning is still worth revisiting in the near-integrable regime.

**The lesson worth keeping.** A Poincaré plot that looks scattered is not evidence of chaos, and one
that looks regular is not proof of its absence. The Lyapunov exponent is the check; the plot is the
picture.

**Resolved.** Component 1 was re-run on 2026-07-29; the Poincaré figure is clean and slide 9 carries it.

**Housekeeping.** `phase_space_explainer.png` was a hand-drawn teaching figure sitting in `figures/`
among notebook output, produced by no cell and referenced by nothing. Moved to
`Assignment 1/slides/assets/`, which is where annotated talk figures already live. `figures/` now
means exactly one thing: regenerated by the notebooks.

---

## What both have in common

1. **The code ran fine.** Neither error raised anything. A silent wrong answer is the expensive kind.
2. **The plot looked plausible.** In both cases the figure was the thing that misled me — a potential curve drawn over states that did not belong to it, and a scatter of dots I read as chaos.
3. **The check that caught it was external.** Not "does this look right" but "does this match `scqubits`' own definition" and "what does the Lyapunov exponent actually say."
4. **Both had a real consequence.** The first cost a factor of nine in model accuracy. The second would have put a false claim in front of my PI.

The working rule I have taken from this: *a figure is a picture, not a measurement.* If a claim can be
reduced to a number, reduce it to a number before writing it down.
