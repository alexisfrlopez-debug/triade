---------------------- MODULE CF3EquivDiffC ----------------------
(***************************************************************************
 * CF3EquivDiffC — L'ENVELOPPE DU TÉMOIN DIFF POUR LES CONTRÔLES du
 * point (a) (aspect EFFET) : les NextDiffw_r enveloppent les XOR MUTÉS
 * (la règle RÉELLE contre la relation Python à l'effet dévié) —
 * chacun DOIT tomber (Error 12 : diff' = TRUE atteint, la faute de
 * transcription ATTRAPÉE par le vérificateur).
 ***************************************************************************)

EXTENDS CF3EquivControles

VARIABLES
  \* @type: Bool;
  diff

InitTypeOKdiffC == TypeOK /\ diff = FALSE

DiffInvC == diff = FALSE

RecopieC ==
  /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte,
                 detruit, destr_injuste, media_corrompu>>
  /\ diff' = FALSE

NextDiffw_VoleKUser == (XORw_VoleKUser /\ diff' = TRUE) \/ (~ XORw_VoleKUser /\ RecopieC)
NextDiffw_VoleSSerrure == (XORw_VoleSSerrure /\ diff' = TRUE) \/ (~ XORw_VoleSSerrure /\ RecopieC)
NextDiffw_VoleSPiege == (XORw_VoleSPiege /\ diff' = TRUE) \/ (~ XORw_VoleSPiege /\ RecopieC)
NextDiffw_FalsifieConteneur == (XORw_FalsifieConteneur /\ diff' = TRUE) \/ (~ XORw_FalsifieConteneur /\ RecopieC)
NextDiffw_FalsifiePiege == (XORw_FalsifiePiege /\ diff' = TRUE) \/ (~ XORw_FalsifiePiege /\ RecopieC)
NextDiffw_RejoueEpoquePassee == (XORw_RejoueEpoquePassee /\ diff' = TRUE) \/ (~ XORw_RejoueEpoquePassee /\ RecopieC)
NextDiffw_OuvrirCorrect == (XORw_OuvrirCorrect /\ diff' = TRUE) \/ (~ XORw_OuvrirCorrect /\ RecopieC)
NextDiffw_OuvrirPhraseErronee == (XORw_OuvrirPhraseErronee /\ diff' = TRUE) \/ (~ XORw_OuvrirPhraseErronee /\ RecopieC)
NextDiffw_OuvrirAncienCouple == (XORw_OuvrirAncienCouple /\ diff' = TRUE) \/ (~ XORw_OuvrirAncienCouple /\ RecopieC)
NextDiffw_Verifier == (XORw_Verifier /\ diff' = TRUE) \/ (~ XORw_Verifier /\ RecopieC)
NextDiffw_CrashPendantSession == (XORw_CrashPendantSession /\ diff' = TRUE) \/ (~ XORw_CrashPendantSession /\ RecopieC)
NextDiffw_CloturerCorrecte == (XORw_CloturerCorrecte /\ diff' = TRUE) \/ (~ XORw_CloturerCorrecte /\ RecopieC)
NextDiffw_CloturerPhraseErronee == (XORw_CloturerPhraseErronee /\ diff' = TRUE) \/ (~ XORw_CloturerPhraseErronee /\ RecopieC)
=============================================================================
