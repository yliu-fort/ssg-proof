# bsc:w2: normal form with Vmax={v0,v1}, Vmin={u}; rows over (v0,v1,u | t1), denominator 32.
from fractions import Fraction as F
import itertools
rows={ 'v0':[((0,13*2,0),0),((0,1,23),5)],   # 13/16 v1 -> 26/32 ; (1/32 v1 + 23/32 u + 5/32 t1)
       'v1':[((0,0,29),0),((0,0,0),8)],      # 29/32 u ; 1/4 t1 = 8/32
       'u': [((30,0,0),0),((0,0,0),1)] }     # 15/16 v0 = 30/32 ; 1/32 t1
V=['v0','v1','u']; kinds={'v0':'max','v1':'max','u':'min'}; den=32
def solve(choice):
    n=3; M=[[F(0)]*(n+1) for _ in range(n)]
    for i,v in enumerate(V):
        co,b=rows[v][choice[v]]; M[i][i]+=1
        for j in range(n): M[i][j]-=F(co[j],den)
        M[i][n]=F(b,den)
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]; pv=M[c][c]; M[c]=[x/pv for x in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[x-f*y for x,y in zip(M[r],M[c])]
    return {v:M[i][n] for i,v in enumerate(V)}
def readout(v,act,val):
    co,b=rows[v][act]; return sum(F(co[j],den)*val[V[j]] for j in range(3))+F(b,den)
def val_sigma(sigma):   # min over tau (componentwise) and the set of best responses
    c=[solve({**sigma,'u':t}) for t in (0,1)]
    low={v:min(c[0][v],c[1][v]) for v in V}
    br=[t for t in (0,1) if all(c[t][v]==low[v] for v in V)]
    return low, br
def val_tau(tau):       # max over sigma
    c=[solve({'v0':a,'v1':b,'u':tau}) for a in (0,1) for b in (0,1)]
    return {v:max(x[v] for x in c) for v in V}
wstar=val_tau(0); wstar={v:min(wstar[v],val_tau(1)[v]) for v in V}
print('w* =',wstar)
def S(sigma,val): return [v for v in ('v0','v1') if readout(v,1-sigma[v],val)>readout(v,sigma[v],val)]
for variant in ('veto','strict'):
    for start in [(0,0),(0,1),(1,0),(1,1)]:
        sigma={'v0':start[0],'v1':start[1]}; rounds=0; trace=[start]
        while True:
            val,br=val_sigma(sigma); Ssig=S(sigma,val)
            if not Ssig: break
            results=set()
            for tau in br:
                U=val_tau(tau)
                if variant=='veto': sw=[v for v in Ssig if readout(v,1-sigma[v],U)>=readout(v,sigma[v],U)]
                else: sw=[v for v in Ssig if readout(v,1-sigma[v],U)>readout(v,sigma[v],U)]
                results.add(tuple(sw))
            assert len(results)==1, ('best-response dependence',results)
            sw=results.pop(); assert sw, 'R_BR empty but S nonempty?'
            for v in sw: sigma[v]=1-sigma[v]
            rounds+=1; trace.append((sigma['v0'],sigma['v1']))
            if rounds>10: break
        # all-switches
        s2={'v0':start[0],'v1':start[1]}; r2=0
        while True:
            val,_=val_sigma(s2); Ssig=S(s2,val)
            if not Ssig: break
            for v in Ssig: s2[v]=1-s2[v]
            r2+=1
        print(f'{variant} start {start}: R_BR {rounds} rounds {trace}; all-switches {r2}')
