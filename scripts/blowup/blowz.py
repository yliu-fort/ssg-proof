import sys; sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights, ba_trace

def D_general(sA, m, mode):
    """Layer (0,0): inner = s_A(v xor z) with z chosen by mode; outer as in D (parity of h_A)."""
    n = 1 << m; A, B = 1 << m, 1 << (m + 1)
    h = ba_heights(sA, m)
    sink = [v for v in range(n) if sA[v] == 0][0]
    start = max(range(n), key=lambda v: h[v])
    if mode == 'ones': z = n - 1
    elif mode == 'sinkstart': z = sink ^ start
    elif mode == 'rev': z = None
    s = [0] * (n << 2)
    for layer in range(4):
        a, b = layer & 1, layer >> 1
        for v in range(n):
            if layer == 0:
                lo = (n - 1) ^ sA[v] if mode == 'rev' else sA[v ^ z]
            else:
                lo = sA[v]
            even = (h[v] % 2 == 0)
            if (a, b) == (0, 0): hi = 0
            elif (a, b) == (1, 0): hi = (A | B) if even else A
            elif (a, b) == (0, 1): hi = B if even else (A | B)
            else: hi = A if even else B
            s[v | (a * A) | (b * B)] = lo | hi
    return s

def rev(s, m):
    n = 1 << m; return [(n - 1) ^ x for x in s]

for mode in ['ones', 'sinkstart', 'rev']:
    s, m = [1, 0], 1
    hs = []
    for it in range(5):
        s2 = D_general(s, m, mode); m2 = m + 2
        ok = is_uso(s2, m2) and is_acyclic(s2, m2)
        if not ok: hs.append(None); break
        h = ba_heights(s2, m2); hs.append(max(h))
        # reversed orientation: walk length from the old sink (= source of the reversal) and its max height
        r = rev(s2, m2); hr = ba_heights(r, m2)
        oldsink = [v for v in range(1 << m2) if s2[v] == 0][0]
        hs[-1] = (max(h), 'rev-from-old-sink', hr[oldsink] if hr else None, 'rev-max', max(hr) if hr else None,
                  'rev AUSO', is_uso(r, m2) and is_acyclic(r, m2))
        s, m = s2, m2
    print(mode, hs)
