"""End-to-end check of the tw:modulator / tw:qp machinery on random stopping SSGs:
pick X = a feedback vertex set (so G[X:=theta] is acyclic -> backward induction), run the grid Tarski search
(tw:tarski) on the rounded cut map (tw:round), recover exactly by continued fractions (tw:recover), compare
with brute-force val (min over Min strategies of max over Max strategies... here: exact LP-free: iterate exact
positional pairs)."""
from fractions import Fraction as F
import random, itertools, math
random.seed(7)
def rand_game(n, a_frac=0.4):
    kinds=[]; succ=[]
    for v in range(n):
        r=random.random(); kinds.append('avg' if r<a_frac else ('max' if r<0.7 else 'min'))
    # successors: forward-biased random with back edges, sinks t0=n, t1=n+1
    for v in range(n):
        s=[]
        for _ in range(2):
            r=random.random()
            if r<0.25: s.append(n+random.randint(0,1))
            else: s.append(random.randrange(n))
        succ.append(tuple(s))
    return kinds,succ
def stopping(kinds,succ,n):
    U=set(range(n)); ch=True
    while ch:
        ch=False
        for v in list(U):
            inU=[u in U for u in succ[v]]
            if not (all(inU) if kinds[v]=='avg' else any(inU)): U.discard(v); ch=True
    return not U
def solve_pair(kinds,succ,n,choice,term):
    """exact value of the chain with controlled choices fixed; term: dict vertex->payoff for frozen vertices (terminals)."""
    idx=[v for v in range(n) if v not in term]; pos={v:i for i,v in enumerate(idx)}; m=len(idx)
    A=[[F(0)]*m for _ in range(m)]; b=[F(0)]*m
    def pay(u): return F(1) if u==n+1 else (F(0) if u==n else term.get(u))
    for v in idx:
        i=pos[v]; A[i][i]+=1
        tg=[(succ[v][choice[v]],F(1))] if kinds[v]!='avg' else [(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
        for u,p in tg:
            if u>=n or u in term: b[i]+=p*pay(u)
            else: A[i][pos[u]]-=p
    aug=[A[i]+[b[i]] for i in range(m)]
    for c in range(m):
        piv=next(i for i in range(c,m) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(m):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    return {v:aug[pos[v]][m] for v in idx}
def val_exact(kinds,succ,n,term):
    """value of the stopping game with frozen terminals: max over Max strategies of min over Min strategies (positional determinacy)."""
    MX=[v for v in range(n) if kinds[v]=='max' and v not in term]; MN=[v for v in range(n) if kinds[v]=='min' and v not in term]
    best=None
    for sb in itertools.product((0,1),repeat=len(MX)):
        worst=None
        for tb in itertools.product((0,1),repeat=len(MN)):
            ch={v:a for v,a in zip(MX,sb)}; ch.update({v:a for v,a in zip(MN,tb)})
            x=solve_pair(kinds,succ,n,ch,term); vec=[x[v] for v in sorted(x)]
            worst=vec if worst is None else [min(p,q) for p,q in zip(worst,vec)]
        best=worst if best is None else [max(p,q) for p,q in zip(best,worst)]
    return dict(zip(sorted(v for v in range(n) if v not in term),best))
def acyclic_solve(kinds,succ,n,term):
    """backward induction on an acyclic (after freezing) game."""
    memo={}
    def val(u):
        if u==n+1: return F(1)
        if u==n: return F(0)
        if u in term: return term[u]
        if u in memo: return memo[u]
        a,b=(val(succ[u][0]),val(succ[u][1]))
        r={'max':max(a,b),'min':min(a,b),'avg':(a+b)/2}[kinds[u]]; memo[u]=r; return r
    return {v:val(v) for v in range(n) if v not in term}
def fvs(kinds,succ,n):
    """greedy feedback vertex set of the successor digraph."""
    X=set()
    def has_cycle(X):
        color={}
        def dfs(u):
            if u>=n or u in X: return False
            if color.get(u)==1: return True
            if color.get(u)==2: return False
            color[u]=1
            for w in succ[u]:
                if dfs(w): return True
            color[u]=2; return False
        return any(dfs(v) for v in range(n))
    while has_cycle(X):
        # pick vertex on a cycle with max degree heuristic: try each
        for v in range(n):
            if v not in X:
                X.add(v)
                if not has_cycle(X) or True: break
    return X
def tarski(F_, d, M):
    """tw:tarski: F_ monotone self-map of {0..M-1}^d given as function on tuples; returns fixed point and #evaluations."""
    cnt=[0]
    def rec(lo,hi,dd,fixed):
        # solve on coordinates 0..dd-1 within box lo,hi (tuples length dd), with coordinates dd.. fixed
        if dd==0: return ()
        lo=list(lo); hi=list(hi)
        while True:
            m=(lo[dd-1]+hi[dd-1])//2
            def g(y): 
                return F_(tuple(y)+(m,)+fixed)[:dd-1]
            ystar=rec(tuple(lo[:dd-1]),tuple(hi[:dd-1]),dd-1,(m,)+fixed)
            x=tuple(ystar)+(m,); fx=F_(x+fixed); cnt[0]+=1
            fx=fx[:dd]
            if fx[dd-1]==m: return x
            if fx[dd-1]>m: lo=list(fx)
            else: hi=list(fx)
    x=rec(tuple([0]*d),tuple([M-1]*d),d,()); return x,cnt[0]
ok=0; tot=0; evals=[]
while tot<25:
    n=random.randint(6,9); kinds,succ=rand_game(n)
    if not stopping(kinds,succ,n): continue
    X=sorted(fvs(kinds,succ,n))
    if not X or len(X)>3: continue
    a=kinds.count('avg'); N=n+2; Delta=1; Q=Delta*2**a; eps=F(1,4*N*2**a*Q*Q); B=math.ceil(math.log2(1/eps)); M=2**B+1
    def Fmap(t):
        theta={x:F(t[i],2**B) for i,x in enumerate(X)}
        vals=acyclic_solve(kinds,succ,n,theta)
        def pay(u): return F(1) if u==n+1 else (F(0) if u==n else (theta[u] if u in theta else vals[u]))
        out=[]
        for x in X:
            p,q=pay(succ[x][0]),pay(succ[x][1])
            r={'max':max(p,q),'min':min(p,q),'avg':(p+q)/2}[kinds[x]]
            out.append(math.ceil(r*2**B))  # round up to grid
        return tuple(out)
    th,ev=tarski(Fmap,len(X),M)
    # recover
    from fractions import Fraction
    rec={}
    for i,x in enumerate(X):
        v=F(th[i],2**B); rec[x]=v.limit_denominator(Q)
    truth=val_exact(kinds,succ,n,{})
    good=all(rec[x]==truth[x] for x in X) and all(F(th[i],2**B)-truth[x]>=0 and F(th[i],2**B)-truth[x]<=N*2**a*eps for i,x in enumerate(X))
    ok+=good; tot+=1; evals.append(ev)
    if not good: print('MISMATCH', n, X, [(str(rec[x]),str(truth[x])) for x in X])
print(f'{ok}/{tot} games: grid Tarski search + rounding + continued-fraction recovery returned val|_X exactly; evaluations {min(evals)}..{max(evals)} (bound 2(B+2)^|X|)')
