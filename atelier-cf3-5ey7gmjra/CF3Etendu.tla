------------------------- MODULE CF3Etendu -------------------------
(***************************************************************************
 * CF3Etendu — LE MODÈLE CF3 ÉTENDU : LA FALSIFICATION OFFERTE PENDANT
 * UNE SESSION OUVERTE (l'instruction 5ey7gmjra, point 1 : « Étends
 * CF3.tla pour offrir falsifie_conteneur pendant une session ouverte
 * (garde alignée sur la sentinelle concrète : destruction locale sur
 * falsification prouvée, média/fragments intacts) »).
 *
 * LA SOURCE DE L'EXTENSION : l'écart de couverture DÉCOUVERT par la
 * campagne PBT v0.15.0 (graine 20261112) et consigné append-only — 660
 * écarts d'UNE classe : falsifie_conteneur pendant une SESSION (phase
 * brouillon, piège intègre) — le modèle REFUSAIT la règle (la garde
 * exigeait le canonique) tandis que le CONCRET DÉTRUISAIT (la
 * sentinelle de v06/coffre_cf3.py court sur le CANONIQUE du conteneur,
 * pas sur le brouillon de session : bit du chiffretexte altéré + un
 * second ouvrir → empreinte divergente APRÈS phrase vérifiée →
 * destruction LOCALE + PV, le média INTACT). LE RÉSULTAT HISTORIQUE
 * (660 divergences) DEMEURE CONSIGNÉ : il est la DÉCOUVERTE qui motiva
 * la présente extension — le modèle v0.15.0 (md5 b762c2c8…) demeure
 * INTACT et rejouable, l'extension vit dans le présent module.
 *
 * L'ALIGNEMENT : la garde de la règle 4 devient trap_ok SEUL — la
 * destruction locale sur falsification PROUVÉE est offerte aux DEUX
 * phases (canonique ET brouillon), l'effet INCHANGÉ (detruit' = TRUE,
 * le média et les fragments intacts, le PV unique) : EXACTEMENT ce que
 * la sentinelle concrète fait. Les DOUZE autres règles demeurent la
 * copie règle à règle de CF3.tla (v0.15.0) — l'unique écart de la
 * présente édition est la garde de la règle 4.
 *
 * L'INVARIANT I (I1–I4) demeure : la falsification en session ne
 * touche NI le secret NI le média NI les fragments NI l'époque — I1
 * secret ⟹ seuil 3 ; I2 pas de destruction injuste (la destruction
 * reste PROUVÉE : falsification cryptographique, piège intègre) ;
 * I3 CF2 et média intacts ; I4 époque ≥ 1. La preuve d'inductivité
 * (Apalache --init=Inv, entiers non bornés) est re-déchargée sur le
 * présent module par la batterie 5ey7gmjra.
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
 * LES 13 RÈGLES — règle à règle depuis CF3.tla (v0.15.0), SAUF la règle 4 :
 * l'extension 5ey7gmjra. L'audit mécanique demeure : toute occurrence de
 * l'époque dans une garde ou action ci-dessous est de la forme e > 1 (le
 * prédicat de classe ≥ 2) ou e + 1 (le successeur de la clôture).
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

(* 4 : LA FALSIFICATION DU CONTENEUR — L'EXTENSION 5ey7gmjra : la
 *     PREUVE exige le piège intègre, la PHASE EST LIBRE (canonique OU
 *     brouillon — la session ouverte comprise) : destruction LOCALE
 *     (PV), le média INTACT — la garde de la sentinelle concrète *)
FalsifieConteneur ==
  /\ trap_ok
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
 * L'INVARIANT INDUCTIF I — IDENTIQUE à CF3.tla : la falsification en
 * session ne touche aucun composant que I contraint au-delà de detruit
 * (la destruction PROUVÉE demeure LOCALE).
 ***************************************************************************)

I1 == secret = FALSE \/ Cardinality(sait) = 3
I2 == destr_injuste = FALSE
I3 == cf2_ok /\ media_corrompu = FALSE
I4 == e >= 1

Inv == TypeOK /\ I1 /\ I2 /\ I3 /\ I4

(* Les violations P1/P3/P4 (P2 est portée par les transitions) *)
P1v == secret /\ Cardinality(sait) < 3
P3v == destr_injuste
P4v == media_corrompu \/ cf2_ok = FALSE
AucuneViolation == ~(P1v \/ P3v \/ P4v)

ContrainteBornes == e =< 5
=============================================================================
