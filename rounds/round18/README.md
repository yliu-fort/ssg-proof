# Round 18 — design and launch record

Brief: `BRIEF.md` (the round-17 brief's four additions stand; the standing
rule corrected). Script: `round18.js`, assembled by `build18.py` from
`round17.js`'s common digest (the repository paragraph, the standing rule
and the harness paths rewritten; a round-17 addendum appended), the seven
route briefs in `routes18.txt`, the two audit lenses and the paper audit.
`inventory.txt` is the result inventory handed to every agent (503
numbered results of `frontier.tex` at commit `812364d`, 229 pages, 17759
lines).

Design: seven object-changing routes (`drive-line`, `one-player-envelope`,
`eval-decision`, `convex-class`, `weakest-oracle`, `beyond-holt-klee`,
`rlt-two`), each followed by a correctness audit and a novelty audit
(pipeline: a route's audits start when it returns); one paper audit on the
round-17 diff (`git diff 7fa45a3..812364d -- frontier.tex`, 1713 added
lines, with the round-17 audit's unchecked backlog as secondary targets).
All 22 agents on Opus 5 (the user's rule: only Opus agents).

## Run history

- 2026-09-04 08:32 UTC: a one-call Opus probe succeeded.
- 2026-09-04 08:43 UTC: launched from session `296b18c1` (root on
  Fable 5.1): run id `wf_f6636a94-d46`, transcript directory
  `~/.claude/projects/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/subagents/workflows/wf_f6636a94-d46/`.
  `SCRATCH` is this session's scratchpad
  (`/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad`),
  into which the harness (`root16/`, `solo/`, `myver/`, logs stripped) was
  copied from session `d1fe2115`'s scratchpad; the round-17 route and
  audit directories stay there, read-only, as `R17`. The routes' `r18-<key>/`
  and the audits' `r18-audit-*` directories are created in `SCRATCH`.
- Before launch: one stale monitor loop from session `d1fe2115` (watching
  the round-16 journal) was killed; the repository was clean at `812364d`.

## Outcomes

### The paper audit (round-17 diff) --- returned 09:31 UTC, NOT SOUND

Three majors and ten minors, all in text integrated in round 17; every
finding was re-checked by the root agent and repaired in batch P
(`results/04_frontier.tex_round-17_diff.json`; the LP findings recomputed
in `scripts/round18-verify/own_r.py`). Everything recomputable in the
round-17 material was reproduced exactly by the auditor (BC(e,s) at ten
sizes, BP(D), OS(R), the blow-up height formulas over all 728 AUSOs, the
137-vertex $B^2$ game and the exact fences, the handicap minors, HDP,
L_6's informative rounds, the five-point certificate, ...).

| # | label | defect | repair |
| --- | --- | --- | --- |
| M1 | `prop:own-stall`, `rem:own-successor`, `rem:transport`, abstract | "that reading decides no controlled vertex" on $R$ is false: the Z-seeded own-successor clause (i) fires at the Min vertex 6, which the seed pins to 0 (and "(i) can never fire" for the LP was wrong: it fires when the seeded polytope forces equality) | the stall is of the two value-distinguishing vertices outside the seed; clause (i)'s separators printed; the abstract and `rem:transport` aligned |
| M2 | `rem:own-stall`, abstract, summary | the seven-vertex game does not "stall both readings": vertices 3 (clause ii) and 1 (pair test) are decided in the same round, only 4 is silent, and after retyping 1 and 3 the certificate decides 4 too | restated as a silence at one vertex, not a stall of the rule; "a stall proper is exhibited nowhere in this document" |
| M3 | `rem:blowup-realise` | "the orientation oracle is weaker than the value oracle already at $m=3$" contradicted by its own numbers (4 out-set queries against $\lvert Cvert+2\ge5$) | "separated by nothing here"; the orientation oracle is the cheaper one on that data |
| m1--m10 | `rem:cyclic-antipodal` (the profile count: one profile goes straight to the sink, three enter the cycle; the 23/8-vertex conventions), `cor:pinned-no-doubling` (the definition misdescribed its own example and lacked a verb; the height-16 bound scoped to blow-up outmaps), `thm:convex-barrier-both` (its proof cited itself), `rem:choice-lift` (an unproved exactness clause marked as the route's claim), the summary's BC clause (the preorder-seeded combination is measured), `rem:order-unique` (UP $\cap$ coUP attribution), the `st2_nf.py` path, the BC game files (archived in `scripts/round17-verify/`; the harness archived in `scripts/harness/`), `rem:slack-grade` (both composites), `prop:cv-measured` ("between two and three times"), `rem:eval-queries` (a fragment) | all repaired as the audit proposed |

Not checked by the audit (recorded for a later audit): `prop:b3-outer`'s 194-vertex game; ST(1)/ST(2); `rem:bias-families`' BP(D) counts; `prop:bias-witnesses`' PATH games; `rem:discount-fold`'s $9D+3$ variant; `thm:eval-queries`' 136/194/344-vertex reproductions; `rem:choice-lift`'s level-two exactness; the round-17 backlog (untouched).

### The routes

(to be filled as the routes and audits return)
