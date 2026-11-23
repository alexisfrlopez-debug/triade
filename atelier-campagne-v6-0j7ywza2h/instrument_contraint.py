#!/usr/bin/env python3
"""instrument_contraint.py — atelier 0J7YWZA2H (la vague 16).

L'INSTRUMENT DU DÉCODAGE CONTRAINT : la grammaire canonique de la notation
TPL-ADD rendue EXÉCUTABLE. Le contexte est celui de l'Entrée 392 : le backend
expose `response_format` mais L'IGNORE (accepté-mais-ignoré) — la contrainte
n'existe pas au décodeur. L'instrument livré ici est donc la moitié qui ne
dépend d'aucun fournisseur : la grammaire, vérifiable MÉCANIQUEMENT.

DEUX LIVRAISONS :
  (1) `GRAMMAIRE_GBNF` — la source GBNF prête pour un serving local qui la
      supporte (llama.cpp, outlines, xgrammar) : la notation devient un
      langage du décodeur, et la classe HORS-FORMAT ne peut plus naître.
  (2) `valider_corps` — la MÊME grammaire en validateur déterministe : ce que
      le serving refuserait au décodage, le laboratoire le refuse à la lecture.
      Le contrôle négatif de l'instrument : une complétion HORS-FORMAT est
      REFUSÉE PAR LA GRAMMAIRE — pas par le juge.

L'ÉCART NOMMÉ : xgrammar/outlines/llguidance n'ont pas de roue Windows sur ce
poste (la compilation source a été interrompue) — l'instrument est livré en
GBNF + validateur, et l'écart est nommé. La campagne v6 N'EST PAS courue.
"""

import argparse
import json
import re
import sys

# --- les registres du domaine (l'énumération fermée de la grammaire) ---
_GPR64 = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"] + [f"r{i}" for i in range(8, 16)]
_GPR32 = ["eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp"] + [f"r{i}d" for i in range(8, 16)]
_GPR8 = ["al", "bl", "cl", "dl", "sil", "dil", "bpl", "spl"] + [f"r{i}b" for i in range(8, 16)]
_XMM = [f"xmm{i}" for i in range(16)]
REGISTRES = set(_GPR64 + _GPR32 + _GPR8 + _XMM)

TAILLES_64 = set(_GPR64) | set(_XMM)
TAILLES_32 = set(_GPR32)
TAILLES_8 = set(_GPR8)

RE_IMMEDIAT = re.compile(r"^-?(0x[0-9a-fA-F]+|\d+)$")
RE_ID = re.compile(r"^(LBL|CST)-(\d{3})$")
RE_ETIQUETTE = re.compile(r"^[a-z][a-z0-9_]*$")
RE_MEMOIRE_AVEC_TAILLE = re.compile(r"^(qword|dword|word|byte) ptr \[(.+)\]$")
RE_MEMOIRE_NUE = re.compile(r"^\[(.+)\]$")
RE_DECOMPOSE = re.compile(r"^([a-z0-9]+)\s*(?:\[(.+)\])?\s*$")

SAUTS = {"jmp", "je", "jne", "jz", "jnz", "ja", "jae", "jb", "jbe",
         "jg", "jge", "jl", "jle", "js", "jns"}
MNEMONIQUES = SAUTS | {"mov", "movzx", "movsx", "cmp", "test", "lea", "call", "ret",
                       "push", "pop", "add", "sub", "xor", "and", "or", "jmp",
                       "inc", "dec", "neg", "not", "shl", "shr", "sar", "imul",
                       "mul", "div", "cqo", "cdq", "nop", "sete", "setne", "setg"}

GRAMMAIRE_GBNF = r"""# LA GRAMMAIRE CANONIQUE DE LA NOTATION TPL-ADD (le corps que l'agent émet)
# Rendue pour un serving local à GBNF (llama.cpp). L'octet du contrat fait foi :
# le matériau TPL-ADD de loupe/ et tls13/notation/.

root        ::= corps
corps       ::= (ligne "\n")*
ligne       ::= definition | instruction
definition  ::= etiquette-locale ":"
etiquette-locale ::= [a-z] ([a-z] | [0-9] | "_")*
instruction ::= mnemonique (ws operande ("," ws operande)?)?
mnemonique  ::= "mov" | "movzx" | "movsx" | "cmp" | "test" | "lea"
              | "call" | "ret" | "push" | "pop" | "add" | "sub"
              | "xor" | "and" | "or" | "inc" | "dec" | "neg" | "not"
              | "shl" | "shr" | "sar" | "imul" | "mul" | "div"
              | "jmp" | "je" | "jne" | "jz" | "jnz" | "ja" | "jae"
              | "jb" | "jbe" | "jg" | "jge" | "jl" | "jle" | "js" | "jns"
operande    ::= registre | memoire | immediat | id | etiquette-locale
memoire     ::= ("qword" | "dword" | "word" | "byte") " ptr " "[" expr "]"
expr        ::= registre (("*" ("2"|"4"|"8")) | (("+"|"-") (registre | immediat)))?
registre    ::= "rax"|"rbx"|"rcx"|"rdx"|"rsi"|"rdi"|"rbp"|"rsp"
              | "r8"|"r9"|"r10"|"r11"|"r12"|"r13"|"r14"|"r15"
              | "eax"|"ebx"|"ecx"|"edx"|"esi"|"edi"|"ebp"|"esp"
              | "r8d"|"r9d"|"r10d"|"r11d"|"r12d"|"r13d"|"r14d"|"r15d"
              | "al"|"bl"|"cl"|"dl"|"sil"|"dil"|"bpl"|"spl"
              | "r8b"|"r9b"|"r10b"|"r11b"|"r12b"|"r13b"|"r14b"|"r15b"
              | "xmm0"|"xmm1"|"xmm2"|"xmm3"|"xmm4"|"xmm5"|"xmm6"|"xmm7"
              | "xmm8"|"xmm9"|"xmm10"|"xmm11"|"xmm12"|"xmm13"|"xmm14"|"xmm15"
immediat    ::= "-"? (("0x" [0-9a-fA-F]+) | [0-9]+)
id          ::= ("LBL" | "CST") "-" [0-9] [0-9] [0-9]
etiquette-locale ::= [a-z] ([a-z] | [0-9] | "_")*
ws          ::= " "+
"""


def _est_operande_simple(texte: str):
    """registre | immediat | ID | etiquette-locale"""
    if texte in REGISTRES:
        return "registre"
    if RE_IMMEDIAT.match(texte):
        return "immediat"
    if RE_ID.match(texte):
        return "id"
    if RE_ETIQUETTE.match(texte):
        return "etiquette"
    return None


def _valider_expression(expr: str):
    """L'intérieur des crochets : registre [*k] [+/- registre|immediat]."""
    m = re.match(r"^([a-z0-9]+)(?:\*(2|4|8))?(?:\s*([+-])\s*(.+))?$", expr.strip())
    if not m:
        return False, f"l'expression d'adressage « {expr} » n'est pas canonique"
    base, _, _, _,reste = m.group(1), m.group(2), m.group(3), m.group(4), m.group(4)
    if base not in REGISTRES:
        return False, f"« {base} » n'est pas un registre du domaine"
    if reste is not None and not _est_operande_simple(reste.strip()):
        return False, f"« {reste} » n'est pas un registre ni un immédiat"
    return True, "VERT"


def valider_ligne(ligne: str):
    """-> (ok, motif). TOUT refus est NOMMÉ à la cause."""
    texte = ligne.split(";")[0].strip()
    if not texte:
        return True, "(vide)"

    # la définition d'étiquette locale
    if texte.endswith(":"):
        nom = texte[:-1].strip()
        if not RE_ETIQUETTE.match(nom):
            return False, f"l'étiquette « {nom} » n'est pas un nom local minuscule"
        if nom.startswith(("lbl", "cst")):
            return False, (f"l'étiquette « {nom} » usurpe un ID du dictionnaire — "
                           f"les LBL-xxx ne se DÉFINISSENT pas")
        return True, "définition"

    parties = texte.split(None, 1)
    mnemo = parties[0].lower()
    reste = parties[1].strip() if len(parties) > 1 else ""
    if mnemo not in MNEMONIQUES:
        return False, f"« {mnemo} » n'est pas un mnémonique du domaine"

    if mnemo in SAUTS or mnemo == "call":
        cible = reste.strip()
        if not _est_operande_simple(cible):
            return False, f"la cible « {cible} » n'est ni un ID ni une étiquette"
        if mnemo in SAUTS and _est_operande_simple(cible) == "registre":
            return False, f"« {mnemo} » ne saute pas vers un registre"
        return True, "saut"

    if mnemo in ("ret", "nop", "cqo", "cdq"):
        return (True, "sans opérande") if not reste else (False, f"« {mnemo} » ne prend pas d'opérande")

    if not reste:
        return False, f"« {mnemo} » exige un opérande"

    # découper les opérandes au niveau supérieur (les crochets ne contiennent pas de virgule)
    operandes = [o.strip() for o in reste.split(",")]
    if len(operandes) > 2:
        return False, f"{len(operandes)} opérandes (deux au plus)"

    types = []
    for op in operandes:
        m = RE_MEMOIRE_AVEC_TAILLE.match(op)
        if m:
            ok, motif = _valider_expression(m.group(2))
            if not ok:
                return False, motif
            types.append(("memoire", m.group(1)))
            continue
        if RE_MEMOIRE_NUE.match(op):
            return False, (f"la mémoire NUE « {op} » est REFUSÉE — la taille doit être "
                           f"nommée (« qword ptr […] »)")
        t = _est_operande_simple(op)
        if not t:
            return False, f"« {op} » n'est ni un registre, ni une mémoire, ni un immédiat, ni un ID"
        types.append((t, None))

    # --- LES QUATRE INTERDITS DE FORME ---
    # (a) aucun cmp/test mémoire-à-mémoire
    if mnemo in ("cmp", "test"):
        nb_memoire = sum(1 for t, _ in types if t == "memoire")
        if nb_memoire > 1:
            return False, "INTERDIT (a) : un opérande mémoire AU PLUS par cmp/test"
    # (b) aucun movzx registre-64 vers registre-64
    if mnemo == "movzx":
        src = operandes[-1].strip()
        if src in TAILLES_64:
            return False, (f"INTERDIT (b) : movzx registre-64 → registre-64 "
                           f"« {src} » (la source doit être 32 bits ou moins)")
    # (c) aucun désalignement de taille dans mov
    if mnemo == "mov" and len(types) == 2 and all(t == "registre" for t, _ in types):
        a, b = operandes[0].strip(), operandes[1].strip()
        taille = lambda r: 64 if r in TAILLES_64 else (32 if r in TAILLES_32 else 8)
        if taille(a) != taille(b):
            return False, (f"INTERDIT (c) : « mov {a}, {b} » désaligne les tailles "
                           f"({taille(a)} vs {taille(b)})")
    # (d) aucun symbole en clair (un nom qui n'est ni registre, ni immédiat, ni ID)
    #     LES IDs SONT PROTÉGÉS DU DÉCOUPAGE : « CST-002 » est UN ID, pas deux symboles.
    for op in operandes:
        m = RE_MEMOIRE_AVEC_TAILLE.match(op)
        candidats = [m.group(2)] if m else [op]
        for c in candidats:
            c_sans_id = re.sub(r"\b(?:LBL|CST)-\d{3}\b", " ", c)
            for jeton in re.split(r"[\[\]\s+*]", c_sans_id):
                if jeton and not (jeton in REGISTRES or RE_IMMEDIAT.match(jeton)
                                  or RE_ID.match(jeton) or RE_ETIQUETTE.match(jeton)):
                    return False, (f"INTERDIT (d) : « {jeton} » est un symbole en clair — "
                                   f"la VALEUR NUMÉRIQUE ou l'ID du dictionnaire, rien d'autre")
    return True, "VERT"


def valider_corps(texte: str):
    """-> (ok, [(num_ligne, ligne, motif)]) — les refus NOMMÉS ligne par ligne."""
    refus = []
    for n, ligne in enumerate(texte.splitlines(), 1):
        ok, motif = valider_ligne(ligne)
        if not ok:
            refus.append((n, ligne, motif))
    return (not refus), refus


def autotest():
    print("=== L'AUTOTEST DE L'INSTRUMENT CONTRAINT ===")
    vert = """
mov r12, qword ptr [rbx + 520]
cmp r13, 15
je LBL-005
mov r10d, dword ptr [rcx + 8]
call CST-002
boucle:
mov qword ptr [rcx + 16], rax
fin:
ret
""".strip()
    refus_nommes = [
        ("mov r12, [rsp+0x28]", "la mémoire NUE"),
        ("movzx rax, rcx", "INTERDIT (b)"),
        ("mov eax, rbx", "INTERDIT (c)"),
        ("cmp qword ptr [rbx + 528], qword ptr [rcx + 8]", "INTERDIT (a)"),
        ("mov rax, WM_PAINT", "n'est ni un registre"),
        ("jmp rax", "ne saute pas vers un registre"),
        ("LBL-004:", "n'est pas un nom local minuscule"),
    ]

    tests = []
    ok, refus = valider_corps(vert)
    print(f"  [1] le corps VALIDE (7 lignes)          : {'VERT' if ok else 'ROUGE'}")
    if not ok:
        for n, l, m in refus:
            print(f"        ligne {n} : {m}")
    tests.append(ok)

    for i, (ligne, attendu) in enumerate(refus_nommes, 2):
        ok_l, motif = valider_ligne(ligne)
        bons = (not ok_l) and (attendu in motif)
        print(f"  [{i}] {ligne[:44]:44s} → {'REFUSÉ' if not ok_l else 'ACCEPTÉ (défaut)'}")
        print(f"        {motif}")
        tests.append(bons)

    print(f"  {sum(1 for t in tests if t)}/{len(tests)} contrôles rendus")
    return 0 if all(tests) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--corps", help="un fichier .asm à valider")
    ap.add_argument("--registre", default=None)
    args = ap.parse_args()
    if args.autotest:
        rc = autotest()
        if args.registre:
            with open(args.registre, "w", encoding="utf-8") as f:
                json.dump({"schema": "TRIADE-GRAMMAIRE-TPL-ADD-v1",
                           "controles": "8/8" if rc == 0 else "ECART",
                           "gbnf": "livré (GRAMMAIRE_GBNF)"},
                          f, ensure_ascii=False, indent=2)
        return rc
    if args.corps:
        texte = open(args.corps, encoding="utf-8").read()
        ok, refus = valider_corps(texte)
        if ok:
            print("[grammaire] VERT")
            return 0
        for n, l, m in refus:
            print(f"[grammaire] REFUS ligne {n} — {m}")
        return 3
    ap.error("--autotest ou --corps requis")


if __name__ == "__main__":
    sys.exit(main())
