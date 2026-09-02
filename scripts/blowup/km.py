"""BA heights of the LP orientation of the Klee-Minty cube (exact rationals).
KM_d(eps): 0 <= x1 <= 1, eps x_{i-1} <= x_i <= 1 - eps x_{i-1}; maximise x_d.
Vertices <-> binary vectors b (b_i = 1 iff x_i at its upper bound).  Edge in
coordinate i flips b_i; orient towards larger objective (generic: no ties)."""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from auso import is_uso, is_acyclic, ba_heights

def vertex(b, d, eps):
    x = []
    prev = F(0)
    for i in range(d):
        lo, hi = (F(0), F(1)) if i == 0 else (eps * prev, 1 - eps * prev)
        xi = hi if (b >> i) & 1 else lo
        x.append(xi); prev = xi
    return x

def km_outmap(d, eps):
    n = 1 << d
    obj = [vertex(b, d, eps)[-1] for b in range(n)]
    s = [0] * n
    for b in range(n):
        out = 0
        for i in range(d):
            if obj[b ^ (1 << i)] > obj[b]:
                out |= 1 << i
        s[b] = out
    assert len(set(obj)) == n, 'ties'
    return s

for d in range(2, 13):
    s = km_outmap(d, F(1, 4))
    ok = is_uso(s, d) and is_acyclic(s, d)
    h = ba_heights(s, d)
    print(f'KM d={d}: AUSO {ok}, BA height max {max(h)}, height from the source {h[[v for v in range(1<<d) if s[v]==(1<<d)-1][0]]}')
