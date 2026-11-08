#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d176.py — LA CONSIGNATION DE LA DÉCISION D176 (la consolidation
v0.8.0) au journal des décisions. Append-only : l'entrée suit D175. Tout
ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
DECISIONS = REPO / "docs" / "DECISIONS.md"

D176 = """

## D176 — LA SPÉCIFICATION v0.8.0 : LA CONSOLIDATION DU PROGRAMME D'APRÈS M9 (le jalon M9 — TLS 1.3 pur en blocs scellés, le domaine `tls13` — FRANCHI : les 28 blocs notés-mesurés-prouvés, le septième run terrain vert recoupé 34/34 sur pièces croisées, LA SESSION RÉELLE — la ligne applicative chiffrée ÉCHANGÉE avec un serveur réel —, la finale `1.0.0` SCELLÉE sur recoup exigé comme pièce [D170]) ; LE TEST GRANDEUR NATURE OUVERT (le jalon M10, D171 : « Loupe », l'éditeur hexadécimal au panneau d'empreintes — la couche I de 18 spécifications [D172] et les QUATRE chantiers de notation accomplis [D173/D174/D175 : les 18 blocs NOTÉS-MESURÉS-PROUVÉS]) ; LA DETTE DU QUATORZIÈME ARBRE NOMMÉE (la cérémonie d'ère du TGN précède tout build — le garde demeure à 13/13 jusque-là) ; le projet fils COFFRE-FORT dégelé en parallèle (D171, D135 amendée)

**Le contexte qui fonde la décision (08/11, la demande du développeur).** La demande du développeur porte la mise à jour du document PDF Protocole TRIADE après les gestes du TGN. Le constat du geste : la spécification vivante v0.7.0 est EN RETARD SUR LE PROGRAMME sur quatre points nommés — le § 18 titre « jalons M0 à M9 » et tient M9 « ouvert » alors que M9 est FRANCHI (finale 1.0.0 scellée le 07/11, Entrée 193/D170 : la session réelle la ligne applicative chiffrée, le témoin « HTTP/1.1 200 OK » déchiffré par la machine, l'épinglage -6 nommé, proxy.exe byte-identique 446279f3…) ; le TGN ouvert au D171 (l'application « Loupe », le domaine `loupe`) et ses QUATRE chantiers de notation accomplis (D172–D175) ne vivent nulle part au document ; le § 13.5 s'arrête aux cérémonies des ères M8/M9 alors que l'ère du TGN porte sa dette nommée (le 14e arbre, D166/D171) ; le projet fils COFFRE-FORT demeure « développement différé » alors que D171 l'a dégelé. Le versionnement suit les RÉVISIONS, jamais les franchissements (addendum Task 62) — mais un programme entré en exécution EST une révision en attente de sa passation : la v0.8.0 est la passation du programme d'après M9 dans la spécification, le miroir exact de ce que D169 fit pour le programme d'après M7.

**Les règles.** (1) **Le programme d'après M9 entre en spécification** : l'état des jalons est CONSTATÉ — M0–M9 FRANCHIS (balises 0.2.0 à 0.9.0 et 1.0.0), M10 OUVERT (le TGN, D171) : la couche I complète (18 spécifications en cinq familles, D172) et les quatre chantiers de notation accomplis (D173 le noyau fichier + empreintes, D174 le rendu + la navigation, D175 l'édition + la table de routage de loupe-09 étendue en révision nommée) — les 18 blocs NOTÉS-MESURÉS-PROUVÉS (59 + 53 + 45 contrôles verts aux trois graines sur les trois harnais). (2) **Le sceau est consigné à son état réel** : TREIZE arbres signés + LA DETTE DU QUATORZIÈME nommée — l'ère du TGN suit la discipline des ères (D166 règle 8 : la dette à la naissance ; D168 : la charge au geste ; D163 : la continuité par le déterminisme Ed25519) ; le § 13.5 étendu consigne la cérémonie À VENIR (la remise FRAÎCHE des quatorze arbres au /Cérémonie, le geste hors-ligne du développeur à la clé du 04/11, les pièces au coffre /test, le garde à QUATORZE arbres VERTS après installation — puis le build de Loupe peut naître). (3) **Le TGN entre au § 18** : la rangée M10 avec ses critères de sortie mesurables (coder une application réelle NEUVE entièrement avec TRIADE, de l'intention à l'octet livré ; l'oracle à scénarios vert ; la balise `loupe 0.1.0` scellée sur run terrain recoupé) et le paragraphe du programme (l'épreuve de la MÉTHODE ENTIÈRE — le modèle RoomEq s'arrêtait au recodage, le TGN exige la CRÉATION). (4) **Aucune règle du cœur n'est modifiée, aucune couche n'est ajoutée à l'exécution, la hiérarchie est inchangée** — la révision consolide, elle ne légifère pas.

**Alternatives rejetées.** Attendre la clôture de M10 pour réviser (rejeté : la consolidation suit le PROGRAMME, pas la finale — M9 franchi ET le TGN ouvert sont DEUX moteurs d'une même passation, le précédent D169 fut la passation d'un programme en cours) ; mettre l'application « Loupe » sous le sceau AVANT la cérémonie (rejeté : le garde suit le calendrier de la cérémonie, jamais l'inverse — le 14e arbre exige la clé hors-ligne du développeur, le laboratoire ne signe jamais à sa place) ; ajouter un profil de cible pour le TGN (rejeté : le profil primaire `x86-64-win11-pe` est l'épreuve ; l'universalité est déjà prouvée M6/M7) ; sceller la 0.1.0 de Loupe au build (rejeté : la balise de développement naît au build — geste de BUILD jamais scellage, miroir M6/M7/M8 ; la 0.1.0 se scellera sur le run terrain vert recoupé) ; signer les sources `docs/` sous le sceau courant (rejeté : le modèle par-version demeure, `v06/I/README.md` § 1).

**Frontières.** Les balises INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 — la révision documente, elle ne scelle rien) ; l'archive v0.7.0 DEMEURE (docs/Protocole_TRIADE_v0.7.0_Specification.pdf, dernier build consigné sha256 dd36eb41…, 999 631 o — rien ne se jette) ; le *Livre du Coffre* v1.1 INCHANGÉ (la révision ne touche pas le coffre) ; la chaîne spec_v070 devient spec_v080 par COPIE (l'archive spec_v070 DEMEURE au dépôt — le modèle des révisions : l'ancienne chaîne reste dans l'histoire). Les pièces : docs/PROTOCOLE_TRIADE.md (v0.8.0, révisé PAR SCRIPT revision_v080_md.py), scripts/revision_v080_tex.py (les 23 remplacements LaTeX ASSERTÉS), scripts/spec_v080/ (la chaîne), scripts/spec_v080/verify_spec.py (le cahier V1–V16), docs/Protocole_TRIADE_v0.8.0_Specification.pdf (l'artefact, 45 pages, sha256 95226c2b24dd…, empreinte consignée PAR LE BUILD n°26).
"""


def main() -> int:
    t = DECISIONS.read_text(encoding="utf-8")
    if "## D176 —" in t:
        print("[inserer-d176] REJEU REFUSÉ : D176 existe déjà.")
        return 1
    if "## D175 —" not in t:
        print("[inserer-d176] ÉCHEC : D175 absente (ordre des décisions rompu).")
        return 1
    if not t.rstrip("\n").endswith("le présent script."):
        print("[inserer-d176] ÉCHEC : la fin du registre n'est pas celle attendue "
              "(D175 doit clore le registre).")
        return 1
    t = t.rstrip("\n") + "\n" + D176.strip("\n") + "\n"
    DECISIONS.write_text(t, encoding="utf-8")
    print("[inserer-d176] PASSÉ : D176 consignée à la suite de D175.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
