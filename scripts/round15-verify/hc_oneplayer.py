"""hcube:oneplayer: verify the m=5 and m=6 nondegenerate one-player normal forms (rows over Vmax; last entry q), D=4096."""
import sys; sys.path.insert(0,'../solo')
from fractions import Fraction as F
from auso import is_uso, is_acyclic, ba_heights, ba_trace
from my_D import is_holt_klee
def check(rows, m, start, D=4096):
    P=[[[F(rows[2*v+a][j],D) for j in range(m)] for a in (0,1)] for v in range(m)]
    Q=[[F(rows[2*v+a][m],D) for a in (0,1)] for v in range(m)]
    leak=all(sum(rows[2*v+a][:m])+rows[2*v+a][m] < D for v in range(m) for a in (0,1))
    def solve(sigma):
        M=[[(F(1) if v==j else F(0))-P[v][sigma>>v&1][j] for j in range(m)] for v in range(m)]; r=[Q[v][sigma>>v&1] for v in range(m)]
        aug=[M[i]+[r[i]] for i in range(m)]
        for c in range(m):
            piv=next(i for i in range(c,m) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
            pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
            for i in range(m):
                if i!=c and aug[i][c]!=0:
                    f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
        return [aug[i][m] for i in range(m)]
    out=[]; ties=0
    for s in range(1<<m):
        x=solve(s); o=0
        for v in range(m):
            a=s>>v&1
            cur=sum(P[v][a][j]*x[j] for j in range(m))+Q[v][a]; alt=sum(P[v][1-a][j]*x[j] for j in range(m))+Q[v][1-a]
            if alt>cur: o|=1<<v
            elif alt==cur: ties+=1
        out.append(o)
    h=ba_heights(out,m)
    print(f'm={m}: strict leak {leak}, ties {ties}, USO {is_uso(out,m)}, acyclic {is_acyclic(out,m)}, HK {is_holt_klee(out,m)[0]}, max height {max(h)}, walk from {start}: {ba_trace(out,start)} (length {len(ba_trace(out,start))-1})')
    return out
rows5=[(1484,1821,561,13,58,0),(28,0,0,4054,0,12),(1144,601,636,1393,5,0),(0,950,190,76,2753,5),(1,1359,1854,11,76,387),(3,7,2929,22,1123,1),(1439,0,0,2655,0,0),(719,1109,277,265,1435,20),(840,3,3222,3,0,0),(14,2,1,1910,1829,5)]
o5=check(rows5,5,12); print('outmap matches route:', o5==[11,4,1,22,15,2,13,0,3,10,8,9,23,14,21,12,17,16,19,6,31,20,29,18,24,25,26,27,7,28,5,30])
rows6=[(3558,515,0,1,0,1,20),(2327,0,1583,0,119,0,65),(4060,33,0,1,1,0,0),(1,0,0,0,0,4069,0),(213,453,1485,0,955,1,892),(0,1,0,4086,0,1,2),(359,221,2,0,1478,2,1850),(0,0,0,0,1,4093,0),(0,0,3318,482,1,0,2),(2310,1261,0,0,0,0,0),(7,9,0,973,0,3085,19),(0,1,3077,0,0,0,901)]
check(rows6,6,25)
