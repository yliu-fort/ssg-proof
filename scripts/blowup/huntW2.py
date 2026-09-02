"""WALK-ONLY variant: only the incidences at the vertices of a prescribed
bottom-antipodal walk are constrained (s(v_t) = v_t xor v_{t+1}, s(v_L) = 0).
hunt7 generalised: integer-row search for a (m Max + k Min) harmonic normal
form whose Max-cube improvement outmap equals a prescribed target.
usage: huntG.py seed k den secs m t0,t1,...,t_{2^m-1}"""
import random, sys, time, json
import numpy as np
from fastnf import margins
seed, k, den, secs, m = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
TRACE = [int(x) for x in sys.argv[6].split(',')]
NS = 1 << m
L = len(TRACE) - 1
TARGET = {}
for t in range(L + 1):
    TARGET[TRACE[t]] = (TRACE[t] ^ TRACE[t + 1]) if t < L else 0
IDX = np.array([sg * m + i for sg in TARGET for i in range(m)])
T = np.array([1 if (TARGET[sg] >> i) & 1 else -1 for sg in TARGET for i in range(m)], dtype=np.int8)

def cost(Ai, bi):
    mu, Z = margins(Ai, bi, m, k, den)
    if mu is None: return 10**6, None
    f = mu.reshape(-1)[IDX]
    if np.any(np.abs(f) < 1e-11): return 10**6, None
    bad = (T * f < 0)
    return int(bad.sum()), float(np.sum(np.maximum(0.0, -T * f)))

def rand_state(n, rng):
    Ai = np.zeros((2 * n, n), dtype=np.int64); bi = np.zeros(2 * n, dtype=np.int64)
    for r in range(2 * n):
        while True:
            w = [rng.randrange(0, den // 2 + 1) for _ in range(n)]; q = rng.randrange(0, den // 2 + 1)
            if sum(w) + q < den: break
        Ai[r] = w; bi[r] = q
    return Ai, bi

def mutate(Ai, bi, n, rng, nm):
    Ai = Ai.copy(); bi = bi.copy()
    for _ in range(nm):
        r = rng.randrange(2 * n); j = rng.randrange(n + 1); step = rng.choice([1, -1, 2, -2, 4, -4])
        if j < n:
            v = Ai[r, j] + step
            if v < 0: continue
            old = Ai[r, j]; Ai[r, j] = v
            if Ai[r].sum() + bi[r] >= den: Ai[r, j] = old
        else:
            v = bi[r] + step
            if v < 0: continue
            old = bi[r]; bi[r] = v
            if Ai[r].sum() + bi[r] >= den: bi[r] = old
    return Ai, bi

rng = random.Random(seed); n = m + k
best = None; bestc = (10**9, 1e18); cur = None; curc = (10**9, 1e18)
t0 = time.time(); it = 0
while time.time() - t0 < secs:
    it += 1
    if cur is None or rng.random() < 0.002:
        Ai, bi = rand_state(n, rng)
    else:
        Ai, bi = mutate(cur[0], cur[1], n, rng, rng.randint(1, 3))
    c, s = cost(Ai, bi)
    if c >= 10**6: continue
    if (c, s) <= curc or rng.random() < 0.02:
        cur, curc = (Ai, bi), (c, s)
    if (c, s) < bestc:
        best, bestc = (Ai, bi), (c, s)
        print(f'[seed{seed} k={k} den={den} it{it} {time.time()-t0:.0f}s] wrong={c} soft={s:.4g}', flush=True)
        if c == 0:
            print('CANDIDATE'); print('A=', Ai.tolist()); print('b=', bi.tolist(), flush=True)
            json.dump(dict(m=m, k=k, den=den, A=Ai.tolist(), b=bi.tolist(), trace=TRACE), open(f'W_m{m}_L{L}_k{k}_den{den}_s{seed}.json', 'w'))
            break
    if it % 20000 == 0:
        cur = None; curc = (10**9, 1e18)
print(f'seed{seed}: best wrong {bestc[0]} soft {bestc[1]:.4g} in {it} iters', flush=True)
