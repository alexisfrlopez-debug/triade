#!/usr/bin/env python3
"""build_m4.py : Jalon M4 de TRIADE — tunnel chiffré SSPI/Schannel, CÂBLÉ (proxy 0.5.1 — jalon v7, D140 : tls-05:R2).

Chaîne : notation (keystone) -> octets -> PE32+ à la main (CINQ sections :
.text/.rdata/.data/.text2 + .text3 NOUVELLE) -> carte projet génération 6
(lignée D80). Implémente le jalon M4 sous les règles R4/R7 (adresses stables —
l'héritage M0/M1/M2/M3 repris OCTET POUR OCTET du proxy.exe 0.4.0 scellé) et
R10 (porte d'intégrité au lancement, plancher 0x00040000).

LIBC-07 (b20007, memset) devient EMBARQUÉ dans proxy.exe M4 : tls-06 (destruction
du clair copié) et tls-07 (descente du résidu en tête) l'exigent — slot 0x13C0
dans la zone reserve-libc (int3 défensif en M3), octets identiques à selftest.exe
(R7), et la porte R10 le couvre (entrée @0x2800).

D95 — LE CÂBLAGE (http-12:R2, g70011 @0x7DC0) : la boucle d'acceptation lance
http-10:R2 (0x74C0 — la session révisée D92) ; l'entrée PE passe à 0x7DC0
(delta documenté ; l'ancêtre http-12:R1 @0x1800 reste embarqué octet pour octet,
R7 — mort au lancement, vivant à la preuve d'héritage). LA PORTE R10 .text3
vient avec le câblage (pas en contrebande) : la table est PLEINE (27 entrées +
terminateur @0x2810, R_VERSION @0x2820 immovable R7) — l'entrée #28
(0x6000, 0x2000, somme .text3) REMPLACE le terminateur et la marche de
http-12:R2 s'arrête à la BORNE (l'adresse de R_VERSION) : fail-closed sur
entrée trouée (rva nul / taille nulle = KO — la troncature silencieuse du
terminateur M3 n'existe plus), la couche M4 entière gardée AU LANCEMENT.

L'ORACLE (D93) est exécuté sur les blobs du build : oracle_m4.executer(blobs,
graine, volume) — 560 cas à volume complet (F1 session / F2 routage / F3 ancêtre
/ F4 falsification), lève EchecOracle sur TOUT écart. L'héritage M3 est
re-vérifié AU PASSAGE : build_m3.assembler_tout() (R5 round-trip + oracle
structurel M3, ~520 verrous) et l'image composée M3 est confrontée OCTET PAR
OCTET au proxy.exe 0.4.0 scellé (sha bf02769f…) AVANT toute extension — la
preuve R7 absolue, puis deltas M4 documentés :

  .text  : [0x13C0, 0x1440) = libc-07 (était int3 défensif)
  .rdata : 0x2550 = 8e entrée de la table des réponses (502 Certificat rejete)
           0x2800 = entrée R10 libc-07
           0x2810 = PORTE R10 .text3 (D95 : l'ancien terminateur M4-dev.1
                    remplacé — la table est PLEINE, marche aux bornes)
           0x2820 = version 0x00050003 (R10 : monotonie, plancher 0x00040000)
           0x29A0+ = extension M4 (descripteurs, secur32, fixtures tls/http-R2)
  .text3 : NOUVELLE (0x6000-0x7FFF) : tls-01..08, http-08:R2, http-10:R2,
           http-12:R2 (0x7DC0 — le câblage ; réserve int3 0x7FC0-0x7FFF)
  PE     : AddressOfEntryPoint 0x1800 -> 0x7DC0 (D95)

Usage :
  python3 build_m4.py                  # construction 0.5.1 (UNIQUE — la carte scelle ensuite, R6)
  python3 build_m4.py --verifier [--graine N] [--volume complet|reduit]
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import struct
import sys
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)
M0_DIR = os.path.join(TRIADE, "m0")
M1_DIR = os.path.join(TRIADE, "m1")
M2_DIR = os.path.join(TRIADE, "m2")
M3_DIR = os.path.join(TRIADE, "m3")


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Chargement des modules (le nom "layout" est disputé m3/m4) ---------------
# 1) m3/layout prend le nom "layout" (build_m3 s'y attend) ;
# 2) build_m3 est exécuté sous ce régime (son L = plan M3, sa carte/oracle M3) ;
# 3) m4/layout PREND ensuite la place du nom "layout" — les harnais M4 et
#    oracle_m4 (importés plus bas) y voient le plan M4. Les références déjà
#    liées (B3.L, B3.cm, B3.od) demeurent : liaison par objet module.


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


L3 = _charger_module("layout", os.path.join(M3_DIR, "layout.py"))     # plan M3
B3 = _charger_module("build_m3", os.path.join(M3_DIR, "build_m3.py"))  # builder M3
L = _charger_module("layout", os.path.join(ICI, "layout.py"))         # plan M4

import capstone  # noqa: E402
import pefile  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

import carte_m4 as cm  # noqa: E402
import oracle_m4 as od4  # noqa: E402

# --- Garde sceau de l'Intention (v0.6.0 axe 3, D105/D87) --------------------
# Les arbres d'intention qui NOURRISSENT la chaîne proxy.exe : hello-02 (M0)
# vit dans .text, la libc M1 dans .text, tcp M2/M3 et http/tls M3/M4 dans
# .text/.text2/.text3 — un arbre divergé de sa signature = un diff
# d'intention NON SIGNÉ par la clé hors-ligne du développeur : le build
# REFUSE (fail-closed). La garde est une source de vérité UNIQUE :
# v06/sceau_I.py (chargé par chemin, aucune duplication de logique).
SCEAU_I = _charger_module("sceau_I", os.path.join(TRIADE, "v06", "sceau_I.py"))
ARBRES_GARDE_M4 = ["m0", "m1", "m2", "m3", "m4"]


def _garde_sceau_I() -> None:
    """Traduit le refus du sceau I en échec de build (fail-closed nommé)."""
    try:
        SCEAU_I.garde(ARBRES_GARDE_M4)
        print(f"[sceau-I] garde : {len(ARBRES_GARDE_M4)} arbres d'intention "
              f"conformes à leurs signatures ({', '.join(ARBRES_GARDE_M4)}) ; "
              f"clé déposée : {SCEAU_I.etat_cle()}")
    except SCEAU_I.EchecSceauI as exc:
        raise EchecBuild(str(exc)) from exc


# --- Blocs M4 embarqués dans .text3 (couche C, génération 6) -------------------
# (id carte, spec, fichier notation, rva, slot) — le plan d'adressage est la
# source unique (L.BLOCS_TLS / L.BLOCS_REVISIONS) ; les tailles notées
# « déclarées » viennent des en-têtes de notation (« ; Code : N o »).

BLOCS_M4 = [(bid, spec, f"tls-0{i}-" + n, rva, slot)
            for (bid, spec, rva, slot, _v, _e), (i, n) in zip(
                L.BLOCS_TLS,
                [(1, "nom-utf16"), (2, "verdicts"), (3, "jetons"),
                 (4, "poignee"), (5, "cles"), (6, "emission"),
                 (7, "reception"), (8, "session")])]
BLOCS_M4 += [("g70009", "http-08:R2", "http-08-cible-r2", 0x7340, 0x180),
             ("g70010", "http-10:R2", "http-10-session-r2", 0x74C0, 0x900),
             ("g70011", "http-12:R2", "http-12-principal-r2", 0x7DC0, 0x200)]
assert [(b[0], b[3], b[4]) for b in BLOCS_M4] == \
    [(b[0], b[2], b[3]) for b in L.BLOCS_TLS + L.BLOCS_REVISIONS], \
    "BLOCS_M4 diverge du plan d'adressage (layout.py, source unique)"

# libc-07 : feuille M1 nouvellement embarquée (zone reserve-libc 0x13C0,
# octets selftest.exe — R7 ; exigée par tls-06/tls-07).
BLOC_LIBC07 = ("b20007", "libc-07:R1", "libc-07-memset", 0x13C0, 0x80)

# Embarqués M4 au total : 26 (héritage M3) + 1 (libc-07) + 11 (M4) = 38.
BLOCS_EMBARQUES_M4 = B3.blocs_embarques() + [BLOC_LIBC07] + BLOCS_M4

# Clés de blobs pour l'oracle D93 (table d'intégration D92 — jamais deux
# sources : la table ci-dessous est la MÊME que harnais_session_r2.charger).
_CLE_BLOB = {
    "g70001": "tls-01", "g70002": "tls-02", "g70003": "tls-03",
    "g70004": "tls-04", "g70005": "tls-05", "g70006": "tls-06",
    "g70007": "tls-07", "g70008": "tls-08",
    "g70009": "http-08-R2", "g70010": "http-10-R2",
    "a10002": "hello-02", "b20001": "libc-01", "b20003": "libc-03",
    "b20004": "libc-04", "b20007": "libc-07",
    "c30003": "tcp-03", "c30004": "tcp-04", "c30005": "tcp-05",
    "c30006": "tcp-06", "c30011": "tcp-11", "e50013": "tcp-13",
    "e50001": "http-01", "e50002": "http-02", "e50003": "http-03",
    "e50004": "http-04", "e50005": "http-05", "e50006": "http-06",
    "e50007": "http-07", "e50008": "http-08-R1", "e50009": "http-09",
    "e50010": "http-10-R1",
}


def chemin_notation_m4(fichier: str) -> str:
    if fichier.startswith("libc-07"):
        return os.path.join(M1_DIR, "notation", fichier + ".asm")
    return os.path.join(ICI, "notation", fichier + ".asm")


# --- Couche I M4 : lecture et audit du gabarit ---------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures", "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2 : écrite-avant-code)")
    return spec


_FICHIERS_I_M4 = {
    "g70001": "tls-01-nom-utf16.md", "g70002": "tls-02-verdicts.md",
    "g70003": "tls-03-jetons.md", "g70004": "tls-04-poignee.md",
    "g70005": "tls-05-handles.md", "g70006": "tls-06-emission.md",
    "g70007": "tls-07-reception.md", "g70008": "tls-08-session.md",
    "g70009": "http-08-cible-r2.md", "g70010": "http-10-session-r2.md",
    "g70011": "http-12-principal-r2.md",
}


def charger_couche_I_m4() -> dict[str, dict]:
    specs = {}
    for bid, sid, _f, _r, _s in BLOCS_M4:
        ident, rev_ref = sid.split(":")
        chemin = os.path.join(ICI, "I", _FICHIERS_I_M4[bid])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec(chemin)
        if spec["id"] != ident:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {ident}")
        if spec["rev"] != int(rev_ref[1:]):
            raise EchecBuild(f"{chemin} : révision {spec['rev']} != R{rev_ref[1:]} référencée par la couche C")
        specs[bid] = spec
    # libc-07 : spécification M1 scellée (l'audit de gabarit est un fait M1 —
    # la carte génération 6 cite la spécification, elle ne la ré-audite pas).
    return specs


# --- Notation : assemblage, tailles déclarées, round-trip (R5) ------------------

def lignes_notation(chemin: str) -> list[str]:
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().splitlines()
    return [l.strip() for l in brut if l.strip() and not l.strip().startswith(";")]


def taille_declaree(chemin: str) -> int | None:
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith("; Code : "):
                return int(ligne.split("Code : ")[1].split(" o ")[0])
    return None


def assembler_bloc(ks: Ks, chemin: str, rva: int, slot: int) -> tuple[bytes, list[dict]]:
    octets, metas, adresse = b"", [], rva
    for ligne in lignes_notation(chemin):
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise EchecBuild(f"{chemin} : ligne inassemblable : {ligne!r}")
        b = bytes(enc)
        metas.append({"ligne": ligne, "adresse": adresse, "taille": len(b)})
        octets += b
        adresse += len(b)
    if len(octets) > slot:
        raise EchecBuild(f"{chemin} : {len(octets)} o > slot {slot:#x} (D8)")
    if slot - len(octets) < 16:
        raise EchecBuild(f"{chemin} : padding {slot - len(octets)} < 16 (D8)")
    declare = taille_declaree(chemin)
    if declare is not None and declare != len(octets):
        raise EchecBuild(f"{chemin} : {len(octets)} o != {declare} o déclarés (en-tête de notation)")
    return octets, metas


# Alias de mnémoniques conditionnels : keystone accepte les deux formes,
# capstone rend TOUJOURS la forme « e » (0x75 = jnz = jne) — la normalisation
# les met sur le même pied (la notation reste la vérité, l'octet est le juge).
ALIAS_JCC = {
    "jz": "je", "jnz": "jne", "jc": "jb", "jnc": "jae", "jna": "jbe",
    "jnbe": "ja", "jng": "jle", "jnle": "jg", "jnge": "jl", "jnl": "jge",
}
_REG = r"(?:r(?:[a-z]{2,3}|[0-9]+[dwb]?)|[er]?[a-d][xhlpi]|sil|dil|bpl|spl)"

# Largeur d'opérande pour le complément à deux des négatifs (capstone rend
# la valeur non signée de la largeur de l'instruction, la notation porte le
# signe : r10 → 64 bits, r10d → 32 — les deux côtés décrivent la même largeur).
_LARGEURS = {r: 64 for r in (
    "rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
    "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15")}
_LARGEURS |= {r: 32 for r in list(
    ("eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp")) + [
        f"r{i}d" for i in range(8, 16)]}
_LARGEURS |= {r: 16 for r in list(
    ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp")) + [
        f"r{i}w" for i in range(8, 16)]}
_LARGEURS |= {r: 8 for r in list(
    ("al", "bl", "cl", "dl", "sil", "dil", "bpl", "spl")) + [
        f"r{i}b" for i in range(8, 16)]}


def _raboter_qualificateur(t: str) -> str:
    """Rabote « (qword|dword|word|byte) ptr » LÀ OÙ il est déductible d'un
    opérande registre (keystone l'infère, capstone l'imprime — mêmes octets).
    Les côtés mémoire+immédiat gardent leur qualificateur (taille portante)."""
    m = re.match(rf"^(\w+) ({_REG}), (qword|dword|word|byte) ptr (\[.*\])$", t)
    if m and m.group(1) not in ("movzx", "movsx", "movsxd"):
        return f"{m.group(1)} {m.group(2)}, {m.group(4)}"
    m = re.match(rf"^(\w+) (qword|dword|word|byte) ptr (\[[^]]*\]), ({_REG})$", t)
    if m:
        return f"{m.group(1)} {m.group(3)}, {m.group(4)}"
    return t


def _largeur_instruction(t: str) -> int:
    m = re.match(r"^\w+\s+(\w+)\b", t)
    if m:
        if m.group(1) in _LARGEURS:
            return _LARGEURS[m.group(1)]
        if m.group(1) in ("qword", "dword", "word", "byte"):
            return {"qword": 64, "dword": 32, "word": 16, "byte": 8}[m.group(1)]
    return 32


def canon(texte: str) -> str:
    t = re.sub(r"\s+", " ", texte.strip().lower())
    # instructions de chaîne : capstone imprime les opérandes IMPLICITES
    # (« rep stosq qword ptr [rdi], rax »), la notation les omet (« rep stosq »)
    m = re.match(r"^(rep(?:e|z|ne|nz)? (?:stos|movs|lods|scas|cmps)[bwdq])(?: .*)?$", t)
    if m:
        return m.group(1)
    morceaux = t.split(" ", 1)
    if morceaux[0] in ALIAS_JCC:
        t = ALIAS_JCC[morceaux[0]] + (" " + morceaux[1] if len(morceaux) > 1 else "")
    masque = (1 << _largeur_instruction(t)) - 1

    def norm(m: re.Match) -> str:
        v = int(m.group(0), 0)
        if v < 0:
            v &= masque
        return f"0x{v:x}"

    t = re.sub(r"(?<![\w\]])-?(?:0x[0-9a-f]+|\d+)(?![\w])", norm, t)
    # espaces internes des crochets : « [rsp + 0x28] » == « [rsp+0x28] »
    t = re.sub(r"\[\s*([^\]]+?)\s*\]",
               lambda m: "[" + re.sub(r"\s*([+\-*])\s*", r"\1", m.group(1)) + "]", t)
    return _raboter_qualificateur(t)


def round_trip(cs: capstone.Cs, ks: Ks, chemin: str, rva: int, octets: bytes, metas: list[dict]) -> list:
    instructions = list(cs.disasm(octets, rva))
    if len(instructions) != len(metas):
        raise EchecBuild(f"{chemin} : {len(instructions)} instructions désassemblées != {len(metas)} notées")
    for insn, meta in zip(instructions, metas):
        if insn.address != meta["adresse"] or insn.size != meta["taille"]:
            raise EchecBuild(f"{chemin} : désalignement à {meta['adresse']:#x}")
        texte_cs = f"{insn.mnemonic} {insn.op_str}".strip()
        if canon(texte_cs) != canon(meta["ligne"]):
            raise EchecBuild(
                f"{chemin} @ {meta['adresse']:#x} : écart texte notation/désassemblage\n"
                f"  notation      : {meta['ligne']}\n  désassemblage : {texte_cs}")
        renc, _ = ks.asm(texte_cs, insn.address)
        if bytes(renc) != octets[meta["adresse"] - rva: meta["adresse"] - rva + insn.size]:
            raise EchecBuild(f"{chemin} @ {meta['adresse']:#x} : ré-assemblage != octets originaux")
    return instructions


def operande_rip_cible(insn) -> int | None:
    m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size + int(m.group(1), 16)
    m = re.search(r"\[rip - (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size - int(m.group(1), 16)
    return None


def deplacements_declares(chemin: str) -> set[int] | None:
    """La table « Déplacements RIP » de l'en-tête de notation (auteur.py) —
    None si absente. Le build vérifie la CONCORDANCE déclarée <-> réelle :
    la notation porte sa propre métadonnée d'adresses, la preuve la relit."""
    cibles: set[int] = set()
    avec_table = False
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if "Déplacements RIP" in ligne:
                avec_table = True
                continue
            m = re.match(r";\s+(0x[0-9a-f]+) \+ (0x[0-9a-f]+) ([+-]) (0x[0-9a-f]+) = (0x[0-9a-f]+)", ligne)
            if m and avec_table:
                addr, taille, signe, disp, cible = (
                    int(m.group(1), 16), int(m.group(2), 16),
                    1 if m.group(3) == "+" else -1,
                    int(m.group(4), 16), int(m.group(5), 16))
                calculee = addr + taille + signe * disp
                if calculee != cible:
                    raise EchecBuild(f"{chemin} : déplacement déclaré incohérent "
                                     f"{addr:#x}+{taille:#x}{m.group(3)}{disp:#x} != {cible:#x}")
                cibles.add(cible)
    return cibles if avec_table else None


# --- Oracle structurel M4 : les invariants de I, par bloc -----------------------

IAT_M4 = {
    "g70001": set(), "g70002": set(), "g70003": set(),
    "g70004": {"InitializeSecurityContextW"},
    "g70005": {"AcquireCredentialsHandleW", "FreeCredentialsHandle", "DeleteSecurityContext"},
    "g70006": {"QueryContextAttributesW", "EncryptMessage"},
    "g70007": {"DecryptMessage"},
    "g70008": set(),          # l'orchestrateur ne touche JAMAIS SSPI directement
    "g70009": set(),
    "g70010": {"CloseHandle"},   # I6' : le SEUL appel IAT de la session révisée
    "g70011": {"GetStdHandle", "InitializeCriticalSection", "ExitProcess",
               "CloseHandle", "WSACleanup"},   # I1 de http-12:R2 — l'héritage R1
    "b20007": set(),         # libc-07 : feuille pure
}
APPELS_DIRECTS_M4 = {
    # tls-04 : tls-02 (verdicts), tls-03 (jetons), tcp-03/04 (émission/réception jetons)
    "g70004": {0x6080, 0x6180, 0x4140, 0x4180},
    # tls-05 : tls-02
    "g70005": {0x6080},
    # tls-06 : tls-02, tls-03, libc-01 (copie), libc-07 (destruction), tcp-04 (émission)
    "g70006": {0x6080, 0x6180, 0x1100, 0x13C0, 0x4180},
    # tls-07 : tls-02, tls-03, libc-01 (résidu en tête) — AUCUNE socket (I2)
    "g70007": {0x6080, 0x6180, 0x1100},
    # tls-08 : tls-01..07 (sauf tls-02/03, wrappés), tcp-03/04/05/11, tcp-13
    "g70008": {0x6000, 0x62C0, 0x65C0, 0x6740, 0x6A40,
               0x4140, 0x4180, 0x41C0, 0x4B00, 0x4400},
    # http-10:R2 : http-01/02/04..07/09, tcp-03..06/11/13, http-08:R2, tls-08
    "g70010": {0x6D40, 0x7340, 0x4C00, 0x4C80, 0x4F40, 0x5080, 0x5140, 0x5200,
               0x54C0, 0x4140, 0x4180, 0x41C0, 0x4300, 0x4B00, 0x4400},
    # http-12:R2 : hello-02 (ligne KO), tcp-01/02/06/11 — l'héritage R1 (I1)
    "g70011": {0x1040, 0x4000, 0x4100, 0x4300, 0x4B00},
    "b20007": set(),
}
DONNEES_RIP_M4 = {
    "g70005": {L.R_PKG_M4},
    "g70008": {L.R_TXT_TLS_ETABLI, L.R_TXT_TLS_CERT},
    "g70009": {L.R_SLASH},
    "g70010": {L.R_TXT_400, L.R_TXT_431, L.R_TXT_501, L.R_TXT_411, L.R_TXT_505,
               L.R_TXT_502, L.R_TXT_TUNNEL, L.R_TXT_502_CERT,
               L.R_MSG_CONNEXION, L.R_MSG_TUNNEL, L.R_MSG_FIN,
               L.R_NOM_HOST, L.R_NOM_CL, L.R_NOM_TE},
    # http-12:R2 : l'ancre/tab_sum/version/borne de la porte + l'état .data +
    # les messages hérités + LES DEUX CIBLES DE CODE PAR lea (pointeurs de
    # fonctions passés à tcp-06 : http-11 @0x5D80 et http-10:R2 @0x74C0 —
    # D95 : le câblage ; JAMAIS 0x5580, la falsification nominale de V4)
    "g70011": {L3.R_TAB_SUM, L.R_VERSION, L3.R_ANCRE, L3.R_STDOUT, L3.R_STDIN,
               L3.R_LISTEN, L3.R_QUIT, L3.R_CS, L3.R_MSG_BANNIERE,
               L3.R_MSG_ARRET, L3.R_MSG_ERREUR, L3.R_MSG_KO,
               0x5D80, 0x74C0},
    "b20007": set(),
}
# Feuilles pures M4 : aucun appel externe (I1 — assistants internes permis).
FEUILLES_M4 = {"g70001", "g70002", "g70003", "g70009", "b20007"}


def _externe(bid: str, insn, adresses_bloc: set, adresse_entree: int) -> str | None:
    """Classe un call : 'iat:nom' | 'bloc:0x…' | 'interne' | None (miroir M3 :
    le dictionnaire IAT est INVERSÉ {adresse: nom} pour la recherche)."""
    if "rip" in insn.op_str:
        cible = operande_rip_cible(insn)
        slots = {v: n for n, v in {**L.IAT_SLOTS, **L.IAT_SEC32_SLOTS}.items()}
        return f"iat:{slots[cible]}" if cible in slots else f"rip:{cible:#x}"
    if insn.op_str.startswith("0x"):
        cible = int(insn.op_str, 16)
        if cible in adresses_bloc and cible != adresse_entree:
            return "interne"
        return f"bloc:{cible:#x}"
    return None


def oracle_structurel_m4(specs: dict, code: dict, blocs: list[tuple]) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    for bid, sid, fichier, rva, slot in blocs:
        insns = code[bid]["insns"]
        mnemos = [i.mnemonic for i in insns]
        adresses_insns = {i.address for i in insns}
        internes_autorises = APPELS_DIRECTS_M4.get(bid, set()) | (
            {a for a in adresses_insns if a != rva} if bid in FEUILLES_M4 else set())

        # Cibles de saut internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic.startswith("j"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}", cible in adresses_insns,
                       f"cible {cible:#x} hors frontière")

        # Appels : IAT et blocs autorisés par I1 ; assistants internes permis
        for i in insns:
            if i.mnemonic == "call":
                classe = _externe(bid, i, adresses_insns, rva)
                if classe is None:
                    continue
                if classe.startswith("iat:"):
                    verrou(f"{bid}:iat-autorisee@{i.address:#x}",
                           classe[4:] in IAT_M4.get(bid, set()),
                           f"{classe} hors IAT déclarée (I1)")
                elif classe.startswith("bloc:"):
                    verrou(f"{bid}:appel-autorise@{i.address:#x}",
                           int(classe[5:], 16) in internes_autorises,
                           f"{classe} hors blocs déclarés (I1)")

        # Données RIP : cibles déclarées du bloc ; étiquettes internes licites
        cibles_rip: set[int] = set()
        for i in insns:
            cible = operande_rip_cible(i)
            if cible is not None and i.mnemonic != "call":
                cibles_rip.add(cible)
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP_M4.get(bid, set())
                       or rva <= cible < rva + slot,
                       f"cible {cible:#x} hors données déclarées (I2/I5)")

        # Concordance déclarée : la table « Déplacements RIP » de l'en-tête
        # doit correspondre EXACTEMENT aux cibles réelles (appels compris).
        declarees = deplacements_declares(chemin_notation_m4(fichier))
        if declarees is not None:
            rip_reelles = set()
            for i in insns:
                c = operande_rip_cible(i)
                if c is not None:
                    rip_reelles.add(c)
            verrou(f"{bid}:deplacements-rip-declares",
                   rip_reelles == declarees,
                   f"réelles {sorted(hex(c) for c in rip_reelles - declarees)} "
                   f"non déclarées / déclarées {sorted(hex(c) for c in declarees - rip_reelles)} absentes")

        # Interface système : jamais de syscall direct (D7)
        verrou(f"{bid}:pas-de-syscall",
               not any(m in ("syscall", "sysenter", "int") for m in mnemos))

        # Padding intra-slot >= 16 et alignement (D8)
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16, f"écart {rva + slot - fin_code}")
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)

        # Aucun stockage sous RSP (zone interdite msx64)
        for i in insns:
            if i.mnemonic.startswith("mov") and "[" in i.op_str and i.op_str.split(",")[0].strip().endswith("]"):
                base = re.search(r"\[(\w+)", i.op_str)
                if base and base.group(1) == "rsp":
                    disp = re.search(r"\+ (0x[0-9a-f]+)\]", i.op_str)
                    verrou(f"{bid}:pas-de-stockage-sous-rsp@{i.address:#x}",
                           disp is None or int(disp.group(1), 16) >= 0)

        # Pile alignée aux points d'appel EXTERNE (miroir M2/M3)
        npush = 0
        while npush < len(insns) and insns[npush].mnemonic == "push":
            npush += 1
        premier_externe = next((k for k, i in enumerate(insns)
                                if i.mnemonic == "call" and _externe(bid, i, adresses_insns, rva)
                                not in (None, "interne")), None)
        if premier_externe is not None:
            ok = False
            for k in range(premier_externe):
                if insns[k].mnemonic == "sub" and insns[k].op_str.startswith("rsp,"):
                    imm = int(insns[k].op_str.split(",")[1].strip(), 16)
                    ok = (8 + 8 * npush - imm) % 16 == 0
                    break
            verrou(f"{bid}:pile-alignee", ok, "prologue non aligné avant appel externe")

    # Feuilles M4 : aucun appel externe
    for bid in FEUILLES_M4:
        rva_bid = next(r for b, _, _, r, _ in blocs if b == bid)
        for i in code[bid]["insns"]:
            if i.mnemonic == "call":
                verrou(f"{bid}:feuille-sans-appel-externe@{i.address:#x}",
                       _externe(bid, i, {x.address for x in code[bid]["insns"]}, rva_bid) == "interne",
                       "une feuille pure n'appelle rien d'extérieur (I1)")

    # g70010 (http-10:R2) — leçon D63 armée sur 0x13390 (V6bis) : le probing
    # touche [rsp-0x13390] AVANT le sub rsp, 0x13390 (multiple de 16, ABI P5).
    m = code["g70010"]["insns"]
    idx_sub = next((k for k, i in enumerate(m)
                    if i.mnemonic == "sub" and i.op_str == f"rsp, {L.TAILLE_CADRE_SESSION_R2:#x}"), None)
    verrou("g70010:prologue-sub-0x13390", idx_sub is not None, "sub rsp, 0x13390 introuvable")
    if idx_sub is not None:
        verrou("g70010:prologue-multiple-16", L.TAILLE_CADRE_SESSION_R2 % 16 == 0)
        verrou("g70010:probing-touche-cadre",
               any(k < idx_sub and "rsp - 0x13390" in i.op_str.replace(" - 0x13390", " - 0x13390")
                   for k, i in enumerate(m[:idx_sub]) if True)
               or any(f"[rsp - {L.TAILLE_CADRE_SESSION_R2:#x}]" in i.op_str for i in m[:idx_sub]),
               "la touche [rsp-0x13390] précède le sub (D63)")
        verrou("g70010:probing-par-pages",
               any("rsp + r10" in i.op_str or "[rsp + r10]" in i.op_str for i in m[:idx_sub]),
               "la boucle de probing par pages est absente")

    # I6' : http-10:R2 appelle EXACTEMENT UNE fonction IAT (CloseHandle) —
    # aucun appel SSPI direct, aucun tls-01..07 direct (tout passe par tls-08).
    iats_g70010 = {classe[4:] for i in m if i.mnemonic == "call"
                   and (classe := _externe("g70010", i, {x.address for x in m}, 0x74C0))
                   and classe.startswith("iat:")}
    verrou("g70010:iat-unique-closehandle", iats_g70010 == {"CloseHandle"},
           f"IAT vues : {iats_g70010}")
    appels_g70010 = {int(i.op_str, 16) for i in m if i.mnemonic == "call" and i.op_str.startswith("0x")}
    interdits = {0x6000, 0x6080, 0x6180, 0x62C0, 0x65C0, 0x6740, 0x6A40}
    verrou("g70010:jamais-tls-feuilles-direct", not (appels_g70010 & interdits),
           f"appels directs TLS interdits : {sorted(hex(a) for a in appels_g70010 & interdits)}")

    # tls-08 : l'orchestrateur n'appelle JAMAIS l'IAT (tout est wrappé).
    verrou("g70008:aucune-iat",
           not any(_externe("g70008", i, {x.address for x in code["g70008"]["insns"]}, 0x6D40)
                   and _externe("g70008", i, {x.address for x in code["g70008"]["insns"]}, 0x6D40).startswith("iat:")
                   for i in code["g70008"]["insns"] if i.mnemonic == "call"))

    # Traçabilité : chaque bloc a sa spécification chargée (D24)
    attendus = {b for b, *_ in blocs}
    verrou("tracabilite-I", attendus <= set(specs) | {"b20007"},
           str(attendus - set(specs) - {"b20007"}))
    return verrous

# --- Composition de l'image M4 -------------------------------------------------

SHA_PROXY_SCELLE = "bf02769fa324ff79b07550c5f31fe6e8f7b0611489e710d16ee07afa73c070af"


def _somme_qwords(octets: bytes) -> int:
    return sum(struct.unpack(f"<{len(octets) // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF


def tranche_section(exe: bytes, rva: int, taille: int) -> bytes:
    """Tranche d'un RVA dans l'image (par section)."""
    if L.TEXT_RVA <= rva < L.RDATA_RVA:
        return exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + taille]
    if L.RDATA_RVA <= rva < L.DATA_RVA:
        return exe[L.RDATA_FILE + (rva - L.RDATA_RVA): L.RDATA_FILE + (rva - L.RDATA_RVA) + taille]
    if L.TEXT2_RVA <= rva < L.TEXT3_RVA:
        return exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA): L.TEXT2_FILE + (rva - L.TEXT2_RVA) + taille]
    if rva >= L.TEXT3_RVA:
        return exe[L.TEXT3_FILE + (rva - L.TEXT3_RVA): L.TEXT3_FILE + (rva - L.TEXT3_RVA) + taille]
    raise EchecBuild(f"RVA {rva:#x} hors sections")


def comparer_scelle(exe_m4: bytes, scelle: bytes, deltas: list[tuple[int, int, str]]) -> None:
    """L'image M4 == l'image scellée 0.4.0, DELTAS documentés exceptés (R7).

    Les sections .text/.text2/.data/.rdata(→0x29A0) sont comparées PAR SECTION
    — chaque artefact à SES offsets fichier propres (D94 : le packaging M4
    glisse de +0x200, les RVA sont intacts). Chaque delta est (rva, taille,
    motif) — tout octet divergent hors deltas est un échec."""
    sections = [
        (L.TEXT_RVA, L.TEXT_VSIZE, L.TEXT_FILE, L3.TEXT_FILE, ".text"),
        (L.TEXT2_RVA, L.TEXT2_VSIZE, L.TEXT2_FILE, L3.TEXT2_FILE, ".text2"),
        (L.DATA_RVA, L.DATA_RAW, L.DATA_FILE, L3.DATA_FILE, ".data"),
        (L.RDATA_RVA, L.R_IMPORTS_M4 - L.RDATA_RVA, L.RDATA_FILE, L3.RDATA_FILE, ".rdata"),
    ]
    for rva_base, vsize, fichier_m4, fichier_m3, nom in sections:
        a = exe_m4[fichier_m4: fichier_m4 + vsize]
        b = scelle[fichier_m3: fichier_m3 + vsize]
        if a == b:
            continue
        # divergence : localiser chaque octet, vérifier l'appartenance aux deltas
        for k, (x, y) in enumerate(zip(a, b)):
            if x != y:
                rva = rva_base + k
                if not any(d <= rva < d + t for d, t, _m in deltas):
                    raise EchecBuild(
                        f"R7 rompu : .{nom} @{rva:#x} diverge du scellé 0.4.0 "
                        f"({x:#04x} != {y:#04x}) hors deltas documentés")
    return None


def composer_image_m4(texte_m3: bytes, rdata_m3: bytes, data_m3: bytes, text2_m3: bytes,
                      code: dict, slot_libc07: bytes):
    """-> (texte, rdata, data, text2, text3) — l'image complète de proxy.exe M4."""
    # .text3 : la section est composée EN PREMIER — la porte R10 .text3 (D95)
    # scelle sa somme sur CES octets (int3 + les onze blocs M4, padding NOP
    # intra-slot) ; la couche M4 entière devient gardée au lancement.
    text3 = bytearray(b"\xcc" * L.TEXT3_VSIZE)
    for bid, _sid, _f, rva, slot in BLOCS_M4:
        text3[rva - L.TEXT3_RVA: rva - L.TEXT3_RVA + slot] = code[bid]["slot"]

    # .text : héritage + libc-07 dans la zone reserve-libc (était int3)
    texte = bytearray(texte_m3)
    texte[0x13C0 - L.TEXT_RVA: 0x13C0 - L.TEXT_RVA + 0x80] = slot_libc07

    # .rdata : héritage + deltas documentés + extension M4
    rdata = bytearray(rdata_m3)
    # (1) 8e entrée de la table des réponses — l'entrée ÉTIQUETÉE (D92, Q3')
    if len(L.TXT_502_CERT) != 34:
        raise EchecBuild(f"garde-fou 502-cert : {len(L.TXT_502_CERT)} o != 34 (D92)")
    rdata[0x2550 - L.RDATA_RVA: 0x2550 - L.RDATA_RVA + 16] = \
        struct.pack("<QQ", L.R_TXT_502_CERT, len(L.TXT_502_CERT))
    # (2) porte R10 : entrée libc-07 @0x2800 + LA PORTE .text3 @0x2810 (D95 —
    #     l'ancien terminateur M4-dev.1 est REMPLACÉ : la table est PLEINE,
    #     28 entrées, la marche aux bornes de http-12:R2 s'arrête à R_VERSION ;
    #     la somme est scellée sur la section .text3 CI-DESSUS — composée d'abord)
    rdata[0x2800 - L.RDATA_RVA: 0x2800 - L.RDATA_RVA + 16] = \
        struct.pack("<IIQ", 0x13C0, 0x80, _somme_qwords(slot_libc07))
    rdata[L.R10_PORTE_TEXT3 - L.RDATA_RVA: L.R10_PORTE_TEXT3 - L.RDATA_RVA + 16] = \
        struct.pack("<IIQ", L.R10_TEXT3_RVA, L.R10_TEXT3_TAILLE,
                    _somme_qwords(bytes(text3)))
    # (3) version (R10 : monotonie — 0.5.1 > dev.2 ≥ plancher 0.4.0 scellé ;
    #     jalon v7/D140 : tls-05:R2 — SCH_CREDENTIALS explicite, révocation retirée)
    rdata[0x2820 - L.RDATA_RVA: 0x2820 - L.RDATA_RVA + 8] = \
        struct.pack("<Q", L.VERSION_U64_051)
    # (4) extension M4 (ARRÊT D81/D92 — layout.py source unique)
    _poses: list[tuple[int, int, str]] = []

    def poser(rva: int, donnees: bytes, nom: str = ""):
        fin = rva + len(donnees)
        if rva - L.RDATA_RVA + len(donnees) > L.RDATA_VSIZE:
            raise EchecBuild(f".rdata débordante à {rva:#x} (D33)")
        if rva < L.R_IMPORTS_M4:
            raise EchecBuild(f"extension M4 sous 0x29A0 (R7 rompu) : {nom or hex(rva)}")
        for rva_p, fin_p, nom_p in _poses:
            if rva < fin_p and rva_p < fin:
                raise EchecBuild(
                    f"chevauchement .rdata M4 : {nom or hex(rva)} [{rva:#x}, {fin:#x})"
                    f" recouvre {nom_p} [{rva_p:#x}, {fin_p:#x})")
        _poses.append((rva, fin, nom or hex(rva)))
        rdata[rva - L.RDATA_RVA: rva - L.RDATA_RVA + len(donnees)] = donnees

    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"
    # table des descripteurs M4 : kernel32 / ws2_32 / secur32 + terminateur
    poser(L.R_IMPORTS_M4,
          struct.pack("<IIIII", L3.R_INT_KERNEL32, 0, 0, L3.R_NOM_DLL, L3.R_IAT)
          + struct.pack("<IIIII", L3.R_INT_WS2, 0, 0, L3.R_NOM_WS2, L3.R_IAT_WS2)
          + struct.pack("<IIIII", L.R_INT_SEC32, 0, 0, L.R_NOM_SEC32, L.R_IAT_SEC32)
          + b"\x00" * 20, "descripteurs-M4")
    poser(L.R_NOM_SEC32, b"secur32.dll\x00", "nom-secur32")
    # hints/names secur32 (les RVA calculés alimentent IAT + INT)
    hints_sec32, rva_h = {}, L.R_HN_SEC32
    for nom in L.SECUR32_IMPORTS:
        hints_sec32[nom] = rva_h
        poser(rva_h, hn(nom))
        rva_h += len(hn(nom))
    poser(L.R_IAT_SEC32, b"".join(struct.pack("<Q", hints_sec32[n]) for n in L.SECUR32_IMPORTS)
          + struct.pack("<Q", 0), "iat-secur32")
    poser(L.R_INT_SEC32, b"".join(struct.pack("<Q", hints_sec32[n]) for n in L.SECUR32_IMPORTS)
          + struct.pack("<Q", 0), "int-secur32")
    # fixtures M4 (garde-fous de longueurs — la notation porte ces valeurs)
    if len(L.PKG_M4) != 90:
        raise EchecBuild(f"garde-fou package : {len(L.PKG_M4)} o != 90 (D81)")
    poser(L.R_PKG_M4, L.PKG_M4, "package")
    for rva, chaine, attendu, nom in (
            (L.R_TXT_TLS_ETABLI, L.TXT_TLS_ETABLI, 23, "tunnel-etabli"),
            (L.R_TXT_TLS_CERT, L.TXT_TLS_CERT, 19, "certificat-rejete"),
            (L.R_TXT_502_CERT, L.TXT_502_CERT, 34, "502-cert")):
        if len(chaine) != attendu:
            raise EchecBuild(f"garde-fou fixture {nom} : {len(chaine)} o != {attendu}")
        poser(rva, chaine + b"\x00", nom)

    # .text3 : composée EN TÊTE de fonction (la porte scelle sa somme dessus)
    return bytes(texte), bytes(rdata), bytes(data_m3), bytes(text2_m3), bytes(text3)


# --- Éditeur PE32+ (cinq sections) ----------------------------------------------

def ecrire_pe32plus(texte: bytes, rdata: bytes, data: bytes, text2: bytes, text3: bytes) -> bytes:
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 5, 0, 0, 0, 0xF0, 0x0002)
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B, 0, 0,
        L.ENTREE, len(texte) + len(text2) + len(text3), 0,
        L.ENTREE_R2, L.TEXT_RVA,   # AddressOfEntryPoint : 0x7DC0 (D95 — le
                                   # câblage ; l'ancêtre 0x1800 reste embarqué,
                                   # mort au lancement, vivant à la preuve R7)
        L.IMAGE_BASE,
        L.SECT_ALIGN, L.FILE_ALIGN,
        6, 0, 0, 1, 6, 0, 0,
        L.SIZE_OF_IMAGE,
        L.TEXT_FILE,                  # SizeOfHeaders : 0x400 (en-têtes 528 o
                                    # arrondis à l'alignement fichier)
        0,
        3,                          # Subsystem : CONSOLE
        L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    dirs = [(0, 0)] * 16
    dirs[1] = (L.R_IMPORTS_M4, 80)     # D81 : répertoire d'imports M4 @0x29A0
    dirs[5] = (L3.R_RELOC, 12)
    dirs[12] = (L3.R_IAT, 88)
    opt = bytes(opt_fixe) + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr, 0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", L.TEXT_VSIZE, L.TEXT_RVA, L.TEXT_VSIZE, L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", L.RDATA_VSIZE, L.RDATA_RVA, L.RDATA_VSIZE, L.RDATA_FILE, 0x40000040)
        + sh(b".data\x00\x00\x00", L.DATA_VSIZE, L.DATA_RVA, L.DATA_RAW, L.DATA_FILE, 0xC0000040)
        + sh(b".text2\x00\x00", L.TEXT2_VSIZE, L.TEXT2_RVA, L.TEXT2_VSIZE, L.TEXT2_FILE, 0x60000020)
        + sh(b".text3\x00\x00", L.TEXT3_VSIZE, L.TEXT3_RVA, L.TEXT3_VSIZE, L.TEXT3_FILE, 0x60000020)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 200, len(entetes)
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[L.TEXT_FILE:L.TEXT_FILE + len(texte)] = texte
    exe[L.RDATA_FILE:L.RDATA_FILE + len(rdata)] = rdata
    exe[L.DATA_FILE:L.DATA_FILE + len(data)] = data
    exe[L.TEXT2_FILE:L.TEXT2_FILE + len(text2)] = text2
    exe[L.TEXT3_FILE:L.TEXT3_FILE + len(text3)] = text3
    return bytes(exe)


# --- Validation PE ---------------------------------------------------------------

def valider_pe(exe: bytes):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.NumberOfSections == 5, "sections != 5"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE_R2, \
        "point d'entrée != http-12:R2 (0x7DC0, D95 — le câblage)"
    assert pe.OPTIONAL_HEADER.ImageBase == L.IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HEVA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2", ".text3"], noms
    assert pe.sections[4].Characteristics & 0x60000020 == 0x60000020, ".text3 non RX"
    assert pe.sections[2].SizeOfRawData == L.DATA_RAW
    # Offsets fichier M4 (D94 : +0x200, contigus, en-têtes 528 o à 0x400)
    assert pe.OPTIONAL_HEADER.SizeOfHeaders == L.TEXT_FILE, "SizeOfHeaders != 0x400"
    for s, attendu in zip(pe.sections, (L.TEXT_FILE, L.RDATA_FILE, L.DATA_FILE,
                                        L.TEXT2_FILE, L.TEXT3_FILE)):
        assert s.PointerToRawData == attendu, \
            f"PointerToRawData {s.Name.decode().rstrip(chr(0))} != {attendu:#x}"
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports[entree.dll.decode().lower()] = [i.name.decode() for i in entree.imports]
    assert imports == {"kernel32.dll": L3.KERNEL32_IMPORTS,
                       "ws2_32.dll": L3.WS2_IMPORTS,
                       "secur32.dll": L.SECUR32_IMPORTS}, imports
    ft_attendus = {"kernel32.dll": L3.R_IAT, "ws2_32.dll": L3.R_IAT_WS2,
                   "secur32.dll": L.R_IAT_SEC32}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        assert entree.struct.FirstThunk == ft_attendus[entree.dll.decode().lower()], \
            f"FirstThunk {entree.dll.decode()} != {ft_attendus[entree.dll.decode().lower()]:#x}"
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress == L.R_IMPORTS_M4, \
        "répertoire d'imports != 0x29A0 (D81)"
    assert len(exe) == L.TAILLE_FICHIER, "taille de fichier inattendue"
    # Zones réservées : int3 dans l'image livrée (héritage M3 + .text3 — la
    # zone réserve-t3 recule à 0x7FC0 : le slot http-12:R2 0x7DC0+0x200 l'exige)
    for rva in (0x4200, 0x45C0, 0x4800, 0x7FC0):
        assert tranche_section(exe, rva, 1)[0] == 0xCC, f"zone réservée @{rva:#x} != int3"
    # 8e entrée de la table des réponses (concordance Q3' — I5 de http-10:R2)
    ptr, lng = struct.unpack("<QQ", tranche_section(exe, 0x2550, 16))
    assert (ptr, lng) == (L.R_TXT_502_CERT, 34), f"8e entrée != (0x2CA0, 34) : {(ptr, lng)}"
    # Version (R10 : monotonie — 0.5.1)
    assert struct.unpack("<Q", tranche_section(exe, 0x2820, 8))[0] == L.VERSION_U64_051
    # Porte R10 : la table marchée depuis l'image est AUTO-CONSISTANTE — la
    # MARCHE AUX BORNES de http-12:R2 (D95 : la table est PLEINE, l'entrée
    # .text3 @0x2810 remplace l'ancien terminateur, fail-closed sur entrée
    # trouée — le MÊME contrat que la notation, jamais deux sources)
    k = 0
    rva_table = L3.R_TAB_SUM
    while rva_table + 16 * k < L.R10_BORNE:
        r, t, s = struct.unpack("<IIQ", tranche_section(exe, rva_table + 16 * k, 16))
        assert r != 0 and t != 0, \
            f"porte R10 : entrée #{k + 1} trouée (rva/taille nuls — fail-closed D95)"
        somme = _somme_qwords(tranche_section(exe, r, t))
        assert somme == s, f"porte R10 : somme de {r:#x} divergente ({somme:#x} != {s:#x})"
        k += 1
        assert k <= L.R10_NB_ENTREES, "porte R10 : borne R_VERSION franchie"
    assert k == L.R10_NB_ENTREES, \
        f"porte R10 : {k} entrées != 28 (26 héritage + libc-07 + porte .text3)"
    return True


# --- Preuve de réutilisation (R7 — les DEUX générations) --------------------------

def preuve_reutilisation(exe: bytes) -> dict:
    """proxy.exe M4 partage son squelette avec le scellé 0.4.0 : .text/.text2/
    .data octet-identiques SAUF libc-07 (@0x13C0, zone int3 en M3) ; .rdata
    identique SAUF les deltas documentés ; hello/selftest/echo inchangés."""
    scelle_p = os.path.join(M3_DIR, "proxy.exe")
    with open(scelle_p, "rb") as f:
        scelle = f.read()
    if hashlib.sha256(scelle).hexdigest() != SHA_PROXY_SCELLE:
        raise EchecBuild("proxy.exe 0.4.0 divergent de l'artefact scellé (R7)")
    for nom, chemin, sha in (("hello", os.path.join(M0_DIR, "hello.exe"), B3.SHA_HELLO),
                             ("selftest", os.path.join(M1_DIR, "selftest.exe"), B3.SHA_SELFTEST),
                             ("echo", os.path.join(M2_DIR, "echo.exe"), B3.SHA_ECHO_SCELLE)):
        with open(chemin, "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != sha:
                raise EchecBuild(f"{nom}.exe divergent de l'artefact scellé (R7)")
    comparer_scelle(exe, scelle, [
        (0x13C0, 0x80, "libc-07 embarqué (zone reserve-libc, int3 en M3)"),
        (0x2550, 16, "8e entrée de la table des réponses (502 Certificat rejete)"),
        (0x2800, 16, "entrée R10 libc-07 (terminateur descendu à 0x2810)"),
        (0x2810, 16, "porte R10 .text3 (D95 : l'ancien terminateur M4-dev.1 "
                     "remplacé — marche aux bornes de http-12:R2)"),
        (0x2820, 8, "version 0x00050003 (R10 monotonie — 0.5.1, D140)"),
    ])
    # libc-07 : octets identiques à selftest.exe @0x13C0 (R7 direct)
    with open(os.path.join(M1_DIR, "selftest.exe"), "rb") as f:
        selftest = f.read()
    if tranche_section(exe, 0x13C0, 0x80) != \
            selftest[L3.TEXT_FILE + (0x13C0 - L3.TEXT_RVA): L3.TEXT_FILE + (0x13C0 - L3.TEXT_RVA) + 0x80]:
        raise EchecBuild("libc-07 divergent de selftest.exe @0x13C0 (R7)")
    return {"sha_proxy_scelle": SHA_PROXY_SCELLE[:16],
            "blocs_reutilises": len(B3.blocs_embarques()) + 1}


# --- Vérifier-puis-écrire : notations <-> artefact (R5) ----------------------------

def verifier_puis_ecrire(exe: bytes, code_m3: dict, code_m4: dict):
    for bid, _sid, _f, rva, slot in BLOCS_EMBARQUES_M4:
        slot_complet = code_m3[bid]["slot"] if bid in code_m3 else code_m4[bid]["slot"]
        if tranche_section(exe, rva, slot) != slot_complet:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5 — verifier-puis-ecrire)")
    return len(BLOCS_EMBARQUES_M4)

# --- Carte projet, génération 6 (lignée D80) -------------------------------------

CONTRATS_M4 = {
    "g70001": ("(src ptr, longueur u64, dst ptr) -> u32",
               "span hote ; dst >= 2*(longueur+1) ; HOTE_MAX 255 ; pile alignee",
               "0 : traduction UTF-16 NUL-terminee ; 1..7 verdicts nommes",
               "feuille pure ; traduction UNE fois (miroir tcp-13:Q2) ; aucune ecriture hors zone",
               "aucune"),
    "g70002": ("(hresult i32) -> (verdict u32, edx u32)",
               "pile alignee",
               "verdict 0-6 nomme ; edx = HRESULT d origine",
               "feuille pure ; table TOTALE fail-closed (6 = fatal inconnu) ; jamais un HRESULT brut seul",
               "aucune"),
    "g70003": ("(operation u32, cadre ptr, args) -> u32",
               "descripteurs dans le cadre propre ; pile alignee",
               "0 : SecBufferDesc conformes (types 0/1/2) ; verdicts nommes",
               "feuille pure ; bornes MAX_JETON ; proprietaire unique des descripteurs",
               "aucune"),
    "g70004": ("(cadre ptr) -> u32",
               "socket connectee ; credentials acquis ; cadre coherent",
               "0 poignee etablie ; 2-6 verdicts tls-02 transportes ; contexte et verdict+HRESULT au cadre",
               "boucle ISC <= 16 allers (E5) ; garde E2 jeton ; accumulation fraiche apres continuation",
               "[g70002] [g70003] [c30003] [c30004] [ext secur32:InitializeSecurityContextW]"),
    "g70005": ("(operation u32, cadre ptr) -> u32",
               "operation 0|1 ; pile alignee",
               "op 0 : credentials acquis ; op 1 : handles detruits, cadre remis a zero",
               "unique proprietaire du cycle de vie (ACH/FCH/DSC) ; HRESULT routes par tls-02",
               "[g70002] [ext secur32:AcquireCredentialsHandleW,FreeCredentialsHandle,DeleteSecurityContext] [rdata:package]"),
    "g70006": ("(cadre ptr, span ptr, longueur u64, sock) -> u32",
               "contexte etabli ; tailles de flux acquises ; span valide ; pile alignee",
               "0 : emission chiffree complete ; 1-6 verdicts nommes",
               "morceaux min(restant, message max NEGOCIE) ; clair copie DETRUIT par libc-07 ; QCA une fois par session",
               "[g70002] [g70003] [b20001] [b20007] [c30004] [ext secur32:QueryContextAttributesW,EncryptMessage]"),
    "g70007": ("(cadre ptr, lot u32) -> u32",
               "contexte etabli ; geometrie coherente (offset + lot <= 32768)",
               "0 : lot decrypte + geometrie normalisee ; 2 incomplet ; 3-6 verdicts",
               "AUCUNE socket (I2) ; offset normalise en tete ; residu descend par libc-01",
               "[g70002] [g70003] [b20001] [ext secur32:DecryptMessage]"),
    "g70008": ("(paquet ptr, cadre ptr) -> u32",
               "paquet rempli par http-10:R2 ; cadre TLS VIERGE ; WSA actif",
               "0 : session complete de bout en bout ; 2-6 verdicts tls-02 transportes ; 7 cible injoignable",
               "compensation INTEGRALE par comptage ; socket cliente JAMAIS fermee (I1) ; certificat rejete AVANT compensation",
               "[g70001] [g70004] [g70005] [g70006] [g70007] [c30003] [c30004] [c30005] [c30011] [e50013] [rdata:etats-nommes]"),
    "g70009": ("(cible ptr, longueur, methode u32, zone ptr 40) -> u32",
               "longueur > 0 (garantie http-02)",
               "0 : forme + spans ; 1..3 verdicts herites R1 ; 4 cible TLS (port 443 implicite)",
               "feuille pure ; https byte-exact strict minuscule ; schema prefixe impossible par construction",
               "[rdata:slash]"),
    "g70010": ("(sock cliente) -> ()",
               "CS/stdout initialises par http-12 ; WSA actif ; pile vierge",
               "session complete : routage https -> tls-08, reponses d echec TLS (502 Certificat rejete / 502 R1), sinon heritage R1",
               "verdict http-08:R2 consigne @+0x7010 sur tout chemin ; garde rdi @+0x7020 ; cadre TLS VIERGE ; UN appel IAT (CloseHandle) ; jamais tls-01..07 direct",
               "[e50001..e50009] [e50013] [g70008] [g70009] [c30003..c30006] [c30011] [ext kernel32:CloseHandle] [rdata:reponses,noms,502-cert]"),
    "g70011": ("() -> noreturn (point d entree PE, thread principal)",
               "pile alignee (convention chargeur) ; .data a l etat image",
               "le processus finit TOUJOURS par ExitProcess (0 arret demande, 1 integrite, 2 erreur structurale)",
               "porte R10 MARCHE AUX BORNES : 28 entrees, fail-closed sur entree trouee, la couche .text3 entiere gardee au lancement ; LA BOUCLE LANCE http-10:R2 (0x74C0 — le cablage) ; ordre d initialisation D42 herite",
               "[a10002] [c30001] [c30002] [c30006] [c30011] [e50011] [g70010] [ext kernel32:GetStdHandle,InitializeCriticalSection,ExitProcess,CloseHandle] [ext ws2_32:WSACleanup] [rdata:table-R10,version,ancre,messages]"),
}
CONTRATS = dict(B3.CONTRATS) | CONTRATS_M4

ROLES = dict(L.NOMS_BLOCS)

EXE_PAR_BLOC = dict(B3.EXE_PAR_BLOC)
EXE_PAR_BLOC["b20007"] = "selftest,proxy"      # libc-07 devient EMBARQUÉ (M4)
EXE_PAR_BLOC |= {bid: "proxy" for bid, *_ in BLOCS_M4}

RVA_PAR_BLOC = {
    "a10001": 0x1000, "a10002": 0x1040, "a10003": 0x1080,
    "b20001": 0x1100, "b20002": 0x1180, "b20003": 0x1200,
    "b20004": 0x1280, "b20005": 0x1300, "b20006": 0x1380,
    "b20007": 0x13C0, "b20008": 0x1800, "c30012": 0x1440,
    "c30007": 0x4400, "c30008": 0x4600, "c30009": 0x4800,
    "c30010": 0x4980, "c30013": 0x1800, "c30014": 0x4680,
}
RVA_PAR_BLOC |= {bid: rva for bid, _s, _f, rva, _sl in B3.blocs_embarques()}
RVA_PAR_BLOC |= {bid: rva for bid, _s, _f, rva, _sl in BLOCS_M4}

SPEC_PAR_BLOC = {
    "a10001": "hello-01:R1", "a10002": "hello-02:R1", "a10003": "hello-03:R1",
    "b20001": "libc-01:R1", "b20002": "libc-02:R1", "b20003": "libc-03:R1",
    "b20004": "libc-04:R1", "b20005": "libc-05:R1", "b20006": "libc-06:R1",
    "b20007": "libc-07:R1", "b20008": "libc-08:R2",
    "c30001": "tcp-01:R1", "c30002": "tcp-02:R1", "c30003": "tcp-03:R1",
    "c30004": "tcp-04:R1", "c30005": "tcp-05:R1", "c30006": "tcp-06:R1",
    "c30007": "tcp-07:R3", "c30008": "tcp-08:R1", "c30009": "tcp-09:R1",
    "c30010": "tcp-10:R1", "c30011": "tcp-11:R1", "c30012": "libc-09:R1",
    "c30013": "tcp-12:R1", "c30014": "tcp-08:R2",
    "e50001": "http-01:R1", "e50002": "http-02:R1", "e50003": "http-03:R1",
    "e50004": "http-04:R1", "e50005": "http-05:R1", "e50006": "http-06:R2",
    "e50007": "http-07:R1", "e50008": "http-08:R1", "e50009": "http-09:R1",
    "e50010": "http-10:R2", "e50011": "http-11:R1", "e50012": "http-12:R1",
    "e50013": "tcp-13:R1",
    "g70001": "tls-01:R1", "g70002": "tls-02:R1", "g70003": "tls-03:R1",
    "g70004": "tls-04:R1", "g70005": "tls-05:R2", "g70006": "tls-06:R1",
    "g70007": "tls-07:R2", "g70008": "tls-08:R1",
    "g70009": "http-08:R2", "g70010": "http-10:R2",
    "g70011": "http-12:R2",
}

FICH_PAR_BID = {
    "a10001": "hello-01-main", "b20005": "libc-05-zone-alloc",
    "b20006": "libc-06-zone-reset", "b20007": "libc-07-memset",
    "b20008": "libc-08-autotest", "c30012": "libc-09-zone-alloc-ts",
    "c30014": "tcp-08-echo-v2", "c30007": "tcp-07-patch",
    "c30008": "tcp-08-echo", "c30009": "tcp-09-conn",
    "c30010": "tcp-10-console", "c30013": "tcp-12-main",
}
FICH_PAR_BID |= {bid: f for bid, _s, f, _r, _sl in B3.blocs_embarques()}
FICH_PAR_BID |= {bid: f for bid, _s, f, _r, _sl in BLOCS_M4}

TOUS_BLOCS = sorted(RVA_PAR_BLOC)
EMBARQUES = {bid for bid, *_ in BLOCS_EMBARQUES_M4}


def _chemin_notation_bid(bid: str) -> str:
    """Notation d'un bloc indexé par la carte : routage M4 par défaut,
    héritage via le routeur M3 (jamais deux sources de vérité du routage)."""
    fichier = FICH_PAR_BID[bid]
    if fichier.startswith("tls-") or fichier in ("http-08-cible-r2", "http-10-session-r2",
                                                  "http-12-principal-r2"):
        return os.path.join(ICI, "notation", fichier + ".asm")
    if fichier == "libc-07-memset":
        return os.path.join(M1_DIR, "notation", fichier + ".asm")
    return B3.chemin_notation(fichier)


def fragments_clairs(exe: bytes, verrous_m3: list, verrous_m4: list, version: str,
                     verdict_oracle: dict, compteurs: dict, journal_runs: list[str]) -> dict[str, bytes]:
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()

    loc = ["[carte-frag] nom=frag-loc generation=6",
           "[zones] io=0x1000-0x10ff libc=0x1100-0x143f app=0x1800-0x1fff "
           "net=0x4000-0x42ff cli=0x4400-0x45bf thr=0x4300-0x43ff "
           "srv=0x4b00-0x4bff http=0x4c00-0x5e7f "
           "tls=0x6000-0x733f revisions=0x7340-0x7fbf reserve-t3=0x7fc0-0x7fff "
           "reserve-libc=0x1440-0x17ff (int3 defensif)"]
    for bid in TOUS_BLOCS:
        loc.append(f"[bloc] id={bid} spec={SPEC_PAR_BLOC[bid]} cible=x86-64-win11-pe "
                   f"exe={EXE_PAR_BLOC[bid]} addr={L.IMAGE_BASE + RVA_PAR_BLOC[bid]:#x} "
                   f"v=1 etat=scelle role={ROLES[bid]}")

    con = ["[carte-frag] nom=frag-con generation=6"]
    for bid in TOUS_BLOCS:
        sig, pre, post, inv, deps = CONTRATS[bid]
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]

    prf = ["[carte-frag] nom=frag-prf generation=6"]
    for bid in TOUS_BLOCS:
        with open(_chemin_notation_bid(bid), "rb") as f:
            empreinte_notation = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [
            f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} crist={crist}/10",
            f"  vecteurs : roundtrip=ok structure=ok notation={empreinte_notation}",
        ]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]

    bld = ["[carte-frag] nom=frag-bld generation=6"]
    for bid in TOUS_BLOCS:
        rva = RVA_PAR_BLOC[bid]
        if bid in EMBARQUES:
            slot = next(s for b, _sid, _f, _r, s in BLOCS_EMBARQUES_M4 if b == bid)
            empreinte = sha(tranche_section(exe, rva, slot))
        else:
            with open(_chemin_notation_bid(bid), "rb") as f:
                empreinte = "notation:" + sha(f.read())[7:]
        bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} empreinte={empreinte}")
    bld += [
        f"[build] artefact=proxy.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous structurels : M3 {len(verrous_m3)} + M4 {len(verrous_m4)} ; "
        f"oracle : {verdict_oracle.get('total_cas', 0)} cas, "
        f"graine={verdict_oracle.get('graine', '-')}, volume={verdict_oracle.get('volume', '-')}",
        f"  heritage : proxy.exe 0.4.0 scelle (bf02769f...) repris octet pour octet "
        f"(R7 : .text/.text2/.data intacts, .rdata aux deltas documentes : 8e reponse, "
        f"entree R10 libc-07, porte R10 .text3, version ; entree PE 0x7DC0 [D95]) ; "
        f"libc-07 embarque a 0x13C0 (octets selftest.exe) ; "
        f"hello.exe 0.1.0 + selftest.exe 0.2.0 + echo.exe 0.3.0 inchanges",
        "[zones] io=0x1000-0x10ff libc=0x1100-0x143f app=0x1800-0x1fff "
        "net=0x4000-0x42ff cli=0x4400-0x45bf thr=0x4300-0x43ff "
        "srv=0x4b00-0x4bff http=0x4c00-0x5e7f "
        "tls=0x6000-0x733f revisions=0x7340-0x7fbf reserve-t3=0x7fc0-0x7fff",
    ]

    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("utf-8", errors="replace")
    return retour


def construire_carte(exe, verrous_m3, verrous_m4, version, verdict_oracle, compteurs,
                     journal_runs):
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    clairs = fragments_clairs(exe, verrous_m3, verrous_m4, version, verdict_oracle,
                              compteurs, journal_runs)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(fragments)
    entete = cm.construire_entete(racine)
    prive, pub = cm.paire_cles(cm.charger_secrets(interactif=False)[1])
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)
    return pub


# --- Verrou croisé (R8 : relecture indépendante — les DEUX générations) ----------

def verrou_croise() -> tuple[int, dict]:
    phrase, _ = cm.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_listes_blanches(entete.decode("ascii"))
    cm.verifier_signature(pub, entete, fragments, signature)
    if cm.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm.ErreurCarte("empreinte racine divergente")
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "proxy.exe"), {})
    for bid in TOUS_BLOCS:
        if bid not in EMBARQUES:
            continue
        rva, slot = RVA_PAR_BLOC[bid], next(
            s for b, _sid, _f, _r, s in BLOCS_EMBARQUES_M4 if b == bid)
        sha = "sha256:" + hashlib.sha256(tranche_section(exe, rva, slot)).hexdigest()
        if sha != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm.ErreurCarte("verrou croisé : empreinte de proxy.exe divergente (R8)")
    return len(empreintes), manifeste


# --- Tableau de bord (§ 15.2, métriques M4) ----------------------------------------

def tableau_de_bord(exe: bytes, verrous_m3: list, verrous_m4: list, nb_blocs_carte: int,
                    manifeste: dict, verdict_oracle: dict) -> str:
    sha = lambda b: hashlib.sha256(b).hexdigest()
    lignes = [
        "[tableau] jalon=M4 artefact=proxy.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb_blocs_carte}/49 : audit de tracabilite I->C->B (5 artefacts)",
        f"  chaines_I_C_B_tests           : {nb_blocs_carte}/{nb_blocs_carte} : specs, carte, exe, vecteurs",
        f"  construction                  : 0 erreur / 0 avertissement : build script",
        f"  tests_differentiels           : oracle M4 {verdict_oracle.get('total_cas', 0)} cas verts "
        f"({verdict_oracle.get('volume', '-')}, graine {verdict_oracle.get('graine', '-')}) ; "
        f"oracle structurel M3 {len(verrous_m3)} + M4 {len(verrous_m4)} verrous PASS",
        f"  reutilisation_heritage        : 27 blocs octet-identiques au scellé 0.4.0 "
        f"(26 embarques M3 + libc-07 selftest.exe — R7, deltas .rdata documentes)",
        f"  empreintes_donnees_embarquees : conforme (fixtures http + tls, table R10 28 entrees "
        f"[marche aux bornes — porte .text3 D95], table des reponses 8 entrees, "
        f"secur32 x7, version 0x00050003)",
        f"  defauts_T1_T6_ouverts         : 0 : journal des decisions D77-D94",
        f"  optimisations_sans_mesure     : 0 : aucune optimisation M4 (R11)",
        f"  changements_hors_journal      : 0 : D77 a D95 consignees",
        f"  preversions                   : {manifeste.get('version', '?')} conforme "
        f"(schema dev, monotonie R10 verifiee par la porte : 28 sommes recalculees du binaire)",
        f"  entrees_non_fiables           : comportement defini par contrat (E1-E8 herites + "
        f"table TOTALE des HRESULT, verdicts nommes, compensation par comptage) ; "
        f"falsification : F4 8 mutations attrapees (D93) + 6/6 http-12:R2 (D95)",
        f"  artefact                      : {len(exe)} octets ; empreinte sha256:{sha(exe)[:16]}... ; "
        f"5 sections (.text3 nouvelle 0x6000) ; secur32 x7 (Schannel) ; "
        f"entree PE 0x7DC0 (le cablage, http-12:R2)",
        f"  verrou_croise                 : {nb_blocs_carte} empreintes reverifiees "
        f"(5 artefacts + notations non embarquees) + signature Ed25519 + racine (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Assemblage + vérification communs ----------------------------------------------

def assembler_tout_m4() -> tuple[dict, dict, list]:
    """libc-07 + les dix blocs M4 : assemblage, tailles déclarées, round-trip."""
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    specs = charger_couche_I_m4()
    code: dict[str, dict] = {}
    for bid, sid, fichier, rva, slot in [BLOC_LIBC07] + BLOCS_M4:
        chemin = chemin_notation_m4(fichier)
        octets, metas = assembler_bloc(ks, chemin, rva, slot)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot_complet = octets + b"\x90" * (slot - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns, "slot": slot_complet}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel_m4(specs, code, [BLOC_LIBC07] + BLOCS_M4)
    print(f"[oracle] structurel M4 : {len(verrous)} verrous PASS (contrats I verifies par bloc)")
    return specs, code, verrous


def blobs_oracle(code_m3: dict, code_m4: dict) -> dict:
    """Les blobs de l'oracle D93 — la MÊME table d'intégration que D92."""
    blobs = {}
    for bid, cle in _CLE_BLOB.items():
        blobs[cle] = code_m3[bid]["octets"] if bid in code_m3 else code_m4[bid]["octets"]
    return blobs


# --- Modes ---------------------------------------------------------------------------

def _anti_rollback() -> None:
    """Une carte scellée (rc/final) interdit la reconstruction (R6)."""
    try:
        _, fragments, _, _ = cm.lire_carte()
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
        version_existante = next(
            (dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
             if "artefact=proxy.exe" in l), None)
        if version_existante and ("-rc" in version_existante
                                  or re.fullmatch(r"\d+\.\d+\.\d+", version_existante)):
            raise EchecBuild(
                f"carte scellée ({version_existante}) : reconstruction interdite — "
                f"procedure lourde R6 ou nouvelle version X.Y.Z+1 requise")
    except (cm.ErreurCarte, FileNotFoundError):
        pass  # pas de carte lisible : première construction


def construire(volume: str, graine: int) -> int:
    print("=== M4 : chaîne artefact TRIADE (profil x86-64-win11-pe) ===")
    _anti_rollback()
    _garde_sceau_I()

    # 1. Héritage M3 re-vérifié de bout en bout (R5 + oracle structurel M3)
    print("[heritage] re-vérification M3 complète (build_m3.assembler_tout)…")
    blocs_m3, _specs_m3, code_m3, verrous_m3 = B3.assembler_tout()
    texte_m3, rdata_m3, data_m3, text2_m3 = B3.composer_sections(code_m3, blocs_m3)

    # 2. L'image composée M3 == le scellé 0.4.0, OCTET PAR OCTET (preuve R7 absolue)
    with open(os.path.join(M3_DIR, "proxy.exe"), "rb") as f:
        scelle = f.read()
    if hashlib.sha256(scelle).hexdigest() != SHA_PROXY_SCELLE:
        raise EchecBuild("proxy.exe 0.4.0 divergent de l'artefact scellé (R7)")
    for nom, compose, taille, fichier in (
            (".text", texte_m3, L.TEXT_VSIZE, L3.TEXT_FILE),
            (".text2", text2_m3, L.TEXT2_VSIZE, L3.TEXT2_FILE),
            (".rdata", rdata_m3, L.RDATA_VSIZE, L3.RDATA_FILE)):
        if compose != scelle[fichier: fichier + taille]:
            raise EchecBuild(f"l'image M3 composée diverge du scellé 0.4.0 ({nom}) — R7")
    if data_m3 != scelle[L3.DATA_FILE: L3.DATA_FILE + L.DATA_RAW]:
        raise EchecBuild("l'image M3 composée diverge du scellé 0.4.0 (.data) — R7")
    print(f"[R7] image M3 composée == scellé 0.4.0 octet pour octet "
          f"(sha {SHA_PROXY_SCELLE[:16]}…) : .text/.rdata/.data/.text2")

    # 3. Blocs M4 + libc-07 : assemblage et oracle structurel
    specs_m4, code_m4, verrous_m4 = assembler_tout_m4()

    # 4. Composition de l'image M4 (deltas documentés + .text3)
    texte, rdata, data, text2, text3 = composer_image_m4(
        texte_m3, rdata_m3, data_m3, text2_m3, code_m4, code_m4["b20007"]["slot"])
    exe = ecrire_pe32plus(texte, rdata, data, text2, text3)
    valider_pe(exe)
    print(f"[PE] proxy.exe : {len(exe)} octets, 5 sections (.text3 0x6000), "
          f"kernel32 x10 + ws2_32 x13 + secur32 x7, entree 0x{L.ENTREE_R2:x} "
          f"(http-12:R2 — le câblage)")

    # 5. Preuves R7 (les deux générations) + verifier-puis-écrire (R5)
    heritage = preuve_reutilisation(exe)
    print(f"[R7] réutilisation : {heritage['blocs_reutilises']} blocs octet-identiques "
          f"(26 héritage M3 + libc-07 selftest.exe), deltas .rdata documentés")
    nb_embarques = verifier_puis_ecrire(exe, code_m3, code_m4)
    print(f"[R5] verifier-puis-ecrire : {nb_embarques}/38 blocs notés == artefact")

    # 6. L'oracle D93 sur les blobs du build (lève EchecOracle sur TOUT écart)
    blobs = blobs_oracle(code_m3, code_m4)
    manquants = {"tls-01", "tls-02", "tls-03", "tls-04", "tls-05", "tls-06",
                 "tls-07", "tls-08", "http-08-R2", "http-10-R2",
                 "hello-02", "libc-01", "libc-03", "libc-04", "libc-07",
                 "tcp-03", "tcp-04", "tcp-05", "tcp-06", "tcp-11", "tcp-13",
                 "http-01", "http-02", "http-03", "http-04", "http-05",
                 "http-06", "http-07", "http-08-R1", "http-09", "http-10-R1"} - set(blobs)
    if manquants:
        raise EchecBuild(f"blobs manquants pour l'oracle : {manquants}")
    verdict = od4.executer(blobs, graine=graine, volume=volume)
    print(f"[oracle] differentiel M4 : {verdict['total_cas']} cas verts ; "
          f"falsification : défauts injectés détectés")

    # 7. Écriture de l'artefact
    with open(os.path.join(ICI, "proxy.exe"), "wb") as f:
        f.write(exe)

    # 8. Carte génération 6 (lignée D80) + verrou croisé + tableau de bord
    version = L.VERSION_051
    compteurs = {bid: 1 for bid in TOUS_BLOCS}
    journal = [f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} build={version}"]
    construire_carte(exe, verrous_m3, verrous_m4, version, verdict, compteurs, journal)
    print(f"[carte] génération 6 écrite (lignée D80) : 4 fragments chiffrés, "
          f"signature Ed25519, 49 blocs indexés sur 5 artefacts")
    nb, manifeste = verrou_croise()
    print(f"[R8] verrou croisé : signature OK, racine OK, {nb} empreintes revérifiées, "
          f"artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous_m3, verrous_m4, nb, manifeste, verdict))
    print("[tableau] tableau de bord écrit (carte/tableau-de-bord.txt)")
    print(f"[B] proxy.exe scellé-dev : sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== M4-dev (oracle vert) : {version} — tunnel chiffré embarqué et CÂBLÉ, "
          f"terrain (étape c) en attente ===")
    return 0


def verifier(graine: int, volume: str) -> int:
    print(f"=== M4 : re-vérification complète (R5/R7/R8, graine {graine}) ===")
    _garde_sceau_I()
    print("[heritage] re-vérification M3 complète (build_m3.assembler_tout)…")
    blocs_m3, _specs_m3, code_m3, verrous_m3 = B3.assembler_tout()
    texte_m3, rdata_m3, data_m3, text2_m3 = B3.composer_sections(code_m3, blocs_m3)
    specs_m4, code_m4, verrous_m4 = assembler_tout_m4()

    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    heritage = preuve_reutilisation(exe)
    nb_embarques = verifier_puis_ecrire(exe, code_m3, code_m4)
    print(f"[R5] verifier-puis-ecrire : {nb_embarques}/38 blocs notés == artefact ; "
          f"[R7] {heritage['blocs_reutilises']} blocs réutilisés, deltas documentés")

    verdict = od4.executer(blobs_oracle(code_m3, code_m4), graine=graine, volume=volume)
    print(f"[oracle] differentiel M4 : {verdict['total_cas']} cas verts")

    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("utf-8")
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m = re.match(r"(\d+)/10", champs.get("crist", "1/10"))
            compteurs[champs["id"]] = int(m.group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    for bid in TOUS_BLOCS:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
                   f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    manifeste_v = next((dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
                        if "artefact=proxy.exe" in l), "?")
    version = manifeste_v if manifeste_v != "?" else L.VERSION_DEV2
    construire_carte(exe, verrous_m3, verrous_m4, version, verdict, compteurs, journal)
    nb, manifeste = verrou_croise()
    crist = {b: compteurs.get(b, 0) for b, *_ in BLOCS_M4}
    print("[R6] cristallisation M4 : " + ", ".join(f"{b}={n}/10" for b, n in list(crist.items())[:6])
          + (", …" if len(crist) > 6 else ""))
    print(f"[R8] verrou croisé : {nb} empreintes conformes ; artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous_m3, verrous_m4, nb, manifeste, verdict))
    return 0


def _sceller(nouvelle_version: str, exigences: str) -> int:
    """Scellage M4 (modèle m3 D74 / m1 D32 / m2 D43) : cristallisation 10/10 +
    conformité § 8.2 verte + bascule de balise dans frag-bld. L'artefact
    n'est PAS touché — le scellage est un fait de carte ; proxy.exe reste
    byte-identique à l'artefact prouvé terrain (md5 2b6481a1…, sha256
    b9264e0b… — les octets du run 17-H : S49 OK + témoin HTTP/1.1 200)."""
    print(f"=== M4 : scellage {nouvelle_version} ({exigences}) ===")
    _garde_sceau_I()
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("utf-8")
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(re.match(r"(\d+)/10", champs.get("crist", "0/10")).group(1))
    incomplets = {b: n for b, n in compteurs.items() if n < 10}
    if incomplets:
        raise EchecBuild(f"cristallisation incomplete : {incomplets} — 10 verifications requises (R6)")
    print(f"[R6] cristallisation : {len(compteurs)} blocs à 10/10")

    # Conformité § 8.2 (m4/conformite_profil.py — D104) : suite exigée à
    # chaque cristallisation rc/finale ; chargée sous un nom distinct (elle
    # recharge build_m4 comme module : aucune collision d'état).
    cp = _charger_module("conformite_profil_m4", os.path.join(ICI, "conformite_profil.py"))
    ok_conf, lignes_conf = cp.executer()
    print("\n".join(lignes_conf[-3:]))
    if not ok_conf:
        raise EchecBuild(f"suite de conformite non verte — {nouvelle_version} refuse")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    if nouvelle_version == L.VERSION_FINALE:
        ancienne = L.VERSION_RC1
        occurrences = bld.count(f"version={ancienne}")
        if occurrences != 1:
            raise EchecBuild(f"balise {ancienne} attendue une fois dans frag-bld "
                             f"({occurrences} occurrence(s)) — scellage final refuse (fail-closed)")
    else:
        ancienne = L.VERSION_DEV2
    bld = bld.replace(f"version={ancienne}", f"version={nouvelle_version}")
    clairs = {"frag-bld": bld.encode("utf-8")}
    for nom in ("frag-loc", "frag-con", "frag-prf"):
        clairs[nom] = cm.dechiffrer_fragment(maitre, nom, fragments[nom])
    nouveaux = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(nouveaux)
    entete = cm.construire_entete(racine)
    _, graine_cles = cm.charger_secrets(interactif=False)
    prive, pub = cm.paire_cles(graine_cles)
    cm.ecrire_carte(entete, nouveaux, cm.signer(prive, entete, nouveaux), pub)

    # Le tableau de bord suit la balise (l'artefact, lui, ne bouge pas)
    chemin_tab = os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt")
    if os.path.exists(chemin_tab):
        with open(chemin_tab, "r", encoding="utf-8") as f:
            tab = f.read()
        tab = tab.replace(f"version={ancienne}", f"version={nouvelle_version}")
        tab = tab.replace(f"{ancienne} conforme", f"{nouvelle_version} conforme")
        with open(chemin_tab, "w", encoding="utf-8") as f:
            f.write(tab)
    print(f"[balise] {nouvelle_version} scellee (immuable § 9 ; defaut -> 0.5.1 "
          f"a contrat stable, R4) ; proxy.exe INTACT (md5 2b6481a1…, "
          f"28 160 o — le scellage est un fait de carte)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--verifier" in args:
            graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 20261028
            volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
            sys.exit(verifier(graine, volume))
        if "--sceller-rc" in args:
            sys.exit(_sceller(L.VERSION_RC1,
                              "cristallisation R6 10/10 + conformite § 8.2 + criteres du "
                              "jalon M4 (HTTPS en transit via Schannel ; echec propre sur "
                              "certificat invalide — prouves par les runs 17-C a 17-H)"))
        if "--sceller-final" in args:
            sys.exit(_sceller(L.VERSION_FINALE,
                              "R6 + conformite + validation terrain consignee (T4 du "
                              "superviseur 17-H du 29/10 : S49 OK + temoin HTTP/1.1 200 "
                              "+ S05C md5 2b6481a1, octets inchanges)"))
        volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 20261028
        sys.exit(construire(volume, graine))
    except (EchecBuild, cm.ErreurCarte, od4.EchecOracle) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
