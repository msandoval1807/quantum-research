# Classical & Quantum Mechanics — Study Guide

**Author:** Marcos Sandoval Lucas
**Project:** AI Design of Quantum Processors — Mondragon-Shem Quantum Group, UIC College of Engineering
**Purpose:** Explain the concepts behind all three components starting from *why the idea exists at
all*, then the intuition, then the equation, then a decoding of every symbol.

> **How to read this.** Most concepts have three layers — **In plain words** (the intuition), **The
> math** (the equation), and **Decode it** (every symbol explained). The plain-words layer stands on
> its own if the maths is unfamiliar. Nothing is defined after it is used, and there are no
> appendices: if a term appears, its explanation is either right there or in an earlier part.

> **Conventions & sources.** The quantum notation follows the group's assigned text, **Essler,
> *Lecture Notes for Quantum Mechanics* (Oxford)** — same Hamiltonian, same ladder operators, same
> spectrum. Cross-references are collected in **Part 9**. Two notes: Essler writes the operators
> using a length scale **ℓ = √(ℏ/2mω)** (§4.6), and Essler does **not** cover the **Wigner
> function** — that comes from the project handout (§4.12). Hardware context is **Part 12**.
> The classical material follows **Goldstein, *Classical Mechanics* 3rd ed.**, mapped in **Part 11**.
> All page numbers cited for Griffiths and Goldstein were checked against the PDFs on 2026-08-13.

## Reading order

| Part | What it covers | Why it is here |
|---|---|---|
| **0** | What the project is, and what machine learning is | The point of the whole thing. |
| **1** | **Why states? Why energy? What is energy here? Why negative?** | The layer underneath every other part. Read it first. |
| **2** | Classical mechanics — Component 1, Tasks 1→4 | The cheap side of the data. |
| **3** | **The maths quantum mechanics needs** — vectors, complex numbers, matrices, eigenvalues, probability | Part 4 assumes all of this. Do not skip it. |
| **4** | Quantum mechanics — Component 2, Tasks 1→3 | The expensive side of the data. |
| **5** | The neural network — Component 3 | The map between the two. |
| **6** | How it all connects | The arc, in one page. |
| **7–12** | Glossary, sanity checks, textbook maps (Essler, Griffiths, Goldstein), hardware | Reference, once you are working. |

---

# PART 0 — What the project is (and is not)

The project's direction is sometimes misread as "use quantum computing to make AI run faster." The
actual direction is the reverse:

> **Use ordinary (classical) machine learning, running on a normal computer, to predict the
> properties of quantum hardware — so the expensive quantum calculation need not be run every time.**

The title states it: "AI **Design of** Quantum Processors." AI is the *tool*; the quantum processor
is the *thing being studied*.

A common analogy for quantum *computing* — "a normal computer tries each path through a maze one by
one, while a quantum computer tries all paths at once" — describes algorithms that exploit
superposition. That is a different subject. This project concerns **quantum mechanics / quantum
hardware**: the physics of the device itself. The work here is on the *physics-and-data* side, not
the *algorithm* side.

**The whole pipeline in one picture:**

```
Component 1            Component 2              Component 3
CLASSICAL  ───────►    QUANTUM       ───────►   MACHINE LEARNING
(the inputs)           (the answers/targets)    (learn the map: inputs → answers)

cheap to compute       expensive to compute     once trained, predicts the
                                                 expensive answer from the
                                                 cheap input
```

The deeper scientific question: **how much about a quantum system can be predicted from classical
information alone — and where does that prediction break down?** That breakdown point is where the
interesting physics lives.

The **harmonic oscillator** (a mass on a spring) is the test system for one reason: it can be solved
**exactly** both classically and quantum-mechanically. That gives an answer key. The project's
golden rule — *never trust a numerical result that cannot be checked against an exact formula* —
relies on the oscillator always providing that exact formula.

## 0.1 What machine learning is, and where this work fits

**In plain words.** Normally a computer is told the rule: "if the input is this, give that." Machine
learning flips that around. Instead of writing the rule, you show the computer many **examples** —
inputs paired with their correct answers — and it adjusts itself until its guesses match those
answers. Once trained, it can take a **new** input it has never seen and predict the answer. The
rule is *learned from data*, not hand-written.

**A simple analogy.** To guess a house's price from its size: collect 500 houses where both are
known, and draw the line that best fits them. For a new house you then need only the size — read the
price off the line. The "learning" was finding that line. Real ML does the same with many inputs at
once and far more flexible shapes than a straight line.

**The two ingredients ML always needs:**
- **Inputs** — information that is cheap and always available (the house's size).
- **Targets** — the answer you actually want but which is expensive to get (the price).

| Component | Role in the ML pipeline | The analogy |
|---|---|---|
| **1 — Classical** | generates the **inputs** (phase-space orbits, energies — cheap) | the house's size |
| **2 — Quantum** | generates the **targets** (spectra, dynamics — expensive) | the house's price |
| **3 — ML** | trains a model on many (input, target) pairs to learn the map | drawing the best-fit line |

**So why all this work before any ML?** A model is only ever as good as the data it is fed.
Components 1 and 2 *are* the foundation of the machine learning — they build the clean, verified
dataset the model cannot work without. This is also why the harmonic oscillator was chosen: its
quantum target can be computed **exactly**, so when the model predicts, there is a real answer key.

**The deeper point.** The science is not "make the model fit." It is to find *where* the prediction
starts to fail — because the place classical information can no longer predict the quantum answer is
exactly where the genuinely quantum physics lives.

## 0.2 Where AI fits, and what "predicting the quantum side" really means

**Is "AI" something separate from the machine learning?** No — here they mean the same thing.
*Artificial intelligence* is the broad umbrella; *machine learning* is the specific branch where the
computer learns a rule from examples. The model trained in Component 3 **is** the "AI" in the project
title. There is no separate AI component.

**The tempting misreading.** It is natural to picture the classical physics itself producing the
spectra and dynamics. It does **not**. Classical mechanics has no notion of quantized energy levels
or of a quasi-probability that can go negative — running Hamilton's equations harder will never
output an energy spectrum.

**What actually produces the prediction.** The **trained model** is the bridge. The classical model
supplies the *input features*; the ML model supplies the *learned mapping*, extracted from matched
pairs during training. So the precise statement is: **the classical data, passed through a trained
model, reproduces the quantum dynamics** — not the classical physics alone.

**Why this is science and not a magic trick.** The prediction works only to the extent the classical
information actually carries fingerprints of the quantum answer. Sometimes it does — a coherent
state's average traces the classical orbit almost exactly (Ehrenfest, §4.11). Sometimes it cannot —
a Wigner function's **negative** regions are purely quantum (§4.12), with no classical shadow.
Locating where classical input stops being enough is the real discovery.

---

# PART 1 — The ideas underneath everything

*Before any mechanics, classical or quantum: what the theory is even for, and four questions that
everything else silently assumes an answer to. This part exists because the rest of the guide used
to start one layer too high — twice.*

## 1.0 What is quantum mechanics actually *for*?

**The framing to drop first.** Quantum mechanics is **not** a machine for locating particles. Intro
courses give that impression because "particle in a box" is the easiest first example, but it is
misleading — and especially so here. In the fluxonium there is **no particle anywhere**. `φ` is a
magnetic phase across a circuit loop and `n` is a count of Cooper pairs that have crossed a junction
(§1.3). There is no little ball whose position is being tracked; the question "where is it" barely
applies.

**What the theory actually is.** A **prediction machine for measurement outcomes**. Set up a system,
measure something, get a number — quantum mechanics tells you the probability of each possible
number. That is the whole content. The state is not the goal; it is the **intermediate object** you
need in order to compute those predictions.

**The shape of it, in language from linear systems.** A state-space model is

```
ẋ = Ax + Bu        x is the state vector
y  = Cx + Du       y is what you actually measure
```

Nobody wants `x` for its own sake — you want the output `y`. But you cannot get `y` without `x`,
because `x` is the minimal thing that makes the output computable. Quantum mechanics has exactly this
shape:

| state-space | quantum |
|---|---|
| state vector `x` | `\|ψ⟩` — a list of complex amplitudes (§4.1) |
| dynamics `ẋ = Ax` | Schrödinger equation, `iℏ d\|ψ⟩/dt = Ĥ\|ψ⟩` (§4.9) |
| output `y = Cx` | expectation value, `⟨φ̂⟩ = ⟨ψ\|φ̂\|ψ⟩` (§3.5) |

The `sesolve` call in Component 2 is literally this — propagate the state, immediately extract the
outputs. `e_ops` is the `C` matrix:

```python
qt.sesolve(H_flux, packet, tlist, e_ops=[phi_op, n_op])
```

The full state `|ψ⟩` is never looked at directly. (The one exception is the Wigner function, §4.12,
which is interesting *precisely because* it shows the whole state instead of two averages.)

**So what is this project trying to achieve?** Three engineering questions about a real device:

1. **What energies can it have?** → the spectrum, which sets the frequency the qubit is driven at.
   The 0.134 `E_C` doublet (§4.13) *is* an operating frequency of the device.
2. **How does it evolve in time?** → that is what a gate operation is.
3. **How long do the two levels stay distinguishable?** → coherence.

The state is needed to answer any of those, and is not wanted beyond that.

**And why the project exists at all.** Computing quantum states is **expensive and does not scale** —
and it is worth seeing *how* badly, because it is the whole justification for the work.

**First, what "Hilbert dimension" actually means: how long the list of numbers is.** A quantum state
*is* a list of complex amplitudes, one per energy level (§4.1). The dimension is the length of that
list — nothing more. The notebook prints it:

```python
DIM = H_flux.shape[0]        # 80
qt.coherent(DIM, alpha)      # -> a list of 80 complex numbers
```

So "80-dimensional Hilbert space" means "the state is 80 numbers."

**Why coupling multiplies instead of adding.** You need **one amplitude per combination**. Two toy
systems with 3 levels each would be 3 + 3 = 6 numbers if they could be tracked separately — but the
joint state needs 3 × 3 = 9, one for *(A in level i, B in level j)* for every pair. They cannot be
tracked separately, because the system can occupy states in which A and B have no independent
description at all; that is **entanglement**, and it is why the joint list is irreducible. So each
extra fluxonium multiplies the dimension by 80.

**Memory is then just `dimension × 16 bytes`** (one complex number in double precision):

| coupled fluxoniums | Hilbert dimension (cutoff 80) | memory for one state |
|---|---|---|
| 1 | 80 | negligible |
| 3 | 512,000 | 8 MB |
| 5 | 3,276,800,000 | **52 GB** |
| 6 | 262,144,000,000 | **4.2 TB** |

"4.2 TB" does not mean slow — it means the state **cannot be stored at all**, before any question of
evolving it (which needs repeated multiplication by a `dimension × dimension` matrix). For plain
two-level qubits the growth is `2ᴺ`, so 300 qubits would need ≈10⁹⁰ amplitudes — more than the number
of atoms in the observable universe.

**The comparison that makes it concrete** — the same systems, described both ways:

| oscillators | **classical** state | **quantum** state |
|---|---|---|
| 1 | 2 numbers | 80 |
| 3 | 6 numbers | 512,000 |
| 5 | 10 numbers | 3,276,800,000 |
| 6 | 12 numbers | 262,144,000,000 |

Classical grows as `2N` — **add** two numbers per oscillator. Quantum grows as `80ᴺ` — **multiply** by
80 per oscillator. Linear against exponential. **That gap is this project in one table:** the left
column stays free forever, the right column hits a wall at about five devices. So the behaviour of a
five-fluxonium chip cannot be computed directly — it has to be *predicted* from something cheap.

Designing a chip means trying many parameter combinations, and a full quantum simulation for each is
unaffordable. So the bet is: *can a cheap classical calculation predict what the expensive quantum
one would have said?* If yes, designs can be searched cheaply and the expensive simulation run only
on the finalists. **That is what "AI Design of Quantum Processors" means** — and Part 5 is the honest
boundary on that bet.

> **Two things this is *not*.** Quantum circuits are not faster (Part 12), and their advantage is not
> that they conserve energy. **Energy conservation is a lossless property, not a quantum one** — a
> resistanceless *classical* LC circuit conserves energy just as exactly. This project measures both
> and they agree: classical energy drift 1.9e-9 (Component 1), quantum `⟨Ĥ⟩` drift 2.1e-7
> (Component 2). What conservation means physically in a circuit is that energy sloshes between the
> capacitor's electric field and the inductor's magnetic field and none of it leaks to heat — so the
> oscillation never dies. A resistor makes it decay, which is the inward spiral of §2.5 instead of a
> closed loop. The quantity that actually limits a qubit is not energy conservation but **coherence**:
> how long the *phase relationship* inside a superposition survives. Phase can randomise without any
> energy being lost at all, which is why engineers quote both `T₁` (energy decay) and `T₂` (phase),
> and why `T₂` is usually the binding constraint.

**Where position honestly fits.** It is **one observable among many**, privileged in textbooks rather
than in the formalism. For an electron in an atom you might care about it; for this circuit you care
about phase and charge. And a quantum state does not *secretly know* a position and hide it — before
measurement there is no definite value, not merely an unknown one (§4.4). That is why the Wigner blob
has finite area instead of being a point.

## 1.1 Why is there such a thing as a "state"?

**The question.** Physics texts say "the state of the system" constantly, as though it were obvious
what that means. It is not obvious, and it is not a quantum word — Component 1 has states too.

**In plain words.** A **state** is the *save file*. It is whatever you would have to write down so
that, if you walked away and came back, you could resume exactly — no more and no less.

Said precisely: *the smallest complete answer to the question "what is this system doing right
now?"* — the minimum you would have to record so that, together with the laws of motion, the entire
future follows.

That is the whole definition. It has two halves, and both matter:

- **Complete** — knowing the state, nothing else about the present can help you predict the future.
- **Minimal** — every number in it is doing real work. Nothing redundant.

**"State" is a bookkeeping word, not a physics word.** Every theory has to answer "what do I need to
write down?", and *state* is the name for that answer. The word names the **role**, not the content —
which is exactly why it appears on both the classical and the quantum side meaning structurally the
same thing while containing completely different numbers.

**Why it takes exactly two numbers classically.** For a mass on a spring, is position enough? No.
Two masses at the same place, one moving left and one moving right, do completely different things
next. So position alone is not complete. Add momentum: now you know where it is *and* how it is
moving, and Hamilton's equations (§2.6) determine everything after that. Is momentum redundant? No —
you just showed it was needed. So `(x, p)` is complete and minimal, and *that pair is the state*.

**Phase space is a plane *because* the state is two numbers** — one axis per number the state needs.
That is not a design choice, it is a consequence. Two coupled oscillators need four numbers, so their
phase space is 4-dimensional and cannot be drawn, which is exactly why Task 4 (§2.10) has to fall
back on 2-D projections.

**Where it sits in your own code:**

```python
sol = solve_ivp(hamilton_rhs, t_span, [x0, p0], ...)
```

`[x0, p0]` *is* a classical state. The solver's whole job is: given a state, produce the state at
later times.

**Why the quantum state is a longer answer.** The same question, asked of a quantum system, has a
different answer — not because "state" changed meaning, but because the two-number answer is not
available. The uncertainty principle (§4.4) says no system ever *has* a definite `x` and a definite
`p` at once, so there is no `(x, p)` pair to write down. What can be written down is a list of
**complex amplitudes** — one per energy level, saying how much of each is present (§4.1). Given that
list, the Schrödinger equation determines the entire future: complete, minimal, same job. In your
code that is

```python
qt.coherent(DIM, alpha)      # DIM = 80, so this state is 80 complex numbers
```

**The distinction that causes the most confusion — what you plot is not always the state.**

Classically the two coincide: you plot `(x, p)`, which *is* the state. That is why phase space feels
so natural.

Quantum-mechanically they come apart. The state is those 80 complex numbers. `⟨φ̂⟩` and `⟨n̂⟩` are two
real numbers **squeezed out** of it by averaging (§3.5). So:

| | classical | quantum |
|---|---|---|
| the state | `(φ, n)` — 2 numbers | `\|ψ⟩` — 80 complex amplitudes |
| what the notebook records | `(φ, n)` — **the state itself** | `⟨φ̂⟩, ⟨n̂⟩` — **2 averages taken from it** |

**So `B[i]` is not a quantum state.** It is a pair of averages extracted from one, at 40 instants.
Component 3 therefore does not learn "classical state → quantum state"; it learns

> classical trajectory → **two averages taken from** the quantum state

which is a much smaller target than the state itself. That is the same point §4.11 makes when it says
averaging throws away the spread and the interference — and it is the reason the Wigner function
(§4.12) exists at all: it draws the *whole* state in the `(x,p)` plane, instead of collapsing it to
its average.

## 1.2 Why is everything about energy?

**The question.** Both components are relentlessly about energy — energy contours, energy spectra,
the Hamiltonian, `e_ops=[phi_op, n_op]`. Why energy rather than force, or speed, or anything else?

**In plain words.** Because **energy is the object that generates the motion.** It is not one
property among many that you might happen to be interested in. Write the energy down as a formula in
terms of position and momentum, and the equations of motion fall out of it mechanically.

**The classical statement.** Hamilton's equations (§2.6) are

`ẋ = ∂H/∂p`  and  `ṗ = −∂H/∂x`

Read that as a machine: *give me the energy `H` as a function of `(x, p)`, and I will hand you back
how the system moves.* You never have to think about forces again — differentiate the energy and the
force appears. That is why §2.4 spends time setting up the Hamiltonian before any motion happens.

**The quantum statement is the same shape.** The Schrödinger equation (§4.9) is

`iℏ d|ψ⟩/dt = Ĥ|ψ⟩`

Same structure: hand it the energy operator `Ĥ`, and it hands back the evolution of the state. This
is why Component 2 Task 1 spends all its effort *building `Ĥ`* — once you have the energy, the
dynamics are a solved problem.

**So the pattern across the entire project is:**

```
write down the energy   →   the equations of motion follow   →   solve them numerically
      H(x,p)                    Hamilton's equations              solve_ivp      (classical)
      Ĥ                         Schrödinger equation              sesolve        (quantum)
```

Two languages, one strategy. This is also why the classical and quantum sides can be honestly
compared at all: they are built from the *same* energy expression, one with numbers and one with
operators.

**A second reason.** Energy is **conserved** — it does not change as the system moves. A quantity
that stays fixed is a powerful constraint: it confines the motion to one curve in phase space
(§2.5), and it gives a free correctness check on any simulation (if your computed energy drifts,
your solver is wrong — §8). Component 1 measures a drift of 1.9e-9 and Component 2 Task 3 measures
`⟨Ĥ⟩` conserved to 2.1e-7. Neither number is decoration; each is a test that could have failed.

## 1.3 What *is* the energy, in this project specifically?

**The question.** "Kinetic plus potential" is fine for a mass on a spring. But the fluxonium is a
superconducting circuit, `φ` is not a position and `n` is not a momentum. So what is actually being
measured?

**Real electrical energy in a circuit.** The fluxonium is a genuine piece of hardware: a Josephson
junction shunted by a large inductor, cooled to near absolute zero so it superconducts. Its
Hamiltonian is

$$\hat H = 4E_C\,\hat n^2 + \tfrac12 E_L\hat\varphi^{\,2} - E_J\cos(\hat\varphi+\varphi_{ext})$$

and each of the three energies is a real, physical, measurable property of the device:

| Symbol | Name | What it physically is |
|---|---|---|
| `E_C` | **charging energy** | the energy cost of putting one more Cooper pair of charge onto the island. Set by the capacitance — a bigger capacitor stores charge more cheaply, so `E_C` is smaller. |
| `E_L` | **inductive energy** | the energy stored in the magnetic field of the shunt inductor when current flows. The circuit's "spring." |
| `E_J` | **Josephson energy** | the energy associated with Cooper pairs tunnelling across the junction's thin insulating barrier. This is the term with no classical-circuit analogue — it is quantum tunnelling built into a component. |

**And the two variables:**

- **`φ` is a magnetic phase, not a position.** It measures the magnetic flux threading the circuit
  loop, in units where one flux quantum is `2π`. It is dimensionless — an angle. When the guide says
  "the wells sit at `φ ≈ ±2.85`", that is 2.85 radians of phase, not 2.85 metres.
- **`n` is a number of Cooper pairs, not a momentum.** It counts how many pairs of electrons have
  moved across to the island. Also dimensionless — it is a *count*.

### What a Cooper pair is, and why the whole device depends on it

**In plain words.** Two electrons bound into a single travelling unit — which should immediately look
wrong, because electrons repel each other.

**The mechanism.** In a metal, electrons move through a lattice of positive ions. An electron flying
past tugs the nearby ions slightly toward it, leaving a small region of **excess positive charge** in
its wake. Ions are about a thousand times heavier than electrons, so they respond slowly and the
distortion lingers after the first electron has gone — and a second electron is drawn into it. The
attraction is **indirect**, carried by a lattice vibration rather than acting between the electrons
directly.

> Two people on a trampoline do not attract each other. But each makes a dip, and each rolls toward
> the other's dip. The trampoline does the work.

The binding is very weak, which is exactly why superconductivity needs millikelvin temperatures —
thermal jostling would break the pairs instantly otherwise. It is also why "two electrons holding
hands" is a misleading picture: a Cooper pair is hundreds of nanometres across, so pairs overlap each
other heavily rather than sitting as tidy little molecules.

**Why pairing changes everything — and it is not about the binding, it is about statistics.**
Electrons are **fermions**: no two may occupy the same quantum state (Pauli exclusion), which is why
atoms have shells and matter is rigid. Bind two together and their spins cancel, so the *pair* has
integer spin and behaves like a **boson** — and bosons obey the opposite rule. They may all occupy
the same state, and they prefer to.

So below the critical temperature **every Cooper pair condenses into one shared quantum state**: not
billions of particles behaving independently, but a single wavefunction spanning the whole piece of
metal.

**That is why a circuit is quantum at all.** Quantum effects normally wash out at large scale because
everything averages away. In a superconductor they do not, because everything is locked into one
state — so the fluxonium is a macroscopic object that behaves quantum-mechanically. It is also why
resistance vanishes: scattering one pair means breaking it *and* removing it from the condensate,
which costs a minimum energy, and below that threshold scattering simply cannot occur.

**Three things in the Hamiltonian this explains:**

1. **Why `n` counts pairs.** Charge crosses the junction in units of `2e`, because the pair is what
   travels.
2. **Where the factor of 4 in `4E_C n̂²` comes from.** The charging energy of `n` pairs is
   `(2e)²n²/(2C) = 4·[e²/2C]·n² = 4E_C n²` with `E_C = e²/2C`. **The 4 is 2²** — the pair's doubled
   charge, nothing more.
3. **Where the cosine comes from — the important one.** Because all pairs share one state, that state
   has a single **phase**, and the phase *difference* across the junction is physically real and
   measurable. That is `φ`. A Josephson junction is two superconductors separated by a barrier thin
   enough to tunnel through, and the current across it depends on that phase difference,
   `I = I_c sin φ`. Integrating current × voltage gives the stored energy:
   `∫ I_c sin φ · (ℏ/2e) dφ = −(ℏI_c/2e) cos φ = −E_J cos φ`.

So the chain runs: **Cooper pairs → one condensate with a phase → tunnelling gives a `sin φ` current
→ a `−E_J cos φ` potential → anharmonicity → an addressable qubit.** That cosine is why the
oscillator is not a plain parabola, which is why the levels are unevenly spaced (§2.9, Part 12), and
it is also the term that breaks Ehrenfest's condition (§4.11) and so gives Component 3 something to
learn.

**What Cooper pairs actually buy — why anyone builds qubits this way.** Three things, and no other
approach gives all three at once:

1. **A quantum system that can be manufactured.** Without the condensate a chunk of metal is 10²³
   electrons behaving independently and every quantum effect averages away. With it, the device is
   one quantum state — so it can be *printed* with lithography rather than trapped atom by atom in a
   vacuum chamber. Trapped ions are naturally quantum but cannot be fabricated by the million; this
   is the trade the superconducting platform makes.
2. **No dissipation — the one that really matters.** A qubit must hold a superposition, and any
   energy leaking out destroys it. Resistance *is* that leak, so a normal-metal circuit would
   decohere almost immediately. Zero resistance is what lets the superposition survive long enough to
   be useful.
3. **A nonlinear element that is also lossless.** To be a qubit the level spacing must be uneven
   (§2.9). Among circuit elements, resistors dissipate and capacitors and inductors are exactly
   linear — **the Josephson junction is the only known element that is nonlinear *and* lossless**, and
   it is nonlinear precisely because Cooper pairs tunnel across it. Without it there is only an LC
   oscillator with evenly spaced levels, which cannot be addressed.

**Why the oscillator language transfers anyway.** Because `φ` and `n` are **conjugate** in exactly
the way `x` and `p` are: they obey the same commutation relation, so the same uncertainty principle
applies, the same Hamiltonian machinery works, and the same ladder operators can be built. The
mapping the notebook uses,

```
x ↔ φ,   p ↔ n,   V₀ ↔ E_J,   m = 1/(8E_C),   ω = √(8E_C E_L)
```

> **One caveat on `V₀ ↔ E_J`.** It is exact only at **zero** flux. At the half-flux point this
> project runs at, `cos(φ + π) = −cos φ`, so the same potential needs **`V₀ = −E_J`** — a
> difference of `2E_J = 10 E_C`. That sign is precisely what makes the fluxonium a **double well**
> rather than the single well of §2.9, and so what produces the tunneling doublet. See §4.13, and
> `Handout_Compliance.md`, which records that the handout states this mapping without the caveat.

is not an analogy or an approximation — it is the statement that these are the *same mathematics*
wearing different physical clothes. That is what lets Component 1's classical oscillator be a
genuine classical limit of Component 2's qubit rather than a lookalike.

**The units the code works in.** Everything is measured in multiples of `E_C`, so `E_C = 1.0` by
definition and `E_J = 5.0`, `E_L = 0.5` are ratios. This is why energies in the notebook are bare
numbers with no joules attached: they are all "in units of the charging energy." Real fluxonium
devices have `E_C` of order a few GHz in frequency units.

## 1.4 Why can energy be negative?

**The question.** The fluxonium potential dips below zero. A negative energy sounds impossible —
less than nothing?

**In plain words: the zero of energy is a choice, not a fact.** Only *differences* in energy are
measurable. Nothing you can do in a laboratory measures an absolute energy; every measurement is a
comparison — how much energy did this transition release, how far apart are these two levels. So
where you put the zero is a bookkeeping convention, and you may put it anywhere.

**Where the minus sign comes from here.** The potential is

`U(φ) = ½E_L φ² − E_J cos(φ + φ_ext)`

with `E_J = 5`. The cosine ranges between −1 and +1, so the second term ranges between −5 and +5.
Near a well, the `−E_J cos(...)` term is doing its most negative work and the harmonic term has not
yet grown large, so the sum lands below zero. Nothing physical is happening — the formula simply
places its zero at "no flux, no charge", and the wells sit below that reference point.

**The check that shows it does not matter.** Add 5 to every energy in the problem. The potential
becomes positive everywhere. Now:

- the well positions — unchanged (adding a constant does not move a minimum)
- the barrier height — unchanged (it is a *difference*)
- the level spacings — unchanged
- the tunneling doublet at 0.134 `E_C` — unchanged
- the dynamics — unchanged, since forces come from `−dU/dφ` and the derivative of a constant is zero

Every prediction is identical. That is what "the zero is arbitrary" means, made concrete.

**What *is* physical.** The **gaps**. The 0.134 `E_C` splitting between the two lowest fluxonium
levels is a real, measurable number — it sets a frequency you could drive the qubit at. The 7.76
`E_C` barrier height is real because it is measured from the well bottom. Whenever a number in this
project matters, it is a difference between two energies, never a single energy on its own.

**A familiar version of the same idea.** Gravitational potential energy is `mgh`, and `h` is measured
from... wherever you decide. Sea level, the floor, the tabletop. Choose the tabletop and anything
below it has negative potential energy. Nobody is troubled by this, because only the *drop* matters.

## 1.5 What a derivative is (and why it is everywhere)

*Needed from §2.6 onward. If this is already familiar, skip to Part 2.*

**In plain words.** A **derivative** is a rate of change: how fast one quantity changes when another
one changes. That is all.

- `dx/dt` — how fast position changes as time passes. That *is* velocity.
- `dp/dt` — how fast momentum changes. That *is* force.

**The notation, decoded.**

| Written | Said | Means |
|---|---|---|
| `ẋ` (dot over it) | "x dot" | rate of change of `x` **with respect to time**. Dots always mean time. |
| `ẍ` | "x double dot" | rate of change of the rate of change — acceleration. |
| `dx/dt` | "d x by d t" | the same thing as `ẋ`, written the long way. |
| `∂H/∂p` | "partial d H by d p" | how much `H` changes if **only `p`** is nudged, holding everything else fixed. The curly `∂` signals "there is more than one variable, and I am varying just this one." |

**Why partial derivatives appear.** `H(x, p)` depends on two things. Asking "how does `H` change?"
is ambiguous until you say *which* variable moved. `∂H/∂p` answers "if I nudge the momentum and
leave the position alone." That is exactly the question Hamilton's equations need.

**The one rule you need in practice.** To differentiate a power, bring the exponent down and reduce
it by one:

```
d/dx (x²)  = 2x            d/dp (p²/2m) = p/m           d/dx (½mω²x²) = mω²x
```

Those three are literally all the calculus Component 1 requires. §2.6 does the derivation with them.

**Where it appears in your code.** The function `hamilton_rhs` returns `[p/m, -m*omega**2*x]` — those
two expressions *are* the two derivatives above. And `solve_ivp` exists to do the reverse operation:
given the rates of change, reconstruct the motion. Every differential-equation solver in this project
is answering "I know how fast everything is changing; where does it end up?"

---

# PART 2 — Classical Mechanics (Component 1)

**Aim:** simulate a mass on a spring and generate clean classical data — the trajectories and energy
structure that become the *inputs* to the machine-learning model.

The notebook has four tasks, each building on the last:

| Task | System | New idea |
|---|---|---|
| 1 | perfect spring | energy as a map over phase space |
| 2 | perfect spring | motion — integrating Hamilton's equations |
| 3 | spring + cosine | the potential stops being a parabola |
| 4 | two coupled oscillators | 4-D phase space, Poincaré maps, testing for chaos |

## 2.1 What a harmonic oscillator is, and why it matters

**In plain words.** A harmonic oscillator is anything that, pushed away from its resting place, feels
a force pulling it back — and the harder the push, the harder the pull, *proportionally*. A mass on a
spring is the classic example. So is a pendulum for small swings, a guitar string, an electrical
circuit, and the building blocks of quantum hardware.

**Why it is everywhere.** Almost any stable system, nudged slightly, behaves like a harmonic
oscillator: any smooth "valley" looks like a parabola close to its minimum. That is why this one
model recurs throughout physics — master it once and you have the leading-order behaviour of
countless systems. It is also why the fluxonium's *wells* can be treated as near-harmonic near their
bottoms, which turns out to be the reason the ML model finds its job easy there (§5.5).

## 2.2 Hooke's Law and Newton's Second Law — the starting point

**In plain words.** Hooke's law says the spring's restoring force is proportional to how far the mass
is stretched from centre, pointing back toward it. Newton's second law says force causes
acceleration. Combined, they give an equation for how the mass moves.

**The math.**

Hooke's law:  `F = -k x`   Newton's second law:  `F = m a = m ẍ`

Combine:  `m ẍ = -k x`  →  `ẍ = -(k/m) x`

**Decode it.**
- `F` = force on the mass. `x` = displacement from equilibrium; `x = 0` is the centre.
- `k` = spring constant / stiffness; a stiffer spring has bigger `k`.
- The minus sign means *restoring*: displacement one way produces force the other way.
- `ẍ` = acceleration = the second time-derivative of position (§1.5).

**The clean form.** Defining the **angular frequency** `ω = √(k/m)` gives `ẍ = -ω² x`.

**Why bother renaming `k` as `ω`?** Because `k` alone does not tell you how the system actually
*moves*. A stiff spring carrying a heavy mass can oscillate slowly; a weak spring with a tiny mass
can oscillate fast. What sets the rhythm is the *combination* `√(k/m)`, and that combination is `ω`.
It packages stiffness and mass into the single number that governs the motion — and it is the thing
you would actually measure.

It is not new physics, just a rename: since `ω = √(k/m)`, squaring gives **`k = mω²`**, so `½kx²`
becomes `½mω²x²`. We do it because (a) `ω` is the physically meaningful quantity, and (b) it
generalises: a pendulum, a circuit and the *quantum* oscillator all have a natural frequency `ω`, and
the quantum energy levels come out as `ℏω(n+½)` — pure `ω`, no `k` in sight. Using `ω` now is what
lets Component 1 connect cleanly to Component 2.

## 2.3 Energy: kinetic + potential

**In plain words.** Rather than tracking forces, track **energy** (§1.2 for why). The oscillator has
two kinds: **kinetic** (energy of motion) and **potential** (energy stored in the stretched spring).
In a frictionless oscillator the total never changes — energy trades back and forth. At the turning
points all energy is potential (momentarily stopped); at the centre all of it is kinetic (fastest).

**The math.**

Potential energy:  `V(x) = ½ k x² = ½ m ω² x²`   Kinetic energy:  `T = ½ m v² = p² / (2m)`

**Decode it.**
- `V(x)` is a parabola — a valley centred at `x = 0`.
- `p` = **momentum** = `m v`. Kinetic energy can be written with velocity (`½mv²`) or with momentum
  (`p²/2m`). **The momentum form is the one quantum mechanics needs**, so it is adopted from the
  start — this is a deliberate setup for Part 4, not an arbitrary choice.

## 2.4 The Hamiltonian and phase space

**In plain words.** The conceptual upgrade that makes the rest work: describe the oscillator by
**position and momentum**, treated as two equal partners, rather than position and velocity. The
total energy written in terms of `x` and `p` is the **Hamiltonian**. The 2-D space whose axes are `x`
and `p` is **phase space**, and one point in it is the entire classical state (§1.1).

**What phase space is, concretely.** It is a graph whose horizontal axis is **position** and whose
vertical axis is **momentum** — you plot `p` against `x`, not `x` against time. The power of it: a
single **dot** in this plane is the *complete* state at one instant, telling you both where the
system is and how it is moving. As time passes the dot moves and traces a curve — the trajectory.

We use it because Hamilton's equations need both `x` and `p`, because energy conservation makes the
picture beautifully simple (§2.5), and because **quantum mechanics uses the same plane**. The Wigner
function (§4.12) draws a quantum state in exactly this `(x,p)` picture, which is what lets Component
3 compare classical and quantum data feature for feature.

**The math.**

`H(x, p) = p²/(2m) + ½ m ω² x²`

**Decode it.** `H` is the total energy expressed in terms of `x` and `p`. The first term is kinetic,
the second potential. `H` stays **constant** in time for a frictionless oscillator — energy
conservation.

## 2.5 Why the trajectories are ellipses

**In plain words.** Because total energy stays constant, the point representing the oscillator can
only move along a curve of fixed energy. For the harmonic oscillator that curve is an **ellipse**
centred on the origin. The oscillator endlessly circles its ellipse; a bigger ellipse means more
energy. Different starting energies give nested, non-crossing ellipses, like the rings of a target.

**The math.** Setting `H(x,p) = E` (a constant):

`p²/(2m) + ½ m ω² x² = E`  →  the equation of an **ellipse** in the `(x, p)` plane.

**What a contour is.** Picture the energy as a **landscape**: for every floor-point `(x,p)`, the
"height" is the energy there. It is a bowl — lowest at the centre and rising as you move out in any
direction. A **contour** is exactly like a contour line on a hiking map: it connects all points at
the same height, here all `(x,p)` with the same energy. In the Task 1 plot, colour is the energy
value (dark centre = low, yellow edges = high) and the white rings are specific contours.

Now freeze the energy at one value and ask *which points have exactly that energy?* A constant equal
to (a squared-`x` term) plus (a squared-`p` term) is the equation of an ellipse — the same family as
the circle `x² + p² = r²`, just stretched differently on each axis. In natural units `m = ω = 1` it
becomes `x² + p² = 2E`, a perfect **circle** of radius `√(2E)`, which is why the plot shows circles.

![Why the orbit is an ellipse: the energy contour map (left) and one orbit looping around its ring (right)](slides/assets/phase_space_explainer.png)

*The left panel is the Task 1 contour plot (every ring is one energy — all possible orbits); the
right is the Task 2 trajectory (the dot stuck on one ring, looping around it). "Freezing the energy"
picks one ring out of the map, and that ring is the orbit.*

**Is it always an ellipse?** For the ideal harmonic oscillator — linear spring, no friction — yes,
always, in phase space. Three honest caveats:

- The ellipse is in **phase space**, **not** in real space. In real space the mass just slides back
  and forth along a line.
- With **friction**, energy drains and the dot spirals *inward* instead of closing.
- With a **non-linear spring** (anharmonic — Task 3, and every real qubit), the orbits are still
  closed loops but no longer perfect ellipses. That deviation is exactly what the later tasks study.

**The three properties, and why each is true.** Orbits are *energy-conserving*, *closed* and
*non-crossing*:

- **Energy-conserving** — no friction means nothing removes energy; mathematically `dH/dt = 0` along
  the motion. So the dot stays on one contour forever.
- **Closed** — the motion is sinusoidal, so after one period `T = 2π/ω` both `x` and `p` are back
  where they started. A closed loop means periodic motion.
- **Non-crossing** — a phase-space point *completely* determines the future (§1.1), and Hamilton's
  equations give exactly one direction of travel at each point. If two orbits crossed, that point
  would have two different futures, which is impossible. So the orbits nest like tree rings without
  ever touching.

**Why this matters.** These three properties *are* the sanity checks (Part 8). If a numerical orbit
drifts in energy, fails to close, or crosses itself, the solver is wrong. And the clean nested
structure is the well-behaved feature space the ML model eventually learns from.

## 2.6 Hamilton's Equations — how the point actually moves

**In plain words.** The ellipse says *where* the oscillator can be; Hamilton's equations say *how it
travels* around it. They replace one second-order equation (acceleration) with two simpler,
symmetric first-order equations.

**The math.**

`ẋ = ∂H/∂p`    and    `ṗ = -∂H/∂x`

**Where they come from.** They are **Newton's laws repackaged**. Newton gives one second-order
equation; Hamilton splits the same physics into two first-order ones using the energy function.
(They descend from Lagrangian/Hamiltonian mechanics, but for this project they can be taken as given
rules, because they provably reproduce Newton — as the derivation below shows.)

**Doing the derivation.** Apply both to `H = p²/2m + ½mω²x²`, using the one calculus rule from §1.5:

- **`ẋ = ∂H/∂p`** — only the `p²/2m` term contains `p` (the `x` term is a constant as far as `p` is
  concerned, so it differentiates to 0). The derivative of `p²/2m` is `p/m`. → **`ẋ = p/m`**, which
  just says momentum = mass × velocity. ✓
- **`ṗ = −∂H/∂x`** — only `½mω²x²` contains `x`. Its derivative is `mω²x`, and the minus sign gives
  → **`ṗ = −mω²x`**, which is exactly Hooke's law. ✓

**Now combine them.** Differentiate `ẋ = p/m` once more in time to get `ẍ = ṗ/m`, then substitute:

`ẍ = (−mω²x)/m = −ω²x`

The same answer Newton gives. Two roads, one destination — and that consistency is the point.

**Why this form matters for code.** Numerical solvers prefer first-order equations.
`scipy.integrate.solve_ivp` is built to march exactly this kind of system forward, one small step at
a time, which is why `hamilton_rhs` returns the pair `[p/m, -m*omega**2*x]`.

## 2.7 Task 1 — Energy and phase space (the map)

1. State `E(x,p) = p²/(2m) + ½mω²x²`.
2. Derive Hamilton's equations (§2.6) — show the algebra.
3. Make a **contour plot** of `E(x,p)` over a grid, producing nested ellipses, and explain why they
   are ellipses (constant energy).

## 2.8 Task 2 — Dynamics and trajectories (the motion)

1. Use `solve_ivp` to solve `ẋ = p/m`, `ṗ = −mω²x` for one starting point. Plot the phase-space path
   and mark the start.
2. Repeat for many random starting points — nested non-crossing ellipses, bigger ellipse = higher
   energy.

**The point of Task 2:** the answer is already known, so this validates the numerical pipeline while
it can still be checked against the exact result. Later systems have no exact answer, so the code
must be trusted here first. The trajectory data becomes ML input later.

## 2.9 Task 3 — The anharmonic (cosine) oscillator

> **Tasks 3 and 4 came later.** The PI's updated handout added them after Tasks 1–2 were done. They
> move the project from the perfect spring toward real hardware: first by bending the spring, then by
> coupling two of them together.

**In plain words.** A perfect spring is *harmonic*: the restoring force grows exactly in proportion
to displacement, and every oscillation has the same period regardless of size. A real qubit is not
like that. Adding a cosine term $-V_0\cos(kx)$ makes the force grow *non*-proportionally — the
oscillator becomes **anharmonic**. The orbits stay closed loops but deform away from ellipses, and
the period now depends on the energy.

**Why it matters.** Anharmonicity is what makes a qubit a *qubit*. In a perfectly harmonic system all
energy levels are evenly spaced, so you cannot address just two of them. The cosine — physically, the
Josephson junction — spaces the levels unevenly, letting you isolate a single two-level system. Task
3 is the classical shadow of that effect. (Part 12 has the hardware version.)

**What the task does.**
1. Add `−V₀cos(kx)` to the potential: `H = p²/2m + ½mω²x² − V₀cos(kx)`.
2. Re-derive Hamilton's equations. Only one term changes: the force picks up `−V₀k sin(kx)`.
3. Integrate orbits at several energies and overlay them.
4. Draw a band of initial conditions inside `E_ref ± ΔE`, coloured by energy.

**What to check.** At *small* `x`, `sin(kx) ≈ kx`, so the cosine merely stiffens the spring — the
effective frequency becomes `√(ω² + V₀k²/m)`, which is `√2` in natural units, not `ω = 1`. Low-energy
orbits should therefore look near-elliptical, and the deviation should grow with energy. The period
becoming energy-dependent is the signature of anharmonicity.

## 2.10 Task 4 — Two coupled oscillators, Poincaré maps, and chaos

**In plain words.** Put two anharmonic oscillators together and let them exchange energy through a
coupling term $\lambda p_1 p_2$. The motion now lives in a **4-dimensional** phase space
$(x_1,p_1,x_2,p_2)$ — too many dimensions to see at once — so we look at 2-D *projections* and at
**Poincaré maps**.

### The four words needed before any of this makes sense

I kept seeing "KAM tori" without knowing what any of it meant. Here is the chain, in order.

**1. Integrable = completely predictable.** A system is **integrable** when it has as many conserved
quantities as degrees of freedom. Two oscillators that never talk to each other are integrable: each
keeps its own energy forever, so they can be solved separately and the answer written down. The
single harmonic oscillator of Tasks 1–2 is integrable — which is exactly why it has an exact formula
to check against. Integrable systems never behave chaotically.

**2. A torus is where integrable motion lives.** Take those two independent oscillators. Each goes
round and round its own loop, so each needs a single **angle** to say where it is in its cycle. Two
angles together describe a **doughnut surface** — a *torus*. Angle one is the position around the
ring, angle two the position around the tube. The state is a point on that doughnut, winding in both
directions at once. Each starting energy gives its own doughnut, nested inside the others. That is
all "the motion lies on a torus" means.

**3. Incommensurate = the two rhythms never line up.** Two frequencies are **commensurate** if their
ratio is a ratio of small whole numbers — 2:1, 3:2 — and **incommensurate** otherwise. Picture two
runners on a circular track. If one is exactly twice as fast, they meet at the start line every lap:
the combined motion repeats and the path closes. If the ratio is something like $1:\sqrt2$ they
*never* line up again, and the path winds around the doughnut forever without closing. That
never-repeating-but-not-random motion is **quasiperiodic**, and it is what a smooth curve of dots on
a Poincaré map is showing.

**4. The KAM theorem — what happens when you nudge it.** Real systems are not integrable; mine has
the oscillators coupled. So: does adding a small coupling destroy all that orderly doughnut motion?
The answer is the **Kolmogorov–Arnold–Moser theorem** (Goldstein §11.2, p. 487). If an integrable system is
disturbed by a perturbation, and

  **(a)** the perturbation is *small*, and
  **(b)** the unperturbed frequencies are *incommensurate*,

then the motion **stays on a torus** for all but a negligible set of starting conditions. The
doughnuts survive, slightly bent. They are called **KAM tori** for exactly that reason.

**Why this is a big deal.** It is not obvious. You might reasonably expect any coupling to wreck the
order eventually — and for a *large* coupling it does. KAM says small couplings do not, which is
roughly why the solar system has stayed stable for billions of years despite the planets pulling on
each other.

**Why the two conditions matter here.** Both are checkable in my own system. Condition (b) failing is
the interesting case: if the two frequencies *are* commensurate, the runners keep meeting at the same
spot, the little pushes from the coupling all add up in the same direction instead of averaging out,
and the torus tears. That is a **resonance**, and it is where chaos starts. My mode frequencies work
out to a ratio of 1.363 — not close to any small whole-number ratio — so condition (b) holds and the
tori should survive. They do.

**What a Poincaré map is.** Instead of watching the full continuous motion, record the state only at
the instants it crosses a chosen surface (here $x_2=0$, crossing in one direction). This turns a
tangled trajectory into a set of dots — and because the motion lives on a doughnut, slicing through
it gives a *closed curve*, which is why regular motion shows up as smooth loops.

- **Regular / quasiperiodic motion** → dots fall on smooth closed curves, each the slice through one
  surviving **KAM torus**.
- **Chaos** → dots scatter to fill a 2-D region (a "chaotic sea") with no clean curve. Tiny changes
  in the start lead to totally different futures.

**What I actually measured — my intuition was wrong.** I expected raising the energy to drive a
transition to chaos. It does not. Using the **maximal Lyapunov exponent** $\lambda_{max}$ (the
quantitative test — positive means chaos, zero means regular; Goldstein §11.4, p. 491), at my parameters
$\lambda=0.3$, $V_0=1$ I get $\lambda_{max}\approx0.004$ at $E=1$, $0.007$ at $E=12$, $0.005$ at
$E=30$. All sit at the $\log t/t$ convergence floor, which is what zero looks like numerically. **The
motion is regular at every energy I tested**, and the Poincaré sections agree.

**Why the intuition fails here.** The nonlinearity is a *cosine*, so it is **bounded**:
$|V_0\cos(kx)|\le V_0$ however large the energy gets. The harmonic term grows without limit. So
raising the energy makes this system *more* nearly harmonic — closer to integrable, the opposite of
the usual picture. The KAM tori survive precisely because the perturbation stays small in the sense
the theorem requires.

**Where the chaos actually lives.** Strengthening the *coupling* does it: at $\lambda=0.8$, $V_0=8$,
$E=12$ I measure $\lambda_{max}=0.11$, and at $\lambda=0.8$, $V_0=15$, $E=25$, $\lambda_{max}=0.34$ —
both firmly chaotic. So the order-to-chaos transition is controlled by coupling strength and well
depth. That regime, not the one I ran, is the natural stress test for classical→quantum prediction.

**The lesson.** A Poincaré plot that "looks scattered" is not evidence of chaos, and one that looks
regular is not proof of its absence. Lyapunov exponents are the check; the plot is the picture. This
is the same lesson as the null result in Component 3 (§5.6) — a figure is a picture, not a
measurement.

### What the textbooks say to do first: normal modes

Both books point the same way. Goldstein devotes **Chapter 6** to small oscillations and the
principal-axis transformation, and Griffiths' coupled-oscillator problem carries a footnote saying
plainly: *start with the normal-mode coordinates you would use to decouple the classical problem.* I
had not done that. Doing it explains the structure of my system exactly.

Rotate by 45°, which is a canonical transformation:
$$X_\pm=\frac{x_1\pm x_2}{\sqrt2},\qquad P_\pm=\frac{p_1\pm p_2}{\sqrt2}.$$

The Hamiltonian becomes

$$H=\frac{P_+^2}{2m_+}+\frac{P_-^2}{2m_-}+\tfrac12 m\omega^2\left(X_+^2+X_-^2\right)-2V_0\cos\!\frac{kX_+}{\sqrt2}\cos\!\frac{kX_-}{\sqrt2},
\qquad \frac{1}{m_\pm}=\frac1m\pm\lambda.$$

I checked this is **exact**, not an approximation — the two forms of `H` agree to **5.3e-15** (machine
precision) over 300 random phase-space points.

**Three things fall out of it.**

1. **The momentum coupling is not really a coupling.** It is removed entirely by the rotation; all it
   does is give the two modes *different effective masses*. The genuine coupling — the only term
   making this system non-integrable — is the **cosine cross-term**. Without the cosine, the problem
   separates into two independent oscillators and is exactly solvable.
2. **The mode frequencies are $\omega_\pm=\omega\sqrt{1\pm\lambda m}$.** Verified numerically to
   1e-3. At $\lambda=0.3$ they are 1.140 and 0.837.
3. **KAM's second condition becomes checkable.** My ratio is $\omega_+/\omega_-=1.363$ — not close to
   any low-order rational — consistent with the tori I actually see surviving.

**A hypothesis I tested and rejected.** Those frequency ratios hit exact low-order resonances at
particular couplings: $\lambda=0.6$ gives exactly **2:1** and $\lambda=0.8$ exactly **3:1**. Since
resonance is what breaks KAM, I guessed that was why $\lambda=0.8$ produced chaos. It is not — at
$\lambda=0.5$, which is *off* resonance (ratio 1.732), the Lyapunov exponent is 0.33, just as
chaotic. The explanation is simpler: at the deep well $V_0=8$ the cosine is no longer a *small*
perturbation, so KAM does not apply at all and the frequency condition is beside the point. The
resonance structure would only matter in the near-integrable regime. Worth revisiting at small $V_0$.

---

# PART 3 — The maths quantum mechanics needs

*Five ideas Part 4 leans on constantly. None is hard, but all five used to be assumed, which is what
made the quantum section read as a wall. Every one is tied to a line of the actual code.*

## 3.1 A vector is an ordered list of numbers

In school a vector is drawn as an arrow. That picture is fine, but the useful definition here is
duller: **a vector is a list of numbers, written in a fixed order, where the order carries meaning.**

```
(3, 4)        3 across and 4 up
(3, 4, 12)    3 across, 4 up, 12 forward
```

`(3, 4)` has **two components**, so it lives in a **two-dimensional** space. "Dimension" just counts
how many numbers you need to pin the thing down. Nothing stops the list being longer: 80 numbers is a
vector in 80-dimensional space. You cannot picture it and you do not need to — the algebra is
identical however long the list is.

**You have already used one.** In Component 3 each classical trajectory `A[i]` is 80 numbers in a
fixed order (40 values of φ, then 40 of n). That row *is* a vector in 80-dimensional space, and the
network's whole job is mapping one such vector to another.

**A basis is the set of reference directions the numbers are counted along.** The list `(3, 4)` is
meaningless until you say *3 of what*. The unspoken answer is usually "3 steps east, 4 steps north" —
those two reference directions are the **basis**, and the numbers are **coordinates**.

Change the basis and the same physical arrow gets a different list of numbers. Nothing about the
arrow changed, only the yardsticks. This does real work later: the *same* quantum state has one list
of numbers in the energy basis and a different list in the position basis, and choosing the
convenient basis is most of what makes a calculation easy.

A basis must **span** the space (every vector can be built from it — east and north are enough for a
flat map, east alone is not) and be **independent** (none of the directions is a combination of the
others, so there is exactly one way to write any vector).

## 3.2 Complex numbers exist so things can cancel by *phase*, not just by sign

A complex number is a pair of ordinary numbers glued together with the symbol `i`, defined by the one
rule `i² = −1`:

```
z = 3 + 4i          "3 real parts and 4 imaginary parts"
```

You add and multiply them like ordinary algebra, using `i² = −1` whenever it comes up. Two pieces of
vocabulary appear constantly:

- The **magnitude** `|z| = √(3² + 4²) = 5` — its size, always a real number ≥ 0.
- The **complex conjugate** `z* = 3 − 4i` — flip the sign of the imaginary part. Multiplying a number
  by its own conjugate always gives the magnitude squared, a plain real number: `z*z = |z|² = 25`.
  **That trick is how quantum mechanics turns complex amplitudes into real probabilities.**

**Why quantum mechanics needs them.** Ordinary probabilities only add up: two routes at 0.3 each give
0.6, and more is always more. But real quantum systems show *interference* — two possibilities can
combine to give **less** than either alone, or nothing at all. That requires quantities that can
point in different directions and cancel. A real number can only cancel one of opposite sign; a
complex number carries a direction (a **phase**) as well as a size, so two can partially cancel at
any angle. That extra freedom is exactly what produces the interference fringes in the superposition
Wigner movie (§4.12) — with real amplitudes those fringes could not exist.

*In the code, Python writes `i` as `j`: `1j` in `p_op = -1j * (a - adag) / np.sqrt(2)`.*

## 3.3 A matrix is a machine that turns one vector into another

A matrix is a grid of numbers. Its job is to **act on** a vector and give back another vector: feed
in a list, get out a list. That is all "operator" ever means in this project.

```
 ⎡0  1⎤   ⎡3⎤     ⎡4⎤
 ⎣1  0⎦ · ⎣4⎦  =  ⎣3⎦        this matrix swaps the two components
```

The rule for the output's first entry: walk along the matrix's first **row**, multiply each entry by
the matching entry of the vector, and add them up. Repeat per row.

Applying two matrices in a row is applying one machine and then the other — and **the order
matters**, because doing A then B is generally not the same as B then A. That single fact is where
the uncertainty principle comes from (§4.4).

## 3.4 Eigenvalues — the special directions a matrix leaves alone

For most input vectors a matrix changes both the direction and the length of what you feed it. But
for a few special vectors it only rescales them — the output points exactly the same way:

```
Â |v⟩ = λ |v⟩          "the machine left this one pointing the same way"
```

Such a `|v⟩` is an **eigenvector** of `Â`, and the number `λ` it got multiplied by is the
**eigenvalue**. ("Eigen" is German for "own" — these are the matrix's *own* characteristic
directions.)

**The physical content of quantum mechanics hangs on this.** The rule, which is a postulate rather
than something derived: *when you measure an observable, the only values you can ever get are the
eigenvalues of its operator*, and immediately afterwards the system is left in the matching
eigenvector. So the eigenvalues are the **menu of allowed outcomes**.

For the oscillator, the energy operator `Ĥ` has eigenvalues `Eₙ = ℏω(n+½)` — those discrete numbers
are the only energies you can ever measure. **That is exactly why energy is quantized:** it is the
eigenvalue list of `Ĥ`. When the code calls `H.eigenenergies()`, it is asking literally "which
numbers can this energy machine return?" That one line is the central quantum computation of the
project.

## 3.5 Probability and expectation value

Two words used constantly from §4.2 onward.

**A probability distribution** is a list of outcomes with a number attached to each, saying how
likely it is. The numbers are between 0 and 1 and they add to 1, because *some* outcome must happen.
For the oscillator's energy, the outcomes are the rungs `E₀, E₁, E₂, …` and the numbers come from the
state.

**An expectation value** is the **average result you would get from many repeated measurements**,
weighted by those probabilities:

```
⟨Â⟩ = (outcome₁ × its probability) + (outcome₂ × its probability) + …
```

It is written with angle brackets: `⟨x̂⟩`, `⟨p̂⟩`, `⟨Ĥ⟩`. Three things to keep straight:

- **It is an average over many measurements, not the result of one.** A single measurement returns
  one eigenvalue. `⟨x̂⟩` is where those results centre if you repeat the experiment.
- **It need not be an allowed outcome itself.** The average of a fair die is 3.5, which is not a face.
  Likewise `⟨Ĥ⟩` can sit between two energy rungs.
- **It is a plain real number**, so it can be plotted against time on an ordinary graph — which is
  exactly what `e_ops=[phi_op, n_op]` in `sesolve` computes, and what Component 3 uses as its
  targets. The entire ML dataset is a table of expectation values.

---

# PART 4 — Quantum Mechanics (Component 2)

**Aim:** compute the *quantum* version of the same oscillator — its allowed energies and how its
states evolve — both with exact formulas (the answer key) and with `qutip`. This produces the
*target* data the ML model learns to predict.

> **The big mental shift.** Classically the oscillator is a **point** at a definite `(x, p)`, moving
> on a definite ellipse. Quantum-mechanically `x` and `p` can never both be known exactly at once. So
> the point becomes a **fuzzy blob of probability**, and energy stops being a smooth dial — it comes
> only in **fixed steps**. Everything below unpacks those two changes.

| Task | What it produces | New idea |
|---|---|---|
| 1 | the energy spectrum | operators, eigenvalues, truncation |
| 2 | three evolving states + Wigner movies | the Schrödinger equation, quasi-probability |
| 3 | the real fluxonium qubit | a system with no exact answer to check against |

## 4.1 Hilbert space — where a quantum state lives

**Start from what you already have.** In Part 2 the complete state of the classical oscillator was a
**point** `(x, p)` in the plane. Two numbers and you know everything. That plane is **phase space**.

Quantum mechanics keeps the idea of "a space of all possible states" (§1.1) and changes what the
states *are*. That new space is **Hilbert space**. The name sounds forbidding; the object is not.

**The one-sentence version.** *Hilbert space is the space of all possible quantum states, where each
state is a vector whose coordinates are complex numbers telling you how much of each energy level the
state contains.* The rest of this section unpacks that sentence.

**What the coordinates actually are.** Start with the energy levels. The oscillator has a discrete
ladder of them — rung 0, rung 1, rung 2 (§4.7). Take those rungs as the **basis** (§3.1): rung 0 is
"east", rung 1 is "north", rung 2 a third direction. In bra-ket notation those basis directions are
`|0⟩, |1⟩, |2⟩, …`

A general state is a weighted blend of them, and blend weights are just coordinates:

```
|ψ⟩ = c₀|0⟩ + c₁|1⟩ + c₂|2⟩ + …     ⟷     the column of numbers  [c₀, c₁, c₂, …]
```

The left side is physics notation, the right side is the vector from §3.1. **They are the same
object.** Each `cₙ` is a complex number called an **amplitude**, answering "how much of rung `n` is
in this state?"

| state | meaning | as a column |
|---|---|---|
| `\|0⟩` | purely the ground state | `[1, 0, 0, 0, …]` |
| `\|1⟩` | purely the first excited state | `[0, 1, 0, 0, …]` |
| `(\|0⟩+\|1⟩)/√2` | an equal blend of the two | `[0.707, 0.707, 0, 0, …]` |

Those amplitudes are **not** probabilities — they are complex, and can be negative or imaginary.
Squaring the magnitude turns one into a probability (§3.2): `|cₙ|²` is the chance that measuring the
energy lands on rung `n`. For the blend above, `|0.707|² = 0.5` — fifty-fifty, as it should be. And
because *some* rung must come up, the squares always sum to 1. That is the whole content of the
normalization rule `⟨ψ|ψ⟩ = 1`, and it is what `.unit()` enforces in the code.

**Are quantum states discrete?** Two different things get mixed here; separate them:

- **The energy levels are discrete.** The allowed *energies* come in a list, `Eₙ = ℏω(n+½)`. You can
  have rung 0, rung 1, rung 2 — never rung 1.5. This is the "quantized" part.
- **The states themselves are continuous.** You can build infinitely many states by *blending* those
  discrete levels in any proportion, with any complex amounts. The amplitudes vary smoothly, so the
  set of possible states is continuous even though the energy *menu* is discrete.

Short version: **discrete menu of energies, continuous set of states built from that menu.** A
coherent state (§4.10) is a good example — a smooth blend of *all* the discrete levels at once.

**Why it needs infinitely many dimensions.** The oscillator has infinitely many rungs, so the column
of amplitudes is infinitely long and Hilbert space here is infinite-dimensional. This is bookkeeping,
not mysticism: one coordinate per rung, and there are infinitely many rungs.

**Side by side with what you already know:**

| | Classical (Component 1) | Quantum (Component 2) |
|---|---|---|
| the space | phase space | Hilbert space |
| a state is | a **point** `(x, p)` | a **vector** `\|ψ⟩` |
| how many numbers | 2 | one complex amplitude per energy rung |
| can states blend? | no — you are at one point or another | **yes** — superposition |
| what you can ask | "where is it, how fast" | "what is the probability of each outcome" |

The last row is the real difference. A classical point answers every question with certainty because
it *is* the answer. A quantum vector answers with probabilities, and the next section is the
machinery that extracts them.

## 4.2 Bras, inner products, and the Born rule

**What makes it "Hilbert" and not just any vector space.** One extra piece of equipment: a way to
multiply two vectors into a single number measuring **how much they overlap**. For ordinary arrows
that is the dot product. Here it is the **inner product**, written `⟨φ|ψ⟩`.

**The notation is a visual pun.** A state written forwards, `|ψ⟩`, is a **ket** — a column. The same
state written backwards, `⟨φ|`, is a **bra** — the column laid on its side into a row, with every
entry complex-conjugated (§3.2). Put a bra in front of a ket and the brackets close up: `⟨φ|ψ⟩`.
Bra + ket = "bracket".

**What a bra is for.** On its own it does nothing. Its job is to be placed in front of a ket, and the
question it always asks is: **"how much of *me* is contained in this state?"**

- `⟨0|ψ⟩` asks "how much ground state is in `|ψ⟩`?" → returns the amplitude `c₀`.
- `⟨1|ψ⟩` asks "how much of level 1 is in there?" → returns `c₁`.

So a bra is a *measuring question* and a ket is *the thing being asked about*.

**What the inner product means.** Mechanically it is the dot product: multiply matching entries, add
them up, get one complex number. Physically it measures alignment:

- `⟨φ|ψ⟩ = 0` — **orthogonal**. Completely distinct states, no overlap, like perpendicular arrows.
  Different energy rungs are all mutually orthogonal (`⟨m|n⟩ = 0` when `m ≠ n`), which is precisely
  what makes them usable as a basis.
- `|⟨φ|ψ⟩| = 1` — the same state, fully aligned.
- In between, `|⟨φ|ψ⟩|²` is a **probability**.

**The Born rule — and what the probability is *of*.** The probability is always of a **specific
measurement result**. In quantum mechanics you do not read the state off directly; you *measure an
observable* and get **one** of its allowed values (its eigenvalues, §3.4), with a probability set by
the state's amplitudes. The rule:

> **Born rule:** the probability of getting the outcome associated with `|φ⟩` is `|⟨φ|ψ⟩|²` — the
> squared overlap.

For the oscillator measuring **energy**: the possible outcomes are the rungs `E₀, E₁, E₂, …`, and the
probability of landing on rung `n` is `|⟨n|ψ⟩|² = |cₙ|²`. So if `|ψ⟩ = (|0⟩+|1⟩)/√2`, a single energy
measurement returns `E₀` half the time and `E₁` half the time. All the `|cₙ|²` add to 1, because some
outcome must happen.

**Superposition.** If `|A⟩` and `|B⟩` are valid states, so is any combination like `(|A⟩ + |B⟩)/√2`.
The system is genuinely "both at once" until measured — not secretly one of them with us being
ignorant. The interference fringes in §4.12 are the proof of the difference.

**Where you have already used all of this.**
```python
psi_super = (basis(N, 0) + basis(N, 1)).unit()
```
`basis(N, 0)` builds the column `[1, 0, 0, …]`, `basis(N, 1)` builds `[0, 1, 0, …]`, adding them
gives `[1, 1, 0, …]`, and `.unit()` rescales to `[0.707, 0.707, 0, …]` so the squares sum to 1.

## 4.3 Observables become operators

**In plain words.** Classically, position is just a number you read off. Quantum-mechanically you
cannot read `x` and `p` off the state at all; instead they become **operators** — machines (matrices,
§3.3) that act on the state and transform it into a new state.

**The math.**
- `x̂` = position operator, `p̂` = momentum operator. Hats mean "operator", not "number".
- The measurable values of an observable are the **eigenvalues** of its operator (§3.4).

**Why this is the core mechanism.** It is what makes quantum different from classical. Measurable
quantities do not take a continuum of values; they come in a discrete *allowed list*, and that list
is the eigenvalue list of the operator. Finding it for `Ĥ` is the central computation of Component 2.

## 4.4 The uncertainty principle (why the point becomes a blob)

**In plain words.** The single most important quantum fact for this project: position and momentum
cannot both be pinned down at once. The more precisely one is known, the fuzzier the other must be.
This is built into reality, not a limitation of instruments. It is why a quantum oscillator cannot
sit perfectly still at the bottom of the valley, and why the phase-space "point" must become a
finite-size "blob".

**The math.** Position and momentum operators **do not commute**:

`[x̂, p̂] = x̂ p̂ − p̂ x̂ = iℏ`

**Decode it.**
- `[Â, B̂] = ÂB̂ − B̂Â` is the **commutator** — it measures whether the order of two operations
  matters (§3.3). Zero means order is irrelevant, like ordinary numbers; nonzero means it matters.
- Here it is **not** zero — it equals `iℏ`. That nonzero result is the mathematical seed of the whole
  uncertainty principle.
- `ℏ` = the **reduced Planck constant** (`h/2π`), a tiny fundamental constant (~1.05×10⁻³⁴ J·s)
  setting the "size" of quantum effects. If `ℏ` were zero, quantum mechanics would collapse to
  classical mechanics.

**Why non-commuting means uncertain.** Two operators that do not commute **cannot share the same
eigenvectors**. Since a state with a definite value of an observable *is* an eigenvector of that
observable (§3.4), no single state can have a definite value of both at once. The consequence is
`Δx · Δp ≥ ℏ/2`: squeeze the position spread tiny and the momentum spread is forced to blow up.

**The picture.** Classically a state is a *point* `(x,p)` — both exactly known. Quantum-mechanically
the sharpest possible state is a little **blob** of area `~ℏ/2` in phase space, never a point. You
can squeeze the blob thin in `x` but then it stretches tall in `p`; its area cannot shrink below the
limit. That blob is exactly what the **Wigner function** (§4.12) draws.

It is not that the values are hidden from us — a state with both simultaneously sharp does not exist.

## 4.5 The quantum Hamiltonian

**In plain words.** Same energy idea as classical — kinetic plus potential — now built from operators
instead of numbers.

**The math.** `Ĥ = p̂²/(2m) + ½ m ω² x̂²`

**Decode it.** Identical in form to the classical `H(x,p)` from §2.4, with hats on `x` and `p`. The
allowed energies are the **eigenvalues** of `Ĥ`, and finding them is the heart of Task 1.

**Are we measuring the energy of the same thing as in Component 1?** Yes — and that sameness is the
entire point of using the oscillator as the test system. Both components describe **one and the same
physical object** and compute its **total energy** from the *same* Hamiltonian form. The difference
is only the rules for `x` and `p`:

| | Classical (Component 1) | Quantum (Component 2) |
|---|---|---|
| State | a point `(x, p)` in phase space | a vector `\|ψ⟩` in Hilbert space |
| `x`, `p` | ordinary numbers | operators (do not commute) |
| Energy | any value, continuous | discrete rungs `Eₙ = ℏω(n+½)` |
| Lowest energy | exactly 0 (sit still at the bottom) | `½ℏω` ≠ 0 (zero-point energy) |
| Phase-space picture | a point on an ellipse | a blob (Wigner) of area ≥ ℏ/2 |

Because it is literally the same system measured two ways, the two answers can be lined up and
checked against each other — which is the whole project.

## 4.6 Ladder operators — the clever trick

**In plain words.** Solving for the energies directly involves hard calculus. A slicker route defines
two helper operators that **step the system up or down** the energy ladder, one rung at a time. With
these, the energy structure follows from algebra instead of calculus.

**The math.**
- `â` = **annihilation** (lowering) operator — steps **down** one energy level.
- `â†` = **creation** (raising) operator — steps **up** one level (`†` is "dagger", the
  conjugate-transpose).
- Key relation: `[â, â†] = 1`.
- Position and momentum rebuild from them: `x̂ = √(ℏ/2mω)(â + â†)` and `p̂ = −i√(ℏmω/2)(â − â†)`.
- The Hamiltonian becomes simple: `Ĥ = ℏω(â†â + ½)`.
- `n̂ = â†â` is the **number operator** — it counts how many energy quanta the state has.

**What "adds one quantum of energy" means.** "A quantum of energy" is **one rung**, an amount `ℏω`.
The creation operator takes a state on rung `n` to rung `n+1`:

```
â†|n⟩ = √(n+1) |n+1⟩      (up one rung  → energy increases by ℏω)
â |n⟩ = √n     |n−1⟩      (down one rung → energy decreases by ℏω)
```

Because the rungs are evenly spaced by `ℏω`, moving up exactly one rung *adds exactly one packet* of
energy — that packet is "one quantum". The `√(n+1)` factor is bookkeeping that keeps states properly
normalized; the key idea is the rung change. In hardware language, one quantum is one photon in the
LC circuit (Part 12).

**Why there is a "ladder" at all.** The allowed energies are evenly spaced, separated by a constant
`ℏω`. Evenly spaced levels *look* like the rungs of a ladder, and `â`/`â†` move you down and up one
rung at a time. That regular structure is why physicists literally call them the ladder operators.

> **Notation warning — the three books do not agree, and the code follows two of them.** This
> tripped me up reading Griffiths §2.3.1 after writing the QuTiP code, so it is worth having in
> front of you:
>
> | | raising | lowering | source |
> |---|---|---|---|
> | Essler, QuTiP, this guide, the notebooks | `â†` ("a dagger") | `â` | eq. 230 |
> | **Griffiths §2.3.1** | **`â₊`** ("a plus") | **`â₋`** ("a minus") | eq. 2.62 |
>
> They are the *same two operators*. Griffiths' `â₊` **is** `â†`, and his `â₋` **is** `â`. So when
> Griffiths writes `Ĥ = ℏω(â₊â₋ + ½)` (his eq. 2.58) that is character-for-character the
> `Ĥ = ℏω(â†â + ½)` above, and the `H_ladder` line in the notebook. He also numbers the two results
> this guide leans on as **eq. 2.61** (`E₀ = ½ℏω`) and **eq. 2.62** (`Eₙ = (n+½)ℏω`).

**Essler's notation (the length scale ℓ).** Essler defines the *same* operators (his eq. 230),
packaging the prefactor into a **characteristic length** `ℓ = √(ℏ/2mω)` (his eq. 258), so
`x̂ = ℓ(â + â†)` — the form his eq. 276 uses. This `ℓ`
is the natural "size" of the quantum oscillator — roughly the width of its ground-state blob. In
natural units it is `1/√2`, which is the `1/np.sqrt(2)` in the code.

**Why it matters.** This is the structure `qutip` uses internally. `qutip.destroy(N)` builds `â`;
everything else (`â†`, `x̂`, `p̂`, `Ĥ`) is assembled from it. Understanding the ladder is
understanding what `qutip` does.

## 4.7 Quantized energy and zero-point energy

**In plain words.** Because the ladder only moves in whole steps, the energy is **quantized** — only
specific, evenly spaced values are allowed. The lowest rung is **not zero**: even in its calmest
state the quantum oscillator still jitters with a minimum "zero-point" energy. It must — sitting
perfectly still would mean knowing both position and momentum exactly, which §4.4 forbids.

**The math.** `Eₙ = ℏω (n + ½)`,  for `n = 0, 1, 2, 3, …`

**Decode it.**
- `n` is the level index: `n=0` is the ground state, `n=1` the first excited, and so on.
- The levels are **evenly spaced**, each `ℏω` apart.
- `n = 0` gives `E₀ = ½ℏω ≠ 0` — the **zero-point energy**, a pure quantum effect with no classical
  counterpart (a classical oscillator at rest has exactly zero energy).
- **This formula is the answer key.** In Task 1 the eigenvalues are computed numerically and overlaid
  on this exact line; they must match for low `n`. Component 2 achieves 5.3e-15 over the lowest 15
  of `N=30`.

*Essler:* the spectrum is eq. 246; the zero-point energy eq. 244; the ladder actions eqs. 250–251.
That the *average* position oscillates at frequency ω is his §6.3. Precisely: because `x̂` connects
only *adjacent* levels, the only Bohr frequency it can produce is `(Eₙ₊₁−Eₙ)/ℏ = ω`. So `⟨x̂⟩(t)`
either oscillates at exactly ω or is identically zero — never anything else. It vanishes for any
state with no adjacent-level coherence: an energy eigenstate `|n⟩`, and also e.g. `(|0⟩+|3⟩)/√2`,
which I checked numerically.

## 4.8 The Fock basis, and building it in QuTiP

**The Fock basis.** "Fock states" are the rungs themselves: `|0⟩, |1⟩, |2⟩, …`, each a state of
*definite energy* (`|n⟩` has exactly `n` quanta). Using them as the reference directions for Hilbert
space (§4.1) is called working **in the Fock basis** — also called the number basis, since `n` counts
quanta. Every other state is written as a blend of these. It is the natural coordinate system for the
oscillator because `Ĥ` is simplest there: diagonal.

**Truncation: infinite → finite.** The true oscillator has infinitely many levels, but a computer
needs finite matrices. So the space is **truncated**: keep the lowest `N` levels and represent every
operator as an `N×N` matrix. As long as states stay well below the top rung, this is harmless.

- `a = qutip.destroy(N)` builds `â` as an `N×N` matrix (`N = 30` in Component 2).
- `a.dag()` gives `â†`; from these come `x̂`, `p̂` and `Ĥ`.
- `H.eigenenergies()` returns the numerical eigenvalues, compared against `Eₙ = ℏω(n+½)`.

**Graphing a matrix.** In the Fock basis an operator is a grid of numbers — the entry in row `m`,
column `n` is `⟨m|Â|n⟩`. To "graph" it you draw the grid as an image: one coloured cell per entry.
This makes the *structure* visible at a glance. In `fig_c2_operator_matrices.png`, `Ĥ` is **diagonal**
(each level has one definite energy) while `x̂` and `p̂` have entries only just off the diagonal —
they connect a level only to its immediate neighbours. **That off-diagonal stripe is the ladder,
drawn.**

Only the lowest **⌈(N−1)/2⌉** levels are trustworthy — 5 of 10, 15 of 30, 25 of 50 — which is why the
notebook checks convergence by rebuilding at `N = 10, 30, 50` and comparing.

**And the reason is sharper than "high levels drift", which is worth knowing because the figure looks
odd until you see it.** Built from truncated operators, `Ĥ = (ââ† + â†â)/2` is *exactly diagonal*. But
`â†` annihilates the top state, so `ââ† = diag(1, 2, …, N−1, 0)` — that last entry should be `N`. The
result is **one** spurious eigenvalue at `(N−1)/2` instead of the correct `N−½`. Since eigenvalues come
back **sorted**, that single low value lands mid-spectrum, one level appears twice, and every level above
it is shifted down exactly one rung. So the error plot is a flat plateau at **exactly 1.000**, not a
growing curve: those high eigenvalues are not wrong *values*, they are correct values wearing the wrong
index, and the true top level is simply missing.

## 4.9 The Schrödinger equation — how quantum states move in time

**In plain words.** The quantum analogue of Hamilton's equations. It gives how a state changes moment
to moment, and like Hamilton's equations it is first-order in time, so a computer can march it
forward step by step.

**The math.** `iℏ d|ψ⟩/dt = Ĥ |ψ(t)⟩`

**Decode it.** The left side is how the state changes in time (§1.5), scaled by `iℏ`. The right side
is the Hamiltonian acting on the current state. In words: *the energy operator drives the evolution
of the state* — exactly the pattern from §1.2. The `qutip` function `sesolve` does this numerically,
and is the quantum twin of `solve_ivp`.

## 4.10 The three states simulated, and what each shows

Task 2 evolves three starting states, each highlighting a different facet of quantumness.

**1. Energy eigenstate (Fock state) `|n⟩`.** A state of one exact, definite energy. It is
**stationary** — its measurable properties do not change in time, and its average position and
momentum are zero for all time. The "purely quantum, nothing classical about it" case.

**2. Superposition `(|0⟩ + |1⟩)/√2`.** The system is genuinely in *two* energy levels at once.
Because the two levels "tick" at different rates they interfere, and the **average position
oscillates back and forth** — like a classical pendulum emerging from quantum pieces. Interference
made visible.

**3. Coherent state `|α⟩` (a displaced Gaussian blob).** The **most classical-like** quantum state. A
compact blob that orbits the phase-space origin, holding its shape and tracing the classical orbit
**exactly** — for the harmonic oscillator, not merely approximately (§4.11). The bridge between the
quantum and classical pictures, and the most important state for this project: it is what
`qt.coherent(DIM, ...)` builds for every one of Component 3's 300 samples.
*Decode `α`:* a complex number setting where the blob sits and how big its orbit is.

*Essler:* coherent states are his **Aside 4** (eqs. 281–289) — defined as eigenstates of the
annihilation operator, `â|α⟩=α|α⟩`, with a Gaussian wavefunction centred at `2ℓα`, which in natural
units is `√2·Re(α)`, exactly where the code places the blob.

## 4.11 Expectation values and Ehrenfest's theorem

**In plain words.** An **expectation value** (§3.5) is the average result of many measurements,
written `⟨x̂⟩(t)`, `⟨p̂⟩(t)`. Plotting `⟨p̂⟩` against `⟨x̂⟩` over time gives a phase-space path lying
directly on top of the classical circle from Part 2. For the coherent state in the harmonic
oscillator the two agree **exactly** — this is *Ehrenfest's theorem*.

**What the theorem actually says — and the condition everyone drops.** The usual one-liner is
"quantum averages obey classical equations of motion". That is not quite it. Ehrenfest gives
(Griffiths eq. 1.38):

$$\frac{d\langle \hat x\rangle}{dt}=\frac{\langle \hat p\rangle}{m},\qquad \frac{d\langle \hat p\rangle}{dt}=\Big\langle -\frac{\partial V}{\partial x}\Big\rangle.$$

The second equation has the average of the **force**, `⟨−∂V/∂x⟩`. The *classical* equation would have
the force **evaluated at the average position**, `−∂V/∂x(⟨x⟩)`. Those two are the same thing only
when `∂V/∂x` is **linear in x** — which is to say, only for a harmonic potential.

- **Harmonic:** the force is `−mω²x`, perfectly linear, so `⟨−mω²x̂⟩ = −mω²⟨x̂⟩`. The averages follow
  the classical path *exactly*, for any state and any packet width. That is why Task 2 agrees so well.
- **Anharmonic (the fluxonium):** the force is `−(E_Lφ + E_J sin(φ+φ_ext))`, and `⟨sin φ̂⟩ ≠ sin⟨φ̂⟩`.
  The averages now obey *no* classical equation. A quick check with a coherent state in
  `V = x²/2 + 0.1x⁴` gives `⟨−dV/dx⟩ = −7.21` against `−dV/dx(⟨x⟩) = −5.94` — a 21% discrepancy from
  one quartic term.

**The intuition, in one line.** A quantum packet is spread out, so it samples the potential over a
*range* rather than at a point. If the force is a straight line, the too-strong pull on one side of
the packet exactly cancels the too-weak pull on the other, and the average force equals the force at
the centre — the errors cancel. If the force curves, they do not cancel, and the packet feels
something genuinely different from what a point particle at its centre would feel.

**Measured, for a coherent state at α = 1.5:**

| potential | `⟨−dV/dx⟩` | `−dV/dx(⟨x⟩)` | disagreement |
|---|---|---|---|
| `V = x²/2` (harmonic) | −2.1213 | −2.1213 | **0.0%** |
| `V = x²/2 + 0.1x⁴` | −7.2125 | −5.9397 | **21.4%** |

One quartic term is enough for a 21% error. In the harmonic case the quantum average tracks the exact
classical path to **8×10⁻⁷** over a full period.

> **Why the condition has to break for this project to exist.** Follow it through: if Ehrenfest's
> condition held, the quantum averages would follow the classical path *exactly*, so `B = A`, so the
> map Component 3 is learning would be the **identity function**, copy-classical would score zero
> error, and there would be nothing to predict. The harmonic oscillator of Task 2 is exactly that
> null case — which is why it belongs in the deck as the baseline the fluxonium then breaks. **The
> project needs a system where classical and quantum genuinely differ, because the difference is the
> thing being predicted.**
>
> And the copy-classical baseline in §5.5 is therefore not just a control: it is a **direct
> measurement of how badly Ehrenfest's condition fails.** Its 2.4× growth toward the barrier (§5.7)
> is the condition breaking harder as the potential curves more — a property of the physics, not of
> any model.

**This is the whole explanation for the Component 2 Task 3 result, and the reason Component 3 has
anything to learn.** The fluxonium packet does not lag the classical trajectory because of numerical
error or vague "packet spreading" — it lags because Ehrenfest's theorem *stops applying* the moment
the potential is anharmonic, and the size of the failure grows with the anharmonicity and the packet
width. Since `φ_zpf = 1.41` is comparable to the width of the well, the packet samples a lot of
curvature and the failure is large. **The MLP in Component 3 is being asked to model exactly the term
Ehrenfest throws away.** That is the single most useful sentence in this guide for explaining the
project out loud.

**The catch.** Collapsing the whole fuzzy blob to a single average point **throws away** most of the
quantum information — the spread, the uncertainty, the interference. The average looks classical
precisely *because* averaging hides the quantum richness. Keeping that richness requires the Wigner
function.

*Essler:* Ehrenfest is §4.1; the `⟨x̂⟩(t)` oscillation result is §6.3, using the position matrix
element eq. 276 — precisely the off-diagonal pattern seen in the `x̂` matrix image (§4.8).

## 4.12 The Wigner function — the quantum picture in phase space

**In plain words.** The centrepiece of Component 2 and the bridge to the ML work. The uncertainty
principle forbids an honest joint probability for exact `(x, p)` — you cannot have a probability
distribution over something that never has definite values. The Wigner function `W(x, p)` is the
closest legal substitute: a **quasi-probability** map over the same `(x, p)` plane used classically.
It lets a quantum state be drawn in phase space and compared directly to the classical ellipse.

**What "quasi" is doing in that word.** A real probability distribution (§3.5) must be non-negative
everywhere — an outcome cannot happen minus-twenty percent of the time. The Wigner function satisfies
almost every other requirement of a probability distribution (it is real, it integrates to 1, and
summing it along one axis gives the correct honest probability distribution for the other variable),
but it **can go negative**. That is the one rule it breaks, and it breaks it on purpose.

**So wherever `W(x,p) < 0`, the state has no classical explanation.** Negativity is the fingerprint of
"genuinely quantum" — there is no way to reproduce that region with any classical statistical picture.
This is why negative regions are the part a classically-fed ML model should struggle most to predict.

> **Note on sources.** The Wigner function is **not** in Essler, and **not** in Griffiths. Essler
> compares quantum and classical oscillators using the *position* probability density `|ψₙ(x)|²`
> (his §6.4). The Wigner representation used here comes from the **project handout** and QuTiP's
> `wigner` function. Both are valid windows on the same physics; the Wigner picture is used because
> it lives in the same `(x,p)` plane as the classical data, which is what Component 3 needs.

**What each state looks like:**
- **Coherent state:** a single positive Gaussian bump, offset from the origin. **No negative
  regions** → the most classical state. It orbits holding its shape.
- **Fock state `|n⟩`:** concentric rings. Going outward the sign flips `n` times, and the centre
  alternates as `W(0,0) ∝ (−1)ⁿ` — so `|1⟩` has a negative crater in the middle, `|2⟩` is positive at
  the middle with a negative ring around it. (The count of *negative regions* is therefore ⌈n/2⌉, not
  `n` — I had that wrong at first.) Strongly non-classical either way.
- **Superposition:** two bumps plus a stripey pattern of **alternating positive/negative interference
  fringes** between them — proof of a true superposition, not a random mixture. Those fringes are
  what §3.2's complex amplitudes make possible.

**A special property of the harmonic oscillator (checked numerically).** Its Wigner function evolves
in time by simply **rotating rigidly** around the origin. I verified this: evolving a lumpy
asymmetric state for a quarter period and rotating the initial Wigner function by 90° give the *same
array to numerical precision*, and after a full period the state returns to itself to 1e-6. The
rotation exactly mirrors the classical flow around the ellipse, with no distortion. This is special
to the quadratic potential — most systems get messy — and is another reason the oscillator is the
ideal teaching system.

**What Task 2 does:** use `sesolve` to evolve each state, `qutip.wigner` to compute `W(x,p)` on a
grid, plot snapshots, and animate movies with a **fixed colour scale** (so negative regions stay
comparable between frames), using a diverging colormap so positive and negative are visually
distinct.

## 4.13 Task 3 — the fluxonium qubit

> Tasks 1–2 are the textbook oscillator, where every number has an exact formula to check against.
> Task 3 spends that confidence on a real superconducting qubit, which has no closed-form answer.

**In plain words.** The **fluxonium** is a real superconducting qubit: a Josephson junction shunted by
a large inductor. Its Hamiltonian,
$$\hat H = 4E_C\,\hat n^2 + \tfrac12 E_L\hat\varphi^2 - E_J\cos(\hat\varphi+\varphi_{ext}),$$
is the exact quantum version of the classical cosine oscillator from §2.9. §1.3 explains what each
energy physically is, and why `φ` and `n` behave like position and momentum despite being a magnetic
phase and a count of Cooper pairs.

**Which coordinate — the one trap I fell into.** `scqubits` writes the potential as
$$U(\varphi)=\tfrac12 E_L\varphi^2 - E_J\cos(\varphi+\varphi_{ext}),$$
with the *inductive* term centred on $\varphi=0$. At half flux that puts the two wells at
$\varphi\approx\pm2.85$ and makes **$\varphi=0$ the top of the barrier**. The same physics can be
written $\tfrac12 E_L(\varphi-\varphi_{ext})^2 - E_J\cos\varphi$, which moves the wells to $0.29$ and
$5.99$ — but that is a *different coordinate*, shifted by $\varphi_{ext}$. Use one form for the
classical trajectory and let `scqubits` use the other for the quantum state, and the two are half a
flux quantum apart, making every comparison between them meaningless. **Rule: always take the
potential from `fluxonium.potential(...)` and integrate the classical equations in that same
$\varphi$.** Fixing this improved the Component 3 validation error about ninefold.

**A caveat on "quantum twin".** At **zero** flux the potential is exactly the cosine oscillator of
§2.9 with $V_0=E_J$. At **half** flux the cosine flips sign ($\cos(\varphi+\pi)=-\cos\varphi$), so
the fluxonium becomes a **double well**, where §2.9's oscillator is a single well. The two are the
same *family*, not the same system.

**The double well and tunneling.** At the half-flux "sweet spot" the potential is a symmetric double
well. The two lowest states form a near-degenerate pair — one symmetric, one antisymmetric across
the barrier — and their tiny splitting is the signature of **quantum tunneling** between the wells,
something with no classical analogue at all. Measured here: a doublet at 0.134 `E_C` under a barrier
of 7.76 `E_C`. Both are *differences*, which is why they are physical (§1.4).

**Wave packets.** We build a Gaussian wave packet (a coherent state, §4.10) localized at a phase
$\varphi_0$ and evolve it. Comparing its averages to the classical trajectory shows where the two
agree — near a well bottom, where the potential is closest to harmonic — and where they diverge, up
the wall and at the barrier.

**Why they diverge — the precise reason.** Not "the packet spreads", which is vague. Ehrenfest
(§4.11) gives $d\langle\hat n\rangle/dt=\langle-\partial U/\partial\varphi\rangle$, and for this
potential $\langle\sin\hat\varphi\rangle\neq\sin\langle\hat\varphi\rangle$. The averages obey no
classical equation of motion at all; the gap is the difference between those two quantities, and it
grows with the anharmonicity and with how much curvature the packet samples. With
$\varphi_{zpf}=1.41$ against a well only a few radians wide, the packet samples a great deal of
curvature, so the gap is large everywhere in this parameter regime — which is exactly what Component
3 measures (RMS 1.07 rad).

---

# PART 5 — Component 3: the neural network, in plain words

Components 1 and 2 build the data; Component 3 builds the **model** that learns from it. §0.1
explained what machine learning is in general; this part explains the specific model, and what it
actually achieved.

## 5.1 What kind of model — a multilayer perceptron (MLP)

**In plain words.** An MLP is the simplest kind of neural network: a stack of layers, where each
layer multiplies its input by a table of adjustable numbers, adds an offset, then bends the result
through a simple non-linear kink. Stacking these lets the network turn straight-line relationships
into flexible curves, so it can approximate almost any input→output map given enough examples.

**The pieces:**
- **Layer / `Linear`.** One "multiply by weights and add a bias" step: `output = W·input + b`. The
  multiplication is exactly the matrix-acting-on-a-vector of §3.3.
- **ReLU** (*rectified linear unit*). The non-linear kink between layers: keep positive values, set
  negative ones to zero. Without a non-linearity, stacking layers would collapse back into a single
  straight line — ReLU is what lets the network bend.
- **Hidden layer.** Any layer between input and output. This task uses **two**, each 128 wide.
- **Weights (parameters).** All the `W`s and `b`s together — the knobs training turns.

The network is `A → hidden (ReLU) → hidden (ReLU) → B̂`.

## 5.2 What it is predicting — regression, not classification

There are two flavours of supervised learning: *classification* (pick a category) and **regression**
(predict continuous numbers). This is regression. The input `A` is a whole classical trajectory
written as `2·N_t = 80` numbers, and the target `B` is the matching quantum trajectory of expectation
values (§3.5), also 80 numbers. The network reads one vector and predicts another — a
*vector-to-vector* map `f(A) ≈ B`.

**And what those 80 numbers physically are:** 40 values of `⟨φ̂⟩(t)` followed by 40 of `⟨n̂⟩(t)` —
the average magnetic phase and average Cooper-pair count at 40 instants (§1.3).

## 5.3 How it learns — loss, optimizer, epochs, batches

Learning is "guess, measure how wrong, nudge the weights to be less wrong, repeat."

- **Loss — MSE (mean squared error).** The score of wrongness: subtract truth from prediction, square,
  average. Zero is perfect.
- **Optimizer — Adam.** The rule deciding how to nudge each weight. The **learning rate** sets how
  big each nudge is (`1e-3` here).
- **Epoch.** One full pass through all the training examples.
- **Mini-batch.** The data is fed in small groups (32 at a time), each giving one weight update.
  Faster, and better for learning, than using all 240 rows at once.

**Standardizing.** Inputs and targets are shifted and rescaled to roughly zero mean and unit spread
before training, purely so the optimizer converges smoothly. Predictions are converted back to
physical units for reporting. The statistics are computed from the **training rows only** — using all
the data would leak information about the validation set into the preparation.

**Were those settings the right ones?** The handout asks for the widths, learning rate and batch size
to be explored rather than assumed, so they were: widths {64, 128, 256} × learning rate
{3e-4, 1e-3, 3e-3}, then batch size {16, 32, 64} at the winner. Three things came out of it:

- **Learning rate dominates.** At 3e-3 every width is worse and training destabilizes (the best epoch
  collapses from ~650 to 122 at width 256 — the optimizer is bouncing). At 3e-4 the runs are still
  improving when the sweep's epoch ceiling hits, so those are under-trained rather than bad.
- **Width barely matters.** That is what a problem which is *not capacity-limited* looks like — no
  surprise when linear regression alone already reaches 0.026 rad.
- **The configuration already in use (128 wide, lr 1e-3, batch 32) came out best.** The useful part
  is not that it changed — it didn't — but that it is now a measurement rather than a default.

The whole grid spans only 2.5×, against a ~12% split-to-split scatter (§5.7), so the broad shape is
real while neighbouring cells are not meaningfully different.

## 5.4 How we know it actually learned — the split, and early stopping

**The train/validation split.** 80% training / 20% validation. The network only *learns* from the
training 80%; the validation 20% is held back as an honesty check. If the training loss keeps
dropping but the validation loss starts *rising*, the model is **overfitting** — memorizing the
training examples instead of learning the general rule.

**A gap between the two curves is not by itself a problem.** The training loss is *always* lower,
because those are the rows the network was fitted on. The only question is whether the **validation**
curve is still going down. While it is, keep training.

**Early stopping.** The epoch where validation bottoms out is the last epoch that bought any real
generalization; training past it only tightens the fit to the training rows. Stopping there is
**early stopping**, and it replaces the arbitrary question "how many epochs?" with a measurement.

**This mattered a lot here.** The first version of the notebook ran a fixed 150 epochs — and the
validation loss was still clearly falling at that point, so the reported number described an
**under-trained** model rather than the model the data could support:

| | fixed 150 epochs | early stopping |
|---|---|---|
| best epoch | 150 (still falling) | **1610** |
| validation MSE (standardized) | 9.34e-4 | **1.47e-4** — 6.4× better |
| train/validation gap | 1.7× | 4.5× |

The wider gap is the expected trade: the network now fits the training set much more closely, and the
validation loss confirms most of that extra fit still generalizes.

**One subtlety worth being able to say out loud.** The stopping epoch was chosen by looking at the
validation set, so that set has now been used to make a decision and is no longer completely
untouched. The honest name for 1.47e-4 is "best validation score", not "test score". A three-way
train/validation/test split would remove the caveat at the cost of training on fewer samples.

## 5.5 Making the number mean something — the baselines

**A loss number alone is not a result.** "Validation MSE 9.3e-4" sounds small, but small compared to
*what*? A number becomes a result only when something else is measured the same way on the same data.
So three simpler methods are scored on the same 60 held-out trajectories, in the same units — RMS
error in `⟨φ̂⟩`, in radians, which is the typical size of the miss at a typical time point.

| model | what it is | RMS `⟨φ̂⟩` error (rad) | vs. copy |
|---|---|---|---|
| **copy-classical** (`B̂ = A`) | hand back the classical input unchanged | 1.067 | — |
| **k-nearest-neighbours** (k=1) | look up the most similar training trajectory | 0.077 | 14× |
| **linear regression** | the best possible *straight-line* map, solved exactly | 0.026 | 41× |
| **MLP** (early-stopped) | the neural network | **0.0057** | **186×** |

The MLP beats all three, so the result is meaningful. But reading down the column says more than the
winner alone:

- **Copy-classical is the floor, and it has physical meaning.** Its error *is* the size of the
  quantum correction — literally the term Ehrenfest discards (§4.11). Beating it 186× means the
  network really is reconstructing that correction rather than passing the classical trajectory
  through. Its 1.067 rad also matches the ≈1.02 rad measured independently, so the bar was the
  expected one.
- **Linear regression is the surprise, and the honest comparison.** A plain least-squares fit with no
  training loop reaches 0.026 rad. That makes sense from the physics: trajectories starting inside
  one well stay close to harmonic, and the *harmonic* classical→quantum map really is linear
  (§4.11 — for a harmonic potential Ehrenfest is exact). So the network's real job is the
  **nonlinear remainder**, and the fair claim is that it improves on linear regression by **4.5×**
  — *on RMS*.

  **Why that qualifier is not pedantry.** RMS squares the errors before averaging them, so one bad
  case pulls it a long way above the typical case. Plotting every held-out trajectory separately
  shows the straight-line fit's RMS sitting **3.6× above its own median**, while the network's sits
  only **1.3×** above. On a *typical* trajectory the network is **1.7×** better; on the *worst* it is
  **6.3×** better. Two models can share an RMS and behave completely differently, and for deciding
  whether to trust one, that difference is the whole story.
- **k-NN being worst of the three learned methods says something too.** Pure interpolation between
  240 stored examples is not enough, and it gets *worse* as `k` grows. The map is smooth and worth
  fitting rather than looking up, and the MLP is not merely memorizing training rows.

## 5.6 Where does the map fail? — the physical axis, and a null result

An average error says the model works *on average*. It does not say **where** — and "where" is the
project's actual scientific question (§0).

**The axis to ask it on.** How far each trajectory *started* from the bottom of the well,
`|φ₀ − φ_min|` with `φ_min ≈ 2.85`. The physics predicts a rise:

- **Near the minimum** the potential is nearly a parabola, so Ehrenfest is nearly exact (§4.11),
  classical and quantum agree, and the map is nearly the identity.
- **Far from the minimum** the cosine bends the potential away from a parabola, the force stops being
  linear, the packet distorts, and the quantum trajectory peels away from the classical one.

**What was measured.** The error is essentially **flat** for every learned model. Tested with
Spearman's rank correlation — which gives a number `ρ` for how steadily error climbs with distance,
and a p-value for whether that climb could be noise:

| model | ρ | p | verdict |
|---|---|---|---|
| copy-classical | +0.254 | 0.051 | not significant (marginal) |
| linear regression | −0.059 | 0.654 | not significant |
| k-NN | +0.077 | 0.559 | not significant |
| MLP | +0.077 | 0.559 | not significant |

**So the honest reading is not "the map is robust everywhere" but "this dataset does not reach far
enough to find the failure point".** The barrier top sits at `φ = 0`, which is 2.85 rad from the
minimum; sampling stops at 1.00 rad — about a third of the way. The breakdown region was never in the
data.

**The one trend that is nearly significant belongs to the physics, not the model.** Copy-classical —
which measures the *size of the quantum correction itself* — drifts from 0.95 to 1.16 rad. The
correction is growing with distance exactly as Ehrenfest's argument predicts. The network is simply
still able to keep up with it.

**Why this is written up as a result rather than quietly fixed.** The first draft of that figure was
titled "prediction error grows with distance from the well bottom", which is what the physics
predicts and what the eye sees in a noisy plot. The measurement does not support it. This is the same
mistake as the chaos claim in §2.10, caught the same way — by testing the trend instead of reading
it off a picture. **A figure is a picture, not a measurement.**

## 5.7 Widening the window — the breakdown, found

§5.6 named the experiment it needed, and §(g) of the notebook runs it. Two things were wrong with the
narrow run, and both are fixed by a second, **separate** dataset (so every number in §5.5–5.6 still
stands):

1. **Coverage.** `φ₀` is now drawn across the whole range from the **barrier top to the well bottom**,
   `φ₀ ∈ [0, φ_min]`, so the axis spans the full 0 → 2.85 rad rather than 0 → 1.0.
2. **A clean axis.** `|φ₀ − φ_min|` **conflated two different regimes**: a point 0.8 rad from the
   minimum could be heading toward the barrier (`φ₀ = 2.05`) *or* climbing the harmonic outer wall
   (`φ₀ = 3.65`). One approaches a tunneling barrier, the other a parabola. Averaging them together
   blurs exactly the signal being looked for. Sampling one-sided makes the axis monotone: **distance
   toward the barrier**, `φ_min − φ₀`.

**The trend appears, and it is significant.**

| model | error at the well bottom | at the barrier | growth | ρ | p |
|---|---|---|---|---|---|
| copy-classical | 1.040 | 2.483 | 2.4× | +0.862 | 8.5e-19 |
| linear regression | 0.079 | 0.140 | 1.8× | +0.285 | 0.027 |
| k-NN | 0.085 | 0.152 | 1.8× | +0.229 | 0.079 |
| **MLP** | **0.0071** | **0.0372** | **5.2×** | **+0.399** | **0.0016** |

**So §5.6's null was a sampling limitation, not a property of the map.** Once the window reaches the
barrier, the rise the physics predicts is measurable — and the reason is exactly §4.11: near the well
bottom the potential is nearly harmonic, Ehrenfest nearly holds, and the classical trajectory nearly
*is* the quantum one. Approach the barrier and the cosine's curvature takes over,
`⟨sin φ̂⟩ ≠ sin⟨φ̂⟩`, and the gap the network must model grows.

**Two things worth noticing in that table.**

- **Copy-classical grows 2.4× with ρ = +0.86.** That is not a statement about any model — it is the
  **size of the quantum correction itself**, growing with proximity to the barrier. This is the
  clearest direct measurement in the project of *where* classical and quantum part company.
- **The MLP degrades fastest in relative terms (5.2×), while staying far the most accurate.** Its
  advantage is largest in the easy near-harmonic regime and shrinks as the physics gets hard. That is
  the honest shape of the result: the network has not abolished the breakdown, it has pushed it down
  in magnitude.

**Two caveats that belong with the numbers.**

- **The truncation was re-justified, not assumed.** These packets sit higher in the potential than the
  narrow run's, so `cutoff=80` was re-checked against `cutoff=110` across the full window: they agree
  to **8.2e-7 rad**. Had that failed, every number above would have been an artifact of the basis size.
- **How much is split noise?** Running the narrow dataset through the same function with a different
  random split moves the MLP number from 0.0057 to 0.0050 — about **12%**. So a difference has to
  clear ~12% before it means anything. The 3.8× narrow→wide degradation clears it comfortably; small
  differences between the three baselines do not.

**What is still open.** The wide run samples *starting points* out to the barrier, but every packet
is still launched inside or on the edge of the double well at one fixed parameter set. The breakdown
has been located along one axis; mapping it across `E_J/E_C`, `E_L/E_C` and flux is the next question,
and it is the one the *Science* 2022 generalization result speaks to (`Research_ClassicalToQuantum_ML.md` §2).

## 5.8 Why this matters

This is where the project's central question finally gets tested: *how far can cheap classical
information predict expensive quantum behaviour, and where does it break down?* Both halves now have
a quantitative answer: a long way — 186× better than copying the classical trajectory, 4.5× better
than a straight-line fit — and the breakdown is at the barrier, where the error climbs 5.2× and the
quantum correction itself climbs 2.4×.

For the machine-learning research context, see `reference/Research_ClassicalToQuantum_ML.md`.

---

### Why "the model is accurate" and "classical differs from quantum" are both true

This trips people up, and it tripped up the group meeting, so it is worth stating carefully.

Three different curves get drawn in this project, and they are **not** interchangeable:

| symbol | what it is | where it comes from |
|---|---|---|
| `A` | the **classical** trajectory | solving Newton's equations for the matched oscillator |
| `B` | the **quantum** trajectory, $\langle\hat\varphi\rangle(t)$ and $\langle\hat n\rangle(t)$ | solving the **Schrödinger equation** |
| $\hat B$ | the network's **prediction** of `B` | the trained MLP, given `A` |

`B` is the truth. It is the expensive calculation the project is trying to avoid repeating, and it
never involves the network — which is exactly why the network's score against it means anything.

Now the two statements that sound contradictory:

- **"Classical and quantum disagree."** That is the distance from `A` to `B`, and it is **1.067 rad**
  — large, obvious, and the whole reason the project exists. Component 2's fluxonium figures are
  pictures of this gap.
- **"The model is accurate."** That is the distance from $\hat B$ to `B`, and it is **0.0057 rad**
  — 186 times smaller. Component 3's prediction figure is a picture of *that* gap.

Both are measurements of the same truth `B`, against two different things. There is no contradiction,
because they were never measuring the same distance.

**The check that makes this concrete.** Ask what would happen if the network simply passed its input
through — if it output `A` and called it a prediction. Then its error would be exactly the first
number, 1.067 rad. That is what the `copy-classical` baseline is, and it is why the baseline is not
bookkeeping: it is the proof that the network is doing something other than copying. Scoring 0.0057
instead of 1.067 is the entire result.

**And the reason the accurate figure looks *perfect* rather than merely good.** 0.0057 rad against an
orbit nearly 2 rad across is under half a percent — thinner than the line used to draw it. An error
can be real, structured, and still invisible at the scale of the physics. That is why the notebook
plots the residual separately on an axis 186× finer: *a gap you cannot see is indistinguishable from
a gap that is not there*, and telling those two apart is the whole question.

---

# PART 6 — How it all connects

The full arc:

- **Component 1 (classical)** gives the cheap, easy-to-compute side: energy contours and trajectories
  in phase space. These become the **inputs**.
- **Component 2 (quantum)** gives the expensive side: energy spectra, state dynamics, and Wigner
  functions — which conveniently live in the *same* `(x, p)` picture as the classical data. These
  become the **targets**.
- **Component 3 (ML)** learns the map from inputs to targets. If it works, expensive quantum
  properties can be predicted from cheap classical data — a real tool for designing quantum
  processors, because full quantum simulation does not scale.

So the role of this work: generate trustworthy data on *both* sides of the classical–quantum divide,
understand exactly where the two pictures agree and where they part ways, and use that to teach a
machine to predict the quantum side from the classical side. The science is not "make the model fit"
— it is discovering **how far classical information can reach into the quantum world before it
fails.**

**The single sentence that ties it together.** For a harmonic potential, Ehrenfest's theorem says the
quantum averages follow the classical path *exactly* — so there would be nothing to learn. The
fluxonium is anharmonic, Ehrenfest's condition fails, and the gap that opens up is precisely what the
neural network is trained to predict. **The project exists in the gap between §4.11 and §2.9.**

**Why the later tasks tie back to the goal.** Tasks 3 and 4 of Component 1 build the *classical*
inputs (anharmonic, possibly chaotic) and Task 3 of Component 2 builds the *quantum* targets (with
tunneling). The scientific payoff is locating **where** the classical input stops predicting the
quantum output — near barriers, in chaotic regions — because that boundary is where the genuinely
quantum physics lives.

*Suggested entry point if starting the code: Component 1, Task 1 — plot the energy contours and
confirm nested ellipses. That single plot anchors the rest of this guide.*

---

# PART 7 — Symbol glossary

**Foundational vocabulary (Parts 1 and 3):**

| Term | In one line |
|---|---|
| **State** | The smallest complete answer to "what is this system doing now" — enough to determine the future, with nothing redundant. |
| **Vector** | An ordered list of numbers. Its length is the dimension of the space it lives in. |
| **Basis** | The reference directions the numbers in a vector are counted along. |
| **Complex number** | `a + bi` with `i² = −1`. Carries a size *and* a phase, so two can cancel at any angle — which is what makes interference possible. |
| **Matrix / operator** | A grid of numbers that acts on a vector and returns another vector. Order of application matters. |
| **Eigenvector / eigenvalue** | A vector the operator only rescales, and the scaling factor. The eigenvalues are the allowed measurement outcomes. |
| **Probability distribution** | Outcomes with likelihoods attached, non-negative and summing to 1. |
| **Expectation value `⟨Â⟩`** | The average of many measurements, weighted by probability. A plain real number, plottable against time. |
| **Derivative** | A rate of change. `ẋ` is with respect to time; `∂H/∂p` varies only `p`. |

**Classical-chaos vocabulary (§2.10):**

| Term | In one line |
|---|---|
| **Integrable** | As many conserved quantities as degrees of freedom — completely predictable, never chaotic. |
| **Torus** | A doughnut surface. Two independent oscillations need two angles to locate, and two angles = a point on a doughnut. |
| **Quasiperiodic** | Motion that never exactly repeats but is not random — it winds the torus forever. A smooth closed curve of dots on a Poincaré map. |
| **Commensurate / incommensurate** | Two frequencies whose ratio *is* / *is not* a ratio of small whole numbers. |
| **Resonance** | A commensurate frequency ratio. The coupling's small pushes stop averaging out and add up instead, tearing a torus. |
| **KAM theorem** | Nudge an integrable system with a *small* perturbation and, if its frequencies are incommensurate, most tori survive. |
| **Lyapunov exponent λ_max** | How fast two nearby trajectories separate. Positive = chaos, zero = regular. The actual *test*, as opposed to eyeballing a plot. |
| **Chaotic sea** | A region of the Poincaré map filled with scattered dots lying on no curve. |

**Symbols:**

| Symbol | Name | Plain meaning |
|---|---|---|
| `x` | position | where the mass is |
| `p` | momentum | mass × velocity; "how much motion" |
| `v`, `ẋ` | velocity | rate of change of position |
| `ẍ` | acceleration | rate of change of velocity |
| `m` | mass | how heavy |
| `k` | spring constant | stiffness |
| `ω` (omega) | angular frequency | how fast it cycles; `ω=√(k/m)` |
| `E` | energy | total energy |
| `V(x)` | potential energy | energy stored in the spring |
| `T` | kinetic energy | energy of motion |
| `H`, `Ĥ` | Hamiltonian | total energy as a function of `x,p` (hat = operator) |
| `∂H/∂x` | partial derivative | how `H` changes if only `x` moves |
| `\|ψ⟩` | ket (state) | the full quantum state ("psi") |
| `⟨φ\|` | bra | the partner used to ask a question of a state |
| `⟨φ\|ψ⟩` | inner product | overlap between two states (a number) |
| `\|⟨φ\|ψ⟩\|²` | Born rule | probability of measuring outcome `φ` |
| `x̂`, `p̂` | operators | position/momentum as quantum operators |
| `[Â,B̂]` | commutator | `ÂB̂−B̂Â`; nonzero ⇒ order matters ⇒ uncertainty |
| `ℏ` (h-bar) | reduced Planck constant | sets the scale of quantum effects |
| `i` | imaginary unit | `√−1`; written `1j` in Python |
| `â`, `â†` | ladder operators | lower / raise energy by one rung |
| `n̂` | number operator | counts energy quanta |
| `\|n⟩` | Fock state | state of exactly `n` quanta (definite energy) |
| `\|α⟩` | coherent state | most classical-like blob ("alpha") |
| `Eₙ` | energy spectrum | `ℏω(n+½)`; the allowed energies |
| `⟨x̂⟩(t)` | expectation value | average position over time |
| `W(x,p)` | Wigner function | quantum state drawn in phase space (can be negative) |
| `ℓ` | length scale | `√(ℏ/2mω)`; Essler's prefactor, `=1/√2` in natural units |
| `φ` | phase | fluxonium's magnetic phase — plays the role of position |
| `n` | Cooper-pair number | fluxonium's charge count — plays the role of momentum |
| `E_C, E_L, E_J` | circuit energies | charging, inductive, Josephson (§1.3) |

---

# PART 8 — Sanity checks (the golden rule in practice)

Always verify numbers against exact formulas. The oscillator has these checks built in:

1. **Energy spectrum:** numerical eigenvalues from `qutip` must equal `Eₙ = ℏω(n+½)` for low `n`.
   Drift at high `n` means the truncation `N` is too small. *Achieved: 5.3e-15 over the lowest 15.*
2. **Ground-state energy:** the lowest eigenvalue must be `½ℏω`, never zero.
3. **Even spacing:** consecutive levels differ by exactly `ℏω`.
4. **Classical limit:** the coherent state's `⟨x̂⟩,⟨p̂⟩` must trace the classical orbit. For the
   *harmonic* oscillator this should be **exact**, not approximate; a visible gap means the dynamics
   are wrong.
5. **Wigner sign:** the coherent state stays positive everywhere. The Fock state `|n⟩` has **`n` sign
   changes** going outward, with the centre alternating as `W(0,0) ∝ (−1)ⁿ`. (Counting *negative
   regions* rather than sign changes gives ⌈n/2⌉, not `n` — I had this wrong at first.) A `|1⟩` with
   no negative region signals a problem.
6. **Classical trajectories:** `solve_ivp` orbits must be closed, non-crossing and at constant
   energy. *Achieved: drift 1.9e-9; solver vs analytic 6.7e-9.*
7. **Energy conservation under `sesolve`:** `⟨Ĥ⟩` must stay constant. *Achieved: 2.1e-7.*
8. **Data alignment:** the classical trajectory starts at `φ₀`, so `A[:, 0]` must **be** `φ₀`.
   Asserted in the Component 3 generation cell.
9. **A trend is not a measurement.** Before claiming error rises with anything, test it — Lyapunov
   exponent for chaos (§2.10), Spearman correlation for the breakdown axis (§5.6). Both times the
   honest answer contradicted the expected one.

---

# PART 9 — Cross-reference map to Essler's *Lecture Notes for Quantum Mechanics*

The assigned text uses the **same conventions** as this guide and the notebooks. The file is
`reference/Quantum Mechanics Lecture Notes.pdf` (Oxford, 17 Feb 2021, 97 pp.). **Every equation and
section number below was checked against that PDF on 2026-08-13 and all of them are correct.**

The oscillator material is one short, dense chapter — worth knowing the layout:

| Essler section | Title | p. |
|---|---|---|
| 3.2 | Heisenberg Uncertainty Relation | 20 |
| 4.1 | Time dependent Schrödinger equation and **Ehrenfest's theorem** | 23 |
| **6** | **Harmonic Oscillators** — ladder operators, eqs. 228–251 | **38** |
| 6.1 | Ground state of the Quantum Harmonic Oscillator | 41 |
| 6.2 | Excited states of the Quantum Harmonic Oscillator | 42 |
| 6.3 | What oscillates in the quantum harmonic oscillator? | 43 |
| 6.4 | Quantum vs classical harmonic oscillator | 44 |

Coherent states are **Aside 4** (eqs. 281–289), inside §6.4.

| Concept | This guide | Essler notes |
|---|---|---|
| Quantum Hamiltonian `Ĥ = p̂²/2m + ½mω²x̂²` | §4.5 | eq. 228 |
| Creation/annihilation operators (length scale `ℓ`) | §4.6 | eq. 230 |
| Commutator `[â,â†]=1` | §4.6 | eq. 231 |
| `Ĥ = ℏω(â†â+½)`, number operator `N̂=â†â` | §4.6 | eqs. 233–234 |
| Zero-point energy `E₀=½ℏω` | §4.7 | eq. 244 |
| Energy spectrum `Eₙ=ℏω(n+½)` | §4.7 | eq. 246 |
| Ladder actions `â\|n⟩=√n\|n−1⟩` | §4.6 | eqs. 250–251 |
| Position matrix element `⟨m\|x̂\|n⟩` | §4.11 | eq. 276 |
| Why `⟨x̂⟩(t)` oscillates at ω (or vanishes) | §4.7, §4.11 | §6.3 |
| Coherent states `â\|α⟩=α\|α⟩` | §4.10 | Aside 4 (eqs. 281–289) |
| Ehrenfest's theorem | §4.11 | §4.1 |
| Heisenberg uncertainty, minimal-uncertainty ground state | §4.4 | §3.2, eqs. 259–261 |
| Quantum vs. classical (Essler uses `\|ψₙ(x)\|²`; here, Wigner) | §4.12 | §6.4 |
| **Wigner function** | §4.12 | *not in Essler* — from the project handout |

**The one notation difference:** Essler's `ℓ = √(ℏ/2mω)` is the constant in front of the ladder
operators. In natural units it equals `1/√2`, the `1/np.sqrt(2)` in the code. So `x̂ = ℓ(â+â†)`
(Essler) and `x̂ = (â+â†)/√2` (code) are the same equation.

---

# PART 10 — Reading path through Griffiths

**The book:** Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd edition**.
Recommended by Prof. Mondragon-Shem. Essler is the group's assigned text and is terser; Griffiths is
the one to actually *learn* from, then use Essler for the group's exact conventions.

**How the two differ.** Essler goes straight to ladder operators and stays algebraic. Griffiths
builds up from the wave function and the Schrödinger equation first, so the formalism arrives with
motivation attached. For someone new, read Griffiths for understanding and Essler for notation.

## The path, in order

Section numbers are 3rd-edition. Difficulty is my honest estimate of a *first* pass.

**Stage 1 — before anything else (Chapter 1, ~a week).**
- **1.1 The Schrödinger Equation**, **1.2 The Statistical Interpretation** — what the wave function
  actually *is*. The conceptual hurdle, not the maths. `readable`
- **1.3 Probability**, **1.4 Normalization**, **1.5 Momentum** — where expectation values come from.
  Read closely: `⟨x̂⟩` and `⟨p̂⟩` are exactly what Component 2 plots and Component 3 predicts.
  `readable`
- **1.6 The Uncertainty Principle** — why the classical point becomes a blob (§4.4). `readable`
- **Ehrenfest's theorem is Equation 1.38** — the single most relevant result in Chapter 1 for this
  project (§4.11). It is why the coherent state's average traces the classical orbit, and its failure
  is why Component 3 has anything to learn.

**Stage 2 — the oscillator itself (Chapter 2).**
- **2.1 Stationary States**, **2.2 The Infinite Square Well** — warm-up; the square well is the
  cleanest example of quantised levels. `readable`
- **2.3.1 The Harmonic Oscillator, Algebraic Method** (pp. 40–47) — **the most important section in
  the book for this project.** Ladder operators, `Ĥ = ℏω(â†â + ½)`, the spectrum, the zero-point
  energy. Line-for-line what Component 2 Task 1 builds. `readable, do it properly`
- **2.3.2 Analytic Method** — the same answers via Hermite polynomials. Mathematically heavy and
  *not* needed for the code. `hard — skim or skip on the first pass`
- 2.4–2.6 — `optional for now`. Come back to **2.6 the finite square well** later, since it is the
  closest simple analogue of the fluxonium's well.

**Stage 3 — the formalism (Chapter 3). This is the hard one.**
This chapter is the textbook version of Part 3 and §4.1–4.3 of this guide.
- **3.1 Hilbert Space** (p. 93) — what "the space of states" means (§4.1). `hard`
- **3.2 Observables** (p. 95) — Hermitian operators, and why observables must be Hermitian (§4.3). `moderate`
- **3.3 Eigenfunctions of a Hermitian Operator** (p. 97) — discrete vs continuous spectra (§3.4,
  §4.8). `hard`
- **3.4 Generalized Statistical Interpretation** (p. 103) — what a measurement returns and with what
  probability (§4.2). `moderate`
- **3.5 The Uncertainty Principle** (p. 105) — the general proof. **3.5.2 The Minimum-Uncertainty
  Wave Packet** (p. 108) deserves real attention: that state *is* the coherent state, and its width
  is the `φ_zpf = 1.41` explaining why my fluxonium packet is as wide as the well.
  `hard, but 3.5.2 pays for itself`
- **3.6 Vectors and Operators / Dirac Notation** (p. 113) — bras, kets, inner products, changing
  bases (§3.1, §4.2). `moderate — mostly notation once the idea lands`

**Stage 4 — the parts that matter for the fluxonium.**
- **Problem 3.42, "Coherent states of the harmonic oscillator"** (pp. 126–127) — *do this problem.*
  It defines the coherent state as an eigenstate of the lowering operator, shows it minimises
  uncertainty, and shows it behaves quasiclassically. That is precisely what `qt.coherent(DIM, alpha)`
  builds in Components 2 and 3. Nothing else in the book is this directly useful.
  `moderate, and worth the time`
- **9.2 Tunneling** (pp. 358–362) — the mechanism behind the fluxonium's 0.134 `E_C` doublet (§4.13).
  Read 9.1 first for context. `hard, but read 9.2 for the picture`

**Stage 5 — optional context.**
- **Chapter 6, Symmetries & Conservation Laws** — the quantum version of the Hamiltonian structure
  behind Component 1. `hard, save for later`

## Cross-reference: concept → this guide → both books

| Concept | This guide | Essler | Griffiths (3rd ed) |
|---|---|---|---|
| The wave function, statistical interpretation | §4.1 | — | §1.1–1.2 |
| Expectation values `⟨x̂⟩, ⟨p̂⟩` | §3.5, §4.11 | — | §1.3–1.5 |
| Ehrenfest's theorem | §4.11 | §4.1 | **eq. 1.38**, §1.5 |
| Uncertainty principle | §4.4 | §3.2, eqs. 259–261 | §1.6; general proof §3.5 |
| Quantum Hamiltonian | §4.5 | eq. 228 | §2.3 |
| Ladder operators, `[â,â†]=1` | §4.6 | eqs. 230–231 | **§2.3.1** (pp. 40–47) |
| `Ĥ = ℏω(â†â+½)`, number operator | §4.6 | eqs. 233–234 | §2.3.1 |
| Energy spectrum `Eₙ=ℏω(n+½)` | §4.7 | eq. 246 | **eq. 2.62** (§2.3.1) |
| Zero-point energy `E₀=½ℏω` | §4.7 | eq. 244 | **eq. 2.61** (§2.3.1) |
| Hilbert space | §4.1 | — | **§3.1** (p. 93) |
| Operators as observables, Hermiticity | §4.3 | — | §3.2 |
| Eigenvalues, discrete vs continuous spectra | §3.4, §4.8 | — | §3.3 |
| What a measurement returns | §4.2 | — | §3.4 |
| Bra-ket notation, inner product | §4.2 | — | §3.6 (p. 113) |
| Minimum-uncertainty wave packet | §4.10 | — | **§3.5.2** (p. 108) |
| Coherent states | §4.10 | Aside 4 | **Problem 3.42** (pp. 126–127) |
| Tunneling through a barrier | §4.13 | — | **§9.2** (pp. 358–362) |

## What is *not* in Griffiths

Worth knowing so I do not go hunting:

- **The Wigner function.** Not in Griffiths, same as Essler. The index has "Wigner, E." (the person)
  and the **Wigner–Eckart theorem**, which is about angular-momentum selection rules and has nothing
  to do with phase-space quasi-probability. My Wigner material comes from the project handout.
- **Superconducting circuits, Josephson junctions, the fluxonium.** Not a Griffiths topic — that is
  the PennyLane tutorial (Part 12) and the `scqubits` documentation.
- **Classical chaos, Poincaré maps, KAM tori.** Component 1 Task 4 territory — Goldstein Ch. 11 and
  Tong's *Classical Dynamics*, not a quantum textbook.

## If I only have a few hours

Read **§2.3.1** and do **Problem 3.42**. Between them they cover the ladder operators behind
Component 2 Task 1 and the coherent state behind Task 2 and all of Component 3 — the two pieces of
theory my code leans on hardest.

---

# PART 11 — Where the classical material lives in Goldstein

**The book:** Goldstein, Poole & Safko, *Classical Mechanics*, **3rd edition**. This is the source
behind Part 2, and especially §2.10 — but the guide had no map for it, so here it is. Page numbers
are the printed ones, checked against the PDF.

**Chapter 6 — Small Oscillations.** The chapter behind the normal-mode analysis in §2.10.

| Section | Title | p. | Why it matters here |
|---|---|---|---|
| 6.1 | Formulation of the Problem | 238 | sets up coupled oscillators about equilibrium |
| **6.2** | The Eigenvalue Equation and the Principal Axis Transformation | **241** | **the 45° rotation used in §2.10** — this is what "principal axis" means |
| **6.3** | Frequencies of Free Vibration, and Normal Coordinates | **250** | where `ω_± = ω√(1±λm)` comes from |
| 6.4 | Free Vibrations of a Linear Triatomic Molecule | 253 | a worked example of the same machinery |
| 6.6 | Beyond Small Oscillations: the Damped Driven Pendulum | 265 | the bridge into Chapter 11 |

**Chapter 11 — Classical Chaos.** Everything in §2.10 after "the four words".

| Section | Title | p. | Why it matters here |
|---|---|---|---|
| 11.1 | Periodic Motion | 484 | tori, commensurate vs incommensurate frequencies, dense orbits |
| **11.2** | Perturbations and the Kolmogorov–Arnold–Moser Theorem | **487** | **the KAM theorem and its two conditions** |
| 11.3 | Attractors | 489 | — |
| **11.4** | Chaotic Trajectories and Liapunov Exponents | **491** | **the test that overturned my chaos claim** |
| **11.5** | Poincaré Maps | **494** | how to build and read the Task 4 figure |
| **11.6** | Hénon–Heiles Hamiltonian | **496** | structurally the same problem as Task 4 |
| 11.8 | The Logistic Equation | 509 | the classic route-to-chaos example |

> **Note on spelling.** Goldstein writes "**Liapunov**"; most other sources (and this guide) write
> "**Lyapunov**". Same person, same exponent — do not go hunting for two different things.

**If I only read three sections:** **§6.2** (the principal-axis rotation that decouples my two
oscillators), **§11.2** (KAM — why my tori survive), and **§11.4** (Liapunov exponents — the
measurement that contradicted what I had written). Those three are the entire theoretical backing
for §2.10.

---

# PART 12 — From oscillator to qubit: the hardware connection

*(Based on the PennyLane tutorial "Quantum computing with superconducting qubits", assigned by the
group.)*

This ties the project to its title, "AI Design of **Quantum Processors**." The harmonic oscillator
simulated here is not a toy — it is the literal starting point of a real superconducting qubit.

## What actually makes a circuit "quantum" — it is not the superconductivity, and it is not speed

**Superconductivity is necessary but not sufficient.** It buys two preconditions — no dissipation,
and one macroscopic wavefunction (§1.3) — but neither of those *is* the quantum behaviour.

**The real criterion is `ℏω ≫ k_B T`**: the gap between energy levels must be much larger than the
thermal energy knocking the circuit around. If it is, the circuit sits in its ground state and can be
deliberately placed in level 1 or in a superposition — the discreteness is *resolvable*. If it is
not, thermal noise kicks it across many levels at once, everything averages, and it behaves
classically.

| Temperature | thermal energy as a frequency | vs a 5 GHz qubit | |
|---|---|---|---|
| 300 K (room) | 6251 GHz | 0.001× | hopelessly classical |
| 4.2 K (liquid helium) | 87.5 GHz | 0.06× | still classical |
| **1.2 K** (aluminium turns superconducting) | 25.0 GHz | 0.2× | **superconducting and still classical** |
| 10 mK (dilution fridge) | 0.21 GHz | **24×** | quantum |

That 1.2 K row is the point: the metal is superconducting there and the circuit is *still not
quantum*. The dilution fridge is a separate requirement on top.

**"Quantum" does not mean faster.** Superconducting qubits run at a few GHz — slower than the
transistors in a laptop. Speed is not the axis. Three things a classical circuit cannot do at *any*
speed:

1. **Energy comes in discrete lumps.** A classical LC circuit stores any amount of energy; a quantum
   one only `E₀, E₁, E₂, …`. There is no 1.5 quanta — those are the only values that exist. A
   classical version of `fig_c2_energy_spectrum.png` would be a solid continuum, not dots.
2. **Superposition.** It can occupy levels 0 and 1 simultaneously with a definite phase relation
   between them — not "we do not know which." The difference is measurable as interference, which is
   the striped pattern in `fig_c2_wigner_t0.png`, and no ignorance-based story reproduces it.
3. **Tunnelling.** The 0.134 `E_C` doublet exists because the state has amplitude on *both* sides of
   a barrier a classical particle cannot cross — `fig_c2_fluxonium_sweep.png`.

**It is the same circuit, not a different kind of circuit.** An inductor and a capacitor; what
changes is the regime:

| | Regular LC circuit | Superconducting LC at 10 mK |
|---|---|---|
| energy | continuous, any value | discrete, `Eₙ = ℏω(n+½)` |
| the state | 2 real numbers (charge, flux) | complex amplitudes over levels |
| resistance | yes — energy decays away | zero |
| obeys | Kirchhoff's laws, ODEs | the Schrödinger equation |
| superposition | no | yes |
| tunnelling | no | yes, with a junction |

Note the top-left cell: a regular LC circuit's state is **two real numbers**, which is a classical
state in exactly the §1.1 sense — the same kind of object as `(x, p)`.

**And this project computes both descriptions of the same device.** Component 1 treats `φ` and `n` as
ordinary numbers; Component 2 treats the same `φ` and `n` as operators. Same Hamiltonian, two
rule-sets. So "what is the difference between a quantum circuit and a regular one" is not abstract
here — it is the gap that was measured: **copy-classical's 1.067 rad** (§5.5) *is* that difference,
quantified for this device.

---

**A qubit starts as a circuit that *is* a harmonic oscillator.** A superconducting **LC circuit** (an
inductor plus a capacitor) oscillates exactly like a mass on a spring: charge sloshes back and forth,
energy trading between inductor and capacitor. Its quantum energy levels are the ones computed in
Component 2 — evenly spaced, `Eₙ = ℏω(n+½)`. The LC circuit is a harmonic oscillator in different
clothing, and §1.3 spells out which physical quantity plays which role.

**A perfect harmonic oscillator cannot be a qubit — and the reason is the exact property plotted in
Component 2.** A qubit needs just *two* usable levels. To control it, a photon tuned to the 0→1
energy gap drives the transition. But because the levels are **evenly spaced** — the result in
`fig_c2_energy_spectrum.png` — that same photon also drives 1→2, 2→3, and so on. The two levels
cannot be isolated. The equal spacing verified as a clean physics result is precisely what makes a
pure oscillator useless as a qubit.

**The fix: break the even spacing with a Josephson junction.** Replacing the inductor with a
**Josephson junction** — a thin insulating gap that Cooper pairs tunnel across — changes the
potential from a perfect parabola into an *anharmonic* well. The levels become **unevenly spaced**,
so the 0→1 gap is unique and a photon at that frequency moves *only* 0→1. This device is an
"**artificial atom**", and §2.9's cosine term is its classical shadow.

**The transmon.** Adding control wiring reintroduces sensitivity to electrical noise; the practical
solution (a large shunt capacitor) is the **transmon regime**, keeping just enough anharmonicity to
be a clean qubit while staying robust — today's workhorse qubit.

## Why superconducting circuits, honestly — the pros and the cons

**The pros.**

- **They are *designable*.** An atom arrives with whatever energy levels nature gave it. A circuit's
  levels are set by `E_J`, `E_C` and `E_L` — parameters *chosen at fabrication*. That is why there is
  a design space at all, and it is the reason this project is called "AI **Design** of Quantum
  Processors." Nothing to search means nothing to optimise.
- **They can be printed.** Lithography, on a wafer, by the thousand. Trapped ions are naturally
  quantum and naturally anharmonic, but cannot be mass-fabricated the same way.
- **They couple strongly to ordinary control electronics**, so driving and reading them is
  microwave engineering rather than optics.

**The cons, which are worth knowing before being asked.**

- **Coherence is short** — microseconds, against seconds for trapped ions.
- **They need a dilution fridge**, ~10 mK (see the table above).
- **Fabrication variation** means no two qubits come out identical, which is itself part of why
  predicting device properties from cheap models is useful.
- **A quantum computer is not a general-purpose speedup.** For most tasks it is worse. The solid
  application is *simulating quantum systems* — Feynman's argument, and the same scaling wall
  quantified in §1.0.

**Where this project sits.** Components 1–2 build and validate the *foundational* model in both
classical and quantum form. A real processor's qubit is *that oscillator plus a controlled anharmonic
tweak* — which is exactly what the fluxonium of §4.13 is. Learning to predict quantum properties from
classical data on the clean, exactly-solvable oscillator is the essential first rung; the same
machinery extends toward the harder systems actual processors are made of. That is the bridge from
"mass on a spring" to "designing quantum processors."

---

> **See also.** `Findings_and_Corrections.md` records the errors found during review — the fluxonium
> coordinate convention, the chaos claim, and the sampling-window null — and how each was caught.
> `Code_Walkthrough_Components_1_to_3.md` explains every line of the code itself, assuming no Python
> knowledge. `Handout_Compliance.md` maps every lettered requirement in the PI's handout to where it
> is satisfied, and lists the five places the work deliberately differs from the handout with the
> reasoning — the fluxonium coordinate convention being the one that matters most.
