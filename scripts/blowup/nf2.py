"""Two-player HARMONIC NORMAL FORM for stopping SSGs, exact rational arithmetic.

Data: n = m + k controlled vertices, indices 0..m-1 are Max, m..m+k-1 are Min.
For each v in C and each action a in {0,1} a substochastic affine map
        z  |->  p^{v,a} . z + q^{v,a},        p >= 0, q >= 0, |p|_1 + q < 1.
(the missing mass goes to t0, q is the mass on t1).

For a pair (sigma,tau) the pair value on C is the unique solution of
        z = P^{sigma,tau} z + q^{sigma,tau}          (|P|_inf < 1),
and  val_sigma = componentwise min over ALL positional tau  (never greedy PI).
Max vertex i is strictly switchable at sigma iff
        p^{i,1-sigma_i}.z + q^{i,1-sigma_i}  >  z_i .
"""
from fractions import Fraction as F


def solve(A, b):
    """Exact Gaussian elimination; A is n x n list of lists of Fractions."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = None
        for i in range(c, n):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                Mc = M[c]
                M[i] = [M[i][t] - f * Mc[t] for t in range(n + 1)]
    return [M[i][n] for i in range(n)]


class NF:
    def __init__(self, m, k, P, Q):
        self.m, self.k, self.n = m, k, m + k
        self.P, self.Q = P, Q            # P[v][a] list of n Fractions, Q[v][a]

    def choice(self, sigma, tau):
        """actions: list of length n."""
        return [(sigma >> i) & 1 for i in range(self.m)] + \
               [(tau >> j) & 1 for j in range(self.k)]

    def pair_value(self, sigma, tau):
        n = self.n
        act = self.choice(sigma, tau)
        A = [[(F(1) if i == j else F(0)) - self.P[i][act[i]][j] for j in range(n)]
             for i in range(n)]
        b = [self.Q[i][act[i]] for i in range(n)]
        return solve(A, b)

    def apply_row(self, v, a, z):
        return sum(self.P[v][a][j] * z[j] for j in range(self.n)) + self.Q[v][a]

    def val_sigma(self, sigma):
        """Componentwise min over all positional tau; verified to be a fixed
        point of T_sigma (so it IS val_sigma, the operator being a contraction)."""
        n, m, k = self.n, self.m, self.k
        best = None
        for tau in range(1 << k):
            z = self.pair_value(sigma, tau)
            if z is None:
                return None
            best = z if best is None else [min(best[i], z[i]) for i in range(n)]
        # verify fixed point of T_sigma
        for i in range(m):
            a = (sigma >> i) & 1
            if self.apply_row(i, a, best) != best[i]:
                return None
        for j in range(k):
            v = m + j
            lo = min(self.apply_row(v, 0, best), self.apply_row(v, 1, best))
            if lo != best[v]:
                return None
        return best

    def incidences(self, sigma, z=None):
        """list over i in [m] of +1 (strictly switchable), -1 (not), 0 (tie)."""
        if z is None:
            z = self.val_sigma(sigma)
        if z is None:
            return None
        out = []
        for i in range(self.m):
            a = (sigma >> i) & 1
            alt = self.apply_row(i, 1 - a, z)
            out.append(1 if alt > z[i] else (-1 if alt < z[i] else 0))
        return out

    def outmap(self):
        """(s, ndeg) : s[sigma] bitmask of strictly switchable Max vertices;
        ndeg True iff no tie anywhere."""
        s = [0] * (1 << self.m)
        ndeg = True
        for sigma in range(1 << self.m):
            inc = self.incidences(sigma)
            if inc is None:
                return None, False
            o = 0
            for i, c in enumerate(inc):
                if c == 0:
                    ndeg = False
                elif c == 1:
                    o |= 1 << i
            s[sigma] = o
        return s, ndeg
