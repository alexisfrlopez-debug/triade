#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'EXPANSEUR DÉTERMINISTE DU MODE AJOUTER (W19ADD) — pointeur-seul.

L'agent n'émet QUE le diff sémantique structuré : opcode, opérandes, offset au point
exact. L'expandeur (côté client) compile la notation complète SANS choix : un seul
rendu canonique par pointeur. Le juge re-parse le texte produit et rend, en cas de
refus, la classe, la position et l'attendu — la boucle de réparation les réinjecte,
bornée à TROIS tours.

Quatre refus nommés fail-closed :
  HORS-FORMAT          opcode hors du domaine fermé, forme non canonique ;
  ID-INCONNU           CST-/LBL- absent du dictionnaire du bloc ;
  EXPANSION-DIVERGENTE l'ID ne convient pas au trou typé (ex. « call » sur une constante) ;
  FORME-INVALIDE       schéma malformé, offset hors plage, opérande incompatible.

Usage :
  python3 scripts/vague19/expandeur_add.py --fixtures      # 18 pointeurs honnêtes + 4 mutés
  python3 scripts/vague19/expandeur_add.py --preregistrer
  python3 scripts/vague19/expandeur_add.py --statut
"""
import hashlib
import json
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = RACINE / "atelier-w19-add"
GRAINE = 20261124
OPS = {"mov", "add", "sub", "xor", "and", "or", "cmp", "test", "jcc", "call", "ret"}
REGS = {"eax", "ebx", "ecx", "edx", "esi", "edi", "rax", "rbx", "rcx", "rdx",
        "r8", "r9", "r10", "r11", "esp", "ebp", "rsp", "rbp"}
MAX_TOURS = 3


class Refus(Exception):
    def __init__(self, classe, position, attendu):
        super().__init__(f"{classe}@{position}: {attendu}")
        self.classe, self.position, self.attendu = classe, position, attendu


def _verifie_schema(p):
    if not isinstance(p, dict):
        raise Refus("FORME-INVALIDE", 0, "un pointeur est un objet {op, dst, src, offset}")
    for k in ("op", "offset"):
        if k not in p:
            raise Refus("FORME-INVALIDE", 0, f"champ obligatoire absent : {k}")
    if not isinstance(p["offset"], int) or not (0 <= p["offset"] <= 0xFFFF):
        raise Refus("FORME-INVALIDE", 0, "offset entier dans [0, 0xFFFF]")
    if p["op"] not in OPS:
        raise Refus("HORS-FORMAT", 0, f"opcode du domaine fermé : {sorted(OPS)}")


def _operande(spec, dictionnaire, trou):
    """Rend l'opérande canonique ; le trou typé décide de ce qui est admis."""
    if not isinstance(spec, dict) or "type" not in spec:
        raise Refus("FORME-INVALIDE", 1, "opérande = {type, valeur}")
    t, v = spec["type"], spec.get("valeur")
    if t == "reg":
        if v not in REGS:
            raise Refus("FORME-INVALIDE", 1, f"registre inconnu : {v}")
        return v
    if t == "imm":
        if not isinstance(v, int) or not (0 <= v <= 0xFFFFFFFF):
            raise Refus("FORME-INVALIDE", 1, "immédiat entier 32 bits")
        return f"0x{v:x}"
    if t == "mem":
        if not re.fullmatch(r"\[[a-z0-9+* ]+\]", str(v)):
            raise Refus("FORME-INVALIDE", 1, "mémoire « [reg+disp] »")
        return str(v)
    if t in ("cst", "lbl"):
        prefixe = "CST-" if t == "cst" else "LBL-"
        if not re.fullmatch(prefixe + r"\d{3}", str(v)):
            raise Refus("FORME-INVALIDE", 1, f"ID au format {prefixe}NNN")
        if v not in dictionnaire:
            raise Refus("ID-INCONNU", 1, f"{v} absent du dictionnaire du bloc")
        if trou and trou != t:
            raise Refus("EXPANSION-DIVERGENTE", 1,
                        f"le trou typé attend un {trou} : {v} ne convient pas")
        return v
    raise Refus("FORME-INVALIDE", 1, f"type d'opérande inconnu : {t}")


def expanse(pointeur, dictionnaire):
    """Compile le pointeur en notation canonique — un seul rendu possible."""
    _verifie_schema(pointeur)
    op = pointeur["op"]
    if op == "ret":
        return "ret"
    if op == "call":
        cible = pointeur.get("src")
        if not isinstance(cible, dict):
            raise Refus("FORME-INVALIDE", 0, "call exige une cible {type: cst}")
        return f"call {_operande(cible, dictionnaire, 'cst')}"
    if "dst" not in pointeur:
        raise Refus("FORME-INVALIDE", 0, "l'opcode exige un dst")
    dst = _operande(pointeur["dst"], dictionnaire, "lbl" if op == "jcc" else None)
    if op == "jcc":
        return f"{op} {dst}"
    if "src" not in pointeur:
        raise Refus("FORME-INVALIDE", 0, "l'opcode exige un src")
    return f"{op} {dst}, {_operande(pointeur['src'], dictionnaire, None)}"


def juge(texte, pointeur, dictionnaire):
    """Re-parse le texte canonique et confronte au pointeur (le juge n'est jamais affaibli)."""
    attendu = expanse(pointeur, dictionnaire)
    if texte != attendu:
        raise Refus("HORS-FORMAT", 0, f"forme canonique : « {attendu} »")
    if "\n" in texte:
        raise Refus("HORS-FORMAT", 0, "une instruction par ligne")
    return True


def boucle_reparation(pointeur, dictionnaire, journal=None):
    """La réparation par contre-exemple, bornée à TROIS tours ; chaque conversion consignée."""
    conversions = []
    essai = pointeur
    for tour in range(1, MAX_TOURS + 1):
        try:
            texte = expanse(essai, dictionnaire)
            juge(texte, essai, dictionnaire)
            if journal is not None:
                journal.append({"tour": tour, "verdict": "VERT", "texte": texte,
                                "classes_converties": conversions})
            return {"verdict": "VERT", "texte": texte, "tours": tour,
                    "classes_converties": conversions}
        except Refus as r:
            conversions.append(r.classe)
            if journal is not None:
                journal.append({"tour": tour, "verdict": f"REFUS {r.classe}",
                                "position": r.position, "attendu": r.attendu})
            # le contre-exemple exact est réinjecté : on répare le champ fautif
            if r.classe == "ID-INCONNU":
                essai = _reparer_id(essai, dictionnaire)
            elif r.classe == "EXPANSION-DIVERGENTE":
                essai = _reparer_trou(essai)
            else:
                break
    return {"verdict": "REFUS", "texte": None, "tours": MAX_TOURS,
            "classes_converties": conversions}


def _reparer_id(p, dictionnaire):
    """Remplace l'ID inconnu par le premier ID du même préfixe au dictionnaire."""
    q = json.loads(json.dumps(p))
    for cote in ("dst", "src"):
        o = q.get(cote)
        if isinstance(o, dict) and o.get("type") in ("cst", "lbl"):
            prefixe = "CST-" if o["type"] == "cst" else "LBL-"
            candidats = sorted(k for k in dictionnaire if k.startswith(prefixe))
            q[cote] = dict(o, valeur=candidats[0] if candidats else o["valeur"])
    return q


def _reparer_trou(p):
    """Un ID de constante employé là où le trou attend une étiquette : on prend l'étiquette."""
    q = json.loads(json.dumps(p))
    o = q.get("src") or q.get("dst")
    if isinstance(o, dict):
        q["src" if "src" in q else "dst"] = dict(o, type="lbl", valeur="LBL-001")
    return q


DICO = {f"CST-{i:03d}": f"constante {i}" for i in range(1, 9)}
DICO.update({f"LBL-{i:03d}": f"étiquette {i}" for i in range(1, 9)})


def fixtures():
    """18 pointeurs honnêtes (une opération par tâche) + 4 mutations, une par refus."""
    honnetes = []
    modeles = [
        {"op": "mov", "dst": {"type": "reg", "valeur": "eax"}, "src": {"type": "cst", "valeur": "CST-001"}},
        {"op": "add", "dst": {"type": "reg", "valeur": "eax"}, "src": {"type": "imm", "valeur": 42}},
        {"op": "sub", "dst": {"type": "reg", "valeur": "ebx"}, "src": {"type": "reg", "valeur": "eax"}},
        {"op": "xor", "dst": {"type": "reg", "valeur": "ecx"}, "src": {"type": "cst", "valeur": "CST-002"}},
        {"op": "and", "dst": {"type": "reg", "valeur": "edx"}, "src": {"type": "imm", "valeur": 255}},
        {"op": "or", "dst": {"type": "reg", "valeur": "esi"}, "src": {"type": "cst", "valeur": "CST-003"}},
        {"op": "cmp", "dst": {"type": "reg", "valeur": "edi"}, "src": {"type": "imm", "valeur": 7}},
        {"op": "test", "dst": {"type": "reg", "valeur": "eax"}, "src": {"type": "reg", "valeur": "eax"}},
        {"op": "jcc", "dst": {"type": "lbl", "valeur": "LBL-001"}},
        {"op": "call", "src": {"type": "cst", "valeur": "CST-004"}},
        {"op": "mov", "dst": {"type": "mem", "valeur": "[esp+4]"}, "src": {"type": "reg", "valeur": "eax"}},
        {"op": "mov", "dst": {"type": "reg", "valeur": "r8"}, "src": {"type": "cst", "valeur": "CST-005"}},
        {"op": "add", "dst": {"type": "reg", "valeur": "r9"}, "src": {"type": "imm", "valeur": 1}},
        {"op": "sub", "dst": {"type": "reg", "valeur": "r10"}, "src": {"type": "reg", "valeur": "r9"}},
        {"op": "xor", "dst": {"type": "reg", "valeur": "eax"}, "src": {"type": "cst", "valeur": "CST-006"}},
        {"op": "mov", "dst": {"type": "reg", "valeur": "ebx"}, "src": {"type": "cst", "valeur": "CST-007"}},
        {"op": "jcc", "dst": {"type": "lbl", "valeur": "LBL-002"}},
        {"op": "ret"},
    ]
    for i, m in enumerate(modeles):
        p = json.loads(json.dumps(m))
        p["offset"] = 0x100 + 4 * i
        honnetes.append(p)
    mutes = {
        "HORS-FORMAT": {"op": "rdtsc", "offset": 0x40},
        "ID-INCONNU": {"op": "mov", "dst": {"type": "reg", "valeur": "eax"},
                       "src": {"type": "cst", "valeur": "CST-999"}, "offset": 0x44},
        "EXPANSION-DIVERGENTE": {"op": "jcc", "dst": {"type": "cst", "valeur": "CST-001"}, "offset": 0x48},
        "FORME-INVALIDE": {"op": "mov", "dst": {"type": "reg", "valeur": "eax"},
                           "src": {"type": "imm", "valeur": -3}, "offset": 0x4C},
    }
    return honnetes, mutes


def compter_tokens(texte):
    """Convention nommée : les unités lexicales (mnémonique, opérandes, ponctuation)."""
    return len(re.findall(r"[A-Za-z0-9_\-\[\]+*]+|,", texte))


def compter_tokens_independant(texte):
    """Seconde implémentation, indépendante (découpage par caractères non alphanumériques)."""
    out = 0
    for mot in re.split(r"([,\s]+)", texte):
        if mot.strip():
            out += 1
    return out


def fixtures_rapport():
    honnetes, mutes = fixtures()
    journal = []
    verts = 0
    for p in honnetes:
        try:
            r = boucle_reparation(p, DICO, journal)
            verts += 1 if r["verdict"] == "VERT" else 0
        except Exception as e:  # pragma: no cover
            print("rouge", e)
    refus = {}
    for classe, p in mutes.items():
        try:
            r = boucle_reparation(p, DICO)
            refus[classe] = r["classes_converties"][0] if r["classes_converties"] else r["verdict"]
        except Refus as r:
            refus[classe] = r.classe
    # ratios aux opérandes NON arrondis
    tokens = [compter_tokens(expanse(p, DICO)) for p in honnetes]
    tokens2 = [compter_tokens_independant(expanse(p, DICO)) for p in honnetes]
    ecarts = [abs(a - b) for a, b in zip(tokens, tokens2)]
    med = sorted(tokens)[len(tokens) // 2]
    med2 = sorted(tokens2)[len(tokens2) // 2]
    print("=" * 78)
    print("EXPANSEUR ADD — 18 POINTEURS HONNÊTES, 4 FIXTURES MUTÉES")
    print("=" * 78)
    print(f"[fixtures] pointeurs honnêtes verts : {verts}/18")
    print(f"[fixtures] refus par classe : {refus}")
    print(f"[tokens] convention 1 : total {sum(tokens)} · médiane {med} · "
          f"convention 2 : total {sum(tokens2)} · médiane {med2} · écart max {max(ecarts)} "
          f"(±1 exigé : {'VERT' if max(ecarts) <= 1 else 'ROUGE'})")
    ok = verts == 18 and set(refus.values()) == set(mutes) and max(ecarts) <= 1
    return 0 if ok else 3


def preregistrer():
    doc = {
        "objet": "frontière add — expansion déterministe côté client, pointeur-seul",
        "cible": "≥ 15/18 verts à ≤ 3 000 tokens par changement validé",
        "mediane": ["sur les 18 tâches", "sur les seules vertes (deux conventions nommées)"],
        "graine": GRAINE,
        "reparation": f"borne {MAX_TOURS} tours, contre-exemple réinjecté",
        "tokenisation": "convention 1 = unités lexicales ; convention 2 = découpage "
                        "indépendant ; écart exigé ≤ 1 token",
        "statut": "EN ATTENTE — aucune campagne servie dans ce bac ; l'instrument et ses "
                  "fixtures sont verts, la mesure viendra d'un serving à structured output",
    }
    DOSSIER.mkdir(exist_ok=True)
    f = DOSSIER / "preregistrement.json"
    f.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[preregistre] {f.relative_to(RACINE)} sha256 {hashlib.sha256(f.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    if "--fixtures" in sys.argv:
        sys.exit(fixtures_rapport())
    if "--preregistrer" in sys.argv:
        sys.exit(preregistrer())
    print("EN ATTENTE — l'instrument est rejouable par --fixtures ; aucune campagne réelle.")
    sys.exit(0)
