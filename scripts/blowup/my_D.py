"""Root verification of allswlower:prop-search(a): the operation D on AUSOs.

D on an AUSO s_A of the m-cube gives an outmap on the (m+2)-cube with
vertices (alpha, beta, v): alpha = bit m, beta = bit m+1.
  inner: s_A(v xor 1bar) on layer (alpha,beta) = (0,0); s_A(v) elsewhere.
  outer: (0,0): {};  (1,0): {a,b} if h_A(v) even else {a};
         (0,1): {b} if even else {a,b};  (1,1): {a} if even else {b}.
Claims: from the 1-cube, four iterations give AUSOs of dims 3,5,7,9 with BA
heights 4,9,16,25, all BA traces obeying both laws, and the dims 5 and 7
orientations violate Holt-Klee.  We check all of it with our own code,
including our own Holt-Klee max-flow test (unit vertex capacities on every
face), validated on the 12 AUSOs of the 2-cube and on the paper's G# outmap.
"""
import sys
sys.path.insert(0, '.')
from auso import is_uso, is_acyclic, ba_heights, ba_trace, obeys_laws, enumerate_ausos


def D(sA, m):
    hA = ba_heights(sA, m)
    assert hA is not None
    n = 1 << m
    ones = n - 1
    A, B = 1 << m, 1 << (m + 1)
    s = [0] * (n << 2)
    for layer in range(4):
        alpha, beta = layer & 1, layer >> 1
        for v in range(n):
            lo = sA[v ^ ones] if layer == 0 else sA[v]
            even = (hA[v] % 2 == 0)
            if (alpha, beta) == (0, 0):
                hi = 0
            elif (alpha, beta) == (1, 0):
                hi = (A | B) if even else A
            elif (alpha, beta) == (0, 1):
                hi = B if even else (A | B)
            else:
                hi = A if even else B
            s[v | (alpha * A) | (beta * B)] = lo | hi
    return s


# ---------- Holt-Klee: my own max-flow with unit vertex capacities ----------
def maxflow_unit(nodes, arcs, src, snk):
    """Vertex-disjoint directed paths from src to snk: split each internal
    node x into x_in -> x_out (cap 1); arcs u->v become u_out -> v_in (cap 1).
    Edmonds-Karp on a small graph."""
    from collections import deque, defaultdict
    cap = defaultdict(int)
    adj = defaultdict(set)

    def add(u, v, c):
        cap[(u, v)] += c
        adj[u].add(v)
        adj[v].add(u)

    for x in nodes:
        if x != src and x != snk:
            add(('i', x), ('o', x), 1)
    for (u, v) in arcs:
        uo = ('o', u) if u != src else ('S',)
        vi = ('i', v) if v != snk else ('T',)
        add(uo, vi, 1)
    S, T = ('S',), ('T',)
    flow = 0
    while True:
        par = {S: None}
        q = deque([S])
        while q and T not in par:
            u = q.popleft()
            for w in adj[u]:
                if w not in par and cap[(u, w)] > 0:
                    par[w] = u
                    q.append(w)
        if T not in par:
            return flow
        w = T
        while par[w] is not None:
            u = par[w]
            cap[(u, w)] -= 1
            cap[(w, u)] += 1
            w = u
        flow += 1


def face_iter(m):
    """Faces as (free mask, fixed bits): every pair (free, base) with base's
    free bits zero."""
    n = 1 << m
    for free in range(n):
        fixed = (n - 1) ^ free
        b = fixed
        # enumerate all subsets of fixed as base
        sub = fixed
        while True:
            yield free, sub
            if sub == 0:
                break
            sub = (sub - 1) & fixed


def is_holt_klee(s, m, only_dim=None):
    """Every face of dimension d >= 1 has d vertex-disjoint directed paths
    from its unique source to its unique sink.  Returns (ok, witness face)."""
    n = 1 << m
    for free, base in face_iter(m):
        d = bin(free).count('1')
        if d < 2:
            continue  # d = 0,1 trivial
        if only_dim is not None and d != only_dim:
            continue
        # vertices of the face
        verts = []
        sub = free
        while True:
            verts.append(base | sub)
            if sub == 0:
                break
            sub = (sub - 1) & free
        sinks = [v for v in verts if (s[v] & free) == 0]
        sources = [v for v in verts if (s[v] & free) == free]
        if len(sinks) != 1 or len(sources) != 1:
            return False, ('not a USO face', free, base)
        src, snk = sources[0], sinks[0]
        arcs = []
        for v in verts:
            out = s[v] & free
            i = 0
            while out:
                if out & 1:
                    arcs.append((v, v ^ (1 << i)))
                out >>= 1
                i += 1
        f = maxflow_unit(verts, arcs, src, snk)
        if f < d:
            return False, (free, base, d, f)
    return True, None


def check(s, m, name):
    n = 1 << m
    uso = is_uso(s, m)
    acy = is_acyclic(s, m)
    h = ba_heights(s, m)
    hmax = max(h) if h else None
    laws = all(obeys_laws(ba_trace(s, v)) for v in range(n))
    print(f'{name}: dim {m}, USO {uso}, acyclic {acy}, BA height {hmax}, laws {laws}')
    return s


if __name__ == '__main__':
    # validation of the HK test: all 12 AUSOs of the 2-cube are Holt-Klee;
    # the paper's G# 4-cube orientation is NOT (3 paths where 4 needed)
    a2 = enumerate_ausos(2)
    print('AUSOs of 2-cube:', len(a2), 'all HK:', all(is_holt_klee(s, 2)[0] for s in a2))
    a3 = enumerate_ausos(3)
    hk3 = sum(1 for s in a3 if is_holt_klee(s, 3)[0])
    print('AUSOs of 3-cube:', len(a3), 'Holt-Klee among them:', hk3,
          'max BA height overall:', max(max(ba_heights(s, 3)) for s in a3),
          'max BA height among HK:', max(max(ba_heights(s, 3)) for s in a3 if is_holt_klee(s, 3)[0]))
    gsharp = [0, 1, 3, 6, 7, 4, 13, 10, 14, 15, 9, 12, 11, 8, 5, 2]
    ok, wit = is_holt_klee(gsharp, 4)
    print('G# outmap: USO', is_uso(gsharp, 4), 'acyclic', is_acyclic(gsharp, 4),
          'BA heights', ba_heights(gsharp, 4), 'Holt-Klee', ok, wit)

    s = [1, 0]  # the 1-cube: sink at 0
    m = 1
    check(s, m, 'seed')
    for it in range(4):
        s = D(s, m)
        m += 2
        check(s, m, f'D^{it+1}')
        if m <= 7:
            ok, wit = is_holt_klee(s, m)
            print(f'   Holt-Klee: {ok} {wit}')
        else:
            ok, wit = is_holt_klee(s, m, only_dim=m)
            print(f'   Holt-Klee on the whole cube only: {ok} {wit}')
