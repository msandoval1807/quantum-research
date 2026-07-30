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
- **Ehrenfest / correspondence prior — now well motivated.** Ehrenfest's theorem gives `d⟨p⟩/dt = ⟨−∂V/∂x⟩`, the average of the force, which equals the classical force at the average position *only for a harmonic potential*. Everything the network has to learn is that discrepancy. So train it to predict the **residual** `B − A` (the quantum correction) rather than `B` from scratch: the residual is literally the term Ehrenfest discards, which makes it both easier to learn and physically interpretable. Measured size of that residual in the current dataset: RMS ≈ 1.02 rad, rising from 0.84 near the well minimum to 1.19 at the edge of the sampled window.

### 3.4 Data and sampling strategy
- **Scale the dataset** (more samples than the current 300) and, per the *Science* 2022 result, sample across a **range of parameters** (`E_J/E_C`, `E_L/E_C`, flux) so the model learns a family, not one point.
- **Curriculum learning** (from the knowledge-distillation paper): start with easy, near-harmonic initial conditions, then add strongly nonlinear / near-barrier ones.
- **Targeted sampling of the breakdown region.** Deliberately oversample initial conditions near the flux sweet spot / barrier where classical–quantum divergence is largest — that is where the model (and the science) is most tested.
- Keep a proper **train / validation / test** split, and standardize inputs and targets (already done).

### 3.5 Quantifying the classical→quantum breakdown (the actual science)
This is the project's real deliverable, not just a low validation loss:
- Plot **prediction error vs. a physical axis** — initial energy, or distance of `φ₀` from the well minimum at `φ ≈ 2.85` (the barrier sits at `φ = 0`; see `Findings_and_Corrections.md` §1 for why the coordinate matters). The error should stay low in the near-classical regime and rise where quantum effects dominate.
- Compare against **honest baselines**: linear regression, k-nearest-neighbors, and "just copy the classical trajectory" (`B̂ = A`). The MLP must beat all three to be meaningful. The copy-classical baseline is already quantified — RMS 1.02 rad in φ — so that number is the bar to clear.
- Report **relative** and **per-time-step** errors, and check the predicted trajectory's own energy drift, not just MSE.

---

## 4. Suggested staged roadmap

1. **Baseline (done).** MLP on raw classical→quantum vectors, MSE, 80/20 split. Validation MSE **9.3e-4** (standardized), train/val gap 1.7×, still falling at epoch 150 — so the model is under-trained and more epochs is the cheapest next experiment.
2. **Baselines + metrics.** Add linear-regression / nearest-neighbor / copy-classical baselines and the physical-axis error plots (§3.5). This immediately shows whether learning is happening and where it fails.
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
- Background methods (widely used, for the architecture upgrades in §3.2–3.3): Fourier Neural Operator (Li et al., arXiv:2010.08895), Neural ODE (Chen et al., arXiv:1806.07366), Hamiltonian Neural Networks (Greydanus et al., arXiv:1906.01563).

*Note: this is a living document. As the group's tools (scqubits, PyTorch) and the tasks evolve, add findings here or split into topic files under `reference/`.*
