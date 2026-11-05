#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9d.py — LE PLAN au geste « LA FAMILLE aead NOTÉE-MESURÉE-PROUVÉE » :
la rangée du chantier M9-(b) porte la famille aead, l'État du programme la
consigne. Deux remplacements ASSERTÉS — tout ancrage manquant = ÉCHEC NOMMÉ,
rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

ANCRE_B = ("; **la famille aead (tls13-15..19) ATTEND SON GESTE — les slots à "
           "la suite de 0xDCC0** |")
SUITE_B = ("; **LA FAMILLE aead (tls13-15..19) NOTÉE-MESURÉE-PROUVÉE le "
           "07/11/2026 (Entrée 173)** : AES-128 le déploiement des clés de "
           "tour (**L'ARRÊT AES-NI** : AESKEYGENASSIST le SubWord/RotWord "
           "MATÉRIEL — aucune table logicielle indexée par la clé, la faille "
           "que la charte § 3 interdit ; pshufd 0xFF la diffusion du mot "
           "d'AES-128 au dword 3 [la disposition DÉRIVÉE DE L'OBSERVATION — "
           "la sonde du labo], la recette préfixe-XOR ⊕ t CONTRE-PROUVÉE sur "
           "C.1, les DIX Rcon en IMMÉDIATS, les dix tours DÉROULÉS — AUCUN "
           "saut, AUCUN déplacement RIP), AES-128 le chiffrement d'un bloc "
           "(pxor + NEUF AESENC + AESENCLAST — **LA BRIQUE D'INVERSION "
           "N'EXISTE PAS** : l'ouverture re-chiffre les compteurs, AES en "
           "sens unique), GHASH la multiplication GF(2^128) (la marche de "
           "l'algorithme 1 SP 800-38D § 6.3 MOT POUR MOT **SANS TABLE PAR "
           "DONNÉE** — PCLMULQDQ un chantier futur nommé ; **LE DOMAINE "
           "GROS-BOUTISTE PAR BSWAP** : les DEUX voies bswapées, "
           "l'extraction shld/sbb/shl [le drapeau capturé AVANT "
           "l'écrasement], le repli 0xE1<<56 au SOMMET de la voie haute ; "
           "SANS BRANCHE — le masque 0/−1 par sbb, le repli par ET "
           "logique, le SEUL saut est le compteur public), GCM sceller (H = "
           "E(K, 0) D'ABORD, le CTR [inc32 le u32 GROS-BOUTISTE par bswap], "
           "le GHASH par APPELS RÉPÉTÉS, les DEUX longueurs en BITS u64 "
           "gros-boutistes, l'étiquette E(K, J0) ⊕ GHASH, les refus −1/−2 "
           "NOMMÉS) et GCM ouvrir (**LA DISCIPLINE DU VERDICT** : le OU "
           "cumulatif des 16 différences en UN seul drapeau, AUCUN "
           "court-circuit, le branch sur LE drapeau ; PUIS le CTR — LA "
           "RESTITUTION EST LA DERNIÈRE OPÉRATION, l'étiquette divergente → "
           "rax = −4 NOMMÉ et la sortie clair INTACTE — fail-closed, RFC "
           "8446 § 5.2) ; LA NOTATION 520/129/162/1076/1163 o (round-trip "
           "100 %) aux slots ARRÊTÉS 0x240/0xC0/0xC0/0x480/0x4C0 tassés "
           "depuis 0xDCC0 (fin de famille 0xE9C0 — D161 rejoué) ; LE HARNAIS "
           "tls13/harnais_aead.py : **49 contrôles · 49 VERTS × 3 graines** "
           "— FIPS 197 C.1 (le déploiement ET le bloc) + SP 800-38A F.1.1 "
           "(les quatre blocs PAR LA COMPOSITION : un déploiement faux rend "
           "un chiffrement faux) + McGrew–Viega TC1..TC4 (TC5/TC6 aux IV "
           "hors 96 bits : HORS CONTRAT de la brique — P2 le nonce de 12 o, "
           "la borne du protocole) + **LE TRANSFERT RFC 8448 : les SEPT "
           "enregistrements chiffrés du § 3 OUVERTS par 19 puis RESCELLÉS "
           "par 18 == l'enregistrement OCTET POUR OCTET** (le nonce = "
           "IV ⊕ séquence, la tête 0x17 en AAD), l'oracle 100+100 ZÉRO "
           "écart, la borne P4 (N = 16384 exact), les DOUZE refus −1, "
           "l'indifférence (A = 0 : le pointeur nul n'est pas un refus), le "
           "contrat (20 entrées de callee alignées aux comptes EXACTS, les "
           "sorties jamais dépassées, le refus SANS corruption), la "
           "falsification (**LES 16 octets de l'étiquette ET les 53 du "
           "chiffré mutés UN PAR UN → −4, la sortie INTACTE 69/69**), le "
           "temps constant MESURÉ (114/26/2199/12531 instructions ; **LE "
           "VERDICT : trois étiquettes divergentes → 11 755 instructions LE "
           "MÊME COMPTE — la position de la divergence INVISIBLE dans le "
           "temps**) ; **DEUX DÉFAUTS DE NOTATION nommés par LA SONDE du "
           "geste** (la représentation GHASH : la première écriture tenait "
           "la chaîne en DEUX u64 little-endian — renversée 30/30, la "
           "commutativité elle-même fausse ; les candidats LE-classique et "
           "X-MSB rejetés par le code 1/43, LE CANDIDAT BSWAP/BE 63/63 — "
           "re-mesuré 139 → 162, le slot TIENT ; le J0 terminal de 18/19 : "
           "le u32 1 posé en boutisme MACHINE [01 00 00 00] — le premier "
           "compteur sortait 01 00 00 01, le chiffré ET l'étiquette faux ; "
           "l'immédiat corrigé 0x01000000, taille NEUTRE, REJOUÉ VERT) ; "
           "**la famille enregistrement (tls13-20/21) ATTEND SON GESTE — "
           "puis la poignée tls13-23..28 au transfert RFC 8448 en bout en "
           "bout, les slots à la suite de 0xE9C0** |")

ANCRE_ETAT = ("le cswap écrasait le bit "
              "du drapeau — k_t préservé en r11d].")
SUITE_ETAT = ("le cswap écrasait le bit "
              "du drapeau — k_t préservé en r11d].** "
              "**LA FAMILLE aead NOTÉE-MESURÉE-PROUVÉE le 07/11/2026 "
              "(Entrée 173)** (tls13-15..19 : AES-128 le déploiement des "
              "clés de tour à L'ARRÊT AES-NI [AESKEYGENASSIST matériel, "
              "pshufd 0xFF, les dix Rcon en immédiats, les dix tours "
              "déroulés], le chiffrement d'un bloc [pxor + NEUF AESENC + "
              "AESENCLAST — la brique d'inversion n'existe pas], GHASH [la "
              "marche § 6.3 mot pour mot sans table par donnée, LE DOMAINE "
              "GROS-BOUTISTE PAR BSWAP — la correction du geste, sans "
              "branche], GCM sceller [H d'abord, le CTR, le GHASH par "
              "appels répétés, les refus −1/−2] et GCM ouvrir [LA "
              "DISCIPLINE DU VERDICT : le OU cumulatif en un drapeau, la "
              "restitution DERNIÈRE — −4 NOMMÉ, la sortie INTACTE]) ; la "
              "notation 520/129/162/1076/1163 o aux slots arrêtés "
              "0x240/0xC0/0xC0/0x480/0x4C0 depuis 0xDCC0 (fin 0xE9C0) ; le "
              "harnais 49/49 VERTS × 3 graines — FIPS 197 C.1 + SP 800-38A "
              "F.1.1 par la composition + McGrew–Viega TC1..TC4 + **LE "
              "TRANSFERT RFC 8448 : les SEPT enregistrements du § 3 ouverts "
              "ET rescellés octet pour octet**, l'oracle 100+100, la borne "
              "P4, les douze refus, la falsification octet par octet (69/69 "
              "→ −4, la sortie intacte), **le verdict TEMPS CONSTANT mesuré "
              "(trois étiquettes divergentes → 11 755 instructions LE MÊME "
              "COMPTE)** ; deux défauts de notation nommés par la sonde du "
              "geste [la représentation GHASH — le domaine gros-boutiste "
              "par bswap ; le J0 terminal — l'immédiat gros-boutiste].")


def main() -> int:
    p = PLAN.read_text(encoding="utf-8")
    if "LA FAMILLE aead NOTÉE-MESURÉE-PROUVÉE le 07/11/2026" in p:
        print("[maj-plan] REJEU REFUSÉ : la famille aead est déjà au PLAN.")
        return 1
    if p.count(ANCRE_B) != 1:
        print(f"[maj-plan] ÉCHEC : l'ancre du chantier (b) trouvée "
              f"{p.count(ANCRE_B)} fois.")
        return 1
    if p.count(ANCRE_ETAT) != 1:
        print(f"[maj-plan] ÉCHEC : l'ancre de l'État du programme trouvée "
              f"{p.count(ANCRE_ETAT)} fois.")
        return 1
    p = p.replace(ANCRE_B, SUITE_B)
    p = p.replace(ANCRE_ETAT, SUITE_ETAT)
    PLAN.write_text(p, encoding="utf-8")
    print("[maj-plan] PASSÉ : le chantier M9-(b) porte la famille aead ; "
          "l'État du programme la consigne.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
