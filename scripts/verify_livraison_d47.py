#!/usr/bin/env python3
"""verify_livraison_d47.py — vérifie que les livrables de l'étape (b) M3 sont
présents et identiques : (1) fichiers clés du miroir Drive (TRIADE/m3/…),
(2) proxy.exe + LISEZMOI-proxy.txt au coffre racine et au dossier test.
Réutilise l'authentification et le listing de drive_sync.py."""
import hashlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import drive_sync as ds  # noqa: E402

REPO = ds.REPO


def md5_local(rel: str) -> str:
    return hashlib.md5((REPO / rel).read_bytes()).hexdigest()


def sous_dossier(nom, parent_id):
    for nom_d, meta in ds.list_folder(parent_id).items():
        if nom_d == nom and meta.get("mimeType") == ds.FOLDER_MIME:
            return meta["id"]
    return None


def verifier_dossier(dossier_id, chemin_local: str, etiquettes: dict):
    """étiquettes : {nom_fichier: chemin_local_relatif ou None (même nom)}"""
    listing = {n: m for n, m in ds.list_folder(dossier_id).items()
               if m.get("mimeType") != ds.FOLDER_MIME}
    ok = 0
    for nom, rel in etiquettes.items():
        if nom not in listing:
            print(f"  ABSENT : {nom}")
            continue
        distant = listing[nom].get("md5Checksum", "?")
        local = md5_local(rel or f"{chemin_local}/{nom}")
        etat = "MATCH" if distant == local else "DIVERGENT"
        ok += etat == "MATCH"
        print(f"  {nom} : md5 distant {distant[:8]}… {etat}")
    return ok, len(etiquettes)


def main():
    triade = sous_dossier("TRIADE", ds.DRIVE_ROOT_ID)
    assert triade, "dossier TRIADE introuvable"
    m3 = sous_dossier("m3", triade)
    assert m3, "dossier m3 absent du miroir"
    notation = sous_dossier("notation", m3)
    carte = sous_dossier("carte", m3)
    assert notation and carte, "m3/notation ou m3/carte absent du miroir"

    print("[miroir] m3/ (fichiers clés de l'étape b) :")
    cles = {"proxy.exe": "m3/proxy.exe", "build_m3.py": "m3/build_m3.py",
            "oracle_m3.py": "m3/oracle_m3.py", "layout.py": "m3/layout.py",
            "carte_m3.py": "m3/carte_m3.py"}
    a, b = verifier_dossier(m3, "m3", cles)
    print("[miroir] m3/notation/ (13 notations) :")
    notations = {f"http-{i:02d}-{n}.asm": None for i, n in enumerate(
        ["ligne", "requete", "entete", "chercher", "nombre", "tete",
         "autorite", "cible", "pompe", "session", "console", "principal"], 1)}
    notations["tcp-13-connexion.asm"] = None
    a2, b2 = verifier_dossier(notation, "m3/notation", notations)
    print("[miroir] m3/carte/ (génération 5) :")
    fragments = {f: None for f in ["frag-bld.bin", "frag-con.bin", "frag-loc.bin",
                                   "frag-prf.bin", "carte.sig", "header.txt",
                                   "tableau-de-bord.txt", "cle-publique.ed25519"]}
    a3, b3 = verifier_dossier(carte, "m3/carte", fragments)

    print("[coffre racine] livrables terrain (enfants directs du coffre) :")
    a4, b4 = verifier_dossier(ds.DRIVE_ROOT_ID, ".", {"proxy.exe": "m3/proxy.exe",
                                                    "LISEZMOI-proxy.txt": "LISEZMOI-proxy.txt"})
    print("[dossier test] livrables terrain :")
    test = sous_dossier("test", ds.DRIVE_ROOT_ID)
    a5, b5 = verifier_dossier(test, ".", {"proxy.exe": "m3/proxy.exe",
                                          "LISEZMOI-proxy.txt": "LISEZMOI-proxy.txt"})

    total, attendu = a + a2 + a3 + a4 + a5, b + b2 + b3 + b4 + b5
    print(f"[bilan] {total}/{attendu} fichiers vérifiés MATCH")
    return 0 if total == attendu else 1


if __name__ == "__main__":
    sys.exit(main())
