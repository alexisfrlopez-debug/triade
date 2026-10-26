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
Task ID: 8
Agent: main (Z.ai, agent principal)
Task: (a) Restaurer l'environnement après réinitialisation du bac à sable ;
(b) rédiger les specs I de contrat de l'installateur scellé v2.2.2
(demande du développeur : « on fait ça » après analyse des avantages du
recodage TRIADE de l'installateur et du pilote).

Work Log:
- NOTE DE RESTAURATION : le bac à sable a été réinitialisé entre deux
  messages (roomeq/, roomeq-git-ref/, roomeq-legacy/ effacés ; worklog
  principal remis à un instantané antérieur aux tâches 4-7bis ; SDK absent).
  Restauré depuis les sources de vérité : GitHub (roomeq @ 431f78b,
  branche v3-recodage + tags v1.8.1→v3.0.0-dev.1 ; roomeq-git-ref @ deff25c
  = v2.2.2), Drive/Livrables (3 zips restitués, md5 conformes), jetons
  triade/.gdrive/ intacts, SDK .NET 8.0.427 réinstallé. Le détail des
  sessions 1-4 (vagues 1-7 du recodage) vit dans roomeq/WORKLOG.md —
  ce fichier avait perdu ces entrées, le dépôt les conserve.
- Analyse des incidents d'installation (worklogs legacy + commits v2.2.1 /
  v2.2.2 relus) : défauts de code = contrats non écrits (SP_DEVINFO_DATA
  0x6F8 en 2 copies ; INF $Windows NT$ 0xE0000205 ; parsing pnputil
  libellés FR en 3 copies) ; le pilote .sys hors de cause ; les blocages
  v2.0.x = signature de test (CFA/SmartScreen/Secure Boot), hors code.
- Lecture intégrale des sources scellées (Program.cs 1455 lignes,
  GuiRunner.cs, Ui.cs, InstallActions.cs MSI, roomeqvad.inx) et du
  DriverSetupManager v3.
- 8 specs I écrites dans roomeq/I/installateur/ (M-INS-01..08, « ⬜ spec
  prête ») : séquence 6 étapes, contrat Win32 (verrou SizeOf==32), contrat
  INF (validateur $CHICAGO$), contrat outils (publi/orig, CP850, repli
  scan, fixtures partagées app), consentement mode test, désinstallation +
  mode normal, charge utile + ASIO (CLSID), affichage rebranchable.
- Gouvernance : D11 (reverse-specs, conditions de lancement : validation v3
  + décision signature + environnement Windows R5 ; alternatives rejetées),
  CARTE (section modules installateur), PLAN_RECODAGE (vague 8 préparée),
  REPRISE, WORKLOG dépôt (session 5).
- Vérification R5 : aucun code source modifié ; tests re-confirmés par le
  sync (437/437 verts, build 0/0 après réinstallation du SDK).
- Sauvegarde D7 : commit 431f78b (13 fichiers, 901 insertions), push GitHub
  v3-recodage + tags, miroir Drive (8 specs créées, 5 docs mis à jour,
  livrables inchangés), bundle git.

Stage Summary:
- Les contrats de l'installateur scellé v2.2.2 sont figés en 8 specs I
  diffables et versionnées : toute future vague 8 part de contrats testés,
  et les trois défauts historiques (0x6F8, 0xE0000205, libellés pnputil FR)
  sont verrouillés par des critères de test explicites.
- Le pilote noyau reste scellé dans tous les cas (stable, jamais en cause,
  invérifiable sans WDK — R5).
- Prochaine étape inchangée : validation utilisateur Windows réelle de la
  v3.0.0-dev.1 → ouverture v3.0.0 ; la vague 8 attend aussi la décision de
  signature (phase A : certificat EV + attestation Microsoft).

---
Task ID: 9
Agent: main (Z.ai, agent principal)
Task: Rédiger le PDF du protocole TRIADE v0.3 en utilisant le recodage de
l'application RoomEq comme démonstration, avec comparatifs de code
avant/après (demande du développeur ; « c'est validé » = validation des
reverse-specs installateur de la tâche 8).

Work Log:
- Reconstitué le contexte complet (spécification v0.3, décisions des deux
  dépôts, audit de parité, worklog du recodage, générateur de la
  spécification) ; collecté les métriques réelles et recalculé les
  empreintes md5 complètes des données embarquées.
- Écrit le générateur scripts/triade_v03_demo_roomeq.py + couverture
  (triade/scripts/triade_v03_demo_cover.html) : 12 chapitres, 14 tableaux,
  9 blocs de code dont 3 comparatifs avant/après verbatim (D8, monolithe
  ViewModel, SanitizeFileName), même série visuelle que la spécification.
- Pipeline de qualité complet (validateurs, rendu vectoriel, pdf_qa PASS,
  font.check 0) + vérificateur dédié /home/z/my-project/scripts/
  verify_demo_pdf.py : pieds i,1-20 ; concordance sommaire ↔ réél ↔
  liens 12/12 ; éléments clés présents.
- Documentation dépôt triade mise à jour (REPRISE_PROJET, README,
  JOURNAL_TRAVAIL) ; régénération du PDF de démonstration documentée
  comme manuelle (édition, hors D17).
- Sauvegarde systématique : commit + Drive + GitHub + livrable download/.

Stage Summary:
- docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf livré (22 pages,
  QA PASS) : le protocole v0.3 démontré par le recodage RoomEq — 42
  modules, 437 tests, parité v2.2.2, comparatifs avant/après sur pièces.
- Note d'interprétation consignée : la cristallisation v3.0.0 finale de
  RoomEq attend toujours la validation Windows explicite ; si « c'est
  validé » la visait, le retrait du suffixe -dev.1 + tag restent à faire.
- Prochaine étape : validation Windows → v3.0.0 ; jalon M0 côté protocole.

---
Task ID: 10
Agent: main (Z.ai, agent principal)
Task: Cristalliser la v3.0.0 de RoomEq (ordre du développeur :
« cristallise la v3.0.0 ») — retrait du suffixe -dev.1, tag, livrables,
sauvegarde complète. S'est prolongée en publication v3.0.1 puis v3.0.2
après deux échecs CI consécutifs, honorés puis corrigés selon le
protocole.

Work Log:
- v3.0.0 (D12, commit bb40fb5) : suffixe -dev.1 retiré des 3 fichiers
  prévus (Directory.Build.props, LISEZMOI.txt, package_v3.sh) ;
  D12 consignée (écarts terrain → patchs 3.0.x à contrat stable, tags
  immuables) ; docs d'état ré-alignés (CARTE, REPRISE, README, PARITE,
  PLAN_RECODAGE, WORKLOG session 6) ; R5 locale verte (build 0/0, 437/437)
  ; tag annoté v3.0.0 ; packaging local (télémétrie réelle régénérée via
  gen_telemetrie.py) ; push GitHub + miroir Drive + 3 zips 3.0.0.
- Incident 1 : le run CI du tag v3.0.0 ÉCHOUE sur windows-latest — 3 tests
  DiagnosticsTests en IOException « being used by another process ».
  Recensement : la CI v3 n'avait JAMAIS été verte (6 runs rouges depuis
  D10). Cause : tests relisant le journal vivant via File.ReadAllText
  (FileShare.Read) contre le writer DiagnosticsLog (FileAccess.Write) —
  verrouillage obligatoire Windows, invisible Linux/macOS. La legacy
  v2.2.2 portait déjà la solution (ReadLogShared, FileShare.ReadWrite,
  avec commentaire) — perdue au portage v3. Production saine (portage à
  l'identique de la v2.2.2 validée terrain).
- v3.0.1 (D13, commit ab2ec86) : correctif TESTS-ONLY (ReadLogShared
  re-porté, assertions inchangées, zéro fichier de production modifié) ;
  tag v3.0.0 conservé (D12c : immuabilité) ; CI v3.0.1 : tests verts sur
  les 3 OS ✓ mais job Packaging rouge.
- Incident 2 : rg (ripgrep) absent des runners GitHub (13 × « command not
  found », contrôles vides → « contenu du zip TEST incorrect ») + zip
  source avalant artifacts/ (OUT interne en CI — 84 Mo au lieu de 488 Ko).
- v3.0.2 (D14, commit f6cb92c) : package_v3.sh porté au socle POSIX
  (rg → grep/grep -E, sémantique identique ; --exclude artifacts
  --exclude download au rsync du zip source) ; reproducteur permanent
  /home/z/my-project/scripts/simulate_ci_packaging.sh (copie type
  checkout, PATH sandbox sans ripgrep, OUT interne) exécuté AVANT push :
  12/12 contrôles verts, source 488 Ko, 437 tests.
- Publication v3.0.2 : packaging local (télémétrie réelle dans le zip
  test) ; sync_backup (push branche + tags, miroir Drive 12 zips,
  bundle) ; **CI VERTE** (branche + tag, 3 OS + packaging) ; **release
  GitHub v3.0.2 publiée** (draft, 3 zips — placeholder télémétrie en CI
  par design, télémétrie réelle uniquement via les livrables Drive).

Stage Summary:
- **RoomEq v3.0.2 est la version cristallisée et publiée** : 42 modules
  🔒, 437 tests verts (CI 3 OS), build 0/0, parité v2.2.2, release
  GitHub + livrables Drive (test 41,7 Mo / public 41,6 Mo / source
  0,5 Mo).
- La séquence D12→D13→D14 documente trois tags : v3.0.0 (tests Windows
  rouges), v3.0.1 (packaging rouge), v3.0.2 (verte) — aucun déplacé,
  chaque échec corrigé en patch à contrat stable (R4). Premier exemple
  complet du mécanisme « échec CI → patch honnête » du protocole.
- Outils durables : simulate_ci_packaging.sh (à exécuter avant tout push
  de tag) ; connaissance Windows re-portée avec son commentaire.
- Prochaines étapes : validation terrain Windows (écarts → 3.0.x) ;
  vague 8 installateur (specs M-INS prêtes, conditions D11) ; décision
  signature phase A (EV/attestation).

---
Task ID: 11
Agent: main (Z.ai, agent principal)
Task: « Optimiser au max le code de RoomEq en fusionnant les modules et en
modifiant directement le code en natif machine » (présenté comme validation
de la démonstration du protocole TRIADE).

Work Log:
- Analyse littérale de la demande composante par composante, confrontée au
  protocole : (a) fusion des modules = destruction des adresses stables et
  des specs par concern (R2/R4, couche C), gain d'exécution nul (EqChain
  matérialise ses filtres en interne, aucune frontière de module sur le
  thread audio) ; (b) natif machine = trois sens, tous morts : assembleur
  main invérifiable sous R5 (Linux, cible Windows) et perd macOS,
  réécriture C/Rust = recodage v4 sans besoin mesuré (natifs déjà scellés
  D1), et le JIT .NET 8 émet déjà du code machine optimisé.
- Équivalent conforme exécuté : MESURER D'ABORD (précédent D8 : analyse
  avant action). Harnais perf/ créé — console autonome volontairement hors
  gouvernance des modules (pas dans src/, pas dans RoomEq.sln, outillage
  comme scripts/ ; bash perf/run.sh, Release). Faux départ corrigé :
  GC.GetAllocatedBytesForCurrentThread (pluriel).
- Mesures (2 vCPU partagés, 48 kHz stéréo, blocs 10 ms, best-of-5) :
  EqChain 30 bandes × 2 canaux 66 µs/bloc → 152× temps réel ;
  0 octet alloué sur 100 000 blocs (1 000 s de son) ; RingBuffer SPSC
  0,18 µs/bloc → 56 461× ; ESS 12 s régénéré en 10,7 ms → 1 121× ;
  FFT 4096 en 165 µs (517×) ; FFT 1 048 576 en 38,2 ms (572×).
- D15 consignée dans docs/DECISIONS.md (refus motivé, table de mesures,
  conditions de réexamen : SIMD uniquement sur profilage d'un scénario
  réel, NativeAOT seulement si un besoin de démarrage mesuré). README
  (structure + D1-D15) et REPRISE (D15 + perf/ dans l'environnement)
  alignés. CARTE.md volontairement INCHANGÉE : aucun module touché.
- R5 re-vérifiée : build 0/0, 437/437 verts ; commit fe40d99 ; sauvegarde
  D7 (push GitHub + miroir Drive + bundle).

Stage Summary:
- Réponse à la demande : REFUS documenté des deux transformations (elles
  détruiraient la démonstration qu'elles prétendent valider), intention
  honorée par la mesure : le thread audio tourne à 152× temps réel avec
  zéro allocation sur une machine 2 vCPU partagée — il n'existe aucun
  problème de performance à corriger.
- La validation de la démonstration est le refus lui-même : D12→D15 forme
  le corpus complet (cristallisation, échec CI honoré, portabilité
  outillage, refus motivé d'une transformation destructrice) — quatre
  tensions, zéro dérive du cristal, zéro ligne de src/ modifiée.
- Outil durable : perf/run.sh — toute future optimisation part de mesures.
- Prochaines étapes inchangées : validation terrain Windows (écarts →
  3.0.x) ; vague 8 installateur (conditions D11) ; signature phase A.

---
Task ID: 12
Agent: main (Z.ai, agent principal)
Task: Exécuter les quatre recommandations d'une évaluation externe du PDF
de démonstration v0.3 pour la prochaine version du document : (1)
restructuration IMRAD aux standards d'un article de recherche de premier
plan en génie logiciel, (2) formalisation académique des concepts TRIADE
(couches I/B/C, verrou croisé, reverse-specs, invariants, règles, fonction
objectif lexicographique), (3) rédaction des travaux connexes (dette
technique, Design by Contract, AISE) et des menaces sur la validité (N=1,
écart refactoring source / génération binaire native), (4) rapport de
vérification interne avant empaquetage.

Work Log:
- Chaîne skill pdf (voie académique) lue intégralement : SKILL.md,
  briefs/academic.md, configs/fonts.md, typesetting/overflow.md,
  typesetting/cover.md ; sources du projet relues (spécification v0.3,
  DECISIONS D1-D17, générateur de la démonstration v0.3 pour les
  comparatifs avant/après verbatim et les métriques).
- Environnement LaTeX validé par test de fumée : Tectonic 0.15 Linux,
  fontspec + Liberation Serif/Sans/Mono, babel français, algorithm2e
  (Entrées/Sorties), listings UTF-8 (accents et guillemets français
  vérifiés dans le PDF), TikZ, natbib. Conflit algorithm2e x unicode-math
  isolé par débogage binaire → mathématiques Computer Modern retenues.
- Article rédigé en 8 fichiers LaTeX (main.tex + 7 sections) + refs.bib
  (29 références réelles et canoniques, toutes citées) : résumé 246 mots,
  contributions C1-C4, RQ1-RQ3, formalisation (définitions 3.1-3.4,
  prédicat de cohérence kappa à cinq conjoints, ordre lexicographique,
  règles en système de transitions, oracle différentiel), étude de cas
  RoomEq (tableau de correspondance des règles, trois comparatifs
  avant/après, résultats quantitatifs, séquence v3.0.0→v3.0.2, mesures
  D15), discussion, menaces sur la validité (Wohlin : construction,
  interne, externe, conclusion, écart conceptuel §6.5), conclusion.
- Compilation itérative jusqu'à 0 erreur / 0 overfull : correctifs
  (\end{defn}, colonnes tabularx raggedright Y, équation (iii)
  raccourcie, \raggedbottom, titres reformulés, incises en
  parenthèses) ; étiquettes françaises (Tableau, Algorithme) alignées
  sur la prose ; citation lattner2004 réintégrée (29/29 réf. citées).
- Couverture Template 03 (académique, arXiv-like) : écart texte-ligne
  corrigé (23,5 px → 42,5 px ≥ 1U), check-html PASS, cover_validate.js
  PASS, rendu vectoriel html2poster.js ; fusion pypdf avec normalisation
  A4 stricte (0,5 pt) et métadonnées complètes.
- QA finale : pdf_qa 11 contrôles passés / 0 erreur (avertissements
  résiduels analysés : faux positifs bicolonne et typographie française,
  consignés) ; pages.clean 0 page blanche ; font.check 0 glyphe manquant ;
  inspection visuelle VLM sur 5 pages (couverture, titre, méthodologie,
  listing, bibliographie) : 5/5 sans défaut.
- Vérification pré-empaquetage scriptée : scripts/article_v04/
  verify_article.py — 44 contrôles PASS / 0 FAIL (terminologie pivot,
  variantes interdites, ordre IMRAD, RQ/contributions, références
  croisées, clés de citation, flottants légendés et référencés,
  anglicismes hors liste blanche) ; rapport interne rédigé :
  docs/VERIFICATION_v0.4_Article.md (audit affirmation par affirmation
  du document v0.3 : reprise sourcée / reformulation / nuance).
- Gouvernance : D18 consignée (édition académique, noyau normatif v0.3
  inchangé, régénération manuelle hors D17) ; REPRISE_PROJET.md (état,
  arborescence, tableau D, commandes — et correction de la ligne d'état
  RoomEq : cristal v3.0.2, plus -dev.1) ; README.md ; note d'en-tête de
  PROTOCOLE_TRIADE.md ; captures QA archivées dans scripts/assets/.
- Livrables : docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf (12
  pages A4) + copie download/ ; sauvegarde systématique (D13/D17 — la
  modification de DECISIONS.md et PROTOCOLE_TRIADE.md déclenche la
  régénération du PDF formel v0.3, comportement attendu de D17).

Stage Summary:
- Édition académique v0.4 livrée : le protocole TRIADE et son étude de
  cas RoomEq restructurés en article de recherche IMRAD de 12 pages
  (LaTeX/Tectonic, bicolonne, 29 références), avec formalisation
  (kappa, ordre lexicographique, transitions, oracle), travaux connexes
  et menaces sur la validité selon Wohlin.
- Changement de niveau de preuve verrouillé : la v0.4 distingue
  explicitement la couche de gouvernance validée par l'étude de cas du
  cœur natif non validé (M0-M7 ouverts, budgets tokens = cibles non
  mesurées) — la lecture « le protocole v0.3 démontré » de la version
  précédente n'est plus possible.
- Vérification interne complète avant empaquetage : 44 contrôles
  programmatiques PASS, QA PDF 0 erreur, 5/5 pages validées visuellement,
  audit des affirmations du document original consigné.
- Prochaine étape inchangée : jalon M0 sur le profil primaire.

---
Task ID: 13
Agent: main (Z.ai, agent principal)
Task: Réviser le protocole en v0.4.0 « gouvernance vérifiée » — intégrer les pratiques
nées du recodage RoomEq dans le noyau normatif (entrée consignée a posteriori le
26/10/2026 depuis le commit 28b245c ; la session n'avait pas étendu le journal).

Work Log:
- Conduit la révision D19-D25 : invariants de révision (D19, la hiérarchie
  Sécurité > Performance > Optimisation > Coût en tokens devient invariante),
  couche I normalisée avec gabarit de spécification et taxonomie T1-T6 des
  défauts de contrat non écrit (D20), R11 optimisation mesurée (D21),
  conformité par profil avec critères d'acceptation M6/M7 (D22),
  officialisation des pratiques reverse-specs / pré-versions / fixtures (D23),
  traçabilité I-C-B-tests + journal des décisions normalisé + tableau de bord
  (D24).
- Remplacé la chaîne PDF formelle : LaTeX/Tectonic (scripts/spec_v040/) à la
  place du générateur ReportLab (D25) ; PDF v0.4.0 régénéré avec 64 contrôles
  PASS (docs/VERIFICATION_v0.4.0.md) ; archives v0.2/v0.3 conservées.
- Aligné manuel agent (v0.4.0), README et REPRISE ; build_pdf.sh étendu à la
  nouvelle chaîne.

Stage Summary:
- Spécification v0.4.0 scellée : la gouvernance validée par l'étude de cas
  RoomEq est désormais normative ; REPRISE et manuel agent alignés.
- Dernier état avant passage à l'implémentation (M0).

---
Task ID: 14
Agent: main (Z.ai, agent principal)
Task: Implémenter le jalon M0 — prouver la chaîne artefact notation -> octets ->
PE32+ -> exécution sans compilateur (entrée consignée a posteriori le 26/10/2026
depuis le commit 3a9b47a ; la session n'avait pas étendu le journal).

Work Log:
- Écrit la couche I du hello (m0/I/hello-01/02/03 au gabarit § 2.2,
  écrite-avant-code R2) puis la notation x86-64 des trois blocs
  (m0/notation/, layout fixe à slots de 64 octets, déplacements RIP calculés
  une fois pour toutes — WYSIWYG intégral, aucun post-patching).
- Implémenté l'éditeur PE32+ à la main (m0/build_m0.py, 571 lignes) :
  en-têtes DOS/COFF/PE32+, .text RX / .rdata R, imports kernel32 par IAT
  (GetStdHandle, WriteFile, ExitProcess), BASERELOC minimal,
  DYNAMICBASE + HIGH_ENTROPY_VA + NX_COMPAT, artefact déterministe de
  1 536 octets (sha256 c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2).
- Construit l'oracle M0 : round-trip keystone -> capstone -> keystone à 100 %
  (18/18 instructions) + 31 verrous structurels générés depuis les contrats I
  (discipline msx64, appels IAT uniquement, frames équilibrés, cibles RIP
  sémantiques, ud2 défensif, padding).
- Implémenté la carte v0 (m0/carte_m0.py) : quatre fragments chiffrés
  XChaCha20-Poly1305 par dérivation Argon2id 64 Mio/3 it + HKDF, signature
  Ed25519, empreinte racine ; verrou croisé en relecture indépendante,
  fail-closed constaté sur falsification d'un octet de .text (exit 1).
- Validation PE par trois outils indépendants concordants (capstone, pefile,
  objdump) ; D26 consignée avec alternatives rejetées (post-patching,
  émulation wine, tag git prématuré) et limites assumées (CFG différé,
  relocalisations ABSOLUTE, oracle différentiel reporté à M1).
- Sauvegarde systématique exécutée ; état consigné « M0-dev » en attente de
  la validation terrain Windows 11 (hello.exe transmis via le miroir Drive).

Stage Summary:
- Chaîne artefact complète implémentée dans m0/ : le paradigme est
  opérationnel à échelle hello-world, dans les règles R1-R3 et R8-R9 dès le
  premier octet.
- Clés locales (phrase maîtresse, graine Ed25519) gardées hors dépôt
  (m0/.keys/, jamais commité) ; phrase maîtresse confiée au coffre du
  développeur.
- Restait le critère de sortie terrain : exécuter hello.exe sur Windows 11.

---
Task ID: 15
Agent: main (Z.ai, agent principal)
Task: Consigner la validation terrain du jalon M0 — le développeur a exécuté
hello.exe sur sa machine Windows 11 (cmd : « TRIADE M0 : Hello, Windows 11 ! »)
— et restaurer le dépôt local après réinitialisation du bac à sable.

Work Log:
- Reçu le compte rendu terrain du développeur : sortie exacte du contrat
  affichée (« TRIADE M0 : Hello, Windows 11 ! »), retour au prompt sans
  incident — quatrième et dernier critère de sortie de M0 acquis.
- Détecté que le bac à sable local avait été restauré à un état périmé
  (dernier commit local : 927c4cd, PDF v0.3) alors que GitHub et le Drive
  portaient l'état réel (v0.4.0 + M0) — le scénario de reprise après sinistre
  de D11 en conditions réelles.
- Restauré le dépôt : git fetch origin (927c4cd..3a9b47a) puis reset --hard
  origin/main ; arbre M0 complet récupéré (m0/, spec_v040/, article_v04/) ;
  vérifié l'empreinte de l'artefact local : sha256 c89e330c...507f2, conforme
  au manifeste frag-bld (l'exécutable exécuté par le développeur est bien
  l'octet scellé).
- Consigné le verdict : amendement à D26 (validation terrain, M0 franchi,
  26 octobre 2026) ; m0/README.md (statut, ligne de résultat, procès-verbal
  de la procédure de validation) ; tableau de bord (élément 2 de la suite de
  conformité : execution terrain constatee) + gabarit générateur aligné.
- Mis à jour la documentation d'état : REPRISE_PROJET.md (M0 franchi,
  arborescence avec m0/, table D1-D26, section 7 réécrite : procès-verbal M0
  + checklist de démarrage M1 avec décision de continuité des clés) ;
  PLAN_MILESTONES.md (état M0 franchi) ; README.md (D1-D26, état du projet).
- Complété le présent journal : entrées 13 et 14 consignées a posteriori
  (les sessions correspondantes n'avaient pas étendu le journal — écart de
  gouvernance corrigé, mentions « a posteriori » explicites).
- Complété la synthèse du journal des décisions dans le PDF formel
  (scripts/spec_v040/sec-d.tex) : D25 (chaîne LaTeX/Tectonic) et D26 (jalon M0
  franchi) désormais mentionnées — l'archive formelle reflète son propre état.
- Sauvegarde systématique finale (D13/D17) : régénération du PDF formel
  (DECISIONS.md modifiée + synthèse .tex), commits 12ee6d8 et 68e62f7,
  synchro Drive, push GitHub.

Stage Summary:
- M0 FRANCHI le 26 octobre 2026 : notation -> octets -> PE32+ -> exécution
  prouvée de bout en bout sans compilateur, carte signée, verrou croisé
  fail-closed, 1 536 octets < 4 Kio. Le jalon existentiel est acquis — le
  paradigme tient.
- L'architecture de continuité D11 a fonctionné en conditions réelles :
  GitHub + Drive ont survécu à la perte du bac à sable, restauration complète
  par fetch/reset, empreinte d'artefact vérifiée.
- Point d'attention pour M1 : m0/.keys/ (phrase maîtresse, graine Ed25519)
  est local par conception et absent du dépôt — au démarrage de M1, choisir
  entre restauration depuis le coffre du développeur ou régénération
  (reconstruction documentée, D26) ; consigner le choix.
- Prochaine étape : jalon M1 (mini-libc scellée, première cristallisation,
  adresses stables, première mesure des budgets tokens).

---
Task ID: 16
Agent: main (Z.ai, agent principal)
Task: Terminer le jalon M1 — cristallisation, suite de conformité, instrumentation
des budgets, scellage rc.1 et export de continuité — après reprise sur troisième
réinitialisation du bac à sable.

Work Log:
- Restauré l'état complet depuis la sauvegarde D11 : clone du bundle Drive
  (méthode A de REPRISE 4.1), jetons .gdrive/ (dossier Tokens), remote GitHub
  reconfigurée (dépôt synchronisé à c003ea3), environnement Python recréé
  (keystone, capstone, unicorn, pynacl, argon2, cryptography, pefile, tiktoken).
- Corrigé demo_r7.py (bug d'offset : le .rdata de hello.exe vit à 0x400 en M0,
  pas 0x1200 — la comparaison lisait hors bornes) ; la démonstration R7 passe
  alors intégralement : blocs dev.1 octet-identiques à la même adresse en dev.2,
  io hérités octet-identiques à hello.exe, memset entré exclusivement dans la
  réserve int3, structures PE inchangées — verdict R7 DÉMONTRÉ.
- D30 consignée (troisième réinitialisation, D27 réappliquée) : régénération de
  triade/.keys/, rebuild M0 et M1 — hello.exe byte-identique (c89e330c…507f2) et
  selftest.exe byte-identique (8038585b…f3c0), preuve que les secrets perdus
  n'étaient que l'enveloppe chiffrée ; compteurs de cristallisation repartis à 1.
- Écrit conformite_profil.py (suite de conformité du profil § 8.2, D22) :
  68 contrôles constatés depuis l'artefact scellé — ISA/boutisme (structures
  .rdata décodées little-endian), ABI msx64 (non-volatils poussés avant écriture,
  shadow space >= 0x28, aucune référence sous RSP, piles équilibrées, args
  volatils), PE32+ (protections, sections, BASERELOC, entrée zone app), interface
  IAT (imports exacts, appels indirects vers les 3 slots uniquement, zéro
  syscall, zéro movabs hors image), notation (round-trip + identité WYSIWYG +
  corpus M0 exact) et granularité/padding (slots D28, NOP intra-slot, réserve
  int3, démo R7 dynamique). Élément 5 (patch à chaud) rapporté hors périmètre M1.
  Verdict : VERTE 68/68.
- Écrit budgets_tokens.py (critère de sortie M1 : première mesure effective) :
  mesure sur la carte scellée déchiffrée et les sources réelles, tokenizer
  tiktoken cl100k_base. Première mesure : localiser 56 tokens — le budget
  normatif de 40 (spec § 4.3/§ 12) est INATTEIGNABLE : le gabarit canonique
  v0.4.0 lui-même mesure 43 tokens. Décision soumise au développeur.
- D31 consignée sur choix du développeur (amender à 64 + alléger) : budget
  localiser 40 -> 64 tokens dans spec/FORMAT_CARTE/manuel agent/sources LaTeX/
  verify_spec ; format frag-loc allégé au gabarit § 4.3 + exe= + role= (zone=
  retiré, dérivable des en-têtes [zones] ; suffixe .exe implicite). Mesure
  finale : localiser 51 / éditer 719 / ajouter 1 086 — conformes (64/3000/6000) ;
  budgets.json consigné avec composition et mesures par bloc.
- Cristallisation R6 exécutée : vérifications graines 4 à 12 (la build graine 3
  ayant posé le premier compteur) — 10/10 sur les onze blocs, chaque exécution
  à 76 010 cas différentiels verts (~1,04 M cas cumulés sur la lignée), oracle
  structurel 134 verrous PASS à chaque passage.
- Scellé 0.2.0-rc.1 (build_m1.py --sceller-rc) : cristallisation complète +
  suite de conformité re-exécutée verte ; tableau de bord final régénéré à rc.1
  (vérification graine 14) avec les trois budgets mesurés.
- Implémenté export_continuite.py (D16, FORMAT_CARTE § 8) : conteneur TRIADE-EXP1
  chiffré XChaCha20-Poly1305 (clé Argon2id+HKDF, contexte distinct de la carte)
  et signé Ed25519 (lignée du projet, vérifiable par la clé publique committée) ;
  contenu I+B+C+manifeste autodescriptif (contrôles d'export consignés) ; oracle
  exclu (D1). Auto-verification d'import (5 étapes § 8.2) au vert ; copie de
  coffre téléversée au racine du dossier Drive + copie download/. m1/export/
  ajouté au .gitignore.
- Documentation alignée : m1/README.md créé (carte d'identité du jalon, résultats,
  procédure de validation terrain rc.1 -> 0.2.0) ; DECISIONS.md D30-D31 ;
  PROTOCOLE_TRIADE.md, FORMAT_CARTE.md, PROTOCOLE_TRIADE_AGENT.md, sources
  spec_v040 (budget amendé) ; REPRISE_PROJET.md et PLAN_MILESTONES.md mis à jour ;
  PDF formel régénéré par la chaîne D17 lors de la sauvegarde systématique.

Stage Summary:
- M1 est à un critère de la fermeture : 0.2.0-rc.1 scellée (cristallisation
  11x10/10, conformité 68/68 verte, budgets mesurés conformes, R7 démontré,
  verrou croisé vert) — reste le constat terrain Windows 11 de selftest.exe
  (21 lignes minilibc OK, code 0) pour basculer la balise en 0.2.0 finale.
- L'instrumentation a fait son travail de révélateur : le budget de localisation
  v0.4.0 était une estimation inatteignable (43 tokens sur le gabarit canonique
  même) — amendé à 64 avec allègement du format (D31, choix développeur).
- La continuité du projet ne dépend plus du poste : l'export de continuité
  chiffré/signé préserve désormais la lignée scellée (compteurs de cristallisation
  compris) dans le coffre Drive — la perte du bac à sable (D30, troisième
  occurrence) ne remettra plus les compteurs à zéro.
- Prochaine étape : validation terrain selftest.exe (développeur), puis M2 —
  patch à chaud sur serveur TCP écho (le jalon de vérité du protocole).

---
Task ID: 17
Agent: main (Z.ai, agent principal)
Task: Fermer le jalon M1 : consigner le constat terrain Windows 11 de selftest.exe
(D32), sceller la balise finale 0.2.0, aligner la documentation et sauvegarder.

Work Log:
- Constat terrain reçu du développeur : `C:\Users\Alek\Downloads>selftest.exe` →
  ligne unique `TRIADE M1 : minilibc 21/21 OK` — exactement la sortie dorée du
  contrat libc-08 Q2 (vecteur V2, N = 21). Erratum détecté au passage :
  REPRISE § 7.2 et m1/README annonçaient « 21 lignes » ; le contrat exige une
  ligne unique « N/21 » — l'artefact fait foi, les documents corrigés (D32).
- D32 consignée au journal des décisions (format normalisé D24) : constat,
  scellage final, anti-rollback étendu, erratum.
- Implémenté `build_m1.py --sceller-final` (modèle de sceller_rc) : exige
  cristallisation 10/10 + conformité § 8.2 verte + balise rc.1 exactement une
  fois dans frag-bld (fail-closed), bascule version → 0.2.0, re-scellage des
  quatre fragments, re-signature Ed25519. VERSION_FINALE ajoutée à layout.py.
- Corrigé l'angle mort anti-rollback de construire() : la reconstruction était
  refusée pour les balises -rc.N mais pas pour une balise finale X.Y.Z — le
  contrôle refuse désormais toute balise scellée (rc ou finale).
- Scellage final exécuté : conformité re-exécutée VERTE 68/68, balise 0.2.0
  scellée. Budgets re-mesurés (obligation D31 à chaque scellage) : localiser 51
  / éditer 719 / ajouter 1 088 (cibles 64/3000/6000) — CONFORME (dérive +2 tok
  sur ajouter, marge inchangée).
- Ré-vérifications post-scellage : graines 15 et 16 — oracle différentiel
  76 010 cas verts, binaire émulé sortie exacte + code 0 (Q3 reconfirmé),
  134 verrous, cristallisation 10/10 partout, verrou croisé : 11 empreintes
  conformes, artefact 0.2.0. Tableau de bord régénéré (version=0.2.0, D27 à
  D32 consignées, graine 16).
- Export de continuité régénéré sur la lignée 0.2.0 : conteneur
  TRIADE-continuite-0.2.0-20261026T121243Z.bin (81 109 o, chiffré + signé),
  import 5 étapes auto-vérifié OK ; coffre téléversé au racine du Drive +
  copie download/.
- Documentation alignée : DECISIONS.md (D32), m1/README.md (statut 0.2.0,
  PV PASS, erratum), REPRISE_PROJET.md (état, § 2/3.2/6/7/9 — M2 devient
  l'étape en cours), PLAN_MILESTONES.md (M1 franchi), README.md racine,
  sec-d.tex (synthèse D32 — PDF formel régénéré par la chaîne D17 à la
  sauvegarde).
- Sauvegarde systématique : sync_backup.sh (commit + Drive + GitHub).

Stage Summary:
- M1 FRANCHI le 26/10/2026 : balise finale 0.2.0 scellée et immuable (§ 9).
  Les quatre critères + conditions transverses + validation terrain sont
  acquis ; défaut ultérieur → 0.2.1 à contrat stable (R4).
- La sortie terrain correspondait au contrat à la lettre (ligne unique 21/21
  OK) ; l'écart était dans la documentation (« 21 lignes »), corrigé et
  consigné — le contrat et l'artefact font foi.
- Bonus du scellage final : trou anti-rollback comblé (les balises finales
  sont désormais refusées à la reconstruction, fail-closed).
- Prochaine étape : M2 — patch à chaud sur serveur TCP écho (le jalon de
  vérité) ; premier chantier : specs I des blocs réseau/threads/trampoline,
  écrites avant notation, plan d'adressage étendu (D28).

---
Task ID: 18
Agent: main (Z.ai, agent principal)
Task: Exécuter le premier build M2 (dev.1) laissé en attente par D33 — consigner
les verdicts réels de la chaîne build/oracle/carte, corriger ce que l'oracle
refuse, sceller dev.1.

Work Log:
- Exécuté `build_m2.py --phase 1` sur l'état commité e7c5bb8 : ÉCHEC fail-closed
  sur l'oracle C1 (console) — journal `commande refusee\r` sans LF + rollback
  non reconnu. La chaîne avait fonctionné exactement comme prévu : round-trips
  R5 19/19 à 100 %, oracle structurel 304 verrous verts, PE composé — puis
  l'émulation a refusé le comportement. Premier verdict réel du jalon de vérité.
- Audit systématique des chaînes .rdata (scripts/audit_rdata_m2.py) : cause
  racine = arithmétique « caractères + CR » oubliant le LF. HUIT constantes
  fausses (tcp-10 : PATCH_OK 28→29, REFUS 17→18, CMD_RB r8d 9→10, cmp r12
  9→10, RB_OK 26→27 ; tcp-12 : CONNEXION 19→20, ERREUR 21→22, ARRET 6→7) et
  l'erreur remontait à la couche I : la spec tcp-10:R1 elle-même portait
  « rollback\r\n » (n=9) — erratum consigné dans la spec (n=10, fixture D20
  inchangée, aucun contrat scellé touché).
- Deuxièmes et troisièmes défauts découverts par le garde-fou : les écarts RVA
  du layout avaient été dimensionnés avec les longueurs fausses — le NUL
  terminal de MSG_CONNEXION écrasait MSG_ECHO[0], celui de CMD_RB écrasait
  CMD_QUIT[0] (masqués par l'ordre des `poser` : exactitude accidentelle).
  Correction : MSG_CRLF 0x266A→0x2665, MSG_ECHO 0x2664→0x2668, CMD_QUIT
  0x2742→0x2748 ; l'ajout du garde-fou de chevauchement dans `poser` (toute
  pose recouvrante désormais refusée) a ensuite attrapé une TROISIÈME
  collision préexistante : R_HN_GSH 0x2078→0x2079 (NUL de "kernel32.dll\0").
  Notations tcp-09/tcp-10/tcp-12 régénérées par outils/auteur.py.
- Quatrième défaut (oracle, erratum) : le test binaire attendait les threads
  console/connexion en RVA (0x4980, 0x4800) alors que tcp-12 passe des
  adresses ABSOLUES (lea rip + bloc, position-indépendance D33) — CreateThread
  reçoit des VA réelles sous Windows. Attente corrigée (IMAGE + RVA).
- Cinquième défaut (le plus grave, couche C) : la porte R10 de tcp-12
  confondait l'entrée staging (taille 0 en dev.1) avec le terminateur de la
  table — LA PORTE NE VÉRIFIAIT AUCUN BLOC. Corrigé selon le contrat Q1
  (« pour chaque entrée de taille non nulle ») : terminaison sur RVA=0,
  saut des entrées de taille nulle (.entree_suivante), boucle de somme
  gardée. tcp-12 : 464→468 o.
- Sixième défaut (oracle, erratum de portée physique) : le test R10 cible
  0x1800 (la porte elle-même) et exige le message KO — mais une porte brisée
  dans son propre prologue ne peut pas témoigner (le flip transformait
  `sub rsp,0x60` en `add [rbx],0x60`, mort avant tout effet). Erratum V3
  consigné dans la spec tcp-12 : pour son propre slot, le garant testable est
  « morte avant tout effet » (aucun ws2, aucun journal) ; le verdict formel
  reste porté par l'oracle externe (D1). Les cinq autres cibles produisent
  toutes KO + code 1 + zéro appel ws2.
- Septième et huitième défauts (outils) : KeyError c30012 dans fragments_clairs
  (le cas libc-09-non-embarqué était codé APRÈS la recherche dans le
  dictionnaire des artefacts hérités — inatteignable ; ordre inversé) ;
  tableau de bord écrit en ascii alors qu'il contient des accents (UTF-8).
- Rebuild final : VERTE. Oracle différentiel 38 522 cas verts, mécanique de
  patch vérifiée (remplaçant en attente, refus 2 en session), falsification
  18/18 corruptions détectées, porte R10 6/6 cibles + version < plancher
  refusée, 305 verrous structurels, R7 : 6 blocs hérités octet-identiques.
  Carte génération 2 écrite (4 fragments chiffrés, signature Ed25519, 25
  blocs sur 3 artefacts), verrou croisé OK (24 empreintes).
- Artefact scellé : echo.exe 15 360 o, sha256
  c214bf68fd44aca8d80481cebe21fe0a331e49ce35e75d176650213bd5815bc7,
  version 0.3.0-dev.1.

Stage Summary:
- M2 dev.1 ACQUIS : le premier build du jalon de vérité a refusé l'état
  commité, forcé huit corrections traçables (1 erratum de spec, 8 constantes,
  3 RVA, 1 porte R10 réparée, 2 errata d'oracle, 2 corrections d'outils) puis
  rendu son verdict vert — la boucle de mise à jour § 5 a fonctionné sur du
  code vivant dès sa première exécution.
- Leçon protocole (matière d'évaluation D34) : trois des huit défauts étaient
  invisibles sans exécution (ordre des poser masquant les collisions, porte
  court-circuitée, self-corruption de porte) — « le protocole ne promet pas,
  il vérifie » s'applique aussi au vérificateur : l'oracle a dû corriger ses
  propres attentes (RVA vs VA, self-test de porte) là où la physique
  l'exigeait.
- Garde-fou ajouté : chevauchement .rdata refusé au build (poser) — la classe
  de défaut « NUL débordant » ne peut plus se reproduire silencieusement.
- Prochaine étape : dev.2 — diff I tcp-08:R1→R2 (majuscules), brouillon
  echo-01-v2, `--phase 2` (boucle § 5 : AUCUN octet de code ne bouge, R7),
  puis cristallisation R8 multi-graines.
