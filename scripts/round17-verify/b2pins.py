# Verify the round-17 realisation-space route's three new realisations of B^2 with the round-16 sparse verifier.
import sys
src = open('sparse_verify.py').read().split("if __name__=='__main__':")[0]
exec(src)
B2 = [7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
for f in sys.argv[1:]:
    print('=====', f.split('/')[-1], flush=True)
    analyse(f, target=B2, start=12)
