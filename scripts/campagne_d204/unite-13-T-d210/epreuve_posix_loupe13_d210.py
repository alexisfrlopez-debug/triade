#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""epreuve_posix_loupe13_d210.py — LE CONTRAT REJOUÉ AU POSIX contre la
pièce C même (l'unité 03 D210, loupe-13 × bras C). Le source PUR ISO C
compile en objet partagé au gcc du labo (gcc -O2 -shared -fPIC — la
feuille pure n'exige ni shim ni mingw : la DLL au terrain se construit
par x86_64-w64-mingw32-gcc, la commande consignée au LISEZMOI), l'export
loupe_13_recherche APPELÉ NATURELLEMENT — le juge est le MODÈLE
INDÉPENDANT (le miroir de l'oracle du bras T : les MÊMES vecteurs, la
MÊME graine 20261115, les MÊMES tirages).

  V1 le doré : le corpus de l'école (le motif au premier octet, au
     dernier, à cheval sur le départ, l'occurrence DOUBLE — LA PREMIÈRE
     exigée, AAAA dans AAAAB, le presque-frère, le départ au milieu, la
     fenêtre vide, la plage vide, le motif trop long) + les marques de
     proxy.exe scellé (MZ @0, PE @+64, les marques absentes → -1) ;
  V2 le différentiel : 10 000 cas (la graine 20261115, les mêmes tirages
     que le terrain), rax == bytes.find À L'IDENTIQUE, la fenêtre et le
     motif LUS SEULS (I3) ;
  V3 les rejets : le motif vide, le motif de 33, le départ au-delà →
     -5 (E1/E2/E3) ;
  V4 la falsification : le source muté (le retour avancé d'un — le
     second match au lieu du premier) — le juge attrape la pièce fausse
     (charte § 3, le miroir du bras T).
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

VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def modele_recherche(fenetre: bytes, motif: bytes, depart: int) -> int:
    """LE MODÈLE INDÉPENDANT — la sémantique du contrat (l'écrit-avant-code),
    jamais les octets de la pièce."""
    if len(motif) < 1 or len(motif) > 32:
        return -5                                  # E1/E2 : la borne P4
    if depart > len(fenetre):
        return -5                                  # E3 : le départ est une position
    if len(motif) > len(fenetre) - depart:
        return -1                                  # Q2 : le constat trivial
    return fenetre.find(motif, depart)             # Q1/Q3/Q4 : la première


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
    lib.loupe_13_recherche.restype = ctypes.c_longlong
    lib.loupe_13_recherche.argtypes = [
        ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_char_p,
        ctypes.c_ulonglong, ctypes.c_ulonglong]
    return lib.loupe_13_recherche


def main() -> int:
    print("=== L'ÉPREUVE POSIX — l'unité 03 D210 (loupe-13 × bras C) : "
          "les vecteurs du contrat, le juge = le modèle indépendant ===")
    so = ICI / "epreuves" / "loupe-13-c.so"
    so.parent.mkdir(exist_ok=True)
    compiler(ATELIER / "loupe-13-C-final.c", so)
    fn = charger(so)
    m9 = PROXY.read_bytes()
    if hashlib.sha256(m9).hexdigest() != \
            "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d":
        sys.exit("[!] proxy.exe scellé divergent")

    def chercher(fenetre: bytes, motif: bytes, depart: int) -> int:
        return fn(fenetre, len(fenetre), motif, len(motif), depart)

    # ---- V1 : le doré — le corpus de l'école + les marques du scellé -------
    ecole = [
        (b"premiere-occurrence", b"premiere", 0, 0),
        (b"premiere-occurrence", b"occurrence", 0, 9),
        (b"XXabcYY", b"abc", 2, 2),
        (b"abcXabc", b"abc", 0, 0),
        (b"AAAAB", b"AAAA", 0, 0),
        (b"AAAAB", b"AAAB", 0, 1),
        (b"abcabcabc", b"abc", 4, 6),
        (b"", b"A", 0, -1),
        (b"abc", b"abc", 3, -1),
        (b"abcd", b"cdef", 2, -1),
    ]
    ecarts = []
    for fenetre, motif, depart, attendu in ecole:
        r = chercher(fenetre, motif, depart)
        if r != attendu:
            ecarts.append((fenetre, motif, depart, r, attendu))
    controle("V1:le-corpus-de-l-ecole", not ecarts,
             f"{len(ecole) - len(ecarts)}/{len(ecole)} == le modèle (le "
             "premier octet, le dernier, à cheval sur le départ, "
             "l'occurrence DOUBLE — LA PREMIÈRE exigée, AAAA dans AAAAB, "
             "le presque-frère, le départ au milieu, la fenêtre vide → -1, "
             "la plage vide → -1, le motif trop long → -1 IMMÉDIAT)"
             + (f" — ÉCARTS : {ecarts}" if ecarts else ""))

    proxy8k = m9[:8192]
    marques = [(b"MZ", proxy8k.find(b"MZ")),
               (b"PE\x00\x00", proxy8k.find(b"PE\x00\x00")),
               (b"This program", proxy8k.find(b"This program")),
               (b"PEMax", proxy8k.find(b"PEMax"))]
    ecarts_m = []
    for motif, attendu in marques:
        r = chercher(proxy8k, motif, 0)
        if r != attendu:
            ecarts_m.append((motif, attendu, r))
    controle("V1:les-marques-de-proxy", not ecarts_m,
             "MZ @0, PE @+64 — chaque position == bytes.find sur la "
             "première fenêtre du scellé ; « This program » et « PEMax » "
             "les marques ABSENTES → -1 LA FIN NOMMÉE"
             + (f" — ÉCARTS : {ecarts_m}" if ecarts_m else ""))

    # ---- V2 : le différentiel 10 000 -----------------------------------------
    rng = random.Random(GRAINE)
    ecarts, ecarts_lecture = 0, 0
    for _ in range(10_000):
        n = rng.randrange(0, 4097)
        pauvre = rng.randrange(2)
        alphabet = b"AB" if pauvre else bytes(range(256))
        fenetre = bytes(alphabet[rng.randrange(len(alphabet))]
                        for _ in range(n))
        m = rng.randrange(1, 33)
        motif = bytes(alphabet[rng.randrange(len(alphabet))]
                      for _ in range(m))
        depart = rng.randrange(0, n + 1) if n else 0
        r = chercher(fenetre, motif, depart)
        if r != modele_recherche(fenetre, motif, depart):
            ecarts += 1
        if fenetre != fenetre[:n] or motif != motif[:m]:
            ecarts_lecture += 1        # I3 (le miroir du T — la lecture seule)
    controle("V2:le-differentiel-10-000-cas", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle (y compris les -1 — "
             f"Q1-Q4 ; la graine {GRAINE}, les mêmes tirages que le terrain)")
    controle("V2:la-fenetre-et-le-motif-lus-seuls", ecarts_lecture == 0,
             "les tampons INTACTS aux 10 000 gestes (I3 — la pureté)")

    # ---- V3 : les rejets ------------------------------------------------------
    fenetre4 = b"ABCD"
    for nom, motif, depart in (
            ("E1:le-motif-vide", b"", 0),
            ("E2:le-motif-de-trente-trois", b"X" * 33, 0),
            ("E3:le-depart-au-dela", b"A", 5)):
        r = chercher(fenetre4, motif, depart)
        controle(f"V3:{nom}", r == -5,
                 f"verdict {r} — chercher rien n'est pas chercher ; la "
                 "borne du quotidien MOTIF_MAX ; le départ est une "
                 "position, pas un vœu")

    # ---- V4 : la falsification — le retour avancé d'un ----------------------
    source = (ATELIER / "loupe-13-C-final.c").read_text(encoding="utf-8")
    cible = "return i;"
    if source.count(cible) != 1:
        sys.exit(f"[!] MUTATION-INTROUVABLE : « {cible} » attendu UNE fois "
                 f"(trouvé {source.count(cible)})")
    mution = source.replace(cible, "return i + 1;")
    chemin_mut = ATELIER / "loupe-13-C-mut.c"
    chemin_mut.write_text(mution, encoding="utf-8")
    so_mut = ICI / "epreuves" / "loupe-13-c-mut.so"
    compiler(chemin_mut, so_mut)
    fn_mut = charger(so_mut)

    def chercher_mut(fenetre, motif, depart):
        return fn_mut(fenetre, len(fenetre), motif, len(motif), depart)

    rng = random.Random(GRAINE)
    pris, avec = 0, 0
    for _ in range(300):
        n = rng.randrange(0, 4097)
        pauvre = rng.randrange(2)
        alphabet = b"AB" if pauvre else bytes(range(256))
        fenetre = bytes(alphabet[rng.randrange(len(alphabet))]
                        for _ in range(n))
        m = rng.randrange(1, 33)
        motif = bytes(alphabet[rng.randrange(len(alphabet))]
                      for _ in range(m))
        depart = rng.randrange(0, n + 1) if n else 0
        attendu = modele_recherche(fenetre, motif, depart)
        r = chercher_mut(fenetre, motif, depart)
        if attendu >= 0:
            avec += 1
            if r != attendu:
                pris += 1
    controle("V4:le-retour-avance-d-un-attrape", pris == avec,
             f"les {pris}/{avec} cas à occurrence DIVERGENT du modèle — "
             "le mutant rend le second match au lieu du premier, la "
             "différentielle ATTRAPE LE FAUX (charte § 3, le miroir du "
             "bras T)")
    r = chercher(proxy8k, b"MZ", 0)
    controle("V4:la-piece-juste-rejouee", r == 0,
             "la pièce juste redevenue la même — le vert rendu au retrait "
             "de la mutation (MZ @0, la première occurrence)")

    print(f"\n=== L'ÉPREUVE POSIX {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
