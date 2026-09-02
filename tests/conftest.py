"""Shared fixtures. Everything is session-scoped and read-only: the suite inspects the
committed notebooks and recomputes physics from scratch, but never re-runs a notebook
(Component 3 alone takes ~11 minutes) and never writes to the repository."""
from __future__ import annotations

import io
import json
import os
import subprocess

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A1 = os.path.join(REPO, "Assignment 1")
NOTEBOOKS = ("component1_classical.ipynb", "component2_quantum.ipynb", "component3_ml.ipynb")

# Physical parameters, as the notebooks declare them. Kept here so a test that
# disagrees with the notebook fails loudly instead of quietly testing itself.
EC, EJ, EL = 1.0, 5.0, 0.5
PHI_EXT = 3.141592653589793


@pytest.fixture(scope="session")
def repo() -> str:
    return REPO


@pytest.fixture(scope="session")
def a1() -> str:
    return A1


def _load(name: str) -> dict:
    with io.open(os.path.join(A1, name), encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="session")
def notebooks() -> dict[str, dict]:
    """All three notebooks, parsed once."""
    return {n: _load(n) for n in NOTEBOOKS}


@pytest.fixture(scope="session")
def nb_source(notebooks) -> dict[str, str]:
    """Concatenated source of every cell, per notebook."""
    return {n: "".join("".join(c["source"]) for c in d["cells"])
            for n, d in notebooks.items()}


@pytest.fixture(scope="session")
def nb_stdout(notebooks) -> dict[str, str]:
    """Concatenated stream output of every code cell, per notebook.

    This is what makes 'the quoted number is the number that was computed' testable:
    prose claims are checked against the notebook's own captured stdout.
    """
    out = {}
    for n, d in notebooks.items():
        out[n] = "".join(
            "".join(o.get("text", []))
            for c in d["cells"] if c["cell_type"] == "code"
            for o in c.get("outputs", []) if o.get("output_type") == "stream"
        )
    return out


@pytest.fixture(scope="session")
def tracked(repo) -> set[str]:
    """Files git actually tracks, so tests can tell 'in the repo' from 'on my disk'."""
    res = subprocess.run(["git", "ls-files"], cwd=repo, capture_output=True, text=True)
    return {line.strip() for line in res.stdout.splitlines() if line.strip()}


@pytest.fixture(scope="session")
def fluxonium():
    """The fluxonium at half flux, built once (diagonalisation is not free)."""
    scq = pytest.importorskip("scqubits")
    return scq.Fluxonium(EJ=EJ, EC=EC, EL=EL, flux=0.5, cutoff=110)
