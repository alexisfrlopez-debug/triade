#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite13C.py — LE TERRAIN DE L'UNITÉ 5 (loupe-13 recherche × bras
C, gcc -O2, la campagne de comparaison des workflows D204).

Le kit porte UNE pièce et UN scénario :
  loupe-13-c.dll     la pièce du bras C — le source écrit par l'agent
                     (loupe_13_recherche : les bornes d'abord, le constat
                     trivial avant la boucle, chaque candidat au memcmp
                     de la bibliothèque — I2, la liste d'appels FERMÉE,
                     jamais une boucle réécrite), compilée gcc -O2
                     croisée — L'EXPORT UNIQUE loupe_13_recherche, les
                     imports servent le démarreur CRT du lieur seul ;
  le présent script  python SEUL (ctypes, hashlib, os, platform, random,
                     struct, sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le modèle de la campagne Loupe, inchangé — la
feuille pure le simplifie à l'extrême) : le scénario est LE CHARGEUR —
LoadLibraryEx DONT_RESOLVE (aucune entrée résolue, AUCUN point d'entrée
exécuté) ; LA DÉCOUVERTE PAR LA TABLE D'EXPORTS (les arités unifiées
(base, rva) — la leçon de la 302) mène à l'export unique, l'appel se
fait à SA RVA DÉCOUVERTE (base + rva). LA CLÔTURE DE LA PIÈCE APPELLE
UNE FEUILLE — le memcmp de msvcrt.dll, par son thunk IAT : le scénario
découvre le slot PAR LA TABLE D'IMPORTS (la même convention (base, rva),
AUCUNE RVA codée) et LIE la feuille au memcmp de la machine AVANT le
premier appel, au guichet fail-closed (la leçon de la 304 : DONT_RESOLVE
ne lie rien — le slot garde sa valeur sur disque, l'entrée hint/nom, une
RVA nue ; le v1 y sauta : access violation 0x92da, le run tombé code 1
au premier candidat de l'école). Le 5e argument (le départ) est posé par
ctypes AU SLOT msx64 [rsp+0x28]. Le juge est le MODÈLE INDÉPENDANT
(bytes.find de Python) — jamais les octets de la pièce.

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
      différentielle attrape le faux (le fixture falsifie-16.bin vit
      au réceptacle preuves-unite13C/, renvoyé ENTIER avec le témoin).

  le témoin : temoin-unite13C.txt au réceptacle preuves-unite13C/ —
  DATER ET SIGNER DE VOTRE MAIN (jamais automatisé, D99), renvoyer le
  dossier ENTIER au coffre /test.

LA RÉVISION v2 (la faute nommée à la 304, la pièce INTACTE — la dll
inchangée, la faute était au kit, jamais à la pièce) :
  ① LA FEUILLE MEMCMP LIÉE — le v1 cartographiait la pièce en
     DONT_RESOLVE sans lier la feuille que la clôture appelle : le
     premier appel sautait à la valeur SUR DISQUE du slot IAT
     (0x92da, l'entrée hint/nom de memcmp — une RVA nue, hors de toute
     page) : access violation, le run tombé code 1 au premier candidat
     de l'école. Le v2 découvre le slot PAR LA TABLE D'IMPORTS, le
     repointe au memcmp de msvcrt.dll de la machine (LoadLibrary +
     GetProcAddress, VirtualProtect l'instant de l'écriture, la
     re-protection, la relecture recoupée), le guichet fail-closed à
     chaque geste — un écart nommé STOPPE le flux, RIEN ne court ;
  ② LE RÉCEPTACLE NOMMÉ JUSTE — le texte du témoin et la note V4 du
     v1 nommaient preuves-unite13/ (le dossier du bras T, le gabarit
     d'où le scénario C fut dérivé) : les voilà à preuves-unite13C/ ;
  LES VECTEURS INTACTS au byte près (V1-V4), le juge inchangé (le
  modèle indépendant), les contrôles inchangés.
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
PIECE = os.path.join(ICI, "loupe-13-c.dll")
RECEPTACLE = os.path.join(ICI, "preuves-unite13C")

# LES CONSTANTES DU PLAN (loupe/layout.py — la source unique)
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
    consigne("=== LE RUN DE L'UNITÉ 5 (loupe-13 recherche × bras C, gcc -O2) — la "
             "campagne D204, le terrain du développeur ===")
    empreintes = lire_empreintes()
    if not empreintes:
        consigne("[T0] REFUS : aucune EMPREINTES*.txt au kit — rien ne court")
        return 2
    sha_dll = sha256_fichier(PIECE)
    attendu = empreintes.get("loupe-13-c.dll", "")
    if sha_dll != attendu:
        consigne(f"[T0] REFUS : loupe-13-c.dll {sha_dll[:16]}… != "
                 f"l'empreinte gravée {attendu[:16]}… — la pièce a divergé, "
                 "rien ne court")
        return 2
    controle("T0:la-piece-recoupee-a-l-empreinte-gravee", True,
             f"loupe-13-c.dll sha256 {sha_dll[:16]}… == la gravure du kit")

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]

    DONT_RESOLVE = 0x00000001
    base = k32.LoadLibraryExW(PIECE, None, DONT_RESOLVE)
    if not base:
        consigne(f"[T0] REFUS : LoadLibraryEx a rendu 0 (GetLastError "
                 f"{ctypes.get_last_error()})")
        return 2
    consigne(f"[T0] l'image cartographiée DONT_RESOLVE @ {base:#x}")
    # ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS (les arités unifiées
    # (base, rva) — la leçon de la 302 : les gardes fail-closed, le
    # terminateur lu au champ) ---------------------------------------------
    def lire_octets(base: int, rva: int, n: int) -> bytes:
        brut = (ctypes.c_ubyte * n)()
        ctypes.memmove(brut, base + rva, n)
        return bytes(brut)

    def lire_u32(base: int, rva: int) -> int:
        return struct.unpack("<I", lire_octets(base, rva, 4))[0]

    def lire_u16(base: int, rva: int) -> int:
        return struct.unpack("<H", lire_octets(base, rva, 2))[0]

    def lire_chaine(base: int, rva: int) -> str:
        sortie = []
        for i in range(256):
            c = lire_octets(base, rva + i, 1)[0]
            if c == 0:
                return "".join(sortie)
            sortie.append(chr(c))
        return "".join(sortie)

    e_lfanew = struct.unpack("<I", lire_octets(base, 0x3C, 4))[0]
    opt = e_lfanew + 4 + 20                      # l'en-tête optionnel PE32+
    rva_exports = lire_u32(base, opt + 112)      # le répertoire 0 : export
    if not rva_exports:
        consigne("[T0] REFUS : le répertoire d'exports introuvable — la "
                 "pièce n'est pas la DLL attendue")
        return 2
    nb_noms = lire_u32(base, rva_exports + 24)
    tab_fonctions = lire_u32(base, rva_exports + 28)
    tab_noms = lire_u32(base, rva_exports + 32)
    tab_ordinaux = lire_u32(base, rva_exports + 36)
    rva_par_nom = {}
    for i in range(nb_noms):
        nom = lire_chaine(base, lire_u32(base, tab_noms + 4 * i))
        ordinal = lire_u16(base, tab_ordinaux + 2 * i)
        if nom:
            rva_par_nom[nom] = lire_u32(base, tab_fonctions + 4 * ordinal)
    if set(rva_par_nom) != {"loupe_13_recherche"}:
        consigne(f"[T0] REFUS : les exports découverts {sorted(rva_par_nom)} "
                 f"!= l'export unique loupe_13_recherche — la pièce a divergé")
        return 2
    R_LOUPE13 = rva_par_nom["loupe_13_recherche"]
    consigne(f"[T0] l'export UNIQUE découvert : loupe_13_recherche "
             f"@+{R_LOUPE13:#x} — la feuille pure, le seul appel de sa "
             "clôture : le memcmp de la bibliothèque")
    consigne("[T0] la clôture de la pièce appelle UNE feuille : le memcmp "
             "de msvcrt.dll par son thunk IAT (I2 — la liste d'appels "
             "FERMÉE) ; les autres imports servent le démarreur CRT du "
             "lieur, qui ne court jamais sous DONT_RESOLVE")

    # ---- LA FEUILLE MEMCMP LIÉE (le seul appel de la clôture de la pièce) --
    # DONT_RESOLVE ne lie RIEN : le slot IAT de memcmp garde sa valeur SUR
    # DISQUE — l'entrée hint/nom, une RVA NUE. Le v1 appelait la pièce sans
    # lier la feuille : le thunk sautait à l'adresse nue, LA FAUTE NOMMÉE à
    # la 304 (access violation 0x92da, le run tombé code 1 au premier
    # candidat de l'école). Le scénario, chargeur minimal, découvre le slot
    # PAR LA TABLE D'IMPORTS (la convention (base, rva) unifiée — la leçon
    # de la 302, AUCUNE RVA codée) et lie la feuille unique au memcmp de la
    # machine, AU GUICHET FAIL-CLOSED : chaque geste vérifié, l'écart nommé,
    # le flux stoppé — jamais un appel sur une feuille morte.
    def lier_feuille_memcmp():
        """Le guichet de la feuille : (rva du slot, valeur sur disque,
        adresse liée) ou None — l'écart nommé, le flux stoppé."""
        rep_imports = lire_u32(base, opt + 120)  # le répertoire 1 : imports
        if not rep_imports:
            consigne("[T0] REFUS : le répertoire d'imports introuvable — "
                     "la pièce n'est pas la DLL attendue")
            return None
        rva_slot, termine = None, False
        for num_desc in range(16):               # la garde : jamais au-delà
            ilt, _, _, rva_dll, iat = struct.unpack(
                "<IIIII", lire_octets(base, rep_imports + 20 * num_desc, 20))
            if ilt == 0 and iat == 0:            # le terminateur lu au champ
                termine = True
                break
            if lire_chaine(base, rva_dll).lower() != "msvcrt.dll":
                continue                         # KERNEL32 : le démarreur CRT
            for k in range(4096):                # la garde : jamais au-delà
                entree = struct.unpack(
                    "<Q", lire_octets(base, ilt + 8 * k, 8))[0]
                if entree == 0:                  # le terminateur lu au champ
                    termine = True
                    break
                if not entree & (1 << 63) and \
                        lire_chaine(base, entree + 2) == "memcmp":
                    rva_slot = iat + 8 * k       # LE slot, découvert par le nom
            if rva_slot is not None:
                break
        if rva_slot is None or not termine:
            consigne("[T0] REFUS : la feuille memcmp de msvcrt.dll "
                     "introuvable à la table d'imports — la pièce a divergé")
            return None
        sur_disque = struct.unpack(
            "<Q", lire_octets(base, rva_slot, 8))[0]
        k32.LoadLibraryW.restype = ctypes.c_void_p
        k32.LoadLibraryW.argtypes = [wt.LPCWSTR]
        msvcrt = k32.LoadLibraryW("msvcrt.dll")
        if not msvcrt:
            consigne(f"[T0] REFUS : msvcrt.dll introuvable (GetLastError "
                     f"{ctypes.get_last_error()}) — la feuille ne peut "
                     "être liée")
            return None
        k32.GetProcAddress.restype = ctypes.c_void_p
        k32.GetProcAddress.argtypes = [ctypes.c_void_p, wt.LPCSTR]
        adresse = k32.GetProcAddress(msvcrt, b"memcmp")
        if not adresse:
            consigne(f"[T0] REFUS : memcmp introuvable dans msvcrt.dll "
                     f"(GetLastError {ctypes.get_last_error()})")
            return None
        ancien = wt.DWORD(0)
        k32.VirtualProtect.restype = wt.BOOL
        k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                       wt.DWORD, ctypes.POINTER(wt.DWORD)]
        if not k32.VirtualProtect(base + rva_slot, 8, 0x40,   # READWRITE
                                  ctypes.byref(ancien)):
            consigne(f"[T0] REFUS : VirtualProtect a rendu 0 (GetLastError "
                     f"{ctypes.get_last_error()}) — le slot demeure à sa "
                     "valeur sur disque")
            return None
        ctypes.memmove(base + rva_slot, struct.pack("<Q", adresse), 8)
        rendu = wt.BOOL(k32.VirtualProtect(base + rva_slot, 8, ancien.value,
                                           ctypes.byref(ancien)))
        if not rendu:
            consigne(f"[T0] REFUS : la re-protection du slot a échoué "
                     f"(GetLastError {ctypes.get_last_error()}) — l'écrit "
                     "demeure, la page ouverte : RIEN ne court")
            return None
        relue = struct.unpack("<Q", lire_octets(base, rva_slot, 8))[0]
        if relue != adresse:
            consigne(f"[T0] REFUS : la relecture du slot {relue:#x} != "
                     f"l'adresse liée {adresse:#x} — la liaison n'est pas "
                     "certaine")
            return None
        return rva_slot, sur_disque, adresse

    feuille = lier_feuille_memcmp()
    if feuille is None:
        return 2
    rva_slot, sur_disque, adresse_memcmp = feuille
    consigne(f"[T0] la feuille unique liée : memcmp de msvcrt.dll — le slot "
             f"IAT @+{rva_slot:#x} (la valeur sur disque {sur_disque:#x}, "
             f"l'entrée hint/nom — l'adresse nue où le v1 sautait) "
             f"repointé à {adresse_memcmp:#x}, l'écriture protégée "
             "l'instant du geste, la relecture recoupée (le guichet "
             "fail-closed)")

    # LA PIÈCE COMME FONCTION (la conduite de la main du kit — le 5e
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
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 5 — loupe-13 recherche × bras C "
                  "(la campagne D204, la comparaison des workflows)")
    lignes.append("=" * 78)
    lignes.append(f"le run      : "
                  f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
                  f" (UTC) — la machine du développeur")
    lignes.append(f"la machine  : {platform.node()} · {platform.system()} "
                  f"{platform.release()} · {platform.machine()} · "
                  f"Python {platform.python_version()}")
    lignes.append(f"la pièce    : loupe-13-c.dll {os.path.getsize(PIECE)} o, "
                  f"sha256 {sha_dll}")
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
    lignes.append("  renvoyer le dossier preuves-unite13C/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite13C.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 5 FINI : dater et signer le témoin de "
             "votre main, renvoyer preuves-unite13C/ ENTIER au coffre /test "
             "===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
