#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jouer_batterie_89488hblm.py — LA BATTERIE INTÉGRALE DU CHANTIER 89488hblm,
DISPATCHABLE PAR PHASE (le bac fauche les processus entre les messages :
chaque appel d'outil est borné, chaque phase tient en un appel).

Les phases (PLAN-89488hblm.md gelé au dcb2d56, l'amendement 2 au 8c831b6,
le correctif au 5247c35) :
  A          — LE CLONE FRAIS : les 7 runs originaux rejoués ; les 11
               clefs du verdicts.json consigné BIT-IDENTIQUES (8/8 VERT) ;
  B-garde    — 13 obligations GARDE (SMT, longueur 0) ;
  B-image    — 13 obligations IMAGE (SMT, longueur 1) ;
  B-activation — 13 obligations ACTIVATION (SMT, longueur 1) ;
  B-rest     — OB1 + OB2 + LT1 + LT2 (SMT) ;
  C-garde    — 13 contrôles GARDE (Error 12 attendus) ;
  C-effet    — 13 contrôles IMAGE (Error 12 attendus) ;
  C-rest     — CB1 + CB2 + CC1 + CC2 (Error 12 attendus) ;
  D-epinglage — l'épinglage TLC des 13 règles (aucun deadlock ni
               violation — les DEUX sens) ;
  D-rest     — le contrôle d'épinglage (deadlock attendu) + le compte
               288 (TLC) + le verifie_couverture_288.py du clone.

  Usage : jouer_batterie_89488hblm.py PHASE [DEBUT FIN]
          (DEBUT/FIN : l'intervalle d'indices de règles, pour trancher
          davantage — défaut 0..13)

Tout verdict est LU des journaux d'outils (aucune valeur gravée). Le
rapport s'accumule à travers les phases (RAPPORT-BATTERIE-A-D.txt).
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ATELIER = pathlib.Path(__file__).resolve().parent
REPO = ATELIER.parents[0]
OUTILS = REPO / "scripts" / "tla_v150" / "outils"
CLONE = pathlib.Path("/tmp/triade-cf3")
LOGS = ATELIER / "logs"
LOGS.mkdir(exist_ok=True)

TLC = ["java", "-jar", str(OUTILS / "tla2tools.jar")]
APA = [str(OUTILS / "apalache-0.63.0" / "bin" / "apalache-mc")]

REGLES = ["VoleKUser", "VoleSSerrure", "VoleSPiege", "FalsifieConteneur",
          "FalsifiePiege", "RejoueEpoquePassee", "OuvrirCorrect",
          "OuvrirPhraseErronee", "OuvrirAncienCouple", "Verifier",
          "CrashPendantSession", "CloturerCorrecte", "CloturerPhraseErronee"]

RAPPORT: list[str] = []
NB_VERT = 0
NB_TOTAL = 0


def ver(nom: str, ok: bool, detail: str = "") -> bool:
    global NB_VERT, NB_TOTAL
    NB_TOTAL += 1
    RAPPORT.append(f"  {'VERT' if ok else 'ROUGE'}  {nom}"
                   + (f" — {detail}" if detail else ""))
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom} {detail}", flush=True)
    if ok:
        NB_VERT += 1
    return ok


def run(nom: str, cmd: list[str], cwd: pathlib.Path, timeout: int = 420):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       cwd=str(cwd))
    journal = (f"$ {' '.join(cmd)}\n\n--- stdout ---\n{r.stdout}\n"
               f"--- stderr ---\n{r.stderr}")
    (LOGS / f"{nom}.txt").write_text(journal, encoding="utf-8")
    return r.stdout + r.stderr


def apa_noerror(nom: str, config: str, module: str, extra: list[str]) -> bool:
    out = run(nom, APA + ["check", f"--config={config}", *extra,
                          module + ".tla"], ATELIER)
    return ver(nom, ("The outcome is: NoError" in out
                     and "EXITCODE: OK" in out))


def apa_attrape(nom: str, config: str, module: str, extra: list[str]) -> bool:
    out = run(nom, APA + ["check", f"--config={config}", *extra,
                          module + ".tla"], ATELIER)
    return ver(nom, ("EXITCODE: ERROR (12)" in out and "violated" in out))


def phase_A() -> None:
    print("=== A — LE CLONE FRAIS : LES 7 RUNS ORIGINAUX REJOUÉS ===")
    orig = json.loads((REPO / "scripts" / "tla_v150" / "verdicts.json")
                      .read_text(encoding="utf-8"))
    run("A_clone_batterie", ["python3", "jouer_tous_les_runs.py"],
        CLONE / "scripts" / "tla_v150", timeout=1800)
    rejoue_path = CLONE / "scripts" / "tla_v150" / "verdicts.json"
    rejoue = json.loads(rejoue_path.read_text(encoding="utf-8"))
    ver("A. les 7 runs originaux : verdicts BIT-IDENTIQUES (11 clefs)",
        rejoue == orig,
        f"{sum(1 for k in orig if rejoue.get(k) == orig[k])}/{len(orig)}")
    texte_orig = (REPO / "scripts" / "tla_v150" / "verdicts.json"
                  ).read_text(encoding="utf-8").strip()
    ver("A. le verdicts.json rejeté : le TEXTE bit-identique",
        texte_orig == rejoue_path.read_text(encoding="utf-8").strip())
    if rejoue != orig:
        for k in orig:
            if rejoue.get(k) != orig[k]:
                print(f"    divergence {k}: {orig[k]!r} → {rejoue.get(k)!r}")


def main() -> int:
    phase = sys.argv[1] if len(sys.argv) > 1 else "TOUS"
    debut = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    fin = int(sys.argv[3]) if len(sys.argv) > 3 else 13

    if phase in ("A", "TOUS"):
        phase_A()
    if phase in ("B-garde", "TOUS"):
        print("=== B — LES OBLIGATIONS GARDE (NoError attendus) ===")
        for r in REGLES[debut:fin]:
            apa_noerror(f"B_equiv_garde_{r}", f"MCEg_{r}.cfg", "CF3Equiv",
                        ["--length=0"])
    if phase in ("B-image", "TOUS"):
        print("=== B — LES OBLIGATIONS IMAGE (NoError attendus) ===")
        for r in REGLES[debut:fin]:
            apa_noerror(f"B_equiv_image_{r}", f"MCEi_{r}.cfg", "CF3Equiv",
                        ["--length=1", "--no-deadlock"])
    if phase in ("B-activation", "TOUS"):
        print("=== B — LES OBLIGATIONS ACTIVATION (NoError attendus) ===")
        for r in REGLES[debut:fin]:
            apa_noerror(f"B_equiv_activation_{r}", f"MCEa_{r}.cfg",
                        "CF3Equiv", ["--length=1", "--no-deadlock"])
    if phase in ("B-rest", "TOUS"):
        print("=== B — O3 ET TRANSLATION (NoError attendus) ===")
        apa_noerror("B_o3_couverture", "MCO_ob1.cfg", "CF3O3",
                    ["--length=0"])
        apa_noerror("B_o3_non_vacuite", "MCO_ob2.cfg", "CF3O3",
                    ["--length=0"])
        apa_noerror("B_translation_gardes", "MCT_lt1.cfg", "CF3Translation",
                    ["--length=0"])
        apa_noerror("B_translation_effets", "MCT_lt2.cfg", "CF3Translation",
                    ["--length=1", "--no-deadlock"])
    if phase in ("C-garde", "TOUS"):
        print("=== C — LES CONTRÔLES GARDE (Error 12 attendus) ===")
        for r in REGLES[debut:fin]:
            apa_attrape(f"C_controle_garde_{r}", f"MCCg_{r}.cfg",
                        "CF3EquivControles", ["--length=0"])
    if phase in ("C-effet", "TOUS"):
        print("=== C — LES CONTRÔLES IMAGE (Error 12 attendus) ===")
        for r in REGLES[debut:fin]:
            apa_attrape(f"C_controle_effet_{r}", f"MCCi_{r}.cfg",
                        "CF3EquivControles", ["--length=1", "--no-deadlock"])
    if phase in ("C-rest", "TOUS"):
        print("=== C — LES CONTRÔLES O3/TRANSLATION (Error 12 attendus) ===")
        apa_attrape("C_controle_o3_couverture", "MCO_cb1.cfg", "CF3O3",
                    ["--length=0"])
        apa_attrape("C_controle_o3_non_vacuite", "MCO_cb2.cfg", "CF3O3",
                    ["--length=0"])
        apa_attrape("C_controle_translation_gardes", "MCT_cc1.cfg",
                    "CF3Translation", ["--length=0"])
        apa_attrape("C_controle_translation_effets", "MCT_cc2.cfg",
                    "CF3Translation", ["--length=1", "--no-deadlock"])
    if phase in ("D-epinglage", "TOUS"):
        print("=== D — L'ÉPINGLAGE TLC (les DEUX sens) ===")
        for r in REGLES[debut:fin]:
            out = run(f"D_epinglage_{r}",
                      TLC + ["-nowarning", "-config", f"MTLP_{r}.cfg",
                             "CF3Equiv.tla"], ATELIER, timeout=600)
            ver(f"D. l'épinglage TLC {r} : les DEUX sens (aucun deadlock, "
                "aucune violation)",
                ("No error has been found" in out
                 and "Deadlock" not in out and "Error" not in out))
    if phase in ("D-rest", "TOUS"):
        print("=== D — LE CONTRÔLE D'ÉPINGLAGE + LE COMPTE 288 ===")
        out = run("D_epinglage_controle",
                  TLC + ["-nowarning", "-config", "MTLP_ctl.cfg",
                         "CF3EquivControles.tla"], ATELIER, timeout=600)
        ver("D. le contrôle d'épinglage : le deadlock ATTRAPÉ",
            "Deadlock reached" in out)
        out = run("D_tlc_o3_compte",
                  TLC + ["-deadlock", "-nowarning", "-config", "MCO.cfg",
                         "CF3O3.tla"], ATELIER, timeout=300)
        m = re.search(r"(\d+) distinct states found", out)
        ver("D. l'énumération TLC des formes : 288",
            m is not None and m.group(1) == "288",
            f"{m.group(1) if m else '?'} états distincts")
        out = run("D_python_couverture_288",
                  ["python3", "verifie_couverture_288.py"],
                  CLONE / "scripts" / "vague5", timeout=300)
        ver("D. le verifie_couverture_288.py du clone : BIJECTION VERT",
            "VERT" in out and "REFUS" not in out)

    # le bilan (le rapport s'accumule à travers les phases)
    entete = (f"LA BATTERIE 89488hblm — phase {phase} [{debut}:{fin}] : "
              f"{NB_VERT}/{NB_TOTAL} VERT")
    chemin = ATELIER / "RAPPORT-BATTERIE-A-D.txt"
    anciennes = []
    if chemin.is_file():
        for ligne in chemin.read_text(encoding="utf-8").splitlines():
            if ligne.startswith("LA BATTERIE") or not ligne.strip():
                continue
            anciennes.append(ligne)
    deja = {l.split("  ", 1)[-1] for l in anciennes}
    nouvelles = [l for l in RAPPORT if l.split("  ", 1)[-1] not in deja]
    chemin.write_text("\n".join([entete] + nouvelles + anciennes) + "\n",
                      encoding="utf-8")
    print(f"\n[verdict {phase}] {NB_VERT}/{NB_TOTAL} VERT")
    return 0 if NB_VERT == NB_TOTAL else 1


if __name__ == "__main__":
    sys.exit(main())
