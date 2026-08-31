# quantum-research

Predicting expensive **quantum** results from cheap **classical** ones, using ordinary machine
learning. Harmonic-oscillator and fluxonium-qubit simulations plus a PyTorch model that learns the
map between them. (UIC, Mondragon-Shem group.)

**New here? Start with [SETUP.md](SETUP.md)** — environment setup end to end, about ten minutes.
To just read the results, you need nothing: the notebooks are committed with their outputs and
GitHub renders them in the browser.

## The project in three sentences

Component 1 generates classical oscillator trajectories (the model inputs). Component 2 generates
the quantum equivalents, including a real fluxonium qubit (the model targets). Component 3 trains a
neural network to predict the second from the first — and the scientific question is *where*
classical information stops predicting quantum behaviour.

The harmonic oscillator is the testbed because it is exactly solvable both ways, so every number has
an exact formula to check against. That is the working rule throughout: **never trust a numerical
result you cannot check against something external.**

## Repository structure

```
quantum-research/                 repo root
├── README.md                     this file (stays at root so GitHub displays it)
├── SETUP.md                      environment setup, start here to run anything
├── requirements.txt              pinned dependencies (stays at root: `pip install -r requirements.txt`)
├── .gitignore
├── .venv/                        the project's virtual environment (not committed)
├── shared/                       reusable code, importable from any assignment (see shared/README.md)
│   ├── oscillator.py             setup() + physics helpers (energy, hamilton_rhs, build_operators, wigner_gif)
│   ├── group_plot_style.py       group plotting standards: apply_group_style()
│   └── output_routing.py         auto-sort saved files into figures/ data/ movies/: route_outputs()
├── reference/                    project-wide documentation
│   ├── PROJECT_CONTEXT.md        what the project is, conventions, how to run it
│   └── Research_ClassicalToQuantum_ML.md   literature survey + roadmap for the ML side
└── Assignment 1/                 one folder per assignment
    ├── component1_classical.ipynb    Component 1 — classical data (ML inputs)
    ├── component2_quantum.ipynb      Component 2 — quantum data (ML targets)
    ├── component3_ml.ipynb           Component 3 — PyTorch MLP, classical → quantum
    ├── Classical_and_Quantum_Mechanics_Study_Guide.md   companion theory guide
    ├── Code_Walkthrough_Components_1_to_3.md           line-by-line code explanation
    ├── Findings_and_Corrections.md   errors found in review, and how each was caught
    ├── Handout_Compliance.md     every handout requirement mapped to where it is met
    ├── handouts/                 the PI's assignment PDFs
    ├── figures/                  saved plots (auto-created on run)
    ├── data/                     saved .npy data (auto-created on run)
    ├── movies/                   Wigner animations (auto-created on run)
    └── slides/                   meeting deck (.pptx/.pdf) + build_deck.js (regenerates it)
```

## Conventions

- **README.md and requirements.txt live at the repo root** — this is the standard: GitHub renders the root README on the repo page, and `pip install -r requirements.txt` looks there by default.
- **Reusable code goes in `shared/`** and is importable everywhere via a `.pth` entry in the venv (details in `shared/README.md`). Future assignments reuse it without copying.
- **Each assignment is its own folder**, with `figures/`, `data/`, and `movies/` subfolders that the notebooks create and fill automatically.

## Setup

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

Then open a notebook in an assignment folder and run Kernel → Restart and Run All.

Verify the shared helpers on their own at any time:

```powershell
python shared\oscillator.py
```

It checks the classical solver against the exact solution, energy conservation, the
Wigner color scale, and the quantum spectrum against `Eₙ = ℏω(n+½)`. It should print `PASS`.
