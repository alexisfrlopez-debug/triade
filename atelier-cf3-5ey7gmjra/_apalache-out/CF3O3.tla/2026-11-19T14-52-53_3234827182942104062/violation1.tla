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
    /\ e = 1
    /\ media_corrompu = FALSE
    /\ phase = "canonique"
    /\ sait = { "S_piege", "S_serrure" }
    /\ secret = TRUE
    /\ trap_ok = FALSE

(* The following formula holds true in the last state and violates the invariant *)
InvariantViolation == ~(secret = FALSE) /\ ~(Cardinality(sait) = 3)

================================================================================
(* Created by Apalache on Thu Nov 19 14:52:56 UTC 2026 *)
(* https://github.com/apalache-mc/apalache *)
