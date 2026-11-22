#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hcgp3_pilote.py — LA VENTILATION À QUATRE BRAS SUR LA PILE OPTIMISÉE
(ay6zuzm8o, la vague 13) : H-CGP3 pré-enregistré, les volumes ÉGALISÉS,
le confond « notation intrinsèque » vs « implémentation du harnais »
tranché par mesure.

LE PRÉ-ENREGISTREMENT (le plan gelé sha256:b15a74cb02f49aa1… AVANT toute
mesure) — H-CGP3 (énoncé falsifiable) : sur la pile optimisée, à volumes
de rebuilds et d'oracle ÉGALISÉS par unité, la part de l'effet NOTATION
INTRINSÈQUE (round-trips + recomposition + cristallisation, HORS
oracles) dans T−C est ≤ 30 %. Si la part mesurée > 30 %, H-CGP3 REJETÉE
et le verdict dit que le coût intrinsèque domine.

LA CLASSIFICATION PAR POSTE (figée au plan) :
  — notation intrinsèque : round-trips de notation, recomposition du
    plan, cristallisation (incrémentale : le manifeste + la fermeture) ;
  — implémentation de vérification : oracles (re-exécutions vivantes),
    gardes de sceau, épreuves confrontées ;
  — régime : rebuilds (compilations gcc côté C / reconstructions de
    pièces côté T — les volumes ÉGALISÉS par unité) ;
  — gouvernance : g1–g4 (les bras C+G/C+G+) et l'assemblage des kits
    (le g4 du bras T).

LES QUATRE BRAS (la pile optimisée, cette machine, n = 5 par bras, L'ORDRE
DES BRAS RANDOMISÉ DANS CHAQUE RUN — random.Random, la graine consignée
AVANT le premier tirage) :
  T     = l'outil M4 complet en mode CHAUD (mémo v2 + double moteur) :
          garde-sceau-I · cristallisation-incrémentale (run 1 : la semence
          full-card ; runs 2-5 : le manifeste + la fermeture) ·
          round-trips ×2 (le cache de round-trip : la semence au run 1,
          le hit + l'audit 1/10 ensuite) · REBUILDS ÉGALISÉS (10 × 6
          unités = 60 : les cinq chaînes de pièces [01, 02, 08, 13, 16]
          + le niveau bloc pour loupe-05 [AUCUNE chaîne de pièce — le gap
          nommé, la notation scellée assemblée dix fois]) · oracle-01 ·
          recomposition-02 · oracle-02 · épreuve-posix · assemblage-kits ;
  C+G+ = la liste C+G+ de la vague 11 (garde-sceau + g1 + 60 rebuilds gcc
          confrontés + base C + g2-g4), les volumes oracle ÉGAUX ;
  C+G  = g1 + base C + g2-g4 ;
  C    = base C.

LES VOLUMES ORACLE ÉGAUX (hérités de la vague 11) : u01 DOUZE épreuves /
QUATORZE contrôles ; u02 2 032 décalages, la graine 20261114.

LES TOLÉRANCES DE RÉCONCILIATION (fixées à l'avance, la vague 11) :
T ±0,150 s · C+G+ ±0,100 s · C+G, C ±0,050 s.

Sorties : m4v13-{bras}-run{N}.json (les registres bruts) ;
code 0 si tout VERT."""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import shutil
import struct
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-hcgp3-ay6zuzm8o"
V9 = REPO / "atelier-cout-boucle-cq01qv1za"
V11 = REPO / "atelier-quatrebras-3lmyfb2xa"
CG_GOUVERNE = REPO / "atelier-cg-3a91o5whb" / "cg_gouverne.py"
A11 = REPO / "atelier-porteuse-ahult8jgd"
MINGW = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-gcc-posix"
U01C = REPO / "scripts" / "campagne_d204" / "unite-01-C"
U02C = REPO / "scripts" / "campagne_d204" / "unite-02-C"
U01T = REPO / "scripts" / "campagne_d204" / "unite-01-T"
U02T = REPO / "scripts" / "campagne_d204" / "unite-02-T"

N = 5
GRAINE_ORDRE = 20261122      # consignée AVANT le premier tirage (le plan)
# la table par unité des rebuilds égalisés (publiée — le plan §1)
UNITES_T = [
    ("loupe-01", U01T, "build_unite01.py", "unite-01-T", "pièce"),
    ("loupe-02", U02T, "build_unite02.py", "unite-02-T", "pièce"),
    ("loupe-05", REPO / "loupe", None, None, "bloc"),  # AUCUNE chaîne : le
    # niveau bloc (le gap nommé — la notation scellée loupe-05-sha256)
    ("loupe-08", REPO / "scripts" / "campagne_d204" / "unite-08-T",
     "build_unite08.py", "unite-08-T", "pièce"),
    ("loupe-13", REPO / "scripts" / "campagne_d204" / "unite-13-T",
     "build_unite13.py", "unite-13-T", "pièce"),
    ("loupe-16", REPO / "scripts" / "campagne_d204" / "unite-16-T-d210",
     "build_unite16_d210.py", "unite-16-T-d210", "pièce"),
]

SCELLES = [REPO / "loupe" / "loupe.exe", REPO / "tls13" / "proxy.exe",
           REPO / "m1" / "selftest.exe",
           U01T / "piece" / "loupe.exe", U02T / "piece" / "loupe.exe"]

# la classification par poste (figée au plan)
POSTE = {
    "garde-sceau-I": "implémentation de vérification",
    "cristallisation-incrémentale": "notation intrinsèque",
    "round-trip-notation-1": "notation intrinsèque",
    "round-trip-notation-2": "notation intrinsèque",
    "recomposition-loupe-02": "notation intrinsèque",
    "rebuilds-égalisés": "régime",
    "oracle-bloc-loupe-01": "implémentation de vérification",
    "oracle-du-bloc-loupe-02": "implémentation de vérification",
    "epreuve-scenario-posix": "implémentation de vérification",
    "assemblage-kits": "gouvernance",
    "garde-intentions-signees (g1)": "gouvernance",
    "chaine-cristallisation (g2)": "gouvernance",
    "assemblage-kit (g4)": "gouvernance",
    "build-gcc-O2-loupe-01": "régime",
    "build-gcc-O2-loupe-02": "régime",
}


def sha(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def empreintes() -> dict:
    return {str(c.relative_to(REPO)): sha(c) for c in SCELLES if c.exists()}


def une_etape(nom: str, cmd, mesures, cwd=REPO, shell=False,
              capture_integrale: bool = False) -> int:
    t0 = time.monotonic()
    if isinstance(cmd, list) and cmd and cmd[0] == "cd":
        shell = True
        cmd = " ".join(cmd)
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=3600, shell=shell)
    dt = time.monotonic() - t0
    console = r.stdout if capture_integrale else r.stdout[-3000:]
    mesures.append({"etape": nom, "secondes": round(dt, 3),
                    "code": r.returncode,
                    "console": console[-50000:],
                    "stderr": r.stderr[-4000:]})
    print(f"  [{nom:<44}] {dt:7.3f} s  code {r.returncode}")
    return r.returncode


# ===========================================================================
# (A) LE BRAS T — la pile optimisée, la liste amendée de l'égalisation
# ===========================================================================

def cristallisation_incrementale(mesures, run: int) -> int:
    """LA CRISTALLISATION INCRÉMENTALE (ahult8jgd §3, la pile adoptée) :
    run 1 = LA SEMENCE full-card (le cristal posé : sha256 par notation +
    le graphe) ; runs 2-5 = LE MANIFESTE + LA FERMETURE (zéro-diff :
    l'audit 1/10 tire un bloc hors fermeture). LA LECTURE SEULE du dépôt —
    le manifeste vit à l'atelier, les notations JAMAIS touchées."""
    manifeste = ICI / "cristal-manifeste-tls13.json"
    t0 = time.monotonic()
    sys.path.insert(0, str(A11))
    import cristallisation_incrementale as CI
    base = CI.CristallisationIncrementale(
        REPO / "tls13" / "notation", manifeste)
    if run == 1 or not manifeste.exists():
        n_semis = base.semer()
        verdict = base.verifier()
        console = (f"la SEMENCE full-card : {n_semis} blocs tls13 VERTS, "
                   f"le cristal posé ; la vérification : fermeture ∅, "
                   f"l'audit a tiré {verdict['audit']}, "
                   f"{len(verdict['verifies'])} blocs vérifiés, "
                   f"verdict {verdict['verdict']}")
        code = 0 if verdict["verdict"] == "VERT" else 2
    else:
        verdict = base.verifier()
        console = (f"le MANIFESTE + LA FERMETURE (zéro-diff) : "
                   f"l'audit a tiré {verdict['audit']}, "
                   f"{len(verdict['verifies'])} blocs vérifiés, "
                   f"verdict {verdict['verdict']}")
        code = 0 if verdict["verdict"] == "VERT" else 2
    dt = time.monotonic() - t0
    mesures.append({"etape": "cristallisation-incrémentale",
                    "secondes": round(dt, 3), "code": code,
                    "console": console})
    print(f"  [{'cristallisation-incrémentale':<44}] {dt:7.3f} s  "
          f"code {code}")
    return code


def rebuilds_egalises_t(mesures, n_rebuilds: int = 10) -> int:
    """LES REBUILDS ÉGALISÉS DU BRAS T : DIX rebuilds par unité aux SIX
    unités (60 — le plan §2), la table par unité publiée au registre.
    Les CINQ chaînes de pièces (01, 02, 08, 13, 16) : la reconstruction
    COMPLÈTE de la pièce en copies hermétiques (le -o au chemin de la
    copie, les octets confrontés — l'équivalent notation de la compilation
    gcc). loupe-05 : AUCUNE chaîne de pièce n'existe (l'unité C close sur
    son rouge) — LE NIVEAU BLOC (l'assemblage keystone de la notation
    scellée + le round-trip), le gap NOMMÉ au registre."""
    code = 0
    for nom, src_dir, build, _unite, niveau in UNITES_T:
        t0 = time.monotonic()
        if niveau == "pièce":
            # les copies DIRECTEMENT sous campagne_d204 (la profondeur du
            # chemin fait le REPO calculé par le build — l'écart v182)
            copies = [REPO / "scripts" / "campagne_d204"
                      / f"_hcgp3_{nom.replace('-', '')}_r{i+1:02d}"
                      for i in range(n_rebuilds)]
            for cp in copies:
                shutil.rmtree(cp, ignore_errors=True)
            for cp in copies:
                shutil.copytree(src_dir, cp, ignore=shutil.ignore_patterns(
                    "kit", "kit-v2", "piece", "kit-temoins"))
                (cp / "piece").mkdir(exist_ok=True)
                s = (cp / build).read_text(encoding="utf-8")
                attendu = f'os.path.join(REPO, "scripts", "campagne_d204", "{_unite}")'
                if attendu not in s:
                    shutil.rmtree(racine, ignore_errors=True)
                    mesures.append({
                        "etape": f"rebuilds-égalisés-{nom}",
                        "secondes": 0.0, "code": 2,
                        "console": "REFUS : l'ancre du patcheur absente "
                        f"({build})"})
                    return 2
                (cp / build).write_text(s.replace(
                    attendu, f'os.path.join(REPO, "scripts", '
                             f'"campagne_d204", "{cp.name}")'),
                    encoding="utf-8")
                # l'unité 16 : le fallback REPO du build d'origine pointe à
                # un chemin de session morte — remplacé par le dépôt vivant
                # (le lien lab/repo2, la même profondeur)
                s16 = (cp / build).read_text(encoding="utf-8")
                if 'lab/repo2' in s16:
                    (cp / build).write_text(
                        s16.replace('if not os.path.basename(REPO) == '
                                    '"triade":', 'if False:'),
                        encoding="utf-8")
            procs = [(cp, subprocess.Popen(
                ["python3", build], cwd=cp, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True))
                for cp in copies]
            codes = {}
            for cp, p in procs:
                p.communicate(timeout=900)
                codes[cp.name] = p.returncode
            shas = {cp.name: sha(cp / "piece" / "loupe.exe")
                    for cp in copies
                    if (cp / "piece" / "loupe.exe").exists()}
            identiques = (len(shas) == n_rebuilds
                          and len(set(shas.values())) == 1)
            dt = time.monotonic() - t0
            mesures.append({
                "etape": f"rebuilds-égalisés-{nom} (×{n_rebuilds} pièces)",
                "secondes": round(dt, 3),
                "code": 0 if identiques and all(
                    v == 0 for v in codes.values()) else 2,
                "console": ("sha par rebuild : " + ", ".join(
                    f"{k}={v[:12]}" for k, v in sorted(shas.items()))
                    + f" ; {len(shas)}/{n_rebuilds} identiques")[:3000]})
            print(f"  [{'rebuilds-' + nom + ' ×10 pièces':<44}] "
                  f"{dt:7.3f} s  code {mesures[-1]['code']}")
            code |= mesures[-1]["code"]
            for cp in copies:
                shutil.rmtree(cp, ignore_errors=True)
        else:
            # LE NIVEAU BLOC (loupe-05 — le gap nommé) : l'assemblage
            # keystone de la notation scellée + le round-trip, DIX fois
            # concourants, les octets confrontés
            script = f"""
import sys, hashlib, pathlib
sys.path.insert(0, "{REPO}")
sys.path.insert(0, "{REPO / 'loupe'}")
import build_loupe as BL
L = BL.L
B4 = BL.B4
ks = BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64)
cs = BL.capstone.Cs(BL.capstone.CS_ARCH_X86, BL.capstone.CS_MODE_64)
rva, slot = L.SLOTS_LOUPE["i110005"]
octets, metas = B4.assembler_bloc(
    ks, "{REPO / 'loupe' / 'notation' / 'loupe-05-sha256.asm'}", rva, slot)
insns = B4.round_trip(cs, ks,
    "{REPO / 'loupe' / 'notation' / 'loupe-05-sha256.asm'}", rva, octets,
    metas)
assert len(insns) == len(metas), "round-trip"
print(hashlib.sha256(octets).hexdigest(), len(octets))
"""
            ftmp = ICI / "_rebuild_bloc05.py"
            ftmp.write_text(script, encoding="utf-8")
            procs = [subprocess.Popen(
                ["python3", str(ftmp)], cwd=REPO, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True) for _ in range(n_rebuilds)]
            sorties = [p.communicate(timeout=300) for p in procs]
            dt = time.monotonic() - t0
            shas = [s[0].strip().split()[0] for s in sorties
                    if s[0].strip()]
            identiques = (len(shas) == n_rebuilds
                          and len(set(shas)) == 1)
            mesures.append({
                "etape": f"rebuilds-égalisés-{nom} (×{n_rebuilds} blocs — "
                         f"AUCUNE chaîne de pièce, le gap nommé)",
                "secondes": round(dt, 3),
                "code": 0 if identiques else 2,
                "console": ("sha par assemblage : " + ", ".join(
                    s[:12] for s in shas)
                    + f" ; {len(shas)}/{n_rebuilds} identiques")[:2000]})
            print(f"  [{'rebuilds-' + nom + ' ×10 blocs':<44}] "
                  f"{dt:7.3f} s  code {mesures[-1]['code']}")
            code |= mesures[-1]["code"]
            ftmp.unlink()
    return code


def bras_t(numero: int) -> int:
    """LE BRAS T — l'outil M4 complet en mode CHAUD, la liste amendée par
    l'égalisation (le plan §2) : la cristallisation 12×u01 REMPLACÉE par
    la cristallisation INCRÉMENTALE + les rebuilds égalisés 10×6 (l'ordre
    de la liste sinon inchangé — les oracles au mémo v2, les volumes
    hérités de la vague 11)."""
    avant_emp = empreintes()
    mesures: list[dict] = []
    t_total = time.monotonic()
    print(f"=== T run {numero} — la pile optimisée, la liste amendée ===")
    memo = str(V9 / "memo-sessions-v2.json")
    code = 0
    code |= une_etape("garde-sceau-I",
                      ["python3", "v06/sceau_I.py", "verifier"], mesures)
    code |= cristallisation_incrementale(mesures, numero)
    for i in range(2):
        code |= une_etape(
            f"round-trip-notation-{i+1}",
            ["python3", "scripts/campagne_d204/unite-01-T/"
             "round_trip_unite01.py"], mesures)
    code |= rebuilds_egalises_t(mesures)
    code |= une_etape(
        "oracle-bloc-loupe-01 (parallèle)",
        ["python3", str(V9 / "oracle_unite01_v182.py"),
         "--memo", memo], mesures, capture_integrale=True)
    code |= une_etape(
        "recomposition-loupe-02",
        ["python3", "scripts/campagne_d204/unite-02-T/"
         "build_unite02.py"], mesures)
    code |= une_etape(
        "oracle-du-bloc-loupe-02 (parallèle)",
        ["python3", str(V9 / "oracle_unite02_v182.py"),
         "--memo", memo], mesures, capture_integrale=True)
    code |= une_etape(
        "epreuve-scenario-posix",
        ["python3", "scripts/campagne_d204/unite-02-T/"
         "epreuve_scenario_unite02.py"], mesures)
    c_asm = une_etape(
        "assemblage-kits",
        ["python3", "scripts/campagne_d204/assembler_kits_unite02.py"],
        mesures)
    if c_asm != 0:
        gravure = U02T / "kit"
        for canon in gravure.glob("loupe*"):
            shutil.copy2(canon, U02T / "piece" / canon.name)
        gravure_c = U02C / "kit"
        canon_c = gravure_c / "loupe-02-c.dll"
        if canon_c.exists():
            shutil.copy2(canon_c, U02C / "epreuves" / "loupe-02-c.dll")
        c_asm = une_etape(
            "assemblage-kits (reprise : la pièce canonique restaurée)",
            ["python3", "scripts/campagne_d204/"
             "assembler_kits_unite02.py"], mesures)
    code |= c_asm
    total = time.monotonic() - t_total
    apres_emp = empreintes()
    scelles_intacts = avant_emp == apres_emp
    (ICI / f"m4v13-T-run{numero}.json").write_text(
        json.dumps({"bras": "T", "run": numero,
                    "total_s": round(total, 3), "etapes": mesures,
                    "postes": {m["etape"].split(" (")[0].split("-run")[0]:
                               POSTE.get(
                        m["etape"].split(" (")[0].split(" ×")[0],
                        "régime" if m["etape"].startswith("rebuilds-")
                        else "?") for m in mesures},
                    "scelles_intacts": scelles_intacts,
                    "empreintes": apres_emp, "code": code},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  === TOTAL T run {numero} : {total:.1f} s ; code {code} ; "
          f"scellés {'INTACTS' if scelles_intacts else 'MODIFIÉS'}")
    return 0 if code == 0 and scelles_intacts else 2


# ===========================================================================
# (B) LES BRAS C+G+, C+G, C — la vague 11 reconduite aux volumes égaux
# ===========================================================================

UNITES_C = [
    ("loupe-01", U01C / "source" / "loupe-01-c.c"),
    ("loupe-02", U02C / "source" / "loupe-02-c.c"),
    ("loupe-05", REPO / "atelier-cg-3a91o5whb" / "loupe-05-c.c"),
    ("loupe-08", REPO / "scripts/campagne_d204/unite-08-C/source/"
                 "loupe-08-c.c"),
    ("loupe-13", REPO / "scripts/campagne_d204/unite-13-C/source/"
                 "loupe-13-c.c"),
    ("loupe-16", REPO / "scripts/campagne_d204/attribution-unite16-C-353/"
                 "source-loupe-16-C.c"),
]


def masques_pe(data: bytes) -> list:
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


def confrontre(echantillons: list) -> bool:
    if not echantillons or any(len(e) != len(echantillons[0])
                               for e in echantillons):
        return False
    ref = canonique(echantillons[0])
    return all(canonique(e) == ref for e in echantillons[1:])


def rebuilds_cristallisation_c(unite: str, src: pathlib.Path, mesures,
                               n_rebuilds: int = 10) -> int:
    """DIX rebuilds gcc CONCURRENTS en copies hermétiques (la vague 11
    reconduite à l'identique), les octets confrontés hors les TROIS champs
    d'horodatage du PE. loupe-05 : le build ECHEC (l'unité close sur son
    rouge) — les DIX échecs confrontés à l'octet de stderr."""
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
        console = ("sha canonique par rebuild : " + ", ".join(canons)
                   + f" ; {n_rebuilds}/{n_rebuilds} identiques : "
                   f"{identiques}")
        code = 0 if identiques else 2
    else:
        echecs = {(rc, err) for _, rc, _, err in resultats}
        cristallise = (len(echecs) == 1
                       and all(rc != 0 for rc, _ in echecs))
        premier = next(iter(echecs)) if echecs else (None, "")
        console = (f"le build mingw ECHEC aux {n_rebuilds} rebuilds : "
                   f"{len(echecs)} échec(s) distinct(s), stderr "
                   + ("IDENTIQUE — l'ECHEC cristallisé"
                      if cristallise else "DIVERGENT")
                   + " : " + premier[1][-300:])
        code = 0 if cristallise else 2
    mesures.append({"etape": f"rebuilds-cristallisation-{unite} "
                             f"(×{n_rebuilds} concourants)",
                    "secondes": round(dt_r, 3), "code": code,
                    "console": console[:4000]})
    print(f"  [{'rebuilds-' + unite + f' ×{n_rebuilds}':<44}] "
          f"{dt_r:7.3f} s  code {code}")
    shutil.rmtree(racine, ignore_errors=True)
    return code


def base_c(mesures) -> int:
    """LA BASE C — les étapes de la vague 10/11 reconduites à l'identique
    (les fautes de rig consignées demeurent, jamais réparées en silence)."""
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
    code |= une_etape(
        "epreuve-contrat-posix-loupe-02",
        f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
        f"epreuve_posix.c && ./epreuve_posix > sortie-epreuve.txt && "
        f"python3 compare_epreuve.py".split(), mesures)
    code |= une_etape(
        "controles-binaires-loupe-02",
        ["python3", "scripts/campagne_d204/unite-02-C/epreuves/"
         "controles_binaires.py"], mesures)
    return code


FAUTES_CONSIGNEES = ("suite-tests-c-contrat", "controles-binaires-loupe-01")


def bras_c(numero: int) -> int:
    mesures = []
    t_total = time.monotonic()
    code = base_c(mesures)
    total = time.monotonic() - t_total
    (ICI / f"m4v13-C-run{numero}.json").write_text(
        json.dumps({"bras": "C", "run": numero,
                    "total_s": round(total, 3), "etapes": mesures,
                    "code": code,
                    "fautes_consignees": FAUTES_CONSIGNEES},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  === TOTAL C run {numero} : {total:.1f} s ; code {code}")
    return code


def bras_cg(numero: int) -> int:
    mesures = []
    t_total = time.monotonic()
    code = 0
    code |= une_etape("garde-intentions-signees (g1)",
                      ["python3", str(CG_GOUVERNE), "--garde"], mesures)
    code |= base_c(mesures)
    code |= une_etape("chaine-cristallisation (g2)",
                      ["python3", str(CG_GOUVERNE), "--cristallisation"],
                      mesures)
    code |= une_etape("assemblage-kit (g4)",
                      ["python3", str(CG_GOUVERNE), "--kit"], mesures)
    total = time.monotonic() - t_total
    (ICI / f"m4v13-CG-run{numero}.json").write_text(
        json.dumps({"bras": "C+G", "run": numero,
                    "total_s": round(total, 3), "etapes": mesures,
                    "code": code,
                    "fautes_consignees": FAUTES_CONSIGNEES},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  === TOTAL C+G run {numero} : {total:.1f} s ; code {code}")
    return code


def bras_cgp(numero: int) -> int:
    mesures = []
    t_total = time.monotonic()
    code = 0
    code |= une_etape("garde-sceau-I",
                      ["python3", "v06/sceau_I.py", "verifier"], mesures)
    code |= une_etape("garde-intentions-signees (g1)",
                      ["python3", str(CG_GOUVERNE), "--garde"], mesures)
    for unite, src in UNITES_C:
        code |= rebuilds_cristallisation_c(unite, src, mesures)
    code |= base_c(mesures)
    code |= une_etape("chaine-cristallisation (g2)",
                      ["python3", str(CG_GOUVERNE), "--cristallisation"],
                      mesures)
    code |= une_etape("assemblage-kit (g4)",
                      ["python3", str(CG_GOUVERNE), "--kit"], mesures)
    total = time.monotonic() - t_total
    (ICI / f"m4v13-CGP-run{numero}.json").write_text(
        json.dumps({"bras": "C+G+", "run": numero,
                    "total_s": round(total, 3), "etapes": mesures,
                    "code": code,
                    "fautes_consignees": FAUTES_CONSIGNEES},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  === TOTAL C+G+ run {numero} : {total:.1f} s ; code {code}")
    return code


# ===========================================================================
# (C) LE PILOTE — l'ordre randomisé, n = 5 par bras
# ===========================================================================

BRAS = {"T": bras_t, "C+G+": bras_cgp, "C+G": bras_cg, "C": bras_c}


def main() -> int:
    ICI.mkdir(exist_ok=True)
    # le rejeu à graine identique : les tirages RECALCULÉS (bit-identiques
    # par construction — random.Random(GRAINE_ORDRE))
    rng = random.Random(GRAINE_ORDRE)
    tirages = {i: rng.sample(list(BRAS), len(BRAS)) for i in range(1, N + 1)}
    (ICI / "tirages-ordre.json").write_text(
        json.dumps({"graine": GRAINE_ORDRE,
                    "tirages": tirages}, indent=1), encoding="utf-8")
    print(f"[hcgp3] la graine d'ordre {GRAINE_ORDRE} consignée AVANT le "
          f"premier tirage ; les tirages :")
    for i in range(1, N + 1):
        print(f"  run {i} : {' → '.join(tirages[i])}")
    # l'exécution par run (le bac tue les processus de fond — chaque run
    # vit SA commande au premier plan, les registres par bras)
    runs_a_jouer = [int(x) for x in sys.argv[1:]] or list(range(1, N + 1))
    code = 0
    for i in runs_a_jouer:
        print(f"\n===== LE RUN {i} — l'ordre {tirages[i]} =====")
        for bras in tirages[i]:
            code |= BRAS[bras](i)
    print(f"\n[hcgp3] LES RUNS {runs_a_jouer} clos — code global {code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
