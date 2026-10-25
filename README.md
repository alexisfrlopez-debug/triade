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
| Consulter la spécification complète | `docs/PROTOCOLE_TRIADE.md` (v0.3, source de travail) — `docs/Protocole_TRIADE_v0.2_Specification.pdf` (archive formelle v0.2) |
| Comprendre le format de la Carte | `docs/FORMAT_CARTE.md` |
| Consulter les arbitrages | `docs/DECISIONS.md` (D1–D16) |
| Voir la feuille de route | `docs/PLAN_MILESTONES.md` (M0–M7) |

## Sauvegarde et continuité

Règle absolue — après **chaque** modification du projet :

```bash
bash scripts/sync_backup.sh "description courte de la modification"
```

Le script committe, synchronise le miroir Google Drive (fichiers + bundle d'historique)
et pousse vers le repo GitHub privé. Le hook `post-commit` synchronise le Drive à chaque
commit. Vérification des jetons : `python3 scripts/check_auth.py`.

## État du projet

Conception terminée (spécification v0.3 figée : universalité par profils, cryptographie
paramétrable, export de continuité), infrastructure de sauvegarde opérationnelle,
implémentation non commencée. **Prochaine étape : jalon M0** — preuve de la chaîne
notation → octets → PE32+ → exécution sur Windows 11 (hello.exe < 4 Kio, carte v0
signée).

## Avertissement

Le dossier `.gdrive/` contient des jetons d'accès : il ne doit jamais être commité,
synchronisé ni affiché. L'application de validation (intercepteur MITM) est destinée à des
tests autorisés en environnement de laboratoire uniquement.
