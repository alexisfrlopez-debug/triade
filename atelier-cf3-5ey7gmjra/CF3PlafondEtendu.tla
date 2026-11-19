----------------------- MODULE CF3PlafondEtendu ----------------------
(***************************************************************************
 * CF3Plafond — LA VARIANTE v120 POUR LE CONTRÔLE DE FIDÉLITÉ D187 :
 * la clôture ramène e <- min(e+1, EpoquesMax) — le plafond ARTIFICIEL
 * de l'explorateur D187 (uniquement ici ; le modèle CF3, lui, ne
 * plafonne plus). L'exploration COMPLÈTE de cette variante doit
 * reproduire l'espace BORNÉ de l'explorateur Python (216 états en
 * exploration complète ; 154 aux bornes historiques profondeur ≤ 6 —
 * voir CF3Fidelite pour la convention de profondeur).
 ***************************************************************************)

EXTENDS CF3Etendu, Naturals

CONSTANT
  \* @type: Int;
  EpoquesMax

Min(a, b) == IF a =< b THEN a ELSE b

CloturerCorrectePlafond ==
  /\ phase = "brouillon"
  /\ trap_ok
  /\ e' = Min(e + 1, EpoquesMax)
  /\ phase' = "canonique"
  /\ UNCHANGED <<sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

NextPlafond ==
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
  \/ CloturerCorrectePlafond
  \/ CloturerPhraseErronee

SpecPlafond == Init /\ [][NextPlafond]_vars

=============================================================================
