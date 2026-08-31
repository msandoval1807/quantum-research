# Findings — four corrections, how each was caught, and what it changed

*Marcos Sandoval Lucas · AI Design of Quantum Processors, Mondragon-Shem Quantum Group (UIC)*
*Written 2026-07-29. Companion to `component1_classical.ipynb`, `component2_quantum.ipynb` and
`component3_ml.ipynb` in this folder; see also `Code_Walkthrough_Components_1_to_3.md` for the
cell-by-cell explanation and `../reference/PROJECT_CONTEXT.md` for the project overview.*

All of these were mine, all survived a first pass because the code ran without complaint, and all
were caught the same way: by checking a result against something external rather than against what I
expected to see. I am keeping the record because the *how* is more transferable than the fix.

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
§11.4, p. 491 — he spells it "Liapunov"): positive means chaos, zero means regular. At the notebook's parameters
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
`p2` when the coupling is in the momenta — **3.2% of recorded crossings ran the wrong way** (158 of 4,971, measured across both energies and every launched trajectory),
overlaying two different sections. Now `direction = 1`, with the launch condition matched.

**What the textbooks suggested afterwards.** Goldstein Ch. 6 (small oscillations, principal-axis
transformation) and a footnote in Griffiths' coupled-oscillator problem both say to start by
decoupling into normal modes. Doing that for this Hamiltonian — a 45° canonical rotation
`X± = (x₁±x₂)/√2`, `P± = (p₁±p₂)/√2` — is **exact** (verified to 5.3e-15 over 300 random points) and shows the momentum
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

## 3. The null result that was a sampling artifact

**What I reported (2026-08-13, correctly).** Prediction error against distance from the well minimum
showed **no** significant trend — Spearman ρ = +0.08, p = 0.56 for the MLP. The first draft of that
figure had been titled *"prediction error grows with distance from the well bottom"*, which is what
the physics predicts and what the eye reads off a noisy log plot. Measuring it said otherwise, so the
title was changed to say the error was flat. That much was right, and it is the §2 lesson applied
correctly the second time.

**But "no trend" was not the whole story, and the write-up nearly stopped there.** Two things were
wrong with the *experiment*, not the analysis:

1. **The window never reached the interesting region.** Sampling ran to `|φ₀ − φ_min| = 1.0` rad while
   the barrier sits 2.85 rad away — 35 % of the distance. The breakdown was never in the data, so a
   null was the only possible outcome. A null result from a measurement that *could not have detected
   the effect* is not evidence of absence.
2. **The axis conflated two different regimes.** `|φ₀ − φ_min|` is a distance with the sign thrown
   away. A point 0.8 rad from the minimum could be heading toward the **barrier** (`φ₀ = 2.05`) or
   climbing the harmonic **outer wall** (`φ₀ = 3.65`). Those are different physics — tunneling barrier
   versus parabola — averaged into one bin. Even with a wider window this axis would have blurred the
   signal.

**The fix.** A second, separate dataset sampling one-sided from the barrier top to the well bottom,
`φ₀ ∈ [0, φ_min]`, with the monotone axis `φ_min − φ₀`.

**Outcome.** The trend is there and it is significant: the MLP's error climbs **5.2×** from well
bottom to barrier (ρ = +0.40, p = 0.0016), and copy-classical — the size of the quantum correction
itself — climbs **2.4×** (ρ = +0.86, p = 8.5e-19). Exactly what Ehrenfest's condition predicts.

**How it was caught.** By writing down *why* the null was expected to be wrong and checking the number
against the geometry: the barrier is at 2.85 rad, the data stopped at 1.00. That is a one-line
comparison the notebook now prints on every run, so the limitation cannot be forgotten again.

**The lesson, which is the mirror image of §2.** §2 was believing a trend that measurement did not
support. This was nearly believing a *non*-trend that the measurement was not capable of finding.
Both come from the same root: not asking what the measurement was actually able to detect. **Before
reporting a null, state the effect size the design could have resolved.**

---

## 4. Two numbers in the prose that a re-run did not reproduce

*Found 2026-08-14 by cross-checking every headline number in the write-ups against what the notebooks
actually print, rather than trusting the prose.*

**Energy drift: quoted 1.3e-8, measured 1.9e-9.** The classical energy-conservation figure had been
carried in the text across many revisions and never re-checked against a run. It was wrong by about
7×, and appeared in **20 files** — the study guide, the walkthrough, the compliance table, the deck's
verification slide, my speaking notes, and the project-context file. I first confirmed there is only
*one* drift measurement in Component 1, so this was not two numbers being confused, then corrected all
29 occurrences.

**Poincaré mis-filtering: quoted "~5%", measured 3.2%.** The claim that filtering on `p₂ > 0` admits
about 5% of crossings in the wrong direction could not be reproduced at that value. Re-running the
comparison the way the notebook actually launches it — both energies, every initial condition, 4,971
crossings — gives **158 wrong-direction crossings, 3.2%**. The conclusion is unchanged (the filter is
still wrong, and that is still the reason the sections smeared); only the size was overstated. Now
quoted with the conditions attached, so it can be reproduced.

**Why this is its own finding.** Neither number changed any conclusion, and that is exactly what makes
them easy to leave alone. But a number in a write-up is a claim, and an unreproducible claim is the
one a PI will happen to ask about. The rule that catches this is mechanical: **every number in the
prose must be traceable to a line of executed output**, and the way to enforce it is to grep the
outputs for each quoted value rather than reading and nodding. That check now exists and takes
seconds to re-run; it found 24 of 25 quoted numbers correct and one wrong, which is about the hit
rate to expect.

---

## Four gotchas from the same session

**`bbox_inches="tight"` will happily save a 200,000-pixel image.** The wide-window figure came out
1262 × **202,783** px (1.6 MB) because a text label was positioned using `ax.get_ylim()` *before*
`ax.set_yscale("log")` was called. After the scale change that data coordinate was nonsense, and
`bbox_inches="tight"` dutifully grew the canvas to include it. Nothing errored; the figure simply
could not be opened (PIL refuses it as a decompression bomb). **Set the scale first, and place
annotations in axes-fraction coordinates (`transform=ax.transAxes`), which are immune to scale
changes.** Worth a glance at the pixel dimensions of any new figure — every other figure in
`figures/` is under 2.4 Mpx.

**A refactor that re-splits is not a reproduction.** Section (g) wraps the (d)–(f) protocol in a
function so narrow and wide datasets are scored identically. The markdown first claimed the narrow
numbers would "come back out unchanged" as a check that the refactor was faithful. They did not —
the function re-splits with its own seed, so it is a *fresh run*. The numbers moved: copy-classical
0.5 %, but the **MLP 12 %** (0.0057 → 0.0050). Rewritten to say so, and the 12 % is now quoted as the
split-to-split scatter — which is genuinely useful, because it sets the threshold a difference must
clear before it means anything.

**Two artifacts, each internally consistent, can still disagree with each other.** Three Component 1
figures existed in the notebooks and appeared in no slide — Task 3(c), Task 4(b continued) and Task
4(c). One of them was *added during this session* to close a handout gap: the notebook was patched
and the deck was not. Nothing flagged it. Every check in place was a **within-artifact** check —
the notebooks were complete, the deck was self-consistent, the compliance table mapped every
sub-task to a notebook cell. None of them looked across the gap.

The same shape of error hit the slide numbering twice: the deck grew, both companion documents kept
their old numbers, and the headers were renumbered while cross-references buried in prose ("covered
on slide 16 above") were not — so half the script pointed at the wrong slides while looking fine.

**The fix is a check that spans the two artifacts, not a more careful reading of either.**
`final_test.py` §3b now diffs `figures/*.png` against the filenames in `build_deck.js` in both
directions, and there is a cross-check that prints every prose slide reference beside the title of
the slide it actually points at. Both take seconds and neither depends on remembering.

**Two curves that agree will hide one of themselves, and the fix is width, not colour.** This
happened **twice**, in two different figures, and the second time only because the first was never
written down.

- **Component 1, single trajectory.** Numerical and analytic agree to 6.7e-9, so they sit exactly on
  top of each other. The analytic curve was drawn in white — visible on the blue curve, invisible in
  the legend key. Redrawing it dark grey fixed the legend and made it vanish against the data.
- **Component 3, "which curve is the truth".** Same shape of error: the prediction (`lw=2.2`) was
  drawn *first*, then the truth (`lw=2.6`) *on top of it*. Being both later and thicker, blue painted
  over red completely. The panel whose entire purpose was "these two agree" showed a single curve,
  which reads as "the prediction was not plotted."

**Neither colour alone nor draw order alone is enough — the two lines must differ in WIDTH.** The
pattern that works: the reference curve as a **thick pale band drawn first**, the comparison curve as
a **thin dark dashed line drawn on top**. The dashes then read against the band *and* as a
distinguishable key in the legend.

```python
a.plot(truth_x, truth_y, color="#9ecae1", lw=5.0, solid_capstyle="round", label="truth")
a.plot(other_x, other_y, color="#c1121f", lw=1.7, dashes=(5, 4),        label="prediction")
```

**Why it kept happening:** agreement is the *result being demonstrated*, so the figure that shows it
best is exactly the figure most likely to hide it. Any figure whose caption says two curves match
needs this check before it ships — and a rendered look at the PNG, because the geometry is correct in
both the broken and fixed versions. Only the pixels differ.

---

## Physics audit, 2026-08-30 — recomputed from first principles

Every quantity below was recomputed in a scratch script that reads **nothing** from the notebooks,
then compared against what the notebooks claim. Derivatives were taken **numerically** rather than
by hand, after a first attempt at this audit produced four false alarms from a sign slip in a
hand-derived `dU/dφ` — the check was wrong, not the notebook. That is worth recording on its own:
*a verification script is code, and gets the same scepticism as the code it verifies.*

| quantity | recomputed | notebook claims |
|---|---|---|
| `1/(2m)` vs `4E_C` | 4.000000 | exact identity |
| `mω²` vs `E_L` | 0.500000 | exact identity |
| well minimum | 2.85234 rad | 2.85 |
| barrier height `U(0) − U(φ_min)` | 7.75833 E_C | 7.76 |
| curvature sign at well / at φ=0 | + / − | minimum / barrier |
| tunneling doublet `E₁−E₀` | 0.134432 E_C | 0.134 |
| `E₂−E₀` | 4.619 E_C | 4.6, "factor of 34" (34.4) |
| HO spectrum vs `ℏω(n+½)` | 3.6e-15 | 5.3e-15 |
| harmonic solver vs exact | 1.07e-9 | 6.7e-9 |
| energy drift, 4 periods | 1.19e-9 | 1.9e-9 |
| cosine small-amplitude ω | 1.41418 | √2 |
| coupled energy drift (with λp₁p₂) | 4.6e-10 | conserved |
| Lyapunov at E≈1 / E≈12 | +0.0054 / +0.0086 | ≈0, regular at every energy |
| `A[:,0] − B[:,0]` | 4.4e-15 rad | paired, no φ_ext offset |
| copy-classical gap from raw data | 1.0724 rad | 1.067 |

All 16 display equations were checked by hand against the handout: Hamilton's equations, the cosine
force `−(mω²x + V₀k sin kx)`, the coupled `ẋᵢ = pᵢ/m + λpⱼ` with the coupling correctly absent from
`ṗᵢ`, the ladder definitions of `x̂` and `p̂`, `Eₙ = ℏω(n+½)`, the scqubits fluxonium Hamiltonian, the
parameter map, and the MLP's three layers. No errors.

**Two things the audit turned up that were not physics.** `	frac` appears 34 times in notebook
markdown (fine — MathJax) and **zero** times in any string that reaches matplotlib (where it would
raise); that separation is now checked rather than assumed. And Jupyter had left a two-month-old
checkpoint copy of a working draft under `.ipynb_checkpoints/`, long superseded by the live file and
quietly diverging from it. **Checkpoint directories are worth scanning whenever files move or get
renamed** — Jupyter writes those copies without being asked, they are ignored by git so they never
show up in `git status`, and a stale duplicate of a document is a trap for the next reader.

---

## Deep verification, 2026-08-30 — sources, and a sharper statement of the handout error

Everything below was checked against the textbooks themselves, the installed library source, and
the published literature — not against this project's own earlier notes.

### The citations hold

The PDF-to-book page offset for Griffiths is **+18**, pinned by 80 printed folios with 80 agreeing.
All ten cited locations land where the guide says: 2.3.1 (p.40), 3.1 (p.93), 3.2 (p.95), 3.3 (p.97),
3.4 (p.103), 3.5 (p.105), 3.5.2 (p.108), 3.6 (p.113), Problem 3.42 (p.126), 9.2 Tunneling (p.358).
One internal inconsistency was found and fixed: the guide gave 2.3.1 as both "pp. 40-47" and
"pp. 41-47". Section 2.3.2 begins on p.48, so **40-47** is right.

Every Essler equation number checks out verbatim: (228) the oscillator Hamiltonian, (230) the ladder
operators, (231) `[a,a-dag] = 1`, (233) `H = hbar*w*(a-dag*a + 1/2)`, (234) `N = a-dag*a`,
(246) `E_n = hbar*w*(n + 1/2)`, (259)-(261) the ground-state expectation values and `dx*dp = hbar/2`.
Essler (259) also settles the operator convention: he writes `<0|x|0> = sqrt(hbar/2mw)<0|a+a-dag|0>`
and `<0|p|0> = -i*sqrt(m*hbar*w/2)<0|a-a-dag|0>` — **identical to the definitions the notebook uses**.

### The handout error, stated precisely

Earlier notes said "`V0 <-> E_J` flips sign at half flux". That is true but understates it. The real
problem is that **the handout's classical form cannot be made to match at any nonzero flux, under any
single change of variable.**

The handout gives the classical Hamiltonian as `H = p^2/2m + 0.5*m*w^2*x^2 - V0*cos(k x)`, in which
**both** terms are centred on `x = 0`. The fluxonium is not like that. Its harmonic term is centred on
`phi = 0` while its cosine is displaced by `phi_ext`:

    U(phi) = 0.5*E_L*phi^2 - E_J*cos(phi + phi_ext)          <- installed scqubits source, verbatim

Follow the handout's own substitution `x = phi - phi_ext` and the cosine lines up (`cos(x + 2*pi) =
cos(x)`, so `V0 = +E_J`) but the harmonic term becomes `0.5*E_L*(x + pi)^2` — centred at `x = -pi`.
Measured over `x` in [-6, 6] that mapping is wrong by **11.89 E_C**. Keep `x = phi` instead and the
harmonic term is exact while the cosine needs `V0 = -E_J`; that reproduces the true potential to
**0.0000 E_C**, and is what the notebooks do.

    handout's substitution, V0 = +E_J : max error 11.89 E_C
    notebook's x = phi,     V0 = -E_J : max error  0.0000 E_C
    the same handout mapping at phi_ext = 0 : max error 0.0000 E_C

So the handout's mapping is exact **only at zero flux**, and the recommended operating point is half
flux. This also explains finding #1: the two coordinate conventions on p.7/p.8(a) versus p.8(b) are
not independent slips, they are two symptoms of this one thing.

**The literature agrees.** Fluxonium papers carry two conventions — flux inside the cosine
(`- E_J*cos(phi - phi_e)`, what scqubits uses) or flux inside the inductive term
(`0.5*E_L*(phi + phi_e)^2 - E_J*cos(phi)`). The handout's form has the flux in *neither*, which is
why it only works at `phi_ext = 0`. Published descriptions of the half-flux sweet spot note it
gives "the **+ sign** in front of the Josephson term" — independent confirmation of `V0 = -E_J`.

### A trap that is not live yet, but will be

The scqubits **documentation** writes the potential with `cos(phi - phi_ext)`; the **installed v4.3.1
source** computes `cos(phi + 2*pi*flux)`. At half flux these coincide exactly, because
`cos(phi + pi) = cos(phi - pi)` — which is why nothing here is affected. Off half flux they do not:

    flux = 0.50 : identical
    flux = 0.40 : differ by 5.88 E_C
    flux = 0.25 : differ by 10.00 E_C

Checked against the library: at `flux = 0.30`, `Fluxonium.potential()` matches the `+` form to 0.00
and the `-` form to 9.51 E_C. **The roadmap item "sweep flux" walks straight into this.** Take the
potential from `fluxonium.potential(...)` rather than retyping either form.

---

## What these have in common

1. **The code ran fine.** Neither error raised anything. A silent wrong answer is the expensive kind.
2. **The plot looked plausible.** In both cases the figure was the thing that misled me — a potential curve drawn over states that did not belong to it, and a scatter of dots I read as chaos.
3. **The check that caught it was external.** Not "does this look right" but "does this match `scqubits`' own definition" and "what does the Lyapunov exponent actually say."
4. **Both had a real consequence.** The first cost a factor of nine in model accuracy. The second would have put a false claim in front of my PI.

The working rule I have taken from this: *a figure is a picture, not a measurement.* If a claim can be
reduced to a number, reduce it to a number before writing it down.
