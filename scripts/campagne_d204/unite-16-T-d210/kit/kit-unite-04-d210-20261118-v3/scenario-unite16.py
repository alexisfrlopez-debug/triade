#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite16.py — LE TERRAIN DE L'UNITÉ 04 D210 (loupe-16 saisie × bras
T, la campagne D210 — LA PREMIÈRE unité À ÉTAT : le journal, le tampon, la
marque, la garde, la vue qui suit).

Le kit porte UNE pièce et UN scénario :
  loupe.exe          la pièce de campagne — le build du plan où le slot
                     loupe-16 (RVA 0x6240, 704 o) porte LA NOTATION DE
                     CAMPAGNE écrite à la main par l'agent (656 o, 178
                     instructions — le contrat loupe-16:R1 : DEUX chiffres
                     hexa composent l'octet — le premier ATTEND, le second
                     ENGAGE — l'octet AU JOURNAL DES ÉCRITURES (l'entrée par
                     décalage, la réécriture REMPLACE, la borne 256) ET au
                     tampon de vue (visible immédiatement), la marque SALE
                     posée, LA GARDE de loupe-18 RÉ-ARMÉE à chaque écriture,
                     le curseur AVANCE clampé et LA VUE SUIT (le recadrage,
                     loupe-02 le scellé RE-LIT, la feuille InvalidateRect
                     repeint) ; E1 -4 sans session, E2 -3 la cellule fantôme,
                     E3 -3 le journal plein, E4 le non-hexa ignoré,
                     VK_SUPPR à l'attente) ;
  le présent script  python SEUL (ctypes, hashlib, os, platform, random,
                     struct, sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (la leçon des Entrées 302/304 reconduite) : le
scénario est LE CHARGEUR — LoadLibraryEx DONT_RESOLVE (aucune entrée
résolue) PUIS LE GUICHET FAIL-CLOSED : les FEUILLES du chemin (user32
InvalidateRect pour le repeint, kernel32 SetFilePointerEx + ReadFile pour
la relecture de loupe-02 le scellé) LIÉES PAR LA TABLE D'IMPORTS — chaque
slot découvert PAR SES NOMS (la dll, la fonction), JAMAIS une RVA codée ;
chaque geste vérifié (VirtualProtect l'instant de l'écriture, la
re-protection, la relecture recoupée) ; tout écart = REFUS NOMMÉ, RIEN ne
court (le miroir du guichet de la 304, étendu aux TROIS feuilles).
L'ÉTAT posé directement aux ZONES DU PLAN (base + 0xE000 le cadre, +
0xE400 la saisie, + 0xE4A0 le journal) — le disque VIVANT par poignée
réelle (CreateFileW du témoin : loupe-02 RE-LIT le disque pour de vrai,
le recouvrement du journal par-dessus). Le juge est le MODÈLE
INDÉPENDANT (le miroir Python de l'oracle du labo, la même graine
20261115).

LA RÉVISION 2 (le correctif du refus nommé — le run v1 du 18/11 12:12,
« [REFUS] RVA-HOURS-SECTIONS : la RVA 0x0 hors des sections », rien ne
courut) : LE GUICHET corrigé sur SES DEUX fautes nommées — ① le
descripteur d'import lu à QUATRE champs (le champ +8 ForwarderChain lu
comme la RVA du nom, la RVA du nom lue comme le FirstThunk, le champ
+16 jamais lu) → LE PARSE AUX CINQ CHAMPS (le précédent de la 304) ;
② LA MARCHE : la découverte marchait l'OFT au pas de qword — mais
l'OFT de la famille vit au pas de DWORD (la retouche dev.8) et la
doctrine du plan loupe consigne LE CHARGEUR MARCHANT LES PLAGES
FIRSTTHUNK jusqu'au séparateur NULL, chaque entrée sur disque == le
RVA hint/nom de SA feuille (D54, l'Entrée 210) → LA MARCHE DES PLAGES
FT au pas de qword — les feuilles mortes comprises : SetFilePointerEx,
ReadFile ET GetLastError (le chemin d'échec de la relecture : les jz de
loupe-02 atterrissent au -6 PAR GetLastError) et InvalidateRect (l'appel
de loupe-16) découvertes PAR LA TABLE, à LEURS slots — LES QUATRE feuilles
du chemin, la liste fermée des notations. LES VECTEURS INTACTS au byte
près ; l'épreuve du guichet née au labo — la découverte rejouée contre
le fichier livré (la règle de la 304 étendue au premier terrain à
état).

LES VECTEURS DU CONTRAT (loupe-16 révision 1) :
  V1  le différentiel : 10 000 frappes (hexa des deux casses, ~2 %
      VK_SUPPR, ~2 % non-hexa ; les ré-écritures des mêmes décalés, la
      frontière des 256 DISTINCTS) : le journal + le tampon + l'attente +
      le curseur + la vue + la marque + LA GARDE == le modèle à CHAQUE
      frappe ;
  V2  le scénario doré : « 4d5a » au curseur 0x22 (les DEUX octets au
      journal ET au tampon, la marque, la garde, la cellule suivante) ET
      LA VUE QUI SUIT (le curseur au bord → le recadrage, LA RELECTURE,
      le recouvrement) ;
  V3  les rejets : E1 sans session → -4 la barre nommée ; E2 la cellule
      fantôme → -3 RIEN au journal ; E3 le 257e distinct → -3 « journal
      plein - Ctrl+S », RIEN perdu ;
  V4  le repli : « z », « ! », l'espace IGNORÉS ; VK_SUPPR à l'attente →
      le nibble effacé ;
  V5  la falsification demandée : LE DISQUE FALSIFIÉ (l'octet de la
      fenêtre re-lue muté) : le tampon après la relecture == le modèle du
      MUTANT (divergent de l'original) — la pièce a lu SON disque à elle,
      la différentielle attrape le faux (le fixture falsifie-16.bin vit
      au réceptacle preuves-unite16/, renvoyé ENTIER avec le témoin).

  le témoin : temoin-unite16.txt au réceptacle preuves-unite16/ —
  DATER ET SIGNER DE VOTRE MAIN (jamais automatisé, D99), renvoyer le
  dossier ENTIER au coffre /test.
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import datetime as dt
import hashlib
import os
import platform
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(ICI, "loupe.exe")
TEMOIN = os.path.join(ICI, "temoin-3f.bin")
RECEPTACLE = os.path.join(ICI, "preuves-unite16")

R_LOUPE16 = 0x6240              # le slot du plan (loupe/layout.py — la source unique)
R_CADRE = 0xE000
R_SAISIE = 0xE400
R_JOURNAL = 0xE4A0
GRAINE = 20261115
TAMPON = 384
EDITS = 256
WM_CHAR = 0x102
VK_SUPPR = 0x08

REUSSITES, ECARTS = [], []
PAGE_RW = 0x04


def consigne(ligne: str) -> None:
    print(ligne, flush=True)


def verdict(rax: int) -> int:
    v = rax & 0xFFFFFFFF
    return v - 0x100000000 if v > 0x7FFFFFFF else v


def controle(nom: str, ok: bool, detail: str = "") -> None:
    consigne(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
             + (f" — {detail}" if detail else ""))
    (REUSSITES if ok else ECARTS).append(nom)


def refus(nom: str, detail: str) -> None:
    consigne(f"[REFUS] {nom} : {detail} — RIEN ne court, le guichet ferme")
    sys.exit(2)


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


# ---- LE MODÈLE INDÉPENDANT (jamais les octets du bloc) ---------------------


def m_journal_seconde(journal: list, curseur: int, octet: int):
    for i, (dec, _) in enumerate(journal):
        if dec == curseur:
            journal[i] = (curseur, octet)
            return journal, False
    if len(journal) >= EDITS:
        return journal, True
    journal.append((curseur, octet))
    return journal, False


def m_vue_suit(curseur: int, vue: int, taille: int, lignes: int = 27):
    v = min(24, max(0, lignes - 3))
    if vue <= curseur < vue + v * 16:
        return vue, False
    nv = min((max(0, curseur - 176)) & ~15,
             (max(0, taille - TAMPON) + 15) & ~15 if taille > TAMPON else 0)
    return nv, nv != vue


def fenetre_editee(disk: bytes, journal: list, vue: int, remplissage: int):
    fen = bytearray(disk[vue:vue + remplissage])
    for dec, oct_ in journal:
        if vue <= dec < vue + remplissage:
            fen[dec - vue] = oct_
    return bytes(fen)


# ---- LE GUICHET FAIL-CLOSED : les feuilles liées PAR LA TABLE D'IMPORTS ----


def lier_feuilles(base: int) -> None:
    """L1 : la feuille DÉCOUVERTE PAR LA TABLE (les noms, jamais une RVA) ;
    L2 : la liaison AVANT TOUT appel ; L3 : chaque geste vérifié
    (VirtualProtect + la re-protection + la relecture recoupée)."""
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                   wt.DWORD, ctypes.POINTER(wt.DWORD)]
    k32.VirtualProtect.restype = wt.BOOL
    exe = open(EXE, "rb").read()
    e = struct.unpack_from("<I", exe, 0x3C)[0]
    opt = struct.unpack_from("<H", exe, e + 20)[0]
    # (la table des imports : LE RÉPERTOIRE 1 des données — DataDirectory[1],
    #  l'option PE32+ : le répertoire vit à e+24+112+8, sa RVA lue là)
    dir_imports = struct.unpack_from("<I", exe, e + 24 + 112 + 8)[0]
    nb = struct.unpack_from("<H", exe, e + 6)[0]
    sections = []
    for k in range(nb):
        o = e + 24 + opt + k * 40
        va = struct.unpack_from("<I", exe, o + 12)[0]
        vs = struct.unpack_from("<I", exe, o + 8)[0]
        ra = struct.unpack_from("<I", exe, o + 20)[0]
        sections.append((va, vs, ra))
    for va, vs, ra in sections:
        if va <= dir_imports < va + vs:
            dir_imports = ra + (dir_imports - va)
    cible = dir_imports
    feuilles = {}          # (dll, nom) -> slot RVA (remplies par la table)
    while True:
        # LE DESCRIPTTEUR AUX CINQ CHAMPS (le précédent de la 304) : l'OFT
        # (+0), l'horodatage (+4), le renvoi (+8), LE NOM (+12), LE
        # FIRSTTHUNK (+16) — le v1 aux quatre champs lisait le renvoi
        # (+8, la valeur 0) comme la RVA du nom : LA RVA 0x0 DU REFUS
        oft, tds, chaine, nom_rva, ft = struct.unpack_from("<IIIII", exe, cible)
        if oft == 0 and ft == 0 and nom_rva == 0:
            break
        dll = exe[ra_of(sections, nom_rva):].split(b"\x00")[0].decode("ascii")
        # LA MARCHE DU CHARGEUR (D54, l'Entrée 210 — la doctrine du plan
        # loupe) : la plage FirstThunk marchée au pas de qword JUSQU'AU
        # séparateur NULL, chaque entrée sur disque == le RVA hint/nom de
        # SA feuille (le préremplissage) — les feuilles mortes comprises
        # (jamais liées par un chargeur ordinaire, liées par le guichet) ;
        # l'OFT au pas de dword de la retouche dev.8 n'est JAMAIS marché
        # (le plan loupe le consigne : la vérification dérive des plages
        # FT, jamais de l'OFT)
        i = 0
        while True:
            entree = struct.unpack_from("<Q", exe, ra_of(
                sections, ft) + 8 * i)[0]
            if entree == 0:
                break
            if not entree & (1 << 63):        # par NOM (l'entrée hint/nom)
                nom = exe[ra_of(sections, entree & 0x7FFFFFFF) + 2:] \
                    .split(b"\x00")[0].decode("ascii")
                if (dll.lower(), nom) not in feuilles:
                    feuilles[(dll.lower(), nom)] = ft + 8 * i
            i += 1
        cible += 20
    voulues = {("user32.dll", "InvalidateRect"),
               ("kernel32.dll", "SetFilePointerEx"),
               ("kernel32.dll", "ReadFile"),
               ("kernel32.dll", "GetLastError")}   # la 4e : le chemin
               # d'échec de loupe-02 (les jz → le -6 LU PAR GetLastError
               # — la feuille morte liée AVANT le premier échec réel)
    for cle in voulues:
        if cle not in feuilles:
            refus("L1-FEUILLE-INTROUVABLE",
                  f"{cle[1]}@{cle[0]} absent de la table d'imports")
    for (dll, nom), slot in feuilles.items():
        if (dll, nom) not in voulues:
            continue
        adresse = base + slot
        bibli = ctypes.WinDLL(dll)
        proc = ctypes.cast(getattr(bibli, nom), ctypes.c_void_p).value
        if not proc:
            refus("L3-GETPROCADDRESS", f"{nom}@{dll} introuvable")
        ancienne = wt.DWORD(0)
        if not k32.VirtualProtect(adresse, 8, PAGE_RW, ctypes.byref(ancienne)):
            refus("L3-VIRTUALPROTECT", f"{nom} : {ctypes.get_last_error()}")
        ctypes.memmove(adresse, struct.pack("<Q", proc), 8)
        if not k32.VirtualProtect(adresse, 8, ancienne.value,
                                  ctypes.byref(ancienne)):
            refus("L3-REPROTECTION", f"{nom} : {ctypes.get_last_error()}")
        relue = struct.unpack("<Q", bytes(
            ctypes.string_at(adresse, 8)))[0]
        if relue != proc:
            refus("L3-RELECTURE", f"{nom} : la relecture diverge")
    consigne("[guichet] les QUATRE feuilles liées par la table d'imports : "
             "user32 InvalidateRect (le repeint de loupe-16), kernel32 "
             "SetFilePointerEx + ReadFile (la relecture de loupe-02 le "
             "scellé) ET GetLastError (le chemin d'échec de la relecture — "
             "le -6 nommé) — chaque geste vérifié, la re-protection posée, "
             "la relecture recoupée")


def ra_of(sections, rva: int) -> int:
    for va, vs, ra in sections:
        if va <= rva < va + vs:
            return ra + (rva - va)
    refus("RVA-HORS-SECTIONS", f"la RVA {rva:#x} hors des sections")


# ---- L'ÉTAT AUX ZONES DU PLAN ----------------------------------------------


class Zones:
    """Le cadre, la saisie, le journal — LUS ET ÉCRITS aux adresses du plan."""

    def __init__(self, base: int, disk: bytes, poignee: int):
        self.base = base
        self.disk = disk
        self.cadre = base + R_CADRE
        self.saisie = base + R_SAISIE
        self.journal = base + R_JOURNAL
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateFileW.restype = ctypes.c_void_p
        k32.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD,
                                     ctypes.c_void_p, wt.DWORD, wt.DWORD,
                                     ctypes.c_void_p]
        self.poignee = poignee
        self.poser_session(disk, poignee)

    def poser_session(self, disk: bytes, poignee: int) -> None:
        taille = len(disk)
        rempl = min(TAMPON, taille)
        self.ecrire(520, struct.pack("<Q", taille))
        self.ecrire(528, struct.pack("<Q", poignee))
        self.ecrire(536, struct.pack("<Q", 0))
        self.ecrire(544, struct.pack("<Q", 0x22))
        self.ecrire(552, struct.pack("<I", rempl))
        self.ecrire(556, struct.pack("<I", 0))
        self.ecrire(560, struct.pack("<I", 0))
        ctypes.memmove(self.cadre + 568,
                      bytes(disk[:rempl].ljust(TAMPON, b"\x00")), TAMPON)
        ctypes.memset(self.saisie, 0, 96)
        ctypes.memset(self.journal, 0, 4112)

    def ecrire(self, off, donnees) -> None:
        ctypes.memmove(self.cadre + off, donnees, len(donnees))

    def u64(self, off) -> int:
        return struct.unpack("<Q", bytes(
            ctypes.string_at(self.cadre + off, 8)))[0]

    def u32(self, off) -> int:
        return struct.unpack("<I", bytes(
            ctypes.string_at(self.cadre + off, 4)))[0]

    def attente(self):
        brut = bytes(ctypes.string_at(self.saisie + 4, 8))
        return struct.unpack("<II", brut)

    def barre(self) -> bytes:
        return bytes(ctypes.string_at(self.saisie + 12, 80)).split(b"\x00")[0]

    def journal_lu(self) -> list:
        n = self.u32_journal()
        entrees = []
        for i in range(n):
            dec = struct.unpack("<Q", bytes(
                ctypes.string_at(self.journal + 16 * i, 8)))[0]
            oct_ = bytes(ctypes.string_at(self.journal + 16 * i + 8, 1))[0]
            entrees.append((dec, oct_))
        return entrees

    def u32_journal(self) -> int:
        return struct.unpack("<I", bytes(
            ctypes.string_at(self.journal + 4096, 4)))[0]

    def poser_journal(self, entrees) -> None:
        ctypes.memset(self.journal, 0, 4112)
        brut = bytearray()
        for dec, oct_ in entrees:
            brut += struct.pack("<QB7x", dec, oct_)
        ctypes.memmove(self.journal, bytes(brut), len(brut))
        ctypes.memmove(self.journal + 4096,
                       struct.pack("<I", len(entrees)), 4)

    def tampon(self) -> bytes:
        return bytes(ctypes.string_at(self.cadre + 568, TAMPON))


def main() -> int:
    consigne("=== LE RUN DE L'UNITÉ 04 D210 (loupe-16 saisie × bras T) — la "
             "campagne D210, le terrain du développeur ===")
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

    # LE GUICHET : les TROIS feuilles du chemin liées AVANT TOUT appel (L2)
    lier_feuilles(base)

    SAISIR = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_uint64,
                              ctypes.c_uint64, ctypes.c_uint64,
                              ctypes.c_uint64)(base + R_LOUPE16)

    def frapper(caractere: int):
        return verdict(SAISIR(0x770001, WM_CHAR, caractere, 0))

    disk = open(TEMOIN, "rb").read()
    taille = len(disk)
    GENERIC_READ = 0x80000000
    OPEN_EXISTING = 3
    FILE_SHARE_READ = 1
    handle = k32.CreateFileW(TEMOIN, GENERIC_READ, FILE_SHARE_READ,
                             None, OPEN_EXISTING, 0, None)
    if handle in (0, (1 << 64) - 1):
        refus("CREATEFILEW", f"le témoin introuvable ({ctypes.get_last_error()})")
    z = Zones(base, disk, handle)
    rng = random.Random(GRAINE)
    hexa = b"0123456789abcdefABCDEF"
    bruit = b"z! "

    # ---- V1 : LE DIFFÉRENTIEL — 10 000 frappes ------------------------------
    journal, m_tampon = [], bytearray(disk[:TAMPON])
    curseur, vue, rempl = 0x22, 0, min(TAMPON, taille)
    m_actif, m_nibble = 0, 0
    divergences = 0
    for _ in range(10_000):
        tirage = rng.random()
        frappe = VK_SUPPR if tirage < 0.02 else (
            rng.choice(bruit) if tirage < 0.04 else rng.choice(hexa))
        r = frapper(frappe)
        if frappe == VK_SUPPR:
            if m_actif:
                m_actif = 0
        elif chr(frappe) in "0123456789abcdefABCDEF":
            valeur = int(chr(frappe), 16)
            if not m_actif:
                m_actif, m_nibble = 1, valeur
            else:
                m_actif = 0
                octet = (m_nibble << 4) | valeur
                journal, refuse = m_journal_seconde(journal, curseur, octet)
                if not refuse:
                    if vue <= curseur < vue + rempl:
                        m_tampon[curseur - vue] = octet
                    curseur = min(curseur + 1, taille - 1)
                    nv, relu = m_vue_suit(curseur, vue, taille)
                    if relu:
                        vue = nv
                        rempl = min(TAMPON, taille - vue)
                        m_tampon = bytearray(
                            fenetre_editee(disk, journal, vue, rempl))
        probleme = None
        if r not in (0, -3):
            probleme = f"le verdict {r} inattendu"
        attente = z.attente()
        if probleme is None and attente != (m_actif, m_nibble if m_actif else 0):
            probleme = "l'attente diverge"
        elif probleme is None and z.journal_lu() != journal:
            probleme = "le journal diverge"
        elif probleme is None and (z.u64(544) != curseur or z.u64(536) != vue):
            probleme = "le curseur ou la vue divergent"
        elif probleme is None and z.u32(552) != rempl:
            probleme = "le remplissage diverge"
        elif probleme is None and z.tampon() != bytes(m_tampon):
            probleme = "le tampon diverge"
        elif probleme is None and z.u32(556) != (1 if journal else 0):
            probleme = "la marque diverge"
        elif probleme is None and z.u32(560) != 0:
            probleme = "la garde diverge"
        if probleme:
            divergences += 1
            if divergences <= 3:
                consigne(f"    [V1] {probleme}")
    controle("V1:le-differentiel-10000-frappes", divergences == 0,
             "le journal PAR DÉCALAGE (la réécriture REMPLACE, la borne 256 "
             "refusée), l'attente CONSOMMÉE par l'engagement, le tampon de "
             "vue (le recouvrement immédiat), la marque sale, LA GARDE "
             "RÉ-ARMÉE à chaque écriture, le pas clampé, LA VUE QUI SUIT "
             "(loupe-02 re-lit le DISQUE VIVANT) — tout == le modèle Python")

    # ---- V2 : LE SCÉNARIO DORÉ + LA VUE QUI SUIT ----------------------------
    z.poser_session(disk, handle)
    for ch in (0x34, 0x64, 0x35, 0x61):          # 4 d 5 a
        r = frapper(ch)
    controle("V2:le-scenario-4d5a", r == 0
             and z.u64(544) == 0x24 and z.u32(556) == 1 and z.u32(560) == 0
             and z.journal_lu() == [(0x22, 0x4D), (0x23, 0x5A)]
             and z.tampon()[0x22] == 0x4D and z.tampon()[0x23] == 0x5A,
             "« 4d5a » au curseur 0x22 : les DEUX octets au journal ET au "
             "tampon (visibles immédiatement), la marque sale, LA GARDE "
             "ré-armée, la cellule suivante active (curseur 0x24)")
    z.poser_session(disk, handle)
    z.ecrire(544, struct.pack("<Q", TAMPON - 1))     # 383 — le bord de la vitrine
    z.ecrire(536, struct.pack("<Q", 0))
    curseur0 = TAMPON - 1
    for ch in (0x34, 0x61):
        r = frapper(ch)                                # « 4a » au bord
    attendu_vue = m_vue_suit(curseur0 + 1, 0, taille)[0]
    attendu_tampon = fenetre_editee(disk, [(curseur0, 0x4A)],
                                    attendu_vue, TAMPON)
    controle("V2:la-vue-qui-suit-le-recadrage", r == 0
             and z.u64(544) == curseur0 + 1
             and z.u64(536) == attendu_vue
             and z.u32(552) == TAMPON
             and z.tampon()[:TAMPON] == attendu_tampon,
             f"le curseur au-delà de la vitrine → la nouvelle vue "
             f"{attendu_vue:#x} (aligne16_inf), LA RELECTURE par loupe-02 le "
             "scellé (le disque vivant, le recouvrement du journal au "
             "tampon) — la cellule suivante ATTEND à l'écran")

    # ---- V3 : LES REJETS -----------------------------------------------------
    z.ecrire(528, struct.pack("<Q", (1 << 64) - 1))        # hors session
    r = frapper(0x34)
    controle("V3:E1-sans-session", r == -4
             and z.barre() == b"aucun fichier ouvert",
             "sans session ouverte → -4, la phrase nommée à la barre")
    z.poser_session(disk, handle)
    z.ecrire(544, struct.pack("<Q", TAMPON + 5))           # la cellule fantôme
    z.ecrire(536, struct.pack("<Q", 0))
    ctypes.memmove(z.saisie + 4, struct.pack("<II", 1, 4), 8)
    r = frapper(0x64)
    attente = z.attente()
    controle("V3:E2-la-cellule-fantome", r == -3
             and z.journal_lu() == [] and attente == (0, 0)
             and z.barre() == b"hors bornes",
             "le curseur forgé au-delà du remplissage → -3 « hors bornes », "
             "RIEN au journal (le refus PRÉCÈDE), l'attente CONSOMMÉE")
    z.poser_session(disk, handle)
    entrees = [(0x40 + i, (i * 7) & 0xFF) for i in range(EDITS)]
    z.poser_journal(entrees)
    ctypes.memmove(z.saisie + 4, struct.pack("<II", 1, 4), 8)
    r = frapper(0x64)
    controle("V3:E3-le-257e-distinct", r == -3
             and z.journal_lu() == entrees
             and z.barre() == b"journal plein - Ctrl+S",
             "le 257e distinct → -3 « journal plein - Ctrl+S », les 256 "
             "premiers INTACTS (RIEN perdu)")

    # ---- V4 : LE REPLI -------------------------------------------------------
    z.poser_journal([])
    ctypes.memset(z.saisie, 0, 96)
    for ch in (0x7A, 0x21, 0x20):                  # z ! espace
        r = frapper(ch)
        if r != 0:
            break
    frapper(0x34)
    frapper(VK_SUPPR)
    attente = z.attente()
    r = frapper(VK_SUPPR)
    controle("V4:le-repli-les-ignores", r == 0 and attente == (0, 0)
             and z.journal_lu() == [],
             "« z », « ! », l'espace IGNORÉS proprement (rax = 0, rien "
             "bougé) ; « 4 » frappé puis VK_SUPPR : le nibble EFFACÉ (le "
             "premier chiffre repart) ; hors attente : ignoré")

    # ---- V5 : LA FALSIFICATION — le disque falsifié -------------------------
    os.makedirs(RECEPTACLE, exist_ok=True)
    z.poser_session(disk, handle)
    z.ecrire(544, struct.pack("<Q", TAMPON - 1))
    z.ecrire(536, struct.pack("<Q", 0))
    curseur0 = TAMPON - 1
    fen = bytearray(disk[curseur0:curseur0 + TAMPON])
    mutant_offset = curseur0 + 8                       # un octet de la fenêtre re-lue
    fen[8] ^= 0x35                                     # l'octet muté
    chemin_faux = os.path.join(RECEPTACLE, "falsifie-16.bin")
    with open(chemin_faux, "wb") as f:                 # le disque falsifié
        f.write(bytes(disk[:mutant_offset])
                + bytes([fen[8]]) + disk[mutant_offset + 1:])
    handle_faux = k32.CreateFileW(chemin_faux, GENERIC_READ, FILE_SHARE_READ,
                                 None, OPEN_EXISTING, 0, None)
    disk_faux = open(chemin_faux, "rb").read()
    z.poser_session(disk_faux, handle_faux)
    z.ecrire(544, struct.pack("<Q", curseur0))
    z.ecrire(536, struct.pack("<Q", 0))
    for ch in (0x34, 0x61):                            # « 4a » au bord → la relecture
        r = frapper(ch)
    tampon_faux = z.tampon()[:TAMPON]
    original = fenetre_editee(disk, [(curseur0, 0x4A)], attendu_vue, TAMPON)
    mutant = fenetre_editee(disk_faux, [(curseur0, 0x4A)], attendu_vue, TAMPON)
    controle("V5:le-disque-falsifie-attrape", r == 0
             and tampon_faux != original
             and tampon_faux == mutant,
             "le disque falsifié (l'octet 8 de la fenêtre re-lue muté) : le "
             "tampon après la relecture == le modèle du MUTANT (divergent de "
             "l'original) — la pièce a lu SON disque à elle par la poignée "
             "fausse, la différentielle ATTRAPE LE FAUX (le fixture "
             "falsifie-16.bin vit au réceptacle)")
    k32.CloseHandle(handle_faux)
    k32.CloseHandle(handle)

    # ---- LE TÉMOIN -----------------------------------------------------------
    lignes = []
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 04 D210 — loupe-16 saisie × bras T "
                  "(la campagne D210, la comparaison des workflows)")
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
    lignes.append("  renvoyer le dossier preuves-unite16/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite16.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 04 D210 FINI : dater et signer le témoin de "
             "votre main, renvoyer preuves-unite16/ ENTIER au coffre /test "
             "===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
