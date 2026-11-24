#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMÉLIORATION 4 (D259) — LE TÉMOIN HORS MACHINE COMME PORTE DE RELEASE.

Aucune ancre locale ne voit la restauration cohérente d'un couple binaire +
état (D254). Le seul remède est un témoin que la machine ne peut pas réécrire :
la carte papier du sachet, le journal Git poussé, l'ancre de transparence.
Ce script vérifie qu'un témoin ATTESTE l'état publié avant toute release :

  temoin = {"date": "2026-11-24", "edition": "v0.24.1",
            "epoch": 41, "sha8": "acf54449"}
  etat   = {"edition": "v0.24.1", "epoch": 41, "sha8": "acf54449"}

Refus nommés : TEMOIN-ABSENT, TEMOIN-ANTERIEUR (époque du témoin < état),
EMPREINTE-DIVERGENTE (sha8), DATE-FUTURE, EDITION-DIVERGENTE.
Sortie : 0 = attesté ; 3 = refus nommé ; 2 = fichier illisible.
"""
import datetime as dt
import json
import sys


class Refus(Exception):
    pass


def verifier(temoin, etat, aujourdhui=None):
    if not temoin:
        raise Refus("TEMOIN-ABSENT")
    for k in ("date", "edition", "epoch", "sha8"):
        if k not in temoin:
            raise Refus("TEMOIN-INCOMPLET")
    if temoin["edition"] != etat["edition"]:
        raise Refus("EDITION-DIVERGENTE")
    if temoin["sha8"] != etat["sha8"]:
        raise Refus("EMPREINTE-DIVERGENTE")
    if int(temoin["epoch"]) < int(etat["epoch"]):
        raise Refus("TEMOIN-ANTERIEUR")
    jour = (aujourdhui or dt.date.today())
    if dt.date.fromisoformat(temoin["date"]) > jour:
        raise Refus("DATE-FUTURE")
    return "ATTESTE"


def autotest():
    etat = {"edition": "v0.24.1", "epoch": 41, "sha8": "acf54449"}
    bon = {"date": "2026-11-24", "edition": "v0.24.1", "epoch": 41, "sha8": "acf54449"}
    cas = [
        ("témoin à l'état", bon, etat, "ATTESTE"),
        ("témoin absent", None, etat, "TEMOIN-ABSENT"),
        ("témoin antérieur", {**bon, "epoch": 40}, etat, "TEMOIN-ANTERIEUR"),
        ("empreinte divergente", {**bon, "sha8": "00000000"}, etat, "EMPREINTE-DIVERGENTE"),
        ("édition divergente", {**bon, "edition": "v0.24.0"}, etat, "EDITION-DIVERGENTE"),
        ("date future", {**bon, "date": "2027-01-01"}, etat, "DATE-FUTURE"),
    ]
    print("=" * 78)
    print("AMÉLIORATION 4 — LE TÉMOIN HORS MACHINE (D259)")
    print("=" * 78)
    verts = 0
    for nom, t, e, attendu in cas:
        try:
            rendu = verifier(t, e, dt.date(2026, 11, 24))
        except Refus as ex:
            rendu = ex.args[0]
        ok = rendu == attendu
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} → {rendu}")
    print(f"{verts}/{len(cas)}")
    return 0 if verts == len(cas) else 3


def main(argv):
    if len(argv) == 3:
        temoin = json.load(open(argv[1], encoding="utf-8"))
        etat = json.load(open(argv[2], encoding="utf-8"))
        try:
            print("[temoin]", verifier(temoin, etat))
            return 0
        except Refus as e:
            print("[temoin] REFUS", e.args[0])
            return 3
    return autotest()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
