# Round 16 — how it was launched, and how to continue from a new session

Launched 2026-09-03 (~12:50 UTC) from session `d1fe2115` (root on Fable 5.1),
run id `wf_bc79ce94-557`, task `wozioe46l`. The paper at launch:
`frontier.tex` 176 pages, commit `ab61ad4`, clean build, no undefined
references; round 15 fully integrated and archived in `rounds/round15/`.

## What is in this directory

| Path | What it is |
| --- | --- |
| `round16.js` | the workflow script actually run: 10 routes × 2 adversarial audits + 7 paper audits, **all on Opus 5** (the user's instruction: only Opus agents). |

Results, journal and transcripts are added here when the round completes.

## The routes

All routes start from the gaps `frontier.tex` states after round 15.

| key | one line |
| --- | --- |
| `b3-level` | the pivot, constructive: realise the third blow-up level B³ (7-cube, height 22) by design from the 138-vertex B² game, and report the cost of one level |
| `level-lemma` | the pivot, theoretical: the inductive "one level at additive cost" lemma in the readout language of `sec:readouts`, or its exact obstruction (precision, `chi_HK`, readout order) |
| `hk-doubling` | the Holt–Klee ceiling: a polynomial upper bound on `h*_HK` (which would bound Howard's rule with two actions), or an HK-preserving dimension-raising rule; `h*_HK(6)`, the five unresolved HK classes at m = 4 |
| `width-amortise` | the amortisation statement of `sec:width` that would make `thm:qp` polynomial, `N^{f(k)}` |
| `few-denominator-stall` | a value-distinguishing stall inside the few-denominator class, or a rounded calculus deciding the class in `poly(N, D)` rounds |
| `bsi-counter` | best-response restart / BSI: a superpolynomial family with non-constant drivers, or a polynomial bound on a class |
| `one-player-howard` | the one-player half on the game side: a superlinear all-switches family (coprime lanes, leapfrog clocks, binarised Fearnley), or a polynomial bound |
| `fresh-16` | free search over formulations: quantitative-to-qualitative reductions, the mixed-Min landscape, certificate size, the easiest bit |
| `min-budget` | the Min-budget hierarchy `h*_k(m)`: upper bounds through `thm:min-count`'s pieces, `chi_HK` of the height-12 witness, of B² and of B³ |
| `fresh-16-alg` | free search over algorithms: random facet on realisable cubes, Lemke on the profile LCP, Tarski with contraction, order first |

Plus seven adversarial audits of the round-15-integrated text of
`frontier.tex`, by line range (never audited as paper text before): width
(2790–3190), laws (3543–3674, 3749–4300), blow-up and B² (5034–5617), ties
and deformed cubes (5617–6332), readouts, projection and the ladder
(6332–6950), BSI and TOP (8198–8450, 9380–9440, 970–1010), front matter and
summary (1–392, 13432–13710).

## How to relaunch from a new session

`resumeFromRunId` is same-session only. From a new session: copy
`round16.js` into the new scratchpad, edit `SCRATCH` at its top (and `PREV`,
which points at session `6e64b33d`'s scratchpad holding the round-15 route
code), recreate the harness there (`root16/`, `solo/`, `myver/` are copies
of session `6e64b33d`'s directories of the same names; the committed subset
is `scripts/blowup/` and `scripts/round15-verify/`), drop the routes whose
results are already in `results/`, and call the Workflow tool with that
`scriptPath`.
