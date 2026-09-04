export const meta = {
  name: 'ssg-round17',
  description: 'Round 17 on the SSG value problem under the tightened brief (rounds/round17/BRIEF.md): seven object-changing routes on Opus 5 against the post-round-16 frontier (209 pp), each audited for correctness and novelty on Opus 5, plus ONE paper audit of the round-16 diff on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
    { title: 'Paper audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/d1fe2115-9b72-4784-bb94-87421ac1106c/scratchpad'

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

${REPO}/frontier.tex is a 209-page LaTeX development of 471 numbered
results (16149 lines) built over sixteen multi-agent rounds and one solo
round by the root agent. Every claim in it is proved and every negative
claim carries an explicit instance verified in exact rational arithmetic.
It contains NO polynomial-time algorithm for the general problem and
claims none. Read the parts you need with grep/sed; do NOT read the whole
file. THE INVENTORY ${SCRATCH}/round17/inventory.txt lists every numbered
result as "L<line> <env> <label> :: <title>", grouped by section: read it
in full FIRST (it is short) and use it for the novelty pre-check below.
Sections and their first lines: Introduction (l.251); The problem (l.253); What is proved here, and what is not (l.331); The Shapley operator (l.418); Stopping games (l.732); The quantitative stopping transformation (l.968); A polynomial special case (l.1250); The value alphabet (l.2394); Width: the search is quasipolynomial, the tables are not (l.2909); The structure of the optimal set (l.3299); Exactly how much a single switch gains (l.3652); Composition, and an energy identity (l.3787); Refutations and barriers (l.3955); The all-switches rule does not dominate (l.3961); Ties in one-player games (l.6110); Deformed cubes, and why the blow-up leaves the Holt--Klee class (l.6546); Gluing facets, the sink lift, and the Holt--Klee ceiling at $m=6,7$ (l.6861); One player: Howard's rule with two actions, sign-definite games, and stacking (l.7271); Readouts: what a game presents to its Max vertices (l.7599); The profile cube and its sink projection (l.7920); Lemke's algorithm as a bias homotopy (l.8148); A rule that needs exponentially many switches (l.8521); The induced orientation of the two-player cube can be cyclic (l.10517); Value iteration is exponential already without players (l.10621); Improving switches need not point toward the optimal set (l.10719); The selection problem is the whole problem (l.11043); What a certificate would look like (l.11445); A subexponential upper bound (l.11501); Subcubes, subgames and dead coordinates (l.11520); The algorithm and its correctness (l.11585); The expected number of switches (l.11646); The remaining gap (l.11857); A global mechanism that beats locality (l.12180); Adding arithmetic: the slack calculus (l.12419); A multiplicative calculus, and why it stops in the same place (l.13061); The branch-compensation barrier (l.13504); Seeding from policy evaluation (l.13642); Freezing one vertex: the response map folds (l.14404); Coupling the two: the transport--slack hybrid (l.14502); A hybrid stall inside the few-denominator class (l.15045); The own-successor rule, and a wedge that defeats it (l.15517); Summary (l.15837).

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


# ROUND-16 ADDENDUM (integrated 2026-09-03/04; the digest above predates it)

Labels added in round 16 -- read their statements before working near them:
prop:forest-k1, prop:modulator-family, sec:composition, def:gate, lem:gate, thm:two-exit, thm:energy, rem:no-amplification, prop:blowup-height, lem:layer-order, rem:b2-anatomy, rem:parity-b2, prop:parity-readable, prop:b3-outer, lem:deformed-rigid, lem:facet-gluing, prop:sink-lift, prop:hk-records, prop:blowup-readout, prop:tstar, prop:hk-doubling-measured, prop:oneplayer-plus-one, sec:oneplayer-howard, rem:oneplayer-dictionary, def:signdef, thm:signdef, rem:signdef, def:balanced, lem:balance, thm:stack, cor:stack-family, rem:stack-measured, prop:hstar-one-five, prop:hstar-one-eight, prop:oneplayer-census-small, prop:pieces-measured, rem:hk-defect, prop:m3-one-min, sec:bias, def:bias, thm:lemke-homotopy, cor:bias-algorithm, rem:bias-attribution, prop:bias-one-improving, prop:bias-shadow, prop:bias-two-nonmono, lem:bias-path-lp, rem:bias-families, prop:bias-witnesses, rem:bias-gap, lem:double-br, lem:clamp-reverses-once, thm:reorder, cor:clamp, rem:clamp, prop:w2, rem:rbr-programme, prop:qualitative, def:cv, prop:cv-values, lem:cv-lift, thm:cv-lower, cor:cv-class, lem:hybrid-narrow, rem:hybrid-narrow, rem:cv, prop:cv-measured.
Headlines: h*_HK = 1,2,4,6,11,>=14,>=20 with a +1 law per dimension
(prop:sink-lift); h*_1 = 1,2,4,6,>=10,>=12,>=13 with its own +1 law
(prop:oneplayer-plus-one) and the 7k/12k stacking family capped by Fekete
(thm:stack, cor:stack-family); the blow-up height is exactly 2h+2
(prop:blowup-height); B^3's outer half is realised on 194 vertices, its
translated layer is not (prop:b3-outer); the blow-up doubles and stays
Holt-Klee at m=4,5 with a non-parity readout, and (T*) stops it on every
tall seed (prop:blowup-readout, prop:tstar); both non-HK 3-cube classes
are realised with ONE Min vertex (prop:m3-one-min); Lemke on the profile
LCP is a bias homotopy (sec:bias, thm:lemke-homotopy, cor:bias-algorithm;
on one player the shadow-vertex path of the occupancy polytope); W_2
(prop:w2) and the clamp bound (cor:clamp); composition: a plugged-in
subgame is a (p,q)-gate (lem:gate), the energy identity sum N_v Delta_v^2 =
4w(1-w) (thm:energy), two-exit contraction (thm:two-exit); the qualitative
sets inside the model (prop:qualitative); CV(e,s) (def:cv .. prop:cv-measured):
a one-player family with D(G) = 2^s constant and one value-distinguishing
Max vertex of gap 1/D at which -- and at every controlled vertex -- the
Z-seeded own-successor hybrid is silent 2^{Omega(N)} rounds by a proved
convex-certificate chain, while the ratio calculus M6 is NOT stalled there
(fires via clause (ii) at rounds 12,22,39,74). Every stall found so far
(H_m, CC, WD, CV) is decided at round zero by the simulation preorder M1
and by the one-round seeded calculus M(1,0), and thm:seed-dichotomy says
any instance defeating the seeded rule with polynomially many improvement
rounds is one on which all-switches itself runs superpolynomially long.
The paper's out-degree-two model is what keeps that open: the exponential
lower bounds for all-switches / Howard in the literature (Friedmann,
Fearnley, Christ-Yannakakis; from memory, unchecked) use Theta(n) actions
per state, and whether they binarise is undecided here.

# The rules of this round (tightened on the user's instruction; read twice)

0. THE OBJECT. Your route CHANGES THE MATHEMATICAL OBJECT. You are not asked
   for another switching rule, another propagation calculus, another
   measured row or another realisation search. You are asked to attach the
   problem to an object the paper does not yet own and prove something
   about the problem THROUGH that object. If your object collapses back
   into one the paper owns, say so; that is a result if you PROVE the
   collapse and a dead-end if you merely observe it.
1. RIGOUR. Return concrete theorems, constructions, equations or
   counterexamples. Status reports and "this step is routine" are rejected.
   If you cannot prove a step, mark it GAP and state the missing statement
   EXACTLY, in one self-contained sentence.
2. NOVELTY PRE-CHECK (mandatory, per result). Before you write a result,
   grep ${SCRATCH}/round17/inventory.txt and ${REPO}/frontier.tex for the
   closest existing statement. Fill closest_label with that label and
   why_not_implied with one line saying why your statement does not follow
   from it in three lines. If it does follow, it is a RESTATEMENT: put it
   in the restatements field (label + one line) and NOT in results. The
   novelty audit repeats this search independently; a restatement reported
   as a result is a defect that costs the route its verdict.
3. WHAT COUNTS. Your verdict is one of SOLVED / new-theorem / new-barrier /
   blocked / dead-end. new-theorem or new-barrier requires at least one
   result with status proved or refuted AND novelty new-object or
   new-relation. "A new row of measurements" is NEVER a result: measured
   data goes into the verification field of the theorem it supports, or
   is omitted. "strict-progress" no longer exists.
4. FIRST PRINCIPLES. The paper imports exactly four facts (thm:determinacy;
   Holt-Klee; Legendre's theorem on convergents; Samelson-Thrall-Wesler).
   You may not import a fifth. If a step needs a known theorem, prove it,
   or state it as a GAP with the attribution from memory flagged
   "unchecked against the source". NO WEB: no WebSearch, WebFetch or any
   network access.
5. VERIFY EVERYTHING in EXACT RATIONAL ARITHMETIC (python3
   fractions.Fraction); floats only to explore. NEVER compute val_sigma by
   greedy policy iteration in a possibly non-stopping game -- it is
   unsound; take the componentwise min over ALL positional tau, or use
   thm:eval-stopfree, or a least fixed point. The harness is at
   ${SCRATCH}/root16/ : mycore.py (class G(kinds, succ) with kinds in
   {'max','min','avg'}, non-sinks 0..n-1, t0 = n, t1 = n+1; profile_value,
   wstar by brute force, trap-based is_stopping, T_op, Z01, slack_step,
   minplus_close, transport_rows/transport_sep, hybrid), core.py (a second
   independent core), mylp.py and lp.py (exact two-phase simplex, Bland),
   zseed.py (the free Z_0/Z_1 seed), ownhyb.py (the own-successor test),
   auso.py and census/ (USO/AUSO predicates, BA walks), normform.py
   (harmonic normal form search), hyb2d.py and rathyb.py (exact 2-D polygon
   engines for |C| = 2), cc.py, wd.py, myinst.py (G8, S, S_r, H_m, G_m,
   A0), gstar.py (G*), t_bsi.py, t_escape.py, ratio.py and mobius.py (M6);
   ${SCRATCH}/solo/ (realiseAP.py, my_D.py = the Holt-Klee max-flow test,
   blowz.py, census/classes4.txt, AP_m4_k0_*.json, B1_game.json);
   ${SCRATCH}/myver/ and ${REPO}/scripts/round15-verify/,
   ${REPO}/scripts/round16-verify/ (the root agent's verification scripts:
   sparse_verify.py = sparse exact solver for games of hundreds of
   vertices, cv_build.py, hkd_check.py, b3.py, ...), ${REPO}/scripts/blowup/
   (B2_small_GAME.json, Blowup.lean, README.md). Round-16 route code,
   read-only, is under ${SCRATCH}/<route>/ for route in b3-level,
   level-lemma, hk-doubling, width-amortise, few-denominator-stall,
   bsi-counter, one-player-howard, fresh-16, fresh-16-alg, min-budget.
   COPY what you need into ${SCRATCH}/r17-<your-route>/ and work there. Do
   NOT write into another route's directory or into ${REPO} (not
   frontier.tex, not README.md, not the repository root); the root agent
   integrates.
6. KNOWN TRAPS, each of which has cost this project real time.
   - Building a constraint row as a dict LITERAL {a: 1/2, c: 1/2} silently
     collapses when a == c. ALWAYS accumulate: d[u] = d.get(u,0) + coeff.
   - When adding fresh vertices, carry the sinks as SENTINELS and map them
     to indices only at the very end.
   - Before believing "the polytope is infeasible", check that w* is feasible.
   - The trap Z_sigma must ADMIT t0 and exclude only t1.
   - Any bound |T^k y - T^k z| <= (...)^k needs y, z to AGREE WITH THE SINK
     PAYOFFS.
   - Membership of a polynomial class is a property of the instance AS
     POSED: check every structural parameter on the subgame REACHABLE FROM v0.
   - When comparing rules, count PRODUCTIVE rounds on both sides, and state
     WHICH VARIANT of a mechanism a measurement used; test BOTH clauses of
     rem:own-successor (round 16's few-denominator route tested clause (i)
     only and reported a stall of M6 that does not exist).
   - RANDOM SAMPLING HAS NEVER FOUND A HARD INSTANCE IN THIS PROJECT. Every
     one had to be ENGINEERED. "No counterexample in 100000 samples" is
     NOT evidence.
   - A Max vertex whose two options are a variable and a CONSTANT switches
     at most twice along any run: counters need non-constant drivers.
   - After proving or measuring anything on the instances you developed it
     on, RE-RUN it on freshly generated, larger instances before reporting.
   - A "witness" normal form that is not dyadic, or whose game was never
     built, is NOT a game. Build the game and verify from the game.
7. HONESTY. Never present an unproved statement as proved. If your route
   ends at a statement of the same strength as the target, SAY SO and mark
   it blocked. Do not report the problem as open and do not editorialise
   about difficulty; report mathematics.
8. Return paste-ready LaTeX for what you PROVED, in the amsthm style of
   frontier.tex, labels prefixed by your route name.
9. TIME AND CLEANUP. Budget your computations (background long runs with
   nohup inside YOUR directory and poll them; keep each foreground command
   under ten minutes). KILL EVERY BACKGROUND JOB YOU STARTED before
   returning (round 16 left sixteen jobs running for five hours) and leave
   no file outside your directory. Return a complete structured result
   even if a computation was cut short -- say what was cut.
`

const ROUTE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['route', 'object', 'verdict', 'headline', 'results', 'restatements', 'gap', 'next_steps'],
  properties: {
    route: { type: 'string' },
    object: { type: 'string', description: 'the mathematical object the route attached the problem to, in one sentence' },
    verdict: { type: 'string', enum: ['SOLVED', 'new-theorem', 'new-barrier', 'blocked', 'dead-end'] },
    headline: { type: 'string' },
    results: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'statement', 'status', 'novelty', 'closest_label', 'why_not_implied', 'argument', 'verification'],
        properties: {
          name: { type: 'string' },
          statement: { type: 'string' },
          status: { type: 'string', enum: ['proved', 'refuted', 'gap'] },
          novelty: { type: 'string', enum: ['new-object', 'new-relation', 'strengthening'] },
          closest_label: { type: 'string', description: 'the label in frontier.tex closest to this statement' },
          why_not_implied: { type: 'string', description: 'one line: why the statement does not follow from closest_label in three lines' },
          argument: { type: 'string' },
          verification: { type: 'string', description: 'what was computed in exact arithmetic, on which instances, with what outcome; measured data lives HERE and only here' },
        },
      },
    },
    restatements: {
      type: 'array',
      description: 'things you proved that turned out to be in the paper already: label and one line',
      items: { type: 'object', additionalProperties: false, required: ['label', 'note'], properties: { label: { type: 'string' }, note: { type: 'string' } } },
    },
    gap: { type: 'string' },
    latex: { type: 'string' },
    code_dir: { type: 'string' },
    prior_art: { type: 'string', description: 'from memory, flagged unchecked' },
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
    novelty_table: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['result_name', 'closest_label', 'class'],
        properties: {
          result_name: { type: 'string' },
          closest_label: { type: 'string' },
          class: { type: 'string', enum: ['new-object', 'new-relation', 'strengthening', 'restatement', 'measurement-only', 'unproved'] },
        },
      },
    },
    verdict: { type: 'string' },
  },
}

const ROUTES = [
  { key: 'query-model', title: 'The strategy-evaluation oracle model: query complexity of the sink on orientations SSGs realise', brief: `THE OBJECT: query complexity. An algorithm sees the game only through an
oracle that, given a Max strategy sigma, returns val_sigma (the full vector;
a weaker oracle returns only the outmap, i.e. the strictly switchable set
S_sigma). The cost is the number of queries. Every improvement rule of the
paper (all-switches, def:bsi, R_BR, the ladder's rules, Lemke's one-player
path of sec:bias) lives in this model; so do Schurr-Szabo's jumping
algorithms on abstract cubes (prior art, from memory). The paper knows
(read first): prop:allsw-auso, thm:flat-resolution, cor:ceiling-general
(every run is a BA walk of an AUSO of the Max cube), prop:auso-size,
prop:oneplayer-lp (one-player orientations are Holt-Klee), thm:profile-uso
and prop:projection, thm:opt-subcube and thm:short-path (from every
strategy at most m single switches reach the optimal subcube -- so the SINK
is at Hamming distance <= m from everywhere, yet finding it is the problem),
thm:compare-equivalence, thm:min-count, rem:four-ceilings, prop:mono-count
(almost every AUSO needs 2^{Omega(m)} vertices). What the paper does NOT
have is any statement about how many QUERIES are needed or suffice; its
lower bounds count ROUNDS of specific rules.

WHAT TO PROVE (pick the strongest you can, in this order of value):
 (A) An UPPER bound: an algorithm in the value-oracle model finding the
     sink of every orientation realised by a stopping SSG with m Max
     vertices in poly(m) queries, using the VALUES (not just the outmap):
     the values give, for each queried sigma, the exact val_sigma vector,
     hence every switch's exact gain, and the gains satisfy laws the paper
     proved (thm:impedance, lem:rise-bound, thm:switch-count, thm:peak-law,
     lem:monotone-law). Note that thm:decide-one-bit and
     thm:compare-equivalence say such an algorithm with poly-time
     processing would put SSG-Value in P -- so check every step; for ONE
     player the answer is known by thm:one-player (an LP), and the interest
     is whether the query count is poly WITHOUT an LP, i.e. whether the
     orientation-plus-values carry enough structure; the two-player case
     is the target and there the oracle val_sigma includes Min's best
     response.
 (B) A LOWER bound: a family of stopping SSGs of polynomial size on whose
     realised orientations every DETERMINISTIC outmap-query algorithm needs
     2^{Omega(m)} queries (adversary argument on the realisable class --
     the adversary must answer with an orientation that some GAME realises,
     so the realisable class must be rich enough; the blow-up hierarchy at
     polynomial size would do but is not realised beyond level two -- so
     find a realisable rich family, e.g. via thm:readout-realise's affine
     readouts, or prove a lower bound on a class that IS realised (deformed
     products def:deformed; stacks thm:stack; the k=1 projections of
     prop:seven-k1)). A lower bound of m^2 or m log m is also a result if it
     is for the VALUE oracle and proved.
 (C) The SEPARATION: is the value oracle strictly more powerful than the
     outmap oracle on realised orientations (an orientation with two
     realisations whose values differ enough to change an algorithm's
     path, or a proof that the values are determined by the orientation up
     to what any algorithm can use)?
 (D) Randomised query complexity: does random-facet's e^{2 sqrt n}
     (thm:subexp) have a matching lower bound in the query model on
     REALISED cubes? (Matousek's abstract lower bound is prior art -- from
     memory, flag it; the question is realisability.)

DELIVERABLE: theorems with proofs about query counts. A measured table of
query counts of existing rules is NOT a result. Labels prefixed qm:.` },
  { key: 'order-lattice', title: 'The order of the values as a certificate: a lattice of orders and a monotone iteration on it', brief: `THE OBJECT: the lattice of (pre)orders on V. The paper proves
thm:order-determines: the ORDER of the average values determines every
value (read it, its proof, and thm:compare-equivalence, cor:wrong-equivalence,
thm:top, thm:lfp-general, cor:comparison, def:simorder and sec:simorder --
the simulation preorder is a fixed point on the lattice of RELATIONS and is
the paper's closest object; thm:matching-barrier shows what every calculus
of its class misses; thm:tarski in sec:width is the paper's Tarski search).
Prior art the project has already rediscovered: Gimbert-Horn's permutation
algorithm (enumerate orders of the average vertices, decode each by a
linear solve, O(a!)); do NOT re-derive it, cite it from memory and go
beyond it.

WHAT THE PARITY-GAME BREAKTHROUGH DID (from memory, unchecked, and to be
rebuilt from first principles here, not imported): certificates ordered in
a lattice (progress measures), a monotone lifting iteration converging to
the least certificate, and a COMPRESSION of the certificate's range to
quasipolynomial size (universal trees), giving a quasipolynomial step
bound. YOUR QUESTION: is there an analogue for SSG-Value with orders as the
certificates?
 (A) The certificate. A (pre)order <= on V is CONSISTENT if the values
     decoded from it (solve the linear system the order induces: each Max
     vertex takes its <=-larger successor, each Min its smaller, averages
     average) reproduce the order. thm:order-determines gives: the true
     order is consistent and its decoding is w*. PROVE what you can about
     the set of consistent orders: is the true order the UNIQUE consistent
     one on a stopping game (if not, characterise the others -- traps,
     lem:trapchar)? Consistency is one linear solve, so orders are
     poly-size certificates checkable in poly time that name NO strategy:
     make that precise.
 (B) The lattice and the lift. Define a partial order on preorders (e.g.
     refinement, or the pointwise order of decoded vectors) and a LIFT
     operator (decode, re-sort, refine) that is monotone. PROVE or REFUTE:
     iterating the lift from the coarsest preorder converges to the true
     order (a Tarski-style least fixed point on a lattice of orders). If
     it converges, BOUND the number of lifts: polynomial (each lift
     strictly refines?), exponential (find the family), or cyclic.
 (C) The compression. If the iteration is exponential because the decoded
     values move by 2^{-a}, look for the analogue of universal trees: a
     coarser lattice (orders modulo an equivalence the decoding ignores)
     of small height. thm:order-determines says the AVERAGE vertices'
     order suffices: the refinement lattice of preorders on a elements has
     height O(a^2), so a lift that strictly refines at every step converges
     in O(a^2) lifts. PROVE whether a monotone strictly-refining SOUND lift
     EXISTS (this is the crux; a negative answer as a theorem -- "every
     sound monotone lift stalls on this family" -- is a new barrier with a
     new object).
 (D) Compare with the paper's mechanisms: an order-lift that decides the
     wedge (sec:wedge) or CV (def:cv) in polynomially many lifts would be
     new; if the simulation preorder M1 already IS the lift you find,
     prove the identity and stop (that is a restatement).

DELIVERABLE: theorems about consistent orders, the lift, its convergence
and its step count; explicit families where it stalls, verified exactly.
Labels prefixed ol:.` },
  { key: 'convex-lift', title: 'The lifted bilinear system and its convex hull: exactness or an integrality gap', brief: `THE OBJECT: the convex hull of a lifted feasible set, and the
Reformulation-Linearisation / Sherali-Adams hierarchy over it. The value
system is x_v = x_{v0} or x_{v1} chosen by Max (max) and Min (min); write
each Min choice as y_v in [0,1] with x_v = y_v x_{v,0} + (1-y_v) x_{v,1}
(and Max's as z_v likewise): a BILINEAR system in (x,y,z) whose solutions
with y,z in {0,1} are exactly the positional pairs' value vectors, and whose
fractional solutions are mixed stationary pairs' values (a rational, not
linear, dependence -- check this). The paper's closest objects, which you
MUST read first and not repeat: sec:transport (the LP over Q(G) that keeps
the convex halves of the controlled rows: lem:transport-exact,
thm:transport-barrier, rem:transport-objective), sec:hybrid (K(Delta),
thm:hybrid-complete, prop:hybrid-rate, thm:hybrid-convex-barrier), the
degree-two Lasserre lift (thm:lasserre-vacuous: the SOS relaxation of
degree two is vacuous -- your hierarchy is the LINEAR one over the CHOICE
variables, a different object, and you must say precisely how it differs),
rem:lcp (interior point closed), prop:lcp (the profile LCP has a P-matrix),
sec:bias (Lemke), thm:opt-subcube, thm:lfp-general (val is the LEAST fixed
point; which rows of {x : x >= Tx} are convex: at Max vertices
x_v >= max(...) is convex, at Min vertices x_v >= min(...) is a union of
two halfspaces).

WHAT TO PROVE:
 (A) The exact statement of the lifted system L(G) and of its level-k RLT
     relaxation R_k(G) (products of up to k choice variables with the value
     rows, McCormick bounds from 0 <= x <= 1). PROVE: R_k is a
     polynomial-size LP for fixed k; its optimum of x(v0) is a sound
     one-sided bound on val(v0) (fix the direction).
 (B) EXACTNESS OR GAP. Is R_1 exact on every stopping SSG? Almost certainly
     not -- find the smallest counterexample by exact LP (mylp.py) and
     PROVE the gap on a family: either the gap of R_k stays large, or R_k
     is exact only for k >= (number of Min vertices) -- which would show
     the hierarchy is the modulator class (thm:modulator) in disguise:
     PROVE that identity if it holds (a new relation between two of the
     paper's objects) or refute it.
 (C) On the wedge WD(2j,j,j+4) (sec:wedge) and on CV(e,s) (def:cv): the
     first exact level, exactly computed for at least three sizes, with
     the proof of the pattern if you see one.
 (D) The convex hull itself: for ONE Min vertex, is conv(L(G)) described by
     polynomially many inequalities (a projection of a disjunctive program
     -- Balas's theorem is prior art; prove what you use)? For k Min
     vertices the disjunctive hull has 2^k pieces; PROVE whether the SSG
     structure (Min's choices interact only through the values, which are
     monotone in each choice) collapses the hull to something smaller --
     that would be new, and its failure on an explicit game would be a
     new barrier for the whole hierarchy.

DELIVERABLE: the relaxation defined exactly, its soundness proved,
exactness or an explicit gap family verified in exact arithmetic, and the
relation to thm:modulator / sec:transport / sec:hybrid stated as a theorem.
Labels prefixed cl:.` },
  { key: 'variational', title: 'Energy functionals and reversibility: a variational characterisation of the value and the class it solves', brief: `THE OBJECT: energy functionals on the game graph and the symmetry
(reversibility) of the chance part. On a reversible Markov chain the
harmonic function with given boundary values is the unique minimiser of
the Dirichlet energy (Thomson/Dirichlet principle) -- a convex problem. The
SSG value is a "game-harmonic" function: harmonic at average vertices, the
max/min of its neighbours at controlled ones. The paper's closest objects
(read first, do not repeat): thm:energy in sec:composition (the identity
sum_v N_v Delta_v^2 = 4w(1-w) for the visits N_v and the gaps Delta_v at
average vertices, and the Doob crossing bound), lem:gate and thm:two-exit,
thm:impedance (the gain of a switch is a transfer impedance over an escape
probability), thm:lfp-general (least fixed point), thm:escape-class /
def:survival (the escape certificate (lambda, x) with Sx <= lambda x, an
LP), thm:few-escape, and the eight polynomial classes plus thm:qp (grep
'polynomial class' and the summary paragraph "Positive algorithmic
results").

WHAT TO PROVE:
 (A) A DIRICHLET PRINCIPLE for one player: for a one-player stopping SSG
     whose chance graph is symmetric in a sense you define (e.g. the chain
     under every strategy is reversible with respect to one measure pi
     independent of the strategy), PROVE that val is the optimum of a
     CONVEX energy problem (concave maximisation over a convex set, or a
     saddle) solvable in polynomial time by a method you also prove
     correct from first principles (do NOT import ellipsoid/interior
     point: an explicit polynomial method for the specific structure, e.g.
     a Laplacian system per strategy plus a convexity argument giving a
     polynomial-step descent -- or show that the convexity makes
     all-switches polynomial on that class).
 (B) TWO PLAYERS: does the symmetry make the max-min problem a
     convex-concave saddle (then solvable in polynomial time, from first
     principles), or does Min break it? Prove either.
 (C) THE CLASS. Define the class exactly (as a property of the instance
     reachable from v0), PROVE it is decidable in polynomial time, PROVE it
     is NOT contained in the union of the paper's nine classes by an
     explicit witness family verified on the reachable subgame (required
     for it to count), and say whether the hard families of the paper (the
     ladder def:ladder, H_m, CC, WD, CV, RD, SD, the deformed products) can
     be made symmetric without changing their difficulty -- if EVERY SSG
     is poly-time equivalent to a symmetric one, the class is the whole
     problem and you must say so (a theorem too, a new relation, and it
     closes the object).
 (D) If (A) fails: the obstruction as a theorem with a small explicit game
     ("no energy of the form E(x) = ... has val as its minimiser because
     ...").

DELIVERABLE: a variational theorem with a convex structure proved, the
class it defines with a witness outside the nine, or the proved
obstruction. Labels prefixed vr:.` },
  { key: 'parametric-path', title: 'The optimal pair as a function of a uniform stopping probability: breakpoints and path-following', brief: `THE OBJECT: the parametric curve p -> (sigma*(p), tau*(p), val_p) for the
game G_p in which every step from an average vertex (or from every
non-sink) stops with probability p and pays a fixed payoff, p from 1 down
to 0. At p = 1 the game is trivial; at p = 0 it is G. The values val_p are
piecewise rational in p; the optimal pair changes at finitely many
BREAKPOINTS. The paper's closest object is sec:bias (read
thm:lemke-homotopy, cor:bias-algorithm, the one-player shadow-vertex
identification, and every family measured there: P_D, G*, HAM_3 and the
D-parametrised ones) -- that homotopy moves a BIAS on the profile LCP, not
the stopping probability; you must prove whether the two paths coincide
(then your route is a restatement: say so and stop) or differ (then
everything below is new). Also read def:damping, lem:gadget,
thm:stopping-transform, thm:contraction, lem:denominator-sharp,
thm:opt-subcube, thm:short-path, prop:allsw-auso.

WHAT TO PROVE:
 (A) WELL-DEFINEDNESS. For every stopping SSG the path p -> optimal pair
     exists, is unique off the breakpoints (nondegeneracy in p: prove or
     handle ties by lexicographic perturbation from first principles), and
     the number of breakpoints B(G) is finite with an explicit upper bound
     (val_p at each pair is a rational function of degree <= N in p; two
     such cross at most 2N times; so B(G) <= 2N x 4^{|C|} trivially -- do
     better).
 (B) PATH-FOLLOWING. At a breakpoint p*, the next pair is determined by
     comparing the two tying successors' values for p slightly below p*:
     PROVE that this comparison is a DERIVATIVE comparison computable by
     one linear solve under the current pair (so each breakpoint costs
     polynomial time and the whole algorithm costs poly(N) x B(G)), and
     that for Min's ties the same holds. If a breakpoint can be degenerate
     (three-way tie, or a tie persisting on an interval), say how to
     resolve it and PROVE the resolution correct.
 (C) THE COUNT. PROVE B(G) polynomial for one-player games (there the path
     is a parametric LP path; is it the shadow-vertex path of the
     occupancy polytope, sec:bias's one-player object? prove the identity
     or the difference), and for two players either PROVE a polynomial
     bound (this would put SSG-Value in P -- check every step against
     thm:decide-one-bit and the standing rule) or CONSTRUCT a family with
     2^{Omega(N)} breakpoints, verified exactly for >= 5 sizes with the
     growth law proved. The ladder def:ladder and the deformed products
     def:deformed are the first candidates; the parametric analogue of
     Klee-Minty (Murty's / Goldfarb's parametric LP examples are prior
     art, from memory) is the shape to aim for.
 (D) MONOTONICITY. Prove or refute: along the path each Max vertex's choice
     changes at most O(1) times (that would give B(G) = O(N)); the values
     val_p(v) are monotone in p; the path never revisits a pair.

DELIVERABLE: the theorems in (A)-(B), and in (C) a proved bound or a proved
exponential family. Labels prefixed pp:.` },
  { key: 'oracle-barrier', title: 'One model containing every mechanism of the paper, and a family every algorithm of the model loses on', brief: `THE OBJECT: a formal model of "local propagation" algorithms and its
query/round complexity. The paper has six mechanisms M1-M6 (sec:simorder,
sec:slack, sec:ratio, sec:seeded, sec:transport, sec:hybrid), the
improvement rules (all-switches, def:bsi, R_BR) and per-mechanism barriers
(thm:matching-barrier for the simulation class, thm:slack-barrier,
thm:seeded-barrier, thm:transport-barrier, thm:hybrid-convex-barrier), each
with its own family (G8, H_m, CC, WD, CV). Every family found is decided at
ROUND ZERO by M1 (def:simorder's greatest fixed point) or by M(1,0) of
def:seeded, and thm:seed-dichotomy shows any family defeating the seeded
rule within polynomially many improvement rounds makes all-switches itself
superpolynomial. READ all of the above and the wedge's rem:wedge, and
prop:locality (no sound rule reads a bounded radius).

WHAT TO PROVE:
 (A) THE MODEL. Define a class A of algorithms, as a THEOREM-GRADE
     definition (inputs, allowed operations, cost), such that M1, M2, M2T,
     M4, M5, M6, all-switches, def:bsi and R_BR are PROVABLY instances (one
     lemma each, with the cost accounting), and such that the class is
     closed under the natural combinations (running two members and taking
     the better verdict; seeding one with another's output). The seeded
     calculus M3 = M(1,0) evaluates a strategy exactly (an LP): decide
     whether your model includes exact strategy evaluation as a unit-cost
     operation (then all-switches is in it and the model is "improvement +
     propagation") or not; make the choice explicit and justify it by what
     the barrier will then mean.
 (B) THE BARRIER. A family (G_N) of stopping SSGs of size N, with a
     value-distinguishing controlled vertex, on which EVERY algorithm of A
     needs 2^{Omega(N)} cost to decide that vertex. The proof must be an
     ADVERSARY or CERTIFICATE argument covering the whole class A, not a
     measurement of its members -- the paper's per-mechanism certificates
     (thm:hybrid-convex-barrier's convex chain) are the model to
     generalise. If A contains exact strategy evaluation, the family must
     make all-switches slow, i.e. it must be a superpolynomial all-switches
     family -- which the paper does not have (prop:auso-size,
     rem:blowup-realise). Say which model you can prove the barrier for.
 (C) THE EDGE. The SMALLEST extension of A that decides your family in
     polynomial cost (which operation, added, breaks the barrier). This is
     the constructive content: name the operation precisely and prove both
     that it decides the family and that it is not in A.
 (D) Relate to prop:locality and thm:seed-dichotomy: is your barrier a
     restatement of either (then say so), or does it cover algorithms they
     do not?

DELIVERABLE: the model as a definition with the membership lemmas, the
barrier theorem with its family verified exactly at >= 5 sizes, the edge
operation. A barrier whose model contains none of M1-M6 is worthless; a
model that contains all of them and a proved family is a new object.
Labels prefixed ob:.` },
  { key: 'realisation-space', title: 'The semialgebraic set of games realising a given orientation: the cost of a blow-up level as a geometric invariant, with B^3 as the test case', brief: `THE OBJECT: for a fixed orientation s of the m-cube, the REALISATION SPACE
R(s) = the set of (one-player, or two-player with k Min vertices) stopping
games of a given shape whose Max-cube orientation is s -- in normal-form
coordinates (the harmonic normal form of def:reduced-rows / sec:readouts:
each Max vertex's two options are affine functions of the values at the
Max vertices, x_v = max(p_v . x + q_v, p'_v . x + q'_v) with substochastic
dyadic rows) R(s) is a semialgebraic set cut out by the 2^m x m sign
conditions "the switch at v under sigma is improving iff s says so", each a
polynomial inequality in the rows once the values val_sigma (rational
functions of the rows) are substituted. The paper's closest objects (read
first): sec:readouts (def:readout, lem:readout, thm:readout-realise: one
player buys affine readouts, the second player concavity; thm:min-count),
prop:oneplayer-lp (Holt-Klee), prop:auso-size, prop:mono-count (counting:
almost every AUSO needs 2^{Omega(m)} vertices -- a Warren/Milnor-Thom-type
count is the natural tool; read the paper's proof and do not repeat it),
thm:blowup and prop:blowup-height, rem:blowup-realise (the open question:
does each level cost O(1) controlled vertices and O(1) bits),
prop:b2-realised (138 vertices), prop:b3-outer (194 vertices realise the
outer half of B^3 = B(B^2), the translated layer is not realised),
prop:m3-realised and prop:m3-one-min, thm:stack (stacking), def:deformed,
and the round-16 b3-level route's record (${REPO}/rounds/round16/results/
2*b3*.json, its code under ${SCRATCH}/b3-level/, the game
${REPO}/scripts/round16-verify/TB_GAME_D10.json).

WHAT TO PROVE:
 (A) STRUCTURE OF R(s). For one player: val_sigma is the solution of a
     linear system in the rows, hence rational in them; PROVE the exact
     algebraic description of R(s) at fixed denominator 2^D and fixed
     shape, its dimension when nonempty, the degree of each sign condition
     in the rows (per sigma the condition "switch improving" is a
     polynomial inequality of degree <= m+1?), whether R(s) is a union of
     polyhedra in the normal-form coordinates after the substitution
     x = val_sigma, and whether the paper's successive-LP realiser
     (round 15's slp6.py, read-only under the round-15 scratchpad named in
     rounds/round16/README.md) is exactly a linearisation of it.
 (B) THE LEVEL COST AS AN INVARIANT. Define c(s) = the least number of
     Max-vertex rows' bits (or of average vertices via lem:dyadic-row) over
     R(s) and PROVE a bound relating c(B(s)) to c(s) -- thm:blowup builds
     B(s) from s combinatorially; does the realisation of B(s) need only
     O(1) more bits and O(1) more Min vertices than s? A proved recurrence
     c(B(s)) <= c(s) + O(1) would answer rem:blowup-realise and give the
     superpolynomial all-switches family (check every step against
     thm:min-count and cor:b2-min's forbidden faces); a proved lower bound
     c(B^k) >= 2^{Omega(k)} would close the hierarchy as a route and is
     equally a result. Either must be a THEOREM about R(s), not a search
     outcome.
 (C) THE TEST CASE. Apply (A)-(B) to B^3: either produce the game (dyadic,
     built with lem:dyadic-row, verified from the game with the sparse
     solver in ${REPO}/scripts/round16-verify/sparse_verify.py: USO,
     acyclic, outmap = B^3, height 22, run printed) or PROVE that R(B^3) is
     empty for the shapes the round-16 route tried (state the shapes
     exactly; an infeasible exact LP for each linearised support pattern,
     with the reason the linearisation is exact for that pattern). "We
     searched and found nothing" is not a result.
 (D) If the theory in (A)-(B) does not reach B^3, PROVE what it does reach:
     e.g. the semialgebraic description of R(s) for every 3-cube class
     (the paper has realisations at prop:m3-realised; only the
     description and the exact c(s) would be new), or the exact c(s) for
     the height-7 orbit.

DELIVERABLE: the semialgebraic description as a theorem, a proved statement
about c(B(s)) vs c(s), and B^3 realised or its obstruction proved for named
shapes. Blind searches are forbidden. Labels prefixed rs:.` },
]

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

1. For EVERY result marked "proved" or "refuted", reconstruct the argument.
   Find the step that is asserted rather than proved. State it as a
   one-sentence GAP. A theorem about a NEW OBJECT is only as good as its
   definitions: check that the object is defined precisely enough that the
   theorem has a truth value, and that the definition matches what the
   computations used.
2. For EVERY numerical or computational claim, REBUILD THE COMPUTATION
   YOURSELF in exact rational arithmetic, from the STATEMENT and not from
   the route's code, in ${SCRATCH}/r17-audit-${r.key}-correctness/. If a
   claimed family, instance, relaxation value, breakpoint count, query
   bound or realisation does not reproduce, that is FATAL and you must give
   the discrepancy explicitly. Recompute at least three rows of any table.
3. Hunt for the project's standing errors: greedy policy iteration in a
   non-stopping game; dict-literal rows collapsing; fresh vertices
   colliding with the sinks; t0 excluded from the trap; the PAIR test
   instead of rem:own-successor; clause (i) tested without clause (ii);
   the Z_0/Z_1 seed omitted; a vacuous stall; a parameter held constant;
   unreachable vertices used to separate a family from a class; unpinned
   sink payoffs; a non-productive round counted; a non-dyadic "witness";
   a "polynomial class" inside thm:few-avg, thm:few-escape, thm:kacyclic,
   thm:bounded-components, thm:escape-class, thm:few-denominator,
   thm:modulator, thm:qp or the trivial min(m,k) = O(log N); an IMPORTED
   theorem beyond the four allowed, used without proof.
4. Check every claimed IMPLICATION between the route's own results and every
   citation of frontier.tex against the actual text of the label cited.
5. If the route claims an algorithm, a barrier, a bound or a class, check it
   against THE STANDING RULE and against the proved equivalences
   (thm:compare-equivalence, thm:decide-one-bit, prop:no-halving,
   cor:wrong-equivalence, rem:transport-objective, rem:bsi, thm:top,
   thm:gap-equivalence): does any step assume an oracle that is
   target-equivalent?

Report findings with severity fatal / major / minor / note. "sound" is TRUE
only if nothing fatal or major survives. Being unable to find a defect in a
result you did not check is not grounds for sound = true; say what you
checked. Kill your background jobs before returning. Write nothing into
${REPO}.
`,
  },
  {
    key: 'novelty',
    prompt: (r, res) => `
You are an ADVERSARIAL AUDITOR. Your job is not to check arithmetic but to
decide whether this work is NEW and MEANS anything, under the tightened
standard of this round, and to say so bluntly.

${COMMON}

# The work under audit (route "${r.key}": ${r.title})

${res}

# Your task: NOVELTY AND SIGNIFICANCE

1. THE NOVELTY TABLE (mandatory). For EVERY entry of results AND of
   restatements, do your OWN search of ${SCRATCH}/round17/inventory.txt and
   ${REPO}/frontier.tex for the closest existing statement, and classify:
   new-object (a theorem about an object the paper does not own),
   new-relation (a proved identity or implication between two of the
   paper's objects, or between a new one and an old one), strengthening
   (same statement, weaker hypothesis or stronger conclusion, proved),
   restatement (follows from closest_label in three lines -- give the
   three lines), measurement-only (a row of numbers with no theorem it
   supports), unproved. Disagree with the route's own classification
   whenever the evidence says so. This project has repeatedly caught routes
   restating thm:ladder, thm:short-path, lem:cut, lem:duality,
   thm:seed-dichotomy, lem:rise-bound, thm:bsi-tracks, lem:hstar-super,
   lem:readout and thm:matching-barrier as new. Also flag anything that is
   standard published mathematics presented without acknowledgement (see
   the prior-art list); a rediscovery the route itself attributes is fine.
2. DID THE ROUTE CHANGE THE OBJECT? Say in one sentence what the object is
   and whether the paper already owns it under another name (the
   simulation preorder IS a lattice fixed point; the hybrid IS a convex
   relaxation; sec:bias IS a parametric path; thm:matching-barrier IS a
   model barrier). If the new object collapses to an old one, was the
   collapse PROVED (a result) or merely noticed?
3. IS IT CIRCULAR OR VACUOUS? Oracle assumptions that are target-equivalent
   (thm:compare-equivalence, thm:decide-one-bit, prop:no-halving,
   cor:wrong-equivalence, rem:transport-objective, rem:bsi, thm:top);
   barriers whose model contains none of M1-M6, all-switches, def:bsi,
   R_BR; classes with no member outside the nine (the eight plus thm:qp)
   verified on the reachable subgame; families measured at fewer than five
   sizes or with no proved growth law; realisations never built as games.
4. THE VERDICT UNDER THE ROUND'S RUBRIC: does the route have at least one
   proved or refuted result of class new-object or new-relation? If not,
   its verdict must be blocked or dead-end regardless of what it says.
   State the route's REAL remaining gap in one sentence, more precisely
   than the route states it.
5. Would integrating this into frontier.tex make the paper better or worse?
   Name WHICH results (by name) are worth integrating and which are not.
   "Worse" is a legitimate verdict. Write nothing into ${REPO}.
`,
  },
]

const PAPER_AUDIT = {
  key: 'round16-diff',
  what: `the 2698 lines ADDED to frontier.tex in round 16 (batches A-I, git diff ab61ad4..7fa45a3), saved as ${SCRATCH}/round17/round16_diff.txt`,
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
was written by the root agent while integrating ten audited routes and
seven paper audits; the routes' claims were audited, the INTEGRATED TEXT
was not. Round 16's own paper audits found eight majors in material
integrated the day before, all of them integration errors: a hypothesis
dropped in transcription, a proof sentence written by the integrator that
is false, a number copied from the wrong table, a label pointing at the
wrong result, a scope claim that later results made false, a "verified"
that the route verified and the manuscript did not. Those are what you
are looking for.

# Your task

1. PROOFS. For every theorem, lemma, proposition and corollary in the added
   text, reconstruct the proof step by step. Report every step asserted
   rather than proved, every hypothesis used but not stated (stopping?
   nondegeneracy? sink payoffs pinned? Min present? dyadic? reachable from
   v0?), every citation whose statement does not give what is used, every
   quantifier error. Sinks, ties, empty sets, the one-vertex game and the
   k = 0 / m <= 2 cases are where this manuscript's errors have lived.
2. NUMBERS. For every explicit instance, table, count or vertex count in the
   added text that can be recomputed in under an hour, RECOMPUTE IT in exact
   rational arithmetic with your own code in
   ${SCRATCH}/r17-paper-audit-${s.key}/ (harness at ${SCRATCH}/root16/,
   ${SCRATCH}/solo/, ${REPO}/scripts/round16-verify/ -- you may READ the
   root agent's scripts to see what was checked, but recompute from the
   manuscript's statement). The ceilings table of rem:four-ceilings, the
   CV(e,s) tables, the stacking family's 12k, the 194-vertex game, the
   194/138/97 vertex counts, prop:w2, the m = 3 one-Min realisations, the
   HAM_3 breakpoints and the bias-homotopy rows are the obvious targets.
3. CONSISTENCY. Every \\Cref in the added text must point at a result that
   says what the text claims. Every qualifier ("measured, not proved",
   "one direction only", "at fixed s") must match the statement it
   qualifies AND the abstract/summary (the abstract and sec:summary were
   rewritten in round 16: check every round-16 claim in them against the
   body). Every "verified on K instances" must say what was varied.
4. PRIOR ART presented as new is a defect; name the source if you know it.
5. OVERSTATEMENT: barriers covering no real rule, classes that are
   restatements, families measured at two sizes, "answers the question"
   where only a special case is answered.

Report findings with severity fatal / major / minor / note, each with the
LINE NUMBER in frontier.tex, the label, the defect in one sentence and the
evidence. "sound" is TRUE only if nothing fatal or major survives. List what
you checked and what you did not. Put target = 'frontier.tex round-16 diff'.
Kill your background jobs before returning. Write nothing into ${REPO}.
`

log(`Round 17: ${ROUTES.length} object-changing routes on Opus 5: ${ROUTES.map(r => r.key).join(', ')}; correctness + novelty audits on Opus 5; one paper audit (round-16 diff) on Opus 5.`)

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\n\n# YOUR ROUTE: ${r.title}\n${r.brief}\n\n` +
    `Work in ${SCRATCH}/r17-${r.key}/ (create it). Copy the harness from ` +
    `${SCRATCH}/root16/ (and what you need from ${SCRATCH}/solo/) into your own ` +
    `directory before using it. Read ${SCRATCH}/round17/inventory.txt in full ` +
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
log(`Round 17 complete: ${good.length}/${ROUTES.length} routes returned; paper audit ${paper ? 'returned' : 'missing'}.`)
return { round: 17, routes: good, paper }
