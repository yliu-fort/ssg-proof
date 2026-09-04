#!/usr/bin/env python3
"""M7 on BC(2,5) (scripts/round17-verify/BC_2_5.json): the round at which it first decides a controlled vertex, with the
free Z-seed, all three readings, cuts at the 8|C| lexicographic optima each round (the convex-class route said round one,
its correctness auditor round two)."""
import sys, os as _os, json
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from hz_w7 import *   # runs the seven-vertex check on import, then exposes the helpers
bc = json.load(open('/data/ssg-proof/scripts/round17-verify/BC_2_5.json'))
g = G(bc['kinds'], [tuple(s) for s in bc['succ']]); w = wstar(g); L, U, Z0, Z1 = seeds(g, w)
C, rows, B = Bmatrix(g); assert psd(B)[0]
A, b = transport_rows(g, L=L, U=U); n = g.n
for rnd in range(4):
    r = readings(g, w, A, b); dec = {v: f for v, f in r.items() if f}
    print(f'BC(2,5) round {rnd}: decided {dec}')
    if dec: break
    A1, b1 = list(A), list(b)
    for v in C:
        for a in g.succ[v]:
            gvec = [F(0)] * n; gvec[v] -= 1
            if a < n: gvec[a] += 1
            for sg in (1, -1):
                for sg2 in (1, -1):
                    c = [sg * x for x in gvec]; second = [F(0)] * n; second[v] = F(sg2)
                    x = opt_point(A, b, n, c, second); xs = x + [F(0), F(1)]
                    q, grad = q_and_grad(g, C, xs)
                    if q > 0:
                        rhs = sum(grad[i] * x[i] for i in range(n)) - q
                        assert sum(grad[i] * w[i] for i in range(n)) <= rhs
                        A1.append(list(grad)); b1.append(rhs)
    print(f'   cuts added this round: {len(A1)-len(A)}')
    A, b = A1, b1
