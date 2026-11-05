#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9c.py — LE PLAN au geste « LA FAMILLE x25519 NOTÉE-MESURÉE-PROUVÉE » :
la rangée du chantier M9-(b) porte la famille x25519, l'État du programme la
consigne. Deux remplacements ASSERTÉS — tout ancrage manquant = ÉCHEC NOMMÉ,
rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

ANCRE_B = ("; **les familles x25519 (tls13-09..14) et aead (tls13-15..19) "
           "ATTENDENT LEUR GESTE** — la suite du chantier, les slots à la "
           "suite de 0xC980 |")
SUITE_B = ("; **LA FAMILLE x25519 (tls13-09..14) NOTÉE-MESURÉE-PROUVÉE le "
           "07/11/2026 (Entrée 172)** : f25519 addition (cinq membres IN PLACE, "
           "UNE passe), soustraction (les membres de 2p RE-DÉRIVÉS PAR "
           "ARITHMÉTIQUE [**ERRATUM tls13-10 I1 consigné AVANT la notation** : "
           "l'écriture « (2^51−38) puis (2^51−1)×4 » compose 2^255−38 ≡ −19 "
           "(mod p) — le membre 4 est 2^52−1 ; Σ prouvé par code == 2·p], "
           "DEUX passes a+2p au SCRATCH puis la chaîne sub/sbb, **LE VERROU "
           "fail-closed** [l'emprunt sortant → rax = −1 NOMMÉ, la sortie a "
           "JAMAIS écrite — l'échec E1 d'av-08 ÉLEVÉ en verdict de la table du "
           "domaine]), multiplication (l'école 5×5 DÉROULÉE aux DIX logements "
           "u128 sur la pile [sous-cadre 0xC0 = 160 o + 32 o d'ombre — le "
           "DIXIÈME reste NUL, il porte le REPLI UNIFORME C[4] = T[4] + 19·T[9]], "
           "le repli ×19 en DEUX morceaux, la chaîne 51 bits [shrd] et LE "
           "RETOUR FINAL r0 += 19·(r4>>51)), LE GARDIEN FUSIONNÉ propagation+gel "
           "SANS BRANCHE DE DONNÉES (**L'AMÉLIORATION NOMMÉE** sur le miroir "
           "av-10 qui branchait jb/ja : le drapeau « ≥ p » en registre SANS "
           "ÉCRIRE, le masque 0/−1 DIFFUSÉ PAR SAR, la soustraction "
           "conditionnelle PAR ET LOGIQUE — p → 0 EXACT, l'entrée "
           "OCTET-IDENTIQUE si < p), l'échelle de Montgomery RFC 7748 § 5 (le "
           "clamp dans la COPIE LOCALE, le bit 255 du point u MASQUÉ, le cswap "
           "XOR MASQUÉ membre à membre, **LA RECETTE 18 appels par itération** "
           "[4 add + 4 sub + 10 mul — **ERRATUM tls13-13 I5 consigné** : « entre "
           "4 et 6 » — la recette I2 fait foi, le compte par code], l'inversion "
           "z2^(p−2) par carré-et-multiplie sur l'exposant FIXE PUBLIC copié du "
           "FIXTURE [255 bornées], la mini-passe puis les QUATRE quads en miroir "
           "d'av-05) et le couple du ClientHello (le point 9 = LA DONNÉE "
           "PUBLIQUE du plan au FIXTURE — jamais un octet de code) ; LA NOTATION "
           "54/252/1078/281/2887/23 o (round-trip 100 %) aux slots ARRÊTÉS "
           "0x80/0x140/0x480/0x140/0xB80/0x40 tassés depuis 0xC980 (fin de "
           "famille 0xDCC0 — D161 rejoué, la préfiguration inclinée DEUX FOIS) ; "
           "**LES FIXTURES .text6 ARRÊTÉS** (R_U9 = 0xFF00 le point 9 LE, "
           "R_EXP_INV = 0xFF20 l'exposant p−2 LE — la réserve .rdata M8 "
           "ÉPUISÉE par K[64], l'ARRÊT D95 consigné, les contenus re-dérivés par "
           "arithmétique) ; LE HARNAIS tls13/harnais_x25519.py : **46 contrôles "
           "· 46 VERTS × 3 graines** — RFC 7748 § 5.2 (les DEUX paires octet "
           "pour octet, la référence croisée avant de juger) + § 6.1 (les clés "
           "publiques d'Alice ET de Bob par le couple, **LE SECRET PARTAGÉ des "
           "DEUX côtés** — la commutativité sur pièces) + **LE TEST ITÉRÉ** "
           "(1 pas 422c8e7a…, 1000 pas 684cf59b…) + **LE TRANSFERT RFC 8448** "
           "(le key_share du ClientHello 99381de5… et le shared 8bd4054f… du "
           "transcript, octet pour octet), l'oracle différentiel (60 échelles + "
           "1600 opérations de champ), les punitifs (les lâches de l'école, la "
           "soustraction lâche, le point non canonique, les dégénérés → 0), le "
           "contrat (**20 398 entrées de callee alignées ≡ 8 mod 16** — les "
           "comptes EXACTS de la recette ; LE VERROU −1 exercé hors contrat, la "
           "sortie INTACTE), la falsification (les fixtures corrompus → "
           "divergence : les données du plan sont LUES), le temps constant "
           "MESURÉ (**1 238 953 instructions EXACTEMENT** — le scalaire et le "
           "point JAMAIS comptés) ; **DEUX DÉFAUTS DE NOTATION nommés par le "
           "fail-closed** (l'école : mul DÉTRUIT rax — le second mul de chaque "
           "rangée multipliait le demi-produit, la bisection a0×b1 → 0 l'a "
           "nommé : a_i RECHARGÉ avant CHAQUE mul, re-mesuré 1002 → 1078, slot "
           "0x400 → 0x480 ; l'échelle : le geste x2' lisait A mort au lieu de la "
           "copie d'AA [TROIS consommateurs destructifs : l'original S3 pour E, "
           "la copie x2 pour le produit, la copie S4 pour le sommet] ET le "
           "cswap écrasait le bit du drapeau [rax est le scratch : k_t préservé "
           "en r11d] — nommés par LA TRACE ITÉRATIVE [l'état comparé à chaque "
           "pas contre Python, la première faute à t = 252], re-mesuré 2887, "
           "slot 0xB80, REJOUÉ VERT) ; **la famille aead (tls13-15..19) ATTEND "
           "SON GESTE — les slots à la suite de 0xDCC0** |")

ANCRE_ETAT = ("un défaut de notation nommé par le fail-closed — l'intérieur "
              "écrasé par l'opad, corrigé par le slot dédié).")
SUITE_ETAT = ("un défaut de notation nommé par le fail-closed — l'intérieur "
              "écrasé par l'opad, corrigé par le slot dédié).** "
              "**LA FAMILLE x25519 NOTÉE-MESURÉE-PROUVÉE le 07/11/2026 "
              "(Entrée 172)** (tls13-09..14 : l'arithmétique du corps "
              "F(2^255−19) radix 2^51 — addition, soustraction AU VERROU "
              "fail-closed [rax = −1 NOMMÉ, RIEN écrit], multiplication école "
              "5×5 aux DIX logements u128, LE GARDIEN FUSIONNÉ propagation+gel "
              "SANS BRANCHE [le drapeau en registre, sar, l'ET logique], "
              "l'échelle de Montgomery RFC 7748 [le cswap XOR masqué, "
              "l'inversion z2^(p−2) à l'exposant public du fixture, "
              "**1 238 953 instructions EXACTEMENT**] et le couple du "
              "ClientHello au fixture U9) ; la notation 54/252/1078/281/2887/23 "
              "o aux slots arrêtés 0x80/0x140/0x480/0x140/0xB80/0x40 depuis "
              "0xC980 (fin 0xDCC0), **LES FIXTURES .text6 ARRÊTÉS** (R_U9 "
              "@0xFF00, R_EXP_INV @0xFF20 — l'ARRÊT D95, la réserve .rdata M8 "
              "épuisée par K[64]) ; le harnais 46/46 VERTS × 3 graines — RFC "
              "7748 § 5.2 (les deux paires + LE TEST ITÉRÉ 1/1000) et § 6.1 "
              "(les clés publiques, LE SECRET PARTAGÉ des deux côtés), LE "
              "TRANSFERT RFC 8448 (le key_share du ClientHello + le shared du "
              "transcript) rendus octet pour octet, l'oracle 60 échelles + 1600 "
              "opérations, les punitifs (p → 0 exact, les lâches, les "
              "non-canoniques, les dégénérés), le contrat (20 398 entrées de "
              "callee alignées, le verrou −1 exercé), la falsification (les "
              "fixtures corrompus → divergence) ; **deux errata d'arithmétique "
              "des specs consignés AVANT la notation** [tls13-10 I1 : les "
              "membres de 2p — « (2^51−38) puis (2^51−1)×4 » compose 2^255−38 ≡ "
              "−19, le membre 4 est 2^52−1 ; tls13-13 I5 : « entre 4 et 6 "
              "opérations » — la recette § 5 exige 4+4+10 = 18], deux défauts "
              "de notation nommés par le fail-closed [mul détruit rax — le "
              "rechargement de a_i avant chaque mul ; le cswap écrasait le bit "
              "du drapeau — k_t préservé en r11d].")


def main() -> int:
    p = PLAN.read_text(encoding="utf-8")
    if "LA FAMILLE x25519 NOTÉE-MESURÉE-PROUVÉE le 07/11/2026" in p:
        print("[maj-plan] REJEU REFUSÉ : la famille x25519 est déjà au PLAN.")
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
    print("[maj-plan] PASSÉ : le chantier M9-(b) porte la famille x25519 ; "
          "l'État du programme la consigne.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
