import sys
sys.setrecursionlimit(10000)

# f(m): max L such that there is a sequence sigma_0..sigma_L in {0,1}^m,
# S_t = sigma_t xor sigma_{t+1} nonempty, with
# (B) for all t<t'<=L : (sigma_t xor sigma_t') & S_t != 0        [cor:no-return]
# (F) for all t<t'<=L-1: (sigma_t xor sigma_t') not subset of S_t' [cor:law-b]
#
# Reformulation used here (equivalent, verified below by a naive checker):
#  points sigma_t are the walk; C_s = {x : x&S_s == sigma_s&S_s} forbidden for all later points
#  F_t  = {x : (x xor sigma_t) subset S_t} must contain no earlier point.

def f_dfs(m, verbose=False):
    full = (1<<m) - 1
    npts = 1<<m
    best = [0]
    bestseq = [None]
    forbidden = bytearray(npts)   # count of covering cubes
    prev = []                     # previous points sigma_0..sigma_{t-1}
    Ss = []

    def cube_pts(s, S):
        # all x with x&S == s&S
        base = s & S
        free = full & ~S
        # enumerate subsets of free
        sub = free
        out = [base]
        # standard subset enumeration
        x = free
        while x:
            out.append(base | x)
            x = (x-1) & free
        return out

    def rec(p, t):
        if t > best[0]:
            best[0] = t
            bestseq[0] = (list(prev)+[p], list(Ss))
        # try each nonempty S
        for S in range(1, npts):
            q = p ^ S
            if forbidden[q]:
                continue
            # (F): no earlier point sigma_s (s<t) with (sigma_s ^ p) subset of S
            ok = True
            for sp in prev:
                d = sp ^ p
                if d & ~S == 0:
                    ok = False; break
            if not ok:
                continue
            pts = cube_pts(p, S)
            for x in pts: forbidden[x]+=1
            prev.append(p); Ss.append(S)
            rec(q, t+1)
            prev.pop(); Ss.pop()
            for x in pts: forbidden[x]-=1
    rec(0,0)
    return best[0], bestseq[0]

def check_naive(sigmas, Ss, m):
    L = len(sigmas)-1
    assert len(Ss)==L
    for t in range(L):
        assert sigmas[t]^sigmas[t+1]==Ss[t] and Ss[t]!=0
    for t in range(L):
        for tp in range(t+1, L+1):
            if (sigmas[t]^sigmas[tp]) & Ss[t] == 0: return False,("B",t,tp)
    for t in range(L):
        for tp in range(t+1, L):
            d = sigmas[t]^sigmas[tp]
            if d & ~Ss[tp] == 0: return False,("F",t,tp)
    return True,None

for m in range(1,6):
    L,(sig,Ss) = f_dfs(m)
    ok,why = check_naive(sig,Ss,m)
    print("m=%d f=%d  ok=%s  sigmas=%s  S=%s" % (m,L,ok,[format(s,'0%db'%m) for s in sig],[format(s,"0%db"%m) for s in Ss]), flush=True)
