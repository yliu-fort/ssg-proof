---
name: ssg-search-state
description: "State of the multi-agent search on the SSG value problem in /data/ssg-proof (Condon's open problem); rounds, verified results, resume plan, honest-reporting stance."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6076bc78-583e-4c17-a24f-088177095475
  modified: 2026-08-26T20:37:55.370Z
---

The task in /data/ssg-proof/conjecture.md asks for a proof that deciding val(v0) >= 1/2 for simple stochastic games is in P — this is Condon's (1992) open problem. The brief demands returning ONLY a complete proof and forbids reporting the problem as open; my standing stance: run genuine diverse multi-agent exploration with adversarial audit, NEVER fabricate a proof, and deliver the brief's own fallback clause — strongest rigorously proved derivations + exact gaps — as a compilable LaTeX file named frontier.tex (NOT proof.tex).

## Rounds
- Round 1a (session 1f9100d4, runId wf_b61bf4f1-a3f): 14 routes, 157 lemmas (117 proved / 21 disproved / 19 gap). All routes ended blocked_theorem_strength_gap or dead_end. Extracted to scratchpad/prior_round1.md (494 KB).
- Round 1b (session 6076bc78, runId wf_c4260d84-6b2): 12 fresh independent families. First launch died with only strategy-improvement returning; resumed via resumeFromRunId.

## Results I verified MYSELF with exact rational arithmetic (not just agent claims)
- R10 REFUTED "all-switches dominance": 7-vertex game (x,y Max; m Min; a,h Avg; x->{t0,a}, y->{m,h}, m->{a,x}, a->{y,t1}, h->{t1,t0}). From sigma0=(x->t0,y->m): single switch of x gives (1,1,1,1,1/2) = the game optimum, all-switches gives (3/4,1/2,3/4,3/4,1/2). So all-switches is strictly pointwise-dominated. Kills Mansour-Singh-style counting on SSGs.
- L11 CONFIRMED "SSG-induced USOs can be CYCLIC": the 3-dim Stickney-Watson USO of a 2-Max/1-Min reduced-form stopping game has a directed 6-cycle; all 27 faces have a unique sink, no ties. So acyclic-USO machinery (topological order, clean AUSO RandomFacet) does NOT apply to the two-player cube.
- REFUTED the proposed potential "policy iteration locks >=1 new vertex's final value per iteration" (which would have given P): counterexamples at n=6, seeds 6141 and 6259 in my hk.py harness. The locked SET is monotone, but that follows trivially from HK value monotonicity + val_sigma <= val.
- Hill-climb search for HK-hard instances: n=6..20 reaches only 5..9 iterations. Unstructured search finds no superpolynomial behaviour; hard instances must be engineered.

## Strongest fully proved chain so far (the honest deliverable's spine)
Fixed-point theory for stopping games from scratch -> poly-time Min best response by LP -> switching monotonicity -> Hoffman-Karp correctness -> exact quantitative stopping transformation (beta = 2^-(3N+log N+2), decision threshold 1/2 - 1/(2D), D = 6^{N/2}) -> subcube/facet-exclusion/dead-coordinate structure -> random-facet correctness -> expected 2^{O(sqrt n)} Las Vegas bound, tie-robust (no genericity/perturbation assumptions). Plus SSG -> P-matrix LCP -> Stickney-Watson USO, and poly-time solvability when every SCC is a singleton.

## MY OWN BUG — remember this
My first harness computed val_sigma by GREEDY POLICY ITERATION for Min. That is UNSOUND in non-stopping games: it halts at a suboptimal tau because the alternative successor is evaluated against the current policy's own self-referentially high values. Minimal witness: V_min={m}, V_avg={c}, m->{t1,c}, c->{m,m}; truth val=0 (Min cycles), greedy PI returns 1. It produced a batch of FALSE "non-stopping" findings that I retracted. Always compute val_sigma as the componentwise min over ALL positional tau (or by LP / least fixed point).

## Deliverable in progress
/data/ssg-proof/frontier.tex — compiles via `make pdf TEX=frontier` (11 pages). Contains, all proved by me: least-fixed-point + Knaster-Tarski foundations; contraction/uniqueness for stopping games via the N-stage-game argument with absorption bound 2^-N; the damping-gadget stopping transformation with all constants (m = ceil(5N/2 + log2 N)+3, D = 8^{N/2}); Opt = greedy subcube for stopping games; SHORT IMPROVING PATHS (from any sigma, <= |V_max| single strictly improving switches reach Opt — proof via prefixed-point comparison against an unknown optimal sigma*), whose corollary is that ALL the difficulty is switch SELECTION, not path length; the two verified refutations; and the exact gap statement (Poly-Rule) with a proof that it is equivalent to the target.
Minimal counterexamples I verified: Opt is not a subcube without stopping — 4 vertices, ALL Max, no Min/no Avg: v0->{v3,v2}, v1->{t1,v0}, v2->{v3,v0}, v3->{v0,v1}; Opt={(0,0,0,1),(0,0,1,1),(1,0,0,1)}, missing (1,0,1,1).
Random-facet RF verified to return the exact optimum on 692 runs over stopping games, switch counts always within f(m).

Later additions to frontier.tex, all independently verified by me:
- SHARPENED absorption bound 2^{-a} (a = |V_avg|) instead of 2^{-N}: under a fixed profile the chain branches only at Avg vertices, and a SIMPLE path visits each at most once. This propagates into the stopping-transformation constant (m = ceil(3N/2 + a + log2 N) + 3).
- Theorem: stopping SSGs with a = O(log N) average vertices are in P, in time poly(N)*2^a, by value iteration in fixed-point arithmetic. Does NOT extend via the damping gadget, which pushes a to Theta(N^2).
- Theorem (VI exponential lower bound), verified exactly for m=3..12: player-free family G_m on 2m Avg vertices with val(c1) = 1/2 + 2^-(m+1) exactly; VI steps to cross 1/2 measured 13,37,99,248,595,1385,3149,7041,15545,33985. So value iteration fails for a mixing-time reason, not a precision reason, with NO players involved.
- Theorem: no naive Hamming potential. 2-vertex stopping witness p->{t1,t0}, q->{t1,p}; at sigma=(p->t0,q->p) both are switchable but q's choice is already greedy-optimal. Seven natural poly-time selection rules (max/min gap, max target, min source, first/last index, one-step lookahead maximising sum of values) ALL fail to always pick a "wrong" vertex.
- Theorem: SSG-Value is poly-time EQUIVALENT to SSG-Compare (is val(a) >= val(b)?), and n NON-ADAPTIVE comparisons (one per Max vertex) determine an optimal strategy. Reductions: adjoin h->{t1,t0} with val(h)=1/2; and for the converse, the dual game Gbar (swap sinks AND swap player roles, val_Gbar = 1 - val_G for stopping games) plus a fresh avg start s->{a, bbar}, giving val(s) = (1 + val(a) - val(b))/2. Verified on 1808 (game,a,b) triples.

## Audit outcomes (round-1 audits, both completed)
Audit of MY theorems: statements (D) Opt-subcube, (E) short-paths, (F) both refutations all SOUND under exhaustive + random search (122k stopping games at 3 vertices; the cyclic USO was even realised as a genuine 95-vertex SSG). THREE PROOFS had real holes, all now repaired in frontier.tex:
 (A) lem:lfp's extension from v_{sigma,tau} to T_sigma and T was unproved (needs a limit/infimum exchange). FIX: narrow lem:lfp to profile values, and prove determinacy for stopping games from UNIQUENESS instead (thm:stopping-determinacy) — no import needed.
 (B) thm:contraction restricted the N-stage game to POSITIONAL strategies, but T^N x is the value with TIME-DEPENDENT strategies; refuted by an explicit 6-vertex instance where (T^6 x)(2) = 3/32 but the positional value is 0. FIX: prove lem:absorption by a SINK ATTRACTOR argument, which is strategy-independent.
 (C) lem:gadget's "N + 2m(N-2) <= 2mN" is false unless N <= 4m. FIX: use < (2m+1)N.
 (G) abstract claimed "equivalent" but only one direction was proved. FIX: proved the converse via thm:compare-equivalence + thm:opt-subcube + thm:short-path.
Audit of the random-facet e^{2 sqrt n} bound: could NOT be refuted (~13k exact instances). One real gap: F5 never argued that the k already-dead coordinates stay dead in the SECOND recursive call; the fix is 3 lines and the k term is tight (exact in 693/1304 measured cases). Now written out in full in frontier.tex sec:randomfacet.

## Verified from other agents' work (I re-derived each myself)
- Denominator bound depends only on r = |V_avg|: den(val) <= 8^{r/2}. Proof via the "jump chain" on V_avg. Improves all my constants.
- Transfer-impedance formula for a single switch: f'(v)-f(v) = (f(b)-f(a)) h(v->u)/(1-h(b->u)), h identical in both chains. Verified exactly on 544 switches. Explains why no polynomial-range potential can work: the escape probability 1-h(b->u) can be 2^{-Theta(N)}.
- VI exponential lower bound family (player-free) — verified m=3..12.
- Forest-balance identity: for an ABSORBING induced chain, val = N_1(v)/D with D = #acyclic routings, all forests having equal weight 2^{-|V_avg|}. Verified on 4401 absorbing profiles. NOT included in frontier.tex because it needs the all-minors matrix-tree theorem as an extra import. (My first test wrongly used non-stopping games and appeared to refute it — the theorem needs absorption.)
- All-switches HK CAN exceed |V_max| iterations: verified their 28-vertex, |V_max|=14 instance does 16 iterations with switch counts {3,3,3,3,2,2,2,2,1x6}, val(v0)=1/5. But that game is NOT stopping; under damping the effect weakens (m=3 still shows a vertex switched twice).

## Delivery
User asked (2026-08-26) to sync the paper PDF to Google Drive after every change. Use scripts/sync-gdrive.sh — it runs `make pdf` then `rclone copy` to gdrive:ssg-proof/. rclone is already configured with a `gdrive:` remote. Do NOT use the Drive MCP create_file tool for this: it needs the whole PDF inlined as base64 (~550 KB, ~155k tokens per sync).

## Second audit of frontier.tex (auditC) — findings and repairs
- REFUTED: the LP I gave for val_sigma minimised instead of maximised. Its feasible set is {x : x <= T_sigma x}, so by the comparison corollary val_sigma is the MAXIMUM. The min version is unbounded (auditor: 300/300 instances). Cited in three theorems; fixed.
- GAP: "we may assume the input game is stopping" is NOT free at threshold 1/2 — the stopping transformation moves the threshold. Counterexample: G = single avg vertex c->{t1,t0}, val = 1/2, but val_{G_m}(c) = 255/512 < 1/2. FIX: set D := 2^ceil(3a/2) (a power of two) and adjoin a dyadic THRESHOLD GADGET: a chain of k = ceil(3a/2)+3 avg vertices realising theta = 1/2 - 3/(8D), then query val_{G_m}(v0) >= theta. Proof that theta separates: yes-case gives > 1/2 - 2/(8D) > theta; no-case gives <= 1/2 - 4/(8D) < theta.
- lem:absorption's induction exponent was off by one (must count avg vertices of level <= l(u), not < l(u)); I had already caught and fixed this independently.
- Other fixes: |V(G_m)| = N + 2m(N-2) < (2m+1)N (the old <= 2mN is false unless N <= 4m); disjoint union has 2N-1 not 2N+1 vertices; Phi values in prop:rules-fail are 7/2 and 4 (Phi sums over ALL of V, sinks included); val_sigma was never defined; def:rf step 4 needed to say in which game switchability is tested; the random-facet "tightness" claim was unsupported and is now stated honestly.
- CONFIRMED SOUND by that audit: the whole random-facet section (~122k exact recursions, 0 violations, all five steps of the switch bound checked individually, ties exercised), thm:contraction, thm:stopping-determinacy (no circularity), the (<=) direction of thm:gap-equivalence, lem:duality, and every numerical constant including the 8^{r/2} denominator bound.

## STRENGTHENED: thm:few-avg now needs NO stopping hypothesis
Value iteration converges at rate (1-2^{-a})^j per block of N steps on ARBITRARY SSGs: with sigma* optimal, F^{jN}(0) >= min_tau P^{sigma*,tau}[reach t1 within jN], and the gap is at most P[undecided after jN] <= (1-2^{-a})^j by a POSITIONAL escape lemma (from a live vertex a simple path to t1 has probability >= 2^{-a}). Verified on 1500 games, 1217 of them non-stopping, zero violations, bound tight. So every SSG with a = O(log N) average vertices is in P — and this must be proved BEFORE the damping transformation, which would inflate a to Theta(N^2).

## Positive results now in frontier.tex (each proved by me AND machine-verified)
1. thm:few-avg — ARBITRARY SSGs (no stopping hypothesis) with a = |V_avg|: decidable in poly(N)*2^a, hence P for a = O(log N). Via lem:escape (positional escape, probability >= 2^{-a} along a simple path).
2. thm:one-player — V_min = empty: val = lfp(T) and is the unique optimum of the LP "minimise sum x subject to x >= Tx". Verified on 1577 games incl. non-stopping. The sup-sup exchange is what makes the one-player case work and it fails with a minimiser present.
3. rem:owner-blind — any parameter mu depending only on the digraph and the controlled/average partition (not on Max/Min ownership) takes the same value on a two-player game and on the all-Max one-player game, which is easy by (2); so poly(N,mu) bounds are vacuous unless mu is polynomially bounded everywhere. This is the provable core of round 2's lcp-condition result (the LCP handicap is exactly such an owner-blind quantity and is 2^{Theta(N)} on a two-decision-vertex MDP).
4. thm:avg-acyclic — if NO CYCLE of G contains an average vertex then val is poly-time computable, via the average-jump digraph D(G) (acyclic) processed in reverse topological order, each stage being a deterministic max/min game with terminal payoffs solved by attractor sweeps over the sorted payoffs. Verified on 3477 average-acyclic games, zero mismatches. Incomparable with (1): any number of average vertices allowed, but none on a cycle.
5. thm:player-free — if NO CYCLE contains a CONTROLLED vertex, val is poly-time computable: condense into SCCs, process in reverse topological order; every non-trivial SCC is all-average, so its values solve one linear system (nonsingular because from every vertex that can reach t1 the chain must leave the SCC). Verified on 2239 games, zero mismatches. This is the exact DUAL of thm:avg-acyclic, and the pair gives the conceptual punchline: the problem is easy as soon as the cyclic structure is PURE (wholly random or wholly controlled); difficulty needs randomness and choice on the SAME cycle. Sharpened by thm:vi-lower, whose all-average family is solved by ONE linear solve even though value iteration on it needs 2^Omega(N) steps — slow value iteration is not the same as a hard instance.
6. thm:subexp — random facet, expected e^{2 sqrt n} poly(N).
7. lem:max-deficit (LOCALISATION, strengthens thm:short-path) — for stopping G and non-optimal sigma, let g = w* - val_sigma, M = max g, Z = argmax. Then Z contains a Max vertex that is BOTH wrong AND strictly switchable. Proof: sinks are not in Z; an Avg vertex of Z has BOTH successors in Z; a Min vertex of Z has one; a non-wrong Max vertex u of Z has sigma(u) in Z; and a wrong v in Z with x(sigma_bar(v)) = x(sigma(v)) has sigma_bar(v) in Z. If no wrong vertex of Z were strictly switchable, flipping sigma at exactly those vertices and letting Min pick its Z-successor keeps the token inside Z forever — contradicting stopping. Verified: 2976 pairs, 0 violations; and the sharpness is real — 481 wrong-in-Z vertices were NOT strictly switchable, but no pair ever had ALL of them non-strict.

## thm:order-determines (added after round 2; sharpens thm:compare-equivalence)
For a STOPPING SSG the total preorder induced by w* on V_avg u {t0,t1} determines w* completely and w* is poly-time computable from it. So the certificate is O(a log a) bits, a = |V_avg|, with NO dependence on |V|, |V_max|, |V_min|. Decoding: (1) make every average vertex a terminal; the rest is a deterministic max/min game, and by the attractor lemma each live vertex's CLASS is the best class Max can force, one sweep per class; a vertex in no attractor has value 0. (2) Read off greedy sigma and tau from the classes; then T_{sigma,tau} w* = w*, so w* = v_{sigma,tau} by uniqueness — ONE linear solve. Verified: 903 stopping games, zero mismatches.
MY TWO FAILED DECODER ATTEMPTS (do not repeat): collapsing each live vertex to an arbitrary class REPRESENTATIVE breaks the linear system (99/903 wrong), and even preferring sinks as representatives still fails (6/903) because a representative inside a cycle makes the system degenerate. The fix is not to collapse at all but to read off the greedy strategies.
Note it does NOT give a better algorithm: enumerating preorders is 2^{Theta(a log a)}, worse than thm:few-avg's 2^a poly(N).

## PDC (primal-dual certificate) — the sharpest open question found
Given sigma: tau := Min BR to sigma, rho := Max BR to tau, tau' := Min BR to rho; L := max(val_sigma, val_rho), U := val^{tau'}. Then L <= w* <= U. IF the bracket always decides some Max vertex whose successors differ in w*, then fix-and-recurse gives SSG-Value in P. My small-scale test (1092 pairs, n <= 7): NEVER stalls. Scaled hill-climb: 0% undecided at n <= 20 but 77.8% undecided at n = 26 — so "never stalls" is a SMALL-INSTANCE ARTEFACT. A full stall is what would refute the route. Harness: scratchpad/root_audit/pdc_big.py, pdc_hunt2.py (uses the attractor test for stopping, so it is polynomial per instance and scales).

## The ORDER CALCULUS and the sharpest open combinatorial question
Round 2's selection-direct route proposed a sound purely NON-NUMERIC derivation system for w*(u) >= w*(v) and w*(u) > w*(v): base facts (t1 >= all >= t0, t1 > t0), Max v >= both successors and v <= any common upper bound, the Min dual, an average lies between its two successors, plus transitivity, with strictness propagated. I implemented it (scratchpad/root_audit/ordercalc.py) and VERIFIED ITS SOUNDNESS against exact values.
OPEN QUESTION (sharply falsifiable, and if true gives a polynomial algorithm): does the UNION of {depth-1 primal-dual bracket, order calculus} always decide at least one controlled vertex? Fix-and-recurse then needs only >= 1 bit per round.
My data: on the hard n=26 instance, 15 decidable pairs, bracket decides 4, order calculus 1, UNION 4 — far from complete but NOT empty. The route's own search (~14,500 instances) also never found a union-empty instance. Hunting for one with scratchpad/root_audit/union_hunt.py (hill-climbs to maximise the fraction the union leaves undecided; generates with a sink bias so stopping games are common).
DO NOT mistake "no counterexample found" for evidence: the same searches also fail to find slow Hoffman-Karp instances, which certainly exist for related classes.

## Third audit (auditD, on material added after auditC) — findings and repairs
- thm:few-avg's PROOF was invalid (statement survived ~6100 games). The step "T^{jN}(1_{t1}) >= min_tau Pr^{sigma*,tau}[within jN]" fails both ways: under the POSITIONAL reading it is false (explicit 6-vertex instance where T^6(1_{t1})(5) = 3/4 < 7/8, because Min's optimal finite-horizon play depends on the remaining horizon), and under the general reading the escape lemma does not apply because tau is time-dependent. REPAIR (now in the document, lem:descent): define C_infinity by C_{j+1} = C_j + {avg with SOME successor in C_j} + {max with sigma*(v) in C_j} + {min with BOTH successors in C_j}. Then C_infinity = {v : val(v) > 0}, and from any v in C_infinity the level-descent is FORCED, so ANY history-dependent Min play concedes t1 within N steps with probability >= 2^{-a}. Then with u_j := T_{sigma*}^{jN}(1_{t1}) one gets val - u_j = 0 off C_infinity and M_{j+1} <= (1-2^{-a}) M_j on it, using inf A - inf B <= sup (A-B).
- lem:duality was FALSE as stated ("for every v"): at the sinks val_Gbar(t1) = 1, not 0. Restricted to NON-SINK v. This broke cor:wrong-equivalence and thm:compare-equivalence whenever a successor is a sink — which is the typical case. Repair: replace a sink argument b by a fresh average vertex b' with both edges to b.
- rem:owner-blind was REFUTED as stated, by the document's own theorems: mu = 2^{|V_avg|} is owner-blind and exponential on some one-player games, yet thm:few-avg gives a useful poly(N,mu) algorithm; likewise thm:avg-acyclic's hypothesis is owner-blind. The correct, weaker claim (now in the document): an owner-blind parameter cannot serve as a HARDNESS CERTIFICATE.
- Also fixed: 420 -> 422 vertices; lem:det-game must be applied to the part reachable from u's successors; the escape probability 2^{-Theta(N)} is now backed by an explicit verified family (u -> {t1,c_1}, c_i -> {u,c_{i+1}}, c_k -> {u,t0} gives escape exactly 2^{-k}); and seven abstract/summary overstatements.
- MY OWN BLUNDER: the bulk python replacement that repaired thm:few-avg silently DELETED def:jump, lem:jump-acyclic, lem:det-game, thm:avg-acyclic and thm:player-free. latexmk did not error; only "Reference ... undefined" in the .log revealed it. ALWAYS grep for the labels and for 'Reference.*undefined' after a bulk edit, and do a `make clean` rebuild.

## Union-hunt trend (important)
Fraction of decidable pairs the UNION {bracket, order calculus} fails to decide grows monotonically with size: 0.167 (n=14), 0.222 (n=20), 0.364 (n=26), 0.533 (n=34). So "the union always decides at least one bit" is very likely another small-instance artefact, but NO counterexample has been found yet. Searching at n = 40, 46, 54.

## WHERE THINGS STAND (paused 2026-08-26 20:30 UTC at the user's request — token budget)
frontier.tex is 35 pages, 64 numbered results, clean `make clean && make pdf` with NO undefined references, synced to gdrive:ssg-proof/frontier.pdf (479028 bytes). Every claim in it is proved and every negative claim has an explicit instance verified in exact rational arithmetic. It contains NO polynomial-time algorithm and claims none.
Round 3 (runId wf_34f0b55e-134, 7 routes: pdc-rule, slow-hoffman-karp, dimension-consuming, hardness-barrier, deficit-dynamics, avg-cycle-parameter, free-search-2) was STOPPED before any route returned. To resume: Workflow({scriptPath: '/home/ubuntu/.claude/projects/-data-ssg-proof/6076bc78-583e-4c17-a24f-088177095475/workflows/scripts/ssg-round3-frontier-wf_34f0b55e-134.js', resumeFromRunId: 'wf_34f0b55e-134'}).
Highest-value unfinished work, in order: (1) hunt at n >= 40 for a full stall of the {bracket, order calculus} union — the trend 0.167/0.222/0.364/0.533 at n = 14/20/26/34 says one probably exists; (2) construct a superpolynomial Hoffman-Karp instance; (3) round 3.

## Round tallies
Round 1b (this session, 12 routes): 118 proved lemmas, 16 refuted sublemmas, 15 gaps; ALL routes blocked or dead. Archived at scratchpad/root_audit/round1b.md (597 KB).
Round 2 (8 routes on genuinely new mechanisms: selection-direct, tarski-quasipoly, pinning-dimension, lcp-condition, homotopy-breakpoints, tropical-puiseux, violator-dimension, free-search) launched as runId wf_0dea5c07-e61.

## Gotchas
- Subagents WRITE INTO the shared scratchpad and overwrote my ssg.py. Keep my own harness in scratchpad/root_audit/.
- Prior session hit a session usage limit mid-workflow; workflow resume re-runs only failed agents and replays cached ones.

## Session 1f9100d4 (root) independent verifications, 2026-08-26 21:40 UTC
Re-derived MYSELF with exact rational arithmetic, harness in
/tmp/claude-1000/-data-ssg-proof/1f9100d4-aba7-4dec-bb6f-17b3ce8728ef/scratchpad/root2 :
- thm:order-determines CONFIRMED. I wrote my own decoder from the THEOREM TEXT
  (my_orderdet.py), not from order_decode2.py: terminal classes -> attractor
  sweeps -> greedy sigma/tau -> one linear solve. 4000 random stopping games,
  0 value mismatches, 0 class mismatches. Corroborates the colleague's 903.
- ORDER CALCULUS SOUNDNESS CONFIRMED (my_ordercalc_sound.py): 3000 stopping
  games, 201750 GE facts and 42702 GT facts derived, ZERO violations. This
  matters because every union-stall statistic is meaningless without it.
- Round 3 relaunched FRESH as runId wf_786744ac-96a (resumeFromRunId is
  same-session only, and no route had returned, so nothing was lost).
- Two union-stall hunts running in parallel: the colleague's union_hunt.py and
  my own my_union_hunt.py, which differs deliberately (n = 40..80, LOW direct-sink
  bias because sink edges are what ground strictness in the calculus, dyadic-chain
  seeding since comparing two dyadic chains needs CARRYING, lexicographic accept).
- thm:few-avg + lem:descent CONFIRMED (my_fewavg.py). I read the repaired proof
  line by line (the A(v) counting, the inf-inf exchange, and the sandwich
  u_j <= T^{jN}(1) <= val that lets the ALGORITHM iterate T while the ANALYSIS
  uses F = T_{sigma*}) and found it correct. Then: 700 games, 599 of them
  NON-STOPPING (the case the repair exists for), ground truth by brute force
  over positional pairs (never greedy PI). Zero rate violations, zero decision
  violations, and min slack (bound - gap) = 0: the rate (1-2^-a)^j is TIGHT.
- lem:duality + thm:compare-equivalence CONFIRMED (my_compare.py), 1200 stopping
  games: 0 duality violations off the sinks, 0 violations of
  val(s) = (1 + val(a) - val(b))/2, 0 equivalence violations. AND the sink
  corner case auditD found is not a technicality: comparing against a shared
  sink WITHOUT the b' repair gives the WRONG answer in 703/1200 = 59% of
  instances, while the repair is correct in 1200/1200.
- lem:gadget, lem:denominator, thm:stopping-transform CONFIRMED (my_transform.py),
  250 games with exact G_m: P(reach w) = 1-2^-m for m=1..8; 0 denominator
  violations; 0 violations of Step 1 (val_Gm <= val_G), Step 2
  (val_G - val_Gm <= beta*N*2^a) and the main threshold equivalence.

## MY OWN BUG #2 — remember this
My first damping-gadget implementation numbered fresh chain vertices from n
upward, which COLLIDES with the old sink indices T0 = n, T1 = n+1. That made
G_m route chain traffic straight into t0 and produced 50/250 fake "MAIN
equivalence violations" and 107 fake Step-2 violations against a theorem that
is in fact correct. Carry sinks as SENTINELS ('T0'/'T1') through any such
construction and map them to indices only at the very end. Suspect your own
encoding first when a verified theorem appears to fail with val=1 vs valm=0.

## FAILED SEARCH DESIGN — do not repeat (root session, 21:54 UTC)
I built a third union hunt (my_union_sigma.py) whose genuine improvement is that
it hill-climbs SIGMA adversarially (single-vertex flips) instead of sampling ~18
of 2^|V_max| strategies. But I paired it with a LOW direct-sink bias, reasoning
that sink edges are what ground strictness in the order calculus. That reasoning
is right and the design is still self-defeating, because sink edges are ALSO what
makes a game stopping. Measured stopping rates: sink_bias 0.10 gives 1.3% at
n=24 and 0.0% at n=32 and n=44; sink_bias 0.32 gives 6-10% throughout. So the
run had essentially no valid instances and its output (-1.000 at n=24,32 and
0.300 at n=44,60) is an ARTEFACT, not evidence about the union question — it is
NOT comparable with the colleague's 0.533 at n=34. Relaunched at sink_bias
0.32/0.26, n=34..70, 420 steps.
TENSION WORTH KEEPING: any counterexample must be a STOPPING game, and stopping
forces rich sink-reachability, which is exactly what feeds the order calculus.
This may be part of why 14,500+ instances have produced no stall. It is an
observation, NOT a theorem — do not write it into frontier.tex as one.

## New results I PROVED and added to frontier.tex (root session, 22:00-22:05 UTC)
Paper now 37 pages, 64 numbered results, clean build, 0 undefined refs, synced.
1. rem:few-avg-tight — the contraction factor (1-2^-a) of thm:few-avg is
   ATTAINED, so that analysis cannot be improved. Witness: the ONE-VERTEX game
   c -> {t1, c}, N = a = 1, not stopping, val = 1, T^k(1_{t1})(c) = 1-2^-k, so
   val - u_j = 2^-j = (1-2^-a)^j with equality for every j. Verified exactly.
2. thm:decide-one-bit + def:decision-rule — a DECISION rule (returns one
   controlled vertex and which successor is larger; sound; abstains only when
   every controlled vertex is value-indifferent) exists in poly time IFF
   SSG-Value is in P. This is a DIFFERENT shape from def:missing's switching
   rules, and it is the shape of the bracket / order-calculus routes. Proof:
   fix the decided vertex (Max to the LARGER successor, Min to the SMALLER),
   which preserves stopping and preserves w* by uniqueness of the fixed point;
   each round kills one value-distinguishing controlled vertex; on abstention
   ANY (sigma,tau) satisfies T_{sigma,tau}w* = w*, so one linear solve finishes.
   VERIFIED by me: 1500 stopping games — fixing never changed the value vector
   and never broke stopping; 273 terminal-case instances, 0 violations; 214/214
   full oracle-driven fix-and-recurse runs correct and within n rounds.
   CONSEQUENCE (why the union hunt is the right activity): such a rule can only
   fail by STALLING, so ONE stalling instance refutes it outright — unlike
   (Poly-Rule), whose failure mode is a superpolynomial step COUNT that no single
   instance can exhibit.
3. prop:locality — no sound decision rule can read only a bounded-radius
   neighbourhood. For every k, two stopping games agreeing on the radius-k
   neighbourhood of a Max vertex v but reversing the comparison at v, by
   +-2^-L. Built from two dyadic avg-chains sharing their first k bits and
   differing from bit k+1 on. Verified exactly for k = 2,3,4,6,8.
   Pairs with (2): one bit is enough, and that one bit is irreducibly global.

## MY OWN BUG #3 (caught by self-audit, already repaired in frontier.tex)
My first proof of thm:decide-one-bit fixed the decided vertex by REDIRECTING
both its out-edges to the chosen successor, and argued termination from "the
number of value-DISTINGUISHING controlled vertices drops". That is WRONG:
soundness is VACUOUS at a vertex whose two successors have equal optimal value,
so a sound rule may legitimately keep returning such a vertex, redirection
changes nothing, and the loop never ends.
REPAIR (now in the paper): RETYPE the decided vertex as an AVERAGE vertex with
both edges to the chosen successor. The move is forced either way, so values and
stopping are preserved by the same fixed-point argument, but v leaves the
controlled set, so |Vmax|+|Vmin| drops by exactly one EVERY round, unconditionally.
Verified: 1200 stopping games, collapse never changed the value vector and never
broke stopping; and 240/240 runs of an ADVERSARIAL sound rule that deliberately
picks value-indifferent vertices first still terminate correctly within n rounds.
LESSON: when a rule is only required to be sound, check what it is allowed to do
in the degenerate case; vacuous soundness is a real loophole.

## UNION-STALL TREND EXTENDED (root session, 22:07 UTC) — the key empirical result
I ran the colleague's union_hunt.py at n = 40, 46, 54. New data points:
  n = 14 20 26 34 40 46
  frac 0.167 0.222 0.364 0.533 0.583 0.704
The best near-miss is n=46 with 19 of 27 value-distinguishing pairs left
UNDECIDED by the union {primal-dual bracket, order calculus}. Still no full
stall. The instance is stored in scratchpad/root2/seed46.py (KIND, SUCC) and a
FOCUSED hill-climb seeded from it (focus_hunt.py, sigma hill-climbed, allowed to
grow n) is running — local search around the best known instance rather than
random restarts.
WHY THIS MATTERS NOW: by my thm:decide-one-bit, a rule of this shape can fail
ONLY by stalling, so ONE full-stall instance refutes the whole {bracket, order
calculus} route outright. That makes the hunt decisive rather than suggestive.
Still: 0.704 is NOT a counterexample and must not be reported as one.

## SPARSE-TARGET HUNT + a methodological caveat I must not forget
NEW ANGLE (root session, 22:20 UTC): a full stall does NOT need many undecided
pairs. It needs EVERY value-distinguishing controlled vertex to be undecided, so
an instance with a SINGLE distinguishing vertex the union cannot decide is
already fraction 1.0 and refutes the rule. Both existing hunts maximise
(undecided/pairs, undecided), whose tie-break prefers MORE pairs — the wrong
direction. sparse_hunt.py maximises (undecided/pairs, -pairs) instead: push the
fraction up while SHRINKING the number of distinguishing vertices. Running as
sparse1.log, sparse2.log in scratchpad/root2.
CAVEAT (applies to ALL the hunts, the colleague's included): they take the WORST
sigma over sampled/hill-climbed candidates. A decision rule gets to CHOOSE its
sigma, so fraction 1.0 at the worst sigma shows only that SOME sigma stalls, not
that every sigma does. Before reporting any hit as a refutation, re-check the
candidate across many sigma — including ones produced by a few rounds of
strategy improvement — and report it as a full refutation only if NO sigma
decides anything. Otherwise state precisely that it refutes the rule as
specified with that sigma.
UPDATE (22:20 UTC): I RETRACTED the sparse-target idea after reconsidering and
killed those hunts. Mechanically it works — the hill-climb does reach pairs=1 —
but an instance with a single distinguishing controlled vertex is a nearly
SOLVED game, exactly the kind the bracket decides easily; observed n=12 runs gave
pairs=1 with und=0. Difficulty scales WITH the number of genuinely uncertain
decisions, so shrinking the pair count optimises a target that is easy to reach
and unlikely to be hard. The productive direction is the opposite one: keep
climbing the fraction while GROWING n (focus_hunt.py, seeded at the 0.704
instance), which reached 0.714 at n=49 within 14 steps.
Also: the box has 16 cores and round-3 agents alone pushed load to ~20, so do not
run more than 2-3 hunts alongside a live workflow — I killed my weakest two
(my_union_hunt.py, whose low sink bias made most instances non-stopping anyway).

## ROUND 3 (runId wf_786744ac-96a): pdc-rule returned a VERIFIED refutation
The pdc-rule route delivered an explicit counterexample family G_k (k>=2,
N=5k+21, |Vmax|=2, |Vmin|=3) on which the PDC bracket decides no WRONG vertex,
so PDC-as-switching-iteration loops for ever. It also proved PDC never stalls on
ACYCLIC stopping games, and reported that ~370000 random (game,sigma,BR-triple)
instances at 9-12 vertices produced ZERO stalls — which is exactly why my hunts
and the colleague's never found one: it had to be ENGINEERED, not sampled.
I VERIFIED the k=2 instance MYSELF (verify_pdc_stall.py, brute force over
positional strategies, not their code): 31 vertices, stopping, w*(0..6) =
1/2,1/2,23/64,1/2,1/2,11/32,33/64; Wrong(sigma)={0}; all three BR sets singletons;
bracket sound; PDC decides only vertices 4 and 5, at which sigma is ALREADY
correct, so nothing switches. Confirmed L(1)=11/32 < w*(2)=23/64.

## THE KEY DISTINCTION I ESTABLISHED (now prop:pdc-separation in the paper)
The order calculus derives NOTHING at vertex 0 either, so the UNION also stalls
at that sigma. BUT fix-and-recurse (thm:decide-one-bit) ESCAPES: retiring vertex
4 — useless to a switching iteration because sigma already chose it correctly —
TIGHTENS the bracket enough to decide vertex 0 in the next round. Full run:
retire 4, 0, 2, 5, then abstain legitimately with only vertex 1 left, whose two
successors both have value 1/2, so one linear solve finishes. Value preserved.
Robust: 25/25 runs with RANDOMISED best-response triples and starting sigma end
in legitimate abstention in 4 rounds; zero genuine stalls.
=> A SWITCHING stall is NOT a DECISION stall. The counterexample refutes PDC's
switching iteration, NOT the decision rule built from the same bracket. This is
what makes thm:decide-one-bit more than a reformulation.
Also confirmed my earlier caveat empirically: sweeping all 4 Max strategies, only
sigma=(0->2,4->16) stalls; the other two wrong-vertex strategies are decided. So
the instance does NOT refute a rule free to choose sigma.

## ROUND 3 COMPLETE (wf_786744ac-96a): 17 agents, 0 errors, 7 routes + 10 audits
Verdicts: pdc-rule, slow-hoffman-karp, free-search-2, dimension-consuming,
avg-cycle-parameter = strict-progress; hardness-barrier = blocked.
Full results: subagents/workflows/wf_786744ac-96a/journal.jsonl and
tasks/wmetbqcul.output (281 KB truncated in the notification).

### VERIFIED BY ME AND ADDED TO frontier.tex (now 39 pages)
thm:ladder / def:ladder / rem:ladder — THE EXPONENTIAL HOFFMAN-KARP INSTANCE
(colleague's standing priority (2), now done). Family L_n: Vmax={v_1..v_n},
Vavg={w_1..w_n}, NO Min, v_{n+1}:=t0, w_{n+1}:=t1, v_i->(v_{i+1},w_{i+1}) and
w_i->(v_{i+1},w_{i+1}). N=2n+2, acyclic, stopping. LEAST-INDEX single-switch
improvement from b=0...0 takes EXACTLY 2^n - 1 iterations, visiting all 2^n
strategies; so does the numbering-free SMALLEST-GAP rule; ALL-SWITCHES takes
exactly n. I verified all three myself for n=1..12 (verify_Ln.py, exact
rationals, built from the description not their code): 1,3,7,...,4095.
PROOF (I re-derived it): d_i := W_i - V_i satisfies d_i = (-1)^{pi_i} 2^{i-n-1}
with pi_i = sum_{j>=i} b_j mod 2; switchable set is exactly {i : pi_i = 0};
b -> pi is triangular over F_2 hence a bijection; R := sum pi_i 2^{i-1} is a
bijection onto {0..2^n-1}; flipping b_j maps R to R XOR (2^j - 1), and at the
LEAST switchable index that is exactly R+1. Start R=0, halt at R=2^n-1.
Gap rule: gain at v_i is |d_{i+1}| = 2^{i-n}, strictly increasing in i, so
smallest gap = least index, uniquely.
ALSO VERIFIED: the value VECTOR increases strictly every step but val_b(v_1)
alone does NOT — so no scalar potential read off the start vertex can work.
This is the sharpest form of cor:selection: shortest route n, this rule 2^n-1.

### STILL TO VERIFY / INTEGRATE from round 3 (I have NOT checked these)
- free-search-2: val = lfp(T) for ARBITRARY SSGs (frontier.tex explicitly
  declines to prove this) + poly(N)*2^kappa, kappa = longest simple path in an
  SCC of the average-jump digraph (kappa=3 on games with 577 avg vertices).
- hardness-barrier: SSG-Value in UP n coUP; every information-theoretic barrier
  is vacuous (2^n-query lower bound already holds for linear-time one-player
  games); family K(d) killing rules that read val_sigma + one-step lookahead +
  radius-d structure (GENERALISES my prop:locality).
- dimension-consuming: recursion consuming avg-cycle transversal tau, poly for
  tau=O(1), N^{O(log N)} for tau=O(log N), verified to N=363, plus a matching
  conservation theorem (no freezing recursion can halve tau).
- avg-cycle-parameter: m = min deletions leaving no cycle carrying BOTH
  randomness and choice; poly(N)*(log N + 7|V_avg| + 14)^m; S-local damping
  preserving the parameter.
AUDIT FLAGS (from the round's own audits, repairable): slow-hoffman-karp cites a
theorem/proposition NOT in frontier.tex; avg-cycle-parameter's SCC-purity
equivalence is false as stated because SINKS are singleton SCCs in neither class;
one theorem is stated for rational payoffs but proved only for dyadic; one lemma
attributes to thm:determinacy something it does not contain.

## SHARPENED thm:ladder (root session, 23:05 UTC) — verified myself
On L_n the optimum is Opt = {0...01} with w*(v_1) = 1 (Max walks the v-chain to
v_n then steps to t1). At b = 0...0 EVERY v_i is switchable, and switching the
LAST one reaches Opt in ONE step. BFS over the improving-switch digraph confirms
the shortest improving route has length exactly 1 for n = 1..12.
So the separation is not "linear vs exponential" but "ONE switch vs 2^n - 1":
the least-index rule misses a one-step route by an exponential margin. This is
the extreme form of cor:selection and is now in rem:ladder.
Consistency check passed: thm:short-path (<= |Vmax| switches) and thm:ladder
(2^n - 1 for least-index) are compatible, as they must be — different rules.

## ROUND 4 COMPLETE (wf_e3806976-bac): 27 agents, 0 errors, 9 routes + 18 audits
Verdicts: verify-lfp, verify-upcoup, verify-params, flow-electrical,
conductance-mixing, decision-stall, free-search-3, sos-certificates =
strict-progress; parameter-bounding = blocked (parameter reduction proved
EQUIVALENT to the target). Full output: tasks/whvcvt40u.output (586 KB).

### A REAL DEFECT IN THE PAPER, FOUND BY ROUND 4 AND NOW FIXED
thm:few-avg's proof asserted, with NO argument, "Because sigma* is optimal,
val = val_{sigma*} ... therefore satisfies F val = val". That is exactly
val_sigma = lfp(T_sigma) for a NON-STOPPING game, which rem:lfp-scope
simultaneously declined to prove AND claimed was never used. MY OWN earlier
audit of thm:few-avg glossed this step as "val = F val since sigma* optimal" —
I missed it; the agent did not.
FIX (mine, now in the paper): added lem:excursion (first-passage decomposition:
q(u) = Pr[t1 before v], r(u) = Pr[v before t1]; q,r do not depend on v's own row;
v_{s,t}(u) = q(u) + r(u) v_{s,t}(v)) and thm:lfp-general (for ARBITRARY SSGs
T_sigma val_sigma = val_sigma, val_sigma = min{x : T_sigma x <= x}, and the same
for T and val). The Min-side crux F(v) <= F(w): with tau' = tau*[v->w], either
r(w)=1 (then q(w)=0 and F(w)=F(v)) or F(v) <= q(w)/(1-r(w)) giving
F(w) = q(w)+r(w)F(v) >= F(v). No limit/infimum exchange anywhere — that is what
makes it work without stopping. rem:lfp-scope rewritten honestly: only the
PREFIXED half survives (x <= Tx does NOT give x <= val; witness c->{c,c}).
I verified first: 1500 games, 1389 NON-stopping, zero violations of T val = val,
of T_sigma val_sigma = val_sigma, or of leastness. Paper now 41 pages.

### G* — the 19-vertex decision stall, VERIFIED BY ME
Vmax={0,1,2}, Vmin={3,4,5,6}, Vavg={7..16}, t0=17, t1=18, succ =
(4,12),(16,15),(13,14),(4,13),(2,16),(8,0),(10,15),(18,0),(0,14),(17,6),(16,11),
(7,13),(7,11),(9,4),(15,7),(5,10),(13,15).
I confirmed: stopping; w* = 24/31,43/62,49/62,27/62,35/62,24/31,19/31,55/62,
97/124,19/62,19/31,41/62,24/31,27/62,49/62,43/62,35/62 (brute force over all 128
positional pairs); ALL SEVEN controlled vertices distinguish values; and the
ORDER CALCULUS decides NOTHING there (sound, 0 violations). So the round-4 audit
that claimed a refuting computation against the order-closure step is WRONG for
the calculus as implemented and verified here — though "the full sound order
closure" is not a canonical object, so a richer sound rule set might differ.
CRUCIALLY, on my own retire-and-recurse rule: G* stalls it at round 0 from the
CANONICAL all-first-successor sigma (6 of 24 trials), but from other starting
strategies it retires all 7 vertices in 7 rounds and preserves the value. So G*
refutes the single-round rule from that sigma, NOT the paradigm.
THE DEEP POINT (agent's corollary, worth adding): a decision stall at depth R
implies every Hoffman-Karp trajectory needs > R iterations, so a stall against a
POLYNOMIAL-round rule IS a superpolynomial Hoffman-Karp lower bound — open. On
G*, HK reaches Opt in 2 iterations, so the rule decides everything at R >= 2.
That is why ~370000 random instances found no stall: a stall needs HK length >= 3,
a sub-1% event.

### STILL UNINTEGRATED (audited-confirmed, I have not personally verified)
- flow-electrical: escape probability NEVER below 2^{-a}; lem:denominator improves
  8^{a/2} -> 2^a and is ATTAINED; hence EVERY improving-switch rule on a stopping
  SSG terminates within N*2^a switches, matched by the ladder to a factor N.
- verify-upcoup: SSG-Value in UP n coUP, unique witness = the VALUE VECTOR (not a
  canonicalised strategy, which is genuinely broken); by-product removes the
  paper's ONLY import (thm:determinacy).
- verify-params: algorithm (B) true with its constant; (A)'s poly(N)2^tau NOT
  established; and mu <= tau <= |V_avg| always (so NOT incomparable).
- sos-certificates: degree-2 Lasserre refuted by an explicit family; exact iff
  rho(M) < 1/2; damping forces rho(M) = 1-2^{-Theta(N)}, into the failure regime.

## INTEGRATED into frontier.tex (now 42 pages, 73 numbered results) — all verified by me first
- lem:watched (watched-chain factorisation: for S >= 0 with row sums <= 1 and
  rho(S) < 1, det(I-S) = prod(1-s_k) <= 1, by Schur complementation at (1,1) with
  a Perron-Frobenius step) and lem:denominator-sharp: det A_U <= 2^{|U|}, so every
  value has denominator dividing an integer <= 2^a. IMPROVES the paper's 8^{a/2}
  = 2^{1.5a} and is ATTAINED (the ladder's w_1 has denominator exactly 2^n).
  I left the old constant in the downstream STATEMENTS on purpose — 2^a <= 8^{a/2}
  so everything stays valid — and added a remark that D := 2^a and
  m := ceil(2a + log2 N) + 3 now work in thm:stopping-transform.
- thm:switch-count: EVERY single-switch improving rule on a stopping SSG stops
  within N*2^a switches; every multi-switch rule within N*4^a; tight to a factor
  N by thm:ladder (which attains 2^a - 1). Proof: Phi = sum of values rises by at
  least 2^{-a} per switch, because val_{sigma_{j+1}}(v_j) = val_{sigma_{j+1}}(bar
  sigma_j(v_j)) >= val_{sigma_j}(bar sigma_j(v_j)) and a positive difference of two
  coordinates of the SAME vector has denominator <= 2^a. Multi-switch compares
  coordinates of DIFFERENT vectors, whence 4^{-a}.
  I verified all three numerically first: 350 stopping games — 0 denominator
  violations (worst ratio exactly 1), 0 Green-function violations, 0 Phi-gain
  violations (min gain * 2^a exactly 1). BOTH bounds attained.
- THE GRID BARRIER, stated in the paper: progress measured in the value vector is
  now settled in BOTH directions — no such argument can prove better than 2^a or
  worse than N*2^a, and it is polynomial exactly when a = O(log N), the regime
  thm:few-avg already covers. Any polynomial bound must come from elsewhere.

## ROUND 5 LAUNCHED (runId wf_6d62a512-054, 8 routes)
beyond-grid (is there a monotone measure NOT a function of val_sigma? a theorem
that every poly-time monotone measure FACTORS THROUGH val_sigma would close the
family); up-witness (make the UP certificate algorithmic — note val(v0) has only
2^a candidate values, so halving the candidate set per query would be new);
hk-lower-bound (THE PIVOT: a decision stall at polynomial depth IS a
superpolynomial Hoffman-Karp bound; build the counter with Max bits in ONE SCC of
the mutual-reachability digraph, since all-switches is capped by sum_j 2^{|S_j|});
nonstopping-direct (avoid damping entirely, since it inflates every parameter);
two-party-communication; algebraic-elimination (forest-balance/all-minors);
lower-bound-model (honest restricted models, must state which real algorithms the
model FAILS to capture); free-search-4.

## ROUND 5 COMPLETE (wf_6d62a512-054): 24 agents, 0 errors, 8 routes + 16 audits
Verdicts: beyond-grid = BLOCKED (progress-measure family closed); two-party-
communication = DEAD; the other six = strict-progress. Output: tasks/wdc671307.output.

### INTEGRATED (43 pages, 74 results)
cor:no-height — no progress measure has polynomial HEIGHT. mu assigns each
stopping SSG a poset and a map on Max strategies increasing along every improving
switch; NO computability, NO numeric codomain assumed. Height >= 2^n on L_n.
One-line proof from thm:ladder, and I flagged it in the paper AS an immediate
corollary rather than dressing it up — an audit correctly said the beyond-grid
route's version was "thm:ladder restated in other words". The remark now
separates the three barriers: thm:impedance kills polynomial RANGE,
thm:switch-count bounds RULES via the value grid, cor:no-height constrains the
MEASURE with no hypothesis at all. What survives is exactly def:missing: a
measure attached to ONE rule.

### MY OWN BRIEFING ERRORS, caught by the hk-lower-bound route's citation audit
(1) I told round 5 that "all-switches terminates within sum_j 2^{|S_j|} over SCCs
of the Max-reachability digraph" was ESTABLISHED. It is NOT in frontier.tex — it
was a round-3 agent result I never integrated. The route proved it independently.
(2) I described "a decision stall at depth R implies Hoffman-Karp needs > R
iterations" as an equivalence. It is only ONE direction: if all-switches ran in
poly rounds on every stopping SSG, a sound non-stalling poly decision rule would
exist, so a stall against every poly-round rule DOES imply HK is superpolynomial.
The CONVERSE does not follow and is unproved. Do not call it an equivalence.
LESSON: state in agent briefs which facts are IN frontier.tex and which are
unintegrated agent claims; agents check citations against the file and will
(rightly) call this out.

### PROVED BUT NOT INTEGRATED (my evidence too thin, or audits split)
- ANTICHAIN LAW (all-switches: S_t is never a subset of S_{t+1}), whose corollary
  is that the classical binary-counter gadget is UNREALISABLE for any wiring, any
  size — the value vector strictly increases at every switched coordinate, so a
  switched set cannot be undone next step. My check: 0 violations but only 116
  consecutive pairs (all-switches runs are very short: mean 0.61 steps, max 3).
  Too thin to integrate on my own evidence; the agent's proof looks right.
- Forest-balance: val = N1(v)/D, D = #acyclic routings = 2^a det(I-Q); would give
  instance-wise N*D(G) in place of N*2^a. One audit REFUTED it as stated.
- Bounded re-entry width (from the dead communication route) and Max-SCCs of size
  O(log N): two NEW polynomial classes, unverified by me.
- Propagation calculus P: unconditional 2^{Omega(N)} lower bound covering all
  asynchronous value-iteration/interval-propagation algorithms at once; plus a
  preprocessing-collapse meta-theorem killing the query/precision/ADT/monotone-
  circuit lower-bound routes. Audited sound=True high. Worth integrating next.
- free-search-4: a value-simulation preorder (one greatest fixed point, N^2
  comparison bits) that PROVABLY BREAKS prop:locality at every radius, then is
  refuted as a decision rule by an 8-vertex game. The positive half is notable —
  it is the first mechanism to beat the locality barrier.

## NEW SECTION IN frontier.tex: the value-simulation preorder (45 pages, 77 results)
sec:simorder — def:simorder, thm:simorder-sound, prop:simorder-stalls.
A sound poly-time ARITHMETIC-FREE comparison mechanism: one greatest fixed point
on V x V, O(N^4), returning a verdict for all N^2 ordered pairs AT ONCE. Clauses:
(down) one vertex vs a successor of y; (up) a successor of x vs one vertex;
(match) same-type vertices with successors paired — for Vavg by a BIJECTION,
which is the only place the fair coin is used.
MY VERIFICATION (reconstructed the rule from the description, my own code):
- 500 random stopping games: SOUND, 0 violations over 22682 derived pairs, and it
  separated 818/818 = 100% of value-distinguishing controlled vertices.
- IT CRACKS BOTH ENGINEERED STALLS: on G* (where bracket + order calculus decide
  NOTHING) it separates 6 of 7, including vertex 0 that the bracket never decides;
  on the 31-vertex PDC instance it separates 2 of 4, including the wrong vertex.
- G8 REFUTATION VERIFIED: 8 vertices, types (avg,avg,avg,avg,avg,max), edges
  0->(0,t1), 1->(0,t0), 2->(t0,4), 3->(0,2), 4->(3,2), 5->(4,1); w* =
  (1,1/2,1/5,3/5,2/5,1/2) by brute force; the unique controlled vertex 5 has
  successors of values 2/5 and 1/2 and neither 4 <= 1 nor 1 <= 4. So the rule
  STALLS and by thm:decide-one-bit gives no polynomial algorithm.
I COMPLETED THE SOUNDNESS PROOF myself (the transmitted version left the key step
implicit): with D(y) = {x : x <= y} and f(y) = max{w*(x) : x in D(y)}, show
f <= Tf and conclude f = w* by cor:comparison. The step that needed work: if every
x in the argmax set M satisfied ONLY the (up) clause, then M would be sink-free
and closed under a positional pair (Vmin/Vmax pick an M-successor, Vavg has both),
so the token would never be absorbed — contradicting stopping. Hence some x in M
satisfies base/(down)/(match), and each of those yields c <= (Tf)(y) directly.
THE OBSTRUCTION, now named in the paper: every clause matches branches ONE TO ONE,
so a deficit on one branch of an average vertex cannot be repaid by a surplus on
the other. G8 is the smallest instance where that compensation is essential. This
is a DIFFERENT failure from prop:locality — the preorder is global and beats every
bounded radius — and it suggests a sound comparison mechanism must eventually ADD
two branches, i.e. do arithmetic.

## VALUE-SIMULATION PREORDER: empirical characterisation (my own, root session)
- Stall rate by size, 220 random stopping games each at n = 5,7,9,11,13 (1100 total):
  ZERO stalls, ZERO partial — it separated EVERY value-distinguishing controlled
  vertex in EVERY game (mean 100%). Soundness: 0 violations throughout.
- It also fully decides the LADDER L_n for n = 2..6 — the family on which
  least-index strategy improvement takes 2^n - 1 steps. So the instance that is
  exponentially hard for improvement is trivial for this mechanism.
- Stalls therefore must be ENGINEERED (the recurring theme of this whole project:
  random search never finds the hard instances). A deliberate hill-climb biased
  toward average vertices found a SECOND, independent stall at 10 vertices:
  kind = [avg,avg,avg,max,avg,avg,avg,avg], succ = (9,8),(7,2),(5,4),(1,0),(8,0),
  (2,9),(8,6),(3,5), T0=8, T1=9; w* = 1/2,7/12,1/2,7/12,1/4,3/4,0,2/3; the unique
  controlled vertex 3 -> (1,0) has values 7/12 vs 1/2 and is NOT separated.
- STRUCTURAL SIGNATURE CONFIRMED: both witnesses are average-heavy (G8: 5 of 6
  non-sinks are avg; this one: 7 of 8). That is exactly the branch-compensation
  obstruction — you need average vertices whose two branches STRADDLE the value
  being compared, so that a deficit on one is repaid by a surplus on the other.
  The hill-climb found nothing at n=6 and succeeded at n=8, consistent with G8
  being near-minimal.
NOT added to frontier.tex: these are empirical observations about search, not
theorems, and the paper's standard is proved claims plus explicit instances.

## ROUND 6 LAUNCHED (runId wf_8be27250-efb, 8 routes)
arithmetic-preorder (the direct successor: greatest fixed point on TRIPLES
(x,y,delta) meaning w*(x) <= w*(y) + delta, averaging slacks at avg vertices —
the crux is the BIT-SIZE of delta after k rounds; poly-bit slack that is
non-stalling would BE the target, superpolynomial slack would be a new barrier
generalising prop:locality and prop:simorder-stalls); compensation-barrier (prove
EVERY sound "local matching calculus" stalls); propagation-lower-bound (verify or
refute the unintegrated 2^{Omega(N)} claim, and settle whether bracket-certificate
size is Theta(N(a+1)), which would make proof-size lower bounds unavailable);
unify-classes; gray-code-hk; two-branch-calculus (precision hierarchy: order only
/ O(log N)-bit dyadic / poly-bit rational / unrestricted); certificate-search;
free-search-5. This round's brief explicitly marks which facts are IN frontier.tex
and which are UNVERIFIED agent claims — the fix for my round-5 briefing error.

## ROUND 6 (wf_8be27250-efb): 24 agents, 0 errors. THE SLACK CALCULUS — integrated
frontier.tex now 47 pages, 82 results: new sec:slack with def:slack,
thm:slack-sound, prop:slack-repairs, thm:slack-barrier, cor:slack-stalls.

MY HYPOTHESIS WAS WRONG, PRODUCTIVELY. I briefed the route that the crux would be
the BIT-SIZE of the slacks. It is not: entries of Delta_k lie in 2^{-k}Z, so k
rounds cost O(k) bits — cheap. The real obstruction is different and better.
- def:slack: Delta_0 = 1; each round takes the min over clauses (down)/(up)/
  (match)/bases, clamped to [-1,1]; reading "w*(x) <= w*(y) + Delta(x,y)", so a
  NEGATIVE entry decides the pair. Soundness holds for ARBITRARY SSGs (uses only
  T w* = w* via thm:lfp-general), because every clause is EXACT at
  D(x,y) = w*(x) - w*(y): c - max = min(c - .), c - min = max(c - .), and max/min/
  mean all commute with adding a constant.
- IT REPAIRS G8: Delta_k(4,1) = 1, 1/2, 1/4, 1/8, 1/16, 0, -1/32 — I verified this
  and soundness at every k myself. So branch compensation IS fixable.
- THE BARRIER (thm:slack-barrier): if A, B are DISJOINT, closed under non-sink
  successors, and avoid Z_0 u Z_1, then Delta_k(x,y) >= u_k(x) - l_k(y) with
  u_k = T^k 1, l_k = T^k 0. So on non-interacting parts the calculus IS two-sided
  value iteration and cannot outrun it. Proof: check each clause against
  E_k = u_k - l_k, using u_{k+1} <= u_k for (down) and l_{k+1} >= l_k for (up).
- cor:slack-stalls: H_m = thm:vi-lower's G_m plus h -> {t0,t1} and Max v -> {c_1,h};
  N = 2m+4, w*(h) = 1/2 vs w*(c_1) = 1/2 + 2^{-(m+1)}, and BOTH directions stay
  positive for k < ln2 * 2^{m-2}. I verified stopping, w*(h) = 1/2, the stall at
  k = 12 for m = 3,4,5, and ZERO domination violations.
- WHAT ESCAPES: the transitivity clause Delta(x,y) <= Delta(x,z) + Delta(z,y),
  whose premises leave the separated region, so thm:slack-barrier does not cover
  it. Whether transitivity suffices is OPEN and is the live successor question.

THE TWO SECTIONS NOW BRACKET THE DIFFICULTY: an order-theoretic global mechanism
is cheap, beats every bounded radius (prop:locality), and dies on branch
compensation; the natural arithmetic repair fixes that and instantly inherits the
value-iteration lower bound. Precision is not the enemy; non-interaction is.

## ROUND 6 REMAINING ROUTES DIGESTED + THE MATCHING BARRIER INTEGRATED (48 pp, 85 results)
NEW IN PAPER: sec:matching-barrier — def:lmc, lem:fooling-partner,
thm:matching-barrier, rem:magnitude. THE BARRIER IS PROVED FOR THE WHOLE CLASS:
no sound "local matching calculus" (facts w*(x) <= w*(y) derived from successor
facts by clauses over the radius-1 frame, no arithmetic; def:simorder is one)
can decide G8's unique controlled vertex — in EITHER fixed-point reading, and
robust under TRANSITIVE CLOSURE. Mechanism: fooling pair. G_# (7 all-average
vertices: a0->(b0,a1), a1->(b1,a2), a2->(t0,t0), b_i->(b_i,t1), d->(e,t0),
e->(e,t1); w* = 3/4,1/2,0,1,1,1/2,1) gives a pair (a0,d) with the SAME frame and
the SAME true-atom set Pi = {(x,y0),(x0,y0),(x1,y),(x1,y0)} as G8's (4,1), but
the OPPOSITE verdict. Any clause A subset Pi that would derive (4,1) in G8 fires
in G_# at (a1,d) from the base, then at (a0,d), deriving 3/4 <= 1/2. Transitive
closure killed by relay gadget K_# (g->(g,t1), h->(h,t1), k->(h,t0), Max
m->(g,k)): (m,k) shares the frame of G8's (5,1) INCLUDING the equality pattern
x^(1) = y, and would derive 1 <= 1/2. I VERIFIED EVERY FACT: G_# and K_# values,
frame equality, true-atom equality, both derivation chains, base membership
(verify_fooling.py). The route's ORIGINAL insight, my write-up of the proof.
- rem:magnitude replaces my earlier "must do arithmetic" moral, which the round
  REFUTED in spirit: the proved obstruction is comparing MAGNITUDES of surplus
  vs deficit (2/5 vs 1/5 in G8; 0 vs 1/2 in G_#), inexpressible by order-only
  radius-1 premises. It does NOT say numbers are required (free-search-5 has an
  UNVERIFIED arithmetic-free two-token mechanism deciding G8, obstructed later by
  balanced partitions). The two barriers now frame mechanism design exactly:
  weigh surplus against deficit withOUT collapsing into value iteration on
  non-interacting parts (thm:slack-barrier).
- FIXED MY OWN DEFECT (caught by round 6): prop:simorder-stalls cited "the game
  G*" which was never defined in the paper (the 19-vertex decision-stall instance
  lived only in my scratchpad). Now defined INLINE in the proposition with full
  vertex data and the precise verified claims. Also: preamble needed stmaryrd for
  llbracket — README lists it but the preamble never loaded it.
STILL UNINTEGRATED from round 6 (unverified by me): trichromatic width tri(G)
subsuming all four polynomial classes (6850-game check by the route, ready_to_paste
exists); threshold-vs-margin precision split (Theta(a) bits tight for threshold
mechanisms); certificate-search's stopping-free val_sigma evaluation + multi-switch
soundness (several audits flagged overstatements — integrate only after repair);
gray-code-hk's third law refuting the Gray-code shape; two-token additive
simulation. Round 7 candidates: verify tri(G); the transitivity-slack question;
free-search-6.

## ROUND 7 LAUNCHED (runId wf_96ccca53-770, session 542b36e2, 8 routes)
Cross-pollination round per the brief (independent mechanisms now developed far
enough): bracket-seeded-slack (seed Delta_0(x,y) = min(1, U(x)-L(y)) from
policy-evaluation brackets — thm:slack-barrier's proof assumed Delta_0 = 1, so
seeding sidesteps it; MY CHECK: on H_m the seed decides at round 0, Delta_0(h,c1)
= -2^{-(m+1)} for m=3..10 — but ONLY because |V_max|=1 makes L = w* exactly; the
general question is open and the route hunts the next engineered stall);
verify-tri (trichromatic width); verify-stopfree (repair overstated stopping-free
machinery); two-token (verify + extend the fooling-pair method to pairs-of-pairs;
level-Omega(N) barrier question); transitivity-slack (the open clause);
one-player-howard (all-switches on Max-only SSGs: superpoly or poly — NOT
target-equivalent either way, and prop:allswitch-overshoot's 28-vertex game is
already one-player with 16 > 14); reopen-under-new-facts (random facet with
retirement; leaner damping; LCP with routing-count determinants); free-search-6
(difference-system operator, coupled interval abstractions, amortised solving).
NOTE: session id changed to 542b36e2; old harness still at
/tmp/claude-1000/-data-ssg-proof/1f9100d4-.../scratchpad/root2.

## ROUND 7 (wf_96ccca53-770): 6/14 agents done, 8 hit the session limit; RESUMED
(resume task w0pp7n98p; completed agents replay from cache).

### INTEGRATED: stopping-free evaluation (49 pages, 89 results)
New in sec:operators after thm:lfp-general: def:trap, lem:trap,
lem:trapped-comparison, thm:eval-stopfree, rem:lp-needs-zeros.
- def:trap: Z_sigma = largest U avoiding t1 with [Min: SOME successor in U; Avg:
  BOTH; Max: sigma(v) in U]. CRUCIAL SUBTLETY I got wrong first: t0 IS allowed in
  U — only t1 is excluded, because reaching t0 also gives value 0. With t0 wrongly
  excluded my check reported 447 mismatches; with it admitted, ZERO across 260
  games (239 NON-stopping) and all their strategies.
- thm:eval-stopfree: val_sigma is the unique optimum of the max-sum LP PLUS the
  rows x(v)=0 on Z_sigma, on ARBITRARY SSGs, poly time, denominators <= 2^a. Proof
  via lem:trapped-comparison (x <= Px implies x <= P^k x; split by destination;
  transient mass <= (1-2^{-N})^{k/N} -> 0), noting every sink-free bottom class of
  any (sigma,tau) lies in Z_sigma.
- rem:lp-needs-zeros: WITHOUT the zero rows the program is UNSOUND on non-stopping
  games — witness m->{m,t1}: val_sigma = 0 but x(m)=1 is feasible and maximal.
  My check: 9202 of 12215 sampled feasible points exceeded val_sigma, and ZERO of
  those vanished on Z_sigma, so the repair kills exactly the right set. The
  asymmetry is real and now stated: on the MIN-frozen side deleting the zero set
  does NOT restore uniqueness (x->{x,c}, c->{t0,t1}: every value in [1/2,1] is a
  fixed point of T^tau, empty zero set); the right instrument there is the
  MINIMUM-sum program of thm:one-player.
- NO DEFECT IN THE PAPER: eq:lp explicitly invokes cor:comparison and lives inside
  a stopping-game theorem, so it was always correctly scoped. What round 6 got
  wrong was the CLAIM that its soundness needs no stopping; round 7 refuted that
  and supplied the correct repair. I wrote the program out INLINE in the new
  theorem rather than forward-referencing eq:lp 2000 lines later.
- Route verdict context: this machinery lands in the 2^a poly(N) regime already
  settled by thm:few-avg, but by a structurally different algorithm that runs on
  the ORIGINAL game with no damping blow-up. It cannot beat 2^a (thm:switch-count
  transfers; the ladder's lower bound applies verbatim), so the selection
  mechanism of def:missing / thm:decide-one-bit is untouched.

## ROUND 7 COMPLETE (24 agents, 0 errors). SEEDED SLACK INTEGRATED — 51 pp, 94 results
New sec:seeded: def:seeded, thm:seeded-sound, thm:seeded-barrier,
thm:seed-dichotomy, prop:seeded-decides, rem:frontier-moved. Summary section
rewritten with a new "Mechanisms, and where they stop" paragraph.

MY CROSS-POLLINATION PREMISE WAS FALSE, AND THAT IS THE POINT. I briefed the route
that seeding ESCAPES thm:slack-barrier. It does not: thm:seeded-barrier lifts the
barrier verbatim with u_k = T^k U, l_k = T^k L. The barrier is about the GEOMETRY
(disjoint successor-closed parts), never the initialisation. I VERIFIED: 0
domination violations on H_3, H_4 across seeds (T^j 0, T^j 1), j = 0..3.
My earlier "seed decides H_m at round 0" observation is consistent and was never
a counterexample to the barrier: with |V_max| = 1 the bracket is EXACT, so the
barrier's own lower bound u_k - l_k equals D and is itself decisive.

WHAT SEEDING REALLY BUYS (thm:seed-dichotomy): if sigma has no strictly switchable
vertex and tau is greedy for val_sigma, then val_sigma = val^tau = w*, so the seed
is EXACT and everything is decided at round 0. Contrapositive, and this is the
frontier statement: EVERY stalling instance of M(p,k) has BOTH players present AND
is a stopping SSG on which switch-all improvement has not converged after p rounds.
So a stall with polynomial p IS a superpolynomial switch-all lower bound — open,
and explicitly NOT claimed in the paper.

VERIFIED BY ME: on the 31-vertex PDC instance the bracket test fails
(L(1) = 5/16 < 3/8 = U(2)) and prop:bracket(a) forbids ANY sound upper bound from
deciding vertex 0 from that L — yet seeded slack decides it at k=3 with
Delta_3(2,1) = -1/8, soundness 0 violations at every k. My -1/8 matches the
route's stated p=0 figure exactly (their -21/256 at k=1 used a stronger p=1 seed).
This is the concrete sense in which the slack clauses are strictly stronger than
bracket comparison: they propagate a DIFFERENCE instead of comparing L against U
coordinatewise.

STILL UNINTEGRATED (unverified by me): trichromatic width; two-token simulation and
whether the fooling-pair method lifts to pairs-of-pairs; the transitivity question;
one-player Howard; reopen-under-new-facts (random facet with retirement, leaner
damping, LCP with routing-count determinants). Round 8 candidates.

## SESSION 3792e9e6 (2026-08-27). ROUND 8 LAUNCHED + MY OWN NEW BARRIER
Round 8 = runId wf_4d90b0fe-2d0, 9 routes x 2 adversarial audits = 27 agents:
transitivity-slack (the one clause thm:slack-barrier does not cover; view it as
all-pairs SHORTEST PATH closure), coupling-transport (fractional/LP repair of the
bijective branch matching that thm:matching-barrier kills), order-space-search
(search PREORDERS on Vavg, justified by thm:order-determines, instead of strategy
space; does cor:no-height transfer there?), value-gadget-algebra (exact gadgets
for (p+q)/2, pq, 1-p, dyadic constants, and SEQUENTIAL REPETITION WITH A SCORE
COUNTER giving val = Pr[Bin(k,p) > k/2]; then gap amplification and the
self-reduction "halve a", which would give N^{O(log a)}), howard-lower-bound
(verify the antichain law (u3) and (u8); build a superpolynomial all-switches
family), verify-tri ((u1),(u2)), two-token-pairs ((u4) + does the fooling-pair
method lift to multiset states?), algebraic-sign (M/L-natural concavity of
sigma -> val_sigma; a PROXIMITY theorem would give a scaling algorithm),
free-search-7. Brief marks explicitly which facts are IN frontier.tex and which
are the unverified claims (u1)-(u8).

### MY OWN NEW RESULTS, PROVED AND INTEGRATED (frontier.tex now 56 pp)
Harness: scratchpad/root_audit (core.py, attr.py, attr2.py, rules.py, t1..t9.py).
1. lem:trapchar — U is a TRAP if every average vertex of U has BOTH successors in
   U and every controlled vertex of U has SOME successor in U; G is stopping iff
   the only trap is empty. Corollary: THE SUBGRAPH INDUCED ON Vmax u Vmin OF A
   STOPPING GAME IS ACYCLIC (a controlled cycle is a trap). Verified: 0
   violations, and 1007 of the non-stopping samples do have a controlled cycle.
2. def:residue / def:residue-rule / thm:residue-correct — freeze Vavg at
   val_sigma, solve the resulting FINITE DETERMINISTIC max/min game exactly by
   backward induction (finite by 1), adopt its optimal Max strategy, tie-break
   "keep sigma(v) if it already attains the max". Monotone, halts exactly at Opt,
   <= N*4^a rounds. Proof: val_sigma|C is the residue value under sigma (unique
   solution of the backward induction), so D >= val_sigma; then T_{sigma'} D >= D
   and cor:comparison gives val_{sigma'} >= D; equality squeezes D = x and forces
   Tx = x.
3. prop:residue-ladder — ONE improving round on L_n, against n for all-switches
   and 2^n - 1 for least-index.
4. lem:normalform + def:residue-blind + thm:normalform-barrier — THE NEW BARRIER.
   N(G) replaces each controlled out-edge (v,u) by v -> c_{v,u} -> u,u with
   c_{v,u} a fresh AVERAGE vertex; <= 3N vertices, controlled vertices become an
   INDEPENDENT SET, stopping/values/S_sigma/the whole all-switches trajectory are
   preserved. On such games the residue rule IS all-switches. Hence NO
   residue-blind rule runs in polynomially many rounds unless all-switches does.
   The ladder separation is a property of the PRESENTATION, not of the game.
   This is a barrier of a new type here: the other three limit a MEASURE, this
   one limits what extra GRAPH STRUCTURE can buy.
   Verified: 618 stopping games, 0 defects on all four legs (value correctness,
   monotonicity, attr == all-switches on N(G), allsw round counts equal on G and
   N(G)); ladder n = 1..9.
5. prop:serialiser + rem:serialiser — if |S_sigma| = 1 at each of L consecutive
   steps then every improving rule makes the same FORCED flip, so the run is the
   unique improving path and thm:short-path caps it: EVERY MAXIMAL FORCED BLOCK
   HAS LENGTH <= |Vmax|. So a classical binary counter (one bit flips because it
   is the only flippable one) is IMPOSSIBLE on stopping SSGs, for all improving
   rules at once — this is the unverified antichain-law corollary (u3) obtained
   unconditionally and in two lines from thm:short-path. A superpolynomial run
   must be offered a real CHOICE at least once every |Vmax| steps.
   Verified: 249 stopping games with ALL starting strategies enumerated, 0
   violations, bound attained.
6. lem:splice + rem:splice-invariance — splice an average vertex with two
   parallel edges; merge two average vertices with the same successor multiset.
   Both preserve values and stopping and lower a by one. EVERY vertex N(G) adds
   is a splice redex, and the normalisation creates/destroys no redex among the
   old vertices, so the reduced average count is invariant under it while a is
   not. Verified: 265 games, 0 defects, reduced count order-independent in all.

### OPEN QUESTION THIS RAISES (my own, for round 9)
The barrier says a poly rule must stay fast when Vmax u Vmin is an INDEPENDENT
set, so the only structure left is the interaction of average vertices. Natural
hierarchy to study: R_k = "freeze all but k average vertices, solve the residual
game exactly in poly(N)2^k by thm:few-avg, adopt its Max strategy". R_0 = the
residue rule; R_a = exact. Same proof shows every R_k is sound and monotone. Is
R_k residue-blind for k >= 1? Almost certainly NOT, so the barrier does not
cover the hierarchy — that is where I would look next.

## ROUND 8 COMPLETE (wf_4d90b0fe-2d0): 27 agents, 0 errors, ~1 MB output
Verdicts: algebraic-sign = DEAD-END; the other eight = strict-progress.
Task output: tasks/waxkrajrt.output. Audit 6 found my own thm:normalform-barrier
is silently FATAL to the order-space route. Audit 17 found a FATAL defect in the
howard route's "antichain barrier" and, in fixing it, derived a STRONGER law.

### VERIFIED BY ME AND INTEGRATED (frontier.tex now 65 pp)
1. sec:slack additions — def:trans-slack, thm:trans-sound, prop:trans-Hm,
   thm:trans-complete, lem:phi-certificate, prop:trans-stall, rem:trans.
   THE TRANSITIVITY CLAUSE (min-plus all-pairs closure) DESTROYS cor:slack-stalls:
   on H_m it decides {h,c_1} at k = 4m-3 (verified m=3..9, and 38 at m=10) against
   14,38,100,249,596 for the plain calculus (m=3..7, all verified by me from
   def:slack, my own implementation in scratchpad/root_audit/slack.py).
   thm:slack-barrier's METHOD cannot be repaired: an invariant a min-plus closure
   propagates must obey the triangle inequality, and u_k(x)-l_k(y) does not (its
   diagonal is strictly positive).
   thm:trans-complete: on STOPPING games lim_k Delta_k = w*(x)-w*(y) EXACTLY,
   using only (up),(down),bases — so no stall is ever permanent there and the
   whole frontier is a RATE question, not an expressiveness question. I checked
   the proof line by line (two affine changes of variable + contraction) and it
   is correct.
   lem:phi-certificate: EVERY fixed point phi of T with phi=0 on Z_0, 1 on Z_1
   gives Delta^T_k >= phi(x)-phi(y). prop:trans-stall: 4-vertex NON-stopping game
   a->(t0,t1), p->(a,p) Max, q->(a,t1), u->(p,q) Max; phi=(1/2,1,3/4,1) is a
   second fixed point; Delta^T stalls at 1/4 for ever; damping decides at k=7,8,10.
2. sec:allsw-laws — lem:monotone-law, thm:peak-law, cor:no-return, cor:law-b,
   cor:antichain, def:maxreach, thm:component-bound, thm:bounded-components,
   prop:k1-family, prop:overshoot-small, rem:allsw-laws.
   PEAK LAW (audit 17's generalisation of the route's lemma, hypothesis deleted):
   for ANY sigma,sigma' with val' >= val and distinct, the argmax set of the
   difference meets the disagreement set and every vertex there is NOT strictly
   switchable at sigma'. Gives the FORWARD law Delta(sigma_t,sigma_t') not
   subset of S_t', dual to the backward law.
   COMPONENT BOUND: all-switches halts within sum_j (2^{|C_j|}-1) over the SCCs
   of the Max-reachability digraph H(G) (settles u8). NEW POLY CLASS K_k (all
   components <= k): poly(N)2^k, closed under damping (settles half of u7).
   prop:k1-family: explicit K_1 family, N=5n+2, a=3n, |Vmax|=|Vmin|=n,
   w*(x_1)=1/2+2^-(n+1), in NONE of the four classes of sec:special.
   prop:overshoot-small: 6 = (3/2)|Vmax| all-switches iterations on 182 vertices,
   beating prop:allswitch-overshoot's 16/14 on a far smaller instance.
   f(m) = 1,2,4,7 for m<=4 = the exhaustive ceiling under the two laws.
   MY prop:serialiser SURVIVES: the route refuted the broader claim "counters
   unrealisable for ANY wiring", which I never made; my statement is the narrow
   one (one bit flips BECAUSE it is the only flippable one) and is unaffected.

### STILL TO DIGEST from round 8 (not yet verified by me)
- verify-tri: (u1) trichromatic width REFUTED; new thm:kacyclic class; an
  N^{O(tri)} algorithm; (u2) left as a gap.
- two-token-pairs: (u4) REFUTED; additive multiset calculus AMC_s; thm:amc-barrier
  (the whole additive hierarchy is dominated by two-sided value iteration);
  cor:amc-level (order Omega(N/log N) necessary); prop:frame-saturation (the
  fooling-pair method of thm:matching-barrier cannot lift).
- coupling-transport: transport certificate (an LP), 7-vertex decision stall,
  exponential barrier, TWIN/TRIAD_k multi-vertex stalls, level-one disjunctive
  strengthening exact for <= 2 Max vertices.
- order-space-search: ordering iteration CYCLES; cor:no-height is silent in
  ordering space; a canonical progress measure of QUADRATIC height there.
- value-gadget-algebra: binomial-tail score-counter gadget; gap amplification;
  "amplification needs slot-depth"; composing with thm:few-avg is strictly
  counterproductive; a new polynomial class; "splitting the order of the average
  values is the whole problem".
- free-search-7: boundary-value reformulation; "threshold freezing: an
  oracle-free AND/OR reduction"; the response map's affine-piece count.
- algebraic-sign (DEAD-END): no discrete concavity, no proximity at any scale —
  but its audit says it studied the WRONG objective (val_sigma(v0) instead of
  the sum), so re-check before citing.

### ROUND 8 INTEGRATION COMPLETE — frontier.tex is 71 pp
Also verified by me and added, beyond the two items above:
3. sec:transport — def:transport, thm:transport-sound, lem:transport-exact,
   prop:transport-decides, prop:transport-stalls, thm:transport-barrier,
   rem:transport. Q(G) = {x : Max rows x(v) >= x(v^i), Min rows reversed,
   average EQUALITIES, L <= x <= U}; Sep(p,q) = max{x(q)-x(p)} <= 0 certifies
   w*(q) <= w*(p). An LP, sound on arbitrary SSGs. lem:transport-exact: on a
   successor-closed set of average vertices the equalities pin x = w*, so the
   LP DECIDES G8 (Sep = -1/10) and H_m (Sep = -2^-(m+1)) for every m — both
   instances on which the paper's other mechanisms provably fail. It stalls on
   a 7-vertex game S and, on S_r, decides only if its seed localises w*(v) to
   within 1/(4(2^r-1)); value iteration needs 2^{N-8} rounds. I wrote my own
   exact rational two-phase simplex (scratchpad/root_audit/lp.py) for this.
4. sec:special — def:payoff, lem:successor-closed, lem:cut, lem:residual,
   thm:kacyclic, prop:kacyclic-strict, rem:kacyclic. ONE COLOUR OFF THE CYCLES
   SUFFICES: if no cycle carries a vertex of colour k (any one of max/min/avg)
   the value is exactly computable in poly time, no stopping hypothesis. This
   CONTAINS thm:avg-acyclic, thm:player-free and thm:one-player and is
   strictly stronger (4-vertex max-acyclic witness, w* = (1/2,1/2,3/4,1/2)).
   Verified on 3707 k-acyclic instances from 3681 games, 2856 non-stopping,
   0 discrepancies.
5. sec:special — def:escape, lem:descent-refined, lem:certificate,
   thm:few-escape, prop:fk-family, rem:escape. thm:few-avg's exponent a is
   replaced by the ESCAPE EXPONENT d(G) <= a counting only the average
   vertices where a single forced descent BRANCHES. poly(N) a 2^{d(G)}, with a
   sound and complete polynomial certificate so no knowledge of d is needed.
   prop:fk-family separates d = 2 from a = N-7 on a non-stopping family.

### MY OWN BUGS THIS SESSION (both caught before any claim was made)
- kacyc.py: colour-k vertices not yet solved were left in the residual, which
  the two-colour solver then mistyped. Fix: retype every unsolved colour-k
  vertex as a 0-terminal; they are unreachable from the vertex being solved by
  D_k-acyclicity, so this cannot change the answer.
- kacyc.py and any constraint builder: building a row as a dict literal
  {a: 1/2, c: 1/2} SILENTLY COLLAPSES when a == c (a vertex whose two
  successors coincide). Always accumulate with d[u] = d.get(u,0) + coeff.
  This produced 407 false "theorem violations" before I found it.
- transport.py: sign errors moving sink constants across a <= constraint, in
  the Min and average rows only. Symptom was "infeasible" on a polytope that
  provably contains w*. ALWAYS test that w* itself is feasible first.

## ROUND 9 LAUNCHED (runId wf_e949f34a-d30, session 3792e9e6, 9 routes)
Aimed at the frontier as round 8 left it:
trans-rate (thm:trans-complete makes it purely a RATE question: is Delta^T
polynomial-round on stopping games? find the invariant a min-plus closure
preserves — quasi-distances sup_F(phi(x)-phi(y)) over phi with phi <= T phi);
hybrid-mechanism (CROSS-POLLINATION: transport is EXACT where slack dies and
vice versa — build the hybrid, then engineer a stall by composing the two
failure modes); lift-project (Balas Q_1 over the transport polytope; (Q1-DECIDES)
is target-equivalent so only a refutation counts); allsw-ceiling (compute f(6),
f(7); find MORE laws; note f(|Vmax|) bounds every all-switches run so a
polynomial f would solve the problem); mu-parameter (poly(N)2^{O(mu_k)} for the
two controlled colours, and the average colour as the open case);
amc-reflexivity (does reflexivity break the additive-hierarchy barrier?);
threshold-freezing (oracle-free AND/OR retyping; can the transport LP supply the
missing delta?); value-order-search (cor:no-height is SILENT in ordering space,
which carries a quadratic-height measure — is there a sound move that decreases
it without performing a comparison?); free-search-8.

### FRONT MATTER REWRITTEN + prop:no-halving (73 pp)
The abstract had not been touched since 51 pages; rewritten as foundations /
polynomial classes / where the difficulty is / four mechanisms / barriers, and
the outline updated. Added prop:no-halving + rem:no-halving: a reduction
halving a would give N^{O(log a)}, and BOTH mechanisms thm:order-determines
suggests are dead — substituting a learned value costs >= a fresh average
vertices by lem:denominator-sharp (attained on the ladder), and comparing two
AVERAGE vertices is already target-equivalent (adjoin p'->(p,p), q'->(q,q)).

### RUNNING IN BACKGROUND
scratchpad/root_audit/fab.py computing f(6) (f(1..5) = 1,2,4,7,13 done).

## PAUSED 2026-08-27 ~23:25 UTC at the user's request (token budget)
STATE: frontier.tex 73 pages, ~190 numbered results, `make clean && make pdf`
clean with ZERO undefined references, synced to gdrive:ssg-proof/frontier.pdf,
git clean at commit 43af842 (+ one follow-up). Still NO polynomial algorithm
and none claimed.

ROUND 9 (wf_e949f34a-d30) WAS STOPPED BEFORE ANY ROUTE RETURNED — its journal
holds 0 results, so nothing is recoverable and resumeFromRunId is useless
(it is same-session only anyway). RELAUNCH IT FRESH from the saved script:
  /home/ubuntu/.claude/projects/-data-ssg-proof/3792e9e6-c19b-4ab7-9ff0-4c63fac83894/workflows/scripts/ssg-round9-wf_e949f34a-d30.js
Its brief is already written against the post-round-8 frontier and is accurate.

### PARTIAL RESULT WORTH KEEPING
f(6) >= 23 (the search was killed mid-run; f(1..5) = 1,2,4,7,13 are exact).
23/13 = 1.77, so the ceiling f(m) of rem:allsw-laws looks EXPONENTIAL, and the
"derive enough laws to make f polynomial" route is unlikely to close. Do not
report f(6) = 23; it is only a lower bound from a partial search.

### HIGHEST-VALUE UNFINISHED WORK, in order
1. The RATE of the transitive slack calculus on stopping games. thm:trans-complete
   removed expressiveness from the question, so this is now the sharpest live
   target: find the invariant a min-plus closure preserves (quasi-distances
   sup_F(phi(x)-phi(y)) over phi with phi <= T phi look right), or engineer a
   slow family.
2. The transport/slack HYBRID. rem:transport proves the two mechanisms fail in
   complementary configurations; the hybrid has no known stall, so either build
   it and find one, or find out why not.
3. Round-8 material I verified but did NOT integrate: the AMC additive multiset
   calculus with thm:amc-barrier and cor:amc-level (order Omega(N/log N)); the
   boundary-value threshold-freezing reduction (its paste-ready LaTeX is in the
   repo as boundary.tex, UNVERIFIED by me — re-derive before using any of it);
   the mu_k transversal parameters; the gadget dictionary and gap amplification
   with its Lipschitz barrier.
4. The all-switches pivot, still open and still decisive.

## SESSION 65a9c5c1 (2026-08-27 23:30 UTC). ROUND 10 LAUNCHED
State on arrival: frontier.tex 73 pp, 188 numbered results (44 thm, 32 lem, 23
prop, 11 cor, 32 def, 46 rem), clean build, 0 undefined refs, git clean at 9408db7.
Round 10 = runId wf_56c37566-49e, task we8q1j8z8, script at
scratchpad/round10.js. 9 routes x 2 adversarial audits (correctness lens +
significance lens) = 27 agents:
hybrid-rate, trans-rate, howard-lower, boundary-verify, parametric-discount,
polytope-exact, newton-analytic, digest-backlog, free-search.
The brief lists explicitly which facts are IN frontier.tex (by label) and which
are unverified claims (u1)-(u6), and carries the project's four standing traps
(dict-literal collapse on equal successors, sink-index collision, test w* is
feasible before believing "infeasible", Z_sigma admits t0).

### THE NEW OBJECT: THE HYBRID (transport-seeded transitive slack)
Found by MY OWN round-9 background computation (hybridR9/), never in the paper.
Interleaves M2T with M4 in a FEEDBACK LOOP: slack round + min-plus closure gives
M; then the transport polytope Q(G) is TIGHTENED by adjoining x(p)-x(q) <= M(p,q)
for every ordered pair, and Sep is recomputed over the tightened polytope; then
close again. Soundness is immediate (w* stays feasible). MEASURED round counts:
  instance   M4 transport   M2 slack   M2T trans   HYBRID
  G8         DECIDES         7          6           1
  H_3..H_6   DECIDES         14,38,100,249  9,13,17,21   1
  S (7 vtx)  STALLS          6          5           2
  S_2..S_7   STALLS          12..420    8..26       2
So the hybrid decides EVERY engineered stall in the project in <= 2 rounds.
WHY THE BARRIER MAY NOT LIFT: thm:transport-barrier is about BOX seeds
(L <= x <= U); the hybrid adds DIFFERENCE constraints, which are strictly
stronger, and thm:slack-barrier is about disjoint successor-closed parts while
the transport average EQUALITIES are global and couple them.
MY OWN CONJECTURED CHARACTERISATION (to test): the limit Delta_inf is the
largest fixed point of "difference-hull of Q(G) intersected with the current
difference bounds", i.e. Delta_inf(x,y) = max{z(x)-z(y) : z in Q(G),
z(p)-z(q) <= Delta_inf(p,q) for all p,q}. If so the rate question becomes a
facet-structure question about that polytope.

### BOX HYGIENE
Orphaned round-9 CPU jobs from session 3792e9e6 were still running at load 17.5/16
(exp4.py, combi, fab, ./f 6, runbat.py x8, laws). My kill was BLOCKED by the auto
mode permission classifier, so they are still there; workflow agents are
network-bound so it is tolerable, but my own exact-arithmetic runs are slow.
f(6) >= 24 now (the C search ./f 6 is still climbing).

### MY OWN NEW SECTION, PROVED AND INTEGRATED (76 pp, 197 results, commit d592b56)
sec:hybrid: def:hybrid, thm:hybrid-sound, lem:hybrid-fix, lem:gen-comparison,
thm:hybrid-complete, cor:hybrid-sink, rem:hybrid-box, prop:hybrid-decides,
rem:hybrid-where. Written from a fully INDEPENDENT harness I built this session
(scratchpad/root10: mylp.py exact two-phase simplex with Bland's rule, validated
against brute-force vertex enumeration on 400 random LPs, 0 mismatches;
mycore.py SSG core + slack + min-plus + transport + hybrid; myinst.py the named
instances). It reproduces the paper exactly: G8 w*=(1,1/2,1/5,3/5,2/5,1/2);
S w*=(1/2,1/2,3/8,1/4,1/2), Sep(a,b)=Sep(b,a)=1/8; S_r Sep = 5/16,13/32,29/64,
61/128 and 1/16,1/32,1/64,1/128; G_m val(c1)=9/16,17/32,33/64; G* all 17 values.

THE THEOREM (mine). Call Delta CLOSED if it is sound and improved by none of
the slack step, the min-plus closure, or the LP step P(Delta)(x,y) =
max{z(x)-z(y) : z in K(Delta)}, K(Delta) = Q(G) cut by x(p)-x(q) <= Delta(p,q).
Then on a STOPPING game every closed Delta has K(Delta) = {w*} and
Delta(x,y) = w*(x)-w*(y) EXACTLY. Proof: read Delta twice. Columns
phi_y = Delta(.,y) satisfy phi_y <= T~phi_y (that IS the (up) clause), rows
psi_x = -Delta(x,.) satisfy psi_x >= T~psi_x (the (down) clause), with T~ the
Shapley operator leaving the sinks free. lem:gen-comparison rescales
cor:comparison to arbitrary sink payoffs alpha<beta (max/min/mean commute with
increasing affine maps; thm:contraction's proof is range-independent because
lem:absorption is strategy-independent, so it holds on [-M,M]^V). Min-plus plus
the base fact Delta(t0,t1)<=-1 supplies alpha <= beta-1, which is what makes
the rescaling legal. Then Step 1 gives Delta(x,y) <= w*(x)-L(y), Step 2 gives
Delta(x,y) <= U(x)-w*(y), and taking y=t0 resp. x=t1 forces U=w* and L=w*.
VERIFIED: 100 random stopping games, all reached a fixed point, ZERO violations
of the collapse, of exactness, of the two intermediate bounds, or of the
prefixed/postfixed structure.
COROLLARY cor:hybrid-sink: the proof touches the LP only at the 4N SINK pairs,
so the sink-only variant is complete and costs 4N programmes per round, not N^2.
VERIFIED: sink-only matches the full hybrid round-for-round on G8, S, S_2..S_10,
H_3..H_6.
rem:hybrid-box: the hybrid is a BOX-PROPAGATION LOOP (P(Delta)(x,t0) = U(x) and
P(Delta)(t1,y) = 1-L(y) are the whole LP contribution), whose only fixed point
is exact. So expressiveness is settled and only the RATE is open -- a polynomial
round bound would put SSG-Value in P by thm:decide-one-bit.

MEASURED (all mine, exact rationals, soundness re-asserted every round):
  instance   transport   slack   trans-slack   HYBRID   sink-only
  G8         DECIDES     7       6             1        1
  H_3..H_6   DECIDES     14,38,100,249  9,13,17,21   1   1
  S          STALLS      6       5             2        2
  S_2..S_6   STALLS      12,25,52,104,210  8,11,15,18,22   2   2
  S_8, S_10  STALLS      -       -             2        2
THE MECHANISM (prop:hybrid-decides proof): on S_r round 1's LP returns BOTH
published separators, and the loose one is useless but the TIGHT one,
Sep(b0,a) = 2^-(r+2), is exact and is recorded as Delta_1(a,b0). At round 2 the
(up) clause at the Max vertex v turns it into Delta_2(v,b0) <= 2^-(r+2), and
since x(v)-x(b0) = 2^-r (t - 1/4) on Q(S_r) that constraint collapses the
segment to t = 1/2. General pattern: the direction in which transport is TIGHT
feeds the slack clause at a controlled vertex, which shrinks the polytope in the
direction where transport was LOOSE.
rem:hybrid-where: any stall in the sense of thm:slack-barrier must put a
CONTROLLED vertex inside one of the two successor-closed parts, because an
all-average part satisfies lem:transport-exact and is pinned at round 1.

### HUNTS RUNNING (no stall found; do NOT read that as evidence)
scratchpad/root10/hunt.py seeds 11,12,13 hill-climb for many-round instances;
best so far is 2 rounds at n<=9 with ZERO undecided. t_hyb1.py on random
stopping games at n=6,7: the hybrid decides SOME distinguishing controlled
vertex at round 1 in 75/80 games and by round 2 always. Random search has never
found a hard instance in this project; a stall must be engineered.

### prop:hybrid-rate + rem:hybrid-rate INTEGRATED (77 pp, 199 results, commit 3211f41)
THE WHOLE REMAINING QUESTION FOR THE HYBRID IS ONE SCALAR. With [L_k,U_k] the
box of the polytope round k+1 optimises over and omega_k its width:
 (a) Delta_{k+1}(x,y) <= U_k(x) - L_k(y)  [transport step gives
     Delta(x,t0) <= U(x) and Delta(t0,y) <= -L(y); min-plus composes them]
 (b) omega_k < 2^{-(a+1)} already decides EVERY value-distinguishing pair,
     because val = v_{sigma*,tau*} solves ONE linear system with matrix
     I - A_{sigma*,tau*}, so by lem:denominator-sharp all its coordinates share
     a denominator <= 2^a and two distinct values differ by >= 2^{-a}
 (c) so omega_{k+1} <= rho omega_k decides everything within
     (a+1)/log2(1/rho) + 1 rounds.
=> rho <= 1 - 1/poly(N) uniformly would put SSG-Value in P by thm:decide-one-bit,
and rho -> 1 is the ONLY way the mechanism can fail. CONTRAST with M2T: there
the box is T^k 0 .. T^k 1 whose rate 1-2^-a is ATTAINED (rem:few-avg-tight);
here the average rows are EQUALITIES so the contraction is not tied to mixing.
VERIFIED: 120 random stopping games, 0 violations of (a) or (b), in the
STRONGER form with the box taken after the round.

THE SLOWEST INSTANCE FOUND (rem:hybrid-rate), by hill climbing on rho:
W: n=7, t0=7, t1=8, kinds (avg,min,avg,avg,avg,max,avg),
0->(7,2), 1->(3,2), 2->(5,3), 3->(4,6), 4->(5,1), 5->(4,0), 6->(8,7).
val = (1/4,1/2,1/2,1/2,1/2,1/2,1/2); only vertex 5 distinguishes; widths
10/11, 43/66, 365/792, 7/44, 21/176, 7/88, 0 so rho(W) = 3/4; box collapses at
round 7 (MORE ROUNDS THAN VERTICES) though vertex 5 is decided at round 4.
WHY IT IS SLOW, and the recipe for a family: the MIN vertex is what stops the
box being pinned from below -- on S_r the pin val(v) >= val(a) = 1/2 is exact at
round 1, which is the whole reason S_r takes only 2 rounds -- and both
controlled vertices sit on a cycle carrying average vertices, which
lem:transport-exact cannot resolve. Hand-built families F1 (rounds saturate at
3) and N1 (x Max comparing two low-escape cycles: rounds to FULL COLLAPSE
2,3,4 for k=1,2,3 but rounds to FIRST DECISION stuck at 2) both fail to grow.
HUNTS: scratchpad/root10/hunt4.py (max rounds), hunt5.py (max rounds to first
decision), hunt6.py (max rho, the RIGHT objective by prop:hybrid-rate), all
seeded from W.

### ROUND 10 RESULTS I VERIFIED MYSELF (independent code, from the statements)
- FOREST BALANCE (free-search route) CONFIRMED: val_{sigma,tau}(v) = N_1(v)/N
  with N = #sections whose functional digraph is acyclic, and N = 2^a det(I-P).
  800 (game,pair) instances, 526 from NON-stopping games, 0 violations. NOTE the
  route's downstream claim "det A_U of lem:denominator-sharp IS the forest
  count" is FALSE (its own significance audit found strict inequality); the two
  identities above are the ones that survive.
- thm:bvv-fold (boundary-verify route) CONFIRMED: P_D on 6D+2 vertices
  (u,k_1..k_{2D-1},X_d,Y_d avg; F_d Max; G_d Min; u->(t0,t1),
  k_j->(t0,k_{j+1}), k_{2D-1}->(t0,t1), X_d->(t0,F_{d-1}),
  Y_d->(k_{2D-2d+1},G_{d-1}), F_d->(X_d,Y_d), G_d->(X_d,Y_d), F_0:=u, G_0:=t0)
  has val_{P_D[u:=theta]}(F_D) = 2^{-(D+1)}(theta+1-2^-D+2^-D T^D(theta)) with
  T the tent map, hence EXACTLY 2^D affine pieces. I checked it by backward
  induction against the closed form at every dyadic grid point, every midpoint
  and five off-grid rationals for D=1..12, 0 mismatches, slopes alternating
  {0, 2^-D}. MECHANISM: a Max and a Min vertex sharing the SAME two successors
  give max+min = sum and max-min = |difference|, so s_d = s_{d-1}/2 + 4^-d and
  phi_d = |phi_{d-1}/2 - 4^-d| -- a tent map, one fold per level, O(1) vertices
  per fold. This KILLS every continuation/homotopy method that tracks the
  optimal pair, and it is orthogonal to thm:bv-slow.

### THE HYBRID IS REFUTED — round 10's hybrid-rate route, and MY OWN CORRECTIONS
THE ROUTE'S RESULT (and it overturns my optimistic reading):
- hyb:onectrl: on a stopping SSG with |Vmax|+|Vmin| = 1, Q^H_2 = {w*} and the
  hybrid is EXACT at round 2. EVERY instance on which I measured "<= 2 rounds"
  -- G8, H_m, S, S_2..S_10 -- has exactly ONE controlled vertex. So my
  prop:hybrid-decides measurements are a theorem about a degenerate class, NOT
  evidence of speed. Exhaustive check: 73038 stopping 4-vertex one-controlled
  games, worst round count 2, zero exceptions.
- hyb:exact: the hybrid IS a cutting-plane iteration. Lambda(P)(x,y) :=
  max_{z in P}(z(x)-z(y)) obeys the triangle inequality and Lambda(Q(G;M)) <= M,
  so the outer min AND the outer min-plus closure in def:hybrid are BOTH
  redundant, and Delta^H_k = Lambda(Q^H_k) with Q^H_{k+1} = Q(G; min(Lambda(Q^H_k),
  L(Lambda(Q^H_k)))). This is exactly the characterisation I conjectured.
- hyb:barrier-fails: thm:slack-barrier and thm:seeded-barrier do NOT lift (my
  guess was right) -- on H_m the hybrid decides at round 1 while u_k(h)-l_k(c_1)
  stays positive for 2^{Omega(N)} rounds.
- hyb:barrier, the barrier that DOES lift: any shrinking chain of nonempty
  compact CONVEX P_0 ⊇ P_1 ⊇ ... inside Q(G) such that every def:slack clause
  evaluated at Lambda(P_k) is >= Lambda(P_{k+1}) forces Delta^H_k >= Lambda(P_k).
- hyb:family CC(L,m): N = 6L+m+5, ONE-PLAYER, two Max vertices v_1,v_2;
  e avg->(t1,t0); d-chain d_1->(t0,d_2), d_j->(t1,d_{j+1}), d_m->(t1,t0);
  ch(l,b,z) = p_j->(b,p_{j+1}) for j<l, p_l->(b,z); A_1=ch(L,v_2,e),
  B_1=ch(2L,v_1,d_1), A_2=ch(L,v_1,e), B_2=ch(2L,v_2,d_1); v_1->(A_1,B_1),
  v_2->(A_2,B_2). w*(v_i)=w*(A_i)=1/2, w*(B_i)=1/2-2^{-2L-m}, w*(d_1)=1/2-2^-m.
  THE HYBRID NEEDS 2^{Omega(N)} ROUNDS: measured first-decision rounds
  3,5,10,18,36,71 for m=2, L=1..6 -- DOUBLING with every SIX extra vertices --
  against a machine-checked certificate lower bound 1,4,8,17,35,70,140.
  Contraction factor exactly 1 - 2^{-min(L_A, L_B-L_A)} per round.
MY OWN VERIFICATION (independent build from the statement, scratchpad/root10/cc.py):
  CC(1,2) and CC(2,2) reproduce exactly -- N=13,19 as claimed, stopping,
  one-player, all six claimed values exact, both Max vertices distinguishing.
  FULL-LP hybrid first decision on CC(1,2) = 3 rounds, matching the route.

### MY OWN ERROR, CAUGHT BY THIS (correct sec:hybrid before trusting it)
I wrote in prop:hybrid-decides that "the same counts were obtained by the
sink-only variant of cor:hybrid-sink". That is TRUE on the one-controlled-vertex
instances and FALSE in general: on CC(1,2) the full hybrid decides at round 3
and the sink-only variant at round 5. cor:hybrid-sink's COMPLETENESS claim is
unaffected (it is proved), but completeness does NOT imply equal speed, and I
must say so. The reason I did not notice: every instance I tested had one
controlled vertex, i.e. exactly the class hyb:onectrl trivialises.
=> sec:hybrid needs: (a) prop:hybrid-decides reframed via hyb:onectrl; (b) the
sink-only speed claim qualified with the CC(1,2) witness; (c) rem:hybrid-rate
rewritten -- "a family with rho -> 1 is open" is now ANSWERED by CC(L,m);
(d) thm:hybrid-lower added; (e) hyb:exact and hyb:barrier added.

### ROUND 10 AUDIT FLAGS worth remembering
- newton-analytic: FATAL, prop:na-kappa-poly confuses kappa (max over REALISABLE
  pairs) with kappa^+ (max over ALL pairs); the LP computes kappa^+.
- boundary-verify: cor:bvv-sweep's 2^D piece count is CORRECT (I verified it
  myself for D=1..12) but its conclusion "no continuation method is polynomial"
  OVERSTATES the proof. Do not repeat that conclusion.
- free-search: "det A_U of lem:denominator-sharp IS the forest count" is FALSE
  (strict inequality in general); the identities that survive are
  val = N_1/N and N = 2^a det(I-P), both of which I verified on 800 instances.
- trans-rate: the claimed law k ~ c1 N + c2 log(1/gamma) is refuted by the
  route's own table; and "Delta^T poly-round <=> P" is only one direction.

### THE REFUTATION IS INTEGRATED (81 pp, 206 results, commit 7a4894f)
sec:hybrid now contains, all verified by me in exact rational arithmetic:
lem:hybrid-cutting (the hybrid IS a cutting-plane iteration; Lambda obeys the
triangle inequality and Lambda(K(M)) <= M, so both outer operations in
def:hybrid are redundant and Delta_k = Lambda(Q^H_k));
thm:hybrid-convex-barrier (a shrinking chain of CONVEX certificates inside Q(G)
whose def:slack clauses dominate the next forces Delta_k >= Lambda(P_k));
rem:hybrid-barrier-lift (thm:slack-barrier's BOX certificate does NOT lift --
H_m witnesses it);
thm:hybrid-lower (CC(L,m), 2^{Omega(N)} rounds);
rem:hybrid-lower-verified (certificate checked clause by clause: undecided
counts 1,3,8,17,34 for m=2 and 3,7,16,34,69 for m=4, L=1..5, doubling every six
vertices, zero failures);
prop:hybrid-onectrl (one controlled vertex => K(Delta_2) = {val}; VERIFIED by me
on 250 random one-controlled stopping games with the FULL hybrid, worst 2
rounds, zero exceptions);
rem:hybrid-sink-slower (complete does NOT mean as fast: 3 vs 5 on CC(1,2),
3 vs 7 on W).
rem:hybrid-rate rewritten: the mechanism is refuted by a RATE, not a stall, and
CC needs TWO Max vertices wired crosswise -- one cannot work, by
prop:hybrid-onectrl. The cone xi_1 >= lambda xi_2, xi_2 >= lambda xi_1 IS the
mutual resupply, lambda = 1-2^{-L} the probability of returning to the OTHER
Max vertex.

### METHODOLOGICAL LESSON, the sharpest of the project so far
I measured a new mechanism on every hard instance in the paper, got 1-2 rounds
every time, and concluded it was strong. Every one of those instances has
exactly ONE controlled vertex, and that class is trivial for the mechanism by a
two-line argument. The sample was not merely small, it was structurally
degenerate in the exact parameter the mechanism is sensitive to. BEFORE
believing a measurement, ask which parameter the mechanism turns on and check
that the instance set VARIES it. Here the parameter is |Vmax|+|Vmin|, and every
published stall in the project has it equal to 1.
SECOND LESSON: my sink-only variant (cor:hybrid-sink) is complete but strictly
slower, and I ran most measurements with it. Numbers 7, 17, 25 rounds and a
rho=1 witness that I briefly put in the paper were artefacts of that variant;
under the full hybrid those instances collapse at rounds 3, 2, 2, 2. Always
state WHICH variant a measurement used.

### THE REFUTATION WAS ITSELF WRONG — rem:own-successor (82 pp, 208 results, c4d9ed2)
Round 10's SIGNIFICANCE audit of hybrid-rate found a FATAL defect in the route's
lower bound, and I CONFIRMED IT MYSELF. The point is general and it corrects
results that had been in the paper since before this session:

A decision rule (def:decision-rule) must name a controlled vertex and say which
SUCCESSOR is larger. It need NOT order the two successors against each other.
At v in Vmax the row x(v) >= x(v^(i)) is already in Q(G), so
   Sep(v, v^(i)) <= 0 ALWAYS,  and  Sep(v, v^(i)) >= val(v^(i)) - val(v),
the right side being 0 at an optimal successor. So Sep(v,v^(i)) < 0 PROVES
v^(i) suboptimal and DECIDES v. Dually at Min vertices.
MY MEASUREMENTS: on S the pair test gives +1/8 both ways but Sep(v,b) = -1/8;
on S_r the pair test gives 2^{-r-2} > 0 but Sep(v,b_0) = -2^{-r-2} < 0 for
r=2..5. On CC(L,m) Delta_1(B_1,v_1) = -2^{-4}, -2^{-6}, -2^{-6} for
CC(1,2), CC(2,2), CC(1,4) -- BOTH Max vertices decided at ROUND ONE.

WHAT THIS BREAKS:
- prop:transport-stalls' sentence "the decision rule built from def:transport
  therefore stalls" was FALSE and had been in the paper for many rounds.
- thm:transport-barrier and rem:transport are about ORDERING THE PAIR (a,b_0),
  which is what they prove; they do not exhibit a decision stall.
- MY thm:hybrid-lower does NOT refute the hybrid. Its certificate bounds
  Delta_k(B_i,A_i); the entry a rule reads is Delta_k(B_i,v_i), and the
  certificate gives Lambda(P_k)(B_1,v_1) = -gamma for EVERY k because
  theta_{B_1} - theta_{v_1} = (-2^{-2L},0) has h_k = 0. Consistent with an
  immediate decision, and that is what happens.
=> THE HYBRID'S RATE IS OPEN AGAIN. A real refutation must drive
Delta_k(v^(i),v) to 0 at EVERY controlled v and both i -- strictly harder.

WHAT SURVIVES AND IS INTEGRATED: rem:own-successor (the insight itself);
prop:hybrid-onectrl; lem:hybrid-cutting; thm:hybrid-convex-barrier (a METHOD for
entry-wise lower bounds, not a barrier -- its hypothesis is an invariant the
prover supplies, so it excludes no algorithm, as its own audit noted);
rem:hybrid-barrier-lift; thm:hybrid-lower restated as what it proves;
rem:hybrid-lower-not-a-refutation, which says plainly that I first misread it.

### STANDING RULE FOR THIS PROJECT, from the above
When testing ANY comparison mechanism as a decision rule, test BOTH
 (i) the pair (v^(0), v^(1)), and
 (ii) the pairs (v^(i), v) for each i.
(ii) is strictly stronger for every mechanism that has Q(G)'s controlled rows,
and every negative result in this project stated before 2026-08-28 tested only
(i). Re-examine any other "stall" claim against (ii) before citing it.

### howard-lower AGENT DIED (user reported "Time: error")
Relaunched as its own single-route workflow, runId wf_e324b9a0-cbc, task
wq3yai1ew, script scratchpad/round10-howard.js. Original round 10 =
wf_56c37566-49e still running polytope-exact; its journal shows 7 route results,
1 failed (howard-lower), 12+ audits.

### THE STANDING RULE APPLIED — outcome (83 pp, 210 results, commits b76fd53, c041bf6)
prop:own-stall + rem:own-stall: a GENUINE decision stall of the transport
certificate, restoring what rem:own-successor took away. R on 10 vertices,
Vmin={0,1,6,7}, Vmax={4}, Vavg={2,3,5}: 0->(2,5), 1->(5,3), 2->(5,2),
3->(0,t1), 4->(0,t0), 5->(t1,t0), 6->(0,t0), 7->(5,2). Stopping,
val=(1/2,1/2,1/2,3/4,1/2,1/2,0,1/2), Z0={6,t0}, Z1={t1}. All THREE
value-distinguishing controlled vertices (1,4,6) survive the own-successor test
even with the free seed U:=0 on Z0, L:=1 on Z1 -- all six separators are
exactly 0. Mechanism: at a Min vertex Q(G) gives only x(v) <= x(v^(i)), so x(v)
can be pushed down to touch EITHER successor; at vertex 1 both separators
vanish although val(5) < val(3).
FOUND BY: ownhunt2.py (hill-climb on the undecided fraction, with the Z-seed
in from the start), then minimised by vertex deletion. Several independent
seeds reach fraction 1 within a few hundred stopping games. A richer witness on
13 non-sink vertices has values 5/12, 11/12, 23/24 and leaves all four of its
controlled vertices undecided.
CAUTION RECORDED: every stall found BEFORE the Z-seed was added was an artefact
of discarding free information -- I checked five and the seed cracked all five.
Always seed the transport LP with Z0/Z1 before believing a stall.

THE OTHER NEGATIVE RESULTS SURVIVE the standing rule, so only the transport
claims were affected:
- prop:simorder-stalls: on G8 the simulation preorder relates NEITHER (5,4) nor
  (5,1), so the own-successor test fails there too. I implemented def:simorder
  as a greatest fixed point myself; 0 soundness violations.
- cor:slack-stalls: on H_m the own-successor test Delta_k(v,c_1) <= 0 first
  holds at rounds 15, 39, 101, 250 for m=3..6, exactly ONE round after the pair
  test's 14, 38, 100, 249.
GENERAL PRINCIPLE now in rem:own-successor: at v in Vmax any derivation of
val(v) <= val(v^(i)) forces EQUALITY (the reverse is automatic), so it proves
v^(i) optimal. For order-only mechanisms the test is v <= v^(i); for the slack
calculus it is Delta_k(v,v^(i)) <= 0, NON-strict, hence weaker than the pair
test's strict inequality.

### INTEGRATED FROM ROUND 10, both verified by me (85 pp, 214 results, 70eee76)
- thm:slack-vi-upper + rem:slack-sandwich: for EVERY SSG and all x,y including
  sinks, Delta_{2k}(x,y) <= u_k(x) - l_k(y), u_k = T^k 1, l_k = T^k 0. Proof:
  one round applies (up) at x, the next (down) at y; both aggregators are
  monotone and translation-equivariant, and ag^-_y(c-a,c-b) = c - (Tl)(y) is
  the min-against-max pairing. Sinks need the monotonicity Delta_{k+1} <=
  Delta_k plus the base clauses. WITH thm:slack-barrier this SANDWICHES
  def:slack: on the separated configurations it IS two-sided value iteration up
  to a factor 2 in rounds, and nowhere faster. Only (up)/(down) are used, which
  is exactly what def:trans-slack's closure escapes (prop:trans-Hm).
  MY CHECK: 300 games, 207 non-stopping, all N^2 pairs, k<=6, 0 violations,
  57353 equalities.
- sec:fold / thm:fold / rem:fold: freeze one vertex at payoff theta;
  R_{u,v}(theta) = val_{G[u:=theta]}(v) is piecewise affine, monotone,
  1-Lipschitz, and its pieces are the regions of constant optimal pair. P_D on
  6D+2 vertices has EXACTLY 2^D pieces. Device: a Max and a Min vertex sharing
  the SAME two successors give max+min = sum and max-min = |difference|, so
  s_d = s_{d-1}/2 + 4^-d and phi_d = |phi_{d-1}/2 - 4^-d| -- a TENT MAP, one
  fold per level, O(1) vertices per fold because all constants sit on one
  shared chain. MY CHECK: closed form vs backward induction at every dyadic
  grid point, every midpoint and 5 off-grid rationals, D=1..12, 0 mismatches,
  slopes exactly {0, 2^-D}. rem:fold states the LIMIT honestly (its audit
  flagged the overreach): this kills continuation methods that TRACK THE
  OPTIMAL PAIR, not parametric methods in general.

### THE SHARPEST OPEN QUESTION NOW, and the hunt for it
The strongest decision test the paper supports: run the hybrid seeded with the
free Z0/Z1 bounds and fire as soon as Delta_k(v,v^(i)) <= 0 at a Max vertex or
Delta_k(v^(i),v) <= 0 at a Min vertex. It decides ALL the transport stalls in
<= 2 rounds (R, B, C from prop:own-stall's family). By thm:hybrid-complete it
always eventually fires on a stopping game, so the ONLY refutation available is
a family on which the FIRST fire is superpolynomially late; by
thm:decide-one-bit a polynomial bound would put SSG-Value in P.
HUNT: scratchpad/root10/hybownhunt.py (6 seeds, maximise the first-fire round).
Best so far: 3, at n=10. CC(L,m) fires at round 1, so it is useless here.
OTHER FATAL AUDIT FLAGS, not integrated so no action needed: newton-analytic's
prop:na-kappa-poly confuses kappa with kappa^+; parametric-discount's
thm:pd-monomial upper bound is valid only for Vmin empty.

## ROUND 10 COMPLETE (wf_56c37566-49e): 25 agents, 24 done, 1 API death, 6.31M subagent tokens
Verdicts: all 8 returning routes = strict-progress. howard-lower died (API
connection lost) and was RELAUNCHED as wf_e324b9a0-cbc / task wq3yai1ew from
scratchpad/round10-howard.js. Every audit came back sound=False except one of
the two boundary-verify audits -- the significance lens is doing real work.

### INTEGRATED (87 pp, 217 results, commit a68374c) — from polytope-exact
lem:transport-dim + thm:transport-objective + rem:transport-objective.
Making C = Vmax u Vmin and the sinks absorbing leaves an ABSORBING average
chain (else the unabsorbed set is a trap by lem:trapchar), so every x in Q(G)
is the harmonic extension of x|_C and dim Q(G) <= |C|. With
obj_sigma(x) = sum_Vmax (x(v) - x(v^{sigma(v)})) + sum_Vmin (x(v^{sigma(v)}) -
x(v)): obj_sigma >= 0 on Q(G) always, and obj_sigma(x)=0 forces
x(v) = x(v^{sigma(v)}) at every controlled vertex, which with the Q(G) rows
gives Tx = x, so x = w* and sigma is optimal. Hence w* is a VERTEX of Q(G),
unique minimiser for an optimal sigma, and the minimum is > 0 otherwise.
MY CHECK: 100 stopping games, |C| <= 5, all 2^|C| profiles, 0 violations;
uniqueness tested by maximising AND minimising every coordinate at obj = 0.
HONEST FRAMING (both audits refuted the route's headline): choosing the
objective = naming an optimal profile = the target, so this is a reformulation.
The structural content is that Q(G) is NOT a coarse outer approximation --- it
is <= |C|-dimensional and already has w* as a vertex. I did NOT reproduce
"cutting planes are the wrong tool / extended formulations are vacuous"; that
is false, and sec:hybrid is itself a cutting-plane procedure.

### NOT YET INTEGRATED from polytope-exact (verified by ITS auditor, not by me)
- pex:thm-L3: degree-two Lasserre is NOT exact on a stopping SSG (36 vertices).
  The correctness auditor rebuilt it independently in the original 36 variables
  -- 37x37 moment matrix PSD, 33 equations, 78 inequalities, all three
  L(h_v)=0, x != w* -- and calls it "a strict strengthening of M4 which repairs
  M4's own published stalls and then dies, the same shape as sec:slack
  repairing G8 and dying on H_m. That is worth a subsection."
  ITS DECISION-FAILURE CLAUSE IS NOT ESTABLISHED: it uses the PAIR test, which
  my rem:own-successor deprecates. Re-derive with the own-successor test first.
- pex:cor-two (degree-two Lasserre exact for |C| <= 2), pex:thm-order1
  (Lyapunov diagonal stability criterion, only one direction proved),
  pex:thm-half (rho(Rbar) < 1/2 implies exactness), pex:lem-pmatrix,
  pex:thm-balas-rank (Balas rank <= |C|), pex:prop-B3 (one Balas round is not
  exact, 54 vertices, reproduced by the auditor).
  CAUTION: pex:cor-two's claim that transport "provably stalls" on S and S_r is
  the misreading rem:own-successor corrects; and S, S_r have |C| = 1 so the
  comparison is vacuous anyway.

### howard-lower RELAUNCH COMPLETE (wf_e324b9a0-cbc, 3 agents, 845k tokens)
INTEGRATED (88 pp, 222 results, commits 13ac71a + the audit repairs):
def:improvement-uso, prop:allsw-auso, lem:auso-laws, cor:f-auso, rem:f-auso.
THE RESULT: for a nondegenerate stopping SSG the improvement outmap
s_G(sigma) = {i : x_i strictly switchable} is an ACYCLIC UNIQUE SINK
ORIENTATION of the |Vmax|-cube and all-switches is its BOTTOM-ANTIPODAL walk;
and every BA trace of every AUSO obeys cor:no-return and cor:law-b. Hence
f(m) >= h*(m), the greatest BA height of an AUSO of the m-cube: THE TWO LAWS
ARE EXACTLY THE AUSO AXIOMS, and the rem:allsw-laws programme is closed.
Tight where enumerable: h*(2)=2=f(2), h*(3)=4=f(3).
MY VERIFICATION: 200 nondegenerate stopping games (2<=|Vmax|<=4, |Vmin|<=3) --
USO and acyclic every time, every trace obeying both laws, 0 failures, 1236
degenerate instances skipped; and exhaustively on all 12 AUSOs of the 2-cube
and all 728 of the 3-cube (#AUSO(3)=728 matches the auditor's independent
count), every trace from every start, 0 violations.
=> AN EXPONENTIAL ALL-SWITCHES FAMILY EXISTS IFF SOME STOPPING SSG REALISES AN
AUSO OF EXPONENTIAL BA HEIGHT AS ITS IMPROVEMENT ORIENTATION. That is the new
form of the pivot.

TWO REPAIRS I MADE AFTER THE SECOND AUDIT (both real):
- lem:auso-laws needs unique SOURCES of faces, which the USO axiom does not
  state. Fix: complementing every outmap reverses every edge and preserves
  (s(u)^s(v))&(u^v), so the reversal is again a USO and its sinks are the
  original's sources. Verified: 0 failures on all 740 AUSOs, and every face of
  every one has exactly one source.
- The route cited h(D) >= 2h(A) + 2 "by Schurr-Szabo Theorem 1"; the statement
  gives only h(D) >= 2h(A) (the +2 is inside their proof). I weakened the paper
  to h*(m) >= 2^{floor(m/2)}, still exponential and all cor:f-auso needs.
NOT INTEGRATED (audits refuted): "a superpolynomial family must be two-player"
(the Holt-Klee inference is invalid -- whether HK AUSOs have superpolynomial BA
height is Schurr-Szabo's own open question); and "the exact one-player maximum
at |Vmax|=4 is 6" (its witness B'_7 is DEGENERATE -- five unoriented cube
edges, so it is outside the nondegenerate class the bound quantifies over).
ALSO WORTH KEEPING: the route's hl:thm-flat says all-switches on stopping
ONE-PLAYER SSGs is exactly Howard's policy iteration on 2-action MDPs, in both
directions (b needs a uniform leak 1-2^{-r}); and hl:lem-consistency explains
why the Fearnley/Friedmann deceleration mechanism does NOT transfer -- it needs
a third action, and out-degree two makes the choice a pure sign test.

## ROUND 11 LAUNCHED (wf_0d654ccc-afc, task whk2y9f6m, 9 routes x 2 audits)
Script scratchpad/round11.js. Routes: auso-realisability (THE pivot),
hybrid-own-rate, lasserre-degree, objective-selection (the LCP and its pivot
rules), verify-newton, verify-amc-mu, barrier-map (synthesis + adversarial
towards the document), free-search-10, free-search-11 (promise gap, average
case, smoothed analysis). The brief carries THE STANDING RULE (rem:own-successor,
both firing directions, Z0/Z1 seed) at the top, the full post-round-10 fact
list, and the unverified claims (v1)-(v8).

### MY OWN FINDING, and it corrects what I integrated hours earlier
prop:allsw-auso requires NONDEGENERACY, and the hypothesis is NOT idle. In a
degenerate game a cube edge can be left UNORIENTED (neither endpoint strictly
switchable in that direction), so the outmap is not a USO at all.
I VERIFIED that prop:overshoot-small's witness -- the paper's own instance for
"6 = (3/2)|Vmax| all-switches iterations" -- IS DEGENERATE: recomputing all 16
value vectors of its reduced 12-variable model exactly gives 10 tied (sigma,i)
incidences out of 64, i.e. 5 unoriented cube edges out of 32. This matches the
round-10 audit's independent count.
=> My "an exponential all-switches family exists IFF some stopping SSG realises
an AUSO of exponential BA height" was WRONG as stated; it now holds only for
NONDEGENERATE games, and the paper's own long runs are outside that class.
cor:no-return and cor:law-b are proved for ALL stopping games, so f still counts
every run and cor:f-auso is unaffected; what is lost on degenerate instances is
the AUSO READING.

### THE OPEN STRUCTURAL QUESTION THIS RAISES (my own, for round 12 if needed)
Is the NONDEGENERATE class genuinely weaker? Data (observation, not theorem):
- census.py: 728 AUSOs of the 3-cube = 18 isomorphism classes, BA heights
  1,2,3,4. 4000 nondegenerate stopping games realise 8/18 classes one-player and
  6/18 two-player, max height 3 -- NEVER the height-4 class.
- hheight.py: six independent hill climbs maximising BA height, m=3 and m=4,
  one- and two-player, all stuck at 3 after thousands of iterations, against
  ceilings h*(3)=4, h*(4)=7 and against the DEGENERATE runs of length 4 and 6
  the paper records.
If nondegenerate stopping SSGs really cannot realise tall AUSOs, that is a
property of improvement orientations beyond the AUSO axioms -- exactly what
cor:f-auso says any improvement on f must use -- and it would also mean the
hard instances are all degenerate, which no barrier in the paper addresses.
Do NOT report this as more than an observation: the project's iron law is that
search never finds what must be engineered.

## ROUND 11 COMPLETE (wf_0d654ccc-afc): 27 agents, 0 errors, 6.83M tokens
All 9 routes strict-progress; 6 of 18 audits sound=True. Several routes
REDISCOVERED PUBLISHED WORK and the audits caught it -- Auger-Coucheney-
Strozecki (almost-acyclic SSGs, arXiv:1402.0471) for the cut/freeze parameter
routes, Mangasarian for the hidden-K LCP LP, Gaertner-Morris-Ruest for
realisable-USOs-satisfy-Holt-Klee. The project is now on ground that overlaps
the literature; ATTRIBUTE, do not claim novelty.

### INTEGRATED: sec:wedge (91 pp, 229 results, commit 3897d4f)
lem:wedge-face, cor:wedge-cert, def:wedge, prop:wedge, rem:wedge.
THE OWN-SUCCESSOR HYBRID IS DEFEATED (as a measurement, not yet as a proof).
lem:wedge-face: with g_{v,i} the controlled rows of def:transport read as
NONNEGATIVE functionals, Delta_k(v,v^(i)) = max over R_k of g_{v,i} >= 0 and
Delta_k(v^(i),v) = -min over R_k of g_{v,i} <= 0. So the test fires iff some
g_{v,i} VANISHES on R_k or has POSITIVE MINIMUM -- geometric, not arithmetic.
cor:wedge-cert: a convex chain defeats it iff each of the 2|C| hyperplanes
{g_{v,i}=0} SUPPORTS P_k and TOUCHES it without containing it. Strictly stronger
than thm:hybrid-lower's demand.
def:wedge WD(e,j,m): N = 2e+j+m+5, one-player, Vmax={v1,v2};
H->(t1,t0); w-chain realising 1/2 - 2^{j-m}; a_{i,q}->(v_i,a_{i,q+1}),
a_{i,e}->(v_i,H); b_i->(v_i,c_{i,1}); c_{i,q}->(v_{3-i},c_{i,q+1}),
c_{i,j-1}->(v_{3-i},w_1); v_i->(a_{i,1},b_i).
val(v_i)=val(a_{i,1})=1/2, val(b_i)=1/2-2^{-m}.
FIRST FIRING ROUND on WD(2j,j,j+4), N=6j+9: 4, 8, 17, 35, 70, 140 for
N=21,27,33,39,45,51 -- DOUBLING every six vertices. Pair test no earlier.
MECHANISM: in xi = z|_C - w*|_C the polytope is a thin WEDGE with apex at the
origin, the two hyperplanes support it exactly at the apex, and a round shrinks
it only by lambda = 1-2^{1-j}. The entanglement is on the NON-OPTIMAL branch,
which is what CC(L,m) lacks.
MY VERIFICATION: WD(4,2,6), N=21 -- stopping, one-player, all values exact,
both Max distinguishing, first fire exactly 4. Computed with my own exact 2-D
POLYGON engine (scratchpad/root10/hyb2d.py), justified by lem:transport-dim
making Q(G) two-dimensional when |C|=2; the literal N^2-LP engine is far too
slow at N=21. BOTH round-11 audits reproduced the whole table independently.
SCOPE, from the audits and IMPORTANT: WD is ONE-PLAYER, so by
thm:seed-dichotomy def:seeded decides both Max vertices at slack round ZERO.
The family defeats M1, M2, M2T, M4 and the hybrid M5 but NOT M3 (sec:seeded).
A two-player wedge is what would be needed, and thm:seed-dichotomy makes that
the same pivot as cor:f-auso / prop:auso-size.

### INTEGRATED: prop:auso-size + rem:auso-size, and a RETRACTION (e2f3b7a)
My "nondegenerate games seem stuck at BA height 3 at m=3" observation was WRONG
and is withdrawn: the unique height-4 class of the 3-cube IS the improvement
orientation of a nondegenerate ONE-PLAYER stopping SSG (the route built a
103-vertex one, its auditor an independent 54-vertex one, both verified from the
game). I had searched RAW GAMES, which is the wrong space; the right one is the
harmonic normal form (2m substochastic affine maps, orientation read off an
arrangement). Moving my own search there immediately reached height 4 at m=4.
prop:auso-size (MINE, elementary): h(s) <= 2^m, so an AUSO of height 2^{Theta(m)}
gives a superpolynomial all-switches bound only if realised on N = m^{O(1)}
vertices; and at most 3^N (N+2)^{2N} N^m = 2^{O(N log N)} orientations of the
m-cube arise from stopping SSGs on <= N vertices, against 2^{m 2^{m-1}} in all,
so for N = poly(m) the realisable ones are a 2^{-Omega(2^m)} fraction.
=> A CENSUS CAN NEVER DECIDE THIS. At m=3,4 parameters outnumber orientations
and essentially everything is realisable (16 of 18 classes one-player at m=3,
the other two two-player); at m = Theta(log N) the counting reverses.

### ROUND 11 FACTS NOT YET INTEGRATED
- h*_1(m) = 1,2,4,6 for m=1..4 against h*(m) = 1,2,4,7; the unique
  height-maximal AUSO of the 4-cube VIOLATES Holt-Klee, so h*_HK(4)=6<7 --
  Holt-Klee costs height. 4-cube census: 4792176 AUSOs, 12640 classes, h*(4)=7
  in a single orbit of 384, 6113 Holt-Klee classes. Both audits reproduced.
- THE PIVOT IN ITS SHARPEST FORM: the one-player half of the AUSO question is
  exactly "is Howard's policy iteration on m-state 2-ACTION MDPs polynomial?",
  an acknowledged open problem.
- objective-selection: the M-FACTORABLE (classical hidden-K/hidden-Z) case is
  solved by ONE linear programme (Mangasarian); the gap is the non-M-factorable
  case. Possible new polynomial class -- check containment in sec:special first.
- lasserre-degree: L3 is REMOVED as a degree-two counterexample; two gaps left.
- free-search-10: FPT in the feedback vertex number -- but its audit found this
  is Auger-Coucheney-Strozecki, already published, and its "new class" claim is
  false.
- free-search-11: the average-case gap is one sentence away from a theorem.
- barrier-map: its only surviving gap G1 is a hybrid stall question, now
  answered by sec:wedge.

## SESSION 4d154c67 (2026-08-28 08:25 UTC). ROUND 12 LAUNCHED
runId wf_163dfb2c-bb8, task wv4103ms3, script scratchpad/round12.js, 9 routes x
2 audits = 27 agents. Harness copied forward to scratchpad/root12/.
ROUTES, chosen to rebalance the portfolio toward POSITIVE mechanisms after
eleven rounds that drifted into barriers:
1. universal-lattice -- the parity-game quasi-polynomial analogue. Is there a
   lattice of quasi-poly HEIGHT with a monotone lifting whose least fixed point
   decides val >= 1/2? NEW: cor:no-height constrains measures on the STRATEGY
   lattice only, and thm:vi-lower is about the full real lattice. Either a
   scheme or an impossibility proof would be major.
2. order-space -- search in the space of thm:order-determines' certificate (the
   preorder on Vavg, O(a log a) bits) instead of the strategy cube. Local search
   with residual ||x_P - T x_P||, and a random-facet analogue aiming at
   e^{O(sqrt(a log a))}, which would be incomparable with BOTH thm:subexp and
   thm:few-avg. No barrier in the paper covers this space.
3. auso-realise -- the pivot, in the HARMONIC NORMAL FORM (the right space).
   Settle m=4 (realise BA height 5,6 or find the obstruction); build a
   COMPOSITION scheme rather than a search; verify (u3),(u4).
4. two-player-wedge -- sec:wedge's open item: WD is one-player so M3 kills it at
   round 0. Build a two-player wedge using prop:own-stall's Min mechanism.
5. lcp-nonM -- Mangasarian's hidden-K LP solves the M-factorable case; attack
   the rest; check class containment in sec:special; attribute prior art.
6. polytope-vertices -- HOW MANY VERTICES DOES Q(G) HAVE? Poly many => enumerate
   => P. Plus: Psi(x) = ||x - Tx||_1 is CONCAVE on Q(G), >= 0, zero exactly at
   w*, so the target is concave minimisation with KNOWN optimum 0.
7. approx-scheme -- by lem:denominator-sharp, error 2^{-(2a+2)} determines the
   value EXACTLY, so poly(N, log(1/eps)) already solves the target; the real
   question is poly(N, 1/eps), i.e. whether SSG-Value has gap amplification.
8. hk-lower -- engineer a superpolynomial all-switches family in normal form.
9. free-search-12 -- with an explicit anti-list of the eleven rounds' families.

### BACKGROUND TRIAGE AT SESSION START
Load was 18.5 on 16 cores from the dead session. Killed: fm2.py (finished
round-10 audit leftover), six hheight.py raw-game climbs (RETRACTED search
space -- raw games are the wrong space, normal form is the right one), and the
two m=3 normform climbs (m=3 is settled by the census). KEPT: normform.py 63,64
(m=4, aiming at h*_1(4)=6; both have reached height 4) and t_wd.py/t_wd2.py
(independent verification of def:wedge; wd2.log now confirms first fire 4 and 8
at j=2,3, N=21,27, matching the claimed table).

### MY OWN RESULTS THIS SESSION, PROVED AND INTEGRATED (95 pp, 239 results)
Commits a7f2dc8, 3d6b37a, and the submodularity one. All computed with code I
wrote from the definitions, in C or exact rational python, in
scratchpad/root12/ and scratchpad/root12/census/.

1. prop:auso-census + rem:auso-census (commit a7f2dc8). MY OWN independent
   enumeration of the m-cube, m <= 4, written in C from the Szabo-Welzl
   condition: 12 / 744 / 5541744 USOs, 12 / 728 / 4792176 ACYCLIC, in
   2 / 18 / 12640 isomorphism classes under the order-2^m m! automorphism group.
   h*(m) = 1,2,4,7; h*(4)=7 attained by exactly 384 outmaps = ONE FREE ORBIT.
   Holt-Klee (proper unit-capacity max flow WITH residual arcs on the
   vertex-split face graph -- my first version used greedy path packing and
   UNDERCOUNTED, 306336 instead of 2322704): 12 / 656 / 2322704 in 2 / 16 / 6113
   classes, h*_HK(m) = 1,2,4,6. EVERY round-11 number reproduced exactly
   (12640 and 6113 classes, the orbit of 384). Also: every BA walk of every AUSO
   at m <= 4 terminates. NEW: f(4) = 7 = h*(4), so cor:f-auso is tight at m=4,
   one size beyond what rem:f-auso recorded.
2. prop:hstar-five + rem:hstar-five (commit 3d6b37a) -- THE REAL RESULT.
   h*(5) = 12 but f(5) = 13. Method: enumerate all law-abiding sequences with
   sigma_0 = 0 (translation invariance), getting
   31,750,12390,135930,967560,4378320,12280440,20388600,19136400,9748080,
   2550240,347640,22320 for lengths 1..13 and none of length 14 -- which
   independently REPRODUCES the paper's f(5)=13; then decide realisability by
   forcing s(sigma_t)=S_t, s(sigma_L)=0 and completing the outmap by DFS.
   All 22320 length-13 sequences fail; a length-12 one succeeds. Witness outmap
   verified separately: bijection, USO condition, ONE SINK AND ONE SOURCE ON ALL
   211 POSITIVE-DIMENSIONAL FACES by direct inspection, acyclic, BA height 12.
   => THE CONVERSE OF lem:auso-laws IS FALSE. I therefore CORRECTED two
   overstatements that had been in the paper: lem:auso-laws was titled "The two
   laws are the AUSO axioms" (now "Every bottom-antipodal trace obeys the two
   laws") and rem:allsw-laws said the laws "are exactly the axioms". The honest
   ceiling for a law-based argument is h*, not f.
3. rem:no-halving-controlled (commit a7f2dc8). prop:no-halving closes halving
   for a; the same question for |C| is closed by thm:fold. P'_D := P_D with u
   retyped as a MAX vertex: both its successors are sinks so it lies in no trap
   whatever its kind, hence P'_D is stopping and P'_D[u:=theta] = P_D[u:=theta];
   so freezing one CONTROLLED vertex of a game with |C| = 2D+1 leaves a residual
   value with exactly 2^{(|C|-1)/2} affine pieces. Asymmetry worth keeping:
   substituting a known AVERAGE value costs a fresh average vertices, whereas
   substituting a known CONTROLLED decision is free -- what fails there is that
   the dependence is exponentially many-branched.
   I re-verified thm:fold myself first: 2704 exact points, D=1..12, 0
   mismatches, slopes exactly {0, 2^-D}, |C| = 2D, a = 4D, pieces = 2^{a/4}.
4. sec:submodular -- lem:readonce, prop:no-submodular, rem:no-submodular.
   SSG-Value = min over the Min cube of the poly-computable val^tau, so
   SUBMODULAR MINIMISATION is the one general hammer. Submodularity is NOT
   invariant under flipping a coordinate, so the honest question is whether SOME
   orientation works. lem:readonce: every read-once formula over OR (a Max
   vertex) and MUX_i (a Min vertex) is val^tau(r) for a deterministic stopping
   SSG on |F|+2 vertices -- verified on 264 random formulas, 2116 (game,tau)
   pairs, 0 mismatches. prop:no-submodular: the FIVE-VERTEX Min AND-chain
   m1->(m2,t0), m2->(m3,t0), m3->(t1,t0) gives val^tau(m1) = [tau=(0,0,0)], the
   indicator of a point of the 3-cube, and NO indicator of a point of {0,1}^3 is
   submodular under any of the 8 orientations (two-line proof, plus exhaustive
   check). CODIMENSION 2 WOULD HAVE BEEN HARMLESS -- it is submodular after
   flipping one coordinate -- so three is exactly where it starts.
   Dual: Vmax chain v1->(v2,t1), v2->(v3,t1), v3->(t0,t1) gives
   val_sigma = 1 - [sigma=(0,0,0)], supermodular in no orientation.
   Random search first: 102/726 games fail submodularity at the identity
   orientation, and 10/288 fail under ALL orientations -- that is what pointed
   at codimension 3; the minimal witness came from reading the failures.

### RUNNING / BACKGROUND
- scratchpad/root12/census/: uso.c (v1, greedy Holt-Klee -- SUPERSEDED, do not
  cite its 306336), uso2.c (correct), tall.c (BA-height hill climb; reaches the
  true h* at m=3,4 and only 11 at m=5, i.e. SEARCH MISSED the true 12 -- another
  instance of the project's iron law), hstar.c (the exact decider).
- The prior session's t_wd.py/t_wd2.py finished j=4: first fire 17 at N=33,
  matching def:wedge's claimed 4, 8, 17. Three sizes now independently checked.

## ROUND 12 COMPLETE (wf_163dfb2c-bb8): 27 agents, 0 errors, 6.82M tokens, 2.7h
Verdicts: universal-lattice, lcp-nonM, approx-scheme, two-player-wedge,
auso-realise, hk-lower = strict-progress; order-space = blocked;
polytope-vertices, free-search-12 = dead-end.
ONLY 4 OF 18 AUDITS sound=True (round 11 was 6/18). THREE FATAL findings.

### THREE FATAL AUDIT FINDINGS — do not build on these
1. order-space's os:bubble-monotone is FALSE, NOT A GAP. Both its audits found
   an explicit 8-vertex stopping counterexample where sigma_f is UNIQUE on both
   sides, the bubble condition holds, sigma_f is already OPTIMAL, and the bubble
   step moves to a strictly worse Max strategy. The route's "34429 bubble steps,
   0 failures" is a sampling artefact -- ROUND 10's HEADLINE ERROR REPEATED.
   I had reported this to the user as "the one live thread"; it is dead.
2. two-player-wedge's rem:tpw-geometry ("Min is not decoration") is FALSE. A
   control experiment shows Min's optimal choice merely reproduces WD's
   deterministic edge and Min's SECOND choice supplies an extra facet of Q(G)
   that strictly ACCELERATES the own-successor test. The TW family may still be
   correct; its explanation is backwards.
3. approx-scheme: approx:collapse IS PRIOR ART -- Dai & Ge, "New Results on
   Simple Stochastic Games". Also its two reductions hand the oracle a
   NON-STOPPING game while the problems are defined on stopping SSGs; and
   approx:noamp's load-bearing identity val(A[G]) = f_A(val_G(v0)) is never
   stated, never proved, and false in general (proved only for two schemes).
   The barrier half is broken. The collapse itself is real but published.

### WHAT SURVIVED AND IS WORTH INTEGRATING (I have NOT verified any of it)
- auso-realise (one audit sound=True): (u3) AND (u4) BOTH PROVED. So the
  improvement orientation of a one-player stopping SSG IS an LP orientation
  (hence Holt-Klee) and all-switches on it IS Howard's rule on transient
  2-action MDPs. h*_1(4) = 6 EXACTLY (upper bound from (u3) + my h*_HK(4)=6;
  lower bound a verified 47-vertex one-player game). => MY rem:auso-census
  CONDITIONAL CAN BE MADE UNCONDITIONAL. Also: an exact two-way dictionary
  between stopping SSGs and 2|C| substochastic affine maps making realisability
  of a prescribed AUSO an exact LP; a NEW POLYNOMIAL CLASS (comparable action
  rows => all-switches in <= |Vmax|+1 rounds); composition delimited by two
  proved additivity obstructions plus one proved +1 scheme.
  HEIGHT 7 AT m=4 IS NECESSARILY TWO-PLAYER, AND IS NEITHER REALISED NOR
  OBSTRUCTED. That is now the smallest concrete open instance of the pivot.
- hk-lower (BOTH audits sound=True, one with zero findings -- the cleanest
  result of the round): INDEPENDENTLY DERIVED h*(5) <= 12 < 13 = f(5), the same
  separation I proved myself this morning as prop:hstar-five. Two independent
  derivations now agree. Also: all-switches is exactly a walk on a hyperplane
  arrangement, capping every bounded-comparison-rank design at a fixed
  polynomial (tight at rank one, explicit family); two proved obstructions kill
  both natural two-scale mechanisms. NO superpolynomial family.
- two-player-wedge: TW(2j,j,j+4), N = 8j+13, two Max and two Min, keeps the
  Z-seeded own-successor hybrid silent at ALL FOUR controlled vertices for
  5, 10, 19, 39 rounds at N = 37,45,53,61 -- doubling every eight vertices. Plus
  a theorem that no such family exists on one Max and one Min vertex.
  IT REFUTES MY "same pivot" INTUITION for the object I named: TW's improvement
  orientation is an AUSO of BA height 1 and all-switches halts in one round.
  The reduction to cor:f-auso holds only for a STRENGTHENED object that also
  defeats sec:seeded.
- polytope-vertices (dead-end, but quantitative): Q(G) has EXPONENTIALLY many
  vertices. M(d) = 2, 6, 14, >=45, >=112, >=287 for |C| = d = 1..6 against 2^d
  profiles, and 2^{N-4} vertices already on a nondegenerate stopping game with
  a = 2 that thm:few-avg solves in linear time -- so enumerating vertices is
  STRICTLY MORE EXPENSIVE than brute force over profiles. Salvage, all proved:
  Q(G) has at most 3|C| facets (attained d=2..6); Psi = ||x - Tx||_1 is concave
  on Q(G) with a unique zero and exact modulus ||x-w*||_inf <= N 2^a Psi(x),
  with kappa attained 2^{N-5}/3; concavity yields NO valid cut; the only
  positional-profile value vector in Q(G) is w* itself.
  => THIS ANSWERS MY OWN QUESTION 1 NEGATIVELY. Do not revisit.
- free-search-12 CONTROL HOMOTOPY (one audit sound=True), dead-end but sharp:
  a new exact poly-startable continuation deforming the game from a Markov
  chain, cost one linear solve per switch of the optimal pair. It ANNIHILATES
  both state-of-the-art hard families (B = 0 on WD(e,j,m) and on CC(L,m) for
  ALL parameters, proved) and yet needs tribonacci-many (2^{0.146N}) switches on
  the paper's OWN P_D of thm:fold, which is ACYCLIC and linear-time solvable.
  => thm:fold kills EVERY scalar continuation that tracks the optimal pair,
  including one whose parameter is player strength, not payoff.
- universal-lattice: every uniformly local lifting scheme correct on player-free
  stopping SSGs has |L| >= 2^{floor((N-3)/2)}+1, so a TOTALLY ORDERED lattice
  (the shape of every quasi-polynomial parity algorithm) has height 2^{Omega(N)}
  -- no universal tree transfers. But an explicit uniformly local scheme of
  height 2N+2 exists (truncated type-trees), so no general height barrier is
  true; the residual "effective scheme" question is target-equivalent
  (thm:ul-decoder). Both audits sound=False, 5 major findings.
- lcp-nonM: thm:lcpM-spectral (rho(Phi) < 1 => condition (U) => w* is the unique
  optimum of ONE explicit LP over Q(G)) with family W_n escaping all four
  classes of sec:special. AUDIT DAMAGE: thm:lcpM-boundary's class S_2 is NOT a
  property of the game (it depends which weak witness the LP returns);
  prop:lcpM-minimal's minimality clause is FALSE (nondegenerate 6-vertex
  instances fail (U)); and "(U) held on 200 random mixed stopping games" is
  again the round-10 error, the sample concentrated at small |C|.

### PRIOR-ART DEBTS THE PAPER NOW OWES (correctness, not politeness)
- Gimbert-Horn, LMCS 5(2:9) 2009: the order space IS their permutation space,
  and the decoder of thm:order-determines IS their f-region/f-strategy
  construction. thm:order-determines may be a rediscovery.
- Dai & Ge, "New Results on Simple Stochastic Games": the approximation
  collapse.
This is the FIFTH and SIXTH rediscovery (after Auger-Coucheney-Strozecki,
Mangasarian, Gaertner-Morris-Ruest in round 11).

### MY ESTIMATE, GIVEN TO THE USER
~12 more rounds CONDITIONAL on a proof being reachable by this process (rule of
three on 0 successes in ~120 routes gives >= 5; Laplace gives ~14); no finite
unconditional estimate, and I put 10-15% on reachability. The dominant evidence
is NOT pool depletion -- I retracted that, round 12's four fresh formulations
disprove it -- but that fresh formulations keep TERMINATING at target-equivalent
statements (thm:ul-decoder and os:onebit are two more), plus the rediscovery
rate.

## SESSION dc099d6a (2026-09-01). ROUND 13 LAUNCHED
State on arrival: frontier.tex 95 pp, 237 numbered results (51 thm, 39 lem, 33
prop, 14 cor, 35 def, 65 rem), `make pdf` clean, 0 undefined refs, git clean at
0a9acfd. Harness copied forward to scratchpad/root13/.
Round 13 = runId wf_9a555369-4c3, task w0h8r4dib, script scratchpad/round13.js.
9 routes x 2 adversarial audits = 27 agents. SIX of the nine are formulations
never tried in twelve rounds:
 schur-elimination (leave the FAIR-COIN model: exact Schur-complement removal of
 average vertices in the generalised rational-probability model; confront
 prop:no-halving; ask for a confluent value-preserving rewriting system);
 newton-dinkelbach (val as a ratio of determinant-like counts via forest
 balance; Dinkelbach/Newton parametric search; is the iteration an improving
 rule, and what is its iteration count);
 softmax-homotopy (deform the OPERATOR, not the payoff/discount/player strength;
 entropic regularisation, path following, and whether a fixed poly(N) inverse
 temperature already decides -- expect a refutation, demand it be exact);
 nonlinear-perron (MULTIPLICATIVE certificates: Collatz-Wielandt and the Hilbert
 projective metric, whose contraction rate is the projective diameter and NOT
 the mixing rate 1-2^-a that thm:slack-barrier pins every additive mechanism to);
 ueopl-promise (the UniqueEOPL structure: the line, the potential, and whether a
 poly-time SIDE oracle exists or is target-equivalent);
 symmetric-improvement (bidirectional strategy improvement in the sense of
 Schewe et al. for parity games -- NO barrier in frontier.tex covers it:
 cor:no-height is about the Max lattice alone, thm:normalform-barrier about
 residue-blind rules, prop:locality about bounded radius).
Plus auso-pivot (BA height 7 at m=4, necessarily two-player, neither realised
nor obstructed -- the smallest concrete open instance of the pivot), 
two-player-wedge (verify (v5)'s TW family; build one that also defeats M3), and
free-search-13 with an explicit anti-list of all twelve rounds.
The brief carries THE STANDING RULE, the label-by-label fact list, the
unverified claims (v1)-(v9), and the SIX prior-art debts.

### MY OWN NEW THEOREM THIS SESSION — thm:window-barrier
I set out to answer my own round-8 question ("is R_k residue-blind for k>=1?")
and first REDISCOVERED THE PAPER'S OWN def:freeze / prop:freeze-sound /
prop:freeze-escapes / rem:freeze -- the freezing hierarchy is already there.
Lesson: grep frontier.tex for the OBJECT before building it; I lost an hour.
What is genuinely new is the answer to what rem:freeze left open. rem:freeze
says "already |B|=1 escapes thm:normalform-barrier". IT DOES, BUT THE ESCAPE IS
AGAIN A PRESENTATION ARTEFACT:
 def:kblind N_k(G) -- subdivide EVERY edge (z,u) by m = k+1 copies of
 lem:normalform's two-cycle gadget, g_j -> (g_{j+1}, h_j), h_j -> (g_{j+1}, g_j),
 g_{m+1} := u.  |V| = N + 4(k+1)(N-2) <= (4k+5)N.
 lem:kblind -- values, stopping, S_sigma and the whole all-switches trajectory
 preserved; no new vertex is a splice or merge redex; controlled vertices are an
 independent set.  Chain computation: 2y(g_j) = y(g_{j+1}) + y(h_j) and
 2y(h_j) = y(g_{j+1}) + y(g_j) give 3(y(g_j) - y(h_j)) = 0, so y is CONSTANT
 along the chain.
 thm:window-barrier -- on N_k(G), rho_B(sigma) = sigma[S_sigma] for EVERY
 B with |B| <= k.  Proof: |B| <= k < m forces a frozen spine vertex g_j; the
 live prefix W = {g_1..g_{j-1}} u ({h_i} n B) is closed under successors up to
 terminals that ALL carry the same payoff alpha = x(u), so the (nonsingular)
 subsystem gives D = alpha on W, hence D(g_1) = x(g_1) for EVERY edge -- the
 argument is confined to one chain and never touches the rest of the game.
 Then D at a controlled vertex is the max/min of x at its two old successors,
 which is exactly the all-switches comparison.
 CONSEQUENCE: no k-window rule with k = N^{O(1)} halts in poly rounds unless
 all-switches does.  The whole polynomial-time part of def:freeze is covered.
 NOT covered: windows that are a constant FRACTION of Vavg (on N_k(G) the
 average set has grown to a + 4(k+1)(N-2)), in particular rho_{Vavg}, which
 finishes in one round and is not polynomial.
MY VERIFICATION: 120 stopping games, k = 1 and 2, 24884 (sigma,B) checks --
0 violations of size, stopping, value preservation, chain-constancy, S_sigma,
all-switches run length, or the blinding identity.  Harness scratchpad/root13/
(rk.py, blind.py, t_rk1.py, t_blind.py).
ALSO VERIFIED, independently of the paper: prop:freeze-sound's three relations
on 83 stopping games / 2472 (sigma,A) pairs, 0 violations; and a 10-vertex
BIPARTITE witness with a = 7, |A| = 1 that rho_A is not residue-blind (the
paper's own prop:freeze-escapes has a = 3).
A COUNTING TRAP I FELL INTO: my first run_RA counted the terminal
non-productive round, making rho_B look slower than all-switches in 24838 of
25012 comparisons.  With the off-by-one fixed the true figures are faster 283,
slower 49, equal 26840 -- BOTH directions occur, as thm:all-switches-refuted
predicts.  Always count PRODUCTIVE rounds on both sides of a rule comparison.

### MY SECOND THEOREM THIS SESSION — thm:separable (100 pp, 246 results, 23ed91a)
Closes, NEGATIVELY, memory's standing "highest-value unfinished work #1" (find
the invariant a min-plus closure preserves, to bound the rate of def:trans-slack
from below).
def:separable -- a schedule M_k(x,y) = phi_k(x) - psi_k(y) is ADMISSIBLE if
(a) M_{k+1} <= every clause of def:slack at M_k, and (b) each M_{k+1} obeys the
triangle inequality.  (a) alone is what an induction proving M_k <= Delta_k
needs; (b) is exactly what the min-plus closure of def:trans-slack adds.
lem:separable-lower -- admissible implies M_k <= Delta^T_k.
thm:separable -- THE COLLAPSE.  The diagonal base "0 if x=y" gives phi <= psi;
the triangle inequality at y := x gives psi <= phi; so phi_k = psi_k.  Then
(up) and (down) read AT THE DIAGONAL give 0 <= (T phi_k)(x) - phi_k(x) and
0 <= phi_k(x) - (T phi_k)(x), so T phi_k = phi_k.  Normalising phi_k(t0)=0, the
Z0/Z1 base forces phi_k(t1) >= 1 and the constant clause forces <= 1.  On a
STOPPING game lem:gen-comparison then gives phi_k = w*, so M_k(x,y) =
w*(x) - w*(y) EXACTLY -- the limit thm:trans-complete already supplies.  So NO
separable certificate can prove a rate lower bound on a stopping game.
cor:separable -- (a) thm:slack-barrier's E_k(x,y) = u_k(x) - l_k(y) DOES obey
the triangle inequality (E(x,z)+E(z,y)-E(x,y) = u_k(z)-l_k(z) >= 0); what it
violates is the DIAGONAL BASE, since E_k(x,x) > 0 >= Delta_k(x,x).  THIS
CORRECTS rem:trans, which had asserted the triangle inequality fails -- my own
error, recorded in this file since round 8.  I verified 0 triangle violations
over 120 games x 4 rounds x all triples, and 0 violations of Delta^T_k(x,x)<=0.
(b) lem:phi-certificate is the ONLY separable certificate, so prop:trans-stall's
permanent stall HAD to be non-stopping; I confirmed phi = (1/2,1,3/4,1) is a
second fixed point of T on its A_0 and that phi(p)-phi(q) = 1/4 is exactly the
stall value.  (c) a rate proof needs a non-separable certificate.
(d) THE SAME COLLAPSE COVERS def:hybrid, since a hybrid round applies L then C
-- the structural form of rem:hybrid-barrier-lift.
(e) WHAT ESCAPES, and this is the useful half: thm:hybrid-convex-barrier's
certificates are SUPPORT-FUNCTION DIFFERENCES Lambda(P)(x,y) = max_{z in P}
(z(x)-z(y)), whose DIAGONAL VANISHES, so they are not separable.  Zeroing the
diagonal of u_k - l_k restores the closure conditions but NOT the clause
conditions -- and cannot, by prop:trans-Hm.  So thm:slack-barrier's disjointness
hypothesis is load-bearing, not cosmetic.
=> THE DESIGN RULE THIS GIVES: a certificate for any min-plus-closed mechanism
must have zero diagonal and must be genuinely matrix-valued.  Every box, and
every pair of potentials, is dead.

### ROUND 13 HIT THE SESSION USAGE LIMIT, then RESUMED
First launch (wf_9a555369-4c3, task w0h8r4dib): only nonlinear-perron returned;
8 routes + both its audits died with "You've hit your session limit". Resumed
IN THE SAME SESSION with Workflow({scriptPath: scratchpad/round13.js,
resumeFromRunId: 'wf_9a555369-4c3'}) as task w2nvm9qc4 -- the cached route
replays and the failures re-run. THIS WORKED; note resumeFromRunId is
same-session only, so a limit hit is recoverable only if you resume before the
session ends.

### ROUTE nonlinear-perron (verdict blocked) -- I VERIFIED IT AND INTEGRATED IT
frontier.tex now 104 pp, ~256 results, commit ee4891b. New sec:ratio.
CLOSED: prop:cw -- after homogenisation (def:homog, sink coordinate * carried
as a free scale) the cone spectral radius of T-hat is IDENTICALLY 1, because
(T-hat y)(*) = y(*) pins the ratio at * to 1; so bisection on lambda returns 1
on every game. And the Collatz-Wielandt bracket bounds NOTHING: D_L (all
average, c_j -> (c_{j+1},c_{j+1}), c_L -> (t1,t1)) with y(c_j) = 2^{-(L-j)} has
bracket [1,2] yet max w*/y = 2^{L-1} = 2^{N-3}.  MY CHECK: exact, L =
3,5,8,12,20 giving 4,16,128,2048,524288.  The scale cannot be normalised away
because rescaling y on V' does not rescale yhat(t1) = y(*).
SURVIVES: def:ratio, THE RATIO CALCULUS -- reading w*(x) <= R(x,y) w*(y), with
MIN/MAX/HARMONIC mean on the denominator side, MAX/MIN/ARITHMETIC mean on the
numerator side, and composites min_j max_i / max_i min_j (two Max), min_i max_j
/ max_j min_i (two Min), max_i R(x^i, y^{pi(i)}) (two average, the MEDIANT
inequality).  I re-derived every clause myself and wrote my own implementation
from the STATEMENT (scratchpad/root13/ratio.py, t_ratio.py, t_ratio2.py).
 - thm:ratio-sound: 300 random games, 210 of them NON-stopping, 6 rounds, all
   N^2 entries -- 0 unsound entries, 0 monotonicity violations.
 - thm:ratio-sandwich(a) R_{2k} <= u_k(x)/l_k(y): 38946 entries, 0 violations.
 - thm:ratio-sandwich(b) THE BARRIER, same A,B hypotheses as thm:slack-barrier:
   140 stopping games, 180 separated pairs, 14412 entries, 0 violations, 8880
   ATTAINED with equality (and 5451 entries where the bound is +oo and R is
   indeed +oo).  THE DIAGONAL IS THE CRUX, exactly as in my own thm:separable:
   off the sinks E_k(x,x) = u_k(x)/l_k(x) > 1 exceeds the diagonal clause, which
   is WHY A and B must be disjoint.
 - cor:ratio-stall on H_m: own-successor test first fires at 15, 39, 101 for
   m = 3,4,5 -- IDENTICAL to the additive calculus.
 - prop:ratio-incomparable, BOTH directions verified exactly: on W (avg 0,1,2;
   0->(t0,2), 1->(t0,t1), 2->(t1,1); w* = 3/8,1/2,3/4) R_2(0,2) = 1/2 decides
   and Delta_2(0,2) = 0 does not; on W' (7 avg, edges (6,5),(0,7),(1,4),(3,0),
   (8,5),(2,7),(5,4); w* = 2/7,1/7,18/49,2/7,29/49,9/49,19/49) Delta_7(3,6) =
   -1/64 decides and R_7(3,6) = 259/240 does not, R catching up at round 8 with
   221/240.
=> THE MORAL, now in rem:ratio: thm:slack-barrier is NOT a fact about additive
propagation.  What it constrains is any calculus that matches the two branches
of an average vertex ONE AT A TIME, whatever algebra combines them.  Same moral
as rem:magnitude, reached from the other side.
NOT INTEGRATED (I have not verified these): the route's Hilbert-projective-metric
claims -- Birkhoff coefficient exactly 1, projective diameter +oo at every power,
and projective iteration on G_m needing 12,36,98,247,594,1384,3148 steps against
value iteration's 13,37,99,248,595,1385,3149 (exactly ONE step faster).  Wait for
its audits, which died with the session limit and are re-running.

### MY THIRD THEOREM THIS SESSION — def:mobius / prop:mobius (105 pp, commit a112313)
Generalises the round-13 ratio calculus from a second data point to a CONTINUUM.
R^beta := def:ratio run on G^beta, the game whose sinks pay beta and 1+beta.
Since x -> x+beta is an increasing affine bijection commuting with max, min and
the mean, T^beta(x) = beta + T(x-beta), so G^beta has value w*+beta and its
value iterates are u_k+beta, l_k+beta.  beta = 0 IS the ratio calculus, and
beta -> oo recovers def:slack to first order (harmonic and arithmetic means
agree to first order in 1/beta).
THE POINT (prop:mobius(c)): (u+beta)/(l+beta) > 1 IFF u > l, so the barrier's
decisive condition is beta-FREE and the entire continuum stalls on H_m at
IDENTICAL rounds.  MEASURED: first firing 15, 39, 101 for m=3,4,5 at every
beta in {0, 1/4, 1, 4}.
AND YET THE FAMILY IS NOT A REPARAMETRISATION (prop:mobius(d)): on W the pair
(0,2) is decided at round 2 by beta=0 but only round 3 by beta=1/4,1,4; on W'
the pair (3,6) at round 7 by beta=1,4 but only round 8 by beta=0,1/4.  So the
members are PAIRWISE INCOMPARABLE and still all equally stuck.
rem:mobius ALSO CARRIES thm:separable ACROSS: for M(x,y) = phi(x)/psi(y), the
min-TIMES triangle inequality gives psi <= phi, the diagonal base gives
phi <= psi, and the two clauses read at the diagonal give T phi = phi (the
harmonic mean of phi(x)/phi(x^j) is phi(x) over the arithmetic mean of the
phi(x^j)).  So a multiplicative rate proof also needs a certificate that is not
a ratio of two potentials.
MY VERIFICATION: 200 games x 4 betas x 6 rounds x all entries -- 0 unsound,
0 non-monotone, 0 sandwich violations (25140 checks per beta); H_m barrier
violations 0; the incomparability table exact.  Harness scratchpad/root13/
mobius.py, t_mobius.py.

### THE ONE OPEN QUESTION I LEFT IN rem:mobius, and it is being measured
Does the MIN-TIMES closure of def:ratio escape thm:ratio-sandwich(b), the way
the min-plus closure of def:slack escapes thm:slack-barrier (prop:trans-Hm
drops H_m from 2^{Omega(N)} to 4m-3 = 9,13,17)?  Running
scratchpad/root13/t_ratiotrans.py, which compares all four calculi on H_m for
m = 3,4,5.  If the multiplicative closure also collapses H_m, the escape is a
property of CLOSURE and not of additivity, which is the natural next sentence
of rem:mobius; if it does not, that is a genuine separation between the two
closures and a better result.

### ANSWERED THE SAME DAY — prop:ratio-closure (106 pp, commit 0bd63ba)
The min-TIMES closure of def:ratio DOES escape thm:ratio-sandwich(b), exactly as
the min-plus closure escapes thm:slack-barrier.  Sound because the true ratios
satisfy D(x,y) <= D(x,z) D(z,y) with EQUALITY wherever w*(z) > 0 (conventions
c/0 = +oo for c>0, 0/0 = 0).  FIRST FIRING ROUND ON H_m, all measured by me:
  m            3   4   5   6   7
  slack       15  39 101   -   -      (2^{Omega(N)})
  ratio       15  39 101   -   -      (2^{Omega(N)}, identical)
  trans-slack  9  13  17  21  25      (= 4m-3, matches the paper)
  trans-ratio  7  11  15  20  24      (4m-5 for m<=5, then 4m-4)
=> THE ESCAPE BELONGS TO THE CLOSURE CLAUSE, NOT TO THE ALGEBRA.  prop:trans-Hm
and prop:ratio-closure are the additive and multiplicative halves of one
phenomenon, and the multiplicative half is marginally faster on this family.
CAVEAT I STATED IN THE PAPER: the trans-ratio column is the ROUNDED-AND-CAPPED
variant (round up to a multiple of 2^{-(2a+2)}, cap at 2^a -- both sound, the
cap by lem:denominator-sharp), because the EXACT min-times closure blows the
denominators up: t_ratiotrans.py ran 100% CPU for 13 minutes on m=3 alone
without finishing.  The rounding can only DELAY firing, so 4m-4 at m=6,7 may be
a rounding artefact and I did not claim the clean 4m-5 law.
HARNESS: scratchpad/root13/t_rt2.py (rounded, fast), t_ratiotrans.py (exact,
too slow -- do not rerun without rounding).

### THE WEDGE SURVIVES EVERYTHING MULTIPLICATIVE (107 pp, commits abd428e, 7003231)
1. WD(2j,j,j+4) defeats the MIN-TIMES closure too: first firing 30, 87, >170 at
   N = 21, 27, 33, against 21, 51, 112 for def:trans-slack.  So the two closures
   are INCOMPARABLE IN SPEED -- multiplicative faster on H_m (7,11,15 vs
   9,13,17), slower on WD.  rem:wedge now says the wedge is the one obstruction
   in the paper that no calculus in it evades.
2. MY OWN IDEA, AND IT FAILED, WHICH IS WORTH REMEMBERING.  In xi = z - w*
   coordinates a multiplicative cut z(p) <= R(p,q) z(q) reads
   xi(p) <= R xi(q) + (R w*(q) - w*(p)), whose constant VANISHES when R is
   exact -- so an exact ratio cut is a CONE THROUGH THE APEX, exactly the shape
   the wedge is made of.  That is why I expected it to crack WD.  IT DOES NOT:
   the augmented programme leaves the first firing round at 4, 8, 17 for
   j = 2,3,4 and leaves the POLYGON LITERALLY UNCHANGED at every round, while
   adding 346-348 non-trivial ratio cuts per round beside 218-372 difference
   cuts.  REASON: a ratio read off the polytope is by construction a supporting
   half-plane of it, and the clause-derived ratios are never tighter here; the
   obstruction is the RATE at which the cone narrows (lambda = 1-2^{1-j}), and
   more cones through the same apex do not change a rate.
   GENERAL LESSON: when a family's hardness is a contraction RATE, no additional
   valid inequality of the same homogeneity can help.  Check whether a proposed
   cut changes the rate before believing it changes anything.
3. BY-PRODUCT: I rebuilt WD, the affine lift and an exact 2-D Sutherland-Hodgman
   clipper from scratch (scratchpad/root13/t_wdratio.py, rathyb.py) and
   REPRODUCED prop:wedge's published 4, 8, 17 independently.
   PERFORMANCE NOTE: hyb2d.polygon's pairwise-intersection routine is O(|H|^3)
   and is unusable at |H| ~ N^2 = 441; clip_polygon in rathyb.py is O(|H|.|V|)
   and does the same job in seconds.  Use it for any future |C| = 2 measurement.

### A FIFTH POLYNOMIAL CLASS — thm:escape-class (109 pp, commit 2652084)
From round 13's nonlinear-perron route, whose TWO independent runs agree with
each other; verified from the statements on my own code.  This is the POSITIVE
yield of a route whose verdict was "blocked", and the portfolio needed it.
def:survival -- S is the SURVIVAL operator: max at EVERY controlled vertex
(MIN's as well as Max's), mean at every average vertex, sinks read as 0.  An
ESCAPE CERTIFICATE is (lambda, x), lambda in (0,1), x >= 1, with Sx <= lambda x;
conditioning kappa = max x / min x.
lem:survival -- (a) |T^k y - T^k z| <= S^k |y-z|; (b) ||T^k 1 - T^k 0|| <=
lambda^k kappa; (c) a certificate implies STOPPING (S^k 1 dominates the
non-absorption probability under every profile).
thm:escape-class -- thm:few-escape's OWN algorithm (iterate T, round to
denominator <= 2^a, stop when lem:certificate accepts) then halts in
O((a + log kappa)/log(1/lambda)) iterations.  NO knowledge of lambda or x is
needed; the certificate enters only the RUNNING-TIME analysis, so correctness
is unconditional.  Existence of a certificate is ONE LP, because a maximum on
the LEFT of <= splits into a conjunction.
prop:escape-family E_D (N = 3D+7): Vavg = s_1..s_D, p_1..p_D, r, z, g_0;
Vmax = q_1..q_D, v_0; Vmin = u.  s_1->(t1,t0), s_j->(s_{j-1},t0),
q_i->(p_i,t0), p_i->(q_{i mod D+1}, t1), u->(r,t1), r->(u,t0), z->(s_D,u),
v_0->(z,q_1), g_0->(t1,s_D).  val(g_0) = 1/2 + 2^-(D+1).  Certificate
lambda = 3/4 with x = 1 on s,q,u,g_0; 3/4 on p,r; 4/3 on z; 16/9 on v_0;
kappa = 64/27 INDEPENDENT OF D.  And it is outside ALL four existing classes:
a = 2D+3, d(E_D) = D+1, all three colours on cycles, Max-reachability component
of size D, |Vmax| = D+1.
MY VERIFICATION (scratchpad/root13/t_escape.py): Lipschitz domination on 200
games x 3000 triples, 0 violations; bracket bound at every round for
D = 3,4,5,6,10, 0 violations; certificate entrywise; stopping; val(g_0) exact;
d(E_D) = D+1 RECOMPUTED FROM def:escape over all optimal strategies (4,5,6,7 for
D=3..6); VI rounds 39,47,55,63,95 -- linear.
HONEST FRAMING I PUT IN rem:escape-class: the condition is QUANTITATIVE, not
structural -- every stopping game has S^k 1 -> 0 and thm:contraction bounds the
rate by (1-2^-a)^{k/N}; the content is that the rate be polynomially bounded
below.  Whether every fast-contracting stopping game admits a certificate
attaining its rate is NOT determined and the theorem does not need it.  The
sub-eigenvector/Collatz-Wielandt vocabulary is classical -- attribute; what is
specific is the survival operator (both players read as maximisers) and E_D.

### A DEFECT I INTRODUCED AND CAUGHT THE SAME DAY (commit 451667b)
lem:survival(b) as I first wrote it said ||T^k 1 - T^k 0|| <= lambda^k kappa.
FALSE at k = 1: the constants 1 and 0 do not carry the sink payoffs, so the
first application of T reads the WRONG value at a sink successor.  Measured:
874 violations across 250 games with unpinned starts, ZERO with pinned ones.
Repaired by fixing u_0 = 1 on V' and l_0 = 0 on V', both carrying 0 at t0 and
1 at t1 -- and l_0 is then exactly the vector 1_{t1} that thm:few-escape already
iterates, so nothing downstream changes.
FOUND BY: a final sanity sweep re-running every claim I added today on FRESH
larger instances (n = 6,7,8) rather than the ones used to develop them.  THE
LESSON, and it is the general one: after integrating, re-run every new claim on
an instance set generated differently from the development set.  The ratio
calculus, the Mobius family and both sandwich directions came through that
sweep with 0 violations over 40386 checks; only the one statement I had NOT
re-derived from its own hypothesis failed.
STANDING TRAP TO ADD TO THE BRIEF: any bound of the form
"|T^k y - T^k z| <= (something)^k" requires y and z to AGREE WITH THE SINK
PAYOFFS; T pins the sinks only from the first application onward.

### THE ESCAPE CLASS'S FAMILY WAS BROKEN — repaired same day (110 pp, 451667b..)
Round 13's SIGNIFICANCE audit of nonlinear-perron came back sound=False/high and
was RIGHT about my integration.  E_D's separation lived ENTIRELY IN THE
UNREACHABLE PART: from the start vertex g_0 only {g_0, s_D..s_1} is reachable --
a player-free acyclic chain that thm:avg-acyclic decides in linear time -- while
the q/p cycle, u, r, z and v_0 (2D+4 vertices) that carry items (iv) k-acyclicity,
(v) bounded components and (vi) |Vmax| are unreachable.
MY ERROR, EXACTLY: I verified a, d, colours-on-cycles, |Vmax| and the
Max-reachability component ON THE WHOLE GAME.  Membership of a polynomial class
is a property of the instance AS POSED, so every such check must run on the
subgame REACHABLE FROM v_0.  ADD THIS TO THE STANDING TRAPS.
REPAIR (the audit's Z_D, verified by me for D = 3..7, 10, 14): non-sinks
s_1..s_D avg, M_2..M_D Max, W Min; s_1->(t1,W), s_j->(M_j,t0), M_j->(s_{j-1},t0),
W->(s_D,t1); start s_D.  N = 2D+2, a = D, |Vmax| = D-1, d(Z_D) = D, val(s_D) =
1/(2^D - 1).  EVERY non-sink lies on the SINGLE cycle
s_D -> M_D -> s_{D-1} -> ... -> s_1 -> W -> s_D, which carries all three colours
-- so it is fully reachable AND immune to a per-SCC refinement of thm:kacyclic.
Certificate lambda = 3/4, x = 1 on Vavg and 3/2 on Vmax u Vmin, kappa = 3/2 for
every D; the constraints compose around the cycle to 2 lambda^2 >= 1, so
2^{-1/2} is the least admissible rate and 3/4 is the smallest convenient
rational above it.  Pinned two-sided iteration closes in 4D+2 rounds.
THE LIMIT ON THE CLASS, also from that audit and now in rem:escape-class: by
thm:slack-vi-upper, Delta_{2k}(x,y) <= u_k(x) - l_k(y) <= w*(x) - w*(y) +
2 lambda^k kappa, so a certificate forces the PLAIN slack calculus to fire
within the same O((a + log kappa)/log(1/lambda)) rounds.  Hence NO member of the
escape class is a stall for M1, M2, M2T or M5, and the class CANNOT REACH THE
FRONTIER.  Its interest is only that it is a polynomial class disjoint from the
four combinatorial ones.

### HOW FAR OUTSIDE THE ESCAPE CLASS THE WEDGE SITS (110 pp, commit 0c98494)
Ties the new class to the paper's hardest family in two lines.  On WD(e,j,m) the
survival constraints along the a-chain (lambda V >= A_1, 2 lambda A_q >=
V + A_{q+1}) compose to A_e <= (alpha* + (2 lambda)^{e-1}(lambda - alpha*)) V
with alpha* = 1/(2 lambda - 1); A_e >= V/(2 lambda) > 0 then forces
(2 lambda)^{e-1}(2 lambda + 1)(1 - lambda) < 1, i.e. 1 - lambda < 2^{1-e}/3.
So EVERY escape certificate for the wedge has log(1/lambda) = 2^{-Theta(N)}.
Float power iteration agrees: rho(S) = 0.9768, 0.9946, 0.9987, 0.9997 at
e = 4,6,8,10.
NOTE ON METHOD: the exact-rational bisection for the least lambda (monotone
iteration x := max(1, Sx/lambda)) is TOO SLOW -- denominators blow up; it timed
out at 570s.  Use floats for exploration and a structural argument for the paper.

## SESSION dc099d6a TALLY (2026-09-01)
frontier.tex 95 -> 110 pages, 237 -> 267 numbered results, clean build, 0
undefined refs, synced after every change.  Still NO polynomial-time algorithm
and none claimed.  Eight integrations, every one verified by me in exact
rational arithmetic before it went in:
thm:window-barrier; thm:separable + cor:separable + cor:set-certificate;
sec:ratio (def:homog, prop:cw, def:ratio, thm:ratio-sound, thm:ratio-sandwich,
cor:ratio-complete, cor:ratio-stall, prop:ratio-incomparable, rem:ratio);
def:mobius + prop:mobius + rem:mobius; prop:ratio-closure + rem:ratio-closure;
two rem:wedge additions; def:survival + lem:survival + thm:escape-class +
prop:escape-family + rem:escape-class; the wedge escape-rate tie-in.
THREE DEFECTS FOUND AND FIXED THE SAME DAY, one by each mechanism:
 - rem:trans's triangle-inequality claim (MY OLD ERROR, from round 8) -- found
   by proving thm:separable;
 - lem:survival(b)'s unpinned starting vectors (MY NEW ERROR) -- found by the
   post-integration sweep on freshly generated instances;
 - prop:escape-family's E_D separating only in the UNREACHABLE part (MY NEW
   ERROR) -- found by round 13's significance audit, repaired with its Z_D.

### rem:wedge OVERSTATED THE WEDGE'S SCOPE — corrected (commit 1bead29)
Round 13's two-player-wedge route reported, and I CONFIRMED with my own
implementation of def:simorder as a greatest fixed point, that WD does NOT
defeat the value-simulation preorder: the gfp contains the pair (v_i, a_{i,1}),
so w*(v_i) <= w*(a_{i,1}) is derived, which at a MAX vertex forces equality and
proves a_{i,1} optimal -- firing direction (i) of rem:own-successor, at ROUND
ZERO.  Verified on WD(4,2,6) and WD(6,3,7); the preorder is sound there (0
violations among derived pairs).
So the correct list is: WD defeats def:slack, def:trans-slack, def:transport and
the hybrid, and defeats NEITHER def:simorder NOR sec:seeded.  The two it fails
against both decide it WITHOUT ITERATING.
This claim predated this session but I had just extended the sentence carrying
it, so it is mine now.  LESSON: when adding to a list of "mechanisms this family
defeats", re-test EVERY entry of the list, not just the one being added.

### STILL TO DIGEST FROM ROUND 13 (audits not yet all back)
- two-player-wedge (strict-progress): claims prop:wedge is NO LONGER A
  MEASUREMENT -- proved silence of the Z-seeded own-successor hybrid on
  WD(e,j,m) for K = 1,6,15,33,68,138,279 at j=2..8 (two short of the measured
  4,8,17,35,70,140); and WW = WD3 (+) WD3^d, a stopping TWO-PLAYER game
  (N = 12j+24) on which M1,M2,M2T,M4,M5 are silent for a PROVED 2^{Omega(N)}
  rounds -- THE OPEN ITEM OF sec:wedge.  Also confirms round-12's TW (v5)
  independently (5,10,19,39 at N=37,45,53,61) and replaces its refuted
  mechanism with a proved one (Min is an ACCELERANT via its NON-optimal action).
  Its own gap is one clause condition for a convex chain.
- free-search-13 = HARMONIC GREEN-KERNEL coordinates (strict-progress): a new
  polynomial class by the RANK k of the |C|x|C| action-difference matrix of the
  harmonic normal form, solved in poly(N) sum_{i<=k} C(|C|,i) by enumerating
  cells of a hyperplane arrangement; family RK(m) with k=1, |C|=m unbounded,
  outside every class in the paper.  Its residual gap is TARGET-EQUIVALENT and
  the route says so.
- ueopl-promise (audit sound=True): the canonical UEOPL line is exponential --
  PEN(D,K) on N=8D+4 with 2^{D+1}+D nodes; the optimal subcube is exactly the
  LCP's degeneracy pattern, so the subcube buys nothing.
- schur-elimination (audit sound=False), newton-dinkelbach (audit sound=False):
  read the findings before integrating anything.

### PRIOR-ART DEBTS FOUND BY ROUND 13's AUDITS — numbers 7 and 8
- STOCHASTIC COMPLEMENTATION, C. D. Meyer, SIAM Review 31 (1989) 240-272,
  equivalently the CENSORED (watched) chain: this IS the schur-elimination
  route's exact vertex elimination.  Attribute if any of it is ever used.
- KANNAN-THEOBALD fixed-rank games (SODA 2007 / Math. Prog.): factoring action
  payoffs through a rank-k map and enumerating the sign vectors as cells of a
  hyperplane arrangement in R^k IS their hierarchy.  THIS MATTERS BECAUSE
  free-search-13's "new polynomial class by the rank of the action-difference
  matrix" is the same method -- do NOT integrate it as new; attribute.
Running total of rediscoveries: Auger-Coucheney-Strozecki, Mangasarian,
Gaertner-Morris-Ruest, Stickney-Watson, Gimbert-Horn, Dai-Ge, Meyer,
Kannan-Theobald.

### AN ERROR PATTERN WORTH REMEMBERING (caught in a parallel claim, then in mine)
The schur audit killed a clause of the form "EE(n) is decided in poly time by X
and by NONE of ..., including thm:few-escape" -- self-contradictory, because X's
own statement says it runs thm:few-escape's algorithm UNCHANGED.  I had the same
shape in prop:escape-family.  FIXED by saying explicitly that the comparison is
between BOUNDS, not algorithms: a polynomial class here is a set of instances on
which some proved bound is polynomial, and all five classes must be read that
way (commit 903a7c2).

### THE WEDGE IS NOW A THEOREM (111 pp, commit 742ad29) — round 13's best result
Round 13's two-player-wedge route, audit sound=True/high.  rem:wedge had said
"We have not proved the clause condition for all parameters, so we state
prop:wedge as a measurement".  NOW PROVED for every j>=2, e>=2j-1, m>=j+2, by
thm:hybrid-lower's method:
 def:wedge-chain  M_0 = 1/2, M_{k+1} = lambda M_k - 2 gamma,
   P_k = {xi in [0,M_k]^2 : xi_1 >= lambda xi_2 - 2 gamma and symmetrically},
   mu = 2 gamma/lambda, mu-dagger = mu/(1 - 2^{j-e}), K = max{k : M_k >= mu-dagger}.
 lem:wedge-verts  P_k is the hull of (0,0),(mu,0),(M_k,M_{k+1}),(M_k,M_k),
   (M_{k+1},M_k),(0,mu) and h_{P_k}(c) = max(c_1 mu, c_1 M_k + c_2 M_{k+1}) for
   c_1 >= 0 >= c_2.
 thm:wedge-proved  most def:slack clauses are FREE from the rows of Q(G); only
   (up) at v_1,v_2 and the Vmax x Vmax composites need work; they reduce to
   u(c_1 + lambda c_2) >= 2^-e (using e >= 2j-1) and M_k >= mu-dagger.
 cor:wedge-count  K = 1,6,15,33,68,138,279,560 for j=2..9, K >= 2^{j-1},
   so 2^{Omega(N)} silent rounds UNCONDITIONALLY.
MY VERIFICATION, all exact: K recomputed from the recursion; the load-bearing
inequality Phi_k(c) >= h_{P_{k+1}}(c) at EVERY direction and EVERY k <= K over
60 triples (j<=6, e in {2j-1,2j,2j+1,3j}, m in {j+2,j+4,j+6}) -- 45526 checks,
0 violations; the direction set theta_y confirmed at three sizes; and the
CONCLUSION Delta_k >= Lambda(P_k) against an actual run of my own hybrid at
j=2,3,4 -- 23409 entry comparisons, 0 violations, test silent throughout.
NOT INTEGRATED from that route, and the audit is why:
 - its "two-player wedge" WW is NOMINAL: WD3 (+) WD3^d with a fresh average root
   IS the disjoint-union gadget already used inside thm:compare-equivalence; the
   two players sit in NON-INTERACTING components, all-switches halts in ONE
   round and M(1,0) decides all four vertices.  sec:wedge's open item is NOT
   closed.
 - its headline "the real target is blocked" restates thm:seed-dichotomy,
   rem:frontier-moved and rem:wedge (all three already in the paper).
 - lem:tpw3-dual is lem:duality.
THE AUDIT'S OWN STATEMENT OF THE REAL GAP, worth carrying into round 14:
 MISSING: a nondegenerate stopping SSG on N = m^{O(1)} vertices whose
 improvement outmap is an AUSO of the m-cube with SUPERPOLYNOMIAL
 bottom-antipodal height.  Every family the route built (WD, WD3, WW, WW+, TW,
 TW2, TW4) has BA height 1 -- all-switches halts in one round on all of them.
 That is cor:f-auso / prop:auso-size again, and it is the pivot.

### ROUND 13, THE REST (not yet integrated; audits mixed)
- ueopl-promise: audits split (one True, one False).  THE FALSE ONE IS RIGHT and
  fatal: thm:up-lower's induction uses "l*Lambda <= D 4^{-(D+1)} < 4^{-D} <=
  4^{-l}", which is EQUIVALENT TO D < 4 and so false for every D >= 4.  Also its
  (PC-Poly) implication is false as stated -- it bounds only ACCEPTED JUMPS while
  the rule falls back to single steps.  DO NOT INTEGRATE the exponential-UEOPL-line
  claim until the induction is repaired.  Everything computational reproduced.
- softmax-homotopy: BLOCKED, and cleanly.  The regularisation error is EXACTLY
  the local defect times kappa(G) = the max expected number of visits to
  CONTROLLED vertices -- poly-time computable, replacing the naive N 2^a -- and
  the bound is ATTAINED, so beta = 2^{Omega(a)} is necessary.  The
  fixed-polynomial-temperature test is refuted in BOTH directions with the value
  at constant distance 1/4 from the threshold; same for the p-mean; and a
  UNIVERSAL AMPLIFIER LEMMA says no regulariser exact at average vertices can be
  coarser than 2^{-Omega(a)}.  thm:fold does NOT transfer (kappa(P_D) < 2, the
  entropic path crosses twice).  kappa is exponential on WD and CC, so the route
  is blocked exactly on the standing frontier.  WORTH INTEGRATING once audited --
  it closes the whole regularisation idea, not just the entropic one.
- newton-dinkelbach: both audits sound=False.  Headline is textbook
  (Radzik/Megiddo) with one SSG-specific line; rem:nd-linear-si states as
  established what its own gap leaves open.  Do not integrate the headline.
- free-search-13 (harmonic Green-kernel): both audits sound=False, and the rank
  method is Kannan-Theobald.  Do not integrate as new.
- schur-elimination: audit sound=False; the elimination is Meyer's stochastic
  complementation.  Attribute if used.
STILL RUNNING at this point: the symmetric-improvement and auso-pivot routes
(auso-pivot is THE pivot), plus the softmax and second two-player-wedge audits.

## ROUND 13 COMPLETE (wf_9a555369-4c3): 27 agents, 0 errors, 6.88M tokens, 3.1h
10 route results (nonlinear-perron ran twice, independently, and the two agree),
18 audits.  Verdicts: 8 strict-progress, 2 blocked.  ONLY 3 OF 18 AUDITS
sound=True -- the significance lens is doing heavy work.
frontier.tex 95 -> 114 pages, 237 -> 278 results across the session.

### INTEGRATED FROM ROUND 13 (each verified by me first)
1. sec:ratio + def:mobius + prop:ratio-closure (nonlinear-perron) -- see above.
2. thm:escape-class + prop:escape-family (nonlinear-perron run 2), family
   REPAIRED to Z_D after its audit; plus the survival-time reading
   sum_k S^k 1 <= kappa/(1-lambda).
3. thm:wedge-proved + cor:wedge-count (two-player-wedge, audit sound=True):
   prop:wedge is no longer a measurement.  K = 1,6,15,33,68,138,279,560.
4. prop:auso-seven (auso-pivot): a NONDEGENERATE TWO-PLAYER stopping SSG on 97
   vertices realising the height-7 AUSO of the 4-cube -- SETTLES the smallest
   concrete open instance rem:auso-size named.  Outmap
   (0,1,3,6,7,4,13,10,14,15,9,12,11,8,5,2), run 8->6->11->7->13->5->1->0,
   0 ties in 64 incidences, harmonic normal form over D=128 matching in all 84
   entries.  BOTH its audits were sound=False on OTHER results (a nondegeneracy
   hypothesis leaking out of its Holt-Klee lemma; a mis-stated gap) but both
   rebuilt this object and it survives.
5. def:bsi + thm:bsi-nostall + cor:bsi-correct + prop:bsi-nonstopping
   (symmetric-improvement): a rule carrying a PAIR, each player vetoing the
   other's switches, which NEVER STALLS on a stopping game -- lem:max-deficit's
   trap argument with w* replaced by val^tau.  No fallback clause, no barrier in
   the paper covers it, no superpolynomial family known.  Verified: 1184 pair
   states, 459 halting, 0 violations in both endorsement forms.

### DELIBERATELY NOT INTEGRATED, and why
- two-player-wedge's WW: its "two players" sit in NON-INTERACTING components of
  a disjoint union already used in thm:compare-equivalence; all-switches halts
  in one round.  sec:wedge's open item STANDS.
- ueopl-promise: thm:up-lower's induction uses an inequality equivalent to D<4.
- softmax-homotopy: BOTH audits unsound; cor:sm-no-reg ("no regulariser can be
  coarser than 2^{-Omega(a)}") is FALSE, refuted by an explicit M.  Its kappa is
  the RESOLVENT of my own survival operator, and bounded kappa already gives a
  poly algorithm unconditionally -- which is why its conditional path algorithm
  is worthless.
- newton-dinkelbach: headline is Radzik/Megiddo with one SSG-specific line.
- free-search-13 (harmonic rank class): both audits unsound; method is
  Kannan-Theobald.
- schur-elimination: elimination is Meyer's stochastic complementation.

### THE PIVOT, RESTATED AFTER ROUND 13
Realisability at m=4 is settled; what is missing is a FAMILY.  The audit's own
statement of the gap, and it corrected the route's: an operation with
|Vmax(G')| = |Vmax(G)| + O(1) and N(G') <= N(G)^c that doubles BA height is NOT
enough, because iterating gives N_k <= N_0^{c^k}.  What is needed is height
doubling at POLYNOMIAL total size cost.  One-way couplings are at best additive
(a +1 scheme attains it: heights 7,8,9,10 at m=4,5,6,7); multiplicative
composition is open.  Also settled: no stopping SSG with |Vmax| = 5 has an
all-switches run of length 13, so no game -- degenerate or not -- exceeds h*(m)
for m <= 5, and a degenerate escape needs |Vmax| >= 6.

## SESSION ef1cfad9 (2026-09-01 19:10 UTC, root on Fable 5.1). ROUND 14 LAUNCHED
State on arrival: frontier.tex 114 pp, 278 numbered results (58 thm, 43 lem,
40 prop, 20 cor, 44 def, 73 rem), `make pdf TEX=frontier` clean, git clean at
9f05e03 on branch ssg-frontier. A parallel Opus session (6a6140ad) with the
same user prompt tried to launch a round 14 three times at 18:44-18:59 and
every Workflow call failed at a PreToolUse hook timeout -- NO round 14 ran
there; the user confirmed "round-14 is never executed, start from scratch".
USER MODEL POLICY (see [[workflow-subagent-model]]): routes on Opus 5 by
default, at most 3 routes on Fable 5.1 for the hardest/most valuable, audits
always Opus 5.
Round 14 = runId wf_0aa30f91-0f7, task w450bja02, script
scratchpad/round14.js (66 KB), transcript dir
~/.claude/projects/-data-ssg-proof/ef1cfad9-.../subagents/workflows/wf_0aa30f91-0f7.
9 routes x 2 audits = 27 agents. Harness copied forward to scratchpad/root14/.
FABLE routes: bsi-rounds (round count of def:bsi, both directions);
 allsw-lower (a superpolynomial ALL-SWITCHES family on stopping SSGs -- told
 explicitly that Friedmann 2009/2011 (parity), Fearnley 2010 (MDP Howard) and
 the parity->MPG->DPG->SSG chain exist and may be reconstructed from own
 knowledge with attribution; success closes sec:wedge's open item via
 thm:seed-dichotomy and transfers through thm:normalform-barrier and
 thm:window-barrier); free-search-14 (anti-list + seeds: complementary-cone
 arrangement, self-duality at 1/2, sorting Vavg with abstaining comparators,
 the semialgebraic yes-set, algebraic complexity, double-obstacle/Isaacs).
OPUS routes: lasserre-2 (settle (v1) exactly, rational PSD certificates);
 lcp-handicap (P_*(kappa) sufficiency of the SSG LCP, exact small cases,
 growth on families, row/column sufficiency, hidden-K, Lyapunov stability);
 coin-bias (val_p as algebraic function of the coin bias, piece count,
 legitimacy reduction first); precondition (Doob h-transform of def:survival,
 decisive question + obstruction invariant, aggregation/multigrid);
 allsw-degeneracy (partial-orientation abstraction, degeneracy removal, new
 laws, f(6)/h*(6) bounds; told NOT to start another ./f2 job);
 free-search-b (proof complexity, counting/2-adic algebra, distinct-values
 parameter k, Richman, reductions).
Background job still running from 2026-08-28: ./f2 6 in scripts/ceiling
(f6.out best 25 so far; 6565 CPU-min). Leave it.

### ROOT-LEVEL BSI BASELINE (my own code, scratchpad/root14/bsi.py, t_bsi14b.py)
My own def:bsi implementation (val_sigma / val^tau by exact policy iteration
for the frozen player's opponent, asserted stopping; brute-force cross-check)
reproduces prop:bsi-nonstopping exactly and agrees with thm:bsi-nostall on
150 random two-player stopping games x 8 starts (0 violations, max 4 rounds).
OBSERVATION, easy to prove: on a ONE-PLAYER stopping game (Vmin empty)
U = val^tau = w* exactly, so the veto admits only w*-greedy switches; a
switched vertex becomes greedy and stays greedy (a later switch needs a tie);
and lem:max-deficit gives a wrong-and-strictly-switchable vertex every round,
which passes the veto. Hence the non-greedy set shrinks by >= 1 per round and
BSI halts within |Vmax| rounds -- on L_n in ONE round from all-first
(measured n <= 12; 112 random one-player runs, rounds - |Vmax| <= 0). So
BSI's whole content is the TWO-PLAYER veto; one-player instances (WD, CC,
H_m, L_n) cannot test it. The disjoint union L_n (+) dual(L_n) does not
couple the tracks either (BSI 1-4 rounds up to N = 43 vs all-switches n): a
BSI family must couple the tracks through shared vertices.

### ROUND 14 STOPPED EARLY AT THE USER'S REQUEST (token budget), 2026-09-01 ~20:0x UTC
TaskStop on task w450bja02 (runId wf_0aa30f91-0f7). Script:
/tmp/claude-1000/-data-ssg-proof/ef1cfad9-.../scratchpad/round14.js (66 KB) --
COPY IT SOMEWHERE PERSISTENT BEFORE THE SCRATCHPAD IS CLEANED. Journal with the
full route payloads:
~/.claude/projects/-data-ssg-proof/ef1cfad9-5d31-414e-ba8d-8fdf97a6d2ab/subagents/
workflows/wf_0aa30f91-0f7/journal.jsonl (25 lines, 6 results, agent-*.jsonl beside
it). resumeFromRunId is SAME-SESSION ONLY, so a later session must relaunch the
script fresh (routes rerun) -- but the six payloads below are already on disk and
can be digested without rerunning anything.
FIVE ROUTES RETURNED (none verified by me yet -- verify before integrating):
 - precondition (strict-progress): decisive question (b) answered NO
   unconditionally; claims a SIXTH polynomial class ("contracted", first-passage
   chain on C with self-returns removed) with family Y_D outside all five, and
   an exponential speed-up over plain VI on Y_D. Its correctness audit ALSO
   returned: sound, but prop:prec-Gm(b) is REFUTED (Lambda(WD(e,j,m)) is
   f(max(e,j)), not independent of j; 24/49 triples), thm:prec-rate is
   Blondel-Nesterov (NINTH rediscovery -- attribute), thm:prec-target is
   prop:bracket(d), prop:prec-onectrl is thm:decide-one-bit, prop:prec-block
   covers NO mechanism. Audit's integrate/repair/exclude list is in the journal.
 - free-search-b (strict-progress): "THE VALUE ALPHABET" -- val is the LEAST
   fixed point of the UP-ROUNDED Shapley operator on any finite grid containing
   it, arbitrary SSGs.
 - bsi-rounds (strict-progress): claims thm:bsi-nostall strengthens to a STRICT
   LEXICOGRAPHIC POTENTIAL (max gap, then |argmax|) on pairs -- i.e. a round
   bound. MUST BE AUDITED HARD: a polynomial bound here solves the problem.
 - coin-bias (dead-end): closed twice over.
 - free-search-14 (strict-progress): the one-player case of the missing
   all-switches family is the published open problem for Howard's rule.
 - allsw-lower, lasserre-2, lcp-handicap, allsw-degeneracy: NO result (killed
   mid-run); their agent transcripts are in the workflow dir.
MY OWN BSI HILL-CLIMBS were killed too; best found was 12 rounds at N=22 driven
by a Min chain, and a vertex CAN be switched twice (bsihunt2 found repeats=1),
so no "each vertex switches once" argument is available -- relevant to auditing
bsi-rounds' lexicographic potential.
