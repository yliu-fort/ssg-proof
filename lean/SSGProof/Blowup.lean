/-
Copyright (c) 2026 ssg-proof contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: ssg-proof contributors
-/

/-!
# A height-doubling blow-up of acyclic unique sink orientations

This file formalises `thm:blowup` of `frontier.tex`, using only the Lean core
library (no Mathlib import is needed).

A vertex of the `ι`-cube is a function `ι → Bool`; an *outmap* `s : V ι → V ι`
records, at each vertex, the set of coordinates whose edge points away from it.
`IsUSO s` is the Szabó–Welzl condition, `IsAcyclic s` the existence of a bounded
rank strictly decreasing along every edge (for a finite cube this is acyclicity
of the edge digraph), `ba s` the bottom-antipodal step `v ↦ v ⊕ s v`, and
`Height s o h` says `h` counts the steps of that walk to the sink `o`.

`blow s z par` is the orientation of the `(ι ⊕ Fin 2)`-cube whose inner part is
`s (v ⊕ z)` on the layer `(0,0)` and `s v` elsewhere, and whose outer part is the
parity table of the theorem. We prove:

* `isUSO_blow`: it is a unique sink orientation whenever `s` is, for every `z`
  and every parity function;
* `isAcyclic_blow`: it is acyclic whenever `s` is, for every `z` and parity;
* `walk_blow`: with `z = o ⊕ u`, `h u = H` and `par = even ∘ h`, the
  bottom-antipodal walk from the appropriate start reaches the sink `(0,0,u)`
  after exactly `2H + 2` steps and not before.
-/

set_option linter.unusedSectionVars false

namespace SSGProof.Cube

/-- Vertices of the cube with coordinate set `ι`. -/
abbrev V (ι : Type _) := ι → Bool

variable {ι : Type _} [DecidableEq ι]

/-- Coordinatewise exclusive or. -/
def xorV (u v : V ι) : V ι := fun i => xor (u i) (v i)

/-- Flip one coordinate. -/
def flip (v : V ι) (i : ι) : V ι := fun j => if j = i then !v i else v j

/-- The zero vector, the outmap of a sink. -/
def zeroV : V ι := fun _ => false

/-- The Szabó–Welzl condition: any two distinct vertices are separated by a
coordinate on which they differ and on which their outmaps differ. -/
def IsUSO (s : V ι → V ι) : Prop :=
  ∀ u v : V ι, u ≠ v → ∃ i, s u i ≠ s v i ∧ u i ≠ v i

/-- The directed edges of the orientation. -/
def Edge (s : V ι → V ι) (v w : V ι) : Prop := ∃ i, s v i = true ∧ w = flip v i

/-- Acyclicity, as the existence of a bounded rank strictly decreasing along
every edge (equivalent to the absence of directed cycles on a finite cube). -/
def IsAcyclic (s : V ι → V ι) : Prop :=
  ∃ (r : V ι → Nat) (R : Nat), (∀ v, r v ≤ R) ∧ ∀ v w, Edge s v w → r w < r v

/-- The bottom-antipodal step. -/
def ba (s : V ι → V ι) (v : V ι) : V ι := xorV v (s v)

/-- `h` is the bottom-antipodal height function of `s` with sink `o`. -/
structure Height (s : V ι → V ι) (o : V ι) (h : V ι → Nat) : Prop where
  sink : s o = zeroV
  h_sink : h o = 0
  step : ∀ v, v ≠ o → h (ba s v) + 1 = h v

/-! ### The blow-up -/

/-- Outer part of the rule in the `α` coordinate, as a function of the layer
`(a, b)` and of the parity flag `e` (`true` when the inner height is even). -/
def outA (a b e : Bool) : Bool :=
  match a, b with
  | false, false => false
  | true, false => true
  | false, true => !e
  | true, true => e

/-- Outer part of the rule in the `β` coordinate. -/
def outB (a b e : Bool) : Bool :=
  match a, b with
  | false, false => false
  | true, false => e
  | false, true => true
  | true, true => !e

/-- The vertex of the blown-up cube with outer coordinates `a, b` and inner
part `v`. -/
def mk (a b : Bool) (v : V ι) : V (ι ⊕ Fin 2) := fun j =>
  match j with
  | Sum.inl i => v i
  | Sum.inr k => if k = 0 then a else b

/-- Inner part of a vertex of the blown-up cube. -/
def inner (w : V (ι ⊕ Fin 2)) : V ι := fun i => w (Sum.inl i)

/-- The blown-up orientation. `z` is the translation vector of the layer
`(0,0)` and `par v` the parity flag of the inner vertex `v`. -/
def blow (s : V ι → V ι) (z : V ι) (par : V ι → Bool) :
    V (ι ⊕ Fin 2) → V (ι ⊕ Fin 2) := fun w =>
  let v := inner w
  let a := w (Sum.inr 0)
  let b := w (Sum.inr 1)
  let innerOut : V ι := if a = false ∧ b = false then s (xorV v z) else s v
  fun j =>
    match j with
    | Sum.inl i => innerOut i
    | Sum.inr k => if k = 0 then outA a b (par v) else outB a b (par v)

/-! ### Finite facts about the outer rule, by `decide` -/

/-- For each parity, the outer rule is a unique sink orientation of the 2-cube. -/
theorem outer_uso :
    ∀ a b a' b' e : Bool, (a, b) ≠ (a', b') →
      (outA a b e ≠ outA a' b' e ∧ a ≠ a') ∨ (outB a b e ≠ outB a' b' e ∧ b ≠ b') := by
  decide

/-- Away from the layer `(0,0)` the outer rule always points along a coordinate
on which the layer has a `1`. -/
theorem outer_own :
    ∀ a b e : Bool, (a, b) ≠ (false, false) →
      (outA a b e = true ∧ a = true) ∨ (outB a b e = true ∧ b = true) := by
  decide

/-- The layer potential: `0` on `(0,0)`; for even parity `1,2,3` on
`(0,1),(1,1),(1,0)`; for odd parity `1,2,3` on `(1,0),(1,1),(0,1)`. -/
def cLayer (a b e : Bool) : Nat :=
  match a, b with
  | false, false => 0
  | true, true => 2
  | false, true => if e then 1 else 3
  | true, false => if e then 3 else 1

/-- Every outer edge either enters the layer `(0,0)` or decreases the layer
potential. -/
theorem outer_decreasing :
    ∀ a b e : Bool,
      (outA a b e = true → ((!a, b) = (false, false) ∨ cLayer (!a) b e < cLayer a b e)) ∧
      (outB a b e = true → ((a, !b) = (false, false) ∨ cLayer a (!b) e < cLayer a b e)) := by
  decide

theorem cLayer_le_three : ∀ a b e : Bool, cLayer a b e ≤ 3 := by decide

theorem cLayer_pos : ∀ a b e : Bool, (a, b) ≠ (false, false) → 1 ≤ cLayer a b e := by decide

/-! ### Component lemmas -/

theorem inner_mk (a b : Bool) (v : V ι) : inner (mk a b v) = v := by
  funext i; rfl

theorem mk_inr0 (a b : Bool) (v : V ι) : mk a b v (Sum.inr 0) = a := by
  simp [mk]

theorem mk_inr1 (a b : Bool) (v : V ι) : mk a b v (Sum.inr 1) = b := by
  simp [mk]

theorem fin2_cases (k : Fin 2) : k = 0 ∨ k = 1 := by
  rcases k with ⟨n, hn⟩
  match n, hn with
  | 0, _ => exact Or.inl rfl
  | 1, _ => exact Or.inr rfl
  | n + 2, h => exact absurd h (by omega)

theorem eq_mk (w : V (ι ⊕ Fin 2)) :
    w = mk (w (Sum.inr 0)) (w (Sum.inr 1)) (inner w) := by
  funext j
  cases j with
  | inl i => rfl
  | inr k =>
    rcases fin2_cases k with rfl | rfl
    · simp [mk]
    · simp [mk]

theorem mk_injective {a b a' b' : Bool} {v v' : V ι} (h : mk a b v = mk a' b' v') :
    a = a' ∧ b = b' ∧ v = v' := by
  refine ⟨?_, ?_, ?_⟩
  · have := congrFun h (Sum.inr 0); simpa [mk] using this
  · have := congrFun h (Sum.inr 1); simpa [mk] using this
  · funext i; exact congrFun h (Sum.inl i)

theorem blow_inl (s : V ι → V ι) (z : V ι) (par : V ι → Bool) (w : V (ι ⊕ Fin 2)) (i : ι) :
    blow s z par w (Sum.inl i) =
      (if w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false then s (xorV (inner w) z)
        else s (inner w)) i := rfl

theorem blow_inr0 (s : V ι → V ι) (z : V ι) (par : V ι → Bool) (w : V (ι ⊕ Fin 2)) :
    blow s z par w (Sum.inr 0) = outA (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w)) := by
  simp [blow]

theorem blow_inr1 (s : V ι → V ι) (z : V ι) (par : V ι → Bool) (w : V (ι ⊕ Fin 2)) :
    blow s z par w (Sum.inr 1) = outB (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w)) := by
  simp [blow]

theorem xor_left_cancel (x y z : Bool) (h : xor x z = xor y z) : x = y := by
  cases x <;> cases y <;> cases z <;> simp_all

theorem xorV_right_injective (v v' z : V ι) (h : xorV v z = xorV v' z) : v = v' := by
  funext i
  exact xor_left_cancel _ _ _ (congrFun h i)

/-! ### The blow-up is a unique sink orientation -/

theorem isUSO_blow (s : V ι → V ι) (hs : IsUSO s) (z : V ι) (par : V ι → Bool) :
    IsUSO (blow s z par) := by
  intro w w' hne
  -- names for the components
  have hw := eq_mk w
  have hw' := eq_mk w'
  generalize ha : w (Sum.inr 0) = a at hw
  generalize hb : w (Sum.inr 1) = b at hw
  generalize hv : inner w = v at hw
  generalize ha' : w' (Sum.inr 0) = a' at hw'
  generalize hb' : w' (Sum.inr 1) = b' at hw'
  generalize hv' : inner w' = v' at hw'
  subst hw; subst hw'
  -- the outmap components at mk
  have i0 : ∀ (x y : Bool) (u : V ι) (i : ι), blow s z par (mk x y u) (Sum.inl i) =
      (if x = false ∧ y = false then s (xorV u z) else s u) i := by
    intro x y u i; rw [blow_inl, mk_inr0, mk_inr1, inner_mk]
  have o0 : ∀ (x y : Bool) (u : V ι), blow s z par (mk x y u) (Sum.inr 0) = outA x y (par u) := by
    intro x y u; rw [blow_inr0, mk_inr0, mk_inr1, inner_mk]
  have o1 : ∀ (x y : Bool) (u : V ι), blow s z par (mk x y u) (Sum.inr 1) = outB x y (par u) := by
    intro x y u; rw [blow_inr1, mk_inr0, mk_inr1, inner_mk]
  by_cases hl : (a, b) = (a', b')
  · -- same layer
    obtain ⟨rfl, rfl⟩ := Prod.mk.inj hl
    have hvv : v ≠ v' := by
      intro h; apply hne; rw [h]
    by_cases h00 : a = false ∧ b = false
    · obtain ⟨i, hi1, hi2⟩ := hs (xorV v z) (xorV v' z)
        (fun h => hvv (xorV_right_injective v v' z h))
      refine ⟨Sum.inl i, ?_, ?_⟩
      · rw [i0, i0, if_pos h00, if_pos h00]; exact hi1
      · show v i ≠ v' i
        intro h; apply hi2; simp [xorV, h]
    · obtain ⟨i, hi1, hi2⟩ := hs v v' hvv
      refine ⟨Sum.inl i, ?_, ?_⟩
      · rw [i0, i0, if_neg h00, if_neg h00]; exact hi1
      · exact hi2
  · -- different layers
    by_cases hvv : v = v'
    · subst hvv
      rcases outer_uso a b a' b' (par v) hl with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · refine ⟨Sum.inr 0, ?_, ?_⟩
        · rw [o0, o0]; exact h1
        · rw [mk_inr0, mk_inr0]; exact h2
      · refine ⟨Sum.inr 1, ?_, ?_⟩
        · rw [o1, o1]; exact h1
        · rw [mk_inr1, mk_inr1]; exact h2
    · by_cases h00 : a = false ∧ b = false
      · -- w lies in the layer (0,0) and w' does not
        obtain ⟨rfl, rfl⟩ := h00
        have hne' : (a', b') ≠ (false, false) := fun h => hl h.symm
        rcases outer_own a' b' (par v') hne' with ⟨h1, h2⟩ | ⟨h1, h2⟩
        · refine ⟨Sum.inr 0, ?_, ?_⟩
          · rw [o0, o0, h1]; simp [outA]
          · rw [mk_inr0, mk_inr0, h2]; simp
        · refine ⟨Sum.inr 1, ?_, ?_⟩
          · rw [o1, o1, h1]; simp [outB]
          · rw [mk_inr1, mk_inr1, h2]; simp
      · by_cases h00' : a' = false ∧ b' = false
        · obtain ⟨rfl, rfl⟩ := h00'
          have hne' : (a, b) ≠ (false, false) := hl
          rcases outer_own a b (par v) hne' with ⟨h1, h2⟩ | ⟨h1, h2⟩
          · refine ⟨Sum.inr 0, ?_, ?_⟩
            · rw [o0, o0, h1]; simp [outA]
            · rw [mk_inr0, mk_inr0, h2]; simp
          · refine ⟨Sum.inr 1, ?_, ?_⟩
            · rw [o1, o1, h1]; simp [outB]
            · rw [mk_inr1, mk_inr1, h2]; simp
        · -- neither layer is (0,0): the inner outmaps are those of s
          obtain ⟨i, hi1, hi2⟩ := hs v v' hvv
          refine ⟨Sum.inl i, ?_, ?_⟩
          · rw [i0, i0, if_neg h00, if_neg h00']; exact hi1
          · exact hi2

/-! ### Flips on the blown-up cube -/

theorem flip_inl_inner (w : V (ι ⊕ Fin 2)) (i : ι) :
    inner (flip w (Sum.inl i)) = flip (inner w) i := by
  funext j
  simp [inner, flip]

theorem flip_inl_inr (w : V (ι ⊕ Fin 2)) (i : ι) (k : Fin 2) :
    flip w (Sum.inl i) (Sum.inr k) = w (Sum.inr k) := by
  simp [flip]

theorem flip_inr_inner (w : V (ι ⊕ Fin 2)) (k : Fin 2) :
    inner (flip w (Sum.inr k)) = inner w := by
  funext j
  simp [inner, flip]

theorem flip_inr_same (w : V (ι ⊕ Fin 2)) (k : Fin 2) :
    flip w (Sum.inr k) (Sum.inr k) = !w (Sum.inr k) := by
  simp [flip]

theorem flip_inr_other (w : V (ι ⊕ Fin 2)) (k k' : Fin 2) (h : k' ≠ k) :
    flip w (Sum.inr k) (Sum.inr k') = w (Sum.inr k') := by
  simp [flip, h]

theorem xorV_flip (v z : V ι) (i : ι) : xorV (flip v i) z = flip (xorV v z) i := by
  funext j
  by_cases hj : j = i
  · subst hj; simp [xorV, flip]
  · simp [xorV, flip, hj]

/-! ### The blow-up is acyclic -/

theorem isAcyclic_blow (s : V ι → V ι) (hs : IsAcyclic s) (z : V ι) (par : V ι → Bool) :
    IsAcyclic (blow s z par) := by
  obtain ⟨r, R, hR, hdec⟩ := hs
  let ρ : V (ι ⊕ Fin 2) → Nat := fun w =>
    if w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false then 4 * r (xorV (inner w) z)
    else 4 * R + 4 + 4 * r (inner w) + cLayer (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w))
  refine ⟨ρ, 8 * R + 7, ?_, ?_⟩
  · intro w
    show (if w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false then 4 * r (xorV (inner w) z)
      else 4 * R + 4 + 4 * r (inner w) + cLayer (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w)))
        ≤ 8 * R + 7
    have h1 := hR (xorV (inner w) z)
    have h2 := hR (inner w)
    have h3 := cLayer_le_three (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w))
    split <;> omega
  · intro w w' ⟨j, hj, hw'⟩
    subst hw'
    show ρ (flip w j) < ρ w
    cases j with
    | inl i =>
      have hin : inner (flip w (Sum.inl i)) = flip (inner w) i := flip_inl_inner w i
      have h0 : flip w (Sum.inl i) (Sum.inr 0) = w (Sum.inr 0) := flip_inl_inr w i 0
      have h1 : flip w (Sum.inl i) (Sum.inr 1) = w (Sum.inr 1) := flip_inl_inr w i 1
      rw [blow_inl] at hj
      by_cases h00 : w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false
      · rw [if_pos h00] at hj
        have hedge : Edge s (xorV (inner w) z) (flip (xorV (inner w) z) i) := ⟨i, hj, rfl⟩
        have := hdec _ _ hedge
        show (if flip w (Sum.inl i) (Sum.inr 0) = false ∧ flip w (Sum.inl i) (Sum.inr 1) = false
            then 4 * r (xorV (inner (flip w (Sum.inl i))) z) else _) < _
        rw [h0, h1, if_pos h00, hin, xorV_flip]
        show 4 * r (flip (xorV (inner w) z) i) <
          (if w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false then 4 * r (xorV (inner w) z) else _)
        rw [if_pos h00]; omega
      · rw [if_neg h00] at hj
        have hedge : Edge s (inner w) (flip (inner w) i) := ⟨i, hj, rfl⟩
        have := hdec _ _ hedge
        have hc := cLayer_le_three (w (Sum.inr 0)) (w (Sum.inr 1)) (par (flip (inner w) i))
        show (if flip w (Sum.inl i) (Sum.inr 0) = false ∧ flip w (Sum.inl i) (Sum.inr 1) = false
            then _ else 4 * R + 4 + 4 * r (inner (flip w (Sum.inl i))) +
              cLayer (flip w (Sum.inl i) (Sum.inr 0)) (flip w (Sum.inl i) (Sum.inr 1))
                (par (inner (flip w (Sum.inl i))))) < _
        rw [h0, h1, if_neg h00, hin]
        show 4 * R + 4 + 4 * r (flip (inner w) i) +
            cLayer (w (Sum.inr 0)) (w (Sum.inr 1)) (par (flip (inner w) i)) <
          (if w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false then _
            else 4 * R + 4 + 4 * r (inner w) +
              cLayer (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w)))
        rw [if_neg h00]; omega
    | inr k =>
      have hin : inner (flip w (Sum.inr k)) = inner w := flip_inr_inner w k
      have hnot00 : ¬ (w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false) := by
        intro h00
        rcases fin2_cases k with rfl | rfl
        · rw [blow_inr0, h00.1, h00.2] at hj; simp [outA] at hj
        · rw [blow_inr1, h00.1, h00.2] at hj; simp [outB] at hj
      have hρw : ρ w = 4 * R + 4 + 4 * r (inner w) +
          cLayer (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w)) := by
        show (if w (Sum.inr 0) = false ∧ w (Sum.inr 1) = false then _ else _) = _
        rw [if_neg hnot00]
      have hbound := hR (xorV (inner w) z)
      rcases fin2_cases k with rfl | rfl
      · rw [blow_inr0] at hj
        have hd := (outer_decreasing (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w))).1 hj
        have e0 : flip w (Sum.inr 0) (Sum.inr 0) = !w (Sum.inr 0) := flip_inr_same w 0
        have e1 : flip w (Sum.inr 0) (Sum.inr 1) = w (Sum.inr 1) :=
          flip_inr_other w 0 1 (by decide)
        show (if flip w (Sum.inr 0) (Sum.inr 0) = false ∧ flip w (Sum.inr 0) (Sum.inr 1) = false
            then 4 * r (xorV (inner (flip w (Sum.inr 0))) z)
            else 4 * R + 4 + 4 * r (inner (flip w (Sum.inr 0))) +
              cLayer (flip w (Sum.inr 0) (Sum.inr 0)) (flip w (Sum.inr 0) (Sum.inr 1))
                (par (inner (flip w (Sum.inr 0))))) < ρ w
        rw [e0, e1, hin, hρw]
        by_cases hh : (!w (Sum.inr 0)) = false ∧ w (Sum.inr 1) = false
        · rw [if_pos hh]
          have h4 : 4 * r (xorV (inner w) z) ≤ 4 * R := Nat.mul_le_mul_left 4 hbound
          exact Nat.lt_of_le_of_lt h4 (by omega)
        · rw [if_neg hh]
          rcases hd with h00' | hlt
          · exact absurd (Prod.mk.inj h00') hh
          · omega
      · rw [blow_inr1] at hj
        have hd := (outer_decreasing (w (Sum.inr 0)) (w (Sum.inr 1)) (par (inner w))).2 hj
        have e0 : flip w (Sum.inr 1) (Sum.inr 0) = w (Sum.inr 0) :=
          flip_inr_other w 1 0 (by decide)
        have e1 : flip w (Sum.inr 1) (Sum.inr 1) = !w (Sum.inr 1) := flip_inr_same w 1
        show (if flip w (Sum.inr 1) (Sum.inr 0) = false ∧ flip w (Sum.inr 1) (Sum.inr 1) = false
            then 4 * r (xorV (inner (flip w (Sum.inr 1))) z)
            else 4 * R + 4 + 4 * r (inner (flip w (Sum.inr 1))) +
              cLayer (flip w (Sum.inr 1) (Sum.inr 0)) (flip w (Sum.inr 1) (Sum.inr 1))
                (par (inner (flip w (Sum.inr 1))))) < ρ w
        rw [e0, e1, hin, hρw]
        by_cases hh : w (Sum.inr 0) = false ∧ (!w (Sum.inr 1)) = false
        · rw [if_pos hh]
          have h4 : 4 * r (xorV (inner w) z) ≤ 4 * R := Nat.mul_le_mul_left 4 hbound
          exact Nat.lt_of_le_of_lt h4 (by omega)
        · rw [if_neg hh]
          rcases hd with h00' | hlt
          · exact absurd (Prod.mk.inj h00') hh
          · omega

/-! ### The bottom-antipodal walk of the blow-up -/

/-- `iter f n x = f (f (⋯ (f x)))`, `n` times. -/
def iter {α : Type _} (f : α → α) : Nat → α → α
  | 0, x => x
  | n + 1, x => f (iter f n x)

theorem iter_succ {α : Type _} (f : α → α) (n : Nat) (x : α) :
    iter f (n + 1) x = f (iter f n x) := rfl

theorem iter_add {α : Type _} (f : α → α) (m n : Nat) (x : α) :
    iter f (m + n) x = iter f n (iter f m x) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Nat.add_succ, iter_succ, iter_succ, ih]

theorem xorV_cancel_right (y z : V ι) : xorV (xorV y z) z = y := by
  funext i; simp only [xorV]; cases y i <;> cases z i <;> rfl

theorem xorV_cancel_left (o u : V ι) : xorV o (xorV o u) = u := by
  funext i; simp only [xorV]; cases o i <;> cases u i <;> rfl

theorem xorV_xor_left (u o : V ι) : xorV u (xorV o u) = o := by
  funext i; simp only [xorV]; cases o i <;> cases u i <;> rfl

theorem xorV_swap (y z w : V ι) : xorV (xorV y z) w = xorV (xorV y w) z := by
  funext i; simp only [xorV]; cases y i <;> cases z i <;> cases w i <;> rfl

theorem xorV_zeroV (v : V ι) : xorV v zeroV = v := by
  funext i; simp only [xorV, zeroV]; cases v i <;> rfl

theorem ba_blow_mk (s : V ι → V ι) (z : V ι) (par : V ι → Bool) (a b : Bool) (v : V ι) :
    ba (blow s z par) (mk a b v) =
      mk (xor a (outA a b (par v))) (xor b (outB a b (par v)))
        (xorV v (if a = false ∧ b = false then s (xorV v z) else s v)) := by
  funext j
  cases j with
  | inl i =>
    show xor (mk a b v (Sum.inl i)) (blow s z par (mk a b v) (Sum.inl i)) = _
    rw [blow_inl, mk_inr0, mk_inr1, inner_mk]
    rfl
  | inr k =>
    rcases fin2_cases k with rfl | rfl
    · show xor (mk a b v (Sum.inr 0)) (blow s z par (mk a b v) (Sum.inr 0)) = _
      rw [blow_inr0, mk_inr0, mk_inr1, inner_mk, mk_inr0]
    · show xor (mk a b v (Sum.inr 1)) (blow s z par (mk a b v) (Sum.inr 1)) = _
      rw [blow_inr1, mk_inr0, mk_inr1, inner_mk, mk_inr1]

theorem outer_step : ∀ e : Bool, xor e (outA e (!e) e) = !e ∧ xor (!e) (outB e (!e) e) = e := by
  decide

theorem not_layer00 : ∀ e : Bool, ¬ (e = false ∧ (!e) = false) := by decide

/-- The parity flag of a height function. -/
def parOf (h : V ι → Nat) : V ι → Bool := fun v => decide (h v % 2 = 0)

/-- The starting vertex of the long walk. -/
def startOf (h : V ι → Nat) (u : V ι) : V (ι ⊕ Fin 2) :=
  if h u % 2 = 0 then mk true false u else mk false true u

theorem Height.ne_sink_of_pos {s : V ι → V ι} {o : V ι} {h : V ι → Nat} (hH : Height s o h)
    {v : V ι} (hv : 1 ≤ h v) : v ≠ o := by
  intro hvo; rw [hvo, hH.h_sink] at hv; omega

theorem Height.eq_sink_of_zero {s : V ι → V ι} {o : V ι} {h : V ι → Nat} (hH : Height s o h)
    {v : V ι} (hv : h v = 0) : v = o := by
  cases Classical.em (v = o) with
  | inl hvo => exact hvo
  | inr hne => have := hH.step v hne; omega

theorem Height.iter_height {s : V ι → V ι} {o : V ι} {h : V ι → Nat} (hH : Height s o h)
    (u : V ι) : ∀ t, t ≤ h u → h (iter (ba s) t u) = h u - t := by
  intro t
  induction t with
  | zero => intro _; rfl
  | succ t ih =>
    intro ht
    have hy := ih (by omega)
    have hne : iter (ba s) t u ≠ o := hH.ne_sink_of_pos (by omega)
    have := hH.step _ hne
    rw [iter_succ]; omega

/-- Phase one: for `t ≤ h u` the walk sits on the layers `(1,0)` and `(0,1)`,
alternating with the parity of the inner height, and its inner part is the
walk of `s`. -/
theorem phase_one {s : V ι → V ι} {o u : V ι} {h : V ι → Nat} (hH : Height s o h) :
    ∀ t, t ≤ h u →
      iter (ba (blow s (xorV o u) (parOf h))) t (startOf h u) =
        mk (decide ((h u - t) % 2 = 0)) (!decide ((h u - t) % 2 = 0)) (iter (ba s) t u) := by
  intro t
  induction t with
  | zero =>
    intro _
    show startOf h u = _
    unfold startOf
    by_cases hp : h u % 2 = 0
    · rw [if_pos hp]; simp [hp, iter]
    · rw [if_neg hp]; simp [hp, iter]
  | succ t ih =>
    intro ht
    have hy := hH.iter_height u t (by omega)
    rw [iter_succ, ih (by omega), ba_blow_mk]
    have hpar : parOf h (iter (ba s) t u) = decide ((h u - t) % 2 = 0) := by
      unfold parOf; rw [hy]
    rw [hpar]
    have hnext : decide ((h u - (t + 1)) % 2 = 0) = !decide ((h u - t) % 2 = 0) := by
      by_cases hp : (h u - t) % 2 = 0
      · have h1 : (h u - (t + 1)) % 2 = 1 := by omega
        simp [hp, h1]
      · have h1 : (h u - (t + 1)) % 2 = 0 := by omega
        simp [hp, h1]
    rw [hnext]
    obtain ⟨e1, e2⟩ := outer_step (decide ((h u - t) % 2 = 0))
    rw [e1, e2, if_neg (not_layer00 _), Bool.not_not]
    rfl

/-- The two transition steps. -/
theorem phase_mid {s : V ι → V ι} {o u : V ι} {h : V ι → Nat} (hH : Height s o h) :
    iter (ba (blow s (xorV o u) (parOf h))) (h u + 2) (startOf h u) = mk false false o := by
  have hP := phase_one hH (h u) (Nat.le_refl _)
  have ho : iter (ba s) (h u) u = o :=
    hH.eq_sink_of_zero (by rw [hH.iter_height u (h u) (Nat.le_refl _)]; omega)
  rw [ho, Nat.sub_self] at hP
  have hpo : parOf h o = true := by unfold parOf; rw [hH.h_sink]; rfl
  have h0 : decide (0 % 2 = 0) = true := rfl
  have step1 : iter (ba (blow s (xorV o u) (parOf h))) (h u + 1) (startOf h u) =
      mk false true o := by
    rw [iter_succ, hP, ba_blow_mk, hpo, hH.sink, h0, if_neg (by decide), xorV_zeroV]
    rfl
  rw [iter_succ, step1, ba_blow_mk, hpo, hH.sink, if_neg (by decide), xorV_zeroV]
  rfl

/-- Phase two: on the layer `(0,0)` the walk is the walk of `s` from `u`,
seen through the translation. -/
theorem phase_two {s : V ι → V ι} {o u : V ι} {h : V ι → Nat} (hH : Height s o h) :
    ∀ t, t ≤ h u →
      iter (ba (blow s (xorV o u) (parOf h))) (h u + 2 + t) (startOf h u) =
        mk false false (xorV (iter (ba s) t u) (xorV o u)) := by
  intro t
  induction t with
  | zero =>
    intro _
    rw [Nat.add_zero, phase_mid hH]
    show mk false false o = mk false false (xorV u (xorV o u))
    rw [xorV_xor_left]
  | succ t ih =>
    intro ht
    rw [Nat.add_succ, iter_succ, ih (by omega), ba_blow_mk, if_pos ⟨rfl, rfl⟩,
      xorV_cancel_right]
    show mk false false (xorV (xorV (iter (ba s) t u) (xorV o u)) (s (iter (ba s) t u))) = _
    rw [xorV_swap]
    rfl

/-- **The walk theorem.** From `startOf h u` the bottom-antipodal walk of the
blow-up reaches `(0,0,u)` after exactly `2 h u + 2` steps and not before. -/
theorem walk_blow {s : V ι → V ι} {o u : V ι} {h : V ι → Nat} (hH : Height s o h) :
    iter (ba (blow s (xorV o u) (parOf h))) (2 * h u + 2) (startOf h u) = mk false false u ∧
    ∀ t, t < 2 * h u + 2 →
      iter (ba (blow s (xorV o u) (parOf h))) t (startOf h u) ≠ mk false false u := by
  constructor
  · have e : 2 * h u + 2 = h u + 2 + h u := by omega
    rw [e, phase_two hH (h u) (Nat.le_refl _)]
    have ho : iter (ba s) (h u) u = o :=
      hH.eq_sink_of_zero (by rw [hH.iter_height u (h u) (Nat.le_refl _)]; omega)
    rw [ho, xorV_cancel_left]
  · intro t ht heq
    by_cases h1 : t ≤ h u
    · rw [phase_one hH t h1] at heq
      obtain ⟨ha, hb, _⟩ := mk_injective heq
      rw [ha] at hb
      exact absurd hb (by decide)
    · by_cases h2 : t = h u + 1
      · subst h2
        have hP := phase_one hH (h u) (Nat.le_refl _)
        have ho : iter (ba s) (h u) u = o :=
          hH.eq_sink_of_zero (by rw [hH.iter_height u (h u) (Nat.le_refl _)]; omega)
        rw [ho, Nat.sub_self] at hP
        have hpo : parOf h o = true := by unfold parOf; rw [hH.h_sink]; rfl
        have h0 : decide (0 % 2 = 0) = true := rfl
        rw [iter_succ, hP, ba_blow_mk, hpo, hH.sink, h0, if_neg (by decide), xorV_zeroV] at heq
        obtain ⟨_, hb, _⟩ := mk_injective heq
        exact absurd hb (by decide)
      · obtain ⟨t', rfl⟩ : ∃ t', t = h u + 2 + t' := ⟨t - (h u + 2), by omega⟩
        have ht' : t' < h u := by omega
        rw [phase_two hH t' (by omega)] at heq
        obtain ⟨_, _, hv⟩ := mk_injective heq
        have hy : iter (ba s) t' u = o := by
          have h3 : xorV (xorV (iter (ba s) t' u) (xorV o u)) (xorV o u) = xorV u (xorV o u) :=
            congrArg (fun w => xorV w (xorV o u)) hv
          rw [xorV_cancel_right, xorV_xor_left] at h3
          exact h3
        have := hH.iter_height u t' (by omega)
        rw [hy, hH.h_sink] at this
        omega

end SSGProof.Cube
