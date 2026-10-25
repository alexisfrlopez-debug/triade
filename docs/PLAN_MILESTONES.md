# FEUILLE DE ROUTE — Jalons M0 à M5

> La feuille de route décompose la validation du protocole en six jalons, chacun couvrant
> une capacité nouvelle et se terminant par des critères de sortie mesurables. Aucun jalon
> n'est franchi sans que la carte soit signée, le verrou croisé vérifié et l'oracle passé :
> la discipline protocolaire s'applique dès le premier octet.

L'application cible — un outil de pentest de type intercepteur MITM pour Windows 11 — est
choisie comme stress test : elle exige du réseau, de la concurrence, du parsing d'entrées
non fiables et du chiffrement, soit un large éventail de blocs aux contrats très différents.
Son usage est encadré : tests autorisés en environnement de laboratoire, machine virtuelle
isolée, autorité de certification de test installée localement.

## Vue d'ensemble

| Jalon | Objectif | Livrables | Critères de sortie |
|---|---|---|---|
| M0 | Prouver la chaîne artefact | Éditeur PE32+ minimal ; hello.exe via WriteFile ; carte v0 à trois blocs ; vérificateur de round-trip | Exécution sur Windows 11 ; round-trip 100 % ; carte signée et vérifiée ; moins de 4 Kio. Règles : R1–R3, R8–R9 |
| M1 | Blocs réutilisables | Mini-libc scellée : memcpy, memcmp, strlen, itoa, allocateur par zone | Oracle à 100 % ; première cristallisation ; adresses stables démontrées. Règles : R5–R7 |
| M2 | Code actif et patch à chaud | Serveur TCP écho ; thread par connexion ; journal console | Patch du bloc écho pendant exécution, sans interruption ; rollback démontré. Boucle complète |
| M3 | Entrées non fiables | Proxy HTTP ; parseur à contrats renforcés ; threading du tunnel | Un million de requêtes fuzzées sans crash ; proxy transparent pour curl. Contrats renforcés |
| M4 | Tunnel chiffré | Contexte SSPI / Schannel ; poignée de main TLS ; relais chiffré | HTTPS en transit ; échec propre sur certificat invalide. Contrats cryptographiques |
| M5 | L'outil complet | Autorité de test locale ; interception et re-chiffrement ; journal des flux ; interface en ligne de commande | Interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build activées. Intégralité du protocole |

## Jalons charnières

**M0 est le jalon existentiel.** Il prouve que la chaîne notation, octets, exécutable,
exécution fonctionne de bout en bout sans compilateur, et que la carte rend le résultat
vérifiable — s'il échoue, le paradigme entier est remis en question avant tout
investissement supplémentaire. Livrables détaillés : éditeur PE32+ minimal (écriture des
en-têtes DOS/COFF/PE32+ et des sections `.text`/`.rdata` par le script de build),
hello.exe affiché via WriteFile, carte v0 décrivant les trois blocs initiaux, et le
vérificateur de round-trip keystone/capstone. Critères : exécution constatée sur
Windows 11, fidélité de round-trip à 100 %, carte signée Ed25519 et verrou croisé vérifié,
exécutable de moins de 4 Kio.

**M2 est le jalon de vérité du protocole.** Le patch à chaud sur code en cours d'exécution
est la capacité qui a motivé l'architecture de balises depuis la première discussion. Sa
démonstration — bascule atomique par trampoline de 12 à 16 octets, continuité de service,
rollback copy-on-write — valide que l'investissement dans la carte et le verrou croisé
paie concrètement. Scénario de sortie : remplacer le bloc d'écho du serveur TCP pendant
qu'il traite des connexions, sans interruption de service.

Les jalons suivants (M3 à M5) étendent le périmètre fonctionnel sans ajouter de mécanisme
protocolaire nouveau : ils éprouvent les mêmes règles sur des contrats de plus en plus
exigeants — parsing d'entrées non fiables (M3), contrats cryptographiques (M4), intégration
complète de l'outil avec interception TLS, journalisation et traçage par build (M5).

## Indicateurs de santé transverses

Mesurés à chaque jalon, ils valident que l'économie promise par le protocole est réellement
délivrée :

| Indicateur | Cible | Premier mesuré |
|---|---|---|
| Précision de localisation (bon bloc identifié du premier coup) | 95 % | M0 |
| Coût moyen d'une édition simple | 5 000 tokens | M1 |
| Taux de régression post-patch (rollback exclus) | zéro | M2 |
| Corruptions détectées par l'oracle | toutes, zéro silence | chaque jalon |
| Échecs de verrou croisé non bloquants | zéro (fail-closed strict) | chaque jalon |

## Rappels protocolaires par jalon

- M0 : règles R1–R3 (jamais de binaire nu, intention d'abord, balisage) et R8–R9 (verrou
  croisé, carte signée) dès le premier octet.
- M1 : règles R5–R7 (vérifie-puis-écrit, cristallisation, adresses stables) — la
  mini-libc est le premier terrain de cristallisation.
- M2 : boucle complète, patch à chaud et rollback démontrés.
- M3 : contrats renforcés sur entrées non fiables — fuzzing systématique.
- M4 : contrats cryptographiques — échec propre sur certificat invalide.
- M5 : intégralité du protocole, empreintes par build activées, interception en VM isolée.

Après M5 : extension RISC-V comme validation de la portabilité du protocole, bloc
optionnel de syscalls directs, TLS 1.3 pur en blocs scellés — volontairement hors
périmètre courant afin que chaque addition s'appuie sur des résultats mesurés.
