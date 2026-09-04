from fractions import Fraction as F
from mycore import G

def G8():
    # prop:simorder-stalls: kinds (avg,avg,avg,avg,avg,max)
    # 0->(0,t1) 1->(0,t0) 2->(t0,4) 3->(0,2) 4->(3,2) 5->(4,1); t0=6,t1=7
    return G(['avg','avg','avg','avg','avg','max'],
             [(0,7),(0,6),(6,4),(0,2),(3,2),(4,1)])

def S():
    # prop:transport-stalls: v=0 max; a=1,b=2,b1=3,b2=4 avg; t0=5,t1=6
    # v->(a,b) a->(t1,t0) b->(v,b1) b1->(b2,t0) b2->(t1,t0)
    return G(['max','avg','avg','avg','avg'],
             [(1,2),(6,5),(0,3),(4,5),(6,5)])

def S_r(r):
    # thm:transport-barrier: v=0 max; a=1; b_0..b_{r+1} = 2..r+3 avg
    n = r+4; T0, T1 = n, n+1
    kinds = ['max','avg'] + ['avg']*(r+2)
    succ = [None]*n
    b = lambda i: 2+i
    succ[0] = (1, b(0))
    succ[1] = (T1, T0)
    for i in range(r):
        succ[b(i)] = (0, b(i+1))
    succ[b(r)]   = (b(r+1), T0)
    succ[b(r+1)] = (T1, T0)
    return G(kinds, succ)

def H_m(m):
    # cor:slack-stalls: G_m of thm:vi-lower (2m avg vertices c_1..c_2m) plus
    # h -> (t0,t1) and a Max vertex v -> (c_1, h).
    # G_m (thm:vi-lower) family: verified separately below by its stated value.
    # c_1..c_{2m}: indices 0..2m-1 ; h = 2m ; v = 2m+1 ; t0 = 2m+2, t1 = 2m+3
    n = 2*m+2; T0, T1 = n, n+1
    kinds = ['avg']*(2*m) + ['avg','max']
    succ = [None]*n
    # the player-free chain of thm:vi-lower with val(c_1) = 1/2 + 2^-(m+1)
    for i in range(2*m):
        succ[i] = None
    # c_i -> (c_{i+1}, c_{i-1}) style chain is the natural birth-death chain;
    # the exact wiring is pinned below by requiring w*(c_1) = 1/2 + 2^-(m+1).
    return None

def Gm(m):
    """thm:vi-lower: c_1..c_{2m} all average.  c_i -> (o_i, c_{i+1}),
    o_i = c_1 (i<m), t_1 (i=m), t_0 (m<i<=2m-1); c_{2m} -> (t0,t1)."""
    L = 2*m; T0, T1 = L, L+1
    kinds = ['avg']*L; succ = [None]*L
    for i in range(1, L):                       # 1-based c_i, i = 1..L-1
        o = 0 if i <= m-1 else (T1 if i == m else T0)
        succ[i-1] = (o, i)                      # c_{i+1} has 0-based index i
    succ[L-1] = (T0, T1)
    return G(kinds, succ)

def H_m(m):
    """cor:slack-stalls: G_m plus h -> (t0,t1) and a Max v -> (c_1, h)."""
    L = 2*m
    h = L; v = L+1; n = L+2; T0, T1 = n, n+1
    kinds = ['avg']*L + ['avg', 'max']
    succ = [None]*n
    for i in range(1, L):
        o = 0 if i <= m-1 else (T1 if i == m else T0)
        succ[i-1] = (o, i)
    succ[L-1] = (T0, T1)
    succ[h] = (T0, T1)
    succ[v] = (0, h)
    return G(kinds, succ)

def A0():
    """prop:trans-stall: a NON-stopping game where the transitive slack calculus
    stalls for ever.  a avg ->(t0,t1); p Max ->(a,p); q avg ->(a,t1);
    u Max ->(p,q).   Indices a=0,p=1,q=2,u=3; t0=4,t1=5."""
    return G(['avg','max','avg','max'], [(4,5),(0,1),(0,5),(1,2)])
