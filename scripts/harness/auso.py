"""Unique sink orientations of the cube, the BottomAntipodal walk, and the
Schurr-Szabo blow-up -- rebuilt from the statement to check that f(m), the
counting function of rem:allsw-laws, is exponential.

An orientation of the m-cube is given by its OUTMAP s : {0,1}^m -> {0,1}^m,
where i in s(v) means the edge in direction i points away from v.
  USO      : for all u != v, (s(u) ^ s(v)) & (u ^ v) != 0.
  ACYCLIC  : the digraph v -> v ^ e_i (i in s(v)) has no directed cycle.
  BA step  : v -> v ^ s(v);  h(v) = number of steps to the sink s(v) = 0.

The two laws of sec:allsw-laws, for a sequence sigma_0..sigma_L with
S_t = sigma_t ^ sigma_{t+1} nonempty and S_L = 0:
  (B) for s < t:            (sigma_s ^ sigma_t) & S_s != 0
  (F) for s < t <= L-1:     (sigma_s ^ sigma_t) not a subset of S_t
"""
from itertools import product


def is_uso(s, m):
    n = 1 << m
    for u in range(n):
        for v in range(u + 1, n):
            if ((s[u] ^ s[v]) & (u ^ v)) == 0:
                return False
    return True


def is_acyclic(s, m):
    n = 1 << m
    colour = [0] * n

    def dfs(u):
        stack = [(u, 0)]
        while stack:
            v, i = stack.pop()
            if i == 0:
                if colour[v] == 2:
                    continue
                if colour[v] == 1:
                    return False
                colour[v] = 1
            if i < m:
                stack.append((v, i + 1))
                if s[v] >> i & 1:
                    w = v ^ (1 << i)
                    if colour[w] == 1:
                        return False
                    if colour[w] == 0:
                        stack.append((w, 0))
            else:
                colour[v] = 2
        return True

    for u in range(n):
        if colour[u] == 0:
            if not dfs(u):
                return False
    return True


def ba_heights(s, m):
    """h(v) for every v; None if the walk does not terminate."""
    n = 1 << m
    h = [None] * n
    for v in range(n):
        seen = []
        u = v
        while h[u] is None and s[u] != 0:
            if u in seen:
                return None
            seen.append(u)
            u = u ^ s[u]
        base = 0 if s[u] == 0 else h[u]
        for j, w in enumerate(reversed(seen)):
            base += 1
            h[w] = base
        if s[v] == 0:
            h[v] = 0
    return h


def ba_trace(s, v):
    out = [v]
    while s[v] != 0:
        v = v ^ s[v]
        out.append(v)
    return out


def obeys_laws(trace):
    L = len(trace) - 1
    S = [trace[t] ^ trace[t + 1] for t in range(L)]
    if any(x == 0 for x in S):
        return False
    for a in range(L + 1):
        for b in range(a + 1, L + 1):
            d = trace[a] ^ trace[b]
            if (d & S[a]) == 0:
                return False
            if b <= L - 1 and (d & ~S[b]) == 0:
                return False
    return True


def enumerate_ausos(m):
    """All AUSOs of the m-cube (feasible for m <= 3)."""
    n = 1 << m
    out = []
    for s in product(range(n), repeat=n):
        if sum(1 for v in range(n) if s[v] == 0) != 1:
            continue
        if is_uso(s, m) and is_acyclic(s, m):
            out.append(list(s))
    return out


def blowup(sA, m):
    """Schurr-Szabo D: an (m+2)-cube from an m-cube AUSO.
    Vertex v = v' + (v'' << m), v'' in {0,1,2,3} read as (bit m, bit m+1).
    s_D(v)' = s_A(v')  except at v''=00 where it is s_A(v' ^ vmax);
    s_D(v)'' depends on v'' and on the parity p of h_A(v')."""
    hA = ba_heights(sA, m)
    assert hA is not None
    n = 1 << m
    vmax = n - 1
    sD = [0] * (n << 2)
    for vpp in range(4):
        for vp in range(n):
            p = hA[vp] & 1
            lo = sA[vp ^ vmax] if vpp == 0 else sA[vp]
            if vpp == 0:
                hi = 0
            elif vpp == 3:
                hi = 1 if p == 0 else 2
            elif vpp == 1:
                hi = 1 if p == 0 else 3
            else:
                hi = 3 if p == 0 else 1
            sD[vp + (vpp << m)] = lo + (hi << m)
    return sD
