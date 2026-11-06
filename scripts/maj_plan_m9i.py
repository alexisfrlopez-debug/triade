#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9i.py — LA CONSIGNED mis à jour du PLAN : la rangée (e) du
chantier M9 (la cérémonie + le build + la carte) passe de « la cérémonie
attend sa remise » à « LE BUILD 1.0.0-dev.1 NÉ » ; l'État du programme
reçoit la phrase du chantier (e). Rejeu REFUSÉ ; tout ancrage absent ou
compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# --- la rangée (e) : la fin de la colonne des preuves ------------------------

ANCIEN_RANGEE = ("; LA CÉRÉMONIE DU DÉVELOPPEUR attend sa remise (signer "
                 "a-signer.txt hors ligne avec la clé du 04/11, ramener "
                 "signatures-I.txt + cle-publique-I.txt au /test du Drive) "
                 "— le build suit le garde VERT 13/13 |")

NOUVELLE_RANGEE = ("; **LE BUILD 1.0.0-dev.1 NÉ le 06/11/2026 (Entrée 178, "
                   "Task 96)** : LA CÉRÉMONIE PASSÉE — la remise du "
                   "développeur déposée au /test, rapatriée md5 contrôlés "
                   "par pièce (la clé du 04/11 constatée 173fae9c…, "
                   "réutilisée), installée par sceau_I.py deposer "
                   "(L'ATOMICITÉ DE CÉRÉMONIE : tout vérifié AVANT toute "
                   "écriture), le garde REPASSÉ VERT 13/13 (l'état "
                   "« reelle ») ; L'ERRATUM n° 4 nommé au chantier du build "
                   "(tls13-27 ré-arrêté 0xB80 [2906 o, les douze fautes du "
                   "geste poignée] SANS déplacer tls13-28 : le chevauchement "
                   "de code [0x10A80, 0x10A9A) recouvrait le socle — "
                   ".refus_pre_taille @0x10A80 et .refus_contexte_nul "
                   "@0x10A92 vivaient DANS tls13-28, le harnais n'a pas vu : "
                   "la pose n'écrit que le code, les chemins -1/-2 jamais "
                   "exercés — RÉPARÉ à la source : TLS28_VA 0x10AC0, les "
                   "notations 27/28 re-générées par l'auteur, le harnais "
                   "poignée re-joué 52/52 × 3 graines, LE CONTRÔLE "
                   "slots-disjoints PERMANENT ; note D8 : padding ≥ 16 + "
                   "aligné 16 [LA DÉCISION], le multiple-de-64 est la "
                   "convention M8, déclinée par l'arrêt consigné 0x120/0xB0) ; "
                   "construire() EXÉCUTÉ : tls13/proxy.exe 1.0.0-dev.1 "
                   "(65 024 o, sha256 9ed63f39…) — le corps 0.9.0 INTACT "
                   "(R7 : la recomposition M3+M4+M5+M8 confrontée OCTET PAR "
                   "OCTET au scellé 1492b0bc… AVANT l'extension), .text5 le "
                   "socle socket sys-04..06 dans la réserve int3 VÉRIFIÉE "
                   "du scellé, .text6 NOUVELLE (0xC000-0x10FFF : les 28 "
                   "blocs + les 17 fixtures DÉRIVÉS du plan — U9/EXP_INV, "
                   "les libellés + HRR, le transport AFD —, la composition "
                   "INTÉGRALE : chaque octet compté : slot, fixture ou "
                   "int3), la version 0x01000001 @0x2820 (geste de BUILD, "
                   "jamais scellage), 8 sections (les en-têtes 648 o ≤ "
                   "0x400), SizeOfImage 0x11000, l'entrée 0x8C80 inchangée, "
                   "AUCUN import nouveau (le socket natif SANS une seule "
                   "entrée d'import réseau : ws2_32 jamais importé PAR LES "
                   "BLOCS NOUVEAUX) ; les oracles : M4 560 + M5 365 + sys "
                   "131 (le socle compris) cas verts, structurels M3 524 + "
                   "M4 492 + M5 312 + M8 54 + socle 71 + tls13 589 verrous "
                   "(AUCUN IAT par bloc tls13, AUCUN site syscall hors "
                   "sys-01, les appels fermés, les RIP == fixtures, LES "
                   "SLOTS DISJOINTS) ; la carte GÉNÉRATION 9 (86 blocs, 8 "
                   "artefacts, les contrats des 31 nouveaux PARSÉS des "
                   "specs I — R2 ; la relève des secrets au coffre : lignée "
                   "D80 + graine durable D144, le témoin e9cd8c549485… "
                   "tenu), le verrou croisé 86/86 (R8/R9), l'artefact "
                   "DÉTERMINISTE (re-construit byte-identique) ; reste (f) "
                   "le terrain — LA GRANDE ŒUVRE → la finale 1.0.0 |")

# --- l'État du programme : la phrase du chantier (e) après celle du (d) ------

ANCIEN_ETAT = ("le VRAI afd.sys de la machine du développeur attend le "
               "chantier (f)** Les chantiers M6-(a)")

NOUVEL_ETAT = ("le VRAI afd.sys de la machine du développeur attend le "
               "chantier (f)** **LE CHANTIER M9-(e) RÉALISÉ le 06/11/2026 "
               "(Entrée 178, Task 96) : LA CÉRÉMONIE DU BUILD 1.0.0 "
               "SOLDÉE, L'ERRATUM n° 4 NOMMÉ, LE BUILD 1.0.0-dev.1 NÉ** "
               "(la remise du développeur déposée au /test, rapatriée md5 "
               "contrôlés — la clé du 04/11 constatée 173fae9c… —, "
               "installée par l'atomicité de cérémonie, le garde repassé "
               "VERT 13/13 ; l'erratum n° 4 : le chevauchement tls13-27/28 "
               "[tls13-27 ré-arrêté 0xB80 sans déplacer tls13-28 : les "
               "refus -1/-2 de la machine d'états vivaient DANS tls13-28] "
               "nommé par la sonde AVANT l'artefact, réparé à la source "
               "[TLS28_VA 0x10AC0, notations 27/28 re-générées, harnais "
               "poignée 52/52 × 3 graines], le contrôle slots-disjoints "
               "PERMANENT ; construire() : tls13/proxy.exe 1.0.0-dev.1, "
               "65 024 o, sha256 9ed63f39… — le corps 0.9.0 INTACT [R7 : "
               "la recomposition confrontée au scellé 1492b0bc… AVANT "
               "l'extension], .text5 le socle dans la réserve int3 "
               "vérifiée, .text6 NOUVELLE [28 blocs + fixtures, la "
               "composition intégrale : chaque octet compté], la version "
               "0x01000001 [geste de BUILD], AUCUN import nouveau ; les "
               "oracles M4 560 + M5 365 + sys 131 cas verts, structurels "
               "524+492+312+54+71+589 verrous ; la carte GÉNÉRATION 9 [86 "
               "blocs, 8 artefacts, contrats parsés des specs I], le "
               "verrou croisé 86/86, l'artefact DÉTERMINISTE — la relève "
               "des secrets au coffre [lignée D80 + graine durable, le "
               "témoin e9cd8c549485… tenu]) ; reste (f) le terrain — LA "
               "GRANDE ŒUVRE → la finale 1.0.0** Les chantiers M6-(a)")


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    if "NÉ le 06/11/2026 (Entrée 178" in plan or "CHANTIER M9-(e) RÉALISÉ" in plan:
        sys.exit("ÉCHEC : la rangée (e)/l'État sont déjà à jour (rejeu REFUSÉ)")
    if plan.count(ANCIEN_RANGEE) != 1:
        sys.exit(f"ÉCHEC : ancrage rangée (e) trouvé {plan.count(ANCIEN_RANGEE)} "
                 f"fois (attendu : 1)")
    if plan.count(ANCIEN_ETAT) != 1:
        sys.exit(f"ÉCHEC : ancrage État du programme trouvé "
                 f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")

    plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
    plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)

    # la relecture fait foi : les DEUX remplacements constatés AVANT écriture
    if "LE BUILD 1.0.0-dev.1 NÉ le 06/11/2026 (Entrée 178, Task 96)" not in plan:
        sys.exit("ÉCHEC : la rangée (e) n'a pas suivi (constat AVANT écriture)")
    if "LE CHANTIER M9-(e) RÉALISÉ le 06/11/2026 (Entrée 178, Task 96)" not in plan:
        sys.exit("ÉCHEC : l'État du programme n'a pas suivi (constat AVANT écriture)")
    if "LA CÉRÉMONIE DU DÉVELOPPEUR attend sa remise" in plan:
        sys.exit("ÉCHEC : l'ancien état de la rangée (e) demeure")

    PLAN.write_text(plan, encoding="utf-8")
    print("[plan] la rangée (e) : LE BUILD 1.0.0-dev.1 NÉ — la cérémonie "
          "passée, l'erratum n° 4 nommé, la carte génération 9, le verrou "
          "croisé 86/86")
    print("[plan] l'État du programme : la phrase du chantier (e) déposée "
          "après celle du (d)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
