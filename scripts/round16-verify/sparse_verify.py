# Exact sparse verification of a two-player game file: outmap, nondegeneracy, USO, acyclicity, height, run.
import json, sys, itertools, time
from fractions import Fraction as F
sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights, ba_trace
def solve_sparse(kinds,succ,choice):
    n=len(kinds); t0,t1=n,n+1
    rows={}; rhs={}
    for v in range(n):
        r={v:F(1)}; b=F(0)
        tg=[(succ[v][0],F(1,2)),(succ[v][1],F(1,2))] if kinds[v]=='avg' else [(succ[v][choice[v]],F(1))]
        for u,c in tg:
            if u==t1: b+=c
            elif u==t0: pass
            else: r[u]=r.get(u,F(0))-c
        rows[v]=r; rhs[v]=b
    # eliminate variables in order of increasing fill: simple minimum-degree heuristic
    order=sorted(range(n), key=lambda v: len(rows[v]))
    x={}
    # forward elimination: process pivot rows; substitute pivot var into other rows containing it
    # maintain column index: which rows contain var
    col={v:set() for v in range(n)}
    for v,r in rows.items():
        for u in r: col[u].add(v)
    eliminated=[]
    remaining=set(range(n))
    while remaining:
        # choose pivot row with smallest size among remaining rows, pivot var = the row's own var if present
        piv=min(remaining, key=lambda v: len(rows[v]))
        r=rows[piv]
        if piv in r and r[piv]!=0: pv=piv
        else:
            pv=next(iter(k for k in r if r[k]!=0))
        c=r[pv]
        r={k:val/c for k,val in r.items() if val!=0}; rhs[piv]=rhs[piv]/c; rows[piv]=r
        for other in list(col[pv]):
            if other==piv or other not in remaining: continue
            ro=rows[other]; f=ro.get(pv,F(0))
            if f==0: continue
            for k,val in r.items():
                nv=ro.get(k,F(0))-f*val
                if nv==0:
                    if k in ro: del ro[k]; col[k].discard(other)
                else:
                    if k not in ro: col[k].add(other)
                    ro[k]=nv
            rhs[other]-=f*rhs[piv]
        remaining.discard(piv); eliminated.append((piv,pv))
        col[pv]=set()
    # back substitution
    for piv,pv in reversed(eliminated):
        r=rows[piv]; val=rhs[piv]
        for k,c in r.items():
            if k!=pv: val-=c*x[k]
        x[pv]=val
    return [x[v] for v in range(n)]
def stopping(kinds,succ):
    n=len(kinds); U=set(range(n)); ch=True
    while ch:
        ch=False
        for v in list(U):
            inU=[u in U for u in succ[v]]
            if not (all(inU) if kinds[v]=='avg' else any(inU)): U.discard(v); ch=True
    return not U
def analyse(path, target=None, start=None):
    g=json.load(open(path)); kinds=g['kinds']; succ=[tuple(s) for s in g['succ']]; n=len(kinds)
    maxv=[i for i in range(n) if kinds[i]=='max']; minv=[i for i in range(n) if kinds[i]=='min']
    print(path,'N',n+2,'Max',len(maxv),'Min',len(minv),'avg',kinds.count('avg'),'stopping',stopping(kinds,succ),flush=True)
    m=len(maxv); out=[0]*(2**m); deg=0; t=time.time(); vals_all={}
    for si in range(2**m):
        sigma={v:(si>>j)&1 for j,v in enumerate(maxv)}
        cand=[]
        for ti in range(2**len(minv)):
            ch=dict(sigma); ch.update({u:(ti>>j)&1 for j,u in enumerate(minv)}); cand.append(solve_sparse(kinds,succ,ch))
        vs=[min(c[v] for c in cand) for v in range(n)]; vals_all[si]=vs
        def w(u): return vs[u] if u<n else (F(1) if u==n+1 else F(0))
        bits=0
        for j,v in enumerate(maxv):
            a=sigma[v]; cur=w(succ[v][a]); oth=w(succ[v][1-a])
            if cur==oth: deg+=1
            if oth>cur: bits|=1<<j
        out[si]=bits
        if si%16==15: print(f'  {si+1}/{2**m} profiles, {time.time()-t:.0f}s',flush=True)
    h=ba_heights(out,m)
    print('outmap',out); print('tied incidences',deg,'USO',is_uso(out,m),'acyclic',is_acyclic(out,m),'height',max(h) if h else None)
    if target is not None: print('outmap == target:',out==target)
    if start is not None:
        tr=ba_trace(out,start); print('run from',start,':',tr,'length',len(tr)-1)
        inc=all(all(vals_all[tr[i+1]][v]>=vals_all[tr[i]][v] for v in range(n)) and vals_all[tr[i+1]]!=vals_all[tr[i]] for i in range(len(tr)-1))
        print('values nondecreasing and changing along the run:',inc)
    return out
if __name__=='__main__':
    B2=[7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
    pstr='00010111011000001111101101110001'; p=[int(c) for c in pstr]
    exec(open('free_parity.py').read().split('paper_B2=')[0].split('random.seed(3)')[1])  # defines Bpz
    target=Bpz(B2,5,p,0)
    analyse('../b3-level/TB_GAME_D10.json', target=target, start=44)
