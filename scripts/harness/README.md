# The root agent's exact-arithmetic harness

The Python modules that every `scripts/round1N-verify/` script imports
(`mycore.py`: the class `G(kinds, succ)` with non-sinks `0..n-1`, `t0 = n`,
`t1 = n+1`; `profile_value`, `wstar` by brute force over positional pairs,
the trap-based `is_stopping`, `T_op`, `Z01`, `slack_step`, `minplus_close`,
`transport_rows` / `transport_sep`, `hybrid`; `zseed.py`: the free `Z_0/Z_1`
seed; `ownhyb.py`: the own-successor hybrid; `ratio.py`, `mobius.py`: the
multiplicative calculus; `lp.py`, `mylp.py`: exact two-phase simplex (Bland);
`auso.py`, `census/`: USO/AUSO predicates and bottom-antipodal walks;
`normform.py`: the harmonic normal form; `my_D.py`: the Holt--Klee test by
max-flow; `myinst.py`, `gstar.py`, `wd.py`, `cc.py`: the paper's instances;
`hyb2d.py`, `rathyb.py`: exact two-dimensional polygon engines for
`|C| = 2`). Everything uses `fractions.Fraction`. Copied here in round 18 from
the session scratchpads (`root16/`, `solo/`) so that the verification scripts
run from a checkout:

```bash
cd scripts/round17-verify && PYTHONPATH=../harness python3 bc_m1.py BC_2_5.json
```

The round-18 scripts locate the harness through `scripts/harness/` relative
to their own directory, with the scratchpad path as a fallback.
