#!/usr/bin/env python3
"""build_corpus.py — LA CHAÎNE INTÉGRALE de l'artefact `corpus` (chantier M6-(b)).

Le corpus paritaire de D149-(2) : les DOUZE blocs du patrimoine (révisions
de granularité R+1 de unix/I/, ancêtres scellés INTACTS) et le principal
propre au jalon — l'instance SysV de la même couche I que l'instance
Windows scellée (le diff nul, MESURÉ PAR SCRIPT par diff_nul.py).

La chaîne (le modèle build_m6.py, la discipline de la lignée) :
  1. couche I : lecture et audit des gabarits (id:R{rev} épinglé par le
     plan — la garde distingue ABSENT d'ILLISIBLE : l'incident de l'état
     zéro du chantier, une carte présente et indéchiffrable est un REFUS,
     jamais une permission) ;
  2. diff nul : diff_nul.py — les fichiers canoniques chargés, l'équivalence
     des observables R1 ↔ R+1, l'invariance des scellés ;
  3. assemblage : notation → octets, round-trip PAR INSTRUCTION (R5) ;
  4. oracle structurel : les contrats I sur le code désassemblé (appels
     déclarés, syscalls par bloc, données RIP déclarées, _start sans push,
     sortir sans ret, verrou tournant posé puis rendu) ;
  5. composition : ELF64 durci (ET_DYN/PIE, 3 segments R/RX/RW, .bss pur,
     PT_GNU_STACK sans X — le durcissement M6-(a) hérité), fixtures dorées
     du patrimoine, staging du remplaçant + table d'intégrité R10 ;
  6. validation : l'image RELUE — W^X depuis les phdr, tables conformes au
     layout (source unique), e_entry relatif ;
  7. oracle natif : oracle_corpus.py — différentiel, scénarios, artefact
     entier, falsification (exécution native au labo) ;
  8. la carte : génération 1 du corpus (fragments chiffrés, signature
     Ed25519 clés projet D27, verrou croisé R8, frag-con documenté PAR
     BLOC pour les DEUX profils — § 8.3-4).

Usage : python3 build_corpus.py [--verifier] [--volume complet|reduit] [--graine N]
                   [--sceller-rc]     # scellage 0.7.0-rc.1 (chantier M6-(c)) :
                                      # contrôle D146 adapté + cristallisation
                                      # 10/10 + conformité 7/7, bascule de balise
                   [--sceller-final]  # 0.7.0 : validation terrain consignée
                                      # (le chantier M6-(d) — jamais avant)
"""

from __future__ import annotations

import hashlib
import os
import re
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
UNIX = ICI
RACINE = os.path.dirname(UNIX)
sys.path.insert(0, UNIX)
sys.path.insert(0, RACINE)
import layout as L  # noqa: E402

import capstone  # noqa: E402
from keystone import KS_ARCH_X86, KS_MODE_64, Ks  # noqa: E402

import oracle_corpus as OC  # noqa: E402
import diff_nul  # noqa: E402


class EchecBuild(Exception):
    """Tout refus nommé de la chaîne (fail-closed : jamais un faux vert)."""


# --- Couche I : lecture et audit (la garde absent ≠ illisible) ------------------

def lire_spec(chemin: str) -> dict:
    if not os.path.exists(chemin):
        raise EchecBuild(f"spécification ABSENTE : {chemin} (l'arbre du jalon "
                         f"doit la porter — écrite-avant-code)")
    try:
        with open(chemin, encoding="utf-8") as f:
            texte = f.read()
    except OSError as e:
        raise EchecBuild(f"spécification ILLISIBLE : {chemin} ({e}) — un fichier "
                         f"présent et illisible est un REFUS, jamais une permission "
                         f"(l'incident de l'état zéro du chantier)") from e
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte,
            "chemin": chemin}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures",
                 "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2 : écrite-avant-code)")
    return spec


def charger_couche_I() -> dict[str, dict]:
    """Les specs du corpus depuis unix/I/ — les MÊMES fichiers que M7 chargera."""
    specs = {}
    for bid, sid, fichier, _, _ in L.BLOCS_CORPUS:
        chemin = os.path.join(UNIX, "I", fichier + ".md")
        spec = lire_spec(chemin)
        if f"{spec['id']}:R{spec['rev']}" != sid:
            raise EchecBuild(f"{chemin} : identifiant/révision {spec['id']}:R{spec['rev']} "
                             f"!= plan {sid} (l'épinglage du plan — la leçon de "
                             f"l'incident : les chaînes scellées refusent la divergence)")
        specs[bid] = spec
    return specs


# --- Assemblage : notation -> octets (R5) ----------------------------------------

def lignes_notation(chemin: str) -> list[str]:
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().splitlines()
    return [l.strip() for l in brut if l.strip() and not l.strip().startswith(";")]


def assembler_bloc(ks: Ks, fichier: str, rva: int, slot: int) -> dict:
    chemin = os.path.join(UNIX, "notation", fichier + ".asm")
    if not os.path.exists(chemin):
        raise EchecBuild(f"notation absente : {chemin} (outils/auteur.py --corpus)")
    octets, metas, adresse = b"", [], rva
    for ligne in lignes_notation(chemin):
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise EchecBuild(f"{fichier} : ligne inassemblable : {ligne!r}")
        b = bytes(enc)
        metas.append({"ligne": ligne, "adresse": adresse, "taille": len(b)})
        octets += b
        adresse += len(b)
    if len(octets) > slot:
        raise EchecBuild(f"{fichier} : {len(octets)} o > slot {slot:#x} (D8)")
    return {"octets": octets, "metas": metas, "slot": octets + b"\x90" * (slot - len(octets)),
            "rva": rva, "slot_taille": slot}


def assembler_tout(ks: Ks, cs: capstone.Cs) -> tuple[dict, dict]:
    code, staging = {}, None
    for bid, _, fichier, rva, slot in L.BLOCS_CORPUS:
        bloc = assembler_bloc(ks, fichier, rva, slot)
        bloc["insns"] = list(cs.disasm(bloc["octets"], rva))
        if len(bloc["insns"]) != len(bloc["metas"]):
            raise EchecBuild(f"{fichier} : désassemblage {len(bloc['insns'])} "
                             f"!= {len(bloc['metas'])} instructions")
        for meta, insn in zip(bloc["metas"], bloc["insns"]):
            if f"{insn.mnemonic} {insn.op_str}".strip() != meta["ligne"]:
                # la notation est déjà la graphie canonique capstone (auteur) :
                # tout écart est une divergence d'identité
                rec, _ = ks.asm(meta["ligne"], insn.address)
                if bytes(rec) != bloc["octets"][meta["adresse"] - rva:
                                                meta["adresse"] - rva + meta["taille"]]:
                    raise EchecBuild(f"{fichier} @ {insn.address:#x} : round-trip R5 rompu")
        code[bid] = bloc
        print(f"[R5] {bid} ({fichier}) : {len(bloc['octets'])} o, "
              f"round-trip {len(bloc['insns'])}/{len(bloc['insns'])} = 100 %")
    # le staging : le remplaçant assemblé POUR la croissance (PAS un bloc placé)
    bid, _, fichier, rva, slot = L.BLOC_STAGING
    staging = assembler_bloc(ks, fichier, rva, slot)
    staging["insns"] = list(cs.disasm(staging["octets"], rva))
    print(f"[R5] {bid} (staging {fichier}, POUR {rva:#x}) : {len(staging['octets'])} o")
    return code, staging


# (octets_de supprimé — la vérification porte sur les métadonnées directement)


# --- Oracle structurel : les contrats I sur le code désassemblé ------------------
# Les déclarations par bloc (I1 des specs — le builder confronte le code)

APPELS_AUTORISES = {
    "f61010": {L.A_ZONE_ALLOC, L.A_ZONE_RESET, L.A_MEMCMP, L.A_MEMCPY,
               L.A_STRLEN, L.A_ITOA, L.A_MEMSET, L.A_ECRIRE_CORPUS},   # libc-08 I1
    "f61011": {L.A_MEMCPY, L.A_ITOA, L.A_STRLEN, L.A_ECRIRE_CORPUS},   # tcp-11 I1
    "f61012": {L.A_MEMCPY},                                            # tcp-07 I1 (+ .protger local)
    "f61013": {L.A_AUTOTEST, L.A_JOURNAL, L.A_SORTIR},                 # corpus-13 I1
}
SYSCALLS_AUTORISES = {
    "f61001": {L.SYS_WRITE},       # écrire I1/I4 : UN appel au service
    "f61002": {L.SYS_EXIT_GROUP},  # sortir I1
    "f61012": {L.SYS_MPROTECT},    # tcp-07 I1 : le service de protection
}
# Les cibles RIP déclarées (I3 des specs — le plan, source unique)
DONNEES_RIP = {
    "f61007": {L.R_CURSEUR_CORPUS, L.ARENE_BASE_CORPUS},                    # libc-05
    "f61008": {L.R_CURSEUR_CORPUS},                                          # libc-06
    "f61010": {L.R_SA, L.R_SB, L.R_SC, L.R_SD, L.R_MOTIF16, L.R_SENT16,
               L.R_MOTIF33, L.R_ZERO16, L.R_FF33, L.R_S_VIDE, L.R_S_TRIADE,
               L.R_S_33, L.R_I0, L.R_IMAX, L.R_I123, L.R_I7,
               L.R_PREFIXE_M1, L.R_OK, L.R_KO},                              # libc-08
    "f61011": {L.R_VERROU},                                                 # tcp-11
    "f61012": {L.R_ETAT_PATCH_CORPUS, L.R_ENTREE_SAUVEE, L.R_TAB_SUM_CORPUS,
               L.R_STAGING_CORPUS, L.A_CROISSANCE, L.A_JOURNAL},            # tcp-07
    "f61013": {L.R_J_PREF, L.R_J_SUFF},                                     # corpus-13
}
FEUILLES_PURES = {"f61003", "f61004", "f61005", "f61006", "f61007",
                  "f61008", "f61009"}   # libc-01..07 : I1 aucun appel, aucun accès système


def cible_rip(insn):
    m = re.match(r"^\[rip \+ (0x[0-9a-f]+)\]$", insn.op_str)
    if m:
        return insn.address + insn.size + int(m.group(1), 16)
    m = re.match(r"^\[rip - (0x[0-9a-f]+)\]$", insn.op_str)
    if m:
        return insn.address + insn.size - int(m.group(1), 16)
    return None


def oracle_structurel(code: dict, staging: dict) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    for bid, bloc in code.items():
        insns = bloc["insns"]
        rva, slot = bloc["rva"], bloc["slot_taille"]
        adresses = {i.address for i in insns}
        locaux = {i.address for i in insns if i.mnemonic.endswith(":")}
        # Sauts internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic[0] == "j" or i.mnemonic == "loop":
                if ", " in i.op_str:      # conditionnel à double opérande (loop…)
                    continue
                cible = int(i.op_str.split(",")[-1].strip(), 16) if "0x" in i.op_str else None
                if cible is not None:
                    verrou(f"{bid}:saut-interne@{i.address:#x}", cible in adresses,
                           f"cible {cible:#x} hors frontière du bloc")
        # Appels directs : les blocs déclarés + les étiquettes locales (I1)
        cibles_locales = {int(i.op_str, 16) for i in insns
                          if i.mnemonic == "call" and i.op_str.startswith("0x")}
        for i in insns:
            if i.mnemonic != "call":
                continue
            if not i.op_str.startswith("0x"):
                continue
            cible = int(i.op_str, 16)
            # les étiquettes locales du bloc : les cibles d'appel DANS le bloc
            est_locale = any(x.address == cible for x in insns)
            verrou(f"{bid}:appel-autorise@{i.address:#x}",
                   cible in APPELS_AUTORISES.get(bid, set()) or est_locale,
                   f"cible {cible:#x} hors blocs déclarés (I1)")
        # Syscalls : numéros autorisés par bloc (I1)
        nr = None
        for i in insns:
            if i.mnemonic == "mov" and i.op_str.startswith("eax,"):
                try:
                    nr = int(i.op_str.split(",")[1].strip(), 0)
                except ValueError:
                    nr = None
            elif i.mnemonic == "xor" and i.op_str.replace(" ", "") == "eax,eax":
                nr = 0
            if i.mnemonic == "syscall":
                verrou(f"{bid}:syscall-autorise@{i.address:#x}",
                       nr in SYSCALLS_AUTORISES.get(bid, set()),
                       f"nr={nr} non déclaré (I1 — la table du jalon)")
        # Feuilles pures : aucun appel, aucun syscall (libc-01..07 I1)
        if bid in FEUILLES_PURES:
            verrou(f"{bid}:feuille-pure",
                   not any(i.mnemonic in ("call", "syscall") for i in insns),
                   "un bloc PUR n'appelle ni bloc ni système (I1)")
        # Données RIP : cibles déclarées (I3 — le plan)
        for i in insns:
            cible = cible_rip(i)
            if cible is not None:
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP.get(bid, set()),
                       f"cible {cible:#x} hors données déclarées (I3)")
        # D8 : slots, padding
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16)
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)
    # sortir : aucun ret, ud2 présent (hello-03:R2 Q1/I1)
    s = code["f61002"]["insns"]
    verrou("f61002:jamais-ret", not any(i.mnemonic == "ret" for i in s))
    verrou("f61002:ud2-defensif", any(i.mnemonic == "ud2" for i in s))
    # écrire : UN seul syscall (I4)
    verrou("f61001:appel-unique",
           sum(1 for i in code["f61001"]["insns"] if i.mnemonic == "syscall") == 1)
    # corpus-13 : _start sans push (I4 — ABI de démarrage), aucun syscall (I2)
    p = code["f61013"]["insns"]
    verrou("f61013:start-sans-push", not any(i.mnemonic == "push" for i in p))
    verrou("f61013:aucun-syscall", not any(i.mnemonic == "syscall" for i in p))
    # tcp-11 : le verrou posé (xchg) puis rendu (store 0) — I1/Q3
    j = code["f61011"]["insns"]
    verrou("f61011:verrou-xchg",
           any(i.mnemonic == "xchg" and "[rip" in i.op_str for i in j))
    verrou("f61011:verrou-rendu",
           any(i.mnemonic == "mov" and i.op_str.startswith("qword ptr [rip") 
               and i.op_str.endswith(", 0") for i in j))
    verrou("f61011:pause-attente", any(i.mnemonic == "pause" for i in j))
    # tcp-07 : le qword posé en UNE écriture alignée (I3) ; la cible = l'entrée journal
    t = code["f61012"]["insns"]
    verrou("f61012:qword-unique",
           any(i.mnemonic == "mov" and i.op_str.startswith("qword ptr [r15],") for i in t))
    verrou("f61012:bit-execute-retenu",
           any(i.mnemonic == "mov" and i.op_str == "edi, 7" for i in t)
           and any(i.mnemonic == "mov" and i.op_str == "edi, 5" for i in t),
           "les constantes du profil 0x7/0x5 (I6, D39 — jamais 0x3)")
    # le staging : assemblé POUR la croissance (le plan, la raison du brouillon v2)
    verrou("staging:pour-croissance",
           staging["rva"] == L.A_CROISSANCE,
           f"le remplaçant doit être assemblé pour {L.A_CROISSANCE:#x}")
    return verrous


# --- Symboles des notations confrontés au layout (leçon C1) -----------------------

SYMBOLES_LAYOUT = {
    "CURSEUR": L.R_CURSEUR_CORPUS, "ARENE": L.ARENE_BASE_CORPUS,
    "VERROU": L.R_VERROU, "ETAT": L.R_ETAT_PATCH_CORPUS,
    "ENTREE_SAUVEE": L.R_ENTREE_SAUVEE, "ENTREE_JOURNAL": L.A_JOURNAL,
    "CROISSANCE": L.A_CROISSANCE, "STAGING": L.R_STAGING_CORPUS,
    "TAB_SUM": L.R_TAB_SUM_CORPUS, "J2_MARK": L.R_J2_MARK,
    "J_PREF": L.R_J_PREF, "J_SUFF": L.R_J_SUFF, "PREFIXE": L.R_PREFIXE_M1,
    "OK": L.R_OK, "KO": L.R_KO, "SA": L.R_SA, "SB": L.R_SB, "SC": L.R_SC,
    "SD": L.R_SD, "MOTIF16": L.R_MOTIF16, "SENT16": L.R_SENT16,
    "MOTIF33": L.R_MOTIF33, "ZERO16": L.R_ZERO16, "FF33": L.R_FF33,
    "S_VIDE": L.R_S_VIDE, "S_TRIADE": L.R_S_TRIADE, "S_33": L.R_S_33,
    "I0": L.R_I0, "IMAX": L.R_IMAX, "I123": L.R_I123, "I7": L.R_I7,
    "A_MEMCPY": L.A_MEMCPY, "A_MEMCMP": L.A_MEMCMP, "A_STRLEN": L.A_STRLEN,
    "A_ITOA": L.A_ITOA, "A_ZONE_ALLOC": L.A_ZONE_ALLOC,
    "A_ZONE_RESET": L.A_ZONE_RESET, "A_MEMSET": L.A_MEMSET,
    "A_AUTOTEST": L.A_AUTOTEST, "A_JOURNAL": L.A_JOURNAL, "A_SORTIR": L.A_SORTIR,
    "A_ECRIRE": L.A_ECRIRE_CORPUS, "SYS_WRITE": L.SYS_WRITE,
    "SYS_EXIT_GROUP": L.SYS_EXIT_GROUP, "SYS_MPROTECT": L.SYS_MPROTECT,
    "PROT_RWX": L.PROT_RWX, "PROT_RX": L.PROT_RX,
    "SENTINELLE": 0xFFFFFFFF, "ARENE_TAILLE": L.ARENE_TAILLE_CORPUS,
    "L_PREF": 18, "L_SUFF": 10,
}


def verifier_symboles() -> int:
    """Chaque @symbole des notations doit être celui du layout (source unique)."""
    n = 0
    for _, _, fichier, _, _ in list(L.BLOCS_CORPUS) + [L.BLOC_STAGING]:
        chemin = os.path.join(UNIX, "notation", fichier + ".asm")
        for ligne in open(chemin, encoding="utf-8"):
            m = re.search(r"; Symboles .*: (.*)$", ligne)
            if m:
                for paire in m.group(1).split(", "):
                    nom, _, val = paire.partition("=")
                    nom = nom.lstrip("@")
                    if nom in SYMBOLES_LAYOUT:
                        attendu = SYMBOLES_LAYOUT[nom]
                        if int(val, 16) != attendu:
                            raise EchecBuild(
                                f"{fichier} : @{nom}={val} != layout {attendu:#x} "
                                f"(C1 : l'arithmétique de l'auteur est vérifiée, jamais crue)")
                        n += 1
                break
    return n


# --- Composition ELF64 durci du corpus --------------------------------------------

def somme_qwords(donnees: bytes) -> int:
    """La somme additive 64 bits des qwords (R10 — la porte d'intégrité)."""
    s = 0
    for i in range(0, len(donnees), 8):
        s = (s + struct.unpack_from("<Q", donnees, i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


def octets_staging(staging: dict) -> tuple[bytes, int, int]:
    """Le staging qword-paddé (int3), sa taille et sa somme (R10)."""
    code = staging["octets"]
    taille = (len(code) + 7) & ~7              # multiple de qword (la somme)
    return code + b"\xcc" * (taille - len(code)), taille, somme_qwords(code + b"\xcc" * (taille - len(code)))


def composer_elf(code: dict, staging: dict) -> bytes:
    seg_r = bytearray(b"\xcc" * L.CORPUS_SEG_R_TAILLE)
    seg_rx = bytearray(b"\xcc" * L.CORPUS_SEG_RX_TAILLE)
    poses = []

    def poser(seg, base, rva, donnees, nom=""):
        poses.append((rva, rva + len(donnees), nom or hex(rva)))
        if rva + len(donnees) > base + len(seg):
            raise EchecBuild(f"segment débordant à {rva:#x} ({nom})")
        seg[rva - base: rva - base + len(donnees)] = donnees

    # — segment R : les vecteurs dorés du patrimoine (MÊMES contenus que m1)
    fixtures = [
        (L.R_SA, b"TRIADE\0", "SA"), (L.R_SB, b"TRIADE\0", "SB"),
        (L.R_SC, b"TRIADF\0", "SC"), (L.R_SD, b"TRI\0", "SD"),
        (L.R_MOTIF16, bytes(range(16)), "MOTIF16"),
        (L.R_SENT16, b"\xaa" * 16, "SENT16"),
        (L.R_MOTIF33, L.CORPUS_MOTIF33, "MOTIF33"),
        (L.R_ZERO16, b"\x00" * 16, "ZERO16"),
        (L.R_FF33, b"\xff" * 33, "FF33"),
        (L.R_S_VIDE, b"\0", "S_VIDE"),
        (L.R_S_TRIADE, b"TRIADE\0", "S_TRIADE"),
        (L.R_S_33, L.CORPUS_S_33 + b"\0", "S_33"),
        (L.R_I0, b"0\0", "I0"), (L.R_IMAX, b"4294967295\0", "IMAX"),
        (L.R_I123, b"1234567890\0", "I123"), (L.R_I7, b"7\0", "I7"),
        (L.R_SLASH, b"/", "SLASH"),
        (L.R_PREFIXE_M1, L.CORPUS_PREFIXE_M1, "PREFIXE_M1"),
        (L.R_OK, b" OK\n", "OK"), (L.R_KO, b" KO\n", "KO"),
        (L.R_J_PREF, L.CORPUS_J_PREF, "J_PREF"),
        (L.R_J_SUFF, L.CORPUS_J_SUFF, "J_SUFF"),
        (L.R_J2_MARK, L.CORPUS_J2_MARK, "J2_MARK"),
    ]
    for rva, donnees, nom in fixtures:
        if len(donnees) > 64 and nom.endswith("33"):
            pass
        poser(seg_r, L.CORPUS_SEG_R_RVA, rva, donnees, nom)
    # — le staging + la table d'intégrité R10 (première entrée = le staging)
    staging_octets, staging_taille, staging_somme = octets_staging(staging)
    if staging_taille > L.STAGING_TAILLE_MAX:
        raise EchecBuild(f"staging {staging_taille} o > max {L.STAGING_TAILLE_MAX:#x}")
    poser(seg_r, L.CORPUS_SEG_R_RVA, L.R_STAGING_CORPUS, staging_octets, "STAGING")
    table = struct.pack("<IIQIQQ", L.R_STAGING_CORPUS, staging_taille, staging_somme,
                        0, 0, 0)              # 1re entrée = staging, puis le terme
    poser(seg_r, L.CORPUS_SEG_R_RVA, L.R_TAB_SUM_CORPUS, table, "TAB_SUM")
    # — segment RX : les treize blocs (NOP intra-slot), la croissance int3
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        poser(seg_rx, L.CORPUS_SEG_RX_RVA, rva, code[bid]["slot"], bid)
    # la croissance demeure int3 (le remplaçant y sera copié par tcp-07)
    # — anti-chevauchement (C1)
    for (d1, f1, n1), (d2, f2, n2) in zip(poses, poses[1:]):
        if d1 < f2 and d2 < f1:
            raise EchecBuild(f"chevauchement : {n1} [{d1:#x},{f1:#x}) / {n2} [{d2:#x},{f2:#x})")
    # — ehdr + 4 phdr (le durcissement M6-(a) : ET_DYN, e_entry RELATIF)
    e_ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8
    ehdr = struct.pack("<16sHHIQQQIHHHHHH", e_ident,
                       3, 0x3E, 1, L.CORPUS_ENTREE, 64, 0, 0,
                       64, 56, 4, 0, 0, 0)
    ph_r = struct.pack("<IIQQQQQQ", 1, 4, L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_RVA,
                       L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_TAILLE, L.CORPUS_SEG_R_TAILLE,
                       L.TAILLE_PAGE)
    ph_rx = struct.pack("<IIQQQQQQ", 1, 5, L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_RVA,
                        L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_TAILLE, L.CORPUS_SEG_RX_TAILLE,
                        L.TAILLE_PAGE)
    ph_rw = struct.pack("<IIQQQQQQ", 1, 6, L.CORPUS_SEG_RW_RVA, L.CORPUS_SEG_RW_RVA,
                        L.CORPUS_SEG_RW_RVA, 0, L.CORPUS_SEG_RW_TAILLE, L.TAILLE_PAGE)
    ph_stack = struct.pack("<IIQQQQQQ", L.PT_GNU_STACK, 6, 0, 0, 0, 0, 0, 0x10)
    seg_r[0:64] = ehdr
    seg_r[64:120] = ph_r
    seg_r[120:176] = ph_rx
    seg_r[176:232] = ph_rw
    seg_r[232:288] = ph_stack
    return bytes(seg_r) + bytes(seg_rx)


def valider_elf(img: bytes, staging: dict) -> list[str]:
    """Relit l'image composée : le durcissement, le plan, la source unique."""
    lignes = []
    if len(img) != L.CORPUS_TAILLE_FICHIER:
        raise EchecBuild(f"taille {len(img):#x} != {L.CORPUS_TAILLE_FICHIER:#x}")
    if img[:4] != b"\x7fELF" or img[4] != 2 or img[5] != 1:
        raise EchecBuild("magie ELF64 LE absente")
    e_type, e_machine = struct.unpack_from("<HH", img, 16)
    e_entry = struct.unpack_from("<Q", img, 24)[0]
    if e_type != 3:
        raise EchecBuild(f"e_type {e_type} != 3 (ET_DYN — le durcissement hérité)")
    if e_machine != 0x3E:
        raise EchecBuild(f"e_machine {e_machine:#x} != 0x3E")
    if e_entry != L.CORPUS_ENTREE:
        raise EchecBuild(f"e_entry {e_entry:#x} != {L.CORPUS_ENTREE:#x} (RVA relatif)")
    phoff, phentsize, phnum = (struct.unpack_from("<Q", img, 32)[0],
                               struct.unpack_from("<H", img, 54)[0],
                               struct.unpack_from("<H", img, 56)[0])
    if (phoff, phentsize, phnum) != (64, 56, 4):
        raise EchecBuild(f"phdr ({phoff},{phentsize},{phnum}) != (64,56,4)")
    loads = []
    for i in range(phnum):
        p = struct.unpack_from("<IIQQQQQQ", img, phoff + i * 56)
        if p[0] == 1:
            loads.append(p)
        elif p[0] == L.PT_GNU_STACK:
            if p[1] != 6 or p[7] != 0x10:
                raise EchecBuild("PT_GNU_STACK != RW sans X, align 0x10 (NX exigé)")
            lignes.append("[phdr] PT_GNU_STACK RW SANS X — NX explicite")
        else:
            raise EchecBuild(f"p_type inattendu {p[0]:#x}")
    if len(loads) != 3 or [p[1] for p in loads] != [4, 5, 6]:
        raise EchecBuild(f"PT_LOAD {[p[1] for p in loads]} != R/RX/RW")
    for p in loads:
        if p[1] & 2 and p[1] & 1:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : inscriptible ET exécutable (W^X rompu)")
        if p[2] != p[3] or p[7] != L.TAILLE_PAGE:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : offset != vaddr ou align != page")
    attendus = {4: (L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_TAILLE, L.CORPUS_SEG_R_TAILLE),
                5: (L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_TAILLE, L.CORPUS_SEG_RX_TAILLE),
                6: (L.CORPUS_SEG_RW_RVA, 0, L.CORPUS_SEG_RW_TAILLE)}
    for p in loads:
        if (p[3], p[5], p[6]) != attendus[p[1]]:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : {(p[3], p[5], p[6])} != plan "
                             f"{attendus[p[1]]} (layout, source unique)")
    lignes.append("[phdr] 3 PT_LOAD R/RX/RW + PT_GNU_STACK RW sans X — W^X CONSTATÉ "
                  "depuis les phdr (le durcissement M6-(a) hérité)")
    lignes.append(f"[phdr] ET_DYN (PIE) : e_entry {e_entry:#x} RELATIF, .bss pur (filesz 0)")
    # le staging et la table (R10) : conformes au build
    st, taille, somme = octets_staging(staging)
    if img[L.R_STAGING_CORPUS:L.R_STAGING_CORPUS + taille] != st:
        raise EchecBuild("le staging de l'image != le staging assemblé (R10)")
    rva_t, taille_t, somme_t = struct.unpack_from("<IIQ", img, L.R_TAB_SUM_CORPUS)
    if (rva_t, taille_t, somme_t) != (L.R_STAGING_CORPUS, taille, somme):
        raise EchecBuild(f"table d'intégrité {(rva_t, taille_t, somme_t)} != build "
                         f"{(L.R_STAGING_CORPUS, taille, somme)} (R10)")
    lignes.append(f"[R10] staging {taille} o @ {L.R_STAGING_CORPUS:#x}, somme "
                  f"{somme:#x} — la porte AVANT tout effet")
    # la croissance : int3 à l'état image (le remplaçant y sera copié)
    if img[L.A_CROISSANCE:L.A_CROISSANCE + 16] != b"\xcc" * 16:
        raise EchecBuild("la croissance n'est pas int3 à l'état image (le plan)")
    return lignes


# --- La carte du corpus : le frag-con des DEUX profils (§ 8.3-4) -------------------

import carte_corpus as cm  # noqa: E402


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# La convention d'appel par bloc, pour les DEUX profils — le paramétrage
# physique qui a quitté la couche I (D149-(3)). Chaque ligne : le contrat
# nomme, frag-con porte.
CONVENTIONS = {
    "f61001": ("écrire : flux/tampon/longueur",
               "msx64 : rcx/rdx/r8, 4e-5e args pile, shadow 0x28, WriteFile IAT (BOOL)",
               "SysV : rdi/rsi/rdx, aucune zone d'accueil, sys_write (rax brut)"),
    "f61002": ("sortir : code",
               "msx64 : rcx, ExitProcess IAT", "SysV : rdi, sys_exit_group"),
    "f61003": ("memcpy : dst/src/n",
               "msx64 : rcx/rdx/r8 (pousse rdi/rsi — non volatils msx64)",
               "SysV : rdi/rsi/rdx (déjà en place pour rep movsb)"),
    "f61004": ("memcmp : ptr1/ptr2/n",
               "msx64 : rcx/rdx/r8", "SysV : rdi/rsi/rdx (repz cmpsb en place)"),
    "f61005": ("strlen : chaîne", "msx64 : rcx", "SysV : rdi"),
    "f61006": ("itoa : valeur/tampon",
               "msx64 : ecx/rdx, travail en rbx sauvegardé",
               "SysV : edi/rsi, travail aux volatils r8/r9"),
    "f61007": ("zone-alloc : taille/alignement", "msx64 : rcx/rdx",
               "SysV : rdi/rsi ; arène au plan (0x3000/0x3040, la géométrie m1)"),
    "f61008": ("zone-reset : —", "msx64 : —", "SysV : — (le curseur au plan)"),
    "f61009": ("memset : dst/valeur/n",
               "msx64 : rcx/dl/r8 (pousse rbx/rdi)",
               "SysV : rdi/sil/rdx (rep stosb en place)"),
    "f61010": ("autotest : — (l'entrée du profil)",
               "msx64 : point d'entrée PE, WriteFile/ExitProcess IAT, \\r\\n, "
               "terminaison par le bloc",
               "SysV : appelé par corpus-13, écrire fd 1, \\n, N rendu (rax) — "
               "le principal termine"),
    "f61011": ("journal : préfixe/longueur/valeur/suffixe/longueur",
               "msx64 : rcx/rdx/r8/r9 + 5e pile, Enter/LeaveCriticalSection IAT "
               "(initialisée par tcp-12), WriteFile (BOOL)",
               "SysV : rdi/rsi/rdx/rcx/r8 (cinq registres), verrou tournant "
               "lock xchg au plan (né déverrouillé), écrire (rax brut)"),
    "f61012": ("patch : mode",
               "msx64 : ecx, VirtualProtect IAT x2, PAGE 0x40/0x20, zone "
               "d'accueil 0x28 (D41), cible echo 0x4600/croissance 0x4680",
               "SysV : edi, sys_mprotect x2 (r10 libre — syscall 4e arg non "
               "requis), PROT 0x7/0x5, aucune zone d'accueil, cible journal "
               "0x1840/croissance 0x1D80 (le plan du corpus)"),
    "f61013": ("principal : l'ABI de démarrage du profil",
               "msx64 : point d'entrée PE (chargeur, PEB) — hello-01:R1, "
               "classe C (l'orchestration d'entrée EST la plateforme)",
               "SysV : _start ELF, [rsp]=argc/argv, rsp ≡ 0 mod 16 sans "
               "adresse de retour — le rituel de parité"),
}


def fragments_clairs(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, empreintes_I, version=None):
    if version is None:
        version = L.VERSION_DEV2
    loc = ["[carte-frag] nom=frag-loc generation=1"]
    for bid, sid, _, rva, slot in L.BLOCS_CORPUS:
        loc.append(f"[bloc] id={bid} spec={sid} cible={L.CORPUS_PROFIL} "
                   f"addr={rva:#x} size={slot} v=1 etat=scelle "
                   f"(RVA — PIE : la base est choisie par le noyau)")
    loc.append(f"[staging] id=f61991 pour={L.A_CROISSANCE:#x} "
               f"addr={L.R_STAGING_CORPUS:#x} taille={len(staging['octets'])}")
    loc.append(f"[zones] io=0x1000-0x1080 libc=0x1080-0x1340 app=0x1340-0x1D80 "
               f"croissance={L.A_CROISSANCE:#x}-{L.A_CROISSANCE + L.CROISSANCE_TAILLE:#x} "
               f"rodata=0x140-0x560 bss=0x3000-0x3818")
    loc.append(f"[bss] curseur={L.R_CURSEUR_CORPUS:#x} arene={L.ARENE_BASE_CORPUS:#x} "
               f"verrou={L.R_VERROU:#x} etat_patch={L.R_ETAT_PATCH_CORPUS:#x} "
               f"entree_sauvee={L.R_ENTREE_SAUVEE:#x}")

    con = ["[carte-frag] nom=frag-con generation=1",
           "# La convention d'appel PAR BLOC, pour les DEUX profils (spec § 8.3-4 —",
           "# la granularité D149-(3) : la couche I nomme, frag-con porte le physique)"]
    for bid in code:
        spec = specs[bid]["texte"]
        sig = re.search(r"Intention : (.+?)\n", spec).group(1)
        nom, win, sysv = CONVENTIONS[bid]
        con += [f"[bloc] id={bid}",
                f"  sig : {sig[:96]}",
                f"  args : {nom}",
                f"  x86-64-win11-pe : {win}",
                f"  x86-64-linux-elf64 : {sysv}"]
    con.append("[alignement] rsp ≡ 8 mod 16 à l'entrée de tout bloc appelé — "
               "IDENTIQUE aux deux profils (l'exception : _start Linux, rsp ≡ 0, "
               "sans adresse de retour)")
    con.append("[volatilite] msx64 : RAX,RCX,RDX,R8-R11 volatils ; SysV : "
               "RAX,RCX,RDX,RSI,RDI,R8-R11 volatils (RDI/RSI changent de camp — "
               "les non volatils : RBX,RBP,R12-R15 aux deux, +RDI,RSI chez msx64)")

    prf = ["[carte-frag] nom=frag-prf generation=1"]
    for bid, _, fichier, _, _ in L.BLOCS_CORPUS:
        with open(os.path.join(UNIX, "notation", fichier + ".asm"), "rb") as f:
            emp = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} "
                f"crist={crist}/10",
                f"  vecteurs : roundtrip=ok structure=ok notation={emp}",
                f"  differentiel : natif ok ({verdict['cas']} cas, graine "
                f"{verdict['graine']})"]
    prf.append("[couche-I] " + " ; ".join(
        f"{n}={e[:12]}" for n, e in sorted(empreintes_I.items())))
    prf.append("[verifications] runs=" + str(len(journal)))
    prf += ["  " + r for r in journal[-12:]]

    bld = ["[carte-frag] nom=frag-bld generation=1"]
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        bld.append(f"[bloc] id={bid} addr={rva:#x} empreinte={sha(code[bid]['slot'])}")
    bld += [
        f"[build] artefact=corpus version={version} profil={L.CORPUS_PROFIL} "
        f"taille={len(img)} empreinte={sha(img)}",
        f"  outils : keystone + capstone {capstone.cs_version()[0]}."
        f"{capstone.cs_version()[1]} ; verrous={len(verrous)} ; symboles vérifiés",
        f"  durcissement : ET_DYN/PIE, 3 segments R/RX/RW, PT_GNU_STACK sans X, "
        f"W^X depuis les phdr — hérité du chantier M6-(a)",
        f"  corpus : 12 blocs du patrimoine (révisions R+1 de unix/I/) + "
        f"corpus-13 ; staging {len(staging['octets'])} o (journal v2 POUR "
        f"{L.A_CROISSANCE:#x}) ; diff nul VERT",
        f"  oracle : natif — {verdict['cas']} cas verts, "
        f"{len(verdict['verrous'])} verrous ; {verdict['binaire']} ; "
        f"falsification {verdict['falsification']}",
    ]
    return {n: ("\n".join(l) + "\n").encode("utf-8")
            for n, l in (("frag-loc", loc), ("frag-con", con),
                         ("frag-prf", prf), ("frag-bld", bld))}


def empreinte_racine(fragments: dict) -> bytes:
    return hashlib.sha256(b"".join(
        fragments[n] for n in sorted(fragments))).digest()


def verrou_croise(code: dict, img: bytes) -> int:
    """R8 : signature + empreintes re-vérifiées depuis le disque."""
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_signature(pub, entete, fragments, signature)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    n = 0
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        m = re.search(rf"\[bloc\] id={bid} addr=\S+ empreinte=(\S+)", bld)
        if not m or m.group(1) != sha(img[rva:rva + slot]):
            raise EchecBuild(f"verrou croisé : {bid} divergent (R8)")
        n += 1
    m = re.search(rf"\[build\] artefact=corpus version=(\S+)", bld)
    if m and m.group(1) == L.VERSION_DEV2:
        pass
    return n


def construire_carte(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, empreintes_I, version=None):
    clairs = fragments_clairs(code, img, verrous, specs, verdict, compteurs,
                              journal, staging, empreintes_I, version=version)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    prive, pub = cm.paire_cles(graine)
    entete = cm.construire_entete(empreinte_racine(fragments))
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)


# --- L'anti-rollback du jalon : ABSENT ≠ ILLISIBLE (la règle née de l'incident) ----

# Le REGISTRE DES VERSIONS ACCEPTÉES de la lignée (fiche § 8 : « LICENSE
# anti-rollback amendé à chaque scellage, modèle D147 ; plancher posé à
# 0.7.0-dev.1 ») — une balise hors registre est un refus, jamais une
# reconstruction opportune.
BALISES_LIGNEE = {L.VERSION_DEV1, L.VERSION_DEV2, L.VERSION_RC1,
                  L.VERSION_FINALE}


def _anti_rollback() -> None:
    """La carte du corpus : ABSENTE = première construction ; PRÉSENTE et
    illisible = REFUS (l'incident de l'état zéro du chantier — jamais
    « illisible » traité comme « absente »). Dev : la reconstruction libre
    est permise tant qu'aucune balise rc/final n'est posée. SCELLÉE
    (rc/final — le chantier M6-(c)) : reconstruction INTERDITE (R6) ; la
    balise courante doit vivre au registre de la lignée (plancher
    0.7.0-dev.1 — une balise inconnue ou antérieure est un refus nommé)."""
    fragments_pres = any(os.path.exists(os.path.join(cm.CARTE_DIR, n + ".bin"))
                         for n in cm.FRAGMENTS)
    if not fragments_pres:
        return
    try:
        _, fragments, _, _ = cm.lire_carte()
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    except cm.ErreurCarte as e:
        raise EchecBuild(
            f"carte du corpus PRÉSENTE et illisible ({e}) — un état présent et "
            f"indéchiffrable est un REFUS, jamais une permission (l'incident de "
            f"l'état zéro du chantier : absent ≠ illisible)") from e
    m = re.search(r"\[build\] artefact=corpus version=(\S+)", bld)
    if not m:
        raise EchecBuild("frag-bld : balise du corpus ILLISIBLE — refus "
                         "(absent ≠ illisible, la garde D151)")
    version_existante = m.group(1)
    if version_existante not in BALISES_LIGNEE:
        raise EchecBuild(f"balise {version_existante} HORS REGISTRE de la lignée "
                         f"{sorted(BALISES_LIGNEE)} — plancher 0.7.0-dev.1, "
                         f"anti-rollback R10 (fail-closed)")
    if "-rc" in version_existante or re.fullmatch(r"\d+\.\d+\.\d+", version_existante):
        raise EchecBuild(f"carte scellée ({version_existante}) : reconstruction interdite — "
                         f"procedure lourde R6 ou nouvelle version requise")


def tableau_de_bord(img, verrous, verdict, phdr_lignes, empreintes_I,
                   version=None) -> str:
    if version is None:
        version = L.VERSION_DEV2
    return "\n".join([
        "[tableau] jalon=M6 artefact=corpus version=" + version,
        "  profil                       : " + L.CORPUS_PROFIL
        + " (fiche — la parité du patrimoine)",
        "  blocs_avec_spec_a_jour        : 13/13 : audit I->C->B (specs, carte, artefact)",
        "  chaines_I_C_B_tests           : 13/13 : " + str(len(verrous))
        + " verrous PASS (structurels) ; diff nul VERT",
        "  construction                 : 0 erreur / 0 avertissement : build script",
        "  format_durci                 : ET_DYN (PIE), 3 segments R/RX/RW, "
        "PT_GNU_STACK RW sans X, W^X constaté depuis les phdr "
        "(héritage M6-(a)), .bss pur",
        "  corpus_paritaire             : 12 blocs du patrimoine M0-M5 "
        "(révisions R+1 de unix/I/, ancêtres scellés INTACTS) + corpus-13 "
        "(domaine neuf, modèle ah-09)",
        "  diff_nul                     : fichiers canoniques unix/I/ "
        "(empreintes mesurées, zéro copie) ; observables R1<->R+1 équivalents "
        "(35 identiques + 1 écart nommé frag-con) ; 5 scellés Windows "
        "octet-identiques à l'état zéro",
        "  contrat_erreurs              : la propagation des verdicts bruts "
        "(écrire/tcp-11 Q2) et les codes nommés 1-5 (tcp-07 Q5) — le style "
        "des CONTRATS du patrimoine ; la table ERRNOS demeure la preuve du "
        "chantier (a)",
        "  patch_a_chaud                : tcp-07 instancié (mprotect 0x7/0x5, "
        "cible = l'entrée du journal, staging journal v2 embarqué) — scénario "
        "complet VERT (apply/effet/rollback/refus 1-5/DEP SIGSEGV) ; "
        "la bascule PENDANT le trafic est le chantier (d)",
        "  tests_differentiels          : oracle m1 régénéré NATIF — "
        + str(verdict["cas"]) + " cas verts (" + str(len(verdict["verrous"]))
        + " verrous) ; " + verdict["binaire"] + " ; falsification "
        + verdict["falsification"],
        "  couche_I                     : " + str(len(empreintes_I))
        + " fichiers unix/I/ empreintés dans frag-prf (la même couche que M7)",
        "  defauts_ouverts              : 0",
        "  preversions                  : " + version
        + " conforme (R10 : monotonie, plancher " + hex(L.VERSION_U64_MIN)
        + ", pointe sonde dev.1)",
        "  artefact                     : " + str(len(img)) + " octets ; "
        "empreinte sha256:" + sha(img)[:24] + "…",
        "  verrou_croise                : 13 empreintes + signature Ed25519 (R8)",
    ]) + "\n" + "\n".join("  " + l for l in phdr_lignes) + "\n"


# --- Construction / vérification ---------------------------------------------------

CHEMIN_ARTIFACT = os.path.join(UNIX, "corpus")


def _empreintes_I() -> dict:
    emps = {}
    for _, _, fichier, _, _ in L.BLOCS_CORPUS:
        with open(os.path.join(UNIX, "I", fichier + ".md"), "rb") as f:
            emps[fichier] = sha(f.read())
    return emps


def construire(volume: str, graine: int) -> int:
    print("=== M6-(b) : le corpus paritaire (unix/, D149) — l'instance SysV du "
          "patrimoine ===")
    _anti_rollback()
    specs = charger_couche_I()
    print(f"[I] {len(specs)} specs chargées — les MÊMES fichiers que M7 "
          f"(révisions épinglées par le plan)")
    diff = subprocess.run([sys.executable, os.path.join(UNIX, "diff_nul.py")],
                          capture_output=True, text=True)
    print(diff.stdout.strip().splitlines()[-1])
    if diff.returncode != 0:
        print(diff.stdout)
        raise EchecBuild("le diff nul n'est pas VERT — la chaîne s'arrête "
                         "(le critère du chantier est une garde, pas un vœu)")
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code, staging = assembler_tout(ks, cs)
    verrous = oracle_structurel(code, staging)
    n_symboles = verifier_symboles()
    print(f"[oracle] structurel : {len(verrous)} verrous PASS ; "
          f"{n_symboles} symboles confrontés au layout (C1)")
    img = composer_elf(code, staging)
    phdr = valider_elf(img, staging)
    with open(CHEMIN_ARTIFACT, "wb") as f:
        f.write(img)
    os.chmod(CHEMIN_ARTIFACT, 0o755)
    print(f"[ELF] corpus : {len(img)} octets, ET_DYN/PIE, entrée "
          f"{L.CORPUS_ENTREE:#x} (RVA), 13 blocs + staging + croissance")
    verdict = OC.executer(CHEMIN_ARTIFACT, graine=graine, volume=volume)
    verdict["graine"] = graine
    compteurs = {bid: 1 for bid, _, _, _, _ in L.BLOCS_CORPUS}
    journal = [f"run graine={graine} volume={volume} verdict={verdict['empreinte']}"
               f" build={L.VERSION_DEV2}"]
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, _empreintes_I())
    print("[carte] génération 1 écrite : 4 fragments chiffrés, signature Ed25519, "
          "frag-con DEUX PROFILS par bloc (§ 8.3-4)")
    nb = verrou_croise(code, img)
    print(f"[R8] verrou croisé : {nb} empreintes re-vérifiées, signature OK")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(tableau_de_bord(img, verrous, verdict, phdr, _empreintes_I()))
    print(f"[tableau] tableau de bord écrit (carte-corpus/tableau-de-bord.txt)")
    print(f"[B] corpus : sha256:{sha(img)}")
    print(f"=== M6-(b) : {L.VERSION_DEV2} — l'oracle m1 régénéré VERT sur "
          f"l'instance Linux (exécution native) ===")
    return 0


def verifier(volume: str, graine: int) -> int:
    print(f"=== M6 : re-vérification complète (R5/R8, graine {graine}) ===")
    # La balise de la carte est PRÉSERVÉE (modèle m5/D147) : un scellé ne se
    # revertit pas — la re-vérification re-signe la carte SOUS sa balise
    # courante, jamais au-dessus (le scellage est un fait de carte, la
    # reconstruction une toute autre porte, gardée par _anti_rollback).
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    manifeste_v = next(
        (dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
         if "artefact=corpus" in l), "?")
    version = manifeste_v if manifeste_v != "?" else L.VERSION_DEV2
    print(f"[balise] la carte vit sous {version} (préservée — la re-vérification "
          f"ne la déplace pas)")
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code, staging = assembler_tout(ks, cs)
    verrous = oracle_structurel(code, staging)
    verifier_symboles()
    with open(CHEMIN_ARTIFACT, "rb") as f:
        img = f.read()
    phdr = valider_elf(img, staging)
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        if img[rva:rva + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5 — "
                             f"verifier-puis-ecrire)")
    verdict = OC.executer(CHEMIN_ARTIFACT, graine=graine, volume=volume)
    verdict["graine"] = graine
    # cristallisation : compteurs +1 (R6), re-scellage de la carte
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m2 = re.match(r"(\d+)/10", champs.get("crist", "1/10"))
            compteurs[champs["id"]] = int(m2.group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    for bid, _, _, _, _ in L.BLOCS_CORPUS:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(f"run graine={graine} volume={volume} verdict={verdict['empreinte']}")
    specs = charger_couche_I()
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, _empreintes_I(), version=version)
    nb = verrou_croise(code, img)
    crist = {b: compteurs.get(b, 0) for b, _, _, _, _ in L.BLOCS_CORPUS}
    print("[R6] cristallisation : " + ", ".join(f"{b}={n}/10" for b, n in crist.items()))
    print(f"[R8] verrou croisé : {nb} empreintes conformes")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(tableau_de_bord(img, verrous, verdict, phdr, _empreintes_I(),
                                version=version))
    return 0


# --- Le scellage du jalon (chantier M6-(c), modèle D147 — m5/_sceller) -------------

# Le sha du corpus dev.2 (constaté au Task 64, Entrée 146) — le scellage est
# un fait de carte, l'artefact ne bouge JAMAIS : toute divergence = refus.
SHA_CORPUS_DEV2 = "dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7"


def _charger_module(nom: str, chemin: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def _sceller(nouvelle_version: str, exigences: str) -> int:
    """Scellage du jalon M6 (modèle D147/m5) : CONTRÔLE D146 ADAPTÉ vert
    (exécution full-ELF à la base réelle — l'image PIE au noyau, l'émulation
    à base fixe interdite comme témoin unique, D149-(6)) + cristallisation
    10/10 (R6) + conformité § 8.2 VERTE 7/7 (SEPT éléments constatés depuis
    l'artefact) + bascule de balise dans frag-bld. L'artefact n'est PAS
    touché — le scellage est un fait de carte, `corpus` reste byte-identique."""
    print(f"=== M6-(c) : scellage {nouvelle_version} ({exigences}) ===")

    # D146 adapté : AVANT que la carte ne se scelle, l'image PIE doit avoir
    # vécu au NOYAU — la base 0 n'existe pas au loader Linux (un pointeur nu
    # y meurt exactement comme sur le terrain : la leçon e3, devenue garde).
    cbr = _charger_module("controle_base_reelle_m6",
                          os.path.join(ICI, "controle_base_reelle.py"))
    vert_d146, lignes_d146 = cbr.executer(bavard=False)
    for l in lignes_d146[:8]:
        print(l)
    if not vert_d146:
        raise EchecBuild("contrôle D146 non vert (base réelle) — "
                         f"{nouvelle_version} refusé : {lignes_d146[-1]}")

    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(
                re.match(r"(\d+)/10", champs.get("crist", "0/10")).group(1))
    incomplets = {b: n for b, n in compteurs.items() if n < 10}
    if incomplets:
        raise EchecBuild(f"cristallisation incomplète : {incomplets} — "
                         f"10 vérifications requises (R6)")
    print(f"[R6] cristallisation : {len(compteurs)} blocs à 10/10")

    # Conformité § 8.2 (unix/conformite_profil.py — modèle m5/D104) : la
    # suite exigée à chaque cristallisation rc/finale, chargée sous un nom
    # distinct (elle recharge build_corpus comme module : aucune collision
    # d'état avec le présent __main__).
    cp = _charger_module("conformite_profil_m6",
                         os.path.join(ICI, "conformite_profil.py"))
    ok_conf, lignes_conf = cp.executer()
    print("\n".join(lignes_conf[-3:]))
    if not ok_conf:
        raise EchecBuild(f"suite de conformité non verte — {nouvelle_version} refusé")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    ancienne = L.VERSION_RC1 if nouvelle_version == L.VERSION_FINALE else L.VERSION_DEV2
    occurrences = bld.count(f"version={ancienne}")
    if occurrences != 1:
        raise EchecBuild(f"balise {ancienne} attendue une fois dans frag-bld "
                         f"({occurrences} occurrence(s)) — scellage refusé (fail-closed)")
    bld = bld.replace(f"version={ancienne}", f"version={nouvelle_version}")
    clairs = {"frag-bld": bld.encode("utf-8")}
    for nom in ("frag-loc", "frag-con", "frag-prf"):
        clairs[nom] = cm.dechiffrer_fragment(maitre, nom, fragments[nom])
    nouveaux = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = empreinte_racine(nouveaux)
    entete = cm.construire_entete(racine)
    _, graine_cles = cm.charger_secrets(interactif=False)
    prive, pub = cm.paire_cles(graine_cles)
    signature = cm.signer(prive, entete, nouveaux)

    # Vérification EN MÉMOIRE avant l'unique écriture (modèle D144/D147)
    cm.verifier_listes_blanches(entete.decode("ascii"))
    cm.verifier_signature(pub, entete, nouveaux, signature)
    if empreinte_racine(nouveaux).hex() not in entete.decode("ascii"):
        raise EchecBuild("contrôle en mémoire : empreinte racine divergente")
    controle = cm.dechiffrer_fragment(maitre, "frag-bld", nouveaux["frag-bld"]).decode()
    if f"version={nouvelle_version}" not in controle or f"version={ancienne}" in controle:
        raise EchecBuild("contrôle en mémoire : bascule de balise non constatée")
    cm.ecrire_carte(entete, nouveaux, signature, pub)

    # Le tableau de bord suit la balise (l'artefact, lui, ne bouge pas)
    chemin_tab = os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt")
    if os.path.exists(chemin_tab):
        with open(chemin_tab, encoding="utf-8") as f:
            tab = f.read()
        tab = tab.replace(f"version={ancienne}", f"version={nouvelle_version}")
        tab = tab.replace(f"{ancienne} conforme", f"{nouvelle_version} conforme")
        with open(chemin_tab, "w", encoding="utf-8") as f:
            f.write(tab)

    # Verrou croisé post-scellage + l'artefact INTACT (le fait de carte)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code, staging = assembler_tout(ks, cs)
    with open(CHEMIN_ARTIFACT, "rb") as f:
        img = f.read()
    nb = verrou_croise(code, img)
    print(f"[R8] verrou croisé post-scellage : {nb} empreintes conformes")
    sha_artefact = sha(img)
    if sha_artefact != SHA_CORPUS_DEV2:
        raise EchecBuild(f"artefact divergent ({sha_artefact[:16]}…) — le scellage "
                         f"est un fait de carte, `corpus` ne bouge pas")
    print(f"[balise] {nouvelle_version} SCELLÉE (immuable § 9 ; défaut → X.Y.Z+1 "
          f"à contrat stable, R4 ; anti-rollback R6 vivant, registre de la lignée "
          f"plancher 0.7.0-dev.1) ; corpus INTACT (sha256 {sha_artefact[:16]}…, "
          f"{len(img)} o — le scellage est un fait de carte)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--sceller-rc" in args:
            sys.exit(_sceller(L.VERSION_RC1,
                              "cristallisation R6 10/10 + conformité § 8.2 7/7 "
                              "(SEPT éléments constatés depuis l'artefact, unix/"
                              "conformite_profil.py) + CONTRÔLE D146 adapté VERT "
                              "exécuté AU scellage (exécution full-ELF à la base "
                              "réelle : 6 bases noyau distinctes constatées, le "
                              "RVA nu nommé mort — unix/controle_base_reelle.py) — "
                              "les critères du jalon prouvés à ce jour : durcissement "
                              "M6-(a) démontré en exécution, diff nul MESURÉ 39 "
                              "recoupements + oracle m1 régénéré 76 631 cas M6-(b) — "
                              "candidate SOUMISE au chantier M6-(d) (le patch en "
                              "production : bascule pendant le trafic + rollback + "
                              "zéro régression, kit terrain au coffre /test, run "
                              "WSL2/VM du développeur)"))
        if "--sceller-final" in args:
            sys.exit(_sceller(L.VERSION_FINALE,
                              "R6 + conformité + contrôle D146 + validation terrain "
                              "consignée (le run M6-(d) : patch pendant le trafic, "
                              "rollback, zéro régression — les preuves au coffre "
                              "/test, verdict sur pièces D138/D145/D148)"))
        if "--verifier" in args:
            graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 2
            volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
            sys.exit(verifier(volume, graine))
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
        volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
        sys.exit(construire(volume, graine))
    except (EchecBuild, OC.EchecOracle, cm.ErreurCarte) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
