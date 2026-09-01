export const meta = {
  name: 'ssg-round14',
  description: 'Round 14 on the SSG value problem: 9 routes against the post-round-13 frontier (3 on Fable 5.1, 6 on Opus 5), each adversarially audited twice on Opus 5',
  phases: [
    { title: 'Routes' },
    { title: 'Audit' },
  ],
}

const REPO = '/data/ssg-proof'
const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/ef1cfad9-5d31-414e-ba8d-8fdf97a6d2ab/scratchpad'

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
    key: 'bsi-rounds',
    model: 'fable',
    title: 'The round count of bidirectional improvement',
    brief: `
YOUR ROUTE IS THE NEWEST MECHANISM IN THE PAPER, AND NO BARRIER IN IT COVERS
THE MECHANISM. Read def:bsi, thm:bsi-nostall, cor:bsi-correct,
prop:bsi-nonstopping, rem:bsi, lem:max-deficit, thm:seed-dichotomy,
cor:no-height, thm:switch-count, thm:normalform-barrier, thm:window-barrier
and thm:ladder in ${REPO}/frontier.tex before anything else.

THE STATE. BSI carries a PAIR (sigma,tau) and reads two exact vectors,
L = val_sigma and U = val^tau, both polynomial to compute. Max switches the
L-improving vertices that U does not veto, Min the U-improving vertices that L
does not veto, simultaneously. thm:bsi-nostall: on a stopping game the rule
can halt only at an optimal pair. cor:bsi-correct bounds the rounds only by
2N4^a. rem:bsi: without the vetoes it is all-switches on G beside all-switches
on G-bar (a polynomial bound for that is EQUIVALENT to one for all-switches),
and a guide U whose order at every Max vertex agrees with w*'s is
target-equivalent; what is open is the round count of the veto by val^tau,
which is NOT such a guide. Attribute: symmetric strategy improvement for parity
games is Schewe-Trivedi-Varghese (2015); say where BSI coincides with it and
where it does not.

A polynomial round bound for BSI on all stopping SSGs SOLVES THE PROBLEM
(cor:bsi-correct plus thm:stopping-transform). A superpolynomial family is a
new barrier covering a mechanism nothing in the paper covers. Both directions
are decisive; work on both, negative first, because a family tells you what a
proof would have to overcome.

DELIVERABLES, in order.
(1) Implement def:bsi exactly, BOTH variants (veto and strict), from the
    definition, in fractions; val_sigma and val^tau by brute force over the
    opponent's positional strategies or by thm:eval-stopfree (LP), never by
    greedy policy iteration. Validate thm:bsi-nostall on 300 random stopping
    games with |Vmax| >= 2 AND |Vmin| >= 2 (every halt at an optimal pair; the
    round count is the number of PRODUCTIVE rounds). ${SCRATCH}/root14/t_bsi.py
    is a prior check you may read but must not trust.
(2) MEASURE, as an exact table, from all four corner starts (sigma all-first /
    all-second, tau all-first / all-second) and from 20 random starts:
    the ladder L_n (n = 1..12) made two-player by the disjoint-union gadget of
    thm:compare-equivalence with its dual (lem:duality: swap sinks AND roles);
    H_m; CC(L,m); WD(e,j,m); S_r; prop:own-stall's R; G* (${SCRATCH}/root14/
    gstar.py); TW(2j,j,j+4) (code in the round-13 two-player-wedge directory,
    rebuild it from its definition there); G-sharp of prop:auso-seven (97
    vertices; rebuild from the harmonic normal form printed in the paper, or
    from the round-13 auso-pivot directory, and VERIFY its outmap first).
    Report rounds for BSI, strict BSI, and plain all-switches side by side.
(3) POSITIVE. Potentials on PAIRS. cor:no-height forbids polynomial height on
    the Max lattice alone; BSI's state is a pair, so it does not apply. For
    each candidate decide, by proof or exact counterexample, whether it is
    monotone under a BSI round and whether its per-round change is bounded
    away from zero by 1/poly(N) or by a grid argument: Phi_1 = sum_v (U(v) -
    L(v)); Phi_2 = |{v : L(v) = U(v)}|; Phi_3 = (M, |Z|) with M = max(U - L)
    and Z = argmax, lexicographic; Phi_4 = the number of controlled vertices
    whose choice agrees with the greedy choice for BOTH L and U. The proof of
    thm:bsi-nostall shows Z is not a trap: turn that into a QUANTITATIVE
    statement (some vertex leaves Z, or M drops by a grid step, within k
    rounds) or state exactly which inequality fails. thm:switch-count's grid
    argument gives 2N4^a; the question is whether the vetoes give N^{O(1)}.
(4) NEGATIVE. ENGINEER a superpolynomial family. The design constraint the
    vetoes impose: at the Max vertices that must move, U must order the
    successors WRONGLY (U(sigma-bar(v)) < U(sigma(v)) while L-improving), which
    means tau is wrong in a way that misleads Max, and symmetrically L must
    mislead Min; both tracks must be slow AND mutually misleading. Couple a
    ladder-like Max track with a dual ladder-like Min track through average
    vertices so that each track's error sustains the other's. Verify exactly
    at >= 4 sizes; report N, |Vmax|, |Vmin|, a, the round counts for BOTH
    variants, and the growth law; check stopping and count tied incidences.
    A superpolynomial family for BSI is a new BARRIER; a polynomial-looking
    family proves nothing.
(5) STRUCTURE. Which barriers apply to BSI, precisely: it reads U, which is not
    a function of the Max history alone, so it is not a switching rule in the
    sense of def:rule and not residue-blind; state what thm:normalform-barrier,
    thm:window-barrier and cor:no-height do and do not say about it, and
    whether lem:normalform's normalisation preserves BSI trajectories (it
    preserves all-switches trajectories; check the dual track too).
(6) VARIANTS, one paragraph each with data: alternating (a Max round then a Min
    round); single vetoed switch of largest gain; the veto tightened to
    U(sigma-bar(v)) > U(sigma(v)); and BSI restarted with tau := Min's best
    response to sigma after each round (which collapses one track; say what
    it becomes).
(7) If you believe you have a polynomial bound, audit yourself to destruction:
    check that no step assumes U orders Max's successors as w* does (rem:bsi
    proves that target-equivalent), and test the bound against the family of
    (4) and against every instance of (2).
`,
  },
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
    key: 'free-search-14',
    model: 'fable',
    title: 'Free search: a formulation nobody here has tried',
    brief: `
YOUR ROUTE IS UNCONSTRAINED except by the anti-list below. Thirteen rounds
have terminated, again and again, at target-equivalent statements. Find a
formulation this project has not tried and push it until it produces a
THEOREM or provably ends at a target-equivalent statement, and say which.

THE ANTI-LIST -- a route landing in one of these without a genuinely new
mechanism is a repeat:
 - strategy improvement rules and switch counts; all-switches laws; AUSO/USO
   combinatorics; random facet; bidirectional improvement (a sibling route);
 - value iteration and its rate; interval, box or difference-matrix propagation
   (M2, M2T, M6, thm:slack-barrier, thm:separable);
 - the transport polytope, Lasserre/SOS/Balas lifts (a sibling route), LCP
   handicaps (a sibling route), vertex enumeration of Q(G);
 - simulation preorders and local matching calculi (thm:matching-barrier);
 - parameterised classes in a, the escape exponent, feedback-vertex-like
   transversals, treewidth, the k-acyclic colour, matrix rank
   (Kannan-Theobald), or an escape certificate (thm:escape-class);
 - approximation schemes (Dai-Ge); progress measures and universal trees
   (cor:no-height; totally ordered lattices have height 2^{Omega(N)});
 - payoff, discount or player-strength homotopies tracking the optimal pair
   (thm:fold); the coin-bias homotopy (a sibling route); entropic/softmax
   regularisation; Newton-Dinkelbach; stochastic complementation;
 - submodularity (prop:no-submodular); communication complexity or query
   lower bounds; UEOPL reformulations.

STARTING POINTS NOT TRIED HERE, offered and not prescribed -- pick one, or
something better of your own:
 - THE COMPLEMENTARY-CONE STRUCTURE. w* is the unique solution of a P-matrix
   LCP whose sign pattern is the optimal profile. The 2^{|C|} complementary
   cones partition R^{|C|}; q lies in exactly one. Is there structure in HOW
   the cones of an SSG LCP are arranged (nestedness, a total order on a line
   through q, a lattice of sign patterns) that a walk can exploit with a
   provable step count? Prove a structural theorem about the arrangement of
   the SSG cones, then decide what it buys.
 - SELF-DUALITY AT THE THRESHOLD. The threshold 1/2 is the value of a fresh
   coin, and lem:duality makes a yes-instance of G a no-instance of G-bar. Is
   there a certificate system SYMMETRIC under duality (a single object that
   certifies val >= 1/2 or val <= 1/2 with the same syntax) that is poly-time
   searchable on one side? Prove something about the symmetric structure of
   the game G (+) G-bar of thm:compare-equivalence, whose value is exactly 1/2
   at the fresh root.
 - SORTING THE AVERAGE VERTICES WITH ABSTAINING COMPARATORS. By
   thm:order-determines the preorder of w* on Vavg determines everything. A
   sound comparator that may ABSTAIN is available from M1-M6. Characterise
   exactly the set of preorders consistent with the answers of a given sound
   abstaining comparator, and whether a poly number of such queries can shrink
   the consistent set to one -- or prove that the consistent set is
   exponential no matter which sound comparator is used (a new barrier).
 - THE SEMIALGEBRAIC SET {val(v0) = 1/2}. Fix the graph and let the average
   vertices carry biases; the yes-set is semialgebraic. Its degree, its
   number of connected components, and whether sign determination for it is
   easier than the general problem.
 - ALGEBRAIC COMPLEXITY. For a fixed pair the value is a ratio of two
   determinant-like counts (forest balance). What must an arithmetic circuit
   computing sign(w*(u) - w*(v)) look like, and is there a lower bound in a
   model that captures the paper's mechanisms (M1-M6 are all such circuits)?
 - THE DOUBLE-OBSTACLE VIEW and the numerical-analysis theory of Howard's
   algorithm for discrete Isaacs equations, including superlinear
   convergence results that are stated for the two-player case.

RULES. State your choice in one paragraph before doing anything; say which
anti-list item it is nearest to and why it is not that item; verify every
claim in exact rational arithmetic; and deliver theorems with proofs. A
negative result that covers one of M1-M6 or def:bsi is worth more than a
positive result about a class thm:kacyclic already contains.
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
    key: 'coin-bias',
    model: 'opus',
    title: 'The value as an algebraic function of the coin bias',
    brief: `
YOUR ROUTE IS A HOMOTOPY IN A PARAMETER NO ROUND HAS DEFORMED. Replace the
fair coin at every average vertex by bias p (probability p on the first-listed
successor, 1-p on the second) and write val_p. At p -> 0 and p -> 1 the game
degenerates to a deterministic reachability/safety game solvable in
polynomial time by attractor sweeps; val_{1/2} is the target. Read thm:fold
(the paper's continuation barrier: freezing one vertex at payoff theta gives
a response map with exactly 2^D pieces; it kills continuations that TRACK THE
OPTIMAL PAIR), (v8), prop:locality and thm:stopping-transform first.

(a) LEGITIMACY FIRST. A biased coin is not an SSG in the sense of def:ssg.
    Prove the reduction back: a bias-p edge with p of polynomial bit size is
    simulated by fair coins using def:damping / lem:gadget, with the exact
    size cost, and stoppingness is preserved. Without this the route is about
    a different problem.
(b) Prove that p -> val_p(v) is piecewise rational on (0,1) with pieces indexed
    by regions where an optimal strategy PAIR is constant, that it is
    continuous, and bound the degree and coefficient size of each piece (the
    denominator is det(I - P_p) for the profile's chain).
(c) THE PIECE COUNT IS THE WHOLE QUESTION. Either prove a polynomial bound on
    the number of breakpoints of p -> (optimal pair) along (0,1) -- which with
    (a) and a continuation algorithm would put the problem in P and must be
    audited to destruction -- or construct a family with superpolynomially
    many breakpoints. Compute exact breakpoints for small instances by exact
    symbolic solving in Q(p) (resultants, or sympy with rational
    coefficients; no floating point for a claim) and report a table for L_n,
    H_m, CC, WD, S_r, R and the P_D of thm:fold. Note thm:fold's family P_D
    has its 2^D pieces in a DIFFERENT parameter; decide whether the same
    family, or a variant, has 2^{Omega(D)} breakpoints in p.
(d) MULTI-PARAMETER. Different biases at different average vertices give a
    homotopy in [0,1]^a. Ask the shadow-vertex question: does a generic
    straight-line path from a solvable corner to the all-1/2 point cross only
    polynomially many pair-regions? Exact data on the families above; a bound
    or a family with exponentially many crossings.
(e) THE ALGEBRAIC-FUNCTION ANGLE: val_p satisfies P(val, p) = 0 for a
    polynomial P with integer coefficients. Bound deg P and its height,
    determine whether P is computable in polynomial time (it is a resultant
    over exponentially many profiles, so probably not -- say exactly which
    elimination step blows up), and whether the sign of val_{1/2} - 1/2 can be
    read from P without computing it.
`,
  },
  {
    key: 'precondition',
    model: 'opus',
    title: 'Preconditioning the survival operator by a change of measure',
    brief: `
YOUR ROUTE ASKS WHETHER THE ESCAPE CLASS CAN BE ENLARGED BY CHANGING THE
OPERATOR RATHER THAN NARROWING THE CLASS. Read def:survival, lem:survival,
thm:escape-class, prop:escape-family, rem:escape-class, thm:contraction,
thm:vi-lower, thm:slack-barrier and rem:wedge (the escape-rate computation on
the wedge) first.

THE STATE. The escape class is quantitative: a certificate (lambda, x) with
Sx <= lambda x for the SURVIVAL operator S (both players maximising) makes
two-sided value iteration close in O((a + log kappa)/log(1/lambda)) rounds.
On the wedge WD every certificate has log(1/lambda) = 2^{-Theta(N)}; on
thm:vi-lower's player-free G_m value iteration itself is exponential. The
question: is there a polynomial-time computable CHANGE OF MEASURE h under
which the transformed operator has a polynomial rate?

(a) FORMALISE. A Doob h-transform for a positive h on V replaces the chain of
    each profile by its h-transform and rescales x -> x/h. Prove exactly which
    transformations of this kind preserve the comparison predicate
    w*(p) >= w*(q) (or the threshold decision at v0) and which preserve
    stoppingness. Give a characterisation, not examples. Note that a
    profile-independent h is what an algorithm can compute; a profile-
    dependent h (e.g. h = val_{sigma,tau}) is available only for the CURRENT
    profile of an iteration -- treat both, and say what each is good for.
(b) THE DECISIVE QUESTION. Is there a polynomial-time computable h with
    lambda(S^h) <= 1 - 1/poly(N) for EVERY stopping SSG? A yes puts the
    problem in P via thm:escape-class (write the full proof, check bit sizes
    and the transformed game's legitimacy, audit to destruction). A no should
    be PROVED as an OBSTRUCTION: an invariant of the game unchanged by every
    admissible h that lower-bounds the transformed rate. Compute it exactly on
    WD(e,j,m) and on G_m. The natural conjecture: the rate is governed by the
    worst profile's absorption time, which h-transforms cannot change because
    they are conjugations; but S is NOT a single chain (it is a max over
    profiles), so prove or refute carefully.
(c) CANDIDATES, each with the exact transformed rate on H_m, S_r, G_m and
    WD(e,j,m) at small parameters (floats to explore; exact rational
    verification only for the claims you make; exact bisection for the least
    lambda is known here to blow up denominators -- use a structural argument
    for the paper): h = val_sigma for a current sigma; h = the harmonic
    function of the average part with controlled vertices absorbing; h = a
    Perron-type vector of S; h = expected hitting time of the sinks under the
    worst profile; h from one round of the slack calculus.
(d) AGGREGATION / MULTIGRID. Aggregating average vertices into classes gives a
    coarse game; a two-level scheme converges fast iff the coarse operator
    captures the slow modes. Is there a poly-time computable aggregation with a
    PROVED convergence bound on all stopping SSGs? Prove or refute with an
    explicit family; G_m (no players at all) is the natural test, and
    lem:watched / Meyer's stochastic complementation (prior art) is the exact
    coarse operator for a single chain -- say what breaks for a max over
    chains.
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
  {
    key: 'free-search-b',
    model: 'opus',
    title: 'Free search: counting, certificates, and reductions',
    brief: `
YOUR ROUTE IS UNCONSTRAINED except by the anti-list, which is the same as for
every route: strategy improvement and switching rules; AUSO/USO combinatorics;
random facet; bidirectional improvement; value iteration, interval, box or
difference-matrix propagation; the transport polytope, Lasserre/SOS/Balas
lifts, LCP handicaps, vertex enumeration; simulation preorders and matching
calculi; parameterised classes in a, the escape exponent, transversals,
treewidth, k-acyclicity, matrix rank, or escape certificates; approximation
schemes; progress measures and universal trees; payoff/discount/player-
strength/coin-bias homotopies; entropic regularisation; Newton-Dinkelbach;
stochastic complementation; submodularity; communication complexity; UEOPL.

STARTING POINTS, offered and not prescribed:
 - PROOF COMPLEXITY. On a yes-instance, what is the smallest cutting-planes,
   Nullstellensatz or Positivstellensatz refutation of "val(v0) < 1/2" over
   the natural encoding (Q(G) plus the quadratic complementarity equalities)?
   A certificate system that is BOTH polynomial-size and polynomial-time
   SEARCHABLE is the target; separating those two is itself provable and
   informative. Give degree or size bounds with proofs on L_n, H_m, WD.
 - COUNTING AND ALGEBRA. For a fixed pair the value is a ratio of two
   determinant-like counts (forest balance; verified here on 800 instances for
   absorbing chains). Is there a SIGNED SUM over strategy pairs that telescopes
   to something polynomial-time computable whose sign decides the threshold?
   Permanents versus determinants; Pfaffian orientations; the all-minors
   matrix-tree structure of the average part; exact linear algebra over the
   2-adics exploiting lem:denominator-sharp (all denominators are powers of
   two dividing 2^a).
 - THE NUMBER OF DISTINCT VALUES. thm:order-determines makes the preorder on
   Vavg the certificate. Parameterise by k = the number of DISTINCT values
   among the average vertices, or among all vertices. Is SSG-Value in
   N^{O(1)} f(k) time? (k = 1 is polynomial: a single class. Beware
   prop:no-halving: comparing two average vertices is target-equivalent, but
   the PROMISE of few classes may change that.) Prove or refute; a proof that
   even k = 2 is target-equivalent is a result.
 - RICHMAN / RANDOM-TURN CORRESPONDENCES: random-turn games have values equal
   to Richman costs of bidding games; the fair coin at EVERY vertex is a
   special SSG; what structure transfers to the mixed case?
 - A REDUCTION to or from a problem whose status is settled, in a direction
   nobody has tried, with a complete proof.

RULES. State your choice in one paragraph before doing anything; say which
anti-list item it is nearest to and why it is not that item; verify every
claim in exact rational arithmetic; deliver theorems with proofs. If your idea
dies, say precisely where and why, with the instance.
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

log(`Round 14: ${ROUTES.length} routes -- Fable: ${ROUTES.filter(r => r.model === 'fable').map(r => r.key).join(', ')}; Opus: ${ROUTES.filter(r => r.model === 'opus').map(r => r.key).join(', ')}; audits on Opus.`)

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
log(`Round 14 complete: ${good.length}/${ROUTES.length} routes returned.`)
return { round: 14, routes: good }
