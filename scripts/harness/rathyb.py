"""The RATIO HYBRID: the transport polytope cut by MULTIPLICATIVE constraints
z(p) <= R(p,q) z(q) as well as by the difference constraints
z(p) - z(q) <= Delta(p,q).

Why it might matter.  In the coordinates xi = z - w* a difference cut is a
half-plane at distance Delta(p,q) - (w*(p)-w*(q)) from the origin, so an exact
difference cut passes through the apex only if the pair is already tight.  A
multiplicative cut z(p) <= R z(q) reads xi(p) <= R xi(q) + (R w*(q) - w*(p)),
whose constant vanishes exactly when R is exact -- so an exact ratio cut is a
CONE through the apex, which is the shape rem:wedge says defeats the difference
cuts.

|C| = 2, so the polytope is a polygon (lem:transport-dim) and everything is
exact.  Built on hyb2d.py's parametrisation.
"""
from fractions import Fraction as F

from mycore import Z01, slack_step, minplus_close, clamp, ones, check_sound
from hyb2d import affine_params, base_halfplanes
from ratio import INF
from t_rt2 import make_round, ratio_step_r, mintimes_close_r


def run(g, w, K, v1, v2, use_ratio=True, bround=None, verbose=False):
    theta, rho = affine_params(g, v1, v2)
    for x in range(g.N):
        assert theta[x][0] * w[v1] + theta[x][1] * w[v2] + rho[x] == w[x], ('lift', x)
    base = base_halfplanes(g, theta, rho, v1, v2)
    N = g.N
    Z0, Z1 = Z01(g, w)
    for x in range(g.n):                                  # the free Z-seed
        if x in Z0:
            base.append((theta[x], F(0) - rho[x]))
        if x in Z1:
            base.append(((-theta[x][0], -theta[x][1]), rho[x] - F(1)))
    a = sum(1 for k in g.kinds if k == 'avg')
    rnd = make_round(bround if bround is not None else 2 * a + 2, F(2) ** a)

    D = ones(N)
    R = [[INF] * N for _ in range(N)]
    histD, histR = [], []
    for k in range(K):
        A = [[clamp(v) for v in r] for r in minplus_close(slack_step(g, D, Z0, Z1), N)]
        D = [[min(D[i][j], A[i][j]) for j in range(N)] for i in range(N)]
        if use_ratio:
            R = mintimes_close_r(ratio_step_r(g, R, Z0, Z1, rnd), N, rnd)

        H = list(base)
        for p in range(N):
            for q in range(N):
                if p == q:
                    continue
                d = (theta[p][0] - theta[q][0], theta[p][1] - theta[q][1])
                if D[p][q] < 1 and d != (0, 0):
                    H.append((d, D[p][q] - rho[p] + rho[q]))
                if use_ratio and R[p][q] is not INF:
                    dm = (theta[p][0] - R[p][q] * theta[q][0],
                          theta[p][1] - R[p][q] * theta[q][1])
                    if dm != (0, 0):
                        H.append((dm, R[p][q] * rho[q] - rho[p]))
        V = clip_polygon(H)
        assert V, ('empty polygon at round %d -- w* must be feasible' % (k + 1))

        for p in range(N):
            zp = [theta[p][0] * x + theta[p][1] * y + rho[p] for (x, y) in V]
            for q in range(N):
                if p == q:
                    continue
                zq = [theta[q][0] * x + theta[q][1] * y + rho[q] for (x, y) in V]
                D[p][q] = min(D[p][q], clamp(max(a1 - a2 for a1, a2 in zip(zp, zq))))
                if use_ratio and all(t > 0 for t in zq):
                    cand = max(a1 / a2 for a1, a2 in zip(zp, zq))
                    if R[p][q] is INF or cand < R[p][q]:
                        R[p][q] = rnd(cand)
        D = [[clamp(v) for v in r] for r in minplus_close(D, N)]
        if use_ratio:
            R = mintimes_close_r(R, N, rnd)
            for p in range(N):
                for q in range(N):
                    if R[p][q] is not INF:
                        assert w[p] <= R[p][q] * w[q], ('unsound R', k, p, q)
        check_sound(g, D, w, 'r%d' % (k + 1))
        histD.append([r[:] for r in D])
        histR.append([r[:] for r in R])
        if verbose:
            print('   round', k + 1, 'vertices', len(V), flush=True)
    return histD, histR


def first_fire(g, histD, histR, ctrl, Z0):
    out = {}
    for v in ctrl:
        aa, bb = g.succ[v]
        out[v] = None
        for k in range(len(histD)):
            D, R = histD[k], histR[k]
            if g.kinds[v] == 'max':
                fired = (D[v][aa] <= 0 or D[v][bb] <= 0
                         or D[aa][v] < 0 or D[bb][v] < 0)
                for u in (aa, bb):
                    if R[v][u] is not INF and R[v][u] <= 1:
                        fired = True
                    if R[u][v] is not INF and R[u][v] < 1 and v not in Z0:
                        fired = True
            else:
                fired = (D[aa][v] <= 0 or D[bb][v] <= 0
                         or D[v][aa] < 0 or D[v][bb] < 0)
            if fired:
                out[v] = k + 1
                break
    return out


# --------------------------------------------------- fast exact 2-D clipping

def clip_polygon(H, box=(F(0), F(1))):
    """Vertices of {s in [lo,hi]^2 : a.s <= c}, by Sutherland-Hodgman clipping.
    O(|H| * |V|) instead of the O(|H|^3) pairwise-intersection routine."""
    lo, hi = box
    P = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
    for (a, b), c in H:
        if not P:
            return []
        out = []
        m = len(P)
        for i in range(m):
            x1, y1 = P[i]
            x2, y2 = P[(i + 1) % m]
            d1 = a * x1 + b * y1 - c
            d2 = a * x2 + b * y2 - c
            if d1 <= 0:
                out.append((x1, y1))
            if (d1 < 0 < d2) or (d2 < 0 < d1):
                t = d1 / (d1 - d2)
                out.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
        P = out
    # drop duplicates while keeping order
    seen, res = set(), []
    for p in P:
        if p not in seen:
            seen.add(p)
            res.append(p)
    return res
