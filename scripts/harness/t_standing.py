"""Apply the standing rule to the OTHER mechanisms' published stalls.

At v in Vmax we always have w*(v) >= w*(v^(i)); so a derivation of
w*(v) <= w*(v^(i)) forces EQUALITY and proves v^(i) optimal.  Hence:
  simulation preorder (def:simorder): v <= v^(i) decides v;
  slack calculus (def:slack):        Delta(v, v^(i)) <= 0 decides v  (NON-strict).
Dually at Min vertices.  Both are weaker demands than the published pair tests,
so the published stalls must be re-checked against them.

Instances: G_8, on which prop:simorder-stalls refutes the preorder via the pair
(4,1); and H_m, on which cor:slack-stalls says the slack calculus needs
2^{Omega(N)} rounds for the pair (h, c_1).
"""
from fractions import Fraction as F
from mycore import (G, wstar, Z01, slack_step, minplus_close, clamp, ones,
                    check_sound, distinguishing)
from myinst import G8, H_m


# ---- the value-simulation preorder of def:simorder, as a greatest fixed point
def simorder(g, w):
    N = g.N
    Z0, Z1 = Z01(g, w)
    R = {(x, y) for x in range(N) for y in range(N)}
    while True:
        nxt = set()
        for (x, y) in R:
            if x in Z0 or y in Z1:
                nxt.add((x, y))
                continue
            ok = False
            if y < g.n:                                   # (down)
                y0, y1 = g.succ[y]
                if g.kinds[y] == 'max':
                    ok = ok or (x, y0) in R or (x, y1) in R
                else:
                    ok = ok or ((x, y0) in R and (x, y1) in R)
            if not ok and x < g.n:                        # (up)
                x0, x1 = g.succ[x]
                if g.kinds[x] == 'min':
                    ok = ok or (x0, y) in R or (x1, y) in R
                else:
                    ok = ok or ((x0, y) in R and (x1, y) in R)
            if not ok and x < g.n and y < g.n and g.kinds[x] == g.kinds[y]:
                x0, x1 = g.succ[x]
                y0, y1 = g.succ[y]
                k = g.kinds[x]
                if k == 'max':
                    ok = all(any((xi, yj) in R for yj in (y0, y1)) for xi in (x0, x1))
                elif k == 'min':
                    ok = all(any((xi, yj) in R for xi in (x0, x1)) for yj in (y0, y1))
                else:
                    ok = (((x0, y0) in R and (x1, y1) in R)
                          or ((x0, y1) in R and (x1, y0) in R))
            if ok:
                nxt.add((x, y))
        if nxt == R:
            return R
        R = nxt


print('=== simulation preorder on G_8 (prop:simorder-stalls) ===')
g = G8()
w = wstar(g)
R = simorder(g, w)
bad = [(x, y) for (x, y) in R if w[x] > w[y]]
print('  soundness violations:', len(bad))
for v in distinguishing(g, w):
    a, b = g.succ[v]
    pair = ((a, b) in R, (b, a) in R)
    own = ((v, a) in R, (v, b) in R) if g.kinds[v] == 'max' else ((a, v) in R, (b, v) in R)
    print(f'  v{v} ({g.kinds[v]}) -> ({a},{b}) values {w[a]},{w[b]}')
    print(f'     pair test  {a}<={b}? {pair[0]}   {b}<={a}? {pair[1]}  -> decides {pair[0] or pair[1]}')
    print(f'     own-successor test {own}  -> decides {own[0] or own[1]}')

print()
print('=== slack calculus on H_m (cor:slack-stalls): pair vs own-successor ===')
for m in (3, 4, 5, 6):
    g = H_m(m)
    w = wstar(g)
    L = 2 * m
    v = L + 1
    c1, h = 0, L
    N = g.N
    Z0, Z1 = Z01(g, w)
    D = ones(N)
    kpair = kown = None
    for k in range(1, 400):
        Dn = slack_step(g, D, Z0, Z1)
        D = [[min(D[i][j], Dn[i][j]) for j in range(N)] for i in range(N)]
        check_sound(g, D, w, 'slack')
        if kpair is None and D[h][c1] < 0:
            kpair = k
        if kown is None and D[v][c1] <= 0:
            kown = k
        if kpair and kown:
            break
    print(f'  H_{m}: N={g.N}  pair test Delta(h,c1)<0 at round {kpair};  '
          f'own-successor Delta(v,c1)<=0 at round {kown}')
