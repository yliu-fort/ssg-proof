"""Exact rational LP (two-phase simplex, Bland's rule) and SSG utilities.

All arithmetic is fractions.Fraction.  No floating point anywhere.
"""
from fractions import Fraction as F
from itertools import product

# ---------------------------------------------------------------- simplex ---

class Infeasible(Exception):
    pass


class Unbounded(Exception):
    pass


def _pivot(T, basis, r, c):
    piv = T[r][c]
    T[r] = [e / piv for e in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            Ti, Tr = T[i], T[r]
            T[i] = [Ti[j] - f * Tr[j] for j in range(len(Ti))]
    basis[r] = c


def _simplex(T, basis, ncols):
    """Maximise: last row holds -(reduced cost); pivot until optimal.
    Dantzig rule with a Bland fallback after many iterations (anti-cycling)."""
    m = len(T) - 1
    it = 0
    limit = 4 * (m + ncols) + 200
    while True:
        it += 1
        col = -1
        if it < limit:
            best = 0
            for j in range(ncols):
                if T[m][j] < best:
                    best, col = T[m][j], j
        else:
            for j in range(ncols):
                if T[m][j] < 0:
                    col = j
                    break                  # Bland
        if col < 0:
            return
        best, row = None, -1
        for i in range(m):
            if T[i][col] > 0:
                ratio = T[i][-1] / T[i][col]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[row]):
                    best, row = ratio, i
        if row < 0:
            raise Unbounded()
        _pivot(T, basis, row, col)


def solve_lp(nvar, rows, obj, maximise=True):
    """max/min obj . z  s.t.  rows,  z >= 0.

    rows: list of (dict var->coef, sense in {'<=','>=','='}, rhs)
    obj : dict var->coef
    Returns (value, z) with exact Fractions.
    """
    rows = [(dict(a), s, F(b)) for a, s, b in rows]
    # make rhs >= 0
    norm = []
    for a, s, b in rows:
        if b < 0:
            a = {k: -v for k, v in a.items()}
            b = -b
            s = {'<=': '>=', '>=': '<=', '=': '='}[s]
        norm.append((a, s, b))
    nslack = sum(1 for _, s, _ in norm if s != '=')
    # artificial for every row (rhs>=0) except '<=' rows (slack is a basis)
    art_rows = [i for i, (_, s, _) in enumerate(norm) if s != '<=']
    ncols = nvar + nslack + len(art_rows)
    m = len(norm)
    T = [[F(0)] * (ncols + 1) for _ in range(m + 1)]
    basis = [None] * m
    sk = nvar
    ak = nvar + nslack
    art_index = {}
    for i, (a, s, b) in enumerate(norm):
        for k, v in a.items():
            T[i][k] += F(v)
        T[i][-1] = b
        if s == '<=':
            T[i][sk] = F(1)
            basis[i] = sk
            sk += 1
        elif s == '>=':
            T[i][sk] = F(-1)
            sk += 1
    for i in art_rows:
        T[i][ak] = F(1)
        basis[i] = ak
        art_index[i] = ak
        ak += 1
    # phase 1: maximise -(sum of artificials).  The objective row is
    #   e_art - sum_{art rows} T[i]   -- the e_art term is essential, without it
    #   the artificial columns get reduced cost -1 and re-enter the basis.
    for j in range(nvar + nslack, ncols):
        T[m][j] += F(1)
    for i in art_rows:
        for j in range(ncols + 1):
            T[m][j] -= T[i][j]
    _simplex(T, basis, ncols)
    if -T[m][-1] != 0:
        raise Infeasible()
    # drive artificials out of the basis; rows that cannot be are redundant
    nstruct = nvar + nslack
    drop = set()
    for i in range(m):
        if basis[i] >= nstruct:
            for j in range(nstruct):
                if T[i][j] != 0:
                    _pivot(T, basis, i, j)
                    break
            else:
                drop.add(i)
    # physically delete the artificial columns and the redundant rows
    keep = [i for i in range(m) if i not in drop]
    T2 = [[T[i][j] for j in range(nstruct)] + [T[i][-1]] for i in keep]
    basis2 = [basis[i] for i in keep]
    m2 = len(T2)
    T2.append([F(0)] * (nstruct + 1))
    sign = F(1) if maximise else F(-1)
    for k, v in obj.items():
        T2[m2][k] -= sign * F(v)
    for i in range(m2):
        if T2[m2][basis2[i]] != 0:
            f = T2[m2][basis2[i]]
            T2[m2] = [T2[m2][j] - f * T2[i][j] for j in range(nstruct + 1)]
    _simplex(T2, basis2, nstruct)
    z = [F(0)] * nvar
    for i in range(m2):
        if basis2[i] < nvar:
            z[basis2[i]] = T2[i][-1]
    val = T2[m2][-1] * sign
    # rule 6-ii, mechanised: never return a point without checking it
    for a, s_, b in rows:
        lhs = sum(F(co) * z[k] for k, co in a.items())
        ok = (lhs <= b) if s_ == '<=' else (lhs >= b) if s_ == '>=' else (lhs == b)
        assert ok, "solve_lp returned an infeasible point: %s %s %s (lhs=%s)" % (a, s_, b, lhs)
    assert sum(F(co) * z[k] for k, co in obj.items()) == val, "objective mismatch"
    return val, z


def check_feasible(rows, point, tol_name=""):
    """Verify an explicit point satisfies every row exactly (rule 6-ii)."""
    for idx, (a, s, b) in enumerate(rows):
        lhs = sum(F(c) * point[k] for k, c in a.items())
        ok = (lhs <= b) if s == '<=' else (lhs >= b) if s == '>=' else (lhs == b)
        if not ok:
            raise AssertionError(f"{tol_name}: row {idx} violated: {a} {s} {b}, lhs={lhs}")
    return True


# ------------------------------------------------------------------- games ---
# A game: n non-sink vertices 0..n-1; sinks are n (=t0) and n+1 (=t1).
# kinds[i] in {'max','min','avg'};  succ[i] = (a, b) indices into 0..n+1.

class Game:
    def __init__(self, kinds, succ):
        self.n = len(kinds)
        self.kinds = list(kinds)
        self.succ = [tuple(s) for s in succ]
        self.t0 = self.n
        self.t1 = self.n + 1
        self.N = self.n + 2
        self.ctrl = [v for v in range(self.n) if kinds[v] in ('max', 'min')]
        self.maxv = [v for v in range(self.n) if kinds[v] == 'max']
        self.minv = [v for v in range(self.n) if kinds[v] == 'min']

    # ---- exact evaluation --------------------------------------------------
    def chain_matrix(self, sigma, tau):
        """Rows of the Markov chain: list of dict target->prob (targets 0..n+1)."""
        P = []
        for v in range(self.n):
            row = {}
            if self.kinds[v] == 'max':
                row[self.succ[v][sigma[v]]] = row.get(self.succ[v][sigma[v]], F(0)) + F(1)
            elif self.kinds[v] == 'min':
                row[self.succ[v][tau[v]]] = row.get(self.succ[v][tau[v]], F(0)) + F(1)
            else:
                for t in self.succ[v]:                      # ACCUMULATE (rule 6-i)
                    row[t] = row.get(t, F(0)) + F(1, 2)
            P.append(row)
        return P

    def reach_prob(self, P):
        """Least fixed point of x = Px + [t1]: exact reachability probability."""
        n = self.n
        # vertices that can reach t1
        can = set([self.t1])
        changed = True
        while changed:
            changed = False
            for v in range(n):
                if v not in can and any(t in can for t in P[v]):
                    can.add(v)
                    changed = True
        R = [v for v in range(n) if v in can]
        pos = {v: i for i, v in enumerate(R)}
        k = len(R)
        A = [[F(0)] * k for _ in range(k)]
        b = [F(0)] * k
        for v in R:
            i = pos[v]
            A[i][i] += F(1)
            for t, p in P[v].items():
                if t == self.t1:
                    b[i] += p
                elif t in pos:
                    A[i][pos[t]] -= p
        sol = gauss(A, b)
        x = [F(0)] * (n + 2)
        x[self.t1] = F(1)
        for v in R:
            x[v] = sol[pos[v]]
        return x

    def val_sigma(self, sigma):
        """Componentwise minimum over ALL positional tau (rule 2)."""
        best = None
        for bits in product([0, 1], repeat=len(self.minv)):
            tau = [0] * self.n
            for idx, v in enumerate(self.minv):
                tau[v] = bits[idx]
            x = self.reach_prob(self.chain_matrix(sigma, tau))
            best = x if best is None else [min(a, b) for a, b in zip(best, x)]
        return best

    def value(self):
        """w* = componentwise max over sigma of val_sigma."""
        best = None
        for bits in product([0, 1], repeat=len(self.maxv)):
            sigma = [0] * self.n
            for idx, v in enumerate(self.maxv):
                sigma[v] = bits[idx]
            x = self.val_sigma(sigma)
            best = x if best is None else [max(a, b) for a, b in zip(best, x)]
        return best

    def is_stopping(self):
        """Non-stopping iff some nonempty U avoiding both sinks has: every avg
        vertex of U keeps BOTH successors in U and every controlled vertex of U
        keeps at least one.  Largest such U by iterated deletion."""
        U = set(range(self.n))
        changed = True
        while changed:
            changed = False
            for v in list(U):
                a, b = self.succ[v]
                if self.kinds[v] == 'avg':
                    ok = (a in U) and (b in U)
                else:
                    ok = (a in U) or (b in U)
                if not ok:
                    U.discard(v)
                    changed = True
        return len(U) == 0


def gauss(A, b):
    k = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    piv_row = 0
    where = [-1] * k
    for col in range(k):
        sel = None
        for r in range(piv_row, k):
            if M[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        M[piv_row], M[sel] = M[sel], M[piv_row]
        pv = M[piv_row][col]
        M[piv_row] = [e / pv for e in M[piv_row]]
        for r in range(k):
            if r != piv_row and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][j] - f * M[piv_row][j] for j in range(k + 1)]
        where[col] = piv_row
        piv_row += 1
    x = [F(0)] * k
    for col in range(k):
        if where[col] >= 0:
            x[col] = M[where[col]][k]
    return x
