# slides/ — Components 1 & 2 meeting deck

- `Components_1_2_Update.pptx` — the meeting deck (Context → Results → Open Questions).
- `Components_1_2_Update.pdf` — PDF copy for quick viewing.
- `assets/` — the figures shown on the slides.
- `make_slide_figures.py` — regenerates `assets/` from the project code.

## Where the slide figures come from

The figures are produced by `make_slide_figures.py`. Each block in that script is the
**same code as the corresponding notebook cell** (`component1_classical.ipynb` /
`component2_quantum.ipynb`) — the same `energy`/`hamilton_rhs` definitions, the same
operator construction, the same `solve_ivp`/QuTiP calls, axis scaling, titles, colors, and
legend positions. Plot styling uses `group_plot_style.py` (`apply_group_style`), exactly as
the notebooks do via `setup()`.

The **only** differences from the notebook figures in `../figures/` are: (1) the short
annotation labels added for the talk, and (2) the output path (`assets/`). So every slide
figure is the same result as its notebook counterpart and traces directly back to the
Component 1 & 2 code.

## Regenerate the figures

With the project `.venv` active:

```
cd "Assignment 1/slides"
python make_slide_figures.py
```

This rewrites `assets/`. (The deck embeds those images, so rebuild/re-export the deck
afterward if the figures change.)
