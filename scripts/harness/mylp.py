"""Exact rational LP: maximise c.x over {A x <= b, x >= 0}.

Two-phase tableau simplex with Bland's rule (so it provably terminates).
Written from scratch for this session; validated in mylp_test.py against
brute-force vertex enumeration.
"""
from fractions import Fraction as F
from itertools import combinations


class Infeasible(Exception):
    pass


def _simplex(T, basis, ncols, allowed):
    """T is (m+1) x (ncols+1); last row is the objective (minimise -c.x form).
    Returns 'optimal' or 'unbounded'.  Bland's rule: smallest index."""
    m = len(T) - 1
    while True:
        piv_col = None
        for j in range(ncols):
            if j in allowed and T[-1][j] < 0:
                piv_col = j
                break
        if piv_col is None:
            return 'optimal'
        piv_row = None
        best = None
        for i in range(m):
            if T[i][piv_col] > 0:
                ratio = T[i][-1] / T[i][piv_col]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[piv_row]):
                    best = ratio
                    piv_row = i
        if piv_row is None:
            return 'unbounded'
        _pivot(T, basis, piv_row, piv_col)


def _pivot(T, basis, r, c):
    pv = T[r][c]
    T[r] = [v / pv for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            Ti, Tr = T[i], T[r]
            T[i] = [Ti[j] - f * Tr[j] for j in range(len(Ti))]
    basis[r] = c


class LP:
    """max c.x over {A x <= b, x >= 0}.  Phase 1 once; then many objectives."""

    def __init__(self, A, b, n):
        m = len(A)
        rows, rhs, sign = [], [], []
        for i in range(m):
            if b[i] < 0:
                rows.append([-F(v) for v in A[i]])
                rhs.append(-F(b[i]))
                sign.append(-1)
            else:
                rows.append([F(v) for v in A[i]])
                rhs.append(F(b[i]))
                sign.append(1)
        art = [i for i in range(m) if sign[i] == -1]
        ncols = n + m + len(art)
        artcol = {i: n + m + k for k, i in enumerate(art)}
        T, basis = [], [None] * m
        for i in range(m):
            row = [F(0)] * (ncols + 1)
            for j in range(n):
                row[j] = rows[i][j]
            row[n + i] = F(sign[i])          # slack column, +1 or -1
            if sign[i] == -1:
                row[artcol[i]] = F(1)
                basis[i] = artcol[i]
            else:
                basis[i] = n + i
            row[-1] = rhs[i]
            T.append(row)
        self.n, self.m, self.ncols = n, m, ncols
        self.feasible = True
        if art:
            obj = [F(0)] * (ncols + 1)
            for i in art:
                obj[artcol[i]] = F(1)
            for i in art:                     # price out the artificial basis
                for j in range(ncols + 1):
                    obj[j] -= T[i][j]
            T.append(obj)
            st = _simplex(T, basis, ncols, set(range(ncols)))
            assert st == 'optimal'
            if -T[-1][-1] != 0:
                self.feasible = False
            else:
                for i in range(m):            # drive artificials out of the basis
                    if basis[i] >= n + m:
                        pc = None
                        for j in range(n + m):
                            if T[i][j] != 0:
                                pc = j
                                break
                        if pc is not None:
                            _pivot(T, basis, i, pc)
            T.pop()
        self.T, self.basis = T, basis
        self.allowed = set(range(n + m))      # artificials barred from re-entering

    def maximize(self, c):
        """Returns the optimum (a Fraction), or None if unbounded/infeasible."""
        if not self.feasible:
            return None
        T, basis, ncols, n, m = self.T, self.basis, self.ncols, self.n, self.m
        obj = [F(0)] * (ncols + 1)
        for j in range(n):
            obj[j] = -F(c[j])
        T.append(obj)
        for i in range(m):                     # price out the current basis
            f = T[-1][basis[i]]
            if f != 0:
                Ti, Tl = T[i], T[-1]
                T[-1] = [Tl[j] - f * Ti[j] for j in range(ncols + 1)]
        st = _simplex(T, basis, ncols, self.allowed)
        val = None if st == 'unbounded' else T[-1][-1]
        T.pop()
        return val


def brute_max(A, b, c, n, ub=None):
    """Independent check: enumerate every basic solution of {Ax<=b, x>=0}.

    Adds the rows x_j >= 0 (and x_j <= ub if given) explicitly, then takes every
    n-subset of rows, solves for the vertex and keeps the feasible ones.
    Exponential -- only for validation on tiny LPs."""
    rows = [list(map(F, r)) for r in A]
    rhs = [F(x) for x in b]
    for j in range(n):
        e = [F(0)] * n
        e[j] = F(-1)
        rows.append(e)
        rhs.append(F(0))
        if ub is not None:
            e2 = [F(0)] * n
            e2[j] = F(1)
            rows.append(e2)
            rhs.append(F(ub))
    best = None
    for S in combinations(range(len(rows)), n):
        M = [rows[i][:] for i in S]
        v = _solve_or_none(M, [rhs[i] for i in S])
        if v is None:
            continue
        if all(sum(rows[i][j] * v[j] for j in range(n)) <= rhs[i] for i in range(len(rows))):
            val = sum(F(c[j]) * v[j] for j in range(n))
            if best is None or val > best:
                best = val
    return best


def _solve_or_none(M, y):
    n = len(M)
    A = [M[i][:] + [y[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if A[r][col] != 0), None)
        if piv is None:
            return None
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [A[r][k] - f * A[col][k] for k in range(n + 1)]
    return [A[i][n] for i in range(n)]
