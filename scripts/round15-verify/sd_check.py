"""SD(K) as a ONE-PLAYER game (Min deleted: u_j -> t0 in the mixtures): all-switches switches v exactly K times?  Also the two-player self-dual version's BSI count."""
from fractions import Fraction as Fr
import sys
sys.argv=['x']; exec(open('rd_sd_check.py').read().split('def RD(n)')[0])  # reuse Game, dyadic_gadget
def mixture(g,name,dist,bits):
    """average tree realising a dyadic distribution dist: {target: prob} with denominators 2^bits, via lem:dyadic-row (collapsed KY tree). Returns entry vertex name."""
    targets=list(dist); D=2**bits
    K=[0]; 
    for t in targets: K.append(K[-1]+int(dist[t]*D)); 
    assert K[-1]==D, (K,dist)
    leafof=lambda i: targets[max(j for j in range(len(targets)) if K[j]<=i)]
    cnt=[0]
    def build(lo,hi,depth):  # leaves lo..hi-1
        if leafof(lo)==leafof(hi-1): return leafof(lo)
        mid=(lo+hi)//2; a=build(lo,mid,depth+1); b=build(mid,hi,depth+1)
        cnt[0]+=1; v=f'{name}_n{cnt[0]}'; g.add(v,'avg',a,b,Fr(1,2)); return v
    return build(0,D,0)
def SD(K,oneplayer):
    eta=Fr(1,2**(K+2)); gam={j:((-1)**(j+1))*2**(j+1)*eta for j in range(1,K)}; gam[K]=Fr(0)
    Delta=-eta-sum(gam[j]*(1-Fr(1,2**j)) for j in range(1,K+1))
    al={j:max(gam[j],0) for j in gam}; be={j:max(-gam[j],0) for j in gam}
    S=sum(al[j]+be[j] for j in gam); ap=(1-S+Delta)/2; aq=(1-S-Delta)/2
    assert ap>=0 and aq>=0
    g=Game()
    for j in range(1,K+1):
        g.add(f'k{j}','avg','t1', 't0' if j==1 else f'k{j-1}', Fr(1,2))
        g.add(f'h{j}','avg','t0', 't1' if j==1 else f'h{j-1}', Fr(1,2))
        g.add(f'x{j}','max', 't1' if j==1 else f'x{j-1}', f'k{j}')
        if not oneplayer: g.add(f'u{j}','min', 't0' if j==1 else f'u{j-1}', f'h{j}')
    U=lambda j: 't0' if oneplayer else f'u{j}'
    dp={}; dq={}
    for j in range(1,K+1):
        if al[j]: dp[f'x{j}']=al[j]; dq[U(j)]=dq.get(U(j),0)+al[j]
        if be[j]: dp[U(j)]=dp.get(U(j),0)+be[j]; dq[f'x{j}']=be[j]
    dp['t1']=dp.get('t1',0)+ap; dp['t0']=dp.get('t0',0)+aq; dq['t1']=dq.get('t1',0)+aq; dq['t0']=dq.get('t0',0)+ap
    bits=K+3
    p=mixture(g,'p',dp,bits); q=mixture(g,'q',dq,bits)
    g.add('v','max',p,q)
    if not oneplayer: g.add("v'",'min',q,p)
    sig={f'x{j}':1 for j in range(1,K+1)}; sig['v']=0   # x_j -> k_j is action 1
    tau={f'u{j}':1 for j in range(1,K+1)}; tau["v'"]=0  # u_j -> h_j action 1 ; v' -> q action 0
    return g,sig,tau
for K in range(2,7):
    g,sig,_=SD(K,True); N=len(g.typ)+2
    # all-switches run with switch sets
    r=0; sw=[]; s=dict(sig)
    while True:
        L=g.val_sigma(s); S=g.S(s,L)
        if not S: break
        sw.append(sorted(S)); s={**s,**{v:1-s[v] for v in S}}; r+=1
    print(f'SD({K}) one-player: N={N} rounds={r} v switched {sum("v" in x for x in sw)} times; switch sets {sw}')
for K in range(2,5):
    g,sig,tau=SD(K,False); N=len(g.typ)+2; log=[]
    b=g.bsi(sig,tau,False,log); print(f'SD({K}) two-player: N={N} BSI veto rounds={b} log={log}')
