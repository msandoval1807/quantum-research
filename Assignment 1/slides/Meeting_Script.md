# Meeting script — Components 1–3 update

**Deck:** `Components_1_3_Update.pptx` (23 slides) · **Target length:** ~20 minutes talking, then questions.

**How to use this.** One block per slide. The *Say* lines are the point I need to land — not a
word-for-word reading. The *Numbers* lines are what to have ready if he asks. If I am running
long, the slides marked **[can skip]** are the ones to drop.

**The one thing I want him to remember:** the pipeline works end to end on a real fluxonium, and
it works because I checked my own results against something external rather than against what I
expected. Two of those checks caught real errors — a coordinate convention that was pairing every
classical trajectory with the wrong quantum one, and a chaos claim that the Lyapunov exponent did
not support. Both are on the slides deliberately.

---

## Opening (slide 1 — title)

> "Thanks for making time. I've got all three components running end to end now, so I want to
> walk through the classical side, the quantum side, and then the machine learning that connects
> them. There's one bug I found along the way that I think is the most interesting part, so I'll
> flag it when we get there."

Don't linger. Ten seconds.

---

## Slide 2 — Context: the pipeline

**Say.** Component 1 makes the classical data — that's the cheap input. Component 2 makes the
quantum data — the expensive target. Component 3 learns the map between them. The question
underneath all of it is how far cheap classical information can predict expensive quantum
behaviour, and where it stops working.

**If he pushes:** the goal is *not* using quantum computing to speed up AI. It's the reverse —
ordinary machine learning on a normal computer predicting properties of quantum hardware.

---

## Slide 3 — Results divider

Just say "so, results" and move on.

---

## Slides 4–6 — Component 1, Tasks 1–2 (the perfect spring) **[can skip 5]**

**Say.** Energy contours in phase space are closed curves, so a classical oscillator of fixed
energy is locked onto one orbit. I integrate Hamilton's equations and get exactly that. The
point of these three slides is that everything here has an exact formula to check against —
that's the safety net for the parts that don't.

**Numbers.** Numerical vs analytic solution agrees to 6.7e-9. Energy drift over a full period
is 1.3e-8 across all 12 saved trajectories.

---

## Slide 7 — Component 1, Task 3 (cosine oscillator)

**Say.** Adding a cosine term makes the oscillator anharmonic — the orbits stay closed but stop
being ellipses, and the period starts depending on energy. This matters because anharmonicity is
what makes a qubit addressable at all: if the levels are evenly spaced you can't drive just two
of them.

---

## Slides 8–9 — Component 1, Task 4 (coupling and chaos)

**Say (8).** Two of these oscillators coupled through their momenta. The state is four numbers,
so I can't draw the motion directly — these are the four 2-D projections.

**Say (9).** A Poincaré section records the state only as it crosses a chosen surface, in one
direction — a tangled orbit becomes a set of dots. Smooth nested curves mean regular motion; a
scattered cloud filling a region would mean chaos.

**This is the second thing I want to walk you through, and it's a correction:**

> "I originally wrote this up as an order-to-chaos transition — regular at E = 1, chaotic at
> E = 12. Then I noticed the E = 12 points still looked like they were sitting on curves, so
> instead of judging by eye I measured the maximal Lyapunov exponent. It came out around 0.005 at
> every energy I tried, which is zero to within the log t over t convergence floor. The motion is
> regular throughout — there's no chaos here."

**Then give the reason, because it's the interesting part:**

> "I think my intuition was backwards. The nonlinear term is a cosine, so it's bounded — it never
> exceeds V₀ no matter how much energy you put in. The harmonic term grows without limit. So at
> high energy this system becomes *more* nearly harmonic, closer to integrable, not less. The KAM
> tori survive because the perturbation stays small in exactly the sense the theorem needs."

**And where the chaos actually is:**

> "Turning up the coupling does it instead of turning up the energy. At λ = 0.8 with V₀ = 8 and
> E = 12, the Lyapunov exponent is 0.11 — unambiguously chaotic. So the transition is controlled
> by coupling strength and well depth. I'd be interested whether Task 4 should be re-run there."

**Also fixed here.** A proper Poincaré map needs several trajectories per energy — one alone draws
a single curve. And it needs one consistent crossing direction: I was filtering on p₂ > 0, but the
crossing direction is dx₂/dt = p₂/m + λp₁, which isn't the same sign when the coupling is in the
momenta. About 5% of my recorded crossings were going the wrong way.

---

## Slides 10–14 — Component 2, Tasks 1–2 (the quantum oscillator) **[can skip 12]**

**Say (10–11).** Operators built from ladder operators in QuTiP. Ĥ is diagonal, x̂ and p̂ only
connect neighbouring levels — that's the ladder structure made visible. The eigenvalues land
exactly on Eₙ = ℏω(n+½), with a nonzero ground state at ½.

**Say (12).** Truncation matters: roughly the lowest N/2 levels are trustworthy for a given N.

**Say (13–14).** The Wigner function puts a quantum state in the same phase-space plane as the
classical picture. The coherent state is a positive blob that orbits like a classical particle —
that's Ehrenfest's theorem. The Fock state has a negative core and the superposition shows
interference fringes; neither has any classical explanation.

**Numbers.** Spectrum matches the exact formula to 5.3e-15 over the lowest 15 of N = 30 levels.

---

## Slide 15 — Component 2, Task 3: the fluxonium

**Say.** This is where it stops being a textbook problem. The fluxonium is a real superconducting
qubit — a Josephson junction shunted by a large inductor. At half flux the potential is a
symmetric double well, and the two lowest states form a tunneling doublet: they're split by only
0.13 E_C while the next level up is 4.6 away. That factor of 34 is what isolates a clean
two-level system, and that tiny splitting *is* tunneling through the barrier. There's no
classical version of it.

**Numbers.** E_J/E_C = 5, E_L/E_C = 0.5, half flux. Wells at φ = ±2.85, barrier 7.76 E_C above
them at φ = 0. Built with `scqubits`.

---

## Slide 16 — Fluxonium dynamics **← the bug slide, slow down here**

**Say.** Both start at the well minimum with the same small charge kick. They agree closely for
about half a period, then the quantum average loses amplitude while the classical point keeps
swinging.

**If he asks why — and he will — give the precise answer, not "the packet spreads":**

> "Ehrenfest's theorem says d⟨p⟩/dt is the *average of the force*, ⟨−∂V/∂x⟩ — not the force
> evaluated at the average position. Those two agree only when the force is linear, so only for a
> harmonic potential. The fluxonium's force has a sine in it, and ⟨sin φ̂⟩ isn't sin⟨φ̂⟩. So the
> averages here obey no classical equation of motion at all. That's Griffiths equation 1.38."

That is also why Component 2 Task 2 agreed *exactly* — a harmonic potential is the one case where
Ehrenfest is exact for any state and any packet width — and why there is anything for the MLP to
learn in Component 3: it is modelling precisely the term Ehrenfest throws away.

**Then, the bug — say it plainly:**

> "This plot was wrong the first time I made it, and the reason is worth explaining. `scqubits`
> writes the fluxonium potential with the inductive term centred on φ = 0, so the wells sit at
> ±2.85 and φ = 0 is the top of the barrier. I'd written it the other common way — shifting the
> coordinate by the external flux instead — which is the same physics but a different coordinate.
> I used one form for my classical trajectory and let `scqubits` use the other for the quantum
> state. So every comparison I was making was between a classical particle and a quantum state
> half a flux quantum apart."

**What it cost me.** The potential curve was drawn π away from the wavefunctions plotted on top
of it. And the window I was sampling from — I thought it straddled the well minimum, but in
`scqubits`' coordinate it was centred exactly on the barrier top. Every training packet was
launched where it splits and tunnels instead of orbiting.

**How I caught it.** Checked where `fluxonium.wavefunction()` actually puts its probability and
compared that against the potential I was drawing. They didn't match. Confirmed it against the
`scqubits` source and documentation.

**If he asks whether I'm sure:** yes — the fix makes the classical-vs-quantum error symmetric
under φ → −φ, which is exactly what the symmetric potential demands and what the broken version
didn't do.

---

## Slide 17 — Sweep across the wells

**Say.** Five starting phases, one well to the other. In the wells the two orbits come closest.
Launched on the barrier top, the classical point sweeps a wide figure-eight through both wells
while the packet splits and stays put — same initial condition, completely different answers.
That gap is exactly what Component 3 has to learn.

---

## Slide 18 — Component 3 divider

> "So that's the data. Here's the model."

---

## Slide 19 — Training

**Say.** 300 paired trajectories, classical input and quantum target from the same starting
packet. A two-hidden-layer MLP, 128 wide, MSE loss, Adam, 80/20 split. Validation MSE lands at
9.3e-4 against a training MSE of 5.4e-4 — a gap of 1.7×.

**The headline:** before the convention fix that validation number was 8.4e-3 with a gap of
13.7×. Fixing the coordinate improved it about nine-fold. Physically consistent pairs are what
made the map learnable at all.

**Be honest:** validation was still falling at epoch 150, so the model is under-trained. More
epochs is the obvious next experiment and I haven't run it yet.

---

## Slide 20 — Held-out prediction

**Say.** One validation trajectory. Grey dotted is the classical input, blue is the true quantum
target, red dashed is the prediction. The prediction sits on the quantum curve, not on its own
input — so the network learned the correction, not a copy.

---

## Slide 21 — The finding

**Say.** Median RMS difference between classical input and quantum target, binned by how far the
packet starts from the well minimum: 0.84, 0.97, 1.19 radians. It degrades steadily as you move
up the wall.

**The part I find interesting:** it never gets below about 0.8. At E_J/E_C = 5 the packet width
is comparable to the well, so a coherent state just isn't a classical point particle anywhere in
this regime. That's a statement about the parameter regime, not about my numerics.

---

## Slide 22 — Verification

**Say.** Every number in the deck is checked against an exact formula where one exists — spectrum
to 5e-15, energy drift 1e-8, solver against the analytic solution to 7e-9. That discipline is
what caught the convention bug, and a few smaller ones: my Wigner animations had a colour scale
that silently rescaled every frame, and the GIFs shipped with no frame delay at all.

---

## Slide 23 — Open questions

Hand it to him. Lead with these two:

1. Is the model learning physics or interpolating? Testing outside the training window would
   tell us.
2. Should the target be trajectories at all, or something with no classical analogue — the
   tunneling splitting, say?

Then: does a deeper well (larger E_J/E_C) bring classical and quantum back together, the way the
correspondence principle says it should? And which fluxonium property is actually worth
predicting for real device design — that one is genuinely his call.

---

## Questions I should be ready for

**"Why the harmonic oscillator?"** — Exactly solvable both classically and quantum-mechanically,
so every number has a built-in answer key. It's the safety net.

**"Why an MLP and not something structured?"** — It's what the handout asked for, and it's the
right baseline: if a plain MLP can't learn the map, a fancier architecture won't tell me why.
Now that it works, structure is the obvious next step.

**"How do you know the model isn't just copying the input?"** — Slide 20. The prediction follows
the quantum curve, which is visibly separate from the classical input it was given.

**"Is 300 samples enough?"** — Probably not. Going from the broken pairs to clean ones moved the
error an order of magnitude, so I haven't yet isolated how much is sample count versus data
quality. Worth a sweep.

**"What's your truncation?"** — N = 30 for the oscillator, cutoff 110 for the fluxonium in
Component 2 and 80 in Component 3, where I run one `sesolve` per sample and traded headroom for
speed. Both well above the 40–60 the handout suggests.

**If I don't know something:** say so and write it down. Don't guess — the whole project runs on
being able to check every number.

---

## Before the call

- [ ] Send the deck the day before.
- [ ] Reread the slide 16 bug explanation out loud once. It's the part worth getting right.
- [ ] Have the notebooks open in a second window in case he wants to see code.
- [ ] Have `reference/PROJECT_CONTEXT.md` §11 open — it's the written version of the bug story.
