# TRIADE — Développement logiciel en code machine par agent IA

Protocole et outillage permettant à un agent IA de développer, vérifier et mettre à jour
des logiciels **100 % code machine natif**, sans compilateur ni langage de programmation,
grâce à une **Carte** de balises signée, chiffrée et fragmentée qui relie les intentions
aux octets. Ce que l'agent écrit est ce qui s'exécute — et rien d'autre.

Le protocole est **universel depuis la v0.3** : toute plateforme / OS / architecture est
un profil de cible vérifiable (profil primaire de validation : x86-64 / Windows 11,
PE32+ écrit à la main). La suite cryptographique est paramétrable par le développeur
(hachage SHA-256 par défaut, listes blanches), et l'**export de continuité** chiffré
permet de sauvegarder et transférer l'état de développement vers n'importe quel agent
conforme TRIADE.

## Priorités (non négociables, arbitrage lexicographique)

**Sécurité > Performance > Optimisation > Coût en tokens** — un objectif n'est jamais
sacrifié au profit d'un objectif de rang inférieur.

## Points d'entrée selon votre rôle

| Vous voulez... | Lisez |
|---|---|
| Reprendre le projet là où il s'est arrêté | `REPRISE_PROJET.md` |
| Démarrer un nouveau projet logiciel avec un agent IA | `PROTOCOLE_TRIADE_AGENT.md` |
| Consulter la spécification complète | `docs/PROTOCOLE_TRIADE.md` (v0.5.0, source de travail) — `docs/Protocole_TRIADE_v0.5.0_Specification.pdf` (archive formelle v0.5.0, révision du retour du terrain : validation terrain normée, taxonomie X1–X8, jalons M0–M2 constatés — D44) ; archives conservées : v0.4.0, v0.3, v0.2 ; vérification : `scripts/spec_v050/verify_spec.py` (cahier V1–V10) |
| Consulter la démonstration | `docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf` (22 p.) — le protocole démontré par le recodage complet de RoomEq sous TRIADE : 42 modules, 437 tests, parité v2.2.2, comparatifs de code avant/après |
| Lire l'édition académique | `docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf` (12 p., D18) — le protocole et son étude de cas restructurés en article de recherche IMRAD : formalisation (verrou croisé, ordre lexicographique), travaux connexes, menaces sur la validité ; vérification interne : `docs/VERIFICATION_v0.4_Article.md` |
| Comprendre le format de la Carte | `docs/FORMAT_CARTE.md` |
| Consulter les arbitrages | `docs/DECISIONS.md` (D1–D32, format normalisé depuis D24) |
| Voir la feuille de route | `docs/PLAN_MILESTONES.md` (M0–M7) |

## Sauvegarde et continuité

Règle absolue — après **chaque** modification du projet :

```bash
bash scripts/sync_backup.sh "description courte de la modification"
```

Le script régénère d'abord le PDF formel si les sources du protocole ont changé (D17 :
`scripts/build_pdf.sh`, empreinte des sources comparée au stamp du dernier build),
committe, synchronise le miroir Google Drive (fichiers + bundle d'historique)
et pousse vers le repo GitHub privé. Le hook `post-commit` synchronise le Drive à chaque
commit. Vérification des jetons : `python3 scripts/check_auth.py`.

## État du projet

Conception terminée et **gouvernance vérifiée** (spécification v0.4.0 : couche I normalisée,
taxonomie des défauts T1–T6, R10 renforcée, R11 ajoutée, conformité par profil, traçabilité
I↔C↔B↔tests et tableau de bord — née des pratiques du recodage RoomEq), infrastructure de
sauvegarde opérationnelle. **Jalon M0 franchi le 26 octobre 2026** (D26) : chaîne
notation → octets → PE32+ → exécution prouvée sans compilateur — hello.exe (1 536 o,
sha256 c89e330c…), carte v0 signée Ed25519, verrou croisé fail-closed, exécution
constatée sur Windows 11. **Jalon M1 franchi le 26 octobre 2026** (D27–D32) —
mini-libc de sept blocs + autotest dans `selftest.exe` (9 216 o, sha256 8038585b…),
réutilisation inter-artefacts octet-identique des blocs io M0 (R7 démontrée), oracle
différentiel Unicorn 76 010 cas/exécution, cristallisation 11×10/10, suite de
conformité du profil verte (68 contrôles), budgets tokens mesurés (localiser 51/64,
éditer 719/3 000, ajouter 1 088/6 000 — D31), export de continuité chiffré au coffre
(D16) ; validation terrain Windows 11 constatée (ligne unique `TRIADE M1 : minilibc
21/21 OK`, D32) — **balise finale `0.2.0` scellée, immuable**. **Étape en cours :
jalon M2** — patch à chaud sur serveur TCP écho (le jalon de vérité).

## Avertissement

Le dossier `.gdrive/` contient des jetons d'accès : il ne doit jamais être commité,
synchronisé ni affiché. L'application de validation (intercepteur MITM) est destinée à des
tests autorisés en environnement de laboratoire uniquement.
