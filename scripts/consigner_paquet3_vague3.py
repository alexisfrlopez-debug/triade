#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_paquet3_vague3.py — LA CONSIGNATION DU PAQUET 3/6 DE LA
VAGUE 3 (l'instruction xboh1kljq — le reclassement des défauts Loupe) :
Entrée 237 au journal de travail, D202 au journal des décisions,
Task 144 au worklog. La discipline append-only tenue : la fin de
chaque journal est VÉRIFIÉE avant l'append, l'unicité des nouvelles
entrées ASSERTÉE (aucune n'existe déjà), aucune ligne antérieure
modifiée."""
from __future__ import annotations

import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"


def append_verifie(chemin: pathlib.Path, ancre_fin: str, bloc: str,
                   marqueur_unique: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    assert marqueur_unique not in texte, \
        f"{marqueur_unique} existe déjà à {chemin.name} — REFUS (append-only)"
    assert texte.rstrip("\n").endswith(ancre_fin.rstrip("\n")), \
        (f"La fin de {chemin.name} n'est pas l'ancre attendue — REFUS. "
         f"Fin réelle : …{texte[-120:]!r}")
    chemin.write_text(texte + bloc, encoding="utf-8")
    relu = chemin.read_text(encoding="utf-8")
    assert relu.count(marqueur_unique) == 1, "l'append n'est pas unique"
    assert relu.endswith(bloc), "l'append n'est pas la dernière section"
    print(f"[OK] {chemin.name} : {marqueur_unique} appéndé "
          f"(+{len(bloc)} caractères)")


# ---------------------------------------------------------------------------
# Entrée 237 — le journal de travail
# ---------------------------------------------------------------------------
ENTREE_237 = """

## Entrée 237 — LE PAQUET 3 DE LA VAGUE 3 EXÉCUTÉ : LE RECLASSEMENT DES DÉFAUTS LOUPE PAR CÔTÉ (l'instruction xboh1kljq menée à terme) : TREIZE classes nommées RECOMPTÉES depuis les entrées 204–217 du journal (chaque citation ASSERTÉE présente au texte de son entrée — le recompte CONTRÔLÉ, jamais déclaré), SEPT côté PIÈCE (le code natif scellé) et SIX côté KIT (le scénario Python, les sondes) ; LES DEUX TAUX PAR LIVRAISON : la métrique PRIMAIRE de RQ1 « code natif écrit par agent » 7/12 (IC Clopper-Pearson 95 % exact [0,2767 ; 0,8483]) et la métrique DE LIVRAISON kit+pièce 11/12 ([0,6152 ; 0,9979]) — chacun recalculé par DEUX MÉTHODES (scipy, ET la bisection maison sur la bêta incomplète régularisée en SCRIPT SÉPARÉ verifier_ic_reclassement_v150.py, l'égalité à 10⁻³ EXIGÉE : écarts constatés 10⁻⁵–10⁻⁶), la RÉSERVE DE NON-INDÉPENDANCE portée aux DEUX taux ; le manuscrit MIS À JOUR (l'abstract EN et FR scindés par côté, la règle §2.3 réécrite aux deux métriques avec les TROIS exclusions nommées [RET-NU nommé au labo avant tout run / T0-PÉRIMÉ sans porte / CORBEILLE-VIDE le coffre, pas la livraison], §3.1 porte les deux taux avec leurs IC exacts et les 13 classes, la Table 4 porte sa colonne Side COMPLÈTE [runs 6 et 7 : piece+kit, un défaut de chaque côté], les Threats et la conclusion alignées) ; la cohérence abstract↔résultats↔conclusion CONTRÔLÉE MÉCANIQUEMENT (coherence_reclassement_v150.py : 26/26 VERT, les chiffres confrontés aux CSV bruts du recompte, les phrases périmées exigées ABSENTES) ; ET LA DETTE DU GÉNÉRATEUR GUÉRIE À LA SOURCE : le parasite « tbp] » (la classe de l'erratum D137 — les guérisons v0.14.0, v0.15.0 et paquet 2 furent ÉPHÉMÈRES, au fichier de sortie, jamais au générateur qui continuait de l'émettre) — extraire_donnees_v150.py émet désormais \\begin{table}[htbp] (cinq lignes), la compilation témoin (bac à sable, le main.pdf livré INTACT) rend 22 pages SANS le parasite ; les tables RÉGÉNÉRÉES ; le rapport de comptage ARCHIVÉ avec son empreinte (rapport.txt sha256 9f6f7e5e0ca81174…, defauts.csv 6f1206d1…, table_categories.csv 02ea8911…, taux.csv 71162b5d…, verification_ic.txt 019da8f2…, coherence.txt 708b27ea…) ; la WIP de la session précédente (le recompte du 22:04, laissé non consigné à l'interruption) RECROPÉE et menée à terme (le rejeu du recompte BIT-IDENTIQUE aux empreintes d'origine) (12/11, la session de la vague 3, paquet 3/6)

**Le recompte.** La méthode de l'instruction tenue à la lettre : « recompte indépendamment depuis les entrées du journal (pas depuis la table existante) » — reclassement_defauts_v150.py lit le journal, localise chaque entrée 204–217, et ASSERT que la citation de chaque classe nommée vit au texte de SON entrée : BASERELOC (204, pièce), ENVELOPPE (205, pièce), CADRE-NÉ (206, pièce), ARGUMENTS-PILE (207, pièce), SESSION-CHARGEUR (208, kit), SAUVEGARDE-ATTENDU (209, kit) et HINSTANCE-PEB (209, pièce), EAX-SANS-SIGNE (210, kit) et D54-QUATRIÈME (210, pièce), SONDE-PYTHON (213, kit), OFT-QWORD (214, pièce), FREE-SANS-TYPE (216, kit — « LE DÉFAUT DU KIT, PAS DE LA PIÈCE », dit l'entrée), SONDE-EXE (217, kit) : TREIZE classes, les runs 6 et 7 en portant DEUX chacune (un de chaque côté). Le résultat recoupe la table existante rangée à rangée — mais il est NÉ de la source (le journal), pas de la table.

**Les deux taux.** Par LIVRAISON (le run, pas le défaut — les runs 6/7 comptent UNE fois par taux) : la métrique PRIMAIRE « code natif écrit par agent » — les runs où un défaut DE LA PIÈCE échappa : 7/12 (runs 1–4, 6, 7, 9) ; la métrique de LIVRAISON — les runs où un défaut QUELCONQUE échappa : 11/12 (tout run sauf le douzième, vert de bout en bout). Les intervalles Clopper-Pearson 95 % EXACTS calculés par scipy.stats.beta.ppf puis RECALCULÉS par la bisection maison (continuation de Lentz, Numerical Recipes § 6.4) dans un script SÉPARÉ sans aucun appel scipy : [0,2767 ; 0,8483] et [0,6152 ; 0,9979] — les écarts entre méthodes 3,03·10⁻⁵ au pire, l'exigence de 10⁻³ tenue avec deux ordres de grandeur de marge. La réserve : douze livraisons SÉQUENTIELLES d'un seul binôme développeur-agent — des résumés descriptifs, JAMAIS une inférence sur une population.

**La dette du générateur (la leçon).** Le parasite « tbp] » (un [htbp] amputé de son crochet ouvrant par une retouche ancienne — la classe de l'erratum D137, nommée page 31 du PDF v0.6.0) vivait ENCORE au générateur : les sessions v0.14.0, v0.15.0 et le paquet 2 guérirent chacune le FICHIER DE SORTIE (le sed éphémère avant la compilation) — et le générateur continua de l'émettre (constaté ce jour : extraire_donnees_v100/v110/v130/v140/v150 portent TOUS le parasite ; le tables_generees.tex du paquet 2 fut guéri en sortie, pas en source). La guérison définitive vit À LA SOURCE : les cinq lignes du générateur portent [htbp], la régénération produit un fichier propre, la compilation témoin le confirme (zéro « tbp] » au PDF). La règle : guérir la sortie sans guérir la source, c'est différer la dette — pas la solder.

**Frontières.** Aucun artefact scellé touché (loupe.exe c1115105…, proxy.exe 446279f3…, demo.exe df8f2e50… — sha256 recoupés AVANT et APRÈS, INTACTS) ; le main.pdf de l'édition LIVRÉE INTACT (la compilation témoin vécut au bac à sable /tmp — le prochain build d'édition appartiendra à la révision manuscrit+spécification, paquet 4) ; le garde sceau-I 14/14 VERT avant et après ; les zips de l'édition v0.15.0 INTACTS (le reclassement vit aux SOURCES, la prochaine édition l'embarquera) ; aucun chiffre fabriqué — tout nombre est LU d'une pièce (taux.csv, defauts.csv) ; les consignations antérieures non réécrites (append-only).
"""

# ---------------------------------------------------------------------------
# D202 — le journal des décisions
# ---------------------------------------------------------------------------
D202 = """

## D202 — LE RECLASSEMENT PAR CÔTÉ CONSACRÉ : DEUX métriques là où la v0.15.0 en portait UNE — la PRIMAIRE de RQ1 compte le CODE NATIF ÉCRIT PAR L'AGENT SEUL (7/12, IC Clopper-Pearson 95 % exact [0,2767 ; 0,8483] : les runs où un défaut de la PIÈCE scellée échappa aux contrôles), la MÉTRIQUE DE LIVRAISON compte l'ENSEMBLE kit+pièce (11/12, [0,6152 ; 0,9979] : les runs où un défaut QUELCONQUE échappa — ce que le développeur reçut) — chacun des deux intervalles recalculé par DEUX méthodes indépendantes (scipy ET la bisection maison en script séparé, l'égalité à 10⁻³ exigée et tenue à 10⁻⁵) et la RÉSERVE DE NON-INDÉPENDANCE portée aux DEUX (douze livraisons séquentielles d'un binôme unique : descriptif, jamais inférentiel) ; LES TREIZE CLASSES NOMMÉES RECLASSÉES (SEPT pièce, SIX kit — les six côté kit ne touchent JAMAIS le code natif scellé : elles vivent dans le scénario Python et les sondes) avec les TROIS EXCLUSIONS NOMMÉES de la règle §2.3 ([RET-NU] nommé au laboratoire avant tout run — jamais échappé ; [T0-PÉRIMÉ] un résidu de bannière sans porte ; [CORBEILLE-VIDE] un défaut du coffre du labo, d'aucun des deux côtés livrés) ; ET LA RÈGLE DU GÉNÉRATEUR QUI GUÉRIT : guérir le FICHIER DE SORTIE laisse la dette au générateur — les guérisons éphémères de la v0.14.0, de la v0.15.0 et du paquet 2 le prouvèrent (le parasite « tbp] » réémis à chaque régénération, la classe de l'erratum D137) — la guérison vit à la SOURCE (extraire_donnees_v150.py porte désormais [htbp], la compilation témoin 22 pages sans parasite)

**Le contexte.** L'instruction xboh1kljq (la vague 3) demande le reclassement des défauts nommés des runs Loupe en deux catégories, deux taux d'échappement à IC exacts, et la mise à jour de l'abstract, de la règle de comptage §2.3, de §3.1, de la Table 4 et des Threats. Le recompte depuis les entrées du journal (les citations assertées) recoupe la table existante et fonde les deux métriques ; la cohérence abstract↔résultats↔conclusion est contrôlée mécaniquement (26/26 VERT).

**Frontières.** Aucun artefact scellé touché (sha256 recoupés avant/après, le garde 14/14) ; le PDF de l'édition livrée INTACT (la compilation témoin vécut au bac à sable) ; les consignations antérieures non réécrites (append-only).
"""

# ---------------------------------------------------------------------------
# Task 144 — le worklog
# ---------------------------------------------------------------------------
TASK_144 = """

Task ID: 144
Agent: Z.ai (agent principal)
Task: LE PAQUET 3/6 DE LA VAGUE 3 (l'instruction xboh1kljq) — le
reclassement des défauts Loupe par côté : 13 classes recomptées, les
deux taux à IC exacts, le manuscrit et la Table 4 mis à jour, la dette
du générateur « tbp] » guérie à la source (D202, Entrée 237).

Work Log:
- LE RECOMPTE CONTRÔLÉ : 13 classes nommées depuis les entrées
  204-217 (citations ASSERTÉES au texte) — 7 PIÈCE, 6 KIT ; runs 6/7
  deux classes chacun ; rejeu BIT-IDENTIQUE (la WIP 22:04 de la
  session précédente recoupée puis menée à terme).
- LES DEUX TAUX : PRIMAIRE RQ1 « code natif écrit par agent » 7/12
  IC95 [0,2767 ; 0,8483] ; LIVRAISON kit+pièce 11/12 [0,6152 ;
  0,9979] — scipy ET bisection maison en SCRIPT SÉPARÉ (écarts
  10⁻⁵-10⁻⁶ < 10⁻³ exigé), réserve de non-indépendance aux DEUX.
- LE MANUSCRIT : abstract EN+FR scindés par côté, §2.3 aux deux
  métriques + TROIS exclusions nommées ([RET-NU]/[T0-PÉRIMÉ]/
  [CORBEILLE-VIDE]), §3.1 les deux taux + 13 classes, Table 4
  colonne Side COMPLÈTE (runs 6/7 : piece+kit), Threats et conclusion
  alignées ; COHÉRENCE 26/26 VERT (chiffres confrontés aux CSV
  bruts).
- LA DETTE DU GÉNÉRATEUR GUÉRIE À LA SOURCE : le parasite « tbp] »
  (classe D137) émis par TOUS les générateurs v100→v150 — les
  guérisons passées furent éphémères (au fichier de sortie) ;
  extraire_donnees_v150.py porte désormais [htbp] (5 lignes),
  compilation témoin 22 pages SANS parasite (bac à sable, le main.pdf
  livré INTACT).
- LES PIÈCES : preuves_v150/reclassement/ (rapport.txt 9f6f7e5e…,
  defauts.csv, table_categories.csv, taux.csv, verification_ic.txt,
  coherence.txt — empreintes consignées à l'Entrée 237).
- Frontières : pièces scellées INTACTES (loupe.exe c1115105…,
  proxy.exe 446279f3…, demo.exe df8f2e50… recoupées avant/après),
  garde sceau-I 14/14 avant/après, zips de l'édition INTACTS,
  append-only, aucun chiffre fabriqué.
- SUITE : le paquet 4/6 — la révision manuscrit+spécification
  (sollwnmae).
"""

append_verifie(
    JOURNAL,
    "les consignations antérieures non réécrites (append-only).\n",
    ENTREE_237,
    "## Entrée 237",
)
append_verifie(
    DECISIONS,
    "les consignations antérieures non réécrites (append-only).\n",
    D202,
    "## D202",
)
# worklog : l'ancre est la fin de la SUITE du Task 143
append_verifie(
    WORKLOG,
    "- SUITE : le paquet 3/6 — le reclassement des défauts Loupe\n"
    "  (xboh1kljq).",
    TASK_144,
    "Task ID: 144",
)
print("\n[CONSIGNÉ] Entrée 237 + D202 + Task 144 — le paquet 3/6 de la "
      "vague 3.")
