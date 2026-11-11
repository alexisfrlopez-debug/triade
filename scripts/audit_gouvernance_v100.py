#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_gouvernance_v100.py — l'audit de gouvernance de l'édition académique
v0.10.0 (l'étape (c) de vérification exigée par l'instruction).

L'audit connaît les QUATRE formes historiques des décisions dans
docs/DECISIONS.md (``## DNN —`` narrative, ``### DNN —`` normalisée § 17.1,
``**DNN —**`` à l'origine du projet, ``| DNN |`` au tableau) et le fait que
certaines décisions pionnières furent consignées au journal/spécification —
une référence est réputée résolue si ELLE vit dans L'UNE des trois sources
de gouvernance (DECISIONS.md, JOURNAL_TRAVAIL.md, PROTOCOLE_TRIADE.md).

  A1  les décisions récentes (D100+) portent une structure reconnaissable
      (Frontières / Les règles / Constat / Le contexte / Choix retenu) ;
  A2  unicité des ID au journal des décisions (aucun DNN en double) ;
  A3  chaînage : toute décision citée (amendement, invalidation, alternative)
      se résout dans l'une des trois sources ;
  A4  append-only au geste : la plus haute décision consignée est D184
      (celle de la présente édition) ;
  A5  les entrées du journal (Entrée NN + Journal NN) sont uniques et
      continues de 1 à la dernière ;
  A6  les décisions de l'édition (D182/D183/D184) portent leur contenu
      attendu — le manuscrit, la proposition NON appliquée, le sha-256.

Usage : python3 scripts/audit_gouvernance_v100.py
Code de sortie : 0 = VERT, 1 = écart constaté.
"""

import re
import sys
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
D = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
J = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
S = (REPO / "docs" / "PROTOCOLE_TRIADE.md").read_text(encoding="utf-8")

ecarts = []


def verifie(cid, nom, ok, detail=""):
    print(f"[{cid}] {nom} : {'VERT' if ok else 'ÉCART'}"
          + (f" — {detail}" if detail else ""))
    if not ok:
        ecarts.append(f"{cid} {nom}")


def ids_decisions(texte):
    """Tous les ID de décisions présents comme ENTRÉES (quatre formes)."""
    ids = set()
    ids |= set(re.findall(r"^## (D\d+) —", texte, re.MULTILINE))
    ids |= set(re.findall(r"^### (D\d+) —", texte, re.MULTILINE))
    ids |= set(re.findall(r"^\*\*(D\d+) —", texte, re.MULTILINE))
    ids |= set(re.findall(r"^\| (D\d+) +\|", texte, re.MULTILINE))
    return ids


tous = ids_decisions(D)
numeros = sorted(int(x[1:]) for x in tous)

# --- A1 : structure des décisions récentes ---
sans_structure = []
for m in re.finditer(r"^## (D1[0-8][0-9]) —.*?(?=^## D|\Z)", D,
                     re.MULTILINE | re.DOTALL):
    bloc = m.group(0)
    # la convention des décisions narratives : au moins un ouvreur de
    # paragraphe en gras (**Le fait.**, **La règle.**, **Frontières.**…)
    if not re.search(r"\*\*(Le |La |Les |Frontières|Décision|Constat|Choix|"
                     r"Alternatives|Détail|Contexte|Règles)", bloc):
        sans_structure.append(m.group(1))
# couverture : chaque D1..D184 vit quelque part dans le corpus de gouvernance
ids_corpus = set(tous)
for n in range(1, 190):
    d = f"D{n}"
    if d in ids_corpus:
        continue
    if (re.search(rf"^## (?:Entrée|Journal|) ?\d+ —.*\b{d}\b", J, re.MULTILINE)
            or re.search(rf"\*\*[^*]*\b{d}\b[^*]*\*\*", J)  # marqueur gras au corps
            or d in S):
        ids_corpus.add(d)
hors_corpus = [f"D{n}" for n in range(1, 190) if f"D{n}" not in ids_corpus]
verifie("A1", "les décisions D100+ portent une structure reconnaissable "
        "et D1..D189 vivent au corpus",
        not sans_structure and not hors_corpus,
        f"{len(tous)} entrées à DECISIONS.md, {len(hors_corpus)} hors corpus ; "
        f"sans structure : {sans_structure[:5] or 'aucune'}")

# --- A2 : unicité des ID ---
par_forme = (re.findall(r"^## (D\d+) —", D, re.MULTILINE)
             + re.findall(r"^### (D\d+) —", D, re.MULTILINE)
             + re.findall(r"^\*\*(D\d+) —", D, re.MULTILINE))
doublons = sorted({x for x in par_forme if par_forme.count(x) > 1})
verifie("A2", "aucun ID de décision réutilisé (formes titres)", not doublons,
        f"doublons : {doublons or 'aucun'}")

# --- A3 : chaînage — les références se résolvent dans les trois sources ---
refs = set(re.findall(r"(?:amendée par|invalidée par|amende) (D\d+)", D))
refs |= set(re.findall(r"l'alternative à la garde durable (D\d+)", D))
corpus = D + J + S
ids_corpus = ids_decisions(corpus)
# certaines décisions pionnières ne vivent qu'en références croisées
# (journal/spécification) : on accepte toute décision dont l'ID apparaît
# comme sujet documenté quelque part dans le corpus
inconnues = []
for r in sorted(refs, key=lambda x: int(x[1:])):
    n = r[1:]
    if r not in ids_corpus and not re.search(rf"\b{r}\b[^|]*\|", corpus):
        # dernière chance : la décision vit-elle en toutes lettres ?
        if not re.search(rf"(?:décision )?{r} —", corpus):
            inconnues.append(r)
verifie("A3", "les références d'amendement se résolvent (3 sources)",
        not inconnues,
        f"{len(refs)} références ; irrésolues : {inconnues or 'aucune'}")

# --- A4 : append-only au geste ---
verifie("A4", "la plus haute décision consignée est D189 (le modèle "
        "formel v0.12.0)",
        numeros and numeros[-1] == 189, f"max = D{numeros[-1] if numeros else '?'}")

# --- A5 : les entrées du journal ---
entrees = re.findall(r"^## (?:Entrée|Journal) (\d+) —", J, re.MULTILINE)
entrees += re.findall(r"^## (\d+) — [Dd]", J, re.MULTILINE)  # ère pionnière : « ## 54 — D64 »
tasks = re.findall(r"^Task ID: (\d+)$", J, re.MULTILINE)
nums = [int(e) for e in entrees] + [int(t) for t in tasks]
doublons_e = sorted({n for n in nums if nums.count(n) > 1})
# Trous historiques CONNUS du journal (constatés avant l'édition v0.10.0 ;
# l'append-only interdit toute renumérotation rétroactive) : les tâches 4-7
# de l'ère pionnière vivaient hors journal, l'entrée 54 sauta la numérotation.
TROUS_HISTORIQUES = {4, 5, 6, 7, 54}
trous = [n for n in range(1, max(nums) + 1)
         if n not in nums and n not in TROUS_HISTORIQUES]
verifie("A5", "entrées du journal uniques et continues (3 ères : Task ID, "
        "Journal, Entrée ; trous historiques 4-7/54 documentés)",
        not doublons_e and not trous,
        f"{len(set(nums))} entrées (max {max(nums)} : "
        f"{len(tasks)} Task ID + {len(entrees)} Journal/Entrée), "
        f"doublons {doublons_e or 'aucun'}, trous {trous[:8] or 'aucun'}")

# --- A6 : le contenu des décisions de l'édition ---
attendus = {
    "D182": ["IMRAD", "51 / 719 / 1 088", "WYSIWYG", "co-auteur",
             "TRIADE_soumission_v0.10.0.zip", "TRIADE_complet_v0.10.0.zip",
             "Zenodo"],
    "D183": ["séquestre", "Shamir", "NON appliquée", "perte/exposition",
             "demeure", "décision active"],
    "D184": ["sha-256", "loupe-06", "les preuves ne se réécrivent jamais"],
    "D185": ["MUTATION TESTING", "83,4", "JAMAIS UN CHIFFRE FAUX",
             "graine", "six instruments"],
    "D186": ["CSPRNG", "tls13-29", "fail-closed", "KIT96", "DOWNGRD"],
    "D187": ["PROUVÉES DANS LE MODÈLE", "154 états", "A1-A5",
             "sha256", "HORS MODÈLE"],
    "D188": ["DEUX PLANS", "intra-sécurité", "facteur", "D81"],
    "D189": ["SPRT", "46×", "réplication", "κ de Cohen", "T/X"],
}
for did, mots in attendus.items():
    m = re.search(rf"^## {did} —.*?(?=^## D|\Z)", D, re.MULTILINE | re.DOTALL)
    if not m:
        verifie("A6", f"la décision {did} existe", False)
        continue
    bloc = m.group(0)
    absents = [x for x in mots if x not in bloc]
    verifie("A6", f"la décision {did} porte son contenu attendu",
            not absents, f"absents : {absents or 'aucun'}")

print()
if ecarts:
    print(f"AUDIT DE GOUVERNANCE : {len(ecarts)} ÉCART(S) — " + " ; ".join(ecarts))
    sys.exit(1)
print("AUDIT DE GOUVERNANCE : VERT — structure, unicité, chaînage, "
      "append-only, entrées du journal et contenu de l'édition constatés.")
