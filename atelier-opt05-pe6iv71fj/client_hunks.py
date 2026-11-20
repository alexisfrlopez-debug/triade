#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""client_hunks.py — LE CLIENT DU FORMAT HUNK (le plan OPT-05 § 1.1-1.2).

Applique les hunks de l'agent à la base, reconstruit la notation
candidate, confronte PAR ROUND-TRIP EXACT (keystone assemble, capstone
désassemble). LES QUATRE REFUS NOMMÉS fail-closed, le premier rencontré
l'emporte :
  HORS-FORMAT | HUNK-INCONNU | CONTEXTE-DIVERGENT | ROUND-TRIP-DIVERGENT

La notation candidate n'est JAMAIS écrite en cas de refus."""
from __future__ import annotations

import re

# ---------------------------------------------------------------- la grammaire
LIGNE_HUNK = re.compile(r"^@@ hunk (\d+)/(\d+)$")
LIGNE_BASE = re.compile(r"^base: (.*)$")
LIGNE_MOINS = re.compile(r"^- (.*)$")
LIGNE_PLUS = re.compile(r"^\+ (.*)$")
FIN = "FIN-HUNKS"


class Refus(Exception):
    """Un refus nommé fail-closed."""

    def __init__(self, nom: str, detail: str):
        super().__init__(f"{nom}: {detail}")
        self.nom = nom
        self.detail = detail


def parse_hunks(reponse: str) -> list[dict]:
    """Parse la réponse à la grammaire gelée — HORS-FORMAT au premier écart."""
    if not isinstance(reponse, str):
        raise Refus("HORS-FORMAT", "la réponse n'est pas un texte")
    lignes = reponse.strip("\r\n").split("\n")
    if not lignes or lignes[-1].strip() != FIN:
        raise Refus("HORS-FORMAT", f"la dernière ligne n'est pas « {FIN} »")
    hunks: list[dict] = []
    courant: dict | None = None
    vu_fin = False
    for i, l in enumerate(lignes):
        s = l.rstrip("\r")
        if vu_fin:
            raise Refus("HORS-FORMAT", f"du texte après {FIN} (ligne {i+1})")
        if s.strip() == FIN:
            vu_fin = True
            continue
        m = LIGNE_HUNK.match(s)
        if m:
            if courant is not None:
                hunks.append(courant)
            k, n = int(m.group(1)), int(m.group(2))
            if k != len(hunks) + 1:
                raise Refus("HORS-FORMAT",
                            f"le hunk {k}/{n} hors séquence (attendu {len(hunks)+1})")
            courant = {"k": k, "n": n, "base": None, "moins": [], "plus": []}
            continue
        if courant is None:
            raise Refus("HORS-FORMAT", f"une ligne avant le premier « @@ hunk » (ligne {i+1})")
        m = LIGNE_BASE.match(s)
        if m and courant["base"] is None:
            courant["base"] = m.group(1)
            continue
        m = LIGNE_MOINS.match(s)
        if m:
            if courant["base"] is None:
                raise Refus("HORS-FORMAT", f"« - » avant « base: » (hunk {courant['k']})")
            courant["moins"].append(m.group(1))
            continue
        m = LIGNE_PLUS.match(s)
        if m:
            if courant["base"] is None:
                raise Refus("HORS-FORMAT", f"« + » avant « base: » (hunk {courant['k']})")
            courant["plus"].append(m.group(1))
            continue
        raise Refus("HORS-FORMAT", f"la ligne {i+1} n'est d'aucune forme admise : {s[:60]!r}")
    if courant is not None:
        hunks.append(courant)
    if not hunks:
        raise Refus("HORS-FORMAT", "aucun hunk dans la réponse")
    for h in hunks:
        if h["base"] is None:
            raise Refus("HORS-FORMAT", f"le hunk {h['k']} n'a pas d'ancre « base: »")
        if not h["plus"]:
            raise Refus("HORS-FORMAT", f"le hunk {h['k']} n'a aucune ligne « + »")
        if h["n"] != len(hunks):
            raise Refus("HORS-FORMAT",
                        f"le hunk {h['k']} annonce {h['n']} hunks, il y en a {len(hunks)}")
    return hunks


def appliquer(base_texte: str, hunks: list[dict]) -> str:
    """Applique les hunks EN ORDRE à la base — HUNK-INCONNU et
    CONTEXTE-DIVERGENT au premier écart. Retourne le texte reconstruit."""
    lignes = base_texte.split("\n")
    # l'état courant : on travaille sur une liste de lignes, chaque hunk
    # localise son ancre DANS LE TEXTE COURANT, retire ses « - », insère
    # ses « + » au même point
    for h in hunks:
        ancre = h["base"]
        idx = None
        for i, l in enumerate(lignes):
            if l == ancre:
                idx = i
                break
        if idx is None:
            raise Refus("HUNK-INCONNU",
                        f"l'ancre « {ancre[:60]} » (hunk {h['k']}) absente du texte courant")
        # les « - » doivent suivre l'ancre IMMÉDIATEMENT, dans l'ordre
        pos = idx + 1
        for attendu in h["moins"]:
            if pos >= len(lignes) or lignes[pos] != attendu:
                raise Refus("CONTEXTE-DIVERGENT",
                            f"la ligne « {attendu[:60]} » (hunk {h['k']}) n'est pas "
                            f"à l'ancre « {ancre[:40]} »")
            pos += 1
        lignes[idx + 1:pos] = list(h["plus"])
    return "\n".join(lignes)


# LES ALIAS DE MNÉMONIQUE (le désassembleur rend la forme canonique :
# jz→je etc. — la classe « encodages équivalents » du projet ; la
# comparaison normalise des deux côtés)
ALIAS = {
    "jz": "je", "jnz": "jne", "jb": "jc", "jnb": "jae", "jna": "jbe",
    "jnae": "jc", "jae": "jae", "jbe": "jbe", "ja": "ja",
    "jng": "jle", "jnle": "jg", "jnge": "jl", "jnl": "jge",
    "jpe": "jp", "jpo": "jnp", "jnc": "jae",
}


def normaliser(ligne: str) -> str:
    s = re.sub(r"\s+", " ", ligne).strip().lower()
    m = re.match(r"^([a-z][a-z0-9]*)\s+(.*)$", s)
    if m and m.group(1) in ALIAS:
        s = f"{ALIAS[m.group(1)]} {m.group(2)}"
    # LES NOMBRES : décimal et hexadécimal rendus à la même valeur (le
    # désassembleur préfère l'hex — la notation choisit librement)
    def _norm_nb(mo):
        try:
            v = int(mo.group(0), 0)
            return f"#{v}"
        except ValueError:
            return mo.group(0)
    s = re.sub(r"(?<![a-z_])(?:0x[0-9a-f]+|-?\d+)(?![a-z_])", _norm_nb, s)
    return s


def _equivalents_largeur(an: str, bn: str) -> bool:
    """Les mêmes nombres à la largeur d'opérande près (le signe est une
    vue : -4 == 0xfffffffc en 32 bits, -16 == 0xffff...f0 en 64)."""
    na = re.findall(r"#(-?\d+)", an)
    nb = re.findall(r"#(-?\d+)", bn)
    sa = re.sub(r"#-?\d+", "#", an)
    sb = re.sub(r"#-?\d+", "#", bn)
    if sa != sb or len(na) != len(nb):
        return False
    for x, y in zip(na, nb):
        ix, iy = int(x), int(y)
        if ix == iy:
            continue
        if (ix - iy) % (1 << 32) == 0 or (ix - iy) % (1 << 64) == 0:
            continue
        return False
    return True


DEBUT_CODE = re.compile(r"^(push|pop|mov|lea|cmp|test|jmp|je|jne|jz|jnz|ja|jb|jae|jbe|jg|jl|jge|jle|js|jns|call|ret|add|sub|and|or|xor|not|neg|shl|shr|sar|imul|mul|idiv|div|inc|dec|nop|db|dw|dd|dq|loop|rep|cld|std|leave|int3|xchg|movzx|movsx|cdq|cqo|sete|setne|setg|setl|seta|setb|cmov\w+)\b")


def extraire_notation(reponse: str) -> str:
    """Extrait la notation d'une réponse qui l'entoure de prose : le bloc
    clôturé ```…``` s'il existe, sinon les lignes de code contiguës (de la
    première à la dernière ligne de code ou de donnée)."""
    import re as _re
    clauses = _re.findall(r"```(?:[a-zA-Z0-9]*\n)?(.*?)```", reponse, _re.S)
    if clauses:
        return max(clauses, key=len)
    lignes = reponse.split("\n")
    idx = [i for i, l in enumerate(lignes) if DEBUT_CODE.match(l.strip())]
    if not idx:
        return reponse
    return "\n".join(lignes[idx[0]:idx[-1] + 1])


def round_trip(notation_texte: str) -> tuple[bool, str]:
    """La confrontation par round-trip exact : les lignes de code (hors
    commentaires) assemblées par keystone, désassemblées par capstone,
    re-notées — tout écart d'instruction, d'opérande ou de taille est
    un refus. Retourne (ok, détail)."""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from keystone import Ks, KS_ARCH_X86, KS_MODE_64

    code = []
    data = []
    for l in notation_texte.split("\n"):
        s = l.strip()
        if not s or s.startswith(";"):
            continue
        # LES COMMENTAIRES EN LIGNE sont retirés avant l'assemblage (le
        # « ; » n'apparaît jamais dans un opérande du domaine)
        s = s.split(";", 1)[0].strip()
        if not s:
            continue
        # LES DIRECTIVES DE DONNÉES (db/dw/dd/dq) ne sont pas des
        # instructions : elles sont comptées et vérifiées syntaxiquement,
        # jamais assemblées au round-trip (les chaînes du domaine vivent
        # en .rdata ; une chaîne littérale au bloc est une déclaration)
        if re.match(r"^(db|dw|dd|dq)\b", s):
            if s.count('"') % 2 != 0:
                return False, f"guillemets non appariés : {s[:60]}"
            data.append(s)
            continue
        if any(ord(c) > 127 for c in s):
            return False, f"caractère non-ASCII dans une instruction : {s[:60]!r}"
        code.append(s)
    if not code:
        return False, "aucune ligne de code"
    texte_code = "\n".join(code)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    try:
        octets, _ = ks.asm(texte_code)
    except Exception as e:
        return False, f"l'assemblage keystone échoue : {str(e)[:120]}"
    if not octets:
        return False, "l'assemblage keystone ne produit aucun octet"
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = False
    desassemble = []
    for ins in md.disasm(bytes(octets), 0x0):
        desassemble.append(f"{ins.mnemonic} {ins.op_str}".strip())
    if len(desassemble) != len(code):
        return False, (f"le désassemblage compte {len(desassemble)} instructions "
                       f"contre {len(code)} notées ({len(data)} ligne(s) de données)")
    for a, b in zip(code, desassemble):
        an = normaliser(a)
        bn = normaliser(b)
        if an != bn and not _equivalents_largeur(an, bn):
            return False, f"« {a} » != « {b} »"
    return True, f"{len(code)} instructions round-trip exact" + (
        f" + {len(data)} ligne(s) de données" if data else "")


def traiter(base_texte: str, reponse: str) -> tuple[str, str]:
    """LE PIPELINE COMPLET : parse (HORS-FORMAT), applique (HUNK-INCONNU,
    CONTEXTE-DIVERGENT), round-trip (ROUND-TRIP-DIVERGENT). Retourne
    (la notation reconstruite, le détail du round-trip). Lève Refus."""
    hunks = parse_hunks(reponse)
    reconstruit = appliquer(base_texte, hunks)
    ok, detail = round_trip(reconstruit)
    if not ok:
        raise Refus("ROUND-TRIP-DIVERGENT", detail)
    return reconstruit, detail


if __name__ == "__main__":
    # l'autotest du client (fail-closed sur les trois contrôles négatifs)
    base = "push rbx\nmov eax, 5\npop rbx\nret"
    ok_hunks = ("@@ hunk 1/1\n"
                "base: push rbx\n"
                "- mov eax, 5\n"
                "+ mov eax, 6\n"
                "FIN-HUNKS")
    r, d = traiter(base, ok_hunks)
    assert "mov eax, 6" in r and d.startswith("4 instructions"), d
    print("VERT  l'application et le round-trip exact :", d)
    cas = [
        ("HUNK-INCONNU", "@@ hunk 1/1\nbase: push rdx\n- mov eax, 5\n+ mov eax, 6\nFIN-HUNKS"),
        ("CONTEXTE-DIVERGENT", "@@ hunk 1/1\nbase: push rbx\n- mov eax, 6\n+ mov eax, 7\nFIN-HUNKS"),
        ("HORS-FORMAT", "mov eax, 6\nFIN-HUNKS"),
        ("HORS-FORMAT", "@@ hunk 1/1\nbase: push rbx\n+ mov eax, 6"),
        ("ROUND-TRIP-DIVERGENT", "@@ hunk 1/1\nbase: push rbx\n+ mov eax, 99999999999999999999\nFIN-HUNKS"),
    ]
    for attendu, rep in cas:
        try:
            traiter(base, rep)
            raise SystemExit(f"ÉCHEC — {attendu} NON ATTRAPÉ")
        except Refus as e:
            assert e.nom == attendu, (e.nom, attendu)
            print(f"VERT  le refus {e.nom} attrapé au premier nom — {e.detail[:60]}")
    print("LE CLIENT HUNKS : 1 VERT + 5 refus nommés — autotest VERT")
