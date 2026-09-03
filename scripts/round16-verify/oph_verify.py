import sys, json, time
sys.path.insert(0,'.')
from sparse_verify import analyse
from auso import ba_heights, ba_trace
from my_D import is_holt_klee
for name in ('H5_GAME.json','ST1_GAME.json','ST2_GAME.json'):
    path='../one-player-howard/'+name
    g=json.load(open(path)); m=g['kinds'].count('max'); k=g['kinds'].count('min')
    print('=====',name,'N',len(g['kinds'])+2,'Max',m,'Min',k,flush=True)
    t=time.time()
    out=analyse(path)
    h=ba_heights(out,m); top=[v for v in range(1<<m) if h[v]==max(h)]
    print('max height',max(h),'attained at',top[:8],'walk from',top[0],':',ba_trace(out,top[0]))
    if m<=8:
        hk,w=is_holt_klee(out,m); print('Holt-Klee:',hk,w)
    print('time',round(time.time()-t,1),'s',flush=True)
