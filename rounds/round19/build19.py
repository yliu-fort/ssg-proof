#!/usr/bin/env python3
"""Assemble rounds/round19/round19.js from rounds/round18/round18.js.

The common digest, the rules, the schemas and the audit lenses are sliced
from round 18's script and patched (the repository paragraph, the inventory
path, the round-18 addendum, the scratch paths, the new required field
games_built, the round-18 lessons); the eight route briefs come from
routes19.txt; the paper audit is rewritten for the round-18 diff.
Run from the repository root:  python3 rounds/round19/build19.py
"""
import re, sys
REPO = '/data/ssg-proof'
SC = '/tmp/claude-1000/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/scratchpad'
R18 = '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad'
R17 = '/tmp/claude-1000/-data-ssg-proof/d1fe2115-9b72-4784-bb94-87421ac1106c/scratchpad'
old = open(f'{REPO}/rounds/round18/round18.js').read()

def esc(t):
    return t.replace('\\', '\\\\').replace('`', '\\`')

def replace_once(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:80])
    return s.replace(a, b)

# ---------- COMMON: slice round 18's, patch the dated parts ----------
i0 = old.index('# The problem'); i1 = old.index('# The rules of this round')
common = old[i0:i1]

inv = open(f'{REPO}/rounds/round19/inventory.txt').read().split('\n')
nres = sum(1 for l in inv if l.startswith('L'))
secs = [f'{m.group(2)} (l.{m.group(1)})' for l in inv for m in [re.match(r'## L(\d+) (.*)$', l)] if m]
seclines = '; '.join(secs)
nlines = sum(1 for _ in open(f'{REPO}/frontier.tex'))
j0 = common.index('# The standing repository'); j1 = common.index('# THE STANDING RULE')
newrepo = '''# The standing repository

${REPO}/frontier.tex is a 244-page LaTeX development of ''' + str(nres) + ''' numbered
results (''' + str(nlines) + ''' lines) built over eighteen multi-agent rounds and one solo
round by the root agent. Every claim in it is proved and every negative
claim carries an explicit instance verified in exact rational arithmetic.
It contains NO polynomial-time algorithm for the general problem and
claims none. Read the parts you need with grep/sed; do NOT read the whole
file. THE INVENTORY ${SCRATCH}/round19/inventory.txt lists every numbered
result as "L<line> <env> <label> :: <title>", grouped by section: read it
in full FIRST (it is short) and use it for the novelty pre-check below.
Line numbers quoted in the route briefs refer to frontier.tex at commit
6e6c011 (HEAD). Sections and their first lines: ''' + seclines + '''.

'''
common = common[:j0] + newrepo + common[j1:]

addendum = '''

# ROUND-18 ADDENDUM (integrated 2026-09-04; the digest above predates it)

Labels added in round 18 -- read their statements before working near them:
prop:one-player-fold, rem:one-player-fold, prop:one-player-response
(rem:fold and rem:fold-width amended); def:escape-ext, thm:escape-level,
thm:escape-no-beta, thm:escape-mixed, cor:escape-m3 (rem:pinned-escape
extended with the exact drive line: 14 cells, 13 fences); prop:router-tree,
rem:merged-matrix (after rem:choice-lift); rem:handicap-base extended,
prop:handicap-singular, prop:hz; rem:tangent-cut (after
rem:convex-barrier-both, whose exclusion list gained the non-pairwise
affine cut); prop:hstar-one-eleven, rem:four-ceilings restated,
cor:stack-family (slope 11/6), rem:hk-survey extended; rem:no-amplification
corrected, two sentences after thm:top's closing paragraph (the free
H > M > L pair), rem:eps-ladder (after prop:bracket's remark);
lem:rational-row, rem:rational-row (after lem:dyadic-row); def:eval-data,
rem:eval-fibre, lem:eval-one-query, prop:eval-lift, prop:eval-decide-lower,
rem:eval-decide-gap (after rem:eval-queries); the round-17 paper audit's
three majors repaired (prop:own-stall / rem:own-successor / rem:transport:
the stall is of the two value-distinguishing vertices outside the seed;
rem:own-stall: the seven-vertex game is a silence at ONE vertex, not a
stall of the rule, and after retyping 1 and 3 the certificate decides 4
too; rem:blowup-realise: the orientation oracle is the CHEAPER one on the
m = 3 data); batch C's duplicate label renamed def:escape-ext (def:escape
is the escape exponent).
Headlines. (1) THE ONE-PLAYER FOLD OF(D) (prop:one-player-fold): one
player, acyclic, N = 9D + 6, the stopping-probability path has exactly
2^m - 1 breakpoints and is a Hamiltonian walk of the Max cube (the tent
map's itinerary), attaining the 2^m factor of the ceiling; the path is
NEVER an all-switches run (cor:law-u), under a fixed strategy the cascade
is AFFINE, all-switches halts within D + 1 rounds -- "what survives is a
fold fed back into its own drive"; the undamped one-player response map
is convex with exactly 2^D + 1 pieces of slopes j 4^{-D}
(prop:one-player-response), so rem:fold's "the device needs a Min vertex"
was wrong. (2) THE ESCAPE SHAPE (def:escape-ext: the outer pair's rest
actions read the block): its level theorem thm:escape-level computes the
outmap from three drives w_00, w_10, w_01 and one sign rho;
thm:escape-no-beta: any outer pair whose drive's switch row reads only the
block and whose rest row reads the partner positively realises no
translate carrying the drive's coordinate -- z = 24, 26 dead for every
block, all four doublings dead when the drive is alpha_2;
thm:escape-mixed: R_alpha - C_alpha must have a negative component, and if
it is >= 0 an up-closedness returns; cor:escape-m3: over the level-two
block z = 10 dead (inner reason), z = 8 dead unless R_alpha - C_alpha is
mixed in sign -- THE ONE SURVIVING CORNER of the escape route to B^3; a
floating-point search did not reach it; "a search is not a proof".
(3) h*_1^nd(5) = h*_LP(5) = h*_HK(5) = 11 (prop:hstar-one-eleven: a
260-vertex nondegenerate one-player game, denominator 2^13, found by a
guided walk through realised orientations), so the nondegenerate
one-player ceiling equals the Holt-Klee one at every m <= 5 against
h*(5) = 12; the stacking slope rises to 11/6; the 6113-class survey of the
4-cube: 5951 realised, 162 open, smallest candidate for a law beyond
Holt-Klee the class (8,9,10,11,13,12,14,15,7,6,4,5,3,2,1,0) of height 2;
the m = 6 walk towards height 13 / the height-14 blow-up cut short.
(4) THE ROUTER TREE (prop:router-tree): level one of the choice lift
closes only a Theta(1/N) fraction of the transport interval, with ONE
player and a CONSTANT number of average vertices; straddles on 10 and 14
vertices; rem:merged-matrix: D <= M D for the merged matrix, level one
exact when M is transient (no splitter); the round-17 exactness claim
stays unproved. (5) THE TANGENT CUT (rem:tangent-cut): on the
handicap-zero class R a seventh sound mechanism outside
thm:convex-barrier-both's language (an affine cut, not a pairwise
difference bound); it decides WD at round one and vertex 4 of the
seven-vertex game, nothing else the others do not; WD and CC lie in R
with B printed, BC(e >= 3) and CV outside; the boundary of R is attained
(prop:handicap-singular); HZ(n) is in R with lambda_min = 1/4, outside
every named bound as presented, yet polynomial by a reduced
1/2-contraction (prop:hz) -- a presentation artefact, not the wanted
member; no family designed against the cut exists. (6) COMPOSITION
(rem:no-amplification corrected): black-box composition amplifies a value
gap by at most (4/3)(s + 3) WITHOUT any admissibility hypothesis (only
the composition being stopping), the ruin chain with a player-free plug
attains Theta(s) (derivative 2i(K+1-i)/(K+1)), tight within 8/3; the free
sink-adjacent pair H > M > L decides no controlled vertex; rem:eps-ladder:
Ord_eps, App_eps, Gap_eps interreducible for dyadic eps, target-equivalent
for eps <= 2^{-N^gamma}, qualitative for eps near 1, THE MIDDLE (1/poly,
1/4) OPEN = whether prob:main reduces to its own promise version.
(7) THE EVALUATION DECISION PROBLEM (def:eval-data .. rem:eval-decide-gap):
deciding the bit from strategy evaluations needs |C| + 1 evaluations at
|C| in {2,3} (certificates of 16 and 400 nodes, every world assembled as
a game through the rejection gadget of lem:rational-row: arbitrary
rational first-passage rows on (l+2)ceil(log2 D) average vertices;
191 and 3863 vertices), against |C| + 2 sufficient (thm:eval-queries); the
two complexities agree up to one query; the general adversary is NOT
proved; nothing there bears on prob:main.
LESSON OF ROUND 18 (for every route and every auditor): the routes'
HEADLINES were wrong in four of seven cases while their mathematics
mostly held ("the hardest stalls all lie in R" false; the modulator
identification refuted; "the m = 5 column closes" wrong with ties allowed;
the diagonal-labelling theorem refuted outright); the novelty audits
ruled three of seven routes dead-end or blocked under the rubric. Your
headline is a claim: it must be a sentence you PROVED, in the words of
one of your results. And one route claimed a family of SSGs but only ever
verified harmonic systems, so both auditors and the root agent had to
assemble the games themselves: the games_built field is now REQUIRED.
'''
common = common + esc(addendum)

# ---------- rules: slice round 18's and patch ----------
r0 = old.index('# The rules of this round'); r1 = old.index('`\n\nconst ROUTE_SCHEMA')
rules = old[r0:r1]
rules = rules.replace('${SCRATCH}/round18/inventory.txt', '${SCRATCH}/round19/inventory.txt')
rules = replace_once(rules, 'COPY what you need into ${SCRATCH}/r18-<your-route>/', 'COPY what you need into ${SCRATCH}/r19-<your-route>/')
old_code = rules[rules.index('Round-17 route code and audits, read-only,'):rules.index('COPY what you need')]
new_code = '''Round-18 route code and audits, read-only, are under ${R18}/r18-<key>/
   and ${R18}/r18-audit-<key>-<lens>/ for key in drive-line,
   one-player-envelope, eval-decision, convex-class, weakest-oracle,
   beyond-holt-klee, rlt-two; their structured returns are
   ${REPO}/rounds/round18/results/*.json (route result = the file whose
   name starts with the route's title; the two audits follow), and the
   root agent's verification scripts and game files (dl_*, of_*, ed_*,
   hz_*, oc_verify, rl_verify, wo_*, H11_m5_GAME.json, cert_m*.json) are
   in ${REPO}/scripts/round18-verify/; the harness is archived in
   ${REPO}/scripts/harness/ (README inside). Round-17 route code is under
   ${R17}/r17-<key>/ for key in query-model, order-lattice, convex-lift,
   variational, parametric-path, oracle-barrier, realisation-space, with
   the root agent's scripts and game files (BC_*, CVX4, CVX6, NCX, DW,
   OL3, OS5, B2_pin137) in ${REPO}/scripts/round17-verify/; round-16 route
   code under ${R17}/<route>/ for route in b3-level, level-lemma,
   hk-doubling, width-amortise, few-denominator-stall, bsi-counter,
   one-player-howard, fresh-16, fresh-16-alg, min-budget.
   '''
rules = rules.replace(old_code, new_code)
assert 'r18-<key>' in rules and 'r17-<your-route>' not in rules
rules = replace_once(rules,
 '''   - A "witness" normal form that is not dyadic, or whose game was never
     built, is NOT a game. Build the game and verify from the game.''',
 '''   - A "witness" normal form that is not dyadic (or rational without the
     stopping hypothesis of lem:rational-row), or whose game was never
     built, is NOT a game. Build the game and verify from the game, and
     record it in the REQUIRED games_built field: round 18's eval-decision
     route verified harmonic systems only, and the auditors and the root
     agent had to assemble 832 worlds as games themselves.
   - Your HEADLINE is a claim of its own and is audited as one: four of
     seven headlines were struck in round 18 while the mathematics under
     them held. Write it in the words of a result you PROVED.
   - Never enumerate the leaves of a binary tree whose depth is the
     bit-length of a denominator (a 280-bit denominator hangs); count
     surviving nodes by boundary tests or build the pruned tree top-down.
   - One reasoning turn that tries to settle a whole question can exceed
     the output limit and kill the route (round 18): think in short
     steps and write every intermediate definition, lemma and computation
     into files in your directory as you go.''')
rules = replace_once(rules, '(round 16 left sixteen jobs running for five hours; round 17 left a monitor loop)',
                     '(round 16 left sixteen jobs running for five hours; round 17 left a monitor loop; round 18 left four stray files in the repository root)')
rules = replace_once(rules, '# The rules of this round (tightened on the user\'s instruction; read twice)',
                     '# The rules of this round (the round-17 rules, tightened on the user\'s instruction; read twice)')

# ---------- routes ----------
routes_src = open(f'{REPO}/rounds/round19/routes19.txt').read()
ROUTES = []
for block in routes_src.split('\n=====ROUTE ')[1:]:
    hdr, body = block.split('\n', 1)
    key, title = hdr.split('|', 1)
    ROUTES.append((key.strip(), title.strip(), body.strip('\n')))
assert len(ROUTES) == 8, len(ROUTES)
for k, t, b in ROUTES:
    assert '`' not in b, k
    for m in re.finditer(r'\$\{(\w+)\}', b):
        assert m.group(1) in ('REPO', 'SCRATCH', 'R18', 'R17'), (k, m.group(0))

# ---------- schemas: add games_built ----------
s0 = old.index('const ROUTE_SCHEMA'); s1 = old.index('const ROUTES = [')
schemas = old[s0:s1]
schemas = replace_once(schemas,
 "required: ['route', 'object', 'verdict', 'headline', 'results', 'restatements', 'gap', 'next_steps'],",
 "required: ['route', 'object', 'verdict', 'headline', 'results', 'restatements', 'gap', 'next_steps', 'games_built'],")
schemas = replace_once(schemas,
 "    headline: { type: 'string' },\n",
 "    headline: { type: 'string', description: 'one sentence you PROVED, in the words of one of your results; it is audited as a claim' },\n")
schemas = replace_once(schemas,
 "    next_steps: { type: 'string' },\n  },\n}",
 "    next_steps: { type: 'string' },\n    games_built: { type: 'string', description: 'REQUIRED: for every result resting on an instance or family, the game file(s) (kinds, successors) in your directory, the checks run FROM THE GAME (stopping by the trap test, values, outmap / run / rows) and the vertex counts; the literal none only for results with no instance' },\n  },\n}")
assert "games_built" in schemas

# ---------- audit lenses ----------
a0 = old.index('const AUDIT_LENSES'); a1 = old.index('const PAPER_AUDIT')
lenses = old[a0:a1]
lenses = lenses.replace('r18-audit-', 'r19-audit-').replace('round18/inventory.txt', 'round19/inventory.txt')
lenses = replace_once(lenses, 'under the tightened\nstandard of this round', 'under the tightened\nstandard of rounds 17 to 19')
lenses = replace_once(lenses,
 '''   monotone-LCP dictionary, thm:top and prop:no-halving as new; in
   round 17 five of seven routes reported restatements as results.''',
 '''   monotone-LCP dictionary, thm:top and prop:no-halving as new; in
   round 17 five of seven routes reported restatements as results, and
   in round 18 three of seven routes were dead-end or blocked under the
   rubric while FOUR HEADLINES were false over sound mathematics: audit
   the headline sentence as a claim of its own, and say whether the
   results as proved support it.''')
lenses = replace_once(lenses,
 '''   theorem beyond the four allowed, used without proof.''',
 '''   theorem beyond the four allowed, used without proof; a family whose
   members were never ASSEMBLED AS GAMES (check the games_built field:
   round 18's eval-decision route verified harmonic systems only) -- if
   the route built no game, build the smallest members yourself and
   check them from the game; a McCormick or RLT relaxation whose
   FEASIBILITY is read as feasibility of the original system.''')
assert 'games_built' in lenses

paper = '''const PAPER_AUDIT = {
  key: 'round18-diff',
  what: `the 1317 lines ADDED to frontier.tex in round 18 (batches P and A-G, git diff 812364d..6e6c011), saved as ${SCRATCH}/round19/round18_diff.txt`,
}

const paperAuditPrompt = (s) => `
You are an ADVERSARIAL AUDITOR of a mathematical manuscript. Your job is to
BREAK the part of ${REPO}/frontier.tex assigned to you, not to appreciate
it. The manuscript's own standard is: every claim proved from first
principles (four named imports), every negative claim witnessed by an
explicit instance verified in exact rational arithmetic, every rediscovery
attributed. Hold it to that standard.

${COMMON}

# Your assignment

${s.what}. Read the diff in full; for every hunk, read the surrounding
paper text (sed -n on ${REPO}/frontier.tex; grep -n 'label{NAME}' for any
result cited) so that you judge the statements IN CONTEXT. This material
was written by the root agent while integrating seven audited routes and
one paper audit; the routes' claims were audited, the INTEGRATED TEXT was
not. Round 18's paper audit of the round-17 text found three majors and
ten minors, all integration errors: a clause false on the paper's own
instance ("that reading decides no controlled vertex" on R, where clause
(i) fires at a Min vertex the seed pins), a stall claimed where only one
vertex is silent, a sentence contradicted by its own numbers (which oracle
is cheaper at m = 3), a proof citing itself, a definition misdescribing
its own example, a stale path, a fragment. Round 17's found seven majors
of the same kind (a hypothesis dropped in transcription, a claim false as
stated, a title contradicting its proof, a stale number). Those are what
you are looking for.

# Your task

1. PROOFS. For every theorem, lemma, proposition and corollary in the added
   text, reconstruct the proof step by step. Report every step asserted
   rather than proved, every hypothesis used but not stated (stopping?
   nondegeneracy? sink payoffs pinned? Min present? dyadic? reachable from
   v0? separated? one player? leaking rows?), every citation whose
   statement does not give what is used, every quantifier error. Sinks,
   ties, empty sets, the one-vertex game and the k = 0 / m <= 2 cases are
   where this manuscript's errors have lived. Prime targets:
   thm:escape-level (the uniqueness of the fixed points via |c|_1 < 1 and
   the slope bound y' <= 1; each of the eight outer-bit derivations;
   whether "the inner part is s_B(w_L(sigma))(sigma)" needs the block to
   read no outer coordinate but beta), thm:escape-no-beta (the tournament
   argument, the tie case w_00 = w_10 = w_01, the table lookup at the
   translated layer, the claim that alpha's rows play no part),
   thm:escape-mixed (a) and (b) (the concavity of rho in t, the three
   increasing arguments), cor:escape-m3 (the inner reason for z = 10, the
   R_alpha >= C_alpha exclusion for z = 8 via the three drives below
   6856791/18130160 and the comparable pairs), lem:rational-row (the
   rejection tree: independence of passes, the surviving-node count, the
   trap characterisation "closed full-mass action sets"), rem:rational-row
   (the relaxation of thm:readout-realise(b) and its trap hypothesis),
   def:eval-data / rem:eval-fibre (the fibre facts, the dimension clause as
   an inequality, the output criterion), lem:eval-one-query, prop:eval-lift
   (M' stopping as the hypothesis), prop:eval-decide-lower (the adversary
   argument: does a node of depth m with W and Y both reproducing the
   datum really force an error for EVERY deterministic algorithm, including
   one that stops early or repeats a query?), rem:eval-decide-gap,
   prop:one-player-fold (the recursions, e_d, the tent identity, the
   breakpoint set, the Hamiltonian-path claim, the Chebyshev seed and its
   size bound O(k^2), the two-sided bound on B*(n,m)),
   prop:one-player-response (the closed form, convexity, exactly 2^D + 1
   pieces of slopes j 4^{-D}), rem:one-player-fold (the four readings: the
   "never a run" argument via cor:law-u, the affine cascade, the convex
   envelope via generating functions and one Min vertex breaking it),
   prop:router-tree (the two decompositions, the straddle, mu in [0,1]),
   rem:merged-matrix (D <= M D: the decomposition step, transience),
   rem:handicap-base (the Hessian, the congruence, the norm criterion,
   the "boundary attained" and HZ clauses), prop:handicap-singular (B and
   its kernel), prop:hz (N = 6n^2 + 2, the circulant eigenvalues >= 1/4,
   the escape-certificate bound lambda > 1 - 2^{1-n}, the modulator and
   treewidth bounds, the reduced 1/2-contraction and the exact recovery),
   rem:tangent-cut (Taylor's formula on the affine hull, soundness,
   "outside the language of thm:convex-barrier-both", the WD computation
   and the seven-vertex decision), prop:hstar-one-eleven (the system is
   substochastic with leaks and p_v^{v,a} = 0, the outmap, Holt-Klee,
   height 11, the walk), rem:four-ceilings and cor:stack-family (11/6),
   rem:hk-survey (the counts 6113 / 5951 / 162 and the height split),
   rem:no-amplification (the admissibility-free bound, the ruin chain's
   derivative 2i(K+1-i)/(K+1), tightness 8/3), the two sentences after
   thm:top (the free pair), rem:eps-ladder (the four reductions and their
   constants, the two ends), and every abstract / summary sentence added
   in round 18 against the body.
2. NUMBERS. For every explicit instance, table, count or vertex count in the
   added text that can be recomputed in under an hour, RECOMPUTE IT in exact
   rational arithmetic with your own code in
   ${SCRATCH}/r19-paper-audit-${s.key}/ (harness at ${SCRATCH}/root16/,
   ${SCRATCH}/solo/, ${REPO}/scripts/harness/, ${REPO}/scripts/round18-verify/
   -- you may READ the root agent's scripts and game files to see what was
   checked, but recompute from the manuscript's statement). Obvious
   targets: the 13 fences of the level-two block's drive line and the 14
   cells; Theta_w = 2036/3313, Theta_u = 2048/3313 and the outmap B^2 from
   the three drives; the edge distances 42, 52, 32, 44; OF(D)'s 2^m - 1
   breakpoints and the single tied vertex per breakpoint (D <= 6), the
   all-switches halting within D + 1 rounds; the 2^D + 1 pieces and slopes
   of OP_D (D <= 5); the one-Min-vertex counterexample values 8/125, 1/8,
   9/50; the 260-vertex system's stopping, outmap, Holt-Klee status and
   run of length 11 from the game (build it by lem:dyadic-row); the router
   tree's values 4/7, 8/11, 2/3 and its level-one points in R_1 by the
   disjunctive LPs; B for WD(4,2,6) and CC(L,m) at one size; the singular
   B of prop:handicap-singular and its kernel; HZ(4)'s N = 98, a = 80,
   lambda_min = 1/4, w*(d_1) = 2^{-16}; the rejection gadget sizes 3, 5, 7,
   11 for the four rows quoted in lem:rational-row; the certificate
   cert_m2_d2.json (16 nodes, all 32 worlds as games: stopping,
   nondegenerate, the bit); the ruin chain's derivative for K <= 7; the
   WD tangent cut -gamma xi_1 + (gamma + mu) xi_2 <= mu^2/2 and the round-one
   decision; the seven-vertex game's lexicographic optimum
   (2/3,1/3,1/3,2/3,1/3) and Sep(4,2) < 0 at round one.
3. CONSISTENCY. Every \\\\Cref in the added text must point at a result that
   says what the text claims (in particular def:escape-ext vs def:escape,
   which batch C had confused for five commits). Every qualifier
   ("measured, not proved", "the route", "the auditor", "recomputed here",
   "unsettled", "open") must match the statement it qualifies AND the
   abstract / summary. Every "verified on K instances" must say what was
   varied. Check that no round-18 sentence contradicts an earlier one
   still in the text (rem:fold vs prop:one-player-response; rem:four-ceilings'
   rows vs prop:hstar-one-eleven and cor:stack-family; rem:hk-survey's
   "none of height 6" vs its earlier "every one of the 56").
4. PRIOR ART presented as new is a defect; name the source if you know it
   (Kelley's cutting plane, Balas' disjunctive closure, McCormick,
   Sherali-Adams, gambler's ruin, the tent map, rejection sampling are the
   obvious ones -- the text flags most; check each).
5. OVERSTATEMENT: barriers covering no real rule, classes that are
   restatements, families measured at two sizes, "answers the question"
   where only a special case is answered, a headline the body does not
   support.
6. IF TIME REMAINS, the backlog no audit has checked: prop:b3-outer's
   194-vertex game (${REPO}/scripts/round16-verify/TB_GAME_D10.json);
   ST(1)/ST(2) of cor:stack-family; rem:bias-families' BP(D) counts;
   prop:bias-witnesses' PATH games and (b)-(d); rem:discount-fold's 9D + 3
   variant; thm:eval-queries' 136/194/344-vertex reproductions;
   rem:choice-lift's level-two exactness (measured); the escape exponent
   d(M_n) = n + 1 (prop:modulator-family); prop:hk-doubling-measured (d),
   (e); prop:oneplayer-census-small's total; prop:cv-measured's rows;
   prop:q16's counts; lem:max-tree's 11-vertex instance; prop:zero-ties'
   26 tied incidences.

Report findings with severity fatal / major / minor / note, each with the
LINE NUMBER in frontier.tex, the label, the defect in one sentence and the
evidence. "sound" is TRUE only if nothing fatal or major survives. List what
you checked and what you did not. Put target = 'frontier.tex round-18 diff'.
Kill your background jobs before returning. Write nothing into ${REPO}.
`

'''

head = '''export const meta = {
  name: 'ssg-round19',
  description: 'Round 19 on the SSG value problem under the round-19 brief (rounds/round19/BRIEF.md): eight routes on Opus 5 at effort high (five from round 18\\'s list, two fresh formulations, one blind) against the post-round-18 frontier (244 pp, ''' + str(nres) + ''' results), each audited for correctness and novelty on Opus 5, plus ONE paper audit of the round-18 diff on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
    { title: 'Paper audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = \'''' + SC + '''\'
const R18 = \'''' + R18 + '''\'
const R17 = \'''' + R17 + '''\'

const COMMON = `
'''
routes_js = 'const ROUTES = [\n' + ''.join("  { key: '%s', title: %s, brief: `%s` },\n" % (k, repr(t), esc(b)) for k, t, b in ROUTES) + ']\n\n'

tail = '''log(`Round 19: ${ROUTES.length} routes on Opus 5 at effort high: ${ROUTES.map(r => r.key).join(', ')}; correctness + novelty audits on Opus 5; one paper audit (round-18 diff) on Opus 5.`)

const PACING = `PACING: a route of round 18 died because one reasoning turn exceeded the ` +
  `output-token limit; think in short steps, write every intermediate definition, ` +
  `lemma and computation into files in your directory as you go, and never try to ` +
  `settle a whole question in one turn.`

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\\n\\n# YOUR ROUTE: ${r.title}\\n${r.brief}\\n\\n` +
    `Work in ${SCRATCH}/r19-${r.key}/ (create it). Copy the harness from ` +
    `${SCRATCH}/root16/ (and what you need from ${SCRATCH}/solo/, ${SCRATCH}/myver/ and ${REPO}/scripts/harness/) into your own ` +
    `directory before using it. Read ${SCRATCH}/round19/inventory.txt in full ` +
    `before anything else. You have a long budget: think hard, write code, ` +
    `verify, iterate. Your final output is the structured object and it is the ` +
    `ONLY thing that reaches the root agent -- make it complete and ` +
    `self-contained, put every explicit instance into files in your directory ` +
    `AND name them in the result, fill games_built, put the path of your code directory in ` +
    `code_dir, and kill your background jobs before returning. ${PACING}`,
    { label: `route:${r.key}`, phase: 'Routes', schema: ROUTE_SCHEMA, model: 'opus', effort: 'high' }
  ),
  (res, r) => {
    if (!res) return null
    const text = JSON.stringify(res, null, 1).slice(0, 60000)
    return parallel(AUDIT_LENSES.map((L) => () =>
      agent(L.prompt(r, text) + `\\n${PACING}`, { label: `audit:${r.key}:${L.key}`, phase: 'Audit', schema: AUDIT_SCHEMA, model: 'opus', effort: 'high' })
    )).then((audits) => ({ route: r.key, result: res, audits: audits.filter(Boolean) }))
  }
)

const paperWork = agent(paperAuditPrompt(PAPER_AUDIT) + `\\n${PACING}`, { label: `paper:${PAPER_AUDIT.key}`, phase: 'Paper audit', schema: AUDIT_SCHEMA, model: 'opus', effort: 'high' })
  .then((a) => (a ? { section: PAPER_AUDIT.key, audit: a } : null))

const [results, paper] = await Promise.all([routeWork, paperWork])
const good = results.filter(Boolean)
log(`Round 19 complete: ${good.length}/${ROUTES.length} routes returned; paper audit ${paper ? 'returned' : 'missing'}.`)
return { round: 19, routes: good, paper }
'''
js = head + common + rules + '`\n\n' + schemas + routes_js + lenses + paper + tail
out = f'{REPO}/rounds/round19/round19.js'
open(out, 'w').write(js)
open(f'{SC}/round19/round19.js', 'w').write(js)
print('round19.js written:', js.count('\n'), 'lines,', len(js), 'bytes; routes', [k for k, _, _ in ROUTES])
for must in ['R18', 'R17', 'round19/inventory.txt', 'r19-', 'ROUND-18 ADDENDUM', 'INCOMPARABLE', "model: 'opus'", "effort: 'high'", 'games_built', 'PACING']:
    print('%-28s %d' % (must, js.count(must)))
assert 'r18-audit-' not in lenses and 'round18/inventory' not in js and 'r18-<your-route>' not in js
assert js.count("model: 'opus'") == 3 and js.count("effort: 'high'") == 3
