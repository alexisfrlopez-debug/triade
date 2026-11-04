#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_136.py — JOURNAL_TRAVAIL.md : insère l'Entrée 136 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
135 < 136 < marqueur recoupé — le même contrat que les entrées 127-135)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 136 — LA CARTE GÉNÉRATION 7 SCELLÉE : 0.6.0-rc.1 (04/11) : « lance le scellage » — le geste développeur attendu depuis D144 ; la machinerie carte M5 écrite (modèle D104 porté : carte_m5 fail-closed, conformité § 8.2, verrou croisé R8, anti-rollback, --sceller-rc/--sceller-final) ; cristallisation 52/52 × 10/10 ; l'artefact 4b8f6af6… OCTET POUR OCTET inchangé ; la finale 0.6.0 attend le critère (b)

**La demande et la balise choisie.** « lance le scellage » — le geste qui appartient au développeur (D87 inchangé : « le scellage d'une NOUVELLE génération de carte reste un geste qui appartient au développeur » ; D144 l'avait rendu EXÉCUTABLE en rendant les deux secrets durables au coffre). La balise est **0.6.0-rc.1**, pas la finale : le critère (b) de D136 — « un flux navigateur intercepté de bout en bout dans la VM » — n'est PAS encore prouvé (aucun navigateur n'a joué le run), et la table des versions du protocole est sans ambiguïté : `X.Y.Z-rc.N` = candidate à la validation (« dev + suite de conformité du profil verte (§ 8.2) + critères du jalon courant ; soumise à la validation terrain »), `X.Y.Z` = finale (« validation terrain consignée au journal des décisions ; balise immuable ») ; le plan m5 dit lui-même « VERSION_060 : la balise est posée à la validation terrain ». Sceller 0.6.0 aujourd'hui inscrirait dans la carte une validation qui n'existe pas — la carte ne ment pas. Modèle D104 exact : 0.5.0-rc.1 d'abord, la finale après la consignation terrain (T4 17-H). Les exigences consignées à la balise : cristallisation R6 10/10 + conformité § 8.2 + critères du jalon M5 prouvés à ce jour (oracle D136 365 cas falsification incluse ; autorité locale 13 contrôles ; étape 1 en VM isolée : runs v7/v8 verdict OK 0 réserve ; empreintes par build D134) — candidate SOUMISE au run M5-b étape 2.

**La machinerie écrite avant le geste (modèle D104 porté à la composition 0.6.0 — trois écritures).** (1) `m5/carte_m5.py` : la carte génération 7 (blocs g8xxxx, les trois révisions R3), même format que M0-M4 (XChaCha20-Poly1305, Argon2id+HKDF, racine SHA-256, Ed25519), sel de génération propre — et `charger_secrets` FAIL-CLOSED : si .keys/ est absent, AUCUN secret n'est généré, l'échec est NOMMÉ (relève au coffre : phrase = entrée lignee-D80, graine = entrée graine-ed25519-cartes) — la délégation à carte_m0.charger_secrets, cause racine de l'orpheline du jalon v7, est ÉTEINTE à la source (D144 appliqué au code, pas seulement au coffre). (2) `m5/conformite_profil.py` : la suite § 8.2 du jalon M5, 58 contrôles constatés depuis l'artefact — élément 1 : SIX sections décodables sans reste, descripteurs M5 (kernel32#2 GetCommandLineW + les trois hérités repris + terminateur), IAT/INT/hints M5, fixtures CLI/flux octet pour octet, héritage intact ; élément 2 : aucun call [rip] hors plages IAT, les SEPT secur32 ET GetCommandLineW visités ; élément 3 : 6 sections, DEP/NX+ASLR+HEV actifs, entrée 0x8C80 ; élément 4 : 3 DLL, kernel32 décrite DEUX fois (11 entrées), table HRESULTS totale ; élément 5 : les DEUX portes VIVANTES (R10 héritée 28 entrées, somme .text3 déclarée == recalculée ; PORTE M5 UNE entrée, somme .text4, le bloc d'entrée DANS la plage gardée) ; élément 6 : round-trip 100 %, R7 38 blocs octet-identiques, scellé 0.5.1 présent (fb41697d…) ; élément 7 : 36 352 o == layout, réserve .text4 int3, R_POLITIQUE à l'état image 0 ; contrôle de jalon : oracle D136 volume reduit (29 cas, falsification incluse). (3) `m5/build_m5.py` : la machinerie carte portée (fragments_clairs 52 blocs sur 6 artefacts, construire_carte, verrou_croise R8, tableau de bord, _anti_rollback, modes --sceller-rc/--sceller-final) + VERSION_RC1/VERSION_FINALE au plan. La garde sceau-I vérifie les arbres D'INTENTION — build_m5.py n'est PAS signé, le geste n'a cassé aucune signature (constaté : m5: vert 1869422e… avant ET après).

**La construction et la cristallisation.** `python3 m5/build_m5.py` : la chaîne entière re-vérifiée (héritage M3 524 + M4 492 verrous ; l'image M4 composée == le scellé 0.5.1 OCTET POUR OCTET ; round-trips 100 % ; oracle structurel M5 312 verrous ; oracles M4 560 + M5 365 cas verts, falsification détectée) PUIS la carte génération 7 NÉE : 4 fragments chiffrés sous la phrase lignée D80, signature Ed25519 de la GRAINE DURABLE (pub e9cd8c549485… — celle du coffre, D144), 52 blocs indexés sur 6 artefacts, verrou croisé R8 52 empreintes du premier coup, tableau de bord écrit — et proxy.exe ressort OCTET POUR OCTET identique (sha256 4b8f6af6…, recoupé contre le témoin pris AVANT le geste : le scellage est un fait de carte). Cristallisation R6 : le construire pose 1/10, puis NEUF passages --verifier aux graines distinctes 20261104…20261112 — chaque passage re-vérifie TOUT (oracles complets, R7, R8 52 empreintes) et incrémente : 52/52 blocs à 10/10, dix runs consignés au frag-prf (verdict-m4 et verdict-m5 datés à chaque run).

**Le scellage (--sceller-rc).** Garde sceau-I VERTE (6 arbres d'intention m0-m5, clé réelle) ; cristallisation 52 × 10/10 exigée puis constatée ; conformité § 8.2 exécutée PAR LE SCELLAGE lui-même : VERTE (58 contrôles PASS, oracle jalon 29 cas, graine datée) ; bascule `version=0.6.0-dev.1` → `version=0.6.0-rc.1` : UNE occurrence attendue, constatée, remplacée (fail-closed) ; fragments re-chiffrés, racine neuve, en-tête, signature Ed25519 (graine durable) ; VÉRIFICATION EN MÉMOIRE AVANT L'UNIQUE ÉCRITURE (listes blanches, signature, racine, bascule constatée au frag-bld re-déchiffré — modèle réparation D144) ; le tableau suit la balise ; verrou croisé post-scellage : 52 empreintes conformes, artefact 0.6.0-rc.1 ; empreinte de proxy.exe re-vérifiée == 4b8f6af6… (le scellage ne touche pas l'artefact).

**Post-vérifications (la preuve que le scellage tient).** P1 la carte est LISIBLE en lignée D80 : frag-bld version=0.6.0-rc.1, empreinte sha256:4b8f6af6…, signature Ed25519 valide (pub e9cd8c549485…), cristallisation 52/52 à 10/10, header génération 7 ; P2 LE VERROU ANTI-ROLLBACK EST VIVANT : `python3 m5/build_m5.py` REFUSE — « carte scellée (0.6.0-rc.1) : reconstruction interdite — procedure lourde R6 ou nouvelle version X.Y.Z+1 requise » ; P3 sceau verifier ONZE arbres VERTS après le geste (m5: vert 1869422e… — l'arbre d'intention signé par la cérémonie du développeur n'a pas bougé) ; P4 proxy.exe OCTET POUR OCTET == témoin pré-scellage (36 352 o). Écrits constatés par git status : m5/carte_m5.py, m5/conformite_profil.py, m5/conformite.txt, m5/carte/ (8 fichiers) NOUVEAUX ; m5/build_m5.py, m5/layout.py modifiés — ET RIEN D'AUTRE côté dépôt (.keys/ gitignoré ; cartes m0/m3/m4 intouchées ; m5/I/ aucun changement ; le bruit de bits de mode préexistant n'est pas commis).

**L'honnêteté des constats (deux contrôles corrigés EN COURS de geste, avant tout scellage).** La conformité est née de deux erreurs de constat, nommées et réparées par ses propres échecs : (a) le scellé 0.5.1 comparé au PRÉFIXE sha16 (l'égalité hexdigest == préfixe était toujours fausse — la comparaison se fait sur les 16 premiers caractères) ; (b) les indexes des tuples BLOCS_REVISIONS_M5 (rva/slot aux positions 2/3, pas 3/4 — le contrôle lisait le slot comme un rva) ; (c) le seuil des ombres ABI copié du M4 (≥ 6 imm8) décrivait l'artefact 0.5.0 : la trame tls-05:R2 passée à 0x98 (D140) vit en imm32 `48 81 EC`, le 0.6.0 — .text3 hérité byte-identique — porte CINQ imm8 + imm32, et .text4 porte SES cadres M5 (quatre imm8) : le contrôle constate MAINTENANT ces octets-là, seuils nommés.

**Frontières.** L'artefact 0.6.0-dev.1 sha256 4b8f6af6… OCTET POUR OCTET inchangé (le scellage est un fait de carte — l'u64 de l'artefact reste 0x00060000, les octets que le futur run jugera) ; les arbres scellés et le sceau INTOUCHÉS (onze verts avant/après, clé réelle jamais sollicitée) ; les cartes m0/m3/m4 INTACTES (la 0.5.1 de la réparation D144 n'a pas bougé) ; .keys/ gitignoré, aucun secret dans aucun écrit (les fragments sont chiffrés, la conformité ne cite que des empreintes) ; la finale 0.6.0 N'EST PAS posée (elle attend la validation terrain — le refus de la poser aujourd'hui est la décision la plus importante du geste) ; aucune suppression, aucune clé traversée.

**Vérifiabilité.** `python3 m5/build_m5.py --verifier` (refuse tant que la carte est scellée rc : P2 rejouable) ; `python3 m5/conformite_profil.py` (58 contrôles, m5/conformite.txt) ; `python3 v06/sceau_I.py verifier` (onze verts) ; la carte se lit par la lignée D80 (frag-bld version=0.6.0-rc.1) ; les graines de cristallisation 20261104…20261112 sont consignées au frag-prf avec les verdicts datés.

**SUITE.** Kit VM ÉTAPE 2 (le navigateur du bac à sable : mandataire 127.0.0.1:25000, page http://autorite.test/ sous --relever-https, décor parefeu-muet v8 verrouillé) ; run M5-b étape 2 — le critère (b) de D136 : la page servie ET la 502 « Certificat rejete » reçues PAR LE NAVIGATEUR, la ligne de flux aux preuves ; SI le run est vert : `python3 m5/build_m5.py --sceller-final` pose 0.6.0 avec la validation consignée (l'exigence est déjà écrite au code). D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-135) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 136" in texte:
    sys.exit("ECHEC : l'Entrée 136 existe déjà")
i135 = texte.find("## Entrée 135")
im = texte.find(MARQUEUR)
if not (0 <= i135 < im):
    sys.exit("ECHEC : ordre inattendu (135/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 135 < 136 < marqueur
j135 = nouveau.find("## Entrée 135")
j136 = nouveau.find("## Entrée 136")
jm = nouveau.find(MARQUEUR)
if not (0 <= j135 < j136 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 136 insérée ({len(ENTREE)} caractères) — ordre 135<136<marqueur recoupé")
