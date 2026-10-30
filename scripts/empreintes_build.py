#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Empreintes par build ACTIVES (M5-a, D134).

Le critère de sortie du chantier (a) du jalon M5 (docs/PLAN_MILESTONES.md) :
« tout artefact livré porte son empreinte CONSIGNÉE par le build qui l'a
produit ; une divergence inter-build est un refus nommé ». Avant D134, la
chaîne build_pdf.sh écrivait bien un stamp (.pdf_build.stamp) mais ce stamp
est l'empreinte des SOURCES, pas celle de l'ARTEFACT : le PDF produit pouvait
être échangé, vieillir ou diverger sans qu'aucun contrôle ne le nomme. Le
correctif structurel :

  1. `consigner` — appelé PAR LE BUILD lui-même (build_pdf.sh étape 5bis,
     build_livre.sh étape 7) juste après la publication de l'artefact :
     sha256 + md5 + taille consignés au TABLEAU DE BORD (docs/TABLEAU_BORD.md,
     généré, jamais édité à la main) ET au JOURNAL DE TRAVAIL (une ligne par
     build, sous le marqueur « m5a:journal-des-builds ») ;
  2. `verifier` — la comparaison inter-build devient un CONTRÔLE AUTOMATIQUE :
     chaque PDF livré sous docs/ doit exister au registre, l'octet sur disque
     doit être l'octet consigné, deux builds des MÊMES sources doivent produire
     le MÊME artefact, et une copie de livraison (download/) doit suivre —
     toute dérive est un REFUS NOMMÉ ;
  3. `modules` — les empreintes md5 des 15 modules d'ANNEXE A (spec v0.6.0,
     mesurées à c504436) se mesurent en direct depuis les blobs git du dépôt :
     le recoupement du terrain (« mon clone diverge-t-il du dépôt ? ») devient
     une commande, l'écart un verdict.

DICTIONNAIRE DES REFUS NOMMÉS (verifier / modules) :
  ARTEFACT-ABSENT                l'artefact consigné n'est plus sur le disque
  EMPREINTE-DIVERGENTE           l'artefact sur disque ≠ dernière consignation
                                 (modifié hors build, ou build non consigné)
  ARTEFACT-DELIVRÉ-NON-CONSIGNÉ  un PDF livré sous docs/ est hors registre
  BUILD-NON-DÉTERMINISTE         deux consignations du même stamp de sources
                                 portent des sha256 différents
  COPIE-DIVERGENTE               la copie de livraison (download/) ≠ dépôt
  REGISTRE-ILLISIBLE             une ligne du registre ne respecte pas le format
  MODULE-DIVERGENT               un module du dépôt ≠ ANNEXE A (spec v0.6.0)

Propriétés :
  - stdlib seule (hashlib, subprocess, argparse — aucune dépendance) ;
  - un seul écrivain : docs/TABLEAU_BORD.md est GÉNÉRÉ intégralement à chaque
    consignation, jamais édité à la main ;
  - idempotent : re-consigner le même octet avec le même stamp et le même
    build n'ajoute AUCUNE entrée ;
  - sûr : aucun secret manipulé, aucune clé touchée — des empreintes publiques.

Usage :
  python3 scripts/empreintes_build.py consigner --artefact docs/X.pdf \
      --build "build_pdf.sh" [--stamp-file .pdf_build.stamp | --stamp <hex>]
  python3 scripts/empreintes_build.py verifier
  python3 scripts/empreintes_build.py modules
  python3 scripts/empreintes_build.py etat

Codes de sortie : 0 = vert ; 1 = refus nommés (verifier/modules) ;
2 = erreur fatale nommée (consigner/lecture).
Variable d'environnement TRIADE_EMPREINTES_ROOT : racine du projet (tests).
"""

import argparse
import datetime
import hashlib
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(
    os.environ.get("TRIADE_EMPREINTES_ROOT",
                   str(pathlib.Path(__file__).resolve().parents[1]))
).resolve()
DOCS = ROOT / "docs"
TDB = DOCS / "TABLEAU_BORD.md"
JOURNAL = DOCS / "JOURNAL_TRAVAIL.md"
DOWNLOAD = ROOT.parent / "download"

MARQUEUR_JOURNAL = (
    "<!-- m5a:journal-des-builds v1 — consignation automatique des empreintes "
    "par build (D134). Les entrées numérotées du journal s'insèrent TOUJOURS "
    "AVANT la présente ligne ; les lignes de build s'ajoutent SOUS elle, la "
    "plus récente en tête. Ne pas édier à la main. -->"
)

# ANNEXE A de la spec v0.6.0 (D133) — md5 mesurés au dépôt, commit c504436,
# contenu canonique LF (blobs git). « (racine) » = fichier à la racine du dépôt.
MODULES_ANNEXE_A = [
    ("coffre_fort.py",              "8c79263b9b4694662fb722a67f14ee82",
     "coffre CF1 (migration CF1 → CF2) — racine du dépôt"),
    ("v06/coffre_cf2.py",           "f50ce894db276818d68dd1e22a92fa4c",
     "coffre CF2 — Shamir, sentinelle, porte D120"),
    ("v06/coffre_cf3.py",           "1cf18644d70073bf82f1f2847976f17d",
     "coffre CF3 — serrure piégée, migration, destruction"),
    ("v06/sceau_I.py",              "baf727058504490c288630dbc5bd9664",
     "sceau de l'Intention — préparateur, dépositeur, vérificateur"),
    ("v06/ceremonie_hors_ligne.py", "982bf0a402607b67a3960952a0adcb11",
     "cérémonie air-gap (stdlib seule)"),
    ("v06/ceremonie_gui.py",        "e4745580b19e7e5508f596b83bb1652f",
     "maître de cérémonie graphique (v2.2, D131)"),
    ("v06/migration_cf3_gui.py",    "933e8405fa49ecad1d11861bd37d1c7a",
     "GUI de migration CF2 → CF3 (v1.1, D132)"),
    ("v06/autotest_cf3_gui.py",     "bcd243448873d633852af27f204ecc27",
     "autotest CF3 graphique"),
    ("v06/sentinelle_cf2.py",       "bbc487423302c7f8f821ff348f3737c4",
     "sentinelle CF2 (moteur laboratoire)"),
    ("v06/test_cf2.py",             "f55fbee3391bbbb4466ba096c06b2ad7",
     "falsifiabilité CF2 (Shamir, sentinelle, restauration)"),
    ("v06/test_coffre_cf3.py",      "33f460171f69aa59ae40192b5de46114",
     "falsifiabilité CF3 (course de clôture, pannes)"),
    ("v06/test_sceau_I.py",         "a4b43fd5aa37acb37e98b77dca5747fc",
     "falsifiabilité du sceau de l'Intention"),
    ("v06/test_migration_cf3.py",   "9e078dfdebea4bbe88b72fb71ab907bd",
     "falsifiabilité de la migration CF2 → CF3"),
    ("v06/test_migration_cf3_gui.py", "5f93800b887e44f52b1e998d5aabf160",
     "falsifiabilité du GUI de migration"),
    ("v06/test_ceremonie_gui.py",   "e275efb83c104bcac30f05d96c7ce318",
     "falsifiabilité du maître de cérémonie"),
]

# ---------------------------------------------------------------- utilitaires

def _sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def _commit():
    """Commit HEAD au moment de l'appel (« hors-git » si échec)."""
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return "hors-git"


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normaliser_chemin(brut):
    """Chemin d'artefact : relatif à ROOT, séparateurs '/', aucun '..'."""
    p = pathlib.Path(brut)
    if p.is_absolute():
        try:
            p = p.relative_to(ROOT)
        except ValueError:
            raise ValueError(f"artefact hors projet ({brut})")
    s = p.as_posix()
    if s.startswith("..") or "/../" in s or s == ".":
        raise ValueError(f"chemin invalide ({brut})")
    return s


# ------------------------------------------------------------- registre (I/O)

LIGNE_REGISTRE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s*\|"
    r"\s*([0-9a-f]{7,40}|hors-git)\s*\|\s*([^\s|]+)\s*\|"
    r"\s*([0-9a-f]{64})\s*\|\s*([0-9a-f]{32})\s*\|\s*(\d+)\s*\|"
    r"\s*([0-9a-f]{64}|—)\s*\|\s*([^|\n]+?)\s*\|$"
)


def lire_registre():
    """Lit le registre (section « Registre des consignations » du tableau).

    Retourne (entrées, anomalies) ; entrées = liste de dictionnaires dans
    l'ordre chronologique. Une ligne de table qui ne respecte pas le format
    est une anomalie → refus REGISTRE-ILLISIBLE.
    """
    entrees, anomalies = [], []
    if not TDB.exists():
        return entrees, anomalies
    dans_registre = False
    for ligne in TDB.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("## Registre des consignations"):
            dans_registre = True
            continue
        if dans_registre and ligne.startswith("## "):
            break
        if not dans_registre or not ligne.startswith("|"):
            continue
        if re.match(r"^\|\s*N\s*\|", ligne) or ligne.startswith("| ---"):
            continue
        m = LIGNE_REGISTRE.match(ligne)
        if not m:
            anomalies.append(ligne.strip()[:80])
            continue
        n, date, commit, artefact, sha, md5v, taille, stamp, build = m.groups()
        entrees.append({"n": int(n), "date": date, "commit": commit,
                        "artefact": artefact, "sha256": sha, "md5": md5v,
                        "taille": int(taille), "stamp": stamp, "build": build.strip()})
    return entrees, anomalies


def ecrire_tableau(entrees):
    """Régénère INTÉGRALEMENT docs/TABLEAU_BORD.md (l'unique écrivain)."""
    dernier = {}
    for e in entrees:
        dernier[e["artefact"]] = e
    l = []
    l.append("# Tableau de bord des empreintes par build — TRIADE (M5-a, D134)")
    l.append("")
    l.append("> Fichier GÉNÉRÉ par `scripts/empreintes_build.py` — ne jamais éditer à la main.")
    l.append("> Chaque build consigne ici l'empreinte de l'artefact qu'il a produit (D134) ;")
    l.append("> la comparaison inter-build est un contrôle automatique (`verifier`) et toute")
    l.append("> divergence est un REFUS NOMMÉ. Le journal de travail reçoit une ligne par build")
    l.append("> (marqueur « m5a:journal-des-builds »). Référence : spec v0.6.0 § M5, plan M5 (a).")
    l.append("")
    l.append("## État courant (dernière consignation par artefact)")
    l.append("")
    l.append("| Artefact | Date (UTC) | Commit | sha256 | md5 | Taille (o) | Stamp | Build |")
    l.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    if dernier:
        for a in sorted(dernier):
            e = dernier[a]
            l.append("| {artefact} | {date} | {commit} | {sha256} | {md5} | "
                     "{taille} | {stamp} | {build} |".format(**e))
    else:
        l.append("| — | — | — | — | — | — | — | — |")
    l.append("")
    l.append("## Registre des consignations (chronologique)")
    l.append("")
    l.append("| N | Date (UTC) | Commit | Artefact | sha256 | md5 | Taille (o) | Stamp | Build |")
    l.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for e in entrees:
        l.append("| {n} | {date} | {commit} | {artefact} | {sha256} | {md5} | "
                 "{taille} | {stamp} | {build} |".format(**e))
    l.append("")
    TDB.write_text("\n".join(l), encoding="utf-8")


def ecrire_ligne_journal(entree):
    """Insère la ligne de build sous le marqueur (la plus récente en tête)."""
    ligne = ("- {date} · {commit} · {artefact} · sha256 {sha256} · md5 {md5} · "
             "{taille} o · {build}").format(**entree)
    if not JOURNAL.exists():
        JOURNAL.write_text(MARQUEUR_JOURNAL + "\n" + ligne + "\n", encoding="utf-8")
        return
    contenu = JOURNAL.read_text(encoding="utf-8")
    lignes = contenu.split("\n")
    if MARQUEUR_JOURNAL not in lignes:
        contenu = contenu.rstrip("\n") + "\n\n" + MARQUEUR_JOURNAL + "\n" + ligne + "\n"
        JOURNAL.write_text(contenu, encoding="utf-8")
        return
    i = lignes.index(MARQUEUR_JOURNAL)
    lignes.insert(i + 1, ligne)
    JOURNAL.write_text("\n".join(lignes), encoding="utf-8")


# ------------------------------------------------------------------ commandes

def cmd_consigner(args):
    try:
        artefact = _normaliser_chemin(args.artefact)
    except ValueError as exc:
        print(f"[empreintes] ERREUR : {exc}")
        return 2
    chemin = ROOT / artefact
    if not chemin.is_file():
        print(f"[empreintes] ERREUR : artefact introuvable ({artefact})")
        return 2
    if "|" in args.build or "\n" in args.build:
        print("[empreintes] ERREUR : libellé de build invalide (pas de « | »)")
        return 2
    args.build = args.build.strip()
    if args.stamp_file:
        stamp = (ROOT / args.stamp_file).read_text(encoding="utf-8").strip()
    elif args.stamp:
        stamp = args.stamp.strip()
    else:
        stamp = "—"
    entrees, anomalies = lire_registre()
    if anomalies:
        for a in anomalies:
            print(f"[empreintes] REFUS REGISTRE-ILLISIBLE : {a}")
        return 2
    sha = _sha256(chemin)
    md5v = _md5(chemin)
    taille = chemin.stat().st_size
    commit = _commit()
    # idempotence : même octet, même stamp, même build → rien à consigner
    dernier = next((e for e in reversed(entrees) if e["artefact"] == artefact), None)
    if dernier and dernier["sha256"] == sha and dernier["stamp"] == stamp \
            and dernier["build"] == args.build:
        print(f"[empreintes] inchangé — {artefact} déjà consigné "
              f"(sha256 {sha[:12]}…, stamp {stamp[:12]}…)")
        return 0
    e = {"n": len(entrees) + 1, "date": _utc(), "commit": commit,
         "artefact": artefact, "sha256": sha, "md5": md5v,
         "taille": taille, "stamp": stamp, "build": args.build}
    entrees.append(e)
    ecrire_tableau(entrees)
    ecrire_ligne_journal(e)
    print(f"[empreintes] consigné n°{e['n']} — {artefact} · sha256 {sha[:12]}… · "
          f"md5 {md5v} · {taille} o · stamp {stamp[:12]}… · {args.build}")
    return 0


def _pdf_livres():
    """PDF livrés sous docs/ (présents sur le disque, tracked ou non)."""
    return sorted(str(p.relative_to(ROOT)) for p in DOCS.glob("*.pdf"))


def cmd_verifier(args):
    refus = []
    entrees, anomalies = lire_registre()
    for a in anomalies:
        refus.append(f"REGISTRE-ILLISIBLE : ligne non conforme — {a}")
    livres = _pdf_livres()
    au_registre = {e["artefact"] for e in entrees}
    # R3 — tout artefact livré porte son empreinte consignée
    for p in livres:
        if p not in au_registre:
            refus.append(f"ARTEFACT-DELIVRÉ-NON-CONSIGNÉ : {p}")
    # dernière consignation par artefact
    dernier = {}
    for e in entrees:
        dernier[e["artefact"]] = e
    for artefact, e in sorted(dernier.items()):
        chemin = ROOT / artefact
        # R1 — l'artefact consigné existe
        if not chemin.is_file():
            refus.append(f"ARTEFACT-ABSENT : {artefact} (consigné n°{e['n']}, "
                         f"sha256 {e['sha256'][:12]}…)")
            continue
        # R2 — l'octet sur disque est l'octet consigné
        sha = _sha256(chemin)
        if sha != e["sha256"]:
            refus.append(f"EMPREINTE-DIVERGENTE : {artefact} — disque {sha[:12]}… "
                         f"≠ consigné {e['sha256'][:12]}… (n°{e['n']})")
        # R5 — la copie de livraison (download/) suit le dépôt
        copie = DOWNLOAD / pathlib.Path(artefact).name
        if copie.is_file() and _sha256(copie) != e["sha256"]:
            refus.append(f"COPIE-DIVERGENTE : {copie} ≠ dépôt ({artefact}, "
                         f"n°{e['n']})")
    # R4 — deux builds des mêmes sources produisent le même artefact
    par_stamp = {}
    for e in entrees:
        if e["stamp"] == "—":
            continue
        par_stamp.setdefault((e["artefact"], e["stamp"]), set()).add(e["sha256"])
    for (artefact, stamp), shas in sorted(par_stamp.items()):
        if len(shas) > 1:
            refus.append(f"BUILD-NON-DÉTERMINISTE : {artefact} — stamp {stamp[:12]}… "
                         f"produit {len(shas)} sha256 différents")
    bilan = (f"[empreintes] verifier : {len(livres)} PDF livrés, "
             f"{len(entrees)} consignations, {len(dernier)} artefacts au registre — "
             f"{len(refus)} refus")
    print(bilan)
    for r in refus:
        print(f"[empreintes] REFUS {r}")
    if refus:
        print("[empreintes] VERDICT : refus nommés ci-dessus — comparer, "
              "consigner ou rétablir avant toute livraison")
        return 1
    print("[empreintes] VERDICT : VERT — tout artefact livré porte son "
          "empreinte consignée par le build qui l'a produit")
    return 0


def cmd_modules(args):
    divergents = 0
    print("[empreintes] modules — référence ANNEXE A spec v0.6.0 "
          "(15 modules, mesurés à c504436) contre les blobs git HEAD :")
    for chemin, attendu, role in MODULES_ANNEXE_A:
        try:
            r = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob",
                                f"HEAD:{chemin}"], capture_output=True, timeout=30)
            if r.returncode != 0:
                print(f"[empreintes] REFUS MODULE-DIVERGENT : {chemin} — "
                      f"absent du dépôt git")
                divergents += 1
                continue
            mesure = _md5_bytes(r.stdout)
        except Exception:
            print(f"[empreintes] ERREUR : git illisible pour {chemin}")
            return 2
        if mesure == attendu:
            print(f"[empreintes]   vert   {chemin} — {attendu}")
        else:
            print(f"[empreintes] REFUS MODULE-DIVERGENT : {chemin} — dépôt "
                  f"{mesure} ≠ ANNEXE A {attendu} ({role})")
            divergents += 1
    if divergents:
        print(f"[empreintes] VERDICT : {divergents} module(s) divergent(s) — "
              "fin de ligne ou génération périmée : la commande git fait foi, "
              "le manifeste du kit tranche")
        return 1
    print("[empreintes] VERDICT : VERT — les 15 modules du dépôt portent les "
          "empreintes d'ANNEXE A")
    return 0


def cmd_etat(args):
    entrees, anomalies = lire_registre()
    dernier = {}
    for e in entrees:
        dernier[e["artefact"]] = e
    print(f"[empreintes] registre : {len(entrees)} consignations, "
          f"{len(dernier)} artefacts, {len(anomalies)} anomalie(s) de lecture")
    for a in sorted(dernier):
        e = dernier[a]
        print(f"[empreintes]   {a} — n°{e['n']} {e['date']} sha256 "
              f"{e['sha256'][:12]}… ({e['build']})")
    return 0


def main():
    p = argparse.ArgumentParser(description="TRIADE — empreintes par build (M5-a, D134)")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("consigner", help="consigner l'empreinte d'un artefact")
    c.add_argument("--artefact", required=True, help="chemin relatif au dépôt")
    c.add_argument("--build", required=True, help="libellé du build consignant")
    c.add_argument("--stamp-file", help="fichier de stamp des sources (sha256)")
    c.add_argument("--stamp", help="valeur de stamp directe")
    v = sub.add_parser("verifier", help="contrôle automatique inter-build")
    sub.add_parser("modules", help="empreintes md5 des 15 modules vs ANNEXE A")
    sub.add_parser("etat", help="état du registre (lecture seule)")
    args = p.parse_args()
    if args.cmd == "consigner":
        sys.exit(cmd_consigner(args))
    if args.cmd == "verifier":
        sys.exit(cmd_verifier(args))
    if args.cmd == "modules":
        sys.exit(cmd_modules(args))
    sys.exit(cmd_etat(args))


if __name__ == "__main__":
    main()
