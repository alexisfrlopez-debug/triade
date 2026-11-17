#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zip_unite08_342.py — L'ASSEMBLAGE DU ZIP DU GUI 1-CLIC DE
L'UNITÉ 02 D210 (l'Entrée 342) : kit-gui-1clic-unite08-d210-20261118.zip
— LE KIT GUI (18 pièces) au geste établi de la 337/339 (deflate, les
permissions 0644/0755) ; LE DOSSIER RACINE PORTE LE NOM DU KIT —
kit-unite-02-d210-20261118 — le pas « 1·KIT : CHOISIR CE DOSSIER » du
livre du kit se vit AU DOUBLE-CLIC : le terrain dézippe, voilà LE
dossier daté nommé, le lanceur y attend (le kit et le GUI vivent au
MÊME dossier, le GUI le recoupe LUI-MÊME à chaque lancement — sans
aucun autre choix).

Puis L'ÉPREUVE DU ZIP : dézipage au bac temporaire, le juge du zip ==
le kit du labo OCTET POUR OCTET (scenario-unite08.py, loupe.exe, la
gravure), le GUI DÉZIPPÉ conduit son PROPRE selftest (le verrou sur
les octets sortis du zip : 15 VERT, 0 ROUGE)."""
import hashlib
import pathlib
import subprocess
import sys
import tempfile
import zipfile

DL = pathlib.Path("/home/z/my-project/download")
KIT = DL / "TRIADE_gui_unite08_d210_v1"
BAC = pathlib.Path("/home/z/my-project/triade/lab/repo2/scripts"
                    "/campagne_d204/unite-08-T-d210/kit"
                    "/kit-unite-02-d210-20261118")
NOM_DOSSIER = "kit-unite-02-d210-20261118"
ZIP = DL / "kit-gui-1clic-unite08-d210-20261118.zip"

# les fichiers du kit (18 : les QUATORZE pièces du verrou + le GUI,
# le lanceur, le livre + l'EMPREINTES-GUI — les résidus du labo
# [__pycache__, l'état, les logs] JAMAIS au zip)
FICHIERS = sorted(p.name for p in KIT.iterdir() if p.is_file())


def h(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    print(f"[zip] {len(FICHIERS)} pièces au kit GUI :")
    for n in FICHIERS:
        print(f"  - {n}")

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for n in FICHIERS:
            p = KIT / n
            arc = f"{NOM_DOSSIER}/{n}"
            zi = zipfile.ZipInfo(arc, date_time=(2026, 11, 18, 21, 0, 0))
            zi.external_attr = (0o755 if p.suffix in (".bat", ".py")
                                else 0o644) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(p, "rb") as f:
                z.writestr(zi, f.read())

    taille = ZIP.stat().st_size
    print(f"[zip] {ZIP.name} né : {taille} o "
          f"({len(FICHIERS)} pièces, deflate, la racine "
          f"{NOM_DOSSIER}/)")

    # -- L'ÉPREUVE DU ZIP : dézipage au bac, les octets sortis font foi
    with tempfile.TemporaryDirectory(prefix="zip_u08_342_") as tmp:
        bac = pathlib.Path(tmp)
        with zipfile.ZipFile(ZIP) as z:
            noms = z.namelist()
            assert len(noms) == len(FICHIERS), \
                f"le zip porte {len(noms)} entrées, {len(FICHIERS)} attendues"
            racines = {n.split("/")[0] for n in noms}
            assert racines == {NOM_DOSSIER}, \
                f"la racine du zip diverge : {racines}"
            z.extractall(bac)
        kit = bac / NOM_DOSSIER
        assert kit.is_dir(), "le dossier racine du zip inexistant"
        print(f"[épreuve] dézipé au bac : {NOM_DOSSIER}/ "
              f"({len(noms)} entrées, la racine du KIT)")

        # le juge du zip == le kit du labo OCTET POUR OCTET (la chaîne
        # de garde par le contenu, D143) : le scénario, la pièce, la
        # gravure, le doré, le témoin 3f
        for piece in ("scenario-unite08.py", "loupe.exe",
                      "EMPREINTES-KIT-UNITE-02-D210.txt", "proxy.exe",
                      "temoin-3f.bin"):
            ok = h(kit / piece) == h(BAC / piece)
            print(f"[épreuve] {piece} == le kit du labo byte-byte : "
                  f"{'VERT' if ok else 'ROUGE'}")
            if not ok:
                return 1

        # le selftest du GUI DÉZIPPÉ (le verrou sur les octets sortis)
        r = subprocess.run(
            [sys.executable, "triade_run_unite08_d210_gui.py",
             "--selftest"], cwd=kit, capture_output=True, text=True,
            timeout=300)
        sortie = r.stdout
        verts = sortie.count("[VERT]")
        rouges = sortie.count("[ROUGE]")
        print(f"[épreuve] le selftest du GUI DÉZIPPÉ : {verts} VERT, "
              f"{rouges} ROUGE (code {r.returncode})")

    ok = verts == 15 and rouges == 0 and r.returncode == 0
    verdict = ("VERT — le zip porte le kit GUI entier, le juge recoupé "
               "byte-byte au kit du labo" if ok else "ROUGE")
    print(f"[zip] L'ÉPREUVE {verdict}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
