#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_session_cq01qv1za.py — LA LIVRAISON DE LA SESSION cq01qv1za ET DE LA
SYNCHRONISATION v0.19.4 (le motif de la session 5ey7gmjra, à UNE commande près) :
  (0) le miroir TRIADE-sauvegarde-git synchronisé (drive_sync.py — le bundle
      compris) PUIS le kit D130 rafraîchi (maj_kit.py) au commit 5be0320 ;
  (1) les pièces au /test du coffre (recoupées byte-byte au re-téléchargement) :
      les DEUX RAPPORTs de la campagne, le contrôle négatif 5/5, le rapport de
      vérification v0.19.4, le rapport de la nouvelle version Zenodo ;
  (2) le pack TRIADE_presentation_v0.19.4_20261120.zip à la RACINE du coffre
      (le motif des packs de présentation) ;
  (3) l'instruction cq01qv1za ARCHIVÉE : /instructions → /ARCHIVE/
      instructions_20261119/ (la règle du développeur) — le geste Drive natif
      addParents/removeParents, la corbeille JAMAIS (D143).

L'AUTHENTIFICATION : celle de drive_sync.py (le relais OAuth s'il vit, le repli
compte de service sinon — D263). Le script REFUSE de mentir : si l'écriture est
refusée (le 403 du lecteur seul), il le NOMME et rend 1 — relancer quand un
justificatif vivant est au .gdrive/."""
import hashlib
import json
import pathlib
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402  l'instrument établi, JAMAIS réécrit

ROOT_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"

PIECES_TEST = [
    ("RAPPORT-cq01qv1za-M4.txt",
     REPO / "atelier-cout-boucle-cq01qv1za/RAPPORT-cq01qv1za-M4.txt"),
    ("RAPPORT-cq01qv1za-POINTEUR.txt",
     REPO / "atelier-cout-boucle-cq01qv1za/RAPPORT-cq01qv1za-POINTEUR.txt"),
    ("controle-negatif-v2.txt",
     REPO / "atelier-cout-boucle-cq01qv1za/preuves/controle-negatif-v2.txt"),
    ("rapport_verification_v0.19.4.txt",
     REPO / "scripts/vague7/rapport_verification_v0.19.4.txt"),
    ("RAPPORT-ZENODO-V0194-20261120.txt",
     REPO / "scripts/vague7/RAPPORT-ZENODO-V0194-20261120.txt"),
]
PACK_RACINE = REPO / "scripts/vague7/TRIADE_presentation_v0.19.4_20261120.zip"
INSTRUCTION = "Qwen__20261118_cq01qv1za.txt"


def api(method, url, body=None):
    return ds.api(method, url, body)


def inventaire(fid):
    return ds.list_folder(fid)


def contenu(file_id):
    req = urllib.request.Request(f"{API}/files/{file_id}?alt=media",
                                 headers={"Authorization": "Bearer " + ds.get_access_token()})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def md5_de(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def resumable(init_url, metadata, chemin):
    return ds.resumable_upload(init_url, metadata, chemin,
                               init_method="PATCH" if "files/" in init_url else "POST")


def main() -> int:
    # (0) le miroir puis le kit — les instruments canoniques TELS QUELS
    print("=== (0) le miroir (drive_sync.py) puis le kit (maj_kit.py) ===")
    r1 = subprocess.run([sys.executable, str(REPO / "scripts/drive_sync.py")],
                        cwd=REPO, capture_output=True, text=True, timeout=1800)
    print(r1.stdout.strip().splitlines()[-1] if r1.stdout.strip() else "(silence)")
    if r1.returncode not in (0, 1):
        print(f"ROUGE drive_sync : {r1.stderr[-300:]}")
        return 1
    r2 = subprocess.run([sys.executable, str(REPO / "scripts/maj_kit.py")],
                        cwd=REPO, capture_output=True, text=True, timeout=1800)
    print(r2.stdout.strip().splitlines()[-1] if r2.stdout.strip() else "(silence)")
    if r2.returncode not in (0, 1):
        print(f"ROUGE maj_kit : {r2.stderr[-300:]}")
        return 1

    bilan = []

    def geste(nom, fn):
        try:
            detail = fn()
            bilan.append(("VERT", nom))
            print(f"VERT  {nom} — {detail}")
        except Exception as e:  # noqa: BLE001
            bilan.append(("ROUGE", nom))
            print(f"ROUGE {nom} — {str(e)[:250]}")

    racine = inventaire(ROOT_ID)
    test_id = racine["test"]["id"]
    archive_id = racine["ARCHIVE"]["id"]
    instructions_id = racine["instructions"]["id"]
    test = inventaire(test_id)

    # (1) les pièces au /test — idempotentes (md5 égal → rien)
    for nom, chemin in PIECES_TEST:
        def g(nom=nom, chemin=chemin, test=test, test_id=test_id):
            if nom in test and test[nom].get("md5Checksum") == md5_de(chemin):
                return "DÉJÀ EN PLACE (md5 égal)"
            if nom in test:
                resumable(f"https://www.googleapis.com/upload/drive/v3/files/"
                          f"{test[nom]['id']}?uploadType=resumable", {}, chemin)
            else:
                resumable("https://www.googleapis.com/upload/drive/v3/files"
                          "?uploadType=resumable",
                          {"name": nom, "parents": [test_id]}, chemin)
            octets = contenu(inventaire(test_id)[nom]["id"])
            assert hashlib.md5(octets).hexdigest() == md5_de(chemin), "recoup échoue"
            return f"posé et recoupé byte-byte ({chemin.stat().st_size} o)"
        geste(f"le /test : {nom}", g)

    # (2) le pack à la racine
    def g_pack():
        nom = PACK_RACINE.name
        racine = inventaire(ROOT_ID)
        if nom in racine and racine[nom].get("md5Checksum") == md5_de(PACK_RACINE):
            return "DÉJÀ EN PLACE (md5 égal)"
        if nom in racine:
            resumable(f"https://www.googleapis.com/upload/drive/v3/files/"
                      f"{racine[nom]['id']}?uploadType=resumable", {}, PACK_RACINE)
        else:
            resumable("https://www.googleapis.com/upload/drive/v3/files"
                      "?uploadType=resumable",
                      {"name": nom, "parents": [ROOT_ID]}, PACK_RACINE)
        octets = contenu(inventaire(ROOT_ID)[nom]["id"])
        assert hashlib.md5(octets).hexdigest() == md5_de(PACK_RACINE), "recoup échoue"
        return f"posé à la racine et recoupé ({PACK_RACINE.stat().st_size:,} o)".replace(",", " ")
    geste("la racine : le pack v0.19.4", g_pack)

    # (3) l'instruction archivée
    def g_archive():
        instructions = inventaire(instructions_id)
        if nom_arch not in instructions:
            dest = inventaire(archive_id)
            if "instructions_20261119" in dest:
                if nom_arch in inventaire(dest["instructions_20261119"]["id"]):
                    return "DÉJÀ ARCHIVÉE"
            raise RuntimeError("l'instruction introuvable au /instructions")
        fid = instructions[nom_arch]["id"]
        dest = inventaire(archive_id)
        if "instructions_20261119" not in dest:
            st, body, _ = api("POST", f"{API}/files",
                              {"name": "instructions_20261119",
                               "mimeType": "application/vnd.google-apps.folder",
                               "parents": [archive_id]})
            assert st in (200, 201), (st, body[:200])
            dest = inventaire(archive_id)
        dest_id = dest["instructions_20261119"]["id"]
        # le geste Drive natif : LA VOIE DOCUMENTÉE (PATCH ?addParents/
        # removeParents) — le POST /files/{id}/parents de l'outil 5ey7gmjra
        # répond désormais 404 (l'écart nommé à la livraison du 20/11 : le
        # geste équivalent vécu, la corbeille JAMAIS — D143)
        st, body, _ = api("PATCH",
                          f"{API}/files/{fid}?addParents={dest_id}"
                          f"&fields=parents", {})
        assert st == 200, (st, body[:200])
        st, body, _ = api("GET", f"{API}/files/{fid}?fields=parents")
        parents = json.loads(body).get("parents", [])
        for p in parents:
            if p != dest_id:
                st, body, _ = api("PATCH",
                                  f"{API}/files/{fid}?removeParents={p}"
                                  f"&fields=parents", {})
                assert st == 200, (st, body[:200])
        # la preuve du geste (la leçon de la Task 202 : le 200 muet du SA n'est
        # pas une preuve — le RE-LISTING aux DEUX bords fait foi)
        assert nom_arch not in inventaire(instructions_id), "encore au /instructions"
        assert nom_arch in inventaire(dest_id), "absente de l'archive"
        return "déplacée /instructions → /ARCHIVE/instructions_20261119/"
    nom_arch = INSTRUCTION
    geste("l'archivage de l'instruction cq01qv1za", g_archive)

    verts = sum(1 for v, _ in bilan if v == "VERT")
    print(f"\nBILAN DE LA LIVRAISON : {verts}/{len(bilan)} VERT")
    if verts == len(bilan):
        print("LA LIVRAISON COMPLÈTE : le miroir, le kit, les pièces au /test, "
              "le pack à la racine, l'instruction archivée.")
    return 0 if verts == len(bilan) else 1


if __name__ == "__main__":
    sys.exit(main())
