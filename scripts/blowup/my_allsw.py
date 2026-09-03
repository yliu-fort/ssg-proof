"""Root all-switches loop, written from def:improvement-uso / prop:allsw-auso:
sigma -> sigma[S_sigma], S_sigma = {v in Vmax : val_sigma(other) > val_sigma(cur)},
val_sigma = Min's exact best response (policy iteration, sound on STOPPING games;
cross-checked against the min over all tau on small games).  Counts tied
incidences (val_sigma(other) == val_sigma(cur)) along the run."""
import sys, itertools
sys.path.insert(0, '.')
from fractions import Fraction as F
import mycore as M
from fast import val_sigma_fast, other


def val_sigma_brute(g, sigma):
    MN = g.of('min')
    best = None
    for choice in itertools.product([0, 1], repeat=len(MN)):
        tau = {u: g.succ[u][c] for u, c in zip(MN, choice)}
        v = M.profile_value(g, sigma, tau)
        best = v if best is None else [min(a, b) for a, b in zip(best, v)]
    return best


def all_switches(g, sigma, brute=False, maxrounds=10**6):
    """Returns (rounds, trace of switched sets, ties)."""
    MX = g.of('max')
    sigma = dict(sigma)
    trace, ties = [], 0
    for _ in range(maxrounds):
        v = val_sigma_brute(g, sigma) if brute else val_sigma_fast(g, sigma)[0]
        S = [x for x in MX if v[other(g, x, sigma[x])] > v[sigma[x]]]
        ties += sum(1 for x in MX if v[other(g, x, sigma[x])] == v[sigma[x]])
        if not S:
            return len(trace), trace, ties, v
        trace.append(tuple(S))
        for x in S:
            sigma[x] = other(g, x, sigma[x])
    raise RuntimeError('no convergence')


def ladder(n):
    """def:ladder L_n: Vmax v_1..v_n = 0..n-1, Vavg w_1..w_n = n..2n-1,
    v_i -> (v_{i+1}, w_{i+1}), w_i -> (v_{i+1}, w_{i+1}), v_{n+1} = t0, w_{n+1} = t1."""
    T0, T1 = 2 * n, 2 * n + 1
    kinds, succ = [], []
    for i in range(n):            # v_i
        kinds.append('max'); succ.append((i + 1 if i + 1 < n else T0, n + i + 1 if i + 1 < n else T1))
    for i in range(n):            # w_i
        kinds.append('avg'); succ.append((i + 1 if i + 1 < n else T0, n + i + 1 if i + 1 < n else T1))
    return M.G(kinds, succ)


def refuted7():
    """thm:all-switches-refuted: x,y Max; m Min; a,h Avg;
    x->{t0,a}, y->{m,h}, m->{a,x}, a->{y,t1}, h->{t1,t0}.  Indices x0 y1 m2 a3 h4, t0=5, t1=6."""
    kinds = ['max', 'max', 'min', 'avg', 'avg']
    succ = [(5, 3), (2, 4), (3, 0), (1, 6), (6, 5)]
    return M.G(kinds, succ)


if __name__ == '__main__':
    for n in range(1, 9):
        g = ladder(n)
        assert M.is_stopping(g)
        sigma = {v: g.succ[v][0] for v in g.of('max')}   # all v_i -> v_{i+1} (the 'all-zero' start)
        r, tr, ties, v = all_switches(g, sigma)
        rb, trb, _, vb = all_switches(g, sigma, brute=True)
        print(f'L_{n}: all-switches rounds {r} (brute {rb}), switched sets {tr}, ties {ties}, val(v_1) = {v[0]}')
    g = refuted7()
    print('7-vertex game stopping:', M.is_stopping(g), 'w* =', M.wstar(g)[:5])
    sigma = {0: 5, 1: 2}          # x->t0, y->m
    r, tr, ties, v = all_switches(g, sigma, brute=True)
    print('all-switches from (x->t0, y->m): rounds', r, 'trace', tr, 'ties', ties, 'final', v[:5])
    # single switch of x alone reaches the optimum (memory: (1,1,1,1,1/2))
    v1 = val_sigma_brute(g, {0: 3, 1: 2}); print('single switch x: ', v1[:5])
    v2 = val_sigma_brute(g, {0: 3, 1: 4}); print('both switched:   ', v2[:5])
