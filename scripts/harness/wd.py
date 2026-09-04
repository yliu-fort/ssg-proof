"""WD(e,j,m): the wedge family on which round 11 claims the own-successor
hybrid stays silent for 2^{Omega(N)} rounds.  Rebuilt from the STATEMENT.

  eps = 2^-e, delta = 2^-j, gamma = 2^-m, lambda = 1 - 2 delta.
  Vmax = {v_1, v_2}, Vmin empty, everything else average.
    H          -> (t1, t0)                                   [value 1/2]
    W chain w_1..w_L, L = m-j, realising 1/2 - 2^{-(m-j)}:
        w_1 -> (t0, w_2);  w_q -> (t1, w_{q+1}) for 2 <= q < L;  w_L -> (t1,t0)
    a_{i,q}    -> (v_i, a_{i,q+1})  for q < e;   a_{i,e} -> (v_i, H)
    b_i        -> (v_i, c_{i,1})
    c_{i,q}    -> (v_{3-i}, c_{i,q+1}) for q < j-1;  c_{i,j-1} -> (v_{3-i}, w_1)
    v_i        -> (a_{i,1}, b_i)
  N = 2e + j + m + 5;  val(v_i) = val(a_{i,1}) = 1/2, val(b_i) = 1/2 - gamma.
"""
from fractions import Fraction as F
from mycore import G


def WD(e, j, m):
    assert e >= 1 and j >= 2 and m >= j + 1
    L = m - j
    names = ['v1', 'v2', 'H'] + [f'w{q}' for q in range(1, L + 1)]
    for i in (1, 2):
        names += [f'a{i}_{q}' for q in range(1, e + 1)]
        names += [f'b{i}']
        names += [f'c{i}_{q}' for q in range(1, j)]
    idx = {nm: k for k, nm in enumerate(names)}
    n = len(names)
    T0, T1 = 'T0', 'T1'
    kind = {nm: 'avg' for nm in names}
    kind['v1'] = kind['v2'] = 'max'
    s = {}
    s['H'] = (T1, T0)
    if L == 1:
        s['w1'] = (T0, T1)                 # value 1/2 - 1/2 = 0 ... guard below
    else:
        s['w1'] = (T0, 'w2')
        for q in range(2, L):
            s[f'w{q}'] = (T1, f'w{q+1}')
        s[f'w{L}'] = (T1, T0)
    for i in (1, 2):
        other = 3 - i
        for q in range(1, e):
            s[f'a{i}_{q}'] = (f'v{i}', f'a{i}_{q+1}')
        s[f'a{i}_{e}'] = (f'v{i}', 'H')
        s[f'b{i}'] = (f'v{i}', f'c{i}_1')
        for q in range(1, j - 1):
            s[f'c{i}_{q}'] = (f'v{other}', f'c{i}_{q+1}')
        s[f'c{i}_{j-1}'] = (f'v{other}', 'w1')
        s[f'v{i}'] = (f'a{i}_1', f'b{i}')

    def num(x):
        return n if x == T0 else (n + 1 if x == T1 else idx[x])

    kinds = [kind[nm] for nm in names]
    succ = [(num(s[nm][0]), num(s[nm][1])) for nm in names]
    return G(kinds, succ), idx
