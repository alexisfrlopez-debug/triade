------------------------ MODULE CF3EquivDiff ------------------------
(***************************************************************************
 * CF3EquivDiff — L'ENVELOPPE DU TÉMOIN DIFF (le point (a), aspect
 * EFFET) : l'égalité relationnelle R_CF3 ≡ R_Python ne peut pas se
 * vérifier avec Inv = FALSE (l'invariant serait violé DÈS la profondeur
 * 0 — un contrôle creux). Le témoin diff enregistre si la transition
 * prise appartient au XOR : Init = TypeOK ∧ diff = FALSE ; la transition
 * XOR pose diff' = TRUE ; l'invariant diff = FALSE tient à la profondeur
 * 0 PAR CONSTRUCTION et tombe à la profondeur 1 SI ET SEULEMENT SI le
 * XOR est non vide depuis un état bien typé.
 *
 *   EQUIV_EFFET_r : Init = InitTypeOKdiff, Next = NextDiff_r,
 *                   Inv = DiffInv, longueur 1 → NoError ⟹ relations
 *                   ÉGALES sur tout état bien typé (garde ET effet,
 *                   contre la règle RÉELLE de CF3.tla).
 *   CONTRÔLE EFFET : Next = NextDiffw_r (le XOR MUTÉ) → Error 12
 *                   attendu (la faute de transcription ATTRAPÉE).
 ***************************************************************************)

EXTENDS CF3Equiv

VARIABLES
  \* @type: Bool;
  diff            (* le témoin : la transition fut-elle dans le XOR ? *)

InitTypeOKdiff == TypeOK /\ diff = FALSE

DiffInv == diff = FALSE

(* la recopie : l'issue hors XOR (le bégaiement, diff rendu FAUX) *)
Recopie ==
  /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte,
                 detruit, destr_injuste, media_corrompu>>
  /\ diff' = FALSE

(* les 13 next-relations : le XOR de la règle RÉELLE contre la relation
 * Python, le témoin posé ; hors XOR, la recopie *)
NextDiff_VoleKUser == (XOR_VoleKUser /\ diff' = TRUE) \/ (~ XOR_VoleKUser /\ Recopie)
NextDiff_VoleSSerrure == (XOR_VoleSSerrure /\ diff' = TRUE) \/ (~ XOR_VoleSSerrure /\ Recopie)
NextDiff_VoleSPiege == (XOR_VoleSPiege /\ diff' = TRUE) \/ (~ XOR_VoleSPiege /\ Recopie)
NextDiff_FalsifieConteneur == (XOR_FalsifieConteneur /\ diff' = TRUE) \/ (~ XOR_FalsifieConteneur /\ Recopie)
NextDiff_FalsifiePiege == (XOR_FalsifiePiege /\ diff' = TRUE) \/ (~ XOR_FalsifiePiege /\ Recopie)
NextDiff_RejoueEpoquePassee == (XOR_RejoueEpoquePassee /\ diff' = TRUE) \/ (~ XOR_RejoueEpoquePassee /\ Recopie)
NextDiff_OuvrirCorrect == (XOR_OuvrirCorrect /\ diff' = TRUE) \/ (~ XOR_OuvrirCorrect /\ Recopie)
NextDiff_OuvrirPhraseErronee == (XOR_OuvrirPhraseErronee /\ diff' = TRUE) \/ (~ XOR_OuvrirPhraseErronee /\ Recopie)
NextDiff_OuvrirAncienCouple == (XOR_OuvrirAncienCouple /\ diff' = TRUE) \/ (~ XOR_OuvrirAncienCouple /\ Recopie)
NextDiff_Verifier == (XOR_Verifier /\ diff' = TRUE) \/ (~ XOR_Verifier /\ Recopie)
NextDiff_CrashPendantSession == (XOR_CrashPendantSession /\ diff' = TRUE) \/ (~ XOR_CrashPendantSession /\ Recopie)
NextDiff_CloturerCorrecte == (XOR_CloturerCorrecte /\ diff' = TRUE) \/ (~ XOR_CloturerCorrecte /\ Recopie)
NextDiff_CloturerPhraseErronee == (XOR_CloturerPhraseErronee /\ diff' = TRUE) \/ (~ XOR_CloturerPhraseErronee /\ Recopie)
=============================================================================
