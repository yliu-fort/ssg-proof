"""Hill-climb for stopping SSGs with both players on which def:bsi takes many
rounds.  Objective: max over the four corner starts of BSI rounds (veto
variant).  Exact arithmetic; logs every improvement with the instance."""
import sys, random, time; sys.path.insert(0, '.')
import mycore as M, bsi as B

def score(g):
    if not M.is_stopping(g): return -1
    if len(g.of('max')) < 2 or len(g.of('min')) < 2: return -1
    best = 0
    for a in (0, 1):
        for b in (0, 1):
            r, *_ = B.bsi(g, B.corner(g, 'max', a), B.corner(g, 'min', b), maxrounds=5000)
            best = max(best, r)
    return best

def rand_game(n, rng):
    T0, T1 = n, n + 1
    kinds = [rng.choice(['max', 'min', 'avg', 'avg']) for _ in range(n)]
    succ = []
    for v in range(n):
        s = []
        for _ in range(2):
            r = rng.random()
            s.append(T1 if r < 0.12 else T0 if r < 0.24 else rng.randrange(n))
        succ.append(tuple(s))
    return M.G(kinds, succ)

def mutate(g, rng):
    kinds = list(g.kinds); succ = [list(s) for s in g.succ]
    n = g.n
    for _ in range(rng.choice([1, 1, 2, 3])):
        v = rng.randrange(n)
        if rng.random() < 0.3:
            kinds[v] = rng.choice(['max', 'min', 'avg'])
        else:
            r = rng.random()
            succ[v][rng.randrange(2)] = g.T1 if r < 0.12 else g.T0 if r < 0.24 else rng.randrange(n)
    return M.G(kinds, [tuple(s) for s in succ])

def main(n, seed, minutes):
    rng = random.Random(seed)
    t_end = time.time() + 60 * minutes
    cur = None; cs = -1
    while cs < 0:
        cur = rand_game(n, rng); cs = score(cur)
    best, bs = cur, cs
    it = 0
    while time.time() < t_end:
        it += 1
        cand = mutate(cur, rng); s = score(cand)
        if s >= cs:
            cur, cs = cand, s
            if s > bs:
                best, bs = cand, s
                print(f"[n={n} seed={seed} it={it}] NEW BEST rounds={bs} N={best.N} |Vmax|={len(best.of('max'))} |Vmin|={len(best.of('min'))} a={len(best.of('avg'))}", flush=True)
                print("   kinds", best.kinds, "succ", best.succ, flush=True)
        if it % 500 == 0:
            if rng.random() < 0.3:
                cur, cs = rand_game(n, rng), -1
                while cs < 0: cur = rand_game(n, rng); cs = score(cur)
    print(f"[n={n} seed={seed}] done it={it} best={bs}", flush=True)

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
