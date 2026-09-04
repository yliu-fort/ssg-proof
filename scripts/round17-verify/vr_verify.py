#!/usr/bin/env python3
"""Root agent's check of the round-17 variational route: the Hessian B of the complementarity form on the
affine hull of Q(G), from the harmonic normal form over C (first-passage laws of v^(a) onto C u {t1}),
B = sym(R_0^T R_1) with R_a = I - P_a; the identity d^T B d = |(I - Pbar) d|^2 - (1/4)|Delta d|^2; the
class R = {B psd}; membership of named instances; and the two new games CVX4, CVX6 (in R, runs 4 and 6)."""
import sys, json, itertools, random; sys.argv = ['x']
from fractions import Fraction as F
exec(open('ol_verify.py').read().split("def preorders(A):")[0])   # Game (value, wstar, is_stopping)
def first_passage(g, start):
    """law of the first vertex of C u {t0,t1} hit from `start`, moving through average vertices only"""
    targets = list(g.C) + [g.t0, g.t1]
    if start in targets: return {t: F(int(t == start)) for t in targets}
    inter = [x for x in range(g.n) if g.kinds[x] == 'avg']; idx = {x: i for i, x in enumerate(inter)}; n = len(inter)
    out = {}
    for t in targets:
        A = [[F(0)] * n for _ in range(n)]; b = [F(0)] * n
        for x in inter:
            i = idx[x]; A[i][i] += 1
            for w in g.succ[x]:
                if w in idx: A[i][idx[w]] -= F(1, 2)
                elif w == t: b[i] += F(1, 2)
        Mx = [A[i][:] + [b[i]] for i in range(n)]
        for c in range(n):
            p = next(r for r in range(c, n) if Mx[r][c] != 0); Mx[c], Mx[p] = Mx[p], Mx[c]
            pv = Mx[c][c]; Mx[c] = [y / pv for y in Mx[c]]
            for r in range(n):
                if r != c and Mx[r][c] != 0:
                    f = Mx[r][c]; Mx[r] = [Mx[r][k] - f * Mx[c][k] for k in range(n + 1)]
        out[t] = Mx[idx[start]][n]
    return out
def hessian(g):
    C = g.C; c = len(C); P = [[[F(0)] * c for _ in range(c)] for a in (0, 1)]
    for i, v in enumerate(C):
        for a in (0, 1):
            law = first_passage(g, g.succ[v][a])
            for j, w in enumerate(C): P[a][i][j] = law[w]
    R = [[[F(int(i == j)) - P[a][i][j] for j in range(c)] for i in range(c)] for a in (0, 1)]
    B = [[sum(R[0][k][i] * R[1][k][j] + R[1][k][i] * R[0][k][j] for k in range(c)) / 2 for j in range(c)] for i in range(c)]
    return P, R, B
def matvec(A, d): return [sum(A[i][j] * d[j] for j in range(len(d))) for i in range(len(A))]
def quad(B, d): return sum(d[i] * sum(B[i][j] * d[j] for j in range(len(d))) for i in range(len(d)))
def minors(B):
    """leading principal minors (exact determinants)"""
    out = []
    for k in range(1, len(B) + 1):
        M = [row[:k] for row in B[:k]]; det = F(1); M = [r[:] for r in M]
        for c in range(k):
            p = next((r for r in range(c, k) if M[r][c] != 0), None)
            if p is None: det = F(0); break
            if p != c: M[c], M[p] = M[p], M[c]; det = -det
            det *= M[c][c]
            for r in range(c + 1, k):
                f = M[r][c] / M[c][c]; M[r] = [M[r][j] - f * M[c][j] for j in range(k)]
        out.append(det)
    return out
def psd(B):
    """exact test: all principal minors >= 0"""
    c = len(B)
    for S in itertools.chain.from_iterable(itertools.combinations(range(c), r) for r in range(1, c + 1)):
        sub = [[B[i][j] for j in S] for i in S]
        if minors(sub)[-1] < 0: return False
    return True
def load(fn):
    d = json.load(open(fn)); return Game(d['kinds'], d['succ'])
def allsw_longest(g, w=None):
    """longest all-switches run over all starts of a one-player game; also the outmap; nondegeneracy"""
    maxs = g.C; vals = {}
    for sig in itertools.product((0, 1), repeat=len(maxs)): vals[sig] = g.value(dict(zip(maxs, sig)))
    out = {}; ties = 0
    for sig, x in vals.items():
        S = set()
        for i, v in enumerate(maxs):
            other = x[g.succ[v][1 - sig[i]]]
            if other == x[v]: ties += 1
            elif other > x[v]: S.add(i)
        out[sig] = S
    best = 0; beststart = None
    for sig in vals:
        cur = sig; L = 0; seen = {cur}
        while out[cur]:
            cur = tuple(cur[i] ^ (1 if i in out[cur] else 0) for i in range(len(maxs))); L += 1
            assert cur not in seen; seen.add(cur)
        if L > best: best, beststart = L, sig
    outmap = [sum(1 << i for i in out[tuple((v >> i) & 1 for i in range(len(maxs)))]) for v in range(2 ** len(maxs))]
    return best, beststart, ties, outmap, vals
D = '/tmp/claude-1000/-data-ssg-proof/d1fe2115-9b72-4784-bb94-87421ac1106c/scratchpad/r17-variational/'
for name in ('CVX4_game.json', 'CVX6_game.json'):
    g = load(D + name); w = g.wstar(); P, R, B = hessian(g)
    L, start, ties, outmap, vals = allsw_longest(g)
    lm = minors(B)
    print(f"{name}: N = {g.n+2}, Max = {len(g.C)}, stopping = {g.is_stopping()}, tied incidences = {ties}, longest all-switches run = {L} from {start}, "
          f"outmap = {outmap}, w*|C = {[str(w[v]) for v in g.C]}, B = {[[str(x) for x in r] for r in B]}, leading minors = {[str(x) for x in lm]}, positive definite = {all(x > 0 for x in lm)}", flush=True)
# NCX: not in R (det B = -1/64); the cyclic game OL3 in R with the printed B; the ladder L_4 in R; G_8 in R; W_14 not in R
g = load(D + 'NCX_game.json'); P, R, B = hessian(g); print('NCX: B =', [[str(x) for x in r] for r in B], 'det =', minors(B)[-1], 'in R:', psd(B))
g = load('/data/ssg-proof/scripts/round17-verify/OL3_GAME.json'); P, R, B = hessian(g); print('OL3 (thm:cyclic-uso relabelled): B =', [[str(x) for x in r] for r in B], 'in R:', psd(B))
def ladder(n):  # def:ladder: v_i -> (v_{i+1}, w_{i+1}), w_i -> (v_{i+1}, w_{i+1}), v_{n+1} = t0, w_{n+1} = t1; v_i = i-1, w_i = n+i-1
    kinds = ['max'] * n + ['avg'] * n; succ = []
    for i in range(1, n + 1):
        nv = (i if i < n else 2 * n); nw = (n + i if i < n else 2 * n + 1); succ.append((nv, nw))
    for i in range(1, n + 1):
        nv = (i if i < n else 2 * n); nw = (n + i if i < n else 2 * n + 1); succ.append((nv, nw))
    return Game(kinds, succ)
g = ladder(4); P, R, B = hessian(g); print('L_4: in R:', psd(B), 'stopping', g.is_stopping())
g8 = Game(['max','avg','avg','avg','avg','avg','avg','avg'], None) if False else None
# G_8 of prop:simorder-stalls: taken from the round-16 harness (myinst.py G8) if present
try:
    sys.path.insert(0, '../root16'); import myinst
    kinds, succ = myinst.G8() if callable(getattr(myinst, 'G8', None)) else (None, None)
    if kinds: g = Game(kinds, [tuple(s) for s in succ]); P, R, B = hessian(g); print('G_8: in R:', psd(B))
except Exception as e: print('G_8 skipped:', e)
W14 = Game(['max','max','max','avg','avg','avg','avg','avg','avg','avg','avg','avg'], [(1,2),(3,4),(7,4),(13,12),(0,5),(0,6),(0,12),(12,8),(13,9),(13,10),(13,11),(13,12)])
P, R, B = hessian(W14); print('W_14: in R:', psd(B), 'B =', [[str(x) for x in r] for r in B])
# the two identities on random stopping games
rng = random.Random(5); cnt = 0
while cnt < 60:
    n = rng.randrange(4, 8); nm = rng.randrange(1, 3); nk = rng.randrange(0, 3)
    if nm + nk > n - 1: continue
    kinds = ['max'] * nm + ['min'] * nk + ['avg'] * (n - nm - nk); succ = [(rng.randrange(n + 2), rng.randrange(n + 2)) for _ in range(n)]
    g = Game(kinds, succ)
    if not g.is_stopping(): continue
    P, R, B = hessian(g); c = len(g.C)
    Pbar = [[(P[0][i][j] + P[1][i][j]) / 2 for j in range(c)] for i in range(c)]; Dl = [[P[1][i][j] - P[0][i][j] for j in range(c)] for i in range(c)]
    for _ in range(3):
        d = [F(rng.randrange(-5, 6), rng.randrange(1, 4)) for _ in range(c)]
        y = [d[i] - sum(Pbar[i][j] * d[j] for j in range(c)) for i in range(c)]; z = matvec(Dl, d)
        assert quad(B, d) == sum(x * x for x in y) - sum(x * x for x in z) / 4
        assert quad(B, d) == sum(matvec(R[0], d)[i] * matvec(R[1], d)[i] for i in range(c))
    cnt += 1
print(f'identities d^T B d = sum (R_0 d)(R_1 d) = |(I-Pbar)d|^2 - |Delta d|^2/4 verified on {cnt} random stopping games')
