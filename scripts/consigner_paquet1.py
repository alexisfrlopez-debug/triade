#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_paquet1.py — LE PAQUET 1 DE LA VAGUE 3 CONSIGNÉ (l'instruction
6zqo2h60n exécutée) : la preuve indépendante TLA+/Apalache et le
raffinement property-based — Entrée 235 + D200 + worklog Task 141.
Append-only : les fins VÉRIFIÉES avant chaque écriture."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"


def append_verifie(chemin, fin_attendue, bloc, nom, marqueur):
    texte = chemin.read_text(encoding="utf-8")
    if texte.count(fin_attendue) != 1:
        sys.exit(f"[consigner] {nom} : fin attendue "
                 f"{texte.count(fin_attendue)} fois — append refusé")
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 f"dernière section — append refusé")
    if marqueur in texte:
        sys.exit(f"[consigner] {nom} : {marqueur} déjà présent — refusé")
    with chemin.open("a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} caractères)")


ENTREE_235 = """

## Entrée 235 — LE PAQUET 1 DE LA VAGUE 3 EXÉCUTÉ : LA PREUVE INDÉPENDANTE TLA+/APALACHE ET LE RAFFINEMENT PROPERTY-BASED (l'instruction 6zqo2h60n menée à terme) : l'invariant I1–I4 DÉCHARGÉ PAR SMT sur entiers non bornés, la fidélité D187 REPRODUITE EXACTEMENT par TLC (154 états), l'audit mécanique des 13 règles VERT, la campagne de 10 000 traces avec ses 660 écarts d'UNE classe consignés et réduits, le rejeu intégral STABLE — le statut « prouvé non borné » garde sa lettre et gagne sa preuve indépendante (12/11, la session de la vague 3, paquet 1/6)

**Le portage TLA+.** CF3.tla (sha256 946e68d4…) : les 13 règles règle à règle depuis modele_invariant_v150.py, l'époque typée Int NON bornée, l'invariant Inv = TypeOK ∧ I1–I4 ; les variantes CF3Plafond.tla (le plafond v120 e ← min(e+1, EpoquesMax) — UNIQUEMENT pour le contrôle de fidélité) et CF3Fidelite.tla (le compteur de profondeur prof < 6 + la clause VIEW qui déduplique par l'état abstrait — la convention même de l'explorateur D187).

**La fidélité.** TLC rejoue l'espace BORNÉ : CF3Fidelite (plafond + profondeur 6 + vue) trouve EXACTEMENT 154 états distincts — les comptes consignés D187 reproduits au nombre EXACT ; CF3Plafond (exploration complète) 216 états — le compte de l'explorateur Python complet ; CF3 bornes étendues (contrainte e ≤ 5, Inv + AucuneViolation) 360 états sans violation — le compte Python complet aux mêmes bornes. Trois conventions de bornes, trois accords. Les outils : tla2tools.jar (TLC v1.8.0, sha256 e1f11b75…) et Apalache 0.63.0 (tarball sha256 a756e96a… == le sha256sum.txt de la release amont) — ENVIRONNEMENT, pas artefacts (.gitignore, re-téléchargeables, empreintes consignées à outils_consignes.txt).

**Le déchargement (le cœur).** Apalache (SMT, Z3, entiers NON bornés) : le CAS DE BASE Init ⟹ Inv (NoError) ; LE PAS INDUCTIF Inv ∧ Next ⟹ Inv′ (NoError) — le prédicat d'initialisation ATTESTÉ Inv au journal (« Set the initialization predicate to Inv » — la config MCA_ind.cfg, après qu'une première tentative révélât que la clause SPECIFICATION d'un fichier de configuration ÉCRASE les drapeaux --init : le piège consigné, les configs refaites en INIT/NEXT explicites). Par induction : tout état atteignable satisfait Inv, TOUTE époque, TOUTE profondeur — P1–P4 prouvées non bornées désormais par preuve SMT indépendante, l'argument Python auto-vérifié de la v0.15.0 devenant le second témoignage.

**La non-vacuité (les contrôles négatifs — la leçon de l'instrument).** Un verdict NoError ne vaut que si l'outil ATTRAPE une violation : C1 — l'invariant AFFAIBLI (sans sait ⊆ Elements, l'univers étendu d'une chaîne étrangère) : contre-exemple PRODUIT (sait de cardinalité 3 → VoleKUser → cardinalité 4, I1 violé — la preuve que Cardinality est réellement raisonné par le SMT, pas ignoré) ; C2 — le prédicat faux dès l'état initial : ATTRAPÉ. La méthodologie validée, le NoError du déchargement est SIGNIFICATIF.

**L'audit mécanique des 13 règles** (audit_regles.py, rapport 6da55b00…) : l'époque n'est lue dans les gardes/actions QUE par le prédicat e > 1 (la classe ≥ 2 — la classe e = 1 n'est JAMAIS testée explicitement, c'est le complément) et le successeur e + 1 (l'écriture de la clôture, la seule) ; 7 règles figent l'époque (UNCHANGED), 3 n'y touchent pas, 2 la lisent par la garde, 1 l'écrit par le successeur — VERT des deux côtés (TLA+ ET Python par analyse syntaxique ast des fonctions actions_possibles/appliquer — pas des témoins par translation).

**Le raffinement property-based** (pbt_raffinement_v150.py, 1f5a407d… — le REMPLACEMENT du raffinement par scénarios exigé) : 10 000 traces à la graine consignée 20261112 (chaque trace tire de Random("GRAIN:i") — reproductible à l'identique), 3–8 pas par trace, les actions offertes selon la phase (le miroir exact de actions_possibles, pondérées vers le cycle honnête), les CHEMINS D'ÉCHEC inclus (la porte du piège AVANT la phrase — l'ordre de la sentinelle), la contre-vérification permanente à chaque pas (époque concrète == abstraite, phase/brouillon, PV, médias). Le harnais mémoïse le KDF déterministe (un Argon2 par coffre — la mémoïsation transparente : mêmes entrées, mêmes octets).

**Le résultat de la campagne.** 6 732 traces finies par longueur, 3 268 par destruction (le conteneur meurt) ; 660 ÉCARTS SUR 660 TRACES, UNE SEULE CLASSE : falsifie_conteneur pendant une SESSION (phase brouillon, piège intègre) — le MODÈLE refuse la règle (la garde exige le canonique), le CONCRET DÉTRUIT (la sentinelle court sur le canonique, pas sur le brouillon : destruction LOCALE + PV, le média INTACT). L'ANALYSE : un écart de COUVERTURE D'ÉTAT du modèle, pas une menace — la destruction concrète reste PROUVÉE (falsification cryptographique) et LOCALE (P3/P4 tenus) ; le raffinement par scénarios (34 pas) ne croisait jamais ce chemin, la randomisation le croise 660 fois. LE SHRINKING (ddmin glouton, TOUTES les traces à écarts) : 655/660 réduites à la séquence MINIMALE [ouvrir_correct, falsifie_conteneur] (2 pas), 2 à 3 pas, 3 à 4 pas. LE REJEU INTÉGRAL à graine identique : 10 000/10 000 condensats IDENTIQUES — pbt_traces.csv et pbt_traces_rejeu.csv BIT-IDENTIQUES (sha256 313b008ba791afad… l'un comme l'autre — la stabilité la plus forte qui soit). Rapport : pbt_raffinement_rapport.txt (4253d834…), généré des pièces par rapport_pbt.py (aucune valeur tapée).

**Le rejeu depuis un clone frais** (verifier_clone_frais.py, 54f4c414… ; rapport 7bab89e4…, 13/13 VERT) : git clone neuf (cb3968f), les outils copiés avec empreintes RECOUPÉES, les SEPT runs TLC/Apalache rejoués DEPUIS LE CLONE (verdicts IDENTIQUES, 8/8 — TLC 154/216/360), la campagne PBT du clone rejouée sur 200 traces aux mêmes indices de graine (200/200 condensats identiques au CSV committé), le modèle Python du clone re-exécuté : D187 REPRODUIT EXACTEMENT (154 états / 1 152 transitions). L'état committé REJOUE l'intégralité du paquet sans dépendre de la session.

**La table des statuts** (statuts_preuves_v150.py étendu, la table RÉGÉNÉRÉE depuis les pièces — l'exigence « uniquement depuis ces pièces ») : P1–P4 « proved unbounded » avec la preuve SMT citée ; la LIGNE NOUVELLE « Independent model proof (TLA+/SMT) — proved unbounded (SMT) » ; la ligne modèle↔implémentation devenue « witnessed (10,000 traces) » avec l'écart de couverture consigné ; les bornes croisées augmentées des accords TLC (154/216/360). Le PDF du manuscrit sera RECONSTRUIT au paquet 4 (la révision sollicitée par sollwnmae) — la table source est prête.

**Frontières.** Aucun artefact scellé touché (le garde sceau-I 14/14 VERT à l'ouverture ET à la clôture du paquet — loupe.exe c1115105…, proxy.exe 446279f3… INTACTS) ; le coffre réel JAMAIS ouvert (10 000 coffres de TEST à la phrase publique marquée D192, aucun conteneur réel lu) ; aucune mesure terrain exécutée ; aucun chiffre fabriqué — tout nombre de cette entrée est LU d'une pièce (verdicts.json, les rapports, les CSV) ; les consignations antérieures non réécrites (append-only).
"""

D200 = """

## D200 — LE STATUT NE CHANGE PAS SANS ARTEFACT, L'ARTEFACT EXISTE : l'invariant inductif I1–I4 (l'argument Python auto-vérifié de la v0.15.0, D198) DÉSORMAIS DÉCHARGÉ PAR PREUVE INDÉPENDANTE — le portage TLA+ (CF3.tla, 13 règles, époque Int non bornée), TLC la fidélité (les comptes D187 154 états reproduits EXACTEMENT sous plafond+profondeur+vue ; les espaces 216/360 CONCORDANTS avec l'explorateur Python), Apalache/SMT le déchargement (Init ⟹ Inv, Inv ∧ Next ⟹ Inv′, zéro contre-exemple sur entiers non bornés), les contrôles négatifs (l'invariant affaibli ATTRAPÉ : la non-vacuité prouvée, la leçon de l'instrument — un NoErreur ne vaut que si l'outil attrape), l'audit mécanique (l'époque lue par {e > 1, e + 1} SEULEMENT — l'uniformité structurelle de la classe ≥ 2 est un FAIT DE CODE audit mécaniquement) ; LE RAFFINEMENT PAR SCÉNARIOS REMPLACÉ par la campagne property-based (10 000 traces à graine consignée, chemins d'échec inclus, 660 écarts d'UNE classe — l'écart de couverture « falsification en session » consigné, réduit à la séquence minimale, P1–P4 non menacées ; le rejeu BIT-IDENTIQUE) ; LA RÈGLE CONSACRÉE : une affirmation de preuve porte ses artefacts rejouables (ici : le clone frais 13/13) — le statut « prouvé non borné » garde sa lettre et gagne sa preuve indépendante

**Le contexte.** L'instruction 6zqo2h60n (la vague 3) commande l'encodage TLA+, le déchargement Apalache, l'audit des gardes et le property-based — avec la clause : « Ne change le statut "prouvé non borné" qu'après existence des artefacts de preuve ». Les artefacts EXISTENT et rejouent : la clause est satisfaite par la PREUVE, pas par le renommage.

**Frontières.** Aucun artefact scellé touché (le garde 14/14 aux deux extrémités du paquet) ; le coffre réel jamais ouvert ; les outils (TLC, Apalache) sont l'ENVIRONNEMENT (empreintes consignées, exclus du dépôt, re-téléchargeables) — les PREUVES sont les artefacts ; les consignations antérieures non réécrites (append-only).
"""

TASK_141 = """

Task ID: 141
Agent: Z.ai (agent principal)
Task: LE PAQUET 1/6 DE LA VAGUE 3 (l'instruction 6zqo2h60n) — la preuve
indépendante TLA+/Apalache et le raffinement property-based, exécutés et
vérifiés au clone frais (D200, Entrée 235).

Work Log:
- LE PORTAGE : CF3.tla (13 règles, époque Int NON bornée, Inv = TypeOK ∧
  I1-I4) + CF3Plafond (le plafond v120 pour la fidélité) + CF3Fidelite
  (profondeur 6 + VIEW abstraite — la convention D187).
- TLC : 154 états EXACTS aux bornes D187 ; 216 (exploration complète du
  plafond) et 360 (e ≤ 5, Inv sans violation) — les DEUX concordants à
  l'explorateur Python aux mêmes conventions.
- APALACHE : base Init ⟹ Inv NoError ; PAS INDUCTIF Inv ∧ Next ⟹ Inv′
  NoError sur entiers NON bornés (init=Inv attesté au journal — le piège
  de la clause SPECIFICATION qui écrase --init découvert et corrigé en
  configs INIT/NEXT explicites).
- LES CONTRÔLES NÉGATIFS : l'invariant affaibli ATTRAPÉ (contre-exemple
  cardinalité 4 — Cardinality réellement raisonné) ; le faux dès
  l'initial ATTRAPÉ — la non-vacuité prouvée.
- L'AUDIT MÉCANIQUE : les 13 règles lisent l'époque uniquement par
  {e > 1, e + 1} — VERT TLA+ et Python (ast).
- LA CAMPAGNE PBT : 10 000 traces à graine 20261112, chemins d'échec
  inclus, contre-vérification permanente — 660 écarts d'UNE SEULE
  classe (falsifie_conteneur en session : le modèle refuse, le concret
  détruit — écart de couverture d'état, P1-P4 non menacées), shrinking
  ddmin : 655/660 réduites à [ouvrir_correct, falsifie_conteneur],
  rejeu 10 000/10 000 (les CSV bit-identiques).
- LE CLONE FRAIS : 13/13 VERT — les 7 runs rejoués du clone (verdicts
  identiques), 200 traces PBT du clone (200/200 identiques), D187
  154/1 152 reproduit du clone.
- LA TABLE DES STATUTS régénérée depuis les pièces (la ligne nouvelle
  « Independent model proof (TLA+/SMT) », la ligne modèle↔implémentation
  devenue witnessed 10,000 traces avec l'écart consigné).
- Frontières : garde 14/14 aux deux extrémités, coffre réel jamais
  ouvert (10 000 coffres de TEST D192), aucun chiffre fabriqué, les
  outils = environnement (empreintes consignées, hors dépôt).
- SUITE : le paquet 2/6 — la campagne de mutation étendue (n4kwcs3wa).
"""


def main() -> int:
    append_verifie(
        JOURNAL,
        "AUCUN chiffre fabriqué — ce qui n'est pas mesuré n'existe pas ; "
        "les consignations antérieures non réécrites (append-only).",
        ENTREE_235, "JOURNAL_TRAVAIL.md", "Entrée 235")
    append_verifie(
        DECISIONS,
        "le garde 14/14 VERT au geste ; les consignations antérieures "
        "NON réécrites (append-only).",
        D200, "DECISIONS.md", "## D200")
    append_verifie(
        WORKLOG,
        "- SUITE : l'exécution paquet par paquet, consignation à l'achèvement de\n"
        "  chacun, sync aux jalons.",
        TASK_141, "worklog.md", "Task ID: 141")
    print("[consigner] Entrée 235 + D200 + Task 141 : CONSIGNÉES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
