#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ajoute_passation_m9u.py — ajoute la section LA PASSATION à l'entrée
Task ID 106 du worklog (le geste est passé : bundle 090-3dc3d3e au
miroir, l'ancien archivé, GitHub à la pointe). Rejeu REFUSÉ."""
import pathlib
import sys

WORKLOG = pathlib.Path("/home/z/my-project/triade/worklog.md")

SECTION = """
- LA PASSATION (passe_bundle_m9u.py) : le bundle courant
  triade-history-090-3dc3d3e (18 784 543 o, md5 4f445352…) DÉPOSÉ AU
  MIROIR ASSERTÉ (relu MATCH : il porte LA SECONDE SIGNATURE DE LA
  RÉVISION 2 ÉTENDUE REÇUE ET INSTALLÉE [Entrée 188 — la remise recoupée
  13/13 : l'ancre de clé 173fae9c… tenue, les DOUZE arbres inchangés ==
  les signatures déposées == build 1.0.0 (LA PREUVE DE D163 REJOINTE UNE
  QUATRIÈME FOIS), m8 re-signé contre c444d730… ; deposer joué, LE GARDE
  13/13 VERTS] + LE REBUILD 1.0.0-dev.3 NÉ SUR L'INSTRUMENT RÉVISÉ [les
  portes re-passées sys-05:R2 + sys-06:R2, la version R10 0x01000003,
  l'héritage 0.9.0 recomposé OCTET PAR OCTET (R7), le harnais révisé
  131 VERTS, la carte génération 11, le verrou croisé 86/86 — l'artefact
  de23e577…, LE DIFF CONTRÔLÉ : TROIS octets sur 65 024 (la version R10
  + LES DEUX POSES DU WSABUF 0x64 → 0x68)] + LE KIT M9F RÉPARÉ
  [scenario-m9f.py re-épinglé + LE T0.erratum-9 (la pose relue dans
  l'image aux DEUX blocs), LISEZMOI réécrit, l'assembleur 28 constantes
  PAR AST + LE CONTRÔLE PERMANENT — kit-m9f.zip md5 79d44284…] livré au
  /test [mis à jour en place, le réceptacle ré-armé, l'index, les pièces
  de cérémonie demeurées] + le worklog Task 106), l'ancien 090-ffcdf19
  (LA PREMIÈRE SIGNATURE + L'ERRATUM n° 9) ARCHIVÉ VERSIONNÉ (md5
  5beab6b7… recoupé — 51 archives, rien supprimé), /test sans copie de
  bundle ET le kit réparé recoupé (79d44284…) + le kit sonde (215c2caa…)
  + les PIÈCES DE CÉRÉMONIE demeurées (signatures-I.txt 503f3822… la
  seconde remise + cle-publique-I.txt 188a7d42… l'ancre) ; LE PUSH
  GITHUB RÉUSSI : origin == 3dc3d3e relu MATCH — LES TROIS MIROIRS
  ALIGNÉS (le commit de passation 551eac9 du geste précédent EMBARQUÉ,
  le flux tenu) ; script suivi : passe_bundle_m9u.py ; LA SÉRIE 090
  POURSUIT — le geste est PASSÉ (Drive + local + GitHub), LE CINQUIÈME
  RUN DU DÉVELOPPEUR EST ATTENDU (le premier du build réparé :
  dézipper kit-m9f.zip dans un dossier NEUF D99, python
  scenario-m9f.py, renvoyer preuves-m9f/ ENTIER au coffre) — ET SI LE
  VERT TIENT : LA FINALE 1.0.0, le jalon M9 — LA GRANDE ŒUVRE.
"""


def main():
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 106 —" not in w:
        sys.exit("ÉCHEC : l'entrée Task ID 106 absente (consigner_entree188 "
                 "d'abord)")
    if "LA PASSATION (passe_bundle_m9u.py)" in w:
        sys.exit("ÉCHEC : la section passation existe déjà (rejeu REFUSÉ)")
    if not w.rstrip().endswith("LE VERT\n  TIENT : LA FINALE 1.0.0, le jalon M9 — LA GRANDE ŒUVRE."):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 106 "
                 "attendue (ancre de suite absente)")
    WORKLOG.write_text(w.rstrip("\n") + "\n" + SECTION, encoding="utf-8")
    print("WORKLOG : la section LA PASSATION ajoutée à la Task ID 106")


if __name__ == "__main__":
    main()
