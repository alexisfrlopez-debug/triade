#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASSEMBLAGE DES PACKS v0.33.1 (la correction de la vague 28) : soumission, présentation, complet.

Patron : l'assemblage v0.33.0 (le patron v0320 reconduit) — mêmes rôles, les
contenus CORRIGÉS de la vague 28. La porte de génération v331 (V1..V7 +
L1..L32) doit être VERTE avant l'assemblage (le refus ferme aux assembleurs).

- soumission  : les quatre pièces au patron v0310 (le LISEZMOI, le manuscrit,
                le manifeste des empreintes v0.33.1, le rapport de
                vérification v0.33.1) ;
- présentation : le pack-v331 entier (les cinq pièces numérotées — les quatre
                reconduites + la preuves régénérée — + leurs descriptions + le
                manifeste + le rapport) ;
- complet     : chaque entrée du complet v0.33.0 SERVIE depuis l'arbre courant
                quand le chemin y vit, sinon reprise TELLE QUELLE (les ateliers
                d'ère), plus les ajouts de la correction (le pack-v331,
                l'atelier-w28corrige, la chaîne v331, les registres corrigés) ;
- MANIFESTE-PACKS-v0.33.1.json : les trois packs, bytes/sha256/md5.

La participation v1.2.0 N'EST PAS RÉASSEMBLÉE (elle est publiée au record
24545356 ; une v1.3.0 — qui porterait les packs v0.33.0 — attend la commande
du maître : l'écart est nommé au LISEZMOI, pas habillé).

Aucun contenu réécrit : les pièces du pack-v330 sont copiées telles quelles ;
les description.txt suivent le patron v0310 (62 octets de rôle, une ligne).
"""
import hashlib
import json
import pathlib
import re
import shutil
import sys
import zipfile

R = pathlib.Path(__file__).resolve().parents[2]
PACK = R / "pack-v331"
OUT = R / "depot-zenodo-v0331"
EDITION = "v0.33.1"
DESCRIPTION = "pièce de l'édition corrective v0.33.1 (la correction de la vague 28, 27 novembre 2026).\n"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def recoup_manifeste():
    """la provenance avant tout geste : les cinq pièces == le manifeste."""
    attendu = {}
    for ligne in (PACK / f"empreintes_livrables_{EDITION}.txt").read_text(
            encoding="utf-8").splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+(.+)$", ligne.strip())
        if m:
            attendu[m.group(2)] = m.group(1)
    pieces = {
        "TRIADE_manuscrit_v0.33.0.pdf": PACK / "1-manuscrit/TRIADE_manuscrit_v0.33.0.pdf",
        "Protocole_TRIADE_v0.15.18_Specification.pdf": PACK / "2-specification/Protocole_TRIADE_v0.15.18_Specification.pdf",
        "Livre_du_Coffre_TRIADE_CF1-CF3_v1.17.pdf": PACK / "3-coffre-fort/Livre_du_Coffre_TRIADE_CF1-CF3_v1.17.pdf",
        "TRIADE_preuves_et_calculs_v0.33.1.pdf": PACK / "4-preuves-calculs/TRIADE_preuves_et_calculs_v0.33.1.pdf",
        "TRIADE_presentation_v0330.pdf": PACK / "5-presentation/TRIADE_presentation_v0330.pdf",
    }
    for nom, chemin in pieces.items():
        if sha(chemin) != attendu[nom]:
            raise SystemExit(f"ROUGE provenance : {nom} != manifeste — assemblage refusé")
    print(f"[provenance] 5/5 VERT — les pièces égalent le manifeste {EDITION}")


def apparat():
    """les copies d'apparat : les plans de la vague à plans-vague28/, les
    description.txt posées au pack-v330."""
    plans = R / "plans-vague28"
    plans.mkdir(exist_ok=True)
    for f in sorted(R.glob("PLAN-W28*.md")):
        shutil.copy2(f, plans / f.name)
    n_plans = len(list(plans.iterdir()))
    for d in sorted(p for p in PACK.iterdir() if p.is_dir()):
        if d.name == "4-preuves-calculs":
            (d / "description.txt").write_text(DESCRIPTION, encoding="utf-8")
    print(f"[apparat] plans-vague28/ : {n_plans} plans ; description.txt de la preuves SEULE "
          "(les quatre reconduites gardent leur description v0.33.0 — le patron v0.23.4)")


def soumission():
    tmp = OUT / "src"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    for f in (R / f"LISEZMOI-livrables-{EDITION}.txt",
              next((PACK / "1-manuscrit").glob("TRIADE_manuscrit_v*.pdf")),
              PACK / f"empreintes_livrables_{EDITION}.txt",
              PACK / f"rapport_verification_{EDITION}.txt"):
        shutil.copy2(f, tmp / f.name)
    chemin = OUT / f"TRIADE_soumission_{EDITION}.zip"
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(tmp.iterdir()):
            z.write(f, f.name)
    print(f"[soumission] {chemin.name} — 4 entrées, {chemin.stat().st_size} o")
    return chemin


def presentation():
    chemin = OUT / "TRIADE_presentation_v0331.zip"
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(PACK.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, str(f.relative_to(R)))
    print(f"[présentation] {chemin.name} — {len(zipfile.ZipFile(chemin).namelist())} entrées, "
          f"{chemin.stat().st_size} o")
    return chemin


AJOUTS_DIR = ["pack-v331", "atelier-w28corrige", "pack-v330", "atelier-w28vaes",
              "atelier-w28opt16", "atelier-w28harnais", "atelier-w28attr",
              "atelier-w28terrain", "atelier-w28rlvr", "atelier-w28imrad",
              "scripts/vague28", "scripts/spec_v160", "scripts/spec_v159",
              "scripts/livre_v20", "scripts/livre_v19", "plans-vague28"]
AJOUTS_FICHIER = ["EMPREINTES-PLANS-VAGUE28.txt", "LISEZMOI-livrables-v0.33.0.txt",
                  "LISEZMOI-livrables-v0.33.1.txt"]


def complet():
    """Le complet = chaque entrée du complet v0.33.0 SERVIE depuis l'arbre
    courant quand le chemin y vit, sinon reprise TELLE QUELLE du v0.33.0
    (les ateliers d'ère), plus les ajouts de la CORRECTION (pack-v331,
    atelier-w28corrige, la chaîne v331, les registres corrigés servis de
    l'arbre)."""
    base = R / "depot-zenodo-v0330" / "TRIADE_complet_v0.33.0.zip"
    chemin = OUT / f"TRIADE_complet_{EDITION}.zip"
    repris, servis, dedoublonne = 0, 0, 0
    with zipfile.ZipFile(base) as src, \
            zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        vus = set()
        for info in src.infolist():
            if info.filename.endswith("/") or info.filename in vus:
                if info.filename in vus:
                    dedoublonne += 1
                continue
            vus.add(info.filename)
            courant = R / info.filename
            if courant.is_file():
                z.write(courant, info.filename)
                servis += 1
            else:
                z.writestr(info.filename, src.read(info.filename))
                repris += 1
        ajouts = []
        for d in AJOUTS_DIR:
            p = R / d
            if not p.exists():
                continue
            for f in p.rglob("*"):
                if f.is_file() and "__pycache__" not in f.parts and ".git" not in f.parts:
                    ajouts.append(f)
        for nom in AJOUTS_FICHIER:
            f = R / nom
            if f.is_file():
                ajouts.append(f)
        nouveaux = 0
        for f in sorted(set(ajouts)):
            rel = str(f.relative_to(R))
            if rel in vus:            # déjà servi de l'arbre au passage de la base — jamais deux fois
                continue
            z.write(f, rel)
            nouveaux += 1
    total = servis + repris + nouveaux
    print(f"[complet] {chemin.name} — {total} entrées uniques "
          f"({servis} servies de l'arbre, {repris} reprises du v0.33.0, "
          f"{nouveaux} ajouts de la correction, {dedoublonne} doublons hérités résorbés), "
          f"{chemin.stat().st_size} o")
    return chemin


def verifie(soum, pres, comp):
    """chaque archive testée, chaque entrée relue, les cinq pièces du pack
    recoupées au manifeste, la soumission recoupée aux sources."""
    attendu = {}
    for ligne in (PACK / f"empreintes_livrables_{EDITION}.txt").read_text(
            encoding="utf-8").splitlines():
        parts = ligne.split()
        if len(parts) == 2 and len(parts[0]) == 64:
            attendu[parts[1]] = parts[0]
    for chemin, controle in ((soum, "soumission"), (pres, "présentation"), (comp, "complet")):
        with zipfile.ZipFile(chemin) as z:
            if z.testzip() is not None:
                raise SystemExit(f"ROUGE testzip : {chemin.name}")
            noms = z.namelist()
            if len(noms) != len(set(noms)):
                raise SystemExit(f"ROUGE doublon d'entrées : {chemin.name}")
            for n in noms:
                donnees = z.read(n)
                if n.startswith("pack-v331/") and n.rsplit("/", 1)[-1] in attendu:
                    if hashlib.sha256(donnees).hexdigest() != attendu[n.rsplit("/", 1)[-1]]:
                        raise SystemExit(f"ROUGE empreinte : {n}")
            if controle == "soumission":
                for f in (OUT / "src").iterdir():
                    if z.read(f.name) != f.read_bytes():
                        raise SystemExit(f"ROUGE soumission != source : {f.name}")
            if controle == "présentation" and len(noms) != 12:
                raise SystemExit(f"ROUGE présentation : {len(noms)} entrées != 12")
        print(f"[vérification] {chemin.name} — testzip OK, entrées relues, empreintes recoupées")


def main():
    recoup_manifeste()
    apparat()
    OUT.mkdir(parents=True, exist_ok=True)
    soum = soumission()
    pres = presentation()
    comp = complet()
    verifie(soum, pres, comp)
    man = {
        "edition": EDITION,
        "packs": {
            p.name: {"bytes": p.stat().st_size, "sha256": sha(p), "md5": md5(p)}
            for p in (soum, pres, comp)
        },
    }
    (OUT / "MANIFESTE-PACKS-v0.33.1.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[manifeste] MANIFESTE-PACKS-v0.33.1.json — {len(man['packs'])} packs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
