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

### The paper audit (round-16 diff) — returned 04:39 UTC, NOT SOUND

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

Filled in as they return.
