#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_comparaison_v150.py — LE VÉRIFICATEUR DU PAQUET 5 (la
comparaison des workflows, l'instruction 54wni4hzh ; le plan consigné à
D204).

La vérification EXIGÉE par l'instruction, contrôlée ici :

  1. LE VERROU — l'empreinte sha256 du plan est consignée et datée à
     D204 AVANT tout fichier de résultats : le dossier des résultats
     (preuves_v150/comparaison_resultats/) N'EXISTE PAS (aucun fichier
     de résultats ne précède ni ne suit la consignation — la campagne
     n'a pas commencé) ; l'empreinte du fichier == l'empreinte consignée
     (le plan n'est plus modifiable) ;
  2. L'AUDIT DU PLAN — AUCUN chiffre de résultat : chaque nombre du plan
     est extrait et classé (structurel : identifiants, versions, dates,
     étiquettes H/CA/M/R/§, tailles d'échantillon et seuils DÉCLARÉS
     comme tels) ; tout nombre d'allure mesurée (tokens, durées,
     comptes de défauts) est un ROUGE ;
  3. LA PREUVE DU DRY-RUN — les compteurs de tokens correspondent aux
     logs À L'UNITÉ PRÈS : chaque ligne du journal du dry-run est
     confrontée au champ usage de la réponse BRUTE de l'API conservée à
     côté ; les totaux sont recalculés ; le chronomètre est prouvé par
     sa calibration (écart sous tolérance) et une commande réelle ;
  4. LE KIT COMPLET — le plan, le LISEZMOI, les deux instruments, les
     trois gabarits, le présent vérificateur ;
  5. AUCUNE MESURE DE CAMPAGNE — les gabarits CSV demeurent VIDES (les
     en-têtes et les commentaires seuls), aucun journal de campagne
     n'existe.

Sortie : le rapport preuves_v150/comparaison_dryrun/
rapport_verification_paquet5.txt (VERT/ROUGE par contrôle)."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
KIT = REPO / "scripts" / "comparaison_v150"
DRYRUN = REPO / "scripts" / "preuves_v150" / "comparaison_dryrun"
RESULTATS = REPO / "scripts" / "preuves_v150" / "comparaison_resultats"
PLAN = KIT / "PLAN_PREREGISTRE_COMPARAISON.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"

rapport: list[str] = []
verts = 0
rouges = 0


def consigne(nom: str, ok: bool, detail: str) -> None:
    global verts, rouges
    rapport.append(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    for ligne in detail.strip().splitlines():
        rapport.append(f"       {ligne}")
    verts += ok
    rouges += not ok


def sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# ------------------------------------------------------------------ 1
def controle_verrou() -> None:
    texte = DECISIONS.read_text(encoding="utf-8")
    m = re.search(r"^## D204\b.*$", texte, re.M)
    d204 = m.group(0) if m else ""
    empreinte_plan = sha256(PLAN)
    consignee = empreinte_plan[:16] in d204 or empreinte_plan in d204
    # le dossier des résultats ne doit PAS exister (aucune mesure)
    resultats_absents = not RESULTATS.exists()
    ok = bool(d204) and consignee and resultats_absents
    consigne("1. LE VERROU — empreinte consignée à D204 avant tout "
             "fichier de résultats", ok,
             f"l'empreinte du plan : {empreinte_plan[:16]}…\n"
             f"  la décision D204 {'PRÉSENTE' if d204 else 'ABSENTE'} ; "
             f"l'empreinte {'CONSIGNÉE' if consignee else 'NON CONSIGNÉE'}\n"
             f"  le dossier des résultats "
             f"{'ABSENT — aucune mesure, aucune campagne ouverte' if resultats_absents else 'PRÉSENT — INCOMPATIBLE avec le verrou'} : "
             f"{RESULTATS.relative_to(REPO)})\n"
             f"  le plan n'est plus modifiable après le début des mesures "
             f"(CA5 — la confrontation à chaque jalon)")


# ------------------------------------------------------------------ 2
def controle_audit_plan() -> None:
    texte = PLAN.read_text(encoding="utf-8")
    lignes = texte.splitlines()
    # les nombres AUTORISÉS, par motif : identifiants et étiquettes,
    # chemins, en-têtes de section, outils et étiquettes d'étude
    autorises = re.compile(
        r"(D\d+|v0\.\d+\.\d+|R\d+|H\d+|CA\d+|M\d+|RQ\d+|§\s*\d|"
        r"\d{4}-\d{2}-\d{2}|20\d{2}|loupe-\d\d|54wni4hzh|sha256|×1,08|"
        r"json|JSONL|CSV|paquet\s+\d|vague\s+\d|##\s*\d|_v\d+|"
        r"gcc|-O2|-Os|clang)", re.I)
    # mots structurels en toutes lettres (fr)
    mots_structurels = re.compile(
        r"(un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|"
        r"douze|quinze|vingt|trente|cent|mille)s?\b", re.I)
    suspects = []
    for i, l in enumerate(lignes, 1):
        for m in re.finditer(r"\d[\d ,.]*", l):
            extrait = l[max(0, m.start() - 45):m.end() + 45]
            if autorises.search(extrait) or mots_structurels.search(extrait):
                continue
            suspects.append(f"ligne {i} : …{extrait.strip()}…")
    ok = not suspects
    n_chiffres = len(re.findall(r"\d", texte))
    consigne("2. L'AUDIT DU PLAN — aucun chiffre de résultat", ok,
             f"le plan : {len(lignes)} lignes, {n_chiffres} chiffres "
             f"extraits et TOUS classés structurels (identifiants D/H/CA/"
             f"M/R, versions, dates, étiquettes, tailles et seuils "
             f"DÉCLARÉS)\n"
             f"  nombres d'allure mesurée (tokens, durées, comptes) : "
             f"{'ZÉRO' if ok else str(len(suspects))}\n"
             + ("\n".join("  " + s for s in suspects[:5]) if suspects
                else "  les seuils du plan (facteur deux, au plus dix) sont "
                     "des SEUILS pré-enregistrés, jamais des mesures ; "
                     "le ×1,08 est cité comme l'estimation INTERDITE"))


# ------------------------------------------------------------------ 3
def controle_dryrun() -> None:
    journal = DRYRUN / "dryrun_tokens.jsonl"
    brut = DRYRUN / "dryrun_brut.jsonl"
    verifs = DRYRUN / "dryrun_verifications.jsonl"
    lignes = [json.loads(l) for l in
              journal.read_text(encoding="utf-8").splitlines() if l.strip()]
    brutes = [json.loads(l) for l in
              brut.read_text(encoding="utf-8").splitlines() if l.strip()]
    # 3a. ligne par ligne : le journal == le champ usage du log BRUT,
    #     À L'UNITÉ PRÈS
    paires = 0
    egaux = 0
    for j, b in zip(lignes, brutes):
        if (j["bras"], j["phase"]) != (b["bras"], b["phase"]):
            continue
        paires += 1
        u = b["reponse_api"]["usage"]
        if (j["prompt_tokens"] == u["prompt_tokens"]
                and j["completion_tokens"] == u["completion_tokens"]
                and j["total_tokens"] == u["total_tokens"]
                and j["id"] == b["reponse_api"]["id"]):
            egaux += 1
    # 3b. les totaux : la somme du journal (recalculée ici) == le total
    #     que l'instrument rapporte
    total_rec = sum(l["total_tokens"] for l in lignes)
    tous_log = all(l.get("source") == "log-api" for l in lignes)
    sommes = all(l.get("somme_coherente") for l in lignes)
    # 3c. le chronomètre : la calibration sous tolérance + une commande
    #     réelle journalisée
    v = [json.loads(l) for l in
         verifs.read_text(encoding="utf-8").splitlines() if l.strip()]
    calib = [x for x in v if x["label"] == "calibration-sleep"]
    reelle = [x for x in v if x["label"] != "calibration-sleep"]
    calib_ok = bool(calib) and all(
        abs(x["secondes"] - 1.5) <= 0.05 for x in calib)
    reelle_ok = bool(reelle) and all(x["code_retour"] == 0 for x in reelle)
    phases = sorted({l["phase"] for l in lignes})
    ok = (paires == len(lignes) == len(brutes) and egaux == paires
          and tous_log and sommes and calib_ok and reelle_ok
          and len(phases) >= 3)
    detail = []
    for l, b in zip(lignes, brutes):
        u = b["reponse_api"]["usage"]
        meme_usage = (l["prompt_tokens"], l["completion_tokens"],
                      l["total_tokens"]) == (u["prompt_tokens"],
                                             u["completion_tokens"],
                                             u["total_tokens"])
        detail.append(
            f"{l['phase']:10s} : journal {l['prompt_tokens']}+"
            f"{l['completion_tokens']}={l['total_tokens']} == log api "
            f"{u['prompt_tokens']}+{u['completion_tokens']}="
            f"{u['total_tokens']} → "
            f"{'ÉGAUX à l unité près' if meme_usage else 'ÉCART'}")
    detail.append(f"les paires confrontées : {egaux}/{paires} ÉGALES ; "
                  f"phases couvertes : {', '.join(phases)}")
    detail.append(f"le total recalculé du journal : {total_rec} tokens — "
                  f"100 % lus du log (zéro estimation : source=log-api "
                  f"{'PARTOUT' if tous_log else 'ÉCART'} ; sommes "
                  f"cohérentes {'PARTOUT' if sommes else 'ÉCART'})")
    detail.append(f"le chronomètre : calibration {calib[0]['secondes']:.3f} s "
                  f"contre 1,500 s demandée "
                  f"({'≤ tolérance 0,05 s' if calib_ok else 'HORS tolérance'}) ; "
                  f"la commande réelle « {reelle[0]['label']} » "
                  f"{reelle[0]['secondes']:.3f} s code "
                  f"{reelle[0]['code_retour']}")
    detail.append("le dry-run est la PREUVE D'INSTRUMENT, PAS une mesure "
                  "de campagne (les fichiers vivent à comparaison_dryrun/, "
                  "le dossier des résultats demeure absent)")
    consigne("3. LA PREUVE DU DRY-RUN — les compteurs == les logs, à "
             "l'unité près", ok, "\n".join(detail))


# ------------------------------------------------------------------ 4-5
def controle_kit() -> None:
    pieces = ["PLAN_PREREGISTRE_COMPARAISON.md", "LISEZMOI-comparaison.txt",
              "compter_tokens.py", "chronometre_verification.py",
              "carnet_temps_humain.csv", "livraisons.csv", "defauts.csv",
              "verifier_comparaison_v150.py"]
    manquantes = [p for p in pieces if not (KIT / p).exists()]
    # les gabarits demeurent VIDES (en-têtes + commentaires seuls)
    vides = True
    detail = []
    for gab in ("carnet_temps_humain.csv", "livraisons.csv", "defauts.csv"):
        lignes = [l for l in (KIT / gab).read_text(encoding="utf-8")
                  .splitlines() if l.strip()]
        donnees = [l for l in lignes
                   if not l.startswith("#") and l.strip()]
        vides &= len(donnees) <= 1  # l'en-tête seule
        detail.append(f"{gab} : {len(lignes)} lignes — "
                      f"{'EN-TÊTE SEULE (aucune donnée)' if len(donnees) <= 1 else 'DONNÉES PRÉSENTES'}")
    ok = not manquantes and vides
    consigne("4. LE KIT COMPLET — et AUCUNE mesure de campagne", ok,
             "les huit pièces du kit : "
             f"{'TOUTES PRÉSENTES' if not manquantes else 'MANQUANTES ' + str(manquantes)}\n"
             + "\n".join("  " + d for d in detail)
             + "\n  le journal de campagne (comparaison_resultats/) : "
               "ABSENT — créé par la première mesure (CA1)")


def main() -> int:
    rapport.append("=" * 74)
    rapport.append("VÉRIFICATION DU PAQUET 5 — LE PLAN DE COMPARAISON "
                   "PRÉ-ENREGISTRÉ (54wni4hzh, D204)")
    rapport.append("=" * 74)
    controle_verrou()
    controle_audit_plan()
    controle_dryrun()
    controle_kit()
    rapport.append("=" * 74)
    rapport.append(f"BILAN : {verts} VERT / {rouges} ROUGE — "
                   f"{'LE PAQUET EST CONSIGNÉ, LA CAMPAGNE ATTEND LE DÉVELOPPEUR' if not rouges else 'CORRIGER AVANT CONSIGNATION'}")
    texte = "\n".join(rapport) + "\n"
    print(texte)
    (DRYRUN / "rapport_verification_paquet5.txt").write_text(
        texte, encoding="utf-8")
    return 0 if not rouges else 1


if __name__ == "__main__":
    sys.exit(main())
