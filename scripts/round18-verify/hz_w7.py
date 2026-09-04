#!/usr/bin/env python3
"""M7 (the tangent cut of the complementarity sum, all three readings, Z-seeded) on the seven-vertex both-readings stall of
rem:own-stall: round 0 silent at vertex 4 (as recorded), round 1 decides it; the cut at the lexicographic optimum and its
validity at w* printed. Also the reduced 1/2-contraction of HZ(n): every first-passage row has mass exactly 1/2, so the
reduced Shapley operator contracts the sup norm by 1/2 (the novelty auditor's observation that HZ(n) is polynomial)."""
import sys, os as _os, json
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from hzlib import *
from mycore import G, wstar, is_stopping, transport_rows, distinguishing
from mylp import LP
from zseed import seeds
from fractions import Fraction as F

def point_after(lp, n):
    x = [F(0)] * n
    for i, bv in enumerate(lp.basis):
        if bv < n: x[bv] = lp.T[i][-1]
    return x
def opt_point(A, b, n, c, second):
    lp = LP(A, b, n); v = lp.maximize(c); assert v is not None
    lp2 = LP(A + [[-x for x in c]], b + [-v], n); v2 = lp2.maximize(second); assert v2 is not None
    return point_after(lp2, n)
def q_and_grad(g, C, xs):
    q = F(0); grad = [F(0)] * g.n
    for v in C:
        a, b = g.succ[v]; f0 = xs[v] - xs[a]; f1 = xs[v] - xs[b]; q += f0 * f1
        for (coef, u) in ((f1, v), (-f1, a), (f0, v), (-f0, b)):
            if u < g.n: grad[u] += coef
    return q, grad
def sep(A, b, n, p, q_):
    c = [F(0)] * n; const = F(0)
    for (u, sg) in ((q_, 1), (p, -1)):
        if u < n: c[u] += sg
        elif u == n + 1: const += sg
    return LP(A, b, n).maximize(c) + const
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
        else:
            if S[(v, a)] <= 0: fired.append(('(i)', 0))
            if S[(v, bb)] <= 0: fired.append(('(i)', 1))
            if S[(a, v)] < 0: fired.append(('(ii)', 1))
            if S[(bb, v)] < 0: fired.append(('(ii)', 0))
            if S[(a, bb)] <= 0: fired.append(('pair', 1))
            if S[(bb, a)] <= 0: fired.append(('pair', 0))
        opt = 0 if (w[a] >= w[bb]) == (kind == 'max') else 1
        assert all(act == opt for _, act in fired), 'UNSOUND'
        dec[v] = fired
    return dec

g = G(['avg','min','avg','max','max'], [(2,6),(3,6),(5,0),(0,5),(1,2)])
w = wstar(g); L, U, Z0, Z1 = seeds(g, w); C, rows, B = Bmatrix(g); assert psd(B)[0]
A, b = transport_rows(g, L=L, U=U); n = g.n
r0 = readings(g, w, A, b); print('round 0:', r0)
A1, b1 = list(A), list(b); cuts = []
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
                    A1.append(list(grad)); b1.append(rhs); cuts.append((x, grad, rhs))
r1 = readings(g, w, A1, b1); print('round 1:', r1, f'({len(cuts)} cuts, all valid at w*)')
assert not r0[4] and r1[4]
for x, grad, rhs in cuts:
    if x[4] == F(1, 3) and x[1] == F(1, 3): print('  cut at x =', [str(t) for t in x], ':', [str(t) for t in grad], '. y <=', rhs)
# HZ(n): reduced 1/2-contraction
M = '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad/r18-convex-class'
for nn in (4, 6):
    d = json.load(open(f'{M}/HZ_{nn}_GAME.json')); gg = G(d['kinds'], [tuple(s) for s in d['succ']])
    Cg, rws, Bg = Bmatrix(gg)
    mass = {sum(rws[(v, a)][0]) for v in Cg for a in (0, 1)}
    print(f'HZ({nn}): first-passage row masses over C (the part the contraction reads): {sorted(str(m) for m in mass)} -> the reduced Shapley operator is a 1/2-contraction in the sup norm')
    assert mass == {F(1, 2)}
print('SEVEN-VERTEX STALL DECIDED BY M7 AT ROUND ONE; HZ REDUCED CONTRACTION CONFIRMED')
