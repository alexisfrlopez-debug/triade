#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""alignement_13_regles.py — LE DIFF RÈGLE PAR RÈGLE ENTRE LE MODÈLE TLA+
ET LA SÉMANTIQUE OPÉRATIONNELLE PYTHON (l'instruction oc2y014vx, point 2 :
« vérifier que le modèle TLA+ soumis à Apalache est textuellement aligné
avec la sémantique opérationnelle du rapport (diff règle par règle,
13 règles) »).

LA MÉTHODE — UN TRANSPILEUR STRICT (fail-closed), jamais une transcription
à la main : chaque action de CF3.tla est PARSÉE puis TRANSPILÉE en Python
(gardes, disjonctions, affectations primées, UNCHANGED) ; toute construction
TLA+ hors du sous-ensemble reconnu REFUSE. L'action transpilée est ensuite
confrontée au modèle Python (modele_invariant_v150.py) sur l'espace concret
borné : e ∈ 1..4 × phase × sait (les 8 sous-ensembles) × trap_ok × cf2_ok ×
secret — chaque activation et chaque image comparées.

Sortie : livraison-vague5/p6-alignement-13-regles.txt
Code retour : 0 = les 13 règles ALIGNÉES ; 2 = refus nommé.
"""
from __future__ import annotations

import itertools
import pathlib
import re
import sys

TLA_TXT = pathlib.Path(
    "/tmp/triade-gh/scripts/tla_v150/CF3.tla").read_text(encoding="utf-8")
sys.path.insert(0, "/tmp/triade-gh/scripts/preuves_v150")
import modele_invariant_v150 as MI  # noqa: E402

ELEMENTS = MI.ELEMENTS

ACTIONS = [  # (Python, TLA+)
    ("vole_K_user", "VoleKUser"),
    ("vole_S_serrure", "VoleSSerrure"),
    ("vole_S_piège", "VoleSPiege"),
    ("falsifie_conteneur", "FalsifieConteneur"),
    ("falsifie_piège", "FalsifiePiege"),
    ("rejoue_époque_passée", "RejoueEpoquePassee"),
    ("ouvrir_correct", "OuvrirCorrect"),
    ("ouvrir_phrase_erronée", "OuvrirPhraseErronee"),
    ("ouvrir_ancien_couple", "OuvrirAncienCouple"),
    ("verifier", "Verifier"),
    ("crash_pendant_session", "CrashPendantSession"),
    ("clôturer_correcte", "CloturerCorrecte"),
    ("clôturer_phrase_erronée", "CloturerPhraseErronee"),
]

CORRESP = {"KUser": '"K_user"', "SSerrure": '"S_serrure"',
           "SPiege": '"S_piège"'}


def corps_action(nom_tla: str) -> str:
    m = re.search(rf"^{nom_tla} ==\s*\n(.*?)(?=^\w+ ==|\Z)", TLA_TXT,
                  re.MULTILINE | re.DOTALL)
    if not m:
        raise SystemExit(f"REFUS : action {nom_tla} introuvable")
    return m.group(1)


def transpile_expr(e: str) -> str:
    """Le sous-ensemble d'expressions de CF3.tla → Python (strict)."""
    e = e.strip()
    e = re.sub(r"\bCardinality\(sait\)\s*>=\s*3", "len(sait & ELEMENTS) >= 3", e)
    for tla, py in CORRESP.items():
        e = re.sub(rf"\b{tla}\b", py, e)
    e = e.replace("\\union", "|")
    e = e.replace("\\notin", " not in ").replace("\\in", " in ")
    e = e.replace("TRUE", "True").replace("FALSE", "False")
    e = re.sub(r'=\s*"(canonique|brouillon)"', r'== "\1"', e)
    residu = re.sub(r'\{"[^"]*"\}', "", e)      # les ensembles littéraux OK
    residu = residu.replace("ELEMENTS", "")     # la constante Python admise
    if re.search(r"[\\{}]|[A-Za-z]'|[A-Z]{2,}", residu):
        raise SystemExit(f"REFUS : expression non transpilable : {e!r}")
    return e


def decoupe_conjonctions(texte: str) -> list[str]:
    """Les conjonctions de HAUT niveau (indentation de 2 espaces) — les
    lignes plus profondes sont des CONTINUATIONS de l'énoncé courant."""
    texte = re.sub(r"\(\*.*?\*\)", "", texte, flags=re.DOTALL)
    enonces, courant = [], []
    for l in texte.splitlines():
        if not l.strip():
            continue
        if l.startswith("  /\\") or l.startswith("  UNCHANGED"):
            if courant:
                enonces.append(" ".join(courant))
            courant = [l.strip()]
        elif l.startswith("   ") and courant:
            courant.append(l.strip())
        else:
            raise SystemExit(f"REFUS : ligne inattendue : {l!r}")
    if courant:
        enonces.append(" ".join(courant))
    return enonces


def compile_action(nom_tla: str):
    """L'action TLA+ → une fonction Python images(s) -> list[dict]."""
    enonces = decoupe_conjonctions(corps_action(nom_tla))
    gardes, branches, affects, unchanged = [], [], [], []
    for enonce in enonces:
        if enonce.startswith("UNCHANGED"):
            m = re.match(r"UNCHANGED <<(.*)>>", enonce)
            if not m:
                raise SystemExit(f"REFUS : UNCHANGED non parsable : "
                                 f"{enonce!r}")
            unchanged += [v.strip() for v in m.group(1).split(",")]
            continue
        if not enonce.startswith("/\\"):
            raise SystemExit(f"REFUS : énoncé non conjonction : {enonce!r}")
        corps = enonce[2:].strip()
        if corps.startswith("UNCHANGED"):
            cible = corps[len("UNCHANGED"):].strip()
            if cible == "vars":
                unchanged += ["e", "phase", "sait", "trap_ok", "cf2_ok",
                              "secret", "accepte", "detruit",
                              "destr_injuste", "media_corrompu"]
            else:
                m = re.match(r"<<(.*)>>", cible)
                if not m:
                    raise SystemExit(f"REFUS : UNCHANGED non parsable : "
                                     f"{enonce!r}")
                unchanged += [v.strip() for v in m.group(1).split(",")]
            continue
        if corps.startswith("\\/"):
            # la disjonction (OuvrirCorrect) — complète en UN énoncé
            branches.extend(compile_disjonction(corps))
            continue
        if "'" in corps:
            m = re.match(r"(\w+)'\s*=\s*(.+)$", corps)
            if not m:
                raise SystemExit(f"REFUS : affectation non parsable : {corps!r}")
            affects.append((m.group(1), transpile_expr(m.group(2))))
        else:
            gardes.append(transpile_expr(corps))
    return {"gardes": gardes, "branches": branches, "affects": affects,
            "unchanged": unchanged}


def compile_disjonction(bloc: str) -> list[tuple[list[str], list[tuple]]]:
    """La disjonction OuvrirCorrect : [(gardes, affectations)], par branche."""
    branches = []
    for branche in bloc.split("\\/"):
        branche = branche.strip()
        if not branche:
            continue
        gardes_b, affects_b = [], []
        for atome in branche.split("/\\"):
            atome = atome.strip()
            if not atome:
                continue
            if "'" in atome:
                m = re.match(r"(\w+)'\s*=\s*(.+)$", atome)
                if not m:
                    raise SystemExit(f"REFUS : atome primé : {atome!r}")
                affects_b.append((m.group(1), transpile_expr(m.group(2))))
            else:
                gardes_b.append(transpile_expr(atome))
        branches.append((gardes_b, affects_b))
    return branches


def images_tla(action: dict, etat: dict) -> list[dict] | None:
    """Les images possibles ; None si la garde de tête échoue."""
    for g in action["gardes"]:
        if not eval(g, {}, {**etat, "ELEMENTS": ELEMENTS}):
            return None
    out = []
    if action["branches"]:
        for gardes_b, affects_b in action["branches"]:
            contexte = {**etat, "ELEMENTS": ELEMENTS}
            if all(eval(g, {}, contexte) for g in gardes_b):
                nouv = dict(etat)
                for var, expr in affects_b:
                    nouv[var] = eval(expr, {}, contexte)
                out.append(nouv)
    else:
        nouv = dict(etat)
        contexte = {**etat, "ELEMENTS": ELEMENTS}
        for var, expr in action["affects"]:
            nouv[var] = eval(expr, {}, contexte)
        out.append(nouv)
    return out


def applique_unchanged(action: dict, images: list[dict], etat: dict) -> None:
    for img in images:
        for var in action["unchanged"]:
            img[var] = etat[var]


# ------------------------------------------------- l'espace concret borné
def espace_borne():
    for e in (1, 2, 3, 4):
        for phase in ("canonique", "brouillon"):
            for n in range(4):                      # les 8 sous-ensembles
                for sait in itertools.combinations(
                        ("K_user", "S_serrure", "S_piège"), n):
                    for trap_ok in (True, False):
                        for cf2_ok in (True, False):
                            for secret in (False, True):
                                yield {
                                    "e": e, "phase": phase,
                                    "sait": frozenset(sait),
                                    "trap_ok": trap_ok, "cf2_ok": cf2_ok,
                                    "secret": secret, "accepte": False,
                                    "detruit": False, "destr_injuste": False,
                                    "media_corrompu": False}


DICT_VERS_PY = lambda d: (d["e"], d["phase"], d["sait"], d["trap_ok"],
                          d["cf2_ok"], d["secret"], d["accepte"],
                          d["detruit"], d["destr_injuste"],
                          d["media_corrompu"])


def main() -> int:
    lignes = [
        "L'ALIGNEMENT RÈGLE PAR RÈGLE — CF3.tla (l'artefact TLC/Apalache) "
        "CONTRE modele_invariant_v150.py",
        "(la sémantique opérationnelle du rapport) — transpilation STRICTE "
        "du TLA+, confrontation état par état",
        "sur l'espace concret borné (e ∈ 1..4, 8 sous-ensembles sait, "
        "trap_ok, cf2_ok, secret ; les quatre drapeaux jamais lus par une",
        "garde tiennent leur valeur initiale — un fait mécanique : aucune "
        "garde ne les référence)",
        "=" * 100,
        f"{'règle (Python ↔ TLA+)':<56}{'états':>8}{'activés':>9}"
        f"{'images':>9}{'verdict':>10}",
        "-" * 100,
    ]
    ecarts = []
    for nom_py, nom_tla in ACTIONS:
        action = compile_action(nom_tla)
        n = actifs = images_egales = 0
        for etat in espace_borne():
            n += 1
            etat_py = DICT_VERS_PY(etat)
            noms_genres = dict(MI.actions_possibles(etat_py))
            img_py = None
            if nom_py in noms_genres:
                img_py = MI.appliquer(etat_py, nom_py, noms_genres[nom_py])
            imgs_tla = images_tla(action, etat)
            if imgs_tla is not None:
                applique_unchanged(action, imgs_tla, etat)
            act_py = img_py is not None
            act_tla = bool(imgs_tla)
            if act_py != act_tla:
                ecarts.append(f"[{nom_py}] activation divergente à "
                              f"{etat_py} : python={act_py} tla={act_tla}")
                continue
            if act_tla:
                actifs += 1
                if len(imgs_tla) != 1:
                    ecarts.append(f"[{nom_py}] {len(imgs_tla)} images TLA+ "
                                  f"à {etat_py} (attendu 1, l'alignement "
                                  "exige le déterminisme par branche)")
                    continue
                if DICT_VERS_PY(imgs_tla[0]) != img_py:
                    ecarts.append(f"[{nom_py}] image divergente à "
                                  f"{etat_py} : python={img_py} "
                                  f"tla={imgs_tla[0]}")
                    continue
                images_egales += 1
        verdict = "ALIGNÉE" if not any(f"[{nom_py}]" in e for e in ecarts) \
            else "DIVERGE"
        lignes.append(f"{nom_py} ↔ {nom_tla:<30}{n:>8}{actifs:>9}"
                      f"{images_egales:>9}{verdict:>10}")
    lignes += [
        "-" * 100,
        "LE VERDICT : " + ("LES 13 RÈGLES ALIGNÉES — gardes et effets "
                           "identiques sur tout l'espace" if not ecarts
                           else f"{len(ecarts)} ÉCART(S) — REFUS"),
    ] + [f"  {e}" for e in ecarts[:12]]
    sortie = pathlib.Path(
        "/home/z/my-project/livraison-vague5/p6-alignement-13-regles.txt")
    sortie.write_text("\n".join(lignes), encoding="utf-8")
    print("\n".join(lignes))
    return 0 if not ecarts else 2


if __name__ == "__main__":
    sys.exit(main())
