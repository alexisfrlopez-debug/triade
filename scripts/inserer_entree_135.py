#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_135.py — JOURNAL_TRAVAIL.md : insère l'Entrée 135 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
134 < 135 < marqueur recoupé — le même contrat que les entrées 127-134)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 135 — LA CARTE GÉNÉRATION 6 DU SCELLÉ 0.5.1 RÉPARÉE (04/11) : « répare la 0.5.1 » — l'orpheline du jalon v7 nommée et re-scellée sous la lignée D80 du coffre ; l'artefact fb41697d… OCTET POUR OCTET inchangé ; le verrou anti-rollback VIT (preuve par refus) ; la graine de signature devient DURABLE (entrée au coffre) ; D144

**La demande et le diagnostic enchaîné.** « répare la 0.5.1 ». Le périmètre d'abord complété : la branche GitHub bundle051/v0.5.1-jalon-v7 portait cd85d8a (Task 51) sans les DEUX commits de la cérémonie — 84d90c8 (PRÊTE) et a5035e1 (CONSOMMÉE) poussés à 21:12, recoupés par ls-remote (branche == HEAD, main INTACTE f62711b — la fusion reste la décision de clôture du développeur). Puis le cœur : la carte m4 génération 6 — celle qui scelle la 0.5.1 — était ORPHELLE. Les preuves enchaînées : sa signature Ed25519 est valide (auto-cohérente, pub ad98a059…) mais AUCUN fragment ne se déchiffre avec la phrase de la lignée D80 (coffre), tandis que la MÊME phrase déchiffre la carte m3 génération 5 ET la carte m4 de l'époque D104 (git 8c280d5, version 0.5.0) — la phrase est bonne, la carte est sous une autre clé. CAUSE RACINE : le labo du jalon v7 était un CLONE du bundle (RAPPORT-chirurgie : « cloné dans l'espace labo ») — .keys/ (gitignoré) n'y vivait pas ; carte_m0.charger_secrets a GÉNÉRÉ une phrase et une graine aléatoires à la première exigence du build, la garde _anti_rollback a passé SILENCIEUSEMENT (le except avale l'échec de déchiffrement : « pas de carte lisible : première construction ») et construire() — qui ne lit JAMAIS l'ancienne carte (compteurs=1, carte entièrement neuve) — a scellé la 0.5.1 sous des secrets morts avec la sandbox. Le changement de pub (f40f8a20 D104 → ad98a059 jalon v7) n'avait pas été consigné : la continuité de clé de signature s'était cassée en silence. Conséquences nommées : verrou anti-rollback de la 0.5.1 MORT (il repasse silencieusement à tout labo), verrou croisé R8 inexécutable, promesse du coffre (« lignee-D80 … déverrouille … les cartes M4+ ») fausse pour cette carte. Vestige constaté au passage : le stash « etat-partiel-d140 » (07:05, restoration du matin) — ses fichiers chirurgie sont les brouillons SUPERSEDÉS par da68021, il est CONSERVÉ tel quel (rien n'est détruit).

**La réparation (modèle D80 — re-scelage à faits strictement inchangés, scripts/reparer_carte_051.py, 23 s).** SEPT gardes fail-closed AVANT tout geste, aucune écriture avant leur verdict : G1 artefact intact (sha256 fb41697d…) ; G2 la phrase .keys EST la lignée D80, PROUVÉE par témoins croisés (m3 génération 5 + m4 D104 déchiffrées) ; G3 la carte courante est l'orpheline authentique (signature valide, racine conforme, pub ad98a059… constatée) ; G4 elle ne se déchiffre PAS en D80 (sinon rien à réparer — refus) ; G5 garde sceau-I VERTE ; G6 sceau verifier ONZE arbres verts ; G7 coffre Drive racine joignable et IDENTIQUE au local (md5 0323029a… — le canal durable existe avant d'y compter). PUIS le geste, par la machinerie EXACTE du build (aucune réinvention) : assemblage honnête (verrous structurels M3 524 + M4 492, round-trips 100 %) ; l'image M4 re-composée confrontée au scellé OCTET POUR OCTET (fb41697d… — R7 : la carte décrira bien l'artefact) SANS réécrire proxy.exe ; l'oracle D93 RE-JOUÉ (560 cas verts, graine datée 20261104, verdict 1e04996b… — le verdict inscrit à frag-bld est un verdict re-vérifié, pas une copie) ; les manifestes régénérés par build_m4.fragments_clairs (49 blocs, version=0.5.1, compteurs=1/10 — les faits de l'orpheline, le journal de carte enregistre le re-scelage) ; scellement sous lignée D80 VÉRIFIÉ EN MÉMOIRE D'ABORD (signature Ed25519, racine, déchiffrement D80, verrou croisé 38/38 blocs embarqués == artefact) avant la SEULE écriture de la carte ; verrou croisé sur disque (build_m4.verrou_croise : 49 empreintes conformes, artefact 0.5.1) ; tableau de bord régénéré (la seule ligne qui change : la graine de l'oracle, 20261028 → 20261104 — l'honnêteté du verdict daté).

**La graine devient durable (D144 — la DERNIÈRE régénération).** Les graines précédentes ont toutes péri aux recyclages du labo (e842727c M0-M2, f40f8a20 m3/terrain, ad98a059 orpheline) : une graine qui ne vit qu'en .keys/ meurt à la première restauration par bundle. La neuve (pub e9cd8c549485…) est DÉPOSÉE AU COFFRE dans le même geste : entrée TRIADE/graine-ed25519-cartes (octets BRUTS 32 o, releve documentée : obtenir TRIADE graine-ed25519-cartes --vers-fichier .keys/ed25519.seed) ; conteneur 1158 → 1906 o, md5 23a2987a9817…, poussé au RACINE du coffre Drive (update), recoupé par RELECTURE (md5 MATCH) ; export chiffré download/coffre_fort.bin ; les DEUX entrées existantes (lignee-D74, lignee-D80) INTACTES (listing 3 entrées). scripts/rapatrier_coffre_cf1.py suit (attestation 23a2987a…, 1906 o).

**Post-vérifications (la preuve que la réparation tient).** P1 la carte est LISIBLE en lignée D80 : frag-bld version=0.5.1, empreinte fb41697d…, signature Ed25519 valide — la promesse du coffre est tenue à nouveau ; P2 LE VERROU ANTI-ROLLBACK EST VIVANT : _anti_rollback() REFUSE désormais — « carte scellée (0.5.1) : reconstruction interdite — procedure lourde R6 ou nouvelle version X.Y.Z+1 requise » (avant la réparation, il passait silencieusement : c'était le défaut même) ; P3 sceau verifier ONZE arbres verts APRÈS le geste (l'arbre m4/I et sa signature n'ont pas bougé — la réparation est un fait de CARTE, le sceau ne couvre pas m4/carte/) ; P4 proxy.exe sha256 fb41697d… INTACT avant/après (28 160 o — l'artefact prouvé terrain n'a pas bougé). Écrits constatés par git status : les HUIT fichiers de m4/carte/ et RIEN d'autre côté dépôt (.keys/ gitignoré ; le log de vol scripts/reparation_carte_051.log gitignoré).

**Frontières.** L'artefact scellé 0.5.1 OCTET POUR OCTET inchangé ; l'arbre m4/I et le sceau INTOUCHÉS (onze verts avant/après, la clé réelle hors-ligne jamais sollicitée) ; l'orpheline authentique CONSERVÉE dans l'historique git (da68021 — rien n'est détruit, le re-scelage est un fait de carte, la nouvelle racine d4cf5067…) ; le coffre ne perd RIEN (2 entrées intactes, 1 ajout) ; la clé privée du sceau du développeur jamais vue ni demandée ; le stash etat-partiel-d140 conservé (vestige supersédé, nommé) ; aucune suppression côté Drive.

**Vérifiabilité.** python3 scripts/reparer_carte_051.py (rejouable — refus honnête si la carte est déjà réparée : G4) ; scripts/reparation_carte_051.log (le vol complet) ; python3 v06/sceau_I.py verifier (onze verts) ; le refus P2 rejouable (import build_m4 ; build_m4._anti_rollback()) ; coffre_fort.py lister (3 entrées) ; listing Drive racine (coffre_fort.bin md5 23a2987a…) ; git log da68021 (l'orpheline) ; ls-remote (branche == a5035e1 + le présent commit).

**SUITE.** Le scellage carte génération 7 (M5, 0.6.0) : les secrets sont désormais DURABLES (phrase lignée D80 + graine au coffre — le geste reste au développeur : quand il le demande, le labo relève les deux secrets du coffre et scelle, modèle D144) ; kit VM ÉTAPE 2 (le navigateur du bac à sable, mandataire 127.0.0.1:25000, page http://autorite.test/ sous --relever-https) ; run M5-b étape 2 — le critère (b) de D136 : la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR, la ligne de flux aux preuves. D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-134) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 135" in texte:
    sys.exit("ECHEC : l'Entrée 135 existe déjà")
i134 = texte.find("## Entrée 134")
im = texte.find(MARQUEUR)
if not (0 <= i134 < im):
    sys.exit("ECHEC : ordre inattendu (134/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 134 < 135 < marqueur
j134 = nouveau.find("## Entrée 134")
j135 = nouveau.find("## Entrée 135")
jm = nouveau.find(MARQUEUR)
if not (0 <= j134 < j135 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 135 insérée ({len(ENTREE)} caractères) — ordre 134<135<marqueur recoupé")
