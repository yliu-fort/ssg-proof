#!/usr/bin/env python3
"""M1 (def:simorder's greatest fixed point, the root's own code t_standing.simorder) on BC(e,s):
the four order tests of rem:own-successor at v0, v1, v2 -- (v, v^i) in R (clause i) and the pair
tests (v^{1-i}, v^i) in R; (x,y) in R means x <= y, i.e. w*(x) <= w*(y)."""
import sys, json, time
sys.path.insert(0, '../root16')
from mycore import G, wstar
from t_standing import simorder
for fn in sys.argv[1:]:
    d = json.load(open(fn)); names = d['names']; kinds = d['kinds']; succ = [list(x) for x in d['succ']]
    g = G(kinds, succ); w = wstar(g); n = len(kinds); t = time.time()
    R = simorder(g, w)
    # soundness of R against w*
    assert all(w[x] <= w[y] for (x, y) in R), 'unsound preorder'
    C = [i for i in range(n) if kinds[i] != 'avg']
    out = {}
    for v in C:
        a, b = g.succ[v]
        out[names[v]] = {'(v,a)': (v, a) in R, '(v,b)': (v, b) in R, '(a,b)': (a, b) in R, '(b,a)': (b, a) in R}
    trans = all((x, z) in R for (x, y) in R for (y2, z) in R if y == y2)
    print(f"{fn.split('/')[-1]} (N={n+2}): |R| = {len(R)}, sound, transitive = {trans}; tests {out}  [{time.time()-t:.0f}s]", flush=True)
