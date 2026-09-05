# ssg-proof

Work on the open problem stated in [`conjecture.md`](conjecture.md): deciding
whether the value of a *simple stochastic game* satisfies
`val(v₀) ≥ 1/2` in polynomial time.

The repository holds two kinds of artefact:

| Path | Purpose |
| --- | --- |
| `frontier.tex` (repo root) | the main document: the frontier of the search --- rigorous derivations of everything established, the exact remaining gaps, and the record of every refuted approach (about 276 pages at round 19); `boundary.tex` is a section fragment (the boundary-value calculus, labels `bv:*`) written for pasting into it; `make pdf TEX=frontier` compiles the main document with `latexmk` |
| `lean/` | a Lean 4 + Mathlib project for machine-checking the argument; `SSGProof/Blowup.lean` formalises `thm:blowup` of `frontier.tex` (core library only, no `sorry`, standard axioms) |
| `scripts/setup-env.sh` | one-shot environment setup |
| `scripts/harness/` | the exact-arithmetic SSG core (games, positional values, traps, first-passage laws, an exact simplex) shared by the verification scripts |
| `scripts/round15-verify/` … `scripts/round19-verify/` | the root agent's exact-arithmetic re-verifications, one directory per round, of every route claim integrated into `frontier.tex` in that round (each script's docstring states what it checks; witness games and certificates archived alongside) |
| `scripts/blowup/`, `scripts/ceiling/` | the blow-up normal forms and the bottom-antipodal ceiling computations that several rounds share |
| `rounds/` | per-round records (`rounds/round14/` … `rounds/round19/`): the brief, the workflow script, the run history, the structured route and audit results (`results/`), and a README whose Outcomes section says what each route found, how it was audited, what the root agent re-verified, and what entered the paper; each README ends with where the next round should start |
| `Makefile` | build entry points |

## Quick start

```bash
./scripts/setup-env.sh     # or: make setup
make lean                  # typecheck the Lean development
make pdf TEX=proof         # compile proof.tex -> proof.pdf
```

`scripts/setup-env.sh` is idempotent — re-run it any time to verify the
environment is still intact.

## Environment

### Shell variables (required)

Both are exported from `~/.profile` and `~/.bashrc`; `make` and
`scripts/setup-env.sh` also set them on their own, so a fresh shell needs no
manual step.

```bash
export ELAN_HOME="/data/opt/elan"        # Lean toolchains
export XDG_CACHE_HOME="/data/opt/cache"  # Mathlib .olean cache
export PATH="$ELAN_HOME/bin:$PATH"
```

`ELAN_HOME` is not optional. The root filesystem has under 10 GB free, while an
elan toolchain is ~3 GB and a built Mathlib is ~8 GB, so both live on the large
`/data` volume. If `ELAN_HOME` is unset, `elan` quietly re-downloads the whole
toolchain into `~/.elan` and fills the root disk.

### Lean 4 and Mathlib

* **elan** 4.2.4, installed at `/data/opt/elan`
* **Lean** `v4.33.1`, pinned by [`lean/lean-toolchain`](lean/lean-toolchain)
* **Mathlib** `v4.33.1` (rev `0df444a360ea`), pinned by
  [`lean/lake-manifest.json`](lean/lake-manifest.json), together with its
  dependencies: batteries, aesop, Qq, ProofWidgets, importGraph, plausible,
  LeanSearchClient, Cli.

Mathlib is *not* built from source. `lake exe cache get` downloads prebuilt
`.olean` files into `lean/.lake/` (~8 GB) using the shared `.ltar` cache under
`$XDG_CACHE_HOME/mathlib`; building from scratch would take hours.

```bash
cd lean
lake exe cache get     # prebuilt oleans; run after any Mathlib bump
lake build             # typecheck this project
```

`lean/.lake/` is git-ignored. Never commit it.

Editor support: install the `leanprover.lean4` VS Code extension and open the
`lean/` directory as the workspace root, so it picks up `lean-toolchain`.

### LaTeX

TeX Live from the Ubuntu 24.04 archive. Installed packages:

```
texlive-base           texlive-latex-base        texlive-latex-recommended
texlive-latex-extra    texlive-science           texlive-fonts-recommended
texlive-pictures       texlive-plain-generic     texlive-bibtex-extra
texlive-lang-greek     texlive-xetex             texlive-binaries
```

That covers everything the proof needs: `amsmath`, `amssymb`, `amsthm`,
`mathtools`, `cleveref`, `hyperref`, `microtype`, `tikz`, `algorithm` /
`algpseudocode`, `algorithm2e`, `stmaryrd`, `booktabs`, `enumitem`, `biblatex`.
Binaries: `pdflatex`, `xelatex`, `latexmk`, `bibtex`, `biber`.

To reinstall on a clean Debian/Ubuntu box:

```bash
sudo apt-get install -y texlive-latex-base texlive-latex-recommended \
  texlive-latex-extra texlive-science texlive-fonts-recommended \
  texlive-pictures texlive-plain-generic texlive-bibtex-extra \
  texlive-xetex latexmk biber
```

## Make targets

| Target | Effect |
| --- | --- |
| `make setup` | run `scripts/setup-env.sh` |
| `make lean` | `lake build` in `lean/` |
| `make cache` | `lake exe cache get` in `lean/` |
| `make pdf` | compile `$(TEX).tex` (default `proof`) |
| `make watch` | `latexmk -pvc` continuous rebuild |
| `make clean` | delete LaTeX build artefacts |

## Notes

* Disk: a full checkout with Mathlib built is ~8 GB under `lean/.lake/`. Keep
  the clone on `/data`.
* There is no `LICENSE` file yet. `lean/SSGProof/Basic.lean` carries the
  standard Mathlib copyright header, whose second line the
  `linter.style.header` check requires verbatim — including its reference to a
  file named `LICENSE`. Add an Apache-2.0 `LICENSE` when you settle on terms.
* No GitHub Actions workflow is configured. The `lake init math` template
  generates one under `lean/.github/`, where GitHub never looks, alongside
  auto-release and auto-update bots that push tags and open pull requests on
  their own; those files were removed rather than promoted to the repo root.
