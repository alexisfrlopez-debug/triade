#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cgp_reconcilier.py — LA RÉCONCILIATION + LE CONTRÔLE NÉGATIF (3lmyfb2xa,
le plan § 3 et § 5) : chaque total RECALCULÉ de ses étapes, la tolérance
NOMMÉE et BORNÉE ; la faute de rig injectée dans UNE COPIE du script de
mesure ATTRAPÉE et ATTRIBUÉE au premier nom (l'étape qui dévie de sa propre
médiane).

LA RÉCONCILIATION (par bras, par run) : Σ(étapes) vs total mesuré. L'ÉCART
NOMMÉ — la comptabilité hors chronomètre d'étape :
  — le bras T : les copytrees de la cristallisation, les sha256 des pièces
    et LES EMPREINTES DES SCELLÉS (avant/après) hors du chronomètre
    d'étape — l'écart admis ~50 ms de la vague 9-10, attribué pareil ;
  — le bras C+G+ : la CONFRONTATION D'OCTETS des rebuilds (10 sha256
    canoniques + la comparaison) APRÈS l'arrêt du chronomètre d'étape, le
    sceau APRÈS hors du chronomètre total — le même genre, borné pareil ;
  — les bras C et C+G : l'inter-étapes seule (quelques ms).
LES TOLÉRANCES (publiées, bornées) : T ≤ 0,15 s ; C+G+ ≤ 0,10 s ;
C+G ≤ 0,05 s ; C ≤ 0,05 s. Tout dépassement : REFUS NOMMÉ (exit 2).

LA DÉCOMPOSITION PAR CONTRÔLE (le plan § 3) : chaque poste chronométré
séparément — rebuilds, oracles, recomposition, gardes (LES QUATRE POSTES DU
RÉGIME), plus la gouvernance g2-g4, la base C reconduite et la
comptabilité : LA SOMME DES POSTES == LE TOTAL MESURÉ (à la comptabilité
près, nommée).

LE CONTRÔLE NÉGATIF : la COPIE cgp_m4_rig.py (JAMAIS l'original) porte
time.sleep(0.5) — LA FAUTE DE RIG +500 ms — injectée à UNE étape du bras
C+G+ (la recomposition-du-plan, une PETITE étape : une faute de 500 ms sur
une étape de 5 s serait noyée dans la gigue — le choix PUBLIÉ) ; le registre
rig écrit à m4-CGP-rig-run6.json (JAMAIS fusionné aux registres bruts). LA
DÉTECTION (aveugle au site d'injection) : pour chaque étape du registre
suspect, la déviation à SA PROPRE MÉDIANE (les 5 runs honnêtes),
NORMALISÉE par le facteur de dérive du run (total/médiane des totaux — la
dérive machine est multiplicative, la faute est additive) ; FAUTIVE si
déviation normalisée > 0,30 s ET valeur > 2 × la médiane de l'étape. LA
SPÉCIFICITÉ : la même règle aux 5 runs honnêtes (médianes hors ce run)
DOIT ne rien signaler. L'ATTRIBUTION : le premier nom signalé, confronté
au site d'injection (connu du seul verdict).

Usage :
  python3 cgp_reconcilier.py                    # réconciliation + tables
  python3 cgp_reconcilier.py --controle-negatif # le rig (+ la détection)
  python3 cgp_reconcilier.py --tout             # les deux
"""
from __future__ import annotations

import json
import pathlib
import shutil
import statistics
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
N = 5
BRAS = (("T", "m4-T"), ("CGP", "m4-CGP"), ("CG", "m4-CG"), ("C", "m4-C"))

# LES TOLÉRANCES DE RÉCONCILIATION (publiées, bornées — la comptabilité
# hors chronomètre d'étape, nommée par bras)
TOLERANCES = {"T": 0.150, "CGP": 0.100, "CG": 0.050, "C": 0.050}

# LA FAUTE DE RIG (le contrôle négatif) : +500 ms à UNE étape — le site
# publié : une PETITE étape du régime (voir l'en-tête)
RIG_ETAPE_CIBLE = "recomposition-du-plan"
RIG_INJECT_MS = 500
RIG_RUN = 6

# --- LA CLASSIFICATION DES POSTES (le plan § 3 : chaque poste chronométré) ---

POSTES_CGP = [   # (le nom du poste, le prédicat d'étape)
    ("REBUILDS (le régime, l'équivalent compilé du round-trip)",
     lambda e: e.startswith("rebuilds-cristallisation-")),
    ("ORACLES (le régime, les volumes équivalents)",
     lambda e: e.startswith("oracle-equivalent-")),
    ("RECOMPOSITION (le régime, le graphe re-vérifié)",
     lambda e: e == "recomposition-du-plan"),
    ("GARDES (le régime + g1)",
     lambda e: e in ("garde-sceau-I", "garde-intentions-signees (g1)")),
    ("GOUVERNANCE g2-g4 (g3 vit à la base C, nommé)",
     lambda e: e in ("chaine-cristallisation (g2)",
                     "assemblage-kit (g4 le gabarit)")),
    ("BASE C reconduite (la liste C, g3 compris)",
     lambda e: e in ("build-gcc-O2-loupe-01", "suite-tests-c-hash",
                     "suite-tests-c-contrat",
                     "controles-binaires-loupe-01",
                     "build-gcc-O2-loupe-02",
                     "epreuve-contrat-posix-loupe-02 (g3 l'oracle)",
                     "controles-binaires-loupe-02")),
]

POSTES_T = [
    ("GARDES (garde-sceau-I)", lambda e: e == "garde-sceau-I"),
    ("CRISTALLISATION ×12 (l'unité 01 seule)",
     lambda e: e.startswith("cristallisation-")),
    ("ROUND-TRIPS de notation (×2, l'octet juge)",
     lambda e: e.startswith("round-trip-notation-")),
    ("ORACLES (bloc 01 + bloc 02)",
     lambda e: e.startswith("oracle-")),
    ("BUILD-RECOMPOSITION (l'unité 02 recomposée)",
     lambda e: e == "build-recomposition-loupe-02"),
    ("ÉPREUVE scénario POSIX",
     lambda e: e == "epreuve-scenario-posix"),
    ("KITS (assemblage + reprise)",
     lambda e: e.startswith("assemblage-kits")),
]


def charger() -> dict[str, list[dict]]:
    """LES REGISTRES BRUTS — les 5 runs par bras, JAMAIS le rig."""
    out = {}
    for bras, fich in BRAS:
        runs = []
        for i in range(1, N + 1):
            p = ICI / f"{fich}-run{i}.json"
            if not p.exists():
                sys.exit(f"[reconcilier] REFUS : {p} ABSENT — la mesure "
                         "d'abord (cgp_m4.py)")
            runs.append(json.loads(p.read_text(encoding="utf-8")))
        out[bras] = runs
    return out


def somme_etapes(run: dict) -> float:
    return sum(e["secondes"] for e in run["etapes"])


# --- LA RÉCONCILIATION : chaque total recalculé de ses étapes ---------------

def reconcilier(data: dict) -> int:
    print("=== LA RÉCONCILIATION — chaque total recalculé de ses étapes "
          "(les tolérances nommées) ===")
    refus = 0
    for bras, _ in BRAS:
        for run in data[bras]:
            s = somme_etapes(run)
            ecart = run["total_s"] - s
            hors = ecart > TOLERANCES[bras] + 1e-9 or ecart < -0.005 - 1e-9
            refus += hors
            print(f"  {bras:>3} run {run['run']} : total "
                  f"{run['total_s']:8.3f} s = Σétapes {s:8.3f} s "
                  f"+ comptabilité {ecart:+7.3f} s "
                  f"[tolérance ±{TOLERANCES[bras]:.3f}] "
                  f"{'HORS TOLÉRANCE — REFUS' if hors else 'ok'}")
    if refus:
        print(f"[reconcilier] REFUS : {refus} run(s) hors tolérance")
    else:
        print("  LES QUATRE BRAS RÉCONCILIÉS — la somme des étapes == le "
              "total mesuré, la comptabilité nommée et bornée")
    return refus


# --- LES MÉDIANES ET LA RÈGLE DE DÉCISION -----------------------------------

def medianes(data: dict) -> dict[str, float]:
    print("\n=== LA MESURE M4 AUX QUATRE BRAS — les médianes (n=5, "
          "l'ordre alterné T, C+G+, C+G, C) ===")
    med = {}
    for bras, _ in BRAS:
        tot = [r["total_s"] for r in data[bras]]
        med[bras] = statistics.median(tot)
        print(f"  LE BRAS {bras:<3}: médiane {med[bras]:7.2f} s "
              f"[min {min(tot):7.2f}, max {max(tot):7.2f}]")
    dt_cgp = med["T"] - med["CGP"]
    dt_cg = med["T"] - med["CG"]
    dregime = med["CGP"] - med["CG"]
    dgouv = med["CG"] - med["C"]
    print(f"\n  T−C+G+ = {dt_cgp:.2f} s (l'effet notation PROPRE, la "
          f"question) ; T−C+G = {dt_cg:.2f} s (cette session ; la vague 10 "
          f"publiait 37,07 s)")
    print(f"  C+G+−C+G = {dregime:.2f} s (l'effet RÉGIME de vérification) ; "
          f"C+G−C = {dgouv:.3f} s (l'effet GOUVERNANCE, la vague 10 "
          f"publiait 0,215 s)")
    ratio = dt_cgp / dt_cg if dt_cg > 0 else float("inf")
    print(f"\n  LA RÈGLE DE DÉCISION (le plan § 4) : (T−C+G+) ≤ 30 % de "
          f"(T−C+G) ?")
    print(f"    (T−C+G+)/T−C+G = {dt_cgp:.2f}/{dt_cg:.2f} = "
          f"{100 * ratio:.1f} % "
          f"{'≤' if ratio <= 0.30 else '>'} 30 %")
    for ref, nom in ((dt_cg, "cette session (appariée, la même machine)"),
                     (37.07, "la référence vague 10 (37,07 s)")):
        r = dt_cgp / ref
        print(f"    recoup {nom} : {100 * r:.1f} % "
              f"{'— LA REQUALIFICATION' if r <= 0.30 else '— l''effet notation propre CONFIRMÉ'}")
    if ratio <= 0.30:
        print("  LE VERDICT : LA REQUALIFICATION — « effet notation isolé » "
              "devient « effet régime de vérification » (à porter aux "
              "pièces par le contrôleur)")
    else:
        print("  LE VERDICT : L'EFFET NOTATION PROPRE CONFIRMÉ — la "
              "ventilation trois-effets : notation propre "
              f"{dt_cgp:.2f} s / régime de vérification {dregime:.2f} s / "
              f"gouvernance {dgouv:.3f} s")
    return med


# --- LA DÉCOMPOSITION PAR CONTRÔLE ------------------------------------------

def decomposer(run: dict, postes: list) -> dict[str, float]:
    """La somme par poste d'UN run + la comptabilité (le poste final)."""
    out: dict[str, float] = {nom: 0.0 for nom, _ in postes}
    for e in run["etapes"]:
        for nom, pred in postes:
            if pred(e["etape"]):
                out[nom] += e["secondes"]
                break
        else:
            out.setdefault("AUTRES (non classé — REFUS)", 0.0)
            out["AUTRES (non classé — REFUS)"] += e["secondes"]
    out["COMPTABILITÉ (hors chronomètre d'étape)"] = \
        round(run["total_s"] - somme_etapes(run), 3)
    return out


def table_postes(data: dict, bras: str, postes: list, titre: str) -> None:
    print(f"\n=== LA DÉCOMPOSITION PAR CONTRÔLE — {titre} ===")
    lignes = [decomposer(r, postes) for r in data[bras]]
    noms = list(lignes[0].keys())
    for nom in noms:
        vals = [l[nom] for l in lignes]
        m = statistics.median(vals)
        part = 100 * m / statistics.median(
            [r["total_s"] for r in data[bras]])
        print(f"  {nom:<58} médiane {m:7.3f} s  ({part:5.1f} % du total) "
              f"[min {min(vals):7.3f}, max {max(vals):7.3f}]")
    s = statistics.median([sum(l.values()) for l in lignes])
    t = statistics.median([r["total_s"] for r in data[bras]])
    print(f"  {'Σ DES POSTES (médiane)':<58} {s:7.3f} s  == total médian "
          f"{t:.3f} s (écart {s - t:+.3f} s, la sommation des médianes vs "
          "la médiane des sommes — nommée)")


# --- LE CONTRÔLE NÉGATIF -----------------------------------------------------

def medians_etapes(runs: list[dict]) -> dict[str, float]:
    out: dict[str, float] = {}
    for e in runs[0]["etapes"]:
        nom = e["etape"]
        vals = []
        for r in runs:
            for x in r["etapes"]:
                if x["etape"] == nom:
                    vals.append(x["secondes"])
        out[nom] = statistics.median(vals)
    return out


def detecter(suspect: dict, honnetes: list[dict], seuil: float = 0.30
             ) -> list[tuple[str, float, float, float]]:
    """LA DÉTECTION : l'étape qui dévie de sa propre médiane, NORMALISÉE
    par le facteur de dérive du run (la dérive machine est multiplicative,
    la faute additive). Retourne [(étape, valeur, médiane, déviation)]."""
    med = medians_etapes(honnetes)
    facteur = suspect["total_s"] / statistics.median(
        [r["total_s"] for r in honnetes])
    signalees = []
    for e in suspect["etapes"]:
        m = med.get(e["etape"])
        if m is None or m <= 0:
            continue
        attendu = m * facteur
        dev = e["secondes"] - attendu
        if dev > seuil and e["secondes"] > 2 * m:
            signalees.append((e["etape"], e["secondes"], m, dev))
    return signalees


def construire_rig(variante: str) -> pathlib.Path:
    """LA COPIE du script de mesure, JAMAIS l'original : la faute de rig
    +500 ms injectée à UNE étape (le site publié : « recomposition-du-plan
    », une PETITE étape du régime — une faute de 500 ms sur une étape de
    5 s serait noyée dans la gigue des rebuilds concourants, le choix
    nommé). DEUX VARIANTES :
      A « inter-étapes » : time.sleep(0,5) AVANT l'appel d'étape — la
        faute vit dans la COMPTABILITÉ du run (hors tout chronomètre
        d'étape) : seule LA BORNE de réconciliation l'attrape ;
      B « in-étape » : sleep 0,5 DANS la commande de l'étape — la faute
        vit DANS le chronomètre de l'étape : LE SCAN d'étape l'attrape
        (l'étape qui dévie de sa propre médiane)."""
    orig = ICI / "cgp_m4.py"
    rig = ICI / f"cgp_m4_rig_{variante}.py"
    texte = orig.read_text(encoding="utf-8")
    marque = "    # LE RÉGIME — LA RECOMPOSITION DU PLAN (le graphe " \
             "re-vérifié)\n"
    if marque not in texte:
        sys.exit("[rig] REFUS : le site d'injection introuvable — "
                 "l'original a-t-il changé ?")
    if variante == "A":
        faux = texte.replace(
            marque,
            marque + f"    time.sleep({RIG_INJECT_MS / 1000:.1f})"
                     "  # LA FAUTE DE RIG INJECTÉE (inter-étapes)\n", 1)
    else:
        cible = '["python3", str(ICI / "cgp_recomposition.py")],'
        if cible not in texte:
            sys.exit("[rig] REFUS : la commande d'étape introuvable")
        faux = texte.replace(
            cible,
            f'["sh", "-c", "sleep {RIG_INJECT_MS / 1000:.1f} && python3 "'
            f"\n                       + repr(str(ICI / "
            f'"cgp_recomposition.py"))],', 1)
    faux = faux.replace('(ICI / f"m4-CGP-run{numero}.json")',
                        f'(ICI / f"m4-CGP-rig{variante}-run{{numero}}.json")',
                        1)
    faux = faux.replace(
        'if __name__ == "__main__":\n    sys.exit(main())',
        f'if __name__ == "__main__":\n'
        f'    # LE MODE RIG : UNE SEULE exécution du bras C+G+ '
        f'(run {RIG_RUN},\n'
        f'    # le registre RIG à part, JAMAIS fusionné aux registres '
        f'bruts)\n'
        f'    sys.exit(bras_cgp({RIG_RUN}))', 1)
    rig.write_text(faux, encoding="utf-8")
    return rig


def executer_rig(rig: pathlib.Path, variante: str) -> dict:
    r = subprocess.run([sys.executable, str(rig)], cwd=ICI,
                       capture_output=True, text=True, timeout=600)
    print((r.stdout + r.stderr).strip()[-400:])
    p = ICI / f"m4-CGP-rig{variante}-run{RIG_RUN}.json"
    if r.returncode != 0 or not p.exists():
        sys.exit(f"[rig] REFUS : l'exécution rig {variante} a retourné "
                 f"{r.returncode}")
    return json.loads(p.read_text(encoding="utf-8"))


def controle_negatif() -> int:
    print("=== LE CONTRÔLE NÉGATIF — la faute de rig +500 ms dans UNE "
          "COPIE du script de mesure (l'original JAMAIS touché) ===")
    sha_orig = subprocess.run(["sha256sum", str(ICI / "cgp_m4.py")],
                              capture_output=True,
                              text=True).stdout.split()[0]
    print(f"  l'original cgp_m4.py intact (sha256 {sha_orig[:12]}…) ; le "
          f"site d'injection publié : « {RIG_ETAPE_CIBLE} » (+"
          f"{RIG_INJECT_MS} ms), DEUX variantes du rig")

    data = charger()
    honnetes = data["CGP"]
    code = 0

    # --- LA VARIANTE A : la faute INTER-ÉTAPES — la borne de comptabilité --
    print(f"\n  LA VARIANTE A (inter-étapes) — la copie "
          f"cgp_m4_rig_A.py exécutée :")
    rig_a = executer_rig(construire_rig("A"), "A")
    compta = rig_a["total_s"] - somme_etapes(rig_a)
    hors = compta > TOLERANCES["CGP"]
    print(f"    LA DÉTECTION PAR LA BORNE : comptabilité du run rig = "
          f"total {rig_a['total_s']:.3f} − Σétapes "
          f"{somme_etapes(rig_a):.3f} = {compta:+.3f} s "
          f"[tolérance ±{TOLERANCES['CGP']:.3f}] — "
          f"{'HORS TOLÉRANCE : ATTRAPÉE' if hors else 'SOUS LA BORNE : NON ATTRAPÉE — REFUS'}")
    scan_a = detecter(rig_a, honnetes)
    print(f"    le scan d'étape (aveugle) : "
          f"{len(scan_a)} étape(s) signalée(s) — la faute inter-étapes "
          f"est INVISIBLE au scan (hors chronomètre d'étape), NOMMÉ : "
          f"seule la borne l'attrape")
    code |= 0 if hors else 2

    # --- LA VARIANTE B : la faute IN-ÉTAPE — le scan d'étape ---------------
    print(f"\n  LA VARIANTE B (in-étape) — la copie "
          f"cgp_m4_rig_B.py exécutée :")
    rig_b = executer_rig(construire_rig("B"), "B")
    print("    LA DÉTECTION — l'étape qui dévie de sa propre médiane "
          "(dérive normalisée, seuil 0,30 s ET valeur > 2× médiane) :")
    signalees = detecter(rig_b, honnetes)
    if not signalees:
        print("    RIEN SIGNALÉ — la faute NON ATTRAPÉE : REFUS")
        code |= 2
    else:
        for nom, val, med, dev in signalees:
            print(f"    SIGNALÉE : « {nom} » = {val:.3f} s (sa médiane "
                  f"{med:.3f} s, déviation normalisée {dev:+.3f} s)")
        fautive = signalees[0][0]    # L'ATTRIBUTION AU PREMIER NOM
        print(f"    L'ATTRIBUTION AU PREMIER NOM : « {fautive} » "
              f"(run rig {RIG_RUN})")
        ok = fautive == RIG_ETAPE_CIBLE
        print(f"    le site vrai : « {RIG_ETAPE_CIBLE} » — "
              f"{'VERT' if ok else 'ROUGE (attribution divergente)'}")
        code |= 0 if ok else 2

    # --- LA SPÉCIFICITÉ : la même règle aux 5 runs honnêtes ----------------
    print("\n  LA SPÉCIFICITÉ — la même règle aux 5 runs honnêtes "
          "(médianes hors ce run) :")
    faux_pos = 0
    for i, run in enumerate(honnetes):
        autres = honnetes[:i] + honnetes[i + 1:]
        for nom, val, med, dev in detecter(run, autres):
            faux_pos += 1
            print(f"    FAUX POSITIF : run {run['run']} « {nom} » = "
                  f"{val:.3f} s (médiane {med:.3f}, dév. {dev:+.3f})")
    if faux_pos:
        print(f"    {faux_pos} faux positif(s) — la règle manque de "
              "spécificité : REFUS")
        code |= 2
    else:
        print("    AUCUN faux positif — la règle est spécifique")

    print(f"\n  LE VERDICT DU CONTRÔLE NÉGATIF : "
          f"{'VERT' if code == 0 else 'ROUGE'} — la faute +{RIG_INJECT_MS} "
          f"ms ATTRAPÉE aux DEUX fenêtres (la borne de comptabilité pour "
          f"l'inter-étapes, le scan d'étape pour l'in-étape) et ATTRIBUÉE "
          f"au premier nom « {RIG_ETAPE_CIBLE} »")
    return code


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--controle-negatif":
        return controle_negatif()
    data = charger()
    code = reconcilier(data)
    medianes(data)
    table_postes(data, "CGP", POSTES_CGP,
                 "LE BRAS C+G+ (les postes du régime en tête)")
    table_postes(data, "T", POSTES_T, "LE BRAS T (la ventilation du régime)")
    table_postes(data, "CG", [
        ("GOUVERNANCE g1-g4 (les gestes)",
         lambda e: e.startswith("garde-intentions") or e.startswith("chaine-")
         or e.startswith("assemblage-kit")),
        ("BASE C (la liste C, g3 compris)",
         lambda e: not (e.startswith("garde-intentions")
                        or e.startswith("chaine-")
                        or e.startswith("assemblage-kit"))),
    ], "LE BRAS C+G (la gouvernance sur la base C)")
    table_postes(data, "C", [
        ("BASE C (la liste C)",
         lambda e: True),
    ], "LE BRAS C (le compilé nu)")
    if mode == "--tout":
        code |= controle_negatif()
    return code


if __name__ == "__main__":
    sys.exit(main())
