"""Exact elimination of the average vertices.

For a STOPPING game the average equalities determine x from its values at the
controlled vertices:  x = Phi(y),  Phi affine, Phi(y)(u) = sum_v h_u(v) y_v + g_u
with h,g >= 0 and sum_v h_u(v) + g_u + (mass at t0) = 1.

Q(G) is then affinely isomorphic to
   Qc = { y in [0,1]^c : y_v >= Phi(y)(v^(i)) (Max),  y_v <= ... (Min) },
a polytope in c = |Vmax|+|Vmin| dimensions, and every Balas lift may be taken
there, because convex hulls commute with affine isomorphisms.
"""
from fractions import Fraction as F
from itertools import product, combinations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lp_exact import Game, gauss, solve_lp, check_feasible


def phi(g):
    """Return Phi as a list over u in 0..N-1 of (coeffs list of length c, const)."""
    c = len(g.ctrl)
    idx = {v: i for i, v in enumerate(g.ctrl)}
    avg = [u for u in range(g.n) if g.kinds[u] == 'avg']
    pos = {u: i for i, u in enumerate(avg)}
    k = len(avg)
    # x_avg = A x_avg + (contributions from ctrl / sinks)
    A = [[F(0)] * k for _ in range(k)]
    RHS = [[F(0)] * (c + 1) for _ in range(k)]   # columns: y_1..y_c, constant
    for u in avg:
        i = pos[u]
        A[i][i] += F(1)
        for t in g.succ[u]:                       # ACCUMULATE (rule 6-i)
            p = F(1, 2)
            if t in pos:
                A[i][pos[t]] -= p
            elif t == g.t1:
                RHS[i][c] += p
            elif t == g.t0:
                pass
            else:                                  # controlled vertex
                RHS[i][idx[t]] += p
    cols = []
    for j in range(c + 1):
        cols.append(gauss([row[:] for row in A], [RHS[i][j] for i in range(k)]))
    out = []
    for u in range(g.N):
        if u == g.t0:
            out.append(([F(0)] * c, F(0)))
        elif u == g.t1:
            out.append(([F(0)] * c, F(1)))
        elif u in idx:
            e = [F(0)] * c
            e[idx[u]] = F(1)
            out.append((e, F(0)))
        else:
            i = pos[u]
            out.append(([cols[j][i] for j in range(c)], cols[c][i]))
    return out


def qc_rows(g, P=None, offset=0, lam=None, pins=None):
    """Rows of Qc in variables offset+0 .. offset+c-1."""
    if P is None:
        P = phi(g)
    c = len(g.ctrl)
    idx = {v: i for i, v in enumerate(g.ctrl)}
    rows = []

    def add(coeffs, const, sense):
        """sum coeffs_j y_j + const  (sense)  0"""
        d = {}
        for j, co in enumerate(coeffs):
            if co != 0:
                d[offset + j] = d.get(offset + j, F(0)) + co
        rhs = -const
        if lam is None:
            rows.append((d, sense, rhs))
        else:
            if rhs != 0:
                d[lam] = d.get(lam, F(0)) - rhs
            rows.append((d, sense, F(0)))

    for v in g.ctrl:
        for i in (0, 1):
            co, ct = P[g.succ[v][i]]
            coeffs = [-x for x in co]
            coeffs[idx[v]] += F(1)
            add(coeffs, -ct, '>=' if g.kinds[v] == 'max' else '<=')
    for j in range(c):
        e = [F(0)] * c
        e[j] = F(1)
        add(e, F(0), '>=')
        add([-x for x in e], F(1), '>=')          # 1 - y_j >= 0
    if pins:
        for v, i in pins.items():
            co, ct = P[g.succ[v][i]]
            coeffs = [-x for x in co]
            coeffs[idx[v]] += F(1)
            add(coeffs, -ct, '=')
    return rows


def build_lift_c(g, subsets, P=None):
    if P is None:
        P = phi(g)
    c = len(g.ctrl)
    nvar = c
    rows = list(qc_rows(g, P))
    for S in subsets:
        profiles = list(product([0, 1], repeat=len(S)))
        blocks = []
        for j in profiles:
            base = nvar
            nvar += c + 1
            blocks.append((base, base + c, dict(zip(S, j))))
        for base, lam, pins in blocks:
            rows.extend(qc_rows(g, P, offset=base, lam=lam, pins=pins))
        for u in range(c):
            d = {u: F(-1)}
            for base, lam, _ in blocks:
                d[base + u] = F(1)
            rows.append((d, '=', F(0)))
        rows.append(({lam: F(1) for _, lam, _ in blocks}, '=', F(1)))
    return nvar, rows


def sep_c(g, p, q, subsets=None, P=None):
    """max Phi(y)(q) - Phi(y)(p) over the level-|S| Balas lift of Qc."""
    if P is None:
        P = phi(g)
    c = len(g.ctrl)
    if subsets:
        nvar, rows = build_lift_c(g, subsets, P)
    else:
        nvar, rows = c, list(qc_rows(g, P))
    cq, kq = P[q]
    cp, kp = P[p]
    obj = {}
    for j in range(c):
        val = cq[j] - cp[j]
        if val != 0:
            obj[j] = val
    val, z = solve_lp(nvar, rows, obj, maximise=True)
    return val + kq - kp, z


def lift_point_c(g, w, subsets, P=None):
    if P is None:
        P = phi(g)
    c = len(g.ctrl)
    y = [w[v] for v in g.ctrl]
    z = list(y)
    for S in subsets:
        att = {}
        for v in S:
            att[v] = 0 if w[v] == w[g.succ[v][0]] else 1
            assert w[v] == w[g.succ[v][att[v]]]
        for j in product([0, 1], repeat=len(S)):
            if all(att[v] == jv for v, jv in zip(S, j)):
                z.extend(list(y) + [F(1)])
            else:
                z.extend([F(0)] * (c + 1))
    return z


def levels(g, k):
    return [tuple(S) for S in combinations(g.ctrl, k)]


def undecided_c(g, k=1, P=None):
    """None if some controlled vertex is decided at level k; else the separators."""
    if P is None:
        P = phi(g)
    subs = levels(g, k) if k >= 1 else None
    out = {}
    for v in g.ctrl:
        a, b = g.succ[v]
        s0 = sep_c(g, a, b, subs, P)[0]
        if s0 <= 0:
            return None
        s1 = sep_c(g, b, a, subs, P)[0]
        if s1 <= 0:
            return None
        out[v] = (s0, s1)
    return out
