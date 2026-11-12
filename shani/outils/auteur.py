#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shani/outils/auteur.py — Outil d'auteur du domaine shani (la variante
SHA-NI, D205) : résolution des étiquettes.

Même discipline qu'en M1..M10 (aucun compilateur entre l'intention et les
octets : keystone assemble, rien d'autre) — cet outil fait l'arithmétique
d'adresses de l'auteur : étiquettes locales -> adresses absolues des sauts,
symboles de blocs -> cibles d'appels directes (I1 des specs), symboles de
données -> déplacements RIP calculés une fois pour toutes depuis le plan
d'adressage shani/layout.py (source unique — le masque BE @0x2800, les
SEIZE groupes de la table K DU SCELLÉ @0x2F00+16·g, et les adresses
scellées R_TLS01..04 importées du plan loupe).

Entrée : notation/brouillons/*.asm. Sortie : notation/*.asm — notation
explicite WYSIWYG, seule lue par le vérificateur et le kit (round-trip R5
sur la sortie par le vérificateur du paquet).

LES SLOTS sont ARRÊTÉS ICI sur les longueurs réelles (D161 : la mesure
auteur décide, la préfiguration s'incline) — l'outil REFUSE tout
débordement (D8 : multiple de 64, padding ≥ 16).

AUCUN SCELLAGE : les blocs générés sont des COPIES DE LABORATOIRE — la
cérémonie d'ère et la carte appartiennent au développeur (charte § 3 du
domaine) ; l'en-tête le dit à chaque fichier.

Usage : python3 outils/auteur.py [--verifier-seulement]
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import layout as L  # noqa: E402  # le plan shani (la source unique)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "..", "notation", "brouillons")
SORTIE = os.path.join(ICI, "..", "notation")

# (fichier brouillon, id bloc, spec, dépendances) — rva/slot dérivés du plan
# d'adressage (layout.py, source unique de vérité ; l'ARRÊT DÉFINITIF des
# slots est celui du plan — la mesure auteur, D161 rejoué). Les ids g21000N
# sont PRÉFIGURÉS pour la carte à naître — AUCUN bloc n'est dans la carte
# aujourd'hui (charte § 3 : le scellage appartient au développeur).
_FICHIERS = {
    "g210001": ("shani-01-sonde", "shani-01:R1",
                "bloc feuille ; CPUID feuilles 7-0 (EBX bit 29 SHA) et 1 "
                "(ECX bit 9 SSSE3) — rbx sauvé (I2), AUCUN autre effet "
                "(Q3) ; AUCUN déplacement RIP"),
    "g210002": ("shani-02-comprimer", "shani-02:R1",
                "bloc feuille ; LE MÊME CONTRAT que tls13-02 (R4) — la "
                "compression FIPS § 6.2.2 par sha256rnds2/msg1/msg2 ; le "
                "corps DÉROULÉ en 16 phases (I3 : zéro saut) ; le masque "
                "BE @R_MASQUE et les SEIZE groupes K du scellé "
                "(@R_K+16·g) cités par déplacement RIP (I2) ; xmm6/7 "
                "sauvés sur la pile (I4)"),
    "g210003": ("shani-03-absorber", "shani-03:R1",
                "shani-01 (la sonde — UNE fois par appel, I1) ; DEUX "
                "appels directs déclarés : shani-02 la variante, tls13-02 "
                "LE SCELLÉ à 0xC080 (le repli, R7) ; le miroir de "
                "tls13-03 (le chemin PLEIN sur l'ÉGALITÉ STRICTE)"),
}


def blocs_shani() -> list[tuple]:
    out = []
    for bid, (fichier, spec, deps) in _FICHIERS.items():
        rva, slot = L.SLOTS_SHANI[bid]
        out.append((fichier, bid, spec, rva, slot, deps))
    return out


BLOCS = blocs_shani()

SYMBOLES = {
    # les blocs du domaine (le plan, source unique — les appels directs I1)
    "SHANI01": L.SHANI01_VA,
    "SHANI02": L.SHANI02_VA,
    "SHANI03": L.SHANI03_VA,
    # le repli scellé (R7 — le plan loupe, importé, source unique)
    "TLS01": L.R_TLS01,
    "TLS02": L.R_TLS02,
    "TLS03": L.R_TLS03,
    "TLS04": L.R_TLS04,
    # le masque BE de la variante
    "MASQUE": L.R_MASQUE,
    # les SEIZE groupes de la table K DU SCELLÉ (jamais dupliquée)
    **{f"K_G{g}": L.R_K + 16 * g for g in range(16)},
}

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_RIP_CIBLE = re.compile(r"^(.*?\[rip\s*([+-])\s*)(\w+|\.\w+)(\s*\].*)$")

REGISTRES64 = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"} \
    | {f"r{i}" for i in range(8, 16)}


class ErreurAuteur(Exception):
    pass


def lire_brouillon(chemin: str):
    instructions, etiquettes_lignes = [], []
    with open(chemin, encoding="utf-8") as f:
        for numero, brut in enumerate(f.read().splitlines(), 1):
            ligne = brut.split(";")[0].strip()
            if not ligne:
                continue
            m = RE_ETIQUETTE.match(ligne)
            if m:
                etiquettes_lignes.append((m.group(1), len(instructions)))
                continue
            instructions.append((ligne, numero))
    return instructions, etiquettes_lignes


def cible_rip(nom: str, etiquettes: dict):
    if nom.startswith("."):
        if nom[1:] not in etiquettes:
            raise ErreurAuteur(f"étiquette inconnue : {nom}")
        return etiquettes[nom[1:]]
    if nom not in SYMBOLES:
        raise ErreurAuteur(f"symbole de données inconnu : {nom}")
    return SYMBOLES[nom]


def taille_ligne(ks: Ks, ligne: str, adresse: int, etiquettes: dict) -> int:
    enc, _ = ks.asm(substituer(ligne, adresse, etiquettes, taille=True), adresse)
    if not enc:
        raise ErreurAuteur(f"ligne inassemblable (calcul de taille) : {ligne!r}")
    return len(enc)


def substituer(ligne: str, adresse: int, etiquettes: dict, taille: int = 0) -> str:
    m = RE_OPERANDE_ETIQUETTE.match(ligne)
    if m:
        mnemo, nom = m.groups()
        cible = etiquettes.get(nom)
        if cible is None:
            raise ErreurAuteur(f"étiquette inconnue : .{nom}")
        return f"{mnemo} 0x{cible:x}"
    m = RE_OPERANDE_SYMBOLE.match(ligne)
    if m:
        mnemo, nom = m.groups()
        if nom in REGISTRES64:
            return ligne          # l'appel indirect DÉCLARÉ (jamais ici aujourd'hui)
        if nom not in SYMBOLES:
            raise ErreurAuteur(f"symbole de bloc inconnu : {nom}")
        return f"{mnemo} 0x{SYMBOLES[nom]:x}"
    m = RE_RIP_CIBLE.match(ligne)
    if m and m.group(3) in SYMBOLES:
        avant, signe, nom, apres = m.groups()
        if taille:
            return f"{avant}0x0{apres}"
    return ligne


def resoudre_rip(ligne: str, adresse: int, taille: int, etiquettes: dict) -> str:
    m = RE_RIP_CIBLE.match(ligne)
    if not m:
        return ligne
    avant, signe, nom, apres = m.groups()
    if signe == "-":
        raise ErreurAuteur(f"forme [rip - symbole] non supportée : {ligne!r}")
    cible = cible_rip(nom, etiquettes)
    disp = cible - (adresse + taille)
    if disp >= 0:
        return f"{avant}0x{disp:x}{apres}"
    return f"{avant[:avant.rindex('+')]}- 0x{-disp:x}{apres}"


NOMS_COURTS = L.NOMS_COURTS


def resoudre_bloc(ks: Ks, fichier: str, bid: str, spec: str, rva: int,
                  slot: int, deps: str):
    chemin = os.path.join(BROUILLONS, fichier + ".asm")
    instructions, etiquettes_lignes = lire_brouillon(chemin)
    if not instructions:
        raise ErreurAuteur(f"{fichier} : brouillon vide")

    etiquettes = {nom: rva + 0x80 for nom, _ in etiquettes_lignes}
    for _ in range(8):
        tailles, adresse = [], rva
        for ligne, _ in instructions:
            t = taille_ligne(ks, ligne, adresse, etiquettes)
            tailles.append(t)
            adresse += t
        nouvelles = {}
        for nom, index in etiquettes_lignes:
            nouvelles[nom] = rva + sum(tailles[:index])
        if nouvelles == etiquettes:
            break
        etiquettes = nouvelles
    else:
        raise ErreurAuteur(f"{fichier} : pas de point fixe en 8 passes")

    lignes_sortie, adresse, calculs = [], rva, []
    for ligne, numero in instructions:
        taille = tailles[len(lignes_sortie)]
        explicite = resoudre_rip(
            substituer(ligne, adresse, etiquettes), adresse, taille, etiquettes)
        lignes_sortie.append((explicite, adresse, taille, numero))
        adresse += taille
    total = adresse - rva
    if total > slot:
        raise ErreurAuteur(f"{fichier} : {total} o > slot {slot:#x} (D8) — "
                           "réarrêter le plan d'adressage sur la mesure")
    if slot - total < 16:
        raise ErreurAuteur(f"{fichier} : padding {slot - total} < 16 (D8)")

    entete = [
        f"; {fichier} · bloc {NOMS_COURTS[fichier]} · spec {spec} · bloc carte {bid} "
        "(PRÉFIGURÉ — la variante n'est PAS dans la carte : charte § 3, "
        "le scellage appartient au développeur)",
        f"; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x{rva:x}, taille {slot} octets",
        f"; Domaine : shani (la variante SHA-NI, D205 — JAMAIS SCELLÉE) · Dépendances : {deps}",
        "; Notation explicite générée par outils/auteur.py depuis brouillons/"
        f"{fichier}.asm",
        "; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)",
        f"; Code : {total} o · padding : {slot - total} o (NOP, 0x90)",
    ]
    if etiquettes_lignes:
        entete.append("; Étiquettes résolues : " + ", ".join(
            f".{nom}=0x{etiquettes[nom]:x}" for nom, _ in etiquettes_lignes))
    refs = [l for l, *_ in lignes_sortie if "[rip" in l]
    if refs:
        entete.append("; Déplacements RIP (cible = adresse + taille + disp) :")
        for ligne_e, adr, t, _ in lignes_sortie:
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", ligne_e)
            if m:
                cible = adr + t + (int(m.group(2), 16) if m.group(1) == "+"
                                   else -int(m.group(2), 16))
                calculs.append((ligne_e, adr, t, cible))
                entete.append(f";   0x{adr:x} + 0x{t:x} "
                              f"{'+' if m.group(1) == '+' else '-'} "
                              f"{m.group(2)} = 0x{cible:x}")
    appels = [l for l, *_ in lignes_sortie if l.startswith("call ")]
    if appels:
        entete.append("; Appels directs (le plan, source unique — I1) : "
                      + ", ".join(appels))
    sauts = [l for l, *_ in lignes_sortie
             if l.startswith("j") or l.startswith("loop")]
    if sauts:
        entete.append("; Sauts : " + ", ".join(sauts))

    corps = [l for l, *_ in lignes_sortie]
    return fichier, bid, rva, slot, total, entete, corps, etiquettes


def ecrire(fichier: str, entete: list, corps: list) -> None:
    chemin = os.path.join(SORTIE, fichier + ".asm")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for ligne in corps:
            f.write(ligne + "\n")


def main(verifier_seulement: bool = False) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== shani/outils/auteur.py — la résolution des étiquettes "
          "(keystone, rien d'autre) ===")
    arretes = {}
    for fichier, bid, spec, rva, slot, deps in BLOCS:
        (fichier, bid, rva, slot, total, entete, corps,
         etiquettes) = resoudre_bloc(ks, fichier, bid, spec, rva, slot, deps)
        arretes[fichier] = (rva, slot, total, len(corps))
        print(f"  {fichier:22} slot 0x{rva:x} · code {total} o · "
              f"padding {slot - total} o · {len(corps)} instructions "
              f"· étiquettes {list(etiquettes)}")
        if not verifier_seulement:
            ecrire(fichier, entete, corps)
    # l'ARRÊT D161 consigné : le plan préfiguré vs la mesure
    print("\nL'ARRÊT SUR LES MESURES (D161) :")
    for fichier, (rva, slot, total, n) in arretes.items():
        print(f"  {fichier:22} préfiguré {slot:#x} · mesuré {total} o "
              f"→ {'TENU' if total <= slot else 'DÉBORDÉ'} (padding "
              f"{slot - total} ≥ 16 : {'OUI' if slot - total >= 16 else 'NON'})")
    fin = max(rva + slot for rva, slot, _, _ in arretes.values())
    print(f"  fin de zone : 0x{fin:x} (la réserve .text2 jusqu'à 0xDFFF "
          f"demeure vierge : {0xE000 - fin} o)")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifier-seulement" in sys.argv))
