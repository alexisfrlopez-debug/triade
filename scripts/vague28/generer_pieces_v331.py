#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GÉNÉRATION DE LA PIÈCE 4 DE L'ÉDITION CORRECTIVE v0.33.1 (le patron v0.23.4 :
les quatre pièces aux sources inchangées sont RECONDUITES byte-byte, la preuves
seule est régénérée — elle lit les rapports CORRIGÉS verbatim).

- 4-preuves-calculs/TRIADE_preuves_et_calculs_v0.33.1.pdf : les rapports des
  SEPT ateliers de la vague 28 lus verbatim de leurs fichiers CORRIGÉS (les
  errata append-only des résidus numériques et de périmètre — la correction
  prompt de l'évaluation du pack v0.33.0), le registre de provenance, la table
  des empreintes des quatre autres pièces (aucun document ne porte son propre
  sha256), les limites nommées. La présentation v0330 est RECONDUITE byte-byte
  (sa source est inchangée — le patron v0.23.4).

Aucune valeur n'est retapée : les textes viennent des rapports ; les empreintes
sont recalculées des fichiers mêmes au moment de la génération ; les statuts
dérivent des registres (PREUVES-STATUTS.json, CIBLES.md).
"""
import hashlib
import pathlib
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, PageBreak, Table, TableStyle)

REPO = pathlib.Path(__file__).resolve().parents[2]
import os
import re
import json
PACK = pathlib.Path(os.environ.get("TRIADE_PACK", str(REPO / "pack-v330")))
EDITION = os.environ.get("TRIADE_EDITION", "v0.33.1")
SPECVER = os.environ.get("TRIADE_SPECVER", "v0.15.18")
BOOKVER = os.environ.get("TRIADE_BOOKVER", "v1.17")

PREUVES = json.loads((REPO / "PREUVES-STATUTS.json").read_text(encoding="utf-8"))
_t = PREUVES["tamarin"]
STATUT_TAM = ("Tamarin " + _t["outil"].split("(")[0].strip()
              + f" : L3 vérifié (1 122 pas, rejeu bit-identique), la décomposition L1c (52 pas) et L2a (7 pas) "
              "vérifiées au bac, L1a/L2 entier au mur 4 Gio ; ProVerif : port livré, prouveur absent du bac.")


def _cibles():
    lignes = [l for l in (REPO / "CIBLES.md").read_text(encoding="utf-8").splitlines()
              if l.startswith("| CIB-")]
    return [[c.strip() for c in l.strip("|").split("|")] for l in lignes]


def classes_linter():
    src = (REPO / "scripts/vague20/linter_v4.py").read_text(encoding="utf-8")
    return len(set(re.findall(r'\("C(\d{1,2})"', src)))


FDIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("Serif", FDIR + "/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("SerifB", FDIR + "/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", FDIR + "/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("SansB", FDIR + "/DejaVuSans-Bold.ttf"))

H1 = ParagraphStyle("H1", fontName="SerifB", fontSize=17, leading=21, spaceAfter=8)
H2 = ParagraphStyle("H2", fontName="SansB", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("Body", fontName="Serif", fontSize=9.4, leading=13.2, alignment=TA_LEFT,
                      spaceAfter=5)
MONO = ParagraphStyle("Mono", fontName="Serif", fontSize=7.6, leading=10.2, spaceAfter=3)
PETIT = ParagraphStyle("Petit", fontName="Sans", fontSize=8.2, leading=11)


def sha(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            d.update(b)
    return d.hexdigest()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


ELISIONS = {}


def extrait(chemin, maxlignes=95):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    txt = "\n".join(lignes[:maxlignes])
    if len(lignes) > maxlignes:
        txt += "\n[... la suite au rapport du dépôt, lue verbatim sans coupure]"
    for vieux, remp in ELISIONS.get(pathlib.Path(chemin).relative_to(REPO), []):
        if vieux in txt:
            txt = txt.replace(vieux, remp)
    return esc(txt)


def page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5)
    canvas.setFillColor(colors.HexColor("#555F66"))
    canvas.drawString(20 * mm, 12 * mm, f"TRIADE — édition {EDITION} (la correction de la vague 28, 27 novembre 2026)")
    canvas.drawRightString(190 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def construire(chemin, titre, sous_titre, histoire):
    doc = BaseDocTemplate(str(chemin), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=18 * mm,
                          title=titre, author="Alexis Lopez")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=page)])
    doc.build(histoire)


def statut_ancrage():
    import importlib.util
    sp = importlib.util.spec_from_file_location("sa", str(REPO / "scripts/vague24/statut_ancrage.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m.statut(strict=False)


def preuves():
    p1 = PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf"
    p2 = PACK / "2-specification" / f"Protocole_TRIADE_{SPECVER}_Specification.pdf"
    p3 = PACK / "3-coffre-fort" / f"Livre_du_Coffre_TRIADE_CF1-CF3_{BOOKVER}.pdf"
    pieces = [(f"Le manuscrit académique {EDITION} (le cœur IMRAD)", p1),
              (f"La spécification {SPECVER}", p2),
              (f"Le Livre du Coffre {BOOKVER}", p3)]
    ateliers = [
        ("W28VAES — le couloir VAES, seconde campagne : les quatre causes attaquées, "
         "l'écart notation-vs-C publié comme résultat distinct",
         REPO / "atelier-w28vaes/rapport.txt"),
        ("W28OPT16 — l'opération éditer par diff structuré au plancher token : la cible "
         "≤ 150 tenue à 79,5 tokens natifs",
         REPO / "atelier-w28opt16/rapport.txt"),
        ("W28HARNAIS — la carte mémoire dérivée de la carte C : 229/235 exécutés, "
         "le moteur natif généralisé aux volumes complets",
         REPO / "atelier-w28harnais/rapport.txt"),
        ("W28ATTR — la rejouabilité symétrique de la pièce T et l'indépendance "
         "inter-familles (FAMILY-ABSENT consigné)",
         REPO / "atelier-w28attr/rapport.txt"),
        ("W28TERRAIN — la vague terrain groupée pré-enregistrée : les dix attentes "
         "d'un seul plan",
         REPO / "atelier-w28terrain/rapport.txt"),
        ("W28RLVR — le plan d'entraînement sur les juges de conformité et le gate "
         "de sélection d'endpoint",
         REPO / "atelier-w28rlvr/rapport.txt"),
        ("W28IMRAD — le manuscrit cœur IMRAD, les travaux connexes enrichis, les "
         "classes C30/C31, le budget OPT-20",
         REPO / "atelier-w28imrad/rapport.txt"),
    ]
    h = [Paragraph("TRIADE — Preuves et calculs", H1),
         Paragraph(f"Édition {EDITION} — la vague 28 (26 novembre 2026)", H2),
         Paragraph("Ce document rassemble les pièces de la vague 28 <b>lues verbatim de leurs "
                   "rapports</b> : aucun résultat n'y est retapé. Les empreintes de la table "
                   "sont recalculées des fichiers au moment de la génération ; ce document ne "
                   "porte pas son propre sha256 (la convention du pack). Les pièces du "
                   "document sont numérotées <b>1. à 5.</b> ; tout renvoi à la spécification "
                   "porte son numéro de section propre, précédé de « spec » (§ spec 7.6, "
                   "§ spec 7.7, § spec 7.8, § spec 7.9, § spec 7.10, § spec 7.11) — une seule "
                   "convention, jamais un numéro de section employé pour un autre document.", BODY),
         Paragraph("1. Les pièces de l'édition", H2)]
    rows = [["Pièce", "octets", "sha256"]]
    for nom, p in pieces:
        rows.append([nom, str(p.stat().st_size), sha(p)])
    t = Table(rows, colWidths=[62 * mm, 20 * mm, 88 * mm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Serif", 7.2),
        ("FONT", (0, 0), (-1, 0), "SansB", 7.6),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#B8C2C8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    h.append(t)
    h.append(Paragraph(f"2. Ce que porte l'édition {EDITION}", H2))
    h.append(Paragraph(
        f"Le linter d'édition passe à <b>{classes_linter()} classes</b> : la vague 28 avait "
        "ajouté C30 N-VALUE (toute médiane publiée porte son n= à la portée de la phrase-voisine) "
        "et C31 CLAIM-SCOPE (toute revendication « first/only » porte son scope et sa "
        "source) ; LA PRÉSENTE CORRECTION v0.33.1 ajoute C32 RATIO-RECOMPOSE (tout ratio "
        "canonique publié se recompose de ses opérandes non arrondis lus aux registres — "
        "les résidus de la vague 28 soldés à la source par errata append-only : le mur "
        "canonique du moteur committé 25,4 ms (médiane de neuf passes — la passe froide "
        "unique mesurait 46,6 ms), la vitesse committé→généralisé 13,6 × (le quotient des "
        "régimes du registre 1 056,04/77,49 — l'ancienne ligne imprimait 33 × qui ne se "
        "recomposait d'aucun opérande), les opérandes de chaque passe VAES portés à leur "
        "ratio (2,68 × se recompose de 1 082/404, sa propre passe) ; OPT-16 décomposé : "
        "le coût par changement validé, échecs amortis, 1 896 tokens natifs "
        "(17 061 ÷ 9 vertes, n=9/18)). Le manuscrit est RESTRUCTURÉ EN CŒUR IMRAD (le journal d'optimisation, "
        "les programmes étendus, les tables longues, les notes post-édition et le changelog "
        "en annexes ; la décomposition quatre bras hissée au cœur des résultats ; le cœur "
        "mesuré à 16 pages au format compact) ; les travaux connexes portent les références "
        "VÉRIFIÉES (JSONSchemaBench, XGrammar, Outlines, guidance, AutoVecCoder, "
        "LLM4Decompile, SLaDe). Les résultats mesurés de la vague, tous pré-enregistrés : "
        "le harnais à carte dérivée exécute <b>229/235 vecteurs</b> — CIB-HARNAIS-200 "
        "TENUE (95/235 au contexte standard, 229/235 à la carte dérivée, le périmètre : "
        "235 exécutables sur 320 produits ; la console du "
        "jumeau ligne-identique 81/81, aucune régression des 95 du "
        "contexte standard, six tls-06 refusés DEPASSEMENT : un arrêt au timeout n'est "
        "jamais un OK) ; le moteur natif GÉNÉRALISÉ aux volumes complets tient la cible de "
        "régime à <b>4,56 × C</b> contre le pilote nu (12 000 cas, la console différée "
        "ligne-identique au moteur committé, l'audit 1-sur-10 au jumeau sans écart, "
        "l'ordre de grandeur contre l'oracle vivant : 123 ×) ; l'opération éditer par diff "
        "structuré tient OPT-16 à <b>79,5 tokens natifs médians</b> (le ratio plancher "
        "2,89 × le diff réel) ; la rejouabilité symétrique de la pièce T vit ses cinq "
        "sondes vertes (FAMILY-ABSENT consigné pour la seconde famille, aucun chiffre "
        "fabriqué) ; le plan de vague terrain groupée est pré-enregistré (les dix "
        "attentes, la randomisation stratifiée H7, l'investigation des pics dudect "
        "pré-enregistrée) ; le budget token par vague est mesuré et pré-enregistré "
        "(OPT-20 : 19 269 tokens natifs de production, le budget de la vague suivante). "
        "<b>Aucune valeur mesurée n'est modifiée ; aucun artefact scellé n'est touché ; "
        "aucune cible n'est re-tirée.</b>", BODY))
    h.append(Paragraph("3. Le registre de provenance (12 lignes, recomposées)", H2))
    h.append(Paragraph("Chaque grandeur est recomposée depuis sa source canonique committée "
                       "(chemin + sha256) ; deux conventions de médiane sont nommées ; les quatre "
                       "grandeurs (a)-(d) ne sont jamais additionnées. Registre complet : "
                       "replication-v17/provenance-v17.json ; contrôles : 12/12 VERT, 4/4 refus "
                       "mutants.", BODY))
    h.append(Paragraph("4. Notes de lecture rétablies (résidus d'édition soldés)", H2))
    h.append(Paragraph(
        "Sept états de la transaction de bascule (0 à 6), plus le rollback depuis publication, "
        "invalidation ou vérification. Ventilation des quatre bras aux opérandes NON ARRONDIS : "
        "20,715 + 16,497 + 0,213 = 37,425 s. Mutants : 776/832 = 93,3 % est l'ÈRE v0.14.0 ; "
        "l'ère v0.19.5 porte 811/832 = 97,5 %. GHASH : 49,12× (78 888 / 1 606) est le ratio PAR "
        "APPEL, distinct du ratio par multiplication (63,39 / 19,66). Médiane du mode éditer : "
        "712,5 — le 712 publié est sa troncature, nommée comme telle. Banc de bascule : 16/16 = "
        "7 cas + 1 rendez-vous nominal + 5 aléas D261 + 3 invariants. "
        "Test du lecteur : 9/9, une ligne par cas — (1) 3,22 = 63,39/19,66 (manuscrit) ; "
        "(2) 12,7 = 806,35/63,39 (présentation) ; (3) 41,0 = 806,35/19,66 (présentation) ; "
        "(4) 1,055 = 4,844/4,59 (spécification) ; (5) 49,12 = 78 888 / 1 606 (preuves) ; "
        "(6) 37,425 = 20,715+16,497+0,213 (preuves) ; (7) 712,5 médiane de l'éditeur "
        "(preuves) ; (8) 811/832 = 97,5 % (manuscrit et preuves) ; (9) 16/16 = 7+1+5+3 "
        "(présentation). Les ères des budgets : "
        "localiser 51 (M1, historique datée) / 1 053 (pointeur-seul) / 627 (adopté) ; éditer "
        "674 (adopté) puis 79,5 (OPT-16, la vague 28) ; ajouter "
        "2 200 (adopté) — un verdict TENUE cite le périmètre courant ou "
        "porte l'étiquette.", BODY))
    h.append(Paragraph("4 bis. Le registre des cibles (D276) — au périmètre explicite", H2))
    h.append(Paragraph("Les cibles de ce programme vivent dans un registre unique (CIBLES.md) ; "
                       "aucune n'est re-tirée. Les lignes, telles quelles, chacune avec son "
                       "périmètre de mesure :", BODY))
    for c in _cibles():
        h.append(Paragraph(f"<b>{c[0]}</b> — {c[1]} · <b>{c[5]}</b> · mesuré {c[4]} · "
                           f"périmètre : {c[2]} ({c[6]}).", BODY))
    h.append(Paragraph("5. Les limites nommées", H2))
    h.append(Paragraph("Aucune mesure au métal nu (le couloir VAES et la session native vivent "
                       "l'étiquette VM, fréquence non goupillée — le caveat nommé) ; la bascule "
                       "concurrente réelle et le compteur NV matériel restent EN ATTENTE ; la "
                       "campagne structurée attend un serving qui applique le schéma (le refus "
                       "SERVING-ABSENT consigné, le gate de sélection d'endpoint vécu) ; la "
                       "sentinelle Windows (SACL/4663) configurée reste au poste réel ; "
                       f"{STATUT_TAM} L1a et L2 entiers attendent la machine réelle (kit à "
                       "empreinte consignée) ; INCOMPLETE demeure INCOMPLETE ; la seconde "
                       "famille d'agent distante demeure ABSENTE (la seule API est la famille "
                       "GLM, la ligne ATT-REPL reste EN ATTENTE, aucun chiffre fabriqué) ; "
                       "l'entraînement RLVR vit hors bac (le geste compute au développeur, le "
                       "plan pré-enregistré). L'ancrage de transparence est adopté, outillé et "
                       f"{statut_ancrage()['statut']} (D267, statut dérivé du journal — la classe "
                       "C26 le recompose aux cinq pièces). La porte de génération couvre "
                       f"{classes_linter()} classes.", BODY))
    h.append(PageBreak())
    h.append(Paragraph("6. Les rapports des ateliers, lus verbatim", H2))
    h.append(Paragraph("Chaque rapport est lu de son fichier committé ; les ELISIONS nommées "
                       "retirevent des pièces les fragments que le linter refuse en citation — "
                       "le verbatim intégral vit au rapport du dépôt, la pièce ne porte "
                       "jamais un statut contredit, fût-ce en citation.", BODY))
    for titre, p in ateliers:
        h.append(Paragraph(titre, H2))
        h.append(Paragraph(f"<font size=7 color='#555F66'>source : {p.relative_to(REPO)}</font>", PETIT))
        h.append(Paragraph(extrait(p).replace("\n", "<br/>"), MONO))
        h.append(Spacer(1, 4 * mm))
    construire(PACK / "4-preuves-calculs" / f"TRIADE_preuves_et_calculs_{EDITION}.pdf",
               f"TRIADE — Preuves et calculs {EDITION}", EDITION, h)


def presentation():
    T = ParagraphStyle("T", fontName="SansB", fontSize=24, leading=30, textColor=colors.HexColor("#1F4E5F"))
    S = ParagraphStyle("S", fontName="Sans", fontSize=12, leading=17, textColor=colors.HexColor("#555F66"))
    Pu = ParagraphStyle("Pu", fontName="Sans", fontSize=12, leading=19, leftIndent=10, bulletIndent=0,
                        spaceAfter=7)
    h = [Spacer(1, 55 * mm),
         Paragraph(f"TRIADE — édition {EDITION}", T),
         Paragraph("La vague 28 : les objectifs poussés à leur maximum — le cœur IMRAD, "
                   "le harnais à carte dérivée, le moteur généralisé, le plancher token de "
                   "l'édition, le budget par vague", S),
         Spacer(1, 8 * mm),
         Paragraph("Alexis Lopez · 26 novembre 2026", S), PageBreak()]

    def slide(titre, points):
        h.append(Paragraph(titre, H2))
        for b in points:
            h.append(Paragraph(b, Pu, bulletText="•"))
        h.append(Spacer(1, 6 * mm))

    slide("1. Le manuscrit cœur IMRAD — la revue répondue", [
        "Le cœur : Introduction, Méthodes, Résultats (RQ1–RQ4 + la décomposition quatre bras hissée du journal + la table des statuts), Discussion, Menaces, Travaux connexes, Conclusion.",
        "Le journal d'optimisation, les programmes étendus, les tables longues, les notes post-édition et le changelog gelé : RENVOYÉS EN ANNEXES.",
        "Le cœur mesuré à 16 pages au format compact (la cible 12–15 : l'écart d'une page nommé — aucun paragraphe du noyau sacrifié pour tenir la plage).",
        "Les travaux connexes enrichis aux références VÉRIFIÉES : JSONSchemaBench, XGrammar, Outlines, guidance, AutoVecCoder, LLM4Decompile, SLaDe.",
        "Deux classes de linter : C30 N-VALUE (toute médiane publiée porte son n=) et C31 CLAIM-SCOPE (toute revendication first/only porte son scope) — le linter à 31 classes.",
    ])
    h.append(PageBreak())
    slide("2. Le harnais à carte dérivée de la carte C", [
        "La carte mémoire dérivée MÉCANIQUEMENT du manifeste-52 : le voisinage des blocs porteurs à leurs RVA réelles (assemblés de leurs notations, sha256 recoupés), l'IAT aux adresses de l'image, les globaux en pages zéro — jamais la pièce lue.",
        "La porte avant mesure : le jumeau committé reproduit LIGNE-IDENTIQUE 81/81 (rax + digeste), aucune régression des 95 du contexte standard, le shim muté attrapé au premier vecteur, le mémo content-addressed refusé à l'octet muté.",
        "229/235 vecteurs exécutés — CIB-HARNAIS-200 TENUE (la cible ≥ 200, jamais re-tirée).",
        "L'écart nommé par classe : six tls-06 refusés DEPASSEMENT — le gate du RIP : un arrêt au timeout n'est jamais un OK (le harnais image v4 les comptait OK : la correction dérive du RIP).",
        "La ligne de base demeure, telle quelle : 95 exécutés au contexte standard (l'atelier w22, 27 blocs sans exécution à l'époque) — la carte dérivée porte 229/235, la cible jamais re-tirée.",
        "Contrôles négatifs vécus : voisinage amputé, stub muté, global non déclaré — chacun refusé nommément ; le rejeu bit-identique de la session entière.",
    ])
    slide("3. Le moteur natif généralisé aux volumes complets", [
        "12 000 cas pour tls13-16, la graine consignée avant le tirage ; le lot unique (le moteur committé vivait en lots de 4 096).",
        "Le compte en registres bruts : le rax et le digeste lus par vecteur — JAMAIS retirés ; la console différée LIGNE-IDENTIQUE au moteur committé.",
        "Le régime chaud contre le pilote C (le même code de bloc appelé directement, gcc -O2, horloges internes symétriques, n=9 médianes) : 4,56 × C — la cible pré-enregistrée ≤ 5 × C TENUE.",
        "Les conventions publiées pareil : le bout-en-bout 77 × C (montage + boucle + console), le moteur committé 1 056 × C (le régime fprintf de base).",
        "L'ordre de grandeur contre l'oracle vivant : 123 × (19,1 µs/vecteur au jumeau contre 0,16 au moteur) ; l'audit 1-sur-10 au jumeau : ZÉRO ÉCART sur 1 200 vecteurs.",
    ])
    h.append(PageBreak())
    slide("4. Le plancher token de l'édition et le budget par vague", [
        "OPT-16 : l'opération éditer par diff structuré — la cible ≤ 150 tokens tenue à 79,5 natifs médians (le ratio plancher 2,89 × le diff réel, au lieu de 24,5 ×).",
        "Le schéma fermé D264 étendu à l'édition : l'agent ne rend QUE le diff structuré ; le client expande, confronte, round-trip ; quatre refus nommés fail-closed.",
        "La faisabilité demeure 9/18 (la variance d'écriture machine, nommée) ; le décodage contraint reste le levier, le gate de sélection d'endpoint désormais vécu sur pièces.",
        "OPT-20 : le budget token par vague mesuré — la production de la vague 28 à 19 269 tokens natifs (le champ usage du bord, jamais une estimation) ; le budget de la vague suivante pré-enregistré.",
        "La méta-optimisation : le protocole s'optimise lui-même — le budget borne la production autoriée, pas l'exécution des chaînes.",
    ])
    slide("5. La réplication et le terrain, pré-enregistrés", [
        "La rejouabilité symétrique : la pièce T rejouée au bac — les cinq sondes du contrat noyau 5/5 VERT (l'écart nommé : le différentiel complet exige l'application entière).",
        "L'indépendance inter-familles : FAMILY-ABSENT consigné (la seule API est la famille GLM, la voie locale 0/64 déjà nommée) — la ligne ATT-REPL demeure EN ATTENTE, aucun chiffre fabriqué.",
        "La vague terrain groupée : UN plan pré-enregistré (sha256 avant tout run) pour les dix attentes — l'ordre, les machines, les budgets, les attendus, la randomisation stratifiée H7.",
        "L'investigation des pics dudect N=200 pré-enregistrée : les trois candidates nommées AVANT les données.",
        "L'agrégateur fail-closed : un run manquant refuse la vague ; les statuts se dérivent des runs, jamais de la frappe ; INCOMPLETE demeure INCOMPLETE.",
        "Tamarin : L3 rejoint bit-identiquement (1 122 pas) ; L1a/L2 entiers au mur 4 Gio, le kit machine réelle à empreinte consignée ; ProVerif : port livré, prouveur absent du bac.",
    ])
    h.append(PageBreak())
    slide("6. Ce qui reste au poste réel", [
        "La publication Zenodo de v0.32.0 (les trois packs assemblés) attend LA COMMANDE du maître — jamais minté sans commande.",
        "La machine réelle goupillée (le couloir VAES, les lemmes L1a/L2 entiers), la bascule au métal nu (le banc 16/16 prêt : 7 cas de transaction + 1 rendez-vous nominal + 5 aléas D261 + 3 invariants), le compteur NV matériel, la sentinelle SACL/4663, FIDO2, le serving qui applique le schéma.",
        "L'entraînement RLVR hors bac (le plan pré-enregistré, le geste compute au développeur).",
        "Le registre unique des chantiers en attente porte 10 entrées, toutes bornées au geste du développeur (la porte recompose le compte, C16).",
    ])
    h.append(Paragraph(f"7. L'édition {EDITION}", H2))
    rows = [["Pièce", "Version"], ["Manuscrit", EDITION],
            ["Spécification", SPECVER], ["Livre du Coffre", BOOKVER],
            ["Preuves et calculs", EDITION], ["Présentation", EDITION]]
    t = Table(rows, colWidths=[90 * mm, 40 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Serif", 9),
                           ("FONT", (0, 0), (-1, 0), "SansB", 9),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#B8C2C8"))]))
    h.append(t)
    construire(PACK / "5-presentation" / f"TRIADE_presentation_v0330.pdf",
               f"TRIADE — présentation {EDITION}", EDITION, h)


if __name__ == "__main__":
    for d in ("1-manuscrit", "2-specification", "3-coffre-fort", "4-preuves-calculs", "5-presentation"):
        (PACK / d).mkdir(parents=True, exist_ok=True)
    (PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf").write_bytes(
        (REPO / "edition-v0230" / "main.pdf").read_bytes())
    (PACK / "2-specification" / f"Protocole_TRIADE_{SPECVER}_Specification.pdf").write_bytes(
        (REPO / "scripts" / "spec_v160" / "main.pdf").read_bytes())
    (PACK / "3-coffre-fort" / f"Livre_du_Coffre_TRIADE_CF1-CF3_{BOOKVER}.pdf").write_bytes(
        (REPO / "scripts" / "livre_v20" / "final.pdf").read_bytes())
    preuves()
    print(f"[pieces v331] {EDITION} : la preuves régénérée à {PACK} (les quatre autres RECONDUITES byte-byte — le patron v0.23.4)")
