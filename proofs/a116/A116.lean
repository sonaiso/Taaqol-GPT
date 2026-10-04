import Std

/-!
Candidate formal proof, not a Taaqol runtime admission or Arabic licence.
Source: Saleh1967/Alghanem@5bcd8ffdf0f288e5df54064b4efc3423269733cc
src/alghanem/arabic/a116_bridge_licence.py: SyllableState, step.
The carrier order is the source order (hamza LAST).
-/
namespace A116

def carriers : List Char := "ابتثجحخدذرزسشصضطظعغفقكلمنهويء".toList
abbrev Carrier := Fin carriers.length

inductive Mark where
  | fatha | damma | kasra | sukun
  deriving DecidableEq, Repr

def marks : List Mark := [.fatha, .damma, .kasra, .sukun]
abbrev Atom := Carrier × Mark

def atoms : List Atom := (List.finRange carriers.length).flatMap
  (fun c => marks.map (fun h => (c, h)))

inductive Q where
  | waiting | vowelled | rejected
  deriving DecidableEq, Repr

def states : List Q := [.waiting, .vowelled, .rejected]
def q0 : Q := .waiting

def delta (q : Q) (a : Atom) : Q :=
  match q, a.2 with
  | .rejected, _ => .rejected
  | .waiting, .sukun => .rejected
  | .waiting, _ => .vowelled
  | .vowelled, .sukun => .waiting
  | .vowelled, _ => .vowelled

def run : Q → List Atom → Q
  | q, [] => q
  | q, a :: rest => run (delta q a) rest

def Safe (q : Q) : Prop := q ≠ .rejected

/- A separate syntactic specification: a sukun requires a previous vowel.
At the start needVowel=true. Carrier identity is deliberately not consulted.
This is a model language, not an Arabic grammar. -/
def LegalSuffix : Bool → List Atom → Prop
  | _, [] => True
  | needVowel, a :: rest =>
    if a.2 = .sukun then needVowel = false ∧ LegalSuffix true rest
    else LegalSuffix false rest

def Admissible (w : List Atom) : Prop := LegalSuffix true w

theorem carrier_count : carriers.length = 29 := by decide
theorem carrier_unique : carriers.Nodup := by decide
theorem atom_count : atoms.length = 116 := by decide
theorem atom_unique : atoms.Nodup := by decide
theorem transition_count : states.length * atoms.length = 348 := by decide

theorem every_atom_listed (a : Atom) : a ∈ atoms := by
  obtain ⟨c, h⟩ := a
  cases h <;> simp [atoms, marks]

theorem every_state_listed (q : Q) : q ∈ states := by
  cases q <;> simp [states]

theorem rejected_absorbing (w : List Atom) : run .rejected w = .rejected := by
  induction w with
  | nil => rfl
  | cons a rest ih => simpa [run, delta] using ih

/- The main theorem is about non-rejection, not merely the codomain of run. -/
theorem exact_safety (q : Q) (w : List Atom) :
    Safe (run q w) ↔ Safe q ∧ LegalSuffix (q == .waiting) w := by
  induction w generalizing q with
  | nil => simp [run, LegalSuffix]
  | cons a rest ih =>
    obtain ⟨c, h⟩ := a
    cases q <;> cases h <;>
      simp [run, delta, ih, Safe, LegalSuffix]

theorem safe_iff_admissible (w : List Atom) :
    Safe (run q0 w) ↔ Admissible w := by
  simpa [q0, Safe, Admissible] using exact_safety .waiting w

theorem all_lengths_safe (w : List Atom) (h : Admissible w) :
    Safe (run q0 w) := (safe_iff_admissible w).mpr h

def v : Atom := (⟨0, by decide⟩, .fatha)
def k : Atom := (⟨0, by decide⟩, .sukun)

theorem initial_sukun_rejected : run q0 [k] = .rejected := by decide
theorem double_sukun_rejected : run q0 [v, k, k] = .rejected := by decide
theorem nonempty_safe_witness : Safe (run q0 [v, k, v]) := by decide
theorem not_every_word_safe : ¬ (∀ w : List Atom, Safe (run q0 w)) := by
  intro h
  exact h [k] initial_sukun_rejected

/- This finite saturation includes rejected; it is NOT Safe. -/
def r0 : List Q := [.waiting]
def grow (qs : List Q) : List Q :=
  (qs ++ qs.flatMap (fun q => atoms.map (delta q))).eraseDups
def r1 : List Q := grow r0

theorem first_saturation : r1 = states := by decide
theorem fixed_point : grow r1 = r1 := by decide
theorem reachable_in_one (q : Q) :
    ∃ w : List Atom, w.length ≤ 1 ∧ run q0 w = q := by
  cases q with
  | waiting => exact ⟨[], by decide, rfl⟩
  | vowelled => exact ⟨[v], by decide, rfl⟩
  | rejected => exact ⟨[k], by decide, rfl⟩

theorem closed_transitions (q : Q) (a : Atom) : delta q a ∈ r1 := by
  rw [first_saturation]
  exact every_state_listed (delta q a)

theorem run_append (q : Q) (w z : List Atom) :
    run q (w ++ z) = run (run q w) z := by
  induction w generalizing q with
  | nil => rfl
  | cons a rest ih => simpa [run] using ih (delta q a)

theorem all_lengths_in_fixpoint (q : Q) (w : List Atom) (hq : q ∈ r1) :
    run q w ∈ r1 := by
  induction w generalizing q with
  | nil => exact hq
  | cons a rest ih => exact ih (delta q a) (closed_transitions q a)

theorem fixpoint_not_safe : ¬ (∀ q, q ∈ r1 → Safe q) := by
  intro h
  have hr : Q.rejected ∈ r1 := by rw [first_saturation]; decide
  exact h .rejected hr rfl

/- Explicitly expose the limit: the model accepts a vowelled alif seat. -/
theorem alif_fatha_model_safe : Safe (run q0 [v]) := by decide

#print axioms carrier_count
#print axioms carrier_unique
#print axioms atom_count
#print axioms atom_unique
#print axioms transition_count
#print axioms every_atom_listed
#print axioms exact_safety
#print axioms safe_iff_admissible
#print axioms all_lengths_safe
#print axioms not_every_word_safe
#print axioms first_saturation
#print axioms fixed_point
#print axioms reachable_in_one
#print axioms all_lengths_in_fixpoint
#print axioms fixpoint_not_safe
#print axioms alif_fatha_model_safe

end A116
