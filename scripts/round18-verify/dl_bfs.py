#!/usr/bin/env python3
"""prop:b2-flip-distance's reachability claims: in the combed-flip graph restricted to ACYCLIC unique sink orientations,
a distance-decreasing path (every flip fixes one differing edge) of length 42 from B^2 to B^2(.^8) exists, and none
exists to B^2(.^24) or B^2(.^26). Exhaustive DFS over the monotone subgraph with memoisation."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl_verify import faces, is_uso, acyclic, dist
m = 5; n = 32; FACES = faces(m)
B2 = (7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18)
sys.setrecursionlimit(10000)
def monotone_path(start, target):
    seen = {}; nodes = [0]
    def dfs(s):
        nodes[0] += 1
        d = dist(s, target, m)
        if d == 0: return []
        if s in seen: return None
        for v in range(n):
            for k in range(m):
                if (v >> k) & 1: continue
                w = v | (1 << k)
                if ((s[v] >> k) & 1) == ((target[v] >> k) & 1): continue      # already agrees
                if (v ^ s[v]) != (w ^ s[w]): continue                          # not combed
                t = list(s); t[v] ^= 1 << k; t[w] ^= 1 << k; t = tuple(t)
                if not acyclic(t, m): continue
                r = dfs(t)
                if r is not None: return [(v, k)] + r
        seen[s] = True
        return None
    return dfs(start), nodes[0]
for z in (8, 24, 26):
    T = tuple(B2[v ^ z] for v in range(n)); d = dist(B2, T, m)
    path, nodes = monotone_path(B2, T)
    print(f'z={z}: d={d}; monotone combed path through acyclic USOs: {"length %d" % len(path) if path else "NONE"}; nodes searched {nodes}')
    if path:
        s = list(B2)
        for v, k in path:
            assert (v ^ s[v]) == ((v | 1 << k) ^ s[v | 1 << k])
            s[v] ^= 1 << k; s[v | 1 << k] ^= 1 << k
            assert is_uso(tuple(s), m, FACES) and acyclic(tuple(s), m)
        assert tuple(s) == T and len(path) == d
print('FLIP-DISTANCE REACHABILITY CLAIMS CONFIRMED')
