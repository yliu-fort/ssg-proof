# Independent checks of fs16:gate, fs16:cross(a), fs16:mixmono on random stopping games (exact arithmetic).
from fractions import Fraction as F
import random, itertools
random.seed(16)
def solve(kinds, succ, choice, bias=None):
    # kinds: dict v->'max'|'min'|'avg'|'coin'; succ v->(a,b); choice for max/min; bias for coin (prob of succ[1])
    V=list(kinds); idx={v:i for i,v in enumerate(V)}; n=len(V)
    M=[[F(0)]*(n+1) for _ in range(n)]
    for v in V:
        i=idx[v]; M[i][i]+=1; k=kinds[v]
        if k=='avg': tg=[(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
        elif k=='coin': b=bias[v]; tg=[(succ[v][0],1-b),(succ[v][1],b)]
        else: tg=[(succ[v][choice[v]],F(1))]
        for u,c in tg:
            if u=='t1': M[i][n]+=c
            elif u=='t0': pass
            else: M[i][idx[u]]-=c
    for c in range(n):
        p=next((r for r in range(c,n) if M[r][c]!=0),None)
        if p is None: return None
        M[c],M[p]=M[p],M[c]; pv=M[c][c]; M[c]=[a/pv for a in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    return {v:M[idx[v]][n] for v in V}
def is_stopping(kinds,succ):
    # every positional pair reaches a sink a.s. <=> no trap (lem:trapchar): largest set U of non-sinks with avg both succ in U, controlled some succ in U
    U=set(kinds)
    changed=True
    while changed:
        changed=False
        for v in list(U):
            s=succ[v]; k=kinds[v]
            inU=[u in U for u in s]
            ok = all(inU) if k in ('avg','coin') else any(inU)
            if not ok: U.discard(v); changed=True
    return len(U)==0
def value(kinds,succ,bias=None):
    maxs=[v for v in kinds if kinds[v]=='max']; mins=[v for v in kinds if kinds[v]=='min']
    best=None; bestsig=None
    for sb in itertools.product((0,1),repeat=len(maxs)):
        sigma=dict(zip(maxs,sb)); worst=None
        for tb in itertools.product((0,1),repeat=len(mins)):
            ch=dict(sigma); ch.update(zip(mins,tb)); val=solve(kinds,succ,ch,bias)
            worst = val if worst is None else {v:min(worst[v],val[v]) for v in val}
        if best is None: best=worst; bestsig=sigma
        else:
            best={v:max(best[v],worst[v]) for v in worst}
    return best
def rand_game(n, prefix, exits=('t0','t1'), kindset=('max','min','avg','avg')):
    names=[f'{prefix}{i}' for i in range(n)]
    while True:
        kinds={v:random.choice(kindset) for v in names}
        succ={}
        for v in names:
            pool=names+list(exits)
            succ[v]=(random.choice(pool),random.choice(pool))
        if is_stopping(kinds,succ): return kinds,succ,names
# ---- fs16:gate ----
def gate_check(trials=25):
    bad=0
    for t in range(trials):
        gk,gs,gn=rand_game(random.randint(3,6),'g'); v0=gn[0]
        p=value(gk,gs)[v0]
        rk={v:('min' if k=='max' else 'max' if k=='min' else k) for v,k in gk.items()}
        q=value(rk,gs)[v0]
        # context H with call vertices c0 (and maybe c1): exits e1,e0 -> vertices of H
        hk,hs,hn=rand_game(random.randint(3,6),'h')
        ncalls=random.randint(1,2)
        calls=[f'c{i}' for i in range(ncalls)]
        exitsH={}
        for c in calls:
            pool=hn+['t0','t1']
            exitsH[c]=(random.choice(pool),random.choice(pool))  # (e1,e0)
        # attach calls into H: rewire some H edges to calls
        hs2=dict(hs)
        for c in calls:
            v=random.choice(hn); a=random.randrange(2); s=list(hs2[v]); s[a]=c; hs2[v]=tuple(s)
        # composed game: copy of G per call
        ck=dict(hk); cs=dict(hs2)
        for c in calls:
            e1,e0=exitsH[c]
            for v in gn:
                ck[f'{c}_{v}']=gk[v]
                cs[f'{c}_{v}']=tuple((f'{c}_{u}' if u in gn else (e1 if u=='t1' else e0)) for u in gs[v])
            ck[c]='avg'; cs[c]=(f'{c}_{v0}',f'{c}_{v0}')   # call = enter the copy
        if not is_stopping(ck,cs): continue
        valH=value(ck,cs)
        # gate game: call c becomes a Max vertex choosing between coin(p) and coin(q) over (e0,e1)
        gk2=dict(hk); gs2=dict(hs2); bias={}
        for c in calls:
            e1,e0=exitsH[c]
            gk2[c]='max'; gs2[c]=(f'{c}_p',f'{c}_q')
            gk2[f'{c}_p']='coin'; gs2[f'{c}_p']=(e0,e1); bias[f'{c}_p']=p
            gk2[f'{c}_q']='coin'; gs2[f'{c}_q']=(e0,e1); bias[f'{c}_q']=q
        if not is_stopping(gk2,gs2): continue
        valG=value(gk2,gs2,bias)
        for v in hn+calls:
            if valH[v]!=valG[v]:
                bad+=1; print('GATE MISMATCH',t,v,valH[v],valG[v]); break
    print('fs16:gate: trials',trials,'mismatches',bad)
# ---- fs16:cross(a): sum_{v avg} N_v Delta_v^2 = 4 w(1-w) under an optimal pair, N_v expected visits from v0 ----
def cross_check(trials=40):
    bad=0
    for t in range(trials):
        gk,gs,gn=rand_game(random.randint(4,7),'g'); v0=gn[0]
        W=value(gk,gs)
        # optimal pair: sigma greedy for W at max, tau greedy at min (in a stopping game greedy strategies are optimal)
        ch={}
        for v in gn:
            if gk[v] in ('max','min'):
                a,b=gs[v]; wa=W.get(a,F(1) if a=='t1' else F(0)); wb=W.get(b,F(1) if b=='t1' else F(0))
                ch[v]=0 if (wa>=wb if gk[v]=='max' else wa<=wb) else 1
        # expected visits N_v from v0: solve N = e_{v0} + N P  (P transition among non-sinks)
        V=gn; idx={v:i for i,v in enumerate(V)}; n=len(V)
        P=[[F(0)]*n for _ in range(n)]
        for v in V:
            if gk[v]=='avg': tg=[(gs[v][0],F(1,2)),(gs[v][1],F(1,2))]
            else: tg=[(gs[v][ch[v]],F(1))]
            for u,c in tg:
                if u in idx: P[idx[v]][idx[u]]+=c
        # solve (I - P^T) N = e
        M=[[F(0)]*(n+1) for _ in range(n)]
        for i in range(n):
            M[i][i]+=1
            for j in range(n): M[i][j]-=P[j][i]
        M[idx[v0]][n]=F(1)
        for c in range(n):
            p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]; pv=M[c][c]; M[c]=[a/pv for a in M[c]]
            for r in range(n):
                if r!=c and M[r][c]!=0:
                    f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
        N={v:M[idx[v]][n] for v in V}
        def w(u): return W[u] if u in W else (F(1) if u=='t1' else F(0))
        lhs=sum(N[v]*(w(gs[v][1])-w(gs[v][0]))**2 for v in V if gk[v]=='avg')
        rhs=4*W[v0]*(1-W[v0])
        if lhs!=rhs: bad+=1; print('CROSS MISMATCH',t,lhs,rhs)
    print('fs16:cross(a): trials',trials,'mismatches',bad)
# ---- fs16:mixmono: V(y) monotone in each Min coordinate ----
def mixmono_check(trials=30):
    bad=0; tested=0
    for t in range(trials):
        gk,gs,gn=rand_game(random.randint(4,7),'g'); v0=gn[0]
        mins=[v for v in gn if gk[v]=='min']
        if not mins: continue
        tested+=1
        for j in mins:
            others=[u for u in mins if u!=j]
            ob={u:random.choice([F(0),F(1,3),F(1,2),F(1)]) for u in others}
            prev=None; direction=None
            for y in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
                kk=dict(gk); bias=dict(ob); bias[j]=y
                for u in mins: kk[u]='coin'
                val=value(kk,gs,bias)[v0]
                if prev is not None:
                    d = (val>prev)-(val<prev)
                    if d!=0:
                        if direction is None: direction=d
                        elif d!=direction: bad+=1; print('MONO FAIL',t,j); break
                prev=val
    print('fs16:mixmono: games with Min',tested,'violations',bad)
gate_check(); cross_check(); mixmono_check()
