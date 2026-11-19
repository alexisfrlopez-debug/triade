#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_opt04.py — LA CONSIGNATION de la session cq01qv1za (append-only
partout) : OPT-04 au journal d'optimisation, D222 au journal des décisions,
l'Entrée 371 au worklog, la carte OU-TROUVER portée."""
import pathlib
import re

REPO = pathlib.Path("/home/z/my-project/depot")

# ---- 1. OPT-04 au journal d'optimisation (append-only) ---------------------
journal = REPO / "atelier-baseline-20261117" / "JOURNAL-OPTIMISATION-TOKENS.txt"
journal.write_text(journal.read_text(encoding="utf-8") + """

================================================================================
OPT-04 — LE COÛT DE LA BOUCLE SOUS R11 : LE POINTEUR SEUL, LE MÉMO V2, LE
DOUBLE MOTEUR, H5 TENUE (le 19/11/2026, l'instruction cq01qv1za — la vague
7, la quatrième ; le plan PLAN-cq01qv1za-COUT.md sha256 cb5d1943… gelé AVANT
toute mesure, le commit fed8c6d précédant la première donnée)
================================================================================
LA MESURE AVANT (l'opération localiser, le format en vigueur) : le total
1 714 natifs MÉDIANE [721–5 204], la réponse 770 [301–2 543] — 18 appels
réels, la graine 20261117, le natif lu du champ usage (100 % log-api, le
modèle glm-4-plus).

LE GAIN MESURÉ (le mode P, le pointeur seul — ID + empreinte sha256, deux
champs LITTÉRAUX, l'expansion côté client à QUATRE refus nommés) :
  le TOTAL : 1 714 → 1 103 natifs = −35,7 % ;
  la RÉPONSE : 770 → 52 = −93,3 % ;
  zéro divergence 18/18, l'expansion client 18/18, la re-tokenisation
  indépendante (encode_ordinary, un objet neuf) à 0 écart — la voie
  segmentée portant un artefact SYSTÉMATIQUE +2 aux frontières de lignes,
  NOMMÉ jamais confondu ; le cl100k parallèle cohérent.

LE VÉRIFICATEUR : la confrontation aux octets reprise TELLE QUELLE de
5gfx6pwkj (loupe.exe lu au slot, padding NOP, aucun int3 instruction —
VERT 18/18) ; les falsifications du pointeur vécues (l'empreinte mutée →
EMPREINTE-DIVERGENTE, l'identifiant inconnu → POINTEUR-INCONNU, la
réponse hors format → HORS-FORMAT, le pointeur croisé →
EXPANSION-DIVERGENTE — 5/5 VERT à expansion_pointeur.py).

LA PILE M4 (le mémo v2 + le double moteur, la même liste fixe que la
vague 5, n=5 par configuration, chronomètre monotone, CE bac 2 cœurs —
il fait partie du record) :
  AVANT (v180) : 39,7 s MÉDIANE [39,4–40,3] ; FROID (semis QEMU) : 6,7 s ;
  CHAUD régime : 6,8 s [6,7–6,9] n=4 (+ l'AUDIT automatique au CHAUD 4 :
  29,4 s — le prix de la preuve, nommé) ; AUDIT dédié : 39,1 s ;
  BRAS C : 2,2 s [2,1–2,2].
  LES ÉTAPES : l'oracle-01 10,340 → 0,453 s ; l'oracle-02 23,445 →
  0,522 s (le loupe-01 sous QEMU : ~0,0 s contre ~10 s sous le harnais
  instrumenté — le hook PAR INSTRUCTION était le coût, le TCG nu ne l'est
  pas).

LA RÉCONCILIATION DU MÉMO D214 SUR PIÈCES : la vague 5 39,3/39,2 s n=2 ;
vljfs6pcj 39,5 [39,1–39,7] n=5 ; CE bac 39,7 [39,4–40,3] n=5 — des bacS
DIFFÉRENTS de la même classe 2 cœurs, les plages se chevauchent, l'écart
0,2–0,5 s (0,5–1,3 %) est la variance inter-bac NOMMÉE ; chaque mesure
vraie À SA MACHINE, le ratio aux DEUX bras de la même machine fait foi.

LE RATIO ET H5 (la règle de l'instruction, sa lettre) : AVANT 39,7/2,2 =
17,9× ; RÉGIME 6,8/2,2 = 3,0× — SOUS ×10 : H5 DEVIENT TENUE, ÉNONCÉ
EXPLICITEMENT ; la falsification D204 (×23,9) DEMEURE consignée comme
mesurée et datée — la réhabilitation est l'AMENDEMENT DU MAÎTRE (la règle
mof9q10vq « la réhabilitation exige le terrain » amendée par
l'instruction ; le terrain à venir confirmera, la table porte le statut
TEL QUE mesuré et sourcé).

LE MÉMO V2 : la clé = sha256(bloc ‖ entrée ‖ contrat ‖ config émulateur ‖
graine ‖ oracle) — le sur-ensemble de la v1 ; le COMPTEUR DE RUNS vit au
CŒUR SIGNÉ (le muter = SIGNATURE-INVALIDE, vécu) ; L'AUDIT 1 RUN SUR 10 :
le 10ᵉ scellement a déclenché l'audit TOUT SEUL pendant la mesure (le
CHAUD 4) — les relevés vivants Unicorn confrontés aux relevés mémoisés
CHAMP À CHAMP : 0 écart (la preuve d'identité).

LE DOUBLE MOTEUR : le lanceur C statique (ms_abi, les SIX feuilles
kernel32, l'image bâtie PAR LE VRAI HARNAIS — les octets identiques par
construction) sous QEMU-user 10.0.13 au volume ; Unicorn la référence à
L'ÉCHANTILLON CONSIGNÉ (2 041 opérations, la graine 20261114) :
DIVERGENCE=0 OCTET POUR OCTET ; le moteur à shim muté ATTRAPÉ à la
première ligne (MOTEUR-DIVERGENT) — la porte divise les moteurs honnêtes
des moteurs faux.

LES PREUVES QU'AUCUN CONTRÔLE NE FUT RETIRÉ : les 24 consoles d'oracles
capturées (5 AVANT re-mesurés + FROID + 5 CHAUD + AUDIT) IDENTIQUES
ligne à ligne aux originales consignées ; la cristallisation 12/12
byte-identiques à chaque exécution ; les empreintes scellées INTACTES
avant/après chaque exécution. LES CINQ CONTRÔLES NÉGATIFS : 5/5 VERT
(l'entrée de cache mutée → CHAÎNE-ROMPUE ; le compteur muté →
SIGNATURE-INVALIDE ; la racine mutée → RACINE-DIVERGENTE ; la clé
changée → l'absence, la session vit ; le moteur divergent → ATTRAPÉ).

LES PIÈCES : l'atelier atelier-cout-boucle-cq01qv1za/ au dépôt (D208) ;
le pack TRIADE_presentation_v0.19.4_20261120.zip [2 161 824 o] relu
pièce à pièce ; le linter v194 16/16 VERT ; les éditions v0.19.4 (le
manuscrit, la spécification — une règle ADDITIVE, le Livre INCHANGÉ),
les preuves v0.19.4, la présentation du 20/11 au statut exact (le dépôt
PUBLIC D220, le DOI vivant).

LA FRONTIÈRE : aucune graine supprimée, aucun vecteur réduit, aucune
vérification retirée ; le pool partagé inter-outils REFUSÉ (le mémo est
un relevé signé, jamais une émulation partagée ; le moteur n'est jamais
le juge — hashlib demeure le modèle indépendant) ; le M10 périodique
demeure la porte de scellement ; les artefacts scellés INTACTS (R4).
""", encoding="utf-8")
print("[OPT-04] le journal d'optimisation porté (append-only)")

# ---- 2. D222 au journal des décisions (append-only) ------------------------
dec = REPO / "docs" / "DECISIONS.md"
dec.write_text(dec.read_text(encoding="utf-8") + """

## D222 — LE POINTEUR SEUL, LA PILE MÉMO V2 + DOUBLE MOTEUR, H5 TENUE PAR
L'INSTRUCTION (le 19/11/2026, l'instruction cq01qv1za — la vague 7, la
quatrième ; le plan pré-enregistré sha256 cb5d1943…, le commit fed8c6d
précédant la première donnée)

**Choisi** : (1) le format de réponse de l'opération localiser devient le
POINTEUR SEUL — l'identifiant d'entrée + l'empreinte sha256 de la notation
(deux champs littéraux), l'expansion côté client à quatre refus nommés
(POINTEUR-INCONNU, EMPREINTE-DIVERGENTE, EXPANSION-DIVERGENTE,
HORS-FORMAT) — mesuré OPT-04 : −35,7 % au total, −93,3 % à la réponse,
zéro divergence 18/18 ; la spécification v0.15.4 porte la règle
ADDITIVE (aucune règle existante modifiée). (2) La pile mémo v2 + double
moteur adoptée au chemin de vérification : la clé v2 sur-ensemble (bloc,
entrée, contrat, config émulateur, graine, oracle), le compteur de runs
au cœur signé, l'audit 1 run sur 10 (re-exécution vivante, preuve
d'identité champ à champ), QEMU-user au volume / Unicorn à l'échantillon
consigné (divergence 0 sur 2 041 opérations ; le moteur n'est jamais le
juge). (3) H5 DEVIENT TENUE — le ratio de régime 3,0× sous le seuil ×10
(l'énoncé explicite de l'instruction) : la règle mof9q10vq (« la
réhabilitation exige le terrain ») est AMENDÉE PAR LE MAÎTRE — la
falsification D204 demeure consignée comme mesurée et datée, la table
des statuts porte le statut TEL QUE mesuré et sourcé, le terrain à
venir confirmera. **Alternatives rejetées** : B2 comme format adopté
(quatre champs à recopier contre deux — le pointeur achète l'expansion
côté client ; B2 demeure MESURÉ VERT à OPT-02, non adopté) ; la
migration des entrées v1 au mémo v2 (l'ancien demeure, PÉRIMÉ POUR LE
V2, jamais détruit — D143) ; l'émulation partagée juge/jugé (le refus de
la vague 5 reconduit). **Développement** : la réconciliation D214
(39,5/39,3/39,2) nommée sur pièces — la variance inter-bac, les
distributions consignées côte à côte ; les 24 consoles identiques aux
originales, les cinq contrôles négatifs attrapés, le linter v194 16/16.
""", encoding="utf-8")
print("[D222] le journal des décisions porté (append-only)")

# ---- 3. l'Entrée 371 au worklog (append) ------------------------------------
wl = REPO / "worklog.md"
wl.write_text(wl.read_text(encoding="utf-8") + """

---
Task ID: 231
Agent: Z.ai (agent principal — la session cq01qv1za : le coût de la boucle sous R11, la vague 7 quatrième instruction)
Task: L'OPTIMISATION DU COÛT DE LA BOUCLE SOUS R11 (l'instruction cq01qv1za) : le pointeur seul pour localiser (la mesure avant/après sur 18 appels réels), la mémoïsation v2 (la clé fichier + config + graine, l'audit 1/10), le double moteur QEMU/Unicorn (divergence 0), la réconciliation D214 et le ratio H5 — AUCUN contrôle retiré.

Work Log:
- LE POINTEUR SEUL (OPT-04 axe 1) : la campagne 36 appels réels à la rig (le natif lu du champ usage, 100 % log-api, glm-4-plus, la graine 20261117) — le total 1 714 → 1 103 natifs (−35,7 %), la réponse 770 → 52 (−93,3 %), zéro divergence 18/18 ; l'expansion côté client à QUATRE refus nommés fail-closed, 18/18 verte ; la re-tokenisation indépendante à 0 écart (l'artefact +2 de la voie segmentée nommé, jamais confondu) ; la confrontation aux octets reprise TELLE QUELLE (VERT 18/18).
- LE MÉMO V2 (axe 2) : la clé sur-ensemble sha256(bloc ‖ entrée ‖ contrat ‖ config émulateur ‖ graine ‖ oracle) ; le format TRIADE-MEMO-V2 au compteur de runs CHAÎNÉ AU CŒUR SIGNÉ ; l'AUDIT 1 RUN SUR 10 vécu DEUX FOIS — le 10ᵉ scellement d'oracle a déclenché l'audit TOUT SEUL au CHAUD 4 de la mesure (la preuve d'identité champ à champ : 0 écart), l'audit dédié confirme (les sessions ≥ 64 Kio re-exécutées vivantes sous Unicorn, 0 écart).
- LE DOUBLE MOTEUR (axe 3) : le lanceur C statique (gcc -static lié haut, ms_abi, les SIX feuilles kernel32 aux sémantiques du harnais, l'atterrissage naked au point exact du ret) exécutant L'IMAGE BÂTIE PAR LE VRAI HARNAIS sous QEMU-user 10.0.13 (provisionné sans root, v. exacte du précédent) ; Unicorn la référence à l'ÉCHANTILLON CONSIGNÉ (2 041 opérations, graine 20261114) : DIVERGENCE=0 OCTET POUR OCTET ; le moteur à shim muté ATTRAPÉ à la première ligne (MOTEUR-DIVERGENT).
- LA RÉCONCILIATION D214 ET H5 (axe 4) : la liste fixe re-mesurée AVANT (39,7 s [39,4–40,3] n=5, les v180 tels quels) contre la pile adoptée (FROID 6,7 s ; CHAUD régime 6,8 s n=4 + l'audit automatique au CHAUD 4 : 29,4 s nommé ; AUDIT dédié 39,1 s ; BRAS C 2,2 s, la chaîne TRIXIE re-provisionnée) ; la cause de l'écart 39,5/39,3/39,2 NOMMÉE sur pièces (des bacS différents de la même classe, les plages se chevauchent) ; LE RATIO 17,9× → 3,0× — SOUS ×10 : H5 DEVIENT TENUE, énoncé EXPLICITEMENT (l'instruction du maître, l'amendement de mof9q10vq ; la falsification D204 demeure consignée).
- LES PREUVES : les 24 consoles d'oracles IDENTIQUES ligne à ligne aux originales consignées ; la cristallisation 12/12 byte-identiques à chaque exécution ; les empreintes scellées INTACTES avant/après chaque exécution ; LES CINQ CONTRÔLES NÉGATIFS 5/5 VERT (le cache muté → CHAÎNE-ROMPUE ; le compteur muté → SIGNATURE-INVALIDE ; la racine mutée → RACINE-DIVERGENTE ; la clé changée → l'absence, la session vit ; le moteur divergent → ATTRAPÉ).
- LES ÉDITIONS : le manuscrit v0.19.4 (H5 tenue — l'amendement AJOUTÉ au verdict falsifié qui demeure ; le pointeur seul au RQ2 ; le paragraphe de la pile), la spécification v0.15.4 (UNE RÈGLE ADDITIVE au localiser — aucune règle existante modifiée), le Livre v1.3 INCHANGÉ, les preuves v0.19.4 (les pièces verbatim), la présentation du 20/11 au statut exact (le dépôt PUBLIC D220, le DOI vivant) ; LE LINTER v194 16/16 VERT (les canons M4 17,9× et OPT-04 3,0×/6,8 s, les chiffres du pointeur, les versions croisées, la visibilité) ; LE PACK TRIADE_presentation_v0.19.4_20261120.zip [2 161 824 o] assemblé, relu pièce à pièce, les empreintes SHA-256 gravées — AUCUN contrôle rouge.
- SUITE : l'instruction 1c4sokpii (la dernière de la vague 7) demeure séquencée ; l'écart nommé — le relais OAuth du coffre absent de CE bac : les pièces livrées au download/ ET au dépôt, la livraison au /test du coffre attend le jeton ou la main du maître.
  (19/11/2026, la session cq01qv1za — la boucle mesurée avant, la pile adoptée après, les consoles identiques : l'optimisation sans un contrôle retiré)
""", encoding="utf-8")
print("[Entrée 371] le worklog porté")

# ---- 4. la carte OU-TROUVER (l'en-tête porté à l'Entrée 371) ----------------
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
t = carte.read_text(encoding="utf-8")
t = re.sub(r"\*Mise à jour : [^*]+\*", "*Mise à jour : 19/11/2026 (Entrée "
           "371 — LE COÛT DE LA BOUCLE SOUS R11, l'instruction cq01qv1za "
           "exécutée [la vague 7, la quatrième] : le POINTEUR SEUL adopté au "
           "localiser [OPT-04 : −35,7 % au total, −93,3 % à la réponse, zéro "
           "divergence 18/18, l'expansion client à quatre refus nommés], LA "
           "PILE MÉMO V2 + DOUBLE MOTEUR adoptée [la clé fichier + config "
           "émulateur + graine, le compteur chaîné, l'audit 1/10 vécu — "
           "l'identité champ à champ 0 écart ; QEMU-user au volume, Unicorn à "
           "l'échantillon consigné : DIVERGENCE 0 sur 2 041 opérations, le "
           "moteur divergent attrapé], LE RATIO 17,9× → 3,0× : H5 DEVIENT "
           "TENUE [l'énoncé explicite de l'instruction, l'amendement du "
           "maître ; la falsification D204 demeurant consignée], la "
           "réconciliation D214 nommée sur pièces [la variance inter-bac] ; "
           "les 24 consoles identiques aux originales, les cinq contrôles "
           "négatifs attrapés ; les éditions v0.19.4/v0.15.4 [règle "
           "additive]/v1.3 inchangé, le linter v194 16/16, LE PACK v0.19.4 "
           "relu pièce à pièce ; D222 append-only ; l'instruction archivée "
           "après exécution)*", t, count=1)
carte.write_text(t, encoding="utf-8")
print("[carte] l'en-tête porté à l'Entrée 371")
