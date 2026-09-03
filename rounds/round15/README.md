# Round 15 (re-run) — how it was launched, and how to continue from a new session

The first launch of round 15 (session `3f223550`, 2026-09-02) was cancelled by
the user before any route returned; its files were removed (recoverable from
git at `c33e2ae`). This directory is the **re-run**, launched 2026-09-03 from
session `6e64b33d` (root on Fable 5.1), run id `wf_fed5a63d-530`, task
`w1d6pkaml`. The paper at launch: `frontier.tex` 137 pages / 330 results,
commit `0538a60` plus the two remarks patched in this session (see the commit
that added this file), clean build, no undefined references.

## What is in this directory

| Path | What it is |
| --- | --- |
| `round15.js` | the workflow script actually run: 10 routes × 2 adversarial audits + 6 paper audits, **all on Opus 5** (the user's instruction for this session: only Opus agents). |
| `build16.py` | builds `round15.js` from the cancelled script (`git show c33e2ae^:rounds/round15/round15.js`) by patching the shared briefing (`COMMON`) with the solo-round state and splicing in `routes16_new.js`. |
| `routes16_new.js` | the four new route briefs (`gadget`, `monotone-lemma`, `degenerate`, `lane-reuse`). |

Results, journal and transcripts are added here when the round completes.

## The routes

| key | one line |
| --- | --- |
| `gadget` | the pivot, constructive side: reverse-engineer the one-player game realising the blow-up of the 2-cube (a translated layer at inner dimension two), then realise the second blow-up level B² (5-cube, height 10) by hand with exact LP |
| `monotone-lemma` | the pivot, negative side: Holt–Klee sufficiency for one player, a projected-Holt–Klee condition for two players, the monotone-readout lemma |
| `howard-cube` | the one-player half as polytope combinatorics: Goldfarb / Amenta–Ziegler cubes, `h*_HK`, finishing the five unresolved Holt–Klee classes at m = 4, an HK-preserving doubling |
| `sink-projection` | the |C|-cube P-LCP USO, Holt–Klee by GMR, the Max cube as its sink projection, what projection preserves, the least k for B² |
| `rbr-rounds` | the round count of R_BR and BSI: geometric decay of the maximal gap, or a family that switches one vertex many times |
| `treewidth` | bounded width: a seventh polynomial class or where response-function tables explode |
| `free-search-15` | a formulation nobody has tried (TOP average vertex, self-reduction measures, forest-count ratio) |
| `verify-r14` | independent verification and paste-ready LaTeX for the round-14 results still outside the paper |
| `degenerate` | degenerate one-player games: a run of length 7 at m = 4 via ties, timers, a superlinear family |
| `lane-reuse` | the lane family with the correct rise accounting; binarising a published counter |

Plus six adversarial audits of `frontier.tex` by line range: classes
(1124–2684), all-switches (3206–4564, including the never-audited blow-up
material), refutations (4564–6430), calculi (7185–8714), hybrid
(8714–10635), summary and front matter. Foundations and structure were
audited in the cancelled launch (no mathematical error found; repairs
committed as `551a6ad`).

## How to relaunch from a new session

`resumeFromRunId` is same-session only. From a new session: copy `round15.js`
into the new scratchpad, edit `SCRATCH` at its top, recreate the harness there
(`root16/` is a copy of session `3f223550`'s `root15/`; `solo/` is a copy of
session `72fdeee0`'s `solo/`; the committed subset is `scripts/blowup/`), drop
the routes whose results are already in `results/`, and call the Workflow tool
with that `scriptPath`.

## Results and audits (archived)

`results/NN_x.json` are the structured returns of the routes and audits of
run `wf_fed5a63d-530` (the resumed run; `journal.jsonl` is its journal).
Integration into `frontier.tex` happened in commits after 9f5a4d7: every
route was trimmed to what its significance audit kept and what the root
agent re-verified (`scripts/round15-verify/`).  Kept: howard-cube
(sec:deformed), monotone (sec:readouts), sink-projection (sec:projection),
free-search (thm:b2-walk, thm:top), best-response (thm:bsi-tracks,
thm:readout, prop:leapfrog), gadget (lem:crossing, cor:b2-min, prop:xor,
thm:alternation-bits), lane and degenerate repairs; then, after their
audits, the bounded-width route (sec:width: lem:payoff-transfer,
lem:cut-sign, thm:tarski, lem:round-recover, thm:modulator, thm:qp,
rem:fold-width, prop:modulator-family) and the verify-r14 items
(lem:same-successor, prop:bsi-normal, prop:q16, prop:zero-ties,
prop:nondeg-overshoot, cor:isolated, cor:selfread, prop:fv-stall).
