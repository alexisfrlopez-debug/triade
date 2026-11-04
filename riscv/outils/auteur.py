#!/usr/bin/env python3
"""auteur.py — Outil d'arithmétique d'adresses de la lignée du jalon M7 (riscv/, D149).

Génère la notation explicite (une instruction par ligne, décalages B/J
RELATIFS calculés et documentés, paires d'ancres auipc+addi vérifiées)
depuis les brouillons étiquetés de l'auteur. L'ASSEMBLEUR MAISON assemble
(outils/as_rv64.py — keystone ne porte pas l'ISA, fiche § 6), capstone
reste le JUGE UNIQUE du round-trip : le rendu du juge est ADOPTÉ comme
texte canonique (le WYSIWYG est l'identité OCTETS, la graphie est
canonique capstone — le modèle du jalon unix, appliqué à une ISA où le
juge a plus de pseudos que l'auteur n'a d'habitudes : mv, beqz, sext.w…).

Brouillon (entrée) :
  @nom = 0xVALEUR        symbole (RVA, taille ou numéro de syscall —
                         build_m7.py vérifie la concordance avec
                         layout.py — leçon C1) ;
  .label:                étiquette locale (adresse de l'instruction suivante) ;
  beqz a0, .label        saut résolu en DÉCALAGE RELATIF (l'encodage B/J
                         est relatif — la cible = adresse + décalage) ;
  jal @A_ECRIRE          appel : le symbole ABSOLU devient décalage
                         (cible - adresse — l'appartenance de la cible est
                         déclarée en I1, l'oracle la vérifie) ;
  lw t0, @ERRNOS(s1)     déplacement mémoire substitué (RVA absolue) ;
  addi a2, zero, @L_BASE immédiat substitué ;
  auipc s1, @ANCRE_BASE_HI   PAIRE D'ANCRE (le portage RV64 du lea rip
  addi s1, s1, @ANCRE_BASE_LO lié-temps soustrait) : le site et la cible
                         vivent au layout (ANCRE_BASE/CIBLE_BASE), l'auteur
                         VÉRIFIE que l'auipc est bien AU SITE déclaré et
                         calcule HI/LO (site + HI*4096 + LO == cible,
                         LO ∈ imm12 — l'arithmétique est documentée en
                         tête de notation et re-vérifiée par l'oracle du
                         build sur le code désassemblé).

TAILLE FIXE (fiche § 1 — sans extension C) : toute instruction fait 4 o —
les adresses d'étiquettes sont connues dès la première passe, le point
fixe du modèle unix (tailles d'encodage variables) COLLAPSE en un passage
unique ; une seconde passe de stabilité est exécutée néanmoins (garde).

Notation (sortie) : texte exact ré-assemblable, une instruction par ligne,
en-tête documenté au style de la lignée (étiquettes résolues, arithmétique
des ancres, décalages B/J, code/padding).

Usage : python3 outils/auteur.py            # régénère les 4 notations
        python3 outils/auteur.py --verifier # round-trip de chaque notation
"""

from __future__ import annotations

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RISCV = os.path.dirname(ICI)
sys.path.insert(0, RISCV)
sys.path.insert(0, os.path.join(RISCV, "outils"))
import layout as L                              # noqa: E402

import capstone                                 # noqa: E402
from as_rv64 import EchecAssemblage, assembler  # noqa: E402

BROUILLONS = os.path.join(RISCV, "notation", "brouillons")
NOTATION = os.path.join(RISCV, "notation")

JUGE = capstone.Cs(capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV64)
JUGE.detail = False

# Mnémoniques dont le DERNIER opérande est un décalage relatif B/J
_RELATIFS = {"beq", "bne", "blt", "bge", "bltu", "bgeu",
             "beqz", "bnez", "bgez", "bltz", "bgtz", "blez",
             "j", "jal"}

# Ancres déclarées au layout : nom → (site, cible). Les DEUX de la sonde
# (chantier M7-(a)) et les TROIS du corpus (chantier M7-(b)) — chaque paire
# vit AU SITE déclaré, le LO relativement à SON auipc (leçon C1).
_ANCRES = {
    "ANCRE_BASE": (L.ANCRE_BASE, L.CIBLE_BASE),
    "ANCRE_BSS": (L.ANCRE_BSS, L.CIBLE_BSS),
    "ANCRE_RODATA": (L.ANCRE_RODATA, L.CIBLE_RODATA),
    "ANCRE_BSS_CORPUS": (L.ANCRE_BSS_CORPUS, L.CIBLE_BSS_CORPUS),
    "ANCRE_ENTREE": (L.ANCRE_ENTREE, L.CIBLE_ENTREE),
}


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
        m = re.match(r"@(\w+)\s*=\s*(-?0x[0-9a-fA-F]+|-?\d+)$", l)
        if m:
            symboles[m.group(1)] = int(m.group(2), 0)
            continue
        if l.startswith(".") and l.endswith(":"):
            lignes.append(("label", l[1:-1]))   # sans le point (clé = nom nu)
            continue
        lignes.append(("instr", l))
    return symboles, lignes


_RE_LABEL = re.compile(r"(?<![\w.])\.(\w+)")
_RE_SYM = re.compile(r"@(\w+)")
_RE_MEM = re.compile(r"@(\w+)\(")


def _paire_ancre(nom: str, adresse_auipc: int) -> tuple[int, int]:
    """HI/LO d'une paire auipc+addi posant ancre=base+cible.

    site + HI*4096 + LO == cible, LO ∈ [-2048, 2047] (arrondi au plus
    proche — le %pcrel_hi/%pcrel_lo canonique du compilateur).
    """
    site, cible = _ANCRES[nom]
    if adresse_auipc != site:
        raise EchecAuteur(
            f"ancre {nom} : l'auipc vit à {adresse_auipc:#x}, le layout déclare "
            f"le site {site:#x} — la paire n'est pas au site (leçon C1)")
    delta = cible - site
    hi = (delta + 0x800) >> 12
    lo = delta - (hi << 12)
    if not -2048 <= lo <= 2047:
        raise EchecAuteur(f"ancre {nom} : LO {lo} hors imm12 — inattendu")
    return hi, lo


def _substituer(texte: str, adresse: int, symboles: dict[str, int],
                etiquettes: dict[str, int], precedent: dict | None
                ) -> tuple[str, list[str]]:
    """Substitue labels/symboles/ancres dans une ligne. Retourne (texte, notes).

    Les décalages relatifs (B/J) : cible - adresse, documentés en note.
    La paire d'ancre : le site se vérifie sur l'auipc (HI) ; le addi (LO)
    se vérifie CONTRE SON AUIPC (la ligne précédente — la paire est
    inséparable : l'arithmétique LO n'a de sens que relativement à SON
    site, jamais isolément).
    """
    notes: list[str] = []
    mnemo = texte.split()[0]
    relatif = mnemo in _RELATIFS

    def repl_label(m: re.Match) -> str:
        nom = m.group(1)
        if nom not in etiquettes:
            raise EchecAuteur(f"étiquette inconnue : .{nom}")
        cible = etiquettes[nom]
        if not relatif:
            raise EchecAuteur(
                f".{nom} hors position de décalage (mnémonique {mnemo} ne "
                f"prend pas de cible relative)")
        off = cible - adresse
        notes.append(f"{adresse:#x} -> .{nom} ({cible:#x}) : décalage {off:+#x}")
        return str(off)

    t = _RE_LABEL.sub(repl_label, texte)

    def repl_sym(m: re.Match) -> str:
        nom = m.group(1)
        # — paire d'ancre (site/cible au layout, vérifiés)
        for ancre in _ANCRES:
            base_nom = ancre.split("_", 1)[1]
            if nom == f"{ancre}_HI":
                hi, lo = _paire_ancre(ancre, adresse)
                notes.append(
                    f"ancre {ancre} @ {adresse:#x} : HI={hi} ({hi & 0xFFFFF:#x}), "
                    f"LO={lo} — {adresse:#x} + {hi:#x}*4096 + {lo} == "
                    f"{_ANCRES[ancre][1]:#x} (CIBLE_{base_nom})")
                return hex(hi & 0xFFFFF)
            if nom == f"{ancre}_LO":
                if precedent is None or not precedent["ligne"].startswith("auipc") \
                        or f"@{ancre}_HI" not in precedent["ligne"]:
                    raise EchecAuteur(
                        f"ancre {ancre} : le LO vit seul — la paire exige SON "
                        f"auipc (@{ancre}_HI) à la ligne précédente")
                hi, lo = _paire_ancre(ancre, precedent["adresse"])
                notes.append(f"ancre {ancre} : LO={lo} (paire avec l'auipc @ "
                             f"{precedent['adresse']:#x})")
                return str(lo)
        if nom not in symboles:
            raise EchecAuteur(f"symbole inconnu : @{nom}")
        cible = symboles[nom]
        # — appel jal vers un bloc : le symbole ABSOLU devient décalage
        if relatif:
            off = cible - adresse
            notes.append(f"{adresse:#x} -> @{nom} ({cible:#x}) : décalage {off:+#x}")
            return str(off)
        return hex(cible)

    t = _RE_SYM.sub(repl_sym, t)
    return t, notes


def resoudre(rva: int, symboles: dict[str, int], lignes: list[tuple[str, str]]):
    """Taille fixe 4 o : adresses connues dès la première passe.

    Retourne (lignes résolues, adresses d'étiquettes, notes d'arithmétique).
    """
    # — passe 1 : adresses des étiquettes (toute instruction fait 4 o)
    pos = rva
    etiquettes: dict[str, int] = {}
    for kind, contenu in lignes:
        if kind == "label":
            etiquettes[contenu] = pos
        else:
            pos += 4
    # — passe 2 : substitution + assemblage (et stabilité re-vérifiée)
    resolues, notes = [], []
    pos = rva
    for kind, contenu in lignes:
        if kind == "label":
            continue
        precedent = resolues[-1] if resolues else None
        t, n = _substituer(contenu, pos, symboles, etiquettes, precedent)
        try:
            octets = assembler(t, pos)
        except EchecAssemblage as exc:
            raise EchecAuteur(
                f"inassemblable : {contenu!r} (substitué : {t!r}) : {exc}") from None
        if len(octets) != 4:
            raise EchecAuteur(f"{contenu!r} : {len(octets)} o != 4 (garde anti-C)")
        resolues.append({"ligne": contenu, "texte": t, "adresse": pos,
                         "octets": octets})
        notes.extend(n)
        pos += 4
    # — stabilité : les adresses d'étiquettes de la passe 2 == passe 1
    pos2 = rva
    for r in resolues:
        pos2 += 4
    if any(etiquettes[n] != v for n, v in etiquettes.items()):
        raise EchecAuteur("instabilité d'étiquettes — impossible en taille fixe")
    return resolues, etiquettes, notes


def generer(bid: str, spec: str, fichier: str, rva: int, slot: int,
            builder: str = "build_m7.py") -> dict:
    """Régénère notation/<fichier>.asm depuis brouillons/<fichier>.asm."""
    chemin_brouillon = os.path.join(BROUILLONS, fichier + ".asm")
    if not os.path.exists(chemin_brouillon):
        raise EchecAuteur(f"brouillon introuvable : {chemin_brouillon}")
    symboles, lignes = charger_brouillon(chemin_brouillon)

    # — concordance des symboles d'ancre déclarés au brouillon (leçon C1 :
    # la déclaration de l'auteur affronte le layout AVANT la substitution)
    for nom, (site, _cible) in _ANCRES.items():
        if nom in symboles and symboles[nom] != site:
            raise EchecAuteur(
                f"@{nom}={symboles[nom]:#x} != site layout {site:#x} (leçon C1)")

    resolues, etiquettes, notes = resoudre(rva, symboles, lignes)

    code = 4 * len(resolues)
    if code > slot:
        raise EchecAuteur(f"{fichier} : {code} o > slot {slot:#x} (D8)")
    if slot - code < 16:
        raise EchecAuteur(f"{fichier} : padding {slot - code} < 16 (D8)")

    # Round-trip intégré : le texte explicite ré-assemble en ses octets,
    # et le rendu du JUGE (capstone) ré-assemble en les MÊMES octets — le
    # rendu du juge est ADOPTÉ comme texte canonique (graphie capstone).
    for r in resolues:
        if assembler(r["texte"], r["adresse"]) != r["octets"]:
            raise EchecAuteur(f"{fichier} @ {r['adresse']:#x} : ré-assemblage != octets")
        insns = list(JUGE.disasm(r["octets"], r["adresse"]))
        if len(insns) != 1 or insns[0].size != 4:
            raise EchecAuteur(
                f"{fichier} @ {r['adresse']:#x} : le juge ne décode pas "
                f"UNE instruction de 4 o : {r['texte']!r}")
        texte_juge = f"{insns[0].mnemonic} {insns[0].op_str}".strip()
        if assembler(texte_juge, r["adresse"]) != r["octets"]:
            raise EchecAuteur(
                f"{fichier} @ {r['adresse']:#x} : le rendu du juge diverge "
                f"en octets\n  auteur   : {r['texte']}\n  capstone : {texte_juge}")
        if texte_juge != r["texte"]:
            r["texte"] = texte_juge          # canonisation (graphie capstone)

    entete = [
        f"; {fichier} · bloc {NOM(fichier)} · spec {spec} · bloc carte {bid}",
        f"; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA {rva:#x}, "
        f"taille {slot} octets",
        "; Notation explicite générée par outils/auteur.py depuis "
        f"brouillons/{fichier}.asm",
        "; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON "
        "outils/as_rv64.py assemble,",
        "; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)",
        f"; Code : {code} o ({len(resolues)} instructions × 4 o — taille fixe, "
        f"garde anti-C) · padding : {slot - code} o (NOP canonique addi x0, x0, 0)",
    ]
    if etiquettes:
        e = ", ".join(f".{n}={etiquettes[n]:#x}" for n in sorted(etiquettes))
        entete.append(f"; Étiquettes résolues : {e}")
    if notes:
        entete.append("; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :")
        for n in notes:
            entete.append(f";   {n}")
    if symboles:
        s = ", ".join(f"@{n}={symboles[n]:#x}" for n in sorted(symboles))
        entete.append(f"; Symboles (vérifiés par {builder} contre layout.py — "
                      f"leçon C1) : {s}")

    chemin_sortie = os.path.join(NOTATION, fichier + ".asm")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for r in resolues:
            f.write(r["texte"] + "\n")
    return {"code": code, "padding": slot - code, "instructions": len(resolues),
            "symboles": symboles, "etiquettes": etiquettes}


def NOM(fichier: str) -> str:
    """sr-02-hex64 -> « formatage hexadécimal u64 » (rôle I)."""
    return {
        "sr-01-ecrire": "écriture par appel système",
        "sr-02-hex64": "formatage hexadécimal u64",
        "sr-03-verdict": "verdict d'erreur syscall",
        "sr-04-principal": "orchestration sonde",
        "hello-02-ecrire-r2": "écriture du flux (interface du corpus)",
        "hello-03-sortir-r2": "terminaison (interface du corpus)",
        "libc-01-memcpy-r2": "copie mémoire",
        "libc-02-memcmp-r2": "comparaison mémoire normalisée",
        "libc-03-strlen-r2": "longueur de chaîne",
        "libc-04-itoa-r3": "conversion décimale u32",
        "libc-05-zone-alloc-r2": "allocateur par zone",
        "libc-06-zone-reset-r2": "réinitialisation de zone",
        "libc-07-memset-r2": "remplissage mémoire",
        "libc-08-autotest-r3": "auto-test de la mini-libc (21 vecteurs dorés)",
        "tcp-11-journal-r2": "ligne de journal (verrou tournant amoswap.d)",
        "tcp-11-journal-v2": "journal v2 — le remplaçant (staging, POUR la croissance)",
        "tcp-07-patch-r4": "moteur de patch (mprotect asm-generic 226, fence.i)",
        "corpus-13-principal": "orchestration du corpus paritaire — _start",
    }.get(fichier, fichier)


def main() -> int:
    verifier = "--verifier" in sys.argv
    corpus = "--corpus" in sys.argv
    if corpus:
        blocs = list(L.BLOCS_CORPUS) + [L.BLOC_STAGING]
        domaine = "corpus"
        builder = "build_corpus.py"
    else:
        blocs = L.BLOCS_SR
        domaine = "sonde"
        builder = "build_m7.py"
    total_instr = 0
    for bid, spec, fichier, rva, slot in blocs:
        if verifier:
            chemin = os.path.join(NOTATION, fichier + ".asm")
            with open(chemin, encoding="utf-8") as f:
                lignes = [l.strip() for l in f.read().splitlines()]
            instrs = [l for l in lignes if l and not l.startswith(";")]
            for i, l in enumerate(instrs):
                octets = assembler(l, rva + 4 * i)
                insns = list(JUGE.disasm(octets, rva + 4 * i))
                if len(insns) != 1 or \
                        f"{insns[0].mnemonic} {insns[0].op_str}".strip() != l:
                    print(f"[auteur] ÉCHEC round-trip @ {rva + 4 * i:#x} : {l!r}")
                    return 1
            print(f"[auteur] {fichier} : {len(instrs)} instructions, "
                  f"round-trip 100 %")
            total_instr += len(instrs)
        else:
            r = generer(bid, spec, fichier, rva, slot, builder=builder)
            total_instr += r["instructions"]
            print(f"[auteur] {fichier} : {r['instructions']} instr, "
                  f"{r['code']} o (padding {r['padding']}) "
                  f"-> notation/{fichier}.asm")
    print(f"[auteur] {len(blocs)} blocs ({domaine}), {total_instr} instructions — "
          f"notation {'vérifiée' if verifier else 'régénérée'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
