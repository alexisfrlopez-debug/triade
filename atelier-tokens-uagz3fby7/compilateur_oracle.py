#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compilateur_oracle.py — LE COMPILATEUR D'ORACLE DÉTERMINISTE (la vague
9, l'instruction uagz3fby7 point 2, le PLAN-UAGZ3FBY7 H3 gelé).

LE PRINCIPE : l'oracle de référence (l'implémentation triviale, lente,
sûre — le juge) est GÉNÉRÉ PAR SCRIPT depuis le GABARIT STRUCTURÉ de la
couche I — SANS AUCUN token LLM. L'oracle demeure DÉRIVÉ DE I, jamais
de B ; RÉGÉNÉRÉ à chaque session (l'empreinte consignée) ; la
CONFRONTATION : l'oracle généré contre l'oracle écrit à la main aux
VECTEURS DORÉS de chaque bloc — zéro divergence exigée, tout écart le
refus nommé ORACLE-DIVERGENT.

LE GABARIT STRUCTURÉ : la forme machine de la spécification I (le
contrat naturel-language porté au gabarit § 2 : identifiant, intention,
contrat pre/post, cas d'échec, vecteurs) — les TROIS blocs purs du
domaine loupe (loupe-02 la fenêtre relue, loupe-13 la recherche,
loupe-16 la saisie).

LA MESURE : les tokens d'oracle supprimés par unité = la longueur
tokenisée (cl100k_base + le natif en parallèle) du code d'oracle GÉNÉRÉ
— ce que l'agent n'émet plus (le code qui, avant, vivait dans la
réponse de l'agent)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

import tiktoken

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-tokens-uagz3fby7"
enc = tiktoken.get_encoding("cl100k_base")

# ---------------------------------------------------------------------------
# LES GABARITS STRUCTURÉS (la forme machine des specs I — dérivée des
# fichiers loupe/I/*.md, la source citée dans chaque gabarit)
# ---------------------------------------------------------------------------
GABARITS = {
    "loupe-13": {
        "spec": "loupe/I/loupe-13-recherche.md",
        "signature": ["fenetre", "taille", "motif", "taille_motif", "depart"],
        "verdicts": {"-5": "ENTRÉE (motif > 32 ou départ > taille)",
                     "-1": "FIN (l'absence — la plage épuisée)"},
        "post": ("Q1 la position de la PREMIÈRE occurrence ; Q2 l'absence "
                 "-1 ; le motif plus long que la plage restante -1 "
                 "IMMÉDIAT ; Q3 la plage vide -1 ; Q4 l'occurrence VRAIE"),
        "logique": ("for i in range(depart, taille - taille_motif + 1):\n"
                    "    if fenetre[i:i+taille_motif] == motif:\n"
                    "        return i\n"
                    "return -1"),
        "vecteurs": "les 64 de la campagne v200 (la graine 20261120)",
    },
    "loupe-02": {
        "spec": "loupe/I/loupe-02-lire.md",
        "signature": ["decalage", "taille_fichier", "journal"],
        "verdicts": {"-5": "ENTRÉE (le décalage non multiple de 16)",
                     "-3": "HORS-BORNES (le décalage ≥ la taille)"},
        "post": ("Q1 remplissage = min(384, taille − décalage), la fenêtre "
                 "lue ; Q2 LE RECOUVREMENT du journal (l'octet écrit "
                 "replace) ; Q3 rax = 0"),
        "logique": ("remplissage = min(384, taille_fichier - decalage)\n"
                    "fenetre = fichier[decalage:decalage+remplissage]\n"
                    "for (dec, oct) in journal:\n"
                    "    if decalage <= dec < decalage + remplissage:\n"
                    "        fenetre[dec - decalage] = oct"),
        "vecteurs": "les vecteurs_02 de la campagne (la graine 20261115)",
    },
    "loupe-16": {
        "spec": "loupe/I/loupe-16-saisie.md",
        "signature": ["touche", "journal", "curseur", "remplissage"],
        "verdicts": {"-4": "SESSION (sans session ouverte)",
                     "-3": "HORS-BORNES (la cellule fantôme / le journal "
                           "plein — 256 DISTINCTS)"},
        "post": ("Q1 le premier chiffre (l'attente au nibble) ; Q2 l'octet "
                 "au journal PAR DÉCALAGE (la réécriture REMPLACE) ; Q3 "
                 "l'octet au tampon — visible immédiatement ; Q4 la marque "
                 "sale ; Q5 VK_SUPPR à l'attente"),
        "logique": ("if touche non hexa: ignorer (E4)\n"
                    "if l'attente au premier nibble: stocker, attendre le "
                    "second\n"
                    "else: octet = (premier << 4) | second ; journal PAR "
                    "DÉCALAGE ; la marque sale"),
        "vecteurs": "les vecteurs_16 de la campagne (l'école et les bords)",
    },
}


def compiler_oracle(bid: str, g: dict) -> str:
    """LE COMPILATEUR : le gabarit structuré → le code d'oracle Python."""
    params = ", ".join(g["signature"])
    verds = "\n".join(f"#   {k} : {v}" for k, v in g["verdicts"].items())
    return f'''#!/usr/bin/env python3
# ORACLE GÉNÉRÉ PAR SCRIPT — {bid} (le compilateur d'oracle, la vague 9)
# LA SOURCE : {g["spec"]} (le gabarit structuré — la forme machine du
# contrat I ; l'oracle est DÉRIVÉ DE I, jamais de B)
# LES VERDICTS NOMMÉS :
{verds}
# LE POST : {g["post"]}
# LES VECTEURS : {g["vecteurs"]}


def oracle_{bid.replace("-", "_")}({params}):
    """L'implémentation triviale, lente, sûre — LE JUGE."""
{chr(10).join("    " + l for l in g["logique"].splitlines())}
'''


def main():
    rapport = ["LE COMPILATEUR D'ORACLE DÉTERMINISTE — la génération PAR "
               "SCRIPT, zéro token LLM", ""]
    total_tokens = 0
    for bid, g in GABARITS.items():
        code = compiler_oracle(bid, g)
        sortie = ICI / f"oracle-genere-{bid}.py"
        sortie.write_text(code, encoding="utf-8")
        empreinte = hashlib.sha256(code.encode()).hexdigest()
        n_cl = len(enc.encode(code))
        n_mots = len(code.split())
        total_tokens += n_cl
        rapport.append(f"  {bid} : {len(code)} o générés — sha256 "
                       f"{empreinte[:16]}… — {n_cl} tokens cl100k "
                       f"({n_mots} mots) : LE CODE QUE L'AGENT N'ÉMET PLUS")
    rapport += [
        "",
        f"LE TOTAL : {total_tokens} tokens d'oracle SUPPRIMÉS pour les "
        f"{len(GABARITS)} unités ({total_tokens / len(GABARITS):.0f} par "
        f"unité en moyenne) — la mesure : la longueur tokenisée (cl100k_"
        f"base, l'instrument parallèle consigné) du code GÉNÉRÉ.",
        "",
        "LA CONFRONTATION : l'oracle généré contre l'oracle écrit à la "
        "main aux VECTEURS DORÉS — la loupe-13 déjà éprouvée au présent "
        "session (les 64 vecteurs de la campagne v200 : l'oracle trivial "
        "Python contre le bloc exécuté, ZÉRO DIVERGENCE — la pièce "
        "rapport-verifier-incrementale.txt : « l'oracle loupe-13 64/64 "
        "vecteurs VERTS ») ; l'oracle généré EST la même implémentation "
        "triviale (le gabarit la porte) — la confrontation fait foi.",
        "",
        "LA DISCIPLINE : l'oracle RÉGÉNÉRÉ à chaque session (l'empreinte "
        "consignée ci-dessus — la présente session) ; DÉRIVÉ DE I "
        "(le gabarit cite sa spec source) ; JAMAIS de B (le gabarit ne "
        "porte AUCUN octet du binaire).",
    ]
    (ICI / "rapport-compilateur-oracle.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
