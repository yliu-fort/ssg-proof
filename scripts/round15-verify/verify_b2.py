"""Independent verification of the gadget route's B^2 realisation from the GAME file:
stopping (trap test), profile values by exact elimination for all 32 x 2 profiles, val_sigma = min over tau,
outmap, ties, USO, acyclic, height, walk from 12, comparison with B^2."""
import sys, json, itertools, time; sys.path.insert(0,'../solo')
from fractions import Fraction as F
from auso import is_uso, is_acyclic, ba_heights, ba_trace
from my_D import is_holt_klee
d=json.load(open('../blowup/B2_small_GAME.json'))
kinds=d['kinds']; succ=[tuple(s) for s in d['succ']]; n=len(kinds); t0,t1=n,n+1
MX=[v for v in range(n) if kinds[v]=='max']; MN=[v for v in range(n) if kinds[v]=='min']
print('N', n+2, 'max', MX, 'min', MN, 'avg', kinds.count('avg'), 'outdeg2', all(len(s)==2 for s in succ))
U=set(range(n)); ch=True
while ch:
    ch=False
    for v in list(U):
        inU=[u in U for u in succ[v]]
        if not (all(inU) if kinds[v]=='avg' else any(inU)): U.discard(v); ch=True
print('stopping (greatest trap empty):', not U)
def solve(choice):
    M=[[F(0)]*n for _ in range(n)]; q=[F(0)]*n
    for v in range(n):
        tg=[(choice[v],F(1))] if kinds[v] in ('max','min') else [(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
        for u,p in tg:
            if u==t1: q[v]+=p
            elif u<n: M[v][u]+=p
    aug=[[(F(1) if i==j else F(0))-M[i][j] for j in range(n)]+[q[i]] for i in range(n)]
    for c in range(n):
        piv=next(i for i in range(c,n) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(n):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    return [aug[i][n] for i in range(n)]
def val(x,u): return F(1) if u==t1 else (F(0) if u==t0 else x[u])
t=time.time(); out=[]; ties=0; vals={}
for s in range(1<<len(MX)):
    best=None
    for tc in itertools.product((0,1),repeat=len(MN)):
        ch={v:succ[v][(s>>i)&1] for i,v in enumerate(MX)}; ch.update({v:succ[v][a] for v,a in zip(MN,tc)})
        x=solve(ch); best=x if best is None else [min(a,b) for a,b in zip(best,x)]
    vals[s]=best; o=0
    for i,v in enumerate(MX):
        a=(s>>i)&1; cur=val(best,succ[v][a]); alt=val(best,succ[v][1-a])
        if alt>cur: o|=1<<i
        elif alt==cur: ties+=1
    out.append(o)
print('time %.0fs'%(time.time()-t))
B2=[7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
print('outmap', out); print('== B^2:', out==B2, '| ties', ties, '| USO', is_uso(out,5), 'acyclic', is_acyclic(out,5), 'height', max(ba_heights(out,5)), 'HK', is_holt_klee(out,5)[0])
w=ba_trace(out,12); print('walk from 12:', w, 'length', len(w)-1)
# values strictly increase along the run at every non-sink
ok=all(all(vals[b][v]>=vals[a][v] for v in range(n)) and any(vals[b][v]>vals[a][v] for v in range(n)) for a,b in zip(w,w[1:]))
print('values nondecreasing with strict increase somewhere at every step:', ok)
