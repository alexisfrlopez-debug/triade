#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif2.py — le correctif-2 de la phase source-c
(bras C) : la structure est réparée (l'argument-chemin, l'ouverture
contractuelle, la session, loupe_03) mais l'audit nomme quatre défauts
nouveaux : les données exportées restées extern, la copie du chemin qui
s'écrit sur elle-même, et la couche MD5/SHA-256 cassée (le transform
SHA-256 est JUSTE — l'absorption et la finalisation ne le sont pas)."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

entete = """Tu es le même auteur du domaine Loupe au laboratoire TRIADE — le bras C de
la campagne D204. Ton correctif-1 a réparé la structure (l'argument est le
chemin, l'ouverture est contractuelle : GENERIC_READ|GENERIC_WRITE,
FILE_SHARE_READ, OPEN_EXISTING, UNE SEULE poignée ; la borne referme avant
-3 ; la session demeure ouverte après le succès ; loupe_03_fermer vit).
Ton sha256_transform est JUSTE (FIPS 180-4 vérifié ligne à ligne au labo).
Mais l'audit nomme QUATRE défauts nouveaux — dont la couche de hachage
entière. Voici ton édition et l'audit ; livre l'édition corrigée.

================================================================================
L'AUDIT — LES QUATRE DÉFAUTS NOMMÉS
================================================================================
D10 (la liaison même) : « extern char cadre[]; extern char panneau[]; » —
    une déclaration extern n'est pas une DÉFINITION : l'éditioniteur
    refuse (« cannot export cadre: symbol not defined »). Le cadre et le
    panneau sont TES DONNÉES EXPORTÉES : définis-les :
        char cadre[960];
        char panneau[48];
D11 (la copie du chemin) : ta boucle écrit « ((char*)chemin_ptr)[i] =
    (char)chemin_w[i] » — la destination EST LA SOURCE (chemin_w ==
    chemin_ptr) : une copie sur soi-même, le cadre +0 n'est JAMAIS
    écrit. La copie va de l'ENTRÉE vers TON cadre à l'offset 0, WCHAR
    par WCHAR jusqu'au L'\\0' (au plus 259 caractères + le NUL) —
    l'entrée n'est JAMAIS modifiée.
D12 (FATAL, le MD5 n'existe pas) : ton « md5 » XOR les tampons à 0x36
    (l'ipad de HMAC — rien à voir), nourrit sha256_transform d'un état
    de 4 mots (débordement : le transform lit 8 mots), et le
    rembourrement est confus. Écris LE MD5 VRAI selon RFC 1321 :
      - l'état : 4 mots A=0x67452301, B=0xEFCDAB89, C=0x98BADCFE,
        D=0x10325476 ;
      - 64 constantes T[i] = floor(abs(sin(i+1)) × 2^32), i = 0..63
        (écris la table des 64 constantes EN DUR — les valeurs
        publiques : d76aa478, e8c7b756, 242070db, c1bdceee, f57c0faf,
        4787c62a, a8304613, fd469501, 698098d8, 8b44f7af, ffff5bb1,
        895cd7be, 6b901122, fd987193, a679438e, 49b40821, f61e2562,
        c040b340, 265e5a51, e9b6c7aa, d62f105d, 02441453, d8a1e681,
        e7d3fbc8, 21e1cde6, c33707d6, f4d50d87, 455a14ed, a9e3e905,
        fcefa3f8, 676f02d9, 8d2a4c8a, fffa3942, 8771f681, 6d9d6122,
        fde5380c, a4beea44, 4bdecfa9, f6bb4b60, bebfbc70, 289b7ec6,
        eaa127fa, d4ef3085, 04881d05, d9d4d039, e6db99e5, 1fa27cf8,
        c4ac5665, f4292244, 432aff97, ab9423a7, fc93a039, 655b59c3,
        8f0ccc92, ffeff47d, 85845dd1, 6fa87e4f, fe2ce6e0, a3014314,
        4e0811a1, f7537e82, bd3af235, 2ad7d2bb, eb86d391) ;
      - les 16 décalages par groupe de 16 rondes :
        ronde 0-15 : 7, 12, 17, 22 ; ronde 16-31 : 5, 9, 14, 20 ;
        ronde 32-47 : 4, 11, 16, 23 ; ronde 48-63 : 6, 10, 15, 21 ;
      - les quatre opérations par ronde i (X = le bloc de 16 mots
        little-endian, x = i modulo 16) :
        i<16  : F=(B&C)|(~B&D)          , x=i ;
        i<32  : F=(D&B)|(~D&C)          , x=(5i+1)%16 ;
        i<48  : F=B^C^D                 , x=(3i+5)%16 ;
        i≥48  : F=C^(B|~D)              , x=(7i)%16 ;
        puis : A_new = D ; D_new = C ; C_new = B ;
               B_new = B + ROTL(A + F + T[i] + X[x], s_i) ;
      - l'absorption : chaque bloc de 64 octets → 16 mots LITTLE-ENDIAN,
        la ronde, puis état += ABCD (initialement sauvegardés) ;
      - la finalisation : le rembourrement 0x80 puis des zéros jusqu'à
        56 octets, puis la longueur TOTALE en BITS sur 8 octets
        LITTLE-ENDIAN (si le partiel ≥ 56 octets, DEUX blocs finaux) ;
      - la sortie : les 4 mots en LITTLE-ENDIAN → les 16 octets.
D13 (la finalisation SHA-256) : autour de ton transform JUSTE,
    l'absorption et la finalisation doivent suivre FIPS 180-4 :
      - absorber les blocs complets de 64 octets AU FUR ET À MESURE,
        retenir le partiel (< 64) et le compte total d'octets ;
      - la finalisation : le partiel + 0x80, des zéros jusqu'à 56
        octets (modulo 64 — si le partiel ≥ 56, un bloc ENTIER de
        zéros de plus), puis la longueur totale en BITS sur 8 octets
        BIG-ENDIAN ; UN ou DEUX transform finaux, pas plus ;
      - la sortie : les 8 mots en BIG-ENDIAN → les 32 octets.
D14 (le XOR 0x36) : c'est l'ipad de HMAC — RIEN à faire ici (le
    panneau n'est pas un HMAC) : supprimé.

================================================================================
TON ÉDITION (correctif-1 — répare ces quatre défauts, garde le reste)
================================================================================
"""

travail = """
================================================================================
TON TRAVAIL (le correctif-2)
================================================================================
Livre L'ÉDITION COMPLÈTE corrigée des deux fichiers — réponds UNIQUEMENT
par leur contenu, délimité exactement ainsi (aucun texte avant, aucun
texte après) :

###FICHIER loupe-01-c.c
(le source C complet — D10 à D14 réparés ; la structure du correctif-1
conservée : l'ouverture contractuelle, la borne, la session, la lecture
à la même poignée ; MD5 et SHA-256 en C pur, l'un et l'autre COMPLETS ;
compact : ≤ 9 000 octets)
###FIN loupe-01-c.c
###FICHIER loupe-01-c.def
(LIBRARY loupe-01-c ; EXPORTS : loupe_01_ouvrir, loupe_03_fermer,
cadre DATA, panneau DATA)
###FIN loupe-01-c.def
"""

edition = (UNITE / "source" / "loupe-01-c.c").read_text(encoding="utf-8")
prompt = entete + edition + travail
(UNITE / "prompts" / "correctif-2.txt").write_text(prompt, encoding="utf-8")
print(f"[composé] prompts/correctif-2.txt : {len(prompt.encode())} o")
