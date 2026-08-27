"""Two-stage search: cheap Q filter, then the Q_1 lift."""
import random, sys, time
from fractions import Fraction as F
from lp_exact import Game, check_feasible
from transport import sep, level_subsets, lift_point, build_lift, q_rows

def rnd(nmax,nmin,navg,rng):
    n=nmax+nmin+navg
    kinds=['max']*nmax+['min']*nmin+['avg']*navg
    rng.shuffle(kinds)
    succ=[(rng.randrange(n+2),rng.randrange(n+2)) for _ in range(n)]
    return Game(kinds,succ)

def undecided(g, subs):
    out={}
    for v in g.ctrl:
        a,b=g.succ[v]
        s0=sep(g,a,b,subsets=subs)[0]
        if s0<=0: return None
        s1=sep(g,b,a,subsets=subs)[0]
        if s1<=0: return None
        out[v]=(s0,s1)
    return out

if __name__=='__main__':
    nmax,nmin,navg,trials,seed=(int(x) for x in sys.argv[1:6])
    rng=random.Random(seed); t0=time.time()
    nstop=0; nQstall=0; nQ1stall=0
    for it in range(trials):
        g=rnd(nmax,nmin,navg,rng)
        if not g.is_stopping(): continue
        nstop+=1
        w=g.value()
        if not any(w[g.succ[v][0]]!=w[g.succ[v][1]] for v in g.ctrl): continue
        # stage 1: Q
        check_feasible(q_rows(g), w, "Q")
        if undecided(g,None) is None: continue
        nQstall+=1
        # stage 2: Q_1
        subs=level_subsets(g,1)
        rows=build_lift(g,subs)[1]
        check_feasible(rows, lift_point(g,w,subs), "lift")
        d=undecided(g,subs)
        if d is not None:
            nQ1stall+=1
            print("Q1-STALL",g.kinds,g.succ); print("  w*=",w); print("  sep=",d)
            sys.stdout.flush()
    print(f"# {trials} trials seed={seed} kinds=({nmax},{nmin},{navg}): stopping={nstop} Qstall={nQstall} Q1stall={nQ1stall} {time.time()-t0:.0f}s")
