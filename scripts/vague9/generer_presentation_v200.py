#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v200.py — la présentation du 20/11 à l'édition
v0.20.0 (la vague 9) : la sécurité au plancher, la boucle de vérification,
les deux couloirs de performance, le coût en tokens au-delà d'OPT-05, le
tableau de bord des quatre axes. LES EMPREINTES SHA-256 des quatre autres
pièces y sont GRAVÉES (la consigne de l'instruction : les empreintes des
cinq pièces consignées dans la présentation et le document de preuves —
la convention : aucun document ne porte son propre sha-256, le manifeste
du pack porte les cinq)."""
import hashlib
import os
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

REPO = Path("/home/z/my-project/depot")
ICI = REPO / "scripts" / "vague9"
OUT = ICI / "presentation_v200_body.pdf"

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/"
                               "DejaVuSansMono.ttf"))

DARK = colors.HexColor("#162032")
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.8, leading=14.6,
                         alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5, leading=21,
                       textColor=DARK, spaceBefore=13, spaceAfter=8)
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.6, leading=8.6,
                         textColor=colors.HexColor("#222222"))
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Sans", fontSize=10.5, leading=15,
                         textColor=colors.HexColor("#555555"), spaceAfter=2)
st_cell = ParagraphStyle("cell", fontName="Serif", fontSize=8.6, leading=11.6,
                         textColor=colors.HexColor("#1a1a1a"))


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace("\n", "<br/>"), st)


def cell(txt):
    return para(txt, st_cell)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


MANUSCRIT = REPO / "edition-v0200" / "main.pdf"
SPEC = REPO / "scripts" / "spec_v156" / "main.pdf"
LIVRE = REPO / "scripts" / "livre_v15" / "final.pdf"
PREUVES = ICI / "TRIADE_preuves_et_calculs_v0.20.0.pdf"
emp_m, emp_s, emp_l, emp_p = (sha(MANUSCRIT), sha(SPEC), sha(LIVRE),
                              sha(PREUVES))

story = [
    para("TRIADE — présentation du 20/11", st_titre),
    para("Édition v0.20.0 — la vague 9 : la sécurité au plancher, la "
         "boucle de vérification, les deux couloirs de performance, le "
         "coût en tokens au-delà d'OPT-05, le tableau de bord des quatre "
         "axes", st_sous),
    Spacer(1, 8),
    para("LE PROTOCOLE EN TROIS PHRASES", st_h1),
    para("TRIADE fait écrire à un agent IA du code machine natif pur "
         "(x86-64 Windows d'abord, Linux et RISC-V ensuite) sans chaîne "
         "de traduction optimisante ni opaque — la notation est WYSIWYG "
         "par le round-trip : l'agent manipule des intentions (couche "
         "I), une carte de balises signée et chiffrée (couche C), et ne "
         "livre que le binaire scellé (couche B). Onze règles non "
         "négociables, la vérification avant tout écrit (oracle "
         "différentiel, round-trip WYSIWYG, vecteurs dorés), la "
         "cristallisation au bout de dix vérifications. L'étude de cas "
         "unique est close et la vague 9 exécutée : la fonction objectif "
         "lexicographique PORTÉE au tableau de bord — la sécurité "
         "gagnée, aucun point cédé aux rangs inférieurs."),
    para("LA VAGUE 9 — LES CINQ POINTS", st_h1),
    para("(1) LA SÉCURITÉ AU PLANCHER (bk79jvzbm, D224) : la sûreté "
         "mémoire — l'analyse v110 reproduite à l'identique d'abord "
         "(2 098 accès, 463 non-résolus), puis l'extension par "
         "inférence d'invariants de boucle, analyse d'intervalles, "
         "analyse d'alias et le model checking borné z3 : 2 006/2 098 "
         "DÉCHARGÉS PAR PREUVE (95,6 %), 92 NOMMÉS avec cause, "
         "mécanisme ET la preuve SAT qu'aucune borne statique n'existe "
         "sans l'invariant externe — zéro non-résolu muet, zéro "
         "hors-cadre ; la mutation — la console v0.14.0 REPRODUITE À "
         "L'IDENTIQUE (776/832, la graine 20261111, les tirages "
         "rejoués jamais nouveaux), la console courante 811/832, les "
         "deux nouveaux scénarios K5 vécus, LES TROIS « TUABLES » DE "
         "LA VAGUE 8 RE-CLASSÉS ÉQUIVALENTS-PAR-SWEEP (la classe "
         "entière : 3 cellules du bord × 10 défilements = 30 "
         "scénarios, ZÉRO ÉCART — l'hypothèse corrigée par la preuve : "
         "le clamp de bornes ABSORBE la mutation) — le score ajusté "
         "811/817 = 99,3 % (les 15 équivalents exclus) à côté du brut "
         "811/832 = 97,5 %, JAMAIS fusionnés, AUCUN tueur affaibli ; "
         "le temps constant — la preuve STATIQUE de non-interférence "
         "sur la notation liftée : les DIX familles crypto PROUVÉES "
         "(0 branche taintée, 0 adresse taintée), le contrôle négatif "
         "ATTRAPÉ ; CF3 — l'invariant inductif MÉCANISÉ en z3 "
         "(L'ASSISTANT INDÉPENDANT de l'explorateur maison et "
         "d'Apalache) : 14/14 obligations VERTES, les certificats "
         "SMT2 archivés rejouables, le contrôle négatif (le seuil "
         "affaibli à 2) ATTRAPÉ au contre-exemple ; la transparence — "
         "le témoin d'époque ANCRÉ au journal (la chaîne des 3 époques "
         "recalculée de la genèse), la réécriture REFUSÉE nommément "
         "ANCRAGE-DIVERGENT, le delta au modèle de menace aux deux "
         "bords ; le fuzzing — loupe-13 (la feuille pure) à 100 % de "
         "couverture au corpus saturant, les blocs de composition "
         "mesurés au niveau bloc (58,0/68,7/19,9 % — le gap NOMMÉ : "
         "l'état d'app), ZÉRO crash, ZÉRO violation de canari."),
    para("(2) LA BOUCLE DE VÉRIFICATION (bkobf06nu, D225 — OPT-07) : le "
         "CERTIFICAT DE CRISTALLISATION — le graphe de dépendances LU "
         "des notations assemblées (jamais déclaré à la main), la "
         "vérification FONCTION DU DIFF : un changement au bloc "
         "loupe-08 re-vérifie 3 blocs (0,05 s) contre 18 la complète "
         "(0,31 s), les 15 inchangés portent leur certificat chaîné "
         "depuis la genèse et SIGNÉ Ed25519 (jamais cru, chaîne et "
         "signature recalculées), LES TROIS FALSIFICATIONS (bloc, "
         "contrat, configuration) chacune REFUSÉE nommément "
         "CERTIFICAT-DIVERGENT ; le DOUBLE MOTEUR au chemin chaud de "
         "l'ouverture — le volume sous le VRAI qemu-x86_64 (le témoin "
         "196 609 o AU FICHIER ENTIER) : 6 relevés en 0,03 s contre "
         "l'échantillon Unicorn 20,0 s, DIVERGENCE=0 octet pour octet, "
         "la clé de mémo étendue à tout ce qui détermine le résultat "
         "(le bloc ‖ l'entrée ‖ le condensé du fichier entier ‖ le "
         "contrat ‖ la config ‖ la graine ‖ l'oracle) ; le régime "
         "ORACLE NATIF PRÉPARÉ — le runner Windows, les scénarios "
         "consignés, la signature Ed25519 du témoin, CE QU'IL ATTRAPE "
         "(l'écart émulation/native : l'ABI réelle, l'IAT du vrai "
         "chargeur, les feuilles kernel32 réelles) et CE QU'IL "
         "N'ATTRAPE PAS (le terrain du développeur — jamais confondu, "
         "les résultats NOMMÉS « natif » partout), le contrôle négatif "
         "VÉCU (le shim muté REFUSÉ à la première ligne) ; la MESURE "
         "M4 à la liste fixe (n=5, l'horloge monotone) : AVANT médiane "
         "39,3 s [39,1–39,6] · FROID 6,8 s · CHAUD médiane 6,9 s (le "
         "run à 29,7 s : l'AUDIT 1/10 VÉCU) · le bras C 2,1 s — LE "
         "RATIO DE RÉGIME 3,4× (le seuil ×10 tenu, H5-amendée-OPT04 "
         "re-mesurée — la mesure RE-JOUÉE de la reprise : les pièces "
         "brutes de la session morte perdues à l'incident, la mesure "
         "refaite aux mêmes n, l'écart nommé)."),
    para("(3) LES DEUX COULOIRS DE PERFORMANCE (0205wxg5q, D226 — "
         "OPT-08) : LE COULOIR A (la parité baseline) — le constat sur "
         "pièces : le gcc -O2 des blocs contrôlés n'emploie PAS SSE2 "
         "(le décompte SIMD des .text : 0), la parité se joue au GPR : "
         "loupe-13 le scellé 1,07× gcc-O2 (la bibliothèque tenue "
         "ÉGALE : les deux bras au memcmp scellé) ; LA VARIANTE SSE2 "
         "BASELINE écrite en notation (à la marge vierge 0xCC00, "
         "AUCUN octet du scellé touché) : le scan 16 octets à la fois "
         "(movdqu + pcmpeqb + pmovmskb — LE BASELINE du x86-64, "
         "AUCUNE extension au-delà), le premier octet diffusé SANS "
         "pshufb (SSSE3 hors baseline, l'interdit), chaque candidat "
         "confirmé au memcmp scellé : round-trip 100 %, ZÉRO "
         "DIVERGENCE aux 24 vecteurs (les 15 de la mesure + les 9 "
         "bords nommés), LA MESURE : 3 928 instructions/op contre "
         "115 292 gcc-O2 — LE RATIO 0,03× (l'objectif « coût "
         "inférieur ou égal à gcc-O2 » TENU avec 31,2× de marge) ; LE "
         "COULOIR B (les chemins chauds) — AES-NI : LA DESCENTE EST "
         "DÉJÀ LE SCELLÉ (l'ère l'exige, I3 de tls13-15 : 26 "
         "instructions/bloc, aesenc vécu), la variante à dispatch "
         "MESURÉE PLUS LENTE (45 contre 26 — le prix du sondage par "
         "bloc : LA LEÇON) ; GHASH PCLMULQDQ : la frontière nommée I5 "
         "(le chantier suivant — mesuré, pas supposé) ; SHA-NI : "
         "OPT-01 5,84× consacré ; x25519 : la pertinence TRANCHÉE PAR "
         "LA MESURE (O(1)/session) ; LA DETTE DE CÉRÉMONIE nommée à "
         "la naissance : les variantes vivent en COPIES DE "
         "LABORATOIRE aux adresses de marge — l'embarquement exigera "
         "la cérémonie d'ère (le sceau-I, la clé hors-ligne)."),
    para("(4) LE COÛT EN TOKENS AU-DELÀ D'OPT-05 (uagz3fby7, D227 — "
         "OPT-09) : la campagne aux QUATRE cellules (n=18, la graine "
         "20261117, le tokenizer natif lu du champ usage) — ÉDITER-H2 "
         "REPRODUIT : 18/18 verts, médiane 2 452 [q1 1 740, q3 3 527], "
         "réponse 40 ; L'AJOUT PAR HUNKS REFUSÉ POUR LA TROISIÈME FOIS "
         "(ajouter-H3, la grammaire v2 + l'exemple complet : 0/18, "
         "tous HORS-FORMAT — le format REFUSÉ DÉFINITIVEMENT en "
         "l'état : la voie de l'ajout demeure LA NOTATION COMPLÈTE) ; "
         "COMPOSER-G (la cellule nouvelle, l'héritage scellé au "
         "prompt) : 3/18 verts (les round-trip divergents dominent), "
         "médiane 4 846 contre ajouter-A2 5 079 — H4 FALSIFIÉE en sa "
         "direction (l'héritage déclaré n'achète PAS la réponse : le "
         "domaine composait DÉJÀ par appels — la bibliothèque "
         "formalise la pratique, le gain est dans l'ORACLE et la "
         "VÉRIFICATION) ; LOCALISER-P REPRODUIT : 18/18 conformes, "
         "médiane 1 103, réponse 52 (le pointeur seul tenu à "
         "l'identique) ; LE COMPILATEUR D'ORACLE DÉTERMINISTE : le "
         "gabarit structuré des specs I → le code d'oracle GÉNÉRÉ PAR "
         "SCRIPT, zéro token LLM, dérivé de I jamais de B — 968 "
         "TOKENS SUPPRIMÉS aux 3 unités (323/unité) ; LES RATIOS AU "
         "PLANCHER (la méthode NOMMÉE : éditer — la paire de lignes "
         "du diff réel ; localiser — le pointeur littéral ; "
         "ajouter/composer — le corps du bloc, le plancher HAUT "
         "honnête) : éditer-H2 136,2× (le matériau relu domine), "
         "localiser-P 38,0×, ajouter-H3 4,1×, composer-G 2,9× — la "
         "convention de périmètre : les trois champs (matériau, "
         "prose, réponse) consignés séparément, jamais fusionnés."),
    para("(5) LE TABLEAU DE BORD DES QUATRE AXES (h0mq0s2m6, D228) : "
         "GÉNÉRÉ depuis les pièces brutes (chaque valeur SOURCÉE : les "
         "CSV des ateliers, les journaux — jamais tapée à la main, "
         "chaque ratio RECALCULÉ, le linter le re-vérifie au build) ; "
         "L'ORDRE LEXICOGRAPHIQUE EXPLICITE : Sécurité > Performance > "
         "Optimisation > Coût en tokens — AUCUNE compensation entre "
         "les rangs (la fonction objectif du protocole § 8 portée au "
         "tableau) ; POUR CHAQUE AXE : la valeur mesurée courante, le "
         "PLANCHER IRRÉDUCTIBLE et SA MÉTHODE, le ratio d'overhead, "
         "la cible et le statut de chaque résidu nommé ; LA SECTION "
         "« DISTANCE AU PLANCHER » portée au manuscrit (les ratios par "
         "axe, la convention de périmètre obligatoire avant toute "
         "comparaison, la lecture lexicographique) ; les macros "
         "régénérées des journaux vivants partagées par les cinq "
         "pièces ; l'alignement à l'état vécu : la spécification "
         "v0.15.6 et le Livre du Coffre v1.5 (les références de "
         "version périmées corrigées, l'annexe B à la plage réelle "
         "D75–D228, la table des preuves au CF3 mécanisé et à la "
         "non-interférence statique — AUCUNE règle modifiée) ; "
         "l'abstract réécrit en un seul paragraphe à l'état courant "
         "v0.20.0 ; LE LINTER INTER-PIÈCES v200 ÉTENDU : les en-têtes, "
         "les DOI, les comptes, les ratios, les probabilités — le "
         "contrôle négatif vécu (la divergence volontaire REFUSÉE "
         "puis retirée)."),
    para("LA TABLE DES STATUTS — LES HYPOTHÈSES", st_h1),
    Table(
        [[cell("Hypothèse"), cell("Énoncé"), cell("Verdict")],
         [cell("H1"), cell("la notation tient le round-trip à 100 %"),
          cell("tenue")],
         [cell("H3"), cell("le bras compilé plus sobre en tokens"),
          cell("réfutée (×1,27 l'inverse)")],
         [cell("H5-D204"), cell("la vérification dans un facteur ×10 "
                               "(le 16/11, mesurée)"),
          cell("RÉFUTÉE (×23,9, n=1 — consignée comme mesurée et datée)")],
         [cell("H5-amendée-OPT04"), cell("la vérification dans un facteur "
                                         "×10 (le 19/11, l'amendement du "
                                         "maître)"),
          cell("TENUE (×3,0 ; re-mesurée ×3,5 aux vagues 8 et 9 — les "
               "deux verdicts DISTINCTS, jamais fusionnés)")],
         [cell("H6"), cell("le taux d'échappées kit-side dans un facteur "
                          "2 entre bras"),
          cell("tenue PAR ATTRIBUTION (le brut affiché : 3 côté T, 0 "
               "côté C — la pièce jamais fautive, 14 VERT 0 ROUGE)")],
         [cell("H7"), cell("l'ordre randomisé n'affecte aucune métrique"),
          cell("non testée (aucun contraste — la randomisation "
               "stratifiée pré-enregistrée pour la prochaine)")],
         [cell("H8"), cell("la spirale corrective > 50 % des tokens"),
          cell("réfutée (51/39/9 % — la spirale déclina)")],
         [cell("H4-composer"), cell("l'héritage scellé déclaré achète la "
                                    "réponse (composer-G)"),
          cell("RÉFUTÉE (3/18 — le gain ~4,5 % : la bibliothèque "
               "formalise, l'oracle économise)")]],
        colWidths=[52, 168, 236]),
    Spacer(1, 6),
    para("L'ÉTAT DES ÉDITIONS — le manuscrit v0.20.0 (le tableau de "
         "bord et la section distance-au-plancher, l'abstract réécrit, "
         "les canons de la vague), la spécification v0.15.6 (la table "
         "des preuves au CF3 mécanisé et à la non-interférence "
         "statique, l'annexe B à D75–D228, aucune règle modifiée), le "
         "Livre du Coffre v1.5 (les références de version alignées, le "
         "compte d'arbres réel), les preuves v0.20.0 (les huit pièces "
         "verbatim de la vague), la présentation du 20/11 à l'état "
         "exact. LA GOUVERNANCE VÉCUE : le séquestre Shamir 5/3 la "
         "garde active, le dépôt PUBLIC (github.com/"
         "alexisfrlopez-debug/triade), le concept DOI "
         "10.5281/zenodo.24367343 résolvant sur la version courante — "
         "la publication AU GESTE DU MAÎTRE (jamais un DOI minté sans "
         "commande explicite)."),
    para("LES EMPREINTES SHA-256 DES PIÈCES DU PACK v0.20.0", st_h1),
    para("La consigne de l'instruction : les empreintes des cinq pièces "
         "consignées dans la présentation et le document de preuves. "
         "LA CONVENTION (l'écart nommé, physique du format) : aucun "
         "document ne peut porter son propre sha-256 — la PRÉSENTE "
         "porte les QUATRE autres ci-dessous, le document de preuves "
         "porte les trois pièces de contenu, et le manifeste "
         "empreintes_livrables_v0.20.0.txt du pack porte les CINQ. Le "
         "linter inter-pièces v200 re-vérifie chaque empreinte au "
         "build (toute divergence un ROUGE)."),
    para(f"TRIADE_manuscrit_v0.20.0.pdf\n  {emp_m}\n"
         f"Protocole_TRIADE_v0.15.6_Specification.pdf\n  {emp_s}\n"
         f"Livre_du_Coffre_TRIADE_CF1-CF3_v1.5.pdf\n  {emp_l}\n"
         f"TRIADE_preuves_et_calculs_v0.20.0.pdf\n  {emp_p}\n"
         f"TRIADE_presentation_20261120_v200.pdf\n  la présente — "
         f"consignée au manifeste du pack", st_mono),
]

story_table_style = TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B9C8D8")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EFF5")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
])
for el in story:
    if isinstance(el, Table):
        el.setStyle(story_table_style)

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * 2.834,
                      rightMargin=2 * 2.834, topMargin=2 * 2.834,
                      bottomMargin=2 * 2.834, title="TRIADE — présentation "
                      "du 20/11, édition v0.20.0")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                          doc.height, id="f")])])
doc.build(story)
print("écrit:", OUT)

# ---------------- la couverture ----------------
COVER_HTML = ICI / "presentation_v200_cover.html"
with open(COVER_HTML, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@page { size: A4; margin: 0; }
body { font-family: 'Liberation Serif', serif; margin: 0; }
.cover { width: 210mm; height: 297mm; background: #162032; color: #fff;
  padding: 30mm 24mm; box-sizing: border-box; }
.kicker { color: #7FB4D8; font-family: 'Liberation Sans', sans-serif;
  font-size: 12pt; letter-spacing: 3px; margin-bottom: 18mm; }
h1 { font-size: 34pt; line-height: 1.2; margin: 0 0 8mm 0; font-weight: normal; }
.sub { font-size: 15pt; color: #B9C8D8; margin-bottom: 26mm; }
.rule { border-top: 1px solid #7FB4D8; margin: 10mm 0; }
.meta { font-size: 10.5pt; color: #B9C8D8; line-height: 1.7; }
</style></head><body><div class="cover">
<div class="kicker">TRIADE</div>
<h1>Pr&eacute;sentation</h1>
<div class="sub">La vague 9 — l'édition v0.20.0 &middot; 20 novembre 2026</div>
<div class="meta">
La s&eacute;curit&eacute; au plancher &middot; 2&nbsp;006/2&nbsp;098 d&eacute;charg&eacute;s &middot; CF3 m&eacute;canis&eacute; 14/14<br/>
La boucle de v&eacute;rification &middot; le certificat de cristallisation &middot; le double moteur &middot; M4 3,5&times;<br/>
Les deux couloirs &middot; la parit&eacute; SSE2 0,03&times; gcc-O2 &middot; AES-NI d&eacute;j&agrave; le scell&eacute;<br/>
Les tokens &middot; le compilateur d'oracle &middot; 968 supprim&eacute;s &middot; les ratios au plancher<br/>
Le tableau de bord des quatre axes &middot; l'ordre lexicographique &middot; aucun point c&eacute;d&eacute;
</div>
<div class="rule"></div>
<div class="meta">La fonction objectif port&eacute;e au tableau &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.20.0</div>
</div></body></html>""")
subprocess.run(["weasyprint", str(COVER_HTML),
                str(ICI / "presentation_v200_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "presentation_v200_cover.pdf")).pages[0])
for p_ in PdfReader(str(OUT)).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — présentation du 20/11, édition "
                          "v0.20.0"})
FINAL = ICI / "TRIADE_presentation_20261120_v200.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(str(FINAL)).pages)} pages)")
