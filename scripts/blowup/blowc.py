import sys; sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights, ba_trace

def blow(sA, m, mode):
    n = 1 << m; A, B = 1 << m, 1 << (m + 1)
    h = ba_heights(sA, m)
    sink = [v for v in range(n) if sA[v] == 0][0]
    start = max(range(n), key=lambda v: h[v])
    z = sink ^ start
    s = [0] * (n << 2)
    for layer in range(4):
        a, b = layer & 1, layer >> 1
        for v in range(n):
            if layer == 0:
                if mode == 'translate': lo = sA[v ^ z]
                elif mode == 'complement': lo = sA[v] ^ z          # reverse the edges in directions z
                elif mode == 'both': lo = sA[v ^ z] ^ z
                elif mode == 'complement_ones': lo = sA[v] ^ (n - 1)
            else:
                lo = sA[v]
            even = (h[v] % 2 == 0)
            if (a, b) == (0, 0): hi = 0
            elif (a, b) == (1, 0): hi = (A | B) if even else A
            elif (a, b) == (0, 1): hi = B if even else (A | B)
            else: hi = A if even else B
            s[v | (a * A) | (b * B)] = lo | hi
    return s, z

for mode in ['translate', 'complement', 'both', 'complement_ones']:
    s, m = [1, 0], 1
    out = []
    for it in range(5):
        s2, z = blow(s, m, mode); m2 = m + 2
        if not (is_uso(s2, m2) and is_acyclic(s2, m2)):
            out.append(('FAIL', 'uso' if not is_uso(s2, m2) else 'cyclic', 'z=', bin(z))); break
        out.append((max(ba_heights(s2, m2)), 'z=' + format(z, f'0{m}b')))
        s, m = s2, m2
    print(mode, out)
