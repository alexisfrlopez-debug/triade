---------------------------- MODULE counterexample ----------------------------

EXTENDS CF3O3

(* Constant initialization state *)
ConstInit == KUser = "K_user" /\ SPiege = "S_piege" /\ SSerrure = "S_serrure"

(* Initial state [_transition(0)] *)
State0 ==
  KUser = "K_user"
    /\ SPiege = "S_piege"
    /\ SSerrure = "S_serrure"
    /\ accepte = FALSE
    /\ cf2_ok = TRUE
    /\ destr_injuste = FALSE
    /\ detruit = FALSE
    /\ e = 0
    /\ media_corrompu = FALSE
    /\ phase = "canonique"
    /\ sait = { "S_piege", "S_serrure" }
    /\ secret = FALSE
    /\ trap_ok = FALSE

(* The following formula holds true in the last state and violates the invariant *)
InvariantViolation ==
  ~((IF e = 1 THEN 1 ELSE IF e >= 2 THEN 2 ELSE 0) \in { 1, 2 })

================================================================================
(* Created by Apalache on Thu Nov 19 14:52:52 UTC 2026 *)
(* https://github.com/apalache-mc/apalache *)
