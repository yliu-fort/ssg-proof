"""Q_16 (verify-r14 / round-14): parse the printed rows, run BSI (veto and strict) from the printed start, exact arithmetic."""
import re, itertools
from fractions import Fraction as F
src=open('../verify-r14/verify14.tex').read()
i=src.index(r'\label{bsr:prop-switches}'); seg=src[i:src.index(r'\end{array}',i)]
rows={}; kind={}
for line in seg.split('\n'):
    m=re.match(r'\s*c_\{(\d+)\}\\ \((\\max|\\min)\): & (.*?) & (.*?)\\\\', line)
    if not m: continue
    v=int(m.group(1)); kind[v]=m.group(2)[1:]
    def parse(s):
        d={}
        for t,mass in re.findall(r'(c_\{\d+\}|t_1)\\!:\\!(\d+)', s):
            key=int(re.search(r'\d+',t).group()) if t.startswith('c') else 't1'; d[key]=int(mass)
        return d
    rows[v]=[parse(m.group(3)),parse(m.group(4))]
assert len(rows)==16, len(rows)
C=sorted(rows); MX=[v for v in C if kind[v]=='max']; MN=[v for v in C if kind[v]=='min']
def solve(choice):
    n=16; idx={v:i for i,v in enumerate(C)}
    A=[[F(int(i==j)) for j in range(n)] for i in range(n)]; b=[F(0)]*n
    for v in C:
        r=rows[v][choice[v]]
        for k,mass in r.items():
            if k=='t1': b[idx[v]]+=F(mass,64)
            else: A[idx[v]][idx[k]]-=F(mass,64)
    aug=[A[i]+[b[i]] for i in range(n)]
    for c in range(n):
        piv=next(i for i in range(c,n) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(n):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    return {v:aug[idx[v]][n] for v in C}
def act(v,a,x): return sum(F(m,64)*(F(1) if k=='t1' else x[k]) for k,m in rows[v][a].items())
def val_sigma(sig):
    best=None
    for tb in itertools.product((0,1),repeat=8):
        x=solve({**sig,**dict(zip(MN,tb))}); vec=[x[v] for v in C]
        best=vec if best is None else [min(p,q) for p,q in zip(best,vec)]
    return dict(zip(C,best))
def val_tau(tau):
    best=None
    for sb in itertools.product((0,1),repeat=8):
        x=solve({**tau,**dict(zip(MX,sb))}); vec=[x[v] for v in C]
        best=vec if best is None else [max(p,q) for p,q in zip(best,vec)]
    return dict(zip(C,best))
def bsi(sig,tau,strict):
    log=[]; r=0
    while True:
        L=val_sigma(sig); U=val_tau(tau)
        S={v for v in MX if act(v,1-sig[v],L)>act(v,sig[v],L)}; Sm={u for u in MN if act(u,1-tau[u],U)<act(u,tau[u],U)}
        Cm={v for v in S if (act(v,1-sig[v],U)>act(v,sig[v],U) if strict else act(v,1-sig[v],U)>=act(v,sig[v],U))}
        Cn={u for u in Sm if (act(u,1-tau[u],L)<act(u,tau[u],L) if strict else act(u,1-tau[u],L)<=act(u,tau[u],L))}
        log.append((sorted(Cm),sorted(Cn)))
        if not Cm and not Cn: return r,log,L,U
        sig={**sig,**{v:1-sig[v] for v in Cm}}; tau={**tau,**{u:1-tau[u] for u in Cn}}; r+=1
sig0=dict(zip(MX,[0,0,1,1,0,0,1,0])); tau0=dict(zip(MN,[0,0,1,1,1,1,0,1]))
for strict in (False,True):
    r,log,L,U=bsi(sig0,tau0,strict)
    from collections import Counter
    cnt=Counter(v for Cm,Cn in log for v in Cm+Cn)
    print('strict' if strict else 'veto', 'rounds',r,'switch multiset',sorted(cnt.values(),reverse=True),'c10 switched',cnt.get(10,0),'halt L==U',all(L[v]==U[v] for v in C),'w*(c1)=',L[1])
    for t,(Cm,Cn) in enumerate(log): print('  t=%d Cmax=%s Cmin=%s'%(t,Cm,Cn))
