--------------------- MODULE CF3PythonControlesEtendu --------------------
(***************************************************************************
 * CF3PythonControlesEtendu — LES 26 MUTATIONS SUR LE MODÈLE ÉTENDU : les
 * fautes de
 * transcription PLAUSIBLES du côté PYTHON (l'instruction 89488hblm :
 * « ajoute-en un par nouvelle obligation (affaiblissement volontaire
 * devant être attrapé) »). CHACUNE doit être ATTRAPÉE — la preuve que
 * les obligations EQUIV_GARDE / EQUIV_IMAGE mordent.
 *
 * Les 13 gardes mutées GPw (l'obligation GARDE : GPw_r ⟺ GT_r DOIT
 * tomber) et les 13 effets mutés FPw (la garde intacte, l'effet dévié —
 * l'obligation IMAGE : les images DOIVENT diverger).
 ***************************************************************************)

EXTENDS CF3PythonEtendu

\* ---- LES GARDES MUTÉES -------------------------------------------------
\* 1 : le vol K_user restreint à tort au canonique (l'offre confondue)
GPw_VoleKUser == phase = "canonique"
\* 2 : le vol S_serrure conditionné au piège (une condition étrangère)
GPw_VoleSSerrure == trap_ok
\* 3 : le vol S_piège réservé à la classe ≥ 2 (l'époque lue à tort)
GPw_VoleSPiege == e > 1
\* 4 : L'EXTENSION ANNULÉE — la garde v0.15.0 restaurée (canonique
\*     seul) : la mutation de 89488hblm (trap_ok) fut ADOPTÉE par
\*     5ey7gmjra comme la VÉRITÉ (la sentinelle concrète) ; l'ancienne
\*     vérité devient LA MUTATION — à phase = "brouillon" le mutant
\*     refuse ce que la règle étendue tire : l'écart des 660 traces
\*     renaîtrait
GPw_FalsifieConteneur == trap_ok /\ phase = "canonique"
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

\* ---- LES EFFETS MUTÉS (garde intacte, effet dévié) ---------------------
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

\* les relations mutées (garde intacte ∧ effet muté)
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
=============================================================================
