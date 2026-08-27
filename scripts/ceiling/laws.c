#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* Ceiling for all-switches schedules under a selectable set of necessary laws.
   sigma_0..sigma_L in {0,1}^m, S_t = sigma_t ^ sigma_{t+1} nonempty, S_L := empty.
   B : (sigma_s ^ sigma_t) & S_s != 0                     for s<t          [cor:no-return]
   F : (sigma_s ^ sigma_t) not subset of S_t              for s<t<=L-1     [cor:law-b]
   C : ((sigma_s ^ sigma_t) & S_s) not subset of S_t      for s<t          [peak-vertex law]
   U : (S_s ^ S_t) & (sigma_s ^ sigma_t) != 0             for s!=t         [USO outmap law]
   flags bit0=F bit1=C bit2=U   (B always on)
*/
static int M,NP,FULL,FL;
static unsigned char forb[1<<21];
static int nfree;
static int prevpt[400], Sarr[400];
static int best,bestseq[401],bestS[400];
static long long nodes=0;

static void rec(int p,int t){
    int S,q,i,ok,d;
    if(t>best){ best=t; for(i=0;i<t;i++){bestseq[i]=prevpt[i];bestS[i]=Sarr[i];} bestseq[t]=p;
        fprintf(stderr,"best %d\n",best); fflush(stderr);}
    if(t+nfree<=best) return;
    nodes++;
    for(S=1;S<NP;S++){
        q=p^S;
        if(forb[q]) continue;            /* law B for the new point */
        ok=1;
        for(i=0;i<t;i++){
            d=prevpt[i]^p;
            if((FL&1) && (d & ~S & FULL)==0){ok=0;break;}
            if((FL&2) && ((d&Sarr[i]) & ~S & FULL)==0){ok=0;break;}
            if((FL&4) && ((Sarr[i]^S) & d)==0){ok=0;break;}
        }
        if(!ok) continue;
        int base=p&S, free_=FULL&~S, sub, x, cnt=0;
        x=base; if(forb[x]++==0) cnt++;
        sub=free_; while(sub){ x=base|sub; if(forb[x]++==0) cnt++; sub=(sub-1)&free_; }
        nfree-=cnt;
        prevpt[t]=p; Sarr[t]=S;
        rec(q,t+1);
        x=base; forb[x]--;
        sub=free_; while(sub){ x=base|sub; forb[x]--; sub=(sub-1)&free_; }
        nfree+=cnt;
    }
}
int main(int argc,char**argv){
    int k,S0,i;
    M=atoi(argv[1]); FL=atoi(argv[2]); NP=1<<M; FULL=NP-1;
    memset(forb,0,NP); nfree=NP; best=0;
    for(k=1;k<=M;k++){
        S0=(1<<k)-1;
        int q=S0,base=0,free_=FULL&~S0,sub,x,cnt=0;
        x=base; if(forb[x]++==0) cnt++;
        sub=free_; while(sub){ x=base|sub; if(forb[x]++==0) cnt++; sub=(sub-1)&free_; }
        nfree-=cnt;
        prevpt[0]=0; Sarr[0]=S0;
        if(!forb[q]) rec(q,1);
        x=base; forb[x]--;
        sub=free_; while(sub){ x=base|sub; forb[x]--; sub=(sub-1)&free_; }
        nfree+=cnt;
    }
    printf("m=%d flags=%d  L=%d  nodes=%lld\nsigmas:",M,FL,best,nodes);
    for(i=0;i<=best;i++) printf(" %d",bestseq[i]);
    printf("\nS:"); for(i=0;i<best;i++) printf(" %d",bestS[i]);
    printf("\n"); fflush(stdout);
    return 0;
}
