# Round 17 — design and launch record

Brief: `BRIEF.md` (the user's four additions on top of `conjecture.md`).
Script: `round17.js` (copied from the session scratchpad at launch);
`inventory.txt` is the result inventory handed to every agent (471 numbered
results of `frontier.tex` at commit `7fa45a3`, 209 pages).

Design: seven object-changing routes (`query-model`, `order-lattice`,
`convex-lift`, `variational`, `parametric-path`, `oracle-barrier`,
`realisation-space`), each with a correctness audit and a novelty audit
that must classify every result as new-object / new-relation /
strengthening / restatement / measurement-only / unproved; verdict scale
SOLVED / new-theorem / new-barrier / blocked / dead-end; one paper audit on
the round-16 diff (`git diff ab61ad4..7fa45a3 -- frontier.tex`, 2698 added
lines). All 22 agents on Opus 5. Scheduled launch 2026-09-04 03:51 UTC.

## Run history

- 2026-09-04 03:51 UTC: the scheduled launch from session `d1fe2115`
  (its in-session cron `a083c5f9`) did not fire; by 03:58 UTC no workflow
  directory and no `r17-*` route directory existed and that session was
  idle.
- 2026-09-04 03:59 UTC: launched from session `5cc7fb9d` (root on
  Fable 5.1, on the user's instruction to take over) after a one-call Opus
  probe succeeded: run id `wf_bf90f29c-0b2`, transcript directory
  `~/.claude/projects/-data-ssg-proof/5cc7fb9d-035b-424b-bca6-ec769216aeb1/subagents/workflows/wf_bf90f29c-0b2/`.
  The script's `SCRATCH` still points at session `d1fe2115`'s scratchpad,
  where the harness (`root16/`, `solo/`, `myver/`) and
  `round17/inventory.txt` live; the routes' `r17-<key>/` and the audits'
  `r17-audit-*` directories are created there.

## Outcomes

### The paper audit (round-16 diff) — returned 04:43 UTC, NOT SOUND

Seven majors and eleven minors, all in text integrated in round 16; every
finding was re-checked by the root agent and repaired in batch A
(`results/01_paper-audit_round16-diff.json`; the two computational
findings recomputed in `scripts/round17-verify/`).

| # | label | defect | repair |
| --- | --- | --- | --- |
| M1 | `rem:four-ceilings` | the new inequality $h^*_1\le h^*_{LP}\le h^*_{HK}$ cited `prop:oneplayer-lp`, which needs nondegeneracy, while $h^*_1$ allows ties (open after `thm:no-seven`) | stated for the nondegenerate ceiling; every lower bound of the last row is attained by a nondegenerate witness, so the LP row inherits it |
| M2 | `rem:signdef` | "closed under `def:damping`" is false: damping reweights first-passage entries by path length | struck; the 9-vertex counterexample recorded (recomputed, `signdef_damping.py`) |
| M3 | `prop:bias-one-improving` | title and statement say single-switch, the proof says multi-switch; the coinciding-breakpoint parenthetical was false | retitled and restated as a multi-switch rule ($N4^a$ bound); `sec:bias` intro, `rem:bias-gap` and the summary aligned |
| M4 | summary | "no named family costs it more than $2\|C\|$" contradicted by `prop:bias-witnesses` | restated as the body's "no hard family ... about $2\|C\|$", the four witnesses named |
| M5 | `cor:stack-family` | superadditivity and Fekete dropped the nondegeneracy of the stacked block | mixed inequality with $h^{*,nd}_1$, a liminf bound; Fekete's limit marked not established; the construction's own cap kept |
| M6 | abstract | "unbounded in ratio to the trivial one" for a constant factor $12/7$ | "exceeds ... by a constant factor"; the summary's Fekete clause likewise |
| M7 | text after `cor:blowup-transl` | stale $h^*_{HK}(6)\ge12$ and "ties the best Holt–Klee height known" after `prop:hk-records` gave 14 | updated: 12 is two below the 14, itself a free-readout blow-up |
| m1–m11 | `prop:blowup-readout`(a) proof, `prop:blowup-height` (the $2^k$ count: 32 of 728 3-cube AUSOs have six or seven maximal vertices, `bh_count.py`; the arbitrary-$z$ clause), `rem:no-amplification`, `thm:lemke-homotopy`(c),(d) proofs, `prop:b3-outer`'s dangling "(i)", `thm:switch-count`'s preamble ($4^{-a}$ for multi-switch), `rem:stack-measured` (ST(2)'s game file not recorded), `prop:fv-stall` (M4 over the rounds tested), `thm:signdef` ("eight polynomial classes" counted `thm:qp`), abstract/summary "translated layer is not" | all repaired as the audit proposed |

Not checked by the audit (recorded for a later audit): the escape exponent
$d(M_n)=n+1$; `prop:hk-doubling-measured`(d),(e); `prop:oneplayer-census-small`'s
total; the measured rows of `prop:cv-measured`; `prop:q16`'s revised counts;
`prop:hstar-one-eight`'s 2691-vertex game (not in the repository);
`prop:bias-witnesses`(b)–(d); `lem:max-tree`'s 11-vertex instance;
`prop:zero-ties`' 26 tied incidences.

### The routes

| key | returned | route's verdict | root agent's own verification (`scripts/round17-verify/`) | audits | integration |
| --- | --- | --- | --- | --- | --- |
| `order-lattice` | 04:54 UTC | new-theorem | `ol_verify.py`: `ol:unique` exhaustive over all preorders on 76 games; OL3's 3-cycle, values, nondegeneracy and $w^*$ from the game; no cycle at $\lvert C\rvert\le2$ (2000 games); the 1-Max-1-Min cross-multiplication proof checked by hand | novelty: sound, verdict DEAD-END (the object collapses, provably, to the profile cube's antipodal walk; `ol:small-C` is four lines from `thm:profile-uso`; `ol:lift-cycles` is the paper's own instance; `ol:read`'s parameter $b$ is inside `thm:modulator`); correctness: NOT sound as delivered but the four theorem statements hold --- the headline's "cannot cycle when $\lvert C\rvert\le2$" is false without separatedness (an 8-vertex non-separated 1-Max-1-Min game on which the lift 2-cycles, recomputed here in `ol_gc.py`), the GAP was a false conjecture, "no sound lift" a non-sequitur, four decodes is three | batch B, commit below: a remark after `thm:order-determines` (uniqueness of the consistent order, the read letters, stopping necessary) and a remark after `thm:cyclic-uso` (the antipodal 3-cycle on the paper's instance; no cycle at $\lvert C\rvert\le2$) |
| `parametric-path` | 04:59 UTC | new-barrier | `bp_verify.py`: BP(D) rebuilt from the statement for $D=1..8$, the tent identity, the breakpoint set $\{k/2^D\}$ with exactly $F_d,G_d$ tied, $2^D$ distinct pairs = the tent itinerary; the route's one-Max instances (roots $\{1/4,1/2\}$, $\{1/8,\dots,5/8\}$) against their own polynomials; `pp:step`'s derivative argument checked by hand; the correctness auditor's repair of the transplant ($P_D$ with a two-vertex chain seed, $6D+3$ vertices) verified for $D\le8$ (`pd_discount.py`) | novelty: sustained narrowly, new-barrier (integrate about a page; `pp:basic` a restatement, `pp:separation` measurement-only, fix the $\beta$ collision); correctness: NOT sound as delivered (the exponential separation from the bias path measured only; `pp:step`'s algorithmic clause refuted by a 14-vertex instance where the derived game has two optimal actions; the "slope $2/\beta$" account of the transplant false, the seed is what fails; minors at $\beta=0$), the family itself reproduced exactly for $D\le9$ | batch C, commit below: `def:discount-path`/`rem:discount-path` after `lem:gadget`, `prop:discount-fold`/`rem:discount-fold` after `rem:fold` (with the seed correction and the $6D+3$ variant), `prop:one-vertex-path`/`cor:two-homotopies` after `prop:bias-witnesses`, a measured BP(D) clause in `rem:bias-families`; the survival probability written $\varrho$ |
| `convex-lift` | 05:06 UTC | new-theorem | `cl_verify.py`: the level-one gap certificate on $W_{14}$ from the paper's normal form (five points in $\tilde Q$, tightness, both convex combinations, so $\max_{R_1}x(v_1)\ge3/5$); $w^*$ and stopping of $W_{14}$, its dual and DW recomputed from the game files; `cl:exact-lift`, `cl:rigid`, `cl:collapse` arguments checked by hand; the audit's correction of `rem:own-successor` recomputed (`pairtest.py`: on $R$ the non-strict pair test decides vertices 1, 4, 6 while the own-successor separators are 0; on the 7-vertex witness both readings are silent at vertex 4) | novelty: NOT sound, verdict new-theorem but weak (`cl:barrier` false at $j=0$ on $G_8$ and $G^*$; `cl:collapse`'s "first exact level $\le\min(m,k)$" false on $W_{14}$; `cl:exact-lift`, `cl:rigid` restatements; DW is `thm:compare-equivalence`'s gadget); correctness: pending | batch D (drafted): one remark after `rem:lasserre` (the choice-variable Sherali–Adams lift fails at level one on $W_{14}$, the five-point certificate, the straddle on $W_{14}$ joined to its dual, the directional collapse bounds) and THE CORRECTION of `rem:own-successor`, `prop:own-stall`, `rem:own-stall` and the summary: the pair test is not strictly weaker, the two readings are incomparable, and the 7-vertex game stalls both |
| `realisation-space` | 05:13 UTC | new-barrier | `b2pins.py` (the round-16 sparse verifier): the three new realisations of $B^2$ (137, 138, 139 vertices, 5 Max, 1 Min) verified from the game files, outmap $=B^2$, no tied incidence, USO, acyclic, height 10, run $12,19,13,17,8,16,0,7,1,5,4$ with values increasing (`B2_pin137_GAME.json` archived); `rs:upclosed` and `rs:no-outer-translate` checked by hand (the up-closedness of the outer vertices' switchable sets on the pinned layer against the parity classes the translate demands); the auditor's missing step recomputed (`rs_upclosed.py`: which pin pairs pass up-closedness on $B^2$ and its doubling translates) | novelty: NOT sound, verdict new-theorem (a closed construction avenue, not a barrier): `rs:metric`'s converse false, `rs:drive` restates `lem:readout`(a), `rs:where`(ii),(iii) vacuous, `prop:b2-realised` is NOT doubly pinned (its block has no pin pair), the pin-pair step of `rs:no-doubling` missing; keep the pinned shape, the level theorem, `rs:upclosed` $\to$ `rs:no-outer-translate` $\to$ `rs:no-doubling`; correctness: pending | batch E (to draft after the correctness audit): after `prop:b3-outer` |
| `oracle-barrier` | 05:19 UTC | new-barrier | in progress: the route's BC(2,5), BC(3,5), BC(4,5) games loaded, $w^*$, the gap $2^{-s}$ at $v_0$ and the seeds confirmed; the root's own slack calculus, min-plus closure and `def:ratio`, Z-seeded, both clauses of `rem:own-successor` at $v_0,v_1,v_2$ (`bc_light.py`, 40 rounds): on BC(2,5) M2 first fires at $v_0$ at round 39 (clause ii) and M2T at round 21, M6 never; on BC(3,5) and BC(4,5) all three silent through 40 rounds --- far beyond the certificate's $K+1=2,5,11$, as a lower bound should be; the full hybrid with the transport LP (`bc_verify.py`) running with few rounds; the root's own `def:simorder` fixed point relates none of the twelve test pairs at $v_0,v_1,v_2$ on all three sizes (`bc_m1.py`) | novelty: NOT sound as framed, verdict new-barrier earned by BC(e,s) alone (the model $\mathfrak D$ cannot produce the coinductive preorder, so "M1 is a member" is false; the M1-seeding clause of the lower bound is measured, not proved; `ob:no-permanent` and `ob:m1-grade` restatements; `ob:edge` is `thm:seed-dichotomy`); integrate the BC subsection, the multiplicative certificate theorem and a one-sentence remark after `def:slack`; correctness: pending | batch F (drafted): `sec:bc` before `sec:wedge` (def, values, the local-matching block, the lift-reduction lemma, the certificate, the lower bound with the M1 clause demoted to measured, a measured remark), `lem:ratio-sign`/`thm:convex-barrier-both` after `thm:hybrid-convex-barrier`, `rem:slack-grade` after `def:slack` |
| `query-model` | 05:44 UTC | new-theorem | the rank argument of `qm:eval` (each non-halting evaluation adds a dimension to the span of the answers, so $d(G)+2\le\lvert C\rvert+2$ evaluations suffice) checked by hand; `dout3.py`: the deterministic outmap-query complexity of the 3-cube AUSO class recomputed by exact minimax, $4$ (and $1,2$ at $m=1,2$) | pending | pending both audits |
