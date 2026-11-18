#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite13.py — LE TERRAIN DE L'UNITÉ 5 (loupe-13 recherche × bras
T, la campagne de comparaison des workflows D204).

Le kit porte UNE pièce et UN scénario :
  loupe.exe          la pièce de campagne — le build du plan où le slot
                     loupe-13 (RVA 0x5740, 192 o) porte LA NOTATION DE
                     CAMPAGNE écrite à la main par l'agent (116 o, 46
                     instructions — le contrat loupe-13:R1 : la première
                     occurrence d'un motif de 1 à 32 o dans une fenêtre,
                     à partir d'un départ donné — la position ABSOLUE de
                     la PREMIÈRE, l'absence → -1 LA FIN NOMMÉE, les trois
                     refus → -5 ; la comparaison par LE SCELLÉ libc-02
                     memcmp à 0x1180 PAR LA CARTE, jamais une boucle
                     réécrite ; AUCUNE entrée IAT — la feuille pure) ; les
                     dix-sept autres blocs demeurent les SCELLÉS du
                     projet ;
  le présent script  python SEUL (ctypes, hashlib, os, platform, random,
                     struct, sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le modèle de la campagne Loupe, inchangé — la
feuille pure le simplifie à l'extrême) : le scénario est LE CHARGEUR —
LoadLibraryEx DONT_RESOLVE (aucune entrée résolue, AUCUN point d'entrée
exécuté) ; LA FEUILLE PURE N'APPELLE PERSONNE : aucune feuille kernel32
à résoudre, le scénario ne touche pas à l'IAT — il APPELLE LOUPE-13 À
SON ADRESSE AU PLAN (base + 0x5740), conduit par la main du kit. Le 5e
argument (le départ) est posé par ctypes AU SLOT msx64 [rsp+0x28]. Le
juge est le MODÈLE INDÉPENDANT (bytes.find de Python) — jamais les octets
du bloc.

LES VECTEURS DU CONTRAT (loupe-13 révision 1) :
  V1  le doré : LE CORPUS DE L'ÉCOLE (le motif au premier octet, au
      dernier, à cheval sur le départ, l'occurrence DOUBLE — LA PREMIÈRE
      exigée, « AAAA » dans « AAAAB », le presque-frère, le départ au
      milieu, la fenêtre vide, la plage vide, le motif plus long que la
      plage restante) + LES MARQUES DE PROXY.EXE SCELLÉ sur sa première
      fenêtre de 8 192 o (MZ @0, PE @+0x40 ; « This program » et « PEMax »
      les marques ABSENTES du scellé — les en-têtes écrits à la main →
      -1 LA FIN NOMMÉE) ;
  V2  le différentiel : 10 000 cas aléatoires (fenêtres 0..4 096 o,
      motifs 1..32, départs aléatoires, alphabet plein ET alphabet
      pauvre pour forcer les occurrences multiples — la graine fixe
      20261115, les mêmes tirages au labo) : rax == bytes.find À
      L'IDENTIQUE, y compris les -1 (Q1-Q4) ; la fenêtre et le motif
      LUS SEULS (I3) ;
  V3  les rejets : le motif vide, le motif de 33 o, le départ au-delà
      → les TROIS verdicts -5 (E1/E2/E3) ;
  V4  la falsification demandée : LE DORÉ COPIÉ AU RÉCEPTACLE avec
      l'octet 1 muté (0x5A → 0x6F — le « MZ » détruit) : la même gamme
      rend -1 LA FIN NOMMÉE QUI DIVERGE du modèle de l'original (0) ET
      == le modèle du mutant : la pièce a lu SES octets, la
      différentielle attrape le faux (le fixture falsifie-16.bin vit au
      réceptacle preuves-unite13/, renvoyé ENTIER avec le témoin).

  le témoin : temoin-unite13.txt au réceptacle preuves-unite13/ —
  DATER ET SIGNER DE VOTRE MAIN (jamais automatisé, D99), renvoyer le
  dossier ENTIER au coffre /test.
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import hashlib
import os
import platform
import random
import struct
import sys
import datetime as dt

ICI = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(ICI, "loupe.exe")
RECEPTACLE = os.path.join(ICI, "preuves-unite13")

# LES CONSTANTES DU PLAN (loupe/layout.py — la source unique)
R_LOUPE13 = 0x5740
GRAINE = 20261115
FENETRE_PROXY = 8192

REUSSITES, ECARTS = [], []


def consigne(ligne: str) -> None:
    print(ligne, flush=True)


def verdict(rax: int) -> int:
    v = rax & 0xFFFFFFFF
    return v - 0x100000000 if v > 0x7FFFFFFF else v


def controle(nom: str, ok: bool, detail: str = "") -> None:
    consigne(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
             + (f" — {detail}" if detail else ""))
    (REUSSITES if ok else ECARTS).append(nom)


def lire_empreintes() -> dict:
    empreintes = {}
    for fich in sorted(os.listdir(ICI)):
        if fich.startswith("EMPREINTES") and fich.endswith(".txt"):
            for ligne in open(os.path.join(ICI, fich), encoding="utf-8",
                              errors="replace").read().splitlines():
                parts = ligne.strip().split(None, 2)
                if len(parts) >= 2 and len(parts[0]) == 64:
                    empreintes[parts[1]] = parts[0].lower()
    return empreintes


def sha256_fichier(chemin: str) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for morceau in iter(lambda: f.read(1 << 20), b""):
            h.update(morceau)
    return h.hexdigest()


def modele_recherche(fenetre: bytes, motif: bytes, depart: int) -> int:
    """LE MODÈLE INDÉPENDANT — la sémantique du contrat, jamais les octets
    du bloc : la position ABSOLUE de la première occurrence, ou les
    verdicts nommés."""
    if len(motif) < 1 or len(motif) > 32:
        return -5                                  # E1/E2 : la borne P4
    if depart > len(fenetre):
        return -5                                  # E3 : le départ est une position
    if len(motif) > len(fenetre) - depart:
        return -1                                  # Q2 : le constat trivial
    return fenetre.find(motif, depart)             # Q1/Q3/Q4 : la première


def main() -> int:
    consigne("=== LE RUN DE L'UNITÉ 5 (loupe-13 recherche × bras T) — la "
             "campagne D204, le terrain du développeur ===")
    empreintes = lire_empreintes()
    if not empreintes:
        consigne("[T0] REFUS : aucune EMPREINTES*.txt au kit — rien ne court")
        return 2
    sha_exe = sha256_fichier(EXE)
    attendu = empreintes.get("loupe.exe", "")
    if sha_exe != attendu:
        consigne(f"[T0] REFUS : loupe.exe {sha_exe[:16]}… != l'empreinte "
                 f"gravée {attendu[:16]}… — la pièce a divergé, rien ne court")
        return 2
    controle("T0:la-piece-recoupee-a-l-empreinte-gravee", True,
             f"loupe.exe sha256 {sha_exe[:16]}… == la gravure du kit")

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]

    DONT_RESOLVE = 0x00000001
    base = k32.LoadLibraryExW(EXE, None, DONT_RESOLVE)
    if not base:
        consigne(f"[T0] REFUS : LoadLibraryEx a rendu 0 (GetLastError "
                 f"{ctypes.get_last_error()})")
        return 2
    consigne(f"[T0] l'image cartographiée DONT_RESOLVE @ {base:#x}")
    consigne("[T0] la feuille pure : AUCUNE feuille kernel32 à résoudre — "
             "le scénario ne touche pas à l'IAT, la pièce n'appelle que "
             "le scellé libc-02 du plan (base + 0x1180)")

    # LE BLOC COMME FONCTION (la conduite de la main du kit — le 5e
    # argument posé par ctypes AU SLOT msx64 [rsp+0x28])
    LOUPE13 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_void_p,
                               ctypes.c_uint64,
                               ctypes.c_uint64)(base + R_LOUPE13)

    fenetre_buf = ctypes.create_string_buffer(8200)
    motif_buf = ctypes.create_string_buffer(40)

    def chercher(fenetre: bytes, motif: bytes, depart: int) -> int:
        ctypes.memmove(fenetre_buf, fenetre, len(fenetre))
        ctypes.memmove(motif_buf, motif, len(motif))
        return verdict(LOUPE13(ctypes.cast(fenetre_buf, ctypes.c_void_p),
                               len(fenetre),
                               ctypes.cast(motif_buf, ctypes.c_void_p),
                               len(motif), depart))

    # ---- V1 : LE DORÉ — l'école + les marques du scellé --------------------
    ecole = [
        (b"premiere-occurrence", b"premiere", 0, 0),   # le motif au premier octet
        (b"premiere-occurrence", b"occurrence", 0, 9),  # au dernier
        (b"XXabcYY", b"abc", 2, 2),                    # à cheval sur le départ
        (b"abcXabc", b"abc", 0, 0),                    # l'occurrence DOUBLE : LA PREMIÈRE
        (b"AAAAB", b"AAAA", 0, 0),                     # le motif répétitif
        (b"AAAAB", b"AAAB", 0, 1),                     # le presque-frère
        (b"abcabcabc", b"abc", 4, 6),                  # le départ au milieu
        (b"", b"A", 0, -1),                            # la fenêtre vide
        (b"abc", b"abc", 3, -1),                       # la plage vide (Q3)
        (b"abcd", b"cdef", 2, -1),                     # le motif > la plage restante
    ]
    ecarts = []
    for fenetre, motif, depart, attendu in ecole:
        r = chercher(fenetre, motif, depart)
        if r != attendu:
            ecarts.append((fenetre, motif, depart, r))
    controle("V1:le-corpus-de-l-ecole", not ecarts,
             f"{len(ecole) - len(ecarts)}/{len(ecole)} == le modèle (le "
             "premier octet, le dernier, à cheval sur le départ, "
             "l'occurrence DOUBLE — LA PREMIÈRE exigée, AAAA dans AAAAB, "
             "le presque-frère, le départ au milieu, la fenêtre vide → -1, "
             "la plage vide → -1, le motif trop long → -1 IMMÉDIAT)"
             + (f" — ÉCARTS : {ecarts}" if ecarts else ""))

    proxy8k = open(os.path.join(ICI, "proxy.exe"), "rb").read(FENETRE_PROXY)
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
             f"MZ @0, PE @+{marques[1][1]:#x}, « This program » et « PEMax » "
             "les marques ABSENTES du scellé (les en-têtes écrits à la "
             "main) → -1 LA FIN NOMMÉE, l'absence constatée"
             + (f" — ÉCARTS : {ecarts_m}" if ecarts_m else ""))

    # ---- V2 : LE DIFFÉRENTIEL — 10 000 cas aléatoires ----------------------
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
        if bytes((ctypes.c_ubyte * len(fenetre))
                 .from_buffer(fenetre_buf, 0))[:len(fenetre)] != fenetre \
                or bytes((ctypes.c_ubyte * len(motif))
                         .from_buffer(motif_buf, 0))[:len(motif)] != motif:
            ecarts_lecture += 1            # I3 : la fenêtre et le motif lus seuls
    controle("V2:le-differentiel-10-000-cas", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle (la graine {GRAINE}, "
             "les mêmes tirages au labo, y compris les -1 — Q1-Q4)")
    controle("V2:la-fenetre-et-le-motif-lus-seuls", ecarts_lecture == 0,
             "les octets de la fenêtre et du motif INTACTS aux 10 000 "
             "gestes (I3 — la pureté)")

    # ---- V3 : LES REJETS — les trois -5 ------------------------------------
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

    # ---- V4 : LA FALSIFICATION DEMANDÉE — l'octet du MZ muté ---------------
    os.makedirs(RECEPTACLE, exist_ok=True)
    doré = proxy8k[:16]                       # « 4D 5A 00 00 … » la pièce de l'ère
    mutant = bytearray(doré)
    mutant[1] ^= 0x35                         # 0x5A ^ 0x35 = 0x6F — le « Z » détruit
    mutant = bytes(mutant)
    chemin_faux = os.path.join(RECEPTACLE, "falsifie-16.bin")
    with open(chemin_faux, "wb") as f:
        f.write(mutant)
    r_original = chercher(doré, b"MZ", 0)
    r_mutant = chercher(mutant, b"MZ", 0)
    controle("V4:l-octet-du-mz-mute-la-fin-nommee",
             r_original == 0 and r_mutant == -1
             and r_mutant != modele_recherche(doré, b"MZ", 0)
             and r_mutant == modele_recherche(mutant, b"MZ", 0),
             "l'octet 1 muté (0x5A → 0x6F) : le « MZ » détruit, la réponse "
             "-1 LA FIN NOMMÉE DIVERGE du modèle de l'original (0) ET == "
             "le modèle du mutant — la pièce a lu SES octets, la "
             "différentielle attrape le faux (le fixture falsifie-16.bin "
             "vit au réceptacle)")

    # ---- LE TÉMOIN ----------------------------------------------------------
    lignes = []
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 5 — loupe-13 recherche × bras T "
                  "(la campagne D204, la comparaison des workflows)")
    lignes.append("=" * 78)
    lignes.append(f"le run      : "
                  f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
                  f" (UTC) — la machine du développeur")
    lignes.append(f"la machine  : {platform.node()} · {platform.system()} "
                  f"{platform.release()} · {platform.machine()} · "
                  f"Python {platform.python_version()}")
    lignes.append(f"la pièce    : loupe.exe {os.path.getsize(EXE)} o, "
                  f"sha256 {sha_exe}")
    lignes.append(f"le verdict  : {len(REUSSITES)} VERT, {len(ECARTS)} ROUGE "
                  f"{'— VERT' if not ECARTS else '— ÉCART NOMMÉ'}")
    lignes.append("")
    lignes.append("LES VECTEURS :")
    for nom in REUSSITES:
        lignes.append(f"  VERT {nom}")
    for nom in ECARTS:
        lignes.append(f"  ROUGE {nom}")
    lignes.append("")
    lignes.append("LE GESTE QUI RESTE À LA MAIN (jamais automatisé, D99) :")
    lignes.append("  DATER ce témoin (la date de votre main), le SIGNER,")
    lignes.append("  renvoyer le dossier preuves-unite13/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite13.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 5 FINI : dater et signer le témoin de "
             "votre main, renvoyer preuves-unite13/ ENTIER au coffre /test "
             "===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
