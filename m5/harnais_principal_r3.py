#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_principal_r3.py — Harnais de la révision http-12:R3 (0.6.0, D136).

LA révision de l'orchestrateur : LA CLI NAÎT (--relever-https arme la
politique ; TOUT argument inconnu = REFUS NOMMÉ, ExitProcess 3, AVANT toute
initialisation — E4), LA PORTE M5 garde la couche .text4 (UNE entrée
(0x8000, 0x2000, somme .text4) marchée aux bornes, fail-closed, miroir D95 —
la porte se garde elle-même : le bloc 0x8C80 est DANS la plage gardée), la
boucle d'acceptation câble http-10:R3 @0x81C0 (LE CÂBLAGE 0.6.0, l'unique
différence fonctionnelle avec R2) et la politique armée est NOMMÉE au journal
(« relever-https arme », entre la bannière et l'écoute — I2).

Vecteurs de la spécification m5/I/http-12-principal-r3.md (écrite-avant-code) :
  V1  round-trip de notation 100 % — R3 (779 o == en-tête « Code : N o »,
      idempotence) ET les DEUX ancêtres assemblés à leurs RVA (http-12:R2
      scellé 0.5.1 @0x7DC0, http-12:R1 scellé 0.4.0 @0x1800) : le préalable
      du différentiel ;
  V2  différentiel d'ancêtre — R2 émulé contre R3 émulé sur les MÊMES
      scénarios SANS argument (ordres exacts Q3, démarrage nominal, corruption
      de squelette/.text3/.text4, accepts successifs, quit, échecs E2/E3) :
      traces IDENTIQUES sauf la cible du spawn session (0x74C0 -> 0x81C0 —
      LA divergence légitime unique) et l'appel GetCommandLineW (la CLI est
      le domaine NOUVEAU, normalisé hors différentiel) ; divergence
      légitime nommée : la corruption .text4 (R2 ne la garde pas — sa porte
      est la table M3/M4 —, R3 la nomme KO — miroir du domaine .text3 de
      l'harnais R2) ; la CLI (drapeau, casse mixte, guillemets, arguments
      multiples, troncature, suffixe) est un domaine SANS ANCÊTRE : le modèle
      de parsing (écrit depuis la SPÉCIFICATION Q2, jamais la notation) juge
      l'émulation OCTET PAR OCTET, la politique .data comprise ;
  V3  fuzz de la porte M5 ET de l'héritage — toute mutation d'un champ
      (rva/taille/somme) des DEUX tables ou tout octet gardé → KO, JAMAIS de
      passage silencieux (le modèle de marche et les octets nomment le même
      verdict) ; fuzz CLI — toute casse, toute troncature, tout suffixe de
      --relever-https est un refus nommé (E4), jamais un armement ; les
      octets mutés évitent le code de R3 et les trappes (la corruption du
      VÉRIFICATEUR n'est pas décidable par le vérificateur — miroir M3) ;
  V4  falsification — mutations d'un point stables en taille (leçon D82)
      attrapées : les DEUX contre-câblages (lea -> 0x74C0 / 0x5580), la
      borne M5 décalée ±0x10, le plancher abaissé, la ligne de politique
      amnésiée, la politique jamais armée, l'ordre d'initialisation, la
      politique armée SANS argument, l'argument inconnu accepté en silence,
      le code de sortie E4 ; témoin vert.

Le harnais émule les octets des NOTATIONS (R3 à 0x8C80, l'ancêtre R2 scellé
0.5.1 à 0x7DC0, l'ancêtre R1 à 0x1800 — R7 : les ancêtres restent embarqués,
morts au lancement de R3, vivants à la preuve d'héritage). L'image
d'émulation couvre 0x1000-0xB000 : remplissage int3-déterministe, les TROIS
orchestrateurs, cinq trappes (hello-02, tcp-01/02/06/11) aux RVA réels, SIX
shims IAT (GetCommandLineW en propre @0xA100 — l'IAT M5 du layout — plus les
cinq hérités), fixtures .rdata héritées ET M5 (refus CLI, ligne de
politique, commande UTF-16), état .data (R_POLITIQUE à l'état image 0 — P3),
LA LIGNE DE COMMANDE (buffer UTF-16 hors plages gardées @0xA200), la table
R10 héritée (28 entrées) ET LA PORTE M5 (UNE entrée) — les sommes sont
calculées sur l'image AVANT mutation (la mutation simule la corruption
POSTÉRIEURE au scellement).
Usage : python3 harnais_principal_r3.py [--graine G] [--fuzz N] [--fuzz-cli N]
"""

from __future__ import annotations

import argparse
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
M4_DIR = os.path.join(ICI, os.pardir, "m4")
sys.path.insert(0, ICI)
sys.path.insert(0, M4_DIR)
sys.path.insert(0, os.path.join(M4_DIR, "outils"))
sys.path.insert(0, os.path.join(ICI, "outils"))

import layout as L4  # noqa: E402  — m4/layout.py (m4 AVANT m5 sur le chemin)

import importlib.util  # noqa: E402
_spec5 = importlib.util.spec_from_file_location(
    "layout_m5", os.path.join(ICI, "layout.py"))
L5 = importlib.util.module_from_spec(_spec5)   # le plan M5 (source unique)
_spec5.loader.exec_module(L5)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402
from unicorn import UC_HOOK_CODE  # noqa: E402

# --- Géométrie de l'image d'émulation (RVA = adresses unicorn) --------------------

RVA_R1, SLOT_R1 = 0x1800, 0x480           # http-12:R1 (scellé 0.4.0, R7)
RVA_R2, SLOT_R2 = next((r, s) for b, _, r, s, _, _ in
                       L4.BLOCS_TLS + L4.BLOCS_REVISIONS if b == "g70011")
RVA_R3, SLOT_R3 = next((r, s) for b, _n, r, s, _v, _e in
                       L5.BLOCS_REVISIONS_M5 if b == "g80003")   # 0x8C80 x 0x340
BASE_MEM, TAILLE_MEM = 0x1000, 0xA000     # image + shims + ligne de commande
ZONE_PILE, TAILLE_PILE = 0x7F000000, 0x10000
RSP = 0x7F008008                          # ≡ 8 mod 16 (P2, convention chargeur)

# Trappes : cinq blocs appelés directement par l'orchestrateur (aux RVA réels)
TRAPPE_WRITE, TRAPPE_TCP_INIT = 0x1040, 0x4000
TRAPPE_TCP_ACCEPT, TRAPPE_TCP_SPAWN = 0x4100, 0x4300
TRAPPE_TCP_JOURNAL = 0x4B00
TRAPPES = (TRAPPE_WRITE, TRAPPE_TCP_INIT, TRAPPE_TCP_ACCEPT,
           TRAPPE_TCP_SPAWN, TRAPPE_TCP_JOURNAL)
# Trappes IAT (adresses factices posées dans les slots .rdata) — les CINQ
# héritées + GetCommandLineW (IAT M5 propre, layout — R7 : les slots scellés
# ne bougent pas). HORS .text4 : la porte M5 somme la couche SANS le harnais.
SHIM_GCLW, SHIM_GSH, SHIM_EP = 0xA100, 0xA110, 0xA120
SHIM_ICS, SHIM_CH, SHIM_WSAC = 0xA130, 0xA140, 0xA150

CONSOLE = 0x5D80                          # http-11 (thread console)
SESSION_R1, SESSION_R2 = 0x5580, 0x74C0   # http-10:R1/R2 (scellés, R7)
SESSION_R3 = 0x81C0                       # http-10:R3 — LE CÂBLAGE 0.6.0

# La ligne de commande (la pièce de la CLI — hors plages gardées)
CMDLINE_ADDR, CMDLINE_TAILLE = 0xA200, 0x400

# Fixtures héritées (R7 — contenu du harnais, longueurs scellées)
MSG_BANNIERE = b"TRIADE M3 : proxy demarre (port 25000)\r\n"   # 40 o
MSG_ERREUR = b"erreur reseau, arret\r\n"                        # 22 o
MSG_ARRET = b"arret\r\n"                                        # 7 o
MSG_KO = b"TRIADE M3 : integrite KO, arret\r\n"                 # 33 o
# Fixtures M5 (layout.py, source unique)
TXT_CMD_KO = L5.TXT_CMD_KO            # « TRIADE M5 : argument inconnu, arret » 37 o
TXT_POLITIQUE = L5.TXT_POLITIQUE      # « relever-https arme » 20 o
TXT_RELEVER = L5.TXT_CMD_RELEVER      # L"--relever-https" + NUL (32 o)

# Table R10 héritée : 26 entrées squelette + libc-07 + LA PORTE .text3 (D95)
TABLE_SQUELETTE = [
    (0x1040, 0x40), (0x1080, 0x40),                       # io (hello-02/03)
    (0x1100, 0x80), (0x1180, 0x80), (0x1200, 0x80),       # libc
    (0x1280, 0x80), (0x1300, 0x80), (0x1380, 0x80),
    (0x1800, SLOT_R1),                                    # http-12:R1 (lui-même)
    (0x4000, 0x100), (0x4100, 0x40), (0x4140, 0x40),      # tcp
    (0x4180, 0x40), (0x41C0, 0x40), (0x4300, 0x100),
    (0x4400, 0x200), (0x4B00, 0x100),
    (0x4C00, 0x80), (0x4C80, 0x200), (0x4E80, 0xC0),      # http
    (0x4F40, 0x140), (0x5080, 0xC0), (0x5140, 0xC0),
    (0x5200, 0x180), (0x5380, 0x140), (0x54C0, 0xC0),
]
ENTREE_LIBC07 = (0x13C0, 0x80)             # @0x2800 (D94)
ENTREE_TEXT3 = (L4.R10_TEXT3_RVA, L4.R10_TEXT3_TAILLE)  # @0x2810 (D95)
ENTREE_M5 = (L5.TEXT4_RVA, L5.TEXT4_VSIZE)              # @0x2EA0 : (0x8000, 0x2000)

VERSION_R3 = L5.VERSION_U64_DEV1           # 0x00060000 (R10 : monotonie)

DRAPEAU = "--relever-https"

REUSSITES, ECHECS = [], []


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [FAIL] {nom}" + (f" — {detail}" if detail else ""))


def somme_qwords(image: bytearray, rva: int, taille: int) -> int:
    n = taille // 8
    return sum(struct.unpack_from(f"<{n}Q", image, rva)) & 0xFFFFFFFFFFFFFFFF


def cmd(*morceaux: str) -> bytes:
    """Une ligne de commande UTF-16LE + NUL (la pièce vue de GetCommandLineW)."""
    return "".join(morceaux).encode("utf-16-le") + b"\x00\x00"


PROXY_SEUL = cmd("proxy.exe")              # l'état SANS argument (P3 : politique 0)


# --- V1 : assemblage des notations -------------------------------------------------

def lignes_notation(chemin: str) -> list[str]:
    lignes = []
    with open(chemin, encoding="utf-8") as f:
        for brut in f:
            ligne = brut.split(";")[0].strip()
            if ligne:
                lignes.append(ligne)
    return lignes


def assembler_lignes(ks: Ks, lignes: list[str], rva: int) -> bytes:
    sortie, adresse = [], rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise RuntimeError(f"ligne inassemblable à 0x{adresse:x} : {ligne!r}")
        sortie.append(bytes(enc))
        adresse += len(enc)
    return b"".join(sortie)


def octets_notation(ks: Ks, chemin: str, rva: int):
    lignes = lignes_notation(chemin)
    declare = None
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith("; Code : "):
                declare = int(ligne.split("Code : ")[1].split(" o ")[0])
    blob = assembler_lignes(ks, lignes, rva)
    return blob, declare


def octets_mutation(ks: Ks, chemin: str, rva: int, mutation: tuple) -> bytes:
    """Mutation d'un point de la notation RÉSOLUE. Deux formes : (avant,
    apres) — ligne unique contenant `avant` ; (ligne, suivant, old, new) —
    la ligne `ligne` dont la SUIVANTE commence par `suivant` (désambiguïse
    les jumeaux « je 0x8e16 » des trois fins de scan de la CLI)."""
    lignes = lignes_notation(chemin)
    if len(mutation) == 2:
        avant, apres = mutation
        cibles = [i for i, l in enumerate(lignes) if avant in l]
        if len(cibles) != 1:
            raise RuntimeError(f"mutation ambiguë ({len(cibles)}) : {avant!r}")
        lignes[cibles[0]] = lignes[cibles[0]].replace(avant, apres)
    else:
        ligne_cible, suivant, old, new = mutation
        cibles = [i for i, l in enumerate(lignes)
                  if l == ligne_cible and i + 1 < len(lignes)
                  and lignes[i + 1].startswith(suivant)]
        if len(cibles) != 1:
            raise RuntimeError(f"mutation à contexte ambiguë ({len(cibles)}) : "
                               f"{ligne_cible!r} + {suivant!r}")
        lignes[cibles[0]] = lignes[cibles[0]].replace(old, new)
    return assembler_lignes(ks, lignes, rva)


# --- Le modèle de la CLI (écrit depuis la SPÉCIFICATION Q2 — jamais la notation) ---

def parser_cli(ligne: bytes) -> tuple[str, int]:
    """-> (verdict, politique) : « ok » / « inconnu », et l'état .data au
    terme du scan (l'armement PRÉCÈDE le refus — un drapeau sain puis un
    argument inconnu laisse R_POLITIQUE = 1 : l'écriture a eu lieu, le
    processus meurt E4 avant toute initialisation).

    Q2 : l'argument 0 (chemin du programme, entre guillemets ou non) est
    SAUTÉ ; chaque argument suivant est comparé BYTE-EXACT (UTF-16, casse
    SENSIBLE) à L"--relever-https" : égal -> politique = 1 ; TOUT autre
    argument non vide -> refus. Séparateurs : espace et tabulation. Après
    le guillemet fermant (ou un guillemet qui termine un chemin nu), UN
    caractère est sauté — la convention du scan, la même des deux côtés."""
    mots = struct.unpack(f"<{len(ligne) // 2}H", ligne)
    n = len(mots)
    fdrapeau = struct.unpack("<15H", DRAPEAU.encode("utf-16-le"))
    i = 0
    if i < n and mots[i] == 0x22:                       # chemin QUOTÉ
        i += 1
        while i < n and mots[i] not in (0, 0x22):
            i += 1
        if i >= n or mots[i] == 0:                      # fin avant guillemet fermant
            return "ok", 0
        i += 2                                          # guillemet fermant + 1
    else:                                               # chemin NU
        while i < n and mots[i] not in (0, 0x20, 0x09, 0x22):
            i += 1
        if i >= n or mots[i] == 0:
            return "ok", 0
        if mots[i] == 0x22:                             # un guillemet termine arg0 nu
            i += 2
    politique = 0
    while True:
        while i < n and mots[i] in (0x20, 0x09):        # séparateurs
            i += 1
        if i >= n or mots[i] == 0:
            return "ok", politique
        j = i
        while j < n and mots[j] not in (0, 0x20, 0x09):
            j += 1
        if tuple(mots[i:j]) == fdrapeau:
            politique = 1
        else:
            return "inconnu", politique
        i = j


# --- Scénarios ----------------------------------------------------------------------

class Scenario:
    """Script d'exécution : retours des trappes, drapeau quit, ligne de
    commande (la pièce de la CLI), mutations POSTÉRIEURES au scellement de
    la table (corruption simulée). r3_seul : le scénario cible la porte M5 —
    elle n'existe pas dans l'image de l'ancêtre R2 (pas de différentiel)."""

    def __init__(self, tcp01=0x1001, console=0x7000, accepts=(-1,), sessions=None,
                 quit=1, version=None, image_mut=(), table_mut=(), porte_mut=None,
                 r3_seul=False, cmdline=None):
        self.tcp01, self.console, self.accepts = tcp01, console, list(accepts)
        self.sessions = list(sessions) if sessions is not None else \
            [0x7001 + i for i in range(max(0, len(self.accepts)))]
        self.quit, self.version = quit, version
        self.image_mut, self.table_mut = list(image_mut), list(table_mut)
        self.porte_mut = porte_mut
        self.r3_seul = r3_seul
        self.cmdline = cmdline if cmdline is not None else PROXY_SEUL


def scenario(nom, **kw) -> tuple[str, Scenario]:
    return nom, Scenario(**kw)


# --- Image d'émulation + tables (l'artefact PARTAGÉ modèle/émulation) ---------------

def construire_artefact(sc: Scenario, blob_r1: bytes, blob_r2: bytes,
                        blob_r3: bytes):
    """-> (image, table_héritée, porte_m5, version) — l'image fait 0xB000
    (RVA = index) ; les DEUX tables sont scellées sur l'image PUIS les
    mutations s'appliquent. Le remplissage est DÉTERMINISTE POSITION-
    DÉPENDANT (un remplissage uniforme rendait possibles des collisions de
    somme entre plages)."""
    image = bytearray(random.Random(0xC0FFEE).randbytes(BASE_MEM + TAILLE_MEM))
    for rva, slot, blob in ((RVA_R1, SLOT_R1, blob_r1),
                            (RVA_R2, SLOT_R2, blob_r2),
                            (RVA_R3, SLOT_R3, blob_r3)):
        image[rva:rva + len(blob)] = blob
        image[rva + len(blob):rva + slot] = b"\x90" * (slot - len(blob))
    for t in TRAPPES:
        image[t] = 0xC3                                    # ret — crochet
    for rva, texte in ((L5.R_MSG_BANNIERE, MSG_BANNIERE),
                       (L5.R_MSG_ARRET, MSG_ARRET),
                       (L5.R_MSG_ERREUR, MSG_ERREUR),
                       (L5.R_MSG_KO, MSG_KO),
                       (L5.R_TXT_CMD_KO, TXT_CMD_KO),
                       (L5.R_TXT_POLITIQUE, TXT_POLITIQUE),
                       (L5.R_CMD_RELEVER, TXT_RELEVER)):
        image[rva:rva + len(texte)] = texte
    # P3 : l'état .data à l'état image (handles nuls, drapeaux nuls,
    # R_POLITIQUE = 0, section critique NON initialisée)
    image[L5.R_STDOUT:L5.R_CS + 0x40] = b"\x00" * (L5.R_CS + 0x40 - L5.R_STDOUT)
    struct.pack_into("<Q", image, L5.R_QUIT, 1 if sc.quit else 0)
    # IAT fausse (les CINQ slots scellés + l'IAT M5 propre)
    for slot_iat, shim in ((L5.IAT_SLOTS["GetStdHandle"], SHIM_GSH),
                           (L5.IAT_SLOTS["ExitProcess"], SHIM_EP),
                           (L5.IAT_SLOTS["InitializeCriticalSection"], SHIM_ICS),
                           (L5.IAT_SLOTS["CloseHandle"], SHIM_CH),
                           (L5.IAT_SLOTS["WSACleanup"], SHIM_WSAC),
                           (L5.IAT_M5_SLOTS["GetCommandLineW"], SHIM_GCLW)):
        struct.pack_into("<Q", image, slot_iat, shim)
    for s in (SHIM_GCLW, SHIM_GSH, SHIM_EP, SHIM_ICS, SHIM_CH, SHIM_WSAC):
        image[s] = 0xC3
    # la ligne de commande : UTF-16 + remplissage NUL (le scan au-delà de la
    # fin lit des zéros — la convention des deux côtés)
    image[CMDLINE_ADDR:CMDLINE_ADDR + CMDLINE_TAILLE] = b"\x00" * CMDLINE_TAILLE
    image[CMDLINE_ADDR:CMDLINE_ADDR + len(sc.cmdline)] = sc.cmdline
    # les DEUX tables scellées sur l'image COURANTE (jamais deux sources)
    table = [(r, t, somme_qwords(image, r, t)) for r, t in TABLE_SQUELETTE]
    table.append((ENTREE_LIBC07[0], ENTREE_LIBC07[1],
                  somme_qwords(image, *ENTREE_LIBC07)))
    table.append((ENTREE_TEXT3[0], ENTREE_TEXT3[1],
                  somme_qwords(image, *ENTREE_TEXT3)))
    for k, (r, t, s) in enumerate(table):
        struct.pack_into("<IIQ", image, L5.R_TAB_SUM + 16 * k, r, t, s)
    porte = (ENTREE_M5[0], ENTREE_M5[1], somme_qwords(image, *ENTREE_M5))
    struct.pack_into("<IIQ", image, L5.R_TAB_SUM_M5, *porte)
    version = sc.version if sc.version is not None else VERSION_R3
    struct.pack_into("<Q", image, L5.R_VERSION, version)
    # mutations POSTÉRIEURES au scellement — dans l'IMAGE (les octets que la
    # marche lira) ET dans les listes (le modèle)
    for idx, champ, val in sc.table_mut:
        r, t, s = table[idx]
        table[idx] = (val, t, s) if champ == "rva" else \
            ((r, val, s) if champ == "taille" else (r, t, val))
        struct.pack_into("<IIQ", image, L5.R_TAB_SUM + 16 * idx, *table[idx])
    if sc.porte_mut is not None:
        champ, val = sc.porte_mut
        r, t, s = porte
        porte = (val, t, s) if champ == "rva" else \
            ((r, val, s) if champ == "taille" else (r, t, val))
        struct.pack_into("<IIQ", image, L5.R_TAB_SUM_M5, *porte)
    for rva, val in sc.image_mut:
        if image[rva] == val & 0xFF:    # une NON-mutation n'est pas une mutation :
            val = (val ^ 0x5A) & 0xFF   # le fuzz exige un octet retourné EFFECTIF
        image[rva] = val & 0xFF
    return image, table, porte, version


# --- Modèle (écrit depuis la SPÉCIFICATION — jamais la notation) -------------------

def porte_modele(image: bytearray, table: list, porte: tuple, version: int,
                 gen: int) -> bool:
    """Q1/Q1bis — les marches par génération, fail-closed (rva nul / taille
    nulle = KO, somme divergente = KO) ; gen 3 marche la table héritée (28
    entrées PLEINES) PUIS la porte M5 (UNE entrée) ; gen 2 (l'ancêtre scellé)
    ne connaît que la marche héritée — la porte .text4 est la couche de R3.
    Q1ter : le plancher 0x40000 (les deux)."""
    for r, t, s in table:
        if r == 0 or t == 0 or somme_qwords(image, r, t) != s:
            return False
    if gen == 3:
        r, t, s = porte
        if r == 0 or t == 0 or somme_qwords(image, r, t) != s:
            return False
    return version >= 0x00040000


def modele_trace(gen: int, sc: Scenario, image, table, porte, version) -> list[tuple]:
    """La trace attendue. E1 (porte) AVANT tout effet ; gen 3 : la CLI
    (I3 : GetCommandLineW AVANT toute initialisation ; E4 : refus nommé
    ExitProcess 3 sans initialisation) ; Q3 : l'ordre hérité TEL QUEL —
    GSH(-11)/GSH(-10)/InitCS/bannière/[ligne de politique SI armée]/écoute/
    console/boucle ; Q4 : le spawn session sur 0x81C0 (gen 3) ; Q5 : le
    processus meurt toujours par ExitProcess (0/1/2/3)."""
    if not porte_modele(image, table, porte, version, gen):
        return [("GSH", -11), ("write", MSG_KO), ("exit", 1)]
    tr: list[tuple] = []
    politique = 0
    if gen == 3:
        tr.append(("GCLW",))                          # la CLI naît (IAT M5)
        verdict, politique = parser_cli(sc.cmdline)
        if verdict == "inconnu":                      # E4 : refus nommé
            return tr + [("GSH", -11), ("write", TXT_CMD_KO), ("exit", 3)]
    tr += [("GSH", -11), ("GSH", -10), ("InitCS",), ("journal", MSG_BANNIERE)]
    if politique == 1:                                # l'état nommé, UNE fois
        tr.append(("journal", TXT_POLITIQUE))
    cible = SESSION_R3 if gen == 3 else SESSION_R2
    tr.append(("tcp01", sc.tcp01))
    if sc.tcp01 == 0:                                 # E2 : écoute
        return tr + [("journal", MSG_ERREUR), ("exit", 2)]
    tr.append(("spawn", CONSOLE, 0, sc.console))
    if sc.console == 0:                               # E2 : console
        return tr + [("journal", MSG_ERREUR), ("exit", 2)]
    tr.append(("CH", sc.console))
    i_acc, i_sess = 0, 0
    while True:
        if i_acc >= len(sc.accepts):
            raise RuntimeError("scénario inachevé : accepts épuisé sans échec final")
        a = sc.accepts[i_acc]
        i_acc += 1
        tr.append(("accept", sc.tcp01, a))
        if a < 0:                                     # échec signé (tcp-02)
            if sc.quit != 0:                          # Q4 : arrêt demandé
                return tr + [("journal", MSG_ARRET), ("WSACLEANUP",), ("exit", 0)]
            return tr + [("journal", MSG_ERREUR), ("exit", 2)]   # E3
        h = sc.sessions[i_sess] if i_sess < len(sc.sessions) else 0
        i_sess += 1
        tr.append(("spawn", cible, a, h))
        if h == 0:                                    # E2 : lancement de session
            return tr + [("journal", MSG_ERREUR), ("exit", 2)]
        tr.append(("CH", h))


# --- Émulation (unicorn, octets réels + trappes crochetées) ------------------------

def _regs():
    from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,
                                   UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                                   UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                                   UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                                   UC_X86_REG_R15, UC_X86_REG_RIP)
    return {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
            "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
            "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
            "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
            "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
            "r15": UC_X86_REG_R15, "rip": UC_X86_REG_RIP}


_REGS = _regs()
SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}


class Emulateur:
    def __init__(self, image: bytearray, sc: Scenario):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.uc.mem_map(BASE_MEM, TAILLE_MEM)
        self.uc.mem_map(ZONE_PILE, TAILLE_PILE)
        self.uc.mem_write(BASE_MEM, bytes(image[BASE_MEM:]))
        self.sc = sc
        self.trace: list[tuple] = []
        self.i_acc, self.i_sess = 0, 0
        self.arret = False
        for adresse in (SHIM_GCLW, SHIM_GSH, SHIM_EP, SHIM_ICS, SHIM_CH,
                        SHIM_WSAC, TRAPPE_WRITE, TRAPPE_TCP_INIT,
                        TRAPPE_TCP_ACCEPT, TRAPPE_TCP_SPAWN, TRAPPE_TCP_JOURNAL):
            self.uc.hook_add(UC_HOOK_CODE, self._crochet, begin=adresse, end=adresse)

    # -- la sémantique des trappes (le modèle d'exécution du harnais) ---------------
    def _crochet(self, uc, adresse, taille_instruction, user_data):
        r = lambda n: uc.reg_read(_REGS[n])
        w = lambda n, v: uc.reg_write(_REGS[n], v)
        if adresse == SHIM_GCLW:                       # LA CLI naît (IAT M5)
            self.trace.append(("GCLW",))
            w("rax", CMDLINE_ADDR)
        elif adresse == SHIM_GSH:
            arg = r("rcx") & 0xFFFFFFFF          # mov ecx, -11 : zero-étendu en 64
            if arg & 0x80000000:
                arg -= 1 << 32
            self.trace.append(("GSH", arg))
            w("rax", 0xF00D0011 if arg == -11 else 0xF00D0010)
        elif adresse == SHIM_ICS:
            self.trace.append(("InitCS",))
        elif adresse == SHIM_EP:
            self.trace.append(("exit", r("rcx") & 0xFFFFFFFF))
            self.arret = True
            uc.emu_stop()
        elif adresse == SHIM_CH:
            self.trace.append(("CH", r("rcx")))
            w("rax", 1)
        elif adresse == SHIM_WSAC:
            self.trace.append(("WSACLEANUP",))
            w("rax", 0)
        elif adresse == TRAPPE_TCP_INIT:
            w("rax", self.sc.tcp01 & 0xFFFFFFFFFFFFFFFF)
            self.trace.append(("tcp01", self.sc.tcp01))
        elif adresse == TRAPPE_TCP_ACCEPT:
            if self.i_acc >= len(self.sc.accepts):
                raise RuntimeError("accepts épuisé — scénario inachevé")
            a = self.sc.accepts[self.i_acc]
            self.i_acc += 1
            w("rax", a & 0xFFFFFFFFFFFFFFFF)
            self.trace.append(("accept", r("rcx"), a))
        elif adresse == TRAPPE_TCP_SPAWN:
            fn, arg = r("rcx"), r("rdx")
            if fn == CONSOLE:
                h = self.sc.console
            else:
                h = self.sc.sessions[self.i_sess] if self.i_sess < len(self.sc.sessions) else 0
                self.i_sess += 1
            w("rax", h & 0xFFFFFFFFFFFFFFFF)
            self.trace.append(("spawn", fn, arg, h))
        elif adresse == TRAPPE_TCP_JOURNAL:
            n = r("rdx")
            self.trace.append(("journal", bytes(uc.mem_read(r("rcx"), n))))
            w("rax", n)
        elif adresse == TRAPPE_WRITE:
            n = r("r8")
            self.trace.append(("write", bytes(uc.mem_read(r("rdx"), n))))
            w("rax", n)

    def executer(self, entree: int) -> tuple[str, list[tuple]]:
        for nom, valeur in SENTINELLES_NV.items():
            self.uc.reg_write(_REGS[nom], valeur)
        self.uc.reg_write(_REGS["rsp"], RSP)
        try:
            self.uc.emu_start(entree, BASE_MEM + TAILLE_MEM - 0x10,
                              timeout=5_000_000, count=1_000_000)
        except Exception as exc:
            return ("CRASH:" + repr(exc)[:48], self.trace)
        if not self.arret:
            return ("SANS_EXIT", self.trace)
        # NOTE : pas de vérification de non-volatils — Q5 : le bloc ne
        # revient JAMAIS (ExitProcess terminal, miroir de l'ancêtre scellé).
        return ("OK", self.trace)

    def politique_lue(self) -> int:
        return struct.unpack("<Q", bytes(
            self.uc.mem_read(L5.R_POLITIQUE, 8)))[0]


def executer_generation(gen: int, sc: Scenario, blob_r1: bytes,
                        blob_r2: bytes, blob_r3: bytes):
    """-> (statut, trace, modele, politique_lue) — l'artefact est construit
    UNE fois et lu par le modèle ET l'émulation (jamais deux sources)."""
    image, table, porte, version = construire_artefact(sc, blob_r1, blob_r2, blob_r3)
    attendu = modele_trace(gen, sc, image, table, porte, version)
    emu = Emulateur(image, sc)
    statut, trace = emu.executer(RVA_R3 if gen == 3 else RVA_R2)
    return statut, trace, attendu, emu.politique_lue()


def normaliser(trace: list[tuple], gen: int) -> list[tuple]:
    """La cible du spawn session EST la divergence légitime du câblage et
    l'appel GetCommandLineW EST le domaine nouveau — pour la comparaison
    croisée R2/R3, l'un est ramené à l'ancêtre, l'autre retiré."""
    if gen != 3:
        return trace
    out = []
    for t in trace:
        if t and t[0] == "GCLW":
            continue
        if t and t[0] == "spawn" and t[1] == SESSION_R3:
            t = ("spawn", SESSION_R2) + t[2:]
        out.append(t)
    return out


# --- V2 : différentiel d'ancêtre (SANS argument) ------------------------------------

def cas_v2() -> list[tuple[str, Scenario]]:
    s = scenario
    return [
        s("nominal : 3 accepts puis arrêt demandé",
          accepts=(0x3001, 0x3002, 0x3003, -1)),
        s("zéro accept : arrêt immédiat demandé", accepts=(-1,)),
        s("E3 : échec d'acceptation SANS arrêt demandé (fail-closed dispo)",
          accepts=(-1,), quit=0),
        s("E2 : échec d'écoute", tcp01=0, accepts=(-1,), quit=1),
        s("E2 : échec du thread console", console=0, accepts=(-1,), quit=1),
        s("E2 : échec du lancement de session", accepts=(0x3001,),
          sessions=[0], quit=1),
        s("porte : octet squelette corrompu (libc @0x1100 — les DEUX)",
          accepts=(-1,), quit=1, image_mut=[(0x1100, 0x33)]),
        s("porte : octet .text3 corrompu (@0x6500 — la porte héritée)",
          accepts=(-1,), quit=1, image_mut=[(0x6503, 0x55)]),
        s("porte : octet .text4 corrompu (@0x8700 — LA NOUVELLE PORTE M5)",
          accepts=(-1,), quit=1, image_mut=[(0x8700, 0x55)]),
        s("porte : version sous plancher (0x30000)",
          accepts=(-1,), quit=1, version=0x30000),
        s("porte : entrée #5 de somme corrompue (les DEUX générations)",
          accepts=(-1,), quit=1, table_mut=[(4, "somme", 0xDEADBEEF)]),
        s("porte M5 : entrée trouée (rva nul — fail-closed D136)",
          accepts=(-1,), quit=1, porte_mut=("rva", 0), r3_seul=True),
        s("porte M5 : entrée de taille nulle (fail-closed)",
          accepts=(-1,), quit=1, porte_mut=("taille", 0), r3_seul=True),
        s("porte M5 : somme corrompue (la couche .text4 non gardée)",
          accepts=(-1,), quit=1, porte_mut=("somme", 0xDEADBEEF), r3_seul=True),
    ]


def differentiel_v2(blob_r1: bytes, blob_r2: bytes, blob_r3: bytes) -> int:
    ecarts = 0
    for nom, sc in cas_v2():
        if sc.r3_seul:
            # la porte M5 n'existe qu'en génération 3 — pas d'ancêtre à
            # comparer (la porte .text4 est la NOUVELLE couche de R3)
            s3, t3, m3, _ = executer_generation(3, sc, blob_r1, blob_r2, blob_r3)
            if not (s3 == "OK" and t3 == m3
                    and m3 == [("GSH", -11), ("write", MSG_KO), ("exit", 1)]):
                ecarts += 1
                print(f"    écart [{nom}] : R3 {s3}, trace {t3[:3]}")
            continue
        s2, t2, m2, _ = executer_generation(2, sc, blob_r1, blob_r2, blob_r3)
        s3, t3, m3, _ = executer_generation(3, sc, blob_r1, blob_r2, blob_r3)
        ok2, ok3 = s2 == "OK" and t2 == m2, s3 == "OK" and t3 == m3
        # la corruption .text4 : R2 ne la garde pas (sa porte est la table
        # M3/M4) — la divergence est LÉGITIME et nommée : R2 nominal, R3 KO
        legit = ".text4 corrompu" in nom
        if legit:
            croisee = (ok2 and
                       m3 == [("GSH", -11), ("write", MSG_KO), ("exit", 1)]
                       and len([e for e in t2 if e[0] in ("tcp01", "accept")]) > 0)
        else:
            croisee = normaliser(t3, 3) == t2
        if not (ok2 and ok3 and croisee):
            ecarts += 1
            print(f"    écart [{nom}] : R2 {s2}/{ok2} R3 {s3}/{ok3} croisée {croisee}")
            if t2 != m2:
                print(f"      R2 trace {t2[:6]} != modèle {m2[:6]}")
            if t3 != m3:
                print(f"      R3 trace {t3[:6]} != modèle {m3[:6]}")
    return ecarts


# --- V2bis : la CLI (domaine NOUVEAU — le modèle juge, sans ancêtre) ----------------

def cas_cli() -> list[tuple[str, bytes, str, int]]:
    """(nom, ligne, verdict attendu, politique attendue) — l'intention de
    chaque cas est ASSERTÉE contre parser_cli : le modèle s'accorde avec la
    spécification AVANT que l'émulation soit jugée (jamais d'écarts muets)."""
    return [
        ("chemin quoté + drapeau — la politique armée, la ligne nommée",
         cmd('"C:\\projets\\proxy.exe" --relever-https'), "ok", 1),
        ("chemin nu + drapeau", cmd("proxy.exe --relever-https"), "ok", 1),
        ("chemin nu SEUL — la politique absente (P3)", cmd("proxy.exe"), "ok", 0),
        ("chemin quoté SEUL", cmd('"proxy.exe"'), "ok", 0),
        ("chemin nu avec espace NON quoté — le second mot est un argument inconnu",
         cmd("mon proxy.exe"), "inconnu", 0),
        ("double drapeau — chaque égal arme (I6 : lu UNE fois, pas d'état caché)",
         cmd("proxy.exe --relever-https --relever-https"), "ok", 1),
        ("séparateurs mêlés espaces/tabulations",
         cmd("proxy.exe \t --relever-https"), "ok", 1),
        ("tabulation terminale après le drapeau",
         cmd("proxy.exe --relever-https\t"), "ok", 1),
        ("séparateurs terminaux nus — rien à nommer",
         cmd("proxy.exe   "), "ok", 0),
        ("casse mixte --RELEVER-HTTPS — refus (la casse est SENSIBLE)",
         cmd("proxy.exe --RELEVER-HTTPS"), "inconnu", 0),
        ("casse mixte --Relever-Https", cmd("proxy.exe --Relever-Https"),
         "inconnu", 0),
        ("tronqué --relever-http", cmd("proxy.exe --relever-http"), "inconnu", 0),
        ("suffixe --relever-httpsX", cmd("proxy.exe --relever-httpsX"),
         "inconnu", 0),
        ("préfixe x--relever-https", cmd("proxy.exe x--relever-https"),
         "inconnu", 0),
        ("argument inconnu nu", cmd("proxy.exe --inconnu"), "inconnu", 0),
        ("drapeau PUIS inconnu — le refus vient quand même (E4), l'état .data "
         "porte l'armement déjà écrit",
         cmd("proxy.exe --relever-https --inconnu"), "inconnu", 1),
        ("inconnu PUIS drapeau — le refus précède",
         cmd("proxy.exe --inconnu --relever-https"), "inconnu", 0),
        ("drapeau QUOTÉ — les guillemets ne sont pas byte-exact",
         cmd('proxy.exe "--relever-https"'), "inconnu", 0),
        ("ligne vide", cmd(""), "ok", 0),
    ]


def jouer_cli(cas: list[tuple[str, bytes, str, int]], blob_r1, blob_r2,
              blob_r3, etiquette: str) -> int:
    ecarts = 0
    for nom, ligne, v_att, p_att in cas:
        v_m, p_m = parser_cli(ligne)
        if (v_m, p_m) != (v_att, p_att):
            controle(f"{etiquette} « {nom} » : le modèle s'accorde avec "
                     f"l'intention", False,
                     f"modèle ({v_m}, {p_m}) != intention ({v_att}, {p_att})")
            ecarts += 1
            continue
        sc = Scenario(accepts=(-1,), quit=1, cmdline=ligne)
        s3, t3, m3, pol = executer_generation(3, sc, blob_r1, blob_r2, blob_r3)
        ok = s3 == "OK" and t3 == m3 and pol == p_att
        detail = (f"exit {t3[-1][1] if t3 and t3[-1][0] == 'exit' else '?'}"
                  f"·politique .data {pol}")
        controle(f"{etiquette} « {nom} »", ok,
                 detail if ok else f"{s3}, trace {t3[:4]} != modèle {m3[:4]}, "
                 f"politique {pol} != {p_att}")
        if not ok:
            ecarts += 1
    return ecarts


# --- V3 : fuzz (la porte ET la CLI — modèle contre octets) --------------------------

def _plages_gardees() -> list[tuple[int, int]]:
    return TABLE_SQUELETTE + [ENTREE_LIBC07, ENTREE_TEXT3, ENTREE_M5]


def cas_fuzz_porte(alea: random.Random, n: int) -> list[tuple[str, Scenario]]:
    """Une mutation D'UN point par cas : champ des DEUX tables OU octet
    gardé ; les octets mutés évitent le code de R3 (0x8C80-0x8FBF) et les
    trappes — la corruption du VÉRIFICATEUR n'est pas décidable par
    lui-même (miroir M3) ; le code mort des ancêtres (@0x1800, @0x7DC0) est
    GARDABLE — mutation licite."""
    cas = []
    plages = _plages_gardees()
    exclus = set(TRAPPES) | set(range(RVA_R3, RVA_R3 + SLOT_R3)) | \
        {SHIM_GCLW, SHIM_GSH, SHIM_EP, SHIM_ICS, SHIM_CH, SHIM_WSAC}
    for i in range(n):
        sc = Scenario(accepts=(-1,), quit=1)
        r = alea.random()
        if r < 0.35:                              # champ de la table héritée
            idx = alea.randrange(L4.R10_NB_ENTREES)
            champ = alea.choice(("rva", "taille", "somme"))
            original = (TABLE_SQUELETTE + [ENTREE_LIBC07, ENTREE_TEXT3])[idx]
            if champ == "rva":
                val = alea.choice((0, alea.randrange(0x1000, 0x9000)))
                while val == original[0]:         # jamais de mutation sans effet
                    val = alea.randrange(0x1000, 0x9000)
            elif champ == "taille":
                val = alea.choice((0, alea.randrange(1, 0x2001)))
                while val == original[1]:
                    val = alea.randrange(1, 0x2001) if val else 0
            else:
                val = alea.randrange(1 << 64)
            sc.table_mut = [(idx, champ, val)]
            cas.append((f"fuzz-porte héritage champ {champ} entrée #{idx}", sc))
        elif r < 0.70:                            # champ de la porte M5
            champ = alea.choice(("rva", "taille", "somme"))
            if champ == "rva":
                val = alea.choice((0, alea.randrange(0x1000, 0x9000)))
                while val == ENTREE_M5[0]:
                    val = alea.randrange(0x1000, 0x9000)
            elif champ == "taille":
                val = alea.choice((0, alea.randrange(1, 0x2001)))
                while val == ENTREE_M5[1]:
                    val = alea.randrange(1, 0x2001) if val else 0
            else:
                val = alea.randrange(1 << 64)
            sc.porte_mut = (champ, val)
            cas.append((f"fuzz-porte M5 champ {champ}", sc))
        else:                                     # octet dans une plage gardée
            while True:
                rva, t = plages[alea.randrange(len(plages))]
                rva_b = rva + alea.randrange(t)
                if rva_b not in exclus:           # (les ancêtres sont MORTS en
                    break                         # génération 3 : plages gardables)
            sc.image_mut = [(rva_b, alea.randrange(256))]
            cas.append((f"fuzz-porte octet @{rva_b:#x}", sc))
    return cas


def fuzz_porte(blob_r1: bytes, blob_r2: bytes, blob_r3: bytes,
               alea: random.Random, n: int) -> tuple[int, int]:
    ecarts, silencieux = 0, 0
    for nom, sc in cas_fuzz_porte(alea, n):
        image, table, porte, version = construire_artefact(sc, blob_r1, blob_r2,
                                                           blob_r3)
        attendu = modele_trace(3, sc, image, table, porte, version)
        emu = Emulateur(image, sc)
        statut, trace = emu.executer(RVA_R3)
        if statut != "OK" or trace != attendu:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart fuzz [{nom}] : {statut}, trace {trace[:3]}")
        if attendu != [("GSH", -11), ("write", MSG_KO), ("exit", 1)]:
            silencieux += 1                       # mutation passée SANS KO
    return ecarts, silencieux


def cas_fuzz_cli(alea: random.Random, n: int) -> list[tuple[str, bytes, str, int]]:
    """La CLI hostile : quasi-drapeaux (casse, troncature, substitution,
    insertion — JAMAIS l'égalité byte-exact), drapeaux sains aux séparateurs
    et chemins variés, bruit d'arguments. Le générateur ne peut PAS produire
    l'égalité par accident : le retournement de casse ne vise que les
    LETTRES (les traits d'union @0/1/9 n'ont pas de casse — une mutation
    sans effet y serait une non-mutation, attrapée par l'assertion
    d'intention), l'alphabet de substitution est disjoint du drapeau, toute
    troncature est plus courte, toute insertion rallonge."""
    cas = []
    for _ in range(n):
        r = alea.random()
        if r < 0.45:                              # quasi-drapeau → refus nommé
            s = list(DRAPEAU)
            k = alea.randrange(4)
            if k == 0:                            # casse (les LETTRES seules —
                lettres = [i for i in range(2, len(s)) if s[i].islower()]
                j = alea.choice(lettres)          # les « - » @0/1/9 n'en ont
                s[j] = s[j].upper()               # pas : mutation EFFECTIVE
            elif k == 1:                          # troncature
                s = s[:alea.randrange(2, len(s))]
            elif k == 2:                          # substitution
                j = alea.randrange(2, len(s))
                s[j] = alea.choice("xyzXYZ0_.")
            else:                                 # insertion
                j = alea.randrange(2, len(s))
                s.insert(j, alea.choice("x-0"))
            arg = "".join(s)
            sep = alea.choice((" ", "\t", "  ", " \t "))
            cas.append((f"quasi-drapeau « {arg} »",
                        cmd("proxy.exe" + sep + arg), "inconnu", 0))
        elif r < 0.80:                            # drapeau sain → armement
            chemin = alea.choice(("proxy.exe", '"C:\\proxy.exe"',
                                  '"mon proxy.exe"', '"chemin\\avec espace.exe"'))
            sep1 = alea.choice((" ", "\t", "  ", "\t \t"))
            fin = alea.choice(("", " ", "\t", "  "))
            cas.append((f"drapeau sain {chemin!r}",
                        cmd(chemin + sep1 + DRAPEAU + fin), "ok", 1))
        else:                                     # bruit → refus nommé
            args = ["".join(alea.choice("aZ0-_.") for _ in range(alea.randint(1, 12)))
                    for _ in range(alea.randint(1, 3))]
            cas.append((f"bruit « {' '.join(args)} »",
                        cmd("proxy.exe " + " ".join(args)), "inconnu", 0))
    return cas


# --- V4 : falsification (mutations stables en taille, leçon D82) -------------------

def falsifier(ks: Ks, chemin_r3: str, blob_r1: bytes, blob_r2: bytes,
              blob_r3: bytes) -> int:
    exposition_nominal = scenario("exposition", accepts=(0x3001, 0x3002, -1))
    exposition_armee = scenario("exposition-armée", accepts=(-1,),
                                cmdline=cmd("proxy.exe --relever-https"))
    mutations = [
        (("lea rcx, [rip - 0xd1f]", "lea rcx, [rip - 0x1a1f]"),
         "LE CONTRE-CÂBLAGE : la boucle lance http-10:R2 (0x74C0) — I1 nominal",
         exposition_nominal),
        (("lea rcx, [rip - 0xd1f]", "lea rcx, [rip - 0x395f]"),
         "le contre-câblage à l'ancêtre http-10:R1 (0x5580)",
         exposition_nominal),
        (("lea r15, [rip - 0x5e59]", "lea r15, [rip - 0x5e69]"),
         "la borne M5 remonte à 0x2EA0 : l'entrée .text4 est SAUTÉE — la "
         "porte ne garde plus la couche M5 (la marche boucle)",
         exposition_nominal),
        (("lea r15, [rip - 0x5e59]", "lea r15, [rip - 0x5e49]"),
         "la borne M5 descend à 0x2EC0 : le remplissage est lu comme une "
         "entrée (fail-closed ou faute — jamais un passage silencieux)",
         exposition_nominal),
        (("cmp rax, 0x40000", "cmp rax, 0x30000"),
         "le plancher anti-rollback abaissé — la version 0x30000 passe",
         scenario("exposition", accepts=(-1,), quit=1, version=0x30000)),
        (("cmp qword ptr [rip - 0x5612], 1", "cmp qword ptr [rip - 0x5612], 0"),
         "la ligne de politique amnésiée (l'état nommé jamais émis — Q3)",
         exposition_armee),
        (("mov qword ptr [rip - 0x55a4], 1", "mov qword ptr [rip - 0x55a4], 0"),
         "la politique jamais armée (le drapeau lu, l'état jamais écrit)",
         exposition_armee),
        (("jne 0x8e97", "je 0x8e97"),
         "l'ordre d'initialisation : la ligne de politique dans le mauvais "
         "état (armée → muette, absente → nommée)",
         exposition_armee),
        (("je 0x8e16", "cmp word ptr [r12], 0x20", "0x8e16", "0x8df9"),
         "la politique armée SANS argument (la fin de scan déviée vers "
         "l'armement — le processus démarre armé en silence)",
         scenario("exposition-sans-argument", accepts=(-1,), quit=1)),
        (("jne 0x8dce", "je 0x8dce"),
         "l'argument inconnu accepté en silence (le sens du test de "
         "comparaison — « foo » armerait)",
         scenario("exposition-bruit", accepts=(-1,), quit=1,
                  cmdline=cmd("proxy.exe foo"))),
        (("mov ecx, 3", "mov ecx, 0"),
         "le code de sortie E4 dévié (3 -> 0 : le refus meurt « nominal »)",
         scenario("exposition-inconnu", accepts=(-1,), quit=1,
                  cmdline=cmd("proxy.exe --inconnu"))),
    ]
    non_attrapees = 0
    exposes = []
    for mutation, desc, (_nom_sc, sc) in mutations:
        blob_m = octets_mutation(ks, chemin_r3, RVA_R3, mutation)
        s_m, t_m, m_m, _ = executer_generation(3, sc, blob_r1, blob_r2, blob_m)
        attrapee = not (s_m == "OK" and t_m == m_m)
        controle(f"V4 {desc} : ATTRAPÉE", attrapee,
                 f"{s_m}, trace {t_m[:4]}" if not attrapee else "")
        if not attrapee:
            non_attrapees += 1
        exposes.append(sc)
    # témoin : la notation INTACTE reste verte sur les MÊMES scénarios
    temoin_ok = True
    for sc in exposes:
        s_t, t_t, m_t, _ = executer_generation(3, sc, blob_r1, blob_r2, blob_r3)
        if not (s_t == "OK" and t_t == m_t):
            temoin_ok = False
    controle(f"V4 témoin (notation intacte, {len(exposes)} scénarios "
             f"d'exposition) : VERT", temoin_ok)
    return non_attrapees


# --- Main ---------------------------------------------------------------------------

def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261103)
    parseur.add_argument("--fuzz", type=int, default=400)
    parseur.add_argument("--fuzz-cli", type=int, default=300)
    args = parseur.parse_args()
    alea = random.Random(args.graine)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    chemin_r3 = os.path.join(ICI, "notation", "http-12-principal-r3.asm")
    chemin_r2 = os.path.join(M4_DIR, "notation", "http-12-principal-r2.asm")
    chemin_r1 = os.path.join(ICI, os.pardir, "m3", "notation",
                             "http-12-principal.asm")

    print("=== harnais_principal_r3.py — révision http-12:R3 (LA CLI et la "
          f"porte M5, 0.6.0), graine {args.graine} ===")

    print("\n--- V1 : round-trip de notation (R3 + les DEUX ancêtres) ---")
    blob_r3, declare_r3 = octets_notation(ks, chemin_r3, RVA_R3)
    controle(f"V1 http-12:R3 : assemblage intégral ({len(blob_r3)} o == "
             f"« Code : {declare_r3} o » déclarés)", len(blob_r3) == declare_r3)
    passe2 = assembler_lignes(ks, lignes_notation(chemin_r3), RVA_R3)
    controle("V1 http-12:R3 : idempotence (2e passe octet-identique)",
             passe2 == blob_r3)
    blob_r2, declare_r2 = octets_notation(ks, chemin_r2, RVA_R2)
    controle(f"V1 http-12:R2 (ancêtre scellé 0.5.1) : assemblage à 0x{RVA_R2:x} "
             f"({len(blob_r2)} o == « Code : {declare_r2} o » déclarés)",
             len(blob_r2) == declare_r2)
    blob_r1, declare_r1 = octets_notation(ks, chemin_r1, RVA_R1)
    controle(f"V1 http-12:R1 (ancêtre scellé 0.4.0) : assemblage à 0x{RVA_R1:x} "
             f"({len(blob_r1)} o == « Code : {declare_r1} o » déclarés)",
             len(blob_r1) == declare_r1)

    print("\n--- V2 : différentiel d'ancêtre (14 scénarios SANS argument, R2 "
          "émulé contre R3 émulé — traces identiques sauf LE CÂBLAGE "
          "0x74C0 -> 0x81C0 ; divergence .text4 nommée ; portes M5 "
          "fail-closed) ---")
    e_v2 = differentiel_v2(blob_r1, blob_r2, blob_r3)
    controle("V2 14 scénarios : R2 == modèle R2 ET R3 == modèle R3 ET traces "
             "croisées identiques (spawn 0x81C0 + GCLW normalisés ; "
             "corruption .text4 : R2 nominal, R3 KO — la divergence "
             "légitime), ordre Q3 constaté, la CLI précède toute "
             "initialisation (I3)", e_v2 == 0, f"{e_v2} écarts")

    print("\n--- V2bis : la CLI (19 cas dirigés, domaine SANS ancêtre — le "
          "modèle de la spécification juge les OCTETS) ---")
    e_cli = jouer_cli(cas_cli(), blob_r1, blob_r2, blob_r3, "CLI")
    controle("V2bis 19 cas CLI : drapeau sain → politique armée + ligne "
             "« relever-https arme » ; TOUT autre argument → refus nommé "
             "ExitProcess 3 SANS initialisation ; l'état .data conforme au "
             "scan (l'armement précède le refus)", e_cli == 0,
             f"{e_cli} écarts")

    print(f"\n--- V3 : fuzz de la porte ({args.fuzz} mutations d'un point : "
          "les DEUX tables + octets gardés) ---")
    e_v3, silencieux = fuzz_porte(blob_r1, blob_r2, blob_r3, alea, args.fuzz)
    controle(f"V3 {args.fuzz} mutations de porte : le modèle et les octets "
             f"nomment le MÊME verdict, ZÉRO passage silencieux",
             e_v3 == 0 and silencieux == 0, f"{e_v3} écarts, {silencieux} silencieux")

    print(f"\n--- V3bis : fuzz de la CLI ({args.fuzz_cli} lignes hostiles) ---")
    e_fcli = jouer_cli(cas_fuzz_cli(alea, args.fuzz_cli), blob_r1, blob_r2,
                       blob_r3, "fuzz-CLI")
    controle(f"V3bis {args.fuzz_cli} lignes : toute casse/troncature/"
             f"substitution/insertion du drapeau est un REFUS NOMMÉ, jamais "
             f"un armement ; les drapeaux sains arment aux séparateurs "
             f"variés", e_fcli == 0, f"{e_fcli} écarts")

    print("\n--- V4 : falsification (une suite qui ne peut pas échouer "
          "ne prouve rien) ---")
    non_attrapees = falsifier(ks, chemin_r3, blob_r1, blob_r2, blob_r3)

    print("\n" + "=" * 78)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC "
          f"(graine {args.graine}, {args.fuzz} mutations de porte, "
          f"{args.fuzz_cli} lignes CLI)")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    if not ECHECS:
        print("La révision http-12:R3 tient son contrat : notation round-trip")
        print("100 % (les deux ancêtres assemblés à leurs RVA), l'héritage R2")
        print("est reproduit trace à trace (l'unique différence : la cible du")
        print("spawn session 0x81C0 — LE CÂBLAGE 0.6.0), la porte M5 marche")
        print("aux bornes sur UNE entrée fail-closed (.text4 entière gardée,")
        print("la porte se garde elle-même), la CLI naît (--relever-https")
        print("arme et est nommée, tout argument inconnu est un refus")
        print("ExitProcess 3 avant toute initialisation) et la suite est")
        print("falsifiable (11/11 attrapées, témoin vert).")
    print("=" * 78)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
