# FEUILLE DE ROUTE — Jalons M0 à M7

> La feuille de route décompose la validation du protocole en huit jalons, chacun couvrant
> une capacité nouvelle et se terminant par des critères de sortie mesurables. Aucun jalon
> n'est franchi sans que la carte soit signée, le verrou croisé vérifié et l'oracle passé :
> la discipline protocolaire s'applique dès le premier octet. Les jalons M0-M5 s'exécutent
> sur le profil primaire `x86-64-win11-pe` ; M6 et M7, ajoutés par la v0.3, valident
> l'universalité (D14). Mis à jour pour la v0.4.0 : conditions transverses d'acceptation
> (oracle vert, suite de conformité, tableau de bord conforme — spécification § 16) et
> critères de parité inter-profils (spécification § 8.3).
>
> **État : M0 franchi le 26 octobre 2026** (D26 amendée — validation terrain Windows 11
> constatée). **Jalon M1 franchi le 26 octobre 2026** (D32 — validation terrain
> Windows 11 constatée : ligne unique `TRIADE M1 : minilibc 21/21 OK`, contrat
> libc-08 Q2 ; balise finale **`0.2.0`** scellée, immuable § 9). **M2 à la balise
> 0.3.0-rc.1** (boucle § 5 démontrée, conformité 124/124 ; constat terrain PARTIEL
> du 26/10 : bannière exacte et porte R10 vivantes sous Windows 11 — le scellement
> final attend la démonstration écho + console). En parallèle (D34, anticipation
> restreinte) : échelle d'auto-hébergement — échelon 1 franchi (hachoir, `m6/`),
> échelon 2 phase 1 scellée (sceau SHA-512 natif, `m7/` — emprunt de nommage,
> les jalons M6/M7 du plan restent inchangés).

L'application cible — un outil de pentest de type intercepteur MITM pour Windows 11 — est
choisie comme stress test : elle exige du réseau, de la concurrence, du parsing d'entrées
non fiables et du chiffrement, soit un large éventail de blocs aux contrats très différents.
Son usage est encadré : tests autorisés en environnement de laboratoire, machine virtuelle
isolée, autorité de certification de test installée localement.

## Vue d'ensemble

| Jalon | Objectif | Livrables | Critères de sortie |
|---|---|---|---|
| M0 | Prouver la chaîne artefact | Éditeur PE32+ minimal ; hello.exe via WriteFile ; carte v0 à trois blocs ; vérificateur de round-trip | Exécution sur Windows 11 ; round-trip 100 % ; carte signée et vérifiée ; moins de 4 Kio. Règles : R1–R3, R8–R9. **Franchi le 26/10/2026** |
| M1 | Blocs réutilisables | Mini-libc scellée : memcpy, memcmp, strlen, itoa, allocateur par zone, memset ; **instrumentation des budgets tokens** ; suite de conformité § 8.2 ; export de continuité D16 | Oracle à 100 % ; première cristallisation ; adresses stables démontrées ; première mesure effective des budgets (localiser/éditer/ajouter). Règles : R5–R7. **Franchi le 26/10/2026 — balise finale `0.2.0` (D32)** |
| M2 | Code actif et patch à chaud | Serveur TCP écho ; thread par connexion ; journal console | Patch du bloc écho pendant exécution, sans interruption ; rollback démontré. Boucle complète |
| M3 | Entrées non fiables | Proxy HTTP ; parseur à contrats renforcés ; threading du tunnel | Un million de requêtes fuzzées sans crash ; proxy transparent pour curl. Contrats renforcés. **Ouvert le 27/10/2026 (D45) — harnais P1-P5 livré et falsifiable, 101 000 cas sans crash sur la surface scellée ; couche I écrite-avant-code : 13 spécifications http-xx + tcp-13 (D46) ; étape (b) accomplie (D47) : proxy.exe scellé 0.4.0-dev.1 — oracle à scénarios 153 036 cas verts, carte génération 5 (38 blocs, 4 artefacts), révisions http-06:R2/http-10:R2 nées de l'implémentation ; étape (c) confiée au superviseur terrain (D48 : T2 traverse le proxy par curl) ; étape (c) validée terrain 6× (T2 du superviseur, D71) ; étape (d) ACCOMPLIE (D72 : campagne million — harnais fuzz_million.py falsifiable, 1 000 000 cas SANS CRASH en 175 s sur http-01..09 + accumulation http-10, re-exécution graine neuve identique ; rapport m3/rapport_million.json) ; reste : fuzzing dans la conformité (e), puis cristallisation + scellage final 0.4.0** |
| terrain/ (hors jalons) | Harnais du terrain (D48) | Superviseur GUI 1 clic : T1 démo + T2 proxy + T3 envoi Drive | **superviseur.exe 0.5.0-terrain.3 scellé (27/10/2026, D50) — 23 blocs dont 11 octet-identiques R7, kit embarqué « 1 seul exe » (D49), oracle 10 102 cas verts, carte génération 5, cristallisation 10/10, audit 61 contrôles ; terrain.2 ne lançait rien (SizeOfHeaders incohérent à six sections — chargeur refusait l'image) : corrigé d'un octet, règle chargeur imposée build+oracle+audit ; run 16 (D71, 28/10 06:54) : T3 démontré de bout en bout PREMIÈRE FOIS — journal terrain_20261028_065408.txt déposé TOUT SEUL dans le dossier test (chaîne de garde fermée, md5 superviseur == LISEZMOI) ; T2 6e vert consécutif ; T1 inchangé D57 (WER attendu)** |
| M4 | Tunnel chiffré | Contexte SSPI / Schannel ; poignée de main TLS ; relais chiffré | HTTPS en transit ; échec propre sur certificat invalide. Contrats cryptographiques |
| M5 | L'outil complet | Autorité de test locale ; interception et re-chiffrement ; journal des flux ; interface en ligne de commande | Interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build activées. Intégralité du protocole |
| M6 | Portabilité inter-OS | Profil `x86-64-linux-elf64` complet : même couche I réutilisée sans modification ; mini-libc re-scellée pour le profil ; hello et serveur écho sur Linux ; **suite de conformité du profil** | **Suite de conformité verte (§ 8.2)** ; diff nul sur la couche I ; carte multi-profils signée et vérifiée ; le même oracle passe sur les deux profils ; **parité inter-profils vérifiée (§ 8.3)** |
| M7 | Portabilité inter-ISA | Profil `riscv64-linux-elf64` : blocs re-générés pour une ISA à instructions de taille fixe ; patch à chaud adapté (registre scratch + `fence.i`) ; **suite de conformité du profil** | Round-trip 100 % sur la nouvelle ISA ; **suite de conformité verte** ; patch à chaud conforme au profil ; verrou croisé multi-profils ; **parité inter-profils vérifiée** ; export de continuité multi-profils vérifié |

## Conditions transverses d'acceptation (v0.4.0)

Ajoutées par la v0.4.0 (spécification § 16), elles s'appliquent à **chaque** jalon, en sus
des critères propres :

1. **Oracle vert** — 100 % des tests différentiels de la couche I concernée (R5).
2. **Suite de conformité verte** pour les éléments du profil couverts par le jalon (§ 8.2).
3. **Tableau de bord conforme** (§ 15.2) — aucune métrique au rouge, les métriques « cible »
   explicitement annotées comme telles tant que l'outillage n'est pas déployé (budgets
   tokens : première mesure effective à M1).
4. **Carte signée, verrou croisé vérifié** — inchangé depuis la v0.1 : dès le premier octet.
5. **Journal à jour** — décisions, optimisations (R11) et classification taxonomique des
   défauts corrigés dans le périmètre du jalon.

## Jalons charnières

**M0 est le jalon existentiel — il est franchi.** Il prouvait que la chaîne notation,
octets, exécutable, exécution fonctionne de bout en bout sans compilateur, et que la
carte rend le résultat vérifiable. Validation acquise le 26 octobre 2026 (D26 amendée) :
round-trip 100 %, 31 verrous structurels PASS, artefact `hello.exe` de 1 536 octets
déterministe, carte v0 signée Ed25519, verrou croisé fail-closed, exécution constatée
sur Windows 11 (sortie exacte du contrat). Livrables : éditeur PE32+ minimal (écriture des
en-têtes DOS/COFF/PE32+ et des sections `.text`/`.rdata` par le script de build),
hello.exe affiché via WriteFile, carte v0 décrivant les trois blocs initiaux, et le
vérificateur de round-trip keystone/capstone — le tout dans `m0/`.

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

## Universalité — M6 et M7 (v0.3)

Ajoutés par la v0.3 (décision D14), M6 et M7 transforment la portabilité de promesse en
propriété démontrée, en isolant chaque variable. **M6 change l'OS à ISA constante** : le
profil `x86-64-linux-elf64` diffère du profil primaire par l'ABI (SysV : RDI RSI RDX RCX
R8 R9, zone rouge de 128 octets — le piège inverse de msx64), le format (ELF64 avec PIE et
RELRO, écrit à la main) et l'interface système (syscalls + libc). Le critère décisif est le
**diff nul sur la couche I** : les contrats écrits pour Windows s'instancient sur Linux
sans réécriture — c'est la preuve que l'intention vit bien dans I et pas dans les octets.
**M7 change d'ISA** : le profil `riscv64-linux-elf64` impose des instructions de taille
fixe, une convention psABI (a0-a7) et un patch à chaud sans trampoline relatif — bascule
par registre scratch suivie de `fence.i`. Le critère décisif est que **le même oracle**,
dérivé de la couche I inchangée, valide les blocs des deux ISA : le coût de vérification
ne double pas, il se mutualise. M7 vérifie de surcroît un export de continuité
multi-profils de bout en bout.

L'ordre est délibéré : valider d'abord le mécanisme des profils (une seule variable à la
fois), puis l'indépendance de l'ISA. Les profils `aarch64-macos-macho` et `wasm32-wasi`
restent réservés : le protocole ne promet pas la portabilité, il la vérifie — chaque
profil déclaré supporté doit avoir franchi ses critères de sortie.

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
- M6 : profil `x86-64-linux-elf64` — règles identiques, ABI/format/interface différents.
- M7 : profil `riscv64-linux-elf64` — règles identiques, ISA différente, patch à chaud
  adapté.

Après M7 : bloc optionnel de syscalls directs, TLS 1.3 pur en blocs scellés, profils
additionnels (`aarch64-macos-macho`, `wasm32-wasi`) — volontairement hors périmètre
courant afin que chaque addition s'appuie sur des résultats mesurés.
