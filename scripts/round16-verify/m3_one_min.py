import json, itertools, sys
from fractions import Fraction as F
sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights
from my_D import is_holt_klee
def solve(kinds,succ,choice):
    n=len(kinds); t0,t1=n,n+1
    M=[[F(0)]*(n+1) for _ in range(n)]
    for v in range(n):
        M[v][v]+=1
        if kinds[v]=='avg': tg=[(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
        else: tg=[(succ[v][choice[v]],F(1))]
        for u,c in tg:
            if u==t1: M[v][n]+=c
            elif u==t0: pass
            else: M[v][u]-=c
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]; pv=M[c][c]; M[c]=[a/pv for a in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    return [M[i][n] for i in range(n)]
def stopping(kinds,succ):
    n=len(kinds); U=set(range(n)); ch=True
    while ch:
        ch=False
        for v in list(U):
            inU=[u in U for u in succ[v]]
            if not (all(inU) if kinds[v]=='avg' else any(inU)): U.discard(v); ch=True
    return not U
for name in ('G_m3_k1_a_game.json','G_m3_k1_b_game.json'):
    g=json.load(open(f'../min-budget/{name}'))
    kinds=g['kinds']; succ=[tuple(s) for s in g['succ']]; n=len(kinds)
    maxv=[i for i in range(n) if kinds[i]=='max']; minv=[i for i in range(n) if kinds[i]=='min']
    print(name,'N',n+2,'max',maxv,'min',minv,'avg',kinds.count('avg'),'stopping',stopping(kinds,succ))
    m=len(maxv); out=[0]*(2**m); degenerate=False
    for si in range(2**m):
        sigma={v:(si>>j)&1 for j,v in enumerate(maxv)}
        vals=[]
        for ti in range(2**len(minv)):
            ch=dict(sigma); ch.update({u:(ti>>j)&1 for j,u in enumerate(minv)}); vals.append(solve(kinds,succ,ch))
        vs=[min(vals[t][v] for t in range(len(vals))) for v in range(n)]   # val_sigma componentwise min over tau
        def w(u): return vs[u] if u<n else (F(1) if u==n+1 else F(0))
        bits=0
        for j,v in enumerate(maxv):
            a=sigma[v]; cur=w(succ[v][a]); oth=w(succ[v][1-a])
            if cur==oth: degenerate=True
            if oth>cur: bits|=1<<j
        out[si]=bits
    h=ba_heights(out,m)
    hk,wit=is_holt_klee(out,m)
    print('  outmap',out,'nondegenerate',not degenerate,'USO',is_uso(out,m),'acyclic',is_acyclic(out,m),'height',max(h) if h else None,'HK',hk)
