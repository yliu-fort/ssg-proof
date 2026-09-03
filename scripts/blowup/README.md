# The blow-up of thm:blowup: computations

Exact-arithmetic scripts behind `thm:blowup`, `rem:blowup-measured`,
`rem:blowup-realise` and `prop:gsharp-bigcube` of `frontier.tex`.

| file | what |
| --- | --- |
| `blowz.py`, `blowc.py` | the blow-up with translation by `sink xor start` (heights 4,10,22,46,94), with `1-bar` (D: 4,9,16,25,36), with reversal (4,10,16,23,30), with partial reversal (not acyclic) |
| `blowvar.py` | the rule family with value-readable readouts (linear growth) |
| `my_D.py` | the unit-vertex-capacity Holt-Klee test and the D operation |
| `bigcube.py` | the 6-cube orientation of G-sharp: USO, acyclic, Holt-Klee, height 5, sink projection = s_{G-sharp} |
| `km.py` | Klee-Minty cubes: bottom-antipodal height d for d <= 12 |
| `leap.py` | readable period-one signals along ladder runs |
| `huntG.py`, `huntW2.py` | integer normal-form searches (full orientation / walk only), after round 13's `hunt7.py` |
| `verifyG.py` | exact re-verification of a search candidate from the game |
| `G_m3_k0_den64_s{1,2}.json`, `B1_game.json` | two one-player realisations of the first level (height 4, dimension 3); the explicit 58-vertex game |
| `b2cube.py` | the blow-up of every AUSO of the 2-cube: Holt-Klee status and membership in the realised classes; the second level B^2 and its layer-00 incidence count |
| `AP_m4_k0_den256_s200.json`, `AP_m4_k0_den256_s200_game.json` | the one-player realisation (normal form, denominator 256; explicit 100-vertex game) of the blow-up of the 2-cube, height 6, whose layer 00 is the inner cube translated by 1-bar |
| `fastnf.py`, `nf2.py`, `build.py`, `verify.py`, `auso.py` | round-13 harness (normal form, gadget construction, verification) |

The Lean formalisation of the theorem is `lean/SSGProof/Blowup.lean`.
