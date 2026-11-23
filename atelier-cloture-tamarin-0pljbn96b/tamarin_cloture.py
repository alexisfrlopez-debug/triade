#!/usr/bin/env python3
"""tamarin_cloture.py — atelier 0PLJBN96B (la vague 16).

LE KIT DE CLÔTURE IDEMPOTENT pour mener CF3-v3b.spthy à verdict complet sous
Tamarin 1.12.0 / Maude 3.4 et ProVerif, AU POSTE RÉEL (RAM ≥ 16 Go).

LE PRINCIPE : le laboratoire PRÉPARE, il ne SIMULE PAS. Le kit rend les
commandes EXACTES, copiables telles quelles au poste réel — chacune avec son
budget NOMMÉ DANS LA COMMANDE (le temps par `timeout`, la mémoire par
`ulimit -v` : les limites internes de Tamarin varient par version, le harnais
du shell est le porteur stable du budget). L'ORDRE EST OBLIGÉ : LE NÉGATIF
D'ABORD — un instrument qui ne voit pas le défaut public n'a aucune autorité
sur les positifs.

Codes de sortie : 0 = tout rendu ; 2 = REFUS (l'outillage absent — jamais un
run simulé) ; 3 = écart à la construction.
"""

import argparse
import json
import os
import re
import shutil
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELES = {   # des chemins en / — le poste réel est Linux
    "v3b": "atelier-cf3-verdict-qa3k5putf/CF3-v3b.spthy",
    "negatif": "atelier-cf3-verdict-qa3k5putf/CF3-v3-negatif.spthy",
    "pv": "atelier-cf3-verdict-qa3k5putf/CF3-v3.pv",
}

# LES BUDGETS (nommés dans chaque commande — JAMAIS implicites)
MEM_16G = 16777216        # ulimit -v, en Kio : 16 Gio
TEMPS_L1 = 14400          # 4 h — la convergence lente constatée au bac
TEMPS_LEMME = 7200        # 2 h
TEMPS_HEURISTIQUE = 3600  # 1 h par heuristique
TEMPS_NEGATIF = 600       # 10 min — la falsification doit être RAPIDE
TEMPS_PROVERIF = 3600     # 1 h

L1 = "implication_secret_appris_reconstitution_illicite"
L2 = "conservation_de_la_cle_utilisateur"
T1 = "temoin_falsification_et_destruction"
T2 = "temoin_la_chaine_vivante"
T3 = "temoin_atteignabilite_du_seuil"

HEURISTIQUES = ("S", "I", "i", "c", "C")   # les cinq éprouvées au bac (registre v15)


def _cmd(temps, memoire, modele, *flags):
    """La commande EXACTE : le budget NOMMÉ DANS la commande elle-même."""
    ulimit = f"ulimit -v {memoire}" if memoire else ":"
    return f"( {ulimit} ; timeout {temps} tamarin-prover {MODELES[modele]} " + " ".join(flags) + " )"


def construire():
    """-> [(rang, identifiant, commande, attendu)] — l'ordre est OBLIGÉ."""
    cmds = []

    # (0) LE NÉGATIF D'ABORD — qui DOIT être falsifié (le défaut v2 public attrapé)
    cmds.append((0, "NEGATIF (la part publique transposée)",
                 _cmd(TEMPS_NEGATIF, None, "negatif", "--stop-on-trace=DFS", "--bound=8"),
                 "FALSIFIÉ — la falsification attendue sur le second étage de L1 "
                 "(le secret appris sans trois parts fuitées) ; un « verified » au "
                 "négatif est un DÉFAUT D'INSTRUMENT, jamais un succès"))

    # (1..5) LES CINQ LEMMES (L1, L2, T1-T3) — L3 est déjà VERIFIED (1 122 pas, 29,4 s)
    cmds.append((1, f"L1 {L1}",
                 _cmd(TEMPS_L1, MEM_16G, "v3b", f"--prove={L1}", "--partial-evaluation=SUMMARY"),
                 "VERIFIED ou INCOMPLETE nommé (la décomposition du but K(p) contre la "
                 "profondeur — jamais un verdict fabriqué)"))
    for h in HEURISTIQUES:
        cmds.append((1, f"L1 {L1} — heuristique {h}",
                     _cmd(TEMPS_HEURISTIQUE, MEM_16G, "v3b", f"--prove={L1}",
                           f"--heuristic={h}", "--partial-evaluation=SUMMARY"),
                     "la variante consignée : le mur de mémoire se déplace, pas se dissipe"))
    cmds.append((2, f"L2 {L2}",
                 _cmd(TEMPS_LEMME, MEM_16G, "v3b", f"--prove={L2}", "--partial-evaluation=SUMMARY"),
                 "VERIFIED ou INCOMPLETE nommé (l'OOM du bac ne préjuge pas du poste 16 Go)"))
    cmds.append((3, f"T1 {T1}",
                 _cmd(TEMPS_LEMME, MEM_16G, "v3b", f"--prove={T1}",
                       "--stop-on-trace=DFS", "--bound=12"),
                 "VERIFIED (le témoin à ~9 pas : la trace bornée doit l'atteindre)"))
    cmds.append((4, f"T2 {T2}",
                 _cmd(TEMPS_LEMME, MEM_16G, "v3b", f"--prove={T2}",
                       "--stop-on-trace=DFS", "--bound=12"),
                 "VERIFIED (le témoin à ~9 pas — la frontière BFS explosait au bac)"))
    cmds.append((5, f"T3 {T3}",
                 _cmd(TEMPS_LEMME, MEM_16G, "v3b", f"--prove={T3}",
                       "--stop-on-trace=DFS", "--bound=12"),
                 "VERIFIED (le témoin : création → migration → 3 fuites → reconstitution → KU)"))

    # (6) LE PORT PROVERIF — les six requêtes actives
    cmds.append((6, "PROVERIF (le port CF3-v3.pv)",
                 f"( timeout {TEMPS_PROVERIF} proverif {MODELES['pv']} )",
                 "les six requêtes actives + LES SIX ÉCARTS DE SÉMANTIQUE nommés "
                 "(ECARTS-SEMANTIQUES-TAMARIN-PROVERIF.txt)"))
    return cmds


def rendre(cmds, sortie=None):
    print("=== LE KIT DE CLÔTURE IDEMPOTENT (tamarin 1.12.0 / Maude 3.4 / proverif) ===")
    print("  LE POSTE REQUIS : Linux, RAM ≥ 16 Go, tamarin-prover 1.12.0 au PATH, Maude 3.4,")
    print("  proverif ; le bac n'a AUCUN de ces binaires — le kit prépare, il ne simule pas.")
    print("  L'ORDRE EST OBLIGÉ : le négatif d'abord (la portance avant l'autorité).")
    print()
    for rang, ident, cmd, attendu in cmds:
        print(f"  [{rang}] {ident}")
        print(f"      {cmd}")
        print(f"      attendu : {attendu}")
        print()
    if sortie:
        with open(sortie, "w", encoding="utf-8") as f:
            json.dump({"schema": "TRIADE-KIT-TAMARIN-CLOTURE-v1",
                       "commandes": [{"rang": r, "id": i, "commande": c, "attendu": a}
                                     for r, i, c, a in cmds],
                       "budgets": {"memoire_kio": MEM_16G, "l1_s": TEMPS_L1,
                                   "lemme_s": TEMPS_LEMME, "heuristique_s": TEMPS_HEURISTIQUE,
                                   "negatif_s": TEMPS_NEGATIF, "proverif_s": TEMPS_PROVERIF}},
                      f, ensure_ascii=False, indent=2)
        print(f"  le registre : {sortie}")


def executer():
    """Le geste du poste réel — REFUSÉ au laboratoire, jamais simulé."""
    absents = [t for t in ("tamarin-prover", "proverif") if shutil.which(t) is None]
    if absents:
        print(f"REFUS (exit 2) : {', '.join(absents)} absent(s) du PATH — le run est le geste")
        print("du poste réel (RAM ≥ 16 Go). Le kit est RENDU, la campagne n'est PAS simulée.")
        return 2
    print("Les binaires sont présents — exécutez les commandes du --rendre au poste réel.")
    return 0


def statuts():
    """La table des statuts DEPUIS LES PIÈCES — jamais depuis l'intention."""
    chemin = os.path.join(RACINE, "atelier-cf3-verdict-qa3k5putf", "table-statuts-cf3.txt")
    if not os.path.isfile(chemin):
        return 3
    print("=== LA TABLE DES STATUTS (l'état des pièces, la vague 15) ===")
    for ligne in open(chemin, encoding="utf-8"):
        if ligne.strip() and not ligne.startswith("TABLE DES") and not ligne.startswith("="):
            print("  " + ligne.rstrip())
    print()
    print("  LA PRÉSENTE (la vague 16) : le kit rendu — les runs attendent le poste réel ;")
    print("  la table sera mise à jour DEPUIS LES PIÈCES au geste (jamais depuis le plan).")
    return 0


def autotest():
    print("=== L'AUTOTEST DU KIT DE CLÔTURE ===")
    cmds = construire()
    tests = []

    # [1] le négatif est PREMIER
    tests.append(cmds[0][0] == 0 and "NEGATIF" in cmds[0][1])
    print(f"  [1] le négatif est PREMIER de l'ordre          : {'OUI' if tests[-1] else 'NON'}")

    # [2] chaque commande porte un budget NOMMÉ
    sans_budget = [i for _, i, c, _ in cmds if "timeout" not in c]
    tests.append(not sans_budget)
    print(f"  [2] chaque commande porte son budget (timeout) : "
          f"{'OUI' if tests[-1] else 'NON — ' + ', '.join(sans_budget)}")

    # [3] les cinq lemmes présents, L3 absent (déjà VERIFIED)
    textes = " ".join(i for _, i, _, _ in cmds)
    tests.append(all(n in textes for n in (L1, L2, T1, T2, T3)))
    print(f"  [3] L1, L2, T1, T2, T3 rendus                  : {'OUI' if tests[-1] else 'NON'}")

    # [4] les modèles EXISTENT au dépôt
    absents = [k for k, v in MODELES.items()
               if not os.path.isfile(os.path.join(RACINE, *v.split("/")))]
    tests.append(not absents)
    print(f"  [4] les trois modèles existent au dépôt        : "
          f"{'OUI' if tests[-1] else 'NON — ' + ', '.join(absents)}")

    # [5] --executer REFUSE au laboratoire (exit 2)
    rc = executer()
    tests.append(rc == 2)
    print(f"  [5] --executer au bac                          : "
          f"{'REFUSÉ exit 2' if tests[-1] else 'DÉFAUT — un run serait simulé !'}")

    # [6] la reproductibilité : deux constructions identiques
    tests.append(construire() == cmds)
    print(f"  [6] la construction est IDEMPOTENTE            : {'OUI' if tests[-1] else 'NON'}")

    print(f"  {sum(1 for t in tests if t)}/{len(tests)} contrôles rendus")
    return 0 if all(tests) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rendre", action="store_true", help="rendre les commandes (le défaut)")
    ap.add_argument("--executer", action="store_true")
    ap.add_argument("--statuts", action="store_true")
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--registre", default=None)
    args = ap.parse_args()
    if args.autotest:
        rc = autotest()
        if args.registre:
            with open(args.registre, "w", encoding="utf-8") as f:
                json.dump({"schema": "TRIADE-KIT-TAMARIN-AUTOTEST-v1",
                           "controles": "6/6" if rc == 0 else "ECART"}, f,
                          ensure_ascii=False, indent=2)
        return rc
    if args.statuts:
        return statuts()
    if args.executer:
        return executer()
    rendre(construire(), args.registre)
    return 0


if __name__ == "__main__":
    sys.exit(main())
