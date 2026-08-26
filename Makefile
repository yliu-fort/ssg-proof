# ssg-proof — build entry points.
#
#   make setup     one-time environment setup (Lean + Mathlib + LaTeX check)
#   make lean      typecheck the Lean formalisation
#   make cache     re-download prebuilt Mathlib .olean files
#   make pdf       compile the LaTeX proof   (make pdf TEX=proof)
#   make clean     remove LaTeX build artefacts

TEX ?= proof
LEAN_DIR := lean

export ELAN_HOME ?= /data/opt/elan
export XDG_CACHE_HOME ?= /data/opt/cache
export PATH := $(ELAN_HOME)/bin:$(PATH)

.PHONY: setup lean cache pdf watch clean

setup:
	./scripts/setup-env.sh

lean:
	cd $(LEAN_DIR) && lake build

cache:
	cd $(LEAN_DIR) && lake exe cache get

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error $(TEX).tex

watch:
	latexmk -pdf -pvc -interaction=nonstopmode $(TEX).tex

clean:
	latexmk -C $(TEX).tex 2>/dev/null || true
	rm -f *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.out *.run.xml *.toc
