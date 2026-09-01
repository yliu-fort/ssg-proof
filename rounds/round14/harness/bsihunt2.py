"""Hill-climb: does def:bsi ever take MORE than |Vmax|+|Vmin| rounds, or switch
a vertex twice?  Objective = rounds - |C| (primary), repeat switches (secondary)."""
import sys, random, time; sys.path.insert(0, '.')
import mycore as M, bsi as B
from bsihunt import rand_game, mutate

def bsi_trace(g, sigma, tau):
    """like B.bsi but also counts how many times each vertex is switched."""
    maxs, mins = g.of('max'), g.of('min')
    sigma, tau = dict(sigma), dict(tau); cnt = {}
    for r in range(5000):
        L, _ = B.best_response_min(g, sigma, tau); U, _ = B.best_response_max(g, tau, sigma)
        Ssig = [v for v in maxs if L[B.other(g, v, sigma[v])] > L[sigma[v]]]
        Stau = [u for u in mins if U[B.other(g, u, tau[u])] < U[tau[u]]]
        Cmax = [v for v in Ssig if U[B.other(g, v, sigma[v])] >= U[sigma[v]]]
        Cmin = [u for u in Stau if L[B.other(g, u, tau[u])] <= L[tau[u]]]
        if not Cmax and not Cmin: return r, cnt
        for v in Cmax: sigma[v] = B.other(g, v, sigma[v]); cnt[v] = cnt.get(v, 0) + 1
        for u in Cmin: tau[u] = B.other(g, u, tau[u]); cnt[u] = cnt.get(u, 0) + 1
    raise RuntimeError

def score(g):
    if not M.is_stopping(g): return (-99, 0)
    if len(g.of('max')) < 2 or len(g.of('min')) < 2: return (-99, 0)
    C = len(g.of('max')) + len(g.of('min'))
    best = (-99, 0)
    for a in (0, 1):
        for b in (0, 1):
            r, cnt = bsi_trace(g, B.corner(g, 'max', a), B.corner(g, 'min', b))
            rep = sum(1 for v in cnt.values() if v >= 2)
            best = max(best, (r - C, rep))
    return best

def main(n, seed, minutes):
    rng = random.Random(seed); t_end = time.time() + 60 * minutes
    cur = None; cs = (-99, 0)
    while cs[0] <= -99: cur = rand_game(n, rng); cs = score(cur)
    best, bs = cur, cs; it = 0
    while time.time() < t_end:
        it += 1
        cand = mutate(cur, rng); s = score(cand)
        if s >= cs:
            cur, cs = cand, s
            if s > bs:
                best, bs = cand, s
                print(f"[n={n} seed={seed} it={it}] NEW BEST rounds-|C|={bs[0]} repeats={bs[1]} N={best.N} |Vmax|={len(best.of('max'))} |Vmin|={len(best.of('min'))} a={len(best.of('avg'))}", flush=True)
                print("   kinds", best.kinds, "succ", best.succ, flush=True)
        if it % 400 == 0 and rng.random() < 0.3:
            cur, cs = None, (-99, 0)
            while cs[0] <= -99: cur = rand_game(n, rng); cs = score(cur)
    print(f"[n={n} seed={seed}] done it={it} best={bs}", flush=True)

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
