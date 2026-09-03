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
