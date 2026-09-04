#!/usr/bin/env python3
"""The query-model route's hidden decision path HDP_m(z) (def:qm-hdp), rebuilt from the definition:
for m = 2..5 and every z: stopping, one controlled skeleton, the value formula x_j = 1/4 + 2^{-j-1} (j < i),
1/4 (j >= i) with i = first index where sigma differs from z, S_sigma = {v_i}, Opt = {z}, and the oracle
answer (values at C and at the successors of C) a function of (sigma, i) only."""
import sys, itertools; sys.argv = ['x']
from fractions import Fraction as F
exec(open('ol_verify.py').read().split("def preorders(A):")[0])
def build(m, z):
    # non-sinks: v_1..v_m = 0..m-1; block j: e0,e1,x,y,s = m + 5(j-1) + (0..4); t0 = 6m, t1 = 6m+1
    n = 6 * m; t0, t1 = n, n + 1
    kinds = ['max'] * m + ['avg'] * (5 * m); succ = [None] * n
    for j in range(1, m + 1):
        base = m + 5 * (j - 1); e0, e1, x, y, s_ = base, base + 1, base + 2, base + 3, base + 4
        succ[j - 1] = (e0, e1)
        b = (e0, e1)[z[j - 1]]; c = (e0, e1)[1 - z[j - 1]]
        if j == 1:
            succ[b] = (t1, t0); succ[c] = (t0, x); succ[x] = (t1, t0); succ[y] = (t0, t0); succ[s_] = (t0, t0)
        else:
            succ[b] = (j - 2, x); succ[x] = (t0, y); succ[y] = (t1, t0); succ[c] = (t0, s_); succ[s_] = (t1, t0)
    return Game(kinds, succ)
for m in range(2, 6):
    skeletons = set(); ok = True; buckets = {}
    for z in itertools.product((0, 1), repeat=m):
        g = build(m, z); assert g.is_stopping()
        skeletons.add((tuple(g.kinds), tuple(g.succ[v] for v in g.C)))
        opt = None
        for sig in itertools.product((0, 1), repeat=m):
            x = g.value(dict(zip(g.C, sig)))
            i = next((j + 1 for j in range(m) if sig[j] != z[j]), m + 1)
            expect = [F(1, 4) + F(1, 2 ** (j + 2)) if j + 1 < i else F(1, 4) for j in range(m)]
            assert [x[v] for v in g.C] == expect, (m, z, sig, [str(x[v]) for v in g.C], [str(e) for e in expect])
            S = {v for v in g.C if x[g.succ[v][1 - sig[v]]] > x[v]}
            assert S == ({i - 1} if i <= m else set()), (m, z, sig, S, i)
            ans = tuple(x[v] for v in g.C) + tuple(x[g.succ[v][a]] for v in g.C for a in (0, 1))
            buckets.setdefault((sig, i), set()).add(ans)
        w = g.wstar(); assert [w[v] for v in g.C] == [F(1, 4) + F(1, 2 ** (j + 2)) for j in range(m)]
    assert len(skeletons) == 1 and all(len(b) == 1 for b in buckets.values())
    print(f'HDP_{m}: {2**m} members, N = {6*m+2}, all stopping, one controlled skeleton, value formula and S_sigma = {{v_i}} at every (z, sigma), Opt = {{z}}, the oracle answer a function of (sigma, i): {len(buckets)} classes, none ambiguous', flush=True)
