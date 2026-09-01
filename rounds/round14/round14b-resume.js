export const meta = {
  name: 'ssg-round14-resume',
  description: 'Round 14 resumed: the four routes killed mid-run (allsw-lower on Fable 5.1; lasserre-2, lcp-handicap, allsw-degeneracy on Opus 5), each adversarially audited twice on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/26460c0d-4bf3-4582-a380-b9b50bf91953/scratchpad'

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

${REPO}/frontier.tex is a 114-page, 278-result LaTeX development built over
thirteen prior multi-agent rounds. Every claim in it is proved and every
negative claim carries an explicit instance verified in exact rational
arithmetic. It contains NO polynomial-time algorithm and claims none. Read the
parts you need with grep/sed; do NOT read all 466 KB.
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
the threshold gadget is needed); def:damping / lem:gadget (any dyadic
probability or small stopping probability is realised by a chain of average
vertices); lem:duality (the dual game G-bar, sinks and roles swapped, has
val = 1 - val OFF THE SINKS only).

POLYNOMIAL CLASSES. thm:few-avg (poly(N)2^a, arbitrary SSGs); thm:few-escape
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

def:bsi (NEW, round 13, THE NEWEST MECHANISM AND NO BARRIER COVERS IT):
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
COUNT IS OPEN and no superpolynomial family is known.

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
ONLY A CONSTRUCTION. prop:auso-seven (NEW, round 13): the height-7 orientation
of the 4-cube IS realised by a nondegenerate two-player stopping SSG on 97
vertices (its harmonic normal form is printed in the paper). Also settled: no
stopping SSG with |Vmax| = 5 has an all-switches run of length 13. The
paper's own LONGEST all-switches runs are DEGENERATE, where the AUSO reading
is unavailable. WHAT IS MISSING: a family of stopping SSGs on N = m^{O(1)}
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

# UNVERIFIED claims from rounds 10-13 (do NOT cite as established)

(v1) DEGREE-TWO LASSERRE / SOS OVER Q(G): whether it is exact on stopping SSGs
 is OPEN. A 36-vertex "counterexample" L3 was WITHDRAWN. Known: exact when
 |C| <= 2; Lyapunov diagonal stability of the LCP P-matrix implies exactness;
 rho((R^0+R^1)/2) < 1/2 implies exactness; Balas disjunctive rank <= |C|; ONE
 Balas round is not exact (54-vertex witness).
(v2) One-player improvement orientations are LP orientations, hence Holt-Klee
 (Gaertner-Morris-Ruest territory); h*_1(4) = 6.
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

# PRIOR ART THIS PROJECT HAS ALREADY REDISCOVERED (eight times)

Auger-Coucheney-Strozecki (almost-acyclic SSGs, FPT in the feedback vertex
number); Mangasarian (hidden-K LCP by one LP); Gaertner-Morris-Ruest
(realisable USOs are Holt-Klee); Stickney-Watson (LCP/USO correspondence);
Gimbert-Horn (the permutation space and its decoder); Dai-Ge (approximation
collapse); Meyer (stochastic complementation / censored chains = exact vertex
elimination); Kannan-Theobald (fixed-rank games, cells of a hyperplane
arrangement). Condon 1992 is the source of the problem and of the stopping
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

# ROUND 14: WHAT CAME BACK, AND WHAT DID NOT

Round 14 launched nine routes and was stopped early. FIVE returned. Their full
payloads are on disk at ${REPO}/rounds/round14/results/*.json -- read the one
your brief names, with python3 -c "import json;..." or jq. NOTHING BELOW HAS
BEEN VERIFIED BY THE ROOT AGENT. It is EVIDENCE, not established fact: you may
build on it only after re-deriving it yourself, and you must say which parts
you re-derived.

(r14-a) free-search-b, "THE VALUE ALPHABET" (results/free-search-b.json).
 Parameterises by Lambda(G) = the SET of values taken by val, k = |Lambda|,
 D = the least common denominator of the values. Claims, all marked proved:
  fvb:thm-alph  val is the LEAST fixed point of x -> ceil_Lambda(Tx) from the
    bottom, on ANY finite grid Lambda containing every value, arbitrary SSGs
    (one line from thm:lfp-general(b)); the DOWN-rounded version is FALSE
    (explicit 5-vertex witness).
  fvb:cor-grid  if D val is integral, at most DN+1 sweeps of x -> ceil_{1/D}(Tx)
    from the bottom compute val, all intermediates integers in [0,D].
  fvb:lem-cover  every interior value of a STOPPING game is the midpoint of two
    other letters of the alphabet (else its level set is a trap).
  fvb:thm-rigid / fvb:cor-chain  the alphabet is the value vector of a
    PLAYER-FREE game on k-2 average vertices, each with one successor strictly
    below it and one strictly above.
  fvb:thm-den   D <= 2^{k-2}, attained by L_n; equivalently k >= 2 + log_2 D.
  fvb:cor-fewvals  a SEVENTH candidate polynomial class {D <= poly(N)}, running
    in O(N^2 D^2); D <= 2^{min(a,k-2)}, so it never loses to thm:few-avg and
    strictly wins on H_m and G_m (a = Theta(m) but D = 2^{m+1}).
  fvb:prop-fv   FV(n): X_i in Vmax -> (L_i, L_{i+1}), Y_i in Vmin ->
    (M_i, M_{i+1}), L_i in Vavg -> (t0, Y_{i+1}), M_i in Vavg -> (t1, X_{i+1}),
    i in Z_n; stopping, N = 4n+2, a = 2n, both players, val = 1/3 on X,L and
    2/3 on Y,M, k = 4, D = 3; claimed outside the escape class.
  fvb:prop-extremes  the gambler's-ruin chain GR(n) has D = k-1, the least
    possible, with a = Theta(N).
  fvb:thm-k4  the value set of a stopping SSG with k <= 4 is one of {0,1},
    {0,1/2,1}, {0,1/4,1/2,1}, {0,1/3,2/3,1}, {0,1/2,3/4,1}.
 ITS OWN GAP, honestly stated: "a poly-time algorithm outputting a poly-size
 set of rationals containing every value" is TARGET-EQUIVALENT.

(r14-b) free-search-14, THE ONE-PLAYER HALF OF THE PIVOT
 (results/free-search-14.json). Claims:
  fs14:howard   a stopping SSG with Vmin empty IS a transient 2-ACTION
    reachability MDP, and all-switches IS Howard's rule on it. So the
    one-player half of the pivot is the published open problem "is Howard's
    policy iteration exponential on 2-ACTION MDPs?". The known exponential
    lower bounds (Friedmann LMCS 2011; Fearnley ICALP 2010; Christ-Yannakakis
    2023) ALL need Theta(n) ACTIONS PER STATE; for a constant number of actions
    per state the best known lower bound is LINEAR (Mukherjee-Kalyanakrishnan,
    ICAPS 2025). These are literature statements from the route's own
    knowledge; treat them as attributions, not as proofs.
  fs14:deadset  if no vertex of W is strictly switchable under val_sigma then
    val_{sigma[W]} <= val_sigma, and val_{sigma[W]} <= val_{sigma_t} along
    every strictly improving run from sigma.
  fs14:cycle    THE OBSTRUCTION, and the sharpest thing round 14 produced. For
    an intrinsic Max cycle C (its options leave through average vertices that
    exit only to sinks), if at round t no vertex of C is strictly switchable
    toward C then val_{sigma_t'} >= lambda_C on C for every t' >= t: AN
    INTRINSIC CYCLE IS BEING CLOSED NOW OR IS DEAD FOR EVER. Friedmann's and
    Fearnley's counters time their exponential jumps by postponing a switch
    into an already attractive cycle for 2i+1 rounds using a competing action
    of larger appeal; with only TWO actions per vertex there is no such state.
    This is a proved reason why the published counters do not binarise.
  fs14:lane     Lane(k): Max l_i -> (l_{i+1}, x_i), l_{k+1} = t1, x_i a coin of
    value 1 - i 2^{-b}, b = floor(log2 k) + 2; N = O(k log k); all-switches
    lasts exactly k rounds from the all-exit start, switching l_k, ..., l_1.
  fs14:mixed-objective  sum_{Vmax} x - sum_{Vmin} x over Q(G) is NOT minimised
    at w*.
 Its gap: a family in which Lane(k) is re-run omega(1) times.

(r14-c) bsi-rounds (results/bsi-rounds.json). NO polynomial bound was obtained.
  bsr:lem-pairloc  if M = max(val^tau - val_sigma) > 0 then the argmax set Z
    meets C_max u C_min, so every BSI round strictly decreases
    Phi_3 = (M, |Z|) lexicographically: rounds <= N x (number of distinct
    M-levels along the run), and THE NUMBER OF LEVELS IS NOT BOUNDED.
  bsr:prop-br   if tau is ANY Min best response to sigma and S_sigma is
    nonempty, then C_max(sigma,tau) is nonempty. Hence the ONE-SIDED rule
    R_BR(sigma) = {v in S_sigma : val^tau(q) >= val^tau(p)}, tau a best
    response to sigma, never stalls. Check it against Hoffman-Karp and against
    Schewe-Trivedi-Varghese before believing it is new.
  bsr:lem-bias  if v in Vmax has successors p in Vmax and q in Vavg with the
    SAME successor pair, then val^tau(p) >= val^tau(q) for every tau. So every
    ladder-shaped Max region is invisible to BSI, and D(L_n) takes
    floor(log2 n) + 1 rounds where all-switches takes n.
  bsr:prop-normal  lem:normalform and def:kblind preserve val_sigma AND
    val^tau, hence the entire BSI trajectory: thm:normalform-barrier and
    thm:window-barrier DO apply to BSI.
  bsr:prop-switches  Q_16, a reduced stopping game with 8 Max and 8 Min
    vertices on which BSI switches ONE VERTEX FOUR TIMES (degenerate, 1072 tied
    incidences). So no "each vertex switches at most once" argument exists.
  Phi_1 = sum_v (U-L)(v) strictly decreases every round; Phi_2 = |{v : L = U}|
  is nondecreasing but flat for up to 5 consecutive rounds; Phi_4 is not
  monotone (11-vertex counterexample).
 THE ROOT AGENT independently confirmed, in exact arithmetic: on a ONE-PLAYER
 stopping game BSI is trivial (U = val^tau = w*, so the veto admits only
 w*-greedy switches, and BSI halts within |Vmax| rounds -- ONE round on L_n).
 So WD, CC, H_m and L_n cannot test BSI at all, and the disjoint union of a
 game with its dual does not couple the two tracks (1-4 rounds up to N = 43).
 A BSI family must be genuinely two-player and couple the tracks through
 SHARED vertices. A hill-climb reached 12 rounds at N = 22, driven by a long
 Min chain.

(r14-d) precondition (results/precondition.json), audited sound = FALSE, with a
 surviving core:
  thm:prec-rate  for a rectangular family {M_pi} of nonnegative matrices with
    Sx = max_pi M_pi x, the least certifiable rate is Lambda = max_pi rho(M_pi),
    certified by policy iteration. THIS IS BLONDEL-NESTEROV (the rectangular /
    independent-row-uncertainty joint spectral radius identity) -- the
    project's NINTH rediscovery. Attribute it.
  cor:prec-characterisation  hence the escape class of thm:escape-class is
    EXACTLY {G : 1 - Lambda(G) >= 1/poly(N)}, an intrinsic spectral condition
    that NO gauge / Doob h-transform can change (thm:prec-invariance;
    lem:prec-monomial: a monotone linear change of variable with monotone
    inverse is a permutation times a positive diagonal).
  prop:prec-Gm(a)  Lambda(G_m) = 1/(2u) with 2u - 1 = u^m, so
    1 - Lambda(G_m) = 2^{-m}(1 + o(1)).  PART (b) IS REFUTED by its own audit:
    Lambda(WD(e,j,m)) is a function of max(e,j), not of e alone; 24 of 49
    triples fail.
  thm:prec-contract / thm:prec-contract-class  eliminating the average part
    (Meyer's stochastic complement) and row-normalising each action by
    1/(1 - alpha_{v,i}) gives a monotone operator with the same fixed point and
    a provably smaller rate Lambdahat <= Lambda: a SIXTH candidate polynomial
    class, strictly containing the escape class, with an explicit member Y_D
    outside all five classes of the paper. Its audit found the stated
    fixed-point precision p insufficient (the accumulated floor is
    2^{1-p} kappahat / (1 - lambdahat)); repairable.
  prop:prec-wedge  Lambdahat(WD(e,j,m)) = 1 - 2^{1-j} exactly.
 Its audit also identified thm:prec-target as prop:bracket(d) and
 prop:prec-onectrl as thm:decide-one-bit, and judged prop:prec-block a barrier
 covering none of M1-M6 or def:bsi.

(r14-e) coin-bias: DEAD END, closed twice over. Do not reopen it.

FOUR ROUTES WERE KILLED MID-RUN in round 14 and never reported: allsw-lower,
lasserre-2, lcp-handicap, allsw-degeneracy. Gzipped partial transcripts are in
${REPO}/rounds/round14/transcripts/. If your route key is one of those four,
you are starting from scratch; you may read your own predecessor's transcript
(zcat), and nothing in it is verified.

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
   A ready harness is at ${SCRATCH}/root14/ : mycore.py (SSG core: class
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
   mobius.py (M6). Round-13 route directories with their own code are beside
   it: ${SCRATCH}/../../dc099d6a-f89a-421b-bbe2-2a87a9e19322/scratchpad/
   (auso-pivot/, two-player-wedge/, symmetric-improvement/, nonlinear-perron/,
   ueopl-promise/, ...). COPY what you need into ${SCRATCH}/<your-route>/ and
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
    key: 'allsw-lower',
    model: 'fable',
    title: 'A superpolynomial family for the all-switches rule on stopping SSGs',
    brief: `
YOUR ROUTE IS THE NEGATIVE HALF OF THE PROJECT'S PIVOT, and it is the one
object thirteen rounds have never produced: a family of STOPPING SSGs on which
the ALL-SWITCHES rule (Max switches every strictly improving vertex at once,
Min best-responds exactly) runs for SUPERPOLYNOMIALLY many rounds. Read
prop:allsw-auso, lem:auso-laws, cor:f-auso, prop:auso-size, rem:auso-size,
prop:auso-seven, thm:seed-dichotomy, rem:wedge, thm:normalform-barrier,
thm:window-barrier, thm:ladder and prop:allswitch-overshoot first.

WHY IT MATTERS. (i) thm:seed-dichotomy: a superpolynomial all-switches family
is exactly what defeats the seeded calculus M3, so it closes sec:wedge's open
item -- a family defeating EVERY mechanism in the paper. (ii)
thm:normalform-barrier and thm:window-barrier TRANSFER the bound verbatim to
every residue-blind and every polynomial-window rule. (iii) cor:f-auso and
prop:auso-size: for nondegenerate games it settles that SSG-realisable AUSOs
have superpolynomial BA height. (iv) It redirects the whole search: every
mechanism that reduces to all-switches is then dead, and only mechanisms that
are provably NOT switching rules (def:bsi is the current example) remain.

WHAT YOU KNOW THAT THIS PROJECT DOES NOT. The literature contains exponential
lower bounds for exactly this rule on RELATED models: Friedmann (LICS 2009,
LMCS 2011) for the locally-optimising, all-switches strategy improvement on
PARITY GAMES, by a binary counter built from cycle gates and a deceleration
lane; Fearnley (ICALP 2010) for Howard's policy iteration on total-reward
MDPs, a probabilistic adaptation of the same counter; and the standard chain
of reductions parity -> mean-payoff -> discounted -> simple stochastic games
(Zwick-Paterson), under which Friedmann's thesis states the lower bounds
transfer. The project's rule forbids the web, but YOUR OWN KNOWLEDGE IS
ALLOWED. If you can reconstruct such a construction, ADAPT it to Condon's
fair-coin model -- def:damping and lem:gadget realise any dyadic probability
and any small stopping probability by a chain of average vertices at
polynomial cost, and thm:stopping-transform is the model -- VERIFY it exactly,
and ATTRIBUTE it. That is the deliverable; a rediscovery honestly labelled is
exactly what is wanted. If you cannot reconstruct it, DESIGN your own on the
same principle: a counter whose low bits are set by all-switches while higher
bits are prevented from switching by a signal that lags behind, and whose
carry resets the low bits.

REQUIREMENTS.
(1) Exact arithmetic. Write your own all-switches loop from the definition
    (S_sigma = strictly switchable vertices under val_sigma; val_sigma by the
    componentwise min over all positional tau, or thm:eval-stopfree's LP for
    larger games -- ${SCRATCH}/root14/mylp.py is an exact simplex). Validate
    your loop on thm:ladder's L_n (all-switches takes exactly n rounds from
    the all-zero start) and on thm:all-switches-refuted's 7-vertex game.
(2) Report the run length for at least FIVE sizes with N, |Vmax|, |Vmin|, a,
    whether the game is stopping, and the number of tied incidences (sigma,i)
    along the run (zero means the AUSO reading applies). The target is a run
    length that doubles per added bit at linear cost in N. State the growth
    law and PROVE it if you can (a lemma about the counter's phases). A
    verified table without a proof is still valuable; label it a measurement.
(3) Give the starting strategy explicitly. A lower bound needs only one bad
    start.
(4) A ONE-PLAYER family (Vmin empty) settles (v3)'s question for Howard's rule
    on 2-action transient MDPs and is valuable on its own; do it first if it
    is easier. The TWO-PLAYER case is what closes sec:wedge's open item. If
    your family is two-player, ALSO run M1 (def:simorder, a greatest fixed
    point; code in ${SCRATCH}/root14/ and the round-13 two-player-wedge
    directory) on it and report whether the value-simulation preorder decides
    any controlled vertex at round zero.
(5) If the construction needs probabilities other than 1/2, realise them with
    average chains and report the exact size cost; the family must be SSGs in
    the sense of def:ssg (fair coins, out-degree two).
(6) Do NOT redo: h*(5) = 12, f(5) = 13; random or raw-game search (never found
    anything here); the AUSO census. Do not spend effort on the positive
    direction (a polynomial bound) beyond saying what property of realisable
    orientations your family violates.
(7) DELIVER the family self-contained: a python function build(n) returning
    kinds and successor lists, the exact table, and the LaTeX definition.
`,
  },
  {
    key: 'lasserre-2',
    model: 'opus',
    title: 'Is the degree-two Lasserre relaxation over Q(G) exact?',
    brief: `
YOUR ROUTE SETTLES (v1), a concrete decisive question left open in rounds
10-12: is the degree-two sum-of-squares / Lasserre relaxation exact on every
stopping SSG? If yes for a fixed degree, SSG-Value is in P (an SDP of
polynomial size, plus exact rounding via lem:denominator-sharp) -- so expect
NO, and make the refutation exact. If no, ask whether the required degree
grows with |C| (a rank lower bound, which is a new barrier).

THE FORMULATION. Read def:transport, lem:transport-dim, thm:transport-sound,
thm:transport-objective, prop:own-stall and sec:hybrid first. Q(G) is the LP
relaxation: controlled rows x(v) >= x(v^i) (Max), x(v) <= x(v^i) (Min),
average equalities, box, sinks pinned. The exact set is
  Q(G) n {x : (x(v) - x(v^0)) (x(v) - x(v^1)) = 0 for every v in C},
which for a stopping game is the single point {w*} (thm:contraction). The
Lasserre hierarchy relaxes the quadratic equalities by moment matrices. USE
lem:transport-dim: Q(G) is affinely isomorphic to a polytope in R^{|C|}, so
after eliminating the average coordinates the degree-2 relaxation has one
(|C|+1) x (|C|+1) moment matrix plus localising matrices for the 2|C| linear
rows and the box, and one linear constraint per quadratic equality. Write
this down precisely; state the alternative formulation on the strategy cube
(binary s_v with x(v) = s_v x(v^0) + (1-s_v) x(v^1)) and say why you do or do
not use it.

WHAT "EXACT" MEANS: the projection of the degree-2 feasible set onto x is
{w*}; equivalently, for every linear objective the SDP optimum equals its
value at w*. Non-exactness is witnessed by ONE feasible moment matrix whose
x-part differs from w*.

TASKS.
(1) Implement the relaxation. To FIND candidates use any floating SDP solver
    available (check for cvxpy/scs/cvxopt; else write a simple one -- a
    projected/dual method at |C| <= 5 is small); to CLAIM anything produce a
    RATIONAL moment matrix, verify PSD by exact LDL^T (fractions) and check
    every linear constraint exactly. Rationalise a float solution by rounding
    to a common denominator and re-verifying; if PSD fails after rounding,
    move the point slightly into the interior along a known feasible direction
    (e.g. towards the rank-one matrix of w*, which IS feasible).
(2) Reproduce the known facts before going further: exactness at |C| <= 2 on
    ten instances; a non-exact ONE-round Balas witness if you can rebuild it.
(3) HUNT with ENGINEERED instances, |C| = 3, 4, 5: prop:own-stall's R (|C| =
    5; every controlled vertex survives the own-successor test at the free
    seed); TW(2j,j,j+4) at j = 2 (|C| = 4); CC(L,m) and WD(e,j,m) (|C| = 2:
    exact by (v1), use them only as controls); the two-player G-sharp of
    prop:auso-seven (|C| = 6); games built to have a LARGE Q(G) in the
    directions the quadratic equalities cut (ask: for which x in Q(G) can a
    PSD moment matrix be completed? the obstruction is that the equalities
    force x(v) in {x(v^0), x(v^1)} on the support, so look for x whose
    controlled coordinates sit at the WRONG successor consistently -- the
    value vector of a wrong PROFILE evaluated as a Markov chain is a natural
    candidate; check whether it lies in Q(G) and whether it lifts).
(4) If you find a non-exact instance: minimise it, verify it independently
    from scratch, then test degree 3 on it, and try to build a family whose
    required degree grows (state what you can prove about the growth).
(5) If after honest engineering everything is exact: prove exactness on the
    largest class you can (Lyapunov diagonal stability of the LCP matrix is
    known sufficient; find the exact boundary), and state the open question
    sharply. Do not report "exact on K random games" as evidence.
`,
  },
  {
    key: 'lcp-handicap',
    model: 'opus',
    title: 'The handicap of the SSG linear complementarity problem',
    brief: `
YOUR ROUTE ASKS AN ALGEBRAIC QUESTION NO ROUND HAS ASKED. Interior-point
methods solve LCP(M,q) in O((1 + kappa) sqrt(n) L) iterations when M is a
P_*(kappa) matrix (a SUFFICIENT matrix of handicap kappa). If the LCP matrix
of a stopping SSG is P_*(kappa) with kappa = poly(N) and polynomial bit size,
SSG-Value is in P. If kappa is exponential or infinite (M not sufficient),
that is a proved barrier of an algebraic kind, covering every interior-point
method at once. Decisive either way; do both directions.

(a) Derive the LCP (M,q) of a stopping SSG YOURSELF from the fixed-point
    system x = Tx -- do not take any formulation on faith -- and prove M is a
    P-matrix, self-contained (this is Stickney-Watson / Gaertner-Ruest
    territory; attribute). Two natural formulations exist (variables on the
    controlled coordinates after lem:transport-dim, with Min's rows
    sign-flipped; or one variable per controlled vertex per action); state
    both and say which you use and why. Give bit sizes in terms of N and the
    damping constants of thm:stopping-transform.
(b) COMPUTE THE HANDICAP. M is P_*(kappa) iff for all x,
      (1 + 4 kappa) sum_{i in I_+} x_i (Mx)_i + sum_{i in I_-} x_i (Mx)_i >= 0,
    I_+ = {i : x_i (Mx)_i > 0}, I_- the rest; M is SUFFICIENT iff some finite
    kappa works, and the handicap is the least such kappa. For |C| <= 4 this
    is a finite family of small quadratic problems (one per sign pattern);
    solve them EXACTLY where possible (each is a copositivity-type question on
    a 2^{|C|}-indexed family; for |C| <= 3 do it by exact case analysis, for
    larger sizes give certified bounds). Report kappa, or non-sufficiency with
    an explicit witness x, for: L_n (n = 2..6); H_m (m = 3..6); S_r (r =
    1..4); CC(L,m) small; WD(e,j,m) small; prop:own-stall's R; TW at j = 2;
    G-sharp of prop:auso-seven if feasible. Then FIT and PROVE the growth on
    at least one family.
(c) If kappa is polynomial on everything you test, write the complete
    algorithm and proof including the exact rounding step (lem:denominator-
    sharp gives the denominator bound; prove the required epsilon is
    2^{-poly}) and audit it to destruction. If kappa is exponential or M is
    not sufficient on an explicit family, PROVE the lower bound.
(d) Independently decisive structural questions on the same matrix, each with
    proof or explicit counterexample: row sufficient? column sufficient?
    hidden-K / hidden-Z (Mangasarian: then one LP solves it -- known for the
    M-factorable case, (v6))? a K-matrix or M-matrix after positive diagonal
    scaling? Lyapunov diagonally stable (positive diagonal D with DM + M^T D
    positive definite)? Each is a concrete algebraic property of an explicit
    matrix; settle as many as you can exactly, and relate them to (v1)'s
    sufficient condition for Lasserre exactness.
`,
  },
  {
    key: 'allsw-degeneracy',
    model: 'opus',
    title: 'Degenerate all-switches runs, and whether degeneracy can be removed',
    brief: `
YOUR ROUTE CLOSES A HOLE IN THE PIVOT. prop:allsw-auso reads all-switches as
the bottom-antipodal walk of an AUSO only for NONDEGENERATE stopping games (no
tied incidence (sigma,i)). The longest all-switches runs recorded in the paper
(prop:overshoot-small, prop:allswitch-overshoot) are DEGENERATE: there a cube
edge can be unoriented, the outmap is not a USO, and cor:f-auso's ceiling
h*(m) does not obviously apply. f(5) = 13 > h*(5) = 12 shows the LAWS allow
more than the AUSO axioms; whether GAMES do is open. Read def:improvement-uso,
prop:allsw-auso, lem:auso-laws, cor:f-auso, rem:f-auso, prop:auso-census,
prop:hstar-five, thm:peak-law, cor:law-b, cor:antichain, thm:component-bound,
lem:switch, lem:trapchar and thm:switch-count first.

(a) THE PARTIAL-ORIENTATION ABSTRACTION. Define the improvement outmap of a
    degenerate stopping game as a PARTIAL orientation of the cube (an edge is
    oriented iff exactly one endpoint is strictly switchable in that
    coordinate; unoriented if neither is -- prove that "both" is impossible,
    or exhibit it). Prove the analogue of lem:auso-laws for partial
    orientations: which of cor:no-return and cor:law-b survive, and does every
    face still have a unique sink in a suitable sense (lem:local-global says
    the optimal set is a subcube -- the sink is a subcube, not a vertex).
    Define h*_partial(m) and compute it exactly for m <= 4 by enumeration in
    C (the round-12 census code is at ${SCRATCH}/root14/census/); compare with
    h*(m) = 1,2,4,7 and f(m) = 1,2,4,7,13.
(b) DEGENERACY REMOVAL. Is there a polynomial-time perturbation of a stopping
    SSG that makes it nondegenerate, preserves or lengthens the all-switches
    run from a given start, and keeps N polynomial? Candidates: perturb the
    sink payoffs (lem:gen-comparison allows arbitrary alpha < beta; then
    realise the payoffs by gadgets); a symbolic epsilon in transition
    probabilities via def:damping chains of different lengths at different
    vertices; lexicographic tie-breaking encoded by tiny leaks to t1. PROVE it
    or give the obstruction with an explicit instance where every perturbation
    shortens the run. If it works, every all-switches lower-bound question
    reduces to the nondegenerate case and cor:f-auso's ceiling is universal;
    if it fails, the degenerate case needs its own combinatorics and (a) is
    the right object.
(c) NEW LAWS. cor:f-auso says any improvement on f must use a property
    improvement orientations have and general AUSOs lack. Derive such laws for
    ALL stopping games including degenerate ones, from lem:switch's vector
    monotonicity (val_sigma increases in the product order along the run),
    thm:peak-law, lem:trapchar, thm:component-bound, and the grid of
    lem:denominator-sharp. State each as a condition on the sequence
    (sigma_t, S_t) and PROVE it. Recompute the law bound at m = 3,4,5 with the
    new laws (adapt ${SCRATCH}/root14/census/ or the C code laws.c in
    ${REPO}/scripts/ceiling/) and report whether it drops below f. Test every
    candidate law against the paper's degenerate runs BEFORE proving it.
(d) f(6) and h*(6): give the best bounds your search can CERTIFY, with an
    honest description of what was exhausted. A long-running exhaustive job
    ./f2 6 has been computing f(6) since 2026-08-28 in ${REPO}/scripts/ceiling
    (see f6.out: best so far 25); do NOT start another such job; read its
    output and state what it does and does not establish.
`,
  },
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

1. For EVERY result marked "proved", reconstruct the argument. Find the step
   that is asserted rather than proved. State it as a one-sentence GAP.
2. For EVERY numerical or computational claim, REBUILD THE COMPUTATION YOURSELF
   in exact rational arithmetic, from the STATEMENT and not from the route's
   code, in your own directory under ${SCRATCH}/audit-${r.key}-correctness/.
   The harness is at ${SCRATCH}/root14/. If a claimed family or instance does
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
   inside thm:few-avg, thm:few-escape, thm:kacyclic, thm:bounded-components
   or thm:escape-class.
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
   presented without acknowledgement -- eight such cases have already been
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
     thm:few-escape, thm:kacyclic, thm:bounded-components or thm:escape-class?
     Demand an explicit member outside all five, verified on the subgame
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

log(`Round 14 (resumed): ${ROUTES.length} routes -- Fable: ${ROUTES.filter(r => r.model === 'fable').map(r => r.key).join(', ')}; Opus: ${ROUTES.filter(r => r.model === 'opus').map(r => r.key).join(', ')}; audits on Opus.`)

const results = await pipeline(
  ROUTES,
  (r) => agent(
    `${COMMON}\n\n# YOUR ROUTE: ${r.title}\n${r.brief}\n\n` +
    `Work in ${SCRATCH}/${r.key}/ (create it). Copy the harness from ` +
    `${SCRATCH}/root14/ into your own directory before using it. You have a ` +
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

const good = results.filter(Boolean)
log(`Round 14 (resumed) complete: ${good.length}/${ROUTES.length} routes returned.`)
return { round: 14, routes: good }
