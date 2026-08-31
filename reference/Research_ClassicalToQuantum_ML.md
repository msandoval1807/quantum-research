# Research Notes — Getting Closer to the Goal: Predicting Quantum from Classical with ML

**Author / for:** Marcos Sandoval Lucas · AI Design of Quantum Processors, Mondragon-Shem Quantum Group (UIC)
**Purpose:** A survey of the ideas, published work, and concrete techniques that can take this project from the current baseline (an MLP mapping classical → quantum fluxonium trajectories) toward the real goal: *reliably predicting quantum behavior from cheap classical data, and understanding where that prediction breaks down.*
**Last updated:** 2026-07-29.

> How to read this: Section 1 frames the goal and what the research literature already establishes. Section 2 surveys the key papers. Section 3 is the practical part — concrete ways to improve **this** project's model. Section 4 is a staged roadmap. Section 5 has references with links.

---

## 1. The goal, restated in research terms

Our project is a **supervised regression / operator-learning** problem: learn a map `f: A → B` where the input `A` is a classical trajectory (cheap) and the target `B` is the matching quantum trajectory of observables `⟨φ̂⟩(t), ⟨n̂⟩(t)` (expensive, from `sesolve`). The deeper scientific question — *how much of the quantum behavior is recoverable from classical information, and where does it fail* — is exactly the frontier the recent literature is mapping out.

Two results from that literature matter most for us:

1. **Classical data + machine learning is provably powerful.** It is now proven that classical ML models, *after learning from data*, can efficiently predict quantum properties that classical algorithms *without* data cannot (Huang et al., *Science* 2022). This is the theoretical backbone of our project: learning from paired data is what makes the classical side able to predict the quantum side.

2. **There is a real breakdown point.** Both classical shadows (Huang–Kueng–Preskill, *Nature Physics* 2020) and the "power of data" analysis (Nature Comms 2021) quantify *when* classical descriptions suffice and when genuinely quantum resources are needed. Our fluxonium is a perfect small testbed for locating that boundary (e.g. tunneling near the flux sweet spot has no classical analogue).

---

## 2. What the literature says (annotated)

**Classical shadows — "Predicting many properties of a quantum system from very few measurements"** (Huang, Kueng, Preskill, *Nature Physics* 2020). A compact *classical description* of a quantum state (a "classical shadow") built from few measurements can predict many properties — energies, correlations, local observables — with a number of samples that scales only logarithmically in the number of target properties. **Relevance:** it legitimizes the whole premise that a classical object can stand in for a quantum state, and suggests representing our quantum target compactly (predict *properties/observables*, not the full wavefunction — which is exactly what we do with `⟨φ̂⟩, ⟨n̂⟩`).

**"Provably efficient machine learning for quantum many-body problems"** (Huang, Kueng, Torlai, Albert, Preskill, *Science* 2022). Proves classical ML can efficiently predict ground-state properties of gapped Hamiltonians *after training on data from the same phase*, and can classify quantum phases; numerics on Rydberg arrays, 2-D Heisenberg, topological phases. **Relevance:** direct theoretical justification that our data-driven approach can generalize across a family of Hamiltonians/parameters — motivating us to train across a *range* of fluxonium parameters and initial conditions, not just one.

**"Power of data in quantum machine learning"** (Nature Communications 2021). Classical ML with enough data can rival quantum models even when the data-generating circuits are classically hard. Introduces geometric/'"projected quantum kernel"' tools to say *when* classical models keep up. **Relevance:** tells us data quantity and the right feature representation are the levers; and gives a language for arguing where classical prediction should still succeed.

**"Emulating quantum dynamics with neural networks via knowledge distillation"** (Frontiers in Materials 2022). Trains a neural network to emulate the time evolution of quantum *wave packets* in a potential, using a curriculum of simple, physics-rich examples ("knowledge distillation"). **Relevance:** this is the closest analogue to our task (wave-packet dynamics → NN emulator). Takeaways we can copy: build a *curriculum* of easy-to-hard initial conditions, and inject physics structure into the training examples rather than throwing raw data at the network.

**"Fourier Neural Operators for Time-Periodic Quantum Systems: Learning Floquet Hamiltonians, Observable Dynamics, and Operator Growth"** (arXiv 2025). Uses Fourier Neural Operators (FNOs) to learn *observable dynamics* of quantum systems. **Relevance:** oscillatory quantum trajectories are smooth and near-periodic — exactly what FNOs exploit. A strong candidate architecture upgrade from a plain MLP (see §3).

**"Machine learning on quantum experimental data toward solving quantum many-body problems"** (Nature Communications 2024). Applies ML to (noisy) experimental quantum data. **Relevance:** a pointer for later, when/if the group moves from simulated targets to real device data.

**Neural operators & sequence models for dynamics (general ML).** Fourier Neural Operators and DeepONets learn maps between *function spaces* (resolution-invariant), and RNN/LSTM/GRU/Transformer models capture temporal correlations. A common warning: **autoregressive rollout accumulates error** over long horizons — so for long-time prediction, prefer direct multi-step output or operator methods over step-by-step feedback.

---

## 2b. Where to actually start reading *(added 2026-08-30)*

§2 above is the theory backbone. This section is the **reading path** — what to read first, and
why each one earns its place. Everything here is free on arXiv.

**Start here if the ML side feels opaque.**

**Dawid et al., *Modern applications of machine learning in quantum sciences*** (arXiv:2204.04198,
Cambridge University Press 2025). 287 pages, 92 figures, written as a course rather than a paper —
supervised/unsupervised learning, phase classification, quantum state representation, circuit
optimization, all with the physics reader assumed and the ML assumed *not*. **Why it matters here:**
it is the single best answer to "I don't know what any of this means." Read the supervised-learning
and observable-prediction chapters; they are Component 3 with better notation.

**Carleo et al., *Machine learning and the physical sciences*** (arXiv:1903.10563,
Rev. Mod. Phys. **91**, 045002 (2019)). The standard review. Shorter and broader than Dawid; good for
seeing where this project sits in the wider field before going deep.

**Read this one for the hardware.**

**Kung et al., *Automatic Characterization of Fluxonium Superconducting Qubit Parameters with Deep
Transfer Learning*** (arXiv:2503.12099, 2025). Trains on energy spectra computed from a model
Hamiltonian across magnetic fields and predicts **E_J, E_C and E_L** — the exact three parameters
this project fixes at `E_J/E_C = 5`, `E_L/E_C = 0.5`. Reports 95.6% average accuracy, and degrades
gracefully when the input spectrum is noisy or incomplete. **Why it matters here:** it is the closest
published neighbour to Component 3 — same qubit, same parameters, ML in the loop — but it runs the
map in the *opposite direction* (spectrum → parameters, where we do classical trajectory → quantum
observables). Worth raising with the PI as the natural "what would a next project look like" answer,
and as evidence the fluxonium-plus-ML pairing is an active area rather than a toy exercise.

**Read this one to name the breakdown result.**

The Component 3 finding — error climbing 5.2× as the packet is launched further toward the
barrier — has an established name in the literature: the **Ehrenfest time**, the timescale on which
a localized wave packet spreads enough to feel the nonlinearity of the potential, after which
expectation values stop following the classical equations. See Zurek and Paz on chaotic systems
(arXiv:nlin/0012048) and the integrable-system treatment in arXiv:1801.06389.

**Why this is worth the effort:** right now the breakdown is written up as an empirical observation
with a Spearman ρ attached. Framed as Ehrenfest-time physics it becomes a *measurement of a known
quantity* in a new system, which is a materially stronger claim and connects directly to the
Ehrenfest-condition argument already used on the fluxonium-dynamics slide.

> **Caveat, stated because it has not been checked.** The Ehrenfest-time literature is largely built
> around *chaotic* systems, where the timescale goes as `ln(1/ℏ)` and is set by the Lyapunov
> exponent. Component 1 established that this system is **regular, not chaotic** (λ_max ≈ 0.005 at
> every energy tested). The integrable-system reference is the relevant one, and whether the standard
> scaling carries over here is an open question — not something to assert in the meeting. Ask the PI
> rather than claim it.

---

## 3. Concrete ways to improve *this* project's model

Ordered roughly from cheapest/highest-value to more advanced.

### 3.1 Better inputs (feature engineering on the classical side)
The current input is the raw classical trajectory vector. Physics-aware features often help far more than a bigger network:
- Add the **conserved energy** `E₀`, the **initial condition** `(φ₀, n₀)`, and the **classical period** as extra input features.
- Add **action–angle** or amplitude/phase features. For the coupled system (C1 Task 4), Poincaré-section descriptors would flag regular vs. chaotic regimes — but note that at the parameters currently used the motion is regular at *every* energy tested (`Findings_and_Corrections.md` §2), so this feature only becomes informative once Task 4 is re-run at stronger coupling.
- Represent the trajectory in a **Fourier basis** (a few dominant frequencies), since the dynamics are oscillatory — fewer, more meaningful numbers than 80 raw samples.

### 3.2 Better architectures (the target is a time series, not a flat vector)
A plain MLP ignores the temporal structure. Options, in increasing sophistication:
- **1-D convolutional network** over the time axis — cheap, captures local temporal patterns.
- **RNN / LSTM / GRU** — designed for sequences; good for preserving time correlations.
- **Neural ODE** — learn the *rate of change* and integrate; naturally continuous-time, good inductive bias for dynamics.
- **Fourier Neural Operator (FNO)** — learn the map in frequency space; strong for smooth, (near-)periodic dynamics like ours, and resolution-invariant so it can predict on finer time grids than it trained on.
- **Transformer** — flexible for long sequences, but usually needs more data.

### 3.3 Physics-informed learning (biggest win for small datasets)
Injecting known physics reduces the data needed and improves generalization:
- **Conservation penalties.** Add loss terms that keep the predicted trajectory's energy `⟨Ĥ⟩` (or the classical energy) approximately constant.
- **Hamiltonian Neural Networks / symplectic networks** — architectures that build energy conservation and phase-space structure in by construction.
- **Ehrenfest / correspondence prior — now well motivated.** Ehrenfest's theorem gives `d⟨p⟩/dt = ⟨−∂V/∂x⟩`, the average of the force, which equals the classical force at the average position *only for a harmonic potential*. Everything the network has to learn is that discrepancy. So train it to predict the **residual** `B − A` (the quantum correction) rather than `B` from scratch: the residual is literally the term Ehrenfest discards, which makes it both easier to learn and physically interpretable. Measured size of that residual: RMS 1.067 rad in the in-well dataset, and 1.673 rad when sampling out to the barrier — where it rises from 1.04 at the well bottom to 2.48 at the barrier top (Spearman ρ=+0.86, p=8.5e-19). That rise *is* the classical→quantum breakdown, measured directly.

### 3.4 Data and sampling strategy
- **Scale the dataset** (more samples than the current 300) and, per the *Science* 2022 result, sample across a **range of parameters** (`E_J/E_C`, `E_L/E_C`, flux) so the model learns a family, not one point.
- **Curriculum learning** (from the knowledge-distillation paper): start with easy, near-harmonic initial conditions, then add strongly nonlinear / near-barrier ones.
- **Targeted sampling of the breakdown region.** Deliberately oversample initial conditions near the flux sweet spot / barrier where classical–quantum divergence is largest — that is where the model (and the science) is most tested.
- Keep a proper **train / validation / test** split, and standardize inputs and targets (already done).

### 3.5 Quantifying the classical→quantum breakdown (the actual science)
This is the project's real deliverable, not just a low validation loss:
- Plot **prediction error vs. a physical axis** — initial energy, or distance of `φ₀` from the well minimum at `φ ≈ 2.85` (the barrier sits at `φ = 0`; see `Findings_and_Corrections.md` §1 for why the coordinate matters). The error should stay low in the near-classical regime and rise where quantum effects dominate.
- Compare against **honest baselines**: linear regression, k-nearest-neighbors, and "just copy the classical trajectory" (`B̂ = A`). The MLP must beat all three to be meaningful. **Measured 2026-08-13:** copy-classical 1.067, k-NN (k=1) 0.077, linear regression 0.026, MLP 0.0057 rad — the MLP clears all three, but the honest headline is the 4.5× over linear regression, not the 186× over copying. Split-to-split scatter on the MLP number is ~12%.
- Report **relative** and **per-time-step** errors, and check the predicted trajectory's own energy drift, not just MSE.

---

## 4. Suggested staged roadmap

1. **Baseline (done).** MLP on raw classical→quantum vectors, MSE, 80/20 split. Now trained to **early stopping** rather than a fixed epoch count: best validation MSE **1.47e-4** at epoch 1610, train/val gap 4.5×. The old fixed-150-epoch number (9.3e-4) described an under-trained model and was 6.4× worse.
2. **Baselines + metrics (done, 2026-08-13).** All three baselines and the physical-axis plots are in `component3_ml.ipynb` §(e)–(g). RMS in `⟨φ̂⟩`: copy-classical 1.067, k-NN 0.077, linear regression 0.026, MLP 0.0057. The breakdown is located — error climbs 5.2× from well bottom to barrier (ρ=+0.40, p=0.0016). **Linear regression at 0.026 is the finding that should shape stage 3:** most of the in-well map is trivially linear, so the residual is where the remaining signal is.
3. **Features + residual target.** Add physics features (§3.1) and predict the quantum *correction* `B − A` (§3.3). Expect a solid jump.
4. **Sequence/operator model.** Swap the MLP for a 1-D CNN or FNO (§3.2); compare fairly against the MLP on the same data.
5. **Physics-informed loss.** Add energy-conservation penalties (§3.3); check generalization to unseen energies.
6. **Scale + parameter sweep.** Enlarge the dataset and train across a range of fluxonium parameters (§3.4); this is where the *Science* 2022 generalization guarantees kick in.
7. **Write-up.** Characterize the breakdown boundary quantitatively — the scientific result.

Each stage is a self-contained, presentable weekly update (Context → Results → Open Questions).

---

## 5. Practical PyTorch tips for small scientific datasets
- **Standardize** inputs and targets (fit on train only) — done.
- Use **early stopping** on validation loss and a **learning-rate scheduler** (e.g. `ReduceLROnPlateau`).
- Add mild **weight decay** (L2) and, if overfitting, **dropout**.
- With few samples, use **k-fold cross-validation** to get trustworthy error bars rather than a single split.
- Always plot **predicted vs. true trajectories** for a few held-out samples, not just the loss number — the eye catches failure modes MSE hides.
- Fix seeds and log hyperparameters so results are reproducible (group GitHub standard).

---

## 6. References

- Huang, Kueng, Preskill — *Predicting many properties of a quantum system from very few measurements* (classical shadows), Nature Physics 16, 1050 (2020). [Semantic Scholar](https://www.semanticscholar.org/paper/Predicting-many-properties-of-a-quantum-system-from-Huang-Kueng/3986bbdcf8784101bf7a0389948cda48f71ac5f3) · [Caltech record](https://authors.library.caltech.edu/records/wn33r-r8106)
- Huang, Kueng, Torlai, Albert, Preskill — *Provably efficient machine learning for quantum many-body problems*, Science 375 (2022). [Science](https://www.science.org/doi/10.1126/science.abk3333) · [arXiv:2106.12627](https://arxiv.org/abs/2106.12627)
- *Power of data in quantum machine learning*, Nature Communications 12, 2631 (2021). [Nature Communications](https://www.nature.com/articles/s41467-021-22539-9)
- *Emulating quantum dynamics with neural networks via knowledge distillation*, Frontiers in Materials (2022). [Frontiers](https://www.frontiersin.org/journals/materials/articles/10.3389/fmats.2022.1060744/full)
- *Machine learning on quantum experimental data toward solving quantum many-body problems*, Nature Communications (2024). [Nature Communications](https://www.nature.com/articles/s41467-024-51932-3)
- *Fourier Neural Operators for Time-Periodic Quantum Systems: Learning Floquet Hamiltonians, Observable Dynamics, and Operator Growth*, arXiv (2025). [arXiv:2509.07084](https://arxiv.org/pdf/2509.07084)
- Dawid et al. — *Modern applications of machine learning in quantum sciences*, Cambridge University Press (2025). [arXiv:2204.04198](https://arxiv.org/abs/2204.04198) — 287-page pedagogical introduction; the "start here" text.
- Carleo, Cranmer, Hack, Kording, et al. — *Machine learning and the physical sciences*, Rev. Mod. Phys. 91, 045002 (2019). [arXiv:1903.10563](https://arxiv.org/abs/1903.10563)
- Kung, Liu, Lee, Hu, Chang, Chen, Wang, Lin — *Automatic Characterization of Fluxonium Superconducting Qubit Parameters with Deep Transfer Learning* (2025). [arXiv:2503.12099](https://arxiv.org/abs/2503.12099) — ML predicting E_J, E_C, E_L from fluxonium spectra; 95.6% accuracy.
- *Scalable Parameter Design for Superconducting Quantum Circuits with Graph Neural Networks* (2024). [arXiv:2411.16354](https://arxiv.org/abs/2411.16354) — GNNs for circuit parameter design at ~870 qubits; adjacent, not central.
- Ehrenfest-time / quantum-classical correspondence breakdown: [arXiv:nlin/0012048](https://arxiv.org/abs/nlin/0012048) (chaotic systems), [arXiv:1801.06389](https://arxiv.org/abs/1801.06389) (integrable systems — the relevant one here, since Component 1 found no chaos).
- Background methods (widely used, for the architecture upgrades in §3.2–3.3): Fourier Neural Operator (Li et al., arXiv:2010.08895), Neural ODE (Chen et al., arXiv:1806.07366), Hamiltonian Neural Networks (Greydanus et al., arXiv:1906.01563).

*Note: this is a living document. As the group's tools (scqubits, PyTorch) and the tasks evolve, add findings here or split into topic files under `reference/`.*
