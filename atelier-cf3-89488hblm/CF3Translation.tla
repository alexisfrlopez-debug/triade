------------------------ MODULE CF3Translation ------------------------
(***************************************************************************
 * CF3Translation — LE LEMME DE TRANSLATION ∀δ DÉCHARGÉ MÉCANIQUEMENT
 * (l'instruction 89488hblm, point (c) : « formalise l'argument
 * d'uniformité en époque en un lemme de translation quantifié (∀δ)
 * déchargé mécaniquement, au lieu du seul audit syntaxique +
 * translations {7, 50, 1000} »).
 *
 * L'ÉNONCÉ. Pour TOUT δ ≥ 0 et TOUT état bien typé d'époque e ≥ 2 (la
 * classe uniforme — D198), le système décalé σ_δ (l'époque lue e + δ,
 * le reste identique) se comporte IDENTIQUEMENT :
 *   LT1 — LES GARDES : pour chacune des 13 règles, la garde au décalé
 *     ⟺ la garde à l'origine — les gardes PYTHON (GP, la transcription
 *     de modele_invariant_v150.py) : leur équivalence aux gardes réelles
 *     est épinglée par le point (a) (EQUIV_GARDE en SMT non borné +
 *     l'épinglage TLC sur les 4 096 représentants) ; les gardes ne
 *     lisent l'époque que par e > 1, invariant de e ≥ 2 et e + δ ≥ 2 —
 *     e, δ NON BORNÉS ;
 *   LT2 — LES EFFETS : quand une règle tire à l'origine, elle tire au
 *     décalé et l'image décalée EST le décalé de l'image
 *     (σ_δ ∘ FT_r = FT_r ∘ σ_δ — la commutation, les règles RÉELLES
 *     instanciées des deux côtés) ; la clôture e ← e + 1 commute :
 *     (e + 1) + δ = (e + δ) + 1, les autres règles ne touchent pas
 *     l'époque.
 *   LT1 ∧ LT2 : UN CONTRE-EXEMPLE À GRANDE ÉPOQUE AURAIT, PAR
 *   TRANSLATION INVERSE, UN CONTRE-EXEMPLE À PETITE ÉPOQUE — la preuve
 *   par formes finies aux classes {1} ∪ {≥2} est COMPLÈTE. Les
 *   témoins {7, 50, 1000} de la vague 3 demeurent, plus jamais la
 *   preuve. L'uniformité des gardes RÉELLES repose en outre sur
 *   l'audit mécanique consigné (audit_regles.py : {e > 1, e + 1}
 *   seulement) — les DEUX voies.
 *
 * L'ENCODAGE : la copie décalée vit dans des VARIABLES MIROIR (te =
 * e + delta, composants égaux) ; le décalage delta est UNCHANGED dans
 * toute transition (un couplage « réparé » en bougeant δ′ ne prouverait
 * rien).
 *
 * LES CONTRÔLES NÉGATIFS :
 *   CC1 — LT1 avec l'hypothèse affaiblie e ≥ 1 : à e = 1, δ ≥ 1, la
 *     garde de rejeu (e > 1) est FAUSSE à l'origine et VRAIE au décalé
 *     — un contre-exemple DOIT être produit : LA FRONTIÈRE DE CLASSE
 *     {1}/{≥2} EST PORTANTE.
 *   CC2 — LT2 avec la clôture REPLACÉE PAR LE PLAFOND v120
 *     (e ← min(e + 1, 3)) des DEUX côtés : à e = 3, δ = 1, l'origine
 *     sature (e' = 3) et le décalé aussi (te' = 3) — le couplage
 *     exige te' = e' + δ = 4 : VIOLÉ — LE PLAFOND N'EST PAS
 *     TRANSLATION-UNIFORME (la raison historique de son retrait,
 *     v120 → v0.15.0).
 ***************************************************************************)

EXTENDS CF3, CF3Python

VARIABLES
  \* @type: Int;
  te,             (* l'époque de la copie décalée *)
  \* @type: Str;
  tphase,
  \* @type: Set(Str);
  tsait,
  \* @type: Bool;
  ttrap_ok,
  \* @type: Bool;
  tcf2_ok,
  \* @type: Bool;
  tsecret,
  \* @type: Bool;
  taccepte,
  \* @type: Bool;
  tdetruit,
  \* @type: Bool;
  tdestr_injuste,
  \* @type: Bool;
  tmedia_corrompu,
  \* @type: Int;
  delta           (* le décalage — NON BORNÉ, δ ≥ 0 *)

(* les règles TLA+ RÉELLES instanciées sur la copie décalée *)
CF3T == INSTANCE CF3 WITH
  e <- te, phase <- tphase, sait <- tsait, trap_ok <- ttrap_ok,
  cf2_ok <- tcf2_ok, secret <- tsecret, accepte <- taccepte,
  detruit <- tdetruit, destr_injuste <- tdestr_injuste,
  media_corrompu <- tmedia_corrompu

(* les gardes PYTHON instanciées sur la copie décalée *)
CFPyT == INSTANCE CF3Python WITH
  e <- te, phase <- tphase, sait <- tsait, trap_ok <- ttrap_ok,
  cf2_ok <- tcf2_ok, secret <- tsecret, accepte <- taccepte,
  detruit <- tdetruit, destr_injuste <- tdestr_injuste,
  media_corrompu <- tmedia_corrompu

(* l'état initial du lemme : l'origine bien typée, la classe ≥ 2, le
 * décalage ≥ 0, la copie COUPLÉE *)
InitLT ==
  /\ TypeOK
  /\ e >= 2
  /\ delta \in Int
  /\ delta >= 0
  /\ te = e + delta
  /\ tphase = phase
  /\ tsait = sait
  /\ ttrap_ok = trap_ok
  /\ tcf2_ok = cf2_ok
  /\ tsecret = secret
  /\ taccepte = accepte
  /\ tdetruit = detruit
  /\ tdestr_injuste = destr_injuste
  /\ tmedia_corrompu = media_corrompu

(* le couplage σ_δ — l'invariant du lemme *)
Couplage ==
  /\ te = e + delta
  /\ tphase = phase
  /\ tsait = sait
  /\ ttrap_ok = trap_ok
  /\ tcf2_ok = cf2_ok
  /\ tsecret = secret
  /\ taccepte = accepte
  /\ tdetruit = detruit
  /\ tdestr_injuste = destr_injuste
  /\ tmedia_corrompu = media_corrompu

(* LT1 — LES GARDES : les 13 gardes Python à l'origine ⟺ au décalé.
 * Vérifié : Init = InitLT, Inv = LT1, longueur 0. *)
LT1 ==
  /\ GP_VoleKUser <=> CFPyT!GP_VoleKUser
  /\ GP_VoleSSerrure <=> CFPyT!GP_VoleSSerrure
  /\ GP_VoleSPiege <=> CFPyT!GP_VoleSPiege
  /\ GP_FalsifieConteneur <=> CFPyT!GP_FalsifieConteneur
  /\ GP_FalsifiePiege <=> CFPyT!GP_FalsifiePiege
  /\ GP_RejoueEpoquePassee <=> CFPyT!GP_RejoueEpoquePassee
  /\ GP_OuvrirCorrect <=> CFPyT!GP_OuvrirCorrect
  /\ GP_OuvrirPhraseErronee <=> CFPyT!GP_OuvrirPhraseErronee
  /\ GP_OuvrirAncienCouple <=> CFPyT!GP_OuvrirAncienCouple
  /\ GP_Verifier <=> CFPyT!GP_Verifier
  /\ GP_CrashPendantSession <=> CFPyT!GP_CrashPendantSession
  /\ GP_CloturerCorrecte <=> CFPyT!GP_CloturerCorrecte
  /\ GP_CloturerPhraseErronee <=> CFPyT!GP_CloturerPhraseErronee

(* LT2 — LES EFFETS : la règle tire SIMULTANÉMENT à l'origine et au
 * décalé (les règles RÉELLES des deux côtés) ; l'invariant de couplage
 * doit tenir — c'est la commutation σ_δ ∘ FT = FT ∘ σ_δ.
 * Vérifié : Init = InitLT, Next = NextLTScelle, Inv = Couplage,
 * longueur 1. *)
NextLT ==
  \/ (VoleKUser /\ CF3T!VoleKUser)
  \/ (VoleSSerrure /\ CF3T!VoleSSerrure)
  \/ (VoleSPiege /\ CF3T!VoleSPiege)
  \/ (FalsifieConteneur /\ CF3T!FalsifieConteneur)
  \/ (FalsifiePiege /\ CF3T!FalsifiePiege)
  \/ (RejoueEpoquePassee /\ CF3T!RejoueEpoquePassee)
  \/ (OuvrirCorrect /\ CF3T!OuvrirCorrect)
  \/ (OuvrirPhraseErronee /\ CF3T!OuvrirPhraseErronee)
  \/ (OuvrirAncienCouple /\ CF3T!OuvrirAncienCouple)
  \/ (Verifier /\ CF3T!Verifier)
  \/ (CrashPendantSession /\ CF3T!CrashPendantSession)
  \/ (CloturerCorrecte /\ CF3T!CloturerCorrecte)
  \/ (CloturerPhraseErronee /\ CF3T!CloturerPhraseErronee)

NextLTScelle == NextLT /\ UNCHANGED <<delta>>

(* CC1 — l'hypothèse affaiblie : la classe e ≥ 1 au lieu de e ≥ 2 *)
InitLTfaible ==
  /\ TypeOK
  /\ e >= 1
  /\ delta \in Int
  /\ delta >= 0
  /\ te = e + delta
  /\ tphase = phase
  /\ tsait = sait
  /\ ttrap_ok = trap_ok
  /\ tcf2_ok = cf2_ok
  /\ tsecret = secret
  /\ taccepte = accepte
  /\ tdetruit = detruit
  /\ tdestr_injuste = destr_injuste
  /\ tmedia_corrompu = media_corrompu

(* CC2 — la clôture REPLACÉE PAR LE PLAFOND v120 (e ← min(e + 1, 3))
 * des DEUX côtés : le v120 transporté — la commutation DOIT ROMPRE à
 * la frontière du plafond (e = 3, δ = 1 : les deux saturent à 3, le
 * couplage exige 3 + δ) *)
CloturerPlafond ==
  /\ phase = "brouillon"
  /\ trap_ok
  /\ e' = IF e + 1 <= 3 THEN e + 1 ELSE 3
  /\ phase' = "canonique"
  /\ UNCHANGED <<sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

TCloturerPlafond ==
  /\ tphase = "brouillon"
  /\ ttrap_ok
  /\ te' = IF te + 1 <= 3 THEN te + 1 ELSE 3
  /\ tphase' = "canonique"
  /\ UNCHANGED <<tsait, ttrap_ok, tcf2_ok, tsecret, taccepte, tdetruit,
                 tdestr_injuste, tmedia_corrompu>>

NextLTplafond ==
  /\ CloturerPlafond /\ UNCHANGED <<te, tphase, tsait, ttrap_ok, tcf2_ok,
                                   tsecret, taccepte, tdetruit,
                                   tdestr_injuste, tmedia_corrompu>>
  /\ TCloturerPlafond /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok,
                                    secret, accepte, detruit,
                                    destr_injuste, media_corrompu>>
  /\ UNCHANGED <<delta>>
=============================================================================
