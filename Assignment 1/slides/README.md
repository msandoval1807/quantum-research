# slides/ — meeting deck

- **`Components_1_3_Update.pptx` — the deck (25 slides).** Component 1 Tasks 1–4, Component 2
  Tasks 1–3, and Component 3's trained, benchmarked classical→quantum model. Structure is
  Context → Results → Open Questions, with full-sentence takeaway titles and one idea per slide.
- **`build_deck.js` — the generator.** `node build_deck.js` rebuilds the deck from scratch, reading
  the current PNGs out of `../figures/`. It contains **no plotting code** and never redraws a figure
  (see below) — it only places the notebook's own output and the slide text.
- `assets/phase_space_explainer.png` — a hand-drawn figure explaining phase space. Not notebook
  output, not currently on a slide; kept because it is useful for explaining the project to someone
  outside the group.

## Where the slide figures come from

Every figure in the deck is the PNG that the notebook wrote, embedded **unmodified** from
`../figures/`. Commentary lives in the slide text rather than being baked into the image.

That is a deliberate change from how the earlier Components 1 & 2 deck worked. That deck used a
`make_slide_figures.py` script which re-plotted each figure with talk annotations — meaning the
repository held **two copies of the plotting code**. They drifted: when the Wigner colour-scale bug
was fixed in `shared/oscillator.py` and `component2_quantum.ipynb`, the slide script still had the
broken version and had to be patched separately. Embedding the notebook output directly removes that
whole class of problem — the image on the slide is byte-for-byte what the notebook produced.

The old deck, its `assets/`, and `make_slide_figures.py` were removed once the 1–3 deck superseded
them. They remain in git history at commit `9e72d54` if ever needed.

Note the distinction from the deleted `make_slide_figures.py`: that script **re-plotted** the
figures, so the repo held two copies of the plotting code. `build_deck.js` only *places* PNGs the
notebooks wrote. Nothing here can drift out of sync with a notebook, because nothing here computes
anything.

## Rebuilding

The deck embeds the current contents of `../figures/`. After re-running a notebook the figures on
disk change but the deck does not — rebuild it to pick them up:

```powershell
cd "~\quantum-research\Assignment 1\slides"; node build_deck.js
```

Requires `pptxgenjs` (`npm install pptxgenjs`). The script prints the slide count when it finishes.

### The PDF

`Components_1_3_Update.pdf` is exported separately — if it is older than the `.pptx`, it is stale.
Easiest path is PowerPoint: File → Export → Create PDF/XPS.

LibreOffice can also do it headlessly, but **this machine's LibreOffice is an MSIX package**, which
adds a wrinkle worth writing down: it lives under `C:\Program Files\WindowsApps\...`, that folder
denies *execution* to non-elevated processes, and the package registers no command-line alias — so
neither `soffice` on PATH nor the full path works, and `shell:AppsFolder\...` fails too. The files
are readable, so the way through is to copy the tree out and run the copy:

```powershell
$src = (Get-AppxPackage -Name *LibreOffice*).InstallLocation + "\VFS\ProgramFilesX64\LibreOffice"
robocopy $src "$env:TEMP\lo" /E /MT:16 | Out-Null
& "$env:TEMP\lo\program\soffice.exe" --headless --norestore --convert-to pdf --outdir . Components_1_3_Update.pptx
```

Takes about 10 seconds to copy (1.5 GB) and a few more to convert.

## Slide map (25 slides)

| # | Content |
|---|---|
| 1–3 | Title · pipeline context · results divider |
| 4–9 | Component 1: energy contours, trajectories, cosine oscillator, coupling, Poincaré + the chaos correction |
| 10–17 | Component 2: operators, spectrum, truncation, Wigner, averages, fluxonium spectrum/dynamics/sweep |
| 18–20 | Component 3: divider, training to early stopping, held-out prediction |
| **21** | **Baselines** — copy-classical / k-NN / linear regression / MLP on the same split |
| **22** | **The null result** — and why the sampling window made it inevitable |
| **23** | **The breakdown** — error against distance to the barrier, the headline result |
| 24–25 | Verification · open questions |

Slides 21–23 are new in the 2026-08-13 rebuild; 19 and 20 were rewritten for the early-stopping
results. Slides 1–17 are unchanged in content — the Component 1 and 2 figures did not change.
