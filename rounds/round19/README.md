# Round 19 — design and launch record

Brief: `BRIEF.md` (the round-17 brief's four additions and the round-18
brief stand; every decision item taken per the root agent's
recommendation, approved by the user on 2026-09-05). Script:
`round19.js`, assembled by `build19.py` from `round18.js`'s common digest
(the repository paragraph and the inventory path rewritten, a round-18
addendum with the lesson of the round appended, the rules extended by the
required `games_built` field, the headline-as-claim rule, the tree-depth
and pacing traps), the eight route briefs in `routes19.txt`, the two audit
lenses (extended by the headline check and the games-built check) and a
paper audit rewritten for the round-18 diff. `inventory.txt` is the result
inventory handed to every agent, regenerated at HEAD `6e6c011` by
`inventory.py` (526 numbered results, 244 pages, 18978 lines; the
round-18 copy had listed only 175).

Design: eight routes (`escape-certificate`, `fold-feedback`,
`hk-law-certificate`, `m6-walk`, `promise-gap`, `extension-complexity`,
`handicap-tangent`, `fresh-19` — the last blind), each followed by a
correctness audit and a novelty audit (pipeline: a route's audits start
when it returns); one paper audit on the round-18 diff
(`git diff 812364d..6e6c011 -- frontier.tex`, 1317 added lines, saved as
`round18_diff.txt` in the session scratchpad, with the two rounds'
unchecked backlog as secondary targets). All 25 agents on Opus 5 at
`effort: 'high'` with the pacing sentence of `round18b.js`.

## Run history

- 2026-09-05 (session `c506180a`, root on Fable 5.1): the harness
  (`root16/`, `solo/`, `myver/`) and the integration tooling
  (`integrate/`) copied from session `296b18c1`'s scratchpad into this
  session's scratchpad `SCRATCH`
  (`/tmp/claude-1000/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/scratchpad`);
  the round-18 route and audit directories stay in `296b18c1`'s
  scratchpad, read-only, as `R18`; round 16/17 code in `d1fe2115`'s as
  `R17`. Before launch: no stale monitor loop or background job found;
  the ~40 gitignored stray logs of the repository root (round 14–18
  leftovers, none referenced, none over 170 bytes) moved to
  `SCRATCH/stray-root/`; the repository clean at `6e6c011`.
- A one-call Opus probe succeeded (7 s).
- Launched from this session: run id `wf_334ff97f-090`, transcript
  directory
  `~/.claude/projects/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/subagents/workflows/wf_334ff97f-090/`.
  The routes' `r19-<key>/` and the audits' `r19-audit-*` directories are
  created in `SCRATCH`.
- In parallel with the run the root agent takes the two cheap checks of
  `rem:eval-decide-gap` / `rem:rational-row` (whether
  `thm:readout-realise`(a)'s system satisfies the trap hypothesis; whether
  |C|+1 or |C|+2 is exact at |C|=3) itself, per decision A4.

## Outcomes

(pending)
