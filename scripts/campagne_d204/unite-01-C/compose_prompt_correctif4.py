#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif4.py — le correctif-4 de la phase source-c
(bras C) : l'épreuve D122 de la couche de hachage rend 0 VERT / 32
ROUGE — l'audit nomme TROIS fautes chirurgicales dans md5_transform
(la ronde 2 majorité au lieu de la sélection, la ronde 4 Ch au lieu de
c^(b|~d), S[i] sans modulo — rotation NULLE des rondes 16 à 63) et deux
régressions dans loupe_01_ouvrir (GENERIC_READ seul, ERROR_PATH_NOT_FOUND
absent). Le format PATCH : les remplacements exacts + la SUITE du
fichier depuis la coupure — l'outil auteur du labo assemble (comme la
notation à étiquettes du bras T)."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

entete = """Tu es le même auteur du domaine Loupe au laboratoire TRIADE — le bras C de
la campagne D204. L'ÉPREUVE DU LABO (ta couche de hachage compilée au
POSIX et confrontée au juge hashlib sur 32 tailles — les frontières du
rembourrage et l'absorption irrégulière) rend : 0 VERT, 32 ROUGE. TOUT
est faux. L'audit nomme TROIS FAUTES CHIRURGICALES dans md5_transform et
DEUX RÉGRESSIONS dans loupe_01_ouvrir. Ton édition est aussi TRONQUÉE
encore (la coupure tombe dans la boucle de lecture). Réponds au format
PATCH : les remplacements exacts, puis la SUITE du fichier.

================================================================================
L'AUDIT — LES CINQ DÉFAUTS NOMMÉS (avant toute correction, la règle)
================================================================================
D20 (la ronde 2 du MD5) : « f = G(c, d, b); » — G est ta macro MAJORITÉ ;
  la ronde 2 du MD5 est la SÉLECTION : f = (d & b) | (~d & c).
D21 (la ronde 4 du MD5) : « f = Ch(b, c, d); » — Ch est (b&c)^(~b&d) ;
  la ronde 4 du MD5 est : f = c ^ (b | ~d).
D22 (FATAL, la rotation) : « ROTL32(a + f + T[i] + w[g], S[i]) » — ta
  table S ne porte que 16 valeurs : S[i] vaut ZÉRO pour toute ronde
  i ≥ 16 (aucune rotation des rondes 16 à 63 !) — l'index est
  i % 16 : S[i % 16].
D23 (l'ouverture, accès) : « GENERIC_READ, FILE_SHARE_READ » — le
  contrat Q1 : GENERIC_READ | GENERIC_WRITE (Loupe est seul maître des
  octets qu'il montrera modifiables, I1).
D24 (l'ouverture, E1) : ERROR_PATH_NOT_FOUND manque — le contrat E1 :
  ERROR_FILE_NOT_FOUND OU ERROR_PATH_NOT_FOUND → -2.

================================================================================
TON ÉDITION ACTUELLE (tronquée — la coupure est à la ligne du ReadFile)
================================================================================
"""

format_patch = """
================================================================================
TON TRAVAIL (le correctif-4) — LE FORMAT PATCH
================================================================================
Réponds UNIQUEMENT par les DEUX sections suivantes, exactement délimitées.

###REMPLACEMENTS
une ligne par remplacement, au format EXACT :
AVANT=<la ligne fautive, copiée au caractère près>
APRÈS=<la ligne corrigée>
Les remplacements attendus (les cinq, dans l'ordre du fichier) :
1. la ligne de la ronde 2 (D20) ;
2. la ligne de la ronde 4 (D21) ;
3. la ligne de la rotation (D22) ;
4. la ligne de CreateFileW (D23 — l'accès corrigé, le reste de la ligne
   inchangé) ;
5. la ligne du verdict E1 (D24 — les deux codes d'erreur).
Et UN remplacement de suppression : la ligne « ((uint16_t*)(cadre + 0))[i]
= (uint16_t)chemin_w[i]; » de la copie du chemin au début de
loupe_01_ouvrir, ET sa boucle « for (int i = 0; i < 259 && chemin_w[i]
!= L'\\0'; ++i) » et sa ligne « ((uint16_t*)(cadre + 0))[259] = 0; » —
la copie du chemin DEMEURE mais déménage APRÈS le succès de l'ouverture
(elle vit dans la suite, avec les autres écritures du cadre — ainsi
RIEN n'est écrit au cadre sur un refus). Écris-les comme :
AVANT=<la ligne>
APRÈS=(supprimée — déménagée à la suite)
###FIN REMPLACEMENTS

###SUITE
LA SUITE DU FICHIER depuis la ligne coupée (la ligne du « if (!ReadFile(h,
morceau, a_lire, &lus, NULL) || lus == 0) break; » est DÉJÀ dans le
fichier — ta suite commence JUSTE APRÈS elle). Elle contient, dans
l'ordre :
  1. dans la boucle while : le remplissage du tampon du cadre — les
     premiers octets du fichier, jusqu'à 384 : une statique locale (ou
     un compteur déclaré avant la boucle) compte les octets déjà pris ;
     pour chaque morceau lu, copier min(lus, 384 - pris) octets de
     morceau[] vers cadre + 568 + pris (une boucle d'octets — le
     compilateur l'inline) ;
  2. dans la boucle while : md5_absorbe(&m5, morceau, lus) puis
     sha256_absorbe(&s2, morceau, lus), puis bytes_restants -= lus ;
  3. la fin de la boucle (l'accolade) ;
  4. APRÈS la boucle, les écritures du cadre : la copie du chemin
     (WCHAR par WCHAR jusqu'au L'\\0' inclus, au plus 259 + le NUL,
     vers cadre + 0), puis la taille à cadre + 520, la poignée
     (uint64_t)h à cadre + 528, la vue 0 à cadre + 536, le curseur 0 à
     cadre + 544, le remplissage min(384, taille) à cadre + 552 ;
  5. les empreintes : md5_final(&m5, panneau) puis sha256_final(&s2,
     panneau + 16) ;
  6. la session : g_session_handle = h ; puis return VERDICT_OK ; et
     l'accolade de fin de loupe_01_ouvrir ;
  7. loupe_03_fermer : si la session vit, CloseHandle et la statique à
     INVALID_HANDLE_VALUE ; retour VERDICT_OK.
###FIN SUITE

Aucun texte avant ###REMPLACEMENTS, aucun texte après ###FIN SUITE.
"""

edition = (UNITE / "source" / "loupe-01-c.c").read_text(encoding="utf-8")
prompt = entete + edition + format_patch
(UNITE / "prompts" / "correctif-4.txt").write_text(prompt, encoding="utf-8")
print(f"[composé] prompts/correctif-4.txt : {len(prompt.encode())} o")
