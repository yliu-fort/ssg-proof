"""helpers for the convex-class checks: first-passage rows over C u {t1}, the matrix B = sym(R_0^T R_1), an exact PSD test."""
import sys, os as _os
sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'harness'))
from fractions import Fraction as F

def solve(Mx, rhs):
    n = len(Mx); T = [list(map(F, Mx[i])) + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if T[r][c] != 0); T[c], T[p] = T[p], T[c]; pv = T[c][c]; T[c] = [x / pv for x in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [T[r][j] - f * T[c][j] for j in range(n + 1)]
    return [T[i][n] for i in range(n)]

def first_passage_rows(g, C):
    avg = [v for v in range(g.n) if g.kinds[v] == 'avg']; ai = {v: i for i, v in enumerate(avg)}
    def law(tgt):
        A = [[F(int(i == j)) for j in range(len(avg))] for i in range(len(avg))]; b = [F(0)] * len(avg)
        for a in avg:
            for s in g.succ[a]:
                if s in ai: A[ai[a]][ai[s]] -= F(1, 2)
                elif s == tgt: b[ai[a]] += F(1, 2)
        h = solve(A, b) if avg else []
        return lambda u: h[ai[u]] if u in ai else F(int(u == tgt))
    laws = {t: law(t) for t in list(C) + [g.T1]}
    return {(v, a): ([laws[u](g.succ[v][a]) for u in C], laws[g.T1](g.succ[v][a])) for v in C for a in (0, 1)}

def Bmatrix(g):
    C = [v for v in range(g.n) if g.kinds[v] in ('max', 'min')]; k = len(C)
    rows = first_passage_rows(g, C)
    R = [[[F(int(i == j)) - rows[(C[i], a)][0][j] for j in range(k)] for i in range(k)] for a in (0, 1)]
    B = [[sum(R[0][t][i] * R[1][t][j] + R[1][t][i] * R[0][t][j] for t in range(k)) / 2 for j in range(k)] for i in range(k)]
    return C, rows, B

def psd(B):
    """exact LDL^T with pivoting on the diagonal: returns (psd, positive_definite)."""
    n = len(B); A = [list(r) for r in B]; pd = True
    for c in range(n):
        p = max(range(c, n), key=lambda r: A[r][r])
        if A[p][p] < 0: return False, False
        if A[p][p] == 0:
            # the remaining block must be zero for PSD
            if any(A[r][s] != 0 for r in range(c, n) for s in range(c, n)): return False, False
            return True, False
        A[c], A[p] = A[p], A[c]
        for r in range(n): A[r][c], A[r][p] = A[r][p], A[r][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            for s in range(c, n): A[r][s] -= f * A[c][s]
    return True, pd
