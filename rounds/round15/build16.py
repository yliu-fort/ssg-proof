#!/usr/bin/env python3
"""Build round15.js (the re-run) from the cancelled round15_cancelled.js:
patch COMMON with the solo-round state, keep six old routes (patched), add four new
ones, replace PAPER_SECTIONS, set SCRATCH, all models opus."""
import re, sys
SC = '/tmp/claude-1000/-data-ssg-proof/6e64b33d-520c-4c82-aa1b-ffb69ecfcb61/scratchpad'
src = open(f'{SC}/round15_cancelled.js').read()
new_routes = open(f'{SC}/routes16_new.js').read()

def must_replace(s, old, new, count=1):
    if old in s:
        return s.replace(old, new, count)
    pat = r'\s+'.join(re.escape(tok) for tok in old.split())
    m = re.search(pat, s)
    if not m:
        sys.exit(f'PATCH FAILED, not found: {old[:90]!r}')
    return s[:m.start()] + new + s[m.end():]

i_common = src.index('const COMMON = `')
i_schema = src.index('const ROUTE_SCHEMA = {')
i_routes = src.index('const ROUTES = [')
i_paper = src.index('const PAPER_SECTIONS = [')
i_prompt = src.index('const paperAuditPrompt = (s) => `')
i_lenses = src.index('const AUDIT_LENSES = [')
i_body = src.index('log(`Round 15:')
head = src[:i_common]
common = src[i_common:i_schema]
schemas = src[i_schema:i_routes]
routes_old = src[i_routes:i_paper]
prompt = src[i_prompt:i_lenses]
lenses = src[i_lenses:i_body]
body = src[i_body:]

# ---------------- head: meta + SCRATCH ----------------
head = must_replace(head,
  "description: 'Round 15 on the SSG value problem: 7 routes against the post-round-14 frontier (1 on Fable 5.1, 6 on Opus 5), each adversarially audited twice on Opus 5, plus an 8-part adversarial audit of frontier.tex itself on Opus 5',",
  "description: 'Round 15 (re-run) on the SSG value problem: 10 routes on Opus 5 against the post-solo-round frontier, each adversarially audited twice on Opus 5, plus six adversarial audits of frontier.tex itself on Opus 5',")
head = head.replace("const SCRATCH = '/tmp/claude-1000/-data-ssg-proof/3f223550-99d5-478f-855b-c1117c4a9d67/scratchpad'",
                    f"const SCRATCH = '{SC}'")
assert SC in head

# ---------------- COMMON ----------------
common = must_replace(common,
  '${REPO}/frontier.tex is a 131-page, 321-result LaTeX development built over\nfourteen prior multi-agent rounds.',
  '${REPO}/frontier.tex is a 137-page, 330-result LaTeX development built over\nfourteen prior multi-agent rounds and one solo round by the root agent (10856\nlines).')
common = must_replace(common, 'do NOT read all 540 KB.', 'do NOT read all 570 KB.')
common = must_replace(common,
  'lem:auso-laws, cor:f-auso: f(m) >= h*(m), the\ngreatest BA height of an AUSO of the m-cube, exponential in general\n(Schurr-Szabo, h*(m) >= 2^{floor(m/2)}, the document\'s only external input\nbesides thm:determinacy).',
  'lem:auso-laws, cor:f-auso: f(m) >= h*(m), the\ngreatest BA height of an AUSO of the m-cube, exponential in general -- PROVED\nHERE: thm:blowup (solo round, see below) gives h*(m+2) >= 2h*(m)+2, hence\nh*(m) >= 2^{m/2+1}-2; the Schurr-Szabo import is GONE and thm:determinacy is\nnow the document\'s ONLY external input.')
common = must_replace(common,
  'cor:seven-two-player: G#\'s orientation violates\nHolt-Klee (3 disjoint monotone source-sink paths where 4 are needed), so its\ntwo Min vertices are NECESSARY. Measured, unverified: h*_HK(4) = 6 < 7,\nh*_HK(5) = 11 < 12;',
  'cor:seven-two-player: G#\'s orientation violates\nHolt-Klee (TWO disjoint monotone source-sink paths on the 4-cube where 4 are\nneeded; max-flow 2, brute force over all 42 simple directed paths), so its\ntwo Min vertices are NECESSARY. h*_HK(4) = 6 < 7 is VERIFIED by the root agent\n(the height-7 orbit is G#\'s and is non-HK; the height-6 outmap\n0 1 3 2 5 14 7 4 13 10 11 12 9 6 15 8 is HK); h*_HK(5) = 11 < 12 is measured,\nunverified;')
common = must_replace(common,
  'WHAT IS MISSING: a family of stopping SSGs on N = m^{O(1)}\nvertices whose all-switches run has SUPERPOLYNOMIAL length -- equivalently,\nfor nondegenerate games, an SSG-realisable AUSO of superpolynomial BA height.\nEvery family built here (WD, CC, TW, ...) has BA height 1: all-switches halts\nin ONE round on all of them. One-way couplings of realisable AUSOs are at best\nADDITIVE (+1 per dimension: heights 7,8,9,10 at m = 4,5,6,7); an operation\nthat DOUBLES height at polynomial TOTAL size cost is what is open -- and\nN\' <= N^c per step is NOT enough (iterating gives N_0^{c^k}).',
  '''WHAT IS MISSING: a family of stopping SSGs on N = m^{O(1)}
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
   d <= 12 (km.py): LP-hard, BA-easy.''')
common = must_replace(common,
  '(v2) NOW PROVED as prop:oneplayer-lp. Unverified: h*_1(4) = 6, h*_HK(5) = 11.',
  '(v2) NOW PROVED as prop:oneplayer-lp. h*_HK(4) = 6 is verified; h*_1(4) = 6 is\n measured (every HK height-6 class realised, no non-HK one); h*_HK(5) = 11 is\n unverified.')
common = must_replace(common,
  'A ready harness is at ${SCRATCH}/root15/ :',
  'A ready harness is at ${SCRATCH}/root16/ :')
common = must_replace(common,
  'COPY what you need into ${SCRATCH}/<your-route>/ and\n   work there.',
  'The solo round\'s working directory is ${SCRATCH}/solo/ (realiseAP.py,\n   sampleAP.py, ap_es.py, ap_lp.py, ap_realise.py, blowz.py, blowc.py,\n   blowvar.py, blowhk.py, blowind.py, my_D.py, my_super.py, bigcube.py, km.py,\n   leap.py, lv1.py, rowgame.py, huntG.py, huntW2.py, verifyG.py, fastnf.py,\n   nf2.py, build.py, verify.py, b2cube.py, census/classes4.txt,\n   survey_*.json, AP_m4_k0_*.json = exact one-player games realising 4-cube\n   classes, B1_game.json, the *_game.json files = explicit games) and the\n   committed subset is ${REPO}/scripts/blowup/. COPY what you need into\n   ${SCRATCH}/<your-route>/ and work there.')
common = must_replace(common,
  '5. Return paste-ready LaTeX for what you PROVED, in the amsthm style of\n   frontier.tex, labels prefixed by your route name.',
  '5. Return paste-ready LaTeX for what you PROVED, in the amsthm style of\n   frontier.tex, labels prefixed by your route name.\n6. NO WEB. Do not use WebSearch, WebFetch or any network access. Use your own\n   knowledge and your own computation only. Attribute prior art from memory\n   and flag it as "from memory, unchecked against the source".\n7. TIME. You have a long budget but not an unbounded one: budget your\n   computations (background long runs with nohup and poll them; keep each\n   foreground command under ten minutes), and return a complete structured\n   result even if a computation is still running -- say what is running and\n   where its output goes.')
common = common.replace('${SCRATCH}/root15/', '${SCRATCH}/root16/')
assert 'root15' not in common, 'root15 left in COMMON'

# ---------------- old routes: extract by key and patch ----------------
def route_block(key):
    i = routes_old.index(f"    key: '{key}',")
    i = routes_old.rfind('  {\n', 0, i)
    j = routes_old.index('  },\n', i) + len('  },\n')
    return routes_old[i:j]

hc = route_block('howard-cube')
hc = must_replace(hc,
  '(the round-14 measurements 6 and 11 are unverified: reproduce them with\n     your own max-flow test on every face, the paper\'s test is described in\n     cor:seven-two-player)',
  '(h*_HK(4) = 6 is verified by the root agent; h*_HK(5) = 11 is NOT:\n     reproduce it with your own max-flow test on every face, validated on\n     the 12 AUSOs of the 2-cube and on the 656 Holt-Klee AUSOs of the\n     3-cube)')
hc = must_replace(hc,
  'QUESTIONS, in order.\n (1) THE CLASSICAL DEFORMED CUBES.',
  '''ALREADY DONE by the root agent -- do not redo, build on it. Klee-Minty
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
 (1) THE CLASSICAL DEFORMED CUBES.''')
hc = must_replace(hc,
  'Report h*_1(m) := the greatest BA height realised by a nondegenerate\n     one-player stopping SSG, for m <= 4 at least, with certificates.',
  'Report h*_1(m) := the greatest BA height realised by a nondegenerate\n     one-player stopping SSG: at m = 4 the survey gives 6 (certificates in\n     ${SCRATCH}/solo/AP_m4_k0_*.json); extend to m = 5 -- is the h*_HK(5) = 11\n     witness one-player realisable (realiseAP.py with m = 5, k = 0, a long\n     budget)? And compute h*_HK(6) if you can: a census is infeasible at\n     m = 6, but Holt-Klee is inherited by faces, so build from HK 5-faces.')
hc = must_replace(hc,
  '(3) THE SCHURR-SZABO BLOW-UP AND HOLT-KLEE. Write down the Schurr-Szabo\n     blow-up exactly (dimension +2, height at least doubled) and the round-14\n     operation D (allswlower:prop-search(a)). Determine whether EITHER\n     preserves Holt-Klee; if neither does, prove a lemma saying WHY (which\n     face fails the disjoint-paths count, as a function of the seed). If some\n     variant preserves Holt-Klee, that is the first candidate for an\n     LP-realisable exponential family and you should push it towards (2).',
  '(3) THE BLOW-UP AND HOLT-KLEE. thm:blowup\'s B (dimension +2, height 2h+2)\n     and prop:D-quadratic\'s D are in the paper and in ${SCRATCH}/solo/blowz.py,\n     my_D.py. B(2-cube) is Holt-Klee; B^2 = B(B(1-cube)) and D from\n     dimension 5 are not. Prove a lemma saying WHY (which face fails the\n     disjoint-paths count, as a function of the seed and of z), and\n     determine whether ANY dimension-raising operation that at least doubles\n     height can preserve Holt-Klee -- blowhk.py found none in B\'s rule\n     family, but products (lem:hstar-super), Klee-Minty-type deformations\n     and operations raising the dimension by 3 or 4 were not tried. An\n     HK-preserving doubling is the first candidate for an LP-realisable\n     exponential family and should be pushed towards (2).')

sp = route_block('sink-projection')
sp = must_replace(sp,
  'TASKS.\n (1) THE BIG CUBE.',
  'ALREADY DONE for G# by the root agent: prop:gsharp-bigcube and\nrem:gsharp-bigcube (${REPO}/scripts/blowup/bigcube.py) -- the 6-cube\norientation of G# is nondegenerate, USO, acyclic, Holt-Klee, of BA height 5,\nand its sink projection is exactly s_{G#}. Start from that code and do the\nGENERAL theory; the concrete instance your theory must be tested on is\nB^2 = B(B(1-cube)) (5-cube, height 10, non-HK; outmap in the briefing above):\nwhat is the least k for which B^2 can be the sink projection of a Holt-Klee\nUSO of the (5+k)-cube, and of one of the special P-LCP form SSGs produce?\n\nTASKS.\n (1) THE BIG CUBE.')
sp = must_replace(sp,
  'Verify on G#: is\n     s_C on the 6-cube Holt-Klee (it must be if GMR applies)? Is it acyclic?\n     Print it.',
  'G# is done (prop:gsharp-bigcube); verify instead on 200 random stopping\n     games, and on the one-player games B1_game.json and\n     AP_m4_k0_den256_s200_game.json in ${SCRATCH}/solo/ (one player: the big\n     cube IS the Max cube and must be Holt-Klee).')

vr = route_block('verify-r14')
vr = must_replace(vr,
  'and\n     allswlower:prop-search(a): the operation D and its heights 4, 9, 16, 25\n     at m = 3, 5, 7, 9 -- recompute the outmaps, check USO, acyclicity, both\n     laws, the BA heights, and the Holt-Klee violations at m = 5, 7 with your\n     own max-flow test.',
  '. The operation D of allswlower:prop-search(a) is INTEGRATED as\n     prop:D-quadratic and verified by the root agent -- skip it.')
vr = must_replace(vr,
  'deg:lem-super (h*(k+l) >=\n     h*(k) + h*(l), so h*(6) >= 13 -- PROVE it: it should be a product\n     construction), ',
  'deg:lem-super is INTEGRATED as lem:hstar-super with the root agent\'s\n     own construction and proof -- skip it; ')
vr = must_replace(vr,
  'Order the items by\nvalue: (2) deg:lem-super and (4) Q_16 first, then (1), (3), (5), (6).',
  'Order the items by\nvalue: (4) Q_16 and (2) deg:prop-hk5 / deg:prop-nondeg4 / deg:prop-zeroties\nfirst, then (1), (3), (5), (6).')

routes_new = 'const ROUTES = [\n' + new_routes + hc + sp + route_block('rbr-rounds') + route_block('treewidth') + route_block('free-search-15') + vr + ']\n\n'
routes_new = routes_new.replace('${SCRATCH}/root15/', '${SCRATCH}/root16/')
assert 'root15' not in routes_new
assert "model: 'fable'" not in routes_new

paper_new = '''const PAPER_SECTIONS = [
  { key: 'classes', lines: '1124-2684', what: 'sec:special: lem:descent, thm:few-avg, rem:few-avg-tight, def:escape, lem:descent-refined, lem:certificate, thm:few-escape, prop:fk-family, def:survival, lem:survival, thm:escape-class, def:survival-rate, lem:escape-rate, prop:escape-family, rem:escape-class, def:jump, lem:jump-acyclic, lem:det-game, thm:avg-acyclic, thm:player-free, thm:one-player, def:payoff, lem:successor-closed, lem:cut, lem:residual, thm:kacyclic, prop:kacyclic-strict, rem:owner-blind; sec:alphabet: def:alphabet, thm:alphabet-iteration, rem:alphabet-down, cor:grid-iteration, lem:alphabet-cover, thm:alphabet-rigid, cor:alphabet-chain, thm:alphabet-denominator, thm:few-denominator, rem:alphabet-compare, prop:alphabet-four, prop:fv-family, rem:alphabet-equivalence' },
  { key: 'allswitches', lines: '3206-4564', what: 'sec:allsw-laws: lem:monotone-law, rem:monotone-law-general, prop:closed-now-or-never, thm:peak-law, cor:no-return, cor:law-b, cor:antichain, def:maxreach, thm:component-bound, thm:bounded-components, prop:k1-family, prop:overshoot-small; the AUSO identification: def:improvement-uso, prop:allsw-auso, lem:auso-laws, def:flat, lem:trichotomy, lem:flat-class, lem:face-sink, thm:flat-resolution, cor:ceiling-general, cor:law-u, rem:flat, cor:f-auso, rem:f-auso, prop:auso-size, prop:auso-seven and its printed normal form, prop:oneplayer-lp, cor:seven-two-player, prop:gsharp-bigcube, prop:auso-census, prop:hstar-five; and the NEVER-AUDITED solo-round material lem:hstar-super, prop:D-quadratic, thm:blowup (reconstruct its proof in full: the unique-sink case analysis, the acyclicity argument with the parity conflicts of outer cycles, the walk of length 2h+2, and the numerical bounds), rem:blowup-measured and rem:blowup-realise -- recompute the heights 4,10,22,46,94 / 2,6,14,30 / 7,16,34,70 / 12,26,54,110 with your own code, the Holt-Klee status of B(1-cube) and of B^2, the 58-vertex realisation (verify it FROM THE GAME), and check the claim that the translation vector is a single coordinate, the alpha introduced two dimensions earlier, against the definition z = o xor u -- which coordinate is it at the second level when the seed height is odd? Also check whether rem:blowup-realise is consistent with the fact, found after it was written, that B(2-cube) is Holt-Klee and realised by a one-player game' },
  { key: 'refutations', lines: '4564-6430', what: 'def:ladder, thm:ladder, rem:ladder, thm:switch-count, cor:no-height, prop:serialiser; sec:residue (lem:trapchar, def:residue, thm:residue-correct, prop:residue-ladder, lem:normalform, thm:normalform-barrier, lem:splice, prop:a-presentation, def:freeze, prop:freeze-sound, prop:freeze-escapes, def:kblind, lem:kblind, def:window, thm:window-barrier); def:bsi through rem:bsi (thm:bsi-nostall, lem:bsi-pairloc, cor:bsi-levels, prop:bsi-twice, rem:bsi-gap, prop:bsi-oneplayer, cor:bsi-correct, prop:bsi-br, rem:bsi-br, prop:bsi-nonstopping); thm:cyclic-uso, cor:no-potential, thm:vi-lower, thm:hamming-refuted, cor:hamming, prop:rules-fail, prop:needle, lem:readonce, prop:no-submodular' },
  { key: 'calculi', lines: '7185-8714', what: 'sec:gap (def:rule, def:missing, thm:gap-equivalence, def:decision-rule, thm:decide-one-bit, prop:locality, prop:pdc-separation), sec:simorder (def:simorder, thm:simorder-sound, prop:simorder-stalls), sec:slack (def:slack, thm:slack-sound, prop:slack-repairs, thm:slack-barrier, cor:slack-stalls, thm:slack-vi-upper, def:trans-slack, thm:trans-sound, prop:trans-Hm, thm:trans-complete, lem:phi-certificate, prop:trans-stall, def:separable, lem:separable-lower, thm:separable, cor:separable, cor:set-certificate), sec:ratio (def:homog, prop:cw, def:ratio, thm:ratio-sound, thm:ratio-sandwich, cor:ratio-complete, cor:ratio-stall, prop:ratio-incomparable, def:mobius, prop:mobius, prop:ratio-closure)' },
  { key: 'hybrid', lines: '8714-10635', what: 'sec:matching-barrier (def:lmc, lem:fooling-partner, thm:matching-barrier), sec:seeded (def:seeded, thm:seeded-sound, thm:seeded-barrier, thm:seed-dichotomy, prop:seeded-decides), sec:transport (def:transport, thm:transport-sound, lem:transport-exact, prop:transport-decides, lem:transport-dim, thm:transport-objective, def:lasserre-two, thm:lasserre-vacuous, rem:lcp, prop:transport-stalls, rem:own-successor, prop:own-stall, thm:transport-barrier), sec:fold (thm:fold), sec:hybrid (def:hybrid, thm:hybrid-sound, lem:hybrid-fix, lem:gen-comparison, thm:hybrid-complete, cor:hybrid-sink, prop:hybrid-decides, prop:hybrid-onectrl, prop:hybrid-rate, lem:hybrid-cutting, thm:hybrid-convex-barrier, thm:hybrid-lower), sec:wedge (lem:wedge-face, cor:wedge-cert, def:wedge, prop:wedge, def:wedge-chain, lem:wedge-verts, thm:wedge-proved, cor:wedge-count, rem:wedge)' },
  { key: 'summary', lines: '10635-10856 together with 1-343', what: 'sec:summary and the front matter READ AGAINST THE BODY: every claim in the abstract, the introduction, "what is proved and what is not" and the summary must match the statement it cites, with the same hypotheses, the same numbers (vertex counts, round counts, the lists of six classes and six mechanisms, the count of prior-art attributions, the statement that thm:determinacy is the ONLY external input and that the Schurr-Szabo import is gone) and the same strength (measured vs proved); list every mismatch. Also check whether the abstract, the introduction and the summary say what the body now justifies about thm:blowup, lem:hstar-super, prop:gsharp-bigcube and the realised first level, and flag what they omit or overstate' },
]

'''

body = re.sub(r"log\(`Round 15: .*?\n", "log(`Round 15 (re-run): ${ROUTES.length} routes, all on Opus 5: ${ROUTES.map(r => r.key).join(', ')}; two audits each on Opus 5; ${PAPER_SECTIONS.length} paper audits on Opus 5.`)\n", body, count=1)
assert 'Fable' not in body
prompt = prompt.replace('${SCRATCH}/root15/', '${SCRATCH}/root16/')
lenses = lenses.replace('${SCRATCH}/root15/', '${SCRATCH}/root16/')
body = body.replace('${SCRATCH}/root15/', '${SCRATCH}/root16/')

out = head + common + schemas + routes_new + paper_new + prompt + lenses + body
assert 'root15' not in out, 'root15 remains'
assert "'fable'" not in out
open(f'{SC}/round15.js', 'w').write(out)
print('wrote', len(out), 'bytes;', out.count('`'), 'backticks')
for k in ['gadget','monotone-lemma','degenerate','lane-reuse','howard-cube','sink-projection','rbr-rounds','treewidth','free-search-15','verify-r14']:
    assert f"key: '{k}'" in out, k
print('routes ok')
