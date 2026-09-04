export const meta = {
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

${REPO}/frontier.tex is a 229-page LaTeX development of 503 numbered
results (17759 lines) built over seventeen multi-agent rounds and one solo
round by the root agent. Every claim in it is proved and every negative
claim carries an explicit instance verified in exact rational arithmetic.
It contains NO polynomial-time algorithm for the general problem and
claims none. Read the parts you need with grep/sed; do NOT read the whole
file. THE INVENTORY ${SCRATCH}/round18/inventory.txt lists every numbered
result as "L<line> <env> <label> :: <title>", grouped by section: read it
in full FIRST (it is short) and use it for the novelty pre-check below.
Sections and their first lines: Introduction (l.269); The problem (l.271); What is proved here, and what is not (l.349); The Shapley operator (l.436); Stopping games (l.750); The quantitative stopping transformation (l.986); A polynomial special case (l.1311); The value alphabet (l.2455); Width: the search is quasipolynomial, the tables are not (l.2971); The structure of the optimal set (l.3361); Composition, and an energy identity (l.3983); Refutations and barriers (l.4155); Ties in one-player games (l.6533); Deformed cubes, and why the blow-up leaves the Holt--Klee class (l.6969); One player: Howard's rule with two actions, sign-definite games, and stacking (l.7707); Readouts: what a game presents to its Max vertices (l.8060); The profile cube and its sink projection (l.8381); Lemke's algorithm as a bias homotopy (l.8709); The induced orientation of the two-player cube can be cyclic (l.11181); Value iteration is exponential already without players (l.11316); Improving switches need not point toward the optimal set (l.11414); The selection problem is the whole problem (l.11738); A subexponential upper bound (l.12236); The remaining gap (l.12592); A global mechanism that beats locality (l.12915); Adding arithmetic: the slack calculus (l.13154); The branch-compensation barrier (l.14258); Seeding from policy evaluation (l.14396); Freezing one vertex: the response map folds (l.15217); Coupling the two: the transport--slack hybrid (l.15433); A one-player family the whole propagation side loses on (l.16570); The own-successor rule, and a wedge that defeats it (l.17101); Summary (l.17421).

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
   grep ${SCRATCH}/round18/inventory.txt and ${REPO}/frontier.tex for the
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
   (B2_small_GAME.json, Blowup.lean, README.md). Round-17 route code and audits, read-only, are under ${R17}/r17-<key>/
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
   COPY what you need into ${SCRATCH}/r18-<your-route>/ and work there. Do
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
   returning (round 16 left sixteen jobs running for five hours; round 17 left a monitor loop) and leave
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
  { key: 'drive-line', title: 'The drive line of a driven block: the orientations a block presents along its drive, what a doubling translate costs on it, and the escape shape at the third level', brief: `THE OBJECT: the DRIVE LINE of a driven block. A driven block (def:pinned)
is a harmonic normal form on m Max and k Min vertices whose rows may read,
with nonnegative weights, one external coordinate beta (the drive); frozen
at y_beta = t it is a stopping game with improvement outmap s_B(t) on the
m-cube. The drive line is the step function t -> s_B(t) on [0,1]; its
FENCES are the values of t at which some incidence (sigma, v) ties. The
paper prints two exact fences of the level-two block {c1,c2,c3,c6} driven
by y_{c5} (rem:pinned-escape: outmap B^1 on [0, 47723619/255897160) and
B^1(. xor e_{beta_1}) on (1175936917/2026652880, 10168377/16341335)) and
proves everything it knows about the PINNED shape: prop:pinned-level
(C1)-(C5), lem:pinned-upclosed, thm:pinned-no-translate,
cor:pinned-no-doubling (pinned on pinned cannot present a doubling
translate z in {8,10,24,26} of B^2, so B^3 is out of that shape's reach;
best doubly pinned 7-cube height 16, realised 12 by prop:b3-outer),
rem:pinned-escape (the escape: an outer vertex whose REST action reads the
block, so the switchability condition becomes a difference of two monotone
functionals and lem:pinned-upclosed says nothing; and THE QUESTION: can a
driven block that is NOT pinned present B^2 at one drive and B^2(. xor z)
at another for a doubling z?). Read also prop:b2-realised, rem:b2-anatomy,
rem:blowup-measured, prop:blowup-readout, prop:parity-readable, thm:blowup,
prop:blowup-height, rem:blowup-realise (the pivot's open question and the
anti-value obstruction), thm:readout-realise, lem:readout, lem:dyadic-row,
thm:min-count, cor:b2-min, prop:xor, lem:switch, lem:crossing. Round-17
realisation-space route: ${R17}/r17-realisation-space/ (read-only), its
result ${REPO}/rounds/round17/results/07_*.json and audits 11_*, 18_*;
the round-16 b3-level route ${R17}/b3-level/; the game files
${REPO}/scripts/round16-verify/TB_GAME_D10.json (194 vertices),
${REPO}/scripts/round17-verify/B2_pin137_GAME.json, ${REPO}/scripts/blowup/.

WHAT TO PROVE:
 (A) THE DRIVE LINE AS AN OBJECT. Under a fixed inner strategy sigma the
     block's values are nondecreasing functions of t (affine when k = 0;
     a minimum over Min's responses in general -- concave piecewise
     affine). PROVE: (a) the number of fences is at most (a function of m,
     k and the denominator you make explicit), each fence a rational of
     bounded denominator; (b) at a fence where exactly one incidence
     ties, the orientation changes by the flip of exactly ONE edge of the
     cube (use lem:switch: the sign of the gain at sigma equals the sign at
     sigma[v]); (c) hence consecutive orientations on a drive line are at
     edge-flip distance one when fences are simple, and the edge-flip
     distance between s_B(t) and s_B(t') is at most the number of fences in
     between; (d) which single-edge flips preserve USO/acyclicity (the flip
     must keep a unique sink on every face: characterise the flippable
     edges of an AUSO -- this is where Holt-Klee-type laws enter for k = 0
     via prop:oneplayer-lp).
 (B) THE DOUBLING QUESTION. For s = B^2 and each z in {8,10,24,26}, COMPUTE
     the edge-flip distance between B^2 and B^2(. xor z) exactly, and the
     minimum number of fences a drive line from one to the other needs
     under (A)(d) (a shortest path in the flip graph of AUSOs of the
     5-cube restricted to the realisable ones -- state exactly which
     restriction you use). PROVE the resulting lower bound on the number
     of fences and translate it, via (A)(a), into a lower bound on the size
     (m, k, bits) of a driven block that presents both -- or prove that no
     bound follows and say why. The realisation-space route claimed (its
     rs:where(ii)) that the pin-drive branch needs at least two Min
     vertices: check what it proved and whether your bound is sharper.
 (C) THE ESCAPE SHAPE. Write down the level theorem for the shape
     rem:pinned-escape names (an outer vertex whose rest action reads the
     block as well as its partner): the analogue of prop:pinned-level with
     Theta_u, Theta_w replaced by monotone functionals of the block
     values, i.e. the sign conditions a game of that shape must satisfy at
     every inner strategy for its outmap to be B_phi(s, z). At m = 3, with
     the level-two block, that is a semialgebraic feasibility problem; for
     a fixed value configuration it is an exact linear programme. DECIDE
     it: feasible -> build the game by lem:dyadic-row and verify it from
     the game with ${REPO}/scripts/round16-verify/sparse_verify.py (USO,
     acyclic, outmap, height, run); infeasible -> the exact infeasibility
     certificates for the named shape with the reason the linearisation is
     exact for that support pattern. "We searched and found nothing" is
     not a result.
 (D) B^3. If the escape shape works from level two to level three, produce
     the 7-cube game (height 22, verified from the game). If it does not,
     the drive-line theorem of (A)-(B) and the level theorem of (C) are the
     deliverable, and you must say exactly which shapes are now excluded.
DELIVERABLE: theorems about drive lines (fences, single flips, the doubling
lower bound), the escape shape's level theorem, a decision at m = 3.
Labels prefixed dl:.` },
  { key: 'one-player-envelope', title: 'The upper envelope of monotone rational functions: is the one-player stopping-probability path superpolynomial, and can the tent itinerary drive an all-switches run', brief: `THE OBJECT: for a ONE-PLAYER stopping SSG the value w_rho = max_sigma
y^sigma_rho of the stopping-probability path (def:discount-path: every step
survives with probability rho) is the UPPER ENVELOPE of 2^m rational
functions of rho, each of degree <= n, each nondecreasing in rho, pairwise
crossing at most 2n times; the number of breakpoints B(G) is the
complexity of that envelope. The paper knows (read first): def:discount-path,
rem:discount-path, prop:discount-fold (BP(D), D Max and D Min, exactly
2^D - 1 breakpoints, the tent map's itinerary), rem:discount-fold (THE GAP,
stated exactly: "there are c > 0 and one-player stopping SSGs G_n on n
vertices with at least 2^{cn} breakpoints -- or its negation"; the fold
needs a Min vertex because every one-player value is a nonnegative
combination of the sink payoffs; the P_D transplant with a two-vertex seed),
prop:one-vertex-path (OS(R): one Max vertex, ANY dyadic breakpoint set R,
Omega(sqrt(N / log N)) reversals of one vertex, the difference of the two
options is 2^{K_0 - K} rho^K prod(rho - r_i)), cor:two-homotopies (the
path returns to pairs it left, so it is not the bias homotopy nor the
shadow-vertex path, which cannot), sec:bias (thm:lemke-homotopy,
prop:bias-shadow: on one player the bias path is the shadow-vertex path of
the occupancy polytope), prop:oneplayer-lp (X(G)), thm:ladder and
rem:ladder (Melekopoglou-Condon: Howard's rule with two actions is the
one-player half of the pivot), thm:fold, prop:leapfrog, rem:grid-per-vertex,
thm:opt-subcube, lem:switch. Round-17 code: ${R17}/r17-parametric-path/
(read-only); result ${REPO}/rounds/round17/results/03_*.json, audits 06_*,
10_*; the root's bp_verify.py, pd_discount.py in
${REPO}/scripts/round17-verify/.

WHAT TO PROVE:
 (A) THE ENVELOPE. State exactly the class of functions {y^sigma_rho}:
     rational of degree <= n, nondecreasing, y^sigma_rho = rho (I - rho
     Q_sigma)^{-1} b_sigma, pairwise crossing at most 2n times. PROVE from
     first principles the best upper bound on B(G) you can for one player
     in terms of n and m (the Davenport-Schinzel bound lambda_{2n}(2^m) is
     prior art, from memory, unchecked -- prove what you use; note that
     the 2^m functions are NOT arbitrary: they are the values of the
     vertices of ONE polytope X(G) under a parametric objective/constraint
     -- exploit that: is the path a parametric-LP path in rho, and which
     kind?).
 (B) THE LOWER BOUND, decided. Either a one-player family with 2^{Omega(n)}
     breakpoints, verified exactly at >= 5 sizes with the growth law
     PROVED, or a polynomial upper bound on B(G) for one player (proved;
     it must be superlinear by prop:one-vertex-path). What a Max vertex
     SEES is the difference of its two options, a difference of two
     nondecreasing rational functions of rho -- prop:one-vertex-path's
     mechanism makes any dyadic polynomial rho^K (Q_+ - Q_-) with Q_+/-
     nonnegative appear at one vertex. The obstacle to compounding is that
     the k-th vertex's difference depends on the (k-1)-th vertex's CHOICE
     (so it is piecewise), and every piece is monotone. PROVE whether
     chains of such vertices can multiply breakpoints (an exponential
     family) or whether monotonicity caps the total (a theorem: e.g. each
     Max vertex reverses at most poly(n) times because ...; note
     prop:one-vertex-path already gives Omega(sqrt(N/log N)) reversals at
     ONE vertex, so the cap cannot be O(1)).
 (C) THE TENT AS A DRIVER OF A RUN -- the only attack on the all-switches
     side of the pivot in this round. On BP(D) the optimal pair follows the
     tent map's itinerary as rho increases; along an all-switches run all
     values increase (lem:switch). Is there a stopping SSG in which an
     all-switches run VISITS the 2^D pairs of BP(D)'s path in order -- a
     game containing a "clock" vertex whose value rises along the run and
     plays the role of rho for a BP(D)-like block? Formulate exactly what
     the block must present to the clock and what the clock must present
     to the block (a driven block in the sense of def:pinned, driven by the
     clock; the tent alternation of the tied pair (F_d, G_d) is a Max and a
     Min vertex reading the same pair -- along a run Min best-responds
     instantly). PROVE either a construction (a superpolynomial all-switches
     family: check every step against prop:auso-size, thm:min-count,
     lem:switch, rem:blowup-realise's anti-value obstruction -- an inner
     vertex would need to see a DEcreasing function of another value,
     which no SSG value is) or the obstruction as a theorem ("no run
     follows the discount path because ..."), which is equally a result.
 (D) SUPPORT ONLY (not results): M1-M6 and all-switches measured on BP(D);
     the row 'BP(D): bias homotopy at most |C|, stopping-probability path
     2^{|C|/2} - 1' for rem:bias-families if you PROVE the first half.
DELIVERABLE: the envelope bound (A) proved; (B) decided or (C) decided.
Labels prefixed ue:.` },
  { key: 'eval-decision', title: 'The decision version of the evaluation-query model: how many strategy evaluations decide val(v0) >= 1/2 on a nondegenerate family with one skeleton, and what the rank-deficient relaxation is', brief: `THE OBJECT: the query complexity of the DECISION problem in the evaluation
model of thm:eval-queries. Read first: thm:eval-queries (the algorithm is
given the controlled skeleton -- C, owners, successor names, which names
coincide, which are sinks -- may query a Max strategy sigma to receive
val_sigma on C and on the successors of C, pays one per query, is not
charged for computation between queries; d(G) + 2 <= |C| + 2 queries NAME
an optimal strategy by the rank argument), rem:eval-queries (the relaxation
"produce a strategy optimal for SOME harmonic system consistent with the
data" is target-equivalent once the data has full rank), prop:hdp-eval
(HDP_m: m queries are needed to name the optimum; but its members are
pairwise isomorphic -- the decision bit is constant -- and degenerate),
rem:run-informs, rem:blowup-realise's last paragraph (outmap queries: 4 at
m = 3; 3 given the skeleton), cor:selection, thm:compare-equivalence,
thm:decide-one-bit, prop:no-halving, thm:top, thm:order-determines,
rem:order-unique, prop:bracket, def:improvement-uso, prop:allsw-auso,
lem:readout, lem:readout-reduce, thm:readout-realise, lem:survival-contract,
lem:dyadic-row. Round-17 code: ${R17}/r17-query-model/ (read-only), result
${REPO}/rounds/round17/results/14_*.json, audits 16_*, 20_*; the root's
hdp_verify.py, dout3.py in ${REPO}/scripts/round17-verify/.

THE HONEST QUESTION (the round-17 route's own next step 3): is the
evaluation-query complexity of DECIDING val(v0) >= 1/2 more than O(1) on a
NONDEGENERATE family with one skeleton whose members lie on both sides of
1/2?

WHAT TO PROVE:
 (A) THE ADVERSARY. A family of nondegenerate stopping SSGs (no tied
     incidence (sigma, i)) sharing one controlled skeleton, with val(v0)
     >= 1/2 on some members and < 1/2 on others, on which every
     deterministic evaluation algorithm needs Omega(|C|) queries (or
     Omega(log |C|), or any superconstant bound you can prove) to output
     the bit. The adversary answers each query with a val_sigma consistent
     with SOME member: by lem:readout the members are harmonic systems --
     substochastic rows over C -- and a dyadic system is a game by
     lem:dyadic-row, so the adversary may reason over systems provided
     every one it commits to is dyadic, stopping and nondegenerate. The
     difficulty: one query returns |C| + (number of successors) numbers,
     and the members must agree on the answers to the first queries while
     disagreeing on the bit; design a HIDDEN-ROW family in which the bit is
     determined by rows that the early queries do not read (each query
     reads the rows of the chosen actions only, through the fixed point),
     and PROVE the bound with the full accounting of what an answer reveals
     (rem:run-informs: an answer adds at most one dimension to the affine
     hull, but a decision needs only one bit -- so the rank argument does
     not give a lower bound; you need an adversary).
 (B) THE UPPER BOUND. Is the decision complexity O(1) on a natural class
     (one Max vertex? |C| <= 2? one-player?) and Theta(|C|) in general, or
     is it between? A theorem with matching bounds up to constants is the
     ideal; a proved separation between naming (Theta(|C|) by
     thm:eval-queries and prop:hdp-eval) and deciding is a new-relation
     result either way.
 (C) RANDOMISED: the zero-error randomised decision complexity on your
     family (prop:hdp-eval has m / log(m + 1) for naming).
 (D) THE RELAXATION. K(D) := the set of harmonic systems over the skeleton
     consistent with the data D (per row a polytope: the consistency
     equations q + p . val_sigma|_C = val_sigma(v^(a)) are linear in the
     row). At rank r < full, K(D) is not a point. PROVE the status of the
     problem "is the bit [val(v0) >= 1/2] constant on K(D)?" and of "output
     the bit if it is constant": polynomial (an algorithm, proved), or
     target-equivalent (a reduction from prob:main -- e.g. any game is a
     member of K(D) for D = empty, so the empty-data case is the target;
     the question is at rank r >= 1 whether the linear equations help),
     or a barrier (the bit is a nonlinear function of the rows, the set of
     systems with val(v0) >= 1/2 is semialgebraic -- what exactly is its
     structure inside a product of polytopes?). This is the new object of
     the route; make it precise and prove one theorem about it.
DELIVERABLE: the family and the lower bound as a theorem with the adversary
argument; the relaxation's status as a theorem. Labels prefixed ed:.` },
  { key: 'convex-class', title: 'The handicap-zero class: a first-principles polynomial algorithm on it, a two-player member outside the eight classes, and the convex cutting plane as a seventh mechanism', brief: `THE OBJECT: the class R := {stopping SSGs whose harmonic normal form over
C := Vmax u Vmin has B := (1/2)(R_0^T R_1 + R_1^T R_0) positive
semidefinite, R_a := I - P_a, P_a the first-passage rows of action a} --
equivalently, whose complementarity sum q(x) := sum_{v in C} (x(v) -
x(v^(0)))(x(v) - x(v^(1))) is CONVEX on the affine hull of Q(G), where it
is nonnegative with unique zero w* (rem:handicap-base: the Hessian is 2B,
base independence by principal-pivot invariance, the criterion ||(P_1 -
P_0)(I - (P_0 + P_1)/2)^{-1}||_2 <= 2; prop:handicap-zero-ceiling: R
attains the one-player ceiling at m <= 4 and handicap is not a property of
the orientation). Read also: thm:transport-objective (w* a vertex of Q(G);
the complementarity forms printed after it), prop:lcp (P-matrix), rem:lcp
(interior point on sufficient matrices: imported, closed, not ours),
sec:transport (Q(G), lem:transport-exact, thm:transport-sound,
thm:transport-barrier), sec:hybrid (thm:hybrid-complete,
thm:hybrid-convex-barrier: nested convex SETS as certificates),
thm:convex-barrier-both, rem:signdef / thm:signdef (the sign-definite
games: also convex-but-not-proved-polynomial), lem:round-recover (exact
recovery from precision 2^{-O(a)}), thm:contraction, thm:one-player (the LP
-- proved in the paper, so an LP solve is an allowed subroutine),
thm:few-avg ... thm:qp (the eight classes plus quasipolynomial treewidth)
and prop:fv-family / prop:modulator-family (the standard for separating a
class from the others: an explicit family, structural parameters checked on
the subgame REACHABLE from v0). Round-17 variational route:
${R17}/r17-variational/ (read-only), result
${REPO}/rounds/round17/results/17_*.json, audits 19_*, 22_*; the root's
vr_verify.py and CVX4_GAME.json, CVX6_GAME.json, NCX_GAME.json in
${REPO}/scripts/round17-verify/.

WHAT TO PROVE (any one of (A), (B), (C) proved is the route's result):
 (A) A FIRST-PRINCIPLES POLYNOMIAL ALGORITHM ON R. Minimise q over Q(G)
     exactly in time poly(N, a) WITHOUT importing ellipsoid, interior
     point or convex-QP results (they would be a fifth import). Available:
     q(x) - q(w*) >= (x - w*)^T B (x - w*) + grad q(w*) . (x - w*) -- check
     the sign of the first-order term on Q(G) --; lem:round-recover (an
     approximation within 2^{-2a-O(1)} recovers w* exactly, values having
     denominator <= 2^a); LP solves over Q(G) (thm:one-player's LP, or the
     transport LP) as unit steps. Candidates: (i) Frank-Wolfe with away
     steps -- linear convergence with rate governed by lambda_min(B) and
     the pyramidal width of Q(G): PROVE lower bounds 2^{-poly(N)} on both
     (lambda_min(B) > 0 is not given by B >= 0; on R with B singular the
     method may stall -- handle it) or exhibit their failure; (ii)
     projected/conditional gradient with exact rational line search; (iii)
     Lemke on the monotone LCP of the KKT system (sec:bias's machinery) --
     is Lemke polynomial on MONOTONE LCPs with this structure? Deliver a
     THEOREM "on R the problem is solved in poly(N, a) time by ..." with
     every step proved, or the exact gap in one sentence.
 (B) A TWO-PLAYER MEMBER OUTSIDE THE EIGHT CLASSES. A family in R with
     min(m, k) = Theta(N), both players present in proportion, verified on
     the reachable subgame to lie outside thm:few-avg, thm:few-escape,
     thm:kacyclic, thm:bounded-components, thm:escape-class,
     thm:few-denominator, thm:modulator, thm:qp (and the trivial min(m,k)
     = O(log N)). The round-17 members were |C| <= 3 or one-player. B >= 0
     is a semidefinite condition on the rows: design blocks whose
     composition PRESERVES it -- disjoint union (block-diagonal B: trivial,
     but the union must stay outside the classes), the stack of thm:stack,
     substitution of a gate (lem:gate) -- and PROVE the preservation. Also
     PROVE or REFUTE closure of R under def:damping (766/766 measured in
     round 17; the quadratic in the damping parameter is not sign-definite
     in general).
 (C) M7, THE CONVEX CUT. On R, for any x in Q(G): grad q(x) . (y - x) <=
     -q(x) is valid for y = w* (convexity and q(w*) = 0). PROVE it is a
     sound cutting plane, DEFINE the mechanism (the transport LP over Q(G)
     intersected with the accumulated cuts, deciding a controlled vertex by
     all three readings of the standing rule, Z-seeded, at most poly(N)
     cuts per round), and PROVE its relation to thm:hybrid-convex-barrier
     (whose certificates are nested convex SETS: does a chain of sets
     bound a mechanism that also uses a convex FUNCTION's tangent cuts?
     If not, the method does not cover M7 and you must find M7's own
     barrier or its own polynomial bound). Then compute B for the paper's
     stalls (H_m, CC, WD, CV, BC, R of prop:own-stall, G*, the 7-vertex
     both-readings stall) to see which are in R, and run M7 on those (exact
     arithmetic) as SUPPORT for a theorem about it, not as a result.
 (D) NOT results: the Hessian identity, convexity on R, base independence,
     the two membership facts -- the paper has them.
DELIVERABLE: a theorem from (A), (B) or (C) of novelty new-object or
new-relation; if (A) and (B) both succeed, R is the ninth polynomial class.
Labels prefixed hz:.` },
  { key: 'weakest-oracle', title: 'The hierarchy of partial-information oracles: which fragments of the value order are target-equivalent and which are polynomial', brief: `THE OBJECT: the hierarchy, under polynomial-time reduction, of ORACLE
FRAGMENTS of the value order of a stopping SSG. The paper proves
target-equivalence for: comparing two named vertices
(thm:compare-equivalence), two named AVERAGE vertices (prop:no-halving(b)),
naming the top average vertex (thm:top, one oracle call, by reference and
boost chains), deciding one named controlled vertex (cor:wrong-equivalence),
a sound non-stalling decision rule that picks its own vertex
(def:decision-rule, thm:decide-one-bit), a guide (rem:bsi), a bracket for a
named vertex (prop:bracket(d)), a polynomial-size superset of the alphabet
(rem:alphabet-equivalence), naming an optimal profile
(thm:transport-objective); and the full order on Vavg u {t0,t1} is a unique
O(a log a)-bit certificate (thm:order-determines, rem:order-unique). What is
NOT settled is the WEAKEST fragment that is still target-equivalent and the
STRONGEST that is polynomial. Read the above, plus thm:alphabet-iteration,
cor:grid-iteration, thm:few-denominator, thm:contraction (rate 1 - 2^{-a}),
thm:vi-lower, lem:round-recover, lem:denominator-sharp, thm:stopping-transform
(its cost, which every reduction must account for), def:simorder (Z_0, Z_1),
thm:kacyclic, prop:locality. Round-17 order-lattice route (dead-end, but its
next step 1 is this route's Q1): ${R17}/r17-order-lattice/ (read-only),
result ${REPO}/rounds/round17/results/02_*.json.

THE FRAGMENTS (prove theorems about at least Q1 and Q3, and one of Q2/Q4):
 (Q1) ANY-COMPARISON. Given a stopping SSG after the free Z_0, Z_1 sweeps
      (so every remaining non-sink value is in (0,1)), output SOME pair
      (x, y) of average vertices with w*(x) > w*(y), or "all equal". The
      algorithm CHOOSES the pair. Polynomial (an algorithm that always
      finds a provable strict comparison -- e.g. is there always an
      average vertex whose value is provably below another's by a local
      argument once Z_0, Z_1 are removed? prop:locality says no rule
      deciding a NAMED vertex reads a bounded radius; that does not cover
      a free choice), or target-equivalent (an adversary reduction: from
      a comparison instance (p, q) build a game in which EVERY strict
      comparison among average vertices reveals the answer -- thm:top's
      reference and boost chains are the tools, and its proof must be read
      carefully since there the oracle also chooses).
 (Q2) ANY-DECISION versus Q1: thm:decide-one-bit already makes the free-
      choice controlled-vertex rule target-equivalent; reduce Q2 to Q1 or
      separate them (a game where a strict average comparison is easy but
      no controlled vertex is decidable from it).
 (Q3) THE epsilon-ORDER. The order of the average values up to epsilon =
      2^{-c}: pairs with |w*(x) - w*(y)| < epsilon may be answered
      arbitrarily. For which c is it polynomial and for which target-
      equivalent? Value iteration with rounding gives it for c = O(log N)
      with a = O(log N) only; thm:contraction's rate 1 - 2^{-a} makes the
      generic bound exponential; lem:round-recover makes c >= 2a + O(1) the
      target. PROVE the dichotomy or the hierarchy exactly: e.g. "the
      epsilon-order is target-equivalent for every epsilon <= 2^{-ca} and
      polynomial for epsilon >= ..." with the threshold located, by a
      reduction that amplifies gaps (thm:top's boost chains double a gap
      per average vertex -- so an epsilon-oracle at epsilon = 2^{-c} plus
      c boost vertices decides exact comparisons? Check whether that makes
      EVERY epsilon = 2^{-O(1)} target-equivalent, which would be a clean
      new-relation theorem: "no approximation of the order helps").
 (Q4) THE ORDER ON A SET. The order among a named set S of average vertices:
      |S| = 2 is target-equivalent; is the order along a fixed simple PATH
      or CYCLE of the graph, or among the average successors of ONE
      controlled vertex (b of rem:order-unique(ii)), or among the vertices
      of one SCC, polynomial or target-equivalent?
WHAT COUNTS: theorems "fragment F is polynomial-time equivalent to
prob:main" (both reductions, from first principles, the stopping
transformation's cost accounted) or "F is polynomial" (an algorithm,
proved), for Q1, Q3 and one of Q2/Q4, plus the map of the hierarchy (which
fragments are equivalent to each other) as a theorem. A fragment proved
polynomial that no class of the paper implies is new-object; a fragment
proved target-equivalent by a genuinely new reduction is new-relation. Do
not restate thm:top / prop:no-halving / thm:decide-one-bit -- cite them.
Labels prefixed wo:.` },
  { key: 'beyond-holt-klee', title: 'The LP orientations of occupancy polytopes: a necessary condition for one-player realisability beyond Holt-Klee, and h*_1(5) in {10, 11}', brief: `THE OBJECT: the class OCC_m of orientations of the m-cube that are LP
orientations of an OCCUPANCY POLYTOPE: by prop:oneplayer-lp, for a
nondegenerate one-player stopping SSG with harmonic normal form (p^{v,a},
q^{v,a}) (first-passage laws of action a at v onto Vmax and onto t1),
X(G) := {y in R^{2m}_{>=0} : sum_a y_{w,a} - sum_{v,a} p^{v,a}_w y_{v,a} = 1
(w in Vmax)} is a simple m-polytope with the cube's graph, whose vertices
are y^sigma = (I - P_sigma^T)^{-1} 1 supported on sigma, and the objective
sum q^{v,a} y_{v,a} orients its graph as the improvement orientation s_G.
Every member is Holt-Klee (the import), whence h*_1 <= h*_LP <= h*_HK; the
ceilings (rem:four-ceilings, nondegenerate): h*_1 = 1,2,4,6,>=10,>=12,>=13;
h*_HK = 1,2,4,6,11,>=14,>=20 (prop:hkfive: h*_HK(5) = 11, exhaustive, with
the height-11 witness printed). At m = 3, OCC_3 = HK_3 (prop:m3-realised);
at m = 4 every HK class of height 6 is realised by a one-player game
(rem:hk-survey, measured; five HK classes of heights 3-5 unresolved). Read:
prop:oneplayer-lp and its proof, cor:seven-two-player, prop:hkfive,
rem:hk-survey, prop:hstar-one-five (h*_1(5) >= 10), cor:hstar-one,
prop:oneplayer-plus-one, prop:sink-lift, prop:hk-records,
prop:hk-doubling-measured, prop:tstar, thm:no-seven, sec:ties,
thm:readout-realise, lem:readout, def:reduced-rows, prop:rows-turn,
lem:crossing, thm:stack, cor:stack-family, prop:oneplayer-census-small,
rem:oneplayer-dictionary, sec:oneplayer-howard, rem:ladder (the one-player
pivot: Howard's rule with two actions per state, Melekopoglou-Condon), the
laws thm:peak-law, lem:monotone-law, lem:rise-bound, thm:switch-count,
cor:no-return, cor:law-u, prop:closed-now-or-never, thm:impedance. Prior art
from memory (flag unchecked): LP-realisable unique sink orientations are a
proper subclass of the Holt-Klee ones from dimension 4 on (Morris; Gaertner
et al.); Holt-Klee is necessary, not sufficient; Develin on LP orientations
of cubes. Tools: ${SCRATCH}/solo/my_D.py (Holt-Klee by max-flow),
${SCRATCH}/solo/census/, AP_m4_k0_*.json (one-player readout systems at
m = 4), ${SCRATCH}/root16/normform.py, auso.py; the round-16 routes
hk-doubling and one-player-howard under ${R17}/.

WHAT TO PROVE:
 (A) A NECESSARY CONDITION BEYOND HOLT-KLEE. X(G) is not an arbitrary
     simple polytope with the cube's graph: its facets are y_{v,a} >= 0,
     its vertex coordinates are expected visit counts >= 1, the rows are
     first-passage laws (substochastic, with q^{v,a} + sum_w p^{v,a}_w <=
     1), and the objective is the total value sum_v val_sigma(v). PROVE
     what that structure forces on s_G that Holt-Klee on the abstract cube
     does not: candidates are the paper's own run laws (thm:peak-law,
     lem:monotone-law, lem:rise-bound, thm:switch-count, cor:law-u,
     prop:closed-now-or-never) -- DECIDE for each whether it is implied by
     Holt-Klee/AUSO axioms on the abstract cube (then it is not a new law
     of OCC_m) or not (then it is, and you must EXHIBIT a Holt-Klee AUSO
     violating it: that is the first "law beyond Holt-Klee" for one player,
     a new-relation result). Other candidates: a sign condition on the
     values of 2-faces (lem:crossing), a shelling/ordering condition on
     the LP orientation of a polytope whose vertices are all >= 1 in every
     coordinate, the fact that the objective vector has entries in [0,1].
 (B) h*_1(5). Decide whether the height-11 Holt-Klee class of prop:hkfive is
     in OCC_5: realise it by a one-player game (an affine dyadic readout
     system, thm:readout-realise(b) with r = 1, built into a game by
     lem:dyadic-row and verified FROM THE GAME: nondegenerate, stopping,
     outmap, height 11) or PROVE it is not (by the law of (A), or by an
     exact infeasibility of the realisation conditions -- 32 x 5 sign
     conditions on the rows, polynomial after substituting val_sigma;
     for each support pattern the conditions are linear: state why your
     case split is exhaustive). Either way h*_1(5) in {10, 11} moves; a
     failed search is not a result, an exhaustive exact case split is.
 (C) THE ONE-PLAYER PIVOT. If (A) yields a law, PROVE whether it bounds
     h*_1(m) polynomially (that would settle Melekopoglou-Condon's question
     for Howard's rule with two actions, positively -- check every step
     against thm:ladder, prop:leapfrog, thm:stack, and the fact that
     h*_1(m) >= m + O(1) grows) or whether OCC_m still contains blow-up-
     like doublings (prop:hk-doubling-measured: the blow-up doubles and
     stays Holt-Klee at m = 4, 5 with a non-parity readout -- are those
     doublings in OCC_m? If they are, and the doubling iterates in OCC_m,
     that is the pivot's one-player half, a new-theorem of the first
     rank; if (T*) of prop:tstar stops them, PROVE why in terms of X(G)).
DELIVERABLE: the law in (A) as a theorem with a Holt-Klee orientation
outside it; (B) decided; (C) stated exactly with what is proved.
Labels prefixed oc:.` },
  { key: 'rlt-two', title: 'The level-two choice lift: an integrality gap engineered from the level-one obstruction, or an exactness theorem on a named class', brief: `THE OBJECT: the level-j Sherali-Adams (reformulation-linearisation) lift
R_j(G) over the CHOICE variables y_v in [0,1], x(v) = y_v x(v^(0)) + (1 -
y_v) x(v^(1)) at every controlled v (rem:choice-lift: level zero is Q(G);
level one is Balas' disjunctive closure of the faces F_v^i := {x in Q(G) :
x(v) = x(v^(i))}, a linear programme of size N^{O(j)} at level j; level one
FAILS on W_14 with a five-point certificate, max_{R_1} x(v_1) >= 3/5 > 1/2;
the round-17 route measured level two exact on everything it tried). Read
the round-17 convex-lift route's results and its audits' corrections
(${REPO}/rounds/round17/results/05_*.json, 09_*, 21_*; code
${R17}/r17-convex-lift/, read-only; the root's cl_verify.py and
DW_GAME.json in ${REPO}/scripts/round17-verify/): cl:barrier (level-one
exactness when fewer than three Max vertices REVERSE -- false at j = 0 as
stated, corrected by the audits; read the corrected form), cl:collapse's
directional bounds (first exact level >= min(m, max(1, rho_max)), the
audit's sharpening), cl:union (disjoint unions do not raise the level),
cl:rigid (= the pair test, a restatement). Read also thm:lasserre-vacuous
(the degree-two SOS lift of Q(G) is a different object and vacuous),
sec:transport (Q(G), thm:transport-sound), thm:hybrid-complete,
thm:modulator (N^{O(mu)} for the freezing-modulator number mu: is the first
exact level the modulator number in disguise? the route did not settle it),
lem:dyadic-row, def:wedge, def:cv, def:bc, prop:own-stall (R),
prop:simorder-stalls (G_8, G*), thm:ladder, def:ladder.

THE STATEMENT AT STAKE: there is a stopping SSG G and a vertex v with
max_{x in R_2(G)} x(v) > w*(v). Its negation ("level two is exact on every
stopping game") is TARGET-EQUIVALENT (an exact rational LP of size N^{O(1)})
and is not to be conjectured; so the route's task is the gap, or a proved
EXACTNESS THEOREM ON A NAMED CLASS (new-relation: e.g. "R_j is exact when at
most j controlled vertices reverse on every controlled cycle", or "R_k is
exact for k = the number of Min vertices" -- then the lift is thm:modulator
in disguise and you must PROVE the identity or the difference).

WHAT TO DO:
 (A) EXACT LEVELS, computed and proved. Write the level-two constraints
     explicitly (products of pairs of choice variables with every row of
     Q(G), McCormick bounds, consistency of pair marginals) and solve the
     level-two LP EXACTLY (fractions; ${SCRATCH}/root16/mylp.py, lp.py are
     exact two-phase simplex -- the LP has O(N^2 |C|^2) variables, so
     restrict to the reduced rows over C by lem:readout-reduce / the
     harmonic normal form, and say why that is exact) on: W_14, G_8, G*,
     R, H_m (m = 3,4,5), WD(2j,j,j+4) (j = 2,3,4), CV(e,s) (three sizes),
     BC(e,s) (three sizes), the ladder L_n, the 7-vertex both-readings
     stall. Report the first exact level of each, and PROVE the pattern
     you see (a theorem, with its hypothesis exactly stated).
 (B) ENGINEER THE LEVEL-TWO GAP. The level-one certificate on W_14 dies at
     level two because the pair pattern "v_1 chooses v_2, v_2 chooses the
     feedback" is infeasible in Q(G), closing a controlled cycle of gain <
     1 with two vertices on it (the route's diagnosis). So: at least three
     reversing Max and three reversing Min vertices (cl:barrier as
     corrected), every controlled cycle of length >= 3 (all pair patterns
     feasible), some TRIPLE pattern infeasible while all pair marginals
     are consistent. Set it up as an exact feasibility problem in the
     rows (alternating: rows <-> level-two moment vector, both halves
     linear) WITH the structural constraint built in, over dyadic reduced
     data; if a candidate appears, BUILD THE GAME by lem:dyadic-row and
     verify the gap by the exact level-two LP from the GAME, not from a
     normal form. Record exactly what was tried if nothing is found; that
     record is not a result, (A)'s theorem is.
 (C) If the gap is found: does R_j need j -> infinity (a family with the
     first exact level growing), and what is the relation to
     thm:modulator? If an exactness theorem is proved instead: is its class
     inside thm:modulator's, or new?
Labels prefixed rl:.` },
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
   the route's code, in ${SCRATCH}/r18-audit-${r.key}-correctness/. If a
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
   restatements, do your OWN search of ${SCRATCH}/round18/inventory.txt and
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
   round 17 five of seven routes reported restatements as results. Also flag anything that is
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
3. CONSISTENCY. Every \\Cref in the added text must point at a result that
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

log(`Round 18: ${ROUTES.length} object-changing routes on Opus 5: ${ROUTES.map(r => r.key).join(', ')}; correctness + novelty audits on Opus 5; one paper audit (round-17 diff) on Opus 5.`)

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\n\n# YOUR ROUTE: ${r.title}\n${r.brief}\n\n` +
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
