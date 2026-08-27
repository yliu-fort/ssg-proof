#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int M, NP, FULL;
static unsigned char forb[1<<20];   /* cover counts */
static int nfree;
static int prevpt[200];             /* sigma_0..sigma_{t-1} */
static int Sarr[200];
static int best, bestseq[201], bestS[200];
static long long nodes=0;

static void rec(int p, int t){
    int S,q,i,ok,d,x,base,free_,sub;
    if(t>best){
        best=t;
        for(i=0;i<t;i++){bestseq[i]=prevpt[i];bestS[i]=Sarr[i];}
        bestseq[t]=p;
        fprintf(stderr,"  new best %d\n",best);
    }
    if(t+nfree<=best) return;
    nodes++;
    for(S=1;S<NP;S++){
        q=p^S;
        if(forb[q]) continue;
        ok=1;
        for(i=0;i<t;i++){ d=prevpt[i]^p; if((d & ~S & FULL)==0){ok=0;break;} }
        if(!ok) continue;
        /* add cube C_t = {x : x&S == p&S} */
        base=p&S; free_=FULL&~S;
        sub=free_;
        { int cnt=0;
          x=base; if(forb[x]++==0) cnt++;
          sub=free_;
          while(sub){ x=base|sub; if(forb[x]++==0) cnt++; sub=(sub-1)&free_; }
          nfree-=cnt;
          prevpt[t]=p; Sarr[t]=S;
          rec(q,t+1);
          prevpt[t]=0;
          x=base; forb[x]--;
          sub=free_;
          while(sub){ x=base|sub; forb[x]--; sub=(sub-1)&free_; }
          nfree+=cnt;
        }
    }
}

int main(int argc,char**argv){
    int k,S0,i;
    M=atoi(argv[1]); NP=1<<M; FULL=NP-1;
    memset(forb,0,NP); nfree=NP; best=0;
    /* sigma_0 = 0 WLOG (translation). S_0 canonical: first k coords, k=1..M (permutation). */
    for(k=1;k<=M;k++){
        S0=(1<<k)-1;
        /* emulate one level of rec with S restricted */
        int p=0,q=S0,base=0,free_=FULL&~S0,sub,x,cnt=0;
        x=base; if(forb[x]++==0) cnt++;
        sub=free_;
        while(sub){ x=base|sub; if(forb[x]++==0) cnt++; sub=(sub-1)&free_; }
        nfree-=cnt;
        prevpt[0]=0; Sarr[0]=S0;
        if(!forb[q]) rec(q,1);
        x=base; forb[x]--;
        sub=free_; while(sub){ x=base|sub; forb[x]--; sub=(sub-1)&free_; }
        nfree+=cnt;
    }
    printf("m=%d f=%d nodes=%lld\n",M,best,nodes);
    printf("sigmas:");
    for(i=0;i<=best;i++) printf(" %d",bestseq[i]);
    printf("\nS:");
    for(i=0;i<best;i++) printf(" %d",bestS[i]);
    printf("\n");
    return 0;
}
