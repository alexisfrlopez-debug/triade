#!/usr/bin/env python3
"""verify_livraison_d46.py — vérifie que les 14 fichiers de la couche I M3
(m3/I/*.md) sont bien sur le miroir Drive (dossier TRIADE/), MD5 identiques
aux fichiers locaux. Réutilise l'authentification et le listing de
drive_sync.py (aucune logique réseau propre)."""
import hashlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import drive_sync as ds  # noqa: E402

REPO = ds.REPO


def sous_dossier(nom, parent_id):
    for nom_d, meta in ds.list_folder(parent_id).items():
        if nom_d == nom and meta.get("mimeType") == ds.FOLDER_MIME:
            return meta["id"]
    return None


def main():
    triade = sous_dossier("TRIADE", ds.DRIVE_ROOT_ID)
    assert triade, "dossier TRIADE introuvable"
    m3 = sous_dossier("m3", triade)
    assert m3, "dossier m3 absent du miroir Drive"
    I = sous_dossier("I", m3)
    assert I, "dossier m3/I absent du miroir Drive"

    distants = ds.list_folder(I)
    print(f"[drive] m3/I contient {len(distants)} fichiers")

    locaux = sorted((REPO / "m3" / "I").glob("*.md"))
    tout_ok = True
    for p in locaux:
        d = distants.get(p.name, {}).get("md5Checksum")
        loc = hashlib.md5(p.read_bytes()).hexdigest()
        ok = d is not None and d == loc
        tout_ok &= ok
        print(f"  {'MATCH ' if ok else 'ÉCART  '} {p.name}"
              + ("" if ok else f" (distant={d}, local={loc})"))
    print("TOUT CONFORME" if tout_ok and len(locaux) == 14 else "ANOMALIE")
    return 0 if tout_ok and len(locaux) == 14 else 1


if __name__ == "__main__":
    sys.exit(main())
