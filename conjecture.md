\documentclass{article}
\usepackage{amsmath,amssymb}

\begin{document}

\paragraph{Simple stochastic games.}
A \emph{simple stochastic game} is a directed graph on vertex set
$V = V_{\max} \cup V_{\min} \cup V_{\mathrm{avg}} \cup \{t_0, t_1\}$,
where every vertex except the sinks $t_0, t_1$ has out-degree two.
A token starts at a designated vertex $v_0$ and is moved along edges:
at vertices in $V_{\max}$ (resp.\ $V_{\min}$) player Max (resp.\ Min)
chooses the edge; at vertices in $V_{\mathrm{avg}}$ the edge is chosen
by a fair coin flip. Max wins if the token reaches $t_1$; Min wins
otherwise. Both players have optimal positional strategies, and the
value $\mathrm{val}(v_0)$ --- the probability that the token reaches
$t_1$ under optimal play --- is a rational number of polynomial bit-size.

\begin{quote}
\textbf{Open problem}. Given a simple stochastic game,
can $\mathrm{val}(v_0) \ge \tfrac12$ be decided in polynomial time?
The problem is in $\mathsf{NP} \cap \mathsf{coNP}$, but not known
to be in $\mathsf{P}$.
\end{quote}

\end{document}


Current task statement

Give a rigorous standalone proof of the above math problem using your own knowledge, computation, and reasoning without searching the public web, connected sources, previous conversations, project contexts, or existing local files. Return the proof as one compilable full-English LaTeX .tex file in repo.
Assume for purposes of this task that a complete affirmative proof exists. Work iteratively until a correct proof has been reached.
Partial progress does not count unless it implies exactly the resolution of the entire problem above. In particular, reductions to other unproved conjectures, computational verification through any fixed parameters, and candidate counterexamples without a proved certificate are insufficient.
Use multiagents aggressively and dynamically. Do not use a fixed assignment such as "N agents for strategy X." Instead, manage the search using the following heuristics:
Begin with a genuinely diverse portfolio of approaches. Agents should explore substantially different formulations, invariants, reductions, algebraic viewpoints, structural inductions, decompositions, flow formulations, transition systems, embeddings, extremal arguments, and computational sanity checks.
Do not tell most agents the currently favored approach. Preserve independence during early rounds so that agents do not all converge to the same attractive but incomplete reduction.
Maintain an explicit registry of approach families. Group agents by the mathematical idea they are using, not by superficial wording. If many agents converge to one family, redirect some of them toward underexplored formulations.
Do not allow one approach to dominate merely because it gives elegant reductions. A route that ends at a lemma equivalent in strength to the original problem is not close to completion unless it supplies a genuinely new proof of that lemma.
When an approach stalls at a theorem-strength missing lemma, mark that route as blocked. Only continue assigning agents to it if someone proposes a materially new mechanism, invariant, or construction.
Keep several incompatible proof routes alive through multiple rounds. Cross-pollinate ideas only after independent agents have developed them far enough to expose their real strengths and gaps.
Use adversarial agents throughout: every candidate proof must be checked for gaps, conditionals, handwavings, and circular uses of an equivalent statement.
Require agents to return concrete lemmas, constructions, equations, or counterexamples to proposed sublemmas. Reject status reports, vague optimism, and claims that an unproved statement is "routine."
The root agent should repeatedly synthesize, challenge, redirect, and launch new rounds. Do not stop after the first wave fails. Produce a complete proof if one survives audit; otherwise report only the strongest rigorously proved derivation and its exact remaining gap.
Do not return merely because current approaches fail or agents report theorem-strength gaps.
Continue launching new rounds, reopening blocked approaches only when there is a genuinely new mechanism, and searching for fresh formulations.
Return only when a complete affirmative proof has been found and survives adversarial audit.
Do not return a reduction, partial result, isolated missing lemma, "best effort" summary, or explanation of why the problem is difficult.
Do not search the public web to determine whether the problem is open, and do not answer that it is open.