#!/usr/bin/env bash
# Set up the proof environment for ssg-proof: Lean 4 + Mathlib + LaTeX.
# Idempotent: safe to re-run. See README.md for what this installs and why.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# The root filesystem on this box is small (<10 GB free); an elan toolchain is
# ~3 GB and a built Mathlib is ~8 GB. Keep both on the large /data volume.
# ELAN_HOME is load-bearing: without it elan silently re-installs into ~/.elan.
export ELAN_HOME="${ELAN_HOME:-/data/opt/elan}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/data/opt/cache}"   # Mathlib `cache` writes here
export PATH="$ELAN_HOME/bin:$PATH"

say() { printf '\n==> %s\n' "$*"; }

say "Checking elan (Lean toolchain manager)"
if ! command -v elan >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
    | sh -s -- -y --no-modify-path
fi
elan --version

say "Installing the toolchain pinned by lean/lean-toolchain"
cd "$REPO_ROOT/lean"
elan toolchain install "$(cat lean-toolchain)"
lean --version
lake --version

# `lake exe cache get` first materialises the dependencies recorded in
# lake-manifest.json, then downloads their prebuilt .olean files. Do NOT use
# `lake update` here: it re-resolves the pins and would silently move Mathlib.
say "Fetching dependencies and prebuilt Mathlib .olean files (skips a multi-hour rebuild)"
lake exe cache get

say "Building the project"
lake build

say "Checking LaTeX"
missing=()
for bin in pdflatex xelatex latexmk biber; do
  command -v "$bin" >/dev/null 2>&1 || missing+=("$bin")
done
for sty in amsthm.sty mathtools.sty cleveref.sty tikz.sty algorithm.sty algpseudocode.sty biblatex.sty; do
  kpsewhich "$sty" >/dev/null 2>&1 || missing+=("$sty")
done
if [ ${#missing[@]} -gt 0 ]; then
  echo "MISSING LaTeX components: ${missing[*]}" >&2
  echo "On Debian/Ubuntu install with:" >&2
  echo "  sudo apt-get install -y texlive-latex-base texlive-latex-recommended \\" >&2
  echo "       texlive-latex-extra texlive-science texlive-fonts-recommended \\" >&2
  echo "       texlive-pictures texlive-xetex latexmk biber" >&2
  exit 1
fi
echo "LaTeX toolchain OK"

say "Environment ready"
