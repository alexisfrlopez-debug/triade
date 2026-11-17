#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zip_juge_v2_339.py — L'ASSEMBLAGE DU ZIP DE LA CORRECTION
(l'Entrée 339) : kit-gui-1clic-unite02-d210-juge-v2-20261118.zip — LE
KIT v2 (LE JUGE RÉPARÉ) au geste établi de la 337 (deflate, les
permissions 0644/0755, le dossier racine nommé du kit). Puis
L'ÉPREUVE DU ZIP : dézipage au bac temporaire, le GUI DÉZIPPÉ conduit
son PROPRE selftest (le verrou sur les octets sortis du zip), la
gravure recoupée, le juge v2 recoupé byte-byte aux archives du bac 295
(la pièce du kit == la pièce archivée — la chaîne de garde par le
contenu, D143)."""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

DL = pathlib.Path("/home/z/my-project/download")
V2 = DL / "TRIADE_gui_unite02_d210_v2"
NOM_DOSSIER = "kit-gui-1clic-unite02-d210-juge-v2-20261118"
ZIP = DL / (NOM_DOSSIER + ".zip")

# les fichiers du kit (23 : les DIX-SEPT pièces du verrou + le GUI, le
# lanceur, le livre, les DEUX correctifs — dont l'EMPREINTES-GUI v2)
FICHIERS = sorted(p.name for p in V2.iterdir() if p.is_file())


def main():
    print(f"[zip] {len(FICHIERS)} pièces au kit v2 :")
    for n in FICHIERS:
        print(f"  - {n}")

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for n in FICHIERS:
            p = V2 / n
            arc = f"{NOM_DOSSIER}/{n}"
            zi = zipfile.ZipInfo(arc, date_time=(2026, 11, 18, 20, 0, 0))
            zi.external_attr = (0o755 if p.suffix in (".bat", ".py")
                                else 0o644) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(p, "rb") as f:
                z.writestr(zi, f.read())

    taille = ZIP.stat().st_size
    print(f"[zip] {ZIP.name} né : {taille} o "
          f"({len(FICHIERS)} pièces, deflate)")

    # -- L'ÉPREUVE DU ZIP : dézipage au bac, le GUI sorti conduit son
    # propre selftest (LE CODE DÉZIPPÉ, pas la copie du labo)
    with tempfile.TemporaryDirectory(prefix="zip_v2_339_") as tmp:
        bac = pathlib.Path(tmp)
        with zipfile.ZipFile(ZIP) as z:
            noms = z.namelist()
            assert len(noms) == len(FICHIERS), \
                f"le zip porte {len(noms)} entrées, {len(FICHIERS)} attendues"
            z.extractall(bac)
        kit = bac / NOM_DOSSIER
        assert kit.is_dir(), "le dossier racine du zip inexistant"
        print(f"[épreuve] dézipé au bac : {NOM_DOSSIER}/ "
              f"({len(noms)} entrées)")

        # le juge v2 recoupé byte-byte aux archives du bac 295
        import hashlib
        h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
        arch = pathlib.Path(
            "/home/z/my-project/triade/lab/repo2/scripts/campagne_d204"
            "/depot-run-v2-T-295/epreuves/scenario-unite02-v2.py")
        ok_juge = h(kit / "scenario-unite02.py") == h(arch)
        print(f"[épreuve] le juge du zip == les archives du bac 295 "
              f"byte-byte : {'VERT (302fa3a1…)' if ok_juge else 'ROUGE'}")

        # le selftest du GUI DÉZIPPÉ (le verrou sur les octets sortis)
        r = subprocess.run(
            [sys.executable, "triade_run_unite02_d210_gui.py",
             "--selftest"], cwd=kit, capture_output=True, text=True,
            timeout=300)
        sortie = r.stdout
        verts = sortie.count("[VERT]")
        rouges = sortie.count("[ROUGE]")
        print(f"[épreuve] le selftest du GUI DÉZIPPÉ : {verts} VERT, "
              f"{rouges} ROUGE (code {r.returncode})")

    ok = ok_juge and verts == 15 and rouges == 0 and r.returncode == 0
    print(f"[zip] L'ÉPREUVE {'VERT — le zip porte le kit v2 entier, le juge recoupé' if ok else 'ROUGE'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
