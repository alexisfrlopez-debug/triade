#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du jalon M1 : résolution des étiquettes.

TRIADE interdit tout compilateur entre l'intention et les octets : la notation
est assemblée par keystone, seule. Cet outil n'assemble RIEN de nouveau — il
fait l'arithmétique d'adquences de l'auteur (celle que M0 consignait à la main
dans les en-têtes « 0x1056 + 0x1062 = 0x20B8 ») :

  - étiquettes locales (.fin)  -> adresses absolues des sauts ;
  - symboles de blocs (MEMCPY) -> cibles d'appels directes ;
  - symboles de données (S_SA) -> déplacements RIP calculés une fois pour
    toutes depuis layout.py.

Entrée : notation/brouillons/*.asm (lignes d'instruction, étiquettes en fin de
ligne «.nom:», commentaires «;»).
Sortie : notation/*.asm — notation explicite WYSIWYG, seule lue par build_m1.py
(le round-trip keystone/capstone/R5 s'applique à la sortie, jamais à l'entrée).

Itérations jusqu'au point fixe : keystone choisit rel8/rel32 selon la distance,
la taille d'un saut peut donc changer quand les adresses se stabilisent —
deux passes suffisent en pratique, trois par précaution.

Usage : python3 outils/auteur.py [--verifier-seulement]
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import layout as L

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "..", "notation", "brouillons")
SORTIE = os.path.join(ICI, "..", "notation")

# (fichier brouillon, fichier sortie, id bloc, spec, rva, slot, dépendances)
BLOCS = [
    ("libc-01-memcpy", "b20001", "libc-01:R1", 0x1100, 0x80,
     "bloc feuille ; aucun accès extérieur"),
    ("libc-02-memcmp", "b20002", "libc-02:R1", 0x1180, 0x80,
     "bloc feuille ; aucun accès extérieur"),
    ("libc-03-strlen", "b20003", "libc-03:R1", 0x1200, 0x80,
     "bloc feuille ; aucun accès extérieur"),
    ("libc-04-itoa", "b20004", "libc-04:R1", 0x1280, 0x80,
     "bloc feuille ; tampon fourni par l'appelant"),
    ("libc-05-zone-alloc", "b20005", "libc-05:R1", 0x1300, 0x80,
     "données : curseur @0x3000, arène @0x3040"),
    ("libc-06-zone-reset", "b20006", "libc-06:R1", 0x1380, 0x40,
     "données : curseur @0x3000"),
    ("libc-07-memset", "b20007", "libc-07:R1", 0x13C0, 0x80,
     "bloc feuille ; aucun accès extérieur"),
    ("libc-08-autotest", "b20008", "libc-08:R1", 0x1800, 0x800,
     "blocs libc-01…07, io-01 write @0x1040, io-02 exit @0x1080, IAT[0] GetStdHandle"),
]

SYMBOLES = {
    # blocs
    "WRITE": 0x1040, "EXIT": 0x1080,
    "MEMCPY": 0x1100, "MEMCMP": 0x1180, "STRLEN": 0x1200, "ITOA": 0x1280,
    "ZONE_ALLOC": 0x1300, "ZONE_RESET": 0x1380, "MEMSET": 0x13C0,
    "AUTOTEST": 0x1800,
    # IAT
    "IAT_GSH": L.IAT_SLOTS["GetStdHandle"],
    "IAT_WF": L.IAT_SLOTS["WriteFile"],
    "IAT_EP": L.IAT_SLOTS["ExitProcess"],
    # données .rdata
    "S_SA": L.R_SA, "S_SB": L.R_SB, "S_SC": L.R_SC, "S_SD": L.R_SD,
    "MOTIF16": L.R_MOTIF16, "SENT16": L.R_SENT16, "MOTIF33": L.R_MOTIF33,
    "ZERO16": L.R_ZERO16, "FF33": L.R_FF33,
    "S_VIDE": L.R_S_VIDE, "S_TRIADE": L.R_S_TRIADE, "S_33": L.R_S_33,
    "I0": L.R_I0, "IMAX": L.R_IMAX, "I123": L.R_I123, "I7": L.R_I7,
    "PREFIXE": L.R_PREFIXE, "SLASH": L.R_SLASH, "OK": L.R_OK, "KO": L.R_KO,
    # données .data
    "CURSEUR": L.R_CURSEUR, "ARENE": L.ARENE_BASE,
}

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_RIP_SYMBOLE = re.compile(r"^(.*?\[rip\s*\+\s*)(\w+)(\s*\].*)$")


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


def taille_ligne(ks: Ks, ligne: str, adresse: int, etiquettes: dict, base: int) -> int:
    enc, _ = ks.asm(substituer(ligne, adresse, etiquettes, base, taille=True), adresse)
    if not enc:
        raise ErreurAuteur(f"ligne inassemblable (calcul de taille) : {ligne!r}")
    return len(enc)


def substituer(ligne: str, adresse: int, etiquettes: dict, base: int, taille: int = 0) -> str:
    """Remplace étiquettes et symboles par leurs formes explicites."""
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
        if nom not in SYMBOLES:
            raise ErreurAuteur(f"symbole de bloc inconnu : {nom}")
        return f"{mnemo} 0x{SYMBOLES[nom]:x}"
    m = RE_RIP_SYMBOLE.match(ligne)
    if m:
        avant, nom, apres = m.groups()
        if nom not in SYMBOLES:
            raise ErreurAuteur(f"symbole de données inconnu : {nom}")
        # taille identique quel que soit le déplacement (toujours disp32) :
        # un point d'ancrage neutre suffit au calcul de taille.
        return f"{avant}0x0{apres}" if taille else ligne
    return ligne


def resoudre_rip(ligne: str, adresse: int, taille: int) -> str:
    """Calcule le déplacement RIP réel : cible - (adresse + taille)."""
    m = RE_RIP_SYMBOLE.match(ligne)
    if not m:
        return ligne
    avant, nom, apres = m.groups()
    if nom not in SYMBOLES:
        raise ErreurAuteur(f"symbole de données inconnu : {nom}")
    cible = SYMBOLES[nom]
    disp = cible - (adresse + taille)
    if disp >= 0:
        return f"{avant}0x{disp:x}{apres}"
    base = avant[:avant.rindex("+")].rstrip()
    return f"{base} - 0x{-disp:x}{apres}"


def resoudre_bloc(ks: Ks, fichier: str, bid: str, spec: str, rva: int, slot: int, deps: str):
    chemin = os.path.join(BROUILLONS, fichier + ".asm")
    instructions, etiquettes_lignes = lire_brouillon(chemin)
    if not instructions:
        raise ErreurAuteur(f"{fichier} : brouillon vide")

    # Point fixe : les tailles dépendent des distances de saut, les distances
    # des tailles. Départ prudent : étiquettes provisionnelles éloignées.
    etiquettes = {nom: rva + 0x800 for nom, _ in etiquettes_lignes}
    for _ in range(4):
        tailles, adresse = [], rva
        for ligne, _ in instructions:
            t = taille_ligne(ks, ligne, adresse, etiquettes, rva)
            tailles.append(t)
            adresse += t
        nouvelles = {}
        for nom, index in etiquettes_lignes:
            nouvelles[nom] = rva + sum(tailles[:index])
        if nouvelles == etiquettes:
            break
        etiquettes = nouvelles
    else:
        raise ErreurAuteur(f"{fichier} : pas de point fixe en 4 passes")

    # Génération : adresses définitives + déplacements RIP réels
    lignes_sortie, adresse, calculs = [], rva, []
    for ligne, numero in instructions:
        taille = tailles[len(lignes_sortie)]
        explicite = resoudre_rip(
            substituer(ligne, adresse, etiquettes, rva), adresse, taille)
        lignes_sortie.append((explicite, adresse, taille, numero))
        calcurs_rip = RE_RIP_SYMBOLE.match(explicite)
        adresse += taille
    total = adresse - rva
    if total > slot:
        raise ErreurAuteur(f"{fichier} : {total} o > slot {slot:#x} (D8)")
    if slot - total < 16:
        raise ErreurAuteur(f"{fichier} : padding {slot - total} < 16 (D8)")

    entete = [
        f"; {fichier} · bloc {NOMS_COURTS.get(fichier, fichier)} · spec {spec} · bloc carte {bid}",
        f"; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x{rva:x}, taille {slot} octets",
        f"; Dépendances : {deps}",
        f"; Notation explicite générée par outils/auteur.py depuis brouillons/{fichier}.asm",
        f"; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)",
        f"; Code : {total} o · padding : {slot - total} o (NOP)",
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
                cible = adr + t + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
                entete.append(f";   0x{adr:x} + 0x{t:x} {m.group(1)} {m.group(2)} = 0x{cible:x}")

    chemin_sortie = os.path.join(SORTIE, fichier + ".asm")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for ligne_e, *_ in lignes_sortie:
            f.write(ligne_e + "\n")
    return total, len(instructions), len(etiquettes_lignes)


NOMS_COURTS = {
    "libc-01-memcpy": "copie mémoire (memcpy)",
    "libc-02-memcmp": "comparaison normalisée (memcmp)",
    "libc-03-strlen": "longueur de chaîne (strlen)",
    "libc-04-itoa": "conversion décimale u32 (itoa)",
    "libc-05-zone-alloc": "allocateur par zone",
    "libc-06-zone-reset": "réinitialisation de zone",
    "libc-07-memset": "remplissage mémoire (memset)",
    "libc-08-autotest": "auto-test de la mini-libc (point d'entrée)",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes (jalon M1) ===")
    for fichier, bid, spec, rva, slot, deps in BLOCS:
        chemin = os.path.join(BROUILLONS, fichier + ".asm")
        if not os.path.exists(chemin):
            print(f"[absent] {fichier} : brouillon absent, ignoré")
            continue
        total, n, e = resoudre_bloc(ks, fichier, bid, spec, rva, slot, deps)
        print(f"[ok] {fichier} ({bid}) : {total} o, {n} instructions, "
              f"{e} étiquettes, {slot - total} o de padding")
    if not verifier_seulement:
        print("Notation explicite écrite dans notation/*.asm")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifier-seulement" in sys.argv))
