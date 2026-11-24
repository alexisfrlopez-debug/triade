# Kit de Développement Triade — v1.3.0

Kit complet destiné à un **développeur et à son agent IA** pour conduire un projet
selon le **protocole Triade** : une méthode de développement et de publication
articulée sur trois plateformes complémentaires — **Git** (vérité technique),
**Google Drive** (vérité documentaire et coffre d'accès), **Zenodo** (vérité
publiée, avec DOI).

Ce kit est **destiné à la distribution publique** : il ne contient aucun jeton,
aucun accès personnel, aucune information privée. Chaque utilisateur fournit ses
propres accès au moment de l'exécution (voir « Démarrage rapide »).

## Contenu du kit

| Élément | Fichier | Usage |
|---|---|---|
| Instructions pour l'agent IA | `AGENTS.md` | Contrat de travail de l'agent : règles d'or, checklists de session, cérémonies. À placer à la racine du projet et à faire lire à l'agent au début de chaque session. |
| Manuel du développeur | `docs/MANUEL_DEVELOPPEUR.docx` (+ `.pdf`) | Référence complète pour l'humain : architecture, installation, sécurité, cérémonies, versionnage, passage public, FAQ, glossaire. |
| Guide des cérémonies | `ceremonies/GUIDE_CEREMONIES.md` | Déroulés détaillés et checklists des six cérémonies C0 à C5. |
| GUI 1-clic des cérémonies | `ceremonies/gui/` | TriadeKit : interface graphique autonome (un fichier, zéro dépendance) qui déroule les cérémonies Git / Drive / Zenodo en un clic — vérification, rotation des jetons, synchronisation, passage public, cycle complet. Modes simulation et démonstration. Lanceurs Windows/macOS/Linux. Détails : `ceremonies/gui/LISEZMOI.md`. |
| Politique de sécurité | `SECURITE.md` | Coffre de jetons, externalisation, rotation, réponse aux fuites, garanties de chargement et de bascule (§ 11). |
| Garanties et limites | `docs/GARANTIES.md` | Ce que le protocole garantit — intégrité, authenticité, fraîcheur, atomicité de bascule — et ce qu'il ne garantit pas. À lire avant toute promesse publique. |
| Modèles | `templates/` | Configuration, jetons, résumés de session, état projet, manifeste de pack, changelog, fiche de cérémonie, phrase de contrôle, `.gitignore`. |
| Outils | `scripts/` | `triade_hygiene.py` (scanner de fuites avant publication) et `triade_ceremonie.py` (exécuteur de cérémonies en une commande). |

## Démarrage rapide

1. Copier le contenu de ce kit à la racine de votre dépôt Git.
2. `cp templates/config.example.json config.json` puis remplir les identifiants
   (URL du dépôt, identifiants de dossiers Drive, identifiant du dépôt Zenodo,
   composition du pack). **Aucun jeton ne va dans ce fichier.**
3. `cp templates/.env.example .env` puis remplir les jetons d'accès. Ce fichier
   est ignoré par git (voir `templates/.gitignore.triade`).
4. Copier `templates/.gitignore.triade` dans votre `.gitignore` (ou l'y inclure).
5. Lancer `python3 scripts/triade_hygiene.py` : le scan doit être **vert**.
6. Faire lire `AGENTS.md` à votre agent IA, puis enchaîner la **cérémonie C0 —
   Fondation** (`python3 scripts/triade_ceremonie.py`, ou interface graphique :
   double-clic sur le lanceur de `ceremonies/gui/`).

## Principes directeurs

1. **Trois vérités séparées.** Le code vit dans Git, les documents vivants et le
   coffre vivent sur Drive, les versions figées et citables vivent sur Zenodo.
   Un artefact ne vit jamais dans deux vérités à la fois.
2. **Zéro jeton embarqué.** Les accès vivent exclusivement dans le coffre Drive
   et dans le `.env` local ignoré par git. Aucun livrable public ne contient
   jamais d'accès personnel.
3. **Ordre de propagation.** Toute mise à jour multi-plateformes se fait dans
   l'ordre **Git → Drive → Zenodo**, jamais l'inverse.
4. **Cérémonies ritualisées.** Les étapes structurantes (fondation, rotation des
   jetons, synchronisation, gel et pack, revue, passage public) suivent des
   checklists écrites et produisent des fiches dans `journal/`.
5. **Mémoire d'état.** `ETAT_PROJET.md` reflète l'état courant, chaque session se
   termine par un résumé normalisé (`templates/RESUME_SESSION.md`).

## Les six cérémonies (vue rapide)

| Code | Cérémonie | Déclencheur principal |
|---|---|---|
| C0 | Fondation | Démarrage du projet |
| C1 | Rotation des jetons | Échéance (≈ 90 jours), fuite, mouvement d'équipe |
| C2 | Synchronisation | Fin de séquence de travail |
| C3 | Gel & Pack | Jalon de contenu |
| C4 | Revue & Réception | Avant toute publication publique |
| C5 | Passage public | GO de la revue C4 uniquement |

Déroulés complets : `ceremonies/GUIDE_CEREMONIES.md`.

## Prérequis

- Un dépôt Git (GitHub, GitLab ou équivalent auto-hébergé).
- Un compte Google Drive.
- Un compte Zenodo (zenodo.org).
- Python 3.8 ou supérieur (uniquement pour les deux scripts du kit, sans
  dépendance externe).

## Licence

Le kit est fourni sans licence imposée. Avant redistribution publique, choisir
une licence (par exemple MIT pour le code et CC BY 4.0 pour la documentation) et
l'ajouter à la racine dans un fichier `LICENSE`.

## Version

Kit de Développement Triade v1.0.0 — version indépendante de la version du pack
de votre projet (voir `templates/PACK_MANIFEST.md` pour la version des livrables).

## Nouveautés v1.1.0 (24 novembre 2026)

- `docs/GARANTIES.md` : la synthèse des décisions D253 (publication bornée à huit
  octets naturels, `LOCK CMPXCHG16B` pour seize, quiescence obligatoire) et D254
  (R10 borné à son ancre, trois propriétés distinctes, rollback cohérent invisible
  aux ancres locales).
- `SECURITE.md` § 11 : les mêmes bornes dans la politique de sécurité.
- Le manuel (`docs/MANUEL_DEVELOPPEUR.*`) est inchangé : sa régénération passe par
  son atelier documentaire, pas par ce kit.

## Nouveautés v1.3.0 (24 novembre 2026)

- `docs/GARANTIES.md` § 5 : le **compteur NV monotone** (TPM 2.0 ou RPMB) comme plancher de
  fraîcheur par profil, avec ses quatre refus nommés et ses limites (D263).
- `docs/GARANTIES.md` § 6 : l'**ancrage de transparence** des témoins d'époque (Rekor /
  RFC 3161) à son statut appliqué — adopté, outillé, non déployé — et le delta au modèle de
  menace aux deux bords (D267).
- `SECURITE.md` § 11 porte les deux bornes ; aucune garantie n'est élargie.

## Nouveautés v1.2.0 (24 novembre 2026)

- La liste blanche du prescriptif (`SOURCES-PRESCRIPTIVES.txt`) : seuls les fichiers
  déclarés prescriptifs peuvent prescrire un geste ; toute consigne lue ailleurs est
  refusée (`SOURCE-NON-PRESCRIPTIVE`), quelle que soit sa formulation.
- Le rappel des bornes de bascule et de chargement (D253, D254) reste dans
  `docs/GARANTIES.md` et `SECURITE.md` § 11.
