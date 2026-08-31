/* build_deck.js — regenerate Components_1_3_Update.pptx from the notebook figures.
 *
 *   cd "Assignment 1/slides" && node build_deck.js
 *
 * Every image is the PNG the notebook wrote, embedded UNMODIFIED from ../figures/.
 * This script contains no plotting code and never redraws a figure — that separation is
 * deliberate (see README.md: an older make_slide_figures.py re-plotted the figures with
 * annotations, drifted out of sync with the notebooks, and had to be patched separately
 * when a plotting bug was fixed). Commentary belongs in the slide text, not in the image.
 */
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const FIG = "../figures";
const OUT = "Components_1_3_Update.pptx";

// ---- palette (matches the previous deck: UIC navy + teal accent) -----------------
const NAVY = "0B1F3A", INK = "16202E", MUTED = "5C6B7A", TEAL = "2EC4B6",
      DEEP = "1C7293", CARD = "E8EEF7", MINT = "EAF6F4", WHITE = "FFFFFF", RED = "B23A48";
const SERIF = "Georgia", SANS = "Calibri";
const FOOT = "AI Design of Quantum Processors  ·  Components 1–3";

// PNG dimensions straight from the IHDR header — avoids an image-size dependency.
function png(file) {
  const b = fs.readFileSync(path.join(FIG, file));
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), p: path.join(FIG, file) };
}
// Fit an image inside a box, preserving aspect ratio, centred.
function fit(im, bx, by, bw, bh) {
  const s = Math.min(bw / im.w, bh / im.h);
  const w = im.w * s, h = im.h * s;
  return { path: im.p, x: bx + (bw - w) / 2, y: by + (bh - h) / 2, w, h };
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";          // 13.3 x 7.5 — must be set before any slide
pres.author = "Marcos Sandoval Lucas";
pres.title = "AI Design of Quantum Processors — Components 1-3";

let pageNo = 0;
function chrome(s) {                   // footer + page number
  pageNo++;
  if (pageNo === 1) return;
  s.addText(FOOT, { x: 0.6, y: 7.0, w: 9.0, h: 0.3, fontFace: SANS, fontSize: 9, color: MUTED });
  s.addText(String(pageNo), { x: 12.4, y: 7.0, w: 0.4, h: 0.3, fontFace: SANS, fontSize: 9,
                              color: MUTED, align: "right" });
}
function eyebrow(s, t) {
  s.addText(t.toUpperCase(), { x: 0.9, y: 0.3, w: 6.0, h: 0.4, fontFace: SANS, fontSize: 12,
                               bold: true, color: TEAL, charSpacing: 1.5 });
}
function title(s, t) {
  s.addText(t, { x: 0.9, y: 0.85, w: 11.9, h: 1.05, fontFace: SERIF, fontSize: 23,
                 color: NAVY, valign: "top", margin: 0 });
}
function bullets(s, items, x, y, w, h) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })),
    { x, y, w, h, fontFace: SANS, fontSize: 13, color: INK, lineSpacing: 19, paraSpaceAfter: 9, valign: "top" });
}
function takeaway(s, t, y, h) {
  h = h || 1.25;
  s.addShape(pres.ShapeType.roundRect, { x: 0.9, y, w: 11.5, h, fill: { color: MINT },
                                         line: { color: MINT }, rectRadius: 0.06 });
  s.addText([{ text: "Takeaway:  ", options: { bold: true, color: DEEP } }, { text: t, options: { color: INK } }],
    { x: 1.15, y: y + 0.12, w: 11.0, h: h - 0.24, fontFace: SANS, fontSize: 12.5, valign: "top", margin: 0 });
}
// Speaker notes. Two lines per slide: what the picture literally is, and why the slide
// exists. These show in Presenter View while presenting.
const NOTES = {};
function note(s, key) { if (NOTES[key]) s.addNotes(NOTES[key]); }

// figure left, "what it shows" bullets right
function formula(s, eq, x, y, w) {          // the governing equation, stated on the slide
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.42, fill: { color: "F4F7FC" },
                                         line: { color: "F4F7FC" }, rectRadius: 0.04 });
  s.addText(eq, { x: x + 0.1, y: y + 0.02, w: w - 0.2, h: 0.38, fontFace: "Cambria",
                  fontSize: 13.5, italic: true, color: NAVY, align: "center",
                  valign: "middle", margin: 0 });
}
function figureSlide(eb, ti, file, items, nk, eq) {
  const s = pres.addSlide();
  eyebrow(s, eb); title(s, ti);
  if (eq) { formula(s, eq, 0.9, 2.06, 6.6); s.addImage(fit(png(file), 0.9, 2.6, 6.6, 3.95)); }
  else    { s.addImage(fit(png(file), 0.9, 2.15, 6.6, 4.4)); }
  s.addText("WHAT IT SHOWS", { x: 8.2, y: 2.1, w: 4.3, h: 0.3, fontFace: SANS, fontSize: 10.5,
                               bold: true, color: TEAL, charSpacing: 1.2 });
  bullets(s, items, 8.2, 2.55, 4.3, 4.1);
  note(s, nk); chrome(s); return s;
}
// wide figure with a takeaway bar underneath
function wideSlide(eb, ti, file, tk, nk, eq) {
  const s = pres.addSlide();
  eyebrow(s, eb); title(s, ti);
  if (eq) { formula(s, eq, 0.9, 2.0, 11.5); s.addImage(fit(png(file), 0.9, 2.5, 11.5, 3.1)); }
  else    { s.addImage(fit(png(file), 0.9, 2.05, 11.5, 3.5)); }
  takeaway(s, tk, 5.75);
  note(s, nk); chrome(s); return s;
}
function divider(label, big, sub) {
  const s = pres.addSlide();
  s.background = { color: NAVY };
  if (label) s.addText(label.toUpperCase(), { x: 0.9, y: 2.7, w: 8, h: 0.4, fontFace: SANS,
                                              fontSize: 12, bold: true, color: TEAL, charSpacing: 1.8 });
  s.addText(big, { x: 0.9, y: 3.2, w: 11.0, h: 1.1, fontFace: SERIF, fontSize: 40, color: WHITE });
  s.addText(sub, { x: 0.9, y: 4.4, w: 10.5, h: 1.0, fontFace: SANS, fontSize: 15, color: CADCFC_SAFE() });
  chrome(s); return s;
}
function CADCFC_SAFE() { return "CADCFC"; }
// three or four big stat callouts in a row
// `sub` is an optional line between title and cards. It exists because the baselines slide
// failed in front of the PI: four numbers with four unfamiliar names, and nothing on the
// slide saying these are deliberately-simple yardsticks rather than four things I built.
function statSlide(eb, ti, stats, tk, nk, th, sub) {
  const s = pres.addSlide();
  eyebrow(s, eb); title(s, ti);
  if (sub) s.addText(sub, { x: 0.9, y: 1.90, w: 11.5, h: 0.66, fontFace: SANS, fontSize: 12.5,
                            color: MUTED, valign: "top", margin: 0 });
  const dy = sub ? 0.34 : 0;   // keeps the takeaway bar clear of the footer at y = 7.0
  const n = stats.length, gap = 0.3, w = (11.5 - gap * (n - 1)) / n;
  stats.forEach((st, i) => {
    const x = 0.9 + i * (w + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y: 2.3 + dy, w, h: 2.5, fill: { color: st.hi ? MINT : CARD },
                                           line: { color: st.hi ? TEAL : CARD }, rectRadius: 0.06 });
    s.addText(st.value, { x: x + 0.15, y: 2.5 + dy, w: w - 0.3, h: 0.95, fontFace: SERIF,
                          fontSize: st.value.length > 7 ? 30 : 38, bold: true,
                          color: st.hi ? DEEP : NAVY, align: "center", margin: 0 });
    s.addText(st.label.toUpperCase(), { x: x + 0.15, y: 3.5 + dy, w: w - 0.3, h: 0.32, fontFace: SANS,
                                        fontSize: 10.5, bold: true, color: st.hi ? DEEP : TEAL,
                                        align: "center", charSpacing: 1, margin: 0 });
    s.addText(st.note, { x: x + 0.15, y: 3.85 + dy, w: w - 0.3, h: 0.85, fontFace: SANS, fontSize: 11,
                         color: MUTED, align: "center", valign: "top", margin: 0 });
  });
  takeaway(s, tk, 5.15 + dy, th);
  note(s, nk); chrome(s); return s;
}

Object.assign(NOTES, {
  pipeline: "LOOKING AT: three boxes = the three components, left to right. Classical data in, quantum data as the answer, ML learning the map.\nWHY: this is the map for the whole talk. Without it the next 20 slides are unconnected figures.\nSAY: classical is cheap, quantum is expensive, the model predicts the second from the first. NOT quantum computing speeding up AI — the reverse.",
  contours: "LOOKING AT: phase space. Horizontal = position, vertical = momentum. Colour = total energy. White rings = constant energy.\nA point on this plot is the complete state: where it is AND how it moves. Energy conservation means it can only travel ALONG a ring, never hop between them.\nWHY: establishes that a classical state is a point living on a ring.",
  singletraj: "LOOKING AT: blue = what my code computed. White dashed = the exact pen-and-paper answer, sitting on top of it. Red dot = the start.\nWHY: proof-of-correctness, not physics. Later systems have no exact answer, so the solver has to be verified HERE.\nNUMBER: agrees to 6.7e-9.",
  manytraj: "LOOKING AT: 12 orbits from random starts, coloured by energy. Bigger ring = more energy. They never cross.\nWHY: this IS the training dataset (classical_trajectories.npy).\nIF ASKED why they never cross: a phase-space point determines the future uniquely, so a crossing would give one point two futures.",
  cosine: "LOOKING AT: orbits at several energies. Low energy still looks elliptical; high energy is visibly deformed.\nWHY: the bridge from toy spring to real hardware.\nSAY: anharmonicity is what makes a qubit addressable. Evenly spaced levels mean a pulse driving 0->1 also drives 1->2; bending the potential breaks that.",
  band: "LOOKING AT: many orbits launched in a NARROW energy band (2.0 +/- 0.5), coloured by energy. They nest like tree rings and never cross.\nWHY: this is the assumption Component 3 is built on. A small change in the classical input gives a small change in the orbit — so a smooth classical->quantum map can exist at all. If these scattered, the whole project would be ill-posed.\nIF ASKED: crossing orbits at the SAME energy would be a signature of chaos. They don't cross.",
  projections: "LOOKING AT: four 2-D shadows of a 4-D motion — two coupled oscillators need four numbers, which can't be drawn.\nWHY: sets up the next two slides. Weakest slide in the deck; drop it first if short.",
  projections_e: "LOOKING AT: the same four projections repeated at E0 = 1, 3, 12 — one row per energy.\nWHY: the handout asks how the projections change with energy. The region grows, fastest in (p1,p2) because the coupling acts through the momenta — but nothing scatters.\nSAY: this is the first hint that my chaos expectation was wrong; the Poincare slide measures it.",
  band2: "LOOKING AT: the energy-band idea from Task 3(c), now with TWO oscillators (E = 3.0 +/- 0.5).\nEach oscillator fills a band whose size grows with its share of the energy.\nWHY: the smooth layered structure survives coupling. The two are correlated, not independent — the momentum coupling passes energy back and forth.\nCuttable if short; it repeats the Task 3(c) message.",
  poincare: "LOOKING AT: state recorded ONLY when it crosses a chosen surface, always the same direction. Smooth curves = regular motion. A scattered cloud would mean chaos.\nWHY: FIRST CORRECTION. I claimed chaos at high energy; measuring the Lyapunov exponent says regular at every energy (~0.005 = zero).\nWHY I WAS WRONG: the nonlinearity is a bounded cosine, the harmonic term is not — so MORE energy makes it MORE nearly harmonic. Intuition was backwards.",
  operators: "LOOKING AT: three matrices drawn as heatmaps. Bright = large, dark = zero. Row/column = energy level.\nH is bright only on the diagonal (each level has a definite energy). x and p are bright only just off the diagonal (they connect a level ONLY to its neighbours).\nWHY: that off-diagonal stripe IS the ladder structure, made visible.",
  spectrum: "LOOKING AT: red line = the exact formula E_n = hbar*omega*(n+1/2). Blue circles = what my code computed, sitting on it.\nWHY: shows energy is quantized AND verifies the code.\nTWO FEATURES: evenly spaced (quantization), and the lowest sits at 0.5 not 0 (zero-point energy — it can't sit still, uncertainty forbids it).\nThe drift at high n is truncation, not error — next slide.",
  convergence: "LOOKING AT: how wrong each energy level is, log scale, for three basis sizes N.\nWHY: the honest footnote to the previous slide. The error is a flat plateau at EXACTLY 1.000, not a growing drift: truncation makes one spurious eigenvalue at (N-1)/2, and sorting shifts every level above it down one rung. So the lowest ceil((N-1)/2) levels are exact - 5 of 10, 15 of 30, 25 of 50.\nSAY: raise N until the numbers you care about stop moving. Cuttable if short.",
  wigner: "LOOKING AT: quantum states drawn in the SAME position-momentum plane as slide 4. Red = positive, blue = NEGATIVE.\nWHY: a real probability can never be negative — so blue means no classical explanation exists.\nPANELS: coherent (right) = one positive blob, most classical, this is what I use for the ML. Fock (left) = negative crater. Superposition (middle) = interference stripes, proof it is genuinely in two states at once.",
  averages: "LOOKING AT: thick red = the classical orbit. Blue dashed = the AVERAGE position/momentum of the quantum state. On the right they lie exactly on top of each other.\nWHY: this is the baseline that slide 20 breaks — the two slides are a pair.\nSAY: for a coherent state the quantum average traces the classical orbit exactly. That is Ehrenfest's theorem. BUT averaging throws away the spread and interference the previous slide showed.",
  fluxspec: "LOOKING AT: a real superconducting qubit. W-shaped curve = potential energy. Horizontal axis is phi, a magnetic PHASE (an angle, not a distance). Two wells at +/-2.85, barrier between them at 0.\nWHY: the step from toy problem to real hardware.\nSAY: the two lowest levels are split by only 0.134 E_C while the next is 4.6 away — factor of 34. That tiny splitting IS tunnelling through the barrier, and has no classical counterpart.",
  fluxdyn: "*** MOST IMPORTANT SLIDE. SLOW DOWN. ***\nLOOKING AT: classical and quantum, same start, plotted against time. They agree until t~0.7, then the quantum one loses amplitude.\nWHY: everything in Act 3 exists because of this gap. If these curves stayed together there'd be nothing to learn.\nTHE EXPLANATION: Ehrenfest says d<p>/dt = the AVERAGE OF THE FORCE. The classical equation uses the FORCE AT THE AVERAGE POSITION. Those agree only if the force is a straight line — i.e. only for a parabola. The fluxonium's force has a sine in it, and <sin phi> is not sin<phi>. So these averages obey NO classical equation.\nThat one fact explains why slide 18 agreed exactly, why this one doesn't, and why the network has anything to learn.\nALSO: this is where the coordinate-convention bug was — classical and quantum written half a flux quantum apart.",
  sweep: "LOOKING AT: five starting phases, one well across the barrier to the other. The MIDDLE panel is the striking one.\nOn the barrier top the classical point sweeps a figure-eight through both wells; the quantum packet splits and stays put.\nWHY: visual climax of Act 2 — same initial condition, completely different answers. That gap is what Component 3 must learn.",
  losscurve: "LOOKING AT: purple = error on data it learned from. Blue = error on data it has NEVER seen (the honest score). Red dotted = where I used to stop (150). Grey dashed = where blue actually bottoms out (1610).\nWHY: shows the model is properly trained now, and how badly the old version under-trained.\nHE WILL ASK: 'the gap got worse, 1.7x to 4.5x — isn't that overfitting?' ANSWER: partly, but validation itself improved 6.4x at the same time. Gap widening while the honest score improves is the expected trade.\nThe spikes are the optimizer; they recover and never beat the minimum.",
  prediction: "*** THIS SLIDE ANSWERS THE QUESTION HE ASKED LAST TIME: how do I know what is real? ***\nSAY THIS FIRST: the blue curve is the truth in both left panels. It comes from solving the Schrodinger equation and never from the model, so the model cannot flatter it.\nTHEN: both panels are the SAME window with the SAME blue curve. Only what it is compared against changes. (a) vs the classical INPUT: a visibly different loop, 1.067 rad away. (b) vs the model OUTPUT: no visible gap.\nTHAT is why Component 2 and Component 3 look like they contradict each other and do not. Two different gaps, one truth.\n(c) EXISTS BECAUSE A GAP YOU CANNOT SEE IS INDISTINGUISHABLE FROM NO GAP. Subtract (b), plot in milliradians, 186x finer: the error is real and structured, not noise.\nTHE LINK TO THE NEXT SLIDE: panel (a) IS the copy-classical baseline. 1.067 rad is the same number, drawn as a picture instead of quoted. If the network were passing its input through it would score panel (a); it scores panel (b).\nIF ASKED whether this is a lucky trajectory: it is the MEDIAN of the held-out set. Best / median / worst are 1.8 / 4.3 / 20.9 mrad.",
  nullresult: "LOOKING AT: error vs how far the packet started from the well bottom. Four FLAT lines.\nPhysics says this should slope up. It doesn't.\nWHY: THIRD CORRECTION, and the subtlest.\nTWO STEPS: (1) I first titled this 'error grows with distance' because that's what I expected and saw; measuring it gave rho=0.08, p=0.56 — no trend, so I retitled. (2) But 'no trend' wasn't the story either: the barrier is 2.85 rad away and I only sampled to 1.0 — a third of the way. The breakdown region was never in my data.\nSAY: a null from a measurement that couldn't have detected the effect is not evidence of absence.",
  breakdown: "*** THE HEADLINE RESULT ***\nLOOKING AT: same axes as the last slide but the lines now clearly RISE. Shaded band on the left = the entire range the previous slide covered (which is why it saw nothing). Dashed line right = the barrier top.\nWHY: this is what the whole project was building toward.\nTWO NUMBERS: the network's error climbs 5.2x (rho=+0.40, p=0.0016). Copy-classical climbs 2.4x (rho=+0.86) — and THAT one isn't about my model at all, it's the size of the quantum correction itself growing. A direct measurement of where classical and quantum part company.\nNUANCE: the network degrades fastest in relative terms while staying most accurate — its advantage is biggest where the physics is easiest.\nIF ASKED about numerics out there: checked, not assumed — bigger basis agrees to 8e-7 rad.",
  baselines: "*** THIS SLIDE DID NOT LAND LAST TIME. LEAD WITH THE FRAMING, NOT THE NUMBERS. ***\nOPEN WITH THIS, BEFORE ANY NUMBER: 'Only the last box is a neural network. The other three are deliberately dumb methods I ran on the identical task, so that my number has a scale. They are yardsticks, not things I am proposing.'\nTHEN: same job for all four \u2014 given a classical trajectory, predict the quantum one. Same 60 held-out trajectories. Radians. Lower is better.\nTHEN walk left to right: 1.067 = hand the input straight back, no model at all (this number IS the size of the quantum correction \u2014 how wrong you are ignoring quantum mechanics). 0.077 = reuse the answer from the most similar training case. 0.026 = one straight-line formula, no training. 0.0057 = the trained network.\nWHY THE SLIDE EXISTS: last time I reported a loss number with nothing to compare it against, which is not a result.\nSAY THIS BEFORE HE DOES: the comparison that counts is 4.5x over the STRAIGHT-LINE FIT, not 186x over copying. Inside one well the motion is near-harmonic, and for a harmonic potential the classical->quantum map really IS linear (slide 18) \u2014 so a straight line already gets most of the way. The network's job is the nonlinear remainder.\nIF HE ASKS FOR THE STANDARD NAMES: box 2 is k-nearest-neighbours (k=1), box 3 is ordinary least-squares linear regression, box 4 is a multi-layer perceptron - 2 hidden layers, ReLU. I kept them off the slide deliberately; the plain descriptions are what made it readable.\nIF ASKED how solid: a different random split moves the MLP number ~12%, so do not defend the last digit.",
  openq: "Two to lead with: (1) is the model learning physics or interpolating? Linear regression reaching 0.026 makes that sharper — most of the in-well map is trivially linear. (2) Should the target be a trajectory at all, or something with no classical analogue like the tunnelling splitting?\nCLOSE on the italic line: which fluxonium property is actually worth predicting for real device design. That is genuinely his call and it shapes the next month.",
  verification: "LOOKING AT: three checks against things with exact answers — spectrum vs formula, energy conservation, basis-size cross-check.\nWHY: the credibility slide, and where all three corrections are listed together.\nTHE LINE TO LAND: none of the three errors raised an error message. The code ran fine and the figures looked plausible every time. A figure is a picture, not a measurement.",
});

/* ======================= 1 — title ======================= */
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText("AI Design of Quantum Processors",
    { x: 0.9, y: 2.2, w: 11.0, h: 1.4, fontFace: SERIF, fontSize: 40, color: WHITE });
  s.addText("Components 1–3 — from classical and quantum data to a trained classical→quantum model",
    { x: 0.9, y: 3.7, w: 10.5, h: 0.8, fontFace: SANS, fontSize: 16, color: "CADCFC" });
  s.addShape(pres.ShapeType.rect, { x: 0.9, y: 4.75, w: 1.6, h: 0.035, fill: { color: TEAL }, line: { color: TEAL } });
  s.addText([{ text: "Marcos Sandoval Lucas\n", options: { bold: true, color: WHITE, fontSize: 15 } },
             { text: "Mondragon-Shem Quantum Group · UIC College of Engineering", options: { color: "8FA6C4", fontSize: 13 } }],
    { x: 0.9, y: 5.4, w: 9.0, h: 1.0, fontFace: SANS, valign: "top" });
  chrome(s);
}

/* ======================= 2 — context ======================= */
{
  const s = pres.addSlide();
  eyebrow(s, "Context");
  title(s, "We test whether classical data can predict quantum properties — first on the exactly-solvable oscillator, now on a real fluxonium qubit.");
  const cards = [
    ["Component 1", "Classical data", "Phase-space orbits & energies — the model INPUTS"],
    ["Component 2", "Quantum data", "Spectra and Wigner functions; the ⟨φ̂⟩,⟨n̂⟩ trajectories are the model TARGETS"],
    ["Component 3", "Machine learning", "Trained, benchmarked, and measured against a physical axis"],
  ];
  cards.forEach((c, i) => {
    const x = 1.05 + i * 4.2;
    s.addShape(pres.ShapeType.roundRect, { x, y: 2.65, w: 3.5, h: 2.2, fill: { color: CARD },
                                           line: { color: CARD }, rectRadius: 0.06 });
    s.addText(c[0].toUpperCase(), { x: x + 0.25, y: 2.85, w: 3.0, h: 0.3, fontFace: SANS, fontSize: 10.5,
                                    bold: true, color: TEAL, charSpacing: 1, margin: 0 });
    s.addText(c[1], { x: x + 0.25, y: 3.2, w: 3.0, h: 0.4, fontFace: SERIF, fontSize: 17, color: NAVY, margin: 0 });
    s.addText(c[2], { x: x + 0.25, y: 3.7, w: 3.0, h: 1.0, fontFace: SANS, fontSize: 11.5, color: MUTED, valign: "top", margin: 0 });
    if (i < 2) s.addText("→", { x: x + 3.55, y: 3.4, w: 0.6, h: 0.5, fontFace: SANS, fontSize: 22, color: TEAL, align: "center" });
  });
  s.addShape(pres.ShapeType.roundRect, { x: 0.9, y: 5.25, w: 7.2, h: 1.2, fill: { color: MINT }, line: { color: MINT }, rectRadius: 0.06 });
  s.addText([{ text: "Central question:  ", options: { bold: true, color: DEEP } },
             { text: "how much of a quantum system can be predicted from classical information alone — and where does that prediction break down?", options: { color: INK } }],
    { x: 1.15, y: 5.42, w: 6.7, h: 0.95, fontFace: SANS, fontSize: 12.5, valign: "top", margin: 0 });
  s.addShape(pres.ShapeType.roundRect, { x: 8.4, y: 5.25, w: 4.0, h: 1.2, fill: { color: CARD }, line: { color: CARD }, rectRadius: 0.06 });
  s.addText([{ text: "Why this system?\n", options: { bold: true, color: NAVY } },
             { text: "The harmonic oscillator is exactly solvable in both worlds — every number has a built-in answer key.", options: { color: MUTED } }],
    { x: 8.65, y: 5.42, w: 3.5, h: 0.95, fontFace: SANS, fontSize: 11.5, valign: "top", margin: 0 });
  note(s, "pipeline"); chrome(s);
}

/* ======================= 3 — results divider ======================= */
divider("Results · part 1 of 3", "Component 1 — Classical data",
  "The cheap side of the pipeline: phase-space orbits and energies for the harmonic, anharmonic and "
  + "coupled oscillators — the model INPUTS. Every result is checked against an exact formula.");

/* ======================= 4–9 — Component 1 ======================= */
figureSlide("Component 1 · Task 1(a, c)",
  "Constant-energy contours are closed elliptical orbits in phase space.",
  "fig_c1_energy_contours.png", [
  "Colour is total energy E(x,p); white rings are constant-energy curves.",
  "Each ring is one allowed classical orbit — the system is locked onto it.",
  "In natural units the ellipses become circles; larger energy = larger ring.",
  "This map defines the classical states the ML model draws its inputs from.",
], "contours", "E(x, p)  =  p²/2m  +  ½ mω²x²          —  the classical energy (Task 1a)");

figureSlide("Component 1 · Task 1(b) + 2(a)",
  "Numerical trajectories match the exact solution and conserve energy.",
  "fig_c1_single_trajectory.png", [
  "solve_ivp steps Hamilton's equations forward in time to trace the orbit.",
  "The numerical path overlaps the analytic solution — the solver is verified.",
  "The orbit closes on itself and energy drift is 1.9e-9 over four periods.",
  "Confidence here is what transfers to systems with no exact answer later.",
], "singletraj", "ẋ = ∂H/∂p = p/m        ṗ = −∂H/∂x = −mω²x          —  Hamilton’s equations (Task 1b)");

figureSlide("Component 1 · Task 2(b)",
  "Higher energy gives larger, non-crossing orbits — the classical feature set.",
  "fig_c1_many_trajectories.png", [
  "Twelve random initial conditions, each coloured by its conserved energy.",
  "Orbits never intersect: a unique state has a unique future.",
  "Saved as classical_trajectories.npy — the inputs for Component 3.",
  "This nested structure is the 'feature space' the ML model learns from.",
], "manytraj");

figureSlide("Component 1 · Task 3(a, b)",
  "Adding a cosine well bends the orbits out of ellipses and ties the period to energy.",
  "fig_c1_cosine_trajectories.png", [
  "H = p²/2m + ½mω²x² − V₀cos(kx) — the classical shadow of a Josephson junction.",
  "Low-energy orbits still look elliptical; higher-energy orbits visibly deform.",
  "Anharmonicity is what makes a qubit addressable — evenly spaced levels cannot be driven two at a time.",
  "These are the classical inputs Component 3 pairs with fluxonium targets.",
], "cosine");

figureSlide("Component 1 · Task 3(c)",
  "Nearby energies trace nearby orbits — the smooth structure the ML model later relies on.",
  "fig_c1_cosine_energy_band.png", [
  "Trajectories launched in a narrow energy band, E = 2.0 ± 0.5, coloured by initial energy.",
  "The orbits nest without ever crossing: a small change in energy gives a small change in orbit.",
  "That is the property Component 3 depends on. If nearby classical inputs gave wildly different orbits, no smooth map from classical to quantum could exist.",
  "It also shows the motion is regular here — crossing orbits at the same energy would signal chaos.",
], "band");

figureSlide("Component 1 · Task 4(a, b)",
  "Two coupled oscillators live in a 4-D phase space, so we read them through 2-D projections.",
  "fig_c1_coupled_projections.png", [
  "Two cosine oscillators joined by momentum coupling λp₁p₂ with λ = 0.3.",
  "The state is (x₁, p₁, x₂, p₂) — four numbers, so the motion cannot be drawn directly.",
  "Each panel projects that 4-D motion onto one pair of coordinates.",
  "The next slide repeats all four panels at three energies.",
], "projections");

figureSlide("Component 1 · Task 4(b continued)",
  "Raising the energy grows the accessible region without ever disordering it.",
  "fig_c1_coupled_projections_energies.png", [
  "The same four projections at E₀ = 1, 3 and 12 — twelve panels, one row per energy.",
  "The accessible region grows with energy, fastest in (p₁, p₂), because the coupling acts through the momenta.",
  "The curves stay smooth and nested at every energy. Nothing scatters.",
  "This is the first evidence against my expectation of chaos at high energy — slide 12 measures it properly.",
], "projections_e");

figureSlide("Component 1 · Task 4(c)",
  "Each oscillator separately fills a band, and the coupling keeps the two correlated.",
  "fig_c1_coupled_energy_band.png", [
  "The (x₁, p₁) and (x₂, p₂) projections for a band of initial energies, E = 3.0 ± 0.5.",
  "Each oscillator explores a filled region whose size grows with its share of the energy.",
  "The two are not independent: the momentum coupling exchanges energy between them, so their regions stay correlated.",
  "Same message as Task 3(c), now with two degrees of freedom — the structure survives coupling.",
], "band2");

figureSlide("Component 1 · Task 4(d)",
  "I expected chaos at high energy. Measuring it properly says the motion stays regular.",
  "fig_c1_coupled_poincare.png", [
  "A Poincaré section records the state only as it crosses x₂ = 0 in one direction.",
  "Smooth nested curves mean regular, quasiperiodic motion (KAM tori); a scattered cloud would mean chaos.",
  "Both E = 1 and E = 12 give nested curves. The Lyapunov exponent confirms it: λ ≈ 0.004–0.007, zero to within the log t/t floor.",
  "The nonlinearity is a bounded cosine while the harmonic term grows without limit — so higher energy makes this system MORE nearly integrable.",
], "poincare");

/* ======================= 10–17 — Component 2 ======================= */
divider("Results · part 2 of 3", "Component 2 — Quantum data",
  "The expensive side: operators, spectra, Wigner functions and wave-packet dynamics — from the "
  + "textbook oscillator to a real fluxonium qubit. These are the model TARGETS.");

wideSlide("Component 2 · Task 1(a)",
  "The quantum operators reveal the ladder structure of the oscillator.",
  "fig_c2_operator_matrices.png",
  "Ĥ is diagonal (each level has a definite energy), while x̂ and p̂ have only off-diagonal entries — they connect a level to its immediate neighbours. That off-diagonal stripe is the ladder, drawn.", "operators", "x̂ = √(ℏ/2mω)(â + â†)     p̂ = −i√(ℏmω/2)(â − â†)     Ĥ = p̂²/2m + ½ mω²x̂²");

figureSlide("Component 2 · Task 1(b)",
  "Quantum energy is discrete, evenly spaced, with a nonzero zero-point energy.",
  "fig_c2_energy_spectrum.png", [
  "QuTiP eigenvalues land exactly on the analytic line Eₙ = ℏω(n+½).",
  "Ground state E₀ = ½ℏω ≠ 0 — a purely quantum effect.",
  "Levels are equally spaced by ℏω (the ladder).",
  "High-n points drift: the expected signature of finite truncation.",
], "spectrum");

figureSlide("Component 2 · Task 1(b) — convergence",
  "The truncation level N sets how many energy levels are trustworthy.",
  "fig_c2_convergence.png", [
  "Error sits at machine-zero, then jumps to a flat plateau at exactly 1.000 — not a growing drift.",
  "Cause: truncation makes one spurious eigenvalue at (N−1)/2; sorting then shifts every level above it by one rung.",
  "So the lowest ⌈(N−1)/2⌉ levels are exact: 5 of 10, 15 of 30, 25 of 50.",
  "Rule: raise N until the quantity of interest stops changing.",
], "convergence");

wideSlide("Component 2 · Task 2(a, b) + 2(c)",
  "Wigner functions expose non-classicality through negativity and interference.",
  "fig_c2_wigner_t0.png",
  "The Fock state has a negative core and the superposition shows interference fringes (both impossible classically); the coherent state stays positive — the most classical state. " +
  "Task 2(c) animates all three at a fixed colour scale — movies/wigner_{coherent,fock,superposition}.gif, playable from the repo.", "wigner");

wideSlide("Component 2 · Task 2(d)",
  "Quantum averages trace the classical orbit, but averaging hides the spread.",
  "fig_c2_expectation_vs_classical.png",
  "For the coherent state ⟨x̂⟩,⟨p̂⟩ follow the classical circle exactly (Ehrenfest's theorem); the Fock state sits at the origin. The averages discard the variance and interference the Wigner picture keeps.", "averages");

figureSlide("Component 2 · Task 3(a, b)",
  "At half flux the fluxonium is a double well whose two lowest states form a tunneling doublet.",
  "fig_c2_fluxonium_spectrum.png", [
  "Ĥ = 4E_C n̂² + ½E_L φ̂² − E_J cos(φ̂ + φ_ext) — scqubits' convention, at E_J/E_C = 5, E_L/E_C = 0.5.",
  "φ_ext = π is the symmetric sweet spot: wells at φ = ±2.85 with a barrier at φ = 0, 7.76 E_C above them.",
  "E₁ − E₀ = 0.134 E_C while E₂ − E₀ = 4.62 E_C — a 34× gap that isolates a clean two-level system.",
  "That tiny splitting is tunneling through the barrier, and it has no classical counterpart.",
], "fluxspec");

wideSlide("Component 2 · Task 3(c, d, e)",
  "A wave packet tracks the classical orbit for half a period, then falls behind it.",
  "fig_c2_fluxonium_dynamics.png",
  "Both start at the well minimum φ₀ = 2.85 with the same charge kick n₀ = 0.5. They agree until t ≈ 0.7, then the quantum average loses amplitude. The reason is precise: Ehrenfest gives d⟨n̂⟩/dt = ⟨−∂U/∂φ⟩, the average of the force — which equals the classical force at the average position only for a harmonic potential. ⟨Ĥ⟩ is conserved to 2.1e-7, so this is physics, not solver error.", "fluxdyn");

wideSlide("Component 2 · Task 3(f)",
  "Launched on the barrier, the classical and quantum pictures stop describing the same system.",
  "fig_c2_fluxonium_sweep.png",
  "Five starting phases from one well, across the barrier, to the other. In the wells (φ₀ = ±2.85) the two come closest. On the barrier top (φ₀ = 0) the classical point sweeps a wide figure-eight through both wells while the packet splits and stays put — the same initial condition, two completely different answers. That gap is what Component 3 has to learn.", "sweep");

/* ======================= 18 — Component 3 divider ======================= */
divider("Results · part 3 of 3 — new this update", "Component 3 — Machine learning",
  "Trained to early stopping, scored against three honest baselines, and measured against a physical axis — the classical→quantum breakdown is now located.");

/* ======================= 19 — training ======================= */
figureSlide("Component 3 · Task 1(a–d)",
  "Training to the validation minimum instead of a fixed 150 epochs improved the model 6.4-fold.",
  "fig_c3_loss_curve.png", [
  "300 paired trajectories: classical solve_ivp input A and fluxonium sesolve target B from the same packet.",
  "Two hidden layers of 128 with ReLU, MSE loss, Adam at lr = 1e-3, an 80/20 split.",
  "Early stopping keeps the weights at the validation minimum — epoch 1610, MSE 1.47e-4.",
  "The old fixed cutoff (red dotted) stopped while validation was still falling: 9.3e-4, 6.4× worse.",
], "losscurve", "h₁ = ReLU(W₁A + b₁)   h₂ = ReLU(W₂h₁ + b₂)   B̂ = W₃h₂ + b₃");

/* ======================= 20 — held-out prediction ======================= */
wideSlide("Component 3 · Task 1(d) — which curve is the truth?",
  "Component 2 and Component 3 measure two different gaps against the same truth: 1.067 rad vs 0.0057.",
  "fig_c3_which_curve_is_truth.png",
  "Blue is the quantum truth in both left panels — it comes from solving the Schrödinger equation and never from the model. " +
  "(a) is the gap Component 2 exists to measure: the classical input sits on a visibly different loop, 1.067 rad away. " +
  "(b) is the same trajectory against the network's prediction, in the identical window — no visible gap. " +
  "(c) subtracts (b) and plots the difference in milliradians, 186× finer, so the error is shown to be real and structured rather than assumed. " +
  "The trajectory is the median of the held-out set, not the best. Panel (a) is also the copy-classical baseline drawn as a picture: 1.067 rad is exactly what the next slide quotes.",
  "prediction");

/* ======================= 21 — the baselines (NEW) ======================= */
statSlide("Component 3 · Beyond the brief — compared to what?",
  "Only the last of these four is a neural network. The other three exist to give its score a scale.",
  [{ value: "1.067", label: "No model at all", note: "Hand the classical trajectory straight back, unchanged" },
   { value: "0.077", label: "Nearest neighbour", note: "Reuse the answer from the most similar training case" },
   { value: "0.026", label: "Straight-line fit", note: "One least-squares formula. No training of any kind" },
   { value: "0.0057", label: "Neural network", hi: true, note: "The trained model — 1610 epochs, early stopped" }],
  "Left to right, the methods get more capable and the error falls. The first number is the size of the quantum correction itself — how wrong you are ignoring quantum mechanics entirely. The last comparison is the one that counts: a straight-line fit already reaches 0.026, because inside a single well the motion is near-harmonic and the harmonic classical→quantum map really is linear. The network's job is only the nonlinear remainder, so the honest headline is 4.5× over a straight line — not 186× over copying.",
  "baselines", 1.20,
  "On its own, \"validation MSE = 1.47e-4\" cannot be judged — so I ran three deliberately simple methods on the identical task: given a classical trajectory, predict the quantum one, scored on the same 60 held-out trajectories, in radians. Yardsticks, not models I am proposing. Lower is better.");

/* ======================= 22 — the null (NEW) ======================= */
figureSlide("Component 3 · Beyond the brief — a null result",
  "My first attempt to find the breakdown found nothing — because it could not have.",
  "fig_c3_error_vs_distance.png", [
  "Error against distance from the well bottom is flat for every model: Spearman ρ = +0.08, p = 0.56 for the MLP.",
  "The first draft of this figure was titled 'error grows with distance'. Measuring the trend said otherwise, so it was retitled.",
  "But the barrier sits 2.85 rad from the minimum and this dataset sampled only to 1.00 rad — 35% of the way.",
  "A null from a measurement that could not have detected the effect is not evidence of absence.",
], "nullresult");

/* ======================= 23 — the breakdown (NEW, headline) ======================= */
// NB: the figure carries its own title ("Widening the window to the barrier makes the
// breakdown appear"), so the slide title must not repeat it — it says *why* instead.
figureSlide("Component 3 · Beyond the brief — the breakdown",
  "The breakdown sits exactly where Ehrenfest's condition fails — at the barrier.",
  "fig_c3_error_vs_distance_wide.png", [
  "A second dataset, from the well bottom to the barrier top, on a monotone one-sided axis.",
  "MLP error climbs 5.2× (ρ = +0.40, p = 0.0016); copy-classical climbs 2.4× (ρ = +0.86, p = 8.5e-19).",
  "Copy-classical's rise IS the quantum correction growing — a direct measurement of where the two pictures part company.",
  "Truncation re-checked for the wider window: cutoff 80 vs 110 agree to 8.2e-7 rad.",
], "breakdown");

/* ======================= 24 — verification ======================= */
statSlide("Verification",
  "Checking every number against an exact formula is what caught all four corrections.",
  [{ value: "5×10⁻¹⁵", label: "Spectrum", note: "max error vs Eₙ = ℏω(n+½), lowest 15 levels" },
   { value: "1.9×10⁻⁹", label: "Energy drift", note: "over four periods, at rtol = atol = 1e-10" },
   { value: "8.2×10⁻⁷", label: "Truncation", note: "cutoff 80 vs 110 across the full sampling window" }],
  "Four corrections came from this discipline, none of which raised an exception. (1) The fluxonium mixed two coordinate conventions — fixing it improved validation MSE nine-fold. (2) A claimed order-to-chaos transition the Lyapunov exponent did not support. (3) A null result that was a limit of the sampling window, not a property of the map. (4) Two numbers in my own write-up that a re-run did not reproduce. A figure is a picture, not a measurement — and a number in prose is a claim until it is traced back to output.", "verification", 1.55);

/* ======================= 25 — open questions ======================= */
{
  const s = pres.addSlide();
  eyebrow(s, "Open questions");
  title(s, "What I don't yet understand, and what I'd do next.");
  const cols = [
    ["WHAT I DON'T YET UNDERSTAND", TEAL, [
      "Is the model learning physics, or interpolating between 240 stored examples? Testing outside the training window would separate the two.",
      "Linear regression already reaches 0.026 rad, so most of the in-well map is trivially linear. How much genuine nonlinear structure is the network actually capturing?",
      "The MLP degrades fastest in relative terms toward the barrier (5.2×). Is that the map getting harder, or the training data thinning out there?",
      "Does a deeper well (larger E_J/E_C) bring classical and quantum back together, as the correspondence principle says it should?",
    ]],
    ["WHAT I'D LIKE TO DO NEXT", DEEP, [
      "Train on the residual B − A rather than B — the part Ehrenfest discards, and the only part that is not near-linear.",
      "Sweep across parameters (E_J/E_C, E_L/E_C, flux) rather than one point, which is where the Science 2022 generalization results apply.",
      "Predict a quantity with no classical analogue — the tunneling splitting — instead of a trajectory.",
      "Re-run Task 4 in the genuinely chaotic regime — λ = 0.8 with V₀ = 8 gives a Lyapunov exponent of 0.11 — if that is worth the time.",
    ]],
  ];
  cols.forEach((c, i) => {
    const x = 0.9 + i * 6.0;
    s.addShape(pres.ShapeType.roundRect, { x, y: 2.15, w: 5.6, h: 4.25, fill: { color: i ? MINT : CARD },
                                           line: { color: i ? MINT : CARD }, rectRadius: 0.05 });
    s.addText(c[0], { x: x + 0.3, y: 2.4, w: 5.0, h: 0.3, fontFace: SANS, fontSize: 10.5, bold: true,
                      color: c[1], charSpacing: 1, margin: 0 });
    s.addText(c[2].map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < c[2].length - 1 } })),
      { x: x + 0.3, y: 2.8, w: 5.0, h: 3.5, fontFace: SANS, fontSize: 12, color: INK,
        lineSpacing: 17, paraSpaceAfter: 10, valign: "top" });
  });
  s.addText("Which fluxonium property is actually worth predicting for real device design? — that one is genuinely your call.",
    { x: 0.9, y: 6.55, w: 11.5, h: 0.35, fontFace: SANS, fontSize: 12.5, italic: true, color: DEEP, margin: 0 });
  note(s, "openq"); chrome(s);
}

pres.writeFile({ fileName: OUT }).then(() => console.log(`wrote ${OUT} (${pageNo} slides)`));
