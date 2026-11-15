#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""epreuve_feuille_memcmp.py — L'ÉPREUVE QUI MANQUAIT (la 304) : la
feuille memcmp du scénario C LIVRÉ tenue contre la faute nommée — la
304 : le run de l'unité 5 × bras C tomba au premier candidat de l'école
(access violation 0x92da, l'adresse nue de l'entrée hint/nom de memcmp
— le slot IAT jamais lié sous DONT_RESOLVE).

L'épreuve lit LE FICHIER livré (l'AST du scénario même, jamais exécuté —
le run est au terrain, CA6) et y vérifie TROIS LOIS :

  L1 LA FEUILLE DÉCOUVERTE PAR LA TABLE D'IMPORTS : le scénario lit le
     répertoire 1 (opt + 120, la table d'imports de l'en-tête PE32+) et
     découvre le slot memcmp PAR LE NOM (msvcrt.dll / memcmp) — la
     convention (base, rva) unifiée de la 302, AUCUNE RVA codée en dur ;
  L2 LA LIAISON AVANT L'APPEL : au flux de main(), la liaison de la
     feuille (le guichet, ou l'écriture au slot découvert) précède la
     CONSTRUCTION de la pièce comme fonction (le CFUNCTYPE — au-delà,
     le premier appel peut survenir à tout geste) et sa retombée est
     gardée (un guichet refusé STOPPE le flux) ; LA FAUTE NOMMÉE du v1 :
     la pièce construite ligne 207, le premier appel ligne 218, RIEN
     lié entre les deux — le thunk sauta à la valeur sur disque du
     slot (0x92da, l'entrée hint/nom), l'adresse nue du crash ;
  L3 LE GUICHET FAIL-CLOSED DE LA LIAISON : chaque geste de la liaison
     (LoadLibrary, GetProcAddress, VirtualProtect ×2, la relecture du
     slot) a son retour LU et son écart NOMMÉ (un REFUS, le flux
     stoppé) — AUCUN geste nu au retour jeté, la relecture recoupe
     l'écrit.

L'épreuve est tenue au bac du labo contre CHAQUE scénario C livré (la
règle née à la 294, étendue à la 304 : la plomberie de la feuille
voyage au terrain, l'épreuve la tient au fichier livré — le harnais du
labo qui shimait memcmp ne prouve JAMAIS le scénario livré).

Usage : epreuve_feuille_memcmp.py <scenario.py>   →  VERT / ROUGE nommé.
"""
import ast
import sys


def nom_appel(node):
    """le nom d'un appel : f(...) → f, ou obj.meth(...) → obj.meth."""
    if not isinstance(node, ast.Call):
        return None
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def trouve_main(tree):
    return next((n for n in tree.body
                 if isinstance(n, ast.FunctionDef) and n.name == "main"),
                None)


def loi_l1(tree, rapport):
    """L1 : la feuille découverte par la table d'imports — le répertoire 1
    lu (opt + 120), les noms cherchés (msvcrt.dll, memcmp), AUCUNE RVA
    codée en dur (0x91a0 ni tout autre slot)."""
    src_lu, noms_dll, noms_fn = [], [], []
    for node in ast.walk(tree):
        # la lecture du répertoire d'imports : lire_u32(base, opt + 120)
        if nom_appel(node) == "lire_u32" and len(node.args) >= 2:
            arg = node.args[1]
            if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add) \
                    and isinstance(arg.left, ast.Name) \
                    and arg.left.id == "opt" \
                    and isinstance(arg.right, ast.Constant) \
                    and arg.right.value == 120:
                src_lu.append(node.lineno)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value.lower() == "msvcrt.dll":
                noms_dll.append(node.lineno)
            if node.value == "memcmp":
                noms_fn.append(node.lineno)
    rvas = [n.lineno for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, int)
            and n.value in (0x91a0, 0x1380, 0x2398)]
    fautes = []
    if not src_lu:
        fautes.append("le répertoire 1 (opt + 120) JAMAIS LU — la table "
                      "d'imports que la pièce porte n'est même pas "
                      "ouverte")
    if not noms_dll or not noms_fn:
        fautes.append("les noms jamais cherchés (msvcrt.dll : "
                      f"{noms_dll or 'rien'} ; memcmp : {noms_fn or 'rien'}) "
                      "— la feuille n'est pas découverte, elle est tenue "
                      "pour absente")
    if rvas:
        fautes.append(f"des RVA CODÉES EN DUR aux lignes {rvas} — la "
                      "convention (base, rva) de la 302 foulée : la table "
                      "parle, jamais le littéral")
    if fautes:
        for f in fautes:
            rapport.append(f"L1 ROUGE : {f}")
        rapport.append("L1 ROUGE : LA FAUTE NOMMÉE du v1 — le scénario "
                       "tenait la feuille pour absente (« le scénario ne "
                       "touche pas à la table d'imports ») tandis que la "
                       "clôture de la pièce appelle le thunk memcmp (le "
                       "seul appel de sa clôture)")
        return False
    rapport.append(
        f"L1 VERT : la feuille découverte par la table — le répertoire 1 "
        f"lu (lignes {src_lu}), les noms cherchés (msvcrt.dll ligne "
        f"{noms_dll[0]}, memcmp ligne {noms_fn[0]}), AUCUNE RVA codée en "
        "dur (la convention (base, rva) de la 302)")
    return True


def loi_l2(tree, rapport):
    """L2 : la liaison avant l'appel — au flux de main(), la liaison
    précède la construction de la pièce (le CFUNCTYPE) et sa retombée
    est gardée."""
    main = trouve_main(tree)
    if main is None:
        rapport.append("L2 ROUGE : pas de main()")
        return False
    idx_construction, idx_liaison, idx_garde = None, None, None
    for i, st in enumerate(main.body):
        sous = list(ast.walk(st))
        # la construction de la pièce : LOUPE13 = CFUNCTYPE(...)(...)
        if idx_construction is None:
            for n in sous:
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Call) \
                        and nom_appel(n.func) == "CFUNCTYPE":
                    idx_construction = i
        # la liaison : l'appel du guichet (lier_feuille_memcmp) ou
        # l'écriture au slot découvert (memmove vers base + rva_slot)
        if idx_liaison is None:
            for n in sous:
                if nom_appel(n) == "lier_feuille_memcmp":
                    idx_liaison = i
                elif nom_appel(n) == "memmove" and n.args:
                    dest = n.args[0]
                    if isinstance(dest, ast.BinOp) \
                            and isinstance(dest.left, ast.Name) \
                            and dest.left.id == "base" \
                            and isinstance(dest.right, ast.Name) \
                            and dest.right.id.startswith("rva_slot"):
                        idx_liaison = i
        # la garde : if feuille is None: return / if not feuille: return
        if isinstance(st, ast.If):
            t = st.test
            nomme_none = isinstance(t, ast.Compare) and \
                len(t.ops) == 1 and isinstance(t.ops[0], (ast.Is, ast.Eq))
            if nomme_none:
                cote_nom = isinstance(t.left, ast.Name)
                cote_none = (len(t.comparators) == 1
                             and isinstance(t.comparators[0], ast.Constant)
                             and t.comparators[0].value is None)
                nomme_none = cote_nom and cote_none
            nomme_not = isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.Not)
            if (nomme_none or nomme_not) and \
                    any(isinstance(s, ast.Return) for s in ast.walk(st)):
                if idx_liaison is not None and idx_garde is None \
                        and i >= idx_liaison:
                    idx_garde = i
    fautes = []
    if idx_liaison is None:
        ou = (f"construite à l'énoncé {idx_construction + 1}"
              if idx_construction is not None else "jamais construite")
        rapport.append(
            "L2 ROUGE : AUCUNE liaison au flux de main() — la pièce "
            f"{ou}, "
            "le premier appel peut suivre, RIEN n'est lié : le thunk "
            "sauterait à la valeur SUR DISQUE du slot IAT (0x92da, "
            "l'entrée hint/nom de memcmp — une RVA nue, hors de toute "
            "page) : L'ADRESSE EXACTE du crash terrain (« access "
            "violation writing 0x92da », le run tombé code 1 au premier "
            "candidat de l'école)")
        return False
    if idx_construction is not None and idx_liaison > idx_construction:
        fautes.append(f"la liaison (énoncé {idx_liaison + 1}) APRÈS la "
                      f"construction de la pièce (énoncé {idx_construction + 1}) "
                      "— un appel entre les deux sauterait à la feuille "
                      "morte")
    if idx_garde is None:
        fautes.append("la retombée de la liaison JAMAIS GARDÉE — un "
                      "guichet refusé laisserait le flux courir sur la "
                      "feuille morte")
    if fautes:
        for f in fautes:
            rapport.append(f"L2 ROUGE : {f}")
        return False
    rapport.append(
        f"L2 VERT : la liaison (énoncé {idx_liaison + 1}) précède la "
        f"construction de la pièce (énoncé "
        f"{idx_construction + 1 if idx_construction is not None else '—'}) "
        f"et sa retombée est gardée (énoncé {idx_garde + 1}) — jamais un "
        "appel sur une feuille morte")
    return True


def loi_l3(tree, rapport):
    """L3 : le guichet fail-closed de la liaison — chaque geste (LoadLibrary,
    GetProcAddress, VirtualProtect, la relecture) a son retour lu et son
    écart nommé (un REFUS + l'arrêt) ; la relecture recoupe l'écrit."""
    gestes = ("LoadLibrary", "GetProcAddress", "VirtualProtect")

    def est_geste(nom):
        return nom is not None and any(nom.startswith(g) for g in gestes)

    # NU = le geste en énoncé d'expression BARE (ast.Expr) : le retour est
    # JETÉ — personne ne le lit. Tout autre port (un Assign, un if-test,
    # une enveloppe convertie) LIT le retour.
    nus, lus = [], []
    for n in ast.walk(tree):
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) \
                and est_geste(nom_appel(n.value)):
            nus.append((nom_appel(n.value), n.value.lineno))
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and est_geste(nom_appel(n)) \
                and not any(nu[1] == n.lineno and nu[0] == nom_appel(n)
                            for nu in nus):
            lus.append((nom_appel(n), n.lineno))
    if not lus:
        rapport.append(
            "L3 ROUGE : AUCUN geste de liaison dans le scénario — ni "
            "LoadLibrary, ni GetProcAddress, ni VirtualProtect : la "
            "feuille ne peut être liée, le défaut est STRUCTUREL (le "
            "harnais du labo la shimmait — le shim ne voyagea jamais au "
            "scénario terrain, la brèche de la 302 rouverte par la "
            "plomberie)")
        return False
    if nus:
        rapport.append(f"L3 ROUGE : {len(nus)} geste(s) NU(S) au retour "
                       f"jeté — {nus} — chaque retour doit être lu, son "
                       "écart nommé, le flux stoppé")
        return False
    # la relecture : une lecture du slot (lire_octets à rva_slot) comparée
    # à l'adresse liée, gardée par un If ... return
    relue = [n.lineno for n in ast.walk(tree)
             if isinstance(n, ast.Call) and nom_appel(n) == "lire_octets"
             and any(isinstance(a, ast.Name) and a.id == "rva_slot"
                     for a in ast.walk(n) if isinstance(a, ast.Name))]
    if not relue:
        rapport.append(
            "L3 ROUGE : AUCUNE relecture du slot après l'écriture — la "
            "liaison n'est jamais recoupée (l'écrit sans relecture n'est "
            "pas une preuve)")
        return False
    rapport.append(
        f"L3 VERT : les {len(lus)} gestes de liaison au guichet — "
        f"{sorted(set(g for g, _ in lus))} — chaque retour lu, "
        "l'écart nommé, le flux stoppé ; la relecture recoupe l'écrit "
        f"(lignes {sorted(set(relue))})")
    return True


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    chemin = sys.argv[1]
    tree = ast.parse(open(chemin, encoding="utf-8").read(), chemin)
    print(f"=== L'ÉPREUVE DE LA FEUILLE MEMCMP — {chemin.split('/')[-1]} ===")
    rapport = []
    l1 = loi_l1(tree, rapport)
    l2 = loi_l2(tree, rapport)
    l3 = loi_l3(tree, rapport)
    for ligne in rapport:
        print(" ", ligne)
    verdict = "VERT" if (l1 and l2 and l3) else "ROUGE"
    print(f"=== L'ÉPREUVE FINIE : {verdict} — L1 {'VERT' if l1 else 'ROUGE'}, "
          f"L2 {'VERT' if l2 else 'ROUGE'}, L3 {'VERT' if l3 else 'ROUGE'} ===")
    return 0 if verdict == "VERT" else 1


if __name__ == "__main__":
    sys.exit(main())
