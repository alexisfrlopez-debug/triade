#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9q.py — LA CONSIGNATION DU PLAN au geste « LE QUATRIÈME RUN
TERRAIN (f) REÇU : LE GESTE (ii) DU RECOUP-3 ACCOMPLI (Windows 11 build
26300) ET LE -6 SE RÉPÈTE À L'IDENTIQUE — LE SUSPECT (a) (la divergence
afd.sys Win10 ↔ Win11) ÉLIMINÉ SUR PIÈCES ; le recoup 30/30, le run
archivé ; LA SONDE SYS-05 (m9-(g)) — le chantier promis — OUVERTE ET
LIVRÉE AU COFFRE (le trampoline de capture, l'artefact INTACT) » : la
rangée (f) reçoit le constat du quatrième run, l'État du programme
reçoit la phrase du geste (le geste du développeur sur la sonde attendu).
Rejeu REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois =
ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# --- la rangée (f) : le constat du QUATRIÈME run, AVANT la colonne du
# critère -------------------------------------------------------------------------

ANCIEN_RANGEE = ("[une machine Windows 11, ou la sonde sys-05 au labo — le "
                 "chantier futur nommé])** | run terrain VERT sur pièces")

NOUVELLE_RANGEE = (
    "[une machine Windows 11, ou la sonde sys-05 au labo — le chantier "
    "futur nommé]** ; **LE QUATRIÈME RUN REÇU le 07/11 (Entrée 184, Task "
    "102) : LE GESTE (ii) ACCOMPLI — LA MACHINE WINDOWS 11 (build 26300, "
    "Python 3.14.3, ntdll b072efae…) ENFIN ESSAYÉE, l'artefact INTACT "
    "[d8928934…], le kit ACQUITTÉ INCHANGÉ [90a1d022…] — ET LE -6 SE "
    "RÉPÈTE À L'IDENTIQUE : le journal du run 4 == celui du run 3, LIGNE "
    "À LIGNE, les horodatements exceptés [CONSTATÉ PAR CODE sur pièces "
    "croisées] → LE SUSPECT (a) ÉLIMINÉ SUR PIÈCES : le refus est "
    "INTER-GÉNÉRATIONS, STRUCTUREL au contrat d'appel de sys-05 ou à "
    "l'état de l'endpoint ; le recoup 30/30, le run archivé → "
    "preuves-run-m9f-4/ AVEC le verdict ; LA SONDE SYS-05 (m9-(g)) — LE "
    "CHANTIER PROMIS — OUVERTE ET LIVRÉE AU COFFRE : kit-sonde-sys05.zip "
    "[md5 215c2caa…] + LISEZMOI + preuves-sonde-sys05/, LE TRAMPOLINE DE "
    "CAPTURE [33 o, l'ABI msx64, l'artefact INTACT — JAMAIS reconstruit] "
    "LIT LE NTSTATUS BRUT qui vit dans rdx [la limite NOMMÉE de "
    "l'instrument, sys-05 Q5], le compas étalonné AVANT la mesure, la "
    "table NTSTATUS canonique, les variations, ET LA CONTRE-ÉPREUVE S4 "
    "[la poignée par LE RAPPEL STANDARD — si le refus disparaît : LA "
    "PERCÉE, la ligne suit DANS LE MÊME RUN]** | run terrain VERT sur "
    "pièces")

# --- l'État du programme : la phrase du geste APRÈS celle du troisième run -------

ANCIEN_ETAT = ("le suspect principal (une machine Windows 11, ou la sonde "
               "sys-05 au labo) — et si le vert tient : LA FINALE 1.0.0, "
               "LE JALON M9 — LA GRANDE ŒUVRE** Les chantiers M6-(a)")

NOUVEL_ETAT = (
    "le suspect principal (une machine Windows 11, ou la sonde sys-05 au "
    "labo) — et si le vert tient : LA FINALE 1.0.0, LE JALON M9 — LA "
    "GRANDE ŒUVRE** **LE QUATRIÈME RUN (f) REÇU ET RECROPÉ le 07/11 "
    "(Entrée 184, Task 102) : LE GESTE (ii) ACCOMPLI, LE SUSPECT (a) "
    "ÉLIMINÉ SUR PIÈCES** (la machine Windows 11 build 26300 enfin "
    "essayée — l'artefact INTACT, le kit ACQUITTÉ INCHANGÉ : seule la "
    "machine a changé — et le -6 se répète À L'IDENTIQUE à l'émission du "
    "CH : le journal du run 4 == celui du run 3, LIGNE À LIGNE, les "
    "horodatements exceptés, CONSTATÉ PAR CODE sur pièces croisées ; T0/"
    "T1/T2 VERT sur Win11 aussi [SSN 85/7/15, handle 0x280 — le socle "
    "traverse VIVANT les deux générations], le recoup du jalon VERT [le "
    "CH == la construction re-jouée, 119 o] et l'erratum n° 7 réparé [la "
    "clé f650affb… NON-NULLE] ; le refus est INTER-GÉNÉRATIONS : la "
    "divergence afd.sys Win10 ↔ Win11 ne PEUT PLUS l'expliquer — il ne "
    "reste qu'UNE information manquante, LE NTSTATUS BRUT qui vit dans "
    "rdx ; le recoup 30/30, le run archivé → preuves-run-m9f-4/) ; **LA "
    "SONDE SYS-05 (m9-(g)) EST LE GESTE RENDU — LE CHANTIER PROMIS, "
    "OUVERT ET LIVRÉ AU COFFRE DANS LE MÊME GESTE** (kit-sonde-sys05.zip "
    "md5 215c2caa… + LISEZMOI-sonde-sys05.txt + preuves-sonde-sys05/ au "
    "/test, la vague m9f DEMEURE INTACTE [kit-m9f.zip 90a1d022…] ; LE "
    "TRAMPOLINE DE CAPTURE — 33 octets posés au run, l'ABI msx64 "
    "démontrée, l'artefact INTACT relu — LIT LE NTSTATUS BRUT DU GESTE "
    "M9F, le compas étalonné AVANT la mesure [handle invalide → -6 + "
    "STATUS_INVALID_HANDLE attendu : fail-closed], la table NTSTATUS "
    "recoupée aux sources canoniques [Wine ET ReactOS au bit près — la "
    "classe de sévérité tranche : un PENDING traité en -6 serait LE BUG "
    "DU CONTRAT], les variations [taille, délai] et LA CONTRE-ÉPREUVE S4 "
    "[la poignée par LE RAPPEL STANDARD sur session NEUVE : si le refus "
    "disparaît, LA PERCÉE — la ligne suit DANS LE MÊME RUN]) ; LE GESTE "
    "DU DÉVELOPPEUR SUR LA SONDE EST ATTENDU — puis le recoup, le "
    "coupable NOMMÉ [le contrat du bloc, l'état de l'endpoint, ou le "
    "réseau], la réparation selon la charte [l'erratum de la notation + "
    "la révision 2 de la spec sys-05 le cas échéant — jamais une dérive "
    "silencieuse] — et si la percée tient : le run m9f réparé, LA "
    "FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE** Les chantiers M6-(a)")


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    if "LE QUATRIÈME RUN REÇU le 07/11" in plan \
            or "LE QUATRIÈME RUN (f) REÇU ET RECROPÉ" in plan:
        sys.exit("ÉCHEC : la rangée (f)/l'État sont déjà à jour "
                 "(rejeu REFUSÉ)")
    if plan.count(ANCIEN_RANGEE) != 1:
        sys.exit(f"ÉCHEC : ancrage rangée (f) trouvé "
                 f"{plan.count(ANCIEN_RANGEE)} fois (attendu : 1)")
    if plan.count(ANCIEN_ETAT) != 1:
        sys.exit(f"ÉCHEC : ancrage État du programme trouvé "
                 f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")

    plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
    plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)

    if "LE QUATRIÈME RUN REÇU le 07/11 (Entrée 184" not in plan:
        sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du "
                 "quatrième run après remplacement")
    if "LE QUATRIÈME RUN (f) REÇU ET RECROPÉ le 07/11" not in plan:
        sys.exit("ÉCHEC : l'État du programme ne porte pas la phrase du "
                 "quatrième run après remplacement")
    PLAN.write_text(plan, encoding="utf-8")

    relu = PLAN.read_text(encoding="utf-8")
    if relu.count("LE QUATRIÈME RUN REÇU le 07/11") != 1 \
            or relu.count("LE QUATRIÈME RUN (f) REÇU ET RECROPÉ") != 1:
        sys.exit("ÉCHEC : relecture — les phrases du geste ne sont pas "
                 "chacune UNIQUES")
    print("[plan] rangée (f) : le constat du quatrième run déposé (le "
          "geste (ii) accompli, la répétition par code, le suspect (a) "
          "éliminé, la sonde livrée)")
    print("[plan] État du programme : la phrase du geste déposée (la "
          "sonde sys-05 — le chantier promis, ouvert et livré)")
    print("[plan] la relecture fait foi : les DEUX ancrages remplacés, "
          "chacune UNIQUE — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
