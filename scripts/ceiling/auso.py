import sys
from itertools import product

def enum_uso(m):
    NP=1<<m
    s=[None]*NP
    out=[]
    def rec(v):
        if v==NP:
            out.append(tuple(s)); return
        forced_on=0; forced_off=0
        for i in range(m):
            u=v^(1<<i)
            if u<v:
                if s[u]>>i & 1: forced_off|=1<<i   # u->v so v's i-edge points back to u? no
                else: forced_on|=1<<i
        # i in s[u] means edge u -> u^ei ; consistency: i in s[v] iff i not in s[u]
        free=[i for i in range(m) if not ((forced_on|forced_off)>>i & 1)]
        base=forced_on
        for bits in range(1<<len(free)):
            val=base
            for j,i in enumerate(free):
                if bits>>j & 1: val|=1<<i
            ok=True
            for u in range(v):
                if ((s[u]^val)&(u^v))==0: ok=False;break
            if ok:
                s[v]=val; rec(v+1); s[v]=None
    rec(0)
    return out

def acyclic(s,m):
    NP=1<<m
    # topological sort of orientation digraph
    indeg=[0]*NP
    adj=[[] for _ in range(NP)]
    for v in range(NP):
        for i in range(m):
            if s[v]>>i&1:
                adj[v].append(v^(1<<i)); indeg[v^(1<<i)]+=1
    q=[v for v in range(NP) if indeg[v]==0]; cnt=0; order=[]
    while q:
        v=q.pop(); cnt+=1; order.append(v)
        for w in adj[v]:
            indeg[w]-=1
            if indeg[w]==0: q.append(w)
    return cnt==NP, order

def reach(s,m):
    NP=1<<m
    R=[set() for _ in range(NP)]
    ok,order=acyclic(s,m)
    for v in reversed(order):
        r=set()
        for i in range(m):
            if s[v]>>i&1:
                w=v^(1<<i); r.add(w); r|=R[w]
        R[v]=r
    return R

def run_len(s,m,start):
    v=start; L=0; seen=set()
    while s[v]!=0:
        v=v^s[v]; L+=1
        if L>10000: return None
    return L

for m in [2,3,4]:
    usos=enum_uso(m)
    na=0; best=0; bestinfo=None; lawC_viol=0; viol_example=None
    for s in usos:
        ok,order=acyclic(s,m)
        if not ok: continue
        na+=1
        for st in range(1<<m):
            L=run_len(s,m,st)
            if L>best: best=L; bestinfo=(s,st)
        R=reach(s,m)
        for u in range(1<<m):
            for v in R[u]:
                if ((s[u]&~s[v])&(u^v))==0:
                    lawC_viol+=1
                    if viol_example is None: viol_example=(s,u,v)
    print("m=%d  #USO=%d  #AUSO=%d  maxAllSwitchesRun=%d  info=%s  lawC violations(pairs)=%d ex=%s"%(m,len(usos),na,best,bestinfo,lawC_viol,viol_example), flush=True)
