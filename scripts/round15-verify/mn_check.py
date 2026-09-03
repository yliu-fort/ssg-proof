"""M_n of the treewidth route: stopping, reachable from h, val(h)=1/2+2^{-(n+1)}, mu_max=1 (freezing h leaves no cycle through a Max vertex)."""
from fractions import Fraction as F
import itertools, sys
sys.argv=['x']; exec(open('tw_check.py').read().split('ok=0; tot=0')[0])
def Mn(n):
    names={}; kinds=[]; succ=[]
    def add(nm,k): names[nm]=len(kinds); kinds.append(k); succ.append(None)
    add('h','max')
    for i in range(1,n+1): add(f'x{i}','max'); add(f'b{i}','avg'); add(f'y{i}','min')
    for j in range(1,2*n+1): add(f'c{j}','avg')
    N=len(kinds); t0,t1=N,N+1
    def S(nm): return names[nm] if nm in names else (t0 if nm=='t0' else t1)
    succ[names['h']]=(S('x1'),S(f'c{2*n}'))
    for i in range(1,n+1):
        succ[names[f'x{i}']]=(S(f'b{i}'),S(f'c{n+i}')); succ[names[f'b{i}']]=(S(f'y{i}'),S('c1'))
        succ[names[f'y{i}']]=(S(f'x{i+1}') if i<n else S('h'), S(f'b{i}'))
    for j in range(1,2*n+1):
        o='c1' if j<n else ('t1' if j==n else 't0')
        succ[names[f'c{j}']]=(S(o),S(f'c{j+1}')) if j<2*n else (t0,t1)
    return kinds,[tuple(s) for s in succ],N,names
for n in range(3,6):
    kinds,succ,N,names=Mn(n)
    st=stopping(kinds,succ,N)
    # reachability from h
    seen={names['h']}; st_=[names['h']]
    while st_:
        u=st_.pop()
        for w in succ[u]:
            if w<N and w not in seen: seen.add(w); st_.append(w)
    # max-cycle after freezing h: any cycle through a Max vertex avoiding h?
    def cycle_through_max_avoiding(X):
        color={}
        def dfs(u,path):
            if u>=N or u in X: return False
            if u in path: return any(kinds[v]=='max' for v in path[path.index(u):])
            if color.get(u)==2: return False
            r=any(dfs(w,path+[u]) for w in succ[u]); color[u]=2; return r
        return any(dfs(v,[]) for v in range(N))
    v=val_exact(kinds,succ,N,{})
    print(f'M_{n}: N={N+2} (5n+3={5*n+3}) stopping={st} reachable={len(seen)==N} val(h)={v[names["h"]]} expected {F(1,2)+F(1,2**(n+1))} '
          f'max-cycle without h: {cycle_through_max_avoiding({names["h"]})}; with nothing frozen: {cycle_through_max_avoiding(set())}')
