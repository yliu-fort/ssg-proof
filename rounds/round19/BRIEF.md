# Round 19 — brief

Supplement to `conjecture.md` (which stands unchanged), to the user's four
additions of round 17 (`rounds/round17/BRIEF.md`: the novelty pre-check
against the full inventory, the four imports only, object-changing routes
dominant with the tightened verdict scale, at most one paper audit) and to
the round-18 brief (`rounds/round18/BRIEF.md`: the corrected standing rule,
every agent on Opus 5). Set by the root agent on 2026-09-05 after the user
approved the root agent's recommendations on every decision item
("全部按你的推荐。开始工作"): eight routes, all Opus 5, `effort: 'high'`
throughout with a pacing sentence; one paper audit on the round-18 diff;
the two cheap eval-decision checks done by the root agent in parallel with
the run rather than by a route.

## Where round 18 left the search (rounds/round18/README.md)

The pivot is unmoved: no superpolynomial all-switches family
(`thm:seed-dichotomy`), no realisation of the third blow-up level. Round 18
narrowed the escape route to $B^{3}$ to one corner ($z=8$ with
$R_\alpha-C_\alpha$ mixed in sign over a driven three-Max block,
`cor:escape-m3`), proved the one-player fold and that a driven fold without
feedback is a cascade (`prop:one-player-fold`, `rem:one-player-fold`),
closed the $m=5$ column of the nondegenerate one-player ceiling at $11$
(`prop:hstar-one-eleven`), left $162$ Holt--Klee classes of the $4$-cube
unrealised (`rem:hk-survey`), found the tangent cut on the handicap-zero
class with no family designed against it (`rem:tangent-cut`), placed the
$\varepsilon$-order ladder's open middle at the promise-gap question
(`rem:eps-ladder`), and showed level one of the choice lift asymptotically
vacuous (`prop:router-tree`). Its README names six starting points; this
round takes five of them and adds two fresh formulations and one blind
route.

## Decisions taken (all per the root agent's recommendation)

| item | decision |
| --- | --- |
| A1 | the $B^{3}$ corner is a route of its own (`escape-certificate`): it is now a finite certificate question, not a search |
| A2 | the $m=6$ walk is a route of its own (`m6-walk`), the one search-flavoured route, held to the object rule by its theorem clauses |
| A3 | one blind route (`fresh-19`) with the digest and the inventory but no direction, for independence (conjecture.md) |
| A4 | the eval-decision follow-up is not a route: the root agent does the two cheap checks of `rem:eval-decide-gap` / `rem:rational-row` itself; the general adversary is dropped (it bears on nothing) |
| A5 | two fresh formulations: `promise-gap`, `extension-complexity` |
| B | every agent on Opus 5 (the user's standing instruction of 2026-09-03) |
| C | `effort: 'high'` on every agent, with the pacing sentence of `round18b.js` (a route died at xhigh on a 64k-token turn) |
| D | one paper audit: the 1317 lines added in round 18 (`git diff 812364d..6e6c011 -- frontier.tex`), the two rounds' backlog as secondary targets |
| E | all rules carried over; new: a required `games_built` field (build the game, verify from the game), no leaf enumeration of bit-length-deep trees, the headline audited as a claim of its own; the root agent's build check covers `undefined` and `multiply defined` |
| F | launched at once from this session after a one-call Opus probe; no token cap |
| G | the ~40 gitignored stray logs of the repository root moved to the session scratchpad; `main` left alone; the root README updated at the end of the round; no Lean work |

## The routes (all Opus 5, two audits each)

| key | object | the deliverable that counts |
| --- | --- | --- |
| `escape-certificate` | the feasibility set of the escape shape (`thm:escape-level`) over a driven block, as a semialgebraic set in its parameters | an exact infeasibility certificate for $z=8$ with mixed sign over the level-two block (closing the escape shape there), or a realisation; the level theorem of the second escape shape and its decision at $m=3$ |
| `fold-feedback` | a fold fed back into its own drive: the affine cascade of `prop:one-player-fold` carrying the counter | a stopping family with a proved superpolynomial all-switches run (the pivot), or a proved barrier on feedback folds |
| `hk-law-certificate` | the realisation set of an orientation by one-player readout systems as a bilinear semialgebraic set, with certificates uniform in the value configuration | a law beyond Holt--Klee with an exact certificate on the smallest unresolved $4$-cube class, tested against all $5951$ realised classes |
| `m6-walk` | the flip graph of realised one-player orientations of the $6$-cube along drive lines | a nondegenerate one-player game of height $\ge13$, the height-$14$ blow-up $s_6$ realised by one player (the doubling made one-player), or a proved obstruction; whether a degenerate five-state game beats $11$ |
| `promise-gap` | the promise problem $\textsc{Gap}_\varepsilon$ and the $\varepsilon$-ladder | $\textsc{Gap}_{1/\mathrm{poly}}$ in P, or target-equivalent by a reduction that reads the edges, or a proved obstruction to a named class of amplifications |
| `extension-complexity` | the value polytope $\mathrm{conv}\{\val_\sigma\}$ and the level of the choice-variable hierarchy as a growing function | a proved level lower bound with a growth law on a family; a nonnegative-rank bound with the factorisation theorem proved |
| `handicap-tangent` | the class $\mathcal R=\{B\succeq0\}$, its strongly convex slice $\{B\succeq\lambda I\}$ and the tangent cut | a family in $\mathcal R$ silent under the cut for a proved superpolynomial number of rounds, or a proved rate on $\{B\succeq\lambda I\}$ giving a polynomial class with a member outside the eight; the damping closure of $\mathcal R$ decided |
| `fresh-19` | chosen by the route, outside every family in the inventory | at least one proved or refuted statement of class new-object or new-relation, confirmed by the novelty audit |

## The paper audit (one agent)

The 1317 lines added to `frontier.tex` in round 18 (batches P, A--G,
`git diff 812364d..6e6c011`), which no one has read as paper text;
secondary targets, if time allows, the backlog of two rounds
(`prop:b3-outer`'s 194-vertex game; ST(1)/ST(2); `rem:bias-families`'
BP(D) counts; `prop:bias-witnesses`' PATH games; `rem:discount-fold`'s
$9D+3$ variant; `thm:eval-queries`' 136/194/344-vertex reproductions;
`rem:choice-lift`'s level-two exactness; $d(M_n)=n+1$;
`prop:hk-doubling-measured`(d),(e); `prop:oneplayer-census-small`'s total;
`prop:cv-measured`; `prop:q16`; `lem:max-tree`'s instance;
`prop:zero-ties`).

## What is unchanged

The standing rule in its round-17 form (three readings, all $Z$-seeded, a
stall only at a value-distinguishing vertex with all three silent), exact
rational arithmetic for every claim, the known-traps list, no writing into
the repository, no background jobs left behind, structured output plus
paste-ready LaTeX. The root agent verifies every load-bearing claim before
integration and applies a route only after both its audits.
