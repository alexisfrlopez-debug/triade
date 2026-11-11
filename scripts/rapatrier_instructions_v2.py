#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rapatrier les TROIS nouveaux fichiers d'instruction (vague 2 du 20261111)
de /instructions vers upload/ + copie au dépôt instructions_20261111/ —
recoup md5 contre les métadonnées Drive (le modèle des trois premiers)."""
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
    "Qwen_text_20261111_f3q3x9i7n.txt",
    "Qwen_text_20261111_ic09ydeli.txt",
    "Qwen_text_20261111_ysddxpk0o.txt",
]

ent = ds.list_folder(INSTR_ID)
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
