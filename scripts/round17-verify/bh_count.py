#!/usr/bin/env python3
"""prop:blowup-height's cardinality clause: is the number of maximal-height vertices of an AUSO
always a power of two? Exhaustive over all USO outmaps of the 3-cube (self-contained)."""
import itertools
m = 3; V = range(2 ** m)
def is_uso(s):
    # every face has exactly one vertex with no outgoing edge inside the face
    for fixed in itertools.product([None, 0, 1], repeat=m):
        free = [i for i in range(m) if fixed[i] is None]
        verts = [v for v in V if all(fixed[i] is None or ((v >> i) & 1) == fixed[i] for i in range(m))]
        sinks = [v for v in verts if all(not ((s[v] >> i) & 1) for i in free)]
        if len(sinks) != 1: return False
    return True
def consistent(s):
    # edge orientation consistent: v has i out iff v^i has i in
    return all(((s[v] >> i) & 1) != ((s[v ^ (1 << i)] >> i) & 1) for v in V for i in range(m))
def acyclic(s):
    seen = {}
    def dfs(v, stack):
        if v in stack: return False
        if v in seen: return True
        stack.add(v)
        for i in range(m):
            if (s[v] >> i) & 1 and not dfs(v ^ (1 << i), stack): return False
        stack.discard(v); seen[v] = 1; return True
    return all(dfs(v, set()) for v in V)
def heights(s):
    h = {}
    for v in V:
        k = 0; x = v
        while s[x] != 0: x ^= s[x]; k += 1
        h[v] = k
    return h
cnt = 0; nonpow = []
for s in itertools.product(range(2 ** m), repeat=2 ** m):
    if not consistent(s) or not is_uso(s) or not acyclic(s): continue
    cnt += 1
    h = heights(s); H = max(h.values()); n = sum(1 for v in V if h[v] == H)
    if n & (n - 1): nonpow.append((s, n, H))
print('AUSOs of the 3-cube:', cnt)
print('with a non-power-of-two number of maximal-height vertices:', len(nonpow))
s = (2, 3, 1, 0, 6, 7, 4, 5)
print('auditor example', s, 'USO', consistent(s) and is_uso(s), 'acyclic', acyclic(s), 'heights', heights(s))
