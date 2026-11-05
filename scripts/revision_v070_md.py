#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v070_md.py — LA RÉVISION v0.7.0 DU PROTOCOLE TRIADE (miroir de
revision_v061_md.py, modèle D133/D137) : la consolidation du programme
d'après M7 (D160). Chaque remplacement est ASSERTÉ (ancrage trouvé UNE fois
exactement) — un ancrage absent ou ambigu = ÉCHEC NOMMÉ, rien n'est écrit.

Douze remplacements/insertions :
  (1)  titre → v0.7.0 ;
  (2)  bloc d'en-tête : autorité v0.7.0, l'archive v0.6.1 ajoutée, la phrase
       de consolidation ;
  (3)  puce Version (l'état consolidé : M0–M8 franchis, M9 ouvert, sceau à
       treize arbres) ;
  (4)  puce Date → 5 novembre 2026 ;
  (5)  § 1.2 : la charge de validation du cœur natif porte M0 à M9 ;
  (6)  § 1.9 « Ce que change la v0.7.0 » NOUVEAU ;
  (7)  § 12 axe 3 : treize arbres + les cérémonies d'ère ;
  (8)  § 12.4 : TREIZE arbres + la discipline des cérémonies d'ère ;
  (9)  § 13.1 (table des cérémonies) : treize arbres VERTS ;
  (10) § 13.5 « Les cérémonies d'ère du sceau (5 novembre 2026) » NOUVEAU ;
  (11) § 18 : M7 franchi + les lignes M8 et M9 + le titre M0 à M9 ;
  (12) § 19.9 « Correspondance v0.6.1 → v0.7.0 » NOUVEAU + rejets ;
  (13) § 21 : la ligne v0.7.0 au journal des versions ;
  (14) § 21 : la clôture réécrite (la clause levée nommément).
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DOC = REPO / "docs" / "PROTOCOLE_TRIADE.md"

REMP = []


def remplace(ancrage, nouveau):
    REMP.append((ancrage, nouveau))


# ---------------------------------------------------------------- (1) titre
remplace(
    "# PROTOCOLE TRIADE v0.6.1 — Spécification technique",
    "# PROTOCOLE TRIADE v0.7.0 — Spécification technique",
)

# ------------------------------------------------- (2) bloc d'en-tête
remplace(
    "> Source de travail faisant autorité pour la v0.6.1. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.6.0_Specification.pdf` (v0.6.0),",
    "> Source de travail faisant autorité pour la v0.7.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.6.1_Specification.pdf` (v0.6.1),\n"
    "> `docs/Protocole_TRIADE_v0.6.0_Specification.pdf` (v0.6.0),",
)
remplace(
    "> D133 — complément opératoire : cérémonies, runbook, mode dégradé ; v1.1 : l'arbitrage\n"
    "> D137 du niveau de naissance y est aligné). Depuis la décision D17,\n"
    "> le PDF formel de la version courante est **régénéré systématiquement** à chaque\n"
    "> modification des sources du protocole : `scripts/build_pdf.sh` compare l'empreinte des\n"
    "> sources au stamp du dernier build et reconstruit avant chaque sauvegarde (`sync_backup.sh`).\n"
    "> La v0.6.1 consigne l'arbitrage du niveau de naissance d'un coffre neuf (D137) ; la",
    "> D137 — complément opératoire : cérémonies, runbook, mode dégradé ; v1.1 : l'arbitrage\n"
    "> D137 du niveau de naissance y est aligné). Depuis la décision D17,\n"
    "> le PDF formel de la version courante est **régénéré systématiquement** à chaque\n"
    "> modification des sources du protocole : `scripts/build_pdf.sh` compare l'empreinte des\n"
    "> sources au stamp du dernier build et reconstruit avant chaque sauvegarde (`sync_backup.sh`).\n"
    "> La v0.7.0 consolide le programme d'après M7 (D160) : le jalon M8 — le domaine `sys`,\n"
    "> les syscalls directs — est franchi (finale 0.9.0 scellée sur run terrain vert recoupé\n"
    "> 30/30), le jalon M9 — le domaine `tls13`, TLS 1.3 pur — est ouvert (couche I complète,\n"
    "> 28 spécifications), et le sceau de l'Intention porte treize arbres, ses cérémonies\n"
    "> d'ère (M8 puis M9) passées sur pièces (garde 13/13) ; la\n"
    "> v0.6.1 consigne l'arbitrage du niveau de naissance d'un coffre neuf (D137) ; la",
)

# ------------------------------------------------------------ (3) puce Version
remplace(
    "- Version : v0.6.1 — le niveau du coffre neuf (CF1/CF2/CF3) devient l'arbitrage du développeur à la création (D137) ; la v0.6.0 avait accompli la souveraineté cryptographique (D133)",
    "- Version : v0.7.0 — la consolidation du programme d'après M7 (D160) : le jalon M8 (syscalls directs — le domaine `sys`) est franchi, finale `0.9.0` scellée le 05/11/2026 sur run terrain vert recoupé 30/30 sur pièces croisées (Entrée 164, D165) ; le jalon M9 (TLS 1.3 pur en blocs scellés — le domaine `tls13`, l'ère 1.0.0) est ouvert (D166) : couche I complète — 28 spécifications en six familles, l'instrument 117 contrôles verts (D167) — et cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13, la dette D166 soldée) ; le sceau de l'Intention porte TREIZE arbres (cérémonies d'ère M8 : 12 arbres, D162/D163 ; M9 : 13 arbres, D168) ; la v0.6.1 avait consigné l'arbitrage du niveau du coffre neuf (D137) ; la v0.6.0 avait accompli la souveraineté cryptographique (D133)",
)

# --------------------------------------------------------------- (4) puce Date
remplace(
    "- Date : 31 octobre 2026",
    "- Date : 5 novembre 2026",
)

# ------------------------------------------------------------- (5) § 1.2 M0-M9
remplace(
    "restent des niveaux de preuve distincts : les\n"
    "jalons M0 à M7 demeurent la charge de validation du cœur natif.",
    "restent des niveaux de preuve distincts : les\n"
    "jalons M0 à M9 demeurent la charge de validation du cœur natif.",
)

# ------------------------------------------------------ (6) § 1.9 NOUVEAU
remplace(
    "justifie quand le secret la mérite. La chaîne de migration CF1 → CF2 → CF3 demeure\n"
    "disponible à tout moment pour un coffre dont les besoins grandissent ; le coffre réel\n"
    "de TRIADE reste CF3 (époque 1, checksum `0cc89a96`). Aucune autre règle n'est\n"
    "modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction\n"
    "objectif est inchangée.\n"
    "\n"
    "## 2. La couche I : format normalisé des spécifications",
    "justifie quand le secret la mérite. La chaîne de migration CF1 → CF2 → CF3 demeure\n"
    "disponible à tout moment pour un coffre dont les besoins grandissent ; le coffre réel\n"
    "de TRIADE reste CF3 (époque 1, checksum `0cc89a96`). Aucune autre règle n'est\n"
    "modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction\n"
    "objectif est inchangée.\n"
    "\n"
    "### 1.9 Ce que change la v0.7.0\n"
    "\n"
    "La révision de consolidation du programme d'après M7 (D160) : ce que la clôture de la\n"
    "v0.6.1 tenait « hors périmètre courant » entre dans la spécification, sur résultats\n"
    "mesurés — la clause est levée NOMMÉMENT pour les deux premières familles, les profils\n"
    "additionnels demeurent hors périmètre. Le **jalon M8** (le bloc optionnel de\n"
    "syscalls directs — le domaine `sys`) est franchi : la charte à huit règles (le SSN\n"
    "est une donnée, jamais un octet de code ; le motif du stub vérifié avant toute\n"
    "extraction ; un stub divergent est un refus nommé — le résolveur ne devine jamais,\n"
    "il ne s'adapte jamais en silence), les spécifications sys-01…03 écrites-avant-code,\n"
    "le harnais différentiel 61 contrôles verts sur fixtures ntdll synthétiques (le\n"
    "laboratoire ne connaît jamais le SSN du terrain), la cérémonie de l'ère passée avant\n"
    "le build (12 arbres, D162/D163), le run terrain sur le VRAI ntdll — la twin de la\n"
    "ligne hello-02 par les DEUX chemins (l'IAT kernel32 et le syscall direct\n"
    "NtWriteFile), le refus -4 nommé du stub crocheté — recoupé 30/30 sur pièces\n"
    "croisées, la finale `0.9.0` scellée (Entrée 164, D165 : le scellage exige le verdict\n"
    "du recoup comme pièce ; le scellage est un fait de carte, l'artefact ne bouge\n"
    "jamais). Le **jalon M9** (TLS 1.3 pur en blocs scellés — le domaine `tls13`, l'ère\n"
    "1.0.0) est ouvert (D166) : la couche I complète — 28 spécifications en six familles\n"
    "(sha, hkdf, x25519, aead, enregistrement, poignée, principal), l'instrument\n"
    "`verifier_specs_m9a.py` 117 contrôles verts (D167) — et la cérémonie de l'ère passée\n"
    "le 05/11 : la remise du développeur, TREIZE arbres signés hors ligne à la clé du\n"
    "04/11 (la continuité prouvée par le déterminisme Ed25519, D163 : les onze arbres\n"
    "inchangés rendent les signatures de l'ère M8), le garde repassé VERT 13/13 — la\n"
    "dette D166 soldée sur pièces. Le **sceau de l'Intention** porte désormais treize\n"
    "arbres (§ 12.4) et les cérémonies d'ère entrent au protocole (§ 13.5) : la dette se\n"
    "nomme à la naissance, jamais après coup (D166, règle 8) ; la charge se prépare au\n"
    "geste qui sert la main du développeur (D168). Aucune règle du cœur n'est modifiée ;\n"
    "aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction objectif\n"
    "est inchangée.\n"
    "\n"
    "## 2. La couche I : format normalisé des spécifications",
)

# ------------------------------------------------------------ (7) § 12 axe 3
remplace(
    "| 3 · Filigrane de l'Intention | D87 | chaque arbre de couche I condensé puis signé par la clé Ed25519 *hors-ligne* ; build et chemin de patch refusent une couche I non signée | **livré, prouvé terrain** — dix arbres signés, re-cérémonie réelle D126 |",
    "| 3 · Filigrane de l'Intention | D87 | chaque arbre de couche I condensé puis signé par la clé Ed25519 *hors-ligne* ; build et chemin de patch refusent une couche I non signée | **livré, prouvé terrain** — treize arbres signés ; re-cérémonie réelle D126, cérémonies d'ère M8 (12 arbres, D162/D163) et M9 (13 arbres, D166/D168) passées sur pièces, garde 13/13 |",
)

# ------------------------------------------------------------- (8) § 12.4
remplace(
    "Dix arbres de couche I vivent sous le sceau (les neuf lignées plus `v06/I` — la\n"
    "spécification du sceau est la première couche qu'il garde).",
    "Treize arbres de couche I vivent sous le sceau — les lignées m0 à m8 (le domaine\n"
    "`sys` depuis l'ère M8), l'arbre `tls13` (le domaine TLS 1.3 pur depuis l'ère M9),\n"
    "`demo`, `terrain`, et `v06/I` : la spécification du sceau est la première couche\n"
    "qu'il garde. Chaque ère qui ouvre un arbre nomme sa dette de cérémonie à la\n"
    "naissance (D166, règle 8) : le registre figé étendu et l'arbre neuf exigent la clé\n"
    "hors-ligne avant tout build — la charge se prépare au geste qui sert la main du\n"
    "développeur (D168), et la continuité de la clé se prouve par le déterminisme\n"
    "Ed25519 (D163) : re-signer les arbres inchangés redonne exactement les signatures\n"
    "déposées.",
)

# ------------------------------------------------------------- (9) § 13.1
remplace(
    "| Sceau de l'Intention (D87/D126) | `preparer` ; cérémonie hors-ligne `signer` (clé physique) ; `deposer` (vérifié avant écriture) ; `verifier` | dix arbres VERTS, code 0 ; commit poussé |",
    "| Sceau de l'Intention (D87/D126) | `preparer` ; cérémonie hors-ligne `signer` (clé physique) ; `deposer` (vérifié avant écriture) ; `verifier` | treize arbres VERTS, code 0 ; commit poussé |",
)

# ------------------------------------------------------------ (10) § 13.5
remplace(
    "git pull`.\n"
    "\n"
    "## 14. Coût en tokens : fragmentation, localisation, budgets",
    "git pull`.\n"
    "\n"
    "### 13.5 Les cérémonies d'ère du sceau de l'Intention (5 novembre 2026)\n"
    "\n"
    "Le sceau a traversé deux cérémonies d'ère en un jour, chacune née d'un garde qui\n"
    "refusait. **Ère M8** : l'ouverture du domaine `sys` avait étendu le registre figé m0\n"
    "et créé l'arbre m8 — le garde a nommé la dette AVANT tout build (D162 : un diff\n"
    "d'intention non signé ; la clé hors-ligne du développeur requise, le laboratoire ne\n"
    "signe jamais à sa place) ; le kit de cérémonie servi au dossier `/Cérémonie` du\n"
    "Drive (la remise, le LISEZMOI pas à pas, la règle d'or « JAMAIS generer »), la\n"
    "cérémonie passée sur pièces : douze arbres, les dix inchangés rendant les MÊMES\n"
    "signatures que celles du 04/11 (la preuve D163 de la réutilisation de la clé, sans\n"
    "jamais voir la clé privée), le garde repassé VERT 12/12 — puis le build 0.9.0-dev.1\n"
    "né, déterministe d'un poste à l'autre. **Ère M9** : la dette fut nommée À LA\n"
    "NAISSANCE (D166, règle 8) ; le geste des 24 spécifications ayant bougé l'arbre, la\n"
    "charge fut RÉGÉNÉRÉE au geste de la cérémonie (D168 : la charge de l'ouverture était\n"
    "périmée — une remise signée dessus aurait laissé l'arbre divergé APRÈS\n"
    "installation) ; le développeur signa hors ligne la remise de TREIZE arbres et\n"
    "déposa signatures-I.txt et cle-publique-I.txt au coffre `/test` ; le laboratoire\n"
    "rapatrie, recoupe — la clé déposée égale l'ancre `173fae9c…`, les ONZE arbres\n"
    "inchangés rendent les signatures de l'ère M8, m0 re-signé, tls13 arbre neuf, les\n"
    "empreintes vivantes égales la remise, chaque signature vérifiée Ed25519 — puis\n"
    "installe canoniquement (tout vérifié AVANT toute écriture) et le garde est repassé\n"
    "VERT 13/13, l'état « reelle » tenant. La règle qui en découle : la cérémonie d'ère\n"
    "n'est pas une formalité de documentation — c'est le geste qui rend le build de\n"
    "l'ère possible, et il suit le calendrier du garde, jamais l'inverse.\n"
    "\n"
    "## 14. Coût en tokens : fragmentation, localisation, budgets",
)

# -------------------------------------------------- (11) § 18 : M7 + M8 + M9
remplace(
    "## 18. Critères d'acceptation des jalons M0 à M7",
    "## 18. Critères d'acceptation des jalons M0 à M9",
)
remplace(
    "Huit jalons, chacun couvrant une capacité nouvelle",
    "Dix jalons, chacun couvrant une capacité nouvelle",
)
remplace(
    "| M7 | Portabilité inter-ISA | profil `riscv64-linux-elf64` : round-trip 100 % sur la nouvelle ISA ; patch à chaud conforme (scratch + `fence.i`) ; verrou croisé multi-profils ; export de continuité multi-profils vérifié | **ouvert** 04/11/2026, exécution DÉBLOQUÉE le 05/11/2026 (M6 franchi — Entrée 149 ; D149, fiche `docs/PROFIL_riscv64-linux-elf64.md`) |",
    "| M7 | Portabilité inter-ISA | profil `riscv64-linux-elf64` : round-trip 100 % sur la nouvelle ISA ; patch à chaud conforme (scratch + `fence.i`) ; verrou croisé multi-profils ; export de continuité multi-profils vérifié | **franchi** 05/11/2026 — balise `0.8.0` (Entrée 155 : run terrain M7-(d) vert sur pièces, recoup labo 29/29 sur pièces croisées, export multi-profils de bout en bout — l'universalité démontrée : win `0.6.0` / linux `0.7.0` / riscv `0.8.0`) |\n"
    "| M8 | Syscalls directs (domaine `sys`) | la charte à huit règles et les spécifications sys-01…03 écrites-avant-code ; le harnais différentiel sur fixtures ntdll synthétiques (le labo ne connaît jamais le SSN du terrain) ; le motif du stub vérifié avant toute extraction ; le run terrain sur le VRAI ntdll — la même observable par les DEUX chemins, les refus nommés ; la cérémonie de l'ère avant le build | **franchi** 05/11/2026 — balise `0.9.0` (Entrées 156–164, D160–D165 : harnais 61 verts ; cérémonie de l'ère passée 12/12 ; run terrain m8d VERT — 35 verts / 0 échec, la twin octet pour octet, le refus -4 du stub crocheté ; recoup labo 30/30 ; finale `0.9.0` scellée sur recoup exigé comme pièce) |\n"
    "| M9 | TLS 1.3 pur (domaine `tls13`) | la charte à huit règles et les 28 spécifications en six familles écrites-avant-code ; les primitives aux vecteurs officiels (FIPS 180-4, RFC 2104/4231, RFC 5869, RFC 7748, SP 800-38D) ; la poignée rejouée sur le transcript RFC 8448 ; le socle socket par syscalls directs (sys-04+) ; la cérémonie de l'ère avant construire() ; la session réelle avec un serveur réel — la ligne applicative chiffrée | **ouvert** 05/11/2026 (D166) — couche I complète (28 spécifications, l'instrument 117 verts, D167) ; cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13 — la dette soldée) ; chantiers (b) notation, (c) harnais RFC 8448, (d) socle socket, (e) build 1.0.0-dev.1, (f) terrain → finale `1.0.0` |",
)
remplace(
    "désormais le critère d'acceptation explicite.\n",
    "désormais le critère d'acceptation explicite. M8 et M9 sont les additions mesurées du\n"
    "programme d'après M7 (D160) : la fondation d'abord — le domaine `sys` est la\n"
    "condition d'une pile TLS 1.3 qui n'émettrait plus par l'IAT userland ; chaque\n"
    "famille s'appuie sur les résultats mesurés de la précédente.\n",
)

# ------------------------------------------------------ (12) § 19.9 NOUVEAU
remplace(
    "le besoin naît. Toucher au code des trois outils — rejeté : les trois actes de\n"
    "création existent et sont prouvés ; c'est le droit de choisir qui manquait, pas la\n"
    "mécanique.\n"
    "\n"
    "## 20. Glossaire",
    "le besoin naît. Toucher au code des trois outils — rejeté : les trois actes de\n"
    "création existent et sont prouvés ; c'est le droit de choisir qui manquait, pas la\n"
    "mécanique.\n"
    "\n"
    "### 19.9 Correspondance v0.6.1 → v0.7.0\n"
    "\n"
    "| Évolution | En v0.6.1 | En v0.7.0 | Statut |\n"
    "|---|---|---|---|\n"
    "| Programme d'après M7 | clause de clôture : syscalls directs et TLS 1.3 pur « hors périmètre courant » | le programme D160 entre en spécification : la clause est LEVÉE NOMMÉMENT pour les deux premières familles — le jalon M8 (domaine `sys`) franchi, le jalon M9 (domaine `tls13`) ouvert ; les profils additionnels demeurent hors périmètre | révisé (D160, D166) |\n"
    "| Sceau de l'Intention | dix arbres sous le sceau | treize arbres (m0–m8, tls13, demo, terrain, v06) ; les cérémonies d'ère entrent au protocole : la dette nommée à la naissance (D166 règle 8), la charge préparée au geste qui sert la main (D168), la continuité de clé prouvée par le déterminisme Ed25519 (D163) | étendu (D162, D166, D168) |\n"
    "| État des jalons | M0–M6 franchis, M7 ouvert | M0–M8 franchis (balises 0.2.0 à 0.9.0), M9 ouvert — la cérémonie de l'ère M9 passée (garde 13/13) | constaté (Entrées 155–168) |\n"
    "| Chaîne PDF | spec_v061 | chaîne spec_v070 ; l'archive v0.6.1 demeure (dernier build consigné : sha256 `4aac10f1…`, 984 555 o) | révisé (D169) |\n"
    "\n"
    "Modifications explicitement rejetées (v0.7.0) : réviser la spécification à chaque\n"
    "franchissement de jalon — rejeté : le versionnement suit les RÉVISIONS, jamais les\n"
    "franchissements (l'état des jalons vit aux sources de travail, régénérées à chaque\n"
    "geste ; la v0.7.0 consolide un PROGRAMME, pas un simple constat). Signer les\n"
    "sources `docs/` sous le sceau courant — rejeté : le modèle par-version demeure\n"
    "(`v06/I/README.md` § 1). Ouvrir les profils additionnels (`aarch64-macos-macho`,\n"
    "`wasm32-wasi`) dans la même révision — rejeté : chacun répétera M6/M7 sur\n"
    "résultats mesurés, hors périmètre. Fusionner les cérémonies d'ère dans la cérémonie\n"
    "CF3 — rejeté : trois gardes, trois menaces ; le sceau garde l'intention, le coffre\n"
    "garde les secrets.\n"
    "\n"
    "## 20. Glossaire",
)

# -------------------------------------------------- (13) § 21 ligne v0.7.0
remplace(
    "| v0.6.1 | 31 oct. 2026 | Révision de l'arbitrage de naissance du coffre (D137)",
    "| v0.7.0 | 5 nov. 2026 | Révision de consolidation du programme d'après M7 (D160) : le jalon M8 — le bloc optionnel de syscalls directs, le domaine `sys` — est franchi (charte à huit règles, spécifications écrites-avant-code, harnais 61 verts, cérémonie de l'ère passée 12 arbres, run terrain m8d vert sur le VRAI ntdll recoupé 30/30, finale `0.9.0` scellée — D160–D165) ; le jalon M9 — TLS 1.3 pur en blocs scellés, le domaine `tls13`, l'ère 1.0.0 — est ouvert (D166) : couche I complète (28 spécifications, six familles, instrument 117 verts — D167), cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13, la dette D166 soldée) ; le sceau de l'Intention porte treize arbres, les cérémonies d'ère entrent au protocole (§ 12.4, § 13.5) ; M7 franchi constaté (balise `0.8.0`, Entrée 155). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |\n"
    "| v0.6.1 | 31 oct. 2026 | Révision de l'arbitrage de naissance du coffre (D137)",
)

# ------------------------------------------------------- (14) § 21 clôture
remplace(
    "La présente version consigne l'arbitrage du niveau de naissance d'un coffre neuf\n"
    "(D137, § 12.5) et l'état au passage de relais : jalons M0 à M4 franchis sur\n"
    "validations terrain (balises finales 0.2.0 à 0.5.0), le programme de souveraineté\n"
    "cryptographique accompli (axes 2-3-4, D133) — le coffre réel a migré CF1 → CF2 → CF3\n"
    "les 30–31 octobre 2026 —, jalon M5 (outil complet) ouvert (D133) : empreintes par\n"
    "build, interception en VM isolée, patch à chaud du journal en production. Les évolutions prévisibles — bloc optionnel de syscalls directs,\n"
    "TLS 1.3 pur en blocs scellés, profils additionnels après M7 — restent volontairement hors\n"
    "du périmètre courant afin que chaque addition s'appuie sur des résultats mesurés. La règle",
    "La présente version consolide le programme d'après M7 (D160, § 1.9) et l'état au\n"
    "passage de relais : jalons M0 à M8 franchis sur validations terrain (balises\n"
    "finales 0.2.0 à 0.9.0), le programme de souveraineté cryptographique accompli\n"
    "(axes 2-3-4, D133) — le coffre réel a migré CF1 → CF2 → CF3 les 30–31 octobre\n"
    "2026 —, le sceau de l'Intention portant treize arbres signés, ses cérémonies d'ère\n"
    "passées sur pièces (garde 13/13) ; jalon M9 (TLS 1.3 pur) ouvert : sa couche I est\n"
    "complète et sa cérémonie d'ère passée — les chantiers de notation, de harnais, de\n"
    "socle socket et de build attendent. La clause « hors périmètre courant » est levée\n"
    "nommément pour les deux premières familles du programme D160 ; les profils\n"
    "additionnels après M7 restent volontairement hors du périmètre courant afin que\n"
    "chaque addition s'appuie sur des résultats mesurés. La règle",
)


def main() -> int:
    texte = DOC.read_text(encoding="utf-8")
    echecs = []
    for ancrage, nouveau in REMP:
        n = texte.count(ancrage)
        if n != 1:
            echecs.append(f"ancrage {n} fois (attendu 1) : {ancrage[:70]!r}…")
            continue
        texte = texte.replace(ancrage, nouveau)
    if echecs:
        print(f"[revision-v070] ÉCHEC — {len(echecs)} ancrage(s) fautif(s), RIEN n'est écrit :")
        for e in echecs:
            print(f"  ✗ {e}")
        return 1
    DOC.write_text(texte, encoding="utf-8")
    print(f"[revision-v070] v0.7.0 PASSÉE — {len(REMP)} remplacements assertés, "
          f"{len(texte.splitlines())} lignes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
