#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_132.py — JOURNAL_TRAVAIL.md : insère l'Entrée 132 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
131 < 132 < marqueur recoupé — le même contrat que les entrées 127-131)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 132 — KIT DE CÉRÉMONIE DEMANDÉ PAR LE DÉVELOPPEUR ET DÉPLOYÉ (03/11) : « fais moi un kit pour la cérémonie que tu mettras dans le drive /Cérémonie » — le geste canonique D130 exécuté et vérifié 57/57 aller-retour, les LISEZMOI perdus au recyclage du disque labo rapatriés du kit Drive (md5 MATCH 5/5)

**La demande (consignée fidèlement) et l'état constaté.** « fais moi un kit pour la cérémonie que tu mettras dans le drive /Cérémonie » — le kit de cérémonie a déjà son DÉPLOYEUR CANONIQUE depuis D130 (scripts/maj_kit.py, suivi par git, appelé par le hook post-commit APRÈS drive_sync.py) : le geste demandé est donc un REJEU VÉRIFIÉ de l'outil, pas une réinvention. État constaté AVANT tout écrit, après le recyclage du disque labo entre les sessions : (1) la zone download/ était AMPUTÉE — les 5 LISEZMOI de cérémonie (LISEZMOI-ceremonie-GUI.txt, LISEZMOI-cle-I.txt, LISEZMOI-coffre-CF2.txt, LISEZMOI-coffre-CF3.txt, LISEZMOI-kit.txt) absents, ceremonie_gui.py et ceremonie_hors_ligne.py présents (datés 17:37) ; (2) git propre à un bruit de bits de mode — 7 fichiers 100644→100755, 0 insertion / 0 suppression, proxy.exe md5 72cf8fdd… == HEAD et sha256 4b8f6af6… (le 0.6.0-dev.1 attendu) : reset --hard (précédent Task 39, « WIP = bits de mode uniquement »), un seul non-suivi bundles-060/ (zone de travail locale, jamais committée) ; (3) le hook post-commit avait DÉJÀ déployé le kit au commit cdfabb6 (.gdrive/last_sync.log 18:21:39Z : fin miroir rc=0, fin kit rc=0) — le kit au Drive était donc déjà à jour, mais UN PIÈGE GUETTAIT : un rejeu de maj_kit.py depuis un labo amputé aurait régénéré un MANIFESTE.txt sans les 5 LISEZMOI (entrées optionnelles absentes localement = « conservé tel quel côté Drive ») — le manifeste n'aurait plus couvert le kit RÉEL, divergence silencieuse d'attestation.

**Le geste (deux pas, l'ordre compte).** PAS 1 — RAPATRIEMENT : scripts/recuperer_lisezmoi_ceremonie.py (labo, hors dépôt — même canal drive_sync, aucun secret) télécharge les 5 LISEZMOI du kit Drive /Cérémonie → download/, md5 comparé AUX MÉTADONNÉES Drive après écriture : 5/5 MATCH (25 136 + 5 391 + 14 246 + 9 171 + 10 264 octets) — le même geste que la récupération post-recyclage du 30/10 (Task 39). PAS 2 — DÉPÔT CANONIQUE : python3 scripts/maj_kit.py → gardes vertes (42 fichiers v06/ suivis par git + 9 racine requis), 57 entrées attendues (57 déjà présentes), 0 téléversés, 1 mis à jour (MANIFESTE.txt régénéré : commit de référence cdfabb6, empreintes md5 des 57 entrées, les 5 LISEZMOI de nouveau couverts), 56 inchangés, 57/57 VÉRIFIÉS aller-retour md5. Recoupement indépendant par la sonde (drive_ceremonie.py --sonde) : 15 entrées racine + le sous-dossier v06/ (42 fichiers) — la racine porte les lanceurs D118 (ceremonie ×2, autotest_cf3 ×2, migration_cf3 ×2), les copies plates « fichier seul sur clef USB » (D87), coffre_fort.py (CF1), les 5 LISEZMOI et MANIFESTE.txt.

**Leçon d'infrastructure (consignée).** Un déploiement IDEMPOTENT n'est pas toujours UN INVENTAIRE : maj_kit.py n'exige les fichiers racine que si requis=True (les LISEZMOI sont optionnels) — après une perte du disque labo, le rejeu à froid produit un manifeste AMPUTÉ sans jamais échouer. La parade tient en un réflexe : après tout recyclage, RAPATRIER D'ABORD les documents du kit depuis le Drive (la vérité durable), REJOUER ensuite le déploiement, RECOUPER enfin le manifeste (les empreintes attendues == le kit réel). Le .gitignore reçoit aussi « bundles-*/ » : la convention « zone de travail locale, jamais committée » (Entrée 131) devient une règle MÉCANIQUE — le git add -A de sync_backup.sh ne peut plus avaler un bundle de 14,8 Mio.

**Frontières.** Aucun secret dans le kit (sceau-I/ ne porte que des preuves publiques : remise, clé PUBLIQUE, état, manifestes, signatures) ; aucune suppression côté Drive (maj_kit.py est prudent : il ne supprime JAMAIS) ; /test intacte (8 entrées D143) ; arbres scellés intouchés ; aucune clé traversée ; aucun artefact touché ; le dépôt git ne reçoit que le script d'insertion, le .gitignore et la présente consignation.

**Vérifiabilité.** scripts/maj_kit.log (bilan 57/57 du 03/11 18:45) ; download/MANIFESTE.txt (copie d'audit, « Commit de référence : cdfabb6 ») ; la sonde (listing API de /Cérémonie) ; .gdrive/last_sync.log ; scripts/recuperer_lisezmoi_ceremonie.py (VERDICT 5/5).

**SUITE.** Inchangée : la cérémonie de signature par le développeur (D87 : clé hors-ligne, carte génération 7, conformité_profil à écrire), puis le kit VM ÉTAPE 2 (le navigateur du bac à sable) et le run M5-b étape 2 — le critère (b) de D136. D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-131) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 132" in texte:
    sys.exit("ECHEC : l'Entrée 132 existe déjà")
i131 = texte.find("## Entrée 131")
im = texte.find(MARQUEUR)
if not (0 <= i131 < im):
    sys.exit("ECHEC : ordre inattendu (131/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 131 < 132 < marqueur
j131 = nouveau.find("## Entrée 131")
j132 = nouveau.find("## Entrée 132")
jm = nouveau.find(MARQUEUR)
if not (0 <= j131 < j132 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 132 insérée ({len(ENTREE)} caractères) — ordre 131<132<marqueur recoupé")
