"""g(m): greatest L of a switch sequence obeying no-return, law-b, law-u (deg:prop-g). Canonical: sigma_0=0, S_0 initial segment."""
import sys
def g(m):
    best=[0]; full=(1<<m)-1
    def ok_S(sig,S,t,sigs,Ss):
        # law-b: (sigma_u xor sigma_t) not subset of S_t ; law-u: (S_u ^ S_t) & (sigma_u ^ sigma_t) != 0  for all u<t
        for u in range(t):
            d=sigs[u]^sig
            if d & ~S == 0: return False
            if (Ss[u]^S) & d == 0: return False
        return True
    def ok_next(nxt,t,sigs,Ss):
        # no-return: (sigma_u xor sigma_{t+1}) & S_u != 0 for all u<=t
        for u in range(t+1):
            if (sigs[u]^nxt) & Ss[u]==0: return False
        return True
    sys.setrecursionlimit(10000)
    def dfs(sigs,Ss):
        t=len(Ss); sig=sigs[t]
        if t>best[0]: best[0]=t
        for S in range(1,full+1):
            if t==0 and (S & (S+1))!=0: continue  # initial segment
            if not ok_S(sig,S,t,sigs,Ss): continue
            nxt=sig^S
            if not ok_next(nxt,t,sigs,Ss+[S]): continue
            dfs(sigs+[nxt],Ss+[S])
    dfs([0],[]); return best[0]
for m in range(1,6):
    print('g(%d)='%m, g(m), flush=True)
