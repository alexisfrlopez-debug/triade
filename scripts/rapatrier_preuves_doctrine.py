#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_preuves_doctrine.py — lecture seule : rapatrie les PIÈCES
ORIGINALES fondatrices des décisions D138 / D145 / D148 (la recoupure
post-mortem promise) depuis les archives du coffre /test :

  preuves-run-v6 (28 pièces, D138 — la lecture virtualisée est aveugle) ;
  preuves-run-e2 (7 pièces,  D145 — aucune garde ne dépend d'une lecture
                            en live d'un fichier en cours d'écriture) ;
  preuves-run-v8 (fetch CIBLÉ : la matrice S3 + hosts — la revendication
                 D148 « v6, v8, e4 : pièces identiques octet pour octet ») ;
  preuves-run-e4 (37 pièces, D148 — les verdicts se rendent post-mortem) :
                 PAS de re-téléchargement — les copies locales de Task 61
                 sont re-contrôlées md5 contre le coffre ; tout écart est
                 NOMMÉ (fail-closed), le coffre fait foi.

Chaque fichier téléchargé est contrôlé : md5 local == md5 distant RE-LU.
Jamais une écriture au coffre, jamais un jeton lu ici.

Usage : python3 scripts/rapatrier_preuves_doctrine.py
Code de sortie : 0 = tout conforme ; 1 = écart nommé ; 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DL = pathlib.Path("/home/z/my-project/download")

# Le fetch ciblé de v8 : la matrice curl S3 + hosts (revendication D148)
V8_CIBLE = ["curl-d2a.txt", "curl-d2b.txt", "curl-d3.txt",
            "curl-d5.txt", "hosts-lu.txt"]


def md5f(p: pathlib.Path) -> str:
    import hashlib
    return hashlib.md5(p.read_bytes()).hexdigest()


def telecharger(file_id: str, destination: pathlib.Path) -> bytes:
    url = f"{ds.API}/files/{file_id}?alt=media"
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.write_bytes(body)
    return body


def archives() -> dict:
    test = ds.list_folder(TEST_ID)
    return ds.list_folder(test["archives-preuves"]["id"])


def rapatrie_dossier(nom_dossier: str, dest: pathlib.Path,
                     cible: list | None = None) -> int:
    """Rapatrie un dossier d'archives (tout, ou le sous-ensemble CIBLE),
    md5 contrôlés par relecture. Retourne le nombre d'écarts nommés."""
    arch = archives()
    d = arch.get(nom_dossier)
    if not d:
        print(f"[doctrine] ERREUR : dossier d'archives ABSENT : {nom_dossier}",
              file=sys.stderr)
        return 2
    distants = ds.list_folder(d["id"])
    noms = (cible if cible is not None
            else sorted(n for n, m in distants.items()
                        if m.get("mimeType") != ds.FOLDER_MIME))
    dest.mkdir(parents=True, exist_ok=True)
    ecarts = 0
    for nom in noms:
        f = distants.get(nom)
        if not f:
            print(f"[doctrine] PIÈCE ABSENTE au coffre : {nom_dossier}/{nom}",
                  file=sys.stderr)
            ecarts += 1
            continue
        destination = dest / nom
        corps = telecharger(f["id"], destination)
        md5_local = md5f(destination)
        md5_distant = (f.get("md5Checksum") or "").lower()
        ok = md5_local == md5_distant and len(corps) == f.get("size", len(corps))
        print(f"[doctrine] {nom_dossier}/{nom} : {len(corps)} o, "
              f"md5 {md5_local[:10]}… {'MATCH' if ok else 'ÉCART'}")
        if not ok:
            ecarts += 1
    return ecarts


def recontrole_e4() -> int:
    """Re-contrôle les copies LOCALES de preuves-run-e4 (Task 61) contre
    le coffre — sans re-télécharger ; le coffre fait foi, tout écart nommé."""
    arch = archives()
    d = arch.get("preuves-run-e4")
    if not d:
        print("[doctrine] ERREUR : preuves-run-e4 ABSENT des archives",
              file=sys.stderr)
        return 2
    distants = ds.list_folder(d["id"])
    dest = DL / "preuves-run-e4"
    if not dest.is_dir():
        print("[doctrine] ERREUR : copies locales e4 ABSENTES (Task 61)",
              file=sys.stderr)
        return 2
    ecarts = 0
    for nom, f in sorted(distants.items()):
        if f.get("mimeType") == ds.FOLDER_MIME:
            continue
        local = dest / nom
        if not local.exists():
            print(f"[doctrine] e4 LOCALE ABSENTE : {nom} — re-téléchargement",
                  file=sys.stderr)
            corps = telecharger(f["id"], local)
            if md5f(local) == (f.get("md5Checksum") or "").lower():
                print(f"[doctrine] e4/{nom} : {len(corps)} o re-téléchargé, MATCH")
                continue
            print(f"[doctrine] e4/{nom} : ÉCART après re-téléchargement")
            ecarts += 1
            continue
        md5_local = md5f(local)
        md5_distant = (f.get("md5Checksum") or "").lower()
        ok = md5_local == md5_distant
        print(f"[doctrine] e4/{nom} : {local.stat().st_size} o, "
              f"md5 {md5_local[:10]}… {'MATCH' if ok else 'ÉCART'}"
              + ("" if ok else " — le coffre fait foi, re-téléchargement"))
        if not ok:
            corps = telecharger(f["id"], local)   # le coffre fait foi
            if md5f(local) != md5_distant:
                print(f"[doctrine] e4/{nom} : ÉCART PERSISTANT — nommé")
                ecarts += 1
    # les fichiers locaux SANS pendant au coffre : nommés (pas des pièces)
    locaux = {p.name for p in dest.iterdir() if p.is_file()}
    sans_pair = sorted(locaux - set(distants.keys()))
    for nom in sans_pair:
        print(f"[doctrine] e4/{nom} : local SANS pendant au coffre "
              f"(nommé, non-pièce probable)")
    return ecarts


def main() -> int:
    try:
        ecarts = 0
        print("[doctrine] === RAPATRIEMENT DES PIÈCES ORIGINALES "
              "D138/D145/D148 (archives, lecture seule) ===")
        print("[doctrine] — preuves-run-v6 (D138, 28 pièces attendues) —")
        ecarts += rapatrie_dossier("preuves-run-v6", DL / "preuves-run-v6") or 0
        print("[doctrine] — preuves-run-e2 (D145, 7 pièces attendues) —")
        ecarts += rapatrie_dossier("preuves-run-e2", DL / "preuves-run-e2") or 0
        print("[doctrine] — preuves-run-v8 (fetch ciblé matrice S3 + hosts, "
              "revendication D148) —")
        ecarts += rapatrie_dossier("preuves-run-v8", DL / "preuves-run-v8",
                                   cible=V8_CIBLE) or 0
        print("[doctrine] — preuves-run-e4 (D148, re-contrôle des copies "
              "Task 61, 37 pièces) —")
        ecarts += recontrole_e4() or 0
    except Exception as exc:  # noqa: BLE001
        print(f"[doctrine] ERREUR FATALE : {exc}", file=sys.stderr)
        return 2
    if ecarts == 0:
        print("[doctrine] RAPATRIEMENT CONFORME — les pièces originales "
              "sont locales, md5 contrôlés contre le coffre")
        return 0
    print(f"[doctrine] {ecarts} écart(s) nommé(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
