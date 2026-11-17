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
 *     ⟺ la garde à l'origine (les gardes ne lisent l'époque que par
 *     e > 1, invariant de e ≥ 2 et e + δ ≥ 2 — e, δ NON BORNÉS) ;
 *   LT2 — LES EFFETS : quand une règle tire à l'origine, elle tire au
 *     décalé et l'image décalée EST le décalé de l'image
 *     (σ_δ ∘ FT_r = FT_r ∘ σ_δ — la commutation ; la clôture e ← e + 1
 *     commute : (e + 1) + δ = (e + δ) + 1, les autres règles ne
 *     touchent pas l'époque).
 *   LT1 ∧ LT2 : UN CONTRE-EXEMPLE À GRANDE ÉPOQUE AURAIT, PAR
 *   TRANSLATION INVERSE, UN CONTRE-EXEMPLE À PETITE ÉPOQUE — la preuve
 *   par formes finies aux classes {1} ∪ {≥2} est COMPLÈTE. Les
 *   témoins {7, 50, 1000} de la vague 3 demeurent, plus jamais la
 *   preuve.
 *
 * L'ENCODAGE : la copie décalée vit dans des VARIABLES MIROIR (te,
 * tphase, …) couplées à l'origine par te = e + delta ∧ composants
 * égaux ; les règles TLA+ RÉELLES s'appliquent à la copie par
 * INSTANCE CF3 (zéro retranscription), les gardes extraites par
 * INSTANCE CF3Equiv. Le décalage delta est UNCHANGED dans toute
 * transition (un couplage « réparé » en bougeant δ′ ne prouverait
 * rien).
 *
 * LES CONTRÔLES NÉGATIFS (l'affaiblissement volontaire, attrapé) :
 *   CC1 — LT1 avec l'hypothèse affaiblie e ≥ 1 (au lieu de e ≥ 2) : à
 *     e = 1, δ ≥ 1, la garde de rejeu (e > 1) est FAUSSE à l'origine
 *     et VRAIE au décalé — un contre-exemple DOIT être produit : LA
 *     FRONTIÈRE DE CLASSE {1}/{≥2} EST PORTANTE.
 *   CC2 — LT2 avec la clôture REPLACÉE PAR LE PLAFOND v120
 *     (e ← min(e + 1, 3)) DES DEUX CÔTÉS : à e = 3, δ = 1, l'origine
 *     sature (e' = 3) et le décalé aussi (te' = 3) — le couplage
 *     exige te' = e' + δ = 4 : VIOLÉ — un contre-exemple DOIT être
 *     produit : LE PLAFOND N'EST PAS TRANSLATION-UNIFORME (c'est la
 *     raison historique de son retrait, v120 → v0.15.0).
 ***************************************************************************)

EXTENDS CF3Equiv

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

(* les gardes extraites, instanciées sur la copie décalée *)
CFE_T == INSTANCE CF3Equiv WITH
  e <- te, phase <- tphase, sait <- tsait, trap_ok <- ttrap_ok,
  cf2_ok <- tcf2_ok, secret <- tsecret, accepte <- taccepte,
  detruit <- tdetruit, destr_injuste <- tdestr_injuste,
  media_corrompu <- tmedia_corrompu

(* l'état initial du lemme : l'origine bien typée, la classe ≥ 2, le
 * décalage ≥ 0, la copie COUPLÉE *)
InitLT ==
  /\ TypeOK
  /\ e >= 2
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

(* LT1 — LES GARDES : les 13 gardes à l'origine ⟺ au décalé.
 * Vérifié : Init = InitLT, Inv = LT1, longueur 0. *)
LT1 ==
  /\ GT_VoleKUser <=> CFE_T!GT_VoleKUser
  /\ GT_VoleSSerrure <=> CFE_T!GT_VoleSSerrure
  /\ GT_VoleSPiege <=> CFE_T!GT_VoleSPiege
  /\ GT_FalsifieConteneur <=> CFE_T!GT_FalsifieConteneur
  /\ GT_FalsifiePiege <=> CFE_T!GT_FalsifiePiege
  /\ GT_RejoueEpoquePassee <=> CFE_T!GT_RejoueEpoquePassee
  /\ GT_OuvrirCorrect <=> CFE_T!GT_OuvrirCorrect
  /\ GT_OuvrirPhraseErronee <=> CFE_T!GT_OuvrirPhraseErronee
  /\ GT_OuvrirAncienCouple <=> CFE_T!GT_OuvrirAncienCouple
  /\ GT_Verifier <=> CFE_T!GT_Verifier
  /\ GT_CrashPendantSession <=> CFE_T!GT_CrashPendantSession
  /\ GT_CloturerCorrecte <=> CFE_T!GT_CloturerCorrecte
  /\ GT_CloturerPhraseErronee <=> CFE_T!GT_CloturerPhraseErronee

(* LT2 — LES EFFETS : la règle tire SIMULTANÉMENT à l'origine et au
 * décalé (les règles RÉELLES des deux côtés) ; l'invariant de couplage
 * doit tenir — c'est la commutation σ_δ ∘ FT = FT ∘ σ_δ.
 * Vérifié : Init = InitLT, Next = NextLT, Inv = Couplage, longueur 1. *)
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

(* les variables NON touchées par un côté demeurent (chaque plafond
 * spécifie SON côté ; l'autre côté et delta sont UNCHANGED) *)
NextLTplafond ==
  /\ CloturerPlafond /\ UNCHANGED <<te, tphase, tsait, ttrap_ok, tcf2_ok,
                                   tsecret, taccepte, tdetruit,
                                   tdestr_injuste, tmedia_corrompu>>
  /\ TCloturerPlafond /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok,
                                    secret, accepte, detruit,
                                    destr_injuste, media_corrompu>>
  /\ UNCHANGED <<delta>>
=============================================================================
