#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_kit_unite02_d210.py — LE KIT DE L'UNITÉ 02 D210 (loupe-08
ligne × les deux bras) : kit-unite-02-d210-20261118/ au dossier de
campagne — la pièce, la notation, le brouillon, le scénario D204
INCHANGÉ, les fixtures (proxy.exe scellé, le témoin 3f), le source C +
les tests, le journal + le garde-brut, la graine, la gravure
EMPREINTES, le LISEZMOI terrain, le lanceur (CRLF conservés)."""
import hashlib
import pathlib
import shutil

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
UNITE = REPO / "scripts" / "campagne_d204" / "unite-08-T-d210"
ATELIER = pathlib.Path("/home/z/my-project/triade/lab/atelier-d210-p39uklsca")
D204 = REPO / "scripts" / "campagne_d204" / "unite-08-T" / "kit-v2"
KIT = UNITE / "kit" / "kit-unite-02-d210-20261118"


def sha(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def main() -> int:
    KIT.mkdir(parents=True, exist_ok=True)

    # 1· les pièces matérielles
    pieces = [
        (UNITE / "piece" / "loupe.exe", "loupe.exe"),
        (UNITE / "notation" / "loupe-08-ligne.asm",
         "notation-loupe-08-ligne.asm"),
        (ATELIER / "bras-T" / "loupe-08-it8.asm",
         "brouillon-loupe-08-ligne.asm"),
        (D204 / "scenario-unite08.py", "scenario-unite08.py"),
        (REPO / "tls13" / "proxy.exe", "proxy.exe"),
        (D204 / "temoin-3f.bin", "temoin-3f.bin"),
        (ATELIER / "bras-C" / "loupe-08-C-final.c", "source-loupe-08-C.c"),
        (ATELIER / "bras-C" / "tests-loupe-08-C.md", "tests-loupe-08-C.md"),
        (ATELIER / "preuves" / "journal-tokens-d210.jsonl",
         "journal-tokens-d210.jsonl"),
        (ATELIER / "preuves" / "garde-brut-d210.jsonl",
         "garde-brut-d210.jsonl"),
        (ATELIER / "GRAINE-D210.txt", "GRAINE-D210.txt"),
    ]
    for src, nom in pieces:
        shutil.copyfile(src, KIT / nom)

    # 2· le lanceur (CRLF conservés — le vécu de la 339)
    lanceur = (D204 / "LANCEUR-UNITE-08-T.bat").read_bytes()
    texte = lanceur.decode("utf-8-sig", errors="replace")
    texte = texte.replace(
        "title TRIADE - Unite 4 (loupe-08 ligne x bras T) - campagne D204",
        "title TRIADE - Unite 02 D210 (loupe-08 ligne x bras T) - "
        "campagne D210")
    texte = texte.replace(
        "rem LANCEUR — LE LANCEUR OFFICIEL du kit de l'unite 4",
        "rem LANCEUR — LE LANCEUR OFFICIEL du kit de l'unite 02 D210")
    texte = texte.replace(
        "rem (loupe-08 ligne x bras T, la campagne D204). Le run court dans SA",
        "rem (loupe-08 ligne x bras T, la campagne D210 — la deuxieme "
        "unite, la sequence tiree). Le run court dans SA")
    with open(KIT / "LANCEUR-UNITE-08-T.bat", "wb") as f:
        f.write(texte.replace("\n", "\r\n").encode("utf-8"))

    # 3· la gravure EMPREINTES (le juge du terrain recoupe à la lecture)
    lignes = [
        "EMPREINTES — LE KIT DE L'UNITÉ 02 D210 (loupe-08 ligne × bras T",
        "— la campagne D210, la deuxième unité, la séquence tirée de la "
        "graine D217)",
        "(chaque pièce sha256 — le scénario recoupe la pièce à la "
        "gravure ; une divergence, rien ne court)",
        "",
    ]
    ordre = [
        "LANCEUR-UNITE-08-T.bat", "notation-loupe-08-ligne.asm",
        "brouillon-loupe-08-ligne.asm", "loupe.exe", "proxy.exe",
        "scenario-unite08.py", "temoin-3f.bin", "source-loupe-08-C.c",
        "tests-loupe-08-C.md", "journal-tokens-d210.jsonl",
        "garde-brut-d210.jsonl", "GRAINE-D210.txt",
    ]
    for nom in ordre:
        lignes.append(f"{sha(KIT / nom)}  {nom}")
    (KIT / "EMPREINTES-KIT-UNITE-02-D210.txt").write_text(
        "\r\n".join(lignes) + "\r\n", encoding="utf-8")

    print(f"[kit] {KIT} : {len(ordre) + 1} pièces gravées")
    for nom in ordre + ["EMPREINTES-KIT-UNITE-02-D210.txt"]:
        print(f"  {sha(KIT / nom)[:16]}…  {nom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
