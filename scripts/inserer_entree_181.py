#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_181.py — LA CONSIGNATION DU GESTE « LE SECOND RUN TERRAIN
(f) REÇU : LE JOURNAL SEUL — T0/T1/T2 VERT (la réparation de l'erratum n° 6
PROUVÉE sur la machine réelle, le VRAI afd.sys franchi pour la première
fois), LE RUN INTERROMPU SANS VERDICT entre T2 VERT et la ligne
« T3 : OUVRIR » (fenêtre Python pur, AUCUN appel machine en vol) ; LE GESTE
RENDU AU DÉVELOPPEUR » : JOURNAL_TRAVAIL +Entrée 181 (ordre 180<181<marqueur,
rejeu REFUSÉ), worklog +Task ID 99. Tout ancrage absent = ÉCHEC NOMMÉ, rien
n'est écrit.

La datation : la présente porte le 06/11 au soir (le geste du développeur
« preuves deposees dans le dossier /test du drive » reçu le 06/11 — le run :
journal muet à 16:56:09, dépôt au coffre 16:56:34, analyse labo 17:03-17:15)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 181 — LE SECOND RUN TERRAIN (f) REÇU (« preuves deposees dans le dossier /test du drive ») : LE JOURNAL SEUL — T0/T1/T2 VERT (LA RÉPARATION DE L'ERRATUM n° 6 PROUVÉE SUR LA MACHINE RÉELLE, LE VRAI afd.sys FRANCHI POUR LA PREMIÈRE FOIS), LE RUN INTERROMPU SANS VERDICT entre T2 VERT et la ligne « T3 : OUVRIR » (fenêtre PYTHON PUR, AUCUN appel machine en vol) ; LE GESTE RENDU AU DÉVELOPPEUR — la console répond (06/11 au soir)

**Le geste du développeur reçu, la pièce lue octet par octet — le run est INCONCLU, et c'est nommé.** LE RAPATRIEMENT (scripts/rapatrier_preuves_m9f.py rejoué à 17:03) : le coffre /test/preuves-m9f/ ne porte QUE scenario-m9f-journal.log (171 o, md5 24680ac9…) à côté du LISEZMOI-preuves.txt du réceptacle (2 094 o, md5 0387616d… — inchangé depuis son ré-armement) ; le TRIO DU RUN (temoin-m9f.txt, VERDICT-run-m9f.txt) ABSENT → le script REFUSE (code 2, « le trio du run absent du coffre » — la garde fait son métier) ; la pièce présente rapatriée à la main, md5 contrôlé contre les métadonnées Drive (171 o, MATCH par relecture). LE JOURNAL LU SUR PIÈCES : TROIS lignes, toutes à 16:56:09 — « T0 VERT » ; « T1 VERT : les DEUX lecteurs d'accord sur les TROIS noms » ; « T2 VERT : l'endpoint AFD TCP IPv4 établi (le VRAI afd.sys, zéro ws2_32) » — LA TERMINAISON CRLF CONSTATÉE (171 o == la ré-écriture EXACTE des trois lignes par _ecrire_journal() en mode texte Windows, reconstituée octet pour octet au geste même : la pièce EST native, jamais coupée à la main) ; LA LIGNE T1 EST LA PREUVE TERRAIN DE LA RÉPARATION : l'erratum n° 6 est mort — le kit CORRIGÉ md5 7d5380ce… a bien été exécuté, le refus -3 « répertoire export absent » NE S'EST PAS REPRÉSENTÉ, les DEUX lecteurs (le miroir Python ET le bloc sys-02 de l'artefact) SONT D'ACCORD sur les SSN des TROIS noms du transport ; LA LIGNE T2 EST UNE PREMIÈRE ABSOLUE : le socle socket court POUR LA PREMIÈRE FOIS sur le VRAI afd.sys — l'endpoint TCP ÉTABLI vers www.cloudflare.com:443 par sys-04 (create + bind + connect, TROIS appels NT, zéro ws2_32) : LE PLUS LOIN QUE LE PROGRAMME AIT JAMAIS ÉTÉ SUR LE TERRAIN.

**L'interruption nommée sur pièces — évidence avant correctif (D54/D68/D98), le kit N'EST PAS convaincu.** LA FENÊTRE : le journal meurt après T2 VERT ; la ligne suivante de la source serait « T3 : OUVRIR — la poignée ENTIÈRE par la machine d'états (le socle câblé aux SYSCALLS DIRECTS) » — journalée AVANT l'appel TLS27 (la ligne 597 contre la 599) ; entre les deux court UN SEGMENT PYTHON PUR : le print de l'entête T3, os.urandom ×2, les temoin() d'aléa et de clés, l'échelle x25519 RFC 7748 refaite en Python, la création des rappels ctypes, les tampons session/kit96 — LA PREMIÈRE INSTRUCTION EN EST UN PRINT CONSOLE, AUCUN APPEL MACHINE en vol : ni l'artefact, ni la machine d'états, ni sys-0x ne sont entrés en scène ; le témoin et le verdict NE NAISSENT qu'à la fin (_verdict()) — leur absence du dépôt est COHÉRENTE, jamais un mystère. L'HORLOGE DES PIÈCES : le mtime du journal (16:56:09.463 — la seconde même de la ligne T2) contre le createdTime Drive (16:56:34) : le run s'est tu DANS LA SECONDE de T2, le dépôt suit de 25 secondes ; un process vivant traverse la fenêtre en millisecondes — à 16:56:34 le run était déjà GELÉ ou MORT. LES CANDIDATS NOMMÉS : (a) LA CONSOLE GELÉE — le mode Sélection QuickEdit de la console Windows (un clic dans la fenêtre) gèle TOUT process sur son prochain print : le gel tomberait PRÉCISÉMENT sur le premier print de la fenêtre, la fenêtre RESTE OUVERTE (le titre porte « Sélection »), ÉCHAP reprend le run LÀ OÙ IL S'EST TU ; (b) LA MORT DU PROCESSUS — fenêtre fermée, Ctrl+C, arrêt : rien sur les pièces ne la distingue de (a) ; (c) LE KIT EST ACQUITTÉ PAR ÉLIMINATION — la fenêtre de mort ne porte AUCUN octet du kit (des prints et du Python pur), et le premier run (16:17:51) avait TRAVERSÉ tous les prints jusqu'à son verdict sur la MÊME console : la console sait imprimer, l'incident est LOCAL ; LA LIMITE nommée : le journal seul ne départage pas (a) de (b) — la console du développeur détient la réponse, et c'est exactement ce que le geste lui demande.

**Le geste rendu au développeur — trois temps, un seul envoi.** (i) SI LA CONSOLE EST ENCORE OUVERTE ET FIGÉE : appuyer sur ÉCHAP (ou ENTRÉE) — le run REPREND à l'instant même où il s'est tu (la ligne « T3 : OUVRIR » suit) ; un verdict « -7 LE TRANSPORT EN ÉCHEC » est alors POSSIBLE ET HONNÊTE : la connexion TCP établie à 16:56:09 est restée muette des dizaines de minutes, le serveur a pu la refermer — c'est la nature du transport, jamais une panne du kit ; (ii) SI LA FENÊTRE EST FERMÉE OU MORTE : relancer `python scenario-m9f.py` (réseau vivant, ~10 s) dans le dossier du kit ; (iii) DANS LES DEUX CAS : renvoyer preuves-m9f/ ENTIER au coffre /test/preuves-m9f/ — le VERT comme le ROUGE nommé : le labo recoupe sur pièces (D138/D145/D148) et, si elles établissent le critère, LA FINALE 1.0.0 est posée (fait de carte, D104) : le jalon M9 franchi — LA GRANDE ŒUVRE.

**Détail.** FRONTIÈRES : le kit du coffre INCHANGÉ (AUCUN correctif : RIEN ne condamne le kit — kit-m9f.zip relu au /test md5 7d5380ce…, l'artefact 1.0.0-dev.2 relu INTACT sha256 d892893469608fd6… 65 024 o re-haché au geste même, le scénario DU KIT == la source du dépôt OCTET POUR OCTET — dézippé et différencié au geste même, 38 992 o), le scellé 0.9.0 INTACT (m8/proxy.exe 1492b0bc… non touché), les arbres I inchangés, AUCUNE balise posée (le run est INCONCLU, pas ROUGE : la finale 1.0.0 attend un run COMPLET vert — D104), la clé privée jamais traversée (D87) ; l'archive du premier run INTACTE aux archives-preuves (D99 : zéro mélange — le réceptacle ré-armé ne portait que son LISEZMOI avant la pièce). Livrables : download/preuves-run-m9f/scenario-m9f-journal.log (LA PIÈCE du second run, md5 24680ac9…) + download/preuves-run-m9f/LISEZMOI-preuves.txt (md5 0387616d…) ; NOTE d'hygiène : le dossier local download/preuves-run-m9f/ porte encore les copies de travail du premier run (temoin/verdict — archivées au coffre par la Task 98) à côté du journal du second : le rapatriement du run COMPLET les écrira toutes (le dossier est dédié au run m9f, jamais aux archives). Consignations : la présente Entrée 181 PAR SCRIPT, PLAN (maj_plan_m9m.py : la rangée (f) + l'État du programme), worklog +Task ID 99. SUITE : le geste du développeur ci-dessus — preuves-m9f/ ENTIER au coffre → le recoup (D138/D145/D148) → si vert : LA FINALE 1.0.0 (fait de carte — D104) : le jalon M9 franchi — LA GRANDE ŒUVRE."""

TASK = """## Task ID 99 — LE SECOND RUN TERRAIN (f) REÇU (« preuves deposees dans le dossier /test du drive ») : LE JOURNAL SEUL, LE RUN INTERROMPU SANS VERDICT — T0/T1/T2 VERT NOMMÉS (la réparation de l'erratum n° 6 PROUVÉE sur la machine réelle, le VRAI afd.sys franchi pour la première fois) ; l'interruption nommée entre T2 VERT et la ligne « T3 : OUVRIR » (fenêtre Python pur, AUCUN appel machine en vol) ; LE GESTE RENDU AU DÉVELOPPEUR (06/11 au soir)

Work Log:
- LE RAPATRIEMENT (17:03) : /test/preuves-m9f/ ne porte QUE le journal
  (171 o, md5 24680ac9…) + le LISEZMOI du réceptacle (0387616d…) ;
  rapatrier_preuves_m9f.py REFUSE (code 2 : le trio absent — la garde
  fait son métier) ; la pièce rapatriée à la main, md5 contrôlé par
  relecture.
- LE JOURNAL LU SUR PIÈCES : TROIS lignes CRLF à 16:56:09 — T0 VERT ;
  T1 VERT (les DEUX lecteurs d'accord sur les TROIS noms : LA
  RÉPARATION DE L'ERRATUM n° 6 PROUVÉE SUR LA MACHINE RÉELLE — le
  refus -3 ne s'est pas représenté, le kit corrigé 7d5380ce… exécuté) ;
  T2 VERT (l'endpoint AFD TCP IPv4 ÉTABLI vers cloudflare:443 par
  sys-04 en TROIS appels NT : LE VRAI afd.sys FRANCHI POUR LA
  PREMIÈRE FOIS — le plus loin du programme sur le terrain) ; 171 o
  == la ré-écriture EXACTE des trois lignes par _ecrire_journal en
  mode texte Windows (CRLF) : la pièce EST native.
- L'INTERRUPTION NOMMÉE : le journal meurt après T2 VERT, la ligne
  suivante (« T3 : OUVRIR ») est journalée AVANT l'appel TLS27 (597
  contre 599) — entre les deux : UN SEGMENT PYTHON PUR (le print
  d'entête T3, os.urandom, l'échelle x25519 en Python, les rappels
  ctypes, les tampons), LA PREMIÈRE INSTRUCTION UN PRINT CONSOLE,
  AUCUN appel machine en vol ; le témoin/le verdict ne naissent qu'à
  la fin (_verdict) : leur absence est COHÉRENTE ; l'horloge des
  pièces : mtime 16:56:09.463 == la seconde de T2, dépôt Drive
  16:56:34 — à 16:56:34 le run était déjà GELÉ ou MORT (un process
  vivant traverse la fenêtre en millisecondes).
- LES CANDIDATS (évidence avant correctif — D54/D68/D98) : (a) LA
  CONSOLE GELÉE (QuickEdit : un clic dans la fenêtre gèle tout print ;
  la fenêtre reste OUVERTE, « Sélection » au titre, ÉCHAP reprend le
  run là où il s'est tu) ; (b) LA MORT DU PROCESSUS (fenêtre fermée,
  Ctrl+C, arrêt — indistinguable sur pièces) ; (c) LE KIT ACQUITTÉ
  PAR ÉLIMINATION : la fenêtre ne porte AUCUN octet du kit, et le
  premier run (16:17) avait traversé tous les prints jusqu'au verdict
  sur la MÊME console — l'incident est LOCAL ; la limite nommée : le
  journal seul ne départage pas, la console du développeur répond.
- LE GESTE RENDU : (i) console figée → ÉCHAP (le run REPREND ; un
  « -7 LE TRANSPORT EN ÉCHEC » est possible et HONNÊTE : la connexion
  muette depuis 16:56 a pu être refermée par le serveur — la nature
  du transport, jamais une panne du kit) ; (ii) fenêtre morte →
  RELANCER python scenario-m9f.py (réseau vivant, ~10 s) ; (iii) PUIS
  renvoyer preuves-m9f/ ENTIER au coffre → le labo recoupe → si
  vert : LA FINALE 1.0.0 (fait de carte, D104) — LA GRANDE ŒUVRE.
- FRONTIÈRES : le kit INCHANGÉ au /test (7d5380ce… relu — AUCUN
  correctif : rien ne condamne le kit), l'artefact d8928934… INTACT
  (re-haché au geste), le scénario du kit == la source du dépôt
  OCTET POUR OCTET (38 992 o, différencié au geste), le scellé 0.9.0
  INTACT, AUCUNE balise (run INCONCLU : la finale attend un run
  COMPLET vert), l'archive du premier run intacte (D99 zéro
  mélange) ; livrables : download/preuves-run-m9f/scenario-m9f-
  journal.log (md5 24680ac9…) + LISEZMOI-preuves.txt (0387616d…) ;
  consignations : Entrée 181 PAR SCRIPT, PLAN (maj_plan_m9m.py :
  rangée (f) + État), worklog +Task ID 99.
- SUITE : LE GESTE DU DÉVELOPPEUR — preuves-m9f/ ENTIER au coffre →
  le recoup (D138/D145/D148) → si vert : LA FINALE 1.0.0, le jalon
  M9 franchi — LA GRANDE ŒUVRE.

Stage Summary:
- LE SECOND RUN EST LE PLUS LOIN QUE LE PROGRAMME AIT JAMAIS ÉTÉ SUR
  LE TERRAIN : T1 VERT prouve la réparation de l'erratum n° 6 SUR LA
  MACHINE RÉELLE, T2 VERT établit la connexion TCP par LE VRAI
  afd.sys — mais le run est INCONCLU : mort silencieuse dans une
  fenêtre Python pur dont la première instruction est un print
  console, AUCUN appel machine en vol, le kit acquitté par
  élimination.
- LE JOURNAL SEUL NE DÉPARTAGE PAS LA CONSOLE GELÉE (Échap reprend)
  DE LA MORT DU PROCESSUS (relancer) : le geste rendu au développeur
  couvre les deux — puis preuves-m9f/ ENTIER, et si vert : LA FINALE
  1.0.0, le jalon M9 franchi — LA GRANDE ŒUVRE."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 181" in journal:
        sys.exit("ÉCHEC : Entrée 181 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 180" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 180 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i180 = journal.index("## Entrée 180")
    im = journal.index(MARQUEUR)
    if not (i180 < im):
        sys.exit("ÉCHEC : l'ordre 180<marqueur est rompu")
    if "## Entrée 181" in journal[i180:im]:
        sys.exit("ÉCHEC : état inattendu entre 180 et le marqueur")
    # l'insertion APRÈS la SECTION 180 (la leçon de l'Entrée 175 :
    # TOUJOURS après la section, avant le marqueur)
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 99" in worklog:
        sys.exit("ÉCHEC : Task ID 99 déjà consigné (rejeu REFUSÉ)")
    if "## Task ID 98" not in worklog:
        sys.exit("ÉCHEC : ancrage Task ID 98 introuvable")
    worklog = worklog.rstrip("\n") + "\n\n" + TASK + "\n"
    WORKLOG.write_text(worklog, encoding="utf-8")

    print("[consignation] Entrée 181 déposée au journal "
          "(ordre 180<181<marqueur)")
    print("[consignation] Task ID 99 déposé au worklog")
    print("[consignation] la relecture fait foi :")
    j = JOURNAL.read_text(encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    assert j.index("## Entrée 180") < j.index("## Entrée 181") < j.index(MARQUEUR)
    assert "## Entrée 181" in j and "24680ac9" in j
    assert "T3 : OUVRIR" in j and "QuickEdit" in j
    assert "T2 VERT" in j and "VRAI afd.sys" in j and "INCONCLU" in j
    assert "## Task ID 99" in w and w.index("## Task ID 98") < w.index("## Task ID 99")
    assert "INCONCLU" in w and "ÉCHAP" in w
    print("[consignation] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
