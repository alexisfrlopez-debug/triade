---------------------------- MODULE counterexample ----------------------------

EXTENDS CF3EtenduDebordant

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
    /\ e = 2
    /\ media_corrompu = FALSE
    /\ phase = "brouillon"
    /\ sait = { "K_user", "S_piege", "S_serrure" }
    /\ secret = TRUE
    /\ trap_ok = TRUE

(* State1 [_transition(8)] *)
State1 ==
  KUser = "K_user"
    /\ SPiege = "S_piege"
    /\ SSerrure = "S_serrure"
    /\ accepte = FALSE
    /\ cf2_ok = TRUE
    /\ destr_injuste = FALSE
    /\ detruit = TRUE
    /\ e = 2
    /\ media_corrompu = TRUE
    /\ phase = "brouillon"
    /\ sait = { "K_user", "S_piege", "S_serrure" }
    /\ secret = TRUE
    /\ trap_ok = TRUE

(* The following formula holds true in the last state and violates the invariant *)
InvariantViolation == ~(media_corrompu = FALSE)

================================================================================
(* Created by Apalache on Thu Nov 19 14:52:39 UTC 2026 *)
(* https://github.com/apalache-mc/apalache *)
