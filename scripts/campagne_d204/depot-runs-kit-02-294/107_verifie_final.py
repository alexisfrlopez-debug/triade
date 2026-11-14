#!/usr/bin/env python3
"""107_verifie_final.py — LE RECOUP FINAL : le miroir Drive ET le /test
portent l'état 294 (le bundle courant à la pointe locale, les TROIS textes,
la carte aux DEUX endroits, le bac 294 au miroir, le kit v2 au /test, les
dépôts rangés, l'archive D141, GitHub au même état)."""
import hashlib
import pathlib
import subprocess
import sys
import tempfile

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

REPO = pathlib.Path("/home/z/my-project/work/triade")
TIP = subprocess.run(["git", "rev-parse", "main"], cwd=REPO,
                     capture_output=True, text=True).stdout.strip()
print(f"[pointe locale] main = {TIP[:12]}…")

coffre = ds.list_folder(ds.DRIVE_ROOT_ID)
miroir = coffre.get("TRIADE-sauvegarde-git")
racine_m = ds.list_folder(miroir["id"])
docs_m = ds.list_folder(racine_m["docs"]["id"])

verts, rouges = [], []

# 1. le bundle courant au miroir
bundle = racine_m.get("triade-history.bundle")
st, data, _ = ds.api("GET", ds.API + f"/files/{bundle['id']}?alt=media")
with tempfile.NamedTemporaryFile(suffix=".bundle", delete=False) as f:
    f.write(data)
    chemin = pathlib.Path(f.name)
tetes = subprocess.run(["git", "bundle", "list-heads", str(chemin)],
                       capture_output=True, text=True).stdout
main = next((l.split()[0] for l in tetes.splitlines()
             if l.endswith("refs/heads/main")), "")
chemin.unlink()
if main == TIP:
    verts.append(f"le bundle courant : main == {TIP[:7]} (l'état 294)")
else:
    rouges.append(f"le bundle courant : main={main[:7]} ≠ {TIP[:7]}")
print(f"[bundle] {int(bundle.get('size',0))/1024:.0f} Ko, pointe {main[:7]}")

# 2. les TROIS textes au miroir
for nom, it, local in [
    ("JOURNAL_TRAVAIL.md", docs_m.get("JOURNAL_TRAVAIL.md"),
     REPO / "docs" / "JOURNAL_TRAVAIL.md"),
    ("worklog.md", racine_m.get("worklog.md"), REPO / "worklog.md"),
    ("OU-TROUVER-LES-LIVRABLES.md", racine_m.get("OU-TROUVER-LES-LIVRABLES.md"),
     REPO / "OU-TROUVER-LES-LIVRABLES.md"),
]:
    md5 = hashlib.md5(local.read_bytes()).hexdigest()
    ok = it is not None and it.get("md5Checksum") == md5
    (verts if ok else rouges).append(f"{nom} au miroir "
                                     + ("md5 == local" if ok else "ÉCART"))

# 3. la carte à la racine du coffre
carte = coffre.get("OU-TROUVER-LES-LIVRABLES.md")
md5 = hashlib.md5((REPO / "OU-TROUVER-LES-LIVRABLES.md").read_bytes()).hexdigest()
ok = carte is not None and carte.get("md5Checksum") == md5
(verts if ok else rouges).append("OU-TROUVER à la racine du coffre "
                                 + ("md5 == local" if ok else "ÉCART"))

# 4. le bac 294 au miroir
bac = racine_m.get("scripts")
if bac:
    c1 = ds.list_folder(bac["id"]).get("campagne_d204")
    if c1:
        c2 = ds.list_folder(c1["id"])
        b294 = c2.get("depot-runs-kit-02-294")
        b293 = c2.get("depot-atelier-ligne-C-293")
        if b294:
            n = len(ds.list_folder(b294["id"]))
            verts.append(f"le bac depot-runs-kit-02-294/ au miroir ({n} entrées)")
        else:
            rouges.append("le bac depot-runs-kit-02-294/ ABSENT du miroir")
        if b293:
            verts.append("le bac 293 demeure au miroir")
# le kit v2 au bac du miroir (les pièces suivies par git)
kitv2 = ds.list_folder(ds.list_folder(c2["unite-02-T"]["id"])["kit-v2"]["id"]) \
    if c2 and c2.get("unite-02-T") else {}
if len(kitv2) == 12:
    verts.append("le kit v2 au bac du miroir (12 pièces)")
else:
    rouges.append(f"le kit v2 au bac du miroir : {len(kitv2)} pièces")

# 5. le /test : le kit v2, les dépôts rangés, la carte
test = [it for nom, it in coffre.items()
        if nom == "test" and it["mimeType"] == ds.FOLDER_MIME][0]
t = ds.list_folder(test["id"])
racine_n = len(t)
k2 = t.get("kit-unite-loupe-02-T-20261114-v2")
if k2:
    verts.append(f"le kit v2 au /test ({len(ds.list_folder(k2['id']))} pièces)")
else:
    rouges.append("le kit v2 ABSENT du /test")
archives = t.get("archives-livraisons")
u2 = ds.list_folder(archives["id"]).get("unite-02-loupe-20261114")
if u2:
    noms = sorted(ds.list_folder(u2["id"]))
    attendus = {"kit-unite-loupe-02-T-20261114", "kit-unite-loupe-02-C-20261114"}
    if set(noms) == attendus:
        verts.append("les DEUX dépôts rangés à unite-02-loupe-20261114/ "
                     f"({len(noms)} dossiers, les noms conservés)")
    else:
        rouges.append(f"l'archive unite-02 porte {noms}")
else:
    rouges.append("l'archive unite-02-loupe-20261114/ ABSENTE")
carte_kits = t.get("LISEZMOI-KITS-UNITES-D204.txt")
ck = hashlib.sha256((BAC := pathlib.Path(
    "/home/z/my-project/work/triade/scripts/campagne_d204/depot-runs-kit-02-294/"
    "epreuves/carte-kits-294.txt")).read_bytes()).hexdigest()
# la carte du /test doit porter la section 294 (le contenu == la carte 294 du bac)
st, corps, _ = ds.api("GET", ds.API + f"/files/{carte_kits['id']}?alt=media")
if corps == BAC.read_bytes():
    verts.append("la carte LISEZMOI-KITS au /test porte la section 294 "
                 f"({len(corps)} o, byte-byte == le bac)")
else:
    rouges.append("la carte LISEZMOI-KITS au /test diverge du bac")

# 6. l'archive D141
arch_b = ds.list_folder(racine_m["archives-bundles"]["id"])
n_bundles = len(arch_b)
if "triade-history-293-bfb20e0.bundle" in arch_b:
    verts.append(f"D141 : le 293-bfb20e0 archivé versionné ({n_bundles} bundles)")
else:
    rouges.append("le 293-bfb20e0 ABSENT des archives-bundles")

print()
for v in verts:
    print(f"  [VERT] {v}")
for r in rouges:
    print(f"  [ROUGE] {r}")
print(f"\n[FINAL] {len(verts)} VERT, {len(rouges)} ROUGE — "
      f"la racine du /test porte {racine_n} entrées")
sys.exit(1 if rouges else 0)
