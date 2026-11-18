#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite16C.py — LE TERRAIN D'ATTRIBUTION DE L'UNITÉ 04 D210
(loupe-16 saisie × bras C — la pièce C compilée RE-LIVRÉE via le kit
standard minimal ; le plan D210 § 4 : « la pièce C re-livrée via un kit
standard minimal — la question "le flux compilé pur l'aurait-il
produite ?" tranchée sur pièces »).

Le kit porte UNE pièce et UN scénario :
  loupe-16-d210-c.dll  la pièce du bras C — le source SCELLÉ de la
                      campagne (source-loupe-16-C.c, sha256 892ef03e…,
                      le même byte pour byte que le kit v3 de l'unité 04)
                      compilé par LE FLUX STANDARD : x86_64-w64-mingw32-gcc
                      12.2.0 -O2 -std=c11 -Wall -Wextra -shared (la
                      chaîne prescrite au LISEZMOI du kit T ; le GAP mingw
                      du labo clos par la chaîne Debian extraite — la
                      commande exacte consignée au LISEZMOI de CE kit) ;
                      L'EXPORT UNIQUE loupe_16_saisie ;
  le présent script   python SEUL (ctypes, hashlib, os, platform, random,
                      struct, sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le modèle de la campagne Loupe, inchangé depuis
l'édition v2 du kit 01 : la découverte PAR LA TABLE, les gardes
fail-closed — la leçon de la 304 reconduite) : le scénario est LE
CHARGEUR — LoadLibraryEx DONT_RESOLVE (aucune feuille résolue, AUCUN
démarreur exécuté), il découvre LUI-MÊME l'export loupe_16_saisie à la
table d'exports du PE et l'APPELLE à son adresse. LA CLÔTURE DE LA
PIÈCE APPELLE UNE FEUILLE — le strlen de msvcrt.dll, par son thunk IAT
(la fermeture constatée au labo : poser_message, le message à la barre,
passe par strlen ; le précédent de la 304 : le memcmp de l'unité 5) :
le scénario découvre le slot PAR LA TABLE D'IMPORTS (le descripteur aux
CINQ champs — la loi L2 ; la marche des plages FT jusqu'au séparateur
NULL — la doctrine D54 ; AUCUNE RVA codée — la leçon de la 302) et LIE
la feuille au strlen de la machine AVANT le premier appel, au guichet
fail-closed : chaque geste vérifié, VirtualProtect l'instant de
l'écriture, LA REPROTECTION, LA RELECTURE recoupée (le memmove à SON
COMPTE — huit octets, la loi L4).

L'ÉCRAN PASSE EN ARGUMENT (la loi L5 PAR CONSTRUCTION au bras C) : la
pièce reçoit « lignes = 27 » à CHAQUE appel — la zone WM_SIZE que le
bras T doit poser n'existe pas ici : le miroir C la demande, le juge la
donne, le modèle la tient (le même 27 que le harnais du labo et que
l'épreuve POSIX — l'écran annoncé, l'écran posé).

LE JUGE EST LE MODÈLE INDÉPENDANT (le miroir Python de l'oracle du bras
T — le même que l'épreuve POSIX de la construction : les MÊMES vecteurs,
la MÊME graine 20261115) — jamais les octets de la pièce.

LES VECTEURS DU CONTRAT (loupe-16 révision 1 — le miroir du bras T) :
  V1  le différentiel : 10 000 frappes aux DEUX disques (le témoin 3f
      de 63 o ET le grand 8k — les ré-écritures, la frontière des 256
      distincts, la vue qui suit, le recouvrement) == le modèle Python
      à CHAQUE frappe ;
  V2  le scénario doré : « 4d5a » au curseur 0x22 (les DEUX octets au
      journal ET au tampon, la marque, la garde, la cellule suivante)
      ET LA VUE QUI SUIT (le curseur au bord → le recadrage à 208, la
      relecture-miroir, le recouvrement au tampon) ;
  V3  les rejets : E1 sans session → -4 la barre nommée ; E2 la cellule
      fantôme → -3 RIEN au journal (ET la fantôme MARQUE SALE — le
      remplissage lu u32 SEUL) ; le fichier vide → -3 ; E3 le 257e
      distinct → -3 « journal plein - Ctrl+S », RIEN perdu ;
  V4  le repli : « z », « ! », l'espace IGNORÉS proprement ; VK_SUPPR à
      l'attente → le nibble EFFACÉ ; hors attente : ignoré ;
  V5  la falsification : LA GARDE RÉ-ARMÉE à l'écriture (le scénario de
      loupe-18 — éditer puis Alt+F4 UNE SEULE fois doit avertir — TIENT
      à la pièce juste) ET LE DISQUE FALSIFIÉ (l'octet 8 de la fenêtre
      re-lue muté AU BUFFER VIVANT) : le tampon après la relecture == le
      modèle du MUTANT, DIVERGENT de l'original — la pièce a lu SON
      disque à elle, la différentielle ATTRAPE LE FAUX (le fixture
      falsifie-16.bin vit au réceptacle preuves-unite16C/).

  le témoin : temoin-unite16C.txt au réceptacle preuves-unite16C/ —
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
PIECE = os.path.join(ICI, "loupe-16-d210-c.dll")
RECEPTACLE = os.path.join(ICI, "preuves-unite16C")

# LES CONSTANTES DU PLAN (loupe/layout.py — la source unique)
GRAINE = 20261115
TAMPON = 384
EDITS = 256
LIGNES = 27            # l'écran PASSÉ EN ARGUMENT — la loi L5 par construction
VK_SUPPR = 0x08

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


# ==================== LE MODÈLE INDÉPENDANT (jamais la pièce) ================
# (le miroir VERBATIM de l'épreuve POSIX de la construction — la 349 : le
# même modèle qui y courut 14 VERT contre la pièce C même)


def m_journal_seconde(journal, curseur, octet):
    for i, (dec, _) in enumerate(journal):
        if dec == curseur:
            journal[i] = (curseur, octet)
            return journal, False
    if len(journal) >= EDITS:
        return journal, True
    journal.append((curseur, octet))
    return journal, False


def m_vue_suit(curseur, vue, taille, lignes=LIGNES):
    v = min(24, max(0, lignes - 3))
    if vue <= curseur < vue + v * 16:
        return vue, False
    nv = min((max(0, curseur - 176)) & ~15,
             (max(0, taille - TAMPON) + 15) & ~15 if taille > TAMPON else 0)
    return nv, nv != vue


def fenetre_editee(disk, journal, vue, rempl):
    fen = bytearray(disk[vue:vue + rempl])
    for dec, oct_ in journal:
        if vue <= dec < vue + rempl:
            fen[dec - vue] = oct_
    return bytes(fen)


# ==================== LA SESSION — les zones du plan, AU JUGE ================
# (le miroir des zones : le cadre, la saisie, le journal, le disque — la
# pièce écrit DEDANS, jamais une copie froide ; le disque vit AU BUFFER
# vivant : la falsification V5 le mute SOUS la pièce)


class Session:
    def __init__(self, saisir, disk: bytes):
        self.saisir = saisir
        self.disk = bytes(disk)
        self.disque = ctypes.create_string_buffer(self.disk, len(self.disk) + 1)
        self.cadre = bytearray(960)
        struct.pack_into("<Q", self.cadre, 520, len(disk))       # taille
        struct.pack_into("<Q", self.cadre, 528, 0x1000)          # poignée
        struct.pack_into("<Q", self.cadre, 536, 0)                # vue
        struct.pack_into("<Q", self.cadre, 544, 0x22)             # curseur
        struct.pack_into("<I", self.cadre, 552, min(TAMPON, len(disk)))
        self.cadre[568:568 + min(TAMPON, len(disk))] = \
            bytearray(disk[:min(TAMPON, len(disk))])
        self.saisie = bytearray(96)
        self.journal = bytearray(4112)
        struct.pack_into("<I", self.journal, 4096, 0)

    def frappe(self, caractere: int):
        # les zones PASSÉES EN ÉCRITURE (des vues vivantes — la pièce écrit
        # DEDANS) ; L'ÉCRAN EN ARGUMENT : LIGNES à chaque appel (la loi L5)
        cadre = (ctypes.c_char * 960).from_buffer(self.cadre)
        saisie = (ctypes.c_char * 96).from_buffer(self.saisie)
        journal = (ctypes.c_char * 4112).from_buffer(self.journal)
        return verdict(self.saisir(cadre, saisie, journal, self.disque,
                                   LIGNES, caractere))

    def muter_disque(self, offset: int, valeur: int) -> None:
        self.disque[offset] = valeur & 0xFF       # le buffer VIVANT muté

    def octets_disque(self) -> bytes:
        return bytes(self.disque[:len(self.disk)])

    def lit(self, off, n=8, zone=None):
        z = self.cadre if zone is None else zone
        return int.from_bytes(bytes(z[off:off + n]), "little")

    def journal_lu(self):
        n = self.lit(4096, 4, self.journal)
        return [(self.lit(16 * i, 8, self.journal),
                 self.journal[16 * i + 8]) for i in range(n)]

    def attente(self):
        return struct.unpack_from("<II", self.saisie, 4)

    def barre(self):
        return bytes(self.saisie[12:12 + 80]).split(b"\x00")[0]


# ==================== LES VECTEURS — le contrat loupe-16 révision 1 ==========
# (le miroir de l'épreuve POSIX : les MÊMES tirages, la MÊME graine —
# chaque vecteur une fonction PURE sur (saisir, Session) : le labo les
# rejouera VERBATIM contre la dll mappée — l'épreuve du kit, plomberie
# comprise, la brèche de la 302 refermée)


def v1_le_differentiel(saisir):
    """V1 — 10 000 frappes aux DEUX disques, tout == le modèle à chaque frappe."""
    rng = random.Random(GRAINE)
    hexa = b"0123456789abcdefABCDEF"
    bruit = b"z! "
    for nom, disk, depart in (
            ("temoin-3f", bytes((i * 7 + 3) & 0xFF for i in range(63)), 0x22),
            ("grand-8k", bytes((i * 31 + 7) & 0xFF for i in range(8192)), 0x17E)):
        taille = len(disk)
        s = Session(saisir, disk)
        struct.pack_into("<Q", s.cadre, 544, depart)
        journal, m_tampon = [], bytearray(
            disk[:min(TAMPON, taille)].ljust(TAMPON, b"\x00"))
        curseur, vue, rempl = depart, 0, min(TAMPON, taille)
        m_actif, m_nibble = 0, 0
        divergences = 0
        for _ in range(10_000):
            tirage = rng.random()
            frappe = VK_SUPPR if tirage < 0.02 else (
                rng.choice(bruit) if tirage < 0.04 else rng.choice(hexa))
            r = s.frappe(frappe)
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
                        curseur = min(curseur + 1, taille - 1) if taille > 1 else 0
                        nv, relu = m_vue_suit(curseur, vue, taille)
                        if relu:
                            vue = nv
                            rempl = min(TAMPON, taille - vue)
                            m_tampon = bytearray(
                                fenetre_editee(disk, journal, vue, rempl)
                                .ljust(TAMPON, b"\x00"))
            probleme = None
            if r not in (0, -3):
                probleme = f"le verdict {r} inattendu"
            actif, nibble = struct.unpack_from("<II", s.saisie, 4)
            if probleme is None and (actif, nibble) != (
                    m_actif, m_nibble if m_actif else 0):
                probleme = "l'attente diverge"
            elif probleme is None and s.journal_lu() != journal:
                probleme = "le journal diverge"
            elif probleme is None and (s.lit(544) != curseur
                                       or s.lit(536) != vue):
                probleme = "curseur/vue divergent"
            elif probleme is None and s.lit(552, 4) != rempl:
                probleme = "le remplissage diverge"
            elif probleme is None and bytes(
                    s.cadre[568:568 + TAMPON]) != bytes(m_tampon):
                probleme = "le tampon diverge"
            elif probleme is None and s.lit(556, 4) != (1 if journal else 0):
                probleme = "la marque diverge"
            elif probleme is None and s.lit(560, 4) != 0:
                probleme = "la garde diverge"
            if probleme:
                divergences += 1
                if divergences <= 3:
                    consigne(f"    [{nom}] {probleme}")
        controle(f"V1:le-differentiel-10000-frappes-{nom}", divergences == 0,
                 "le journal PAR DÉCALAGE (la réécriture REMPLACE, la borne "
                 "256 refusée), l'attente CONSOMMÉE, le tampon (le "
                 "recouvrement), la marque, la garde, le pas clampé, LA VUE "
                 "QUI SUIT — tout == le modèle Python")


def v2_le_scenario_dore(saisir):
    """V2 — « 4d5a » au curseur 0x22, puis la vue qui suit au bord."""
    s = Session(saisir, bytes((i * 7 + 3) & 0xFF for i in range(63)))
    for ch in (0x34, 0x64, 0x35, 0x61):
        r = s.frappe(ch)
    controle("V2:le-scenario-4d5a",
             r == 0 and s.lit(544) == 0x24 and s.lit(556, 4) == 1
             and s.lit(560, 4) == 0
             and s.journal_lu() == [(0x22, 0x4D), (0x23, 0x5A)]
             and s.cadre[568 + 0x22] == 0x4D and s.cadre[568 + 0x23] == 0x5A,
             "« 4d5a » : les DEUX octets au journal ET au tampon, la marque, "
             "LA GARDE ré-armée, la cellule suivante active (curseur 0x24)")
    disk = bytes((i * 31 + 7) & 0xFF for i in range(8192))
    s = Session(saisir, disk)
    struct.pack_into("<Q", s.cadre, 544, 0x17E)
    s.frappe(0x34)
    s.frappe(0x41)
    r = s.frappe(0x35)
    r = s.frappe(0x30)
    attendu = fenetre_editee(disk, [(0x17E, 0x4A), (0x17F, 0x50)], 208, TAMPON)
    controle("V2:la-vue-qui-suit-le-recadrage",
             r == 0 and s.lit(544) == 384 and s.lit(536) == 208
             and s.lit(552, 4) == TAMPON
             and bytes(s.cadre[568:568 + TAMPON]) == attendu,
             "le curseur au-delà de la vitrine → la nouvelle vue 208 "
             "(aligne16_inf), LA RELECTURE-MIROIR (le disque + le "
             "recouvrement du journal), remplissage 384 — la cellule suivante "
             "ATTEND à l'écran")


def v3_les_rejets(saisir):
    """V3 — E1, la fantôme (ET sale), le vide, E3 le 257e distinct."""
    s = Session(saisir, bytes(63))
    struct.pack_into("<Q", s.cadre, 528, (1 << 64) - 1)          # hors session
    r = s.frappe(0x34)
    controle("V3:E1-sans-session", r == -4 and s.barre() == b"aucun fichier ouvert",
             "-4, la phrase nommée à la barre (le mode MESSAGE posé)")
    s = Session(saisir, bytes(TAMPON))
    struct.pack_into("<Q", s.cadre, 544, TAMPON + 5)
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    controle("V3:E2-la-cellule-fantome",
             r == -3 and s.lit(4096, 4, s.journal) == 0 and s.attente() == (0, 0)
             and s.barre() == b"hors bornes",
             "le curseur forgé au-delà du remplissage → -3, RIEN au journal "
             "(le refus PRÉCÈDE), l'attente CONSOMMÉE")
    struct.pack_into("<I", s.cadre, 556, 1)                     # la marque
    struct.pack_into("<Q", s.cadre, 544, TAMPON + 5)
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    controle("V3:E2-la-fantome-marche-sale",
             r == -3 and s.lit(4096, 4, s.journal) == 0,
             "la marque posée : la fantôme REFUSÉE QUAND MÊME — le "
             "remplissage lu u32 SEUL (jamais le qword)")
    s = Session(saisir, b"")                                    # le vide
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    controle("V3:le-fichier-vide", r == -3 and s.lit(4096, 4, s.journal) == 0,
             "taille zéro : aucune cellule n'existe → -3")
    s = Session(saisir, bytes(TAMPON))
    struct.pack_into("<Q", s.cadre, 544, 0x20)
    for i in range(256):                                        # 256 distincts
        struct.pack_into("<Q", s.journal, 16 * i, 0x40 + i)
        s.journal[16 * i + 8] = (i * 7) & 0xFF
    struct.pack_into("<I", s.journal, 4096, 256)
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    controle("V3:E3-le-257e-distinct",
             r == -3 and s.lit(4096, 4, s.journal) == 256
             and s.barre() == b"journal plein - Ctrl+S",
             "le 257e distinct → -3 nommé, les 256 INTACTS (RIEN perdu)")
    return s


def v4_le_repli(saisir, s):
    """V4 — les ignorés, VK_SUPPR à l'attente (la session de V3 poursuite)."""
    for ch in (0x7A, 0x21, 0x20):
        r = s.frappe(ch)
        if r != 0:
            break
    controle("V4:le-non-hexa-ignore",
             r == 0 and s.lit(4096, 4, s.journal) == 256,
             "« z », « ! », l'espace IGNORÉS proprement (rien bougé)")
    s2 = Session(saisir, bytes(63))
    s2.frappe(0x34)
    s2.frappe(VK_SUPPR)
    attente = s2.attente()
    r = s2.frappe(VK_SUPPR)
    controle("V4:vk-suppr-a-l-attente",
             attente == (0, 0) and r == 0
             and s2.lit(4096, 4, s2.journal) == 0,
             "« 4 » frappé, VK_SUPPR : le nibble EFFACÉ ; hors attente : "
             "ignoré")


def v5_la_falsification(saisir):
    """V5 — la garde ré-armée (loupe-18 tient) ET le disque falsifié attrapé."""
    # ① LA GARDE : l'écriture RÉ-ARME (le premier Alt+F4 refusé, l'écrit
    # l'efface — le scénario de loupe-18 : éditer puis Alt+F4 UNE SEULE fois
    # doit avertir)
    s = Session(saisir, bytes(TAMPON))
    struct.pack_into("<I", s.cadre, 560, 1)     # le premier Alt+F4 refusé
    s.frappe(0x62)
    r = s.frappe(0x62)                          # « bb » → l'octet 0xBB
    controle("V5:la-garde-re-armee-a-l-ecriture",
             r == 0 and s.lit(560, 4) == 0,
             "la pièce : l'écriture RÉ-ARME la garde (refus_quitter = 0) — "
             "Alt+F4 une seule fois après l'édition AVERTIRAIT (le scénario "
             "de loupe-18 tient au bras C)")
    # ② LE DISQUE FALSIFIÉ : l'octet 8 de la fenêtre re-lue muté AU BUFFER
    # VIVANT — la relecture-miroir le lira-elle ? le modèle du MUTANT
    # diverge de l'original : la pièce a lu SON disque à elle
    os.makedirs(RECEPTACLE, exist_ok=True)
    disk = bytes((i * 31 + 7) & 0xFF for i in range(8192))
    s = Session(saisir, disk)
    struct.pack_into("<Q", s.cadre, 544, TAMPON - 1)     # 383 — le bord
    struct.pack_into("<Q", s.cadre, 536, 0)
    curseur0 = TAMPON - 1
    fen = bytearray(disk[curseur0:curseur0 + TAMPON])
    fen[8] ^= 0x35                                        # l'octet muté
    mutant_offset = curseur0 + 8
    s.muter_disque(mutant_offset, fen[8])                 # le buffer VIVANT
    chemin_faux = os.path.join(RECEPTACLE, "falsifie-16.bin")
    with open(chemin_faux, "wb") as f:                    # le disque falsifié
        f.write(s.octets_disque())
    for ch in (0x34, 0x61):                               # « 4a » au bord
        r = s.frappe(ch)
    attendu_vue = m_vue_suit(curseur0 + 1, 0, len(disk))[0]
    tampon_faux = bytes(s.cadre[568:568 + TAMPON])
    original = fenetre_editee(disk, [(curseur0, 0x4A)], attendu_vue, TAMPON)
    mutant = fenetre_editee(s.octets_disque(), [(curseur0, 0x4A)],
                            attendu_vue, TAMPON)
    controle("V5:le-disque-falsifie-attrape", r == 0
             and s.lit(544) == curseur0 + 1 and s.lit(536) == attendu_vue
             and tampon_faux != original
             and tampon_faux == mutant,
             "le disque falsifié (l'octet 8 de la fenêtre re-lue muté AU "
             "BUFFER VIVANT) : le tampon après la relecture == le modèle du "
             "MUTANT (divergent de l'original) — la pièce a lu SON disque à "
             "elle, la différentielle ATTRAPE LE FAUX (le fixture "
             "falsifie-16.bin vit au réceptacle)")


# ==================== LE TERRAIN — Windows, le chargeur, le guichet =========


def main() -> int:
    consigne("=== LE RUN D'ATTRIBUTION DE L'UNITÉ 04 D210 (loupe-16 saisie × "
             "bras C — la pièce C compilée re-livrée via le kit standard "
             "minimal, le plan D210 § 4) — le terrain du développeur ===")
    empreintes = lire_empreintes()
    if not empreintes:
        consigne("[T0] REFUS : aucune EMPREINTES*.txt au kit — rien ne court")
        return 2
    sha_dll = sha256_fichier(PIECE)
    attendu = empreintes.get("loupe-16-d210-c.dll", "")
    if sha_dll != attendu:
        consigne(f"[T0] REFUS : loupe-16-d210-c.dll {sha_dll[:16]}… != "
                 f"l'empreinte gravée {attendu[:16]}… — la pièce a divergé, "
                 "rien ne court")
        return 2
    controle("T0:la-piece-recoupee-a-l-empreinte-gravee", True,
             f"loupe-16-d210-c.dll sha256 {sha_dll[:16]}… == la gravure du kit")

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
    # (base, rva) — la leçon de la 302 : les gardes fail-closed) -------------
    def lire_octets(rva: int, n: int) -> bytes:
        brut = (ctypes.c_ubyte * n)()
        ctypes.memmove(brut, base + rva, n)
        return bytes(brut)

    def lire_u32(rva: int) -> int:
        return struct.unpack("<I", lire_octets(rva, 4))[0]

    def lire_u16(rva: int) -> int:
        return struct.unpack("<H", lire_octets(rva, 2))[0]

    def lire_chaine(rva: int) -> str:
        sortie = []
        for i in range(256):
            c = lire_octets(rva + i, 1)[0]
            if c == 0:
                return "".join(sortie)
            sortie.append(chr(c))
        return "".join(sortie)

    e_lfanew = struct.unpack("<I", lire_octets(0x3C, 4))[0]
    opt = e_lfanew + 4 + 20                      # l'en-tête optionnel PE32+
    rva_exports = lire_u32(opt + 112)            # le répertoire 0 : export
    if not rva_exports:
        consigne("[T0] REFUS : le répertoire d'exports introuvable — la "
                 "pièce n'est pas la DLL attendue")
        return 2
    nb_noms = lire_u32(rva_exports + 24)
    tab_fonctions = lire_u32(rva_exports + 28)
    tab_noms = lire_u32(rva_exports + 32)
    tab_ordinaux = lire_u32(rva_exports + 36)
    rva_par_nom = {}
    for i in range(nb_noms):
        nom = lire_chaine(lire_u32(tab_noms + 4 * i))
        ordinal = lire_u16(tab_ordinaux + 2 * i)
        if nom:
            rva_par_nom[nom] = lire_u32(tab_fonctions + 4 * ordinal)
    if set(rva_par_nom) != {"loupe_16_saisie"}:
        consigne(f"[T0] REFUS : les exports découverts {sorted(rva_par_nom)} "
                 f"!= l'export unique loupe_16_saisie — la pièce a divergé")
        return 2
    R_LOUPE16 = rva_par_nom["loupe_16_saisie"]
    consigne(f"[T0] l'export UNIQUE découvert : loupe_16_saisie "
             f"@+{R_LOUPE16:#x} — la saisie au bras C, l'écran EN ARGUMENT")

    # ---- LA FEUILLE STRLEN LIÉE (le seul appel de la clôture de la pièce) --
    # DONT_RESOLVE ne lie RIEN : le slot IAT de strlen garde sa valeur SUR
    # DISQUE — l'entrée hint/nom, une RVA NUE. Le précédent de la 304 (le
    # memcmp de l'unité 5) : appeler la pièce sans lier la feuille que sa
    # clôture appelle, c'est sauter à l'adresse nue. Le scénario, chargeur
    # minimal, découvre le slot PAR LA TABLE D'IMPORTS (le descripteur aux
    # CINQ champs — la loi L2 ; la marche des plages FT jusqu'au séparateur
    # NULL — la doctrine D54 ; AUCUNE RVA codée) et lie la feuille au strlen
    # de la machine, AU GUICHET FAIL-CLOSED : chaque geste vérifié, l'écart
    # nommé, le flux stoppé — jamais un appel sur une feuille morte.
    def lier_feuille_strlen():
        """Le guichet de la feuille : (rva du slot, valeur sur disque,
        adresse liée) ou None — l'écart nommé, le flux stoppé."""
        rep_imports = lire_u32(opt + 120)  # le répertoire 1 : imports
        if not rep_imports:
            consigne("[T0] REFUS : le répertoire d'imports introuvable — "
                     "la pièce n'est pas la DLL attendue")
            return None
        rva_slot, termine = None, False
        for num_desc in range(16):               # la garde : jamais au-delà
            # LE DESCRIPTEUR AUX CINQ CHAMPS (la loi L2 — la faute de la 350
            # fut le parse à QUATRE)
            ilt, _, _, rva_dll, iat = struct.unpack(
                "<IIIII", lire_octets(rep_imports + 20 * num_desc, 20))
            if ilt == 0 and iat == 0:            # le terminateur lu au champ
                termine = True
                break
            if lire_chaine(rva_dll).lower() != "msvcrt.dll":
                continue                         # KERNEL32 : le démarreur CRT
            marche = ilt if ilt else iat         # la doctrine D54 : les FT
            for k in range(4096):                # la garde : jamais au-delà
                entree = struct.unpack(
                    "<Q", lire_octets(marche + 8 * k, 8))[0]
                if entree == 0:                  # le terminateur lu au champ
                    termine = True
                    break
                if not entree & (1 << 63) and \
                        lire_chaine(entree + 2) == "strlen":
                    rva_slot = iat + 8 * k       # LE slot, découvert par le nom
            if rva_slot is not None:
                break
        if rva_slot is None or not termine:
            consigne("[T0] REFUS : la feuille strlen de msvcrt.dll "
                     "introuvable à la table d'imports — la pièce a divergé")
            return None
        sur_disque = struct.unpack(
            "<Q", lire_octets(rva_slot, 8))[0]
        k32.LoadLibraryW.restype = ctypes.c_void_p
        k32.LoadLibraryW.argtypes = [wt.LPCWSTR]
        msvcrt = k32.LoadLibraryW("msvcrt.dll")
        if not msvcrt:
            consigne(f"[T0] REFUS : msvcrt.dll introuvable (GetLastError "
                     f"{ctypes.get_last_error()}) — la feuille ne peut être "
                     "liée")
            return None
        k32.GetProcAddress.restype = ctypes.c_void_p
        k32.GetProcAddress.argtypes = [ctypes.c_void_p, wt.LPCSTR]
        adresse = k32.GetProcAddress(msvcrt, b"strlen")
        if not adresse:
            consigne(f"[T0] REFUS : strlen introuvable dans msvcrt.dll "
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
        # LA LIAISON — le memmove à SON COMPTE : huit octets, la largeur du
        # slot qword (la loi L4 — l'arité de la faute de la 351)
        ctypes.memmove(base + rva_slot, struct.pack("<Q", adresse), 8)
        rendu = wt.BOOL(k32.VirtualProtect(base + rva_slot, 8, ancien.value,
                                           ctypes.byref(ancien)))
        if not rendu:
            consigne(f"[T0] REFUS : la re-protection du slot a échoué "
                     f"(GetLastError {ctypes.get_last_error()}) — l'écrit "
                     "demeure, la page ouverte : RIEN ne court")
            return None
        relue = struct.unpack("<Q", lire_octets(rva_slot, 8))[0]
        if relue != adresse:
            consigne(f"[T0] REFUS : la relecture du slot {relue:#x} != "
                     f"l'adresse liée {adresse:#x} — la liaison n'est pas "
                     "certaine")
            return None
        return rva_slot, sur_disque, adresse

    feuille = lier_feuille_strlen()
    if feuille is None:
        return 2
    rva_slot, sur_disque, adresse_strlen = feuille
    consigne(f"[guichet] la feuille unique liée : strlen de msvcrt.dll — le "
             f"slot IAT @+{rva_slot:#x} (la valeur sur disque {sur_disque:#x}, "
             f"l'entrée hint/nom — l'adresse nue où l'on sauterait sans la "
             f"liaison) repointé à {adresse_strlen:#x}, l'écriture protégée "
             "l'instant du geste, la relecture recoupée (le guichet "
             "fail-closed — la leçon de la 304)")

    # LA PIÈCE COMME FONCTION (la conduite de la main du kit — SIX arguments
    # msx64 : cadre, saisie, journal, disque aux registres, LIGNES et le
    # caractère aux slots de pile [rsp+0x20] et [rsp+0x28] — posés par ctypes)
    SAISIR = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                              ctypes.c_void_p, ctypes.c_void_p,
                              ctypes.c_void_p, ctypes.c_uint,
                              ctypes.c_uint)(base + R_LOUPE16)

    # ---- LES VECTEURS (le contrat rejoué — le miroir de l'épreuve POSIX) ---
    v1_le_differentiel(SAISIR)
    v2_le_scenario_dore(SAISIR)
    s_v3 = v3_les_rejets(SAISIR)
    v4_le_repli(SAISIR, s_v3)
    v5_la_falsification(SAISIR)

    # ---- LE TÉMOIN ----------------------------------------------------------
    lignes = []
    lignes.append("TÉMOIN DU RUN D'ATTRIBUTION DE L'UNITÉ 04 D210 — loupe-16 "
                  "saisie × bras C (la pièce C compilée re-livrée via le kit "
                  "standard minimal — le plan D210 § 4)")
    lignes.append("=" * 78)
    lignes.append(f"le run      : "
                  f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
                  f" (UTC) — la machine du développeur")
    lignes.append(f"la machine  : {platform.node()} · {platform.system()} "
                  f"{platform.release()} · {platform.machine()} · "
                  f"Python {platform.python_version()}")
    lignes.append(f"la pièce    : loupe-16-d210-c.dll "
                  f"{os.path.getsize(PIECE)} o, sha256 {sha_dll}")
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
    lignes.append("  renvoyer le dossier preuves-unite16C/ ENTIER au coffre "
                  "/test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite16C.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN D'ATTRIBUTION FINI : dater et signer le témoin de "
             "votre main, renvoyer preuves-unite16C/ ENTIER au coffre /test "
             "===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
