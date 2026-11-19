--------------------- MODULE CF3EquivControlesEtendu --------------------
(***************************************************************************
 * CF3EquivControlesEtendu — LES 26 CONTRÔLES NÉGATIFS SUR LE MODÈLE
 * ÉTENDU, UN PAR
 * OBLIGATION (l'instruction 89488hblm : « affaiblissement volontaire
 * devant être attrapé ») — l'encodage des copies (l'amendement 2).
 *
 * Les 13 contrôles GARDE (longueur 0, Init = TypeOK) :
 *   Inv = OblFaibleGarde_r : GPw_r ⟺ GT_r → Error 12 attendu.
 * Les 13 contrôles IMAGE (longueur 1, Init = InitCopies) :
 *   Next = la règle RÉELLE sur la copie R ∧ la relation PYTHON MUTÉE
 *   (CFPw!RPyw_r — la garde intacte, l'effet dévié) sur la copie P ;
 *   Inv = InvImage → Error 12 attendu (les images divergent).
 * Le contrôle de l'épinglage TLC : la garde mutée de la falsification
 * du conteneur (L'EXTENSION ANNULÉE — la garde v0.15.0 canonique-seule
 * restaurée comme mutation, PLUS RESTRICTIVE que la règle étendue)
 * — le TLC DOIT tomber : à phase = "brouillon" la règle RÉELLE étendue
 * tire (marque posée) tandis que la garde mutée REFUSE — l'INVARIANT
 * InvPinCtl tombe (la violation rapportée — le sens inverse du contrôle
 * 89488hblm, la même discipline).
 ***************************************************************************)

EXTENDS CF3EquivEtendu, CF3PythonControlesEtendu

\* la relation Python MUTÉE sur la copie P
CFPw == INSTANCE CF3PythonControlesEtendu WITH
  e <- eP, phase <- phaseP, sait <- saitP, trap_ok <- trapP,
  cf2_ok <- cf2P, secret <- secretP, accepte <- accepteP,
  detruit <- detruitP, destr_injuste <- injusteP,
  media_corrompu <- mediaP

\* ---- LES OBLIGATIONS AFFAIBLIES GARDE ----------------------------------
OblFaibleGarde_VoleKUser == GPw_VoleKUser <=> GT_VoleKUser
OblFaibleGarde_VoleSSerrure == GPw_VoleSSerrure <=> GT_VoleSSerrure
OblFaibleGarde_VoleSPiege == GPw_VoleSPiege <=> GT_VoleSPiege
OblFaibleGarde_FalsifieConteneur == GPw_FalsifieConteneur <=> GT_FalsifieConteneur
OblFaibleGarde_FalsifiePiege == GPw_FalsifiePiege <=> GT_FalsifiePiege
OblFaibleGarde_RejoueEpoquePassee == GPw_RejoueEpoquePassee <=> GT_RejoueEpoquePassee
OblFaibleGarde_OuvrirCorrect == GPw_OuvrirCorrect <=> GT_OuvrirCorrect
OblFaibleGarde_OuvrirPhraseErronee == GPw_OuvrirPhraseErronee <=> GT_OuvrirPhraseErronee
OblFaibleGarde_OuvrirAncienCouple == GPw_OuvrirAncienCouple <=> GT_OuvrirAncienCouple
OblFaibleGarde_Verifier == GPw_Verifier <=> GT_Verifier
OblFaibleGarde_CrashPendantSession == GPw_CrashPendantSession <=> GT_CrashPendantSession
OblFaibleGarde_CloturerCorrecte == GPw_CloturerCorrecte <=> GT_CloturerCorrecte
OblFaibleGarde_CloturerPhraseErronee == GPw_CloturerPhraseErronee <=> GT_CloturerPhraseErronee

\* ---- LES NEXT MUTÉS IMAGE (la règle réelle ∧ la relation mutée) --------
NextImageCtl_VoleKUser == CF3R!VoleKUser /\ CFPw!RPyw_VoleKUser /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_VoleSSerrure == CF3R!VoleSSerrure /\ CFPw!RPyw_VoleSSerrure /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_VoleSPiege == CF3R!VoleSPiege /\ CFPw!RPyw_VoleSPiege /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_FalsifieConteneur == CF3R!FalsifieConteneur /\ CFPw!RPyw_FalsifieConteneur /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_FalsifiePiege == CF3R!FalsifiePiege /\ CFPw!RPyw_FalsifiePiege /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_RejoueEpoquePassee == CF3R!RejoueEpoquePassee /\ CFPw!RPyw_RejoueEpoquePassee /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_OuvrirCorrect == CF3R!OuvrirCorrect /\ CFPw!RPyw_OuvrirCorrect /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_OuvrirPhraseErronee == CF3R!OuvrirPhraseErronee /\ CFPw!RPyw_OuvrirPhraseErronee /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_OuvrirAncienCouple == CF3R!OuvrirAncienCouple /\ CFPw!RPyw_OuvrirAncienCouple /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_Verifier == CF3R!Verifier /\ CFPw!RPyw_Verifier /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_CrashPendantSession == CF3R!CrashPendantSession /\ CFPw!RPyw_CrashPendantSession /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_CloturerCorrecte == CF3R!CloturerCorrecte /\ CFPw!RPyw_CloturerCorrecte /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>
NextImageCtl_CloturerPhraseErronee == CF3R!CloturerPhraseErronee /\ CFPw!RPyw_CloturerPhraseErronee /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, marque>>

\* ---- LE CONTRÔLE DE L'ÉPINGLAGE TLC ------------------------------------
\* la garde mutée de la falsification du conteneur (la phase canonique
\* oubliée) : à phase = "brouillon" la garde mutée prétend que le tir
\* est possible — la règle RÉELLE refuse — le deadlock DOIT être
\* rapporté par TLC (le contrôle de l'épinglage)
NextPinCtl_FalsifieConteneur ==
  \/ (marque = FALSE /\ CF3R!FalsifieConteneur /\ marque' = TRUE /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, destr_injuste, media_corrompu, eP, phaseP, saitP, trapP, cf2P, secretP, accepteP, detruitP, injusteP, mediaP>>)
  \/ (marque = FALSE /\ ~ GPw_FalsifieConteneur /\ RecopieTout)
  \/ (marque = TRUE /\ RecopieTout)
InvPinCtl_FalsifieConteneur == marque = FALSE \/ GPw_FalsifieConteneur
=============================================================================
