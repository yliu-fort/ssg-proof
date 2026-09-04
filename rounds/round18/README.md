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
- 09:39 UTC: the `eval-decision` route died on `max_output_tokens` (one
  reasoning turn of 64000 tokens, at effort xhigh; nine tool uses, no file
  written); relaunched at 09:43 UTC as run `wf_49cdc87a-da0`
  (`round18b.js`: the single route at effort high with a pacing sentence,
  its two audits, no paper audit).
- 11:17 UTC: the main run completed: 19 of 20 agents returned (the paper
  audit at 09:31, the six routes between 09:17 and 10:53, their twelve
  audits between 09:29 and 11:15), 5.6M subagent tokens, 2 h 32 min. The
  root agent verified every load-bearing claim in exact arithmetic before
  integration (`scripts/round18-verify/`), applied each route only after
  both its audits, and integrated in batches P, A, B, C, D, E, F (below).
- 12:04 UTC: the relaunched `eval-decision` route and its two audits
  completed (`wf_49cdc87a-da0`); verified, audited and integrated as batch G.

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
| `drive-line` | 09:50 UTC | new-theorem | `dl_verify.py`: the combed-flip law and the acyclicity clause exhaustive over all USOs of the 2- and 3-cubes (8928 flips), the parity law over all pairs, $B^2$'s 17 combed edges, sign $+1$, $d(B^2,B^2(\cdot\oplus z))=42,52,32,44$; `dl_line.py`: the level-two block's drive line recomputed from `B2_small_nf.json`: the same 14 cells, 13 fences (all simple, all combed), geodesic of length 8; `dl_escape.py`: the escape level theorem reproduces the whole outmap $B^2$ of the 138-vertex game from three drives and one comparison, $\Theta_w=2036/3313$, $\Theta_u=2048/3313$; the tournament argument and the no-$\beta$-translate bit table checked by hand; `dl_bfs.py`: the monotone reachability searches node-for-node | novelty: new-theorem on ONE result (`dl:no-beta-translate`, a new-relation; `dl:escape-level` a strengthening of `prop:pinned-level`; the combed-flip graph does no work, `dl:drive-flip` is `lem:flat-class`(a), `dl:fences`(a),(b) is `lem:readout`(a), `dl:b2-line` was already computed by the round-17 correctness audit, `dl:b2-distance` consequence-free by the route's own account; the auditor supplied a three-line proof of the no-$\beta$ theorem needing none of $\alpha$'s rows); correctness: sound, everything reproduced node-for-node (minors: the acyclicity-restricted distance mislabelled $D$, the window sentence of (c) false as stated though the comparison holds on the wide interval, the walk/non-walk contrast wrong, `dl:fences`(c) needs isolated ties, the search described inconsistently; the auditor completed the $z=10$ monotone search: none) | batch C, commit below: after `rem:pinned-escape`, `def:escape-ext`, `thm:escape-level`, `thm:escape-no-beta` (in the auditor's wider form: any outer pair whose drive's switch row reads only the block and whose rest row reads the partner positively; hence all four doublings excluded when the drive is $\alpha_2$), `thm:escape-mixed`, `cor:escape-m3`; the exact drive line (13 fences, all simple and combed, the geodesic) as data in `rem:pinned-escape`; abstract and summary aligned |
| `rlt-two` | 10:20 UTC | new-theorem | `rl_verify.py`: the level-one choice lift built as one exact LP (Balas' homogenisation) on 120 random one-player stopping games, the merged matrix $M$ and its transience (an M-matrix test) recomputed from first-passage laws, $\max_{R_1}x=w^*$ at every Max vertex whenever $M$ is transient (119 cases); the router trees $T_2(3,\tfrac14)$, $T_3(3,\tfrac14)$, $T_1(3,\tfrac12)$ rebuilt from the definition: stopping, $w^*=\kappa$, $\max_Q x(\mathrm{root})=1$, the explicit level-one point verified in $Q$ and in $R_1$ by per-vertex Balas LPs, root values $\tfrac47,\tfrac8{11},\tfrac23$, the merged bound $D\le MD$ on it; the proofs of the merged bound and of the splitter corollary checked by hand | correctness: new-theorem with `rl:modulator` STRUCK (false as stated: the freezing of `thm:modulator` retypes with an arbitrary payoff, the route's freezes to an action; on $T_2$ the two numbers are 1 and 3), the attribution to `rem:choice-lift` fabricated, `rl:cone`'s witnesses never built as games; the router tree confirmed at seven sizes up to $N=263$; novelty: new-theorem, `rl:levels`/`rl:cone` theorems about a level-$j$ lift the paper never defines, `rl:where` citing the unproved round-17 clause, the 'smallest instance' false ($T_1(2,\tfrac38)$ on 10 vertices straddles), the straddle corollary dropping a hypothesis, the ladder witness wrong ($\rho_{\max}(L_n)=0$; $W_{14}$ is the witness) | batch D, commit `11267d9`: `prop:router-tree` (the family, its values, the explicit level-one point, the straddle on 10 and 14 vertices, under the theorem's full hypothesis) and `rem:merged-matrix` (the level-one bound and the no-splitter criterion; the higher levels only as the route's own formalisation; the modulator identification recorded as refuted) after `rem:choice-lift`; `rl:cone`, the tables and the enumeration not integrated |
| `convex-class` | 10:27 UTC | new-theorem | `hz_wedge.py`: M7 (tangent cuts of the complementarity sum at the $8\lvert C\rvert$ lexicographic optima of the Z-seeded transport polytope, all three readings) rebuilt from the statement: on $\mathrm{WD}(2j,j,j+4)$, $j=2,3,4$, $B=2^{-(e+1)}\bigl[\begin{smallmatrix}1&-\lambda\\-\lambda&1\end{smallmatrix}\bigr]$ from the game (in $\mathcal R$), round 0 silent, 12 cuts all valid at $w^*$, round 1 decides both Max vertices; `hz_ring.py`: HZ(4), HZ(6) from the game files ($N=6n^2+2$, stopping, reachable, $\lvert\Vmax\rvert=\lvert\Vmin\rvert=n^2/2$, $a=5n^2$, $P_a=\tfrac12\cdot$permutation, $B\succ0$ with $B-\tfrac14I$ PSD and singular, least value $2^{-n^2}$, one SCC holds all controlled vertices), the singular member, membership in $\mathcal R$ of $G_8$, $S$, $S_3$, $H_{3,4,5}$, CC, $R$, the 7-vertex stall, BC(2,5) (BC(3,5) outside); `hz_w7.py`: M7 decides vertex 4 of the seven-vertex stall at round one, HZ's reduced $\tfrac12$-contraction; `hz_bc.py`: BC(2,5) decided at round one here (16 cuts; the auditor's implementation, with 4 cuts, at round two --- a tie-break matter) | novelty: new-theorem (weak), NOT sound as framed: the headline 'the hardest stalls all lie in R' false (BC($e\ge3$), CV outside), HZ($n$) polynomial by a reduced $\tfrac12$-contraction so not the member `rem:handicap-base` asks for, `hz:escape`'s general claim unproved, the phenomenon already in the paper on WD (M1, M(1,0) at round zero; Lasserre exact at $\lvert C\rvert=2$); what is new: an affine cut that is not a pairwise difference bound, outside `thm:convex-barrier-both`'s language, and one genuine decision; correctness: NOT sound (the BC round, the headline; minors: the tie-break unspecified, no bit-size bound, the exactness threshold off by 64, the escape step $2s<2^s$, the bisector sentence reversed, the singular instance's polytope a point), the core reproduced exactly | batch E, commit `05f4aab`: `rem:handicap-base` extended, `prop:handicap-singular`, `prop:hz` (reframed as a presentation artefact, polynomial by the reduced contraction) after `rem:handicap-base`; `rem:tangent-cut` after `rem:convex-barrier-both`, whose exclusion list gains the non-pairwise affine cut; the summary's mechanism paragraph |
| `beyond-holt-klee` | 10:53 UTC | new-theorem | `oc_verify.py` (+ `H11_m5_GAME.json` archived): the 260-vertex game rebuilt from its file: stopping, the printed normal form equals the game's first-passage laws (denominator $2^{13}$, $p^{v,a}_v=0$, every row leaks, $\rho=2047/2048$ over states), the outmap from the 32 exact value vectors equals the printed $s$, least margin $580908876268806955/409811754332034205696$, USO, acyclic, Holt--Klee by the harness's max-flow test, height 11, the run $10,17,6,21,22,24,4,8,12,28,30,31$, values nondecreasing along it | novelty: DEAD-END under the rubric (the object is the paper's own `thm:readout-realise`(b) at $r=1$; the record a strengthening of `prop:hstar-one-five`; the slope a restatement of `cor:stack-family`; `oc:diagonal` a restatement whose conclusion would mislead; the local-maxima counts follow from the combed criterion now in `rem:pinned-escape`; the m = 5 column does NOT close for $h^*_1$ with ties allowed) --- integrate the record; correctness: NOT sound (`oc:diagonal` REFUTED: it drops the peak law's second conclusion, which fails on every 2-face; its multi-switch clause false for general acyclic orientations), results 1, 2, 4 reproduced digit for digit, the m = 4 survey (5951 distinct classes) reproduced in full | batch F, commit below: `prop:hstar-one-eleven` after `prop:hstar-one-five` ($h^{*,\mathrm{nd}}_1(5)=h^*_{LP}(5)=h^*_{HK}(5)=11$, the normal form and outmap printed, the stacking slope $11/6$); `rem:four-ceilings` (LP row 11, $h^*_1$ row $\ge11$), `cor:stack-family`, `rem:hk-survey` (the 6113-class survey, the smallest unresolved class, the open m = 6 walk), abstract and summary aligned; `oc:diagonal` and `oc:local-max` not integrated |
| `eval-decision` | relaunched 09:43, returned 12:35 UTC (effort high) | new-theorem | `ed_onequery.py`: the one-query lift on 300 random systems (row in the simplex, stopping kept, query reproduced, value 1 after the switch); `ed_cert.py`: both adversary certificates rechecked from the rows alone (tree completeness, every NO world stopping, nondegenerate, $\mathrm{val}^*(v_0)<\tfrac12$, last query switchable, consistent with all ancestors; every YES witness stopping, nondegenerate, $\ge\tfrac12$, consistent with the whole path): 16 nodes at $m=2$, 400 at $m=3$; `ed_ratrow.py`: the rejection gadget on nine rational rows; `ed_games.py`: every world ASSEMBLED as an SSG through the gadget (which the route never did) and checked from the game with the harness --- all 32 at $m=2$ (31--191 vertices), all 4800 gadgets at $m=3$ from their built trees and the 205 smallest $m=3$ worlds in full (games up to 3863 vertices); the realised sizes 191 and 3863 computed, not the route's $10^4$ | novelty: NEW-THEOREM by the letter, footnote by the meaning (the fibre object is `thm:eval-queries`' own; the dimension clause false as an equality; the sparsity corollary unproved over the STOPPING members; the general headline a two-size certificate; prune hard, keep the rational-row lemma, the one-query lift, the level lift and the two certified sizes); correctness: NOT SOUND (two majors: the level lift's stopping clause false under the route's reachability hypothesis, a two-vertex counterexample; the sparsity corollary asserted over the STOPPING members without proof; minors: the dimension clause, the epsilon-scaling step, the one-query title false when the recorded value is already $\ge\tfrac12$, the pursuit-game 'exactly' ignoring irrational members, `thm:contraction` cited where `lem:survival-contract` applies) --- yet both headline results reproduce completely: both certificates re-verified with independent code, d(G)=m on every NO world, all 832 worlds built as games (largest 3863 vertices), the interpretation softened to 'the same complexity up to one query'; every finding applied in batch G | batch G: `lem:rational-row` + `rem:rational-row` (with the relaxation of `thm:readout-realise`(b) to rational non-leaking pieces under a trap hypothesis, stated as unsettled) after `lem:dyadic-row`; `def:eval-data`, `rem:eval-fibre`, `lem:eval-one-query`, `prop:eval-lift`, `prop:eval-decide-lower`, `rem:eval-decide-gap` after `rem:eval-queries`; the abstract, the summary and `prop:hdp-eval`'s caveat pointed at it; the Moebius/vertex material and the decision criterion dropped as the audit asked |

## What the round changed, in one paragraph

Seven object-changing routes; every one returned (one after a relaunch), and
every one was cut hard by its audits --- the novelty audits ruled three of
the seven routes dead-end or blocked under the rubric and struck a headline
claim in four (the paper's "hardest stalls all lie in $\mathcal R$", the
modulator identification, the "$m=5$ column closes", the diagonal-labelling
theorem, the last refuted outright by its correctness audit). The paper
audit of the round-17 text found three majors, all repaired (batch P). What
survived and entered the paper: the one-player fold $\mathrm{OF}(D)$, on
which the stopping-probability path has $2^{m}-1$ breakpoints and is a
Hamiltonian walk of the Max cube, correcting `rem:fold`'s claim that the
device needs a Min vertex, with the undamped one-player response map proved
convex with exactly $2^{D}+1$ pieces (A); the escape shape of the third
level, its level theorem, and the proof that no outer pair whose drive's
switch row reads only the block and whose rest row reads its partner
positively can realise a translate carrying the drive's coordinate --- two
of the four doublings to $B^{3}$ dead for every block, all four when the
drive is $\alpha_2$, and over the level-two block only $z=8$ with a
mixed-sign rest readout left (C); the $m=5$ record $h^{*,\mathrm{nd}}_1(5)=h^*_{LP}(5)=h^*_{HK}(5)=11$
on $260$ vertices, found by a guided walk through realised orientations,
with the stacking slope $11/6$ (F); the router tree, on which level one of
the choice lift closes only a $\Theta(1/N)$ fraction of the transport
interval with one player and five average vertices, and the merged-matrix
bound on that level (D); the tangent cut of the convex complementarity sum,
sound on the handicap-zero class, an affine cut outside the certificate
method's language, deciding the wedge at round one and one vertex nothing
else decides, together with the closed forms placing WD and CC inside
$\mathcal R$ and BC, CV outside, the boundary of $\mathcal R$ attained,
and HZ$(n)$ --- outside every named bound as presented, yet polynomial by a
reduced $\tfrac12$-contraction, a companion to `prop:a-presentation` (E);
and, on the negative side, that black-box composition amplifies a value
gap by at most a linear factor without any admissibility hypothesis, with
the ruin chain tight, the free sink-adjacent comparison, and the
$\varepsilon$-order ladder whose middle is the promise-gap question (B).
And in the evaluation model the bit alone costs as much as naming an
optimal strategy up to one query at $|C|\le3$, by certificate: $|C|+1$
evaluations are necessary against the $|C|+2$ that suffice, the worlds assembled as games
through a rejection gadget that realises arbitrary rational rows (G).
The pivot is unmoved: no superpolynomial all-switches family, no
$B^{3}$; the escape route to $B^{3}$ is narrowed to one corner.

## Where the next round should start

1. $B^{3}$: the one surviving corner, $z=8$ with $R_\alpha-C_\alpha$ mixed in
   sign over a driven three-Max block (the published one, or one reading
   the level-three drive), as an exact infeasibility question in the
   seventeen parameters of `thm:escape-level` --- a certificate, not a
   search; and the second escape shape, an outer pair whose drive's switch
   row reads the partner as well.
2. The one-player half of the pivot: $h^{*,\mathrm{nd}}_1=h^*_{HK}$ at every
   $m\le5$; the guided walk at $m=6$ towards a height-$13$ Holt--Klee class
   and towards the height-$14$ blow-up $B_\varphi(s,13)$ was cut short
   (`rem:hk-survey`) --- a hit at $14$ would make the blow-up doubling
   one-player; and whether a degenerate five-state game beats $11$.
3. The law beyond Holt--Klee: an exact infeasibility certificate for the
   smallest unresolved $4$-cube class, uniform in the value configuration
   (a McCormick/RLT relaxation with a Farkas certificate).
4. A family in the handicap-zero class designed against the tangent cut
   (its cut points are lexicographic optima of the own-successor rows); and
   the damping closure of $\mathcal R$, open.
5. The fold fed back into its own drive: `prop:one-player-fold` shows a
   driven fold without feedback is a cascade and the path is never a run;
   a family must make the affine cascade carry the counter.
6. The evaluation-query decision problem is settled at $|C|\in\{2,3\}$ only
   (`prop:eval-decide-lower`); the general adversary is the missing sentence
   of `rem:eval-decide-gap`, and nothing there bears on the pivot. Two
   cheap checks are worth a route's first hour: whether the rational readout
   system of `thm:readout-realise`(a) satisfies the trap hypothesis of
   `rem:rational-row`, which would moot the dyadic question at the end of
   that theorem; and whether $|C|+1$ or $|C|+2$ is exact at $|C|=3$ (a
   depth-4 search, with an LP maximising the switchability slack instead of
   sampling the fibres).

## Integration commits

`fccc750` batch P (the paper audit's 3 majors and 10 minors; the harness
archived in `scripts/harness/`, the BC game files in
`scripts/round17-verify/`); `a7969fd` batch A (the one-player fold, the
convex one-player response map); `e10d4d8` batch B (the admissibility-free
amplification bound, the free pair, the $\varepsilon$-ladder); `35cea73`
batch C (the escape shape, `thm:escape-no-beta`, `cor:escape-m3`, the exact
drive line); `11267d9` batch D (the router tree, the merged matrix);
`05f4aab` batch E (WD and CC in $\mathcal R$, the singular member, HZ$(n)$,
the tangent cut); `295e1a6` batch F (the $m=5$ record, the slope $11/6$,
the survey); `f0295c1` batch G (the rational-row gadget, the decision
version of the evaluation model at $|C|\le3$). The paper stands at $244$
pages with no undefined references; the PDF is synced to gdrive:ssg-proof/.
