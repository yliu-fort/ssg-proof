#!/usr/bin/env python3
"""Root agent's check of the round-17 oracle-barrier route's family BC(e,s) with the ROOT'S OWN round-16
harness (written from the paper's definitions): w* by brute force against the file, the Z-seeded
own-successor hybrid (ownhyb.hybrid_rounds: both clauses of rem:own-successor at every controlled
vertex, seeded with Z_0, Z_1) and def:ratio (ratio.ratio_rounds, both clauses), recording the first
firing round at v0, v1, v2.  The route claims silence of every member of its model for K+1 operator
applications, K+1 = 2, 5, 11 at (e,s) = (2,5), (3,5), (4,5), and measured silence of the slack, closure
and ratio calculi for ten rounds on BC(2,5)."""
import sys, json, time
sys.path.insert(0, '../root16')
from fractions import Fraction as F
from mycore import G, wstar, Z01
from ownhyb import hybrid_rounds
from ratio import ratio_rounds, INF, sound
for fn in sys.argv[1:]:
    d = json.load(open(fn)); names = d['names']; kinds = d['kinds']; succ = [list(x) for x in d['succ']]
    g = G(kinds, succ); w = wstar(g); n = len(kinds)
    assert [str(x) for x in w[:n]] == d['wstar'][:n], 'w* mismatch'
    Z0, Z1 = Z01(g, w)
    C = [i for i in range(n) if kinds[i] != 'avg']
    gaps = {names[v]: str(abs(w[succ[v][0]] - w[succ[v][1]])) for v in C}
    print(f"{fn.split('/')[-1]}: N = {n+2}, e = {d['e']}, s = {d['s']}, stopping = {g.N > 0}, w*(v0,v1,v2) = {[str(w[v]) for v in C]}, successor gaps {gaps}, Z0 = {[names[x] if x < n else ('t0','t1')[x-n] for x in sorted(Z0)]}, Z1 = {[names[x] if x < n else ('t0','t1')[x-n] for x in sorted(Z1)]}", flush=True)
    t = time.time(); K = {2: 4, 3: 3, 4: 3}[d["e"]]
    first, dist = hybrid_rounds(g, w, K=K, seeded=True)
    print(f"  Z-seeded own-successor hybrid, {K} rounds: distinguishing vertices {[names[v] for v in dist]}, first firing {{ {', '.join(f'{names[v]}: {first.get(v)}' for v in C)} }}  [{time.time()-t:.0f}s]", flush=True)
    t = time.time(); KR = 60
    Rs = ratio_rounds(g, w, KR); firstR = {}
    for k, R in enumerate(Rs, 1):
        assert sound(g, R, w) == 0, ('unsound', k)
        for v in C:
            if v in firstR: continue
            c1 = [u for u in g.succ[v] if R[v][u] is not INF and R[v][u] <= 1]
            c2 = [u for u in g.succ[v] if R[u][v] is not INF and R[u][v] < 1] if v not in Z0 else []
            if c1 or c2: firstR[v] = (k, '(i)' if c1 else '(ii)')
    print(f"  def:ratio, {KR} rounds, both clauses: first firing {{ {', '.join(f'{names[v]}: {firstR.get(v)}' for v in C)} }}  [{time.time()-t:.0f}s]", flush=True)
