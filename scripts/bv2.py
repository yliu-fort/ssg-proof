"""Round-9 independent verification kit for the boundary-value route.

Everything is fractions.Fraction.  No floating point anywhere.
Values are ALWAYS computed as
    val_sigma = componentwise min over ALL positional tau
    val       = componentwise max over ALL positional sigma
(never by greedy policy iteration), with v_{sigma,tau} the exact least
fixed point of the absorbing Markov chain.

Games carry ARBITRARY rational terminal payoffs, which is what the
boundary substitution G[u := theta] needs.
"""
from fractions import Fraction as F
from itertools import product
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lp_exact import gauss, solve_lp, check_feasible, Infeasible, Unbounded


class PGame:
    """Payoff game.  Vertices 0..n-1 are non-terminal, kinds in max/min/avg,
    out-degree 2 (repetitions allowed).  Vertices n..n+m-1 are terminals with
    payoffs pay[0..m-1].  A play that never absorbs pays Max 0."""

    def __init__(self, kinds, succ, pay):
        self.n = len(kinds)
        self.kinds = list(kinds)
        self.succ = [tuple(s) for s in succ]
        self.pay = [F(p) for p in pay]
        self.m = len(pay)
        self.N = self.n + self.m
        self.maxv = [v for v in range(self.n) if self.kinds[v] == 'max']
        self.minv = [v for v in range(self.n) if self.kinds[v] == 'min']
        self.avgv = [v for v in range(self.n) if self.kinds[v] == 'avg']
        for v in range(self.n):
            assert self.kinds[v] in ('max', 'min', 'avg')
            for t in self.succ[v]:
                assert 0 <= t < self.N

    # ---------------- exact evaluation of one positional pair --------------
    def chain(self, sigma, tau):
        P = []
        for v in range(self.n):
            row = {}
            if self.kinds[v] == 'max':
                t = self.succ[v][sigma[v]]
                row[t] = row.get(t, F(0)) + 1              # accumulate
            elif self.kinds[v] == 'min':
                t = self.succ[v][tau[v]]
                row[t] = row.get(t, F(0)) + 1
            else:
                for t in self.succ[v]:
                    row[t] = row.get(t, F(0)) + F(1, 2)    # accumulate
            P.append(row)
        return P

    def evaluate(self, P):
        """Exact E[payoff at absorption] (0 if never absorbed)."""
        n = self.n
        A = set(v for v in range(n) if any(t >= n for t in P[v]))
        ch = True
        while ch:
            ch = False
            for v in range(n):
                if v not in A and any(t < n and t in A for t in P[v]):
                    A.add(v)
                    ch = True
        R = sorted(A)
        pos = {v: i for i, v in enumerate(R)}
        k = len(R)
        M = [[F(0)] * k for _ in range(k)]
        b = [F(0)] * k
        for v in R:
            i = pos[v]
            M[i][i] += 1
            for t, p in P[v].items():
                if t >= n:
                    b[i] += p * self.pay[t - n]
                elif t in pos:
                    M[i][pos[t]] -= p
        sol = gauss(M, b) if k else []
        x = [F(0)] * self.N
        for j in range(self.m):
            x[n + j] = self.pay[j]
        for v in R:
            x[v] = sol[pos[v]]
        return x

    def strategies(self, which):
        vs = self.maxv if which == 'max' else self.minv
        for bits in product([0, 1], repeat=len(vs)):
            s = [0] * self.n
            for i, v in enumerate(vs):
                s[v] = bits[i]
            yield s

    def val_sigma(self, sigma):
        best = None
        for tau in self.strategies('min'):
            x = self.evaluate(self.chain(sigma, tau))
            best = x if best is None else [min(p, q) for p, q in zip(best, x)]
        return best

    def value(self):
        best = None
        for sigma in self.strategies('max'):
            x = self.val_sigma(sigma)
            best = x if best is None else [max(p, q) for p, q in zip(best, x)]
        return best

    # ---------------- structure --------------------------------------------
    def T(self, x):
        y = list(x)
        for v in range(self.n):
            a, b = self.succ[v]
            if self.kinds[v] == 'max':
                y[v] = max(x[a], x[b])
            elif self.kinds[v] == 'min':
                y[v] = min(x[a], x[b])
            else:
                y[v] = (x[a] + x[b]) / 2
        for j in range(self.m):
            y[self.n + j] = self.pay[j]
        return y

    def is_stopping(self):
        """A trap is a nonempty set U of non-terminals with: every avg vertex
        keeps both successors in U, every controlled vertex keeps one."""
        U = set(range(self.n))
        ch = True
        while ch:
            ch = False
            for v in list(U):
                a, b = self.succ[v]
                ok = ((a in U) and (b in U)) if self.kinds[v] == 'avg' else ((a in U) or (b in U))
                if not ok:
                    U.discard(v)
                    ch = True
        return len(U) == 0

    def hitting(self, sigma, tau, target):
        """h_{sigma,tau}(v -> target) for every v: probability of ever
        visiting `target` (target counts as visited at time 0)."""
        n, N = self.n, self.N
        P = self.chain(sigma, tau)
        # make target absorbing with payoff 1, all terminals payoff 0
        kinds2 = list(self.kinds)
        pay2 = [F(0)] * self.m
        # build a modified PGame where target is a terminal of payoff 1
        # simplest: solve directly
        A = set()
        ch = True
        while ch:
            ch = False
            for v in range(n):
                if v in A:
                    continue
                if v == target:
                    continue
                if any(t == target or (t < n and t in A) for t in P[v]):
                    A.add(v)
                    ch = True
        R = sorted(A)
        pos = {v: i for i, v in enumerate(R)}
        k = len(R)
        M = [[F(0)] * k for _ in range(k)]
        b = [F(0)] * k
        for v in R:
            i = pos[v]
            M[i][i] += 1
            for t, p in P[v].items():
                if t == target:
                    b[i] += p
                elif t < n and t in pos:
                    M[i][pos[t]] -= p
        sol = gauss(M, b) if k else []
        h = [F(0)] * N
        h[target] = F(1)
        for v in R:
            h[v] = sol[pos[v]]
        return h

    def alpha(self, sigma, tau, u, good):
        """Pr[reach terminal `good` (payoff-weighted over all terminals)
        without visiting u]."""
        n, N = self.n, self.N
        P = self.chain(sigma, tau)
        # u becomes absorbing with payoff 0
        A = set()
        ch = True
        while ch:
            ch = False
            for v in range(n):
                if v in A or v == u:
                    continue
                if any(t >= n or (t < n and t != u and t in A) for t in P[v]):
                    A.add(v)
                    ch = True
        R = sorted(A)
        pos = {v: i for i, v in enumerate(R)}
        k = len(R)
        M = [[F(0)] * k for _ in range(k)]
        b = [F(0)] * k
        for v in R:
            i = pos[v]
            M[i][i] += 1
            for t, p in P[v].items():
                if t >= n:
                    b[i] += p * self.pay[t - n]
                elif t != u and t in pos:
                    M[i][pos[t]] -= p
        sol = gauss(M, b) if k else []
        al = [F(0)] * N
        for j in range(self.m):
            al[n + j] = self.pay[j]
        for v in R:
            al[v] = sol[pos[v]]
        al[u] = F(0)
        return al


def freeze(g, u, theta):
    """G[u := theta]: u becomes a terminal of payoff theta.  Vertex numbering
    is preserved by turning u into a *terminal index* -- we keep the vertex
    set and simply give u no successors.  Implementation: append a new
    terminal carrying theta and redirect every edge into u to it, then leave u
    itself in place but unreachable-from-nothing (it is deleted from the
    non-terminal list by giving it kind 'avg' with both successors the new
    terminal, which makes its own value theta as well)."""
    n = g.n
    newt = g.N                      # index of the new terminal
    pay = list(g.pay) + [F(theta)]
    kinds = list(g.kinds)
    succ = []
    for v in range(n):
        a, b = g.succ[v]
        a = newt if a == u else a
        b = newt if b == u else b
        succ.append((a, b))
    # u itself: both edges to the new terminal, kind avg -> value theta
    kinds[u] = 'avg'
    succ[u] = (newt, newt)
    return PGame(kinds, succ, pay)


def ssg_to_pgame(kinds, succ):
    """kinds/succ in lp_exact.Game convention (sinks n, n+1) -> PGame."""
    return PGame(kinds, succ, [F(0), F(1)])


def const_chain(theta, t0, t1, start_index):
    """Average-vertex chain realising a dyadic theta in (0,1) from sinks.
    Returns (kinds, succ, root) with vertex indices start_index..; the chain
    is a DAG, so it adds no cycle and no average cycle."""
    assert 0 <= theta <= 1
    if theta == 0:
        return [], [], t0
    if theta == 1:
        return [], [], t1
    num, den = theta.numerator, theta.denominator
    k = den.bit_length() - 1
    assert den == 1 << k, "dyadic only"
    bits = [(num >> (k - 1 - i)) & 1 for i in range(k)]   # b_1..b_k
    kinds, succ = [], []
    # node i (0-based) = start_index+i, value = sum_{j>i} b_j 2^{-(j-i)}
    for i in range(k):
        nxt = start_index + i + 1 if i + 1 < k else t0
        kinds.append('avg')
        succ.append((t1 if bits[i] else t0, nxt))
    return kinds, succ, start_index


def value_iteration(g, k, start=None):
    x = [F(0)] * g.N if start is None else list(start)
    for j in range(g.m):
        x[g.n + j] = g.pay[j]
    for _ in range(k):
        x = g.T(x)
    return x
