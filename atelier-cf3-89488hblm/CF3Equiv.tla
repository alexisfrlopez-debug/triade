--------------------------- MODULE CF3Equiv ---------------------------
(***************************************************************************
 * CF3Equiv — L'ÉQUIVALENCE TLA+ ↔ SÉMANTIQUE PYTHON, RÈGLE PAR RÈGLE,
 * DÉCHARGÉE PAR SMT SUR ENTIERS NON BORNÉS (l'instruction 89488hblm,
 * point (a) : « remplace la confrontation TLA+↔sémantique Python
 * échantillonnée (512 états/règle) par une équivalence déchargée par SMT
 * sur entiers non bornés, garde-à-garde et effet-à-effet, pour chacune
 * des 13 règles et tout état bien typé »).
 *
 * LES DEUX SEMANTIQUES :
 *   — CÔTÉ TLA+ : les règles RÉELLES de CF3.tla (EXTENDS CF3 — le module
 *     est la pièce consignée, copie recoupée md5 b762c2c8… ; ZÉRO
 *     retranscription pour les relations : VoleKUser, …, CloturerPhraseErronee
 *     sont utilisées TELLES QUELLES). Seule la GARDE non-amorcée GT_r est
 *     transcrite (l'extraction non-amorcée de la règle) — et sa fidélité
 *     est ÉPINGLÉE par le couple de contrôles ci-dessous (garde + relation).
 *   — CÔTÉ PYTHON : la transcription FIDÈLE de modele_invariant_v150.py
 *     (actions_possibles = l'offre ; appliquer ≠ None = la garde EFFECTIVE ;
 *     l'effet = les affectations de appliquer). GP_r = la garde effective,
 *     FP_r = l'effet. Le seuil Python est LITTÉRAL :
 *     Cardinality(sait ∩ Elements) ≥ 3 (le code lit len(sait & ELEMENTS)) —
 *     l'égalité avec Cardinality(sait) sous TypeOK est CONTENU DE LA PREUVE.
 *
 * LES OBLIGATIONS (par règle r, toute quantification sur les états BIEN
 * TYPÉS — e ∈ Int NON BORNÉ) :
 *   EQUIV_GARDE_r == GP_r <=> GT_r            (longueur 0 : Init = TypeOK)
 *   EQUIV_EFFET_r == CF3.r ≡ (GP_r ∧ FP_r)  (longueur 1 : Next = le XOR
 *     des deux relations, Inv = FALSE, --no-deadlock ; NoError ⟹ les
 *     relations sont ÉGALES — la garde ET l'effet, contre la règle RÉELLE)
 *   La décomposition : le XOR relationnel se scinde en différence de
 *   gardes et différence d'effets ; EQUIV_GARDE isole l'aspect garde,
 *   EQUIV_EFFET (la relation contre l'artefact réel) porte l'aspect effet
 *   et rescouvre la garde — ensemble elles SONT le « garde-à-garde et
 *   effet-à-effet » exigé. Les effets sont DÉTERMINISTES (13 règles,
 *   l'image est fonction de l'état) : l'égalité relationnelle entraîne
 *   l'égalité des gardes ET des fonctions d'effet.
 *
 * LA CORRESPONDANCE DES NOMS (Python → TLA+) : vole_K_user → VoleKUser,
 * vole_S_serrure → VoleSSerrure, vole_S_piège → VoleSPiege,
 * falsifie_conteneur → FalsifieConteneur, falsifie_piège → FalsifiePiege,
 * rejoue_époque_passée → RejoueEpoquePassee, ouvrir_correct → OuvrirCorrect,
 * ouvrir_phrase_erronée → OuvrirPhraseErronee, ouvrir_ancien_couple →
 * OuvrirAncienCouple, verifier → Verifier, crash_pendant_session →
 * CrashPendantSession, clôturer_correcte → CloturerCorrecte,
 * clôturer_phrase_erronée → CloturerPhraseErronee.
 ***************************************************************************)

EXTENDS CF3

\* le seuil PYTHON, LITTÉRAL (len(sait & ELEMENTS) >= 3)
SeuilPy == Cardinality(sait \intersect Elements) >= 3

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
 * LA SÉMANTIQUE PYTHON — la transcription fidèle de
 * modele_invariant_v150.py (actions_possibles : l'OFFRE ; appliquer :
 * la garde effective — None = refus — et l'effet).
 ***************************************************************************)

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

\* 4 : falsifie_conteneur — offert toujours ; EFFECTIF : piège intègre ET
\*     canonique (appliquer : if trap_ok and phase == "canonique")
GP_FalsifieConteneur == trap_ok /\ phase = "canonique"
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

(***************************************************************************
 * LES RELATIONS PYTHON (garde effective ∧ effet) — contre les règles
 * RÉELLES de CF3.tla dans les XOR.
 ***************************************************************************)

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

(***************************************************************************
 * LES OBLIGATIONS GARDE-À-GARDE (longueur 0, Init = TypeOK) — la garde
 * Python (effective) contre la garde TLA+ (extraite).
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
 * LES XOR RELATIONNELS (longueur 1, Inv = FALSE, --no-deadlock) — la
 * règle RÉELLE de CF3.tla contre la relation Python : NoError ⟹
 * ÉGALITÉ des relations (garde ET effet) sur tout état bien typé.
 ***************************************************************************)

XOR_VoleKUser == (VoleKUser /\ ~ RPy_VoleKUser) \/ (~ VoleKUser /\ RPy_VoleKUser)
XOR_VoleSSerrure == (VoleSSerrure /\ ~ RPy_VoleSSerrure) \/ (~ VoleSSerrure /\ RPy_VoleSSerrure)
XOR_VoleSPiege == (VoleSPiege /\ ~ RPy_VoleSPiege) \/ (~ VoleSPiege /\ RPy_VoleSPiege)
XOR_FalsifieConteneur == (FalsifieConteneur /\ ~ RPy_FalsifieConteneur) \/ (~ FalsifieConteneur /\ RPy_FalsifieConteneur)
XOR_FalsifiePiege == (FalsifiePiege /\ ~ RPy_FalsifiePiege) \/ (~ FalsifiePiege /\ RPy_FalsifiePiege)
XOR_RejoueEpoquePassee == (RejoueEpoquePassee /\ ~ RPy_RejoueEpoquePassee) \/ (~ RejoueEpoquePassee /\ RPy_RejoueEpoquePassee)
XOR_OuvrirCorrect == (OuvrirCorrect /\ ~ RPy_OuvrirCorrect) \/ (~ OuvrirCorrect /\ RPy_OuvrirCorrect)
XOR_OuvrirPhraseErronee == (OuvrirPhraseErronee /\ ~ RPy_OuvrirPhraseErronee) \/ (~ OuvrirPhraseErronee /\ RPy_OuvrirPhraseErronee)
XOR_OuvrirAncienCouple == (OuvrirAncienCouple /\ ~ RPy_OuvrirAncienCouple) \/ (~ OuvrirAncienCouple /\ RPy_OuvrirAncienCouple)
XOR_Verifier == (Verifier /\ ~ RPy_Verifier) \/ (~ Verifier /\ RPy_Verifier)
XOR_CrashPendantSession == (CrashPendantSession /\ ~ RPy_CrashPendantSession) \/ (~ CrashPendantSession /\ RPy_CrashPendantSession)
XOR_CloturerCorrecte == (CloturerCorrecte /\ ~ RPy_CloturerCorrecte) \/ (~ CloturerCorrecte /\ RPy_CloturerCorrecte)
XOR_CloturerPhraseErronee == (CloturerPhraseErronee /\ ~ RPy_CloturerPhraseErronee) \/ (~ CloturerPhraseErronee /\ RPy_CloturerPhraseErronee)

(* L'invariant bidon des contrôles relationnels : toute transition du XOR
 * est un contre-exemple. *)
Faux == FALSE
=============================================================================
