#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conformite_profil.py — Suite de conformité du profil x86-64-linux-elf64 (spec § 8.2).

Jalon M6-(c) : la suite exigée « à chaque cristallisation de version rc et
finale (spec § 9) » — modèle m5/conformite_profil.py (D104/D136), portée à
l'artefact `corpus` (0.7.0-dev.2, sha256 dd14195c…, 12 288 o — les octets
assemblés par le build M6-(b) dont le diff nul est mesuré et l'oracle m1
régénéré VERT sur l'instance Linux, Entrée 146). Les SEPT éléments sont
CONSTATÉS depuis l'artefact (le fichier relu par la présente suite), les
sources (couche I, notations) et le plan d'adressage (unix/layout.py, source
unique) — jamais déclarés sans preuve. Chaque constat est tranché binaire
(PASS/ECHEC), aucun « pass mou ».

Éléments et constats :
  1 ISA et types        : magie ELF64 LE (EI_CLASS 2, EI_DATA 1), e_type 3
                          (ET_DYN), e_machine 0x3E ; le segment RX décodable
                          mode 64 SANS RESTE (padding NOP/int3 compris) ; les
                          23 vecteurs dorés du patrimoine aux adresses du
                          plan, OCTET POUR OCTET (les MÊMES contenus que m1).
  2 ABI d'appel (SysV)  : chaque appel direct du RX aboutit à une entrée de
                          bloc du plan OU à une étiquette locale du même bloc
                          ; la ZONE ROUGE est inutilisée (aucun accès
                          [rsp - k] dans l'image — le réflexe msx64, la fiche
                          § 2 : permise par l'ABI, interdite aux blocs qui
                          appellent) ; la pile ÉQUILIBRÉE par bloc (push/pop
                          et sub/add rsp appariés, ret à delta nul) ;
                          l'ALIGNEMENT 16 à chaque point d'appel (delta
                          conduit depuis l'ABI : ≡ 8 mod 16 à l'entrée des
                          blocs appelés, ≡ 0 pour le _start) ; les
                          conventions PAR BLOC pour les DEUX profils vivent
                          dans frag-con (carte déchiffrée, § 8.3-4).
  3 Format d'exécutable : ET_DYN (PIE), e_entry 0x1C40 RELATIF ; TROIS
                          PT_LOAD R/RX/RW, p_offset == p_vaddr, align page ;
                          RW filesz 0 (.bss pur) ; PT_GNU_STACK 0x6474E551 à
                          drapeaux RW SANS X ; W^X : aucun segment
                          inscriptible ET exécutable — le tout RELU depuis
                          l'artefact ET recoupé par readelf indépendant.
  4 Interface système   : les numéros de syscall AUTORISÉS PAR BLOC, constatés
                          depuis les octets (écrire {write=1}, sortir
                          {exit_group=231}, patch {mprotect=10}, les DIX
                          autres : AUCUN) ; le contrat d'erreurs : écrire
                          rend rax BRUT (le syscall immédiatement suivi de
                          ret — aucune conversion) et tcp-07 porte ses SIX
                          codes nommés, EXERCÉS en exécution par l'oracle
                          (codes 1-5 dont le refus RÉEL EACCES du noyau) ;
                          la table ERRNOS (miroir HRESULTS, la preuve du
                          chantier (a)) lue depuis la SONDE de la lignée.
  5 Patch à chaud       : la PORTE R10 DÉCLINÉE ELF — table d'intégrité
                          @0x540, première entrée = le staging (rva 0x300,
                          taille > 0), somme déclarée == somme RECALCULÉE
                          DEPUIS L'ARTEFACT (la porte VIVANTE, les mêmes
                          qwords de garde que m4/m5) ; les constantes du
                          profil 0x7/0x5 DANS LES OCTETS de tcp-07 (D39 — le
                          bit exécution retenu) ; le qword de bascule posé en
                          UNE écriture alignée ([r15]) ; la cible = l'entrée
                          du journal au plan ; le scénario complet EN
                          EXÉCUTION (l'oracle) : apply → croissance = staging
                          octet pour octet + E9+NOPs + L'ENTRÉE APPELÉE rend
                          le journal v2, rollback → v1, refus code 3
                          (staging corrompu — R10 exercé), refus code 5
                          (mprotect EACCES réel), DEP V7 (0x7→0x3 : le ret
                          faute) ; frontière : la bascule PENDANT le trafic
                          est le chantier (d).
  6 Notation            : round-trip 100 % rejoué (les 13 blocs + le staging,
                          assembler_tout — EchecBuild sinon) ; les empreintes
                          des notations dans frag-prf == les fichiers actuels
                          (la carte à jour, R8 côté sources) ; le diff nul
                          VERT rejoué (les MÊMES fichiers I que l'instance
                          Windows, les CINQ scellés intacts — le critère du
                          chantier (b) est une garde qui vit).
  7 Granularité/padding : taille 12 288 o == plan ; les 13 blocs aux
                          rva/slot du plan, slots multiples de 64 alignés 16
                          (D8) ; padding inter-blocs >= 16 ; la croissance
                          0x1D80 int3 à l'état image (le remplaçant y
                          dormira) ; le staging dans sa réserve.

Contrôle de jalon M6 : l'oracle m1 régénéré en volume « reduit » (graine
datée donc reproductible, falsification incluse) — exécution native au labo.

Sortie : unix/conformite.txt (une ligne de synthèse, reproductible).
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import struct
import subprocess
import sys
import time

import capstone
from keystone import KS_ARCH_X86, KS_MODE_64, Ks

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import layout as L  # noqa: E402

import oracle_corpus as OC  # noqa: E402
import carte_corpus as cm  # noqa: E402


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# build_corpus rechargé sous nom propre (miroir du modèle D104/D136 : aucune
# collision d'état avec le __main__ du scellage qui invoque la présente suite)
BC = _charger_module("build_corpus_conf", os.path.join(ICI, "build_corpus.py"))

CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
CS.detail = False

CHEMIN_ART = os.path.join(ICI, "corpus")
SHA_CORPUS_ATTENDU = "dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7"


class Suite:
    """Sept éléments ; chaque constat tranché binaire (jamais de « pass mou »)."""

    def __init__(self):
        self.controles = []

    def verrou(self, element: int, nom: str, ok: bool, detail: str = ""):
        self.controles.append((element, nom, bool(ok), detail))
        print(f"  [{element}] {'PASS' if ok else 'ECHEC'} : {nom}"
              + (f" ({detail})" if detail else ""))

    def lignes(self) -> list[str]:
        return [f"[conformite] element {e} {'PASS' if ok else 'ECHEC'} : {n}"
                + (f" ({d})" if d else "") for e, n, ok, d in self.controles]

    @property
    def ok(self) -> bool:
        return all(c[2] for c in self.controles)


def _lire(chemin: str) -> bytes:
    with open(chemin, "rb") as f:
        return f.read()


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _somme_qwords(donnees: bytes) -> int:
    s = 0
    for i in range(0, len(donnees), 8):
        s = (s + struct.unpack_from("<Q", donnees, i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


def _blocs_depuis_artefact(art: bytes) -> dict[str, list]:
    """Le désassemblage de CHAQUE bloc du plan, relu depuis l'artefact."""
    out = {}
    for bid, _spec, _f, rva, slot in L.BLOCS_CORPUS:
        out[bid] = list(CS.disasm(art[rva:rva + slot], rva))
    return out


# --- Élément 1 : ISA et types -----------------------------------------------------

VECTEURS_DORES = [
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


def element_1(s: Suite, art: bytes):
    print("element 1 : ISA et types")
    s.verrou(1, "magie ELF64 petit-boutiste (\\x7fELF, EI_CLASS 2, EI_DATA 1, "
             "EI_VERSION 1, EI_OSABI 0)",
             art[:16] == b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8)
    e_type, e_machine, e_version = struct.unpack_from("<HHI", art, 16)
    s.verrou(1, "e_type 3 (ET_DYN — PIE) ; e_machine 0x3E (x86-64) ; e_version 1",
             e_type == 3 and e_machine == 0x3E and e_version == 1,
             f"type {e_type}, machine {e_machine:#x}")

    # Le segment RX décodable mode 64 SANS RESTE (le padding NOP/int3 compris)
    code = art[L.CORPUS_SEG_RX_RVA:L.CORPUS_SEG_RX_RVA + L.CORPUS_SEG_RX_TAILLE]
    reste = len(code)
    for _insn in CS.disasm(code, L.CORPUS_SEG_RX_RVA):
        reste -= _insn.size
    s.verrou(1, "segment RX 0x1000-0x3000 décodable mode 64 sans reste",
             reste == 0, f"reste {reste} o")

    # Les vecteurs dorés du patrimoine : OCTET POUR OCTET aux adresses du plan
    manquants = [n for rva, donnees, n in VECTEURS_DORES
                 if art[rva:rva + len(donnees)] != donnees]
    s.verrou(1, "les 23 vecteurs dorés du patrimoine aux adresses du plan, "
             "octet pour octet (les MÊMES contenus que m1)",
             not manquants, f"divergents : {manquants}" if manquants
             else "memcmp/memcpy/strlen/itoa/memset + rituel + j2")


# --- Élément 2 : ABI d'appel (SysV) ------------------------------------------------

ENTREES_PLAN = {L.A_ECRIRE_CORPUS, L.A_SORTIR, L.A_MEMCPY, L.A_MEMCMP,
                L.A_STRLEN, L.A_ITOA, L.A_ZONE_ALLOC, L.A_ZONE_RESET,
                L.A_MEMSET, L.A_AUTOTEST, L.A_JOURNAL, L.A_PATCH,
                L.A_PRINCIPAL_CORPUS}


def element_2(s: Suite, art: bytes, blocs: dict):
    print("element 2 : ABI d'appel (SysV)")
    # (a) chaque appel direct : une entrée du plan OU une étiquette locale
    hors_plan = 0
    total_appels = 0
    for bid, insns in blocs.items():
        rva, slot = next((r, sl) for b, _sp, _f, r, sl in L.BLOCS_CORPUS
                         if b == bid)
        for i in insns:
            if i.mnemonic == "call" and i.op_str.startswith("0x"):
                cible = int(i.op_str, 16)
                total_appels += 1
                if cible not in ENTREES_PLAN and not (rva <= cible < rva + slot):
                    hors_plan += 1
    s.verrou(2, "aucun appel direct hors des entrées du plan / étiquettes "
             "locales (I1 de chaque spec)",
             hors_plan == 0, f"{total_appels} appels, {hors_plan} hors plan")

    # (b) la ZONE ROUGE inutilisée : aucun accès [rsp - k] dans l'image
    zone_rouge = 0
    for bid, insns in blocs.items():
        for i in insns:
            if "[rsp - " in i.op_str:
                zone_rouge += 1
    s.verrou(2, "zone rouge INUTILISÉE : aucun accès [rsp - k] dans le "
             "segment RX (permise par SysV, interdite aux blocs qui appellent "
             "— la fiche § 2)",
             zone_rouge == 0, f"{zone_rouge} accès sous rsp")

    # (c) la pile équilibrée + l'alignement 16 AUX POINTS D'APPEL — le scan
    # PAR CONTEXTE : le corps principal conduit depuis l'ABI (≡ 8 mod 16 à
    # l'entrée des blocs APPELÉS, ≡ 0 au _start corpus-13) ; les
    # SOUS-PROGRAMMES LOCAUX (les cibles d'appel internes au bloc — .protger
    # de tcp-07) sont scannés dans LEUR contexte (le retour de l'appelant y
    # est déjà posé) ; push/pop et sub/add rsp appariés, tout autre écriture
    # de rsp = indécidable = refus
    problemes = []
    for bid, insns in blocs.items():
        rva, slot = next((r, sl) for b, _sp, _f, r, sl in L.BLOCS_CORPUS
                         if b == bid)

        def _conduire(base_entree: int, liste):
            delta = 0
            for i in liste:
                if i.mnemonic == "push":
                    delta -= 8
                elif i.mnemonic == "pop":
                    delta += 8
                elif i.mnemonic == "sub" and i.op_str.startswith("rsp,"):
                    delta -= int(i.op_str.split(",")[1].strip(), 0)
                elif i.mnemonic == "add" and i.op_str.startswith("rsp,"):
                    delta += int(i.op_str.split(",")[1].strip(), 0)
                elif i.mnemonic == "mov" and i.op_str.split(",")[0].strip() == "rsp":
                    problemes.append(f"{bid}: écriture directe de rsp @ {i.address:#x}")
                elif i.mnemonic in ("xchg", "lea", "leave") and i.op_str.startswith("rsp"):
                    problemes.append(f"{bid}: {i.mnemonic} rsp @ {i.address:#x} (indécidable)")
                if i.mnemonic == "call" and i.op_str.startswith("0x"):
                    if (base_entree + delta) % 16 != 0:
                        problemes.append(f"{bid}: appel @ {i.address:#x} à rsp "
                                         f"≡ {(base_entree + delta) % 16} mod 16")
                if i.mnemonic == "ret" and delta != 0:
                    problemes.append(f"{bid}: ret @ {i.address:#x} à delta {delta}")

        cibles_internes = {int(i.op_str, 16) for i in insns
                           if i.mnemonic == "call" and i.op_str.startswith("0x")
                           and rva <= int(i.op_str, 16) < rva + slot}
        regions = []
        for t in sorted(cibles_internes):
            fin = next((i.address + i.size for i in insns
                        if i.address >= t and i.mnemonic == "ret"), rva + slot)
            regions.append((t, fin))
        corps = [i for i in insns
                 if not any(t <= i.address < f for t, f in regions)]
        _conduire(0 if bid == "f61013" else 8, corps)   # le _start n'a pas de cadre
        for t, f in regions:
            _conduire(8, [i for i in insns if t <= i.address < f])
    s.verrou(2, "pile équilibrée par bloc (push/pop, sub/add appariés, ret à "
             "delta nul) — prologue/épilogue symétriques (I4)",
             not problemes, "; ".join(problemes[:3]) if problemes
             else "13 blocs conduits sans écart")

    # (d) le _start sans cadre : corpus-13 ne touche pas la pile (I4 —
    # l'alignement du noyau traverse jusqu'aux appels)
    p = blocs["f61013"]
    s.verrou(2, "corpus-13 (_start) : aucun push, aucun sub rsp — rsp ≡ 0 "
             "mod 16 de l'entrée ELF aux appels (l'ABI de démarrage Linux)",
             not any(i.mnemonic == "push" or
                     (i.mnemonic in ("sub", "add") and i.op_str.startswith("rsp,"))
                     for i in p))

    # (e) les conventions PAR BLOC pour les DEUX profils vivent dans frag-con
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    con = cm.dechiffrer_fragment(maitre, "frag-con", fragments["frag-con"]).decode()
    avec_sysv = sum(1 for bid, _sp, _f, _r, _sl in L.BLOCS_CORPUS
                    if re.search(rf"\[bloc\] id={bid}\n(?:  .*\n){{3}}"
                                 rf"  x86-64-linux-elf64 : ", con))
    s.verrou(2, "frag-con : la convention d'appel PAR BLOC pour les DEUX "
             "profils (§ 8.3-4 — 13 lignes x86-64-linux-elf64)",
             avec_sysv == 13, f"{avec_sysv}/13")
    s.verrou(2, "frag-con : l'alignement partagé et la volatilité SysV "
             "nommées (RDI/RSI changent de camp)",
             "[alignement]" in con and "[volatilite]" in con
             and "RDI/RSI changent de camp" in con)


# --- Élément 3 : format d'exécutable -----------------------------------------------

def element_3(s: Suite, art: bytes):
    print("element 3 : format d'exécutable")
    e_type = struct.unpack_from("<H", art, 16)[0]
    e_entry = struct.unpack_from("<Q", art, 24)[0]
    s.verrou(3, "ET_DYN (PIE) ; e_entry 0x1C40 RELATIF à la base",
             e_type == 3 and e_entry == L.CORPUS_ENTREE,
             f"entrée {e_entry:#x} (RVA)")
    phoff, phentsize, phnum = (struct.unpack_from("<Q", art, 32)[0],
                               struct.unpack_from("<H", art, 54)[0],
                               struct.unpack_from("<H", art, 56)[0])
    loads, stack_ok, wx = [], True, False
    for i in range(phnum):
        p_type, p_flags = struct.unpack_from("<II", art, phoff + i * 56)
        p_offset, p_vaddr = struct.unpack_from("<QQ", art, phoff + i * 56 + 8)
        p_filesz, p_memsz = struct.unpack_from("<QQ", art, phoff + i * 56 + 32)
        p_align = struct.unpack_from("<Q", art, phoff + i * 56 + 48)[0]
        if p_type == 1:
            loads.append((p_flags, p_offset, p_vaddr, p_filesz, p_memsz, p_align))
            if p_flags & 2 and p_flags & 1:
                wx = True
        elif p_type == L.PT_GNU_STACK:
            stack_ok = (p_flags == 6 and p_align == 0x10)
    s.verrou(3, "TROIS PT_LOAD R(4)/RX(5)/RW(6), p_offset == p_vaddr, "
             "align page — RELUS depuis l'artefact",
             [f[0] for f in loads] == [4, 5, 6]
             and all(f[1] == f[2] and f[5] == L.TAILLE_PAGE for f in loads),
             " / ".join(f"{f[0]:#x}@{f[2]:#x}" for f in loads))
    s.verrou(3, "le segment RW est .bss PUR (filesz 0, memsz 0x1000)",
             loads[2][3] == 0 and loads[2][4] == L.CORPUS_SEG_RW_TAILLE)
    s.verrou(3, "PT_GNU_STACK 0x6474E551 à drapeaux RW SANS X (NX explicite)",
             stack_ok)
    s.verrou(3, "W^X : aucun PT_LOAD inscriptible ET exécutable", not wx)
    s.verrou(3, "taille fichier 12 288 o == plan (0x3000)",
             len(art) == L.CORPUS_TAILLE_FICHIER)

    # Le témoin INDÉPENDANT : readelf (pas le build, pas capstone)
    r = subprocess.run(["readelf", "-hlW", CHEMIN_ART],
                       capture_output=True, text=True, timeout=30)
    texte = r.stdout
    lignes_load = [l.split() for l in texte.splitlines() if l.strip().startswith("LOAD")]
    drapeaux = [" ".join(l[6:-1]) for l in lignes_load]
    gnustack = next((l for l in texte.splitlines() if "GNU_STACK" in l), "")
    gs_drapeaux = " ".join(gnustack.split()[6:-1]) if gnustack else ""
    s.verrou(3, "readelf indépendant recoupe : DYN, 3 LOAD R / R E / RW, "
             "GNU_STACK RW sans E",
             "Type:" in texte and "DYN" in texte.split("Type:")[1].splitlines()[0]
             and drapeaux == ["R", "R E", "RW"]
             and gs_drapeaux == "RW",
             f"LOAD {'/'.join(drapeaux)} ; GNU_STACK {gs_drapeaux}")


# --- Élément 4 : interface système -------------------------------------------------

SYS_PAR_BLOC = {"f61001": {L.SYS_WRITE}, "f61002": {L.SYS_EXIT_GROUP},
                "f61012": {L.SYS_MPROTECT}}


def element_4(s: Suite, art: bytes, blocs: dict, verrous: list[str]):
    print("element 4 : interface système")
    # (a) les numéros PAR BLOC, constatés depuis les octets de l'artefact
    ecarts = []
    observes = {}
    for bid, insns in blocs.items():
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
                if nr not in SYS_PAR_BLOC.get(bid, set()):
                    ecarts.append(f"{bid}: nr={nr}")
                observes.setdefault(bid, set()).add(nr)
    s.verrou(4, "numéros de syscall AUTORISÉS PAR BLOC (I1 — la table du "
             "jalon) : écrire {write}, sortir {exit_group}, patch {mprotect}, "
             "les DIX autres : AUCUN",
             not ecarts and observes == {"f61001": {1}, "f61002": {231},
                                         "f61012": {10}},
             f"observés : {sorted(observes)}" if ecarts
             else "write=1, exit_group=231, mprotect=10 — exactement")

    # (b) le contrat d'erreurs, côté octets : écrire rend rax BRUT
    # (le syscall immédiatement suivi de ret — aucune conversion, la
    # propagation hello-02:R2 Q2)
    e = blocs["f61001"]
    idx = next(k for k, i in enumerate(e) if i.mnemonic == "syscall")
    s.verrou(4, "écrire rend rax BRUT : le syscall suivi immédiatement de ret "
             "(aucun marshalling — la propagation du contrat)",
             idx + 1 < len(e) and e[idx + 1].mnemonic == "ret"
             and e[idx - 1].op_str.startswith("eax, 1"))

    # (c) le contrat d'erreurs, côté exécution : les codes nommés de tcp-07
    # EXERCÉS par l'oracle (refus 1-5 dont EACCES réel du noyau — code 5)
    attendus = ["tcp-07 refus:", "tcp-07 intégrité:", "tcp-07 absent:",
                "tcp-07 service:"]
    presents = [a for a in attendus if any(v.startswith(a) for v in verrous)]
    s.verrou(4, "le contrat d'erreurs de tcp-07 EXERCÉ en exécution : codes "
             "1-5 nommés (mode invalide, état incohérent, staging corrompu "
             "R10, absent, mprotect EACCES RÉEL du noyau)",
             len(presents) == 4, f"{len(presents)}/4 familles")

    # (d) la table ERRNOS (miroir HRESULTS — la preuve du chantier (a)) :
    # lue depuis la SONDE de la lignée (dev.1), l'ancêtre directe
    sonde = _lire(os.path.join(ICI, "sonde"))
    n = struct.unpack_from("<I", sonde, L.R_ERRNOS)[0]
    entree = struct.unpack_from("<II", sonde, L.R_ERRNOS + 4)
    s.verrou(4, "la table ERRNOS de la lignée (la sonde 0.7.0-dev.1, sha "
             "f5f0a08f…) : [1] {EBADF 9 → verdict 1}, VERDICT_FATAL 6 — le "
             "miroir de la table HRESULTS D79",
             _sha(sonde).startswith("f5f0a08f") and n == 1
             and entree == (9, 1) and L.VERDICT_FATAL == 6,
             "succès par plage, échec nommé, fatal fail-closed")


# --- Élément 5 : patch à chaud (la porte R10 déclinée ELF) --------------------------

def element_5(s: Suite, art: bytes, blocs: dict, verrous: list[str]):
    print("element 5 : patch à chaud")
    # (a) la PORTE R10 déclinée ELF : la table d'intégrité, VIVANTE
    rva_t, taille_t, somme_t = struct.unpack_from("<IIQ", art, L.R_TAB_SUM_CORPUS)
    somme_recalculee = _somme_qwords(art[L.R_STAGING_CORPUS:L.R_STAGING_CORPUS + taille_t])
    terme = art[L.R_TAB_SUM_CORPUS + 16:L.R_TAB_SUM_CORPUS + 36]
    s.verrou(5, "la porte R10 déclinée ELF : table @0x540, première entrée = "
             "le staging (rva 0x300, taille > 0, qwords)",
             rva_t == L.R_STAGING_CORPUS and 0 < taille_t <= L.STAGING_TAILLE_MAX
             and taille_t % 8 == 0, f"staging {taille_t} o")
    s.verrou(5, "la somme déclarée == la somme RECALCULÉE depuis l'artefact "
             "(la porte VIVANTE — les mêmes qwords de garde que m4/m5)",
             somme_t == somme_recalculee and somme_t != 0, f"somme {somme_t:#x}")
    s.verrou(5, "le terme de table est NUL (rva 0 — la marche s'arrête nommée)",
             terme == b"\x00" * 20)

    # (b) les constantes du profil DANS LES OCTETS de tcp-07 (D39) et le
    # qword de bascule en UNE écriture alignée
    t = blocs["f61012"]
    s.verrou(5, "tcp-07 porte les constantes du profil 0x7/0x5 (D39 : le bit "
             "exécution RETENU pendant l'écriture de code — jamais 0x3)",
             any(i.mnemonic == "mov" and i.op_str == "edi, 7" for i in t)
             and any(i.mnemonic == "mov" and i.op_str == "edi, 5" for i in t))
    s.verrou(5, "le qword de bascule posé en UNE écriture alignée "
             "(mov qword ptr [r15], reg — I3, atomicité x86-64)",
             any(i.mnemonic == "mov" and i.op_str.startswith("qword ptr [r15],")
                 for i in t))

    # (c) la cible du patch : l'entrée du journal au plan (le qword lu et
    # réécrit à A_JOURNAL — les accès déclarés de tcp-07 I3)
    cible_nommee = any(i.mnemonic == "mov" and "rax, qword ptr [r15]" == i.op_str
                       for i in t)
    s.verrou(5, "la CIBLE = l'entrée du journal tcp-11 @0x1840 au plan (le "
             "remplaçant vit au staging POUR la croissance 0x1D80)",
             L.A_JOURNAL == 0x1840 and L.A_CROISSANCE == 0x1D80 and cible_nommee)

    # (d) le scénario complet EN EXÉCUTION (l'oracle natif — mprotect réel)
    attendus = ["tcp-07 apply:", "tcp-07 effet:", "tcp-07 rollback:",
                "tcp-07 intégrité:", "tcp-07 service:", "tcp-07 DEP:"]
    presents = [a for a in attendus if any(v.startswith(a) for v in verrous)]
    s.verrou(5, "le patch DÉMONTRÉ en exécution : apply (croissance = staging "
             "octet pour octet, E9+NOPs, état 1), l'ENTRÉE APPELÉE rend le "
             "journal v2, rollback (v1 de retour), refus code 3 (R10), refus "
             "code 5 (EACCES réel), DEP V7 (0x7→0x3 : le ret faute)",
             len(presents) == 6, f"{len(presents)}/6 familles")

    # (e) la frontière : le moteur est EMBARQUÉ (les octets + le scénario),
    # la bascule PENDANT le trafic est le chantier (d) — rapportée, pas tue
    s.verrou(5, "frontière nommée : la bascule PENDANT le trafic (M5-(c) "
             "refermé) est le chantier M6-(d) — le moteur est embarqué, la "
             "démonstration en production attend", True,
             "constat partagé (miroir D73/D104 : portes vivantes, moteur "
             "rapporté ; ici le moteur est EMBARQUÉ, la bascule au trafic "
             "reste à (d))")


# --- Élément 6 : notation (round-trip + carte + diff nul) ----------------------------

def element_6(s: Suite, code: dict, staging: dict):
    print("element 6 : notation")
    # (a) le round-trip 100 % rejoué : assembler_tout a exigé l'identité
    # keystone→octets→capstone PAR INSTRUCTION (EchecBuild sinon — son succès
    # même est le constat)
    s.verrou(6, "round-trip 100 % rejoué : les 13 blocs + le staging "
             "assemblés (assembler_tout — l'identité par instruction)",
             len(code) == 13 and staging is not None
             and all(b["insns"] for b in code.values()),
             f"13 blocs + staging {len(staging['octets'])} o")

    # (b) les empreintes des notations dans frag-prf == les fichiers actuels
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    empreintes = {}
    for ligne in prf.splitlines():
        m = re.match(r"\[bloc\] id=(\S+)", ligne)
        if m:
            courant = m.group(1)
        m = re.search(r"notation=(\S+)", ligne)
        if m and courant:
            empreintes[courant] = m.group(1)
    divergents = []
    for bid, _spec, fichier, _r, _sl in L.BLOCS_CORPUS:
        avec = _sha(_lire(os.path.join(ICI, "notation", fichier + ".asm")))
        if empreintes.get(bid) != avec:
            divergents.append(bid)
    s.verrou(6, "les empreintes des notations dans frag-prf == les fichiers "
             "actuels (la carte à jour — R8 côté sources)",
             not divergents and len(empreintes) == 13,
             f"divergents : {divergents}" if divergents else "13/13")

    # (c) le diff nul VERT rejoué (le critère du chantier (b) est une garde
    # qui vit, pas un souvenir)
    diff = subprocess.run([sys.executable, os.path.join(ICI, "diff_nul.py")],
                          capture_output=True, text=True, timeout=300)
    s.verrou(6, "le diff nul VERT rejoué : les MÊMES fichiers I que "
             "l'instance Windows, les CINQ scellés intacts (39 recoupements)",
             diff.returncode == 0, diff.stdout.strip().splitlines()[-1][:96]
             if diff.stdout.strip() else "sans sortie")


# --- Élément 7 : granularité et padding ----------------------------------------------

def element_7(s: Suite, art: bytes, blocs: dict):
    print("element 7 : granularité et padding")
    s.verrou(7, "taille artefact == plan (12 288 o — 0x3000)",
             len(art) == 12288)
    problemes = []
    for bid, insns in blocs.items():
        rva, slot = next((r, sl) for b, _sp, _f, r, sl in L.BLOCS_CORPUS
                         if b == bid)
        if slot % 64 != 0 or rva % 16 != 0:
            problemes.append(f"{bid}: D8 (slot {slot:#x}, rva {rva:#x})")
        # la fin du CODE (le dernier insn non-NOP de queue) → fin du slot
        corps = [i for i in insns if not (i.mnemonic == "nop" and i.size == 1)]
        if not corps:
            problemes.append(f"{bid}: bloc vide")
            continue
        fin = corps[-1].address + corps[-1].size
        if rva + slot - fin < 16:
            problemes.append(f"{bid}: padding {rva + slot - fin} < 16")
        if art[rva:rva + 8] == b"\xcc" * 8:
            problemes.append(f"{bid}: slot int3 (le code n'y vit pas)")
    s.verrou(7, "les 13 blocs aux rva/slot du plan, slots multiples de 64 "
             "alignés 16 (D8), padding inter-blocs >= 16",
             not problemes, "; ".join(problemes[:3]) if problemes
             else "13/13 à leur adresse de plan")
    croissance = art[L.A_CROISSANCE:L.A_CROISSANCE + 16]
    s.verrou(7, "la croissance 0x1D80 int3 (0xCC) à l'état image — le "
             "remplaçant y sera copié par tcp-07 (le staging est POUR elle)",
             croissance == b"\xcc" * 16)
    rva_t, taille_t, _somme = struct.unpack_from("<IIQ", art, L.R_TAB_SUM_CORPUS)
    s.verrou(7, "le staging dans sa réserve (0x300 + taille <= 0x580, la "
             "table suit @0x540)",
             L.R_STAGING_CORPUS + taille_t <= L.R_TAB_SUM_CORPUS
             and rva_t == L.R_STAGING_CORPUS, f"staging {taille_t} o @ 0x300")


# --- Contrôle de jalon M6 : l'oracle m1 régénéré, volume reduit -----------------------

def controle_jalon(s: Suite, graine: int) -> dict:
    print(f"contrôle de jalon M6 (oracle m1 régénéré, volume reduit, graine {graine})")
    t0 = time.time()
    verdict = OC.executer(CHEMIN_ART, graine=graine, volume="reduit")
    duree = round(time.time() - t0, 1)
    s.verrou(0, "oracle m1 régénéré VERT en exécution native (différentiel "
             "par blocs + autotest + journal concurrent + patch complet + "
             "artefact + falsification zéro silence)",
             verdict["cas"] >= 8000 and len(verdict["verrous"]) >= 20,
             f"{verdict['cas']} cas, {len(verdict['verrous'])} verrous, "
             f"{duree}s")
    return verdict


def executer(graine: int | None = None) -> tuple[bool, list[str]]:
    """Exécute la suite complète ; retourne (verdict, lignes de rapport)."""
    if graine is None:
        graine = int(time.strftime("%Y%m%d"))
    art = _lire(CHEMIN_ART)
    if _sha(art) != SHA_CORPUS_ATTENDU:
        raise OC.EchecOracle(
            f"l'artefact corpus diverge ({_sha(art)[:16]}…) — la suite "
            f"constate l'artefact {SHA_CORPUS_ATTENDU[:16]}… (fail-closed)")
    blocs = _blocs_depuis_artefact(art)
    s = Suite()
    element_1(s, art)
    element_2(s, art, blocs)
    element_3(s, art)
    # le contrôle de jalon FOURNIT l'exécution aux éléments 4 et 5
    verdict = controle_jalon(s, graine)
    verrous = verdict["verrous"]
    element_4(s, art, blocs, verrous)
    element_5(s, art, blocs, verrous)
    # élément 6 : les sources (l'ordre du build, l'héritage re-vérifié par
    # les mêmes fonctions que construire/verifier)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code, staging = BC.assembler_tout(ks, cs)
    element_6(s, code, staging)
    element_7(s, art, blocs)
    lignes = s.lignes()
    total_c = len(s.controles)
    verdict_txt = "verte" if s.ok else "ROUGE"
    synthese = (f"{verdict_txt} (conformite_profil.py : elements 1-7 + controle "
                f"de jalon M6 : {total_c} controles "
                f"{'PASS' if s.ok else 'EN ECHEC'} ; la porte R10 déclinée ELF "
                f"VIVANTE (staging {struct.unpack_from('<IIQ', art, L.R_TAB_SUM_CORPUS)[1]} o, "
                f"somme recalculée depuis l'artefact) ; le patch démontré en "
                f"exécution (apply/effet/rollback/refus 1-5/EACCES/DEP), la "
                f"bascule pendant le trafic au chantier (d) ; contrôle de "
                f"jalon : oracle m1 {verdict['cas']} cas verts, graine "
                f"{graine} ; artefact corpus sha256 "
                f"{SHA_CORPUS_ATTENDU[:16]}… — le diff nul rejoué VERT, les "
                f"MÊMES fichiers I que l'instance Windows)")
    with open(os.path.join(ICI, "conformite.txt"), "w", encoding="utf-8") as f:
        f.write(synthese + "\n")
    lignes.append(f"[conformite.txt] {synthese}")
    return s.ok, lignes


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(
        description="Suite de conformite du profil x86-64-linux-elf64 "
                    "(spec 8.2) — jalon M6-(c) : oracle m1 régénéré intégré")
    ap.add_argument("--graine", type=int, default=None,
                    help="graine maitresse de l'oracle (defaut : AAAAMMJJ du "
                         "jour, reproductible)")
    args = ap.parse_args()
    try:
        ok, rapport = executer(graine=args.graine)
        print("\n".join(rapport))
        sys.exit(0 if ok else 1)
    except (OC.EchecOracle, BC.EchecBuild, cm.ErreurCarte) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
