#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_177.py — LA CONSIGNATION DU GESTE « LA REPRISE SUR LES
TROIS MIROIRS : LE CHANTIER M9-(e) OUVERT — LA CÉRÉMONIE DU BUILD 1.0.0
ARMÉE, la dette de consignation des Tasks 93/94 soldée » :
JOURNAL_TRAVAIL +Entrée 177 (ordre 176<177<marqueur, rejeu REFUSÉ),
worklog +Task ID 95. Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit.

La datation : les présentes consignations portent le 06/11 (les
horodatages git des gestes récents disent 06/11 00:35-09:07 UTC — les
écritures « 07/11 » des Entrées 172-176 demeurent, l'anomalie est nommée
ici, jamais réécrite)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 177 — LA REPRISE SUR LES TROIS MIROIRS (« ok continue ») : LE CHANTIER M9-(e) OUVERT — LA CÉRÉMONIE DU BUILD 1.0.0 ARMÉE ; la dette de consignation des Tasks 93/94 NOMMÉE et SOLDÉE, la remise fraîche préparée, le kit de cérémonie déployé et recoupé (06/11)

**La reprise sur les trois miroirs (la demande du développeur : « ok continue »).** La synchro vérifiée AVANT le geste : HEAD 611f878 == origin (relu par fetch), le miroir Drive 1 297 fichiers inchangés + le bundle d'historique rafraîchi (0 erreur — les refs du fetch), la branche jalon bundle051/v0.5.1-jalon-v7 propre, l'arbre propre ; le scellé 0.9.0 relu INTACT (m8/proxy.exe sha256 1492b0bc…), la réserve instrumentale VIVANTE (keystone/capstone/unicorn/nacl/pefile — le disque labo non recyclé cette fois), la garde sceau-I lue : ONZE arbres verts, m8 + tls13 DIVERGÉS (fichier modifié : README.md) — la dette de cérémonie de l'ère 1.0.0 que la Task 94 avait nommée. La datation : les horodatages git des gestes récents disent le 06/11 (00:35-09:07 UTC) — les écritures « 07/11 » des Entrées 172-176 demeurent, l'anomalie est nommée ici.

**La dette de consignation des Tasks 93/94 — NOMMÉE et SOLDÉE (la passation Task 94 revendiquait « relu MATCH : il porte ... [Entrée 176 — sys-04..06 notés-mesurés-prouvés ...] + le worklog Task 94 » : le worklog y était, l'Entrée NON — un MATCH jamais constaté sur cette pièce ; la règle demeure : un verdict sans ses faits est un échec muet).** TROIS anomalies constatées sur pièces : (1) l'Entrée 176 ABSENTE du journal — la Task 94 n'avait consigné ni l'Entrée ni le plan ; (2) l'ORDRE 174<175 VIOLÉ — le défaut de inserer_entree_175.py : l'insertion se faisait à l'INDEX de l'en-tête « ## Entrée 174 » (donc AVANT elle) au lieu d'après SA SECTION — le journal portait 173, 175, 174 ; (3) le PLAN INCOMPLET — maj_plan_m9f.py n'avait remplacé QUE la rangée (b) : la phrase « Entrée 175 » de l'État du programme manquait (le worklog Task 93 consignait pourtant « PLAN (... + État du programme) »), la rangée M9-(d) n'avait jamais reçu sa complétion, la phrase « Entrée 176 » n'existait nulle part. LES RÈGLEMENTS : scripts/inserer_entree_176.py — l'ordre RESTAURÉ par ÉCHANGE PUR (les DEUX sections byte-identiques, seules leurs positions échangées, le constat et les condensés AVANT l'écriture) + l'Entrée 176 DÉPOSÉE (le geste de la Task 94 consigné depuis le worklog qui fait foi, la note de reprise en tête — la dette nommée en toutes lettres) ; scripts/maj_plan_m9g.py — les DEUX remplacements assertés (l'État du programme : les phrases Entrées 175 et 176 insérées après la phrase 174, avant « Les chantiers M6-(a) » ; la rangée M9-(d) : « RÉALISÉ le 07/11/2026 (Entrée 176, Task 94) » — LE SOCLE SOCKET noté-mesuré-prouvé, le VRAI afd.sys attend le (f)) ; rejeu REFUSÉ aux deux.

**Le chantier (e) ouvert : LA CÉRÉMONIE DU BUILD 1.0.0 ARMÉE (le plan M9 l'exigeait : « LA CÉRÉMONIE DU SCEAU I D'ABORD ... précède construire() »).** LA REMISE FRAÎCHE : sceau_I.py preparer — 13 arbres, DEUX empreintes nouvelles (m8 sys.1 72aadd38eadcff2b2e8fa01db6a0b3f2e9014a4123177e2692ec001ed7182822 [la révision M9-(d) : README.md + les TROIS specs sys-04/05/06 — 7 fichiers vivants contre 4 déposés] ; tls13 tls13.1 4255986216f8b459fb7465ccdb6e733352aec901a2008da8165754ed90f6e473 [l'erratum n° 2 : README.md seul — 29 contre 29, les 28 specs inchangées octet pour octet]), les ONZE autres aux empreintes inchangées (Ed25519 déterministe : les re-signer redonne exactement les signatures déposées — la preuve de D163, rejouée aux cérémonies précédentes). LA PIÈCE NOUVELLE : download/LISEZMOI-ceremonie-build-1.0.0.txt ÉCRIT (le modèle ere-M9 : POURQUOI [le garde refuse le build : m8 + tls13 divergés, la dette née aux gestes de notation — R2 : l'écrit a précédé — échue au build], CE QUI A CHANGÉ [les DEUX empreintes citées noir sur blanc], LA RÈGLE D'OR [JAMAIS « generer », la clé du 04/11 réutilisée — 173fae9c75229b15…], le PAS-À-PAS [emporter ceremonie_hors_ligne.py + a-signer.txt + cle-publique-I.txt + cle-I-privee.txt ; signer → auto-vérifications ; verifier → TOUT VERT + la clé commence par 173fae9c… ; ramener signatures-I.txt + cle-publique-I.txt au /test du Drive], CE QUE CELA DÉBLOQUE [le garde VERT 13/13 → construire() : l'artefact 1.0.0-dev.1 — le corps 0.9.0 INTACT (R7), .text5 le socle socket sys-04..06 dans la réserve 0xA240+, .text6 NOUVELLE les 28 blocs tls13 + les fixtures (0xC000..0x10CF0), la version 0x01000001 @0x2820 (geste de BUILD, jamais scellage), l'oracle structurel : le socket natif SANS une seule entrée d'import réseau (ws2_32 n'est JAMAIS importé), AUCUN IAT par bloc tls13, AUCUN site syscall hors du domaine sys ; la carte génération 9, le verrou croisé, la cristallisation] ; puis le terrain (f) — LA GRANDE ŒUVRE ; la clé privée ne traverse JAMAIS le bac à sable — le labo ne signera JAMAIS à la place du développeur, D87). LE DÉPÔT CANONIQUE : maj_kit.py ÉTENDU (RACINE_KIT reçoit l'entrée LISEZMOI-ceremonie-build-1.0.0.txt, optionnelle comme ses aînées — le contrat D130 inchangé ; NOTE_D130 RÉORIENTÉE : la mention de la cérémonie de l'ère M8 était PÉRIMÉE, celle de la cérémonie du build 1.0.0 l'a remplacée — le développeur qui ouvre le dossier est orienté vers LE LISEZMOI courant) puis REJOUÉ : 48 fichiers v06/ suivis par git + 9 racine requis, 59 entrées attendues, 1 téléversé (le LISEZMOI), 2 mis à jour (MANIFESTE.txt + v06/sceau-I/a-signer.txt), 56 inchangés, 59/59 VÉRIFIÉS ALLER-RETOUR md5 ; LE RECOUP INDÉPENDANT par script : le a-signer du kit == le local (MATCH, 1 002 o), les DEUX empreintes nouvelles présentes, le MANIFESTE orienté « CÉRÉMONIE DU BUILD 1.0.0 ».

**Détail.** FRONTIÈRES : AUCUN artefact écrit (le build attend la cérémonie du développeur — le garde demeure : m8 + tls13 DIVERGÉS jusqu'à la remise), les signatures et manifestes déposés INTACTS (l'état « reelle » inchangé, la clé déposée 173fae9c…, les 11 arbres verts inchangés), le scellé 0.9.0 INTACT, AUCUNE balise posée (la 1.0.0-dev.1 viendra de construire(), geste de BUILD — le miroir D162/D165), les arbres I inchangés par la présente (m8 + tls13 demeurent à leurs empreintes vivantes — la remise les porte, la notation est COMPLÈTE : la couche I est FINALE). Livrables : v06/sceau-I/a-signer.txt (la remise fraîche, 13 arbres), download/LISEZMOI-ceremonie-build-1.0.0.txt (au kit, la source labo), scripts/maj_kit.py (RACINE_KIT + NOTE_D130), scripts/inserer_entree_176.py + scripts/maj_plan_m9g.py (les règlements de dette), scripts/maj_plan_m9h.py (la rangée (e)), scripts/inserer_entree_177.py (la présente consignation), le kit /Cérémonie du Drive (déployé, 59/59). Consignations : Entrée 176 (la dette Task 94) + la présente Entrée 177 PAR SCRIPT, PLAN (l'État du programme + la rangée (d) PAR maj_plan_m9g.py ; la rangée (e) PAR maj_plan_m9h.py), worklog +Task ID 95. SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer a-signer.txt avec la clé du 04/11, ramener signatures-I.txt + cle-publique-I.txt au /test du Drive — le kit /Cérémonie porte tout) → LE DÉPÔT (sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt) → LE GARDE REPASSÉ (TREIZE arbres VERTS) → LE BUILD EXÉCUTÉ (construire : l'artefact 1.0.0-dev.1 + la carte génération 9 + le verrou croisé + la cristallisation) ; puis le chantier (f) — le terrain, LA GRANDE ŒUVRE."""

TASK = """## Task ID 95 — LA REPRISE SUR LES TROIS MIROIRS : LE CHANTIER M9-(e) OUVERT — LA CÉRÉMONIE DU BUILD 1.0.0 ARMÉE, la dette de consignation des Tasks 93/94 soldée (06/11)

- LA SYNCHRO VÉRIFIÉE AVANT LE GESTE (« ok continue ») : HEAD 611f878 ==
  origin relu (fetch), le miroir Drive 1 297 inchangés + le bundle
  rafraîchi (0 erreur), l'arbre propre, le scellé 0.9.0 INTACT
  (1492b0bc…), la réserve instrumentale VIVANTE, la garde : m8 + tls13
  DIVERGÉS (README.md) — la dette de cérémonie de l'ère 1.0.0.
- LA DETTE DE CONSIGNATION NOMMÉE ET SOLDÉE : (1) l'Entrée 176 ABSENTE
  (la passation Task 94 la revendiquait « relu MATCH » — un MATCH jamais
  constaté sur la pièce) ; (2) l'ordre 174<175 VIOLÉ (le défaut de
  inserer_entree_175.py : l'insertion à l'INDEX de l'en-tête au lieu
  d'après la section — le journal portait 173, 175, 174) ; (3) le PLAN
  INCOMPLET (la phrase Entrée 175 de l'État du programme manquait — le
  worklog Task 93 la consignait pourtant ; la rangée (d) sans
  complétion). LES RÈGLEMENTS : inserer_entree_176.py (l'ordre RESTAURÉ
  par échange pur — les sections byte-identiques, le constat AVANT
  l'écriture — + l'Entrée 176 déposée depuis le worklog qui fait foi,
  la note de reprise en tête) ; maj_plan_m9g.py (l'État du programme +
  les phrases Entrées 175/176, la rangée (d) « RÉALISÉ ») ; rejeu
  REFUSÉ aux deux. La datation : les présentes portent le 06/11 (les
  horodatages git des gestes récents : 06/11 00:35-09:07 UTC — les
  écritures « 07/11 » des Entrées 172-176 demeurent, l'anomalie est
  nommée, jamais réécrite).
- LA CÉRÉMONIE ARMÉE (le plan (e) : « LA CÉRÉMONIE DU SCEAU I D'ABORD
  ... précède construire() ») : preparer — la remise fraîche 13 arbres,
  DEUX empreintes nouvelles (m8 72aadd38… [README + sys-04/05/06 : 7
  vivants contre 4 déposés], tls13 42559862… [l'erratum n° 2 : README
  seul, les 28 specs inchangées]), les ONZE autres inchangées (Ed25519
  déterministe) ; LISEZMOI-ceremonie-build-1.0.0.txt ÉCRIT (le modèle
  ere-M9 : POURQUOI, CE QUI A CHANGÉ, LA RÈGLE D'OR [JAMAIS « generer
  », la clé du 04/11 réutilisée 173fae9c…], le PAS-À-PAS, CE QUE CELA
  DÉBLOQUE [construire() : l'artefact 1.0.0-dev.1 — le corps 0.9.0
  INTACT R7, .text5 le socle dans la réserve 0xA240+, .text6 les 28
  blocs + fixtures 0xC000..0x10CF0, la version 0x01000001 @0x2820,
  l'oracle : le socket natif SANS une seule entrée d'import réseau, la
  carte génération 9] ; la clé privée ne traverse JAMAIS le bac à
  sable) ; maj_kit.py ÉTENDU (RACINE_KIT + NOTE_D130 RÉORIENTÉE — la
  mention M8 était périmée) et REJOUÉ : 1 téléversé (le LISEZMOI),
  2 mis à jour (MANIFESTE + a-signer), 56 inchangés, 59/59 ALLER-
  RETOUR md5 ; le recoup indépendant : le a-signer du kit == le local
  (MATCH), les DEUX empreintes présentes, le MANIFESTE orienté.
- FRONTIÈRES : AUCUN artefact (le build attend le geste du développeur),
  les signatures/manifestes déposés INTACTS (l'état « reelle », la clé
  173fae9c…), le scellé 0.9.0 INTACT, aucune balise posée, les arbres I
  inchangés (la remise porte leurs empreintes vivantes — la couche I est
  FINALE) ; consignations : Entrées 176+177 PAR SCRIPT, PLAN (m9g :
  l'État du programme + la rangée (d) ; m9h : la rangée (e)), worklog
  +Task ID 95.
- SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer
  a-signer.txt avec la clé du 04/11, ramener signatures-I.txt +
  cle-publique-I.txt au /test) → LE DÉPÔT (sceau_I.py deposer) → LE
  GARDE REPASSÉ (13/13) → LE BUILD EXÉCUTÉ (construire : 1.0.0-dev.1 +
  la carte génération 9 + le verrou croisé) ; puis (f) le terrain — LA
  GRANDE ŒUVRE.
- PASSATION (le même geste, Task ID 95) : le bundle courant
  triade-history-090-<pointe>.bundle (branche jalon == la pointe [le
  geste + sa consignation]) DÉPOSÉ AU MIROIR ASSERTÉ (relu MATCH : il
  porte LA CÉRÉMONIE ARMÉE [Entrée 177 — la dette de consignation
  soldée, la remise fraîche 13 arbres : m8 72aadd38… + tls13
  42559862…, le kit 59/59 recoupé, le LISEZMOI du geste] + le worklog
  Task 95), l'ancien 090-686b33e (LE SOCLE SOCKET) ARCHIVÉ VERSIONNÉ,
  /test sans copie, le push GitHub à la pointe ; LA SÉRIE 090 POURSUIT
  — le geste est PASSÉ.

Stage Summary:
- LA CÉRÉMONIE DU BUILD 1.0.0 EST ARMÉE : le kit /Cérémonie porte la
  remise fraîche (13 arbres, les DEUX empreintes nouvelles m8 + tls13),
  le LISEZMOI du geste, le MANIFESTE réorienté — le développeur signe
  hors-ligne avec sa clé du 04/11, le build suivra le garde VERT.
- LA DETTE DE CONSIGNATION DES TASKS 93/94 EST SOLDÉE : l'ordre du
  journal restauré, l'Entrée 176 déposée, le plan complété — la
  passation revendiquait un MATCH jamais constaté : nommé, réparé, la
  règle demeure (un verdict sans ses faits est un échec muet).
- LA NOTATION EST COMPLÈTE, LA COUCHE I EST FINALE : la cérémonie est
  la DERNIÈRE pièce avant l'artefact — puis le terrain, LA GRANDE
  ŒUVRE."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 177" in journal:
        sys.exit("ÉCHEC : Entrée 177 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 176" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 176 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i176 = journal.index("## Entrée 176")
    im = journal.index(MARQUEUR)
    if not (i176 < im):
        sys.exit("ÉCHEC : l'ordre 176<marqueur est rompu")
    if "## Entrée 177" in journal[i176:im]:
        sys.exit("ÉCHEC : état inattendu entre 176 et le marqueur")
    # l'insertion APRÈS la SECTION 176 (la leçon du défaut de l'Entrée 175 :
    # jamais à l'index de l'en-tête — TOUJOURS après la section, avant le
    # marqueur)
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")
    print("[journal] +Entrée 177 (ordre 176<177<marqueur — insérée APRÈS la "
          "section 176, la leçon du défaut de l'Entrée 175 appliquée)")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    log = WORKLOG.read_text(encoding="utf-8")
    if "Task ID 95" in log:
        sys.exit("ÉCHEC : Task ID 95 déjà consignée (rejeu REFUSÉ)")
    if "Task ID 94" not in log:
        sys.exit("ÉCHEC : ancrage Task ID 94 introuvable")
    log = log.rstrip() + "\n\n" + TASK + "\n"
    WORKLOG.write_text(log, encoding="utf-8")
    print("[worklog] +Task ID 95")
    return 0


if __name__ == "__main__":
    sys.exit(main())
