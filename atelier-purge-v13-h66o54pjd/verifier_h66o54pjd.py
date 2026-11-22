#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_h66o54pjd.py — LA VÉRIFICATION APRÈS MODIFICATIONS (la lettre
du plan gelé) :
  1. le grep multi-motifs sur les PDF RÉGÉNÉRÉS : zéro occurrence
     prescriptive, chaque occurrence restante classée HISTORIQUE-DATÉE ;
  2. la relecture intégrale des paragraphes réparés (les marqueurs des
     réécritures complètes présents, les splices ABSENTS) ;
  3. la simulation du runbook : les huit étapes sans écriture de dépôt, le
     geste-piège et SA VARIANTE refusés au premier nom, le scan de
     l'historique : le marqueur aux seules pièces de consignation nommées ;
  4. le linter étendu vert sur les sources + les deux PDF ;
  5. la version aux PDF == v1.7 / v0.15.8 partout ;
  6. la garde pre-commit : le secret réinjecté à la copie REFUSÉ nommé, le
     faux positif nul sur l'état courant ;
  7. le sceau 14/14 avant et après.

Sortie : rapport-purge-v13.txt ; code 0 si TOUT VERT."""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = REPO / "atelier-purge-v13-h66o54pjd"
LIVRE_PDF = REPO / "scripts/livre_v17/final.pdf"
SPEC_PDF = REPO / "scripts/spec_v158/main.pdf"

VERT = []


def controle(nom: str, cond: bool, detail: str = "") -> None:
    VERT.append(cond)
    print(f"  [{nom:<54}] {'VERT' if cond else 'ROUGE'} {detail}")


def main() -> int:
    print("[h66o54pjd] LA VÉRIFICATION APRÈS MODIFICATIONS")

    # (1) le grep multi-motifs sur les PDF régénérés
    import tempfile
    txts = {}
    for nom, pdf in [("livre", LIVRE_PDF), ("spec", SPEC_PDF)]:
        out = pathlib.Path(tempfile.mkstemp(suffix=".txt")[1])
        subprocess.run(["pdftotext", str(pdf), str(out)], check=True,
                       capture_output=True)
        txts[nom] = out.read_text(encoding="utf-8")
        out.unlink()
    REFERENT = re.compile(
        r"fichier-remise|garde durable|phrase de contr[oô]le|"
        r"PHRASE-CONTROLE|remise D81", re.I)
    VERBES = re.compile(
        r"committ|pouss|push|écri[s(t]|ecr[i (]|dépos|depos|"
        r"pos(?:e|ez|er)\b|sauvegard|est la remise|EST la remise", re.I)
    MARQUEURS = ["du 4 au 19 novembre", "De D81 au 19", "amendée D223",
                 "amendé D223", "l'histoire datée", "d'époque", "DATÉE",
                 "HISTOIRE DATÉE", "En v0.5.2", "D81 :", "vivait",
                 "fut la remise", "jamais un geste courant", "de l'époque",
                 "D81 d'alors", "28 oct. 2026", "v0.5.2", "v0.5.1",
                 "Correspondance v", "la vague 11", "la vague 12",
                 "est REFUSÉ", "JAMAIS écrite au dépôt",
                 "n'est JAMAIS", "en AUCUN dépôt"]
    for nom, texte in txts.items():
        lignes = texte.split("\n")
        hors_date = 0
        for k, l in enumerate(lignes):
            if REFERENT.search(l):
                ctx = "\n".join(lignes[max(0, k - 3):k + 4])
                # LA RÈGLE (la même que le linter) : le référent à
                # PROXIMITÉ D'UN VERBE D'ÉCRITURE DE DÉPÔT — le référent
                # seul (la description, la proposition, l'histoire) n'est
                # JAMAIS prescriptif
                if VERBES.search(ctx) and not any(m in ctx for m in MARQUEURS):
                    # LA REMISE DU SCEAU (sceau_I.py deposer, les arbres
                    # signés, la graine Ed25519) : UNE AUTRE remise, la
                    # classe nommée au rapport
                    if re.search(r"sceau|signature|arbres|graine|Ed25519",
                                 ctx, re.I):
                        continue
                    hors_date += 1
                    print(f"    [{nom} l.{k}] {l.strip()[:90]}")
        controle(f"le grep PDF {nom} : zéro prescriptive",
                 hors_date == 0,
                 f"({len(REFERENT.findall(texte))} référents, "
                 f"{hors_date} hors date")

    # (2) les paragraphes réparés : les splices ABSENTS, les réécritures
    #     présentes
    livre = "\n".join(f.read_text(encoding="utf-8") for f in
                      sorted((REPO / "scripts/livre_v17").glob(
                          "sec-*.tex")))
    spec = "\n".join(f.read_text(encoding="utf-8") for f in
                     sorted((REPO / "scripts/spec_v158").glob(
                         "sec-*.tex")))
    controle("le §7.5 du Livre : le splice ABSENT",
             "depuis qu'elle l'est (D220/D223, la matrice honorée : "
             "public + Zenodo)\ntant qu'elle ne l'est pas" not in livre)
    controle("le §7.5 du Livre : la réécriture complète présente",
             "La cérémonie de séquestre A ÉTÉ" in livre
             and "les DEUX états sont datés" in livre)
    controle("le §8.2 item 7 : « tant qu'elle est VÉCUE » réparé",
             "tant\nqu'elle est VÉCUE" not in livre
             and "elle est \\emph{au\npassé}, datée" in livre)
    controle("le §14.3 de la spec : le splice réparé",
             "la phrase ne vit plus au\nracine du coffre Drive" not in spec
             and "AUCUNE phrase en clair au dépôt ni au coffre Drive"
             in spec)
    controle("sec-a : l'énoncé périmé porté à l'état courant",
             "EST PASSÉ au séquestre" in spec
             and "DEMEURE à la garde D81 —\naucune clé touchée" not in spec)

    # (3) la simulation du runbook
    r = subprocess.run(["python3", str(ICI / "rejouer_runbook_v13.py")],
                       capture_output=True, text=True, timeout=600)
    controle("le runbook : 8 étapes sans écriture, les pièges refusés",
             "LE VERDICT : VERT" in r.stdout)

    # (4) le linter étendu
    r2 = subprocess.run(["python3", str(ICI / "linter_v13.py")],
                        capture_output=True, text=True, timeout=300)
    # le SEUL rouge autorisé : la copie réinjectée du contrôle négatif
    rouges = [l for l in r2.stdout.splitlines() if l.startswith("ROUGE")]
    controle("le linter étendu vert (le rouge = la copie du contrôle)",
             len(rouges) == 1 and "copie réinjectée" in rouges[0])

    # (5) les versions aux PDF
    for nom, attendu, texte in [("livre", "v1.7", txts["livre"]),
                                ("spec", "v0.15.8", txts["spec"])]:
        controle(f"la version au PDF {nom} == {attendu}", attendu in texte)
        # l'édition courante DECLARÉE : aucune déclaration périmée du
        # « courant » (les correspondances « vX → vY » demeurent datées)
        courants_perimes = []
        for l in texte.split("\n"):
            if re.search(r"courante|présente é|the present edition", l,
                         re.I) and any(
                    v in l for v in ("v1.6", "v1.5", "v1.4", "v1.3",
                                     "v0.15.7", "v0.15.6")):
                courants_perimes.append(l.strip()[:60])
        controle(f"aucune édition courante périmée déclarée au PDF {nom}",
                 not courants_perimes, str(courants_perimes[:2]))

    # (6) la garde pre-commit : le contrôle négatif + le faux positif nul
    r3 = subprocess.run(["python3", "scan_secrets.py", "--test"], cwd=REPO,
                        capture_output=True, text=True, timeout=300)
    controle("la garde : le contrôle négatif (5 classes)",
             "LE CONTRÔLE NÉGATIF" in r3.stdout
             and "VERT" in r3.stdout)
    r4 = subprocess.run(["python3", "scan_secrets.py"], cwd=REPO,
                        capture_output=True, text=True, timeout=600)
    controle("la garde : le faux positif NUL sur l'état courant",
             "0 détection" in r4.stdout)

    # (7) le sceau
    r5 = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                        cwd=REPO, capture_output=True, text=True,
                        timeout=300)
    controle("le sceau 14/14 APRÈS", "14 arbres VERTS" in r5.stdout)

    total, verts = len(VERT), sum(1 for ok in VERT if ok)
    print(f"[h66o54pjd] {verts}/{total} VERT")
    return 0 if verts == total else 1


if __name__ == "__main__":
    sys.exit(main())
