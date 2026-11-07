#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""loupe/harnais_noyau.py — LE HARNAIS DU NOYAU du domaine loupe.

Chantier M10-(b) : les blocs loupe-01..07 (le noyau fichier + empreintes du
TGN « Loupe ») NOTÉS-MESURÉS-PROUVÉS. Le modèle est le harnais sha du
domaine tls13 (M9-(b)) : l'émulation nue aux RVA du plan (mécanisme D79),
l'appelant factice pose les sentinelles non volatiles et les canaris, le
verdict est TRANCHÉ par le code — jamais cru.

LA PIÈCE NEUVE DU GESTE : LE MINI-OS VIRTUEL. Le noyau touche le monde
(CreateFileW, GetFileSizeEx, SetFilePointerEx, ReadFile, CloseHandle,
GetLastError — les SIX feuilles kernel32 du noyau, la liste fermée de
l'IAT) : le harnais dote l'émulation de SHIMS à l'ABI msx64 — un système
de fichiers virtuel aux témoins réels (proxy.exe scellé INCLUS : la
pièce de l'ère jugée par sa propre application), les échecs
PARAMÉTRABLES (le Nième ReadFile en échec : E4 de loupe-02/05/06), le
journal des gle (I4 : le code consigné, jamais un code brut à la barre).

LE CAHIER (le miroir M9-(b), la charte § 3 : les vecteurs officiels AVANT
usage, la falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé 1.0.0 relu (65 024 o, sha256
       446279f3… — L'ERRATUM loupe-01 r2 CONSTATÉ : la taille 44 544
       était celle du scellé 0.9.0 de l'ère close), le scellé M1 relu
       (selftest.exe, la minilibc), les notations m1/tls13 intacts, les
       SEPT specs relues (les têtes + la révision 2 de loupe-01), le
       plan d'adressage (les slots du noyau ARRÊTÉS sur les mesures, les
       zones, l'IAT 34 feuilles recomptée) ;
  V1 — LE ROUND-TRIP + LA STRUCTURE : chaque notation ré-assemblée en
       ses octets (keystone == capstone, R5), les longueurs == les
       mesures de l'arrêt (D161), les déplacements RIP cibles == les
       symboles du plan (CADRE, CUMUL, MD5_S, les feuilles IAT), les
       appels directs == la liste fermée des blocs (LOUPE02/03/04/07,
       TLS01/03/04, LIBC01/07 — le réseau des specs), les feuilles IAT
       par bloc == la liste fermée de chaque spec (I5), LES CONSTANTES
       MD5 RE-DÉRIVÉES PAR ARITHMÉTIQUE (les 64 T par sinus, les S, les
       abscisses), L'HÉRITAGE PAR LA CARTE CONSTATÉ BYTE-IDENTIQUE (R7 :
       les octets émulés de tls13-01..04 et libc-01/07 == les octets
       EXTRAITS DES SCELLÉS, et les notations d'origine ré-assemblées ==
       les extraits — la double preuve), AUCUN syscall, LA BORNE 2 Gio
       dans les octets (le bord exact accepté, le refus strictement
       au-delà) ;
  V2 — LES SEPT VECTEURS OFFICIELS RFC 1321 (le doré) : le témoin virtuel
       porte les sept messages, loupe-06 AU FICHIER (les gammes) rend
       les condensés OCTET POUR OCTET — chaque attendu RECROISÉ à
       hashlib.md5 (l'instrument se contrôle avant de juger) ; le
       différentiel 1 000 gammes aléatoires ; le témoin 3×64 Kio + 1
       entier par fenêtres glissantes ;
  V3 — LE DIFFÉRENTIEL SHA (l'héritage au travail) : loupe-05 sur
       proxy.exe SCELLÉ (le fichier virtuel alimenté par les octets
       RÉELS de la pièce) : la gamme entière == hashlib.sha256 == le
       témoin absolu 446279f3… — l'application rend l'empreinte DE SA
       PROPRE PIÈCE ; les vecteurs FIPS au fichier ; les gammes
       aléatoires (la graine) des témoins ;
  V4 — LE NOYAU FICHIER : loupe-04 le cadre vierge (960 o : zéros
       partout sauf la poignée INVALIDE), loupe-01 la session née
       ENTIÈRE (le cadre champ à champ, le panneau né == hashlib),
       loupe-02 la fenêtre bornée (1 000 décalages aléatoires valides +
       LE RECOUVREMENT du journal), loupe-03 la fermeture (le cadre
       re-vierge, l'hygiène, l'idempotence comptée), loupe-07 le panneau
       48 o == (md5, sha256) hashlib ; les zones des chantiers suivants
       INTACTES ;
  V5 — LES REJETS NOMMÉS : absent -2 / verrouillé -7 / accès -6 / la
       borne 2 Gio + 1 → -3 LA POIGNÉE REFERMÉE (comptée) / la session
       double -5 L'ANCIEN INTACT / sans session -4 / non aligné -5 /
       hors bornes -3 / la sortie nulle -5 / le shim ReadFile en échec →
       -6 partout (la sortie INTACTE, le remplissage 0, le code AU
       JOURNAL du harnais, le refus propagé par loupe-01 LA SESSION
       CLOSE) ;
  V6 — LA FALSIFICATION (zéro silence) : une constante MD5_T mutée d'un
       ulp à la table .rdata → les sept vecteurs dorés échouent, chaque
       octet du condensé attendu muté → l'égalité échoue (la comparaison
       n'est pas muette), le tampon de vue INTACT pendant le calcul
       (I3 : l'exclusion de famille), le journal INTACT pendant loupe-07
       (I4), le panneau TOUJOURS celui du disque.

Usage : python3 harnais_noyau.py            # le cahier complet
        python3 harnais_noyau.py --graine N # la graine du générateur (défaut 20261108)
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)
M4_DIR = os.path.join(TRIADE, "m4")
sys.path.insert(0, ICI)
sys.path.insert(0, M4_DIR)
sys.path.insert(0, os.path.join(M4_DIR, "outils"))

# Le plan loupe chargé par CHEMIN NOMINATIF (leçon D158 : le nom « layout »
# est disputé par la chaîne build_m3/build_m4 — jamais d'import anonyme ici).
if "layout_loupe" in sys.modules:
    L = sys.modules["layout_loupe"]
else:
    _spec_l = importlib.util.spec_from_file_location(
        "layout_loupe", os.path.join(ICI, "layout.py"))
    L = importlib.util.module_from_spec(_spec_l)
    sys.modules["layout_loupe"] = L
    _spec_l.loader.exec_module(L)

# Le plan tls13 (les SLOTS_TLS13 du scellé 1.0.0 — l'extraction des octets
# hérités), par chemin nominatif.
if "layout_tls13" in sys.modules:
    LT = sys.modules["layout_tls13"]
else:
    _spec_t = importlib.util.spec_from_file_location(
        "layout_tls13", os.path.join(TRIADE, "tls13", "layout.py"))
    LT = importlib.util.module_from_spec(_spec_t)
    sys.modules["layout_tls13"] = LT
    _spec_t.loader.exec_module(LT)

# La machinerie de notation de la lignée (assembler_bloc/round_trip — le
# lecteur canonique des notations, le même outil qui scella M4..M9).
if "build_m4" in sys.modules:
    B4 = sys.modules["build_m4"]
else:
    _spec_b4 = importlib.util.spec_from_file_location(
        "build_m4", os.path.join(M4_DIR, "build_m4.py"))
    B4 = importlib.util.module_from_spec(_spec_b4)
    sys.modules["build_m4"] = B4
    _spec_b4.loader.exec_module(B4)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
import capstone  # noqa: E402
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                               UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                               UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                               UC_X86_REG_R15, UC_X86_REG_RIP)

REGS = {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
        "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
        "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
        "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
        "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
        "r15": UC_X86_REG_R15}

# --- La mémoire du harnais (l'image loupe aux RVA du plan, mécanisme D79) --------

ZONE_LIBC = (0x1000, 0x1000)    # .text 0x1000-0x1FFF : la minilibc aux adresses scellées M1
ZONE_RDATA = (0x2000, 0x1000)    # .rdata : MD5_S/T + l'IAT + K[64] @0x2F00 (la table du scellé)
ZONE_IMAGE = (0x4000, 0x9000)    # .text2 0x4000-0xBFFF (le domaine) + les sha héritées 0xC000-0xC3C0
ZONE_DATA = (0xE000, 0x12000)    # .data : les zones du domaine (CUMUL finit 0x20000)
ZONE_SHIMS = (0x900000, 0x2000)  # les adresses shims (0x900000+) + le mort (0x901000)
ZONE_TESTS = (0x700000, 0x1000)  # les sorties de test + le chemin d'appel
SHIM_MORT = 0x901000             # les 28 feuilles hors noyau : l'appel y est DÉNONCÉ
RET_MAGIQUE = 0xDE00             # dans la réserve .text — jamais exécuté
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
ENTREE_RSP = RSP0 - 0x108        # ≡ 8 (mod 16) — le point de vue de l'APPELÉ

ADRESSE_SORTIE16 = 0x700100      # les condensés md5 (16 o)
ADRESSE_SORTIE32 = 0x700200      # les condensés sha256 (32 o)
ADRESSE_SORTIE48 = 0x700300      # le panneau (48 o)
ADRESSE_CHEMIN = 0x700400        # le chemin d'appel (jusqu'à 522 o)

CANARI = b"\xA5"

SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}

# --- Les scellés (les pièces V0 — les ancres R7 des octets hérités) --------------

SCELLE_M9 = "tls13/proxy.exe"    # la pièce de l'ère 1.0.0 (le septième run l'a courue)
SCELLE_M9_TAILLE = 65024
SCELLE_M9_SHA256 = ("446279f3ab356900870cc3b3e1700654"
                    "a4216ec0b264172340e453db3b00d93d")
SCELLE_M1 = "m1/selftest.exe"    # la pièce de la minilibc (l'ère M1)
SCELLE_M1_TAILLE = 9216
SCELLE_M1_SHA256 = ("8038585b7af83c9fe5e6fdccd197e678"
                    "88b9e5fb09d8d6c84cb998c684bff3c0")

# Les emplacements ORIGINAUX des blocs hérités dans leurs scellés (les plans
# d'origine — la carte du projet, jamais une adresse devinée) :
#   M1  : libc-01 memcpy @RVA 0x1100 (slot 0x80), libc-07 memset @0x13C0 (0x80)
#   M9  : tls13-01..04 aux SLOTS_TLS13 du plan tls13 (0xC000/0xC080/0xC240/
#         0xC300 — slots 0x80/0x1C0/0xC0/0xC0)
EMPLACEMENTS_M1 = {
    "libc-01": (0x1100, 0x80, os.path.join(TRIADE, "m1", "notation"),
                "libc-01-memcpy"),
    "libc-07": (0x13C0, 0x80, os.path.join(TRIADE, "m1", "notation"),
                "libc-07-memset"),
}
EMPLACEMENTS_M9 = {
    "tls13-01": (LT.TLS01_VA, 0x80, os.path.join(TRIADE, "tls13", "notation"),
                 "tls13-01-sha256-init"),
    "tls13-02": (LT.TLS02_VA, 0x1C0, os.path.join(TRIADE, "tls13", "notation"),
                 "tls13-02-sha256-comprimer"),
    "tls13-03": (LT.TLS03_VA, 0xC0, os.path.join(TRIADE, "tls13", "notation"),
                 "tls13-03-sha256-absorber"),
    "tls13-04": (LT.TLS04_VA, 0xC0, os.path.join(TRIADE, "tls13", "notation"),
                 "tls13-04-sha256-finaliser"),
}
DESTINATIONS = {          # les slots loupe (le plan, source unique) :
    "libc-01": L.R_LIBC01, "libc-07": L.R_LIBC07,
    "tls13-01": L.R_TLS01, "tls13-02": L.R_TLS02,
    "tls13-03": L.R_TLS03, "tls13-04": L.R_TLS04,
}

# --- Les six feuilles kernel32 du noyau (la liste fermée, charte § 9) -------------

FEUILLES_NOYAU = ("CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                  "ReadFile", "CloseHandle", "GetLastError")

# --- Les vecteurs officiels RFC 1321 § A.5 (le doré — chaque attendu RECROISÉ
# --- à hashlib.md5 par le harnais même : le juge est le code, la constante
# --- n'est jamais crue sur parole)

VECTEURS_RFC1321 = [
    ("le vide (la gamme nulle)", b"",
     "d41d8cd98f00b204e9800998ecf8427e"),
    ("« a »", b"a",
     "0cc175b9c0f1b6a831c399e269772661"),
    ("« abc »", b"abc",
     "900150983cd24fb0d6963f7d28e17f72"),
    ("« message digest »", b"message digest",
     "f96b697d7cb7938d525a2f31aaf161d0"),
    ("l'alphabet minuscule", b"abcdefghijklmnopqrstuvwxyz",
     "c3fcd3d76192e4007dfb496cca67e13b"),
    ("l'alphabet mixte",
     b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
     "d174ab98d277d9f5a5611c2c9f419d9f"),
    ("« 1234567890 » ×8", b"1234567890" * 8,
     "57edf4a22be3c955ac49da2e2107b67a"),
]

# Les vecteurs FIPS 180-4 au fichier (loupe-05 V2 — l'héritage les porte)
VECTEURS_FIPS = [
    ("le vide", b"",
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("« abc »", b"abc",
     "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
]

# Les noms machine des blocs du noyau (la table i11xxxx du README)
NOMS_NOYAU = {
    "i110001": "loupe-01-ouvrir", "i110002": "loupe-02-lire",
    "i110003": "loupe-03-fermer", "i110004": "loupe-04-cadre",
    "i110005": "loupe-05-sha256", "i110006": "loupe-06-md5",
    "i110007": "loupe-07-cumul",
}

REUSSITES, ECHECS = [], []


class ErreurHarnais(Exception):
    """Tout écart du harnais (mode build : lève, jamais un verdict muet)."""


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append((nom, detail))
        print(f"  [ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))


def section(titre: str) -> None:
    print(f"\n--- {titre} ---")


def s64(v: int) -> int:
    return v - (1 << 64) if v >= (1 << 63) else v


def verdict_eax(rax64: int) -> int:
    """LE VERDICT VIT DANS EAX — la table des SEPT verdicts (charte § 9) : les
    blocs rendent leurs refus par « mov eax, -N » (l'opération 32 bits
    zéro-étend rax) ; le harnais lit le verdict 32 bits SIGNÉ. Les poignées
    64 bits ne transitent JAMAIS par rax ici — le cadre les porte."""
    eax = rax64 & 0xFFFFFFFF
    return eax - (1 << 32) if eax >= (1 << 31) else eax


# --- La re-dérivation par arithmétique (le juge est le code) ----------------------

def deriv_MD5_T() -> list[int]:
    """RFC 1321 § 3.4 : T[i] = floor(2^32 · |sin(i+1)|) — les 64 constantes."""
    return [int((1 << 32) * abs(math.sin(i + 1))) & 0xFFFFFFFF
            for i in range(64)]


def deriv_MD5_S() -> list[int]:
    """RFC 1321 § 3.1 : les décalages des quatre rounds."""
    return [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 \
        + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4


# --- Le mini-OS virtuel (les shims kernel32 du noyau — la pièce neuve) ------------

class FichierVirtuel:
    def __init__(self, contenu: bytes | None = None, taille: int | None = None,
                 verrouille: bool = False, refus_acces: bool = False):
        self.contenu = contenu
        self.taille = len(contenu) if taille is None else taille
        self.verrouille = verrouille
        self.refus_acces = refus_acces

    def lire(self, pos: int, n: int) -> bytes:
        if self.contenu is None or pos >= self.taille:
            return b"\x00" * n       # la taille déclarée sans contenu : des zéros
        fin = min(pos + n, self.taille)
        return self.contenu[pos:fin]


class OSVirtuel:
    """Le noyau vu par les shims : les fichiers virtuels (les témoins RÉELS
    du dépôt inclus), les poignées, le dernier gle, les échecs paramétrables
    et les compteurs — tout ce que le harnais constate sur pièces."""

    def __init__(self):
        self.fichiers: dict[str, FichierVirtuel] = {}
        self.poignees: dict[int, tuple[str, int]] = {}   # handle → (chemin, pos)
        self.prochaine = 0x1000
        self.gle = 0
        self.journal_gle: list[tuple[str, int]] = []     # le journal du harnais
        self._echec_armedans: int | None = None          # le Nième après armement
        self._echec_compteur = 0
        self.echec_close = False
        self.compteurs = {"CreateFileW": 0, "GetFileSizeEx": 0,
                          "SetFilePointerEx": 0, "ReadFile": 0,
                          "CloseHandle": 0, "GetLastError": 0}
        self.appels_interdits = 0                        # les feuilles hors noyau

    def declarer(self, chemin: str, fv: FichierVirtuel) -> None:
        self.fichiers[chemin] = fv

    def armer_echec_read(self, dans: int | None) -> None:
        """Arme l'échec du Nième ReadFile À VENIR (None désarme) — E4 des
        blocs : le refus système au moment choisi par le harnais."""
        self._echec_armedans = dans
        self._echec_compteur = 0

    def _erreur(self, code: int) -> None:
        self.gle = code

    def create_file_w(self, chemin: str) -> int:
        self.compteurs["CreateFileW"] += 1
        fv = self.fichiers.get(chemin)
        if fv is None:
            self._erreur(2)          # ERROR_FILE_NOT_FOUND
            return 0xFFFFFFFFFFFFFFFF
        if fv.verrouille:
            self._erreur(32)         # ERROR_SHARING_VIOLATION
            return 0xFFFFFFFFFFFFFFFF
        if fv.refus_acces:
            self._erreur(5)          # ERROR_ACCESS_DENIED
            return 0xFFFFFFFFFFFFFFFF
        h = self.prochaine
        self.prochaine += 8
        self.poignees[h] = (chemin, 0)
        self.gle = 0
        return h

    def taille_de(self, h: int) -> int | None:
        ent = self.poignees.get(h)
        return self.fichiers[ent[0]].taille if ent else None

    def read_file(self, h: int, pos: int, n: int) -> tuple[bytes, bool]:
        """Retourne (données, succès) ; l'échec posé au journal par gle."""
        self.compteurs["ReadFile"] += 1
        if self._echec_armedans is not None:
            self._echec_compteur += 1
            if self._echec_compteur == self._echec_armedans:
                self._erreur(1117)   # ERROR_IO_DEVICE — le refus nommé du labo
                return b"", False
        ent = self.poignees.get(h)
        if ent is None:
            self._erreur(6)          # ERROR_INVALID_HANDLE
            return b"", False
        donnees = self.fichiers[ent[0]].lire(pos, n)
        self.poignees[h] = (ent[0], pos + n)
        self.gle = 0
        return donnees, True

    def close_handle(self, h: int) -> bool:
        self.compteurs["CloseHandle"] += 1
        if self.echec_close:
            self._erreur(6)
            return False
        self.poignees.pop(h, None)
        self.gle = 0
        return True


# --- L'émulation (le modèle harnais_sha : l'appelant factice msx64) ---------------

class Emulation:
    """L'image loupe posée aux RVA du plan : les SEPT notations du noyau,
    les SIX héritages EXTRAITS DES SCELLÉS (R7), les tables MD5, l'IAT aux
    shims — appelée comme des fonctions msx64 ordinaires."""

    def __init__(self, os_virtuel: OSVirtuel):
        self.os = os_virtuel
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cs.detail = False
        self.uc.mem_map(*ZONE_LIBC)
        self.uc.mem_map(*ZONE_RDATA)
        self.uc.mem_map(*ZONE_IMAGE)
        self.uc.mem_map(*ZONE_DATA)
        self.uc.mem_map(*ZONE_SHIMS)
        self.uc.mem_map(*ZONE_TESTS)
        self.uc.mem_map(ZONE_PILE, TAILLE_PILE)

        # LA TABLE DU SCELLÉ — K[64] @0x2F00 : le déplacement RIP de tls13-02
        # hérité la vise TELLE QUELLE (les 64 constantes FIPS 180-4 § 4.2.2
        # vivent à tls13/layout.py, la source unique — jamais re-déclarées)
        self.uc.mem_write(L.R_K, struct.pack("<64I", *LT.K))

        # l'IAT : les 34 feuilles aux slots du plan — les SIX du noyau vers
        # leurs shims, les 28 autres vers LE MORT (l'appel y est DÉNONCÉ)
        self.adr_shims: dict[int, str] = {}
        base = ZONE_SHIMS[0]
        for i, feuille in enumerate(FEUILLES_NOYAU):
            adr = base + 8 * i
            self.adr_shims[adr] = feuille
            self.uc.mem_write(L.IAT_SLOTS[feuille], struct.pack("<Q", adr))
        for feuille, slot in L.IAT_SLOTS.items():
            if feuille not in FEUILLES_NOYAU:
                self.uc.mem_write(slot, struct.pack("<Q", SHIM_MORT))

        # les tables MD5 publiques .rdata (le plan, source unique)
        self.uc.mem_write(L.R_MD5_S, struct.pack("<64I", *L.MD5_S))
        self.uc.mem_write(L.R_MD5_T, struct.pack("<64I", *L.MD5_T))

        # LE CADRE À L'IMAGE naît poignée INVALIDE (l'initialiseur .data du
        # futur build — le zéro de la mémoire vierge serait une session
        # fantôme : loupe-02 y croirait ; miroir du commentaire du plan)
        self.uc.mem_write(L.R_CADRE + 528, b"\xFF" * 8)

        # les notations du noyau (le lecteur canonique — keystone, rien d'autre)
        self.blobs: dict[str, tuple[bytes, list[dict]]] = {}
        for bid, nom in NOMS_NOYAU.items():
            rva, slot = L.SLOTS_LOUPE[bid]
            chemin = os.path.join(ICI, "notation", nom + ".asm")
            octets, metas = B4.assembler_bloc(self.ks, chemin, rva, slot)
            self.uc.mem_write(rva, octets)
            self.blobs[bid] = (octets, metas)

        # L'INSTRUMENT PERMANENT (la leçon du premier passage V4/V6 : unicorn
        # attache les hooks à la TRADUCTION des blocs — posé AVANT tout)
        self.uc.hook_add(UC_HOOK_CODE, self._instrument)
        self.heritages: dict[str, bytes] = {}
        self.extraits: dict[str, bytes] = {}

    # -- la pose des héritages (V0 relit les pièces, V1 les recroupe) ------------

    def poser_heritages(self, donnees_m9: bytes, donnees_m1: bytes) -> None:
        """Les octets des SCELLÉS posés aux slots loupe — R7 PAR CONSTRUCTION,
        le constat se fait en relisant les deux sources (jamais cru)."""
        def extraire(donnees: bytes, rva_orig: int, slot: int) -> bytes:
            # le parse minimal des sections PE (RVA -> raw) :
            e = struct.unpack_from("<I", donnees, 0x3C)[0]
            n = struct.unpack_from("<H", donnees, e + 6)[0]
            opt = struct.unpack_from("<H", donnees, e + 20)[0]
            for i in range(n):
                o = e + 24 + opt + i * 40
                va, = struct.unpack_from("<I", donnees, o + 12)
                ra, = struct.unpack_from("<I", donnees, o + 20)
                vs, = struct.unpack_from("<I", donnees, o + 8)
                if va <= rva_orig < va + vs:
                    raw = ra + (rva_orig - va)
                    return donnees[raw:raw + slot]
            raise ErreurHarnais(f"RVA {rva_orig:#x} introuvable dans le scellé")
        for nom, (rva_orig, slot, _, _) in \
                {**EMPLACEMENTS_M1, **EMPLACEMENTS_M9}.items():
            source = donnees_m1 if nom in EMPLACEMENTS_M1 else donnees_m9
            extraits = extraire(source, rva_orig, slot)
            self.extraits[nom] = extraits
            self.uc.mem_write(DESTINATIONS[nom], extraits)
            self.heritages[nom] = bytes(self.uc.mem_read(DESTINATIONS[nom], slot))

    # -- le hook des shims -------------------------------------------------------

    def _retour(self, uc, rax: int) -> None:
        """Le retour msx64 du shim : rax posé, rip = l'adresse de retour
        lue à [rsp] (le call a poussé le retour), rsp += 8."""
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RAX, rax & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RIP, ret)

    def _lire_utf16(self, adr: int, cap: int = 260) -> str:
        try:
            brut = bytes(self.uc.mem_read(adr, cap * 2))
        except UcError as err:
            raise ErreurHarnais(
                f"le chemin reçu à {adr:#x} est illisible ({err}) — le "
                "bloc appelant a-t-il préservé rcx jusqu'à l'appel ?") from err
        fin = brut.find(b"\x00\x00")
        if fin > 0:
            brut = brut[:fin + 1]
        return brut.decode("utf-16-le", errors="replace").rstrip("\x00")

    def _shim(self, uc, feuille: str) -> None:
        os_v = self.os
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        r9 = uc.reg_read(UC_X86_REG_R9)
        if feuille == "CreateFileW":
            chemin = self._lire_utf16(rcx)
            self._retour(uc, os_v.create_file_w(chemin))
        elif feuille == "GetFileSizeEx":
            os_v.compteurs["GetFileSizeEx"] += 1
            taille = os_v.taille_de(rcx)
            if taille is None:
                os_v._erreur(6)
                self._retour(uc, 0)
            else:
                uc.mem_write(rdx, struct.pack("<Q", taille))
                self._retour(uc, 1)
        elif feuille == "SetFilePointerEx":
            os_v.compteurs["SetFilePointerEx"] += 1
            ent = os_v.poignees.get(rcx)
            if ent is None or r9 != 0:          # FILE_BEGIN seul (I4 de 05/06)
                os_v._erreur(6)
                self._retour(uc, 0)
            else:
                os_v.poignees[rcx] = (ent[0], rdx)
                if r8:
                    uc.mem_write(r8, struct.pack("<Q", rdx))
                self._retour(uc, 1)
        elif feuille == "ReadFile":
            pos = os_v.poignees.get(rcx, ("", 0))[1]
            donnees, ok = os_v.read_file(rcx, pos, r8)
            if not ok:
                self._retour(uc, 0)      # rax = 0 : l'échec, lu inchangé
                return
            if donnees:
                uc.mem_write(rdx, donnees)
            uc.mem_write(r9, struct.pack("<Q", len(donnees)))
            self._retour(uc, 1)
        elif feuille == "CloseHandle":
            self._retour(uc, 1 if os_v.close_handle(rcx) else 0)
        elif feuille == "GetLastError":
            os_v.compteurs["GetLastError"] += 1
            os_v.journal_gle.append((feuille, os_v.gle))
            self._retour(uc, os_v.gle)
        else:                                   # la liste est fermée
            raise ErreurHarnais(f"shim inconnu : {feuille}")

    def _instrument(self, uc, adresse, taille, donnees):
        if adresse in self.adr_shims:
            self._shim(uc, self.adr_shims[adresse])
        elif adresse == SHIM_MORT:
            self.os.appels_interdits += 1
            self._retour(uc, 0)          # le retour factice, le COMPTEUR dénonce

    # -- l'appelant factice ------------------------------------------------------

    def appeler(self, va: int, args: dict[str, int] | None = None):
        """Appelle un bloc comme une fonction msx64. Retourne le dict des
        registres de sortie + canaris + pile (l'ombre de l'appelant couverte)."""
        uc = self.uc
        for nom, val in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(REGS[nom], val)
        uc.reg_write(UC_X86_REG_RAX, 0)
        rsp = ENTREE_RSP
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp + 8, CANARI * 0x170)          # l'ombre de l'appelant
        uc.mem_write(rsp, struct.pack("<Q", RET_MAGIQUE))
        entree_rsp = rsp
        try:
            uc.emu_start(va, RET_MAGIQUE, count=200_000_000)
        except UcError as err:
            return {"crash": str(err), "entree_rsp": entree_rsp,
                    "canaris_haut": False, "pile_equilibree": False}
        sortie = {k: uc.reg_read(REGS[k]) for k in REGS}
        sortie["rax"] = verdict_eax(sortie["rax"])
        sortie["entree_rsp"] = entree_rsp
        sortie["crash"] = None
        sortie["pile_equilibree"] = uc.reg_read(REGS["rsp"]) == entree_rsp + 8
        sortie["canaris_haut"] = bytes(
            uc.mem_read(entree_rsp + 8, 0x170)) == CANARI * 0x170
        return sortie

    def non_volatiles_rendus(self, r: dict) -> bool:
        return all(r[nom] == SENTINELLES_NV[nom] for nom in SENTINELLES_NV)

    def etat_propre(self, r: dict) -> bool:
        return (r["crash"] is None and r["pile_equilibree"]
                and r["canaris_haut"] and self.non_volatiles_rendus(r))

    # -- les zones du domaine (les helpers de lecture/écriture) ------------------

    def cadre(self) -> bytes:
        return bytes(self.uc.mem_read(L.R_CADRE, 960))

    def ecrire_cadre(self, decalage: int, donnees: bytes) -> None:
        self.uc.mem_write(L.R_CADRE + decalage, donnees)

    def champ(self, decalage: int, n: int) -> bytes:
        return bytes(self.uc.mem_read(L.R_CADRE + decalage, n))

    def u64(self, decalage: int) -> int:
        return struct.unpack("<Q", self.champ(decalage, 8))[0]

    def u32(self, decalage: int) -> int:
        return struct.unpack("<I", self.champ(decalage, 4))[0]

    def chemin_cadre(self) -> str:
        brut = self.champ(0, 522)
        fin = brut.find(b"\x00\x00")
        if fin > 0:
            brut = brut[:fin + 1]
        return brut.decode("utf-16-le", errors="replace").rstrip("\x00")

    def panneau(self) -> bytes:
        return bytes(self.uc.mem_read(L.R_EMPREINTES, 48))

    def poser_journal(self, entrees: list[tuple[int, int]]) -> None:
        """Poser le journal d'édition (le format loupe-16 : u64 décalage ·
        u8 octet · 7 réserve — 256 entrées max, le nombre à +4096)."""
        self.uc.mem_write(L.R_JOURNAL, b"\x00" * L.ZONE_JOURNAL)
        for i, (dec, octet) in enumerate(entrees):
            self.uc.mem_write(L.R_JOURNAL + 16 * i,
                              struct.pack("<QB7x", dec, octet))
        self.uc.mem_write(L.R_JOURNAL + 4096, struct.pack("<I", len(entrees)))

    def journal_nombre(self) -> int:
        return struct.unpack("<I", bytes(
            self.uc.mem_read(L.R_JOURNAL + 4096, 4)))[0]

    def zones_annexes(self) -> bytes:
        """Les zones des chantiers SUIVANTS (saisie · motif · écran · hwnd ·
        métriques) : le noyau ne les touche QUE par l'hygiène de loupe-03."""
        return (bytes(self.uc.mem_read(L.R_SAISIE, L.ZONE_SAISIE))
                + bytes(self.uc.mem_read(L.R_MOTIF, L.ZONE_MOTIF))
                + bytes(self.uc.mem_read(L.R_ECRAN, L.ZONE_ECRAN))
                + bytes(self.uc.mem_read(L.R_HWND, L.ZONE_HWND))
                + bytes(self.uc.mem_read(L.R_METRIQUES, L.ZONE_METRIQUES)))


# --- Les témoins (le kit terrain en miniature — les contenus RECROISÉS hashlib) ---

def composer_temoins() -> dict[str, bytes]:
    """Les témoins du harnais : les trois formes du remplissage (1 o, 384 o,
    3 × 64 Kio + 1) et le témoin RFC 1321 (les sept messages concaténés aux
    offsets connus) — une génération FIXE (graine 20261107), indépendante de
    la graine de re-jeu : les témoins ne changent JAMAIS entre les re-jeux."""
    rng = random.Random(20261107)
    temoins = {
        "temoin-1.bin": b"\x42",
        "temoin-384.bin": rng.randbytes(384),
        "temoin-3f.bin": rng.randbytes(3 * 65536 + 1),
        "rfc1321.bin": b"".join(msg for _, msg, _ in VECTEURS_RFC1321),
    }
    return temoins


def offsets_rfc1321() -> list[tuple[str, int, int, bytes, str]]:
    """(nom, offset, longueur, message, condensé attendu) — les gammes du
    témoin RFC 1321."""
    out, pos = [], 0
    for nom, msg, attendu in VECTEURS_RFC1321:
        out.append((nom, pos, len(msg), msg, attendu))
        pos += len(msg)
    return out


def emplacer_session(emul: Emulation, os_v: OSVirtuel, chemin: str) -> int:
    """Ouvre la session par LOUPE-01 (le geste réel — la session née entière)
    et rend la poignée ; les tests repartent de l'état réel."""
    emul.uc.mem_write(ADRESSE_CHEMIN,
                      chemin.encode("utf-16-le") + b"\x00\x00")
    r = emul.appeler(L.LOUPE01_VA, {"rcx": ADRESSE_CHEMIN})
    if r["rax"] != 0:
        raise ErreurHarnais(f"l'ouverture de {chemin} a rendu {r['rax']}")
    return emul.u64(528)


def fermer_session(emul: Emulation) -> None:
    emul.appeler(L.LOUPE03_VA, {})


# --- V0 : les pièces du plan --------------------------------------------------------

def vecteur_v0():
    section("V0 — les pièces du plan (les scellés relus, l'erratum constaté)")
    donnees_m9 = open(os.path.join(TRIADE, SCELLE_M9), "rb").read()
    ok_m9 = (len(donnees_m9) == SCELLE_M9_TAILLE
             and hashlib.sha256(donnees_m9).hexdigest() == SCELLE_M9_SHA256)
    controle("V0.a:le-scelle-1.0.0-relu",
             ok_m9, f"{len(donnees_m9)} o, sha256 446279f3…00d93d — l'ancre R7 "
             "de la famille sha héritée")
    # L'ERRATUM loupe-01 r2 : la pièce de l'ère mesure 65 024 o (la taille
    # 44 544 fautive était celle du scellé 0.9.0 de l'ère close) — le harnais
    # le CONSTATE sur pièces en relisant la spécification révisée
    spec01 = open(os.path.join(ICI, "I", "loupe-01-ouvrir.md"),
                  encoding="utf-8").read()
    controle("V0.b:l'erratum-loupe-01-r2-constate",
             "révision 3" in spec01 and "65 024 o" in spec01
             and "44 544" in spec01,
             "la spec relue (révision 3, qui documente r2) : la taille 44 544 "
             "(l'ère close) corrigée en 65 024 o — la pièce mesure, "
             "l'empreinte 446279f3… était la bonne")
    donnees_m1 = open(os.path.join(TRIADE, SCELLE_M1), "rb").read()
    ok_m1 = (len(donnees_m1) == SCELLE_M1_TAILLE
             and hashlib.sha256(donnees_m1).hexdigest() == SCELLE_M1_SHA256)
    controle("V0.c:le-scelle-M1-relu",
             ok_m1, f"{len(donnees_m1)} o, sha256 8038585b…bff3c0 — l'ancre "
             "R7 de la minilibc héritée")
    # les notations d'origine intactes (les pièces relues : m1 + tls13)
    ok_notations = all(
        os.path.exists(os.path.join(chemin, nom + ".asm"))
        for (_, _, chemin, nom) in {**EMPLACEMENTS_M1, **EMPLACEMENTS_M9}.values())
    controle("V0.d:les-notations-d-origine-intactes", ok_notations,
             "libc-01/07 (m1/notation) + tls13-01..04 (tls13/notation) — "
             "les sources R7 du recoupement")
    # les SEPT specs du noyau relues (les têtes + les révisions)
    ok_specs = True
    for bid, nom in NOMS_NOYAU.items():
        chemin = os.path.join(ICI, "I", nom + ".md")
        if not os.path.exists(chemin):
            ok_specs = False
            continue
        premiere = open(chemin, encoding="utf-8").readline()
        if f"loupe-{bid[5:7]}" not in premiere or "révision" not in premiere:
            ok_specs = False
    controle("V0.e:les-sept-specs-du-noyau-relues", ok_specs,
             "les têtes des spécifications loupe-01..07 (la révision 2 de "
             "loupe-01 porte l'erratum de la taille de la pièce)")
    # le plan d'adressage : les slots du noyau ARRÊTÉS sur les mesures (D161)
    mesures = {"i110004": (47, 0x40), "i110001": (388, 0x1C0),
               "i110002": (296, 0x140), "i110003": (122, 0xC0),
               "i110005": (312, 0x180), "i110006": (879, 0x380),
               "i110007": (102, 0x80)}
    ordre = ("i110004", "i110001", "i110002", "i110003",
             "i110005", "i110006", "i110007")
    ok_slots = all(L.SLOTS_LOUPE[b][1] == s and s % 64 == 0 and s - t >= 16
                   for b, (t, s) in mesures.items())
    ok_tasse = all(L.SLOTS_LOUPE[a][0] + L.SLOTS_LOUPE[a][1] == L.SLOTS_LOUPE[b][0]
                   for a, b in zip(ordre, ordre[1:])) \
        and L.SLOTS_LOUPE["i110004"][0] == 0x4040
    controle("V0.f:les-slots-du-noyau-arretes-sur-les-mesures",
             ok_slots and ok_tasse,
             "multiples de 64, padding >= 16, tassés depuis 0x4040 (04@0x4040 → 01@0x4080 → 02@0x4240 → 03@0x4380"
             " → 05@0x4440 → 06@0x45C0 → 07@0x4940, fin 0x49C0) — la mesure "
             "décide (D161)")
    # l'IAT : 34 feuilles recomptées aux slots (l'ordre figé du geste (a))
    ok_iat = (len(L.IAT_SLOTS) == 34
              and len(L.IAT_KERNEL32) == 10 and len(L.IAT_USER32) == 18
              and len(L.IAT_GDI32) == 6
              and L.IAT_SLOTS["CreateFileW"] == 0x2418
              and L.IAT_SLOTS["ReadFile"] == 0x2430
              and L.IAT_SLOTS["GetLastError"] == 0x2448
              and L.IAT_SLOTS["GetStockObject"] == 0x24E0)
    controle("V0.g:l'IAT-34-feuilles-recomptee", ok_iat,
             "kernel32 10 @0x2400 · user32 18 @0x2450 · gdi32 6 @0x24E0 — "
             "l'ordre figé du plan (a)")
    # les zones .data aux adresses ARRÊTÉES (les tailles du geste (a))
    ok_zones = (L.R_CADRE == 0xE000 and L.R_EMPREINTES == 0xE3C0
                and L.R_SAISIE == 0xE400 and L.R_MOTIF == 0xE460
                and L.R_JOURNAL == 0xE4A0 and L.R_ECRAN == 0xF4C0
                and L.R_CUMUL == 0x10000
                and L.R_JOURNAL + L.ZONE_JOURNAL <= L.R_ECRAN
                and L.R_ECRAN + L.ZONE_ECRAN <= L.R_HWND
                and L.R_CUMUL + L.ZONE_CUMUL == 0x20000
                and L.R_K == 0x2F00 and L.R_TLS04 + 0xC0 <= 0xE000)
    controle("V0.h:les-zones-data-aux-adresses-arretees", ok_zones,
             "cadre 960 @0xE000 · empreintes 48 @0xE3C0 · journal 4112 "
             "@0xE4A0 · écran 2320 @0xF4C0 · CUMUL 64 Kio @0x10000 (fin "
             "0x20000) — la disposition source unique ; K[64] @0x2F00 LA "
             "TABLE DU SCELLÉ (le déplacement hérité la vise) ; la famille "
             "sha s'arrête à 0xC3C0, la marge jusqu'à .data VIERGE")
    return donnees_m9, donnees_m1


# --- V1 : round-trip + structure + l'héritage byte-identique (R7) -------------------

def vecteur_v1(emul: Emulation, donnees_m9: bytes, donnees_m1: bytes):
    section("V1 — round-trip + concordance au plan + l'héritage R7 constaté")
    insns_par_bloc = {}
    attendus = {"i110001": 388, "i110002": 296, "i110003": 122,
                "i110004": 47, "i110005": 312, "i110006": 879, "i110007": 102}
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_LOUPE[bid]
        chemin = os.path.join(ICI, "notation", NOMS_NOYAU[bid] + ".asm")
        octets, metas = B4.assembler_bloc(emul.ks, chemin, rva, slot)
        insns = B4.round_trip(emul.cs, emul.ks, chemin, rva, octets, metas)
        insns_par_bloc[bid] = insns
        controle(f"V1.a:{bid}:round-trip-100",
                 len(insns) == len(metas) and len(octets) == attendu,
                 f"{len(octets)} o == {attendu} o mesurés à l'arrêt, "
                 f"{len(insns)}/{len(metas)} instructions")

    # les déplacements RIP : les cibles == les symboles du plan (la liste fermée)
    cibles_legales = {L.R_CADRE, L.R_EMPREINTES, L.R_SAISIE, L.R_MOTIF,
                      L.R_JOURNAL, L.R_ECRAN, L.R_HWND, L.R_METRIQUES,
                      L.R_CUMUL, L.R_MD5_S} | set(L.IAT_SLOTS.values())
    ok_rip, vus = True, 0
    for bid, insns in insns_par_bloc.items():
        for insn in insns:
            cible = B4.operande_rip_cible(insn)
            if cible is not None:
                vus += 1
                if cible not in cibles_legales:
                    ok_rip = False
    controle("V1.b:les-deplacements-rip-aux-symboles-du-plan",
             ok_rip and vus >= 20,
             f"{vus} déplacements, chaque cible ∈ le plan (le cadre, les "
             "zones, CUMUL, MD5_S, les feuilles IAT)")

    # les appels directs : la liste fermée par bloc (le réseau des specs)
    appels_attendus = {
        "i110004": {L.R_LIBC07},
        "i110001": {L.R_LIBC01, L.LOUPE02_VA, L.LOUPE03_VA, L.LOUPE04_VA,
                    L.LOUPE07_VA},
        "i110002": set(),
        "i110003": {L.LOUPE04_VA, L.R_LIBC07},
        "i110005": {L.R_TLS01, L.R_TLS03, L.R_TLS04},
        "i110006": {L.R_LIBC01, L.R_LIBC07},   # + la sous-routine .comprimer
        "i110007": {L.LOUPE05_VA, L.LOUPE06_VA},
    }
    ok_appels = True
    for bid, attendu_set in appels_attendus.items():
        rva, slot = L.SLOTS_LOUPE[bid]
        for insn in insns_par_bloc[bid]:
            if insn.mnemonic == "call" and "[rip" not in insn.op_str:
                cible = int(insn.op_str, 0)
                if cible not in attendu_set and not (rva <= cible < rva + slot):
                    ok_appels = False
    controle("V1.c:les-appels-directs-a-la-liste-fermee",
             ok_appels, "loupe-01 → 02/03/04/07+libc-01 · loupe-03 → "
             "04+libc-07 · loupe-05 → tls13-01/03/04 · loupe-06 → libc-01 "
             "+ libc-07 (le couplage et les zéros du bourre) (+.comprimer "
             "locale) · loupe-07 → 05/06 — le réseau des specs")

    # les appels IAT par bloc : les feuilles déclarées (I5 de chaque spec)
    iat_par_bloc = {
        "i110001": {"CreateFileW", "GetFileSizeEx", "CloseHandle", "GetLastError"},
        "i110002": {"SetFilePointerEx", "ReadFile", "GetLastError"},
        "i110003": {"CloseHandle", "GetLastError"},
        "i110005": {"SetFilePointerEx", "ReadFile", "GetLastError"},
        "i110006": {"SetFilePointerEx", "ReadFile", "GetLastError"},
        "i110004": set(), "i110007": set(),
    }
    inverse = {v: k for k, v in L.IAT_SLOTS.items()}
    ok_iat = True
    for bid, attendu_feuilles in iat_par_bloc.items():
        for insn in insns_par_bloc[bid]:
            if insn.mnemonic == "call" and "[rip" in insn.op_str:
                cible = B4.operande_rip_cible(insn)
                feuille = inverse.get(cible)
                if feuille is None or feuille not in attendu_feuilles:
                    ok_iat = False
    controle("V1.d:les-feuilles-IAT-par-bloc-a-la-liste-fermee",
             ok_iat, "la liste fermée de chaque spec (I5) : 01 CreateFileW/"
             "GetFileSizeEx/CloseHandle/GetLastError · 02/05/06 SetFile-"
             "PointerEx/ReadFile/GetLastError · 03 CloseHandle/GetLastError "
             "· 04/07 AUCUNE (les feuilles pures)")

    # LES CONSTANTES MD5 RE-DÉRIVÉES PAR ARITHMÉTIQUE (le juge est le code)
    controle("V1.e:les-64-MD5_T-re-derives-par-sinus",
             deriv_MD5_T() == list(L.MD5_T),
             "T[i] = floor(2^32·|sin(i+1)|) — T[0] D76AA478, T[63] EB86D391 "
             "(RFC 1321 § 3.4)")
    controle("V1.f:les-64-MD5_S-re-comptes",
             deriv_MD5_S() == list(L.MD5_S),
             "les quatre rounds : (7,12,17,22) (5,9,14,20) (4,11,16,23) "
             "(6,10,15,21) — RFC 1321 § 3.1")
    controle("V1.g:les-4-abscisses-au-plan",
             list(L.MD5_ABSCISSE) == [0x67452301, 0xEFCDAB89,
                                      0x98BADCFE, 0x10325476],
             "RFC 1321 § 3.3 — les QUATRE abscisses de l'init")

    # la structure : AUCUN syscall (le noyau ne touche le monde QUE par l'IAT)
    ok_struct = True
    for bid, insns in insns_par_bloc.items():
        for insn in insns:
            if insn.mnemonic in ("syscall", "int", "sysenter"):
                ok_struct = False
    controle("V1.h:calcul-pur-aucun-syscall", ok_struct,
             "les sept notations — le monde n'est touché que par l'IAT "
             "déclarée (V1.d), jamais un site syscall")

    # L'HÉRITAGE PAR LA CARTE CONSTATÉ BYTE-IDENTIQUE (R7) : les octets
    # émulés == les octets EXTRAITS des scellés, ET les notations d'origine
    # ré-assemblées == les extraits (la double preuve)
    emul.poser_heritages(donnees_m9, donnees_m1)
    ok_r7, details_r7 = True, []
    for nom, (rva_orig, slot, chemin_notation, fichier) in \
            {**EMPLACEMENTS_M1, **EMPLACEMENTS_M9}.items():
        extraits = emul.extraits[nom]
        poses = emul.heritages[nom]
        if poses != extraits or len(poses) != slot:
            ok_r7 = False
            details_r7.append(f"{nom} : la pose diverge")
        octets_notation, _ = B4.assembler_bloc(
            emul.ks, os.path.join(chemin_notation, fichier + ".asm"),
            rva_orig, slot)
        if extraits[:len(octets_notation)] != octets_notation:
            ok_r7 = False
            details_r7.append(f"{nom} : la notation d'origine diverge du scellé")
    controle("V1.i:l'heritage-R7-byte-identique-constate",
             ok_r7, "libc-01/07 == selftest.exe (M1) · tls13-01..04 == "
             "proxy.exe (1.0.0) — les octets EXTRAITS DES SCELLÉS posés aux "
             "slots loupe, les notations d'origine ré-assemblées == les "
             "extraits (la double preuve)" + (" ; " + "; ".join(details_r7)
                                              if details_r7 else ""))

    # LA BORNE 2 Gio DANS LES OCTETS : mov eax, 0x80000000 (B8 00 00 00 80)
    # puis cmp r13, rax / jbe — le bord exact INCLUS (le refus est STRICTEMENT
    # au-delà) ; l'intégrale 2 Gio vit au terrain (le kit m10-(d))
    octets01, _ = emul.blobs["i110001"]
    ok_borne = b"\xb8\x00\x00\x00\x80" in octets01
    controle("V1.j:la-borne-2-Gio-dans-les-octets",
             ok_borne, "mov eax, 0x80000000 (zero-étendu : le bord exact "
             "0x80000000 est ACCEPTÉ, le refus est > — 2 Gio + 1 nommé à V5 ; "
             "l'intégrale vivra au terrain, le natif la calcule en secondes)")


# --- V2 : les sept vecteurs officiels RFC 1321 --------------------------------------

def vecteur_v2(emul: Emulation, temoins: dict[str, bytes]):
    section("V2 — les SEPT vecteurs officiels RFC 1321 (le doré, au fichier)")
    os_v = OSVirtuel()
    os_v.declarer("rfc1321.bin", FichierVirtuel(contenu=temoins["rfc1321.bin"]))
    emul.os = os_v
    emplacer_session(emul, os_v, "rfc1321.bin")
    ok_tous, details = True, []
    for i, (nom, offset, longueur, message, attendu_hex) in \
            enumerate(offsets_rfc1321()):
        attendu = bytes.fromhex(attendu_hex)
        # la référence CROISÉE : hashlib == le vecteur officiel (l'instrument
        # se contrôle avant de juger — la constante fautive serait attrapée)
        if hashlib.md5(message).hexdigest() != attendu_hex:
            controle(f"V2.{i}:reference-hashlib-{nom}", False,
                     "la constante du vecteur diverge de hashlib — "
                     "INSTRUMENT DÉFAILLANT")
            ok_tous = False
            continue
        r = emul.appeler(L.LOUPE06_VA, {"rcx": offset, "rdx": longueur,
                                        "r8": ADRESSE_SORTIE16})
        condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16))
        if not (condense == attendu and r["rax"] == 0 and emul.etat_propre(r)):
            ok_tous = False
            details.append(f"{nom} DIVERGE ({condense.hex()})")
    controle("V2.a:les-sept-vecteurs-octet-pour-octet", ok_tous,
             "loupe-06 AU FICHIER (les gammes du témoin RFC 1321) — chaque "
             "condensé == l'officiel, chaque attendu recroisé à hashlib"
             + (" ; " + "; ".join(details) if details else ""))
    # la gamme vide : le vecteur du vide par la gamme nulle (Q4)
    r = emul.appeler(L.LOUPE06_VA, {"rcx": 0, "rdx": 0, "r8": ADRESSE_SORTIE16})
    vide = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16))
    controle("V2.b:la-gamme-vide-le-vecteur-du-vide",
             vide == bytes.fromhex("d41d8cd98f00b204e9800998ecf8427e")
             and r["rax"] == 0,
             "d41d8cd98f00b204e9800998ecf8427e — RFC 1321 § A.5, la gamme "
             "nulle rend le condensé du vide")

    # le différentiel : 1 000 gammes aléatoires des témoins et de proxy.exe
    rng = random.Random(GRAINE)
    corpus = {"temoin-384.bin": temoins["temoin-384.bin"],
              "temoin-3f-8k.bin": temoins["temoin-3f.bin"][:8192],
              "proxy-8k.bin": temoins["proxy.exe"][:8192]}
    for nom_f, donnees in corpus.items():
        os_v.declarer(nom_f, FichierVirtuel(contenu=donnees))
    ok_diff, n_diff = True, 0
    comptes = {"temoin-384.bin": 334, "temoin-3f-8k.bin": 333,
               "proxy-8k.bin": 333}
    for nom_f, donnees in corpus.items():
        fermer_session(emul)
        emplacer_session(emul, os_v, nom_f)
        for _ in range(comptes[nom_f]):
            dec = rng.randrange(0, len(donnees) + 1)
            lon = rng.randrange(0, min(257, len(donnees) - dec + 1))
            r = emul.appeler(L.LOUPE06_VA, {"rcx": dec, "rdx": lon,
                                            "r8": ADRESSE_SORTIE16})
            condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16))
            attendu = hashlib.md5(donnees[dec:dec + lon]).digest()
            n_diff += 1
            if condense != attendu or r["rax"] != 0:
                ok_diff = False
    controle("V2.c:le-differentiel-1000-gammes-md5", ok_diff and n_diff == 1000,
             f"{n_diff} gammes aléatoires (graine {GRAINE}) des témoins et "
             "de proxy.exe — l'égalité exacte à hashlib.md5")

    # le témoin 3×64Kio+1 ENTIER (les fenêtres glissantes exercées)
    fermer_session(emul)
    os_v.declarer("temoin-3f.bin", FichierVirtuel(contenu=temoins["temoin-3f.bin"]))
    emplacer_session(emul, os_v, "temoin-3f.bin")
    r = emul.appeler(L.LOUPE06_VA, {"rcx": 0, "rdx": 196609,
                                    "r8": ADRESSE_SORTIE16})
    condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16))
    controle("V2.d:le-temoin-3f-entier-par-fenetres",
             condense == hashlib.md5(temoins["temoin-3f.bin"]).digest()
             and r["rax"] == 0,
             "196 609 o = 3 fenêtres de 64 Kio + 1 — le cumul par fenêtres "
             "glissantes, jamais tout en mémoire")
    fermer_session(emul)


# --- V3 : le différentiel SHA (l'héritage au travail) -------------------------------

def vecteur_v3(emul: Emulation, temoins: dict[str, bytes]):
    section("V3 — le différentiel SHA (l'héritage tls13 PAR LA CARTE)")
    os_v = emul.os
    # LA PIÈCE DE L'ÈRE : proxy.exe scellé en fichier virtuel RÉEL
    os_v.declarer("proxy.exe", FichierVirtuel(contenu=temoins["proxy.exe"]))
    emplacer_session(emul, os_v, "proxy.exe")
    r = emul.appeler(L.LOUPE05_VA, {"rcx": 0, "rdx": 65024,
                                    "r8": ADRESSE_SORTIE32})
    condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE32, 32))
    controle("V3.a:proxy-scele-la-gamme-entiere",
             condense == hashlib.sha256(temoins["proxy.exe"]).digest()
             == bytes.fromhex(SCELLE_M9_SHA256) and r["rax"] == 0,
             "loupe-05(0, 65024) == hashlib == 446279f3…00d93d — L'APPLICATION "
             "REND L'EMPREINTE DE SA PROPRE PIÈCE (la composition héritée, "
             "les fenêtres 64 Kio)")
    fermer_session(emul)

    # les vecteurs FIPS au fichier (Q3 de loupe-05)
    ok_fips = True
    for i, (nom, message, attendu_hex) in enumerate(VECTEURS_FIPS):
        if hashlib.sha256(message).hexdigest() != attendu_hex:
            ok_fips = False
            continue
        chemin_f = f"fips-{i}.bin"
        os_v.declarer(chemin_f, FichierVirtuel(contenu=message))
        emplacer_session(emul, os_v, chemin_f)
        r = emul.appeler(L.LOUPE05_VA, {"rcx": 0, "rdx": len(message),
                                        "r8": ADRESSE_SORTIE32})
        condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE32, 32))
        if condense != bytes.fromhex(attendu_hex) or r["rax"] != 0:
            ok_fips = False
        fermer_session(emul)
    controle("V3.b:les-vecteurs-FIPS-au-fichier", ok_fips,
             "le vide (e3b0c442…) et « abc » (ba7816bf…) rejoués AU FICHIER "
             "par l'héritage — chaque attendu recroisé à hashlib")

    # les gammes aléatoires (la graine) : proxy.exe PUIS le témoin 3f —
    # chaque fichier SA session (l'ouverture n'est pas un goulot à répéter)
    rng = random.Random(GRAINE + 1)
    ok_diff, n_diff = True, 0
    for nom_f in ("proxy.exe", "temoin-3f.bin"):
        donnees = temoins[nom_f]
        emplacer_session(emul, os_v, nom_f)
        for _ in range(100):
            dec = rng.randrange(0, len(donnees) + 1)
            lon = rng.randrange(0, min(4097, len(donnees) - dec + 1))
            r = emul.appeler(L.LOUPE05_VA, {"rcx": dec, "rdx": lon,
                                            "r8": ADRESSE_SORTIE32})
            condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE32, 32))
            attendu = hashlib.sha256(donnees[dec:dec + lon]).digest()
            n_diff += 1
            if condense != attendu or r["rax"] != 0:
                ok_diff = False
        fermer_session(emul)
    controle("V3.c:le-differentiel-200-gammes-sha", ok_diff,
             f"{n_diff} gammes aléatoires (graine {GRAINE + 1}) de proxy.exe "
             "scellé et du témoin 3f — l'égalité exacte à hashlib.sha256")

    # le témoin 3f entier (les fenêtres)
    emplacer_session(emul, os_v, "temoin-3f.bin")
    r = emul.appeler(L.LOUPE05_VA, {"rcx": 0, "rdx": 196609,
                                    "r8": ADRESSE_SORTIE32})
    condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE32, 32))
    controle("V3.d:le-temoin-3f-entier-par-fenetres",
             condense == hashlib.sha256(temoins["temoin-3f.bin"]).digest()
             and r["rax"] == 0,
             "196 609 o : la composition héritée passe ses fenêtres glissantes")
    fermer_session(emul)


# --- V4 : le noyau fichier (les scénarios de chaque bloc) ---------------------------

CADRE_VIERGE = b"\x00" * 528 + b"\xFF" * 8 + b"\x00" * 424


def vecteur_v4(emul: Emulation, temoins: dict[str, bytes]):
    section("V4 — le noyau fichier (le cadre, la session née entière, les états)")
    os_v = emul.os
    for nom, contenu in temoins.items():
        os_v.declarer(nom, FichierVirtuel(contenu=contenu))

    # LOUPE-04 : le cadre vierge (V1 de loupe-04) — 960 o : zéros partout
    # sauf la poignée INVALIDE aux octets +528..+535
    emul.ecrire_cadre(0, b"\xEE" * 960)          # un état sale AVANT le geste
    r = emul.appeler(L.LOUPE04_VA, {})
    controle("V4.a:loupe-04-le-cadre-vierge",
             emul.cadre() == CADRE_VIERGE and r["rax"] == 0
             and emul.etat_propre(r),
             "960 o : zéros partout sauf la poignée INVALIDE @+528 (V1 de "
             "loupe-04 — le modèle recomposé octet par octet, depuis un "
             "état sale de 0xEE)")

    # LOUPE-01 : la session née ENTIÈRE (V1 de loupe-01) — le témoin 384
    emplacer_session(emul, os_v, "temoin-384.bin")
    controle("V4.b:loupe-01-la-session-nee-entiere",
             emul.chemin_cadre() == "temoin-384.bin" and emul.u64(520) == 384
             and emul.u64(536) == 0 and emul.u64(544) == 0
             and emul.u32(552) == 384
             and emul.champ(568, 384) == temoins["temoin-384.bin"],
             "le cadre champ à champ : le chemin COPIÉ (libc-01 PAR LA "
             "CARTE), la taille, la vue 0, le curseur 0, le remplissage 384, "
             "le tampon == le témoin (la fenêtre lue par loupe-02)")
    attendu_panneau = (hashlib.md5(temoins["temoin-384.bin"]).digest()
                       + hashlib.sha256(temoins["temoin-384.bin"]).digest())
    controle("V4.c:loupe-01-le-panneau-ne",
             emul.panneau() == attendu_panneau,
             "le panneau d'empreintes 48 o == (md5, sha256) du témoin — "
             "né par loupe-07 À L'OUVERTURE (Q4), recoupé à hashlib")

    # LOUPE-01 révision 3 : LE FICHIER VIDE — la session née entière SANS la
    # fenêtre (loupe-02 P3 refuse toute fenêtre sur taille 0) ; le
    # remplissage 0, LE PANNEAU DU VIDE défini (d41d8cd9… + e3b0c442…)
    os_v.declarer("vide.bin", FichierVirtuel(contenu=b""))
    fermer_session(emul)
    emplacer_session(emul, os_v, "vide.bin")
    controle("V4.c2:loupe-01-le-fichier-vide",
             emul.chemin_cadre() == "vide.bin" and emul.u64(520) == 0
             and emul.u32(552) == 0
             and emul.panneau() == (hashlib.md5(b"").digest()
                                    + hashlib.sha256(b"").digest()),
             "le vide s'ouvre : remplissage 0, la grille vide un état "
             "légitime, le panneau == (d41d8cd9…, e3b0c442…) — les empreintes "
             "du vide, RFC 1321 § A.5 et FIPS 180-4 (révision 3 de la spec)")
    fermer_session(emul)

    # LOUPE-02 : la fenêtre bornée (V1 de loupe-02) — 1 000 décalages valides
    rng = random.Random(GRAINE + 2)
    ok_l, n_l = True, 0
    emplacer_session(emul, os_v, "temoin-384.bin")
    for _ in range(1000):
        dec = rng.randrange(0, 384) & ~0xF        # multiple de 16 (P2)
        r = emul.appeler(L.LOUPE02_VA, {"rcx": dec})
        attendu_rempl = 384 - dec
        if not (r["rax"] == 0 and emul.u32(552) == attendu_rempl
                and emul.champ(568, attendu_rempl)
                == temoins["temoin-384.bin"][dec:dec + attendu_rempl]):
            ok_l = False
        n_l += 1
    fermer_session(emul)
    emplacer_session(emul, os_v, "temoin-3f.bin")
    for _ in range(60):
        dec = rng.randrange(0, 196609) & ~0xF
        r = emul.appeler(L.LOUPE02_VA, {"rcx": dec})
        attendu_rempl = min(384, 196609 - dec)
        if not (r["rax"] == 0 and emul.u32(552) == attendu_rempl
                and emul.champ(568, attendu_rempl)
                == temoins["temoin-3f.bin"][dec:dec + attendu_rempl]
                and emul.u64(536) == 0):
            ok_l = False
        n_l += 1
    controle("V4.d:loupe-02-la-fenetre-bornee", ok_l,
             f"{n_l} décalages aléatoires valides (les témoins 384 et 3f) — "
             "le remplissage == min(384, taille−décalage), le tampon == la "
             "découpe Python, la vue et le curseur INTACTS")

    # LE RECOUVREMENT du journal (V2 de loupe-02) : l'édition survit
    emul.poser_journal([(0, 0xAA), (16, 0xBB), (383, 0xCC), (400, 0xDD)])
    r = emul.appeler(L.LOUPE02_VA, {"rcx": 0})
    modele = bytearray(temoins["temoin-3f.bin"][0:384])
    modele[0] = 0xAA
    modele[16] = 0xBB
    modele[383] = 0xCC                       # le dernier de la fenêtre
    controle("V4.e:loupe-02-le-recouvrement-du-journal",
             r["rax"] == 0 and emul.champ(568, 384) == bytes(modele),
             "les entrées 0/16/383 (dans la fenêtre) RECOUVERTES, l'entrée "
             "400 (hors fenêtre) IGNORÉE — l'édition survit au défilement")

    # LOUPE-03 : la fermeture (V1/V2 de loupe-03) — l'hygiène + l'idempotence
    emul.poser_journal([(8, 0x11)])
    emul.uc.mem_write(L.R_MOTIF + 32, struct.pack("<I", 7))
    emul.uc.mem_write(L.R_SAISIE, struct.pack("<I", 2))
    avant_close = os_v.compteurs["CloseHandle"]
    r = emul.appeler(L.LOUPE03_VA, {})
    ok_hygiene = (r["rax"] == 0 and emul.etat_propre(r)
                  and emul.cadre() == CADRE_VIERGE
                  and emul.journal_nombre() == 0
                  and struct.unpack("<I", bytes(
                      emul.uc.mem_read(L.R_MOTIF + 32, 4)))[0] == 0
                  and struct.unpack("<I", bytes(
                      emul.uc.mem_read(L.R_SAISIE, 4)))[0] == 0
                  and os_v.compteurs["CloseHandle"] == avant_close + 1)
    # l'idempotence : fermer sur session fermée — AUCUN appel, rien bougé
    avant_close2 = os_v.compteurs["CloseHandle"]
    cadre_avant = emul.cadre()
    r2 = emul.appeler(L.LOUPE03_VA, {})
    controle("V4.f:loupe-03-la-fermeture-propre",
             ok_hygiene,
             "le cadre re-vierge, le journal nombre 0, le motif longueur 0, "
             "le mode saisie 0, UNE fermeture comptée — l'hygiène ne fuit "
             "jamais d'un fichier à l'autre")
    controle("V4.g:loupe-03-l'idempotence",
             r2["rax"] == 0 and emul.etat_propre(r2)
             and os_v.compteurs["CloseHandle"] == avant_close2
             and emul.cadre() == cadre_avant,
             "session close : rax = 0, AUCUN appel CloseHandle (compté), "
             "le cadre relu identique — rien fait, rien de plus")

    # LOUPE-07 : le panneau du fichier entier (V1 de loupe-07)
    ok_07 = True
    for nom in ("temoin-1.bin", "proxy.exe"):
        emplacer_session(emul, os_v, nom)
        donnees = temoins[nom]
        r = emul.appeler(L.LOUPE07_VA, {"rcx": ADRESSE_SORTIE48})
        panneau = bytes(emul.uc.mem_read(ADRESSE_SORTIE48, 48))
        attendu = (hashlib.md5(donnees).digest()
                   + hashlib.sha256(donnees).digest())
        if not (r["rax"] == 0 and emul.etat_propre(r) and panneau == attendu):
            ok_07 = False
        fermer_session(emul)
    controle("V4.h:loupe-07-le-panneau-du-fichier-entier", ok_07,
             "le témoin 1 o ET proxy.exe scellé (65 024 o) : les 48 o == "
             "(md5, sha256) hashlib — les DEUX passages par TAMPON_CUMUL, "
             "l'un après l'autre")

    # les zones des chantiers suivants INTACTES (le noyau ne les touche pas)
    controle("V4.i:les-zones-annexes-intactes",
             emul.zones_annexes() == b"\x00" * (L.ZONE_SAISIE + L.ZONE_MOTIF
                                                + L.ZONE_ECRAN + L.ZONE_HWND
                                                + L.ZONE_METRIQUES),
             "saisie · motif · écran · hwnd · métriques : les zéros du "
             "départ — le noyau n'y touche QUE par l'hygiène de loupe-03")


# --- V5 : les rejets nommés -----------------------------------------------------------

def vecteur_v5(emul: Emulation, temoins: dict[str, bytes]):
    section("V5 — les rejets nommés (la table des SEPT verdicts, sur pièces)")
    os_v = emul.os
    adr = ADRESSE_CHEMIN

    # LOUPE-01 E1 : le chemin absent → -2 (la barre le nomme)
    emul.uc.mem_write(adr, "absent.bin".encode("utf-16-le") + b"\x00\x00")
    r = emul.appeler(L.LOUPE01_VA, {"rcx": adr})
    ok_absent = r["rax"] == -2 and emul.etat_propre(r)
    # E2 : le fichier verrouillé → -7
    os_v.declarer("verrouille.bin", FichierVirtuel(contenu=b"\x00" * 16,
                                                   verrouille=True))
    emul.uc.mem_write(adr, "verrouille.bin".encode("utf-16-le") + b"\x00\x00")
    r = emul.appeler(L.LOUPE01_VA, {"rcx": adr})
    ok_verrou = r["rax"] == -7
    # E3 : l'accès refusé → -6 (gle consigné)
    os_v.declarer("acces-refuse.bin", FichierVirtuel(contenu=b"\x00" * 16,
                                                     refus_acces=True))
    emul.uc.mem_write(adr, "acces-refuse.bin".encode("utf-16-le") + b"\x00\x00")
    r = emul.appeler(L.LOUPE01_VA, {"rcx": adr})
    ok_acces = r["rax"] == -6 and any(c == 5 for _, c in os_v.journal_gle)
    controle("V5.a:loupe-01-les-trois-refus-d-OS",
             ok_absent and ok_verrou and ok_acces,
             "absent → -2 (gle 2) · verrouillé → -7 (gle 32) · accès "
             "refusé → -6 (gle 5 AU JOURNAL du harnais) — traduits par la "
             "table, jamais un code brut à la barre (I4)")
    os_v.journal_gle.clear()

    # Q2 : LA BORNE NOMMÉE — 2 Gio + 1 → -3, la poignée FERMÉE AVANT le
    # retour (jamais une poignée pendante)
    os_v.declarer("geant-plus.bin",
                  FichierVirtuel(contenu=None, taille=0x80000001))
    emul.uc.mem_write(adr, "geant-plus.bin".encode("utf-16-le") + b"\x00\x00")
    avant_close = os_v.compteurs["CloseHandle"]
    r = emul.appeler(L.LOUPE01_VA, {"rcx": adr})
    controle("V5.b:loupe-01-la-borne-2-Gio",
             r["rax"] == -3 and emul.etat_propre(r)
             and os_v.compteurs["CloseHandle"] == avant_close + 1
             and emul.cadre() == CADRE_VIERGE,
             "la taille déclarée 2 Gio + 1 → -3, la poignée REFERMÉE AVANT "
             "le retour (comptée), le cadre re-vierge — hors périmètre 0.1.0")

    # E4 : la session déjà ouverte → -5, RIEN TOUCHÉ (l'ancien fichier INTACT)
    emplacer_session(emul, os_v, "temoin-384.bin")
    cadre_avant = emul.cadre()
    panneau_avant = emul.panneau()
    emul.uc.mem_write(adr, "temoin-1.bin".encode("utf-16-le") + b"\x00\x00")
    r = emul.appeler(L.LOUPE01_VA, {"rcx": adr})
    controle("V5.c:loupe-01-la-session-double",
             r["rax"] == -5 and emul.etat_propre(r)
             and emul.cadre() == cadre_avant and emul.panneau() == panneau_avant,
             "l'ouverture sur session ouverte → -5, le cadre ET le panneau "
             "relu identiques — l'ancien fichier INTACT, un fichier à la fois")

    # le chemin trop long (P1) : 260 sans NUL → -5, jamais un débordement
    # (le fichier EXISTE sous ce nom : le refus vient de la MESURE, jamais
    # d'un -2 d'absence qui précéderait)
    fermer_session(emul)
    nom_long = "A" * 260
    os_v.declarer(nom_long, FichierVirtuel(contenu=b"\x00" * 16))
    emul.uc.mem_write(adr, (nom_long + "\x00").encode("utf-16-le"))
    r = emul.appeler(L.LOUPE01_VA, {"rcx": adr})
    ok_long = r["rax"] == -5 and emul.champ(0, 4) == b"\x00\x00\x00\x00"
    controle("V5.d:loupe-01-le-chemin-trop-long", ok_long,
             "260 caractères sans NUL → -5 (l'argument invalide), RIEN au "
             "cadre — jamais un débordement, le renforcement nommé de P1")

    # LOUPE-02 : les QUATRE refus de la fenêtre (V3 de loupe-02)
    r1 = emul.appeler(L.LOUPE02_VA, {"rcx": 0})                     # sans session
    emplacer_session(emul, os_v, "temoin-384.bin")
    r2_ = emul.appeler(L.LOUPE02_VA, {"rcx": 8})                    # non aligné
    r3_ = emul.appeler(L.LOUPE02_VA, {"rcx": 384})                  # à la taille
    r4_ = emul.appeler(L.LOUPE02_VA, {"rcx": 512})                  # au-delà
    controle("V5.e:loupe-02-les-quatre-refus",
             r1["rax"] == -4 and r2_["rax"] == -5 and r3_["rax"] == -3
             and r4_["rax"] == -3 and all(emul.etat_propre(x)
                                           for x in (r1, r2_, r3_, r4_)),
             "sans session -4 · non multiple de 16 -5 (la grille ne se "
             "penchera pas) · à la taille -3 · au-delà -3 — RIEN lu")

    # LOUPE-05/06 : sans session / hors bornes / la sortie nulle
    fermer_session(emul)
    r5a = emul.appeler(L.LOUPE05_VA, {"rcx": 0, "rdx": 1, "r8": ADRESSE_SORTIE32})
    r6a = emul.appeler(L.LOUPE06_VA, {"rcx": 0, "rdx": 1, "r8": ADRESSE_SORTIE16})
    emplacer_session(emul, os_v, "temoin-384.bin")
    r5b = emul.appeler(L.LOUPE05_VA, {"rcx": 384, "rdx": 1, "r8": ADRESSE_SORTIE32})
    r6b = emul.appeler(L.LOUPE06_VA, {"rcx": 384, "rdx": 1, "r8": ADRESSE_SORTIE16})
    r5c = emul.appeler(L.LOUPE05_VA, {"rcx": 0, "rdx": 1, "r8": 0})
    r6c = emul.appeler(L.LOUPE06_VA, {"rcx": 0, "rdx": 1, "r8": 0})
    controle("V5.f:loupe-05-06-les-refus-de-gamme",
             r5a["rax"] == -4 and r6a["rax"] == -4
             and r5b["rax"] == -3 and r6b["rax"] == -3
             and r5c["rax"] == -5 and r6c["rax"] == -5,
             "sans session -4 · la gamme hors fichier -3 · la sortie "
             "nulle -5 — les TROIS verdicts nommés de chaque bloc")

    # LE SHIM ReadFile EN ÉCHEC (V4 de loupe-02/05/06, E3 de loupe-07)
    os_v.armer_echec_read(1)
    os_v.journal_gle.clear()
    emul.uc.mem_write(ADRESSE_SORTIE32, CANARI * 32)
    r = emul.appeler(L.LOUPE05_VA, {"rcx": 0, "rdx": 384, "r8": ADRESSE_SORTIE32})
    sortie_intacte = bytes(emul.uc.mem_read(ADRESSE_SORTIE32, 32)) == CANARI * 32
    ok_gle = any(c == 1117 for _, c in os_v.journal_gle)
    os_v.armer_echec_read(None)
    controle("V5.g:loupe-05-le-refus-systeme-la-sortie-intacte",
             r["rax"] == -6 and sortie_intacte and ok_gle
             and emul.etat_propre(r),
             "le shim ReadFile en échec → -6, la sortie INTACTE (comparée à "
             "son état d'avant — jamais un condensé partiel), le code 1117 "
             "AU JOURNAL du harnais")
    os_v.journal_gle.clear()
    # loupe-02 : le refus système → remplissage 0 (fail-closed)
    os_v.armer_echec_read(1)
    r = emul.appeler(L.LOUPE02_VA, {"rcx": 0})
    remplissage = emul.u32(552)
    os_v.armer_echec_read(None)
    controle("V5.h:loupe-02-le-refus-systeme-fail-closed",
             r["rax"] == -6 and remplissage == 0,
             "remplissage = 0 — le tampon ne montre JAMAIS un octet non lu "
             "(E4 de loupe-02)")
    # loupe-06 : le refus système → la sortie intacte
    os_v.armer_echec_read(1)
    emul.uc.mem_write(ADRESSE_SORTIE16, CANARI * 16)
    r = emul.appeler(L.LOUPE06_VA, {"rcx": 0, "rdx": 384, "r8": ADRESSE_SORTIE16})
    ok6 = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16)) == CANARI * 16
    os_v.armer_echec_read(None)
    controle("V5.i:loupe-06-le-refus-systeme-la-sortie-intacte",
             r["rax"] == -6 and ok6,
             "la sortie INTACTE — le calcul ne publie que le vrai (E4)")
    # loupe-07 E3 : le refus RELAYÉ TEL QUEL (le verdict traverse)
    os_v.armer_echec_read(1)
    emul.uc.mem_write(ADRESSE_SORTIE48, CANARI * 48)
    r = emul.appeler(L.LOUPE07_VA, {"rcx": ADRESSE_SORTIE48})
    panneau_intact = bytes(emul.uc.mem_read(ADRESSE_SORTIE48, 48)) == CANARI * 48
    os_v.armer_echec_read(None)
    controle("V5.j:loupe-07-le-refus-relaye-tel-quel",
             r["rax"] == -6 and panneau_intact,
             "le -6 de loupe-05 traverse loupe-07 sans être avalé — le "
             "panneau ne publie RIEN (E3)")
    # loupe-01 : le refus de la session née → LA SESSION CLOSE, le verdict
    # remonte (jamais une poignée pendante)
    fermer_session(emul)
    os_v.armer_echec_read(1)
    avant_close = os_v.compteurs["CloseHandle"]
    emul.uc.mem_write(adr, "temoin-384.bin".encode("utf-16-le") + b"\x00\x00")
    r = emul.appeler(L.LOUPE01_VA, {"rcx": adr})
    cadre = emul.cadre()
    os_v.armer_echec_read(None)
    controle("V5.k:loupe-01-le-refus-propage-la-session-close",
             r["rax"] == -6 and os_v.compteurs["CloseHandle"] == avant_close + 1
             and cadre == CADRE_VIERGE,
             "le ReadFile de loupe-02 en échec à l'ouverture : le refus -6 "
             "remonte, loupe-03 A FERMÉ (comptée), le cadre re-vierge — "
             "jamais une poignée pendante")


# --- V6 : la falsification (zéro silence) ----------------------------------------------

def vecteur_v6(emul: Emulation, temoins: dict[str, bytes]):
    section("V6 — la falsification (une mutation = un échec, zéro silence)")
    os_v = emul.os

    # UNE CONSTANTE MD5_T MUTÉE D'UN ULP à la table .rdata (V5 de loupe-06) :
    # les sept vecteurs dorés échouent — attrapés PAR LES VECTEURS OFFICIELS
    # (avec la session OUVERTE : la divergence vient de la TABLE, jamais
    # d'un refus — rax == 0 exigé à chaque gamme)
    emplacer_session(emul, os_v, "rfc1321.bin")
    table_originale = bytes(emul.uc.mem_read(L.R_MD5_T, 256))
    mutee = bytearray(table_originale)
    mutee[4] ^= 0x01                     # T[1] d'un ulp (le bit 0 du 2e mot)
    emul.uc.mem_write(L.R_MD5_T, bytes(mutee))
    divergences = 0
    for nom, offset, longueur, message, attendu_hex in offsets_rfc1321():
        r = emul.appeler(L.LOUPE06_VA, {"rcx": offset, "rdx": longueur,
                                        "r8": ADRESSE_SORTIE16})
        condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16))
        if r["rax"] == 0 and condense != bytes.fromhex(attendu_hex):
            divergences += 1
    emul.uc.mem_write(L.R_MD5_T, table_originale)     # la table restaurée
    controle("V6.a:la-constante-mutee-attrapee-par-les-vecteurs",
             divergences == 7,
             f"T[1] muté d'un ulp : {divergences}/7 vecteurs dorés "
             "échouent — la falsification DEMANDÉE est attrapée par les "
             "VECTEURS OFFICIELS (jamais par une inspection de code)")

    # la table restaurée : le vecteur re-passe (la restauration prouvée)
    # — la gamme de « abc » À SON OFFSET dans le témoin concaténé
    _, off_abc, lon_abc, _, attendu_abc = offsets_rfc1321()[2]
    r = emul.appeler(L.LOUPE06_VA, {"rcx": off_abc, "rdx": lon_abc,
                                    "r8": ADRESSE_SORTIE16})
    condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16))
    controle("V6.b:la-table-restauree-les-vecteurs-repassent",
             condense == bytes.fromhex(attendu_abc) and r["rax"] == 0,
             "« abc » re-passe après restauration — la mutation ne laisse "
             "AUCUNE trace")

    # LA COMPARAISON N'EST PAS MUETTE : chaque octet du condensé attendu
    # muté → l'égalité échoue (16 essais, l'anti-muet)
    r = emul.appeler(L.LOUPE06_VA, {"rcx": 0, "rdx": 3, "r8": ADRESSE_SORTIE16})
    condense = bytes(emul.uc.mem_read(ADRESSE_SORTIE16, 16))
    ok_muet = all((condense[:i] + bytes([condense[i] ^ 1]) + condense[i + 1:])
                  != condense for i in range(16))
    controle("V6.c:l'anti-muet-16-octets-mutes", ok_muet,
             "chaque octet du condensé attendu muté d'un bit → l'égalité "
             "échoue — la différentielle n'est pas muette")

    # LE TAMPON DE VUE INTACT pendant le calcul (I3 de loupe-05/06 :
    # l'exclusion de famille — la lecture passe par TAMPON_CUMUL, jamais
    # le tampon de vue du cadre)
    fermer_session(emul)
    emplacer_session(emul, os_v, "temoin-3f.bin")
    motif_vue = bytes((i * 3 + 1) & 0xFF for i in range(384))
    ok_vue = True
    for va, sortie, nom in ((L.LOUPE05_VA, ADRESSE_SORTIE32, "loupe-05"),
                            (L.LOUPE06_VA, ADRESSE_SORTIE16, "loupe-06")):
        emul.ecrire_cadre(568, motif_vue)
        r = emul.appeler(va, {"rcx": 0, "rdx": 196609, "r8": sortie})
        if emul.champ(568, 384) != motif_vue:
            ok_vue = False
    controle("V6.d:le-tampon-de-vue-intact-pendant-le-calcul", ok_vue,
             "loupe-05 ET loupe-06 sur 196 609 o : les 384 o du tampon "
             "de vue relus IDENTIQUES — la lecture vit à TAMPON_CUMUL "
             "(l'exclusion de famille, jamais deux flux)")

    # LE JOURNAL INTACT pendant loupe-07 (I4 : le calcul ne touche à rien
    # de la session) + LE PANNEAU TOUJOURS CELUI DU DISQUE (I3 : les
    # écritures non sauvées n'y figurent PAS)
    emul.poser_journal([(16, 0x55), (32, 0x66)])
    journal_avant = bytes(emul.uc.mem_read(L.R_JOURNAL, L.ZONE_JOURNAL))
    r = emul.appeler(L.LOUPE07_VA, {"rcx": ADRESSE_SORTIE48})
    panneau = bytes(emul.uc.mem_read(ADRESSE_SORTIE48, 48))
    attendu = (hashlib.md5(temoins["temoin-3f.bin"]).digest()
               + hashlib.sha256(temoins["temoin-3f.bin"]).digest())
    controle("V6.e:le-journal-intact-le-panneau-du-disque",
             bytes(emul.uc.mem_read(L.R_JOURNAL, L.ZONE_JOURNAL))
             == journal_avant and r["rax"] == 0 and panneau == attendu,
             "les écritures en attente demeurent AU JOURNAL, le panneau "
             "== les empreintes du DISQUE — l'astérisque de la barre "
             "nommera la divergence (jamais un condensé d'avant)")
    fermer_session(emul)


# --- Le cahier complet ---------------------------------------------------------------

GRAINE = 20261108


def main() -> int:
    global GRAINE
    if "--graine" in sys.argv:
        GRAINE = int(sys.argv[sys.argv.index("--graine") + 1])
    print(f"=== loupe/harnais_noyau.py — LE HARNAIS DU NOYAU (chantier "
          f"M10-(b), graine {GRAINE}) ===")
    temoins = composer_temoins()
    temoins["proxy.exe"] = open(os.path.join(TRIADE, SCELLE_M9), "rb").read()

    donnees_m9, donnees_m1 = vecteur_v0()
    os_v = OSVirtuel()
    emul = Emulation(os_v)
    vecteur_v1(emul, donnees_m9, donnees_m1)
    vecteur_v2(emul, temoins)
    vecteur_v3(emul, temoins)
    vecteur_v4(emul, temoins)
    vecteur_v5(emul, temoins)
    vecteur_v6(emul, temoins)

    # le compte final : AUCUNE feuille hors noyau n'a été appelée
    controle("FINAL:aucune-feuille-hors-noyau-appellee",
             emul.os.appels_interdits == 0,
             "les 28 feuilles IAT hors noyau n'ont JAMAIS été touchées (le "
             "compteur du mort) — la liste fermée tenue sur pièces")

    total = len(REUSSITES) + len(ECHECS)
    print(f"\n=== LE CAHIER : {total} contrôles — "
          f"{len(REUSSITES)} VERTS, {len(ECHECS)} ÉCHECS ===")
    if ECHECS:
        for nom, detail in ECHECS:
            print(f"  [ÉCHEC] {nom} — {detail}")
        print("VERDICT : ÉCHEC — le chantier n'est pas prouvé")
        return 1
    print("VERDICT : VERT — le noyau loupe-01..07 est NOTÉ-MESURÉ-PROUVÉ "
          "sur pièces (les vecteurs officiels, le différentiel hashlib, "
          "l'héritage sha byte-identique — R7, les rejets nommés, la "
          "falsification attrapée)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
