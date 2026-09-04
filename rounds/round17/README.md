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

Outcomes: filled in as the round proceeds.
