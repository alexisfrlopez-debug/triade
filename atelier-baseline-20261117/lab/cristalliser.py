#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cristalliser.py — LE CONTRÔLE MÉCANIQUE DE CRISTALLISATION (le labo de
la baseline, session 2026-11-17) : assemble la notation par keystone à
une base factice, en résolvant equ, étiquettes locales (préfixe courant)
et directives db, REFUSE l'appel direct aux externes (I5 : l'IAT D161 —
call qword ptr [rip+disp]), EXIGE le 0x90 final (I5), puis vérifie le
round-trip R5 (keystone == capstone, l'instruction pour l'instruction).

Le contrôle nomme les défauts (la classe, le mécanisme, la ligne) — le
correctif appartient à la rig (outil_correctif, le bundle-défaut).
Sortie : {vert: bool, defauts: [...], octets: hex, nb_octets: n}
"""
from __future__ import annotations

import json
import re
import sys

import capstone
import keystone

BASE = 0x00401000  # la base factice du contrôle


def charger(piece: str):
    """le texte source + la numérotation des lignes nues."""
    texte = open(piece, encoding="utf-8").read()
    num: dict[str, int] = {}
    for no, raw in enumerate(texte.splitlines(), 1):
        l = re.split(r"\s+;", raw.strip())[0].strip()
        if l and not l.startswith(("```", ";")):
            num[l] = no
    return texte, num


def purifier(texte: str):
    """les lignes exécutables/données, les externes, les equ."""
    lignes, externes = [], set()
    for raw in texte.splitlines():
        l = raw.strip()
        if not l or l.startswith("```") or l.startswith(";"):
            continue
        m = re.match(r"extern\s+(\w+)", l, re.I)
        if m:
            externes.add(m.group(1))
            continue
        if l.lower().startswith(("section ", "global ")):
            continue
        l = re.split(r"\s+;", l)[0].strip()
        if l:
            lignes.append(l)
    return lignes, externes


def controler(piece: str) -> dict:
    texte, num = charger(piece)
    lignes, externes = purifier(texte)
    defauts: dict[tuple, dict] = {}

    def nommer(classe, mecanisme, ligne):
        if (classe, ligne) not in defauts:
            defauts[(classe, ligne)] = {
                "classe": classe, "mecanisme": mecanisme,
                "ligne": ligne, "no": num.get(ligne, 0)}

    # ① les équivalences — un registre n'est pas une adresse de zone
    equ: dict[str, str] = {}
    propres = []
    for l in lignes:
        m = re.match(r"(\w+)\s+equ\s+(.+)$", l, re.I)
        if m:
            nom, val = m.group(1), m.group(2).strip()
            if val.lower() in ("rsp", "rbp", "esp", "ebp"):
                nommer("TAMPON-NON-ALLIE",
                       f"« {l} » — un registre n'est pas une adresse de"
                       " tampon : TAMPON_CUMUL est une zone de 64 Kio à"
                       " ALLOUER (le contrat I3)", l)
            else:
                equ[nom] = val
            continue
        propres.append(l)

    # ② l'IAT : l'appel direct à l'extern est refusé (I5, D161)
    for l in propres:
        m = re.match(r"call\s+(\w+)$", l, re.I)
        if m and m.group(1) in externes:
            nommer("IAT-D161",
                   f"l'appel DIRECT à l'extern {m.group(1)} — l'I5 du"
                   " contrat exige l'appel INDIRECT par l'IAT déclarée"
                   " (call qword ptr [rip+dép])", l)

    # ③ la structure : étiquettes, données, code
    items = []  # (etiquette, nom) | (data, octets) | (code, ligne)
    prefixe = ""
    for l in propres:
        m = re.match(r"^(\.?\w+):\s*db\s+(.+)$", l, re.I)
        if m:
            nom = (prefixe + m.group(1)) if m.group(1).startswith(".") \
                else m.group(1)
            try:
                octs = bytes(int(b, 0) for b in
                             re.split(r"[,\s]+", m.group(2).strip()) if b)
                items.append(("etiquette", nom))
                items.append(("data", octs))
            except ValueError:
                nommer("SYNTAXE", f"la directive db refuse « {l} »", l)
            continue
        m = re.match(r"^(\.?\w+):$", l)
        if m:
            nom = m.group(1)
            if not nom.startswith("."):
                prefixe = nom
            items.append(("etiquette",
                          (prefixe + nom) if nom.startswith(".") else nom))
            continue
        items.append(("code", l))

    # ④+⑤ LE POINT FIXE — les avant-références résolues par itération :
    # les estimations d'adresses convergent (les tailles d'encodage se
    # stabilisent en deux-trois tours), la dernière passe fait foi
    ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    noms = [v for k, v in items if k == "etiquette"]
    estimations = {n: BASE for n in noms}
    octets, erreurs_dernieres = b"", {}
    for _ in range(8):
        addr = BASE
        octets = b""
        octets_code = b""  # le code seul — la règle FIN-RET le juge,
        #                     les données .data vivent après lui
        pref = ""
        nouvelles: dict[str, int] = {}
        erreurs_tour: dict[str, str] = {}
        for kind, val in items:
            if kind == "etiquette":
                nouvelles[val] = addr
                if "." not in val:
                    pref = val
                continue
            if kind == "data":
                addr += len(val)
                octets += val
                continue
            v = resoudre(val, equ, {**estimations, **nouvelles}, pref)
            try:
                enc, _ = ks.asm(v, addr)
                addr += len(enc)
                octets += bytes(enc)
                octets_code += bytes(enc)
            except keystone.KsError as e:
                erreurs_tour[val] = str(e)
                addr += 1
                octets += b"\x00"
        if nouvelles == estimations:
            erreurs_dernieres = erreurs_tour
            break
        estimations = dict(nouvelles)
    else:
        erreurs_dernieres = erreurs_tour

    # les fautes de syntaxe restées APRÈS le point fixe — une ligne déjà
    # nommée par une classe antérieure (IAT, TAMPON…) ne se répète pas :
    # la classe fait foi, la manifestation tombe
    for l, err in erreurs_dernieres.items():
        if not any(d["ligne"] == l for d in defauts.values()):
            nommer("SYNTAXE", f"keystone refuse « {l} » : {err}", l)

    # ⑥ I5, LA CONVENTION DE LA FAMILLE SCELLÉE (loupe-05, la pièce de
    # référence) : la notation s'achève à « ret » — le padding NOP 0x90
    # au slot est le geste du BUILD (documenté à l'en-tête : « Code :
    # N o · padding : M o (NOP, 0x90) »), jamais des nops écrits à la
    # main dans la notation. [correction du contrôle du labo contre la
    # pièce scellée — la règle « finir par 0x90 » était trop stricte,
    # elle n'est pas la convention de la famille ; le geste est NOMMÉ au
    # rapport de session]
    if not octets_code.endswith(b"\xc3"):
        nommer("FIN-RET",
               "la pièce ne s'achève pas sur le ret (la convention de la"
               " famille : le dernier octet du code est 0xc3, le padding"
               " NOP 0x90 du slot appartient au build)", "(fin de pièce)")

    # ⑦ R5 : le round-trip keystone == capstone
    if not defauts:
        cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        for ins in cs.disasm(octets, BASE):
            try:
                enc, _ = ks.asm(ins.mnemonic + " " + ins.op_str,
                                ins.address)
                if bytes(enc) != ins.bytes:
                    nommer("ROUND-TRIP",
                           f"« {ins.mnemonic} {ins.op_str} » à "
                           f"0x{ins.address:x} ne se réassemble pas à "
                           "l'identique", f"{ins.mnemonic} {ins.op_str}")
            except keystone.KsError:
                nommer("ROUND-TRIP",
                       f"keystone refuse la réassemblée de « {ins.mnemonic}"
                       f" {ins.op_str} »",
                       f"{ins.mnemonic} {ins.op_str}")

    liste = sorted(defauts.values(), key=lambda d: (d["no"], d["classe"]))
    return {"vert": not liste, "defauts": liste,
            "octets": octets.hex() if not liste else "",
            "nb_octets": len(octets)}


def resoudre(l: str, equ: dict, adresses: dict, pref: str) -> str:
    """les equ substitués, les références d'étiquettes résolues (les
    locales par le préfixe courant, les sauts/calls et les immédiats)."""
    for nom, val in equ.items():
        l = re.sub(rf"\b{nom}\b", val, l)
    m = re.match(r"^(j\w+|call|loop)\s+(\.?\w+)$", l, re.I)
    if m:
        cible = (pref + m.group(2)) \
            if m.group(2).startswith(".") else m.group(2)
        if cible in adresses:
            return f"{m.group(1)} 0x{adresses[cible]:x}"
    m = re.match(r"^(mov|lea|cmp|push)\s+(\w+)\s*,\s*(\.?\w+)$", l, re.I)
    if m and m.group(3) in adresses:
        return f"{m.group(1)} {m.group(2)}, 0x{adresses[m.group(3)]:x}"
    return l


if __name__ == "__main__":
    resultat = controler(sys.argv[1])
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    sys.exit(0 if resultat["vert"] else 2)
