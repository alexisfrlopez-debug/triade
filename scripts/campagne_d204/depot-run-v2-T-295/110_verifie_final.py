#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""110_verifie_final.py — LE RECOUP FINAL 295 : les NEUF points VERT de la
session (le dépôt rangé, la carte au /test, le kit v2, le livre, le miroir
— le courant bundle à la pointe 295, les TROIS textes, le bac, D141 aux
archives — et GitHub à la pointe)."""
import hashlib
import subprocess
import sys

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

REPO = "/home/z/my-project/work/triade"
rapport = []


def note(num, vert, texte):
    ligne = f"{'VERT' if vert else 'ROUGE'} {num}: {texte}"
    print(ligne)
    rapport.append(ligne)


def sub(folder_id, name):
    for nom, it in ds.list_folder(folder_id).items():
        if nom == name and it["mimeType"] == ds.FOLDER_MIME:
            return it
    return None


coffre = ds.list_folder(ds.DRIVE_ROOT_ID)
test = coffre.get("test")

# 1. le dépôt rangé
u2 = sub(sub(test["id"], "archives-livraisons")["id"], "unite-02-loupe-20261114")
copie = sub(u2["id"], "preuves-unite02")
md5 = ds.list_folder(copie["id"]).get("temoin-unite02.txt", {}).get("md5Checksum", "") \
    if copie else ""
racine_sans = sub(test["id"], "preuves-unite02") is None
note(1, copie is not None and md5 == "02a5d7fce14f865dfd6470f44d479210" and racine_sans,
     f"preuves-unite02/ rangé à l'archive (temoin-unite02.txt md5 {md5[:8]}… == 02a5d7fc…, "
     f"la racine du /test sans le dépôt) — D143 tenu")

# 2. la carte au /test
carte = ds.list_folder(test["id"]).get("LISEZMOI-KITS-UNITES-D204.txt")
st, octets, _ = ds.api("GET", ds.API + f"/files/{carte['id']}?alt=media")
sha = hashlib.sha256(octets).hexdigest()
note(2, len(octets) == 15448 and sha.startswith("c6f22126")
        and octets.decode("utf-8-sig").startswith("LISEZMOI-KITS-UNITES-D204")
        and "Entrée 295" in octets.decode("utf-8-sig"),
     f"la carte LISEZMOI-KITS au /test : {len(octets)} o, sha256 {sha[:8]}… — "
     f"la 294 en tête, la section 295 en queue")

# 3. le kit v2 demeure au /test (la pièce intacte)
v2 = sub(test["id"], "kit-unite-loupe-02-T-20261114-v2")
st, exe, _ = ds.api("GET", ds.API + f"/files/{ds.list_folder(v2['id'])['loupe.exe']['id']}?alt=media")
note(3, hashlib.sha256(exe).hexdigest().startswith("98354ff6"),
     f"kit-unite-loupe-02-T-20261114-v2/ au /test, loupe.exe re-haché "
     f"{hashlib.sha256(exe).hexdigest()[:8]}… == la gravure (le kit demeure, D143)")

# 4. le livre : les DEUX lignes de loupe-01 seules (l'unité 2 attend son geste)
atelier = sub(sub(sub(test["id"], "archives-livraisons")["id"],
                  "unite-01-loupe-20261114")["id"],
              "atelier-campagne-d204-20261114-013520")
st, livre, _ = ds.api("GET", ds.API + f"/files/{ds.list_folder(atelier['id'])['livraisons.csv']['id']}?alt=media")
lignes = [l for l in livre.decode("utf-8").splitlines() if l and not l.startswith("#")]
note(4, len(lignes) == 3 and "T-loupe-01-it1" in lignes[1] and "C-loupe-01-it1" in lignes[2],
     f"le livre (atelier 013520) : {len(lignes)-1} lignes de livraison (loupe-01 T et C seules) — "
     f"C-loupe-02-it1 et T-loupe-02-it1 attendent le geste de l'onglet 5")

# 5. le miroir : le courant bundle à la pointe 295
miroir = coffre.get("TRIADE-sauvegarde-git")
courant = ds.list_folder(miroir["id"]).get("triade-history.bundle")
st, octets_b, _ = ds.api("GET", ds.API + f"/files/{courant['id']}?alt=media")
import tempfile, pathlib
with tempfile.NamedTemporaryFile(suffix=".bundle", delete=False) as f:
    f.write(octets_b)
    chemin = pathlib.Path(f.name)
tetes = subprocess.run(["git", "bundle", "list-heads", str(chemin)],
                       capture_output=True, text=True).stdout
chemin.unlink()
main_b = next((l.split()[0] for l in tetes.splitlines() if l.endswith("refs/heads/main")), "")
local = subprocess.run(["git", "rev-parse", "main"], cwd=REPO,
                       capture_output=True, text=True).stdout.strip()
note(5, main_b == local == "444876b39c5d" + main_b[7:] or main_b == local,
     f"le miroir : le courant bundle à la pointe {main_b[:7]} == le local {local[:7]} (l'état 295)")

# 6. les TROIS textes au miroir
for nom, chemin_repo in (("OU-TROUVER-LES-LIVRABLES.md", "OU-TROUVER-LES-LIVRABLES.md"),
                         ("worklog.md", "worklog.md"),
                         ("JOURNAL_TRAVAIL.md", "docs/JOURNAL_TRAVAIL.md")):
    r = ds.list_folder(miroir["id"]).get(nom) if nom != "JOURNAL_TRAVAIL.md" \
        else ds.list_folder(sub(miroir["id"], "docs")["id"]).get(nom)
    st, corps, _ = ds.api("GET", ds.API + f"/files/{r['id']}?alt=media")
    local_txt = open(f"{REPO}/{chemin_repo}", "rb").read()
    ok = corps == local_txt
    note(6, ok, f"le miroir : {nom} {'==' if ok else '!='} le local "
                f"({len(corps)} o {'MATCH byte-byte' if ok else 'DIVERGE'})")

# 7. le bac 295 au miroir
bac = sub(sub(sub(miroir["id"], "scripts")["id"], "campagne_d204")["id"],
          "depot-run-v2-T-295")
n_bac = len(ds.list_folder(bac["id"])) if bac else 0
note(7, bac is not None and n_bac >= 5,
     f"le bac depot-run-v2-T-295/ au miroir : {n_bac} entrées (les outils + les epreuves/)")

# 8. D141 : l'archive versionnée
archives = ds.list_folder(sub(miroir["id"], "archives-bundles")["id"])
arch = archives.get("triade-history-294-be7f948.bundle")
note(8, arch is not None and arch.get("md5Checksum", "").startswith("1b39fb56"),
     f"D141 : triade-history-294-be7f948.bundle aux archives "
     f"(md5 {arch.get('md5Checksum', '')[:8]}…, {len(archives)} bundles)")

# 9. GitHub à la pointe (le jeton du relais, JAMAIS imprimé — GIT_ASKPASS)
import os, re, tempfile
tokens_dir = coffre.get("Tokens")
tg = ds.list_folder(tokens_dir["id"]).get("token_git.txt")
st, corps, _ = ds.api("GET", ds.API + f"/files/{tg['id']}?alt=media")
jeton = re.search(r"(ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+)",
                  corps.decode("utf-8", errors="replace")).group(1)
f = tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False)
f.write("#!/bin/sh\ncase \"$1\" in\n  Username*) echo triade-labo ;;\n"
        "  *) echo \"$TRIADE_JETON\" ;;\nesac\n")
f.close()
os.chmod(f.name, 0o700)
env = dict(os.environ, TRIADE_JETON=jeton, GIT_ASKPASS=f.name,
           GIT_TERMINAL_PROMPT="0")
push_ok = subprocess.run(["git", "ls-remote", "https://github.com/alexisfrlopez-debug/triade.git",
                          "refs/heads/main"], cwd=REPO, env=env, capture_output=True, text=True)
os.unlink(f.name)
tip = push_ok.stdout.split()[0] if push_ok.stdout else ""
note(9, push_ok.returncode == 0 and tip == local,
     f"GitHub : main @ {tip[:12]}… == le local (le push de la session, recoupé au ls-remote)")

print()
verts = sum(1 for l in rapport if l.startswith("VERT"))
print(f"=== LE RECOUP FINAL 295 : {verts}/{len(rapport)} VERT ===")
pathlib.Path(f"{REPO}/scripts/campagne_d204/depot-run-v2-T-295/"
             "RECOUP-FINAL-295.txt").write_text(
    "LE RECOUP FINAL 295 — " + f"{verts}/{len(rapport)} VERT\n" + "=" * 60 + "\n\n"
    + "\n".join(rapport) + "\n", encoding="utf-8")
sys.exit(0 if verts == len(rapport) else 2)
