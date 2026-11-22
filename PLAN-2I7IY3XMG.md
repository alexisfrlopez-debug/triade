# PLAN GELÉ — 2I7IY3XMG (la vague 15)
> L'atelier du corpus d'entraînement : construire le dataset depuis les journaux
> append-only et les campagnes, en triples (contrat, fragment, notation, verdict,
> classe de refus, diff) JSONL — SANS inventer une seule donnée.
> Gelé AVANT toute extraction ; l'empreinte du plan précède la première ligne.

## Le mandat
(1) **L'EXTRACTION MÉCANIQUE** (jamais retapée) depuis journal_v4.jsonl,
garde-brut, garde-prompts, resultats, les diffs chirurgicaux ; les splits
TRAIN/DEV/TEST étanches — le TEST ne porte AUCUNE notation dorée (seulement
juges + canari + endpoint) ; LE CANARI unique embarqué dans TRAIN ; LA SONDE DE
CONTAMINATION (dérivation 128 constantes + canari + overlap n-gram) livrée.
(2) **LA PORTE DE SCRUB fail-closed** (équivalent Python gitleaks — LE CONTRÔLE
NÉGATIF : un secret planté DOIT être attrapé) ; lab-copy-only à phrases de test
visiblement marquées (D105) ; les cibles bénignes only (binaires intercepteurs,
dual-use exclus) ; le sous-ensemble permissif Apache-2.0/CC-BY (tâches
synthétiques, définitions math, vecteurs FIPS/RFC, grammaire) séparé du BSL.
(3) **LA DATASET CARD** (provenance par ID de décision, licence, splits, canari,
gaps nommés, dual-use) + LE MANIFESTE (commit, sha256 par fichier, vecteur de
versions, empreintes des juges, graines, canari) ; la cristallisation 10
rebuilds bit-identiques ; le dépôt Zenodo/HF DEMEURE le geste du développeur.

## Les gestes
1. Le plan gelé ; l'extracteur mécanique (les sources nominatives, la graine
   consignée).
2. Les splits + le canari + la sonde de contamination.
3. La porte de scrub + le contrôle négatif vécu + la séparation permissif/BSL.
4. La dataset card + le manifeste + la cristallisation 10×.

## La vérification après modifications
Contrôles négatifs VÉCUS (secret planté attrapé, canari présent et unique,
AUCUNE dorée dans le split TEST, empreintes des juges conformes) ; archive
déterministe 10× ; extraction re-jouée à graine identique bit-identique ; aucun
coffre réel ni phrase réelle touchés ; entrée append-only au journal.

## Les refus
Jamais une donnée inventée ; jamais une dorée au TEST ; jamais un secret passé ;
jamais le dual-use inclus ; jamais le dépôt minté sans commande.
