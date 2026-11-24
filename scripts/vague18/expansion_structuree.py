#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSV9ITVNG — L'EXPANSION SOUS CONTRAINTE DE GRAMMAIRE (D264).

L'opération « ajouter » échouait en texte libre (campagne v5 : 5/18 verts, cible
≥ 15/18 manquée, cause nommée : variance CLI du sujet ; 21/24 vertes refusées par
la grammaire, D257). L'expansion ne s'écrit plus en texte libre : le modèle rend un
SCHÉMA STRUCTURÉ (opcode / opérande / offset), validé à la génération, puis rendu
en notation canonique par un formateur unique. Un refus honnête fournit le
contre-exemple minimal (ddmin), borné à 3 tours de réparation.

Aucun chiffre de campagne n'est produit ici : l'instrument est livré, la campagne
attend un serving qui expose le structured output (EN ATTENTE, jamais simulée).
"""
import json
import sys

OPCODES = {"mov", "add", "sub", "cmp", "and", "or", "xor", "lea", "jmp", "je", "jne",
           "call", "ret", "push", "pop", "inc", "dec", "nop"}
FORMES = {"reg", "reg_mem_taille", "imm", "label"}
OFFSET_MAX = 2 ** 31 - 1
TOURS_MAX = 3


class Refus(Exception):
    pass


def valide_schema(obj):
    if not isinstance(obj, dict) or set(obj) != {"opcode", "operande", "offset"}:
        raise Refus("SCHEMA-INCOMPLET")
    if obj["opcode"] not in OPCODES:
        raise Refus("OPCODE-HORS-ENUMERATION")
    if not isinstance(obj["operande"], dict) or obj["operande"].get("forme") not in FORMES:
        raise Refus("FORME-D-OPERANDE-INCONNUE")
    off = obj["offset"]
    if not isinstance(off, int) or abs(off) > OFFSET_MAX:
        raise Refus("OFFSET-HORS-BORNES")
    return True


def rendre(obj):
    """Le formateur UNIQUE : le schéma devient la notation TPL-ADD canonique."""
    valide_schema(obj)
    o, forme, off = obj["opcode"], obj["operande"], obj["offset"]
    if forme["forme"] == "reg":
        return f"{o} {forme['reg']}"
    if forme["forme"] == "reg_mem_taille":
        return f"{o} {forme['reg']}, {forme['taille']} ptr [{forme['base']} + {off}]"
    if forme["forme"] == "imm":
        return f"{o} {forme['valeur']}"
    return f"{o} {forme['label']}"


def ddmin(lignes, echoue):
    """Réduit à un contre-exemple minimal qui ÉCHOUE encore (delta debugging simple)."""
    courant = list(lignes)
    n = 2
    while len(courant) >= 2:
        morceaux = [courant[i::n] for i in range(n)]
        reduit = False
        for m in morceaux:
            candidat = [l for l in courant if l not in m] or m
            if echoue(candidat):
                courant = candidat
                n = max(n - 1, 2)
                reduit = True
                break
        if not reduit:
            if n >= len(courant):
                break
            n = min(n * 2, len(courant))
    return courant


def boucle_reparation(schema, juge, reparer, max_tours=TOURS_MAX):
    """Jusqu'à trois tours : le refus fournit le contre-exemple minimal (ddmin), que
    `reparer(schema, contre_exemple)` — le modèle, à l'extérieur — consomme. La boucle
    est BORNÉE : au troisième refus, elle rend REFUS-APRES-3-TOURS, jamais un 4e tour."""
    courant = schema
    for tour in range(max_tours):
        texte = rendre(courant)
        verdict, motif = juge(texte)
        if verdict:
            return {"statut": "VERT", "tours": tour, "texte": texte}
        contre = ddmin(texte.splitlines(), lambda ls: juge("\n".join(ls))[0] is False)
        courant = reparer(courant, contre)
    return {"statut": "REFUS-APRES-3-TOURS", "tours": max_tours}


def autotest():
    cas = [
        ("schéma valide", {"opcode": "mov", "operande": {"forme": "reg_mem_taille", "reg": "rax", "taille": "qword", "base": "rbx"}, "offset": 16}, "VERT"),
        ("opcode hors énumération", {"opcode": "syscall", "operande": {"forme": "reg", "reg": "rax"}, "offset": 0}, "REFUS"),
        ("forme d'opérande inconnue", {"opcode": "mov", "operande": {"forme": "memoire_nue"}, "offset": 0}, "REFUS"),
        ("offset hors bornes", {"opcode": "mov", "operande": {"forme": "reg", "reg": "rax"}, "offset": OFFSET_MAX + 1}, "REFUS"),
        ("schéma incomplet", {"opcode": "mov", "operande": {"forme": "reg", "reg": "rax"}}, "REFUS"),
    ]
    verts = 0
    print("=" * 78)
    print("LSV9ITVNG — L'EXPANSION SOUS CONTRAINTE (D264)")
    print("=" * 78)
    for nom, obj, attendu in cas:
        try:
            valide_schema(obj); rendu = "VERT"
        except Refus:
            rendu = "REFUS"
        ok = (rendu == attendu)
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} → {rendu}")
    # le rendu canonique
    t = rendre({"opcode": "mov", "operande": {"forme": "reg_mem_taille", "reg": "rax", "taille": "qword", "base": "rbx"}, "offset": 16})
    ok = t == "mov rax, qword ptr [rbx + 16]"
    verts += 1 if ok else 0
    print(f"[{'VERT' if ok else 'ROUGE'}] rendu canonique → {t}")
    # ddmin : garde le contre-exemple minimal qui échoue encore
    lignes = ["mov rax, qword ptr [rbx + 16]", "mov rcx, [rbx]", "ret"]
    juge = lambda s: ("VERT" if "[" not in s.replace("ptr [", "") else "REFUS", "memoire nue")
    reduit = ddmin(lignes, lambda ls: juge("\n".join(ls))[0] == "REFUS")
    ok = reduit == ["mov rcx, [rbx]"]
    verts += 1 if ok else 0
    print(f"[{'VERT' if ok else 'ROUGE'}] ddmin → contre-exemple minimal {reduit}")
    # la boucle est bornée à 3 tours
    # (i) la boucle CONVERGE quand la réparation consomme le contre-exemple
    etat = {"n": 0}
    def repare(schema, contre):
        etat["n"] += 1
        return {"opcode": "mov", "operande": {"forme": "reg", "reg": "rax"}, "offset": 0} if etat["n"] < 2 else schema
    convergence = boucle_reparation({"opcode": "mov", "operande": {"forme": "reg", "reg": "rbx"}, "offset": 0},
                                    lambda s: (etat["n"] >= 2, "refus"), repare)
    ok = convergence["statut"] == "VERT" and convergence["tours"] == 2
    verts += 1 if ok else 0
    print(f"[{'VERT' if ok else 'ROUGE'}] boucle convergente → {convergence['statut']} au tour {convergence['tours']}")
    # (ii) la boucle REFUSE au troisième tour quand rien ne converge
    r = boucle_reparation({"opcode": "mov", "operande": {"forme": "reg", "reg": "rax"}, "offset": 0},
                          lambda s: (False, "refus"), lambda schema, contre: schema)
    ok = r["statut"] == "REFUS-APRES-3-TOURS" and r["tours"] == 3
    verts += 1 if ok else 0
    print(f"[{'VERT' if ok else 'ROUGE'}] boucle bornée → {r['statut']} après {r['tours']} tours")
    total = len(cas) + 4
    print(f"{verts}/{total}")
    print("campagne : EN ATTENTE d'un serving à structured output — aucun chiffre produit ici")
    return 0 if verts == total else 3


if __name__ == "__main__":
    sys.exit(autotest())
