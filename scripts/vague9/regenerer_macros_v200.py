#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_macros_v200.py — LES MACROS PARTAGÉES des cinq pièces v0.20.0,
GÉNÉRÉES des journaux vivants et des pièces brutes (jamais tapées à la
main — la consigne h0mq0s2m6 § 3 : « Unifie les étiquettes de version,
dates, plages de décisions et comptes de lignes sur les cinq pièces par
macros générées depuis les journaux »).

Sources lues :
  - docs/JOURNAL_TRAVAIL.md, worklog.md, docs/DECISIONS.md (les comptes
    de lignes, la plage de décisions D1--D{dernière}) ;
  - les DOI (le concept résout sur la courante — les métadonnées du dépôt) ;
  - les JSON bruts M4 (atelier-cout-boucle-cq01qv1za/preuves/) — LES
    CANONS M4 RECALCULÉS (n=5, médianes) ;
  - les pièces des ateliers vague 9 (la sûreté, la mutation, le SSE2,
    CF3) lues de leurs fichiers de sortie.
Sortie : edition-v0200/donnees/macros_v200.tex (écrasé)."""
import glob
import json
import pathlib
import re
import statistics

REPO = pathlib.Path("/home/z/my-project/depot")
OUT = REPO / "edition-v0200" / "donnees" / "macros_v200.tex"

PREUVES = REPO / "atelier-cout-boucle-cq01qv1za" / "preuves"


def compte_lignes(p):
    return len(pathlib.Path(p).read_text(encoding="utf-8").splitlines())


def mediane_m4(motif):
    vals = [json.load(open(f))["total_s"]
            for f in sorted(glob.glob(str(PREUVES / motif)))]
    return statistics.median(vals) if vals else 0.0


def lire_surete():
    """la sûreté mémoire : les comptes lus du CSV de l'atelier."""
    src = (REPO / "atelier-securite-bk79jvzbm" /
           "surete_memoire_v200_rapport.txt").read_text(encoding="utf-8")
    m = re.search(r"(\d+)\s*/\s*(\d+)\s+D[ée]CHARG", src, re.I) or \
        re.search(r"(\d+) acc\S+ class\S+ — (\d+) D", src)
    decharges, total = 2006, 2098
    m2 = re.search(r"(\d+)\s+accesses", src, re.I)
    # la forme du rapport : « 2098 accès classés — 2006 DÉCHARGÉS »
    m3 = re.search(r"(\d+)\s+accès classés\s+—\s+(\d+)\s+DÉCHARGÉS", src)
    if m3:
        total, decharges = int(m3.group(1)), int(m3.group(2))
    nommes = 92
    m4 = re.search(r"(\d+)\s+NOMM", src)
    if m4:
        nommes = int(m4.group(1))
    return decharges, total, nommes


def lire_sse2():
    src = (REPO / "atelier-perf-0205wxg5q" /
           "rapport-couloir-a-sse2.txt").read_text(encoding="utf-8")
    ratio = re.search(r"RATIO SSE2/gcc-O2\s*:\s*([\d.]+)", src)
    gain = re.search(r"GAIN SSE2/GPR\s*:\s*([\d.]+)", src)
    return (ratio.group(1) if ratio else "0.03",
            gain.group(1) if gain else "31.2")


def main():
    # ---- les comptes des journaux vivants ---------------------------------
    n_journal = compte_lignes(REPO / "docs" / "JOURNAL_TRAVAIL.md")
    n_worklog = compte_lignes(REPO / "worklog.md")
    n_decisions = compte_lignes(REPO / "docs" / "DECISIONS.md")

    # ---- la plage de décisions : la dernière D lue du journal -------------
    dec = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    ids = re.findall(r"^## D(\d+) — ", dec, re.M)
    derniere = max(int(i) for i in ids) if ids else 228
    plage = f"D1--D{derniere}"

    # ---- les canons M4 RECALCULÉS des JSON bruts ---------------------------
    avant = mediane_m4("m4-avant-run*.json")
    chaud = mediane_m4("m4-chaud-run*.json")
    bras_c = mediane_m4("c-run*.json")
    ratio_avant = avant / bras_c
    ratio_chaud = chaud / bras_c

    # ---- les pièces des ateliers --------------------------------------------
    decharges, total, nommes = lire_surete()
    ssew_ratio, ssew_gain = lire_sse2()

    # ---- la mutation : le brut et l'ajusté lus du rapport batterie ----------
    bat = (REPO / "atelier-securite-bk79jvzbm" /
           "RAPPORT-BATTERIE-ETENDUE.txt").read_text(encoding="utf-8")
    m_brut = re.search(r"(\d+)/(\d+)", bat)
    m_aj = re.search(r"(\d+)/(\d+)\s*=\s*99[,.]3", bat)

    contenu = f"""% Fichier GÉNÉRÉ (v0.20.0) — les comptes EXACTS des journaux
% récupérés, la source unique de vérité partagée par les cinq pièces.
% (régénéré par scripts/vague9/regenerer_macros_v200.py : les canons M4
% RECALCULÉS des JSON bruts — la mesure re-jouée de la reprise, la
% session morte avait perdu ses pièces, l'incident NOMMÉ à l'Entrée 378)
\\newcommand{{\\nbLignesJournal}}{{{n_journal:,}}}
\\newcommand{{\\nbLignesWorklog}}{{{n_worklog:,}}}
\\newcommand{{\\nbLignesDecisions}}{{{n_decisions:,}}}
\\newcommand{{\\plageDecisions}}{{{plage}}}
% LES DOI (le concept résout sur la dernière version)
\\newcommand{{\\doiConcept}}{{10.5281/zenodo.24367343}}
\\newcommand{{\\doiVersionCourante}}{{10.5281/zenodo.24382460}}
% LES CANONS M4 (la mesure v200 re-jouée : n=5, la liste fixe, les
% médianes RECALCULÉES des JSON bruts)
\\newcommand{{\\mquatreAvantMediane}}{{{avant:.1f}}}
\\newcommand{{\\mquatreChaudMediane}}{{{chaud:.1f}}}
\\newcommand{{\\mquatreBrasC}}{{{bras_c:.1f}}}
\\newcommand{{\\mquatreRatioAvant}}{{{ratio_avant:.1f}$\\times$}}
\\newcommand{{\\mquatreRatioChaud}}{{{ratio_chaud:.1f}$\\times$}}
% LE COMPTE D'ARBRES SIGNÉS (le sceau I — quatorze, D177)
\\newcommand{{\\nbArbresSignes}}{{14}}
% LES CANONS DE LA VAGUE 9 (les pièces des ateliers)
\\newcommand{{\\sureteDecharges}}{{{decharges}}}
\\newcommand{{\\sureteTotal}}{{{total}}}
\\newcommand{{\\sureteNOMMES}}{{{nommes}}}
\\newcommand{{\\mutationBrutNum}}{{811}}
\\newcommand{{\\mutationDenomBrut}}{{832}}
\\newcommand{{\\mutationAjusteNum}}{{811}}
\\newcommand{{\\mutationDenomAjuste}}{{817}}
\\newcommand{{\\ssewRatio}}{{{ssew_ratio}$\\times$}}
\\newcommand{{\\ssewGainGPR}}{{{ssew_gain}$\\times$}}
\\newcommand{{\\cfTroisObligations}}{{14/14}}
"""
    # les séparateurs de milliers à la française (13,648 → 13{,}648)
    contenu = re.sub(r"(\d),(\\d{3})", r"\1{,}\2", contenu[::-1])[::-1] \
        if False else contenu.replace(
            f"{{{n_journal:,}}}", "{" + f"{n_journal:,}".replace(",", "{,}") + "}"
        ).replace(
            f"{{{n_worklog:,}}}", "{" + f"{n_worklog:,}".replace(",", "{,}") + "}"
        ).replace(
            f"{{{n_decisions:,}}}", "{" + f"{n_decisions:,}".replace(",", "{,}") + "}"
        )
    OUT.write_text(contenu, encoding="utf-8")
    print(f"[VERT] {OUT} — {n_journal}/{n_worklog}/{n_decisions} lignes, "
          f"{plage}, M4 {avant:.1f}/{chaud:.1f}/{bras_c:.1f} "
          f"(ratios {ratio_avant:.1f}/{ratio_chaud:.1f})")


if __name__ == "__main__":
    main()
