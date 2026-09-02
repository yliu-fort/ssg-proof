# Round 15 — how it was launched, and how to continue from a new session

Launched 2026-09-02 ~06:50 UTC from session `3f223550` (root on Fable 5.1),
run id `wf_2e2aee70-8e9`, task `w3jg6ovj6`. The paper at launch:
`frontier.tex` 131 pages / 321 results, commit `71a0437`, clean build, no
undefined references.

## What is in this directory

| Path | What it is |
| --- | --- |
| `round15.js` | the workflow script actually run (7 routes × 2 adversarial audits + 8 paper audits). |
| `build_round15.py` | builds `round15.js` from `../round14/round14.js` by patching the shared briefing (`COMMON`) with round 14's results and replacing the route list. Re-run it after editing to regenerate the script. |

Results, journal and transcripts are added here when the round completes.

## Model policy (set by the user on 2026-09-02)

Routes run on Opus 5 by default; **at most one** route per round on Fable 5.1,
reserved for the hardest or most valuable route; adversarial audits always on
Opus 5. In the script this is the `model` field of each route and the
hard-coded `model: 'opus'` on the audit agents.

## The routes

| key | model | one line |
| --- | --- | --- |
| `allsw-family` | fable | the pivot: a superpolynomial all-switches family — two-player height doubling through the harmonic normal form, the degenerate one-player crack, lane re-use with the correct rise accounting |
| `howard-cube` | opus | the one-player half as polytope combinatorics: BA heights of Klee–Minty / Goldfarb / Amenta–Ziegler cubes, `h*_HK(m)`, realisability of Holt–Klee AUSOs as occupancy polytopes, whether the Schurr–Szabó blow-up preserves Holt–Klee |
| `rbr-rounds` | opus | the round count of `R_BR` and BSI: geometric decay of the maximal gap, or a family that switches one vertex many times (composing `Q_16`) |
| `sink-projection` | opus | the |C|-cube as a P-matrix LCP orientation (Holt–Klee by Gärtner–Morris–Rüst) and the Max cube as its sink projection |
| `treewidth` | opus | bounded treewidth / pathwidth: a seventh polynomial class or the exact place where response-function tables explode; the one-colour feedback class as a corollary of `thm:kacyclic` |
| `free-search-15` | opus | a formulation nobody has tried, with seeds (TOP average vertex, self-reduction measures, forest-count ratio) |
| `verify-r14` | opus | independent verification and paste-ready LaTeX for the round-14 results still outside the paper |

Plus eight adversarial audits of `frontier.tex` itself, by line range:
foundations, classes, structure, allswitches, refutations, calculi, hybrid,
summary/front matter.

## How to relaunch from a new session

`resumeFromRunId` is same-session only. From a new session:

```bash
cp /data/ssg-proof/rounds/round15/round15.js /tmp/claude-1000/-data-ssg-proof/<session-id>/scratchpad/round15.js
```

Edit `SCRATCH` at the top to the new session's scratchpad, recreate the
harness there (`root15/` is a copy of round 14's `root14/` plus
`r14routes/{allsw-lower,free-search-14,bsi-rounds}`; the round-14 harness is
archived in `../round14/harness/` and the full round-14 code under the
scratchpads of sessions `26460c0d` and `ef1cfad9`), drop the routes whose
results are already in `results/`, and call the Workflow tool with that
`scriptPath`.
