"""Independent check of RD(n) (thm:readout) and SD(K) (prop:leapfrog): exact rationals, val_sigma as min over ALL Min strategies."""
from fractions import Fraction as Fr
import itertools, sys
def solve_chain(n, succ, prob, sinks):
    """values of a Markov chain: succ[v]=list of (w,p); sinks: dict v->payoff. Gaussian elimination."""
    idx={v:i for i,v in enumerate([v for v in succ if v not in sinks])}; N=len(idx)
    A=[[Fr(0)]*N for _ in range(N)]; b=[Fr(0)]*N
    for v,i in idx.items():
        A[i][i]+=1
        for w,p in succ[v]:
            if w in sinks: b[i]+=p*sinks[w]
            else: A[i][idx[w]]-=p
    aug=[A[i]+[b[i]] for i in range(N)]
    for c in range(N):
        piv=next(i for i in range(c,N) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(N):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    val={v:aug[i][N] for v,i in idx.items()}; val.update(sinks); return val
class Game:
    def __init__(s): s.typ={}; s.succ={}  # typ: 'max','min','avg', succ: (a,b) or list for avg with probs
    def add(s,v,t,a,b=None,pa=None):
        s.typ[v]=t; s.succ[v]=(a,b) if t!='avg' else [(a,pa),(b,1-pa)]
    def chain(s,choice):
        succ={}
        for v,t in s.typ.items():
            if t=='avg': succ[v]=s.succ[v]
            else: succ[v]=[(s.succ[v][choice[v]],Fr(1))]
        return succ
    def val_pair(s,sig,tau):
        ch={**sig,**tau}; return solve_chain(0,s.chain(ch),None,{'t0':Fr(0),'t1':Fr(1)})
    def mins(s): return [v for v,t in s.typ.items() if t=='min']
    def maxs(s): return [v for v,t in s.typ.items() if t=='max']
    def val_sigma(s,sig):
        best=None; bests=[]
        for bits in itertools.product([0,1],repeat=len(s.mins())):
            tau=dict(zip(s.mins(),bits)); v=s.val_pair(sig,tau)
            vec=[v[u] for u in s.typ]
            if best is None or vec<best: pass
            best=vec if best is None else [min(a,b) for a,b in zip(best,vec)]
        d=dict(zip(s.typ,best)); d.update({'t0':Fr(0),'t1':Fr(1)}); return d
    def val_tau(s,tau):
        best=None
        for bits in itertools.product([0,1],repeat=len(s.maxs())):
            sig=dict(zip(s.maxs(),bits)); v=s.val_pair(sig,tau); vec=[v[u] for u in s.typ]
            best=vec if best is None else [max(a,b) for a,b in zip(best,vec)]
        d=dict(zip(s.typ,best)); d.update({'t0':Fr(0),'t1':Fr(1)}); return d
    def best_responses(s,sig):
        L=s.val_sigma(sig); out=[]
        for bits in itertools.product([0,1],repeat=len(s.mins())):
            tau=dict(zip(s.mins(),bits)); v=s.val_pair(sig,tau)
            if all(v[u]==L[u] for u in s.typ): out.append(tau)
        return out
    def S(s,sig,L): return {v for v in s.maxs() if L[s.succ[v][1-sig[v]]]>L[s.succ[v][sig[v]]]}
    def Smin(s,tau,U): return {u for u in s.mins() if U[s.succ[u][1-tau[u]]]<U[s.succ[u][tau[u]]]}
    def C_max(s,sig,S,U,strict):
        return {v for v in S if (U[s.succ[v][1-sig[v]]]>U[s.succ[v][sig[v]]] if strict else U[s.succ[v][1-sig[v]]]>=U[s.succ[v][sig[v]]])}
    def C_min(s,tau,Sm,L,strict):
        return {u for u in Sm if (L[s.succ[u][1-tau[u]]]<L[s.succ[u][tau[u]]] if strict else L[s.succ[u][1-tau[u]]]<=L[s.succ[u][tau[u]]])}
    def allsw(s,sig):
        r=0
        while True:
            L=s.val_sigma(sig); S=s.S(sig,L)
            if not S: return r
            sig={**sig,**{v:1-sig[v] for v in S}}; r+=1
    def rbr_all(s,sig,strict):
        """set of round counts over all best-response choices"""
        L=s.val_sigma(sig); S=s.S(sig,L)
        if not S: return {0}
        res=set()
        for tau in s.best_responses(sig):
            U=s.val_tau(tau); C=s.C_max(sig,S,U,strict); assert C
            res|={1+x for x in s.rbr_all({**sig,**{v:1-sig[v] for v in C}},strict)}
        return res
    def bsi(s,sig,tau,strict,log=None):
        r=0
        while True:
            L=s.val_sigma(sig); U=s.val_tau(tau); S=s.S(sig,L); Sm=s.Smin(tau,U)
            C=s.C_max(sig,S,U,strict); Cm=s.C_min(tau,Sm,L,strict)
            if not C and not Cm: return r
            if log is not None: log.append((sorted(C),sorted(Cm)))
            sig={**sig,**{v:1-sig[v] for v in C}}; tau={**tau,**{u:1-tau[u] for u in Cm}}; r+=1
def dyadic_gadget(g,name,val,den_bits):
    """average chain giving exact dyadic value val (0<val<1) with den 2^den_bits: chain of fair coins."""
    # binary expansion b1..bd: vertex c_j -> (t1 if b_j else t0, c_{j+1}) with prob 1/2; last c_d -> (t1/t0 per b_d, t0)
    bits=[(val*2**j).__floor__()%2 for j in range(1,den_bits+1)]
    assert sum(Fr(b,2**j) for j,b in enumerate(bits,1))==val
    prev=None
    for j in range(den_bits,0,-1):
        v=f'{name}_{j}'; hi='t1' if bits[j-1] else 't0'
        g.add(v,'avg',hi, prev if prev else 't0', Fr(1,2)); prev=v
    return prev
def RD(n):
    g=Game(); g.add('H','avg','t0','t1',Fr(1,2))
    for j in range(1,n+1):
        th=dyadic_gadget(g,f'Th{j}',Fr(1,2)-Fr(1,4**j),2*j+1); bj=dyadic_gadget(g,f'b{j}',Fr(1,2)+Fr(1,4**j),2*j+1)
        aj='t0' if j==1 else f'a{j}'
        if j>1: g.add(aj,'avg',f'u{j-1}','H',Fr(1,2))
        g.add(f'v{j}','max',aj,bj); g.add(f'u{j}','min',f'v{j}',th)
    sig={f'v{j}':0 for j in range(1,n+1)}; tau={f'u{j}':0 for j in range(1,n+1)}
    return g,sig,tau
for n in range(1,6):
    g,sig,tau=RD(n)
    a=g.allsw(sig); rb_s=g.rbr_all(sig,True); rb_v=g.rbr_all(sig,False); log=[]; b_s=g.bsi(sig,tau,True); b_v=g.bsi(sig,tau,False,log)
    # worst all-switches over all starts
    worst=max(g.allsw({f'v{j}':bits[j-1] for j in range(1,n+1)}) for bits in itertools.product([0,1],repeat=n))
    print(f'RD({n}): allsw {a} (worst over starts {worst}) R_BR strict {rb_s} veto {rb_v} BSI strict {b_s} veto {b_v} log {log if n<=3 else "..."}')
