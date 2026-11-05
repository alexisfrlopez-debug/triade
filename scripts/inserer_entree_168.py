#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_168.py — LA CONSIGNATION DU GESTE « LA CÉRÉMONIE DE L'ÈRE M9
PASSÉE SUR PIÈCES » : JOURNAL_TRAVAIL +Entrée 168 (ordre 167<168<marqueur,
rejeu REFUSÉ), worklog +Task ID 86. Tout ancrage absent = ÉCHEC NOMMÉ, rien
n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 168 — LA CÉRÉMONIE DE L'ÈRE M9 PASSÉE SUR PIÈCES : LA DETTE D166 SOLDÉE (LE GARDE VERT 13/13, L'ÉTAT « reelle » TENANT) — le geste du développeur venu et annoncé (« le fichier de signatures et la clé publique sont dans le dossier /test du drive »), le labo rapatrie, recoupe, installe (05/11 au soir)

**Le geste du développeur (l'annonce).** Le SUITE du Task 85 nommait LA CÉRÉMONIE HORS-LIGNE : signer la remise 13 arbres à la clé du 04/11, ramener signatures-I.txt + cle-publique-I.txt au coffre /test. Le développeur l'a conduite — l'annonce est venue avec la demande de la dernière version complète du document PDF Protocole TRIADE. Les DEUX pièces sont au coffre /test (constaté au sondage).

**Le rapatriement (LECTURE SEULE, md5 contrôlés).** scripts/rapatrier_ceremonie_m9.py (miroir de rapatrier_ceremonie_m8.py, D162) : signatures-I.txt (1 847 o, md5 728cf189…) et cle-publique-I.txt (66 o, md5 a082f3ce…) téléchargés par le canal OAuth du relais, md5 re-contrôlés APRÈS écriture contre les métadonnées Drive — MATCH.

**Le recoup intégral AVANT tout dépôt (le verdict, pas la croyance).** (a) L'ANCRE DE CLÉ : la clé DÉPOSÉE PAR LE DÉVELOPPEUR == 173fae9c75229b15… (l'ancre de toutes les ères — la règle d'or « JAMAIS generer » respectée, la continuité de l'état « reelle » tenue) ; l'ancre locale du dépôt identique. (b) LE FORMAT : 13/13 lignes valides « arbre balise signature-128hex », balises == la table canonique (la rotation couvre TOUS les arbres, spec § 5). (c) LE RECOUP DE L'ÈRE (D163 rejouée) : les ONZE arbres inchangés (m1-m8, demo, terrain, v06) rendent les MÊMES signatures que celles déposées à la cérémonie de l'ère M8 — la preuve de la réutilisation de la clé du 04/11 PAR LE DÉTERMINISME Ed25519, sans jamais voir la clé privée ; m0 RE-SIGNÉ (le registre figé étendu au domaine tls13 — l'empreinte 4ebe6a2c…) ; tls13 ARBRE NEUF (9ff91874… = l'arbre complet des 28 spécifications, jamais signé avant). (d) LES EMPREINTES VIVANTES == a-signer.txt 13/13 (la remise fraîche régénérée au geste du Task 85 — la charge de l'ARBRE COURANT). (e) CHAQUE SIGNATURE VÉRIFIÉE Ed25519 contre la clé de l'ère sur l'empreinte du manifeste VIVANT : 13/13 VERT.

**Le dépôt canonique (l'atomicité).** sceau_I.py deposer --cle : les 13 signatures vérifiées INTÉGRALEMENT avant toute écriture, puis installées avec les manifestes vivants — l'état « reelle (ceremonie hors-ligne, D87) » INTACT. Puis LES CONTRÔLES : verifier → TREIZE arbres VERTS, code 0 ; etat → clé « reelle », la table des treize arbres tous SIGNE (vert).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), AUCUN build exécuté (construire() est le chantier (e) — un geste à part, la remise est installée, le garde est vert, le build PEUT naître), AUCUN octet de notation (R2), m8/proxy.exe INTACT (1492b0bc…), la clé privée n'a JAMAIS traversé le bac à sable (le contrat D87 tenu — le labo n'a rien signé). Livrables : download/ceremonie-ere-m9/ (les deux pièces rapatriées), scripts/rapatrier_ceremonie_m9.py ; consignations : la présente Entrée PAR SCRIPT, worklog +Task ID 86. Ce que cela DÉBLOQUE : le build de l'ère (chantier (e) : 1.0.0-dev.1, le geste de BUILD jamais scellage) — et la PRÉSENTE DEMANDE DU DÉVELOPPEUR : la dernière version complète du document PDF Protocole TRIADE (la spécification v0.7.0, la consolidation des ères M8/M9 — le geste qui suit).

- SUITE : LA SPÉCIFICATION v0.7.0 (la demande du développeur : produire la dernière version complète du document PDF — la consolidation du programme d'après M7 : M8 franchi, M9 ouvert, le sceau à treize arbres, les cérémonies d'ère au protocole) ; puis LES CHANTIERS M9 en parallèle licite : (b) la notation des 28 blocs + les vecteurs officiels, (e) le build 1.0.0-dev.1 (le garde est vert, construire() peut naître).

"""

TASK = """
## Task ID 86 — LA CÉRÉMONIE DE L'ÈRE M9 PASSÉE SUR PIÈCES : la dette D166 soldée, le garde VERT 13/13, l'état « reelle » tenant (05/11 au soir)

- LE GESTE DU DÉVELOPPEUR VENU : l'annonce (« le fichier de signatures et la
  clé publique sont dans le dossier /test du drive ») — les deux pièces au
  coffre, le SUITE du Task 85 tenu.
- LE RAPATRIEMENT : les deux pièces md5 contrôlés après écriture contre les
  métadonnées Drive (signatures-I.txt 1 847 o, cle-publique-I.txt 66 o) —
  lecture seule, aucun écrit avant le verdict.
- LE RECOUP INTÉGRAL VERT : la clé déposée == l'ancre 173fae9c… (la règle
  d'or tenue) ; 13/13 lignes valides ; les ONZE arbres inchangés == les
  signatures de l'ère M8 (la preuve D163 par le déterminisme Ed25519) ; m0
  re-signé (registre étendu) ; tls13 arbre neuf ; empreintes vivantes ==
  la remise ; Ed25519 13/13.
- L'INSTALLATION CANONIQUE : sceau_I.py deposer (tout vérifié AVANT
  écriture) ; le garde REPASSÉ VERT 13/13 ; l'état « reelle » intact.
- FRONTIÈRES : aucune balise, aucun build (le chantier (e) est un geste à
  part), aucun octet de notation, la clé privée jamais traversée (D87) ;
  consignations : Entrée 168 PAR SCRIPT, worklog +Task ID 86 ; script
  suivi : rapatrier_ceremonie_m9.py.
- SUITE : LA SPÉCIFICATION v0.7.0 (la demande du développeur : la dernière
  version complète du document PDF) ; les chantiers M9 (b)/(e) en parallèle
  licite.

Stage Summary:
- LA DETTE DE CÉRÉMONIE DE L'ÈRE M9 EST SOLDÉE : le garde treize arbres
  verts, l'état « reelle » — le build de l'ère est DÉBLOQUÉ.
- LA PREUVE D163 REJOUÉE SUR PIÈCES : les onze arbres inchangés ont rendu
  exactement les signatures de l'ère M8 — la continuité de la clé prouvée
  sans jamais la voir.
"""


def inserer(journal_entree, task):
    j = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 168 —" in j:
        print("[inserer-168] REJEU REFUSÉ : l'Entrée 168 existe déjà.")
        return 1
    n = j.count(MARQUEUR)
    if n != 1:
        print(f"[inserer-168] ÉCHEC : marqueur {n} fois dans le journal.")
        return 1
    if "## Entrée 167 —" not in j:
        print("[inserer-168] ÉCHEC : l'Entrée 167 est absente (ordre 167<168).")
        return 1
    j = j.replace(MARQUEUR, journal_entree + MARQUEUR)
    JOURNAL.write_text(j, encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 86 —" in w:
        print("[inserer-168] REJEU REFUSÉ : le Task ID 86 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + task
    WORKLOG.write_text(w, encoding="utf-8")
    print("[inserer-168] PASSÉ : Entrée 168 insérée avant le marqueur ; worklog +Task ID 86.")
    return 0


if __name__ == "__main__":
    sys.exit(inserer(ENTREE, TASK))
