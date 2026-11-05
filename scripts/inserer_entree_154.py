#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_154.py — JOURNAL_TRAVAIL.md : insère l'Entrée 154 PAR
SCRIPT (ordre 153<154<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 154 — LE CHANTIER M7-(d), LA PART LABORATOIRE ACCOMPLIE (« continue » — la suite annoncée au Task 71) : L'EXPORT DE CONTINUITÉ MULTI-PROFILS VERT DE BOUT EN BOUT (le premier depuis M1 — D16/FORMAT_CARTE § 8 étendu aux TROIS profils déclarés : `riscv/export_continuite.py` : le conteneur TRIADE-EXP1 729 277 o CHIFFRÉ (XChaCha20-Poly1305, AAD = en-tête clair ; la clé : Argon2id 64 Mio/3 it sur un sel DÉDIÉ à l'export — jamais celui d'une carte — puis HKDF à contexte propre) + SIGNÉ (Ed25519, la lignée D27 du projet) portant 126 fichiers — la couche I : 81 spécifications (m0..m5 win, unix/I LES CANONIQUES partagées, riscv/I les miroirs sr), la couche B : CINQ artefacts (m5/proxy.exe 0.6.0 le scellé de la lignée win, unix/sonde 0.7.0-dev.1 + unix/corpus 0.7.0, riscv/sonde 0.8.0-dev.1 + riscv/corpus 0.8.0-rc.1), la couche C : les CINQ cartes de l'ère courante (m5/carte les 52 blocs de la pile win, les quatre M6/M7) ; L'IMPORT AUTO-PORTANT aux CINQ ÉTAPES § 8.2 : (1) déchiffrement — un échec est terminal, rien n'est interprété ; (2) signature du conteneur + des CINQ cartes transportées (le vérificateur PORTÉ au script, PROUVÉ équivalent aux modules du dépôt — une seule lignée, UNE clé publique recoupée au dépôt) ; (3) LE VERROU CROISÉ : 34 empreintes de blocs (13+13 corpus, 4+4 sondes — les DEUX ISA) + les 5 artefacts ENTIERS, recalculés aux offsets du MANIFESTE et recoupés au frag-bld de CHAQUE carte — la table de géométrie (id/offset/taille/empreinte) et les paramètres PUBLICS de dérivation de chaque carte (sel Argon2id, contexte HKDF, génération) vivent AU MANIFESTE chiffré+signé : l'import ne doit au dépôt QUE la clé publique ; (4) l'oracle RÉGÉNÉRÉ depuis I (81 specs — jamais importé, D1) ; (5) la REPRISE : l'état scellé cohérent (win 0.6.0 / linux 0.7.0 / riscv 0.8.0-rc.1, la racine de la carte du jalon) ; LA PREUVE D'EXÉCUTION DE BOUT EN BOUT : les RITUELS rejoués sur les octets TRANSPORTÉS (le conteneur déchiffré en mémoire, jamais le disque) — corpus unix NATIF et corpus riscv SOUS QEMU : chacun exactement les DEUX lignes au code 0 (la parité § 8.3 aux TROIS profils dans un seul conteneur), sondes : les quatre lignes au code 6 (VERDICT_FATAL propre) ; le scellé win : FRONTIÈRE NOMMÉE (son rituel vit au poste Windows du développeur — le verrou (3) porte ses octets) ; LES CONSTATS D'ÈRES sur pièces : HUIT cartes de l'ère courante de la phrase (m3/m4/m5/terrain + les quatre M6/M7 — signatures valides, UNE seule clé D27) ; les cartes m0/m1/m2/demo/m6/m7 sont des ÈRES PASSÉES de la phrase (signatures valides, fragments NON déchiffrables avec la phrase courante — les réinitialisations D27/D30) : l'état scellé COURANT du profil win vit dans SA dernière carte de l'ère courante (m5/carte) ; LE KIT TERRAIN M7 ASSEMBLÉ ET ÉPROUVÉ (`scripts/assembler_kit_m7d.py`, modèle m6d) : le SCELLÉ riscv/corpus (ec343b4e…) + le DÉMONSTRATEUR riscv/demo (e57fc74b…) + L'INSTRUMENT EMBARQUÉ qemu-riscv64 10.0.13 STATIQUE (14 821 328 o, md5 bae5a36f… — aucun paquet, aucun réseau, aucun droit root) + le SCÉNARIO PRÉ-ASSEMBLÉ (les constantes FIGÉES depuis le plan : les 14 chaînes RECOUPÉES PAR AST au layout, le site DEP TROUVÉ PAR DÉSASSEMBLAGE @0x1ad4 « addi a0, zero, 7 » dernière occurrence, les 191 adresses du démonstrateur assemblées depuis la notation, les tailles FIGÉES 15 425/4 290) + le LISEZMOI ; L'ÉPREUVE D153 : le kit EXACT, extraction vierge + run au labo — VERT 16 PASS / 0 ÉCHEC (T0 le témoin : empreintes ASSERTÉES, l'instrument identifié version+md5, la réserve D149 NOMMÉE ; T1 le rituel de parité ×3 + les TROIS bases forcées du chargeur ; T2 la bascule fence.i pendant le trafic : transcription 15 425 o OCTET POUR OCTET, le journal cohère 1 200 indices, le DEP falsifié SIGSEGV 4 290 o EXACTS, la falsification du démonstrateur ROMPUE à l'essai 1, les bases forcées identiques ; T3 zéro régression : les DEUX fichiers relus, le rituel rejoué) ; LA CLÔTURE D143 DU RUN m6d (`scripts/deposer_kit_m7d.py`) : la vague m6d ARCHIVÉE (kit-m6d.zip + LISEZMOI-m6d.txt → archives-livraisons/vagues-m6/, md5 constatés après le geste), les PIÈCES DU RUN → archives-preuves/preuves-run-m6d/ (temoin + journal + VERDICT du run + le VERDICT-DU-RECOUP du labo — Entrée 149 : l'archive porte le JUGEMENT avec les pièces), preuves-m6/ DEMEURE avec son LISEZMOI (le réceptacle), les DEUX index mis à jour, preuves-m7/ NÉ avec son LISEZMOI, la vague m7d DÉPOSÉE à la racine (kit-m7d.zip sha256 85f7b4bf…, md5 4d17f3fa… + LISEZMOI-m7d.txt) ; L'EXPORT POUSSÉ au coffre Drive racine « Triade » (TRIADE-continuite-multiprofils-0.8.0-rc.1-20261104T235621Z.bin — la forme sous laquelle l'état protocole quitte le poste, 3-2-1) ; TROIS leçons de geste attrapées aux épreuves (D158 : qemu-user EXIGE le bit exécutable de l'image invitée — « Exec format error » constaté, le scénario le RÉTABLIT geste nommé ; les LIGNÉES HOMONYMES se chargent par CHEMIN ABSOLU — sys.modules écrase layout.py/carte_corpus.py entre unix/ et riscv/, le premier import gagne et le second rend le premier ENCORE ; l'extraction zip du bac NE RESTAURE PAS les permissions — le bit rétabli par le scénario, jamais cru) ; LE SCELLAGE 0.8.0 ATTEND LE RUN TERRAIN DU DÉVELOPPEUR (modèle m6d : le kit déposé → le run sur SA machine → le recoup sur pièces → --sceller-final) (05/11)

**Détail.** Le manifeste est AUTO-DESCENT au sens plein : la géométrie par
artefact, les paramètres publics de dérivation par carte, les versions par
profil, les contrôles effectués à l'export — tout vit au conteneur signé ;
seuls la phrase maîtresse (coffre du développeur) et la clé publique (le
dépôt — recoupement, transportée en dernier recours avec la réserve nommée)
viennent de l'extérieur. FRONTIÈRES : le conteneur chiffré ne se committe
PAS (riscv/export/ gitignoré, modèle m1/export/) ; le demo n'est PAS un
artefact de la lignée (pas de carte — l'instrument du chantier) ; le code 5
STRUCTUREL sous qemu-user (l'hôte accorde RWX sur mapping privé) ; la
concurrence HORS périmètre (mono-fil, fiche § 5) ; le kit dépose l'instrument
qemu EMBARQUÉ (statique) — la réserve instrumentale D149 NOMMÉE dans chaque
verdict, la version ET le md5 consignés au témoin. Livrables :
riscv/export_continuite.py (+ export/ le conteneur poussé au Drive),
riscv/terrain/ (scenario-m7d.py.in le gabarit, scenario-m7d.py le généré,
LISEZMOI-KIT-M7D.md), scripts/assembler_kit_m7d.py,
scripts/deposer_kit_m7d.py ; consignations : la présente Entrée PAR SCRIPT,
D158 PAR SCRIPT (à la suite de D157), fiche riscv64 (§ État le chantier (d)
labo), PLAN § État (M7-(d) la part laboratoire RÉALISÉE) + la ligne M7 du
tableau, worklog +Task ID 72 ; scripts suivis : inserer_entree_154.py,
inserer_d158.py, passe_bundle_m7d.py.

- SUITE : LE RUN TERRAIN M7-(d) DU DÉVELOPPEUR — le kit-m7d.zip au coffre
  /test (qemu-riscv64 DANS le kit, la réserve D149 nommée dans chaque
  verdict) ; les preuves renvoyées à preuves-m7/ ; le recoup sur pièces
  (D138/D145/D148) ; si vert : --sceller-final pose LA FINALE 0.8.0 — LE
  JALON M7 FRANCHI, l'universalité DÉMONTRÉE : chaque profil déclaré
  supporté a franchi ses critères.

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 154" in texte:
    sys.exit("ECHEC : l'Entrée 154 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i153 = texte.find("## Entrée 153")
if i153 < 0:
    sys.exit("ECHEC : l'Entrée 153 introuvable (l'ordre 153<154)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j153 = nouveau.find("## Entrée 153")
j154 = nouveau.find("## Entrée 154")
jm = nouveau.find(MARQUEUR)
if not (0 <= j153 < j154 < jm):
    sys.exit("ECHEC : l'ordre 153<154<marqueur n'est pas tenu "
             f"({j153}, {j154}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 154 insérée (l'ordre 153<154<marqueur constaté)")
