"""Root-agent (session ef1cfad9) implementation of def:bsi and of all-switches,
written from the statements in frontier.tex, independent of any route code.
Exact rational arithmetic.  Vertices 0..n-1 non-sinks, T0 = n, T1 = n+1.
"""
from fractions import Fraction as F
from itertools import product
import mycore as M

def is_stopping(g):
    return M.is_stopping(g)

def best_response_min(g, sigma, tau=None):
    """val_sigma on a STOPPING game by exact policy iteration for Min.
    Sound only on stopping games (dual of lem:switch + lem:local-global);
    asserted.  Returns (L, tau_best)."""
    assert is_stopping(g), "PI for Min is unsound on non-stopping games"
    mins = g.of('min')
    if tau is None:
        tau = {u: g.succ[u][0] for u in mins}
    tau = dict(tau)
    while True:
        v = M.profile_value(g, sigma, tau)
        sw = [u for u in mins if v[other(g, u, tau[u])] < v[tau[u]]]
        if not sw:
            return v, tau
        for u in sw:
            tau[u] = other(g, u, tau[u])

def best_response_max(g, tau, sigma=None):
    assert is_stopping(g)
    maxs = g.of('max')
    if sigma is None:
        sigma = {v: g.succ[v][0] for v in maxs}
    sigma = dict(sigma)
    while True:
        v = M.profile_value(g, sigma, tau)
        sw = [x for x in maxs if v[other(g, x, sigma[x])] > v[sigma[x]]]
        if not sw:
            return v, sigma
        for x in sw:
            sigma[x] = other(g, x, sigma[x])

def other(g, v, s):
    a, b = g.succ[v]
    return b if s == a else a

def val_sigma_brute(g, sigma):
    mins = g.of('min')
    best = None
    for bits in product((0, 1), repeat=len(mins)):
        tau = {u: g.succ[u][b] for u, b in zip(mins, bits)}
        v = M.profile_value(g, sigma, tau)
        best = v if best is None else [min(x, y) for x, y in zip(best, v)]
    return best

def val_tau_brute(g, tau):
    maxs = g.of('max')
    best = None
    for bits in product((0, 1), repeat=len(maxs)):
        sigma = {x: g.succ[x][b] for x, b in zip(maxs, bits)}
        v = M.profile_value(g, sigma, tau)
        best = v if best is None else [max(x, y) for x, y in zip(best, v)]
    return best

def bsi(g, sigma, tau, strict=False, maxrounds=10**6, brute=False):
    """def:bsi.  Returns (rounds, sigma, tau, L, U, history)."""
    maxs, mins = g.of('max'), g.of('min')
    sigma, tau = dict(sigma), dict(tau)
    hist = []
    for r in range(maxrounds):
        if brute:
            L = val_sigma_brute(g, sigma); U = val_tau_brute(g, tau)
        else:
            L, _ = best_response_min(g, sigma, tau)
            U, _ = best_response_max(g, tau, sigma)
        S_sig = [v for v in maxs if L[other(g, v, sigma[v])] > L[sigma[v]]]
        S_tau = [u for u in mins if U[other(g, u, tau[u])] < U[tau[u]]]
        if strict:
            Cmax = [v for v in S_sig if U[other(g, v, sigma[v])] > U[sigma[v]]]
            Cmin = [u for u in S_tau if L[other(g, u, tau[u])] < L[tau[u]]]
        else:
            Cmax = [v for v in S_sig if U[other(g, v, sigma[v])] >= U[sigma[v]]]
            Cmin = [u for u in S_tau if L[other(g, u, tau[u])] <= L[tau[u]]]
        hist.append((len(S_sig), len(S_tau), len(Cmax), len(Cmin)))
        if not Cmax and not Cmin:
            return r, sigma, tau, L, U, hist
        for v in Cmax:
            sigma[v] = other(g, v, sigma[v])
        for u in Cmin:
            tau[u] = other(g, u, tau[u])
    raise RuntimeError("no halt")

def all_switches(g, sigma, maxrounds=10**6, count_ties=True):
    """Productive rounds of sigma -> sigma[S_sigma] with Min best-responding."""
    maxs = g.of('max')
    sigma = dict(sigma)
    ties = 0
    for r in range(maxrounds):
        L, _ = best_response_min(g, sigma)
        S = []
        for v in maxs:
            a, b = L[other(g, v, sigma[v])], L[sigma[v]]
            if a > b: S.append(v)
            elif a == b: ties += 1
        if not S:
            return r, sigma, L, ties
        for v in S:
            sigma[v] = other(g, v, sigma[v])
    raise RuntimeError("no halt")

# ------------------------------------------------------------- constructions

def dual(g):
    """lem:duality: swap sinks and roles.  val_dual = 1 - val off the sinks."""
    swap = {'max': 'min', 'min': 'max', 'avg': 'avg'}
    kinds = [swap[k] for k in g.kinds]
    def m(u):
        if u == g.T0: return g.T1
        if u == g.T1: return g.T0
        return u
    succ = [(m(a), m(b)) for a, b in g.succ]
    return M.G(kinds, succ)

def union(g1, g2, root_kind='avg', root_to=None):
    """Disjoint union with a fresh root vertex (index 0) of kind root_kind whose
    successors are (a in g1, b in g2); sinks shared."""
    n1, n2 = g1.n, g2.n
    n = 1 + n1 + n2
    T0, T1 = n, n + 1
    def m1(u):
        if u == g1.T0: return T0
        if u == g1.T1: return T1
        return 1 + u
    def m2(u):
        if u == g2.T0: return T0
        if u == g2.T1: return T1
        return 1 + n1 + u
    a, b = root_to if root_to else (0, 0)
    kinds = [root_kind] + list(g1.kinds) + list(g2.kinds)
    succ = [(m1(a), m2(b))] + [(m1(x), m1(y)) for x, y in g1.succ] + [(m2(x), m2(y)) for x, y in g2.succ]
    return M.G(kinds, succ)

def ladder(n):
    """def:ladder L_n: Vmax v_1..v_n (indices 0..n-1), Vavg w_1..w_n (n..2n-1)."""
    kinds = ['max'] * n + ['avg'] * n
    T0, T1 = 2 * n, 2 * n + 1
    def v(i): return i - 1 if i <= n else T0
    def w(i): return n + i - 1 if i <= n else T1
    succ = [(v(i + 1), w(i + 1)) for i in range(1, n + 1)] + [(v(i + 1), w(i + 1)) for i in range(1, n + 1)]
    return M.G(kinds, succ)

def corner(g, kind, which):
    return {v: g.succ[v][which] for v in g.of(kind)}

if __name__ == '__main__':
    import sys
    # sanity 1: thm:ladder -- all-switches takes exactly n rounds from all-first
    for n in range(1, 8):
        g = ladder(n)
        r, s, L, ties = all_switches(g, corner(g, 'max', 0))
        assert r == n, (n, r)
    print("ladder all-switches = n: ok")
    # sanity 2: thm:all-switches-refuted 7-vertex game
    kinds = ['max', 'max', 'min', 'avg', 'avg']; T0, T1 = 5, 6
    x, y, m, a, h = range(5)
    g = M.G(kinds, [(T0, a), (m, h), (a, x), (y, T1), (T1, T0)])
    w = M.wstar(g); assert w[:5] == [F(1), F(1), F(1), F(1), F(1, 2)], w
    r, s, L, ties = all_switches(g, {x: T0, y: m})
    print("7-vertex: all-switches rounds", r, "final", L[:5], "ties", ties)
    # sanity 3: prop:bsi-nonstopping is NON-stopping -> our PI asserts; use brute on it
    kinds = ['avg', 'min', 'max', 'max', 'avg', 'max']; T0, T1 = 6, 7
    g = M.G(kinds, [(6, 7), (7, 1), (7, 0), (0, 4), (5, 0), (3, 1)])
    assert not is_stopping(g)
    sigma = {2: T1, 3: 0, 5: 1}; tau = {1: T1}
    Ls = val_sigma_brute(g, sigma); Us = val_tau_brute(g, tau); w = M.wstar(g)
    print("bsi-nonstopping: L", Ls[:6], "w*", w[:6], "U", Us[:6])
    r, s, t, L, U, hist = bsi(g, sigma, tau, brute=True)
    print("  BSI halts at round", r, "with L==U?", L == U, "hist", hist)
    # sanity 4: thm:bsi-nostall on random stopping games with both players
    import random
    random.seed(14)
    from gen import random_game  # may not exist

def wstar_hk(g):
    """w* of a STOPPING game by Hoffman-Karp (all-switches with exact Min best
    response); sound by lem:local-global.  Cross-checked against M.wstar on
    small instances in t_bsi14b.py."""
    sigma = corner(g, 'max', 0)
    r, sigma, L, ties = all_switches(g, sigma)
    return L
