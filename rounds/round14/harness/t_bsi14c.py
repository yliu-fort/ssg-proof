import sys; sys.path.insert(0, '.')
import mycore as M, bsi as B, cc, wd
from t_bsi14b_lib import table
def unwrap(x):
    return x[0] if isinstance(x, tuple) else x
table("CC(1,2)", unwrap(cc.CC(1, 2))); table("CC(2,3)", unwrap(cc.CC(2, 3)))
table("WD(4,2,6)", unwrap(wd.WD(4, 2, 6))); table("WD(6,3,7)", unwrap(wd.WD(6, 3, 7)))
kinds = ['min','min','avg','avg','max','avg','min','min']; T0, T1 = 8, 9
R = M.G(kinds, [(2,5),(5,3),(5,2),(0,T1),(0,T0),(T1,T0),(0,T0),(5,2)])
table("R (prop:own-stall)", R)
table("R (+) dual R", B.union(R, B.dual(R)))
