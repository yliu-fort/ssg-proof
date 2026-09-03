# Round-15 verification scripts (root agent)

Independent exact-arithmetic checks of the round-15 route claims integrated
into `frontier.tex`.  All use Python `fractions`; none uses greedy policy
iteration (val_sigma is always the componentwise minimum over all positional
Min strategies).

- `hk_product.py` — lem:hstar-super product of the h*_HK(5)=11 witness with
  the 1-cube (witness first, z=1): Holt--Klee, heights 12 and 13
  (rem:four-ceilings, the sentence after prop:hkfive); the other order fails
  Holt--Klee.
- `rd_sd_check.py` — the readout cascade RD(n), n<=5: all-switches 1 round,
  R_BR n rounds (all best responses, both variants), BSI 2n (thm:readout).
- `sd_check.py` — the leapfrog SD(K) as a one-player game (K<=6, v switched
  K times) and its two-player self-dual form (K<=4) (prop:leapfrog).
- `gad_check.py` — gad:xor (i)-(iii) from the printed 100-vertex normal form
  and the turn witnesses of cor:b2-rows.
- `b2_profile.py` — the 6-cube of profiles of the 138-vertex B^2 game:
  profile-nondegenerate, USO, acyclic, Holt--Klee, height 9
  (sec:projection).  Needs `../blowup/B2_small_GAME.json`.
- `verify_b2.py`, `verify_games.py`, `hc_oneplayer.py`, `stack_parity.py`,
  `seven_flat.py`, `rise_bound.py`, `top_check.py`, `rbr_gsharp.py` — the
  checks recorded in the paper as "reproduced here" for prop:b2-realised,
  prop:m3-realised, prop:oneplayer-runs, lem:stack, lem:seven-flat,
  lem:rise-bound / cor:peak-sharp, thm:top and rem:bsi-br.
- `tw_check.py` — the grid Tarski search + rounding + continued-fraction
  recovery of sec:width on random stopping games with a frozen feedback set
  (thm:modulator's chain), 25/25 exact.
- `mn_check.py` — the family M_n (prop:modulator-family): stopping,
  reachability, val(h), the Max-cycle claim.
- `q16_check.py` — Q_16 (prop:q16) from its printed rows: both BSI variants.
- `glaw.py` — the three-law ceiling g(m)=1,2,4,7,12 (rem:flat).
