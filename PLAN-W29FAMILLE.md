# PLAN GELÉ — W29FAMILLE (la seconde famille + le canari de fidélité continu)

> Vague 29, prompt 6 (dépôt du 27/11/2026, instructions.txt §10 Prompt 6 — suggestions
> C10/C11 de l'évaluation). L'écart FAMILY-ABSENT est nommé (seule API : famille GLM ;
> voie locale 1.5B à 0/64). Le présent plan gèle l'atelier AVANT toute mesure.

## Geste
1. LE MODÈLE OUVERT CAPABLE CHOISI (identifiant ET empreinte consignés au choix) :
   **Qwen2.5-Coder-7B-Instruct** (Qwen/Qwen2.5-Coder-7B-Instruct) — la classe 7–14B
   coder, une famille DISTINCTE de GLM (Qwen ≠ GLM : la seconde famille nommée au
   plan). L'empreinte consignée : celle du `tokenizer.json` + `config.json`
   téléchargés au présent atelier (les octets mêmes, sha256). LA LIMITE STRUCTURELLE
   DU BAC NOMMÉE : 4 Gio de RAM / 2 vCPU / aucun GPU — le run appartient au poste
   réel (le geste compute du développeur) ; AU BAC : aucune confrontation de la
   seconde famille n'est mesurée (FAMILY-ABSENT ne devient VERT que sur pièces).
2. LA CONFRONTATION TRIPARTITE (le kit livré, le run au poste réel) : spec ↔ seconde
   famille ↔ définitions mathématiques sur les 128 constantes MD5 T[64] (la table
   RFC 1321 — la dérivation aux décimales de |sin(i)|) et SHA-256 K[64] (RFC 6324 —
   les racines cubiques entières, la partie fractionnaire exacte en confirmation).
   AU BAC : LE VOLET MATHÉMATIQUE VÉCU — les 128 constantes des cinq pièces
   recalculées depuis les définitions (Python décimal à précision étendue, la
   dérivation aux décimales pour MD5, la racine cubique entière pour SHA-256) et
   confrontées aux constantes du domaine (loupe-06-md5 MD5_T, tls13 K[64]) — le
   critère de divergence pré-enregistré : ZÉRO écart attendu, tout écart nommé avec
   sa pièce. LA SPEC ET LES DÉFINITIONS d'accord : le volet vérifiable au bac.
3. L'ÉCHANTILLON PRÉ-ENREGISTRÉ de notations (≥ 6 blocs, mêmes contrats, juge
   inchangé) : loupe-06-md5, loupe-05-sha256, tls13-16-aes128-bloc, b20004, c30010,
   g70003 (la graine 20261128 consignée AVANT tirage — l'ordre canonique du corpus,
   jamais re-tiré). Les contrats de contexte recoupés (les empreintes au manifeste).
4. LE CANARI DE FIDÉLITÉ CONTINU : à CHAQUE appel de campagne, une violation ordonnée
   (op hors enum, offset hors bornes) qui DOIT être refusée au décodage ; un serving
   qui l'accepte en cours de session INVALIDE LA SESSION (fail-closed, refus nommé
   **SERVING-INFIDELE**) — le gate de sélection devient un garde continu. AU BAC :
   le canari ÉPROUVÉ sur le bord GLM (le seul disponible — le verdict consigné tel
   quel : le bord accepte sans appliquer, la session du bord serait INVALIDÉE) ; le
   canari câblé au harnais de la campagne future (le fichier du canari, sa
   violation, son verdict attendu — le kit complet livré).
5. LE JUGE inchangé (expandeur_add.py 9fc325e2… INTACT) ; les splits scellés du
   corpus recoupés INTACTS (les deux fichiers auxiliaires divergents re-consignés au
   registre des écarts, jamais masqués).

## Critères d'acceptation
- Le rejeu bit-identique des confrontations vécues au bac (le volet mathématique,
  le canari sur le bord) ; les recoupes d'empreintes du juge et du corpus VERTES.
- Le canari vérifié à chaque évaluation (la sonde du bord GLM rejouée) ; le sceau-I
  14/14 avant et après ; la porte 32 classes zéro rouge.
- Les verdicts publiés TELS QUELS : FAMILY-ABSENT ne devient VERT que sur pièces —
  la limite du bac nommée sans maquillage ; AUCUN chiffre fabriqué.
