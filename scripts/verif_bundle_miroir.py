#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_bundle_miroir.py — re-vérification sur pièces du bundle courant du
miroir Drive (lecture seule) : téléchargement, md5 recoupé à la métadonnée,
git bundle list-heads + verify (la branche MAIN du bundle == la pointe du
dépôt local — la branche canonique du miroir depuis D141 ; la branche jalon
bundle051/v0.5.1-jalon-v7 était l'artefact de l'époque v0.5.1, figée à
9888d06, elle n'a jamais bougé depuis — comparée à la pointe elle rendait
un ÉCHEC faux ; corrigé à la session du 12/11, Entrée 232/D199).
Usage : python3 scripts/verif_bundle_miroir.py <nom-du-bundle>"""
import hashlib
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import drive_sync as ds  # noqa: E402

REPO = "/home/z/my-project/triade"


def main(nom: str) -> int:
    coffre = ds.list_folder(ds.DRIVE_ROOT_ID)
    miroir = coffre["TRIADE-sauvegarde-git"]
    racine = ds.list_folder(miroir["id"])
    f = racine.get(nom) or sys.exit(f"[verif] {nom} introuvable au miroir")
    md5_meta = f.get("md5Checksum", "")
    print(f"[verif] métadonnée Drive : md5 {md5_meta}")
    url = ds.API + f"/files/{f['id']}?alt=media"
    req = urllib.request.Request(
        url, headers={"Authorization": "Bearer " + ds.get_access_token()})
    with urllib.request.urlopen(req, timeout=300) as r:
        donnees = r.read()
    chemin = "/tmp/" + nom
    with open(chemin, "wb") as out:
        out.write(donnees)
    md5_local = hashlib.md5(donnees).hexdigest()
    print(f"[verif] téléchargé : {len(donnees)} o, md5 {md5_local}"
          f" — {'MATCH' if md5_local == md5_meta else 'DIVERGEANT'}")
    if md5_local != md5_meta:
        return 1
    tetes = subprocess.run(["git", "bundle", "list-heads", chemin],
                           cwd=REPO, capture_output=True, text=True).stdout
    print("[verif] têtes :")
    for ligne in tetes.splitlines():
        print("        " + ligne)
    verif = subprocess.run(["git", "bundle", "verify", chemin], cwd=REPO,
                           capture_output=True, text=True)
    ok = verif.returncode == 0
    print(f"[verif] git bundle verify : "
          f"{'VALIDE' if ok else 'INVALIDE — ' + verif.stderr[:200]}")
    pointe = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    ligne_main = next((l for l in tetes.splitlines()
                       if l.endswith("refs/heads/main")),
                      "")
    ok_pointe = ligne_main.startswith(pointe)
    print(f"[verif] la branche main du bundle "
          f"{'==' if ok_pointe else '≠'} la pointe locale {pointe[:7]}")
    print(f"[verif] VERDICT : {'VERT — le miroir porte la pointe du dépôt' if ok and ok_pointe else 'ÉCHEC'}")
    return 0 if (ok and ok_pointe) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else
                  "triade-history.bundle"))
