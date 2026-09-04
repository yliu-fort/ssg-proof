#!/usr/bin/env python3
"""The convex-class route's HZ(n) (from its game files HZ_4/HZ_6), the singular member SING, and the membership of the
paper's stalls in R, all recomputed: N = 6n^2+2, stopping, reachable, |Vmax| = |Vmin| = n^2/2, a = 5n^2, B from the
first-passage rows with lambda_min = 1/4 (B - I/4 PSD and singular), w*(d_1) = 2^{-n^2}, every row cycle three-coloured,
the controlled vertices in one strongly connected component; SING's B PSD and singular; B >= 0 on H_m, CC, G8, S, R, W7, BC(2,5)."""
import sys, os as _os, json
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from hzlib import *
from mycore import G, is_stopping, wstar
import myinst, cc as CCMOD
from fractions import Fraction as F
M = '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad/r18-convex-class'

def load(fn):
    d = json.load(open(fn)); g = G(d['kinds'], [tuple(s) for s in d['succ']]); return d, g

def reachable(g, s):
    seen = {s}; st = [s]
    while st:
        u = st.pop()
        for w in (g.succ[u] if u < g.n else ()):
            if w not in seen: seen.add(w); st.append(w)
    return seen

def sccs(g):
    idx = {}; low = {}; st = []; on = set(); out = []; counter = [0]
    sys.setrecursionlimit(100000)
    def dfs(u):
        idx[u] = low[u] = counter[0]; counter[0] += 1; st.append(u); on.add(u)
        for w in g.succ[u]:
            if w >= g.n: continue
            if w not in idx: dfs(w); low[u] = min(low[u], low[w])
            elif w in on: low[u] = min(low[u], idx[w])
        if low[u] == idx[u]:
            comp = []
            while True:
                w = st.pop(); on.discard(w); comp.append(w)
                if w == u: break
            out.append(comp)
    for u in range(g.n):
        if u not in idx: dfs(u)
    return out

for n in (4, 6):
    d, g = load(f'{M}/HZ_{n}_GAME.json'); names = d['names']
    assert g.N == 6 * n * n + 2 and is_stopping(g)
    assert reachable(g, d['start']) >= set(range(g.N))
    km = sum(1 for k in g.kinds if k == 'max'); kn = sum(1 for k in g.kinds if k == 'min'); ka = sum(1 for k in g.kinds if k == 'avg')
    assert km == kn == n * n // 2 and ka == 5 * n * n
    w = [F(x) for x in d['wstar']]                     # the file's value vector, certified by the exact fixed-point test T w = w
    assert len(w) == g.N and w[g.T0] == 0 and w[g.T1] == 1
    for v in range(g.n):
        a, b = g.succ[v]
        tv = max(w[a], w[b]) if g.kinds[v] == 'max' else min(w[a], w[b]) if g.kinds[v] == 'min' else (w[a] + w[b]) / 2
        assert tv == w[v], ('not a fixed point', v)
    C, rows, B = Bmatrix(g); k = len(C)
    # P_a = (1/2) * a permutation matrix
    for a in (0, 1):
        P = [rows[(v, a)][0] for v in C]
        assert all(sorted(r) == [F(0)] * (k - 1) + [F(1, 2)] for r in P) and all(sum(P[i][j] for i in range(k)) == F(1, 2) for j in range(k))
    Bq = [[B[i][j] - F(int(i == j), 4) for j in range(k)] for i in range(k)]
    ok, pd = psd(B); ok4, pd4 = psd(Bq)
    assert ok and pd and ok4 and not pd4
    assert min(x for x in w[:g.n] if x > 0) == F(1, 2 ** (n * n)), 'least positive value'
    dn = [i for i in range(g.n) if w[i] == F(1, 2 ** (n * n))]
    print('   vertices of value 2^-n^2:', [names[i] for i in dn][:4])
    comps = sccs(g); big = [c for c in comps if any(g.kinds[v] != 'avg' for v in c)]
    assert len(big) == 1 and all(v in big[0] for v in C)
    # each row cycle: c_{i,0} -> b0 -> c_{i+1,0} ... contains Max, Min and avg
    for i in range(n):
        row = [names.index(f'c{i}_{j}') for j in range(n)]; kinds = {g.kinds[v] for v in row}
        assert kinds == {'max', 'min'}
    print(f'HZ({n}): N={g.N}, stopping, all reachable, |Vmax|=|Vmin|={km}, a={ka}, P_a = (1/2)*permutation, B > 0 with B - I/4 PSD and singular (lambda_min = 1/4), w*(d_1) = 2^-{n*n}, one SCC holds all controlled vertices, every row has both players')
# the singular member
d, g = load(f'{M}/SING_GAME.json'); assert is_stopping(g); w = wstar(g); C, rows, B = Bmatrix(g); ok, pd = psd(B)
print('SING: N=%d, stopping, w*=%s, B=%s, PSD=%s, PD=%s' % (g.N, [str(x) for x in w[:g.n]], [[str(x) for x in r] for r in B], ok, pd))
assert ok and not pd
# membership of the paper's stalls
def show(name, g):
    C, rows, B = Bmatrix(g); ok, pd = psd(B); print(f'  {name}: |C|={len(C)}, in R: {ok} (positive definite: {pd})'); return ok
res = {}
res['G8'] = show('G_8', unpack(myinst.G8())); res['S'] = show('S', unpack(myinst.S())); res['S_3'] = show('S_3', unpack(myinst.S_r(3)))
for m in (3, 4, 5): res[f'H_{m}'] = show(f'H_{m}', unpack(myinst.H_m(m)))
def unpack(r): return r[0] if isinstance(r, tuple) else r
res['CC(2,2)'] = show('CC(2,2)', unpack(CCMOD.CC(2, 2))); res['CC(3,4)'] = show('CC(3,4)', unpack(CCMOD.CC(3, 4)))
res['R'] = show('R (prop:own-stall)', G(['min','min','avg','avg','max','avg','min','min'], [(2,5),(5,3),(5,2),(0,9),(0,8),(9,8),(0,8),(5,2)]))
res['W7'] = show('7-vertex stall', G(['avg','min','avg','max','max'], [(2,6),(3,6),(5,0),(0,5),(1,2)]))
bc = json.load(open('/data/ssg-proof/scripts/round17-verify/BC_2_5.json')); res['BC(2,5)'] = show('BC(2,5)', G(bc['kinds'], [tuple(s) for s in bc['succ']]))
bc = json.load(open('/data/ssg-proof/scripts/round17-verify/BC_3_5.json')); res['BC(3,5)'] = show('BC(3,5)', G(bc['kinds'], [tuple(s) for s in bc['succ']]))
assert all(res[k] for k in ['G8','S','S_3','H_3','H_4','H_5','CC(2,2)','CC(3,4)','R','W7','BC(2,5)']) and not res['BC(3,5)']
print('ALL HZ / R-MEMBERSHIP CHECKS PASSED')
