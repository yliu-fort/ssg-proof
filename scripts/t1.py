from fractions import Fraction as F
from lp_exact import Game
from transport import *

# S of prop:transport-stalls:  v=0 max, a=1, b=2, b1=3, b2=4 avg; t0=5,t1=6
S = Game(['max','avg','avg','avg','avg'],
         [(1,2),(6,5),(0,3),(4,5),(6,5)])
w = S.value()
print("S stopping:", S.is_stopping())
print("w* =", w)
print("Q  : Sep(a,b)=", sep(S,1,2)[0], " Sep(b,a)=", sep(S,2,1)[0])
subs = level_subsets(S,1)
print("subsets", subs)
sanity(S, subs, name="S/Q1")
print("Q1 : Sep(a,b)=", sep(S,1,2,subsets=subs)[0], " Sep(b,a)=", sep(S,2,1,subsets=subs)[0])
print("decided at level1:", decided(S,k=1,verbose=True))
