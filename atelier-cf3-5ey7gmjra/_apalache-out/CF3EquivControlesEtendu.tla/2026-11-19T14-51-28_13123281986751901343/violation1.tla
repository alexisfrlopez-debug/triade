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
    /\ trapP = TRUE
    /\ trapR = TRUE
    /\ trap_ok = TRUE

(* The following formula holds true in the last state and violates the invariant *)
InvariantViolation ==
  ~((phase = "canonique"
    /\ trap_ok
    /\ "K_user" \in sait
    /\ Cardinality({
      t_e_1 \in sait:
        t_e_1 \in { "K_user", "S_serrure", "S_piege" }
    })
      >= 3)
    = (trap_ok
      /\ phase = "canonique"
      /\ (~("K_user" \in sait) \/ ("K_user" \in sait /\ Cardinality(sait) >= 3))))

================================================================================
(* Created by Apalache on Thu Nov 19 14:51:40 UTC 2026 *)
(* https://github.com/apalache-mc/apalache *)
