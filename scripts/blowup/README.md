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
| `fastnf.py`, `nf2.py`, `build.py`, `verify.py`, `auso.py` | round-13 harness (normal form, gadget construction, verification) |

The Lean formalisation of the theorem is `lean/SSGProof/Blowup.lean`.
