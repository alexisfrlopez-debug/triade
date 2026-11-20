#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agregateur_dudect.py — L'AGRÉGATEUR FAIL-CLOSED DU KIT DUDECT (l4nnwqlld).

LA RÈGLE DE FER (le plan l4nnwqlld) : « tout run manquant = le protocole
REFUSÉ (jamais d'agrégat partiel) ». Le présent agrégateur VALIDE LA
COMPLÉTUDE AVANT TOUT CALCUL : aucune moyenne, aucune médiane, aucun t de
Welch n'est calculé tant qu'un seul manque n'est pas nommé — c'est écrit
dans l'ORDRE du code (valider_completude() précède agreger()), pas dans
une intention.

LA COMPLÉTUDE EXIGÉE (REGLE-JUGEMENT.txt, gelée) :
  - ≥ 2 machines, chacune avec runs/temoin-machine-<ID>.txt portant
    L'EMPREINTE CPU ET LA FRÉQUENCE consignées (un témoin muet = un
    manque — fail-closed sur la forme aussi) ;
  - les QUATRE cibles : tls13-02, tls13-13, tls13-16, tls13-17 ;
  - les TROIS N : 60, 200, 400 ;
  - n ≥ 10 runs par cellule (machine × cible × N), chacun un dossier
    runs/machine-<ID>/<cible>/N<N>/run<NN>/ portant UN journal
    journal-dudect-*.csv COMPLET : N lignes classe « fixe » et N lignes
    classe « aleatoire », les cycles présents et entiers.

LE CALCUL (seulement après validation) : le t DE WELCH recalculé DEPUIS
LES CYCLES des journaux (aucune confiance aux consoles), la MÉDIANE des t
par cellule, la DÉCISION PAR CIBLE (au moins une cellule à divergence ⇒
la cible est à divergence au seuil ; toutes sans ⇒ « aucune divergence au
seuil, consignée comme telle » — jamais « constant time proven »).

Usage :
  python3 agregateur_dudect.py runs/            (l'agrégation réelle)
  python3 agregateur_dudect.py --selftest       (l'autotest fail-closed
                                                 sur fixtures SYNTHÉTIQUES —
                                                 jamais des mesures réelles)

Sortie : 0 = agrégat rendu (le verdict est DANS le fichier et à l'écran,
le code ne dit PAS « constant time ») ; 2 = REFUS nommé (les manques).
"""

from __future__ import annotations

import csv
import math
import os
import re
import statistics
import sys
import tempfile
import time

CIBLES = ["tls13-02", "tls13-13", "tls13-16", "tls13-17"]
NS = [60, 200, 400]
N_RUNS_MIN = 10
SEUIL = 5.0
MOTIF_TEMOIN_CPU = re.compile(r"(?i)^\s*empreinte\s*cpu\s*:", re.M)
MOTIF_TEMOIN_FREQ = re.compile(r"(?i)^\s*fr[ée]quence\s*:", re.M)
MOTIF_RUN = re.compile(r"^run(\d+)$")
MOTIF_JOURNAL = re.compile(r"^journal-dudect-.*\.csv$")


# --- la lecture d'un journal (fail-closed sur la forme) -------------------------

def lire_journal(chemin, n_attendu):
    """Retour (cycles_fixe, cycles_alea) — REFUS nommé si le journal est
    incomplet : le compte de classes, les cycles absents ou non entiers."""
    fixes, aleas = [], []
    with open(chemin, newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        champs = lecteur.fieldnames or []
        if not {"cible", "classe", "cycles"} <= set(champs):
            raise ValueError(f"{chemin} : colonnes {champs} — le journal "
                             "n'est pas celui du mesureur scellé")
        for ligne in lecteur:
            try:
                cyc = int(ligne["cycles"])
            except (TypeError, ValueError):
                raise ValueError(f"{chemin} : cycles illisibles à la ligne "
                                 f"{lecteur.line_num}")
            if ligne["classe"] == "fixe":
                fixes.append(cyc)
            elif ligne["classe"] == "aleatoire":
                aleas.append(cyc)
            else:
                raise ValueError(f"{chemin} : classe {ligne['classe']!r} "
                                 "inconnue (fixe/aleatoire attendues)")
    if len(fixes) != n_attendu or len(aleas) != n_attendu:
        raise ValueError(f"{chemin} : {len(fixes)} fixes / {len(aleas)} "
                         f"aléatoires — {n_attendu} attendus de chaque : "
                         "journal INCOMPLET (un run tronqué est un manque)")
    return fixes, aleas


# --- la statistique (le t de Welch, recalculé depuis les cycles) ----------------

def t_welch(fixe, alea):
    """(m_fixe − m_alea) / sqrt(v_fixe/n + v_alea/n) — variances inégales
    admises (la correction de Welch), les deux effectifs égaux."""
    n1, n2 = len(fixe), len(alea)
    m1, m2 = statistics.fmean(fixe), statistics.fmean(alea)
    v1 = statistics.variance(fixe) if n1 > 1 else 0.0
    v2 = statistics.variance(alea) if n2 > 1 else 0.0
    den = math.sqrt(v1 / n1 + v2 / n2)
    return (m1 - m2) / den if den > 0 else 0.0


# --- LA COMPLÉTUDE AVANT TOUT CALCUL (la règle de fer) --------------------------

def valider_completude(racine):
    """Retour (arbre, manques) — l'arbre n'est retourné que si manques est
    vide ; AUCUN calcul n'a lieu ici, la validation EST la fonction."""
    manques = []
    if not os.path.isdir(racine):
        return None, [f"le répertoire {racine} n'existe pas"]
    temoins = {}
    for nom in sorted(os.listdir(racine)):
        chemin = os.path.join(racine, nom)
        m = re.match(r"^temoin-machine-(.+)\.txt$", nom)
        if m and os.path.isfile(chemin):
            texte = open(chemin, encoding="utf-8", errors="replace").read()
            if not MOTIF_TEMOIN_CPU.search(texte):
                manques.append(f"{nom} : l'EMPREINTE CPU manque (témoin muet)")
            if not MOTIF_TEMOIN_FREQ.search(texte):
                manques.append(f"{nom} : la FRÉQUENCE manque (témoin muet)")
            temoins[m.group(1)] = chemin
    machines = []
    for nom in sorted(os.listdir(racine)):
        chemin = os.path.join(racine, nom)
        if re.match(r"^machine-(.+)$", nom) and os.path.isdir(chemin):
            machines.append((nom.split("-", 1)[1], chemin))
    if len(machines) < 2:
        manques.append(f"{len(machines)} machine(s) trouvée(s) — le protocole "
                       "exige ≥ 2 machines (machine-A/, machine-B/…)")
    for mid, _ in machines:
        if mid not in temoins:
            manques.append(f"machine-{mid} : runs/temoin-machine-{mid}.txt "
                           "ABSENT (l'empreinte CPU et la fréquence exigées)")
    for mid, chemin_machine in machines:
        for cible in CIBLES:
            chemin_cible = os.path.join(chemin_machine, cible)
            if not os.path.isdir(chemin_cible):
                manques.append(f"machine-{mid}/{cible}/ : ABSENT")
                continue
            for n in NS:
                chemin_n = os.path.join(chemin_cible, f"N{n}")
                if not os.path.isdir(chemin_n):
                    manques.append(f"machine-{mid}/{cible}/N{n}/ : ABSENT")
                    continue
                vus = set()
                for nom_run in sorted(os.listdir(chemin_n)):
                    chemin_run = os.path.join(chemin_n, nom_run)
                    m = MOTIF_RUN.match(nom_run)
                    if not m or not os.path.isdir(chemin_run):
                        manques.append(f"machine-{mid}/{cible}/N{n}/{nom_run} : "
                                       "pas un dossier run<NN> — l'arborescence "
                                       "exigée (LISEZMOI § 6)")
                        continue
                    vus.add(int(m.group(1)))
                    journaux = [j for j in sorted(os.listdir(chemin_run))
                                if MOTIF_JOURNAL.match(j)]
                    if not journaux:
                        manques.append(f"machine-{mid}/{cible}/N{n}/{nom_run} : "
                                       "AUCUN journal-dudect-*.csv — run manquant")
                        continue
                    if len(journaux) > 1:
                        manques.append(f"machine-{mid}/{cible}/N{n}/{nom_run} : "
                                       f"{len(journaux)} journaux — UN par run")
                        continue
                    try:
                        lire_journal(os.path.join(chemin_run, journaux[0]), n)
                    except ValueError as exc:
                        manques.append(str(exc))
                if len(vus) < N_RUNS_MIN:
                    manques.append(f"machine-{mid}/{cible}/N{n} : "
                                   f"{len(vus)} run(s) valide(s) — "
                                   f"{N_RUNS_MIN} exigés (n ≥ 10, gelé)")
                attendus = set(range(1, N_RUNS_MIN + 1))
                trous = sorted(attendus - vus)
                if trous:
                    manques.append(f"machine-{mid}/{cible}/N{n} : run(s) "
                                   f"manquant(s) {['run%02d' % t for t in trous]}")
    if manques:
        return None, manques
    return (temoins, machines), []


# --- l'agrégation (seulement sur un arbre COMPLET) ------------------------------

def agreger(racine):
    """Retour le dictionnaire du verdict — PRÉCONDITION : l'arbre a passé
    valider_completude (l'appelant l'exige, la fonction l'asserte)."""
    arbre, manques = valider_completude(racine)
    if manques:
        raise RuntimeError("AGRÉGAT IMPOSSIBLE — la complétude a refusé : "
                           + " ; ".join(manques[:5]))
    temoins, machines = arbre
    cellules = {}
    for mid, chemin_machine in machines:
        for cible in CIBLES:
            for n in NS:
                chemin_n = os.path.join(chemin_machine, cible, f"N{n}")
                ts = []
                for nom_run in sorted(os.listdir(chemin_n)):
                    chemin_run = os.path.join(chemin_n, nom_run)
                    if not (MOTIF_RUN.match(nom_run) and os.path.isdir(chemin_run)):
                        continue
                    journal = next(j for j in os.listdir(chemin_run)
                                   if MOTIF_JOURNAL.match(j))
                    fixe, alea = lire_journal(os.path.join(chemin_run, journal), n)
                    ts.append(t_welch(fixe, alea))
                cellules[(mid, cible, n)] = {
                    "n": len(ts),
                    "median": statistics.median(ts),
                    "ts": ts,
                }
    decision_cible = {}
    for cible in CIBLES:
        divergente = any(abs(cellules[(mid, cible, n)]["median"]) > SEUIL
                         for mid, _ in machines for n in NS)
        decision_cible[cible] = ("À DIVERGENCE AU SEUIL (au moins une cellule "
                                 "machine×N au-dessus de |t|>5 — consigné tel "
                                 "quel)" if divergente else
                                 "SANS divergence au seuil sur ces échantillons, "
                                 "ces machines (n ≥ 10 par cellule, ≥ 2 machines, "
                                 "3 N) — jamais « constant time proven »")
    return {"temoins": temoins, "machines": machines, "cellules": cellules,
            "decision_cible": decision_cible}


def rendre(verdict, racine):
    lignes = [
        "VERDIT DUDECT AGRÉGÉ (fail-closed — kit l4nnwqlld, "
        + time.strftime("%Y-%m-%d %H:%M:%S") + ")",
        f"source : {racine} — complétude VALIDÉE AVANT TOUT CALCUL "
        f"({len(verdict['machines'])} machines × {len(CIBLES)} cibles × "
        f"{len(NS)} N × n ≥ {N_RUNS_MIN} runs)",
        "",
    ]
    for mid, _ in verdict["machines"]:
        lignes.append(f"machine {mid} : témoin {verdict['temoins'][mid]} "
                      "(l'empreinte CPU et la fréquence consignées, relues)")
    lignes.append("")
    for cible in CIBLES:
        lignes.append(f"--- {cible} ---")
        for mid, _ in verdict["machines"]:
            for n in NS:
                c = verdict["cellules"][(mid, cible, n)]
                lignes.append(f"  machine-{mid} N={n} : médiane t = "
                              f"{c['median']:+.2f} sur {c['n']} runs")
        lignes.append(f"  DÉCISION : {verdict['decision_cible'][cible]}")
    lignes += [
        "",
        "frontière : dudect est un OUTIL DE DÉTECTION, pas une preuve "
        "d'exploitabilité — les canaux cachés de cache et de puissance "
        "demeurent hors périmètre ; « sans divergence au seuil » n'est jamais "
        "« constant time proven ».",
    ]
    texte = "\n".join(lignes) + "\n"
    chemin = os.path.join(racine, "verdit-dudect-%d.txt" % int(time.time()))
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)
    return chemin, texte


# --- l'autotest (fixtures SYNTHÉTIQUES — jamais des mesures réelles) ------------

def _fixture(racine, machines=("A", "B"), manque=False):
    """Construit l'arbre synthétique : partout des classes IDENTIQUES en
    distribution (t ≈ 0 attendu par construction), SAUF machine-A/tls13-02/
    N200 où la classe fixe est décalée de +1000 cycles (|t| énorme attendu
    par construction). Si manque=True : le run05 de machine-B/tls13-17/N400
    est OMIS (l'autre face du fail-closed)."""
    for mid in machines:
        os.makedirs(os.path.join(racine, f"machine-{mid}"), exist_ok=True)
        with open(os.path.join(racine, f"temoin-machine-{mid}.txt"), "w",
                  encoding="utf-8") as f:
            f.write(f"temoin machine {mid} (SYNTHÉTIQUE — autotest)\n"
                    f"empreinte CPU : FIXTURE-SYNT-{mid}\n"
                    f"fréquence : 0000 MHz (fixture)\n")
        for cible in CIBLES:
            for n in NS:
                for k in range(1, N_RUNS_MIN + 1):
                    if manque and mid == "B" and cible == "tls13-17" \
                            and n == 400 and k == 5:
                        continue
                    chemin_run = os.path.join(racine, f"machine-{mid}", cible,
                                              f"N{n}", "run%02d" % k)
                    os.makedirs(chemin_run, exist_ok=True)
                    decalle = (mid == "A" and cible == "tls13-02" and n == 200)
                    base = 100000 + 37 * k
                    with open(os.path.join(chemin_run,
                                           "journal-dudect-fix.csv"), "w",
                              newline="", encoding="utf-8") as f:
                        f.write("cible,classe,iteration,cycles,secondes\n")
                        for i in range(n):
                            bruit = (i * 37 + k * 11) % 13   # le MÊME bruit aux
                            # DEUX classes : t = 0 PAR CONSTRUCTION (le décalé
                            # seul porte l'écart +1000 construit)
                            fixe = base + (1000 if decalle else 0) + bruit
                            alea = base + bruit
                            f.write(f"{cible},fixe,{i},{fixe},0.000001\n")
                            f.write(f"{cible},aleatoire,{i},{alea},0.000001\n")


def selftest():
    ok = True
    print("=== L'AUTOTEST DE L'AGRÉGATEUR (fixtures SYNTHÉTIQUES — jamais "
          "des mesures réelles) ===")
    with tempfile.TemporaryDirectory() as tmp:
        # 1. l'arbre COMPLET : l'agrégat se calcule, les verdicts sont ceux
        #    CONSTRUITS (t ≈ 0 partout sauf la cellule décalée)
        racine = os.path.join(tmp, "runs")
        _fixture(racine, manque=False)
        arbre, manques = valider_completude(racine)
        bon = arbre is not None and not manques
        print(f"  arbre complet     : complétude "
              f"{'VALIDÉE' if bon else 'REFUSÉE ' + str(manques[:2])} -> "
              f"{'OK' if bon else 'ÉCART'}")
        ok &= bon
        if bon:
            verdict = agreger(racine)
            cel = verdict["cellules"]
            bon = (abs(cel[("A", "tls13-02", 60)]["median"]) < 2.0
                   and abs(cel[("A", "tls13-02", 200)]["median"]) > SEUIL
                   and abs(cel[("B", "tls13-13", 400)]["median"]) < 2.0
                   and cel[("A", "tls13-02", 60)]["n"] == N_RUNS_MIN)
            print(f"  cellules calculées : médianes t = "
                  f"A/tls13-02/N60 {cel[('A', 'tls13-02', 60)]['median']:+.2f} "
                  f"(≈0 attendu), A/tls13-02/N200 "
                  f"{cel[('A', 'tls13-02', 200)]['median']:+.1f} "
                  f"(>>+5 attendu, décalage +1000 construit), "
                  f"B/tls13-13/N400 "
                  f"{cel[('B', 'tls13-13', 400)]['median']:+.2f} (≈0 attendu) "
                  f"-> {'OK' if bon else 'ÉCART'}")
            ok &= bon
            bon = ("À DIVERGENCE" in verdict["decision_cible"]["tls13-02"]
                   and "SANS divergence" in verdict["decision_cible"]["tls13-13"]
                   and "SANS divergence" in verdict["decision_cible"]["tls13-17"])
            print(f"  décision par cible : tls13-02 À DIVERGENCE, tls13-13/16/17 "
                  f"SANS divergence (attendus par construction) -> "
                  f"{'OK' if bon else 'ÉCART'}")
            ok &= bon
    with tempfile.TemporaryDirectory() as tmp:
        # 2. UN SEUL RUN MANQUANT : REFUS, AUCUN AGRÉGAT PARTIEL
        racine = os.path.join(tmp, "runs")
        _fixture(racine, manque=True)
        arbre, manques = valider_completude(racine)
        bon = arbre is None and len(manques) >= 1 \
            and any("machine-B/tls13-17/N400" in m and "run05" in m
                    for m in manques)
        detail = next((m for m in manques if "run05" in m),
                      manques[0] if manques else "aucun manque ?!")
        print(f"  UN run manquant   : REFUS ({detail}) -> "
              f"{'OK' if bon else 'ÉCART'}")
        ok &= bon
        try:
            agreger(racine)
            print("  agrégat partiel   : CALCULÉ — ÉCART (la règle de fer "
                  "violée)")
            ok = False
        except RuntimeError:
            print("  agrégat partiel   : IMPOSSIBLE (RuntimeError nommé) -> OK")
    with tempfile.TemporaryDirectory() as tmp:
        # 3. un TÉMOIN MACHINE MUET (sans empreinte CPU) : REFUS aussi
        racine = os.path.join(tmp, "runs")
        _fixture(racine)
        with open(os.path.join(racine, "temoin-machine-B.txt"), "w",
                  encoding="utf-8") as f:
            f.write("temoin muet (la fixture du refus) — rien de consigné\n")
        arbre, manques = valider_completude(racine)
        bon = arbre is None and any("temoin-machine-B" in m for m in manques)
        print(f"  témoin muet       : REFUS "
              f"({len(manques)} manque(s) nommé(s)) -> {'OK' if bon else 'ÉCART'}")
        ok &= bon
    print(f"[autotest] {'VERT' if ok else 'ROUGE'} — la règle de fer : tout "
          f"run manquant = REFUS, la complétude AVANT TOUT calcul")
    return ok


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        return 0 if selftest() else 2
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    racine = sys.argv[1]
    arbre, manques = valider_completude(racine)
    if manques:
        print("REFUS (fail-closed) — LE PROTOCOLE EST REFUSÉ, AUCUN AGRÉGAT "
              "PARTIEL :")
        for m in manques:
            print(f"  - {m}")
        print(f"({len(manques)} manque(s)) — compléter les runs puis relancer ; "
              "jamais d'agrégat sur ce qui existe.")
        return 2
    verdict = agreger(racine)
    chemin, texte = rendre(verdict, racine)
    print(texte)
    print(f"[sortie] {chemin} — à signer (la grille du kit) et à déposer au "
          "coffre avec runs/ entier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
