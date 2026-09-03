import sys; sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights, ba_trace
from my_D import is_holt_klee
import json
# thm:blowup's B with z = sink xor u, u = first vertex of maximal height (blowz.py's 'sinkstart')
def B(sA, m):
    n = 1 << m; A, Bb = 1 << m, 1 << (m + 1)
    h = ba_heights(sA, m)
    sink = [v for v in range(n) if sA[v] == 0][0]
    starts = [v for v in range(n) if h[v] == max(h)]
    start = starts[0]
    z = sink ^ start
    s = [0] * (n << 2)
    for layer in range(4):
        a, b = layer & 1, layer >> 1
        for v in range(n):
            lo = sA[v ^ z] if layer == 0 else sA[v]
            even = (h[v] % 2 == 0)
            if (a, b) == (0, 0): hi = 0
            elif (a, b) == (1, 0): hi = (A | Bb) if even else A
            elif (a, b) == (0, 1): hi = Bb if even else (A | Bb)
            else: hi = A if even else Bb
            s[v | (a * A) | (b * Bb)] = lo | hi
    return s, z, starts
s, m = [1, 0], 1
paper_B2 = [7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
for level in (1,2,3):
    s, z, starts = B(s, m); m += 2
    ok = is_uso(s, m) and is_acyclic(s, m)
    h = ba_heights(s, m)
    top = [v for v in range(1<<m) if h[v] == max(h)]
    print(f'level {level}: dim {m}, z={z} (bit {z.bit_length()-1}), USO+acyclic={ok}, height={max(h)}, maximal vertices={top}, seed starts={starts}')
    if level == 2:
        print('  matches paper B^2:', s == paper_B2)
    if level == 3:
        hk, wit = is_holt_klee(s, m)
        print('  B^3 Holt-Klee:', hk, wit)
        print('  B^3 outmap:', s)
        print('  walk from', top[0], ':', ba_trace(s, top[0]))
        json.dump({'m': m, 'outmap': s, 'height': max(h), 'starts': top}, open('B3.json','w'))
