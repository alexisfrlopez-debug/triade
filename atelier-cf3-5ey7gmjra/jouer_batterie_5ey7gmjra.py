#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jouer_batterie_5ey7gmjra.py — LA BATTERIE DE L'INSTRUCTION 5ey7gmjra :
le programme de preuve étendu (la falsification en session), DISPATCHÉE
EN LOT PARALLÈLE (le bac fauche les processus ENTRE les appels : chaque
lot vit DANS un appel, les jobs d'un lot courent N à la fois — chaque
job reste un appel d'outil borné et journalisé).

Les lots :
  A          — la fidélité : TLC scellé (154/896) + diff au consigné,
               TLC étendu, les DEUX modèles Python ;
  B1..B4     — Apalache CF3Etendu (base, inductif) ; les 13 GARDE ;
               les 13 IMAGE ; les 13 ACTIVATION ; LT1/LT2 ; OB1/OB2 ;
  C1..C3     — les contrôles GARDE (13) ; les contrôles IMAGE (13) ;
               le contrôle inductif (le débordement) + CC1/CC2/CB1/CB2 ;
  D          — les 13 épinglages TLC + le contrôle du pin + le compte
               288.

Usage : jouer_batterie_5ey7gmjra.py LOT
Tout verdict est LU des journaux d'outils (aucune valeur gravée).
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import pathlib
import re
import subprocess
import sys

ATELIER = pathlib.Path(__file__).resolve().parent
REPO = ATELIER.parents[0]
OUTILS = ATELIER / "outils"
LOGS = ATELIER / "logs"
LOGS.mkdir(exist_ok=True)

TLC = ["java", "-jar", str(OUTILS / "tla2tools.jar")]
APA = [str(OUTILS / "apalache-0.63.0" / "bin" / "apalache-mc")]
N_PARALLELE = 3

REGLES = ["VoleKUser", "VoleSSerrure", "VoleSPiege", "FalsifieConteneur",
          "FalsifiePiege", "RejoueEpoquePassee", "OuvrirCorrect",
          "OuvrirPhraseErronee", "OuvrirAncienCouple", "Verifier",
          "CrashPendantSession", "CloturerCorrecte", "CloturerPhraseErronee"]

VERDICTS: dict[str, bool] = {}
RAPPORT: list[str] = []


def ver(nom: str, ok: bool, detail: str = "") -> bool:
    VERDICTS[nom] = ok
    RAPPORT.append(f"  {'VERT' if ok else 'ROUGE'}  {nom}"
                   + (f" — {detail}" if detail else ""))
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom} {detail}", flush=True)
    return ok


def run(nom: str, cmd: list[str], timeout: int = 600):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       cwd=str(ATELIER))
    journal = (f"$ {' '.join(cmd)}\n\n--- stdout ---\n{r.stdout}\n"
               f"--- stderr ---\n{r.stderr}")
    (LOGS / f"{nom}.txt").write_text(journal, encoding="utf-8")
    return r.stdout + r.stderr


# les jobs : (nom, attendu 'NoError'|'Error12'|..., commande)
APA_JOBS: list[tuple[str, str, list[str]]] = []


def apa(nom: str, attendu: str, config: str, module: str, extra: list[str]):
    APA_JOBS.append((nom, attendu,
                     APA + ["check", f"--config={config}", *extra,
                            module + ".tla"]))


def lot_A() -> None:
    print("=== A — LA FIDÉLITÉ : LA CHAÎNE SCELLÉE PUIS L'ÉTENDUE ===")
    out = run("A_tlc_fidelite_scellee",
              TLC + ["-deadlock", "-config", "CF3Fidelite.cfg",
                     "CF3Fidelite.tla"])
    m = re.search(r"(\d+) states generated, (\d+) distinct states found",
                  out)
    ver("A. TLC la chaîne SCELLÉE : 154 états distincts",
        m is not None and m.group(2) == "154",
        f"{m.group(1)} générés / {m.group(2)} distincts" if m else "?")
    ver("A. le journal TLC scellé : la profondeur 7, aucun état en file",
        "depth of the complete state graph search is 7" in out
        and "Model checking completed" in out
        and "0 states left on queue" in out)

    out = run("A_tlc_fidelite_etendue",
              TLC + ["-deadlock", "-config", "CF3FideliteEtendu.cfg",
                     "CF3FideliteEtendu.tla"])
    m = re.search(r"(\d+) states generated, (\d+) distinct states found",
                  out)
    ver("A. TLC la chaîne ÉTENDUE : l'espace atteignable INVARIANT "
        "(154 états distincts — l'extension n'ajoute AUCUN état)",
        m is not None and m.group(2) == "154",
        f"{m.group(1)} générés / {m.group(2)} distincts (les transitions "
        f"tirées croissent : la falsification offerte en session)"
        if m else "?")

    out = run("A_python_scelle",
              ["python3", str(REPO / "scripts/preuves_v150/"
                              "modele_invariant_v150.py")], timeout=1800)
    ver("A. le modèle Python SCELLÉ : 154/1152 D187 REPRODUIT",
        "154 états / 1152 transitions — D187 REPRODUIT" in out)
    out = run("A_python_etendu",
              ["python3", str(ATELIER / "modele_invariant_v153.py")],
              timeout=1800)
    ver("A. le modèle Python ÉTENDU : la fidélité + les preuves + "
        "l'uniformité",
        "154 états / 1152 transitions — D187 REPRODUIT" in out
        and "0 violation(s)" in out and "UNIFORME" in out)


def construire_B():
    apa("B_apalache_base_etendu", "NoError", "MEE_base.cfg", "CF3Etendu",
        ["--length=0"])
    apa("B_apalache_inductif_etendu", "NoError", "MEE_ind.cfg", "CF3Etendu",
        ["--length=1", "--no-deadlock"])
    for r in REGLES:
        apa(f"B_equiv_garde_{r}", "NoError", f"MEEg_{r}.cfg",
            "CF3EquivEtendu", ["--length=0"])
        apa(f"B_equiv_image_{r}", "NoError", f"MEEi_{r}.cfg",
            "CF3EquivEtendu", ["--length=1", "--no-deadlock"])
        apa(f"B_equiv_activation_{r}", "NoError", f"MEEa_{r}.cfg",
            "CF3EquivEtendu", ["--length=1", "--no-deadlock"])
    apa("B_translation_gardes_etendu", "NoError", "MET_lt1.cfg",
        "CF3TranslationEtendu", ["--length=0"])
    apa("B_translation_effets_etendu", "NoError", "MET_lt2.cfg",
        "CF3TranslationEtendu", ["--length=1", "--no-deadlock"])
    apa("B_o3_couverture", "NoError", "MCO_ob1.cfg", "CF3O3", ["--length=0"])
    apa("B_o3_non_vacuite", "NoError", "MCO_ob2.cfg", "CF3O3", ["--length=0"])


def construire_C():
    for r in REGLES:
        apa(f"C_controle_garde_{r}", "Error12", f"MCCg_{r}.cfg",
            "CF3EquivControlesEtendu", ["--length=0"])
        apa(f"C_controle_effet_{r}", "Error12", f"MCCi_{r}.cfg",
            "CF3EquivControlesEtendu", ["--length=1", "--no-deadlock"])
    apa("C_controle_inductif_debordant", "Error12", "MEE_ctl.cfg",
        "CF3EtenduDebordant", ["--length=1", "--no-deadlock"])
    apa("C_controle_translation_gardes", "Error12", "MET_cc1.cfg",
        "CF3TranslationEtendu", ["--length=0"])
    apa("C_controle_translation_effets", "Error12", "MET_cc2.cfg",
        "CF3TranslationEtendu", ["--length=1", "--no-deadlock"])
    apa("C_controle_o3_couverture", "Error12", "MCO_cb1.cfg", "CF3O3",
        ["--length=0"])
    apa("C_controle_o3_non_vacuite", "Error12", "MCO_cb2.cfg", "CF3O3",
        ["--length=0"])


def jouer_lot_apa(attendus: set[str] | None = None) -> None:
    jobs = [(n, a, c) for (n, a, c) in APA_JOBS
            if attendus is None or n in attendus]
    print(f"--- {len(jobs)} jobs Apalache, {N_PARALLELE} à la fois ---",
          flush=True)

    def un_job(job):
        nom, attendu, cmd = job
        out = run(nom, cmd)
        return nom, attendu, out

    with cf.ThreadPoolExecutor(max_workers=N_PARALLELE) as ex:
        for nom, attendu, out in ex.map(un_job, jobs):
            if attendu == "NoError":
                ver(nom, "The outcome is: NoError" in out
                    and "EXITCODE: OK" in out)
            else:
                ver(nom, "EXITCODE: ERROR (12)" in out and "violated" in out)


def lot_D() -> None:
    print("=== D — L'ÉPINGLAGE TLC (les DEUX sens) + LE COMPTE 288 ===")

    def un_epinglage(r):
        out = run(f"D_epinglage_{r}",
                  TLC + ["-nowarning", "-config", f"MTLP_{r}.cfg",
                         "CF3EquivEtendu.tla"])
        return r, out

    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        for r, out in ex.map(un_epinglage, REGLES):
            ver(f"D. l'épinglage TLC {r} : les DEUX sens",
                "No error has been found" in out and "Deadlock" not in out
                and "Error" not in out)
    out = run("D_epinglage_controle",
              TLC + ["-nowarning", "-config", "MTLP_ctl.cfg",
                     "CF3EquivControlesEtendu.tla"])
    ver("D. le contrôle d'épinglage : l'INVARIANT du pin TOMBE "
        "(l'extension annulée ATTRAPÉE)",
        "is violated" in out)
    out = run("D_tlc_o3_compte",
              TLC + ["-deadlock", "-nowarning", "-config", "MCO.cfg",
                     "CF3O3.tla"])
    m = re.search(r"(\d+) distinct states found", out)
    ver("D. l'énumération TLC des formes : 288 (les formes INCHANGÉES)",
        m is not None and m.group(1) == "288",
        f"{m.group(1) if m else '?'} états distincts")


LOTS = {
    "A": lambda: lot_A(),
    "B": lambda: (construire_B(), jouer_lot_apa()),
    "C": lambda: (construire_C(), jouer_lot_apa()),
    "D": lambda: lot_D(),
}


def main() -> int:
    lot = sys.argv[1] if len(sys.argv) > 1 else "TOUS"
    if lot == "TOUS":
        for l in ("A", "B", "C", "D"):
            LOTS[l]()
    else:
        LOTS[lot]()

    verts = sum(1 for v in VERDICTS.values() if v)
    entete = (f"LA BATTERIE 5ey7gmjra — lot {lot} : "
              f"{verts}/{len(VERDICTS)} VERT")
    chemin = ATELIER / "RAPPORT-BATTERIE-5EY7GMJRA.txt"
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
    vj = {}
    f_vj = ATELIER / "verdicts-5ey7gmjra.json"
    if f_vj.is_file():
        vj = json.loads(f_vj.read_text(encoding="utf-8"))
    vj.update(VERDICTS)
    f_vj.write_text(json.dumps(vj, indent=1, sort_keys=True),
                    encoding="utf-8")
    print(f"\n[verdict {lot}] {verts}/{len(VERDICTS)} VERT")
    return 0 if verts == len(VERDICTS) else 1


if __name__ == "__main__":
    sys.exit(main())
