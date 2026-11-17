#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jouer_batterie_89488hblm.py — LA BATTERIE INTÉGRALE DU CHANTIER 89488hblm
(le plan pré-enregistré, phases A-D puis l'assemblage ; la phase E — la
campagne 10 000 traces — vit en arrière-plan, son résultat lu à l'assemblage
par assembler_verdicts_89488hblm.py).

Les phases (le PLAN-89488hblm.md, gelé au dcb2d56, l'amendement 780033a) :
  A — LE CLONE FRAIS : les 7 runs originaux rejoués (le jouer_tous_les_runs
      du clone) ; les 11 clefs du verdicts.json consigné BIT-IDENTIQUES ;
  B — LES 30 OBLIGATIONS NOUVELLES : 13 équivalences garde + 13 effet +
      OB1 + OB2 + LT1 + LT2 — NoError attendus ;
  C — LES 30 CONTRÔLES NÉGATIFS : 13 + 13 + CB1 + CB2 + CC1 + CC2 —
      Error 12 attendus (chaque affaiblissement ATTRAPÉ) ;
  D — LE COMPTE 288 : l'énumération TLC + le verifie_couverture_288.py du
      clone (via le lien /tmp/triade-gh).

Aucune valeur gravée : tout verdict est LU des journaux d'outils. Échec
fermé : un seul rouge arrête la batterie (le rapport porte le détail).
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
VERTS: list[str] = []


def ver(nom: str, ok: bool, detail: str = "") -> bool:
    RAPPORT.append(f"  {'VERT' if ok else 'ROUGE'}  {nom}"
                   + (f" — {detail}" if detail else ""))
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom} {detail}", flush=True)
    if ok:
        VERTS.append(nom)
    return ok


def run(nom: str, cmd: list[str], cwd: pathlib.Path, timeout: int = 420):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       cwd=str(cwd))
    journal = (f"$ {' '.join(cmd)}\n\n--- stdout ---\n{r.stdout}\n"
               f"--- stderr ---\n{r.stderr}")
    (LOGS / f"{nom}.txt").write_text(journal, encoding="utf-8")
    return r.stdout + r.stderr


def apalache_noerror(nom: str, args: list[str], module: str) -> bool:
    out = run(nom, APA + ["check"] + args + [module + ".tla"], ATELIER)
    return ver(nom, ("The outcome is: NoError" in out
                     and "EXITCODE: OK" in out))


def apalache_attrape(nom: str, args: list[str], module: str) -> bool:
    out = run(nom, APA + ["check"] + args + [module + ".tla"], ATELIER)
    return ver(nom, ("EXITCODE: ERROR (12)" in out and "violated" in out))


def main() -> int:
    tous: list[bool] = []

    # ------------------------------------------------------------------ A
    print("=== A — LE CLONE FRAIS : LES 7 RUNS ORIGINAUX REJOUÉS ===")
    orig = json.loads((REPO / "scripts" / "tla_v150" / "verdicts.json")
                      .read_text(encoding="utf-8"))
    out = run("A_clone_batterie",
              ["python3", "jouer_tous_les_runs.py"],
              CLONE / "scripts" / "tla_v150", timeout=1800)
    rejoue_path = CLONE / "scripts" / "tla_v150" / "verdicts.json"
    rejoue = json.loads(rejoue_path.read_text(encoding="utf-8"))
    identiques = (rejoue == orig)
    tous.append(ver("A. les 7 runs originaux : verdicts BIT-IDENTIQUES "
                    "au consigné (11 clefs)", identiques,
                    f"{sum(1 for k in orig if rejoue.get(k) == orig[k])}"
                    f"/{len(orig)} clefs"))
    texte_orig = (REPO / "scripts" / "tla_v150" / "verdicts.json"
                  ).read_text(encoding="utf-8").strip()
    texte_rej = rejoue_path.read_text(encoding="utf-8").strip()
    tous.append(ver("A. le verdicts.json rejeté : le TEXTE bit-identique",
                    texte_orig == texte_rej))
    if not identiques:
        for k in orig:
            if rejoue.get(k) != orig[k]:
                print(f"    divergence {k}: {orig[k]!r} → {rejoue.get(k)!r}")

    # ------------------------------------------------------------------ B
    print("=== B — LES 30 OBLIGATIONS NOUVELLES (NoError attendus) ===")
    for r in REGLES:
        tous.append(apalache_noerror(
            f"B_equiv_garde_{r}",
            ["--config=MCE.cfg", "--init=TypeOK",
             f"--inv=OblGarde_{r}", "--length=0"], "CF3Equiv"))
    for r in REGLES:
        tous.append(apalache_noerror(
            f"B_equiv_effet_{r}",
            ["--config=MCD.cfg", "--init=InitTypeOKdiff",
             f"--next=NextDiff_{r}", "--inv=DiffInv", "--length=1",
             "--no-deadlock"], "CF3EquivDiff"))
    tous.append(apalache_noerror(
        "B_o3_couverture", ["--config=MCO.cfg", "--init=Inv",
                            "--inv=OblOB1", "--length=0"], "CF3O3"))
    tous.append(apalache_noerror(
        "B_o3_non_vacuite", ["--config=MCO.cfg", "--init=FormeDomaineEtat",
                             "--inv=OblOB2", "--length=0"], "CF3O3"))
    tous.append(apalache_noerror(
        "B_translation_gardes", ["--config=MCT.cfg", "--init=InitLT",
                                 "--inv=LT1", "--length=0"],
        "CF3Translation"))
    tous.append(apalache_noerror(
        "B_translation_effets", ["--config=MCT.cfg", "--init=InitLT",
                                 "--next=NextLTScelle", "--inv=Couplage",
                                 "--length=1", "--no-deadlock"],
        "CF3Translation"))

    # ------------------------------------------------------------------ C
    print("=== C — LES 30 CONTRÔLES NÉGATIFS (Error 12 attendus) ===")
    for r in REGLES:
        tous.append(apalache_attrape(
            f"C_controle_garde_{r}",
            ["--config=MCE.cfg", "--init=TypeOK",
             f"--inv=OblFaibleGarde_{r}", "--length=0"],
            "CF3EquivControles"))
    for r in REGLES:
        tous.append(apalache_attrape(
            f"C_controle_effet_{r}",
            ["--config=MCDc.cfg", "--init=InitTypeOKdiffC",
             f"--next=NextDiffw_{r}", "--inv=DiffInvC", "--length=1",
             "--no-deadlock"], "CF3EquivDiffC"))
    tous.append(apalache_attrape(
        "C_controle_o3_couverture", ["--config=MCO.cfg", "--init=InvSansI4",
                                     "--inv=OblOB1", "--length=0"], "CF3O3"))
    tous.append(apalache_attrape(
        "C_controle_o3_non_vacuite", ["--config=MCO.cfg",
                                      "--init=FormDomainFaible",
                                      "--inv=OblOB2", "--length=0"],
        "CF3O3"))
    tous.append(apalache_attrape(
        "C_controle_translation_gardes", ["--config=MCT.cfg",
                                          "--init=InitLTfaible",
                                          "--inv=LT1", "--length=0"],
        "CF3Translation"))
    tous.append(apalache_attrape(
        "C_controle_translation_effets", ["--config=MCT.cfg",
                                          "--init=InitLT",
                                          "--next=NextLTplafond",
                                          "--inv=Couplage", "--length=1",
                                          "--no-deadlock"],
        "CF3Translation"))

    # ------------------------------------------------------------------ D
    print("=== D — LE COMPTE 288 (ÉNUMÉRÉ, par deux outils) ===")
    out = run("D_tlc_o3_compte",
              TLC + ["-deadlock", "-nowarning", "-config", "MCO.cfg",
                     "CF3O3.tla"], ATELIER, timeout=300)
    m = re.search(r"(\d+) distinct states found", out)
    compte_tlc = int(m.group(1)) if m else None
    tous.append(ver("D. l'énumération TLC des formes : 288",
                    compte_tlc == 288, f"{compte_tlc} états distincts"))
    out = run("D_python_couverture_288",
              ["python3", "verifie_couverture_288.py"],
              CLONE / "scripts" / "vague5", timeout=300)
    tous.append(ver("D. le verifie_couverture_288.py du clone : BIJECTION "
                    "VERT", "VERT" in out and "REFUS" not in out))

    # ------------------------------------------------------------------ bilan
    nb_vert = sum(tous)
    RAPPORT.insert(0, f"LA BATTERIE 89488hblm — PHASES A-D : "
                      f"{nb_vert}/{len(tous)} VERT")
    (ATELIER / "RAPPORT-BATTERIE-A-D.txt").write_text(
        "\n".join(RAPPORT) + "\n", encoding="utf-8")
    print(f"\n[verdict A-D] {nb_vert}/{len(tous)} VERT")
    return 0 if nb_vert == len(tous) else 1


if __name__ == "__main__":
    sys.exit(main())
