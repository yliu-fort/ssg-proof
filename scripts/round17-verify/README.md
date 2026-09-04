# Round-17 verification scripts

The root agent's own exact-arithmetic checks of claims made in round 17
(by routes or by the paper audit) before they entered `frontier.tex`.
Everything uses `fractions.Fraction`; nothing here imports the routes' or
auditors' code.

| Script | What it checks | Outcome |
| --- | --- | --- |
| `signdef_damping.py` | The paper audit's counterexample to the (now struck) claim in `rem:signdef` that the sign-definite class of `def:signdef` is closed under `def:damping`. Builds the 9-vertex stopping game, damps every edge by a chain of `m` average vertices exactly as `def:damping` prescribes, and recomputes `d^v` from the first-passage laws. | `G` is sign-definite (`d^v = (0,0,1/4)`); `G_m` is not for `m = 1..4` (`(0,-1/16,3/32)`, `(0,-9/128,45/256)`, ...), matching the closed form `(0, -l^2(1-l)/2, l^2(2-l)/4)`, `l = 1-2^-m`. |
| `bh_count.py` | `prop:blowup-height`'s former clause that a maximal-height set has `2^k` vertices: exhaustive over all 728 acyclic unique sink orientations of the 3-cube (self-contained USO / acyclicity / height code). | 32 orientations have a non-power-of-two number of maximal vertices (24 with six, 8 with seven); the auditor's example `(2,3,1,0,6,7,4,5)` has heights `(2,2,1,0,2,2,2,2)`. |
