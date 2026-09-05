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
- The run completed at 13:57 UTC: 25 of 25 agents, no errors, no
  relaunch, 6.03M subagent tokens, 2 h 45 min. Route returns and audits
  were dumped to `results/` (`dump19.py`; 25 structured returns plus the
  routes' LaTeX where it was a file), each route verified by the root
  agent in `scripts/round19-verify/` and integrated in batches (commit list
  at the end).

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

### The paper audit (round-18 diff) --- NOT SOUND: two majors, nine minors/notes, no fatal

Every finding was re-checked by the root agent and repaired in batch P
(commit `2067dc4`; `results/08_frontier.tex_round-18_diff.json`). The
auditor reproduced, from the statements alone and in exact arithmetic,
essentially every printed number of the 1317 added lines
(`prop:hstar-one-eleven`'s outmap, margin, heights and walk; the whole
drive line of `prop:b2-realised`'s block; the escape-level data; the
evaluation-model certificates; `prop:router-tree`'s points; ...).

| # | label | defect | repair |
| --- | --- | --- | --- |
| M1 | `thm:escape-mixed`(a) | clause (a) said $R_\alpha-C_\alpha$ has a strictly *negative* component; the proof gives a strictly *positive* one, and with the printed sign (b) and `cor:escape-m3`'s $z=8$ case were vacuous | sign corrected; the downstream statements re-read against it |
| M2 | `prop:own-stall`, proof | the parenthetical for clause (i) at a Min vertex printed the clause-(ii) expression, which is $\le0$ at every Min vertex of $Q(G)$ | clause (i) stated as $\mathrm{Sep}(v,v^{(i)})\le0$; the separators re-derived |
| m1--m9 | `rem:own-stall` ($\mathrm{Sep}(t_1,3)$, not $\mathrm{Sep}(3,t_1)$), `rem:one-player-fold` (the worst all-switches run of OF($D$) is exactly $D+1$, not the printed row; eight, not nine, average vertices per level, also in the summary), `prop:one-player-response` ($u$'s out-edges), `prop:router-tree` (the point of $Q$ attaining $1$ is not the all-ones vector), abstract and summary (the surviving corner scoped to the level-two block), `prop:hz` (the modulator and treewidth clauses justified or flagged), the free-datum paragraph after `thm:top` (FB($L$)$^\pm$ defined, the stopping hypothesis), `rem:eval-fibre`/`def:eval-data` (nondegenerate members; two-player $\mathrm{val}^*$), `lem:rational-row` (the trap step's case split), `rem:merged-matrix` ("first exact level" scoped), the paragraph after `prop:eval-lift`, `prop:eval-decide-lower` (vertex counts tied to the leaf order) | all repaired as the audit proposed |

### The root agent's two cheap checks --- batch H

Section above; commit `8059686` (`lem:readout-trap`, `cor:readout-exact`,
`lem:eval-forced`, `thm:eval-star`, `rem:eval-face`), after a
single-agent correctness audit of the root agent's own draft (two repairs:
"supported in $U$" is mass one; the seven-vertex parenthetical struck).

### The routes

All eight routes returned (one `Workflow` run, no relaunch); every route
was verified by the root agent from the statements, in exact arithmetic,
before anything entered the paper, and integrated only after both audits.

| key | route's verdict and headline | root agent's own verification (`scripts/round19-verify/`) | audits | integration |
| --- | --- | --- | --- | --- |
| `fresh-19` (blind: routings and the rotor game) | new-theorem; the $n$-chip rotor game's value is within $\tfrac12\sum_u\lvert\mathrm{val}(u^0)-\mathrm{val}(u^1)\rvert$ of $n\,\mathrm{val}(v_0)$ | `fr_root.py`: the routing formula and the nonemptiness lemma on random stopping and non-stopping games; $\det M=\lvert R\rvert=\det A_U\det A_{U^c}$; the rotor identity and the sandwich by exact backward induction on small games; E1 attains ($M(n)=n/2+1$); RC($m$) built as a game with $2\,\mathrm{OUT}_n>n$ through $n<7(2^m-1)$; period exactness; the retyping identity | correctness (result 04): SOUND, everything re-derived (2596 pairs, 60 games, the period gap measured); novelty (09): NOT sound as submitted --- two majors: the divisibility clause of the acyclic corollary, and the chip bound's $m$ range (needs $m\ge3$) --- the mathematics of routings and the rotor identity correct | batch B, commit `a4961b4`: `sec:routings` (`def:routing`, `lem:routing-nonempty`, `thm:routing` --- the round-10 forest balance finally enters, proved without the matrix-tree theorem ---, `cor:routing-det`, `rem:routing-attribution`, `cor:routing-acyclic` corrected, `prop:retyping`, `def:rotor`, `lem:rotor-terminate`, `thm:rotor-identity`, `cor:rotor-sandwich`, `rem:rotor-period`, `thm:rotor-chips` at $m\ge3$); the period-divides-$\lvert R\rvert$ conjecture recorded as measured |
| `escape-certificate` | new-theorem; over the level-two block with the outer pair $(\alpha_2,\beta_2)$ no doubling translate of $B^2$ is realised by either escape shape | `ec_root.py`: the block's drive line from `B2_small_nf.json` (the 13 fences of `rem:pinned-escape`, the refined breakpoints, affinity of every $y_\sigma$ between them); the two drive-map identities; the tournament, the LOW/HIGH windows and their pruning for the four $z$; the 104 Farkas certificates against rows rebuilt here; the second-shape level theorem from the route's two games (138 and 149 vertices) | novelty (07): new-theorem qualified --- `thm:ec-main` a new relation closing the corner `cor:escape-m3` left open; `prop:ec-criterion` and `cor:ec-no-beta-fails` do not hold as stated, `thm:ec-level2` a strengthening; correctness (12): NOT sound --- the same two results over-stated, one in a way that would settle the route's own gap; the central mathematics reproduces exactly | batch A, commit `a4961b4`: `def:escape-ext2`, `lem:escape-substochastic`, `thm:escape-level-two`, `lem:escape-identity`, `lem:escape-domination`, `thm:escape-block-closed`, `rem:escape-second-shape` (the tournament argument does not survive $A''>0$; the exact open case: the relabelled second shape at $z=8,24$); the criterion without its pairing hypothesis not carried |
| `promise-gap` | new-theorem; $\mathrm{Gap}_\varepsilon$, $\mathrm{App}_\varepsilon$, $\mathrm{Ord}_\varepsilon$ for $\varepsilon\ge1/\mathrm{poly}$ are polynomial-time equivalent to $\mathrm{Gap}_{1/4}$ | `pg_root.py`: the majority composite built as a game with value $3p^2-2p^3$ on 80 instances (two-level towers included); the level count from $\delta=2^{-3},\dots,2^{-16}$ certified by two-sided rounding against the proved bound; the influence bound on 1535 (acyclic context, positional pair) polynomials; the ruin composites (the two-player one is not stopping, the player-free one is, with the printed values); WELL$^\pm(K)$ at $K=8,10,12$: values, and value iteration, the bracket and the lower iterate against $Q=3^{h-1}/16$ | novelty (05): mathematics sound, self-assessment not (new-object `thm:pg-influence`/`thm:pg-acyclic`, new-relation `thm:pg-schemes`, strengthening `prop:pg-ruin`); correctness (15): NOT SOUND --- two majors in claims the proofs do not reach (the "no decision rule reading only them" punchline, refuted by the exact iterates, which separate WELL$^+(14)$ from WELL$^-(14)$ from $k=12$; and the second) --- the mathematics under them holds, four tables reproduced | batch C, commit `7a7d627`: `sec:promise` (`def:majority-context`, `lem:majority-context`, `lem:majority-levels`, `thm:gap-collapse`, `rem:gap-collapse`, `def:acyclic-context`, `thm:influence`, `thm:acyclic-square`, `def:well`, `prop:well`, `thm:well-schemes` stated about the *verdicts* read from the bounds, `prop:ruin-exact`); `rem:eps-ladder` pointed at it |
| `handicap-tangent` | new-theorem; $B\succeq\lambda I$ bounds the expected visits to $C$ by $3\lvert C\rvert/\lambda$, and the slice $\mathcal R_\lambda$ is a polynomial class | `ht_root.py`: $\kappa\le3\lvert C\rvert/\lambda$ on 120 random stopping members of $\mathcal R$ ($\lambda$ by exact bisection); $\sigma_n\le\kappa/n$ on 840 pairs; the reduced value iteration with continued-fraction recovery exact on 60 games; DR(8,38) and its damped game on 1082 vertices: $\det B_\rho<0$, so $\mathcal R$ is not closed under damping | novelty (11): new-theorem but small --- $\kappa$ is the paper's own survival quantity restricted to $C$ (round 13, (v11)); the separation from the escape class proved through `prop:hz`; correctness (17): NOT SOUND --- two majors (the sub-multiplicativity step `ht:thm-kappa` needed, and the deliverable (A) not achieved: no family in $\mathcal R$ on which the tangent cut is silent) --- the central mathematics holds, the visit bound confirmed on 250 fresh games | batch D, commit `7a7d627`: `def:visit-number`, `lem:handicap-visits`, `lem:visits-nonstationary`, `lem:visits-decay`, `thm:visits-class`, `cor:handicap-slice`, `prop:handicap-damping`; `prop:hz`'s exactness clause, `rem:handicap-base`, `rem:tangent-cut` aligned |
| `hk-law-certificate` | new-theorem; the Holt--Klee class $s_0$ of height 2 is not one-player realisable, so at $m=4$ realisability is strictly stronger than Holt--Klee | `hk_root.py`: $s_0$ and its facet datum $(t,\chi)$; the 43 route systems realise $t$ with the five determinant signs and the Radon signs of $\chi$ (300 perturbations the same); the census scan: 17 classes carry the datum, 13 Holt--Klee of heights 2,3,4 in multiplicities 3,6,4, $s_0$ among them | novelty (16): NEW-THEOREM, "the strongest of the round's realisability work", the headline supported word for word, closing the gap the round-18 novelty audit named; correctness (20): SOUND, every step re-derived, five notes and one write-up slip | batch E, commit `0631fe3`: `def:facet-datum`, `lem:facet`, `thm:facet-obstruction`, `thm:hk-not-sufficient`, `rem:hk-law`; `rem:hk-survey` and the summary aligned |
| `m6-walk` | new-theorem; no one-player game with $\lvert\Vmax\rvert=5$ has an all-switches run of length 12, degenerate or not, so $h^*_1(5)=11$; a 418-vertex nondegenerate game of height 13 at $m=6$ | `mw_root.py`: the flip criterion exhaustive at $m\le3$ (744 USOs, 8928 reversals, 48 acyclic-to-cyclic; the example's actual cycle $1\to5\to4\to6\to2\to3\to1$); an own walk-then-complete enumeration --- 48 at $(4,7)$, 480 at $(5,12)$ equal to the route's list, none at $(5,13)$ --- and the (F1)--(F4) partitions: 240 admit one, unique, the start edge, $x$ equidistributed; the 418-vertex game from its file (stopping, rows, 64 values, outmap, margin, USO/acyclic/Holt--Klee, height 13 at $\{25,27,57,59\}$, the run, longest run 13); the level-two block's 14 cells from the normal form, every fence simple, the edge list (first edge $(4,\alpha_1)$, not $(4,\beta_1)$), $\{3,7\}$ reversed twice, flip distance 11 | novelty (18): new-theorem, "but barely, and on a different result" --- the bar met by the monotone drive lines with the level-two return (an obstruction invisible cell by cell) and by the cell theorem; `mw:no-twelve` and `mw:h13` strengthenings, verified; correctness (21): sound=false only on the cell theorem's fence bound, which needs affine drive lines; everything load-bearing reproduces (480 orientations, the game, the block; minors: the edge name, the cycle example, the uncertified search state) | batch F, commit `e5c509a`: `lem:flip-criterion`, `lem:drive-monotone`, `prop:b2-return` after `rem:pinned-escape`; `lem:twelve-flat`, `thm:no-twelve`, `rem:no-twelve-scope` in `sec:ties` replacing the "cannot be enumerated" paragraph; `prop:hstar-one-thirteen`, `rem:walk-state` (flagged as the route's report); `cor:hstar-one`, `rem:four-ceilings` (LP and one-player rows $1,2,4,6,11,\ge13,\ge14$), `prop:hstar-one-eight`, `cor:stack-family` ($13/7$), abstract and summary aligned; `mw:w3`, the cell theorem and the $W_m$ subsection not integrated |
| `fold-feedback` | new-theorem; every all-switches step of a fold cascade is one of $m$ maps, and the mismatch level climbs unless the drive leaves its cell | `ff_root.py`: the B-map on 5997 random nondegenerate configurations (gains in $[2,6)$, $m\le6$, one and two players); the route's eight games FF1/FF2($D\le4$) from kinds and successors: stopping, the cascade coefficients read off by first-passage laws (every gain 2, $\mathrm{val}(Y_0)=\tfrac12$), exact all-switches runs from every start with Min optimal, maxrun $=m-1$, the identities and the B-map prediction at every nondegenerate round, the route's recorded runs matched; the relabelling counts for $B(1\text{-cube})$'s two walks (2 and 4 of 48) and $B^2$'s (none of 3840) | novelty (19): new-theorem, narrowed --- `def:ff` a new object, the deliverable the proved collapse at $m\le4$; three restatements, `thm:ff-exhaust` an overclaimed equivalence; correctness (22): NOT SOUND, six majors (the "attained only by the constant drive" clause false; the LP's undeclared loop-gain cap and cell shrinking; $a_d=0$ and two $c$-families only; `lem:ff-response`'s bound false; `cor:ff-parity` over-cites `cor:parity-unreadable`; `cor:ff-level0` a restatement) --- `thm:ff-bmap` sound and stress-tested, the games check out, the numbers of the search reproduce with the restrictions relaxed | batch G, commit `d655106`: `def:ff` (normalised, the average excursion), `thm:ff-bmap`, `cor:ff-climb` (the cell lemma folded in), `rem:ff-measured` (the $m\le4$ search as a measurement over two families, the auditor's relaxation and correction, the sign-reading gadget in one sentence), `prop:ff-blowup`; `rem:one-player-fold` pointed at it; `cor:ff-level0`, `lem:ff-response`, `cor:ff-parity` and the equivalence not carried |
| `extension-complexity` | new-theorem; level two of the choice lift is exact on the router trees $T_1(2,\tfrac38)$, $T_2(2,\tfrac38)$ (the headline the novelty audit struck); the value polytope $V(G)$ and the ladder's as a parallelotope | `xc_root.py`: the ladder $L_n$ built from `def:ladder`, all $2^n$ value vectors for $n\le10$, $\varphi_i(\mathrm{val}_\sigma)=\bigoplus_{k\ge i}\sigma_k$ exactly; the proof that $R_1$ is Balas' closure and that $R_{\lvert C\rvert}=\{w^*\}$ checked by hand | novelty (24): new-theorem at the minimum bar only, carried by `xc:ladder`; the hierarchy restates `rem:choice-lift` (what is new: the programme (L1)--(L4), a proof of the Balas parenthetical, $R_{\lvert C\rvert}=\{w^*\}$), the headline struck (`prop:router-tree` already records level two as measured), CYC dominated by WD(4,2,6), Yannakakis without SSG content; correctness: see below | batch I (see below) |

**`extension-complexity`, correctness audit (result 25): NOT SOUND, headline reproduces.** The auditor rebuilt every game and number from the statements with its own exact simplex: on the paper's own 10-vertex $T_1(2,\tfrac38)$ and 14-vertex $T_2(2,\tfrac38)$ (the route had built 12- and 20-vertex variants with a damping chain per leaf --- the same first-passage data, so nothing changes, but not the instances `prop:router-tree` defines) the lifts give sum-ranges $[9/8,3],[9/8,3/2],[9/8,9/8]$ and $\max_{R_1}=72/17$ with $R_2=\{w^*\}$, so $\operatorname{lev}=2$ exactly; the ladder identity for $n\le12$; CYC, AND, the exit matrices reproduce. Three majors: the closing clause of the Balas-iteration lemma ("a necessary condition for $\operatorname{lev}\ge j+2$ is that $R_j\cap F^i_v$ is nonempty for every $v$ and both $i$") is FALSE, refuted by a 13-vertex stopping game, and the route's search plan rests on it; the sentence "the vacuity does not grow with $d$" is an extrapolation from two exact points inside a proposition marked proved; the $8\cdot10^5$-system search is floating point (HiGHS, tolerances $10^{-8}$) under a heading "all exact". Minors: the conditioning lemma needs the one-line case for pairs whose $A'$ meets $B$ (supplied); `xc:onectrl` needs $p^{v,i}<1$; the exit remark's "level-$j$ form" overstates; the "only form in which extension complexity bears on the problem" clause is misleading (a lower bound would close only that route); the occupancy remark's positive half needs one player. **Batch I, commit `e76c8a1`:** `def:choice-lift`, `lem:choice-lift-balas` (with the auditor's case; the router-tree exactness credited to route and auditor; the searches marked floating point), `rem:value-polytope` (the "only form" clause replaced by "no barrier") after `rem:choice-lift`; `rem:choice-lift`'s parenthetical and `prop:router-tree`'s closing clause aligned; the headline, CYC, the exit bound, the Balas-iteration lemma, Yannakakis, the occupancy remark not carried.

## What the round changed, in one paragraph

Eight object-changing routes, all returned in one run, all cut by their
audits: the novelty audits sustained new-theorem for every route but
struck a headline in two (the extension-complexity route's router-tree
exactness, already recorded; the m6-walk route's leading result, whose bar
was met by a different theorem), and the correctness audits found the
mathematics under every route sound while refuting six clauses as stated
(the fold-feedback route's uniqueness clause and drive-response bound, the
escape route's criterion and no-$\beta$ corollary, the promise-gap route's
"no decision rule" punchline, the m6-walk route's cell-theorem fence
bound). The paper audit of the round-18 text found two majors, both
repaired (batch P). What entered the paper, all of it re-verified by the
root agent: the one-player ceiling is now exact with ties at every
$m\le5$ --- no one-player game with five Max vertices runs twelve rounds,
by an enumeration of the 480 height-12 orientations of the 5-cube and the
one tie each admits --- and stands at $\ge13,\ge14$ for $m=6,7$ on a
418-vertex nondegenerate game found by a walk through realised
orientations, with the stacking slope $13/7$ (F); Holt--Klee is *not*
sufficient for one-player realisability at $m=4$: thirteen Holt--Klee
classes carry a facet datum no nondegenerate one-player game presents, by
a Radon-circuit certificate uniform over all realisations (E); the last
open doubling corner of the level-two block is closed by an exact
certificate for both escape shapes, and the remaining question is the
relabelled second shape at $z=8,24$ (A); the level-two block's drive line
reverses one edge twice, which no one-player driven block can do, so its
Min vertex shapes the line and not only the outmap, with the single-edge
reversal criterion proved (F); every all-switches step of a fold cascade is
one of $m$ maps and the fed-back fold collapses at $m\le4$, while the
height-doubling device is not a fold from level two on (G); the promise
problems $\mathrm{Gap}_\varepsilon$ for $\varepsilon\ge1/\mathrm{poly}$ are
one problem, value iteration and the damped path fail it for $2^{\Omega(N)}$
rounds on player-free wells, and the influence of one coin on an acyclic
context is bounded (C); the value of a positional pair is the fraction of
acyclic selections routing to $t_1$, the round-10 forest balance finally
proved, with the rotor game as its deterministic shadow (B); the visit
number bounds the strongly convex slice of the handicap class into a
polynomial class, and the class is not closed under damping (D); the
evaluation-query decision problem is settled at $\lvert C\rvert\le3$ and
the dyadic question of `thm:readout-realise` is moot (H); the ladder's
value polytope is a parallelotope, closing the extension-complexity
direction, and the choice hierarchy has its programme and its level-one
identification proved (I). The pivot is unmoved: no superpolynomial
all-switches family, no $B^3$, and the one-player ceiling still one below
the Holt--Klee one at $m=6$.

## Where the next round should start

1. $B^3$: the one case `thm:escape-block-closed` leaves --- the relabelled
   second shape, the outer pair $(\beta_2,\alpha_2)$ with $A''>0$, at
   $z=8$ and $z=24$ (`rem:escape-second-shape`) --- as an exact
   infeasibility certificate; and whether the tournament argument of
   `thm:escape-no-beta` has an analogue under $A''>0$.
2. The one-player half of the pivot: $h^*_1(6)\ge13$ against
   $h^*_{HK}(6)\ge14$; the walk at height 13 found no height-14
   orientation within flip distance two of 475 realised ones
   (`rem:walk-state`, the route's report) --- a hit at 14 would make the
   $4\to6$ doubling one-player; and whether $h^*_1\le h^*_{HK}$ beyond
   $m=5$, which the enumeration method cannot reach.
3. The law beyond Holt--Klee: `thm:hk-not-sufficient` excludes 13 of the
   162 open classes of the 4-cube; the missing statement is whether
   co-realisability of every facet datum together with Holt--Klee
   characterises one-player realisability at $m=4$ (149 classes left).
4. The handicap class: $\mathcal R_\lambda$ is polynomial and $\mathcal R$
   is not closed under damping; no family in $\mathcal R$ silences the
   tangent cut --- either find one or prove the cut decides every member.
5. The fold fed back into its own drive is closed for the pivot
   (`prop:ff-blowup`: the doubling device is not a fold); what remains
   there is only the general bound, uniform as the loop gain tends to 1,
   on the number of cell crossings a monotone drive can make.
6. The promise gap is one problem, $\mathrm{Gap}_{1/4}$; the wells show
   what fails at $\varepsilon=\tfrac14$ (value iteration, the bracket, the
   damped value) --- the open question is a rule reading more than those.
7. The choice hierarchy: no stopping game with $\operatorname{lev}\ge3$ is
   known and exactness of level two is target-equivalent, so not
   conjectured; a candidate must keep both level-one faces alive at every
   controlled vertex and be non-flat (the routes' 848 197 random systems
   never failed at level two). The rotor game's period-divides-$\lvert R\rvert$
   conjecture is measured only.
8. The evaluation model is settled at $\lvert C\rvert\le3$
   (`thm:eval-star`); the general adversary is the missing sentence.

## Integration commits

`e3a1e99` brief, routes, inventory, launch record; `cc74610` the two cheap
checks (scripts and README); `8059686` batch H (the root agent's two
results); `2067dc4` batch P (the paper audit's two majors and nine
minors); `a4961b4` batches A (escape-certificate) and B (fresh-19);
`0631fe3` batch E (hk-law-certificate); `e5c509a` batch F (m6-walk);
`7a7d627` batches C (promise-gap) and D (handicap-tangent); `d655106`
batch G (fold-feedback); `e76c8a1` batch I (extension-complexity); then the round's README and the
root README.

