---------------------------- MODULE counterexample ----------------------------

EXTENDS CF3EquivControlesEtendu

(* Constant initialization state *)
ConstInit == KUser = "K_user" /\ SPiege = "S_piege" /\ SSerrure = "S_serrure"

(* Initial state [_transition(0)] *)
State0 ==
  KUser = "K_user"
    /\ SPiege = "S_piege"
    /\ SSerrure = "S_serrure"
    /\ accepte = FALSE
    /\ accepteP = FALSE
    /\ accepteR = FALSE
    /\ cf2P = FALSE
    /\ cf2R = FALSE
    /\ cf2_ok = FALSE
    /\ destr_injuste = FALSE
    /\ detruit = FALSE
    /\ detruitP = FALSE
    /\ detruitR = FALSE
    /\ e = 0
    /\ eP = 0
    /\ eR = 0
    /\ injusteP = FALSE
    /\ injusteR = FALSE
    /\ marque = FALSE
    /\ mediaP = FALSE
    /\ mediaR = FALSE
    /\ media_corrompu = FALSE
    /\ phase = "canonique"
    /\ phaseP = "canonique"
    /\ phaseR = "canonique"
    /\ sait = {}
    /\ saitP = {}
    /\ saitR = {}
    /\ secret = FALSE
    /\ secretP = FALSE
    /\ secretR = FALSE
    /\ trapP = FALSE
    /\ trapR = FALSE
    /\ trap_ok = FALSE

(* State1 [_transition(0)] *)
State1 ==
  KUser = "K_user"
    /\ SPiege = "S_piege"
    /\ SSerrure = "S_serrure"
    /\ accepte = FALSE
    /\ accepteP = FALSE
    /\ accepteR = FALSE
    /\ cf2P = FALSE
    /\ cf2R = FALSE
    /\ cf2_ok = FALSE
    /\ destr_injuste = FALSE
    /\ detruit = FALSE
    /\ detruitP = FALSE
    /\ detruitR = FALSE
    /\ e = 0
    /\ eP = 0
    /\ eR = 0
    /\ injusteP = FALSE
    /\ injusteR = FALSE
    /\ marque = FALSE
    /\ mediaP = FALSE
    /\ mediaR = FALSE
    /\ media_corrompu = FALSE
    /\ phase = "canonique"
    /\ phaseP = "canonique"
    /\ phaseR = "canonique"
    /\ sait = {}
    /\ saitP = {}
    /\ saitR = {"S_serrure"}
    /\ secret = FALSE
    /\ secretP = FALSE
    /\ secretR = FALSE
    /\ trapP = FALSE
    /\ trapR = FALSE
    /\ trap_ok = FALSE

(* The following formula holds true in the last state and violates the invariant *)
InvariantViolation == ~(saitR = saitP)

================================================================================
(* Created by Apalache on Thu Nov 19 14:50:57 UTC 2026 *)
(* https://github.com/apalache-mc/apalache *)
