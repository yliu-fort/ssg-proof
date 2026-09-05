#!/usr/bin/env python3
"""How common is a provably informative fourth query? Random stopping nondegenerate one-player dyadic systems on
|C| = 3, ALL 56 triples of distinct strategies as the first three queries (the datum D_3 taken from the system itself,
as an adversary answering truthfully from it would), and for each remaining strategy sigma_4 the corner-sign test of
ed_corners.py: g multi-affine on the box of the three fibre segments, one strict sign at all eight corners means no
member of K(D_3) answers sigma_4 on the plane through x_1, x_2, x_3, so the fourth query raises the rank to 4 for
every consistent world. Tallies: per triple the number of provably informative fourth queries (0..5), the rank of the
datum, and -- as a sanity check of the corner argument -- on a sample of (triple, sigma_4) pairs flagged informative,
the sign of the plane function at 200 random interior points of the box (must never vanish or change sign)."""
import sys, os, random, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ed_depth4 import value, nullvec, segment, analyse, stopping, strategies, m
from ed_corners import g_value

def random_system(rng, D=5):
    while True:
        R = {}
        for i in range(m):
            for a in (0, 1):
                w = [rng.randrange(0, 2 ** D) for _ in range(m + 1)]
                s = rng.randrange(max(sum(w), 1), 2 * max(sum(w), 1) + 1)   # mass <= 1, leaks with positive probability
                R[(i, a)] = tuple(F(x, s) for x in w)
        if not stopping(R): continue
        an = analyse(R)
        if an is None or not an[2]: continue
        return R

if __name__ == '__main__':
    rng = random.Random(1904)
    hist = {}; ranks = {}; checked = 0; sanity_bad = 0; systems = 0
    while systems < 60:
        W = random_system(rng); systems += 1
        vals = {s: value(W, s) for s in strategies}
        for triple in itertools.combinations(strategies, 3):
            E = [[F(1)] + list(vals[s]) for s in triple]; d = nullvec(E)
            if d is None: ranks['<3'] = ranks.get('<3', 0) + 1; continue
            ranks[3] = ranks.get(3, 0) + 1
            segs = {k: segment(W[k], d) for k in W}
            inf = 0
            for sig4 in strategies:
                if sig4 in triple: continue
                used = [(i, sig4[i]) for i in range(m)]
                signs = set()
                for corner in itertools.product((0, 1), repeat=3):
                    v = g_value(W, d, sig4, {used[i]: segs[used[i]][corner[i]] for i in range(3)}); signs.add((v > 0) - (v < 0))
                if signs in ({1}, {-1}):
                    inf += 1
                    if checked < 40:      # sanity: interior sampling
                        checked += 1; sgn = next(iter(signs))
                        for _ in range(200):
                            lams = {used[i]: segs[used[i]][0] + (segs[used[i]][1] - segs[used[i]][0]) * F(rng.randrange(1, 64), 64) for i in range(3)}
                            v = g_value(W, d, sig4, lams)
                            if (v > 0) - (v < 0) != sgn: sanity_bad += 1
            hist[inf] = hist.get(inf, 0) + 1
    print('systems:', systems, 'triples by rank:', ranks)
    print('rank-3 triples by number of provably informative fourth queries (of 5):', dict(sorted(hist.items())))
    print('sanity: interior samples contradicting the corner sign:', sanity_bad, 'of', checked * 200)
