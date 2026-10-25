# Journal de travail — projet TRIADE

Journal partagé des agents travaillant sur le projet TRIADE. Protocole : lire ce fichier
avant de travailler, y ajouter une section par tâche (voir `triade/REPRISE_PROJET.md` pour
la reprise du projet). Une copie projet est maintenue dans `triade/docs/JOURNAL_TRAVAIL.md`
et sauvegardée avec le dépôt.

---
Task ID: 1
Agent: main (Z.ai, agent principal)
Task: Sauvegarde complète du projet TRIADE sur Google Drive, création du repo git, génération des fichiers d'instruction, mise en place de la sauvegarde/synchro systématiques.

Work Log:
- Vérifié l'environnement : réseau OK, git 2.47.3, Python 3.12.15 ; accès au dossier Drive « Triade » (105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp) confirmé via la vue publique.
- Listé le sous-dossier « Tokens » du Drive ; téléchargé les 4 jetons (client OAuth, refresh token Drive, compte de service, token GitHub) vers triade/.gdrive/ avec permissions 600 — exclus du dépôt (.gitignore, décision D12).
- Lu l'intégralité de la spécification v0.2 existante (PDF de 18 pages généré en session précédente via scripts/triade_v02_spec.py) pour garantir la cohérence des nouveaux fichiers.
- Testé les jetons via scripts/check_auth.py : échange refresh->access token OK (compte alexis.fr.lopez@...), API Drive OK, GitHub OK (compte alexisfrlopez-debug).
- Matérialisé le projet dans /home/z/my-project/triade : README.md, docs/PROTOCOLE_TRIADE.md (spécification v0.2 complète en markdown), docs/FORMAT_CARTE.md, docs/DECISIONS.md (D1-D13), docs/PLAN_MILESTONES.md, copie du PDF formel et des sources de génération (script + diagrammes + assets).
- Rédigé les deux fichiers d'instruction demandés : REPRISE_PROJET.md (reprise rapide : état, restauration, règle de sauvegarde, M0) et PROTOCOLE_TRIADE_AGENT.md (manuel complet pour agent IA : 10 règles, format Carte, boucle de mise à jour, sécurité, cible msx64/PE32+, interdits, checklist de démarrage).
- Créé l'outillage : scripts/drive_sync.py (miroir Drive idempotent par MD5 + bundle git + fichiers d'instruction à la racine, stdlib uniquement), scripts/sync_backup.sh (commit + Drive + GitHub), git-hooks/post-commit (synchro Drive à chaque commit), scripts/check_auth.py (vérification des jetons sans les afficher).
- Initialisé le dépôt git (branche main, commit 86d1bcf, 27 fichiers, 4585 insertions) ; vérifié qu'aucun secret n'est suivi par git.
- Première sauvegarde Drive déclenchée automatiquement par le hook post-commit au moment du commit ; vérifiée par listing API : racine = REPRISE_PROJET.md + PROTOCOLE_TRIADE_AGENT.md + TRIADE/ + Tokens/ ; TRIADE/ = miroir complet + triade-history.bundle (1,9 Mo) ; idempotence confirmée (2e passage : 28 inchangés, 0 erreur).
- Créé le repo GitHub privé alexisfrlopez-debug/triade (HTTP 201) ; configuré le credential helper vers .gdrive/git-credentials (600) ; poussé main (tracking origin/main).
- Copié les livrables dans download/ (fichiers d'instruction + archive zip avec bundle) ; test final de sync_backup.sh de bout en bout.
- Découvert et corrigé un bug lors du test de bout en bout : l'initiation de session résumable pour la mise à jour d'un fichier Drive existant exige la méthode PATCH (POST renvoyait 404 — chemin jamais exercé avant, car la première synchro ne faisait que des créations) ; au passage, toutes les erreurs HTTP sont converties en SyncError, donc un échec par fichier ne bloque plus la synchro complète (commit 574e686). Re-test de bout en bout : 29 inchangés, 0 erreur, push GitHub OK.

Stage Summary:
- Architecture de continuité en place (D11) : dépôt git local = source de vérité ; Google Drive « Triade » = miroir lisible + bundle d'historique restaurable (git clone triade-history.bundle) ; GitHub privé = miroir distant.
- Règle D13 opérationnelle : sync_backup.sh après chaque modification + hook post-commit (synchro Drive à chaque commit) ; le script réinstalle le hook automatiquement s'il manque.
- Prochaine étape du projet : jalon M0 (chaîne notation -> octets -> PE32+ -> exécution Windows 11, hello.exe < 4 Kio, carte v0 signée) — checklist détaillée dans REPRISE_PROJET.md § 7.
- Point de sécurité ouvert : les jetons restent présents dans le dossier Drive partagé par lien — restreindre le partage ou les supprimer du Drive (les copies locales suffisent), puis rotation si doute (REPRISE_PROJET.md § 8).

---
Task ID: 2
Agent: main (Z.ai, agent principal)
Task: Étendre le protocole TRIADE à la v0.3 — trois demandes du développeur : (1) universalité totale (toute plateforme/OS/architecture), (2) SHA-256 par défaut mais modifiable par le développeur, (3) récupération/sauvegarde de la Carte par le développeur pour reprendre le projet avec un agent différent.

Work Log:
- Analysé les trois demandes au regard de la fonction objectif (Sécurité > Performance > Optimisation > Coût en tokens) et de la gouvernance du journal des décisions (amendements explicites, jamais de changement silencieux).
- Conçu la réponse architecturale : (1) universalité par profils de cible à sept éléments obligatoires (ISA/types, ABI, format, interface système, patch à chaud, notation, padding) — couche I indépendante de la cible, carte indexée par profil, un binaire par profil ; (2) suite cryptographique paramétrable en trois champs d'en-tête (algo_hachage sha256 par défaut, algo_signature ed25519, algo_chiffrement xchacha20poly1305) bornée par des listes blanches, empreintes préfixées, migration par re-cryptage atomique ; (3) export de continuité chiffré + signé (I+B+C+manifeste autodescriptif), import en cinq étapes, oracle jamais exporté.
- Réécrit docs/PROTOCOLE_TRIADE.md en v0.3 : §10 « Profils de cible » (table des profils, différences inter-profils SysV/zone rouge et RISC-V/fence.i), §8.3 suite paramétrable, §8.4 export de continuité (avec ligne « vol d'export » au modèle de menace), précisions R1/R7, glossaire (+4 termes), journal des versions.
- Réécrit docs/FORMAT_CARTE.md : en-tête normalisé avec champs de suite cryptographique, champ cible= dans l'entrée de bloc, empreintes <algo>:<hex>, nouvelle section export de continuité (contenu, sécurité, import 5 étapes, statut de l'interdiction), nouvelle section re-cryptage.
- Ajouté D14 (universalité, amende D10), D15 (cryptographie paramétrable, amende D5), D16 (export de continuité, précise R1) à docs/DECISIONS.md avec développements et alternatives rejetées (bytecode portable rejeté car trahit la fonction objectif Performance).
- Étendu docs/PLAN_MILESTONES.md à M0–M7 : M6 portabilité inter-OS (x86-64-linux-elf64, critère = diff nul sur I), M7 portabilité inter-ISA (riscv64-linux-elf64, fence.i, critère = même oracle mutualisé), mise à jour des rappels protocolaires.
- Réécrit PROTOCOLE_TRIADE_AGENT.md en v0.3 : nouveau §2 profils de cible, en-tête de carte en §4, listes blanches, procédure d'import de l'export, §7 rebaptisé « profil primaire » avec §7.5 différences inter-profils, interdits étendus à 12 (export non chiffré, import sans vérification), checklist mise à jour.
- Mis à jour REPRISE_PROJET.md (version v0.3, §1 réécrit, tableau d'état, section « Nouveautés de la v0.3 », tableau D1–D16, checklist M0 avec en-tête normalisé) et README.md (universalité, D1–D16, M0–M7, état v0.3).
- Corrigé deux incidents d'édition en cours de route (édits MultiEdit qui se chevauchaient ou old_str inexistant — repérés par lecture du fichier puis re-appliqués proprement, dont une coquille « commencue »).
- Sauvegarde systématique exécutée (règle D13) : commit + synchro Drive + push GitHub ; livrables download/ rafraîchis.

Stage Summary:
- Spécification v0.3 figée : le protocole ne dépend plus d'aucune plateforme ; Windows 11 x86-64 reste le profil primaire de validation (M0–M5) ; l'universalité sera démontrée par M6 (Linux) et M7 (RISC-V).
- La cryptographie est désormais paramétrable par le développeur via l'en-tête signé de la carte, dans des listes blanches (seuil : 128 bits, AEAD, signatures déterministes) ; changer en cours de projet = re-cryptage atomique et journalisé.
- L'anti-enfermement est garanti : l'export de continuité (I+B+C+manifeste, chiffré, signé, autodescriptif) permet au développeur de changer d'agent ou de poste ; l'oracle, éphémère, est régénéré depuis I et jamais exporté.
- Précision terminologique consignée : SHA-256 est un algorithme de hachage (empreintes du verrou croisé), pas un chiffrement ; le chiffrement au repos reste XChaCha20-Poly1305 — les trois sont paramétrables dans leurs listes respectives.
- Prochaine étape inchangée : jalon M0 sur le profil primaire ; le PDF v0.3 sera généré à la stabilisation (scripts/triade_v02_spec.py sert de modèle).
