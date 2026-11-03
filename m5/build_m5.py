#!/usr/bin/env python3
"""build_m5.py : Jalon M5 de TRIADE — LE FLUX NAVIGATEUR (proxy 0.6.0 — D136).

Chaîne : notation (keystone) -> octets -> PE32+ à la main (SIX sections :
.text/.rdata/.data/.text2/.text3 + .text4 NOUVELLE) -> carte projet génération 7.
Implémente le jalon 0.6.0 sous les règles R4/R7 (adresses stables — l'héritage
M0/M1/M2/M3/M4 repris OCTET POUR OCTET du proxy.exe 0.5.1 scellé, sha256
fb41697d…, le binaire PROUVÉ par les runs v7 et v8) et R10 (porte au
lancement — la marche héritée 28 entrées PLUS la PORTE M5).

LA COMPOSITION 0.6.0 (D136, m5/I/README.md) :
  - http-08:R3  (g80001 @0x8000)  le verdict « cible à relever » (5) — SOUS
    politique armée SEULEMENT ; sans politique : R2 OCTET POUR OCTET ;
  - http-10:R3  (g80002 @0x81C0)  le routage du verdict 5 par LE MÊME chemin
    Q2' (port 443) + LA LIGNE DE FLUX (tcp-11, zéro secret) ;
  - http-12:R3  (g80003 @0x8C40)  LA CLI naît (--relever-https ; TOUT
    argument inconnu = REFUS NOMMÉ, ExitProcess 3) + LA PORTE M5 (UNE entrée,
    fail-closed, miroir D95) + le câblage de la boucle sur 0x81C0.
  RENUMÉROTATION (verdict v8) : l'intention de D136 disait « http-12:R2 » ;
  le nom est PRIS par le câblage D95 — la révision CLI est http-12:R3.

Deltas PE documentés (R7 — tout le reste est l'héritage scellé 0.5.1) :
  .text4 : NOUVELLE (0x8000-0x9FFF) : les trois révisions R3
  .rdata : 0x2CE0+ = extension M5 (fixtures CLI/flux, descripteurs M5,
           IAT/INT/hints GetCommandLineW, PORTE M5)
  .data  : R_POLITIQUE @0x3860 — l'état image reste 0 (écrit par http-12:R3)
  PE     : AddressOfEntryPoint 0x7DC0 -> 0x8C40 ; SizeOfImage 0x8000 -> 0xA000 ;
           répertoire d'imports 0x29A0 (80 o) -> 0x2DA0 (100 o — kernel32 est
           décrit DEUX FOIS : les 10 slots scellés + GetCommandLineW) ;
           table de sections 5 -> 6 ; taille de fichier 0x6E00 -> 0x8E00.

L'ORACLE (D136) est exécuté sur les blobs du build : oracle_m5.executer(blobs,
graine, volume) — les scénarios étendus (cible relevée saine / certificat
invalide relevé / politique absente ZÉRO écart / ligne de flux OCTET PAR
OCTET / ports explicites / hôte tronqué / porte M5 fuzzée / CLI fuzzée /
falsification), lève EchecOracle sur TOUT écart. L'héritage M4 est re-vérifié
AU PASSAGE : build_m4.assembler_tout_m4() (round-trip + oracle structurel M4)
et l'image composée M4 est confrontée OCTET PAR OCTET au proxy.exe 0.5.1
scellé AVANT toute extension — la preuve R7 absolue.

Usage :
  python3 build_m5.py                  # construction 0.6.0-dev.1
  python3 build_m5.py --verifier [--graine N] [--volume complet|reduit]
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
M3_DIR = os.path.join(TRIADE, "m3")
M4_DIR = os.path.join(TRIADE, "m4")
# Le builder M4 charge ses modules par imports PLAINS (carte_m4, oracle_m4,
# les outils) : ses répertoires doivent être sur le chemin AVANT son
# chargement (le builder M3 insère lui-même les siens — miroir des harnais).
for _d in (M4_DIR, os.path.join(M4_DIR, "outils"), ICI,
           os.path.join(ICI, "outils")):
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


# Le plan M4 se charge sous un nom distinct (le fichier s'appelle layout.py
# comme le plan M5) ; le builder M4 charge build_m3 à son tour — la chaîne
# d'héritage complète est re-vérifiée à chaque build M5 (R5/R7).
L4 = _charger_module("layout_m4", os.path.join(M4_DIR, "layout.py"))
B4 = _charger_module("build_m4", os.path.join(M4_DIR, "build_m4.py"))
# build_m4 laisse sys.modules["layout"] = le plan M4 : les DEUX oracles et
# leurs harnais (harnais_session, _r2, _r3, cible_r3) s'y lient ICI — tous
# leurs « import layout » voient le plan M4, leurs plans M5 sont chargés
# sous nom propre par importlib (liaison par objet module, miroir build_m4).
import oracle_m4 as od4  # noqa: E402
import oracle_m5 as od5  # noqa: E402
L = _charger_module("layout", os.path.join(ICI, "layout.py"))   # plan M5

import capstone  # noqa: E402
import pefile  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

# --- Garde sceau de l'Intention (D87/D105) -----------------------------------
# Les arbres d'intention qui NOURRISSENT la chaîne : l'héritage M0-M4 est
# signé (cérémonies réelles v7, D87) ; l'arbre m5 porte les révisions R3
# écrites-avant-code (D136) — signé par la cérémonie 0.6.0 du 04/11
# (remise 11 lignes, sceau_I.py deposer → verifier 11 verts code 0).
SCEAU_I = B4.SCEAU_I
ARBRES_GARDE_M5 = ["m0", "m1", "m2", "m3", "m4", "m5"]


def _garde_sceau_I() -> None:
    try:
        SCEAU_I.garde(ARBRES_GARDE_M5)
        print(f"[sceau-I] garde : {len(ARBRES_GARDE_M5)} arbres d'intention "
              f"conformes à leurs signatures ({', '.join(ARBRES_GARDE_M5)}) ; "
              f"clé déposée : {SCEAU_I.etat_cle()}")
    except SCEAU_I.EchecSceauI as exc:
        raise EchecBuild(str(exc)) from exc


# --- Blocs M5 embarqués dans .text4 (couche C, génération 7 — g8xxxx) -----------

BLOCS_M5 = [(bid, spec, fichier, rva, slot)
            for bid, _s, rva, slot, _v, _e in L.BLOCS_REVISIONS_M5
            for fichier, spec in ((nom, sid) for nom, sid in (
                ("http-08-cible-r3", "http-08:R3"),
                ("http-10-session-r3", "http-10:R3"),
                ("http-12-principal-r3", "http-12:R3"),
            ) if sid == _s)]
assert [(b[0], b[3], b[4]) for b in BLOCS_M5] == \
    [(b[0], b[2], b[3]) for b in L.BLOCS_REVISIONS_M5], \
    "BLOCS_M5 diverge du plan d'adressage (layout.py, source unique)"

# L'héritage M4 complet (io, libc, tcp, http R1/R2, tls, http-12:R2, libc-07)
# est repris OCTET POUR OCTET (R7) — le build_m5 le lit via B4.
BLOCS_EMBARQUES_M5 = B4.BLOCS_EMBARQUES_M4 + BLOCS_M5

# Clés de blobs pour l'oracle (table M4 + LES TROIS révisions M5).
_CLE_BLOB = dict(B4._CLE_BLOB)
_CLE_BLOB |= {"g80001": "http-08-R3", "g80002": "http-10-R3",
              "g80003": "http-12-R3"}


def chemin_notation_m5(fichier: str) -> str:
    return os.path.join(ICI, "notation", fichier + ".asm")


# --- Couche I M5 : lecture et audit du gabarit ----------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)),
            "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures",
                 "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2 : écrite-avant-code)")
    return spec


_FICHIERS_I_M5 = {
    "g80001": "http-08-cible-r3.md",
    "g80002": "http-10-session-r3.md",
    "g80003": "http-12-principal-r3.md",
}


def charger_couche_I_m5() -> dict[str, dict]:
    specs = {}
    for bid, sid, _f, _r, _s in BLOCS_M5:
        ident, rev_ref = sid.split(":")
        chemin = os.path.join(ICI, "I", _FICHIERS_I_M5[bid])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec(chemin)
        if spec["id"] != ident:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {ident}")
        if spec["rev"] != int(rev_ref[1:]):
            raise EchecBuild(f"{chemin} : révision {spec['rev']} != R{rev_ref[1:]}")
        specs[bid] = spec
    return specs


# --- Notation : assemblage, tailles déclarées, round-trip (R5) ------------------
# Les primitives sont CELLES du builder M4 (une seule implémentation —
# lignes_notation/assembler_bloc/round_trip/canon/deplacements_declares).

lignes_notation = B4.lignes_notation
taille_declaree = B4.taille_declaree
assembler_bloc = B4.assembler_bloc
round_trip = B4.round_trip
canon = B4.canon
operande_rip_cible = B4.operande_rip_cible
deplacements_declares = B4.deplacements_declares
EchecOracle = od4.EchecOracle


# --- Oracle structurel M5 : les invariants de I, par bloc ------------------------

IAT_M5 = {
    "g80001": set(),             # feuille pure (I1 de http-08:R3)
    "g80002": {"CloseHandle"},   # I7 : EXACTEMENT {CloseHandle} — hérité
    "g80003": {"GetStdHandle", "InitializeCriticalSection", "ExitProcess",
               "CloseHandle", "WSACleanup", "GetCommandLineW"},  # I1 : LA seule entrée nouvelle
}
APPELS_DIRECTS_M5 = {
    # http-08:R3 : feuille pure — assistants internes seulement
    "g80001": set(),
    # http-10:R3 : l'héritage R2 + LES TROIS libc (la ligne de flux) —
    # JAMAIS tls-01..07 direct (tout passe par tls-08 @0x6D40)
    "g80002": {0x6D40, 0x8000, 0x4C00, 0x4C80, 0x4F40, 0x5080, 0x5140,
               0x5200, 0x54C0, 0x4140, 0x4180, 0x41C0, 0x4300, 0x4B00,
               0x4400, 0x1100, 0x1200, 0x1280},
    # http-12:R3 : hello-02, tcp-01/02/06/11 — l'héritage R1 (I1)
    "g80003": {0x1040, 0x4000, 0x4100, 0x4300, 0x4B00},
}
DONNEES_RIP_M5 = {
    "g80001": {L4.R_SLASH},
    "g80002": {L4.R_TXT_400, L4.R_TXT_431, L4.R_TXT_501, L4.R_TXT_411,
               L4.R_TXT_505, L4.R_TXT_502, L4.R_TXT_TUNNEL, L4.R_TXT_502_CERT,
               L4.R_MSG_CONNEXION, L4.R_MSG_TUNNEL, L4.R_MSG_FIN,
               L4.R_NOM_HOST, L4.R_NOM_CL, L4.R_NOM_TE,
               L4.R_TAB_METHODES,   # I9 : la méthode du préfixe PAR TABLE (.rdata STABLE)
               L.R_POLITIQUE},
    # http-12:R3 : l'héritage R2 + LES structures M5 (porte, CLI, politique) +
    # les DEUX cibles de code par lea (0x5D80 la console, 0x81C0 LA SESSION
    # http-10:R3 — JAMAIS 0x74C0/0x5580 : le contre-câblage nominal)
    "g80003": {L4.R_TAB_SUM, L4.R_VERSION, L4.R_ANCRE, L4.R_STDOUT,
               L4.R_STDIN, L4.R_LISTEN, L4.R_QUIT, L4.R_CS,
               L4.R_MSG_BANNIERE, L4.R_MSG_ARRET, L4.R_MSG_ERREUR,
               L4.R_MSG_KO, 0x5D80, 0x81C0,
               L.R_TAB_SUM_M5, L.R_BORNE_M5, L.R_TXT_CMD_KO,
               L.R_TXT_POLITIQUE, L.R_CMD_RELEVER, L.R_POLITIQUE,
               L.R_IAT_M5},
}
FEUILLES_M5 = {"g80001"}

_SLOTS_IAT_COMPLETS = {**L.IAT_SLOTS, **L.IAT_SEC32_SLOTS, **L.IAT_M5_SLOTS}


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


def oracle_structurel_m5(specs: dict, code: dict, blocs: list[tuple]) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    for bid, sid, fichier, rva, slot in blocs:
        insns = code[bid]["insns"]
        mnemos = [i.mnemonic for i in insns]
        adresses_insns = {i.address for i in insns}
        internes_autorises = APPELS_DIRECTS_M5.get(bid, set()) | (
            {a for a in adresses_insns if a != rva} if bid in FEUILLES_M5 else set())

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
                    verrou(f"{bid}:iat-autorisee@{i.address:#x}",
                           classe[4:] in IAT_M5.get(bid, set()),
                           f"{classe} hors IAT déclarée (I1)")
                elif classe.startswith("bloc:"):
                    verrou(f"{bid}:appel-autorise@{i.address:#x}",
                           int(classe[5:], 16) in internes_autorises,
                           f"{classe} hors blocs déclarés (I1)")

        cibles_rip: set[int] = set()
        for i in insns:
            cible = operande_rip_cible(i)
            if cible is not None and i.mnemonic != "call":
                cibles_rip.add(cible)
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP_M5.get(bid, set())
                       or rva <= cible < rva + slot,
                       f"cible {cible:#x} hors données déclarées (I2/I5)")

        declarees = deplacements_declares(chemin_notation_m5(fichier))
        if declarees is not None:
            rip_reelles = {operande_rip_cible(i) for i in insns}
            rip_reelles.discard(None)
            verrou(f"{bid}:deplacements-rip-declares", rip_reelles == declarees,
                   f"réelles {sorted(hex(c) for c in rip_reelles - declarees)} "
                   f"non déclarées / déclarées {sorted(hex(c) for c in declarees - rip_reelles)} absentes")

        verrou(f"{bid}:pas-de-syscall",
               not any(m in ("syscall", "sysenter", "int") for m in mnemos))

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

    # Feuilles M5 : aucun appel externe
    for bid in FEUILLES_M5:
        rva_bid = next(r for b, _, _, r, _ in blocs if b == bid)
        for i in code[bid]["insns"]:
            if i.mnemonic == "call":
                verrou(f"{bid}:feuille-sans-appel-externe@{i.address:#x}",
                       _externe(bid, i, {x.address for x in code[bid]["insns"]},
                                rva_bid) == "interne",
                       "une feuille pure n'appelle rien d'extérieur (I1)")

    # g80001 (http-08:R3) — I7 : la politique est LUE UNE fois ([rsp+0x30]),
    # jamais écrite ; I6 : le verdict 5 naît À LA PLACE du succès générique
    m = code["g80001"]["insns"]
    lectures_loge = [i for i in m if "[rsp + 0x30]" in i.op_str]
    verrou("g80001:loge-5-lue-une-fois", len(lectures_loge) == 1,
           f"{len(lectures_loge)} lectures de [rsp+0x30] (I7)")
    verrou("g80001:loge-5-jamais-ecrite",
           not any("[rsp + 0x30]" in i.op_str and i.mnemonic.startswith("mov")
                   and i.op_str.split(",")[0].strip().endswith("]") for i in m),
           "la loge 5 est LUE, jamais écrite (I7)")
    verrou("g80001:verdict-5-present",
           any(i.mnemonic == "mov" and i.op_str == "eax, 5" for i in m),
           "le verdict 5 (cible à relever) manque")

    # g80002 (http-10:R3) — leçon D63 armée sur 0x13390 (V6bis) : le probing
    # touche [rsp-0x13390] AVANT le sub rsp (multiple de 16, ABI P5) ; P8 :
    # SEPT pushes ; I7 : EXACTEMENT UNE fonction IAT (CloseHandle) ; la
    # sentinelle de flux est posée au prologue (Q6)
    m = code["g80002"]["insns"]
    idx_sub = next((k for k, i in enumerate(m)
                    if i.mnemonic == "sub" and
                    i.op_str == f"rsp, {L.TAILLE_CADRE_SESSION:#x}"), None)
    verrou("g80002:prologue-sub-0x13390", idx_sub is not None,
           "sub rsp, 0x13390 introuvable")
    verrou("g80002:prologue-7-pushes",
           all(m[k].mnemonic == "push" for k in range(7)) and
           m[7].mnemonic != "push", "le prologue n'a pas SEPT pushes (P8)")
    if idx_sub is not None:
        verrou("g80002:probing-touche-cadre",
               any(f"[rsp - {L.TAILLE_CADRE_SESSION:#x}]" in i.op_str
                   for i in m[:idx_sub]),
               "la touche [rsp-0x13390] précède le sub (D63)")
        verrou("g80002:sentinelle-flux-prologue",
               any(i.mnemonic == "mov" and "[rsp + 0x7028]" in i.op_str
                   and (i.op_str.endswith("-1")
                        or i.op_str.endswith("0xffffffffffffffff"))
                   for i in m[:idx_sub + 4]),
               "la sentinelle -1 n'est pas posée au prologue (Q6)")
    iats_g80002 = {classe[4:] for i in m if i.mnemonic == "call"
                   and (classe := _externe("g80002", i,
                                           {x.address for x in m}, 0x81C0))
                   and classe.startswith("iat:")}
    verrou("g80002:iat-unique-closehandle", iats_g80002 == {"CloseHandle"},
           f"IAT vues : {iats_g80002}")
    appels_g80002 = {int(i.op_str, 16) for i in m
                     if i.mnemonic == "call" and i.op_str.startswith("0x")}
    interdits = {0x6000, 0x6080, 0x6180, 0x62C0, 0x65C0, 0x6740, 0x6A40}
    verrou("g80002:jamais-tls-feuilles-direct", not (appels_g80002 & interdits),
           f"appels directs TLS interdits : "
           f"{sorted(hex(a) for a in appels_g80002 & interdits)}")
    # P7 : la politique est lue UNE fois dans .data ([rip + POLITIQUE])
    lectures_pol = [i for i in m if i.mnemonic == "mov" and "rip" in i.op_str
                    and operande_rip_cible(i) == L.R_POLITIQUE]
    verrou("g80002:politique-lue-une-fois", len(lectures_pol) == 1,
           f"{len(lectures_pol)} lectures de R_POLITIQUE (P7 : UNE)")

    # g80003 (http-12:R3) — I1 : GetCommandLineW est LA seule entrée IAT
    # nouvelle ; le contre-câblage (lea 0x74C0/0x5580) est INTERDIT ; la
    # porte M5 est précédée de la marche héritée (I3) ; la CLI précède
    # TOUTE initialisation (I3 : aucun GSH avant la CLI)
    m = code["g80003"]["insns"]
    cibles_lea = {operande_rip_cible(i) for i in m
                  if i.mnemonic == "lea" and "rip" in i.op_str
                  and operande_rip_cible(i) is not None}
    verrou("g80003:cibles-code-0x81c0", 0x81C0 in cibles_lea,
           "la boucle ne câble pas http-10:R3 (Q4)")
    verrou("g80003:jamais-ancetres-session",
           0x74C0 not in cibles_lea and 0x5580 not in cibles_lea,
           "le contre-câblage (0x74C0/0x5580) est la falsification nominale (I1)")
    iat_gclw = [i for i in m if i.mnemonic == "call" and "rip" in i.op_str
                and operande_rip_cible(i) == L.R_IAT_M5]
    verrou("g80003:getcommandlinew-une-fois", len(iat_gclw) == 1,
           "GetCommandLineW appelée exactement une fois (Q2/I6)")
    idx_gclw = next((k for k, i in enumerate(m)
                     if i.mnemonic == "call" and "rip" in i.op_str
                     and operande_rip_cible(i) == L.R_IAT_M5), None)
    idx_gsh = next((k for k, i in enumerate(m)
                    if i.mnemonic == "call" and "rip" in i.op_str
                    and operande_rip_cible(i) == L4.IAT_SLOTS["GetStdHandle"]),
                   None)
    if idx_gclw is not None and idx_gsh is not None:
        verrou("g80003:cli-avant-initialisation", idx_gclw < idx_gsh,
               "la CLI précède TOUTE initialisation (I3/E4)")
    # Q2 : le refus nommé (ExitProcess 3) existe et précède l'écoute
    verrou("g80003:refus-nomme-3",
           any(i.mnemonic == "mov" and i.op_str == "ecx, 3" for i in m),
           "le refus CLI n'est pas nommé (E4 : ExitProcess 3)")

    # Traçabilité : chaque bloc a sa spécification chargée (D24)
    attendus = {b for b, *_ in blocs}
    verrou("tracabilite-I", attendus <= set(specs),
           str(attendus - set(specs)))
    return verrous


# --- Composition de l'image M5 ----------------------------------------------------

SHA_PROXY_051 = "fb41697ddde265ac"    # préfixe — la scellé 0.5.1 PROUVÉ v7/v8


def _somme_qwords(octets: bytes) -> int:
    return sum(struct.unpack(f"<{len(octets) // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF


def tranche_section(exe: bytes, rva: int, taille: int) -> bytes:
    if L.TEXT_RVA <= rva < L.RDATA_RVA:
        return exe[L.TEXT_FILE + (rva - L.TEXT_RVA):
                   L.TEXT_FILE + (rva - L.TEXT_RVA) + taille]
    if L.RDATA_RVA <= rva < L.DATA_RVA:
        return exe[L.RDATA_FILE + (rva - L.RDATA_RVA):
                   L.RDATA_FILE + (rva - L.RDATA_RVA) + taille]
    if L.DATA_RVA <= rva < L.TEXT2_RVA:       # .data committée (état serveur)
        return exe[L.DATA_FILE + (rva - L.DATA_RVA):
                   L.DATA_FILE + (rva - L.DATA_RVA) + taille]
    if L.TEXT2_RVA <= rva < L.TEXT3_RVA:
        return exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA):
                   L.TEXT2_FILE + (rva - L.TEXT2_RVA) + taille]
    if L.TEXT3_RVA <= rva < L.TEXT4_RVA:
        return exe[L.TEXT3_FILE + (rva - L.TEXT3_RVA):
                   L.TEXT3_FILE + (rva - L.TEXT3_RVA) + taille]
    if rva >= L.TEXT4_RVA:
        return exe[L.TEXT4_FILE + (rva - L.TEXT4_RVA):
                   L.TEXT4_FILE + (rva - L.TEXT4_RVA) + taille]
    raise EchecBuild(f"RVA {rva:#x} hors sections")


def composer_image_m5(texte_m4: bytes, rdata_m4: bytes, data_m4: bytes,
                      text2_m4: bytes, text3_m4: bytes, code: dict):
    """-> (texte, rdata, data, text2, text3, text4) — l'image de proxy.exe M5."""
    # .text4 : la section est composée EN PREMIER — la porte M5 scelle sa
    # somme sur CES octets (miroir D95 : la porte se garde elle-même).
    text4 = bytearray(b"\xcc" * L.TEXT4_VSIZE)
    for bid, _sid, _f, rva, slot in BLOCS_M5:
        text4[rva - L.TEXT4_RVA: rva - L.TEXT4_RVA + slot] = code[bid]["slot"]

    # .rdata : héritage M4 OCTET POUR OCTET + l'extension M5 (0x2CE0+)
    rdata = bytearray(rdata_m4)
    if len(rdata) != L.RDATA_VSIZE:
        raise EchecBuild(f".rdata héritée : {len(rdata)} o != {L.RDATA_VSIZE:#x}")
    zone_avant = bytes(rdata[0x2CC2 - L.RDATA_RVA:])
    if any(zone_avant):
        raise EchecBuild("la zone .rdata M5 (0x2CC2-0x2FFF) n'est pas vierge "
                         "dans l'héritage — R7 rompu")
    _poses: list[tuple[int, int, str]] = []

    def poser(rva_c: int, donnees: bytes, nom: str = ""):
        fin = rva_c + len(donnees)
        if fin > L.RDATA_RVA + L.RDATA_VSIZE:
            raise EchecBuild(f".rdata débordante à {rva_c:#x} (D33)")
        if rva_c < L.R_TXT_CMD_KO:
            raise EchecBuild(f"extension M5 sous {L.R_TXT_CMD_KO:#x} "
                             f"(R7 rompu) : {nom or hex(rva_c)}")
        for rva_p, fin_p, nom_p in _poses:
            if rva_c < fin_p and rva_p < fin:
                raise EchecBuild(
                    f"chevauchement .rdata M5 : {nom or hex(rva_c)} "
                    f"[{rva_c:#x}, {fin:#x}) recouvre {nom_p} "
                    f"[{rva_p:#x}, {fin_p:#x})")
        _poses.append((rva_c, fin, nom or hex(rva_c)))
        rdata[rva_c - L.RDATA_RVA: rva_c - L.RDATA_RVA + len(donnees)] = donnees

    # Les fixtures M5 (garde-fous de longueurs — la notation porte ces
    # valeurs) ; les littéraux de la ligne de flux vivent EN IMMÉDIATS dans
    # http-10:R3 (I9 — layout : la zone 0x2D30-0x2D7F reste VIERGE)
    fixtures = (
        (L.R_TXT_CMD_KO, L.TXT_CMD_KO, 37, "refus-cli"),
        (L.R_TXT_POLITIQUE, L.TXT_POLITIQUE, 20, "ligne-politique"),
    )
    for rva_c, chaine, attendu, nom in fixtures:
        if len(chaine) != attendu:
            raise EchecBuild(f"garde-fou fixture {nom} : {len(chaine)} o "
                             f"!= {attendu}")
        poser(rva_c, chaine + b"\x00", nom)
    if len(L.TXT_CMD_RELEVER) != 32:
        raise EchecBuild(f"garde-fou commande : {len(L.TXT_CMD_RELEVER)} o != 32")
    poser(L.R_CMD_RELEVER, L.TXT_CMD_RELEVER, "cmd-relever")

    # La table des descripteurs M5 : kernel32#2 (GetCommandLineW) + les TROIS
    # descripteurs hérités REPRIS (pointeurs identiques) + terminateur
    poser(L.R_IMPORTS_M5,
          struct.pack("<IIIII", L.R_INT_M5, 0, 0, L.R_NOM_KERNEL32_M5, L.R_IAT_M5)
          + struct.pack("<IIIII", L4.L3.R_INT_KERNEL32, 0, 0, L4.L3.R_NOM_DLL,
                        L4.L3.R_IAT)
          + struct.pack("<IIIII", L4.L3.R_INT_WS2, 0, 0, L4.L3.R_NOM_WS2,
                        L4.L3.R_IAT_WS2)
          + struct.pack("<IIIII", L4.R_INT_SEC32, 0, 0, L4.R_NOM_SEC32, L4.R_IAT_SEC32)
          + b"\x00" * 20, "descripteurs-M5")
    poser(L.R_NOM_KERNEL32_M5, b"kernel32.dll\x00", "nom-kernel32-M5")
    hn = struct.pack("<H", 0) + b"GetCommandLineW\x00"
    if len(hn) != 18:
        raise EchecBuild(f"garde-fou hints/name : {len(hn)} o != 18")
    poser(L.R_HN_M5, hn, "hn-GetCommandLineW")
    poser(L.R_IAT_M5, struct.pack("<QQ", L.R_HN_M5, 0), "iat-M5")
    poser(L.R_INT_M5, struct.pack("<QQ", L.R_HN_M5, 0), "int-M5")

    # LA PORTE M5 : UNE entrée (0x8000, 0x2000, somme .text4) — miroir D95
    poser(L.R_TAB_SUM_M5,
          struct.pack("<IIQ", L.TEXT4_RVA, L.TEXT4_VSIZE, _somme_qwords(bytes(text4))),
          "porte-M5")

    # LA VERSION : le delta documenté (R10 : monotonie — 0x00060000 > le
    # 0x00050003 du scellé 0.5.1, plancher 0x00040000 inchangé)
    struct.pack_into("<Q", rdata, L4.R_VERSION - L.RDATA_RVA, L.VERSION_U64_DEV1)

    # .data : l'état image — R_POLITIQUE naît à 0 (P3 de http-12:R3)
    data = bytearray(data_m4)
    politique = struct.unpack("<Q", bytes(data[0x3860 - L.DATA_RVA:
                                                  0x3860 - L.DATA_RVA + 8]))[0]
    if politique != 0:
        raise EchecBuild("R_POLITIQUE @0x3860 n'est pas à l'état image 0")

    return (bytes(texte_m4), bytes(rdata), bytes(data), bytes(text2_m4),
            bytes(text3_m4), bytes(text4))


# --- Éditeur PE32+ (six sections) ---------------------------------------------------

def ecrire_pe32plus(texte: bytes, rdata: bytes, data: bytes, text2: bytes,
                    text3: bytes, text4: bytes) -> bytes:
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 6, 0, 0, 0, 0xF0, 0x0002)
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B, 0, 0,
        L.ENTREE, len(texte) + len(text2) + len(text3) + len(text4), 0,
        L.ENTREE_M5, L.TEXT_RVA,   # AddressOfEntryPoint : 0x8C80 (http-12:R3 —
                                   # les ancêtres restent embarqués, R7)
        L.IMAGE_BASE,
        L.SECT_ALIGN, L.FILE_ALIGN,
        6, 0, 0, 1, 6, 0, 0,
        L.SIZE_OF_IMAGE,
        L.TEXT_FILE,               # SizeOfHeaders : 0x400
        0,
        3,                         # Subsystem : CONSOLE
        L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    dirs = [(0, 0)] * 16
    dirs[1] = (L.R_IMPORTS_M5, 100)   # le répertoire d'imports M5 @0x2DA0
    dirs[5] = (L4.R_RELOC, 12)
    dirs[12] = (L4.L3.R_IAT, 88)
    opt = bytes(opt_fixe) + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr,
                           0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", L.TEXT_VSIZE, L.TEXT_RVA, L.TEXT_VSIZE,
           L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", L.RDATA_VSIZE, L.RDATA_RVA, L.RDATA_VSIZE,
             L.RDATA_FILE, 0x40000040)
        + sh(b".data\x00\x00\x00", L.DATA_VSIZE, L.DATA_RVA, L.DATA_RAW,
             L.DATA_FILE, 0xC0000040)
        + sh(b".text2\x00\x00", L.TEXT2_VSIZE, L.TEXT2_RVA, L.TEXT2_VSIZE,
             L.TEXT2_FILE, 0x60000020)
        + sh(b".text3\x00\x00", L.TEXT3_VSIZE, L.TEXT3_RVA, L.TEXT3_VSIZE,
             L.TEXT3_FILE, 0x60000020)
        + sh(b".text4\x00\x00", L.TEXT4_VSIZE, L.TEXT4_RVA, L.TEXT4_VSIZE,
             L.TEXT4_FILE, 0x60000020)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 240, len(entetes)
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[L.TEXT_FILE:L.TEXT_FILE + len(texte)] = texte
    exe[L.RDATA_FILE:L.RDATA_FILE + len(rdata)] = rdata
    exe[L.DATA_FILE:L.DATA_FILE + len(data)] = data
    exe[L.TEXT2_FILE:L.TEXT2_FILE + len(text2)] = text2
    exe[L.TEXT3_FILE:L.TEXT3_FILE + len(text3)] = text3
    exe[L.TEXT4_FILE:L.TEXT4_FILE + len(text4)] = text4
    return bytes(exe)


# --- Validation PE -------------------------------------------------------------------

def valider_pe(exe: bytes):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.NumberOfSections == 6, "sections != 6"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE_M5, \
        f"point d'entrée != {L.ENTREE_M5:#x} (http-12:R3)"
    assert pe.OPTIONAL_HEADER.ImageBase == L.IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HEVA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2", ".text3", ".text4"], noms
    assert pe.sections[5].Characteristics & 0x60000020 == 0x60000020, \
        ".text4 non RX"
    assert pe.sections[2].SizeOfRawData == L.DATA_RAW
    assert pe.OPTIONAL_HEADER.SizeOfHeaders == L.TEXT_FILE, "SizeOfHeaders != 0x400"
    for s, attendu in zip(pe.sections, (L.TEXT_FILE, L.RDATA_FILE, L.DATA_FILE,
                                        L.TEXT2_FILE, L.TEXT3_FILE,
                                        L.TEXT4_FILE)):
        assert s.PointerToRawData == attendu, \
            f"PointerToRawData {s.Name.decode().rstrip(chr(0))} != {attendu:#x}"
    # Le répertoire d'imports M5 : kernel32 est décrit DEUX FOIS (les slots
    # scellés + GetCommandLineW), ws2_32 et secur32 repris à l'identique
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports.setdefault(entree.dll.decode().lower(), []).extend(
            i.name.decode() for i in entree.imports)
    # kernel32 décrit DEUX FOIS (le descripteur M5 MENÉ — GetCommandLineW —
    # puis les DIX slots scellés), ws2_32 et secur32 repris à l'identique
    assert imports["kernel32.dll"] == ["GetCommandLineW"] + L4.L3.KERNEL32_IMPORTS, \
        "kernel32 != GetCommandLineW + l'héritage"
    assert imports["ws2_32.dll"] == L4.L3.WS2_IMPORTS, "ws2_32 divergente"
    assert imports["secur32.dll"] == L4.SECUR32_IMPORTS, "secur32 divergente"
    ft = [(entree.dll.decode().lower(), entree.struct.FirstThunk,
           entree.struct.OriginalFirstThunk)
          for entree in pe.DIRECTORY_ENTRY_IMPORT]
    attendus_ft = {
        ("kernel32.dll", L.R_IAT_M5, L.R_INT_M5),
        ("kernel32.dll", L4.L3.R_IAT, L4.L3.R_INT_KERNEL32),
        ("ws2_32.dll", L4.L3.R_IAT_WS2, L4.L3.R_INT_WS2),
        ("secur32.dll", L4.R_IAT_SEC32, L4.R_INT_SEC32),
    }
    assert set(ft) == attendus_ft, f"thunks divergents : {ft}"
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress == L.R_IMPORTS_M5, \
        "répertoire d'imports != 0x2DA0 (M5)"
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].Size == 100
    assert len(exe) == L.TAILLE_FICHIER, "taille de fichier inattendue"
    # Zones réservées : int3 dans l'image livrée (héritage + .text4 —
    # 0x8FC0 : la réserve .text4 après le 2e réarrêt D8)
    for rva in (0x4200, 0x45C0, 0x4800, 0x7FC0, 0x8FC0):
        assert tranche_section(exe, rva, 1)[0] == 0xCC, \
            f"zone réservée @{rva:#x} != int3"
    # Version (R10 : monotonie — 0x00060000 > 0.5.1 = 0x00050003)
    version = struct.unpack("<Q", tranche_section(exe, L4.R_VERSION, 8))[0]
    assert version == L.VERSION_U64_DEV1, f"version {version:#x} != 0x00060000"
    # R_POLITIQUE @0x3860 : l'état image reste 0
    politique = struct.unpack("<Q", tranche_section(exe, L.R_POLITIQUE, 8))[0]
    assert politique == 0, "R_POLITIQUE naît armée (P3)"
    # Les fixtures M5 : concordance exacte
    for rva, chaine in ((L.R_TXT_CMD_KO, L.TXT_CMD_KO),
                        (L.R_TXT_POLITIQUE, L.TXT_POLITIQUE)):
        lu = tranche_section(exe, rva, len(chaine) + 1)
        assert lu == chaine + b"\x00", f"fixture @{rva:#x} divergente"
    assert tranche_section(exe, L.R_CMD_RELEVER, 32) == L.TXT_CMD_RELEVER, \
        "la commande --relever-https divergente"
    # La porte M5 : UNE entrée, la somme recalculée == la somme portée
    r, t, s = struct.unpack("<IIQ", tranche_section(exe, L.R_TAB_SUM_M5, 16))
    assert (r, t) == (L.TEXT4_RVA, L.TEXT4_VSIZE), "l'entrée M5 divergente"
    assert s == _somme_qwords(tranche_section(exe, r, t)), \
        "porte M5 : la somme de .text4 divergente"
    # La porte héritée R10 : la marche complète (28 entrées) reste auto-
    # consistante (miroir valider_pe du builder M4)
    k = 0
    rva_table = L4.R_TAB_SUM
    while rva_table + 16 * k < L4.R10_BORNE:
        r2, t2, s2 = struct.unpack("<IIQ",
                                   tranche_section(exe, rva_table + 16 * k, 16))
        assert r2 != 0 and t2 != 0, \
            f"porte R10 : entrée #{k + 1} trouée (fail-closed D95)"
        assert s2 == _somme_qwords(tranche_section(exe, r2, t2)), \
            f"porte R10 : somme de {r2:#x} divergente"
        k += 1
        assert k <= L4.R10_NB_ENTREES, "porte R10 : borne franchie"
    assert k == L4.R10_NB_ENTREES, f"porte R10 : {k} entrées != 28"
    return True


# --- Preuve de réutilisation (R7 — les TROIS générations) ----------------------------

def preuve_reutilisation(exe: bytes) -> dict:
    """proxy.exe M5 partage son squelette avec le scellé 0.5.1 : .text/
    .text2/.data/.text3 OCTET POUR OCTET ; .rdata identique jusqu'à 0x2CC2
    (l'extension M5 vit dans la zone VIERGE VÉRIFIÉE) ; les deltas PE sont
    documentés. Les ancêtres 0.4.0/0.5.0 restent vérifiés par build_m4."""
    scelle_p = os.path.join(M4_DIR, "proxy.exe")
    with open(scelle_p, "rb") as f:
        scelle = f.read()
    if hashlib.sha256(scelle).hexdigest()[:16] != SHA_PROXY_051:
        raise EchecBuild("proxy.exe 0.5.1 divergent de l'artefact scellé "
                         "PROUVÉ par les runs v7/v8 (R7)")
    for nom, section, vsize, fichier in (
            (".text", tranche_section(exe, L.TEXT_RVA, L.TEXT_VSIZE),
             L.TEXT_VSIZE, L.TEXT_FILE),
            (".text2", tranche_section(exe, L.TEXT2_RVA, L.TEXT2_VSIZE),
             L.TEXT2_VSIZE, L.TEXT2_FILE),
            (".data", tranche_section(exe, L.DATA_RVA, L.DATA_RAW),
             L.DATA_RAW, L.DATA_FILE),
            (".text3", tranche_section(exe, L.TEXT3_RVA, L.TEXT3_VSIZE),
             L.TEXT3_VSIZE, L.TEXT3_FILE)):
        scelle_section = scelle[fichier: fichier + vsize]
        if section != scelle_section:
            for k, (x, y) in enumerate(zip(section, scelle_section)):
                if x != y:
                    raise EchecBuild(
                        f"R7 rompu : {nom} @{L.TEXT_RVA if nom == '.text' else ''}"
                        f"diverge du scellé 0.5.1 à l'octet {k:#x}")
    # .rdata : identique au scellé AVANT l'extension M5 (0x2CC2) SAUF LA
    # VERSION @0x2820 — LE delta documenté (R10 : monotonie, 0x00060000 >
    # 0x00050003 ; le même arbitrage que la preuve M4 pour sa version)
    for debut, fin in ((L.RDATA_RVA, L4.R_VERSION), (L4.R_VERSION + 8, 0x2CC2)):
        if tranche_section(exe, debut, fin - debut) != \
                scelle[L.RDATA_FILE + (debut - L.RDATA_RVA):
                       L.RDATA_FILE + (debut - L.RDATA_RVA) + (fin - debut)]:
            raise EchecBuild(f"R7 rompu : .rdata diverge du scellé 0.5.1 "
                             f"entre {debut:#x} et {fin:#x} (hors version)")
    # Les deltas PE documentés
    pe_m5 = pefile.PE(data=exe)
    pe_s = pefile.PE(data=scelle)
    assert pe_m5.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE_M5
    assert pe_s.OPTIONAL_HEADER.AddressOfEntryPoint == L4.ENTREE_R2
    assert pe_m5.OPTIONAL_HEADER.SizeOfImage == 0xA000
    assert pe_s.OPTIONAL_HEADER.SizeOfImage == 0x8000
    return {"sha_proxy_051": SHA_PROXY_051,
            "blocs_reutilises": len(B4.BLOCS_EMBARQUES_M4)}


# --- Verrou croisé et carte ----------------------------------------------------------
# La carte génération 7 est un fait de CÉRÉMONIE (les secrets vivent hors
# du laboratoire — D87) ; le build vérifie ce qu'il peut et nomme ce qui
# reste à l'opérateur. Le verrou croisé s'installe à la cérémonie.

def verifier_carte_possible() -> str:
    """-> le motif : 'cérémonie requise' (secrets absents) ou 'prête'."""
    chemin_phrase = os.path.join(TRIADE, ".keys", "passphrase.txt")
    chemin_graine = os.path.join(TRIADE, ".keys", "ed25519.seed")
    if not os.path.exists(chemin_phrase) or not os.path.exists(chemin_graine):
        return ("cérémonie requise (D87) : les secrets de la carte ne vivent "
                "pas au laboratoire — l'opérateur scelle (R6/R8/R9)")
    return "prête"


# --- Assemblage + vérification --------------------------------------------------------

def assembler_tout_m5() -> tuple[dict, dict, list]:
    """Les trois révisions M5 : assemblage, tailles déclarées, round-trip."""
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    specs = charger_couche_I_m5()
    code: dict[str, dict] = {}
    for bid, sid, fichier, rva, slot in BLOCS_M5:
        chemin = chemin_notation_m5(fichier)
        octets, metas = assembler_bloc(ks, chemin, rva, slot)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot_complet = octets + b"\x90" * (slot - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns,
                     "slot": slot_complet}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, "
              f"round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel_m5(specs, code, BLOCS_M5)
    print(f"[oracle] structurel M5 : {len(verrous)} verrous PASS "
          f"(contrats I vérifiés par bloc)")
    return specs, code, verrous


def blobs_oracle(code_m3: dict, code_m4: dict, code_m5: dict) -> dict:
    blobs = {}
    for bid, cle in _CLE_BLOB.items():
        if bid in code_m5:
            blobs[cle] = code_m5[bid]["octets"]
        elif bid in code_m4:
            blobs[cle] = code_m4[bid]["octets"]
        else:
            blobs[cle] = code_m3[bid]["octets"]
    return blobs


# --- Modes -----------------------------------------------------------------------------

def construire(volume: str, graine: int) -> int:
    print("=== M5 : chaîne artefact TRIADE (profil x86-64-win11-pe, 0.6.0) ===")
    _garde_sceau_I()

    # 1. Héritage M3+M4 re-vérifié de bout en bout (R5 + oracles structurels)
    print("[héritage] re-vérification M3+M4 complète (build_m4.assembler_tout_m4)…")
    specs_m4, code_m4, verrous_m4 = B4.assembler_tout_m4()
    blocs_m3, _specs_m3, code_m3, verrous_m3 = B4.B3.assembler_tout()
    texte_m3, rdata_m3, data_m3, text2_m3 = B4.B3.composer_sections(code_m3, blocs_m3)
    print(f"[héritage] M3 : {len(verrous_m3)} verrous ; M4 : {len(verrous_m4)} verrous")

    # 2. L'image M4 composée == le scellé 0.5.1, OCTET PAR OCTET (preuve R7)
    with open(os.path.join(M4_DIR, "proxy.exe"), "rb") as f:
        scelle_051 = f.read()
    sections_m4 = B4.composer_image_m4(
        texte_m3, rdata_m3, data_m3, text2_m3, code_m4,
        code_m4["b20007"]["slot"])
    exe_m4_compose = B4.ecrire_pe32plus(*sections_m4)
    if hashlib.sha256(exe_m4_compose).hexdigest() != hashlib.sha256(scelle_051).hexdigest():
        raise EchecBuild("l'image M4 composée diverge du scellé 0.5.1 "
                         "(fb41697d…) — R7")
    print(f"[R7] l'image M4 composée == le scellé 0.5.1 OCTET POUR OCTET "
          f"(sha {SHA_PROXY_051}…) — les runs v7/v8 PROUVENT CES OCTETS")

    # 3. Blocs M5 : assemblage et oracle structurel
    specs_m5, code_m5, verrous_m5 = assembler_tout_m5()

    # 4. Composition de l'image M5 (deltas documentés + .text4)
    texte, rdata, data, text2, text3, text4 = composer_image_m5(
        sections_m4[0], sections_m4[1], sections_m4[2], sections_m4[3],
        sections_m4[4], code_m5)
    exe = ecrire_pe32plus(texte, rdata, data, text2, text3, text4)
    valider_pe(exe)
    print(f"[PE] proxy.exe : {len(exe)} octets, 6 sections (.text4 0x8000), "
          f"kernel32 x10 + GetCommandLineW + ws2_32 x13 + secur32 x7, "
          f"entrée {L.ENTREE_M5:#x} (http-12:R3 — la CLI et la porte M5)")

    # 5. Preuves R7 (les TROIS générations)
    heritage = preuve_reutilisation(exe)
    print(f"[R7] réutilisation : {heritage['blocs_reutilises']} blocs "
          f"octet-identiques au scellé 0.5.1 (héritage complet), "
          f"deltas .rdata/.text4/PE documentés")

    # 6. L'oracle M4 (l'héritage rejoué sur ses blobs) PUIS l'oracle M5 étendu
    blobs_m4 = B4.blobs_oracle(code_m3, code_m4)
    verdict_m4 = od4.executer(blobs_m4, graine=graine, volume=volume)
    print(f"[oracle] différentiel M4 (héritage) : {verdict_m4['total_cas']} "
          f"cas verts")
    blobs = blobs_oracle(code_m3, code_m4, code_m5)
    manquants = {"http-08-R3", "http-10-R3", "http-12-R3"} - set(blobs)
    if manquants:
        raise EchecBuild(f"blobs manquants pour l'oracle M5 : {manquants}")
    verdict = od5.executer(blobs, graine=graine, volume=volume)
    print(f"[oracle] différentiel M5 (scénarios étendus D136) : "
          f"{verdict['total_cas']} cas verts ; falsification détectée")

    # 7. Écriture de l'artefact
    with open(os.path.join(ICI, "proxy.exe"), "wb") as f:
        f.write(exe)

    # 8. La carte génération 7 : un fait de cérémonie (D87)
    etat_carte = verifier_carte_possible()
    print(f"[carte] génération 7 : {etat_carte}")
    print(f"[B] proxy.exe 0.6.0-dev.1 : sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== M5-dev (oracle vert) : {L.VERSION_DEV1} — le flux navigateur "
          f"embarqué et CÂBLÉ, cérémonie de signature puis terrain (étape 2) "
          f"en attente ===")
    return 0


def verifier(graine: int, volume: str) -> int:
    print(f"=== M5 : re-vérification complète (R5/R7, graine {graine}) ===")
    _garde_sceau_I()
    specs_m4, code_m4, verrous_m4 = B4.assembler_tout_m4()
    blocs_m3, _s3, code_m3, verrous_m3 = B4.B3.assembler_tout()
    specs_m5, code_m5, verrous_m5 = assembler_tout_m5()
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    heritage = preuve_reutilisation(exe)
    print(f"[R7] {heritage['blocs_reutilises']} blocs réutilisés du scellé "
          f"0.5.1, deltas documentés")
    blobs_m4 = B4.blobs_oracle(code_m3, code_m4)
    verdict_m4 = od4.executer(blobs_m4, graine=graine, volume=volume)
    print(f"[oracle] différentiel M4 (héritage) : {verdict_m4['total_cas']} cas verts")
    blobs = blobs_oracle(code_m3, code_m4, code_m5)
    verdict = od5.executer(blobs, graine=graine, volume=volume)
    print(f"[oracle] différentiel M5 : {verdict['total_cas']} cas verts")
    valider_pe(exe)
    print("[PE] proxy.exe 0.6.0-dev.1 re-validé (6 sections, porte M5, porte "
          "R10, fixtures M5, version 0x00060000)")
    print(f"[carte] génération 7 : {verifier_carte_possible()}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--verifier" in args:
            graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 20261103
            volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
            sys.exit(verifier(graine, volume))
        volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 20261103
        sys.exit(construire(volume, graine))
    except (EchecBuild, EchecOracle) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
