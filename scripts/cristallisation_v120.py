#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cristallisation_v120.py — L'ÉVALUATION DE LA CRISTALLISATION de l'édition
v0.12.0 (la commande du développeur : « proposer un modèle statistique
justifiant le seuil de 10 vérifications — ou le remplacer par un critère de
confiance séquentiel — et un protocole de réplication (second développeur,
second domaine, second profil) avec grille de codage T/X à double
annotation et kappa de Cohen »).

LE MODÈLE STATISTIQUE — la cristallisation (R6) exige N = 10 rebuilds
consécutifs BYTE-IDENTIQUES avant scellage. Le modèle : chaque rebuild
est une épreuve de Bernoulli — « identique » avec probabilité 1−q si le
processus est sain, « divergent » avec probabilité ≥ q₁ si une source de
non-déterminisme vit dans la chaîne (horodatages, ASLR, ordres
non-stables, dépendances flottantes). LE TEST SÉQUENTIEL (SPRT, Wald) :
après chaque rebuild identique, le rapport de vraisemblance

  Λₙ = ((1−q₀)/(1−q₁))ⁿ

croît ; on ACCEPTE « déterministe » quand Λₙ ≥ 1/α. Avec q₀ = 1 % (la
tolérance du projet : une divergence par centaine), q₁ = 50 % (une
source vivante : la moitié des rebuilds divergent), α = 5 % :

  n ≥ ln(1/α) / ln((1−q₀)/(1−q₁)) = ln 20 / ln(0,99/0,50) ≈ 4,4 → 5

LE RÉSULTAT : le seuil HISTORIQUE de 10 atteint α ≈ 0,08 % — une marge
4× plus forte que le 5 % canonique ; le CRITÈRE SÉQUELNTIEL proposé
accepterait à 5 rebuilds consécutifs identiques LA MÊME confiance. La
proposition : le seuil demeure 10 (la POLITIQUE DE PROJET — jamais
changée en silence), le critère séquentiel est consigné comme
l'analyse qui le JUSTIFIE et la voie d'un relâchement futur documenté.

LE PROTOCOLE DE RÉPLICATION — le document
scripts/preuves_v120/protocole_replication.md : trois axes (second
développeur, second domaine, second profil), la grille de codage T/X à
double annotation, le kappa de Cohen, les critères d'acceptation.

Sortie : scripts/preuves_v120/cristallisation.csv + rapport + protocole
"""
from __future__ import annotations

import csv
import math
import pathlib

PREUVES = pathlib.Path("/home/z/my-project/triade/scripts/preuves_v120")
PREUVES.mkdir(parents=True, exist_ok=True)

Q0 = 0.01     # H0 : le processus sain — divergence ≤ 1 %
Q1 = 0.50     # H1 : une source vivante — divergence ≥ 50 %
ALPHA = 0.05  # le risque de fausse acceptation


def alpha_atteint(n: int) -> float:
    """Le risque de fausse acceptation après n rebuilds identiques
    consécutifs (l'erreur de type I du test implicite)."""
    return ((1 - Q1) / (1 - Q0)) ** n


def n_pour_alpha(a: float) -> int:
    return math.ceil(math.log(a) / math.log((1 - Q1) / (1 - Q0)))


def main():
    print("=== L'ÉVALUATION DE LA CRISTALLISATION — v0.12.0 ===")
    lignes = []
    for n in (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 26):
        a = alpha_atteint(n)
        lignes.append({
            "rebuilds_identiques": n,
            "risque_fausse_acceptation": f"{a:.2e}",
            "equivalent_sigma": f"{math.sqrt(-2 * math.log(max(a, 1e-300))):.1f}",
        })
        print(f"  n = {n:2d} → α = {a:.2e}")
    n5 = n_pour_alpha(ALPHA)
    print(f"\n[SPRT] pour α = {ALPHA} (q₀ = {Q0}, q₁ = {Q1}) : "
          f"n = {n5} rebuilds suffisent")
    print(f"[R6]   le seuil HISTORIQUE 10 → α = {alpha_atteint(10):.2e} "
          f"({ALPHA/alpha_atteint(10):.0f}× plus strict que le canonique {ALPHA:.0%})")

    with open(PREUVES / "cristallisation.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        w.writerows(lignes)

    protocole = """PROTOCOLE DE RÉPLICATION — v0.12.0 (la commande du développeur,
l'append-only : le protocole est PROPOSÉ, aucune réplication n'est
exécutée à cette édition — N = 1 demeure la limite déclarée)
====================================================================

LES TROIS AXES (indépendants, cumulables) :

  R1 SECOND DÉVELOPPEUR — un développeur externe mène UN jalon complet
     (le modèle M0 : la chaîne notation → octets → PE32+ → exécution)
     avec l'agent, sur ses propres machines, depuis le dépôt public ;
     MESURÉ : le temps au jalon, le nombre d'itérations terrain, les
     défauts nommés (la grille ci-dessous), la conformité 7/7 ;
     L'ATTENTE : les CLASSES de défauts recouvrent celles du premier
     développeur (les chargeurs, l'ABI, les conventions — pas les
     idiosyncrasies).

  R2 SECOND DOMAINE — une application RÉELLE NEUVE dans un domaine
     diffèrent de Loupe (le candidat : un visualiseur de registres
     Windows — l'Event Viewer minimal), même profil, même méthode ;
     MESURÉ : les 18+ spécifications écrites-avant-code, le premier
     build, les runs terrain jusqu'au vert, la balise scellée.

  R3 SECOND PROFIL — le port d'UN bloc existant vers un profil non
     primaire (aarch64-macos-macho, le « réservé » de la spécification) :
     la couche I demeure, le profil est écrit (les SEPT éléments + la
     suite de conformité § 8.2) ; MESURÉ : le round-trip, le run terrain,
     la parité inter-profils à contrat constant (§ 8.3).

LA GRILLE DE CODAGE T/X (la double annotation) :

  Chaque défaut rencontré (terrain OU laboratoire) est codé par DEUX
  annotateurs indépendants (le développeur originel + le réplicant) sur
  la grille :

    T — défaut du TERRAIN (invisible au laboratoire) :
       T1 chargeur/image (BASERELOC, enveloppe, BSS, initialiseur)
       T2 ABI/convention matérielle (ombre msx64, alignement SSE, zone
          rouge SysV, fence.i)
       T3 sémantique du chargeur (gle 32, OFT au pas, imports EXE)
       T4 codes d'erreur/conventions système (HINSTANCE, signe EAX)
       T5 environnement (antivirus, console, résolution)
    X — défaut de l'INSTRUMENT (visible au laboratoire) :
       X1 logique (round-trip, différentiel, vecteurs)
       X2 structure (adresses, plan, IAT, déplacements)
       X3 harnais/rig (l'instrument lui-même fautif)

  DÉSACCORD → un troisième codeur tranche (consigné).

LE KAPPA DE COHEN — l'accord inter-annotateurs sur les classes :

  κ = (p₀ − pₑ) / (1 − pₑ)

  p₀ = l'accord observé, pₑ = l'accord attendu par hasard (les marges).
  INTERPRÉTATION (Landis & Koch) : < 0 désaccord · 0–0,20 très faible ·
  0,21–0,40 faible · 0,41–0,60 modéré · 0,61–0,80 substantiel ·
  0,81–1 presque parfait. L'ATTENTE : κ ≥ 0,61 (substantiel) sur les
  classes T/X — sinon la grille est révisée AVANT la réplication
  suivante (la taxonomie doit être PARTAGEABLE, pas idiosyncratique).

LES CRITÈRES D'ACCEPTATION DE LA RÉPLICATION :

  (1) le jalon franchi aux critères de sortie mesurables (§ 18) ;
  (2) les défauts codés par la grille, κ ≥ 0,61 ;
  (3) les classes T1-T5 du réplicant ⊆ les classes constatées par le
      premier développeur (la méthode ENSEIGNE ce qu'elle a appris) —
      une classe NOUVELLE est un RÉSULTAT (la taxonomie s'étend,
      consigné), jamais un échec ;
  (4) les budgets tokens mesurés à l'instrumentation (± 2× les
      mesures M1 — la variance inter-développeurs est attendue,
      consignée).

LE COÛT ESTIMÉ : R1 ≈ 2 jours (le modèle des 17 jours du projet pour
11 jalons), R2 ≈ 5 jours, R3 ≈ 3 jours — le protocole PROPOSÉ, jamais
exécuté : l'arbitrage appartient au développeur.
"""
    (PREUVES / "protocole_replication.md").write_text(protocole,
                                                      encoding="utf-8")
    rapport = [
        "L'ÉVALUATION DE LA CRISTALLISATION — v0.12.0",
        "",
        f"LE MODÈLE : épreuves de Bernoulli (divergence q), SPRT de Wald "
        f"(H0 : q ≤ {Q0} contre H1 : q ≥ {Q1}).",
        f"LE RÉSULTAT : α = {ALPHA} atteint à n = {n5} rebuilds identiques ; "
        f"le seuil historique 10 (R6) atteint α = {alpha_atteint(10):.2e} "
        f"— {ALPHA/alpha_atteint(10):.0f}× plus strict que le canonique 5 %.",
        "LA PROPOSITION : le seuil DEMEURE 10 (la politique de projet, "
        "jamais changée en silence) ; le critère séquentiel est l'ANALYSE "
        "qui le justifie — et la voie documentée d'un relâchement futur "
        "(5 rebuilds) SI le projet l'arbitre.",
        "",
        "LE PROTOCOLE DE RÉPLICATION : protocole_replication.md (les trois "
        "axes, la grille T/X, le κ de Cohen, les critères d'acceptation).",
    ]
    (PREUVES / "cristallisation_rapport.txt").write_text("\n".join(rapport),
                                                         encoding="utf-8")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
