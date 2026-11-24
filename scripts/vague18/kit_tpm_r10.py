#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HETETZNTH — LE COMPTEUR NV TPM 2.0 COMME PLANCHER R10 (D263).

Le plancher de version n'est plus un fichier local (que l'administrateur peut
réécrire, D254) : c'est un COMPTEUR NV MONOTONE du TPM 2.0, incrémenté à chaque
scellage et lu AU CHARGEMENT avant toute entrée dans le chemin d'exécution.

Ce que le kit éprouve — sur SIMULATEUR logiciel, la sémantique TPM 2.0 nommée :
  - nominal : version scellée == compteur → OUVERT ;
  - rejeu d'un binaire ancien → RETOUR-EN-ARRIERE ;
  - restauration cohérente binaire + état → RETOUR-EN-ARRIERE (le NV survit) ;
  - compteur absent ou inaccessible → ANCRE-PERDUE (fail-closed) ;
  - TPM clear / ownership takeover → ANCRE-PERDUE, jamais de réinitialisation ;
  - incrément non monotone tenté → INCREMENT-NON-MONOTONE ;
  - artefact plus récent que le compteur → SCELAGE-NON-ENREGISTRE.
L'agrégateur REFUSE tout run manquant : jamais un verdict partiel.

STATUT : mécanisme éprouvé sur SIMULATEUR ; le run matériel est le geste du
développeur, EN ATTENTE — aucun chiffre matériel n'est annoncé.
"""
import sys


class Refus(Exception):
    pass


class SimulateurNV:
    """Le compteur NV : présence, valeur, effacement (TPM clear), journal."""
    def __init__(self, valeur=0, present=True):
        self.valeur = valeur
        self.present = present
        self.efface = False
        self.journal = []

    def increment(self, delta=1):
        if not self.present or self.efface:
            raise Refus("ANCRE-PERDUE")
        if delta != 1:
            raise Refus("INCREMENT-NON-MONOTONE")
        self.valeur += 1
        self.journal.append(self.valeur)
        return self.valeur

    def lire(self):
        if self.efface or not self.present:
            raise Refus("ANCRE-PERDUE")
        return self.valeur

    def clear(self):  # TPM2_Clear / ownership takeover
        self.efface = True


def porte_chargement(version_scellee, nv):
    """La porte : le NV est lu AVANT toute exécution ; tout écart est un refus nommé."""
    compteur = nv.lire()
    if version_scellee < compteur:
        raise Refus("RETOUR-EN-ARRIERE")
    if version_scellee > compteur:
        raise Refus("SCELAGE-NON-ENREGISTRE")
    return "OUVERT"


def agrege(runs, attendus):
    """Refuse tout run manquant : un verdict partiel n'existe pas."""
    manquants = [r for r in attendus if r not in runs]
    if manquants:
        raise Refus("RUN-MANQUANT:" + ",".join(manquants))
    ok = all(runs[r] == "VERT" for r in attendus)
    return "VERT" if ok else "ROUGE"


def autotest():
    essais = []

    def essai(nom, f, attendu):
        try:
            rendu = f()
        except Refus as e:
            rendu = e.args[0]
        essais.append((nom, rendu, attendu, rendu == attendu))

    essai("nominal (artefact == compteur)", lambda: porte_chargement(12, SimulateurNV(12)), "OUVERT")
    essai("rejeu d'un binaire ancien", lambda: porte_chargement(11, SimulateurNV(12)), "RETOUR-EN-ARRIERE")
    essai("restauration cohérente binaire+état (le NV survit)", lambda: porte_chargement(11, SimulateurNV(12)), "RETOUR-EN-ARRIERE")
    essai("compteur absent", lambda: porte_chargement(12, SimulateurNV(12, present=False)), "ANCRE-PERDUE")
    essai("TPM clear", lambda: (lambda n: (n.clear(), n.lire()))(SimulateurNV(12))[1], "ANCRE-PERDUE")
    essai("incrément non monotone", lambda: SimulateurNV(12).increment(2), "INCREMENT-NON-MONOTONE")
    essai("artefact plus récent que le compteur", lambda: porte_chargement(13, SimulateurNV(12)), "SCELAGE-NON-ENREGISTRE")
    essai("agrégateur complet", lambda: agrege({k: "VERT" for k in "ABCDE"}, "ABCDE"), "VERT")
    essai("agrégateur partiel", lambda: agrege({"A": "VERT", "B": "VERT"}, "ABCDE"), "RUN-MANQUANT:C,D,E")
    essai("compteur remis à zéro non déclaré", lambda: porte_chargement(12, SimulateurNV(0)), "SCELAGE-NON-ENREGISTRE")
    def scelle_et_charge():
        n = SimulateurNV(12); n.increment(); return porte_chargement(13, n)
    essai("scellage puis chargement à la nouvelle version", scelle_et_charge, "OUVERT")
    essai("agrégateur complet avec un ROUGE", lambda: agrege({**{k: "VERT" for k in "ABCD"}, "E": "ROUGE"}, "ABCDE"), "ROUGE")
    print("=" * 78)
    print("KIT TPM R10 — COMPTEUR NV MONOTONE (simulateur ; run matériel EN ATTENTE)")
    print("=" * 78)
    verts = 0
    for nom, rendu, attendu, ok in essais:
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} → {rendu}")
    print(f"{verts}/{len(essais)} — simulateur ; matériel EN ATTENTE, aucun chiffre")
    return 0 if verts == len(essais) else 3


if __name__ == "__main__":
    sys.exit(autotest())
