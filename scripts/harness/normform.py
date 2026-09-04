"""One-player improvement orientations via the NORMAL FORM, which is the right
search space -- my earlier hill climb searched raw games and never exceeded
height 3 at m = 3, while the abstract ceiling is h*(3) = 4.

Normal form: for each Max vertex i and action a in {0,1}, a substochastic affine
map z |-> p^{i,a}.z + q^{i,a} with p >= 0, q >= 0 and |p|_1 + q < 1.  Then
   z(sigma) = (I - P^sigma)^{-1} q^sigma,
and i is strictly switchable at sigma iff
   p^{i,1-sigma_i}.z(sigma) + q^{i,1-sigma_i} > z_i(sigma).
By lem:auso-normalform every such dyadic family is realised by an explicit
stopping one-player SSG, so a normal form of bottom-antipodal height h is a
genuine witness that h is realisable.
"""
import random
import sys
import time
from fractions import Fraction as F
from auso import is_uso, is_acyclic, ba_heights


def solve(A, b):
    m = len(A)
    M = [list(A[i]) + [b[i]] for i in range(m)]
    for c in range(m):
        piv = next((i for i in range(c, m) if M[i][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for i in range(m):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][k] - f * M[c][k] for k in range(m + 1)]
    return [M[i][m] for i in range(m)]


def outmap(P, Q, m):
    """P[i][a] is a list of m coefficients, Q[i][a] a scalar."""
    s = [0] * (1 << m)
    for code in range(1 << m):
        bits = [(code >> i) & 1 for i in range(m)]
        A = [[(F(1) if i == j else F(0)) - P[i][bits[i]][j] for j in range(m)]
             for i in range(m)]
        b = [Q[i][bits[i]] for i in range(m)]
        z = solve(A, b)
        if z is None:
            return None
        o = 0
        for i in range(m):
            alt = sum(P[i][1 - bits[i]][j] * z[j] for j in range(m)) + Q[i][1 - bits[i]]
            if alt == z[i]:
                return None                      # degenerate
            if alt > z[i]:
                o |= 1 << i
        s[code] = o
    return s


def rand_nf(m, rng, den):
    P = [[None, None] for _ in range(m)]
    Q = [[None, None] for _ in range(m)]
    for i in range(m):
        for a in (0, 1):
            while True:
                w = [rng.randrange(0, den // 2) for _ in range(m)]
                q = rng.randrange(0, den // 2)
                if sum(w) + q < den:
                    break
            P[i][a] = [F(x, den) for x in w]
            Q[i][a] = F(q, den)
    return P, Q


def mutate(P, Q, m, rng, den):
    P = [[list(P[i][a]) for a in (0, 1)] for i in range(m)]
    Q = [[Q[i][a] for a in (0, 1)] for i in range(m)]
    for _ in range(rng.randint(1, 3)):
        i = rng.randrange(m)
        a = rng.randrange(2)
        j = rng.randrange(m + 1)
        step = F(rng.choice([1, -1, 2, -2, 4, -4]), den)
        if j < m:
            nv = P[i][a][j] + step
            if nv < 0:
                nv = F(0)
            old = P[i][a][j]
            P[i][a][j] = nv
            if sum(P[i][a]) + Q[i][a] >= 1:
                P[i][a][j] = old
        else:
            nv = Q[i][a] + step
            if nv < 0:
                nv = F(0)
            old = Q[i][a]
            Q[i][a] = nv
            if sum(P[i][a]) + Q[i][a] >= 1:
                Q[i][a] = old
    return P, Q


m = int(sys.argv[2])
den = int(sys.argv[3]) if len(sys.argv) > 3 else 64
rng = random.Random(int(sys.argv[1]))
best = 0
bestnf = None
t0 = time.time()
it = 0
while time.time() - t0 < 100000:
    it += 1
    if bestnf is None or rng.random() < 0.05:
        P, Q = rand_nf(m, rng, den)
    else:
        P, Q = mutate(bestnf[0], bestnf[1], m, rng, den)
    s = outmap(P, Q, m)
    if s is None:
        continue
    if not (is_uso(s, m) and is_acyclic(s, m)):
        print('*** NOT AN AUSO ***', P, Q, s, flush=True)
        continue
    h = max(ba_heights(s, m))
    if h > best:
        best = h
        bestnf = (P, Q)
        print(f'[{it}] one-player BA height {h} at m={m}; outmap {s}', flush=True)
        print(f'      P={[[[str(x) for x in P[i][a]] for a in (0,1)] for i in range(m)]}', flush=True)
        print(f'      Q={[[str(Q[i][a]) for a in (0,1)] for i in range(m)]}', flush=True)
