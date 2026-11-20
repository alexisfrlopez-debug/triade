#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generateur_randomisation.py — LE GÉNÉRATEUR DE LA RANDOMISATION STRATIFIÉE
de la campagne H7 (kit l4nnwqlld, pièce 4).

LA RÈGLE (PLAN-H7.txt, gelé avant le premier tirage réel) : les unités sont
APPARIÉES PAR FAMILLE (14 strates fixées — § 3 du plan), l'ordre du bras est
TIRÉ DANS LES STRATES (une pièce équilibrée par strate : la première unité
T-première et la seconde C-première, OU l'inverse) — LES DEUX ORDRES
SURVIENNENT PAR CONSTRUCTION : le contraste d'ordre est garanti
structurellement, le « une-sur-seize » de D210 est impossible, AUCUN
re-tirage n'est jamais nécessaire.

LA GRAINE : 20261120 (consignée au plan AVANT tout tirage réel — le modèle
D210 : 20261117). Le tirage est DÉTERMINISTE à la graine : re-exécuter le
générateur DOIT redonner LA MÊME table (l'autotest le vérifie — la preuve
de non-rétropédalage). LA TABLE OFFICIELLE n'existe que par le geste
« --tirer » (consignée, signée, à l'ouverture de la campagne) ; l'autotest
vérifie les invariants SANS produire la pièce officielle.

LE PLAN DE PUISSANCE codé (§ 2 du plan — α = 0,05, puissance 0,8, l'effet
attendu dérivé de D204/D210) :
  δ̂ = |ln(67 475/53 158)| = 0,2385  (la paire instrumentée D204, ×1,27) ;
  σ̂ = SD des log-M2 des 4 unités D210 = 0,2863 (borne conservatrice) ;
  normale : n = ((z_{0,975}+z_{0,80})·σ̂/δ̂)² = 11,31 → 12 ;
  t de Student itérée (ddl = n−1) : converge à 14 ;
  LA DÉCISION FAIL-CLOSED : 14 strates (la borne la plus exigeante).

Usage :
  python3 generateur_randomisation.py --autotest   (les invariants à la graine)
  python3 generateur_randomisation.py --tirer      (LA TABLE officielle — le
                                                    geste d'ouverture, à
                                                    consigner et signer)
"""

from __future__ import annotations

import hashlib
import math
import random
import sys

GRAINE = 20261120          # consignée au plan, avant le premier tirage réel
ALPHA = 0.05               # gelé (§ 2 du plan)
PUISSANCE = 0.80           # gelé (§ 2 du plan)

# LA FIXATION DES STRATES (§ 3 du plan — GELÉE) : 14 strates × 2 unités.
# S01..S12 : les DOUZE familles de blocs loupe JAMAIS livrées à une campagne
#            (six familles ont vécu D204/D210 : 01, 02, 05, 08, 13, 16) ;
# S13, S14 : les RELIVRAISONS nommées (loupe-01 : la paire instrumentée qui
#            fonde δ̂ ; loupe-16 : la famille à état du plafond D210).
STRATES = [
    ("S01", "loupe-03-fermer",     "fermer-tour1",  "fermer-tour2"),
    ("S02", "loupe-04-cadre",      "cadre-tour1",   "cadre-tour2"),
    ("S03", "loupe-06-md5",        "md5-tour1",     "md5-tour2"),
    ("S04", "loupe-07-cumul",      "cumul-tour1",   "cumul-tour2"),
    ("S05", "loupe-09-ecran",      "ecran-tour1",   "ecran-tour2"),
    ("S06", "loupe-10-peinture",   "peinture-tour1", "peinture-tour2"),
    ("S07", "loupe-11-defilement", "defilement-tour1", "defilement-tour2"),
    ("S08", "loupe-12-aller",      "aller-tour1",   "aller-tour2"),
    ("S09", "loupe-14-suivant",    "suivant-tour1", "suivant-tour2"),
    ("S10", "loupe-15-curseur",    "curseur-tour1", "curseur-tour2"),
    ("S11", "loupe-17-sauver",     "sauver-tour1",  "sauver-tour2"),
    ("S12", "loupe-18-quitter",    "quitter-tour1", "quitter-tour2"),
    ("S13", "loupe-01-relivree",   "ouverture-rel1", "ouverture-rel2"),
    ("S14", "loupe-16-relivree",   "saisie-rel1",   "saisie-rel2"),
]

# Les données fondatrices (§ 2 du plan — les chiffres CONSIGNÉS des
# campagnes, jamais recomptés : les entrées du registre).
M2_D204_PAIRE = (53158, 67475)              # loupe-01 : bras T, bras C
M2_D210_UNITES = [42610, 52729, 40749, 26662]  # loupe-02/-08/-13/-16


# --- le plan de puissance, codé (il se re-dérive au geste) ----------------------

def _t_student_cumul(x, ddl):
    """La CDF du t de Student (Abramowitz-Stegun 26.7.10, précision ~1e-4 —
    suffisante pour un calcul de taille documenté ; la borne adoptée est
    arrondie AU-DESSUS, la précision ne change jamais la décision)."""
    if ddl <= 0:
        return float("nan")
    a = math.gamma((ddl + 1) / 2) / (math.sqrt(ddl * math.pi)
                                     * math.gamma(ddl / 2))
    # intégration numérique simple sur la densité
    pas = 0.001
    s, t = 0.0, -12.0
    while t < x:
        s += a / (1 + t * t / ddl) ** ((ddl + 1) / 2) * pas
        t += pas
    return s


def t_quantile(p, ddl):
    """Le quantile du t de Student par inversion numérique (bornes serrées)."""
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if _t_student_cumul(mid, ddl) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def puissance_h7():
    """Le calcul documenté du § 2 : retour (delta, sigma, n_normale,
    n_student, decision)."""
    delta = abs(math.log(M2_D204_PAIRE[1] / M2_D204_PAIRE[0]))
    logs = [math.log(m) for m in M2_D210_UNITES]
    mu = sum(logs) / len(logs)
    sigma = math.sqrt(sum((x - mu) ** 2 for x in logs) / (len(logs) - 1))
    z_a = 1.959964                    # z_{0,975}
    z_b = 0.841621                    # z_{0,80}
    n_normale = ((z_a + z_b) * sigma / delta) ** 2
    n = max(2, math.ceil(n_normale))  # itération de la correction t
    for _ in range(50):
        ddl = n - 1
        t_a = t_quantile(1 - ALPHA / 2, ddl)
        t_b = t_quantile(PUISSANCE, ddl)
        n_suivant = math.ceil(((t_a + t_b) * sigma / delta) ** 2)
        if n_suivant <= n:
            break
        n = n_suivant
    n_student = n
    decision = max(math.ceil(n_normale), n_student)   # fail-closed : la borne
    # la plus exigeante
    return delta, sigma, n_normale, n_student, decision


# --- le tirage stratifié (déterministe à la graine) -----------------------------

def tirer_table(graine=GRAINE):
    """La table de tirage : par strate, UNE pièce équilibrée — la première
    unité T-première et la seconde C-première, OU l'inverse. Les deux ordres
    surviennent PAR CONSTRUCTION dans CHAQUE strate."""
    rng = random.Random(graine)
    lignes = []
    for sid, famille, u1, u2 in STRATES:
        if rng.random() < 0.5:
            lignes.append((sid, famille, u1, "T-premiere", u2, "C-premiere"))
        else:
            lignes.append((sid, famille, u2, "T-premiere", u1, "C-premiere"))
    return lignes


def table_canonique(lignes):
    """Le rendu canonique (la table dont le sha256 se consigne)."""
    entete = ("# TABLE DE TIRAGE — campagne H7, randomisation stratifiée "
              "(kit l4nnwqlld)\n"
              f"# graine : {GRAINE} (consignée au plan AVANT le premier "
              "tirage réel)\n"
              "# par strate : la pièce équilibrée décide quelle unité porte "
              "le bras T en premier ;\n"
              "# l'autre unité porte le bras C en premier — LES DEUX ORDRES "
              "PAR CONSTRUCTION.\n")
    corps = "\n".join(f"{sid}|{famille}|{ut}|T-premiere|{uc}|C-premiere"
                      for sid, famille, ut, _, uc, _ in lignes)
    return entete + corps + "\n"


def sha_table(lignes):
    return hashlib.sha256(table_canonique(lignes).encode()).hexdigest()


# --- l'autotest (les invariants à la graine — SANS produire la pièce officielle) -

def autotest():
    ok = True
    print("=== L'AUTOTEST DU GÉNÉRATEUR DE RANDOMISATION (à la graine "
          f"{GRAINE}) ===")
    delta, sigma, n_normale, n_student, decision = puissance_h7()
    bon = (abs(delta - 0.2385) < 0.0002 and abs(sigma - 0.2856) < 0.0002
           and 11.0 < n_normale <= 12 and decision == 14 and len(STRATES) == decision)
    print(f"  plan de puissance  : delta={delta:.4f} (0,2385 attendu : la "
          f"paire D204 x1,27), sigma={sigma:.4f} (0,2856 attendu : les 4 "
          f"log-M2 D210) ; normale n={n_normale:.2f} -> {math.ceil(n_normale)}, "
          f"t itérée -> {n_student} ; DECISION fail-closed = {decision} "
          f"strates = {len(STRATES)} fixées -> "
          f"{'OK' if bon else 'ÉCART'}")
    ok &= bon

    t1, t2 = tirer_table(), tirer_table()
    canon1 = [table_canonique(t1), table_canonique(t2)]
    bon = canon1[0] == canon1[1] and len(t1) == 14
    print(f"  déterminisme       : la graine redonne LA MÊME table "
          f"(sha256 {sha_table(t1)[:16]}…) -> {'OK' if bon else 'ÉCART'}")
    ok &= bon

    contraste = all(
        sum(1 for l in lignes_strate if l[3] == "T-premiere") == 1
        for lignes_strate in [[l] for l in t1])
    bon = all(l[3] == "T-premiere" and l[5] == "C-premiere" for l in t1)
    n_t = sum(1 for _, _, ut, o, _, _ in t1 for _ in [0] if o == "T-premiere")
    print(f"  contraste garanti  : les 14 strates portent CHACUNE une unité "
          f"T-premiere et une C-premiere (total T-premieres = {n_t}/28) -> "
          f"{'OK' if bon else 'ÉCART'}")
    ok &= bon

    familles = [famille for _, famille, _, _, _, _ in t1]
    distinctes = len(set(familles))
    bon = distinctes == 14
    print(f"  strates fixées     : {len(STRATES)} strates, {distinctes} "
          "familles distinctes (les 12 jamais livrées + les 2 relivraisons "
          f"nommées) -> {'OK' if bon else 'ÉCART'}")
    ok &= bon

    autre = tirer_table(GRAINE + 1)
    bon = table_canonique(autre) != table_canonique(t1)
    print(f"  sensibilité graine : une autre graine donne une AUTRE table "
          f"(la graine compte) -> {'OK' if bon else 'ÉCART'}")
    ok &= bon

    print(f"[autotest] {'VERT' if ok else 'ROUGE'} — le générateur est PRÊT ; "
          "la table officielle n'existera qu'au geste --tirer (consignée, "
          "signée, à l'ouverture de la campagne)")
    return ok


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("--autotest", "--tirer"):
        print(__doc__)
        return 2
    if sys.argv[1] == "--autotest":
        return 0 if autotest() else 2
    lignes = tirer_table()
    table = table_canonique(lignes)
    empreinte = sha_table(lignes)
    print(table)
    print(f"# sha256 de la table canonique : {empreinte}")
    print("# LE GESTE : consigner cette table datée-signée à l'ouverture de "
          "la campagne H7 ;\n#   la re-exécution à la graine "
          f"{GRAINE} doit redonner CETTE table "
          "(sha compris).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
