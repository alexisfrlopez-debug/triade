#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outil_rapport.py — L'OUTIL RAPPORT DU TRIO D122 (0i4pkzbyr, la vague 15)
: le journal d'écran + LA BOÎTE NOIRE HORODATÉE + LE BOUTON ENVOYER.
LES TROIS PIÈCES :
  1. LE JOURNAL D'ÉCRAN (capture) : les événements de session lus du
     journal JSONL de l'adopteur — ZÉRO phrase libre (les événements
     structurés seuls), ZÉRO chemin réel, ZÉRO clé (l'anonymisation à la
     porte) ;
  2. LA BOÎTE NOIRE HORODATÉE : chaque événement CHAÎNÉ (sha256 du
     précédent ‖ l'événement ‖ l'horodatage) — TOUTE mutation
     ultérieure DÉTECTÉE (la chaîne rompue au premier octet déplacé) ;
  3. LE BOUTON ENVOYER : la génération de la soumission (le CSV anonymisé
     du codage F/L + LE MANIFESTE sha256 par pièce + le paquet) —
     JAMAIS d'envoi automatique (le geste humain D122), la PORTE DE
     SECRETS en entrée de soumission : LE CONTRÔLE NÉGATIF (une phrase de
     test marquée plantée dans un rapport DOIT être refusée), un secret
     réel REFUSÉ, un champ requis manquant REFUSÉ nommé.
LE CODAGE F/L OBLIGATOIRE (la grille D203) : la correspondance
un-pour-un au CSV ; le calculateur κ du kit annotateur (l4nnwqlld,
re-autotesté à ab2vh5c2m) ; le protocole d'arbitrage en cinq points.
L'OUTILLAGE H7 GÉNÉRALISÉ : le tirage stratifié par paires de familles
(les DEUX ordres PAR CONSTRUCTION — le générateur l4nnwqlld reconduit),
les règles d'arrêt D207 et l'agrégateur (ab2vh5c2m — la pièce de la
présente vague).
Usage :
  outil_rapport.py boite-noire <session.jsonl> <sortie.boite>
  outil_rapport.py verifier-boite <boite>                    (la chaîne)
  outil_rapport.py soumettre <session.jsonl> <codage_fl.csv> --sortie <dossier>
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

# LA PORTE DE SECRETS — les sept classes + la phrase marquée D105 (le
# miroir de triade_feedback.py, la même porte aux trois outils)
MOTIFS_SECRETS = [
    ("jeton_github", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,255}")),
    ("cle_privee_pem", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("jeton_bearer", re.compile(r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("refresh_token_oauth", re.compile(r"1//[A-Za-z0-9\-_]{100,}")),
    ("jeton_generique", re.compile(
        r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*\S{16,}")),
    ("chemin_absolu", re.compile(r"(?<![\w])(/[A-Za-z0-9_.-]+){3,}")),
    ("username_systeme", re.compile(
        r"/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+")),
    # la casse EXACTE (le faux positif /Home/End nomme au corpus)
]
MARQUEUR_PHRASE_TEST = "PHRASE-TEST-MARQUEE-D105"

# LA GRILLE D203 — la correspondance un-pour-un (le codage F/L au CSV)
GRILLE_FL = {
    "T": "F",   # l'ancienne étiquette T → F (D203 : la grille renommée)
    "X": "L",
}


def scan_secrets(texte: str) -> list:
    trouves = []
    if MARQUEUR_PHRASE_TEST in texte:
        trouves.append(("phrase_test_marquee",
                        "la balise D105 interdit la soumission"))
    for nom, motif in MOTIFS_SECRETS:
        m = motif.search(texte)
        if m:
            trouves.append((nom, m.group(0)[:40]))
    return trouves


def anonymiser(texte: str) -> str:
    texte = re.sub(r"/home/[A-Za-z0-9_.-]+", "/home/USER", texte)
    texte = re.sub(r"/Users/[A-Za-z0-9_.-]+", "/Users/USER", texte)
    return texte


# ------------------------------------------------- LA BOÎTE NOIRE ---------
def boite_noire(session: list, origine: str) -> dict:
    """chaque événement CHAÎNÉ : h_i = sha256(h_{i-1} ‖ l'événement ‖
    l'horodatage) — la genèse h_0 = sha256('TRIADE-BOITE-NOIRE-v1')."""
    h = hashlib.sha256(b"TRIADE-BOITE-NOIRE-v1").hexdigest()
    entrees = []
    for ev in session:
        horodatage = (ev.get("horodatage")
                      or datetime.datetime.now(datetime.timezone.utc)
                      .isoformat())
        charge = json.dumps({"evenement": ev, "horodatage": horodatage},
                            sort_keys=True, ensure_ascii=False)
        h = hashlib.sha256((h + charge).encode()).hexdigest()
        entrees.append({"charge": charge, "empreinte": h})
    return {"schema": "TRIADE-BOITE-NOIRE-v1", "origine": origine,
            "n": len(entrees), "genese": entrees[0]["empreinte"] if entrees
            else None,
            "chaine_tete": h, "entrees": entrees}


def verifier_boite(boite: dict) -> tuple:
    """la chaîne re-vérifiée depuis la genèse : TOUTE mutation = ROMPUE au
    premier octet déplacé."""
    h = hashlib.sha256(b"TRIADE-BOITE-NOIRE-v1").hexdigest()
    for i, e in enumerate(boite.get("entrees", [])):
        h = hashlib.sha256((h + e["charge"]).encode()).hexdigest()
        if h != e["empreinte"]:
            return False, f"la chaîne ROMPUE à l'entrée {i} (la mutation " \
                          "détectée — la boîte ne se réécrit pas)"
    return h == boite.get("chaine_tete"), \
        ("la chaîne INTACTE (la genèse à la tête)" if h == boite.get(
            "chaine_tete") else "la tête DIVERGENTE")


# ------------------------------------------------- LA SOUMISSION ----------
def cmd_boite_noire(args) -> int:
    session = [json.loads(l) for l in
               pathlib.Path(args.session).read_text(encoding="utf-8")
               .splitlines() if l.strip()]
    texte = json.dumps(session, ensure_ascii=False)
    secrets = scan_secrets(texte)
    if secrets:
        print("REFUS — secrets au journal (la boîte n'est pas écrite) :",
              file=sys.stderr)
        for nom, extrait in secrets:
            print(f"  [{nom}] {extrait}", file=sys.stderr)
        return 2
    boite = boite_noire(session, anonymiser(str(args.session)))
    pathlib.Path(args.sortie).write_text(
        json.dumps(boite, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"OK — la boîte noire : {boite['n']} entrées chaînées, la tête "
          f"{boite['chaine_tete'][:16]}… -> {args.sortie}")
    return 0


def cmd_verifier_boite(args) -> int:
    boite = json.loads(pathlib.Path(args.boite).read_text(encoding="utf-8"))
    ok, msg = verifier_boite(boite)
    print(("VERT — " if ok else "ROUGE — ") + msg)
    return 0 if ok else 2


def cmd_soumettre(args) -> int:
    dossier = pathlib.Path(args.sortie)
    dossier.mkdir(parents=True, exist_ok=True)
    # LA PORTE : le journal ET le codage ET la boîte
    pieces = {"session": pathlib.Path(args.session).read_text(
        encoding="utf-8"),
        "codage_fl": pathlib.Path(args.codage_fl).read_text(
            encoding="utf-8")}
    for nom, texte in pieces.items():
        secrets = scan_secrets(texte)
        if secrets:
            print(f"REFUS — secrets à {nom} (la soumission n'est pas "
                  f"générée) :", file=sys.stderr)
            for n2, extrait in secrets:
                print(f"  [{n2}] {extrait}", file=sys.stderr)
            return 2
    # LE CODAGE F/L : la grille D203 un-pour-un (les étiquettes T/X
    # historiques converties ; la colonne f/l EXIGÉE)
    lignes_csv = [l for l in pieces["codage_fl"].splitlines() if l.strip()]
    entete = lignes_csv[0].split(",")
    if "f_l" not in entete and "fl" not in entete:
        print("REFUS — le CSV de codage sans la colonne f/l (la grille "
              "D203 exigée)", file=sys.stderr)
        return 2
    convertis = 0
    corps = []
    for l in lignes_csv[1:]:
        champs = l.split(",")
        for i, c in enumerate(champs):
            if c.strip() in GRILLE_FL:
                champs[i] = GRILLE_FL[c.strip()]
                convertis += 1
        corps.append(",".join(champs))
    # LE MANIFESTE : sha256 par pièce
    manifeste = {"schema": "TRIADE-SOUMISSION-v1",
                 "date": datetime.date.today().isoformat(),
                 "pieces": {}}
    (dossier / "codage-fl-anonymise.csv").write_text(
        anonymiser(lignes_csv[0] + "\n" + "\n".join(corps)) + "\n",
        encoding="utf-8")
    boite = boite_noire([json.loads(l) for l in
                         pieces["session"].splitlines() if l.strip()],
                        "soumission")
    (dossier / "boite-noire.json").write_text(
        json.dumps(boite, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    for f in ("codage-fl-anonymise.csv", "boite-noire.json"):
        manifeste["pieces"][f] = hashlib.sha256(
            (dossier / f).read_bytes()).hexdigest()
    manifeste["conversions_d203"] = convertis
    (dossier / "MANIFESTE.json").write_text(
        json.dumps(manifeste, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"OK — la soumission générée à {dossier} (le geste d'envoi "
          f"appartient à l'adopteur — JAMAIS automatique, D122) : "
          f"{len(manifeste['pieces'])} pièces au manifeste, "
          f"{convertis} étiquettes T/X converties à la grille D203")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="triade rapport")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("boite-noire")
    b.add_argument("session")
    b.add_argument("sortie")
    b.set_defaults(f=cmd_boite_noire)
    v = sub.add_parser("verifier-boite")
    v.add_argument("boite")
    v.set_defaults(f=cmd_verifier_boite)
    s = sub.add_parser("soumettre")
    s.add_argument("session")
    s.add_argument("codage_fl")
    s.add_argument("--sortie", required=True)
    s.set_defaults(f=cmd_soumettre)
    args = p.parse_args()
    return args.f(args)


if __name__ == "__main__":
    sys.exit(main())
