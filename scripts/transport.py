"""Transport polytope Q(G;L,U) (def:transport) and its Balas lift-and-project
strengthenings Q_1, Q_2, ..., all in exact rational arithmetic."""
from fractions import Fraction as F
from itertools import product, combinations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lp_exact import Game, solve_lp, check_feasible, Infeasible, Unbounded


def q_rows(g, L=None, U=None, offset=0, lam=None, pins=None):
    """Rows of Q(G;L,U) in variables offset+u  (u = 0..N-1).

    If lam is not None it is a variable index and the rows are HOMOGENISED:
    every right-hand side r is replaced by r*x[lam] (moved to the left).
    pins: dict v -> i, adding the equality x(v) = x(v^(i)).
    Coefficients are always ACCUMULATED (rule 6-i: v^(0) may equal v^(1)).
    """
    N = g.N
    if L is None:
        L = [F(0)] * N
    if U is None:
        U = [F(1)] * N
    rows = []

    def add(d, sense, rhs):
        dd = {}
        for k, v in d.items():
            dd[offset + k] = dd.get(offset + k, F(0)) + v      # accumulate
        dd = {k: v for k, v in dd.items() if v != 0}
        if lam is None:
            rows.append((dd, sense, F(rhs)))
        else:
            if rhs != 0:
                dd[lam] = dd.get(lam, F(0)) - F(rhs)
            rows.append((dd, sense, F(0)))

    add({g.t0: F(1)}, '=', 0)
    add({g.t1: F(1)}, '=', 1)
    for v in range(g.n):
        a, b = g.succ[v]
        if g.kinds[v] == 'max':
            add({v: F(1), a: F(-1)}, '>=', 0)
            add({v: F(1), b: F(-1)}, '>=', 0)
        elif g.kinds[v] == 'min':
            add({v: F(1), a: F(-1)}, '<=', 0)
            add({v: F(1), b: F(-1)}, '<=', 0)
        else:
            d = {v: F(1)}
            d[a] = d.get(a, F(0)) - F(1, 2)
            d[b] = d.get(b, F(0)) - F(1, 2)
            add(d, '=', 0)
    for u in range(N):
        add({u: F(1)}, '>=', L[u])
        add({u: F(1)}, '<=', U[u])
    if pins:
        for v, i in pins.items():
            add({v: F(1), g.succ[v][i]: F(-1)}, '=', 0)
    return rows


def build_lift(g, subsets, L=None, U=None):
    """Extended (Balas) formulation of  INTERSECTION over S in `subsets` of
        conv( union over profiles j on S of  Q(G;L,U) & {x(v)=x(v^{j_v}) : v in S} ).
    Variables: x[u] = u (0..N-1), then one block per (S, profile).
    Returns (nvar, rows)."""
    N = g.N
    nvar = N
    rows = list(q_rows(g, L, U))               # the base polytope too (Q_1 <= Q)
    for S in subsets:
        profiles = list(product([0, 1], repeat=len(S)))
        blocks = []
        for j in profiles:
            base = nvar
            nvar += N + 1                      # y block, then lambda
            lam = base + N
            blocks.append((base, lam, dict(zip(S, j))))
        for base, lam, pins in blocks:
            rows.extend(q_rows(g, L, U, offset=base, lam=lam, pins=pins))
        # x = sum of the y blocks
        for u in range(N):
            d = {u: F(-1)}
            for base, lam, _ in blocks:
                d[base + u] = F(1)
            rows.append((d, '=', F(0)))
        rows.append(({lam: F(1) for _, lam, _ in blocks}, '=', F(1)))
    return nvar, rows


def lift_point(g, w, subsets, L=None, U=None):
    """The explicit point of the lift induced by w (rule 6-ii check)."""
    N = g.N
    z = [F(0)] * N
    for u in range(N):
        z[u] = w[u]
    for S in subsets:
        profiles = list(product([0, 1], repeat=len(S)))
        # the profile that w attains on S
        att = {}
        for v in S:
            a, b = g.succ[v]
            att[v] = 0 if w[v] == w[a] else 1
            assert w[v] == w[g.succ[v][att[v]]], "w does not attain at %d" % v
        for j in profiles:
            blk = [F(0)] * (N + 1)
            if all(att[v] == jv for v, jv in zip(S, j)):
                blk = list(w) + [F(1)]
            z.extend(blk)
    return z


def sep(g, p, q, L=None, U=None, subsets=None):
    """max x(q) - x(p) over Q_1 (or Q if subsets is None/empty)."""
    if subsets:
        nvar, rows = build_lift(g, subsets, L, U)
    else:
        nvar, rows = g.N, list(q_rows(g, L, U))
    obj = {}
    obj[q] = obj.get(q, F(0)) + F(1)
    obj[p] = obj.get(p, F(0)) - F(1)
    val, z = solve_lp(nvar, rows, obj, maximise=True)
    return val, z


def level_subsets(g, k):
    return [tuple(S) for S in combinations(g.ctrl, k)]


def decided(g, L=None, U=None, k=1, verbose=False):
    """For each controlled vertex, does the level-k separator decide it?
    Returns dict v -> ('0>=1' | '1>=0' | 'both' | None)."""
    subs = level_subsets(g, k) if k >= 1 else None
    out = {}
    for v in g.ctrl:
        a, b = g.succ[v]
        s_ab, _ = sep(g, a, b, L, U, subs)   # max x(b)-x(a)  <=0  =>  w*(b)<=w*(a)
        s_ba, _ = sep(g, b, a, L, U, subs)
        tag = None
        if s_ab <= 0 and s_ba <= 0:
            tag = 'both'
        elif s_ab <= 0:
            tag = '0>=1'
        elif s_ba <= 0:
            tag = '1>=0'
        out[v] = (tag, s_ab, s_ba)
        if verbose:
            print(f"   v={v} succ=({a},{b}) Sep({a},{b})={s_ab} Sep({b},{a})={s_ba} -> {tag}")
    return out


def sanity(g, subsets, L=None, U=None, name=""):
    """Verify w* is feasible for the lift BEFORE interpreting anything."""
    w = g.value()
    rows = build_lift(g, subsets, L, U)[1]
    z = lift_point(g, w, subsets, L, U)
    check_feasible(rows, z, name or "lift")
    return w
