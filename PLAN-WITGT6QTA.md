# PLAN GELÉ — WITGT6QTA (la vague 15)
> L'atelier feedback : livrer l'outil `triade feedback` + le schéma
> TRIADE-FEEDBACK-v1 gelé par empreinte AVANT tout rapport, conforme
> D105/R10/D122.
> Gelé AVANT tout rapport ; l'empreinte du schéma précède la première génération.

## Le mandat
(1) **LE SCHÉMA PRÉ-ENREGISTRÉ** (sha256 consignée) : kit/contract/manifest,
agent (family, identifier_as_exposed, checkpoint not_exposed si inconnu), env,
capability (128 constantes + smoke), measured (opérations aux refus par classe +
tokens natifs des logs + wall ; défauts F/L locus kit|piece + evidence_sha256 ;
régime/mémo/audit), commentary optionnel ≤500 tokens marqué non vérifié,
consent (public_digest, licence CC-BY-4.0), signature adopteur optionnelle
(jamais l'ancre du projet).
(2) **LA PART MEASURED EXTRAITE MÉCANIQUEMENT** du journal de session déjà
consigné (jamais retapée, coût token marginal ≈0) ; commentary est la seule part
budgétée ; LES PORTES fail-closed : champ requis manquant → refus nommé ; secret
détecté → refus ; chemins/usernames anonymisés.
(3) **LA SORTIE** : report-<date>-<kitver>.json + le gabarit d'issue GitHub
pré-rempli ; JAMAIS d'envoi automatique (le geste humain D122) ; aucune
dépendance réseau au build (R10) ; la consigne agent dans DOC-FEEDBACK (lancer à
la fin de session, relire, envoyer si consenti).

## Les gestes
1. Le plan gelé ; le schéma TRIADE-FEEDBACK-v1 + son empreinte consignée.
2. L'outil `triade feedback` (l'extraction mécanique depuis le journal, les
   portes fail-closed, l'anonymisation).
3. Le gabarit d'issue GitHub + DOC-FEEDBACK.
4. Les contrôles négatifs VÉCUS (une phrase de test marquée plantée dans un
   faux journal DOIT être attrapée et le rapport refusé ; un champ requis
   retiré DOIT être refusé).

## La vérification après modifications
Contrôles négatifs vécus ; validation de schéma sur un rapport d'exemple à zéro
secret ; coût token marginal de la part measured mesuré (≈0) ; anonymat vérifié ;
offline (aucun appel réseau à la génération) ; entrée append-only.

## Les refus
Jamais un envoi automatique ; jamais un secret dans un rapport ; jamais la part
measured retapée ; jamais l'ancre du projet embarquée.
