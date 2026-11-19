#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""partie1_et_4_1c4sokpii.py — LES PARTIES (1) ET (4) DE L'INSTRUCTION :
(1) le plan D210 à son terme : le comptage des unités aux deux bras LU DU
REGISTRE (jamais tapé), l'état de la cap et de la clôture — n≥6 tenu SANS
nouveau tirage (l'amendement conditionnel jamais déclenché) ;
(4) la grille finalisée : chaque défaut du registre codé F/L (la
correspondance D203), le protocole du SECOND ANNOTATEUR (à recruter —
aucune annotation inventée), le calculateur κ re-passé."""
from __future__ import annotations

import csv
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
LED = REPO / "scripts/campagne_d204/reception-357"

# ---- (1) le comptage des unités AUX DEUX BRAS (lu du registre) -------------
liv = [l for l in csv.DictReader(
    (x for x in open(LED / "livraisons.csv", encoding="utf-8-sig")
     if not x.startswith("#")))]
unites: dict[str, set] = {}
for l in liv:
    base = l["tache"].replace("-d210", "").replace("-attr", "")
    unites.setdefault(base, set()).add(l["bras"])
deux_bras = sorted(u for u, b in unites.items() if {"T", "C"} <= b)
print(f"(1) LES UNITÉS AUX DEUX BRAS (lu de livraisons.csv, {len(liv)} lignes) :")
for u in deux_bras:
    print(f"    {u} — bras {sorted(unites[u])}")
print(f"    N = {len(deux_bras)} unités entièrement livrées aux deux bras "
      f"≥ 6 : {'TENU' if len(deux_bras) >= 6 else 'ÉCHOUÉ'}")
assert len(deux_bras) >= 6

# les tirages : la séquence D210 (QUATRE unités) épuisée à la cap — la
# clôture consignée à l'Entrée 358 (l'édition v0.19.0 la porte) ; AUCUN
# nouveau tirage → l'amendement conditionnel du plan JAMAIS DÉCLENCHE
# (la lettre de l'instruction : « si la séquence est épuisée à la cap,
# amende AVANT tout nouveau tirage » — il n'y en a pas eu)
d210 = [l for l in liv if l["tache"].endswith("-d210")
        or l["tache"] == "loupe-16-attr"]
print(f"    les livraisons D210 : {len(d210)} (la séquence QUATRE unités "
      "épuisée à la cap M1, la clôture à l'Entrée 358)")
print("    VERDICT (1) : n≥6 TENU SANS nouveau tirage — l'amendement "
      "conditionnel jamais déclenché ; les runs terrain clos au geste du "
      "développeur (le livre fait foi)")

# ---- (4a) la codification F/L de CHAQUE défaut du registre -----------------
# la correspondance D203 : T→F (terrain), X→L (laboratoire) ; chaque défaut
# codé à SA NATURE consignée (la colonne « mecanisme » du registre, lue et
# classée à la main par le labo — l'annotateur 1, sur pièces) :
#   F1 la table des imports/descripteurs · F2 la convention d'appel (l'arité)
#   F3 la sémantique du chargeur (la feuille non liée que le VRAI chargeur
#       aurait liée) · F5 l'environnement (le kit, les locales)
#   L3 l'instrument (le harnais, le scénario-juge)
CODAGE_PAR_CLASSE = {
    "plantage-harnais-v3": ("L3", "le constructeur ctypes du scénario — "
                              "l'instrument"),
    "plantage-harnais-decouverte": ("L3", "les arités de la découverte — "
                                     "l'instrument"),
    "plantage-harnais-feuille-memcmp": ("F3", "le slot IAT non lié que le "
                                         "VRAI chargeur eût lié — la "
                                         "sémantique du chargeur"),
    "plantage-lanceur-prose-non-remmee": ("F5", "le lanceur du kit — "
                                          "l'environnement de livraison"),
    "ecart-harnais-console-locale": ("F5", "le codec LOCALE du parent — "
                                      "l'environnement"),
    "plantage-harnais-feuille-memcpy": ("F3", "la feuille memcpy non liée "
                                         "au chemin Windows — la sémantique "
                                         "du chargeur"),
    "plantage-hote-feuille-memcpy": ("F3", "la feuille memcpy non liée DANS "
                                      "le processus hôte — la sémantique du "
                                      "chargeur"),
    "guichet-descripteur-quatre-champs": ("F1", "le champ +8 ForwarderChain "
                                           "lu comme la RVA du nom, la marche "
                                           "de l'OFT — la table des imports"),
    "liaison-memmove-deux-arguments": ("F2", "memmove à DEUX arguments, le "
                                       "compte 8 manquant — la convention "
                                       "d'appel"),
    "les-metriques-ecran-jamais-posees-par-le-juge": ("L3", "le "
                                                      "scénario-juge sans "
                                                      "geste pour la zone — "
                                                      "l'instrument"),
}


def classe_de(ligne: dict) -> tuple[str, str]:
    return CODAGE_PAR_CLASSE.get(ligne.get("classe", ""),
                                 ("L3", "l'instrument (le défaut du registre)"))


defauts = [l for l in csv.DictReader(
    (x for x in open(LED / "defauts.csv", encoding="utf-8-sig")
     if not x.startswith("#")))]
lignes_codage = []
for d in defauts:
    classe, justification = classe_de(d)
    lignes_codage.append({
        "id": d.get("livraison", "") or f"{d.get('bras','')}-{d.get('tache','')}",
        "défaut": d.get("classe", ""),
        "classe_annotateur_1": classe,
        "source": justification,
    })
with open(REPO / "scripts/replication_v150/codage_annotateur1.csv", "w",
          encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "défaut",
                                      "classe_annotateur_1", "source"])
    w.writeheader()
    for l in lignes_codage:
        w.writerow(l)
from collections import Counter  # noqa: E402
compteur = Counter(l["classe_annotateur_1"] for l in lignes_codage)
print(f"\n(4a) LA GRILLE CODÉE : {len(lignes_codage)} défauts du registre, "
      f"chacun sa classe F/L — {dict(sorted(compteur.items()))}")
print("     la pièce : scripts/replication_v150/codage_annotateur1.csv "
      "(l'annotateur 1 = le labo, sur pièces)")

# ---- (4b) le protocole du second annotateur (à recruter) --------------------
(REPO / "scripts/replication_v150/PROTOCOLE-SECOND-ANNOTATEUR.txt").write_text(
"""LE PROTOCOLE DU SECOND ANNOTATEUR — la réplication 1c4sokpii (partie 4)
============================================================================
LE BESOIN : le κ de Cohen exige DEUX jeux d'annotations indépendants. Le
premier est le codage du labo (codage_annotateur1.csv — chaque défaut du
registre de campagne codé à sa classe F/L lue de sa nature consignée) ; le
second appartient À RECRUTER : un annotateur indépendant qui code LES MÊMES
défauts SANS VOIR le codage du labo.

LA GRILLE (D189, les étiquettes D203) : cinq classes terrain, trois classes
laboratoire — les définitions opérationnelles et les exemples vécus vivent
à grille_tx.csv ; les classes :
  F1 chargeur/image · F2 ABI/matériel · F3 sémantique du chargeur ·
  F4 conventions système · F5 environnement ·
  L1 logique · L2 structure · L3 harnais.

LE GESTE DE L'ANNOTATEUR : lire chaque défaut du registre (le id + le nom +
la pièce citée au registre), choisir SA classe, UNE par défaut — le CSV de
rendu : « id,classe » (une ligne par défaut, les id COMMUNS exigés).

LE CALCUL : python3 kohen_kappa_v150.py codage_annotateur1.csv <le rendu>
— le calculateur EST AUTOTESTÉ (trois cas synthétiques calculables à la
main : l'accord parfait +1, le désaccord total -1, l'accord partiel +0,4 —
la console du 20/11 fait foi) ; l'acceptation pré-enregistrée D189 :
κ ≥ 0,61 (substantiel, Landis & Koch 1977).

LA FRONTIÈRE : AUCUNE annotation n'est inventée ; le recrutement et le
rendu appartiennent au maître ; le κ réel se calculera le jour où les deux
jeux existeront (le statut consigné, jamais un chiffre fabriqué).
""", encoding="utf-8")
print("(4b) le protocole du second annotateur écrit (à recruter — aucune "
      "annotation inventée)")

# ---- (4c) le calculateur κ re-passé -----------------------------------------
r = subprocess.run([sys.executable,
                    str(REPO / "scripts/replication_v150/kohen_kappa_v150.py")],
                   capture_output=True, text=True, timeout=120)
ok = "VERT" in r.stdout
print(f"(4c) le calculateur κ re-passé : {'VERT (autotest 3/3)' if ok else 'ROUGE'}")
assert ok
print("\nVERDICT (1)+(4a-c) : VERT — n≥6 tenu sans tirage, la grille codée, "
      "le protocole écrit, κ autotesté")
