#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_purge.py — LA VÉRIFICATION SÉMANTIQUE DE LA PURGE (0uug27teo).

(1) LE GREP SÉMANTIQUE ÉLARGI sur les deux pièces régénérées : les motifs
    « fichier-remise », « remise D81 », « le fichier est la remise », et
    « phrase de contrôle » À PROXIMITÉ d'un verbe d'écriture de dépôt
    (commit/push/écrire/déposer/poser/sauvegarder) OU d'un impératif
    prescriptif (posez, commitez, vérifiez le fichier) — toute occurrence
    PRESCRIPTIVE = ROUGE ; chaque occurrence restante doit être classée
    HISTORIQUE-DATÉE à la table nommée.
(2) LE CONTRÔLE NÉGATIF PLANTÉ : une phrase prescriptive synthétique
    (« posez la phrase courante dans le fichier-remise, commit, push »)
    réintroduite dans une COPIE du texte — REFUSÉE au premier nom.
Sortie : rapport-verification-purge.txt"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = REPO / "atelier-purge-0uug27teo"
LIVRE = REPO / "scripts" / "livre_v16" / "final.pdf"
SPEC = REPO / "scripts" / "spec_v157" / "main.pdf"

MOTIFS = re.compile(
    r"fichier-remise|remise D81|le fichier AVANT tout|PHRASE-CONTROLE", re.I)
# « le fichier est la remise » ne vit qu'au contexte PHRASE (la remise de la
# clé I — generer/signer, D87 — est une remise AUTRE, admissible au nom)
MOTIF_REMISE_PHRASE = re.compile(
    r"le fichier est la remise", re.I)
VERBES = re.compile(
    r"committ|pouss|push|écri[s(t]|ecr[i (]|dépos|depos|"
    r"pos(?:e|ez|er)\b|sauvegard|vit sur", re.I)
# LA TABLE NOMMÉE des contextes historiques datés admis (par pièce) :
ADMIS = {
    "livre": ["De D81 au 19 novembre 2026", "le fichier fut la remise",
              "l'histoire datée", "d'époque", "amendée D223",
              "amendé D223", "AMENDÉE", "l'épisode fondateur"],
    "specification": ["En v0.5.2", "En v0.5.1", "d'époque",
                      "amendée D223", "amendé D223", "D81 ;"],
}


def extraire(chemin: pathlib.Path) -> str:
    txt = subprocess.run(["pdftotext", str(chemin), "-"],
                         capture_output=True, check=True).stdout.decode(
                             "utf-8", "replace")
    txt = txt.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", txt)


def main() -> int:
    rapport = [
        "LA VÉRIFICATION SÉMANTIQUE DE LA PURGE D81 (0uug27teo)",
        "le grep sémantique élargi sur les deux pièces régénérées —",
        "les motifs : fichier-remise · remise D81 · le fichier est la",
        "remise · le fichier AVANT tout · PHRASE-CONTROLE ; la proximité",
        "d'un verbe d'écriture de dépôt OU d'un impératif prescriptif",
        "",
    ]
    total_prescriptif = 0
    classes: list[tuple[str, str, str]] = []
    for nom, chemin in (("livre", LIVRE), ("specification", SPEC)):
        t = extraire(chemin)
        occurrences = list(MOTIFS.finditer(t))
        occurrences += [m for m in MOTIF_REMISE_PHRASE.finditer(t)
                        if re.search(r"phrase|contr[oô]le|coffre",
                                     t[max(0, m.start() - 260):m.end() + 260],
                                     re.I)]
        for m in occurrences:
            ctx = t[max(0, m.start() - 180):m.end() + 180]
            prescriptif = bool(VERBES.search(ctx)) and not any(
                a in ctx for a in ADMIS[nom])
            classification = ("PRESCRIPTIF" if prescriptif
                              else "HISTORIQUE-DATÉE")
            classes.append((nom, classification, m.group(0) + " … " +
                            ctx.strip()[:70]))
            if prescriptif:
                total_prescriptif += 1
    # le classement complet à la table nommée
    rapport.append("LA TABLE NOMMÉE DES OCCURRENCES (le classement complet) :")
    for piece, classe, ctx in classes:
        rapport.append(f"  [{piece}] {classe} : « {ctx} »")
    rapport += ["", f"LE VERDICT DU GREP : {total_prescriptif} occurrence(s) "
                "PRESCRIPTIVE(S) — " +
                ("ROUGE" if total_prescriptif else "ZÉRO (la purge exacte au "
                 "périmètre sémantique)")]

    # ---- (2) LE CONTRÔLE NÉGATIF PLANTÉ --------------------------------
    t = extraire(LIVRE)
    copie = t.replace(
        "Le séquestre 5/3 est à jour",
        "posez la phrase courante dans le fichier-remise, commit, push — puis "
        "rejouez. Le séquestre 5/3 est à jour", 1)
    negatifs = 0
    for m in MOTIFS.finditer(copie):
        ctx = copie[max(0, m.start() - 180):m.end() + 180]
        if VERBES.search(ctx) and not any(a in ctx for a in ADMIS["livre"]):
            if "posez la phrase courante" in ctx:
                negatifs += 1
                rapport += [
                    "",
                    "LE CONTRÔLE NÉGATIF VÉCU : la phrase prescriptive "
                    "synthétique réintroduite à la copie —",
                    f"  « {m.group(0)} » à proximité du verbe prescriptif : "
                    "REFUSÉE AU PREMIER NOM (le motif vivant du linter)"]
    if negatifs == 0:
        rapport.append("LE CONTRÔLE NÉGATIF : NON ATTRAPÉ — ROUGE")
        total_prescriptif += 1
    else:
        rapport.append(f"LE CONTRÔLE NÉGATIF : REFUSÉ au premier nom "
                       f"({negatifs} occurrence(s) attrapée(s)) — VERT")

    verdict = "ROUGE" if total_prescriptif else "VERT"
    rapport += ["", f"LE VERDICT FINAL : {verdict}"]
    (ICI / "rapport-verification-purge.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    return 0 if verdict == "VERT" else 2


if __name__ == "__main__":
    sys.exit(main())
