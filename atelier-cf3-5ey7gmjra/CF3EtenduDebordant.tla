--------------------- MODULE CF3EtenduDebordant ---------------------
(***************************************************************************
 * CF3EtenduDebordant — LE CONTRÔLE NÉGATIF DE L'INDUCTIVITÉ (l'instruction
 * 5ey7gmjra : « Apalache Init⇒I et I∧Next⇒I′ NoError + contrôle négatif
 * attrapé ») : la règle 4 étendue MUTÉE — la destruction qui DÉBORDE sur
 * le média (media_corrompu' = TRUE, la confusion P3/P4 de la mutation
 * 89488hblm transportée à la garde étendue).
 *
 * L'OBLIGATION DE CONTROLÉ : Init = Inv, Next = NextDebordant, Inv = Inv —
 * un contre-exemple DOIT être produit (l'état Inv de phase quelconque à
 * piège intègre où la règle mutée tire : media_corrompu' = TRUE viole I3)
 * — Error 12 attendu : LA PREUVE D'INDUCTIVITÉ MORD sur la règle étendue.
 ***************************************************************************)

EXTENDS CF3Etendu

FalsifieConteneurDebordant ==
  /\ trap_ok
  /\ detruit' = TRUE
  /\ media_corrompu' = TRUE
  /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte,
                 destr_injuste>>

NextDebordant ==
  \/ VoleKUser
  \/ VoleSSerrure
  \/ VoleSPiege
  \/ FalsifieConteneurDebordant
  \/ FalsifiePiege
  \/ RejoueEpoquePassee
  \/ OuvrirCorrect
  \/ OuvrirPhraseErronee
  \/ OuvrirAncienCouple
  \/ Verifier
  \/ CrashPendantSession
  \/ CloturerCorrecte
  \/ CloturerPhraseErronee
=============================================================================
