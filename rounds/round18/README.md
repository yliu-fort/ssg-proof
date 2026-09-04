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

(to be filled as the routes and audits return)
