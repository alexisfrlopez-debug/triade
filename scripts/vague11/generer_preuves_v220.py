#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v220.py — le document TRIADE_preuves_et_calculs_v0.22.0.pdf
(ReportLab + weasyprint) : les pièces de la vague 11 — les huit ateliers
(la purge D81, les couloirs SIMD, la boucle porteuse, les gabarits, le
coffre durci, le quatrième bras, les kits pré-enregistrés, la soundness
du lifter), LA DÉCOMPOSITION MÉMOIRE CORRIGÉE (l'erratum nommé — la
correction (a) de zho5vilpy), LA CAUSE DU « couloir B : code 1 »
consignée (la correction (f)). Les pièces verbatim sont LUES des
ateliers — jamais retapées, INTÉGRALES (la coupure À LA LIGNE près, la
limite de 2 600 caractères de la v0.21.0 corrigée)."""
import csv
import hashlib
import pathlib
import subprocess

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer)

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "scripts" / "vague11"
OUT = ICI / "preuves_v220_body.pdf"
PUR = REPO / "atelier-sequestre-ou6wn6wlv"
COR = REPO / "atelier-corridors-fnvan0zes"
POR = REPO / "atelier-porteuse-ahult8jgd"
GAB = REPO / "atelier-gabarits-o5apue194"
COF = REPO / "atelier-coffre-vr9n3s3l7"
Q4 = REPO / "atelier-quatrebras-3lmyfb2xa"
KIT = REPO / "atelier-preregistre-l4nnwqlld"
LIF = REPO / "atelier-lifter-hrbdfy6i4"
SEC = REPO / "atelier-securite-bk79jvzbm"
MED = REPO / "atelier-medians-zho5vilpy"

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/"
                               "DejaVuSansMono.ttf"))

DARK = colors.HexColor("#162032")
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=14.2,
                         alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=15.5, leading=20,
                      textColor=DARK, spaceBefore=14, spaceAfter=8)
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.3, leading=8.2,
                        textColor=colors.HexColor("#222222"))
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Serif", fontSize=11.6, leading=15.6,
                         textColor=colors.HexColor("#444444"))


def para(txt, st):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;"), st)


def lit(chemin, max_lignes=None):
    """LA COUPE À LA LIGNE (la correction (f) de zho5vilpy) : la limite de
    2 600 CARACTÈRES de la v0.21.0 (qui tronquait « N'ÉMET AUCUN » en
    « n'émAUCUN ») devient la coupure au bord de LIGNE — le verbatim des
    rapports d'atelier INTÉGRAL par défaut."""
    t = pathlib.Path(chemin).read_text(encoding="utf-8", errors="replace")
    if max_lignes is None:
        return t
    lignes = t.splitlines()
    return "\n".join(lignes[:max_lignes])


def decomposition_corrigee():
    """LA DÉCOMPOSITION MÉMOIRE CORRIGÉE (la correction (a)) : RECALCULÉE
    du CSV brut — la ligne publiée « médiés 0 » sommait à 1750, pas
    2098 ; l'erratum nommé."""
    with open(SEC / "surete_memoire_v200.csv", newline="",
              encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    tot = {k: 0 for k in rows[0] if k not in ("domaine", "bloc")}
    for r in rows:
        for k, v in r.items():
            if k in tot:
                tot[k] += int(v)
    lignes = [
        "LA DÉCOMPOSITION MÉMOIRE CORRIGÉE (zho5vilpy, la correction (a) — "
        "L'ERRATUM NOMMÉ)",
        "La ligne publiée à la v0.21.0 (la pièce 4 d'alors, le verbatim de "
        "rapport-gardes.txt) :",
        "  pile 1247 · médiés 0 · constants 191 · plan-fixe 189 · plan-garde "
        "13 · contrat-boucle 18 · nommés 92 · hors-cadre 0",
        f"  — LA SOMME PUBLIÉE : 1750, PAS 2098 : LA FAUTE NOMMÉE. Le compte "
        f"« médiés 0 » était UNE ERREUR : la colonne medies_contrat du CSV "
        f"brut porte {tot['medies_contrat']}.",
        "",
        "LE RECOMPTE (surete_memoire_v200.csv, 52 lignes, chaque catégorie "
        "sommée PAR CODE — le générateur même de la présente pièce) :",
        f"  pile {tot['pile']} · MÉDIÉS {tot['medies_contrat']} · constants "
        f"{tot['constants_rip']} · plan-fixe {tot['plan_fixe']} · plan-garde "
        f"{tot['plan_garde']} · contrat-boucle {tot['contrat_boucle']} · "
        f"nommés {tot['nommes']} · hors-cadre {tot['hors_cadre']}",
        f"  = {tot['pile'] + tot['medies_contrat'] + tot['constants_rip'] + tot['plan_fixe'] + tot['plan_garde'] + tot['contrat_boucle'] + tot['nommes'] + tot['hors_cadre']} "
        f"EXACTEMENT (== acces_mem {tot['acces_mem']})",
        "",
        f"LA COHÉRENCE RECONDUITE : 2006 déchargés + 34 LEA relationnels + "
        f"58 gardes = 2098 ; les catégories déchargées somment à "
        f"{tot['pile'] + tot['medies_contrat'] + tot['constants_rip'] + tot['plan_fixe'] + tot['plan_garde'] + tot['contrat_boucle']} "
        f"(2006 attendus).",
        "Le verbatim de rapport-gardes.txt demeure à la pièce publiée "
        "v0.21.0, octet pour octet (l'histoire n'est pas réécrite) ; la "
        "présente correction vit au texte des preuves v0.22.0.",
    ]
    return "\n".join(lignes)


def cause_couloir_b():
    return "\n".join([
        "LA CAUSE DU « couloir B : code 1 » NOMMÉE (zho5vilpy, la "
        "correction (f))",
        "LA LIGNE (la pièce 1 des preuves v0.21.0, le verbatim de "
        "rapport-remesure.txt — la ligne demeure au verbatim, la cause "
        "consignée ici) :",
        "  !! couloir B : code 1",
        "LA CAUSE : le sous-processus cpuid_hisse.py MORT À L'IMPORT — la "
        "chaîne cpuid_hisse.py → m4/build_m4.py → « import pefile » (et "
        "pynacl à la pile du labo) : pefile/nacl ABSENTS du bac à la "
        "régénération du rapport v0.21.0, ModuleNotFoundError, code de "
        "sortie 1.",
        "LA RE-EXÉCUTION (pefile+pynacl MAINTENANT posés au bac — la mesure "
        "re-ouverte à l'identique, le rig 8z4hj76w4, 64 blocs, la graine "
        "20261120) : LA V1 (le sondage par bloc) 45 instructions/bloc ; LA "
        "V2 (le sondage hissé) 34.4 ; LE SCELLÉ GPR 26 ; le scellé en flot "
        "34.4 — LES CHIFFRES PUBLIQUÉS V0.21.0 REPRODUITS (reexecution-"
        "couloir-b.txt à l'atelier zho5vilpy, l'import vivant, exit 0).",
        "LA LEÇON : la ligne « code 1 » demeurée au verbatim n'était PAS un "
        "échec de mesure — la mesure vivait au rapport-temps-reel.txt ; "
        "c'était l'outil de re-vérification du couloir B qui mourait à "
        "l'import au bac de régénération : la cause nommée, la pièce "
        "demeurée.",
    ])


story = [
    para("TRIADE — preuves et calculs", st_titre),
    para("Édition v0.22.0 — la vague 11 : la purge des instructions de "
         "remise D81, les couloirs SIMD mesurés sur matériel, la boucle "
         "porteuse AES-NI restructurée sous sa cible, les gabarits "
         "versionnés, le coffre durci sur copies de laboratoire, le "
         "quatrième bras C+G+, les kits pré-enregistrés, la soundness du "
         "lifter au domaine — et les errata nommés de la v0.21.0 (la "
         "décomposition mémoire, la cause du « couloir B : code 1 »)",
         st_sous),
    Spacer(1, 6),
    para("Le présent document porte les pièces de la vague 11 : les neuf "
         "instructions exécutées aux plans gelés d'abord (les empreintes "
         "consignées AVANT la première donnée à EMPREINTES-PLANS-VAGUE11."
         "txt, le commit 3962b26 précédant toute mesure), les huit "
         "ateliers portés par leurs rapports verbatim INTÉGRAUX (la coupure "
         "à la ligne près — la limite de 2 600 caractères de la v0.21.0, "
         "qui tronquait « n'ÉMET AUCUN » en « n'émAUCUN », corrigée), LA "
         "DÉCOMPOSITION MÉMOIRE CORRIGÉE avec l'erratum nommé (le compte "
         "« médiés 0 » publié à la v0.21.0 sommait à 1750, pas 2098 — le "
         "recompte du CSV brut porte 348, la somme exacte 2098), et LA "
         "CAUSE du « couloir B : code 1 » consignée (le sous-processus "
         "mort à l'import, les chiffres re-exécutés et reproduits). Les "
         "pièces verbatim sont lues des ateliers — jamais retapées. Le "
         "concept DOI 10.5281/zenodo.24367343 résout sur la version "
         "courante (le dépôt public D220).", st_body),
    para("LA VAGUE 11 EN UNE PAGE", st_h1),
    para("(1) ou6wn6wlv — LA PURGE D81 : le séquestre 5/3 LA GARDE ACTIVE, "
         "le dépôt public ; LE LIVRE v1.6 (15 remplacements ancrés) ET LA "
         "SPEC v0.15.7 (11 remplacements) purgés des instructions de "
         "remise ; la simulation du runbook au clone D105 : huit étapes "
         "sans écriture, LE GESTE PIÈGE REFUSÉ au premier nom, le scan "
         "des 513 commits zéro fuite. (2) fnvan0zes — LES COULOIRS SIMD : "
         "l'hybride memchr+memcmp 704 cycles [52] (25,9× sous le scellé "
         "GPR — LA CLASSE des primitives SIMD libc), le SHA-NI corps "
         "128,5 c/bloc (6,5×), l'AVX2 dominé par le sondage au bac "
         "virtualisé (cpuid ≈ 2 660 cycles — le hissage par session) ; LA "
         "BATTERIE 559 vecteurs ZÉRO DIVERGENCE. (3) ahult8jgd — LA "
         "BOUCLE PORTEUSE : la v4-inline 7,09 c/bloc [0,09] — LA CIBLE "
         "≤12 ATTEINTE (7,1× sur le flux v2 50,56, la classe du scellé "
         "appelé 7,62) ; LE CACHE de round-trip 680,6× (le contrôle "
         "négatif double) ; LA CRISTALLISATION INCRÉMENTALE −54 % (l'audit "
         "1/10 un filet probabiliste NOMMÉ) ; LES 37 s DÉCOMPOSÉES (les "
         "oracles 81 %). (4) o5apue194 — LES GABARITS : éditer 1 106 → "
         "674 natif (−39,1 %, la prose −57 %), localiser 1 053 → 627 "
         "(−40,5 %), ajouter 3 074 → 2 200 (−28,5 %, la faisabilité 0→3 — "
         "LE GAP NOMMÉ aux quinze refus honnêtes). (5) vr9n3s3l7 — LE "
         "COFFRE DURCI : (a)-(g) verts sur copies labo (D105), LE MODÈLE "
         "z3 quatre invariants (le contrôle négatif nommant la garde). "
         "(6) 3lmyfb2xa — LE QUATRIÈME BRAS C+G+ : T 39,39 · C+G+ 18,68 · "
         "C+G 2,18 · C 1,97 — NOTATION PROPRE 20,72 s (55,7 %) + RÉGIME "
         "16,50 s (44,3 %) + GOUVERNANCE 0,213 s : H-CGP2 CONFIRMÉE, la "
         "requalification rejetée ; la réconciliation 20/20, le contrôle "
         "négatif double attrapé et attribué. (7) l4nnwqlld — LES SIX KITS "
         "PRÉ-ENREGISTRÉS hashés (57/57 autotests, AUCUN résultat — la "
         "règle : le geste du développeur seul produit le terrain). "
         "(8) hrbdfy6i4 — LA SOUNDNESS DU LIFTER AU DOMAINE : 942 "
         "encodages ZÉRO divergence (la méthode exacte — écritures au "
         "diff, lectures à la sentinelle différentielle), 155 mutantes "
         "TOUTES HORS VOCABULAIRE (LA GARDE fail-closed), H secret couvert "
         "(tls13-17 à P3 — ni branche ni adresse), LA NON-INTERFÉRENCE "
         "16/16 blocs, SEPT familles, tls13-04 au modèle affiné ; le "
         "premier passage artefactuel consigné.",
         st_body),
    Spacer(1, 10),
]

# ---- LES ERRATA NOMMÉS (les corrections (a) et (f) de zho5vilpy) ---------
story += [para("LES ERRATA NOMMÉS DE LA v0.21.0 (l'atelier zho5vilpy — "
               "les corrections sur pièces)", st_h1),
          para(decomposition_corrigee(), st_mono),
          Spacer(1, 6),
          para(cause_couloir_b(), st_mono),
          Spacer(1, 10)]

# ---- les pièces verbatim (les huit ateliers, INTÉGRALES) ----------------
PIECES = [
    ("LA PIÈCE 1 — LA PURGE DES INSTRUCTIONS DE REMISE D81 (ou6wn6wlv — "
     "le rapport, verbatim intégral)", PUR / "rapport-purge.txt"),
    ("LA PIÈCE 2 — LES COULOIRS SIMD : la batterie et le temps réel "
     "(fnvan0zes — les deux rapports, verbatim intégraux)",
     [COR / "rapport-corridors.txt", COR / "rapport-temps-reel-corridors.txt"]),
    ("LA PIÈCE 3 — LA BOUCLE PORTEUSE AES-NI RESTRUCTURÉE (ahult8jgd — le "
     "rapport, verbatim intégral)", POR / "rapport-porteuse.txt"),
    ("LA PIÈCE 4 — LES GABARITS VERSIONNÉS (o5apue194 — le rapport, "
     "verbatim intégral)", GAB / "rapport-gabarits.txt"),
    ("LA PIÈCE 5 — LE DURCISSEMENT DU COFFRE SUR COPIES DE LABORATOIRE "
     "(vr9n3s3l7 — le rapport, verbatim intégral)", COF / "rapport-coffre.txt"),
    ("LA PIÈCE 6 — LE QUATRIÈME BRAS C+G+ (3lmyfb2xa — le rapport de "
     "mesure, verbatim intégral)", Q4 / "rapport-cgp-m4.txt"),
    ("LA PIÈCE 7 — LES KITS PRÉ-ENREGISTRÉS (l4nnwqlld — le rapport, "
     "verbatim intégral)", KIT / "rapport-preregistre.txt"),
    ("LA PIÈCE 8 — LA SOUNDNESS DU LIFTER AU DOMAINE (hrbdfy6i4 — le "
     "rapport, verbatim intégral)", LIF / "rapport-lifter.txt"),
    ("LA PIÈCE 9 — LE PLANCHER ÉDITER AU NATIF ET LE RECOMPTE MÉMOIRE "
     "(zho5vilpy — les rapports de l'atelier des errata, verbatim "
     "intégraux)",
     [MED / "rapport-plancher-natif.txt", MED / "rapport-recompte.txt"]),
]
for titre, chemins in PIECES:
    story.append(para(titre, st_h1))
    if isinstance(chemins, list):
        for c in chemins:
            story.append(para(f"— {c.name} —", st_body))
            story.append(para(lit(c), st_mono))
    else:
        story.append(para(lit(chemins), st_mono))

# ---- la table des empreintes des pièces de contenu ----------------------
EMP = {
    "TRIADE_manuscrit_v0.22.0.pdf": REPO / "edition-v0220" / "main.pdf",
    "Protocole_TRIADE_v0.15.7_Specification.pdf":
        REPO / "scripts" / "spec_v157" / "main.pdf",
    "Livre_du_Coffre_TRIADE_CF1-CF3_v1.6.pdf":
        REPO / "scripts" / "livre_v16" / "final.pdf",
    "rapport-purge.txt": PUR / "rapport-purge.txt",
    "rapport-corridors.txt": COR / "rapport-corridors.txt",
    "rapport-temps-reel-corridors.txt":
        COR / "rapport-temps-reel-corridors.txt",
    "rapport-porteuse.txt": POR / "rapport-porteuse.txt",
    "rapport-gabarits.txt": GAB / "rapport-gabarits.txt",
    "rapport-coffre.txt": COF / "rapport-coffre.txt",
    "rapport-cgp-m4.txt": Q4 / "rapport-cgp-m4.txt",
    "rapport-preregistre.txt": KIT / "rapport-preregistre.txt",
    "rapport-lifter.txt": LIF / "rapport-lifter.txt",
    "rapport-plancher-natif.txt": MED / "rapport-plancher-natif.txt",
    "rapport-recompte.txt": MED / "rapport-recompte.txt",
}
lignes = ["LA TABLE DES EMPREINTES (les pièces de contenu gravées — la "
          "convention : le document ne porte pas son propre sha-256)"]
for nom, ch in EMP.items():
    h = hashlib.sha256(ch.read_bytes()).hexdigest()
    lignes.append(f"{h}  {nom}")
story += [para("LA TABLE DES EMPREINTES", st_h1),
          para("\n".join(lignes), st_mono)]

doc = BaseDocTemplate(str(OUT), pagesize=A4,
                      leftMargin=52, rightMargin=52,
                      topMargin=54, bottomMargin=54,
                      title="TRIADE preuves v0.22.0",
                      author="TRIade")
f = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="c")
doc.addPageTemplates([PageTemplate(id="p", frames=[f])])
doc.build(story)
print(f"[body] {OUT}")

COVER_HTML = ICI / "preuves_v220_cover.html"
COVER_HTML.write_text("""<html><head><meta charset="utf-8"><style>
@page { size: A4; margin: 0; }
body { margin: 0; font-family: 'Liberation Serif', serif; }
.cover { width: 210mm; height: 297mm; background: #162032; color: #fff;
padding: 24mm 20mm; box-sizing: border-box; }
h1 { font-size: 34pt; margin: 0 0 4mm; }
.sub { font-size: 13pt; color: #cdd6e6; margin-bottom: 14mm; }
.label { font-size: 10pt; letter-spacing: 3px; color: #8fa3c8;
margin-bottom: 4mm; }
.meta { font-size: 10.5pt; line-height: 1.7; color: #dfe6f2; }
.rule { border-top: 1px solid #3a4a66; margin: 10mm 0; }
</style></head><body><div class="cover">
<h1>Preuves et calculs</h1>
<div class="sub">La vague 11 — l'&eacute;dition v0.22.0</div>
<div class="label">PI&Egrave;CES DE LA VAGUE</div>
<div class="meta">
La purge D81 : le s&eacute;questre 5/3 la garde active, le d&eacute;p&ocirc;t public — le geste pi&egrave;ge refus&eacute;<br/>
Les couloirs SIMD : l'hybride 704 cycles, le SHA-NI 128,5 c/bloc — la batterie 559 &agrave; z&eacute;ro divergence<br/>
La boucle porteuse : 7,09 c/bloc — la cible &le;12 atteinte ; le cache de round-trip 680,6&times;<br/>
Les gabarits versionn&eacute;s : &eacute;diter 674 natifs (la prose &minus;57&nbsp;%), localiser 627, ajouter par squelette<br/>
Le quatri&egrave;me bras : la notation propre 20,72&nbsp;s (55,7&nbsp;%) s&eacute;par&eacute;e du r&eacute;gime (44,3&nbsp;%) — H-CGP2 confirm&eacute;e<br/>
La soundness du lifter au domaine : 942 encodages, la garde fail-closed, 16 blocs<br/>
Les errata nomm&eacute;s : la d&eacute;composition m&eacute;moire corrig&eacute;e (m&eacute;di&eacute;s 348, la somme 2098 exacte), la cause du &laquo;&nbsp;couloir B&nbsp;: code 1&nbsp;&raquo;
</div>
<div class="rule"></div>
<div class="meta">Document de preuve &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.22.0 &middot; 21 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", str(COVER_HTML),
                str(ICI / "preuves_v220_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "preuves_v220_cover.pdf")).pages[0])
for p_ in PdfReader(str(OUT)).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — preuves et calculs v0.22.0"})
FINAL = ICI / "TRIADE_preuves_et_calculs_v0.22.0.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(str(FINAL)).pages)} pages)")
