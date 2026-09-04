#!/usr/bin/env python3
"""BC(e,s): the root's own slack calculus (def:slack), its min-plus closure (def:trans-slack) and
def:ratio, seeded with Z_0, Z_1, both clauses of rem:own-successor at v0, v1, v2, no LPs."""
import sys, json, time
sys.path.insert(0, '../root16')
from fractions import Fraction as F
from mycore import G, wstar, Z01, slack_step, minplus_close, clamp, ones, check_sound
from ratio import ratio_rounds, INF, sound
def fires(D, g, v, Z0):
    a, b = g.succ[v]
    if g.kinds[v] == 'max':
        c1 = [u for u in (a, b) if D[v][u] <= 0]; c2 = [u for u in (a, b) if D[u][v] < 0]
    else:
        c1 = [u for u in (a, b) if D[u][v] <= 0]; c2 = [u for u in (a, b) if D[v][u] < 0]
    return ('(i)' if c1 else '(ii)') if (c1 or c2) else None
for fn in sys.argv[1:]:
    d = json.load(open(fn)); names = d['names']; kinds = d['kinds']; succ = [list(x) for x in d['succ']]
    g = G(kinds, succ); w = wstar(g); n = len(kinds); Z0, Z1 = Z01(g, w); C = [i for i in range(n) if kinds[i] != 'avg']
    K = 40; t = time.time()
    D = ones(g.N); first_s = {}; first_t = {}; Dt = ones(g.N)
    for k in range(1, K + 1):
        D = [[clamp(x) for x in r] for r in slack_step(g, D, Z0, Z1)]; check_sound(g, D, w, f's{k}')
        Dt = [[clamp(x) for x in r] for r in minplus_close(slack_step(g, Dt, Z0, Z1), g.N)]; check_sound(g, Dt, w, f't{k}')
        for v in C:
            if v not in first_s and fires(D, g, v, Z0): first_s[v] = (k, fires(D, g, v, Z0))
            if v not in first_t and fires(Dt, g, v, Z0): first_t[v] = (k, fires(Dt, g, v, Z0))
    print(f"{fn.split('/')[-1]} (N={n+2}): slack M2 first firing {{ {', '.join(f'{names[v]}: {first_s.get(v)}' for v in C)} }}; closure M2T {{ {', '.join(f'{names[v]}: {first_t.get(v)}' for v in C)} }}  [{K} rounds, {time.time()-t:.0f}s]", flush=True)
    t = time.time(); Rs = ratio_rounds(g, w, K); firstR = {}
    for k, R in enumerate(Rs, 1):
        assert sound(g, R, w) == 0
        for v in C:
            if v in firstR: continue
            c1 = [u for u in g.succ[v] if R[v][u] is not INF and R[v][u] <= 1]
            c2 = [u for u in g.succ[v] if R[u][v] is not INF and R[u][v] < 1] if v not in Z0 else []
            if c1 or c2: firstR[v] = (k, '(i)' if c1 else '(ii)')
    print(f"   ratio M6 first firing {{ {', '.join(f'{names[v]}: {firstR.get(v)}' for v in C)} }}  [{K} rounds, {time.time()-t:.0f}s]", flush=True)
