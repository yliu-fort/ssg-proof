# thm:two-exit: contract a part M with two exits (o1,o0) into one (p_e,q_e)-gate per entry; values outside M unchanged.
import random, itertools
from fractions import Fraction as F
exec(open('fs16_check.py').read().split('# ---- fs16:gate ----')[0])   # solve, is_stopping, value, rand_game
random.seed(21); done=0; bad=0; tried=0
while done<40 and tried<400:
    tried+=1
    # build G = context part H plus a part M whose edges land in M u {o1,o0}
    hk,hs,hn=rand_game(random.randint(3,5),'h')          # outside part
    mk,ms,mn=rand_game(random.randint(2,4),'m',exits=('t0','t1'))   # part M with sinks as placeholders
    o1,o0=random.sample(hn,2)
    kinds=dict(hk); succ=dict(hs)
    for v in mn:
        kinds[v]=mk[v]; succ[v]=tuple((o1 if u=='t1' else o0 if u=='t0' else u) for u in ms[v])
    # entries: rewire some H edges into M
    entries=random.sample(mn, random.randint(1,min(2,len(mn))))
    for e in entries:
        v=random.choice(hn); a=random.randrange(2); s_=list(succ[v]); s_[a]=e; succ[v]=tuple(s_)
    names=hn+mn
    if not is_stopping(kinds,succ): continue
    valG=value(kinds,succ)
    # G_M: M alone with o1->t1, o0->t0 ; p_e = val, q_e = val of role-reversed
    gk={v:mk[v] for v in mn}; gs={v:ms[v] for v in mn}
    if not is_stopping(gk,gs): continue
    pv=value(gk,gs); rk={v:('min' if k=='max' else 'max' if k=='min' else k) for v,k in gk.items()}; qv=value(rk,gs)
    # G/M: delete M, gate per entry
    ck={v:hk[v] for v in hn}; cs={}
    for v in hn:
        cs[v]=tuple((f'g_{u}' if u in mn else u) for u in succ[v])
    bias={}
    for e in entries:
        p,q=pv[e],qv[e]
        if not (0<p<1 and 0<q<1): break
        # gate = controlled vertex with two coin actions: implement by enumerating the case split exactly (as in fs16_gate2)
        ck[f'g_{e}']='gate'; cs[f'g_{e}']=(o1,o0); bias[f'g_{e}']=(p,q)
    else:
        gates=[g for g in ck if ck[g]=='gate']
        sols=[]
        for cases in itertools.product((0,1),repeat=len(gates)):
            k2=dict(ck); b2={}
            for g,c_ in zip(gates,cases):
                k2[g]='coin'; s1,s0=cs[g]; cs2=dict(cs); 
                b2[g]=bias[g][0] if c_==0 else bias[g][1]
            cs2={g:(cs[g][1],cs[g][0]) if k2[g]=='coin' else cs[g] for g in cs}   # coin: (e0,e1) with prob b of second = e1
            if not is_stopping(k2,cs2): continue
            val=value(k2,cs2,b2)
            def w(u): return val[u] if u in val else (F(1) if u=='t1' else F(0))
            ok=all((c_==0 and w(cs[g][0])>=w(cs[g][1])) or (c_==1 and w(cs[g][0])<w(cs[g][1])) for g,c_ in zip(gates,cases))
            if ok: sols.append(val)
        done+=1
        if not sols: bad+=1; print('no consistent gate solution'); continue
        for val in sols:
            if any(valG[v]!=val[v] for v in hn) or any(valG[e]!=val[f'g_{e}'] for e in entries):
                bad+=1; print('MISMATCH', {v:(str(valG[v]),str(val[v])) for v in hn if valG[v]!=val[v]}); break
print('two-exit contractions checked', done, 'mismatches', bad)
