"""The hybrid on a game with |C| = 2, computed exactly in the plane.

By lem:transport-dim every z in Q(G) is the harmonic extension of its
restriction to C, so with C = {v1, v2} the polytope lives in R^2:
    z(x) = theta_x[0] * s1 + theta_x[1] * s2 + rho_x.
Q(G) is then a convex polygon in (s1,s2), the difference cuts
z(p) - z(q) <= Delta(p,q) are half-planes, and
    Delta_{new}(p,q) = max over the polygon of (z(p) - z(q))
is a linear programme in two variables, solved exactly by evaluating at the
polygon's vertices.  No general simplex is needed and nothing is approximate.
"""
from fractions import Fraction as F
from mycore import Z01, slack_step, minplus_close, clamp, ones, check_sound


def affine_params(g, v1, v2):
    """z(x) = theta_x . (s1,s2) + rho_x, by solving the average system three
    times with (s1,s2) = (0,0), (1,0), (0,1)."""
    def solve(s1, s2):
        val = {g.T0: F(0), g.T1: F(1), v1: F(s1), v2: F(s2)}
        rest = [x for x in range(g.n) if x not in (v1, v2)]
        idx = {x: i for i, x in enumerate(rest)}
        mm = len(rest)
        A = [[F(0)] * mm for _ in range(mm)]
        b = [F(0)] * mm
        for x in rest:
            i = idx[x]
            A[i][i] += F(1)
            assert g.kinds[x] == 'avg', 'only the two controlled vertices may be controlled'
            for t in g.succ[x]:
                if t in idx:
                    A[i][idx[t]] -= F(1, 2)
                else:
                    b[i] += F(1, 2) * val[t]
        M = [A[i][:] + [b[i]] for i in range(mm)]
        for c in range(mm):
            p = next(r for r in range(c, mm) if M[r][c] != 0)
            M[c], M[p] = M[p], M[c]
            pv = M[c][c]
            M[c] = [x / pv for x in M[c]]
            for r in range(mm):
                if r != c and M[r][c] != 0:
                    f = M[r][c]
                    M[r] = [M[r][k] - f * M[c][k] for k in range(mm + 1)]
        out = dict(val)
        for x in rest:
            out[x] = M[idx[x]][mm]
        return out
    z00, z10, z01 = solve(0, 0), solve(1, 0), solve(0, 1)
    theta, rho = {}, {}
    for x in list(range(g.n)) + [g.T0, g.T1]:
        rho[x] = z00[x]
        theta[x] = (z10[x] - z00[x], z01[x] - z00[x])
    return theta, rho


def base_halfplanes(g, theta, rho, v1, v2):
    """rows of Q(G) as a . s <= c."""
    H = []

    def add(t, r, bound, upper):
        # theta.s + rho <= bound  (upper) or >= bound (lower)
        if upper:
            H.append(((t[0], t[1]), bound - r))
        else:
            H.append(((-t[0], -t[1]), r - bound))

    for x in range(g.n):
        add(theta[x], rho[x], F(1), True)
        add(theta[x], rho[x], F(0), False)
        a, b = g.succ[x]
        if g.kinds[x] == 'max':
            for u in (a, b):
                d = (theta[u][0] - theta[x][0], theta[u][1] - theta[x][1])
                H.append((d, rho[x] - rho[u]))          # z(u) - z(x) <= 0
        elif g.kinds[x] == 'min':
            for u in (a, b):
                d = (theta[x][0] - theta[u][0], theta[x][1] - theta[u][1])
                H.append((d, rho[u] - rho[x]))
    return H


def polygon(H):
    """vertices of {s : a.s <= c for all (a,c)}, by pairwise intersection."""
    pts = []
    n = len(H)
    for i in range(n):
        (a1, b1), c1 = H[i][0], H[i][1]
        for j in range(i + 1, n):
            (a2, b2), c2 = H[j][0], H[j][1]
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            if all(a * x + b * y <= c + 0 for (a, b), c in H):
                pts.append((x, y))
    return list(set(pts))


def hybrid2d(g, w, K, v1, v2, verbose=False):
    theta, rho = affine_params(g, v1, v2)
    for x in range(g.N):
        assert theta[x][0] * w[v1] + theta[x][1] * w[v2] + rho[x] == w[x], ('lift', x)
    base = base_halfplanes(g, theta, rho, v1, v2)
    N = g.N
    Z0, Z1 = Z01(g, w)
    # free seed: U = 0 on Z_0, L = 1 on Z_1
    for x in range(g.n):
        if x in Z0:
            base.append((theta[x], F(0) - rho[x]))
        if x in Z1:
            base.append(((-theta[x][0], -theta[x][1]), rho[x] - F(1)))
    D = ones(N)
    hist = []
    for k in range(K):
        A = [[clamp(v) for v in r] for r in minplus_close(slack_step(g, D, Z0, Z1), N)]
        M = [[min(D[i][j], A[i][j]) for j in range(N)] for i in range(N)]
        H = list(base)
        for p in range(N):
            for q in range(N):
                if p == q or M[p][q] >= 1:
                    continue
                d = (theta[p][0] - theta[q][0], theta[p][1] - theta[q][1])
                if d == (0, 0):
                    continue
                H.append((d, M[p][q] - rho[p] + rho[q]))
        V = polygon(H)
        assert V, 'empty polygon -- w* must be feasible'
        for p in range(N):
            for q in range(N):
                if p == q:
                    continue
                d = (theta[p][0] - theta[q][0], theta[p][1] - theta[q][1])
                c = rho[p] - rho[q]
                best = max(d[0] * x + d[1] * y for (x, y) in V) + c
                M[p][q] = min(M[p][q], clamp(best))
        M = [[clamp(v) for v in r] for r in minplus_close(M, N)]
        check_sound(g, M, w, f'r{k+1}')
        D = M
        hist.append([r[:] for r in D])
    return hist


def first_fire(g, w, hist, ctrl):
    out = {}
    for v in ctrl:
        a, b = g.succ[v]
        out[v] = None
        for k, D in enumerate(hist):
            if g.kinds[v] == 'max':
                fired = (D[v][a] <= 0 or D[v][b] <= 0 or D[a][v] < 0 or D[b][v] < 0)
            else:
                fired = (D[a][v] <= 0 or D[b][v] <= 0 or D[v][a] < 0 or D[v][b] < 0)
            if fired:
                out[v] = k + 1
                break
    return out
