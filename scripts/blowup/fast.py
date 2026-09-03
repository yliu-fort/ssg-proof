"""Exact val_sigma / val^tau by opponent policy iteration.  Sound ONLY on
stopping games (asserted).  Cross-checked against brute force in t13.py."""
import sys, itertools
from fractions import Fraction as F
sys.path.insert(0,'.')
import mycore as M

def other(g,v,cur):
    a,b=g.succ[v]; return b if cur==a else a

def val_sigma_fast(g, sigma):
    assert M.is_stopping(g)
    MN=g.of('min'); tau={u:g.succ[u][0] for u in MN}
    while True:
        v=M.profile_value(g,sigma,tau)
        sw=[u for u in MN if v[other(g,u,tau[u])] < v[tau[u]]]
        if not sw: return v, tau
        for u in sw: tau[u]=other(g,u,tau[u])

def val_tau_fast(g, tau):
    assert M.is_stopping(g)
    MX=g.of('max'); sigma={v:g.succ[v][0] for v in MX}
    while True:
        v=M.profile_value(g,sigma,tau)
        sw=[x for x in MX if v[other(g,x,sigma[x])] > v[sigma[x]]]
        if not sw: return v, sigma
        for x in sw: sigma[x]=other(g,x,sigma[x])
