#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif3.py — le correctif-3 de la phase source-c
(bras C) : l'audit du correctif-2 nomme la couche de hachage encore
cassée (rondes MD5 2/4 fausses, ROTL absent, absorption incohérente,
sha256_buf jamais rempli, sha5_buf, finalisation sha256 à deux blocs
fausse) et la troncature (la fin du fichier + le .def manquent — le
.def du correctif-1 est retenu, juste). Le correctif-3 PRESCRIT
l'architecture incrémentale exacte."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

entete = """Tu es le même auteur du domaine Loupe au laboratoire TRIADE — le bras C de
la campagne D204. L'audit du labo sur ton correctif-2 : la STRUCTURE est
bonne (les données définies, l'ouverture contractuelle, la session, la
borne), tes TABLES sont justes (T[64] complet, S par index modulo,
sha256_transform conforme FIPS 180-4, la finalisation MD5 à deux blocs),
MAIS la couche de hachage reste CASSÉE et l'édition est TRONQUÉE encore
(la limite de complétion coupa dans loupe_01_ouvrir). Ce correctif
PRESCRIT l'architecture exacte — suis-la à la lettre.

================================================================================
L'AUDIT — LES DÉFAUTS NOMMÉS DU CORRECTIF-2
================================================================================
D15 (les rondes MD5 2 et 4 sont FAUSSES) : ta ronde 2 appelle G(c,d,b)
    = la MAJORITÉ — la vraie ronde 2 du MD5 est f = (d & b) | (~d & c) ;
    ta ronde 4 appelle Ch(b,c,d) = (b&c)^(~b&d) — la vraie ronde 4 est
    f = c ^ (b | ~d). Les QUATRE rondes exactes (w = le bloc en 16 mots
    LITTLE-ENDIAN, g l'index du mot) :
      i < 16 : f = (b & c) | (~b & d)  ; g = i
      i < 32 : f = (d & b) | (~d & c)  ; g = (5*i + 1) % 16
      i < 48 : f = b ^ c ^ d           ; g = (3*i + 5) % 16
      i < 64 : f = c ^ (b | ~d)        ; g = (7*i) % 16
    puis la ronde : temp = d ; d = c ; c = b ;
    b = b + ROTL32(a + f + T[i] + w[g], S[i % 16]) ; a = temp ;
    et à la fin état[0..3] += a,b,c,d. Ajoute la macro manquante :
    #define ROTL32(x, n) (((x) << (n)) | ((x) >> (32 - (n))))
D16 (l'absorption est incohérente) : tes compteurs « (md5_len + 63)/64
    - 1 » transforment le MAUVAIS tampon le MAUVAIS nombre de fois, et
    sha256_buf n'est JAMAIS rempli (la lecture va dans md5_buf seul) —
    sans compter la coquille « sha5_buf ». Remplace TOUTE la couche par
    L'ARCHITECTURE INCRÉMENTALE PRESCRITE ci-dessous.
D17 (la finalisation SHA-256 à deux blocs est fausse) : ton « if
    (sha256_part_len >= 56) transform; transform; » transforme le même
    bloc deux fois — suis la finalisation prescrite.
D18 (la troncature) : la fin de loupe_01_ouvrir (la copie du chemin au
    CADRE +0 — jamais sur l'entrée même —, la pose du cadre, la lecture
    du tampon, la naissance du panneau, la session), loupe_03_fermer
    entier, et le .def manquent. Le .def retenu (celui de ton
    correctif-1, juste) :
        LIBRARY loupe-01-c
        EXPORTS
            loupe_01_ouvrir
            loupe_03_fermer
            cadre DATA
            panneau DATA
D19 (la copie du chemin) : elle va de l'ENTRÉE vers TON cadre à
    l'offset 0, WCHAR par WCHAR, jusqu'au L'\\0' inclus (au plus 259
    caractères + le NUL) — l'entrée n'est JAMAIS modifiée :
        for (i = 0; i < 259 && chemin_w[i] != 0; ++i)
            ((uint16_t*)(cadre + 0))[i] = (uint16_t)chemin_w[i];
        ((uint16_t*)(cadre + 0))[i] = 0;

================================================================================
L'ARCHITECTURE INCRÉMENTALE PRESCRITE (les deux empreintes, exactement)
================================================================================
    /* UN contexte PAR empreinte — l'absorption et la finalisation */
    typedef struct { uint32_t etat[4]; uint8_t tampon[64];
                     uint32_t rempli; uint64_t total; } ctx_md5;
    typedef struct { uint32_t etat[8]; uint8_t tampon[64];
                     uint32_t rempli; uint64_t total; } ctx_sha256;

    md5_absorbe(ctx_md5 *c, const uint8_t *d, uint32_t n) :
        pour chaque octet : c->tampon[c->rempli++] = d[k] ; c->total++ ;
        si c->rempli == 64 : md5_transform(c->etat, c->tampon) ;
        c->rempli = 0 ;
    sha256_absorbe : la même chose avec sha256_transform.

    md5_final(ctx_md5 *c, uint8_t sortie[16]) :
        uint64_t bits = c->total * 8 ;
        c->tampon[c->rempli++] = 0x80 ;
        si c->rempli > 56 : { zéros de rempli à 64 ; md5_transform ;
                             rempli = 0 ; }
        zéros de rempli à 56 ;
        la longueur bits sur 8 octets LITTLE-ENDIAN à tampon[56..63] ;
        md5_transform ;
        sortie : etat[0..3], chacun en LITTLE-ENDIAN → 16 octets.
    sha256_final(ctx_sha256 *c, uint8_t sortie[32]) :
        uint64_t bits = c->total * 8 ;
        c->tampon[c->rempli++] = 0x80 ;
        si c->rempli > 56 : { zéros de rempli à 64 ; sha256_transform ;
                             rempli = 0 ; }
        zéros de rempli à 56 ;
        la longueur bits sur 8 octets BIG-ENDIAN à tampon[56..63] ;
        sha256_transform ;
        sortie : etat[0..7], chacun en BIG-ENDIAN → 32 octets.

    /* la lecture : UN SEUL passage nourrit les DEUX empreintes */
    uint8_t morceau[4096] ;  /* sur la pile */
    while (reste > 0) {
        uint32_t a_lire = (reste > 4096) ? 4096 : reste ;
        DWORD lus = 0 ;
        if (!ReadFile(h, morceau, a_lire, &lus, NULL) || lus == 0) break ;
        md5_absorbe(&m5, morceau, lus) ;
        sha256_absorbe(&s2, morceau, lus) ;
        reste -= lus ;
    }
    md5_final(&m5, panneau) ;            /* les 16 premiers octets */
    sha256_final(&s2, panneau + 16) ;    /* les 32 suivants */

================================================================================
TON ÉDITION CORRIGÉE (le correctif-2 — structure conservée, couches
cassées à remplacer ; le début jusqu'à md5_transform est à reprendre,
l'absorption et la finalisation à réécrire selon la prescription)
================================================================================
"""

travail = """
================================================================================
TON TRAVAIL (le correctif-3)
================================================================================
Livre LE FICHIER loupe-01-c.c SEUL, COMPLET, corrigé selon la
prescription — réponds UNIQUEMENT par son contenu, délimité exactement
ainsi (aucun texte avant, aucun texte après ; le .def est déjà retenu,
ne le réécris pas) :

###FICHIER loupe-01-c.c
(le source C complet : <windows.h> + <stdint.h> seuls ; les rondes MD5
exactes (D15), l'architecture incrémentale prescrite (D16/D17), la fin
de loupe_01_ouvrir et loupe_03_fermer (D18), la copie du chemin au
cadre (D19) ; COMPACT : ≤ 8 500 octets, commentaires d'une ligne,
aucune bannière)
###FIN loupe-01-c.c
"""

edition = (UNITE / "source" / "loupe-01-c.c").read_text(encoding="utf-8")
prompt = entete + edition + travail
(UNITE / "prompts" / "correctif-3.txt").write_text(prompt, encoding="utf-8")
print(f"[composé] prompts/correctif-3.txt : {len(prompt.encode())} o")
