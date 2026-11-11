#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_232.py — LA SESSION DE REPRISE DU 12/11 consignée :
le point de reprise vérifié aux TROIS MIROIRS (/instructions VIDE, GitHub ==
pointe, bundle Drive recoupé, garde 14/14), L'INSTRUMENT DU MIROIR RÉPARÉ
(verif_bundle_miroir.py : la branche jalon v0.5.1 figée rendait un ÉCHEC
faux — la comparaison portée à refs/heads/main, la branche canonique D141),
L'AUTOTEST D183 re-exécuté VERT (la pièce D192 restaurée intacte) — Entrée
232 + D199 + worklog Task 138. Append-only : les fins sont VÉRIFIÉES avant
chaque écriture (Entrée 231 / D198 / Task 137 attendues à la fin)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"


def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    if fin_attendue not in texte:
        sys.exit(f"[consigner] {nom} : la fin attendue est ABSENTE — "
                 f"append refusé (discipline append-only)")
    if texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")) is False:
        # la fin attendue doit être LA dernière section
        pass  # contrôle strict fait ci-dessous par comptage
    occurrences = texte.count(fin_attendue)
    if occurrences != 1:
        sys.exit(f"[consigner] {nom} : la fin attendue apparaît "
                 f"{occurrences} fois (attendu : 1) — append refusé")
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 f"dernière section — append refusé")
    if "Entrée 232" in texte:
        sys.exit(f"[consigner] {nom} : Entrée 232 déjà présente — "
                 f"append refusé (doublon)")
    with chemin.open("a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} caractères)")


ENTREE_232 = """

## Entrée 232 — LE POINT DE REPRISE VÉRIFIÉ AUX TROIS MIROIRS ET L'INSTRUMENT DU MIROIR RÉPARÉ : /instructions VIDE (aucun dépôt nouveau depuis la livraison v0.15.0), la branche jalon v0.5.1 de verif_bundle_miroir.py remplacée par la branche canonique refs/heads/main, l'autotest D183 re-exécuté VERT (la pièce D192 restaurée intacte) — le programme du labo ÉPUISÉ, les quatre suites attendent le développeur (12/11, la session du point de reprise)

**Le point de reprise.** Le dossier /instructions du coffre est VIDE — l'instruction ic09ydeli exécutée et archivée à la clôture v0.15.0 (Entrée 231) demeure la dernière. Le pointage temporel du coffre ENTIER (racine, /instructions, /test, /Cérémonie, /Tokens, /ARCHIVE — les métadonnées created/modified de chaque entrée) : aucun dépôt nouveau depuis la livraison — les derniers écrits du coffre sont les TROIS livrables v0.15.0 (soumission, complet, empreintes — 11/11 18:08 UTC), œuvres de la session de livraison elle-même ; la racine ne porte que les versions COURANTES (la règle D197 appliquée et tenue). Les TROIS MIROIRS recoupés : le dépôt PROPRE à d582bfb ; GitHub origin/main == HEAD (le fetch relit la pointe) ; le bundle triade-history.bundle du miroir Drive téléchargé et recoupé (md5 b1c2097b… MATCH la métadonnée, git bundle verify VALIDE, refs/heads/main == d582bfb). LE GARDE sceau-I : 14 arbres VERTS, la clé demeurée « reelle (ceremonie hors-ligne, D87) ».

**La réparation de l'instrument (D199).** L'outil de re-vérification du miroir (scripts/verif_bundle_miroir.py) a rendu ce jour un verdict « ÉCHEC » sur un miroir CORRECT : sa comparaison portait sur la branche jalon bundle051/v0.5.1-jalon-v7 — l'artefant de l'époque v0.5.1, figée à 9888d06 depuis son scellage, elle n'a JAMAIS bougé — au lieu de la branche canonique. Le faux négatif constaté AUX PIÈCES d'abord (les têtes du bundle listées : refs/heads/main == d582bfb, la pointe), la cause lue au code ensuite. La réparation minimale : la comparaison portée à refs/heads/main (la branche canonique du bundle courant depuis D141), le nom par défaut porté au bundle courant triade-history.bundle ; l'outil re-exécuté : VERT — le miroir porte la pointe. La leçon : un instrument de vérification figé sur une référence d'époque rend des verdicts faux SANS le dire — chaque instrument de re-vérification porte sa référence VIVANTE (la branche canonique du dépôt, jamais une balise de cérémonie passée).

**L'autotest D183 re-exécuté.** La suite séquestre (la deuxième des quatre, Task 137) confirmée OUTILLÉE au point de reprise : l'autotest du kit (scripts/kit_ceremonie_d183/sequestre_d183.py --autotest) re-exécuté VERT — les C(5,3) = 10 combinaisons au seuil reconstituent EXACTEMENT la phrase de test publique, les C(5,2) = 10 paires sous le seuil rendent un déchet, une part seule ne porte rien (Shamir 1979). La PIÈCE D192 (AUTOTEST.txt, exécuté le 11/11 15:00:31) RESTAURÉE INTACTE après le geste : l'outil écrase son rapport à chaque exécution — la pièce consignée à D192 demeure, la re-exécution du point de reprise vit dans la présente entrée. LE COFFRE RÉEL N'A PAS ÉTÉ TOUCHÉ (aucune phrase réelle lue, aucun conteneur ouvert — D87/D192/D183 : la cérémonie appartient au développeur).

**L'état.** Le programme du laboratoire est ÉPUISÉ : tout ce qui est outillable au labo est LIVRÉ (la v0.15.0 menée à terme, Entrée 231). Les QUATRE suites nommées (Task 137) attendent leurs acteurs : (a) LES RUNS MATÉRIELS du développeur — le dudect temps réel, le fence.i sur silicium, le terrain tiers Loupe (les trois kits aux LISEZMOI pas à pas, aucun chiffre n'existe) ; (b) LA CÉRÉMONIE DU SÉQUESTRE D183 — le kit VERT, le LISEZMOI pas à pas (la répétition générale, le découpage, la répartition des médias, la preuve de reconstitution à froid avant tout retrait) ; (c) LA CÉRÉMONIE D'ÈRE — Ed25519 hors-ligne, la clé jamais traversée ; (d) LA RÉPLICATION — le second annotateur À RECRUTER, le second domaine EN ATTENTE d'une vraie commande. Aucun programme inventé pour soi-même : la session de reprise VÉRIFIE, RÉPARE l'instrument défaillant, CONSIGNE — et rend la main au développeur.
"""

D199 = """

## D199 — LA BRANCHE CANONIQUE DU MIROIR ASSERTÉE : refs/heads/main (la réparation de l'instrument de re-vérification verif_bundle_miroir.py — la branche jalon bundle051/v0.5.1-jalon-v7, artefact de l'époque v0.5.1 figée à 9888d06 depuis son scellage, comparée à la pointe locale rendait un ÉCHEC FAUX alors que le miroir portait la pointe : le faux négatif constaté aux pièces ce jour [les têtes du bundle : refs/heads/main == d582bfb == HEAD], la cause lue au code, la réparation minimale vécue) ; LA RÈGLE DE L'INSTRUMENT QUI VIEILLIT (un instrument de vérification figé sur une référence d'époque rend des verdicts faux SANS le dire : chaque instrument de re-vérification porte sa référence VIVANTE — la branche canonique du dépôt, jamais une balise de cérémonie passée ; le défaut du nom porté au bundle courant triade-history.bundle ; le verdict faux du 12/11 a nommé la dette, la réparation la solde au geste)

**Le contexte.** La session de reprise du 12/11 exécute la routine D13 (les trois miroirs relus au point de reprise) ; l'instrument du miroir rend « ÉCHEC » sur un miroir correct. La discipline « vérifier avant d'agir » s'applique À L'OUTIL LUI-MÊME : le verdict confronté aux pièces brutes (list-heads du bundle), la divergence localisée à la référence de comparaison — pas au miroir.

**Frontières.** Lecture seule sur le coffre ; AUCUNE pièce historique modifiée (AUTOTEST.txt de D192 restauré intact après la re-exécution de l'autotest, le diff vide) ; aucun artefact scellé touché ; le garde 14/14 VERT au geste ; les consignations antérieures NON réécrites (append-only).
"""

TASK_138 = """

Task ID: 138
Agent: Z.ai (agent principal)
Task: LA SESSION DE REPRISE DU 12/11 — le point de reprise vérifié aux
TROIS MIROIRS, /instructions VIDE, l'instrument du miroir RÉPARÉ (D199),
l'autotest D183 re-exécuté VERT (la pièce D192 restaurée) — le programme
du labo ÉPUISÉ, les quatre suites attendent le développeur.

Work Log:
- LE POINTAGE DU COFFRE : /instructions VIDE ; aucun dépôt nouveau depuis
  la livraison v0.15.0 (les trois livrables du 11/11 18:08 UTC, œuvres de
  la session de livraison) ; la racine ne porte que les versions courantes
  (D197 tenue).
- LES TROIS MIROIRS : le dépôt PROPRE à d582bfb ; origin/main == HEAD (le
  fetch relit la pointe) ; le bundle triade-history.bundle recoupé (md5
  b1c2097b… MATCH, git bundle verify VALIDE, refs/heads/main == d582bfb).
- LE GARDE : sceau-I 14/14 VERT (la clé « reelle », D87).
- L'INSTRUMENT RÉPARÉ (D199) : verif_bundle_miroir.py comparait la branche
  jalon bundle051/v0.5.1-jalon-v7 (figée à 9888d06) — verdict ÉCHEC FAUX
  sur un miroir correct ; la comparaison portée à refs/heads/main (la
  branche canonique D141), le défaut porté au bundle courant ; re-exécuté
  : VERT.
- L'AUTOTEST D183 : re-exécuté VERT au point de reprise (les 10
  combinaisons au seuil EXACTES, les 10 paires sous le seuil DÉCHET) ;
  la pièce D192 (AUTOTEST.txt du 11/11 15:00:31) RESTAURÉE intacte ; le
  coffre réel jamais touché.
- SUITE : au développeur — les trois runs matériels (les kits dudect /
  fence.i / terrain tiers), la cérémonie du séquestre D183 (le kit VERT,
  le LISEZMOI pas à pas), la cérémonie d'ère, le recrutement de
  l'annotateur R2, le second domaine à la vraie commande.
"""


def main() -> int:
    # 1) Les fins attendues (une seule occurrence, à la fin de chaque fichier)
    append_verifie(JOURNAL, "ARCHIVÉE après exécution (md5 recoupé).",
                   ENTREE_232, "JOURNAL_TRAVAIL.md")
    # 2) D199 après D198
    append_verifie(DECISIONS,
                   "le raffinement relie le modèle à l'implémentation, "
                   "il ne transforme pas le symbolique en réel.",
                   D199, "DECISIONS.md")
    # 3) Task 138 après Task 137
    append_verifie(WORKLOG,
                   "séquestre D183, la cérémonie d'ère, la réplication.",
                   TASK_138, "worklog.md")
    print("[consigner] Entrée 232 + D199 + Task 138 : CONSIGNÉES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
