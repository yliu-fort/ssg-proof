# Round 17 — brief

Supplement to `conjecture.md` (which stands unchanged). Set by the user on
2026-09-04 02:15 UTC after the round-16 self-assessment; launch scheduled
for 03:51 UTC (one hour thirty minutes after the instruction), all agents
on Opus 5.

## The user's four additions (verbatim, then how they are enforced)

1. 在路线设计时规避重复发现已有引理的问题。
   Every route receives the full inventory of the paper's 471 numbered
   results (`inventory.txt`: line, environment, label, title) and must,
   before reporting any result, name the closest existing label and say in
   one line why the new statement does not follow from it in three lines.
   The novelty audit repeats that search independently. A result whose
   closest label yields it in three lines is a restatement and is not a
   result.
2. 从第一性原理建的原则要保留。
   The four imports stay the only imports (thm:determinacy, Holt–Klee,
   Legendre, Samelson–Thrall–Wesler). No web access. Prior art may be
   named from memory, flagged as unchecked, and is never a proof.
3. 让"换对象"的路线占据探索的主导。成功标准要收紧："新结果"是已有引理的
   重述，以及"新的一行测量数据"这种不能作为成功。
   All seven routes change the mathematical object (query complexity,
   the order lattice, convex lifts, variational principles, a parametric
   path, a unified oracle model, realisation spaces); the one in-framework
   target (the third blow-up level) is carried inside the realisation-space
   route as its test case, not as a route of its own. The verdict scale is
   SOLVED / new-theorem / new-barrier / blocked / dead-end; "strict-progress"
   is gone. A route succeeds only if it returns at least one proved or
   refuted statement whose novelty class is new-object or new-relation and
   which the novelty audit confirms. Measured rows are supporting evidence
   attached to a theorem, never a result; restatements are reported in a
   separate field and earn nothing.
4. 论文的审计每轮最多开一个agent。
   One paper audit, on the highest-yield target by round 16's evidence:
   the 2698 lines added to `frontier.tex` in round 16 (batches A–I,
   `git diff ab61ad4..7fa45a3`), which no one has read as paper text.

## The routes (all Opus 5, two audits each)

| key | object | the deliverable that counts |
| --- | --- | --- |
| `query-model` | the strategy-evaluation oracle model on the Max cube | a proved lower or upper bound on the query complexity of finding the sink on orientations SSGs realise, as opposed to abstract AUSOs |
| `order-lattice` | the lattice of vertex orders as certificates (thm:order-determines) | a monotone iteration over orders with a proved step bound, or a proved obstruction to any such iteration |
| `convex-lift` | the lifted bilinear system in (values, Min choices) and its convex hull / RLT hierarchy | exactness or an explicit integrality gap with its growth, and the first exact level on the wedge and on CV |
| `variational` | energy functionals and reversibility | a polynomial class defined by a symmetry of the chance part, with a witness outside the eight classes, or a theorem that the symmetry never helps |
| `parametric-path` | the optimal pair as a function of a uniform stopping probability | a proved bound or an explicit exponential family for the number of breakpoints, and whether the path can be followed with one-player solves |
| `oracle-barrier` | one model containing M1–M6, all-switches and BSI | a family on which every algorithm of the model needs 2^Ω(N) steps, and the smallest extension that decides it |
| `realisation-space` | the semialgebraic set of games realising a given orientation | the cost of a blow-up level as a geometric invariant; B^3 as the test case (constructively or with a proved obstruction) |

## What is unchanged

The standing rule (rem:own-successor with the Z-seed), exact rational
arithmetic for every claim, the known-traps list, no writing into the
repository, no background jobs left behind, structured output plus
paste-ready LaTeX. The root agent verifies every load-bearing claim before
integration and applies a route only after both its audits.
