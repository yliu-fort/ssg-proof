# Round 14 — saved state, and how to continue from a new session

Round 14 was launched on 2026-09-01 and **stopped early at the user's request**
(token budget) with 5 of 9 routes and 1 of 18 audits returned. Everything needed
to continue is in this directory. Nothing here has been verified by the root
agent, and **nothing here has been integrated into `frontier.tex`**.

## What is in this directory

| Path | What it is |
| --- | --- |
| `round14.js` | the full workflow script (9 routes × 2 adversarial audits, 66 KB). Re-runnable as is. |
| `journal.jsonl` | the workflow journal: every `started` and `result` record, with the complete route payloads. |
| `results/*.json` | the six payloads extracted one file per agent, human-readable. |
| `transcripts/*.jsonl.gz` | full agent transcripts of the four routes that were killed before returning. They contain real partial work. |
| `harness/` | the root agent's own exact-arithmetic code written this session (see below). |
| `memory-snapshot.md` | snapshot of the project memory file as of the stop, for a session that starts without memory. |

The paper is unchanged: `frontier.tex` is at 114 pages / 278 results, commit
`9f05e03`, clean build, no undefined references.

## The five route results, and what to do with each

Read `results/<name>.json`. **Verify before integrating** — the project rule is
that the root agent re-derives every claim in exact rational arithmetic from the
statement, not from the route's code.

* **`precondition.json`** (strict-progress). Answers its decisive question NO
  unconditionally, and claims a *sixth* polynomial class (the "contracted" class:
  the first-passage chain on the controlled vertices with self-returns removed),
  with a family `Y_D` outside all five existing classes. Its significance audit
  also returned (`audit-precondition-significance.json`) and is unusually
  detailed: it confirms `Y_D` independently, **refutes `prop:prec-Gm(b)`**
  (Λ(WD(e,j,m)) depends on `max(e,j)`, not on `e` alone; 24 of 49 triples fail),
  flags `thm:prec-rate` as Blondel–Nesterov (a ninth rediscovery — attribute),
  and identifies `thm:prec-target` and `prop:prec-onectrl` as restatements of
  `prop:bracket(d)` and `thm:decide-one-bit`. Its integrate / repair / exclude
  list is the best starting point for the next session.
* **`bsi-rounds.json`** (strict-progress). Claims the no-stall theorem
  strengthens to a **strict lexicographic potential** (max gap, then |argmax|) on
  pairs, i.e. a round bound for bidirectional improvement. **Audit this hardest**:
  a polynomial bound here would settle the whole problem, so the prior is that
  something is wrong. Counter-evidence already collected by the root agent: a
  vertex *can* be switched twice (see below), so no "each vertex switches once"
  argument is available.
* **`free-search-b.json`** (strict-progress). "The value alphabet": val is the
  least fixed point of the *up-rounded* Shapley operator on any finite grid
  containing it, on arbitrary SSGs.
* **`free-search-14.json`** (strict-progress). The one-player case of the missing
  all-switches family is the published open problem for Howard's rule.
* **`coin-bias.json`** (dead-end). Closed twice over; read the argument, then
  record the closure in the paper if it is sound.

## The four routes that never returned

`allsw-lower` (the superpolynomial all-switches family — the pivot),
`lasserre-2`, `lcp-handicap`, `allsw-degeneracy`. Their transcripts are in
`transcripts/`. Re-running the script re-runs them from scratch.

## How to relaunch

`resumeFromRunId` is same-session only, so the original run
(`wf_0aa30f91-0f7`, task `w450bja02`) cannot be resumed from a new session.
Relaunch the script instead:

```bash
cp /data/ssg-proof/rounds/round14/round14.js /tmp/claude-1000/-data-ssg-proof/<session-id>/scratchpad/round14.js
```

Then call the Workflow tool with that `scriptPath`. Before doing so, edit two
things at the top of the script:

1. `SCRATCH` — it points at this session's scratchpad directory and must be
   changed to the new session's.
2. the `ROUTES` array — drop the routes whose results are already in
   `results/`, and keep `allsw-lower`, `lasserre-2`, `lcp-handicap`,
   `allsw-degeneracy`.

Model policy, set by the user: routes run on Opus 5 by default, **at most three**
on Fable 5.1 (reserved for the hardest or most valuable routes), and adversarial
audits always on Opus 5. In the script this is the `model` field of each route
and the hard-coded `model: 'opus'` on the audit agents.

## The root agent's own work this session (`harness/`)

Written from the definitions in `frontier.tex`, independent of any route code,
exact rational arithmetic throughout. Import next to the round-13 harness
(`mycore.py` and friends), which these files depend on.

* `bsi.py` — bidirectional improvement (both the veto and the strict variant),
  all-switches with productive-round counting and tie counting, the dual game,
  the disjoint-union gadget, the ladder, and a fast exact `w*` by Hoffman–Karp.
* `bsihunt.py`, `bsihunt2.py` — hill-climbs for slow bidirectional-improvement
  instances; the second also counts vertices switched more than once.
* `t_bsi14b.py`, `t_bsi14c.py` — the baseline tables.

Findings, all reproduced in exact arithmetic:

* The no-stall theorem holds on 150 random two-player stopping games × 8 starts,
  zero violations, at most 4 rounds.
* **On a one-player stopping game the rule is trivial**: with Min absent the
  guide `val^tau` is exactly `w*`, so the veto admits only greedy switches and
  the rule halts within |Vmax| rounds — one round on the ladder, measured to
  n = 12, and 112 random one-player runs never exceeded |Vmax|. So every
  one-player family in the paper (`WD`, `CC`, `H_m`, `L_n`) is useless for
  testing it, and the disjoint union of a game with its dual does not couple the
  two tracks either (1–4 rounds up to N = 43).
* The hill-climb's best was 12 rounds on 22 vertices, driven by a long Min
  chain, and `bsihunt2` found an instance where a vertex is switched **twice**.

A family that stresses the rule must therefore couple the two tracks through
shared vertices, and must be two-player. That is the open item.
