#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le complément md de la consolidation v0.9.0 — la correspondance
§ 19.11 (v0.8.4 → v0.9.0) + les modifications rejetées, le modèle D176."""

CHEMIN = "/home/z/my-project/triade/docs/PROTOCOLE_TRIADE.md"
texte = open(CHEMIN, encoding="utf-8").read()


def remplace(ancien, nouveau, combien=1):
    global texte
    n = texte.count(ancien)
    assert n == combien, f"ancre {n}x (attendu {combien}) : {ancien[:80]!r}"
    texte = texte.replace(ancien, nouveau)


remplace("""Sceller la 0.1.0 de Loupe au build — rejeté : la balise de développement naît au
build (geste de BUILD jamais scellage, miroir M6/M7/M8) ; la 0.1.0 se scellera sur
le run terrain vert recoupé.

## 20. Glossaire""",
         """Sceller la 0.1.0 de Loupe au build — rejeté : la balise de développement naît au
build (geste de BUILD jamais scellage, miroir M6/M7/M8) ; la 0.1.0 se scellera sur
le run terrain vert recoupé.

### 19.11 Correspondance v0.8.4 → v0.9.0

| Évolution | En v0.8.4 | En v0.9.0 | Statut |
|---|---|---|---|
| Jalon M10 (le TGN « Loupe ») | ouvert : cinq runs vécus, cinq défauts nommés (les refus du chargeur, [CADRE-NÉ], la classe des arguments pile, [SESSION] -7 — la pièce acquittée), la retouche dev.6 au kit seul | FRANCHI : ONZE RUNS TERRAIN, ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES ([HINSTANCE-PEB], [D54-QUATRIÈME] + [EAX-SANS-SIGNE], [OFT-QWORD], [FREE-SANS-TYPE], [RET-NU], [SONDE-EXE] — la liaison prouvée par le vivant) ; LA VITRINE VIVANTE (0 et 0 aux dixième et onzième runs — l'application née de TRIADE a vécu chez son utilisateur) ; le onzième run recoupé 39/39 | révisé (D178, Entrées 209–219) |
| La balise `loupe 0.1.0` | attend le vert entier (la dette de la carte nommée : génération 13/dev.5, la pièce dev.8) | SCELLÉE PAR FAIT DE CARTE : la dette de la carte soldée par la RÉGÉNÉRATION DES NOTATIONS (18/18 == la pièce octet pour octet, l'écart 587 → 0), la cristallisation 26 × 10/10, la re-signature à la graine durable (le témoin ne bouge pas), l'anti-rollback ARMÉ, loupe.exe INTACT (054de960…) — le même binaire que le onzième run a couru | révisé (D178) |
| La dette [R10-PÉRIMÉE] | nommée au scellage (17 sommes de l'ère dev.5 à la porte de la pièce — réparable à 0.1.1+, jamais un hot-fix d'un scellé) | SOLDÉE À LA NAISSANCE : la version `0.1.1-dev.1` COMMANDÉE (D179) naît de la recomposition même — les 17 sommes rafraîchies à la vérité des blocs, le qword porté 0x00010101, 0 octet de code changé (R4/R7) ; la carte GÉNÉRATION 17 ; le kit 0.1.1-dev.1 déposé au coffre `/test`, LE DOUZIÈME RUN ATTENDU — la balise `loupe 0.1.1` se scellera sur le vert recoupé (le miroir D165/D170) | révisé (D179) |
| Programme d'après M10 | — (le jalon attend son scellage) | OUVERT À LA COMMANDE DU DÉVELOPPEUR : la consolidation v0.9.0 (le modèle D169/D176), la version 0.1.1 (D179) ; le projet fils COFFRE-FORT demeure dégélable au rythme du développeur (D135 amendée par D171) | nouveau (D179) |
| Chaîne PDF | spec_v084 (née spec_v083 — les révisions de terrain v0.8.1 à v0.8.4) ; les archives v0.7.0 à v0.8.3 demeurent | chaîne spec_v090 (née spec_v084) ; les archives v0.7.0 à v0.8.4 demeurent | révisé (D180) |

Modifications explicitement rejetées (v0.9.0) : rafraîchir la table R10 au scellage
de la 0.1.0 — rejeté : LA PIÈCE ne bouge jamais au scellage (fait de carte) ; la
dette se nomme et se paie à la version suivante, jamais un hot-fix d'un scellé
(D178). Sceller la 0.1.1 au build sans le run terrain — rejeté : le miroir
D165/D170 exige le verdict du recoup vert COMME PIÈCE, la porte est de processus.
Rouvrir le jalon M10 pour la 0.1.1 — rejeté : M10 est clos sur sa balise ; la 0.1.1
est une version de maintenance à contrat stable (R4), pas une réépreuve du jalon.
Modifier les notations D172–D175 pour la 0.1.1 — rejeté : le code est
byte-identique au vécu des onze runs ; les notations décrivent LA PIÈCE (R2/R5).

## 20. Glossaire""")

open(CHEMIN, "w", encoding="utf-8").write(texte)
print("[md] la correspondance § 19.11 (v0.8.4 → v0.9.0) consignée + les 4 rejets")
