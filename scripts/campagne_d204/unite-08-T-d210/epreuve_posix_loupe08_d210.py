#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""epreuve_posix_loupe08_d210.py — LE CONTRAT REJOUÉ AU POSIX contre la
pièce C même (l'unité 02 D210, loupe-08 × bras C). Le source PUR ISO C
compile en objet partagé au gcc du labo (gcc -O2 -shared -fPIC — la
feuille pure n'exige ni shim ni mingw : la DLL au terrain se construit
par x86_64-w64-mingw32-gcc, la commande consignée au LISEZMOI), l'export
loupe_08_ligne APPELÉ NATURELLEMENT — le juge est le MODÈLE
INDÉPENDANT (le miroir de l'oracle du bras T : les MÊMES vecteurs, la
MÊME graine 20261115, les MÊMES tirages).

  V1 le doré : la première ligne de proxy.exe scellé + la ligne finale
     incomplète du témoin 3 × 64 Kio + 1 (Q1-Q4) ;
  V2 le différentiel : 10 000 lignes (la graine 20261115), la sortie ==
     le modèle OCTET PAR OCTET, le poison au-delà de 77 INTACT (I2), la
     source LUE SEULE (I3) ;
  V3 les rejets : longueur 0 / 17, source nulle, sortie nulle → -5, la
     sortie POISON INTACTE (E1/E2/E3) ;
  V4 la falsification : le source muté (la table décalée d'un octet —
     chaque ligne diverge) — le juge attrape la pièce fausse (charte § 3).
"""
import ctypes
import hashlib
import os
import pathlib
import random
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
ATELIER = pathlib.Path(
    "/home/z/my-project/triade/lab/atelier-d210-p39uklsca/bras-C")
REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
PROXY = REPO / "tls13" / "proxy.exe"
GRAINE = 20261115
POISON = b"\xCC"

VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def modele_ligne(decalage: int, octets: bytes) -> bytes:
    s = f"{decalage:08X}  "
    g = [f"{b:02X}" if i < len(octets) else "  "
         for i, b in enumerate(octets + b"\x00" * (16 - len(octets)))]
    s += " ".join(g[:8]) + "  " + " ".join(g[8:]) + "  "
    miroir = "".join(chr(b) if 0x20 <= b <= 0x7E else "."
                     for b in octets[:16])
    s += miroir + " " * (16 - len(miroir))
    return s.encode("latin-1") + b"\x00"          # 77 o exacts


def compiler(source: pathlib.Path, sortie: pathlib.Path) -> None:
    r = subprocess.run(
        ["gcc", "-O2", "-std=c11", "-Wall", "-Wextra", "-shared", "-fPIC",
         "-o", str(sortie), str(source)],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr)
        sys.exit(f"[!] la compilation refuse : {r.stderr[:300]}")


def charger(chemin: pathlib.Path):
    lib = ctypes.CDLL(str(chemin))
    lib.loupe_08_ligne.restype = ctypes.c_longlong
    lib.loupe_08_ligne.argtypes = [
        ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_char_p,
        ctypes.c_ulonglong]
    return lib.loupe_08_ligne


def composer(fn, source: bytes, longueur: int, decalage: int):
    sortie = ctypes.create_string_buffer(POISON * 96)
    r = fn(source, longueur, sortie, decalage)
    return r, sortie.raw[:96]


def main() -> int:
    print("=== L'ÉPREUVE POSIX — l'unité 02 D210 (loupe-08 × bras C) : "
          "les vecteurs du contrat, le juge = le modèle indépendant ===")
    so = ICI / "epreuves" / "loupe-08-c.so"
    so.parent.mkdir(exist_ok=True)
    compiler(ATELIER / "loupe-08-C-final.c", so)
    fn = charger(so)
    m9 = PROXY.read_bytes()
    if hashlib.sha256(m9).hexdigest() != \
            "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d":
        sys.exit("[!] proxy.exe scellé divergent")

    # ---- V1 : le doré --------------------------------------------------------
    r, ligne = composer(fn, m9[:16], 16, 0)
    attendu = modele_ligne(0, m9[:16])
    controle("V1:le-dore-proxy-premiere-ligne",
             r == 0 and ligne[:77] == attendu and ligne[77:] == POISON * 19,
             f"les 77 o == le modèle (« {attendu[:34].decode('latin-1')}… »)")

    rng_t = random.Random(20261117)
    temoin3f = rng_t.randbytes(3 * 65536 + 1)
    r, ligne = composer(fn, temoin3f[-1:], 1, 3 * 65536)
    attendu = modele_ligne(3 * 65536, temoin3f[-1:])
    controle("V1:le-témoin-3f-ligne-finale-incomplète",
             r == 0 and ligne[:77] == attendu and ligne[77:] == POISON * 19,
             "UN octet valide : quinze groupes d'espaces, la colonne "
             "ASCII droite — Q3")

    # ---- V2 : le différentiel 10 000 -----------------------------------------
    rng = random.Random(GRAINE)
    ecarts, ecarts_poison = 0, 0
    for _ in range(10_000):
        decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
        longueur = rng.randrange(1, 17)
        source = bytes(rng.randrange(0, 100) % 256 for _ in range(16))
        r, ligne = composer(fn, source, longueur, decalage)
        attendu = modele_ligne(decalage, source[:longueur])
        if ligne[:77] != attendu or r != 0:
            ecarts += 1
        if ligne[77:] != POISON * 19:
            ecarts_poison += 1
    controle("V2:le-différentiel-10-000-lignes", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle")
    controle("V2:exactement-77-o", ecarts_poison == 0,
             "le poison au-delà de 77 demeure (I2 : jamais un de plus)")

    # ---- V3 : les rejets ------------------------------------------------------
    for nom, args in (
            ("E1:la-longueur-nulle", (b"ABCDE", 0)),
            ("E2:la-longueur-dix-sept", (b"A" * 17, 17)),
            ("E3:la-source-nulle", (None, 5)),
            ("E3:la-sortie-nulle", (b"ABCDE", 5))):
        sortie = ctypes.create_string_buffer(POISON * 96)
        src, ln = args
        r = fn(src, ln, sortie if nom != "E3:la-sortie-nulle" else None, 0)
        intact = sortie.raw[:96] == POISON * 96
        controle(f"V3:{nom}", r == -5 and intact,
                 f"verdict {r}, la sortie POISON INTACTE")

    # ---- V4 : la falsification — la table décalée ---------------------------
    texte = (ATELIER / "loupe-08-C-final.c").read_text(encoding="utf-8")
    cible = 'static const char hex_chars[] = "0123456789ABCDEF";'
    if texte.count(cible) != 1:
        sys.exit("[!] la table introuvable à la pièce C")
    mut = ATELIER / "loupe-08-C-mut.c"
    mut.write_text(texte.replace(
        cible, 'static const char hex_chars[] = "123456789ABCDEF";'), encoding="utf-8")
    so_mut = ICI / "epreuves" / "loupe-08-c-mut.so"
    compiler(mut, so_mut)
    fn_mut = charger(so_mut)
    rng = random.Random(GRAINE)
    pris = 0
    for _ in range(200):
        decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
        longueur = rng.randrange(1, 17)
        source = bytes(rng.randrange(0, 256) for _ in range(16))
        r, ligne = composer(fn_mut, source, longueur, decalage)
        if ligne[:77] != modele_ligne(decalage, source[:longueur]):
            pris += 1
    controle("V4:la-table-décalée-attrapée", pris == 200,
             "les 200 lignes du mutant DIVERGENT du modèle — la "
             "falsification DÉTECTABLE (la table ne bouge jamais, la "
             "faute si)")
    r, ligne = composer(fn, m9[:16], 16, 0)
    controle("V4:la-pièce-juste-rejouée", r == 0
             and ligne[:77] == modele_ligne(0, m9[:16]),
             "la pièce redevenue la même — le vert rendu au retrait")

    print(f"\n=== L'ÉPREUVE POSIX {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
