#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASSEMBLAGE DES PACKS v0.32.0 (la vague 27) : soumission, présentation, complet.

Patron : les packs v0.31.0 (depot-zenodo-v0310, l'assemblage de la vague 26) —
mêmes rôles, contenus de la vague 27. La porte de génération v320 (V1..V7 +
L1..L29) doit être VERTE avant l'assemblage (le refus ferme aux assembleurs,
la doctrine des vagues précédentes).

- soumission  : les quatre pièces au patron v0310 (le LISEZMOI, le manuscrit,
                le manifeste des empreintes, le rapport de vérification) ;
- présentation : le pack-v320 entier (les cinq pièces numérotées + leurs
                descriptions + le manifeste + le rapport) ;
- complet     : chaque entrée du complet v0.31.0 SERVIE depuis l'arbre courant
                quand le chemin y vit, sinon reprise TELLE QUELLE (les ateliers
                d'ère), plus les ajouts de la vague 27 (le pack-v320, les six
                ateliers w27, les scripts/vague27, les plans-vague27, le
                manifeste des plans, le LISEZMOI) ;
- MANIFESTE-PACKS-v0.32.0.json : les trois packs, bytes/sha256/md5.

La participation v1.2.0 N'EST PAS RÉASSEMBLÉE (elle est publiée au record
24545356 ; une v1.3.0 — qui porterait les packs v0.32.0 — attend la commande
du maître : l'écart est nommé au LISEZMOI, pas habillé).

Les trois doublons d'entrées hérités du complet v0.31.0 (PREUVES-STATUTS.json,
atelier-w23-harnais/harnais-resultat.json, atelier-w23-seuils/seuils.json —
chacun deux fois au zip) sont résorbés : chaque nom écrit UNE fois, les octets
servis depuis l'arbre courant (l'acte nommé au journal, l'extraction inchangée).

Aucun contenu réécrit : les pièces du pack-v320 sont copiées telles quelles ;
les description.txt suivent le patron v0310 (62 octets de rôle, une ligne).
"""
import hashlib
import json
import pathlib
import shutil
import sys
import zipfile

R = pathlib.Path(__file__).resolve().parents[2]
PACK = R / "pack-v320"
OUT = R / "depot-zenodo-v0320"
EDITION = "v0.32.0"
DESCRIPTION = "pièce de l'édition v0.32.0 (la vague 27, 26 novembre 2026).\n"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def recoup_manifeste():
    """la provenance avant tout geste : les cinq pièces == le manifeste
    (le recoup de la 438 rejoué — la porte v320 l'exige aussi à V1)."""
    import re
    attendu = {}
    for ligne in (PACK / f"empreintes_livrables_{EDITION}.txt").read_text(
            encoding="utf-8").splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+(.+)$", ligne.strip())
        if m:
            attendu[m.group(2)] = m.group(1)
    pieces = {
        "TRIADE_manuscrit_v0.32.0.pdf": PACK / "1-manuscrit/TRIADE_manuscrit_v0.32.0.pdf",
        "Protocole_TRIADE_v0.15.17_Specification.pdf": PACK / "2-specification/Protocole_TRIADE_v0.15.17_Specification.pdf",
        "Livre_du_Coffre_TRIADE_CF1-CF3_v1.16.pdf": PACK / "3-coffre-fort/Livre_du_Coffre_TRIADE_CF1-CF3_v1.16.pdf",
        "TRIADE_preuves_et_calculs_v0.32.0.pdf": PACK / "4-preuves-calculs/TRIADE_preuves_et_calculs_v0.32.0.pdf",
        "TRIADE_presentation_v0320.pdf": PACK / "5-presentation/TRIADE_presentation_v0320.pdf",
    }
    for nom, chemin in pieces.items():
        if sha(chemin) != attendu[nom]:
            raise SystemExit(f"ROUGE provenance : {nom} != manifeste — assemblage refusé")
    print(f"[provenance] 5/5 VERT — les pièces égalent le manifeste {EDITION}")


def apparat():
    """les copies d'apparat du pack (le précédent 6aa4557) : les plans de la
    vague copiés à plans-vague27/, les description.txt posées au pack-v320."""
    plans = R / "plans-vague27"
    plans.mkdir(exist_ok=True)
    for f in sorted(R.glob("PLAN-W27*.md")):
        shutil.copy2(f, plans / f.name)
    n_plans = len(list(plans.iterdir()))
    for d in sorted(p for p in PACK.iterdir() if p.is_dir()):
        (d / "description.txt").write_text(DESCRIPTION, encoding="utf-8")
    print(f"[apparat] plans-vague27/ : {n_plans} plans ; description.txt aux cinq dossiers du pack")


def soumission():
    tmp = OUT / "src"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    for f in (R / f"LISEZMOI-livrables-{EDITION}.txt",
              PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf",
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
    chemin = OUT / "TRIADE_presentation_v0320.zip"
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(PACK.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, str(f.relative_to(R)))
    print(f"[présentation] {chemin.name} — 12 entrées, {chemin.stat().st_size} o")
    return chemin


AJOUTS_DIR = ["pack-v320", "atelier-w27recon", "atelier-w27resid", "atelier-w27cibles",
              "atelier-w27decco", "atelier-w27preuv", "atelier-w27vaes",
              "scripts/vague27", "plans-vague27"]
AJOUTS_FICHIER = ["EMPREINTES-PLANS-VAGUE27.txt", "LISEZMOI-livrables-v0.32.0.txt"]


def complet():
    """Le complet = chaque entrée du complet v0.31.0 SERVIE depuis l'arbre
    courant quand le chemin y vit, sinon reprise TELLE QUELLE du pack v0.31.0
    (les ateliers d'ère), plus les ajouts de la vague 27."""
    base = R / "depot-zenodo-v0310" / "TRIADE_complet_v0.31.0.zip"
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
            for f in (R / d).rglob("*"):
                if f.is_file() and "__pycache__" not in f.parts and ".git" not in f.parts:
                    ajouts.append(f)
        for nom in AJOUTS_FICHIER:
            f = R / nom
            if f.is_file():
                ajouts.append(f)
        for f in sorted(set(ajouts)):
            z.write(f, str(f.relative_to(R)))
    total = servis + repris + len(set(ajouts))
    print(f"[complet] {chemin.name} — {total} entrées uniques "
          f"({servis} servies de l'arbre, {repris} reprises du v0.31.0, "
          f"{len(set(ajouts))} ajouts de la vague 27, {dedoublonne} doublons hérités résorbés), "
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
    ok = 0
    for chemin, controle in ((soum, "soumission"), (pres, "présentation"), (comp, "complet")):
        with zipfile.ZipFile(chemin) as z:
            if z.testzip() is not None:
                raise SystemExit(f"ROUGE testzip : {chemin.name}")
            noms = z.namelist()
            if len(noms) != len(set(noms)):
                raise SystemExit(f"ROUGE doublon d'entrées : {chemin.name}")
            for n in noms:
                donnees = z.read(n)
                if n.startswith("pack-v320/") and n.rsplit("/", 1)[-1] in attendu:
                    if hashlib.sha256(donnees).hexdigest() != attendu[n.rsplit("/", 1)[-1]]:
                        raise SystemExit(f"ROUGE empreinte : {n}")
            if controle == "soumission":
                for f in (OUT / "src").iterdir():
                    if z.read(f.name) != f.read_bytes():
                        raise SystemExit(f"ROUGE soumission != source : {f.name}")
            if controle == "présentation" and len(noms) != 12:
                raise SystemExit(f"ROUGE présentation : {len(noms)} entrées != 12")
        ok += 1
        print(f"[vérification] {chemin.name} — testzip OK, entrées relues, empreintes recoupées")
    return ok


def main():
    OUT.mkdir(exist_ok=True)
    recoup_manifeste()
    apparat()
    soum = soumission()
    pres = presentation()
    comp = complet()
    verifie(soum, pres, comp)
    doc = {}
    for f in (soum, pres, comp):
        doc[f.name] = {"bytes": f.stat().st_size, "sha256": sha(f), "md5": md5(f)}
    (OUT / "MANIFESTE-PACKS-v0.32.0.json").write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for k, v in doc.items():
        print(f"{k}  {v['bytes']} o  sha256 {v['sha256'][:16]}…  md5 {v['md5']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
