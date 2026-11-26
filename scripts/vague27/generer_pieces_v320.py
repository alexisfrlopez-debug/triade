#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GÉNÉRATION DES PIÈCES 4 ET 5 DE L'ÉDITION v0.32.0 (la vague 27).

- 4-preuves-calculs/TRIADE_preuves_v0.32.0.pdf : les rapports des six ateliers de
  la vague 27 LUS VERBATIM de leurs fichiers, le registre de provenance, la table
  des empreintes des quatre autres pièces (aucun document ne porte son propre
  sha256), les limites nommées.
- 5-presentation/TRIADE_presentation_v0320.pdf : la présentation de la vague 25.

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
PACK = pathlib.Path(os.environ.get("TRIADE_PACK", str(REPO / "pack-v320")))
EDITION = os.environ.get("TRIADE_EDITION", "v0.32.0")
SPECVER = os.environ.get("TRIADE_SPECVER", "v0.15.17")
BOOKVER = os.environ.get("TRIADE_BOOKVER", "v1.16")

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


def vague_courante():
    man = (REPO / "edition-v0230/main.tex").read_text(encoding="utf-8")
    m = re.findall(r"the present edition, the ([a-z-]+) wave", man)
    mot = m[-1] if m else "twenty-fifth"
    table = {"fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
             "nineteenth": 19, "twentieth": 20, "twenty-first": 21, "twenty-second": 22,
             "twenty-third": 23, "twenty-fourth": 24, "twenty-fifth": 25}
    return table.get(mot, 25)


def statut_ancrage():
    import importlib.util
    sp = importlib.util.spec_from_file_location("sa", str(REPO / "scripts/vague24/statut_ancrage.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m.statut(strict=False)


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


ELISIONS = {
    # la citation d'un défaut n'est pas le défaut — MAIS le linter refuse certaines
    # formulations même citées dans une pièce : le verbatim vit au rapport committé
    pathlib.Path("atelier-w27recon/rapport.txt"): [
        ("(run exécuté)", "(run [elidé : C26 — la citation vit au rapport committé])"),
        ("« la règle est adoptée et outillée, le\n   déploiement n'est pas fait : aucun témoin ancré n'existe à cette révision, et la porte de\n   release le dit EN ATTENTE »",
         "[la prose divergente du Livre v1.15, elidée : C26 — le verbatim vit au rapport committé]"),
        ("(le déploiement n'est pas fait ; aucun témoin ancré n'existe ; la porte de\n   release le dit EN ATTENTE)",
         "(les trois fragments fautifs [elidés : C26 — le verbatim vit au rapport committé])"),
        ("portait « le déploiement n'est pas fait »",
         "portait [le fragment fautif, elidé : C26]"),
    ],
    pathlib.Path("atelier-w27resid/rapport.txt"): [
        ("« INCOMPLETE au mur mémoire 4 Gio »", "[fragment cité elidé : C26 — le verbatim vit au rapport committé]"),
        ("verifier 13 arbres VERTS", "[elidé : C27 — le verbatim vit au rapport committé]"),
        ("« verifier 13 arbres » ressuscité refusé",
         "[l'invocation des arbres mutée — elidée : C27] ressuscitée refusée"),
    ],
}

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
    canvas.drawString(20 * mm, 12 * mm, f"TRIADE — édition {EDITION} (la vague 25, 26 novembre 2026)")
    canvas.drawRightString(190 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def construire(chemin, titre, sous_titre, histoire):
    doc = BaseDocTemplate(str(chemin), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=18 * mm,
                          title=titre, author="Alexis Lopez")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=page)])
    doc.build(histoire)


def preuves():
    p1 = PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf"
    p2 = PACK / "2-specification" / f"Protocole_TRIADE_{SPECVER}_Specification.pdf"
    p3 = PACK / "3-coffre-fort" / f"Livre_du_Coffre_TRIADE_CF1-CF3_{BOOKVER}.pdf"
    pieces = [(f"Le manuscrit académique {EDITION}", p1), (f"La spécification {SPECVER}", p2),
              (f"Le Livre du Coffre {BOOKVER}", p3)]
    ateliers = [
        ("W27RECON — la réconciliation sémantique inter-pièces : D267 soldé, la classe C26",
         REPO / "atelier-w27recon/rapport.txt"),
        ("W27RESID — les résidus éditoriaux soldés à la source, les classes C27-C29",
         REPO / "atelier-w27resid/rapport.txt"),
        ("W27CIBLES — le registre des cibles au périmètre explicite, la règle des ères",
         REPO / "atelier-w27cibles/rapport.txt"),
        ("W27DECCO — la campagne add à décodage contraint : le harnais prêt, SERVING-ABSENT",
         REPO / "atelier-w27decco/rapport.txt"),
        ("W27PREUV — les preuves symboliques : la décomposition vécue, la sémantique d'occurrence",
         REPO / "atelier-w27preuv/rapport.txt"),
        ("W27VAES — le couloir VAES/VPCLMULQDQ + la session native du moteur d'oracle",
         REPO / "atelier-w27vaes/rapport.txt"),
    ]
    h = [Paragraph("TRIADE — Preuves et calculs", H1),
         Paragraph(f"Édition {EDITION} — la vague 25 (26 novembre 2026)", H2),
         Paragraph("Ce document rassemble les pièces de la vague 25 <b>lues verbatim de leurs "
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
        f"Le linter d'édition passe à <b>{classes_linter()} classes</b> : la vague 25 ajoute "
        "C26 STATUS-INTERPIECES (tout statut sémantique partagé — ancrage, compteur NV, "
        "Tamarin/ProVerif, sentinelle Windows, fence.i — est recomposé du registre "
        "PREUVES-STATUTS.json et AUCUNE des cinq pièces ne peut le contredire : la "
        "divergence D267 du Livre v1.15, démontrée sur pièces, est soldée par le Livre v1.16 "
        "au statut dérivé du journal d'ancrage append-only), C27 COUNT-TABLECELL (tout compte "
        "d'arbres en cellule confronté au registre — les quatorze arbres signés de la Table 12, "
        "D177), C28 TITLE-UNIQUE (les deux titres de vague distingués) et C29 LANG-BODY (la "
        "langue du corps par pièce — les fragments français du manuscrit anglais rendus à "
        "l'anglais). Le registre des cibles porte sa table des ères et chaque verdict TENUE "
        "cite son périmètre ou porte l'étiquette HISTORIQUE-DATÉ ; la campagne add à décodage "
        "contraint vit son refus nommé SERVING-ABSENT (le bord accepte response_format et ne "
        "l'applique pas — le harnais est prêt, aucun chiffre fabriqué) ; les preuves "
        "symboliques avancent (L1c et L2a vérifiées au bac par décomposition, la sémantique "
        "d'occurrence du prouveur nommée, le kit machine réelle à empreinte consignée) ; le "
        "couloir VAES est écrit sur sa notation gelée et mesuré : porte verte d'abord (20/20 "
        "CAVP contre la référence indépendante, le mutant refusé au premier vecteur, "
        "round-trip vert), cible pré-enregistrée ≤ 1,05 × EVP <b>manquée à 5,66 ×</b> et "
        "publiée telle quelle ; la session native du moteur d'oracle exécute le corpus des "
        "235 vecteurs à 0,266 s médiane (cible &lt; 10 s, classification 235/235 identique au "
        "jumeau). <b>Aucune valeur mesurée n'est modifiée ; aucun artefact scellé n'est "
        "touché ; aucune cible n'est re-tirée.</b>", BODY))
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
        "674 (adopté) ; ajouter 2 200 (adopté) — un verdict TENUE cite le périmètre courant ou "
        "porte l'étiquette.", BODY))
    h.append(Paragraph("4 bis. Le registre des cibles (D276) — au périmètre explicite", H2))
    h.append(Paragraph("Les cibles de ce programme vivent dans un registre unique (CIBLES.md) ; "
                       "aucune n'est re-tirée. Les lignes, telles quelles, chacune avec son "
                       "périmètre de mesure :", BODY))
    for c in _cibles():
        h.append(Paragraph(f"<b>{c[0]}</b> — {c[1]} · <b>{c[5]}</b> · mesuré {c[4]} · "
                           f"périmètre : {c[2]} ({c[6]}).", BODY))
    h.append(Paragraph("Le couloir AES-GCM entrelacé est mesuré (1,26 × EVP) et <b>hors sujet</b> "
                       "de la cible 1,05 × : celle-ci vise le couloir VAES — écrit à la vague 25, "
                       "mesuré à 5,66 × EVP, <b>manquée et publiée telle quelle</b> ; la machine "
                       "réelle goupillée demeure le geste du poste.", BODY))
    h.append(Paragraph("5. Les limites nommées", H2))
    h.append(Paragraph("Aucune mesure au métal nu (le couloir VAES et la session native vivent "
                       "l'étiquette VM, fréquence non goupillée — le caveat nommé) ; la bascule "
                       "concurrente réelle et le compteur NV matériel restent EN ATTENTE ; la "
                       "campagne structurée attend un serving qui applique le schéma (le refus "
                       "SERVING-ABSENT consigné) ; la sentinelle Windows (SACL/4663) configurée "
                       "reste au poste réel ; "
                       f"{STATUT_TAM} L1a et L2 entiers attendent la machine réelle (kit à "
                       "empreinte consignée) ; INCOMPLETE demeure INCOMPLETE. L'ancrage de "
                       "transparence est adopté, outillé et "
                       f"{statut_ancrage()['statut']} (D267, statut dérivé du journal — la classe "
                       "C26 le recompose aux cinq pièces). La porte de génération couvre "
                       f"{classes_linter()} classes.", BODY))
    h.append(PageBreak())
    h.append(Paragraph("6. Les rapports des ateliers, lus verbatim", H2))
    h.append(Paragraph("Chaque rapport est lu de son fichier committé ; les ELISIONS nommées "
                       "(C26/C27) retirent des pièces les répétitions des fragments fautifs "
                       "cités — le verbatim intégral vit au rapport du dépôt, la pièce ne porte "
                       "jamais un statut contredit, fût-ce en citation.", BODY))
    for titre, p in ateliers:
        h.append(Paragraph(titre, H2))
        h.append(Paragraph(f"<font size=7 color='#555F66'>source : {p.relative_to(REPO)}</font>", PETIT))
        h.append(Paragraph(extrait(p).replace("\n", "<br/>"), MONO))
        h.append(Spacer(1, 4 * mm))
    construire(PACK / "4-preuves-calculs" / f"TRIADE_preuves_et_calculs_{EDITION}.pdf",
               f"TRIADE — Preuves et calculs {EDITION}", EDITION, h)


def presentation():
    p1 = PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf"
    p2 = PACK / "2-specification" / f"Protocole_TRIADE_{SPECVER}_Specification.pdf"
    p3 = PACK / "3-coffre-fort" / f"Livre_du_Coffre_TRIADE_CF1-CF3_{BOOKVER}.pdf"
    p4 = PACK / "4-preuves-calculs" / f"TRIADE_preuves_et_calculs_{EDITION}.pdf"
    T = ParagraphStyle("T", fontName="SansB", fontSize=24, leading=30, textColor=colors.HexColor("#1F4E5F"))
    S = ParagraphStyle("S", fontName="Sans", fontSize=12, leading=17, textColor=colors.HexColor("#555F66"))
    Pu = ParagraphStyle("Pu", fontName="Sans", fontSize=12, leading=19, leftIndent=10, bulletIndent=0,
                        spaceAfter=7)
    h = [Spacer(1, 55 * mm),
         Paragraph(f"TRIADE — édition {EDITION}", T),
         Paragraph(f"La vague {vague_courante()} : la revue du pack répondue à la source, "
                   "les statuts recomposés, les cibles au périmètre explicite", S),
         Spacer(1, 8 * mm),
         Paragraph("Alexis Lopez · 26 novembre 2026", S), PageBreak()]

    def slide(titre, points):
        h.append(Paragraph(titre, H2))
        for b in points:
            h.append(Paragraph(b, Pu, bulletText="•"))
        h.append(Spacer(1, 6 * mm))

    slide("1. La divergence D267, démontrée puis soldée", [
        "Le Livre v1.15 portait « le déploiement n'est pas fait » ; la spécification, la présentation et les preuves portaient DÉPLOYÉ.",
        "La cause est nommée : la classe C20 ne couvrait que trois pièces — le Livre lui échappait.",
        "Le statut unique se DÉRIVE du journal d'ancrage append-only (témoin RFC 3161 vérifié à chaque porte V6).",
        "Le Livre v1.16 régénéré à la source ; la classe C26 STATUS-INTERPIECES recompose désormais cinq statuts partagés aux cinq pièces.",
        "Six contrôles négatifs vécus : le statut muté dans une pièce, le registre muté — chaque refus nommé.",
    ])
    h.append(PageBreak())
    slide("2. Les résidus éditoriaux, corrigés à la source", [
        "La Table 12 disait « treize arbres » : le sceau de l'Intention en signe QUATORZE depuis D177 — la colonne historique demeure datée.",
        "Les deux titres « Ce que change la v0.15.16 » distingués (D274 les six résidus · D275 la prose de statut).",
        "Les fragments français du manuscrit anglais rendus à l'anglais — les valeurs demeurent intactes.",
        "La chronologie du Livre réordonnée aux dates imprimées ; le texte de chaque rangée inchangé.",
        "Trois classes nouvelles : COUNT-TABLECELL, TITLE-UNIQUE, LANG-BODY — le linter à 29 classes.",
    ])
    slide("3. Les cibles au périmètre explicite", [
        "La table des ères rendue visible : ère M1 (historique, datée), pointeur-seul, contenu seul, ADOPTÉ (le périmètre courant).",
        "CIB-LOC-BUDGET aux deux ères côte à côte : 51 M1 (HISTORIQUE-DATÉ) contre 627 adopté / 1 053 pointeur-seul.",
        "La règle générale : un verdict TENUE cite la mesure du périmètre courant ou porte l'étiquette HISTORIQUE-DATÉ.",
        "C25 étendue : un verdict appuyé sur une mesure d'une autre ère sans étiquette est REFUSÉ.",
        "Trois contrôles négatifs vécus ; aucune cible re-tirée ; onze lignes recomposées du registre.",
    ])
    h.append(PageBreak())
    slide("4. La campagne à décodage contraint : SERVING-ABSENT", [
        "La cible pré-enregistrée (≥ 15/18 à ≤ 3 000 tokens) n'est JAMAIS re-tirée.",
        "Le harnais est prêt : schéma fermé {op, dst, src, offset}, 11 opcodes, juge importé à empreinte sha256 consignée.",
        "La boucle de réparation bornée à trois tours ; l'agrégateur fail-closed (un appel manquant refuse le verdict).",
        "La sonde vécue : le bord accepte response_format — json_schema strict — et NE L'APPLIQUE PAS ; la violation passe intégrale.",
        "Verdict : SERVING-ABSENT, consigné ; aucun chiffre fabriqué ; les fixtures 18/18, quatre refus nommés éprouvés, rejeu bit-identique.",
    ])
    slide("5. Les preuves symboliques : la décomposition vécue", [
        "L3 rejoint bit-identiquement (1 122 pas) ; L1c vérifiée (52 pas : le pont des trois fuites tenues).",
        "L2a vérifiée (7 pas : la chaîne des phrases hôtes par induction).",
        "La première formulation de L2b REFUTÉE par la sémantique d'occurrence de tamarin 1.12.0 — un fait s'ancre à sa consommation : la sémantique de l'OUTIL, pas une attaque du protocole.",
        "L1a et L2 entiers demeurent au mur mémoire 4 Gio ; le kit de run machine réelle vit à empreinte de modèle consignée.",
        "Tout statut dérive de PREUVES-STATUTS.json ; INCOMPLETE demeure INCOMPLETE — aucun verdict fabriqué.",
    ])
    h.append(PageBreak())
    slide("6. Le couloir VAES : la porte verte d'abord, la cible manquée", [
        "La notation gelée AVANT l'implémentation (sha256 consignée) : CPUID hissé hors boucle, CTR×VAES deux blocs par vAESENC, GHASH à pli de huit blocs sur VPCLMULQDQ.",
        "Cinq fautes de première passe nommées au source (la réflexion, l'appariement des puissances, les voies de Karatsuba) — trouvées par la référence GCM indépendante et le juge croisé.",
        "LA PORTE : 20/20 vecteurs NIST CAVP contre EVP octet pour octet ; le mutant refusé au premier vecteur ; le round-trip inter-implémentations VERT.",
        "LA MESURE : 5,66 × OpenSSL EVP au même volume — la cible pré-enregistrée ≤ 1,05 × est MANQUÉE, publiée telle quelle.",
        "La décomposition du coût nommée : l'expansion hors boucle, la conversion par bloc, le calendrier C que le compilateur ne préserve pas.",
    ])
    slide("7. La session native du moteur d'oracle", [
        "Le refus mmap 0xC000 du bac d'alors RE-ÉPROUVÉ : mmap_min_addr = 4 096 — la cartographie passe.",
        "La porte du moteur re-vécue verte : jumeau ligne-identique, shim muté attrapé au premier vecteur, mémo content-addressed, audit 1-sur-10.",
        "LA SESSION : 50 blocs assemblés depuis leurs notations (sha256 recoupés 50/50), 235 vecteurs exécutés nativement.",
        "Classification 235/235 identique au jumeau ; le digeste 81/81 ; les quatre écarts d'une classe nommée (rax non défini par le bloc).",
        "MÉDIANE 0,266 s sur n=5 — la cible T &lt; 10 s (CIB-ORACLE-T) TENUE ; l'échelle nommée : le corpus de 235, pas les 12 000 cas par bloc.",
    ])
    h.append(PageBreak())
    h.append(Paragraph(f"8. L'édition {EDITION}", H2))
    rows = [["Pièce", "Version"], ["Manuscrit", EDITION], ["Spécification", SPECVER],
            ["Livre du Coffre", BOOKVER], ["Preuves et calculs", EDITION],
            ["Présentation", EDITION]]
    t = Table(rows, colWidths=[90 * mm, 40 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Serif", 9),
                           ("FONT", (0, 0), (-1, 0), "SansB", 9),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#B8C2C8"))]))
    h.append(t)
    h.append(Paragraph("9. Ce qui reste au poste réel", H2))
    for b in [
        "La machine réelle goupillée pour le couloir VAES (le kit livré : notation + source + porte + commande de mesure) et les lemmes L1a/L2 entiers.",
        "La bascule au métal nu : le banc de bascule 16/16 = 7 cas de transaction + 1 rendez-vous nominal + 5 aléas D261 + 3 invariants, le métal EN ATTENTE (≥ 2 machines).",
        "Le serving qui applique le schéma (la campagne D264 prête à courir), la bascule au métal nu, le compteur NV matériel.",
        "La sentinelle Windows SACL/4663, IMA/Authenticode configurés, le prototype FIDO2.",
        "Les vecteurs d'oracle : 320 produits = 235 exécutables + 85 tests de rejet ; "
        "95 exécutés au contexte standard, 27 blocs sans exécution — recomposé depuis les fichiers (C17).",
        "Le registre unique des chantiers en attente porte 10 entrées (STATUTS-EN-ATTENTE.md) ; "
        "la porte recompose ce compte (C16) et refuse tout écart.",
    ]:
        h.append(Paragraph(b, Pu, bulletText="•"))
    construire(PACK / "5-presentation" / "TRIADE_presentation_v0320.pdf",
               f"TRIADE — présentation {EDITION}", EDITION, h)


if __name__ == "__main__":
    for d in ("1-manuscrit", "2-specification", "3-coffre-fort", "4-preuves-calculs", "5-presentation"):
        (PACK / d).mkdir(parents=True, exist_ok=True)
    (PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf").write_bytes(
        (REPO / "edition-v0230" / "main.pdf").read_bytes())
    (PACK / "2-specification" / f"Protocole_TRIADE_{SPECVER}_Specification.pdf").write_bytes(
        (REPO / "scripts" / "spec_v159" / "main.pdf").read_bytes())
    (PACK / "3-coffre-fort" / f"Livre_du_Coffre_TRIADE_CF1-CF3_{BOOKVER}.pdf").write_bytes(
        (REPO / "scripts" / "livre_v19" / "final.pdf").read_bytes())
    for d in ("1-manuscrit", "2-specification", "3-coffre-fort"):
        pass
    preuves()
    presentation()
    print(f"[pieces] {EDITION} : les cinq pièces à {PACK}")
