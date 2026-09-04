#!/usr/bin/env python3
"""The eval-decision route's adversary certificates (cert_m2_d2.json, cert_m3_d3.json), rechecked from the rows alone:
one-player harmonic systems over C = {0..m-1} (rows (q; p_0..p_{m-1}) per incidence (v,a), substochastic), the start v0 = 0.
For every node (a sequence of <= m distinct queries): the NO world is stopping, nondegenerate, has val*(v0) < 1/2, leaves
the last queried strategy strictly switchable somewhere, and answers every query on its path exactly as the ancestor at
that depth does (so the data D of the path is well defined); the YES witness is stopping, nondegenerate, has
val*(v0) >= 1/2 and reproduces the whole path's data. Tree completeness: every node of depth < m has, for every strategy
not yet queried, a child. Hence after m answers both bits are consistent with the data: m+1 evaluations are necessary."""
import sys, os, json, itertools
from fractions import Fraction as F
M = os.path.dirname(os.path.abspath(__file__))   # the certificates are archived beside this script

def solve(Mx, rhs):
    n = len(Mx); T = [list(map(F, Mx[i])) + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if T[r][c] != 0), None)
        if p is None: return None
        T[c], T[p] = T[p], T[c]; pv = T[c][c]; T[c] = [x / pv for x in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [T[r][j] - f * T[c][j] for j in range(n + 1)]
    return [T[i][n] for i in range(n)]

def parse(rows, m):
    R = {}
    for k, v in rows.items():
        i, a = map(int, k.split(',')); vals = [F(x) for x in v]
        R[(i, a)] = (vals[0], vals[1:]); assert len(vals) == m + 1 and all(x >= 0 for x in vals) and sum(vals) <= 1
    return R

def stopping(R, m):
    for U in range(1, 1 << m):
        us = [i for i in range(m) if (U >> i) & 1]
        if all(any(R[(i, a)][0] == 0 and sum(R[(i, a)][1]) == 1 and all(R[(i, a)][1][j] == 0 for j in range(m) if not (U >> j) & 1) for a in (0, 1)) for i in us):
            return False
    return True

def evaluate(R, sig, m):
    P = [R[(i, sig[i])][1] for i in range(m)]; q = [R[(i, sig[i])][0] for i in range(m)]
    x = solve([[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)], q); assert x is not None
    app = {(i, a): R[(i, a)][0] + sum(R[(i, a)][1][j] * x[j] for j in range(m)) for i in range(m) for a in (0, 1)}
    return tuple(x), app

def analyse(R, m):
    strategies = list(itertools.product((0, 1), repeat=m)); vals = {}; nondeg = True; switch = {}
    for sig in strategies:
        x, app = evaluate(R, sig, m); vals[sig] = x
        sw = [i for i in range(m) if app[(i, 1 - sig[i])] > x[i]]; switch[sig] = sw
        if any(app[(i, 1 - sig[i])] == x[i] for i in range(m)): nondeg = False
    star = tuple(max(vals[s][i] for s in strategies) for i in range(m))   # one player: val* = componentwise max
    return vals, switch, nondeg, star

for m, fn in ((2, 'cert_m2_d2.json'), (3, 'cert_m3_d3.json')):
    cert = json.load(open(f'{M}/{fn}')); nodes = {tuple(tuple(q) for q in c['queries']): c for c in cert}
    assert len(nodes) == len(cert)
    strategies = list(itertools.product((0, 1), repeat=m))
    # completeness
    depths = {}
    for key in nodes: depths.setdefault(len(key), 0); depths[len(key)] += 1
    for key in list(nodes) + [()]:
        if len(key) < m:
            for s in strategies:
                if s not in key: assert key + (s,) in nodes, ('missing child', key, s)
    # per node
    mism = []
    answers = {}   # path prefix -> (values, appeals) of the NO world at that depth
    for key in sorted(nodes, key=len):
        c = nodes[key]; R = parse(c['no_rows'], m); Y = parse(c['yes_rows'], m)
        assert stopping(R, m) and stopping(Y, m)
        vals, sw, nd, star = analyse(R, m); yvals, ysw, ynd, ystar = analyse(Y, m)
        assert nd and ynd, ('degenerate', key)
        assert star[0] < F(1, 2) and ystar[0] >= F(1, 2), ('bit', key, star[0], ystar[0])
        if [F(x) for x in c['no_valstar']] != list(star): mism.append(('no_valstar', key))
        if F(c['yes_val']) != ystar[0]:
            # the file's yes_val may be the value under the recorded yes_sigma rather than val*; note it
            ys = tuple(c['yes_sigma']); mism.append(('yes_val', key, str(c['yes_val']), str(ystar[0]), str(yvals[ys][0])))
        last = key[-1]; assert sw[last], ('last query not switchable', key)
        assert vals[last][0] < F(1, 2)
        x, app = evaluate(R, last, m); answers[key] = (x, app)
        # consistency of the NO world with all ancestors' answers, and of the YES witness with the whole path
        for r in range(1, len(key) + 1):
            prefix = key[:r]; ax, aapp = answers[prefix]
            xx, aa = evaluate(R, key[r - 1], m); assert (xx, aa) == (ax, aapp), ('NO world inconsistent with ancestor', key, r)
            yx, ya = evaluate(Y, key[r - 1], m); assert (yx, ya) == (ax, aapp), ('YES witness inconsistent', key, r)
    if mism: print(f'  note: {len(mism)} recorded numbers differ from mine (informational, first: {mism[0]})')
    print(f'm={m}: {len(nodes)} nodes ({depths}), tree complete to depth {m}; every NO world stopping, nondegenerate, val*(v0) < 1/2, last query strictly switchable, consistent with its ancestors; every YES witness stopping, nondegenerate, val*(v0) >= 1/2, consistent with the whole path => {m+1} evaluations are necessary to decide the bit')
print('ADVERSARY CERTIFICATES CONFIRMED')
