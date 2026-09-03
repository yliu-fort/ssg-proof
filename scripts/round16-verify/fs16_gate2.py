import random, itertools
from fractions import Fraction as F
exec(open('fs16_check.py').read().split('# ---- fs16:gate ----')[0])
def gate_value(hk,hs2,calls,exitsH,p,q):
    # enumerate case assignments: each call uses coin p (case A>=B) or coin q (case A<B); keep consistent ones
    sols=[]
    for cases in itertools.product((0,1),repeat=len(calls)):
        gk2=dict(hk); gs2=dict(hs2); bias={}
        for c,cs_ in zip(calls,cases):
            e1,e0=exitsH[c]; gk2[c]='coin'; gs2[c]=(e0,e1); bias[c]= p if cs_==0 else q
        if not is_stopping(gk2,gs2): continue
        val=value(gk2,gs2,bias)
        def w(u): return val[u] if u in val else (F(1) if u=='t1' else F(0))
        ok=True
        for c,cs_ in zip(calls,cases):
            e1,e0=exitsH[c]; A,B=w(e1),w(e0)
            if (cs_==0 and not A>=B) or (cs_==1 and not A<B): ok=False
        if ok: sols.append(val)
    return sols
random.seed(16); bad=0; done=0; qgtp=0
for t in range(60):
    gk,gs,gn=rand_game(random.randint(3,6),'g'); v0=gn[0]
    p=value(gk,gs)[v0]
    rk={v:('min' if k=='max' else 'max' if k=='min' else k) for v,k in gk.items()}
    q=value(rk,gs)[v0]
    if q>p: qgtp+=1
    hk,hs,hn=rand_game(random.randint(3,6),'h')
    ncalls=random.randint(1,2); calls=[f'c{i}' for i in range(ncalls)]
    exitsH={}
    for c in calls:
        pool=hn+['t0','t1']; exitsH[c]=(random.choice(pool),random.choice(pool))
    hs2=dict(hs)
    for c in calls:
        v=random.choice(hn); a=random.randrange(2); s=list(hs2[v]); s[a]=c; hs2[v]=tuple(s)
    ck=dict(hk); cs=dict(hs2)
    for c in calls:
        e1,e0=exitsH[c]
        for v in gn:
            ck[f'{c}_{v}']=gk[v]
            cs[f'{c}_{v}']=tuple((f'{c}_{u}' if u in gn else (e1 if u=='t1' else e0)) for u in gs[v])
        ck[c]='avg'; cs[c]=(f'{c}_{v0}',f'{c}_{v0}')
    if not is_stopping(ck,cs): continue
    valH=value(ck,cs)
    sols=gate_value(hk,hs2,calls,exitsH,p,q)
    done+=1
    if not sols: print('no consistent gate solution',t); bad+=1; continue
    for val in sols:
        if any(valH[v]!=val[v] for v in hn+calls):
            bad+=1; print('MISMATCH',t,{v:(valH[v],val[v]) for v in hn+calls if valH[v]!=val[v]}); break
print('gate (case-split operator): composed games',done,'mismatches',bad,'| instances with q>p:',qgtp)
