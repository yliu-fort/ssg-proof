#!/usr/bin/env python3
"""Deterministic outmap-query complexity of the class of ALL acyclic unique sink orientations of the
3-cube (every one realised by a stopping SSG, prop:m3-realised): an algorithm queries a vertex v and
learns the out-set s(v); it must name the sink. Exact minimax over the 728 AUSOs (query-model route: 4)."""
import itertools, sys
from functools import lru_cache
sys.setrecursionlimit(10000)
m = 3; V = range(8)
exec(open('bh_count.py').read().split('cnt = 0')[0])          # consistent, is_uso, acyclic
AUSOS = [s for s in itertools.product(range(8), repeat=8) if consistent(s) and is_uso(s) and acyclic(s)]
print('AUSOs:', len(AUSOS))
IDX = {s: i for i, s in enumerate(AUSOS)}
sink = [s.index(0) for s in AUSOS]
@lru_cache(maxsize=None)
def depth(state):
    """state: frozenset of indices of orientations still consistent; 0 if all share the sink"""
    if len({sink[i] for i in state}) == 1: return 0
    best = 99
    for v in V:
        groups = {}
        for i in state: groups.setdefault(AUSOS[i][v], []).append(i)
        if len(groups) == 1: continue                          # uninformative query
        worst = max(depth(frozenset(g)) for g in groups.values())
        best = min(best, 1 + worst)
    return best
D = depth(frozenset(range(len(AUSOS))))
print('deterministic outmap-query complexity of the 3-cube AUSO class:', D, '(route: 4)')
# the same for the 2-cube and 1-cube classes as a sanity check
for mm, expect in ((1, 1), (2, 2)):
    m = mm; V = range(2 ** m)
    A2 = [s for s in itertools.product(range(2 ** m), repeat=2 ** m) if consistent(s) and is_uso(s) and acyclic(s)]
    snk = [s.index(0) for s in A2]
    @lru_cache(maxsize=None)
    def d2(state):
        if len({snk[i] for i in state}) == 1: return 0
        best = 99
        for v in V:
            groups = {}
            for i in state: groups.setdefault(A2[i][v], []).append(i)
            if len(groups) == 1: continue
            best = min(best, 1 + max(d2(frozenset(g)) for g in groups.values()))
        return best
    print(f'  {mm}-cube: {len(A2)} AUSOs, complexity {d2(frozenset(range(len(A2))))} (expected {expect})')
