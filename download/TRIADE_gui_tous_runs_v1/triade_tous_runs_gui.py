#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
triade_tous_runs_gui.py — TRIADE : TOUS LES RUNS, PAS À PAS · GUI v1.0.0
=========================================================================
UN SEUL FICHIER PYTHON, ZÉRO LIGNE DE COMMANDE (si ce n'est le lancer) —
le GUI qui conduit, geste après geste, TOUS LES TESTS ET RUNS du projet
(la commande du développeur : « fais un GUI pas a pas tout au clic pour
la campagne d204 — fais ça pour tous les tests et runs quand c'est
possible ») :

    — LA CAMPAGNE D204, la comparaison des workflows aux DEUX bras
      (le plan pré-enregistré VERROUILLÉ — sha256 a78caf8c… consigné
      AVANT toute mesure) : le verrou des HUIT pièces, l'atelier, la
      calibration, les QUATORZE unités (six blocs × deux bras + la
      partie réaliste EN ATTENTE), le carnet M3, les livraisons M1,
      les défauts nommés, le chronomètre M4, le suivi ;
    — LES SEPT RUNS 1-CLIC, chacun conduit pas à pas : LE FICHIER
      (choisi, recoupé contre son empreinte GRAVÉE — fail-closed),
      LE RUN (la console officielle du fichier autonome, INTACTE),
      LA PIÈCE (le témoin ouvert au bloc-notes, le coffre /test au
      navigateur — dater, signer DE VOTRE MAIN, renvoyer le dossier
      ENTIER), L'ÉTAT (ce que chaque run attend, nommé, jamais
      maquillé) :
        LE DIAGNOSTIC MACHINE    — choisit la machine du geste B ;
        LE GESTE B SHA-NI        — exige un silicium qui A SHA-NI ;
        LA VOIE 1 QEMU (M7D)     — le rejeu, le qemu-riscv64 embarqué ;
        LA VOIE 2 QEMU (SHANI)   — le rejeu, l'ARTEFACT TCG consigné ;
        LE TÉMOIN VITRINE (loupe)— deux fenêtres que VOUS fermez ;
        LE SÉQUESTRE D183        — la répétition générale, la
                                   cérémonie à la machine HORS-LIGNE ;
        LA RÉPLICATION (κ)       — l'autotest, le κ le jour des DEUX
                                   jeux d'annotations.
    — LES CHAÎNES DÉJÀ FERMÉES, nommées au catalogue (le kit-2 dudect
      N=200/N=400, le constat-ARM, la cérémonie d'ère — un registre) :
      l'histoire demeure, D143, jamais rejouée par ce GUI.

LES SEPT ÉTAPES DU GUI (tout au clic, dans l'ordre) :
    ÉTAPE 1  LE CATALOGUE — tous les tests et runs, leurs états
             (OUVERT / FACULTATIF / EN ATTENTE / FERMÉ), l'ordre des
             gestes restants ; CONDUIRE le run choisi ;
    ÉTAPE 2  LA CAMPAGNE · LE VERROU — les HUIT pièces recoupées
             sha256 par sha256 (le plan VERROUILLÉ a78caf8c… en tête) ;
             l'ATELIER de campagne naît ici (les COPIES datées des
             trois gabarits — les originaux scellés INTACTS) ;
    ÉTAPE 3  LA CAMPAGNE · LA CALIBRATION — la preuve d'horloge du
             chronomètre (2 s, la pause portable v3) — un DRY-RUN,
             jamais une mesure (CA1) ;
    ÉTAPE 4  LA CAMPAGNE · LES QUATORZE UNITÉS — chacune en SEPT
             onglets : LE KIT, LE RUN, LE TÉMOIN, LE CARNET M3, LA
             LIVRAISON M1 (la cap tenue), LES DÉFAUTS M1, LE CHRONO M4 ;
    ÉTAPE 5  LES AUTRES RUNS — les sept tests 1-clic, chacun son
             conduite pas à pas (le fichier recoupé, le run lancé
             INTACT, la pièce signée de votre main, l'état nommé) ;
    ÉTAPE 6  LE SUIVI — la campagne (les comptes SEULS, CA7) et l'état
             de tous les runs ;
    ÉTAPE 7  LES PIÈCES — où vit quoi, le plan, la console officielle,
             le coffre /test, les frontières.

CE QUE CE GUI NE FERA JAMAIS (les frontières du protocole, tenues par
construction) :
    — DATER ni SIGNER un témoin (votre main, toujours — D99) ;
    — DÉPOSER au coffre (le renvoi du dossier de run ENTIER appartient
      au développeur — le GUI ouvre le coffre, jamais il n'écrit) ;
    — FABRIQUER un chiffre (CA5/CA6 : aucun résultat n'existe avant
      sa mesure ; le labo prépare, recoupe et consigne) ;
    — TOUCHER les originaux scellés (le GUI ne vit que sur les COPIES
      datées de l'atelier — la confrontation des empreintes, CA5) ;
    — DÉPASSER la cap pré-enregistrée (au plus TROIS livraisons par
      bloc, DOUZE par application — l'arrêt au premier vert, § 7) ;
    — COURIR un kit à votre place (le fichier 1-clic et le lanceur
      officiel courent dans LEUR console, INTACTS — CA6) ;
    — REJOUER une chaîne fermée (le kit-2, le constat-ARM : l'histoire
      demeure ; les rejeux voie 1 / voie 2 sont FACULTATIFS et nommés
      tels — D165 : le rejeu ne re-scelle rien).

Lancement :
    double-cliquez LANCER-GUI-TOUS-RUNS.bat  (le kit complet),
    ou :  python3 triade_tous_runs_gui.py [--kit DOSSIER] [--selftest]

L'ÉDITION v1.0.0 (le 14/11/2026) — LA PREMIÈRE ÉDITION DU GUI DE TOUS
LES RUNS : le GUI de campagne v1.0.1 (le correctif encodage) demeure au
coffre, INTACT (D143 : jamais jeté) ; le présent GUI porte sa campagne
OCTET POUR OCTET (les MÊMES HUIT pièces, les MÊMES empreintes) et
AJOUTE les sept runs 1-clic au catalogue. LA CONTINUITÉ : si l'état du
GUI campagne v1 vit à côté (etat-campagne-d204.json), il est IMPORTÉ au
premier ouverture — l'atelier, la calibration et les kits choisis
survivent ; l'atelier se retrouve aussi par le bouton « CHOISIR
L'ATELIER EXISTANT… » de l'étape 2 (la campagne continue, jamais ne
recommence).
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

# ===========================================================================
# SECTION A — LES CONSTANTES DU KIT (les pièces, le plan, les catalogues)
# ===========================================================================

VERSION = "1.0.0"
EDITION = "la première édition, le 14/11/2026"

GUI_DIR = pathlib.Path(__file__).resolve().parent
FICHIER_ETAT = GUI_DIR / "etat-tous-runs.json"
FICHIER_ETAT_V1 = "etat-campagne-d204.json"     # le GUI campagne v1.0.1
DOSSIER_LOGS = GUI_DIR / "TRIADE_logs"

# le coffre — le dossier /test du Drive « Triade »
COFFRE_TEST_URL = ("https://drive.google.com/drive/folders/"
                   "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0")

# LES HUIT PIÈCES de campagne-d204 — celles du GUI campagne v1.0.1,
# OCTET POUR OCTET (le chronomètre v3, le compteur v2 — l'édition sans
# faute de page de codes ; les SIX autres celles du kit 1-clic v2 de
# l'Entrée 273) — sha256 gravées : la transparence, la confrontation à
# chaque geste (CA5)
EMPREINTES_PIECES = {
    "LANCER-CAMPAGNE-D204.bat":
        "5f1ffa9776d296b809ada54217e86f8e4789bc865a5d77e0402ea222e021d1a9",
    "LISEZMOI-comparaison.txt":
        "609a0e81b99376e698ef0bd90e89a0537ba97caf88cb8d9ee67637227f282beb",
    "PLAN_PREREGISTRE_COMPARAISON.md":
        "a78caf8c0cb9498446a91d18d0f8a02ee16b6893d4fe4ce49843397f30240255",
    "carnet_temps_humain.csv":
        "ba736b1f1e153e18a8c9bf6e97d73c04e456dcf136ede93e278802eca98baf0e",
    "chronometre_verification.py":
        "ff0c96522fa558ccc37af6f16b9d63cc91ced71ae81c699c2cd26c1a0853a58f",
    "compter_tokens.py":
        "e2939ef9d3ef7f228c1881b55744e182238fbb489b58d30595882d926eea26e5",
    "defauts.csv":
        "e2756e76a84ac9c5d552ca01da26dc228e8b23c50b05689cb1cf9cee11380497",
    "livraisons.csv":
        "3d7d13f033b1176efba8d4096b4512655805897e89127461fa25fc56cc8e2d10",
}

VERROU_PLAN = EMPREINTES_PIECES["PLAN_PREREGISTRE_COMPARAISON.md"]
TOLERANCE_CALIBRATION = 0.05   # s — la preuve d'horloge du chronomètre

# LA PARTIE CONTRÔLÉE — les six blocs (les MÊMES contrats que D193/D195)
BLOCS = [
    ("loupe-01", "ouvrir"),
    ("loupe-02", "lire"),
    ("loupe-05", "sha256"),
    ("loupe-08", "ligne"),
    ("loupe-13", "recherche"),
    ("loupe-16", "saisie"),
]
BRAS = [("T", "TRIADE — la notation scellée"), ("C", "standard — C + gcc")]

# LA CAP pré-enregistrée (§ 7 du plan) : au plus TROIS livraisons par
# bloc, DOUZE par application — l'arrêt au premier vert, la cap sans
# vert = CENSURÉE (rapportée telle quelle, jamais prolongée)
CAP_BLOC = 3
CAP_APP = 12

# LES GESTES M3 du carnet (§ 4-M3 du plan) — par bras
GESTES_M3 = {
    "T": ["cristallisation", "garde", "cérémonie de scellement"],
    "C": ["tag-backup", "relecture de livraison"],
    "X": ["revue des livrables", "arbitrage d'un défaut"],
}

# LES LISTES FIXES M4 (§ 4-M4 du plan) — toute commande hors liste est
# un ÉCART NOMMÉ ; le GUI les rappelle avant chaque chronométrage
LISTES_M4 = {
    "T": ["le garde des arbres signés",
          "le round-trip de la notation livrée",
          "l'oracle du bloc au périmètre livré",
          "le build (la recomposition de la pièce)"],
    "C": ["la compilation gcc -O2 (la commande consignée)",
          "la suite de tests du camp C",
          "les contrôles binaires (empreintes, format)"],
}

# LES PHASES M2 (l'information du carnet de tokens — l'instrument du labo)
PHASES_M2 = ("spec", "notation", "source-c", "tests-c", "oracle", "build",
             "correctif", "ceremonie", "revue", "analyse")

# les colonnes EXACTES des gabarits (jamais retouchées — D202/M3/M1)
COLONNES_CARNET = ["date", "bras", "tache", "geste", "debut", "fin",
                   "minutes", "notes"]
COLONNES_LIVRAISONS = ["livraison", "bras", "tache", "numero_iteration",
                       "date_kit", "date_run", "verdict", "recoup"]
COLONNES_DEFAUTS = ["livraison", "bras", "tache", "classe", "mecanisme",
                    "cote", "piece_appui", "exclusion", "raison_exclusion"]

# ---------------------------------------------------------------------------
# LES FICHIERS 1-CLIC — les empreintes GRAVÉES des sept fichiers autonomes
# (l'édition FICHIERS-1CLIC du 13/11, l'Entrée 270 — celles du kit des
# runs restants de l'Entrée 273 pour geste-b/séquestre/réplication,
# INTACTES octet pour octet) : le GUI recoupe CHAQUE fichier choisi
# contre sa table AVANT tout lancement — un octet divergent, le run ne
# part pas (fail-closed). La console de campagne existe en TROIS
# éditions (v1/v2/v3) : la v3 EST l'édition courante — le GUI de
# campagne la remplace nativement, la table ne porte que les SEPT runs
# qu'il conduit.
# ---------------------------------------------------------------------------
EMPREINTES_1CLIC = {
    "TRIADE-1CLIC-DIAGNOSTIC.bat":
        "c0d6de86ed047f0ee4af7ddf24acc91c4cb9ec8bef366a4e0d2086e515659b2b",
    "TRIADE-1CLIC-GESTE-B-SHANI.bat":
        "e20582febde26c5dcd6870e5a31725c4d18117a51db5795260b3dbe99416095e",
    "TRIADE-1CLIC-VOIE1-QEMU.bat":
        "662fa0da547f90e376c3bec2fc3c694e3d50d9a85547f8db670002d4259fd7b3",
    "TRIADE-1CLIC-VOIE2-QEMU.bat":
        "2e1bc7142992be61444cfab08d17109809d5e62ac0d5236e44013ddac6f7ea68",
    "TRIADE-1CLIC-TEMOIN-VITRINE.bat":
        "80a617f6b53927dbfe0c5608fc84221f9668a28e76e0d75de3f538103a811f5d",
    "TRIADE-1CLIC-SEQUESTRE-D183.bat":
        "51fe8f575412714c5c021627961817fb336c5844f7e303ca7bb08410020b9e5c",
    "TRIADE-1CLIC-REPLICATION.bat":
        "850c9457a4e426d4b2bdd4152c841bc9147ece20e64c1a38044897ff4d4eb0a9",
}

# LE CATALOGUE DES SEPT RUNS 1-CLIC conduits par le GUI (étape 5) —
# l'état, l'exigence, le témoin attendu, le geste qui reste à la main :
# nommés, jamais maquillés (D189)
RUNS_1CLIC = {
    "diagnostic": {
        "etat_court": "OUVERT — choisit la machine du geste B",
        "court": "DIAGNOSTIC",
        "titre": "LE DIAGNOSTIC MACHINE",
        "bat": "TRIADE-1CLIC-DIAGNOSTIC.bat",
        "etat": "OUVERT — sert à CHOISIR la machine du geste B",
        "quoi": "la machine nommée, le silicium lu par CPUID, SHA-NI "
                "présent ou absent, le verdict des kits vivables",
        "quoi_court": "SHA-NI présent ou absent — le verdict des kits",
        "exigences": "Python 3 (aucune autre exigence)",
        "temoins": ["diagnostic-machine.txt"],
        "reste": "renvoyer le dossier de run ENTIER au coffre /test — la "
                 "pièce qui compte : diagnostic-machine.txt (un témoin "
                 "AUTO : sa signature est FACULTATIVE, D99)",
        "attente": "vécu sur ALEKPC et PORTABLE (SHA-NI ABSENT les deux "
                   "— le refus nommé T0.silicium est un RÉSULTAT, D189) ; "
                   "le geste B attend une machine qui A SHA-NI — le "
                   "diagnostic la choisit",
    },
    "geste-b": {
        "etat_court": "OUVERT — le vrai silicium",
        "court": "GESTE B",
        "titre": "LE GESTE B SHA-NI RÉEL",
        "bat": "TRIADE-1CLIC-GESTE-B-SHANI.bat",
        "etat": "OUVERT — la mesure avant/après sur le VRAI silicium",
        "quoi": "LA mesure avant/après SHA-NI, la pièce qui manque au "
                "bloc D-RQ3 (la preuve par la main)",
        "quoi_court": "la mesure avant/après sur le VRAI silicium",
        "exigences": "Python 3 + un silicium qui A SHA-NI (Ice Lake et "
                     "après chez Intel, Ryzen chez AMD — le diagnostic "
                     "le dit AVANT) ; sur une machine sans SHA-NI, le "
                     "refus nommé T0.silicium est un RÉSULTAT",
        "temoins": ["**/temoin-shani.txt", "**/VERDICT-run-shani.txt"],
        "reste": "dater et SIGNER la ligne signature du geste du témoin "
                 "preuves-shani\\temoin-shani.txt DE VOTRE MAIN, puis "
                 "renvoyer le dossier preuves-shani\\ ENTIER au coffre "
                 "/test",
        "attente": "la mesure avant/après n'a de sens que sur le VRAI "
                   "silicium — la frontière de l'émulation demeure "
                   "(l'artefact TCG appartient AU RUN, consigné tel quel)",
    },
    "voie1": {
        "etat_court": "FACULTATIF — chaîne fermée (E272)",
        "court": "VOIE 1",
        "titre": "LA VOIE 1 QEMU (LE KIT M7D REJOUÉ)",
        "bat": "TRIADE-1CLIC-VOIE1-QEMU.bat",
        "etat": "FACULTATIF — la chaîne est FERMÉE (l'Entrée 272)",
        "quoi": "le kit M7D rejoué sous le qemu-riscv64 EMBARQUÉ — le "
                "même VERDICT et le même journal attendus (la "
                "reproduction sur la même machine)",
        "quoi_court": "le kit M7D rejoué, qemu-riscv64 embarqué",
        "exigences": "WSL2 + Python 3 (le qemu-riscv64 vit EMBARQUÉ "
                     "dans le fichier — rien d'autre à installer)",
        "temoins": ["**/temoin-m7d.txt", "**/VERDICT-run-m7d.txt"],
        "reste": "le témoin AUTO né du rejeu ne diffère de celui signé "
                 "(l'Entrée 272) QUE par la ligne de date — sa signature "
                 "est FACULTATIVE (D99) ; renvoyer le dossier de run "
                 "ENTIER au coffre /test",
        "attente": "le rejeu ne RE-SCELLE RIEN (D165) — la chaîne de la "
                   "voie 1 demeure fermée par la première main ; chaque "
                   "témoin AUTO compte, nommé tel quel",
    },
    "voie2": {
        "etat_court": "FACULTATIF — chaîne fermée (E278)",
        "court": "VOIE 2",
        "titre": "LA VOIE 2 QEMU (LE KIT-SHANI SOUS ÉMULATION)",
        "bat": "TRIADE-1CLIC-VOIE2-QEMU.bat",
        "etat": "FACULTATIF — la chaîne est FERMÉE (l'Entrée 278)",
        "quoi": "le kit-shani sous qemu-x86_64 -cpu max — la chaîne "
                "T0-T5 entière, l'ARTEFACT TCG consigné TEL QUEL, "
                "jamais une vérité de silicium",
        "quoi_court": "le kit-shani sous qemu — l'artefact TCG tel quel",
        "exigences": "WSL2 + qemu-user + Python 3",
        "temoins": ["**/temoin-shani.txt", "**/VERDICT-run-shani.txt"],
        "reste": "le témoin AUTO né du rejeu : sa signature est "
                 "FACULTATIVE (D99) ; si vous signez, écrivez sous votre "
                 "main « run sous qemu-x86_64 -cpu max, ÉMULATION, pas "
                 "le silicium » ; renvoyer le dossier de run ENTIER au "
                 "coffre /test",
        "attente": "le rejeu ne RE-SCELLE RIEN (D165) — la chaîne de la "
                   "voie 2 demeure fermée (la main des Entrées "
                   "277/278) ; chaque témoin AUTO compte",
    },
    "vitrine": {
        "etat_court": "FACULTATIF — vécu propre",
        "court": "VITRINE",
        "titre": "LE TÉMOIN VITRINE (LE KIT LOUPE)",
        "bat": "TRIADE-1CLIC-TEMOIN-VITRINE.bat",
        "etat": "FACULTATIF — vécu propre, chaque témoin compte",
        "quoi": "le témoin vitrine du kit loupe : deux fenêtres que VOUS "
                "fermez (Alt+F4), les codes consignés",
        "quoi_court": "deux fenêtres que VOUS fermez, codes consignés",
        "exigences": "AUCUNE exigence",
        "temoins": ["**/temoin-vitrine.txt"],
        "reste": "renvoyer le dossier de run ENTIER au coffre /test — "
                 "le témoin AUTO : sa signature est FACULTATIVE (D99)",
        "attente": "vécu propre à la seconde vague (deux codes 0, aucun "
                   "WER loupe) — le rejeu demeure facultatif",
    },
    "sequestre": {
        "etat_court": "OUVERT — machine hors-ligne",
        "court": "SÉQUESTRE",
        "titre": "LE SÉQUESTRE D183 (LA CÉRÉMONIE DES CINQ PARTS)",
        "bat": "TRIADE-1CLIC-SEQUESTRE-D183.bat",
        "etat": "OUVERT — la cérémonie à la machine HORS-LIGNE",
        "quoi": "la répétition générale (l'autotest, VERT exigé), le "
                "découpage, la preuve de reconstitution à froid",
        "quoi_court": "la cérémonie des cinq parts, hors-ligne",
        "exigences": "Python 3 + pynacl + cryptography AVANT la mise "
                     "hors-ligne (« pip install pynacl cryptography » "
                     "sur la machine de cérémonie, EN LIGNE, avant le "
                     "retrait du réseau)",
        "temoins": ["**/AUTOTEST.txt"],
        "reste": "la cérémonie elle-même à la machine HORS-LIGNE : les "
                 "CINQ médias, la preuve de reconstitution à froid, le "
                 "retrait de la phrase en clair après le séquestre — "
                 "JAMAIS au bac à sable, jamais en ligne",
        "attente": "l'instrument a vécu jusqu'à l'import (le cache "
                   "cpython-314 né) ; aucune pièce d'autotest née au "
                   "dossier — la cérémonie demeure",
    },
    "replication": {
        "etat_court": "EN ATTENTE — les 2 jeux d'annot.",
        "court": "RÉPLICATION",
        "titre": "LA RÉPLICATION (LE κ DE COHEN)",
        "bat": "TRIADE-1CLIC-REPLICATION.bat",
        "etat": "EN ATTENTE — les DEUX jeux d'annotations",
        "quoi": "l'autotest du κ de Cohen + la grille T/X — le calcul "
                "vit le jour des deux jeux d'annotations",
        "quoi_court": "l'autotest du κ, la grille T/X (au jour des 2 jeux)",
        "exigences": "Python 3",
        "temoins": ["**/grille_tx.csv"],
        "reste": "renvoyer le dossier de run ENTIER au coffre /test "
                 "(l'autotest vit à la console)",
        "attente": "le seuil pré-enregistré κ >= 0,61 (D189) ; les DEUX "
                   "acteurs manquants demeurent NOMMÉS : le second "
                   "annotateur à recruter, le second domaine en attente "
                   "d'une vraie commande — jamais maquillés",
    },
}

# LES CHAÎNES DÉJÀ FERMÉES — l'histoire demeure (D143), ce GUI ne les
# rejoue jamais ; elles se lisent au catalogue, c'est tout
RUNS_FERMES = [
    ("LE KIT-2 DUDECT", "FERMÉ",
     "la mesure vécue deux fois (N=200, N=400), témoins signés"),
    ("LE CONSTAT-ARM (ANDROID)", "FERMÉ",
     "le constat VERT, témoin signé — l'APK vit au /test"),
    ("LA CÉRÉMONIE D'ÈRE", "REGISTRE",
     "un registre du projet, jamais un test"),
]

# L'ORDRE DES GESTES RESTANTS (le LISEZMOI-RUNS-RESTANTS de l'Entrée
# 273, la voie 2 fermée depuis) — le catalogue le rappelle en tête
ORDRE_GESTES = [
    ("1.", "LA CAMPAGNE D204 aux deux bras", "campagne"),
    ("2.", "LE GESTE B sur un silicium qui A SHA-NI", "geste-b"),
    ("3.", "LA CÉRÉMONIE DU SÉQUESTRE à la machine hors-ligne", "sequestre"),
    ("4.", "LE κ le jour des deux jeux d'annotations", "replication"),
]


def maintenant_local() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def horodatage_fichier() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def sha256_fichier(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# ===========================================================================
# SECTION B — LA LOGIQUE (testable sans tkinter : --selftest)
# ===========================================================================

class ErreurCampagne(RuntimeError):
    """Un refus nommé du GUI — la cause s'affiche, rien ne court."""


def trouver_dossier_pieces() -> pathlib.Path | None:
    """Cherche le dossier campagne-d204 : à côté du GUI, puis un niveau
    plus bas (un dossier de run extrait), sinon None (l'étape 2 demande)."""
    cand = GUI_DIR / "campagne-d204"
    if cand.is_dir() and (cand / "PLAN_PREREGISTRE_COMPARAISON.md").is_file():
        return cand
    for sous in sorted(GUI_DIR.glob("*/campagne-d204")):
        if (sous / "PLAN_PREREGISTRE_COMPARAISON.md").is_file():
            return sous
    return None


def verifier_pieces(dossier: pathlib.Path) -> list:
    """Recoupe CHAQUE pièce contre son empreinte gravée (fail-closed).
    Retourne [(nom, intact, détail)] — le plan en PREMIER (le verrou D204)."""
    ordre = ["PLAN_PREREGISTRE_COMPARAISON.md"] + [
        n for n in EMPREINTES_PIECES if n != "PLAN_PREREGISTRE_COMPARAISON.md"]
    resultat = []
    for nom in ordre:
        attendu = EMPREINTES_PIECES[nom]
        chemin = dossier / nom
        if not chemin.is_file():
            resultat.append((nom, False, "ABSENTE"))
            continue
        obtenu = sha256_fichier(chemin)
        ok = obtenu == attendu
        detail = (f"{obtenu[:16]}… == {attendu[:16]}…"
                  if ok else f"{obtenu[:16]}… != {attendu[:16]}… DIVERGENTE")
        resultat.append((nom, ok, detail))
    return resultat


def trouver_atelier(racine: pathlib.Path) -> pathlib.Path | None:
    """L'atelier de campagne vivant à cette racine (le dossier daté qui
    porte livraisons.csv) — None s'il n'y en a pas."""
    for existant in sorted(racine.glob("atelier-campagne-d204-*")):
        if (existant / "livraisons.csv").is_file():
            return existant
    return None


def ouvrir_atelier(dossier_pieces: pathlib.Path) -> pathlib.Path:
    """L'ATELIER de campagne : né du verrou vert, UNE fois — les COPIES
    datées des trois gabarits y vivent (les originaux INTACTS, scellés)."""
    racine = dossier_pieces.parent
    existant = trouver_atelier(racine)
    if existant is not None:
        return existant            # l'atelier existe — la continuité
    atelier = racine / f"atelier-campagne-d204-{horodatage_fichier()}"
    atelier.mkdir(parents=True)
    for nom in ("carnet_temps_humain.csv", "livraisons.csv", "defauts.csv"):
        source = dossier_pieces / nom
        if not source.is_file():
            raise ErreurCampagne(f"la pièce {nom} est absente du kit")
        shutil.copyfile(source, atelier / nom)
    (atelier / "comparaison_resultats").mkdir(exist_ok=True)
    # la trace de l'ouverture : le verrou qui tenait à la naissance
    lignes = [f"OUVERTURE DE L'ATELIER — {maintenant_local()}",
              f"le kit : {dossier_pieces}",
              "le verrou tenait (les HUIT pièces recoupées sha256 par "
              "sha256, le plan a78caf8c… == D204) ;",
              "les COPIES datées des trois gabarits y vivent — les "
              "originaux scellés demeurent INTACTS ;",
              "le dossier des résultats naît de la première mesure "
              "instrumentée (CA1), jamais avant.", ""]
    for nom in sorted(EMPREINTES_PIECES):
        ok = sha256_fichier(dossier_pieces / nom) == EMPREINTES_PIECES[nom]
        lignes.append(f"  {'VERT ' if ok else 'ROUGE'} {nom}")
    (atelier / "journal-ouverture.txt").write_text(
        "\n".join(lignes), encoding="utf-8")
    return atelier


def atelier_valide(chemin) -> pathlib.Path | None:
    """Un atelier candidat est VALIDE s'il porte livraisons.csv —
    le bouton « CHOISIR L'ATELIER EXISTANT » de l'étape 2 le vérifie."""
    candidat = pathlib.Path(chemin)
    if candidat.is_dir() and (candidat / "livraisons.csv").is_file():
        return candidat
    return None


def _lire_csv_gabarit(chemin: pathlib.Path) -> list:
    """Lit un gabarit : les lignes '#' sont les règles, la première ligne
    claire est l'en-tête, le reste est la donnée (le journal brut)."""
    if not chemin.is_file():
        return []
    lignes_claires = []
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if ligne.strip() and not ligne.lstrip().startswith("#"):
                lignes_claires.append(ligne)
    if not lignes_claires:
        return []
    lecteur = csv.reader(lignes_claires)
    entete = next(lecteur)
    return [dict(zip(entete, row)) for row in lecteur if row]


def _ajouter_ligne(chemin: pathlib.Path, valeurs: list) -> None:
    """Append-only, UTF-8, une ligne — le gabarit ne se réécrit JAMAIS."""
    with open(chemin, "a", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(valeurs)


def _valider_date(texte: str, quoi: str) -> str:
    try:
        d = dt.datetime.strptime(texte.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ErreurCampagne(f"la {quoi} « {texte} » n'est pas une date "
                             "ISO (AAAA-MM-JJ)")
    return d.isoformat()


def _valider_heure(texte: str, quoi: str) -> int:
    m = re.match(r"^(\d{1,2}):(\d{2})$", texte.strip())
    if not m:
        raise ErreurCampagne(f"l'heure {quoi} « {texte} » n'est pas HH:MM")
    h, mn = int(m.group(1)), int(m.group(2))
    if h > 23 or mn > 59:
        raise ErreurCampagne(f"l'heure {quoi} « {texte} » n'existe pas")
    return h * 60 + mn


def _tache_valide(tache: str) -> None:
    if not re.match(r"^(loupe-(01|02|05|08|13|16)|app)$", tache):
        raise ErreurCampagne(f"la tâche « {tache} » n'est pas de la "
                             "campagne (loupe-01/02/05/08/13/16 ou app)")


def _bras_valide(bras: str) -> None:
    if bras not in ("T", "C"):
        raise ErreurCampagne(f"le bras « {bras} » n'existe pas (T ou C)")


def carnet_consigner(atelier: pathlib.Path, date: str, bras: str,
                     tache: str, geste: str, debut: str, fin: str,
                     notes: str) -> dict:
    """UNE ligne AU GESTE (§ 4-M3) — jamais reconstruite de mémoire ;
    les minutes se calculent de début à fin (l'arrondi à la minute)."""
    _bras_valide(bras)
    _tache_valide(tache)
    _valider_date(date, "date")
    if not geste.strip():
        raise ErreurCampagne("le geste est vide — nommez-le (cristallisation, "
                             "garde, revue des livrables…)")
    d = _valider_heure(debut, "de début")
    f = _valider_heure(fin, "de fin")
    if f < d:
        raise ErreurCampagne("la fin précède le début — toute interruption "
                             "> 5 min ferme la ligne et en ouvre une autre")
    minutes = f - d
    _ajouter_ligne(atelier / "carnet_temps_humain.csv",
                   [date.strip(), bras, tache, geste.strip(),
                    debut.strip(), fin.strip(), str(minutes), notes.strip()])
    return {"minutes": minutes}


def livraisons_depuis(atelier: pathlib.Path, bras: str,
                      tache: str) -> list:
    _bras_valide(bras)
    _tache_valide(tache)
    toutes = _lire_csv_gabarit(atelier / "livraisons.csv")
    return [l for l in toutes if l.get("bras") == bras
            and l.get("tache") == tache]


def livraison_consigner(atelier: pathlib.Path, bras: str, tache: str,
                        date_kit: str, date_run: str, verdict: str,
                        recoup: str) -> dict:
    """UNE ligne par run terrain (§ 4-M1) — la cap pré-enregistrée TENUE
    par le GUI : au plus TROIS par bloc, DOUZE par application, l'arrêt
    au PREMIER VERT (§ 7) — le refus est NOMMÉ, jamais contourné."""
    _bras_valide(bras)
    _tache_valide(tache)
    cap = CAP_APP if tache == "app" else CAP_BLOC
    existantes = livraisons_depuis(atelier, bras, tache)
    if any(l.get("verdict", "").strip().upper() == "VERT"
           for l in existantes):
        raise ErreurCampagne(
            "l'unité est CLOSE — l'arrêt au PREMIER VERT (§ 7 du plan) ; "
            "le rejouage d'une unité verte n'est pas une livraison")
    if len(existantes) >= cap:
        raise ErreurCampagne(
            f"la CAP pré-enregistrée est ATTEINTE ({cap} livraisons sans "
            "vert) — l'unité est CENSURÉE, rapportée telle quelle ; elle "
            "ne se prolonge JAMAIS (§ 7)")
    numero = len(existantes) + 1
    if verdict.strip().upper() not in ("VERT", "ROUGE"):
        raise ErreurCampagne("le verdict est VERT ou ROUGE — le mot du "
                             "recoup, jamais autre chose")
    _valider_date(date_kit, "date du kit")
    _valider_date(date_run, "date du run")
    identifiant = f"{bras}-{tache}-it{numero}"
    _ajouter_ligne(atelier / "livraisons.csv",
                   [identifiant, bras, tache, str(numero),
                    date_kit.strip(), date_run.strip(),
                    verdict.strip().upper(), recoup.strip()])
    return {"livraison": identifiant, "numero": numero, "cap": cap}


def defaut_consigner(atelier: pathlib.Path, bras: str, tache: str,
                     classe: str, mecanisme: str, cote: str,
                     piece_appui: str, exclusion: str,
                     raison_exclusion: str, livraison: str = "") -> dict:
    """UNE ligne par défaut NOMMÉ (classe + mécanisme + pièce à l'appui,
    AVANT toute correction — la discipline vaut aux DEUX bras)."""
    _bras_valide(bras)
    _tache_valide(tache)
    for nom, valeur in (("la classe", classe), ("le mécanisme", mecanisme)):
        if not valeur.strip():
            raise ErreurCampagne(f"{nom} du défaut est vide — un défaut se "
                                 "NOMME avant toute correction")
    if cote not in ("piece", "kit", "exclu"):
        raise ErreurCampagne("le côté est piece, kit ou exclu (la règle D202)")
    if exclusion not in ("oui", "non"):
        raise ErreurCampagne("l'exclusion est oui ou non — nommée avec sa "
                             "raison, jamais silencieuse")
    if exclusion == "oui" and not raison_exclusion.strip():
        raise ErreurCampagne("une exclusion NOMMÉE exige sa raison")
    if not piece_appui.strip():
        raise ErreurCampagne("la pièce à l'appui est vide — un défaut nommé "
                             "s'appuie sur une pièce")
    if livraison and not re.match(r"^[TC]-(loupe-(01|02|05|08|13|16)|app)"
                                  r"-it\d+$", livraison):
        raise ErreurCampagne(f"la livraison « {livraison} » n'est pas un "
                             "identifiant de la campagne")
    _ajouter_ligne(atelier / "defauts.csv",
                   [livraison, bras, tache, classe.strip(),
                    mecanisme.strip(), cote, piece_appui.strip(),
                    exclusion, raison_exclusion.strip()])
    return {}


def statut_unite(livraisons: list, cap: int) -> str:
    """L'état HONNÊTE d'une unité — lu des lignes, rien d'autre :
    PAS COMMENCÉE / EN COURS / VERT (close) / CENSURÉE (la cap sans vert)."""
    if not livraisons:
        return "PAS COMMENCÉE"
    if any(l.get("verdict", "").strip().upper() == "VERT"
           for l in livraisons):
        return "VERT — close (l'arrêt au premier vert)"
    if len(livraisons) >= cap:
        return "CENSURÉE (la cap sans vert — rapportée telle quelle)"
    return "EN COURS"


def lire_empreintes_kit(dossier: pathlib.Path) -> list:
    """Parse un fichier EMPREINTES*.txt d'un kit d'unité : les lignes
    « <sha256>  <fichier>  (…) » — [(fichier, sha256 attendu)]."""
    resultats = []
    for fich in sorted(dossier.glob("EMPREINTES*.txt")):
        for ligne in fich.read_text(encoding="utf-8",
                                    errors="replace").splitlines():
            m = re.match(r"^([0-9a-fA-F]{64})\s+(\S+)", ligne.strip())
            if not m:
                continue
            attendu, nom = m.group(1).lower(), m.group(2)
            resultats.append((nom, attendu))
    return resultats


def recouper_kit_unite(dossier: pathlib.Path) -> list:
    """Recoupe les empreintes GRAVÉES d'un kit d'unité livré par le labo
    (si le kit en porte) — sinon le kit 1-clic fait son propre recoup."""
    empreintes = lire_empreintes_kit(dossier)
    if not empreintes:
        return []
    resultat = []
    for nom, attendu in empreintes:
        chemin = dossier / nom
        if not chemin.is_file():
            resultat.append((nom, False, "ABSENTE"))
            continue
        obtenu = sha256_fichier(chemin)
        resultat.append((nom, obtenu == attendu,
                         f"{obtenu[:16]}… {'==' if obtenu == attendu else '!='}"
                         f" {attendu[:16]}…"))
    return resultat


# ---------------------------------------------------------------------------
# LES RUNS 1-CLIC — la logique propre (recoup du fichier, découverte du
# témoin, consignation du run) — testable sans fenêtre
# ---------------------------------------------------------------------------
def recouper_fichier_1clic(chemin: pathlib.Path,
                           attendu: str) -> tuple:
    """Recoupe UN fichier 1-clic contre son empreinte GRAVÉE (la table
    EMPREINTES_1CLIC) — fail-closed : un octet divergent, le run ne
    part pas. Retourne (ok, détail)."""
    chemin = pathlib.Path(chemin)
    if not chemin.is_file():
        return False, f"« {chemin.name} » n'existe pas — choisissez-le d'abord"
    if not re.match(r"^[0-9a-f]{64}$", attendu):
        return False, "l'empreinte gravée est MAL FORMÉE — écart nommé au labo"
    obtenu = sha256_fichier(chemin)
    if obtenu == attendu:
        return True, (f"{obtenu[:16]}… == {attendu[:16]}… — le fichier "
                      "autonome est INTACT, l'édition gravée")
    return False, (f"{obtenu[:16]}… != {attendu[:16]}… — le fichier DIVERGE : "
                   "re-téléchargez-le du coffre /test, RIEN ne court "
                   "(fail-closed)")


def trouver_temoins(run_dossier: pathlib.Path, motifs: list) -> list:
    """Cherche les témoins attendus d'un dossier de run — chaque motif
    (glob) rend son PREMIER trouvé (les dispositions vécues des DEUX
    vagues couvertes) : [(motif, chemin | None)]."""
    resultat = []
    for motif in motifs:
        trouves = sorted(run_dossier.glob(motif))
        trouves = [t for t in trouves if t.is_file()]
        resultat.append((motif, trouves[0] if trouves else None))
    return resultat


def consigner_run_1clic(etat: dict, cle: str, run_dossier) -> dict:
    """Consigne le dossier d'un run 1-clic né (l'historique du run —
    dédoublonné, append-only) : RETOURNE l'état mis à jour (jamais
    écrit ici — l'écriture appartient au geste du GUI)."""
    if cle not in RUNS_1CLIC:
        raise ErreurCampagne(f"le run « {cle} » n'est pas du catalogue")
    dossier = str(pathlib.Path(run_dossier))
    runs = etat.setdefault("runs_1clic", {}).setdefault(cle, {})
    historique = runs.setdefault("historique", [])
    if dossier not in historique:
        historique.append(dossier)
    runs["run"] = dossier
    return {"historique": len(historique)}


def statut_run_1clic(etat: dict, cle: str) -> str:
    """L'état LU de l'état du GUI — les comptes seuls, rien d'autre."""
    if cle not in RUNS_1CLIC:
        return "—"
    runs = etat.get("runs_1clic", {}).get(cle, {})
    n = len(runs.get("historique", []))
    if not n:
        return "AUCUN run consigné"
    return f"{n} run(s) consigné(s) — le dernier : " \
           f"{pathlib.Path(runs['historique'][-1]).name}"


def charger_etat() -> dict:
    if FICHIER_ETAT.is_file():
        try:
            return json.loads(FICHIER_ETAT.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def sauver_etat(etat: dict) -> None:
    tmp = FICHIER_ETAT.with_suffix(".tmp")
    tmp.write_text(json.dumps(etat, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    tmp.replace(FICHIER_ETAT)


def importer_etat_v1() -> dict:
    """L'HÉRITAGE du GUI campagne v1.0.1 : son fichier d'état
    (etat-campagne-d204.json) vit à côté du GUI (le kit dézippé
    PAR-DESSUS ou À CÔTÉ de l'ancien) — l'atelier, la calibration, les
    kits choisis et les unités SURVIVENT (la campagne continue, jamais
    ne recommence). Retourne {} s'il n'y a rien à hériter."""
    candidats = [GUI_DIR / FICHIER_ETAT_V1,
                 GUI_DIR.parent / "TRIADE_gui_campagne_v1" / FICHIER_ETAT_V1]
    for cand in candidats:
        if cand.is_file():
            try:
                retour = json.loads(cand.read_text(encoding="utf-8"))
                if isinstance(retour, dict):
                    retour["_chemin_heritage"] = str(cand)
                    return retour
            except Exception:
                pass
    return {}


def heriter_etat_v1() -> tuple:
    """Fusionne l'héritage v1 dans un état NEUF du présent GUI — les
    clés de campagne portées telles quelles (kit, atelier, calibration,
    unites, commande_reelle_arrivee). Retourne (état, héritage_ou_non)."""
    etat = charger_etat()
    heritage = importer_etat_v1()
    if etat or not heritage:
        return etat, False
    for cle in ("kit", "atelier", "calibration", "unites",
                "commande_reelle_arrivee"):
        if cle in heritage:
            etat[cle] = heritage[cle]
    etat["heritage_v1"] = heritage.get("_chemin_heritage", "")
    return etat, True


# ---------------------------------------------------------------------------
# LE SELFTEST — la logique éprouvée au labo, sans fenêtre (D122 : le labo
# ne court JAMAIS le Windows du terrain ; il éprouve la logique sur copie)
# ---------------------------------------------------------------------------
def selftest() -> int:
    print(f"[selftest] triade_tous_runs_gui.py v{VERSION} — la logique, "
          "sans fenêtre")
    verts, rouges = 0, 0

    def consigne(nom, ok, detail=""):
        nonlocal verts, rouges
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
              + (f" — {detail}" if detail else ""))
        verts += ok
        rouges += not ok

    with tempfile.TemporaryDirectory() as tmp:
        racine = pathlib.Path(tmp)
        # T1 — le verrou : les vraies pièces, recoupées une à une
        # (LECTURE SEULE — le selftest ne modifie jamais le kit)
        pieces = trouver_dossier_pieces()
        if pieces is None:
            consigne("T1 le verrou des HUIT pièces", False,
                     "le dossier campagne-d204 n'est pas à côté du GUI")
        else:
            resultat = verifier_pieces(pieces)
            consigne("T1 le verrou des HUIT pièces",
                     all(ok for _, ok, _ in resultat),
                     f"{sum(ok for _, ok, _ in resultat)}/8 intactes")
            # T2 — fail-closed : une pièce corrompue est NOMMÉE (sur copie)
            copie = racine / "kit-corrompu"
            copie.mkdir()
            for nom in EMPREINTES_PIECES:
                shutil.copyfile(pieces / nom, copie / nom)
            with open(copie / "livraisons.csv", "a", encoding="utf-8") as f:
                f.write("une ligne qui diverge\n")
            resultat2 = verifier_pieces(copie)
            divergence = [n for n, ok, _ in resultat2 if not ok]
            consigne("T2 fail-closed — la pièce divergente NOMMÉE",
                     divergence == ["livraisons.csv"], str(divergence))

        # T3 — l'atelier : les copies datées naissent, les originaux
        # intacts — le selftest travaille sur une COPIE temporaire du
        # kit, JAMAIS sur le kit lui-même (D122 : sur copie, toujours)
        pieces_reel = trouver_dossier_pieces()
        pieces = racine / "kit-selftest" / "campagne-d204"
        pieces.mkdir(parents=True)
        if pieces_reel is not None:
            for nom in EMPREINTES_PIECES:
                shutil.copyfile(pieces_reel / nom, pieces / nom)
        else:
            for nom, contenu in (
                    ("carnet_temps_humain.csv",
                     "# règles\n" + ",".join(COLONNES_CARNET) + "\n"),
                    ("livraisons.csv",
                     "# règles\n" + ",".join(COLONNES_LIVRAISONS) + "\n"),
                    ("defauts.csv",
                     "# règles\n" + ",".join(COLONNES_DEFAUTS) + "\n"),
                    ("PLAN_PREREGISTRE_COMPARAISON.md", "# le plan\n"),
                    ("LISEZMOI-comparaison.txt", "# le lisezmoi\n"),
                    ("LANCER-CAMPAGNE-D204.bat", "@echo off\n"),
                    ("chronometre_verification.py", "# le chrono\n"),
                    ("compter_tokens.py", "# le compteur\n")):
                (pieces / nom).write_text(contenu, encoding="utf-8")
        empreintes_avant = {n: sha256_fichier(pieces / n)
                            for n in EMPREINTES_PIECES}
        atelier = ouvrir_atelier(pieces)
        consigne("T3 l'atelier né, les trois copies vivantes",
                 all((atelier / n).is_file() for n in
                     ("carnet_temps_humain.csv", "livraisons.csv",
                      "defauts.csv")))
        consigne("T3b l'atelier STABLE — la continuité du carnet",
                 ouvrir_atelier(pieces) == atelier)
        empreintes_apres = {n: sha256_fichier(pieces / n)
                            for n in EMPREINTES_PIECES}
        consigne("T3c les ORIGINAUX intacts — l'atelier n'y touche pas",
                 empreintes_avant == empreintes_apres)
        consigne("T3d trouver_atelier retrouve l'atelier vivant",
                 trouver_atelier(pieces.parent) == atelier)
        faux = racine / "pas-un-atelier"
        faux.mkdir()
        consigne("T3e un dossier sans livraisons.csv N'EST PAS un atelier",
                 atelier_valide(faux) is None
                 and trouver_atelier(racine / "vide-inexistant") is None)

        # T4 — le carnet : la ligne au geste, les minutes calculées
        r = carnet_consigner(atelier, "2026-11-14", "T", "loupe-05",
                             "garde", "10:00", "10:12", "les dix arbres")
        consigne("T4 le carnet — 12 minutes calculées", r["minutes"] == 12)
        lignes = _lire_csv_gabarit(atelier / "carnet_temps_humain.csv")
        consigne("T4b la ligne vit au carnet, les colonnes exactes",
                 bool(lignes) and lignes[0]["minutes"] == "12"
                 and list(lignes[0].keys()) == COLONNES_CARNET)
        try:
            carnet_consigner(atelier, "2026-11-14", "T", "loupe-05",
                             "garde", "10:30", "10:00", "inversée")
            consigne("T4c la fin avant le début — REFUS NOMMÉ", False)
        except ErreurCampagne:
            consigne("T4c la fin avant le début — REFUS NOMMÉ", True)

        # T5 — les livraisons : la cap tenue, l'arrêt au premier vert
        for _ in range(3):
            livraison_consigner(atelier, "C", "loupe-01",
                                "2026-11-14", "2026-11-14", "ROUGE", "labo")
        try:
            livraison_consigner(atelier, "C", "loupe-01", "2026-11-14",
                                "2026-11-14", "ROUGE", "labo")
            consigne("T5 la cap de bloc — REFUS au-delà de TROIS", False)
        except ErreurCampagne as e:
            consigne("T5 la cap de bloc — REFUS au-delà de TROIS",
                     "CAP" in str(e))
        st = statut_unite(livraisons_depuis(atelier, "C", "loupe-01"),
                          CAP_BLOC)
        consigne("T5b l'unité à la cap sans vert — CENSURÉE",
                 st.startswith("CENSURÉE"), st)
        livraison_consigner(atelier, "T", "loupe-01", "2026-11-14",
                            "2026-11-14", "VERT", "labo")
        try:
            livraison_consigner(atelier, "T", "loupe-01", "2026-11-14",
                                "2026-11-14", "ROUGE", "labo")
            consigne("T5c l'arrêt au premier vert — REFUS", False)
        except ErreurCampagne as e:
            consigne("T5c l'arrêt au premier vert — REFUS",
                     "PREMIER VERT" in str(e))

        # T6 — les défauts : nommés, la pièce à l'appui, l'exclusion raisonnée
        defaut_consigner(atelier, "T", "loupe-01", "T6-classe",
                         "le mécanisme", "piece", "preuve.txt", "non", "")
        try:
            defaut_consigner(atelier, "T", "loupe-01", "T6", "m", "piece",
                             "p.txt", "oui", "")
            consigne("T6b l'exclusion sans raison — REFUS", False)
        except ErreurCampagne:
            consigne("T6b l'exclusion sans raison — REFUS", True)

        # T7 — les empreintes gravées d'un kit d'unité (le parseur)
        dossier_kit = racine / "kit-unite"
        dossier_kit.mkdir()
        (dossier_kit / "EMPREINTES-KIT.txt").write_text(
            "EMPREINTES — le kit d'unité\n"
            "===========================\n"
            f"{sha256_fichier(pieces / 'livraisons.csv')}  livraisons.csv"
            "  (la pièce du kit)\n", encoding="utf-8")
        shutil.copyfile(pieces / "livraisons.csv",
                        dossier_kit / "livraisons.csv")
        recoup = recouper_kit_unite(dossier_kit)
        consigne("T7 le recoup des empreintes gravées d'un kit d'unité",
                 bool(recoup) and recoup[0][1] is True)

        # T8 — la table des fichiers 1-clic : SEPT empreintes gravées,
        # bien formées, chaque run du catalogue a SON fichier
        table_ok = (len(EMPREINTES_1CLIC) == 7
                    and all(re.match(r"^[0-9a-f]{64}$", h)
                            for h in EMPREINTES_1CLIC.values())
                    and all(re.match(r"^TRIADE-1CLIC-[A-Z0-9-]+\.bat$", n)
                            for n in EMPREINTES_1CLIC))
        correspondance = all(
            RUNS_1CLIC[c]["bat"] in EMPREINTES_1CLIC for c in RUNS_1CLIC)
        consigne("T8 la table des SEPT fichiers 1-clic gravée",
                 table_ok and correspondance,
                 f"{len(EMPREINTES_1CLIC)} entrées, "
                 f"{len(RUNS_1CLIC)} runs au catalogue")

        # T9 — le recoup d'un fichier 1-clic : INTACT puis DIVERGENT
        # (fail-closed — sur une copie temporaire, l'empreinte de la
        # copie sert de gravure : la LOGIQUE s'éprouve, pas la table)
        faux_bat = racine / "TRIADE-1CLIC-ESSAI.bat"
        faux_bat.write_bytes(b"@echo off\r\nrem un faux fichier 1-clic\r\n")
        gravure = sha256_fichier(faux_bat)
        ok, detail = recouper_fichier_1clic(faux_bat, gravure)
        consigne("T9 le fichier 1-clic INTACT — recoup VERT", ok, detail)
        with open(faux_bat, "ab") as f:
            f.write(b"un octet de plus\r\n")
        ok2, detail2 = recouper_fichier_1clic(faux_bat, gravure)
        consigne("T9b le fichier 1-clic DIVERGENT — REFUS nommé",
                 (not ok2) and "DIVERGE" in detail2, detail2)
        ok3, _ = recouper_fichier_1clic(racine / "inexistant.bat", gravure)
        consigne("T9c le fichier absent — REFUS nommé", not ok3)

        # T10 — la découverte des témoins : les DISPOSITIONS VÉCUES des
        # deux vagues, pièce par pièce (octet pour octet la structure)
        def arbre(base, chemins):
            for c in chemins:
                p = base / c
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("un témoin\n", encoding="utf-8")
        # geste B — la disposition vécue
        g = racine / "run-geste-b"
        arbre(g, ["pc-windows/kit-1-shani/preuves-shani/temoin-shani.txt",
                  "pc-windows/kit-1-shani/preuves-shani/VERDICT-run-shani.txt"])
        t = trouver_temoins(g, RUNS_1CLIC["geste-b"]["temoins"])
        consigne("T10 geste B — le témoin ET le verdict trouvés",
                 all(chemin is not None for _, chemin in t))
        # voie 1 — la disposition vécue
        v1 = racine / "run-voie1"
        arbre(v1, ["qemu-wsl2/kit-m7d/preuves-m7/temoin-m7d.txt",
                   "qemu-wsl2/kit-m7d/preuves-m7/VERDICT-run-m7d.txt"])
        t = trouver_temoins(v1, RUNS_1CLIC["voie1"]["temoins"])
        consigne("T10b voie 1 — le témoin m7d ET le verdict trouvés",
                 all(chemin is not None for _, chemin in t))
        # voie 2 — les DEUX dispositions vécues (le run du développeur,
        # la référence du labo)
        v2a = racine / "run-voie2-dev"
        arbre(v2a, ["pc-windows/kit-1-shani/preuves-shani/temoin-shani.txt"])
        v2b = racine / "run-voie2-labo"
        arbre(v2b, ["qemu-wsl2/preuves-shani-emulation-labo/temoin-shani.txt"])
        t_a = trouver_temoins(v2a, RUNS_1CLIC["voie2"]["temoins"])
        t_b = trouver_temoins(v2b, RUNS_1CLIC["voie2"]["temoins"])
        consigne("T10c voie 2 — le témoin trouvé aux DEUX dispositions",
                 t_a[0][1] is not None and t_b[0][1] is not None)
        # vitrine / diagnostic / séquestre / réplication
        vi = racine / "run-vitrine"
        arbre(vi, ["loupe-kit-13/preuves-loupe/temoin-vitrine.txt"])
        di = racine / "run-diagnostic"
        arbre(di, ["diagnostic-machine.txt"])
        sq = racine / "run-sequestre"
        arbre(sq, ["sequestre-d183/scripts/kit_ceremonie_d183/AUTOTEST.txt"])
        re_ = racine / "run-replication"
        arbre(re_, ["replication/grille_tx.csv"])
        for cle, base in (("vitrine", vi), ("diagnostic", di),
                          ("sequestre", sq), ("replication", re_)):
            t = trouver_temoins(base, RUNS_1CLIC[cle]["temoins"])
            consigne(f"T10d {cle} — la pièce attendue trouvée",
                     all(chemin is not None for _, chemin in t))
        # un dossier vide ne trouve RIEN (l'absence est une réponse)
        vide = racine / "run-vide"
        vide.mkdir()
        t = trouver_temoins(vide, RUNS_1CLIC["geste-b"]["temoins"])
        consigne("T10e le run sans témoin — l'absence NOMMÉE",
                 all(chemin is None for _, chemin in t))

        # T11 — la consignation des runs 1-clic : l'historique dédoublonné
        etat = {}
        r = consigner_run_1clic(etat, "geste-b", g)
        r2 = consigner_run_1clic(etat, "geste-b", g)      # dédoublonné
        consigne("T11 le run consigné, l'historique dédoublonné",
                 r["historique"] == 1 and r2["historique"] == 1)
        v2a_str = str(v2a)
        consigner_run_1clic(etat, "voie2", v2a)
        consigne("T11b les runs vivent SéPARÉment par clé",
                 etat["runs_1clic"]["voie2"]["historique"] == [v2a_str]
                 and statut_run_1clic(etat, "voie2").startswith("1 run"))
        try:
            consigner_run_1clic(etat, "inconnu", g)
            consigne("T11c la clé inconnue — REFUS nommé", False)
        except ErreurCampagne:
            consigne("T11c la clé inconnue — REFUS nommé", True)

        # T12 — l'héritage du GUI campagne v1 : les clés portées, le
        # dossier de pièces EXIGÉ (jamais un héritage muet)
        heritage = {"kit": str(pieces), "atelier": str(atelier),
                    "calibration": {"statut": "VERT", "ecart": "0.001"},
                    "unites": {"T-loupe-01": {"kit": "x"}}}
        dest = racine / "etat-heritage.json"
        dest.write_text(json.dumps(heritage), encoding="utf-8")
        lu = json.loads(dest.read_text(encoding="utf-8"))
        porte = all(k in lu for k in
                    ("kit", "atelier", "calibration", "unites"))
        consigne("T12 l'héritage v1 — les clés de campagne portées",
                 porte and lu["calibration"]["statut"] == "VERT")

    print(f"[selftest] {verts} VERT, {rouges} ROUGE — "
          f"{'TOUT VERT' if rouges == 0 else 'ÉCHEC'}")
    return 0 if rouges == 0 else 1


# ===========================================================================
# SECTION C — LA GUI (tkinter, import PROTÉGÉ : --selftest reste sans fenêtre)
# ===========================================================================

try:
    import queue
    import threading
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    TKINTER_DISPONIBLE, TKINTER_ERREUR = True, ""
except ImportError as _exc:                                    # noqa: E722
    TKINTER_DISPONIBLE, TKINTER_ERREUR = False, str(_exc)

COULEUR_VERTE = "#1a7f37"
COULEUR_ROUGE = "#b42318"
COULEUR_ENCRE = "#1f2328"
COULEUR_ATTENTE = "#9a6700"
COULEUR_FOND = "#f6f8fa"
COULEUR_BORD = "#d0d7de"
POLICE_FIXE = ("TkFixedFont", 10)

ETAPES = [
    (1, "LE CATALOGUE", "tous les runs, leurs états"),
    (2, "LA CAMPAGNE · VERROU", "les HUIT pièces, l'atelier"),
    (3, "LA CAMPAGNE · CALIBRATION", "la preuve d'horloge"),
    (4, "LA CAMPAGNE · UNITÉS", "les quatorze unités"),
    (5, "LES AUTRES RUNS", "les sept tests 1-clic"),
    (6, "LE SUIVI", "les comptes seuls"),
    (7, "LES PIÈCES", "le plan, le coffre"),
]


class Enregistreur:
    """Le journal de session du GUI — chaque geste y vit (D99)."""

    def __init__(self, dossier: pathlib.Path):
        dossier.mkdir(parents=True, exist_ok=True)
        self.chemin = dossier / f"tous_runs_gui_{horodatage_fichier()}.log"
        with open(self.chemin, "a", encoding="utf-8") as f:
            f.write(f"=== TRIADE tous les runs GUI v{VERSION} — "
                    f"{maintenant_local()} ===\n")

    def ligne(self, texte: str, genre: str = "info") -> None:
        try:
            with open(self.chemin, "a", encoding="utf-8") as f:
                f.write(f"[{genre}] {texte}\n")
        except Exception:
            pass


class Executeur:
    """Un fil + une file : les instruments ne gèlent JAMAIS la fenêtre
    (tkinter n'est PAS thread-safe — la file est la SEULE frontière :
    les lignes de journal comme le verdict y passent, jamais un appel
    direct au fil principal)."""

    def __init__(self, app):
        self.app = app
        self.file = queue.Queue()
        self.occupe = False

    def lancer(self, titre: str, fonction, args=()) -> bool:
        if self.occupe:
            messagebox.showwarning(
                "TRIADE — tous les runs",
                "Un geste court déjà — laissez-le finir (le refus est "
                "nommé, jamais doublé).")
            return False
        self.occupe = True
        self.app.journal_ajoute(f"── {titre} ──", "titre")
        self.app.verdict(None, f"{titre} : en cours…")
        threading.Thread(target=self._fil, args=(fonction, args),
                         daemon=True).start()
        return True

    def emit(self, ligne) -> None:
        """Thread-safe : une ligne de journal, depuis le fil ouvrier —
        elle passe par la file, jamais par tkinter."""
        self.file.put(("ligne", str(ligne)))

    def emit_appel(self, fonction, *args) -> None:
        """Thread-safe : un appel de fenêtre à faire au FIL PRINCIPAL
        seul (afficher un recoup, rafraîchir une table) — tkinter
        n'est PAS thread-safe : l'appel passe par la file, jamais
        depuis le fil ouvrier (même pas racine.after)."""
        self.file.put(("appel", (fonction, args)))

    def _fil(self, fonction, args):
        try:
            r = fonction(*args)
        except ErreurCampagne as exc:
            self.app.enreg.ligne(f"refus nommé : {exc}", "refus")
            r = (False, f"REFUS NOMMÉ : {exc}")
        except Exception as exc:
            self.app.enreg.ligne(f"échec inattendu ({type(exc).__name__}) : "
                                 f"{exc}", "crash")
            self.app.enreg.ligne(traceback.format_exc(), "crash")
            r = (False, f"échec inattendu ({type(exc).__name__}) : {exc}")
        if isinstance(r, bool):
            r = (r, "VERT" if r else "ÉCHEC")
        elif isinstance(r, tuple) and len(r) == 2:
            r = (bool(r[0]), str(r[1]))
        else:
            r = (True, str(r))
        self.file.put(("fin", r))

    def pompe(self):
        try:
            while True:
                genre, donnees = self.file.get_nowait()
                if genre == "ligne":
                    self.app.journal_ajoute(donnees)
                elif genre == "appel":
                    fonction, args = donnees
                    try:
                        fonction(*args)
                    except Exception as exc:
                        self.app.enreg.ligne(
                            f"échec d'affichage ({type(exc).__name__}) : "
                            f"{exc}", "crash")
                else:
                    self.occupe = False
                    ok, texte = donnees
                    self.app.verdict(ok, texte)
                    self.app.sur_fin_geste()
        except queue.Empty:
            pass
        self.app.racine.after(80, self.pompe)


def ouvrir_au_systeme(chemin) -> tuple:
    """Ouvre un fichier ou dossier comme un double-clic (la console
    officielle d'un kit, l'explorateur, le bloc-notes)."""
    chemin = pathlib.Path(chemin)
    if not chemin.exists():
        return False, f"« {chemin} » n'existe pas — choisissez-le d'abord"
    try:
        if hasattr(os, "startfile"):            # Windows
            os.startfile(str(chemin))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(chemin)])
        else:
            subprocess.Popen(["xdg-open", str(chemin)])
        return True, f"« {chemin.name} » ouvert"
    except Exception as exc:
        return False, f"l'ouverture a échoué ({type(exc).__name__}) : {exc}"


class Application:
    """La fenêtre : les étapes à gauche, le geste à droite, le journal
    en bas — tout au clic, fail-closed partout."""

    def __init__(self, racine: tk.Tk, kit_choisi):
        self.racine = racine
        self.etat, heritage = heriter_etat_v1()
        self.enreg = Enregistreur(DOSSIER_LOGS)
        self.executeur = Executeur(self)
        self.atelier = None
        self.verrou_vert = False

        racine.title(f"TRIADE — tous les runs pas à pas · GUI v{VERSION}")
        racine.geometry("1280x800")
        racine.minsize(1080, 680)
        racine.configure(bg=COULEUR_FOND)

        style = ttk.Style(racine)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TNotebook.Tab", padding=(8, 4))
        style.configure("Verdict.TLabel", font=("TkDefaultFont", 11, "bold"))
        style.configure("Titre.TLabel", font=("TkDefaultFont", 14, "bold"))
        style.configure("Sous.TLabel", foreground="#57606a")
        style.configure("Etape.TButton", padding=(12, 9))
        style.configure("Geste.TButton", padding=(12, 8))

        # ---- la barre du haut
        haut = ttk.Frame(racine, padding=(14, 10, 14, 4))
        haut.pack(fill="x")
        ttk.Label(haut, text="TRIADE — TOUS LES TESTS ET RUNS, PAS À PAS, "
                             "TOUT AU CLIC",
                  style="Titre.TLabel").pack(side="left")
        ttk.Label(haut, text=f"GUI v{VERSION} · {EDITION}",
                  style="Sous.TLabel").pack(side="right")

        # ---- le corps : les étapes à gauche, le contenu à droite
        corps = ttk.Frame(racine, padding=(14, 4))
        corps.pack(fill="both", expand=True)
        corps.columnconfigure(1, weight=1)
        corps.rowconfigure(0, weight=1)

        self.cadre_etapes = ttk.Frame(corps, padding=(10, 6, 14, 6),
                                      borderwidth=1, relief="solid")
        self.cadre_etapes.grid(row=0, column=0, sticky="nsw")
        self.boutons_etapes = {}
        self.pastilles = {}
        ttk.Label(self.cadre_etapes, text="LES ÉTAPES",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w",
                                                           pady=(0, 6))
        for numero, titre, sous in ETAPES:
            ligne = ttk.Frame(self.cadre_etapes)
            ligne.pack(anchor="w", fill="x", pady=2)
            pastille = tk.Label(ligne, text="○", fg=COULEUR_ATTENTE,
                                bg=COULEUR_FOND, width=3)
            pastille.pack(side="left")
            bouton = ttk.Button(
                ligne, text=f"{numero}. {titre}", style="Etape.TButton",
                command=lambda n=numero: self.aller_etape(n))
            bouton.pack(side="left", fill="x", expand=True)
            ttk.Label(self.cadre_etapes, text="   " + sous,
                      style="Sous.TLabel",
                      font=("TkDefaultFont", 8)).pack(anchor="w")
            self.boutons_etapes[numero] = bouton
            self.pastilles[numero] = pastille

        self.cadre_contenu = ttk.Frame(corps, borderwidth=1,
                                       relief="solid")
        self.cadre_contenu.grid(row=0, column=1, sticky="nsew")

        # ---- le journal et le verdict, en bas
        bas = ttk.Frame(racine, padding=(14, 4, 14, 10))
        bas.pack(fill="both")
        bas.columnconfigure(0, weight=1)
        self.journal = scrolledtext.ScrolledText(
            bas, height=9, font=POLICE_FIXE, state="disabled",
            background="#ffffff", relief="solid", borderwidth=1,
            wrap="word")
        self.journal.grid(row=0, column=0, sticky="nsew", pady=(0, 6))
        self.journal.tag_config("titre", foreground=COULEUR_VERTE,
                                font=("TkFixedFont", 10, "bold"))
        self.journal.tag_config("vert", foreground=COULEUR_VERTE)
        self.journal.tag_config("rouge", foreground=COULEUR_ROUGE)
        self.journal.tag_config("refus", foreground=COULEUR_ROUGE,
                                font=("TkFixedFont", 10, "bold"))
        self.var_verdict = tk.StringVar(
            value="Le GUI est ouvert — commencez au catalogue (étape 1).")
        self.droit = ttk.Frame(bas)
        self.droit.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        self.etiquette_verdict = ttk.Label(
            self.droit, textvariable=self.var_verdict,
            style="Verdict.TLabel", wraplength=330, justify="left")
        self.etiquette_verdict.pack(anchor="ne", pady=2)

        # ---- l'état restauré (le présent GUI, puis l'héritage v1)
        if kit_choisi is not None:
            self.etat["kit"] = str(kit_choisi)
        self.dossier_pieces = (pathlib.Path(self.etat["kit"])
                               if self.etat.get("kit") else None)
        if self.dossier_pieces is None:
            self.dossier_pieces = trouver_dossier_pieces()
        if self.dossier_pieces is not None:
            self.etat["kit"] = str(self.dossier_pieces)
        if self.etat.get("atelier"):
            candidat = atelier_valide(self.etat["atelier"])
            if candidat is not None:
                self.atelier = candidat
        if self.atelier is None and self.dossier_pieces is not None:
            retrouvé = trouver_atelier(self.dossier_pieces.parent)
            if retrouvé is not None:
                self.atelier = retrouvé
                self.etat["atelier"] = str(retrouvé)
        if self.dossier_pieces is not None:
            resultat = verifier_pieces(self.dossier_pieces)
            self.verrou_vert = all(ok for _, ok, _ in resultat)

        self.enreg.ligne(f"GUI ouvert — kit={self.dossier_pieces}, "
                         f"atelier={self.atelier}, verrou="
                         f"{'VERT' if self.verrou_vert else 'PAS ENCORE'}")
        self.journal_ajoute(f"Le GUI de tous les runs est ouvert ({EDITION}).")
        if heritage:
            self.journal_ajoute(
                f"L'HÉRITAGE du GUI campagne v1 est PORTÉ : {heritage} — "
                "l'atelier, la calibration et les kits choisis survivent "
                "(la campagne continue, jamais ne recommence).", "vert")
        self.journal_ajoute("Ce GUI ne signe jamais, ne dépose jamais, ne "
                            "fabrique aucun chiffre — il conduit vos gestes, "
                            "les recoupe et les consigne (D189/CA5/CA6).")
        if self.dossier_pieces is None:
            self.journal_ajoute("Le dossier des pièces campagne-d204 n'est "
                                "pas encore choisi — l'étape 2 vous le "
                                "demande (les sept autres runs, eux, vivent "
                                "de leurs fichiers 1-clic seuls).", "refus")
        self._rafraichir_etapes()
        self.executeur.pompe()
        self.aller_etape(1)

    # ------------------------------------------------------------------ util
    def journal_ajoute(self, texte: str, genre: str = "info") -> None:
        self.journal.configure(state="normal")
        self.journal.insert("end", texte.rstrip() + "\n", genre)
        self.journal.see("end")
        self.journal.configure(state="disabled")
        self.enreg.ligne(texte, genre)

    def verdict(self, ok, texte: str) -> None:
        self.var_verdict.set(texte)
        couleur = COULEUR_ATTENTE if ok is None else (
            COULEUR_VERTE if ok else COULEUR_ROUGE)
        self.etiquette_verdict.configure(foreground=couleur)

    def sur_fin_geste(self) -> None:
        """Après un geste qui touche l'état : les étapes se réévaluent."""
        if self.dossier_pieces is not None:
            resultat = verifier_pieces(self.dossier_pieces)
            self.verrou_vert = all(ok for _, ok, _ in resultat)
        self._rafraichir_etapes()

    def _rafraichir_etapes(self) -> None:
        accessible = {1: True,
                      2: True,
                      3: self.verrou_vert,
                      4: self.verrou_vert,
                      5: True,
                      6: True,
                      7: True}
        for numero, bouton in self.boutons_etapes.items():
            bouton.configure(state=("normal" if accessible[numero]
                                    else "disabled"))
        faits = {1: False,
                 2: self.verrou_vert,
                 3: self.etat.get("calibration", {}).get("statut") == "VERT",
                 4: self.atelier is not None
                 and bool(self._lire_livraisons_toutes()),
                 5: bool(self.etat.get("runs_1clic")),
                 6: False, 7: False}
        for numero, pastille in self.pastilles.items():
            if faits.get(numero):
                pastille.configure(text="●", fg=COULEUR_VERTE)
            elif accessible[numero]:
                pastille.configure(text="○", fg=COULEUR_ATTENTE)
            else:
                pastille.configure(text="○", fg=COULEUR_BORD)

    def _lire_livraisons_toutes(self) -> list:
        if self.atelier is None:
            return []
        return _lire_csv_gabarit(self.atelier / "livraisons.csv")

    # ------------------------------------------------------------- navigation
    def aller_etape(self, numero: int) -> None:
        limite = {3: "le verrou doit tenir (étape 2) avant toute mesure "
                     "de campagne",
                  4: "le verrou doit tenir (étape 2) avant toute unité"}
        if numero in limite and not self.verrou_vert:
            self.verdict(False, f"REFUS — {limite[numero]} (fail-closed).")
            return
        for enfant in self.cadre_contenu.winfo_children():
            enfant.destroy()
        self.journal_ajoute(f"— l'étape {numero} : {ETAPES[numero - 1][1]}")
        if numero == 1:
            self.page_catalogue()
        elif numero == 2:
            self.page_verrou()
        elif numero == 3:
            self.page_calibration()
        elif numero == 4:
            self.page_campagne()
        elif numero == 5:
            self.page_autres_runs()
        elif numero == 6:
            self.page_suivi()
        else:
            self.page_pieces()

    def _cadre(self, titre: str, sous_titre: str = "") -> ttk.Frame:
        cadre = ttk.Frame(self.cadre_contenu, padding=(16, 12))
        cadre.pack(fill="both", expand=True)
        ttk.Label(cadre, text=titre, style="Titre.TLabel").pack(anchor="w")
        if sous_titre:
            ttk.Label(cadre, text=sous_titre, style="Sous.TLabel",
                      wraplength=820, justify="left").pack(anchor="w",
                                                           pady=(2, 8))
        return cadre

    @staticmethod
    def _encadre(parent, texte: str, couleur: str = COULEUR_ENCRE) -> None:
        boite = tk.Label(parent, text=texte, fg=couleur, bg="#ffffff",
                         relief="solid", borderwidth=1, justify="left",
                         anchor="w", wraplength=800, padx=12, pady=10)
        boite.pack(fill="x", pady=(4, 8))

    # ==================================================================
    # ÉTAPE 1 — LE CATALOGUE
    # ==================================================================
    def page_catalogue(self) -> None:
        cadre = self._cadre(
            "ÉTAPE 1 — LE CATALOGUE DE TOUS LES TESTS ET RUNS",
            "Tout ce qui se vit, tout ce qui s'attend, tout ce qui est "
            "fermé — nommé, jamais maquillé (D189). Choisissez une ligne "
            "puis CONDUIRE : la campagne s'ouvre à son verrou (étape 2), "
            "chaque run 1-clic s'ouvre à sa conduite pas à pas (étape 5).")
        verrou = ("VERT — le plan VERROUILLÉ tient" if self.verrou_vert
                  else "PAS ENCORE — l'étape 2 le vit (la campagne "
                       "l'exige, les autres runs non)")
        self._encadre(
            cadre,
            "L'ORDRE DES GESTES RESTANTS (le LISEZMOI-RUNS-RESTANTS, la "
            "voie 2 fermée à l'Entrée 278) :\n"
            "  1. LA CAMPAGNE D204 aux deux bras — le travail de fond, le "
            "plan fait foi ;\n"
            "  2. LE GESTE B sur un silicium qui A SHA-NI — le diagnostic "
            "choisit la machine ;\n"
            "  3. LA CÉRÉMONIE DU SÉQUESTRE à la machine hors-ligne ;\n"
            "  4. LE κ le jour des deux jeux d'annotations.\n"
            "  (facultatif : les rejeux voie 1 / voie 2 / témoin vitrine — "
            "chaque témoin AUTO compte, D99 ; le rejeu ne re-scelle rien, "
            "D165.)\n"
            f"LE VERROU DE CAMPAGNE : {verrou} · L'ATELIER : "
            + (str(self.atelier) if self.atelier
               else "pas né (l'étape 2 le fait naître)"))

        zone = ttk.Frame(cadre)
        zone.pack(fill="both", expand=True)
        colonnes = ("run", "etat", "quoi", "conductible")
        self.table_catalogue = ttk.Treeview(
            zone, columns=colonnes, show="headings", height=13)
        for col, (nom, largeur, ancrage) in {
                "run": ("LE RUN", 250, "w"),
                "etat": ("L'ÉTAT", 200, "w"),
                "quoi": ("CE QUE C'EST", 320, "w"),
                "conductible": ("CONDUITE", 85, "center")}.items():
            self.table_catalogue.heading(col, text=nom)
            self.table_catalogue.column(col, width=largeur,
                                        anchor=ancrage, stretch=False)
        self.table_catalogue.column("quoi", stretch=True)
        self.table_catalogue.pack(fill="both", expand=True)
        self.table_catalogue.tag_configure("vert", foreground=COULEUR_VERTE)
        self.table_catalogue.tag_configure("attente",
                                           foreground=COULEUR_ATTENTE)
        self.table_catalogue.tag_configure("rouge", foreground=COULEUR_ROUGE)
        self.table_catalogue.tag_configure("gris", foreground="#57606a")

        # la campagne — le travail de fond
        livraisons = self._lire_livraisons_toutes()
        self.table_catalogue.insert(
            "", "end",
            values=("LA CAMPAGNE D204",
                    "OUVERT · le travail de fond",
                    "la comparaison des workflows aux deux bras "
                    f"({len(livraisons)} livr.)",
                    "ÉTAPE 2"), tags=("attente",))
        # les sept runs 1-clic
        for cle, desc in RUNS_1CLIC.items():
            n = len(self.etat.get("runs_1clic", {}).get(
                cle, {}).get("historique", []))
            etat_txt = desc["etat_court"] + (f" · {n} run(s)" if n else "")
            tag = ("vert" if desc["etat_court"].startswith("OUVERT")
                   else "attente" if desc["etat_court"].startswith(
                       "EN ATTENTE")
                   else "gris")
            self.table_catalogue.insert(
                "", "end",
                values=(desc["titre"].split(" (")[0], etat_txt,
                        desc["quoi_court"], "ÉTAPE 5"), tags=(tag,))
        # les chaînes fermées — l'histoire demeure (D143)
        for titre, etat_f, quoi in RUNS_FERMES:
            self.table_catalogue.insert(
                "", "end", values=(titre, etat_f, quoi, "—"),
                tags=("gris",))

        barre = ttk.Frame(cadre)
        barre.pack(fill="x", pady=6)
        ttk.Button(barre, text="CONDUIRE LE RUN CHOISI →",
                   style="Geste.TButton",
                   command=self.conduire_selection).pack(side="left")
        ttk.Label(barre, text="(ou double-cliquez la ligne)",
                  style="Sous.TLabel").pack(side="left", padx=8)
        ttk.Button(barre, text="RECALCULER",
                   command=self.aller_etape_catalogue).pack(
                       side="left", padx=8)
        self.table_catalogue.bind(
            "<Double-1>", lambda _e: self.conduire_selection())

    def aller_etape_catalogue(self) -> None:
        self.aller_etape(1)

    def conduire_selection(self) -> None:
        selection = self.table_catalogue.selection()
        if not selection:
            self.verdict(False, "Choisissez un run dans la table (un clic "
                                "sur sa ligne).")
            return
        valeurs = self.table_catalogue.item(selection[0], "values")
        nom = str(valeurs[0])
        if nom.startswith("LA CAMPAGNE"):
            self.aller_etape(2)
            return
        for cle, desc in RUNS_1CLIC.items():
            if desc["titre"].split(" (")[0] == nom or desc["titre"] == nom:
                self.conduire_run(cle)
                return
        # une chaîne fermée — l'histoire demeure, D143
        self.verdict(False, f"« {nom} » est FERMÉ — la mesure y est vécue, "
                            "les témoins signés ; l'histoire demeure (D143), "
                            "ce GUI ne la rejoue jamais.")

    def conduire_run(self, cle: str) -> None:
        """Ouvre l'étape 5 SUR l'onglet du run choisi."""
        self.aller_etape(5)
        onglet = getattr(self, "onglets_runs", {}).get(cle)
        if onglet is not None and hasattr(self, "notebook_runs"):
            self.notebook_runs.select(onglet)

    # ==================================================================
    # ÉTAPE 2 — LA CAMPAGNE · LE VERROU
    # ==================================================================
    def page_verrou(self) -> None:
        cadre = self._cadre(
            "ÉTAPE 2 — LA CAMPAGNE : LE VERROU",
            "Les HUIT pièces du kit recoupées sha256 par sha256, le plan "
            "pré-enregistré VERROUILLÉ en tête (son empreinte est consignée "
            "à D204 AVANT toute mesure — CA1). Une divergence : RIEN ne "
            "court, fail-closed.")
        if self.etat.get("heritage_v1"):
            self._encadre(
                cadre,
                f"L'HÉRITAGE du GUI campagne v1 est PORTÉ (depuis "
                f"{self.etat['heritage_v1']}) — l'atelier et la calibration "
                "survivent ; la campagne CONTINUE, jamais ne recommence.",
                COULEUR_VERTE)

        ligne_kit = ttk.Frame(cadre)
        ligne_kit.pack(fill="x", pady=4)
        self.var_kit = tk.StringVar(
            value=str(self.dossier_pieces) if self.dossier_pieces else
            "le dossier campagne-d204 n'est pas encore choisi")
        ttk.Label(ligne_kit, text="LE DOSSIER DES PIÈCES :",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        ligne2 = ttk.Frame(ligne_kit)
        ligne2.pack(fill="x", pady=2)
        ttk.Entry(ligne2, textvariable=self.var_kit).pack(
            side="left", fill="x", expand=True)
        ttk.Button(ligne2, text="CHOISIR LE DOSSIER…",
                   style="Geste.TButton",
                   command=self.choisir_dossier_pieces).pack(
            side="left", padx=(8, 0))

        boutons = ttk.Frame(cadre)
        boutons.pack(fill="x", pady=6)
        ttk.Button(boutons, text="RECOUPER LES HUIT PIÈCES",
                   style="Geste.TButton",
                   command=self.geste_verrou).pack(side="left")
        self.bouton_atelier = ttk.Button(
            boutons, text="OUVRIR L'ATELIER DE CAMPAGNE…",
            style="Geste.TButton", command=self.geste_ouvrir_atelier,
            state=("normal" if self.verrou_vert else "disabled"))
        self.bouton_atelier.pack(side="left", padx=(10, 0))
        ttk.Button(boutons, text="CHOISIR L'ATELIER EXISTANT…",
                   style="Geste.TButton",
                   command=self.geste_choisir_atelier).pack(
                       side="left", padx=(10, 0))

        self._encadre(cadre,
                      "L'ATELIER : né du verrou vert, UNE fois — les COPIES "
                      "datées des trois gabarits (carnet, livraisons, "
                      "défauts) y vivent et grandissent au fil de la "
                      "campagne ; les ORIGINAUX scellés demeurent INTACTS, "
                      "octet pour octet (la confrontation des empreintes, "
                      "CA5). L'atelier retourne au coffre avec les preuves.\n"
                      "CHOISIR L'ATELIER EXISTANT : si votre atelier vit "
                      "ailleurs (né du GUI campagne v1), pointez-le — le "
                      "dossier qui porte livraisons.csv ; la campagne "
                      "CONTINUE, le carnet jamais perdu.")

        zone = ttk.Frame(cadre)
        zone.pack(fill="both", expand=True)
        colonnes = ("piece", "verdict", "detail")
        self.table_verrou = ttk.Treeview(
            zone, columns=colonnes, show="headings", height=9)
        for col, (nom, largeur, ancrage) in {
                "piece": ("LA PIÈCE", 320, "w"),
                "verdict": ("LE RECOUP", 120, "center"),
                "detail": ("LE DÉTAIL", 360, "w")}.items():
            self.table_verrou.heading(col, text=nom)
            self.table_verrou.column(col, width=largeur, anchor=ancrage)
        self.table_verrou.pack(fill="both", expand=True)
        self.table_verrou.tag_configure("vert", foreground=COULEUR_VERTE)
        self.table_verrou.tag_configure("rouge", foreground=COULEUR_ROUGE)
        if self.dossier_pieces is not None:
            self.afficher_verrou(verifier_pieces(self.dossier_pieces))

    def choisir_dossier_pieces(self) -> None:
        dossier = filedialog.askdirectory(
            title="Le dossier campagne-d204 (celui des HUIT pièces — "
                  "d'un run du kit 1-clic, ou du zip du coffre)",
            initialdir=str(GUI_DIR))
        if not dossier:
            return
        candidat = pathlib.Path(dossier)
        if not (candidat / "PLAN_PREREGISTRE_COMPARAISON.md").is_file():
            self.journal_ajoute(
                f"REFUS — « {candidat} » ne porte pas le plan pré-enregistré "
                "(choisissez le dossier campagne-d204 lui-même)", "refus")
            self.verdict(False, "REFUS — ce dossier ne porte pas le plan "
                                "pré-enregistré.")
            return
        self.dossier_pieces = candidat
        self.etat["kit"] = str(candidat)
        sauver_etat(self.etat)
        self.var_kit.set(str(candidat))
        self.geste_verrou()

    def geste_verrou(self) -> None:
        if self.dossier_pieces is None:
            self.verdict(False, "REFUS — choisissez d'abord le dossier des "
                                "pièces.")
            return

        def geste():
            resultat = verifier_pieces(self.dossier_pieces)
            self.executeur.emit_appel(self.afficher_verrou, resultat)
            tout = all(ok for _, ok, _ in resultat)
            return tout, ("LES HUIT PIÈCES INTACTES — le verrou tient, le "
                          "plan == D204 (a78caf8c…)" if tout else
                          "UNE PIÈCE DIVERGE — REFUS, RIEN ne court "
                          "(fail-closed) ; re-téléchargez le kit du coffre")

        self.executeur.lancer("LE RECOUP DU VERROU", geste)

    def afficher_verrou(self, resultat) -> None:
        table = getattr(self, "table_verrou", None)
        if table is None:
            return
        table.delete(*table.get_children())
        for nom, ok, detail in resultat:
            marque = "● VERT" if ok else "● ROUGE"
            if nom == "PLAN_PREREGISTRE_COMPARAISON.md":
                detail = ("l'empreinte consignée à D204 — le verrou tient"
                          if ok else detail)
            table.insert("", "end", values=(nom, marque, detail),
                         tags=("vert" if ok else "rouge"))
        tout = all(ok for _, ok, _ in resultat)
        self.verrou_vert = tout
        if tout:
            self.bouton_atelier.configure(state="normal")
        self._rafraichir_etapes()

    def geste_ouvrir_atelier(self) -> None:
        if not self.verrou_vert or self.dossier_pieces is None:
            return
        try:
            if self.atelier is None:
                self.atelier = ouvrir_atelier(self.dossier_pieces)
                self.etat["atelier"] = str(self.atelier)
                sauver_etat(self.etat)
                self.journal_ajoute(f"L'ATELIER est né : {self.atelier}",
                                    "vert")
            self.verdict(True, f"L'atelier vit à :\n{self.atelier}\n"
                               "— les copies datées des trois gabarits y "
                               "grandissent au fil de la campagne.")
            self._rafraichir_etapes()
        except ErreurCampagne as exc:
            self.verdict(False, f"REFUS NOMMÉ : {exc}")

    def geste_choisir_atelier(self) -> None:
        """La reprise d'un atelier né ailleurs (le GUI campagne v1) —
        le dossier daté qui porte livraisons.csv ; le carnet continue."""
        dossier = filedialog.askdirectory(
            title="L'atelier de campagne EXISTANT (le dossier daté "
                  "atelier-campagne-d204-… qui porte livraisons.csv)")
        if not dossier:
            return
        candidat = atelier_valide(dossier)
        if candidat is None:
            self.journal_ajoute(
                f"REFUS — « {dossier} » ne porte pas livraisons.csv : "
                "ce n'est pas un atelier de campagne", "refus")
            self.verdict(False, "REFUS — ce dossier n'est pas un atelier "
                                "(livraisons.csv absent).")
            return
        self.atelier = candidat
        self.etat["atelier"] = str(candidat)
        sauver_etat(self.etat)
        lignes = _lire_csv_gabarit(candidat / "livraisons.csv")
        self.journal_ajoute(
            f"L'ATELIER EXISTANT est repris : {candidat} — "
            f"{len(lignes)} livraison(s) y vivent, le carnet CONTINUE",
            "vert")
        self.verdict(True, f"L'atelier est repris :\n{candidat}\n— "
                           f"{len(lignes)} livraison(s) consignée(s) ; la "
                           "campagne continue, jamais ne recommence.")
        self._rafraichir_etapes()

    # ==================================================================
    # ÉTAPE 3 — LA CAMPAGNE · LA CALIBRATION
    # ==================================================================
    def page_calibration(self) -> None:
        cadre = self._cadre(
            "ÉTAPE 3 — LA CAMPAGNE : LA CALIBRATION DU CHRONOMÈTRE",
            "La preuve d'horloge de l'instrument M4 : une pause de durée "
            "connue (2 s), mesurée par time.monotonic — la pause portable "
            "v3 à l'annonce SANS FAUTE DE PAGE DE CODES (le correctif "
            "encodage du 14/11 au soir : la pause était MESURÉE et "
            "JOURNALISÉE, l'annonce seule avait failli sous cp1252). "
            "L'écart doit rester sous la tolérance 0,05 s. "
            "UN DRY-RUN, jamais une mesure de campagne (CA1).")
        cal = self.etat.get("calibration", {})
        if cal.get("statut") == "VERT":
            self._encadre(cadre,
                          f"LA DERNIÈRE CALIBRATION : VERT "
                          f"({cal.get('ecart', '?')} s d'écart, le "
                          f"{cal.get('quand', '?')}) — l'horloge est "
                          f"prouvée. Vous pouvez la rejouer quand vous "
                          f"voulez : c'est une preuve d'instrument.",
                          COULEUR_VERTE)
        else:
            self._encadre(cadre,
                          "AUCUNE calibration VERT n'est encore consignée "
                          "— l'étape se vit avant la première mesure M4.")
        boutons = ttk.Frame(cadre)
        boutons.pack(fill="x", pady=6)
        ttk.Button(boutons, text="LANCER LA CALIBRATION (2 s)",
                   style="Geste.TButton",
                   command=self.geste_calibration).pack(side="left")
        self._encadre(cadre,
                      "CE QUE LE CHRONOMÈTRE MESURE (les listes FIXES du "
                      "plan § 4-M4, par bras) :\n"
                      "  bras T — le garde des arbres signés ; le "
                      "round-trip de la notation livrée ; l'oracle du bloc "
                      "au périmètre livré ; le build (la recomposition).\n"
                      "  bras C — la compilation gcc -O2 ; la suite de "
                      "tests du camp C ; les contrôles binaires.\n"
                      "Toute commande hors liste est un ÉCART NOMMÉ. Le "
                      "débit d'émulation n'est PAS la métrique (la "
                      "convention v0.13.0) : c'est le coût de VÉRIFICATION "
                      "qui se mesure.")

    def geste_calibration(self) -> None:
        if self.dossier_pieces is None:
            return

        def geste():
            instrument = self.dossier_pieces / "chronometre_verification.py"
            try:
                proc = subprocess.run(
                    [sys.executable, "-u", str(instrument),
                     "--calibration", "2.00"],
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=120,
                    cwd=str(self.dossier_pieces))
            except Exception as exc:
                return False, (f"le chronomètre n'a pas couru "
                               f"({type(exc).__name__}) : {exc}")
            sortie = (proc.stdout or "") + (proc.stderr or "")
            for ligne in sortie.strip().splitlines():
                if ligne.strip():
                    self.executeur.emit(ligne.strip())
            m = re.search(r"mesurée ([\d.]+) s — écart ([\d.]+) s", sortie)
            ecart = m.group(2) if m else "?"
            ok = proc.returncode == 0
            if ok:
                self.etat.setdefault("calibration", {}).update(
                    {"statut": "VERT", "ecart": ecart,
                     "quand": maintenant_local()})
                sauver_etat(self.etat)
            return ok, (f"LA CALIBRATION VERT — écart {ecart} s <= tolérance "
                        f"{TOLERANCE_CALIBRATION:.2f} s, l'horloge est "
                        "prouvée (un dry-run, jamais une mesure)" if ok
                        else "LA CALIBRATION ROUGE — l'écart dépasse la "
                             "tolérance : renvoyez cet écran TEL QUEL "
                             "(D122), le labo recoupe")

        self.executeur.lancer("LA CALIBRATION (2 s)", geste)

    # ==================================================================
    # ÉTAPE 4 — LA CAMPAGNE · LES QUATORZE UNITÉS
    # ==================================================================
    def page_campagne(self) -> None:
        cadre = self._cadre(
            "ÉTAPE 4 — LA CAMPAGNE : LES QUATORZE UNITÉS, PAS À PAS",
            "La partie contrôlée : SIX blocs aux DEUX bras (douze unités, "
            "appariées par contrat) ; la partie réaliste : UNE commande "
            "applicative réelle aux deux bras (EN ATTENTE tant qu'aucune "
            "commande n'est arrivée — un statut, jamais un résultat "
            "fabriqué). Au plus TROIS livraisons par bloc, DOUZE par "
            "application, l'arrêt au PREMIER VERT — la cap sans vert est "
            "CENSURÉE, rapportée telle quelle (§ 7).")
        self.cadre_campagne = cadre
        self.afficher_grille_unites()

    def afficher_grille_unites(self) -> None:
        cadre = getattr(self, "cadre_campagne", None)
        if cadre is None:
            return
        for enfant in cadre.winfo_children()[2:]:
            enfant.destroy()
        zone = ttk.Frame(cadre)
        zone.pack(fill="both", expand=True)
        colonnes = ("unite", "tache", "libelle", "livraisons", "dernier",
                    "etat")
        table = ttk.Treeview(zone, columns=colonnes, show="headings",
                             height=15)
        for col, (nom, largeur, ancrage) in {
                "unite": ("L'UNITÉ", 95, "w"),
                "tache": ("LA TÂCHE", 80, "w"),
                "libelle": ("LE BRAS", 240, "w"),
                "livraisons": ("LIVRÉ/CAP", 85, "center"),
                "dernier": ("DERNIER", 80, "center"),
                "etat": ("L'ÉTAT", 240, "w")}.items():
            table.heading(col, text=nom)
            table.column(col, width=largeur, anchor=ancrage)
        table.pack(fill="both", expand=True)
        table.tag_configure("vert", foreground=COULEUR_VERTE)
        table.tag_configure("attente", foreground=COULEUR_ATTENTE)
        table.tag_configure("rouge", foreground=COULEUR_ROUGE)

        for bras, libelle in BRAS:
            for tache, _ in BLOCS:
                self._inserer_unite(table, bras, tache, libelle)
        for bras, libelle in BRAS:                    # la partie réaliste
            self._inserer_unite(table, bras, "app", libelle)

        table.bind("<Double-1>",
                   lambda _e: self.ouvrir_unite_selectionnee(table))
        barre = ttk.Frame(cadre)
        barre.pack(fill="x", pady=6)
        ttk.Button(barre, text="OUVRIR L'UNITÉ CHOISIE →",
                   style="Geste.TButton",
                   command=lambda: self.ouvrir_unite_selectionnee(table)
                   ).pack(side="left")
        ttk.Label(barre, text="(ou double-cliquez la ligne)",
                  style="Sous.TLabel").pack(side="left", padx=8)
        ttk.Button(barre, text="RECALCULER",
                   command=self.afficher_grille_unites).pack(side="left",
                                                             padx=8)

    def _inserer_unite(self, table, bras: str, tache: str,
                       libelle: str) -> None:
        cap = CAP_APP if tache == "app" else CAP_BLOC
        livraisons = (livraisons_depuis(self.atelier, bras, tache)
                      if self.atelier else [])
        etat_txt = statut_unite(livraisons, cap)
        dernier = (livraisons[-1].get("verdict", "?") if livraisons else "—")
        if tache == "app" and not livraisons:
            etat_txt = "EN ATTENTE (la commande réelle)"
        tag = ("vert" if etat_txt.startswith("VERT") else
               "rouge" if etat_txt.startswith("CENSURÉE") else "attente")
        table.insert("", "end",
                     values=(f"{bras}-{tache}", tache, libelle,
                             f"{len(livraisons)} / {cap}", dernier,
                             etat_txt), tags=(tag,))

    def ouvrir_unite_selectionnee(self, table) -> None:
        selection = table.selection()
        if not selection:
            self.verdict(False, "Choisissez une unité dans la table "
                                "(un clic sur sa ligne).")
            return
        valeurs = table.item(selection[0], "values")
        bras, tache = str(valeurs[0]).split("-", 1)
        self.panneau_unite(bras, tache)

    def panneau_unite(self, bras: str, tache: str) -> None:
        for enfant in self.cadre_contenu.winfo_children():
            enfant.destroy()
        libelle_bloc = dict(BLOCS).get(
            tache, "la commande applicative réelle")
        libelle_bras = dict(BRAS)[bras]
        cap = CAP_APP if tache == "app" else CAP_BLOC
        livraisons = (livraisons_depuis(self.atelier, bras, tache)
                      if self.atelier else [])
        cadre = self._cadre(
            f"{bras}-{tache} — {libelle_bras}",
            f"La tâche {tache} ({libelle_bloc}) au bras {bras} — "
            f"{len(livraisons)} / {cap} livraisons consignées, "
            f"{statut_unite(livraisons, cap)}.")
        if tache == "app" and not self.etat.get("commande_reelle_arrivee"):
            self._encadre(cadre,
                          "LA PARTIE RÉALISTE DEMEURE EN ATTENTE — aucune "
                          "commande applicative réelle n'est encore "
                          "arrivée (le précédent R2/D189 : jamais un "
                          "exercice démonstratif). Quand la commande "
                          "vivra, le labo livrera les kits des deux bras "
                          "au coffre — cliquez alors le bouton ci-dessous "
                          "et conduisez l'unité comme les six blocs.",
                          COULEUR_ATTENTE)
            ttk.Button(cadre, text="LA COMMANDE RÉELLE EST ARRIVÉE — "
                                   "OUVRIR CETTE UNITÉ",
                       style="Geste.TButton",
                       command=lambda: self._deverrouiller_app(bras, tache)
                       ).pack(anchor="w", pady=4)
            ttk.Button(cadre, text="← TOUTES LES UNITÉS",
                       command=self.aller_etape_campagne).pack(
                anchor="w", pady=10)
            return

        carnet = ttk.Notebook(cadre)
        carnet.pack(fill="both", expand=True, pady=6)
        self._onglet_kit(carnet, bras, tache)
        self._onglet_run(carnet, bras, tache)
        self._onglet_temoin(carnet, bras, tache)
        self._onglet_carnet(carnet, bras, tache)
        self._onglet_livraison(carnet, bras, tache)
        self._onglet_defauts(carnet, bras, tache)
        self._onglet_chrono(carnet, bras, tache)
        ttk.Button(cadre, text="← TOUTES LES UNITÉS",
                   command=self.aller_etape_campagne).pack(anchor="w",
                                                           pady=8)

    def aller_etape_campagne(self) -> None:
        self.aller_etape(4)

    def _deverrouiller_app(self, bras: str, tache: str) -> None:
        if messagebox.askyesno(
                "TRIADE — la partie réaliste",
                "La commande applicative réelle est-elle ARRIVÉE ?\n\n"
                "Ce geste n'ouvre que le panneau de l'unité — il ne "
                "fabrique rien (le statut « en attente » demeure la "
                "vérité tant qu'aucun kit n'est livré)."):
            self.etat["commande_reelle_arrivee"] = True
            sauver_etat(self.etat)
            self.journal_ajoute("la commande réelle est déclarée arrivée "
                                "(la partie réaliste s'ouvre)", "titre")
            self.panneau_unite(bras, tache)

    # ------------------------------------------------------------- 1. LE KIT
    def _onglet_kit(self, carnet, bras: str, tache: str) -> None:
        onglet = ttk.Frame(carnet, padding=14)
        carnet.add(onglet, text=" 1 · KIT ")
        ttk.Label(onglet, text=(
            "LE KIT DE L'UNITÉ — livré par le labo au coffre /test (la "
            "pièce dev + le scénario + les témoins, le mécanisme de la "
            "campagne Loupe). Choisissez son DOSSIER ici ; le GUI recoupe "
            "ses EMPREINTES gravées s'il en porte — sinon le kit 1-clic "
            "fait son propre recoup à son lancement."),
            style="Sous.TLabel", wraplength=740,
            justify="left").pack(anchor="w", pady=(0, 8))
        if not hasattr(self, "vars_kit"):
            self.vars_kit = {}
        ligne = ttk.Frame(onglet)
        ligne.pack(fill="x", pady=2)
        var = tk.StringVar(value=self.etat.get("unites", {})
                           .get(f"{bras}-{tache}", {}).get("kit", ""))
        self.vars_kit[f"{bras}-{tache}"] = var
        ttk.Label(ligne, text="LE DOSSIER DU KIT :",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        ligne2 = ttk.Frame(ligne)
        ligne2.pack(fill="x", pady=2)
        ttk.Entry(ligne2, textvariable=var).pack(side="left", fill="x",
                                                 expand=True)
        ttk.Button(ligne2, text="CHOISIR…",
                   command=lambda: self._choisir_kit_unite(bras, tache)
                   ).pack(side="left", padx=(8, 0))
        boutons = ttk.Frame(onglet)
        boutons.pack(fill="x", pady=6)
        ttk.Button(boutons, text="RECOUPER LES EMPREINTES DU KIT",
                   style="Geste.TButton",
                   command=lambda: self._recouper_kit_unite(bras, tache)
                   ).pack(side="left")
        if not hasattr(self, "tables_kit"):
            self.tables_kit = {}
        zone = ttk.Frame(onglet)
        zone.pack(fill="both", expand=True)
        table = ttk.Treeview(zone, columns=("piece", "verdict", "detail"),
                             show="headings", height=7)
        for col, (nom, largeur, ancrage) in {
                "piece": ("LA PIÈCE", 300, "w"),
                "verdict": ("LE RECOUP", 100, "center"),
                "detail": ("LE DÉTAIL", 350, "w")}.items():
            table.heading(col, text=nom)
            table.column(col, width=largeur, anchor=ancrage)
        table.tag_configure("vert", foreground=COULEUR_VERTE)
        table.tag_configure("rouge", foreground=COULEUR_ROUGE)
        table.pack(fill="both", expand=True)
        self.tables_kit[f"{bras}-{tache}"] = table

    def _choisir_kit_unite(self, bras: str, tache: str) -> None:
        dossier = filedialog.askdirectory(
            title=f"Le dossier du kit de l'unité {bras}-{tache} "
                  f"(téléchargé du coffre /test)")
        if not dossier:
            return
        var = self.vars_kit.get(f"{bras}-{tache}")
        if var:
            var.set(dossier)
        self.etat.setdefault("unites", {}).setdefault(
            f"{bras}-{tache}", {})["kit"] = dossier
        sauver_etat(self.etat)
        self.journal_ajoute(f"le kit de {bras}-{tache} est choisi : "
                            f"{dossier}")
        self._recouper_kit_unite(bras, tache)

    def _recouper_kit_unite(self, bras: str, tache: str) -> None:
        var = self.vars_kit.get(f"{bras}-{tache}")
        table = self.tables_kit.get(f"{bras}-{tache}")
        if var is None or table is None:
            return
        dossier = pathlib.Path(var.get())
        if not dossier.is_dir():
            self.verdict(False, "REFUS — choisissez d'abord le dossier du "
                                "kit de cette unité.")
            return

        def geste():
            resultat = recouper_kit_unite(dossier)
            self.executeur.emit_appel(self._afficher_recoup_kit, table,
                                      resultat)
            if not resultat:
                return True, ("AUCUNE empreinte gravée ne vit au dossier — "
                              "le kit fera son propre recoup à son "
                              "lancement (le mécanisme 1-clic) ; notez-le "
                              "au carnet si vous le jugez un écart")
            tout = all(ok for _, ok, _ in resultat)
            return tout, ("LES PIÈCES DU KIT INTACTES — les empreintes "
                          "gravées recoupées" if tout else
                          "UNE PIÈCE DU KIT DIVERGE — re-téléchargez-le du "
                          "coffre /test, RIEN ne court (fail-closed)")

        self.executeur.lancer(f"LE RECOUP DU KIT {bras}-{tache}", geste)

    def _afficher_recoup_kit(self, table, resultat) -> None:
        table.delete(*table.get_children())
        for nom, ok, detail in resultat:
            table.insert("", "end", values=(nom, "● VERT" if ok
                                            else "● ROUGE", detail),
                         tags=("vert" if ok else "rouge"))

    # ------------------------------------------------------------- 2. LE RUN
    def _onglet_run(self, carnet, bras: str, tache: str) -> None:
        onglet = ttk.Frame(carnet, padding=14)
        carnet.add(onglet, text=" 2 · RUN ")
        ttk.Label(onglet, text=(
            "LE RUN TERRAIN — le lancer OFFICIEL du kit, INTACT, dans sa "
            "propre console : le GUI ne l'intercepte jamais (le kit fait "
            "naître son dossier de run daté, recoupe ses pièces et court "
            "le scénario — D99 : ne mélangez jamais les runs). Choisissez "
            "le FICHIER lanceur (.bat du kit), puis cliquez LANCER."),
            style="Sous.TLabel", wraplength=740,
            justify="left").pack(anchor="w", pady=(0, 8))
        var_lanceur = tk.StringVar(value=self.etat.get("unites", {})
                                   .get(f"{bras}-{tache}", {})
                                   .get("lanceur", ""))
        var_run = tk.StringVar(value=self.etat.get("unites", {})
                               .get(f"{bras}-{tache}", {})
                               .get("dernier_run", ""))
        ligne = ttk.Frame(onglet)
        ligne.pack(fill="x")
        ttk.Label(ligne, text="LE LANCEUR DU KIT :",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        l2 = ttk.Frame(ligne)
        l2.pack(fill="x", pady=2)
        ttk.Entry(l2, textvariable=var_lanceur).pack(side="left", fill="x",
                                                     expand=True)
        ttk.Button(l2, text="CHOISIR…",
                   command=lambda: self._choisir_lanceur(
                       bras, tache, var_lanceur)).pack(side="left",
                                                       padx=(8, 0))
        ligne3 = ttk.Frame(onglet)
        ligne3.pack(fill="x", pady=(6, 2))
        ttk.Label(ligne3, text="LE DOSSIER DU RUN NÉ (à consigner au "
                               "retour) :",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        l4 = ttk.Frame(ligne3)
        l4.pack(fill="x", pady=2)
        ttk.Entry(l4, textvariable=var_run).pack(side="left", fill="x",
                                                 expand=True)
        ttk.Button(l4, text="CHOISIR…",
                   command=lambda: self._choisir_run(
                       bras, tache, var_run)).pack(side="left", padx=(8, 0))
        boutons = ttk.Frame(onglet)
        boutons.pack(fill="x", pady=8)
        ttk.Button(boutons, text="LANCER LE KIT (console officielle)",
                   style="Geste.TButton",
                   command=lambda: self._lancer_kit(bras, tache,
                                                    var_lanceur)
                   ).pack(side="left")
        self._encadre(onglet,
                      "APRÈS LE RUN : le dossier né (TRIADE-…-run-…) se "
                      "choisit ci-dessus — il sera la pièce à renvoyer "
                      "ENTIER au coffre. Le témoin né du run se datera et "
                      "se signera DE VOTRE MAIN (onglet 3) — jamais par "
                      "ce GUI.")

    def _choisir_lanceur(self, bras: str, tache: str, var) -> None:
        fichier = filedialog.askopenfilename(
            title=f"Le lanceur du kit {bras}-{tache} (le .bat officiel)",
            filetypes=[("Lanceurs", "*.bat *.cmd"), ("Tous", "*.*")])
        if fichier:
            var.set(fichier)
            self.etat.setdefault("unites", {}).setdefault(
                f"{bras}-{tache}", {})["lanceur"] = fichier
            sauver_etat(self.etat)

    def _choisir_run(self, bras: str, tache: str, var) -> None:
        dossier = filedialog.askdirectory(
            title="Le dossier du run NÉ (TRIADE-…-run-…, à côté du kit)")
        if dossier:
            var.set(dossier)
            self.etat.setdefault("unites", {}).setdefault(
                f"{bras}-{tache}", {})["dernier_run"] = dossier
            sauver_etat(self.etat)
            self.journal_ajoute(f"le run de {bras}-{tache} est consigné : "
                                f"{dossier}")

    def _lancer_kit(self, bras: str, tache: str, var) -> None:
        chemin = pathlib.Path(var.get())
        if not chemin.is_file():
            self.verdict(False, "REFUS — choisissez d'abord le fichier "
                                "lanceur du kit.")
            return
        ok, texte = ouvrir_au_systeme(chemin)
        if ok:
            self.journal_ajoute(f"le kit {bras}-{tache} est lancé dans sa "
                                f"console officielle : {chemin}", "titre")
            self.verdict(True, "Le kit court dans sa console — quand le "
                               "run est fini, choisissez son dossier né "
                               "ci-dessus, puis passez à l'onglet 3.")
        else:
            self.verdict(False, f"REFUS — {texte}")

    # --------------------------------------------------- 3. LE TÉMOIN/RETOUR
    def _onglet_temoin(self, carnet, bras: str, tache: str) -> None:
        onglet = ttk.Frame(carnet, padding=14)
        carnet.add(onglet, text=" 3 · TÉMOIN ")
        self._encadre(onglet,
                      "LE GESTE QUI N'AUTOMATISE JAMAIS — dater et SIGNER "
                      "le témoin de VOTRE main, puis renvoyer le dossier "
                      "de run ENTIER au coffre /test. Le GUI ouvre les "
                      "fenêtres ; la main et le renvoi vous appartiennent "
                      "(D99).", COULEUR_ROUGE)
        boutons = ttk.Frame(onglet)
        boutons.pack(fill="x", pady=4)
        ttk.Button(boutons, text="OUVRIR LE DOSSIER DU RUN",
                   style="Geste.TButton",
                   command=lambda: self._ouvrir_run(bras, tache)).pack(
            side="left")
        ttk.Button(boutons, text="OUVRIR UN TÉMOIN AU BLOC-NOTES",
                   command=self._ouvrir_temoin).pack(side="left", padx=8)
        ttk.Button(boutons, text="OUVRIR LE COFFRE /test (Drive)",
                   command=self._ouvrir_coffre).pack(side="left")
        self._encadre(onglet,
                      "LE RENVOI : glissez le dossier du run ENTIER dans "
                      "le coffre /test (le Drive « Triade » → test) — les "
                      "pièces de preuve ne se trient jamais : le dossier "
                      "fait foi, ENTIER (le témoin signé, le VERDICT, le "
                      "journal, le paquet né du kit). Le labo recoupe au "
                      "retour, pièce par pièce, md5 par md5.")

    def _ouvrir_run(self, bras: str, tache: str) -> None:
        chemin = self.etat.get("unites", {}).get(
            f"{bras}-{tache}", {}).get("dernier_run", "")
        if not chemin:
            self.verdict(False, "REFUS — consignez d'abord le dossier du "
                                "run né (onglet 2).")
            return
        ok, texte = ouvrir_au_systeme(pathlib.Path(chemin))
        self.verdict(ok, texte if not ok else
                     f"Le dossier du run est ouvert :\n{chemin}\n— datez "
                     "et signez le témoin de votre main, puis renvoyez le "
                     "dossier ENTIER au coffre.")

    def _ouvrir_temoin(self) -> None:
        fichier = filedialog.askopenfilename(
            title="Le témoin à dater et signer (temoin*.txt du dossier "
                  "de run)",
            filetypes=[("Témoins", "*.txt"), ("Tous", "*.*")])
        if fichier:
            ok, texte = ouvrir_au_systeme(pathlib.Path(fichier))
            self.verdict(ok, texte if not ok else
                         "Le témoin est ouvert au bloc-notes — écrivez la "
                         "date, signez de votre main (« fait le "
                         "JJ/MM/AAAA / Alexis Lopez »), puis renvoyez le "
                         "dossier ENTIER.")

    def _ouvrir_coffre(self) -> None:
        import webbrowser
        webbrowser.open(COFFRE_TEST_URL)
        self.journal_ajoute("le coffre /test est ouvert au navigateur — "
                            "le renvoi du dossier ENTIER appartient à "
                            "votre main")
        self.verdict(True, "Le coffre /test est ouvert au navigateur — "
                           "glissez-y le dossier du run ENTIER.")

    # -------------------------------------------------------- 4. LE CARNET M3
    def _onglet_carnet(self, carnet, bras: str, tache: str) -> None:
        onglet = ttk.Frame(carnet, padding=14)
        carnet.add(onglet, text=" 4 · CARNET ")
        ttk.Label(onglet, text=(
            "LE TEMPS HUMAIN DE CÉRÉMONIE/REVUE — la ligne se remplit AU "
            "GESTE (jamais reconstruite de mémoire), arrondie à la minute "
            "(§ 4-M3). Les gestes du bras " + bras + " : "
            + " ; ".join(GESTES_M3[bras] + GESTES_M3["X"]) + "."),
            style="Sous.TLabel", wraplength=740,
            justify="left").pack(anchor="w", pady=(0, 8))
        champs = ttk.Frame(onglet)
        champs.pack(fill="x")

        def champ(parent, etiquette, valeur, largeur=14):
            cadre_champ = ttk.Frame(parent)
            cadre_champ.pack(side="left", padx=(0, 10))
            ttk.Label(cadre_champ, text=etiquette,
                      font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
            var = tk.StringVar(value=valeur)
            ttk.Entry(cadre_champ, textvariable=var,
                      width=largeur).pack()
            return var

        vars_c = {}
        vars_c["date"] = champ(champs, "LA DATE (AAAA-MM-JJ)",
                               dt.date.today().isoformat(), 12)
        vars_c["debut"] = champ(champs, "LE DÉBUT (HH:MM)",
                                dt.datetime.now().strftime("%H:%M"), 8)
        vars_c["fin"] = champ(champs, "LA FIN (HH:MM)", "", 8)
        ligne_geste = ttk.Frame(onglet)
        ligne_geste.pack(fill="x", pady=6)
        ttk.Label(ligne_geste, text="LE GESTE :",
                  font=("TkDefaultFont", 9, "bold")).pack(side="left")
        vars_c["geste"] = tk.StringVar(value=GESTES_M3[bras][0])
        ttk.Combobox(ligne_geste, textvariable=vars_c["geste"],
                     values=GESTES_M3[bras] + GESTES_M3["X"], width=28,
                     state="readonly").pack(side="left", padx=8)
        ttk.Label(ligne_geste, text="LES NOTES :").pack(side="left",
                                                        padx=(10, 4))
        vars_c["notes"] = tk.StringVar(value="")
        ttk.Entry(ligne_geste, textvariable=vars_c["notes"],
                  width=46).pack(side="left", fill="x", expand=True)
        ttk.Button(onglet, text="CONSIGNER LA LIGNE AU CARNET",
                   style="Geste.TButton",
                   command=lambda: self._geste_carnet(bras, tache,
                                                      vars_c)).pack(
            anchor="w", pady=8)
        self._encadre(onglet,
                      "La ligne vit à la COPIE datée du carnet, dans "
                      "l'atelier — l'original scellé demeure INTACT. "
                      "Toute interruption > 5 min ferme la ligne et en "
                      "ouvre une autre (la règle au commentaire du "
                      "gabarit).")

    def _geste_carnet(self, bras: str, tache: str, vars_c) -> None:
        if self.atelier is None:
            self.verdict(False, "REFUS — l'atelier n'est pas né (étape 2).")
            return
        try:
            r = carnet_consigner(
                self.atelier, vars_c["date"].get(), bras, tache,
                vars_c["geste"].get(), vars_c["debut"].get(),
                vars_c["fin"].get(), vars_c["notes"].get())
            self.journal_ajoute(
                f"le carnet ({bras}-{tache}) : {vars_c['geste'].get()}, "
                f"{r['minutes']} minute(s) — la ligne vit au geste",
                "vert")
            self.verdict(True, "LA LIGNE CONSIGNÉE — "
                               f"{vars_c['geste'].get()}, "
                               f"{r['minutes']} minute(s) au carnet de "
                               "l'atelier.")
            vars_c["debut"].set(dt.datetime.now().strftime("%H:%M"))
            vars_c["fin"].set("")
            self._rafraichir_etapes()
        except ErreurCampagne as exc:
            self.verdict(False, f"REFUS NOMMÉ : {exc}")

    # ---------------------------------------------------- 5. LA LIVRAISON M1
    def _onglet_livraison(self, carnet, bras: str, tache: str) -> None:
        onglet = ttk.Frame(carnet, padding=14)
        carnet.add(onglet, text=" 5 · LIVRAISON ")
        cap = CAP_APP if tache == "app" else CAP_BLOC
        livraisons = livraisons_depuis(self.atelier, bras, tache) \
            if self.atelier else []
        ttk.Label(onglet, text=(
            f"UNE LIGNE PAR RUN TERRAIN — la métrique M1 (la règle D202). "
            f"Cette unité en est à {len(livraisons)} / {cap} livraisons : "
            f"{statut_unite(livraisons, cap)}. Le GUI TIENT la cap "
            f"pré-enregistrée : il REFUSE au-delà de {cap}, et après le "
            f"PREMIER VERT (§ 7) — le refus est nommé, jamais contourné."),
            style="Sous.TLabel", wraplength=740,
            justify="left").pack(anchor="w", pady=(0, 8))
        champs = ttk.Frame(onglet)
        champs.pack(fill="x")

        def champ_l(parent, etiquette, valeur, largeur=14):
            c = ttk.Frame(parent)
            c.pack(side="left", padx=(0, 10))
            ttk.Label(c, text=etiquette,
                      font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
            var = tk.StringVar(value=valeur)
            ttk.Entry(c, textvariable=var, width=largeur).pack()
            return var

        vars_l = {}
        vars_l["date_kit"] = champ_l(champs, "LA DATE DU KIT (AAAA-MM-JJ)",
                                     dt.date.today().isoformat(), 12)
        vars_l["date_run"] = champ_l(champs, "LA DATE DU RUN (AAAA-MM-JJ)",
                                     dt.date.today().isoformat(), 12)
        ttk.Label(champs, text="LE VERDICT :",
                  font=("TkDefaultFont", 9, "bold")).pack(side="left")
        vars_l["verdict"] = tk.StringVar(value="ROUGE")
        ttk.Combobox(champs, textvariable=vars_l["verdict"],
                     values=("VERT", "ROUGE"), width=8,
                     state="readonly").pack(side="left", padx=6)
        vars_l["recoup"] = champ_l(champs, "LE RECOUP", "en attente", 14)
        ttk.Button(onglet, text="CONSIGNER LA LIVRAISON",
                   style="Geste.TButton",
                   command=lambda: self._geste_livraison(
                       bras, tache, vars_l)).pack(anchor="w", pady=8)

    def _geste_livraison(self, bras: str, tache: str, vars_l) -> None:
        if self.atelier is None:
            self.verdict(False, "REFUS — l'atelier n'est pas né (étape 2).")
            return
        try:
            r = livraison_consigner(
                self.atelier, bras, tache, vars_l["date_kit"].get(),
                vars_l["date_run"].get(), vars_l["verdict"].get(),
                vars_l["recoup"].get())
            self.journal_ajoute(
                f"la livraison {r['livraison']} est consignée "
                f"({r['numero']}/{r['cap']}, verdict "
                f"{vars_l['verdict'].get()})", "vert")
            self.verdict(True, f"LA LIVRAISON {r['livraison']} CONSIGNÉE — "
                               f"{r['numero']} / {r['cap']}. "
                               + ("L'unité est CLOSE (l'arrêt au premier "
                                  "vert)."
                                  if vars_l["verdict"].get() == "VERT"
                                  else "La suite demeure ouverte."))
            self._rafraichir_etapes()
        except ErreurCampagne as exc:
            self.verdict(False, f"REFUS NOMMÉ : {exc}")

    # ------------------------------------------------------- 6. LES DÉFAUTS
    def _onglet_defauts(self, carnet, bras: str, tache: str) -> None:
        onglet = ttk.Frame(carnet, padding=14)
        carnet.add(onglet, text=" 6 · DÉFAUTS ")
        ttk.Label(onglet, text=(
            "UN DÉFAUT SE NOMME AVANT TOUTE CORRECTION — la classe, le "
            "mécanisme, la pièce à l'appui (la discipline vaut aux DEUX "
            "bras). Le côté (règle D202) : « piece » le code écrit par "
            "l'agent seul, « kit » l'ensemble kit+pièce, « exclu » une "
            "exclusion nommée avec sa raison ([RET-NU]-like, "
            "[CORBEILLE-VIDE]-like)."),
            style="Sous.TLabel", wraplength=740,
            justify="left").pack(anchor="w", pady=(0, 8))
        livraisons = livraisons_depuis(self.atelier, bras, tache) \
            if self.atelier else []
        ids = [l.get("livraison", "") for l in livraisons]
        vars_d = {}
        r1 = ttk.Frame(onglet)
        r1.pack(fill="x", pady=2)
        ttk.Label(r1, text="LA LIVRAISON :",
                  font=("TkDefaultFont", 9, "bold")).pack(side="left")
        vars_d["livraison"] = tk.StringVar(value=ids[-1] if ids else "")
        ttk.Combobox(r1, textvariable=vars_d["livraison"], values=ids,
                     width=18).pack(side="left", padx=6)
        ttk.Label(r1, text="LA CLASSE :").pack(side="left", padx=(10, 0))
        vars_d["classe"] = tk.StringVar(value="")
        ttk.Entry(r1, textvariable=vars_d["classe"], width=18).pack(
            side="left", padx=6)
        ttk.Label(r1, text="LE MÉCANISME :").pack(side="left",
                                                  padx=(10, 0))
        vars_d["mecanisme"] = tk.StringVar(value="")
        ttk.Entry(r1, textvariable=vars_d["mecanisme"],
                  width=30).pack(side="left", fill="x", expand=True)
        r2 = ttk.Frame(onglet)
        r2.pack(fill="x", pady=2)
        ttk.Label(r2, text="LE CÔTÉ :",
                  font=("TkDefaultFont", 9, "bold")).pack(side="left")
        vars_d["cote"] = tk.StringVar(value="piece")
        ttk.Combobox(r2, textvariable=vars_d["cote"],
                     values=("piece", "kit", "exclu"), width=8,
                     state="readonly").pack(side="left", padx=6)
        ttk.Label(r2, text="LA PIÈCE À L'APPUI :").pack(side="left",
                                                        padx=(10, 0))
        vars_d["piece"] = tk.StringVar(value="")
        ttk.Entry(r2, textvariable=vars_d["piece"],
                  width=30).pack(side="left", fill="x", expand=True)
        ttk.Button(r2, text="CHOISIR…",
                   command=lambda: self._choisir_piece_appui(
                       vars_d["piece"])).pack(side="left", padx=6)
        r3 = ttk.Frame(onglet)
        r3.pack(fill="x", pady=2)
        ttk.Label(r3, text="L'EXCLUSION :",
                  font=("TkDefaultFont", 9, "bold")).pack(side="left")
        vars_d["exclusion"] = tk.StringVar(value="non")
        ttk.Combobox(r3, textvariable=vars_d["exclusion"],
                     values=("non", "oui"), width=6,
                     state="readonly").pack(side="left", padx=6)
        ttk.Label(r3, text="LA RAISON (si exclusion) :").pack(
            side="left", padx=(10, 0))
        vars_d["raison"] = tk.StringVar(value="")
        ttk.Entry(r3, textvariable=vars_d["raison"],
                  width=44).pack(side="left", fill="x", expand=True)
        ttk.Button(onglet, text="CONSIGNER LE DÉFAUT NOMMÉ",
                   style="Geste.TButton",
                   command=lambda: self._geste_defaut(bras, tache,
                                                      vars_d)).pack(
            anchor="w", pady=8)

    def _choisir_piece_appui(self, var) -> None:
        fichier = filedialog.askopenfilename(
            title="La pièce à l'appui du défaut nommé",
            filetypes=[("Tous", "*.*")])
        if fichier:
            var.set(fichier)

    def _geste_defaut(self, bras: str, tache: str, vars_d) -> None:
        if self.atelier is None:
            self.verdict(False, "REFUS — l'atelier n'est pas né (étape 2).")
            return
        try:
            defaut_consigner(
                self.atelier, bras, tache, vars_d["classe"].get(),
                vars_d["mecanisme"].get(), vars_d["cote"].get(),
                vars_d["piece"].get(), vars_d["exclusion"].get(),
                vars_d["raison"].get(), vars_d["livraison"].get())
            self.journal_ajoute(
                f"le défaut est nommé ({bras}-{tache}) : "
                f"{vars_d['classe'].get()} / {vars_d['mecanisme'].get()} "
                "— la pièce à l'appui est consignée", "vert")
            self.verdict(True, "LE DÉFAUT NOMMÉ CONSIGNÉ — la correction "
                               "peut suivre (la pièce à l'appui fait foi).")
        except ErreurCampagne as exc:
            self.verdict(False, f"REFUS NOMMÉ : {exc}")

    # ------------------------------------------------------ 7. LE CHRONO M4
    def _onglet_chrono(self, carnet, bras: str, tache: str) -> None:
        onglet = ttk.Frame(carnet, padding=14)
        carnet.add(onglet, text=" 7 · CHRONO ")
        ttk.Label(onglet, text=(
            "LE TEMPS MURAL D'UNE COMMANDE DE VÉRIFICATION — la liste est "
            "FIXÉE par le plan § 4-M4. Bras " + bras + " : "
            + " ; ".join(LISTES_M4[bras]) + ". Toute commande hors liste "
            "est un ÉCART NOMMÉ. La mesure exige le bras ; le dry-run "
            "n'écrit JAMAIS au journal de campagne (CA1)."),
            style="Sous.TLabel", wraplength=740,
            justify="left").pack(anchor="w", pady=(0, 8))
        vars_m = {}
        r1 = ttk.Frame(onglet)
        r1.pack(fill="x", pady=2)
        ttk.Label(r1, text="LA COMMANDE :",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        r2 = ttk.Frame(onglet)
        r2.pack(fill="x", pady=2)
        vars_m["commande"] = tk.StringVar(value="")
        ttk.Entry(r2, textvariable=vars_m["commande"],
                  width=70).pack(side="left", fill="x", expand=True)
        ttk.Label(r2, text=" LE LABEL :").pack(side="left")
        vars_m["label"] = tk.StringVar(value=f"{bras}-{tache}")
        ttk.Entry(r2, textvariable=vars_m["label"], width=16).pack(
            side="left")
        vars_m["dryrun"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(r2, text="dry-run",
                        variable=vars_m["dryrun"]).pack(
            side="left", padx=6)
        ttk.Button(onglet, text="CHRONOMÉTRER LA COMMANDE",
                   style="Geste.TButton",
                   command=lambda: self._geste_chrono(bras, tache,
                                                      vars_m)).pack(
            anchor="w", pady=8)
        self._encadre(onglet,
                      "La ligne naît au journal des vérifications, dans "
                      "l'atelier (comparaison_resultats/) — le dossier ne "
                      "naît que de la PREMIÈRE mesure réelle (CA1). La "
                      "calibration (étape 3) demeure la preuve d'horloge, "
                      "toujours rejouable.")

    def _geste_chrono(self, bras: str, tache: str, vars_m) -> None:
        if self.atelier is None or self.dossier_pieces is None:
            self.verdict(False, "REFUS — l'atelier n'est pas né (étape 2).")
            return
        commande = vars_m["commande"].get().strip()
        if not commande:
            self.verdict(False, "REFUS — la commande à chronométrer est "
                                "vide.")
            return

        def geste():
            instrument = self.dossier_pieces / "chronometre_verification.py"
            journal = (self.atelier / "comparaison_resultats"
                       / "journal_verifications.jsonl")
            args = [sys.executable, "-u", str(instrument),
                    "--command", commande,
                    "--label",
                    vars_m["label"].get().strip() or "verification",
                    "--bras", bras, "--tache", tache,
                    "--journal", str(journal)]
            if vars_m["dryrun"].get():
                args.append("--dryrun")
            try:
                proc = subprocess.run(
                    args, capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=3600,
                    cwd=str(self.dossier_pieces))
            except Exception as exc:
                return False, (f"le chronomètre n'a pas couru "
                               f"({type(exc).__name__}) : {exc}")
            sortie = (proc.stdout or "") + (proc.stderr or "")
            for ligne in sortie.strip().splitlines():
                if ligne.strip():
                    self.executeur.emit(ligne.strip())
            ok = proc.returncode == 0
            suffixe = ("(DRY-RUN, pas une mesure)"
                       if vars_m["dryrun"].get()
                       else "(la ligne vit au journal de campagne)")
            return ok, (f"LA COMMANDE CHRONOMÉTRÉE — {suffixe}" if ok
                        else "la commande a échoué — son code de retour "
                             "est consigné au journal ; renvoyez l'écran "
                             "TEL QUEL (D122)")

        self.executeur.lancer("LE CHRONOMÉTRAGE M4", geste)

    # ==================================================================
    # ÉTAPE 5 — LES AUTRES RUNS (les sept tests 1-clic, pas à pas)
    # ==================================================================
    def page_autres_runs(self) -> None:
        cadre = self._cadre(
            "ÉTAPE 5 — LES AUTRES RUNS : LES SEPT TESTS 1-CLIC, PAS À PAS",
            "Chaque test vit d'un FICHIER AUTONOME téléchargé du coffre "
            "/test (l'édition FICHIERS-1CLIC — un test = un fichier = un "
            "double-clic). Le GUI conduit le geste : LE FICHIER recoupé "
            "contre son empreinte GRAVÉE (fail-closed), LE RUN lancé dans "
            "SA PROPRE console, LA PIÈCE signée de VOTRE main et renvoyée "
            "ENTIER au coffre.")
        if not hasattr(self, "vars_run_1clic"):
            self.vars_run_1clic = {}
        if not hasattr(self, "tables_run_1clic"):
            self.tables_run_1clic = {}
        self.notebook_runs = ttk.Notebook(cadre)
        self.notebook_runs.pack(fill="both", expand=True, pady=6)
        self.onglets_runs = {}
        for cle, desc in RUNS_1CLIC.items():
            onglet = ttk.Frame(self.notebook_runs, padding=8)
            self.notebook_runs.add(onglet, text=f" {desc['court']} ")
            self.onglets_runs[cle] = onglet
            self._construire_onglet_run(onglet, cle)

    @staticmethod
    def _encadre_etroit(parent, texte: str,
                        couleur: str = COULEUR_ENCRE) -> None:
        """L'encadré d'une DEMI-colonne — la largeur y est étroite, le
        retour à la ligne s'y calibre (aucun texte rogné)."""
        boite = tk.Label(parent, text=texte, fg=couleur, bg="#ffffff",
                         relief="solid", borderwidth=1, justify="left",
                         anchor="w", wraplength=420, padx=10, pady=8)
        boite.pack(fill="x", pady=(4, 6))

    def _construire_onglet_run(self, onglet, cle: str) -> None:
        desc = RUNS_1CLIC[cle]
        empreinte = EMPREINTES_1CLIC[desc["bat"]]

        # ---- l'identité du run (le catalogue porte l'état général)
        self._encadre(
            onglet,
            f"{desc['titre']} — {desc['etat']}\n"
            f"CE QUE C'EST : {desc['quoi']}\n"
            f"EXIGE : {desc['exigences']}\n"
            f"LE FICHIER : {desc['bat']} — sha256 {empreinte[:16]}… "
            "(l'édition FICHIERS-1CLIC du 13/11)")

        zone = ttk.Frame(onglet)
        zone.pack(fill="both", expand=True)
        zone.columnconfigure(0, weight=1)
        zone.columnconfigure(1, weight=1)

        # ---- 1 · LE FICHIER (colonne gauche, haut)
        g_fichier = ttk.LabelFrame(zone, text=" 1 · LE FICHIER 1-CLIC ",
                                   padding=8)
        g_fichier.grid(row=0, column=0, sticky="nsew", pady=(0, 6),
                       padx=(0, 6))
        var_bat = tk.StringVar(value=self.etat.get("runs_1clic", {})
                               .get(cle, {}).get("bat", ""))
        self.vars_run_1clic[cle] = var_bat
        l1 = ttk.Frame(g_fichier)
        l1.pack(fill="x")
        ttk.Label(l1, text="LE FICHIER AUTONOME (.bat du coffre /test) :",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        l2 = ttk.Frame(l1)
        l2.pack(fill="x", pady=2)
        ttk.Entry(l2, textvariable=var_bat).pack(side="left", fill="x",
                                                 expand=True)
        ttk.Button(l2, text="CHOISIR…",
                   command=lambda: self._choisir_bat_1clic(cle)).pack(
                       side="left", padx=(8, 0))
        ttk.Button(g_fichier, text="RECOUPER (sha256 gravé)",
                   style="Geste.TButton",
                   command=lambda: self._recouper_bat_1clic(cle)).pack(
                       anchor="w", pady=6)
        table = ttk.Treeview(g_fichier, columns=("verdict", "detail"),
                             show="headings", height=2)
        for col, (nom, largeur, ancrage) in {
                "verdict": ("LE RECOUP", 100, "center"),
                "detail": ("LE DÉTAIL", 350, "w")}.items():
            table.heading(col, text=nom)
            table.column(col, width=largeur, anchor=ancrage)
        table.tag_configure("vert", foreground=COULEUR_VERTE)
        table.tag_configure("rouge", foreground=COULEUR_ROUGE)
        table.pack(fill="both", expand=True)
        self.tables_run_1clic[cle] = table

        # ---- 2 · LE RUN (colonne gauche, bas)
        g_run = ttk.LabelFrame(zone, text=" 2 · LE RUN ", padding=8)
        g_run.grid(row=1, column=0, sticky="nsew", pady=6, padx=(0, 6))
        var_run = tk.StringVar(value=self.etat.get("runs_1clic", {})
                               .get(cle, {}).get("run", ""))
        self.vars_run_1clic[cle + ":run"] = var_run
        ttk.Label(g_run, text="LE FICHIER court dans SA PROPRE console — "
                              "il fait naître son dossier de run NEUF et "
                              "daté à CÔTÉ DE LUI (D99 : ne mélangez "
                              "jamais les runs).",
                  style="Sous.TLabel", wraplength=430,
                  justify="left").pack(anchor="w", pady=(0, 4))
        ttk.Button(g_run, text="LANCER (console officielle)",
                   style="Geste.TButton",
                   command=lambda: self._lancer_bat_1clic(cle)).pack(
                       anchor="w", pady=4)
        l3 = ttk.Frame(g_run)
        l3.pack(fill="x", pady=(6, 2))
        ttk.Label(l3, text="LE DOSSIER DU RUN NÉ (à renvoyer ENTIER) :",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        l4 = ttk.Frame(l3)
        l4.pack(fill="x", pady=2)
        ttk.Entry(l4, textvariable=var_run).pack(side="left", fill="x",
                                                 expand=True)
        ttk.Button(l4, text="CHOISIR…",
                   command=lambda: self._choisir_run_1clic(cle)).pack(
                       side="left", padx=(8, 0))

        # ---- 3 · LA PIÈCE (colonne droite, haut)
        g_piece = ttk.LabelFrame(zone, text=" 3 · LA PIÈCE ", padding=8)
        g_piece.grid(row=0, column=1, sticky="nsew", pady=(0, 6))
        self._encadre_etroit(g_piece, "CE QUI RESTE À VOTRE MAIN (jamais "
                                      "automatisé) : " + desc["reste"],
                             COULEUR_ROUGE)
        boutons = ttk.Frame(g_piece)
        boutons.pack(fill="x", pady=4)
        ttk.Button(boutons, text="OUVRIR LE DOSSIER DU RUN",
                   style="Geste.TButton",
                   command=lambda: self._ouvrir_run_1clic(cle)).pack(
                       anchor="w", pady=2)
        ttk.Button(boutons, text="OUVRIR LE TÉMOIN AU BLOC-NOTES",
                   command=lambda: self._ouvrir_temoin_1clic(cle)).pack(
                       anchor="w", pady=2)
        ttk.Button(boutons, text="OUVRIR LE COFFRE /test (Drive)",
                   command=self._ouvrir_coffre).pack(anchor="w", pady=2)

        # ---- 4 · L'ÉTAT (colonne droite, bas)
        g_etat = ttk.LabelFrame(zone, text=" 4 · L'ÉTAT DU RUN ",
                                padding=8)
        g_etat.grid(row=1, column=1, sticky="nsew", pady=6)
        ttk.Label(g_etat, text="L'ATTENTE, NOMMÉE (D189 — jamais "
                               "maquillée) :\n" + desc["attente"],
                  style="Sous.TLabel", wraplength=430,
                  justify="left").pack(anchor="w", pady=(0, 4))
        ttk.Label(g_etat, text="LE CONSIGNÉ PAR CE GUI : "
                               + statut_run_1clic(self.etat, cle),
                  wraplength=430, justify="left").pack(anchor="w")

    def _choisir_bat_1clic(self, cle: str) -> None:
        desc = RUNS_1CLIC[cle]
        fichier = filedialog.askopenfilename(
            title=f"Le fichier autonome {desc['bat']} (téléchargé du "
                  "coffre /test)",
            filetypes=[("Fichiers 1-clic", "*.bat"), ("Tous", "*.*")])
        if not fichier:
            return
        var = self.vars_run_1clic.get(cle)
        if var:
            var.set(fichier)
        self.etat.setdefault("runs_1clic", {}).setdefault(
            cle, {})["bat"] = fichier
        sauver_etat(self.etat)
        # le nom du fichier choisi doit ÊTRE celui du run (le recoup
        # suivra sur l'empreinte — le nom seul ne suffit jamais)
        if pathlib.Path(fichier).name != desc["bat"]:
            self.journal_ajoute(
                f"ÉCART NOMMÉ — le fichier choisi s'appelle "
                f"« {pathlib.Path(fichier).name} », le run {cle} attend "
                f"« {desc['bat']} » : le recoup d'empreinte décide "
                "(fail-closed)", "refus")
        self._recouper_bat_1clic(cle)

    def _recouper_bat_1clic(self, cle: str) -> None:
        desc = RUNS_1CLIC[cle]
        var = self.vars_run_1clic.get(cle)
        table = self.tables_run_1clic.get(cle)
        if var is None or table is None:
            return
        chemin = pathlib.Path(var.get())
        if not str(chemin).strip():
            self.verdict(False, "REFUS — choisissez d'abord le fichier "
                                f"de {desc['titre'].lower()}.")
            return

        def geste():
            attendu = EMPREINTES_1CLIC[desc["bat"]]
            ok, detail = recouper_fichier_1clic(chemin, attendu)
            self.executeur.emit_appel(self._afficher_recoup_bat, table, ok,
                                      detail)
            return ok, (f"LE FICHIER {desc['bat']} INTACT — l'édition "
                        "gravée, le run peut courir dans sa console" if ok
                        else f"REFUS — {detail}")

        self.executeur.lancer(f"LE RECOUP DU FICHIER {desc['bat']}", geste)

    def _afficher_recoup_bat(self, table, ok, detail) -> None:
        table.delete(*table.get_children())
        table.insert("", "end", values=("● VERT" if ok else "● ROUGE",
                                        detail),
                     tags=("vert" if ok else "rouge"))

    def _lancer_bat_1clic(self, cle: str) -> None:
        desc = RUNS_1CLIC[cle]
        var = self.vars_run_1clic.get(cle)
        if var is None or not str(var.get()).strip():
            self.verdict(False, "REFUS — choisissez d'abord le fichier "
                                "1-clic (et recoupez-le : le GUI ne lance "
                                "qu'un fichier INTACT).")
            return
        chemin = pathlib.Path(var.get())
        if not chemin.is_file():
            self.verdict(False, f"REFUS — « {chemin} » n'existe pas.")
            return
        # fail-closed : le GUI ne lance qu'un fichier RECOUPÉ VERT au
        # cours de la session (l'empreinte gravée fait foi)
        attendu = EMPREINTES_1CLIC[desc["bat"]]
        ok, detail = recouper_fichier_1clic(chemin, attendu)
        table = self.tables_run_1clic.get(cle)
        if table is not None:
            self._afficher_recoup_bat(table, ok, detail)
        if not ok:
            self.journal_ajoute(f"REFUS DE LANCEMENT — {detail}", "refus")
            self.verdict(False, f"REFUS DE LANCEMENT — {detail}")
            return
        ok2, texte = ouvrir_au_systeme(chemin)
        if ok2:
            self.journal_ajoute(
                f"le fichier {desc['bat']} est lancé dans sa console "
                f"officielle : {chemin}", "titre")
            self.verdict(True, f"{desc['titre']} court dans sa console — "
                               "quand il a fini, CHOISISSEZ le dossier de "
                               "run né (TRIADE-1CLIC-…-run-…) à la "
                               "section 2, puis vivez la PIÈCE (section 3).")
        else:
            self.verdict(False, f"REFUS — {texte}")

    def _choisir_run_1clic(self, cle: str) -> None:
        dossier = filedialog.askdirectory(
            title="Le dossier du run NÉ (TRIADE-1CLIC-…-run-YYYYMMDD-…, "
                  "à côté du fichier 1-clic)")
        if not dossier:
            return
        var = self.vars_run_1clic.get(cle + ":run")
        if var:
            var.set(dossier)
        r = consigner_run_1clic(self.etat, cle, dossier)
        sauver_etat(self.etat)
        self.journal_ajoute(
            f"le run {cle} est consigné : {dossier} "
            f"({r['historique']} au total)", "vert")
        # les témoins attendus se cherchent aussitôt — l'existence se
        # constate, le contenu s'ouvre à la main (jamais parsé)
        run = pathlib.Path(dossier)
        temoins = trouver_temoins(run, RUNS_1CLIC[cle]["temoins"])
        for motif, chemin in temoins:
            if chemin is not None:
                self.journal_ajoute(f"la pièce attendue vit au run : "
                                    f"{chemin.relative_to(run)}", "vert")
            else:
                self.journal_ajoute(
                    f"la pièce attendue ({motif}) est ABSENTE du run — "
                    "l'absence est une réponse, nommée (D189)", "refus")
        self._rafraichir_etapes()

    def _ouvrir_run_1clic(self, cle: str) -> None:
        chemin = self.etat.get("runs_1clic", {}).get(cle, {}).get(
            "run", "")
        if not chemin:
            self.verdict(False, "REFUS — consignez d'abord le dossier du "
                                "run né (section 2 de cet onglet).")
            return
        ok, texte = ouvrir_au_systeme(pathlib.Path(chemin))
        self.verdict(ok, texte if not ok else
                     f"Le dossier du run est ouvert :\n{chemin}\n— "
                     "datez et signez le témoin de votre main (section 3), "
                     "puis renvoyez le dossier ENTIER au coffre.")

    def _ouvrir_temoin_1clic(self, cle: str) -> None:
        """Le témoin attendu du run consigné — ouvert au bloc-notes s'il
        vit (le PREMIER trouvé par motif) ; sinon un choix libre."""
        chemin_run = self.etat.get("runs_1clic", {}).get(cle, {}).get(
            "run", "")
        if chemin_run:
            temoins = trouver_temoins(pathlib.Path(chemin_run),
                                      RUNS_1CLIC[cle]["temoins"])
            for _, chemin in temoins:
                if chemin is not None:
                    ok, texte = ouvrir_au_systeme(chemin)
                    self.verdict(ok, texte if not ok else
                                 f"Le témoin est ouvert au bloc-notes :\n"
                                 f"{chemin}\n— écrivez la date, signez de "
                                 "votre main, puis renvoyez le dossier "
                                 "ENTIER au coffre.")
                    return
        fichier = filedialog.askopenfilename(
            title="Le témoin à dater et signer (temoin*.txt / la pièce "
                  "attendue du dossier de run)",
            filetypes=[("Témoins", "*.txt *.md"), ("Tous", "*.*")])
        if fichier:
            ok, texte = ouvrir_au_systeme(pathlib.Path(fichier))
            self.verdict(ok, texte if not ok else
                         "Le témoin est ouvert au bloc-notes — écrivez la "
                         "date, signez de votre main, puis renvoyez le "
                         "dossier ENTIER.")

    # ==================================================================
    # ÉTAPE 6 — LE SUIVI
    # ==================================================================
    def page_suivi(self) -> None:
        cadre = self._cadre(
            "ÉTAPE 6 — LE SUIVI : LES COMPTES SEULS",
            "La campagne : les comptes lus des lignes du carnet — AUCUNE "
            "agrégation orientant la suite (CA7 : l'analyse se calcule aux "
            "deux bras complets de la partie contrôlée, jamais en cours "
            "de route). Les autres runs : leurs consignations, leurs "
            "attendus — l'état nommé, rien d'autre.")
        # ---- les autres runs d'abord (le catalogue vivant)
        zone_runs = ttk.LabelFrame(cadre, text=" LES AUTRES RUNS — LES "
                                   "CONSIGNATIONS ", padding=10)
        zone_runs.pack(fill="x", pady=(0, 8))
        colonnes = ("run", "etat", "consigne")
        table_runs = ttk.Treeview(zone_runs, columns=colonnes,
                                  show="headings", height=8)
        for col, (nom, largeur, ancrage) in {
                "run": ("LE RUN", 220, "w"),
                "etat": ("L'ÉTAT NOMMÉ", 330, "w"),
                "consigne": ("LE CONSIGNÉ PAR CE GUI", 360, "w")}.items():
            table_runs.heading(col, text=nom)
            table_runs.column(col, width=largeur, anchor=ancrage)
        table_runs.pack(fill="both", expand=True)
        table_runs.tag_configure("vert", foreground=COULEUR_VERTE)
        table_runs.tag_configure("attente", foreground=COULEUR_ATTENTE)
        for cle, desc in RUNS_1CLIC.items():
            n = len(self.etat.get("runs_1clic", {}).get(
                cle, {}).get("historique", []))
            table_runs.insert(
                "", "end",
                values=(desc["titre"].split(" (")[0], desc["etat_court"],
                        statut_run_1clic(self.etat, cle)),
                tags=("vert" if n else "attente"))

        # ---- la campagne
        if self.atelier is None:
            self._encadre(cadre, "L'ATELIER DE CAMPAGNE N'EST PAS NÉ — "
                                 "son suivi vivra dès l'étape 2 vécue.",
                          COULEUR_ATTENTE)
            return

        livraisons = _lire_csv_gabarit(self.atelier / "livraisons.csv")
        defauts = _lire_csv_gabarit(self.atelier / "defauts.csv")
        carnet_lignes = _lire_csv_gabarit(
            self.atelier / "carnet_temps_humain.csv")

        minutes_totales = 0
        for l in carnet_lignes:
            try:
                minutes_totales += int(l.get("minutes", 0) or 0)
            except ValueError:
                pass
        resume = (f"LA CAMPAGNE — LES LIVRAISONS : {len(livraisons)} "
                  f"ligne(s) · LES DÉFAUTS NOMMÉS : {len(defauts)} "
                  f"ligne(s) · LE CARNET : {len(carnet_lignes)} ligne(s), "
                  f"{minutes_totales} minute(s)")
        self._encadre(cadre, resume,
                      COULEUR_VERTE if livraisons else COULEUR_ATTENTE)

        zone = ttk.Frame(cadre)
        zone.pack(fill="both", expand=True)
        tables = ttk.Notebook(zone)
        tables.pack(fill="both", expand=True)

        def table(parent, titre, lignes, colonnes):
            page = ttk.Frame(parent, padding=8)
            parent.add(page, text=f" {titre} ")
            vue = ttk.Treeview(page, columns=list(colonnes),
                               show="headings", height=8)
            for col in colonnes:
                vue.heading(col, text=col)
                vue.column(col, width=110, anchor="w")
            for ligne in lignes:
                vue.insert("", "end",
                           values=[ligne.get(c, "") for c in colonnes])
            vue.pack(fill="both", expand=True)

        table(tables, f"LES LIVRAISONS ({len(livraisons)})",
              livraisons, COLONNES_LIVRAISONS)
        table(tables, f"LES DÉFAUTS ({len(defauts)})",
              defauts, COLONNES_DEFAUTS)
        table(tables, f"LE CARNET ({len(carnet_lignes)})",
              carnet_lignes, COLONNES_CARNET)

        barre = ttk.Frame(cadre)
        barre.pack(fill="x", pady=8)
        ttk.Button(barre, text="LE RÉCAPITULATIF DES TOKENS (M2)",
                   style="Geste.TButton",
                   command=self.geste_tokens).pack(side="left")
        ttk.Button(barre, text="OUVRIR L'ATELIER",
                   command=lambda: ouvrir_au_systeme(self.atelier)
                   ).pack(side="left", padx=8)
        cal = self.etat.get("calibration", {})
        self._encadre(cadre,
                      "LA CALIBRATION : "
                      + cal.get("statut", "PAS ENCORE")
                      + (f" ({cal.get('ecart', '?')} s d'écart, le "
                         f"{cal.get('quand', '?')})"
                         if cal.get("statut") == "VERT"
                         else " — l'étape 3 se vit avant la première "
                              "mesure M4")
                      + " · LES TOKENS : chaque appel au modèle passe par "
                      "l'instrument du labo (compter_tokens.py, le log "
                      "d'usage lu à l'unité près — CA3) ; le récapitulatif "
                      "se lit du journal, rien d'autre.")

    def geste_tokens(self) -> None:
        if self.atelier is None:
            return
        journaux = sorted(self.atelier.glob("**/journal_tokens.jsonl"))
        if journaux:
            self._lancer_tokens(journaux[0])
            return
        fichier = filedialog.askopenfilename(
            title="Le journal des tokens (journal_tokens.jsonl — livré par "
                  "le labo avec les kits)",
            filetypes=[("Journal JSONL", "*.jsonl"), ("Tous", "*.*")])
        if fichier:
            self._lancer_tokens(pathlib.Path(fichier))

    def _lancer_tokens(self, journal: pathlib.Path) -> None:
        if self.dossier_pieces is None:
            return

        def geste():
            instrument = self.dossier_pieces / "compter_tokens.py"
            try:
                proc = subprocess.run(
                    [sys.executable, "-u", str(instrument), "--total",
                     "--journal", str(journal)],
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=120,
                    cwd=str(self.dossier_pieces))
            except Exception as exc:
                return False, (f"le compteur n'a pas couru "
                               f"({type(exc).__name__}) : {exc}")
            sortie = (proc.stdout or "") + (proc.stderr or "")
            for ligne in sortie.strip().splitlines():
                if ligne.strip():
                    self.executeur.emit(ligne.strip())
            return proc.returncode == 0, (
                "LE RÉCAPITULATIF DES TOKENS — lu du journal, bras par "
                "bras, phase par phase (100 % log, zéro estimation)"
                if proc.returncode == 0 else
                "le compteur a refusé — l'écran ci-dessus nomme la cause")

        self.executeur.lancer("LE RÉCAPITULATIF DES TOKENS", geste)

    # ==================================================================
    # ÉTAPE 7 — LES PIÈCES
    # ==================================================================
    def page_pieces(self) -> None:
        cadre = self._cadre(
            "ÉTAPE 7 — LES PIÈCES, OÙ VIT QUOI",
            "Le plan pré-enregistré fait foi ; la console officielle du "
            "kit demeure un chemin ENTIER (les mêmes instruments) ; le "
            "coffre /test reçoit les dossiers de run ENTIERS.")
        pieces = self.dossier_pieces

        zone = ttk.Frame(cadre)
        zone.pack(fill="both", expand=True)
        zone.columnconfigure(0, weight=1)
        zone.columnconfigure(1, weight=1)

        def bouton(parent, texte, commande):
            ttk.Button(parent, text=texte, style="Geste.TButton",
                       command=commande).pack(anchor="w", pady=3)

        def chemin_court(p) -> str:
            """Le chemin affiché court (les deux dernières composantes) —
            le chemin ENTIER vit à l'explorateur, ouvert au bouton."""
            parties = pathlib.Path(p).parts
            return str(pathlib.Path(*parties[-2:])) if p else "—"

        g1 = ttk.LabelFrame(zone, text="LE KIT DE LA CAMPAGNE",
                            padding=10)
        g1.grid(row=0, column=0, sticky="nsew", pady=4, padx=(0, 6))
        ttk.Label(g1, text=(f"le dossier des pièces : "
                            f"{chemin_court(pieces)}"
                            if pieces else
                            "le dossier des pièces n'est pas choisi "
                            "(étape 2)"),
                  wraplength=430, justify="left").pack(anchor="w")
        if pieces:
            rangee = ttk.Frame(g1)
            rangee.pack(fill="x", pady=3)
            ttk.Button(rangee, text="OUVRIR LE PLAN (le bloc-notes)",
                       command=lambda: ouvrir_au_systeme(
                           pieces / "PLAN_PREREGISTRE_COMPARAISON.md")
                       ).pack(side="left")
            ttk.Button(rangee, text="OUVRIR LE LISEZMOI",
                       command=lambda: ouvrir_au_systeme(
                           pieces / "LISEZMOI-comparaison.txt")
                       ).pack(side="left", padx=6)
            bouton(g1, "OUVRIR LA CONSOLE OFFICIELLE (le chemin console)",
                   lambda: ouvrir_au_systeme(
                       pieces / "LANCER-CAMPAGNE-D204.bat"))

        g2 = ttk.LabelFrame(zone, text="L'ATELIER DE CAMPAGNE",
                            padding=10)
        g2.grid(row=1, column=0, sticky="nsew", pady=4, padx=(0, 6))
        ttk.Label(g2, text=(f"l'atelier : {chemin_court(self.atelier)}"
                            if self.atelier
                            else "l'atelier n'est pas né (étape 2)"),
                  wraplength=430, justify="left").pack(anchor="w")
        if self.atelier:
            bouton(g2, "OUVRIR L'ATELIER (l'explorateur)",
                   lambda: ouvrir_au_systeme(self.atelier))
        bouton(g2, "OUVRIR LE COFFRE /test (le Drive « Triade » → test)",
               self._ouvrir_coffre)

        g25 = ttk.LabelFrame(zone, text="LES FICHIERS 1-CLIC (LES SEPT "
                             "RUNS)", padding=10)
        g25.grid(row=2, column=1, sticky="nsew", pady=4)
        lignes_1clic = "\n".join(
            f"  {d['bat']}  {EMPREINTES_1CLIC[d['bat']][:16]}…"
            for d in RUNS_1CLIC.values())
        ttk.Label(g25, text=(
            "chaque test vit d'un fichier autonome téléchargé du coffre "
            "/test — l'étape 5 les recoupe et les conduit :\n"
            + lignes_1clic),
            wraplength=430, justify="left").pack(anchor="w")

        g3 = ttk.LabelFrame(zone, text="LES FRONTIÈRES TENUES PAR CE GUI",
                            padding=10)
        g3.grid(row=0, column=1, rowspan=2, sticky="nsew", pady=4)
        ttk.Label(g3, text=(
            "— il ne DATERA ni SIGNERA jamais un témoin (votre main, "
            "D99) ;\n"
            "— il ne DÉPOSERA jamais au coffre (le renvoi du dossier "
            "ENTIER vous appartient) ;\n"
            "— il ne FABRIQUERA aucun chiffre (CA5/CA6 — les résultats "
            "tels quels, favorables ou non) ;\n"
            "— il ne TOUCHERA jamais les originaux scellés (les copies "
            "datées de l'atelier seulement — CA5) ;\n"
            "— il ne DÉPASSERA jamais la cap pré-enregistrée (§ 7) : "
            "TROIS livraisons par bloc, DOUZE par application, l'arrêt "
            "au premier vert ;\n"
            "— il ne LANCERA jamais un fichier 1-clic divergent (le "
            "recoup d'empreinte précède tout lancement — fail-closed) ;\n"
            "— les runs terrain vous appartiennent (CA6) : le labo "
            "prépare, recoupe et consigne."),
            wraplength=430, justify="left").pack(anchor="w")

        g4 = ttk.LabelFrame(zone, text="LE JOURNAL DE SESSION DU GUI",
                            padding=10)
        g4.grid(row=2, column=0, sticky="nsew", pady=4, padx=(0, 6))
        ttk.Label(g4, text="chaque geste du GUI y vit : "
                           f"{chemin_court(self.enreg.chemin.parent)}",
                  wraplength=430, justify="left").pack(anchor="w")
        bouton(g4, "OUVRIR LE DOSSIER DES JOURNAUX",
               lambda: ouvrir_au_systeme(DOSSIER_LOGS))


# ===========================================================================
# SECTION D — LE LANCEMENT
# ===========================================================================

def demarrer(kit_choisi=None) -> int:
    if not TKINTER_DISPONIBLE:
        print("tkinter est absent de ce Python — la fenêtre ne peut pas "
              "s'ouvrir.")
        if sys.platform.startswith("linux"):
            print("  Linux : sudo apt install python3-tk")
        elif sys.platform == "darwin":
            print("  macOS : réinstallez Python depuis python.org "
                  "(installeur incluant « Tcl/Tk »)")
        else:
            print("  Windows : réinstallez Python depuis python.org en "
                  "cochant « tcl/tk and IDLE »")
        print(f"  détail : {TKINTER_ERREUR}")
        return 1
    racine = tk.Tk()
    Application(racine, kit_choisi)
    racine.mainloop()
    return 0


def main() -> int:
    kit_choisi = None
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if "--kit" in args:
        try:
            kit_choisi = pathlib.Path(
                args[args.index("--kit") + 1]).resolve()
        except (IndexError, OSError):
            print("[REFUS NOMMÉ] --kit exige un chemin")
            return 2
    return demarrer(kit_choisi)


if __name__ == "__main__":
    sys.exit(main())
