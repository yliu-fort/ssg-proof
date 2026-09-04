"""Re-check the two surviving negative results against BOTH firing directions
of rem:own-successor:
  (i)  Delta(v, v^(i)) <= 0   -> v^(i) is optimal;
  (ii) Delta(v^(i), v) <  0   -> v^(i) is NOT optimal, so the other one is.
A preorder has no strictness, so only (i) is available to def:simorder.
"""
from mycore import G, wstar, Z01, slack_step, ones, check_sound, distinguishing
from myinst import G8, H_m


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
            if y < g.n:
                y0, y1 = g.succ[y]
                if g.kinds[y] == 'max':
                    ok = ok or (x, y0) in R or (x, y1) in R
                else:
                    ok = ok or ((x, y0) in R and (x, y1) in R)
            if not ok and x < g.n:
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


g = G8()
w = wstar(g)
R = simorder(g, w)
print('soundness violations of the preorder on G8:',
      sum(1 for (x, y) in R if w[x] > w[y]))
for v in distinguishing(g, w):
    a, b = g.succ[v]
    if g.kinds[v] == 'max':
        print(f'G8 v{v} (max) -> ({a},{b}): (i) ({v}<={a})={(v,a) in R} '
              f'({v}<={b})={(v,b) in R} -> fires {(v,a) in R or (v,b) in R}')
    else:
        print(f'G8 v{v} (min) -> ({a},{b}): (i) ({a}<={v})={(a,v) in R} '
              f'({b}<={v})={(b,v) in R} -> fires {(a,v) in R or (b,v) in R}')

print()
for m in (3, 4, 5, 6):
    g = H_m(m)
    w = wstar(g)
    L = 2 * m
    v = L + 1
    c1, h = 0, L
    N = g.N
    Z0, Z1 = Z01(g, w)
    D = ones(N)
    k1 = k2 = None
    for k in range(1, 400):
        Dn = slack_step(g, D, Z0, Z1)
        D = [[min(D[i][j], Dn[i][j]) for j in range(N)] for i in range(N)]
        check_sound(g, D, w, 'slack')
        if k1 is None and (D[v][c1] <= 0 or D[v][h] <= 0):
            k1 = k
        if k2 is None and (D[c1][v] < 0 or D[h][v] < 0):
            k2 = k
        if k1 and k2:
            break
    pair = [14, 38, 100, 249][m - 3]
    print(f'H_{m}: (i) fires at {k1};  (ii) fires at {k2};  pair test {pair}')
