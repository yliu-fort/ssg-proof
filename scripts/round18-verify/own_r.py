#!/usr/bin/env python3
"""The round-18 paper audit's two majors on the stall material, recomputed with the root's harness: on R of
prop:own-stall and on the seven-vertex game of rem:own-stall, ALL THREE readings of the transport certificate
(own-successor clause (i), clause (ii), and the non-strict pair test), Z-seeded, at every value-distinguishing
controlled vertex; then the seven-vertex game after retyping the decided vertices (thm:decide-one-bit).
Sep(p,q) := max{x(q) - x(p) : x in Q(G;L,U)}; Sep(p,q) <= 0 certifies w*(q) <= w*(p)."""
import sys, os as _os; sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'harness')); sys.path.insert(0, '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad/root16')
from fractions import Fraction as F
from mycore import G, wstar, transport_sep, distinguishing
from zseed import seeds

def readings(name, kinds, succ):
    g = G(kinds, [list(s) for s in succ]); w = wstar(g); L, U, Z0, Z1 = seeds(g, w)
    dist = distinguishing(g, w)
    print(f'{name}: N={g.N}, w*={[str(x) for x in w[:g.n]]}, Z0={sorted(Z0)}, Z1={sorted(Z1)}, value-distinguishing controlled vertices {dist}')
    decided = {}
    for v in dist:
        a, b = g.succ[v]; kind = g.kinds[v]
        S = transport_sep(g, [(v, a), (v, b), (a, v), (b, v), (a, b), (b, a)], L=L, U=U)
        opt = 0 if (w[a] >= w[b]) == (kind == 'max') else 1
        fired = []
        if kind == 'max':
            # (i): w*(v) <= w*(v^i) i.e. Sep(v^i, v) <= 0 -> v^i optimal; (ii): w*(v^i) < w*(v) i.e. Sep(v, v^i) < 0 -> v^i not optimal
            if S[(a, v)] <= 0: fired.append(('(i)', 0))
            if S[(b, v)] <= 0: fired.append(('(i)', 1))
            if S[(v, a)] < 0: fired.append(('(ii)', 1))
            if S[(v, b)] < 0: fired.append(('(ii)', 0))
            if S[(a, b)] <= 0: fired.append(('pair', 0))   # w*(b) <= w*(a): a optimal at Max
            if S[(b, a)] <= 0: fired.append(('pair', 1))
        else:
            # (i): w*(v^i) <= w*(v) i.e. Sep(v, v^i) <= 0 -> v^i optimal; (ii): w*(v) < w*(v^i) i.e. Sep(v^i, v) < 0 -> v^i not optimal
            if S[(v, a)] <= 0: fired.append(('(i)', 0))
            if S[(v, b)] <= 0: fired.append(('(i)', 1))
            if S[(a, v)] < 0: fired.append(('(ii)', 1))
            if S[(b, v)] < 0: fired.append(('(ii)', 0))
            if S[(a, b)] <= 0: fired.append(('pair', 1))   # w*(b) <= w*(a): b optimal at Min
            if S[(b, a)] <= 0: fired.append(('pair', 0))
        sound = all(act == opt for _, act in fired)
        print(f'  {kind} {v}->({a},{b}) w*=({w[a]},{w[b]}) optimal action {opt}: Sep(v,a)={S[(v,a)]} Sep(v,b)={S[(v,b)]} Sep(a,v)={S[(a,v)]} Sep(b,v)={S[(b,v)]} Sep(a,b)={S[(a,b)]} Sep(b,a)={S[(b,a)]} -> fires {fired} sound={sound}')
        if fired: decided[v] = opt
    return g, w, decided

# R of prop:own-stall: {0..7}, t0=8, t1=9
readings('R', ['min','min','avg','avg','max','avg','min','min'], [(2,5),(5,3),(5,2),(0,9),(0,8),(9,8),(0,8),(5,2)])
# the seven-vertex game of rem:own-stall: Vavg={0,2}, Vmin={1}, Vmax={3,4}; t0=5, t1=6
kinds = ['avg','min','avg','max','max']; succ = [(2,6),(3,6),(5,0),(0,5),(1,2)]
g, w, decided = readings('W7', kinds, succ)
# retype the decided vertices as average vertices pointing at their optimal successor twice, re-run
kinds2 = list(kinds); succ2 = [tuple(s) for s in succ]
for v, act in decided.items():
    kinds2[v] = 'avg'; succ2[v] = (succ[v][act], succ[v][act])
print('retyped', decided)
readings('W7 after retyping', kinds2, succ2)
