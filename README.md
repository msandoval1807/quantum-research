# quantum-research

Harmonic oscillator simulations, classical and quantum (UIC Mondragon-Shem group).

## Repository structure

```
quantum-research/                 repo root
├── README.md                     this file (stays at root so GitHub displays it)
├── requirements.txt              pinned dependencies (stays at root: `pip install -r requirements.txt`)
├── .gitignore
├── .venv/                        the project's virtual environment (not committed)
├── shared/                       reusable code, importable from any assignment (see shared/README.md)
│   ├── oscillator.py             setup() + physics helpers (energy, hamilton_rhs, build_operators, wigner_gif)
│   ├── group_plot_style.py       group plotting standards: apply_group_style()
│   └── output_routing.py         auto-sort saved files into figures/ data/ movies/: route_outputs()
└── Assignment 1/                 one folder per assignment
    ├── component1_classical.ipynb
    ├── component2_quantum.ipynb
    ├── Classical_and_Quantum_Mechanics_Study_Guide.md   companion theory guide
    ├── Code_Walkthrough_Components_1_and_2.md           line-by-line code explanation
    ├── figures/                  saved plots (auto-created on run)
    ├── data/                     saved .npy data (auto-created on run)
    ├── movies/                   Wigner animations (auto-created on run)
    └── slides/                   meeting deck (.pptx/.pdf), assets/, make_slide_figures.py
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
