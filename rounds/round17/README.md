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

Run history and outcomes: filled in as the round proceeds.
