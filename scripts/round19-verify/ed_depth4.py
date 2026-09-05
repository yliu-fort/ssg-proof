#!/usr/bin/env python3
"""Is |C| + 1 or |C| + 2 exact at |C| = 3 for DECIDING val(v0) >= 1/2 from strategy evaluations (rem:eval-decide-gap)?

The rank argument (rem:eval-fibre, prop:eval-lift): after t queries the fibres have dimension m + 1 - rho(D) with
rho(D) = dim span{<x_r>}; at rho = m + 1 = 4 every fibre is a point and the datum determines the system. So an
adversary surviving a FOURTH query must answer it with x_4 in the affine hull of x_1, x_2, x_3 (then <x_4> lies in
the span, every member of K(D_3) has val_{sigma_4} = x_4, and K(D_4) = K(D_3): the fourth query is uninformative).
This script tries to extend the route's depth-3 certificate cert_m3_d3.json (scripts/round18-verify/) to depth 4:
for every depth-3 node (NO world W, queries sigma_1..sigma_3, YES witness Y) and every remaining strategy sigma_4,
it looks for W' in K(D_3) -- W with the three rows sigma_4 uses moved along their fibre segments -- such that
  (1) x_4' := val_{W',sigma_4} lies on the plane d_0 + d'.x = 0 through x_1, x_2, x_3 (d = the null vector of the
      3 x 4 matrix of readings; the condition is AFFINE in each single row's parameter, so it is solved exactly),
  (2) W' is stopping and nondegenerate, val*_{W'}(v0) < 1/2, and sigma_4 is strictly switchable somewhere in W',
and checks that Y reproduces the fourth answer (val_{Y,sigma_4} = x_4'). If every (node, sigma_4) extends, the
adversary survives four queries and FIVE evaluations are necessary at |C| = 3: decision = naming = |C| + 2 there.
The rows not used by sigma_4 are left as in W first; if that fails they are moved as well (they change val* only).
Writes cert_m3_d4.json (the depth-4 nodes) beside this script when the extension is complete.
"""
import sys, os, json, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
R18 = os.path.join(HERE, '..', 'round18-verify')
m = 3; V0 = 0
strategies = list(itertools.product((0, 1), repeat=m))

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

def parse(rows):
    R = {}
    for k, v in rows.items():
        i, a = map(int, k.split(',')); vals = [F(x) for x in v]
        assert len(vals) == m + 1 and all(x >= 0 for x in vals) and sum(vals) <= 1
        R[(i, a)] = tuple(vals)      # (q, p_0, p_1, p_2)
    return R

def unparse(R): return {f'{i},{a}': [str(x) for x in R[(i, a)]] for (i, a) in sorted(R)}

def stopping(R):
    for U in range(1, 1 << m):
        us = [i for i in range(m) if (U >> i) & 1]
        if all(any(R[(i, a)][0] == 0 and sum(R[(i, a)][1:]) == 1 and all(R[(i, a)][1 + j] == 0 for j in range(m) if not (U >> j) & 1) for a in (0, 1)) for i in us):
            return False
    return True

def value(R, sig):
    P = [R[(i, sig[i])][1:] for i in range(m)]; q = [R[(i, sig[i])][0] for i in range(m)]
    return solve([[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)], q)

def reading(z, x): return z[0] + sum(z[1 + j] * x[j] for j in range(m))

def analyse(R):
    """values per strategy, switchable sets, nondegenerate?, val* at v0 (one player: componentwise max)."""
    vals = {}; sw = {}; nondeg = True
    for sig in strategies:
        x = value(R, sig)
        if x is None: return None
        vals[sig] = x
        s = []
        for i in range(m):
            ap = reading(R[(i, 1 - sig[i])], x)
            if ap == x[i]: nondeg = False
            if ap > x[i]: s.append(i)
        sw[sig] = s
    star = max(vals[s][V0] for s in strategies)
    return vals, sw, nondeg, star

def nullvec(E):
    """a nonzero d with E d = 0 for a 3 x 4 matrix E of rank 3 (None if rank < 3)."""
    # Gaussian elimination to reduced form
    A = [list(r) for r in E]; rows = len(A); cols = 4; piv = []
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; pv = A[r][c]; A[r] = [x / pv for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [A[i][j] - f * A[r][j] for j in range(cols)]
        piv.append(c); r += 1
        if r == rows: break
    if len(piv) < 3: return None
    free = [c for c in range(cols) if c not in piv][0]
    d = [F(0)] * cols; d[free] = F(1)
    for i, c in enumerate(piv): d[c] = -A[i][free]
    return d

def segment(z, d):
    """[lo, hi] with z + lam d in Delta (all coordinates >= 0, mass <= 1)."""
    lo, hi = -F(10**9), F(10**9)
    for j in range(4):
        if d[j] > 0: lo = max(lo, -z[j] / d[j])
        elif d[j] < 0: hi = min(hi, -z[j] / d[j])
    sd = sum(d); sz = sum(z)
    if sd > 0: hi = min(hi, (1 - sz) / sd)
    elif sd < 0: lo = max(lo, (1 - sz) / sd)
    return lo, hi

def grid(lo, hi, k):
    return [lo + (hi - lo) * F(i, k) for i in range(k + 1)]

def try_extend(W, queries, Y, sig4, verbose=False):
    xs = [value(W, tuple(s)) for s in queries]
    E = [[F(1)] + list(x) for x in xs]
    d = nullvec(E)
    if d is None: return None, 'rank<3'
    plane = lambda x: d[0] + sum(d[1 + j] * x[j] for j in range(m))
    assert all(plane(x) == 0 for x in xs)
    used = [(i, sig4[i]) for i in range(m)]; others = [(i, 1 - sig4[i]) for i in range(m)]
    segs = {key: segment(W[key], d) for key in W}
    # the plane condition as an affine function of lambda_0 (row (0, sig4[0])) at fixed lambda_1, lambda_2:
    def cond(lams):
        R = dict(W)
        for key, lam in lams.items(): R[key] = tuple(W[key][j] + lam * d[j] for j in range(4))
        P = [R[(i, sig4[i])][1:] for i in range(m)]; q = [R[(i, sig4[i])][0] for i in range(m)]
        A = [[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)]
        # det(A) * plane(x_4) with x_4 = A^{-1} q, by Cramer: det(A) * (d_0 + sum_j d_{1+j} x_j)
        def det3(M): return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        dA = det3(A); val = d[0] * dA
        for j in range(m):
            Mj = [row[:] for row in A]
            for i in range(m): Mj[i][j] = q[i]
            val += d[1 + j] * det3(Mj)
        return val, R
    for K in (6, 12, 24):
        for lam1 in grid(*segs[used[1]], K):
            for lam2 in grid(*segs[used[2]], K):
                base = {used[1]: lam1, used[2]: lam2}
                g0, _ = cond({**base, used[0]: F(0)}); g1, _ = cond({**base, used[0]: F(1)})
                if g1 == g0:
                    cands = [F(0)] if g0 == 0 else []
                else:
                    cands = [-g0 / (g1 - g0)]
                lo, hi = segs[used[0]]
                for lam0 in cands:
                    if not (lo <= lam0 <= hi): continue
                    for oth in ([{}] + [{k: v} for k in others for v in grid(*segs[k], 4)]):
                        _, R = cond({**base, used[0]: lam0, **oth})
                        if not stopping(R): continue
                        an = analyse(R)
                        if an is None: continue
                        vals, sw, nondeg, star = an
                        if not nondeg or star >= F(1, 2) or not sw[sig4]: continue
                        x4 = vals[sig4]
                        assert plane(x4) == 0
                        # every member of K(D_3) must answer sigma_4 with x4: check the YES witness and W itself
                        assert value(Y, sig4) == x4 and value(W, sig4) != x4 or value(W, sig4) == x4
                        assert value(Y, sig4) == x4, 'YES witness does not reproduce the fourth answer'
                        # W' reproduces the three recorded answers (values and appeals)
                        for s in queries:
                            s = tuple(s); xw = value(W, s); assert value(R, s) == xw
                            for key in R: assert reading(R[key], xw) == reading(W[key], xw)
                        return R, 'ok'
    return None, 'not found'

if __name__ == '__main__':
    cert = json.load(open(os.path.join(R18, 'cert_m3_d3.json')))
    nodes = {tuple(tuple(q) for q in c['queries']): c for c in cert}
    depth3 = [k for k in nodes if len(k) == 3]
    print(f'{len(depth3)} depth-3 nodes; trying {5 * len(depth3)} fourth queries')
    new_nodes = []; fails = []; ranks = {}
    for key in sorted(depth3):
        c = nodes[key]; W = parse(c['no_rows']); Y = parse(c['yes_rows'])
        for sig4 in strategies:
            if sig4 in key: continue
            R, why = try_extend(W, key, Y, sig4)
            if R is None: fails.append((key, sig4, why)); continue
            vals, sw, nondeg, star = analyse(R)
            new_nodes.append({'queries': [list(s) for s in key] + [list(sig4)], 'no_rows': unparse(R), 'no_valstar': [str(x) for x in [max(vals[s][i] for s in strategies) for i in range(m)]],
                              'yes_sigma': c['yes_sigma'], 'yes_val': c['yes_val'], 'yes_rows': c['yes_rows']})
        done = len(new_nodes) + len(fails)
        if done % 200 == 0 or done == 5 * len(depth3): print(f'  {done}: {len(new_nodes)} extended, {len(fails)} failed', flush=True)
    print(f'extended {len(new_nodes)} of {5 * len(depth3)}; failures: {len(fails)}')
    for f in fails[:20]: print('  FAIL', f)
    if not fails:
        json.dump(cert + new_nodes, open(os.path.join(HERE, 'cert_m3_d4.json'), 'w'))
        print(f'cert_m3_d4.json written: {len(cert) + len(new_nodes)} nodes (8 + 56 + 336 + 1680); run ed_cert4.py to recheck it from the rows alone')
        print('FIVE EVALUATIONS ARE NECESSARY AT |C| = 3: the decision complexity equals the naming complexity |C| + 2 there')
