export const meta = {
  name: 'ssg-round19',
  description: 'Round 19 on the SSG value problem under the round-19 brief (rounds/round19/BRIEF.md): eight routes on Opus 5 at effort high (five from round 18\'s list, two fresh formulations, one blind) against the post-round-18 frontier (244 pp, 526 results), each audited for correctness and novelty on Opus 5, plus ONE paper audit of the round-18 diff on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
    { title: 'Paper audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/scratchpad'
const R18 = '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad'
const R17 = '/tmp/claude-1000/-data-ssg-proof/d1fe2115-9b72-4784-bb94-87421ac1106c/scratchpad'

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

${REPO}/frontier.tex is a 244-page LaTeX development of 526 numbered
results (18978 lines) built over eighteen multi-agent rounds and one solo
round by the root agent. Every claim in it is proved and every negative
claim carries an explicit instance verified in exact rational arithmetic.
It contains NO polynomial-time algorithm for the general problem and
claims none. Read the parts you need with grep/sed; do NOT read the whole
file. THE INVENTORY ${SCRATCH}/round19/inventory.txt lists every numbered
result as "L<line> <env> <label> :: <title>", grouped by section: read it
in full FIRST (it is short) and use it for the novelty pre-check below.
Line numbers quoted in the route briefs refer to frontier.tex at commit
6e6c011 (HEAD). Sections and their first lines: Introduction (l.279); The problem (l.281); What is proved here, and what is not (l.359); The Shapley operator (l.446); Stopping games (l.760); The quantitative stopping transformation (l.996); A polynomial special case (l.1388); The value alphabet (l.2532); Width: the search is quasipolynomial, the tables are not (l.3048); The structure of the optimal set (l.3440); Exactly how much a single switch gains (l.4164); Composition, and an energy identity (l.4299); Refutations and barriers (l.4490); The all-switches rule does not dominate (l.4496); Three laws for all-switches, a component bound, and a new (l.4564); Ties in one-player games (l.7113); Deformed cubes, and why the blow-up leaves the Holt--Klee class (l.7549); Gluing facets, the sink lift, and the Holt--Klee ceiling at $m=6,7$ (l.7876); One player: Howard's rule with two actions, sign-definite games, and stacking (l.8289); Readouts: what a game presents to its Max vertices (l.8714); The profile cube and its sink projection (l.9035); Lemke's algorithm as a bias homotopy (l.9441); A rule that needs exponentially many switches (l.9898); Solving the deterministic residue exactly, and why it does not (l.10198); The induced orientation of the two-player cube can be cyclic (l.11913); Value iteration is exponential already without players (l.12049); Improving switches need not point toward the optimal set (l.12147); The objective of the strategy-space formulation is (l.12335); The selection problem is the whole problem (l.12471); What a certificate would look like (l.12939); A subexponential upper bound (l.13036); Subcubes, subgames and dead coordinates (l.13055); The algorithm and its correctness (l.13120); The expected number of switches (l.13181); The remaining gap (l.13392); A global mechanism that beats locality (l.13715); Adding arithmetic: the slack calculus (l.13954); A multiplicative calculus, and why it stops in the same place (l.14617); The branch-compensation barrier (l.15060); Seeding from policy evaluation (l.15198); A linear-programming certificate, and a complementary (l.15387); Freezing one vertex: the response map folds (l.16151); Coupling the two: the transport--slack hybrid (l.16576); A hybrid stall inside the few-denominator class (l.17292); A one-player family the whole propagation side loses on (l.17765); The own-successor rule, and a wedge that defeats it (l.18298); Summary (l.18618).

# THE STANDING RULE -- read this before designing any experiment

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
# The rules of this round (the round-17 rules, tightened on the user's instruction; read twice)

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
   grep ${SCRATCH}/round19/inventory.txt and ${REPO}/frontier.tex for the
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
   (B2_small_GAME.json, Blowup.lean, README.md). Round-18 route code and audits, read-only, are under ${R18}/r18-<key>/
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
   COPY what you need into ${SCRATCH}/r19-<your-route>/ and work there. Do
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
     WHICH VARIANT of a mechanism a measurement used; test ALL THREE readings of
     the standing rule -- own-successor (i), (ii) and the non-strict pair
     test -- Z-seeded (round 16's few-denominator route tested clause (i)
     only and reported a stall of M6 that does not exist; round 17's
     routes ran their OWN drivers, which silently weakened tests; re-run
     the paper's definitions).
   - RANDOM SAMPLING HAS NEVER FOUND A HARD INSTANCE IN THIS PROJECT. Every
     one had to be ENGINEERED. "No counterexample in 100000 samples" is
     NOT evidence.
   - A Max vertex whose two options are a variable and a CONSTANT switches
     at most twice along any run: counters need non-constant drivers.
   - After proving or measuring anything on the instances you developed it
     on, RE-RUN it on freshly generated, larger instances before reporting.
   - A "witness" normal form that is not dyadic (or rational without the
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
     into files in your directory as you go.
7. HONESTY. Never present an unproved statement as proved. If your route
   ends at a statement of the same strength as the target, SAY SO and mark
   it blocked. Do not report the problem as open and do not editorialise
   about difficulty; report mathematics.
8. Return paste-ready LaTeX for what you PROVED, in the amsthm style of
   frontier.tex, labels prefixed by your route name.
9. TIME AND CLEANUP. Budget your computations (background long runs with
   nohup inside YOUR directory and poll them; keep each foreground command
   under ten minutes). KILL EVERY BACKGROUND JOB YOU STARTED before
   returning (round 16 left sixteen jobs running for five hours; round 17 left a monitor loop; round 18 left four stray files in the repository root) and leave
   no file outside your directory. Return a complete structured result
   even if a computation was cut short -- say what was cut.
`

const ROUTE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['route', 'object', 'verdict', 'headline', 'results', 'restatements', 'gap', 'next_steps', 'games_built'],
  properties: {
    route: { type: 'string' },
    object: { type: 'string', description: 'the mathematical object the route attached the problem to, in one sentence' },
    verdict: { type: 'string', enum: ['SOLVED', 'new-theorem', 'new-barrier', 'blocked', 'dead-end'] },
    headline: { type: 'string', description: 'one sentence you PROVED, in the words of one of your results; it is audited as a claim' },
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
    games_built: { type: 'string', description: 'REQUIRED: for every result resting on an instance or family, the game file(s) (kinds, successors) in your directory, the checks run FROM THE GAME (stopping by the trap test, values, outmap / run / rows) and the vertex counts; the literal none only for results with no instance' },
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
  { key: 'escape-certificate', title: 'The escape shape as a semialgebraic feasibility set: an exact certificate for the last doubling corner over the level-two block, and the second escape shape', brief: `THE OBJECT: the FEASIBILITY SET of the escape shape. thm:escape-level
(l.6806; def:escape-ext l.6791) describes every nondegenerate stopping
escape extension of a driven block B by the parameters A, A' > 0, the
nonnegative row vectors C_alpha, C_beta, R_alpha, R_beta over the block's
readable coordinates and the constants q_A, q'_A, q_B, q'_B, and computes
its improvement outmap from three drives w_00, w_10, w_01 (fixed points
t = c . y_sigma(t) + d of the block's drive-line value functions y_sigma)
and one sign rho(sigma, w_01). For a TARGET orientation s* on the
(m+2)-cube, the set E(B, s*) of parameter vectors whose extension has
outmap s* is a semialgebraic set: the block's value functions y_sigma(t)
are concave piecewise-affine in t on the cells of the drive line
(rem:pinned-escape l.6740 prints the 13 fences of the level-two block
{c1,c2,c3,c6} driven by y_{c5}; scripts/round18-verify/dl_line.py
recomputes them and the per-cell affine pieces from
${REPO}/scripts/blowup/B2_small_nf.json), so once each of the 3 x 2^m
drives w_L(sigma) is assigned to a cell, every fixed point is a rational
function of the parameters and every bit P, Q, R, S of the theorem is a
polynomial inequality of low degree. The paper knows: thm:escape-no-beta
(l.6872: z = 24, 26 dead for every block; all four doublings dead when the
drive is alpha_2), thm:escape-mixed (l.6925: R_alpha - C_alpha must have a
negative component, and if R_alpha >= C_alpha componentwise an
up-closedness returns), cor:escape-m3 (l.6964: over the level-two block
z = 10 dead for an inner reason, z = 8 dead when R_alpha >= C_alpha; THE
ONE SURVIVING CORNER is z = 8 with R_alpha - C_alpha mixed in sign, where
rho(sigma, .) need not be concave; a floating-point search from several
thousand starts did not reach feasibility, the residual sitting at the
inner strategy sigma = 1; "a search is not a proof"). Read also
def:pinned, prop:pinned-level, lem:pinned-upclosed, thm:pinned-no-translate,
cor:pinned-no-doubling (l.6571-6740), prop:b2-realised (l.6202, the outmap
B^2 and the 138-vertex game), rem:b2-anatomy, prop:b3-outer (l.6533),
thm:blowup (l.5977, the table of outer bits by layer and parity),
rem:blowup-realise (l.6999), lem:switch, lem:readout (l.8739),
thm:readout-realise (l.8823). Round-18 drive-line route code (read-only):
${R18}/r18-drive-line/, its result ${REPO}/rounds/round18/results/ (the
file whose name starts with the route's title) and audits; the root
agent's scripts ${REPO}/scripts/round18-verify/dl_*.py.

WHAT TO PROVE:
 (A) THE CERTIFICATE FOR z = 8, MIXED SIGN, OVER THE LEVEL-TWO BLOCK. Write
     E := E(B_2, B^2(. xor 8)) with (alpha, beta) = (alpha_2, beta_2) as
     an explicit system: for each of the 8 inner strategies sigma the four
     bits (P, Q, R, S)(sigma) prescribed by the table of thm:blowup at the
     translated layer, the inner condition that s_B(w_L(sigma))(sigma)
     equals the target's inner part on each layer L, the substochastic and
     positivity constraints, nondegeneracy as strict inequalities. Then
     DECIDE E = empty by a certificate: branch on the cell of each drive
     (the drive line has 14 cells, so finitely many branches, most of them
     killed at once by the inner condition since each cell presents ONE
     orientation), and in each surviving branch the system is bilinear in
     (parameters, drives); linearise it (McCormick envelopes over the boxes
     [0,1], or eliminate the drives by the closed form of each fixed point
     and clear denominators) and produce a FARKAS CERTIFICATE of
     infeasibility of the linear relaxation in exact rational arithmetic
     (an LP dual vector; the paper has exact simplex in
     ${SCRATCH}/root16/mylp.py and lp.py). Infeasibility of a relaxation
     is infeasibility of E; a feasible relaxation is NOT feasibility ---
     refine (a second McCormick level, a split of the box) or find a
     genuine point. PROVE the McCormick inequalities you use (they are
     one-line). The deliverable is either (i) a finite case tree with a
     verified certificate at every leaf, hence THE THEOREM "no escape
     extension of the level-two block realises B^2(. xor 8)", completing
     cor:escape-m3 into a full negative answer for the published block, or
     (ii) a feasible point, i.e. an escape extension realising a doubling
     translate of B^2 --- then build the game (lem:dyadic-row after dyadic
     rounding, or lem:rational-row l.1112 for rational rows), verify the
     outmap from the game, and go to (C).
 (B) THE SECOND ESCAPE SHAPE. thm:escape-no-beta needs beta's switch action
     to read only the block. Drop that: let beta's action 1 read alpha too
     (weight A'' > 0), so that w_01 and w_11 differ. Write the level
     theorem for this shape (the analogue of thm:escape-level with four
     drives), prove it, and redo the tournament argument: which of the
     four doublings z in {8,10,24,26} survive it, for the drive as beta_2
     and as alpha_2? If some survive, repeat (A) for them over the
     level-two block.
 (C) BEYOND THE PUBLISHED BLOCK. The level-three question is a block with
     5 Max and 1 Min vertices presenting B^2 at one drive and B^2(. xor z)
     at another (rem:pinned-escape). State exactly which properties of a
     block's DRIVE LINE the outer constraints of (A)/(B) force --- the
     analogue of thm:escape-mixed(b) when R_alpha - C_alpha is mixed: what
     closure, if any, of {phi~ = 0} in the block's value order survives ---
     and prove it. If (A) gave a certificate, say which of its Farkas
     multipliers depend on the block's data and which are universal; a
     universal part is a theorem about every block.
 (D) If (A)(ii) happened: the same programme for the level-three shape
     (block = the whole 138-vertex level-two game minus its outer pair,
     drive = beta_3), at least the inner condition and the tournament.

KNOWN TRAPS FOR THIS ROUTE: the drive-line cells are open intervals and
the fixed point of one layer may sit on a fence (a tie), which
nondegeneracy excludes --- handle the boundary cases explicitly; the
block's value functions are concave piecewise-affine, so "affine on a
cell" needs the cell, not the whole line; thm:escape-level's uniqueness of
the fixed points uses |c|_1 < 1 --- keep it as a constraint; every game
you claim must be BUILT and its outmap verified from the game
(games_built field); a floating-point local search is exploration only.
The deliverable that counts is the certificate or the point; a theorem
about which bits are forced is a new-relation only if it goes beyond
thm:escape-mixed.` },
  { key: 'fold-feedback', title: 'A fold fed back into its own drive: can the affine cascade carry the counter, or is every feedback fold a cascade', brief: `THE OBJECT: a FOLD WHOSE DRIVE IS PRODUCED BY THE FOLD ITSELF.
prop:one-player-fold (l.16440) is OF(D): one-player, acyclic, N = 9D + 6,
in which the damping rho (def:discount-path) drives a tent-map cascade
psi_d = 2|psi_{d-1}| - 1 whose sign vector runs through all 2^{D+1}
strategies as rho sweeps [0,1]; rem:one-player-fold (l.16526) proves that
this path is never an all-switches run (the singleton {F_d} would be the
switched set 2^d times against cor:law-u), that under a FIXED strategy the
cascade is AFFINE (psi_d = 2 eps_{d-1} psi_{d-1} - 1, the absolute value
being a property of the greedy choice), and that all-switches halts on
OF(D) within D + 1 rounds (thm:component-bound, the game being acyclic);
its last sentence: "what survives is a fold fed back into its own drive".
The pivot (rem:blowup-realise l.6999, thm:seed-dichotomy l.15263, rem:wedge):
a stopping SSG family on which the all-switches run is superpolynomial in
N. Every such run is the bottom-antipodal walk of an AUSO of the Max cube
(prop:allsw-auso, thm:flat-resolution), so it needs m >= log_2(run) Max
vertices and, by thm:switch-count, a = omega(log N) average vertices; the
blow-up B(s) (thm:blowup) achieves 2h + 2 by two OUTER vertices that
switch in every round while the inner walk is run twice on translated
copies --- and realising its levels costs what rem:blowup-realise
describes (the anti-value obstacle). Read also thm:fold and rem:fold
(l.16175, 16232), prop:one-player-response (l.16251), prop:discount-fold
and rem:discount-fold (l.16319, 16392), prop:one-vertex-path, cor:law-u,
cor:no-return, cor:antichain, thm:peak-law, thm:component-bound,
lem:rise-bound, thm:switch-count, prop:leapfrog (SD(K): one Max vertex
switched K times on O(K^2) vertices), prop:serialiser, prop:closed-now-or-never
and rem:closed-now-or-never (a Max vertex over a Max vertex simulates a
third action with one round of lag), lem:max-tree, thm:stack (l.8422,
stacking adds runs but never per-state), the flip counts of a Max vertex
along the ladder run in rem:blowup-realise (3,4,4,4,7,8,8,8), thm:ladder
and rem:ladder (Melekopoglou-Condon's question: Howard's rule with two
actions per state --- a one-player superpolynomial all-switches family
would answer it). Code: ${REPO}/scripts/round18-verify/of_verify.py,
ofc_verify.py, fold1p_verify.py; ${R18}/r18-one-player-envelope/
(read-only); the all-switches driver in ${SCRATCH}/root16/mycore.py.

WHAT TO PROVE:
 (A) THE FEEDBACK MODEL. Define a FEEDBACK FOLD: the fold OF(D) (or the
     two-player fold P_D of thm:fold) in which the drive u_1 (payoff rho)
     is replaced by a vertex or gadget whose value is a monotone function
     of the fold's own values under the current strategy --- so that the
     strategy determines the drive and the drive determines the switchable
     set. Prove the basic identity: under strategy sigma the fold's
     values are affine in the drive t with the cascade slopes
     (rem:one-player-fold), so the switchable set at sigma is determined
     by comparing finitely many affine functions of t at t = t(sigma),
     and t(sigma) itself is the fixed point of a monotone map. Write the
     all-switches dynamics sigma -> sigma xor S_sigma of a feedback fold
     as an explicit map on the cube and the drive.
 (B) THE COUNTER, OR THE BARRIER. Either
     (i) design a feedback fold family (stopping; the feedback closes a
     cycle, so stopping must be arranged and PROVED by lem:trapchar) whose
     all-switches run from a stated start has length superpolynomial in N
     --- build the games, run the paper's all-switches on them in exact
     arithmetic at >= 5 sizes, PROVE the growth law (a recursion on the
     run of D + 1 from the run of D, as thm:blowup does for the height),
     and check the run against cor:law-u, thm:peak-law, cor:no-return at
     every size; a one-player such family answers Melekopoglou-Condon; or
     (ii) prove the BARRIER: for every feedback fold in your model the
     all-switches run is O(poly(D)), and say exactly which property of
     the model the proof uses (monotonicity of the drive in the values?
     the affine cascade? acyclicity of the fold minus the feedback edge?)
     and which known device escapes the model (the blow-up's outer pair
     switches every round: is it a feedback fold? show it is or is not).
     A barrier is a result only if it covers a device someone would try
     --- name it.
 (C) THE ROLE OF THE ANTI-VALUE. rem:blowup-realise: the inner game would
     have to read the anti-value val(j^0) + val(j^1) - val(j), strictly
     decreasing in val(j), which no vertex has; but the fold computes
     |a - b| = 2 max(a,b) - (a+b) from a Max and an average vertex, which
     is what a tent map needs. Prove or refute: a fold can present to a
     downstream vertex the SIGN of a difference of two of its own values
     as a value comparison (the readout Psi of thm:readout-realise with
     r = 1 pieces), and hence the layer parity that the blow-up's outer
     rule reads (prop:xor, thm:alternation-bits, cor:parity-unreadable ---
     which says NO AFFINE functional reads the parity; the fold is not
     affine in the strategy, it is affine in the drive). If the fold reads
     the parity, say what the blow-up costs per level with a fold as the
     readout (rem:blowup-realise's additive-cost question).
 (D) Verify every run on freshly built games (games_built), never from the
     recursion alone; report the runs at every size in the verification
     field with the exact strategy sequence for the smallest two.

KNOWN TRAPS FOR THIS ROUTE: a Max vertex whose options are a value and a
CONSTANT switches at most twice (lem:switch), so the drive must be a value;
the run is bounded by h*(m) <= 2^m and by N 4^a, so state m and a of every
instance; a "run" must be the paper's all-switches (sigma -> sigma[S_sigma]
with S_sigma the STRICTLY switchable set, Min playing a best response), not
a single-switch rule; feedback creates cycles, so verify stopping by the
trap test and compute val_sigma by the LP or the least fixed point, never
by greedy iteration; random search has never found a hard instance here.` },
  { key: 'hk-law-certificate', title: 'A law beyond Holt-Klee by an exact certificate: the realisation set of an orientation by one-player readout systems, uniform in the value configuration', brief: `THE OBJECT: the REALISATION SET of an orientation by ONE-PLAYER READOUT
SYSTEMS, as a semialgebraic set, and certificates of its emptiness that
are UNIFORM in the value configuration. thm:readout-realise (l.8823) with
lem:readout and lem:readout-reduce (l.8739): a nondegenerate one-player
stopping SSG with m Max vertices x_0..x_{m-1} presents, for each action
(v,a), an AFFINE substochastic readout Psi_{v,a}(x_{-v}) = p^{v,a} . x +
q^{v,a} (p^{v,a} >= 0 with p^{v,a}_v = 0, |p|_1 + q < 1 for leaking rows;
prop:hstar-one-eleven l.8611 prints such a system on five states with
denominator 2^13); the value configuration (x_sigma)_sigma satisfies
x_sigma(v) = Psi_{v,sigma(v)}(x_sigma) and the orientation is s(sigma) =
{v : Psi_{v,1-sigma(v)}(x_sigma) > x_sigma(v)}. So Real_1(s) = {(p, q, x)
: those equations and strict inequalities} is a BILINEAR semialgebraic
set (products p . x); prop:oneplayer-lp proves it lies inside Holt-Klee
(via the occupancy polytope: an LP orientation), and the paragraph after
thm:readout-realise says that for FIXED x the readouts are an LP, the
one-player case tying all gradients. rem:hk-survey (l.7082): at m = 4 all
6113 Holt-Klee classes were attacked, 5951 realised by exact dyadic
systems, 162 UNRESOLVED (heights 2 to 5: 12, 56, 69, 25; none of height
6); the smallest candidate for a further law is the Holt-Klee class
(8,9,10,11,13,12,14,15,7,6,4,5,3,2,1,0) of height 2 (outmap in the
paper's convention: s(sigma) as an integer bitmask, sigma = 0..15). At
m = 3 Holt-Klee IS the condition (prop:m3-realised). Read also
prop:hkfive (l.7278), rem:four-ceilings (l.7823), sec:deformed (why the
blow-up leaves Holt-Klee; lem:blowup-faces), thm:min-count (l.8880),
def:readout-system, the statement of Holt-Klee as the paper imports it
(grep 'Holt--Klee' near prop:oneplayer-lp l.5602) and the max-flow test
${SCRATCH}/solo/my_D.py; rem:choice-lift (l.15684) for the paper's use of
Balas' disjunctive closure. Code: ${SCRATCH}/solo/realiseAP.py (the
realisation LP at fixed x), census/classes4.txt (the 4-cube classes),
${REPO}/scripts/round18-verify/oc_verify.py (the 260-vertex check),
${R18}/r18-beyond-holt-klee/ (read-only: the 6113-class survey, the list
of 162 unresolved classes --- find and copy it), its result in
${REPO}/rounds/round18/results/.

WHAT TO PROVE:
 (A) THE SYSTEM. For the target class s_0 := (8,9,10,11,13,12,14,15,7,6,4,
     5,3,2,1,0) (check its Holt-Klee status and height yourself), write
     Real_1(s_0) explicitly: unknowns p^{v,a} in [0,1]^{m-1}, q^{v,a} in
     [0,1], x_sigma in [0,1]^m for all 16 sigma; equalities x_sigma(v) =
     p^{v,sigma(v)} . x_sigma + q^{v,sigma(v)}; strict inequalities for
     the orientation; substochasticity. State precisely which of the
     paper's realisation notions you decide (nondegenerate one-player
     stopping games = leaking dyadic systems, thm:readout-realise(b); or
     rational leaking systems via lem:rational-row l.1112; or systems
     without leak whose game is stopping --- rem:rational-row's trap
     hypothesis): the certificate must match the notion.
 (B) THE CERTIFICATE. Relax the bilinear terms p_u x_sigma(u) by McCormick
     envelopes over [0,1]^2 (prove the four inequalities) --- or by the
     level-one RLT products of the linear constraints --- and decide the
     linear relaxation by exact LP (${SCRATCH}/root16/mylp.py). If it is
     INFEASIBLE, extract the Farkas vector and READ THE LAW OFF IT: which
     constraints carry nonzero multipliers, on which faces of the cube;
     state the law as a combinatorial condition on orientations (a sign
     pattern on some 2- or 3-faces, a condition relating the sinks of
     faces sharing an edge, ...), PROVE that every one-player-realisable
     orientation satisfies it (directly from the readout equations, not
     from the LP), check it on all 5951 realised classes (they MUST pass)
     and on the 162 unresolved ones, and exhibit the Holt-Klee orientation
     that violates it (s_0, if it does). That is the deliverable: a
     necessary condition strictly beyond Holt-Klee, with a proof and a
     witness. If the relaxation is FEASIBLE, its x is a candidate
     configuration: run the exact realisation LP at that x (and at nearby
     rational x); a realisation reduces the 162; else tighten (a second
     McCormick level over a split box, or RLT level two) and iterate.
     Record what each level decides on the 162: how many are certified
     unrealisable, how many realised, how many left.
 (C) UNIFORMITY. The certificate of (B) is for one class; the law must be
     a statement about orientations. Test the law against the census: on
     the 3-cube every AUSO class is realised (prop:m3-realised), so the
     law must be VACUOUS at m = 3 --- check it; on the 4-cube count how
     many Holt-Klee classes it excludes and whether any realised class
     fails it (a failure refutes the law or the realisation --- rebuild
     that realisation from its system and check).
 (D) THE m = 5 COLUMN AS A TEST. prop:hstar-one-eleven realises a
     height-11 Holt-Klee class at m = 5. Does your law admit every
     realised m = 5 orientation you can find (the round-18 route's walk
     material in ${R18}/r18-beyond-holt-klee/) and does it exclude any
     Holt-Klee class of height 11 there (prop:hkfive: how many are there)?

KNOWN TRAPS FOR THIS ROUTE: infeasibility of a relaxation proves
unrealisability; feasibility proves nothing --- say which; the class must
be taken up to the 384 cube automorphisms (the paper's convention for
outmaps: grep prop:b2-realised and prop:hstar-one-eleven for the bitmask
convention, and state yours); a "law" that is Holt-Klee in disguise
(check: does it follow from Holt-Klee's statement in three lines?) is a
restatement; the McCormick relaxation of a product over [0,1]^2 is exact
at the box's corners only --- the relaxation can be feasible for every
unrealisable class, in which case say so and report what the level-two
relaxation does; verify any realisation you claim by BUILDING the game
(lem:dyadic-row) and computing its outmap from the game.` },
  { key: 'm6-walk', title: 'The flip graph of realised one-player orientations of the 6-cube: height 13, the height-14 blow-up made one-player, and whether ties beat 11 at m = 5', brief: `THE OBJECT: the FLIP GRAPH W_m of orientations realised by nondegenerate
one-player stopping SSGs with m Max vertices, whose edges are the
single-edge reversals along drive lines --- at a simple fence exactly one
edge of the cube ties and reverses (rem:pinned-escape l.6740, lem:switch),
and a single-edge reversal of a unique sink orientation stays one exactly
when the two endpoints have the same bottom-antipodal successor (checked
exhaustively at m <= 3 there) --- so that moving one row of a realised
system through a fence moves the orientation along an edge of W_m. The
round-18 beyond-Holt-Klee route found the height-11 five-state witness of
prop:hstar-one-eleven (l.8611: the system, denominator 2^13, the outmap,
the walk 10,17,6,21,22,24,4,8,12,28,30,31) by a guided walk through
realised orientations, and its walk at m = 6 towards a Holt-Klee class of
height 13 and towards the height-14 blow-up was CUT SHORT by its budget
(rem:hk-survey l.7082). The ceilings (rem:four-ceilings l.7823): h*_HK =
1,2,4,6,11,>=14,>=20; h*_1^nd = 1,2,4,6,11,>=12,>=13 with h*_1^nd(m) =
h*_HK(m) for m <= 5; h*(6) >= 16. THE TWO TARGETS AT m = 6: a nondegenerate
one-player game of height >= 13 (a new ceiling entry), and above all the
orientation s_6 of prop:hk-doubling-measured(b) (l.8161): the Holt-Klee
blow-up B_phi(s, 13) of the height-6 seed s = (0,1,3,2,6,13,12,7,14,9,8,11,
10,5,4,15) with readout phi of support {1,8,9,10,12}, height 14 = 2 h*_HK(4)
+ 2, which is prop:hk-records' s_6 --- a one-player realisation of s_6
would make the blow-up doubling ONE-PLAYER at the step 4 -> 6, a new
relation between thm:blowup and prop:oneplayer-lp (the paper's realised
doublings all need a Min vertex: prop:b2-realised, cor:seven-two-player).
Read also prop:oneplayer-lp (l.5602), thm:readout-realise (l.8823),
lem:readout, thm:stack and cor:stack-family (l.8422, 8506: stacking gives
slope 11/6 but never per-state gain), prop:oneplayer-plus-one,
prop:sink-lift, thm:no-seven and sec:ties (l.7113: no one-player game with
m = 4, degenerate or not, runs 7; thm:flat-resolution; def:flat;
thm:zero-timer), prop:hstar-five (l.5806: h*(5) = 12) and prop:hkfive
(l.7278: h*_HK(5) = 11). Code: ${R18}/r18-beyond-holt-klee/ (read-only:
the walk engine and its m = 6 state --- start from where it stopped),
${REPO}/scripts/round18-verify/H11_m5_GAME.json and oc_verify.py,
${SCRATCH}/solo/my_D.py (Holt-Klee by max-flow), realiseAP.py,
${REPO}/scripts/round16-verify/hkd_check.py (the blow-up engine),
${SCRATCH}/root16/auso.py and census/ (BA heights).

WHAT TO PROVE:
 (A) THE GRAPH AS AN OBJECT. Prove: (a) along a drive line (one row of a
     realised system moved continuously in one coordinate, or the whole
     system moved along a segment), the orientation changes only at
     fences, and at a simple fence by exactly one edge reversal
     (lem:switch); (b) the single-edge-reversal criterion for staying a
     unique sink orientation, in general (the m <= 3 check of
     rem:pinned-escape is a measurement --- prove the criterion or give the
     counterexample); (c) hence W_m is a subgraph of the flip graph of
     AUSOs and every realised orientation reached by a walk comes with a
     realised system --- the walk is a proof device, not a heuristic.
     State what is open: is W_m connected? is every Holt-Klee class
     reachable from the trivial orientation?
 (B) THE WALK AT m = 6. Resume the guided walk (heights as the guide,
     Holt-Klee as the filter, the exact LP at each step). Targets in
     order: any class of height >= 13 realised (build the game by
     lem:dyadic-row, verify the outmap and the run from the game, print
     the system as prop:hstar-one-eleven does); then s_6 itself ---
     compute its Holt-Klee status and height yourself, then walk towards
     it (the edge-flip distance to s_6 as the guide) and at every visited
     orientation within distance 3 of s_6 run the exact realisation LP on
     s_6 directly at that system's value configuration and at the
     configurations of its neighbours. A realisation of s_6 is the
     headline; state exactly what it makes one-player.
 (C) TIES AT m = 5. thm:no-seven closed the degenerate question at m = 4.
     At m = 5, h*(5) = 12 > 11 = h*_HK(5): can a DEGENERATE one-player
     stopping game have a run of length 12? Its flat resolution
     (thm:flat-resolution) would be a height-12 AUSO of the 5-cube (list
     them: prop:hstar-five), none Holt-Klee. Decide it by the method of
     thm:no-seven (read its proof at sec:ties) extended to m = 5, or by an
     exact LP with non-strict inequalities at the tied incidences for
     each height-12 class and each way of resolving its ties into a run
     of length 12 --- a certificate per class, or a degenerate game
     running 12 (build it, verify the run FROM THE GAME with the paper's
     tie convention). Either outcome is a theorem; a search cut short is
     not.
 (D) Report, in the verification field, the heights reached at m = 6 and
     the systems (denominators, leaks), and put every game in
     games_built.

KNOWN TRAPS FOR THIS ROUTE: heights are bottom-antipodal heights of the
improvement outmap, computed by the paper's auso.py convention --- state
the convention and the start vertex (the ceiling is over all starts); a
system must LEAK on every row and be dyadic to be a game by lem:dyadic-row
(or rational via lem:rational-row l.1112 with its stopping hypothesis);
nondegeneracy means no tied incidence at ANY strategy (check all 2^m x m);
"the walk found nothing" is not a result --- (A) and (C) are where the
theorems are; blind search at m >= 5 has failed for hours in this project
(the DEAD list), so keep the walk GUIDED and report its state so the next
round can resume it.` },
  { key: 'promise-gap', title: 'The promise problem: is deciding val(v0) >= 1/2 + eps against <= 1/2 - eps polynomial for eps = 1/poly, target-equivalent, or neither provably', brief: `THE OBJECT: the PROMISE PROBLEM Gap_eps and the eps-ORDER LADDER.
rem:eps-ladder (l.12995): with eps(N) nonincreasing, log(1/eps) = poly(N),
Ord_eps (a total preorder on Vavg u {t0,t1} correct on pairs eps apart),
App_eps (every value to within eps) and Gap_eps (the bit of val(v0) >= 1/2
with either answer allowed within eps of 1/2) are interreducible up to
constant factors in eps (for dyadic eps; the four reductions are stated
there: binary search against spliced dyadic reference chains, sorting, one
query against m -> (t0,t1), the difference vertex of lem:duality). THE TWO
KNOWN ENDS: for eps <= 2^{-N^gamma} the fragment is target-equivalent by
padding (lem:denominator-sharp: the value gap is at least 4^{-a}); for
eps > 1 - 2^{-(N-2)} it is the qualitative preorder of prop:qualitative.
THE OPEN MIDDLE: eps = 1/poly(N), or eps = 1/4 --- "exactly whether
prob:main reduces in polynomial time to its own promise version". What
constrains a reduction: rem:no-amplification (l.4428) proves that a
BLACK-BOX context on s vertices reading a plugged-in game through its gate
multiplies a value gap by at most (4/3)(s+3) (the energy identity
thm:energy, lem:gate, thm:two-exit), the gambler's-ruin chain attaining
Theta(s) --- so amplifying 2^{-a} to 1/poly by composition costs 2^{a}
vertices; nested compositions and outputs read inside the copies are NOT
covered, and every transformation of the paper (thm:stopping-transform,
thm:compare-equivalence, lem:normalform, thm:top) reads the edges and is
outside the bound's scope. On the algorithmic side: thm:vi-lower (value
iteration needs 2^{Omega(N)} steps with no players --- for the exact value;
what it needs for App_eps at eps = 1/poly is a question), thm:contraction
(rate 1 - 2^{-a}), thm:escape-class (an escape certificate (lambda, x)
gives two-sided value iteration in O((a + log kappa)/log(1/lambda)) rounds
--- the class where App is cheap), thm:few-denominator and
thm:alphabet-iteration (exact from a grid), lem:round-recover (Legendre:
exact values from approximations to within the denominator gap),
thm:one-player (LP), prop:bracket (l.12951: certificates for the exact
order are as hard as the problem), rem:order-unique, thm:order-determines,
prop:no-halving. Prior art from memory, unchecked: Condon 1992 on the
value gap; Dai-Ge on approximation collapse at exponentially small eps ---
say what you remember and flag it. Code: ${REPO}/scripts/round18-verify/
wo_verify.py, wo_lip.py; ${R18}/r18-weakest-oracle/ (read-only).

WHAT TO PROVE (any one of the three, honestly labelled):
 (A) POSITIVE: a deterministic polynomial-time algorithm for Gap_{1/poly}
     (or Gap_{1/4}) on stopping SSGs, from first principles. Candidates
     to test, each of which must be PROVED or REFUTED with an instance:
     (a) value iteration for poly(N)/eps rounds decides Gap_eps --- refute
     or prove (the paper's slow blocks G_n of thm:vi-lower have values
     2^{-n}: what is their App_eps cost?); (b) the stopping-probability
     path (def:discount-path) at rho = 1 - eps/poly: is w_rho within eps
     of w* with rho = 1 - 1/poly? (the survival time can be 2^{a}: prove
     the bound or the counterexample); (c) an LP or convex programme
     whose optimum is within eps of the value --- the transport programme
     over Q(G) is exact on successor-closed average parts
     (lem:transport-exact) and off by 1/2 on W_14: what is its worst
     error as a function of N? (d) any new idea. A polynomial algorithm
     for Gap_{1/4} would be the strongest positive result of the project;
     a proof that each candidate fails at eps = 1/poly, with explicit
     families and growth laws, is a new barrier IF it covers a natural
     approximation scheme (name the scheme; measure at >= 5 sizes; prove
     the law).
 (B) NEGATIVE: a polynomial-time many-one reduction SSG-Value <= Gap_eps
     for some eps = 1/poly (target-equivalence of the whole middle). It
     must read the edges (rem:no-amplification forbids black-box
     amplification); prove exactly what it does to the value and why the
     bit is preserved. Two starting ideas to test rigorously: (a)
     amplification by RESTARTS that read the structure (on reaching t0
     restart from v0 with probability r: the value becomes p/(1-(1-p)r),
     a Moebius map of derivative 1/(1-(1-p)r)^2 --- bounded by (4/3)(s+3)
     if black-box; is there a non-black-box restart scheme, e.g. into
     intermediate vertices whose values you know relative to v0, whose
     amplification exceeds the bound?); (b) the denominator: the value
     lies on a grid of mesh >= 4^{-a} (lem:denominator-sharp); can
     App_{eps} on POLYNOMIALLY MANY derived games (different sink payoffs
     or plugged constants, all read from G) pin the grid point? Prove or
     refute: an eps-approximation of val on G and on the games G_theta
     with t1 replaced by a dyadic theta (or v0 by a difference vertex)
     determines val exactly for eps = 1/poly.
 (C) A THEOREM LOCATING THE MIDDLE: e.g. Gap_{1/poly} in P iff Ord_{1/poly}
     in P iff App_{1/poly} in P is already in rem:eps-ladder; go beyond
     it: prove that Gap_eps for eps = 1/poly is equivalent to the exact
     problem on a NAMED subclass (e.g. games with a = O(log N) are exact
     by thm:few-avg, so nothing there; games whose value gap at v0 is
     >= 1/poly are Gap-decidable trivially by an exact algorithm ---
     which is the point: prove or refute that the value gap
     |val(v0) - 1/2| is >= 1/poly on some structural class where exact
     solving is not known polynomial), or prove that the zero-error
     randomised complexity of Gap_{1/4} is polynomial (random-facet is
     e^{2 sqrt n} for exact: does the promise help it? PROVE the
     recurrence you claim).

KNOWN TRAPS FOR THIS ROUTE: Gap is a PROMISE problem --- an algorithm may
answer anything inside the gap, and a reduction must map instances
outside the promise to instances outside the promise; eps must be a
function of N, stated; "approximation within eps" in the additive sense,
values in [0,1]; any use of an LP solver's polynomiality is an
assumption to state; a Moebius amplification p -> p/(1 - (1-p) r) is
black-box and rem:no-amplification bounds it; the paper's transformations
move the threshold to an explicit dyadic theta (thm:stopping-transform),
keep that in mind when composing; prior art (Condon's gap, approximation
results) from memory only, flagged, never a proof.` },
  { key: 'extension-complexity', title: 'Extended formulations: the value polytope, the exactness level of the choice-variable hierarchy as a growing function, and what no polynomial-size LP can project to', brief: `THE OBJECT: EXTENDED FORMULATIONS. Two polytopes attached to a stopping
SSG G: (1) the VALUE POLYTOPE V(G) := conv{val_sigma : sigma in {0,1}^m}
in [0,1]^V (with Min playing optimally against each sigma; its profile
version V_C(G) := conv{val_{sigma,tau}} over all positional pairs), whose
coordinatewise maximum is w* = val_{sigma*} (thm:opt-subcube,
thm:determinacy) so that deciding val(v0) >= 1/2 is deciding max_{V(G)}
x(v0) >= 1/2; and (2) the CHOICE-VARIABLE HIERARCHY R_j(G) of
rem:choice-lift (l.15684): each controlled row x(v) = y_v x(v^0) + (1-y_v)
x(v^1) with y_v in [0,1], level-j Sherali-Adams over the y's, level zero
= Q(G) (def:transport l.15398, lem:transport-dim, thm:transport-objective:
w* is a vertex of Q(G) and the unique point of Q(G) with every
controlled row tight at one action, since the complementarity sum q is
>= 0 on Q(G) with q = 0 only at w*), level one = Balas' disjunctive
closure. Known: level one fails on W_14 (a five-point certificate) and is
asymptotically vacuous on the router tree T_d(e,kappa) (prop:router-tree
l.15722: max_{R_1} x(root) >= 1 - Theta(1/N) against w* = kappa, with
ONE player and a = e + D CONSTANT average vertices); rem:merged-matrix
(l.15790): with one player every x in R_1 has D := x - w* >= 0 and
D <= M D for the merged matrix M, so R_1 = {w*} whenever M is transient,
in particular when no Max vertex is a splitter; the route's claim
"exact at level >= min(|Vmax|, rho + 1)" is UNPROVED and recorded as a
claim; exactness at any fixed level is target-equivalent and not
conjectured; thm:lasserre-vacuous (l.15572): the degree-two Lasserre lift
of Q(G) adds nothing on W_10 and W_14. DEAD in the paper: vertex
enumeration of Q(G) (exponentially many vertices on linear-time
instances). What the paper does NOT have: the polytope V(G) at all; any
level lower bound growing with N; any nonnegative-rank / extension
complexity statement. Read also thm:one-player (one player: w* is the
least element of Q(G), an LP), rem:transport-objective (naming an optimal
profile is target-equivalent), prop:oneplayer-lp (the occupancy polytope
X(G) of d'Epenoux, whose vertices are the 2^m strategies), sec:projection
(thm:profile-uso, prop:lcp: the profile cube as a P-matrix LCP),
rem:lcp. Code: ${REPO}/scripts/round18-verify/rl_verify.py (the level-one
lift as one exact LP by Balas' homogenisation), ${REPO}/scripts/
round17-verify/cl_verify.py; ${R18}/r18-rlt-two/ and ${R17}/r17-convex-lift/
(read-only).

WHAT TO PROVE:
 (A) THE LEVEL AS A GROWING FUNCTION. Define lev(G) := the least j with
     R_j(G) = {w*} (state the level-j lift precisely: which products,
     which linearisation --- the paper defines levels zero and one only;
     define level j so that level one agrees with Balas' closure and
     PROVE that agreement). Then PROVE a growth law: a family G_n, built
     as games and verified, with lev(G_n) >= f(n) -> infinity (f = Omega(n),
     or Omega(log n), or Omega(sqrt n) --- say which and prove it), by an
     explicit feasible point of R_{f(n)-1}(G_n) other than w* whose
     membership is certified level by level (the router tree gives level
     one; a tree of depth d with d independent splitters is the natural
     candidate for level d --- prove or refute that the merged-matrix
     bound and its higher-level form of rem:merged-matrix bound lev from
     above by the number of splitters, and find a family where the number
     of splitters and lev both grow). A proved lev(G_n) = Omega(n) on a
     ONE-PLAYER family is a new barrier: the hierarchy has no fixed exact
     level even where the problem is an LP.
 (B) THE VALUE POLYTOPE. Prove from first principles the factorisation
     theorem you use (an extended formulation of size r exists iff the
     slack matrix of P has nonnegative rank <= r, both directions --- half
     a page each; Yannakakis, from memory, flag it) and then: (a) compute
     V(G) exactly (vertices, facets, slack matrix, nonnegative rank
     bounds by rectangle covering / fooling sets) on the paper's small
     instances (the ladder L_n at n <= 5, WD(e,j,m), the seven-vertex game
     of rem:own-stall, W_14, G8); (b) prove a LOWER BOUND on the
     extension complexity of V(G_n) for an explicit family (a fooling set
     of exponential size in the slack matrix is the standard route; the
     ladder's 2^n distinct value vectors are the candidate) --- and then
     say honestly what it means: V(G) for a one-player game is
     computable by LP as far as its coordinatewise maximum goes, so an
     exponential xc(V) is a statement about a polytope, not about the
     problem, UNLESS you can prove (c) that some polytope whose
     polynomial extended formulation would put SSG-Value in P has
     exponential extension complexity --- state such a polytope (the
     convex hull of the (sigma, val_sigma) pairs? the profile polytope
     V_C?) and prove either the equivalence or the bound.
 (C) THE ONE-PLAYER SIDE, TO CALIBRATE. With Vmin empty, is V(G) the
     projection of the occupancy polytope X(G) (d'Epenoux) under an
     affine map --- i.e. does V(G) have a polynomial-size extended
     formulation for one player? Prove or refute with an instance
     (the ladder). If yes, the one-player value polytope is small and
     (B)(b) must use two players; if no, xc(V) is not the obstacle and
     say so.

KNOWN TRAPS FOR THIS ROUTE: R_j must be defined as a linear programme of
size N^{O(j)} whose exactness is what you bound --- a hierarchy that is
exact at level one by definition on one-player games (min over Q) is not
the question, the MAX side is (prop:router-tree bounds max_{R_1});
"exponential extension complexity" of a polytope nobody optimises over is
not a barrier --- (B)(c) is the only form that counts against the
problem; every feasible point you exhibit in a lift must be certified by
the lift's own linear constraints in exact arithmetic (the paper's
five-point certificate style), not by a solver's status; a family must be
built as games and verified (games_built), with >= 5 sizes and a proved
growth law.` },
  { key: 'handicap-tangent', title: 'The handicap-zero class against its own cut: a family silent under the tangent cut, or a proved rate on the strongly convex slice with a member outside the eight classes, and the damping closure of R', brief: `THE OBJECT: the class R := {stopping SSGs whose harmonic normal form over
C has B := sym(R_0^T R_1) >= 0} of rem:handicap-base (l.9319), on which the
complementarity sum q(x) = sum_v (x(v) - x(v^0))(x(v) - x(v^1)) is CONVEX
on Q(G) with unique zero w*, its strongly convex slice R_lambda := {B >=
lambda I}, and the TANGENT CUT M7 of rem:tangent-cut (l.17159): keep the
Z-seeded transport polytope, test the three readings of the standing rule
over it each round, and adjoin the tangent cuts nabla q(x).(y - x) <= -q(x)
at the 8|C| lexicographic optima of (+-g_{v,i}, +-x(v)) (a fixed tie-break
is part of the definition; q(y) = q(x) + nabla q(x).(y-x) + |y-x|_B^2 on
the affine hull of Q(G)). Known: M7 is sound on R, lies outside the
language of thm:convex-barrier-both (l.17134: its certificate method bounds
pairwise differences, a tangent cut is an affine inequality in all of x),
decides WD(e,j,m) at round one and vertex 4 of the seven-vertex game of
rem:own-stall, and BC(2,s) at round one or two by the tie-break; WD and
CC(L,m) lie in R with B printed (lambda_min = 2^{-(e+j)} and 2^{-3L}),
BC(e >= 3, s) and CV(e,s) lie outside; the boundary of R is attained
(prop:handicap-singular l.9374: B singular on an 8-vertex stopping game);
HZ(n) (prop:hz l.9393) is in R with lambda_min(B) = 1/4 for every n,
outside every named bound as presented, yet polynomial by a reduced
1/2-contraction (lem:readout with C pinned; a companion to
prop:a-presentation) --- so it is NOT the member of R outside the tractable
classes that rem:handicap-base asks for; "no family designed against the
cut exists yet". Membership in R is a property of the presentation (the
subdivision carries 16 of 181 members out). rem:signdef's damping-closure
claim was struck in round 17 (a 9-vertex counterexample for
sign-definite games); whether R is closed under Condon's damping
(def:damping, def:discount-path: every step survives with probability
rho) is open. Read also thm:transport-objective, lem:transport-dim,
def:transport (l.15398), rem:own-successor / prop:own-stall / rem:own-stall
(sec:wedge l.18298), def:wedge and thm:wedge-proved, lem:wedge-verts,
def:wedge-chain (the certificate chain), sec:bc (BC(e,s), thm:bc-lower),
def:cv, thm:hybrid-convex-barrier (the method for lower bounds),
prop:lcp and rem:lcp (P-matrix LCP, handicap: prior art, closed as not
ours), lem:round-recover (exact values from approximations). Code:
${REPO}/scripts/round18-verify/hz_wedge.py, hz_ring.py, hz_w7.py, hz_bc.py,
hzlib.py (the root agent's implementation of M7 --- READ it for the
paper's tie-break), ${REPO}/scripts/round17-verify/ (BC_*, CVX4, CVX6 game
files), ${R18}/r18-convex-class/ (read-only).

WHAT TO PROVE:
 (A) THE FAMILY AGAINST THE CUT. Design a family in R (B >= 0 VERIFIED from
     the normal form at every size) with a value-distinguishing controlled
     vertex at which M7 --- with the three readings, Z-seeded, the paper's
     tie-break --- is silent for a number of rounds superpolynomial in N,
     and PROVE it. The certificate method of thm:convex-barrier-both cannot
     bound an affine cut, so you need a new method: e.g. a nested sequence
     of convex sets P_k containing w* and the cut points of round k, on
     which every tangent cut is implied by the constraints of P_{k+1}
     (Kelley's method has known slow instances --- from memory, flag ---
     where the cut points stay on a face far from the optimum); design so
     that the lexicographic optima sit where q is exponentially small
     (q(x) >= |x - w*|_B^2 with lambda_min(B) exponentially small along a
     near-kernel direction: the cut's depth is q(x)). Measure at >= 5
     sizes with the root agent's hzlib.py (state the tie-break), then
     PROVE the growth law. This is the deliverable that counts on the
     negative side.
 (B) THE RATE ON THE STRONGLY CONVEX SLICE. On R_lambda, q is
     lambda-strongly convex on the affine hull of Q(G) and w* is its
     minimiser over the polytope Q(G). PROVE a first-principles bound on
     the number of rounds of a cutting-plane or projection method that
     reaches q(x_k) <= 2^{-poly} --- polynomial in N and 1/lambda --- and
     then recover w* exactly by lem:round-recover (values on a grid of
     mesh >= 4^{-a}). State every assumption (exact LP solving as a
     primitive? bit sizes of the iterates? --- Kelley's method has no
     polynomial rate in general; the ellipsoid method or a central-cut
     scheme does, from memory, flag; prove what you use, or mark the
     GAP exactly). Result: R_lambda with lambda >= 1/poly(N) is a
     POLYNOMIAL CLASS (a class defined by a spectral condition on the
     normal form). Then the question rem:handicap-base asks: EXHIBIT a
     member of R_{1/poly} outside the eight classes and outside
     prop:hz's reduced-contraction trick, on the subgame reachable from
     v0 --- prove membership and non-membership --- or prove that every
     member of R_lambda is solved by a reduced contraction of rate
     depending on lambda (which would make (B) a restatement of prop:hz's
     mechanism: say so).
 (C) THE DAMPING CLOSURE. Prove or refute: if G is in R then G_rho
     (def:discount-path) is in R for every rho in (0,1); and the same for
     the stopping transformation of thm:stopping-transform. A refutation
     needs an explicit game with B >= 0 and B_rho not >= 0, verified in
     exact arithmetic with the eigenvalue certificate (a negative
     Rayleigh quotient), and the smallest such.
 (D) The 7-vertex game of rem:own-stall is in R; is the class of games at
     which all three readings are silent at round zero but M7 decides at
     round one characterisable (a property of the lexicographic optima)?
     A theorem here is a new-relation; a list of instances is not.

KNOWN TRAPS FOR THIS ROUTE: B is computed in the harmonic normal form
over C (first-passage rows), not on the raw game; membership is checked on
the reachable subgame; the cut points are the lexicographic optima of the
Z-SEEDED polytope --- unseeded runs are a different mechanism; a stall
needs all three readings AND the cut silent at a value-distinguishing
vertex; a class must have a member outside thm:few-avg, thm:few-escape,
thm:kacyclic, thm:bounded-components, thm:escape-class,
thm:few-denominator, thm:modulator, thm:qp, min(m,k) = O(log N) and
prop:hz's contraction, all on the reachable subgame; every family built
as games (games_built), >= 5 sizes, proved growth law.` },
  { key: 'fresh-19', title: 'A blind route: a formulation of the problem outside every approach family of the inventory', brief: `THE OBJECT: YOURS TO CHOOSE, subject to one rule: it must lie OUTSIDE every
approach family the inventory already holds. Read ${SCRATCH}/round19/
inventory.txt in full first. The families already tried, across eighteen
rounds (each with its results in frontier.tex): monotone fixed-point theory
of the Shapley operator; stopping transformations and denominators;
polynomial classes by cycle colours, components, escape certificates,
denominators, modulators, treewidth; the structure of the optimal set and
short improving paths; switching rules (all-switches, single-switch,
least-index, smallest-gap, bidirectional, best-response restart) and their
laws; the AUSO / bottom-antipodal identification, Holt-Klee, blow-ups,
readouts, realisation; propagation calculi (simulation preorder, slack,
min-plus closure, ratio, Moebius continuum), policy-evaluation seeding,
the transport LP, the transport-slack hybrid, the tangent cut; convex
lifts (Lasserre degree two, Sherali-Adams over choice variables, Balas);
LCP / Lemke / handicap / P-matrix and interior point; homotopies (bias,
stopping probability, damping) and folds; query and evaluation models;
the order lattice and unique certificates; variational / energy /
reversibility; oracle hierarchies and partial information; realisation
spaces as semialgebraic sets; random facet and subexponential bounds;
Newton-Dinkelbach, nonlinear Perron-Frobenius, Schur elimination, softmax
regularisation, symmetric improvement, UEOPL, submodularity, deformed
products, extension complexity and the promise problem (this round's
other routes). You are NOT told which of these the root agent favours,
and you should not care.

WHAT TO DO:
 (A) Choose a formulation the list does not contain --- an algebraic,
     automata-theoretic, combinatorial, probabilistic, geometric or
     complexity-theoretic view of the object "value of a stopping SSG"
     or of the object "the switchable set as a function of the strategy"
     that no listed family uses --- and say in the object field what it
     is and why it is not one of the listed families under another name.
 (B) Prove something about the problem THROUGH it: a theorem, a
     construction, a refutation, with the same standard as every route
     (exact arithmetic, first principles, the novelty pre-check per
     result, games built for every instance). A statement of the same
     strength as the target (see the REFORMULATIONS list in the digest)
     is a dead-end unless you supply a genuinely new proof of it.
 (C) If your formulation collapses onto a listed family, PROVE the
     collapse (that is a result) or report it as a dead-end; do not
     dress it up.

KNOWN TRAPS FOR THIS ROUTE: the digest's REFORMULATIONS AND EQUIVALENCES
are all target-equivalent --- ending at one of them is ending at the
target; the eight polynomial classes and the trivial min(m,k) = O(log N)
must be excluded, on the reachable subgame, for any class you claim;
prior art from memory is flagged and is never a proof; random sampling
finds nothing here; a barrier must cover a rule someone runs.` },
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
   the route's code, in ${SCRATCH}/r19-audit-${r.key}-correctness/. If a
   claimed family, instance, relaxation value, breakpoint count, query
   bound or realisation does not reproduce, that is FATAL and you must give
   the discrepancy explicitly. Recompute at least three rows of any table.
3. Hunt for the project's standing errors: greedy policy iteration in a
   non-stopping game; dict-literal rows collapsing; fresh vertices
   colliding with the sinks; t0 excluded from the trap; a stall claimed
   without testing all three readings of the standing rule (own-successor
   (i), (ii) and the non-strict pair test), Z-seeded, with the PAPER'S
   definitions rather than the route's own driver;
   the Z_0/Z_1 seed omitted; a vacuous stall; a parameter held constant;
   unreachable vertices used to separate a family from a class; unpinned
   sink payoffs; a non-productive round counted; a non-dyadic "witness";
   a "polynomial class" inside thm:few-avg, thm:few-escape, thm:kacyclic,
   thm:bounded-components, thm:escape-class, thm:few-denominator,
   thm:modulator, thm:qp or the trivial min(m,k) = O(log N); an IMPORTED
   theorem beyond the four allowed, used without proof; a family whose
   members were never ASSEMBLED AS GAMES (check the games_built field:
   round 18's eval-decision route verified harmonic systems only) -- if
   the route built no game, build the smallest members yourself and
   check them from the game; a McCormick or RLT relaxation whose
   FEASIBILITY is read as feasibility of the original system.
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
standard of rounds 17 to 19, and to say so bluntly.

${COMMON}

# The work under audit (route "${r.key}": ${r.title})

${res}

# Your task: NOVELTY AND SIGNIFICANCE

1. THE NOVELTY TABLE (mandatory). For EVERY entry of results AND of
   restatements, do your OWN search of ${SCRATCH}/round19/inventory.txt and
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
   lem:readout, thm:matching-barrier, thm:profile-uso, prop:lcp's
   monotone-LCP dictionary, thm:top and prop:no-halving as new; in
   round 17 five of seven routes reported restatements as results, and
   in round 18 three of seven routes were dead-end or blocked under the
   rubric while FOUR HEADLINES were false over sound mathematics: audit
   the headline sentence as a claim of its own, and say whether the
   results as proved support it. Also flag anything that is
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
3. CONSISTENCY. Every \\Cref in the added text must point at a result that
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

log(`Round 19: ${ROUTES.length} routes on Opus 5 at effort high: ${ROUTES.map(r => r.key).join(', ')}; correctness + novelty audits on Opus 5; one paper audit (round-18 diff) on Opus 5.`)

const PACING = `PACING: a route of round 18 died because one reasoning turn exceeded the ` +
  `output-token limit; think in short steps, write every intermediate definition, ` +
  `lemma and computation into files in your directory as you go, and never try to ` +
  `settle a whole question in one turn.`

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\n\n# YOUR ROUTE: ${r.title}\n${r.brief}\n\n` +
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
      agent(L.prompt(r, text) + `\n${PACING}`, { label: `audit:${r.key}:${L.key}`, phase: 'Audit', schema: AUDIT_SCHEMA, model: 'opus', effort: 'high' })
    )).then((audits) => ({ route: r.key, result: res, audits: audits.filter(Boolean) }))
  }
)

const paperWork = agent(paperAuditPrompt(PAPER_AUDIT) + `\n${PACING}`, { label: `paper:${PAPER_AUDIT.key}`, phase: 'Paper audit', schema: AUDIT_SCHEMA, model: 'opus', effort: 'high' })
  .then((a) => (a ? { section: PAPER_AUDIT.key, audit: a } : null))

const [results, paper] = await Promise.all([routeWork, paperWork])
const good = results.filter(Boolean)
log(`Round 19 complete: ${good.length}/${ROUTES.length} routes returned; paper audit ${paper ? 'returned' : 'missing'}.`)
return { round: 19, routes: good, paper }
