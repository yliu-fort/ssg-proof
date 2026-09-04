"""My own implementation of def:slack and of the transitive variant, written
from the DEFINITION in frontier.tex, not from any agent's code."""
import sys; sys.path.insert(0,'.')
from fractions import Fraction as F
from core import SSG

def agp(kind, a, b):      # ag^+ : max / min / mean
    return max(a,b) if kind=='max' else (min(a,b) if kind=='min' else (a+b)/2)
def agm(kind, a, b):      # ag^- : the dual
    return min(a,b) if kind=='max' else (max(a,b) if kind=='min' else (a+b)/2)

def slack(g, w, K, transitive=False, snapshot=None):
    n=g.n; T0,T1=g.T0,g.T1; V=list(range(n+2))
    def val(v): return F(1) if v==T1 else (F(0) if v==T0 else w[v])
    Z0={v for v in V if val(v)==0}; Z1={v for v in V if val(v)==1}
    kind={v:(g.kind[v] if v<n else 'sink') for v in V}
    succ={v:(g.succ[v] if v<n else None) for v in V}
    D={(x,y):F(1) for x in V for y in V}
    out=[]
    for k in range(1,K+1):
        Dn={}
        for x in V:
            for y in V:
                cands=[F(1)]
                if x in Z0: cands.append(F(0))
                if y in Z1: cands.append(F(0))
                if x in Z0 and y in Z1: cands.append(F(-1))
                if x==y: cands.append(F(0))
                if succ[y] is not None:
                    a,b=succ[y]; cands.append(agm(kind[y], D[(x,a)], D[(x,b)]))
                if succ[x] is not None:
                    a,b=succ[x]; cands.append(agp(kind[x], D[(a,y)], D[(b,y)]))
                if succ[x] is not None and succ[y] is not None and kind[x]==kind[y]:
                    x0,x1=succ[x]; y0,y1=succ[y]
                    if kind[x]=='avg':
                        cands.append((D[(x0,y0)]+D[(x1,y1)])/2)
                        cands.append((D[(x0,y1)]+D[(x1,y0)])/2)
                    else:
                        # both orders of composing (up) and (down); each is exact at D
                        cands.append(agm(kind[y], agp(kind[x],D[(x0,y0)],D[(x1,y0)]),
                                                  agp(kind[x],D[(x0,y1)],D[(x1,y1)])))
                        cands.append(agp(kind[x], agm(kind[y],D[(x0,y0)],D[(x0,y1)]),
                                                  agm(kind[y],D[(x1,y0)],D[(x1,y1)])))
                v=min(cands)
                Dn[(x,y)]=max(F(-1),min(F(1),v))
        if transitive:                       # min-plus all-pairs closure (Floyd-Warshall)
            for z in V:
                for x in V:
                    dxz=Dn[(x,z)]
                    for y in V:
                        s=dxz+Dn[(z,y)]
                        if s<Dn[(x,y)]: Dn[(x,y)]=max(F(-1),s)
        D=Dn
        if snapshot: out.append((k,{p:D[p] for p in snapshot}))
    return D,out

def Hm(m):
    L=2*m; n=L+2                      # c_1..c_L = 0..L-1 ; h = L ; v = L+1
    T0,T1=n,n+1
    kind=['avg']*L+['avg','max']
    succ=[None]*n
    for i in range(1,L):
        o = 0 if i<=m-1 else (T1 if i==m else T0)
        succ[i-1]=(o,i)
    succ[L-1]=(T0,T1)
    succ[L]=(T0,T1)
    succ[L+1]=(0,L)
    return SSG(kind,succ)
