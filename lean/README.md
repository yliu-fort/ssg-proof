# SSGProof — Lean 4 formalisation

Lean 4 + Mathlib scaffold for the simple-stochastic-game development.
See the [repository README](../README.md) for environment setup.

```bash
cd lean
lake exe cache get   # prebuilt Mathlib .olean files
lake build
```

* `lean-toolchain` pins the Lean version; `lake-manifest.json` pins Mathlib.
* `SSGProof/` holds the library sources, re-exported from `SSGProof.lean`.
* `SSGProof/Basic.lean` is a smoke test only — replace it with real content.

No GitHub Actions workflow is configured. The `lake init math` template ships
one, plus auto-release and auto-update bots; they were removed because they sat
under `lean/.github/` where GitHub never reads them, and the bots push tags and
open pull requests on their own.
