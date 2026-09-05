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

## The root agent's two cheap checks (decision A4), done during the run

Both settled, with proofs, in `scripts/round19-verify/` (batch H). A
single-agent adversarial correctness audit (Opus 5, effort high, run
`wf_eac574a6-9fc`, 25 min, 199k tokens) reconstructed every step and
rebuilt every computation independently (300 stopping games, the star at
$m=2,3,4$, 777 member checks, 2800 fourth queries, the star on all 832
certificate worlds): the mathematics held; two clauses were false as
written and repaired (the lemma's statement said "supported in $U$" where
mass one is meant; a parenthetical about a seven-vertex "mixed-$\tau$"
witness was wrong --- that game's violation is a singleton, and with one
Min vertex a single $\tau$ always serves); nine minor points applied
("never survives $m+1$" qualified to the star's queries; naming counts
by depth; the 960 figure attributed to `ed_star.py`; uniqueness of the
fixed point under the trap hypothesis proved inside `cor:readout-exact`;
the corollary $d(G)=|C|$ for nondegenerate one-player games stated; the
two-player caveat and the orientation-oracle sentence made precise).

1. **The trap hypothesis holds.** The rational readout system that
   `thm:readout-realise`(a) delivers always satisfies the hypothesis of
   `rem:rational-row`: a violation --- a set $U\subseteq\Vmax$ at each of
   whose vertices some action has, under some Min strategy $\tau_v$, a
   first-passage law of full mass inside $U$ --- makes
   $W=U\cup\bigcup_v(\text{vertices visited before }\Vmax)$ a trap of the
   game in the sense of `lem:trapchar` (a trap needs only *some* in-set
   successor at each controlled vertex, so the $\tau_v$ need not agree),
   against stopping. Hence the two halves of `thm:readout-realise` meet:
   realisability by a nondegenerate stopping SSG is exactly realisability
   by a rational readout system with the trap hypothesis
   (`lem:readout-trap`, `cor:readout-exact`); the dyadic question at the
   end of the theorem no longer separates them, only the size does.
   `rr_trap.py`: 3000 random two-player games, no violation on the 332
   stopping ones, every one of the 2370 violations on non-stopping games
   yields the trap.
2. **$|C|+1$ is exact at $|C|\in\{2,3\}$, and $|C|+1$ suffice for every
   nondegenerate one-player game, non-adaptively.** The key is a lemma
   (`lem:eval-forced`): whether a query's answer lies in the affine hull of
   the recorded values is decided by a linear system $(\ast)$ in the data
   alone --- either every consistent system answers with the same hull
   point (the query is wasted) or none does (the rank grows). For the
   queries $e_1,\dots,e_m,0$ the system $(\ast)$ is never solvable, so the
   $m+1$ values are affinely independent and determine every row of the
   normal form: the bit and an optimal strategy from $|C|+1$ evaluations
   fixed in advance (`thm:eval-star`). With `prop:eval-decide-lower` the
   decision complexity is exactly $|C|+1$ at $|C|\in\{2,3\}$; naming costs
   at most that, and the certificates do not bound naming (NO world and
   YES witness share their optimum at 9 of the 12 depth-2 nodes at $m=2$
   and 242 of the 336 depth-3 nodes at $m=3$, `ed_naming.py`); also
   $d(G)=|C|$ for every nondegenerate one-player game, so `thm:eval-queries`'
   bound reads $|C|+2$ on that whole class, one more than needed. At $|C|=3$ a fourth query is wasted essentially only
   when it completes the three queries to a 2-face (`rem:eval-face`); on
   the route's depth-3 certificate exactly 149 nodes (144 face completions
   + 5 coincidences) admit a forced fourth query and the tree extends there
   and nowhere else (`ed_depth4.py`, `ed_corners.py`: at every node at least
   four of the five fourth queries are informative for every consistent
   world, by the sign of a multi-affine function at the eight corners of
   the fibre box), so the round-18 route's depth-4 search could not have
   succeeded. `ed_star.py`: rank $m+1$ and exact row recovery for
   $m\le6$; the lemma on 3300 (member, strategy) pairs; 960 = all face
   completions forced on 40 random systems; degenerate systems drop rank.

## Outcomes

(pending)
