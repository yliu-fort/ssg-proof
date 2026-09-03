export const meta = {
  name: 'ssg-round15',
  description: 'Round 15 (re-run) on the SSG value problem: 10 routes on Opus 5 against the post-solo-round frontier, each adversarially audited twice on Opus 5, plus six adversarial audits of frontier.tex itself on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
    { title: 'Paper audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/6e64b33d-520c-4c82-aa1b-ffb69ecfcb61/scratchpad'

const COMMON = `
# The problem

A SIMPLE STOCHASTIC GAME (SSG) is a directed graph on
V = Vmax u Vmin u Vavg u {t0,t1}; every non-sink has out-degree exactly two.
A token starts at v0; at a Vmax (resp. Vmin) vertex player Max (resp. Min)
picks the outgoing edge, at a Vavg vertex a fair coin does. Max wins iff the
token reaches t1. val(v) is the value under optimal play. THE TARGET: decide
val(v0) >= 1/2 in deterministic polynomial time. A COMPLETE AFFIRMATIVE PROOF
IS WHAT IS WANTED; barriers and refutations are useful only insofar as they
redirect the search.

Notation: N = |V|, a = |Vavg|, C = Vmax u Vmin, m or n = |Vmax|. w* = val, the
value vector. T = the Shapley operator. T_sigma = T with Max frozen to sigma;
val_sigma = the value when Max plays sigma and Min plays optimally; val^tau =
the value when Min plays tau and Max plays optimally. STOPPING means that under
every positional pair the token reaches a sink with probability 1.
S_sigma = {v in Vmax : val_sigma(sigma-bar(v)) > val_sigma(sigma(v))}, the
strictly switchable set. ALL-SWITCHES: sigma -> sigma[S_sigma].

# The standing repository

${REPO}/frontier.tex is a 137-page, 330-result LaTeX development built over
fourteen prior multi-agent rounds and one solo round by the root agent (10856
lines). Every claim in it is proved and every
negative claim carries an explicit instance verified in exact rational
arithmetic. It contains NO polynomial-time algorithm and claims none. Read the
parts you need with grep/sed; do NOT read all 570 KB.
\`grep -n 'label{' ${REPO}/frontier.tex\` lists every result.

# THE STANDING RULE -- read this before designing any experiment

Round 10 found a defect that ran through several of the paper's negative
results. It is now rem:own-successor, and every route must respect it.

A decision rule (def:decision-rule) must name a controlled vertex and say WHICH
SUCCESSOR IS LARGER. It need NOT order the two successors against each other.
At v in Vmax there are two ways to fire:
  (i)  deriving w*(v) <= w*(v^(i)) forces EQUALITY, since w*(v) >= w*(v^(i)) is
       automatic, so it proves v^(i) OPTIMAL;
  (ii) deriving w*(v^(i)) < w*(v) proves v^(i) NOT optimal, so the other is.
Both dualise at Vmin. THE PAIR TEST Sep(v^(0),v^(1)) IS STRICTLY WEAKER AND IS
THE WRONG TEST. If you claim any mechanism stalls, you MUST test both (i) and
(ii) at every controlled vertex, and you MUST seed the programme with Z_0 and
Z_1 (the free attractor sweeps, linear time). Five stalls found in round 10
without that seed were all artefacts; the seed cracked every one.

# What is PROVED in frontier.tex (cite by label; do not reprove)

FOUNDATIONS. thm:lfp-general (val and every val_sigma are LEAST fixed points on
ARBITRARY SSGs); cor:comparison (two-sided, stopping games); lem:gen-comparison
(arbitrary sink payoffs); thm:contraction (rate 1-2^{-a}, attained);
lem:trapchar (U is a trap iff every avg vertex of U has BOTH successors in U
and every controlled vertex has SOME; G is stopping iff the only trap is empty;
hence the subgraph induced on C is ACYCLIC); thm:eval-stopfree (val_sigma by
LP with zero rows on the trap, arbitrary SSGs); lem:denominator-sharp (every
value has denominator dividing an integer <= 2^a, attained);
thm:stopping-transform (arbitrary SSG -> stopping SSG of size O(N(a + log N)),
all constants explicit; the threshold moves to an explicit dyadic theta and
the threshold gadget is needed); def:damping / lem:gadget (a stopping leak of
exactly beta = 2^{-m} is realised by a chain of m average vertices; an
ARBITRARY dyadic probability p = k/2^m needs the binary-expansion chain that
sec:fold describes in prose -- a route that needs it must implement and verify
it itself, at cost m average vertices per probability); lem:duality (the dual game G-bar, sinks and roles swapped, has
val = 1 - val OFF THE SINKS only).

POLYNOMIAL CLASSES (SIX). thm:few-avg (poly(N)2^a, arbitrary SSGs);
thm:few-denominator (NEW, round 14, sec:alphabet: stopping games whose values
share a common denominator D are solved in O(N^2 D^2) with no advance
knowledge of D, by the UP-rounded Shapley iteration on the grid, which is
exact on ANY finite grid containing the values -- thm:alphabet-iteration; the
value alphabet Lambda(G) with k letters is rigid, D <= 2^{k-2} sharply,
thm:alphabet-rigid / thm:alphabet-denominator; prop:fv-family gives FV_2(n)
inside this class and outside the other five; rem:alphabet-equivalence: a
poly-size SUPERSET of the alphabet is target-equivalent); thm:few-escape
(escape exponent d(G) <= a, separated from a by Theta(N) on prop:fk-family);
thm:kacyclic (ONE COLOUR off the cycles suffices; contains thm:avg-acyclic,
thm:player-free, thm:one-player); thm:bounded-components (all-switches halts
within sum_j (2^{|C_j|}-1) over SCCs of the Max-reachability digraph);
thm:escape-class (NEW, round 13): def:survival is the SURVIVAL OPERATOR S --
max at EVERY controlled vertex (Min's as well as Max's), mean at average
vertices, sinks read as 0; an escape certificate (lambda, x) has x >= 1 and
Sx <= lambda x, conditioning kappa = max x / min x; then two-sided value
iteration closes in O((a + log kappa)/log(1/lambda)) rounds, the certificate
enters only the running-time analysis, and its existence for fixed lambda is
one LP. prop:escape-family Z_D is inside this class and outside the four
combinatorial ones; rem:escape-class: NO member of the escape class is a stall
for M1, M2, M2T or M5, so the class cannot reach the frontier; on the wedge
every certificate has log(1/lambda) = 2^{-Theta(N)}. thm:subexp (random facet,
e^{2 sqrt n} poly(N)). A POLYNOMIAL CLASS here is a set of instances on which
some PROVED BOUND is polynomial; classes are compared as bounds, not as
algorithms.

REFORMULATIONS AND EQUIVALENCES -- all TARGET-EQUIVALENT, so a route that ends
at one of them has ended at the target and must say so:
thm:compare-equivalence (compare two vertex values); thm:order-determines (the
preorder induced by w* on Vavg u {t0,t1} determines w*; O(a log a) bits;
probably Gimbert-Horn, attribute); thm:decide-one-bit (a sound poly-time
DECISION rule resolving one controlled vertex per round exists IFF SSG-Value is
in P; termination by RETYPING the decided vertex as an average vertex);
prop:no-halving (no reduction halves a; comparing two average vertices is
target-equivalent); cor:wrong-equivalence; thm:transport-objective
(naming an optimal profile); thm:gap-equivalence ((Poly-Rule) itself);
rem:bsi (a GUIDE U whose order agrees with w* at every Max vertex is
target-equivalent).

STRATEGY IMPROVEMENT. thm:short-path (<= |Vmax| single improving switches
suffice from ANY sigma); cor:selection (all the difficulty is SELECTION);
thm:switch-count (every single-switch improving rule stops within N 2^a;
multi-switch within N 4^a); thm:ladder (def:ladder: L_n has Vmax = {v_1..v_n},
Vavg = {w_1..w_n}, v_i -> (v_{i+1}, w_{i+1}), w_i -> (v_{i+1}, w_{i+1}),
v_{n+1} = t0, w_{n+1} = t1; least-index and smallest-gap take 2^n - 1 switches
while all-switches takes n and the shortest improving route has length ONE);
cor:no-height (no progress measure of polynomial height on the Max strategy
lattice, with NO computability or numeric hypotheses); thm:impedance (no
potential of polynomial range); prop:serialiser; thm:normalform-barrier (no
residue-blind rule beats all-switches: lem:normalform makes the controlled
vertices an independent set preserving values, stopping and the whole
all-switches trajectory); thm:window-barrier (NEW, round 13: def:kblind puts
every value behind k+1 average two-cycles, so NO rule that solves exactly a
polynomially bounded number of average vertices halts in poly rounds unless
all-switches does); thm:all-switches-refuted (all-switches does not dominate
single switches); prop:allswitch-overshoot.

def:bsi (round 13, THE NEWEST MECHANISM AND NO BARRIER COVERS IT):
BIDIRECTIONAL IMPROVEMENT carries a PAIR (sigma,tau); L = val_sigma,
U = val^tau; S_sigma as above, S^tau = {u in Vmin : U(tau-bar(u)) < U(tau(u))};
vetoes C_max = {v in S_sigma : U(sigma-bar(v)) >= U(sigma(v))},
C_min = {u in S^tau : L(tau-bar(u)) <= L(tau(u))}; one round switches both
sets simultaneously; halt when both are empty; the STRICT variant uses strict
veto inequalities. thm:bsi-nostall: on a stopping game halting implies
L = U = w* (the trap argument of lem:max-deficit with w* replaced by U).
cor:bsi-correct: at most 2N4^a rounds. prop:bsi-nonstopping: stopping is
necessary (explicit 8-vertex instance). rem:bsi: without the vetoes it is
all-switches on G beside all-switches on G-bar (so a poly bound for THAT is
equivalent to one for all-switches); the veto by val^tau is the whole content;
a guide U ordering Max's successors as w* does is target-equivalent. ITS ROUND
COUNT IS OPEN and no superpolynomial family is known. ROUND 14 ADDED:
lem:bsi-pairloc / cor:bsi-levels (the argmax set Z of g = U - L always
contains an endorsed switch, so Phi = (M, |Z|) with M = max g strictly
decreases LEXICOGRAPHICALLY every productive round; rounds <= |V| x #levels,
where #levels = number of distinct values M takes -- a reparametrisation, not
a bound); prop:bsi-br / rem:bsi-br: if tau is ANY Min best response to sigma
and S_sigma is nonempty then C_max is nonempty, so R_BR(sigma) :=
sigma[{v in S_sigma : val^tau(sigma-bar(v)) >= val^tau(sigma(v))}] is a
SWITCHING RULE in def:rule's sense that halts only at an optimum; it is NOT
residue-blind, so thm:normalform-barrier and thm:window-barrier miss it; on
L_n it takes floor(log2 n)+1 rounds where all-switches takes n; on G# it takes
4 (all-switches 7) and switches c_1 TWICE. prop:bsi-twice: a vertex can be
switched more than once. Round 14's bsi-rounds route (unintegrated, code in
${SCRATCH}/root16/r14routes/bsi-rounds/) found Q_16, a reduced game with 8 Max
and 8 Min on which non-strict BSI switches Min vertex c_10 FOUR times
(four_switch_rows.json); its lem-bias says ladders are useless for BSI (a Max
vertex over a Max/avg pair with the same successor pair is never endorsed);
its prop-selfdual says on a SELF-DUAL game BSI collapses to a one-sided rule
MR reading val_sigma only. ATTRIBUTION: def:bsi is reported to be van
Dijk-Loho-Maat's generalised symmetric strategy iteration and R_BR its
one-track variant; Schewe-Trivedi-Varghese for symmetric improvement.
prop:closed-now-or-never (round 14): a CLOSED CONFIGURATION (W, pi) -- every
vertex reachable from pi(W) avoiding W is average or a sink -- once nothing is
switching into it, is bounded below by lambda_W for ever and NEVER ENTERED
AGAIN: the first irreversible event a polynomial bound could count; the
remark says it is NOT a barrier (a Max vertex over a Max vertex simulates a
third action with one round of lag). rem:lcp (round 14): the P_*(kappa)
interior-point route is CLOSED (handicap 2^{Omega(N)} on a one-player family
Y_k with |C| = 3; handicap EXACTLY 0 on every hard family here, which all have
|C| <= 2). thm:lasserre-vacuous (round 14): item (v1) is CLOSED NEGATIVELY --
the degree-two Lasserre lift of Q(G) improves the Q(G) bound by NOTHING on a
10-vertex two-player and on a 14-vertex ONE-player game.

THE ALL-SWITCHES / AUSO IDENTIFICATION -- THE PIVOT.
def:improvement-uso, prop:allsw-auso: for a NONDEGENERATE stopping SSG (no
tied incidence (sigma,i)) the improvement outmap is the outmap of an ACYCLIC
UNIQUE SINK ORIENTATION (AUSO) of the |Vmax|-cube and all-switches is exactly
its BOTTOM-ANTIPODAL (BA) walk. lem:auso-laws, cor:f-auso: f(m) >= h*(m), the
greatest BA height of an AUSO of the m-cube, exponential in general -- PROVED
HERE: thm:blowup (solo round, see below) gives h*(m+2) >= 2h*(m)+2, hence
h*(m) >= 2^{m/2+1}-2; the Schurr-Szabo import is GONE and thm:determinacy is
now the document's ONLY external input. prop:auso-census: h*(m) = 1,2,4,7 for m <= 4;
prop:hstar-five: h*(5) = 12 < f(5) = 13, so the laws are strictly weaker than
the axioms. prop:auso-size: at most 3^N (N+2)^{2N} N^m = 2^{O(N log N)}
orientations arise from stopping SSGs on <= N vertices, a 2^{-Omega(2^m)}
fraction once N = poly(m): NO CENSUS OR SAMPLING CAN DECIDE REALISABILITY,
ONLY A CONSTRUCTION. prop:auso-seven (round 13): the height-7 orientation
of the 4-cube IS realised by a nondegenerate two-player stopping SSG G# on 99
vertices (4 Max, 2 Min, 91 average; its harmonic normal form is printed in the
paper and reproduced in ${SCRATCH}/root16/seven.tex, t_seven.py). Also settled: no
stopping SSG with |Vmax| = 5 has an all-switches run of length 13. ROUND 14 REMOVED THE NONDEGENERACY HYPOTHESIS: def:flat, lem:trichotomy (no
cube edge points out at both ends; the two ends of a flat edge have the SAME
value vector), lem:flat-class (flat classes = level sets of sigma -> val_sigma
= subcubes), lem:face-sink, thm:flat-resolution (orienting flat edges towards
a chosen corner of each class RESOLVES the structure into a genuine AUSO
agreeing with the outmap at the corners), cor:ceiling-general (EVERY
all-switches run of EVERY stopping game, degenerate or not, is a BA walk of an
AUSO, so L <= h*(m) = 1,2,4,7,12 for m <= 5), cor:law-u (the switched sets
S_0..S_L are pairwise distinct). prop:oneplayer-lp (round 14): for a
NONDEGENERATE ONE-PLAYER stopping game the improvement orientation is the LP
orientation of the occupancy polytope X(G) (d'Epenoux's dual LP), a simple
m-polytope with the m-cube graph, hence HOLT-KLEE (Holt-Klee +
Gaertner-Morris-Ruest); cor:seven-two-player: G#'s orientation violates
Holt-Klee (TWO disjoint monotone source-sink paths on the 4-cube where 4 are
needed; max-flow 2, brute force over all 42 simple directed paths), so its
two Min vertices are NECESSARY. h*_HK(4) = 6 < 7 is VERIFIED by the root agent
(the height-7 orbit is G#'s and is non-HK; the height-6 outmap
0 1 3 2 5 14 7 4 13 10 11 12 9 6 15 8 is HK); h*_HK(5) = 11 < 12 is measured,
unverified; with cor:law-u the law ceiling is 1,2,4,7,12,21 at m <= 6
against f = 1,2,4,7,13,25 (f(6) = 25 is an exhaustive computation in
${REPO}/scripts/ceiling/f6.out). DEGENERATE one-player games are NOT bound by
Holt-Klee: thm:flat-resolution's resolution is a combinatorial completion,
not an LP orientation (rem:oneplayer-lp). WHAT IS MISSING: a family of stopping SSGs on N = m^{O(1)}
vertices whose all-switches run has SUPERPOLYNOMIAL length -- equivalently,
for nondegenerate games, an SSG-realisable AUSO of superpolynomial BA height.
Every family built here (WD, CC, TW, ...) has BA height 1. The ABSTRACT
doubling now EXISTS (thm:blowup, below); what is missing is its REALISATION
by games at polynomial total size, and N' <= N^c per level is NOT enough
(iterating gives N_0^{c^k}).

THE SOLO ROUND (root agent, 2026-09-02/03; everything below verified in exact
arithmetic, thm:blowup also machine-checked). READ THESE LABELS FIRST if your
route touches all-switches: lem:hstar-super, prop:D-quadratic, thm:blowup,
rem:blowup-measured, rem:blowup-realise, prop:gsharp-bigcube,
rem:gsharp-bigcube. Code: ${REPO}/scripts/blowup/ (README.md explains each
file) and ${SCRATCH}/solo/ (the full working directory).
 - lem:hstar-super: h*(k+l) >= h*(k) + h*(l), by
   s(v1,v2) = (s1(v1), s2(v2 xor c(v1))) with c = z off the s1-sink and 0
   at it.
 - prop:D-quadratic: the round-14 operation D (translation by 1-bar) gives
   heights 4,9,16,25,36 at dimensions 3,5,7,9,11 -- QUADRATIC; Holt-Klee at
   dimension 3, non-HK from dimension 5.
 - thm:blowup (PROVED; machine-checked in lean/SSGProof/Blowup.lean, no
   sorry, core library only): for ANY AUSO s of the m-cube with sink o and a
   vertex u of maximal BA height h, put z := o xor u; the (m+2)-cube
   orientation B(s) with layers (alpha,beta) has inner part s(v xor z) on
   layer 00 and s(v) on the other three layers, and outer part depending
   only on the layer and on the PARITY of h(v): 00 -> {}; 10 -> {a,b} if
   h(v) even, {a} if odd; 01 -> {b} if even, {a,b} if odd; 11 -> {a} if
   even, {b} if odd. Then B(s) is an AUSO of BA height >= 2h+2 (exactly
   2h+2 on every seed measured: 1-cube 4,10,22,46,94; 2-cube 2,6,14,30;
   G# 7,16,34,70; the h*(5) = 12 seed 12,26,54,110). Hence
   h*(m+2) >= 2h*(m)+2. The walk: from (10,u) if h is even, (01,u) if odd,
   it alternates 10 <-> 01 while running s's walk (h steps), then
   (10,o) -> (01,o) -> (00,o), then the TRANSLATE's walk from o, which is
   s's walk from u again (h steps).
 - rem:blowup-measured: from the second level on, z is a SINGLE coordinate
   of the previous level's outer pair (beta if that level's seed height was
   odd, alpha if even; heights after the first level are even, so alpha
   from the third level on): layer 00 presents the previous level "as if
   that coordinate were flipped". z = 1-bar gives D (quadratic). REVERSING
   all inner edges instead (what a game does by swapping its sink payoffs)
   gives 4,10,16,23,30 -- linear, because the reversed orientation's walk
   from the old sink is short. Per-coordinate reversal s(v) xor z is a USO
   but not acyclic from level 2.
 - THE FIRST LEVEL IS REALISED: B(1-cube) = outmap [0,1,3,6,7,4,5,2] of the
   3-cube, height 4, is the improvement orientation of a nondegenerate
   ONE-PLAYER stopping SSG on 58 vertices (3 Max, 53 avg):
   ${REPO}/scripts/blowup/B1_game.json, normal form G_m3_k0_den64_s1.json,
   verified from the game (verifyG.py); Holt-Klee as prop:oneplayer-lp
   requires.
 - A TRANSLATED LAYER IS REALISED AT INNER DIMENSION TWO (root agent,
   2026-09-03, ${SCRATCH}/solo/b2cube.py): B(2-cube) for the height-2 seeds
   [0,1,3,2], [0,3,2,1], [3,0,1,2], [3,2,0,1] is ONE Holt-Klee AUSO class of
   the 4-cube of height 6, canonical outmap
   [0,1,3,2,7,6,4,13,15,14,12,9,11,10,8,5], and it is realised by the
   nondegenerate one-player stopping SSG
   ${SCRATCH}/solo/AP_m4_k0_den256_s200_game.json (N = 100: 4 Max, 94 avg;
   normal form AP_m4_k0_den256_s200.json, denominator 256; a second
   realisation AP_m4_k0_den512_s126, N = 109), verified from the game: BA
   height 6, walk [2, 8, 5, 9, 13, 14, 15]. Its layer 00 carries the inner
   2-cube TRANSLATED BY 1-bar, i.e. each inner vertex compares its options
   as if the other were flipped -- so the "anti-value" of rem:blowup-realise
   is an obstruction to one naive substitution, NOT a theorem: monotone
   readouts do produce a translated sign pattern at inner dimension two.
   (The other four height-2 seeds give a non-HK B.)
 - THE SECOND LEVEL B^2 = B(B(1-cube)) IS THE SMALLEST OPEN INSTANCE:
   5-cube, height 10, NOT Holt-Klee (so it needs Min vertices), outmap
   [7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,
   22,15,12,13,18] (bits 0,1,2 inner = B^1 with bit 1 = alpha_1, bit 2 =
   beta_1; bits 3,4 = alpha_2, beta_2); layer 00 carries s1(v xor e_2),
   differing from s1 in 16 of 24 inner incidences: all 8 at coordinate 2
   itself and 8 at other vertices, (v,i) = (0,0),(0,1),(1,0),(2,1),(4,0),
   (4,1),(5,0),(6,1). Integer and float searches for it (huntG, huntW2,
   ascendB, realiseAP with k = 2,3 Min vertices; hours) did NOT converge,
   but the same searches also failed to re-find G#'s known walk in the same
   budget, so that is not evidence; round 13's curriculum search stalled on
   m = 5 walks too. DO NOT RETRY WITH THE SAME TOOLS; design by hand.
 - rem:blowup-realise: the layer-00 CONDITION is readable in the same round
   (both outer vertices at rest; a Max vertex x over p,q is at rest iff
   val(x) = max(val p, val q), the value of a Max vertex over p and q). The
   OPERATION was thought to be the obstacle: on layer 00 an inner vertex
   must compare its options as it would at v xor e_j, and j's state reaches
   the rest of the game only through val(j), so a naive substitution would
   need the ANTI-VALUE val(j^0)+val(j^1)-val(j), strictly decreasing in
   val(j), while every SSG value is NONDECREASING in every other. What a
   gadget can do is reproduce the SIGN PATTERN: swapped weights and a
   constant shift, conditional summands as min(theta,x) through a Min
   vertex against a threshold theta built from the rest predicates. The
   realised B(2-cube) game shows this is possible with monotone readouts at
   inner dimension two; how it does it has NOT been analysed.
 - BITS ARE READABLE AS PREDICATES, INSTANTANEOUSLY: sigma_j = 1 iff
   val(x_j) = val(E_j^1); an equality test is a comparison of two option
   values (1/2 min(x_j,E^1) + 1/2 K' against 1/2 max(x_j,E^1) + 1/2 K),
   robust while |E^0 - E^1| > eps. What is NOT available is turning a
   comparison outcome into an ABSOLUTE value level. Gadgets should use Min
   vertices and coins (instantaneous) rather than extra Max readers, whose
   values lag by two rounds.
 - prop:gsharp-bigcube: G#'s full 6-cube orientation (each of the 6
   controlled vertices strictly prefers its other action) is nondegenerate,
   a USO, ACYCLIC, HOLT-KLEE, of BA height 5; its Min-face sinks are Min's
   best responses and its sink projection is EXACTLY s_{G#} (height 7,
   non-HK): projection loses Holt-Klee and gains height.
   ${REPO}/scripts/blowup/bigcube.py.
 - ONE-PLAYER REALISABILITY AT m = 4 (root agent's survey,
   ${SCRATCH}/solo/realiseAP.py, sampleAP.py, survey_*.json;
   census/classes4.txt = one representative per AUSO class of the 4-cube,
   12640 classes: heights 1:1, 2:754, 3:4776, 4:5404, 5:1561, 6:143 of which
   56 are Holt-Klee, 7:1): an evolution strategy over the average part P
   plus an exact LP over the controlled rows Q, then dyadic rounding and an
   exact normal-form check. ALL 56 HK height-6 classes are realised by
   one-player games (53 exactly at denominator 1024; AP_m4_k0_*.json); 33
   random non-HK height-6 classes ALL FAIL (the control prop:oneplayer-lp
   demands); of 60 random HK height-5 and 60 random HK height-3/4 classes,
   all but 5 are realised (survey_h5HK_k0.json idx 26, 40; survey_h34HK_k0.json
   idx 10, 45, 49 unresolved after 2 x 600 s). INTERPRETATION (measured, not
   proved): at m = 4 Holt-Klee appears to be the WHOLE condition for
   one-player realisability. In the blow-up rule family NO HK-preserving
   rule doubles (blowhk.py: best HK-preserving growth 4,9,12); translation
   breaks HK from level 2. Klee-Minty cubes have BA height exactly d for
   d <= 12 (km.py): LP-hard, BA-easy.

THE MECHANISMS AND WHERE THEY STOP (sec:gap).
 M1 def:simorder, the value-simulation preorder: arithmetic-free, one greatest
 fixed point, beats every bounded radius, dies on branch compensation (G8);
 thm:matching-barrier kills its whole class.
 M2 def:slack, the slack calculus (Delta_k(x,y) bounds w*(x)-w*(y) from above;
 a negative entry decides); thm:slack-barrier and thm:slack-vi-upper SANDWICH
 it: on separated configurations it IS two-sided value iteration.
 M2T def:trans-slack (min-plus transitive closure): thm:trans-complete says on
 STOPPING games it converges to the exact differences, so the question is a
 RATE; prop:trans-Hm collapses H_m from 2^{Omega(N)} to 4m-3 rounds.
 M3 def:seeded, seeding from policy evaluation; thm:seeded-barrier;
 thm:seed-dichotomy: if sigma has no strictly switchable vertex and tau is
 greedy for val_sigma then the seed is EXACT, so EVERY STALLING INSTANCE OF M3
 HAS BOTH PLAYERS PRESENT AND IS A STOPPING GAME ON WHICH ALL-SWITCHES HAS NOT
 CONVERGED AFTER p ROUNDS.
 M4 def:transport, the LP over Q(G) = {x : x(v) >= x(v^i) at Max, <= at Min,
 mean at avg, 0 <= x <= 1, sinks pinned}; Sep(p,q) = max x(q)-x(p) over Q;
 lem:transport-dim (Q(G) is affinely |C|-dimensional: every x in Q is the
 harmonic extension of x|_C); Q(G) has <= 3|C| facets but EXPONENTIALLY many
 vertices; thm:transport-objective (w* is a VERTEX of Q(G); the difficulty is
 choosing among 2^{|C|} objectives); prop:own-stall (a GENUINE decision stall
 of M4 on 10 vertices, R: Vmin = {0,1,6,7}, Vmax = {4}, Vavg = {2,3,5};
 0->(2,5), 1->(5,3), 2->(5,2), 3->(0,t1), 4->(0,t0), 5->(t1,t0), 6->(0,t0),
 7->(5,2)).
 M5 sec:hybrid, the transport-slack hybrid: thm:hybrid-complete,
 lem:hybrid-cutting, prop:hybrid-onectrl (|C| = 1 is exact at round two, which
 is why every early measurement was uninformative), thm:hybrid-lower (CC(L,m):
 Vmax = {v1,v2}, one-player, crosswise chains; 2^{Omega(N)} rounds for the
 pair entry) and rem:hybrid-lower-not-a-refutation; thm:hybrid-convex-barrier
 (a METHOD: a shrinking chain of convex certificates bounds every entry below).
 M6 sec:ratio (NEW, round 13): def:ratio, the MULTIPLICATIVE calculus
 (w*(x) <= R(x,y) w*(y); harmonic mean and mediant at average vertices),
 thm:ratio-sound, thm:ratio-sandwich (the SAME two-sided bound as M2),
 cor:ratio-stall (same stall on H_m at rounds 15, 39, 101), prop:ratio-
 incomparable (pairwise incomparable with M2), def:mobius / prop:mobius (a
 continuum between M2 and M6, every member stalling identically),
 prop:ratio-closure (the min-times closure escapes as the min-plus one does:
 7, 11, 15, 20, 24 on H_m), prop:cw (the Collatz-Wielandt bracket bounds
 nothing after homogenisation). MORAL: thm:slack-barrier constrains any
 calculus matching the two branches of an average vertex ONE AT A TIME,
 whatever the algebra.
 sec:wedge, THE STATE OF THE ART ON THE NEGATIVE SIDE. def:wedge WD(e,j,m),
 N = 2e+j+m+5, ONE-PLAYER, Vmax = {v1,v2}, both value-distinguishing with gap
 2^{-m}: Z-seeded own-successor hybrid first fires at rounds 4, 8, 17, 35, 70,
 140 at N = 21..51 (prop:wedge, a measurement), and thm:wedge-proved +
 cor:wedge-count make the silence UNCONDITIONAL: K = 1,6,15,33,68,138,279,560
 silent rounds for j = 2..9, so 2^{Omega(N)}. rem:wedge: WD defeats M2, M2T,
 M4, M5 and M6 (min-times closure: 30, 87, >170 at N = 21,27,33) and defeats
 NEITHER M1 (the gfp contains (v_i, a_{i,1}), firing direction (i) at round
 zero) NOR M3 (one-player, so the seed is exact by thm:seed-dichotomy). THE
 OPEN ITEM: a family defeating M1 AND M3 as well -- by thm:seed-dichotomy a
 family defeating M3 is a superpolynomial all-switches family.

BARRIERS, and exactly what each covers. thm:impedance (polynomial RANGE);
cor:no-height (polynomial HEIGHT on the Max lattice); prop:locality (bounded
radius, every k); thm:normalform-barrier (residue-blind rules);
thm:window-barrier (polynomial windows); thm:matching-barrier;
thm:slack-barrier / thm:seeded-barrier / thm:ratio-sandwich;
thm:hybrid-convex-barrier (a method, not a barrier); prop:no-submodular
(the strategy-space objective is not submodular in any orientation of either
cube; lem:readonce); sec:fold / thm:fold (freezing one vertex at payoff theta
gives a response map with EXACTLY 2^D pieces -- kills continuations that TRACK
THE OPTIMAL PAIR); thm:vi-lower (value iteration exponential with NO players);
thm:separable (NEW, round 13: a certificate phi(x)-psi(y) surviving a min-plus
closure must have phi = psi = a fixed point of T, so on a stopping game it is
the exact limit and proves NOTHING about a rate; a rate certificate for any
closed calculus must have ZERO DIAGONAL and be genuinely matrix-valued; the
same holds multiplicatively, rem:mobius); prop:a-presentation (a is a property
of the presentation).

# UNVERIFIED claims from rounds 10-14 (do NOT cite as established)

(v1) CLOSED by thm:lasserre-vacuous (see above). Still unverified from that
 route: exact iff |C| <= 2; a CYC family with a spectral criterion.
(v2) NOW PROVED as prop:oneplayer-lp. h*_HK(4) = 6 is verified; h*_1(4) = 6 is
 measured (every HK height-6 class realised, no non-HK one); h*_HK(5) = 11 is
 unverified.
(v3) All-switches on stopping ONE-player SSGs is exactly Howard's policy
 iteration on transient 2-action MDPs, both directions. If so the one-player
 half of the pivot is "is Howard's rule polynomial on 2-action MDPs".
(v4) An exact two-way dictionary between stopping SSGs and 2|C| substochastic
 affine maps (the HARMONIC NORMAL FORM: the first-passage law of the average
 part from each action, a substochastic row over C u {t1}); realisability of a
 prescribed AUSO is then an exact LP feasibility question. Round 12 proved two
 additivity obstructions to composition and one +1 scheme.
(v5) TW(2j,j,j+4), N = 8j+13, two Max and two Min, keeps the Z-seeded
 own-successor hybrid silent at all four controlled vertices for 5, 10, 19, 39
 rounds at N = 37,45,53,61; confirmed independently by round 13; its published
 mechanism was WRONG (Min's non-optimal action is an ACCELERANT). All-switches
 halts on it in ONE round (BA height 1).
(v6) The M-factorable (hidden-K / hidden-Z) case of the SSG LCP is one LP
 (Mangasarian, published). thm:lcpM-spectral: rho(Phi) < 1 implies w* is the
 unique optimum of one explicit LP over Q(G); its "class S_2" and minimality
 clause were refuted.
(v7) Newton on F(x) = x - Tx: piecewise-affine homeomorphism, Lip(F^{-1}) =
 kappa(G) <= N 2^a attained; plain Newton CYCLES with period 3 on a 25-vertex
 stopping SSG.
(v8) A poly-startable exact CONTROL HOMOTOPY annihilates WD and CC yet needs
 2^{0.146N} switches on thm:fold's P_D.
(v9) The approximation collapse is Dai-Ge (prior art).
(v10) UEOPL: the canonical line is exponential (PEN(D,K)); but the route's
 induction used an inequality equivalent to D < 4; DO NOT cite.
(v11) A regularisation error bound "kappa(G) = max expected visits to
 controlled vertices" -- bounded kappa gives a polynomial algorithm
 unconditionally (it is the resolvent of def:survival), so any algorithm
 conditional on it is worthless; cor:sm-no-reg was refuted.

# PRIOR ART THIS PROJECT HAS ALREADY REDISCOVERED (fifteen times)

Auger-Coucheney-Strozecki (almost-acyclic SSGs, FPT in the feedback vertex
number); Mangasarian (hidden-K LCP by one LP); Gaertner-Morris-Ruest
(realisable USOs are Holt-Klee); Stickney-Watson (LCP/USO correspondence);
Gimbert-Horn (the permutation space and its decoder); Dai-Ge (approximation
collapse); Meyer (stochastic complementation / censored chains = exact vertex
elimination); Kannan-Theobald (fixed-rank games, cells of a hyperplane
arrangement); Blondel-Nesterov (the escape rate as a joint spectral radius);
van Dijk-Loho-Maat (def:bsi is their generalised symmetric strategy
iteration; R_BR its one-track variant); Melekopoglou-Condon (thm:ladder's
least-index 2^n - 1 on two-action instances, and the OPEN QUESTION they
leave, Howard's rule with two actions per state, which IS the one-player
half of this project's pivot); d'Epenoux (the occupancy LP X(G)); Holt-Klee
and Gaertner-Morris-Ruest (LP orientations and realisable USOs are
Holt-Klee); Hansen & Ibsen-Jensen (2TBSG -> P-matrix LCP, interior-point
bounds); de Klerk & E.-Nagy (exponential handicap of sufficient matrices);
Haddad-Monmege (two-sided rounded iteration); the abstract-interpretation
exactness criterion (extensive rounding preserves least fixed points).
STATE OF THE ART on the pivot, as the round-14 free-search-14 route reported
from its own knowledge: exponential all-switches lower bounds exist for
parity / mean-payoff / discounted / simple stochastic games (Friedmann 2011)
and for Howard on total- and average-reward MDPs (Fearnley 2010) and
reachability MDPs (Christ-Yannakakis 2023), ALL with Theta(n) actions per
state; for a CONSTANT number of actions the best known lower bound for
Howard's rule is LINEAR (Mukherjee-Kalyanakrishnan 2025). A superlinear
binary family would therefore be new even for one player. Condon 1992 is the source of the problem and of the stopping
transformation; Ludwig and Bjorklund-Vorobyov of the random-facet bound;
Schewe-Trivedi-Varghese of symmetric strategy improvement for parity games.
If your route reproduces something standard, SAY SO and attribute it. A
rediscovery honestly labelled is useful; a rediscovery presented as new is a
defect.

DEAD, not to be re-derived: entropic/softmax regularisation; Newton-Dinkelbach
(Radzik/Megiddo with one SSG-specific line); polynomial classes by the rank of
an action-difference matrix (Kannan-Theobald); Schur/vertex elimination
(Meyer); vertex enumeration of Q(G) (exponentially many vertices even on
linear-time instances); the bubble step in order space (FALSE on an 8-vertex
game); totally ordered universal lattices (height 2^{Omega(N)}).

# The rules of this round

1. RIGOUR. Return concrete lemmas, constructions, equations, or counterexamples.
   Status reports and "this step is routine" are rejected. If you cannot prove a
   step, mark it GAP and state the missing statement EXACTLY, in one
   self-contained sentence.
2. VERIFY EVERYTHING in EXACT RATIONAL ARITHMETIC (python3 fractions.Fraction).
   Never floating point for a claim (floats may be used to EXPLORE). NEVER
   compute val_sigma by greedy policy iteration in a possibly non-stopping game
   -- it is unsound; take the componentwise min over ALL positional tau, or use
   thm:eval-stopfree, or a least fixed point.
   A ready harness is at ${SCRATCH}/root16/ : mycore.py (SSG core: class
   G(kinds, succ) with kinds in {'max','min','avg'}, non-sinks 0..n-1, t0 = n,
   t1 = n+1; profile_value, wstar by brute force, trap-based is_stopping,
   T_op, Z01, slack_step, minplus_close, transport_rows/transport_sep, hybrid),
   core.py (a second independent core), mylp.py and lp.py (exact two-phase
   simplex with Bland's rule), zseed.py (the free Z_0/Z_1 seed), ownhyb.py
   (the own-successor test), auso.py and census/ (USO/AUSO predicates, BA
   walks, law checking), normform.py (harmonic normal form search), hyb2d.py
   and rathyb.py (exact 2-D polygon engines for |C| = 2), cc.py (CC(L,m)),
   wd.py (WD(e,j,m)), myinst.py (G8, S, S_r, H_m, G_m, A0), gstar.py (G*),
   t_bsi.py (a BSI check), t_escape.py (the escape class), ratio.py and
   mobius.py (M6). Round-14 route code is under ${SCRATCH}/root16/r14routes/
   (allsw-lower/: allsw.py, mdp.py, gsharp.py, hk.py, blowsearch*.py,
   allswlower.tex; free-search-14/: build.py, t_lane.py, fastsw.py, fs14.tex;
   bsi-rounds/: bsi.py, osc.py, selfdual.py, realise.py, four_switch_rows.json,
   bsi_rounds.tex). Round-13 and round-14 route directories with their own
   code are beside it:
   ${SCRATCH}/../../dc099d6a-f89a-421b-bbe2-2a87a9e19322/scratchpad/
   (auso-pivot/, two-player-wedge/, ...) and
   ${SCRATCH}/../../26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad/
   (allsw-lower/, allsw-degeneracy/, lasserre-2/, lcp-handicap/). The solo round's working directory is ${SCRATCH}/solo/ (realiseAP.py,
   sampleAP.py, ap_es.py, ap_lp.py, ap_realise.py, blowz.py, blowc.py,
   blowvar.py, blowhk.py, blowind.py, my_D.py, my_super.py, bigcube.py, km.py,
   leap.py, lv1.py, rowgame.py, huntG.py, huntW2.py, verifyG.py, fastnf.py,
   nf2.py, build.py, verify.py, b2cube.py, census/classes4.txt,
   survey_*.json, AP_m4_k0_*.json = exact one-player games realising 4-cube
   classes, B1_game.json, the *_game.json files = explicit games) and the
   committed subset is ${REPO}/scripts/blowup/. COPY what you need into
   ${SCRATCH}/<your-route>/ and work there. Do NOT write into another route's directory and do NOT modify
   ${REPO}/frontier.tex -- the root agent integrates.
3. KNOWN TRAPS, each of which has cost this project real time.
   - Building a constraint row as a dict LITERAL {a: 1/2, c: 1/2} silently
     collapses when a == c. ALWAYS accumulate: d[u] = d.get(u,0) + coeff.
   - When adding fresh vertices, carry the sinks as SENTINELS and map them to
     indices only at the very end.
   - Before believing "the polytope is infeasible", check that w* is feasible.
   - The trap Z_sigma must ADMIT t0 and exclude only t1.
   - Any bound |T^k y - T^k z| <= (...)^k needs y, z to AGREE WITH THE SINK
     PAYOFFS; T pins the sinks only from the first application onward.
   - Membership of a polynomial class is a property of the instance AS POSED:
     check every structural parameter on the subgame REACHABLE FROM v0.
   - When comparing rules, count PRODUCTIVE rounds on both sides, and state
     WHICH VARIANT of a mechanism a measurement used.
   - RANDOM SAMPLING HAS NEVER FOUND A HARD INSTANCE IN THIS PROJECT. Every one
     had to be ENGINEERED. "No counterexample in 100000 samples" is NOT
     evidence; say so if that is all you have.
   - Check whether your instance set VARIES the parameter your mechanism turns
     on. Round 10 measured a mechanism only at |C| = 1, a class it trivialises;
     round 11 searched raw games when the right space was the harmonic normal
     form; round 12 reported "34429 steps, 0 failures" for a lemma FALSE on an
     8-vertex game; round 13 separated a family from every class using vertices
     UNREACHABLE from the start.
   - After proving or measuring anything on the instances you developed it on,
     RE-RUN it on freshly generated, larger instances before reporting.
4. HONESTY. Never present an unproved statement as proved. If your route ends at
   a lemma of the same strength as the target, SAY SO and mark it blocked --
   that is a valid and useful outcome. Do not report the problem as open and do
   not editorialise about difficulty; report mathematics.
5. Return paste-ready LaTeX for what you PROVED, in the amsthm style of
   frontier.tex, labels prefixed by your route name.
6. NO WEB. Do not use WebSearch, WebFetch or any network access. Use your own
   knowledge and your own computation only. Attribute prior art from memory
   and flag it as "from memory, unchecked against the source".
7. TIME. You have a long budget but not an unbounded one: budget your
   computations (background long runs with nohup and poll them; keep each
   foreground command under ten minutes), and return a complete structured
   result even if a computation is still running -- say what is running and
   where its output goes.
`

const ROUTE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['route', 'verdict', 'headline', 'results', 'gap', 'next_steps'],
  properties: {
    route: { type: 'string' },
    verdict: { type: 'string', enum: ['SOLVED', 'strict-progress', 'blocked', 'dead-end'] },
    headline: { type: 'string' },
    results: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'statement', 'status', 'argument', 'verification'],
        properties: {
          name: { type: 'string' },
          statement: { type: 'string' },
          status: { type: 'string', enum: ['proved', 'refuted', 'gap', 'measured'] },
          argument: { type: 'string' },
          verification: { type: 'string' },
        },
      },
    },
    gap: { type: 'string' },
    latex: { type: 'string' },
    code_dir: { type: 'string' },
    next_steps: { type: 'string' },
  },
}

const AUDIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['target', 'sound', 'confidence', 'findings', 'verdict'],
  properties: {
    target: { type: 'string' },
    sound: { type: 'boolean' },
    confidence: { type: 'string', enum: ['low', 'medium', 'high'] },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['severity', 'result_name', 'defect', 'evidence'],
        properties: {
          severity: { type: 'string', enum: ['fatal', 'major', 'minor', 'note'] },
          result_name: { type: 'string' },
          defect: { type: 'string' },
          evidence: { type: 'string' },
        },
      },
    },
    verdict: { type: 'string' },
  },
}

const ROUTES = [
  {
    key: 'gadget',
    model: 'opus',
    title: 'Realising the second blow-up level by hand: the inner game is given, the outer layer is a design problem',
    brief: `
YOUR ROUTE IS THE CONSTRUCTIVE SIDE OF THE PIVOT'S DICHOTOMY
(rem:blowup-realise). Read thm:blowup, rem:blowup-measured,
rem:blowup-realise, prop:gsharp-bigcube, prop:oneplayer-lp,
cor:seven-two-player, thm:impedance, lem:switch and def:improvement-uso
first, then ${REPO}/scripts/blowup/README.md and the code it names, then
${SCRATCH}/solo/b2cube.py (the root agent's computation summarised below).

THE TARGET. B^2 := B(B(1-cube)), an AUSO of the 5-cube of BA height 10.
Outmap (vertex index v = bit0 + 2 bit1 + 4 bit2 + 8 bit3 + 16 bit4; the
outmap value is the bitmask of coordinates pointing OUT):
  [7, 4, 5, 2, 0, 1, 3, 6, 24, 9, 27, 14, 31, 28, 29, 10,
   16, 25, 19, 30, 23, 20, 21, 26, 8, 17, 11, 22, 15, 12, 13, 18].
Bits 0,1,2 are the INNER cube carrying s1 := B(1-cube) = [0,1,3,6,7,4,5,2]
(bit 0 the seed coordinate, bit 1 = alpha_1, bit 2 = beta_1); bits 3,4 are
the outer layer (alpha_2, beta_2). The layer (alpha_2,beta_2) = (0,0)
carries the TRANSLATE s1(v xor e_2): the translated coordinate is j = bit 2
(beta_1, because the seed's height 1 is odd; from the third level on it is
alpha). Exactly 16 of the 24 inner incidences of layer 00 differ from s1:
all 8 at j itself ((v,2) for every v: j's own preference is reversed at
every inner vertex, which a threshold shift can do) and 8 with i != j:
(v,i) = (0,0),(0,1),(1,0),(2,1),(4,0),(4,1),(5,0),(6,1) -- inner vertices
0 and 1 must compare their options AS IF j WERE FLIPPED. B^2 is NOT
Holt-Klee (a 3-face fails), so by prop:oneplayer-lp any nondegenerate
realisation has Min vertices.

WHAT IS ALREADY REALISED, and what you must reverse-engineer FIRST.
 (a) s1 itself: ${REPO}/scripts/blowup/B1_game.json is a nondegenerate
     one-player stopping SSG on 58 vertices (3 Max, 53 avg); its harmonic
     normal form (rows over C u {t1}, denominator 64) is
     G_m3_k0_den64_s1.json in the same directory. The inner of B^2 can be
     THIS game.
 (b) A TRANSLATED LAYER IS REALISABLE AT INNER DIMENSION TWO. B(2-cube),
     for the four height-2 seeds [0,1,3,2], [0,3,2,1], [3,0,1,2],
     [3,2,0,1] of the 2-cube, is one Holt-Klee AUSO class of the 4-cube of
     height 6, and it is realised by the nondegenerate ONE-PLAYER stopping
     SSG ${SCRATCH}/solo/AP_m4_k0_den256_s200_game.json (N = 100: 4 Max,
     94 avg; normal form AP_m4_k0_den256_s200.json, denominator 256; a
     second realisation AP_m4_k0_den512_s126, N = 109), both verified from
     the game by verifyG.py: BA height 6, walk [2, 8, 5, 9, 13, 14, 15].
     There the translation is by 1-bar of the 2-dimensional inner cube, so
     on layer 00 EACH inner vertex compares its options as if the OTHER
     were flipped -- the very operation rem:blowup-realise calls the
     obstacle -- and a one-player game does it with monotone readouts.
     YOUR FIRST TASK is to explain HOW: from that game's normal form write
     each inner vertex's two option values, on each of the four layers, as
     explicit affine-fractional functions of the other inner vertex's value
     and of the outer values, and exhibit the mechanism (which weights,
     which shifts, where the thresholds sit) by which layer 00 shows the
     translated sign pattern while layers 10, 01, 11 show s. State it as a
     lemma about normal-form rows. Then decide whether the mechanism is
     specific to a translation by 1-bar at dimension 2 or extends to a
     single-coordinate translation e_j at dimension 3 with two OTHER
     vertices reading j.
 (c) Do the same for B1_game.json (inner dimension 1: layer 00 carries the
     reversal of the seed coordinate) -- the simplest instance of the outer
     rule, whose two outer coordinates switch in every round of the inner
     walk according to the PARITY of the inner height.

THEN BUILD. Design, by hand and with exact LP on the harmonic normal form
(${SCRATCH}/solo/ap_lp.py, nf2.py, realiseAP.py -- for a FIXED average part
P the LP over the controlled rows Q is exact and linear;
${SCRATCH}/root16/r14routes/allsw-lower/gsharp.py), a stopping SSG with 5
Max vertices, and as few Min vertices as needed, whose improvement
orientation is B^2. Structure it: inner = the 58-vertex game or a re-solved
variant; outer = alpha_2, beta_2 with the parity-of-height rule (along
B^1's walk the heights 4,3,2,1,0 alternate in parity, and the rest
predicate of the outer pair is readable in the same round: a Max vertex x
over p,q is at rest iff val(x) = max(val p, val q), the value of a Max
vertex over p and q); layer-00 translation = the mechanism of (b)
generalised, or the weight-swap of rem:blowup-realise (swapped weights and
a shift, with conditional summands min(theta, x) through Min vertices
against a threshold theta built from the rest predicates). FIX THE SUPPORT
PATTERN of the rows by design and solve for the entries by LP; do not run
blind searches (huntG, huntW2, ascendB and realiseAP at m = 5 with k = 2,3
all failed for hours, and round 13's curriculum search failed before them).

DELIVERABLES, in order of value. (1) An explicit stopping SSG realising
B^2: kinds and successor lists, verified FROM THE GAME with
${SCRATCH}/solo/verifyG.py's machinery or your own exact code --
nondegenerate, USO, acyclic, outmap = B^2, and the all-switches run of
length 10 from the start of thm:blowup's proof printed round by round with
the exact value vectors. (2) The size recurrence for the next level (B^3:
dimension 7, height 22): does |C| grow by O(1) and the average part by
O(N) per level, or multiplicatively? If multiplicative, give the exact
recurrence -- still a theorem. (3) If you fail, the obstruction AS A
THEOREM with an explicit instance: "no game of shape X (inner =
B1_game.json, outer = ...) has layer-00 orientation s1(v xor e_2), because
Y", where Y is a computed impossibility -- an infeasible exact LP for a
fixed support pattern is a theorem about that pattern; say exactly which
patterns you excluded and which you did not.

REQUIREMENTS. Exact rational arithmetic for every claim; floats only to
explore. val_sigma with Min present is a minimum over ALL positional tau or
thm:eval-stopfree's LP, never greedy policy iteration. Every probability
other than 1/2 realised by average chains (lem:gadget), size cost reported.
Labels prefixed gad:.
`,
  },
  {
    key: 'monotone-lemma',
    model: 'opus',
    title: 'What monotone readouts can and cannot do: the negative side of the blow-up dichotomy, tested at the smallest open size',
    brief: `
YOUR ROUTE IS THE NEGATIVE SIDE OF THE PIVOT'S DICHOTOMY
(rem:blowup-realise): either a gadget realises the height-doubling
blow-up, or there is a THEOREM that improvement orientations of stopping
SSGs cannot present, on one face, the translate of what they present on a
parallel face. Read thm:blowup, rem:blowup-measured, rem:blowup-realise,
prop:oneplayer-lp, cor:seven-two-player, prop:gsharp-bigcube,
thm:flat-resolution, lem:trichotomy, thm:impedance and lem:switch first.
Another route works on the constructive side; you do not coordinate with
it, and you must not assume it fails.

THE FACTS YOU MUST BE CONSISTENT WITH (verified by the root agent in exact
arithmetic; code in ${SCRATCH}/solo/: b2cube.py, B2CUBE.txt, verifyG.py).
 (i) B(1-cube) = [0,1,3,6,7,4,5,2] (3-cube, height 4) is realised by a
     one-player game on 58 vertices (${REPO}/scripts/blowup/B1_game.json).
     Its layer 00 carries the REVERSAL of the seed coordinate.
 (ii) B(2-cube) (4-cube, height 6, Holt-Klee) is realised by a one-player
     game on 100 vertices (${SCRATCH}/solo/AP_m4_k0_den256_s200_game.json;
     a second on 109). Its layer 00 carries the inner 2-cube orientation
     TRANSLATED BY 1-bar: each inner vertex compares its options as if the
     other were flipped. So "an inner vertex cannot read another's flipped
     bit" is FALSE as a general statement -- monotone readouts do it at
     inner dimension two.
 (iii) B^2 = B(B(1-cube)) (5-cube, height 10, NOT Holt-Klee; outmap in
     ${SCRATCH}/solo/b2cube.py's output) is the smallest instance not
     known to be realisable; its layer 00 is s1(v xor e_2), differing from
     s1 in 16 of 24 incidences, 8 of them at vertices other than the
     translated coordinate.
 (iv) prop:oneplayer-lp: nondegenerate one-player orientations are LP
     orientations of the occupancy polytope, hence Holt-Klee. At m = 4
     every Holt-Klee height-6 class was realised by a one-player game (56
     of 56) and every non-HK one failed (33 of 33).

FORMULATE THE RIGHT STATEMENT, then prove or refute it. Candidates, from
weakest to strongest; settle what you can and say precisely what remains.
 (A) ONE PLAYER. Is every Holt-Klee AUSO of the m-cube the improvement
     orientation of some nondegenerate one-player stopping SSG? (iv) says
     yes at m <= 4, height 6, empirically. If yes in general, there is NO
     one-player law beyond Holt-Klee and the one-player half of the pivot
     is the abstract question "do Holt-Klee AUSOs have superpolynomial
     bottom-antipodal height". If no, find the smallest Holt-Klee AUSO
     that is not an occupancy-polytope orientation and state the extra
     necessary condition as a lemma. From your own knowledge (flag it as
     from memory): what did Develin, and Morris, prove about the
     sufficiency of Holt-Klee for LP orientations of cubes in dimensions
     3 and 4, and does an occupancy polytope of a two-action transient MDP
     -- a deformed cube of a very special kind -- satisfy anything more?
 (B) TWO PLAYERS, THE STRUCTURAL CONSTRAINT. prop:gsharp-bigcube shows the
     Max cube is the SINK PROJECTION of the Holt-Klee USO of the
     (m+k)-cube (Stickney-Watson; Gaertner-Morris-Ruest). State and prove
     what the sink projection of a Holt-Klee USO of the (m+k)-cube MUST
     satisfy -- a "projected Holt-Klee" condition: a lower bound on
     disjoint monotone paths in terms of k, or a bound on the height it
     can gain -- and test it on B^2: what is the least k for which B^2
     could be a sink projection of a Holt-Klee USO of the (5+k)-cube? If
     your condition excludes B^2 for every small k, that is a theorem
     about which orientations two players can realise at bounded |Vmin|,
     and it bounds the Min vertices any realisation of level L needs.
 (C) THE MONOTONE-READOUT LEMMA PROPER. Fix the inner game (a subgame H
     with boundary ports whose payoffs are values of the rest of the game,
     hence MONOTONE nondecreasing functions of H's own values, by
     thm:lfp-general and Min's best response being a minimum of such).
     Characterise the set of inner orientations obtainable as the outer
     strategies vary; prove a closure property of that set (for instance
     the one you extract from the mechanism in (ii)'s game); and decide
     whether the set can contain both s1 and s1(v xor e_2) for a single
     game together with the parity-driven outer rule of thm:blowup. A
     counterexample is a realisation of B^2 (the other side's result). A
     proof is the negative half of the pivot, but note carefully what it
     implies: "all-switches is subexponential on stopping SSGs" ALSO
     needs a height bound for every realisable orientation, not only the
     exclusion of one construction; say exactly what your lemma gives.
DELIVERABLES. Theorems with full proofs and explicit instances. Exhaustive
exact enumerations over normal forms with small fixed supports are
legitimate evidence and must be reported as measurements with the
parameter ranges. A theorem-strength gap is stated in one sentence. Labels
prefixed mono:.
`,
  },
  {
    key: 'degenerate',
    model: 'opus',
    title: 'Degenerate one-player games: ties as a resource, and a run longer than the Holt-Klee ceiling with one player',
    brief: `
YOUR ROUTE EXPLOITS THE CRACK ROUND 14 OPENED AND NOBODY HAS USED.
prop:oneplayer-lp bounds NONDEGENERATE one-player improvement orientations
by Holt-Klee, so with one player and no ties the all-switches run at
|Vmax| = 4 has length at most h*_HK(4) = 6 (verified) and at |Vmax| = 5 at
most 11 (measured). DEGENERATE one-player games are not bound by it:
thm:flat-resolution's resolution is a combinatorial completion, not an LP
orientation (rem:oneplayer-lp), and cor:ceiling-general bounds every run
only by h*(m) = 1,2,4,7,12. Read def:flat, lem:trichotomy, lem:flat-class,
lem:face-sink, thm:flat-resolution, cor:ceiling-general, cor:law-u,
rem:flat, prop:oneplayer-lp, rem:oneplayer-lp, prop:auso-seven,
cor:seven-two-player, thm:impedance and thm:ladder first. The round-14
allsw-degeneracy route's unintegrated items deg:prop-nondeg4 (a
nondegenerate 253-vertex realisation) and deg:prop-zeroties (damping cannot
remove ties at value 0) are in
${SCRATCH}/../../26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad/allsw-degeneracy/.

TASKS, in order.
 (1) THE FIRST TARGET IS CONCRETE: a ONE-PLAYER stopping SSG with |Vmax| = 4
     whose all-switches run from some start has length 7. Nondegenerate
     games cannot (h*_HK(4) = 6), so it must carry ties, and its flat
     resolution must be the height-7 orbit of G# (the unique AUSO class of
     height 7 at m = 4, prop:auso-census). Design it: a flat edge is a
     coordinate whose two ends have the SAME value vector (lem:trichotomy),
     i.e. a Max vertex whose two options have equal value at that
     strategy; ties at value 0 are cheap (deg:prop-zeroties: a Max vertex
     both of whose options are in the trap of the current strategy is
     tied at 0, and it becomes live only when something else opens).
     Work in the harmonic normal form with an explicit zero pattern, and
     verify from the game. If it does not exist, prove that: "every
     degenerate one-player run at m = 4 has length at most 6 because ...",
     with the exact mechanism (which flat classes can occur, and why their
     resolutions are still Holt-Klee).
 (2) THE TIMER. In a degenerate game a tied vertex does not switch; its tie
     is broken by a change elsewhere, and thm:impedance says the change a
     single switch causes at a distant vertex is (gap) x h(v -> u)/(1 -
     h(b -> u)), which can be exponentially SMALL or, through the escape
     denominator, LARGE. Design a vertex that stays tied (at 0, or at an
     exact equality maintained by symmetric chains) for exactly T rounds
     of an independent sub-run and then wakes: that is a timer, the
     component every published exponential family needs and that
     allswlower:cor-selfread showed a self-reading Max vertex cannot be
     in a nondegenerate game. Prove what you build (the phases as
     lemmas) and measure at five sizes.
 (3) A FAMILY. With a timer, build a one-player degenerate family whose
     run length grows superlinearly in |Vmax| at polynomial N -- already
     new for one player, since the best known lower bound for Howard's
     rule with two actions per state is linear (Mukherjee-Kalyanakrishnan,
     from memory) -- and push it as far as the timer allows. Report N,
     |Vmax|, a, the tie count along the run, the run length and the start
     for at least five sizes; state the growth law and prove it.
 (4) THE CEILING WITH TIES. For m <= 4, determine exactly which AUSO
     classes arise as flat resolutions of DEGENERATE one-player stopping
     games (h*_deg1(m)): is it all of h*(m) = 1,2,4,7, or does some law
     survive degeneracy? Exhaustion over small normal forms with a fixed
     zero pattern is the tool (${SCRATCH}/solo/ap_lp.py, nf2.py,
     realiseAP.py; ${SCRATCH}/solo/census/classes4.txt lists one
     representative per class with height and Holt-Klee flag).
REQUIREMENTS. Exact arithmetic; ties are exact equalities and must be
verified as such. All-switches with ties: a vertex switches iff STRICTLY
switchable (S_sigma), the paper's convention. Labels prefixed degen:.
`,
  },
  {
    key: 'lane-reuse',
    model: 'opus',
    title: 'Lane re-use with the correct rise accounting: a superlinear one-player all-switches family',
    brief: `
YOUR ROUTE REOPENS A CONSTRUCTION THAT WAS ABANDONED ON A FALSE
OBSTRUCTION. Read thm:ladder, rem:ladder, thm:impedance, lem:switch,
lem:monotone-law, thm:peak-law, cor:no-return, cor:law-b, cor:antichain,
cor:law-u, prop:closed-now-or-never, rem:closed-now-or-never,
prop:oneplayer-lp and rem:oneplayer-lp first, and read
${SCRATCH}/root16/r14routes/free-search-14/fs14.tex (fs14:lane, fs14:cycle,
fs14:howard) and ${SCRATCH}/root16/r14routes/allsw-lower/allswlower.tex
(lem-isolated, cor-selfread, the two re-running laws) IN FULL.

THE STARTING POINT. fs14:lane, Lane(k): Max vertices l_i -> (l_{i+1}, x_i),
l_{k+1} = t1, x_i a coin of value 1 - i 2^{-b}; from the all-exit start,
all-switches lasts exactly k rounds, switching l_k, ..., l_1 in that order,
N = O(k log k). The route then abandoned lane re-use because "val_sigma is
1-Lipschitz in a frozen payoff" would cap what a later switch can gain.
That bounds the GAP, not the RISE: thm:impedance says the rise of a switch
is (gap) x h(v -> u)/(1 - h(b -> u)), and the escape denominator 1 - h can
be 2^{-Theta(N)}, so a delayed switch CAN gain far more than its trigger
did. That is the reopening reason. The constraints you must respect are
the laws: cor:no-return (a set that switches alone is never returned to),
cor:law-u (the switched sets are pairwise distinct), cor:antichain, and
allswlower:lem-isolated (a recursive family cannot RESET a gadget; the
second run must be the first run TRANSLATED, and in every round of the
inner run some outer vertex switches too). Also: fs14:cycle covers only
INTRINSIC cycles, and the published counters' timing cycles are not
intrinsic (Fearnley's timing action is a self-loop escaping to a gadget,
not to a sink), so nothing forbids binarising a published counter; a
faithful binarisation of Fearnley's or Friedmann's one-player family at
polynomial size would settle the pivot outright and is worth a serious
attempt AFTER the lane family.

TASKS.
 (1) THE RE-ORDERED LANE. Take Lane(k) and add a trigger Max vertex whose
     switch changes the coin values x_i through a shared average part so
     that the lane's coins are RE-ORDERED, not reset (a reset is forbidden
     by lem-isolated). Compute the run exactly. Then nest: a trigger of
     triggers. The target is a one-player family on N = O(k log k) or
     O(k^2) vertices with all-switches length omega(N) -- superlinear is
     already new for one player, superpolynomial is the pivot.
 (2) THE RISE ACCOUNTING. For each vertex of your family, state its rise at
     each of its switches through thm:impedance's formula, and show where
     the escape denominator is used. A vertex switched twice must have a
     rise the second time; cor:no-return says its first switch set was
     never returned to -- reconcile the two explicitly.
 (3) HOLT-KLEE CHECK. If your family is nondegenerate, its orientation is
     Holt-Klee (prop:oneplayer-lp), so its BA height is at most h*_HK(m) =
     1,2,4,6,11 for m <= 5. Check the small members against that ceiling;
     a family exceeding it must be degenerate (then say so and count the
     ties) or you have an error.
 (4) THE BINARISATION. Write down the smallest published one-player family
     with superpolynomial Howard/all-switches behaviour that you know from
     memory (Fearnley 2010 for total reward; Christ-Yannakakis 2023 for
     reachability MDPs), state its action counts, and attempt a
     two-action binarisation at polynomial size respecting the laws. If it
     fails, give the obstruction as a lemma with an explicit instance.
REQUIREMENTS. Exact arithmetic; validate your all-switches loop on L_n
(exactly n rounds from the all-zero start) and on thm:all-switches-refuted's
seven-vertex game. Report N, |Vmax|, a, stopping, the number of tied
incidences along the run, the run length and the start, for at least FIVE
sizes; state the growth law and PROVE it (a lemma per phase). Every
probability other than 1/2 realised by average chains, size cost reported.
Labels prefixed lane:.
`,
  },
  {
    key: 'howard-cube',
    model: 'opus',
    title: 'Bottom-antipodal walks on LP orientations of cubes: Klee-Minty, deformed products, and one-player realisability',
    brief: `
YOUR ROUTE ISOLATES THE ONE-PLAYER HALF OF THE PIVOT AS A QUESTION ABOUT
POLYTOPES, and answers what can be answered by computation and by the
literature you know. prop:oneplayer-lp says: for a NONDEGENERATE one-player
stopping SSG, the improvement orientation s_G of the Max cube is the
orientation induced by the linear functional obj on the occupancy polytope
X(G) = {y >= 0 : sum_a y_{w,a} - sum_{v,a} p^{v,a}_w y_{v,a} = 1 for all w},
a simple m-polytope whose graph is the m-cube; all-switches is the
bottom-antipodal (BA) walk on that orientation; and by fs14:howard it is
literally Howard's policy iteration on a two-action transient MDP. Read
prop:oneplayer-lp, rem:oneplayer-lp, cor:seven-two-player, prop:auso-census,
prop:hstar-five, rem:hstar-five, thm:ladder, rem:ladder and
${SCRATCH}/root16/r14routes/allsw-lower/allswlower.tex (lem-lp, hk.py) first.

ALREADY DONE by the root agent -- do not redo, build on it. Klee-Minty
cubes have BA height exactly d for d <= 12 (${SCRATCH}/solo/km.py), so for
Klee-Minty question (1) is answered: LP-hard, BA-easy; do Goldfarb and the
Amenta-Ziegler deformed products only. The m = 4 one-player survey
(${SCRATCH}/solo/survey_*.json, realiseAP.py): all 56 Holt-Klee height-6
classes realised, every non-HK class failed, and FIVE Holt-Klee classes are
unresolved after 2 x 600 s (survey_h5HK_k0.json idx 26 and 40;
survey_h34HK_k0.json idx 10, 45, 49; their outmaps are in the json): finish
them with a longer budget, other denominators or a structured LP, or prove
one unrealisable -- a single Holt-Klee class with NO one-player realisation
would be a new necessary condition and is worth more than the other four.
B(2-cube) is Holt-Klee at dimension 4 and realised
(${SCRATCH}/solo/AP_m4_k0_den256_s200_game.json); B^2 = B(B(1-cube)) is not
Holt-Klee. In the blow-up rule family no HK-preserving rule doubles
(blowhk.py).

QUESTIONS, in order.
 (1) THE CLASSICAL DEFORMED CUBES. Compute EXACTLY the BA height of the
     improvement orientation of the Klee-Minty cube in dimensions 2..12
     (the LP orientation of the KM cube, sink = optimum, edge oriented
     towards the better objective), of Goldfarb's cubes, and of the deformed
     products of Amenta-Ziegler that you can write down; state each
     orientation as an outmap and verify it is an AUSO. Known long paths for
     simplex pivot rules live on these; the question is whether ANY known
     deformed cube has superlinear BA height. Report a table.
 (2) HOLT-KLEE AUSOs OF LARGE BA HEIGHT. Among AUSOs of the m-cube for
     m <= 5, determine h*_HK(m), the greatest BA height of a Holt-Klee AUSO
     (h*_HK(4) = 6 is verified by the root agent; h*_HK(5) = 11 is NOT:
     reproduce it with your own max-flow test on every face, validated on
     the 12 AUSOs of the 2-cube and on the 656 Holt-Klee AUSOs of the
     3-cube), and print a witness orientation for each m. Then
     ask which of those witnesses is an LP ORIENTATION OF A CUBE at all (Holt-
     Klee is necessary, not sufficient) -- attempt an exact realisation as a
     deformed cube (a polytope combinatorially a cube with a linear functional
     inducing s), and, sharper, as an OCCUPANCY POLYTOPE X(G) of a two-action
     transient MDP with DYADIC rows (which is what a one-player stopping SSG
     is, after lem:gadget). Give the realisability problem as an explicit
     system: for each sigma the sign pattern of val_{sigma[v]} - val_sigma over
     v, with val_sigma = (I - P_sigma)^{-1} q_sigma; this is polynomial in the
     rows, so it is a semialgebraic feasibility question, and for a FIXED
     support pattern of the rows it may collapse to something you can decide.
     Report h*_1(m) := the greatest BA height realised by a nondegenerate
     one-player stopping SSG: at m = 4 the survey gives 6 (certificates in
     ${SCRATCH}/solo/AP_m4_k0_*.json); extend to m = 5 -- is the h*_HK(5) = 11
     witness one-player realisable (realiseAP.py with m = 5, k = 0, a long
     budget)? And compute h*_HK(6) if you can: a census is infeasible at
     m = 6, but Holt-Klee is inherited by faces, so build from HK 5-faces.
 (3) THE BLOW-UP AND HOLT-KLEE. thm:blowup's B (dimension +2, height 2h+2)
     and prop:D-quadratic's D are in the paper and in ${SCRATCH}/solo/blowz.py,
     my_D.py. B(2-cube) is Holt-Klee; B^2 = B(B(1-cube)) and D from
     dimension 5 are not. Prove a lemma saying WHY (which face fails the
     disjoint-paths count, as a function of the seed and of z), and
     determine whether ANY dimension-raising operation that at least doubles
     height can preserve Holt-Klee -- blowhk.py found none in B's rule
     family, but products (lem:hstar-super), Klee-Minty-type deformations
     and operations raising the dimension by 3 or 4 were not tried. An
     HK-preserving doubling is the first candidate for an LP-realisable
     exponential family and should be pushed towards (2).
 (4) THE POSITIVE DIRECTION, stated honestly. Is the BA walk polynomial on
     LP orientations of combinatorial cubes? On occupancy polytopes of
     two-action transient MDPs? A proof would resolve the open question
     Melekopoglou-Condon left (Howard with two actions per state), so treat
     any proof you find with the deepest suspicion and audit it yourself
     against (1)-(3). If you can prove a weaker statement -- e.g. BA is
     polynomial on LP orientations of cubes that are PRODUCTS or of bounded
     "deformation depth", or the run is bounded by the number of distinct
     objective values on the walk with a geometric decay you can certify --
     state and prove exactly that.

REQUIREMENTS. Exact arithmetic (fractions) for every orientation and every
value; float only to explore. Your Holt-Klee test must be a genuine max-flow
with unit vertex capacities on EVERY face, validated on the paper's G#
orientation (3 paths on the 4-cube) and on the 12 AUSOs of the 2-cube (all
Holt-Klee). The census code is in ${SCRATCH}/root16/census/ and
${REPO}/scripts/ceiling/. Attribute everything you know from the literature
(Klee-Minty, Goldfarb, Amenta-Ziegler, Holt-Klee, Gaertner-Morris-Ruest,
Schurr-Szabo, Melekopoglou-Condon, Mukherjee-Kalyanakrishnan, Hansen-
Miltersen-Zwick). Labels prefixed hcube:.
`,
  },
  {
    key: 'sink-projection',
    model: 'opus',
    title: 'The two-player cube as a P-matrix LCP orientation, and the Max cube as its sink projection',
    brief: `
YOUR ROUTE SUPPLIES THE MISSING STRUCTURAL CONSTRAINT FOR TWO-PLAYER
REALISABILITY. prop:oneplayer-lp constrains nondegenerate ONE-player
orientations (Holt-Klee). For TWO players the paper has only prop:auso-size
(counting) and the single realised orbit prop:auso-seven. But a stopping SSG
with controlled set C = Vmax u Vmin is a P-matrix linear complementarity
problem (Stickney-Watson; Hansen & Ibsen-Jensen's reduction is cited in
rem:lcp and the round-14 lcp-handicap code under
${SCRATCH}/../../26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad/lcp-handicap/
builds M and q exactly), and a P-matrix LCP induces a UNIQUE SINK ORIENTATION
of the |C|-cube (Stickney-Watson) which, by Gaertner-Morris-Ruest, is
HOLT-KLEE. Read def:improvement-uso, prop:allsw-auso, thm:cyclic-uso (the
two-player cube can be CYCLIC), prop:auso-seven, cor:seven-two-player,
lem:trapchar and thm:eval-stopfree first.

ALREADY DONE for G# by the root agent: prop:gsharp-bigcube and
rem:gsharp-bigcube (${REPO}/scripts/blowup/bigcube.py) -- the 6-cube
orientation of G# is nondegenerate, USO, acyclic, Holt-Klee, of BA height 5,
and its sink projection is exactly s_{G#}. Start from that code and do the
GENERAL theory; the concrete instance your theory must be tested on is
B^2 = B(B(1-cube)) (5-cube, height 10, non-HK; outmap in the briefing above):
what is the least k for which B^2 can be the sink projection of a Holt-Klee
USO of the (5+k)-cube, and of one of the special P-LCP form SSGs produce?

TASKS.
 (1) THE BIG CUBE. Construct, from a stopping SSG, the P-matrix LCP (M, q)
     and its Stickney-Watson orientation s_C of the |C|-cube, in exact
     arithmetic; state the sign conventions so that a vertex of the cube is a
     profile (sigma, tau) and the outmap at (sigma, tau) is the set of
     controlled vertices at which the profile is not locally optimal for its
     owner under val_{sigma,tau}. Prove that this is a USO (cite
     Stickney-Watson, verify on 200 random stopping games including
     degenerate ones, and say what degeneracy does to it). G# is done (prop:gsharp-bigcube); verify instead on 200 random stopping
     games, and on the one-player games B1_game.json and
     AP_m4_k0_den256_s200_game.json in ${SCRATCH}/solo/ (one player: the big
     cube IS the Max cube and must be Holt-Klee).
 (2) THE PROJECTION. Define the SINK PROJECTION: for each Max strategy sigma
     take the unique sink of the face {sigma} x {0,1}^{Vmin} -- prove it is
     (sigma, tau_sigma) with tau_sigma a Min best response -- and read off
     the Max coordinates of s_C there. Prove this equals s_G of
     def:improvement-uso (the all-switches outmap) for nondegenerate games,
     and say exactly what it equals for degenerate ones (compare with
     thm:flat-resolution). This identifies the Max cube's orientation as the
     inherited orientation of a quotient, a standard USO construction; say
     whose.
 (3) WHAT PROJECTION PRESERVES. Holt-Klee is NOT preserved (G#: the 6-cube is
     HK by GMR, the 4-cube projection is not, cor:seven-two-player). Determine
     what IS: does the sink projection of a Holt-Klee USO of the (m+k)-cube
     satisfy any property beyond being a USO? Prove or refute by exhaustive
     enumeration at small (m, k): "every AUSO of the m-cube is the sink
     projection of some Holt-Klee AUSO of the (m+k)-cube with k <= m" -- if
     TRUE constructively, two-player realisability of ANY orientation reduces
     to P-LCP realisability of a Holt-Klee USO, and you should say what
     P-matrices SSGs give (their M has a specific sign/structure: describe it
     exactly, e.g. as I - (substochastic) with a block sign flip for Min) and
     whether THAT class is further constrained (hidden-K? sufficient?
     bounded handicap? -- rem:lcp says the handicap is 0 on every hard family
     here, which is itself a constraint you should turn into a theorem about
     which orientations arise when the handicap is 0).
 (4) THE CYCLIC CASE. thm:cyclic-uso exhibits a cyclic two-player cube whose
     Max projection (all-switches) is a walk on an AUSO by cor:ceiling-general.
     Show on that instance how the cycle disappears under projection, and
     state a lemma: the sink projection of any P-LCP USO of an SSG is acyclic
     (this should follow from lem:switch and cor:ceiling-general -- prove it
     cleanly from the big cube's structure, not by citation).

REQUIREMENTS. Exact arithmetic; validate the LCP against val by brute force
on 300 stopping games; validate the projection against the paper's printed
s_{G#} exactly. Every USO/HK/acyclicity claim verified by your own code on the
whole census where feasible (m + k <= 6). Attribute Stickney-Watson,
Gaertner-Morris-Ruest, Szabo-Welzl, Hansen & Ibsen-Jensen, Jurdzinski-Savani.
Labels prefixed sproj:.
`,
  },
  {
    key: 'rbr-rounds',
    model: 'opus',
    title: 'The round count of best-response restart and bidirectional improvement: geometric decay of the maximal gap, or a family that switches one vertex many times',
    brief: `
YOUR ROUTE ATTACKS THE ONE MECHANISM NO BARRIER COVERS. R_BR (prop:bsi-br)
is a switching rule in def:rule's sense -- polynomial per round, halts only
at an optimum -- that is NOT residue-blind (thm:normalform-barrier and
thm:window-barrier miss it) and NOT a scalar potential (thm:impedance,
cor:no-height miss it); BSI (def:bsi) has the strict lexicographic potential
(M, |Z|) of cor:bsi-levels. A polynomial round bound for EITHER is the
target; a superpolynomial family for BOTH closes the last uncovered
mechanism. Read def:bsi, thm:bsi-nostall, lem:bsi-pairloc, cor:bsi-levels,
prop:bsi-br, rem:bsi-br, prop:bsi-twice, prop:bsi-nonstopping, rem:bsi,
lem:max-deficit, thm:impedance and
${SCRATCH}/root16/r14routes/bsi-rounds/bsi_rounds.tex (lem-bias,
prop-selfdual, prop-switches / Q_16, the leapfrog analysis) first.

THE STRUCTURE OF THE QUESTION, made precise.
 - Along BSI, g = U - L is pointwise nonincreasing, M = max g is
   nonincreasing, and at every productive round some vertex of the argmax
   set Z is switched (lem:bsi-pairloc). The run length is at most |V| times
   the number of distinct values of M. M lives on the grid 4^{-a}, so the
   count of levels is at most 4^a, which is the trivial bound.
 - A POLYNOMIAL BOUND needs: M decays by a constant factor every poly(N)
   rounds, or the number of levels is polynomial for a structural reason.
 - A SUPERPOLYNOMIAL FAMILY needs: superpolynomially many levels, hence some
   vertex switched superpolynomially often (cor:bsi-levels), which needs a
   K-fold LEAPFROG at one vertex of the pairs (L(p), L(q)) and (U(p), U(q))
   driven by other vertices' switches. The best realised is K = 4 (Q_16,
   258 vertices after lem:gadget). Ladders are useless (lem-bias). A family
   for the self-dual one-sided rule MR (prop-selfdual) is a family for BSI.

TASKS.
 (1) THE RATE. For BSI and for R_BR separately, on a stopping game, prove or
     refute by an exact instance: "within each level the switched Z-vertex's
     gain is at least a constant fraction of M" and "M is halved every
     poly(N) rounds". Use lem:max-deficit's trap argument: at the moment a
     level ends, WHY did M drop, and by how much? Express the drop through
     thm:impedance (rise = gap x h/(1-h)) and find whether the escape
     denominator can make it 2^{-Theta(N)} of M. An instance where a level
     drops M by a 2^{-Theta(N)} fraction is the first step of a family;
     prove the drop is bounded below if you cannot find one.
 (2) THE LEAPFROG. Analyse Q_16 mechanically: which switches drive c_10's four
     reversals, and what are the four (L, U) pairs at c_10 at each reversal.
     Then COMPOSE: design a shared-feeder gadget in which a vertex's two
     options are fed by Min-dependent vertices (lem-bias says a bare avg/Max
     pair cannot do it), so that K reversals are driven at ADDITIVE cost per
     reversal. Target: a family with K = 6, 8, 10 reversals at one vertex and
     N = O(K) or O(K^2). If additive cost is impossible, prove it: a lemma of
     the form "each reversal at v needs a fresh vertex that switches alone,
     and such a vertex is spent (cor:no-return)".
 (3) R_BR SPECIFICALLY. R_BR resets tau to a best response every round, so
     U = val^tau is NOT monotone along its run and cor:bsi-levels does not
     apply. Find a potential for R_BR, or an instance where R_BR takes MORE
     rounds than all-switches from the same start (none is known: on every
     measured instance it is faster). Exhaust all starts on G#, the OSC
     instances (${SCRATCH}/root16/r14routes/bsi-rounds/osc.py) and Q_16.
 (4) THE SELF-DUAL RULE MR. On a self-dual stopping game (an involution phi
     swapping roles and sinks), BSI's Max track is the one-sided rule MR:
     switch v in S_sigma iff Min's best response at phi(v) prefers phi(q).
     This reads val_sigma only. Engineer a self-dual family on which MR
     switches some vertex many times; the design space is a half-game.

REQUIREMENTS. Exact arithmetic; val^tau by the dual game and lem:duality
(OFF the sinks only). Validate your BSI on the paper's numbers: L_n's disjoint
union with its dual, G# (BSI 5, strict 5, all-switches 7 from the start that
attains 7), R_BR on G# (4 rounds, c_1 twice). Report every family with N,
|Vmax|, |Vmin|, a, stopping, rounds, and the switch count at the most-switched
vertex, for at least four sizes. A "polynomial bound" that assumes an oracle
that is target-equivalent (rem:bsi: a guide U ordering Max's successors as w*
does) must be labelled as such. Labels prefixed rbr:.
`,
  },
  {
    key: 'treewidth',
    model: 'opus',
    title: 'Bounded width: a seventh polynomial class, or the exact place where interface tables explode',
    brief: `
YOUR ROUTE ASKS A STRUCTURAL QUESTION THE PAPER HAS NEVER ASKED: is
SSG-Value polynomial for SSGs whose underlying graph has bounded TREEWIDTH
(or pathwidth, or directed treewidth / DAG-width / Kelly-width), and if not,
exactly where does a dynamic programme over a decomposition explode? Every
polynomial class in the paper is a colour condition on cycles (thm:kacyclic),
a count (thm:few-avg, thm:few-escape, thm:bounded-components, a class keyed
to |C_j|), a rate (thm:escape-class) or the answer (thm:few-denominator).
None is a WIDTH condition, and the hard families here (L_n, H_m, WD, CC, TW,
G_m) are all of pathwidth at most 3 -- so a positive answer for bounded width
would put every hard instance in the document into a polynomial class, and
a negative one would need a new kind of instance. Read sec:special
(thm:kacyclic, thm:few-avg, thm:few-escape, thm:bounded-components,
thm:escape-class, thm:few-denominator, prop:k1-family, prop:escape-family,
prop:fv-family), sec:fold (thm:fold: freezing one vertex at payoff theta
gives a response map with EXACTLY 2^D pieces -- this is the obstruction a
table-based DP must beat), thm:vi-lower and lem:gen-comparison first.

TASKS.
 (1) THE DP. Fix a tree decomposition of width k. For a bag X, the subgame
     below X interacts with the rest only through the values on X; the
     natural table is the RESPONSE FUNCTION R_X: [0,1]^{|X|} -> [0,1]^{|X|}
     giving the values of the boundary vertices as a function of the payoffs
     assigned to the boundary's outside successors (lem:gen-comparison
     allows arbitrary sink payoffs). Prove R_X is monotone, piecewise linear
     (rational) and 1-Lipschitz in the sup norm on stopping subgames, and
     determine its number of pieces: thm:fold says 2^D for ONE frozen vertex
     on the family P_D, so the tables are exponential in general. Then
     identify what ELSE must be bounded for the DP to be polynomial: the
     number of pieces of R_X is a function of the subgame; give it a name,
     bound it by a structural parameter (e.g. the number of average vertices
     below X, the alphabet size k of thm:alphabet-rigid, the escape exponent)
     and state the resulting class as a theorem with an explicit family INSIDE
     it and OUTSIDE all six existing classes (check membership on the subgame
     reachable from the start). "Bounded treewidth AND bounded pieces" is
     acceptable if the pieces bound is checkable in polynomial time.
 (2) PATHWIDTH 2 EXACTLY. Since the ladder L_n and H_m have pathwidth <= 3
     and are solved in linear time by back-substitution, ask whether
     pathwidth <= 2 (or bandwidth <= c) forces polynomial time by a sweep,
     with the tables kept as EXACT piecewise-linear functions of ONE variable
     (a path decomposition has two-sided interfaces). Prove it or exhibit a
     pathwidth-2 stopping family on which the one-variable response function
     has 2^{Omega(N)} breakpoints (thm:fold's P_D may already be it -- check
     its pathwidth).
 (3) THE LITERATURE. From your own knowledge: Obdrzalek (parity games of
     bounded treewidth in P), Chatterjee-Ibsen-Jensen-Pavlogiannis and
     related work on MDPs/games of bounded treewidth, Auger-Coucheney-
     Strozecki (FPT in the feedback vertex number, prior art number 1 here).
     State precisely what is known for SSG VALUES (as opposed to qualitative
     objectives), and attribute. If a polynomial algorithm for bounded
     treewidth SSGs is KNOWN, say so, reproduce its argument, and verify it.
 (4) ONE-COLOUR FEEDBACK. A cheap generalisation of thm:kacyclic that the
     paper may lack: if a set F of Min vertices meets every cycle that
     contains a Min vertex, then enumerating Min's 2^{|F|} choices on F and
     retyping F as one-successor vertices leaves a game in which Min lies on
     no cycle, which thm:kacyclic solves; so poly(N) 2^{f_min} where f_min is
     the Min-feedback number, and symmetrically for Max. State it, prove it
     in three lines, note it is incomparable with Auger et al.'s feedback
     vertex number, and give a family inside it and outside the six classes.
     grep the paper first: if it is already there, say where and skip.

REQUIREMENTS. Exact arithmetic; the DP validated against brute-force values
on 300 stopping games of treewidth <= 3 (build them from a random tree
decomposition, not by hoping); breakpoint counts computed exactly, not
estimated. Labels prefixed tw:.
`,
  },
  {
    key: 'free-search-15',
    model: 'opus',
    title: 'Free search: a formulation nobody here has tried, tested against the whole frontier',
    brief: `
YOUR ROUTE IS FREE, WITH ONE RULE: whatever you propose must be checked
against the paper BEFORE you develop it. Fourteen rounds have tried, and
frontier.tex records the outcome of: strategy improvement in every switching
rule named above, random facet, Tarski/quasi-polynomial lattices, pinning and
violator dimension, LCP conditions (P, hidden-K, handicap), Lasserre/SOS,
homotopy and breakpoints, tropical/Puiseux, order/permutation space and its
bubble step (FALSE), simulation preorders, slack/ratio/Mobius calculi,
transport LPs and the hybrid, seeded brackets, Newton and Newton-Dinkelbach,
softmax/entropic regularisation, universal lattices, UEOPL, Schur/vertex
elimination, coin-bias algebra, preconditioning by change of measure, value
alphabets, bidirectional improvement. Do NOT propose any of these. Before you
commit to an idea, grep the paper for it and write one sentence saying why it
is not already there.

SEEDS, none mandatory, each chosen because it is falsifiable in a day.
 (A) THE TOP AVERAGE VERTEX. Let nu = max_{c in Vavg} val(c) on a stopping
     game with Vavg nonempty and nu < 1. Prove first that every value is
     either 1 or at most nu (a controlled vertex of value in (nu, 1) would
     lie in a Min-closed set of controlled vertices that never meets an
     average vertex, contradicting stopping) -- so nu is the second-largest
     letter of the alphabet. QUESTION: is TOP, "output an average vertex of
     maximum value", polynomial-time computable, or target-equivalent?
     prop:no-halving makes COMPARING two average vertices target-equivalent,
     but TOP is a different problem. Either give a reduction from
     SSG-Compare to TOP (then say so and stop), or an algorithm for TOP, or a
     precise statement of what TOP as an oracle would buy (a peeling
     recursion through thm:order-determines?).
 (B) NON-ADAPTIVE COMPARISONS AS A SELF-REDUCTION. thm:compare-equivalence:
     n non-adaptive comparisons determine sigma*. Each is an instance of the
     same problem on a game of size O(N). Is there a self-reduction in which
     the instances are SMALLER in some measure (fewer average vertices on
     cycles with both players; smaller alphabet; smaller escape exponent)?
     prop:no-halving forbids halving a; find what it does NOT forbid and
     test whether that measure can be reduced by a constant per round.
 (C) THE VALUE AS A RATIO OF FOREST COUNTS. Under a fixed absorbing profile,
     val = N_1/D with D the number of acyclic routings (all-minors
     matrix-tree; the project verified this on 4401 profiles but never used
     it). The decision val(v0) >= 1/2 under the OPTIMAL profile is a
     max-min over profiles of a ratio of two determinants of the same
     matrix family. Is there a combinatorial structure (a matroid, a lattice
     of routings, an exchange property between profiles) that makes the
     max-min tractable, or a proved reason there is not (e.g. the ratio is
     not monotone in any exchange)?
 (D) SOMETHING OF YOUR OWN, from the literature you know that this project
     has not cited: name the source, state what it gives for SSGs exactly,
     and test it on the paper's hard instances (G8, H_m, WD, CC, TW, G#, Q_16,
     the wedge, prop:own-stall's R -- all in ${SCRATCH}/root16/myinst.py,
     wd.py, cc.py, gstar.py, seven.tex, r14routes/).

REQUIREMENTS. Exact arithmetic. A route that ends at a target-equivalent
statement must SAY SO (thm:compare-equivalence, thm:decide-one-bit,
prop:no-halving, cor:wrong-equivalence, rem:transport-objective, rem:bsi,
rem:alphabet-equivalence are the known ones). Everything measured must be
measured on instances that VARY the parameter your idea turns on. Labels
prefixed fs15:.
`,
  },
  {
    key: 'verify-r14',
    model: 'opus',
    title: 'Independent verification and paste-ready LaTeX for the round-14 results still outside the paper',
    brief: `
YOUR ROUTE IS A VERIFICATION ROUTE. Round 14 produced results that its own
auditors confirmed but that the root agent has NOT verified and has NOT
integrated. The project rule is that nothing enters frontier.tex until it has
been re-derived, in exact arithmetic, from the STATEMENT and not from the
route's code. Do that, one item at a time, and for each item return: the
exact statement, your independent verification (your own code, in
${SCRATCH}/verify-r14/), a proof written out in full where the item is a
theorem, the paste-ready LaTeX in the paper's amsthm style with the paper's
own labels cited, and a one-line verdict INTEGRATE / REPAIR / EXCLUDE with the
reason. Sources: ${SCRATCH}/root16/r14routes/allsw-lower/allswlower.tex,
${SCRATCH}/root16/r14routes/bsi-rounds/bsi_rounds.tex, the round-14
allsw-degeneracy and lasserre-2 directories under
${SCRATCH}/../../26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad/, and the
precondition directory under
${SCRATCH}/../../ef1cfad9-5d31-414e-ba8d-8fdf97a6d2ab/scratchpad/.

THE ITEMS.
 (1) allswlower:lem-isolated and allswlower:cor-selfread (the two re-running
     laws; check that lem-isolated is not already cor:no-return restated --
     if it is a two-line corollary, say so and draft it as a corollary), . The operation D of allswlower:prop-search(a) is INTEGRATED as
     prop:D-quadratic and verified by the root agent -- skip it.
 (2) From allsw-degeneracy: deg:prop-g (law ceiling 1,2,4,7,12 with cor:law-u
     added), deg:prop-g6 (21 at m = 6 -- reproduce or bound what you can in
     the time), deg:prop-hk5 (h*_HK(5) = 11), deg:lem-super is INTEGRATED as lem:hstar-super with the root agent's
     own construction and proof -- skip it; deg:prop-nondeg4 (a nondegenerate 253-vertex realisation
     of the flat-resolution AUSO B' with the same run), deg:prop-zeroties
     (damping cannot remove ties at value 0 -- prove it from lem:trichotomy
     or refute).
 (3) From lasserre-2: las2:thm-two (the degree-two lift is exact iff |C| <= 2
     -- check BOTH directions; the paper's thm:lasserre-vacuous has |C| = 3
     witnesses, so the "if" direction is what needs a proof), las2:thm-cyc
     and its spectral criterion, las2:prop-rlt, las2:prop-cyc-rlt.
 (4) From bsi-rounds: bsr:lem-bias (same-successor bias), bsr:prop-selfdual
     (BSI on self-dual games is the one-sided rule MR), bsr:prop-switches
     (Q_16: rebuild from four_switch_rows.json, realise by lem:gadget
     yourself, run non-strict BSI from the printed start, confirm c_10 is
     switched four times and the realised SSG's run coincides), bsr:prop-
     normal (normalisation preserves val^tau, hence the BSI trajectory).
 (5) From precondition: cor:prec-characterisation (the escape class is
     exactly {1 - Lambda >= 1/poly} with Lambda = max_pi rho(M_pi), to be
     attributed to Blondel-Nesterov), thm:prec-contract-class (the
     "contracted" class -- needs the precision repair its audit demanded:
     state it), prop:prec-wedge. prop:prec-Gm(b) is REFUTED; do not include.
 (6) thm:few-denominator has no "no member is a stall" bound, unlike every
     other class (rem:escape-class has one). Determine whether a member of
     the few-denominator class can be a stall for M1, M2, M2T, M4, M5 --
     FV_2(n) is the family to test -- and draft the sentence.

REQUIREMENTS. Each verification must be from the statement; if you must read
the route's code, say what you read. Report every discrepancy with the
route's numbers explicitly. Where a proof in the source is a sketch, write the
full proof or mark GAP. Labels keep their route prefixes. Order the items by
value: (4) Q_16 and (2) deg:prop-hk5 / deg:prop-nondeg4 / deg:prop-zeroties
first, then (1), (3), (5), (6).
`,
  },
]

const PAPER_SECTIONS = [
  { key: 'classes', lines: '1124-2684', what: 'sec:special: lem:descent, thm:few-avg, rem:few-avg-tight, def:escape, lem:descent-refined, lem:certificate, thm:few-escape, prop:fk-family, def:survival, lem:survival, thm:escape-class, def:survival-rate, lem:escape-rate, prop:escape-family, rem:escape-class, def:jump, lem:jump-acyclic, lem:det-game, thm:avg-acyclic, thm:player-free, thm:one-player, def:payoff, lem:successor-closed, lem:cut, lem:residual, thm:kacyclic, prop:kacyclic-strict, rem:owner-blind; sec:alphabet: def:alphabet, thm:alphabet-iteration, rem:alphabet-down, cor:grid-iteration, lem:alphabet-cover, thm:alphabet-rigid, cor:alphabet-chain, thm:alphabet-denominator, thm:few-denominator, rem:alphabet-compare, prop:alphabet-four, prop:fv-family, rem:alphabet-equivalence' },
  { key: 'allswitches', lines: '3206-4564', what: 'sec:allsw-laws: lem:monotone-law, rem:monotone-law-general, prop:closed-now-or-never, thm:peak-law, cor:no-return, cor:law-b, cor:antichain, def:maxreach, thm:component-bound, thm:bounded-components, prop:k1-family, prop:overshoot-small; the AUSO identification: def:improvement-uso, prop:allsw-auso, lem:auso-laws, def:flat, lem:trichotomy, lem:flat-class, lem:face-sink, thm:flat-resolution, cor:ceiling-general, cor:law-u, rem:flat, cor:f-auso, rem:f-auso, prop:auso-size, prop:auso-seven and its printed normal form, prop:oneplayer-lp, cor:seven-two-player, prop:gsharp-bigcube, prop:auso-census, prop:hstar-five; and the NEVER-AUDITED solo-round material lem:hstar-super, prop:D-quadratic, thm:blowup (reconstruct its proof in full: the unique-sink case analysis, the acyclicity argument with the parity conflicts of outer cycles, the walk of length 2h+2, and the numerical bounds), rem:blowup-measured and rem:blowup-realise -- recompute the heights 4,10,22,46,94 / 2,6,14,30 / 7,16,34,70 / 12,26,54,110 with your own code, the Holt-Klee status of B(1-cube) and of B^2, the 58-vertex realisation (verify it FROM THE GAME), and check the claim that the translation vector is a single coordinate, the alpha introduced two dimensions earlier, against the definition z = o xor u -- which coordinate is it at the second level when the seed height is odd? Also check whether rem:blowup-realise is consistent with the fact, found after it was written, that B(2-cube) is Holt-Klee and realised by a one-player game' },
  { key: 'refutations', lines: '4564-6430', what: 'def:ladder, thm:ladder, rem:ladder, thm:switch-count, cor:no-height, prop:serialiser; sec:residue (lem:trapchar, def:residue, thm:residue-correct, prop:residue-ladder, lem:normalform, thm:normalform-barrier, lem:splice, prop:a-presentation, def:freeze, prop:freeze-sound, prop:freeze-escapes, def:kblind, lem:kblind, def:window, thm:window-barrier); def:bsi through rem:bsi (thm:bsi-nostall, lem:bsi-pairloc, cor:bsi-levels, prop:bsi-twice, rem:bsi-gap, prop:bsi-oneplayer, cor:bsi-correct, prop:bsi-br, rem:bsi-br, prop:bsi-nonstopping); thm:cyclic-uso, cor:no-potential, thm:vi-lower, thm:hamming-refuted, cor:hamming, prop:rules-fail, prop:needle, lem:readonce, prop:no-submodular' },
  { key: 'calculi', lines: '7185-8714', what: 'sec:gap (def:rule, def:missing, thm:gap-equivalence, def:decision-rule, thm:decide-one-bit, prop:locality, prop:pdc-separation), sec:simorder (def:simorder, thm:simorder-sound, prop:simorder-stalls), sec:slack (def:slack, thm:slack-sound, prop:slack-repairs, thm:slack-barrier, cor:slack-stalls, thm:slack-vi-upper, def:trans-slack, thm:trans-sound, prop:trans-Hm, thm:trans-complete, lem:phi-certificate, prop:trans-stall, def:separable, lem:separable-lower, thm:separable, cor:separable, cor:set-certificate), sec:ratio (def:homog, prop:cw, def:ratio, thm:ratio-sound, thm:ratio-sandwich, cor:ratio-complete, cor:ratio-stall, prop:ratio-incomparable, def:mobius, prop:mobius, prop:ratio-closure)' },
  { key: 'hybrid', lines: '8714-10635', what: 'sec:matching-barrier (def:lmc, lem:fooling-partner, thm:matching-barrier), sec:seeded (def:seeded, thm:seeded-sound, thm:seeded-barrier, thm:seed-dichotomy, prop:seeded-decides), sec:transport (def:transport, thm:transport-sound, lem:transport-exact, prop:transport-decides, lem:transport-dim, thm:transport-objective, def:lasserre-two, thm:lasserre-vacuous, rem:lcp, prop:transport-stalls, rem:own-successor, prop:own-stall, thm:transport-barrier), sec:fold (thm:fold), sec:hybrid (def:hybrid, thm:hybrid-sound, lem:hybrid-fix, lem:gen-comparison, thm:hybrid-complete, cor:hybrid-sink, prop:hybrid-decides, prop:hybrid-onectrl, prop:hybrid-rate, lem:hybrid-cutting, thm:hybrid-convex-barrier, thm:hybrid-lower), sec:wedge (lem:wedge-face, cor:wedge-cert, def:wedge, prop:wedge, def:wedge-chain, lem:wedge-verts, thm:wedge-proved, cor:wedge-count, rem:wedge)' },
  { key: 'summary', lines: '10635-10856 together with 1-343', what: 'sec:summary and the front matter READ AGAINST THE BODY: every claim in the abstract, the introduction, "what is proved and what is not" and the summary must match the statement it cites, with the same hypotheses, the same numbers (vertex counts, round counts, the lists of six classes and six mechanisms, the count of prior-art attributions, the statement that thm:determinacy is the ONLY external input and that the Schurr-Szabo import is gone) and the same strength (measured vs proved); list every mismatch. Also check whether the abstract, the introduction and the summary say what the body now justifies about thm:blowup, lem:hstar-super, prop:gsharp-bigcube and the realised first level, and flag what they omit or overstate' },
]

const paperAuditPrompt = (s) => `
You are an ADVERSARIAL AUDITOR of a mathematical manuscript. Your job is to
BREAK the part of ${REPO}/frontier.tex assigned to you, not to appreciate it.
The manuscript's own standard is: every claim proved from first principles,
every negative claim witnessed by an explicit instance verified in exact
rational arithmetic, every rediscovery attributed. Hold it to that standard.

${COMMON}

# Your assignment

Lines ${s.lines} of ${REPO}/frontier.tex: ${s.what}. Read those lines in
full (sed -n), and read any result they cite from elsewhere in the file when
you need its exact statement (grep -n 'label{NAME}' then sed).

# Your task

1. PROOFS. For every theorem, lemma, proposition and corollary in your range,
   reconstruct the proof step by step. Report every step that is asserted
   rather than proved, every hypothesis used but not stated (stopping?
   nondegeneracy? sink payoffs pinned? Min present?), every citation of
   another label whose statement does not actually give what is used, and
   every quantifier error. Sinks, ties, empty sets and the one-vertex game
   are where this manuscript's errors have lived: check them.
2. NUMBERS. For every explicit instance, table, count or vertex count in
   your range that can be recomputed in under an hour, RECOMPUTE IT in exact
   rational arithmetic with your own code in ${SCRATCH}/paper-audit-${s.key}/
   (the harness is at ${SCRATCH}/root16/: mycore.py, myinst.py, wd.py, cc.py,
   gstar.py, seven.tex/t_seven.py, auso.py, census/). Report every mismatch
   with both numbers. Do not skip the small ones; a wrong count is a defect.
3. CONSISTENCY. Every \\Cref in your range must point at a result that says
   what the text claims it says. Every remark that qualifies a result
   ("measured, not proved", "one direction only", "off the sinks") must be
   consistent with the result's statement and with the abstract/summary.
   Every "we verified on K instances" must say what was varied.
4. PRIOR ART. Anything in your range that is standard published mathematics
   presented as new is a defect; fifteen such cases have been caught. Name
   the source if you know it. A rediscovery already labelled as one is fine.
5. OVERSTATEMENT. Where the text claims more significance than the
   mathematics supports (a "barrier" covering no real rule, a "class" that
   is a restatement, a "family" measured at two sizes), say so.

Report findings with severity fatal / major / minor / note, each with the
LINE NUMBER, the label, the defect in one sentence and the evidence (your
recomputation, the counterexample, or the exact quote that is wrong). "sound"
is TRUE only if nothing fatal or major survives. Being unable to find a defect
in a result you did not check is not grounds for sound = true; list what you
checked and what you did not. Put target = 'frontier.tex ${s.key} (lines
${s.lines})'.
`

const AUDIT_LENSES = [
  {
    key: 'correctness',
    prompt: (r, res) => `
You are an ADVERSARIAL AUDITOR. Your job is to BREAK the work below, not to
appreciate it. Assume every claim is wrong until you have checked it yourself.

${COMMON}

# The work under audit (route "${r.key}": ${r.title})

${res}

# Your task: CORRECTNESS

1. For EVERY result marked "proved", reconstruct the argument. Find the step
   that is asserted rather than proved. State it as a one-sentence GAP.
2. For EVERY numerical or computational claim, REBUILD THE COMPUTATION YOURSELF
   in exact rational arithmetic, from the STATEMENT and not from the route's
   code, in your own directory under ${SCRATCH}/audit-${r.key}-correctness/.
   The harness is at ${SCRATCH}/root16/. If a claimed family or instance does
   not reproduce, that is a FATAL finding and you must give the discrepancy
   explicitly. If the route claims a run-length table (all-switches, BSI,
   breakpoints, rounds), recompute at least three of its rows independently.
3. Hunt for the project's standing errors: computing val_sigma by greedy policy
   iteration in a non-stopping game; dict-literal rows collapsing when a
   vertex's two successors coincide; fresh vertices colliding with the sink
   indices; excluding t0 from the trap Z_sigma; using the PAIR test instead of
   the own-successor test of rem:own-successor; omitting the Z_0/Z_1 seed;
   measuring a mechanism only on instances where the parameter it turns on is
   constant; separating a family from a class using vertices UNREACHABLE from
   the start; unpinned sink payoffs in an iteration bound; counting a
   non-productive terminal round; a "polynomial class" whose member is already
   inside thm:few-avg, thm:few-escape, thm:kacyclic, thm:bounded-components,
   thm:escape-class or thm:few-denominator.
4. Check every claimed IMPLICATION between the route's own results, and every
   citation of frontier.tex, against the actual text of the label cited.
5. If the route claims a decision rule, a barrier, a lower bound or a
   polynomial algorithm, check it against THE STANDING RULE and against the
   proved equivalences: does any step assume an oracle that is
   target-equivalent (thm:compare-equivalence, thm:decide-one-bit,
   prop:no-halving, cor:wrong-equivalence, rem:transport-objective, rem:bsi)?

Report findings with severity fatal / major / minor / note. "sound" is TRUE only
if nothing fatal or major survives your checking. Being unable to find a defect
in a result you did not check is not grounds for sound = true; say what you
checked.
`,
  },
  {
    key: 'significance',
    prompt: (r, res) => `
You are an ADVERSARIAL AUDITOR. Your job is not to check arithmetic but to
decide whether this work MEANS anything, and to say so bluntly.

${COMMON}

# The work under audit (route "${r.key}": ${r.title})

${res}

# Your task: SIGNIFICANCE AND NOVELTY

1. IS IT NEW? For each result, grep ${REPO}/frontier.tex and check whether it is
   already there under another name or is an immediate corollary of something
   there. This project has repeatedly caught routes restating thm:ladder,
   thm:short-path, lem:cut, lem:duality or thm:seed-dichotomy as new. Name
   the label if so. Also flag anything that is standard published mathematics
   presented without acknowledgement -- fifteen such cases have already been
   caught here (see the prior-art list above). A rediscovery that the route
   itself labels and attributes is NOT a defect; an unlabelled one is.
2. IS IT CIRCULAR OR VACUOUS?
   - Does a claimed algorithm assume an oracle that is target-equivalent? The
     proved equivalences are thm:compare-equivalence, thm:decide-one-bit,
     prop:no-halving, cor:wrong-equivalence, rem:transport-objective and
     rem:bsi.
   - Does a claimed BARRIER rule anything out, or is its hypothesis so strong
     that no real algorithm satisfies it? Name which of M1, M2, M2T, M3, M4,
     M5, M6 and def:bsi it actually covers. A barrier covering none of them is
     nearly worthless and must be labelled as such.
   - Is a claimed polynomial CLASS nonempty and not already inside thm:few-avg,
     thm:few-escape, thm:kacyclic, thm:bounded-components, thm:escape-class
     or thm:few-denominator? Demand an explicit member outside all six, verified on the subgame
     reachable from the start vertex.
   - Is a claimed lower-bound FAMILY genuinely a family (a build(n) with a
     proved or at least measured growth law at >= 4 sizes), stopping, and
     legitimate in the sense of def:ssg (fair coins, out-degree two)?
3. IS THE VERIFICATION HONEST? Random sampling has never found a hard instance
   in this project. If a claim rests on "no counterexample in K random
   samples", the claim is UNSUPPORTED. Check that the sampled instances
   satisfied the hypothesis at all, and that the instance set VARIES the
   parameter the mechanism turns on.
4. WHAT IS THE ROUTE'S REAL REMAINING GAP, in one sentence, stated more
   precisely than the route states it? If the route's gap is softer than the
   truth, give the true one.
5. Would integrating this into frontier.tex make the paper better or worse?
   Answer directly, and say WHICH results (by name) are worth integrating and
   which are not. "Worse" is a legitimate and useful verdict.
`,
  },
]

log(`Round 15 (re-run): ${ROUTES.length} routes, all on Opus 5: ${ROUTES.map(r => r.key).join(', ')}; two audits each on Opus 5; ${PAPER_SECTIONS.length} paper audits on Opus 5.`)

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\n\n# YOUR ROUTE: ${r.title}\n${r.brief}\n\n` +
    `Work in ${SCRATCH}/${r.key}/ (create it). Copy the harness from ` +
    `${SCRATCH}/root16/ into your own directory before using it. You have a ` +
    `long budget: think hard, write code, verify, iterate. Your final output ` +
    `is the structured object and it is the ONLY thing that reaches the root ` +
    `agent -- make it complete and self-contained, and put the path of your ` +
    `code directory in code_dir.`,
    { label: `route:${r.key}`, phase: 'Routes', schema: ROUTE_SCHEMA, model: r.model }
  ),
  (res, r) => {
    if (!res) return null
    const text = JSON.stringify(res, null, 1).slice(0, 60000)
    return parallel(AUDIT_LENSES.map((L) => () =>
      agent(L.prompt(r, text), { label: `audit:${r.key}:${L.key}`, phase: 'Audit', schema: AUDIT_SCHEMA, model: 'opus' })
    )).then((audits) => ({ route: r.key, model: r.model, result: res, audits: audits.filter(Boolean) }))
  }
)

const paperWork = parallel(PAPER_SECTIONS.map((s) => () =>
  agent(paperAuditPrompt(s), { label: `paper:${s.key}`, phase: 'Paper audit', schema: AUDIT_SCHEMA, model: 'opus' })
    .then((a) => (a ? { section: s.key, lines: s.lines, audit: a } : null))
))

const [results, paper] = await Promise.all([routeWork, paperWork])

const good = results.filter(Boolean)
const paperGood = paper.filter(Boolean)
log(`Round 15 complete: ${good.length}/${ROUTES.length} routes returned; ${paperGood.length}/${PAPER_SECTIONS.length} paper audits returned.`)
return { round: 15, routes: good, paper: paperGood }
