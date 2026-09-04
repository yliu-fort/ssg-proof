#!/usr/bin/env python3
"""The convex-lift novelty auditor's correction to rem:own-successor / rem:own-stall, checked with the
root's harness: on R of prop:own-stall the NON-STRICT pair test Sep(v^(0),v^(1)) <= 0 or
Sep(v^(1),v^(0)) <= 0 (Sep(p,q) = max x(q)-x(p) over Q(G;L,U), Z-seeded) decides every
value-distinguishing controlled vertex although the own-successor separators are all 0; and on the
auditor's 7-vertex witness both readings are silent at the value-distinguishing Max vertex 4."""
import sys; sys.path.insert(0, '../root16')
from fractions import Fraction as F
from mycore import G, wstar, transport_sep, distinguishing
from zseed import seeds
def analyse(name, kinds, succ):
    g = G(kinds, [list(s) for s in succ]); w = wstar(g); L, U, Z0, Z1 = seeds(g, w)
    print(f'{name}: N = {g.N}, w* = {[str(x) for x in w[:g.n]]}, Z0 = {sorted(Z0)}, Z1 = {sorted(Z1)}, value-distinguishing controlled vertices {distinguishing(g, w)}')
    for v in distinguishing(g, w):
        a, b = g.succ[v]; kind = g.kinds[v]
        if kind == 'max': own = transport_sep(g, [(v, a), (v, b)], L=L, U=U); own_fires = own[(v, a)] < 0 or own[(v, b)] < 0
        else: own = transport_sep(g, [(a, v), (b, v)], L=L, U=U); own_fires = own[(a, v)] < 0 or own[(b, v)] < 0
        pair = transport_sep(g, [(a, b), (b, a)], L=L, U=U)
        # Sep(a,b) <= 0 proves w*(b) <= w*(a): at Max this names a (action 0) optimal, at Min b (action 1)
        pair_fires = pair[(a, b)] <= 0 or pair[(b, a)] <= 0
        named = None
        if pair[(a, b)] <= 0: named = 0 if kind == 'max' else 1
        elif pair[(b, a)] <= 0: named = 1 if kind == 'max' else 0
        opt = 0 if (w[a] >= w[b]) == (kind == 'max') else 1
        print(f'   {kind} {v} -> ({a},{b}) w* {str(w[a])},{str(w[b])}: own-successor seps {[str(x) for x in own.values()]} fires={own_fires}; '
              f'pair seps Sep(a,b)={pair[(a,b)]} Sep(b,a)={pair[(b,a)]} fires={pair_fires}' + (f' names action {named} (optimal {opt}, sound={named==opt})' if named is not None else ''))
# R of prop:own-stall: {0..7}, t0=8, t1=9
analyse('R', ['min','min','avg','avg','max','avg','min','min'],
        [(2,5),(5,3),(5,2),(0,9),(0,8),(9,8),(0,8),(5,2)])
# the auditor's witness: Vavg={0,2}, Vmin={1}, Vmax={3,4}; t0=5, t1=6
analyse('W7', ['avg','min','avg','max','max'], [(2,6),(3,6),(5,0),(0,5),(1,2)])
