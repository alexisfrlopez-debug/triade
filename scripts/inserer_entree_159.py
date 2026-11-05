#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_159.py — JOURNAL_TRAVAIL.md : insère l'Entrée 159 PAR
SCRIPT (ordre 158<159<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 159 — LA SYNCHRO SUR PIÈCES + LE KIT DE CÉRÉMONIE DE L'ÈRE M8 DÉPOSÉ (« fais une synchro git et drive, et fais moi un kit pour la cérémonie comme tu as fait pour les précédentes ») : git f3d72e9 == GitHub (recoupé ls-remote, 0 avance/0 retard, arbre propre), le miroir Drive re-synchronisé (rc=0 : 1 126 inchangés, le bundle mis à jour), les 5 LISEZMOI RAPATRIÉS du kit Drive (md5 MATCH 5/5 — le disque labo avait encore été recyclé), LE LISEZMOI DE LA CÉRÉMONIE DE L'ÈRE ÉCRIT ET RECOUPÉ (LISEZMOI-ceremonie-ere-M8.txt : la re-signature m0 + m8, la règle d'or « JAMAIS generer » — la clé du 04/11 173fae9c… réutilisée), LE KIT DÉPLOYÉ 60/60 ALLER-RETOUR AU DOSSIER /Cérémonie (le rejeu canonique D130 — l'Entrée 132 rejouée, sans le piège du manifeste amputé)

**La demande (consignée fidèlement) et l'état constaté AVANT tout écrit.** « fais une synchro git et drive, et fais moi un kit pour la cérémonie comme tu as fait pour les précédentes » — deux gestes, l'ordre compte : la SYNCHRO d'abord (la doctrine : sur pièces, jamais sur mémoire), le KIT ensuite (le déployeur canonique existe depuis D130 : le geste demandé est un REJEU VÉRIFIÉ, pas une réinvention — la leçon de l'Entrée 132). État constaté : (1) git PROPRE à f3d72e9, la branche jalon bundle051/v0.5.1-jalon-v7 == origin (recoupé ls-remote : f3d72e9829a8…, 0 avance / 0 retard — GitHub est à la pointe, rien à pousser) ; (2) le miroir Drive portait déjà l'état f3d72e9 (le hook post-commit a tourné à CHAQUE commit : last_sync.log 05:59:21Z, fin miroir rc=0, fin kit rc=0) — le rejeu manuel de drive_sync.py confirme : rc=0, 1 126 fichiers inchangés, triade-history.bundle mis à jour ; (3) la zone download/ ÉTAIT AMPUTÉE des 5 LISEZMOI de cérémonie (le disque labo a encore été recyclé entre les sessions — mêmes traces qu'à l'Entrée 132 : ceremonie_gui.py et ceremonie_hors_ligne.py présents, les LISEZMOI absents) — LE PIÈGE DE L'ENTRÉE 132 GUETTAIT : un rejeu de maj_kit.py depuis un labo amputé aurait régénéré un MANIFESTE sans les LISEZMOI (entrées optionnelles absentes localement = « conservé tel quel côté Drive » — le manifeste n'aurait plus couvert le kit RÉEL).

**PAS 1 — LE RAPATRIEMENT + LE RECOUP DE L'ÈRE (scripts/rapatrier_lisezmoi_ceremonie.py, labo hors dépôt, même canal drive_sync, aucun secret).** Les 5 LISEZMOI téléchargés du kit Drive /Cérémonie → download/, chaque fichier vérifié md5 CONTRE LES MÉTADONNÉES Drive après écriture : **5/5 MATCH** (LISEZMOI-ceremonie-GUI 25 136 o, LISEZMOI-cle-I 5 391 o, LISEZMOI-coffre-CF2 14 246 o, LISEZMOI-coffre-CF3 9 171 o, LISEZMOI-kit 10 264 o — les mêmes tailles qu'à l'Entrée 132). PUIS LE RECOUP NOUVEAU, propre à la cérémonie de l'ère (sur métadonnées, sans téléchargement) : le kit Drive porte DÉJÀ la remise fraîche **v06/sceau-I/a-signer.txt md5 MATCH** (12 arbres — déposé au kit par le hook du commit d999103, la charge du développeur est EN PLACE), **cle-publique-I.txt MATCH** (173fae9c…, l'ancre de rotation) et **etat-cle.txt MATCH** (« reelle (ceremonie hors-ligne, D87) ») — le kit et le dépôt décrivent le MÊME état de cérémonie.

**LA PIÈCE NOUVELLE — LISEZMOI-ceremonie-ere-M8.txt ÉCRIT ET RECOUPÉ.** Le kit avait le mode d'emploi de la cérémonie de la CLÉ (LISEZMOI-cle-I.txt, la première fois : generer + signer + déposer --cle) ; il lui manquait celui de la CÉRÉMONIE DE L'ÈRE (la re-signature : PAS de generer, la clé du 04/11 réutilisée). Le LISEZMOI porte : POURQUOI (le garde-sceau D87 refuse le registre m0 étendu au M8-(a) sans re-signature — fichier modifié README.md, code 10 — et l'arbre m8 jamais signé : la dette est échue au premier build, D162) ; CE QUI A CHANGÉ (la remise compte DOUZE arbres ; DEUX empreintes ont bougé — m0 0.1.0 d94154840c9de80a… le registre étendu [les specs hello INTACTES], m8 sys.1 621daf173debcc4c… le domaine sys [README + sys-01/02/03] ; les DIX autres portent les MÊMES empreintes qu'au 04/11 — et Ed25519 est déterministe : les re-signer redonne les signatures déjà déposées) ; **LA RÈGLE D'OR : JAMAIS « generer »** (la clé du 04/11 est réutilisée, sa moitié publique 173fae9c75229b15… écrite noir sur blanc — une clé neuve romprait la continuité de l'état « réelle » ; si cle-publique-I.txt diverge : ARRÊT) ; LE PAS-À-PAS (emporter ceremonie_hors_ligne.py + a-signer.txt + cle-publique-I.txt + SA cle-I-privee.txt ; signer → signatures-I.txt 12 lignes auto-vérifiées ; verifier → TOUT VERT + la clé commence par 173fae9c… ; ramener signatures-I.txt ET cle-publique-I.txt) ; LE DÉPÔT (sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt — l'atomicité de cérémonie : tout est vérifié AVANT toute écriture) ; CE QUE CELA DÉBLOQUE (le garde repassé → construire() : l'artefact m8/proxy.exe 0.9.0-dev.1 + la carte génération 8 → le chantier (d), le VRAI ntdll). LE RECOUP PAR SCRIPT avant dépôt : les empreintes m0/m8 et la clé citées dans le LISEZMOI == les pièces (a-signer.txt, cle-publique-I.txt — AUCUN chiffre inventé), les empreintes vivantes des DIX arbres inchangés == leurs manifestes déposés (la phrase « mêmes empreintes qu'au 04/11 » est PROUVÉE sur pièces), aucun marqueur de substitution.

**PAS 2 — LE DÉPÔT CANONIQUE (maj_kit.py ÉTENDU puis rejoué).** L'extension : RACINE_KIT reçoit l'entrée LISEZMOI-ceremonie-ere-M8.txt (optionnelle comme ses cinq aînées — le contrat D130 inchangé), et NOTE_D130 — qui alimente MANIFESTE.txt — porte désormais la mention de la cérémonie de l'ère (le développeur qui ouvre le dossier est ORIENTÉ : « le build 0.9.0-dev.1 attend la re-signature m0 + m8, suivez LISEZMOI-ceremonie-ere-M8.txt, la remise est v06/sceau-I/a-signer.txt, JAMAIS generer »). Le rejeu : gardes vertes (44 fichiers v06/ suivis par git + 9 racine requis — la zone download/ réparée par le PAS 1, plus d'entrée muette), **60 entrées attendues, 1 téléversé (LISEZMOI-ceremonie-ere-M8.txt), 1 mis à jour (MANIFESTE.txt), 58 inchangés, 60/60 vérifiés aller-retour md5** — le manifeste couvre le kit RÉEL, le piège de l'Entrée 132 est désamorcé PAR LE RAPATRIEMENT D'ABORD.

**Détail.** FRONTIÈRES : AUCUN artefact m8 écrit (m8/proxy.exe n'existe toujours pas — il naîtra de construire() après la cérémonie) ; AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; la remise a-signer.txt INCHANGÉE (12 arbres — elle était déjà au kit via le hook, le geste ne fait que la porter à la main du développeur avec son mode d'emploi) ; le scellé 0.6.0 INTACT (l'ancre R7 de l'ère) ; l'état de clé du sceau « réelle » INTACT (le kit ne porte que des preuves publiques : remise, clé PUBLIQUE, état, manifestes, signatures — AUCUN secret, D130) ; le labo ne signe rien (la cérémonie appartient au développeur, D87/D162). Livrables : download/LISEZMOI-ceremonie-ere-M8.txt (la pièce nouvelle), scripts/maj_kit.py étendu (RACINE_KIT + NOTE_D130), le kit Drive /Cérémonie à jour (60/60) ; consignations : la présente Entrée PAR SCRIPT, PLAN (la ligne M8-(c) : le kit déposé), worklog +Task ID 77 ; scripts suivis (labo, hors dépôt) : rapatrier_lisezmoi_ceremonie.py ; script suivi (dépôt) : inserer_entree_159.py.

- SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer a-signer.txt avec la clé du 04/11, ramener signatures-I.txt + cle-publique-I.txt — le kit /Cérémonie du Drive porte tout) → LE DÉPÔT (sceau_I.py deposer) → LE GARDE REPASSÉ → LE BUILD EXÉCUTÉ (construire : l'artefact m8/proxy.exe 0.9.0-dev.1 + la carte génération 8 + le verrou croisé) ; puis le chantier (d) — le kit terrain au coffre /test, le VRAI ntdll lu sur la machine du développeur.

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 159" in texte:
    sys.exit("ECHEC : l'Entrée 159 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i158 = texte.find("## Entrée 158")
if i158 < 0:
    sys.exit("ECHEC : l'Entrée 158 introuvable (l'ordre 158<159)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j158 = nouveau.find("## Entrée 158")
j159 = nouveau.find("## Entrée 159")
jm = nouveau.find(MARQUEUR)
if not (0 <= j158 < j159 < jm):
    sys.exit("ECHEC : l'ordre 158<159<marqueur n'est pas tenu "
             f"({j158}, {j159}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 159 insérée (l'ordre 158<159<marqueur constaté)")
