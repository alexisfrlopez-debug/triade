--------------------------- MODULE CF3Equiv ---------------------------
(***************************************************************************
 * CF3Equiv — L'ÉQUIVALENCE TLA+ ↔ SÉMANTIQUE PYTHON, RÈGLE PAR RÈGLE,
 * DÉCHARGÉE PAR SMT SUR ENTIERS NON BORNÉS (l'instruction 89488hblm,
 * point (a) : « remplace la confrontation TLA+↔sémantique Python
 * échantillonnée (512 états/règle) par une équivalence déchargée par SMT
 * sur entiers non bornés, garde-à-garde et effet-à-effet, pour chacune
 * des 13 règles et tout état bien typé »).
 *
 * L'ENCODAGE (l'amendement 2 au plan — le XOR relationnel est REFUSÉ par
 * la discipline d'affectation d'Apalache, « Illegal assignment inside an
 * assignment-free expression » : la négation d'un système d'affectations
 * n'existe pas ; l'absence de transition n'est pas observable en vérification
 * bornée — le deadlock n'y est pas rapporté) : LES COPIES MIROIR.
 *   — l'état de base (les 10 variables de CF3) demeure INVARIANT dans les
 *     transitions de preuve ;
 *   — la copie R (eR, phaseR, …) porte l'image par la règle RÉELLE : les
 *     règles de CF3.tla instanciées par CF3R (zéro retranscription) ;
 *   — la copie P (eP, phaseP, …) porte l'image par la relation PYTHON :
 *     GP/FP instanciés par CFP (la transcription de CF3Python.tla) ;
 *   — marque : le témoin du tir réel.
 *
 * LES TROIS OBLIGATIONS PAR RÈGLE (tout état bien typé, e ∈ Int NON
 * BORNÉ) :
 *   EQUIV_GARDE_r (longueur 0) : GP_r ⟺ GT_r — la garde Python contre
 *     la garde TLA+ extraite (GT : l'extraction non-amorcée des règles
 *     de CF3.tla, 13 lignes auditable) ;
 *   EQUIV_IMAGE_r (longueur 1) : quand la règle RÉELLE tire (CF3R!r sur
 *     la copie R) ET que la garde Python tient (CFP!GP_r), les images
 *     COÏNCIDENT (l'invariant InvImage : copie R = copie P) ;
 *   EQUIV_ACTIVATION_r (longueur 1) : quand la règle RÉELLE tire, la
 *     garde Python TENAIT (l'invariant InvActivation : marque = FALSE ∨
 *     GP_r — le tir réel pose marque, la garde Python se lit sur la
 *     base inchangée).
 *   ET L'ÉPINGLAGE TLC (tlp_garde_reel_r, la phase D du plan) : sur les
 *     4 096 états représentants (e ∈ {1, 2} — la réduction justifiée :
 *     l'uniformité de classe des gardes Python par LT1 (SMT, le point
 *     (c)), celle des gardes réelles par l'audit mécanique consigné
 *     audit_regles.py), TLC exige : GP_r ⟺ le tir réel est possible —
 *     le sens MANQUANT (GP ∧ ¬tir réel : le TLC rapporte le deadlock ;
 *     tir réel ∧ ¬GP : l'invariant tombe). Les DEUX sens, l'artefact
 *     réel, l'énumération finie justifiée.
 *   L'ENSEMBLE : les gardes équivalentes (SMT entre les sémantiques
 *   écrites + TLC contre l'artefact réel), les images égales (SMT),
 *   les activations d'accord (SMT + TLC) — l'équivalence complète.
 ***************************************************************************)

EXTENDS CF3, CF3Python

(***************************************************************************
 * LES GARDES TLA+ — l'extraction non-amorcée des règles de CF3.tla.
 ***************************************************************************)

GT_VoleKUser == TRUE
GT_VoleSSerrure == TRUE
GT_VoleSPiege == TRUE
GT_FalsifieConteneur == trap_ok /\ phase = "canonique"
GT_FalsifiePiege == trap_ok
GT_RejoueEpoquePassee == e > 1
GT_OuvrirCorrect ==
  /\ trap_ok
  /\ phase = "canonique"
  /\ (KUser \notin sait \/ (KUser \in sait /\ Cardinality(sait) >= 3))
GT_OuvrirPhraseErronee == phase = "canonique"
GT_OuvrirAncienCouple == phase = "canonique" /\ e > 1
GT_Verifier == phase = "canonique"
GT_CrashPendantSession == TRUE
GT_CloturerCorrecte == phase = "brouillon" /\ trap_ok
GT_CloturerPhraseErronee == phase = "brouillon"

(***************************************************************************
 * LES COPIES MIROIR ET LES INSTANCES.
 ***************************************************************************)

VARIABLES
  \* @type: Int;
  eR, \* @type: Str;
  phaseR, \* @type: Set(Str);
  saitR, \* @type: Bool;
  trapR, \* @type: Bool;
  cf2R, \* @type: Bool;
  secretR, \* @type: Bool;
  accepteR, \* @type: Bool;
  detruitR, \* @type: Bool;
  injusteR, \* @type: Bool;
  mediaR,
  \* @type: Int;
  eP, \* @type: Str;
  phaseP, \* @type: Set(Str);
  saitP, \* @type: Bool;
  trapP, \* @type: Bool;
  cf2P, \* @type: Bool;
  secretP, \* @type: Bool;
  accepteP, \* @type: Bool;
  detruitP, \* @type: Bool;
  injusteP, \* @type: Bool;
  mediaP,
  \* @type: Bool;
  marque

\* la règle RÉELLE sur la copie R (zéro retranscription)
CF3R == INSTANCE CF3 WITH
  e <- eR, phase <- phaseR, sait <- saitR, trap_ok <- trapR,
  cf2_ok <- cf2R, secret <- secretR, accepte <- accepteR,
  detruit <- detruitR, destr_injuste <- injusteR,
  media_corrompu <- mediaR

\* la relation PYTHON sur la copie P
CFP == INSTANCE CF3Python WITH
  e <- eP, phase <- phaseP, sait <- saitP, trap_ok <- trapP,
  cf2_ok <- cf2P, secret <- secretP, accepte <- accepteP,
  detruit <- detruitP, destr_injuste <- injusteP,
  media_corrompu <- mediaP

\* l'état initial des preuves : la base bien typée, les copies COUPLÉES
InitCopies ==
  /\ TypeOK
  /\ eR = e /\ phaseR = phase /\ saitR = sait /\ trapR = trap_ok
  /\ cf2R = cf2_ok /\ secretR = secret /\ accepteR = accepte
  /\ detruitR = detruit /\ injusteR = destr_injuste
  /\ mediaR = media_corrompu
  /\ eP = e /\ phaseP = phase /\ saitP = sait /\ trapP = trap_ok
  /\ cf2P = cf2_ok /\ secretP = secret /\ accepteP = accepte
  /\ detruitP = detruit /\ injusteP = destr_injuste
  /\ mediaP = media_corrompu
  /\ marque = FALSE

\* l'invariant d'image : les copies COÏNCIDENT
InvImage ==
  /\ eR = eP /\ phaseR = phaseP /\ saitR = saitP /\ trapR = trapP
  /\ cf2R = cf2P /\ secretR = secretP /\ accepteR = accepteP
  /\ detruitR = detruitP /\ injusteR = injusteP /\ mediaR = mediaP

(***************************************************************************
 * LES OBLIGATIONS GARDE (longueur 0, Init = TypeOK) : la garde Python
 * contre la garde TLA+ extraite.
 ***************************************************************************)

OblGarde_VoleKUser == GP_VoleKUser <=> GT_VoleKUser
OblGarde_VoleSSerrure == GP_VoleSSerrure <=> GT_VoleSSerrure
OblGarde_VoleSPiege == GP_VoleSPiege <=> GT_VoleSPiege
OblGarde_FalsifieConteneur == GP_FalsifieConteneur <=> GT_FalsifieConteneur
OblGarde_FalsifiePiege == GP_FalsifiePiege <=> GT_FalsifiePiege
OblGarde_RejoueEpoquePassee == GP_RejoueEpoquePassee <=> GT_RejoueEpoquePassee
OblGarde_OuvrirCorrect == GP_OuvrirCorrect <=> GT_OuvrirCorrect
OblGarde_OuvrirPhraseErronee == GP_OuvrirPhraseErronee <=> GT_OuvrirPhraseErronee
OblGarde_OuvrirAncienCouple == GP_OuvrirAncienCouple <=> GT_OuvrirAncienCouple
OblGarde_Verifier == GP_Verifier <=> GT_Verifier
OblGarde_CrashPendantSession == GP_CrashPendantSession <=> GT_CrashPendantSession
OblGarde_CloturerCorrecte == GP_CloturerCorrecte <=> GT_CloturerCorrecte
OblGarde_CloturerPhraseErronee == GP_CloturerPhraseErronee <=> GT_CloturerPhraseErronee

(***************************************************************************
 * LES OBLIGATIONS IMAGE (longueur 1) : la règle RÉELLE tire sur la
 * copie R, la relation PYTHON tire sur la copie P — les images doivent
 * coïncider (InvImage). Init = InitCopies, Inv = InvImage.
 ***************************************************************************)

NextImage_VoleKUser == CF3R!VoleKUser /\ CFP!RPy_VoleKUser /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_VoleSSerrure == CF3R!VoleSSerrure /\ CFP!RPy_VoleSSerrure /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_VoleSPiege == CF3R!VoleSPiege /\ CFP!RPy_VoleSPiege /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_FalsifieConteneur == CF3R!FalsifieConteneur /\ CFP!RPy_FalsifieConteneur /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_FalsifiePiege == CF3R!FalsifiePiege /\ CFP!RPy_FalsifiePiege /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_RejoueEpoquePassee == CF3R!RejoueEpoquePassee /\ CFP!RPy_RejoueEpoquePassee /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_OuvrirCorrect == CF3R!OuvrirCorrect /\ CFP!RPy_OuvrirCorrect /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_OuvrirPhraseErronee == CF3R!OuvrirPhraseErronee /\ CFP!RPy_OuvrirPhraseErronee /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_OuvrirAncienCouple == CF3R!OuvrirAncienCouple /\ CFP!RPy_OuvrirAncienCouple /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_Verifier == CF3R!Verifier /\ CFP!RPy_Verifier /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_CrashPendantSession == CF3R!CrashPendantSession /\ CFP!RPy_CrashPendantSession /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_CloturerCorrecte == CF3R!CloturerCorrecte /\ CFP!RPy_CloturerCorrecte /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImage_CloturerPhraseErronee == CF3R!CloturerPhraseErronee /\ CFP!RPy_CloturerPhraseErronee /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>

(***************************************************************************
 * LES OBLIGATIONS ACTIVATION (longueur 1) : la règle RÉELLE tire sur la
 * copie R et pose marque — la garde Python devait tenir sur la base
 * (inchangée). Init = InitCopies, Inv = InvAct_r (par règle).
 ***************************************************************************)

NextAct_VoleKUser == CF3R!VoleKUser /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_VoleKUser == marque = FALSE \/ GP_VoleKUser

NextAct_VoleSSerrure == CF3R!VoleSSerrure /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_VoleSSerrure == marque = FALSE \/ GP_VoleSSerrure

NextAct_VoleSPiege == CF3R!VoleSPiege /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_VoleSPiege == marque = FALSE \/ GP_VoleSPiege

NextAct_FalsifieConteneur == CF3R!FalsifieConteneur /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_FalsifieConteneur == marque = FALSE \/ GP_FalsifieConteneur

NextAct_FalsifiePiege == CF3R!FalsifiePiege /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_FalsifiePiege == marque = FALSE \/ GP_FalsifiePiege

NextAct_RejoueEpoquePassee == CF3R!RejoueEpoquePassee /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_RejoueEpoquePassee == marque = FALSE \/ GP_RejoueEpoquePassee

NextAct_OuvrirCorrect == CF3R!OuvrirCorrect /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_OuvrirCorrect == marque = FALSE \/ GP_OuvrirCorrect

NextAct_OuvrirPhraseErronee == CF3R!OuvrirPhraseErronee /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_OuvrirPhraseErronee == marque = FALSE \/ GP_OuvrirPhraseErronee

NextAct_OuvrirAncienCouple == CF3R!OuvrirAncienCouple /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_OuvrirAncienCouple == marque = FALSE \/ GP_OuvrirAncienCouple

NextAct_Verifier == CF3R!Verifier /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_Verifier == marque = FALSE \/ GP_Verifier

NextAct_CrashPendantSession == CF3R!CrashPendantSession /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_CrashPendantSession == marque = FALSE \/ GP_CrashPendantSession

NextAct_CloturerCorrecte == CF3R!CloturerCorrecte /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_CloturerCorrecte == marque = FALSE \/ GP_CloturerCorrecte

NextAct_CloturerPhraseErronee == CF3R!CloturerPhraseErronee /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>
InvAct_CloturerPhraseErronee == marque = FALSE \/ GP_CloturerPhraseErronee

(***************************************************************************
 * L'ÉPINGLAGE TLC — les 4 096 représentants (e ∈ {1, 2}) : GP_r ⟺ le
 * tir réel possible. Le sens GP ∧ ¬tir réel : TLC RAPPORTE le deadlock
 * (ne pas passer -deadlock) ; le sens tir réel ∧ ¬GP : l'invariant
 * InvPin_r tombe. Init = InitPin, Next = NextPin_r.
 ***************************************************************************)

TypeOKClasses == TypeOK /\ e \in {1, 2}

InitPin ==
  /\ TypeOKClasses
  /\ eR = e /\ phaseR = phase /\ saitR = sait /\ trapR = trap_ok
  /\ cf2R = cf2_ok /\ secretR = secret /\ accepteR = accepte
  /\ detruitR = detruit /\ injusteR = destr_injuste
  /\ mediaR = media_corrompu
  /\ eP = e /\ phaseP = phase /\ saitP = sait /\ trapP = trap_ok
  /\ cf2P = cf2_ok /\ secretP = secret /\ accepteP = accepte
  /\ detruitP = detruit /\ injusteP = destr_injuste
  /\ mediaP = media_corrompu
  /\ marque = FALSE

RecopieTout ==
  UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit,
              destr_injuste, media_corrompu, eR, phaseR, saitR, trapR,
              cf2R, secretR, accepteR, detruitR, injusteR, mediaR,
              eP, phaseP, saitP, trapP, cf2P, secretP, accepteP,
              detruitP, injusteP, mediaP, marque>>

NextPin_VoleKUser ==
  \/ (marque = FALSE /\ CF3R!VoleKUser /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_VoleKUser /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_VoleKUser == marque = FALSE \/ GP_VoleKUser

NextPin_VoleSSerrure ==
  \/ (marque = FALSE /\ CF3R!VoleSSerrure /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_VoleSSerrure /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_VoleSSerrure == marque = FALSE \/ GP_VoleSSerrure

NextPin_VoleSPiege ==
  \/ (marque = FALSE /\ CF3R!VoleSPiege /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_VoleSPiege /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_VoleSPiege == marque = FALSE \/ GP_VoleSPiege

NextPin_FalsifieConteneur ==
  \/ (marque = FALSE /\ CF3R!FalsifieConteneur /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_FalsifieConteneur /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_FalsifieConteneur == marque = FALSE \/ GP_FalsifieConteneur

NextPin_FalsifiePiege ==
  \/ (marque = FALSE /\ CF3R!FalsifiePiege /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_FalsifiePiege /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_FalsifiePiege == marque = FALSE \/ GP_FalsifiePiege

NextPin_RejoueEpoquePassee ==
  \/ (marque = FALSE /\ CF3R!RejoueEpoquePassee /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_RejoueEpoquePassee /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_RejoueEpoquePassee == marque = FALSE \/ GP_RejoueEpoquePassee

NextPin_OuvrirCorrect ==
  \/ (marque = FALSE /\ CF3R!OuvrirCorrect /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_OuvrirCorrect /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_OuvrirCorrect == marque = FALSE \/ GP_OuvrirCorrect

NextPin_OuvrirPhraseErronee ==
  \/ (marque = FALSE /\ CF3R!OuvrirPhraseErronee /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_OuvrirPhraseErronee /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_OuvrirPhraseErronee == marque = FALSE \/ GP_OuvrirPhraseErronee

NextPin_OuvrirAncienCouple ==
  \/ (marque = FALSE /\ CF3R!OuvrirAncienCouple /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_OuvrirAncienCouple /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_OuvrirAncienCouple == marque = FALSE \/ GP_OuvrirAncienCouple

NextPin_Verifier ==
  \/ (marque = FALSE /\ CF3R!Verifier /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_Verifier /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_Verifier == marque = FALSE \/ GP_Verifier

NextPin_CrashPendantSession ==
  \/ (marque = FALSE /\ CF3R!CrashPendantSession /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_CrashPendantSession /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_CrashPendantSession == marque = FALSE \/ GP_CrashPendantSession

NextPin_CloturerCorrecte ==
  \/ (marque = FALSE /\ CF3R!CloturerCorrecte /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_CloturerCorrecte /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_CloturerCorrecte == marque = FALSE \/ GP_CloturerCorrecte

NextPin_CloturerPhraseErronee ==
  \/ (marque = FALSE /\ CF3R!CloturerPhraseErronee /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GP_CloturerPhraseErronee /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPin_CloturerPhraseErronee == marque = FALSE \/ GP_CloturerPhraseErronee

Tautologie == TRUE
=============================================================================
