#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9e.py — LE PLAN au geste « LA FAMILLE enregistrement
NOTÉE-MESURÉE-PROUVÉE » : la rangée du chantier M9-(b) porte la famille
enregistrement, l'État du programme la consigne. Deux remplacements
ASSERTÉS — tout ancrage manquant = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

ANCRE_B = ("; **la famille enregistrement (tls13-20/21) ATTEND SON GESTE — "
           "puis la poignée tls13-23..28 au transfert RFC 8448 en bout en "
           "bout, les slots à la suite de 0xE9C0** |")
SUITE_B = ("; **LA FAMILLE enregistrement (tls13-20/21) NOTÉE-MESURÉE-PROUVÉE "
           "le 07/11/2026 (Entrée 174)** : l'enregistrement protéger "
           "(**LE CONTEXTE 200 o** à la disposition DÉCLARÉE : clés de tour "
           "@+0 [176], IV @+176 [12], réserve @+188 [4], séquence u64 @+192 "
           "[8] — posé par l'APPELANT, tls13-24 le posera au geste qui le "
           "dérivera ; **LE CADRE NOMMÉ 0x4078** : le texte interne jusqu'à "
           "2^14+1 SUR LA PILE ; l'en-tête LOCALE cinq octets fixes [23, "
           "0x0303, N+17 u16 gros-boutiste] copiée à la sortie APRÈS le "
           "succès — le fail-closed : le refus n'écrit RIEN ; le nonce = "
           "IV ⊕ séquence GROS-BOUTISTE, le contexte jamais réécrit sur son "
           "IV ; le type au DERNIER octet du texte interne — une VALEUR pas "
           "un pointeur ; l'incrémentation SUIT le scellement ; UNE "
           "composition TLS18 ; **LE VERDICT -3 PROPAGÉ** : N = 2^14 porte "
           "le texte interne à 2^14+1, HORS la brique — le maximal du "
           "protocole REFUSÉ par la composition, la fragmentation à "
           "l'APPELANT ; l'indifférence [N = 0 : le pointeur de charge nul "
           "n'est pas un refus]) et l'enregistrement déprotéger "
           "(**L'EN-TÊTE CONFRONTÉE AVANT TOUT** : le type reçu == 23 → −1, "
           "la longueur déclarée == reçue et les bornes 18..2^14+16 → −2 — "
           "19 ne peut plus refuser sur les longueurs ; **LA VERSION "
           "HÉRITAGE IGNORÉE par la logique mais COUVERTE par l'AAD** "
           "[RFC 8446 § 5.1 « MUST be ignored » : la mutation → −4, la "
           "cryptographie attrape ce que la logique ignore] ; l'AAD = "
           "l'en-tête reçue telle quelle ; le type = le DERNIER octet "
           "déverrouillé dans le tampon local ; LA RESTITUTION DERNIÈRE ; "
           "UNE composition TLS19) ; LA NOTATION 349/403 o (round-trip "
           "100 %) aux slots ARRÊTÉS 0x180/0x1C0 tassés depuis 0xE9C0 "
           "(fin de famille 0xED00 — D161 rejoué, le verdict 64 bits "
           "nommé par la sonde : 343→349, 395→403, les slots TIENNENT) ; "
           "LE HARNAIS tls13/harnais_enregistrement.py : **48 contrôles · "
           "48 VERTS × 3 graines** — **LE TRANSFERT RFC 8448 EN CHAÎNES** "
           "(LES QUATRE contextes de trafic consommés en séquence : chaque "
           "enregistrement du § 3 PROTÉGÉ par 20 == le transcript OCTET "
           "POUR OCTET, PUIS DÉPROTÉGÉ par 21 [les charges ET les types], "
           "ET LA REJOUE REFUSÉE ×4 — L'ANTI-REJOUE DU PROTOCOLE tient "
           "dans la cryptographie, pas dans un compteur de logique), "
           "l'oracle 60+60 ZÉRO écart, LA BORNE (N = 2^14−1 : le texte "
           "interne 2^14 == la borne de la brique ; N = 2^14 → le −3 "
           "propagé, la sortie VIERGE, la séquence figée), le type "
           "passe-plat, les refus, L'ORDRE (7 → 8 au succès, FIGÉE sur le "
           "−3 et le −4), le contrat (**LE CONTEXTE RÉÉCRIT SUR SA "
           "SÉQUENCE SEULE** — les 192 premiers octets OCTET-IDENTIQUES ; "
           "la zone morte profonde à −0x5000 sous le cadre nommé), la "
           "falsification (17/17 — l'en-tête mutée : le type → −1, la "
           "longueur → −2, LES OCTETS VERSION → −4), le temps constant "
           "MESURÉ (12 963/13 029/11 800 instructions — LE VERDICT : la "
           "position de la divergence INVISIBLE dans le temps) ; **UN "
           "DÉFAUT DE NOTATION nommé par LA SONDE du geste** (les verdicts "
           "en eax 32 bits — le haut de rax à zéro, l'appelant lit "
           "4294967295 : corrigé en mov rax, −N le 64 bits signé de la "
           "famille) ; **la famille poignée (tls13-23..28) ATTEND SON "
           "GESTE — LE TRANSFERT RFC 8448 en bout en bout, de "
           "l'enregistrement au Finished, les slots à la suite de 0xED00 "
           "(la marge : 0x300 o, la mesure décidera)** |")

ANCRE_ETAT = ("la représentation GHASH — le domaine gros-boutiste "
              "par bswap ; le J0 terminal — l'immédiat gros-boutiste].")
SUITE_ETAT = ("la représentation GHASH — le domaine gros-boutiste "
              "par bswap ; le J0 terminal — l'immédiat gros-boutiste].** "
              "**LA FAMILLE enregistrement NOTÉE-MESURÉE-PROUVÉE le "
              "07/11/2026 (Entrée 174)** (tls13-20/21 : l'enregistrement "
              "protéger [le contexte 200 o, le cadre nommé 0x4078 : le "
              "texte interne sur la pile, l'en-tête locale copiée APRÈS "
              "le succès, le nonce = IV ⊕ séquence, l'incrémentation "
              "après le scellement, LE VERDICT -3 PROPAGÉ à la borne du "
              "protocole] et l'enregistrement déprotéger [l'en-tête "
              "confrontée avant tout, LA VERSION héritage ignorée par la "
              "logique mais couverte par l'AAD, la restitution dernière, "
              "l'anti-rejoue par la séquence]) ; la notation 349/403 o "
              "aux slots arrêtés 0x180/0x1C0 depuis 0xE9C0 (fin 0xED00) ; "
              "le harnais 48/48 VERTS × 3 graines — **LE TRANSFERT RFC "
              "8448 EN CHAÎNES : les QUATRE contextes consommés en "
              "séquence, chaque enregistrement protégé PUIS déprotégé "
              "octet pour octet, LA REJOUE refusée ×4**, la borne (N = "
              "2^14 → le -3 propagé), l'ordre (un échec n'avance jamais "
              "la séquence), le contexte réécrit sur sa séquence seule, "
              "**le verdict temps constant mesuré (11 800 instructions "
              "LE MÊME COMPTE)** ; un défaut de notation nommé par la "
              "sonde [les verdicts 32 bits → le 64 bits signé].")


def main() -> int:
    p = PLAN.read_text(encoding="utf-8")
    if "LA FAMILLE enregistrement NOTÉE-MESURÉE-PROUVÉE le 07/11/2026" in p:
        print("[maj-plan] REJEU REFUSÉ : la famille enregistrement est déjà au PLAN.")
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
    print("[maj-plan] PASSÉ : le chantier M9-(b) porte la famille "
          "enregistrement ; l'État du programme la consigne.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
