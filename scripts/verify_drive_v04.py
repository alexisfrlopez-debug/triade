#!/usr/bin/env python3
"""Vérification ciblée du miroir Drive : les livrables v0.4 (article PDF +
rapport de vérification + sources) doivent exister côté Drive avec le bon
md5. Utilise l'API du module drive_sync.py (jetons, aucun affichage de
secret). Sortie : liste des fichiers vérifiés et verdict.
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TARGETS = [
    "docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf",
    "docs/VERIFICATION_v0.4_Article.md",
    "docs/Protocole_TRIADE_v0.3_Specification.pdf",  # régénéré par D17
    "scripts/article_v04/main.tex",
    "scripts/article_v04/refs.bib",
    "scripts/article_v04/verify_article.py",
]

# Racine du dossier Drive « Triade » puis sous-dossier TRIADE/ (miroir)
ROOT_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
st, body, _ = ds.api("GET",
    "https://www.googleapis.com/drive/v3/files?q="
    + ds.urllib.parse.quote(f"'{ROOT_ID}' in parents and trashed = false"
                             " and mimeType = 'application/vnd.google-apps.folder'")
    + "&fields=files(id,name)")
folders = {f["name"]: f["id"] for f in json.loads(body)["files"]}
triade_id = folders.get("TRIADE")
assert triade_id, f"dossier TRIADE introuvable : {list(folders)}"


def find(relpath):
    """Descend l'arborescence Drive pour retrouver l'identifiant du fichier."""
    cur = triade_id
    parts = relpath.split("/")
    for part in parts[:-1]:
        q = ds.urllib.parse.quote(
            f"'{cur}' in parents and trashed = false and name = '{part}'")
        st, body, _ = ds.api(
            "GET", f"https://www.googleapis.com/drive/v3/files?q={q}"
                   "&fields=files(id,name)")
        items = json.loads(body)["files"]
        if not items:
            return None
        cur = items[0]["id"]
    q = ds.urllib.parse.quote(
        f"'{cur}' in parents and trashed = false and name = '{parts[-1]}'")
    st, body, _ = ds.api(
        "GET",
        f"https://www.googleapis.com/drive/v3/files?q={q}"
        "&fields=files(id,name,md5Checksum,size)")
    items = json.loads(body)["files"]
    return items[0] if items else None


ok = True
for rel in TARGETS:
    local = REPO / rel
    if not local.exists():
        print(f"[ERREUR] fichier local absent : {rel}")
        ok = False
        continue
    local_md5 = hashlib.md5(local.read_bytes()).hexdigest()
    remote = find(rel)
    if remote is None:
        print(f"[ABSENT DRIVE] {rel}")
        ok = False
    elif remote.get("md5Checksum") != local_md5:
        print(f"[MD5 DIVERGENT] {rel} "
              f"(drive={remote.get('md5Checksum')} local={local_md5})")
        ok = False
    else:
        print(f"[OK] {rel} — md5 conforme "
              f"({int(remote.get('size', 0)) / 1024:.1f} Kio)")

print()
print("VERDICT :", "MIROIR DRIVE CONFORME" if ok else "ÉCARTS DÉTECTÉS")
sys.exit(0 if ok else 1)
