#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_h66o54pjd.py — LA PURGE v13 ET LES MÉTADONNÉES v1.7 / v0.15.8
(h66o54pjd, la vague 13) : le recensement EXHAUSTIF des gestes
prescriptifs de remise de phrase, chaque occurrence corrigée vers LA
GARDE ACTIVE D223 (le séquestre 5/3, la reconstitution à froid de TROIS
parts, la phrase en AUCUN dépôt) ou bornée en HISTOIRE DATÉE ; les
PHRASES CASSÉES réparées par RÉÉCRITURE COMPLÈTE des paragraphes (jamais
par remplacement de sous-chaînes) ; les métadonnées v1.7 / v0.15.8.

LA MÉTHODE : remplacements ancrés — REFUS si une ancre manque (jamais un
remplacement sournois). Les pièces historiques datées demeurent.

AUCUN coffre réel, aucune phrase réelle (D105) — du texte seul."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
LIVRE = REPO / "scripts" / "livre_v17"
SPEC = REPO / "scripts" / "spec_v158"
PROTO = REPO / "docs" / "PROTOCOLE_TRIADE.md"
CARTE = REPO / "docs" / "FORMAT_CARTE.md"

R = []


def remplace(chemin: pathlib.Path, ancien: str, nouveau: str, nom: str):
    t = chemin.read_text(encoding="utf-8")
    if ancien not in t:
        print(f"ANCRE MANQUANTE ({chemin.name}) : {nom}")
        sys.exit(2)
    if t.count(ancien) != 1:
        print(f"ANCRE AMBIGUE {t.count(ancien)}x ({chemin.name}) : {nom}")
        sys.exit(2)
    chemin.write_text(t.replace(ancien, nouveau), encoding="utf-8")
    R.append(f"{chemin.name} : {nom}")


# ===========================================================================
# (A) LA SPEC v0.15.8 — les cibles prescriptives nommées
# ===========================================================================
def patcher_spec():
    # (a) LE TABLEAU 14 CF1 (sec-cf.tex:373-374) — « garde durable de la
    #     phrase (D81) » au rang de CE QUI VIENT AVEC un coffre neuf : la
    #     garde est l'ARBITRAGE du développeur (D137), la garde ACTIVE
    #     D223 (le séquestre à reconstitution à froid)
    remplace(
        SPEC / "sec-cf.tex",
        "CF1 & \\code{coffre\\_fort.py init} & conteneur chiffré à phrase (D75) ; garde durable\nde la phrase (D81) ; relève simple \\\\",
        "CF1 & \\code{coffre\\_fort.py init} & conteneur chiffré à phrase (D75) ; la garde\nde la phrase à l'arbitrage du développeur (D137 — la garde active\nD223 : le séquestre à seuil, la reconstitution à froid de trois\nparts, la phrase en AUCUN dépôt ; l'histoire D81 datée du 4 au\n19 novembre 2026) ; relève simple \\\\",
        "Tableau 14 CF1 — la garde active D223")

    # (b) LE §12.5 (sec-cf.tex:403-406) — l'exigence normative « CF1 — la
    #     garde durable de la phrase » : la garantie de niveau CF1 est la
    #     garde de la phrase SELON L'ARBITRAGE, la D223 la forme vécue
    remplace(
        SPEC / "sec-cf.tex",
        "par niveau : CF1 — la garde durable de la phrase ; CF2 — les T copies hors-ligne et\nla liste blanche ; CF3 — le média du piège (sans S\\_piège, le déverrouillage est\n\\emph{impossible}, pas seulement refusé) et la discipline du sachet",
        "par niveau : CF1 — la garde de la phrase à l'arbitrage du développeur (D137 ;\nla garde active D223 : la reconstitution à froid de trois parts du\nséquestre, la phrase en AUCUN dépôt — le refus nommé de l'écriture\nde dépôt) ; CF2 — les T copies hors-ligne et\nla liste blanche ; CF3 — le média du piège (sans S\\_piège, le déverrouillage est\n\\emph{impossible}, pas seulement refusé) et la discipline du sachet",
        "§12.5 — l'exigence CF1 à la garde active")

    # (c) LE §14.3 (sec-d.tex:82-84) — LE SPLICE : le paragraphe du
    #     conteneur porte le fragment « la phrase ne vit plus au … racine
    #     du coffre Drive, AVANT toute autre action » (la coupure de la
    #     passe vague 12) — RÉÉCRITURE COMPLÈTE du membre de phrase
    remplace(
        SPEC / "sec-d.tex",
        "phrase de contrôle sous garde durable (D81, AMENDÉE PAR D223 — le séquestre chiffré\nD183 est la garde VÉCUE depuis le 19 novembre 2026 : la phrase ne vit plus au\nracine du coffre Drive, AVANT toute autre action), Argon2id aux",
        "phrase de contrôle sous séquestre à seuil (D183/D223, la garde VÉCUE\ndepuis le 19 novembre 2026 : la phrase répartie en CINQ parts à seuil\nTROIS, AUCUNE phrase en clair au dépôt ni au coffre Drive — la\ncérémonie de reconstitution à froid de trois parts est l'unique voie,\nle refus nommé D223 garde la ligne ; l'histoire D81 — la phrase au\nfichier-remise — est datée du 4 au 19 novembre 2026), Argon2id aux",
        "§14.3 — le splice réparé par réécriture complète")

    # (d) LE §sec-a.tex:328-340 — l'énoncé PÉRIMÉ « le coffre réel du
    #     développeur DEMEURE à la garde D81 » : l'état a changé (D220/
    #     D223) — le séquestre EST VÉCU, le dépôt PUBLIC
    remplace(
        SPEC / "sec-a.tex",
        "décision D183 ; le coffre réel du développeur DEMEURE à la garde D81 —\naucune clé touchée, aucun conteneur réécrit, la proposition attend le\ngeste du développeur.",
        "décision D183 ; le coffre réel du développeur EST PASSÉ au séquestre\nà seuil le 19 novembre 2026 (D220/D223 : la cérémonie vécue, la\nphrase répartie, le dépôt passé public — la matrice de visibilité\nD219 honorée) — l'énoncé d'époque (« demeure à la garde D81 ») est\nl'histoire datée du document, jamais l'état courant.",
        "sec-a — l'énoncé périmé porté à l'état courant")

    # (e) LE TABLEAU DES GARDES (sec-d.tex:440-443) — la rangée D81 : la
    #     colonne « garde » porte le fichier-remise au présent : bornée en
    #     HISTOIRE DATÉE
    remplace(
        SPEC / "sec-d.tex",
        "\\code{PHRASE-CONTROLE-COFFRE.txt} au dépôt (git, GitHub, miroir Drive) et au racine du\ncoffre Drive, AVANT toute autre action ; le fichier est la remise & modifié",
        "\\code{PHRASE-CONTROLE-COFFRE.txt} au dépôt et au racine du coffre\nDrive — HISTOIRE DATÉE (D81, du 4 au 19 novembre 2026, amendée\nD223 : la phrase ne vit plus en AUCUN dépôt, la reconstitution à\nfroid de trois parts est la garde) & modifié",
        "le tableau des gardes — la rangée D81 bornée en histoire datée")

    # (f) D236 PORTÉ À L'ANNEXE B (sec-d.tex:1551, la plage étendue) — la
    #     décision manquante au registre de l'annexe
    t = (SPEC / "sec-d.tex").read_text(encoding="utf-8")
    ancre = "D235 &"
    if ancre in t and "D236 &" not in t:
        # la ligne D236 insérée après D235 (la plage réelle D75–D25x)
        lignes = t.split("\n")
        for k, l in enumerate(lignes):
            if l.startswith("D235 &"):
                lignes.insert(k + 1, l.replace(
                    "D235 &", "D236 &", 1)[:0] + "D236 & La marge vierge "
                    "consacrée (les variantes à la marge 0xC000-0xEFFF ne "
                    "touchent JAMAIS les scellés) & les corridors SIMD, la "
                    "porteuse, le GHASH — la vague 13 au rebord \\\\")
                break
        (SPEC / "sec-d.tex").write_text("\n".join(lignes),
                                        encoding="utf-8")
        R.append("sec-d.tex : D236 porté à l'annexe B")
    else:
        print(f"[constat] D236 {'déjà' if 'D236 &' in t else 'ancre D235 absente'}"
              " — la plage nommée au rapport")


# ===========================================================================
# (B) LE LIVRE v1.7 — les phrases cassées RÉÉCRITES + les métadonnées
# ===========================================================================
def patcher_livre():
    # (i) LE §7.5 (sec-4.tex) — LE SPLICE « tant que… depuis que… » : le
    #     paragraphe LES FRONTIÈRES porte DEUX fragments contradictoires
    #     cousus (la passe vague 12) — RÉÉCRITURE COMPLÈTE
    remplace(
        LIVRE / "sec-4.tex",
        "\\textbf{LES FRONTIÈRES} : le laboratoire n'exécute \\emph{jamais} la\ncérémonie sur la phrase réelle (D87) ; l'outil ne supprime \\emph{jamais}\nrien (le retrait est humain, listé) ; le coffre réel demeure intact tant\nque la cérémonie n'est pas vécue — et \\textbf{le dépôt est PASSÉ PUBLIC}\ndepuis qu'elle l'est (D220/D223, la matrice honorée : public + Zenodo)\ntant qu'elle ne l'est pas et que la rotation n'est pas vérifiée : public +\nZenodo seulement après (la matrice de visibilité du kit, D219). Le kit",
        "\\textbf{LES FRONTIÈRES} : le laboratoire n'exécute \\emph{jamais} la\n\\newpage cérémonie sur la phrase réelle (D87) ; l'outil ne supprime \\emph{jamais}\nrien (le retrait est humain, listé). La cérémonie de séquestre A ÉTÉ\nVÉCUE le 19 novembre 2026 : depuis ce jour la garde active est le\nséquestre 5/3 (la reconstitution à froid de trois parts, la phrase en\nAUCUN dépôt — D223) et \\textbf{le dépôt est PASSÉ PUBLIC}\n(D220/D223, la matrice de visibilité D219 honorée : public + Zenodo,\nla rotation vérifiée AVANT le passage). Avant la cérémonie, le dépôt\ndemeurait privé et le coffre intact : les DEUX états sont datés, le\nprésent énonce le second. Le kit",
        "§7.5 — le splice « tant que… depuis que… » réécrit")

    # (ii) LE §8.2 ITEM 7 (sec-4.tex) — « tant qu'elle est VÉCUE » : le
    #      membre fautif (la cérémonie N'EST PLUS au commandement, elle
    #      EST VÉCUE) — RÉÉCRITURE COMPLÈTE de l'item
    remplace(
        LIVRE / "sec-4.tex",
        "\\item \\textbf{Le séquestre de la phrase (D183, préparé D219)} : au\ncommandement — la cérémonie § \\ref{sec:cerd183} (le kit au dépôt) ; tant\nqu'elle est VÉCUE, la garde active est le séquestre 5/3 et le dépôt est\nPUBLIC (D220) — l'état vécu acté par D223.",
        "\\item \\textbf{Le séquestre de la phrase (D183/D223, préparé D219)} : la\ncérémonie § \\ref{sec:cerd183} (le kit au dépôt) A ÉTÉ VÉCUE le\n19 novembre 2026 — depuis, la garde active est le séquestre 5/3\n(la reconstitution à froid de trois parts, la phrase en AUCUN\ndépôt) et le dépôt est PUBLIC (D220) — l'état vécu acté par D223 ;\nla cérémonie n'est plus \\emph{au commandement}, elle est \\emph{au\npassé}, datée.",
        "§8.2 item 7 — « tant qu'elle est VÉCUE » réécrit")

    # (iii) LES MÉTADONNÉES v1.7 — le main.tex (l'en-tête, fancyhead,
    #       pdftitle) et la couverture
    t = (LIVRE / "main.tex").read_text(encoding="utf-8")
    for ancien, nouveau in [
            ("(v1.6, ou6wn6wlv)", "(v1.7, h66o54pjd)"),
            ("v1.6 : la purge des instructions de remise D81 (ou6wn6wlv — le",
             "v1.7 : les phrases cassées réparées, les résidus prescriptifs au"),
            ("Le Livre du Coffre — TRIADE CF1 → CF3 (v1.6)",
             "Le Livre du Coffre — TRIADE CF1 → CF3 (v1.7)"),
            ("TRIADE CF1 → CF2 → CF3 (v1.6)",
             "TRIADE CF1 → CF2 → CF3 (v1.7)")]:
        if ancien in t:
            t = t.replace(ancien, nouveau, 1)
            R.append(f"main.tex (Livre) : {ancien[:34]} → v1.7")
    (LIVRE / "main.tex").write_text(t, encoding="utf-8")
    t = (LIVRE / "cover.html").read_text(encoding="utf-8")
    for ancien, nouveau in [
            ("R&eacute;vision v1.6 (D236, la purge D81)",
             "R&eacute;vision v1.7 (h66o54pjd)"),
            ("r&eacute;vision v1.6 (D236)", "r&eacute;vision v1.7"),
            ("v0.15.7", "v0.15.8"),
            ("D75&ndash;D243", "D75&ndash;D250")]:
        if ancien in t:
            t = t.replace(ancien, nouveau, 1)
            R.append(f"cover.html (Livre) : {ancien[:30]} → v1.7")
    (LIVRE / "cover.html").write_text(t, encoding="utf-8")

    # (iv) L'AVANT-PROPOS (sec-1.tex:8) — la version
    t = (LIVRE / "sec-1.tex").read_text(encoding="utf-8")
    if "v1.6" in t:
        t = t.replace("v1.6", "v1.7", 1)
        R.append("sec-1.tex : l'avant-propos à v1.7")
    (LIVRE / "sec-1.tex").write_text(t, encoding="utf-8")

    # (v) LE §10.1 ET LA TABLE 12 (sec-5.tex) — la version et la plage
    #      décisionnelle réelle
    t = (LIVRE / "sec-5.tex").read_text(encoding="utf-8")
    if "v1.6" in t:
        t = t.replace("v1.6", "v1.7", 1)
        R.append("sec-5.tex : la version à v1.7")
    for ancien, nouveau in [("D75--D243", "D75--D250"),
                            ("D75–D243", "D75–D250")]:
        if ancien in t:
            t = t.replace(ancien, nouveau)
            R.append(f"sec-5.tex : la plage décisionnelle {nouveau}")
    (LIVRE / "sec-5.tex").write_text(t, encoding="utf-8")


# ===========================================================================
# (C) LE PROTOCOLE_TRIADE.md — les cibles prescriptives
# ===========================================================================
def patcher_proto():
    # (l) le tableau CF1 (l.1355)
    remplace(
        PROTO,
        "| CF1 | `coffre_fort.py init` | conteneur chiffré à phrase (D75) ; garde durable de la phrase (D81) ; relève simple |",
        "| CF1 | `coffre_fort.py init` | conteneur chiffré à phrase (D75) ; la garde de la phrase à l'arbitrage du développeur (D137 — la garde active D223 : le séquestre à reconstitution à froid, la phrase en AUCUN dépôt ; l'histoire D81 datée) ; relève simple |",
        "le tableau CF1 — la garde active D223")
    # (m) le §12.5 équivalent (l.1374)
    remplace(
        PROTO,
        "Ce qui demeure obligatoire, niveau par niveau : CF1 — la garde durable de la phrase ;",
        "Ce qui demeure obligatoire, niveau par niveau : CF1 — la garde de la phrase à l'arbitrage du développeur (D137 ; la garde active D223 : la reconstitution à froid de trois parts, la phrase en AUCUN dépôt) ;",
        "l'exigence CF1 — la garde active D223")
    # (n) la table des cérémonies (l.1398) — « phrase (remise D81 AVANT tout) »
    remplace(
        PROTO,
        "| CF1 → CF2 (D106) | phrase (remise D81 AVANT tout) ; `migrer` ; 5 gardes ; T = 3 copies hors-ligne (feuille g3–g5 ou USB) ; relecture ; liste blanche | CF2 `verifier` VERT ; CF1 laissé intact |",
        "| CF1 → CF2 (D106) | phrase (la garde en vigueur : D223 — la reconstitution à froid de trois parts du séquestre ; l'histoire D81 « remise AVANT tout » datée du 4 au 19 novembre 2026) ; `migrer` ; 5 gardes ; T = 3 copies hors-ligne (feuille g3–g5 ou USB) ; relecture ; liste blanche | CF2 `verifier` VERT ; CF1 laissé intact |",
        "la table des cérémonies — la remise D81 bornée datée")
    # (o) LE §17.3 (l.1708-1712) — l'instruction prescriptive de remise
    #      RÉÉCRITE vers la garde active
    remplace(
        PROTO,
        "consigné : chaque cérémonie de clés (D27/D30) alimente le coffre-fort dans la même\nsession, et **la phrase de contrôle est sauvegardée durablement AVANT TOUTE AUTRE\nACTION** — `PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt (phrase seule sur une ligne,\nlisible par `--phrase-fichier`), commit dédié, push GitHub, miroir du coffre Drive par\nle hook, copie au racine du coffre Drive — le fichier EST la remise (l'affichage unique\nde D27/D30 demeure possible mais n'est plus le canal de survie). À chaque rotation le",
        "consigné : chaque cérémonie de clés (D27/D30) alimente le coffre-fort dans la même\nsession. **La garde de la phrase est le séquestre à seuil depuis le 19 novembre 2026\n(D223)** : la phrase répartie en CINQ parts à seuil TROIS, AUCUNE phrase en clair au\ndépôt ni au coffre Drive — la voie de survie est la cérémonie de reconstitution à\nfroid de trois parts (§ 17.3bis), le refus nommé D223 garde la ligne ; l'affichage\nunique de cérémonie (D27/D30) demeure possible mais n'est jamais le canal de survie.\n(L'histoire D81 — la phrase au fichier-remise `PHRASE-CONTROLE-COFFRE.txt`, commit\ndédié, push GitHub, miroir et coffre Drive, AVANT toute autre action — est DATÉE :\ndu 4 au 19 novembre 2026, amendée par D223, jamais un geste courant.) À chaque rotation le",
        "§17.3 — l'instruction prescriptive RÉÉCRITE vers la garde D223")
    # (p) LE GLOSSAIRE (l.2113)
    remplace(
        PROTO,
        "| Phrase de contrôle | Secret ouvrant le coffre-fort — sous garde durable depuis D81 : `PHRASE-CONTROLE-COFFRE.txt` au dépôt et au racine du coffre Drive, sauvegardé AVANT toute autre action dès production (§ 17.3) |",
        "| Phrase de contrôle | Secret ouvrant le coffre-fort — sous séquestre à seuil depuis le 19 novembre 2026 (D223) : répartie en CINQ parts à seuil TROIS, AUCUNE phrase en clair au dépôt ni au coffre Drive, la reconstitution à froid de trois parts l'unique voie (§ 17.3) ; l'histoire D81 (le fichier-remise au dépôt) est datée du 4 au 19 novembre 2026 |",
        "le glossaire — la garde active D223")


# ===========================================================================
# (D) LE FORMAT_CARTE.md — les deux blocs prescriptifs
# ===========================================================================
def patcher_carte():
    # (r) l.310-315 : la description de la garde
    remplace(
        CARTE,
        "- la **phrase de contrôle** ouvre le coffre ; elle vit sous garde durable depuis D81 —\n  sauvegardée dès production (init, rotation, changement) dans le dépôt\n  (`PHRASE-CONTROLE-COFFRE.txt` au racine, phrase seule sur une ligne, lisible par\n  `--phrase-fichier`) et au racine du coffre Drive, AVANT toute autre action de la\n  session ; le fichier EST la remise — l'affichage unique de cérémonie (D27/D30) demeure\n  possible mais n'est plus le canal de survie ;",
        "- la **phrase de contrôle** ouvre le coffre ; elle vit sous séquestre à seuil depuis\n  le 19 novembre 2026 (D223) — répartie en CINQ parts à seuil TROIS, AUCUNE phrase\n  en clair au dépôt ni au coffre Drive, la cérémonie de reconstitution à froid de\n  trois parts est l'unique voie de survie ; l'affichage unique de cérémonie (D27/D30)\n  demeure possible mais n'est jamais le canal ; (l'histoire D81 — le fichier-remise\n  `PHRASE-CONTROLE-COFFRE.txt` au dépôt et au coffre Drive — est datée du 4 au\n  19 novembre 2026, amendée D223) ;",
        "la description de la garde — D223 active")
    # (s) l.355-360 : l'instruction (4) prescriptive et la (5) de restauration
    remplace(
        CARTE,
        "production d'une phrase de contrôle neuve est sauvegardée AVANT TOUTE AUTRE ACTION —\n`PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt (commit dédié, push GitHub, miroir Drive\npar le hook) + copie au racine du coffre Drive, md5 vérifiés — le fichier est la remise\n(D81) ; à chaque rotation il est remplacé et git conserve les phrases retirées du service ;\n(5) après une réinitialisation : importer le conteneur, relire la phrase de contrôle\ndepuis `PHRASE-CONTROLE-COFFRE.txt` (dépôt, miroir ou racine du coffre Drive — D81), puis",
        "production d'une phrase de contrôle neuve vivra sous la garde en vigueur (D223 :\nle séquestre à seuil — la cérémonie de répartition en cinq parts à seuil trois,\nAUCUNE phrase en clair au dépôt ; l'histoire D81 du fichier-remise commité est\ndatée du 4 au 19 novembre 2026, jamais un geste courant) ; à chaque rotation les\nparts sont rafraîchies et git ne conserve AUCUNE phrase ;\n(5) après une réinitialisation : importer le conteneur, reconstituer la phrase de contrôle\nà froid depuis TROIS parts du séquestre (la cérémonie D223 — jamais le dépôt), puis",
        "les instructions (4) et (5) — la garde D223 au présent")


def main() -> int:
    print("[h66o54pjd] LES PATCHERS ANCRÉS — REFUS si une ancre manque")
    patcher_spec()
    patcher_livre()
    patcher_proto()
    patcher_carte()
    print(f"\nLES {len(R)} REPLACEMENTS VÉCUS :")
    for r in R:
        print(f"  — {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
