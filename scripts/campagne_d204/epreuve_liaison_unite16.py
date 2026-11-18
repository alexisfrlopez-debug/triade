#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_liaison_unite16.py — L'ÉPREUVE DE LA LIAISON, née au correctif du
crash nommé de l'unité 04 D210 (le run v2 du 18/11 14:09 : « TypeError: this
function takes at least 3 arguments (2 given) » — la liaison memmove à DEUX
arguments) : la PLOMBERIE DE LA LIAISON EXÉCUTÉE AU LABO contre le fichier
livré — le bloc de liaison VERBATIM extrait par AST (les gestes Windows
neutralisés au contexte seul, JAMAIS le code touché ; le memmove et la
relecture string_at RÉELS — la forme de l'appel éprouvée pour de vrai).

LA QUATRIÈME LOI (L4 — le complément de l'épreuve du guichet, née à la 350 :
celle-ci éprouvait la DÉCOUVERTE, la plomberie Windows-seule n'avait jamais
couru au labo — la brèche nommée) :
  L4 LA LIAISON ÉPOUVÉE : le bloc de liaison (du « for cle in voulues » au
     consigne final) EXÉCUTÉ VERBATIM au contexte neutre — chaque feuille
     ÉCRITE par le memmove du fichier même, RELUE par le string_at du
     fichier même, l'égalité recoupée ; l'appel d'une mauvaise arité est
     un ROUGE NOMMÉ au premier geste.

  Et l'AUDIT D'ARITÉ (le miroir statique) : chaque appel ctypes.memmove et
  ctypes.memset du scénario porte TROIS arguments (dst, src, compte) —
  chaque ctypes.string_at en porte DEUX.

CONTRE LE v2 : ROUGE — le TypeError RECONSTITUÉ au labo MOT POUR MOT (« this
function takes at least 3 arguments (2 given) » == la ligne de la console du
terrain). CONTRE LE v3 : VERT.

Usage : python3 scripts/campagne_d204/epreuve_liaison_unite16.py
(les chemins par défaut : le kit v2 et le kit v3 du bac de l'unité 04)
"""

import ast
import ctypes
import pathlib
import struct
import sys
import types

REPO = pathlib.Path(__file__).resolve().parents[2]
CAMP = pathlib.Path(__file__).resolve().parent

KIT_V2 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v2"
KIT_V3 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v3"
TERRAIN = CAMP / "depot-run-unite16-d210-v2-351" / "epreuves" / \
    "run-console-unite16-d210-20261118-140903.txt"


class RefusCapture(Exception):
    """le refus du guichet capturé — JAMAIS exécuté, JAMAIS masqué."""

    def __init__(self, nom: str, detail: str):
        super().__init__(f"[REFUS] {nom} : {detail}")
        self.nom = nom
        self.detail = detail


# ---------------------------------------------------------------- l'extraction

def extraire(source: str):
    """ra_of + le bloc découverte + la voulue + LE BLOC DE LIAISON — VERBATIM."""
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
    return module, ra_of_def, corps[debut:fin], corps[fin], corps[fin + 1:]


def rejoue_et_lie(chemin_scenario: pathlib.Path, chemin_exe: pathlib.Path):
    """la découverte rejouée PUIS LA LIAISON EXÉCUTÉE — le code VERBATIM,
    le contexte neutre du labo (le memmove et le string_at RÉELS)."""
    source = chemin_scenario.read_text(encoding="utf-8")
    module, ra_of_def, bloc, voulues_assign, liaison = extraire(source)

    # le contexte de la découverte (le miroir de l'épreuve du guichet)
    ctx = {"struct": struct, "EXE": str(chemin_exe), "open": open}

    def refus(nom, detail):
        raise RefusCapture(nom, detail)

    ctx["refus"] = refus
    exec(compile(ast.Module(body=[ra_of_def], type_ignores=[]),
                 str(chemin_scenario), "exec"), ctx)
    exec(compile(ast.Module(body=list(bloc), type_ignores=[]),
                 str(chemin_scenario), "exec"), ctx)
    voulues = eval(compile(ast.Expression(body=voulues_assign.value),
                           str(chemin_scenario), "eval"), ctx)
    feuilles = ctx["feuilles"]

    # LE CONTEXTE NEUTRE DE LA LIAISON : un VRAI tampon pour les adresses,
    # les gestes Windows neutralisés au contexte seul — le memmove, le
    # unpack et le string_at DU FICHIER MÊME, RÉELS
    tampon = ctypes.create_string_buffer(0x4000)
    base = ctypes.addressof(tampon)

    class _Bibliotheque:
        def __init__(self, dll):
            self._dll = dll

        def __getattr__(self, nom):
            for cle in voulu_par_nom:
                if cle[1] == nom:
                    return ctypes.c_void_p(0x00007FFA00000000
                                           + (voulu_par_nom.index(cle) + 1))
            raise AttributeError(nom)

    voulues_liste = sorted(voulues)
    voulu_par_nom = list(voulues)

    ctypes_neutre = types.SimpleNamespace(
        WinDLL=lambda dll: _Bibliotheque(dll),
        cast=ctypes.cast, c_void_p=ctypes.c_void_p, byref=ctypes.byref,
        memmove=ctypes.memmove, string_at=ctypes.string_at,
        get_last_error=getattr(ctypes, "get_last_error", lambda: 0))
    ctx_liaison = {
        "struct": struct, "ctypes": ctypes_neutre, "refus": refus,
        "base": base, "feuilles": feuilles, "voulues": voulues,
        "wt": types.SimpleNamespace(DWORD=ctypes.c_uint32),
        "k32": types.SimpleNamespace(
            VirtualProtect=lambda *a: 1),
        "PAGE_RW": 0x40,
        "consigne": lambda msg: messages.append(msg),
    }
    messages = []
    exec(compile(ast.Module(body=list(liaison), type_ignores=[]),
                 str(chemin_scenario), "exec"), ctx_liaison)
    return feuilles, voulues, messages, source


# ---------------------------------------------------------------- l'audit statique

def audit_arite(source: str) -> tuple:
    """chaque memmove/memset à TROIS arguments, chaque string_at à DEUX."""
    attendus = {"memmove": 3, "memset": 3, "string_at": 2}
    fautes, comptes = [], {}
    module = ast.parse(source)
    for st in ast.walk(module):
        if isinstance(st, ast.Call) and isinstance(st.func, ast.Attribute):
            if st.func.attr in attendus and isinstance(st.func.value, ast.Name) \
                    and st.func.value.id == "ctypes":
                n = len(st.args)
                comptes[st.func.attr] = comptes.get(st.func.attr, 0) + 1
                if n != attendus[st.func.attr]:
                    fautes.append((st.func.attr, n, st.lineno))
    return fautes, comptes


# ---------------------------------------------------------------- l'épreuve

def ligne_terrain() -> str:
    if TERRAIN.exists():
        for l in TERRAIN.read_text(encoding="utf-8", errors="replace").splitlines():
            if l.startswith("TypeError:"):
                return l
    return ""


def eprouve(edition: str, chemin_scenario: pathlib.Path,
            chemin_exe: pathlib.Path) -> tuple:
    verts, rouges = [], []

    def vert(nom, ligne=""):
        verts.append(nom)
        print(f"[VERT] {nom}" + (f" — {ligne}" if ligne else ""))

    def rouge(nom, ligne=""):
        rouges.append(nom)
        print(f"[ROUGE] {nom}" + (f" — {ligne}" if ligne else ""))

    print(f"=== L'ÉPREUVE DE LA LIAISON — CONTRE LE {edition} "
          f"({chemin_scenario.parent.name}) ===")
    source = chemin_scenario.read_text(encoding="utf-8")

    # l'audit d'arité d'abord (le miroir statique)
    fautes, comptes = audit_arite(source)
    arite = (", ".join(f"{k} ×{v}" for k, v in sorted(comptes.items()))
             or "aucun appel")
    if fautes:
        detail = "; ".join(f"{a} à {n} arguments ligne {l}" for a, n, l in fautes)
        rouge("L4:l-audit-d-arite", f"{detail} ({arite})")
    else:
        vert("L4:l-audit-d-arite",
             f"chaque appel porte son compte ({arite})")

    # puis l'exécution VERBATIM de la liaison
    try:
        feuilles, voulues, messages, _ = rejoue_et_lie(chemin_scenario,
                                                      chemin_exe)
    except RefusCapture as exc:
        rouge("L4:la-liaison-eprouvee",
              f"le refus reconstitué « [REFUS] {exc.nom} : {exc.detail} »")
        print(f"[VERDICT {edition}] {len(verts)} VERT, {len(rouges)} ROUGE")
        return verts, rouges
    except TypeError as exc:
        reconstitue = f"TypeError: {exc}"
        terrain = ligne_terrain()
        identique = reconstitue == terrain
        rouge("L4:la-liaison-eprouvee",
              f"le TypeError RECONSTITUÉ « {exc} »"
              + (" — IDENTIQUE mot pour mot à la console du terrain"
                 if identique else ""))
        print(f"    reconstitué : {reconstitue}")
        if terrain:
            print(f"    terrain     : {terrain}")
        print(f"[VERDICT {edition}] {len(verts)} VERT, {len(rouges)} ROUGE"
              " — LE CRASH RECONSTITUÉ, L'ÉPREUVE QUI MANQUAIT")
        return verts, rouges

    liees = sum(1 for cle in voulues if cle in feuilles)
    if messages and liees == len(voulues) and len(voulues) == 4:
        vert("L4:la-liaison-eprouvee",
             f"les {liees} feuilles ÉCRITES par le memmove du fichier même, "
             f"RELUES par son string_at, l'égalité recoupée — "
             f"« {messages[-1][:60]}… »")
    else:
        rouge("L4:la-liaison-eprouvee",
              f"la liaison ne porta pas ses feuilles ({liees}/{len(voulues)})")
    print(f"[VERDICT {edition}] {len(verts)} VERT, {len(rouges)} ROUGE"
          f"{' — TOUT VERT' if not rouges else ''}")
    return verts, rouges


def main() -> int:
    if not KIT_V3.exists():
        print("[ÉPREUVE] le kit v3 n'existe pas encore — l'épreuve attend "
              "le constructeur")
        return 1
    v2v, v2r = eprouve("v2", KIT_V2 / "scenario-unite16.py", KIT_V2 / "loupe.exe")
    print()
    v3v, v3r = eprouve("v3", KIT_V3 / "scenario-unite16.py", KIT_V3 / "loupe.exe")
    print()
    print(f"[BILAN] v2 : {len(v2v)} VERT {len(v2r)} ROUGE — l'épreuve qui "
          f"aurait arrêté la faute AVANT le terrain ; "
          f"v3 : {len(v3v)} VERT {len(v3r)} ROUGE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
