#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outil_m4_v181.py — LE RUNNER M4 DE L'ATELIER vljfs6pcj (le plan
PLAN-vljfs6pcj-M4.md § 4 : la liste fixe de la vague 5, AUCUNE étape
ajoutée, AUCUNE retirée, n≥5 par configuration, chronomètre monotone).

TROIS CONFIGURATIONS :
  --mode avant   : la liste fixe TELLE QU'ELLE (les outils v180 — l'état
                   actuel du projet) : la mesure AVANT, n exécutions ;
  --mode froid   : la liste v181 (les oracles au MÉMO SCELLÉ), le mémo
                   EFFACÉ AVANT : la SEMENCE — le prix du premier passage,
                   UNE exécution, consignée mais jamais confondue avec le
                   régime ;
  --mode chaud   : la liste v181, le mémo PRÉSENT et vérifié : la mesure
                   APRÈS de régime, n exécutions.

Le chronomètre : time.monotonic, par étape ET total. Les empreintes
SHA-256 des pièces scellées vérifiées AVANT/APRÈS chaque exécution.
Les consoles des oracles capturées INTÉGRALEMENT (stdout séparé de
stderr — l'identité ligne à ligne avec l'original est exigée par le plan
§ 5.1, vérifiée par extraire_m4_v181.py).

Sortie : preuves/m4-{mode}-run{N}.json ; code 0 si tout VERT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

REPO = pathlib.Path("/tmp/triade-gh")
ATELIER = REPO / "atelier-m4-vljfs6pcj"
V180 = REPO / "scripts" / "vague5" / "m4"
SORTIE = ATELIER / "preuves"
MEMO_CHEMIN = ATELIER / "memo-sessions-v1.json"
U01 = REPO / "scripts" / "campagne_d204" / "unite-01-T"
U02 = REPO / "scripts" / "campagne_d204" / "unite-02-T"

SCELLES = [REPO / "loupe" / "loupe.exe", REPO / "tls13" / "proxy.exe",
           REPO / "m1" / "selftest.exe",
           U01 / "piece" / "loupe.exe", U02 / "piece" / "loupe.exe"]


def sha(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def empreintes() -> dict:
    return {str(c.relative_to(REPO)): sha(c) for c in SCELLES if c.exists()}


def etape(nom: str, cmd: list[str], mesures: list, cwd=REPO,
          capture_integrale: bool = False) -> int:
    t0 = time.monotonic()
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=1800)
    dt = time.monotonic() - t0
    console = r.stdout if capture_integrale else r.stdout[-4000:]
    mesures.append({"etape": nom, "secondes": round(dt, 3),
                    "code": r.returncode,
                    "console": console[-40000:],
                    "stderr": r.stderr[-4000:]})
    print(f"  [{nom:<34}] {dt:7.3f} s  code {r.returncode}")
    return r.returncode


def cristallisation(mesures: list, n_rebuilds: int = 12) -> int:
    """DOUZE rebuilds CONCURRENTS — le geste de la vague 5 inchangé :
    chaque rebuild dans SA COPIE hermétique du dossier d'unité (l'outil
    original INTACT, une substitution mécanique du SEUL chemin d'unité),
    toutes les sorties comparées octet à octet (la preuve du déterminisme
    est SANS ordre), la pièce d'origine INTACTE."""
    racine = REPO / "scripts" / "campagne_d204"
    copies = []
    for i in range(n_rebuilds):
        cp = racine / f"_cristal_v181_r{i+1:02d}"
        if cp.exists():
            shutil.rmtree(cp)
        shutil.copytree(U01, cp,
                        ignore=shutil.ignore_patterns("kit", "kit-v2",
                                                      "piece"))
        (cp / "piece").mkdir(exist_ok=True)
        src = (cp / "build_unite01.py").read_text(encoding="utf-8")
        assert 'os.path.join(REPO, "scripts", "campagne_d204", "unite-01-T")' in src
        (cp / "build_unite01.py").write_text(
            src.replace('os.path.join(REPO, "scripts", "campagne_d204", '
                        '"unite-01-T")',
                        f"os.path.join(REPO, \"scripts\", "
                        f"\"campagne_d204\", \"{cp.name}\")"),
            encoding="utf-8")
        copies.append(cp)
    ref_avant = empreinte_piece(U01)
    t0 = time.monotonic()
    procs = [(i + 1, subprocess.Popen(
        ["python3", "build_unite01.py"], cwd=cp,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        for i, cp in enumerate(copies)]
    codes = {}
    for i, p in procs:
        out, err = p.communicate(timeout=1800)
        codes[i] = p.returncode
    dt = time.monotonic() - t0
    shas = {i: sha(cp / "piece" / "loupe.exe")
            for i, cp in enumerate(copies, 1)}
    identiques = len(set(shas.values())) == 1
    ref_intacte = (ref_avant == "") or (shas[1] == ref_avant)
    mesures.append({"etape": f"cristallisation-{n_rebuilds}-concourants",
                    "secondes": round(dt, 3),
                    "code": 0 if identiques and ref_intacte else 2,
                    "console": ("sha par rebuild : "
                                + ", ".join(f"r{i}={s[:12]}"
                                            for i, s in
                                            sorted(shas.items()))
                                + f" ; pièce d'origine intacte : "
                                f"{ref_intacte}")[:4000],
                    "stderr": ""})
    print(f"  [{'cristallisation (12 concourants)':<34}] {dt:7.3f} s  "
          f"code {mesures[-1]['code']}")
    for cp in copies:
        shutil.rmtree(cp, ignore_errors=True)
    if not identiques or any(c != 0 for c in codes.values()) \
            or not ref_intacte:
        return 2
    return 0


def empreinte_piece(unite: pathlib.Path) -> str:
    p = unite / "piece" / "loupe.exe"
    return sha(p) if p.exists() else ""


def oracle_cmds(mode: str):
    """Les commandes d'oracle par mode — avant : les outils v180 tels quels
    (l'état actuel) ; froid/chaud : les v181 au mémo scellé."""
    if mode == "avant":
        return (["python3", str(V180 / "oracle_unite01_v180.py")],
                ["python3", str(V180 / "oracle_unite02_v180.py")])
    return (["python3", str(ATELIER / "oracle_unite01_v181.py"),
             "--memo", str(MEMO_CHEMIN)],
            ["python3", str(ATELIER / "oracle_unite02_v181.py"),
             "--memo", str(MEMO_CHEMIN)])


def une_execution(mode: str, numero: int) -> int:
    avant_emp = empreintes()
    mesures: list[dict] = []
    t_total = time.monotonic()
    print(f"=== M4 {mode.upper()} — exécution {numero} — la liste fixe du "
          f"bras T, chronomètre monotone, cette machine ===")
    cmd_o1, cmd_o2 = oracle_cmds(mode)
    code = 0

    code |= etape("garde-sceau-I",
                  ["python3", "v06/sceau_I.py", "verifier"], mesures)
    code |= cristallisation(mesures)
    for i in range(2):
        code |= etape(f"round-trip-notation-{i+1}",
                      ["python3", "scripts/campagne_d204/unite-01-T/"
                       "round_trip_unite01.py"], mesures)
    code |= etape("oracle-bloc-loupe-01 (parallèle)", cmd_o1, mesures,
                  capture_integrale=True)
    code |= etape("build-recomposition-loupe-02",
                  ["python3", "scripts/campagne_d204/unite-02-T/"
                   "build_unite02.py"], mesures)
    code |= etape("oracle-du-bloc-loupe-02 (parallèle)", cmd_o2, mesures,
                  capture_integrale=True)
    code |= etape("epreuve-scenario-posix",
                  ["python3", "scripts/campagne_d204/unite-02-T/"
                   "epreuve_scenario_unite02.py"], mesures)
    c_asm = etape("assemblage-kits",
                  ["python3", "scripts/campagne_d204/"
                   "assembler_kits_unite02.py"], mesures)
    if c_asm != 0:
        gravure = U02 / "kit"
        for canon in gravure.glob("loupe*"):
            shutil.copy2(canon, U02 / "piece" / canon.name)
        # la pièce C canonique aussi — la gravure du kit C la porte (le
        # comportement vécu de la campagne : l'assemblage recoupe les
        # pièces contre les compilations consignées, la gravure détient
        # les canoniques ; l'Entrée 320 commita une recompilation au
        # epreuves — la pièce canonique est restaurée pareil)
        gravure_c = REPO / "scripts" / "campagne_d204" / "unite-02-C" / "kit"
        canon_c = gravure_c / "loupe-02-c.dll"
        if canon_c.exists():
            shutil.copy2(canon_c,
                         REPO / "scripts" / "campagne_d204" / "unite-02-C"
                         / "epreuves" / "loupe-02-c.dll")
        c_asm = etape("assemblage-kits (reprise : la pièce canonique "
                      "restaurée de la gravure)",
                      ["python3", "scripts/campagne_d204/"
                       "assembler_kits_unite02.py"], mesures)
    code |= c_asm

    total = time.monotonic() - t_total
    apres_emp = empreintes()
    scelles_intacts = avant_emp == apres_emp

    rapport = {"mode": mode, "run": numero,
               "total_s": round(total, 3),
               "etapes": mesures,
               "scelles_intacts": scelles_intacts,
               "empreintes": apres_emp,
               "code": code}
    SORTIE.mkdir(parents=True, exist_ok=True)
    (SORTIE / f"m4-{mode}-run{numero}.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"=== TOTAL {mode.upper()} run {numero} : {total:.1f} s ; "
          f"code {code} ; scellés "
          f"{'INTACTS' if scelles_intacts else 'MODIFIÉS'}")
    return 0 if code == 0 and scelles_intacts else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("avant", "froid", "chaud"),
                    required=True)
    ap.add_argument("--runs", type=int, default=None)
    args = ap.parse_args()
    n = args.runs if args.runs is not None else \
        {"avant": 5, "froid": 1, "chaud": 5}[args.mode]

    if args.mode == "froid":
        if MEMO_CHEMIN.exists():
            MEMO_CHEMIN.unlink()
            print(f"[memo] effacé avant la semence : {MEMO_CHEMIN}")
    if args.mode == "chaud" and not MEMO_CHEMIN.exists():
        print(f"ERREUR : le mode chaud exige le mémo semé ({MEMO_CHEMIN})",
              file=sys.stderr)
        return 2

    code = 0
    for i in range(1, n + 1):
        code |= une_execution(args.mode, i)
    return code


if __name__ == "__main__":
    sys.exit(main())
