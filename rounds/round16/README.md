# Round 16 — how it was launched, what came back, and how it was integrated

Launched 2026-09-03 (~12:50 UTC) from session `d1fe2115` (root on Fable 5.1),
run id `wf_bc79ce94-557`. The paper at launch: `frontier.tex` 176 pages,
commit `ab61ad4`, clean build, no undefined references; round 15 fully
integrated and archived in `rounds/round15/`.

## What is in this directory

| Path | What it is |
| --- | --- |
| `round16.js` | the workflow script: 10 routes × 2 adversarial audits + 7 paper audits, **all on Opus 5** (the user's instruction: only Opus agents). |
| `round16b.js` | the completion script (run id `wf_374facb2-b8a`): the `few-denominator-stall` route with its two audits, and the four audits that hit the session usage limit, fed the saved route results through `args`. |
| `results/` | the structured returns of every route and audit (`NN_*.json`), with each route's paste-ready LaTeX (`NN_*.tex`). |

## How the run went

The first launch died in full at 13:27–13:31 UTC: all 17 first-stage
agents hit API 529/500 server errors within four minutes (2.7M subagent
tokens, nothing returned). A resume at 18:07 UTC (after an Opus probe
succeeded) re-ran everything; 30 of 35 agents completed (9.6M tokens,
2 h 31 min) and the last five hit the session usage limit. A second
`resumeFromRunId` after the limit reset re-started the 17 agents that had
failed in the first launch and later succeeded (a key that ever failed is
not treated as cached); it was killed after two minutes and replaced by
`round16b.js`.

## The routes

| key | verdict | what survived its two audits and my own verification |
| --- | --- | --- |
| `fresh-16` | strict-progress | the two qualitative sets proved inside the model (`prop:qualitative`); a plugged-in stopping game is exactly a $(p,q)$-gate with $q$ the value of the role-reversed game (`lem:gate`, verified on 49 compositions); two-exit contraction (`thm:two-exit`); the energy identity $\sum N_v\Delta_v^2=4w(1-w)$ and the Doob crossing bound (`thm:energy`); a black-box no-amplification remark. Dropped: the top-controlled-vertex equivalence (fails ties), the polynomial-class claim, the finite-automaton consequence (outside its own hypothesis). |
| `level-lemma` | strict-progress | the height of $B(s)$ is exactly $2h+2$ with a closed form per layer (`prop:blowup-height`, verified on six seeds); `lem:layer-order`; the anatomy of the level-two game — its outer pair pinned to $2048/3313, 2036/3313$ driving one frozen inner block (`rem:b2-anatomy`, verified); $\chi_{\mathrm{HK}}\le 2^m$. Dropped: the "finite order" equivalence (overclaims thm:readout-realise's open half), the driven-liftability gap (not satisfied by the level-two game). |
| `hk-doubling` | strict-progress | $h^*_{\mathrm{HK}}(6)\ge14$, $h^*_{\mathrm{HK}}(7)\ge20$ with explicit orientations (verified), the sink lift $+1$ per dimension (verified), the blow-up with a free readout doubling while Holt–Klee at $m=4,5$, the readout-free condition (T*); audits pending in `round16b`. |
| `width-amortise` | strict-progress | $\mathrm{FL}(D)$: $2^D$ response pieces at treewidth = pathwidth 3 (`rem:fold-width`; piece count verified); treewidth one lies in $\mathcal K_1$ (`prop:forest-k1`). The "PI_k" reformulation is equivalent to the goal (both audits) and the amortisation paragraph was corrected accordingly. |
| `few-denominator-stall` | — | hit the session limit; re-run in `round16b`. |
| `bsi-counter` | strict-progress | $W_2$: best-response restart takes $2^m-1=3$ rounds at $m=2$ where all-switches takes 2 (`prop:w2`, verified); the reordering bound; clamped games are easy for the rule (a bound, not a class); the double-best-response form of the rule. Dropped: the constant-option lemma (already in the paper), the piercing asymptotics (unproved). |
| `one-player-howard` | strict-progress | stacking behind a freezing bias (`thm:stack`): a one-player family with $7k$ Max vertices and run $12k$ (verified from the games at $k=1,2$, the latter through its exact normal form over all $2^{14}$ starts); $h^*_1(5)\ge10$ (verified), $h^*_1(8)\ge13$; sign-definite games as a rule bound; the exhaustive census at $N\le8$; Fekete: stacking is capped by its best block. The dictionary (v3) cut to a remark (it is `lem:readout` at $k=0$). |
| `fresh-16` (formulations) and `fresh-16-alg` | strict-progress | Lemke's algorithm on the profile LCP is a bias homotopy (`thm:lemke-homotopy`); on one player an improving single-switch rule and the shadow-vertex path of the occupancy polytope; on two players a directed path of the profile cube (the auditor's correction); four one-player witnesses with $2^3-1,12,18,22$ breakpoints (`HAM_3` verified). Dropped: the Murty conclusion, the warm-start count (vacuous), the families proposition (rewritten as a remark). |
| `min-budget` | strict-progress | both non-Holt–Klee classes of the 3-cube realised with **one** Min vertex (`prop:m3-one-min`, verified from the games); the Holt–Klee defect data at $m\le5$ (`rem:hk-defect`); the best-response pieces of $G^\sharp$ and $B^2$. Dropped: the block bound (vacuous on every instance), its lemmas (restatements). |
| `b3-level` | strict-progress | $B^3$ is not realised. Kept: a parity readable along the walk (`prop:parity-readable`) and the 194-vertex 7-cube game realising the relaxed target of height 12 (`prop:b3-outer`, verified from the game). Dropped: the "relaxed theorem" (the paper's own machine-checked generality), the rise-sign lemma (false as stated), the cost claim. |

## The paper audits (all seven returned; every defect repaired in batch A/B)

| range | majors found |
| --- | --- |
| ties/deformed 5617–6332 | `rem:four-ceilings` overstated ("strictly below $h^*$ from $m=4$ on"); a wrong case in `lem:two-ties` |
| laws 3543–3674, 3749–4300 | `lem:max-tree` needs a balanced tree; $K_n$ of `prop:k1-family` lies in the escape class (verified: $\lambda=19/20$) |
| blow-up 5034–5617 | `cor:b2-min`'s proof sentence false (the Min response varies on 32 of 80 faces, verified); `cor:parity-unreadable`'s second clause unsupported |
| width 2790–3190 | `thm:modulator` needs stopping in the statement; the "no hard instance in the modulator class" claim false; `prop:modulator-family` argued three of six exclusions (the other three verified here) |
| BSI/top 8198–8450, 9380–9440, 970–1010 | `prop:q16`'s switch counts; `prop:leapfrog`'s "$O(1)$ per reversal"; the two-player tightness claim |
| readouts/projection 6332–6950 | `lem:readout(b)`'s dyadicity claim false (repaired by defining $G[y]$ as a payoff game) |
| front matter and summary | seven scope/strength mismatches (imports, $\mathcal K_1$, $Z_D$ and $M_n$ class claims, projection scope, zero-tie scope, slack-stall scope) |

## Integration commits

`e40b995` batch A (83 repairs, six line-range audits); `b286c5f` batch B
(front matter and summary); `d02f5dc` batch C part 1 (exact blow-up
height, level-two anatomy, FL(D), treewidth one); `6570930` batch D (the
route integrations above); batch E (hk-doubling) pending its audits.
The verification scripts behind every "verified" above are in
`scripts/round16-verify/`.

## How to relaunch from a new session

`resumeFromRunId` is same-session only, and after a partial failure it
re-runs every agent whose key ever failed. From a new session: copy the
script into the new scratchpad, edit `SCRATCH` and `PREV` at its top,
recreate the harness there (`root16/`, `solo/`, `myver/` are copies of
session `6e64b33d`'s directories; the committed subset is
`scripts/blowup/`, `scripts/round15-verify/` and `scripts/round16-verify/`),
drop the routes whose results are already in `results/`, and call the
Workflow tool with that `scriptPath`.
