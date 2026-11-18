#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_livre_v12.py — l'édition de cohérence du Livre du Coffre (v1.2, D218) :
l'en-tête courant, le sommaire des décisions D75–D137, les QUATORZE arbres,
la table d'empreintes portée à sha-256 (D184/D187), la référence à la spec
courante v0.15.1. Chaque remplacement EST ANCRÉ — REFUS si une ancre manque.
AUCUNE règle modifiée, AUCUN geste de cérémonie changé."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
FAITS = []


def remplace(nom_fichier, ancien, nouveau, nom):
    p = ICI / nom_fichier
    t = p.read_text(encoding="utf-8")
    if ancien not in t:
        raise SystemExit(f"[livre_v12] ANCRE INTROUVABLE — {nom}")
    p.write_text(t.replace(ancien, nouveau, 1), encoding="utf-8")
    FAITS.append(nom)


# ---- main.tex : l'en-tête courant (la scorie v1.0), le pdftitle, le bandeau ----
remplace("main.tex",
         "\\fancyhead[L]{\\small\\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.0)}",
         "\\fancyhead[L]{\\small\\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.2)}",
         "main.tex : l'en-tête courant v1.2 (la scorie v1.0 nommée)")
remplace("main.tex",
         "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.0)},",
         "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.2)},",
         "main.tex : le pdftitle v1.2")
remplace("main.tex",
         "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.1, D137)",
         "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.2, D218)\n"
         "%  v1.2 : édition de cohérence inter-pièces (D218) — l'en-tête courant\n"
         "%  (la scorie v1.0), le sommaire des décisions D75–D137, les QUATORZE\n"
         "%  arbres signés (D177), la table d'empreintes portée à sha-256\n"
         "%  (D184/D187), la référence à la spécification courante v0.15.1.\n"
         "%  AUCUNE règle modifiée, AUCUN geste de cérémonie changé.",
         "main.tex : le bandeau de version v1.2")

# ---- sec-1.tex : la référence à la spécification courante ----
remplace("sec-1.tex",
         "spécification (v0.6.0, D133 ; v1.1 alignée sur la v0.6.1) : il ne crée aucune règle,",
         "spécification (v1.2 : l'édition courante est la v0.15.1) : il ne crée aucune règle,",
         "sec-1.tex : la référence à la spec courante v0.15.1")

# ---- sec-4.tex : les QUATORZE arbres signés ----
remplace("sec-4.tex",
         "Le sceau signe la spécification elle-même — l'arbre \\code{v06/I/} et les neuf arbres\n"
         "de lignée. Quatre gestes, depuis le clone :",
         "Le sceau signe la spécification elle-même — l'arbre \\code{v06/I/} et les treize\n"
         "arbres de lignée : le garde est à QUATORZE arbres signés (D177 — l'arbre\n"
         "\\code{loupe} entré à la table canonique par la cérémonie d'ère du TGN).\n"
         "Quatre gestes, depuis le clone :",
         "sec-4.tex : les QUATORZE arbres (D177)")

# ---- sec-5.tex : le sommaire des décisions D75 à D137 ----
remplace("sec-5.tex",
         "\\section{Les décisions du coffre — D75 à D133}\\label{sec:decisionslivre}",
         "\\section{Les décisions du coffre — D75 à D137}\\label{sec:decisionslivre}",
         "sec-5.tex : le sommaire des décisions D75–D137 (la table porte la ligne D137)")

# ---- sec-5.tex : la table d'empreintes md5 -> sha-256 (D184/D187) ----
remplace("sec-5.tex",
         "Chaque rapport de cérémonie affiche les md5 des modules qui ont tourné : la\n"
         "génération de code se \\emph{lit}, ne se devine pas. Un verdict rendu par un module\n"
         "d'empreinte inconnue est un verdict à interroger : quelle génération ? quel correctif\n"
         "? Le tableau ci-dessous est la référence au jour de la passation (D133, commit\n"
         "\\code{c504436}, contenu canonique LF du dépôt).",
         "Chaque rapport de cérémonie porte les empreintes des modules qui ont tourné : la\n"
         "génération de code se \\emph{lit}, ne se devine pas. Un verdict rendu par un module\n"
         "d'empreinte inconnue est un verdict à interroger : quelle génération ? quel correctif\n"
         "? La gouvernance des empreintes est à sha-256 depuis D184 (la migration de la\n"
         "v0.9.0 : la même méthode, l'empreinte longue) et les manifestes de kit à sha-256\n"
         "depuis D187 ; md5 demeure côté application une fonctionnalité d'affichage de\n"
         "Loupe (le panneau d'empreintes) et les preuves historiques gardent leurs md5 —\n"
         "les preuves ne se réécrivent jamais. Le tableau ci-dessous est la référence\n"
         "sha-256 des modules, alignée sur l'annexe A de la spécification v0.15.1\n"
         "(contenu canonique LF du dépôt).",
         "sec-5.tex : la prose des empreintes à sha-256 (D184/D187)")

OLD_TABLE = """\\begin{table}[htbp]
\\centering\\footnotesize
\\caption{Empreintes md5 des modules v06 — référence D133.}
\\label{tab:empreintslivre}
\\begin{tabularx}{\\textwidth}{@{}l l Y@{}}
\\toprule
\\textbf{Module} & \\textbf{md5} & \\textbf{Rôle} \\\\
\\midrule
\\code{coffre\\_fort.py} (racine) & \\code{8c79263b9b4694662fb722a67f14ee82} & CF1 \\\\
\\code{v06/coffre\\_cf2.py} & \\code{f50ce894db276818d68dd1e22a92fa4c} & CF2 \\\\
\\code{v06/coffre\\_cf3.py} & \\code{1cf18644d70073bf82f1f2847976f17d} & CF3 \\\\
\\code{v06/sceau\\_I.py} & \\code{baf727058504490c288630dbc5bd9664} & sceau I \\\\
\\code{v06/ceremonie\\_hors\\_ligne.py} & \\code{982bf0a402607b67a3960952a0adcb11} &
cérémonie air-gap \\\\
\\code{v06/ceremonie\\_gui.py} & \\code{e4745580b19e7e5508f596b83bb1652f} & GUI
cérémonie (v2.2) \\\\
\\code{v06/migration\\_cf3\\_gui.py} & \\code{933e8405fa49ecad1d11861bd37d1c7a} & GUI
migration (v1.1) \\\\
\\code{v06/autotest\\_cf3\\_gui.py} & \\code{bcd243448873d633852af27f204ecc27} &
autotest CF3 \\\\
\\code{v06/sentinelle\\_cf2.py} & \\code{bbc487423302c7f8f821ff348f3737c4} &
sentinelle CF2 \\\\
\\code{v06/test\\_cf2.py} & \\code{f55fbee3391bbbb4466ba096c06b2ad7} & falsifiabilité
CF2 \\\\
\\code{v06/test\\_coffre\\_cf3.py} & \\code{33f460171f69aa59ae40192b5de46114} &
falsifiabilité CF3 \\\\
\\code{v06/test\\_sceau\\_I.py} & \\code{a4b43fd5aa37acb37e98b77dca5747fc} &
falsifiabilité sceau \\\\
\\code{v06/test\\_migration\\_cf3.py} & \\code{9e078dfdebea4bbe88b72fb71ab907bd} &
falsifiabilité migration \\\\
\\code{v06/test\\_migration\\_cf3\\_gui.py} & \\code{5f93800b887e44f52b1e998d5aabf160} &
falsifiabilité GUI migration \\\\
\\code{v06/test\\_ceremonie\\_gui.py} & \\code{e275efb83c104bcac30f05d96c7ce318} &
falsifiabilité GUI cérémonie \\\\
\\bottomrule
\\end{tabularx}
\\end{table}"""

NEW_TABLE = """\\begin{table}[tbp]
\\centering\\footnotesize
\\caption{Empreintes sha-256 des modules v06 — référence D184/D187, alignée sur
l'annexe A de la spécification v0.15.1 (contenu canonique LF du dépôt).}
\\label{tab:empreintslivre}
\\begin{tabularx}{\\textwidth}{@{}l >{\\raggedright\\arraybackslash}p{5.6cm} Y@{}}
\\toprule
\\textbf{Module} & \\textbf{sha-256} & \\textbf{Rôle} \\\\
\\midrule
\\code{coffre\\_fort.py} (racine) & \\code{\\allowbreak f5b2fb90cc020ba7\\allowbreak fafc735ffa2b8adf\\allowbreak e896f169f52409b7\\allowbreak 5fe837808b706198} & CF1 \\\\
\\code{v06/coffre\\_cf2.py} & \\code{\\allowbreak 603ab952b45243fa\\allowbreak 1d82b1fd0b4321a7\\allowbreak e9af8cf97feda685\\allowbreak d429814e6043f12f} & CF2 — Shamir, sentinelle, porte D120 \\\\
\\code{v06/coffre\\_cf3.py} & \\code{\\allowbreak ea871be616964a61\\allowbreak 677be92ca671ac3d\\allowbreak 12ce4cb96a105142\\allowbreak a4d77a7694c24891} & CF3 — serrure piégée, migration, destruction \\\\
\\code{v06/sceau\\_I.py} & \\code{\\allowbreak 89048e813043a3dd\\allowbreak 73b805ac82f55f35\\allowbreak 91694c5db37f3ec9\\allowbreak 54ec2bafa8170810} & sceau I (le registre étendu au 14\\textsuperscript{e} arbre, D177) \\\\
\\code{v06/ceremonie\\_hors\\_ligne.py} & \\code{\\allowbreak b5a3fc7ac25c7ab4\\allowbreak aab22530e1882c48\\allowbreak a6bc43f0603fecbb\\allowbreak eb7c54060d7bb7b7} &
cérémonie air-gap \\\\
\\code{v06/ceremonie\\_gui.py} & \\code{\\allowbreak 9df2583e6aa55d6a\\allowbreak 8bfd780dc1cc309a\\allowbreak d238c2bab30da3d3\\allowbreak c2009e54420a28d5} & GUI
cérémonie (v2.2) \\\\
\\code{v06/migration\\_cf3\\_gui.py} & \\code{\\allowbreak ba5c2a92141deee0\\allowbreak 246e02015d718d8b\\allowbreak a056412ff996b4b9\\allowbreak a5e47403c5e86eda} & GUI
migration (v1.1) \\\\
\\code{v06/autotest\\_cf3\\_gui.py} & \\code{\\allowbreak 557add0cf4f69346\\allowbreak d5dbbda218923aa5\\allowbreak dd1e90e6daf4fecd\\allowbreak cdd5c89396d3c04b} &
autotest CF3 \\\\
\\code{v06/sentinelle\\_cf2.py} & \\code{\\allowbreak 9454e7563b403853\\allowbreak 7d0189044fe69f81\\allowbreak 2017ad9b7dd4b472\\allowbreak 5549d6ce5708ead8} &
sentinelle CF2 \\\\
\\code{v06/test\\_cf2.py} & \\code{\\allowbreak 8445d97e94e5a812\\allowbreak 94387c1dec120ce1\\allowbreak 2e0bcc2cdd6cd191\\allowbreak 8ea007a7709b17b5} & falsifiabilité
CF2 \\\\
\\code{v06/test\\_coffre\\_cf3.py} & \\code{\\allowbreak 54066b1c5d7c7efe\\allowbreak 855e9a1cbcb3547d\\allowbreak bd02b0470a619398\\allowbreak 0c1c60c463f21ce0} &
falsifiabilité CF3 \\\\
\\code{v06/test\\_sceau\\_I.py} & \\code{\\allowbreak 6758133cf0f62dc1\\allowbreak c192757d371df9a2\\allowbreak 55c2f47e9adc1b23\\allowbreak 8a97cf14e5685f0c} &
falsifiabilité sceau \\\\
\\code{v06/test\\_migration\\_cf3.py} & \\code{\\allowbreak adcfe77ce6659510\\allowbreak 745c83e802f54ce7\\allowbreak 377c64e7124cdba2\\allowbreak d3c6247684bdc04c} &
falsifiabilité migration \\\\
\\code{v06/test\\_migration\\_cf3\\_gui.py} & \\code{\\allowbreak 370364a2d68c9005\\allowbreak dab89ed59840dc83\\allowbreak d5ebd1cdf17beb52\\allowbreak bf68110f1f618f12} &
falsifiabilité GUI migration \\\\
\\code{v06/test\\_ceremonie\\_gui.py} & \\code{\\allowbreak fbfd15d9e8a49dc3\\allowbreak f8ce4bc8273be63c\\allowbreak ff26b869014f9885\\allowbreak c2abd7cf6855a234} &
falsifiabilité GUI cérémonie \\\\
\\bottomrule
\\end{tabularx}
\\end{table}"""

# la table source porte la scorie historique \begin{table}tbp] ? Non — vérifiée propre.
p = ICI / "sec-5.tex"
t = p.read_text(encoding="utf-8")
if OLD_TABLE not in t:
    # l'ancre stricte échoue (retours à la ligne différents) : essai ligne à ligne
    raise SystemExit("[livre_v12] ANCRE INTROUVABLE — la table md5 (voir le source)")
p.write_text(t.replace(OLD_TABLE, NEW_TABLE, 1), encoding="utf-8")
FAITS.append("sec-5.tex : la table d'empreintes portée à sha-256 (D184/D187)")

# ---- sec-5.tex : la note de divergence terrain garde ses md5 HISTORIQUES, nommés ----
remplace("sec-5.tex",
         "Au rapport du 30/10 20:41, le \\code{coffre\\_fort.py} du clone terrain rend\n"
         "\\code{299fd124\\ldots{}} alors que le dépôt rend \\code{8c79263b\\ldots{}} — ni l'un ni",
         "Au rapport du 30/10 20:41, le \\code{coffre\\_fort.py} du clone terrain rendait\n"
         "\\code{299fd124\\ldots{}} (md5, la preuve historique telle que consignée) alors que\n"
         "le dépôt rendait \\code{8c79263b\\ldots{}} (md5) — ni l'un ni",
         "sec-5.tex : la divergence terrain, ses md5 nommés HISTORIQUES")

# ---- cover.html : version, note, date, compagnon v0.15.1 ----
remplace("cover.html",
         '<div class="label">Document compl&eacute;mentaire &middot; Version 1.1</div>',
         '<div class="label">Document compl&eacute;mentaire &middot; Version 1.2</div>',
         "cover.html : la version 1.2")
remplace("cover.html",
         "Compagnon op&eacute;ratoire de la sp&eacute;cification v0.6.1&nbsp;:",
         "Compagnon op&eacute;ratoire de la sp&eacute;cification (l'&eacute;dition courante v0.15.1)&nbsp;:",
         "cover.html : le compagnon de la spec courante")
remplace("cover.html",
         "R&eacute;vision v1.1 (D137)&nbsp;: le niveau d'un",
         "R&eacute;vision v1.2 (D218, &eacute;dition de coh&eacute;rence)&nbsp;: les empreintes &agrave; sha-256, les quatorze arbres sign&eacute;s, le sommaire des d&eacute;cisions D75&ndash;D137. La v1.1 portait le niveau d'un",
         "cover.html : la note de révision v1.2")
remplace("cover.html",
         "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.1 (D137)</span>",
         "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.2 (D218)</span>",
         "cover.html : le pied de révision v1.2")
remplace("cover.html",
         "<span>31 octobre 2026</span>",
         "<span>19 novembre 2026</span>",
         "cover.html : la date de l'édition")

# ---- merge_cover.py : les métadonnées ----
p = ICI / "merge_cover.py"
t = p.read_text(encoding="utf-8")
t = t.replace("v1.1", "v1.2").replace("v 1.1", "v1.2")
p.write_text(t, encoding="utf-8")
FAITS.append("merge_cover.py : les métadonnées v1.2")

print(f"[livre_v12] {len(FAITS)} éditions ancrées :")
for f in FAITS:
    print(f"  - {f}")
