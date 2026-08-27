"""Step 1: validate the kit against value vectors already recorded in
frontier.tex, then verify the claims of boundary.tex one by one."""
from fractions import Fraction as F
from itertools import product
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bv2 import PGame, freeze, ssg_to_pgame, value_iteration

def show(x):
    return "(" + ", ".join(str(t) for t in x) + ")"

# ---- G8 of prop:simorder-stalls -----------------------------------------
G8 = ssg_to_pgame(['avg','avg','avg','avg','avg','max'],
                  [(0,7),(0,6),(6,4),(0,2),(3,2),(4,1)])
w = G8.value()
print("G8  w* =", show(w[:6]), " expected 1,1/2,1/5,3/5,2/5,1/2")
assert w[:6] == [F(1),F(1,2),F(1,5),F(3,5),F(2,5),F(1,2)]

# ---- S of prop:transport-stalls -----------------------------------------
S = ssg_to_pgame(['max','avg','avg','avg','avg'],
                 [(1,2),(6,5),(0,3),(4,5),(6,5)])
w = S.value()
print("S   w* =", show(w[:5]), " expected 1/2,1/2,3/8,1/4,1/2  stopping:", S.is_stopping())
assert w[:5] == [F(1,2),F(1,2),F(3,8),F(1,4),F(1,2)]
assert S.is_stopping()

# ---- H_m of cor:slack-stalls is not rebuilt here; G8 and S suffice -------

# ---- D of prop:bv-rule ---------------------------------------------------
D = ssg_to_pgame(['max','avg','avg','avg','avg','avg','avg'],
                 [(1,5),(0,2),(0,3),(8,4),(7,8),(4,6),(4,8)])
wD = D.value()
print("D   w* =", show(wD[:7]), "stopping:", D.is_stopping())
assert wD[:7] == [F(3,4),F(3,4),F(3,4),F(3,4),F(1,2),F(5,8),F(3,4)], wD
D0 = freeze(D, 0, F(1,2))
wD0 = D0.value()
print("D_0 w  =", show(wD0[:7]), " expected 1/2,9/16,5/8,3/4,1/2,5/8,3/4")
assert wD0[:7] == [F(1,2),F(9,16),F(5,8),F(3,4),F(1,2),F(5,8),F(3,4)], wD0
print("  true comparison  val_D(1)=%s > val_D(5)=%s" % (wD[1], wD[5]))
print("  frozen comparison val_D0(1)=%s < val_D0(5)=%s   -> frozen rule names the WRONG successor"
      % (wD0[1], wD0[5]))
assert wD[1] > wD[5] and wD0[1] < wD0[5]

# ---- prop:bv-neither -----------------------------------------------------
Gn = ssg_to_pgame(['avg','avg','avg','max','min','avg','avg'],
                  [(7,8),(0,8),(7,0),(6,1),(6,2),(3,4),(7,8)])
wn = Gn.value()
print("bv-neither w* =", show(wn[:7]), "stopping:", Gn.is_stopping())
for th in [F(0),F(1,8),F(1,4),F(1,2),F(3,4),F(7,8),F(1)]:
    g = freeze(Gn, 6, th)
    v = g.value()
    pred = F(1,2)*max(th,F(3,4)) + F(1,2)*min(th,F(1,4))
    assert v[5] == pred, (th, v[5], pred)
print("  V_5(theta) = 1/2 max(theta,3/4) + 1/2 min(theta,1/4) confirmed at 7 thetas"
      " -> slopes 1/2,0,1/2: neither convex nor concave")
print("OK step 1")
