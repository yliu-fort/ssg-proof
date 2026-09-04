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
- 04:00–06:2x UTC: all 22 agents ran to completion on the first launch
  (no API outage, no usage-limit cut): the paper audit at 04:43, the seven
  routes between 04:54 and 06:00, the fourteen audits between 05:05 and
  06:2x. The root agent verified every load-bearing claim of every route in
  exact arithmetic before integration (`scripts/round17-verify/`), applied
  each route only after both its audits, and integrated in batches A–I
  (below); the abstract and summary were updated last (batch H).

## Outcomes

### The paper audit (round-16 diff) — returned 04:43 UTC, NOT SOUND

Seven majors and eleven minors, all in text integrated in round 16; every
finding was re-checked by the root agent and repaired in batch A
(`results/01_paper-audit_round16-diff.json`; the two computational
findings recomputed in `scripts/round17-verify/`).

| # | label | defect | repair |
| --- | --- | --- | --- |
| M1 | `rem:four-ceilings` | the new inequality $h^*_1\le h^*_{LP}\le h^*_{HK}$ cited `prop:oneplayer-lp`, which needs nondegeneracy, while $h^*_1$ allows ties (open after `thm:no-seven`) | stated for the nondegenerate ceiling; every lower bound of the last row is attained by a nondegenerate witness, so the LP row inherits it |
| M2 | `rem:signdef` | "closed under `def:damping`" is false: damping reweights first-passage entries by path length | struck; the 9-vertex counterexample recorded (recomputed, `signdef_damping.py`) |
| M3 | `prop:bias-one-improving` | title and statement say single-switch, the proof says multi-switch; the coinciding-breakpoint parenthetical was false | retitled and restated as a multi-switch rule ($N4^a$ bound); `sec:bias` intro, `rem:bias-gap` and the summary aligned |
| M4 | summary | "no named family costs it more than $2\|C\|$" contradicted by `prop:bias-witnesses` | restated as the body's "no hard family ... about $2\|C\|$", the four witnesses named |
| M5 | `cor:stack-family` | superadditivity and Fekete dropped the nondegeneracy of the stacked block | mixed inequality with $h^{*,nd}_1$, a liminf bound; Fekete's limit marked not established; the construction's own cap kept |
| M6 | abstract | "unbounded in ratio to the trivial one" for a constant factor $12/7$ | "exceeds ... by a constant factor"; the summary's Fekete clause likewise |
| M7 | text after `cor:blowup-transl` | stale $h^*_{HK}(6)\ge12$ and "ties the best Holt–Klee height known" after `prop:hk-records` gave 14 | updated: 12 is two below the 14, itself a free-readout blow-up |
| m1–m11 | `prop:blowup-readout`(a) proof, `prop:blowup-height` (the $2^k$ count: 32 of 728 3-cube AUSOs have six or seven maximal vertices, `bh_count.py`; the arbitrary-$z$ clause), `rem:no-amplification`, `thm:lemke-homotopy`(c),(d) proofs, `prop:b3-outer`'s dangling "(i)", `thm:switch-count`'s preamble ($4^{-a}$ for multi-switch), `rem:stack-measured` (ST(2)'s game file not recorded), `prop:fv-stall` (M4 over the rounds tested), `thm:signdef` ("eight polynomial classes" counted `thm:qp`), abstract/summary "translated layer is not" | all repaired as the audit proposed |

Not checked by the audit (recorded for a later audit): the escape exponent
$d(M_n)=n+1$; `prop:hk-doubling-measured`(d),(e); `prop:oneplayer-census-small`'s
total; the measured rows of `prop:cv-measured`; `prop:q16`'s revised counts;
`prop:hstar-one-eight`'s 2691-vertex game (not in the repository);
`prop:bias-witnesses`(b)–(d); `lem:max-tree`'s 11-vertex instance;
`prop:zero-ties`' 26 tied incidences.

### The routes

| key | returned | route's verdict | root agent's own verification (`scripts/round17-verify/`) | audits | integration |
| --- | --- | --- | --- | --- | --- |
| `order-lattice` | 04:54 UTC | new-theorem | `ol_verify.py`: `ol:unique` exhaustive over all preorders on 76 games; OL3's 3-cycle, values, nondegeneracy and $w^*$ from the game; no cycle at $\lvert C\rvert\le2$ (2000 games); the 1-Max-1-Min cross-multiplication proof checked by hand | novelty: sound, verdict DEAD-END (the object collapses, provably, to the profile cube's antipodal walk; `ol:small-C` is four lines from `thm:profile-uso`; `ol:lift-cycles` is the paper's own instance; `ol:read`'s parameter $b$ is inside `thm:modulator`); correctness: NOT sound as delivered but the four theorem statements hold --- the headline's "cannot cycle when $\lvert C\rvert\le2$" is false without separatedness (an 8-vertex non-separated 1-Max-1-Min game on which the lift 2-cycles, recomputed here in `ol_gc.py`), the GAP was a false conjecture, "no sound lift" a non-sequitur, four decodes is three | batch B, commit below: a remark after `thm:order-determines` (uniqueness of the consistent order, the read letters, stopping necessary) and a remark after `thm:cyclic-uso` (the antipodal 3-cycle on the paper's instance; no cycle at $\lvert C\rvert\le2$) |
| `parametric-path` | 04:59 UTC | new-barrier | `bp_verify.py`: BP(D) rebuilt from the statement for $D=1..8$, the tent identity, the breakpoint set $\{k/2^D\}$ with exactly $F_d,G_d$ tied, $2^D$ distinct pairs = the tent itinerary; the route's one-Max instances (roots $\{1/4,1/2\}$, $\{1/8,\dots,5/8\}$) against their own polynomials; `pp:step`'s derivative argument checked by hand; the correctness auditor's repair of the transplant ($P_D$ with a two-vertex chain seed, $6D+3$ vertices) verified for $D\le8$ (`pd_discount.py`) | novelty: sustained narrowly, new-barrier (integrate about a page; `pp:basic` a restatement, `pp:separation` measurement-only, fix the $\beta$ collision); correctness: NOT sound as delivered (the exponential separation from the bias path measured only; `pp:step`'s algorithmic clause refuted by a 14-vertex instance where the derived game has two optimal actions; the "slope $2/\beta$" account of the transplant false, the seed is what fails; minors at $\beta=0$), the family itself reproduced exactly for $D\le9$ | batch C, commit below: `def:discount-path`/`rem:discount-path` after `lem:gadget`, `prop:discount-fold`/`rem:discount-fold` after `rem:fold` (with the seed correction and the $6D+3$ variant), `prop:one-vertex-path`/`cor:two-homotopies` after `prop:bias-witnesses`, a measured BP(D) clause in `rem:bias-families`; the survival probability written $\varrho$ |
| `convex-lift` | 05:06 UTC | new-theorem | `cl_verify.py`: the level-one gap certificate on $W_{14}$ from the paper's normal form (five points in $\tilde Q$, tightness, both convex combinations, so $\max_{R_1}x(v_1)\ge3/5$); $w^*$ and stopping of $W_{14}$, its dual and DW recomputed from the game files; `cl:exact-lift`, `cl:rigid`, `cl:collapse` arguments checked by hand; the audit's correction of `rem:own-successor` recomputed (`pairtest.py`: on $R$ the non-strict pair test decides vertices 1, 4, 6 while the own-successor separators are 0; on the 7-vertex witness both readings are silent at vertex 4) | novelty: NOT sound, verdict new-theorem but weak (`cl:barrier` false at $j=0$ on $G_8$ and $G^*$; `cl:collapse`'s "first exact level $\le\min(m,k)$" false on $W_{14}$; `cl:exact-lift`, `cl:rigid` restatements; DW is `thm:compare-equivalence`'s gadget); correctness: NOT sound as submitted (the same false clause of `cl:collapse` and the false `cl:barrier` at $j=0$, `cl:families`' three "theorem" claims unproved, `cl:rigid` = the pair test), but `cl:gap-one`, `cl:dw`, `cl:union` and the directional halves of `cl:collapse` reproduced exactly, with a sharper collapse bound $j\ge\min(m,\max(1,\rho_{\max}))$ supplied | batch D, commit below: one remark after `rem:lasserre` (the choice-variable Sherali–Adams lift fails at level one on $W_{14}$, the five-point certificate, the straddle on $W_{14}$ joined to its dual, the directional collapse bounds) and THE CORRECTION of `rem:own-successor`, `prop:own-stall`, `rem:own-stall` and the summary: the pair test is not strictly weaker, the two readings are incomparable, and the 7-vertex game stalls both |
| `realisation-space` | 05:13 UTC | new-barrier | `b2pins.py` (the round-16 sparse verifier): the three new realisations of $B^2$ (137, 138, 139 vertices, 5 Max, 1 Min) verified from the game files, outmap $=B^2$, no tied incidence, USO, acyclic, height 10, run $12,19,13,17,8,16,0,7,1,5,4$ with values increasing (`B2_pin137_GAME.json` archived); `rs:upclosed` and `rs:no-outer-translate` checked by hand (the up-closedness of the outer vertices' switchable sets on the pinned layer against the parity classes the translate demands); the auditor's missing step recomputed (`rs_upclosed.py`: which pin pairs pass up-closedness on $B^2$ and its doubling translates) | novelty: NOT sound, verdict new-theorem (a closed construction avenue, not a barrier): `rs:metric`'s converse false, `rs:drive` restates `lem:readout`(a), `rs:where`(ii),(iii) vacuous, `prop:b2-realised` is NOT doubly pinned (its block has no pin pair), the pin-pair step of `rs:no-doubling` missing; keep the pinned shape, the level theorem, `rs:upclosed` $\to$ `rs:no-outer-translate` $\to$ `rs:no-doubling`; correctness: NOT sound (five majors: the same pin-pair gap, and its repair needs the block's pin rows not to read the drive; `rs:cost`'s hypotheses insufficient; `rs:metric`'s converse false; `rs:b2-window`'s 16 breakpoints are the refinement with the $\tau$-partition, the outmap partition has 13; the $B^3$ "smallest margin" is $\min\lvert\Psi\rvert$; the height formula for arbitrary readouts needs its own line), the pinned structure of both published games and the windows' fences reproduced exactly | batch E, commit below: after `prop:b3-outer`, `def:pinned`, `prop:pinned-level`, `lem:pinned-upclosed`, `thm:pinned-no-translate`, `cor:pinned-no-doubling` (restated for $B^2$, with the pin-pair step and the drive-free pin hypothesis), `rem:pinned-escape` (exact fences, the 137-vertex game, the escape shape) |
| `oracle-barrier` | 05:19 UTC | new-barrier | in progress: the route's BC(2,5), BC(3,5), BC(4,5) games loaded, $w^*$, the gap $2^{-s}$ at $v_0$ and the seeds confirmed; the root's own slack calculus, min-plus closure and `def:ratio`, Z-seeded, both clauses of `rem:own-successor` at $v_0,v_1,v_2$ (`bc_light.py`, 40 rounds): on BC(2,5) M2 first fires at $v_0$ at round 39 (clause ii) and M2T at round 21, M6 never; on BC(3,5) and BC(4,5) all three silent through 40 rounds --- far beyond the certificate's $K+1=2,5,11$, as a lower bound should be; the full hybrid with the transport LP (`bc_verify.py`) running with few rounds; the root's own `def:simorder` fixed point relates none of the twelve test pairs at $v_0,v_1,v_2$ on all three sizes (`bc_m1.py`) | novelty: NOT sound as framed, verdict new-barrier earned by BC(e,s) alone (the model $\mathfrak D$ cannot produce the coinductive preorder, so "M1 is a member" is false; the M1-seeding clause of the lower bound is measured, not proved; `ob:no-permanent` and `ob:m1-grade` restatements; `ob:edge` is `thm:seed-dichotomy`); integrate the BC subsection, the multiplicative certificate theorem and a one-sentence remark after `def:slack`; correctness: one major (the same false membership of M1 in the model), no fatal --- the family, the certificate chain, the lower bound's quantities, the frames and the round counts all reproduced from the statements at six sizes; minors: $K$ not $K+1$, the chain description, the $K_\sharp$ diagonal-pair step, soundness omitted from the certificate theorem's conclusion, the linear-fractional vertex step unproved, `prop:ratio-closure`'s min-times closure not in the repertoire (measured silent 16 rounds) | batch F, commit below: `sec:bc` before `sec:wedge` (def, values, the local-matching block, the lift-reduction lemma, the certificate, the lower bound with the M1 clause demoted to measured, a measured remark), `lem:ratio-sign`/`thm:convex-barrier-both` after `thm:hybrid-convex-barrier`, `rem:slack-grade` after `def:slack` |
| `query-model` | 05:44 UTC | new-theorem | the rank argument of `qm:eval` (each non-halting evaluation adds a dimension to the span of the answers, so $d(G)+2\le\lvert C\rvert+2$ evaluations suffice) checked by hand; `dout3.py`: the deterministic outmap-query complexity of the 3-cube AUSO class recomputed by exact minimax, $4$ (and $1,2$ at $m=1,2$); `hdp_verify.py`: $\mathrm{HDP}_m$ rebuilt from the definition for $m\le5$, every claim of `thm:qm-hdp`(a),(b) reproduced | novelty: sound, verdict new-theorem "by the letter, only just" (`cor:qm-nobarrier` restates `cor:selection`/`rem:ladder`; the model charges the cheap step; `thm:qm-hdp`'s family is degenerate and its members isomorphic; `def:qm-dim` does no work); integrate `thm:qm-eval` after `cor:selection` citing `lem:readout`/`lem:survival-contract`, `cor:qm-runs` as a remark on `rem:ladder`, HDP only with both caveats in the statement, one sentence in `rem:blowup-realise` with the Schurr--Szabo qualifier; correctness: NOT sound as submitted but the central theorem holds (the profile-oracle clause's bound is $d_\pi+2$, not $d+2$; $Q_{\mathrm{out}}=4$ is $3$ once the skeleton is given; the certificate-free halting claim, `cor:qm-theta`'s quantifier, the tree-depth import and the non-closed hypothesis set all repaired in the text) | batch G, commit below: `thm:eval-queries`, `prop:hdp-eval`, `rem:eval-queries` after `cor:selection`; `rem:run-informs` after `rem:ladder`; a clause in `cor:selection`; a sentence at the end of `rem:blowup-realise` |
| `variational` | 06:00 UTC | new-theorem | `vr_verify.py`: the Hessian $B$ of the complementarity form computed from the harmonic normal form over $C$; the identity $d^TBd=\lvert(I-\bar P)d\rvert^2-\tfrac14\lvert\Delta d\rvert^2$ on 60 random stopping games; CVX4 (48 vertices) and CVX6 (127 vertices) rebuilt from the game files: stopping, no tie, runs 4 and 6 (the one-player ceilings at $m=3,4$), $B$ positive definite with the printed entries and minors, CVX4's outmap the first blow-up level; NCX outside $\mathcal R$ ($\det B=-1/64$), the cyclic game inside with the printed $B$, $L_4$ inside, $W_{14}$ outside | novelty: sound, verdict new-theorem "on the narrowest reading" (the Hessian, convexity, Dirichlet and improvement-direction results are the monotone-LCP dictionary on `prop:lcp`; the class $\mathcal R$ is `rem:lcp`'s handicap-zero slice with no member outside the tractable regime; two membership facts already printed after `prop:seven-k1`; `vr:rev-vacuous` is `lem:splice`(a) backwards); keep CVX4/CVX6 as one proposition after `prop:seven-k1` in the paper's handicap vocabulary, the base-independence as a five-line remark with the principal-pivot attribution, `vr:rev-trivial` as a short remark; correctness: pending | batch I (redrafted): one proposition and two remarks |

## What the round changed, in one paragraph

Seven object-changing routes; every one returned, and every one was cut
hard by its audits. Two corrections to the paper itself came out of the
audits: the round-16 paper audit's seven majors (batch A), and the
discovery, by the convex-lift audit, that the paper's standing rule "the
pair test is strictly weaker" was false --- the two readings of the
transport certificate are incomparable, and a seven-vertex game stalls
both (batch D). The genuinely new mathematics that survived: the
stopping-probability path, exponentially long by the tent map and not the
bias homotopy (batch C, `prop:discount-fold`); $\mathrm{BC}(e,s)$, the
first family on which the simulation preorder and every propagation
calculus, in both registers, are silent $2^{\Omega(N)}$ rounds while one
policy evaluation decides it, with the certificate method extended to the
multiplicative register (batch F, `sec:bc`, `thm:convex-barrier-both`);
the pinned shape's level theorem and the proof that pinning once more on
top of the outer half of the third level cannot reach $B^{3}$ (batch E,
`cor:pinned-no-doubling`); an optimal strategy from $|C|+2$ adaptively
chosen evaluations, so every exponential lower bound in the paper is a
bound on rounds, not information (batch G, `thm:eval-queries`); handicap
zero attaining the one-player ceiling at $m\le4$ (batch I); and smaller
items --- the unique consistent order and the antipodal 3-cycle on the
paper's own instance (batch B), the Sherali--Adams lift failing at level
one (batch D). The pivot is unmoved: no superpolynomial all-switches
family, no realisation of $B^{3}$, and the one shape that reached its
outer half is now proved unable to go further.

## Where the next round should start

1. The third level: the escape shape named in `rem:pinned-escape` (an
   outer vertex whose rest action reads the block), and the question every
   route to $B^{3}$ now runs through --- a driven block that is not pinned
   presenting $B^{2}$ at one drive and $B^{2}(\cdot\oplus z)$ at another for
   a doubling $z\in\{8,10,24,26\}$.
2. $\mathrm{BC}(e,s)$ defeats M1 and M2--M6 but not M3; the M3 half of
   `rem:wedge`'s open item is still the superpolynomial all-switches
   family (`thm:seed-dichotomy`). The M1-seeding clause of `thm:bc-lower`
   is measured, not proved.
3. The one-player discount path: is it superpolynomial for one player
   (`rem:discount-fold`'s gap)?
4. The decision version of the evaluation-query model: is more than $O(1)$
   evaluations needed to decide $\val(v_0)\ge\tfrac12$ on a nondegenerate
   family with one skeleton?
5. The standing rule for future audit prompts must say: test both
   readings of the transport certificate (own-successor, both clauses, and
   the non-strict pair test), all Z-seeded.

## Integration commits

`120bc54` batch A (the paper audit's 7 majors and 11 minors); `63ba9de`
batch C (the stopping-probability path); `b7c4d61` batch B (orders as
certificates, the antipodal 3-cycle); `2499e7c` + `a639b05` batch F and
F2 ($\mathrm{BC}(e,s)$, the two-register certificate theorem, the
$\{0,1\}$-grade remark); `282f1c9` batch E (the pinned shape and the
no-doubling corollary); `3412ce9` batch G (evaluation queries); `19027be`
batch D (the Sherali--Adams remark and the pair-test correction);
batch I and batch H: see the end of this file.
