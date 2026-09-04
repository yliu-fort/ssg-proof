# Round-16 verification scripts (root agent)

Exact-arithmetic re-verifications behind the round-16 repairs and integrations
of `frontier.tex`.

| file | what |
| --- | --- |
| `sparse_verify.py` | sparse exact solver (dict rows, min-degree pivots) verifying a game file: stopping, ties, outmap, USO, acyclicity, height, run; 256 profiles of a 194-vertex game in 8 s |
| `TB_GAME_D10.json` | the round-16 b3 route's 194-vertex game (7 Max, 1 Min, 184 average) realising the relaxed level-three target $B_{p,0}(B^2)$, height 12 (verified from the game) |
| `b3.py`, `B3.json` | $B^3=B(B^2)$: 7-cube, height 22, not Holt--Klee, translation coordinate $\alpha_2$ |
| `free_parity.py` | the blow-up with an arbitrary parity function and translation vector is an AUSO with the predicted sink and walk length (240 random cases) |
| `kn_escape.py` | $K_n$ of `prop:k1-family` carries the constant escape certificate $\lambda=19/20$ ($n\le40$) |
| `mn_escape.py` | $M_n$ of `prop:modulator-family`: escape exponent $n+1$, denominator $2^{n+1}$, unique optimal strategy ($n=3,4,5$) |
| `m3_one_min.py`, `m3games/G_m3_k1_*.json` | both non-Holt--Klee classes of the 3-cube realised with one Min vertex (145 and 86 vertices), verified from the game |
| `m3games/game_m3_*.json`, `X3a_170_game.json`, `X3c_98_game.json`, `B1_39_game.json` | the round-15 monotone route's eighteen realisations behind `prop:m3-realised` (sixteen one-player, two with six Min vertices) and its 39-vertex first-level game |
| `fs16_check.py`, `fs16_gate2.py` | the gate composition lemma (case-split operator: 49 compositions, 0 mismatches; the "max over two chance actions" form fails when $q>p$), the energy identity (40 games) and mixed-Min monotonicity (22 games) |
| `fl_check.py` | $\mathrm{FL}(D)$: $2^D$ response pieces with slopes $\{0,2^{-D}\}$ at $D\le4$ |
| `cv_build.py`, `cv_hybrid.py`, `cv_ratio.py`, `cv_width.py` | $\mathrm{CV}(e,s)$ of `def:cv`: $N$, stopping, $D(G)=2^{s}$ and the gap $1/D$ at $v_0$ (values by brute force over the eight Max profiles); the Z-seeded own-successor hybrid fires at round 4 on $\mathrm{CV}(1,4)$; the ratio calculus of `def:ratio` with **both** clauses of `rem:own-successor` fires at $v_0$ through clause (ii) at rounds $12,22,39,74$ ($s=4$) and $10,16,26,44$ ($s=3$), $e=1,\dots,4$ --- the finding that struck M6 from the route's stall claim; the width $\max_{K(\Delta_k)}(z(v_1)-\tfrac12)$ per hybrid round against the law $\lambda^{k-1}/2$ |
