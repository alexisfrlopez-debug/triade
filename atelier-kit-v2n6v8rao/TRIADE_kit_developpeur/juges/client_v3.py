#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""client_v3.py — LE CLIENT TPL-ADD-v3 (5nwnwoceo, la vague 13) : le
squelette déterministe + le dictionnaire de domaine versionné (v2
reconduits) + LA GRAMMAIRE PUBLIÉE ET LES VALIDATEURS DE FORMES + LA
BOUCLE DE RÉPARATION À BUDGET PLAFONNÉ.

LES AJOUTS v3 (la lettre du plan gelé) :
  (1) TPL-ADD-GRAMMAIRE-v1 — LA GRAMMAIRE EBNF DU SQUELETTE PUBLIÉE AU
      CLIENT (définition d'étiquette, ligne d'instruction, ligne ID,
      opérandes — registres, immédiats, adresses, IDs), sha256 GRAVÉE au
      matériau et recoupée ; FOURNIE AU MODÈLE DANS LE PROMPT (le levier
      nommé : le modèle connaît la FORME avant d'écrire) ;
  (2) LES VALIDATEURS DE FORMES au client — les quatre interdits nommés
      par OPT-15 (cmp mémoire-à-mémoire proscrit · movzx r64/r64 proscrit
      · désalignement de taille proscrit · symboles en clair proscrits,
      IDs seuls) : refus FORME-INVALIDE AU NOM DE LA CAUSE, AVANT
      l'assemblage (l'erreur nommée à la ligne près) ;
  (3) LA BOUCLE « assemble → refus nommé → réparation ciblée » — le
      budget de reprises PLAFONNÉ À TROIS (consigné par tentative au
      JSONL) ; la réparation porte LE REFUS NOMMÉ et LA LIGNE FAUTIVE —
      jamais la relaxation d'un contrôle ;
  (4) LES QUATRE REFUS v2 RECONDUITS (ID-INCONNU · DICT-DIVERGENT ·
      EXPANSION-DIVERGENTE · HORS-FORMAT) — AUCUN CONTRÔLE RETIRÉ."""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
V2 = REPO / "atelier-ajouter-v2-pgodgk35l"
V1 = REPO / "atelier-gabarits-o5apue194"
sys.path.insert(0, str(V2))
sys.path.insert(0, str(V1))
sys.path.insert(0, str(V1.parent / "atelier-fenetre-mqf258e4l"))

from client_v2 import (construire_dictionnaire, dictionnaire_muté,  # noqa
                       prompt_ajouter_v2, assembler_v2, expandir_ligne)
from client_gabarits import Refus  # noqa

GRAMMAIRE_ID = "TPL-ADD-GRAMMAIRE-v1"

# ===========================================================================
# LA GRAMMAIRE EBNF DU SQUELETTE — publiée, versionnée, sha256 gravée
# ===========================================================================
GRAMMAIRE_EBNF = """\
TPL-ADD-GRAMMAIRE-v1 — LA GRAMMAIRE EBNF DU CORPS (ce que tu émets) :

  corps        = { ligne } ;
  ligne        = definition | instruction ;
  definition   = etiquette_locale ":" ;
  etiquette_locale = lettre_minuscule { lettre_minuscule | chiffre | "_" } ;
  instruction  = mnemonique [ operande [ "," operande ] ] ;
  operande     = registre | immediat | adresse_memoire | ID | etiquette_locale ;
  registre     = "rax" | "rbx" | "rcx" | "rdx" | "rsi" | "rdi" | "rbp"
               | "rsp" | "r8".."r15" | "eax".."r15d" | "al".."r15b"
               | "xmm0".."xmm15" ;
  immediat     = [ "-" ] ( chiffre { chiffre } | "0x" hexa { hexa } ) ;
  adresse_memoire = "[" registre [ ("+" | "-") ( registre [ "*" ("2"|"4"|"8")
                   | immediat ) ] ] [ ("+" | "-") immediat ] "]" ;
  ID           = ( "LBL" | "CST" ) "-" chiffre chiffre chiffre ;
  saut         = ( "jmp" | "je" | "jne" | "jz" | "jnz" | "ja" | "jae" | "jb"
                 | "jbe" | "jg" | "jge" | "jl" | "jle" | "js" | "jns" )
                 ( ID | etiquette_locale ) ;
  appel        = "call" ( ID | immediat ) ;

LES QUATRE INTERDITS DE FORME (le client REFUSE au nom de la cause, à la
ligne près — AVANT l'assemblage) :
  (a) AUCUN « cmp » mémoire-à-mémoire (un opérande mémoire AU PLUS par
      cmp/test — l'autre est un registre ou un immédiat) ;
  (b) AUCUN « movzx » registre-64 vers registre-64 (la source de movzx
      est 32 bits ou moins : « movzx rax, ecx » admis, « movzx rax, rcx »
      REFUSÉ) ;
  (c) AUCUN désalignement de taille entre destination et source d'un mov
      (« mov eax, rbx » REFUSÉ — 32 vers 64 : les tailles s'accordent) ;
  (d) AUCUN symbole en clair (WM_PAINT, ANSI_FIXED_FONT, MB_OK…) : la
      VALEUR NUMÉRIQUE littérale ou l'ID du dictionnaire, RIEN D'AUTRE.
"""

GRAMMAIRE_SHA256 = hashlib.sha256(
    GRAMMAIRE_EBNF.encode("utf-8")).hexdigest()


# ===========================================================================
# LES VALIDATEURS DE FORMES — les quatre interdits, refus au nom de la
# cause, à la ligne près (AVANT l'assemblage)
# ===========================================================================
RE_MEMOIRE = re.compile(r"\[[^\]]+\]")
RE_REG64 = re.compile(r"^\s*r(?:ax|bx|cx|dx|si|di|bp|sp|8|9|1[0-5])\s*$")
RE_REG32 = re.compile(
    r"^\s*(?:e(?:ax|bx|cx|dx|si|di|bp|sp)|r(?:8|9|1[0-5])d)\s*$")
RE_SYMBOLE_CLAIR = re.compile(r"^[A-Z][A-Z0-9_]{3,}$")
RE_IDS_ADMIS = re.compile(r"^(LBL|CST)-[0-9]{3}$")
MNEMOS = ("mov", "cmp", "test", "add", "sub", "and", "or", "xor", "lea",
          "movzx", "jmp", "je", "jne", "jz", "jnz", "ja", "jae", "jb",
          "jbe", "jg", "jge", "jl", "jle", "js", "jns", "call", "ret",
          "push", "pop", "inc", "dec", "shl", "shr", "sar", "imul",
          "nop", "cdq", "cqo")


def valider_formes(lignes: list) -> None:
    """LES QUATRE INTERDITS — chaque violation REFUSÉE au nom de la cause
    (FORME-INVALIDE : cmp-mémoire-à-mémoire · movzx-r64-r64 · taille ·
    symbole-en-clair), à la ligne près. AUCUN contrôle retiré : les
    validateurs s'AJOUTENT aux contrôles v2 (le juge de l'assemblage
    demeure)."""
    for k, l in enumerate(lignes, 1):
        s = l.split(";")[0].strip()
        if not s or s.endswith(":"):
            continue
        parties = s.split()
        mnemo = parties[0].lower() if parties else ""
        # (a) cmp/test mémoire-à-mémoire
        if mnemo in ("cmp", "test"):
            ops = s[len(mnemo):]
            if len(RE_MEMOIRE.findall(ops)) >= 2:
                raise Refus(
                    "FORME-INVALIDE",
                    f"la ligne {k} : « {s[:52]} » — cmp/test "
                    "mémoire-à-mémoire PROSCRIT (un opérande mémoire au "
                    "plus : passe par un registre)")
        # (b) movzx r64/r64
        if mnemo == "movzx":
            ops = [x.strip() for x in s[len(mnemo):].split(",", 1)]
            if len(ops) == 2 and RE_REG64.match(ops[0]) \
                    and RE_REG64.match(ops[1]):
                raise Refus(
                    "FORME-INVALIDE",
                    f"la ligne {k} : « {s[:52]} » — movzx r64/r64 PROSCRIT "
                    "(la source est 32 bits ou moins)")
        # (c) le désalignement de taille d'un mov registre-registre
        if mnemo in ("mov", "and", "or", "xor", "add", "sub"):
            ops = [x.strip() for x in s[len(mnemo):].split(",", 1)]
            if len(ops) == 2 and not RE_MEMOIRE.search(s):
                d, src = ops
                if (RE_REG32.match(d) and RE_REG64.match(src)) or \
                        (RE_REG64.match(d) and RE_REG32.match(src)):
                    raise Refus(
                        "FORME-INVALIDE",
                        f"la ligne {k} : « {s[:52]} » — désalignement de "
                        "taille PROSCRIT (les tailles de la destination et "
                        "de la source s'accordent)")
        # (d) les symboles en clair (hors IDs, hors mnémoniques)
        for tok in re.split(r"[\s,\[\]+*\-]+", s):
            tok = tok.strip().rstrip(":")
            if not tok or tok.lower() in ("ptr", "byte", "word", "dword",
                                          "qword", "rip") or \
                    tok.lower() in MNEMOS:
                continue
            if RE_IDS_ADMIS.match(tok) or tok.lower() == tok:
                continue
            if RE_SYMBOLE_CLAIR.match(tok):
                raise Refus(
                    "FORME-INVALIDE",
                    f"la ligne {k} : « {s[:52]} » — le symbole « {tok} » en "
                    "clair PROSCRIT (la valeur numérique littérale ou "
                    "l'ID du dictionnaire, rien d'autre)")


# ===========================================================================
# LE PROMPT v3 — le squelette + le dictionnaire + LA GRAMMAIRE
# ===========================================================================
def prompt_ajouter_v3(nom_bloc: str) -> tuple:
    """LE PROMPT v3 = le prompt v2 + LA GRAMMAIRE PUBLIÉE (le modèle
    connaît la forme AVANT d'écrire — le levier OPT-15 inversé : au lieu
    de refuser la forme fausse APRÈS coup, la forme juste est ÉNONCÉE
    avant)."""
    prompt_v2, meta = prompt_ajouter_v2(nom_bloc)
    insertion = (
        f"\n{GRAMMAIRE_EBNF}\n"
        f"L'EMPREINTE DE LA GRAMMAIRE : sha256:{GRAMMAIRE_SHA256[:16]}… "
        "(gravée au matériau — tout écart de forme est refusé au nom de "
        "la cause, la réparation ciblée suit).\n"
    )
    marqueur = "REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE"
    assert marqueur in prompt_v2
    prompt = prompt_v2.replace(marqueur, insertion + "\n" + marqueur, 1)
    meta = dict(meta)
    meta["grammaire_id"] = GRAMMAIRE_ID
    meta["grammaire_sha256"] = GRAMMAIRE_SHA256
    return prompt, meta


# ===========================================================================
# L'ASSEMBLAGE v3 — les validateurs PUIS la chaîne v2 (aucun retrait)
# ===========================================================================
def assembler_v3(squelette: str, logique: str, meta: dict) -> tuple:
    """LE CLIENT ASSEMBLE v3 : (1) LES VALIDATEURS DE FORMES d'abord (les
    quatre interdits, refus au nom de la cause, la ligne fautive rendue à
    la réparation) ; (2) LA CHAÎNE v2 INTÉGRALEMENT (le dictionnaire
    recoupé, les formes du domaine, l'expansion, le round-trip, le cadre
    ABI) — AUCUN CONTRÔLE RETIRÉ."""
    lignes = logique.strip("\r\n").split("\n")
    valider_formes(lignes)
    return assembler_v2(squelette, logique, meta)


# ===========================================================================
# LA BOUCLE DE RÉPARATION — le budget TROIS, le refus nommé + la ligne
# ===========================================================================
def prompt_reparation(prompt_origine: str, logique_fautive: str,
                      refus_nom: str, refus_detail: str,
                      tentative: int) -> str:
    """LE PROMPT DE RÉPARATION CIBLÉE : la logique fautive, LE REFUS NOMMÉ,
    la ligne fautive extraite du détail — le modèle répare LA cause, le
    reste demeure. Le budget : TROIS reprises au plus (consigné par
    tentative — la présente ne porte QUE la construction du prompt)."""
    ligne_fautive = ""
    m = re.search(r"la ligne (\d+)", refus_detail)
    if m:
        k = int(m.group(1)) - 1
        lignes = logique_fautive.strip("\r\n").split("\n")
        if 0 <= k < len(lignes):
            ligne_fautive = lignes[k]
    return (
        "RÉPARATION CIBLÉE (la boucle « assemble → refus nommé → "
        "réparation »).\n\n"
        f"TA RÉPONSE PRÉCÉDENTE A ÉTÉ REFUSÉE : {refus_nom}\n"
        f"LA CAUSE EXACTE : {refus_detail}\n"
        + (f"LA LIGNE FAUTIVE : « {ligne_fautive.strip()} »\n"
           if ligne_fautive else "") +
        "\n"
        "TA TÂCHE : rends la logique RÉPARÉE — UNIQUEMENT la cause nommée\n"
        "change (la ligne fautive corrigée ; toute ligne saine demeure\n"
        "OCTET POUR OCTET) ; la même forme que la grammaire exige ; la\n"
        "réponse entière remplace la précédente (le squelette et le\n"
        "dictionnaire demeurent ceux du prompt d'origine, rappelés\n"
        "ci-dessous).\n\n"
        "=== LE PROMPT D'ORIGINE (le squelette, le dictionnaire, la "
        "grammaire) ===\n"
        f"{prompt_origine}\n"
        f"=== TA RÉPONSE FAUTIVE (à réparer) ===\n{logique_fautive}\n"
        f"=== FIN (tentative de réparation {tentative} sur le budget 3) ===\n"
    )
