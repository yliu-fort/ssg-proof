#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* Ceiling under laws: (B) cor:no-return, (F) cor:law-b, and optionally (C) the peak-vertex law.
   mode 0 : (B)+(F)                  -> f(m)   of rem:allsw-laws
   mode 1 : (B)+(C)                  -> f_C(m) ; (C) implies (F)
*/
static int M,NP,FULL,MODE;
static unsigned char forb[1<<21];
static int nfree;
static int prevpt[300], Sarr[300];
static int best,bestseq[301],bestS[300];
static long long nodes=0;

static void rec(int p,int t){
    int S,q,i,ok,d;
    if(t>best){ best=t; for(i=0;i<t;i++){bestseq[i]=prevpt[i];bestS[i]=Sarr[i];} bestseq[t]=p;
        fprintf(stderr,"best %d\n",best); }
    if(t+nfree<=best) return;
    nodes++;
    for(S=1;S<NP;S++){
        q=p^S;
        if(forb[q]) continue;
        ok=1;
        for(i=0;i<t;i++){
            d=prevpt[i]^p;
            if(MODE) d &= Sarr[i];
            if((d & ~S & FULL)==0){ok=0;break;}
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
    M=atoi(argv[1]); MODE=atoi(argv[2]); NP=1<<M; FULL=NP-1;
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
    printf("m=%d mode=%d  L=%d  nodes=%lld\n",M,MODE,best,nodes);
    printf("sigmas:"); for(i=0;i<=best;i++) printf(" %d",bestseq[i]);
    printf("\nS:"); for(i=0;i<best;i++) printf(" %d",bestS[i]);
    printf("\n");
    return 0;
}
