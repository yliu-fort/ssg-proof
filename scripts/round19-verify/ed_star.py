#!/usr/bin/env python3
"""|C| + 1 evaluations, chosen in advance, determine a nondegenerate stopping ONE-PLAYER harmonic system.

The forced-answer lemma. Let D be data of t queries with affinely independent values x_1..x_t, recorded from a
nondegenerate stopping one-player system (so Delta_r(v) := A_r(v, 1 - sigma_r(v)) - x_r(v) != 0 for every r, v).
For a strategy sigma and a member W' of K(D): val_{W',sigma} lies in the affine hull of x_1..x_t iff
val_{W',sigma} = sum_r alpha_r x_r for the (unique) alpha with sum alpha_r = 1 and
      sum_{r : sigma_r(v) != sigma(v)} alpha_r Delta_r(v) = 0   for every v in C,          (*)
because the reading of a row at an affine combination of the x_r is the same combination of its recorded readings,
so sum alpha_r x_r is a fixed point of the frozen operator of EVERY member, unique by stopping. Hence (*) depends on
the data alone: either every member answers sigma with the same point of the hull (the query is uninformative) or
none does (the rank grows by one for every member).
The star. Query e_1, ..., e_m (the strategies switching one vertex) and then 0. At step t + 1 <= m the column of
v = t + 1 ... more simply: a solution alpha of (*) with support S needs, at every v, either no or at least two
r in S with sigma_r(v) != sigma(v); for the star every nonempty S meets some column in exactly one element, so (*)
has no solution and every query is informative: the m + 1 value vectors are affinely independent, the m + 1 readings
determine every row, the system is known, and with it the bit and an optimal strategy. With prop:eval-decide-lower
(m + 1 necessary at m in {2, 3}) the decision and the naming complexity are exactly |C| + 1 there.
Checks here (exact): (1) on random nondegenerate stopping systems for m = 2..6 the star's values have rank m + 1 and
the rows are recovered exactly from the readings; (2) the lemma: on random data of t = 2, 3 queries (m = 3), for
every other sigma, the solvability of (*) coincides with membership of val_sigma in the hull for the true world AND
for random other members of K(D) (built along the fibres), and when (*) is solvable all members answer alike;
(3) at m = 3, t = 3: (*) is solvable exactly for the fourth vertex of a 2-face containing the three queries, on all
56 triples of random systems (the codimension-one coincidences do not occur at random); (4) a degenerate system on
which the star's rank drops (nondegeneracy is needed)."""
import sys, os, random, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)

def solve(Mx, rhs):
    n = len(Mx); T = [list(map(F, Mx[i])) + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if T[r][c] != 0), None)
        if p is None: return None
        T[c], T[p] = T[p], T[c]; pv = T[c][c]; T[c] = [x / pv for x in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [T[r][j] - f * T[c][j] for j in range(n + 1)]
    return [T[i][n] for i in range(n)]

def rank(rows):
    A = [list(r) for r in rows]; rk = 0; ncol = len(A[0])
    for c in range(ncol):
        p = next((i for i in range(rk, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]; pv = A[rk][c]; A[rk] = [x / pv for x in A[rk]]
        for i in range(len(A)):
            if i != rk and A[i][c] != 0:
                f = A[i][c]; A[i] = [A[i][j] - f * A[rk][j] for j in range(ncol)]
        rk += 1
    return rk

class Sys:
    def __init__(self, m, rows): self.m = m; self.rows = rows      # rows[(v,a)] = (q, p_0..p_{m-1})
    def stopping(self):
        m = self.m
        for U in range(1, 1 << m):
            us = [i for i in range(m) if (U >> i) & 1]
            if all(any(self.rows[(i, a)][0] == 0 and sum(self.rows[(i, a)][1:]) == 1 and all(self.rows[(i, a)][1 + j] == 0 for j in range(m) if not (U >> j) & 1) for a in (0, 1)) for i in us):
                return False
        return True
    def value(self, sig):
        m = self.m; P = [self.rows[(i, sig[i])][1:] for i in range(m)]; q = [self.rows[(i, sig[i])][0] for i in range(m)]
        return solve([[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)], q)
    def reading(self, key, x): z = self.rows[key]; return z[0] + sum(z[1 + j] * x[j] for j in range(self.m))
    def nondegenerate(self):
        for sig in itertools.product((0, 1), repeat=self.m):
            x = self.value(sig)
            if x is None: return False
            for i in range(self.m):
                if self.reading((i, 1 - sig[i]), x) == x[i]: return False
        return True

def random_system(rng, m, D=5, degenerate=False):
    while True:
        rows = {}
        for i in range(m):
            for a in (0, 1):
                w = [rng.randrange(0, 2 ** D) for _ in range(m + 1)]; s = rng.randrange(max(sum(w), 1), 2 * max(sum(w), 1) + 1)
                rows[(i, a)] = tuple(F(x, s) for x in w)
        if degenerate:      # make one vertex's two rows equal: a tie at every strategy
            rows[(0, 1)] = rows[(0, 0)]
        S = Sys(m, rows)
        if not S.stopping(): continue
        if degenerate or S.nondegenerate(): return S

def alpha_system(S, queries, xs, sig):
    """the linear system (*): unknown alpha in R^t; returns a solution or None."""
    m = S.m; t = len(queries)
    E = [[F(1)] * t]; b = [F(1)]
    for v in range(m):
        row = [F(0)] * t
        for r in range(t):
            if queries[r][v] != sig[v]:
                row[r] = S.reading((v, sig[v]), xs[r]) - xs[r][v]        # Delta_r(v), the appeal gap of sigma's action at sigma_r
                assert row[r] != 0
        if any(row): E.append(row); b.append(F(0))
    # solve E alpha = b (possibly over/under-determined): least squares not needed -- try exact elimination
    A = [E[i] + [b[i]] for i in range(len(E))]; rk = 0; piv = []
    for c in range(t):
        p = next((i for i in range(rk, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]; pv = A[rk][c]; A[rk] = [x / pv for x in A[rk]]
        for i in range(len(A)):
            if i != rk and A[i][c] != 0:
                f = A[i][c]; A[i] = [A[i][j] - f * A[rk][j] for j in range(t + 1)]
        piv.append(c); rk += 1
    for i in range(rk, len(A)):
        if A[i][t] != 0: return None       # inconsistent
    alpha = [F(0)] * t
    for i, c in enumerate(piv): alpha[c] = A[i][t]
    return alpha

def in_hull(x, xs):
    return rank([[F(1)] + list(y) for y in xs]) == rank([[F(1)] + list(y) for y in xs] + [[F(1)] + list(x)])

def member(rng, S, queries, xs):
    """a random other member of K(D): each row moved to a random point of its fibre (a random direction in the null
    space of the readings, scaled to stay in Delta)."""
    m = S.m; t = len(queries); rows = {}
    E = [[F(1)] + list(x) for x in xs]
    for key, z in S.rows.items():
        # random integer vector, projected onto the null space of E by solving for t coordinates
        for _ in range(20):
            d = [F(rng.randrange(-8, 9)) for _ in range(m + 1)]
            # fix the first t coordinates so that E d = 0, keep the others
            free = list(range(t, m + 1)); pivc = list(range(t))
            A = [[E[r][c] for c in pivc] for r in range(t)]; rhs = [-sum(E[r][c] * d[c] for c in free) for r in range(t)]
            sol = solve(A, rhs)
            if sol is None: continue
            for c, val in zip(pivc, sol): d[c] = val
            if all(x == 0 for x in d): continue
            lo, hi = -F(10 ** 6), F(10 ** 6)
            for j in range(m + 1):
                if d[j] > 0: lo = max(lo, -z[j] / d[j])
                elif d[j] < 0: hi = min(hi, -z[j] / d[j])
            sd = sum(d); sz = sum(z)
            if sd > 0: hi = min(hi, (1 - sz) / sd)
            elif sd < 0: lo = max(lo, (1 - sz) / sd)
            if lo < hi:
                lam = lo + (hi - lo) * F(rng.randrange(1, 16), 16); rows[key] = tuple(z[j] + lam * d[j] for j in range(m + 1)); break
        else: rows[key] = z
    return Sys(m, rows)

if __name__ == '__main__':
    rng = random.Random(1905)
    # (1) the star
    for m in range(2, 7):
        for _ in range(40 if m <= 4 else 10):
            S = random_system(rng, m)
            star = [tuple(int(j == i) for j in range(m)) for i in range(m)] + [tuple([0] * m)]
            xs = [S.value(s) for s in star]; E = [[F(1)] + list(x) for x in xs]
            assert rank(E) == m + 1, ('rank drop on a nondegenerate system', m)
            for key, z in S.rows.items():
                zz = solve(E, [S.reading(key, x) for x in xs]); assert tuple(zz) == z
    print('(1) star: rank m+1 and exact row recovery on nondegenerate stopping one-player systems, m = 2..6')
    # (2) the lemma on random data, m = 3
    m = 3; strategies = list(itertools.product((0, 1), repeat=m)); agree = 0; forced = 0; checked = 0
    for _ in range(60):
        S = random_system(rng, m)
        for t in (2, 3):
            queries = rng.sample(strategies, t); xs = [S.value(s) for s in queries]
            if rank([[F(1)] + list(x) for x in xs]) < t: continue
            members = [S] + [member(rng, S, queries, xs) for _ in range(4)]
            for Wp in members:
                assert Wp.stopping() or Wp is not S
                for s in queries:
                    assert Wp.value(s) == S.value(s) and all(Wp.reading(k, S.value(s)) == S.reading(k, S.value(s)) for k in S.rows)
            for sig in strategies:
                if sig in queries: continue
                alpha = alpha_system(S, queries, xs, sig)
                answers = set()
                for Wp in members:
                    if not Wp.stopping(): continue
                    x = Wp.value(sig); checked += 1
                    assert in_hull(x, xs) == (alpha is not None), ('lemma violated', t, queries, sig)
                    if alpha is not None:
                        assert x == [sum(alpha[r] * xs[r][j] for r in range(t)) for j in range(m)]; answers.add(tuple(x))
                if alpha is not None: forced += 1; assert len(answers) == 1
                agree += 1
    print(f'(2) forced-answer lemma: {checked} (member, sigma) checks agree; {forced} forced queries, all members answering alike')
    # (3) t = 3: forced iff the fourth vertex of a 2-face
    face = 0; tot = 0; bad = 0
    for _ in range(40):
        S = random_system(rng, m)
        for triple in itertools.combinations(strategies, 3):
            xs = [S.value(s) for s in triple]
            if rank([[F(1)] + list(x) for x in xs]) < 3: bad += 1; continue
            for sig in strategies:
                if sig in triple: continue
                tot += 1
                solv = alpha_system(S, triple, xs, sig) is not None
                on_face = any(all(s[v] == triple[0][v] for s in triple + (sig,)) for v in range(m)) and sig == tuple(a ^ b ^ c for a, b, c in zip(*triple))
                assert solv == on_face, (triple, sig, solv, on_face)
                face += on_face
    print(f'(3) m = 3, t = 3: of {tot} fourth queries exactly {face} are forced, and they are exactly the fourth vertices of 2-faces; rank-deficient triples: {bad}')
    # (4) a degenerate system: the rank drops
    drops = 0
    for _ in range(30):
        S = random_system(rng, 3, degenerate=True)
        star = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)]
        xs = [S.value(s) for s in star]
        if rank([[F(1)] + list(x) for x in xs]) < 4: drops += 1
    print(f'(4) degenerate systems (one vertex with two equal rows): the star\'s rank dropped on {drops} of 30 -- nondegeneracy is needed')
    assert drops > 0
    print('|C| + 1 EVALUATIONS, CHOSEN IN ADVANCE, DETERMINE A NONDEGENERATE STOPPING ONE-PLAYER SYSTEM')
