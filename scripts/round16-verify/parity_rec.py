import sys; sys.path.insert(0,'.')
from auso import ba_heights
exec(open('b3.py').read().split('s, m = [1, 0], 1')[0])   # defines B(sA,m)
def check(sA,m,name):
    n=1<<m; h=ba_heights(sA,m); o=[v for v in range(n) if sA[v]==0][0]
    starts=[v for v in range(n) if h[v]==max(h)]; u=starts[0]; z=o^u; hu=h[u]
    s,_,_=B(sA,m); H=ba_heights(s,m+2); A,Bb=1<<m,1<<(m+1)
    bad=0
    for v in range(n):
        vp=v^sA[v]
        pred={ (0,0): h[v^z], (1,1): h[v]+2+hu,
               (1,0): h[v]+2+hu if h[v]%2==0 else 1+h[vp^z],
               (0,1): 1+h[vp^z] if h[v]%2==0 else h[v]+2+hu }
        for (a,b),val in pred.items():
            idx=v|(a*A)|(b*Bb)
            if H[idx]!=val: bad+=1
    print(f'{name}: dim {m}->{m+2}, h_u={hu}, max height {max(H)} (=2h+2: {max(H)==2*hu+2}), mismatches {bad}/{4*n}')
B1=[0,1,3,6,7,4,5,2]; B2=[7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
gsharp=[0,1,3,6,7,4,13,10,14,15,9,12,11,8,5,2]
hk11=None
import re
txt=open('/data/ssg-proof/frontier.tex').read()
i=txt.find('label{prop:hkfive}'); seg=txt[i:i+3000]
m_=re.search(r'\(((?:\d+,\s*){31}\d+)\)',seg)
if m_: hk11=[int(x) for x in m_.group(1).replace(' ','').split(',')]
for sA,m,name in [([1,0],1,'1-cube'),(B1,3,'B^1'),(B2,5,'B^2'),(gsharp,4,'G#'),([0,1,3,2],2,'2-cube h2')]+([(hk11,5,'HK11')] if hk11 else []):
    check(sA,m,name)
