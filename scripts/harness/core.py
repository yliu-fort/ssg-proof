"""Private exact SSG harness for the root agent (subagents share the parent
scratchpad and have overwritten files there, so this copy stays here).

Vertices 0..n-1 internal; sinks T0 = n, T1 = n+1.
kind[v] in {'max','min','avg'}; succ[v] = (a,b), a,b in 0..n+1.
"""
from fractions import Fraction as F
from itertools import product
import random


def gauss(A, m):
    A = [r[:] for r in A]
    where = [-1] * m
    row = 0
    for col in range(m):
        piv = next((r for r in range(row, m) if A[r][col] != 0), None)
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        pv = A[row][col]
        A[row] = [c / pv for c in A[row]]
        for r in range(m):
            if r != row and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[row])]
        where[col] = row
        row += 1
    x = [F(0)] * m
    for col in range(m):
        if where[col] != -1:
            x[col] = A[where[col]][m]
    return x


class SSG:
    def __init__(self, kind, succ):
        self.n = len(kind)
        self.kind = list(kind)
        self.succ = [tuple(s) for s in succ]
        self.T0, self.T1 = self.n, self.n + 1
        self.MX = [v for v in range(self.n) if kind[v] == 'max']
        self.MN = [v for v in range(self.n) if kind[v] == 'min']

    def profile_values(self, sigma, tau):
        n = self.n
        nxt = []
        for v in range(n):
            if self.kind[v] == 'max':
                nxt.append((sigma[v],))
            elif self.kind[v] == 'min':
                nxt.append((tau[v],))
            else:
                nxt.append(self.succ[v])
        can = [False] * (n + 2)
        can[self.T1] = True
        ch = True
        while ch:
            ch = False
            for v in range(n):
                if not can[v] and any(can[u] for u in nxt[v]):
                    can[v] = True
                    ch = True
        idx = [v for v in range(n) if can[v]]
        pos = {v: i for i, v in enumerate(idx)}
        m = len(idx)
        A = [[F(0)] * (m + 1) for _ in range(m)]
        for v in idx:
            i = pos[v]
            A[i][i] += F(1)
            outs = nxt[v]
            w = F(1, len(outs))
            for u in outs:
                if u == self.T1:
                    A[i][m] += w
                elif u != self.T0 and can[u]:
                    A[i][pos[u]] -= w
        x = gauss(A, m)
        val = [F(0)] * n
        for v in idx:
            val[v] = x[pos[v]]
        return val

    def lk(self, val, u):
        return F(1) if u == self.T1 else (F(0) if u == self.T0 else val[u])

    def min_best_response_pi(self, sigma):
        """Greedy policy iteration for Min. CORRECT ONLY FOR STOPPING GAMES:
        in a non-stopping game it can halt at a strictly suboptimal tau,
        because the alternative successor is evaluated against the current
        policy's own (self-referentially high) values. Kept only to exhibit
        that failure; val_sigma below does not use it."""
        tau = {v: self.succ[v][0] for v in self.MN}
        while True:
            val = self.profile_values(sigma, tau)
            sw = False
            for v in self.MN:
                a, b = self.succ[v]
                other = b if tau[v] == a else a
                if self.lk(val, other) < self.lk(val, tau[v]):
                    tau[v] = other
                    sw = True
            if not sw:
                return val

    def val_sigma(self, sigma):
        """val_sigma = min over ALL positional tau of v_{sigma,tau}, taken
        componentwise. Exact and valid in every SSG (Min has a uniformly
        optimal positional counterstrategy, so the componentwise minimum is
        attained by a single tau). Exponential in |V_min|; fine for the small
        instances used here."""
        best = None
        for bits in product([0, 1], repeat=len(self.MN)):
            tau = {v: self.succ[v][bits[i]] for i, v in enumerate(self.MN)}
            val = self.profile_values(sigma, tau)
            best = val if best is None else [min(a, b) for a, b in zip(best, val)]
        return best

    def optimal_value(self):
        best = None
        for bits in product([0, 1], repeat=len(self.MX)):
            sigma = {v: self.succ[v][bits[i]] for i, v in enumerate(self.MX)}
            val = self.val_sigma(sigma)
            best = val if best is None else [max(a, b) for a, b in zip(best, val)]
        return best


def random_ssg(n, seed=None, p=(0.34, 0.33)):
    rnd = random.Random(seed)
    kind = []
    for _ in range(n):
        r = rnd.random()
        kind.append('max' if r < p[0] else ('min' if r < p[0] + p[1] else 'avg'))
    succ = [(rnd.randrange(n + 2), rnd.randrange(n + 2)) for _ in range(n)]
    return SSG(kind, succ)
