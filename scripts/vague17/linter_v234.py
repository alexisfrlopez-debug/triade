#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linter v2.3.4 — LA GARDE DES CONSIGNES ACTIVES (atelier W17R1D81).

Objet : empêcher qu'une consigne HISTORIQUE de la garde D81 (« la phrase de
contrôle se sauvegarde au dépôt, commit, push, remplacement du fichier ») soit
exécutée comme une procédure ACTIVE. D223 a remplacé D81 : la phrase vit sous
séquestre à seuil 5/3, en AUCUN dépôt.

Deux classes :
  ACTIVE-PRESCRIPTIVE  — une ligne qui demande un geste git/push/dépôt sur la
                         phrase de contrôle sans marqueur historique  -> REFUS
  HISTORIQUE-DATEE     — la même mention, portée par un marqueur historique
                         (HISTORIQUE, DATÉE, une plage de dates, « du 4 au
                         19 novembre 2026 », append-only, amendée)          -> ADMIS

Le linter ne lit JAMAIS la valeur d'un secret : il ne rapporte que le chemin,
la classe et un motif expurgé.

Usage :
  python3 scripts/vague17/linter_v234.py                 # balaie les consignes actives
  python3 scripts/vague17/linter_v234.py --controle-negatif   # autotest 2/2
Sorties : 0 = conforme ; 2 = violation (une consigne active non datée).
"""
import argparse
import os
import re
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Les pièces où une mention NON datée est une violation : les consignes actives.
CIBLES = [
    "REPRISE_PROJET.md",
    "OU-TROUVER-LES-LIVRABLES.md",
    "LISEZMOI-PHRASE-CONTROLE.txt",
    "LISEZMOI-ARCHIVE.txt",
    "docs/PROTOCOLE_TRIADE.md",
    "docs/FORMAT_CARTE.md",
    "docs/DECISIONS.md",
    "docs/TABLEAU_BORD.md",
    "docs/PLAN_MILESTONES.md",
]

SUJET = re.compile(r"phrase[- _]de[- _]contr|PHRASE-CONTROLE", re.I)
GESTE = re.compile(
    r"\b(commit\w*|push\w*|pouss\w+|t[ée]l[ée]vers\w*|d[ée]pos\w+|sauvegard\w+|remplac\w+|restaur\w+)\b",
    re.I,
)
# Marqueurs d'historicité : sur la ligne, ou dans les trois lignes qui précèdent,
# ou dans l'en-tête du fichier (les 12 premières lignes).
HISTO = re.compile(
    r"HISTORIQUE|HISTOIRE|DAT[ÉE]E|historique|append-only|amend[ée]"
    r"|non appliqu[ée]e|document[ée]e|depuis le\s+\d"
    r"|\d{1,2}/\d{1,2}/\d{4}",
    re.I,
)
PLAGE = re.compile(r"du\s+\d{1,2}\s+au\s+\d{1,2}\s+\w+\s+\d{4}", re.I)


def lire(chemin):
    try:
        with open(chemin, "r", encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except OSError:
        return None


def classer(lignes):
    """-> (violations, admises) ; chaque entrée = (numero_ligne, classe)."""
    entete = "\n".join(lignes[:12])
    viol, admis = [], []
    for i, ligne in enumerate(lignes):
        if not SUJET.search(ligne) or not GESTE.search(ligne):
            continue
        fenetre = "\n".join(lignes[max(0, i - 5): i + 3])
        marque = bool(HISTO.search(fenetre) or PLAGE.search(fenetre))
        # l'en-tête du fichier peut porter le marqueur d'historicité global
        if not marque and re.search(r"HISTORIQUE|HISTOIRE DAT", entete, re.I):
            marque = True
        (admis if marque else viol).append((i + 1, "ACTIVE-PRESCRIPTIVE" if not marque else "HISTORIQUE-DATEE"))
    return viol, admis


def balayer(cibles):
    total_viol, total_admis, absents = [], [], []
    for rel in cibles:
        chemin = rel if os.path.isabs(rel) else os.path.join(RACINE, rel)
        if not os.path.isfile(chemin):
            absents.append(rel)
            continue
        lignes = lire(chemin)
        if lignes is None:
            continue
        viol, admis = classer(lignes)
        for num, classe in viol:
            total_viol.append((rel, num, classe))
        for num, classe in admis:
            total_admis.append((rel, num, classe))
    return total_viol, total_admis, absents


def rapport(viol, admis, absents, silencieux=False):
    if not silencieux:
        for rel, num, classe in admis:
            print(f"[linter-v234] ADMIS   {rel}:{num}  {classe}")
        for rel in absents:
            print(f"[linter-v234] ABSENT  {rel} (pièce non trouvée, non comptée)")
        for rel, num, classe in viol:
            print(f"[linter-v234] REFUSÉ  {rel}:{num}  {classe} — consigne active de remise D81 sans marqueur historique")
        print(f"[linter-v234] {len(admis)} mention(s) historique(s) admise(s), "
              f"{len(viol)} consigne(s) active(s) refusée(s)")
    return 2 if viol else 0


def controle_negatif():
    """Deux fixtures : la consigne active DOIT être refusée, la datée DOIT passer."""
    actif = (
        "PROCÉDURE DE REMISE — à chaque rotation, remplacer la ligne de\n"
        "PHRASE-CONTROLE-COFFRE.txt, committer AVANT TOUT puis pousser sur GitHub.\n"
    )
    date = (
        "HISTORIQUE (du 4 au 19 novembre 2026, amendée par D223) — la remise\n"
        "consistait à committer PHRASE-CONTROLE-COFFRE.txt puis à pousser sur GitHub.\n"
    )
    ok = 0
    with tempfile.TemporaryDirectory() as d:
        for nom, texte in (("actif.txt", actif), ("date.txt", date)):
            with open(os.path.join(d, nom), "w", encoding="utf-8") as f:
                f.write(texte)
        v_actif, a_actif = classer(lire(os.path.join(d, "actif.txt")))
        v_date, a_date = classer(lire(os.path.join(d, "date.txt")))
    if v_actif and not a_actif:
        print("[linter-v234] autotest 1/2 : la consigne ACTIVE est REFUSÉE — vert")
        ok += 1
    else:
        print("[linter-v234] autotest 1/2 : ÉCHEC — la consigne active n'est pas refusée")
    if a_date and not v_date:
        print("[linter-v234] autotest 2/2 : la mention DATÉE est ADMISE — vert")
        ok += 1
    else:
        print("[linter-v234] autotest 2/2 : ÉCHEC — la mention datée est refusée à tort")
    print(f"[linter-v234] contrôle négatif : {ok}/2")
    return 0 if ok == 2 else 2


def main():
    p = argparse.ArgumentParser(description="Garde des consignes actives D81/D223")
    p.add_argument("--controle-negatif", action="store_true", help="autotest 2/2 des deux classes")
    p.add_argument("--fichier", action="append", default=None, help="chemin à balayer (répétable)")
    a = p.parse_args()
    if a.controle_negatif:
        sys.exit(controle_negatif())
    cibles = a.fichier or CIBLES
    viol, admis, absents = balayer(cibles)
    sys.exit(rapport(viol, admis, absents))


if __name__ == "__main__":
    main()
