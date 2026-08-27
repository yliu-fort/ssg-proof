"""Exact rational LP with a CHECKED optimality certificate.

Every call returns (value, x, cert) where x is verified primal-feasible and
cert is a verified dual solution of equal objective value, so the answer is
correct independently of the pivoting code.  All Fractions.

Primal:   max c.x   s.t.  rows (each  a.x <= b, >= b or = b),  x >= 0.
Dual:     min b.y   s.t.  A^T y >= c,  y >= 0 on '<=' rows,  y <= 0 on '>=',
                          y free on '=' rows.
"""
from fractions import Fraction as F


class LPError(Exception):
    pass


def _simplex(T, basis, n):
    """Bland's rule; T is (m+1) x (n+1), row m the reduced-cost row."""
    m = len(T) - 1
    while True:
        col = -1
        for j in range(n):
            if T[m][j] < 0:
                col = j
                break
        if col < 0:
            return
        row, best = -1, None
        for i in range(m):
            if T[i][col] > 0:
                r = T[i][-1] / T[i][col]
                if best is None or r < best or (r == best and basis[i] < basis[row]):
                    best, row = r, i
        if row < 0:
            raise LPError("unbounded")
        piv = T[row][col]
        T[row] = [e / piv for e in T[row]]
        for i in range(m + 1):
            if i != row and T[i][col] != 0:
                f = T[i][col]
                T[i] = [T[i][j] - f * T[row][j] for j in range(n + 1)]
        basis[row] = col


def solve(nvar, rows, obj, maximise=True):
    """rows: list of (dict var->coef, sense, rhs).  Variables are >= 0."""
    # ---- standard form  A z = b, z >= 0 --------------------------------
    A, b = [], []
    ncol = nvar
    extra = []                                  # (row index, +-1) slack columns
    for (a, s, r) in rows:
        a = dict(a); r = F(r)
        if s == '<=':
            extra.append((len(A), 1))
        elif s == '>=':
            extra.append((len(A), -1))
        A.append(a); b.append(r)
    ncol = nvar + len(extra)
    M = [[F(0)] * ncol for _ in A]
    for i, a in enumerate(A):
        for k, v in a.items():
            M[i][k] += F(v)
    for j, (i, sg) in enumerate(extra):
        M[i][nvar + j] = F(sg)
    # make b >= 0
    for i in range(len(M)):
        if b[i] < 0:
            M[i] = [-e for e in M[i]]
            b[i] = -b[i]
    m = len(M)
    # ---- phase 1 --------------------------------------------------------
    T = [M[i] + [F(0)] * m + [b[i]] for i in range(m)]
    for i in range(m):
        T[i][ncol + i] = F(1)
    basis = [ncol + i for i in range(m)]
    n1 = ncol + m
    cost = [F(0)] * n1 + [F(0)]
    for i in range(m):
        for j in range(n1 + 1):
            cost[j] -= T[i][j]
    for j in range(ncol, n1):
        cost[j] = F(0)                          # artificials priced out
    for i in range(m):
        cost[ncol + i] = F(0)
    T.append(cost)
    _simplex(T, basis, n1)
    if -T[m][-1] != 0:
        raise LPError("infeasible")
    # drive artificials out
    for i in range(m):
        if basis[i] >= ncol:
            for j in range(ncol):
                if T[i][j] != 0:
                    piv = T[i][j]
                    T[i] = [e / piv for e in T[i]]
                    for k in range(m + 1):
                        if k != i and T[k][j] != 0:
                            f = T[k][j]
                            T[k] = [T[k][t] - f * T[i][t] for t in range(n1 + 1)]
                    basis[i] = j
                    break
    keep = [i for i in range(m) if basis[i] < ncol]
    T2 = [[T[i][j] for j in range(ncol)] + [T[i][-1]] for i in keep]
    bs2 = [basis[i] for i in keep]
    m2 = len(T2)
    sign = F(1) if maximise else F(-1)
    c = [F(0)] * ncol
    for k, v in obj.items():
        c[k] = sign * F(v)
    crow = [-x for x in c] + [F(0)]
    for i in range(m2):
        if crow[bs2[i]] != 0:
            f = crow[bs2[i]]
            crow = [crow[j] - f * T2[i][j] for j in range(ncol + 1)]
    T2.append(crow)
    _simplex(T2, bs2, ncol)
    x = [F(0)] * nvar
    for i in range(m2):
        if bs2[i] < nvar:
            x[bs2[i]] = T2[i][-1]
    val = T2[m2][-1] * sign
    # ---- verify primal feasibility --------------------------------------
    for (a, s, r) in rows:
        lhs = sum(F(v) * x[k] for k, v in a.items())
        ok = lhs <= r if s == '<=' else lhs >= r if s == '>=' else lhs == r
        if not ok:
            raise LPError("primal point infeasible -- pivoting bug")
    if any(t < 0 for t in x):
        raise LPError("negative variable -- pivoting bug")
    if sum(F(v) * x[k] for k, v in obj.items()) != val:
        raise LPError("objective mismatch")
    return val, x


def certify(nvar, rows, obj, val, maximise=True):
    """Verify optimality of `val` by exhibiting a dual solution: solve the dual
    LP and check strong duality.  Returns the dual vector."""
    # dual variables y_i free/signed; encode y = yp - ym with yp,ym >= 0
    m = len(rows)
    sgn = F(1) if maximise else F(-1)
    # primal: max sgn*obj . x, A x (<=,>=,=) b, x >= 0
    # dual  : min b.y, A^T y >= sgn*c, sign conditions
    drows, dobj = [], {}
    for i, (a, s, r) in enumerate(rows):
        dobj[2 * i] = F(r); dobj[2 * i + 1] = -F(r)
    for j in range(nvar):
        pairs = []
        for i, (a, s, r) in enumerate(rows):
            if j in a:
                pairs.append((2 * i, F(a[j])))
                pairs.append((2 * i + 1, -F(a[j])))
        d = {}
        for k, v in pairs:
            d[k] = d.get(k, F(0)) + v
        cj = sgn * F(obj.get(j, 0))
        drows.append(({k: v for k, v in d.items() if v != 0}, '>=', cj))
    for i, (a, s, r) in enumerate(rows):
        if s == '<=':
            drows.append(({2 * i + 1: F(1)}, '=', 0))      # y >= 0
        elif s == '>=':
            drows.append(({2 * i: F(1)}, '=', 0))          # y <= 0
    dval, y = solve(2 * m, drows, dobj, maximise=False)
    if dval * sgn != val:
        raise LPError("duality gap: primal %s dual %s" % (val, dval))
    return [y[2 * i] - y[2 * i + 1] for i in range(m)]
