export const meta = {
  name: 'ssg-round16',
  description: 'Round 16 on the SSG value problem: 10 routes on Opus 5 against the post-round-15 frontier (176 pp), each adversarially audited twice on Opus 5, plus seven adversarial audits of the round-15-integrated parts of frontier.tex on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
    { title: 'Paper audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/d1fe2115-9b72-4784-bb94-87421ac1106c/scratchpad'
const PREV = '/tmp/claude-1000/-data-ssg-proof/6e64b33d-520c-4c82-aa1b-ffb69ecfcb61/scratchpad'
const P14 = '/tmp/claude-1000/-data-ssg-proof/26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad'
const P13 = '/tmp/claude-1000/-data-ssg-proof/dc099d6a-f89a-421b-bbe2-2a87a9e19322/scratchpad'

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

Notation: N = |V|, a = |Vavg|, C = Vmax u Vmin, m or n = |Vmax|, k = |Vmin|.
w* = val, the value vector. T = the Shapley operator. T_sigma = T with Max
frozen to sigma; val_sigma = the value when Max plays sigma and Min plays
optimally; val^tau = the value when Min plays tau and Max plays optimally.
STOPPING means that under every positional pair the token reaches a sink with
probability 1. S_sigma = {v in Vmax : val_sigma(sigma-bar(v)) >
val_sigma(sigma(v))}, the strictly switchable set. ALL-SWITCHES:
sigma -> sigma[S_sigma]. A RUN is the sequence of strategies all-switches
produces; its LENGTH is the number of productive rounds.

# The standing repository

${REPO}/frontier.tex is a 176-page LaTeX development of about 400 numbered
results (13710 lines, 740 KB) built over fifteen multi-agent rounds and one
solo round by the root agent. Every claim in it is proved and every negative
claim carries an explicit instance verified in exact rational arithmetic. It
contains NO polynomial-time algorithm for the general problem and claims
none. Read the parts you need with grep/sed; do NOT read the whole file.
\`grep -n 'label{' ${REPO}/frontier.tex\` lists every result; sections:
sec:operators (l.392), sec:stopping (706), sec:transform (942), sec:special
(1223; sec:alphabet 2367, sec:width 2874), sec:structure (3190),
sec:refutations (3674; sec:allsw-laws 3749, the AUSO identification and the
blow-up 4564-5617, sec:ties 5617, sec:deformed 6045, sec:readouts 6332,
sec:projection 6537, the ladder 6759, the residue and the BSI material
7036-8450, the two-player cube 8514, value iteration 8618), sec:selection
(9040), sec:randomfacet (9496), sec:gap (9852; sec:simorder 10175,
sec:slack 10359, sec:ratio 11001, sec:matching-barrier 11444, sec:seeded
11582, the transport programme 11771, sec:fold 12344, sec:hybrid 12442,
sec:wedge 13112), sec:summary (13432).

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
without that seed were all artefacts; the seed cracked every one. A stall at
a vertex whose two successors have EQUAL value is VACUOUS (prop:fv-stall):
a sound rule is licensed to abstain there. Only a stall at a
VALUE-DISTINGUISHING vertex (successors of different value) counts.

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
exactly beta = 2^{-m} is realised by a chain of m average vertices);
lem:dyadic-row (round 15, l.980: an ARBITRARY substochastic dyadic row of
denominator 2^D over a target set is realised by a chain of at most D
average vertices per row -- use it, do not re-derive it); lem:duality (the
dual game G-bar, sinks and roles swapped, has val = 1 - val OFF THE SINKS
only).

POLYNOMIAL CLASSES (EIGHT). thm:few-avg (poly(N)2^a, arbitrary SSGs);
thm:few-denominator (sec:alphabet: stopping games whose values share a common
denominator D are solved in O(N^2 D^2) with no advance knowledge of D, by the
UP-rounded Shapley iteration on the grid, which is exact on ANY finite grid
containing the values -- thm:alphabet-iteration; the value alphabet
Lambda(G) := {0,1} u {val(v) : v reachable} with k letters is rigid,
D <= 2^{k-2} sharply, thm:alphabet-rigid / thm:alphabet-denominator;
prop:fv-family gives FV_2(n) inside this class and outside the other five
combinatorial ones; rem:alphabet-equivalence: a poly-size SUPERSET of the
alphabet is target-equivalent); thm:few-escape (escape exponent d(G) <= a,
separated from a by Theta(N) on prop:fk-family); thm:kacyclic (ONE COLOUR off
the cycles suffices; contains thm:avg-acyclic, thm:player-free,
thm:one-player); thm:bounded-components (all-switches halts within
sum_j (2^{|C_j|}-1) over SCCs of the Max-reachability digraph);
thm:escape-class (def:survival is the SURVIVAL OPERATOR S -- max at EVERY
controlled vertex, mean at average vertices, sinks read as 0; an escape
certificate (lambda, x) has x >= 1 and Sx <= lambda x; then two-sided value
iteration closes in O((a + log kappa)/log(1/lambda)) rounds; its existence for
fixed lambda is one LP; rem:escape-class: NO member of the escape class is a
stall for M1, M2, M2T or M5, so the class cannot reach the frontier);
thm:modulator (round 15, sec:width: N^{O(mu)} for the freezing-modulator
number mu into any freezing-closed polynomial class -- the k-acyclic games,
the acyclic games, games with a <= a_0, the classes of thm:bounded-components
and the escape class are freezing-closed; thm:few-denominator is NOT;
prop:modulator-family M_n is in this class and outside the six others);
thm:qp (round 15: stopping games of treewidth k are solved EXACTLY in
N^{O(k log N)} by the Etessami-Papadimitriou-Rubinstein-Yannakakis Tarski
fixed-point search on lem:cut's cut map at balanced separators
(thm:tarski, lem:cut-sign: the cut map is monotone and sign-definite;
lem:round-recover: Legendre's convergent recovers exact values from
approximations; lem:payoff-transfer) -- QUASIPOLYNOMIAL, NOT POLYNOMIAL:
each of the O(B^{k+1}) queries at a separator re-solves both sides from
scratch; storing the response function is forbidden by rem:fold-width
(thm:fold's P_D has 2^{(N-2)/6} response pieces at tw = pw = 4; no
explosion at interface dimension one). THE AMORTISATION GAP of sec:width
(stated after prop:modulator-family, l.3170): "the O(B^{k+1}) payoff
vectors at which a separator node queries its children during one search
can be answered in total time polynomially related to the time to answer
one of them" -- that sentence would make thm:qp polynomial, N^{f(k)}.
Trivially in P as well: min(m,k) = O(log N), by enumerating the smaller
player's strategies and thm:one-player (noted at thm:bsi-tracks).
thm:subexp (random facet, e^{2 sqrt n} poly(N)). A POLYNOMIAL CLASS here is
a set of instances on which some PROVED BOUND is polynomial; classes are
compared as bounds, not as algorithms.

REFORMULATIONS AND EQUIVALENCES -- all TARGET-EQUIVALENT, so a route that ends
at one of them has ended at the target and must say so:
thm:compare-equivalence (compare two vertex values); thm:order-determines (the
preorder induced by w* on Vavg u {t0,t1} determines w*; O(a log a) bits;
Gimbert-Horn); thm:decide-one-bit (a sound poly-time DECISION rule resolving
one controlled vertex per round exists IFF SSG-Value is in P; termination by
RETYPING the decided vertex as an average vertex); prop:no-halving (no
reduction halves a; comparing two average vertices is target-equivalent);
cor:wrong-equivalence; thm:transport-objective (naming an optimal profile);
thm:gap-equivalence ((Poly-Rule) itself: a switching rule halting in
polynomially many rounds from every start exists iff SSG-Value is in P);
rem:bsi (a GUIDE U whose order agrees with w* at every Max vertex is
target-equivalent); thm:top (round 15, l.9390: finding the average vertex of
LARGEST value is target-equivalent -- one oracle call suffices, by reference
and boost chains).

STRATEGY IMPROVEMENT. thm:short-path (<= |Vmax| single improving switches
suffice from ANY sigma); cor:selection (all the difficulty is SELECTION);
thm:switch-count (every single-switch improving rule stops within N 2^a;
multi-switch within N 4^a); thm:ladder (def:ladder: L_n has Vmax = {v_1..v_n},
Vavg = {w_1..w_n}, v_i -> (v_{i+1}, w_{i+1}), w_i -> (v_{i+1}, w_{i+1}),
v_{n+1} = t0, w_{n+1} = t1; least-index and smallest-gap take 2^n - 1 switches
while all-switches takes n and the shortest improving route has length ONE;
rem:ladder: this is Melekopoglou-Condon transcribed, and THEIR open question
-- is Howard's rule superpolynomial with two actions per state -- is the
one-player half of this project's pivot); cor:no-height (no progress measure
of polynomial height on the Max strategy lattice); thm:impedance (the exact
gain of a switch is a bounded transfer impedance divided by an escape
probability that can be 2^{-Theta(N)}; no potential of polynomial range);
prop:serialiser; thm:normalform-barrier (no residue-blind rule beats
all-switches: lem:normalform makes the controlled vertices an independent set
preserving values, stopping and the whole all-switches trajectory);
thm:window-barrier (def:kblind puts every value behind k+1 average
two-cycles; covers rules that solve O(N^alpha) average vertices for alpha < 1
and NOT linear windows -- corrected in round 15);
thm:all-switches-refuted (all-switches does not dominate single switches);
prop:allswitch-overshoot; prop:rules-fail (seven natural rules fail, each
with an explicit witness).

THE ALL-SWITCHES LAWS (sec:allsw-laws). thm:peak-law (the peak of
val_{t'} - val_t over an interval sits on S_t; cor:peak-sharp, round 15);
cor:no-return, cor:law-b, cor:antichain, cor:law-u (the switched sets
S_0..S_L of a run are pairwise distinct); thm:component-bound;
prop:closed-now-or-never (a CLOSED CONFIGURATION (W,pi), once nothing is
switching into it, is bounded below by lambda_W for ever and NEVER ENTERED
AGAIN -- the first irreversible event a polynomial bound could count;
rem:closed-now-or-never: NOT a barrier, a Max vertex over a Max vertex
simulates a third action with one round of lag; lem:max-tree: a Max vertex
of fan-out r is binarised by a Max tree with lag ceil(log2 r));
lem:rise-bound (round 15: for sigma <= sigma' pointwise and u in Vmax at
rest at sigma, the RISE of u is at most the largest rise among the vertices
its later action reads -- the impedance denominator of thm:impedance
amplifies the GAP, not the RISE; rem:impedance); cor:isolated;
prop:zero-ties; rem:grid-per-vertex (l.6913: L <= sum_v n_v <= m(D(a)-1),
L <= m at a = 0, and the one-player chain RC(k): v_i -> (v_{i+1}, t0),
v_k -> (t1, t0) attains L = N-2; whether L <= N-2 holds for EVERY one-player
stopping SSG is open, measured true at n <= 10).

def:bsi, BIDIRECTIONAL IMPROVEMENT (no barrier covers it): a PAIR (sigma,tau);
L = val_sigma, U = val^tau; S_sigma as above, S^tau = {u in Vmin :
U(tau-bar(u)) < U(tau(u))}; vetoes C_max = {v in S_sigma : U(sigma-bar(v)) >=
U(sigma(v))}, C_min = {u in S^tau : L(tau-bar(u)) <= L(tau(u))}; one round
switches both sets simultaneously; halt when both are empty; the STRICT
variant uses strict veto inequalities. thm:bsi-nostall (halting implies
L = U = w* on stopping games); cor:bsi-correct (<= 2N4^a rounds);
prop:bsi-nonstopping; lem:bsi-pairloc / cor:bsi-levels ((M,|Z|) with
M = max(U-L) decreases lexicographically); prop:bsi-br / rem:bsi-br: if tau
is ANY Min best response to sigma and S_sigma is nonempty then C_max is
nonempty, so R_BR(sigma) := sigma[{v in S_sigma : val^tau(sigma-bar(v)) >=
val^tau(sigma(v))}] is a SWITCHING RULE halting only at an optimum; on L_n
it takes floor(log2 n)+1 rounds; on G# 5 rounds (c_3 switched three times,
corrected in round 15). ROUND 15 ADDED: thm:bsi-tracks (R <= m+(m+1)B,
R <= k+(k+1)A, so a superpolynomial BSI run needs BOTH tracks
superpolynomially long, both variants); thm:readout (RD(n), N = 9n:
all-switches halts in ONE round from every start, R_BR takes exactly n
rounds, def:bsi exactly 2n -- R_BR CAN be slower than all-switches by a
factor Theta(N)); prop:leapfrog (SD(K): a ONE-PLAYER stopping SSG on O(K^2)
vertices in which one Max vertex is switched K times by all-switches --
per-vertex switch counts are unbounded); lem:same-successor (two Max
vertices with the same successor pair: the strict clause); prop:bsi-normal
(BSI is compatible with lem:normalform's normal form); prop:q16 (Q_16, 288
vertices: BSI reverses Min vertex c_10 four times, three of them L-ties and
one genuine). The rbr route's proposed counter (v_j over (a_j, b_j) with b_j
a CONSTANT gadget, u_j -> (v_j, Theta_j)) was REFUTED by its auditor: a Max
vertex with a constant successor switches at most twice. ATTRIBUTION: def:bsi
is van Dijk-Loho-Maat's generalised symmetric strategy iteration and R_BR its
one-track variant; Schewe-Trivedi-Varghese for symmetric improvement.

THE ALL-SWITCHES / AUSO IDENTIFICATION -- THE PIVOT.
def:improvement-uso, prop:allsw-auso: for a NONDEGENERATE stopping SSG (no
tied incidence (sigma,i)) the improvement outmap is the outmap of an ACYCLIC
UNIQUE SINK ORIENTATION (AUSO) of the |Vmax|-cube and all-switches is exactly
its BOTTOM-ANTIPODAL (BA) walk. thm:flat-resolution / cor:ceiling-general:
EVERY all-switches run of EVERY stopping game, degenerate or not, is a BA
walk of an AUSO. THE FOUR CEILINGS (rem:four-ceilings, l.6303, all exact):
  m            1  2  3  4   5    6    7
  h*(m)        1  2  4  7  12  >=16 >=26   (prop:auso-census, prop:hstar-five, thm:blowup)
  h*_HK(m)     1  2  4  6  11  >=12 >=13   (prop:hkfive: h*_HK(5) = 11 PROVED, exhaustive)
  h*_LP(m)     1  2  4  6  >=9 >=12 >=12
  h*_1(m)      1  2  4  6  >=9 >=12 >=12   (cor:hstar-one: h*_1(4) = 6 PROVED; prop:oneplayer-runs)
where h*_1 is the one-player ceiling (nondegenerate one-player games), h*_HK
the greatest BA height of a Holt-Klee AUSO, h*_LP that of an LP orientation.
prop:oneplayer-lp: a NONDEGENERATE ONE-PLAYER stopping game's improvement
orientation is the LP orientation of its occupancy polytope (d'Epenoux),
hence HOLT-KLEE (Holt-Klee + Gaertner-Morris-Ruest) -- so h*_1 <= h*_LP <=
h*_HK. thm:no-seven (sec:ties): NO one-player stopping SSG with |Vmax| = 4,
degenerate or not, has a run of length 7, so ties do not beat the HK
ceiling at m = 4; thm:zero-timer: a zero-tie timer wakes within m rounds
(sharp); thm:b2-walk: B^2's walk from the paper's start is the run of NO
one-player game, degenerate or not. lem:hstar-super: h*(k+l) >= h*(k) +
h*(l) (the product preserves Holt-Klee for SOME block orders: HK(6) >= 12,
HK(7) >= 13; no doubling follows). thm:blowup (PROVED, machine-checked in
lean/SSGProof/Blowup.lean): for ANY AUSO s of the m-cube with sink o and a
vertex u of maximal BA height h, z := o xor u; the (m+2)-cube orientation
B(s) has inner part s(v xor z) on layer (alpha,beta) = 00 and s(v) on the
other three layers, and outer part depending only on the layer and the
PARITY of h(v): 00 -> {}; 10 -> {a,b} if h(v) even, {a} if odd; 01 -> {b}
if even, {a,b} if odd; 11 -> {a} if even, {b} if odd. B(s) is an AUSO of
BA height >= 2h+2 (exactly 2h+2 on every seed measured). Hence h*(m+2) >=
2h*(m)+2 and h*(m) >= 2^{m/2+1}-2. B depends on the PAIR (s,u).
rem:blowup-measured: from the second level on z is a SINGLE coordinate of
the previous level's outer pair (beta if that level's seed height was odd,
alpha if even, hence alpha from the third level on). sec:deformed (round 15):
lem:blowup-faces / cor:blowup-parity / cor:blowup-transl: WHY B loses
Holt-Klee -- a parity condition on the seed alone and a translation
condition, so EVERY iterate B^k, k >= 2, is non-Holt-Klee; HK blow-ups in
the rule family reach only heights 4,6,8 at dimensions 3,4,5;
thm:deformed-flat: every Amenta-Ziegler deformed product of cubes
(Klee-Minty, Chvatal, Goldfarb-Sit) has BA height at most the sum of its
factors' heights, at most d -- the classical LP arsenal is LP-hard and
BA-easy (prop:km-measured: Klee-Minty has BA height exactly d for d <= 12).
prop:auso-size: at most 2^{O(N log N)} orientations arise from stopping SSGs
on <= N vertices: NO CENSUS OR SAMPLING CAN DECIDE REALISABILITY, ONLY A
CONSTRUCTION.

WHAT IS REALISED. prop:auso-seven: the height-7 orbit of the 4-cube is the
improvement orientation of the two-player game G# on 97 vertices (4 Max, 2
Min, 89 average; normal form printed in the paper); cor:seven-two-player:
s_{G#} is non-HK, so its Min vertices are necessary. The first blow-up level
B(1-cube) (3-cube, height 4) is realised by a one-player game on 58 vertices
(${REPO}/scripts/blowup/B1_game.json). A layer translated by ONE coordinate
at inner dimension two is realised by one-player games (the 4-cube class
(0,1,3,2,7,6,4,13,15,14,12,9,11,10,8,5) of height 6, Holt-Klee; the
round-15 briefing's "translated by 1-bar" was the root agent's ERROR, since
corrected). prop:b2-realised (round 15, l.5288): THE SECOND LEVEL
B^2 = B(B(1-cube)), 5-cube, height 10, non-HK, outmap
(7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18)
in coordinates (seed, alpha_1, beta_1, alpha_2, beta_2), IS REALISED by a
nondegenerate stopping SSG on 138 vertices (5 Max, 1 Min, 130 average,
denominator 2^9), designed by hand (NOT found by search: every blind search
had failed), verified from the game by the root agent; its run from
sigma = 12 is 12,19,13,17,8,16,0,7,1,5,4; its harmonic normal form is
printed in the paper and is ${REPO}/scripts/blowup/B2_small_nf.json, the
game B2_small_GAME.json, the verifier verify_b2.py. The gadget theory
around it (l.5387-5534): def:reduced-rows, prop:rows-turn, cor:b2-rows,
lem:crossing (the crossing lemma on 2-faces), cor:b2-min (where the Min
vertex must act: four forbidden (2-face, coordinate) pairs),
cor:parity-unreadable (no affine functional reads the parity of the inner
height), prop:xor (how the layer is read: an XOR of alternation bits),
thm:alternation-bits. rem:blowup-realise (l.5534) now states THE OPEN
QUESTION OF THE PIVOT: whether each further level costs only O(1)
controlled vertices and O(1) bits of precision (the step 1 -> 2 cost +2 Max,
+1 Min, +3 bits; a lower bound of log2(h-1) average vertices holds); if so,
an SSG-realisable family of exponential BA height on polynomially many
vertices exists and (through thm:seed-dichotomy) the family defeats M3 and
sec:wedge's open item closes; a cost of N -> N^c per level would NOT do. THE
THIRD LEVEL B^3 = B(B^2), DIMENSION 7, HEIGHT 22, IS THE SMALLEST OPEN
INSTANCE. sec:readouts (round 15): def:readout / thm:readout-realise --
realisability of an orientation by a stopping SSG with m Max vertices is
EXACTLY a concave interpolation problem: per (v,a) a readout Psi_{v,a} of
the other Max values that is a MIN of r substochastic affine maps (one
player: r = 1, affine; each Min vertex at most doubles r), and conversely a
dyadic delta-leaky readout system of order (m,r) and denominator 2^D gives a
nondegenerate stopping SSG with m Max, <= 2m(r-1) Min and <= 2mr(m+1)D
average vertices; thm:min-count: k >= log2 chi_HK(s), where chi_HK(s) is the
least number of HK AUSOs s is a pointwise selection from (attained at B^2:
chi_HK = 2, k = 1); prop:m3-realised: ALL 18 AUSO classes of the 3-cube are
realised (16 HK by one player, the 2 non-HK by two-player games), so at
m = 3 one-player realisability = Holt-Klee EXACTLY; at m = 4 every HK class
of height 6 is realised by a one-player game (rem:hk-survey, measured).
sec:projection (round 15): the PROFILE CUBE (all 2^{|C|} positional pairs,
each controlled vertex strictly preferring its other action) of a
profile-nondegenerate stopping SSG is the Stickney-Watson orientation of a
P-matrix LCP with M = E(I-Q_1)(I-Q_0)^{-1}E (thm:profile-uso, prop:lcp:
P-matrix from first principles), the Max cube is its SINK PROJECTION along
the Min coordinates (prop:projection), and that projection is acyclic even
when the profile cube is cyclic; prop:seven-k1: s_{G#} is the k = 1 sink
projection of an explicit HK ACYCLIC 5-cube USO of height 7; the
projected-Holt-Klee constraint is VACUOUS at m <= 3 (every USO of the
3-cube is a k = 1 projection of an HK USO of the 4-cube, from the route,
not in the paper); the interior-point / handicap route is closed (rem:lcp).

THE MECHANISMS AND WHERE THEY STOP (sec:gap).
 M1 def:simorder, the value-simulation preorder: arithmetic-free, one greatest
 fixed point, beats every bounded radius, dies on branch compensation (G8);
 thm:matching-barrier kills its whole class.
 M2 def:slack, the slack calculus (Delta_k(x,y) bounds w*(x)-w*(y) from above;
 a negative entry decides); thm:slack-barrier and thm:slack-vi-upper SANDWICH
 it: on separated configurations it IS two-sided value iteration.
 cor:slack-stalls' 2^{Omega(N)} is PROVED for the pair test only; the
 own-successor firing rounds on H_m (15, 39, 101, 250, 597) are MEASURED.
 M2T def:trans-slack (min-plus transitive closure): thm:trans-complete says on
 STOPPING games it converges to the exact differences, so the question is a
 RATE; prop:trans-Hm collapses H_m from 2^{Omega(N)} to 4m-3 rounds (m <= 9).
 M3 def:seeded, seeding from policy evaluation; thm:seeded-barrier;
 thm:seed-dichotomy (CORRECTED in round 15: the exactness clause holds when
 Vmax is EMPTY or when sigma has no strictly switchable vertex and tau is
 greedy for val_sigma; it is FALSE for Vmin empty -- WD(4,2,6) is a
 one-player game on which M(0,0) stalls): EVERY STALLING INSTANCE OF M3 IS A
 STOPPING GAME ON WHICH ALL-SWITCHES HAS NOT CONVERGED AFTER p ROUNDS.
 M4 def:transport, the LP over Q(G) = {x : x(v) >= x(v^i) at Max, <= at Min,
 mean at avg, 0 <= x <= 1, sinks pinned}; lem:transport-dim; thm:transport-
 objective (w* is a VERTEX of Q(G)); prop:own-stall (a GENUINE decision
 stall of M4 on 10 vertices).
 M5 sec:hybrid, the transport-slack hybrid: thm:hybrid-complete,
 lem:hybrid-cutting, prop:hybrid-onectrl (|C| = 1 exact at round two),
 thm:hybrid-lower (CC(L,m), 2^{Omega(N)} rounds for the pair entry),
 thm:hybrid-convex-barrier (a METHOD).
 M6 sec:ratio, the MULTIPLICATIVE calculus: thm:ratio-sandwich (the SAME
 two-sided bound as M2), cor:ratio-stall, prop:mobius (a continuum between
 M2 and M6, every member stalling identically), prop:ratio-closure. MORAL:
 thm:slack-barrier constrains any calculus matching the two branches of an
 average vertex ONE AT A TIME, whatever the algebra. thm:separable: a
 certificate phi(x)-psi(y) surviving a min-plus closure is the exact limit
 and proves nothing about a rate.
 sec:wedge, THE STATE OF THE ART ON THE NEGATIVE SIDE. def:wedge WD(e,j,m),
 N = 2e+j+m+5, ONE-PLAYER, Vmax = {v1,v2}, both value-distinguishing with gap
 2^{-m}: thm:wedge-proved + cor:wedge-count: the Z-seeded own-successor
 hybrid is silent for K = 1,6,15,33,68,138,279,560 rounds at j = 2..9, so
 2^{Omega(N)}. rem:wedge: WD defeats M2, M2T, M4, M5 and M6 and defeats
 NEITHER M1 (the gfp contains (v_i, a_{i,1}), firing at round zero) NOR the
 one-round variant M(1,0) of M3 (one all-switches round reaches Opt on
 WD). THE OPEN ITEM: a family defeating M1 AND M3 as well -- by
 thm:seed-dichotomy a family defeating M3 is a superpolynomial all-switches
 family. prop:fv-stall (round 15): FV(n), FV_2(n) with D(G) = 3 are
 PERMANENT stalls for M2, M2T, M4 (n = 3,4,5 exact), but VACUOUS ones --
 every controlled vertex has two successors of equal value; whether the
 few-denominator class contains a stall at a VALUE-DISTINGUISHING vertex is
 open (thm:slack-vi-upper converts the gap 1/D into a firing round only
 through the value-iteration width, whose rate is (1-2^{-a})^{k/N}).

BARRIERS, and exactly what each covers. thm:impedance (polynomial RANGE);
cor:no-height (polynomial HEIGHT on the Max lattice); prop:locality (bounded
radius, every k); thm:normalform-barrier (residue-blind rules);
thm:window-barrier (windows O(N^alpha), alpha < 1); thm:matching-barrier;
thm:slack-barrier / thm:seeded-barrier / thm:ratio-sandwich;
thm:hybrid-convex-barrier (a method); prop:no-submodular (lem:readonce);
sec:fold / thm:fold (freezing one vertex at payoff theta gives a response
map with EXACTLY 2^D pieces -- kills continuations that TRACK THE OPTIMAL
PAIR, and kills exact response TABLES in width decompositions);
thm:vi-lower (value iteration exponential with NO players); thm:separable;
prop:a-presentation (a is a property of the presentation);
thm:lasserre-vacuous (the degree-two Lasserre lift of Q(G) adds nothing;
exact at |C| <= 2); rem:lcp (interior point / handicap: closed, not ours).

# UNVERIFIED claims from earlier rounds (do NOT cite as established)

(v3) All-switches on stopping ONE-player SSGs is exactly Howard's policy
 iteration on transient 2-action MDPs, both directions (b needs a uniform
 leak). If so the one-player half of the pivot is "is Howard's rule
 polynomial on 2-action MDPs" -- Melekopoglou-Condon's question.
(v5) TW(2j,j,j+4), N = 8j+13, two Max and two Min, keeps the Z-seeded
 own-successor hybrid silent at all four controlled vertices for 5, 10, 19, 39
 rounds at N = 37,45,53,61; all-switches halts on it in ONE round.
(v7) Newton on F(x) = x - Tx: plain Newton CYCLES with period 3 on a 25-vertex
 stopping SSG.
(v8) A poly-startable exact CONTROL HOMOTOPY annihilates WD and CC yet needs
 2^{0.146N} switches on thm:fold's P_D.
(v10) UEOPL: the canonical line is exponential (PEN(D,K)); the route's
 induction used an inequality equivalent to D < 4; DO NOT cite.
(v11) Bounded kappa(G) = max expected visits to controlled vertices gives a
 polynomial algorithm unconditionally, so any algorithm conditional on it is
 worthless.
(s1) From the round-15 sink-projection route, not in the paper: every USO of
 the 3-cube is the k = 1 sink projection of an HK USO of the 4-cube; the
 route's auditor found all 31 sampled non-HK 4-cube classes to be k = 1
 projections of HK 5-cube USOs; no HK 5-cube USO within Hamming distance 7
 of B^2 projects to it at k = 1.
(s2) From the round-15 monotone route: 13 one-player games at m = 4 present
 a single-coordinate translate of a 3-cube on a facet; prop:mono-count:
 almost every AUSO needs 2^{Omega(m)} vertices (counting).
(s3) From the round-15 lane route: the annealer of its measurements could not
 even rediscover RC(7); its numbers are not evidence.

# PRIOR ART THIS PROJECT HAS ALREADY REDISCOVERED (about twenty times)

Auger-Coucheney-Strozecki (almost-acyclic SSGs, FPT in the feedback vertex
number); Mangasarian (hidden-K LCP by one LP); Gaertner-Morris-Ruest
(realisable USOs are Holt-Klee); Stickney-Watson (LCP/USO correspondence);
Gimbert-Horn (the permutation space and its decoder); Dai-Ge (approximation
collapse); Meyer (stochastic complementation = exact vertex elimination);
Kannan-Theobald (fixed-rank games); Blondel-Nesterov (escape rate as a joint
spectral radius); van Dijk-Loho-Maat (def:bsi; R_BR); Melekopoglou-Condon
(thm:ladder and the open question); d'Epenoux (the occupancy LP);
Holt-Klee; Hansen & Ibsen-Jensen (2TBSG -> P-matrix LCP); de Klerk & E.-Nagy
(exponential handicap); Haddad-Monmege (two-sided rounded iteration);
Amenta-Ziegler (deformed products); Etessami-Papadimitriou-Rubinstein-
Yannakakis and Dang-Qi-Ye (Tarski fixed-point search); Legendre
(convergents); Samelson-Thrall-Wesler (P-matrices); Charnes / Dantzig-Orden-
Wolfe (lexicographic perturbation); Jonsson-Larsen / Segala-Lynch
(probabilistic simulation); Schurr-Szabo (jumping in abstract cubes, whose
open question is the growth of the BA height of realisable cubes).
STATE OF THE ART on the pivot as reported from memory by earlier routes:
exponential all-switches lower bounds exist for parity / mean-payoff /
discounted / simple stochastic games (Friedmann 2011) and for Howard on
total- and average-reward MDPs (Fearnley 2010) and reachability MDPs
(Christ-Yannakakis 2023), ALL with Theta(n) actions per state; for TWO
actions per state the best known upper bound for Howard is O(2^n/n)
(Mansour-Singh; Hollanders-Gerencser-Delvenne-Jungers) and the best known
lower bound is linear or quadratic (Hansen-Zwick for deterministic
mean-cost cycles; Mukherjee-Kalyanakrishnan). A superlinear BINARY family
would be new even for one player. Whether Fearnley's construction
binarises is undecided here: its timing action is a self-loop escaping to
g_i, not a sink, so the round-14 argument that it does not was wrong.
Condon 1992 is the source of the problem and of the stopping transformation;
Ludwig and Bjorklund-Vorobyov of the random-facet bound. If your route
reproduces something standard, SAY SO and attribute it, from memory, flagged
as unchecked. A rediscovery honestly labelled is useful; a rediscovery
presented as new is a defect.

DEAD, not to be re-derived: entropic/softmax regularisation; Newton-Dinkelbach
(Radzik/Megiddo with one SSG-specific line); polynomial classes by the rank of
an action-difference matrix (Kannan-Theobald); Schur/vertex elimination
(Meyer); vertex enumeration of Q(G) (exponentially many vertices even on
linear-time instances); the bubble step in order space (FALSE on an 8-vertex
game); totally ordered universal lattices (height 2^{Omega(N)}); blind
searches for realisations at m >= 5 (huntG, huntW2, ascendB, realiseAP,
bilinear alternation, successive LP -- all failed for hours on a target
later realised by design); the Lasserre degree-two lift; the interior-point
handicap route; deformed products as a source of tall BA walks; zero-tie
timers as a source of long one-player runs (capped at m rounds).

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
   mobius.py (M6), seven.tex/t_seven.py (G#), r14routes/ (round-14 route
   code: allsw-lower/, free-search-14/, bsi-rounds/). The solo round's
   working directory is ${SCRATCH}/solo/ (realiseAP.py, ap_lp.py, ap_es.py,
   blowz.py, blowc.py, blowhk.py, my_D.py (the Holt-Klee max-flow test),
   bigcube.py, km.py, verifyG.py, fastnf.py, nf2.py, build.py, verify.py,
   b2cube.py, census/classes4.txt = one representative per AUSO class of the
   4-cube, AP_m4_k0_*.json = exact one-player games realising 4-cube
   classes, B1_game.json). The root agent's round-15 verification scripts
   are ${SCRATCH}/myver/ and, committed, ${REPO}/scripts/round15-verify/
   (verify_b2.py, hk_product.py, hc_oneplayer.py, sd_check.py,
   rd_sd_check.py, q16_check.py, tw_check.py, mn_check.py, rise_bound.py,
   glaw.py, gad_check.py, top_check.py, stack_parity.py, verify_games.py);
   the blow-up files are ${REPO}/scripts/blowup/ (README.md explains each;
   B2_small_GAME.json, B2_small_nf.json, hstar_all.c, ...). ROUND-15 ROUTE
   CODE, read-only, is under ${PREV}/<route>/ : gadget/ (slp6.py = the
   successive-LP realiser with a prescribed Min response, faces.py = the
   forbidden faces, polish.py, build512.py, gcore.py, b2target.py, verify.py,
   finalcheck.py), monotone-lemma/ (mono.py with concave_lp, mono2.py,
   slp.py, targets.py, t_m3.py), howard-cube/ (hc_hk.c = the Holt-Klee
   max-flow test in C, hc_deform.py, t_stack.py, t_blowhk.py, nf2.py, and the
   exact m = 5,6 one-player normal forms in its nf*.log files), treewidth/
   (alg.py = the Tarski/separator algorithm, family.py = M_n, fold.py),
   rbr-rounds/ (brlib.py, family.py = RD/SD, the Q_16 data), free-search-15/
   (t_b2_ties.py = the completion + tie screen; the root agent's hwalk.c
   completion enumerator is in ${SCRATCH}/myver/), sink-projection/,
   degenerate/, lane-reuse/, verify-r14/. Round-14 and round-13 route
   directories are under ${P14}/ (allsw-lower/, allsw-degeneracy/,
   lasserre-2/, lcp-handicap/) and ${P13}/ (auso-pivot/, two-player-wedge/).
   COPY what you need into ${SCRATCH}/<your-route>/ and work there. Do NOT
   write into another route's directory, into ${PREV}, or into ${REPO}
   (in particular do NOT touch frontier.tex or README.md -- a round-15 route
   wrote into README.md and its edit was reverted); the root agent
   integrates.
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
     UNREACHABLE from the start; round 15's root agent recorded a translation
     vector wrong by reading one seed pair for all of them.
   - A Max vertex whose two options are a variable and a CONSTANT switches at
     most twice along any run (round 15's rbr audit): counters need
     non-constant drivers.
   - After proving or measuring anything on the instances you developed it on,
     RE-RUN it on freshly generated, larger instances before reporting.
   - A "witness" normal form that is not dyadic, or whose game was never
     built, is NOT a game (round 15's degenerate route claimed attainment by
     non-dyadic normal forms). Build the game and verify from the game.
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
   where its output goes. Kill your own background jobs before returning
   unless their output is named in your result.
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
    key: 'b3-level',
    model: 'opus',
    title: 'The third blow-up level: realise B^3 (7-cube, height 22) and measure the cost of one level',
    brief: `
YOUR ROUTE IS THE CONSTRUCTIVE SIDE OF THE PIVOT AT ITS SMALLEST OPEN
INSTANCE. Read, in this order: thm:blowup and rem:blowup-measured (l.5125,
5214), prop:b2-realised and the gadget theory that follows it (l.5288-5534:
def:reduced-rows, prop:rows-turn, cor:b2-rows, lem:crossing, cor:b2-min,
cor:parity-unreadable, prop:xor, thm:alternation-bits), rem:blowup-realise
(l.5534), sec:readouts (l.6332-6537), lem:dyadic-row (l.980),
prop:oneplayer-lp (l.4752), thm:min-count (l.6486). Then
${REPO}/scripts/blowup/README.md and the files it names, and the round-15
gadget route's code, read-only, at ${PREV}/gadget/ (slp6.py = successive LP
over the harmonic normal form with a PRESCRIBED Min best response;
faces.py = the forbidden (2-face, coordinate) pairs of cor:b2-min; polish.py;
build512.py = dyadic rounding at denominator 512 and game construction;
gcore.py = the normal-form game class NFG(m,k,P,Q) with outmap();
b2target.py; verify.py; finalcheck.py; its result record is
${REPO}/rounds/round15/results/16_*.json, whose next_steps say exactly how
it expected level three to go).

THE TARGET. B^3 := B(B^2), where B^2 is the 5-cube outmap printed in
prop:b2-realised and B is thm:blowup's operation with u the start of the
walk of B^2 (the vertex of maximal height 10, which in the paper's
coordinates is sigma = 12; compute z = o xor u yourself and confirm it is a
single coordinate, alpha_2 by rem:blowup-measured). B^3 is an AUSO of the
7-cube of BA height 22 (recompute it with ${REPO}/scripts/blowup/blowz.py or
your own code, confirm USO, acyclicity and height 22 in exact arithmetic,
and print the outmap in the coordinates (seed, alpha_1, beta_1, alpha_2,
beta_2, alpha_3, beta_3)). Its layer (alpha_3,beta_3) = 00 carries B^2
translated by e_{alpha_2}.

WHAT TO DO.
 (1) Reproduce the level-two realisation first: from B2_small_nf.json build
     the game, verify outmap = B^2 from the game (all 32 Max strategies, Min's
     best response by the minimum over both tau), and READ OFF THE DESIGN:
     which rows encode the layer, how the Min vertex c_6 implements the
     four forbidden faces of cor:b2-min, where the alternation bits of
     thm:alternation-bits live in the rows. Write that as a lemma about the
     normal form ("the rows of a B(s)-realisation are the rows of an
     s-realisation extended by ..."), so that level three is a TRANSFORMATION
     of the level-two normal form rather than a fresh search.
 (2) Build B^3 by design: inner = the 138-vertex game (or its normal form,
     re-solved), outer = alpha_3, beta_3 with the parity-of-height rule read
     through alternation bits, layer-00 translation by alpha_2. Decide how
     many Min vertices the forbidden faces of B^3 need (list them with
     faces.py generalised to dimension 7; thm:min-count gives a lower bound
     through chi_HK(B^3) -- compute chi_HK(B^3) if you can, it is a
     set-cover question over HK 7-cube AUSOs agreeing with B^3 pointwise on
     subsets, which you may attack via the faces). Fix the support pattern
     of the rows, solve for the entries by exact LP (a prescribed Min
     response per Max strategy makes the system linear), round to dyadic at
     the least denominator that survives, and build the game with
     lem:dyadic-row.
 (3) VERIFY FROM THE GAME: nondegenerate, stopping, USO, acyclic, outmap =
     B^3, BA height 22, the all-switches run of length 22 printed round by
     round with the exact value vectors, values increasing every round.
     The verification is 2^7 Max strategies times 2^k Min strategies of an
     exact linear solve on a game of a few hundred vertices: budget it
     (write it in exact arithmetic with a sparse solver; hours are
     acceptable in the background; report what is still running).
 (4) THE COST DATUM. Report |Vmax|, |Vmin|, the denominator and |Vavg| at
     levels 1, 2, 3, and state the recurrence the three points support.
     Say whether level three cost O(1) controlled vertices and O(1) bits
     over level two, as rem:blowup-realise asks.
 (5) If you fail: the obstruction AS A THEOREM with an explicit instance --
     "no game of shape X (inner = the 138-vertex game, outer = ..., Min
     vertices acting on faces F) has layer-00 orientation B^2 translated by
     alpha_2, because Y", with Y an infeasible exact LP for a fixed support
     pattern; say exactly which patterns you excluded and which you did not.

REQUIREMENTS. Exact rational arithmetic for every claim; floats only to
explore. val_sigma with Min present is a minimum over ALL positional tau or
thm:eval-stopfree's LP. Every probability realised by lem:dyadic-row chains,
size cost reported. Do NOT run blind searches. Labels prefixed b3:.
`,
  },
  {
    key: 'level-lemma',
    model: 'opus',
    title: 'One blow-up level at additive cost, as a theorem: the inductive realisation lemma or its exact obstruction',
    brief: `
YOUR ROUTE IS THE THEORETICAL SIDE OF THE PIVOT'S OPEN QUESTION. Read
thm:blowup (l.5125), rem:blowup-measured (5214), prop:b2-realised and the
gadget theory (5288-5534: def:reduced-rows, prop:rows-turn, cor:b2-rows,
lem:crossing, cor:b2-min, cor:parity-unreadable, prop:xor,
thm:alternation-bits), rem:blowup-realise (5534), sec:readouts in full
(6332-6537: def:readout, lem:readout, lem:readout-reduce, def:readout-system,
thm:readout-realise, thm:min-count, prop:m3-realised), thm:impedance
(3543), lem:switch, and lem:dyadic-row (980). The level-two game is
${REPO}/scripts/blowup/B2_small_GAME.json with normal form B2_small_nf.json;
the round-15 monotone route's code (read-only) is ${PREV}/monotone-lemma/
(mono.py: concave_lp decides, for a FIXED value configuration x = (x_sigma),
whether readouts exist, as one LP).

THE QUESTION, stated exactly (rem:blowup-realise): is there a constant c such
that for every level k the orientation B^k is the improvement orientation of
a nondegenerate stopping SSG whose controlled part has O(k) vertices and all
of whose first-passage probabilities are dyadic of denominator at most
2^{ck}? Level 1 -> 2 cost +2 Max, +1 Min, +3 bits. A lower bound of
log2(h-1) average vertices is known and is far from an obstruction.

YOUR TASK is to prove the inductive step or to find the exact obstruction.
 (A) THE INDUCTION HYPOTHESIS. B(s) asks the inner game to export two
     things: the rest predicate of the outer pair (readable in the same
     round: a Max vertex x over p,q is at rest iff val(x) = max(val p, val q))
     and the PARITY of the inner height h(v) at the current inner strategy,
     which cor:parity-unreadable says no affine functional of the values
     reads, and which the level-two game reads through an XOR of alternation
     bits (prop:xor, thm:alternation-bits). Formulate the right STRENGTHENED
     hypothesis: "s is realised by a readout system of order (m,r),
     denominator 2^D, which in addition exports a parity signal of the form
     ..." -- and prove that B(s) is then realised by a readout system of
     order (m+2, r') and denominator 2^{D+c} exporting the same kind of
     signal. Every ingredient must be an explicit substochastic affine map
     or a min of them (thm:readout-realise's language), with the leak and
     the denominator tracked. The translated layer needs the inner vertices
     to compare their options AS IF alpha_{k-1} were flipped when both outer
     vertices are at rest; say precisely which readouts change and by what
     conditional summand (a min against a threshold built from the rest
     predicates, through Min vertices).
 (B) TEST THE STEP AT THE KNOWN LEVELS. Whatever you formulate must
     reproduce a realisation of B^2 from the 58-vertex B^1 game (or from
     its normal form) and must, applied to the 138-vertex B^2 game, produce
     a candidate for B^3 whose realisation you can at least begin to verify
     (the b3 route is doing the full construction independently; you may
     exchange nothing with it, but your lemma must be consistent with the
     realised data: +2 Max, +1 Min, +3 bits at level two).
 (C) IF THE STEP FAILS, THE OBSTRUCTION AS A THEOREM. Candidates: the
     parity signal's precision must double per level (prove a lower bound on
     the denominator of any realisation of B^k, better than log2(h-1), from
     the walk's 2h+2 strictly increasing value vectors and thm:impedance's
     gain formula); or the number of Min vertices must grow with chi_HK(B^k)
     (thm:min-count) -- compute or bound chi_HK(B^k) as a function of k; or
     the readout order r must double per level. A lower bound that grows
     superpolynomially in k CLOSES the blow-up as a source of the pivot's
     family, and is a theorem worth as much as the construction.
 (D) Also answer the monotone route's open question where you can: is every
     AUSO of the m-cube realised by a readout system of FINITE order
     (equivalently by a stopping SSG with exactly m Max vertices)? At m = 3
     yes (prop:m3-realised); B^2 at order (5,2). A proof, or an orientation
     realisable by no finite order, either is progress.

REQUIREMENTS. Every construction exact (fractions); every game built and
verified from the game. Labels prefixed lvl:.
`,
  },
  {
    key: 'hk-doubling',
    model: 'opus',
    title: 'The Holt-Klee ceiling: is h*_HK(m) superpolynomial, and what LP orientations of cubes can do for the bottom-antipodal walk',
    brief: `
YOUR ROUTE IS THE ONE-PLAYER HALF OF THE PIVOT ON THE POLYTOPE SIDE. Read
prop:oneplayer-lp and rem:oneplayer-lp (l.4752, 4874), cor:seven-two-player,
sec:ties (5617-6045, especially thm:no-seven, cor:hstar-one, prop:hkfive,
thm:b2-walk), sec:deformed in full (6045-6332: def:deformed,
lem:deformed-rigid, thm:deformed-flat, prop:km-measured, lem:stack,
lem:blowup-faces, cor:blowup-parity, cor:blowup-transl, prop:oneplayer-runs,
rem:four-ceilings), lem:hstar-super (5034), thm:blowup (5125). The Holt-Klee
test is ${SCRATCH}/solo/my_D.py (unit-vertex-capacity max-flow); the 4-cube
class list is ${SCRATCH}/solo/census/classes4.txt; the law-abiding sequence
enumerator with all acyclic completions is ${REPO}/scripts/blowup/hstar_all.c;
the round-15 howard-cube route's code is ${PREV}/howard-cube/ (read-only;
hc_hk.c, t_stack.py, hc_deform.py, t_blowhk.py, and the exact one-player
normal forms of height 9 and 12 at m = 5, 6 in its nf*.log files).

THE FACTS. h*_HK(m) = 1, 2, 4, 6, 11 for m <= 5 (exact; h*_HK(5) = 11 by
exhaustive enumeration, witness printed in prop:hkfive); >= 12, >= 13 at
m = 6, 7 by the product of lem:hstar-super with the height-11 witness as its
FIRST block (the product preserves Holt-Klee for some block orders and not
others). Every iterate B^k, k >= 2, of the blow-up is non-HK for two
explicit 2-face reasons (a parity condition on the seed, a translation
condition); HK members of the blow-up rule family reach only 4, 6, 8.
Deformed products of cubes are BA-flat (height <= sum of the factors'
heights <= d). Klee-Minty has BA height exactly d for d <= 12. Nondegenerate
one-player all-switches runs are BA walks of HK AUSOs (prop:oneplayer-lp),
so h*_1 <= h*_LP <= h*_HK, and a polynomial bound on h*_HK would bound
Howard's rule on 2-action transient MDPs (Melekopoglou-Condon's question;
Mansour-Singh's O(2^n/n) is the best known upper bound, from memory).

YOUR TASK, either direction is a theorem.
 (UP) Prove h*_HK(m) <= poly(m), or h*_LP(m) <= poly(m). Holt-Klee is a
     combinatorial condition (m vertex-disjoint monotone source-to-sink
     paths on every face); the BA walk flips ALL outgoing coordinates at
     once; the disjoint paths give, on every 2-face, a source, a sink and
     two other vertices in a pattern (lem:blowup-faces lists what a 2-face
     refuses). Look for a potential that the disjoint-path structure
     supplies: e.g. the position of the current vertex along a fixed system
     of disjoint paths, the number of coordinates on which the outmap of the
     current vertex agrees with the sink's antipode, the Hamming distance to
     the sink after each jump on an LP orientation (the objective value
     strictly increases along the walk on an LP orientation: an LP
     orientation is induced by a linear functional on a polytope with the
     cube's graph, and the jump goes from a vertex to the vertex obtained by
     flipping all its improving coordinates -- on a cube polytope, is that
     vertex related to the current one by a bounded number of objective
     thresholds?). A polynomial upper bound for LP orientations alone would
     already give h*_1 <= poly(m), i.e. all-switches POLYNOMIAL on
     nondegenerate one-player stopping SSGs -- state exactly what you prove.
 (DOWN) Construct an HK-preserving dimension-raising operation with
     superlinear growth: dimension +2 with a readout that is NOT the parity
     of the inner height (the parity readout is what a 2-face refuses:
     enumerate readouts phi on the inner walk that are, on every 2-face,
     either unbalanced or separating the face's source from its sink,
     before building any orientation), or +3, +4 rules never tried; or a
     direct family of LP orientations of cubes (an explicit deformed
     polytope with the cube's graph and an explicit objective) with BA
     height growing faster than any polynomial. Verify HK by the max-flow
     test and acyclicity exactly; give the outmaps at three consecutive
     dimensions and the heights.
 (BETWEEN) Settle the remaining finite questions exactly where you can:
     h*_HK(6) (is it 12? the enumeration at m = 6 is large; use the
     law-abiding-sequence method of hstar_all.c with the HK test on
     completions, and say what you could and could not finish); whether the
     five unresolved HK classes at m = 4 are LP orientations (a real
     quantifier-elimination or sign-pattern-fixed linear feasibility
     question the round-15 route left open); h*_1(5) (is it 9, 10 or 11? the
     exact one-player normal forms of height 9 exist; a one-player game of
     height 11 at m = 5 would need the prop:hkfive witness realised).

REQUIREMENTS. Exact arithmetic; every orientation you exhibit printed as an
outmap with USO/acyclic/HK/height verified. Labels prefixed hkd:.
`,
  },
  {
    key: 'width-amortise',
    model: 'opus',
    title: 'Bounded treewidth: the amortisation statement that would make the quasipolynomial search polynomial',
    brief: `
YOUR ROUTE IS A POSITIVE ALGORITHMIC ONE. Read sec:width in full
(l.2874-3190: def:width, lem:payoff-transfer, lem:cut-sign, thm:tarski,
lem:round-recover, thm:modulator, thm:qp, rem:fold-width,
prop:modulator-family, and the amortisation paragraph after it), lem:cut
(2155) and lem:successor-closed, thm:fold (12368, the response map with 2^D
pieces), thm:alphabet-iteration (sec:alphabet, the up-rounded iteration
exact on a grid), thm:contraction. The round-15 treewidth route's code is
${PREV}/treewidth/ (read-only; alg.py implements the separator recursion
with the Tarski search, family.py builds M_n, fold.py builds P_D; its result
record ${REPO}/rounds/round15/results/18_*.json states its two ideas for the
gap: warm-starting the child searches along the nested box of lem:cut-sign,
and a path-decomposition sweep whose state is the value vector on one
interface). The root agent's checks are ${SCRATCH}/myver/tw_check.py and
mn_check.py.

THE GAP, stated exactly (l.3170): the O(B^{k+1}) payoff vectors at which a
separator node queries its children during one search can be answered in
total time polynomially related to the time to answer one of them. That
statement makes thm:qp polynomial, N^{f(k)}: a SEVENTH combinatorial
polynomial class, bounded treewidth, which contains no earlier class and is
contained in none (check this against thm:few-avg, thm:kacyclic,
thm:bounded-components, thm:escape-class, thm:few-denominator, thm:modulator
with explicit members, on the reachable subgame).

WHAT TO TRY, in order.
 (1) The structure of a child's response. For a separator X and a component
     C, the map theta -> val_{C}(theta) (values on C's interface as a function
     of the payoffs theta on X) is monotone, nonexpansive in the sup norm,
     piecewise affine with pieces indexed by positional pairs on C, and
     lem:cut-sign says it is sign-definite. The Tarski search on the parent
     queries it at points that move one corner of a shrinking box. Prove or
     refute: the total number of DISTINCT pieces the search visits is
     polynomial in the search length -- or the total number of value changes
     across queries is bounded by a potential (e.g. the sum over the
     interface of the number of times a coordinate's optimal pair changes
     is bounded by the number of Tarski steps times something polynomial).
     rem:fold-width forbids storing all pieces; it does not forbid a
     potential argument on the VISITED pieces.
 (2) Warm starts. A child solved at theta is a strategy pair optimal for
     theta; at theta' near theta, strategy improvement from that pair needs
     how many rounds? Use thm:short-path (<= |Vmax| switches suffice) and
     lem:cut-sign, and bound the work per query by the number of vertices
     whose optimal action changes between consecutive queries; then bound
     the total number of action changes along the search by a monotonicity
     argument (queries move monotonically in each coordinate of the box).
 (3) A different decomposition. Path decompositions with a left-to-right
     sweep whose state is the value vector on one interface, solved by the
     up-rounded iteration of thm:alphabet-iteration on the alphabet's grid
     (denominators are bounded by 2^a, so the grid is exponential; the
     sweep may still be polynomial per interface point if the interface is
     bounded and the values on it are determined by few candidates --
     examine whether lem:round-recover lets you work with O(N)-bit
     approximations).
 (4) Prior art from memory: parity games of bounded treewidth are in P
     (Obdrzalek); for stochastic games of bounded treewidth say what you
     know and flag it; if the bounded-treewidth SSG problem is already known
     to be polynomial, reconstruct the argument and attribute it.
 Deliverables: an algorithm with a complete proof of correctness and a
 bound N^{f(k)}, implemented and checked exactly against brute force on
 random stopping games of treewidth 2, 3, 4 with N up to 40 (vary the width,
 report the measured query counts against the bound); or a theorem locating
 exactly why the amortisation fails (an explicit family of width 2 or 3 on
 which the visited pieces are superpolynomial in the search length).

REQUIREMENTS. Exact arithmetic for every value; report every hypothesis
(stopping, the decomposition given, payoffs dyadic). Labels prefixed wa:.
`,
  },
  {
    key: 'few-denominator-stall',
    model: 'opus',
    title: 'Does the few-denominator class contain a genuine stall, or do the calculi decide it?',
    brief: `
YOUR ROUTE SITS BETWEEN THE CLASSES AND THE MECHANISMS. Read sec:alphabet in
full (l.2367-2874, especially def:alphabet, thm:alphabet-iteration,
cor:grid-iteration, thm:few-denominator, rem:alphabet-compare,
prop:fv-family, prop:fv-stall and the paragraph after it), sec:slack
(10359-11001: def:slack, thm:slack-sound, thm:slack-barrier,
cor:slack-stalls, thm:slack-vi-upper, def:trans-slack, thm:trans-complete),
rem:own-successor and prop:own-stall (in the transport section, 11771-12344),
sec:hybrid (12442-13112: def:hybrid, thm:hybrid-complete, lem:hybrid-cutting,
thm:hybrid-lower), sec:wedge (13112-13432), sec:simorder (10175-10359),
def:seeded and thm:seed-dichotomy (11582-11771). The harness has all six
mechanisms (${SCRATCH}/root16/: mycore.py slack_step / minplus_close /
transport_sep / hybrid, ownhyb.py for the own-successor test, zseed.py for
the Z_0/Z_1 seed, ratio.py, mobius.py, the simulation preorder in the
sec:simorder code under myinst.py / t_standing.py) and the round-15 verify
route's FV stall code is ${PREV}/verify-r14/ (read-only).

THE QUESTION, stated exactly (after prop:fv-stall): exhibit a stopping SSG
family with D(G) = poly(N) carrying a VALUE-DISTINGUISHING controlled vertex
(two successors of different value) on which the Z-seeded own-successor
transport-slack hybrid of sec:hybrid is silent for superpolynomially many
rounds -- or prove that none exists. The tension: a common denominator D
makes every nonzero gap at least 1/D, and the up-rounded iteration on the
grid is exact in O(ND) rounds (thm:alphabet-iteration), but the calculi do
not round, and thm:slack-vi-upper converts a gap into a firing round only
through the two-sided value-iteration width, whose rate is (1-2^{-a})^{k/N}.
The wedge WD has gap 2^{-m} and denominators 2^{Theta(N)}, so it is not in
the class; FV(n) is in the class and stalls, but vacuously.

WHAT TO DO.
 (1) THE NEGATIVE ATTEMPT, engineered not sampled: take the wedge's
     mechanism (two Max vertices reading long average chains whose values
     differ by a tiny amount that value iteration resolves only after
     2^{Omega(N)} rounds) and ask whether the SAME slowness can be produced
     with values on a coarse grid: a chain of a average vertices whose
     first-passage values are all multiples of 1/D with D = poly(N) yet
     whose two-sided value iteration from the sink payoffs needs 2^{Omega(a)}
     rounds to separate two of them (the iteration's width is about the
     escape probability, not about the denominators: a gambler's-ruin chain
     GR(n) has D = n+1 and mixing time n^2 -- is there a coarse-grid chain
     with EXPONENTIAL mixing time? by lem:denominator-sharp the denominators
     divide 2^a, so coarse values force massive cancellation; find the
     structure or prove it impossible). Then wrap it in the wedge's two Max
     vertices and test EVERYTHING: M1, M2, M2T, M4, M5, M6, BSI, all-switches,
     both firing directions, Z-seeded, at every controlled vertex; report
     the silent-round counts at >= 5 sizes and the growth law.
 (2) THE POSITIVE ATTEMPT: prove that on every stopping game with common
     denominator D some mechanism fires at every value-distinguishing vertex
     within poly(N, D) rounds. Candidates: (a) the slack calculus RUN ON THE
     GRID -- round each entry of Delta_k up to the grid of multiples of 1/D
     (or of 1/(2D)) after each step; prove the rounded calculus is sound
     (an upper bound rounded up stays an upper bound) and that it reaches
     the exact differences in poly(N,D) rounds by the argument of
     thm:alphabet-iteration; this would be a NEW MECHANISM M7 -- define it,
     prove soundness, prove the bound, and then find its stall families
     (which must have D superpolynomial, so the class is exactly what it
     decides); (b) the hybrid with its LP over Q(G) intersected with the
     grid constraints; (c) the simulation preorder M1 with a grid-aware
     clause. For (a): the difficulty is that rounding an upper bound on a
     DIFFERENCE w*(x)-w*(y) up to the grid is sound, but the grid of
     differences is 1/D again; and the calculus's average clause takes
     means of entries, which leave the grid -- decide whether up-rounding
     after the mean preserves the two-sided sandwich of thm:slack-vi-upper
     and speeds the lower side.
 (3) Whatever you find, relate it to thm:few-denominator: a mechanism that
     decides the class in poly(N,D) rounds is a second algorithm for the
     class and its extension beyond the class is the interesting object; a
     genuine stall inside the class shows the calculi are blind to precision
     structure the rounded iteration sees.

REQUIREMENTS. Exact arithmetic; every family at >= 5 sizes with the growth
law; every stall tested against the STANDING RULE. Labels prefixed fd:.
`,
  },
  {
    key: 'bsi-counter',
    model: 'opus',
    title: 'Best-response restart and bidirectional improvement: a superpolynomial family with non-constant drivers, or a polynomial bound',
    brief: `
YOUR ROUTE IS THE NEWEST MECHANISM'S ROUND COUNT. Read def:bsi through
rem:bsi (l.7825-8500), prop:bsi-br and rem:bsi-br (8049, 8101),
thm:bsi-tracks, def:readout-cascade, thm:readout, prop:leapfrog, rem:readout,
lem:same-successor, prop:bsi-normal, prop:q16 (8198-8450),
prop:closed-now-or-never and rem:closed-now-or-never (3800-3880),
lem:rise-bound and cor:peak-sharp (3960-4000), thm:impedance (3543),
lem:dyadic-row (980). The round-15 rbr route's code is ${PREV}/rbr-rounds/
(read-only: brlib.py = R_BR and BSI in both variants, family.py = RD(n) and
SD(K)); its result record is ${REPO}/rounds/round15/results/11_*.json and
its two audits 17_*.json and the significance audit among 21-43_x.json;
the root agent's checks are ${SCRATCH}/myver/rd_sd_check.py, sd_check.py,
q16_check.py, rbr_gsharp.py, rbr_small.py.

THE STATE. R_BR is a switching rule (def:rule) halting only at an optimum;
no barrier covers it; no superpolynomial family is known; it can be slower
than all-switches by a factor Theta(N) (RD(n)); a Max vertex can be switched
K times by all-switches on O(K^2) vertices (SD(K), one player); both BSI
tracks must be long (thm:bsi-tracks). The rbr route's proposed counter --
v_j -> (a_j, b_j) with b_j a CONSTANT gadget and u_j -> (v_j, Theta_j), with
val_sigma(v_j) and val_sigma(Theta_j) crossing 2^{n-j} times -- was REFUTED
by its auditor: a Max vertex one of whose options is constant switches at
most twice along any run (prove this yourself first; it is a one-paragraph
consequence of lem:switch and the monotonicity of val_sigma along a run).
The route's own next step was: graft SD(K)'s observer (which switches at
every round) onto RD(n)'s cascade (which forces one switch per round) and
make Theta_j read the LOWER bits, so the drivers of the leapfrog at u_j are
recurring lower bits rather than fresh vertices.

YOUR TASK.
 (DOWN) Build a family on which R_BR (or def:bsi) takes superpolynomially
     many rounds. The mechanism you need: a vertex v_j whose endorsement by
     Min's best-response value val^tau flips many times because Min's best
     response itself changes as lower bits count -- so BOTH options of v_j
     must be non-constant, and Min's best response at u_j must depend on
     the lower bits (prop:q16's c_10 reversals show a Min vertex can be
     reversed four times; understand WHY from the Q_16 data and scale it).
     Note prop:bsi-br's freedom: R_BR may take ANY best response; a family
     must be slow for EVERY choice, or you must state the tie-breaking rule
     and count it as part of the rule. Verify at >= 5 sizes in exact
     arithmetic, both variants, from a stated start, and give the growth
     law with a proof or with the recurrence measured. Since a superlinear
     family for R_BR on ONE-PLAYER games is impossible (R_BR = all-switches
     there), your family has Min vertices; keep it stopping.
 (UP) Or prove a polynomial bound for R_BR on a nontrivial class: games
     with ONE Min vertex (then val^tau has two candidates; the veto compares
     against one of two fixed one-player value functions -- bound the number
     of rounds by the number of times the best response changes, times the
     one-player run length, or refute by an instance where one Min vertex
     already makes R_BR slower than all-switches by more than a constant);
     self-dual games (prop-selfdual of round 14 says BSI collapses to a
     one-sided rule MR there); or the general case through the lexicographic
     potential (M,|Z|) of cor:bsi-levels by bounding the number of levels M
     takes -- a polynomial bound there is (Poly-Rule) and hence the target;
     say so if you reach it.
 (SHARP) Answer the exact question thm:bsi-tracks leaves: is B (the number
     of Min-active rounds) bounded by a polynomial in N times the number of
     distinct Min best responses visited? Any inequality relating the two
     tracks beyond R <= m+(m+1)B is progress.

REQUIREMENTS. Exact arithmetic; productive rounds counted; the variant named;
both firing directions when a decision is claimed. Labels prefixed bsc:.
`,
  },
  {
    key: 'one-player-howard',
    model: 'opus',
    title: 'Howard with two actions: a superlinear all-switches family of one-player stopping SSGs, or a polynomial bound',
    brief: `
YOUR ROUTE IS THE ONE-PLAYER HALF OF THE PIVOT ON THE GAME SIDE. Do not
read the AUSO/Holt-Klee sections first; work from games. Read thm:ladder and
rem:ladder (6759-6900), thm:switch-count and rem:grid-per-vertex (6900-6950),
sec:allsw-laws (3749-4300: thm:peak-law, cor:peak-sharp, lem:rise-bound,
prop:closed-now-or-never, rem:closed-now-or-never, lem:max-tree, cor:law-u,
thm:component-bound), thm:impedance (3543), prop:leapfrog (8299),
thm:zero-timer and cor:gate (5954-6045), lem:dyadic-row (980). The round-15
lane route's code is ${PREV}/lane-reuse/ (read-only; its result record
${REPO}/rounds/round15/results/08_*.json) and the round-14 free-search-14
lane code is ${SCRATCH}/root16/r14routes/free-search-14/ (build.py,
t_lane.py, fastsw.py); the exact one-player normal forms with runs of
length 9 and 12 at m = 5, 6 are in ${PREV}/howard-cube/ and the root agent's
${SCRATCH}/myver/hc_oneplayer.py rebuilds and verifies them.

THE FACTS. For one-player stopping SSGs (Vmin empty) all-switches is
Howard's policy iteration on a transient 2-action MDP with reachability
reward ((v3), unverified as a formal dictionary; prove the direction you
use). Known one-player runs: the ladder L_n has length n on 2n+2 vertices;
the chain RC(k) attains L = N-2; SD(K) switches one vertex K times on O(K^2)
vertices, so switch counts per vertex are unbounded but its run length is
only O(K); the exact normal forms give runs 9 and 12 at m = 5, 6, so
h*_1(5) >= 9, h*_1(6) >= 12. No one-player run longer than N-2 is known
(rem:grid-per-vertex's question). Every nondegenerate one-player run is at
most h*_HK(m) = 1,2,4,6,11 long at m <= 5. Prior art from memory:
Melekopoglou-Condon (least-index exponential, Howard open); Mansour-Singh
O(2^n/n) for Howard on 2-action MDPs; Fearnley 2010 exponential for Howard
with Theta(n) actions; Hansen-Zwick lower bounds for deterministic
mean-cost cycles; a linear lower bound for constant actions
(Mukherjee-Kalyanakrishnan, as reported). A superlinear binary family is
new even for one player.

YOUR TASK, either direction is a theorem.
 (DOWN) A family of one-player stopping SSGs on N = poly(k) vertices whose
     all-switches run has length omega(N) -- superlinear is the first
     target, superpolynomial the real one. Mechanisms to engineer (not
     sample): (a) two lanes of COPRIME lengths weakly cross-coupled, so that
     the union's switched sets stay distinct while each lane re-runs its
     wave out of phase (the lane route's own suggestion; it needs turnaround
     vertices that read a MIXTURE of all lane vertices so no proper subset
     is a closed configuration); (b) a counter: a Max vertex that is
     switched Theta(K) times by leapfrog (prop:leapfrog's mechanism) used as
     a CLOCK driving a second copy, so that the run length multiplies; (c)
     Fearnley's deceleration binarised: reconstruct from memory the shape of
     Fearnley's MDP (a counter whose bits are set and reset by a timing
     action that postpones), replace its Theta(n)-action states by Max trees
     (lem:max-tree, lag ceil(log2 r)) and its rewards by average chains into
     t1 (lem:dyadic-row), and see whether the postponement survives out-
     degree two (the round-14 objection that it does not was wrong; the
     round-14 law prop:closed-now-or-never says a configuration nothing
     switches into is never re-entered -- your construction must keep every
     counter bit's configuration OPEN by having something switch into it).
     Verify at >= 5 sizes exactly; give the growth law.
 (UP) Or prove all-switches polynomial on one-player stopping SSGs: a
     potential on runs using lem:rise-bound, cor:peak-sharp,
     prop:closed-now-or-never (the first irreversible event), cor:law-u, and
     the fact that the value vector increases strictly; e.g. bound the run
     by the number of closed configurations that become closed, or by the
     number of times the SET of vertices at rest changes in a monotone way.
     A proof of L <= N-2 (rem:grid-per-vertex's question) would already be
     a theorem; a proof of L <= poly(N) answers Melekopoglou-Condon.
 Whatever you prove, state it also in the AUSO language at the end (a
 one-player family of run length L gives h*_1(m) >= L).

REQUIREMENTS. Exact arithmetic; every family built as a game and its run
printed; the growth law at >= 5 sizes. Labels prefixed oph:.
`,
  },
  {
    key: 'fresh-16',
    model: 'opus',
    title: 'Free search: a formulation nobody has tried in sixteen rounds',
    brief: `
YOUR ROUTE IS A FREE SEARCH FOR A FORMULATION OF THE PROBLEM THAT NOBODY HAS
TRIED HERE. You are given the anti-list and a menu of seeds. Read sec:gap's
opening (9852-9930), thm:decide-one-bit (9943), thm:compare-equivalence
and thm:order-determines (sec:selection, 9040-9440), lem:cut (2155),
thm:stopping-transform (942-1223), and the abstract (1-120) -- then decide.

ANTI-LIST (tried, in the paper or dead): every mechanism M1-M6 and BSI;
strategy improvement with any of the seven rules of prop:rules-fail;
random facet; value iteration and its two-sided and rounded forms; the
transport LP over Q(G) and its Lasserre lift; the LCP / interior-point /
handicap route; Newton on x - Tx; entropic/softmax regularisation and
homotopies in the operator, the payoff, the discount, the player strength;
Schur/vertex elimination; Kannan-Theobald rank classes; treewidth and
modulators; the escape class and survival certificates; the value alphabet
and denominators; the permutation/order space (Gimbert-Horn) and sorting
Vavg with abstaining comparators; self-duality at 1/2; the complementary-
cone arrangement; the semialgebraic yes-set and algebraic complexity;
smoothed and average-case analysis; the promise gap; UEOPL; symmetric
improvement; the AUSO pivot and all its realisations; submodularity;
Hamming potentials; TOP (the largest average vertex); forest-count ratios;
double-obstacle / Isaacs formulations; Dinkelbach.

SEEDS (pick at least two, go deep; a seed that dies at a target-equivalent
lemma is reported as such, with the lemma stated exactly):
 (alpha) QUANTITATIVE TO QUALITATIVE. Almost-sure reachability (val = 1) and
     positive reachability (val > 0) are decidable in polynomial time by
     attractor computations (prove it in the SSG model; attribute de Alfaro /
     Chatterjee from memory). Is there a polynomial transformation G, v0 ->
     G', v0' with val_{G'}(v0') = 1 iff val_G(v0) >= 1/2? Try: a repeated
     game in which Max must win a fair comparison against a coin many times
     (the law of large numbers pushes probabilities to 0/1 but only in the
     limit; a finite number of repetitions gives a threshold with error --
     compute the error exactly in terms of the gap 1/2^a of
     lem:denominator-sharp and see whether poly(N) repetitions and an exact
     tie-break at the grid decide); or a gadget game whose value is a step
     function of val_G(v0) at 1/2. Either construct it (then SSG-Value is in
     P: check every step twice) or prove that any such transformation is
     target-equivalent in a precise sense.
 (beta) THE MIXED-MIN LANDSCAPE. For y in [0,1]^k let G^y be G with each Min
     vertex u_j replaced by a biased coin choosing its action 1 with
     probability y_j; V(y) := val_{G^y}(v0) is a rational function, and
     val_G(v0) = min over y of V(y), attained at a vertex of the cube. Study
     V: is it quasi-convex along coordinate lines (it is a ratio of
     polynomials of degree <= 1 in each y_j separately -- a Moebius
     function in each coordinate, so monotone in each coordinate on [0,1]),
     what are its critical points, is coordinate descent from any y a
     polynomial process, does the sublevel set {V <= 1/2} have a structure
     (a union of boxes? a convex set after a transformation?) that a
     separation oracle can exploit? Relate to Hoffman-Karp for Min.
 (gamma) CERTIFICATE SIZE. The coNP witness for val(v0) < 1/2 is a Min
     strategy tau with val^tau(v0) < 1/2, verified by one LP; the NP witness
     a Max strategy. Ask for witnesses with SHORT verification: a tau under
     which the Max-optimal LP has an integral or small-support dual, a pair
     (sigma,tau) with a certificate x = val_{sigma,tau} verifiable by
     T x = x in linear time (that is what thm:qp's certification uses), or a
     certificate that survives self-reduction (thm:decide-one-bit's retyping)
     -- and whether the SET of certificates has a lattice structure that a
     polynomial search can traverse.
 (delta) THE EASIEST BIT. thm:decide-one-bit needs only ONE decidable
     controlled vertex per round, after which it is retyped. Prove or refute
     an existence theorem: in every stopping SSG some controlled vertex,
     recognisable in polynomial time, is decided by some sound polynomial
     test -- candidates: a vertex both of whose successors lie in a subgame
     solved by lem:cut; the controlled vertex of largest value (thm:top
     says finding the largest AVERAGE vertex is target-equivalent -- is the
     largest CONTROLLED vertex different?); the vertex nearest the sinks in
     the acyclic C-subgraph of lem:trapchar; the vertex whose two options
     differ most under the Z-seeds. A refutation is an instance in which NO
     controlled vertex is decided by M1-M6, BSI or all-switches within p
     rounds -- which by thm:seed-dichotomy is a superpolynomial all-switches
     family; say so if that is what you find.
 (epsilon) YOUR OWN. Anything genuinely absent from the anti-list, stated as
     a lemma with a proof or an exact instance.

REQUIREMENTS. Exact arithmetic; every claimed reduction checked on random
AND engineered instances; every dead end reported with the exact statement
it died at. Labels prefixed fs16:.
`,
  },
  {
    key: 'min-budget',
    model: 'opus',
    title: 'The Min-budget hierarchy h*_k(m): how much bottom-antipodal height k Min vertices buy',
    brief: `
YOUR ROUTE DEFINES AND ATTACKS A NEW PARAMETER OF THE PIVOT. Read
def:improvement-uso and prop:allsw-auso (4280-4400), prop:oneplayer-lp
(4752), prop:auso-seven (4671-4752, G# with 4 Max and 2 Min, height 7),
prop:b2-realised (5288, 5 Max and 1 Min, height 10), sec:readouts in full
(6332-6537, especially thm:readout-realise, thm:min-count and its proof:
along a run, Min's best response tau_sigma partitions the Max cube into at
most 2^k pieces on each of which the orientation is that of an HK AUSO),
sec:projection (6537-6759: the profile cube and its sink projection),
thm:bsi-tracks (8198), rem:four-ceilings (6303), prop:hkfive (5781),
thm:b2-walk (5867). Code: ${SCRATCH}/solo/my_D.py (HK test),
${SCRATCH}/solo/census/classes4.txt, ${REPO}/scripts/blowup/ (B2 files,
hstar_all.c), ${PREV}/sink-projection/ and ${PREV}/monotone-lemma/
(read-only).

DEFINITION. h*_k(m) := the greatest BA height of the improvement
orientation of a nondegenerate stopping SSG with m Max and k Min vertices.
Known: h*_0(m) = h*_1(m) of the paper = 1,2,4,6,>=9,>=12 (<= h*_HK(m) =
1,2,4,6,11,>=12); h*_2(4) >= 7 = h*(4) (G#); h*_1(5) >= 10 (B^2);
h*_k(m) <= h*(m) = 1,2,4,7,12 for m <= 5. thm:min-count: k >=
log2 chi_HK(s). The class min(m,k) = O(log N) is trivially in P, so this
hierarchy is about the RULE, not about P; but the pivot's family, if it
exists through the blow-up, has k growing with the level, and a bound
h*_k(m) <= f(k) poly(m) for HK-polynomial h*_HK would say Min vertices are
what a superpolynomial family must spend.

YOUR TASK.
 (UP) Prove an upper bound h*_k(m) <= F(k, h*_HK(m)) with F polynomial in
     h*_HK(m) for fixed k -- e.g. (2^k) h*_HK(m), or (k+1) h*_HK(m), or
     h*_HK(m) + k m. The run is a BA walk on an outmap that is, on each of
     at most 2^k pieces S_tau = {sigma : tau is a best response}, the outmap
     of an HK AUSO t_tau; the pieces are not faces; the walk can leave and
     re-enter a piece. Use the monotonicity of Min's best-response values
     along a run (val_sigma increases; the best response to a larger sigma
     ...), thm:bsi-tracks' counting, cor:law-u, and the profile cube (the run
     lifts to a walk on the profile cube where Min's coordinates are always
     at a face sink): does the lifted walk have a potential the Max cube
     lacks? Even a bound for k = 1 -- h*_1(m) <= 2 h*_HK(m) + c, say -- is a
     theorem; test any conjectured bound exactly at m <= 5 against every
     realised orientation you can get (G#: h = 7 with k = 2 against
     h*_HK(4) = 6; B^2: 10 with k = 1 against 11).
 (DOWN) Show one Min vertex buys more than the bound you can prove: is the
     h*(5) = 12 orientation of prop:hstar-five realised with k = 1 (a
     readout system of order (5,2))? thm:min-count needs chi_HK = 2 for
     that: compute chi_HK of the h*(5) = 12 witness and of B^2 and of the
     other height-11/12 5-cube classes (a set-cover over HK 5-cube AUSOs
     agreeing pointwise -- use the completion enumerator hstar_all.c and
     the HK test); if chi_HK = 2, attempt the realisation BY DESIGN in the
     readout formulation (fix which Max strategies get which best response
     from the two-piece structure, then it is an LP per piece); if chi_HK >
     2 you have proved that k = 1 does not reach h*(5). Then do the same
     for B^3 (7-cube): chi_HK(B^3) decides whether the "+1 Min per level"
     of the gadget route is forced.
 (STRUCTURE) Characterise the pieces: which subsets of the Max cube can be
     the set S_tau of strategies to which a given tau is a best response
     (is it always an up-set or down-set in some coordinate order? a union
     of faces? convex in the cube metric?). A structural theorem here
     restricts the pivot's family and is progress in either direction.

REQUIREMENTS. Exact arithmetic; every orientation printed with its
USO/acyclic/HK/height data; every game verified from the game. Labels
prefixed mb:.
`,
  },
  {
    key: 'fresh-16-alg',
    model: 'opus',
    title: 'Free search, algorithmic: an algorithm with a proof, or its exact obstruction',
    brief: `
YOUR ROUTE IS A FREE SEARCH FOR AN ALGORITHM. It must end with an algorithm
and a complete proof of a bound, or with the exact obstruction as a theorem
or a target-equivalent lemma. Read sec:gap (9852-9930), sec:randomfacet
(9496-9852), thm:profile-uso and prop:lcp (6537-6759), thm:qp and thm:tarski
(2953-3140), thm:contraction and thm:stopping-determinacy (706-942),
thm:alphabet-iteration (sec:alphabet), rem:lcp (12068), and the abstract.

ANTI-LIST: everything in the fresh-16 anti-list of this round, which you
must reconstruct from the paper's section list and from the DEAD list
above; in particular do NOT propose strategy improvement with a new
switching rule unless you can prove a bound (seven rules fail, all-switches
is the pivot, R_BR and BSI are open and have their own route this round).

SEEDS (pick at least two):
 (a) RANDOM FACET ON REALISABLE CUBES. Ludwig's e^{2 sqrt n} bound is for
     abstract AUSOs and is tight there (Matousek's cubes). SSG-realisable
     orientations are a 2^{O(N log N)} subset; one-player ones are LP
     orientations of the occupancy polytope (prop:oneplayer-lp); two-player
     ones are sink projections of P-matrix LCP orientations
     (prop:projection). Is random facet, or a DERANDOMISED facet order
     reading the game (e.g. facets ordered by the first-passage rows),
     polynomial or at least e^{O(n^{1/2 - c})} on realisable cubes? Gaertner
     showed (from memory) that Matousek's hard cubes that are LP-realisable
     are easy; Friedmann-Hansen-Zwick gave subexponential lower bounds for
     random facet on actual LPs and MDPs with many actions. Reconstruct what
     you can, then look for a proof using the readout structure
     (sec:readouts: one player buys affine readouts) that the recursion's
     expected depth is polynomial on affine-readout orientations, or an
     explicit one-player family on which random facet is subexponential.
 (b) LEMKE ON THE PROFILE LCP. The profile cube is the Stickney-Watson
     orientation of LCP(M,q) with M = E(I-Q_1)(I-Q_0)^{-1}E, a P-matrix with
     a special shape (prop:lcp). Lemke's algorithm terminates on P-matrix
     LCPs; its path length is exponential on Murty's examples. Is Lemke's
     path polynomial on SSG matrices M? Implement Lemke exactly, run it on
     every hard family in the paper (WD, CC, G#, B^2, the ladder, H_m, P_D),
     count pivots against N, and either find a family with superpolynomial
     Lemke paths (engineer it from Murty's structure inside the SSG shape)
     or prove a bound from the substochastic structure of Q_0, Q_1.
 (c) TARSKI WITH CONTRACTION. T is monotone and nonexpansive on [0,1]^N and
     T^N is a contraction on stopping games with a unique fixed point.
     Tarski fixed-point algorithms need O(log^{ceil((N+1)/2)} of the grid
     size) queries in general (Fearnley-Palvolgyi-Savani, Dang-Qi-Ye, from
     memory) and that is not polynomial. Does UNIQUENESS plus the
     contraction rate 1-2^{-a}, plus the value alphabet's grid, reduce the
     query count -- e.g. a binary search on ONE coordinate combined with the
     monotone dependence of the rest (thm:qp does this at a separator of
     bounded size; the whole game is a separator of size N); or a
     dimension-reduction: fix the values on Vmax only (m coordinates), the
     rest is a one-player game for Min solved by LP, and search the
     m-dimensional monotone map -- is that map's Tarski search polynomial
     for the SSG shape (it is the readout system of sec:readouts read the
     other way)?
 (d) ORDER FIRST. thm:order-determines: the preorder of the a+2 average
     values determines w*. Sorting needs O(a log a) comparisons; each
     comparison is target-equivalent in general (prop:no-halving), but a
     comparison is EASY when M1-M6 decide it. Design an adaptive sorting
     strategy that only ever asks comparisons the mechanisms can answer,
     with the game simplified between questions (retyping decided vertices,
     thm:decide-one-bit), and either prove it always finds an easy
     comparison (an existence theorem -- fresh-16's seed delta approaches it
     from the vertex side; you approach it from the ORDER side: e.g. the
     two average vertices of extreme value, or two adjacent in the true
     order) or exhibit a game where no comparison between average vertices
     is decided by any mechanism after Z-seeding (test with the harness).
 (e) YOUR OWN.

REQUIREMENTS. Exact arithmetic; every algorithm implemented and checked
against brute force on random AND engineered instances; every bound proved
or the missing statement given exactly. Labels prefixed fsa:.
`,
  },
]

const PAPER_SECTIONS = [
  { key: 'width', lines: '2790-3190', what: 'the end of sec:alphabet (prop:fv-stall and the paragraph after it, rem:alphabet-equivalence) and ALL of sec:width, integrated in round 15 and never audited as paper text: def:width, lem:payoff-transfer, lem:cut-sign, thm:tarski, lem:round-recover, thm:modulator (its freezing-closed classes, the N^{O(mu)} bound, the search for X, the certification by T_H w = w and the stopping hypothesis), thm:qp (the balanced separator argument, the query count, the bit-size claim, the Tarski search on lem:cut\'s cut map), rem:fold-width (the 2^{(N-2)/6} pieces and the treewidth/pathwidth claims), prop:modulator-family (M_n: stopping, reachability, val(h), mu_max = 1, the feedback number, membership in no other class -- rebuild M_n for n <= 5 and check every clause), and the amortisation paragraph' },
  { key: 'laws', lines: '3543-3674 together with 3749-4300', what: 'thm:impedance, cor:selfread (round 15) and rem:impedance; then sec:allsw-laws with the round-15 insertions: lem:monotone-law, rem:monotone-law-general, prop:closed-now-or-never, rem:closed-now-or-never, lem:max-tree (the binarisation lag), thm:peak-law, cor:peak-sharp, lem:rise-bound (the rise/gap distinction -- check the proof: subtract x(u) >= p.x + q from y(u) = p.y + q, substochastic row, 1 - p_u > 0 by stopping), cor:no-return, cor:isolated, cor:law-b, cor:antichain, def:maxreach, thm:component-bound, thm:bounded-components, prop:k1-family, prop:overshoot-small, prop:zero-ties, rem:allsw-laws, def:improvement-uso, lem:sw' },
  { key: 'blowup', lines: '5034-5617', what: 'lem:hstar-super, prop:D-quadratic, rem:D-quadratic, thm:blowup, rem:blowup-measured (the translation-vector claims, the heights, the "single coordinate" statement and which coordinate), prop:b2-realised (REBUILD the 138-vertex game from the printed normal form with lem:dyadic-row, verify stopping, nondegeneracy, USO, acyclicity, outmap = B^2, the run 12,19,13,17,8,16,0,7,1,5,4 -- the committed files are scripts/blowup/B2_small_*.json and verify_b2.py but you must recompute from the PRINTED rows), def:reduced-rows, prop:rows-turn, cor:b2-rows, lem:crossing, cor:b2-min (the four forbidden pairs), cor:parity-unreadable, prop:xor, thm:alternation-bits, rem:blowup-realise (every number in it, and whether its statement of the open question is consistent with prop:b2-realised and with thm:min-count), rem:hk-survey' },
  { key: 'ties-deformed', lines: '5617-6332', what: 'sec:ties: lem:tie-perturb, cor:one-tie, lem:seven-flat, thm:no-seven (reconstruct: flat classes distinct, corner resolution of height 7 unique, the (F1)-(F4) exhaustion, one flat incidence, the perturbation LP), cor:hstar-one, prop:hkfive (h*_HK(5) = 11: the enumeration counts 347640 / 480 / 0 HK and the height-11 witness -- verify the witness is USO, acyclic, HK, height 11), lem:tie-partner, lem:two-ties, thm:b2-walk (the 1897 / 875 / 0 counts), prop:no-linear-tiebreak, thm:zero-timer, cor:gate; then sec:deformed: def:deformed, lem:deformed-rigid, thm:deformed-flat (the BA-flatness of deformed products -- reconstruct the proof), prop:km-measured, lem:stack, lem:blowup-faces, cor:blowup-parity, cor:blowup-transl (every B^k, k >= 2, non-HK), prop:oneplayer-runs (rebuild the m = 5, 6 normal forms as games: nondegenerate, stopping, runs 9 and 12), rem:four-ceilings (every entry of the table against the result it cites; HK(6) >= 12 and HK(7) >= 13 by the product with the height-11 witness first and z = 1: recompute)' },
  { key: 'readouts-projection', lines: '6332-6950', what: 'sec:readouts: def:readout, lem:readout, lem:readout-reduce, def:readout-system, thm:readout-realise (both halves; the size counts 2m(r-1) Min and 2mr(m+1)D average vertices; the delta-leaky and dyadic hypotheses), thm:min-count (the proof through best responses and lexicographic perturbation; the chi_HK = 2 claim at B^2), prop:m3-realised (all 18 classes: rebuild at least the two non-HK realisations from whatever the text gives and verify); sec:projection: def:profile-orientation, lem:profile-trichotomy, lem:profile-faces, thm:profile-uso, lem:survival-contract, prop:lcp (the P-matrix proof from first principles and the Samelson-Thrall-Wesler citation), prop:projection (acyclic even when the profile cube is cyclic), prop:seven-k1 (verify the printed HK acyclic 5-cube USO of height 7 projects to s_{G#}); then the ladder block: def:ladder, thm:ladder, rem:ladder, thm:switch-count, rem:grid-per-vertex (RC(k) attains N-2; the sum bound), cor:no-height' },
  { key: 'bsi-top', lines: '8198-8450 together with 9380-9440 and 970-1010', what: 'thm:bsi-tracks (both inequalities, both variants; the counting argument), def:readout-cascade, thm:readout (RD(n): rebuild for n <= 5, all-switches one round from EVERY start, R_BR exactly n rounds for EVERY best response, BSI 2n), prop:leapfrog (SD(K): rebuild for K = 2..5 from the printed parameters, one player, stopping, vertex counts 20,31,41,56,66, the K switches of v), rem:readout, lem:same-successor (the strict clause), prop:bsi-normal, prop:q16 (288 vertices; c_10 reversed four times, three L-ties); thm:top (the reduction: reference chain and boost chains; target-equivalence in both directions); lem:dyadic-row (the chain realising an arbitrary dyadic substochastic row, its size)' },
  { key: 'front', lines: '1-392 together with 13432-13710', what: 'the abstract, the introduction, "what is proved here, and what is not", and the summary READ AGAINST THE BODY after the round-15 integrations: every claim must match the statement it cites with the same hypotheses, the same numbers (97 vertices for G#, 138 for the B^2 realisation, the four ceilings table, the list of eight polynomial classes incl. modulator and quasipolynomial treewidth, the six mechanisms, the count of imported facts: thm:determinacy, Holt-Klee, Legendre, Samelson-Thrall-Wesler -- are there others, e.g. the Tarski search, lexicographic perturbation, Amenta-Ziegler, the Etessami et al. algorithm?), and the same strength (measured vs proved: h*_HK(5) = 11 is now proved, h*_1(4) = 6 proved, the realised levels, the corrected thm:seed-dichotomy, the corrected window barrier scope, cor:slack-stalls\' pair-test scope, prop:fv-stall\'s vacuity). List every mismatch and every omission of a round-15 result the summary should name' },
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
you need its exact statement (grep -n 'label{NAME}' then sed). This material
was integrated in round 15 from route results, after the routes' own audits,
and has NEVER been audited as paper text: integration errors (a hypothesis
dropped in transcription, a number copied from the wrong table, a label
pointing at the wrong result, a "verified" that was verified by the route
and not by the manuscript) are exactly what you are looking for.

# Your task

1. PROOFS. For every theorem, lemma, proposition and corollary in your range,
   reconstruct the proof step by step. Report every step that is asserted
   rather than proved, every hypothesis used but not stated (stopping?
   nondegeneracy? sink payoffs pinned? Min present? dyadic?), every citation
   of another label whose statement does not actually give what is used, and
   every quantifier error. Sinks, ties, empty sets and the one-vertex game
   are where this manuscript's errors have lived: check them.
2. NUMBERS. For every explicit instance, table, count or vertex count in
   your range that can be recomputed in under an hour, RECOMPUTE IT in exact
   rational arithmetic with your own code in ${SCRATCH}/paper-audit-${s.key}/
   (the harness is at ${SCRATCH}/root16/ and ${SCRATCH}/solo/; the root
   agent's own verification scripts are in ${SCRATCH}/myver/ and
   ${REPO}/scripts/round15-verify/ -- you may READ them to see what was
   checked, but you must recompute from the manuscript's statement, not
   from their output). Report every mismatch with both numbers. Do not skip
   the small ones; a wrong count is a defect.
3. CONSISTENCY. Every \\Cref in your range must point at a result that says
   what the text claims it says. Every remark that qualifies a result
   ("measured, not proved", "one direction only", "off the sinks") must be
   consistent with the result's statement and with the abstract/summary.
   Every "we verified on K instances" must say what was varied.
4. PRIOR ART. Anything in your range that is standard published mathematics
   presented as new is a defect; about twenty such cases have been caught.
   Name the source if you know it. A rediscovery already labelled is fine.
5. OVERSTATEMENT. Where the text claims more significance than the
   mathematics supports (a "barrier" covering no real rule, a "class" that
   is a restatement, a "family" measured at two sizes), say so.

Report findings with severity fatal / major / minor / note, each with the
LINE NUMBER, the label, the defect in one sentence and the evidence (your
recomputation, the counterexample, or the exact quote that is wrong). "sound"
is TRUE only if nothing fatal or major survives. Being unable to find a defect
in a result you did not check is not grounds for sound = true; list what you
checked and what you did not. Put target = 'frontier.tex ${s.key} (lines
${s.lines})'. Write nothing into ${REPO}.
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
   The harness is at ${SCRATCH}/root16/ and ${SCRATCH}/solo/. If a claimed
   family, instance or realisation does not reproduce, that is a FATAL
   finding and you must give the discrepancy explicitly. If the route claims
   a run-length table (all-switches, BSI, R_BR, Lemke pivots, Tarski
   queries), recompute at least three of its rows independently. If the
   route claims a realisation of an orientation, rebuild the game from its
   normal form or successor lists and verify the outmap from the game.
3. Hunt for the project's standing errors: computing val_sigma by greedy policy
   iteration in a non-stopping game; dict-literal rows collapsing when a
   vertex's two successors coincide; fresh vertices colliding with the sink
   indices; excluding t0 from the trap Z_sigma; using the PAIR test instead of
   the own-successor test of rem:own-successor; omitting the Z_0/Z_1 seed;
   calling a vacuous stall (equal successor values) a stall; measuring a
   mechanism only on instances where the parameter it turns on is constant;
   separating a family from a class using vertices UNREACHABLE from the
   start; unpinned sink payoffs in an iteration bound; counting a
   non-productive terminal round; a non-dyadic "witness" never built as a
   game; a "polynomial class" whose member is already inside thm:few-avg,
   thm:few-escape, thm:kacyclic, thm:bounded-components, thm:escape-class,
   thm:few-denominator, thm:modulator or the trivial min(m,k) = O(log N).
4. Check every claimed IMPLICATION between the route's own results, and every
   citation of frontier.tex, against the actual text of the label cited.
5. If the route claims a decision rule, a barrier, a lower bound or a
   polynomial algorithm, check it against THE STANDING RULE and against the
   proved equivalences: does any step assume an oracle that is
   target-equivalent (thm:compare-equivalence, thm:decide-one-bit,
   prop:no-halving, cor:wrong-equivalence, rem:transport-objective, rem:bsi,
   thm:top)?

Report findings with severity fatal / major / minor / note. "sound" is TRUE only
if nothing fatal or major survives your checking. Being unable to find a defect
in a result you did not check is not grounds for sound = true; say what you
checked. Write nothing into ${REPO}.
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
   thm:short-path, lem:cut, lem:duality, thm:seed-dichotomy, lem:rise-bound
   or thm:bsi-tracks as new. Name the label if so. Also flag anything that is
   standard published mathematics presented without acknowledgement -- about
   twenty such cases have already been caught here (see the prior-art list
   above). A rediscovery that the route itself labels and attributes is NOT
   a defect; an unlabelled one is.
2. IS IT CIRCULAR OR VACUOUS?
   - Does a claimed algorithm assume an oracle that is target-equivalent? The
     proved equivalences are thm:compare-equivalence, thm:decide-one-bit,
     prop:no-halving, cor:wrong-equivalence, rem:transport-objective, rem:bsi
     and thm:top.
   - Does a claimed BARRIER rule anything out, or is its hypothesis so strong
     that no real algorithm satisfies it? Name which of M1, M2, M2T, M3, M4,
     M5, M6, def:bsi, R_BR and all-switches it actually covers. A barrier
     covering none of them is nearly worthless and must be labelled as such.
   - Is a claimed polynomial CLASS nonempty and not already inside thm:few-avg,
     thm:few-escape, thm:kacyclic, thm:bounded-components, thm:escape-class,
     thm:few-denominator, thm:modulator or the trivial min(m,k) = O(log N)?
     Demand an explicit member outside all of them, verified on the subgame
     reachable from the start vertex.
   - Is a claimed lower-bound FAMILY genuinely a family (a build(n) with a
     proved or at least measured growth law at >= 5 sizes), stopping, and
     legitimate in the sense of def:ssg (fair coins, out-degree two)? Is a
     claimed realisation a GAME (dyadic, built, verified from the game)?
   - Does a claimed cost datum (vertices, bits per level) rest on one step?
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
   which are not. "Worse" is a legitimate and useful verdict. Write nothing
   into ${REPO}.
`,
  },
]

log(`Round 16: ${ROUTES.length} routes, all on Opus 5: ${ROUTES.map(r => r.key).join(', ')}; two audits each on Opus 5; ${PAPER_SECTIONS.length} paper audits on Opus 5.`)

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\n\n# YOUR ROUTE: ${r.title}\n${r.brief}\n\n` +
    `Work in ${SCRATCH}/${r.key}/ (create it). Copy the harness from ` +
    `${SCRATCH}/root16/ (and what you need from ${SCRATCH}/solo/) into your own ` +
    `directory before using it. You have a long budget: think hard, write code, ` +
    `verify, iterate. Your final output is the structured object and it is the ` +
    `ONLY thing that reaches the root agent -- make it complete and ` +
    `self-contained, put every explicit instance (successor lists or normal ` +
    `forms) into files in your directory AND name them in the result, and put ` +
    `the path of your code directory in code_dir.`,
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
log(`Round 16 complete: ${good.length}/${ROUTES.length} routes returned; ${paperGood.length}/${PAPER_SECTIONS.length} paper audits returned.`)
return { round: 16, routes: good, paper: paperGood }
