------------------------ MODULE CF3PythonEtendu ------------------------
(***************************************************************************
 * CF3PythonEtendu — LA SÉMANTIQUE PYTHON DE CF3 ÉTENDUE EN TLA+ : la
 * transcription fidèle de modele_invariant_v153.py (l'instruction 5ey7gmjra
 * — le pendant Python de CF3Etendu.tla : la règle 4 étendue, les douze
 * autres la copie de la v0.15.0).
 *
 * LA SOURCE : actions_possibles (l'OFFRE — quelles actions sont proposées
 * selon la phase) et appliquer (la garde EFFECTIVE — None = refus — et
 * l'effet — les affectations). GP_r : la garde effective (l'offre ∧
 * appliquer ≠ None) ; FP_r : l'effet (les conjonctions primées) ;
 * RPy_r == GP_r ∧ FP_r : la relation de transition Python de la règle r.
 *
 * LE SEUIL LITTÉRAL : le code Python lit len(sait & ELEMENTS) >= 3 —
 * transcrit Cardinality(sait ∩ Elements) >= 3 ; l'égalité avec
 * Cardinality(sait) sous TypeOK est CONTENU DE LA PREUVE (les gardes
 * TLA+ portent Cardinality(sait) >= 3).
 *
 * La correspondance des noms : vole_K_user → VoleKUser, vole_S_serrure →
 * VoleSSerrure, vole_S_piège → VoleSPiege, falsifie_conteneur →
 * FalsifieConteneur, falsifie_piège → FalsifiePiege, rejoue_époque_passée
 * → RejoueEpoquePassee, ouvrir_correct → OuvrirCorrect,
 * ouvrir_phrase_erronée → OuvrirPhraseErronee, ouvrir_ancien_couple →
 * OuvrirAncienCouple, verifier → Verifier, crash_pendant_session →
 * CrashPendantSession, clôturer_correcte → CloturerCorrecte,
 * clôturer_phrase_erronée → CloturerPhraseErronee.
 ***************************************************************************)

EXTENDS CF3Etendu

\* le seuil PYTHON, LITTÉRAL (len(sait & ELEMENTS) >= 3)
SeuilPy == Cardinality(sait \intersect Elements) >= 3

\* 1-3 : les vols — offerts TOUJOURS, jamais refusés
GP_VoleKUser == TRUE
FP_VoleKUser ==
  /\ sait' = sait \union {KUser}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

GP_VoleSSerrure == TRUE
FP_VoleSSerrure ==
  /\ sait' = sait \union {SSerrure}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

GP_VoleSPiege == TRUE
FP_VoleSPiege ==
  /\ sait' = sait \union {SPiege}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

\* 4 : falsifie_conteneur — L'EXTENSION 5ey7gmjra : offert toujours ;
\*     EFFECTIF : piège intègre SEUL (appliquer : if trap_ok — les DEUX
\*     phases, la session ouverte comprise : la sentinelle concrète)
GP_FalsifieConteneur == trap_ok
FP_FalsifieConteneur ==
  /\ detruit' = TRUE
  /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte,
                 destr_injuste, media_corrompu>>

\* 5 : falsifie_piège — offert toujours ; EFFECTIF : trap_ok
GP_FalsifiePiege == trap_ok
FP_FalsifiePiege ==
  /\ trap_ok' = FALSE
  /\ UNCHANGED <<e, phase, sait, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

\* 6 : rejoue_époque_passée — offert toujours ; EFFECTIF : e > 1 ;
\*     l'état RETOURNÉ INCHANGÉ
GP_RejoueEpoquePassee == e > 1
FP_RejoueEpoquePassee == UNCHANGED vars

\* 7 : ouvrir_correct — offert au canonique ; EFFECTIF : trap_ok et
\*     (K_user ∉ sait — l'honnête — ou K_user ∈ sait ∧ seuil ≥ 3) ;
\*     le secret appris à la branche seuil, conservé sinon
GP_OuvrirCorrect ==
  /\ phase = "canonique"
  /\ trap_ok
  /\ (KUser \notin sait \/ (KUser \in sait /\ SeuilPy))
FP_OuvrirCorrect ==
  /\ phase' = "brouillon"
  /\ secret' = IF KUser \in sait THEN TRUE ELSE secret
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, accepte, detruit,
                 destr_injuste, media_corrompu>>

\* 8 : ouvrir_phrase_erronée — offert au canonique ; JAMAIS refusé ;
\*     l'état inchangé
GP_OuvrirPhraseErronee == phase = "canonique"
FP_OuvrirPhraseErronee == UNCHANGED vars

\* 9 : ouvrir_ancien_couple — offert au canonique SI e > 1 ; jamais
\*     refusé ensuite ; l'état inchangé (REFUS NOMMÉ)
GP_OuvrirAncienCouple == phase = "canonique" /\ e > 1
FP_OuvrirAncienCouple == UNCHANGED vars

\* 10 : verifier — offert au canonique ; l'état inchangé
GP_Verifier == phase = "canonique"
FP_Verifier == UNCHANGED vars

\* 11 : crash_pendant_session — offert aux DEUX phases ; l'état
\*      revient au canonique, l'époque NE BOUGE PAS
GP_CrashPendantSession == TRUE
FP_CrashPendantSession ==
  /\ phase' = "canonique"
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

\* 12 : clôturer_correcte — offerte au brouillon ; EFFECTIVE : trap_ok ;
\*      e ← e+1 SANS PLAFOND, retour au canonique
GP_CloturerCorrecte == phase = "brouillon" /\ trap_ok
FP_CloturerCorrecte ==
  /\ e' = e + 1
  /\ phase' = "canonique"
  /\ UNCHANGED <<sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

\* 13 : clôturer_phrase_erronée — offerte au brouillon ; l'état inchangé
GP_CloturerPhraseErronee == phase = "brouillon"
FP_CloturerPhraseErronee == UNCHANGED vars

\* les relations Python (garde effective ∧ effet)
RPy_VoleKUser == GP_VoleKUser /\ FP_VoleKUser
RPy_VoleSSerrure == GP_VoleSSerrure /\ FP_VoleSSerrure
RPy_VoleSPiege == GP_VoleSPiege /\ FP_VoleSPiege
RPy_FalsifieConteneur == GP_FalsifieConteneur /\ FP_FalsifieConteneur
RPy_FalsifiePiege == GP_FalsifiePiege /\ FP_FalsifiePiege
RPy_RejoueEpoquePassee == GP_RejoueEpoquePassee /\ FP_RejoueEpoquePassee
RPy_OuvrirCorrect == GP_OuvrirCorrect /\ FP_OuvrirCorrect
RPy_OuvrirPhraseErronee == GP_OuvrirPhraseErronee /\ FP_OuvrirPhraseErronee
RPy_OuvrirAncienCouple == GP_OuvrirAncienCouple /\ FP_OuvrirAncienCouple
RPy_Verifier == GP_Verifier /\ FP_Verifier
RPy_CrashPendantSession == GP_CrashPendantSession /\ FP_CrashPendantSession
RPy_CloturerCorrecte == GP_CloturerCorrecte /\ FP_CloturerCorrecte
RPy_CloturerPhraseErronee == GP_CloturerPhraseErronee /\ FP_CloturerPhraseErronee
=============================================================================
