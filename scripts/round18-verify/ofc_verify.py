#!/usr/bin/env python3
"""Root-agent verification of ue:cheb: OFC(D,k) rebuilt from the statement. The seed x_0, y_0 are the two dyadic rows
2^{-K} sum_d (A_d)_+/- rho^{K+d} of Tt_k(rho) := T_k(2 rho - 1) = sum_d A_d rho^d, realised on a shared chain
q_l -> (q_{l-1}, q_{l-1}), q_0 = t1 (value rho^l in the damped game) by pruned binary trees of average vertices in
which the leaf for the digit 2^b of |A_d| sits at depth K-b and points at q_{d+b}; the constants come from the halving
chain c_j -> (c_{j-1}, t0), c_0 = t1, through Y_d -> (R_d, c_{K-1+3d}). Exact arithmetic."""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from of_verify import damped_values, Td, gated_game, is_stopping, G

def cheb_coeffs(k):
    """integer coefficients A_0..A_k of T_k(2 rho - 1) as a polynomial in rho."""
    def mul(p, q):
        r = [0]*(len(p)+len(q)-1)
        for i, a in enumerate(p):
            for j, b in enumerate(q): r[i+j] += a*b
        return r
    def sub(p, q):
        r = [0]*max(len(p), len(q))
        for i, a in enumerate(p): r[i] += a
        for i, b in enumerate(q): r[i] -= b
        return r
    x = [-1, 2]                       # 2 rho - 1
    P = [[1], x]
    for j in range(1, k): P.append(sub(mul([-2, 4], P[j]), P[j-1]))   # P_{j+1} = (4 rho - 2) P_j - P_{j-1}
    return P[k]

def prefix_tree(leaves, tag):
    """leaves: list of (target, depth). Build a binary tree of average vertices realising mass 2^{-depth} to each target
    (Kraft: sum 2^{-depth} <= 1); returns (root, adds) where adds is a list of (name, kind, (s0, s1)); unused leaves -> t0."""
    leaves = sorted(leaves, key=lambda t: t[1])
    assert sum(F(1, 2**d) for _, d in leaves) <= 1
    adds = []; counter = [0]
    def node(depth, pending):
        # pending: leaves to place in this subtree (all with depth >= current depth)
        if not pending: return 't0'
        if len(pending) == 1 and pending[0][1] == depth: return pending[0][0]
        assert all(d > depth for _, d in pending)
        # split pending into two halves by capacity: greedily fill the left child
        left, right, cap = [], [], F(0)
        for t, d in pending:
            if cap + F(1, 2**(d-depth-1)) <= 1: left.append((t, d)); cap += F(1, 2**(d-depth-1))
            else: right.append((t, d))
        nm = (tag, counter[0]); counter[0] += 1
        s0 = node(depth+1, left); s1 = node(depth+1, right)
        adds.append((nm, 'avg', (s0, s1)))
        return nm
    root = node(0, leaves)
    return root, adds

def build_OFC(D, k):
    A = cheb_coeffs(k); K = 0
    while 2**K < sum(abs(a) for a in A): K += 1
    names, kinds, succ = [], [], []
    def add(nm, kd, s): names.append(nm); kinds.append(kd); succ.append(s)
    # shared chain q_l, l = 1..K+k
    for l in range(1, K+k+1): add(('q', l), 'avg', (('q', l-1) if l > 1 else 't1', ('q', l-1) if l > 1 else 't1'))
    # halving chain c_j, j = 1..K-1+3D
    for j in range(1, K+3*D): add(('c', j), 'avg', (('c', j-1) if j > 1 else 't1', 't0'))
    def row(sign):
        leaves = []
        for d, a in enumerate(A):
            v = a if sign > 0 else -a
            if v <= 0: continue
            b = 0
            while v:
                if v & 1: leaves.append((('q', d+b) if d+b > 0 else 't1', K-b))
                v >>= 1; b += 1
        return leaves
    rootX, addsX = prefix_tree(row(+1), 'ax'); rootY, addsY = prefix_tree(row(-1), 'ay')
    for nm, kd, s in addsX + addsY: add(nm, kd, s)
    # X0, Y0 are the roots themselves (or a trivial vertex if the row is empty/a single leaf)
    def alias(nm, root):
        if isinstance(root, tuple) and root[0] in ('ax', 'ay'): names[names.index(root)] = nm
        else: assert root == 't0'; add(nm, 'avg', ('t0', 't0'))   # empty row only
        return nm
    X0 = alias('X0', rootX); Y0 = alias('Y0', rootY)
    # fix references to renamed roots
    succ[:] = [tuple(('X0' if x == rootX and rootX != X0 else 'Y0' if x == rootY and rootY != Y0 else x) for x in s) for s in succ]
    add('F0', 'max', ('X0', 'Y0'))
    for d in range(D): add(('H', d), 'avg', (('X', d) if d > 0 else 'X0', ('Y', d) if d > 0 else 'Y0'))
    for d in range(1, D+1):
        add(('P', d), 'avg', (('F', d-1) if d > 1 else 'F0', ('F', d-1) if d > 1 else 'F0'))
        add(('X', d), 'avg', (('P', d), 't0'))
        add(('R', d), 'avg', (('H', d-1), ('H', d-1)))
        add(('Y', d), 'avg', (('R', d), ('c', K-1+3*d)))
        add(('F', d), 'max', (('X', d), ('Y', d)))
    n = len(names); idx = {nm: i for i, nm in enumerate(names)}; idx['t0'] = n; idx['t1'] = n+1
    return names, kinds, [(idx[a], idx[b]) for a, b in succ], idx, A, K

def Tt(A, rho): return sum(a * rho**d for d, a in enumerate(A))

if __name__ == '__main__':
    rhos = [F(1,3), F(2,7), F(5,11), F(7,9), F(13,16), F(41,97)]
    for k in range(1, 7):
        for D in range(0, 5):
            names, kinds, succ, idx, A, K = build_OFC(D, k)
            g = G(kinds, succ); assert is_stopping(g) and kinds.count('min') == 0 and kinds.count('max') == D+1
            for rho in rhos:
                v = damped_values(kinds, succ, rho)
                e0 = (rho/2)**K
                x0 = v[idx['X0']]; y0 = v[idx['Y0']]
                assert x0 - y0 == e0 * Tt(A, rho), (D, k, rho)
                u0 = (1 + Tt(A, rho)) / 2
                for d in range(D+1):
                    e = e0 * (rho**3/8)**d
                    X = v[idx['X0']] if d == 0 else v[idx[('X', d)]]; Y = v[idx['Y0']] if d == 0 else v[idx[('Y', d)]]
                    assert (X - Y)/e == 2*Td(u0, d) - 1, (D, k, rho, d)
            print(f'OFC({D},{k}): n={len(names)}, K={K}, A={A}, stopping, one player, m={D+1}; psi_d = 2T^d(u_0)-1 at {len(rhos)} rationals')
    # breakpoint counts per level by sign changes on a fine grid (k 2^d per level, total k(2^{D+1}-1))
    for k in (1, 2, 3, 4):
        for D in (0, 1, 2, 3):
            names, kinds, succ, idx, A, K = build_OFC(D, k)
            Mg = 400 * k * 2**(D+1)
            prev = None; counts = [0]*(D+1)
            for t in range(1, Mg):
                rho = F(t, Mg); v = damped_values(kinds, succ, rho)
                sg = tuple((v[idx['X0']] if d == 0 else v[idx[('X', d)]]) > (v[idx['Y0']] if d == 0 else v[idx[('Y', d)]]) for d in range(D+1))
                if prev is not None:
                    for d in range(D+1):
                        if sg[d] != prev[d]: counts[d] += 1
                prev = sg
            assert counts == [k * 2**d for d in range(D+1)], (k, D, counts)
            print(f'OFC({D},{k}): sign changes per level {counts} = k*2^d, total {sum(counts)} = k(2^(D+1)-1) = {k*(2**(D+1)-1)}')
    # from the game with rho-gates
    for D, k, rho in [(0, 2, F(3,8)), (1, 2, F(7,16)), (0, 3, F(5,16)), (2, 2, F(9,32))]:
        names, kinds, succ, idx, A, K = build_OFC(D, k)
        gg, N = gated_game(kinds, succ, rho); assert is_stopping(gg)
        # one-player acyclic: backward induction on the gated game with max at Max vertices, then compare
        n2 = gg.n; memo = {}
        def val(v):
            if v == n2: return F(0)
            if v == n2+1: return F(1)
            if v in memo: return memo[v]
            a, b = gg.succ[v]
            r = max(val(a), val(b)) if gg.kinds[v] == 'max' else (val(a)+val(b))/2
            memo[v] = r; return r
        w = [val(v) for v in range(len(names))]
        v = damped_values(kinds, succ, rho)
        assert w == v, (D, k, rho)
        print(f'OFC({D},{k})_rho, rho={rho}: gated SSG on {N+2} vertices, stopping, values from the gated game == damped values at all {len(names)} vertices')
    # sizes
    print('sizes n(D,k):', {(D, k): build_OFC(D, k)[0].__len__() for D in (0, 3) for k in (1, 2, 3, 4, 5, 6, 8)})
    print('ALL OFC CHECKS PASSED')
