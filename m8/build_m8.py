#!/usr/bin/env python3
"""build_m8.py — Jalon M8 de TRIADE : LE DOMAINE `sys` (proxy 0.9.0-dev.1 — D160/D161).

Chaîne : notation (keystone) -> octets -> PE32+ à la main (SEPT sections :
.text/.rdata/.data/.text2/.text3/.text4 + .text5 NOUVELLE) -> carte projet
génération 8. Implémente le chantier (c) du jalon M8 sous les règles R4/R7
(adresses stables — l'héritage M0-M5 repris OCTET POUR OCTET du proxy.exe
0.6.0 scellé, sha256 c1e46fb0…, l'artefact PROUVÉ par le run e4 et la carte
génération 7 scellée) et R10 (la version 0x00090001 — geste de BUILD,
JAMAIS un scellage : la 0.9.0 finale attend le terrain vert du chantier (d)).

LA COMPOSITION 0.9.0-dev.1 (D160/D161, m8/I/README.md) :
  - sys-01  (g90001 @0xA000, slot 0x40)  l'émetteur — le trombone ABI
    (mov r10, rcx ; syscall ; ret — SIX octets, AUCUN prologue I3) ;
  - sys-02  (g90002 @0xA040, slot 0x140)  le résolveur SSN — l'EAT de ntdll
    LUE directement (la marche BORNÉE, le MOTIF_STUB AVANT l'imm32, memcmp
    libc-02 le seul appel) ;
  - sys-03  (g90003 @0xA180, slot 0xC0)   la twin de hello-02 par
    NtWriteFile — les NEUF arguments, le fixture-ligne CITÉ, zéro IAT.

Deltas PE documentés (R7 — tout le reste est l'héritage scellé 0.6.0) :
  .text5 : NOUVELLE (0xA000-0xBFFF) : les trois blocs du domaine + la
           réserve int3 0xA240-0xBFFF (croissance : sys-04 et suivants) ;
  .rdata : 0x2EC0-0x2EFF = fixtures du domaine (le span-nom « NtWriteFile »
           @0x2EC0, la LIGNE de hello-02 @0x2ED0) posées dans la zone
           VIERGE vérifiée (0x2EB0-0x2FFF nuls dans le scellé, D161) ;
  version: @0x2820 : 0x00060001 -> 0x00090001 (R10 : geste de BUILD —
           monotonie > 0x00060001, plancher 0x00040000 inchangé) ;
  PE     : NumberOfSections 6 -> 7 ; SizeOfImage 0xA000 -> 0xC000 ; taille
           de fichier 0x8E00 -> 0xAE00 (.text5 raw @0x8E00) ; les en-têtes
           restent <= 0x400 — AUCUN décalage de packaging (64+4+20+240+280
           = 608 o ; le modèle D94 n'est PAS rejoué : la marge suffit).

L'ORACLE DU DOMAINE (m8/harnais_sys.py) est exécuté sur les BLOBS du
build : harnais.executer(blobs, graine, volume) — le différentiel sur
FIXTURES ntdll synthétiques (le labo ne connaît pas le SSN du terrain et
ne le devine jamais), la twin au différentiel (LA MÊME ligne par les DEUX
chemins), la falsification (zéro silence). L'héritage est re-vérifié AU
PASSAGE : build_m4.assembler_tout_m4() + build_m5 (round-trip + oracles
structurels M3/M4/M5) et l'image M5 composée est confrontée OCTET PAR
OCTET au proxy.exe 0.6.0 scellé AVANT toute extension — la preuve R7.

LE GARDE-SCEAU (D87) : le build REFUSE de démarrer si un arbre d'intention
de la lignée win (m0-m5) ou le domaine (m8) a divergé de sa signature. La
cérémonie de l'ère M8 (re-signature de m0 [registre figé étendu au
M8-(a)] + création de l'arbre m8) est EXIGÉE avant tout build — la remise
du développeur (sa clé hors-ligne) : v06/sceau-I/a-signer.txt.

Usage :
  python3 build_m8.py                  # construction 0.9.0-dev.1 (+ carte gén. 8)
  python3 build_m8.py --verifier [--graine N] [--volume complet|reduit]
                                       # re-vérification + cristallisation R6
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
M4_DIR = os.path.join(TRIADE, "m4")
M5_DIR = os.path.join(TRIADE, "m5")
# Le builder M5 charge ses modules par imports PLAINS (oracle_m4, oracle_m5,
# carte_m5) : ses répertoires doivent être sur le chemin AVANT son
# chargement (miroir du builder M5 pour le M4 — la chaîne complète est
# re-vérifiée à chaque build M8, R5/R7).
for _d in (M4_DIR, os.path.join(M4_DIR, "outils"), M5_DIR,
           os.path.join(M5_DIR, "outils"), ICI, os.path.join(ICI, "outils")):
    if _d not in sys.path:
        sys.path.insert(0, _d)


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# La chaîne d'héritage : plan M4 -> builder M4 (qui charge build_m3) ->
# builder M5 (qui charge oracle_m4/oracle_m5/carte_m5 et le plan M5 sous
# « layout ») — puis le plan M8 et le harnais SOUS NOMS PROPRES (leçon
# D158 ; le harnais RÉUTILISE les modules déjà chargés, une seule instance).
L4 = _charger_module("layout_m4", os.path.join(M4_DIR, "layout.py"))
B4 = _charger_module("build_m4", os.path.join(M4_DIR, "build_m4.py"))
B5 = _charger_module("build_m5", os.path.join(M5_DIR, "build_m5.py"))
L = _charger_module("layout_m8", os.path.join(ICI, "layout.py"))   # plan M8
harnais = _charger_module("harnais_sys", os.path.join(ICI, "harnais_sys.py"))
import carte_m8 as cm8  # noqa: E402  # génération 8 (lignée D80, graine durable D144)

import capstone  # noqa: E402
import pefile  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

# Les primitives de notation sont CELLES du builder M4 (une seule
# implémentation — miroir build_m5 : lignes_notation/assembler_bloc/
# round_trip/canon/deplacements_declares).
lignes_notation = B4.lignes_notation
taille_declaree = B4.taille_declaree
assembler_bloc = B4.assembler_bloc
round_trip = B4.round_trip
canon = B4.canon
operande_rip_cible = B4.operande_rip_cible
deplacements_declares = B4.deplacements_declares
EchecOracle = B4.od4.EchecOracle if hasattr(B4, "od4") else None

# --- Garde sceau de l'Intention (D87) -------------------------------------------
# L'héritage win m0-m5 est signé (cérémonies réelles — la 0.6.0 du 04/11 a
# remis 11 lignes) ; l'arbre m8 (le domaine sys, avec ses errata D161)
# NÉCESSITE la cérémonie de l'ère M8 : sceau_I.py preparer a écrit
# a-signer.txt — la remise du développeur (sa clé hors-ligne) est EXIGÉE
# avant tout build (le refus est NOMMÉ, jamais contourné).
SCEAU_I = B4.SCEAU_I
ARBRES_GARDE_M8 = ["m0", "m1", "m2", "m3", "m4", "m5", "m8"]


def _garde_sceau_I() -> None:
    try:
        SCEAU_I.garde(ARBRES_GARDE_M8)
        print(f"[sceau-I] garde : {len(ARBRES_GARDE_M8)} arbres d'intention "
              f"conformes à leurs signatures ({', '.join(ARBRES_GARDE_M8)}) ; "
              f"clé déposée : {SCEAU_I.etat_cle()}")
    except SCEAU_I.EchecSceauI as exc:
        raise EchecBuild(
            f"{exc}\n  [cérémonie] la remise du développeur est requise : "
            f"v06/sceau-I/a-signer.txt (signer hors-ligne les arbres divergés/"
            f"nouveaux — au minimum m0 [registre étendu M8] et m8 [le domaine "
            f"sys] — puis : python3 v06/sceau_I.py deposer signatures-I.txt "
            f"--cle cle-publique-I.txt)") from exc


# --- Le scellé 0.6.0 (l'ancre R7 de l'ère M8) ------------------------------------

SHA_PROXY_060 = "c1e46fb0b857b6f33c67aa7f26a1db3064f2e3adbd528414116b497220b6a20c"
# le proxy.exe 0.6.0 scellé (l'artefact du run e4 + la carte génération 7
# scellée version=0.6.0 — le scellage est un fait de carte, D104 ; le sha
# est celui de l'artefact, identique du dev.2 à la finale)

# --- Blocs M8 embarqués dans .text5 (couche C, génération 8 — g9xxxx) ------------

BLOCS_M8 = [
    ("g90001", "sys-01:R1", "sys-01-emetteur", L.SYS01_VA, L.SLOTS_SYS["g90001"][1]),
    ("g90002", "sys-02:R1", "sys-02-resolveur", L.SYS02_VA, L.SLOTS_SYS["g90002"][1]),
    ("g90003", "sys-03:R1", "sys-03-ecriture", L.SYS03_VA, L.SLOTS_SYS["g90003"][1]),
]
assert all((b[3], b[4]) == L.SLOTS_SYS[b[0]] for b in BLOCS_M8), \
    "BLOCS_M8 diverge du plan d'adressage (layout.py, source unique — D161)"

# L'héritage M4+M5 complet (io, libc, tcp, http, tls, les révisions R2/R3)
# est repris OCTET POUR OCTET (R7) — le build_m8 le lit via B5/B4.
BLOCS_EMBARQUES_M8 = B5.BLOCS_EMBARQUES_M5 + BLOCS_M8

_CLE_BLOB = {"g90001": "sys-01", "g90002": "sys-02", "g90003": "sys-03"}


def chemin_notation_m8(fichier: str) -> str:
    return os.path.join(ICI, "notation", fichier + ".asm")


# --- Couche I M8 : lecture et audit du gabarit ----------------------------------
# Le gabarit des blocs de DOMAINE (charte m8/I/README.md) : l'Intention et
# le Contrat (pre/post/inv) vivent dans CHAQUE spec ; la Provenance
# (écrite-avant-code, R2) et les références vivent au README du domaine —
# la charte LIE les trois spécifications (l'audit exige l'un ET l'autre).

def lire_spec_m8(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)),
            "texte": texte}
    for bloc in ("Intention", "Contrat", "pre", "post", "inv"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    return spec


_FICHIERS_I_M8 = {
    "g90001": "sys-01-emetteur.md",
    "g90002": "sys-02-resolveur.md",
    "g90003": "sys-03-ecriture.md",
}


def charger_couche_I_m8() -> dict[str, dict]:
    specs = {}
    readme = os.path.join(ICI, "I", "README.md")
    with open(readme, encoding="utf-8") as f:
        texte_readme = f.read()
    if "écrite-avant-code" not in texte_readme:
        raise EchecBuild("m8/I/README.md : la provenance écrite-avant-code "
                         "absente de la charte (R2)")
    for bid, sid, _f, _r, _s in BLOCS_M8:
        ident, rev_ref = sid.split(":")
        chemin = os.path.join(ICI, "I", _FICHIERS_I_M8[bid])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec_m8(chemin)
        if spec["id"] != ident:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {ident}")
        if spec["rev"] != int(rev_ref[1:]):
            raise EchecBuild(f"{chemin} : révision {spec['rev']} != R{rev_ref[1:]}")
        specs[bid] = spec
    return specs


# --- Oracle structurel M8 : les invariants de I, par bloc ------------------------
# LA RÈGLE DU DOMAINE (charte § 3, D160) : AUCUN IAT PAR BLOC sys — la
# seule interaction système du domaine est l'instruction syscall ELLE-MÊME
# (sys-01) ; ntdll est LUE (sys-02), jamais appelée.

IAT_M8 = {
    "g90001": set(),   # I1 : le site syscall est l'unique interaction
    "g90002": set(),   # I5 : aucun IAT — memcmp est un appel DIRECT déclaré
    "g90003": set(),   # I1 : la twin se preuve à l'oracle structurel
}
APPELS_DIRECTS_M8 = {
    "g90001": set(),                       # le trombone n'appelle RIEN
    "g90002": {L.MEMCMP_VA},               # I2 : memcmp libc-02, le seul
    "g90003": {L.SYS02_VA, L.SYS01_VA},    # I3 : résoudre PUIS émettre
}
DONNEES_RIP_M8 = {
    "g90001": set(),
    "g90002": set(),       # ntdll est lue par POINTEURS fournis (P1-P3)
    "g90003": {L.R_SYS_NOM, L.R_SYS_LIGNE},   # I4 : les fixtures CITÉES
}
FEUILLES_M8 = {"g90001"}

_SLOTS_IAT_COMPLETS = {**B5.L4.IAT_SLOTS, **B5.L4.IAT_SEC32_SLOTS,
                       **B5.L.IAT_M5_SLOTS}


def _externe(bid: str, insn, adresses_bloc: set, adresse_entree: int) -> str | None:
    if "rip" in insn.op_str:
        cible = operande_rip_cible(insn)
        slots = {v: n for n, v in _SLOTS_IAT_COMPLETS.items()}
        return f"iat:{slots[cible]}" if cible in slots else f"rip:{cible:#x}"
    if insn.op_str.startswith("0x"):
        cible = int(insn.op_str, 16)
        if cible in adresses_bloc and cible != adresse_entree:
            return "interne"
        return f"bloc:{cible:#x}"
    return None


def oracle_structurel_m8(specs: dict, code: dict, blocs: list[tuple]) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    for bid, sid, fichier, rva, slot in blocs:
        insns = code[bid]["insns"]
        mnemos = [i.mnemonic for i in insns]
        adresses_insns = {i.address for i in insns}
        internes_autorises = APPELS_DIRECTS_M8.get(bid, set()) | (
            {a for a in adresses_insns if a != rva} if bid in FEUILLES_M8 else set())

        for i in insns:
            if i.mnemonic.startswith("j"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}",
                       cible in adresses_insns, f"cible {cible:#x} hors frontière")

        for i in insns:
            if i.mnemonic == "call":
                classe = _externe(bid, i, adresses_insns, rva)
                if classe is None:
                    continue
                if classe.startswith("iat:"):
                    # LA RÈGLE DU DOMAINE : aucun slot IAT n'est jamais
                    # autorisé — la preuve structurelle (charte § 3)
                    verrou(f"{bid}:AUCUN-IAT@{i.address:#x}",
                           classe[4:] in IAT_M8.get(bid, set()),
                           f"{classe} — AUCUN IAT PAR BLOC sys (charte § 3)")
                elif classe.startswith("bloc:"):
                    verrou(f"{bid}:appel-autorise@{i.address:#x}",
                           int(classe[5:], 16) in internes_autorises,
                           f"{classe} hors blocs déclarés")

        cibles_rip: set[int] = set()
        for i in insns:
            cible = operande_rip_cible(i)
            if cible is not None and i.mnemonic != "call":
                cibles_rip.add(cible)
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP_M8.get(bid, set())
                       or rva <= cible < rva + slot,
                       f"cible {cible:#x} hors données déclarées")

        declarees = deplacements_declares(chemin_notation_m8(fichier))
        if declarees is not None:
            rip_reelles = {operande_rip_cible(i) for i in insns}
            rip_reelles.discard(None)
            verrou(f"{bid}:deplacements-rip-declares", rip_reelles == declarees,
                   f"réelles {sorted(hex(c) for c in rip_reelles - declarees)} "
                   f"non déclarées / déclarées {sorted(hex(c) for c in declarees - rip_reelles)} absentes")

        # LE SITE SYSCALL : exactement UN dans sys-01 (Q1), AUCUN ailleurs
        # (I4 de sys-02 : le bloc qui LIT n'ÉMET pas ; sys-03 émet PAR sys-01)
        nb_syscall = sum(1 for m in mnemos if m in ("syscall", "sysenter"))
        if bid == "g90001":
            verrou("g90001:site-syscall-unique", nb_syscall == 1,
                   f"{nb_syscall} instructions syscall (Q1 : exactement un)")
            verrou("g90001:six-octets-trombone",
                   [f"{i.mnemonic} {i.op_str}".strip() for i in insns] ==
                   ["mov r10, rcx", "syscall", "ret"],
                   "le trombone est TROIS instructions : mov r10, rcx ; "
                   "syscall ; ret (I3/I6)")
            # I2 : rax n'est JAMAIS écrit avant le site (le SSN traverse)
            idx_syscall = mnemos.index("syscall")
            verrou("g90001:rax-jamais-ecrit-avant-le-site",
                   not any(i.mnemonic.startswith("mov") and
                           i.op_str.split(",")[0].strip() in ("rax", "eax")
                           for i in insns[:idx_syscall]),
                   "écrire rax avant le site détournerait le SSN (I2)")
            # I6 : le ret suit IMMÉDIATEMENT le site
            verrou("g90001:ret-immediat",
                   idx_syscall == len(insns) - 2 and insns[-1].mnemonic == "ret",
                   "après le verdict du noyau, la main rendue est la suivante (I6)")
            # I3 : AUCUN prologue (aucun push, aucun sub rsp, aucune écriture)
            verrou("g90001:aucun-prologue",
                   not any(i.mnemonic in ("push", "sub") and "rsp" in i.op_str
                           for i in insns[:idx_syscall]),
                   "la pile de l'appelant EST la pile du syscall (I3)")
        else:
            verrou(f"{bid}:aucun-syscall", nb_syscall == 0,
                   f"{nb_syscall} instruction(s) syscall — le domaine sépare "
                   f"LIRE (sys-02) et ÉMETTRE (sys-01, I4)")

        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16,
               f"écart {rva + slot - fin_code}")
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)

        for i in insns:
            if i.mnemonic.startswith("mov") and "[" in i.op_str and \
                    i.op_str.split(",")[0].strip().endswith("]"):
                base = re.search(r"\[(\w+)", i.op_str)
                if base and base.group(1) == "rsp":
                    disp = re.search(r"\+ (0x[0-9a-f]+)\]", i.op_str)
                    verrou(f"{bid}:pas-de-stockage-sous-rsp@{i.address:#x}",
                           disp is None or int(disp.group(1), 16) >= 0)

        npush = 0
        while npush < len(insns) and insns[npush].mnemonic == "push":
            npush += 1
        premier_externe = next((k for k, i in enumerate(insns)
                                if i.mnemonic == "call" and _externe(
                                    bid, i, adresses_insns, rva)
                                not in (None, "interne")), None)
        if premier_externe is not None:
            ok = False
            for k in range(premier_externe):
                if insns[k].mnemonic == "sub" and insns[k].op_str.startswith("rsp,"):
                    imm = int(insns[k].op_str.split(",")[1].strip(), 16)
                    ok = (8 + 8 * npush - imm) % 16 == 0
                    break
            verrou(f"{bid}:pile-alignee", ok, "prologue non aligné avant appel externe")

    # g90002 — I3 : le MOTIF est vérifié AVANT l'imm32 (l'ordre est le contrat)
    m = code["g90002"]["insns"]
    idx_motif = next((k for k, i in enumerate(m)
                      if i.mnemonic == "cmp" and "0xb8d18b4c" in i.op_str), None)
    idx_imm = next((k for k, i in enumerate(m)
                    if i.mnemonic == "mov" and i.op_str.startswith("eax, dword ptr [rdx + 4]")), None)
    verrou("g90002:motif-avant-imm32",
           idx_motif is not None and idx_imm is not None and idx_motif < idx_imm,
           "les quatre octets du MOTIF_STUB d'abord, le numéro à +4 ensuite (I3)")
    verrou("g90002:memcmp-le-seul-appel",
           [i.op_str for i in m if i.mnemonic == "call" and
            i.op_str.startswith("0x")] == [f"{L.MEMCMP_VA:#x}"],
           "memcmp libc-02 est l'unique appel direct (I2)")
    # g90002 — I1 : la borne NumberOfNames lue UNE fois ([r10 + 0x18])
    lectures_borne = [i for i in m if i.mnemonic == "mov" and
                      f"[r10 + {L.EXP_NBNOMS:#x}]" in i.op_str]
    verrou("g90002:borne-lue-une-fois", len(lectures_borne) == 1,
           f"{len(lectures_borne)} lectures de NumberOfNames (I1)")

    # g90003 — I3 : l'ordre est le contrat (résoudre AVANT émettre) ;
    # I5 : l'échec de résolution court-circuite l'émission (le js)
    m = code["g90003"]["insns"]
    appels = [(k, i.op_str) for k, i in enumerate(m) if i.mnemonic == "call"]
    verrou("g90003:ordre-resoudre-puis-emettre",
           [a[1] for a in appels] == [f"{L.SYS02_VA:#x}", f"{L.SYS01_VA:#x}"],
           f"appels constatés : {[a[1] for a in appels]} (I3)")
    idx_res = next(k for k, _ in appels)
    idx_test = next((k for k in range(idx_res, len(m))
                     if m[k].mnemonic == "test" and m[k].op_str == "rax, rax"), None)
    verrou("g90003:echec-court-circuite",
           idx_test == idx_res + 1 and m[idx_test + 1].mnemonic == "js",
           "le verdict du résolveur est testé et court-circuite l'émission (I5)")

    # Traçabilité : chaque bloc a sa spécification chargée (D24)
    attendus = {b for b, *_ in blocs}
    verrou("tracabilite-I", attendus <= set(specs), str(attendus - set(specs)))
    return verrous


# --- L'héritage complet (M3+M4+M5 re-vérifié, la preuve R7 absolue) ---------------

def heritage_complet() -> dict:
    """Re-vérifie TOUT l'héritage (R5 + oracles structurels M3/M4/M5) et
    compose l'image M5 — confrontée OCTET PAR OCTET au scellé 0.6.0."""
    specs_m4, code_m4, verrous_m4 = B4.assembler_tout_m4()
    blocs_m3, _specs_m3, code_m3, verrous_m3 = B4.B3.assembler_tout()
    texte_m3, rdata_m3, data_m3, text2_m3 = B4.B3.composer_sections(code_m3, blocs_m3)
    print(f"[héritage] M3 : {len(verrous_m3)} verrous ; M4 : {len(verrous_m4)} verrous")

    specs_m5, code_m5, verrous_m5 = B5.assembler_tout_m5()
    sections_m4 = B4.composer_image_m4(
        texte_m3, rdata_m3, data_m3, text2_m3, code_m4,
        code_m4["b20007"]["slot"])
    texte, rdata, data, text2, text3, text4 = B5.composer_image_m5(
        sections_m4[0], sections_m4[1], sections_m4[2], sections_m4[3],
        sections_m4[4], code_m5)
    exe_m5_compose = B5.ecrire_pe32plus(texte, rdata, data, text2, text3, text4)
    with open(os.path.join(M5_DIR, "proxy.exe"), "rb") as f:
        scelle_060 = f.read()
    if hashlib.sha256(scelle_060).hexdigest() != SHA_PROXY_060:
        raise EchecBuild("m5/proxy.exe diverge du scellé 0.6.0 (c1e46fb0…) — "
                         "l'ancre R7 de l'ère M8 est rompue")
    if hashlib.sha256(exe_m5_compose).hexdigest() != hashlib.sha256(scelle_060).hexdigest():
        raise EchecBuild("l'image M5 composée diverge du scellé 0.6.0 "
                         "(c1e46fb0…) — R7")
    print(f"[R7] l'image M5 composée == le scellé 0.6.0 OCTET PAR OCTET "
          f"(sha {SHA_PROXY_060[:16]}…) — la carte génération 7 scellée "
          f"prouve CES octets (version=0.6.0, le fait de carte D104)")
    return {"code_m3": code_m3, "code_m4": code_m4, "code_m5": code_m5,
            "specs_m5": specs_m5, "verrous_m3": verrous_m3,
            "verrous_m4": verrous_m4, "verrous_m5": verrous_m5,
            "sections_m5": (texte, rdata, data, text2, text3, text4)}


# --- Assemblage + vérification -----------------------------------------------------

def assembler_tout_m8() -> tuple[dict, dict, list]:
    """Les trois blocs du domaine : assemblage, tailles déclarées, round-trip."""
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    specs = charger_couche_I_m8()
    code: dict[str, dict] = {}
    for bid, sid, fichier, rva, slot in BLOCS_M8:
        chemin = chemin_notation_m8(fichier)
        octets, metas = assembler_bloc(ks, chemin, rva, slot)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot_complet = octets + b"\x90" * (slot - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns,
                     "slot": slot_complet}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, "
              f"round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel_m8(specs, code, BLOCS_M8)
    print(f"[oracle] structurel M8 : {len(verrous)} verrous PASS "
          f"(LA RÈGLE AUCUN IAT PAR BLOC sys constatée — charte § 3)")
    return specs, code, verrous


def blobs_sys(code_m8: dict) -> dict[str, bytes]:
    return {_CLE_BLOB[bid]: code_m8[bid]["octets"] for bid, *_ in BLOCS_M8}


# --- Composition de l'image M8 ----------------------------------------------------

def _somme_qwords(octets: bytes) -> int:
    return sum(struct.unpack(f"<{len(octets) // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF


def tranche_section(exe: bytes, rva: int, taille: int) -> bytes:
    """La tranche d'une section aux RVA du plan M8 (.text5 comprise)."""
    if rva < L.TEXT5_VA:
        return B5.tranche_section(exe, rva, taille)
    if rva >= L.TEXT5_VA + 0x2000:
        raise EchecBuild(f"RVA {rva:#x} hors sections")
    return exe[L.TEXT5_FILE + (rva - L.TEXT5_VA):
               L.TEXT5_FILE + (rva - L.TEXT5_VA) + taille]


def composer_image_m8(sections_m5: tuple, code: dict):
    """-> (texte, rdata, data, text2, text3, text4, text5) — proxy.exe M8."""
    texte, rdata_m5, data, text2, text3, text4 = sections_m5

    # .text5 : la section NOUVELLE — la réserve est int3 (convention des
    # zones réservées), les slots portent code + padding NOP (D161/I7)
    text5 = bytearray(b"\xcc" * 0x2000)
    for bid, _sid, _f, rva, slot in BLOCS_M8:
        text5[rva - L.TEXT5_VA: rva - L.TEXT5_VA + slot] = code[bid]["slot"]

    # .rdata : héritage M5 OCTET POUR OCTET + l'extension du domaine
    rdata = bytearray(rdata_m5)
    if len(rdata) != B5.L.RDATA_VSIZE:
        raise EchecBuild(f".rdata héritée : {len(rdata)} o != {B5.L.RDATA_VSIZE:#x}")
    # la zone d'extension du domaine est VIERGE dans le scellé (vérifiée
    # D161 : 0x2EB0-0x2FFF nuls — le corps ne bouge d'AUCUN octet, R7)
    zone = bytes(rdata[L.R_SYS_NOM - 0x2000: 0x1000])
    if any(zone):
        raise EchecBuild("la zone .rdata du domaine (0x2EB0-0x2FFF) n'est "
                         "pas vierge dans l'héritage — R7 rompu")

    _poses: list[tuple[int, int, str]] = []

    def poser(rva_c: int, donnees: bytes, nom: str = ""):
        fin = rva_c + len(donnees)
        if fin > L.R_SYS_BORNE:
            raise EchecBuild(f".rdata du domaine débordante à {rva_c:#x} "
                             f"(la borne {L.R_SYS_BORNE:#x}, miroir D95)")
        if rva_c < 0x2EB0:
            raise EchecBuild(f"extension M8 sous 0x2EB0 (R7 rompu) : "
                             f"{nom or hex(rva_c)}")
        for rva_p, fin_p, nom_p in _poses:
            if rva_c < fin_p and rva_p < fin:
                raise EchecBuild(
                    f"chevauchement .rdata M8 : {nom or hex(rva_c)} "
                    f"[{rva_c:#x}, {fin:#x}) recouvre {nom_p} "
                    f"[{rva_p:#x}, {fin_p:#x})")
        _poses.append((rva_c, fin, nom or hex(rva_c)))
        rdata[rva_c - 0x2000: rva_c - 0x2000 + len(donnees)] = donnees

    # les fixtures du domaine (garde-fous de longueurs — la notation porte
    # ces valeurs ; le span-nom SANS NUL : P1 de sys-02 est un SPAN)
    if len(L.TXT_SYS_NOM) != L.LEN_SYS_NOM:
        raise EchecBuild(f"garde-fou span-nom : {len(L.TXT_SYS_NOM)} o "
                         f"!= {L.LEN_SYS_NOM}")
    poser(L.R_SYS_NOM, L.TXT_SYS_NOM, "span-nom")
    if len(L.TXT_SYS_LIGNE) != L.LEN_SYS_LIGNE + 1:
        raise EchecBuild(f"garde-fou fixture-ligne : {len(L.TXT_SYS_LIGNE)} o "
                         f"!= {L.LEN_SYS_LIGNE + 1}")
    poser(L.R_SYS_LIGNE, L.TXT_SYS_LIGNE, "fixture-ligne")

    # LA VERSION : le delta documenté (R10 : geste de BUILD — 0x00090001 >
    # 0x00060001 du scellé 0.6.0, plancher 0x00040000 inchangé ; JAMAIS un
    # scellage : la 0.9.0 finale attend le terrain vert du chantier (d))
    struct.pack_into("<Q", rdata, B5.L4.R_VERSION - 0x2000, L.VERSION_U64_DEV1)

    return (bytes(texte), bytes(rdata), bytes(data), bytes(text2),
            bytes(text3), bytes(text4), bytes(text5))


# --- Éditeur PE32+ (sept sections) ---------------------------------------------------

def ecrire_pe32plus(texte: bytes, rdata: bytes, data: bytes, text2: bytes,
                    text3: bytes, text4: bytes, text5: bytes) -> bytes:
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 7, 0, 0, 0, 0xF0, 0x0002)
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B, 0, 0,
        B5.L.ENTREE, len(texte) + len(text2) + len(text3) + len(text4), 0,
        B5.L.ENTREE_M5, B5.L.TEXT_RVA,  # AddressOfEntryPoint : 0x8C80 INCHANGÉ
                                       # (http-12:R3 — le principal n'est PAS
                                       # recâblé, R7 ; le domaine est la pièce
                                       # rapportée, câblée au chantier (d))
        B5.L.IMAGE_BASE,
        B5.L.SECT_ALIGN, B5.L.FILE_ALIGN,
        6, 0, 0, 1, 6, 0, 0,
        L.SIZE_OF_IMAGE,               # 0xC000 (0xA000 + .text5)
        B5.L.TEXT_FILE,                # SizeOfHeaders : 0x400 (INCHANGÉ —
                                       # 7 en-têtes = 608 o, la marge suffit :
                                       # le décalage D94 n'est PAS rejoué)
        0,
        3,                             # Subsystem : CONSOLE
        B5.L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    dirs = [(0, 0)] * 16
    dirs[1] = (B5.L.R_IMPORTS_M5, 100)   # le répertoire d'imports M5 INCHANGÉ
    dirs[5] = (B5.L4.R_RELOC, 12)
    dirs[12] = (B5.L4.L3.R_IAT, 88)
    opt = bytes(opt_fixe) + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr,
                           0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", B5.L.TEXT_VSIZE, B5.L.TEXT_RVA, B5.L.TEXT_VSIZE,
           B5.L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", B5.L.RDATA_VSIZE, B5.L.RDATA_RVA, B5.L.RDATA_VSIZE,
             B5.L.RDATA_FILE, 0x40000040)
        + sh(b".data\x00\x00\x00", B5.L.DATA_VSIZE, B5.L.DATA_RVA, B5.L.DATA_RAW,
             B5.L.DATA_FILE, 0xC0000040)
        + sh(b".text2\x00\x00", B5.L.TEXT2_VSIZE, B5.L.TEXT2_RVA, B5.L.TEXT2_VSIZE,
             B5.L.TEXT2_FILE, 0x60000020)
        + sh(b".text3\x00\x00", B5.L.TEXT3_VSIZE, B5.L.TEXT3_RVA, B5.L.TEXT3_VSIZE,
             B5.L.TEXT3_FILE, 0x60000020)
        + sh(b".text4\x00\x00", B5.L.TEXT4_VSIZE, B5.L.TEXT4_RVA, B5.L.TEXT4_VSIZE,
             B5.L.TEXT4_FILE, 0x60000020)
        + sh(b".text5\x00\x00", 0x2000, L.TEXT5_VA, 0x2000,
             L.TEXT5_FILE, 0x60000020)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 280, len(entetes)
    assert len(entetes) <= B5.L.TEXT_FILE, "les 7 en-têtes débordent SizeOfHeaders"
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[B5.L.TEXT_FILE:B5.L.TEXT_FILE + len(texte)] = texte
    exe[B5.L.RDATA_FILE:B5.L.RDATA_FILE + len(rdata)] = rdata
    exe[B5.L.DATA_FILE:B5.L.DATA_FILE + len(data)] = data
    exe[B5.L.TEXT2_FILE:B5.L.TEXT2_FILE + len(text2)] = text2
    exe[B5.L.TEXT3_FILE:B5.L.TEXT3_FILE + len(text3)] = text3
    exe[B5.L.TEXT4_FILE:B5.L.TEXT4_FILE + len(text4)] = text4
    exe[L.TEXT5_FILE:L.TEXT5_FILE + len(text5)] = text5
    return bytes(exe)


# --- Validation PE -------------------------------------------------------------------

def valider_pe(exe: bytes):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.NumberOfSections == 7, "sections != 7"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == B5.L.ENTREE_M5, \
        f"point d'entrée != {B5.L.ENTREE_M5:#x} (http-12:R3 — INCHANGÉ, R7)"
    assert pe.OPTIONAL_HEADER.ImageBase == B5.L.IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HEVA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE, \
        f"SizeOfImage != {L.SIZE_OF_IMAGE:#x}"
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2", ".text3", ".text4",
                    ".text5"], noms
    assert pe.sections[6].Characteristics & 0x60000020 == 0x60000020, \
        ".text5 non RX"
    assert pe.sections[6].VirtualAddress == L.TEXT5_VA
    assert pe.sections[6].PointerToRawData == L.TEXT5_FILE, \
        f".text5 raw != {L.TEXT5_FILE:#x}"
    assert pe.sections[2].SizeOfRawData == B5.L.DATA_RAW
    assert pe.OPTIONAL_HEADER.SizeOfHeaders == B5.L.TEXT_FILE, "SizeOfHeaders != 0x400"
    for s, attendu in zip(pe.sections, (B5.L.TEXT_FILE, B5.L.RDATA_FILE,
                                        B5.L.DATA_FILE, B5.L.TEXT2_FILE,
                                        B5.L.TEXT3_FILE, B5.L.TEXT4_FILE,
                                        L.TEXT5_FILE)):
        assert s.PointerToRawData == attendu, \
            f"PointerToRawData {s.Name.decode().rstrip(chr(0))} != {attendu:#x}"
    # Le répertoire d'imports : INCHANGÉ (kernel32 x2 descripteurs, ws2_32,
    # secur32 — le domaine ne déclare RIEN, la preuve structurelle)
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports.setdefault(entree.dll.decode().lower(), []).extend(
            i.name.decode() for i in entree.imports)
    assert imports["kernel32.dll"] == ["GetCommandLineW"] + B5.L4.L3.KERNEL32_IMPORTS
    assert imports["ws2_32.dll"] == B5.L4.L3.WS2_IMPORTS
    assert imports["secur32.dll"] == B5.L4.SECUR32_IMPORTS
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress == B5.L.R_IMPORTS_M5
    assert len(exe) == L.TAILLE_FICHIER, "taille de fichier inattendue"
    # Zones réservées : int3 dans l'image livrée (héritage + .text5 — la
    # réserve du domaine 0xA240 : la croissance sys-04 et suivants)
    for rva in (0x4200, 0x45C0, 0x4800, 0x7FC0, 0x8FC0, 0xA240):
        assert tranche_section(exe, rva, 1)[0] == 0xCC, \
            f"zone réservée @{rva:#x} != int3"
    # Version (R10 : geste de BUILD — 0x00090001 > 0x00060001 du scellé)
    version = struct.unpack("<Q", tranche_section(exe, B5.L4.R_VERSION, 8))[0]
    assert version == L.VERSION_U64_DEV1, f"version {version:#x} != 0x00090001"
    assert version >= L.VERSION_U64_MIN, "le plancher R10 est franchi"
    # R_POLITIQUE @0x3860 : l'état image reste 0 (héritage)
    politique = struct.unpack("<Q", tranche_section(exe, B5.L.R_POLITIQUE, 8))[0]
    assert politique == 0, "R_POLITIQUE divergente (R7)"
    # Les fixtures du domaine : concordance exacte (le span SANS NUL, la
    # ligne byte-exact le MESSAGE M0)
    assert tranche_section(exe, L.R_SYS_NOM, L.LEN_SYS_NOM) == L.TXT_SYS_NOM, \
        "le span-nom divergent"
    assert tranche_section(exe, L.R_SYS_LIGNE, L.LEN_SYS_LIGNE + 1) == \
        L.TXT_SYS_LIGNE, "la fixture-ligne divergente"
    # la réserve .rdata au-delà de la borne : VIERGE
    assert not any(tranche_section(exe, L.R_SYS_BORNE, 0x100)), \
        "la réserve .rdata 0x2F00-0x2FFF n'est pas vierge"
    # La porte M5 : UNE entrée, la somme recalculée == la somme portée
    # (.text4 INCHANGÉ — la somme est celle du scellé)
    r, t, s = struct.unpack("<IIQ", tranche_section(exe, B5.L.R_TAB_SUM_M5, 16))
    assert (r, t) == (B5.L.TEXT4_RVA, B5.L.TEXT4_VSIZE), "l'entrée M5 divergente"
    assert s == _somme_qwords(tranche_section(exe, r, t)), \
        "porte M5 : la somme de .text4 divergente"
    # La porte héritée R10 : la marche complète (28 entrées) auto-consistante
    k = 0
    rva_table = B5.L4.R_TAB_SUM
    while rva_table + 16 * k < B5.L4.R10_BORNE:
        r2, t2, s2 = struct.unpack("<IIQ",
                                   tranche_section(exe, rva_table + 16 * k, 16))
        assert r2 != 0 and t2 != 0, \
            f"porte R10 : entrée #{k + 1} trouée (fail-closed D95)"
        assert s2 == _somme_qwords(tranche_section(exe, r2, t2)), \
            f"porte R10 : somme de {r2:#x} divergente"
        k += 1
        assert k <= B5.L4.R10_NB_ENTREES, "porte R10 : borne franchie"
    assert k == B5.L4.R10_NB_ENTREES, f"porte R10 : {k} entrées != 28"
    return True


# --- Preuve de réutilisation (R7 — l'héritage 0.6.0) ----------------------------

def preuve_reutilisation(exe: bytes) -> dict:
    """proxy.exe M8 partage son squelette avec le scellé 0.6.0 : .text/
    .text2/.data/.text3/.text4 OCTET POUR OCTET ; .rdata identique SAUF la
    version @0x2820 (LE delta R10 documenté — geste de BUILD) et l'extension
    du domaine 0x2EB0-0x2EFF (la zone VIERGE vérifiée, D161) ; les deltas PE
    sont documentés (7e section, SizeOfImage, taille)."""
    with open(os.path.join(M5_DIR, "proxy.exe"), "rb") as f:
        scelle = f.read()
    if hashlib.sha256(scelle).hexdigest() != SHA_PROXY_060:
        raise EchecBuild("m5/proxy.exe diverge du scellé 0.6.0 (c1e46fb0…) — "
                         "l'ancre R7 de l'ère M8 est rompue")
    for nom, rva_base, vsize, fichier in (
            (".text", B5.L.TEXT_RVA, B5.L.TEXT_VSIZE, B5.L.TEXT_FILE),
            (".text2", B5.L.TEXT2_RVA, B5.L.TEXT2_VSIZE, B5.L.TEXT2_FILE),
            (".data", B5.L.DATA_RVA, B5.L.DATA_RAW, B5.L.DATA_FILE),
            (".text3", B5.L.TEXT3_RVA, B5.L.TEXT3_VSIZE, B5.L.TEXT3_FILE),
            (".text4", B5.L.TEXT4_RVA, B5.L.TEXT4_VSIZE, B5.L.TEXT4_FILE)):
        section = tranche_section(exe, rva_base, vsize)
        scelle_section = scelle[fichier: fichier + vsize]
        if section != scelle_section:
            for k, (x, y) in enumerate(zip(section, scelle_section)):
                if x != y:
                    raise EchecBuild(f"R7 rompu : {nom} diverge du scellé "
                                     f"0.6.0 à l'octet {k:#x}")
    # .rdata : identique au scellé SAUF la version (LE delta documenté) et
    # l'extension du domaine (la zone vierge vérifiée) — le même arbitrage
    # que la preuve M5 pour sa version. Les tranches INTACTES sont
    # comparées au scellé ; les TROUÉES du domaine (autour des fixtures)
    # sont exigées VIERGES DES DEUX CÔTÉS
    for debut, fin in ((0x2000, B5.L4.R_VERSION),
                       (B5.L4.R_VERSION + 8, 0x2EB0)):
        if tranche_section(exe, debut, fin - debut) != \
                scelle[B5.L.RDATA_FILE + (debut - 0x2000):
                       B5.L.RDATA_FILE + (debut - 0x2000) + (fin - debut)]:
            raise EchecBuild(f"R7 rompu : .rdata diverge du scellé 0.6.0 "
                             f"entre {debut:#x} et {fin:#x} (hors version)")
    fin_span = L.R_SYS_NOM + L.LEN_SYS_NOM          # 0x2ECB
    fin_ligne = L.R_SYS_LIGNE + L.LEN_SYS_LIGNE + 1  # 0x2EF2
    for debut, fin, nom_t in ((0x2EB0, L.R_SYS_NOM, "avant le span-nom"),
                              (fin_span, L.R_SYS_LIGNE, "entre les fixtures"),
                              (fin_ligne, 0x3000, "après la ligne — la réserve")):
        if any(tranche_section(exe, debut, fin - debut)):
            raise EchecBuild(f"R7 rompu : .rdata M8 non vierge {nom_t} "
                             f"[{debut:#x}, {fin:#x}) — la zone libre du "
                             f"scellé ne reçoit QUE les fixtures déclarées")
        if any(scelle[B5.L.RDATA_FILE + (debut - 0x2000):
                      B5.L.RDATA_FILE + (debut - 0x2000) + (fin - debut)]):
            raise EchecBuild(f"R7 rompu : la zone {nom_t} [{debut:#x}, {fin:#x}) "
                             f"n'est pas vierge dans le scellé 0.6.0 — l'ancre "
                             f"de l'ère M8 est fausse")
    # les deltas PE documentés
    pe_m8 = pefile.PE(data=exe)
    pe_s = pefile.PE(data=scelle)
    assert pe_m8.FILE_HEADER.NumberOfSections == 7
    assert pe_s.FILE_HEADER.NumberOfSections == 6
    assert pe_m8.OPTIONAL_HEADER.SizeOfImage == 0xC000
    assert pe_s.OPTIONAL_HEADER.SizeOfImage == 0xA000
    assert pe_m8.OPTIONAL_HEADER.AddressOfEntryPoint == \
        pe_s.OPTIONAL_HEADER.AddressOfEntryPoint == B5.L.ENTREE_M5
    return {"sha_proxy_060": SHA_PROXY_060,
            "blocs_reutilises": len(BLOCS_EMBARQUES_M8) - len(BLOCS_M8)}


# --- Carte génération 8 : tables, fragments, verrou croisé (modèle D104/D144) -----

CONTRATS_M8 = {
    "g90001": ("(ssn en rax, arguments aux loges NT) -> NTSTATUS dans rax",
               "P1 rax = le SSN (le numero de service, une DONNEE chargee par "
               "l appelant — charte § 1 : jamais un octet de code) ; P2 rcx/"
               "rdx/r8/r9 et la pile a [rsp+0x28]+ portent les arguments du "
               "syscall DANS L ORDRE de l API NT (l appelant a fait le travail "
               "msx64, ombre 0x20 comprise) ; P3 la pile est alignee 16 a "
               "l entree",
               "Q1 le syscall execute UNE fois au site unique ; Q2 rax = le "
               "NTSTATUS rendu par le noyau TEL QUEL ; Q3 rcx et r11 DETRUITS "
               "(le coup du noyau) ; Q4 la pile est inchangee a l entree pres",
               "I1 AUCUN IAT, aucun appel — le site syscall est l unique "
               "interaction ; I2 rax n est JAMAIS ecrit avant le site ; I3 "
               "AUCUN prologue (la pile de l appelant EST la pile du syscall — "
               "le noyau lit [rsp+0x28] AU MOMENT de l instruction) ; I4 aucun "
               "non-volatil touche ; I5 aucun etat, aucune ecriture memoire ; "
               "I6 le ret suit IMMEDIATEMENT le site ; I7 le padding du slot "
               "est NOP (convention de la lignee)",
               "[] (feuille pure — le trombone ABI, six octets)"),
    "g90002": ("(rcx span du nom ASCII, rdx longueur, r8 base ntdll) -> rax "
               "le SSN ou verdict negatif nomme ; rdx l adresse du stub au "
               "succes",
               "P1 rcx = le pointeur du span du nom EXACT (jamais une "
               "terminaison NUL supposee) ; P2 rdx = la longueur (> 0, le "
               "verdict -5 sinon) ; P3 r8 = la base du module ntdll (lue par "
               "le bloc, verifiee au motif PE — verdict -2 sinon)",
               "Q1 succes : rax = LE SSN (l imm32 du mov eax du stub, "
               "zero-etendu — positif en 64 bits) ; Q2 a la reussite rdx = "
               "l adresse du stub (la piece de la lecture) ; Q3 echecs nommes "
               "-1..-5 (la table des SEPT verdicts au plan d adressage)",
               "I1 la marche des noms BORNEE par NumberOfNames lu UNE fois ; "
               "I2 la comparaison est memcmp libc-02 (b20002, l heritage "
               "scelle M1 — le SEUL appel direct declare) ; I3 le MOTIF_STUB "
               "verifie AVANT la lecture de l imm32 ; I4 le bloc n emet "
               "JAMAIS syscall (lire n est pas emettre) ; I5 aucun IAT ; I6 "
               "aucun etat detenu ; I7 non-volatils intacts ; I8 AUCUNE "
               "ecriture dans le module lu",
               "[b20002 libc-02 memcmp @0x1180 — le seul appel direct] "
               "[memoire : ntdll LUE par pointeurs fournis, jamais appelee]"),
    "g90003": ("(rcx base ntdll, rdx handle d ecriture) -> rax 0 la ligne "
               "EMISE / -1 resolution echouee (rdx la CAUSE) / -6 STATUS non "
               "nul consigne en rdx",
               "P1 rcx = la base du module ntdll (fournie par l appelant — "
               "aucun IAT, pas meme GetModuleHandleA) ; P2 rdx = le handle "
               "d ecriture (le meme que hello-02 recevrait) ; P3 les fixtures "
               "du domaine vivent en .rdata : le span-nom « NtWriteFile » "
               "(11 o) et la LIGNE de hello-02 (33 o utiles + NUL, byte-exact "
               "le fixture M0)",
               "Q1 succes : rax = 0, la ligne EMISE octet pour octet le "
               "fixture de hello-02 ; Q2 le SSN resolu AU GESTE MEME (sys-02 "
               "appele depuis le bloc — jamais un numero en cache) ; Q3 les "
               "NEUF arguments de NtWriteFile dans l ordre NT (Event/Apc/"
               "Context NULL, l IO_STATUS_BLOCK sur la pile du bloc, le "
               "tampon le fixture, 33, ByteOffset NULL, Key 0 — les cinq "
               "derniers a [rsp+0x28]+ au moment du syscall) ; Q4 echecs "
               "nommes : -1 (rdx la cause, AUCUN syscall emis) et -6 (rdx le "
               "NTSTATUS brut — nomme, jamais muet ; la divergence iosb est "
               "-6)",
               "I1 AUCUN IAT (la preuve STRUCTURELLE du domaine) ; I2 l iosb "
               "vit sur la pile du bloc (zone morte au retour) ; I3 les "
               "seuls appels : sys-02 PUIS sys-01 — l ordre est le contrat ; "
               "I4 le fixture-ligne CITÉ par deplacement (jamais une seconde "
               "copie) ; I5 echec de resolution = AUCUN syscall emis ; I6 "
               "non-volatils intacts ; I7 le NTSTATUS jamais muet ; I8 le "
               "padding du slot est NOP",
               "[g90002 sys-02 @0xa040 — resoudre] [g90001 sys-01 @0xa000 — "
               "emettre] [rdata:span-nom,fixture-ligne]"),
}

TOUS_BLOCS = B5.TOUS_BLOCS + [b[0] for b in BLOCS_M8]          # 55 (génération 8)
RVA_PAR_BLOC = dict(B5.RVA_PAR_BLOC) | {b[0]: b[3] for b in BLOCS_M8}
SPEC_PAR_BLOC = dict(B5.SPEC_PAR_BLOC) | {b[0]: b[1] for b in BLOCS_M8}
EXE_PAR_BLOC = dict(B5.EXE_PAR_BLOC) | {b[0]: "proxy" for b in BLOCS_M8}
CONTRATS = dict(B5.CONTRATS) | CONTRATS_M8
ROLES = dict(L.NOMS_BLOCS)
EMBARQUES = {b[0] for b in BLOCS_EMBARQUES_M8}                 # 44 blocs
FICH_PAR_BID = dict(B5.FICH_PAR_BID) | {b[0]: b[2] for b in BLOCS_M8}


def _chemin_notation_bid(bid: str) -> str:
    """Notation d'un bloc indexé par la carte : routage M8 par défaut,
    héritage via le routeur M5 (jamais deux sources de vérité du routage)."""
    if bid in {b[0] for b in BLOCS_M8}:
        return chemin_notation_m8(FICH_PAR_BID[bid])
    return B5._chemin_notation_bid(bid)


_ZONES_CARTE = ("[zones] io=0x1000-0x10ff libc=0x1100-0x143f app=0x1800-0x1fff "
                "net=0x4000-0x42ff cli=0x4400-0x45bf thr=0x4300-0x43ff "
                "srv=0x4b00-0x4bff http=0x4c00-0x5e7f "
                "tls=0x6000-0x733f revisions=0x7340-0x7fbf reserve-t3=0x7fc0-0x7fff "
                "revisions-m5=0x8000-0x8fbf reserve-t4=0x8fc0-0x9fff "
                "sys=0xa000-0xa23f reserve-t5=0xa240-0xbfff "
                "reserve-libc=0x1440-0x17ff (int3 defensif)")


def fragments_clairs(exe: bytes, verrous_m3: list, verrous_m4: list,
                     verrous_m5: list, verrous_m8: list, version: str,
                     verdict_m4: dict, verdict_m5: dict, verdict_m8: dict,
                     compteurs: dict, journal_runs: list[str]) -> dict[str, bytes]:
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()

    loc = ["[carte-frag] nom=frag-loc generation=8", _ZONES_CARTE]
    for bid in TOUS_BLOCS:
        loc.append(f"[bloc] id={bid} spec={SPEC_PAR_BLOC[bid]} cible=x86-64-win11-pe "
                   f"exe={EXE_PAR_BLOC[bid]} addr={B5.L.IMAGE_BASE + RVA_PAR_BLOC[bid]:#x} "
                   f"v=1 etat=scelle role={ROLES[bid]}")

    con = ["[carte-frag] nom=frag-con generation=8"]
    for bid in TOUS_BLOCS:
        sig, pre, post, inv, deps = CONTRATS[bid]
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]

    prf = ["[carte-frag] nom=frag-prf generation=8"]
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

    bld = ["[carte-frag] nom=frag-bld generation=8"]
    for bid in TOUS_BLOCS:
        rva = RVA_PAR_BLOC[bid]
        if bid in EMBARQUES:
            slot = next(s for b, _sid, _f, _r, s in BLOCS_EMBARQUES_M8 if b == bid)
            empreinte = sha(tranche_section(exe, rva, slot))
        else:
            with open(_chemin_notation_bid(bid), "rb") as f:
                empreinte = "notation:" + sha(f.read())[7:]
        bld.append(f"[bloc] id={bid} addr={B5.L.IMAGE_BASE + rva:#x} empreinte={empreinte}")
    bld += [
        f"[build] artefact=proxy.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous structurels : M3 {len(verrous_m3)} + M4 {len(verrous_m4)} + M5 {len(verrous_m5)} "
        f"+ M8 {len(verrous_m8)} ; oracles : M4 (heritage rejoue) {verdict_m4.get('total_cas', 0)} cas "
        f"+ M5 (scenarios etendus D136) {verdict_m5.get('total_cas', 0)} cas + M8 (domaine sys, "
        f"fixtures ntdll synthetiques D161) {verdict_m8.get('total_cas', 0)} cas, "
        f"graine={verdict_m8.get('graine', '-')}, volume={verdict_m8.get('volume', '-')}",
        f"  heritage : proxy.exe 0.6.0 scelle (c1e46fb0...) repris octet pour octet "
        f"(R7 : .text/.text2/.text3/.text4/.data intacts, .rdata identique SAUF la "
        f"version @0x2820 = 0x00090001 [LE delta R10 — geste de BUILD, jamais "
        f"scellage : la 0.9.0 finale attend le terrain vert du chantier (d)] et "
        f"l extension du domaine 0x2EC0-0x2EFF dans la zone VIERGE VERIFIEE "
        f"[span-nom NtWriteFile, ligne de hello-02 byte-exact le fixture M0] ; "
        f"section .text5 NOUVELLE [0xA000-0xBFFF : sys-01 @0xA000/0x40, sys-02 "
        f"@0xA040/0x140, sys-03 @0xA180/0xC0 — l arret D161 sur les longueurs "
        f"reelles, la reserve int3 0xA240+] ; PE : 7 sections, SizeOfImage "
        f"0xC000, taille 0xAE00, en-tetes <= 0x400 AUCUN decalage (le modele "
        f"D94 n est pas rejoue) ; entree PE 0x8C80 INCHANGEE (le principal "
        f"n est pas recable — le domaine est la piece rapportee, cablee au "
        f"chantier (d)) ; les 44 blocs heritages octet-identiques ; "
        f"hello.exe 0.1.0 + selftest.exe 0.2.0 + echo.exe 0.3.0 + proxy.exe "
        f"0.4.0 + proxy.exe 0.5.1 + proxy.exe 0.6.0 (lignees D74/D80/D144) "
        f"inchanges",
        _ZONES_CARTE,
    ]

    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("utf-8", errors="replace")
    return retour


def construire_carte(exe, verrous_m3, verrous_m4, verrous_m5, verrous_m8,
                     version, verdict_m4, verdict_m5, verdict_m8, compteurs,
                     journal_runs):
    phrase, _ = cm8.charger_secrets(interactif=False)
    maitre = cm8.cle_maitresse(phrase)
    clairs = fragments_clairs(exe, verrous_m3, verrous_m4, verrous_m5,
                              verrous_m8, version, verdict_m4, verdict_m5,
                              verdict_m8, compteurs, journal_runs)
    fragments = {n: cm8.chiffrer_fragment(maitre, n, clairs[n]) for n in cm8.FRAGMENTS}
    racine = cm8.empreinte_racine(fragments)
    entete = cm8.construire_entete(racine)
    prive, pub = cm8.paire_cles(cm8.charger_secrets(interactif=False)[1])
    signature = cm8.signer(prive, entete, fragments)
    cm8.ecrire_carte(entete, fragments, signature, pub)
    return pub


# --- Verrou croisé (R8 : relecture indépendante) ----------------------------------

def verrou_croise() -> tuple[int, dict]:
    phrase, _ = cm8.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm8.lire_carte()
    cm8.verifier_listes_blanches(entete.decode("ascii"))
    cm8.verifier_signature(pub, entete, fragments, signature)
    if cm8.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm8.ErreurCarte("empreinte racine divergente")
    maitre = cm8.cle_maitresse(phrase)
    bld = cm8.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
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
    for bid, _sid, _f, rva, slot in BLOCS_EMBARQUES_M8:
        sha = "sha256:" + hashlib.sha256(tranche_section(exe, rva, slot)).hexdigest()
        if sha != empreintes.get(bid):
            raise cm8.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm8.ErreurCarte("verrou croisé : empreinte de proxy.exe divergente (R8)")
    return len(empreintes), manifeste


# --- Tableau de bord (§ 15.2, métriques M8) -----------------------------------------

def tableau_de_bord(exe: bytes, verrous_m3: list, verrous_m4: list,
                    verrous_m5: list, verrous_m8: list, nb_blocs_carte: int,
                    manifeste: dict, verdict_m4: dict, verdict_m5: dict,
                    verdict_m8: dict) -> str:
    sha = lambda b: hashlib.sha256(b).hexdigest()
    lignes = [
        "[tableau] jalon=M8 artefact=proxy.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb_blocs_carte}/55 : audit de tracabilite I->C->B (7 artefacts)",
        f"  chaines_I_C_B_tests           : {nb_blocs_carte}/{nb_blocs_carte} : specs, carte, exe, vecteurs",
        f"  construction                  : 0 erreur / 0 avertissement : build script",
        f"  tests_differentiels           : oracle M4 (heritage rejoue) {verdict_m4.get('total_cas', 0)} cas verts "
        f"+ oracle M5 (scenarios etendus D136) {verdict_m5.get('total_cas', 0)} cas verts "
        f"+ harnais M8 (domaine sys, fixtures ntdll synthetiques D161) {verdict_m8.get('total_cas', 0)} "
        f"cas verts ({verdict_m8.get('volume', '-')}, graine {verdict_m8.get('graine', '-')}) ; "
        f"oracle structurel M3 {len(verrous_m3)} + M4 {len(verrous_m4)} + M5 {len(verrous_m5)} "
        f"+ M8 {len(verrous_m8)} verrous PASS (LA REGLE AUCUN IAT PAR BLOC sys)",
        f"  reutilisation_heritage        : 44 blocs octet-identiques au scelle 0.6.0 "
        f"(R7, deltas .rdata/.text5/PE documentes — version 0x00090001 : geste de BUILD)",
        f"  empreintes_donnees_embarquees : conforme (fixtures http + tls + CLI/flux M5 "
        f"+ span-nom/fixture-ligne M8 dans la zone VIERGE 0x2EC0-0x2EFF, table R10 "
        f"28 entrees archee, porte M5, version {L.VERSION_U64_DEV1:#x})",
        f"  defauts_T1_T6_ouverts         : 0 : journal des decisions D77-D161",
        f"  optimisations_sans_mesure     : 0 : aucune optimisation M8 (R11)",
        f"  changements_hors_journal      : 0 : D77 a D161 consignees",
        f"  preversions                   : {manifeste.get('version', '?')} conforme "
        f"(schema dev, monotonie R10 : 0x00090001 > 0x00060001 — la finale 0.9.0 "
        f"attend le terrain vert du chantier (d), jamais un scellage ici)",
        f"  entrees_non_fiables           : comportement defini par contrat (les SEPT "
        f"verdicts nommes du domaine, le NTSTATUS jamais muet, I5 echec de "
        f"resolution = AUCUN syscall) ; falsification : V4 15/15 mutations "
        f"attrapees (D161)",
        f"  artefact                      : {len(exe)} octets ; empreinte sha256:{sha(exe)[:16]}... ; "
        f"7 sections (.text5 nouvelle 0xA000 — le domaine sys) ; AUCUN import "
        f"nouveau (la preuve structurelle : le domaine ne declare RIEN) ; "
        f"entree PE 0x8C80 inchangee",
        f"  verrou_croise                 : {nb_blocs_carte} empreintes reverifiees "
        f"(7 artefacts + notations non embarquees) + signature Ed25519 (graine "
        f"durable D144, pub e9cd8c549485... — le temoin ne bouge pas) + racine (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Anti-rollback (R6) --------------------------------------------------------------

def _anti_rollback() -> None:
    """Une carte scellée (rc/finale) interdit la reconstruction (R6). La
    0.9.0-dev.1 n'est PAS scellée (schéma dev — la finale 0.9.0 attend le
    terrain vert du chantier (d)) : la reconstruction de dev est licite
    (cristallisation R6 au fil des vérifications)."""
    try:
        _, fragments, _, _ = cm8.lire_carte()
        phrase, _ = cm8.charger_secrets(interactif=False)
        maitre = cm8.cle_maitresse(phrase)
        bld = cm8.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
        version_existante = next(
            (dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
             if "artefact=proxy.exe" in l), None)
        if version_existante and ("-rc" in version_existante
                                  or re.fullmatch(r"\d+\.\d+\.\d+", version_existante)):
            raise EchecBuild(
                f"carte scellée ({version_existante}) : reconstruction interdite — "
                f"procedure lourde R6 ou nouvelle version X.Y.Z+1 requise")
    except (cm8.ErreurCarte, FileNotFoundError):
        pass  # pas de carte lisible : première construction


def verifier_carte_possible() -> str:
    """-> le motif : 'cérémonie requise' (secrets absents) ou 'prête'."""
    chemin_phrase = os.path.join(TRIADE, ".keys", "passphrase.txt")
    chemin_graine = os.path.join(TRIADE, ".keys", "ed25519.seed")
    if not os.path.exists(chemin_phrase) or not os.path.exists(chemin_graine):
        return ("cérémonie requise (D144) : relève au coffre — phrase = entrée "
                "lignee-D80, graine = entrée graine-ed25519-cartes")
    return "prête (lignée D80 + graine durable D144)"


# --- Modes -----------------------------------------------------------------------------

def construire(volume: str, graine: int) -> int:
    print("=== M8 : chaîne artefact TRIADE (profil x86-64-win11-pe, 0.9.0-dev.1) ===")
    _anti_rollback()
    _garde_sceau_I()

    # 1. L'héritage M3+M4+M5 re-vérifié de bout en bout, la preuve R7
    h = heritage_complet()

    # 2. Les blocs M8 : assemblage et oracle structurel (LA RÈGLE du domaine)
    specs_m8, code_m8, verrous_m8 = assembler_tout_m8()

    # 3. Composition de l'image M8 (deltas documentés + .text5)
    sections = composer_image_m8(h["sections_m5"], code_m8)
    exe = ecrire_pe32plus(*sections)
    valider_pe(exe)
    print(f"[PE] proxy.exe : {len(exe)} octets, 7 sections (.text5 0xA000 — le "
          f"domaine sys : sys-01/sys-02/sys-03, la réserve int3), AUCUN import "
          f"nouveau, entrée {B5.L.ENTREE_M5:#x} inchangée (R7)")

    # 4. Preuve R7 (l'héritage 0.6.0)
    heritage = preuve_reutilisation(exe)
    print(f"[R7] réutilisation : {heritage['blocs_reutilises']} blocs "
          f"octet-identiques au scellé 0.6.0, deltas .rdata/.text5/PE "
          f"documentés (version 0x00090001 : geste de BUILD, jamais scellage)")

    # 5. Les oracles : l'héritage M4 puis M5 PUIS le domaine (les blobs du build)
    blobs_m4 = B4.blobs_oracle(h["code_m3"], h["code_m4"])
    verdict_m4 = B4.od4.executer(blobs_m4, graine=graine, volume=volume)
    print(f"[oracle] différentiel M4 (héritage) : {verdict_m4['total_cas']} cas verts")
    blobs_m5 = B5.blobs_oracle(h["code_m3"], h["code_m4"], h["code_m5"])
    verdict_m5 = B5.od5.executer(blobs_m5, graine=graine, volume=volume)
    print(f"[oracle] différentiel M5 (héritage) : {verdict_m5['total_cas']} cas verts")
    verdict_m8 = harnais.executer(blobs_sys(code_m8), graine=graine, volume=volume)
    print(f"[oracle] harnais M8 (le domaine sys) : {verdict_m8['total_cas']} cas verts")

    # 6. Écriture de l'artefact
    with open(os.path.join(ICI, "proxy.exe"), "wb") as f:
        f.write(exe)

    # 7. Carte génération 8 (lignée D80, graine durable D144) + verrou croisé
    #    + tableau de bord — le scellage est un fait de carte (D104) et il
    #    N'AURA PAS LIEU ici (la 0.9.0 attend le terrain vert du chantier (d))
    version = L.VERSION_DEV1
    compteurs = {bid: 1 for bid in TOUS_BLOCS}
    journal = [f"run graine={graine} volume={volume} "
               f"verdict-m4={verdict_m4['empreinte']} verdict-m5={verdict_m5['empreinte']} "
               f"verdict-m8={verdict_m8['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"build={version}"]
    construire_carte(exe, h["verrous_m3"], h["verrous_m4"], h["verrous_m5"],
                     verrous_m8, version, verdict_m4, verdict_m5, verdict_m8,
                     compteurs, journal)
    print(f"[carte] génération 8 écrite (lignée D80, graine durable D144) : "
          f"4 fragments chiffrés, signature Ed25519, {len(TOUS_BLOCS)} blocs "
          f"indexés sur 7 artefacts")
    nb, manifeste = verrou_croise()
    print(f"[R8] verrou croisé : signature OK, racine OK, {nb} empreintes "
          f"revérifiées, artefact {manifeste.get('version')}")
    with open(os.path.join(cm8.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, h["verrous_m3"], h["verrous_m4"],
                                h["verrous_m5"], verrous_m8, nb, manifeste,
                                verdict_m4, verdict_m5, verdict_m8))
    print("[tableau] tableau de bord écrit (carte/tableau-de-bord.txt)")
    print(f"[B] proxy.exe {manifeste.get('version')} : "
          f"sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== M8-dev (oracle vert) : {version} — le domaine sys composé sur le "
          f"corps 0.6.0 INTACT, carte génération 8 vivante ; le chantier (d) "
          f"(le kit terrain, le VRAI ntdll) attend ; la finale 0.9.0 attend le "
          f"terrain vert ===")
    return 0


def verifier(graine: int, volume: str) -> int:
    print(f"=== M8 : re-vérification complète (R5/R7, graine {graine}) ===")
    _garde_sceau_I()
    h = heritage_complet()
    specs_m8, code_m8, verrous_m8 = assembler_tout_m8()
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    heritage = preuve_reutilisation(exe)
    print(f"[R7] {heritage['blocs_reutilises']} blocs réutilisés du scellé "
          f"0.6.0, deltas documentés")
    valider_pe(exe)
    blobs_m4 = B4.blobs_oracle(h["code_m3"], h["code_m4"])
    verdict_m4 = B4.od4.executer(blobs_m4, graine=graine, volume=volume)
    print(f"[oracle] différentiel M4 (héritage) : {verdict_m4['total_cas']} cas verts")
    blobs_m5 = B5.blobs_oracle(h["code_m3"], h["code_m4"], h["code_m5"])
    verdict_m5 = B5.od5.executer(blobs_m5, graine=graine, volume=volume)
    print(f"[oracle] différentiel M5 (héritage) : {verdict_m5['total_cas']} cas verts")
    verdict_m8 = harnais.executer(blobs_sys(code_m8), graine=graine, volume=volume)
    print(f"[oracle] harnais M8 (le domaine sys) : {verdict_m8['total_cas']} cas verts")
    print(f"[PE] proxy.exe 0.9.0-dev.1 re-validé (7 sections, portes R10+M5, "
          f"fixtures du domaine, version {L.VERSION_U64_DEV1:#x})")

    # Cristallisation R6 : chaque passage incrémente les compteurs — la carte
    # est re-signée à chaque passage (fragments re-chiffrés, graine durable
    # D144), le verrou croisé re-vérifié (R8). La 10/10 sera exigée au
    # scellage de la 0.9.0 (qui attend le terrain vert du chantier (d)).
    phrase, _ = cm8.charger_secrets(interactif=False)
    maitre = cm8.cle_maitresse(phrase)
    _, fragments, _, _ = cm8.lire_carte()
    prf = cm8.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("utf-8")
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
    journal.append(f"run graine={graine} volume={volume} "
                   f"verdict-m4={verdict_m4['empreinte']} verdict-m5={verdict_m5['empreinte']} "
                   f"verdict-m8={verdict_m8['empreinte']} "
                   f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")

    bld = cm8.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    manifeste_v = next((dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
                        if "artefact=proxy.exe" in l), "?")
    version = manifeste_v if manifeste_v != "?" else L.VERSION_DEV1
    construire_carte(exe, h["verrous_m3"], h["verrous_m4"], h["verrous_m5"],
                     verrous_m8, version, verdict_m4, verdict_m5, verdict_m8,
                     compteurs, journal)
    nb, manifeste = verrou_croise()
    crist = {b: compteurs.get(b, 0) for b, *_ in BLOCS_M8}
    print("[R6] cristallisation M8 : " + ", ".join(f"{b}={n}/10" for b, n in crist.items()))
    print(f"[R8] verrou croisé : {nb} empreintes conformes ; artefact {manifeste.get('version')}")
    with open(os.path.join(cm8.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, h["verrous_m3"], h["verrous_m4"],
                                h["verrous_m5"], verrous_m8, nb, manifeste,
                                verdict_m4, verdict_m5, verdict_m8))
    print(f"[carte] génération 8 : {verifier_carte_possible()}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    graine = 20261105
    volume = "complet"
    if "--graine" in args:
        graine = int(args[args.index("--graine") + 1])
    if "--volume" in args:
        volume = args[args.index("--volume") + 1]
    if "--verifier" in args:
        return verifier(graine, volume)
    return construire(volume, graine)


if __name__ == "__main__":
    sys.exit(main())
