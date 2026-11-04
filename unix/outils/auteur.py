#!/usr/bin/env python3
"""auteur.py — Outil d'arithmétique d'adresses de la lignée du jalon M6 (unix/, D149).

Génère la notation explicite (une instruction par ligne, sauts en adresses
absolues, déplacements RIP calculés et documentés) depuis les brouillons
étiquetés de l'auteur. Keystone assemble, rien d'autre : les labels .nom et
les symboles @nom sont résolus par itération au point fixe — les tailles
d'encodage keystone décident seules de la stabilité (initialisation pire-cas
rel32, convergence monotonne, garde-fou 12 itérations).

Brouillon (entrée) :
  @nom = 0xVALEUR        symbole (RVA ou taille — build_m6.py vérifie la
                         concordance avec layout.py) ;
  .label:                étiquette locale (adresse de l'instruction suivante) ;
  jl .label              saut résolu en adresse absolue ;
  lea rax, [rip + @nom]  déplacement RIP calculé (cible = adresse + taille
                         + disp) ;
  mov edx, @nom          immédiat substitué ;
  call .emit             sous-programme local : l'étiquette devient adresse
                         (les cibles d'appel locaux sont déclarées en I1).

Notation (sortie) : texte exact ré-assemblable, une instruction par ligne,
en-tête documenté au style de la lignée (étiquettes résolues, arithmétique
RIP, code/padding).

Usage : python3 outils/auteur.py            # régénère les 4 notations
        python3 outils/auteur.py --verifier # round-trip de chaque notation
"""

from __future__ import annotations

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
UNIX = os.path.dirname(ICI)
sys.path.insert(0, UNIX)
import layout as L  # noqa: E402

import capstone  # noqa: E402
from keystone import KS_ARCH_X86, KS_MODE_64, Ks  # noqa: E402

BROUILLONS = os.path.join(UNIX, "notation", "brouillons")
NOTATION = os.path.join(UNIX, "notation")


class EchecAuteur(Exception):
    """Tout échec de résolution, d'assemblage ou de round-trip."""


def charger_brouillon(chemin: str):
    """Retourne (symboles @, lignes [(kind, contenu)]) — kind: label|instr."""
    symboles: dict[str, int] = {}
    lignes: list[tuple[str, str]] = []
    with open(chemin, encoding="utf-8") as f:
        brut = [l.strip() for l in f.read().splitlines()]
    for l in brut:
        if not l or l.startswith(";"):
            continue
        m = re.match(r"@(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)$", l)
        if m:
            symboles[m.group(1)] = int(m.group(2), 0)
            continue
        if l.startswith(".") and l.endswith(":"):
            lignes.append(("label", l[1:-1]))   # sans le point (clé = nom nu)
            continue
        lignes.append(("instr", l))
    return symboles, lignes


_RE_LABEL = re.compile(r"(?<![\w.])\.(\w+)")
_RE_RIP = re.compile(r"\[rip\s*([+-])\s*@(\w+)\]")
_RE_IMM = re.compile(r"(?<![\w@])@(\w+)")


def _substituer(texte: str, adresses: dict[str, int], symboles: dict[str, int],
                adresse: int, taille_connue: int | None, ks: Ks) -> tuple[str, int]:
    """Substitue labels/symboles dans une ligne. Retourne (texte, taille).

    taille_connue : taille d'encodage déjà établie pour le rip-relatif
    (l'encodage rip est toujours disp32 : la taille est stable).
    """
    def repl_label(m: re.Match) -> str:
        nom = m.group(1)
        if nom not in adresses:
            raise EchecAuteur(f"label inconnu : .{nom}")
        return hex(adresses[nom])

    t = _RE_LABEL.sub(repl_label, texte)

    def repl_rip(m: re.Match) -> str:
        nom = m.group(2)
        if nom not in symboles:
            raise EchecAuteur(f"symbole inconnu : @{nom}")
        if taille_connue is None:
            return "[rip + 0x0]"                    # factice : mesure de taille
        cible = symboles[nom]                        # convention : + cible
        disp = cible - (adresse + taille_connue)
        return f"[rip + {disp}]" if disp >= 0 else f"[rip - {-disp}]"

    t = _RE_RIP.sub(repl_rip, t)

    def repl_imm(m: re.Match) -> str:
        nom = m.group(1)
        if nom not in symboles:
            raise EchecAuteur(f"symbole inconnu : @{nom}")
        return hex(symboles[nom])

    t = _RE_IMM.sub(repl_imm, t)
    enc, _ = ks.asm(t, adresse)
    if not enc:
        raise EchecAuteur(f"inassemblable : {texte!r} (substitué : {t!r})")
    return t, len(enc)


def resoudre(ks: Ks, rva: int, symboles: dict[str, int], lignes: list[tuple[str, str]]):
    """Point fixe : adresses de labels stables. Retourne les lignes résolues.

    Chaque ligne résolue : dict(ligne, texte, adresse, taille, octets).
    """
    labels = [c for k, c in lignes if k == "label"]
    adresses: dict[str, int] = {nom: rva + 0x100000 for nom in labels}  # pire-cas
    for _ in range(12):
        pos = rva
        nouvelles: dict[str, int] = {}
        resolues: list[dict] = []
        for kind, contenu in lignes:
            if kind == "label":
                nouvelles[contenu] = pos
                continue
            t1, taille = _substituer(contenu, adresses, symboles, pos, None, ks)
            t2, _ = _substituer(contenu, adresses, symboles, pos, taille, ks)
            enc, _ = ks.asm(t2, pos)
            resolues.append({"ligne": contenu, "texte": t2, "adresse": pos,
                             "taille": taille, "octets": bytes(enc)})
            pos += taille
        if nouvelles == adresses:
            return resolues, adresses
        adresses = nouvelles
    raise EchecAuteur("point fixe non atteint (12 itérations — oscillation ?)")


def generer(bid: str, spec: str, fichier: str, rva: int, slot: int,
            ks: Ks, cs: capstone.Cs) -> dict:
    """Régénère notation/<fichier>.asm depuis brouillons/<fichier>.asm."""
    chemin_brouillon = os.path.join(BROUILLONS, fichier + ".asm")
    if not os.path.exists(chemin_brouillon):
        raise EchecAuteur(f"brouillon introuvable : {chemin_brouillon}")
    symboles, lignes = charger_brouillon(chemin_brouillon)
    resolues, adresses = resoudre(ks, rva, symboles, lignes)

    code = sum(r["taille"] for r in resolues)
    if code > slot:
        raise EchecAuteur(f"{fichier} : {code} o > slot {slot:#x} (D8)")
    if slot - code < 16:
        raise EchecAuteur(f"{fichier} : padding {slot - code} < 16 (D8)")

    # Round-trip intégré : chaque texte explicite ré-assemble en ses octets,
    # et le désassemblage capstone rend un texte qui ré-assemble en les MÊMES
    # octets — le rendu capstone est ALORS ADOPTÉ comme texte canonique de la
    # notation (le brouillon peut écrire 60, la notation porte 0x3c — le
    # WYSIWYG est l'identité OCTETS, la graphie est canonique capstone).
    for r in resolues:
        enc, _ = ks.asm(r["texte"], r["adresse"])
        if bytes(enc) != r["octets"]:
            raise EchecAuteur(f"{fichier} @ {r['adresse']:#x} : ré-assemblage != octets")
        insns = list(cs.disasm(r["octets"], r["adresse"]))
        if len(insns) != 1:
            raise EchecAuteur(f"{fichier} @ {r['adresse']:#x} : pas une instruction")
        texte_cs = f"{insns[0].mnemonic} {insns[0].op_str}".strip()
        enc_cs, _ = ks.asm(texte_cs, r["adresse"])
        if bytes(enc_cs) != r["octets"]:
            raise EchecAuteur(
                f"{fichier} @ {r['adresse']:#x} : le rendu capstone diverge en octets\n"
                f"  auteur   : {r['texte']}\n  capstone : {texte_cs}")
        if texte_cs != r["texte"]:
            r["texte"] = texte_cs          # canonisation (graphie capstone)

    # Déplacements RIP : extraits du BROUILLON (le texte substitué ne porte
    # plus les @nom) — correspondance par ordre des lignes d'instructions.
    displacements = []
    instrs_brouillon = [c for k, c in lignes if k == "instr"]
    for r, source in zip(resolues, instrs_brouillon):
        for m in _RE_RIP.finditer(source):
            nom = m.group(2)
            cible = symboles[nom]
            disp = cible - (r["adresse"] + r["taille"])
            displacements.append((r["adresse"], r["taille"], disp, cible, nom))

    entete = [
        f"; {fichier} · bloc {NOM(fichier)} · spec {spec} · bloc carte {bid}",
        f"; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA {rva:#x}, taille {slot} octets",
        "; Notation explicite générée par outils/auteur.py depuis "
        f"brouillons/{fichier}.asm",
        "; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)",
        f"; Code : {code} o · padding : {slot - code} o (NOP)",
    ]
    if adresses:
        etiquettes = ", ".join(f".{n}={adresses[n]:#x}" for n in sorted(adresses))
        entete.append(f"; Étiquettes résolues : {etiquettes}")
    if displacements:
        entete.append("; Déplacements RIP (cible = adresse + taille + disp) :")
        for adresse, taille, disp, cible, nom in displacements:
            entete.append(f";   {adresse:#x} + {taille:#x} {'+' if disp >= 0 else '-'} "
                          f"{abs(disp):#x} = {cible:#x} (@{nom})")
    if symboles:
        ents = ", ".join(f"@{n}={symboles[n]:#x}" for n in sorted(symboles))
        entete.append(f"; Symboles (vérifiés par build_m6.py contre layout.py) : {ents}")

    chemin_sortie = os.path.join(NOTATION, fichier + ".asm")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for r in resolues:
            f.write(r["texte"] + "\n")
    return {"code": code, "padding": slot - code, "instructions": len(resolues),
            "symboles": symboles, "etiquettes": adresses}


def NOM(fichier: str) -> str:
    """su-02-hex64 -> « formatage hexadécimal u64 » (rôle I)."""
    return {
        "su-01-ecrire": "écriture par appel système",
        "su-02-hex64": "formatage hexadécimal u64",
        "su-03-verdict": "verdict d'erreur syscall",
        "su-04-principal": "orchestration sonde",
    }.get(fichier, fichier)


def main() -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs.detail = False
    verifier = "--verifier" in sys.argv
    total_instr = 0
    for bid, spec, fichier, rva, slot in L.BLOCS_SU:
        r = generer(bid, spec, fichier, rva, slot, ks, cs)
        total_instr += r["instructions"]
        print(f"[auteur] {fichier} : {r['instructions']} instr, {r['code']} o "
              f"(padding {r['padding']}) -> notation/{fichier}.asm")
    print(f"[auteur] 4 blocs, {total_instr} instructions — notation régénérée")
    return 0


if __name__ == "__main__":
    sys.exit(main())
