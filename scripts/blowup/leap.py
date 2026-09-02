"""Readable period signals along an all-switches run.
For the run sigma_0..sigma_L of a ONE-player game, and any two vertices p, q,
an outer Max vertex whose options are (affine) readouts of val(p), val(q)
flips exactly when the sign of  a*val_t(p) - b*val_t(q) - c  changes.
Count, over all lines, the maximal number of sign changes along the run,
i.e. the maximal number of times a reader of (p,q) can flip."""
import sys, itertools
sys.path.insert(0, '.')
from fractions import Fraction as F
import mycore as M
from my_allsw import ladder

def run(g, sigma):
    MX = g.of('max'); hist = []
    sigma = dict(sigma)
    for _ in range(10**4):
        val = M.profile_value(g, sigma, {})
        S = [v for v in MX if val[(lambda a, b: b if sigma[v] == a else a)(*g.succ[v])] > val[sigma[v]]]
        hist.append(val)
        if not S: return hist
        for v in S:
            a, b = g.succ[v]; sigma[v] = b if sigma[v] == a else a

def max_crossings(pts):
    """pts: list of (x_t, y_t) exact.  Max over lines of the number of strict
    sign alternations of a x - b y - c along t (a line is counted only if no
    point lies on it, after a tiny shift)."""
    L = len(pts); best = 0; bestline = None
    cands = []
    for i in range(L):
        for j in range(i + 1, L):
            (x1, y1), (x2, y2) = pts[i], pts[j]
            if (x1, y1) == (x2, y2): continue
            a, b = (y2 - y1), (x2 - x1)          # line: a*(x - x1) - b*(y - y1) = 0
            c = a * x1 - b * y1
            for eps in (F(1, 10**9), -F(1, 10**9)):
                cands.append((a, b, c + eps))
    # also axis-parallel lines through gaps
    xs = sorted(set(p[0] for p in pts)); ys = sorted(set(p[1] for p in pts))
    for u, v in zip(xs, xs[1:]): cands.append((F(1), F(0), (u + v) / 2))
    for u, v in zip(ys, ys[1:]): cands.append((F(0), F(-1), -(u + v) / 2))
    for (a, b, c) in cands:
        signs = [1 if a * x - b * y - c > 0 else (-1 if a * x - b * y - c < 0 else 0) for (x, y) in pts]
        if 0 in signs: continue
        k = sum(1 for s, s2 in zip(signs, signs[1:]) if s != s2)
        if k > best: best, bestline = k, (a, b, c)
    return best, bestline

if __name__ == '__main__':
    for n in range(3, 11):
        g = ladder(n)
        hist = run(g, {v: g.succ[v][0] for v in g.of('max')})
        L = len(hist) - 1
        best = (0, None)
        for p in range(g.n):
            for q in range(p + 1, g.n):
                pts = [(h[p], h[q]) for h in hist]
                k, line = max_crossings(pts)
                if k > best[0]: best = (k, (p, q, line))
        print(f'L_{n}: run length {L}; max readable flips over vertex pairs = {best[0]} at pair {best[1][:2] if best[1] else None}')
