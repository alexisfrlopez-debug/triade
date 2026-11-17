--------------------------- MODULE CF3 ---------------------------
(***************************************************************************
 * CF3 — LA SÉMANTIQUE OPÉRATIONNELLE DU COFFRE EN TLA+ (l'instruction
 * 6zqo2h60n : « Encode la sémantique opérationnelle du coffre CF3
 * (13 règles, état d'époque non borné) dans TLA+ et décharge l'invariant
 * I (I1–I4) par Apalache (SMT, entiers non bornés) »).
 *
 * LE PORTAGE — la source de vérité : scripts/preuves_v150/
 * modele_invariant_v150.py (v0.15.0), lui-même le portage fidèle de
 * l'explorateur D187 (154 états / 1 152 transitions aux bornes
 * historiques). Les 13 règles ci-dessous sont la copie règle à règle de
 * actions_possibles/appliquer — l'époque y est lue UNIQUEMENT par le
 * prédicat e > 1 (la classe ≥ 2) et l'opération successeur e + 1 (la
 * clôture) : l'AUDIT MÉCANIQUE (audit_regles.py) le vérifie sur les
 * gardes/actions, pas sur les témoins par translation.
 *
 * L'ÉPOQUE EST NON BORNÉE : e \in Int (Apalache, SMT) — la clôture fait
 * e' = e + 1 SANS plafond. Le plafond v120 (e <- min(e+1, EpoquesMax)),
 * artefact de l'époque D187, vit dans CF3Plafond.tla — UNIQUEMENT pour
 * le contrôle de fidélité (reproduction des comptes bornés).
 *
 * L'INVARIANT INDUCTIF I : I1 secret ⟹ seuil atteint (les TROIS
 * éléments) ; I2 pas de destruction injuste ; I3 CF2 et média intacts ;
 * I4 époque ≥ 1. Inv inclut TypeOK : la preuve d'inductivité
 * (Apalache --init=Inv) porte sur les états BIEN TYPÉS seulement.
 ***************************************************************************)

EXTENDS Integers, FiniteSets

CONSTANTS
  \* @type: Str;
  KUser,       (* l'élément utilisateur : la phrase *)
  \* @type: Str;
  SSerrure,    (* l'élément serrure : la moitié du conteneur *)
  \* @type: Str;
  SPiege       (* l'élément piège : la moitié du média *)

Elements == {KUser, SSerrure, SPiege}

VARIABLES
  \* @type: Int;
  e,              (* l'époque — NON bornée : la non-bornitude vécue *)
  \* @type: Str;
  phase,          (* "canonique" | "brouillon" *)
  \* @type: Set(Str);
  sait,           (* les éléments volés par l'adversaire, \in SUBSET Elements *)
  \* @type: Bool;
  trap_ok,        (* le piège PRÉSENT et INTÈGRE (le tag) *)
  \* @type: Bool;
  cf2_ok,         (* les fragments CF2 intacts *)
  \* @type: Bool;
  secret,         (* le secret appris — exige le seuil 3 *)
  \* @type: Bool;
  accepte,        (* un rejeu accepté — P2 : JAMAIS *)
  \* @type: Bool;
  detruit,        (* la destruction LOCALE (PV unique) *)
  \* @type: Bool;
  destr_injuste,  (* la destruction INJUSTE — P3 : JAMAIS *)
  \* @type: Bool;
  media_corrompu  (* le média du piège touché — P4 : JAMAIS *)

vars == <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit,
          destr_injuste, media_corrompu>>

TypeOK ==
  /\ e \in Int
  /\ phase \in {"canonique", "brouillon"}
  /\ sait \in SUBSET Elements
  /\ trap_ok \in BOOLEAN
  /\ cf2_ok \in BOOLEAN
  /\ secret \in BOOLEAN
  /\ accepte \in BOOLEAN
  /\ detruit \in BOOLEAN
  /\ destr_injuste \in BOOLEAN
  /\ media_corrompu \in BOOLEAN

Init ==
  /\ e = 1
  /\ phase = "canonique"
  /\ sait = {}
  /\ trap_ok = TRUE
  /\ cf2_ok = TRUE
  /\ secret = FALSE
  /\ accepte = FALSE
  /\ detruit = FALSE
  /\ destr_injuste = FALSE
  /\ media_corrompu = FALSE

(***************************************************************************
 * LES 13 RÈGLES — règle à règle depuis modele_invariant_v150.py.
 * L'audit mécanique : toute occurrence de l'époque dans une garde ou
 * action ci-dessous est de la forme e > 1 (le prédicat de classe ≥ 2)
 * ou e + 1 (le successeur de la clôture) — RIEN d'autre.
 ***************************************************************************)

(* 1-3 : L'ADVERSAIRE VOLE UN ÉLÉMENT — toujours possibles *)
VoleKUser ==
  /\ sait' = sait \union {KUser}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

VoleSSerrure ==
  /\ sait' = sait \union {SSerrure}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

VoleSPiege ==
  /\ sait' = sait \union {SPiege}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

(* 4 : LA FALSIFICATION DU CONTENEUR — la PREUVE exige le piège intègre
 *     et l'état canonique : destruction LOCALE (PV), le média INTACT *)
FalsifieConteneur ==
  /\ trap_ok
  /\ phase = "canonique"
  /\ detruit' = TRUE
  /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte,
                 destr_injuste, media_corrompu>>

(* 5 : LA FALSIFICATION DU PIÈGE — le tag invalide : refus SANS
 *     destruction, le piège devient indisponible (pour toujours) *)
FalsifiePiege ==
  /\ trap_ok
  /\ trap_ok' = FALSE
  /\ UNCHANGED <<e, phase, sait, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

(* 6 : LE REJEU D'ÉPOQUE PASSÉE — l'adversaire restaure un couple
 *     ancien : REFUS NOMMÉ, l'état INCHANGÉ (garde : e > 1) *)
RejoueEpoquePassee ==
  /\ e > 1
  /\ UNCHANGED vars

(* 7 : L'OUVERTURE CORRECTE — trois cas : l'honnête (rien volé : le
 *     brouillon s'ouvre), le seuil atteint (les TROIS éléments : le
 *     secret est appris), le REFUS (K_user volé seul : le KEK
 *     indérivable — la règle n'est pas possible) *)
OuvrirCorrect ==
  /\ trap_ok
  /\ phase = "canonique"
  /\ \/ /\ KUser \notin sait
        /\ phase' = "brouillon"
        /\ secret' = secret
     \/ /\ KUser \in sait
        /\ Cardinality(sait) >= 3
        /\ phase' = "brouillon"
        /\ secret' = TRUE
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, accepte, detruit,
                 destr_injuste, media_corrompu>>

(* 8 : L'OUVERTURE PHRASE ERRONÉE — BÉNIGNE, l'état inchangé *)
OuvrirPhraseErronee ==
  /\ phase = "canonique"
  /\ UNCHANGED vars

(* 9 : L'OUVERTURE DE L'ANCIEN COUPLE (le rejeu A4) — refus « RETOUR
 *     EN ARRIÈRE », l'état inchangé (garde : e > 1) *)
OuvrirAncienCouple ==
  /\ phase = "canonique"
  /\ e > 1
  /\ UNCHANGED vars

(* 10 : LA VÉRIFICATION — le verdict VERT, l'état inchangé *)
Verifier ==
  /\ phase = "canonique"
  /\ UNCHANGED vars

(* 11 : LE CRASH DE SESSION — le brouillon meurt, le canonique revient
 *      (l'époque ne bouge pas) *)
CrashPendantSession ==
  /\ phase' = "canonique"
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

(* 12 : LA CLÔTURE CORRECTE — époque + 1 SANS PLAFOND (le modèle de
 *      l'implémentation : « epoque2 = epoque_n + 1 ») *)
CloturerCorrecte ==
  /\ phase = "brouillon"
  /\ trap_ok
  /\ e' = e + 1
  /\ phase' = "canonique"
  /\ UNCHANGED <<sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

(* 13 : LA CLÔTURE PHRASE ERRONÉE — AUCUN scellement, l'état inchangé *)
CloturerPhraseErronee ==
  /\ phase = "brouillon"
  /\ UNCHANGED vars

Next ==
  \/ VoleKUser
  \/ VoleSSerrure
  \/ VoleSPiege
  \/ FalsifieConteneur
  \/ FalsifiePiege
  \/ RejoueEpoquePassee
  \/ OuvrirCorrect
  \/ OuvrirPhraseErronee
  \/ OuvrirAncienCouple
  \/ Verifier
  \/ CrashPendantSession
  \/ CloturerCorrecte
  \/ CloturerPhraseErronee

Spec == Init /\ [][Next]_vars

(***************************************************************************
 * L'INVARIANT INDUCTIF I — la conjonction déchargée par Apalache :
 *   Init ⟹ Inv (la base) ;  Inv ∧ Next ⟹ Inv' (le pas inductif,
 *   entiers NON bornés).  Inv ⊨ P1/P3/P4 ; la monotonie de l'époque et
 *   le rejeu-état-inchangé portent P2 (raffinement_v150 + PBT).
 ***************************************************************************)

I1 == secret = FALSE \/ Cardinality(sait) = 3
I2 == destr_injuste = FALSE
I3 == cf2_ok /\ media_corrompu = FALSE
I4 == e >= 1

Inv == TypeOK /\ I1 /\ I2 /\ I3 /\ I4

(* Les violations P1/P3/P4 (P2 est portée par les transitions) —
 * vérifiées NULLES sur tout état Inv (TLC, bornes étendues). *)
P1v == secret /\ Cardinality(sait) < 3
P3v == destr_injuste
P4v == media_corrompu \/ cf2_ok = FALSE
AucuneViolation == ~(P1v \/ P3v \/ P4v)

ContrainteBornes == e =< 5
=============================================================================
