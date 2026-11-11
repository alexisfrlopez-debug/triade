#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_paquet2.py — LE PAQUET 2 DE LA VAGUE 3 CONSIGNÉ (l'instruction
n4kwcs3wa exécutée) : la campagne de mutation étendue — Entrée 236 +
D201 + worklog Task 143. Append-only : les fins VÉRIFIÉES."""

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


ENTREE_236 = """

## Entrée 236 — LE PAQUET 2 DE LA VAGUE 3 EXÉCUTÉ : LA CAMPAGNE DE MUTATION ÉTENDUE (l'instruction n4kwcs3wa menée à terme) : 10 400 mutants sur les 52 blocs scellés (200 par bloc, la graine 20261112, QUATRE types dont multi-octets et substitutions sémantiques), les tueurs en ordre de coût K1→K4, les taux par domaine aux intervalles Clopper-Pearson exacts, les 737 survivants TOUS classés (chemins non couverts nommés), le rejeu à graine identique BIT-IDENTIQUE — la comparaison à v0.11.0/v0.14.0 citée, l'historique jamais remplacé (12/11, la session de la vague 3, paquet 2/6)

**La campagne** (mutation_vague3.py, b86083f8…). Les 52 blocs assemblés depuis les NOTATIONS (des copies de laboratoire — les pièces scellées JAMAIS touchées) ; 200 mutants par bloc, chaque mutant tiré de Random("20261112:bloc:index") — reproductible à l'identique, par mutant. LES QUATRE TYPES : A l'octet simple (l'héritage v0.11.0), B le multi-octets (2 à 4 octets CONSÉCUTIFS), C la substitution d'opérateur/condition À LONGUEUR CONSERVÉE (keystone : jz↔jnz, add↔sub, and↔or, shl↔shr, inc↔dec, test↔cmp, mov↔lea — splice seulement si la longueur tient exactement), D l'altération d'immédiat/déplacement (±1, bit inversé, complément).

**Les tueurs en ordre de coût** (jamais affaiblis) : K1 ROUND-TRIP 3 339 tués ; K2 STRUCTUREL 4 183 ; K3 DIFFÉRENTIEL (les harnais de famille aux vecteurs officiels croisés à hashlib/hmac, loupe-06 à md5) 1 112 ; K4 COMPOSITION (le rejeu v0.14.0 réutilisé TEL QUEL : la boucle winmain complète pour loupe, la poignée + l'enregistrement protégé pour l'orchestration tls13, le harnais sys autonome) 1 029. TOTAL : 9 663/10 400 tués (92,9 %).

**Les taux par domaine** (taux.csv, IC Clopper-Pearson 95 % exacts — scipy.stats.beta.ppf, la définition) : loupe 2 863/3 600 (79,5 %, IC95 [78,2 % ; 80,8 %]) — 737 vivants ; tls13 5 600/5 600 (100 %, IC95 [99,9 % ; 100 %]) ; sys 1 200/1 200 (100 %, IC95 [99,7 % ; 100 %]). LE TOTAL 92,9 %, IC95 [92,4 % ; 93,4 %].

**La classification des survivants** (survivants.csv, 67619374… — chaque survivant re-GÉNÉRÉ depuis sa graine puis classé, la re-génération ASSERTÉE identique au verdict). Les 737 vivants — tous dans loupe — portent CHACUN sa classe et sa pièce : CHEMIN NON COUVERT, le scénario nommé (la boucle winmain : l'ouverture, la cascade, la peinture, la saisie, le défilement, le curseur, la sauvegarde, la fermeture) et le contrôle manquant nommé (un vecteur qui exercerait la valeur/l'opération mutée). LA NOTE HONNÊTE sur les zéro équivalents : aucun mutant équivalent ne survit PAR CONSTRUCTION — K1 CANONICALISE l'encodage (capstone→keystone) : un mutant qui ne changerait QUE l'encodage meurt au round-trip car sa ré-assemblure canonique diverge ; tout survivant est NÉCESSAIREMENT une mutation sémantique non distinguée — un chemin non couvert, nommé.

**La comparaison historique** (rapport.txt, 80b821a5… — les pièces citées, jamais remplacées) : v0.11.0 (16 mutants/bloc, octet simple, K1-K3) loupe 79,9 %, tls13 88,6 %, sys 69,8 %, TOTAL 83,4 % ; v0.14.0 (le rejeu des 832 aux tueurs de composition) loupe 80,6 %, TOTAL 93,3 %. La campagne étendue (12,5× plus de mutants, quatre types visant la sémantique) CONFIRME le portrait : tls13 et sys à 100 %, loupe le domaine des survivants (79,5 % — dans l'intervalle de v0.14.0), la limite constatée et nommée : la couverture du scénario winmain sur les chemins rares.

**Le rejeu** (l'exigence « verdicts bit-identiques ») : toute la campagne re-jouée à graine identique — verdicts.csv et verdicts_rejeu.csv BIT-IDENTIQUES (sha256 c47ebe14c0e686… l'un comme l'autre, 10 400 lignes).

**Les lignes de tables régénérées par le générateur** (l'exigence) : extraire_donnees_v150.py étendu — QUATRE lignes nouvelles à la table des preuves (les trois domaines + le total, les IC cités, les sources preuves_v150/mutation_vague3/), les lignes historiques v0.11.0 INTACTES ; tables_generees.tex régénéré (38 lignes).

**Frontières.** Aucun artefact scellé touché (loupe.exe c1115105…, proxy.exe 446279f3…, demo.exe df8f2e50…, selftest.exe 8038585b… — sha256 recoupés APRÈS la campagne, INTACTS ; le garde sceau-I 14/14 VERT) ; les blocs mutés sont des COPIES DE LABORATOIRE assemblées depuis les notations ; aucun chiffre fabriqué — tout nombre est LU d'une pièce ; les consignations antérieures non réécrites (append-only).
"""

D201 = """

## D201 — LA CAMPAGNE DE MUTATION ÉTENDUE CONSACRÉE : 200 mutants par bloc (la graine 20261112, quatre types — l'octet simple hérité, le multi-octets, la substitution d'opérateur/condition à longueur conservée, l'altération d'immédiat/déplacement), les tueurs EN ORDRE DE COÛT jamais affaiblis (round-trip → structurel → différentiel → composition), 10 400 mutants sur les 52 blocs scellés en COPIES DE LABORATOIRE ; LE TAUX GLOBAL 92,9 % (IC Clopper-Pearson 95 % exact [92,4 % ; 93,4 %]) — loupe 79,5 %, tls13 et sys 100 % ; LES 737 SURVIVANTS TOUS CLASSÉS (chemin non couvert : le scénario et le contrôle manquant NOMMÉS — la classe « mutant équivalent » est VIDE PAR CONSTRUCTION : le round-trip canonicalise l'encodage, un mutant qui ne change que l'encodage meurt au K1) ; LE REJEU À GRAINE IDENTIQUE BIT-IDENTIQUE (les CSV des deux passages partagent le sha256) ; LA COMPARAISON À v0.11.0/v0.14.0 citée SANS remplacer l'historique ; LA RÈGLE : un survivant sans classification est une dette — ici chaque survivant porte sa classe, son scénario et son contrôle manquant

**Le contexte.** L'instruction n4kwcs3wa (la vague 3) étend la campagne v0.11.0 (832 mutants, un octet) d'un facteur 12,5 en VOLUME et en PROFONDEUR (les mutations sémantiques C/D visent les opérateurs et les constantes, pas seulement l'encodage). Le portrait v0.14.0 CONFIRMÉ : tls13 et sys intégralement tués, loupe le domaine de la limite — la couverture des chemins rares de l'interface.

**Frontières.** Aucun artefact scellé touché (sha256 recoupés avant/après, le garde 14/14) ; les copies de laboratoire assemblées depuis les notations ; les consignations antérieures non réécrites (append-only).
"""

TASK_143 = """

Task ID: 143
Agent: Z.ai (agent principal)
Task: LE PAQUET 2/6 DE LA VAGUE 3 (l'instruction n4kwcs3wa) — la campagne
de mutation étendue : 10 400 mutants, tueurs K1→K4, IC exacts, les 737
survivants classés, le rejeu bit-identique (D201, Entrée 236).

Work Log:
- LA CAMPAGNE : 52 blocs × 200 mutants, graine 20261112 (par mutant :
  Random("GRAIN:bloc:index")), quatre types A/B/C/D (multi-octets,
  substitutions jz↔jnz/add↔sub/… à longueur conservée, immédiats et
  déplacements).
- LES TUEURS : K1 3 339 · K2 4 183 · K3 1 112 · K4 1 029 (le rejeu
  v0.14.0 réutilisé tel quel) — TOTAL 9 663/10 400 (92,9 %).
- LES TAUX : loupe 79,5 % IC95 [78,2 ; 80,8] ; tls13 100 % ; sys 100 %
  (Clopper-Pearson exacts).
- LA CLASSIFICATION : 737 survivants (tous loupe) — CHEMIN NON COUVERT
  nommé (scénario + contrôle manquant) ; zéro équivalent PAR
  CONSTRUCTION (K1 canonicalise l'encodage — la note honnête).
- LE REJEU : verdicts.csv == verdicts_rejeu.csv BIT-IDENTIQUES
  (sha256 c47ebe14…).
- LA COMPARAISON : v0.11.0 83,4 % / v0.14.0 93,3 % cités, l'historique
  intact ; QUATRE lignes nouvelles à la table des preuves (le
  générateur extraire_donnees_v150 étendu, tables_generees.tex régénéré).
- Frontières : pièces scellées INTACTES (sha256 recoupés après :
  loupe.exe c1115105…, proxy.exe 446279f3…, demo.exe df8f2e50…,
  selftest.exe 8038585b…), copies de laboratoire uniquement, garde
  14/14, aucun chiffre fabriqué.
- SUITE : le paquet 3/6 — le reclassement des défauts Loupe
  (xboh1kljq).
"""


def main() -> int:
    append_verifie(
        JOURNAL,
        "tout nombre de cette entrée est LU d'une pièce (verdicts.json, "
        "les rapports, les CSV) ; les consignations antérieures non "
        "réécrites (append-only).",
        ENTREE_236, "JOURNAL_TRAVAIL.md", "Entrée 236")
    append_verifie(
        DECISIONS,
        "les PREUVES sont les artefacts ; les consignations antérieures "
        "non réécrites (append-only).",
        D201, "DECISIONS.md", "## D201")
    append_verifie(
        WORKLOG,
        "- SUITE : le paquet 2/6 — la campagne de mutation étendue "
        "(n4kwcs3wa).",
        TASK_143, "worklog.md", "Task ID: 143")
    print("[consigner] Entrée 236 + D201 + Task 143 : CONSIGNÉES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
