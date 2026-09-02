"""Does the work still meet the handout, and is the repository internally consistent?

The cross-artifact checks here exist because every one of them caught something real. Each
compares two *different* artifacts — the notebooks against the handout, the figures against
the deck generator, the prose against the executed output. Checks that only look inside one
artifact pass happily while two artifacts drift apart.
"""
from __future__ import annotations

import io
import os
import re

import pytest

# quantum_researcher 4.pdf, parsed from the PDF itself during the 2026-08-30 audit.
REQUIRED = {
    ("component1_classical.ipynb", 1): "abc",
    ("component1_classical.ipynb", 2): "ab",
    ("component1_classical.ipynb", 3): "abc",
    ("component1_classical.ipynb", 4): "abcd",
    ("component2_quantum.ipynb", 1): "abc",
    ("component2_quantum.ipynb", 2): "abcde",
    ("component2_quantum.ipynb", 3): "abcdef",
    ("component3_ml.ipynb", 1): "abcd",
}


def _headers(nb):
    return [ln.strip() for c in nb["cells"] if c["cell_type"] == "markdown"
            for ln in "".join(c["source"]).splitlines() if ln.strip().startswith("#")]


@pytest.mark.parametrize("key", sorted(REQUIRED), ids=lambda k: f"{k[0][9:11]}-task{k[1]}")
def test_every_subtask_has_a_visible_header(key, notebooks):
    """The PI grades the rendered notebook, not the source.

    Three sub-tasks once existed only as `# (b)` comments inside code cells: the work was
    there and correct, but a reader saw (a) -> figure -> (c).
    """
    name, task = key
    hdrs = _headers(notebooks[name])
    if name != "component3_ml.ipynb":
        start = next(i for i, h in enumerate(hdrs) if re.match(rf"^# Task {task}\b", h))
        after = [i for i, h in enumerate(hdrs) if re.match(r"^# Task \d", h) and i > start]
        hdrs = hdrs[start: after[0] if after else len(hdrs)]
    found = set()
    for h in hdrs:
        found |= set(re.findall(r"\(([a-h])(?:\s*continued)?[,)]", h + ")"))
        for grp in re.findall(r"\(([a-h](?:\s*,\s*[a-h])+)\)", h):
            found |= set(re.findall(r"[a-h]", grp))
    missing = [L for L in REQUIRED[key] if L not in found]
    assert not missing, f"{name} Task {task}: no visible header for {missing}"


def test_notebooks_are_fully_executed(notebooks):
    """A committed notebook with an unrun cell is a claim nobody checked."""
    for name, nb in notebooks.items():
        code = [c for c in nb["cells"] if c["cell_type"] == "code"]
        unrun = [i for i, c in enumerate(code) if c.get("execution_count") is None]
        errors = [i for i, c in enumerate(code)
                  if any(o.get("output_type") == "error" for o in c.get("outputs", []))]
        assert not unrun, f"{name}: unrun code cells at {unrun}"
        assert not errors, f"{name}: error output in cells {errors}"


def test_every_figure_has_a_caption(notebooks, a1):
    """The handout: 'Every figure needs a caption that explains what is shown and what the
    key takeaway is.'"""
    missing = []
    for name, nb in notebooks.items():
        cells = nb["cells"]
        for i, c in enumerate(cells):
            if c["cell_type"] != "code":
                continue
            for m in re.finditer(r'savefig\("([^"]+\.png)"', "".join(c["source"])):
                nearby = [j for j in range(i + 1, min(i + 4, len(cells)))
                          if cells[j]["cell_type"] == "markdown"
                          and "Figure caption" in "".join(cells[j]["source"])]
                if not nearby:
                    missing.append(f"{name}:{m.group(1)}")
    assert not missing, f"figures without a caption: {missing}"


def test_every_declared_figure_exists(notebooks, a1):
    declared, missing = set(), []
    for nb in notebooks.values():
        for c in nb["cells"]:
            for m in re.finditer(r'savefig\("(?:figures/)?([^"]+\.png)"', "".join(c["source"])):
                declared.add(m.group(1))
    for f in sorted(declared):
        if not os.path.exists(os.path.join(a1, "figures", f)):
            missing.append(f)
    assert declared, "no figures declared at all - the parser is broken"
    assert not missing, f"declared but not on disk: {missing}"


def test_no_figure_is_orphaned_from_the_deck(a1):
    """A figure produced by a notebook and used on no slide is usually an oversight.

    One is deliberate and documented in Handout_Compliance.md deviation 7; it is named here
    so a *second* orphan fails the suite.
    """
    ALLOWED = {"fig_c3_prediction_vs_true.png"}
    js = io.open(os.path.join(a1, "slides", "build_deck.js"), encoding="utf-8").read()
    used = {os.path.basename(m) for m in re.findall(r"[\w./-]+\.png", js)}
    import glob
    have = {os.path.basename(f) for f in glob.glob(os.path.join(a1, "figures", "*.png"))}
    orphans = have - used - ALLOWED
    assert not orphans, f"produced by a notebook but on no slide: {sorted(orphans)}"
    ghosts = {u for u in used if u.endswith(".png")} - have
    assert not ghosts, f"the deck references figures that do not exist: {sorted(ghosts)}"


QUOTED = [
    ("copy-classical baseline", r"copy-classical\s+1\.0666"),
    ("linear regression baseline", r"linear regression\s+0\.0259"),
    ("MLP result", r"MLP \(early-stopped\)\s+0\.0057"),
    ("well minimum", r"well minimum at phi = 2\.85"),
    ("barrier height", r"barrier height above the well = 7\.758"),
    ("energy drift", r"Total energy drift: 1\.9\de-09"),
    ("solver vs analytic", r"deviation = 6\.7\de-09"),
    ("truncation agreement", r"cutoff=80 agrees with cutoff=110 to 8\.\de-07"),
]


@pytest.mark.parametrize("label,pattern", QUOTED, ids=[q[0] for q in QUOTED])
def test_quoted_numbers_trace_back_to_executed_output(label, pattern, nb_stdout):
    """Every headline number must appear in a notebook's own captured stdout.

    Prose drifts from code silently; this is the check that catches it.
    """
    blob = "".join(nb_stdout.values())
    assert re.search(pattern, blob), f"{label}: no executed output matches /{pattern}/"
