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

---
Task ID: 3
Agent: main (Z.ai, agent principal)
Task: Générer le PDF formel v0.3 de la spécification et mettre en place la régénération systématique du PDF à chaque mise à jour du protocole (demande explicite du développeur).

Work Log:
- Reconstitué le contexte : lecture du worklog, des quatre sources v0.3 (PROTOCOLE_TRIADE.md, FORMAT_CARTE.md, DECISIONS.md, PLAN_MILESTONES.md) et du générateur v0.2 complet (1276 lignes) ; lecture de la chaîne du skill PDF (SKILL.md, brief report, fonts, cover, palette, overflow, pagination).
- Écrit scripts/triade_v03_spec.py (1603 lignes) sur le modèle v0.2 : mêmes fonte/palette/géométrie (continuité visuelle), contenu étendu aux mécanismes v0.3 — tableau des décisions D1–D16, en-tête normalisé de la carte (§4.2 + bloc de code + table des champs), §8.3 suite cryptographique paramétrable avec table des listes blanches, §8.4 export de continuité (conteneur, import en cinq étapes, statut de R1), chapitre 10 « Profils de cible » (sept éléments, table des cinq profils, ABI msx64, différences inter-profils), feuille de route M0–M7, glossaire 16 termes, journal des versions à trois lignes — 17 tableaux, 4 blocs de code, 2 figures réutilisées.
- Écrit la couverture v0.3 (triade_v03_cover.html, gabarit 01 HUD inchangé) : kicker « Version 0.3 », résumé et méta actualisés (universalité, cryptographie paramétrable, export de continuité, profil primaire).
- Chemins du générateur rendus restaurables : tout dérive de TRIADE_BASE (défaut /home/z/my-project) et du dépôt triade/ — le script vit dans le dépôt et écrit ses artefacts dans le dépôt (corps, couverture, PDF final) + copie livrable dans download/.
- Découvert et corrigé un défaut latent de numérotation hérité du générateur v0.2 : les pieds de page sont dessinés au DÉBUT de chaque page, or le marqueur de début de corps mettait à jour BODY_START en cours de passe — avec un sommaire sur deux pages, la séquence devenait i, 1, 2, 2 (le « ii » manquait, doublon de « 2 »). Correctif : gel effectif de la valeur en phase 2 (drapeau BODY_FROZEN) ; le commentaire « valeur gelée » du v0.2 n'était pas appliqué réellement.
- Erratum v0.2 : même correctif appliqué au générateur v0.2, archive régénérée à l'identique (21 pages, contenu inchangé, seuls les numéros de pied de page des pages i/ii/1 sont corrigés) — documenté dans D17 et le présent journal.
- Pipeline de qualité exécuté sur les deux PDF : poster_validate + cover_validate (0 chevauchement), rendu vectoriel html2poster 794px, code.sanitize, meta.brand, pages.clean (0 page blanche), font.check (0 glyphe manquant), pdf_qa 12/12 PASS, vérification programmatique de la concordance sommaire ↔ pages réelles et de la séquence complète des pieds de page (i, ii, 1–24).
- Mis en place la régénération systématique (D17) : scripts/build_pdf.sh — empreinte SHA-256 des six sources (4 markdown + générateur + couverture) comparée au stamp .pdf_build.stamp suivi par git ; toute divergence déclenche la reconstruction complète avec contrôles ; intégré à sync_backup.sh en étape 0.5, AVANT le commit. Testé de bout en bout : idempotence (2e appel sans action), détection d'une modification réelle de contenu (--check → code 2), reconstruction + QA, sémantique de retour arrière (rebuild après revert).
- Mise à jour documentaire : D17 consignée dans docs/DECISIONS.md (choix, alternatives rejetées, développement) ; note d'en-tête de PROTOCOLE_TRIADE.md réécrite (PDF v0.3 généré + règle de régénération) ; REPRISE_PROJET.md (tableau d'état, arborescence avec build_pdf.sh et fichiers v0.3, description du flux de sauvegarde étendu, ligne D17) ; README.md (pointeurs de spécification, D1–D17, description du sync).
- Captures QA archivées dans scripts/assets/ (qa_v03_p01_couverture, p02_sommaire, p07_decisions, p23_profils, p25_jalons).
- Sauvegarde systématique finale (D13) : le sync a régénéré le PDF (sources DECISIONS/PROTOCOLE modifiées — démonstration en conditions réelles de D17), commit + synchro Drive + push GitHub ; livrables download/ rafraîchis (PDF v0.3, zip de sauvegarde regénéré).

Stage Summary:
- PDF formel v0.3 livré : docs/Protocole_TRIADE_v0.3_Specification.pdf (27 pages : couverture + sommaire i-ii + corps 1-24), QA 12/12, sommaire cliquable concordant, numérotation i, ii, 1-24 sans doublon.
- D17 opérationnelle : le PDF est un artefact dérivé, régénéré automatiquement avant chaque commit dès qu'une source du protocole change ; un clone frais ne reconstruit pas inutilement (stamp suivi par git) ; un échec de build est signalé sans bloquer la sauvegarde des sources.
- Erratum v0.2 consigné et appliqué : numérotation des pieds de page corrigée sur l'archive (défaut latent du générateur, révélé par le sommaire v0.3 sur deux pages).
- Prochaine étape inchangée : jalon M0 sur le profil primaire (checklist dans REPRISE_PROJET.md § 7).

---
Task ID: 9
Agent: main (Z.ai, agent principal)
Task: Rédiger le PDF du protocole v0.3 en utilisant le recodage de RoomEq
comme démonstration, avec comparatifs de code avant/après (demande du
développeur ; fait suite à la validation des reverse-specs installateur).

Work Log:
- Reconstitué le contexte : spécification v0.3 intégrale, FORMAT_CARTE,
  DECISIONS (protocole D1-D17 / RoomEq D1-D11), CARTE RoomEq, PARITE-v2.2.2,
  WORKLOG du recodage, générateur v0.3 complet (continuité visuelle).
- Collecté les métriques réelles des deux dépôts : legacy @ deff25c
  (82 fichiers, 14 891 lignes, 228 tests, MixerViewModel 1 075 lignes) vs
  v3 @ v3.0.0-dev.1 (93 fichiers, 15 438 lignes, 437 tests, plus gros
  ViewModel 399 lignes en 5 partiels) ; empreintes md5 complètes des données
  embarquées recalculées.
- Écrit scripts/triade_v03_demo_roomeq.py (générateur ReportLab complet,
  même fonte/palette/géométrie que la spécification) : 12 chapitres —
  synthèse du protocole (couches avec colonne d'instanciation RoomEq,
  dix règles traduites, boucle, profils), candidat et dette, adaptation D4,
  sept vagues, TROIS comparatifs de code avant/après extraits verbatim
  (D8 seuil 8→1000 mesuré + spec I + test PureNoise ; monolithe
  MixerViewModel → 5 partiels + OutputPresetCoordinator ; SanitizeFileName
  multi-plateformes), résultats mesurés, reverse-specs D11, portée de la
  preuve, feuille de route — 14 tableaux, 9 blocs de code, figure
  d'architecture réutilisée.
- Écrit la couverture (triade_v03_demo_cover.html, gabarit 01 HUD) :
  kicker « étude de démonstration », héros « Recodage / RoomEq ».
- Pipeline de qualité : poster_validate + cover_validate (0 chevauchement),
  rendu vectoriel html2poster 794px, code.sanitize, meta.brand,
  pages.clean (0 page blanche), font.check (0 glyphe manquant),
  pdf_qa PASS intégral ; vérificateur dédié
  (scripts/verify_demo_pdf.py hors dépôt) : séquence des pieds i, 1-20 ;
  concordance sommaire ↔ pages réelles ↔ destinations des liens 12/12 ;
  présence des éléments clés (extraits, test D8, empreintes complètes).
- Correctifs en cours de route : cellules « — » isolées remplacées
  (avertissements de ponctuation), colonne empreintes élargie (hash md5
  sur une ligne), association liens du vérificateur recalibrée.
- Régénération MANUELLE (choix documenté dans l'en-tête du script) : le
  PDF de démonstration est une édition, contrairement au PDF formel
  (D17 s'applique aux seules sources du protocole).
- Documentation : REPRISE_PROJET.md (état, arborescence, commandes),
  README.md (ligne « Consulter la démonstration »), présent journal.
- Sauvegarde systématique (D13) : commit + synchro Drive + push GitHub ;
  copie livrable dans download/.

Stage Summary:
- PDF de démonstration livré : docs/Protocole_TRIADE_v0.3_Demonstration_
  RoomEq.pdf (22 pages : couverture + sommaire i + corps 1-20), QA PASS,
  sommaire cliquable concordant, numérotation i, 1-20 sans doublon.
- Le protocole dispose désormais de deux volets documentaires : la
  spécification normative (27 p.) et sa démonstration à échelle réelle
  (22 p.) — même série visuelle, faits vérifiables (empreintes, tests,
  dépôts scellés).
- Prochaine étape inchangée : jalon M0 sur le profil primaire ; côté
  RoomEq, validation Windows puis v3.0.0 finale.
