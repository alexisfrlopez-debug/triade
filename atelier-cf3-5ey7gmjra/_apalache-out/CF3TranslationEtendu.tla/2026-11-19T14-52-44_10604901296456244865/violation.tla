---------------------------- MODULE counterexample ----------------------------

EXTENDS CF3TranslationEtendu

(* Constant initialization state *)
ConstInit == KUser = "K_user" /\ SPiege = "S_piege" /\ SSerrure = "S_serrure"

(* Initial state [_transition(0)] *)
State0 ==
  KUser = "K_user"
    /\ SPiege = "S_piege"
    /\ SSerrure = "S_serrure"
    /\ accepte = FALSE
    /\ cf2_ok = FALSE
    /\ delta = 1
    /\ destr_injuste = FALSE
    /\ detruit = FALSE
    /\ e = 3
    /\ media_corrompu = FALSE
    /\ phase = "brouillon"
    /\ sait = {}
    /\ secret = FALSE
    /\ taccepte = FALSE
    /\ tcf2_ok = FALSE
    /\ tdestr_injuste = FALSE
    /\ tdetruit = FALSE
    /\ te = 4
    /\ tmedia_corrompu = FALSE
    /\ tphase = "brouillon"
    /\ trap_ok = TRUE
    /\ tsait = {}
    /\ tsecret = FALSE
    /\ ttrap_ok = TRUE

(* State1 [_transition(0)] *)
State1 ==
  KUser = "K_user"
    /\ SPiege = "S_piege"
    /\ SSerrure = "S_serrure"
    /\ accepte = FALSE
    /\ cf2_ok = FALSE
    /\ delta = 1
    /\ destr_injuste = FALSE
    /\ detruit = FALSE
    /\ e = 3
    /\ media_corrompu = FALSE
    /\ phase = "canonique"
    /\ sait = {}
    /\ secret = FALSE
    /\ taccepte = FALSE
    /\ tcf2_ok = FALSE
    /\ tdestr_injuste = FALSE
    /\ tdetruit = FALSE
    /\ te = 3
    /\ tmedia_corrompu = FALSE
    /\ tphase = "canonique"
    /\ trap_ok = TRUE
    /\ tsait = {}
    /\ tsecret = FALSE
    /\ ttrap_ok = TRUE

(* The following formula holds true in the last state and violates the invariant *)
InvariantViolation == ~(te = e + delta)

================================================================================
(* Created by Apalache on Thu Nov 19 14:52:53 UTC 2026 *)
(* https://github.com/apalache-mc/apalache *)
