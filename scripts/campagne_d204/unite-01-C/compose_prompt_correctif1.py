#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif1.py — le correctif-1 de la phase source-c (bras
C) : la première édition revint TRONQUÉE (la limite de complétion coupa à
« // loupe_03_fermer ») et l'audit du labo nomma les défauts. Le correctif
livre l'édition COMPLÈTE corrigée des deux fichiers."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

entete = """Tu es le même auteur du domaine Loupe au laboratoire TRIADE — le bras C de
la campagne D204 (le flux conventionnel, C + gcc). Tu viens d'écrire la
première édition du source C de loupe-01 · ouvrir : elle revint TRONQUÉE
(la limite de complétion la coupa pile avant le corps de loupe_03_fermer —
le .def manque aussi) et l'AUDIT DU LABO nomma des défauts. Voici TOUT :
tes notes, l'oracle, le juge exact, l'audit, et ton édition tronquée.
Livre maintenant L'ÉDITION COMPLÈTE CORRIGÉE.

================================================================================
RAPPEL DU MÉCANISME (les faits — ta pièce affronte ceci)
================================================================================
- la pièce : UNE DLL PE32+ x86-64, « gcc -O2 -shared -o loupe-01-c.dll
  loupe-01-c.c loupe-01-c.def » ;
- au terrain : LoadLibraryEx DONT_RESOLVE — AUCUN import résolu, AUCUN
  point d'entrée exécuté, LE CRT JAMAIS INITIALISÉ : AUCUN appel CRT dans
  ton code (memset, memcpy, strlen… interdits — le compilateur INLINE les
  boucles à -O2, vérifié au labo : écris des boucles, jamais l'appel) ;
- le scénario résout LUI-MÊME les six feuilles kernel32 dans TA table
  d'imports réelle : CreateFileW, GetFileSizeEx, SetFilePointerEx,
  ReadFile, CloseHandle, GetLastError ;
- le scénario découvre tes adresses PAR TA TABLE D'EXPORTS :
    loupe_01_ouvrir(chemin)   la fonction — L'ARGUMENT EST LE CHEMIN
                              (un pointeur vers UTF-16 NUL-terminé),
                              retour long long ;
    loupe_03_fermer()         la clôture — referme la session si elle
                              vit (CloseHandle, la statique → INVALIDE),
                              retour long long ;
    cadre    DONNÉE exportée — TON TABLEAU GLOBAL de 960 octets, à plat ;
    panneau  DONNÉE exportée — TON TABLEAU GLOBAL de 48 octets ;
- le juge appelle loupe_01_ouvrir(chemin), lit TON cadre exporté aux
  offsets du plan (chemin +0 (520 o), taille +520 (8), poignée +528 (8),
  vue +536 (8), curseur +544 (8), remplissage +552 (4), charge +556 (4),
  tampon +568 (384), marge +952 (8)) et TON panneau (md5 16 o puis
  sha256 32 o du fichier ENTIER).

================================================================================
L'AUDIT DU LABO — LES DÉFAUTS NOMMÉS DE TON ÉDITION TRONQUÉE
================================================================================
D1 (FATAL, l'argument confondu) : tu écris « cadre = (char*)p_cadre » —
    NON : l'argument de loupe_01_ouvrir EST LE CHEMIN ; le cadre EST TA
    DONNÉE EXPORTÉE (le tableau global de 960 octets), pas un pointeur
    reçu. La signature juste : long long loupe_01_ouvrir(const void
    *chemin_ptr) — et le chemin s'y lit, le cadre s'écrit chez toi.
D2 (FATAL, la copie du chemin) : ta boucle d'octets « if
    ((char*)chemin_w)[i] == 0 break » s'arrête au PREMIER octet haut
    UTF-16 (il est 0 pour tout caractère ASCII !) — la copie doit être
    WCHAR PAR WCHAR jusqu'au L'\\0' (au plus 259 + le NUL).
D3 (le partage) : l'ouverture doit offrir FILE_SHARE_READ (I1 :
    « FILE_SHARE_READ offert aux autres ») — tu ouvres avec dwShareMode=0.
    L'accès : GENERIC_READ|GENERIC_WRITE (Q1), OPEN_EXISTING.
D4 (FATAL, la double ouverture) : calculer_panneau(chemin) ré-OUVRE le
    fichier par un second CreateFileW — AUCUNE seconde ouverture : le
    panneau se nourrit DE LA MÊME POIGNÉE, dans le même passage de
    lecture que la fenêtre (ou un second ReadFile sur la même poignée
    après un SetFilePointerEx à 0 — ton choix d'ingénieur).
D5 (les appels CRT) : « memset(md5_buf, 0, 64) » — INTERDIT : le CRT
    n'est jamais initialisé. Écris des boucles d'initialisation (le
    compilateur les inline à -O2 — vérifié au labo) ou des statiques.
D6 (la compilation même) : tu redéfinis ERROR_FILE_NOT_FOUND,
    ERROR_PATH_NOT_FOUND, ERROR_SHARING_VIOLATION — windows.h les définit
    DÉJÀ (constantes de macro) : la compilation refuse. Utilise-les
    telles quelles. Et uint32_t/uint8_t exigent <stdint.h>.
D7 (la troncature) : loupe_03_fermer n'a pas de corps, le .def manque.
D8 (l'état après succès) : la session DEMEURE OUVERTE après un succès
    (ta statique retient la poignée) — loupe_03_fermer seule referme ;
    au refus -5 (E4), RIEN n'est touché : ni cadre, ni panneau, ni
    système (la vérification de session est LE PREMIER geste).
D9 (la compacité) : la limite de complétion coupa ton édition (les
    commentaires trop longs) — cette fois : COMPACT (le .c ≤ 8 500
    octets, une ligne de commentaire par clause honorée, pas de bannière).

================================================================================
LE JUGE EXACT (le code qui jouera contre ta pièce — extrait du scénario)
================================================================================
    # le juge lit TA pièce par TA table d'exports, aux offsets du plan :
    TAILLE, POIGNEE = 520, 528
    VUE, CURSEUR, REMPL, TAMPON = 536, 544, 552, 568

    # V1 : les témoins (temoin-1.bin 1 o, temoin-384.bin 384 o,
    # temoin-3f.bin 196 609 o, vide.bin 0 o) :
    r = appeler_ouvrir(nom_utf16 + NUL)
    attendu : r == 0, cadre_chemin() == nom (L'ENTRÉE MÊME, le nom
              relatif), cadre[TAILLE] == taille du fichier,
              cadre[VUE] == 0, cadre[CURSEUR] == 0,
              cadre[REMPL] == min(384, taille),
              cadre[TAMPON:rempl] == donnees[:rempl]
    modele = hashlib.md5(donnees).digest() + hashlib.sha256(donnees).digest()
    attendu : panneau() == modele   # LE VIDE AUSSI
    LOUPE03()                        # entre chaque témoin

    # V2 : absent → -2 ; verrouillé (le juge TIENT le fichier sans
    # partage, dwShareMode 0) → -7 ; l'accès refusé : NOMMÉ ABSENT.

    # V3 : la borne 2 Gio + 1 (un fichier réel posé épars) → -3, la
    #      poignée fermée AVANT le retour ;
    #      la session double : ouvrir temoin-384 (succès), puis ouvrir
    #      temoin-1 → -5 ET le cadre (960 o) ET le panneau relus
    #      IDENTIQUES octet par octet ; puis LOUPE03() ;
    #      le chemin de 260 caractères sans NUL (le NUL vit à l'octet
    #      520 du tampon du juge) : le système refuse lui-même —
    #      r ∈ {-2, -5, -6} accepté, RIEN au cadre.

================================================================================
TON ÉDITION TRONQUÉE (intégrale — répare-la, ne recommence pas à l'aveugle)
================================================================================
"""

travail = """
================================================================================
TON TRAVAIL (le correctif-1 de la phase source-c)
================================================================================
Livre L'ÉDITION COMPLÈTE CORRIGÉE des deux fichiers — réponds UNIQUEMENT
par leur contenu, délimité exactement ainsi (aucun texte avant, aucun
texte après) :

###FICHIER loupe-01-c.c
(le source C complet et compact — <windows.h> + <stdint.h> seuls ; les
défauts D1 à D8 réparés ; MD5 et SHA-256 en C pur, corrects aux
frontières du rembourrage — 55, 56, 63, 64, 65, 119, 120 octets —
l'initial/le comptage 64 bits, le remplissage 0x80 puis les zéros, la
longueur en bits little-endian (md5) / big-endian (sha256) ; une ligne
de commentaire par clause du contrat honorée, pas de bannière)
###FIN loupe-01-c.c
###FICHIER loupe-01-c.def
(LIBRARY loupe-01-c ; EXPORTS : loupe_01_ouvrir, loupe_03_fermer,
cadre DATA, panneau DATA)
###FIN loupe-01-c.def
"""

edition = (UNITE / "source" / "loupe-01-c.c").read_text(encoding="utf-8")
prompt = entete + edition + travail
(UNITE / "prompts" / "correctif-1.txt").write_text(prompt, encoding="utf-8")
print(f"[composé] prompts/correctif-1.txt : {len(prompt.encode())} o "
      f"(édition tronquée embarquée : {len(edition.encode())} o)")
