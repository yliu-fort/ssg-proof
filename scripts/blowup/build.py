"""HARMONIC NORMAL FORM  ->  explicit stopping SSG.

Row (v,a) carries a dyadic distribution mu on C u {t1} u {t0} with denominator
2^d.  A Knuth-Yao DDG tree of fair coins realises mu with sum_j n_j average
vertices, n_1 = 1, n_{j+1} = 2 n_j - k_j, k_j = #targets whose j-th binary digit
is 1.  The controlled vertex v then points, for action a, at the root of that
tree (or straight at the single target when mu is a point mass).

Sinks are carried as the SENTINELS 'T0','T1' and mapped to indices only at the
very end.
"""
from fractions import Fraction as F


def dyadic_depth(mu):
    d = 1
    for x in mu.values():
        den = x.denominator
        while (1 << d) % den:
            d += 1
    return d


def ddg_tree(mu, newnode):
    """mu : dict target -> Fraction, summing to 1, dyadic.
    newnode() allocates a fresh average vertex and returns its id.
    Returns (entry, edges) with edges a dict node -> [child0, child1]."""
    items = [(t, x) for t, x in mu.items() if x > 0]
    if len(items) == 1:
        return items[0][0], {}
    d = dyadic_depth(mu)
    bits = {}
    for t, x in items:
        num = int(x * (1 << d))
        bits[t] = [(num >> (d - j)) & 1 for j in range(1, d + 1)]   # bit j = 2^-j
    edges = {}
    root = newnode()
    slots = [(root, 0), (root, 1)]
    for j in range(1, d + 1):
        term = [t for t, b in bits.items() if b[j - 1]]
        assert len(term) <= len(slots), (mu, j, len(term), len(slots))
        assign = slots[:len(term)]
        rest = slots[len(term):]
        for (nd, side), t in zip(assign, term):
            edges.setdefault(nd, [None, None])[side] = t
        slots = []
        for (nd, side) in rest:
            c = newnode()
            edges.setdefault(nd, [None, None])[side] = c
            slots.append((c, 0)); slots.append((c, 1))
    assert not slots, mu
    return root, edges


def build_ssg(m, k, P, Q):
    """P[v][a] list of n Fractions, Q[v][a] Fraction; |p|_1 + q <= 1.
    Vertices 0..m-1 Max, m..m+k-1 Min, then the gadget average vertices."""
    n = m + k
    kinds = ['max'] * m + ['min'] * k
    succ = [None] * n
    nodes = {}                       # id -> [c0,c1]  (average vertices)
    counter = [n]

    def newnode():
        i = counter[0]; counter[0] += 1
        kinds.append('avg'); succ.append(None); return i

    for v in range(n):
        pair = []
        for a in (0, 1):
            mu = {}
            for u in range(n):
                if P[v][a][u] > 0:
                    mu[u] = mu.get(u, F(0)) + P[v][a][u]      # accumulate, never a dict literal
            if Q[v][a] > 0:
                mu['T1'] = mu.get('T1', F(0)) + Q[v][a]
            rest = F(1) - sum(mu.values())
            if rest > 0:
                mu['T0'] = mu.get('T0', F(0)) + rest
            assert sum(mu.values()) == 1
            root, edges = ddg_tree(mu, newnode)
            for nd, ch in edges.items():
                succ[nd] = tuple(ch)
            pair.append(root)
        succ[v] = tuple(pair)
    NT = counter[0]
    T0, T1 = NT, NT + 1
    succ = [tuple(T0 if x == 'T0' else (T1 if x == 'T1' else x) for x in s) for s in succ]
    return kinds, succ
