#!/usr/bin/env python3
"""The beyond-holt-klee route's record: the 260-vertex one-player game H11_m5_GAME.json. Checked here from the game:
stopping; the first-passage rows over C u {t1} recomputed by my own solver equal the printed normal form (denominator
8192); the improvement outmap from the 32 exact value vectors equals the printed s; no tied incidence; USO, acyclic,
Holt-Klee (max-flow test of the harness), bottom-antipodal height 11, the run from sigma = 10; values nondecreasing along
the run; the stacking hypotheses rho < 1 and g_min > 0; the class is not the orbit of prop:hkfive's witness."""
import sys, os as _os, json, itertools
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from hzlib import first_passage_rows, solve
from mycore import G, is_stopping
from fractions import Fraction as F
import auso, my_D
d = json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'H11_m5_GAME.json')))
g = G(d['kinds'], [tuple(s) for s in d['succ']]); m = d['m']; den = d['den']
assert g.N == 260 and g.kinds.count('max') == 5 and g.kinds.count('min') == 0 and is_stopping(g)
C = [v for v in range(g.n) if g.kinds[v] == 'max']
rows = first_passage_rows(g, C)
for i, v in enumerate(C):
    for a in (0, 1):
        p, q = rows[(v, a)]
        assert [x * den for x in p] == d['A'][2*i + a] and q * den == d['b'][2*i + a], (v, a)
        assert p[i] == 0 and sum(p) + q < 1
print('normal form: the printed rows are the game\'s first-passage laws (denominator 8192), p^{v,a}_v = 0, every row leaks')
rho = max(sum(rows[(v, a)][0]) for v in C for a in (0, 1)); print('rho = max row mass over C =', rho, '(< 1)')
# values under every strategy (reduced system over C: x = P_sigma x + q_sigma), and the outmap
def values(sig):
    P = [rows[(C[i], sig[i])][0] for i in range(m)]; q = [rows[(C[i], sig[i])][1] for i in range(m)]
    A = [[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)]
    return solve(A, q)
s = []; gmin = None; vals = {}
for sig in itertools.product((0, 1), repeat=m):
    x = values(sig); vals[sig] = x; out = 0
    for i in range(m):
        other = rows[(C[i], 1 - sig[i])]; alt = sum(other[0][j] * x[j] for j in range(m)) + other[1]
        marg = alt - x[i]
        assert marg != 0, 'tie'
        gmin = abs(marg) if gmin is None else min(gmin, abs(marg))
        if marg > 0: out |= 1 << i
    s.append(out)
s = tuple(s); idx = lambda sig: sum(sig[i] << i for i in range(m))
S = [0] * 32
for sig in itertools.product((0, 1), repeat=m): S[idx(sig)] = s[list(itertools.product((0, 1), repeat=m)).index(sig)]
S = tuple(S)
assert S == tuple(d['outmap']), (S, d['outmap'])
print('outmap from the 32 exact value vectors equals the printed s; least margin', gmin, '(> 0: nondegenerate)')
assert auso.is_uso(list(S), m) and auso.is_acyclic(list(S), m)
h = auso.ba_heights(list(S), m)
print('USO, acyclic; max bottom-antipodal height:', max(h.values()) if isinstance(h, dict) else max(h))
hk = my_D.is_holt_klee(list(S), m)
print('Holt-Klee:', hk)
# the run from sigma = 10 and the values along it
sig = 10; run = [sig]
while S[sig]: sig ^= S[sig]; run.append(sig)
print('run from 10:', run, 'length', len(run) - 1)
tosig = lambda v: tuple((v >> i) & 1 for i in range(m))
for a, b in zip(run, run[1:]):
    xa, xb = vals[tosig(a)], vals[tosig(b)]
    assert all(xb[i] >= xa[i] for i in range(m))
assert len(run) - 1 == 11 and hk
print('values nondecreasing along the run; h*_1(5) >= 11 witnessed')
