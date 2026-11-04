#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_134.py — JOURNAL_TRAVAIL.md : insère l'Entrée 134 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
133 < 134 < marqueur recoupé — le même contrat que les entrées 127-133)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 134 — LA CÉRÉMONIE 0.6.0 CONSOMMÉE (04/11) : « c'est signé » — la remise du développeur déposée au sceau : ONZE arbres VERTS code 0, clé réelle INTACTE (sans rotation) ; m5 entre à la garde (ARBRES_GARDE_M5 verte d'un coup) ; la re-vérification complète M5 toute verte ; le sceau ne ment plus par sous-état (étiquette « 10 arbres » corrigée en compte dynamique)

**La remise et ses contrôles sans clé.** « c'est signé » : signatures-I.txt reçu du développeur par le chat (1 564 o, md5 a2b34831…, 11 lignes, fins CRLF — la machine Windows du geste, comme au LISEZMOI). Contrôles AVANT tout geste, sans la clé, comme le LISEZMOI l'enseigne : ONZE lignes ; balises identiques à a-signer.txt ligne à ligne (diff VIDE) ; les NEUF signatures héritées OCTET POUR OCTET identiques aux déposées (Ed25519 déterministe : c'est la MÊME clé réelle qui a signé — preuve de continuité) ; m5 sans signature déposée (attendu, l'arbre était hors sceau) ; v06 divergente (attendu, l'arbre a grandi à onze). Canal durable : la remise poussée dans /test du Drive (drive_livraison.py --dossier-test, md5 MATCH par relecture — /test porte 11 entrées, aucune suppression).

**La consommation : deposer puis verifier.** sceau_I.py deposer : les 11 signatures vérifiées intégralement contre la clé publique déposée AVANT toute écriture (l'atomicité de cérémonie — une remise invérifiable n'écrit RIEN) → « 11 signatures installées (manifestes vivants) », état de clé « reelle (ceremonie hors-ligne, D87) » INTACT — pas de rotation, la même clé signe la nouvelle intention (spec § 5). verifier : ONZE arbres VERTS code 0 — m5 = 1869422eca104a6a… (la NEUVE attendue), v06 = a8166442abe2d98f… (la RE-SIGNÉE attendue), les 9 héritées à l'identique. Écrits (et rien d'autre — git status le prouve) : signatures/m5.txt + manifestes/m5.txt NOUVEAUX ; signatures/v06.txt + manifestes/v06.txt mis à jour ; les 9 autres paires INCHANGÉES ; a-signer.txt INCHANGÉ (il vivait déjà au commit 84d90c8).

**Le geste post-cérémonie nommé par la passation.** ARBRES_GARDE_M5 étendue de m5 (m5/build_m5.py : ["m0", "m1", "m2", "m3", "m4", "m5"], commentaire historisé — la signature de m5 appartient désormais à la cérémonie 0.6.0 du 04/11) → la garde passe VERTE d'un coup, comme promis : « 6 arbres d'intention conformes à leurs signatures (m0, m1, m2, m3, m4, m5) ; clé déposée : reelle ». Re-vérification complète (build_m5.py --verifier) TOUTE VERTE : oracles structurels 524 + 312 verrous PASS, différentiels M4 560 cas + M5 365 cas verts, R7 38 blocs réutilisés du scellé 0.5.1, PE proxy.exe 0.6.0-dev.1 re-validé (sha256 4b8f6af6… INCHANGÉ). Le build nomme lui-même la suite : « [carte] génération 7 : cérémonie requise (D87) : les secrets de la carte ne vivent pas au laboratoire — l'opérateur scelle (R6/R8/R9) ».

**Le sceau ne ment plus par sous-état (défaut nommé, corrigé).** test_sceau_I.py : T3-g et le [final] imprimaient « 10 arbres » en dur — un reste de l'ère v7 ; le CONTRÔLE était juste (verifier() == OK) mais l'ÉTIQUETTE sous-étatait la table (11 arbres réels). Corrigé en compte dynamique (len(ARBRES)) : 51 PASS / 0 ÉCHEC, [final] « dépôt réel : VERT (11 arbres, canon LF D115) » — le contrôle ne ment plus dans un sens comme dans l'autre. À noter : le labo recyclé avait perdu les dépendances du build (capstone, keystone, pefile, pynacl, unicorn — pip réinstallé), rien d'autre n'a changé.

**Frontières.** La clé privée du développeur jamais vue ni demandée (la remise ne contient QUE des signatures — 11 × 128 hex, aucun octet de clé) ; la clé publique déposée INCHANGÉE (173fae9c…) ; les 9 arbres signés INCHANGÉS ; aucun artefact scellé touché (proxy 0.6.0-dev.1 4b8f6af6… et scellé 0.5.1 intacts) ; .keys/ toujours absent du labo (le scellage carte génération 7 exige le geste opérateur).

**Vérifiabilité.** python3 v06/sceau_I.py verifier (11 verts code 0) ; python3 v06/test_sceau_I.py (51 PASS, [final] 11 arbres) ; cd m5 && python3 build_m5.py --verifier (garde 6 arbres + chaîne verte) ; listing de /test (11 entrées, signatures-I.txt md5 a2b34831…) ; ce commit (signatures + manifestes + garde + étiquette).

**SUITE.** Scellage carte génération 7 : cérémonie requise, les secrets ne vivent pas au labo — le geste OPÉRATEUR sera proposé au développeur (la carte de la génération 7 porte les blocs M5 g8xxxx, verrou croisé R6/R8/R9) ; kit VM ÉTAPE 2 (le navigateur du bac à sable, mandataire 127.0.0.1:25000, page http://autorite.test/ sous --relever-https) ; run M5-b étape 2 — le critère (b) de D136 : la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR, la ligne de flux aux preuves. D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-133) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 134" in texte:
    sys.exit("ECHEC : l'Entrée 134 existe déjà")
i133 = texte.find("## Entrée 133")
im = texte.find(MARQUEUR)
if not (0 <= i133 < im):
    sys.exit("ECHEC : ordre inattendu (133/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 133 < 134 < marqueur
j133 = nouveau.find("## Entrée 133")
j134 = nouveau.find("## Entrée 134")
jm = nouveau.find(MARQUEUR)
if not (0 <= j133 < j134 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 134 insérée ({len(ENTREE)} caractères) — ordre 133<134<marqueur recoupé")
