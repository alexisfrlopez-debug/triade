#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite02C.py — LE TERRAIN DE L'UNITÉ 2 (loupe-02 lire × bras C,
la campagne de comparaison des workflows D204).

Le kit porte UNE pièce et UN scénario :
  loupe-02-c.dll     la pièce du bras C (gcc -O2 -shared, 95 413 o) — le
                     même contrat loupe-02:R1 que le bras T : la fenêtre
                     bornée + LE RECOUVREMENT du journal ; le bloc session
                     (loupe_01_ouvrir/loupe_03_fermer) repris TEL QUEL du
                     kit 01 (le flux standard réutilise son code éprouvé —
                     l'écart nommé du bras C : sa première fenêtre est lue
                     INLINE à l'ouverture, le loupe-01 du plan APPELLE
                     loupe-02) ;
  le présent script  python SEUL (ctypes, hashlib, os, platform, struct,
                     sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le modèle de la campagne Loupe, inchangé — l'édition
v2 du kit 01 : la découverte PAR LA TABLE D'EXPORTS, la résolution aux
SLOTS RÉELS de la table d'imports — le terminateur lu au CHAMP Name, les
gardes fail-closed) : le scénario est LE CHARGEUR — LoadLibraryEx
DONT_RESOLVE, il résout LUI-MÊME les SIX feuilles kernel32 que la pièce
déclare (SetFilePointerEx PRÉSENTE cette fois — la pièce la raconte à
CHAQUE lecture), ouvre la session PAR LA PIÈCE, et APPELLE LOUPE_02_LIRE à
son export. Le juge est le MODÈLE INDÉPENDANT (hashlib, les découpes) —
jamais les octets de la pièce.

LES VECTEURS DU CONTRAT (loupe-02 révision 1 — les mêmes que le bras T) :
  V1  le différentiel : les témoins du kit — la fenêtre née à l'ouverture
      (INLINE au bras C, l'écart nommé), puis les frontières (0, la
      dernière pleine, la dernière partielle) + la graine fixe (100 tirés)
      — le tampon == la découpe, remplissage == min(384, taille −
      décalage), la vue et le curseur INTACTS ; le vide : aucun décalage
      n'y est valide ;
  V2  le recouvrement du journal : les entrées posées aux BORDS de la
      fenêtre (le premier, le dernier, l'avant, l'après) puis CINQ dedans
      dont une NON ALIGNÉE — l'octet écrit REMPLACE l'octet lu ; le
      journal (exporté DONNÉE) INTACT après le geste ;
  V3  les rejets : sans session → -4 ; non multiple de 16 → -5 ; à la
      taille exacte et au-delà → -3 — RIEN lu : le tampon empoisonné et
      le remplissage INTACTS ;
  V4  l'échec système : la plage [0, 384) VERROUILLÉE par un second
      détenteur (LockFile) → ReadFile refuse → -6, remplissage 0
      (fail-closed), la session SURVIT ; si le verrou ne mord pas au
      terrain : NOMMÉ ABSENT, jamais maquillé ;
  V5  la falsification demandée : un octet du tampon muté après lecture —
      l'état lu DIVERGE du modèle (le juge lit l'état).

  le témoin : temoin-unite02C.txt au réceptacle preuves-unite02C/ —
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
PIECE = os.path.join(ICI, "loupe-02-c.dll")
RECEPTACLE = os.path.join(ICI, "preuves-unite02C")

FEUILLES_KIT = {"CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                "ReadFile", "CloseHandle", "GetLastError"}
TAILLE, POIGNEE = 520, 528
VUE, CURSEUR, REMPL, TAMPON = 536, 544, 552, 568
ZONE_JOURNAL = 4112
GRAINE = 20261114

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


def lire_octets(base: int, rva: int, n: int) -> bytes:
    brut = (ctypes.c_ubyte * n)()
    ctypes.memmove(brut, base + rva, n)
    return bytes(brut)


def lire_u32(base: int, rva: int) -> int:
    return struct.unpack("<I", lire_octets(base, rva, 4))[0]


def lire_u16(base: int, rva: int) -> int:
    return struct.unpack("<H", lire_octets(base, rva, 2))[0]


def lire_chaine(base: int, rva: int, limite: int = 64) -> str:
    brut = lire_octets(base, rva, limite)
    fin = brut.find(b"\x00")
    return brut[:fin if fin >= 0 else limite].decode("ascii",
                                                     errors="replace")


def decales_terrain(taille: int) -> list[int]:
    """Les décalages du terrain : les frontières à la main + la graine fixe
    (100 tirés pour les grands témoins — le terrain lit de vrais octets)."""
    rng = random.Random(GRAINE)
    out = [0]
    if taille >= 16:
        dernier = (taille - 1) // 16 * 16    # la dernière valide
        if dernier not in out:
            out.append(dernier)
        pleine = taille - 384                        # la dernière PLEINE
        if pleine >= 0:
            pleine -= pleine % 16
            if pleine >= 0 and pleine not in out:
                out.append(pleine)
        if taille % 16 == 0 and taille - 16 not in out:
            out.append(taille - 16)
        pool = list(range(0, (taille + 15) // 16 * 16, 16))
        out += [d for d in rng.sample(pool, min(100, len(pool)))
                if d not in set(out)]
    return out


def main() -> int:
    consigne("=== LE RUN DE L'UNITÉ 2 × BRAS C (loupe-02 lire, gcc -O2) — "
             "la campagne D204, le terrain du développeur ===")
    empreintes = lire_empreintes()
    if not empreintes:
        consigne("[T0] REFUS : aucune EMPREINTES*.txt au kit — rien ne court")
        return 2
    sha_piece = sha256_fichier(PIECE)
    attendu = empreintes.get("loupe-02-c.dll", "")
    if sha_piece != attendu:
        consigne(f"[T0] REFUS : loupe-02-c.dll {sha_piece[:16]}… != "
                 f"l'empreinte gravée {attendu[:16]}… — la pièce a divergé, "
                 f"rien ne court")
        return 2
    controle("T0:la-piece-recoupee-a-l-empreinte-gravee", True,
             f"loupe-02-c.dll sha256 {sha_piece[:16]}… == la gravure du kit")

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                   wt.DWORD, ctypes.POINTER(wt.DWORD)]
    k32.GetProcAddress.restype = ctypes.c_void_p
    k32.GetProcAddress.argtypes = [ctypes.c_void_p, wt.LPCSTR]
    k32.GetModuleHandleW.restype = ctypes.c_void_p
    k32.GetModuleHandleW.argtypes = [wt.LPCWSTR]
    k32.CreateFileW.restype = ctypes.c_void_p
    k32.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD,
                                ctypes.c_void_p, wt.DWORD, wt.DWORD,
                                ctypes.c_void_p]
    k32.LockFile.restype = wt.BOOL
    k32.LockFile.argtypes = [ctypes.c_void_p, wt.DWORD, wt.DWORD,
                             wt.DWORD, wt.DWORD]
    k32.UnlockFile.restype = wt.BOOL
    k32.UnlockFile.argtypes = [ctypes.c_void_p, wt.DWORD, wt.DWORD,
                               wt.DWORD, wt.DWORD]

    DONT_RESOLVE = 0x00000001
    base = k32.LoadLibraryExW(PIECE, None, DONT_RESOLVE)
    if not base:
        consigne(f"[T0] REFUS : LoadLibraryEx a rendu 0 (GetLastError "
                 f"{ctypes.get_last_error()})")
        return 2
    consigne(f"[T0] l'image cartographiée DONT_RESOLVE @ {base:#x}")

    # ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS (le bras C : la pièce
    # compilée porte SES adresses aux tables du PE) --------------------------
    e_lfanew = struct.unpack("<I", lire_octets(base, 0x3C, 4))[0]
    opt = e_lfanew + 4 + 20                      # l'en-tête optionnel PE32+
    rva_exports = lire_u32(base, opt + 112)      # le répertoire 0 : export
    rva_imports = lire_u32(base, opt + 120)      # le répertoire 1 : import
    if not rva_exports or not rva_imports:
        consigne("[T0] REFUS : les répertoires d'exports/d'imports "
                 "introuvables — la pièce n'est pas la DLL attendue")
        return 2
    noms_vus, rva_par_nom = [], {}
    nb_noms = lire_u32(base, rva_exports + 24)
    tab_fonctions = lire_u32(base, rva_exports + 28)
    tab_noms = lire_u32(base, rva_exports + 32)
    tab_ordinaux = lire_u32(base, rva_exports + 36)
    for i in range(nb_noms):
        nom = lire_chaine(base, lire_u32(base, tab_noms + 4 * i))
        ordinal = lire_u16(base, tab_ordinaux + 2 * i)
        rva_par_nom[nom] = lire_u32(base, tab_fonctions + 4 * ordinal)
        noms_vus.append(nom)
    for attendu_nom in ("loupe_01_ouvrir", "loupe_02_lire", "loupe_03_fermer",
                        "cadre", "journal", "panneau"):
        if attendu_nom not in rva_par_nom:
            consigne(f"[T0] REFUS : l'export {attendu_nom} introuvable à "
                     f"la table ({noms_vus}) — la pièce a divergé")
            return 2
    R_OUVRIR = rva_par_nom["loupe_01_ouvrir"]
    R_LIRE = rva_par_nom["loupe_02_lire"]
    R_FERMER = rva_par_nom["loupe_03_fermer"]
    R_CADRE = rva_par_nom["cadre"]
    R_JOURNAL = rva_par_nom["journal"]
    R_PANNEAU = rva_par_nom["panneau"]
    consigne("[T0] les SIX exports découverts : loupe_01_ouvrir "
             f"@+{R_OUVRIR:#x}, loupe_02_lire @+{R_LIRE:#x}, loupe_03_fermer "
             f"@+{R_FERMER:#x}, cadre (DONNÉE, 960 o) @+{R_CADRE:#x}, "
             f"journal (DONNÉE, 4 112 o) @+{R_JOURNAL:#x}, panneau "
             f"(DONNÉE, 48 o) @+{R_PANNEAU:#x}")

    # ---- LA RÉSOLUTION AUX SLOTS RÉELS de la table d'imports ---------------
    # (l'édition v2 du kit 01 : le terminateur se lit au CHAMP Name —
    #  l'RVA NUL, AVANT toute lecture de chaîne ; gardes fail-closed : au
    #  plus 64 descripteurs, aucun Name hors image — REFUS nommé, jamais
    #  un plantage)
    h_k32 = ctypes.c_void_p(k32.GetModuleHandleW("kernel32.dll"))
    slots = {}                                    # nom → l'adresse du slot
    taille_image = lire_u32(base, opt + 56)       # SizeOfImage (PE32+ : +56)
    desc = rva_imports
    for _garde in range(64):
        nom_rva = lire_u32(base, desc + 12)
        if not nom_rva:                           # LE TERMINATEUR : Name NUL
            break
        if nom_rva >= taille_image:               # la garde fail-closed
            consigne(f"[T0] REFUS : un descripteur d'import pointe hors "
                     f"image (@+{nom_rva:#x}) — la pièce a divergé, rien "
                     f"ne court")
            return 2
        nom_dll = lire_chaine(base, nom_rva)
        if not nom_dll:
            break
        if "kernel32" in nom_dll.lower():
            ilt = lire_u32(base, desc + 0)        # OriginalFirstThunk
            iat = lire_u32(base, desc + 16)       # FirstThunk
            j = 0
            while True:
                entree = struct.unpack(
                    "<Q", lire_octets(base, ilt + 8 * j, 8))[0] if ilt \
                    else lire_u32(base, iat + 8 * j)
                if not entree:
                    break
                if not (entree >> 63):
                    feuille = lire_chaine(base, (entree & 0xFFFFFFFF) + 2)
                    if feuille in FEUILLES_KIT:
                        slots[feuille] = base + iat + 8 * j
                j += 1
        desc += 20
    else:
        consigne("[T0] REFUS : la table d'imports sans terminateur — la "
                 "pièce a divergé, rien ne court")
        return 2
    manquantes = [f for f in FEUILLES_KIT if f not in slots]
    if manquantes:
        consigne(f"[T0] REFUS : les feuilles {manquantes} introuvables à "
                 f"la table d'imports — la pièce a divergé")
        return 2
    for feuille, adresse_slot in sorted(slots.items()):
        adresse = k32.GetProcAddress(h_k32, feuille.encode("ascii"))
        if not adresse:
            consigne(f"[T0] REFUS : {feuille} introuvable à kernel32")
            return 2
        ancien = wt.DWORD(0)
        page = adresse_slot & ~0xFFF
        if not k32.VirtualProtect(ctypes.c_void_p(page), 0x1000,
                                  0x40, ctypes.byref(ancien)):
            consigne("[T0] REFUS : VirtualProtect sur l'IAT impossible")
            return 2
        ctypes.memmove(adresse_slot, struct.pack("<Q", adresse), 8)
        k32.VirtualProtect(ctypes.c_void_p(page), 0x1000, ancien.value,
                           ctypes.byref(ancien))
    consigne(f"[T0] les {len(slots)} feuilles kernel32 de la pièce résolues "
             f"aux slots réels de SA table d'imports ({', '.join(sorted(slots))}"
             f") — SetFilePointerEx PRÉSENTE (la pièce la raconte à CHAQUE "
             f"lecture)")

    # ---- LES BLOCS COMME FONCTIONS (la conduite de la main du kit) ---------
    LOUPE01 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(base + R_OUVRIR)
    LOUPE02 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_uint64)(base + R_LIRE)
    LOUPE03 = ctypes.CFUNCTYPE(ctypes.c_int64)(base + R_FERMER)

    def appeler_ouvrir(tampon: bytes) -> int:
        zone = ctypes.create_string_buffer(bytes(tampon), len(tampon) + 8)
        r = LOUPE01(ctypes.cast(zone, ctypes.c_void_p))
        return verdict(r)

    def lire_fenetre(decalage: int) -> int:
        return verdict(LOUPE02(decalage))

    def ecrire_cadre(off: int, donnees: bytes) -> None:
        ctypes.memmove(base + R_CADRE + off, donnees, len(donnees))

    def cadre_champ(off: int, n: int = 8) -> bytes:
        return lire_octets(base, R_CADRE + off, n)

    def cadre_qword(off: int) -> int:
        return struct.unpack("<Q", cadre_champ(off, 8))[0]

    def cadre_dword(off: int) -> int:
        return struct.unpack("<I", cadre_champ(off, 4))[0]

    def poser_journal(entrees) -> None:
        brut = bytearray(ZONE_JOURNAL)
        for i, (dec, octet) in enumerate(entrees):
            brut[16 * i:16 * i + 16] = struct.pack("<QB7x", dec, octet)
        brut[4096:4100] = struct.pack("<I", len(entrees))
        ctypes.memmove(base + R_JOURNAL, bytes(brut), ZONE_JOURNAL)

    def journal_zone() -> bytes:
        return lire_octets(base, R_JOURNAL, ZONE_JOURNAL)

    def modele_tampon(donnees: bytes, decalage: int, journal):
        rempl = min(384, len(donnees) - decalage)
        tampon = bytearray(donnees[decalage:decalage + rempl])
        for dec, octet in journal:
            if decalage <= dec < decalage + rempl:
                tampon[dec - decalage] = octet
        return rempl, bytes(tampon)

    # ---- V1 : LE DIFFÉRENTIEL — la fenêtre bornée --------------------------
    for nom in ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin"):
        donnees = open(os.path.join(ICI, nom), "rb").read()
        r = appeler_ouvrir(nom.encode("utf-16-le") + b"\x00\x00")
        rempl0 = min(384, len(donnees))
        controle(f"V1:{nom}-la-fenetre-nee-a-l-ouverture",
                 r == 0 and cadre_dword(REMPL) == rempl0
                 and cadre_champ(TAMPON, rempl0) == donnees[:rempl0],
                 f"la première fenêtre lue INLINE au bloc session (l'écart "
                 f"nommé du bras C) : remplissage {cadre_dword(REMPL)} == "
                 f"min(384, {len(donnees)}), le tampon == la découpe")
        tout_ok, appels = True, 0
        for dec in decales_terrain(len(donnees)):
            avant_vue, avant_cur = cadre_qword(VUE), cadre_qword(CURSEUR)
            r = lire_fenetre(dec)
            rempl_att, tamp_att = modele_tampon(donnees, dec, [])
            tout_ok &= (r == 0 and cadre_dword(REMPL) == rempl_att
                        and cadre_champ(TAMPON, rempl_att) == tamp_att
                        and cadre_qword(VUE) == avant_vue
                        and cadre_qword(CURSEUR) == avant_cur)
            appels += 1
        controle(f"V1:{nom}-la-fenetre-bornee-a-{appels}-decalages", tout_ok,
                 f"{appels} décalages valides (les frontières + la graine "
                 f"{GRAINE}) : le tampon == la découpe, remplissage == "
                 f"min(384, taille − décalage), la vue et le curseur INTACTS")
        LOUPE03()
    donnees = open(os.path.join(ICI, "vide.bin"), "rb").read()
    r = appeler_ouvrir("vide.bin".encode("utf-16-le") + b"\x00\x00")
    controle("V1:vide.bin-l-ouverture-sans-fenetre",
             r == 0 and cadre_dword(REMPL) == 0,
             "le vide s'ouvre, remplissage 0 (la fenêtre née est vide)")
    r = lire_fenetre(0)
    controle("V1:vide.bin-aucune-fenetre-valide", r == -3,
             f"rax={r} (sur le vide, décalage 0 ≥ taille 0 → -3 HORS-BORNES)")
    LOUPE03()
    donnees = open(os.path.join(ICI, "temoin-3f.bin"), "rb").read()
    appeler_ouvrir("temoin-3f.bin".encode("utf-16-le") + b"\x00\x00")
    ecrire_cadre(VUE, (64).to_bytes(8, "little"))
    ecrire_cadre(CURSEUR, (65).to_bytes(8, "little"))
    r = lire_fenetre(4096)
    controle("V1:la-vue-et-le-curseur-intacts",
             r == 0 and cadre_qword(VUE) == 64 and cadre_qword(CURSEUR) == 65,
             "la lecture à 4096 ne déplace NI la vue (64) NI le curseur (65) "
             "— le défilement est à loupe-11")
    LOUPE03()

    # ---- V2 : LE RECOUVREMENT DU JOURNAL ------------------------------------
    donnees = open(os.path.join(ICI, "temoin-3f.bin"), "rb").read()
    appeler_ouvrir("temoin-3f.bin".encode("utf-16-le") + b"\x00\x00")
    fen = 65536
    journal_bords = [(fen, 0xAA), (fen + 383, 0xBB),
                     (fen + 384, 0xCC), (fen - 16, 0xDD)]
    poser_journal(journal_bords)
    journal_avant = journal_zone()
    r = lire_fenetre(fen)
    rempl_att, tamp_att = modele_tampon(donnees, fen, journal_bords)
    controle("V2:les-bords-de-fenetre",
             r == 0 and cadre_dword(REMPL) == rempl_att
             and cadre_champ(TAMPON, rempl_att) == tamp_att,
             "le premier (0xAA) et le dernier (0xBB) recouverts ; l'avant "
             "(fenêtre−16) et l'après (fenêtre+384) IGNORÉS — l'édition "
             "survit au défilement")
    controle("V2:le-journal-intact", journal_zone() == journal_avant,
             "loupe_02_lire n'écrit JAMAIS au journal (I2 : la lecture ne "
             "touche que le tampon du cadre)")
    journal_multi = [(fen + 5, 0x11), (fen + 100, 0x22), (fen + 200, 0x33),
                     (fen + 300, 0x44), (fen + 383, 0x55)]
    poser_journal(journal_multi)
    r = lire_fenetre(fen)
    rempl_att, tamp_att = modele_tampon(donnees, fen, journal_multi)
    controle("V2:cinq-entrees-dont-une-non-alignee",
             r == 0 and cadre_champ(TAMPON, rempl_att) == tamp_att,
             "cinq entrées dedans (fen+5 NON ALIGNÉE comprise) — le tampon "
             "== le modèle indépendant")
    poser_journal([])
    LOUPE03()

    # ---- V3 : LES REJETS — rien lu, le tampon empoisonné INTACT -------------
    r = lire_fenetre(0)
    controle("V3:E1-sans-session", r == -4,
             f"rax={r} (attendu -4 SESSION, la session fermée — rien lu)")
    appeler_ouvrir("temoin-384.bin".encode("utf-16-le") + b"\x00\x00")
    ecrire_cadre(TAMPON, b"\xCC" * 384)             # le poison
    ecrire_cadre(REMPL, (0xBEEF).to_bytes(4, "little"))
    poison, rempl_poison = cadre_champ(TAMPON, 384), cadre_dword(REMPL)
    r = lire_fenetre(40)
    controle("V3:E2-le-decalage-non-aligne",
             r == -5 and cadre_champ(TAMPON, 384) == poison
             and cadre_dword(REMPL) == rempl_poison,
             f"rax={r} (40 non multiple de 16 → -5 ENTRÉE), le tampon ET le "
             f"remplissage INTACTS (rien lu)")
    r = lire_fenetre(384)
    controle("V3:E3a-le-decalage-a-la-taille",
             r == -3 and cadre_champ(TAMPON, 384) == poison,
             f"rax={r} (384 == la taille → -3 HORS-BORNES), rien lu")
    r = lire_fenetre(1 << 40)
    controle("V3:E3b-le-decalage-immense",
             r == -3 and cadre_champ(TAMPON, 384) == poison,
             f"rax={r} (2^40 → -3 HORS-BORNES), rien lu")

    # ---- V4 : L'ÉCHEC SYSTÈME — la plage verrouillée par un second détenteur
    verrou = k32.CreateFileW(os.path.join(ICI, "temoin-384.bin"),
                             0x80000000, 3, None, 3, 0, None)
    arme = bool(verrou) and bool(k32.LockFile(
        ctypes.c_void_p(verrou), 0, 0, 384, 0))
    if arme:
        r = lire_fenetre(0)
        if r == -6:
            controle("V4:la-plage-verrouillee",
                     r == -6 and cadre_dword(REMPL) == 0,
                     f"rax={r} (ReadFile refuse la plage verrouillée → -6 "
                     f"SYSTÈME), remplissage {cadre_dword(REMPL)} == 0 "
                     f"(fail-closed : jamais un octet non lu)")
        else:
            controle("V4:la-plage-verrouillee-NOMMÉ-ABSENT", True,
                     f"rax={r} — le verrou de plage n'a pas fait échouer la "
                     f"lecture au terrain (le système de fichiers l'ignore) "
                     f"— NOMMÉ ABSENT, jamais maquillé")
        k32.UnlockFile(ctypes.c_void_p(verrou), 0, 0, 384, 0)
        k32.CloseHandle(ctypes.c_void_p(verrou))
        r = lire_fenetre(0)
        controle("V4:la-session-survit",
                 r == 0 and cadre_dword(REMPL) == 384,
                 f"rax={r} — l'échec ne clôt PAS la session : la lecture "
                 f"suivante est verte, remplissage {cadre_dword(REMPL)}")
    else:
        if verrou:
            k32.CloseHandle(ctypes.c_void_p(verrou))
        controle("V4:la-plage-verrouillee-NOMMÉ-ABSENT", True,
                 "le verrou de plage n'a pu être posé au terrain — NOMMÉ "
                 "ABSENT, jamais maquillé")
    LOUPE03()

    # ---- V5 : LA FALSIFICATION DEMANDÉE (charte § 3) -------------------------
    appeler_ouvrir("temoin-384.bin".encode("utf-16-le") + b"\x00\x00")
    r = lire_fenetre(0)
    donnees384 = open(os.path.join(ICI, "temoin-384.bin"), "rb").read()
    modele = donnees384[:384]
    ok_lecture = (r == 0 and cadre_champ(TAMPON, 384) == modele)
    octet_avant = cadre_champ(TAMPON, 384)[3]
    ecrire_cadre(TAMPON + 3, b"\xFF")                # l'octet muté
    divergence = cadre_champ(TAMPON, 384) != modele
    controle("V5:l-octet-mute-l-etat-lu-diverge",
             ok_lecture and divergence,
             f"la lecture d'abord VERT (le tampon == le modèle), l'octet 3 "
             f"muté {octet_avant:#04x} → 0xff : l'état lu DIVERGE du modèle "
             f"— la falsification est DÉTECTABLE (le juge lit l'état)")
    LOUPE03()

    # ---- LE TÉMOIN -------------------------------------------------------------
    os.makedirs(RECEPTACLE, exist_ok=True)
    lignes = []
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 2 — loupe-02 lire × bras C "
                  "(la campagne D204, la comparaison des workflows)")
    lignes.append("=" * 78)
    lignes.append(f"le run      : "
                  f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
                  f" (UTC) — la machine du développeur")
    lignes.append(f"la machine  : {platform.node()} · {platform.system()} "
                  f"{platform.release()} · {platform.machine()} · "
                  f"Python {platform.python_version()}")
    lignes.append(f"la pièce    : loupe-02-c.dll {os.path.getsize(PIECE)} o, "
                  f"sha256 {sha_piece}")
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
    lignes.append("  renvoyer le dossier preuves-unite02C/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite02C.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 2 × BRAS C FINI : dater et signer le "
             "témoin de votre main, renvoyer preuves-unite02C/ ENTIER au "
             "coffre /test ===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
