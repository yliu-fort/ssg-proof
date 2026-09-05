#!/usr/bin/env python3
"""Root agent's verification of the round-19 hk-law-certificate route, from the statements.

 [1] s_0 = (8,9,10,11,13,12,14,15,7,6,4,5,3,2,1,0) is an acyclic Holt-Klee unique sink orientation of the 4-cube of
     bottom-antipodal height 2; its facet datum at (u,a) = (0,0) read on the coordinates 1,2,3 is t = (4,5,6,7,3,2,1,0)
     with the colouring chi = b_0, chi^{-1}(1) = {2,4,6,7}; t is a Holt-Klee AUSO of height 2.
 [2] the 43 distinct exact one-player readout systems of the route realise t (outmap from the system, nondegenerate),
     and on each of them, and on several hundred random perturbations still realising t, the five 4x4 determinants
     of the homogeneous value points have the signs (D(0,2,5,6), D(2,3,5,6), D(0,2,3,5), D(0,2,3,6), D(0,3,5,6))
     = (-,-,+,+,-) and the Radon coefficients on {0,2,3,5,6} have the signs of chi, so no affine functional
     separates chi -- the obstruction the proof forces for EVERY realisation;
 [3] the exclusion scan over the 12640 classes of the 4-cube census: the classes carrying a facet datum isomorphic to
     (t, chi) or (t, 1-chi) under the 48 automorphisms of the 3-cube -- expected 17, of which 13 Holt-Klee with
     heights 2,3,4 in multiplicities 3,6,4 -- and that s_0 is among them.
"""
import sys, os, json, itertools, random
from fractions import Fraction as F
M = '/tmp/claude-1000/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/scratchpad'
sys.path.insert(0, f'{M}/solo'); sys.path.insert(0, f'{M}/root16')
from my_D import is_holt_klee
from auso import is_uso, is_acyclic, ba_heights
R19 = f'{M}/r19-hk-law-certificate'

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

def det(Mx):
    n = len(Mx); A = [list(map(F, r)) for r in Mx]; d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return F(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]; pv = A[c][c]
        for r in range(c + 1, n):
            if A[r][c] != 0:
                f = A[r][c] / pv; A[r] = [A[r][j] - f * A[c][j] for j in range(n)]
    return d

# [1]
s0 = (8, 9, 10, 11, 13, 12, 14, 15, 7, 6, 4, 5, 3, 2, 1, 0); m = 4
assert is_uso(s0, m) and is_acyclic(s0, m) and is_holt_klee(s0, m)[0]
h = ba_heights(s0, m); assert max(h) == 2
b = [v ^ s0[v] for v in range(16)]
t = tuple((s0[sig << 1] >> 1) & 7 for sig in range(8))          # facet u = 0, a = 0, read on coordinates 1,2,3
chi = tuple(b[sig << 1] & 1 for sig in range(8))
assert t == (4, 5, 6, 7, 3, 2, 1, 0) and {i for i in range(8) if chi[i]} == {2, 4, 6, 7}
assert is_uso(t, 3) and is_acyclic(t, 3) and is_holt_klee(t, 3)[0] and max(ba_heights(t, 3)) == 2
print('[1] s_0: acyclic Holt-Klee USO of height 2; its (0,0)-facet datum is t = (4,5,6,7,3,2,1,0) with chi^-1(1) = {2,4,6,7}; t is a Holt-Klee AUSO of height 2')

# [2] the systems
def load_systems():
    out = {}
    for fn in ('systems3_t.json', 'systems3_t_big.json'):
        for S in json.load(open(f'{R19}/{fn}')):
            rows = tuple(tuple(F(x, S['den']) for x in S['A'][i]) + (F(S['b'][i], S['den']),) for i in range(6))
            out[rows] = rows
    return list(out.values())
def values(rows, sig):
    A = [[F(int(i == j)) - rows[2 * i + sig[i]][j] for j in range(3)] for i in range(3)]
    q = [rows[2 * i + sig[i]][3] for i in range(3)]
    return solve(A, q)
def outmap_of(rows):
    s = [0] * 8; nd = True; xs = {}
    for sig in itertools.product((0, 1), repeat=3):
        x = values(rows, sig)
        if x is None: return None, False, None
        xs[sig] = x; msk = 0
        for i in range(3):
            other = sum(rows[2 * i + 1 - sig[i]][j] * x[j] for j in range(3)) + rows[2 * i + 1 - sig[i]][3]
            if other > x[i]: msk |= 1 << i
            elif other == x[i]: nd = False
        s[sig[0] | (sig[1] << 1) | (sig[2] << 2)] = msk
    return tuple(s), nd, xs
def circuit(xs):
    Y = {i: list(xs[(i & 1, (i >> 1) & 1, (i >> 2) & 1)]) + [F(1)] for i in range(8)}   # the route's convention: the 1 last
    D = lambda *idx: det([Y[i] for i in idx])
    signs = tuple((v > 0) - (v < 0) for v in (D(0, 2, 5, 6), D(2, 3, 5, 6), D(0, 2, 3, 5), D(0, 2, 3, 6), D(0, 3, 5, 6)))
    S = (0, 2, 3, 5, 6); mu = {}
    for k, i in enumerate(S):
        rest = [Y[j] for j in S if j != i]; mu[i] = (-1) ** k * det(rest)
    assert all(sum(mu[i] * Y[i][c] for i in S) == 0 for c in range(4))
    musign = tuple((mu[i] > 0) - (mu[i] < 0) for i in S)
    return signs, musign
systems = load_systems(); assert len(systems) == 43, len(systems)
ok = 0
for rows in systems:
    for r in rows: assert all(x >= 0 for x in r) and sum(r) <= 1
    s, nd, xs = outmap_of(rows); assert s == t and nd
    signs, musign = circuit(xs); assert signs == (-1, -1, 1, 1, -1) and musign == (-1, 1, -1, -1, 1), (signs, musign); ok += 1
print(f'[2] all {ok} distinct route systems realise t nondegenerately with the five determinant signs (-,-,+,+,-) and Radon signs (-,+,-,-,+) on (0,2,3,5,6): positive exactly on {{2,6}} in chi^-1(1), negative on {{0,3,5}} in chi^-1(0)')
rng = random.Random(1912); pert = 0; tried = 0
while pert < 300 and tried < 20000:
    base = rng.choice(systems); tried += 1
    rows = []
    for r in base:
        rr = [max(F(0), x + F(rng.randrange(-40, 41), 20000)) for x in r]
        if sum(rr) >= 1: rr = [x * F(999, 1000) / sum(rr) for x in rr]
        rows.append(tuple(rr))
    s, nd, xs = outmap_of(rows)
    if s != t or not nd: continue
    signs, musign = circuit(xs); assert signs == (-1, -1, 1, 1, -1) and musign == (-1, 1, -1, -1, 1); pert += 1
print(f'[2] {pert} random perturbations still realising t: the same signs every time')
# no affine functional separates chi on these configurations: any phi with phi(y_i) > 0 on chi=1 and < 0 on chi=0 gives sum mu_i phi(y_i) > 0 against 0 -- the Radon identity above is the certificate

# [3] the exclusion scan over the census
def act3(u, perm, z):
    """orientation u of the 3-cube transported by sigma -> perm(sigma) xor z (perm a permutation of the coordinates)."""
    def pb(x): return sum(((x >> i) & 1) << perm[i] for i in range(3))
    out = [0] * 8
    for sig in range(8): out[pb(sig) ^ z] = pb(u[sig])
    return tuple(out)
def canon(tt, cc):
    best = None
    for perm in itertools.permutations(range(3)):
        for z in range(8):
            def pb(x): return sum(((x >> i) & 1) << perm[i] for i in range(3))
            to = [0] * 8; co = [0] * 8
            for sig in range(8): to[pb(sig) ^ z] = pb(tt[sig]); co[pb(sig) ^ z] = cc[sig]
            for flip in (0, 1):
                key = (tuple(to), tuple(c ^ flip for c in co))
                if best is None or key < best: best = key
    return best
target = canon(t, chi)
def facet_data(s):
    out = []
    for u in range(4):
        for a in (0, 1):
            others = [c for c in range(4) if c != u]
            tt = []; cc = []
            for sig in range(8):
                full = a << u
                for k, c in enumerate(others): full |= ((sig >> k) & 1) << c
                val = s[full]; tv = 0
                for k, c in enumerate(others): tv |= ((val >> c) & 1) << k
                tt.append(tv); cc.append(((full ^ val) >> u) & 1)
            out.append((u, a, tuple(tt), tuple(cc)))
    return out
classes = []
for line in open(f'{M}/solo/census/classes4.txt'):
    if not line.startswith('REP'): continue
    head, vec = line.split(':'); s = tuple(int(x) for x in vec.split()); hh = int(head.split('h=')[1].split()[0]); hk = int(head.split('hk=')[1].split()[0])
    classes.append((s, hh, hk))
assert len(classes) == 12640
excl = []
for s, hh, hk in classes:
    if any(canon(tt, cc) == target for (u, a, tt, cc) in facet_data(s)): excl.append((s, hh, hk))
from collections import Counter
hkc = Counter((hh) for s, hh, hk in excl if hk); nonhk = sum(1 for s, hh, hk in excl if not hk)
print(f'[3] classes of the 4-cube carrying a facet datum isomorphic to (t,chi) or its complement: {len(excl)}; Holt-Klee among them {sum(1 for s,h_,hk in excl if hk)} with heights {dict(sorted(hkc.items()))}; non-Holt-Klee {nonhk}; s_0 among them: {any(canon_s == s0 or True for canon_s in [None]) and any(canon(*fd[2:]) == target for fd in facet_data(s0))}')
assert len(excl) == 17 and sum(1 for s, h_, hk in excl if hk) == 13 and dict(hkc) == {2: 3, 3: 6, 4: 4}
print('HK-LAW ROUTE: s_0 is not one-player realisable -- the facet datum obstruction reproduced on the systems and the census')
