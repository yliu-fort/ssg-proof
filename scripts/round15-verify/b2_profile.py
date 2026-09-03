"""Profile cube of the B^2 game (5 Max + 1 Min): profile-nondegenerate? USO? acyclic? Holt-Klee? BA height?"""
import sys, json, itertools, time, collections
from fractions import Fraction as F
_t=open('hk_product.py').read(); exec(_t[_t.index('def is_uso'):_t.index('def product')])  # is_uso, acyclic, max_height, is_hk
d=json.load(open('../blowup/B2_small_GAME.json'))
kinds=d['kinds']; succ=[tuple(s) for s in d['succ']]; n=len(kinds); t0,t1=n,n+1
C=[v for v in range(n) if kinds[v] in ('max','min')]; c=len(C)
def solve(choice):
    M=[[F(0)]*n for _ in range(n)]; q=[F(0)]*n
    for v in range(n):
        tg=[(choice[v],F(1))] if kinds[v] in ('max','min') else [(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
        for u,p in tg:
            if u==t1: q[v]+=p
            elif u<n: M[v][u]+=p
    aug=[[(F(1) if i==j else F(0))-M[i][j] for j in range(n)]+[q[i]] for i in range(n)]
    for col in range(n):
        piv=next(i for i in range(col,n) if aug[i][col]!=0); aug[col],aug[piv]=aug[piv],aug[col]
        pv=aug[col][col]; aug[col]=[x/pv for x in aug[col]]
        for i in range(n):
            if i!=col and aug[i][col]!=0:
                f=aug[i][col]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[col])]
    return [aug[i][n] for i in range(n)]
def val(x,u): return F(1) if u==t1 else (F(0) if u==t0 else x[u])
t=time.time(); s=[0]*(2**c); flat=0
for pi in range(2**c):
    ch={v:succ[v][(pi>>i)&1] for i,v in enumerate(C)}; x=solve(ch); o=0
    for i,v in enumerate(C):
        a=(pi>>i)&1; cur=val(x,succ[v][a]); alt=val(x,succ[v][1-a])
        if alt==cur: flat+=1
        elif (alt>cur) == (kinds[v]=='max'): o|=1<<i
    s[pi]=o
print('profiles',2**c,'flat incidences',flat,'time',round(time.time()-t))
print('USO',is_uso(s,c),'acyclic',acyclic(s,c),'height',max_height(s,c),'HK',is_hk(s,c))
print('outmap',s)
