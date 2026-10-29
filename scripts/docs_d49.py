#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs_d49.py — D49 (DECISIONS) + Journal 38 (JOURNAL_TRAVAIL) + alignements
REPRISE/README/PLAN_MILESTONES pour la lignée terrain.2 (kit embarqué)."""
import os

ICI = "/home/z/my-project/triade"

D49 = """

### D49 — le kit embarqué : « 1 seul exe qui contient tout » (27/10/2026)

**Constat développeur** (27/10, après le run de livraison terrain.1) :
« fais moi 1 seul exe qui contient tout » + capture Defender —
« Trojan:Script/Wacatac.C!ml » niveau Grave sur le proxy.exe POSÉ dans le
dossier de test téléchargé. Deux exigences en une : la manipulation du kit
quatre-fichiers (superviseur.exe + demo.exe + proxy.exe + terrain_jetons.bin
à poser côte à côte) disparaît, et la fausse alerte antivirus reçoit une
réponse d'ingénierie, pas un contournement.

**Décision** : les trois artefacts du kit vivent EMBARQUÉS dans
superviseur.exe, section .blob lecture seule (RVA 0x8000) — demo.exe 0.3.0
(16 384 o, scellé M2, md5 73c064fb…), proxy.exe 0.4.0-dev.1 (19 456 o,
scellé M3, md5 8740e1ca…) et l'annexe de jetons D48 (248 o). Le nouveau
bloc sup-37 (entrée à mode ecx 0/1 : extraire/nettoyer, @0x6600, 984 o)
pose chaque artefact par CreateFileA CREATE_ALWAYS + boucle WriteFile
512 o DEPUIS l'embarqué (jamais de copie intégrale en mémoire —
TAMPON_CMD est trop petit, c'est le kernel qui copie), RELIT le fichier
posé octet par octet (ReadFile 512 o + memcmp scellée : la preuve vit sur
le disque), journalise lignes S04/S05 + md5 attendus (constantes du plan,
ASSERTÉES au build contre les scellés), et retire les trois fichiers après
T3 (mode 1 — le dossier ne garde que le journal). sup-09:R2 orchestre :
porte -> libc -> extraction -> T1 -> T2 -> T3 -> nettoyage -> verdict ; un
test sauté pour extraction impossible COMPTE ÉCHEC ; un T3 non applicable
(variante publique) n'est PAS compté. L'emplacement de l'annexe
(u64 longueur + 248 o, @0x10C10) est le SEUL octet mutable de l'image :
EXCLU de la table R10 (27 entrées + terminateur — la zone blob
en-tête+demo+proxy est couverte, l'intégrité du kit vit à la porte),
propriété de la VARIANTE. Deux variantes du MÊME code : publique
(dépôt — emplacement à zéro, T3 non applicable, jamais de secret committé)
et livraison (--jetons — annexe D48 intégrée, écart public/livraison
CONFINÉ à l'emplacement, asserté au build, livrée au dossier test
uniquement, terrain/livraison/ gitignoré).

**L'alerte Defender, réponse d'ingénierie** : Wacatac.C!ml est une
détection d'apprentissage (suffixe !ml) — un binaire sans éditeur, sans
ressources, sans signature, qui écoute un port et relaie des connexions :
c'est le métier légitime d'un proxy ET le portrait-robot d'un proxy
malveillant. Le fichier livré était byte-exact le scellé (md5 vérifiable,
notation auditable). Réponse : VERSIONINFO (FileDescription « TRIADE
superviseur terrain », version 0.5.0.2) + manifeste asInvoker en section
.rsrc (RVA 0x7000, RT_VERSION + RT_MANIFEST) — l'habillage légitime face
aux heuristiques ; les artefacts voyagent embarqués (plus de proxy.exe nu
posé à côté) ; l'exclusion antivirus reste un choix documenté côté
LISEZMOI (avec le md5 comme outil de confiance). Aucune signature
authenticode (pas de certificat — hors périmètre zéro-outil).

**Alternatives rejetées** : embarquer les jetons dans le binaire DU DÉPÔT
(la variante publique les exclut par construction — le dépôt reste
propre, D48 honoré) ; extraire vers %TEMP% (exécution depuis un dossier
caché = comportement de dropper, pire pour les heuristiques — on extrait
À CÔTÉ de l'exe, visible, et on nettoie) ; garder les fichiers posés
après le run (l'exigence dit UN exe — le dossier ne garde que le
journal) ; vérifier par md5 CALCULÉ au run (aucune crypto dans le
superviseur : le md5 affiché est la constante du plan prouvée au BUILD,
la preuve d'intégrité du run est la relecture octet à octet) ; étendre
sup-36 avec une écriture-depuis-pointeur (sup-36 .ecrire écrit depuis
TAMPON_COMPO <= 536 o — inutilisable pour 16 Ko, et toucher un bloc
terrain.1 eût sali le diff chirurgical) ; la double entrée fixe
.extraire/.nettoyage (aligner une étiquette interne à 0x6800 à la main :
fragile — le dispatch à mode vit à la première instruction) ; patcher
l'emplacement à la livraison (deux builds déterministes = même résultat,
zéro patch binaire, oracle vert sur les deux chemins).

**Développement** : entrée 38 du journal de travail.
"""

JOURNAL38 = """

## Journal 38 — D49 : le kit embarqué — « 1 seul exe qui contient tout » : demo.exe + proxy.exe + l'annexe de jetons vivent DANS superviseur.exe 0.5.0-terrain.2 (section .blob, extraction vérifiée par relecture octet à octet, nettoyage après run), la fausse alerte Defender du 27/10 reçoit sa réponse d'ingénierie (VERSIONINFO + manifeste asInvoker, md5 vérifiables, exclusion documentée) ; six défauts attrapés avant le build par la chaîne elle-même

Le développeur revient du terrain avec deux choses : une exigence —
« fais moi 1 seul exe qui contient tout » (le kit terrain.1 demandait
QUATRE fichiers posés à la main) — et une capture — Defender niveau Grave
sur proxy.exe (« Trojan:Script/Wacatac.C!ml ») dans le dossier de test
téléchargé. La réponse est une seule lignée : le kit EMBARQUÉ.

**Ce qui a été construit** (specs écrites-avant-code, la discipline
d'abord) : spec sup-37:R1 (extraction du kit embarqué — une entrée à
mode ecx 0/1 @0x6600, écriture ET relecture en morceaux de 512 o
depuis/vers l'embarqué, zéro fuite de handle, longueurs lues à l'en-tête
.blob jamais codées en dur, md5 attendus tracés comme constantes du
plan) ; spec sup-09:R2 (l'orchestration étendue : porte -> libc ->
EXTRACTION -> T1 -> T2 -> T3 -> NETTOYAGE -> verdict ; un test sauté pour
extraction impossible COMPTE ÉCHEC — jamais de TOUT OK usurpé ; un T3 non
applicable en variante publique n'est pas compté). Le plan : section
.blob (RVA 0x8000, en-tête longueurs + demo.exe + proxy.exe + emplacement
annexe 256 o), section .rsrc (RVA 0x7000, VERSIONINFO 0.5.0.2 +
manifeste asInvoker — l'habillage légitime), zone données sup 3
(0x6A00-0x6DFF, lignes S04-S07), six sections PE (en-têtes 568 o,
première section brute reculée à 0x400 — les RVA ne bougent pas), table
R10 à 27 entrées + terminateur (la zone blob couverte, l'emplacement
annexe EXCLU : seul octet mutable de l'image, propriété de la variante).
Deux variantes du même code : PUBLIQUE (dépôt, emplacement à zéro,
T3 non applicable — jamais de secret committé) et LIVRAISON (--jetons,
annexe D48 intégrée, écart confiné à l'emplacement, terrain/livraison/
gitignoré, interdit 11 honoré).

**La chaîne a fonctionné comme conçue** — six classes de défauts
attrapées AVANT le build, chacune par le maillon prévu pour elle :
(1) le structural a refusé la pile de sup-37 (dispatch avant prologue —
restructuration en prologue commun 0x40) ; (2) l'analyse d'alignement a
révélé un vrai bug latent : un cadre 0x20 eût laissé les args pile de
CreateFileA écraser les registres sauvés (0x40 imposé) ; (3) pefile a
rejeté le premier arbre .rsrc — les décalages d'ANNUAIRE sont relatifs à
la section, seuls les pointeurs de DONNÉE sont des RVA absolus ; (4)
l'extraction pefile a distingué clés d'octets vs de chaînes ; (5) la
preuve R7 a refusé les offsets fichier périmés (les artefacts scellés
gardent la convention M2, terrain.2 non — deux fonctions de tranche) ;
(6) l'oracle comportemental a vu le chemin composé « demo.exejetons.bin »
— le NUL fait partie du nom copié (contrat sup-36 P3, un inc rax).

**Résultat** : superviseur.exe 0.5.0-terrain.2, 61 952 o, 23 blocs (11
octet-identiques R7 aux scellés M0/M1/M2/démo, sup-09:R2, sup-37 nouveau),
oracle 10 102 cas verts (nominal x2 variantes : publique 4 lancements /
livraison 7 ; échecs étendus : annexe non posable, extraction impossible,
écart de relecture ; falsification 27/27 cibles dont la zone blob + 5
mutations), carte génération 5 re-scellée (23 empreintes, Ed25519),
cristallisation 10/10 (graines 11-21), audit_terrain2.py 53 contrôles
TOUT CONFORME (diff chirurgical : 21 blocs intacts, .rdata borné à
L00 + table R10, écart public/livraison confiné à 245 octets dans
l'emplacement, kit byte-exact les scellés). Publique : md5 4542ee20…,
sha256 4a139cc7…. Livraison : md5 45ca7292…, sha256 35fce4b7….
LISEZMOI-superviseur réécrit : UN fichier, procédure 2 clics, section
ANTIVIRUS complète (pourquoi la détection est une fausse alerte
vérifiable, comment exclure le dossier si besoin, les md5 de confiance).
"""

with open(os.path.join(ICI, "docs", "DECISIONS.md"), "a", encoding="utf-8") as f:
    f.write(D49)

with open(os.path.join(ICI, "docs", "JOURNAL_TRAVAIL.md"), "a", encoding="utf-8") as f:
    f.write(JOURNAL38)

# --- REPRISE : ligne d'état + §7.2 terrain -----------------------------------
p = os.path.join(ICI, "REPRISE_PROJET.md")
s = open(p, encoding="utf-8").read()
s = s.replace("superviseur.exe 0.5.0-terrain.1", "superviseur.exe 0.5.0-terrain.2")
s = s.replace("0.5.0-terrain.1 (kit 4 fichiers", "0.5.0-terrain.2 (kit embarqué 1 fichier, D49")
s = s.replace("terrain.1 (D48)", "terrain.2 (D48/D49)")
open(p, "w", encoding="utf-8").write(s)

# --- README racine : ligne terrain -------------------------------------------
p = os.path.join(ICI, "README.md")
s = open(p, encoding="utf-8").read()
s = s.replace("0.5.0-terrain.1", "0.5.0-terrain.2")
s = s.replace("TOUS les tests en 1 clic (kit 4 fichiers)", "TOUS les tests en 1 clic, 1 SEUL exe (kit embarqué, D49)")
open(p, "w", encoding="utf-8").write(s)

# --- PLAN_MILESTONES : ligne terrain -----------------------------------------
p = os.path.join(ICI, "docs", "PLAN_MILESTONES.md")
s = open(p, encoding="utf-8").read()
s = s.replace("terrain.1", "terrain.2")
open(p, "w", encoding="utf-8").write(s)

print("D49 + Journal 38 + REPRISE/README/PLAN alignés")
