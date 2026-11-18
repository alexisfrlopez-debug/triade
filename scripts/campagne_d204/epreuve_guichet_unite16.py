#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_guichet_unite16.py — L'ÉPREUVE DU GUICHET, née au correctif du
refus nommé de l'unité 04 D210 (la règle de la 304 étendue au premier
terrain à état) : la DÉCOUVERTE du guichet REJOUÉE AU LABO contre le
fichier livré — le code VERBATIM extrait par AST (les gestes Windows
neutralisés au contexte seul, JAMAIS le code touché).

LES TROIS LOIS (le miroir des lois de la 304, étendues à la famille) :
  L1 LA DÉCOUVERTE PAR LES PLAGES FT (la doctrine D54, l'Entrée 210) : la
     marche rejoint le séparateur NULL de chaque plage, chaque entrée sur
     disque == le RVA hint/nom de SA feuille — les feuilles mortes
     comprises — ET la LISTE FERMÉE des notations (les appels IAT déclarés
     aux en-têtes « Déplacements RIP » de loupe-16 et loupe-02, filtrés à
     la fenêtre IAT du plan) TOUTE entière découverte, la voulue du
     scénario la COUVRANT par ses noms — le guichet lie EXACTEMENT les
     slots que les notations appellent ;
  L2 LA LIAISON AVANT TOUT APPEL : lier_feuilles précède la construction
     SAISIR au flux de main() (le texte livré lu, statique) ;
  L3 LE GUICHET FAIL-CLOSED : les refus NOMMÉS présents (RVA-HORS-
     SECTIONS, L1-FEUILLE-INTROUVABLE, L3-GETPROCADDRESS, L3-VIRTUALPROTECT,
     L3-REPROTECTION, L3-RELECTURE).

CONTRE LE v1 : ROUGE — le refus RECONSTITUÉ au labo MOT POUR MOT (« la
RVA 0x0 hors des sections »). CONTRE LE v2 : VERT.

Usage : python3 scripts/campagne_d204/epreuve_guichet_unite16.py
(les chemins par défaut : le kit v1 et le kit v2 du bac de l'unité 04)
"""

import ast
import pathlib
import struct
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
CAMP = pathlib.Path(__file__).resolve().parent

KIT_V1 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118"
KIT_V2 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v2"
NOTATION_16 = KIT_V2 / "notation-loupe-16-saisie.asm"
NOTATION_02 = REPO / "loupe" / "notation" / "loupe-02-lire.asm"
TERRAIN = CAMP / "depot-run-unite16-d210-350" / "epreuves" / \
    "run-console-unite16-d210-20261118-121219.txt"

IAT_BORNES = (0x3100, 0x3240)     # la fenêtre IAT du plan (layout.py)


class RefusCapture(Exception):
    """le refus du guichet capturé — JAMAIS exécuté, JAMAIS masqué."""

    def __init__(self, nom: str, detail: str):
        super().__init__(f"[REFUS] {nom} : {detail}")
        self.nom = nom
        self.detail = detail


# ---------------------------------------------------------------- l'extraction

def extraire(source: str):
    """ra_of + le bloc découverte + la voulue — VERBATIM, par AST."""
    module = ast.parse(source)
    ra_of_def = lier = None
    for noeud in module.body:
        if isinstance(noeud, ast.FunctionDef):
            if noeud.name == "ra_of":
                ra_of_def = noeud
            elif noeud.name == "lier_feuilles":
                lier = noeud
    if ra_of_def is None or lier is None:
        raise SystemExit("[ROUGE] le scénario livré ne porte pas "
                         "ra_of/lier_feuilles — l'épreuve refuse")
    corps = lier.body
    debut = fin = None
    for k, st in enumerate(corps):
        if isinstance(st, ast.Assign) and any(
                getattr(t, "id", None) == "exe" for t in st.targets):
            if any(isinstance(sous, ast.Call)
                   and getattr(sous.func, "id", None) == "open"
                   and getattr(sous.args[0], "id", None) == "EXE"
                   for sous in ast.walk(st.value)):
                debut = k
        if isinstance(st, ast.Assign) and any(
                getattr(t, "id", None) == "voulues" for t in st.targets):
            fin = k
            break
    if debut is None or fin is None:
        raise SystemExit("[ROUGE] le bloc découverte introuvable — "
                         "l'épreuve refuse")
    return module, ra_of_def, corps[debut:fin], corps[fin]


def rejoue(chemin_scenario: pathlib.Path, chemin_exe: pathlib.Path):
    """la découverte rejouée — le code VERBATIM, le contexte du labo."""
    source = chemin_scenario.read_text(encoding="utf-8")
    module, ra_of_def, bloc, voulues_assign = extraire(source)
    contexte = {"struct": struct, "EXE": str(chemin_exe), "open": open}

    def refus(nom, detail):
        raise RefusCapture(nom, detail)

    contexte["refus"] = refus
    exec(compile(ast.Module(body=[ra_of_def], type_ignores=[]),
                 str(chemin_scenario), "exec"), contexte)
    exec(compile(ast.Module(body=list(bloc), type_ignores=[]),
                 str(chemin_scenario), "exec"), contexte)
    voulues = eval(compile(ast.Expression(body=voulues_assign.value),
                           str(chemin_scenario), "eval"), contexte)
    return contexte["feuilles"], voulues, source


# ---------------------------------------------------------------- les lois

def cibles_rip_iat(chemin_notation: pathlib.Path) -> set:
    """les cibles [rip] de la notation, filtrées à la fenêtre IAT du plan."""
    cibles = set()
    for ligne in chemin_notation.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne.startswith(";") or "=" not in ligne:
            continue
        try:
            cible = int(ligne.split("=")[-1].strip(), 16)
        except ValueError:
            continue
        if IAT_BORNES[0] <= cible < IAT_BORNES[1]:
            cibles.add(cible)
    return cibles


def loi_l2(source: str) -> bool:
    """lier_feuilles AVANT la construction SAISIR au flux de main()."""
    module = ast.parse(source)
    appel_g = saisir = None
    for noeud in module.body:
        if isinstance(noeud, ast.FunctionDef) and noeud.name == "main":
            for st in ast.walk(noeud):
                if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call) \
                        and getattr(st.value.func, "id", None) == "lier_feuilles":
                    appel_g = st.lineno
                if isinstance(st, ast.Assign) and any(
                        getattr(t, "id", None) == "SAISIR" for t in st.targets):
                    saisir = st.lineno
    return appel_g is not None and saisir is not None and appel_g < saisir


def loi_l3(source: str) -> list:
    """les refus NOMMÉS présents au guichet (lier_feuilles + ra_of)."""
    noms = set()
    module = ast.parse(source)
    for noeud in module.body:
        if isinstance(noeud, ast.FunctionDef) \
                and noeud.name in ("lier_feuilles", "ra_of"):
            for st in ast.walk(noeud):
                if isinstance(st, ast.Call) \
                        and getattr(st.func, "id", None) == "refus":
                    noms.add(st.args[0].value)
    return sorted(noms)


# ---------------------------------------------------------------- l'épreuve

def eprouve(edition: str, chemin_scenario: pathlib.Path,
            chemin_exe: pathlib.Path) -> tuple:
    verts, rouges, detail = [], [], []

    def vert(nom, ligne=""):
        verts.append(nom)
        print(f"[VERT] {nom}" + (f" — {ligne}" if ligne else ""))

    def rouge(nom, ligne=""):
        rouges.append(nom)
        print(f"[ROUGE] {nom}" + (f" — {ligne}" if ligne else ""))

    print(f"=== L'ÉPREUVE DU GUICHET — CONTRE LE {edition} "
          f"({chemin_scenario.parent.name}) ===")
    cibles = {}
    for nom_f, chemin in (("loupe-16", NOTATION_16), ("loupe-02", NOTATION_02)):
        cibles[nom_f] = cibles_rip_iat(chemin)
        print(f"  [notation {nom_f}] les appels IAT déclarés : "
              f"{sorted(hex(c) for c in cibles[nom_f])}")
    toutes_cibles = cibles["loupe-16"] | cibles["loupe-02"]

    try:
        feuilles, voulues, source = rejoue(chemin_scenario, chemin_exe)
    except RefusCapture as exc:
        refus_reconstitue = f"[REFUS] {exc.nom} : {exc.detail} — RIEN ne court, le guichet ferme"
        ligne_terrain = ""
        if TERRAIN.exists():
            for l in TERRAIN.read_text(encoding="utf-8",
                                        errors="replace").splitlines():
                if l.startswith("[REFUS]"):
                    ligne_terrain = l
                    break
        identique = refus_reconstitue == ligne_terrain
        rouge("L1:la-decouverte-par-les-plages-ft",
              f"le refus RECONSTITUÉ au labo « {exc.nom} : {exc.detail} »"
              + (" — IDENTIQUE mot pour mot à la console du terrain"
                 if identique else ""))
        print(f"    reconstitué : {refus_reconstitue}")
        if ligne_terrain:
            print(f"    terrain     : {ligne_terrain}")
        source = chemin_scenario.read_text(encoding="utf-8")
        vert("L2:la-liaison-avant-tout-appel") if loi_l2(source) \
            else rouge("L2:la-liaison-avant-tout-appel")
        attends = {"RVA-HORS-SECTIONS", "L1-FEUILLE-INTROUVABLE",
                   "L3-GETPROCADDRESS", "L3-VIRTUALPROTECT",
                   "L3-REPROTECTION", "L3-RELECTURE"}
        noms3 = loi_l3(source)
        (vert if set(noms3) == attends else rouge)(
            "L3:le-guichet-fail-closed",
            f"{len(noms3)} refus nommés : {', '.join(noms3)}")
        print(f"[VERDICT {edition}] {len(verts)} VERT, {len(rouges)} ROUGE"
              f"{' — LE REFUS RECONSTITUÉ, L\'ÉPREUVE QUI MANQUAIT' if rouges else ''}")
        return verts, rouges

    feuilles_par_slot = {slot: cle for cle, slot in feuilles.items()}
    marche = sum(1 for _ in feuilles)
    vert("L1:la-decouverte-par-les-plages-ft",
          f"la marche a joint les séparateurs NULL : {marche} feuilles "
          f"découvertes (les mortes comprises)")
    manquantes = [c for c in toutes_cibles if c not in feuilles_par_slot]
    if manquantes:
        rouge("L1:les-appels-des-notations-couverts",
              f"les cibles {sorted(hex(c) for c in manquantes)} HORS du "
              f"marché du guichet")
    else:
        vert("L1:les-appels-des-notations-couverts",
             "chaque cible [rip] des notations EST un slot découvert")
    non_liees = []
    for c in sorted(toutes_cibles):
        cle = feuilles_par_slot.get(c)
        if cle and cle not in voulues:
            non_liees.append((hex(c), cle[1]))
    if non_liees:
        rouge("L1:la-voulue-couvre-la-liste-fermee",
              f"les feuilles {non_liees} appelées par les notations mais "
              f"JAMAIS liées par le guichet — la classe de la 304")
    else:
        vert("L1:la-voulue-couvre-la-liste-fermee",
             "la voulue couvre TOUTE la liste fermée des notations — "
             "le guichet lie exactement les slots appelés")
    for c in sorted(toutes_cibles):
        cle = feuilles_par_slot.get(c)
        if cle:
            marque = " (liée)" if cle in voulues else " (NON liée)"
            print(f"    {hex(c)} → {cle[1]}@{cle[0]}{marque}")

    (vert if loi_l2(source) else rouge)("L2:la-liaison-avant-tout-appel")
    attends = {"RVA-HORS-SECTIONS", "L1-FEUILLE-INTROUVABLE",
               "L3-GETPROCADDRESS", "L3-VIRTUALPROTECT",
               "L3-REPROTECTION", "L3-RELECTURE"}
    noms3 = loi_l3(source)
    (vert if set(noms3) == attends else rouge)(
        "L3:le-guichet-fail-closed",
        f"{len(noms3)} refus nommés : {', '.join(noms3)}")
    print(f"[VERDICT {edition}] {len(verts)} VERT, {len(rouges)} ROUGE"
          f"{' — TOUT VERT' if not rouges else ''}")
    return verts, rouges


def main() -> int:
    v1v, v1r = eprouve("v1", KIT_V1 / "scenario-unite16.py", KIT_V1 / "loupe.exe")
    print()
    v2v, v2r = eprouve("v2", KIT_V2 / "scenario-unite16.py", KIT_V2 / "loupe.exe")
    print()
    print(f"[BILAN] v1 : {len(v1v)} VERT {len(v1r)} ROUGE — l'épreuve qui "
          f"aurait arrêté la faute AVANT le terrain ; "
          f"v2 : {len(v2v)} VERT {len(v2r)} ROUGE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
