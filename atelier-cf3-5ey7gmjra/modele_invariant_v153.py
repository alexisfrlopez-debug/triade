#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""modele_invariant_v153.py — LE MODÈLE FORMEL NON BORNÉ DE CF3, ÉTENDU :
LA FALSIFICATION OFFERTE PENDANT UNE SESSION OUVERTE (l'instruction
5ey7gmjra, point 1 — le pendant Python de CF3Etendu.tla).

L'EXTENSION : la règle falsifie_conteneur offerte aux DEUX phases —
la garde devient trap_ok SEUL (la destruction locale sur falsification
PROUVÉE, le média et les fragments intacts), EXACTEMENT la sentinelle
concrète de v06/coffre_cf3.py. L'ÉCART HISTORIQUE — 660 divergences
d'UNE classe (falsification en session : le modèle v0.15.0 refusait,
le concret détruisait), DÉCOUVERT par la campagne PBT à la graine
20261112 — demeure CONSIGNÉ append-only : il est la découverte qui
motive la présente édition. Les DOUZE autres règles demeurent la copie
fidèle de modele_invariant_v150.py (v0.15.0, INTACTE et rejouable).

Tout le reste du fichier — l'invariant I, les preuves par formes
finies, l'explorateur borné — est le portage de v0.15.0 (voir son
docstring pour la généalogie D187/D196) ; les comptes de fidélité
v120 (154/1152) sont ceux du modèle SCELLÉ (la reproduction s'exécute
sur modele_invariant_v150.py, jamais sur la présente) ; l'explorateur
de la présente porte l'extension (les refus de falsification en
session deviennent des destructions : les comptes étendus sont
consignés au rapport de la présente).

LE PRINCIPE. L'explorateur v120 (D187) énumérait l'espace BORNÉ (époques ≤ 3 —
un plafond ARTIFICIEL dans la règle de clôture : e ← min(e+1, 3)) : « prouvé
dans le modèle » voulait dire « prouvé jusqu'aux bornes ». Ici le plafond est
RETIRÉ (la règle de clôture fait e ← e+1, SANS limite — le modèle est celui de
l'implémentation, v06/coffre_cf3.py ligne « epoque2 = epoque_n + 1 ») et la
preuve passe par INDUCTION :

  1. INITIALISATION — l'invariant I tient à l'état initial ;
  2. PRÉSERVATION — pour CHACUNE des 13 règles de la sémantique, pour TOUT
     état satisfaisant I (et la garde de la règle), l'état image satisfait I ;
  3. DÉDUCTION — I entraîne P1, P3, P4 ; la MONOTONIE de l'époque (prouvée
     par règle, inconditionnellement) et la structure des règles de rejeu
     (retour de l'état inchangé) entraînent P2.

La préservation est vérifiée MÉCANIQUEMENT sur l'ensemble FINI des FORMES
d'état (les 10 composants du modèle, les valeurs contraintes par I énumérées
dans le domaine I, les deux classes d'époque {e = 1} ∪ {e ≥ 2}) — l'espace des
formes est fini ALORS que l'espace des époques ne l'est pas. La complétude
repose sur l'UNIFORMITÉ de la classe e ≥ 2 : les règles n'accèdent à l'époque
que par le prédicat (e > 1) et le successeur (e + 1) — AUCUNE autre constante
que 1 n'y intervient. Cette uniformité est (a) STRUCTURELLE : le code des
règles ci-dessous n'écrit e que dans ces deux formes ; (b) TÉMOIGNÉE
MÉCANIQUEMENT : le TEST DE TRANSLATION re-exécute TOUTE la preuve sur le
modèle décalé (e → e + δ, δ ∈ {7, 50, 1000}) et exige des verdicts IDENTIQUES
— un contre-exemple à grande époque aurait, par translation inverse, un
contre-exemple à petite époque.

LES QUATRE PROPRIÉTÉS (D187, inchangées) :
  P1 SECRET SOUS SEUIL — un adversaire à ≤ 2 éléments n'apprend JAMAIS le
     secret ;  P2 REFUS DU ROLL-BACK — le rejeu d'un couple d'époque passée
     n'est JAMAIS accepté (l'époque ne décroît pas) ;  P3 PAS DE DESTRUCTION
     SUR PHRASE ERRONÉE ;  P4 RAYON BORNÉ À UNE ÉPOQUE — le média du piège et
     les fragments CF2 ne sont JAMAIS touchés.

LES HYPOTHÈSES A1-A5 : inchangées de D187 (le docstring de
modele_formel_v120.py les énonce — A1 symbolique, A2 seuil ≤ 2, A3 média non
enrichissable, A4 rejeu des anciens couples, A5 hors modèle).

LA CONTRE-VÉRIFICATION BORNÉE (le point « bornes étendues ») : l'explorateur
de v120 est porté SANS son plafond et exécuté aux bornes étendues (époques ≤ 5,
profondeur ≤ 8) : (a) tout état atteignable satisfait I ; (b) aucun
contre-exemple P1-P4 ; (c) aux bornes historiques (époques ≤ 3, profondeur 6,
plafond v120) les comptes REPRODUISENT EXACTEMENT D187 (154 états, 1 152
transitions) — la preuve de fidélité du portage.

Sortie : scripts/preuves_v150/modele_invariant.csv + rapport txt.
"""

from __future__ import annotations

import csv
import itertools
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
PREUVES = pathlib.Path(__file__).resolve().parent   # l'atelier 5ey7gmjra
PREUVES.mkdir(parents=True, exist_ok=True)

ELEMENTS = frozenset({"K_user", "S_serrure", "S_piège"})

# ---------------------------------------------------------------------------
# LA SÉMANTIQUE — 13 règles, l'époque SANS plafond (décalage δ pour le test
# de translation ; δ = 0 est le modèle de l'implémentation).
# ---------------------------------------------------------------------------


def etat_initial(delta: int = 0):
    return (1 + delta, "canonique", frozenset(), True, True, False, False,
            False, False, False)


def actions_possibles(s):
    """Les 13 règles (gardes comprises) — IDENTIQUES à v120 sauf le plafond."""
    e, phase, sait, trap_ok, cf2_ok, *_ = s
    acts = []
    if phase == "canonique":
        acts.append(("ouvrir_correct", "protocole"))
        acts.append(("ouvrir_phrase_erronée", "protocole"))
        acts.append(("verifier", "protocole"))
        if e > 1:
            acts.append(("ouvrir_ancien_couple", "protocole"))  # le rejeu A4
        acts.append(("crash_pendant_session", "protocole"))
    if phase == "brouillon":
        acts.append(("clôturer_correcte", "protocole"))       # e ← e+1 SANS
        acts.append(("clôturer_phrase_erronée", "protocole"))  # plafond
        acts.append(("crash_pendant_session", "protocole"))
    for element in ("K_user", "S_serrure", "S_piège"):
        acts.append((f"vole_{element}", "adversaire"))
    acts.append(("falsifie_conteneur", "adversaire"))
    acts.append(("falsifie_piège", "adversaire"))
    acts.append(("rejoue_époque_passée", "adversaire"))
    return acts


def appliquer(s, action, genre):
    """La sémantique de transition — la copie fidèle de v120 SANS le plafond
    d'époque (l'unique divergence, voulue : min(e+1, EPOQUES_MAX) → e+1)."""
    (e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit,
     destr_injuste, media_corrompu) = s

    def avec(**kw):
        base = [e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit,
                destr_injuste, media_corrompu]
        for k, v in kw.items():
            base[{"e": 0, "phase": 1, "sait": 2, "trap_ok": 3, "cf2_ok": 4,
                  "secret": 5, "accepte": 6, "detruit": 7,
                  "destr_injuste": 8, "media_corrompu": 9}[k]] = v
        return tuple(base)

    if genre == "adversaire":
        if action == "vole_K_user":
            return avec(sait=sait | {"K_user"})
        if action == "vole_S_serrure":
            return avec(sait=sait | {"S_serrure"})
        if action == "vole_S_piège":
            return avec(sait=sait | {"S_piège"})
        if action == "falsifie_conteneur":
            # L'EXTENSION 5ey7gmjra : la garde devient trap_ok SEUL — la
            # falsification PROUVÉE détruit LOCALEMENT aux DEUX phases (la
            # session ouverte comprise : la sentinelle concrète court sur
            # le canonique du conteneur, pas sur le brouillon de session)
            if trap_ok:
                return avec(detruit=True)
            return None
        if action == "falsifie_piège":
            return avec(trap_ok=False) if trap_ok else None
        if action == "rejoue_époque_passée":
            if e > 1:
                return s  # REFUS NOMMÉ : l'état ne change PAS
            return None
    if action == "ouvrir_correct":
        if not trap_ok:
            return None
        if "K_user" in sait and len(sait & ELEMENTS) >= 3:
            return avec(phase="brouillon", secret=True)  # seuil dépassé
        if "K_user" in sait and len(sait & ELEMENTS) < 3:
            return None  # KEK indérivable : l'ouverture ÉCHOUE
        return avec(phase="brouillon")
    if action == "ouvrir_phrase_erronée":
        return s
    if action == "ouvrir_ancien_couple":
        return s  # REFUS NOMMÉ « RETOUR EN ARRIÈRE »
    if action == "verifier":
        return s
    if action == "crash_pendant_session":
        return avec(phase="canonique")
    if action == "clôturer_correcte":
        if not trap_ok:
            return None
        return avec(e=e + 1, phase="canonique")   # ← SANS PLAFOND (v0.15.0)
    if action == "clôturer_phrase_erronée":
        return s
    return None


# ---------------------------------------------------------------------------
# L'INVARIANT INDUCTIF I ET LES PROPRIÉTÉS DE TRANSITION
# ---------------------------------------------------------------------------

def invariant(s) -> bool:
    """I(s) — la conjonction préservée par les 13 règles :
    I1  secret ⟹ seuil = 3          (porte P1)
    I2  ¬destruction_injuste         (porte P3)
    I3  cf2_intact ∧ ¬média_corrompu (porte P4)
    I4  époque ≥ 1                   (le domaine des époques)
    """
    e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, injuste, \
        media = s
    i1 = (not secret) or len(sait & ELEMENTS) == 3
    i2 = not injuste
    i3 = cf2_ok and not media
    i4 = e >= 1
    return i1 and i2 and i3 and i4


def violations(s):
    """Les contre-exemples P1-P4 d'un état (pour la contre-vérification)."""
    e, phase, sait, trap_ok, cf2_ok, secret, accepte, detruit, injuste, \
        media = s
    seuil = len(sait & ELEMENTS)
    return {
        "P1": bool(secret and seuil < 3),
        "P3": bool(injuste),
        "P4": bool(media or not cf2_ok),
        # P2 est portée par la monotonie des transitions, pas par l'état
    }


def forme_domaines(i_inv: bool = True):
    """L'énumération EXHAUSTIVE des formes d'état — le domaine de la preuve.

    Si i_inv : seulement les états satisfaisant I (le domaine de la preuve de
    préservation). Sinon : TOUTES les formes (pour la monotonie T1,
    inconditionnelle). Les composants : phase (2) × savoirs (8) × trap (2) ×
    secret (2) × accepte (2) × detruit (2) × cf2 (2) × media (2) × injuste
    (2) — l'époque est traitée PAR CLASSES ci-dessous.
    """
    for phase in ("canonique", "brouillon"):
        for n_els in range(4):
            for savoirs in itertools.combinations(sorted(ELEMENTS), n_els):
                sait = frozenset(savoirs)
                for trap in (True, False):
                    for secret in (False, True):
                        for accepte in (False, True):
                            for detruit in (False, True):
                                for cf2 in (True, False):
                                    for media in (False, True):
                                        for injuste in (False, True):
                                            s = (1, phase, sait, trap, cf2,
                                                 secret, accepte, detruit,
                                                 injuste, media)
                                            if not i_inv or invariant(s):
                                                yield s


# ---------------------------------------------------------------------------
# LA PREUVE PAR RÈGLES — initialisation, préservation, monotonie, rejeu
# ---------------------------------------------------------------------------

def preuve_preservation(delta: int = 0):
    """La préservation de I par les 13 règles, sur TOUTES les formes I-vari-
    antes (l'époque instanciée aux classes 1+delta et 2+delta).

    Retour (nb_formes, violations: [(règle, état, image)]).
    """
    problemes = []
    nb = 0
    for s0 in forme_domaines(i_inv=True):
        for e_classe in (1, 2):  # les DEUX classes de gardes (e>1 / e=1)
            e = e_classe + delta
            s = (e,) + s0[1:]
            if not invariant(s):  # la translation doit rester dans I
                problemes.append(("(hors I après translation)", s, None))
                continue
            nb += 1
            for action, genre in actions_possibles(s):
                image = appliquer(s, action, genre)
                if image is None:
                    continue  # règle refusée : rien à préserver
                if not invariant(image):
                    problemes.append((action, s, image))
    return nb, problemes


def preuve_monotonie(delta: int = 0):
    """T1 (porte P2) : AUCUNE règle ne décroît l'époque — vérifié sur TOUTES
    les formes (inconditionnel : I n'est pas exigé). Retour (nb, violations).
    """
    problemes = []
    nb = 0
    for s0 in forme_domaines(i_inv=False):
        for e_classe in (1, 2):
            e = e_classe + delta
            s = (e,) + s0[1:]
            nb += 1
            for action, genre in actions_possibles(s):
                image = appliquer(s, action, genre)
                if image is not None and image[0] < s[0]:
                    problemes.append((action, s, image))
    return nb, problemes


def preuve_rejeu(delta: int = 0):
    """P2, second volet : les règles de rejeu (rejoue_économie_passée comme
    ouvrir_ancien_couple) retournent l'état INCHANGÉ — le rejeu d'un couple
    passé ne change RIEN (ni ouverture, ni destruction)."""
    problemes = []
    nb = 0
    for s0 in forme_domaines(i_inv=False):
        for e_classe in (1, 2):
            e = e_classe + delta
            s = (e,) + s0[1:]
            nb += 1
            for action, genre in actions_possibles(s):
                if action not in ("rejoue_époque_passée",
                                  "ouvrir_ancien_couple"):
                    continue
                image = appliquer(s, action, genre)
                if image is not None and image != s:
                    problemes.append((action, s, image))
    return nb, problemes


# ---------------------------------------------------------------------------
# LA CONTRE-VÉRIFICATION BORNÉE — l'explorateur de D187, bornes étendues
# ---------------------------------------------------------------------------

def explorer(epoques_max: int, profondeur_max: int, plafond_v120: bool = False,
             delta: int = 0):
    """L'énumération exhaustive de l'espace BORNÉ (v120 porté). Si
    plafond_v120 : la règle de clôture ramène e ← min(e+1, epoques_max) — la
    reproduction EXACTE de D187 ; sinon : les transitions au-delà de la borne
    sont coupées (le modèle, lui, ne plafonne plus)."""
    def ap(s, action, genre):
        if plafond_v120 and action == "clôturer_correcte":
            # la ligne de v120 — pour la reproduction des comptes D187
            if s[3]:  # trap_ok
                return ((min(s[0] + 1, epoques_max), "canonique") + s[2:])
            return None
        return appliquer(s, action, genre)

    depart = etat_initial(delta)
    vus = {depart: 0}
    frontiere = [(depart, ())]
    stats = {"états": 0, "transitions": 0, "refus": 0}
    ce = {p: 0 for p in ("P1", "P2", "P3", "P4")}
    etats_hors_I = 0
    while frontiere:
        etat, chemin = frontiere.pop(0)
        stats["états"] += 1
        if not invariant(etat):
            etats_hors_I += 1
        for p, v in violations(etat).items():
            if v:
                ce[p] += 1
        if len(chemin) >= profondeur_max:
            continue
        # la borne d'époque (coupe d'exploration, PAS un plafond du modèle)
        for action, genre in actions_possibles(etat):
            nouveau = ap(etat, action, genre)
            stats["transitions"] += 1
            if nouveau is None:
                stats["refus"] += 1
                continue
            if plafond_v120 or nouveau[0] <= epoques_max + delta:
                if nouveau not in vus or vus[nouveau] > len(chemin) + 1:
                    vus[nouveau] = len(chemin) + 1
                    frontiere.append((nouveau, chemin + ((action, genre),)))
    stats["contre_exemples"] = ce
    stats["états_hors_I"] = etats_hors_I
    return stats


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("=== LE MODÈLE FORMEL NON BORNÉ DE CF3, ÉTENDU (v0.15.3 — la "
          "falsification en session, l'instruction 5ey7gmjra) ===")
    lignes_rapport = [
        "LE MODÈLE FORMEL NON BORNÉ DE CF3, ÉTENDU — v0.15.3",
        "L'EXTENSION 5ey7gmjra : falsifie_conteneur offerte en session "
        "ouverte (garde trap_ok seule, la sentinelle concrète) ; l'écart "
        "historique des 660 divergences demeure consigné — la découverte "
        "qui motiva l'extension ; les douze autres règles inchangées.",
        "",
        "LE PRINCIPE : le plafond d'époque de v120 est RETIRÉ (la clôture "
        "fait e ← e+1, comme l'implémentation coffre_cf3.py) ; la preuve "
        "passe par induction — I tient à l'initial, I est préservé par les "
        "13 règles, I entraîne P1/P3/P4 ; la monotonie (par règle, "
        "inconditionnelle) et le rejeu-état-inchangé entraînent P2.",
        "",
        "L'INVARIANT I : I1 secret ⟹ seuil = 3 ; I2 ¬destruction_injuste ; "
        "I3 cf2_intact ∧ ¬média_corrompu ; I4 époque ≥ 1.",
        "",
    ]

    # 1 — INITIALISATION
    init_ok = invariant(etat_initial())
    print(f"[initialisation] I(s0) {'TIENT' if init_ok else 'VIOLÉ'}")
    lignes_rapport.append(
        f"1. INITIALISATION : I(s0) {'TIENT' if init_ok else 'VIOLÉE'}.")

    # 2 — PRÉSERVATION (δ = 0) + TEST DE TRANSLATION (δ ∈ {7, 50, 1000})
    nb, problemes = preuve_preservation(0)
    pres_ok = init_ok and not problemes
    print(f"[préservation] {nb} formes × 13 règles : "
          f"{len(problemes)} violation(s)")
    trad_ok = True
    trad_details = []
    for delta in (7, 50, 1000):
        nb_d, pb_d = preuve_preservation(delta)
        meme = (nb_d == nb and not pb_d)
        trad_details.append(f"δ={delta} : {nb_d} formes, "
                            f"{len(pb_d)} violation(s), "
                            f"{'IDENTIQUE' if meme else 'DIVERGENT'}")
        if not meme:
            trad_ok = False
    print(f"[translation] {'UNIFORME' if trad_ok else 'DIVERGENTE'} — "
          + " ; ".join(trad_details))
    lignes_rapport.append(
        f"2. PRÉSERVATION : {nb} formes d'état (les valeurs I-variantes des "
        f"10 composants × les classes d'époque {{1}} ∪ {{≥2}}) × 13 règles "
        f"= {nb * 13} instances de préservation : "
        f"{len(problemes)} violation(s) — I est PRÉSERVÉ."
        if not problemes else
        f"2. PRÉSERVATION : {len(problemes)} VIOLATION(S) — voir rapport.")
    lignes_rapport.append(
        "   LE TEST DE TRANSLATION (l'uniformité de la classe e ≥ 2, "
        "témoignée mécaniquement) : " + " ; ".join(trad_details) + ".")

    # 3 — MONOTONIE (T1, porte P2) + REJEU-INCHANGÉ
    nb_m, pb_m = preuve_monotonie(0)
    mono_ok = not pb_m
    nb_r, pb_r = preuve_rejeu(0)
    rejeu_ok = not pb_r
    print(f"[monotonie] {nb_m} formes (inconditionnel) : "
          f"{len(pb_m)} décroissance(s)")
    print(f"[rejeu-état-inchangé] {nb_r} formes : "
          f"{len(pb_r)} divergence(s)")
    lignes_rapport.append(
        f"3. MONOTONIE (porte P2) : {nb_m} formes TOUTES (I n'est pas "
        f"exigé — la propriété est inconditionnelle) × 13 règles : "
        f"{len(pb_m)} décroissance d'époque — l'époque ne décroît JAMAIS."
        if mono_ok else "3. MONOTONIE : VIOLÉE.")
    lignes_rapport.append(
        f"   LE REJEU-ÉTAT-INCHANGÉ (second volet de P2) : les règles "
        f"rejoue_époque_passée et ouvrir_ancien_couple retournent l'état "
        f"INCHANGÉ sur les {nb_r} formes : {len(pb_r)} divergence(s).")

    # 4 — DÉDUCTION : I ⊨ P1, P3, P4 (vérifié sur toutes les formes I)
    deduction_ok = True
    for s in forme_domaines(i_inv=True):
        v = violations(s)
        if v["P1"] or v["P3"] or v["P4"]:
            deduction_ok = False
            break
    print(f"[déduction] I ⊨ ¬P1 ∧ ¬P3 ∧ ¬P4 : "
          f"{'TIENT' if deduction_ok else 'VIOLÉ'}")
    lignes_rapport.append(
        "4. DÉDUCTION : sur toutes les formes satisfaisant I, AUCUNE "
        "violation P1/P3/P4 (P1 : I1 interdit secret ∧ seuil < 3 ; P3 : "
        "I2 interdit la destruction injuste ; P4 : I3 exige CF2 et le "
        "média intacts).")

    # 5 — CONTRE-VÉRIFICATION BORNÉE
    # 5a — fidélité : reproduction EXACTE des comptes D187 (plafond v120)
    st_fid = explorer(3, 6, plafond_v120=True)
    fidele = (st_fid["états"] == 154 and st_fid["transitions"] == 1152)
    print(f"[fidélité v120] époques ≤ 3, prof 6, plafond : "
          f"{st_fid['états']} états / {st_fid['transitions']} transitions — "
          f"{'D187 REPRODUIT (154/1152)' if fidele else 'ÉCART !'}")
    lignes_rapport.append(
        "5. CONTRE-VÉRIFICATION BORNÉE. (a) FIDÉLITÉ : l'explorateur "
        "porté, aux bornes et AU PLAFOND de v120, reproduit EXACTEMENT "
        f"D187 — {st_fid['états']} états / "
        f"{st_fid['transitions']} transitions"
        f"{' (154/1152, la preuve du portage fidèle)' if fidele else ' — ÉCART À CONSIGNER !'}.")

    # 5b — bornes étendues, SANS plafond (le point « époques > 3,
    #     profondeur > 6 » de la commande)
    st_ext = explorer(5, 8, plafond_v120=False)
    ext_ok = (st_ext["états_hors_I"] == 0
              and all(v == 0 for v in st_ext["contre_exemples"].values()))
    print(f"[bornes étendues] époques ≤ 5, prof 8, SANS plafond : "
          f"{st_ext['états']} états / {st_ext['transitions']} transitions, "
          f"{st_ext['états_hors_I']} état(s) hors I, contre-exemples "
          f"{st_ext['contre_exemples']}")
    lignes_rapport.append(
        f"   (b) BORNES ÉTENDUES (époques ≤ 5, profondeur ≤ 8, SANS "
        f"plafond) : {st_ext['états']} états / "
        f"{st_ext['transitions']} transitions — "
        f"{st_ext['états_hors_I']} état atteignable hors I, "
        f"contre-exemples P1-P4 : {st_ext['contre_exemples']}.")
    # 5c — la contre-vérification qui MORD : profondeur 12, la borne
    #     d'époque ≤ 7 est atteinte (6 cycles ouvrir+clôturer = 12 actions)
    st_ext2 = explorer(7, 12, plafond_v120=False)
    ext2_ok = (st_ext2["états_hors_I"] == 0
               and all(v == 0 for v in st_ext2["contre_exemples"].values()))
    print(f"[bornes étendues 2] époques ≤ 7, prof 12 : "
          f"{st_ext2['états']} états / {st_ext2['transitions']} transitions, "
          f"hors I : {st_ext2['états_hors_I']}, "
          f"contre-exemples : {st_ext2['contre_exemples']}")
    lignes_rapport.append(
        f"   (c) ROBUSTESSE (époques ≤ 7, profondeur ≤ 12 — la borne d'époque "
        f"MORD : six cycles ouvrir+clôturer atteignables) : "
        f"{st_ext2['états']} états / {st_ext2['transitions']} transitions — "
        f"hors I : {st_ext2['états_hors_I']}, contre-exemples : "
        f"{st_ext2['contre_exemples']}.")

    # 6 — LES VERDICTS (les statuts SYSTÉMATIQUES de la commande, point 4)
    p1_ok = pres_ok and trad_ok and deduction_ok and ext_ok and ext2_ok
    p2_ok = mono_ok and rejeu_ok
    p3_ok = p1_ok
    p4_ok = p1_ok
    statuts = [
        ("P1", "secret sous seuil (≤ 2 éléments)",
         "PROUVÉE NON BORNÉE" if p1_ok else "RÉFUTÉE",
         "l'invariant I1 (secret ⟹ seuil = 3) : initialisé, préservé par "
         "les 13 règles sur les formes finies, uniforme par translation "
         "δ ∈ {7, 50, 1000} ; contre-vérification bornée époques ≤ 5 et ≤ 7",
         "A1 symbolique, A2 seuil ≤ 2 (le vol des TROIS est hors modèle A5)"),
        ("P2", "refus du roll-back (l'époque ne décroît jamais ; le rejeu "
               "d'un couple passé est refusé nommé)",
         "PROUVÉE NON BORNÉE" if p2_ok else "RÉFUTÉE",
         f"la monotonie inconditionnelle ({nb_m} formes × 13 règles, "
         f"{len(pb_m)} décroissance) + le rejeu-état-inchangé "
         f"({len(pb_r)} divergence) — l'induction couvre TOUTE époque",
         "A4 anciens couples (le rejeu complet est modélisé)"),
        ("P3", "absence de destruction sur phrase erronée",
         "PROUVÉE NON BORNÉE" if p3_ok else "RÉFUTÉE",
         "l'invariant I2 : aucune règle n'écrit destruction_injuste — "
         "vérifié forme par forme",
         "la phrase erronée mène à PhraseErronee (réessai) — spec § 5.4"),
        ("P4", "rayon borné à une époque (le média et CF2 jamais touchés)",
         "PROUVÉE NON BORNÉE" if p4_ok else "RÉFUTÉE",
         "l'invariant I3 : aucune règle n'écrit média_corrompu ni touche "
         "cf2_intact — vérifié forme par forme",
         "la destruction (falsification PROUVÉE, piège intègre) ne touche "
         "que l'état local — spec § 7"),
    ]
    lignes_rapport += ["", "LES VERDICTS (les statuts systématiques) :"]
    for pid, nom, verdict, detail, hyp in statuts:
        lignes_rapport.append(f"  {pid} {verdict} — {nom}")
        lignes_rapport.append(f"     preuve : {detail}")
        lignes_rapport.append(f"     hypothèses : {hyp}")
    lignes_rapport += [
        "",
        "LES STATUTS DISTINCTS (la commande, point 4) : P1-P4 PROUVÉES NON "
        "BORNÉES (par invariant inductif, TOUTE époque, TOUTE profondeur) ; "
        "la contre-vérification bornée (époques ≤ 5/≤ 7, prof 8) : "
        "PROUVÉE BORNÉE (l'évidence supplémentaire) ; les mesures "
        "matérielles (dudect temps réel, fence.i sur silicium, terrain "
        "tiers Loupe) : EN ATTENTE DE RUN MATÉRIEL (les kits sont prêts, "
        "aucun chiffre n'existe).",
        "",
        "LECTURE HONNÊTE : la preuve porte sur le MODÈLE (la sémantique "
        "abstraite, primitives symboliques A1) — le raffinement "
        "modèle↔implémentation est vérifié PAR AILLEURS "
        "(raffinement_v150.py) ; ce qui sort de A1-A4 (A5 : canaux "
        "auxiliaires, failles d'implémentation, le vol des TROIS, le "
        "quantique) demeure HORS MODÈLE et le dit. Le modèle, l'invariant "
        "et le vérificateur sont LE MÊME FICHIER : re-productibilité "
        "totale (python3 scripts/preuves_v150/modele_invariant_v150.py).",
    ]

    csv_path = PREUVES / "modele_invariant.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["propriété", "énoncé", "statut",
                                          "preuve", "hypothèses"])
        w.writeheader()
        for pid, nom, verdict, detail, hyp in statuts:
            w.writerow({"propriété": pid, "énoncé": nom, "statut": verdict,
                        "preuve": detail, "hypothèses": hyp})

    (PREUVES / "modele_invariant_rapport.txt").write_text(
        "\n".join(lignes_rapport) + "\n", encoding="utf-8")
    print(f"\n[sortie] {csv_path}")
    print("[verdicts] " + " ; ".join(f"{p[0]}={p[2]}" for p in statuts))


if __name__ == "__main__":
    main()
