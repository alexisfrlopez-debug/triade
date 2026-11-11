#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jouer_tous_les_runs.py — TOUS LES RUNS TLC/APALACHE DU PAQUET TLA+
(6zqo2h60n), journalisés et verdictés (aucune valeur gravée : les verdicts
sont LUS des journaux d'outils).

Les runs (dans le répertoire de CE script — le rend rejouable depuis un
clone frais) :
  TLC 1 — CF3Fidelite (plafond v120 + profondeur 6 + vue abstraite) :
          attendu 154 états distincts (les comptes D187 EXACTS) ;
  TLC 2 — CF3Plafond (exploration COMPLÈTE du plafond) : attendu 216 ;
  TLC 3 — CF3 bornes étendues (spec NON bornée, contrainte e ≤ 5) :
          attendu 360, Inv + AucuneViolation sans violation ;
  APA 1 — Apalache cas de base : Init ⟹ Inv (NoError attendu) ;
  APA 2 — Apalache PAS INDUCTIF : Inv ∧ Next ⟹ Inv′ sur Int NON BORNÉS
          (NoError attendu — LE DÉCHARGEMENT) ;
  APA 3 — contrôle négatif C1 : l'invariant AFFAIBLI (sans sait ⊆
          Elements) doit PRODUIRE un contre-exemple (Error 12 attendu —
          la non-vacuité : Cardinality est réellement raisonné) ;
  APA 4 — contrôle négatif C2 : le prédicat FAUX dès l'initial
          (Error 12 attendu).

Sorties : logs/*.txt (les journaux bruts), verdicts.json (la synthèse
LUE des journaux — la pièce que lit la table des statuts).
"""
import json
import pathlib
import re
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
OUTILS = ICI / "outils"
LOGS = ICI / "logs"
LOGS.mkdir(exist_ok=True)

TLC = ["java", "-jar", str(OUTILS / "tla2tools.jar")]
APA = [str(OUTILS / "apalache-0.63.0" / "bin" / "apalache-mc")]


def run(nom: str, cmd: list[str], timeout: int = 300) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       cwd=ICI)
    journal = (f"$ {' '.join(cmd)}\n\n--- stdout ---\n{r.stdout}\n"
               f"--- stderr ---\n{r.stderr}")
    (LOGS / f"{nom}.txt").write_text(journal, encoding="utf-8")
    return r.stdout + r.stderr


def main() -> int:
    verdicts = {}

    # --- TLC : les trois configurations ---
    v = run("tlc_fidelite",
            TLC + ["-deadlock", "-config", "CF3Fidelite.cfg",
                   "CF3Fidelite.tla"])
    m = re.search(r"(\d+) distinct states found", v)
    verdicts["tlc_fidelite_etats"] = int(m.group(1)) if m else None
    verdicts["tlc_fidelite_d187"] = (
        verdicts["tlc_fidelite_etats"] == 154
        and "No error has been found" in v)

    v = run("tlc_plafond",
            TLC + ["-deadlock", "-config", "CF3Plafond.cfg",
                   "CF3Plafond.tla"])
    m = re.search(r"(\d+) distinct states found", v)
    verdicts["tlc_plafond_etats"] = int(m.group(1)) if m else None
    verdicts["tlc_plafond_inv"] = (
        verdicts["tlc_plafond_etats"] == 216
        and "No error has been found" in v)

    v = run("tlc_bornes", TLC + ["-config", "CF3Bornes.cfg", "CF3.tla"])
    m = re.search(r"(\d+) distinct states found", v)
    verdicts["tlc_bornes_etats"] = int(m.group(1)) if m else None
    verdicts["tlc_bornes_inv"] = (
        verdicts["tlc_bornes_etats"] == 360
        and "No error has been found" in v)

    # --- Apalache : la base, le pas inductif, les contrôles ---
    v = run("apalache_base",
            APA + ["check", "--config=MCA_base.cfg", "--length=1",
                   "CF3.tla"])
    verdicts["apalache_base"] = ("The outcome is: NoError" in v
                                 and "EXITCODE: OK" in v)

    v = run("apalache_inductif",
            APA + ["check", "--config=MCA_ind.cfg", "--length=1",
                   "CF3.tla"])
    verdicts["apalache_inductif"] = ("The outcome is: NoError" in v
                                     and "EXITCODE: OK" in v)
    # la preuve que le prédicat d'initialisation ÉTAIT Inv (pas écrasé
    # par la config) : lue du journal
    verdicts["apalache_inductif_init_inv"] = (
        "Set the initialization predicate to Inv" in v)

    v = run("apalache_controle_c1",
            APA + ["check", "--config=MCA_faible.cfg", "--length=1",
                   "CF3Controle.tla"])
    verdicts["apalache_controle_c1_attrape"] = (
        "state invariant 2 violated" in v or "state invariant" in v
        and "violated" in v) and "EXITCODE: ERROR (12)" in v

    v = run("apalache_controle_c2",
            APA + ["check", "--config=MCA_base.cfg", "--inv=Faux",
                   "--length=0", "CF3Controle.tla"])
    verdicts["apalache_controle_c2_attrape"] = (
        "violated" in v and "EXITCODE: ERROR (12)" in v)

    (ICI / "verdicts.json").write_text(
        json.dumps(verdicts, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print(json.dumps(verdicts, ensure_ascii=False, indent=1))
    tous = [verdicts["tlc_fidelite_d187"], verdicts["tlc_plafond_inv"],
            verdicts["tlc_bornes_inv"], verdicts["apalache_base"],
            verdicts["apalache_inductif"],
            verdicts["apalache_inductif_init_inv"],
            verdicts["apalache_controle_c1_attrape"],
            verdicts["apalache_controle_c2_attrape"]]
    print(f"\n[verdict global] {sum(tous)}/{len(tous)} VERT")
    return 0 if all(tous) else 1


if __name__ == "__main__":
    sys.exit(main())
