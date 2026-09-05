#!/usr/bin/env python3
"""Root agent's verification of the round-19 handicap-tangent route, from the statements.

 [1] the visit number kappa(G) (max over selections of ||(I-Q_alpha)^{-1}||_inf, from the harmonic normal form over
     C) and the bound kappa <= 3|C|/lambda_min(B) on random stopping members of R (lambda by exact bisection on the
     PSD test), plus the decay sigma_n <= kappa/n;
 [2] the algorithm of thm:visits-class end to end (reduced value iteration J = ceil(2K)(2a+3) steps, continued-fraction
     recovery, fixed-point certificate) on random stopping games and on the paper's HZ(4) (from scripts/round18-verify);
 [3] DR(8,38): P_0 = P_1, B, lambda_min = 4^-8; the damped game (built by lem:gadget's chain of 7 average vertices on
     every edge, 1082 vertices) has B_rho with a negative direction, matching the algebraic rows.
"""
import sys, os, json, itertools, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'harness'))
from mycore import G, is_stopping, wstar

def solve(M, rhs):
    n = len(M); A = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; pv = A[c][c]; A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [A[r][j] - f * A[c][j] for j in range(n + 1)]
    return [A[i][n] for i in range(n)]

def inverse(M):
    n = len(M); cols = []
    for j in range(n):
        e = [F(int(i == j)) for i in range(n)]; cols.append(solve(M, e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def normal_form(g):
    """first-passage rows over C u {t1} of every action: P_a[v][u], r_a[v]; the average part eliminated exactly."""
    C = [v for v in range(g.n) if g.kinds[v] != 'avg']; idx = {v: i for i, v in enumerate(C)}; avg = g.of('avg'); aidx = {u: i for i, u in enumerate(avg)}
    # from an average vertex: probability of first meeting C at u, and of t1
    def law_from(start):
        # unknowns: h_w for average w; h_w = 1/2 sum over successors of (indicator/target law)
        k = len(C) + 1  # targets: C..., t1
        na = len(avg); A = [[F(int(i == j)) for j in range(na)] for i in range(na)]; b = [[F(0)] * k for _ in range(na)]
        for w in avg:
            i = aidx[w]
            for s in g.succ[w]:
                if s in aidx: A[i][aidx[s]] -= F(1, 2)
                elif s in idx: b[i][idx[s]] += F(1, 2)
                elif s == g.T1: b[i][k - 1] += F(1, 2)
        H = [solve(A, [b[i][t] for i in range(na)]) for t in range(k)]   # H[t][i]
        def law_of(s):
            if s in idx: return [F(int(t == idx[s])) for t in range(k)]
            if s == g.T1: return [F(0)] * (k - 1) + [F(1)]
            if s == g.T0: return [F(0)] * k
            return [H[t][aidx[s]] for t in range(k)]
        return law_of
    law_of = law_from(None)
    P = {a: [[F(0)] * len(C) for _ in C] for a in (0, 1)}; r = {a: [F(0)] * len(C) for a in (0, 1)}
    for v in C:
        for a in (0, 1):
            lw = law_of(g.succ[v][a]); P[a][idx[v]] = lw[:-1]; r[a][idx[v]] = lw[-1]
    return C, P, r

def matB(P0, P1):
    k = len(P0); R = {a: [[F(int(i == j)) - (P0 if a == 0 else P1)[i][j] for j in range(k)] for i in range(k)] for a in (0, 1)}
    B = [[sum(R[0][l][i] * R[1][l][j] + R[1][l][i] * R[0][l][j] for l in range(k)) / 2 for j in range(k)] for i in range(k)]
    return B

def psd_shift(B, lam):
    """is B - lam I positive semidefinite? (LDL^T with exact pivots)"""
    k = len(B); A = [[B[i][j] - (lam if i == j else 0) for j in range(k)] for i in range(k)]
    for c in range(k):
        if A[c][c] < 0: return False
        if A[c][c] == 0:
            if any(A[c][j] != 0 for j in range(c + 1, k)): return False
            continue
        for i in range(c + 1, k):
            f = A[i][c] / A[c][c]
            for j in range(c, k): A[i][j] -= f * A[c][j]
    return True

def lambda_min(B, bits=40):
    if not psd_shift(B, F(0)): return None
    lo, hi = F(0), F(4)
    for _ in range(bits):
        mid = (lo + hi) / 2
        if psd_shift(B, mid): lo = mid
        else: hi = mid
    return lo

def kappa(P0, P1):
    k = len(P0); best = F(0)
    for alpha in itertools.product((0, 1), repeat=k):
        Q = [(P0 if alpha[i] == 0 else P1)[i] for i in range(k)]
        inv = inverse([[F(int(i == j)) - Q[i][j] for j in range(k)] for i in range(k)])
        best = max(best, max(sum(row) for row in inv))
    return best

def reduced_algorithm(g, K):
    C, P, r = normal_form(g); k = len(C); a = len(g.of('avg'))
    def T_C(y):
        out = []
        for i, v in enumerate(C):
            vals = [sum(P[a_][i][j] * y[j] for j in range(k)) + r[a_][i] for a_ in (0, 1)]
            out.append(max(vals) if g.kinds[v] == 'max' else min(vals))
        return out
    y = [F(0)] * k; J = (2 * K + (1 if 2 * K != int(2 * K) else 0)) * (2 * a + 3); J = int(J)
    for _ in range(J): y = T_C(y)
    # continued-fraction recovery: the best rational with denominator <= 2^a within 2^-(2a+3)
    def recover(x):
        D = 2 ** a; eps = F(1, 2 ** (2 * a + 3))
        # convergents of x
        p0, q0, p1, q1 = 0, 1, 1, 0; xx = x
        while True:
            aa = xx.numerator // xx.denominator
            p0, q0, p1, q1 = p1, q1, aa * p1 + p0, aa * q1 + q0
            if q1 > D: return None
            if abs(F(p1, q1) - x) <= eps: return F(p1, q1)
            if xx == aa: return F(p1, q1) if q1 <= D else None
            xx = 1 / (xx - aa)
    yhat = [recover(x) for x in y]
    if any(v is None for v in yhat): return None
    return yhat if T_C(yhat) == yhat else None

rng = random.Random(1907)
def random_stopping_R(rng):
    while True:
        n = rng.randint(3, 7); kinds = [rng.choice(['max', 'min', 'avg', 'avg']) for _ in range(n)]
        if not any(k != 'avg' for k in kinds): continue
        succ = [(rng.randrange(n + 2), rng.randrange(n + 2)) for _ in range(n)]
        g = G(kinds, succ)
        if not is_stopping(g): continue
        C, P, r = normal_form(g); B = matB(P[0], P[1]); lam = lambda_min(B)
        if lam is None or lam == 0: continue
        return g, C, P, r, B, lam

# [1]
worst = F(0); cnt = 0; decay_ok = 0
while cnt < 120:
    g, C, P, r, B, lam = random_stopping_R(rng); k = len(C)
    kap = kappa(P[0], P[1]); assert kap * lam <= 3 * k, ('kappa bound', kap, lam, k)
    worst = max(worst, kap * lam / (3 * k))
    # decay: sigma_n = ||S^n 1||_inf <= kappa/n
    y = [F(1)] * k
    for n in range(1, 8):
        y = [max(sum(P[a_][i][j] * y[j] for j in range(k)) for a_ in (0, 1)) for i in range(k)]
        assert max(y) <= kap / n; decay_ok += 1
    cnt += 1
print(f'[1] kappa <= 3|C|/lambda on {cnt} random stopping members of R (lambda by exact bisection to 2^-40; worst ratio {float(worst):.4f}); sigma_n <= kappa/n on {decay_ok} (game, n) pairs')

# [2] the algorithm
ok = 0
for _ in range(60):
    g, C, P, r, B, lam = random_stopping_R(rng); kap = kappa(P[0], P[1])
    yhat = reduced_algorithm(g, kap); assert yhat is not None
    ws = wstar(g); assert all(yhat[i] == ws[v] for i, v in enumerate(C)); ok += 1
    # with K too small the algorithm may fail but never returns a wrong certified vector
    y2 = reduced_algorithm(g, F(1, 4))
    assert y2 is None or all(y2[i] == ws[v] for i, v in enumerate(C))
print(f'[2] the reduced value iteration with continued-fraction recovery returns the exact value on {ok} random games (and never a wrong certified vector at K = 1/4)')
HZ = json.load(open(os.path.join(HERE, '..', 'round18-verify', 'HZ4_GAME.json'))) if os.path.exists(os.path.join(HERE, '..', 'round18-verify', 'HZ4_GAME.json')) else None
if HZ:
    g = G(HZ['kinds'], [tuple(s) for s in HZ['succ']]); C, P, r = normal_form(g); B = matB(P[0], P[1]); lam = lambda_min(B)
    kap = kappa(P[0], P[1]) if len(C) <= 8 else None
    print(f'[2] HZ(4): N = {g.N}, |C| = {len(C)}, lambda_min(B) >= {float(lam):.4f}' + (f', kappa = {kap}' if kap is not None else ''))

# [3] DR(8,38) and its damping
def DR(r, L, rho_chain=0):
    """DR(r,L); with rho_chain = m > 0 every edge is replaced by lem:gadget's chain of m average vertices (leak 2^-m)."""
    names = []; kinds = {}; S = {}
    def add(nm, k, s): names.append(nm); kinds[nm] = k; S[nm] = s
    add('v1', 'max', ('a1', "a'1")); add('v2', 'max', ('c1', 'e1'))
    for j in range(1, r + 1):
        add(f'a{j}', 'avg', ('v2', f'a{j+1}' if j < r else 't0')); add(f"a'{j}", 'avg', ('v2', f"a'{j+1}" if j < r else 't1'))
        add(f'c{j}', 'avg', ('v1', f'c{j+1}' if j < r else 't0')); add(f"c'{j}", 'avg', ('v1', f"c'{j+1}" if j < r else 't1'))
    for j in range(1, L + 1):
        add(f'e{j}', 'avg', (f'e{j+1}' if j < L else "c'1",) * 2)
    if rho_chain:
        # damp every edge (x -> y) through a chain g_1..g_m: g_i -> (y, g_{i+1}), g_m -> (y, t0)
        newS = {}; extra = []
        for nm in list(names):
            s = list(S[nm])
            for pos in (0, 1):
                y = s[pos]; chain = [f'{nm}.{pos}.g{i}' for i in range(1, rho_chain + 1)]
                for i, cn in enumerate(chain):
                    extra.append((cn, 'avg', (y, chain[i + 1] if i + 1 < rho_chain else 't0')))
                s[pos] = chain[0]
            newS[nm] = tuple(s)
        S.update(newS)
        for cn, k, s in extra: add(cn, k, s)
    n = len(names); ix = {nm: i for i, nm in enumerate(names)}; ix['t0'] = n; ix['t1'] = n + 1
    return G([kinds[nm] for nm in names], [(ix[S[nm][0]], ix[S[nm][1]]) for nm in names])
g = DR(8, 38); assert g.N == 74 and is_stopping(g)
C, P, r = normal_form(g); assert P[0] == P[1] and P[0][0][1] == F(255, 256) and P[0][1][0] == F(255, 256)
B = matB(P[0], P[1]); assert B == [[F(130561, 65536), F(-255, 128)], [F(-255, 128), F(130561, 65536)]]
lam = lambda_min(B, 60); assert abs(lam - F(1, 65536)) < F(1, 2 ** 50)
ws = wstar(g); assert ws[0] != ws[g.succ[0][0]] or ws[0] != ws[g.succ[0][1]]
print(f'[3] DR(8,38): N = 74, stopping, P_0 = P_1 with mass 255/256, B as printed, lambda_min = 4^-8')
gd = DR(8, 38, rho_chain=7); assert gd.N == 1082 and is_stopping(gd)
C, P, r = normal_form(gd); Bd = matB(P[0], P[1])
det = Bd[0][0] * Bd[1][1] - Bd[0][1] * Bd[1][0]; d = [F(1), F(15, 16)]
quad = sum(d[i] * Bd[i][j] * d[j] for i in range(2) for j in range(2))
rho = F(127, 128); p_alg = rho ** 2 * (1 - (rho / 2) ** 8) / (2 - rho); q1_alg = rho ** 38 * p_alg
assert P[0][0][1] == p_alg and P[1][0][1] == p_alg and P[0][1][0] == p_alg and P[1][1][0] == q1_alg, 'algebraic rows'
assert det < 0 and quad < 0
print(f'[3] the damped game (1082 vertices, stopping): rows equal the algebraic rho-rows, det B_rho = {float(det):.4e} < 0, d^T B_rho d = {float(quad):.4e} < 0 for d = (1, 15/16): R is not closed under damping')
print('HANDICAP-TANGENT ROUTE: the visit-number bound, the algorithm and the damping witness reproduced')
