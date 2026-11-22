#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""triage_rapports.py — LE PIPELINE DE TRIAGE DES RAPPORTS ADOPTEURS et le
DIGEST PAR RELEASE (e1lr9i8ts, la vague 15).
LES TROIS ÉTAGES :
  1. LA VALIDATION À L'ENTRÉE fail-closed : le schéma (par version — les
     rapports de versions DIFFÉRENTES ne sont JAMAIS poolés sans note de
     périmètre), le scan de secrets (les motifs de triade_feedback), la
     signature si présente (vérifiée, jamais exigée) ;
  2. LE CLUSTERING MÉCANIQUE : les classes de refus, les défauts F/L, la
     doc_confusion, la frontière de capacité PAR FAMILLE — les rapports
     malformés REFUSÉS au premier jet ;
  3. LE TRIAGE PROPOSE des décisions (Dxxx) — L'ARBITRAGE APPARTIENT AU
     DÉVELOPPEUR, le journal est append-only, AUCUNE amendment automatique
     du protocole.
LE DIGEST PAR RELEASE : généré mécaniquement — RECOMPUTABLE depuis les
rapports bruts (zéro divergence exigée), ZÉRO secret (le scan + le
contrôle négatif), les contributeurs acknowledged opt-in (CC-BY-4.0). Le
dépôt Zenodo du digest DEMEURE le geste du développeur.

Usage :
  triage_rapports.py valider <rapport.json>...
  triage_rapports.py trier <dossier_rapports/>
  triage_rapports.py digest <dossier_rapports/> --version v0.23.2 --sortie digest.json
  triage_rapports.py recomputer <dossier_rapports/> --digest digest.json
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

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


def scan_secrets(texte: str) -> list:
    trouves = []
    if MARQUEUR_PHRASE_TEST in texte:
        trouves.append(("phrase_test_marquee", ""))
    for nom, motif in MOTIFS_SECRETS:
        m = motif.search(texte)
        if m:
            trouves.append((nom, m.group(0)[:40]))
    return trouves


def valider_rapport(rapport: dict) -> tuple:
    erreurs = []
    if not isinstance(rapport, dict):
        return ["le rapport n'est pas un objet JSON"], "inconnue"
    version = rapport.get("schema", "inconnue")
    if version not in ("TRIADE-FEEDBACK-v1",):
        erreurs.append("schéma non supporté : " + str(version) +
                       " (le refus nommé, JAMAIS un pool silencieux "
                       "inter-schéma)")
    for champ in ("kit", "agent", "env", "capability", "measured", "consent"):
        if champ not in rapport:
            erreurs.append("champ requis manquant : " + champ)
    if "agent" in rapport and "family" not in rapport.get("agent", {}):
        erreurs.append("champ requis manquant : agent.family")
    if "measured" in rapport:
        m = rapport["measured"]
        for c in ("operations", "refus_par_classe", "tokens_natifs", "wall"):
            if c not in m:
                erreurs.append("champ requis manquant : measured." + c)
    texte = json.dumps(rapport, ensure_ascii=False)
    for nom, extrait in scan_secrets(texte):
        erreurs.append("secret détecté [" + nom + "] — le rapport REFUSÉ")
    if "signature_adopteur" in rapport:
        sig = rapport["signature_adopteur"]
        if not re.fullmatch(r"[0-9a-f]{16,}", sig):
            erreurs.append("signature_adopteur présente mais mal formée")
    return erreurs, version


def trier_dossier(dossier: pathlib.Path) -> dict:
    par_version = collections.defaultdict(
        lambda: {"rapports": [], "refus_valide": []})
    for f in sorted(dossier.glob("*.json")):
        if f.name.startswith("digest"):
            continue  # le digest N'EST PAS un rapport (nommé au rapport)
        try:
            rapport = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            par_version["inconnue"]["refus_valide"].append(
                {"fichier": f.name, "erreurs": ["malformé : " + str(e)]})
            continue
        erreurs, version = valider_rapport(rapport)
        if erreurs:
            par_version[version]["refus_valide"].append(
                {"fichier": f.name, "erreurs": erreurs})
            continue
        par_version[version]["rapports"].append(rapport)

    clusters = {}
    for version, groupe in par_version.items():
        if not groupe["rapports"] and not groupe["refus_valide"]:
            continue
        refus = collections.Counter()
        defauts = collections.Counter()
        doc_confusion = 0
        frontiere = {}
        for r in groupe["rapports"]:
            famille = r["agent"]["family"]
            for classe, n in r["measured"]["refus_par_classe"].items():
                refus[classe] += n
            for d in r["measured"].get("defauts_fl", []):
                defauts[d["classe"] + "@" + d["locus"]] += 1
            com = r.get("commentary", "").lower()
            if any(m in com for m in ("doc_confusion", "documentation",
                                      "le manuel dit", "the manual says")):
                doc_confusion += 1
            frontiere.setdefault(famille, []).append({
                "constantes_128": r["capability"]["constantes_128"],
                "operations": r["measured"]["operations"],
                "tokens_natifs": r["measured"]["tokens_natifs"]})
        clusters[version] = {
            "n_rapports": len(groupe["rapports"]),
            "refus_par_classe": dict(refus.most_common()),
            "defauts_fl": dict(defauts.most_common()),
            "doc_confusion": doc_confusion,
            "frontiere_par_famille": {
                f: {"n": len(v),
                    "constantes_128": [x["constantes_128"] for x in v],
                    "tokens_median": sorted(
                        x["tokens_natifs"] for x in v)[len(v) // 2]}
                for f, v in frontiere.items()},
            "refus_validation": groupe["refus_valide"],
        }
    return clusters


def proposer_decisions(clusters: dict) -> list:
    propositions = []
    for version, c in clusters.items():
        for classe, n in c["refus_par_classe"].items():
            if n >= 5:
                propositions.append({
                    "decision_proposee": "D<prochain> — grammaire/gabarit",
                    "objet": "la classe de refus « " + classe + " » vue " +
                             str(n) + " fois (" + version + ")",
                    "arbitrage": "AU DÉVELOPPEUR (jamais auto-appliqué)"})
        for defaut, n in c["defauts_fl"].items():
            if n >= 3:
                propositions.append({
                    "decision_proposee": "D<prochain> — nouvelle classe X + "
                                         "vecteur de falsification",
                    "objet": "le défaut F/L « " + defaut + " » vu " +
                             str(n) + " fois (" + version + ")",
                    "arbitrage": "AU DÉVELOPPEUR"})
        if c["doc_confusion"] >= 2:
            propositions.append({
                "decision_proposee": "D<prochain> — révision doc",
                "objet": "la doc_confusion vue " + str(c["doc_confusion"]) +
                         " fois (" + version + ")",
                "arbitrage": "AU DÉVELOPPEUR"})
        for famille, fr in c["frontiere_par_famille"].items():
            if any(("refus" in str(x).lower()) or
                   ("echec" in str(x).lower())
                   for x in fr["constantes_128"]):
                propositions.append({
                    "decision_proposee": "D<prochain> — frontière de "
                                         "capacité",
                    "objet": "la famille « " + famille + " » échoue la "
                             "dérivation des 128 : la frontière NOMMÉE "
                             "(le conseil fail-closed, jamais le "
                             "gatekeeping)",
                    "arbitrage": "AU DÉVELOPPEUR"})
    return propositions


def generer_digest(dossier: pathlib.Path, version_kit: str) -> dict:
    clusters = trier_dossier(dossier)
    digest = {
        "digest": "digest-" + version_kit,
        "version_kit": version_kit,
        "par_schema": clusters,
        "comptes": {v: c["n_rapports"] for v, c in clusters.items()},
        "zero_secret": True,
        "contributeurs": [],
    }
    for f in sorted(dossier.glob("*.json")):
        if f.name.startswith("digest"):
            continue
        try:
            r = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if r.get("consent", {}).get("licence") == "CC-BY-4.0":
            digest["contributeurs"].append(
                r["consent"].get("public_digest", "")[:16] + "…")
    texte = json.dumps(digest, ensure_ascii=False)
    if scan_secrets(texte):
        digest["zero_secret"] = False
    return digest


def recomputer(dossier: pathlib.Path, digest: dict) -> bool:
    regen = generer_digest(dossier, digest.get("version_kit", "?"))
    return json.dumps(regen, sort_keys=True) == json.dumps(digest,
                                                           sort_keys=True)


def main() -> int:
    p = argparse.ArgumentParser(prog="triade triage")
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("valider")
    v.add_argument("rapports", nargs="+")
    t = sub.add_parser("trier")
    t.add_argument("dossier")
    d = sub.add_parser("digest")
    d.add_argument("dossier")
    d.add_argument("--version", required=True)
    d.add_argument("--sortie", required=True)
    rc = sub.add_parser("recomputer")
    rc.add_argument("dossier")
    rc.add_argument("--digest", required=True)
    args = p.parse_args()

    if args.cmd == "valider":
        code = 0
        for rf in args.rapports:
            try:
                rapport = json.loads(pathlib.Path(rf).read_text(
                    encoding="utf-8"))
            except Exception as e:
                print(rf + " : REFUS — malformé (" + str(e) + ")")
                code = 2
                continue
            erreurs, version = valider_rapport(rapport)
            if erreurs:
                print(rf + " [" + version + "] : REFUS — " +
                      " ; ".join(erreurs))
                code = 2
            else:
                print(rf + " [" + version + "] : VERT")
        return code
    if args.cmd == "trier":
        clusters = trier_dossier(pathlib.Path(args.dossier))
        propositions = proposer_decisions(clusters)
        print(json.dumps({"clustering": clusters,
                          "propositions": propositions}, indent=2,
                         ensure_ascii=False))
        return 0
    if args.cmd == "digest":
        digest = generer_digest(pathlib.Path(args.dossier), args.version)
        pathlib.Path(args.sortie).write_text(
            json.dumps(digest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print("OK — " + args.sortie + " (" + str(digest["comptes"]) +
              ", zero_secret=" +
              ("VERT" if digest["zero_secret"] else "ROUGE") +
              ") — le dépôt Zenodo DEMEURE le geste du développeur")
        return 0 if digest["zero_secret"] else 2
    if args.cmd == "recomputer":
        digest = json.loads(pathlib.Path(args.digest).read_text(
            encoding="utf-8"))
        ok = recomputer(pathlib.Path(args.dossier), digest)
        print("VERT — zéro divergence (le digest recomputable)" if ok else
              "ROUGE — divergence au rejeu")
        return 0 if ok else 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
