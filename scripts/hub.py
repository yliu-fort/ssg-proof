"""The hub class:  SSGs with a vertex meeting every cycle.

Contains
  * builder for the separating family W(k,r),
  * a class-membership audit against every polynomial class of frontier.tex,
  * the ACYCLIC exact solver used as the inner oracle,
  * the one-vertex boundary reduction (dyadic bisection + continued-fraction
    rounding), which is the new algorithm,
all in exact rational arithmetic.
"""
from fractions import Fraction as F
from itertools import product
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bv2 import PGame, freeze, ssg_to_pgame, const_chain

# ------------------------------------------------------------------ graph ---

def cycles_exist_through(g, avoid):
    """Is there a directed cycle among non-terminal vertices avoiding `avoid`?"""
    n = g.n
    col = [0]*n
    def dfs(v):
        col[v] = 1
        for t in g.succ[v]:
            if t >= n or t in avoid:
                continue
            if col[t] == 1:
                return True
            if col[t] == 0 and dfs(t):
                return True
        col[v] = 2
        return False
    for v in range(n):
        if v not in avoid and col[v] == 0 and dfs(v):
            return True
    return False


def cycles(g):
    """All elementary cycles (Johnson-free brute force; fine for small n)."""
    n = g.n
    out = []
    def ext(path, onpath, start):
        v = path[-1]
        for t in g.succ[v]:
            if t >= n or t < start:
                continue
            if t == start:
                out.append(list(path))
            elif t not in onpath:
                onpath.add(t); path.append(t)
                ext(path, onpath, start)
                path.pop(); onpath.discard(t)
    for s in range(n):
        ext([s], {s}, s)
    return out


def kacyclic(g, kind):
    return all(all(g.kinds[v] != kind for v in c) for c in cycles(g))


def maxreach_sccs(g):
    """SCCs of H(G) (def:maxreach): Max vertices, edge u->v iff v reachable
    from u by a positive-length path."""
    n = g.n
    reach = {}
    for u in range(n):
        seen = set()
        stack = [t for t in g.succ[u] if t < n]
        while stack:
            v = stack.pop()
            if v in seen: continue
            seen.add(v)
            stack += [t for t in g.succ[v] if t < n]
        reach[u] = seen
    M = [v for v in range(n) if g.kinds[v] == 'max']
    comp = []
    left = set(M)
    while left:
        u = next(iter(left))
        c = {v for v in left if v in reach[u] and u in reach[v]} | {u}
        comp.append(sorted(c))
        left -= c
    return comp


def levels(g, sigma):
    """C_j of lem:descent for a Max strategy sigma; returns ell (dict)."""
    n, N = g.n, g.N
    # terminals: t1 is the payoff-1 terminal(s)
    ell = {}
    C = set(i for i in range(n, N) if g.pay[i-n] == 1)
    for v in C: ell[v] = 0
    j = 0
    while True:
        j += 1
        new = set()
        for v in range(n):
            if v in ell: continue
            a, b = g.succ[v]
            k = g.kinds[v]
            if k == 'avg' and (a in C or b in C): new.add(v)
            elif k == 'max' and g.succ[v][sigma[v]] in C: new.add(v)
            elif k == 'min' and a in C and b in C: new.add(v)
        if not new: break
        for v in new: ell[v] = j
        C |= new
    return ell


def escape_exponent_sigma(g, sigma):
    """d(sigma) = max over v in C_inf of A_sigma(v)  (def:escape)."""
    ell = levels(g, sigma)
    n = g.n
    order = sorted(ell, key=lambda v: ell[v])
    A = {}
    for v in order:
        if ell[v] == 0:
            A[v] = 0; continue
        if v >= n:
            A[v] = 0; continue
        k = g.kinds[v]
        succ = [g.succ[v][sigma[v]]] if k == 'max' else list(g.succ[v])
        down = [w for w in succ if w in ell and ell[w] < ell[v]]
        w = 0
        if k == 'avg':
            # one point of loss per average vertex exactly one of whose two
            # EDGES descends (if both edges descend the token descends surely)
            lower = [t for t in g.succ[v] if t in ell and ell[t] < ell[v]]
            w = 1 if len(lower) == 1 else 0
        A[v] = w + max((A[x] for x in down), default=0)
    return max((A[v] for v in ell), default=0)


# ------------------------------------------------- exact acyclic solver ----

def solve_acyclic(g):
    """Exact values of an acyclic payoff game by backward induction."""
    n, N = g.n, g.N
    order, mark = [], {}
    def dfs(v):
        mark[v] = 1
        for t in g.succ[v]:
            if t < n:
                assert mark.get(t, 0) != 1, "not acyclic"
                if t not in mark: dfs(t)
        mark[v] = 2; order.append(v)
    for v in range(n):
        if v not in mark: dfs(v)
    x = [F(0)]*N
    for j in range(g.m): x[n+j] = g.pay[j]
    for v in order:                    # reverse topological: successors first
        a, b = g.succ[v]
        k = g.kinds[v]
        x[v] = max(x[a], x[b]) if k == 'max' else min(x[a], x[b]) if k == 'min' \
               else (x[a]+x[b])/2
    return x


# --------------------------------------- one-vertex boundary reduction -----

def R_of(g, u, theta, solver):
    y = solver(freeze(g, u, theta))
    a, b = g.succ[u]
    k = g.kinds[u]
    return max(y[a], y[b]) if k == 'max' else min(y[a], y[b]) if k == 'min' \
           else (y[a]+y[b])/2


def cf_round(lo, hi, Dmax):
    """The unique rational with denominator <= Dmax in [lo,hi], by the
    Stern-Brocot/continued-fraction search.  Returns None if none."""
    def simplest(x, y):
        """rational in [x,y] of least denominator; 0 <= x <= y"""
        if x.denominator == 1:
            return x
        fx = x.numerator // x.denominator
        if fx + 1 <= y:
            return F(fx + 1)
        return fx + 1 / simplest(1/(y - fx), 1/(x - fx))
    p = simplest(lo, hi)
    return p if p.denominator <= Dmax and lo <= p <= hi else None


def boundary_value(g, u, solver, a_bound=None, trace=None):
    """val_G(u) exactly, for a STOPPING G, using O(a) calls to `solver` on
    the frozen games G[u := dyadic].  Sound by the sign test:
        val_G(u) >= c  iff  R_u(c) >= c.
    """
    a = len(g.avgv) if a_bound is None else a_bound
    D = 1 << a                       # denominator bound (lem:denominator-sharp)
    lo, hi = F(0), F(1)              # invariant: lo <= val <= hi
    steps = 2*a + 2
    for _ in range(steps):
        mid = (lo+hi)/2
        if R_of(g, u, mid, solver) >= mid:      # val >= mid
            lo = mid
        else:
            hi = mid
        if trace is not None: trace.append((lo, hi))
    cand = cf_round(lo, hi, D)
    assert cand is not None, ("no rational of denominator <= 2^a in the window", lo, hi)
    assert R_of(g, u, cand, solver) == cand, "candidate is not a fixed point"
    return cand


# ------------------------------------------------------ the family W(k,r) --

def build_W(k, r, consts=None):
    """u (avg hub) -> (p_1, h); p_1..p_{2k} alternate Max/Min around one cycle
    back to u, each with an exit; exit of p_1 is the top of a descent chain
    g_r -> ... -> g_1 of values 2^-j; the other exits are dyadic constants.
    Returns (PGame, index of u)."""
    if consts is None:
        consts = [F(1,2) + F((-1)**i * (i+1), 16) for i in range(2*k)]
    kinds, succ = [], []
    def new(kind, s):
        kinds.append(kind); succ.append(s); return len(kinds)-1
    # placeholders; sinks get index n, n+1 at the end -> use sentinels
    T0, T1 = 'T0', 'T1'
    u = new('avg', None)
    h = new('avg', (T0, T1))
    P = [new('max' if i % 2 == 0 else 'min', None) for i in range(2*k)]
    # descent chain g_1..g_r  (g_j value 2^-j), g_j -> (g_{j-1}, T0)
    G = []
    for j in range(r):
        G.append(new('avg', None))
    for j in range(r):
        succ[G[j]] = (T1 if j == 0 else G[j-1], T0)
    exits = [G[r-1] if r > 0 else T1]
    for i in range(1, 2*k):
        ck, cs, root = const_chain(consts[i], T0, T1, len(kinds))
        for kk, ss in zip(ck, cs): new(kk, ss)
        exits.append(root)
    for i in range(2*k):
        succ[P[i]] = (P[i+1] if i+1 < 2*k else u, exits[i])
    succ[u] = (P[0], h)
    n = len(kinds)
    idx = {T0: n, T1: n+1}
    succ = [tuple(idx.get(t, t) for t in s) for s in succ]
    return PGame(kinds, succ, [F(0), F(1)]), u


def build_W2(k, r, consts=None, hub_kind='avg'):
    """Refined separating family.  One cycle
         u -> z_1 -> z_2 -> ... -> z_{3k} -> u
    whose vertices cycle through the kinds max, min, avg, so that the cycle
    carries all three colours; every z_j also has an exit edge, the exit of
    z_1 being the top of the descent chain g_r -> ... -> g_1 (values 2^-j)
    and the others dyadic constants.  u is an average vertex (the hub) with
    second successor h of value 1/2.  All cycles pass through u.
    Returns (PGame, u)."""
    L = 3*k
    if consts is None:
        consts = [F(1,2) + F((-1)**i*(i+1), 64) for i in range(L)]
    kinds, succ = [], []
    T0, T1 = 'T0', 'T1'
    def new(kind, s):
        kinds.append(kind); succ.append(s); return len(kinds)-1
    u = new(hub_kind, None)
    h = new('avg', (T0, T1))
    Z = [new(['max','min','avg'][i % 3], None) for i in range(L)]
    G = [new('avg', None) for _ in range(r)]
    for j in range(r):
        succ[G[j]] = (T1 if j == 0 else G[j-1], T0)
    exits = [G[r-1] if r > 0 else T1]
    for i in range(1, L):
        ck, cs, root = const_chain(consts[i], T0, T1, len(kinds))
        for kk, ss in zip(ck, cs): new(kk, ss)
        exits.append(root)
    for i in range(L):
        succ[Z[i]] = (Z[i+1] if i+1 < L else u, exits[i])
    succ[u] = (Z[0], h)
    n = len(kinds)
    idx = {T0: n, T1: n+1}
    succ = [tuple(idx.get(t, t) for t in s) for s in succ]
    return PGame(kinds, succ, [F(0), F(1)]), u


def boundary_value_lfp(g, u, solver, a_bound=None, trace=None):
    """val_G(u) exactly for an ARBITRARY SSG (no stopping hypothesis).

    R_u has all slopes in [0,1] (thm:bv-affine), so theta -> R_u(theta)-theta
    is non-increasing and  P(theta) := [R_u(theta) <= theta]  is an UP-SET
    predicate whose least element is  lfp R_u = val_G(u)  (thm:bv-lfp).
    Bisect for that least element and round to the denominator grid.
    """
    a = len(g.avgv) if a_bound is None else a_bound
    D = 1 << a
    P = lambda th: R_of(g, u, th, solver) <= th
    if P(F(0)):
        return F(0)
    lo, hi = F(0), F(1)          # P(lo) false, P(hi) true (R<=1 always)
    assert P(hi)
    for _ in range(2*a + 2):
        mid = (lo + hi)/2
        if P(mid): hi = mid
        else:      lo = mid
        if trace is not None: trace.append((lo, hi))
    cand = cf_round(lo, hi, D)
    assert cand is not None and R_of(g, u, cand, solver) == cand, \
        ("rounding failed", lo, hi, cand)
    return cand
