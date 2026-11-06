#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_passation_m9j.py — dépose le paragraphe PASSATION au worklog
Task ID 96 (après la puce SUITE, avant le Stage Summary) : le bundle courant
090-3fa7168 déposé au miroir, l'ancien archivé, GitHub à la pointe — la
passation du geste LE BUILD 1.0.0-dev.1 NÉ. Rejeu REFUSÉ."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
WORKLOG = REPO / "worklog.md"

PASSATION = """- PASSATION (le même geste, Task ID 96) : le bundle courant
  triade-history-090-3fa7168.bundle (17 991 135 o, md5 60401423…, branche
  jalon == 3fa7168 [le geste + sa consignation]) DÉPOSÉ AU MIROIR ASSERTÉ
  (relu MATCH : il porte LE BUILD NÉ [Entrée 178 — la cérémonie soldée : la
  remise du développeur rapatriée md5 contrôlés, la clé du 04/11 constatée
  173fae9c…, le dépôt atomique, le garde VERT 13/13 ; l'erratum n° 4 : le
  chevauchement tls13-27/28 nommé par la sonde AVANT l'artefact, réparé à
  la source — TLS28_VA 0x10AC0, notations 27/28 re-générées, harnais
  poignée 52/52 × 3 graines, le contrôle slots-disjoints PERMANENT — ;
  construire() : tls13/proxy.exe 1.0.0-dev.1 (65 024 o, sha256 9ed63f39…)
  sur le corps 0.9.0 INTACT confronté OCTET PAR OCTET, .text6 NOUVELLE (28
  blocs + 17 fixtures, la composition intégrale), AUCUN import nouveau ;
  la carte GÉNÉRATION 9 (86 blocs, 8 artefacts, contrats parsés des specs
  I), le verrou croisé 86/86, l'artefact DÉTERMINISTE] + le worklog Task
  96 + la signature tls13 déposée [128 hex — la cérémonie soldée]),
  l'ancien 090-ae47935 (LA CÉRÉMONIE ARMÉE) ARCHIVÉ VERSIONNÉ (md5
  ca52d0c3… recoupé — 40 archives, rien supprimé), /test sans copie
  (recoupé), le push GitHub à la pointe (origin == 3fa7168 relu MATCH —
  les trois miroirs alignés) ; script suivi : passe_bundle_m9j.py ; LA
  SÉRIE 090 POURSUIT — le geste est PASSÉ."""


def main():
    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    texte = WORKLOG.read_text(encoding="utf-8")
    if "PASSATION (le même geste, Task ID 96)" in texte:
        sys.exit("ÉCHEC : la passation Task ID 96 est déjà consignée (rejeu REFUSÉ)")
    ancrage = ("si vert : la finale 1.0.0 (le\n  fait de carte) et le jalon M9 "
               "franchi.\n")
    if texte.count(ancrage) != 1:
        sys.exit(f"ÉCHEC : ancrage SUITE introuvable ou ambigu "
                 f"({texte.count(ancrage)} fois)")
    texte = texte.replace(ancrage, ancrage + PASSATION + "\n", 1)
    # la relecture fait foi : la passation est DANS la section Task 96
    if "PASSATION (le même geste, Task ID 96)" not in texte:
        sys.exit("ÉCHEC : la passation n'a pas suivi (constat AVANT écriture)")
    WORKLOG.write_text(texte, encoding="utf-8")
    print("[passation] le paragraphe PASSATION déposé au worklog Task ID 96 "
          "(après la puce SUITE, avant le Stage Summary)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
