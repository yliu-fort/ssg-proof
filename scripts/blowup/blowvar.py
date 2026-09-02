"""Search over dimension-raising rules of the Schurr-Szabo / D shape, restricted
to what a GAME can read.  Given an AUSO s_A of the m-cube, build an outmap on the
(m+2)-cube with vertices (alpha,beta,v):
   inner part on layer (a,b):  Tr_{ab}(s_A)(v)  with Tr in {id, trans (s_A(v xor 1bar)),
                               rev (complement of s_A(v))}
   outer part on layer (a,b):  rule[(a,b)][f(v)] in {0,A,B,AB}
   f(v) in a menu of binary readouts of the inner state.
Report, per (inner transform choice per layer, f), whether iterating from the
1-cube gives AUSOs and how the BA height grows.
"""
import sys, itertools
sys.path.insert(0, '.')
from auso import is_uso, is_acyclic, ba_heights

def transform(sA, m, kind):
    n = 1 << m; ones = n - 1
    if kind == 'id':   return list(sA)
    if kind == 'tr':   return [sA[v ^ ones] for v in range(n)]
    if kind == 'rev':  return [(ones ^ sA[v]) for v in range(n)]
    raise ValueError

def readouts(sA, m):
    """binary functions of the inner state v"""
    n = 1 << m; h = ba_heights(sA, m); sink = [v for v in range(n) if sA[v] == 0][0]
    src = [v for v in range(n) if sA[v] == n - 1][0]
    R = {}
    R['hpar'] = [h[v] & 1 for v in range(n)]                    # parity of BA height (NOT value-readable)
    R['sink'] = [1 if v == sink else 0 for v in range(n)]        # is the sink (readable: value maximal)
    R['nsink'] = [0 if v == sink else 1 for v in range(n)]
    R['src'] = [1 if v == src else 0 for v in range(n)]
    R['h1'] = [1 if h[v] >= 1 else 0 for v in range(n)]         # same as nsink
    R['h2'] = [1 if h[v] >= 2 else 0 for v in range(n)]         # height threshold (monotone along walk)
    R['hhalf'] = [1 if h[v] >= max(h)/2 else 0 for v in range(n)]
    R['bit0'] = [v & 1 for v in range(n)]                        # a single inner coordinate (readable? the
    R['pop'] = [bin(v).count('1') & 1 for v in range(n)]         #  choice at one vertex is not value-readable in general)
    return R

def build(sA, m, trs, rule, f):
    n = 1 << m; A, B = 1 << m, 1 << (m + 1)
    inner = {L: transform(sA, m, trs[L]) for L in range(4)}
    s = [0] * (n << 2)
    for L in range(4):
        a, b = L & 1, L >> 1
        for v in range(n):
            hi = rule[L][f[v]]
            s[v | (a * A) | (b * B)] = inner[L][v] | (hi[0] * A) | (hi[1] * B)
    return s

OUT = [(0,0),(1,0),(0,1),(1,1)]
def search(iters=3, verbose=False):
    seed = [1, 0]
    results = []
    tr_choices = ['id', 'tr', 'rev']
    # layer (0,0) transform varies; other layers identity (as in D); also try transform on layer (1,1)
    for tr00 in tr_choices:
      for tr11 in ['id', 'rev', 'tr']:
        trs = {0: tr00, 1: 'id', 2: 'id', 3: tr11}
        for fname in ['hpar', 'sink', 'nsink', 'h2', 'hhalf', 'bit0', 'pop', 'src']:
            # outer rule: layer (0,0) always empty (the sink layer); others depend on f
            for r1 in itertools.product(OUT, repeat=2):
              for r2 in itertools.product(OUT, repeat=2):
                for r3 in itertools.product(OUT, repeat=2):
                    rule = {0: ((0,0),(0,0)), 1: r1, 2: r2, 3: r3}
                    s, m = seed, 1
                    hs = []
                    ok = True
                    for it in range(iters):
                        f = readouts(s, m)[fname]
                        s2 = build(s, m, trs, rule, f)
                        m2 = m + 2
                        if not is_uso(s2, m2) or not is_acyclic(s2, m2):
                            ok = False; break
                        h = ba_heights(s2, m2)
                        hs.append(max(h)); s, m = s2, m2
                    if ok and len(hs) == iters:
                        results.append((hs, tr00, tr11, fname, rule))
    return results

if __name__ == '__main__':
    res = search(iters=3)
    print('rules giving AUSOs through 3 iterations:', len(res))
    # best by final height per (tr00,tr11,fname)
    best = {}
    for hs, t0, t3, f, rule in res:
        key = (t0, t3, f)
        if key not in best or hs[-1] > best[key][0][-1]:
            best[key] = (hs, rule)
    for key in sorted(best, key=lambda k: -best[k][0][-1]):
        print(key, best[key][0], best[key][1])
