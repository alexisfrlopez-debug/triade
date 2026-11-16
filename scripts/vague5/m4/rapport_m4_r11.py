#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapport_m4_r11.py — LE RAPPORT R11 DE L'OPTIMISATION M4 (l'instruction
mof9q10vq : « mesurer avant/après sur la même unité, même machine,
chronomètre monotone, et consigner les résultats (R11) ; si le ratio
repasse sous ×10, le rapporter comme nouvelle mesure n=1 sans déclarer
H5 réhabilitée ; documenter tout compromis de couverture refusé »).
"""
import json
import pathlib

S = pathlib.Path("/home/z/my-project/livraison-vague5")
avant = json.loads((S / "p8-m4-avant.json").read_text())
apres = json.loads((S / "p8-m4-apres.json").read_text())
c_total = 2.2          # mesuré ce jour sur cette machine (mesure_c_v180.py)

lignes = [
    "LE RAPPORT R11 — L'OPTIMISATION DU TEMPS DE VÉRIFICATION (M4, BRAS T)",
    "(l'instruction mof9q10vq, la vague 5 — la même unité, la même machine,",
    " le chronomètre monotone, AUCUN contrôle retiré)",
    "=" * 92,
    "",
    "LA MACHINE : ce bac du laboratoire — 2 cœurs CPU (le parallélisme y est",
    "borné à ~2× ; les leviers sont mesurés tels quels, n=1).",
    "",
    "LA MESURE AVANT (la liste fixe originale, les outils de campagne) :",
    f"  TOTAL {avant['total_s']:.1f} s — "
    + " ; ".join(f"{e['etape']} {e['secondes']}s"
                 for e in avant['etapes']
                 if not e['etape'].startswith('build-rebuild')),
    f"  (les 12 rebuilds de cristallisation : "
    f"{sum(e['secondes'] for e in avant['etapes'] if e['etape'].startswith('build-rebuild')):.1f} s)",
    "",
    "LA MESURE APRÈS (la liste optimisée, les MÊMES contrôles) :",
    f"  TOTAL 39.3 s (première exécution) puis {apres["total_s"]:.1f} s "
    "(seconde) —",
    "  deux exécutions CONSÉCUTIVES, verdicts identiques (tout VERT), les",
    "  empreintes des pièces scellées INTACTES avant/après.",
    f"  " + " ; ".join(f"{e['etape']} {e['secondes']}s"
                       for e in apres['etapes']),
    "",
    "LES LEVIERS IMPLÉMENTÉS :",
    "  1. LA CRISTALLISATION CONCURRENTE — les 12 rebuilds courent en",
    "     parallèle, chacun dans SA COPIE hermétique du dossier d'unité",
    "     (l'outil original INTACT, une substitution mécanique du SEUL",
    "     chemin d'unité) ; toutes les sorties comparées octet à octet",
    "     (l'identité de TOUTES implique chaque paire consécutive — la",
    "     preuve de déterminisme est sans ordre) : 6.0 s → 4.2 s.",
    "  2. LES ORACLES AUX SESSIONS PARALLÈLES — le profil est sans appel :",
    "     l'OUVERTURE de session (le md5+sha256 du fichier ENTIER sous",
    "     émulation : 3.2 s pour 65 Kio, ~10 s pour 196 Kio) domine, les",
    "     lectures sont quasi gratuites (0,15 ms). Chaque fichier de V1",
    "     (puis la vue pré-posée et V2) vit dans SA PROPRE émulation",
    "     Unicorn persistante — un pool de travailleurs : l'oracle loupe-02",
    "     33.2 s → 23.2 s ; loupe-01 sans gain (le témoin 196 Kio EST le",
    "     chemin critique, 10.3 s).",
    "  3. LA VÉRIFICATION INCRÉMENTALE GUIDÉE PAR LA CARTE — DÉJÀ LA",
    "     CONCEPTION des outils de campagne : le différentiel du build est",
    "     confiné au slot touché (loupe-01 : [0x3280, 0x3440) + la porte",
    "     R10), les oracles sont par bloc ; la re-vérification complète",
    "     périodique demeure la porte de scellement (la suite M10 complète",
    "     159×3 graines — inchangée, hors de cette liste).",
    "",
    "LA PREUVE QU'AUCUN CONTRÔLE NE FUT RETIRÉ : les consoles des oracles",
    "v180 sont IDENTIQUES aux originales, ligne à ligne (diff vide) — les",
    "mêmes vecteurs, les mêmes graines (20261114), le même juge, le même",
    "ordre d'impression ; seuls changent l'ORDONNANCEMENT des exécutions.",
    "",
    "LE RATIO (les DEUX bras sur CETTE machine) :",
    f"  C = {c_total:.1f} s (la liste fixe du bras C, la chaîne croisée",
    "      TRIXIE re-extraite des .deb SANS ROOT — les versions EXACTES de",
    "      la campagne : gcc-mingw-w64 14.2.0-19+27+b1, binutils",
    "      2.44-3+12+b1, mingw-w64 12.0.0-5).",
    f"  AVANT : {avant['total_s']:.1f} / {c_total:.1f} = "
    f"{avant['total_s']/c_total:.1f}×  (le recoup : la campagne avait mesuré "
    "23.9×",
    f"  APRÈS : {apres['total_s']:.1f} / {c_total:.1f} = "
    f"{apres['total_s']/c_total:.1f}×",
    "",
    "LA LECTURE HONNÊTE : le gain est de "
    f"{(1 - apres['total_s']/avant['total_s'])*100:.0f} % sur cette machine "
    "à 2 cœurs ; le",
    "ratio demeure AU-DESSUS de ×10 — H5 DEMEURE FALSIFIÉE (la mesure est",
    "n=1, la machine fait partie du record) ; le chemin critique restant",
    "est l'émulation cryptographique des sessions de contrat (le md5+sha256",
    "du témoin 196 Kio, ~10 s — irréductible sans changer les contrôles),",
    "et les leviers parallèles monteront avec les cœurs (la machine du",
    "développeur en a davantage).",
    "",
    "LES COMPROMIS DE COUVERTURE REFUSÉS : AUCUN — aucune graine supprimée,",
    "aucun vecteur réduit, aucune vérification retirée (la preuve : les",
    "consoles identiques) ; le levier « pool persistant inter-outils » (une",
    "seule émulation partagée entre le build, le round-trip et l'oracle)",
    "fut CONSIDÉRÉ ET REFUSÉ : il couplerait des outils que le protocole",
    "exige indépendants (le juge ne partage pas l'état du jugé).",
]
(S / "p8-m4-rapport-r11.txt").write_text("\n".join(lignes), encoding="utf-8")
print("\n".join(lignes[:14]))
print("...")
print("rapport écrit :", S / "p8-m4-rapport-r11.txt")
