#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""comparer_v140.py — LE COMPARATEUR DU BRAS DE RÉFÉRENCE COMPILATEUR
(v0.14.0, point 1 de la commande ic09ydeli — le plan pré-enregistré
D193 : scripts/preuves_v140/PLAN_PREENREGISTRE_v140.md).

LES DEUX CAMPS, LE MÊME TERRAIN :
  - camp A : les blocs scellés de Loupe (la notation à la main) posés par
    le harnais ÉDITION (EmulationEdition ⊃ rendu ⊃ noyau : les 18 blocs,
    le mini-OS, les shims, le cadre au plan) ;
  - camp C : la référence compilée (bras_c.c, -O2 et -Os) DEPUIS LES MÊMES
    CONTRATS, chargée dans le MÊME mini-OS (une émulation noyau fraîche),
    les primitives OS prises par table de pointeurs AUX MÊMES SHIMS
    (l'inverse de adr_shims) — CA2 du plan.

LES MESURES : les vecteurs des contrats (le modèle indépendant Python :
hashlib, le format 77 o, bytes.find, le journal par décalage), les
instructions PAR OPÉRATION COMPLÈTE au même crochet (la convention D191 :
jamais une lecture de compteur intermédiaire), les tailles au bon
périmètre (le bloc au plan / la fonction seule), la mutation (16
mutants/bloc, graine 20261111, le protocole v0.11.0 : une instruction au
hasard, un octet au hasard, une valeur différente — le MÊME tirage pour
les deux camps).

LES TUEURS (les adaptations NOMMÉES, CA4) : camp A — K2-décodage
(capstone : un mutant indécodable est mort ; le round-trip keystone de la
campagne v0.11.0 n'est pas rejoué ici, l'écart est nommé au rapport) et
K3 (les vecteurs au modèle) ; camp C — K3 (les mêmes vecteurs) et
K2-adapté (les comptes d'appels OS des blocs OS contre la référence ; le
round-trip est EXCLU par nature — la commande le dit). Le taux COMMUN
rapporté : K3 seul ; chaque campporte en plus son tueurs propres.

Sorties : scripts/preuves_v140/bras_c.csv + bras_c_rapport.txt.
"""
from __future__ import annotations

import csv
import ctypes
import hashlib
import importlib.util
import pathlib
import random
import struct
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
PREUVES = REPO / "scripts" / "preuves_v140"
CDIR = REPO / "scripts" / "bras_c_v140"

import capstone  # noqa: E402
from unicorn import UC_HOOK_CODE  # noqa: E402

BASE_BRAS = 0x1400000
TABLE_OS = 0x730000
CADRE_C = 0x740000
ZONE_TAMPON_C = 0x760000          # les entrées/sorties des blocs purs C
GRAINE_MUT = 20261111
GRAINE_VEC = 20261113

BLOCS = ["loupe-01", "loupe-02", "loupe-05", "loupe-08", "loupe-13",
         "loupe-16"]
FONCTIONS_C = {"loupe-01": "loupe01_ouvrir", "loupe-02": "loupe02_lire",
               "loupe-05": "loupe05_sha256", "loupe-08": "loupe08_ligne",
               "loupe-13": "loupe13_recherche",
               "loupe-16": "loupe16_saisie"}
VA_A = {}                          # rempli au démarrage (les VA du plan)


def charger_module(nom: str, chemin: pathlib.Path):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


HN = charger_module("h_noyau_v140", REPO / "loupe" / "harnais_noyau.py")
HE = charger_module("h_edition_v140", REPO / "loupe" / "harnais_edition.py")
L = HN.L
for _bid in BLOCS:
    VA_A[_bid] = getattr(L, f"LOUPE{_bid[-2:]}_VA")


# ------------------------------------------------------------ la compilation

def compiler(niveau: str):
    obj = CDIR / f"bras_{niveau}.o"
    exe = CDIR / f"bras_{niveau}.elf"
    plat = CDIR / f"bras_{niveau}.bin"
    subprocess.run(["gcc", f"-{niveau}", "-fno-pic", "-no-pie",
                    "-ffreestanding", "-fno-asynchronous-unwind-tables",
                    "-c", str(CDIR / "bras_c.c"), "-o", str(obj)], check=True)
    script = CDIR / f"lie_{niveau}.ld"
    script.write_text(f"""
SECTIONS {{
  . = {BASE_BRAS:#x};
  .text : {{ *(.text*) }}
  .rodata : {{ *(.rodata*) }}
  .data : {{ *(.data*) }}
  /DISCARD/ : {{ *(.comment) *(.note*) }}
}}
""", encoding="utf-8")
    subprocess.run(["gcc", "-nostdlib", "-no-pie", "-static",
                    "-Wl,-T," + str(script), str(obj), "-o", str(exe)],
                   check=True)
    subprocess.run(["objcopy", "-O", "binary", "--only-section=.text*",
                    "--only-section=.rodata*", "--only-section=.data*",
                    str(exe), str(plat)], check=True)
    nms = subprocess.run(["nm", "-S", "--defined-only", str(exe)],
                         capture_output=True, text=True).stdout
    symboles = {}
    for ligne in nms.splitlines():
        p = ligne.split()
        if len(p) == 4 and p[3] in list(FONCTIONS_C.values()) + \
                ["os", "cadre_ptr"]:
            symboles[p[3]] = (int(p[0], 16), int(p[1], 16))
    return plat.read_bytes(), symboles, exe


# ------------------------------------------------- le cadre C (le miroir ABI)

class CadreC(ctypes.Structure):
    _fields_ = [("chemin", ctypes.c_uint16 * 260),
                ("reserve0", ctypes.c_uint64),
                ("taille", ctypes.c_uint64),
                ("poignee", ctypes.c_uint64),
                ("remplissage", ctypes.c_uint64),
                ("tampon", ctypes.c_uint8 * 384),
                ("vue", ctypes.c_uint64),
                ("curseur", ctypes.c_uint64),
                ("sale", ctypes.c_uint32),
                ("refus_quitter", ctypes.c_uint32),
                ("nibble", ctypes.c_uint8),
                ("journal_n", ctypes.c_uint32),
                ("journal", ctypes.c_uint8 * (256 * 16)),
                ("cumul", ctypes.c_uint8 * 65536),
                ("sortie32", ctypes.c_uint8 * 32)]


OFF = {n: getattr(CadreC, n).offset for n, _ in CadreC._fields_}
TAILLE_CADRE_C = ctypes.sizeof(CadreC)


class CampC:
    """La référence compilée dans le mini-OS du harnais noyau."""

    def __init__(self, image: bytes, symboles: dict):
        os_v = HN.OSVirtuel()
        self.os = os_v
        self.emul = HN.Emulation(os_v)
        ucx = self.emul.uc
        ucx.mem_map(BASE_BRAS, 0x80000)
        ucx.mem_write(BASE_BRAS, image)
        inverse = {feuille: adr for adr, feuille in
                   self.emul.adr_shims.items()}
        champs = ["CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                  "ReadFile", "CloseHandle", "GetLastError"]
        ucx.mem_map(TABLE_OS, 0x4000)
        ucx.mem_write(TABLE_OS, b"".join(struct.pack("<Q", inverse[c])
                                         for c in champs))
        ucx.mem_map(ZONE_TAMPON_C, 0x2000)   # les entrées/sorties des purs
        pages = ((TAILLE_CADRE_C + 0xFFF) // 0x1000) * 0x1000
        ucx.mem_map(CADRE_C, pages)
        ucx.mem_write(CADRE_C, b"\x00" * TAILLE_CADRE_C)
        for nom, cible in (("os", TABLE_OS), ("cadre_ptr", CADRE_C)):
            adr, _ = symboles[nom]
            ucx.mem_write(adr, struct.pack("<Q", cible))
        self.symboles = symboles
        self.compteur = 0
        self.actif = False
        ucx.hook_add(UC_HOOK_CODE, self._crochet)

    def _crochet(self, uc_, adresse, taille, donnees):
        if self.actif:
            self.compteur += 1

    def appeler(self, fonction: str, args: dict, pile5: int | None = None):
        va, _ = self.symboles[fonction]
        self.compteur = 0
        self.actif = True
        try:
            r = _appel_avec_pile5(self.emul, va, args, pile5)
        finally:
            self.actif = False
        r["instructions"] = self.compteur
        return r

    def u64(self, champ: str) -> int:
        return struct.unpack("<Q", self.emul.uc.mem_read(
            CADRE_C + OFF[champ], 8))[0]

    def octets(self, adr: int, n: int) -> bytes:
        return bytes(self.emul.uc.mem_read(adr, n))

    def ecrire(self, adr: int, donnees: bytes) -> None:
        self.emul.uc.mem_write(adr, donnees)

    def ouvrir(self, chemin: str, contenu: bytes | None = None,
               taille: int | None = None, verrouille: bool = False):
        if contenu is not None:
            self.os.declarer(chemin, HN.FichierVirtuel(contenu=contenu))
        elif taille is not None:
            self.os.declarer(chemin, HN.FichierVirtuel(taille=taille))
        if verrouille:
            self.os.declarer(chemin, HN.FichierVirtuel(contenu=b"x",
                                                       verrouille=True))
        self.emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                               chemin.encode("utf-16-le") + b"\x00\x00")
        return self.appeler("loupe01_ouvrir", {"rcx": HN.ADRESSE_CHEMIN})

    def fermer(self):
        """Le miroir de fermer_session : le cadre re-vierge (la poignée
        au néant — la session close pour les vecteurs suivants)."""
        self.emul.uc.mem_write(CADRE_C, b"\x00" * TAILLE_CADRE_C)

    def journal(self) -> list:
        n = struct.unpack("<I", self.emul.uc.mem_read(
            CADRE_C + OFF["journal_n"], 4))[0]
        base = CADRE_C + OFF["journal"]
        out = []
        for i in range(n):
            dec = struct.unpack("<Q", self.emul.uc.mem_read(
                base + 16 * i, 8))[0]
            out.append((dec, self.emul.uc.mem_read(base + 16 * i + 8, 1)[0]))
        return out


class CampA:
    """Les blocs scellés dans le harnais ÉDITION."""

    def __init__(self):
        os_v = HE.OSEdition()
        self.os = os_v
        self.emul = HE.EmulationEdition(
            os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
            (REPO / "m1" / "selftest.exe").read_bytes(),
            (REPO / "demo" / "demo.exe").read_bytes())
        self.compteur = 0
        self.actif = False
        self.emul.uc.hook_add(UC_HOOK_CODE, self._crochet)

    def _crochet(self, uc_, adresse, taille, donnees):
        if self.actif:
            self.compteur += 1

    def appeler(self, bid: str, args: dict, pile5: int | None = None):
        self.compteur = 0
        self.actif = True
        try:
            r = _appel_avec_pile5(self.emul, VA_A[bid], args, pile5)
        finally:
            self.actif = False
        r["instructions"] = self.compteur
        return r

    def ouvrir(self, chemin: str, contenu: bytes | None = None,
               taille: int | None = None, verrouille: bool = False):
        if contenu is not None:
            self.os.declarer(chemin, HE.FichierEditable(contenu=contenu))
        elif taille is not None:
            self.os.declarer(chemin, HE.FichierEditable(taille=taille))
        if verrouille:
            self.os.declarer(chemin, HE.FichierEditable(contenu=b"x",
                                                        verrouille=True))
        self.emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                               chemin.encode("utf-16-le") + b"\x00\x00")
        return self.appeler("loupe-01", {"rcx": HN.ADRESSE_CHEMIN})



def _appel_avec_pile5(emul, va, args, pile5):
    """Le miroir de Emulation.appeler avec le 5e argument msx64 posé
    APRÈS les canaris (ceux-ci couvrent [rsp+8, rsp+0x178] — le vrai
    slot [rsp+0x28] serait autrement écrasé)."""
    import struct as _st
    ucx = emul.uc
    for nom, val in HN.SENTINELLES_NV.items():
        ucx.reg_write(HN.REGS[nom], val)
    for nom, val in (args or {}).items():
        ucx.reg_write(HN.REGS[nom], val)
    ucx.reg_write(HN.REGS["rax"], 0)
    ucx.reg_write(HN.REGS["rsp"], HN.ENTREE_RSP)
    ucx.mem_write(HN.ENTREE_RSP + 8, HN.CANARI * 0x170)
    ucx.mem_write(HN.ENTREE_RSP, _st.pack("<Q", HN.RET_MAGIQUE))
    if pile5 is not None:
        ucx.mem_write(HN.ENTREE_RSP + 0x28, _st.pack("<Q", pile5))
    try:
        ucx.emu_start(va, HN.RET_MAGIQUE, count=200_000_000)
    except Exception:
        return {"rax": None, "crash": True}
    sortie = {k: ucx.reg_read(HN.REGS[k]) for k in HN.REGS}
    sortie["rax"] = HN.verdict_eax(sortie["rax"])
    sortie["crash"] = None
    return sortie

# ------------------------------------------------------------ les modèles

def modele_ligne(source: bytes, longueur: int, decalage: int) -> bytes:
    s = f"{decalage:08X}  "
    groupes = []
    for i in range(16):
        if i == 8:
            groupes.append(" ")     # l'espace médian DOUBLÉ (le contrat)
        groupes.append(f"{source[i]:02X}" if i < longueur else "  ")
        if i < 15:
            groupes.append(" ")
    s += "".join(groupes) + "  "
    miroir = "".join(
        chr(source[i]) if i < longueur and 0x20 <= source[i] <= 0x7E
        else ("." if i < longueur else " ") for i in range(16))
    return (s + miroir).encode("ascii") + b"\x00"


def stats(vals: list[int]) -> dict:
    v = sorted(vals)
    if not v:
        return {"min": None, "q1": None, "mediane": None, "q3": None,
                "max": None, "n": 0}

    def pct(p):
        return v[min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))]

    return {"min": v[0], "q1": pct(0.25), "mediane": pct(0.5),
            "q3": pct(0.75), "max": v[-1], "n": len(v)}


# --------------------------------------------- les suites K3 (le modèle)

TEM = "temoin-bras.bin"


def suite_a(a: CampA, contenu: bytes) -> tuple[bool, str]:
    """La suite K3 du camp A (2-4 vecteurs par bloc, le modèle Python).
    Retourne (tout_conforme, détail)."""
    try:
        # loupe-01 : l'ouverture saine (la session née entière)
        a.os.declarer(TEM, HE.FichierEditable(contenu=contenu))
        r = a.ouvrir(TEM, contenu=contenu)
        if r["rax"] != 0 or a.emul.u64(520) != len(contenu) \
                or a.emul.u64(552) != 384:
            return False, "loupe-01 saine"
        if a.emul.champ(568, 384) != contenu[:384]:
            return False, "loupe-01 tampon"
        # loupe-02 : la fenêtre médiane + le non-aligné
        r = a.appeler("loupe-02", {"rcx": 384})
        if r["rax"] != 0 or a.emul.u64(552) != 384 or \
                a.emul.champ(568, 384) != contenu[384:768]:
            return False, "loupe-02 dec=384"
        r = a.appeler("loupe-02", {"rcx": 8})
        if r["rax"] != -5:
            return False, "loupe-02 non-aligné"
        # loupe-05 : la gamme entière + le vide
        r = a.appeler("loupe-05", {"rcx": 0, "rdx": len(contenu),
                                   "r8": HN.ADRESSE_SORTIE32})
        if r["rax"] != 0 or bytes(a.emul.uc.mem_read(
                HN.ADRESSE_SORTIE32, 32)) != hashlib.sha256(contenu).digest():
            return False, "loupe-05 gamme"
        r = a.appeler("loupe-05", {"rcx": 0, "rdx": 0,
                                   "r8": HN.ADRESSE_SORTIE32})
        if r["rax"] != 0 or bytes(a.emul.uc.mem_read(
                HN.ADRESSE_SORTIE32, 32)) != hashlib.sha256(b"").digest():
            return False, "loupe-05 vide"
        # loupe-08 : la ligne MZ
        src = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
        a.emul.uc.mem_write(0x700500, src)
        r = a.appeler("loupe-08", {"rcx": 0x700500, "rdx": 16,
                                   "r8": 0x700540, "r9": 0})
        if r["rax"] != 0 or bytes(a.emul.uc.mem_read(0x700540, 77)) != \
                modele_ligne(src, 16, 0):
            return False, "loupe-08 MZ"
        # loupe-13 : l'école
        for fen, mot, dep, attendu in ((b"AAAAB", b"AAAA", 0, 0),
                                       (b"AAAAB", b"AAAB", 0, 1),
                                       (b"AAAAB", b"Z", 0, -1)):
            a.emul.uc.mem_write(0x700600, fen)
            a.emul.uc.mem_write(0x700A00, mot)
            r = a.appeler("loupe-13", {"rcx": 0x700600, "rdx": len(fen),
                                       "r8": 0x700A00, "r9": len(mot)},
                          pile5=dep)
            if r["rax"] != attendu:
                return False, f"loupe-13 école ({attendu})"
        # loupe-16 : la paire 4d/5a au curseur 0x22
        HN.fermer_session(a.emul)
        a.os.declarer(TEM, HE.FichierEditable(contenu=contenu))
        HN.emplacer_session(a.emul, a.os, TEM)
        a.emul.uc.mem_write(L.R_JOURNAL, b"\x00" * L.ZONE_JOURNAL)
        a.emul.ecrire_cadre(544, struct.pack("<Q", 0x22))
        for frappe in (0x34, 0x64, 0x35, 0x61):
            r = a.appeler("loupe-16", {"rcx": 0x770001, "rdx": 0x102,
                                       "r8": frappe, "r9": 0})
            if r["rax"] != 0:
                return False, f"loupe-16 frappe {frappe:#x}"
        if HE.lire_journal(a.emul) != [(0x22, 0x4d), (0x23, 0x5a)]:
            return False, "loupe-16 journal"
        return True, "suite A conforme"
    except Exception as exc:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        return False, f"crash ({type(exc).__name__})"


def suite_c(c: CampC, contenu: bytes) -> tuple[bool, str]:
    """La suite K3 du camp C — les MÊMES vecteurs, le MÊME modèle."""
    try:
        r = c.ouvrir(TEM, contenu=contenu)
        if r["rax"] != 0 or c.u64("taille") != len(contenu) \
                or c.u64("remplissage") != 384:
            return False, "loupe-01 saine"
        if c.octets(CADRE_C + OFF["tampon"], 384) != contenu[:384]:
            return False, "loupe-01 tampon"
        if c.octets(CADRE_C + OFF["sortie32"], 32) != \
                hashlib.sha256(contenu).digest():
            return False, "loupe-01 panneau (sha du fichier entier)"
        r = c.appeler("loupe02_lire", {"rcx": 384})
        if r["rax"] != 0 or c.u64("remplissage") != 384 or \
                c.octets(CADRE_C + OFF["tampon"], 384) != contenu[384:768]:
            return False, "loupe-02 dec=384"
        r = c.appeler("loupe02_lire", {"rcx": 8})
        if r["rax"] != -5:
            return False, "loupe-02 non-aligné"
        r = c.appeler("loupe05_sha256", {"rcx": 0, "rdx": len(contenu),
                                         "r8": CADRE_C + OFF["sortie32"]})
        if r["rax"] != 0 or c.octets(CADRE_C + OFF["sortie32"], 32) != \
                hashlib.sha256(contenu).digest():
            return False, "loupe-05 gamme"
        r = c.appeler("loupe05_sha256", {"rcx": 0, "rdx": 0,
                                         "r8": CADRE_C + OFF["sortie32"]})
        if r["rax"] != 0 or c.octets(CADRE_C + OFF["sortie32"], 32) != \
                hashlib.sha256(b"").digest():
            return False, "loupe-05 vide"
        src = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
        c.ecrire(ZONE_TAMPON_C, src)
        r = c.appeler("loupe08_ligne", {"rcx": ZONE_TAMPON_C, "rdx": 16,
                                        "r8": ZONE_TAMPON_C + 64, "r9": 0})
        if r["rax"] != 0 or c.octets(ZONE_TAMPON_C + 64, 77) != \
                modele_ligne(src, 16, 0):
            return False, "loupe-08 MZ"
        for fen, mot, dep, attendu in ((b"AAAAB", b"AAAA", 0, 0),
                                       (b"AAAAB", b"AAAB", 0, 1),
                                       (b"AAAAB", b"Z", 0, -1)):
            c.ecrire(ZONE_TAMPON_C + 0x200, fen)
            c.ecrire(ZONE_TAMPON_C + 0x500, mot)
            r = c.appeler("loupe13_recherche",
                          {"rcx": ZONE_TAMPON_C + 0x200, "rdx": len(fen),
                           "r8": ZONE_TAMPON_C + 0x500, "r9": len(mot)},
                          pile5=dep)
            if r["rax"] != attendu:
                return False, f"loupe-13 école ({attendu})"
        c2 = c
        c2.ecrire(CADRE_C + OFF["curseur"], struct.pack("<Q", 0x22))
        for frappe in (0x34, 0x64, 0x35, 0x61):
            r = c2.appeler("loupe16_saisie", {"rcx": frappe})
            if r["rax"] != 0:
                return False, f"loupe-16 frappe {frappe:#x}"
        if c2.journal() != [(0x22, 0x4d), (0x23, 0x5a)]:
            return False, "loupe-16 journal"
        return True, "suite C conforme"
    except Exception as exc:  # noqa: BLE001
        return False, f"crash ({type(exc).__name__})"


def compteurs_os_c(c: CampC) -> dict:
    return dict(c.os.compteurs)


def compteurs_os_a(a: CampA) -> dict:
    return dict(a.os.compteurs)


# ------------------------------------------------------------------- main

def main():
    print("=== LE BRAS DE RÉFÉRENCE COMPILATEUR — v0.14.0 (D193) ===")
    clang = subprocess.run(["which", "clang"], capture_output=True, text=True)
    ecart_clang = clang.returncode != 0
    print(f"[écart nommé] clang {'ABSENT' if ecart_clang else 'présent'} "
          "du laboratoire — gcc 14.2 tient la place")

    rng_vec = random.Random(GRAINE_VEC)
    contenu = bytes(rng_vec.randrange(256) for _ in range(1000))
    resultats = []

    cs_dis = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs_dis.detail = False

    for niveau in ("O2", "Os"):
        image, symboles, _ = compiler(niveau)
        manquants = [f for f in list(FONCTIONS_C.values()) + ["os",
                   "cadre_ptr"] if f not in symboles]
        assert not manquants, f"symboles manquants ({niveau}) : {manquants}"
        print(f"[camp C -{niveau}] image {len(image)} o")

        # ---- (0) l'auto-vérification du camp C : la suite AVANT tout -----
        c = CampC(image, symboles)
        ok0, det = suite_c(c, contenu)
        assert ok0, f"CA1 VIOLÉ — la référence -{niveau} est fautive : {det}"
        print(f"[CA1] la référence -{niveau} est saine (suite conforme)")

        # ---- (1) la passe de mesure aux vecteurs -------------------------
        a = CampA()
        ok_a0, det_a = suite_a(a, contenu)
        assert ok_a0, f"camp A fautif : {det_a}"
        ins_a = {b: [] for b in BLOCS}
        ins_c = {b: [] for b in BLOCS}
        divergences = []

        def note(bid, r_a, r_c, ok, nom):
            if ok:
                ins_a[bid].append(r_a["instructions"])
                ins_c[bid].append(r_c["instructions"])
            else:
                divergences.append(f"{bid}/{nom}")

        # les sessions des suites FERMÉES (les refus de loupe-01 exigent
        # une session close — P2 précède le fichier, sinon -5 partout)
        HN.fermer_session(a.emul)
        c.fermer()
        # loupe-01 : cinq vecteurs — LES REFUS D'ABORD (sans session :
        # P2 précède le fichier, une session ouverte rendrait -5 partout)
        ra = a.ouvrir("nulle-part.bin")
        rc = c.ouvrir("nulle-part.bin")
        note("loupe-01", ra, rc, ra["rax"] == rc["rax"] == -2, "absent")
        ra = a.ouvrir("ver.bin", contenu=b"x", verrouille=True)
        rc = c.ouvrir("ver.bin", contenu=b"x", verrouille=True)
        note("loupe-01", ra, rc, ra["rax"] == rc["rax"] == -7, "verrouillé")
        ra = a.ouvrir("geant.bin", taille=0x80000001)
        rc = c.ouvrir("geant.bin", taille=0x80000001)
        note("loupe-01", ra, rc, ra["rax"] == rc["rax"] == -3,
             "hors-périmètre")
        # la saine : LA SESSION NÉE ENTIÈRE (les deux camps sur LE MÊME
        # fichier, le même contenu)
        ra = a.ouvrir(TEM, contenu=contenu)
        rc = c.ouvrir(TEM, contenu=contenu)
        obs_ok = (ra["rax"] == rc["rax"] == 0
                  and a.emul.u64(520) == c.u64("taille") == len(contenu)
                  and a.emul.u64(552) == c.u64("remplissage") == 384
                  and a.emul.champ(568, 384)
                  == c.octets(CADRE_C + OFF["tampon"], 384)
                  == contenu[:384])
        note("loupe-01", ra, rc, obs_ok, "saine")
        ra = a.ouvrir(TEM)            # déjà ouverte (la saine l'a ouverte)
        rc = c.ouvrir(TEM)
        note("loupe-01", ra, rc, ra["rax"] == rc["rax"] == -5,
             "déjà-ouverte")

        # loupe-02 : les fenêtres + les rejets + le recouvrement
        for dec in (0, 384, 768, 624):
            ra = a.appeler("loupe-02", {"rcx": dec})
            rc = c.appeler("loupe02_lire", {"rcx": dec})
            n = min(384, 1000 - dec)
            ok = (ra["rax"] == rc["rax"] == 0
                  and a.emul.u64(552) == c.u64("remplissage") == n
                  and a.emul.champ(568, n)
                  == c.octets(CADRE_C + OFF["tampon"], n))
            note("loupe-02", ra, rc, ok, f"dec={dec}")
        for nom, dec in (("non-aligné", 8), ("hors-borne", 1000)):
            ra = a.appeler("loupe-02", {"rcx": dec})
            rc = c.appeler("loupe02_lire", {"rcx": dec})
            note("loupe-02", ra, rc, ra["rax"] == rc["rax"], nom)
        HN.fermer_session(a.emul)
        HN.emplacer_session(a.emul, a.os, TEM)
        a.emul.uc.mem_write(L.R_JOURNAL, b"\x00" * L.ZONE_JOURNAL)
        a.emul.uc.mem_write(L.R_JOURNAL, struct.pack("<Q", 16) + b"\xAA"
                            + b"\x00" * 7)
        a.emul.uc.mem_write(L.R_JOURNAL + 4096, struct.pack("<I", 1))
        ra = a.appeler("loupe-02", {"rcx": 0})
        c.ecrire(CADRE_C + OFF["journal"], struct.pack("<Q", 16) + b"\xAA"
                 + b"\x00" * 7)
        c.ecrire(CADRE_C + OFF["journal_n"], struct.pack("<I", 1))
        rc = c.appeler("loupe02_lire", {"rcx": 0})
        ok = (ra["rax"] == rc["rax"] == 0
              and a.emul.champ(568, 384)
              == c.octets(CADRE_C + OFF["tampon"], 384)
              and c.octets(CADRE_C + OFF["tampon"], 384)[16] == 0xAA)
        note("loupe-02", ra, rc, ok, "recouvrement")

        # loupe-05 : les gammes
        gammes = [(0, 0), (0, 1000)] + [
            (rng_vec.randrange(0, 900), rng_vec.randrange(1, 101))
            for _ in range(20)]
        for dec, lon in gammes:
            attendu = hashlib.sha256(contenu[dec:dec + lon]).digest()
            ra = a.appeler("loupe-05", {"rcx": dec, "rdx": lon,
                                        "r8": HN.ADRESSE_SORTIE32})
            rc = c.appeler("loupe05_sha256",
                           {"rcx": dec, "rdx": lon,
                            "r8": CADRE_C + OFF["sortie32"]})
            ok = (ra["rax"] == rc["rax"] == 0
                  and bytes(a.emul.uc.mem_read(HN.ADRESSE_SORTIE32, 32))
                  == c.octets(CADRE_C + OFF["sortie32"], 32) == attendu)
            note("loupe-05", ra, rc, ok, f"gamme {dec}+{lon}")

        # loupe-08 : les lignes
        srcs = [(b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff"
                 b"\x00\x00", 16, 0)]
        for _ in range(23):
            srcs.append((bytes(rng_vec.randrange(256) for _ in range(16)),
                         rng_vec.randrange(1, 17),
                         rng_vec.randrange(0, 1 << 20) * 16))
        for src, lon, dec in srcs:
            attendu = modele_ligne(src, lon, dec)
            a.emul.uc.mem_write(0x700500, src)
            ra = a.appeler("loupe-08", {"rcx": 0x700500, "rdx": lon,
                                        "r8": 0x700540, "r9": dec})
            c.ecrire(ZONE_TAMPON_C, src)
            rc = c.appeler("loupe08_ligne", {"rcx": ZONE_TAMPON_C,
                                            "rdx": lon,
                                            "r8": ZONE_TAMPON_C + 64,
                                            "r9": dec})
            ok = (ra["rax"] == rc["rax"] == 0
                  and bytes(a.emul.uc.mem_read(0x700540, 77))
                  == c.octets(ZONE_TAMPON_C + 64, 77) == attendu)
            note("loupe-08", ra, rc, ok, f"ligne dec={dec}")
        for lon in (0, 17):
            ra = a.appeler("loupe-08", {"rcx": 0x700500, "rdx": lon,
                                        "r8": 0x700540, "r9": 0})
            rc = c.appeler("loupe08_ligne", {"rcx": ZONE_TAMPON_C,
                                            "rdx": lon,
                                            "r8": ZONE_TAMPON_C + 64,
                                            "r9": 0})
            note("loupe-08", ra, rc, ra["rax"] == rc["rax"], f"rejet {lon}")

        # loupe-13 : les recherches
        cas = [(b"AAAAB", b"AAAA", 0, 0), (b"AAAAB", b"AAAB", 0, 1),
               (b"AAAAB", b"AAB", 2, 2), (b"AAAAB", b"Z", 0, -1)]
        for _ in range(24):
            fen = bytes(rng_vec.randrange(4) + 65
                        for _ in range(rng_vec.randrange(1, 400)))
            mot = bytes(rng_vec.randrange(4) + 65
                        for _ in range(rng_vec.randrange(1, 33)))
            dep = rng_vec.randrange(0, len(fen) + 1)
            pos = fen[dep:].find(mot)
            cas.append((fen, mot, dep, pos + dep if pos >= 0 else -1))
        for fen, mot, dep, attendu in cas:
            a.emul.uc.mem_write(0x700600, fen)
            a.emul.uc.mem_write(0x700A00, mot)
            ra = a.appeler("loupe-13", {"rcx": 0x700600, "rdx": len(fen),
                                        "r8": 0x700A00, "r9": len(mot)},
                           pile5=dep)
            c.ecrire(ZONE_TAMPON_C + 0x200, fen)
            c.ecrire(ZONE_TAMPON_C + 0x500, mot)
            rc = c.appeler("loupe13_recherche",
                           {"rcx": ZONE_TAMPON_C + 0x200, "rdx": len(fen),
                            "r8": ZONE_TAMPON_C + 0x500, "r9": len(mot)},
                           pile5=dep)
            note("loupe-13", ra, rc,
                 ra["rax"] == rc["rax"] == attendu, f"rech {len(fen)}")
        for nom, fen, mot, dep in (("motif-vide", b"AB", b"", 0),
                                   ("motif-33", b"A" * 40, b"A" * 33, 0),
                                   ("départ-hors", b"AB", b"A", 3)):
            a.emul.uc.mem_write(0x700600, fen)
            a.emul.uc.mem_write(0x700A00, mot)
            ra = a.appeler("loupe-13", {"rcx": 0x700600, "rdx": len(fen),
                                        "r8": 0x700A00, "r9": len(mot)},
                           pile5=dep)
            c.ecrire(ZONE_TAMPON_C + 0x200, fen)
            c.ecrire(ZONE_TAMPON_C + 0x500, mot)
            rc = c.appeler("loupe13_recherche",
                           {"rcx": ZONE_TAMPON_C + 0x200, "rdx": len(fen),
                            "r8": ZONE_TAMPON_C + 0x500, "r9": len(mot)},
                           pile5=dep)
            note("loupe-13", ra, rc, ra["rax"] == rc["rax"], nom)

        # loupe-16 : la saisie
        HN.fermer_session(a.emul)
        HN.emplacer_session(a.emul, a.os, TEM)
        a.emul.uc.mem_write(L.R_JOURNAL, b"\x00" * L.ZONE_JOURNAL)
        a.emul.ecrire_cadre(544, struct.pack("<Q", 0x22))
        # le camp C : SA session (c la garde) remise au curseur 0x22
        c.ecrire(CADRE_C + OFF["curseur"], struct.pack("<Q", 0x22))
        c.ecrire(CADRE_C + OFF["journal_n"], b"\x00" * 4)
        for frappe in (0x34, 0x64, 0x35, 0x61, 0x7A, 0x21, 0x30, 0x08,
                       0x41, 0x42):
            ra = a.appeler("loupe-16", {"rcx": 0x770001, "rdx": 0x102,
                                        "r8": frappe, "r9": 0})
            rc = c.appeler("loupe16_saisie", {"rcx": frappe})
            ok = (ra["rax"] == rc["rax"]
                  and HE.lire_journal(a.emul) == c.journal())
            note("loupe-16", ra, rc, ok, f"frappe {frappe:#x}")

        # ---- (2) la passe de MUTATION ------------------------------------
        print(f"[-{niveau}] la campagne de mutation (graine "
              f"{GRAINE_MUT}, 16/bloc)…")
        rng = random.Random(GRAINE_MUT)
        ref_a = CampA()
        octets_a, tailles_a = {}, {}
        for bid in BLOCS:
            taille = L.SLOTS_LOUPE[f"i1100{bid[-2:]}"][1]
            tailles_a[bid] = taille
            octets_a[bid] = bytes(ref_a.emul.uc.mem_read(VA_A[bid], taille))
        tailles_c = {bid: symboles[FONCTIONS_C[bid]][1] for bid in BLOCS}
        mut = {b: {"a_k3": 0, "a_dec": 0, "a_tot": 0, "c_k3": 0,
                   "c_os": 0, "c_tot": 0, "vivant_a": None, "vivant_c": None}
               for b in BLOCS}
        for bid in BLOCS:
            base_a = octets_a[bid]
            ins_list_a = list(cs_dis.disasm(base_a, VA_A[bid]))
            adr_c, t_c = symboles[FONCTIONS_C[bid]]
            base_c = image[adr_c - BASE_BRAS:adr_c - BASE_BRAS + t_c]
            ins_list_c = list(cs_dis.disasm(base_c, adr_c))
            # la référence des comptes OS du camp C (K2-adapté, UNE fois)
            ref_cpt = {bid: compteurs_os_c(CampC(image, symboles))
                       for bid in ("loupe-01", "loupe-02", "loupe-05")}
            for _ in range(16):
                ia = rng.randrange(len(ins_list_a))
                pos_a = (ins_list_a[ia].address - VA_A[bid]
                         + rng.randrange(ins_list_a[ia].size))
                val = base_a[pos_a]
                nouvelle = rng.choice([x for x in range(256) if x != val])
                ic = rng.randrange(len(ins_list_c))
                pos_c = (ins_list_c[ic].address - adr_c
                         + rng.randrange(ins_list_c[ic].size))
                val_c = base_c[pos_c]
                nouvelle_c = rng.choice([x for x in range(256)
                                         if x != val_c])
                # — camp A
                mut[bid]["a_tot"] += 1
                m = bytearray(base_a)
                m[pos_a] = nouvelle
                m = bytes(m)
                if list(cs_dis.disasm(m, VA_A[bid])) is None or \
                        not all(i.mnemonic for i in
                                cs_dis.disasm(m, VA_A[bid])):
                    mut[bid]["a_dec"] += 1        # K2-décodage
                    continue
                try:
                    aa = CampA()
                    aa.emul.uc.mem_write(VA_A[bid], m)
                    aa.emul.uc.ctl_remove_cache(
                        VA_A[bid] & ~0xFFF,
                        (VA_A[bid] + len(m) + 0xFFF) & ~0xFFF)
                    ok, _ = suite_a(aa, contenu)
                except Exception:  # noqa: BLE001
                    ok = False
                if not ok:
                    mut[bid]["a_k3"] += 1
                elif mut[bid]["vivant_a"] is None:
                    mut[bid]["vivant_a"] = f"{pos_a:#x}: {val:#04x}" \
                                           f"→{nouvelle:#04x}"
                # — camp C
                mut[bid]["c_tot"] += 1
                img_m = bytearray(image)
                img_m[adr_c - BASE_BRAS + pos_c] = nouvelle_c
                tue_os = False
                try:
                    cc = CampC(bytes(img_m), symboles)
                    ok, _ = suite_c(cc, contenu)
                    # K2-adapté : les comptes OS contre la référence (les
                    # blocs OS seuls — exclusif de K3 : le mutant qui rate
                    # la suite est déjà K3-mort)
                    if ok and bid in ("loupe-01", "loupe-02", "loupe-05"):
                        tue_os = compteurs_os_c(cc) != ref_cpt[bid]
                except Exception:  # noqa: BLE001
                    ok = False
                if not ok:
                    mut[bid]["c_k3"] += 1
                elif tue_os:
                    mut[bid]["c_os"] += 1
                elif mut[bid]["vivant_c"] is None:
                    mut[bid]["vivant_c"] = f"{pos_c:#x}: {val_c:#04x}" \
                                           f"→{nouvelle_c:#04x}"
            tues_a = mut[bid]["a_k3"] + mut[bid]["a_dec"]
            tues_c = mut[bid]["c_k3"] + mut[bid]["c_os"]
            print(f"   {bid} : A {tues_a}/{mut[bid]['a_tot']} "
                  f"(K3 {mut[bid]['a_k3']}, déc {mut[bid]['a_dec']}) / "
                  f"C {tues_c}/{mut[bid]['c_tot']} "
                  f"(K3 {mut[bid]['c_k3']}, OS {mut[bid]['c_os']})")

        for bid in BLOCS:
            resultats.append({
                "niveau": f"-{niveau}", "bloc": bid,
                "ins_A": stats(ins_a[bid]), "ins_C": stats(ins_c[bid]),
                "taille_A": tailles_a[bid], "taille_C": tailles_c[bid],
                "mut": dict(mut[bid]),
                "n_divergences": len(divergences)})
        if divergences:
            print(f"[-{niveau}] DIVERGENCES : {divergences[:8]}")

    # ---- l'écriture -------------------------------------------------------
    with open(PREUVES / "bras_c.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["niveau", "bloc", "ins_A_min", "ins_A_med", "ins_A_q1",
                    "ins_A_q3", "ins_A_max", "ins_C_min", "ins_C_med",
                    "ins_C_q1", "ins_C_q3", "ins_C_max", "taille_A",
                    "taille_C", "rapport_taille", "mut_A_K3",
                    "mut_A_dec", "mut_A_tot", "mut_C_K3", "mut_C_os",
                    "mut_C_tot"])
        for r in resultats:
            ia, ic, m = r["ins_A"], r["ins_C"], r["mut"]
            w.writerow([r["niveau"], r["bloc"], ia["min"], ia["mediane"],
                        ia["q1"], ia["q3"], ia["max"], ic["min"],
                        ic["mediane"], ic["q1"], ic["q3"], ic["max"],
                        r["taille_A"], r["taille_C"],
                        round(r["taille_A"] / r["taille_C"], 2),
                        m["a_k3"], m["a_dec"], m["a_tot"],
                        m["c_k3"], m["c_os"], m["c_tot"]])
    rapport = [
        "LE BRAS DE RÉFÉRENCE COMPILATEUR — v0.14.0 (le plan pré-enregistré "
        "D193 ; les critères CA1-CA5)",
        "",
        "NOTE D'INTERPRÉTATION : loupe-01 « saine » est la session née "
        "entière — la cascade complète (fenêtre + panneau d'empreintes) ; "
        "sa médiane élevée cache la queue légère des refus, le CSV porte "
        "min/max. ADAPTATION DU PANNEAU : le camp C calcule la moitié "
        "sha256 du panneau (le md5 C du banc v0.11.0 fut écarté comme "
        "fautif — aucun md5 C audité n'existe au labo) : les comptes de "
        "loupe-01 saine ne sont PAS à travail égal, l'écart est nommé. "
        "La taille de loupe-05 A (384 o) EXCLUT les blocs sha hérités "
        "(tls13-01..04, ~765 o au scellé) que le camp C embarque "
        "(1707 o) — l'héritage PAR LA CARTE est un partage, pas une "
        "copie : la comparaison honnête est 384+765 contre 1707.",
        f"écart nommé : clang {'ABSENT' if ecart_clang else 'présent'} du "
        "laboratoire — gcc 14.2 -O2/-Os tient la place (le précédent v0.11.0)",
        "adaptations nommées (CA4) : le round-trip EXCLU du camp C (la "
        "commande) ; K2 camp A = le DÉCODAGE capstone (le round-trip "
        "keystone de v0.11.0 non rejoué, l'écart nommé) ; K2 camp C = les "
        "comptes d'appels OS contre la référence (les blocs OS seuls) ; la "
        "comparaison de loupe-13 par memcmp du C (l'équivalent compilé du "
        "libc-02 hérité).",
        "",
        "LES INSTRUCTIONS PAR OPÉRATION COMPLÈTE (le même crochet, la "
        "convention D191) — médiane [q1..q3] :",
    ]
    for r in resultats:
        ia, ic, m = r["ins_A"], r["ins_C"], r["mut"]
        rapport.append(
            f"{r['niveau']} {r['bloc']} : A {ia['mediane']} "
            f"[{ia['q1']}..{ia['q3']}] / C {ic['mediane']} "
            f"[{ic['q1']}..{ic['q3']}] (n={ia['n']}/{ic['n']}) — "
            f"tailles A {r['taille_A']} o / C {r['taille_C']} o "
            f"({r['taille_A'] / r['taille_C']:.2f}×) — mutation A "
            f"{m['a_k3'] + m['a_dec']}/{m['a_tot']} [K3 {m['a_k3']}, "
            f"déc {m['a_dec']}] / C {m['c_k3'] + m['c_os']}/{m['c_tot']} "
            f"[K3 {m['c_k3']}, OS {m['c_os']}]"
            + (f" — vivant A : {m['vivant_a']}" if m["vivant_a"] else "")
            + (f" — vivant C : {m['vivant_c']}" if m["vivant_c"] else ""))
    par_niveau = {}
    for r in resultats:
        par_niveau[r["niveau"]] = max(par_niveau.get(r["niveau"], 0),
                                      r["n_divergences"])
    rapport += ["", "divergences des vecteurs (A ≠ C ou ≠ modèle) : "
                + (", ".join(f"{k} : {v}" for k, v in par_niveau.items())
                   if any(par_niveau.values()) else "AUCUNE — les camps "
                   "s'accordent sur tous les vecteurs")]
    (PREUVES / "bras_c_rapport.txt").write_text("\n".join(rapport) + "\n",
                                                encoding="utf-8")
    print("\n".join(rapport))
    print("\n[bras_c] écrit : preuves_v140/bras_c.csv + rapport")


if __name__ == "__main__":
    main()
