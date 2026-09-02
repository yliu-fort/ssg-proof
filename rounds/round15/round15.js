export const meta = {
  name: 'ssg-round15',
  description: 'Round 15 on the SSG value problem: 7 routes against the post-round-14 frontier (1 on Fable 5.1, 6 on Opus 5), each adversarially audited twice on Opus 5, plus an 8-part adversarial audit of frontier.tex itself on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
    { title: 'Paper audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/3f223550-99d5-478f-855b-c1117c4a9d67/scratchpad'

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

${REPO}/frontier.tex is a 131-page, 321-result LaTeX development built over
fourteen prior multi-agent rounds. Every claim in it is proved and every
negative claim carries an explicit instance verified in exact rational
arithmetic. It contains NO polynomial-time algorithm and claims none. Read the
parts you need with grep/sed; do NOT read all 540 KB.
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
${SCRATCH}/root15/r14routes/bsi-rounds/) found Q_16, a reduced game with 8 Max
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
greatest BA height of an AUSO of the m-cube, exponential in general
(Schurr-Szabo, h*(m) >= 2^{floor(m/2)}, the document's only external input
besides thm:determinacy). prop:auso-census: h*(m) = 1,2,4,7 for m <= 4;
prop:hstar-five: h*(5) = 12 < f(5) = 13, so the laws are strictly weaker than
the axioms. prop:auso-size: at most 3^N (N+2)^{2N} N^m = 2^{O(N log N)}
orientations arise from stopping SSGs on <= N vertices, a 2^{-Omega(2^m)}
fraction once N = poly(m): NO CENSUS OR SAMPLING CAN DECIDE REALISABILITY,
ONLY A CONSTRUCTION. prop:auso-seven (round 13): the height-7 orientation
of the 4-cube IS realised by a nondegenerate two-player stopping SSG G# on 99
vertices (4 Max, 2 Min, 91 average; its harmonic normal form is printed in the
paper and reproduced in ${SCRATCH}/root15/seven.tex, t_seven.py). Also settled: no
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
Holt-Klee (3 disjoint monotone source-sink paths where 4 are needed), so its
two Min vertices are NECESSARY. Measured, unverified: h*_HK(4) = 6 < 7,
h*_HK(5) = 11 < 12; with cor:law-u the law ceiling is 1,2,4,7,12,21 at m <= 6
against f = 1,2,4,7,13,25 (f(6) = 25 is an exhaustive computation in
${REPO}/scripts/ceiling/f6.out). DEGENERATE one-player games are NOT bound by
Holt-Klee: thm:flat-resolution's resolution is a combinatorial completion,
not an LP orientation (rem:oneplayer-lp). WHAT IS MISSING: a family of stopping SSGs on N = m^{O(1)}
vertices whose all-switches run has SUPERPOLYNOMIAL length -- equivalently,
for nondegenerate games, an SSG-realisable AUSO of superpolynomial BA height.
Every family built here (WD, CC, TW, ...) has BA height 1: all-switches halts
in ONE round on all of them. One-way couplings of realisable AUSOs are at best
ADDITIVE (+1 per dimension: heights 7,8,9,10 at m = 4,5,6,7); an operation
that DOUBLES height at polynomial TOTAL size cost is what is open -- and
N' <= N^c per step is NOT enough (iterating gives N_0^{c^k}).

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
(v2) NOW PROVED as prop:oneplayer-lp. Unverified: h*_1(4) = 6, h*_HK(5) = 11.
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
   A ready harness is at ${SCRATCH}/root15/ : mycore.py (SSG core: class
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
   mobius.py (M6). Round-14 route code is under ${SCRATCH}/root15/r14routes/
   (allsw-lower/: allsw.py, mdp.py, gsharp.py, hk.py, blowsearch*.py,
   allswlower.tex; free-search-14/: build.py, t_lane.py, fastsw.py, fs14.tex;
   bsi-rounds/: bsi.py, osc.py, selfdual.py, realise.py, four_switch_rows.json,
   bsi_rounds.tex). Round-13 and round-14 route directories with their own
   code are beside it:
   ${SCRATCH}/../../dc099d6a-f89a-421b-bbe2-2a87a9e19322/scratchpad/
   (auso-pivot/, two-player-wedge/, ...) and
   ${SCRATCH}/../../26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad/
   (allsw-lower/, allsw-degeneracy/, lasserre-2/, lcp-handicap/). COPY what you need into ${SCRATCH}/<your-route>/ and
   work there. Do NOT write into another route's directory and do NOT modify
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
    key: 'allsw-family',
    model: 'fable',
    title: 'The superpolynomial all-switches family: the degenerate crack, lane re-use, and height doubling by two players',
    brief: `
YOUR ROUTE IS THE PROJECT'S PIVOT, unchanged for three rounds and unproduced
in fourteen: a family of STOPPING SSGs on N = m^{O(1)} vertices whose
ALL-SWITCHES run (Max switches every strictly improving vertex at once, Min
best-responds exactly) has SUPERPOLYNOMIAL length; by cor:ceiling-general that
is the same as an SSG-REALISABLE AUSO family of superpolynomial
bottom-antipodal height, degenerate games now included. Read
def:improvement-uso, prop:allsw-auso, lem:auso-laws, cor:f-auso,
prop:auso-size, prop:auso-seven, thm:flat-resolution, cor:ceiling-general,
cor:law-u, prop:oneplayer-lp, rem:oneplayer-lp, thm:impedance, thm:ladder,
prop:closed-now-or-never, thm:seed-dichotomy and rem:wedge first, and read
${SCRATCH}/root15/r14routes/allsw-lower/allswlower.tex and
${SCRATCH}/root15/r14routes/free-search-14/fs14.tex, the two previous
attempts, IN FULL. Do not repeat their searches; start where they stopped.

WHAT THE LAST ROUND ESTABLISHED, and what you must build on.
 (a) allswlower:lem-isolated (from cor:no-return): if some round switches only
     vertices of W then sigma|_W never again equals what it was at the start
     of that round; a vertex that switches alone is spent for ever. So a
     recursive family cannot RESET an inner gadget and re-run it from the
     same local configuration: the second run must be the first run
     TRANSLATED (s(v xor z)), which is exactly what the Schurr-Szabo blow-up
     does -- in every round of the inner's run some outer vertex switches too.
 (b) allswlower:cor-selfread: in a one-player game a vertex p reading a loop
     through itself switches exactly when the loop value passes its current
     value; the three timing requirements of a naive reset ("p waits while
     the inner idles", "the closed loop beats the signal", "the signal beats
     the idle port") are contradictory, y_0 < l < val(A) < y_0.
 (c) The abstract operation D of allswlower:prop-search(a) raises the
     dimension by two and gives BA heights 4, 9, 16, 25 at m = 3, 5, 7, 9:
     QUADRATIC, and its orientations violate Holt-Klee from m = 5, so by
     prop:oneplayer-lp they need TWO PLAYERS. No rule of the same shape (outer
     outmap a function of the layer and of h_A(v) mod 2, 3, 4) doubles.
     5.7 x 10^6 engineered one- and two-player templates never grew by more
     than +2 per level.
 (d) fs14:lane, Lane(k): Max vertices l_i -> (l_{i+1}, x_i), l_{k+1} = t1, x_i
     a coin of value 1 - i 2^{-b}; from the all-exit start all-switches lasts
     exactly k rounds switching l_k, ..., l_1 in that order, N = O(k log k).
     The route then ABANDONED lane re-use on a FALSE obstruction: it argued
     that "val_sigma is 1-Lipschitz in a frozen payoff" caps what a
     non-improving switch can gain after a trigger. That bounds the GAP, not
     the RISE: thm:impedance says the rise of a switch is
     (gap) x h(v->u)/(1 - h(b->u)), and the escape denominator can be
     2^{-Theta(N)}, so a delayed switch CAN gain far more than its trigger
     did. THIS IS THE REOPENING REASON. Also fs14:cycle ("a cycle is active
     now or dead for ever") covers only INTRINSIC cycles (options leading to
     the next cycle vertex through average vertices exiting only to sinks);
     Fearnley's timing cycles are NOT intrinsic, so "the published counters do
     not binarise" was never established.
 (e) Nondegenerate ONE-PLAYER improvement orientations are LP orientations of
     a combinatorial cube, hence Holt-Klee (prop:oneplayer-lp); h*_HK(4) = 6.
     DEGENERATE one-player games escape this: thm:flat-resolution's AUSO is a
     combinatorial completion, and the paper's longest one-player runs are
     degenerate. Nobody has yet tried to EXPLOIT degeneracy on purpose.

THREE LINES OF ATTACK, in the order you should try them.
 (1) TWO PLAYERS, HEIGHT DOUBLING AT ADDITIVE SIZE. The Schurr-Szabo blow-up
     and the operation D are abstract. prop:auso-seven shows a non-Holt-Klee
     height-7 orientation IS realised with two Min vertices. Realise the
     dimension-5, height-9 orientation D(D(1-cube)) (or the genuine
     Schurr-Szabo blow-up of the 3-cube) by a two-player stopping SSG. The
     tool is the harmonic-normal-form dictionary (item v4 / gsharp.py): a
     stopping SSG with controlled set C is, up to the average part, a family
     of 2|C| substochastic rows over C u {t1}; the orientation is a sign
     pattern of val_sigma differences; with Min present, val_sigma is a MIN
     over Min's rows, i.e. piecewise-linear-fractional in the rows. Set it up
     as: choose Min's role EXPLICITLY (Min vertices are the timers -- Min's
     best response changes as Max switches, and that is what makes the outer
     coordinates switch "in every round of the inner's run"), then solve for
     the rows by exact LP on each linear piece, or by a structured design in
     which every row has at most two nonzero entries. If you obtain a
     realisation of height 9 at m = 5, ITERATE: the question is whether the
     realisation can be made UNIFORM in the level, with |C| growing by O(1)
     and the average part by O(N) per level (N_k <= N_{k-1} + poly(k), NOT
     N_{k-1}^c). If the size cost is multiplicative, SAY SO and give the
     exact recurrence; that is still a theorem.
 (2) DEGENERATE ONE-PLAYER GAMES. Design ties on purpose: a flat edge is a
     coordinate whose two ends have the same value vector (lem:trichotomy),
     and thm:flat-resolution lets the resolution orient it EITHER way. Build a
     one-player family whose flat classes are large and whose all-switches
     run from a chosen start exceeds h*_HK(m) (the Holt-Klee ceiling is 6 at
     m = 4, 11 at m = 5): that alone would be a new theorem ("degenerate
     one-player runs exceed the nondegenerate ceiling"). Then ask whether the
     ties can be used as a TIMER: a vertex that is tied does not switch, a
     tie is broken by an exponentially small change elsewhere (the impedance
     denominator), and lem:trichotomy forbids nothing about WHEN.
 (3) LANE RE-USE WITH THE CORRECT RISE ACCOUNTING. Take Lane(k), add a
     trigger vertex whose switch changes the coin values x_i through a shared
     average part (so that the lane's coins are re-ordered, not reset -- a
     reset is forbidden by (a)), and compute the run exactly. The target is a
     family on N = O(k log k) or O(k^2) vertices with all-switches length
     omega(N): superlinear is ALREADY new for one player (the best published
     lower bound for Howard with two actions per state is linear), and
     superpolynomial is the pivot.

REQUIREMENTS.
 - Exact arithmetic. Use ${SCRATCH}/root15/r14routes/allsw-lower/allsw.py or
   write your own loop from the definition; validate on L_n (exactly n rounds
   from the all-zero start) and on thm:all-switches-refuted's 7-vertex game.
   For games with a Min player, val_sigma is a minimum over ALL positional tau
   or thm:eval-stopfree's LP -- NEVER greedy policy iteration.
 - Report, for at least FIVE sizes: N, |Vmax|, |Vmin|, a, stopping (trap test),
   the number of tied incidences along the run, the run length, and the
   starting strategy. State the growth law and PROVE it if you can (a lemma
   about the phases); a verified table without a proof is a measurement.
 - Every probability other than 1/2 must be realised by average chains
   (fair coins, out-degree two, def:ssg); report the exact size cost.
 - If a line fails, give the OBSTRUCTION AS A THEOREM with an explicit
   instance, in the style of allswlower:lem-isolated -- "no family of shape X
   exceeds height Y because Z" -- not as a search report.
 - Do NOT redo: the AUSO census, h*(5) = 12, f(6) = 25, random search, the
   5.7 x 10^6 templates. Do not spend effort on the positive direction beyond
   naming what property of realisable orientations your family violates.
 - DELIVER: a python build(n) returning kinds and successor lists, the exact
   table, the LaTeX definition and lemmas, labels prefixed allswfam:.
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
${SCRATCH}/root15/r14routes/allsw-lower/allswlower.tex (lem-lp, hk.py) first.

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
     (the round-14 measurements 6 and 11 are unverified: reproduce them with
     your own max-flow test on every face, the paper's test is described in
     cor:seven-two-player), and print a witness orientation for each m. Then
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
     one-player stopping SSG, for m <= 4 at least, with certificates.
 (3) THE SCHURR-SZABO BLOW-UP AND HOLT-KLEE. Write down the Schurr-Szabo
     blow-up exactly (dimension +2, height at least doubled) and the round-14
     operation D (allswlower:prop-search(a)). Determine whether EITHER
     preserves Holt-Klee; if neither does, prove a lemma saying WHY (which
     face fails the disjoint-paths count, as a function of the seed). If some
     variant preserves Holt-Klee, that is the first candidate for an
     LP-realisable exponential family and you should push it towards (2).
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
Holt-Klee). The census code is in ${SCRATCH}/root15/census/ and
${REPO}/scripts/ceiling/. Attribute everything you know from the literature
(Klee-Minty, Goldfarb, Amenta-Ziegler, Holt-Klee, Gaertner-Morris-Ruest,
Schurr-Szabo, Melekopoglou-Condon, Mukherjee-Kalyanakrishnan, Hansen-
Miltersen-Zwick). Labels prefixed hcube:.
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
${SCRATCH}/root15/r14routes/bsi-rounds/bsi_rounds.tex (lem-bias,
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
     instances (${SCRATCH}/root15/r14routes/bsi-rounds/osc.py) and Q_16.
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

TASKS.
 (1) THE BIG CUBE. Construct, from a stopping SSG, the P-matrix LCP (M, q)
     and its Stickney-Watson orientation s_C of the |C|-cube, in exact
     arithmetic; state the sign conventions so that a vertex of the cube is a
     profile (sigma, tau) and the outmap at (sigma, tau) is the set of
     controlled vertices at which the profile is not locally optimal for its
     owner under val_{sigma,tau}. Prove that this is a USO (cite
     Stickney-Watson, verify on 200 random stopping games including
     degenerate ones, and say what degeneracy does to it). Verify on G#: is
     s_C on the 6-cube Holt-Klee (it must be if GMR applies)? Is it acyclic?
     Print it.
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
     the wedge, prop:own-stall's R -- all in ${SCRATCH}/root15/myinst.py,
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
reason. Sources: ${SCRATCH}/root15/r14routes/allsw-lower/allswlower.tex,
${SCRATCH}/root15/r14routes/bsi-rounds/bsi_rounds.tex, the round-14
allsw-degeneracy and lasserre-2 directories under
${SCRATCH}/../../26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad/, and the
precondition directory under
${SCRATCH}/../../ef1cfad9-5d31-414e-ba8d-8fdf97a6d2ab/scratchpad/.

THE ITEMS.
 (1) allswlower:lem-isolated and allswlower:cor-selfread (the two re-running
     laws; check that lem-isolated is not already cor:no-return restated --
     if it is a two-line corollary, say so and draft it as a corollary), and
     allswlower:prop-search(a): the operation D and its heights 4, 9, 16, 25
     at m = 3, 5, 7, 9 -- recompute the outmaps, check USO, acyclicity, both
     laws, the BA heights, and the Holt-Klee violations at m = 5, 7 with your
     own max-flow test.
 (2) From allsw-degeneracy: deg:prop-g (law ceiling 1,2,4,7,12 with cor:law-u
     added), deg:prop-g6 (21 at m = 6 -- reproduce or bound what you can in
     the time), deg:prop-hk5 (h*_HK(5) = 11), deg:lem-super (h*(k+l) >=
     h*(k) + h*(l), so h*(6) >= 13 -- PROVE it: it should be a product
     construction), deg:prop-nondeg4 (a nondegenerate 253-vertex realisation
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
value: (2) deg:lem-super and (4) Q_16 first, then (1), (3), (5), (6).
`,
  },
]

const PAPER_SECTIONS = [
  { key: 'foundations', lines: '1-1046', what: 'front matter (abstract, introduction, "what is proved and what is not"), sec:operators (the Shapley operator, least fixed points, comparison), sec:stopping (absorption, contraction, determinacy, evaluation), sec:transform (the quantitative stopping transformation and the threshold gadget)' },
  { key: 'classes', lines: '1046-2593', what: 'sec:special: thm:few-avg, lem:descent, thm:few-escape, thm:kacyclic and its three special cases, thm:bounded-components, thm:escape-class, prop:escape-family, sec:alphabet (thm:alphabet-iteration, thm:alphabet-rigid, thm:alphabet-denominator, thm:few-denominator, prop:alphabet-four, prop:fv-family)' },
  { key: 'structure', lines: '2593-3089 and 5975-6695', what: 'sec:structure (thm:opt-subcube, thm:short-path, lem:max-deficit, thm:impedance and the exact gain of a switch), sec:selection (thm:compare-equivalence, thm:order-determines, thm:decide-one-bit, prop:no-halving, the certificate), sec:randomfacet (thm:rf-correct, thm:rf-bound, lem:fbound, thm:subexp)' },
  { key: 'allswitches', lines: '3089-4109', what: 'the all-switches laws (lem:monotone-law, prop:closed-now-or-never, thm:peak-law, cor:no-return, cor:law-b, cor:antichain, thm:component-bound, thm:bounded-components), the AUSO identification (def:improvement-uso, prop:allsw-auso, lem:auso-laws), the flat resolution (def:flat .. cor:law-u, rem:flat), cor:f-auso, prop:auso-size, prop:auso-seven and its printed normal form, prop:oneplayer-lp, cor:seven-two-player, prop:auso-census, prop:hstar-five' },
  { key: 'refutations', lines: '4109-5975', what: 'thm:ladder and rem:ladder, the deterministic residue (lem:normalform, thm:normalform-barrier, thm:window-barrier, prop:freeze-escapes), def:bsi through rem:bsi-br (thm:bsi-nostall, lem:bsi-pairloc, cor:bsi-levels, prop:bsi-br, prop:bsi-twice, prop:bsi-nonstopping), thm:cyclic-uso, thm:vi-lower, thm:hamming-refuted, prop:rules-fail, prop:needle, prop:locality, prop:serialiser, lem:readonce, prop:no-submodular, thm:switch-count' },
  { key: 'calculi', lines: '6695-8224', what: 'sec:gap (def:rule, def:missing, thm:gap-equivalence), sec:simorder (def:simorder, the greatest fixed point, prop:locality-beaten, G8), sec:slack (def:slack, thm:slack-sound, thm:slack-barrier, thm:slack-vi-upper, def:trans-slack, thm:trans-complete, prop:trans-Hm, thm:separable, cor:set-certificate), sec:ratio (def:ratio, thm:ratio-sound, thm:ratio-sandwich, cor:ratio-stall, prop:ratio-incomparable, def:mobius, prop:mobius, prop:ratio-closure, prop:cw)' },
  { key: 'hybrid', lines: '8224-10138', what: 'thm:matching-barrier, sec:seeded (def:seeded, thm:seeded-barrier, thm:seed-dichotomy), sec:transport (def:transport, lem:transport-dim, lem:transport-exact, thm:transport-objective, prop:own-stall, thm:transport-barrier, rem:own-successor, thm:lasserre-vacuous, rem:lcp), sec:fold (thm:fold), sec:hybrid (thm:hybrid-complete, cor:hybrid-sink, prop:hybrid-onectrl, prop:hybrid-rate, thm:hybrid-convex-barrier, thm:hybrid-lower), sec:wedge (def:wedge, prop:wedge, thm:wedge-proved, cor:wedge-count, rem:wedge)' },
  { key: 'summary', lines: '10138-end, together with 1-330', what: 'sec:summary and the front matter READ AGAINST THE BODY: every claim in the abstract, the introduction, "what is proved and what is not" and the summary must match the statement it cites, with the same hypotheses, the same numbers (page counts, vertex counts, round counts, the lists of six classes and six mechanisms and fifteen prior-art attributions) and the same strength (measured vs proved); list every mismatch' },
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
   (the harness is at ${SCRATCH}/root15/: mycore.py, myinst.py, wd.py, cc.py,
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
   The harness is at ${SCRATCH}/root15/. If a claimed family or instance does
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

log(`Round 15: ${ROUTES.length} routes -- Fable: ${ROUTES.filter(r => r.model === 'fable').map(r => r.key).join(', ')}; Opus: ${ROUTES.filter(r => r.model === 'opus').map(r => r.key).join(', ')}; audits on Opus; ${PAPER_SECTIONS.length} paper audits on Opus.`)

const routeWork = pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\n\n# YOUR ROUTE: ${r.title}\n${r.brief}\n\n` +
    `Work in ${SCRATCH}/${r.key}/ (create it). Copy the harness from ` +
    `${SCRATCH}/root15/ into your own directory before using it. You have a ` +
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
