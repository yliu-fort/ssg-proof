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
| M3 | `rem:blowup-realise` | "the orientation oracle is weaker than the value oracle already at $m=3$" contradicted by its own numbers (4 out-set queries against $\lvert C
vert+2\ge5$) | "separated by nothing here"; the orientation oracle is the cheaper one on that data |
| m1--m10 | `rem:cyclic-antipodal` (the profile count: one profile goes straight to the sink, three enter the cycle; the 23/8-vertex conventions), `cor:pinned-no-doubling` (the definition misdescribed its own example and lacked a verb; the height-16 bound scoped to blow-up outmaps), `thm:convex-barrier-both` (its proof cited itself), `rem:choice-lift` (an unproved exactness clause marked as the route's claim), the summary's BC clause (the preorder-seeded combination is measured), `rem:order-unique` (UP $\cap$ coUP attribution), the `st2_nf.py` path, the BC game files (archived in `scripts/round17-verify/`; the harness archived in `scripts/harness/`), `rem:slack-grade` (both composites), `prop:cv-measured` ("between two and three times"), `rem:eval-queries` (a fragment) | all repaired as the audit proposed |

Not checked by the audit (recorded for a later audit): `prop:b3-outer`'s 194-vertex game; ST(1)/ST(2); `rem:bias-families`' BP(D) counts; `prop:bias-witnesses`' PATH games; `rem:discount-fold`'s $9D+3$ variant; `thm:eval-queries`' 136/194/344-vertex reproductions; `rem:choice-lift`'s level-two exactness; the round-17 backlog (untouched).

### The routes

| key | returned | route's verdict | root agent's own verification (`scripts/round18-verify/`) | audits | integration |
| --- | --- | --- | --- | --- | --- |
| `one-player-envelope` | 09:18 UTC | new-theorem | `of_verify.py`: OF(D) rebuilt from the statement, the tent identity at ten rationals and the full breakpoint structure (Gray walk, level $D-\nu_2(k)$) for $D\le9$, the affine cascade at every strategy and the run bound for $D\le5$, values from gated games with genuine average vertices (up to 281 vertices) by brute force; `ofc_verify.py`: OFC(D,k) rebuilt with a Kraft tree, the Chebyshev identity ($k\le6$, $D\le4$), per-level counts $k2^d$, gated games up to 409 vertices; `fold1p_verify.py`: the novelty auditor's undamped one-player fold, its closed form, convexity and the $2^D+1$ slopes $j4^{-D}$ for $D\le8$ (the count then PROVED by a sign count) | correctness: sound, everything reproduces (Sturm root counts; minors: the switchability biconditional false at ties, cor(b)'s false clause, the gap misattributed to `rem:discount-fold`, two unstated steps in the seed's size bound, two mis-citations); novelty: DEAD-END under the rubric (`ue:path-not-run` = `cor:law-u`, `ue:cascade` = `thm:component-bound` and weaker than $\mathcal K_1$'s $D+1$, `ue:pgf` = `rem:discount-path`; the one-player fold itself is a strengthening that corrects `rem:fold`'s "whole device"; the auditor proposed the undamped one-player fold with $2^D+1$ response pieces) | batch A, commit below: `prop:one-player-fold` + `rem:one-player-fold` after `rem:discount-fold` (OF(D), the Chebyshev seed's two-sided bound, path-not-run via `cor:law-u`, the no-feedback cascade via `thm:component-bound`, the convex one-player envelope with the Min counterexample); `prop:one-player-response` after `rem:fold` (convex, exactly $2^D+1$ pieces of slopes $j4^{-D}$, proved from the closed form); `rem:fold` and `rem:fold-width` amended; abstract, summary, `rem:discount-path`, `rem:discount-fold` aligned |
| `weakest-oracle` | 09:29 UTC | new-theorem | `wo_verify.py`: the free blocks H/M/L and the strict pair on 778 random reduced games (with the bracket), FB(L)$^\pm$ rebuilt for $L\le9$, the ruin chain's values and slopes (derivative $2i(K+1-i)/(K+1)$, not $(K+1)/2$ for even $K$), the tied copies; `wo_lip.py`: the admissibility-free Lipschitz bound on 300 random contexts, 228 not admissible | novelty: BLOCKED (three of five results restatements: the free pair is `lem:alphabet-cover` at the extreme letters plus the paragraph after `thm:top`; any-set is `prop:no-halving`(b); free-blind is `prop:locality` + `thm:decide-one-bit`; keep the admissibility-free bound with the ruin amplifier, two sentences on the free pair, one remark on the $\varepsilon$-ladder); correctness: NOT sound (two majors inside the Lipschitz result: the ruin composition is stopping only for a player-free plugged-in game --- with two players two adjacent copies form a trap --- and the derivative $(K+1)/2$ is wrong for even $K$; minors: Any-Decision undefined, the context-blind corollary without its stopping hypothesis, the bracket off by one iterate, the ladder's constants need dyadic $\varepsilon$, RUIN(1) is admissible; everything else reproduced exhaustively, 122040 games on three non-sinks) | batch B, commit below: `rem:no-amplification` corrected (admissibility not needed; the excluded replay loop is where amplification lives; the ruin chain with a player-free plug, derivative $2i(K+1-i)/(K+1)$, tight within a factor approaching $8/3$), two sentences after `thm:top`'s closing paragraph (the free H $\succ$ M $\succ$ L pair, any named set is `prop:no-halving`(b), the free datum decides no controlled vertex), `rem:eps-ladder` after `prop:bracket`'s remark (Ord/App/Gap interreducible for dyadic $\varepsilon$, target-equivalent for $\varepsilon\le2^{-N^\gamma}$ by padding, the middle is the promise-gap question) |
| `drive-line` | 09:50 UTC | new-theorem | `dl_verify.py`: the combed-flip law and the acyclicity clause exhaustive over all USOs of the 2- and 3-cubes (8928 flips), the parity law over all pairs, $B^2$'s 17 combed edges, sign $+1$, $d(B^2,B^2(\cdot\oplus z))=42,52,32,44$; `dl_line.py`: the level-two block's drive line recomputed from `B2_small_nf.json`: the same 14 cells, 13 fences (all simple, all combed), geodesic of length 8; `dl_escape.py`: the escape level theorem reproduces the whole outmap $B^2$ of the 138-vertex game from three drives and one comparison, $\Theta_w=2036/3313$, $\Theta_u=2048/3313$; the tournament argument and the no-$\beta$-translate bit table checked by hand; `dl_bfs.py`: the monotone reachability searches node-for-node | novelty: new-theorem on ONE result (`dl:no-beta-translate`, a new-relation; `dl:escape-level` a strengthening of `prop:pinned-level`; the combed-flip graph does no work, `dl:drive-flip` is `lem:flat-class`(a), `dl:fences`(a),(b) is `lem:readout`(a), `dl:b2-line` was already computed by the round-17 correctness audit, `dl:b2-distance` consequence-free by the route's own account; the auditor supplied a three-line proof of the no-$\beta$ theorem needing none of $\alpha$'s rows); correctness: sound, everything reproduced node-for-node (minors: the acyclicity-restricted distance mislabelled $D$, the window sentence of (c) false as stated though the comparison holds on the wide interval, the walk/non-walk contrast wrong, `dl:fences`(c) needs isolated ties, the search described inconsistently; the auditor completed the $z=10$ monotone search: none) | batch C, commit below: after `rem:pinned-escape`, `def:escape`, `thm:escape-level`, `thm:escape-no-beta` (in the auditor's wider form: any outer pair whose drive's switch row reads only the block and whose rest row reads the partner positively; hence all four doublings excluded when the drive is $\alpha_2$), `thm:escape-mixed`, `cor:escape-m3`; the exact drive line (13 fences, all simple and combed, the geodesic) as data in `rem:pinned-escape`; abstract and summary aligned |
| `rlt-two` | 10:20 UTC | new-theorem | `rl_verify.py`: the level-one choice lift built as one exact LP (Balas' homogenisation) on 120 random one-player stopping games, the merged matrix $M$ and its transience (an M-matrix test) recomputed from first-passage laws, $\max_{R_1}x=w^*$ at every Max vertex whenever $M$ is transient (119 cases); the router trees $T_2(3,\tfrac14)$, $T_3(3,\tfrac14)$, $T_1(3,\tfrac12)$ rebuilt from the definition: stopping, $w^*=\kappa$, $\max_Q x(\mathrm{root})=1$, the explicit level-one point verified in $Q$ and in $R_1$ by per-vertex Balas LPs, root values $\tfrac47,\tfrac8{11},\tfrac23$, the merged bound $D\le MD$ on it; the proofs of the merged bound and of the splitter corollary checked by hand | pending | pending (after `rem:choice-lift`) |
