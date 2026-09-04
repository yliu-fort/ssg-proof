"""Realise a FULL Max-cube orientation with the round-13 machinery: outer ES
over the transition part P (ap_es), inner exact LP over the payoff part Q
(ap_lp), then rounding to dyadic rows and EXACT re-verification (nf2).
usage: realiseAP.py seed m k budget_secs s0,s1,...   [den1,den2,...]"""
import sys, json, time
import numpy as np
from fractions import Fraction as F
from ap_es import search
from fastnf import margins
from nf2 import NF

seed, m, k, budget = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
TARGET = [int(x) for x in sys.argv[5].split(',')]
DENS = [int(x) for x in sys.argv[6].split(',')] if len(sys.argv) > 6 else [128, 256, 512, 1024]
n = m + k
cons = [(sg, i, 'pos' if (TARGET[sg] >> i) & 1 else 'neg') for sg in range(1 << m) for i in range(m)]
rng = np.random.default_rng(seed)
t0 = time.time()
P, Q, taus, it = search(m, k, cons, 1e-3, rng, budget, restart=1500, report=True)
print(f'seed{seed} m={m} k={k}: search {"succeeded" if P is not None else "failed"} after {it} iters, {time.time()-t0:.0f}s', flush=True)
if P is None:
    sys.exit(1)

def exact_outmap(Ai, bi, den):
    Pq = [[[F(int(Ai[2*v+a][j]), den) for j in range(n)] for a in (0, 1)] for v in range(n)]
    Qq = [[F(int(bi[2*v+a]), den) for a in (0, 1)] for v in range(n)]
    nf = NF(m, k, Pq, Qq)
    return nf.outmap()

def clip(Ai, bi, den):
    Ai = np.maximum(Ai, 0); bi = np.maximum(bi, 0)
    for r in range(Ai.shape[0]):
        while Ai[r].sum() + bi[r] >= den:
            j = int(np.argmax(Ai[r]))
            if bi[r] > Ai[r][j]: bi[r] -= 1
            else: Ai[r][j] -= 1
    return Ai, bi

# Q from ap_lp is a vector of length 2n (payoff column), P is (2n, n)
Qv = np.array(Q).reshape(-1)[:2 * n]
for den in DENS:
    Ai = np.rint(P * den).astype(np.int64); bi = np.rint(Qv * den).astype(np.int64)
    Ai, bi = clip(Ai, bi, den)
    s, ndeg = exact_outmap(Ai, bi, den)
    ok = (s == TARGET)
    print(f'  den={den}: exact outmap matches {ok}, nondegenerate {ndeg}', flush=True)
    if ok:
        json.dump(dict(m=m, k=k, den=den, A=Ai.tolist(), b=bi.tolist(), target=TARGET),
                  open(f'AP_m{m}_k{k}_den{den}_s{seed}.json', 'w'))
        print('SAVED', flush=True)
        sys.exit(0)
# small integer repair from the rounded float solution (wrong-count cost)
import random
den = DENS[-1]
Ai = np.rint(P * den).astype(np.int64); bi = np.rint(Qv * den).astype(np.int64); Ai, bi = clip(Ai, bi, den)
T = np.array([[1 if (TARGET[sg] >> i) & 1 else -1 for i in range(m)] for sg in range(1 << m)], dtype=np.int8).reshape(-1)
def cost(Ai, bi):
    mu, Z = margins(Ai, bi, m, k, den)
    if mu is None: return 10**6
    f = mu.reshape(-1)
    return int((T * f <= 0).sum())
r = random.Random(seed); cur = (Ai, bi); curc = cost(Ai, bi); t1 = time.time()
while time.time() - t1 < 300 and curc > 0:
    A2 = cur[0].copy(); b2 = cur[1].copy()
    for _ in range(r.randint(1, 3)):
        rr = r.randrange(2 * n); j = r.randrange(n + 1); st = r.choice([1, -1, 2, -2])
        if j < n:
            if A2[rr][j] + st >= 0: A2[rr][j] += st
        else:
            if b2[rr] + st >= 0: b2[rr] += st
    A2, b2 = clip(A2, b2, den)
    c = cost(A2, b2)
    if c <= curc: cur, curc = (A2, b2), c
print(f'  repair: wrong={curc}', flush=True)
if curc == 0:
    s, ndeg = exact_outmap(cur[0], cur[1], den)
    print('  exact after repair:', s == TARGET, 'nondegenerate', ndeg, flush=True)
    if s == TARGET:
        json.dump(dict(m=m, k=k, den=den, A=cur[0].tolist(), b=cur[1].tolist(), target=TARGET), open(f'AP_m{m}_k{k}_den{den}_s{seed}.json', 'w')); print('SAVED', flush=True)
