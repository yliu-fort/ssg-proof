"""CC(L,m): the family on which the hybrid-rate route claims the hybrid needs
2^{Omega(N)} rounds.  Rebuilt here from the STATEMENT, not from their code.

  Max v_1, v_2;  e avg -> (t1,t0);
  d-chain d_1..d_m:  d_1 -> (t0,d_2),  d_j -> (t1,d_{j+1}) for 2<=j<=m-1,
                     d_m -> (t1,t0);
  chain ch(l,b,z):   p_j -> (b,p_{j+1}) for j<l,  p_l -> (b,z);
  A_1 = ch(L, v_2, e),  B_1 = ch(2L, v_1, d_1),
  A_2 = ch(L, v_1, e),  B_2 = ch(2L, v_2, d_1);
  v_1 -> (A_1, B_1),    v_2 -> (A_2, B_2).
Claims: N = 6L+m+5, stopping, one-player (Vmin empty),
w*(v_i) = w*(A_i) = 1/2, w*(B_i) = 1/2 - 2^{-2L-m}, w*(d_1) = 1/2 - 2^{-m}.
"""
from mycore import G


def CC(L, m):
    assert L >= 1 and m >= 2
    # lay out vertices, carrying sinks as sentinels until the very end
    names = ['v1', 'v2', 'e'] + [f'd{j}' for j in range(1, m + 1)]
    names += [f'A1_{j}' for j in range(1, L + 1)]
    names += [f'B1_{j}' for j in range(1, 2 * L + 1)]
    names += [f'A2_{j}' for j in range(1, L + 1)]
    names += [f'B2_{j}' for j in range(1, 2 * L + 1)]
    idx = {nm: i for i, nm in enumerate(names)}
    n = len(names)
    T0, T1 = 'T0', 'T1'
    kind = {nm: 'avg' for nm in names}
    kind['v1'] = kind['v2'] = 'max'
    s = {}
    s['e'] = (T1, T0)
    s['d1'] = (T0, 'd2') if m >= 2 else (T0, T1)
    for j in range(2, m):
        s[f'd{j}'] = (T1, f'd{j+1}')
    s[f'd{m}'] = (T1, T0)

    def chain(tag, l, b, z):
        for j in range(1, l):
            s[f'{tag}_{j}'] = (b, f'{tag}_{j+1}')
        s[f'{tag}_{l}'] = (b, z)

    chain('A1', L, 'v2', 'e')
    chain('B1', 2 * L, 'v1', 'd1')
    chain('A2', L, 'v1', 'e')
    chain('B2', 2 * L, 'v2', 'd1')
    s['v1'] = ('A1_1', 'B1_1')
    s['v2'] = ('A2_1', 'B2_1')

    def num(x):
        if x == T0:
            return n
        if x == T1:
            return n + 1
        return idx[x]

    kinds = [kind[nm] for nm in names]
    succ = [(num(s[nm][0]), num(s[nm][1])) for nm in names]
    return G(kinds, succ), idx, n
