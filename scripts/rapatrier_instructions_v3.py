#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rapatrier les SIX nouveaux fichiers d'instruction (vague 3 du 20261111,
19:14-19:15 UTC) de /instructions vers upload/ + copie au dépôt
instructions_20261111/ — recoup md5 contre les métadonnées Drive
(le modèle des vagues 1 et 2)."""
import pathlib
import shutil
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

INSTR_ID = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
UPLOAD = pathlib.Path("/home/z/my-project/upload")
DEPOT = REPO / "instructions_20261111"

FICHIERS = [
    "Qwen__20261111_sollwnmae.txt",
    "Qwen__20261111_xboh1kljq.txt",
    "Qwen__20261111_6zqo2h60n.txt",
    "Qwen__20261111_n4kwcs3wa.txt",
    "Qwen__20261111_54wni4hzh.txt",
    "Qwen__20261111_lfh49a1xf.txt",
]

ent = ds.list_folder(INSTR_ID)
print(f"[instr] /instructions porte {len(ent)} entrées")
erreurs = 0
for nom in FICHIERS:
    f = ent.get(nom)
    if not f:
        print(f"[instr] ABSENT de /instructions : {nom}", file=sys.stderr)
        erreurs += 1
        continue
    dest = UPLOAD / nom
    st, corps, _ = ds.api("GET", f"{ds.API}/files/{f['id']}?alt=media")
    if st != 200:
        print(f"[instr] téléchargement impossible ({st}) : {nom}", file=sys.stderr)
        erreurs += 1
        continue
    dest.write_bytes(corps)
    md5 = ds.md5_of(dest)
    attendu = f.get("md5Checksum")
    ok = md5 == attendu
    print(f"[instr] {nom} : {len(corps)} o, md5 {md5[:12]}… "
          f"{'MATCH' if ok else 'ÉCART (attendu ' + str(attendu) + ')'}")
    if not ok:
        erreurs += 1
        continue
    cible = DEPOT / nom
    if not cible.exists():
        shutil.copy2(dest, cible)
        print(f"[instr] copie dépôt : {cible}")
    elif ds.md5_of(cible) != md5:
        print(f"[instr] ÉCART : {cible} existe et diverge", file=sys.stderr)
        erreurs += 1

sys.exit(1 if erreurs else 0)
