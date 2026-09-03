from fractions import Fraction as F
import itertools
# driven inner block of prop:b2-realised, rows in 512ths over (c1,c2,c3,c6) | t1-mass = a*t + b with t = y_{c5}
rows = {  # vertex: [(coeffs over (c1,c2,c3,c6), (a,b)) for action 0, action 1]
 'c1': [((12,461,36,0),(0,0)), ((276,0,0,0),(127,47))],
 'c2': [((0,0,509,0),(0,0)),  ((0,83,0,0),(320,12))],
 'c3': [((0,0,0,460),(0,43)), ((267,187,0,0),(56,0))],
 'c6': [((472,0,0,0),(0,0)),  ((0,493,0,0),(16,1))],
}
V=['c1','c2','c3','c6']
def solve(choice,t):
    n=4; M=[[F(0)]*(n+1) for _ in range(n)]
    for i,v in enumerate(V):
        co,(a,b)=rows[v][choice[v]]
        M[i][i]+=1
        for j in range(n): M[i][j]-=F(co[j],512)
        M[i][n]=F(a,512)*t+F(b,512)
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]; pv=M[c][c]; M[c]=[x/pv for x in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[x-f*y for x,y in zip(M[r],M[c])]
    return {v:M[i][n] for i,v in enumerate(V)}
def outmap(t):
    out=[]
    for si in range(8):
        sigma={'c1':(si>>0)&1,'c2':(si>>1)&1,'c3':(si>>2)&1}
        cands=[]
        for tb in (0,1):
            ch=dict(sigma); ch['c6']=tb; cands.append(solve(ch,t))
        val={v:min(cands[0][v],cands[1][v]) for v in V}
        # improvement outmap: for each Max vertex, is the other action's readout larger?
        bitsout=0
        for j,v in enumerate(['c1','c2','c3']):
            a=sigma[v]
            def readout(act):
                co,(aa,bb)=rows[v][act]
                return sum(F(co[k],512)*val[V[k]] for k in range(4)) + F(aa,512)*t + F(bb,512)
            cur=readout(a); oth=readout(1-a)
            if oth==cur: return None
            if oth>cur: bitsout|=1<<j
        out.append(bitsout)
    return out
B1=[0,1,3,6,7,4,5,2]; B1t=[7,4,5,2,0,1,3,6]
for t,name in [(F(0),'t=0'),(F(2036,3313),'t=pi_B'),(F(1,4),'t=1/4'),(F(47,80),'t=47/80'),(F(311,500),'t=311/500')]:
    o=outmap(t); print(name, o, 'B1' if o==B1 else ('B1 translate' if o==B1t else 'other'))
# pinned values check
A0=F(502,512); a0=F(8,512); Bp=F(509,512)
piA=a0/(1-A0*Bp); print('pi_A',piA,'pi_B',Bp*piA)
