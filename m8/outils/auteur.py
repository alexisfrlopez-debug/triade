#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du jalon M8 (0.9.0-dev.1) : résolution des étiquettes.

Même discipline qu'en M1/M2/M3/M4/M5 (aucun compilateur entre l'intention et
les octets : keystone assemble, rien d'autre) — cet outil fait l'arithmétique
d'adresses de l'auteur : étiquettes locales -> adresses absolues des sauts,
symboles de blocs -> cibles d'appels directes, symboles de données ->
déplacements RIP calculés une fois pour toutes depuis le plan d'adressage M8
(m8/layout.py, source unique — lui-même charge l'héritage m5 par chemin
absolu, leçon D158 : memcmp libc-02 est CITÉ depuis la table scellée
BLOCS_LIBC_EMBARQUES, jamais un littéral).

Entrée : notation/brouillons/*.asm. Sortie : notation/*.asm — notation
explicite WYSIWYG, seule lue par le futur build_m8.py (round-trip R5 sur la
sortie ; le harnais du chantier (b) le joue déjà).

Usage : python3 outils/auteur.py [--verifier-seulement]
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import layout as L  # noqa: E402  # le plan M8 (la source unique)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "..", "notation", "brouillons")
SORTIE = os.path.join(ICI, "..", "notation")

# (fichier brouillon, id bloc, spec, dépendances) — rva/slot dérivés du plan
# d'adressage (layout.py, source unique de vérité ; l'ARRÊT DÉFINITIF des
# slots est celui du plan — la mesure auteur, D161).
_FICHIERS = {
    "g90001": ("sys-01-emetteur", "sys-01:R1",
               "bloc feuille ; le site syscall est l'unique interaction "
               "(aucun IAT, aucun appel)"),
    "g90002": ("sys-02-resolveur", "sys-02:R1",
               "memcmp libc-02 (b20002, l'héritage scellé M1 — le seul appel "
               "direct DÉCLARÉ)"),
    "g90003": ("sys-03-ecriture", "sys-03:R1",
               "sys-02 (la résolution au geste même) PUIS sys-01 (l'émission) "
               "— l'ordre est le contrat (I3) ; les fixtures .rdata NOM/LIGNE "
               "cités par déplacement (I4)"),
    # LE SOCLE SOCKET (chantier M9-(d), l'ère 1.0.0 du transport) — les
    # TROIS blocs du plan : l'établissement AFD, l'émission, la réception
    "g90004": ("sys-04-transport", "sys-04:R1",
               "sys-02 × 3 PUIS sys-01 × 3 — create PUIS bind PUIS connect, "
               "la séquence MESURÉE mswsock (I6) ; chaque SSN résolu au "
               "geste même (Q3) ; les fixtures .text6 DEVICE/EA/BIND et les "
               "noms de résolution cités par déplacement (I3/T5)"),
    "g90005": ("sys-05-emission", "sys-05:R1",
               "sys-02 PUIS sys-01 (IOCTL_AFD_SEND) — TOTALE ou refus -7 "
               "(Q2) ; AUCUNE copie de la charge (I2) ; le fixture .text6 "
               "NOM_DEVICEIOCTL cité par déplacement (T5)"),
    "g90006": ("sys-06-reception", "sys-06:R1",
               "sys-02 PUIS sys-01 (IOCTL_AFD_RECEIVE bloquant) — LE ZÉRO "
               "EST LA DEMI-FIN -7 (Q2) ; le noyau ÉCRIT chez le kit (I2) ; "
               "AfdFlags 0x20 LA MESURE (l'erratum) ; le fixture .text6 "
               "NOM_DEVICEIOCTL cité par déplacement (T5)"),
}


def blocs_m8() -> list[tuple]:
    out = []
    for bid, (fichier, spec, deps) in _FICHIERS.items():
        rva, slot = L.SLOTS_SYS[bid]
        out.append((fichier, bid, spec, rva, slot, deps))
    return out


BLOCS = blocs_m8()

SYMBOLES = {
    # les blocs du domaine (le plan, source unique)
    "SYS01": L.SYS01_VA,
    "SYS02": L.SYS02_VA,
    "SYS03": L.SYS03_VA,
    "SYS04": L.SYS04_VA,
    "SYS05": L.SYS05_VA,
    "SYS06": L.SYS06_VA,
    # l'héritage scellé : memcmp libc-02 (b20002) — CITÉ depuis la table
    # scellée par m8/layout.py (MEMCMP_VA), jamais un littéral ici
    "MEMCMP": L.MEMCMP_VA,
    # les fixtures .rdata du domaine (le plan, source unique)
    "NOM": L.R_SYS_NOM,
    "LIGNE": L.R_SYS_LIGNE,
    # les fixtures .text6 du SOCLE SOCKET (chantier M9-(d) — le plan,
    # source unique : le device UTF-16LE, le EA déterministe, le bind
    # WILDCARD, les noms de résolution en SPANS sans NUL)
    "DEVICE": L.R_SYS_DEVICE,
    "EA": L.R_SYS_EA,
    "BIND": L.R_SYS_BIND,
    "NOM_CREATEFILE": L.R_SYS_NOM_CREATEFILE,
    "NOM_DEVICEIOCTL": L.R_SYS_NOM_DEVICEIOCTL,
    "NOM_CLOSE": L.R_SYS_NOM_CLOSE,
}

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_LEA_ETIQUETTE = re.compile(r"^(lea\s+\w+), \[\.(\w+)\]$")
RE_RIP_CIBLE = re.compile(r"^(.*?\[rip\s*([+-])\s*)(\w+|\.\w+)(\s*\].*)$")


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
    m = RE_LEA_ETIQUETTE.match(ligne)
    if m:
        if taille:
            return f"{m.group(1)}, [rip + 0x0]"
        return ligne
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
    m = RE_RIP_CIBLE.match(ligne)
    if m and m.group(3) in SYMBOLES:
        avant, signe, nom, apres = m.groups()
        if taille:
            return f"{avant}0x0{apres}"
    return ligne


def resoudre_rip(ligne: str, adresse: int, taille: int, etiquettes: dict) -> str:
    m = RE_LEA_ETIQUETTE.match(ligne)
    if m:
        cible = etiquettes.get(m.group(2))
        if cible is None:
            raise ErreurAuteur(f"étiquette inconnue : .{m.group(2)}")
        disp = cible - (adresse + 7)
        if disp >= 0:
            return f"{m.group(1)}, [rip + 0x{disp:x}]"
        return f"{m.group(1)}, [rip - 0x{-disp:x}]"
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


def resoudre_bloc(ks: Ks, fichier: str, bid: str, spec: str, rva: int, slot: int, deps: str):
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
        f"; {fichier} · bloc {NOMS_COURTS[fichier]} · spec {spec} · bloc carte {bid}",
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
    "sys-01-emetteur": "émetteur syscall (le trombone ABI, six octets)",
    "sys-02-resolveur": "résolveur SSN (l'EAT de ntdll lue, le motif vérifié)",
    "sys-03-ecriture": "écriture directe — la twin de hello-02 par NtWriteFile",
    "sys-04-transport": "le transport établi — le socket natif par AFD, "
                        "sans ws2_32 (create + bind WILDCARD + connect)",
    "sys-05-emission": "l'émission du transport — le send AFD par syscall "
                       "direct, TOTALE ou refus -7",
    "sys-06-reception": "la réception du transport — le recv AFD bloquant, "
                        "le zéro est LA DEMI-FIN -7",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes (jalon M8, domaine sys) ===")
    for fichier, bid, spec, rva, slot, deps in BLOCS:
        chemin = os.path.join(BROUILLONS, fichier + ".asm")
        if not os.path.exists(chemin):
            print(f"[absent] {fichier} : brouillon absent, ignoré (attendu selon la phase)")
            continue
        total, n, e = resoudre_bloc(ks, fichier, bid, spec, rva, slot, deps)
        print(f"[ok] {fichier} ({bid}) : {total} o, {n} instructions, "
              f"{e} étiquettes, {slot - total} o de padding")
    if not verifier_seulement:
        print("Notation explicite écrite dans notation/*.asm")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifier-seulement" in sys.argv))
