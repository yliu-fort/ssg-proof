/-
Copyright (c) 2026 ssg-proof contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: ssg-proof contributors
-/
import Mathlib

/-!
# Environment smoke test

This file exists only to check that the toolchain is wired up: it imports all of
Mathlib and proves two one-line facts about `Set.Icc (0 : ℝ) 1`, the range of the
value function of a simple stochastic game. Delete it once real content lands.
-/

namespace SSGProof

/-- A value in `[0,1]`, the range of `val` for a simple stochastic game. -/
abbrev Value := Set.Icc (0 : ℝ) 1

/-- The averaging step at a coin-flip vertex keeps values in `[0,1]`. -/
theorem avg_mem_Icc {x y : ℝ} (hx : x ∈ Set.Icc (0 : ℝ) 1) (hy : y ∈ Set.Icc (0 : ℝ) 1) :
    (x + y) / 2 ∈ Set.Icc (0 : ℝ) 1 := by
  obtain ⟨hx0, hx1⟩ := hx
  obtain ⟨hy0, hy1⟩ := hy
  constructor <;> linarith

/-- `max` of two values in `[0,1]` stays in `[0,1]`; the Max player's step. -/
theorem max_mem_Icc {x y : ℝ} (hx : x ∈ Set.Icc (0 : ℝ) 1) (hy : y ∈ Set.Icc (0 : ℝ) 1) :
    max x y ∈ Set.Icc (0 : ℝ) 1 :=
  ⟨le_max_of_le_left hx.1, max_le hx.2 hy.2⟩

end SSGProof
