# JOURNAL DES DÉCISIONS — Projet TRIADE

> Toute décision structurante est consignée ici avec ses alternatives rejetées et sa
> justification rattachée à la fonction objectif (Sécurité > Performance > Optimisation >
> Coût en tokens). Ce journal est la mémoire des arbitrages : toute révision future doit
> soit respecter ces décisions, soit expliciter précisément ce qui les invalide. Rien ne
> se change en silence.

## Décisions de la v0.2 (D1–D10, 25 octobre 2026)

| ID | Décision | Choix retenu | Alternatives rejetées |
|---|---|---|---|
| D1 | Oracle de vérification | Éphémère et obligatoire : régénéré à chaque session depuis la couche I, détruit après usage | Oracle persistant versionné ; aucun oracle (confiance aveugle) |
| D2 | Notation | keystone (assemblage) + capstone (round-trip), in-process, granularité instruction | nasm -f bin ; écriture directe des octets à la main |
| D3 | Couche I | Contrats légers : signatures typées, pré/post-conditions, invariants | Spécification formelle lourde (TLA+, Alloy) |
| D4 | Crypto de la carte | Ed25519 (signature) + XChaCha20-Poly1305 (repos) + Argon2id (dérivation) | AES-GCM ; clés dérivées par SHA-256 nu |
| D5 | Verrou croisé | SHA-256 par bloc scellé + carte signée en entier, vérifiés avant chaque édition et au chargement | Signature du seul binaire |
| D6 | Empreintes par build | Variante unique par livraison : réordonnancement, nops, encodages équivalents | Binaire identique pour tous les destinataires |
| D7 | Appels système | API Windows via IAT (kernel32, ws2_32, Schannel) | Syscalls directs avec table par build de Windows |
| D8 | Granularité des blocs | 32 à 512 instructions, un bloc = une responsabilité, padding de 16 octets ; budgets 40/200 tokens | Micro-blocs (1–8 instructions) ; méga-blocs (plusieurs milliers) |
| D9 | TLS | Schannel (SSPI) au jalon M4 | TLS 1.3 pur implémenté en blocs scellés (reporté en objectif post-M5) |
| D10 | Cible | x86-64, Windows 11, PE32+ écrit à la main, DEP/ASLR/CFG respectés | RISC-V sous QEMU ; x86-64 Linux |

### Développements

**D1 — Oracle éphémère.** Pivot du compromis entre le « 100 % code machine » exigé pour
l'artefact et la sûreté d'exécution. L'implémentation de référence — triviale, lente,
écrite dans un langage sûr — ne sort jamais du laboratoire : elle est régénérée à chaque
session puis détruite. Elle ne dégrade donc ni la performance ni la pureté de l'artefact
livré, tout en attrapant les corruptions mémoire avant le scellage. Sur le plan du coût en
tokens, elle est rentable : régénérer un oracle trivial coûte moins cher que de traquer
une corruption silencieuse dans un binaire déjà scellé.

**D2 — Notation, pas compilateur.** keystone et capstone forment le couple d'assemblage
et de désassemblage de référence : granularité instruction et contrôle octet par octet en
processus, sans fichier objet intermédiaire. Nuance capitale : cette notation n'est pas un
compilateur — aucune optimisation, aucune décision de réécriture ne s'intercale entre ce
que l'agent écrit et les octets produits. Le principe WYSIWYG est préservé intégralement,
et l'artefact demeure le couple octets + carte. nasm en mode binaire plat reste le repli
pour les encodages exotiques que keystone ne saurait pas produire.

**D5 — Verrou croisé.** Répond à la menace spécifique de l'empoisonnement de carte : un
attaquant qui falsifierait les métadonnées ferait travailler l'agent sur des informations
fausses, et pourrait lui faire introduire une porte dérobée en croyant respecter les
contrats. Contre-mesure bilatérale : la carte porte le SHA-256 de chaque bloc scellé, et
la carte entière est signée Ed25519. L'agent refuse toute carte non signée et tout binaire
dont les empreintes divergent ; le binaire, de son côté, vérifie ses propres checksums au
chargement et s'arrête proprement en cas d'écart.

**D7 — IAT plutôt que syscalls.** Les syscalls directs exigeraient une table de numéros
par build de Windows — c'est-à-dire une carte cachée supplémentaire, fragile et coûteuse à
maintenir — pour un gain relevant de la furtivité, hors du périmètre des jalons M0 à M4.
Les appels via l'IAT préservent la compatibilité entre builds et respectent l'ASLR.

## Décisions d'infrastructure (D11–D13, 25 octobre 2026)

| ID | Décision | Choix retenu | Alternatives rejetées |
|---|---|---|---|
| D11 | Architecture de sauvegarde | Git local (source de vérité) + Google Drive (miroir des fichiers + bundle d'historique dans le sous-dossier TRIADE/) + repo GitHub privé | Dépôt Drive seul ; repo GitHub seul ; copie brute du répertoire .git sur le Drive |
| D12 | Gestion des jetons | Stockés dans `triade/.gdrive/` (permissions 600, exclus du dépôt et des synchronisations, jamais affichés) ; récupérés une fois depuis le Drive | Jetons commités dans le dépôt ; jetons dans des variables d'environnement persistées |
| D13 | Sauvegarde systématique | `scripts/sync_backup.sh "message"` après chaque modification ; hook `post-commit` déclenchant la synchro Drive à chaque commit ; push GitHub automatique si remote configurée | Sauvegardes manuelles ponctuelles ; synchronisation par lot en fin de session |

### Développements

**D11 — Trois copies complémentaires.** Le dépôt git local est la source de vérité : c'est
le seul endroit où l'historique est complet et où les opérations atomiques (commit,
rollback) sont natives. Le Drive porte un double miroir : les fichiers en clair
(parcourables depuis n'importe quel navigateur) et `triade-history.bundle`, un bundle git
complet qui permet une restauration intégrale (`git clone triade-history.bundle`) y compris
après perte du poste local. GitHub ajoute un miroir distant versionné, priviligiant la
sécurité par un repo privé. La copie brute du répertoire `.git` a été écartée : fichiers
verrous non cohérents hors d'un système de fichiers local, et restauration non garantie.

**D12 — Jetons confinés.** Les jetons (OAuth Google Drive, GitHub, compte de service)
sont la seule partie du projet qui ne doit JAMAIS figurer dans le dépôt, le bundle ou le
miroir Drive du projet. Ils vivent dans `.gdrive/`, couvert par `.gitignore`, permissions
600. Le script `check_auth.py` permet de les vérifier sans jamais les afficher.
Avertissement maintenu : les jetons ont transité par un dossier Drive partagé par lien —
restreindre le partage ou supprimer les fichiers après vérification (voir
`REPRISE_PROJET.md` § 8).

**D13 — Systématique et idempotente.** La sauvegarde est déclenchée à deux niveaux : le
hook `post-commit` synchronise le Drive à chaque commit (y compris manuel), et
`sync_backup.sh` orchestre la séquence complète commit + Drive + GitHub. La synchronisation
est idempotente (comparaison des empreintes MD5 avant tout transfert) : un double appel ne
coûte rien. Cette redondance est volontaire : elle couvre le cas d'un hook absent (clone
frais), désactivé ou contourné.

## Décisions de la v0.3 (D14–D16, 25 octobre 2026)

| ID | Décision | Choix retenu | Alternatives rejetées |
|---|---|---|---|
| D14 | Universalité | Profils de cible : le cœur du protocole est indépendant de la cible ; chaque plateforme est une instanciation vérifiable de sept éléments (ISA/types, ABI, format, interface système, patch à chaud, notation, padding) ; Windows 11 x86-64 reste le profil primaire de validation | Cibles multiples codées en dur dans le protocole ; couche d'abstraction logicielle « portable » (trahit la fonction objectif Performance) ; rester mono-cible (D10 initial, amendé) |
| D15 | Suite cryptographique | Paramétrable : `algo_hachage` (défaut sha256), `algo_signature` (défaut ed25519), `algo_chiffrement` (défaut xchacha20poly1305) — modifiables par le développeur dans des listes blanches ; choix consigné dans l'en-tête signé de la carte ; empreintes au format préfixé ; changement en cours de projet = re-cryptage atomique | SHA-256 et suite figés ; liberté totale sans liste blanche (affaiblissement possible, contraire à la fonction objectif) |
| D16 | Récupération de la carte | Export de continuité : conteneur unique chiffré (AEAD + Argon2id) et signé, regroupant I, B, C et un manifeste autodescriptif ; procédure d'import en cinq étapes ; l'oracle, éphémère, n'est jamais exporté ; précise R1 — l'interdiction porte sur la livraison avec l'artefact, pas sur la propriété du développeur | Carte non exportable (enfermement de l'agent et du projet) ; export en clair ; export non signé ; export incluant l'oracle |

### Développements

**D14 — Universalité par profils.** L'universalité exigée est structurelle, pas
opportuniste. Le cœur du protocole (règles R1-R10, boucle de mise à jour, vérification) ne
mentionne aucune plateforme — la v0.2 le savait déjà, mais liait la cible au protocole par
D10. D14 amende D10 : la cible Windows 11 x86-64 reste le profil primaire de validation
(l'application pentest y court, jalons M0-M5), mais cesse d'être une limite du protocole.
Exiger sept éléments par profil rend l'extension vérifiable plutôt que déclarative : un
profil incomplet est refusé, exactement comme un build sans carte. La couche I, indépendante
de la cible, s'écrit une fois ; la carte indexe par profil ; chaque profil possède son
binaire et ses empreintes de build. Conséquence sur la feuille de route : M6 change l'OS à
ISA constante, M7 change d'ISA — l'ordre isole chaque variable, et l'oracle, dérivé de I,
valide les blocs de tous les profils sans coût supplémentaire. L'alternative d'une couche
d'abstraction logicielle (bytecode portable, machine virtuelle) est rejetée parce qu'elle
réintroduirait précisément la couche d'exécution intermédiaire que le protocole existe pour
supprimer.

**D15 — Cryptographie paramétrable sous seuil.** La demande de modifiabilité est légitime
— conformité réglementaire (FIPS 140-3, CNSA), résistance anticipée (SHA-3, BLAKE3),
performance (BLAKE3 sur les très gros blocs) — mais une liberté totale ouvrirait la porte
à un affaiblissement contraire à la fonction objectif : un développeur pressé choisissant
MD5 casserait le verrou croisé pour tous les agents qui suivraient. La liste blanche
réconcilie les deux exigences : la volonté du développeur s'exerce entre algorithmes
conformes au seuil (128 bits minimum, collision-résistants, AEAD authentifiés, signatures
déterministes ou hedged). Le choix est consigné dans l'en-tête de la carte, signé avec
elle, et les empreintes sont préfixées (`sha256:…`) : la carte reste autodescriptive pour
tout agent, présent ou futur, et une migration reste lisible par les outils antérieurs. Le
changement en cours de projet est possible par re-cryptage complet — atomique, journalisé,
avec archivage de l'ancienne carte. La dérivation Argon2id n'est pas paramétrable : ses
paramètres de coût sont des planchers, ajustables à la hausse seulement.

**D16 — Export de continuité.** L'interdiction de livraison visait l'artefact destiné aux
tiers, pas la propriété du développeur sur son état de travail. Sans mécanisme de
récupération, la règle créait un enfermement : le projet ne survivrait ni au changement
d'agent, ni au changement de poste — une dépendance inacceptable envers l'outil qui a
généré la carte. L'export de continuité rétablit l'équilibre : chiffré intégralement, il
peut être stocké n'importe où sans exposer la carte ; signé, il est vérifiable à l'import ;
autodescriptif (manifeste : version, suite cryptographique, profils, empreinte racine), il
ne requiert aucune connaissance extérieure. L'oracle est volontairement exclu : éphémère
par conception (D1), il est régénéré depuis I à l'arrivée — l'export n'embarque ainsi aucun
artefact empoisonnable persistant. La procédure d'import en cinq étapes (déchiffrement,
signature, verrou croisé, oracle, reprise) applique au transfert les mêmes garde-fous qu'à
l'édition : rien n'est interprété avant vérification, et l'échec d'une étape est terminal.

## Décision D17 — PDF formel régénéré systématiquement (25 octobre 2026)

| ID | Décision | Choix retenu | Alternatives rejetées |
|---|---|---|---|
| D17 | PDF formel du protocole | `scripts/build_pdf.sh` : empreinte SHA-256 des sources (PROTOCOLE_TRIADE.md, FORMAT_CARTE.md, DECISIONS.md, PLAN_MILESTONES.md, script générateur, couverture) comparée au stamp `.pdf_build.stamp` suivi par git ; toute divergence déclenche la reconstruction complète (validation couverture, rendu vectoriel, corps ReportLab, contrôles qualité) ; intégré à `sync_backup.sh` **avant** le commit — la sauvegarde embarque toujours un PDF synchrone des sources | Régénération manuelle à la demande (risque d'oubli, PDF périmé dans le dépôt) ; génération dans le hook post-commit (trop tard : le commit contiendrait l'ancien PDF, et un échec de build bloquerait la synchro Drive) ; comparaison par dates (mtime : faux positifs au clone et faux négatifs en cas de revert) |

**Développement.** Le PDF de spécification est un artefact dérivé : sa source de vérité
est le markdown du protocole. Laissé à une régénération manuelle, il diverge
inévitablement des sources — un agent reprendrait le projet sur une spécification
périmée, exactement le genre de dérive silencieuse que la gouvernance du projet
interdit. Le mécanisme retenu est volontairement simple et vérifiable : le stamp
contient l'empreinte des sources au moment du dernier build ; il est commité avec le
PDF, si bien qu'un clone frais ne reconstruit pas inutilement (empreintes identiques),
tandis que toute modification réelle d'une source déclenche la reconstruction au
prochain `sync_backup.sh`. La reconstruction échoue bruyamment (validateurs de
couverture, contrôle `pdf_qa`) sans bloquer la sauvegarde des sources : le markdown
est toujours sauvegardé, le PDF retardé est signalé. La même session a corrigé un
défaut latent de numérotation hérité du générateur v0.2 (pieds de page du sommaire :
séquence i, 1, 2, 2 au lieu de i, ii, 1, 2) — l'archive v0.2 a été régénérée à
l'identique (erratum, contenu inchangé) et le générateur v0.3 gèle désormais la valeur
entre les deux phases de construction.

## Décision D18 — Édition académique du protocole : article de recherche v0.4 (26 octobre 2026)

| ID | Décision | Choix retenu | Alternatives rejetées |
|---|---|---|---|
| D18 | Restructuration académique du document du protocole | Réécrire la présentation du protocole en article de recherche IMRAD (`docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf`, 12 p.) : formalisation des couches I/B/C, du verrou croisé (prédicat de cohérence κ), de la fonction objectif lexicographique (ordre ≻_lex) et des règles en système de transitions ; section travaux connexes (dette technique, Design by Contract, AISE) ; étude de cas RoomEq reprise avec questions de recherche et design monocasal déclaré ; menaces sur la validité (Wohlin) dont l'écart conceptuel refactorisation source / génération binaire native ; rapport de vérification interne avant empaquetage (`docs/VERIFICATION_v0.4_Article.md`). Sources LaTeX conservées dans `scripts/article_v04/` (main.tex + 7 sections + refs.bib + cover.html Template 03 + merge_cover.py + verify_article.py) ; régénération manuelle, hors D17. Le noyau normatif du protocole est inchangé — la numérotation v0.4 désigne l'édition du document, le contenu normatif reste celui de la v0.3 | Réviser la spécification v0.3 elle-même (aucun mécanisme nouveau à spécifier : la formalisation est une présentation, pas un changement de règles) ; publier en anglais (la série documentaire du projet est francophone ; les équivalents académiques sont donnés aux premières occurrences) ; intégrer l'article au périmètre D17 (le PDF formel régénéré automatiquement reste la spécification ; l'article, comme la démonstration, se régénère manuellement) |

**Développement.** L'édition académique répond à une évaluation externe du
PDF de démonstration v0.3, qui recommandait de porter le document aux
standards d'un article de recherche de premier plan. La réécriture
restructure sans changer les faits : chaque affirmation de la démonstration
est soit reprise avec sa source (tableaux de mesures), soit explicitement
nuancée dans les menaces sur la validité — le changement de niveau de preuve
le plus important étant la distinction désormais verrouillée entre ce que
l'étude de cas établit (la couche de gouvernance du protocole appliquée à
une instanciation source de la couche B) et ce qu'elle ne prouve pas (le
cœur natif : notation, round-trip, patch à chaud, jalons M0–M7 ouverts ;
les budgets en tokens restent des cibles, pas des mesures). Deux
enseignements issus de la démonstration entrent dans le corps du texte
comme contributions : la cristallisation à pré-versions (-dev.N) et les
reverse-specs. La vérification préalable à l'empaquetage est scriptée
(`verify_article.py` : 44 contrôles — terminologie, structure IMRAD,
références croisées, flottants, anglicismes) et consignée dans
`docs/VERIFICATION_v0.4_Article.md` ; les avertissements résiduels y sont
justifiés un par un (faux positifs bicolonne, typographie française).

## Mode de gouvernance

Une nouvelle décision reçoit l'ID suivant la séquence (D18, D19, ...), la date, le choix
retenu, les alternatives rejetées et un développement si elle engage l'architecture. Une
décision ne se modifie jamais en silence : la révision remplace l'entrée par une note
d'invalidation explicite référençant la décision qui la supplante — D14 (amende D10) et
D15 (amende D5) illustrent la procédure.

## Décisions de la v0.4.0 (D19–D24, 26 octobre 2026) — format normalisé § 15.1 de la spécification

> La révision v0.4.0 est une révision de gouvernance vérifiée : elle convertit en normes les
> pratiques nées de la démonstration RoomEq, étend le modèle de menace et renforce R10, sans
> toucher à la hiérarchie de la fonction objectif ni affaiblir une seule règle. Les entrées
> ci-dessous appliquent le format normalisé défini par D24 (elles font foi pour les entrées
> futures ; les entrées D1–D18 restent au format historique, valide).

### D19 — Couche I normalisée et taxonomie des défauts ; hiérarchie verrouillée

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : la v0.3 décrivait la couche I comme « contrats légers » sans gabarit ; la
  démonstration RoomEq a fixé une pratique (44 spécifications avant le code) et révélé une
  classe récurrente de défauts (contrat non écrit) méritant une taxonomie. Le cahier de
  révision exige par ailleurs que la hiérarchie de la fonction objectif ne soit pas modifiée.
- **Choix retenu** : gabarit normalisé de spécification I (identifiants stables `<DOM>-<NN>`,
  intention, contrat pre/post/inv, cas d'échec nommés, vecteurs de vérification, fixtures,
  provenance, décisions) ; taxonomie T1–T6 des défauts de contrat non écrit avec détecteurs
  et verrous ; la hiérarchie Sécurité > Performance > Optimisation > Coût en tokens devient
  un **invariant de révision** — aucune révision future ne peut la modifier sans invalider
  le protocole entier.
- **Alternatives rejetées** : spécification formelle lourde (TLA+, Alloy — déjà rejetée par
  D3, la légèreté est maintenue) ; gabarit libre par projet (l'expérience montre que sans
  structure, les cas d'échec et les vecteurs ne sont pas écrits) ; modification de la
  hiérarchie (interdite par le cahier de révision, et contraire à l'identité du protocole).
- **Développement** : le gabarit est diffable par construction (une exigence par phrase
  numérotée), ce qui sert directement R2 ; la taxonomie alimente le tableau de bord
  (métrique « défauts ouverts par classe ») et la liste de contrôle de rédaction. Les
  occurrences de référence viennent de la démonstration : seuil 8 (T1+T6), SP_DEVINFO_DATA
  (T2), sanitisation dépendante de l'hôte (T3), parsing pnputil (T4+T5).

### D20 — Menace étendue et R10 renforcée

- **Statut** : active (renforce R10 sans l'amender : l'énoncé v0.3 est un cas particulier
  du nouvel énoncé) · **Date** : 26 octobre 2026
- **Contexte** : le cahier de révision exige un threat model minimal couvrant binaire
  altéré, carte corrompue, rollback non autorisé, agent défaillant, données embarquées
  modifiées et environnement non conforme — et un renforcement de R10 (checksums,
  signature, anti-rollback, fail-closed explicite).
- **Choix retenu** : six menaces ajoutées au modèle (les sept de la v0.3 sont conservées) ;
  R10 devient « échec contrôlé intégré » : checksums par bloc, signature du manifeste de
  build couvrant code et données embarquées, monotonie de version (anti-rollback),
  contrôles de conformité de l'environnement — tout avant l'entrée en exécution, arrêt
  propre immédiat, aucun chemin dégradé. La vérification est strictement locale.
- **Alternatives rejetées** : anti-rollback par contrôle en ligne (le chargement doit
  échouer proprement hors ligne — dépendance réseau interdite) ; exécution en mode dégradé
  après avertissement (violerait fail-closed et la fonction objectif Sécurité) ; extension
  du modèle aux menaces physiques (hors périmètre d'un protocole logiciel).
- **Développement** : la politique précise anti-rollback (registre des versions acceptées,
  stockage du plancher) appartient au profil — c'est le huitième livrable du profil (§ 14).
  Les données embarquées étaient déjà couvertes en pratique par la démonstration (empreintes
  md5 des bibliothèques) : la norme généralise la pratique.

### D21 — R11 optimisation mesurée et journal d'optimisation

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : l'ordre lexicographique place l'optimisation au troisième rang, mais la
  v0.3 n'interdisait pas explicitement l'optimisation prématurée ; la démonstration a
  éprouvé le cas (demande d'« optimisation maximale », honorée par la mesure puis refusée
  comme transformation — décision D15 du dépôt RoomEq).
- **Choix retenu** : règle R11 — toute optimisation exige un hot path identifié par mesure,
  une mesure avant/après consignée et un contrat stable ; l'optimisation prématurée est
  interdite, sa demande refusée et consignée. Instrument : journal d'optimisation au format
  OPT-NN, versionné avec la couche I.
- **Alternatives rejetées** : laisser l'interdiction implicite (l'ordre lexicographique ne
  dit pas quand mesurer) ; autoriser l'optimisation sans mesure sur les blocs cristallisés
  (un bloc cristallisé est précisément celui qu'on ne touche pas sans procédure lourde) ;
  journal facultatif (une exigence non tracée est une exigence affaiblie).
- **Développement** : R11 sanctionne le commit, pas l'intention — la demande peut être
  examinée et refusée sans coût, c'est son écriture permanente qui est gardée. L'entrée de
  référence est la mesure RoomEq : 152× le temps réel, zéro allocation par bloc —
  l'absence de problème de performance est un résultat, pas un échec de l'optimisation.

### D22 — Suite de conformité par profil et parité inter-profils

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : la v0.3 rend l'extension vérifiable (sept éléments par profil, D14) mais
  ne fixe ni suite de tests par profil ni définition formelle de la parité inter-profils —
  les critères M6/M7 étaient dispersés dans la feuille de route.
- **Choix retenu** : chaque profil embarque une suite de conformité vérifiant ses sept
  éléments (ISA/types, ABI, format et protections, interface système, patch à chaud,
  notation, padding) ; un profil sans suite verte n'est pas déclarable supporté. La parité
  inter-profils se définit à contrat constant : même spécification I (à la paramétrisation
  près), oracle mutualisé vert sur les deux profils, verdicts équivalents sur les vecteurs,
  différences documentées dans frag-con — elle se vérifie par exécution, jamais par
  déduction.
- **Alternatives rejetées** : couche d'abstraction pour obtenir la parité « gratuitement »
  (bytecode portable, machine virtuelle — trahirait la fonction objectif Performance,
  déjà rejetée par D14) ; déclaration de support sur inspection (une propriété non
  exécutée n'est pas une propriété) ; parité au niveau octet (les profils diffèrent par
  construction — la parité est au niveau des verdicts).
- **Développement** : la suite est exécutée à chaque cristallisation rc et finale sur le
  profil concerné ; elle devient le critère d'acceptation explicite de M6 et M7 (critères
  de sortie mis à jour dans PLAN_MILESTONES.md, conditions transverses ajoutées).

### D23 — Officialisation des pratiques nées de la démonstration

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : trois pratiques inventées pendant le recodage RoomEq n'existaient pas dans
  la spécification : les reverse-specs (spécifications extraites de l'installateur scellé,
  décision D11 du dépôt), les pré-versions de cristallisation (`-dev.1` pour distinguer
  « vérifié par l'oracle » de « validé terrain ») et le partage de fixtures entre
  consommateurs d'un même contrat externe (parsing pnputil).
- **Choix retenu** : officialisation intégrale — reverse-specs (gabarit § 2.2 + provenance
  + statut « prête »/« validée » ; le recodage d'un binaire scellé ne peut partir que de sa
  reverse-spec validée) ; pré-versions dev.N / rc.N / X.Y.Z avec monotonie (alimente
  l'anti-rollback de R10), immuabilité des balises et progression de contrat par X.(Y+1).0 ;
  fixtures contractuelles portées par la spécification I, toute copie privée étant un défaut
  T5.
- **Alternatives rejetées** : laisser ces pratiques au rang d'usages (un usage non normé
  diverge d'un projet à l'autre — la démonstration elle-même a dû les inventer faute de
  norme) ; exiger le recodage des binaires hérités (contraire à l'esprit : figer la
  connaissance avant de décider) ; pré-versions rc sans suite de conformité (une candidate
  non conforme à son profil n'est pas une candidate).
- **Développement** : la numérotation du protocole passe à trois segments à partir de la
  présente révision, alignée sur le schéma qu'elle définit ; la séquence RoomEq
  (v3.0.0-dev.1 → v3.0.0 → v3.0.1 → v3.0.2) devient l'occurrence de référence du
  mécanisme « échec honoré, balise immuable, patch à contrat stable ».

### D24 — Traçabilité, journal des décisions normalisé et tableau de bord

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : la traçabilité exigence → bloc → test était implicite ; le journal des
  décisions suivait un format de facto sans être normé ; les indicateurs de santé étaient
  dispersés entre la spécification et la feuille de route.
- **Choix retenu** : table de traçabilité I ↔ C ↔ B ↔ tests obligatoire (champ `spec=` dans
  chaque entrée de carte, audit mécanique, refus de build si maillon manquant — l'exception
  visible étant la reverse-spec « prête ») ; format normalisé du journal des décisions
  (ID, date, statut, contexte, choix, alternatives rejetées, amendements, développement ;
  append-only, pas de rétrodatage) ; tableau de bord de conformité unifié — onze métriques
  mesurables avec cibles et sources, généré par l'audit à chaque commit et cristallisation,
  archivé avec la carte. La norme de fragmentation (« aucune opération ne lit tout ») et la
  localisation par intention (interdiction du balayage) sont consolidées au passage.
- **Alternatives rejetées** : traçabilité par balises de code source (duplication de la
  connaissance — défaut T5) ; journal des décisions en prose libre (le format est la
  condition de l'audit automatique) ; tableau de bord déclaratif (une métrique sans source
  de mesure est une opinion).
- **Développement** : la commande d'audit de traçabilité et le tableau de bord sont
  spécifiés dans FORMAT_CARTE.md § 10 ; les budgets tokens (40 / 3 000 / 6 000) restent
  inchangés et passent du statut de cible à celui de métrique instrumentée dès M1. Les
  entrées D19–D24 appliquent le format normalisé et font foi pour les entrées futures.

### D25 — PDF formel v0.4.0 : chaîne LaTeX/Tectonic

- **Statut** : active (amende D17 sur la mise en œuvre, pas sur le principe) · **Date** :
  26 octobre 2026
- **Contexte** : la v0.4.0 étant une révision majeure de la spécification, le PDF formel de
  la version courante doit être régénéré depuis les nouvelles sources ; la chaîne
  ReportLab du générateur v0.3 (1 603 lignes à adapter) doit être remplacée ou portée.
  L'espace de travail dispose depuis l'édition académique (D18) d'une chaîne
  LaTeX/Tectonic éprouvée (polices Liberation, babel français, listings, fusion pypdf,
  QA complète).
- **Choix retenu** : `scripts/spec_v040/` — manuscrit LaTeX monocolonne avec sommaire
  (main.tex + 4 fichiers de sections), couverture académique Template 03 fusionnée par
  pypdf ; `build_pdf.sh` bascule sur cette chaîne et produit
  `docs/Protocole_TRIADE_v0.4.0_Specification.pdf` (archives v0.2/v0.3 conservées, non
  régénérées) ; la liste des sources du stamp couvre les 4 markdown + les 5 .tex + la
  couverture + le script de fusion.
- **Alternatives rejetées** : portage du générateur ReportLab v0.3 (coût élevé, risque de
  régression, bénéfice nul — la source de vérité reste le markdown) ; génération du PDF
  depuis le markdown par conversion automatique (perte du contrôle typographique :
  sommaire cliquable, tableaux normatifs, listings encadrés) ; abandon du PDF formel
  (contr contraire à D17 : un clone frais doit disposer d'un PDF synchrone des sources).
- **Développement** : le principe de D17 est inchangé — empreinte SHA-256 des sources
  comparée au stamp suivi par git, reconstruction intégrale avant chaque commit, échec
  signalé sans bloquer la sauvegarde des sources. Seule la chaîne de production change.

### D26 — Jalon M0 : chaîne artefact implémentée, validée sur le terrain (M0 franchi)

- **Statut** : active · **Date** : 26 octobre 2026 · **Amendée le** : 26 octobre 2026 (validation terrain)
- **Contexte** : la révision v0.4.0 étant scellée, la feuille de route désigne M0 comme
  prochaine étape — prouver la chaîne notation → octets → PE32+ → exécution sans
  compilateur sur le profil primaire `x86-64-win11-pe`, avec carte v0 signée et verrou
  croisé dès le premier octet (R1-R3, R8-R9).
- **Choix retenu** : mise en œuvre complète dans `m0/` — trois spécifications I au
  gabarit § 2.2 (hello-01/02/03, provenance écrite-avant-code), notation x86-64
  keystone à layout fixe documenté (slots de 64 octets alignés 16, padding inter-blocs
  ≥ 16, déplacements RIP calculés une fois pour toutes puis vérifiés
  **sémantiquement** — aucun post-patching, WYSIWYG intégral), éditeur PE32+ écrit à la
  main (DYNAMICBASE + HIGH_ENTROPY_VA + NX_COMPAT, BASERELOC minimal, imports kernel32
  par IAT : GetStdHandle, WriteFile, ExitProcess, 1 536 octets < 4 Kio, déterministe),
  oracle M0 à deux volets régénéré depuis I (round-trip keystone→capstone→keystone
  100 % + 31 verrous structurels : discipline msx64, appels IAT uniquement, frames
  équilibrés, ud2 défensif, cibles RIP exactes), carte v0 complète (en-tête v0.4.0,
  quatre fragments XChaCha20-Poly1305 par Argon2id 64 Mio/3 it + HKDF par fragment et
  génération, signature Ed25519, empreinte racine), verrou croisé en relecture
  indépendante (fail-closed constaté sur falsification d'octet). Balise d'artefact
  `0.1.0-dev.1` consignée au manifeste frag-bld (schéma § 9 : oracle vert, validation
  terrain en attente).
- **Alternatives rejetées** : post-patching des déplacements après assemblage (casserait
  le WYSIWYG et le round-trip — la notation doit être ce qui s'exécute) ; omettre la
  table de relocalisation (DYNAMICBASE sans BASERELOC : ASLR non honoré, contraire au
  profil) ; exécution locale sous émulation wine (pas le critère M0 — la sortie exige
  Windows 11 réel ; la validation locale multi-outils capstone/pefile/objdump suffit à
  la préparation) ; tag git `v0.1.0-dev.1` (une pré-version de développement est un
  usage interne, la balise d'artefact vit dans frag-bld) ; export de continuité dès M0
  (aucune reprise inter-agents à ce stade — première génération).
- **Développement** : résultats mesurés — round-trip 18/18 instructions (100 %),
  oracle structurel 31 verrous PASS, construction 0 erreur/0 avertissement, artefact
  1 536 octets reproductible (sha256 c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2),
  concordance de trois validateurs indépendants (capstone, pefile, objdump),
  falsification d'un octet de `.text` détectée par le verrou croisé (exit 1).
  Gestion des clés : phrase maîtresse 128 bits générée et mise en coffre côté
  développeur, graine Ed25519 locale, sel Argon2id déterministe documenté (la
  dérivation reste reproductible depuis la seule phrase). Limites assumées : CFG
  différé à M1+ (exige LOAD_CONFIG/GFIDS conçus pour les appels IAT indirects) ;
  oracle différentiel complet reporté à M1 avec la mini-libc (premier terrain de
  cristallisation) ; perte de phrase = reconstruction de carte possible depuis I+B
  (le projet survit, pas l'historique chiffré). Le jalon M0 sera franchi après
  exécution constatée sur Windows 11 (critère de sortie) ; tout écart se corrige en
  `0.1.0+1` à contrat stable (R4).
- **Amendement — validation terrain (26 octobre 2026)** : le développeur a exécuté
  `hello.exe` sur sa machine Windows 11 (interpréteur `cmd`, copie issue du miroir
  Drive `TRIADE/m0/`) ; sortie constatée à l'identique du contrat :
  `TRIADE M0 : Hello, Windows 11 !`, retour au prompt sans incident. Empreinte de
  l'artefact revérifiée localement après restauration du dépôt : sha256
  `c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2`, conforme au
  manifeste frag-bld. Les quatre critères de sortie de M0 sont donc acquis —
  exécution constatée sur Windows 11, round-trip à 100 %, carte signée Ed25519 et
  verrou croisé vérifié, exécutable de 1 536 octets < 4 Kio. **Le jalon M0 est
  franchi** : la chaîne notation → octets → PE32+ → exécution fonctionne de bout en
  bout sans compilateur, le paradigme tient. La balise `0.1.0-dev.1` devient
  candidate à la cristallisation M0 (tag git `v0.1.0` sur demande du développeur,
  R6) ; l'étape suivante est M1 — mini-libc scellée, première cristallisation,
  adresses stables, première mesure effective des budgets tokens. Contrôle
  optionnel laissé au choix du développeur : `echo %ERRORLEVEL%` après exécution
  (attendu : 0).

## Décisions du jalon M1 (D27–D32, 26 octobre 2026)

### D27 — Continuité des clés après réinitialisation du bac à sable : régénération et centralisation

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : deuxième réinitialisation du bac à sable depuis la création du dépôt ;
  les secrets locaux `m0/.keys/` (phrase maîtresse 128 bits, graine Ed25519) sont perdus
  et la carte M0 devient indéchiffrable — le verrou croisé constate l'échec en
  fail-closed, exactement comme prévu. La checklist M1 (REPRISE § 7.2, point 1) exige
  une décision explicite : restaurer depuis le coffre du développeur ou régénérer.
- **Choix retenu** : **régénérer** (option prévue par D26 : « la carte se reconstruit
  depuis I + notation ») et **centraliser** les secrets du projet dans `triade/.keys/`
  (chmod 700/600, `.gitignore`), partagés par toutes les générations de la carte — la
  carte M0 est reconstruite avec la nouvelle lignée et `hello.exe` régénéré
  **byte-identique** à l'artefact scellé (sha256 `c89e330c…507f2` vérifié, preuve que
  la valeur perdue n'était que l'enveloppe chiffrée, jamais le projet). La carte M1
  (génération 1) dérive ses clés de la même phrase par contexte HKDF distinct.
- **Alternatives rejetées** : attendre la restauration depuis le coffre du développeur
  (bloque M1, et rien ne garantit que le coffre a été alimenté avant la perte) ;
  conserver une carte M0 illisible (tableau de bord au rouge, contraire au fail-closed) ;
  dériver les clés d'une phrase mémorisable (entropie affaiblie — les 128 bits
  aléatoires sont conservés) ; modifier le sel Argon2id de M0 (la constante documentée
  reste la référence de la génération 0).
- **Développement** : la nouvelle phrase maîtresse est réaffichée une fois au
  développeur (fin de session M1) avec l'instruction de coffre immédiat — les
  réinitialisations répétées du bac à sable en font la seule protection réelle de la
  continuité chiffrée. L'export de continuité (D16) reste le mécanisme prévu pour tout
  transfert de poste ; sa génération est à la demande du développeur. Le point
  d'attention « clés » de la reprise M0 est levé : `carte_m0.py` est patché pour lire
  `triade/.keys/` (KEYS_DIR), unique modification du module M0 — l'artefact et la
  notation restent intouchés.

### D28 — Jalon M1 : plan d'adressage par zones, carte projet multi-artefacts, mini-libc

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : M1 exige des blocs réutilisables — c'est le premier jalon où un
  binaire (`selftest.exe`) embarque des blocs scellés par un autre (`hello.exe`), où
  la bibliothèque grandit (memset entre en dev.2) et où la carte doit indexer des
  blocs vivant dans plusieurs artefacts.
- **Choix retenu** : un **plan d'adressage par zones** documenté dans `m1/layout.py`
  (source unique partagée par le builder, l'outil d'auteur et l'oracle) — zone io
  0x1000-0x10FF (write@0x1040 et exit@0x1080 réutilisés octet-identiques de M0 ;
  0x1000 et 0x10C0 réservés), zone libc 0x1100-0x17FF (six blocs M1 + réserve pour
  libc-08+, memset y entre en dev.2 sans rien déplacer — démonstration R7 en
  conditions réelles), zone app 0x1800-0x1FFF (autotest, point d'entrée, non scellée) ;
  structures PE héritées de M0 à positions immuables (descripteurs, hint/names, INT,
  IAT@0x20B0, BASERELOC) car les déplacements RIP des blocs scellés l'exigent ; slots
  réservés remplis d'`int3` défensif (R10 à l'échelle du layout). La **carte projet
  génération 1** indexe les blocs des deux artefacts (champ `artefact=` par entrée,
  `role=` pour la localisation par intention) avec numérotation a1xxxx (M0) /
  b2xxxx (M1). Le balisage suit § 9 : `0.2.0-dev.1` (six blocs + autotest 18/18) →
  `0.2.0-dev.2` (+ memset, 21/21) → `0.2.0-rc.1` à la cristallisation.
- **Alternatives rejetées** : déplacer write/exit vers une zone io unifiée (re-liage
  forcée, interdite par R7) ; une carte par artefact (fragmente l'interface unique de
  développement et doublerait le coût de localisation) ; réserver la zone libc à sa
  seule taille initiale (toute croissance déplacerait des blocs scellés) ; IAT
  relocalisée (casserait les octets scellés de M0).
- **Développement** : la démonstration R7 s'appuie sur l'historique git — dev.1 scelle
  six blocs libc + les deux blocs io réutilisés ; dev.2 ajoute memset dans la réserve
  et étend l'autotest (libc-08:R1 → R2, 18 → 21 vecteurs) ; la preuve compare les
  octets des slots scellés entre les deux commits et contre `hello.exe`. L'outil
  d'auteur `outils/auteur.py` fait l'arithmétique d'adresses de l'auteur (étiquettes,
  symboles, déplacements RIP) et émet la notation explicite WYSIWYG — keystone assemble
  seul, le round-trip s'applique à la sortie ; l'outil n'est jamais dans la chaîne de
  build. Trois défauts ont été attrapés par la chaîne de vérification AVANT scellage :
  (1) sémantique d'arrêt de `repe cmpsb` — un désaccord sur le dernier octet laisse
  rcx=0 et ZF=0, le test `test rcx, rcx` concluait à tort à l'égalité (corrigé :
  branchement direct sur ZF) — classe T4 (contrat de l'instruction mal cerné) ;
  (2) clause Q4 de libc-04 irréalisable pour une génération en place — révision du
  contrat à R2 avant scellage (borne dure de douze octets, espace de travail non
  spécifié au-delà du NUL) — classe T2 (contrat écrit impossible) ; (3) constante de
  longueur du préfixe de verdict (22 au lieu de 21 octets) — détectée par l'émulation
  binaire complète — classe T3 (désynchronisation intention/notation). Aucun de ces
  défauts n'a survécu au scellage : l'oracle a payé son coût.

### D29 — Substrat d'émulation de l'oracle différentiel (Unicorn)

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : le protocole exige un oracle différentiel à volume de référence de
  douze mille cas par bloc critique (§ 8), exécuté à chaque session depuis I — mais
  les blocs ciblent Windows 11 : sans substrat d'exécution local, la boucle
  vérifie-puis-écrit (R5) exigerait la machine cible à chaque édition.
- **Choix retenu** : **Unicorn** (émulation x86-64) comme substrat de l'oracle M1 —
  exécution des blocs chargés depuis l'artefat scellé avec entrées aléatoires
  contraintes par les pré-conditions, comparaison à la référence Python dérivée de I
  (valeur de retour, mémoire de destination, curseur d'arène, registres non volatils,
  RSP, intégrité de l'image hors régions autorisées, canari de pile) ; émulation du
  binaire entier avec shim IAT (GetStdHandle/WriteFile/ExitProcess interceptés :
  sortie exacte et code de sortie vérifiés) ; falsification systématique (corruption
  d'octet de code → détection obligatoire, zéro silence). Les graines différencient
  les exécutions : dix vérifications cristallisent un bloc (R6) sans jamais répéter
  les mêmes entrées.
- **Alternatives rejetées** : attendre Windows pour chaque vérification (pas de boucle
  locale, R5 inapplicable, le développeur devient goulot d'étranglement) ; interpréteur
  x86-64 maison (surface d'erreur disproportionnée — l'oracle deviendrait moins fiable
  que le code qu'il vérifie) ; wine (dépendance extérieure non contrôlée, sémantique
  des API divergente, échec silencieux possible) ; QEMU process-level (lourd, pilotage
  complexe pour des appels de fonction isolés).
- **Développement** : l'émulation ne remplace pas la validation terrain (D26) — elle
  la précède et la prépare : l'oracle prouve la sémantique des blocs à chaque session,
  le terrain prouve l'environnement une fois par balise. Les verdicts hachés survivent
  seuls dans frag-prf (D1 : l'oracle est éphémère, régénéré, jamais archivé). La
  baseline d'intégrité de l'image est prise APRÈS résolution de l'IAT (le chargeur
  légitime réécrit l'IAT — mesurer avant produirait un faux positif, découvert et
  documenté pendant la mise au point).

### D30 — Troisième réinitialisation du bac à sable : D27 réappliquée, preuves byte-identiques

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : troisième réinitialisation du poste de développement depuis la création
  du dépôt ; `triade/.keys/` (phrase maîtresse, graine Ed25519 de la lignée D27) est
  perdu, les cartes M0 et M1 du dépôt redeviennent indéchiffrables — le scénario D27 à
  l'identique. La reprise s'est faite par la méthode A (clone du bundle Drive), jetons
  restaurés depuis le dossier « Tokens », remote GitHub reconfigurée.
- **Choix retenu** : réappliquer D27 telle quelle — régénérer la lignée (`triade/.keys/`)
  et reconstruire les cartes depuis I + notation. Les preuves de continuité sont
  constatées : `hello.exe` régénéré byte-identique (sha256 `c89e330c…507f2`) et
  `selftest.exe` régénéré byte-identique (sha256 `8038585b…f3c0`) — les octets scellés
  n'ont jamais dépendu des secrets perdus. Les compteurs de cristallisation repartent
  de 1 (l'ancien frag-prf est indéchiffrable), le protocole R6 exigeant dix
  vérifications de la nouvelle lignée de toute façon.
- **Alternatives rejetées** : restaurer la phrase D27 depuis le coffre du développeur
  (elle ne suffirait pas : la graine Ed25519, jamais confiée, est perdue avec le poste
  — la signature de la carte aurait dû être régénérée dans tous les cas, et l'attente
  bloque le jalon, exactement l'alternative déjà rejetée en D27) ; conserver des cartes
  illisibles dans le dépôt (tableau de bord au rouge, contraire au fail-closed).
- **Développement** : la nouvelle phrase maîtresse est réaffichée une seule fois au
  développeur en fin de session, avec l'instruction de coffre immédiat (D27). Le
  premier **export de continuité** chiffré et signé (D16) est généré dans la même
  session : c'est le mécanisme prévu pour que la perte du poste n'entraîne plus jamais
  celle de la lignée — l'export, conservé dans le coffre, restaure l'état complet sur
  n'importe quel poste conforme.

### D31 — Budget de localisation amendé à 64 tokens : la mesure M1 invalide l'estimation v0.4.0

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : l'instrumentation des budgets (critère de sortie M1, `m1/budgets_tokens.py`,
  tokenizer de référence tiktoken cl100k_base) mesure la ligne de localisation frag-loc
  à 56 tokens en moyenne — au-delà du budget normatif de 40 (spec § 4.3, § 12,
  FORMAT_CARTE § 4.1/§ 7). L'analyse attribue la cause aux deux niveaux : la dérive du
  format M1 (champs `artefact=`, `zone=` ajoutés par D28 sans mesure) ET, plus
  fondamentalement, l'estimation v0.4.0 elle-même — le gabarit canonique du § 4.3,
  pris à la lettre, mesure déjà 43 tokens en cl100k_base : le budget de 40 n'était
  pas atteignable, même avec une conformité parfaite au gabarit.
- **Choix retenu** : **amender le budget à 64 tokens** (spec § 12, FORMAT_CARTE § 4.1/§ 7,
  manuel agent § 4.3/§ 8, PDF formel via D17) ET **alléger le format frag-loc** au
  gabarit § 4.3 strict + `exe=` + `role=` : `zone=` est retiré (dérivable de l'en-tête
  `[zones]`), le suffixe `.exe` devient implicite. Ligne mesurée : 48–55 tokens
  (moyenne 51), marge 13 tokens sous le budget amendé. Les budgets éditer (3 000,
  mesuré 724) et ajouter (6 000, mesuré 1 091) sont inchangés — l'estimation y était
  saine.
- **Alternatives rejetées** : conserver le budget 40 en l'état (inatteignable même par
  le gabarit canonique : une norme que personne ne peut suivre est une non-norme) ;
  raccourcir la ligne sous 40 en retirant `role=` ou `cible=` (la localisation par
  intention exige le nom sémantique, le multi-profils exige le champ profil — rogner
  la sémantique pour 11 tokens inverse la hiérarchie des priorités au profit du coût
  en tokens, dernier des quatre objectifs) ; laisser la non-conformité au tableau de
  bord en attendant la validation terrain (bloque le scellage rc.1 sans apporter
  d'information nouvelle).
- **Développement** : le budget amendé reste un plafond, pas une licence : la mesure
  est consignée dans `m1/budgets.json` (composition détaillée, mesures par bloc) et le
  tableau de bord affiche désormais les trois métriques mesurées avec leurs cibles.
  Le tokenizer de référence (cl100k_base) est documenté dans l'outil et le budgets.json
  pour reproductibilité ; toute future dérive du format frag-loc sera constatée par
  la même instrumentation, désormais obligatoire à chaque scellage rc/final (§ 8.2).

### D32 — Jalon M1 franchi : validation terrain Windows 11 constatée, balise finale 0.2.0

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : dernier critère de fermeture M1 — le constat terrain de
  `selftest.exe` (9 216 o, sha256 8038585b…ff3c0, balise 0.2.0-rc.1, distribué par le
  miroir Drive `TRIADE/m1/`). Le développeur a exécuté l'artefact sur sa machine
  Windows 11 (cmd, `C:\Users\Alek\Downloads>selftest.exe`) : la ligne unique
  `TRIADE M1 : minilibc 21/21 OK` s'affiche à l'identique du contrat libc-08 Q2 —
  c'est le vecteur doré V2 (sortie exacte attendue, N = 21 vecteurs réussis) — puis
  retour au prompt sans incident. Erratum de documentation consigné à cette
  occasion : REPRISE_PROJET § 7.2 et m1/README § validation annonçaient « 21 lignes »
  de sortie ; le contrat Q2 exige une ligne unique « N/21 » suivie de « OK »/« KO » —
  l'artefact et le contrat font foi, les deux documents sont corrigés.
- **Choix retenu** : consigner le constat (présente décision) et sceller la
  **balise finale `0.2.0`** — nouveau mode `build_m1.py --sceller-final` : exige
  cristallisation 10/10 (R6) ET suite de conformité § 8.2 verte, vérifie que la
  balise courante est exactement `0.2.0-rc.1` (fail-closed), bascule la version du
  manifeste frag-bld vers `0.2.0`, re-scelle les quatre fragments et re-signe la
  carte (Ed25519), instrumentation des budgets re-exécutée (D31), tableau de bord
  régénéré. Balise immuable (§ 9) : tout défaut découvert après coup se corrige en
  `0.2.1` à contrat stable (R4). Les quatre critères de sortie M1 et les conditions
  transverses (§ 16) sont acquis — **jalon M1 franchi le 26 octobre 2026**.
- **Alternatives rejetées** : exiger les contrôles optionnels ERRORLEVEL/certutil
  avant le scellage (le verdict est porté par la ligne de sortie elle-même :
  l'auto-test a compté N = 21 et affiché OK ; le code 0 est la post-condition Q3,
  vérifiée par l'oracle à chaque exécution en émulation — reconfirmée à la graine 15
  post-scellage) ; reconstruire l'artefact sous balise 0.2.0 (interdit : la carte
  cristallisée refuse la reconstruction — R6/R10 ; le scellage final ne touche que
  la balise du manifeste, aucun octet du binaire) ; poser un tag git `v0.2.0` sans
  demande du développeur (précédent M0 : la balise d'artefact vit dans frag-bld, le
  tag git viendra sur demande).
- **Développement** : l'écriture du scellage final a révélé un angle mort du
  contrôle anti-rollback de `construire()` : la reconstruction était refusée pour
  une balise `-rc.N` mais autorisée pour une balise finale `X.Y.Z` — corrigé dans la
  même décision : le contrôle refuse désormais toute balise scellée (rc ou finale),
  fail-closed. Export de continuité régénéré sur la lignée 0.2.0 et poussé au
  coffre (racine Drive, D16/D30). Prochaine étape : **M2** — patch à chaud sur
  serveur TCP écho, le jalon de vérité du protocole (élément 5 de la suite de
  conformité § 8.2).

### D33 — Ouverture M2 : plan d'adressage étendu, couche I et notation posées

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : reprise du jalon M2 (patch à chaud, serveur TCP écho). La session
  d'ouverture a produit la couche I complète (quatorze spécifications : tcp-01 à
  tcp-12 + tcp-08:R2 en croissance + libc-09 dans la réserve prévue) et la notation
  des treize blocs embarqués plus libc-09, avec la chaîne build/oracle/carte — sans
  encore exécuter la construction (interruption de session). La présente décision
  sécurise l'état intermédiaire et consigne le plan d'adressage sur lequel la
  couche I s'appuie déjà.
- **Choix retenu** : étendre le plan D28 par une quatrième section `.text2` RX
  @ 0x4000-0x4FFF (zones net 0x4000, thr 0x4300, tramp 0x4400, echo 0x4600 avec
  croissance 0x4680, srv 0x4800) ; l'ensemble d'imports kernel32 passe de 3 à 10
  entrées et ws2_32 rejoint les imports (D7) — l'INT kernel32 déménage de 0x2090 à
  0x2110 (donnée pure, aucun octet de code ne la référence : relocation sans effet
  R7) ; l'état serveur vit en .data @ 0x3800+, la zone curseur+arène (0x3000-0x37FF)
  restant à l'identique. Carte génération 2 : 14 blocs nouveaux c30001-c30014,
  artefact #3 echo.exe, blocs M0/M1 réembarqués octet-identiques à leurs adresses
  historiques (R7). Discipline M2 : composition sur pile privée par thread (zéro
  état partagé hors section critique du journal), libc-09 livrée comme primitive
  scellée pour M3+ (aucun appelant dans echo.exe).
- **Alternatives rejetées** : étaler .text (impossible : 0x1000-0x1FFF scellé M1,
  R7 interdit tout déplacement) ; créer un domaine nouveau par bloc réseau (le
  registre figé § 2.1 étend le domaine `tcp` réservé M2 — un domaine unique garde
  la traçabilité I↔C lisible) ; committer la couche I sans décision (le journal
  d'abord : l'état intermédiaire est consigné AVANT la sauvegarde, pas après).
- **Développement** : la construction dev.1, l'oracle et le scellage restent à
  exécuter — la présente décision borne l'état : couche I et notation posées,
  construction non encore exécutée, aucun verdict émis. La session suivante
  exécute `build_m2.py --phase 1` et consigne les verdicts réels.

### D34 — Auto-hébergement de l'agent : profil Linux ouvert, échelle d'auto-hébergement

- **Statut** : active · **Date** : 26 octobre 2026
- **Contexte** : demande du développeur : l'agent utilise TRIADE pour son propre
  travail et pousse l'expérience « jusqu'à remplacer Python », « au plus bas niveau
  possible avec l'architecture matérielle », en créant sa propre méthode si
  nécessaire — l'expérience nourrissant l'évaluation du protocole. Fait terrain
  déterminant : l'environnement d'exécution de l'agent est une machine Linux
  x86-64 sur laquelle l'agent peut écrire et exécuter des ELF64 natifs (sonde
  validée : ELF minimal de 159 octets, en-têtes écrits à la main, appels système
  directs, exécution constatée sortie exacte) — l'agent est donc SON PROPRE
  TERRAIN sur ce profil, capacité qu'aucun jalon du plan actuel n'exploite avant
  M6. Le CPU expose par ailleurs SHA-NI et AVX2 (optimisation future, R11).
- **Choix retenu** : ouvrir le profil `x86-64-linux-elf64` par anticipation
  restreinte sur M6 (la demande du développeur prime sur l'ordre des jalons ; les
  critères de sortie M6 complets — diff nul sur la couche I, parité inter-profils —
  restent soumis à l'achèvement de M2-M5 : le présent périmètre est l'auto-hébergement
  de l'agent, pas le jalon M6). Méthode créée : **l'échelle d'auto-hébergement** —
  échelon 1, exécution native (les outils de l'agent tournent en code machine nu
  sur son propre terrain) ; échelon 2, vérification native (hachage et signature
  vérifiés par des blocs TRIADE) ; échelon 3, assemblage natif (un assembleur en
  notation remplace keystone pour le sous-ensemble du projet) ; échelon 4, fermeture
  de boucle (l'assembleur natif assemble ses propres blocs, byte-identique — le
  berceau Python devient vérificateur externe optionnel). Premier artefact :
  `hachoir` (m6/), hacheur SHA-256 natif conforme FIPS 180-4 — neuf blocs, domaine
  nouveau `ah` (registre figé étendu), sortie au format sha256sum (remplaçant
  direct), lignée carte propre (génération 1 auto-hôte, sel de dérivation distinct,
  clés projet partagées D27), ABI SysV + interface noyau (le piège miroir de msx64 :
  4e argument syscall en r10, rcx/r11 détruits — spécifié dans la couche I). La
  preuve d'environnement du profil Linux est produite par l'agent et vérifiable par
  le développeur par re-exécution.
- **Alternatives rejetées** : attendre M6 dans l'ordre strict (l'expérience
  d'évaluation demandée par le développeur produirait ses données après quatre
  jalons : la boucle de rétroaction du protocole serait allongée pour rien) ;
  écrire l'outillage de l'agent en scripts non balisés (viole R1-R3 : chaque octet
  produit par l'agent doit vivre dans la carte — l'auto-hébergement n'est pas une
  exception à la discipline, c'est son terrain d'épreuve le plus strict) ; utiliser
  un compilateur pour l'outillage (un compilateur est précisément ce que TRIADE
  n'utilise pas : le berceau Python reste toléré comme outil d'amorce, il sera
  rétrogradé échelon par échelon, jamais remplacé par un autre traducteur opaque).
- **Développement** : l'échelle est le protocole d'évaluation de l'expérience :
  chaque échelon franchi doit être mesuré (budgets tokens D31, temps d'exécution,
  lignes de notation) et consigné — l'expérience alimente la spécification (les
  budgets « ajouter » seront mesurés sur des blocs réellement écrits par l'agent
  pour lui-même, première mesure auto-référentielle du projet). Le plancher
  d'accès matériel de l'agent est documenté sans détour : ring 3, appels système
  bruts, ELF écrit à la main — l'anneau 0 (MSR, tables de pages, firmware) n'est
  pas accessible depuis le bac à sable et le protocole ne le prétend pas
  (« le protocole ne promet pas, il vérifie » — réciproquement, il n'imagine pas,
  il constate).
