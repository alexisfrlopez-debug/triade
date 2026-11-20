#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cgp_m4.py — LA MESURE M4 AUX QUATRE BRAS (3lmyfb2xa, la vague 11) : T,
C+G+, C+G, C sur LA MÊME MACHINE (le plan § 3), n=5 exécutions par bras,
l'horloge monotone, la liste fixe, LES QUATRE BRAS EN ORDRE ALTERNÉ (T,
C+G+, C+G, C — la rotation contre la dérive thermique : pour chaque run i,
enchaîne T(i), C+G+(i), C+G(i), C(i)).

LA LISTE T : l'outil de la vague 9 TEL QUEL (outil_m4_v182, la liste
complète : garde-sceau, cristallisation×12, round-trips, oracles, build,
épreuve, kits) — la sortie REDIRIGÉE au présent atelier (les preuves de la
vague 9 JAMAIS écrasées), le registre recopié à m4-T-run{N}.json.

LA LISTE C et LA LISTE C+G : les étapes de la vague 10 reconduites
(bras_c et bras_cg de cg_m4.py, les mêmes commandes, les mêmes noms).

LA LISTE C+G+ : LA LISTE C+G PLUS LE RÉGIME DE VÉRIFICATION COMPLET DU
BRAS T ADAPTÉ AU COMPILÉ (le plan § 2) :
  — garde-sceau-I (la garde du bras T, 14 arbres) ;
  — LES REBUILDS DE CRISTALLISATION : chaque unité recompilée DIX fois
    CONCURRENTES en copies hermétiques (le MÊME -o relatif — ld embarque
    le chemin, l'écart nommé), les octets confrontés (l'équivalent
    compilé du round-trip, DOCUMENTÉ, jamais confondu) ; les TROIS champs
    d'horodatage du PE seuls épargnés (l'heure du lien par construction) ;
  — LES VOLUMES ORACLE ÉQUIVALENTS : u01 DOUZE épreuves / QUATORZE
    contrôles (les vecteurs de l'oracle T, E3 ARMÉ), u02 2032 décalages
    (la même graine 20261114, le juge modèle indépendant) ;
  — LA RECOMPOSITION DU PLAN : le graphe de dépendances des sources
    re-vérifié à chaque livraison (cgp-plan.json, fail-closed).

Sortie : m4-{T,CGP,CG,C}-run{N}.json (les registres bruts)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import struct
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-quatrebras-3lmyfb2xa"
V9 = REPO / "atelier-cout-boucle-cq01qv1za"
CG_GOUVERNE = REPO / "atelier-cg-3a91o5whb" / "cg_gouverne.py"
MINGW = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-gcc-posix"
U01C = REPO / "scripts" / "campagne_d204" / "unite-01-C"
U02C = REPO / "scripts" / "campagne_d204" / "unite-02-C"
CORPUS = ICI / "cgp-corpus"
N = 5

# LES FAUTES DE RIG DU BRAS C CONSIGNÉES (vague 10, l'état de la campagne
# D204 — le M1 : « la epreuve_posix loupe-01 et les contrôles binaires —
# l'état consigné de la campagne, jamais réparées en silence ») : le gcc
# de l'épreuve u01 ne trouve pas loupe-01-c.c depuis epreuves/, le chemin
# des contrôles binaires u01 est nu — RECONDUITES À L'IDENTIQUE (les
# mêmes commandes, les mêmes codes), portées au registre, jamais maquillées
FAUTES_CONSIGNEES = ("suite-tests-c-contrat", "controles-binaires-loupe-01")

# L'ORDRE STRATIFIÉ PAR FAMILLE (le plan § 2 — les sources du bras C+G)
UNITES = [
    ("loupe-01", REPO / "scripts/campagne_d204/unite-01-C/source/"
                 "loupe-01-c.c"),
    ("loupe-02", REPO / "scripts/campagne_d204/unite-02-C/source/"
                 "loupe-02-c.c"),
    ("loupe-05", REPO / "atelier-cg-3a91o5whb/loupe-05-c.c"),
    ("loupe-08", REPO / "scripts/campagne_d204/unite-08-C/source/"
                 "loupe-08-c.c"),
    ("loupe-13", REPO / "scripts/campagne_d204/unite-13-C/source/"
                 "loupe-13-c.c"),
    ("loupe-16", REPO / "scripts/campagne_d204/attribution-unite16-C-353/"
                 "source-loupe-16-C.c"),
]


def une_etape(nom, cmd, mesures, cwd=REPO):
    t0 = time.monotonic()
    shell = isinstance(cmd, str) or (cmd and cmd[0] == "cd")
    args = " ".join(cmd) if isinstance(cmd, list) and cmd and cmd[0] == "cd" \
        else cmd
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       timeout=600, shell=shell)
    dt = time.monotonic() - t0
    mesures.append({"etape": nom, "secondes": round(dt, 3),
                    "code": r.returncode,
                    "console": (r.stdout + r.stderr)[-3000:]})
    print(f"  [{nom:<44}] {dt:7.3f} s  code {r.returncode}")
    return r.returncode


# --- LES REBUILDS DE CRISTALLISATION (l'équivalent compilé du round-trip) --

def masques_pe(data: bytes) -> list[tuple[int, int]]:
    """LES TROIS CHAMPS D'HORODATAGE DU PE — l'en-tête TimeDateStamp, la
    somme de contrôle, le TimeDateStamp du répertoire d'exports : l'heure
    du lien PAR CONSTRUCTION du format (ld l'écrit à chaque lien), JAMAIS
    une divergence de compilation — NOMMÉS et BORNÉS, seuls épargnés de
    la confrontation d'octets."""
    e = struct.unpack_from("<I", data, 0x3C)[0]
    zones = [(e + 8, e + 12), (e + 24 + 64, e + 24 + 68)]
    exp_rva = struct.unpack_from("<I", data, e + 24 + 112)[0]
    nb = struct.unpack_from("<H", data, e + 6)[0]
    opt = struct.unpack_from("<H", data, e + 20)[0]
    for k in range(nb):
        o = e + 24 + opt + k * 40
        vs, va, rs, ra = struct.unpack_from("<IIII", data, o + 8)
        if va <= exp_rva < va + vs and ra:
            zones.append((ra + (exp_rva - va) + 4,
                          ra + (exp_rva - va) + 8))
    return zones


def canonique(data: bytes) -> bytes:
    b = bytearray(data)
    for a, bb in masques_pe(data):
        for i in range(a, min(bb, len(b))):
            b[i] = 0
    return bytes(b)


def confrontre(echantillons: list[bytes]) -> bool:
    """La confrontation d'octets : TOUTES les longueurs égales, TOUS les
    octets égaux hors les TROIS champs d'horodatage nommés."""
    if not echantillons or any(len(e) != len(echantillons[0])
                               for e in echantillons):
        return False
    ref = canonique(echantillons[0])
    return all(canonique(e) == ref for e in echantillons[1:])


def rebuilds_cristallisation(unite: str, src: pathlib.Path, mesures,
                             n_rebuilds: int = 10) -> int:
    """DIX rebuilds CONCURRENTS en copies hermétiques (le MÊME -o relatif
    « <unite>-cg.dll » — le nom de la chaîne vague 10 ; ld embarque le
    chemin de sortie : le même -o rend les builds confrontables, l'écart
    nommé), les octets confrontés. loupe-05 : le build ECHEC (l'unité
    close sur son rouge à la cap) — les DIX échecs confrontés à l'octet
    de stderr (l'ECHEC cristallisé, l'état même de la chaîne)."""
    racine = ICI / "cgp-rebuild" / unite
    shutil.rmtree(racine, ignore_errors=True)
    racine.mkdir(parents=True)
    copies = [racine / f"r{i+1:02d}" for i in range(n_rebuilds)]
    for cp in copies:
        cp.mkdir()
    t0 = time.monotonic()
    procs = [(cp, subprocess.Popen(
        [MINGW, "-O2", "-shared", "-o", f"{unite}-cg.dll", str(src)],
        cwd=cp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        for cp in copies]
    resultats = []
    for cp, p in procs:
        out, err = p.communicate(timeout=600)
        resultats.append((cp, p.returncode, out, err))
    dt_r = time.monotonic() - t0

    if all(rc == 0 for _, rc, _, _ in resultats):
        octets = [(cp / f"{unite}-cg.dll").read_bytes()
                  for cp, _, _, _ in resultats]
        identiques = confrontre(octets)
        canons = [hashlib.sha256(canonique(o)).hexdigest()[:12]
                  for o in octets]
        console = ("sha canonique par rebuild (les 3 champs d'horodatage "
                   "du PE masqués) : "
                   + ", ".join(f"r{i+1}={c}"
                               for i, c in enumerate(canons))
                   + f" ; {n_rebuilds}/{n_rebuilds} identiques : "
                   f"{identiques}")
        code = 0 if identiques else 2
    else:
        echecs = {(rc, err) for _, rc, _, err in resultats}
        cristallise = (len(echecs) == 1
                       and all(rc != 0 for rc, _ in echecs))
        premier = next(iter(echecs)) if echecs else (None, "")
        verdict = ("IDENTIQUE — l'ECHEC cristallisé (l'état clos de la "
                   "chaîne, sha256_dll = ECHEC)" if cristallise
                   else "DIVERGENT")
        console = (f"le build mingw ECHEC aux {n_rebuilds} rebuilds : "
                   f"{len(echecs)} échec(s) distinct(s), stderr {verdict} : "
                   + premier[1][-400:])
        code = 0 if cristallise else 2
    mesures.append({"etape": f"rebuilds-cristallisation-{unite} "
                             f"(×{n_rebuilds} concourants)",
                    "secondes": round(dt_r, 3), "code": code,
                    "console": console[:4000]})
    print(f"  [{'rebuilds-' + unite + f' ×{n_rebuilds}':<44}] {dt_r:7.3f} s"
          f" code {code}")
    shutil.rmtree(racine, ignore_errors=True)
    return code


# --- LA LISTE T : l'outil de la vague 9, la sortie redirigée ----------------

def bras_t(numero: int) -> int:
    sys.path.insert(0, str(V9))
    import outil_m4_v182 as m4t
    m4t.SORTIE = ICI          # les preuves de la vague 9 jamais écrasées
    code = m4t.une_execution("avant", numero)
    src = ICI / f"m4-avant-run{numero}.json"
    dst = ICI / f"m4-T-run{numero}.json"
    if src.exists():
        dst.write_bytes(src.read_bytes())   # le registre brut, VERBATIM
        src.unlink()                        # un seul nom par bras
    return code


# --- LA LISTE C : les étapes de la vague 10 reconduites ---------------------

def bras_c(numero: int) -> int:
    mesures = []
    t_total = time.monotonic()
    code = 0
    code |= une_etape(
        "build-gcc-O2-loupe-01",
        f"cd {U01C} && {MINGW} -O2 -shared -o epreuves/loupe-01-c.dll "
        f"source/loupe-01-c.c source/loupe-01-c.def".split(), mesures)
    code |= une_etape("suite-tests-c-hash",
                      ["python3", "epreuve_hash_posix.py"], mesures,
                      cwd=U01C)
    code |= une_etape(
        "suite-tests-c-contrat",
        f"cd {U01C}/epreuves && gcc -O2 -o epreuve_posix epreuve_posix.c "
        f"-I. && ./epreuve_posix > observe.txt && python3 "
        f"compare_epreuve.py".split(), mesures)
    code |= une_etape("controles-binaires-loupe-01",
                      ["python3", "controles_binaires.py"], mesures,
                      cwd=U01C)
    code |= une_etape(
        "build-gcc-O2-loupe-02",
        f"cd {REPO} && {MINGW} -O2 -shared -o scripts/campagne_d204/"
        f"unite-02-C/epreuves/loupe-02-c.dll scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.c scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.def".split(), mesures)
    code |= une_etape("epreuve-contrat-posix-loupe-02",
                      f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
                      f"epreuve_posix.c && ./epreuve_posix > "
                      f"sortie-epreuve.txt && python3 compare_epreuve.py".split(),
                      mesures)
    code |= une_etape("controles-binaires-loupe-02",
                      ["python3", "scripts/campagne_d204/unite-02-C/"
                       "epreuves/controles_binaires.py"], mesures)
    total = time.monotonic() - t_total
    (ICI / f"m4-C-run{numero}.json").write_text(
        json.dumps({"bras": "C", "run": numero, "total_s": round(total, 3),
                    "etapes": mesures, "code": code,
                    "fautes_consignees": FAUTES_CONSIGNEES}, indent=1),
        encoding="utf-8")
    print(f"  === TOTAL C run {numero} : {total:.1f} s ; code {code} "
          f"(les fautes de campagne consignées, vague 10 — jamais "
          f"réparées en silence)")
    return code


# --- LA LISTE C+G : la liste C plus les gestes de gouvernance ---------------

def bras_cg(numero: int) -> int:
    mesures = []
    t_total = time.monotonic()
    code = 0
    code |= une_etape(
        "garde-intentions-signees (g1)",
        ["python3", str(CG_GOUVERNE), "--garde"], mesures)
    code |= une_etape(
        "build-gcc-O2-loupe-01",
        f"cd {U01C} && {MINGW} -O2 -shared -o epreuves/loupe-01-c.dll "
        f"source/loupe-01-c.c source/loupe-01-c.def".split(), mesures)
    code |= une_etape("suite-tests-c-hash",
                      ["python3", "epreuve_hash_posix.py"], mesures,
                      cwd=U01C)
    code |= une_etape(
        "suite-tests-c-contrat",
        f"cd {U01C}/epreuves && gcc -O2 -o epreuve_posix epreuve_posix.c "
        f"-I. && ./epreuve_posix > observe.txt && python3 "
        f"compare_epreuve.py".split(), mesures)
    code |= une_etape("controles-binaires-loupe-01",
                      ["python3", "controles_binaires.py"], mesures,
                      cwd=U01C)
    code |= une_etape("chaine-cristallisation (g2)",
                      ["python3", str(CG_GOUVERNE), "--cristallisation"],
                      mesures)
    code |= une_etape(
        "build-gcc-O2-loupe-02",
        f"cd {REPO} && {MINGW} -O2 -shared -o scripts/campagne_d204/"
        f"unite-02-C/epreuves/loupe-02-c.dll scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.c scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.def".split(), mesures)
    code |= une_etape("epreuve-contrat-posix-loupe-02 (g3 l'oracle)",
                      f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
                      f"epreuve_posix.c && ./epreuve_posix > "
                      f"sortie-epreuve.txt && python3 compare_epreuve.py".split(),
                      mesures)
    code |= une_etape("controles-binaires-loupe-02",
                      ["python3", "scripts/campagne_d204/unite-02-C/"
                       "epreuves/controles_binaires.py"], mesures)
    code |= une_etape("assemblage-kit (g4 le gabarit)",
                      ["python3", str(CG_GOUVERNE), "--kit"], mesures)
    total = time.monotonic() - t_total
    (ICI / f"m4-CG-run{numero}.json").write_text(
        json.dumps({"bras": "C+G", "run": numero,
                    "total_s": round(total, 3),
                    "etapes": mesures, "code": code,
                    "fautes_consignees": FAUTES_CONSIGNEES}, indent=1),
        encoding="utf-8")
    print(f"  === TOTAL C+G run {numero} : {total:.1f} s ; code {code} "
          f"(les fautes de campagne consignées, vague 10)")
    return code


# --- LA LISTE C+G+ : la liste C+G PLUS le régime de vérification ------------

def bras_cgp(numero: int) -> int:
    mesures = []
    t_total = time.monotonic()
    code = 0
    # LE RÉGIME — la garde du sceau (la liste T l'ouvre pareil)
    code |= une_etape("garde-sceau-I",
                      ["python3", "v06/sceau_I.py", "verifier"], mesures)
    # LA GOUVERNANCE g1
    code |= une_etape("garde-intentions-signees (g1)",
                      ["python3", str(CG_GOUVERNE), "--garde"], mesures)
    # LE RÉGIME — LES REBUILDS DE CRISTALLISATION (les six unités × dix)
    for unite, src in UNITES:
        code |= rebuilds_cristallisation(unite, src, mesures)
    # LA BASE C — l'unité 1
    code |= une_etape(
        "build-gcc-O2-loupe-01",
        f"cd {U01C} && {MINGW} -O2 -shared -o epreuves/loupe-01-c.dll "
        f"source/loupe-01-c.c source/loupe-01-c.def".split(), mesures)
    code |= une_etape("suite-tests-c-hash",
                      ["python3", "epreuve_hash_posix.py"], mesures,
                      cwd=U01C)
    code |= une_etape(
        "suite-tests-c-contrat",
        f"cd {U01C}/epreuves && gcc -O2 -o epreuve_posix epreuve_posix.c "
        f"-I. && ./epreuve_posix > observe.txt && python3 "
        f"compare_epreuve.py".split(), mesures)
    code |= une_etape("controles-binaires-loupe-01",
                      ["python3", "controles_binaires.py"], mesures,
                      cwd=U01C)
    # LE RÉGIME — L'ORACLE ÉQUIVALENT u01 (12 épreuves, le volume du bras T)
    code |= une_etape(
        "oracle-equivalent-loupe-01 (12 épreuves)",
        f"cd {CORPUS} && gcc -O2 -I{U01C}/source -I{U01C}/epreuves "
        f"-o cgp_oracle_u01 {ICI}/cgp_oracle_u01.c && ./cgp_oracle_u01 "
        f"> cgp-sortie-u01.txt && python3 {ICI}/cgp_juge_u01.py "
        f"cgp-sortie-u01.txt".split(), mesures)
    # LA GOUVERNANCE g2
    code |= une_etape("chaine-cristallisation (g2)",
                      ["python3", str(CG_GOUVERNE), "--cristallisation"],
                      mesures)
    # LA BASE C — l'unité 2
    code |= une_etape(
        "build-gcc-O2-loupe-02",
        f"cd {REPO} && {MINGW} -O2 -shared -o scripts/campagne_d204/"
        f"unite-02-C/epreuves/loupe-02-c.dll scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.c scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.def".split(), mesures)
    # LE RÉGIME — L'ORACLE ÉQUIVALENT u02 (2032 décalages, la même graine)
    code |= une_etape(
        "oracle-equivalent-loupe-02 (2032 décalages)",
        f"cd {CORPUS} && python3 {ICI}/cgp_juge_u02.py --prepare && "
        f"gcc -O2 -I{U02C}/epreuves -I{U02C}/source -o cgp_oracle_u02 "
        f"{ICI}/cgp_oracle_u02.c && ./cgp_oracle_u02 > cgp-sortie-u02.txt "
        f"&& python3 {ICI}/cgp_juge_u02.py --juge cgp-sortie-u02.txt".split(),
        mesures)
    # LA GOUVERNANCE g3 (l'oracle du bloc à l'épreuve de contrat POSIX)
    code |= une_etape("epreuve-contrat-posix-loupe-02 (g3 l'oracle)",
                      f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
                      f"epreuve_posix.c && ./epreuve_posix > "
                      f"sortie-epreuve.txt && python3 compare_epreuve.py".split(),
                      mesures)
    code |= une_etape("controles-binaires-loupe-02",
                      ["python3", "scripts/campagne_d204/unite-02-C/"
                       "epreuves/controles_binaires.py"], mesures)
    # LE RÉGIME — LA RECOMPOSITION DU PLAN (le graphe re-vérifié)
    code |= une_etape("recomposition-du-plan",
                      ["python3", str(ICI / "cgp_recomposition.py")],
                      mesures)
    # LA GOUVERNANCE g4
    code |= une_etape("assemblage-kit (g4 le gabarit)",
                      ["python3", str(CG_GOUVERNE), "--kit"], mesures)
    total = time.monotonic() - t_total
    # le sceau APRÈS (hors la liste chronométrée — la comptabilité nommée,
    # le modèle de l'outil vague 9 : les empreintes hors du chronomètre)
    r = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                       cwd=REPO, capture_output=True, text=True)
    sceau_ok = (r.returncode == 0
                and "14 arbres VERTS" in r.stdout + r.stderr)
    # LE RÉGIME fail-closed : les étapes DU RÉGIME seules abortent — les
    # deux fautes de campagne consignées (vague 10, jamais réparées en
    # silence) sont l'état reconduit, portées au code total nommé
    code_regime = 0
    for e in mesures:
        if e["etape"] not in FAUTES_CONSIGNEES:
            code_regime |= e["code"]
    (ICI / f"m4-CGP-run{numero}.json").write_text(
        json.dumps({"bras": "C+G+", "run": numero,
                    "total_s": round(total, 3),
                    "etapes": mesures, "sceau_apres_ok": sceau_ok,
                    "code": code, "code_regime": code_regime,
                    "fautes_consignees": FAUTES_CONSIGNEES},
                   ensure_ascii=False, indent=1),
        encoding="utf-8")
    print(f"  === TOTAL C+G+ run {numero} : {total:.1f} s ; code {code} "
          f"(régime {code_regime}, les fautes consignées à part) ; "
          f"sceau {'VERT' if sceau_ok else 'ROUGE'}")
    return 0 if code_regime == 0 and sceau_ok else 2


def resume() -> None:
    import statistics
    print("\nLA MESURE M4 AUX QUATRE BRAS — les médianes (n=5 par bras)")
    for bras, fich in (("T", "m4-T"), ("CGP", "m4-CGP"), ("CG", "m4-CG"),
                       ("C", "m4-C")):
        tot = [json.load(open(ICI / f"{fich}-run{i}.json"))["total_s"]
               for i in range(1, N + 1)]
        print(f"  LE BRAS {bras} : médiane {statistics.median(tot):.2f} s "
              f"[min {min(tot):.2f}, max {max(tot):.2f}]")


def main() -> int:
    # --depuis N : les runs N..5 (le bac d'exécution tue tout processus
    # survivant à l'appel — CHAQUE run en un bloc contigu T→C+G+→C+G→C,
    # l'alternance interne INTACTE, l'écart de découpage nommé au rapport)
    depuis = 1
    if len(sys.argv) > 2 and sys.argv[1] == "--depuis":
        depuis = int(sys.argv[2])
    print("LA MESURE M4 AUX QUATRE BRAS — la même machine, n=5 par bras, "
          "l'ordre alterné T, C+G+, C+G, C (la rotation anti-dérive)")
    code = 0
    for i in range(depuis, N + 1):
        # T : la liste de la vague 9 — un échec T est un VRAI échec
        print(f"--- run {i} : le bras T ---")
        c = bras_t(i)
        if c != 0:
            print(f"[m4] REFUS : le bras T run {i} a retourné {c} — "
                  "FAIL-CLOSED")
            return c
        # C+G+ : LE RÉGIME fail-closed (les fautes consignées à part)
        print(f"--- run {i} : le bras C+G+ ---")
        c = bras_cgp(i)
        if c != 0:
            print(f"[m4] REFUS : le régime du bras C+G+ run {i} a "
                  f"retourné {c} — FAIL-CLOSED")
            return c
        # C+G puis C : la reconduction vague 10 (les fautes de campagne
        # consignées portées aux registres, jamais un arrêt)
        print(f"--- run {i} : le bras C+G ---")
        code |= bras_cg(i)
        print(f"--- run {i} : le bras C ---")
        code |= bras_c(i)
    resume()
    return code


if __name__ == "__main__":
    sys.exit(main())
