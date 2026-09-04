#!/usr/bin/env python3
"""The convex-class route's M7 (tangent cuts of the complementarity sum q on the Z-seeded transport polytope), rebuilt
from the statement, on the paper's wedge WD(2j,j,j+4): (i) the harmonic normal form over C = {v1,v2} from the game gives
B = 2^{-(e+1)} [[1,-lambda],[-lambda,1]] with lambda = 1 - 2^{1-j}, positive definite (WD in R); (ii) round 0 (the transport
LP with the free Z-seed, all three readings of the standing rule) is silent at both Max vertices; (iii) one round of tangent
cuts at the 8|C| lexicographic optima decides both by clause (ii). q(x) = sum_{v in C} (x(v)-x(v^0))(x(v)-x(v^1)) on the
full vertex coordinates; the cut at x is grad q(x).(y - x) <= -q(x), valid at w* when q is convex on aff Q(G). Exact."""
import sys, os as _os
sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'harness'))
from fractions import Fraction as F
from mycore import G, wstar, is_stopping, transport_rows, distinguishing
from mylp import LP
from zseed import seeds
import wd as WDMOD

def solve(Mx, rhs):
    n = len(Mx); T = [list(map(F, Mx[i])) + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if T[r][c] != 0); T[c], T[p] = T[p], T[c]; pv = T[c][c]; T[c] = [x / pv for x in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [T[r][j] - f * T[c][j] for j in range(n + 1)]
    return [T[i][n] for i in range(n)]

def first_passage_rows(g, C):
    """for each controlled v and action a: the law of the first hit of C u {t1} from v^(a) through average vertices."""
    avg = [v for v in range(g.n) if g.kinds[v] == 'avg']; ai = {v: i for i, v in enumerate(avg)}
    def law(tgt):
        A = [[F(int(i == j)) for j in range(len(avg))] for i in range(len(avg))]; b = [F(0)] * len(avg)
        for a in avg:
            for s in g.succ[a]:
                if s in ai: A[ai[a]][ai[s]] -= F(1, 2)
                elif s == tgt: b[ai[a]] += F(1, 2)
        h = solve(A, b) if avg else []
        return lambda u: h[ai[u]] if u in ai else F(int(u == tgt))
    laws = {t: law(t) for t in list(C) + [g.T1]}
    rows = {}
    for v in C:
        for a in (0, 1):
            s = g.succ[v][a]; rows[(v, a)] = ([laws[u](s) for u in C], laws[g.T1](s))
    return rows

def point_after(lp, n):
    """the current basic solution of the tableau (after a maximize call)."""
    x = [F(0)] * n
    for i, bv in enumerate(lp.basis):
        if bv < n: x[bv] = lp.T[i][-1]
    return x

def opt_point(A, b, n, c, second=None):
    """lexicographic: maximise c, then maximise `second` among optima; return the point."""
    lp = LP(A, b, n); v = lp.maximize(c); assert v is not None
    if second is None: return point_after(lp, n)
    A2 = A + [[-x for x in c]]; b2 = b + [-v]
    lp2 = LP(A2, b2, n); v2 = lp2.maximize(second); assert v2 is not None
    return point_after(lp2, n)

def q_and_grad(g, C, x, xs):
    """q(x) and its gradient over the non-sink coordinates; xs = full vector with sinks appended."""
    q = F(0); grad = [F(0)] * g.n
    for v in C:
        a, b = g.succ[v]; f0 = xs[v] - xs[a]; f1 = xs[v] - xs[b]; q += f0 * f1
        for (coef, u) in ((f1, v), (-f1, a), (f0, v), (-f0, b)):
            if u < g.n: grad[u] += coef
    return q, grad

def sep(A, b, n, p, q_):
    """max x(q) - x(p) over the polytope rows (A,b); sinks: T0 -> 0, T1 -> 1."""
    c = [F(0)] * n; const = F(0)
    for (u, sg) in ((q_, 1), (p, -1)):
        if u < n: c[u] += sg
        elif u == n + 1: const += sg
    lp = LP(A, b, n); v = lp.maximize(c); return v + const

def readings(g, w, A, b):
    dec = {}
    for v in distinguishing(g, w):
        a, bb = g.succ[v]; kind = g.kinds[v]
        S = {pr: sep(A, b, g.n, *pr) for pr in [(v, a), (v, bb), (a, v), (bb, v), (a, bb), (bb, a)]}
        fired = []
        if kind == 'max':
            if S[(a, v)] <= 0: fired.append(('(i)', 0))
            if S[(bb, v)] <= 0: fired.append(('(i)', 1))
            if S[(v, a)] < 0: fired.append(('(ii)', 1))
            if S[(v, bb)] < 0: fired.append(('(ii)', 0))
            if S[(a, bb)] <= 0: fired.append(('pair', 0))
            if S[(bb, a)] <= 0: fired.append(('pair', 1))
        opt = 0 if (w[a] >= w[bb]) == (kind == 'max') else 1
        assert all(act == opt for _, act in fired), 'UNSOUND'
        dec[v] = fired
    return dec

for j in (2, 3, 4):
    e, m = 2 * j, j + 4
    ret = WDMOD.WD(e, j, m); g = ret[0] if isinstance(ret, tuple) else ret
    assert is_stopping(g); w = wstar(g); L, U, Z0, Z1 = seeds(g, w)
    C = [v for v in range(g.n) if g.kinds[v] in ('max', 'min')]
    rows = first_passage_rows(g, C); k = len(C)
    P0 = [rows[(v, 0)][0] for v in C]; P1 = [rows[(v, 1)][0] for v in C]
    R0 = [[F(int(i == jj)) - P0[i][jj] for jj in range(k)] for i in range(k)]; R1 = [[F(int(i == jj)) - P1[i][jj] for jj in range(k)] for i in range(k)]
    B = [[sum(R0[t][i] * R1[t][jj] + R1[t][i] * R0[t][jj] for t in range(k)) / 2 for jj in range(k)] for i in range(k)]
    lam = 1 - F(2, 2 ** j); want = [[F(1, 2 ** (e + 1)), -lam * F(1, 2 ** (e + 1))], [-lam * F(1, 2 ** (e + 1)), F(1, 2 ** (e + 1))]]
    assert B == want, (j, B)
    assert B[0][0] > 0 and B[0][0] * B[1][1] - B[0][1] * B[1][0] > 0
    A, b = transport_rows(g, L=L, U=U); n = g.n
    r0 = readings(g, w, A, b)
    # the tangent cuts at the 8|C| lexicographic optima
    cuts = 0; A1 = list(A); b1 = list(b)
    for v in C:
        for a in g.succ[v]:
            gvec = [F(0)] * n
            if v < n: gvec[v] -= 1
            if a < n: gvec[a] += 1        # g_{v,i} = x(v^i) - x(v)
            for sg in (1, -1):
                for sg2 in (1, -1):
                    c = [sg * x for x in gvec]; second = [F(0)] * n; second[v] = F(sg2)
                    x = opt_point(A, b, n, c, second)
                    xs = x + [F(0), F(1)]
                    q, grad = q_and_grad(g, C, x, xs)
                    if q > 0:
                        # grad . (y - x) <= -q  ->  grad . y <= grad . x - q
                        A1.append(list(grad)); b1.append(sum(grad[i] * x[i] for i in range(n)) - q); cuts += 1
                        ws = w[:n]; assert sum(grad[i] * (ws[i] - x[i]) for i in range(n)) <= -q, 'cut invalid at w*'
    r1 = readings(g, w, A1, b1)
    maxv = [v for v in C if g.kinds[v] == 'max']
    print(f'WD({e},{j},{m}), N={g.N}: B = 2^-(e+1)[[1,-l],[-l,1]] with l={lam} OK (in R); round 0 fires {[r0[v] for v in maxv]} at the Max vertices; '
          f'{cuts} tangent cuts (all valid at w*); round 1 fires {[r1[v] for v in maxv]}')
    assert all(not r0[v] for v in maxv) and all(r1[v] for v in maxv)
print('M7 DECIDES THE WEDGE AT ROUND ONE: CONFIRMED')
