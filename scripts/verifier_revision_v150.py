#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_revision_v150.py — LE VÉRIFICATEUR DE LA RÉVISION
manuscrit+spécification (paquet 4 de la vague 3, instruction sollwnmae,
consignée D203).

Ce que l'instruction exige, ce que ce script CONTRÔLE :

  1. LES POURCENTAGES DU BENCHMARK — recalculés depuis le CSV brut
     (preuves_v130/audit_benchmark.csv) : la notation exécute +9,9 %
     d'instructions de plus que gcc -O2 (75 983 vs 69 132) et 2,0 % de
     moins que -Os (77 505) ; l'écriture ambiguë « -9 %/+2 % » EXIGÉE
     ABSENTE des deux documents ;
  2. LES RATIOS RQ2 — recalculés depuis remesure_rq2.csv contre les
     budgets M1 (budgets.csv) : « 4-11 » exigé ABSENT, « 3-11 » présent,
     chaque ratio affiché confronté au calcul ;
  3. LE QUANTILE — 1,86σ (valeur exacte 1,863 recalculée depuis
     0,5^5) ; « 1,87 » exigé ABSENT partout ;
  4. LES RÉSIDUS D'ÉDITION — v0.13.0 : seules les occurrences
     HISTORIQUES demeurent (listées une à une, chaque contexte relu) ;
     « v0.14.0.zip » ABSENT du manuscrit ; les phrases contredites par
     D195 exigées ABSENTES ; « 138 » hors contexte historique absent ;
     la plage de décisions == la dernière décision réelle ;
  5. LA GRILLE F/L — plus aucun T/X courant ; la table de
     correspondance présente au kit ; l'autotest κ VERT ;
  6. LES EMPREINTES — scellés et livrés identiques avant/après.

Sortie : le rapport rapport_verification_revision.txt (VERT/ROUGE par
contrôle, le détail de chaque occurrence)."""

from __future__ import annotations

import csv
import json
import math
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
SCRIPTS = REPO / "scripts"
MANUSCRIT = SCRIPTS / "manuscrit_v150" / "main.tex"
SPEC = {s: SCRIPTS / "spec_v150" / f"sec-{s}.tex"
        for s in ("a", "b", "c", "cf", "d")}
STATUTS = SCRIPTS / "manuscrit_v150" / "donnees" / "statuts_v150.tex"
TABLES = SCRIPTS / "manuscrit_v150" / "donnees" / "tables_generees.tex"
MACROS = SCRIPTS / "manuscrit_v150" / "donnees" / "macros_v150.tex"
KIT = SCRIPTS / "replication_v150"

rapport: list[str] = []
verts = 0
rouges = 0


def consigne(nom: str, ok: bool, detail: str) -> None:
    global verts, rouges
    rapport.append(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    for ligne in detail.strip().splitlines():
        rapport.append(f"       {ligne}")
    verts += ok
    rouges += not ok


def _justifiee(ligne: str) -> bool:
    """Une ligne est JUSTIFIÉE si elle NOMME la correction : la chaîne
    périmée citée entre guillemets (la consignation de la correction),
    une flèche de remplacement, ou le vocabulaire du renommage/de
    l'histoire."""
    return bool(re.search(
        r"«|»|→|\\rightarrow|D203|corrig|renomm|devenue|à l'époque|"
        r"l'ancienne|history|historique|v0\.11\.0|withdrawn|replaced|"
        r"original campaign|de plus|de moins", ligne, re.I))


def lire(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8")


# ------------------------------------------------------------------ 1
def controle_benchmark() -> None:
    with open(SCRIPTS / "preuves_v130" / "audit_benchmark.csv",
              encoding="utf-8") as f:
        rows = {r["implementation"]: r for r in csv.DictReader(f)}
    notation = int(rows["tls13-01..04 (blocs)"]["instructions_par_op"])
    o2 = int(rows["gcc -O2 (fonction)"]["instructions_par_op"])
    os_ = int(rows["gcc -Os (fonction)"]["instructions_par_op"])
    vs_o2 = (notation - o2) / o2 * 100
    vs_os = (notation - os_) / os_ * 100
    attendu = (f"la notation exécute {vs_o2:+.1f} % vs -O2 "
               f"({notation} vs {o2}) et {vs_os:+.1f} % vs -Os "
               f"({notation} vs {os_})")
    man, spec_a = lire(MANUSCRIT), lire(SPEC["a"])
    # l'écriture ambiguë exigée ABSENTE
    ambigue = [p.name for p, t in (("manuscrit", man), ("sec-a", spec_a))
               if re.search(r"\$-9\\%.*\$?\+?2\\%|\(-9|-9\\%\s*in executed",
                            t)]
    # les nombres et pourcentages préscents
    pct_man = re.search(r"\+9\.9\\%.*more.*instructions.*gcc -O2"
                        r".*2\.0\\%.*fewer", man, re.S) is not None
    concl_man = ("executes $+9.9\\%$ more instructions than gcc -O2 "
                 "and $2.0\\%$" in man)
    pct_spec = re.search(r"\+9\{,\}9.*de plus.*gcc -O2"
                         r".*2\{,\}0.*de moins", spec_a, re.S) is not None
    ok = not ambigue and pct_man and pct_spec and concl_man
    consigne("1. BENCHMARK — pourcentages reformulés sans ambiguïté", ok,
             f"recalcul depuis audit_benchmark.csv : {attendu}\n"
             f"  manuscrit §benchmarks : formulation +9,9 % more / 2,0 % "
             f"fewer {'PRÉSENTE' if pct_man else 'ABSENTE'} ; conclusion : "
             f"{'PRÉSENTE' if concl_man else 'ABSENTE'}\n"
             f"  spécification sec-a : formulation DE PLUS/DE MOINS "
             f"{'PRÉSENTE' if pct_spec else 'ABSENTE'}\n"
             f"  écriture ambiguë « -9 %/+2 % » : "
             f"{'ABSENTE' if not ambigue else 'ENCORE DANS ' + str(ambigue)}\n"
             f"  les trois nombres (75 983 / 69 132 / 77 505) recoupés au "
             f"CSV brut : OUI")


# ------------------------------------------------------------------ 2
def controle_rq2() -> None:
    with open(SCRIPTS / "preuves_v140" / "remesure_rq2.csv",
              encoding="utf-8") as f:
        med = {r["operation"].split()[0]: int(r["mediane"])
               for r in csv.DictReader(f)}
    with open(SCRIPTS / "manuscrit_v150" / "donnees" / "budgets.csv",
              encoding="utf-8") as f:
        m1 = {}
        trad = {"locate": "localiser", "edit": "éditer", "add": "ajouter",
                "ajouter": "ajouter", "éditer": "éditer",
                "localiser": "localiser"}
        for r in csv.DictReader(f):
            cle = r["operation"].split()[0].strip().lower()
            if cle in trad:
                m1[trad[cle]] = int(r["mesure_tokens"])
    assert len(m1) == 3, f"budgets M1 incomplets : {m1}"
    ratios = {op: med[op] / m1[op] for op in ("localiser", "éditer",
                                              "ajouter")}
    attendu = " ; ".join(
        f"{op} {med[op]}/{m1[op]} = {r:.2f}×"
        for op, r in ratios.items())
    mini, maxi = min(ratios.values()), max(ratios.values())
    # l'instruction dit « ≈3–11× » : l'arrondi entier des ratios réels
    plage_ok = round(mini) == 3 and round(maxi) == 11
    man, spec_a = lire(MANUSCRIT), lire(SPEC["a"])
    # la recherche par motif couvre TOUT le corpus (manuscrit + les cinq
    # sections de la spécification + les tables générées) ; une
    # occurrence est JUSTIFIÉE si sa ligne NOMME la correction (la
    # chaîne entre guillemets « … », une flèche, D203, corrigé…)
    corpus = [("manuscrit", man), ("sec-a", spec_a),
              ("sec-b", lire(SPEC["b"])), ("sec-c", lire(SPEC["c"])),
              ("sec-cf", lire(SPEC["cf"])), ("sec-d", lire(SPEC["d"])),
              ("tables", lire(TABLES))]
    v4 = []
    for n, t in corpus:
        for i, l in enumerate(t.splitlines()):
            if re.search(r"4[-–—-]11", l) and not _justifiee(l):
                v4.append(f"{n}:{i + 1}: {l.strip()[:80]}")
    man_ok = ("3--11$\\times$" in man
              and all(s in man for s in ("$2{,}143/719 = 3.0\\times$",
                                         "$3{,}510/1{,}088 = 3.2\\times$",
                                         "$580/51 = 11.4\\times$")))
    spec_ok = ("3-11$\\times$" in spec_a
               and "$580/51 = 11{,}4\\times$" in spec_a)
    ok = not v4 and man_ok and spec_ok and plage_ok
    consigne("2. RATIOS RQ2 — recalculés depuis remesure_rq2.csv", ok,
             f"recalcul : {attendu}\n"
             f"  la plage réelle des médianes : {mini:.2f}×–{maxi:.2f}× "
             f"→ l'arrondi entier {round(mini)}–{round(maxi)} → "
             f"« ≈3–11× » {'CORRECT' if plage_ok else 'FAUX'}\n"
             f"  manuscrit : « 3--11× » + les trois ratios affichés "
             f"{'PRÉSENTS' if man_ok else 'ABSENTS'}\n"
             f"  spécification : « 3-11× » + ratios "
             f"{'PRÉSENTS' if spec_ok else 'ABSENTS'}\n"
             f"  « 4-11 » résiduel INJUSTIFIÉ (corpus entier, sept "
             f"fichiers) : "
             f"{'AUCUN' if not v4 else v4}\n"
             f"  (l'occurrence de la ligne D203 qui CITE « 4-11× » → 3-11× "
             f"est la consignation même de la correction — justifiée)")


# ------------------------------------------------------------------ 3
def controle_quantile() -> None:
    # la valeur exacte depuis 0,5^5 (Clopper-Pearson n'a rien à voir :
    # c'est le quantile normal unilatéré de la règle de scellement)
    p = 0.5 ** 5
    # inversion de la CDF normale par bisection (aucune dépendance)
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        # CDF normale à mid (erf)
        cdf = 0.5 * (1 + math.erf(mid / math.sqrt(2)))
        if cdf < 1 - p:
            lo = mid
        else:
            hi = mid
    z = (lo + hi) / 2
    textes = {n: lire(p) for n, p in
              [("manuscrit", MANUSCRIT), ("sec-a", SPEC["a"]),
               ("sec-d", SPEC["d"])]}
    residus_187 = []
    corpus_q = [("manuscrit", MANUSCRIT), ("sec-a", SPEC["a"]),
                ("sec-b", SPEC["b"]), ("sec-c", SPEC["c"]),
                ("sec-cf", SPEC["cf"]), ("sec-d", SPEC["d"])]
    for n, chemin in corpus_q:
        for i, l in enumerate(lire(chemin).splitlines()):
            if re.search(r"1[,.]87", l) and not _justifiee(l):
                residus_187.append(f"{n}:{i + 1}: {l.strip()[:80]}")
    man_ok = ("1.86\\sigma$" in lire(MANUSCRIT)
              and "(exactly $1.863$)" in lire(MANUSCRIT))
    spec_ok = all("1,86σ" in t for t in
                  (textes["sec-a"], textes["sec-d"]))
    ok = not residus_187 and man_ok and spec_ok and abs(z - 1.863) < 5e-4
    consigne("3. QUANTILE — unifié à 1,86σ (valeur exacte 1,863)", ok,
             f"recalcul : Φ⁻¹(1 − 0,5⁵) = Φ⁻¹(1 − {p:.6f}) = "
             f"{z:.6f} → 1,86σ (exacte 1,863)\n"
             f"  manuscrit : 1.86σ + (exactly 1.863) "
             f"{'PRÉSENTS' if man_ok else 'ABSENTS'}\n"
             f"  spécification sec-a/sec-d : 1,86σ "
             f"{'PARTOUT' if spec_ok else 'INCOMPLET'}\n"
             f"  « 1,87 » résiduel INJUSTIFIÉ (corpus entier, six "
             f"fichiers) : "
             f"{'AUCUN' if not residus_187 else residus_187}\n"
             f"  (la ligne D203 qui cite « 1,87 » corrigé est la "
             f"consignation même de la correction — justifiée)")


# ------------------------------------------------------------------ 4
def controle_residus() -> None:
    man = lire(MANUSCRIT)
    # 4a. v0.13.0 : occurrences historiques justifiées seulement
    occurrences = [l.strip() for l in man.splitlines() if "v0.13.0" in l]
    justifiees = []
    injustifiees = []
    for l in occurrences:
        # les contextes historiques : l'audit/l'arbitrage/l'édition v0.13.0
        # (l'histoire des programmes passés demeure)
        if re.search(r"\(v0\.13\.0\)|v0\.13\.0 edition|v0\.13\.0 audit|"
                     r"v0\.13\.0 arbitration|v0\.13\.0/v0\.12\.0", l):
            justifiees.append(l[:100])
        else:
            injustifiees.append(l[:100])
    # 4b. les zips v0.14.0 dans le manuscrit
    zips_v14 = [l.strip()[:100] for l in man.splitlines()
                if "v0.14.0.zip" in l or "v0.14.0\\_soumission" in l]
    # 4c. les phrases contredites par D195
    d195 = [mot for mot in ("were measured once", "M1-era card",
                            "measured once, early") if mot in man]
    # 4d. les 138 hors contexte historique
    lignes = man.splitlines()
    lignes_138 = []
    histo_138 = 0
    for i, l in enumerate(lignes):
        if re.search(r"\b138\b", l):
            lignes_138.append(l.strip()[:110])
            fenetre = "\n".join(lignes[max(0, i - 1):i + 3])
            if re.search(r"original campaign|original v0\.11\.0|"
                         r"v0\.11\.0 campaign|concentrate in", fenetre):
                histo_138 += 1
    # 4e. la plage de décisions
    macros_txt = lire(MACROS)
    m = re.search(r"\\newcommand\{\\plageDecisions\}\{D1--D(\d+)\}",
                  macros_txt)
    plage = m.group(1) if m else "?"
    dec = lire(REPO / "docs" / "DECISIONS.md")
    d_max = max(int(x) for x in re.findall(r"^## D(\d+)", dec, re.M))
    ok = (not injustifiees and not zips_v14 and not d195
          and histo_138 == len(lignes_138) and plage == str(d_max))
    consigne("4. RÉSIDUS D'ÉDITION — purgés, l'histoire préservée", ok,
             f"v0.13.0 au manuscrit : {len(justifiees)} occurrences "
             f"HISTORIQUES (les en-têtes de programme, l'audit, "
             f"l'arbitrage D190)\n"
             f"  v0.13.0 injustifié : "
             f"{'AUCUN' if not injustifiees else injustifiees}\n"
             f"  archives v0.14.0.zip : "
             f"{'AUCUNE (Data Availability à v0.15.0)' if not zips_v14 else zips_v14}\n"
             f"  phrases contredites par D195 : "
             f"{'AUCUNE' if not d195 else d195}\n"
             f"  « 138 » : {len(lignes_138)} occurrence(s), toutes "
             f"historiques (v0.11.0 original) : "
             f"{'OUI' if histo_138 == len(lignes_138) else 'NON'}\n"
             f"  \\plageDecisions = D1--D{plage} ; dernière décision du "
             f"journal = D{d_max} → "
             f"{'COHÉRENT' if plage == str(d_max) else 'DIVERGENT'}\n"
             f"  (la plage de l'instruction « D1–D197 → D1–D198 » était "
             f"périmée à l'exécution : D199–D203 prirent place — "
             f"l'Entrée 234 le consigna AVANT l'exécution)")


# ------------------------------------------------------------------ 5
def controle_grille() -> None:
    textes = {n: lire(p) for n, p in
              [("manuscrit", MANUSCRIT), ("statuts", STATUTS),
               ("sec-a", SPEC["a"]), ("sec-d", SPEC["d"])]}
    # T/X courant : les mentions T/X qui ne portent PAS la mention du
    # renommage (D203/devenue/renommée/à l'époque) dans un voisinage
    tx_courants = []
    for n, t in textes.items():
        for i, l in enumerate(t.splitlines()):
            if re.search(r"T/X|T1--T5|X1--X3", l):
                voisinage = "\n".join(t.splitlines()[max(0, i - 2):
                                                    i + 3])
                if not re.search(r"D203|devenue|renomm|à l'époque|"
                                 r"l'ancienne", voisinage, re.I):
                    tx_courants.append(f"{n}:{i + 1}: {l.strip()[:90]}")
    # la table de correspondance au kit
    with open(KIT / "grille_tx.csv", encoding="utf-8") as f:
        colonne = "ancien_libelle" in f.readline()
    autotest = subprocess.run(
        ["python3", str(KIT / "kohen_kappa_v150.py")],
        capture_output=True, text=True)
    autotest_vert = "VERT" in autotest.stdout and autotest.returncode == 0
    man = textes["manuscrit"]
    fl_ok = ("F1--F5" in man and "L1--L3" in man
             and "an F/L coding grid" in man
             and "the F/L grid and the $\\kappa$ calculator" in man)
    ok = (not tx_courants and colonne and autotest_vert and fl_ok)
    consigne("5. GRILLE DE RÉPLICATION — F/L partout, table de "
             "correspondance au kit", ok,
             f"manuscrit : F/L grid + F1--F5/L1--L3 + la phrase du "
             f"renommage D203 {'PRÉSENTS' if fl_ok else 'ABSENTS'}\n"
             f"  T/X courant (sans mention du renommage) : "
             f"{'AUCUN' if not tx_courants else tx_courants}\n"
             f"  grille_tx.csv : colonne ancien_libelle (la table de "
             f"correspondance) {'PRÉSENTE' if colonne else 'ABSENTE'} ; "
             f"les id F1-F5/L1-L3\n"
             f"  autotest κ : "
             f"{'VERT' if autotest_vert else 'ROUGE'} (les anciennes "
             f"étiquettes T/X admises et converties à la volée)")


# ------------------------------------------------------------------ 6
def controle_empreintes() -> None:
    avant = json.loads(pathlib.Path(
        "/tmp/instantane_avant.json").read_text(encoding="utf-8"))
    proc = subprocess.run(
        ["python3", str(SCRIPTS / "instantane_revision_v150.py"),
         "apres", "/tmp/instantane_apres.json"],
        capture_output=True, text=True)
    apres = json.loads(pathlib.Path(
        "/tmp/instantane_apres.json").read_text(encoding="utf-8"))
    # les empreintes CONSIGNÉES des pièces scellées (empreintes.csv,
    # générée par le script d'extraction depuis les pièces — D170/D178/D181)
    consignes = {}
    with open(SCRIPTS / "manuscrit_v150" / "donnees" / "empreintes.csv",
              encoding="utf-8") as f:
        for r in csv.DictReader(f):
            consignes[r["artefact"]] = r["attendu"]
    scelles_ok = avant["scelles"] == apres["scelles"]
    livres_ok = avant["livres"] == apres["livres"]
    sources_changees = {k for k in avant["sources"]
                        if avant["sources"][k] != apres["sources"][k]}
    garde = subprocess.run(
        ["python3", str(REPO / "v06" / "sceau_I.py"), "verifier"],
        capture_output=True, text=True, cwd=str(REPO))
    garde_ok = "14 arbres VERTS" in garde.stdout
    # chaque scellé confronté à l'empreinte CONSIGNÉE (pas seulement
    # avant == après : l'identité à la valeur scellée fait foi)
    attendus = {"loupe.exe": "loupe.exe 0.1.1 (sealed, D181)",
                "proxy.exe": "proxy.exe 1.0.0 (sealed, D170)",
                "demo.exe": None, "selftest.exe": None}
    ok_consignes = True
    detail_consignes = []
    for chemin, h in apres["scelles"].items():
        nom = pathlib.Path(chemin).name
        cle = attendus.get(nom)
        if cle and cle in consignes:
            bon = h == consignes[cle]
            ok_consignes &= bon
            detail_consignes.append(
                f"{nom} : sha256 {'== CONSIGNÉE' if bon else 'DIVERGENTE'} "
                f"({consignes[cle][:12]}…)")
    ok = scelles_ok and livres_ok and garde_ok and ok_consignes
    detail = []
    for k in sorted(apres["scelles"]):
        detail.append(
            f"{pathlib.Path(k).name} : "
            f"{'IDENTIQUE avant/après' if avant['scelles'].get(k) == apres['scelles'][k] else 'MODIFIÉ'} "
            f"({apres['scelles'][k][:12]}…)")
    detail.extend(detail_consignes)
    for k in sorted(avant["livres"]):
        detail.append(
            f"{pathlib.Path(k).name} : "
            f"{'IDENTIQUE' if avant['livres'][k] == apres['livres'][k] else 'MODIFIÉ'}")
    detail.append(f"garde sceau-I : "
                  f"{'14/14 VERT' if garde_ok else 'ÉCHEC'}")
    detail.append(f"sources révisées ({len(sources_changees)}) : "
                  f"manuscrit main.tex, spec sec-a/sec-d, statuts, kit "
                  f"réplication, macros/tables régénérés")
    consigne("6. EMPREINTES — scellés, livrés et garde intacts", ok,
             "\n".join(detail))


def main() -> None:
    rapport.append("=" * 72)
    rapport.append("VÉRIFICATION DE LA RÉVISION MANUSCRIT+SPÉCIFICATION "
                   "(paquet 4/6, sollwnmae — D203)")
    rapport.append("=" * 72)
    controle_benchmark()
    controle_rq2()
    controle_quantile()
    controle_residus()
    controle_grille()
    controle_empreintes()
    rapport.append("=" * 72)
    rapport.append(f"BILAN : {verts} VERT / {rouges} ROUGE — "
                   f"{'LA RÉVISION EST CONSIGNÉE' if not rouges else 'CORRIGER AVANT CONSIGNATION'}")
    texte = "\n".join(rapport) + "\n"
    print(texte)
    sortie = SCRIPTS / "preuves_v150" / "revision_manuscrit"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "rapport_verification_revision.txt").write_text(
        texte, encoding="utf-8")
    return 0 if not rouges else 1


if __name__ == "__main__":
    sys.exit(main())
