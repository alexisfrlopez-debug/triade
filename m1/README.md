# Jalon M1 — mini-libc scellée et blocs réutilisables

> Premier jalon de réutilisation : un binaire (`selftest.exe`) embarque des blocs
> scellés par un autre (`hello.exe`), la bibliothèque grandit **sans déplacer quoi
> que ce soit** (R7), les blocs se cristallisent (R6), l'oracle différentiel tourne
> à volume de référence (R5, D29) et les budgets tokens passent de cibles de
> conception à **métriques mesurées** (D31). Profil primaire `x86-64-win11-pe`.

**Statut : `0.2.0` finale — jalon M1 franchi** (26 octobre 2026, D32). Validation
terrain Windows 11 constatée : ligne unique `TRIADE M1 : minilibc 21/21 OK` à
l'identique du contrat libc-08 Q2 (vecteur doré V2). Cristallisation 10/10 sur les
onze blocs, suite de conformité du profil verte (68 contrôles, éléments 1-4 et
6-7), budgets mesurés conformes — balise **immuable** (§ 9) : tout défaut
ultérieur se corrige en `0.2.1` à contrat stable (R4). Jalon suivant : **M2**
(patch à chaud sur serveur TCP écho).

## Résultats mesurés (session du 26 octobre 2026)

| Contrôle | Résultat |
|---|---|
| Round-trip de notation (R5) | **100 %** — 388 instructions sur 9 blocs embarqués (279 pour le seul autotest), keystone → capstone → keystone |
| Oracle structurel | **134 verrous PASS** (contrats I vérifiés sur le code désassemblé) |
| Oracle différentiel (D29, Unicorn) | **76 010 cas verts** par exécution (graines 3-14, ~1,04 M cas cumulés) ; falsification 10/10 corruptions détectées |
| Cristallisation (R6) | **11/11 blocs à 10/10** — immuables ; toute modification exige la procédure lourde |
| Adresses stables (R7) | **DÉMONTRÉ** par `demo_r7.py` : dev.1 → dev.2, 0 octet déplacé, memset entré exclusivement dans la réserve int3, io hérités octet-identiques à `hello.exe` |
| Suite de conformité profil (§ 8.2, D22) | **VERTE — 68/68 contrôles** (éléments 1-4, 6-7 ; élément 5 = patch à chaud, jalon M2) |
| Budgets tokens (D31, mesurés) | **localiser 51** (cible 64) / **éditer 719** (cible 3 000) / **ajouter 1 088** (cible 6 000) — `budgets_tokens.py`, tokenizer cl100k_base, re-mesurés au scellage final (D31/D32) |
| Construction | 0 erreur / 0 avertissement ; artefact déterministe |
| Artefact | **selftest.exe, 9 216 octets** (sha256 `8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0`), réutilisation M0 : a10002/a10003 octet-identiques |
| Carte projet (D28) | génération 1, multi-artefacts : 11 blocs indexés sur 2 exécutables, 4 fragments chiffrés, signature Ed25519, verrou croisé R8 fail-closed |
| Export de continuité (D16) | généré et auto-vérifié : conteneur chiffré + signé, import 5 étapes OK (`export_continuite.py`) — lignée `0.2.0` au coffre Drive |
| **Validation terrain Windows 11 (D32)** | **PASS — 26/10/2026** : `C:\Users\Alek\Downloads>selftest.exe` → ligne unique `TRIADE M1 : minilibc 21/21 OK` (contrat Q2, vecteur doré V2), retour au prompt sans incident ; ré-vérification post-scellage graine 15/16 verte (76 010 cas, sortie exacte, code 0) |

## Structure

```
m1/
├── README.md              ce fichier
├── I/                     couche I : 8 spécifications libc (gabarit § 2.2, écrites avant notation)
├── notation/              notation x86-64 des blocs (brouillons/ = arithmétique d'adresses de l'auteur)
├── layout.py              plan d'adressage par zones (D28) — source unique builder/oracle/outils
├── build_m1.py            chaîne : assemblage, oracle, éditeur PE32+, carte, verrou croisé
├── oracle_differentiel.py oracle éphémère (D1) sur substrat Unicorn (D29)
├── carte_m1.py            crypto de la carte projet (Argon2id, HKDF, XChaCha20, Ed25519)
├── conformite_profil.py   suite de conformité du profil (§ 8.2, D22) — 68 contrôles
├── budgets_tokens.py      instrumentation des budgets (§ 12, D31)
├── demo_r7.py             démonstration des adresses stables (lit l'historique git)
├── export_continuite.py   export de continuité chiffré + signé (D16, FORMAT_CARTE § 8)
├── selftest.exe           artefact B (9 216 o)
├── carte/                 couche C : en-tête, 4 fragments, signature, clé publique, tableau de bord
├── outils/auteur.py       outil d'auteur : arithmétique d'adresses des déplacements RIP
└── export/                conteneurs de continuité (LOCAUX, jamais committés — coffre)
```

## Layout par zones (D28 — R7, jamais déplacé)

| Zone | Plage | Contenu |
|---|---|---|
| io | `0x1000-0x10FF` | `0x1000` réservé (hello-main M0) ; a10002 write @ `0x1040`, a10003 exit @ `0x1080` (octets hérités M0) ; `0x10C0` réservé io-03+ |
| libc | `0x1100-0x17FF` | memcpy @ `0x1100`, memcmp @ `0x1180`, strlen @ `0x1200`, itoa @ `0x1280`, zone_alloc @ `0x1300`, zone_reset @ `0x1380`, memset @ `0x13C0` (réserve dev.1 → occupé dev.2) ; `0x1440+` réserve int3 pour libc-09+ |
| app | `0x1800-0x1FFF` | autotest libc-08 (point d'entrée, non scellé — propre au binaire) |
| .rdata | `0x2000+` | structures PE héritées de M0 aux RVA exactes (descripteurs `0x2030`, hint/names, INT `0x2090`, IAT `0x20B0`, BASERELOC `0x20D0`), puis vecteurs dorés et messages |
| .data | `0x3000+` | curseur d'arène (8 o) puis arêne alignée 64 (`0x3040`, 1 984 o) |

Les six premiers blocs libc + les deux io ont été scellés en dev.1 ; memset est
entré en dev.2 **exclusivement dans la réserve** (slot `0x13C0` rempli d'int3 en
dev.1) sans qu'aucun octet scellé ne bouge — c'est la démonstration R7, prouvée
par `demo_r7.py` sur l'historique git lui-même.

## Les quatre critères de sortie M1 (PLAN_MILESTONES)

1. **Oracle à 100 %** — acquis : 76 010 cas verts à chaque exécution, entrées
   aléatoires contraintes par les pré-conditions, référence Python dérivée de I,
   comparaison octet par octet (valeur de retour, mémoire, curseur d'arène,
   registres non volatils, RSP, intégrité de l'image, canari de pile).
2. **Première cristallisation** — acquise : 10 vérifications réussies par bloc
   (graines distinctes 3-12), compteurs consignés dans frag-prf, blocs immuables.
3. **Adresses stables démontrées** — acquise : `demo_r7.py` (verdict R7 DÉMONTRÉ).
4. **Première mesure effective des budgets** — acquise : `budgets_tokens.py` sur
   la carte scellée déchiffrée et les sources réelles (D31) ; le tableau de bord
   affiche localiser/éditer/ajouter mesurés avec leurs cibles.

Conditions transverses : oracle vert ✓, suite de conformité verte ✓, tableau de
bord conforme sans métrique au rouge ✓, carte signée + verrou croisé ✓, journal à
jour (D27-D32) ✓.

**Fermeture du jalon : validation terrain Windows 11 constatée le 26 octobre 2026
(D32)** — procès-verbal ci-dessous ; balise finale `0.2.0` scellée par
`build_m1.py --sceller-final` (cristallisation 10/10 + conformité 68/68
re-exécutées, manifeste frag-bld basculé, carte re-signée).

## Utilisation

```bash
cd m1
python3 build_m1.py --phase 2          # construction dev.2 (déterministe, byte-identique)
python3 build_m1.py --verifier --graine N   # R5/R8 : ré-vérification + cristallisation (R6)
python3 build_m1.py --sceller-rc       # rc.1 : exige 10/10 + conformité verte
python3 build_m1.py --sceller-final  # 0.2.0 finale : exige 10/10 + conformité verte + constat terrain consigné (D32)
python3 conformite_profil.py           # suite de conformité du profil (§ 8.2)
python3 budgets_tokens.py              # mesure des budgets (écrit budgets.json)
python3 demo_r7.py                     # démonstration des adresses stables
python3 export_continuite.py           # export de continuité chiffré + signé + auto-import
```

Dépendances : celles de M0 + `unicorn`, `tiktoken` (instrumentation).

## Procédure de validation terrain (rc.1 → 0.2.0 finale) — CLOSE

1. Récupérer `selftest.exe` (miroir Drive `TRIADE/m1/` ou copie `download/`).
2. Sur Windows 11 : `cd` vers le dossier, puis `.\selftest.exe` (PowerShell) ou
   `selftest.exe` (cmd). Defender peut demander confirmation (exécutable non
   signé — chantier séparé).
3. Attendu : la ligne unique `TRIADE M1 : minilibc 21/21 OK` (contrat libc-08
   Q2 : « N/21 » suivi de « OK »/« KO »), code de sortie 0. *Erratum (D32) : ce
   document annonçait initialement « 21 lignes » — erreur de formulation ; le
   contrat et l'artefact font foi.*
4. Contrôles optionnels : `echo %ERRORLEVEL%` (attendu 0) et
   `certutil -hashfile selftest.exe SHA256` (attendu `8038585b…f3c0`).
5. Consigner le constat au journal des décisions → la balise `0.2.0-rc.1`
   devient `0.2.0` (version finale, balise immuable) ; écart éventuel →
   `0.2.1` à contrat stable (R4).

**Procès-verbal (26 octobre 2026) : PASS — balise `0.2.0` finale scellée (D32).**
Exécuté depuis `cmd` sur la machine Windows 11 du développeur
(`C:\Users\Alek\Downloads>selftest.exe`) : la ligne unique
`TRIADE M1 : minilibc 21/21 OK` s'affiche à l'identique du contrat Q2 (vecteur
doré V2 — N = 21 vecteurs dorés réussis), retour au prompt sans incident.
L'auto-test a rendu son verdict embarqué ; le code de sortie 0 est la
post-condition Q3, reconfirmée par l'oracle en émulation après scellage
(graines 15 et 16 : 76 010 cas verts, sortie exacte, code 0). Empreinte de
l'artefact scellé : sha256 `8038585b…ff3c0` (manifeste frag-bld, revérifiée
localement). La balise `0.2.0` est immuable (§ 9) ; tout défaut découvert après
coup se corrige en `0.2.1` à contrat stable (R4). Contrôles optionnels au choix
du développeur : `echo %ERRORLEVEL%` (attendu 0), `certutil -hashfile
selftest.exe SHA256` (attendu `8038585b…f3c0`).

## Limites assumées (consignées D28-D31)

- **CFG différé** (héritage M0) : DEP/ASLR/HEVA actifs, LOAD_CONFIG/GFIDS
  reportée — la conformité élément 3 du profil est verte sur les protections
  exigées à M1.
- **Arène non thread-safe** : l'allocateur par zone est mono-thread (contrat
  libc-05) ; le multi-thread arrive avec le serveur TCP (M2).
- **Budget localiser amendé** (D31) : la mesure a invalidé l'estimation v0.4.0
  (le gabarit canonique mesurait déjà 43 tokens) — budget 64 tokens, format
  frag-loc allégé en conséquence (51 tokens mesurés).
- **Cristallisation et continuité** : les compteurs de cristallisation vivent
  dans frag-prf, chiffré avec la phrase maîtresse ; la perte du poste les remet
  à zéro (D30) — l'export de continuité (D16) est désormais le mécanisme de
  coffre qui les préserve.
