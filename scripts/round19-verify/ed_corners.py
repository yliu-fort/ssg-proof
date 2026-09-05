#!/usr/bin/env python3
"""For every depth-3 node of cert_m3_d3.json and every remaining fourth query sigma_4: is the fourth query
PROVABLY informative for every member of K(D_3)?

With d the null vector of the readings (the plane d_0 + d'.x = 0 through x_1, x_2, x_3), a member W' of K(D_3) answers
sigma_4 on the plane iff g(lambda) := det(I - P') * (d_0 + d'.x_4') = 0, where only the three rows sigma_4 uses enter,
each moving along its fibre segment z + lambda d, so g is MULTI-AFFINE in (lambda_0, lambda_1, lambda_2) on the box of
the three segments. A multi-affine function on a box is a convex combination of its corner values, so if g has one
strict sign at all eight corners, no member of the box answers on the plane; det(I - P') > 0 on stopping members, so
the fourth query then raises the rank to 4 for EVERY consistent world and the datum determines the system
(rem:eval-fibre). A depth-3 node at which some sigma_4 is provably informative cannot head a depth-4 adversary
subtree with the recorded data, whatever NO world is chosen inside K(D_3).
Output: per node the number of provably informative fourth queries; the number of nodes with none (the only ones a
depth-4 extension could pass through).
"""
import sys, os, json, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); R18 = os.path.join(HERE, '..', 'round18-verify')
sys.path.insert(0, HERE)
from ed_depth4 import parse, value, nullvec, segment, strategies, m

def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))

def g_value(W, d, sig4, lams):
    R = dict(W)
    for key, lam in lams.items(): R[key] = tuple(W[key][j] + lam * d[j] for j in range(4))
    P = [R[(i, sig4[i])][1:] for i in range(m)]; q = [R[(i, sig4[i])][0] for i in range(m)]
    A = [[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)]
    val = d[0] * det3(A)
    for j in range(m):
        Mj = [row[:] for row in A]
        for i in range(m): Mj[i][j] = q[i]
        val += d[1 + j] * det3(Mj)
    return val

if __name__ == '__main__':
    cert = json.load(open(os.path.join(R18, 'cert_m3_d3.json')))
    nodes = {tuple(tuple(q) for q in c['queries']): c for c in cert}
    depth3 = sorted(k for k in nodes if len(k) == 3)
    hist = {}; rankdef = 0; open_nodes = []
    for key in depth3:
        W = parse(nodes[key]['no_rows'])
        xs = [value(W, tuple(s)) for s in key]; d = nullvec([[F(1)] + list(x) for x in xs])
        if d is None: rankdef += 1; open_nodes.append(key); continue
        segs = {k2: segment(W[k2], d) for k2 in W}
        informative = 0
        for sig4 in strategies:
            if sig4 in key: continue
            used = [(i, sig4[i]) for i in range(m)]
            signs = set()
            for corner in itertools.product((0, 1), repeat=3):
                lams = {used[i]: segs[used[i]][corner[i]] for i in range(3)}
                v = g_value(W, d, sig4, lams); signs.add((v > 0) - (v < 0))
            if signs in ({1}, {-1}): informative += 1
        hist[informative] = hist.get(informative, 0) + 1
        if informative == 0: open_nodes.append(key)
    print('depth-3 nodes by number of PROVABLY informative fourth queries (of 5):', dict(sorted(hist.items())), '; rank-deficient nodes:', rankdef)
    print(f'{len(open_nodes)} nodes with no provably informative fourth query (a depth-4 extension of this tree would have to pass through these only)')
    json.dump([list(map(list, k)) for k in open_nodes], open(os.path.join(HERE, 'ed_open_nodes.json'), 'w'))
