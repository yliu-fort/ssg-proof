#!/usr/bin/env python3
"""ed:rational-row: a row of rationals r_1..r_l >= 0 with common denominator D and sum <= 1 is realised by a gadget of
fair-coin average vertices with a rejection loop: the complete binary tree of depth d = ceil(log2 D), leaf i -> w_j when
K_{j-1} <= i < K_j, -> t_0 when K_l <= i < D, back to the entry when i >= D; nodes whose leaf interval carries one
assignment are pruned. Exit probabilities solved exactly; node count <= (l+2)d."""
from fractions import Fraction as F
import math

def gadget(r):
    D = 1
    for x in r: D = D * x.denominator // math.gcd(D, x.denominator)
    K = [0]
    for x in r: K.append(K[-1] + int(x * D))
    l = len(r); d = max(1, math.ceil(math.log2(D))) if D > 1 else 0
    if d == 0: return {}, ('w', 0) if r and r[0] == 1 else 't0', D, 0
    def assign(i):
        if i >= D: return 'entry'
        if i >= K[-1]: return 't0'
        return ('w', next(j for j in range(l) if K[j] <= i < K[j + 1]))
    nodes = {}
    def build(depth, lo):   # node covering leaves [lo, lo + 2^(d-depth))
        span = 1 << (d - depth)
        assigns = {assign(i) for i in range(lo, lo + span)}
        if len(assigns) == 1: return assigns.pop()
        nm = ('n', depth, lo); nodes[nm] = (build(depth + 1, lo), build(depth + 1, lo + span // 2)); return nm
    root = build(0, 0)
    return nodes, root, D, d

def exits(nodes, root, l):
    """solve h_t(node) = prob of exiting at target t, with 'entry' = the root (rejection loop)."""
    names = list(nodes); idx = {nm: i for i, nm in enumerate(names)}; n = len(names)
    out = {}
    for t in [('w', j) for j in range(l)] + ['t0']:
        A = [[F(int(i == j)) for j in range(n)] for i in range(n)]; b = [F(0)] * n
        for nm, (a, c) in nodes.items():
            for s in (a, c):
                s2 = root if s == 'entry' else s
                if s2 in idx: A[idx[nm]][idx[s2]] -= F(1, 2)
                elif s2 == t: b[idx[nm]] += F(1, 2)
        # Gaussian elimination
        T = [A[i] + [b[i]] for i in range(n)]
        for col in range(n):
            p = next(rr for rr in range(col, n) if T[rr][col] != 0); T[col], T[p] = T[p], T[col]; pv = T[col][col]; T[col] = [x / pv for x in T[col]]
            for rr in range(n):
                if rr != col and T[rr][col] != 0:
                    f = T[rr][col]; T[rr] = [T[rr][j] - f * T[col][j] for j in range(n + 1)]
        out[t] = T[idx[root]][n] if root in idx else F(int(root == t))
    return out

for r in ([F(1,3), F(1,3)], [F(2,7), F(3,7)], [F(1,5)], [F(4,15), F(1,3), F(2,5)], [F(1,3)]*3, [F(3,8)], [F(11,13)], [F(7,37), F(9,37), F(20,37)]):
    nodes, root, D, d = gadget(r); ex = exits(nodes, root, len(r))
    assert all(ex[('w', j)] == r[j] for j in range(len(r))) and ex['t0'] == 1 - sum(r)
    assert len(nodes) <= (len(r) + 2) * d
    print(f'row {[str(x) for x in r]}: D={D}, depth {d}, {len(nodes)} average vertices (bound {(len(r)+2)*d}); exact exit probabilities, residue to t0 = {ex["t0"]}')
print('RATIONAL-ROW GADGET CONFIRMED')
