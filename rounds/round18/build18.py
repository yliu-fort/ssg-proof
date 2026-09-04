import re
SC='/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad'
R17='/tmp/claude-1000/-data-ssg-proof/d1fe2115-9b72-4784-bb94-87421ac1106c/scratchpad'
old=open('/data/ssg-proof/rounds/round17/round17.js').read()

def esc(t): return t.replace('\\','\\\\').replace('`','\\`')

# ---------- COMMON: slice round 17's, patch the dated parts ----------
i0=old.index('# The problem'); i1=old.index('# The rules of this round')
common=old[i0:i1]

inv=open(f'{SC}/round18/inventory.txt').read().split('\n')
secs=[f'{m.group(2)} (l.{m.group(1)})' for l in inv for m in [re.match(r'## L(\d+) (.*)$',l)] if m]
seclines='; '.join(secs)
j0=common.index('# The standing repository'); j1=common.index('# THE STANDING RULE')
newrepo='''# The standing repository

${REPO}/frontier.tex is a 229-page LaTeX development of 503 numbered
results (17759 lines) built over seventeen multi-agent rounds and one solo
round by the root agent. Every claim in it is proved and every negative
claim carries an explicit instance verified in exact rational arithmetic.
It contains NO polynomial-time algorithm for the general problem and
claims none. Read the parts you need with grep/sed; do NOT read the whole
file. THE INVENTORY ${SCRATCH}/round18/inventory.txt lists every numbered
result as "L<line> <env> <label> :: <title>", grouped by section: read it
in full FIRST (it is short) and use it for the novelty pre-check below.
Sections and their first lines: ''' + seclines + '''.

'''
common=common[:j0]+newrepo+common[j1:]

k0=common.index('# THE STANDING RULE'); k1=common.index('# What is PROVED in frontier.tex')
newrule='''# THE STANDING RULE -- read this before designing any experiment

Round 10 found a defect that ran through several of the paper's negative
results; it is rem:own-successor, and round 17 corrected the rule itself.
Every route must respect the corrected form.

A decision rule (def:decision-rule) must name a controlled vertex and say WHICH
SUCCESSOR IS LARGER. At v in Vmax there are THREE sound ways to fire:
  (i)  deriving w*(v) <= w*(v^(i)) forces EQUALITY, since w*(v) >= w*(v^(i)) is
       automatic, so it proves v^(i) OPTIMAL (the own-successor reading, first
       clause; for the transport LP this clause can never fire);
  (ii) deriving w*(v^(i)) < w*(v) proves v^(i) NOT optimal, so the other is
       (the own-successor reading, second clause; Sep(v, v^(i)) < 0 for the LP);
  (iii) the NON-STRICT PAIR TEST: deriving w*(v^(0)) <= w*(v^(1)) (Sep(v^(0),
       v^(1)) <= 0 for the LP) names v^(1) as an optimal successor.
All three dualise at Vmin. THE OWN-SUCCESSOR READINGS AND THE PAIR TEST ARE
INCOMPARABLE (round 17, convex-lift audit, verified by the root agent in
${REPO}/scripts/round17-verify/pairtest.py): on the ten-vertex game R of
prop:own-stall every own-successor separator is 0 while the non-strict pair
test decides all three value-distinguishing vertices (through x >= 0 and the
Z_0 pin); on S and on S_r of thm:transport-barrier the pair test is positive
while Sep(v, b) < 0 decides. The earlier statement that the pair test is
"strictly weaker" was FALSE and has been struck from the paper. A genuine
stall of both readings exists: the seven-vertex game Vavg = {0,2}, Vmin = {1},
Vmax = {3,4}, 0 -> (2,t1), 1 -> (3,t1), 2 -> (t0,0), 3 -> (0,t0), 4 -> (1,2),
at vertex 4 (rem:own-stall). If you claim any mechanism stalls, you MUST test
(i), (ii) AND (iii) at every controlled vertex, and you MUST seed the
programme with Z_0 and Z_1 (the free attractor sweeps, linear time). Five
stalls found in round 10 without that seed were all artefacts; the seed
cracked every one. A stall at a vertex whose two successors have EQUAL value
is VACUOUS (prop:fv-stall): a sound rule is licensed to abstain there. Only a
stall at a VALUE-DISTINGUISHING vertex (successors of different value)
counts, and only when all three readings are silent.

'''
common=common[:k0]+newrule+common[k1:]

addendum='''

# ROUND-17 ADDENDUM (integrated 2026-09-04; the digest above predates it)

Labels added in round 17 -- read their statements before working near them:
def:discount-path, rem:discount-path, thm:eval-queries, prop:hdp-eval,
rem:eval-queries, def:pinned, prop:pinned-level, lem:pinned-upclosed,
thm:pinned-no-translate, cor:pinned-no-doubling, rem:pinned-escape,
prop:handicap-zero-ceiling, rem:handicap-base, prop:bias-one-improving
(restated as a multi-switch rule), prop:one-vertex-path, cor:two-homotopies,
rem:run-informs, rem:cyclic-antipodal, rem:order-unique, rem:slack-grade,
rem:choice-lift, prop:discount-fold, rem:discount-fold, lem:ratio-sign,
thm:convex-barrier-both, rem:convex-barrier-both, sec:bc (def:bc,
prop:bc-values, prop:bc-lmc, lem:lift-reduction, thm:bc-cert, thm:bc-lower,
rem:bc-measured); rem:own-successor, prop:own-stall, rem:own-stall and the
summary CORRECTED (the pair-test rule above); rem:four-ceilings restated for
the nondegenerate ceiling; rem:signdef's damping-closure claim STRUCK
(a 9-vertex counterexample); cor:stack-family's Fekete limit marked not
established.
Headlines. (1) THE STOPPING-PROBABILITY PATH (def:discount-path: every step
survives with probability rho, i.e. Condon's damping read as a homotopy in
rho) is exponentially long: BP(D) on 10D+2 vertices (D Max, D Min) has
exactly 2^D - 1 breakpoints at k/2^D, the optimal pair following the TENT
MAP's itinerary (prop:discount-fold); thm:fold's P_D with a two-vertex seed
gives 2^{(N-3)/6} - 1 on 6D+3 vertices; one Max vertex realises ANY dyadic
breakpoint set (prop:one-vertex-path) and the path returns to pairs it left,
so it is NOT the bias homotopy of sec:bias (cor:two-homotopies). Whether a
ONE-PLAYER family has 2^{Omega(n)} breakpoints is open (rem:discount-fold).
(2) BC(e,s) (sec:bc): a one-player family, N = 12e + 2s + 11, with ONE
value-distinguishing vertex v_0 (gap 2^{-s}), on which the simulation
preorder decides nothing (prop:bc-lmc), and the slack calculus, its min-plus
closure, the transport step, the hybrid and the ratio calculus -- in any
interleaving, seeding, rounding, and the order transfer of
thm:convex-barrier-both -- are silent for a PROVED K + 1 >= floor((2^{e+1} -
3)(s - 4) ln 2 / 3) operator applications, i.e. 2^{Omega(N)}, while ONE
policy evaluation decides it (thm:bc-cert, thm:bc-lower; the multiplicative
register covered by the certificate method for the first time,
thm:convex-barrier-both, lem:ratio-sign). The M1-seeding clause is MEASURED
at ten sizes, not proved. BC defeats M1, M2, M2T, M4, M5, M6 and NOT M3 (one
all-switches round decides it): the open item of rem:wedge is still the
superpolynomial all-switches family (thm:seed-dichotomy).
(3) THE PINNED SHAPE (def:pinned): the shape shared by prop:b3-outer and the
outer pair of prop:b2-realised, with its level theorem prop:pinned-level
(C1)-(C5); lem:pinned-upclosed; thm:pinned-no-translate; and
cor:pinned-no-doubling: pinned on top of pinned cannot present a doubling
translate (z in {8,10,24,26} of B^2), so B^3 (height 22) is OUT OF REACH of
that shape, whose best 7-cube height is 16 (12 realised). rem:pinned-escape
names the escape: an outer vertex whose REST action reads the block, and the
question every route to B^3 runs through -- a driven block that is not
pinned presenting B^2 at one drive and B^2(. xor z) at another. Exact
fences of the level-two block's drive line are printed there; B^2 is also
realised on 137 vertices.
(4) EVALUATION QUERIES (thm:eval-queries): an optimal strategy is found from
at most d(G) + 2 <= |C| + 2 adaptively chosen strategy evaluations (a rank
argument: each non-halting answer adds a dimension), at the price of solving
the hypothesis between queries -- a statement about INFORMATION, not rounds;
so every exponential lower bound in the paper bounds the ROUNDS of a rule,
never information (rem:eval-queries, rem:run-informs: any run informs at
most |C| + 1 rounds). prop:hdp-eval: m evaluations are needed to NAME the
optimum on the degenerate, pairwise-isomorphic family HDP_m; the DECISION
version on a nondegenerate one-skeleton family is open. Outmap-query
complexity of the 3-cube class is exactly 4 (3 given the skeleton).
(5) The convex side: the Sherali-Adams lift over the CHOICE variables fails
at level one on W_14 with a five-point certificate (max_{R_1} x(v_1) >= 3/5
against w* = 1/2), level two measured exact everywhere tried (rem:choice-lift);
HANDICAP ZERO (B := sym(R_0^T R_1) >= 0 in the normal form over C, base-
independent by principal-pivot invariance, rem:handicap-base) attains the
one-player ceiling at m <= 4 (prop:handicap-zero-ceiling: a 39-vertex
realisation of the first blow-up level has handicap zero, the 58-vertex one
has not; CVX6 on 127 vertices has run 6 with B > 0), so handicap is not a
property of the orientation and does not bound the run; the class R = {B >= 0}
is a class on which the problem is CONVEX (q(x) = sum_v (x(v) - x(v^0))
(x(v) - x(v^1)) convex on Q(G) with unique zero w*) and NOT a proved
polynomial class (no first-principles convex-QP method; no member outside
the eight classes exhibited).
(6) Orders: the consistent order is unique (UP cap coUP with O(a log a) bits,
rem:order-unique); decode-and-re-sort from an arbitrary preorder can 3-cycle
on the paper's own cyclic instance (rem:cyclic-antipodal; it is the profile
cube's antipodal walk); no cycle with |C| <= 2 on separated games.
'''
common=common+esc(addendum)

# ---------- rules: slice round 17's and patch ----------
r0=old.index('# The rules of this round'); r1=old.index('`\n\nconst ROUTE_SCHEMA')
rules=old[r0:r1]
rules=rules.replace('${SCRATCH}/round17/inventory.txt','${SCRATCH}/round18/inventory.txt')
rules=rules.replace('COPY what you need into ${SCRATCH}/r17-<your-route>/','COPY what you need into ${SCRATCH}/r18-<your-route>/')
old_r16=rules[rules.index('Round-16 route code,'):rules.index('COPY what you need')]
new_r16='''Round-17 route code and audits, read-only, are under ${R17}/r17-<key>/
   and ${R17}/r17-audit-<key>-<lens>/ for key in query-model,
   order-lattice, convex-lift, variational, parametric-path,
   oracle-barrier, realisation-space; their structured returns are
   ${REPO}/rounds/round17/results/*.json (route result = the file whose
   name starts with the route's title; the two audits follow), and the
   root agent's verification scripts and game files (BC_*, CVX4, CVX6,
   NCX, DW, OL3, OS5, B2_pin137) are in ${REPO}/scripts/round17-verify/
   (README inside). Round-16 route code is under ${R17}/<route>/ for
   route in b3-level, level-lemma, hk-doubling, width-amortise,
   few-denominator-stall, bsi-counter, one-player-howard, fresh-16,
   fresh-16-alg, min-budget.
   '''
rules=rules.replace(old_r16,new_r16)
rules=rules.replace('test BOTH clauses of\n     rem:own-successor (round 16\'s few-denominator route tested clause (i)\n     only and reported a stall of M6 that does not exist).',
 'test ALL THREE readings of\n     the standing rule -- own-successor (i), (ii) and the non-strict pair\n     test -- Z-seeded (round 16\'s few-denominator route tested clause (i)\n     only and reported a stall of M6 that does not exist; round 17\'s\n     routes ran their OWN drivers, which silently weakened tests; re-run\n     the paper\'s definitions).')
assert 'ALL THREE readings' in rules
rules=rules.replace('(round 16 left sixteen jobs running for five hours)','(round 16 left sixteen jobs running for five hours; round 17 left a monitor loop)')

# ---------- routes ----------
routes_src=open(f'{SC}/round18/routes18.txt').read()
ROUTES=[]
for block in routes_src.split('\n=====ROUTE ')[1:]:
    hdr,body=block.split('\n',1)
    key,title=hdr.split('|',1)
    ROUTES.append((key.strip(),title.strip(),body.strip('\n')))
assert len(ROUTES)==7, len(ROUTES)

s0=old.index('const ROUTE_SCHEMA'); s1=old.index('const ROUTES = [')
schemas=old[s0:s1]

a0=old.index('const AUDIT_LENSES'); a1=old.index('const PAPER_AUDIT')
lenses=old[a0:a1]
lenses=lenses.replace('r17-audit-','r18-audit-').replace('round17/inventory.txt','round18/inventory.txt')
lenses=lenses.replace('the PAIR test\n   instead of rem:own-successor; clause (i) tested without clause (ii);',
 'a stall claimed\n   without testing all three readings of the standing rule (own-successor\n   (i), (ii) and the non-strict pair test), Z-seeded, with the PAPER\'S\n   definitions rather than the route\'s own driver;')
assert 'all three readings of the standing rule' in lenses
lenses=lenses.replace('under the tightened standard of this round','under the tightened standard of rounds 17 and 18')
lenses=lenses.replace('thm:seed-dichotomy, lem:rise-bound, thm:bsi-tracks, lem:hstar-super,\n   lem:readout and thm:matching-barrier as new.',
 'thm:seed-dichotomy, lem:rise-bound, thm:bsi-tracks, lem:hstar-super,\n   lem:readout, thm:matching-barrier, thm:profile-uso, prop:lcp\'s\n   monotone-LCP dictionary, thm:top and prop:no-halving as new; in\n   round 17 five of seven routes reported restatements as results.')
assert 'five of seven routes' in lenses

paper='''const PAPER_AUDIT = {
  key: 'round17-diff',
  what: `the 1713 lines ADDED to frontier.tex in round 17 (batches A-I, git diff 7fa45a3..812364d), saved as ${SCRATCH}/round18/round17_diff.txt`,
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
not. Round 17's paper audit of the round-16 text found seven majors and
eleven minors, all integration errors: a hypothesis dropped in
transcription (nondegeneracy, the stacked block), a claim false as stated
(closure under damping), a title contradicting its proof (single- versus
multi-switch), a stale number after a later result superseded it, a
summary sentence contradicted by a proposition, a count that is not a
power of two. Those are what you are looking for.

# Your task

1. PROOFS. For every theorem, lemma, proposition and corollary in the added
   text, reconstruct the proof step by step. Report every step asserted
   rather than proved, every hypothesis used but not stated (stopping?
   nondegeneracy? sink payoffs pinned? Min present? dyadic? reachable from
   v0? separated? profile-nondegenerate?), every citation whose statement
   does not give what is used, every quantifier error. Sinks, ties, empty
   sets, the one-vertex game and the k = 0 / m <= 2 cases are where this
   manuscript's errors have lived. Prime targets: thm:eval-queries (the
   rank argument, the barycentre/stopping clause, the pair-oracle clause
   with d_pi), prop:hdp-eval, thm:bc-cert and thm:bc-lower (the chain P_k,
   the six displayed quantities, the closed form of K + 1, the M1 clause
   demoted to measured), lem:lift-reduction, thm:convex-barrier-both and
   lem:ratio-sign (the multiplicative register: the +infinity convention,
   (D1)-(D6), the order transfer), prop:pinned-level (C1)-(C5),
   lem:pinned-upclosed, thm:pinned-no-translate, cor:pinned-no-doubling
   (the pin-pair step, the drive-free pin hypothesis, the height formula
   10 + 2 + h), prop:discount-fold (the tent identity, the tied sets, the
   Min vertex count), rem:discount-fold (the P_D transplant with the
   two-vertex seed, 6D + 3), prop:one-vertex-path (K, K_0, the size
   bound), cor:two-homotopies (the interval argument for shadow-vertex
   paths), rem:choice-lift (the five-point certificate), rem:handicap-base
   (the Hessian identity, the congruence, the norm criterion),
   prop:handicap-zero-ceiling (the minors), rem:order-unique (i)-(iii),
   rem:cyclic-antipodal, rem:run-informs, rem:slack-grade, and the
   CORRECTED rem:own-successor / prop:own-stall / rem:own-stall.
2. NUMBERS. For every explicit instance, table, count or vertex count in the
   added text that can be recomputed in under an hour, RECOMPUTE IT in exact
   rational arithmetic with your own code in
   ${SCRATCH}/r18-paper-audit-${s.key}/ (harness at ${SCRATCH}/root16/,
   ${SCRATCH}/solo/, ${REPO}/scripts/round17-verify/ -- you may READ the
   root agent's scripts and game files to see what was checked, but
   recompute from the manuscript's statement). BC(e,s)'s K + 1 table
   (2, 5, 11, 22, 46; 4, 9; 5; 16, 34) and w*, BP(D)'s 2^D - 1 breakpoints,
   OS({1/4,1/2})'s path 0,1,0, the 137-vertex B^2 game, rs_upclosed's
   violation counts 12,3,5,9,1,7,9,6,6, the W_14 five points, the 39- and
   58-vertex minors, CVX6's normal form and run, the 7-vertex both-readings
   stall, R's pair-test decisions, L_6's 7 informative rounds, the 3-cube
   outmap-query number 4, the level-two block's exact fences are the
   obvious targets.
3. CONSISTENCY. Every \\\\Cref in the added text must point at a result that
   says what the text claims. Every qualifier ("measured, not proved",
   "one direction only", "at fixed s", "the route's auditor") must match
   the statement it qualifies AND the abstract/summary (both rewritten in
   round 17: check every round-17 claim in them against the body). Every
   "verified on K instances" must say what was varied.
4. PRIOR ART presented as new is a defect; name the source if you know it.
5. OVERSTATEMENT: barriers covering no real rule, classes that are
   restatements, families measured at two sizes, "answers the question"
   where only a special case is answered.
6. IF TIME REMAINS, the backlog no audit has checked: the escape exponent
   d(M_n) = n + 1 (prop:modulator-family); prop:hk-doubling-measured (d),
   (e); prop:oneplayer-census-small's total; the measured rows of
   prop:cv-measured; prop:q16's revised counts; prop:bias-witnesses
   (b)-(d); lem:max-tree's 11-vertex instance; prop:zero-ties' 26 tied
   incidences.

Report findings with severity fatal / major / minor / note, each with the
LINE NUMBER in frontier.tex, the label, the defect in one sentence and the
evidence. "sound" is TRUE only if nothing fatal or major survives. List what
you checked and what you did not. Put target = 'frontier.tex round-17 diff'.
Kill your background jobs before returning. Write nothing into ${REPO}.
`

'''

head='''export const meta = {
  name: 'ssg-round18',
  description: 'Round 18 on the SSG value problem under the round-17 brief (rounds/round18/BRIEF.md): seven object-changing routes on Opus 5 against the post-round-17 frontier (229 pp, 503 results), each audited for correctness and novelty on Opus 5, plus ONE paper audit of the round-17 diff on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
    { title: 'Paper audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad'
const R17 = '/tmp/claude-1000/-data-ssg-proof/d1fe2115-9b72-4784-bb94-87421ac1106c/scratchpad'

const COMMON = `
'''
routes_js='const ROUTES = [\n'+''.join("  { key: '%s', title: %s, brief: `%s` },\n" % (k, repr(t), esc(b)) for k,t,b in ROUTES)+']\n\n'

tail='''log(`Round 18: ${ROUTES.length} object-changing routes on Opus 5: ${ROUTES.map(r => r.key).join(', ')}; correctness + novelty audits on Opus 5; one paper audit (round-17 diff) on Opus 5.`)

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\\n\\n# YOUR ROUTE: ${r.title}\\n${r.brief}\\n\\n` +
    `Work in ${SCRATCH}/r18-${r.key}/ (create it). Copy the harness from ` +
    `${SCRATCH}/root16/ (and what you need from ${SCRATCH}/solo/ and ${SCRATCH}/myver/) into your own ` +
    `directory before using it. Read ${SCRATCH}/round18/inventory.txt in full ` +
    `before anything else. You have a long budget: think hard, write code, ` +
    `verify, iterate. Your final output is the structured object and it is the ` +
    `ONLY thing that reaches the root agent -- make it complete and ` +
    `self-contained, put every explicit instance into files in your directory ` +
    `AND name them in the result, put the path of your code directory in ` +
    `code_dir, and kill your background jobs before returning.`,
    { label: `route:${r.key}`, phase: 'Routes', schema: ROUTE_SCHEMA, model: 'opus' }
  ),
  (res, r) => {
    if (!res) return null
    const text = JSON.stringify(res, null, 1).slice(0, 60000)
    return parallel(AUDIT_LENSES.map((L) => () =>
      agent(L.prompt(r, text), { label: `audit:${r.key}:${L.key}`, phase: 'Audit', schema: AUDIT_SCHEMA, model: 'opus' })
    )).then((audits) => ({ route: r.key, result: res, audits: audits.filter(Boolean) }))
  }
)

const paperWork = agent(paperAuditPrompt(PAPER_AUDIT), { label: `paper:${PAPER_AUDIT.key}`, phase: 'Paper audit', schema: AUDIT_SCHEMA, model: 'opus' })
  .then((a) => (a ? { section: PAPER_AUDIT.key, audit: a } : null))

const [results, paper] = await Promise.all([routeWork, paperWork])
const good = results.filter(Boolean)
log(`Round 18 complete: ${good.length}/${ROUTES.length} routes returned; paper audit ${paper ? 'returned' : 'missing'}.`)
return { round: 18, routes: good, paper }
'''
js = head + common + rules + '`\n\n' + schemas + routes_js + lenses + paper + tail
open(f'{SC}/round18/round18.js','w').write(js)
print('round18.js written:', js.count('\n'), 'lines,', len(js), 'bytes; routes', [k for k,_,_ in ROUTES])
for must in ['R17','round18/inventory.txt','r18-','ROUND-17 ADDENDUM','INCOMPARABLE','model: \'opus\'']:
    print(must, js.count(must))
assert 'r17-audit-' not in lenses and 'round17/inventory' not in js
