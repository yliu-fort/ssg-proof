#!/usr/bin/env python3
"""The step the realisation-space novelty auditor supplied for rs:no-doubling, checked combinatorially.
For an outmap S of the 5-cube (coordinates 0..4 = seed, alpha_1, beta_1, alpha_2, beta_2) and a candidate
pin pair (p,q), the pinned layer is {p = 0, q = 0}; on it the inner orientation is S restricted to the
other three coordinates, and rs:upclosed demands that E_x := {inner sigma : x in S(sigma, p=0, q=0)} be
closed under improving single switches of inner coordinates (which raise the block's values, lem:switch).
Which (p,q) pass for B^2 itself, and for its four doubling translates B^2(. xor z)?"""
import itertools
B2 = [7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
m = 5
def translate(S, z): return [S[v ^ z] for v in range(2 ** m)]
def heights(S):
    h = {}
    for v in range(2 ** m):
        k = 0; x = v
        while S[x]: x ^= S[x]; k += 1
        h[v] = k
    return h
def passes(S, p, q):
    inner = [i for i in range(m) if i not in (p, q)]
    layer = [v for v in range(2 ** m) if not (v >> p) & 1 and not (v >> q) & 1]
    viol = 0
    for x in (p, q):
        for v in layer:
            if not (S[v] >> x) & 1: continue            # v not in E_x
            for i in inner:
                if (S[v] >> i) & 1:                       # improving single switch of inner coordinate i
                    if not (S[v ^ (1 << i)] >> x) & 1: viol += 1
    return viol
h = heights(B2); sink = B2.index(0); H = max(h.values())
print('B^2: sink', sink, 'height', H, 'maximal vertices', [v for v in range(32) if h[v] == H])
doubling = [z for z in range(32) if h[sink ^ z] == H]
print('doubling translations z (h(sink xor z) = 10):', doubling, ' -- all carry the alpha_2 bit (bit 3):', all((z >> 3) & 1 for z in doubling))
inner_z = [z for z in range(32) if not (z >> 3) & 1 and not (z >> 4) & 1]
print('best purely inner translation: max h(sink xor z) =', max(h[sink ^ z] for z in inner_z), '-> cap 10 + 2 +', max(h[sink ^ z] for z in inner_z))
names = ['seed', 'a1', 'b1', 'a2', 'b2']
print('\nup-closedness violations at the (0,0) layer of each candidate pin pair:')
print('  target:       ' + '  '.join(f'{names[p]},{names[q]:>4}' for p, q in itertools.combinations(range(m), 2)))
for label, S in [('B^2', B2)] + [(f'B^2(.xor {z})', translate(B2, z)) for z in doubling]:
    row = [passes(S, p, q) for p, q in itertools.combinations(range(m), 2)]
    print(f'  {label:14s}' + '  '.join(f'{r:8d}' for r in row))
