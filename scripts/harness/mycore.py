"""SSG core + the four mechanisms, written from the statements in frontier.tex.

Root-agent copy for round 10.  Deliberately independent of the round-9 harness.
Exact rational arithmetic throughout.  Vertices 0..n-1 are non-sinks; T0 = n,
T1 = n+1.
"""
from fractions import Fraction as F
from itertools import product


class G:
    def __init__(self, kinds, succ):
        self.kinds = list(kinds)
        self.succ = [tuple(s) for s in succ]
        self.n = len(kinds)
        self.T0, self.T1 = self.n, self.n + 1
        self.N = self.n + 2
        assert all(k in ('max', 'min', 'avg') for k in self.kinds)
        assert all(0 <= u < self.N for s in self.succ for u in s)

    def of(self, k):
        return [v for v in range(self.n) if self.kinds[v] == k]


# ---------------------------------------------------------------- values

def _lin_solve(A, b):
    m = len(A)
    M = [list(A[i]) + [b[i]] for i in range(m)]
    for col in range(m):
        piv = next((r for r in range(col, m) if M[r][col] != 0), None)
        assert piv is not None, "singular"
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(m):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[col][c] for c in range(m + 1)]
    return [M[i][m] for i in range(m)]


def profile_value(g, sigma, tau):
    """Value under the positional pair; correct on NON-stopping games too, by
    restricting the linear system to the vertices that can reach t1 at all."""
    dist = []
    for v in range(g.n):
        k = g.kinds[v]
        if k == 'max':
            dist.append({sigma[v]: F(1)})
        elif k == 'min':
            dist.append({tau[v]: F(1)})
        else:
            d = {}
            for u in g.succ[v]:                       # accumulate: successors may coincide
                d[u] = d.get(u, F(0)) + F(1, 2)
            dist.append(d)
    reach = {g.T1}
    changed = True
    while changed:
        changed = False
        for v in range(g.n):
            if v not in reach and any(u in reach for u in dist[v]):
                reach.add(v)
                changed = True
    R = sorted(v for v in range(g.n) if v in reach)
    val = [F(0)] * g.N
    val[g.T1] = F(1)
    if not R:
        return val
    idx = {v: i for i, v in enumerate(R)}
    m = len(R)
    A = [[F(0)] * m for _ in range(m)]
    b = [F(0)] * m
    for v in R:
        i = idx[v]
        A[i][i] += F(1)
        for u, p in dist[v].items():
            if u == g.T1:
                b[i] += p
            elif u in idx:
                A[i][idx[u]] -= p
    x = _lin_solve(A, b)
    for v in R:
        val[v] = x[idx[v]]
    return val


def wstar(g):
    """max over sigma of min over tau -- brute force, never greedy iteration."""
    MX, MN = g.of('max'), g.of('min')
    best = None
    for sc in (product(*[[0, 1]] * len(MX)) if MX else [()]):
        sigma = {v: g.succ[v][sc[i]] for i, v in enumerate(MX)}
        cur = None
        for tc in (product(*[[0, 1]] * len(MN)) if MN else [()]):
            tau = {v: g.succ[v][tc[i]] for i, v in enumerate(MN)}
            val = profile_value(g, sigma, tau)
            cur = val if cur is None else [min(a, b) for a, b in zip(cur, val)]
        best = cur if best is None else [max(a, b) for a, b in zip(best, cur)]
    return best


def T_op(g, x):
    y = list(x)
    for v in range(g.n):
        a, b = g.succ[v]
        k = g.kinds[v]
        y[v] = max(x[a], x[b]) if k == 'max' else (min(x[a], x[b]) if k == 'min' else (x[a] + x[b]) / 2)
    y[g.T0], y[g.T1] = F(0), F(1)
    return y


def is_stopping(g):
    """lem:trapchar: U is a trap if every avg vertex of U has BOTH successors in
    U and every controlled vertex has SOME.  G is stopping iff the only trap is
    empty.  Computed as the greatest such U inside the non-sinks."""
    U = set(range(g.n))
    changed = True
    while changed:
        changed = False
        for v in list(U):
            a, b = g.succ[v]
            ok = (a in U and b in U) if g.kinds[v] == 'avg' else (a in U or b in U)
            if not ok:
                U.discard(v)
                changed = True
    return not U


def Z01(g, w):
    return ({v for v in range(g.N) if w[v] == 0}, {v for v in range(g.N) if w[v] == 1})


# ---------------------------------------------------------------- slack calculus

def clamp(x):
    return F(-1) if x < -1 else (F(1) if x > 1 else x)


def _agp(g, x, a, b):          # (up):   bound on w*(x) - w*(y) from the x-side
    k = g.kinds[x]
    return max(a, b) if k == 'max' else (min(a, b) if k == 'min' else (a + b) / 2)


def _agm(g, y, a, b):          # (down): bound from the y-side
    k = g.kinds[y]
    return min(a, b) if k == 'max' else (max(a, b) if k == 'min' else (a + b) / 2)


def slack_step(g, D, Z0, Z1):
    """One round of def:slack.  D is the current N x N matrix."""
    N = g.N
    out = [[F(1)] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            c = [F(1)]
            if x in Z0 and y in Z1:
                c.append(F(-1))
            elif x in Z0 or y in Z1:
                c.append(F(0))
            if x == y:
                c.append(F(0))
            if y < g.n:
                y0, y1 = g.succ[y]
                c.append(_agm(g, y, D[x][y0], D[x][y1]))
            if x < g.n:
                x0, x1 = g.succ[x]
                c.append(_agp(g, x, D[x0][y], D[x1][y]))
            if x < g.n and y < g.n and g.kinds[x] == g.kinds[y]:
                x0, x1 = g.succ[x]
                y0, y1 = g.succ[y]
                k = g.kinds[x]
                if k == 'avg':
                    c.append((D[x0][y0] + D[x1][y1]) / 2)
                    c.append((D[x0][y1] + D[x1][y0]) / 2)
                elif k == 'max':
                    c.append(max(min(D[x0][y0], D[x0][y1]), min(D[x1][y0], D[x1][y1])))
                    c.append(min(max(D[x0][y0], D[x1][y0]), max(D[x0][y1], D[x1][y1])))
                else:
                    c.append(min(max(D[x0][y0], D[x0][y1]), max(D[x1][y0], D[x1][y1])))
                    c.append(max(min(D[x0][y0], D[x1][y0]), min(D[x0][y1], D[x1][y1])))
            out[x][y] = clamp(min(c))
    return out


def minplus_close(D, N):
    """def:trans-slack: all-pairs min-plus (Floyd-Warshall) closure."""
    A = [r[:] for r in D]
    for k in range(N):
        Ak = A[k]
        for i in range(N):
            aik = A[i][k]
            Ai = A[i]
            for j in range(N):
                s = aik + Ak[j]
                if s < Ai[j]:
                    Ai[j] = s
    return A


def ones(N):
    return [[F(1)] * N for _ in range(N)]


def check_sound(g, D, w, tag=''):
    for i in range(g.N):
        for j in range(g.N):
            assert D[i][j] >= w[i] - w[j], ('UNSOUND', tag, i, j, D[i][j], w[i] - w[j])


# ---------------------------------------------------------------- transport LP

def _row(g, v):
    """The affine form of x(v): (dict over non-sink variables, constant)."""
    if v == g.T0:
        return {}, F(0)
    if v == g.T1:
        return {}, F(1)
    return {v: F(1)}, F(0)


def _sub(d1, c1, d2, c2):
    d = dict(d1)
    for k, val in d2.items():
        d[k] = d.get(k, F(0)) - val
    return {k: v for k, v in d.items() if v != 0}, c1 - c2


def transport_rows(g, D=None, L=None, U=None):
    """Rows of Q(G;L,U), optionally tightened by difference bounds D.
    Returns (A, b) for A x <= b with variables x_0..x_{n-1}."""
    A, b = [], []

    def push(d, c):                     # d.x + c <= 0   ->   d.x <= -c
        row = [F(0)] * g.n
        for k, v in d.items():
            row[k] += v
        A.append(row)
        b.append(-c)

    for v in range(g.n):
        a0, a1 = g.succ[v]
        dv, cv = _row(g, v)
        for u in (a0, a1):
            du, cu = _row(g, u)
            if g.kinds[v] == 'max':          # x(u) - x(v) <= 0
                d, c = _sub(du, cu, dv, cv)
                push(d, c)
            elif g.kinds[v] == 'min':        # x(v) - x(u) <= 0
                d, c = _sub(dv, cv, du, cu)
                push(d, c)
        if g.kinds[v] == 'avg':              # x(v) = (x(a0)+x(a1))/2, both ways
            d0, c0 = _row(g, a0)
            d1, c1 = _row(g, a1)
            dm, cm = {}, F(0)
            for dd, cc in ((d0, c0), (d1, c1)):
                for k, val in dd.items():
                    dm[k] = dm.get(k, F(0)) + val / 2
                cm += cc / 2
            dm = {k: v for k, v in dm.items() if v != 0}
            d, c = _sub(dv, cv, dm, cm)
            push(d, c)
            d, c = _sub(dm, cm, dv, cv)
            push(d, c)
    for v in range(g.n):
        lo = F(0) if L is None else L[v]
        hi = F(1) if U is None else U[v]
        r = [F(0)] * g.n
        r[v] = F(1)
        A.append(r[:])
        b.append(hi)
        r2 = [F(0)] * g.n
        r2[v] = F(-1)
        A.append(r2)
        b.append(-lo)
    if D is not None:                        # x(p) - x(q) <= D[p][q]
        for p in range(g.N):
            for q in range(g.N):
                if p == q or D[p][q] >= 1:
                    continue
                dp, cp = _row(g, p)
                dq, cq = _row(g, q)
                d, c = _sub(dp, cp, dq, cq)
                if not d:
                    continue
                row = [F(0)] * g.n
                for k, v in d.items():
                    row[k] += v
                A.append(row)
                b.append(D[p][q] - c)
    return A, b


def transport_sep(g, pairs, D=None, L=None, U=None):
    """Sep(p,q) = max{x(q)-x(p)} over the (tightened) transport polytope."""
    A, b = transport_rows(g, D=D, L=L, U=U)
    S = LPclass(A, b, g.n)
    if not S.feasible:
        raise RuntimeError('INFEASIBLE transport polytope')
    out = {}
    for (p, q) in pairs:
        dq, cq = _row(g, q)
        dp, cp = _row(g, p)
        d, c = _sub(dq, cq, dp, cp)
        if not d:
            out[(p, q)] = clamp(c)
            continue
        cvec = [d.get(j, F(0)) for j in range(g.n)]
        v = S.maximize(cvec)
        out[(p, q)] = None if v is None else clamp(v + c)
    return out


from mylp import LP as LPclass                     # noqa: E402


# ---------------------------------------------------------------- the hybrid

def hybrid(g, w, K, use_lp=True, trans=True, seed=None, stop_pair=None, verbose=False):
    """Delta_0 = seed (all ones by default).  Each round: slack step, min-plus
    closure, then (if use_lp) re-derive every pair by maximising over Q(G)
    tightened by the current matrix, then close again.  Soundness asserted every
    round against the true w*.  Returns the list of matrices."""
    N = g.N
    Z0, Z1 = Z01(g, w)
    D = ones(N) if seed is None else [r[:] for r in seed]
    hist = []
    for k in range(K):
        A = slack_step(g, D, Z0, Z1)
        if trans:
            A = [[clamp(v) for v in r] for r in minplus_close(A, N)]
        M = [[min(D[i][j], A[i][j]) for j in range(N)] for i in range(N)]
        if use_lp:
            pairs = [(p, q) for p in range(N) for q in range(N) if p != q]
            sep = transport_sep(g, pairs, D=M)
            for (p, q), v in sep.items():
                if v is not None:
                    # Sep(p,q) bounds w*(q) - w*(p), i.e. it is a bound on D[q][p]
                    M[q][p] = min(M[q][p], v)
        if trans:
            M = [[clamp(v) for v in r] for r in minplus_close(M, N)]
        D = M
        check_sound(g, D, w, tag=f'round{k+1}')
        hist.append([r[:] for r in D])
        if verbose:
            print(f'  round {k+1}', {f'{p}->{q}': str(D[p][q]) for (p, q) in ([stop_pair] if stop_pair else [])})
        if stop_pair and D[stop_pair[0]][stop_pair[1]] < 0:
            break
    return hist


def first_negative(hist, x, y):
    for k, D in enumerate(hist):
        if D[x][y] < 0:
            return k + 1
    return None


def distinguishing(g, w):
    """Controlled vertices whose two successors have different optimal values."""
    return [v for v in range(g.n) if g.kinds[v] in ('max', 'min')
            and w[g.succ[v][0]] != w[g.succ[v][1]]]
