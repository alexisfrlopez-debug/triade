------------------------ MODULE CF3EquivControles -----------------------
(***************************************************************************
 * CF3EquivControles — LES 26 CONTRÔLES NÉGATIFS DU POINT (a) : UN PAR
 * OBLIGATION (l'instruction 89488hblm : « ajoute-en un par nouvelle
 * obligation (affaiblissement volontaire devant être attrapé) »).
 *
 * CHAQUE contrôle est une FAUTE DE TRANSCRIPTION PLAUSIBLE du côté
 * PYTHON (le côté TLA+ est la règle réelle de CF3.tla — c'est la
 * transcription Python que les obligations gardent) : une garde
 * amputée ou chargée d'une condition étrangère, un effet qui vise le
 * mauvais composant. Chacune DOIT être attrapée (Error 12 attendu) —
 * la preuve que les obligations EQUIV_GARDE / EQUIV_EFFET mordent.
 *
 * Les 13 contrôles GARDE : Inv = (GPw_r ⟺ GT_r), Init = TypeOK,
 * longueur 0. Les 13 contrôles EFFET : Next = le XOR de la règle
 * RÉELLE contre la relation Python MUTÉE (garde intacte, effet muté :
 * RPyw_r == GP_r ∧ FPw_r), Inv = FALSE, longueur 1, --no-deadlock.
 ***************************************************************************)

EXTENDS CF3Equiv

(***************************************************************************
 * LES GARDES MUTÉES (GPw) — l'affaiblissement volontaire de chaque
 * obligation GARDE.
 ***************************************************************************)

\* 1 : le vol K_user restreint à tort au canonique (l'offre confondue)
GPw_VoleKUser == phase = "canonique"
\* 2 : le vol S_serrure conditionné au piège (une condition étrangère)
GPw_VoleSSerrure == trap_ok
\* 3 : le vol S_piège réservé à la classe ≥ 2 (l'époque lue à tort)
GPw_VoleSPiege == e > 1
\* 4 : la falsification du conteneur SANS l'exigence canonique — LA
\*     simplification fausse que la campagne PBT a croisée (l'écart de
\*     couverture v0.15.0 : la sentinelle court sur le canonique)
GPw_FalsifieConteneur == trap_ok
\* 5 : le piège falsifiable même indisponible (le tag jamais testé)
GPw_FalsifiePiege == TRUE
\* 6 : le rejeu accepté dès l'époque 1 (le e > 1 oublié)
GPw_RejoueEpoquePassee == TRUE
\* 7 : l'ouverture correcte SANS la branche honnête (K_user ∉ sait
\*     amputé — l'honnête ne peut plus ouvrir son brouillon)
GPw_OuvrirCorrect ==
  /\ phase = "canonique"
  /\ trap_ok
  /\ KUser \in sait
  /\ SeuilPy
\* 8 : la phrase erronée offerte au brouillon aussi
GPw_OuvrirPhraseErronee == TRUE
\* 9 : l'ancien couple accepté dès l'époque 1 (le e > 1 oublié)
GPw_OuvrirAncienCouple == phase = "canonique"
\* 10 : la vérification offerte au brouillon aussi
GPw_Verifier == TRUE
\* 11 : le crash réservé au brouillon (le canonique ne peut plus crasher)
GPw_CrashPendantSession == phase = "brouillon"
\* 12 : la clôture au piège indisponible (le trap_ok oublié)
GPw_CloturerCorrecte == phase = "brouillon"
\* 13 : la clôture erronée offerte au canonique
GPw_CloturerPhraseErronee == TRUE

(* les obligations AFFAIBLIES — le vérificateur DOIT produire un
 * contre-exemple pour chacune *)
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

(***************************************************************************
 * LES EFFETS MUTÉS (FPw) — la garde Python INTACTE, l'effet dévié.
 ***************************************************************************)

\* 1 : le vol qui prend le MAUVAIS ÉLÉMENT (S_serrure au lieu de K_user)
FPw_VoleKUser ==
  /\ sait' = sait \union {SSerrure}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 2 : le vol SANS EFFET (le savoir jamais augmenté)
FPw_VoleSSerrure == UNCHANGED vars
\* 3 : le vol qui prend DEUX éléments d'un coup
FPw_VoleSPiege ==
  /\ sait' = sait \union {KUser, SPiege}
  /\ UNCHANGED <<e, phase, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 4 : la destruction qui DÉBORDE sur le média (la confusion P3/P4)
FPw_FalsifieConteneur ==
  /\ detruit' = TRUE
  /\ media_corrompu' = TRUE
  /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte,
                 destr_injuste>>
\* 5 : le piège cassé qui DÉTRUIT (la falsification jamais anodine)
FPw_FalsifiePiege ==
  /\ trap_ok' = FALSE
  /\ detruit' = TRUE
  /\ UNCHANGED <<e, phase, sait, cf2_ok, secret, accepte,
                 destr_injuste, media_corrompu>>
\* 6 : LE ROLL-BACK — le rejeu qui DÉCRÔIT l'époque (la faute P2)
FPw_RejoueEpoquePassee ==
  /\ e' = e - 1
  /\ UNCHANGED <<phase, sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 7 : le secret TOUJOURS appris — même la branche honnête (la faute P1)
FPw_OuvrirCorrect ==
  /\ phase' = "brouillon"
  /\ secret' = TRUE
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 8 : la phrase erronée qui OUVRE une session
FPw_OuvrirPhraseErronee ==
  /\ phase' = "brouillon"
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 9 : l'ancien couple qui OUVRE une session (le rejeu accepté)
FPw_OuvrirAncienCouple ==
  /\ phase' = "brouillon"
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 10 : la vérification qui ACCEPTE (le rejeu entériné — la faute P2)
FPw_Verifier ==
  /\ accepte' = TRUE
  /\ UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, detruit,
                 destr_injuste, media_corrompu>>
\* 11 : le crash qui AVALE une époque
FPw_CrashPendantSession ==
  /\ phase' = "canonique"
  /\ e' = e + 1
  /\ UNCHANGED <<sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 12 : la clôture qui n'AVANCE PAS l'époque (la faute P2)
FPw_CloturerCorrecte ==
  /\ phase' = "canonique"
  /\ UNCHANGED <<e, sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>
\* 13 : la phrase erronée qui SCELLE (clôture effective)
FPw_CloturerPhraseErronee ==
  /\ phase' = "canonique"
  /\ e' = e + 1
  /\ UNCHANGED <<sait, trap_ok, cf2_ok, secret, accepte, detruit,
                 destr_injuste, media_corrompu>>

(* les relations Python mutées (garde intacte ∧ effet muté) *)
RPyw_VoleKUser == GP_VoleKUser /\ FPw_VoleKUser
RPyw_VoleSSerrure == GP_VoleSSerrure /\ FPw_VoleSSerrure
RPyw_VoleSPiege == GP_VoleSPiege /\ FPw_VoleSPiege
RPyw_FalsifieConteneur == GP_FalsifieConteneur /\ FPw_FalsifieConteneur
RPyw_FalsifiePiege == GP_FalsifiePiege /\ FPw_FalsifiePiege
RPyw_RejoueEpoquePassee == GP_RejoueEpoquePassee /\ FPw_RejoueEpoquePassee
RPyw_OuvrirCorrect == GP_OuvrirCorrect /\ FPw_OuvrirCorrect
RPyw_OuvrirPhraseErronee == GP_OuvrirPhraseErronee /\ FPw_OuvrirPhraseErronee
RPyw_OuvrirAncienCouple == GP_OuvrirAncienCouple /\ FPw_OuvrirAncienCouple
RPyw_Verifier == GP_Verifier /\ FPw_Verifier
RPyw_CrashPendantSession == GP_CrashPendantSession /\ FPw_CrashPendantSession
RPyw_CloturerCorrecte == GP_CloturerCorrecte /\ FPw_CloturerCorrecte
RPyw_CloturerPhraseErronee == GP_CloturerPhraseErronee /\ FPw_CloturerPhraseErronee

(* les XOR des contrôles effet : la règle RÉELLE contre la relation
 * mutée — chacun DOIT trouver un contre-exemple *)
XORw_VoleKUser == (VoleKUser /\ ~ RPyw_VoleKUser) \/ (~ VoleKUser /\ RPyw_VoleKUser)
XORw_VoleSSerrure == (VoleSSerrure /\ ~ RPyw_VoleSSerrure) \/ (~ VoleSSerrure /\ RPyw_VoleSSerrure)
XORw_VoleSPiege == (VoleSPiege /\ ~ RPyw_VoleSPiege) \/ (~ VoleSPiege /\ RPyw_VoleSPiege)
XORw_FalsifieConteneur == (FalsifieConteneur /\ ~ RPyw_FalsifieConteneur) \/ (~ FalsifieConteneur /\ RPyw_FalsifieConteneur)
XORw_FalsifiePiege == (FalsifiePiege /\ ~ RPyw_FalsifiePiege) \/ (~ FalsifiePiege /\ RPyw_FalsifiePiege)
XORw_RejoueEpoquePassee == (RejoueEpoquePassee /\ ~ RPyw_RejoueEpoquePassee) \/ (~ RejoueEpoquePassee /\ RPyw_RejoueEpoquePassee)
XORw_OuvrirCorrect == (OuvrirCorrect /\ ~ RPyw_OuvrirCorrect) \/ (~ OuvrirCorrect /\ RPyw_OuvrirCorrect)
XORw_OuvrirPhraseErronee == (OuvrirPhraseErronee /\ ~ RPyw_OuvrirPhraseErronee) \/ (~ OuvrirPhraseErronee /\ RPyw_OuvrirPhraseErronee)
XORw_OuvrirAncienCouple == (OuvrirAncienCouple /\ ~ RPyw_OuvrirAncienCouple) \/ (~ OuvrirAncienCouple /\ RPyw_OuvrirAncienCouple)
XORw_Verifier == (Verifier /\ ~ RPyw_Verifier) \/ (~ Verifier /\ RPyw_Verifier)
XORw_CrashPendantSession == (CrashPendantSession /\ ~ RPyw_CrashPendantSession) \/ (~ CrashPendantSession /\ RPyw_CrashPendantSession)
XORw_CloturerCorrecte == (CloturerCorrecte /\ ~ RPyw_CloturerCorrecte) \/ (~ CloturerCorrecte /\ RPyw_CloturerCorrecte)
XORw_CloturerPhraseErronee == (CloturerPhraseErronee /\ ~ RPyw_CloturerPhraseErronee) \/ (~ CloturerPhraseErronee /\ RPyw_CloturerPhraseErronee)
=============================================================================
