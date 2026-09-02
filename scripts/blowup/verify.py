"""Exact verification of a built SSG, from the GAME.
 - stopping by the trap characterisation (lem:trapchar)
 - pair values by exact rational elimination (average vertices first, in reverse
   topological order: no fill-in), cross-checked against mycore.profile_value
 - val_sigma = componentwise MIN over ALL positional tau (never greedy)
 - nondegeneracy, improvement outmap, USO / acyclicity / BA height
"""
from fractions import Fraction as F
from itertools import product
import mycore
from auso import is_uso, is_acyclic, ba_heights, ba_trace


def pair_value(kinds, succ, sigma, tau):
    """sigma: dict maxvertex -> chosen successor; tau likewise."""
    n = len(kinds)
    T0, T1 = n, n + 1
    dist = []
    for v in range(n):
        d = {}
        if kinds[v] == 'max':
            d[sigma[v]] = d.get(sigma[v], F(0)) + 1
        elif kinds[v] == 'min':
            d[tau[v]] = d.get(tau[v], F(0)) + 1
        else:
            for u in succ[v]:
                d[u] = d.get(u, F(0)) + F(1, 2)
        dist.append(d)
    # eliminate average vertices in reverse topological order of the DAG they form
    avg = [v for v in range(n) if kinds[v] == 'avg']
    order, mark = [], {}
    def visit(v):
        st = [(v, 0)]
        while st:
            u, ph = st.pop()
            if ph == 0:
                if mark.get(u): continue
                mark[u] = 1
                st.append((u, 1))
                for w in dist[u]:
                    if w < n and kinds[w] == 'avg' and not mark.get(w):
                        st.append((w, 0))
            else:
                order.append(u)
    for v in avg:
        visit(v)
    expand = {}
    for v in order:                                # children already expanded
        d = {}
        for u, p in dist[v].items():
            if u < n and kinds[u] == 'avg':
                for w, pw in expand[u].items():
                    d[w] = d.get(w, F(0)) + p * pw
            else:
                d[u] = d.get(u, F(0)) + p
        expand[v] = d
    C = [v for v in range(n) if kinds[v] != 'avg']
    idx = {v: i for i, v in enumerate(C)}
    r = len(C)
    A = [[F(0)] * r for _ in range(r)]
    b = [F(0)] * r
    for v in C:
        i = idx[v]
        A[i][i] += 1
        d = {}
        for u, p in dist[v].items():
            if u < n and kinds[u] == 'avg':
                for w, pw in expand[u].items():
                    d[w] = d.get(w, F(0)) + p * pw
            else:
                d[u] = d.get(u, F(0)) + p
        for u, p in d.items():
            if u == T1:
                b[i] += p
            elif u == T0:
                pass
            else:
                A[i][idx[u]] -= p
    x = mycore._lin_solve(A, b)
    val = [F(0)] * (n + 2)
    val[T1] = F(1)
    for v in C:
        val[v] = x[idx[v]]
    for v in order:
        s = F(0)
        for u, p in expand[v].items():
            s += p * (F(1) if u == T1 else (F(0) if u == T0 else val[u]))
        val[v] = s
    return val


def analyse(kinds, succ, cross=0):
    n = len(kinds)
    g = mycore.G(kinds, succ)
    assert mycore.is_stopping(g), 'NOT STOPPING'
    MX = [v for v in range(n) if kinds[v] == 'max']
    MN = [v for v in range(n) if kinds[v] == 'min']
    m, k = len(MX), len(MN)
    vals = {}
    for sc in product(*[[0, 1]] * m) if m else [()]:
        sigma = {v: succ[v][sc[i]] for i, v in enumerate(MX)}
        cur = None
        for tc in product(*[[0, 1]] * k) if k else [()]:
            tau = {v: succ[v][tc[i]] for i, v in enumerate(MN)}
            val = pair_value(kinds, succ, sigma, tau)
            if cross:
                ref = mycore.profile_value(g, sigma, tau)
                assert val == ref, 'pair value mismatch'
                cross -= 1
            cur = val if cur is None else [min(a, b) for a, b in zip(cur, val)]
        # cur is val_sigma: check it is a fixed point of T_sigma
        y = list(cur)
        for v in range(n):
            a, b = succ[v]
            if kinds[v] == 'max':
                y[v] = cur[sigma[v]]
            elif kinds[v] == 'min':
                y[v] = min(cur[a], cur[b])
            else:
                y[v] = (cur[a] + cur[b]) / 2
        assert y == cur[:n] + cur[n:] or y[:n] == cur[:n], 'val_sigma not a fixed point'
        code = sum(sc[i] << i for i in range(m))
        vals[code] = cur
    s = [0] * (1 << m)
    ndeg = True
    for code, val in vals.items():
        o = 0
        for i, v in enumerate(MX):
            a, b = succ[v]
            if val[a] == val[b]:
                ndeg = False
            cur_choice = succ[v][(code >> i) & 1]
            other = b if cur_choice == a else a
            if val[other] > val[cur_choice]:
                o |= 1 << i
        s[code] = o
    return dict(m=m, k=k, N=n + 2, outmap=s, nondegenerate=ndeg,
                uso=is_uso(s, m), acyclic=is_acyclic(s, m),
                heights=ba_heights(s, m), vals=vals, MX=MX, MN=MN)
