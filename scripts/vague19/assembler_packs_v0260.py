#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASSEMBLAGE DES PACKS v0.26.0 (vague 19) : soumission, présentation, complet,
participation v1.1.0, plus le kit développeur v1.3.0 déjà construit.

Patron : les packs v0.25.0 (depot-zenodo-v0250) — mêmes rôles, contenus de la vague 19.
Aucun contenu réécrit : les pièces du pack-v260 sont copiées telles quelles.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import zipfile

R = pathlib.Path(__file__).resolve().parents[2]
PACK = R / "pack-v260"
OUT = R / "depot-zenodo-v0260"
EDITION = "v0.26.0"

SOUMISSION_README = """TRIADE — la soumission de l'édition v0.26.0 (vague 19, 24 novembre 2026)
========================================================================
Le manuscrit v0.26.0 porte la vague 19 : la PORTE DE GÉNÉRATION exécute le linter
d'édition et six classes fail-closed (table des versions, plage des décisions, ordre du
changelog, numérotation, recompte des bancs, qualification sémantique des menaces), les
six résidus constatés sont soldés, et la chaîne de décisions D261–D267 entre au journal
et à la spécification (liste blanche du prescriptif, compteur NV, expansion structurée,
ancrage de transparence). Le banc de bascule se décompose : 7 cas de transaction + 1
rendez-vous nominal + 5 aléas D261 + 3 invariants = 16/16, recompté depuis le kit.
Aucune valeur mesurée n'a changé ; les cinq pièces v0.25.0 sont intactes (5/5 sha256).
"""


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def zipdir(nom, racine, entrees):
    """écrit OUT/nom en incluant chaque chemin (relatif à racine) tel quel."""
    chemin = OUT / nom
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for e in entrees:
            p = R / e
            if not p.exists():
                print(f"  [absent] {e}")
                continue
            if p.is_dir():
                for f in sorted(p.rglob("*")):
                    if f.is_file() and ".git" not in f.parts and "__pycache__" not in f.parts:
                        z.write(f, str(f.relative_to(racine)))
            else:
                z.write(p, str(p.relative_to(racine)))
    return chemin


def soumission():
    tmp = OUT / "soumission-src"
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "README.txt").write_text(SOUMISSION_README, encoding="utf-8")
    for f in (PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf",
              PACK / f"empreintes_livrables_{EDITION}.txt",
              PACK / f"rapport_verification_{EDITION}.txt"):
        shutil.copy2(f, tmp / f.name)
    tbl = PACK / "tables_generees.txt"
    if not tbl.exists():
        tbl.write_text("Tables engendrées : voir replication-v17/TABLEAU-DESCENDANT.md "
                       "(provenance à diff nul, D260).\n", encoding="utf-8")
    shutil.copy2(tbl, tmp / tbl.name)
    return zipdir(f"TRIADE_soumission_{EDITION}.zip", R, [str(p.relative_to(R)) for p in sorted(tmp.iterdir())])


def presentation():
    return zipdir(f"TRIADE_presentation_{EDITION}.zip", R, [str(PACK.relative_to(R))])


TOP = ["ARCHIVE", "docs", "pack-v240", "pack-v260", "edition-v0230", "replication-v17",
       "scripts", "vague15", "vague16", "vague17", "vague18", "ateliers-v1234",
       "ateliers-vague15", "ateliers-vague16", "ateliers-vague17", "ateliers-vague18",
       "ateliers-vague19", "plans-vague18", "plans-vague19", "instructions_vague17_20261124",
       "atelier-coherence-vxf37231r", "atelier-w19-dec", "atelier-w19-metal",
       "atelier-w19-oracle", "atelier-w19-add",
       "EMPREINTES-PLANS-VAGUE19.txt", "OU-TROUVER-LES-LIVRABLES.md", "REPRISE_PROJET.md",
       "SOURCES-PRESCRIPTIVES.txt", "worklog.md", "PROTOCOLE_TRIADE_AGENT.md",
       "atelier-w19-dec.rapport.txt", "atelier-w19-lint.rapport.txt",
       "atelier-w19-metal.rapport.txt", "atelier-w19-oracle.rapport.txt",
       "atelier-w19-add.rapport.txt", "TRIADE_kit_developpement_v1.3.0.zip"]


def complet():
    """Le complet = chaque entrée du pack v0.25.0 SERVIE depuis l'arbre courant quand le
    chemin y vit, sinon reprise TELLE QUELLE du pack v0.25.0 (les ateliers d'ère), plus
    les ajouts de la vague 19."""
    OUT.mkdir(exist_ok=True)
    (R / "ateliers-vague19").mkdir(exist_ok=True)
    for f in R.glob("atelier-w19-*.rapport.txt"):
        shutil.copy2(f, R / "ateliers-vague19" / f.name)
    (R / "plans-vague19").mkdir(exist_ok=True)
    for f in R.glob("PLAN-W19*.md"):
        shutil.copy2(f, R / "plans-vague19" / f.name)
    base = R / "depot-zenodo-v0250" / "TRIADE_complet_v0.25.0.zip"
    chemin = OUT / f"TRIADE_complet_{EDITION}.zip"
    repris = 0
    with zipfile.ZipFile(base) as src, zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for info in src.infolist():
            if info.filename.endswith("/"):
                continue
            courant = R / info.filename
            if courant.is_file():
                z.write(courant, info.filename)
            else:
                z.writestr(info, src.read(info.filename))
                repris += 1
        ajouts = []
        for d in ("pack-v260", "atelier-w19-dec", "atelier-w19-metal", "atelier-w19-oracle",
                  "atelier-w19-add", "scripts/vague19", "ateliers-vague19", "plans-vague19"):
            for f in (R / d).rglob("*"):
                if f.is_file() and "__pycache__" not in f.parts:
                    ajouts.append(f)
        for f in list(R.glob("atelier-w19-*.rapport.txt")) + [
                R / "TRIADE_kit_developpement_v1.3.0.zip", R / "EMPREINTES-PLANS-VAGUE19.txt"]:
            if f.exists():
                ajouts.append(f)
        for f in sorted(set(ajouts)):
            z.write(f, str(f.relative_to(R)))
    print(f"  [complet] {chemin.name} — {len(ajouts)} ajouts, {repris} entrées reprises du v0.25.0")
    return chemin


PART_README = """# Participer à TRIADE — pack v1.1.0

Le pack réunit ce qu'il faut pour **évaluer** le protocole et y **contribuer** : le
complet (dépôt et ateliers), la présentation (les cinq pièces), le kit développeur et le
pack d'entraînement. Les DOI stables sont dans `INDEX-DOI.md` ; les six commandes
d'évaluation dans `EVALUATION.md` ; la checklist de contribution dans `CONTRIBUTING.md`.
"""


def participation(kit_zip, train_zip, soum, pres, comp):
    d = R / "participation-v11"
    if d.exists():
        shutil.rmtree(d)
    (d / "kits").mkdir(parents=True)
    (d / "CONTRIBUTING.md").write_text(
        (R / "participation-v1" / "CONTRIBUTING.md").read_text(encoding="utf-8"), encoding="utf-8")
    (d / "EVALUATION.md").write_text(
        (R / "participation-v1" / "EVALUATION.md").read_text(encoding="utf-8"), encoding="utf-8")
    (d / "INDEX-DOI.md").write_text(
        (R / "participation-v1" / "INDEX-DOI.md").read_text(encoding="utf-8"), encoding="utf-8")
    (d / "README-PARTICIPER.md").write_text(PART_README, encoding="utf-8")
    for f in (comp, pres, kit_zip, train_zip, soum):
        shutil.copy2(f, d / "kits" / f.name)
    lignes = ["# Manifeste du pack participation v1.1.0", ""]
    for f in sorted((d / "kits").iterdir()):
        lignes.append(f"- `{f.name}` — {f.stat().st_size} o — sha256 {sha(f)}")
    (d / "MANIFESTE.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return zipdir("TRIADE_participer_v1.1.0.zip", d.parent, [str(d.relative_to(R))])


def main():
    OUT.mkdir(exist_ok=True)
    soum = soumission()
    pres = presentation()
    comp = complet()
    kit = R / "TRIADE_kit_developpement_v1.3.0.zip"
    train = next(R.glob("TRIADE_train_v1.0.0.zip"), None)
    if train is None:
        train = next((R / "participation-v1" / "kits").glob("TRIADE_train_*.zip"))
    part = participation(kit, train, soum, pres, comp)
    doc = {}
    for f in (soum, pres, comp, part, kit):
        doc[f.name] = {"bytes": f.stat().st_size, "sha256": sha(f), "md5": md5(f)}
    (OUT / "MANIFESTE-PACKS-v0.26.0.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    for k, v in doc.items():
        print(f"{k}  {v['bytes']} o  sha256 {v['sha256'][:16]}…  md5 {v['md5']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
