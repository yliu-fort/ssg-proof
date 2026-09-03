"""R_BR on G# from the harmonic normal form PRINTED in prop:auso-seven: exhaustive over
all 16 starts and over every Min best response at every round, both veto variants."""
from fractions import Fraction as F
import itertools
rows = {  # (c1..c6, t1) /128 ; index 0..5 = c1..c6
 0: [(6,3,88,1,0,0,4),(1,0,0,0,126,0,0)],
 1: [(0,0,14,113,0,0,0),(0,6,0,0,0,0,53)],
 2: [(0,0,0,127,0,0,0),(120,0,0,0,0,0,7)],
 3: [(0,0,0,0,0,120,7),(2,74,46,0,0,0,0)],
 4: [(0,0,0,0,13,0,64),(0,0,125,0,0,1,1)],
 5: [(0,127,0,0,0,0,0),(0,0,121,0,0,1,4)],
}
MAX=[0,1,2,3]; MIN=[4,5]; n=6
def solve(choice):  # choice: dict v->action
    M=[[F(int(v==j)) - F(rows[v][choice[v]][j],128) for j in range(n)] for v in range(n)]
    r=[F(rows[v][choice[v]][6],128) for v in range(n)]
    aug=[M[i]+[r[i]] for i in range(n)]
    for c in range(n):
        piv=next(i for i in range(c,n) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(n):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    return [aug[i][n] for i in range(n)]
def action_value(v,a,x): return sum(F(rows[v][a][j],128)*x[j] for j in range(n))+F(rows[v][a][6],128)
def choice_of(sig,tau): return {**{v:(sig>>i)&1 for i,v in enumerate(MAX)}, **{v:(tau>>i)&1 for i,v in enumerate(MIN)}}
prof={(s,t):solve(choice_of(s,t)) for s in range(16) for t in range(4)}
def val_sigma(s):
    vals=[prof[(s,t)] for t in range(4)]
    return [min(v[j] for v in vals) for j in range(n)]
def min_best_responses(s):
    vs=val_sigma(s); return [t for t in range(4) if prof[(s,t)]==vs]
def val_tau(t):
    vals=[prof[(s,t)] for s in range(16)]
    return [max(v[j] for v in vals) for j in range(n)]
# check the outmap
out=[]
for s in range(16):
    x=val_sigma(s); o=0
    for i,v in enumerate(MAX):
        a=(s>>i)&1
        if action_value(v,1-a,x)>action_value(v,a,x): o|=1<<i
        assert action_value(v,1-a,x)!=action_value(v,a,x)
    out.append(o)
print('outmap', out, 'matches paper:', out==[0,1,3,6,7,4,13,10,14,15,9,12,11,8,5,2])
def S_of(s):
    x=val_sigma(s); return {i for i,v in enumerate(MAX) if action_value(v,1-((s>>i)&1),x)>action_value(v,(s>>i)&1,x)}
def veto(s,S,t,strict):
    U=val_tau(t); C=set()
    for i in S:
        v=MAX[i]; a=(s>>i)&1
        alt=action_value(v,1-a,U); cur=action_value(v,a,U)
        if (alt>cur) if strict else (alt>=cur): C.add(i)
    return C
def runs(s,strict,path):
    """yield all complete runs (list of switch sets) from s"""
    S=S_of(s)
    if not S: yield path; return
    for t in min_best_responses(s):
        C=veto(s,S,t,strict)
        assert C, ('empty veto set', s, t, strict)
        s2=s
        for i in C: s2^=1<<i
        yield from runs(s2,strict,path+[sorted(C)])
for strict in (False,True):
    worst=(0,None,None)
    for s in range(16):
        for r in runs(s,strict,[]):
            if len(r)>worst[0]: worst=(len(r),s,r)
    print('strict' if strict else 'non-strict', 'worst rounds', worst[0], 'from start', format(worst[1],'04b'), '(c1..c4 bits)', 'sets', [[f'c{i+1}' for i in C] for C in worst[2]])
    # also: the number of distinct best responses per strategy
print('best responses per sigma:', [len(min_best_responses(s)) for s in range(16)])
# all-switches from the height-7 start
s=8; L=0
while S_of(s): 
    for i in S_of(s): s^=1<<i
    L+=1
print('all-switches from 8:', L)
