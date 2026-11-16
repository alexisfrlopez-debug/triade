#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outil_m4_v180.py — L'INSTRUMENT ET LE RUNNER M4 DE LA VAGUE 5
(l'instruction mof9q10vq : « Instrumenter le temps par étape (round-trip,
oracles, 3 seeds, cristallisation 10 rebuilds, guard) sur l'unité de
référence ... mesurer avant/après sur la même unité, même machine,
chronomètre monotone, et consigner les résultats (R11) »).

LA LISTE FIXE (celle du plan D204, vécue au journal_verifications.jsonl) :
  bras T : (1) le garde des arbres signés ; (2) la cristallisation — DOUZE
  rebuilds du build (l'édification + les dix + le témoin) comparés
  octet à octet ; (3) le round-trip ×2 ; (4) l'oracle du bloc loupe-01 ;
  (5) la recomposition loupe-02 ; (6) l'oracle du bloc loupe-02 ; (7)
  l'épreuve de scénario POSIX ; (8) l'assemblage des kits.

DEUX MODES :
  --mode avant    : la liste fixe SÉQUENTIELLE, les outils originaux —
                    la mesure AVANT (la même unité, cette machine) ;
  --mode apres    : la liste fixe OPTIMISÉE — la cristallisation en
                    rebuilds CONCURRENTS (copies hermétiques du dossier
                    d'unité, l'outil original INTACT), les oracles aux
                    différentiels PARALLÈLES (les MÊMES vecteurs, les
                    MÊMES graines, chaque travailleur son émulation
                    Unicorn vivante — le pool persistant par travailleur).

Le chronomètre : time.monotonic, par étape ET total. Les empreintes
SHA-256 des pièces scellées vérifiées AVANT/APRÈS (aucun octet déplacé).
Les verdicts (consoles) capturés pour l'identité bit-à-bit entre modes
et entre exécutions.

Sortie : livraison-vague5/p8-m4-{mode}.json + console ; code 0 si tout VERT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import time

REPO = pathlib.Path("/tmp/triade-gh")
SORTIE = pathlib.Path("/home/z/my-project/livraison-vague5")
U01 = REPO / "scripts" / "campagne_d204" / "unite-01-T"
U02 = REPO / "scripts" / "campagne_d204" / "unite-02-T"
V180 = pathlib.Path("/home/z/my-project/scripts/vague5/m4")

SCELLES = [REPO / "loupe" / "loupe.exe", REPO / "tls13" / "proxy.exe",
           REPO / "m1" / "selftest.exe",
           U01 / "piece" / "loupe.exe", U02 / "piece" / "loupe.exe"]


def sha(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def empreintes() -> dict:
    return {str(c.relative_to(REPO)): sha(c) for c in SCELLES if c.exists()}


def etape(nom: str, cmd: list[str], mesures: list, cwd=REPO) -> int:
    t0 = time.monotonic()
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=1200)
    dt = time.monotonic() - t0
    mesures.append({"etape": nom, "secondes": round(dt, 3),
                    "code": r.returncode,
                    "console": (r.stdout + r.stderr)[-4000:]})
    print(f"  [{nom:<34}] {dt:7.3f} s  code {r.returncode}")
    return r.returncode


def cristallisation(mode: str, mesures: list, n_rebuilds: int = 12) -> int:
    """DOUZE rebuilds : séquentiels (avant) ou concurrents (après) —
    chaque rebuild concurrent dans SA COPIE hermétique du dossier d'unité
    (l'outil original INTACT, aucun conflit d'écriture), toutes les
    sorties comparées octet à octet (l'identité de TOUTES implique
    l'identité de chaque paire consécutive — la preuve du déterminisme
    est SANS ordre)."""
    if mode == "avant":
        codes = []
        shas = []
        for i in range(n_rebuilds):
            c = etape(f"build-rebuild-{i+1}",
                      ["python3", "scripts/campagne_d204/unite-01-T/"
                       "build_unite01.py"], mesures)
            codes.append(c)
            shas.append(sha(U01 / "piece" / "loupe.exe"))
        identiques = len(set(shas)) == 1
        print(f"  [cristallisation] {n_rebuilds} rebuilds, "
              f"{'TOUTES IDENTIQUES' if identiques else 'DIVERGENTES'} "
              f"({shas[0][:16]}…)")
        return 0 if identiques and all(c == 0 for c in codes) else 2

    # ---- le mode APRÈS : les rebuilds CONCURRENTS ----
    # les copies sont SŒURS d'unite-01-T (la MÊME profondeur de chemin :
    # le build dérive REPO de __file__ — un niveau de plus casserait
    # l'import du harnais)
    racine = REPO / "scripts" / "campagne_d204"
    copies = []
    for i in range(n_rebuilds):
        cp = racine / f"_cristal_v180_r{i+1:02d}"
        if cp.exists():
            shutil.rmtree(cp)
        shutil.copytree(U01, cp,
                        ignore=shutil.ignore_patterns("kit", "kit-v2",
                                                      "piece"))
        (cp / "piece").mkdir(exist_ok=True)
        # LA VARIANTE MÉCANIQUE : le build original porte UNITE en dur
        # (REPO/scripts/campagne_d204/unite-01-T) — la variante substitue
        # LE SEUL nom du dossier d'unité par celui de la copie, le reste
        # du texte est OCTET POUR OCTET l'original
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
        out, err = p.communicate(timeout=1200)
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
                                f"{ref_intacte}")[:4000]})
    print(f"  [{'cristallisation (12 concourants)':<34}] {dt:7.3f} s  "
          f"code {mesures[-1]['code']}")
    for cp in copies:                          # le nettoyage des copies
        shutil.rmtree(cp, ignore_errors=True)
    if not identiques or any(c != 0 for c in codes.values()) \
            or not ref_intacte:
        return 2
    return 0


def empreinte_piece(unite: pathlib.Path) -> str:
    p = unite / "piece" / "loupe.exe"
    return sha(p) if p.exists() else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("avant", "apres"), required=True)
    args = ap.parse_args()
    SORTIE.mkdir(parents=True, exist_ok=True)

    avant_emp = empreintes()
    mesures: list[dict] = []
    t_total = time.monotonic()
    print(f"=== M4 {args.mode.upper()} — la liste fixe du bras T, "
          f"chronomètre monotone, cette machine ===")
    code = 0

    code |= etape("garde-sceau-I",
                  ["python3", "v06/sceau_I.py", "verifier"], mesures)
    code |= cristallisation(args.mode, mesures)
    for i in range(2):
        code |= etape(f"round-trip-notation-{i+1}",
                      ["python3", "scripts/campagne_d204/unite-01-T/"
                       "round_trip_unite01.py"], mesures)
    if args.mode == "avant":
        code |= etape("oracle-bloc-loupe-01",
                      ["python3", "scripts/campagne_d204/unite-01-T/"
                       "oracle_unite01.py"], mesures)
    else:
        code |= etape("oracle-bloc-loupe-01 (parallèle)",
                      ["python3", str(V180 / "oracle_unite01_v180.py")],
                      mesures)
    code |= etape("build-recomposition-loupe-02",
                  ["python3", "scripts/campagne_d204/unite-02-T/"
                   "build_unite02.py"], mesures)
    if args.mode == "avant":
        code |= etape("oracle-du-bloc-loupe-02",
                      ["python3", "scripts/campagne_d204/unite-02-T/"
                       "oracle_unite02.py"], mesures)
    else:
        code |= etape("oracle-du-bloc-loupe-02 (parallèle)",
                      ["python3", str(V180 / "oracle_unite02_v180.py")],
                      mesures)
    code |= etape("epreuve-scenario-posix",
                  ["python3", "scripts/campagne_d204/unite-02-T/"
                   "epreuve_scenario_unite02.py"], mesures)
    # L'ASSEMBLAGE — le comportement VÉCU de la campagne : la recomposition
    # du build change l'horodatage PE de la pièce, l'assemblage refuse
    # UNE FOIS (code 2), la pièce canonique est restaurée de la gravure,
    # la reprise passe (le journal de campagne porte les DEUX lignes)
    c_asm = etape("assemblage-kits",
                  ["python3", "scripts/campagne_d204/"
                   "assembler_kits_unite02.py"], mesures)
    if c_asm != 0:
        gravure = U02 / "kit"
        for canon in gravure.glob("loupe*"):
            shutil.copy2(canon, U02 / "piece" / canon.name)
        c_asm = etape("assemblage-kits (reprise : la pièce canonique "
                      "restaurée de la gravure)",
                      ["python3", "scripts/campagne_d204/"
                       "assembler_kits_unite02.py"], mesures)
    code |= c_asm

    total = time.monotonic() - t_total
    apres_emp = empreintes()
    scelles_intacts = avant_emp == apres_emp

    rapport = {
        "mode": args.mode,
        "total_s": round(total, 3),
        "etapes": mesures,
        "scelles_intacts": scelles_intacts,
        "empreintes": apres_emp,
        "code": code,
    }
    (SORTIE / f"p8-m4-{args.mode}.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"=== TOTAL {args.mode.upper()} : {total:.1f} s ; "
          f"code {code} ; scellés "
          f"{'INTACTS' if scelles_intacts else 'MODIFIÉS'}")
    return 0 if code == 0 and scelles_intacts else 2


if __name__ == "__main__":
    sys.exit(main())
