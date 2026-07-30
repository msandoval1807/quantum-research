# slides/ — meeting deck

- **`Components_1_3_Update.pptx` / `.pdf` — the deck (23 slides).** Component 1 Tasks 1–4,
  Component 2 Tasks 1–3, and Component 3's trained classical→quantum model. Structure is
  Context → Results → Open Questions, with full-sentence takeaway titles and one idea per slide.
- **`Meeting_Script.md`** — speaking notes, one block per slide: the point to land, the numbers to
  have ready, and which slides to drop if running long. Also lists the questions to expect.
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

## Rebuilding

The deck embeds the current contents of `../figures/`. After re-running a notebook, the figures on
disk change but the deck does not — it has to be rebuilt to pick them up.
