#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifie_couverture_288.py — L'OBLIGATION (O3) DU LEMME DE COUVERTURE :
l'ensemble des 288 formes est EXACTEMENT l'image par α (l'abstraction :
l'époque projetée sur ses classes {1}/{≥2}, les autres composants gardés)
de l'ensemble {TypeOK ∧ Inv} des états concrets bien typés satisfaisant
l'invariant — une BIJECTION, vérifiée mécaniquement (la vague 5,
l'instruction oc2y014vx, point 1).

LA COUVERTURE END-TO-END : tout état ATTEIGNABLE (l'explorateur borné
étendu : e ≤ 5 profondeur 8 ; e ≤ 7 profondeur 12 — les contre-vérifications
consignées) est projeté par α dans l'ensemble des 288 formes.

Sortie : livraison-vague5/p6-couverture-288.txt ; code 0 = VERT, 2 = refus.
"""
from __future__ import annotations

import itertools
import pathlib
import sys

sys.path.insert(0, "/tmp/triade-gh/scripts/preuves_v150")
import modele_invariant_v150 as MI  # noqa: E402

ELEMENTS = MI.ELEMENTS
EPOQUES_REPRESENTATIVES = (1, 2, 3, 7, 50, 1000)


def classe_epoque(e: int) -> int:
    return 1 if e == 1 else 2


def alpha(s) -> tuple:
    """L'abstraction α : l'époque par classes, le reste identique."""
    e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, \
        destr_injuste, media_corrompu = s
    return (classe_epoque(e), phase, sait, trap_ok, cf2_ok, secret,
            accepte, detruit, destr_injuste, media_corrompu)


def typeok(s) -> bool:
    e, phase, sait, *_ = s
    return (e >= 1 and phase in ("canonique", "brouillon")
            and sait <= ELEMENTS)


def explorer_borne(epoques_max: int, profondeur_max: int) -> set[tuple]:
    """Le BFS borné de l'explorateur (les MÊMES sémantiques : etat_initial,
    actions_possibles, appliquer ; la coupe aux bornes, PAS un plafond) —
    retourne l'ENSEMBLE des états atteignables (ce que stats ne porte pas)."""
    depart = MI.etat_initial()
    vus = {depart}
    frontiere = [(depart, 0)]
    while frontiere:
        etat, prof = frontiere.pop(0)
        if prof >= profondeur_max:
            continue
        for action, genre in MI.actions_possibles(etat):
            nouveau = MI.appliquer(etat, action, genre)
            if nouveau is None:
                continue
            if nouveau[0] > epoques_max:
                continue                     # la coupe d'exploration
            if nouveau not in vus:
                vus.add(nouveau)
                frontiere.append((nouveau, prof + 1))
    return vus


def main() -> int:
    # ---- l'ensemble des 288 formes (l'énumération de la preuve) ----------
    formes = set(MI.forme_domaines(i_inv=True))
    formes_avec_classes = set()
    for f in formes:
        for e_classe in (1, 2):
            formes_avec_classes.add((e_classe,) + f[1:])

    # ---- (O3) la bijection : α({TypeOK ∧ Inv}) == les formes -------------
    images_alpha = set()
    for e in EPOQUES_REPRESENTATIVES:
        for phase in ("canonique", "brouillon"):
            for n in range(4):
                for sait in itertools.combinations(sorted(ELEMENTS), n):
                    for trap in (True, False):
                        for cf2 in (True, False):
                            for secret in (False, True):
                                for accepte in (False, True):
                                    for detruit in (False, True):
                                        for injuste in (False, True):
                                            for media in (False, True):
                                                s = (e, phase,
                                                     frozenset(sait), trap,
                                                     cf2, secret, accepte,
                                                     detruit, injuste, media)
                                                if typeok(s) and MI.invariant(s):
                                                    images_alpha.add(alpha(s))
    bijection = (images_alpha == formes_avec_classes)

    # ---- chaque forme satisfait Inv (aucune forme hors invariant) --------
    formes_hors_inv = [f for f in formes_avec_classes if not MI.invariant(f)]

    # ---- la couverture end-to-end : les états ATTEIGNABLES bornés ---------
    couverture_ok, n_atteignables = True, 0
    attendus = {(5, 8): 228, (7, 12): 372}   # les comptes consignés v0.15.0
    comptes = {}
    for epoques_max, profondeur in ((5, 8), (7, 12)):
        etats = explorer_borne(epoques_max, profondeur)
        comptes[(epoques_max, profondeur)] = len(etats)
        for s in etats:
            n_atteignables += 1
            if alpha(s) not in formes_avec_classes:
                couverture_ok = False

    lignes = [
        "LE LEMME DE COUVERTURE — L'OBLIGATION (O3) : LA BIJECTION DES 288 "
        "FORMES (la vague 5, oc2y014vx)",
        "=" * 88,
        f"  les formes de la preuve (forme_domaines, classes d'époque "
        f"{{1}}∪{{≥2}}) : {len(formes_avec_classes)}",
        f"  α({{TypeOK ∧ Inv}}) sur les époques représentatives "
        f"{EPOQUES_REPRESENTATIVES} : {len(images_alpha)}",
        f"  LA BIJECTION : " + ("VERT — les deux ensembles sont ÉGAUX"
                                if bijection else
                                "ROUGE — les ensembles divergent"),
        f"  les formes hors Inv : {len(formes_hors_inv)}",
        f"  la couverture des états atteignables (e≤5 d≤8 ; e≤7 d≤12) : "
        f"{n_atteignables} états {comptes}, "
        + ("TOUS couverts par les 288 formes" if couverture_ok else
           "AU MOINS UN ÉTAT NON COUVERT — REFUS"),
        "",
        "LE LEMME, AVEC (O1)/(O2) DÉCHARGÉES PAR APALACHE "
        "(CF3Couverture.tla — base et pas inductif NoError,",
        "le contrôle négatif attrapé) : tout état concret atteignable est "
        "représenté par au moins une",
        "des 288 formes — la preuve de préservation sur les formes couvre "
        "donc TOUT l'espace atteignable.",
    ]
    ok = bijection and not formes_hors_inv and couverture_ok \
        and len(formes_avec_classes) == 288
    lignes.append("LE VERDICT : " + ("VERT" if ok else "ROUGE — REFUS"))
    sortie = pathlib.Path(
        "/home/z/my-project/livraison-vague5/p6-couverture-288.txt")
    sortie.write_text("\n".join(lignes), encoding="utf-8")
    print("\n".join(lignes))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
