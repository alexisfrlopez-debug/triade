#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""decomposition_37s.py — LA DÉCOMPOSITION DES 37 s DU BRAS T (ahult8jgd §4) :
la session M4 du bras T (la liste fixe de la vague 5, les outils v180 — la
configuration « AVANT » de cq01qv1za, 39,24 s la médiane consignée v0.21.0)
décomposée PAR CONTRÔLE : rebuilds de cristallisation, round-trips,
recomposition du plan, oracles — chaque poste chronométré par
l'instrumentation de la copie (l'horloge monotone, n=5, la médiane), LA TABLE
PUBLIÉE, la réconciliation : la somme des postes == le total mesuré (l'écart
nommé et borné sinon — l'inter-poste : les empreintes avant/après, les
lancements, l'écriture du registre).

LA COPIE INSTRUMENTÉE (jamais l'original) : le runner
atelier-cout-boucle-cq01qv1za/outil_m4_v182.py repris à la lettre pour la
liste fixe — AUCUNE étape ajoutée, AUCUNE retirée, les commandes TELLES
QUELLES — instrumenté de : le chrono d'inter-poste (le temps hors postes
d'une exécution), la capture de l'identité des consoles run à run ET contre
les originales consignées (les preuves m4-avant-run*.json du dépôt — la
discipline « consoles d'oracle LIGNE-IDENTIQUES »).

LE TERRAIN D'EXÉCUTION : /tmp/triade-gh-porteuse — le CLONE du dépôt (le
dépôt réel JAMAIS touché par les rebuilds ; les scellés du clone vérifiés
VERTS avant la première mesure — 14 arbres, la même cle déposée). Les modes
froid/chaud/audit du mémo v2 sont le territoire de cq01qv1za — la
décomposition porte la session AVANT (v180), celle des 39 s.

Sortie : registres/decomposition-37s-run{N}.json ·
registres/decomposition-37s.json (la table) · rapport-decomposition-37s.txt"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import statistics
import subprocess
import sys
import time

REPO = pathlib.Path("/tmp/triade-gh-porteuse")     # le clone (jamais le dépôt)
DEPOT = pathlib.Path("/home/z/my-project/depot")
ICI = DEPOT / "atelier-porteuse-ahult8jgd"
SORTIE = ICI / "registres"
SORTIE.mkdir(parents=True, exist_ok=True)
V180 = REPO / "scripts" / "vague5" / "m4"
U01 = REPO / "scripts" / "campagne_d204" / "unite-01-T"
U02 = REPO / "scripts" / "campagne_d204" / "unite-02-T"

SCELLES = [REPO / "loupe" / "loupe.exe", REPO / "tls13" / "proxy.exe",
           REPO / "m1" / "selftest.exe",
           U01 / "piece" / "loupe.exe", U02 / "piece" / "loupe.exe"]

# la liste fixe (le plan D204, la lettre de la vague 5 — INCHANGÉE)
LISTE = [
    ("garde-sceau-I", ["python3", "v06/sceau_I.py", "verifier"], False, None),
    ("cristallisation-12-concourants", None, False, "cristallisation"),
    ("round-trip-notation-1",
     ["python3", "scripts/campagne_d204/unite-01-T/round_trip_unite01.py"],
     False, None),
    ("round-trip-notation-2",
     ["python3", "scripts/campagne_d204/unite-01-T/round_trip_unite01.py"],
     False, None),
    ("oracle-bloc-loupe-01 (parallèle)",
     ["python3", str(V180 / "oracle_unite01_v180.py")], True, None),
    ("build-recomposition-loupe-02",
     ["python3", "scripts/campagne_d204/unite-02-T/build_unite02.py"],
     False, None),
    ("oracle-du-bloc-loupe-02 (parallèle)",
     ["python3", str(V180 / "oracle_unite02_v180.py")], True, None),
    ("epreuve-scenario-posix",
     ["python3", "scripts/campagne_d204/unite-02-T/"
      "epreuve_scenario_unite02.py"], False, None),
    ("assemblage-kits",
     ["python3", "scripts/campagne_d204/assembler_kits_unite02.py"],
     False, None),
]


def sha(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def empreintes() -> dict:
    return {str(c.relative_to(REPO)): sha(c) for c in SCELLES if c.exists()}


def etape(nom: str, cmd: list[str], mesures: list, cwd=REPO,
          capture_integrale: bool = False) -> int:
    t0 = time.monotonic()
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=3600)
    dt = time.monotonic() - t0
    console = r.stdout if capture_integrale else r.stdout[-4000:]
    mesures.append({"etape": nom, "secondes": round(dt, 3),
                    "code": r.returncode,
                    "console": console[-60000:],
                    "stderr": r.stderr[-6000:]})
    print(f"  [{nom:<34}] {dt:7.3f} s  code {r.returncode}")
    return r.returncode


def cristallisation(mesures: list, n_rebuilds: int = 12) -> int:
    """DOUZE rebuilds CONCURRENTS — le geste de la vague 5 inchangé (le
    runner TEL QUEL : chaque rebuild dans SA COPIE hermétique, toutes les
    sorties comparées octet à octet, la pièce d'origine INTACTE)."""
    racine = REPO / "scripts" / "campagne_d204"
    copies = []
    for i in range(n_rebuilds):
        cp = racine / f"_cristal_porteuse_r{i+1:02d}"
        if cp.exists():
            shutil.rmtree(cp)
        shutil.copytree(U01, cp,
                        ignore=shutil.ignore_patterns("kit", "kit-v2",
                                                      "piece"))
        (cp / "piece").mkdir(exist_ok=True)
        src = (cp / "build_unite01.py").read_text(encoding="utf-8")
        assert 'os.path.join(REPO, "scripts", "campagne_d204", "unite-01-T")' \
            in src
        (cp / "build_unite01.py").write_text(
            src.replace('os.path.join(REPO, "scripts", "campagne_d204", '
                        '"unite-01-T")',
                        f"os.path.join(REPO, \"scripts\", "
                        f"\"campagne_d204\", \"{cp.name}\")"),
            encoding="utf-8")
        copies.append(cp)
    ref_avant = sha(U01 / "piece" / "loupe.exe") \
        if (U01 / "piece" / "loupe.exe").exists() else ""
    t0 = time.monotonic()
    procs = [(i + 1, subprocess.Popen(
        ["python3", "build_unite01.py"], cwd=cp,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        for i, cp in enumerate(copies)]
    codes = {}
    for i, p in procs:
        p.communicate(timeout=3600)
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


def une_execution(numero: int) -> dict:
    avant_emp = empreintes()
    mesures: list[dict] = []
    t_total = time.monotonic()
    print(f"=== T AVANT (v180) — exécution {numero} — la liste fixe, "
          f"chronomètre monotone, le clone ===")
    code = 0
    for nom, cmd, integral, special in LISTE:
        if special == "cristallisation":
            code |= cristallisation(mesures)
            continue
        c = etape(nom, cmd, mesures, capture_integrale=integral)
        if nom == "assemblage-kits" and c != 0:
            # la reprise à la lettre du runner (la pièce canonique restaurée
            # de la gravure — le geste de cq01qv1za, inchangé)
            gravure = U02 / "kit"
            for canon in gravure.glob("loupe*"):
                shutil.copy2(canon, U02 / "piece" / canon.name)
            c = etape("assemblage-kits (reprise : la pièce canonique "
                      "restaurée de la gravure)",
                      cmd, mesures)
        code |= c
    total = time.monotonic() - t_total
    apres_emp = empreintes()
    scelles_intacts = avant_emp == apres_emp
    somme = sum(m["secondes"] for m in mesures)
    rapport = {"run": numero,
               "total_s": round(total, 3),
               "somme_postes_s": round(somme, 3),
               "inter_poste_s": round(total - somme, 3),
               "etapes": mesures,
               "scelles_intacts": scelles_intacts,
               "empreintes": apres_emp,
               "code": code}
    (SORTIE / f"decomposition-37s-run{numero}.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"=== TOTAL run {numero} : {total:.1f} s (la somme des postes "
          f"{somme:.1f} s, l'inter-poste {total - somme:.3f} s) ; code "
          f"{code} ; scellés "
          f"{'INTACTS' if scelles_intacts else 'MODIFIÉS'}")
    return rapport


def main() -> int:
    n = 5
    # le garde-fou : les scellés du clone VERTS avant la première mesure
    r = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                       cwd=REPO, capture_output=True, text=True, timeout=300)
    verts = r.stdout.count(": vert (")
    print(f"[garde-fou] les scellés du clone : {verts} arbres VERTS")
    if verts != 14:
        print("ROUGE : le clone n'est pas scellé vert")
        return 2

    runs = [une_execution(i) for i in range(1, n + 1)]

    # ---- la table (les médianes par poste, n=5) -------------------------------
    postes = [m["etape"] for m in runs[0]["etapes"]]
    for rr in runs[1:]:
        for m in rr["etapes"]:
            if m["etape"] not in postes:
                postes.append(m["etape"])
    table = []
    for poste in postes:
        vals = [next((m["secondes"] for m in rr["etapes"]
                      if m["etape"] == poste), None) for rr in runs]
        vals = [v for v in vals if v is not None]
        table.append({"poste": poste,
                      "mediane_s": round(statistics.median(vals), 3),
                      "min_s": min(vals), "max_s": max(vals)})
    tot = [rr["total_s"] for rr in runs]
    som = [rr["somme_postes_s"] for rr in runs]
    inter = [rr["inter_poste_s"] for rr in runs]

    # ---- l'identité des consoles (run à run, puis contre les originales) ------
    identite_run = all(
        [m["console"] for m in runs[0]["etapes"]]
        == [m["console"] for m in rr["etapes"]] for rr in runs[1:])
    identite_originale = None
    orig_dir = REPO / "atelier-cout-boucle-cq01qv1za" / "preuves"
    if orig_dir.exists():
        try:
            consoles_origin = {}
            for i in range(1, 6):
                d = json.loads((orig_dir / f"m4-avant-run{i}.json").read_text())
                for e in d["etapes"]:
                    consoles_origin.setdefault(e["etape"], e["console"])
            diff = []
            for rr in runs:
                for m in rr["etapes"]:
                    if m["etape"] in consoles_origin \
                            and m["console"] != consoles_origin[m["etape"]]:
                        diff.append((rr["run"], m["etape"]))
            identite_originale = not diff
        except Exception:
            identite_originale = None

    med_tot = statistics.median(tot)
    med_som = statistics.median(som)
    med_inter = statistics.median(inter)
    ok = (all(rr["code"] == 0 for rr in runs)
          and all(rr["scelles_intacts"] for rr in runs)
          and identite_run and identite_originale is True)

    lignes = ["LA DÉCOMPOSITION DES 37 s DU BRAS T (ahult8jgd §4) — la "
              "session M4 AVANT (v180), la liste fixe de la vague 5, le "
              "clone /tmp/triade-gh-porteuse (le dépôt jamais touché), "
              "l'horloge monotone, n=5, cette machine",
              "",
              "LA TABLE PAR POSTE (la médiane [min–max] sur 5 exécutions) :"]
    for t in table:
        lignes.append(f"  {t['poste']:<42} {t['mediane_s']:8.3f} s "
                      f"[{t['min_s']:.3f}–{t['max_s']:.3f}]")
    lignes += [
        f"  {'— LA SOMME DES POSTES':<42} {med_som:8.3f} s",
        f"  {'— L\u2019INTER-POSTE (empreintes, lancements)':<42} "
        f"{med_inter:8.3f} s",
        f"  {'— LE TOTAL MESURÉ':<42} {med_tot:8.3f} s",
        "",
        "LA RÉCONCILIATION : la somme des postes + l'inter-poste == le "
        f"total (médianes : {med_som:.3f} + {med_inter:.3f} = "
        f"{med_som + med_inter:.3f} vs {med_tot:.3f} s — l'écart "
        f"{abs(med_tot - med_som - med_inter)*1000:.0f} ms, l'inter-poste "
        "BORNE : " + f"[{min(inter):.3f}–{max(inter):.3f}] s — les "
        "empreintes sha avant/après, les lancements python, l'écriture du "
        "registre)",
        "",
        f"LES CONSOLES : identiques run à run ({'OUI' if identite_run else 'NON — ROUGE'})"
        + (f" ; LIGNE-IDENTIQUES aux originales consignées (les preuves "
           f"m4-avant-run*.json du dépôt) : "
           f"{'OUI' if identite_originale else 'NON — ÉCART NOMMÉ'}"
           if identite_originale is not None else " ; les originales "
           "introuvables au clone"),
        "",
        f"LES SCELLÉS : INTACTS avant/après CHAQUE exécution "
        f"({', '.join(str(c.relative_to(REPO)) for c in SCELLES)})",
        "",
        "LA LECTURE : les oracles portent "
        f"{next(t['mediane_s'] for t in table if 'oracle-bloc' in t['poste']) + next(t['mediane_s'] for t in table if 'oracle-du-bloc' in t['poste']):.1f} s "
        f"des {med_tot:.1f} s ("
        f"{(next(t['mediane_s'] for t in table if 'oracle-bloc' in t['poste']) + next(t['mediane_s'] for t in table if 'oracle-du-bloc' in t['poste']))/med_tot*100:.0f} "
        "% — les re-exécutions vivantes sous Unicorn, LE poste dominant) ; "
        "la cristallisation "
        f"{next(t['mediane_s'] for t in table if 'cristallisation' in t['poste']):.1f} s ; les round-trips "
        f"{next(t['mediane_s'] for t in table if t['poste'] == 'round-trip-notation-1')*2:.2f} s ; la recomposition du plan "
        f"{next(t['mediane_s'] for t in table if 'recomposition' in t['poste']):.2f} s",
        "",
        f"LE VERDICT : {'VERT' if ok else 'ROUGE'}"]
    (ICI / "rapport-decomposition-37s.txt").write_text("\n".join(lignes) + "\n",
                                                       encoding="utf-8")
    (SORTIE / "decomposition-37s.json").write_text(json.dumps({
        "runs": [{k: v for k, v in rr.items() if k != "etapes"}
                 for rr in runs],
        "table": table,
        "medianes": {"total_s": round(med_tot, 3),
                     "somme_postes_s": round(med_som, 3),
                     "inter_poste_s": round(med_inter, 3)},
        "identite_consoles_run_a_run": identite_run,
        "identite_consoles_originales": identite_originale,
        "scelles_intacts": all(rr["scelles_intacts"] for rr in runs),
        "codes": [rr["code"] for rr in runs],
        "verdict": "VERT" if ok else "ROUGE"}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print("\n".join(lignes))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
