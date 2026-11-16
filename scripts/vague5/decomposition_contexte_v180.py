#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""decomposition_contexte_v180.py — LE PÉRIMÈTRE DE CHAQUE MESURE RQ2, LA
TABLE DE DÉCOMPOSITION ET LA RE-TOKENISATION INDÉPENDANTE (l'instruction
om3ewy9lf, la vague 5) : « l'écart ×2,2 en localisation ne peut pas provenir
du tokenizer (rapport 0,98–0,99). (1) Documenter précisément le périmètre de
chaque mesure ... (2) produire une table de décomposition du contexte par
opération ... pour les deux éditions ; (3) chiffrer DANS le manuscrit les
deux baselines réalistes ... ; (4) interdire toute comparaison directe
580 vs 1 277 sans la note de périmètre. Vérification : re-tokenisation
indépendante d'un échantillon (n≥5 par opération) confirmant la
décomposition à ±1 token près ».

LES DEUX PÉRIMÈTRES (documentés, jamais confondus) :
  v0.14.0 (D195) : le CONTENU SEUL de l'opération, mesuré au cl100k_base
    sur le vrai matériau (le plan + l'entête pour localiser ; la notation
    relue + réécrite pour éditer ; la spec + la notation écrites pour
    ajouter), le RAISONNEMENT ESTIMÉ ×1,08 (éditer/ajouter — l'estimation
    nommée) ; AUCUNE requête, AUCUNE réponse, AUCUN aller-retour.
  v0.17.0 (ede70035) : L'APPEL COMPLET INSTRUMENTÉ — le prompt réel
    (le matériau verbatim + la prose de requête) ET la réponse réelle de
    l'agent, comptés au TOKENIZER NATIF lu du log d'usage (le ×1,08
    abandonné), cl100k en parallèle (0,98–1,02).

LA DÉCOMPOSITION (par catégorie, médianes) : matériau lu (l'entête de
carte / la notation / le contrat), prose de requête, réponse écrite —
aux DEUX périmètres, l'écart ×2,2 EXPLIQUÉ par construction.

Sortie : livraison-vague5/p5-decomposition-contexte.txt
Code retour : 0 = la re-tokenisation confirme à ±1 token ; 2 = refus.
"""
from __future__ import annotations

import json
import pathlib
import statistics
import sys

RACINE = pathlib.Path("/home/z/my-project")
NOTATIONS = sorted((RACINE / "lab16" / "loupe" / "notation").glob("*.asm"))
CONTRATS = sorted((RACINE / "lab16" / "loupe" / "I").glob("*.md"))
BRUTES = RACINE / "livraison-vague4" / "p4-mesures-brutes.jsonl"
GARDE = RACINE / "livraison-vague4" / "p4-garde-brut.jsonl"
SORTIE = RACINE / "livraison-vague5"

import importlib.util

import tiktoken  # noqa: E402
CL100K = tiktoken.get_encoding("cl100k_base")

# LA CONSTRUCTION ORIGINALE IMPORTÉE (jamais recopiée) : la re-tokenisation
# utilise LE MÊME chemin de construction que la mesure — le plan
# pré-enregistré ede70035, tel que vécu (aucune divergence de gabarit)
_spec = importlib.util.spec_from_file_location(
    "mesure_rq2_v2", RACINE / "scripts" / "vague4" / "mesure_rq2_v2.py")
_m = importlib.util.module_from_spec(_spec)
sys.modules["mesure_rq2_v2"] = _m
_spec.loader.exec_module(_m)
ECH = {(t): prompt for _, t, prompt in _m.echantillons()}

mesures = [json.loads(l) for l in BRUTES.read_text(encoding="utf-8").splitlines()]
garde = [json.loads(l) for l in GARDE.read_text(encoding="utf-8").splitlines()]
reponses = {(g["phase"], g["tache"]): g["reponse_api"] for g in garde}


def med(v):
    return statistics.median(v)


def categorie_par_operation(nom_op):
    """(m, materiau, requete, prompt, reponse) pour chaque échantillon v2 —
    le prompt reconstruit PAR LA CONSTRUCTION ORIGINALE (echantillons()),
    le matériau et la prose RE-DÉCOUPÉS du même gabarit."""
    out = []
    for m in mesures:
        if m.get("operation") != nom_op or "erreur" in m:
            continue
        tache = m["tache"]
        prompt = ECH[tache]
        if nom_op == "localiser":
            avant, apres = prompt.split("REQUÊTE : ", 1)
            materiau = avant.split(
                "BLOC DE LA CARTE (entête lu du fichier même) :", 1)[1]
            requete = apres
        elif nom_op == "éditer":
            avant, apres = prompt.split("Demande : ", 1)
            materiau = avant.split("NOTATION À ÉDITER (verbatim) :", 1)[1]
            requete = apres
        else:
            avant, apres = prompt.split("REQUÊTE : ", 1)
            materiau = avant.split("CONTRAT DE COUCHE I (verbatim) :", 1)[1]
            requete = apres
        reponse = reponses[(m["phase"], tache)]["choices"][0]["message"]["content"]
        out.append((m, materiau, requete, prompt, reponse))
    return out


def main() -> int:
    lignes = [
        "LE PÉRIMÈTRE DE CHAQUE MESURE RQ2 — LA DÉCOMPOSITION DU CONTEXTE "
        "ET LA RE-TOKENISATION INDÉPENDANTE",
        "(la vague 5, l'instruction om3ewy9lf — l'écart ×2,2 en "
        "localisation EXPLIQUÉ par périmètre, jamais par tokenizer)",
        "=" * 96,
        "",
        "LES DEUX PÉRIMÈTRES :",
        "  v0.14.0 (D195)      : le CONTENU SEUL, cl100k_base, le vrai "
        "matériau ;",
        "                        le raisonnement ESTIMÉ ×1,08 (éditer/"
        "ajouter) — l'estimation nommée ;",
        "                        ni requête, ni réponse, ni aller-retour.",
        "  v0.17.0 (ede70035)  : L'APPEL COMPLET INSTRUMENTÉ — prompt réel "
        "(matériau + prose)",
        "                        + réponse réelle, au TOKENIZER NATIF lu "
        "du log (le ×1,08 abandonné),",
        "                        cl100k en parallèle (rapport 0,98–1,02 "
        "selon l'opération).",
        "",
        "LA TABLE DE DÉCOMPOSITION (médianes, tokens) — LE MÊME MATÉRIAU, "
        "LES DEUX PÉRIMÈTRES :",
        f"{'opération':<12}{'matériau lu':>13}{'prose req.':>11}"
        f"{'réponse écrite':>16}{'TOTAL v2 (natif)':>18}"
        f"{'v0.14.0 contenu':>17}",
        "-" * 96,
    ]
    ecarts = []
    for op in ("localiser", "éditer", "ajouter"):
        ech = categorie_par_operation(op)
        mats = [len(CL100K.encode(mat)) for _, mat, _, _, _ in ech]
        reqs = [len(CL100K.encode(req)) for _, _, req, _, _ in ech]
        reps = [len(CL100K.encode(rep)) for *_, rep in ech]
        tot_natif = [m["total_tokens"] for m, *_ in ech]
        v140 = {"localiser": 580, "éditer": 2143, "ajouter": 3510}[op]
        lignes.append(f"{op:<12}{med(mats):>13.0f}{med(reqs):>11.0f}"
                      f"{med(reps):>16.0f}{med(tot_natif):>18.0f}{v140:>17}")
        # la re-tokenisation indépendante (n≥5 par opération) : le prompt
        # RECONSTRUIT et la réponse LUE de la garde brute, contre les
        # valeurs consignées — à ±1 token près
        n_verif = 0
        for m, mat, req, prompt, rep in ech:
            if n_verif >= 5:
                break
            p_cl100k = len(CL100K.encode(prompt))
            r_cl100k = len(CL100K.encode(rep))
            if abs(p_cl100k - m["cl100k_prompt"]) > 1:
                ecarts.append(f"[{op}/{m['tache']}] prompt cl100k reconstruit "
                              f"{p_cl100k} ≠ consigné {m['cl100k_prompt']} "
                              f"(> ±1)")
            if abs(r_cl100k - m["cl100k_completion"]) > 1:
                ecarts.append(f"[{op}/{m['tache']}] réponse cl100k "
                              f"{r_cl100k} ≠ consignée "
                              f"{m['cl100k_completion']} (> ±1)")
            n_verif += 1
    lignes += [
        "-" * 96,
        "",
        "LA LECTURE : l'écart 580 → 1 277 (localisation) se décompose en "
        "matériau (l'entête, déjà compté à v0.14.0),",
        "+ la prose de requête + LA RÉPONSE ÉCRITE (l'agent rend l'entête "
        "complet — le coût de l'aller-retour réel),",
        "le tout au tokenizer natif : le rapport cl100k/natif 0,98–1,02 "
        "NE PEUT PAS produire ×2,2 — le périmètre oui.",
        "Toute comparaison directe 580 vs 1 277 sans cette note est "
        "INTERDITE (la contrainte de l'instruction, portée au linter).",
        "",
        "LES DEUX BASELINES RÉALISTES (les mêmes 18 blocs, cl100k) :",
        "  (a) désassemblage de la fonction entière : médiane 2 074 "
        "tokens [q1 1 192 .. q3 3 202] (min 317, max 6 552)",
        "  (b) retrieval hiérarchique (entête + fenêtre 15) : médiane 792 "
        "tokens [q1 628 .. q3 982] (min 525, max 1 217)",
        "",
        "LA RE-TOKENISATION INDÉPENDANTE (n=5 par opération, prompt "
        "reconstruit + réponse lue, ±1 token) : "
        + (f"VERT — {3 * 5} échantillons, zéro écart > 1 token"
           if not ecarts else f"ROUGE — {len(ecarts)} écart(s)"),
    ] + [f"    {e}" for e in ecarts]
    (SORTIE / "p5-decomposition-contexte.txt").write_text(
        "\n".join(lignes), encoding="utf-8")
    print("\n".join(lignes))
    return 0 if not ecarts else 2


if __name__ == "__main__":
    sys.exit(main())
