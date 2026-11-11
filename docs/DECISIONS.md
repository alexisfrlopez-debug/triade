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
  **Échelon 1 FRANCHI le 26/10/2026 (journal 20)** : hachoir 0.7.0-dev.1 scellé
  (9 blocs, 1 149 o de code, 12 288 o d'ELF64 écrit à la main, oracle natif
  20 cas + falsification 27/27, cristallisation 10/10, carte génération 1 au
  sel distinct). Mesures : hachoir 0,0048 s vs sha256sum 0,0025 s sur 1 Mo
  (ratio 1,9, SHA-NI non implémenté — R11) ; budgets tokens 8 774 (specs) +
  5 099 (notations livrées) ; build + oracle natif 30,5 s. Premier usage
  auto-référentiel effectif : les empreintes des artefacts du projet sont
  désormais produites par hachoir (parité sha256sum octet-identique constatée
  sur hello.exe/selftest.exe/echo.exe). Leçons versées à l'évaluation : la
  discipline a attrapé sur l'outil de l'agent DEUX défauts livrables (rol/ror :
  digest faux partout ; jbe/jb : crash sur toute taille multiple de 64) que
  l'œil de l'auteur avait ratés — l'écart « intention écrite vs octets exécutés »
  ne se ferme que par l'exécution, jamais par la relecture.
  **Échelon 2, PHASE 1 le 26/10/2026 (journal 21)** : sceau 0.8.0-dev.1 scellé
  (m7, 8 blocs notés dont 3 héritages hachoir OCTET-IDENTIQUES aux mêmes
  adresses, 355 instructions, 1 411 o de code, 16 384 o d'ELF64, oracle natif
  21 cas + falsification 28/28 zéro silence, cristallisation enclenchée,
  carte génération 1 au sel lignée sceau). SHA-512 natif écrit à la main —
  le moteur de hachage d'Ed25519 — et mode diagnostic --hacher (ligne
  sha512sum exacte). Mesures : sceau 0,0031 s vs sha512sum 0,0034 s sur
  1 Mo (ratio 0,91, PLUS RAPIDE que l'outil système : les 80 rondes u64
  occupent exactement les registres 64 bits) ; budgets mesurés : specs 17
  blocs 16 081 tok, lignée phase 1 9 171 tok. Usage auto-référentiel 512
  bits : empreintes des cinq artefacts par sceau, parité exacte. Trois
  défauts corrigés (offset structurel W[i-7] lu en W[i-11] — la leçon C1
  étendue aux constantes d'adressage ; étiquette de boucle déplacée —
  les ADRESSES du savoir-faire font foi, pas sa lecture ; ombre de
  variable dans l'outil de falsification). Les specs des 12 blocs restants
  (corps f25519 radix 2^51, edwards25519 projective complète, vérificateur
  RFC 8032) sont POSÉES écrite-avant-code — dev.2+ : notations, oracle
  contre Python rétrogradé en RÉFÉRENCE, puis vérification des cartes du
  projet par code machine nu.

### D35 — Défaut champ IAT ws2_32 dans echo.exe 0.3.0-rc.1 : correctif rc.2 et démonstration graphique en un clic

- **Statut** : active · **Date** : 27 octobre 2026
- **Contexte** : demande du développeur : un `.exe` à interface graphique réalisant
  la démonstration complète M2 « en un clic », TRIADE utilisé partout où possible,
  chaque expérience servant à améliorer le protocole en continu. La revue croisée
  préalable à toute réutilisation des blocs scellés (discipline R7 : vérifier les
  octets avant de les embarquer) a exposé un défaut livrable dans `echo.exe`
  0.3.0-rc.1 : le descripteur d'import ws2_32 porte `FirstThunk = 0x22A0` alors que
  la notation scellée appelle les slots `0x2300-0x2348` — dans le binaire livré,
  ces slots contiennent des zéros. Le chargeur Windows résout les adresses à
  l'adresse pointée par `FirstThunk` : au premier appel `WSAStartup` (tcp-01),
  l'exécutable effectue `call qword ptr [0x2300]` = `call 0` et se termine sur
  violation d'accès — immédiatement APRÈS la bannière, qui s'imprime avant
  l'initialisation réseau. Le constat terrain du 26/10 était donc PARTIEL au sens
  strict : il prouvait la bannière et la porte R10 (kernel32 : descripteur FT
  0x20B0 correct), pas le service. L'oracle ne pouvait pas attraper le défaut :
  ses shims écrivaient directement aux adresses `IAT_SLOTS` (0x2300+), modélisant
  un chargeur qui écrit là où le code appelle — une hypothèse d'environnement
  fausse, invisible différentiellement puisque partagée par l'oracle et le défaut.
- **Taxonomie (T1-T6)** : défaut de type **T3** (contrat incohérent entre couches) —
  la couche I du profil déclare l'IAT ws2_32 aux slots 0x2300+ (I1 de tcp-01) mais
  le binaire livré ne satisfait pas la pré-condition de résolution du chargeur
  (FirstThunk ≠ slots appelés) ; aggravé d'un **défaut d'oracle** (modèle
  d'environnement non dérivé de I : la correspondance descripteur→slots n'était
  vérifiée par personne — la leçon D34 « l'écart ne se ferme que par l'exécution »
  s'applique aussi au modèle du chargeur).
- **Choix retenu** : (1) correctif `0.3.0-rc.2` à contrat stable (R4) —
  `FirstThunk` ws2_32 réaligné sur 0x2300, pré-IAT posée aux slots appelés
  (convention kernel32), hints ws2_32 déménagés 0x2310 → 0x2360 et version u64
  0x00030002 → 0x00030003 (monotonie R10) : le diff est intégralement en `.rdata`,
  données pures, AUCUN octet de code ne bouge (R7 préservé, tranches tcp
  octet-identiques) ; le garde-fou anti-rollback est amendé pour autoriser
  exactement rc.1 → rc.2 (toute autre reconstruction reste interdite) ; l'oracle
  gagne un verrou « chargeur réel » : chaque descripteur d'import doit avoir son
  `FirstThunk` sur les slots que la notation appelle (fail-closed sur la
  divergence oracle/terrain). (2) La démonstration demandée devient le véhicule de
  validation du correctif : `demo.exe` (jalon démo, `demo/`), exécutable
  WINDOWS_GUI PE32+ à la main embarquant les blocs scellés M0/M1/M2
  octet-identiques (io, libc, tcp-01..09, tcp-11, staging echo v2) + neuf blocs
  nouveaux `win-01..win-09` (fenêtre, boucle de messages, procédure, journal
  graphique, autotest porte R10+libc, client TCP, serveur d'acceptation,
  scénario complet) — un clic exécute : porte R10 → vecteurs libc → mécanique
  patch/rollback hors réseau → serveur écho local → client → boucle § 5 complète
  (patch EN PRODUCTION pendant le trafic, retour arrière, vérifications byte à
  byte) → arrêt propre. Sous-système WINDOWS_GUI (le journal TCP hérité échoue
  proprement sans console ; handles stdout/stdin mis en cache si une console
  existe). Imports étendus : user32 ×14, gdi32 ×1, kernel32 ×11 (+GetModuleHandleW),
  ws2_32 ×11 (+connect) — l'IAT ws2_32 de la démo porte le correctif D35 dès la
  première génération.
- **Alternatives rejetées** : garder 0x22A0 comme FirstThunk et réécrire la
  notation des six blocs tcp vers 0x22A0 (interdit : R7 — déplacer les cibles
  d'appels IAT des blocs scellés ; et le désordre table/slots serait persistant) ;
  corriger seulement la démo et laisser rc.1 en référence (rejeté : la balise de
  référence du jalon de vérité ne peut pas porter un artefact qui crash au premier
  appel réseau — la correction est précisément le mécanisme prévu par R4) ;
  rétrograder le défaut en « note » sans nouvelle pré-version (rejeté : le scellage
  final 0.3.0 exige un artefact sain ; toute balise est immuable mais la lignée
  avance — dev.1 → dev.2 → rc.1 → rc.2).
- **Développement** : le correctif et la démo sont consignés au journal de travail
  (entrées 22-23) ; la cristallisation rc.2 repart à zéro (10/10 exigés avant
  scellage, R6) ; la suite de conformité est re-exécutée au scellage. La preuve
  terrain complète (écho + patch + rollback + console) sera fournie par la
  démonstration graphique elle-même, en un clic, sur la machine du développeur.

### D36 — demo.1 fenêtre vide : divergence notation/spec WM_SIZE, correctif demo.2 et trace terrain (journal fichier)

- **Constat** (terrain Windows 11) : demo.exe 0.3.0-demo.1 s'exécute sans
  erreur mais la fenêtre paraît VIDE — ni journal ni bouton, la démonstration
  en un clic est inopérante et MUETTE : aucune trace d'exécution n'existe
  (« il faudrait que tu puisses obtenir les logs de l'exécution de demo.exe »).
- **Diagnostic** : win-04 (WM_SIZE) lisait `RECT.top` (`[rsp+0x24]`,
  toujours 0 côté client) comme LARGEUR au lieu de `RECT.right`
  (`[rsp+0x28]`) → MoveWindow(largeur = -16) sur journal et bouton →
  contrôles créés puis rendus invisibles au premier redimensionnement (WM_SIZE
  est envoyé PENDANT CreateWindowExW). La spec win-04:R1 exigeait déjà
  « (8, 8, w-16, h-56) » : la spécification était JUSTE, les octets étaient
  faux — troisième divergence de la classe « mauvais champ / mauvais slot »
  (après W[i-7] du SHA-512 m7 et l'offset .rdata M0). L'oracle durci en a
  révélé une QUATRIÈME sur le même gestionnaire : nHeight recevait `bottom`
  et bRepaint `bottom-56` (slots intervertis — la hauteur du journal
  débordait sous le bouton).
- **Pourquoi l'oracle R1 est resté vert** : (1) la coquille GUI (win-01..04)
  n'était JAMAIS exécutée — seuls win-05..win-10 l'étaient, le scénario étant
  appelé directement : l'écart « blocs de preuve testés / habillage non
  testé » était structurel ; (2) le shim MoveWindow retournait 1 sans
  examiner les arguments — un témoin muot ne prouve que l'appel, pas la
  géométrie ; (3) le shim GetClientRect écrivait le RECT dans rcx (hwnd) au
  lieu de rdx (lpRect) — défaut latent jamais déclenché faute d'exécution.
- **Correctif (demo.2, 0.3.0-demo.2, u64 0x00030102)** :
  1. win-04:R2 — lecture `RECT.right`, nHeight = h-56, bRepaint = 1 ;
     création de contrôle nulle → fail-closed tracé (retour -1 : une vitrine
     sans contrôle est un mensonge muet, R1 la tolérait, D36 la refuse) ;
  2. win-11:R1 (nouveau bloc) — journal FICHIER `demo_journal.txt` posé à
     côté de l'exécutable : init paresseuse (GetModuleFileNameA + scan
     arrière du séparateur + memcpy libc-01 scellé + CreateFileA
     FILE_APPEND_DATA | CREATE_ALWAYS), trois modes (ligne ASCII ; préfixe +
     décimal via itoa libc-04 scellé ; UTF-16 → Latin-1 avec 0x2192→'>' et
     ≥0x100→'-', CRLF idempotent), FlushFileBuffers à chaque ligne (trace
     survivant à un crash), échec → handle -1 puis re-tentative, append
     atomique multi-threads ;
  3. win-05:R2 — miroir fichier de chaque ligne d'écran (l'écran D'ABORD :
     la démonstration reste regardable même si le fichier est impossible) ;
  4. win-02:R2 — L00 « demarrage » AVANT tout appel GUI (le fichier existe
     dès la première seconde : un crash précoce laisse une trace), L01 après
     création, LKO…gle=NN à l'échec (GetLastError AVANT MessageBoxW) ;
  5. imports kernel32#2 — descripteur dédié @0x2080 (l'ancien terminateur,
     le marché s'étend en place), FT 0x2E80 (slots appelés, D35), hints dans
     les interstices libres : l'IAT kernel32 historique 0x20B0 reste INTACTE
     (R7, zéro octet scellé déplacé) ;
  6. re-planification — win-09 déménagé en .text2 @0x4C00 (ré-assemblé, spec
     R1 inchangée), table R10 à 29 entrées, R_VERSION 0x2610→0x2628, R_ANCRE
     0x2620 inchangé (l'ancre de win-06 reste stable).
- **Oracle durci (l'acquis principal)** : la coquille GUI est exécutée du
  point d'entrée à ExitProcess — RegisterClassExW VALIDÉ (cbSize, wndproc
  dans l'image, nom de classe), CreateWindowExW top-niveau dispatche
  RÉELLEMENT WM_CREATE puis WM_SIZE à la procédure (appels imbriqués :
  sauvegarde/restauration du contexte complet, pile séparée), invariant
  géométrique MoveWindow (x, y ≥ 0 et largeur, hauteur > 0, rejet sinon) +
  géométrie exacte (journal (8, 8, 764, 504), bouton (8, 516, 764, 36)),
  journal fichier exact dans l'ordre L00→L02→L01, clic unique (spawn UNE
  fois, EnableWindow FALSE, L03, second clic ignoré), échec piloté (classe
  en échec → MessageBoxW + LKO gle=87 + sortie 1), FALSIFICATION RECT :
  l'octet 0x28 réécrit en 0x24 (le défaut originel) DOIT faire échouer
  l'oracle. Verdict : 73 cas verts (49 avant), structurel 541, falsification
  28/28, carte re-scellée + verrou croisé R8 vert.
- **Enseignements protocolaires (boucle d'amélioration continue)** :
  (a) un shim sans invariant est un témoin muet — toute API simulée doit
  REJETER les arguments impossibles, pas seulement constater l'appel ;
  (b) l'oracle doit exécuter la chaîne COMPLÈTE du point d'entrée à la
  sortie, pas seulement les blocs porteurs de preuve ;
  (c) les divergences notation/spec « mauvais champ/mauvais slot » se
  détectent par les DONNÉES traversant les frontières (le RECT lu doit
  redevenir la géométrie attendue), jamais par le seul flux d'appels ;
  (d) l'outil auteur gagne les symboles LEN_* (longueurs dérivées du plan :
  zéro comptage manuel) et 16 passes de point fixe (frontière rel8 des
  sauts courts).
- **Alternatives rejetées** : attacher une console (AllocConsole) pour la
  trace — contredit la démonstration graphique et ne survit pas à un crash
  du processus ; journal dans %TEMP% — introuvable pour l'utilisateur, le
  fichier à côté de l'exe est immédiatement visible ; tracer seulement
  depuis le scénario (win-09) — les échecs PRÉCOCES (création de fenêtre)
  précèdent tout clic, le journal doit exister dès la première seconde ;
  GetModuleFileNameW + conversion — GetModuleFileNameA suffit (chemin ASCII).
- **Développement** : entrée 23 du journal de travail. Validation terrain
  attendue : fenêtre complète (journal + bouton), clic = démonstration
  intégrale, et demo_journal.txt à côté de l'exe contenant la trace
  complète (L00…« boucle § 5 complète — DÉMO OK ») — ou, en cas d'échec,
  la dernière étape franchie AVEC son code GetLastError : le terrain ne
  pourra plus jamais être muet.

### D37 — demo.2 écran vide au démarrage : miroir écran universel (win-05:R3), diagnostics MoveWindow (L4C/L4D) et extension .text2

- **Constat** (terrain Windows 11, capture 1920×1080 du 26/10/2026 20:56,
  déposée dans le dossier Drive « test » avec le journal fichier) : la
  fenêtre demo.2 maximisée affiche le bon titre, une zone client
  uniformément grise avec SEULE trace visible une scrollbar verticale
  (x≈1888-1904, flèches y≈39-63 et y≈992-1019 — le contrôle journal,
  correctement dimensionné par le correctif D36) — mais AUCUN texte et
  AUCUN bouton « TOUT DÉMARRER ». Le journal fichier, lui, est complet
  (L00/L02/L01, zéro LKO).
- **Diagnostic écran vide (défaut CONÇU, pas subi)** : les traces de
  démarrage (L00/L01/L02/L03/LKO) appelaient win-11 EN DIRECT (modes 0/1
  — fichier seul) : la spec win-02:R2 l'exigeait explicitement (« le
  fichier est le jumeau SILENCIEUX de MessageBoxW »). Combiné à l'edit
  créé avec un texte initial VIDE (chaîne "" @0x2A52), la vitrine restait
  muette tant que personne ne cliquait — et le bouton, seul élément
  visible attendu, ne s'affichait pas (voir ci-dessous). La cause
  fonctionnelle : 17 appels au miroir écran win-05 existaient bien
  (scénario ×16 + serveur ×1) mais AUCUN pour le démarrage.
- **Bouton invisible (mystère ouvert, instrumenté)** : audit octet
  intégral (styles 0x50000001 avec WS_VISIBLE, positions (8,396,716,36)
  puis (8,h-44,w-16,36), handles distincts 0x3868/0x3870, IAT MoveWindow
  réelle, chaînes "EDIT"/"BUTTON"/"TOUT DÉMARRER" NUL-terminées,
  WM_CREATE→WM_SIZE confirmé par la géométrie mesurée de la scrollbar) :
  TOUT est correct — notation, octets, oracle. Aucune explication
  statique ne tient. Décision : ne PAS deviner — INSTRUMENTER. WM_SIZE
  journalise désormais les RETOURS BOOL des deux MoveWindow (L4C/L4D,
  win-11 mode 1) : le prochain run terrain dira si MoveWindow(bouton)
  réussit (1) ou échoue (0), fenêtre maximisée OU NON.
- **Correctif (demo.3, 0.3.0-demo.3, u64 0x00030103)** :
  1. win-05:R3 — miroir UNIVERSEL, point de passage unique de toutes les
     lignes (D37) : écran d'abord PUIS fichier, deux entrées — trace
     (0x5000 : contrat 4 args de win-11, drop-in pour win-02/win-04 :
     re-ciblage pur des 8 sites) et scénario (0x5100 : shim
     `mov r8d,2 ; jmp` — les 17 appelants historiques ne bougent pas) ;
     conversion ASCII→UTF-16 sur place (BUF_MIROIR .data 128 o, itoa
     libc-04 scellé pour les valeurs, CRLF+NUL en une écriture dword+word),
     garde HWND_JOURNAL nul (avant WM_CREATE : L00 reste au fichier —
     il n'y a rien à peindre), relais fichier en QUEUE (`jmp win-11` :
     comportement fichier inchangé octet par octet) ;
  2. win-02:R3/win-04:R3 — traces via JOURNAL_TRACE ; WM_SIZE capture
     les retours MoveWindow AVANT tout appel suivant (I5, r12d/r13d
     libres : uMsg/wParam consommés à ce point) ;
  3. extension .text2 : le win-05:R3 (258 o) ne tient ni dans son slot
     .text historique (256 o — slot 0x19C0-0x1ABF désormais LIBRE) ni
     dans la zone 0x4700-0x47FF → .text2 passe à 0x1400 (VSIZE), image
     0x6000 (alignement SectionAlignment — 0x5400 nu aurait été refusé
     par le chargeur ET unicorn), fichier 0x4000 (16384 o) ; win-05 vit
     à 0x5000, hors des pages VirtualProtect du patch (0x4000-0x4FFF) ;
  4. l'entrée trace porte le prologue à l'INSTRUCTION 0 (le verrou
     pile-alignée M2 compte les pushes depuis la première instruction —
     fonction scellée non modifiable : c'est le shim qui vit en fin de
     slot, pas l'inverse).
- **Oracle durci (77 cas verts, +4)** : win-05 testé par ses DEUX
  entrées (scénario utf16 ; trace modes 0/1/valeur + garde E1) ; la
  coquille GUI vérifie désormais l'ÉCRAN au démarrage (ECRAN_DEMARRAGE :
  L02→L4C→L4D→L01 — l'ordre prouve le dispatch imbriqué WM_CREATE+WM_SIZE
  de CreateWindowExW) et après clic (L03) ; le test win-09 pose un
  HWND_JOURNAL factice (sur le terrain, le scénario tourle TOUJOURS avec
  le GUI vivant) ; falsification D37 : re-cibler la trace L01 de win-02
  vers win-11 (le défaut demo.2 exact) doit ôter L01 de l'ÉCRAN sans
  altérer le fichier — sinon l'anti-régression ne garde rien.
- **Enseignements protocolaires** : (a) une spécification peut EXIGER le
  défaut — win-02:R2 demandait un fichier silencieux : le retour terrain
  (capture) a jugé la CONCEPTION, pas seulement l'implémentation ; (b)
  l'oracle vérifiait le journal fichier de la coquille mais pas son
  ÉCRAN : toute sortie observable du terrain doit avoir son témoin ;
  (c) une falsification « post-appel » doit porter son contrôle INLINE —
  les vérifications de la coquille vivent dans executer(), pas dans
  appeler() : envelopper seul l'appel ne teste rien (la falsification
  RECT, elle, est détectée par un shim PENDANT l'exécution — deux
  mécaniques différentes) ; (d) quand le statique est épuisé et
  irréprochable, la réponse n'est pas la spéculation mais
  l'INSTRUMENTATION ciblée (L4C/L4D : 2 lignes, 60 octets).
- **Alternatives rejetées** : raser 12 octets du win-05:R3 pour le
  faire tenir en 240 (factoring des SendMessage — compte ±2 non
  démontrable à la main : la marge de confiance était nulle) ; placer
  win-05 dans le padding d'un autre bloc (violation D8 un-bloc-un-slot) ;
  attacher l'écran AVANT le fichier dans win-11 lui-même (win-11:R1
  aurait bougé — la chaîne fichier devait rester octet-identique).
- **Développement** : entrée 25 du journal de travail. Validation terrain
  attendue : la fenêtre affiche DÈS LE LANCEMENT L02, L4C, L4D puis L01
  (miroir vivant), le bouton est visible OU L4D=0 l'explique ; clic =
  démonstration intégrale à l'écran ET au fichier. La capture terrain a
  été convertie en preuve : forensique pixel (cartographie des 2 114
  pixels non-fond — scrollbar seule, zéro texte, zéro bouton) + VLM sur
  l'image brute.

### D38 — demo.3 bouton invisible malgré L4D=1 : registres volatiles relus après l'appel (win-04:R4), oracle durci sur l'ABI caller-saved

- **Constat** (terrain Windows 11, dossier Drive « test », 26/10/2026
  22:11-22:13) : le journal demo.3 (150 o) livre la séquence complète
  L00→L02→L4C=1→L4D=1→L01 — D37 VALIDÉ sur terrain réel (la fenêtre affiche
  son démarrage : 4 lignes lues par VLM, largeurs 213/113/117/162 px
  proportionnelles aux textes) et Windows déclare placer le bouton avec
  succès (L4D=1). Or la capture (957×691) montre, sous l'edit dont la
  scrollbar prouve la géométrie exacte (flèches y 58-62 / 617-621 = h-56,
  soit client 764×516 logique), une bande basse (y 631-680) UNIFORMÉMENT
  grise : le bouton n'est pas « discret », il est ABSENT du rendu. DPI
  déduit de la taille physique : écran du développeur à 125 % (780×560
  logique → ~975×700 physique, uniforme).
- **Diagnostic (le binaire trahi par l'ABI, pas par la logique)** : audit
  octet du fautif présumé — styles 0x50000001 (WS_CHILD|WS_VISIBLE),
  classe "BUTTON", libellé "TOUT DÉMARRER" UTF-16, parent rbx, id 1,
  handles 0x3868/0x3870 distincts, table d'imports vérifiée slot par slot
  (chaque appel win-04 désigne la bonne fonction : la divergence 0x2850
  était dans ma table d'attente, pas dans le binaire) — TOUT est correct,
  encore. Le coupable est dans WM_SIZE : w = RECT.right et h =
  RECT.bottom étaient chargés dans r10d/r11d, REGISTRES VOLATILES
  (caller-saved), puis RELUS après le premier `call MoveWindow` pour
  positionner le bouton. Le premier appel consomme w/h avant l'appel
  (correct : l'edit est géométriquement parfait), le second les relit
  APRÈS : détruits par l'appel — l'instruction `syscall` écrit RFLAGS
  dans r11 PAR MATÉRIEL (r11 ≈ 0x246) et r10 ne survit pas. Le bouton
  reçoit alors (8, 0x246-44=538, 0-16=-16, 36) : y=538 dans un client de
  516 → HORS FENÊTRE. Win32 accepte un enfant hors zone parent et
  retourne VRAI : L4D=1 était VRAI et le bouton invisible — les deux
  faits, contradictoires en apparence, s'expliquent ensemble. La spec
  win-04:R3 I5 avait raisonné la volatilité de rax (retours capturés en
  r12d/r13d callee-saved) mais oublié r10d/r11d : la discipline avait le
  bon réflexe à moitié appliqué.
- **Pourquoi toute la chaîne était verte** : notation (le flux sur le
  papier est correct : chargé, consommé, relu), round-trip (les octets
  sont ce que la notation dit), audit IAT (les appels sont bons), oracle
  (les shims Python posent rax et ne TOUCHENT AUCUN autre registre : les
  r10/r11 de la CPU émulée survivent à l'appel — l'ABI caller-saved
  n'était PAS modélisée). Classe de défaut nouvelle : le contrat
  d'ABI lui-même, invisible à toute vérification qui ne détruit pas les
  volatiles au retour des appels.
- **Correctif (demo.4, 0.3.0-demo.4, u64 0x00030104)** : win-04:R4 — w/h
  chargés UNE fois dans r14d/r15d (callee-saved) avant le premier appel,
  relus tels quels par les DEUX MoveWindow. r14 portait lParam d'entrée
  (seule la branche DefWindowProc — jamais atteinte depuis WM_SIZE — en
  a besoin) et r15 est libre hors WM_CREATE : zéro conflit, taille
  identique (encodages 44 8B 74/7C 24 …, 45 89 F1/F8), le slot ne bouge
  pas. Invariant I6 écrit AVANT le code : « aucun registre volatile ne
  survit à un appel IAT ».
- **Oracle durci (78 cas verts, +1) — le vrai correctif** : les shims
  CLOBBENT désormais rcx/rdx/r8/r9 (sentinelles 0xCC…) et r10=0,
  r11=0x246 (un retour kernel réaliste : RFLAGS dans r11) à CHAQUE
  retour IAT, y compris le retour simulé du dispatch imbriqué
  CreateWindowExW. Le code correct ne le remarque pas (aucun bloc ne
  relit un volatile après un appel — vérifié par le passage à 78/78),
  le défaut D38 meurt immédiatement : falsification V5 — réécrire les
  deux usages callee-saved du second MoveWindow en r10d/r11d (45 89
  F8→D8, 45 89 F1→D1 : le défaut demo.3 exact) fait ÉCHOUER l'invariant
  géométrique (largeur = -16) — le bouton invisible est impossible à
  réintroduire silencieusement. Poétique : c'est l'invariant D36 (géométrie)
  qui attrape le défaut D38 (ABI).
- **Défaut latent de même classe, DIFFÉRÉ** : libc-09-zone-alloc-ts (M2,
  c30012, indexé par la carte mais NON embarqué dans echo.exe ni demo.exe)
  sauvegarde ses arguments dans r10/r11 à travers EnterCriticalSection et
  son retour dans r10 à travers LeaveCriticalSection — deux sites. Non
  corrigé ici : la notation est scellée dans la carte M2 (R4, contrat
  stable) et le bloc n'a aucun appelant vivant ; le correctif partira
  avec la prochaine révision M2. Garde posée : scripts/scan_abi_volatile.py
  (scanner statique persisté, 220 alertes brutes dont les deux vraies
  positives — win-04 terrain-démontré, libc-09 latent — extraites par
  revue manuelle ; le scanner reste volontairement conservateur).
- **Enseignements protocolaires** : (a) un retour BOOL VRAI de l'API ne
  prouve pas le résultat VISIBLE — Win32 accepte des coordonnées hors
  zone parent : la preuve d'exécution (L4D) et la preuve de rendu
  (capture) sont deux faits distincts qu'il faut demander tous les deux ;
  (b) un émulateur à shims doit modéliser le contrat d'ABI (destruction
  des volatiles au retour), pas seulement les effets fonctionnels —
  sinon il bénit une classe entière de défauts ; (c) la volatilité est
  une propriété SILENCIEUSE en statique : la discipline « captured AVANT
  tout appel suivant » de I5 devait s'appliquer à TOUT ce qui vit à
  travers un appel, pas seulement aux valeurs de retour ; (d) la
  résolution du mystère est venue de la CONFRONTATION de trois preuves
  indépendantes (journal L4D=1, géométrie scrollbar au pixel, capture
  VLM) — jamais de l'octet seul.
- **Alternatives rejetées** : relire w/h depuis la pile RECT après le
  premier appel (les slots [rsp+0x20/0x28] SERVENT d'arguments 5/6 aux
  MoveWindow : le RECT y est détruit par le premier appel — c'est
  précisément pourquoi les valeurs vivaient en registres) ; recalculer
  via GetClientRect deux fois (deux appels de plus pour rien : les
  callee-saved règlent la question gratuitement) ; clobber aléatoire
  des volatiles au shim (non reproductible : le sentinel D38 — r10=0,
  r11=0x246 — est déterministe ET réaliste, la falsification V5 repose
  dessus).
- **Développement** : entrée 26 du journal de travail. Validation terrain
  attendue : bouton « TOUT DÉMARRER » VISIBLE sous la zone journal dès le
  lancement (éventuellement après rétablissement de la fenêtre), clic =
  démonstration intégrale (miroir 16 lignes + « boucle § 5 complète —
  DÉMO OK »), journal + capture à renvoyer. Si vert : scellage final
  0.3.0 (M2).

### D39 — demo.4 mort au premier VirtualProtect : tcp-07:R2 (protection RWX), oracle durci sur le DEP réel

- **Constat** (terrain Windows 11, dossier Drive « test », 26/10/2026
  21:53 — journal 298 o reçu 10 min après livraison) : le journal demo.4
  livre la séquence la plus avancée jamais vue sur terrain réel — L00
  (0.3.0-demo.4), L02, L4C=1, L4D=1, L01 (D37/D38 confirmés), **L03 clic :
  lancement du scenario** (LE BOUTON A ÉTÉ CLIQUÉ — D38 validé), J_ENTETE,
  J_PROTO, « porte R10 : intégrité VERTE », « libc M1 scellée : 4/4 verts »
  (porte + libc scellées M1 exécutées sur machine réelle) — puis RIEN :
  ni J_MEC_OK, ni J_SRV_OK, ni aucun chemin d'échec tracé (J_DEF_KO
  absent). Le scénario est entré dans la phase mécanique et n'en est
  jamais ressorti. L'écart de 10 lignes est EXACTEMENT à la frontière
  J_LIBC_OK → mécanique : un arrêt utilisateur aléatoire n'aurait pour ainsi
  dire jamais coupé dans un intervalle de quelques microsecondes.
- **Diagnostic (audit octet scripts/audit_demo_dep.py, sans Windows)** :
  la phase mécanique appelle tcp-07 (patch à chaud) pour la PREMIÈRE FOIS
  sur machine réelle. Le bloc passait la page 0x4000 — qui contient
  tcp-07 LUI-MÊME (slot 0x4400), l'écho (0x4600) et la croissance
  (0x4680) — en PAGE_READWRITE (constante 4, sites 0x446E application et
  0x44FA rollback) pour écrire le remplaçant, puis la restaurait en
  PAGE_EXECUTE_READ (0x20). Or demo.exe est PE32+ AMD64 avec NX_COMPAT
  explicite : en 64 bits le DEP est PERMANENT et PAGE_READWRITE est SANS
  bit execute. Au retour du premier VirtualProtect, l'instruction
  suivante (`add rsp, 8` @ 0x4551, dans la page devenue non exécutable)
  est fetchée → violation DEP/NX → exception non gérée → MORT DU
  PROCESSUS, nette et silencieuse. Le journal gèle à la dernière ligne
  flushée : J_LIBC_OK — correspondance EXACTE avec le terrain. Cinquième
  classe de défaut invisible sans exécution : **la sémantique de
  protection mémoire du système, non modélisée par l'oracle** (le shim
  VirtualProtect renvoyait 1 sans appliquer les permissions — mensonge
  par omission).
- **Pourquoi toute la chaîne était verte** : notation et round-trip (les
  octets sont exactement la spec), porte R10 (les octets scellés sont les
  octets embarqués — le code était FAUX mais fidèle à lui-même),
  cristallisation et conformité 124/124 (aucun contrôle ne raisonne la
  sémantique DEP de VirtualProtect), oracle M2/démo (le shim admettait
  TOUTE valeur de protection et n'appliquait RIEN : la page restait RWX
  en Unicorn, le fetch post-retour survivait). La spec tcp-07:R1 Q4
  exigeait elle-même PAGE_READWRITE : le défaut vivait DANS le contrat
  écrit — la révision devait corriger la SPEC d'abord (écrite-avant-code,
  y compris pour la réparation).
- **Correctif (tcp-07:R2, diff de DEUX constantes)** : les phases
  d'écriture passent en **PAGE_EXECUTE_READWRITE (0x40)** — écriture ET
  exécution, la page reste exécutable en continu — les restaurations
  restent en PAGE_EXECUTE_READ (0x20). Q4 réécrite, invariant nouveau I6 :
  « toute protection appliquée à une page contenant du code en cours
  d'exécution RETIENT le bit execute ». Signature, codes, effets et
  atomicité inchangés (R4). Cascade de scellage exécutée intégralement :
  spec R2 écrite avant code → brouillon + notation régénérés (diff
  chirurgical : 2 octets + en-têtes) → echo.exe reconstruit →
  **0.3.0-rc.3 scellée** (oracle 50 532 cas verts AVEC permissions
  réelles, cristallisation 10/10 graines 1-10, conformité 124/124
  re-exécutée VERTE, amendement anti-rollback D39 : reconstruction
  autorisée EXACTEMENT pour rc.2 → rc.3) → demo.5 construite sur
  l'héritage rc.3 (16 blocs + staging octet-identiques, R7).
- **Oracle durci (M2 50 532 cas +1 ; démo 79 cas +1) — le vrai
  correctif** : le shim VirtualProtect APPLIQUE désormais les permissions
  (mem_protect + invalidation TCG ciblée, granularité page fidèle :
  0x04 → RW sans execute, 0x20 → RX, 0x40 → RWX ; valeur inconnue ou
  refus piloté → échec SANS effet, comme le vrai Windows). Fidélité
  vérifiée expérimentalement AVANT d'écrire le durcissement
  (scripts/test_unicorn_dep.py, 5 scénarios) : fetch depuis page RW =
  faute ; écriture émulée en page RW = permise ; re-protection RWX =
  l'exécution revient. Conséquences : (a) le code défaillant R1 FAUT
  maintenant en émulation exactement là où il mourait sur terrain ;
  (b) `_ecrire_image` déverrouille l'image avant réécriture (un test
  antérieur peut laisser la page 0x4000 en RX) ; (c) falsification V7
  des deux côtés : la constante 0x40 réécrite en 0x04 (le défaut
  terrain exact) DOIT faire fauter l'émulation — la falsification démo
  appelle tcp-07 DIRECTEMENT car par le scénario, la porte R10
  détecterait l'octet corrompu AVANT la mécanique (la falsification vise
  la sémantique DEP, pas l'intégrité) ; (d) l'oracle démo vérifie
  désormais l'appariement RWX/RX des 8 VirtualProtect du scénario
  complet (mécanique + trafic).
- **Portée** : echo.exe portait le même défaut (sa commande console
  « patch » se serait écrasée pareillement) — le terrain n'avait jamais
  exécuté le patch (constat M2 partiel : bannière seule). echo-0.3.0-rc.3
  livré au coffre avec la demo.5. Le défaut était INVISIBLE à la porte
  R10 par construction : R10 garantit que les octets embarqués sont les
  octets scellés, pas que les octets scellés sont sémantiquement justes
  vis-à-vis du système — seule l'exécution fidèle peut trancher.
- **Enseignements protocolaires** : (a) un shim système qui ne fait
  qu'acquitter un appel ment par omission — chaque argument d'une API a
  une sémantique que l'oracle doit appliquer, pas seulement le code de
  retour ; (b) l'auto-référence rend les défauts de protection
  systemiques : tcp-07 protège la page qui le contient, donc TOUTE
  valeur sans bit execute est fatale — le patcheur fait partie des
  patchés ; (c) la frontière du journal (couper entre deux lignes
  d'intervalles de durée très différentes : µs pour la mécanique, ms
  pour le réseau) est elle-même une preuve — l'analyse d'un journal gelé
  doit commencer par localiser l'intervalle mort ; (d) la révision
  écrite-avant-code s'applique aussi aux RÉPARATIONS : la spec R1 était
  fausse, c'est elle qu'il fallait réviser d'abord.
- **Alternatives rejetées** : PAGE_READWRITE + exécution depuis une autre
  page (le helper .protger vit DANS la page protégée : il faudrait
  déménager tcp-07 hors page 0x4000 — révolution d'adressage pour une
  constante) ; VirtualProtect par BYTE (granularité page : impossible,
  et l'étendue 0x700 couvre déjà le minimum vital) ; laisser la page RWX
  en permanence (violation W^X permanente de l'image : la restauration
  RX après chaque écriture reste exigée par Q4/I2) ; modéliser le DEP
  par simple vérification statique des constantes (sans application
  réelle, un futur bloc utilisant une protection invalide passerait
  encore).
- **Développement** : entrée 27 du journal de travail. Validation terrain
  attendue : run demo.5 → journal complet 17 lignes jusqu'à « boucle § 5
  complète — DÉMO OK » → si vert : scellage final 0.3.0 (M2) sur
  preuve intégrale.

### D40 — demo.5 meurt encore à la frontière mécanique après correctif DEP : instrumentation par sondes (win-09:R2), 6e classe de défaut invisible

- **Constat terrain** : journal demo.5 (298 o, 10 lignes, md5 49671b8e…) —
  L00 confirme « 0.3.0-demo.5 » : c'est BIEN le binaire corrigé DEP qui a
  tourné. Démarrage complet, clic (L03), porte R10 VERTE, 4/4 libc verts —
  puis silence après J_LIBC_OK, NI J_MEC_OK NI ligne d'échec (tous les
  chemins d'échec du scénario journalisent : la mort est un crash
  silencieux, pas un arrêt propre). Même frontière que demo.4, mais le
  défaut DEP (D39) est corrigé : la mort est ailleurs, DANS la mécanique.
- **Audit exhaustif SANS DÉFAUT TROUVÉ** : (a) binaire fidèle à la
  notation (and rcx,~0xFFF encodé 64 bits sign-étendu, VirtualProtect
  apparié RWX/RX, retour vérifié, alignement pile exact) ; (b) payload v2
  (staging c30014) TOTALEMENT position-indépendant — hypothèse ASLR du
  payload morte ; (c) PE DYNAMIC_BASE+HIGH_ENTROPY_VA mais .reloc vide
  (0xC o) : chargement à la base préférée 0x140000000, comme l'oracle ;
  (d) chaînes v1/v2 cohérentes, checksum staging conforme (wrapping 64) ;
  (e) IAT 0x20D0 = VirtualProtect confirmée ; (f) oracle différentiel
  re-exécuté VERT (79 cas, permissions réellement appliquées, clobber
  actif, falsifications 28/28). Le défaut appartient à une classe que
  NI l'audit statique NI l'émulation ne peuvent voir : 6e classe
  (après géométrie D36, ABI volatiles D38, DEP D39…) — l'écart
  environnement réel/émulation ne se révèle qu'à l'exécution terrain.
- **Décision** : INSTRUMENTER (méthode D36/D37 qui a résolu le bouton
  invisible). win-09:R2 ajoute TROIS sondes de trace (entrée trace
  win-05, mode 0, ASCII) qui encadrent chaque étape jamais exécutée sur
  le terrain : sonde1 avant le premier appel écho (entrée mécanique),
  sonde2 après le retour 0 du patch pose (tcp-07 mode 0 COMPLET),
  sonde3 après le memcmp de l'écho patché (v2 confirmé). Chaque sonde
  écrit le fichier journal AVANT l'étape suivante : la dernière sonde
  visible localise l'instruction mortelle. Sondes TEMPORAIRES (retirées
  en R3 après correction).
- **Contraintes d'ingénierie résolues** : (a) budget code : 3 sondes ×
  20 o = 60 o > padding win-09 (67-16) → slot win-09 élargi 0x380→0x3C0
  dans le trou libre 0x4F80-0x4FFF (aucun bloc déplacé, D8 respecté,
  padding final 71 o) ; (b) budget .rdata : zones UTF-16 (14 o) et ASCII
  (2 o) PLEINES → sondes posées dans les interstices libres jamais lus
  par le chargeur (0x2748 INT k32#2→reloc, 0x276C reloc→INT user32,
  0x22F1 hint FFB→IAT ws2 — précédent : les hints D36 vivent déjà en
  interstices) ; (c) sondes en mode 0 avec r8d explicitement mis à zéro
  (le mode est passé tel quel à win-11 : garbage ≠ déterministe interdit).
- **Oracle durci en conséquence** : le journal nominal attendu du
  scénario passe à 14 lignes (11 + 3 sondes intercalées après J_LIBC_OK,
  écran et fichier) — l'oracle exécute les sondes et vérifie leur texte
  exact ; verrou structurel : entrée trace win-05 (0x5000) déclarée dans
  les appels autorisés de win-09 ; sondes ajoutées aux données RIP
  autorisées. Build 0.3.0-demo.6 : 79 cas verts, falsification 28/28,
  héritage R7 intact (16 blocs + staging), carte re-scellée génération 4.
- **Valeur de preuve croisées** : le LISEZMOI demande en plus du journal
  (a) une capture d'écran de la fenêtre après l'arrêt (l'écran et le
  fichier peuvent diverger d'une ligne — divergence = information : mort
  dans l'écriture journal elle-même) et (b) l'état de la fenêtre
  (disparue = mort processus ; figée = blocage). Trois lectures
  indépendantes du même événement.
- **Alternatives rejetées** : instrumenter tcp-07 (casserait l'héritage
  octet-identique R7 — le bloc est scellé M2) ; instrumenter via l'entrée
  scénario UTF-16 (zone .rdata pleine) ; deux sondes au lieu de trois
  (laissait l'écho#1/memcmp#1 sans encadrement — jamais exécutés sur
  terrain avant demo.4) ; rapatrier un crash dump Windows (outillage
  lourd côté développeur, le journal suffit à localiser l'intervalle).
- **Développement** : entrée 28 du journal de travail. Validation terrain
  attendue : journal demo.6 avec sondes → l'intervalle mort identifié →
  correctif ciblé + retrait des sondes (R3) → scellage final 0.3.0.

### D41 — terrain demo.6 parle : mort après sonde1 localisée à la POSE — .protger appelait VirtualProtect SANS zone d'accueil ABI (ret empoisonné vers 0x700) ; tcp-07:R3, 7e classe de défaut invisible

- **Constat terrain** : journal demo.6 rapatrié (dossier test Drive,
  317 o, 12 lignes, md5 0d4cd4d1…) + état de la fenêtre rapporté par
  le développeur : « fenêtre disparue (crash) » = MORT DU PROCESSUS,
  pas un blocage. L00 confirme demo.6 ; démarrage complet, clic L03,
  porte R10 VERTE, libc 4/4 verts — puis « sonde1 avant echo »
  (écriture COMPLÈTE, CRLF final présent) et plus RIEN. L'instrumentation
  D40 a fonctionné exactement comme conçue : la mort est dans
  l'intervalle écho#1 | memcmp#1 | POSE tcp-07.
- **Élimination statique** : (a) écho v1 (@0x4600) désassemblé — 11
  instructions, boucle de copie octet par octet pure (mov r10b,[rdx+r9] /
  mov [rcx+r9],r10b), aucun appel, aucune pile, bornes exactes (dest =
  pile, src = .rdata, 14 o) — NE PEUT PAS fauter ; (b) memcmp (libc-02)
  déjà EXÉCUTÉ AVEC SUCCÈS sur le terrain quelques µs plus tôt (sceau
  4/4 verts) — restait la POSE.
- **Défaut trouvé (byte-exact)** : `.protger` (tcp-07 @0x4531) appelait
  VirtualProtect par IAT avec `sub rsp, 8` — l'alignement était PARFAIT
  (rsp ≡ 0 mod 16 au call) mais les **0x20 octets de zone d'accueil ABI
  msx64 (shadow space) n'étaient PAS réservés**. Le code système Windows
  est compilé `/homeparams` : kernel32!VirtualProtect range ses 4
  arguments dans la zone d'accueil de l'appelant — rdx (0x700, la taille
  de page) atterrit EXACTEMENT sur l'adresse de retour de .protger ;
  son `ret` saute à l'adresse 0x700 → violation d'accès → processus
  mort, fenêtre disparue, journal gelé après sonde1. Correspondance
  EXACTE avec le terrain. **7e classe de défaut invisible sans
  exécution** : obligation ABI CÔTÉ APPELANT que le shim Python de
  l'oracle ne modélisait pas (il n'écrit jamais dans la zone d'accueil).
  Le correctif D39 (DEP) MASQUAIT celui-ci : la faute NX survenait au
  retour du premier VirtualProtect, AVANT le ret empoisonné.
- **Audit systémique** (scripts/audit_shadow_space.py, tracké) : les
  58 sites d'appel IAT/pointeur du binaire audités un par un — 57 sains,
  EXACTEMENT 1 défaillant (le call VirtualProtect de .protger) ; les
  appels ws2_32 jamais exécutés au terrain (serveur/client) sont
  ABI-conformes : la correction ouvre la route jusqu'au bout de la
  démonstration, pas d'un cran.
- **Correctif écrit-avant-code — tcp-07:R3** : I4/I5 précisés, **I7**
  ajouté (.protger réserve 0x28 = 0x20 accueil + 0x8 alignement ; la
  zone d'accueil ne peut jamais recouvrir l'adresse de retour ni la
  loge old-protect, déménagée à [rsp+0x20]) ; **V8** ajouté (falsification
  shadow space : 0x28→0x08 aux deux sites = le défaut terrain exact →
  l'émulation DOIT fauter au ret) ; V2 amendé. Diff limité à .protger :
  sub rsp 8→0x28, lea r9 [rsp+0x38]→[rsp+0x20], add rsp 8→0x28 —
  3 octets, AUCUN déplacement déplacé (le call [rip-0x2481] est
  inchangé), signature/codes/effets inchangés (R4).
- **Oracles durcis (M2 + démo)** : le shim VirtualProtect modélise
  désormais /homeparams — il range les 4 arguments dans la zone
  d'accueil de l'appelant AVANT tout effet : le défaut démo.6 rejoué en
  émulation FAUTE au ret (saut vers 0x700 non mappé). L'oracle M2
  passe à 50 533 cas (+1 V8), l'oracle démo à 80 cas (+1 V8).
- **Cascade M2** : layout 0.3.0-rc.4 (u64 0x00030005), amendement
  anti-rollback D41 (reconstruction autorisée EXACTEMENT rc.3→rc.4),
  cristallisation 10/10 (graines 1-10), conformité 124/124 re-exécutée
  VERTE → **0.3.0-rc.4 scellée** (echo.exe sha256:da4a6ca2…fdb2 — le
  serveur console portait le même défaut, il est corrigé).
- **demo.7** : build héritage rc.4 — round-trip 192/192, 565 verrous
  structurels, héritage R7 intact (16 blocs + staging octet-identiques
  echo rc.4), 80 cas verts, falsification 28/28, carte re-scellée.
  demo.exe 16 384 o, sha256:1917c9af…ffff (md5 89cf9e23…). **Sondes
  CONSERVÉES** (D40) : le run terrain doit maintenant montrer
  sonde1 → sonde2 → sonde3 → mécanique → … → « boucle § 5 complète —
  DÉMO OK » — la lecture du correctif est elle-même une preuve ; le
  retrait des sondes (R3 final) suivra le constat.
- **Audit final** (scripts/audit_demo7.py, tracké) : sondes 3/3
  conformes, L00 demo.7, u64 0x00030107, DEP intact (2× 0x40, 0
  résiduel), séquence .protger EXACTE (I7), diff demo.6→demo.7
  CHIRURGICAL : 7 octets (3 code + version u64 + L00 + 2 somme R10).
  audit_shadow_space.py : 58/58 sites sains, .protger D41 conforme.
- **Alternatives rejetées** : homeparams dans TOUS les shims (les 57
  autres sites sont prouvés sains — statique + terrain — le durcissement
  ciblé VP + l'audit systémique couvrent la classe sans risque de
  régression) ; ajouter une 4e sonde entre memcmp et la pose (l'élimination
  statique rendait la fenètre déjà monotonique : la pose était le seul
  suspect restant) ; reconstruire .protger avec push/pop (diff plus
  large, aucun bénéfice).
- **Développement** : entrée 29 du journal de travail. Validation
  terrain attendue : journal demo.7 complet 14 lignes jusqu'à
  « boucle § 5 complète — DÉMO OK » → scellage final 0.3.0 (M2) + retrait
  des sondes.

### D42 — terrain demo.7 parle : la mécanique est franchie (sondes 3/3, serveur écoute, client connecté) mais le processus meurt au premier échange — la section critique R_CS n'a JAMAIS été initialisée dans l'hôte démo (devoir de tcp-12 non repris) ; win-09:R3, 8e classe de défaut invisible

- **Constat terrain** : journal demo.7 rapatrié (dossier test Drive,
  435 o, 16 lignes, md5 da86c16f…) + « fenêtre disparue » = MORT DU
  PROCESSUS, comme demo.6. L00 confirme demo.7 ; démarrage complet,
  clic L03, porte R10 VERTE, libc 4/4 verts, **sonde1 → sonde2 →
  sonde3** (le correctif D41 VIT : la pose du patch, l'écho patché et
  le rollback sont franchis), « mécanique : v1>v2>v1 confirmés »
  (première terrain), « serveur : écoute » et « client : connecté »
  (premières terrain) — puis plus RIEN, dernière ligne complète
  (é CP1252 + CRLF finaux : pas de troncature), AUCUNE ligne d'échec
  E5. La mort est VIOLENTE, dans le premier échange réseau ou en
  concurrence dans le fil d'écho serveur.
- **Élimination statique** : (a) win-10-echange relu à la main —
  alignement conforme (5 pushes + sub rsp,0x40 → rsp ≡ 0 mod 16 aux
  deux appels IAT), zone d'accueil conforme (tampon de réception
  [rsp+0x20, rsp+0x40), hors de l'ombre), boucles bornées, échecs
  propres ; l'audit D41 (58/58 sites) couvrait ses appels. (b) les
  wrappers tcp-03/04/02 relus — sub rsp,0x28 (zone d'accueil +
  alignement) chaque fois. (c) tcp-06-spawn relu — les 6 arguments de
  CreateThread exacts (5e/6e aux loges [rsp+0x20]/[rsp+0x28]) ;
  spawn#1 (win-08) avait déjà VÉCU au terrain (« serveur : écoute »
  le prouve). (d) tcp-09-conn relu — prologue 5 pushes + sub rsp,0x460
  (aligné), tampon [rsp+0x30] de 1072 o ≥ 1024 requis, zone d'accueil
  libre, échecs propres. Rien à reprocher aux CODES.
- **Défaut trouvé (byte-exact)** : **la section critique R_CS
  (0x3830, .data) est zéro dans l'image et n'est initialisée par
  PERSONNE dans demo.exe**. Le grep de toute la lignée ne trouve
  qu'UN seul initialiseur : tcp-12-main (IAT 0x20D8) — or tcp-12 est
  le bloc orchestrateur console REMPLACÉ par win-01/win-04 lors de
  l'embarquement démo (« tcp-10 et tcp-12 NON embarqués », layout
  démo). La pre-condition **P5 de tcp-11** (journal console, appelé
  par tcp-09 après CHAQUE réception) exige « la section critique
  .data (R_CS) est initialisée … par tcp-12 » : l'hôte démo a repris
  le caching des handles (P4, win-09) mais PAS l'initialisation de
  la CS. Au premier échange : le client envoie, le serveur accepte,
  spawn tcp-09, recv réussit, tcp-09 appelle tcp-11 pour journaliser
  « echo 14 » → **EnterCriticalSection sur une CS vierge** : sous
  Windows 10/11, une CS initialisée a LockCount = -1 (libre) ; une CS
  zéro a LockCount = 0 (« verrouillée ») et OwningThread = 0 — le
  chemin de contention de ntdll (RtlpWaitOnCriticalSection) reçoit un
  état impossible et lève une exception non gérée : le fil d'écho
  meurt, Windows tue le PROCESSUS entier (une exception dans n'importe
  quel fil est fatale), la fenêtre disparaît, et le client — bloqué
  dans recv — n'a jamais pu écrire la moindre ligne E5.
  Correspondance EXACTE avec le terrain, timing inclus. **8e classe
  de défaut invisible sans exécution** : pré-condition d'état hérité
  non reprise par l'hôte lors du retrait d'un bloc orchestrateur
  scellé — et doublement invisible à l'oracle, dont les shims de
  section critique étaient des no-ops sans état ET qui n'exécutait
  JAMAIS tcp-09 (le recv du client « reflétait » l'état du patch en
  court-circuitant le fil serveur).
- **Correctif écrit-avant-code — win-09:R3 (couche démo, AUCUNE
  cascade M2)** : la faute est dans l'HÔTE, pas dans les blocs scellés
  (echo.exe est correct : tcp-12 y initialise la CS). I0 ajouté :
  InitializeCriticalSection(R_CS) est le PREMIER appel du scénario —
  avant GetStdHandle, avant tout journal, avant tout spawn — le
  miroir exact du devoir de tcp-12, placé au plus tôt du fil qui
  orchestre toute la démonstration. P5 ajouté au contrat. Diff :
  2 instructions (lea rcx,[rip+R_CS] + call IAT 0x20D8), 13 octets.
- **Oracle durci (démo)** : (a) shims à état — InitializeCriticalSection
  enregistre l'adresse, EnterCriticalSection sur CS non enregistrée
  LÈVE (le défaut demo.7 rejoué en émulation : V9) ; (b) tcp-09
  exécuté POUR DE VRAI pour la première fois (recv scripté par file
  d'attente, écho réel, tcp-11 réel, send observé, fermeture) ;
  (c) contrôle post-run du scénario : la CS DOIT figurer dans l'état
  des initialisations (toute régression du correctif est détectée) ;
  (d) falsification V9 : tcp-09 sur CS vierge DOIT fauter.
- **Instrumentation bilatérale conservée (D40/D41) + étendue** :
  sondes 1-3 inchangées ; win-08:R2 ajoute S1 (accept retourné) et
  S2 (fil écho lancé) côté serveur ; win-10:R2 ajoute sonde4 (émission
  complète) et sonde5 (réception complète) côté client — la dernière
  sonde visible localise toute mortalité résiduelle à l'intervalle
  près, des deux côtés de la socket. Risque accepté et consigné :
  le fil serveur journalise via win-05 en concurrence avec le fil
  scénario (tampons .data non réentrants — au pire une ligne mélangée,
  jamais un crash ; l'ordre S1/S2 autour de « client : connecté »
  n'est pas garanti au terrain, toutes combinaisons interprétables).
  Chaînes des 4 nouvelles sondes dans la zone libre M2 0x266E-0x26D8
  (chaînes tcp-10/12 non posées dans la démo, jamais lues par le
  chargeur). Journal nominal attendu au terrain : 28 lignes.
- **Alternatives rejetées** : initialiser la CS dans win-01 (entrée
  processus — correct mais touche le point d'entrée pour un état dont
  le seul consommateur vit en aval du scénario ; win-09 est l'équivalent
  structurel de tcp-12) ; initialiser la CS dans win-08 avant le
  premier spawn (fonctionnellement suffisant mais place le devoir
  d'héritage dans un fil de service plutôt que chez l'orchestrateur) ;
  réviser tcp-11 pour se passer de CS (bloc M2 scellé — R6/R7 :
  la faute est dans l'hôte) ; retirer l'appel tcp-11 de tcp-09 (idem,
  scellé) ; poser une CS pré-initialisée dans l'image .data (l'état
  initialisé exact d'une CRITICAL_SECTION dépend de la version de
  Windows — l'API est la seule voie portable).
- **Développement** : entrée 31 du journal de travail. Validation
  terrain attendue : journal demo.8 complet 28 lignes jusqu'à
  « boucle § 5 complète — DÉMO OK » → retrait de TOUTES les sondes
  (R3/R4 finales) + scellage final 0.3.0 (M2).

### D43 — terrain demo.8 : « boucle § 5 complète — DÉMO OK » (28/28 lignes, sondes vertes des deux côtés) — la boucle § 5 est DÉMONTRÉE sur machine réelle ; retrait de TOUTES les sondes (demo.9 finale de lignée) + scellage final M2 0.3.0

- **Constat terrain** : journal demo.8 rapatrié (dossier test Drive,
  706 o, 28 lignes exactement comme attendu, md5 84f5d58e…, CRLF
  final propre). L00 confirme demo.8 ; démarrage complet, clic L03,
  porte R10 VERTE, libc 4/4 verts, sondes 1→2→3, « mécanique :
  v1>v2>v1 confirmés », « serveur : écoute 127.0.0.1:25000 »,
  « client : connecté », puis **S1 accept ok / S2 fil echo lance**
  (lus APRÈS « client : connecté » : la course documentée de D42,
  résolue sans incident — aucune ligne mélangée), puis **sonde4/
  sonde5 autour de CHACUN des trois échanges** : « écho réseau :
  aller-retour exact » (identité), « patch en production :
  MAJUSCULES » (patch posé PENDANT le trafic, réponse v2 vérifiée
  par memcmp), « retour arrière : identité confirmée » (rollback,
  re-vérification), et **« boucle § 5 complète — DÉMO OK »**.
  Le correctif D42 est VALIDÉ au terrain : le premier échange —
  le point de mort de demo.7 — a vécu (la CS initialisée par
  win-09:R3 a tenu sous EnterCriticalSection réel de Windows 11).
- **La cascade terrain close (8 classes de défauts, demo.1→demo.8)**
  : (1) WM_SIZE lisait RECT.top comme largeur (D36, fenêtre vide) ;
  (2) traces fichier seul, écran muet (D37, jumeau silencieux) ;
  (3) w/h en volatiles relus après l'appel (D38, bouton invisible) ;
  (4) phase de patch sans execute (D39, DEP) ; (5) défaut latent
  sans exécution (D40, méthodologie des sondes) ; (6) zone d'accueil
  ABI absente de .protger (D41, ret empoisonné vers 0x700) ; (7)
  … (D41 : la POSE localisée par sonde) ; (8) section critique
  héritée jamais initialisée (D42). Chaque classe a été nommée,
  corrigée byte-exact, et rendue impossible à réintroduire
  (falsifications V4-V9 + audits). HUIT lectures de journal terrain
  en deux jours, zéro run supplémentaire demandé après demo.7
  (D42 trouvé par lecture des octets).
- **Retrait des sondes — specs écrites-avant-code (win-08:R3,
  win-09:R4, win-10:R3)** : l'instrumentation avait un devoir
  TEMPORAIRE (D40 : « retirées en R3 après correction ») — le
  constat vert l'acquitte. Les 7 sondes (140 o de code : lea/mov/
  xor/call ×7) sont retirées : win-08 retrouve son orchestration
  nue (accept → spawn → CloseHandle, discipline r12/r13 conservée),
  win-09 journalise EXACTEMENT ses 11 lignes de preuve (le correctif
  D42 — init R_CS en tête — RESTE : c'est un devoir d'héritage, pas
  une sonde), win-10 redevient muet (séquence R1 : boucle émission →
  boucle réception → memcmp). Les 7 chaînes de sondes (105 o) sont
  retirées des zones libres .rdata (interstices D40 + zone libre M2
  D42) qui reviennent à zéro — CHAINES_SONDES vidé dans le plan
  d'adressage, aucun symbole SONDE_* résoluble (une référence
  résiduelle fait échouer la résolution d'auteur).
- **Anti-régression du retrait (oracle durci)** : le chemin nominal
  de win-08 est MUET (toute ligne au journal = échec) ; le journal
  du scénario doit être EXACTEMENT 11 lignes (toute sonde
  réintroduite = divergence) ; les falsifications V4-V9 (RECT,
  miroir D37, volatils D38, DEP D39, zone d'accueil D41, CS vierge
  D42) restent toutes vivantes. 86 cas verts, falsification 28/28
  blocs détectés, oracle structurel 561 verrous.
- **demo.9 (0.3.0-demo.9, u64 0x00030109 — FINALE de lignée)** :
  16 384 o, md5 73c064fb…, sha256 df8f2e50…. Audit final
  (scripts/audit_demo9.py, tracké) TOUT CONFORME : 7 zones de sondes
  à zéro, L00 demo.9, correctif D42 vivant (lea → 0x3830, call →
  IAT 0x20D8, AVANT GetStdHandle), 0 appel trace depuis les trois
  blocs (win-02/04 intacts : 3+7 appels légitimes), win-10 séquence
  R1, héritage D41 intact (0x40 ×2, sub/add rsp,0x28, lea
  r9,[rsp+0x20], zéro résiduel), **diff demo.8→demo.9 CHIRURGICAL :
  1 047 o (916 code des 3 blocs révisés + 131 données : sondes
  retour zéro, L00, u64, sommes R10), 0 octet hors zones
  autorisées**. Héritage R7 intact : 16 blocs + staging
  octet-identiques aux artefacts scellés M0/M1/M2.
- **Scellage final M2 0.3.0** : la conformité 1-7 ré-exécutée VERTE
  (124/124) puis la balise basculée rc.4 → 0.3.0 dans frag-bld
  (fail-closed : la balise rc.4 devait exister EXACTEMENT une fois),
  carte re-chiffrée et re-signée Ed25519 — immuable § 9 (défaut →
  0.3.1 à contrat stable, R4). echo.exe reste l'artefact rc.4
  byte-identique (le scellage final est une opération de CARTE,
  modèle M1 0.2.0). **Le jalon M2 est clos : boucle § 5 complète
  (patch à chaud en production + rollback) démontrée sur machine
  réelle, conformité 124/124, carte signée, cristallisation 10/10,
  journal à jour.**
- **Journal terrain final attendu (formalité)** : 17 lignes (6 de
  démarrage GUI : L00/L02/L4C/L4D/L01/L03 + 11 de preuve) — le
  développeur peut relire la démonstration propre, sans
  instrumentation ; toute divergence serait un constat neuf (et le
  binaire livré est exactement celui audité ci-dessus).
- **Alternatives rejetées** : garder les sondes dans la finale
  (bruit permanent + concurrence de fils documentée comme risque —
  le retrait était promis en D40/D42) ; renuméroter la démo 0.3.0
  (la lignée démo a son propre schéma u64 0x0003_01xx, monotone —
  la confusion avec l'artefact atelier 0x3_0000 serait une
  régression de lisibilité) ; reconstruire echo.exe avec la balise
  0.3.0 dans le binaire (le scellage final est un fait de CARTE,
  l'artefact rc.4 est l'objet validé au terrain — le reconstruire
  invaliderait les empreintes scellées pour un cosmétique).
- **Développement** : entrée 32 du journal de travail. M2 clos —
  prochain jalon M3 (contrats renforcés sur entrées non fiables,
  fuzzing systématique).

### D44 — révision v0.5.0 du protocole : la validation terrain devient couche de vérification normée ; taxonomie étendue X1–X8 des défauts invisibles à l'émulation ; jalons M0–M2 constatés ; corrections

- **Statut** : active · **Date** : 27 octobre 2026
- **Contexte** : demande développeur « rédige une nouvelle version, mise à jour et
  corrigée, académique et complète du protocole Triade puis M3 ». La v0.4.0 datait
  d'avant la cascade terrain : elle décrivait M0 comme « à démarrer » et ne disait
  rien des huit classes de défauts que la campagne M2 venait de nommer — le
  protocole était en retard sur ses propres leçons.
- **Choix retenu** : révision v0.5.0 du protocole (markdown source de vérité +
  PDF formel LaTeX/Tectonic, chaîne spec_v040 → spec_v050) : (1) § 8.4 norme la
  VALIDATION TERRAIN — boucle d'évidence en cinq éléments (journal d'exécution
  écrit après vérification, lecture asymétrique, instrumentation contractualisée
  avec retrait promis, diff chirurgical audité, archive brute empreintée) ; (2)
  § 8.5 fixe la taxonomie X1–X8 des défauts invisibles à l'émulation — une classe
  par décision D35–D42 (chargeur, lecture de structure, canal de vérité, ABI
  caller-saved, protections mémoire, écart émulation/terrain, obligations ABI de
  l'appelant, état hérité), chacune gardée par une falsification permanente, la
  taxonomie restant OUVERTE (X9 sera nommée, jamais dissimulée) ; (3) § 16
  constate les jalons M0/M1/M2 FRANCHIS avec dates, balises et preuves ; (4)
  corrections : budget de localisation 40 → 64 tokens dans le tableau de bord
  (incohérence résiduelle de la v0.4.0 malgré D31), valeurs mesurées affichées
  (51/719/1 088), coquille « converts », huit défauts typographiques du PDF
  (ponctuation en début de ligne), apostrophes normalisées dans le vérifieur ;
  (5) § 17.3/17.4 tracent les huit évolutions et quatre rejets de la révision ;
  (6) le journal des décisions du protocole (§ 16 du PDF) est étendu D33 → D45.
- **Académique** : la lecture structurante est explicitée — un oracle différentiel
  valide la conformité d'un artefact à un MODÈLE d'environnement ; la validation
  terrain valide le MODÈLE lui-même ; les deux couches sont complémentaires
  (entrées à coût nul vs environnements au coût d'un run) et le protocole exige
  les deux. C'est la formalisation de la leçon des 8 classes.
- **Alternatives rejetées** : règle R12 « validation terrain obligatoire » (découle
  de R5 + critères de jalon — dilution inutile) ; fuzzing étendu à tous les blocs
  (M3 cible la surface d'entrées non fiables) ; reconstruire les artefacts 0.2.0/
  0.3.0 pour la doc (balises finales immuables) ; fusionner X dans T (remèdes
  distincts : écrire le contrat vs enrichir le modèle et falsifier).
- **Vérification** : cahier de révision étendu à dix critères — V1–V9 de la v0.4.0
  (hiérarchie intacte, règles non affaiblies, aucune couche d'abstraction, rejets
  consignés) + V10 contenu v0.5.0. Exécution finale : 68 contrôles PASS / 0 FAIL (V1-V10) après
  correction de la normalisation d'apostrophes du PDF dans le vérifieur ; QA PDF
  100 % vert (0 avertissement, contre 8 en v0.4.0).
- **Développement** : entrée 33 du journal de travail.

### D45 — ouverture du jalon M3 : harnais de fuzzing à propriétés (P1-P5) — 101 000 cas SANS CRASH sur la surface d'entrées non fiables scellée ; harnais falsifiable (auto-test : défauts injectés détectés) ; prochaine étape : blocs parseur HTTP à contrats renforcés

- **Statut** : active · **Date** : 27 octobre 2026
- **Contexte** : suite de la demande développeur « … puis M3 ». Le critère M3 —
  « un million de requêtes fuzzées sans crash ; proxy transparent pour curl ;
  contrats renforcés » — exige un HARNAIS avant les blocs M3 : on ne fuzz pas
  ce qu'on ne sait pas observer.
- **Choix retenu** : (1) le harnais (m3/fuzz.py, ~420 lignes, tracké) calibre
  la méthodologie sur la surface d'entrées non fiables DÉJÀ scellée — tcp-09
  (c30009, session serveur M2 : la boucle recv/écho/send consomme des octets
  réseau de longueur et contenu arbitraires) et win-10 (d40010, échange
  client démo : réception cumulative d'une réponse serveur non fiable) ;
  (2) cinq propriétés dérivées des contrats I existants, jamais au-delà :
  P1 survie (aucune faute d'exécution), P2 terminaison bornée, P3
  différentiel (écho == entrée pour tcp-09 ; verdict eax == modèle
  accumulation-14 + memcmp pour win-10), P4 fermeture exactement unique
  (Q2), P5 mémoire (crochet d'écriture Unicorn : pages de code de l'image
  interdites — patch désactivé — et pile sous la profondeur légitime
  interdite, I4) ; (3) architecture : lots de 50 cas par émutateur (état
  recréé), REJEU sur état vierge de tout échec avant consignation (exclusion
  des artefacts de réutilisation), graine maîtresse → scénarios
  reproductibles, six générateurs nommés (aléatoire, tronquatures,
  binaire-hostile — NUL/CRLF/format/pleine capacité —, fragmentation TCP
  1-7 octets, fins prématurées, frontières du tampon 1023/1024/1025).
- **Calibration = leçon D40 inversée** : les premières divergences étaient
  dans le MODÈLE du harnais, pas dans le bloc — recv ne sert jamais plus que
  demandé (cap 1024), et un retour 0 (y compris un item vide) = fermeture du
  pair (Q2), pas une réception nulle à continuer. Deux corrections du modèle
  de référence avant toute campagne — le differential ne prouve que si son
  modèle est fidèle au contrat ; la calibration est l'endroit où cette
  fidélité s'établit.
- **Campagne d'ouverture** : 101 000 cas (60 500 tcp-09 à ~430 cas/s +
  40 500 win-10 à ~4 150 cas/s, graines 1-3) — **ZÉRO échec confirmé** :
  P1-P5 tenues sur toute la surface scellée. Aucune faute, aucune boucle
  infinie, aucun écho divergent, aucune double fermeture, aucune écriture
  hors zone — la surface M2 (écho brut, sans parsing) est sûre PAR
  CONSTRUCTION, ce que la campagne quantifie.
- **Harnais falsifiable (miroir V4-V9)** : --auto-test injecte deux défauts
  d'un octet (tcp-09 : demande recv 1024→768 ; win-10 : longueur memcmp
  14→13) — le harnais DOIT les détecter : 122/300 et 300/300 échecs
  confirmés → PASS. Un harnais qui ne peut pas échouer ne vérifie rien ;
  celui-ci peut.
- **Chemin vers le million** : débit constaté ≈ 39 min pour 10^6 cas tcp-09
  (+ 4 min win-10) — atteignable en une session dédiée. Le million du
  critère M3 s'appliquera au PERIMÈTRE M3 (parseur HTTP + proxy) : le
  harnais est prêt à les accueillir dès leurs blocs.
- **Prochaines étapes M3** : (a) spécifications I écrites-avant-code du
  domaine http-xx (parseur de ligne de requête, en-têtes, limites —
  contrats renforcés : chaque entrée non fiable a un comportement défini,
  échec propre nommé) ; (b) blocs + notation + oracle étendu ; (c) proxy
  transparent (curl) ; (d) campagne million sur le parseur ; (e) le fuzzing
  rejoint la suite de conformité comme contrôle permanent (défauts ouverts
  par classe X au tableau de bord).
- **Alternatives rejetées** : fuzzing en aveugle sans modèle différentiel
  (ne prouve que l'absence de crash, pas la conformité au contrat) ; un
  seul émutateur pour toute la campagne (pollution d'état non exclue — le
  rejeu sur état vierge est la garantie) ; attendre les blocs M3 pour
  construire le harnais (le harnais se calibre sur du scellé connu : toute
  divergence de calibration est un bug de harnais, pas un doute sur le
  binaire).
- **Développement** : entrée 34 du journal de travail.

### D46 — couche I du jalon M3 : treize spécifications écrites-avant-code du domaine http (http-01 à http-12 + tcp-13) — contrats renforcés : chaque octet non fiable a un comportement défini, chaque échec est nommé, aucune tolérance de format n'est silencieuse

- **Statut** : active · **Date** : 27 octobre 2026
- **Contexte** : étape (a) des prochaines étapes de D45 — les blocs
  parseur exigent leurs contrats AVANT la notation (R2, écrite-avant-code ;
  le gabarit § 2.2 de la v0.5.0). Le critère M3 « contrats renforcés »
  n'est pas un slogan : c'est une propriété vérifiable du texte des
  spécifications — chaque entrée non fiable a un verdict, chaque verdict a
  un nom, chaque constante a un propriétaire unique.
- **Choix retenu** : (1) **décomposition en verbes uniques** : treize
  spécifications — huit parseurs feuilles purs (http-01 itérateur CRLF
  [propriétaire T5 du balayage de ligne], http-02 ligne de requête [la
  table des huit méthodes EST la validation], http-03 ligne d'en-tête
  [OWS rognés en bornes, jamais en recopie], http-04 recherche d'en-tête
  [l'unique comparaison insensible à la casse du domaine, obligation RFC
  7230 §3.2], http-05 décimal borné [test de borne À CHAQUE chiffre],
  http-06 fin de tête [propriétaire de MAX_TETE], http-07 autorité
  [propriétaire T5 du découpage hôte:port, crochets IPv6 exclus de la
  valeur], http-08 cible [formes absolue/origine/autorité, découpe sans
  interprétation]), une pompe (http-09 : relais unidirectionnel qui ne
  ferme JAMAIS), la session (http-10 : orchestration complète, unique
  propriétaire des fermetures et de la table des réponses), la console
  (http-11 : quit), l'orchestrateur (http-12 : porte R10 + ordre
  d'initialisation D42 en invariant), et l'extension cliente tcp-13
  (getaddrinfo + connect sur cible arbitraire — win-07 de la lignée démo
  était soudé à 127.0.0.1:25000, inutilisable ; la traduction span→chaîne
  C y est propriété unique, exigée par getaddrinfo) ;
  (2) **conventions transverses** (charte m3/I/README.md, liée par renvoi,
  jamais recopiée — T5) : spans partout (aucune terminaison NUL supposée
  sur le réseau), verdicts eax 0/nommés mappés par la table des réponses
  de http-10 (400/411/431/501/502/505 + 200 tunnel), constantes à
  propriétaire unique (MAX_TETE 8192 chez http-06 — RFC 7230 §3.1.1
  exige ≥ 8000 ; MAX_CIBLE 2048 chez http-02 — usage navigateur ;
  HOTE_MAX 255 chez tcp-13 — limite DNS), CRLF strict (LF isolé → 400 :
  la RFC 7230 §3.5 PERMET le LF nu, M3 le refuse — durcissement
  anti-contrebande), zéros de tête rejetés sur Content-Length (RFC 7230
  §5.5.1), schéma « http:// » strict minuscule (durcissement : tous les
  émetteurs réels émettent minuscules), une requête par connexion
  cliente, réponse JAMAIS parsée (relais à fermeture délimitée — ce qui
  n'est pas parsé ne peut pas être mal parsé), fermetures à propriétaire
  unique (session seule, pompes jamais), échec avant l'entrée système
  (rien d'ambigu n'atteint le résolveur) ;
  (3) **réutilisation R7** : proxy.exe embarque les octets scellés
  a10002/a10003, b20001-04, c30001-06 et c30011 (tcp-11 journal) à leurs
  RVA exacts — l'IAT existante est inchangée, deux entrées ws2_32 sont
  appendues (getaddrinfo 0x2350, freeaddrinfo 0x2358) ; tcp-07/08/09/10/
  12 et libc-05/06/07/09 ne sont pas embarqués (le patch à chaud du
  journal revient à M5) ; tcp-13 occupe le trou libre net 0x4200, la
  zone http étend .text2 depuis 0x4C00, http-12 prend le slot
  d'application 0x1800 ; (4) **surface de fuzzing** : http-01..09 +
  chaîne d'accumulation de http-10 — les V3 de chaque spécification lient
  le contrat au harnais P1-P5 de D45 ; la campagne million (étape d)
  vise CE périmètre ; les orchestrateurs relèvent de l'oracle à
  scénarios et du terrain (§ 8.4), pas du fuzz aveugle — ils n'ont pas
  d'entrée non fiable directe ;
  (5) **règles de tranchement notables** : POST/PUT sans Content-Length et
  sans Transfer-Encoding → 411 (RFC) ; Transfer-Encoding présent → 501
  (le relais en flux n'est pas dans le périmètre M3 — refus honnête) ;
  forme origine sans Host → 400 (RFC 7230 §5.4) ; CONNECT sans port → 400
  (pas de schéma, pas de base de déduction — jamais deviner) ; forme
  absolue sans chemin → chemin « / » par DÉFINITION (fixture http-08,
  pas une déduction d'exécution) ; la version du client est relayée
  telle quelle (span d'origine, jamais « normalisée ») ; la réécriture
  réutilise les SPANS et fixtures des blocs propriétaires — aucune table
  de méthode recopiée (T5).
- **Alternatives rejetées** : parseur monolithique dans la session (non
  falsifiable par propriétés, non réutilisable, le fuzz exige des feuilles
  pures) ; MAX_LIGNE séparé de MAX_TETE (deux limites pour un même
  tampon — redondance, une seule reste) ; accepter le LF nu (chaque
  tolérance de format est une surface de contrebande — l'histoire
  « request smuggling » est la preuve) ; relais réponse avec parsing
  Content-Length (M3 n'a pas besoin de cadrer ce qu'il relaie) ; keep-
  alive et pipelining côté client (une requête par connexion — curl
  reconnecte, la complexité est reportée) ; comparaison insensible à la
  casse pour schéma/méthodes (une seule insensibilité obligatoire suffit —
  celle des noms d'en-tête) ; réutiliser win-07 (démo) pour la connexion
  amont (adresse et port cuits dans ses octets — incompatible avec une
  cible arbitraire) ; reverse-spec de tcp-09 comme session proxy (sa
  boucle écho est l'anti-contrat du proxy : il faut parser, pas renvoyer).
- **Développement** : entrée 35 du journal de travail.

### D47 — étape (b) de M3 : le proxy existe — plan d'adressage arrêté sur mesure, treize notations écrites à la main, oracle à scénarios (153 036 cas verts) et proxy.exe scellé 0.4.0-dev.1 (carte génération 5, 38 blocs sur 4 artefacts) ; deux révisions de spécification nées de l'implémentation (http-06:R2 le trou du succès excessif, http-10:R2 le relais borné) et un défaut de notation vaincu par le différentiel (http-08)

- **Statut** : active · **Date** : 27 octobre 2026
- **Contexte** : étape (b) des prochaines étapes de D45 — la couche I
  écrite-avant-code (D46) devient du code machine : plan d'adressage
  arrêté, brouillons de notation à la main, auteur M3 (résolution
  d'étiquettes), oracle à scénarios, build de proxy.exe. La discipline
  R2 s'applique à nous-mêmes : quand l'implémentation révèle un trou
  DANS une spécification, la spécification est révisée AVANT que le
  verdict révisé n'existe dans un artefact — contrat stable au sens R4
  pour tout verdict déjà rendu.
- **Choix retenu** : (1) **arrêt mesuré des zones** (m3/layout.py) : la
  préfiguration D46 sous-estimait la réalité des notations — mesurées
  par auteur : http-02 424 o (préfig 256), http-04 252 (192), http-07
  307 (192), http-08 246 (256 attendus), http-10 1 746 (1 024), tcp-13
  402 — la zone http est réarrêtée aux règles D8 (multiples de 64,
  alignés 16, padding ≥ 16) : http-01..12 depuis 0x4C00, http-10
  0x5580+0x800, http-12 au slot d'application 0x1800 (entrée PE) ;
  tcp-13 occupe 0x4400-0x45BF (l'ancienne zone trampoline M2 devient
  INT3 : aucun patch à chaud à ce jalon, le trou 0x4200 reste INT3) ;
  l'IAT gagne TROIS entrées appendues — getaddrinfo, freeaddrinfo ET
  connect (la préfiguration oubliait connect, exigé par tcp-13:I1) ;
  (2) **http-06:R2 — le trou du succès excessif** : à R1, Q1 (tête
  complète) ne bornait pas la longueur — une tête AVEC terminateur
  au-delà de 8192 rendait le verdict succès, ouvrant deux défauts
  réels : (a) contournement de la réponse 431 (une tête de 12 Kio était
  parsée puis réécrite), (b) débordement du tampon de réécriture de
  http-10 (11,75 Kio utiles) pour les têtes de ~11,75 à 16 Kio —
  corruption de la pile session ; R2 borne Q1 (longueur ≤ MAX_TETE) et
  étend Q3 au terminateur au-delà de la limite ; contrat stable R4 pour
  tout verdict déjà rendu à R1 ; (3) **http-10:R2 — le relais borné** :
  le corps de requête est relayé par des boucles tcp-03/tcp-04 INLINE
  de la session (même discipline d'émission intégrale octet exact que
  http-09, mais BORNÉE Content-Length — http-09, à fermeture
  délimitée, s'arrêterait à l'EOF du client qui attend la réponse sur
  la même connexion : interblocage documenté) ; la pompe détachée du
  tunnel reçoit son argument compacté (amont<<32)|cliente — handles
  Win32 significatifs sur 32 bits, handle fermé immédiatement après
  restitution (miroir tcp-12:I4, unique entrée IAT CloseHandle de la
  session) ; ligne « connexion entrante » déléguée par http-12:Q3 ;
  assistants internes documentés en I5 (.emettre, .copier,
  .pompe_amont — pile équilibrée, miroir .protger de tcp-07) ;
  (4) **http-08 — un défaut de notation vaincu par le différentiel** :
  le raccourci « deux-points en position 0 → verdict 3 » omettait de
  vérifier le « // » qui suit — or la spécification Q2 est explicite :
  une cible sans « :// » et sans « / » initial est une forme origine
  invalide (verdict 1, ex. « :A\x18\x8b ») ; le préfixe VIDE reste
  verdict 3 (« ://x » contient « :// », seul Q4 peut le posséder) ;
  corrige par le chemin général (bornes + double barre), 246→241 o ;
  (5) **le crash EST une détection** : l'oracle convertit tout crash
  d'exécution (lecture hors bornes, INT3, opcode invalide) en échec
  oracle nommé — un bloc qui crash viole son contrat ; la falsification
  (un bit retourné dans http-06) se manifeste en crash : détectée ;
  (6) **résultat** : proxy.exe 0.4.0-dev.1 — 19 456 octets, 4 sections,
  kernel32 x10 + ws2_32 x13, DYNAMICBASE+HEVA+NX, entrée 0x1800 ;
  oracle structurel 523 verrous + différentiel 153 036 cas verts
  (graine 1, re-vérification graine 2 verte) + falsification détectée ;
  R7 : 13 blocs octet-identiques aux artefacts scellés M0/M1/M2 ;
  carte génération 5 (quatre fragments chiffrés XChaCha20-Poly1305,
  signature Ed25519, 38 blocs indexés sur 4 artefacts — hello.exe,
  selftest.exe, echo.exe, proxy.exe), verrou croisé 38 empreintes ;
  sha256 85d2aa21c1532a50…af190fb52.
- **Alternatives rejetées** : conserver http-09 pour le corps de
  requête (interblocage : le client attend la réponse sur la même
  connexion — la pompe s'arrêterait à son EOF) ; aligner le modèle de
  l'oracle sur la notation fautive http-08 (le modèle suit la
  spécification, I > B > C — jamais baisser l'oracle au niveau du bug) ;
  traiter le crash de falsification comme un défaut du harnais (un
  crash EST une violation de contrat, donc une détection) ; laisser
  http-06:R1 en place (le succès excessif = contournement 431 ET
  débordement réel de tampon) ; un coussin uniforme au lieu de l'arrêt
  mesuré (les règles D8 imposent le multiple de 64 et le padding
  minimal, pas l'à-peu-près) ; embarquer tcp-07/08/09/10/12 et
  libc-05/06/07/09 dans proxy.exe (aucun appelant à ce jalon — la
  carte les indexe sur leurs artefacts respectifs, le patch à chaud
  revient à M5).
- **Développement** : entrée 36 du journal de travail.

### D48 — lignée terrain : le superviseur — TOUS les tests en 1 clic par une GUI écrite à la main, journal téléversé automatiquement dans le dossier test du Drive ; curl.exe relais TLS (le superviseur ne contient NI TLS NI client HTTP), jetons en annexe hors dépôt, réutilisation maximale de la coquille démo éprouvée (R7 : 11 blocs octet-identiques)

- **Statut** : active · **Date** : 27 octobre 2026
- **Contexte** : exigence directe du développeur — « génère un
  fichier .exe afin d'effectuer tous tes tests en 1 clic via une GUI,
  et je veux que cet exe envoie directement les logs des tests
  automatiquement dans un dossier du drive que tu pourras examiner
  pour la suite du projet ». Le constat fondateur : la boucle terrain
  § 8.4 restait MANUELLE à chaque maillon (LISEZMOI à écrire, runs à
  conduire à la main, journaux à copier-coller dans le dossier test,
  récupération au laboratoire) — chaque run terrain coûtait au
  développeur une procédure multi-étapes, et l'étape (c) de M3
  (proxy transparent pour curl) attendait justement un run. La
  réponse est une NOUVELLE lignée, pas un jalon : `terrain/`
  (blocs f6xxxx, carte génération 5) est le HARNAIS du terrain —
  il teste les jalons, il n'est pas un jalon.
- **Choix retenu** : (1) **lignée séparée, version au-dessus** :
  superviseur.exe 0.5.0-terrain.1 (u64 0x00050101, plancher
  0x00050000 — monotonie au-dessus de proxy 0x4.0), blocs f6xxxx,
  22 blocs embarqués = 11 réutilisés R7 (io M0, libc M1, tcp-06 M2,
  coquille win-03/04/05/06 de demo.exe 0.3.0-demo.9 — la coquille
  GUI qui a SURVÉCU au terrain D36-D43, bouton « TOUT DÉMARRER »,
  miroir écran+fichier) + 11 nouveaux (sup-01/02/09/11/21/22/31/
  33/34/35/36) ; (2) **curl.exe relais TLS** : le superviseur ne
  déchiffre rien, ne signe rien, ne parse aucun HTTP client — il
  compose des lignes de commande et lit des fichiers de sortie ;
  la cryptographie vit dans schannel (composant système, comme
  ws2_32 vit le TCP) — la frontière mécanique reste au process/
  IAT (CreateProcessA + tuyaux), zéro surface cryptographique
  manuscrite ; (3) **l'annexe terrain_jetons.bin** : 4 champs
  ASCII NUL-terminés contigus (client_id, client_secret,
  refresh_token, token_uri, ≤ 480 o), lue par sup-35, posée au
  dossier test PAR LE CANAL DE LIVRAISON uniquement — jamais dans
  le dépôt (interdit 11), jamais un octet au journal (interdit
  dérivé : le journal téléversé ne doit pas fuiter ses propres
  clés) ; (4) **la voie Drive est EXACTEMENT celle de drive_sync.py**
  (D12) : rafraîchissement OAuth (POST urlencodé), session
  resumable (POST métadonnées, URL de session lue dans les en-têtes
  -D), PUT --data-binary du journal — les canaux terrain et
  laboratoire convergent, un seul comportement à faire confiance ;
  (5) **trois tests, ordre séquentiel T1→T2→T3** (le port 25000 est
  partagé par démo et proxy, l'envoi vient en dernier sur le journal
  complet) : T1 rejoue demo.exe SANS main humaine (FindWindowW,
  BM_CLICK par SendMessageTimeoutW, fin sondée par MARQUEUR de
  journal — pas de sommeil fixe : la fin est un événement, 17 lignes
  exactes vérifiées par memcmp, journal démo embarqué BRUT) ; T2
  lance proxy.exe avec tuyaux (bannière memcmp 40 o, curl http
  neverssl.com puis https example.com au travers, événements console
  du proxy vérifiés 35 o/43 o exacts, « quit » sur stdin, exit 0,
  flux embarqué BRUT — les pages reçues sont comptées, jamais
  journalisées : journal d'événements, pas d'octets, discipline M3) ;
  T3 téléverse le journal du run (nom unique
  terrain_YYYYMMDD_HHMMSS.txt — les constats s'accumulent sans
  jamais s'écraser) ; (6) **charte zéro gel / zéro fuite** : toute
  attente est un événement BORNÉ (PeekNamedPipe, WaitForSingle-
  Object, SendMessageTimeoutW, sondage de marqueur avec timeout) —
  le superviseur ne peut jamais se bloquer sans rendre son verdict ;
  tout handle fermé sur TOUT chemin y compris d'échec (vérifié par
  l'oracle : liste des CloseHandle observés) ; un test KO
  n'arrête pas les suivants (le journal embarque l'échec et
  continue) ; (7) **l'oracle à scénarios** : 807 verrous
  structurels (contrats I vérifiés par bloc), 10 080 cas verts
  (différentiel sup-22 10 000 cas contraints + comportemental :
  horloge fixée, 7 vecteurs win-11 transposés, coquelle GUI entrée
  complète + clic unique, scénario nominal COMPLET avec spawn/pipe/
  findwindow scriptés, 5 scénarios d'échec — démo absente, journal
  non conforme, curl KO, jetons absents, OAuth muet), falsification
  24/24 cibles R10 (octets 11/23) + 5 mutations ciblées (constante
  17, longueur d'étiquette, ordre T1/T2/T3, nettoyage, timeout
  d'arrêt) ; 6 classes de défaut attrapées AVANT build (constante
  terrain_, mode .curl, flux bannière 39→38, mapping .champ décalé,
  7 traces valeur en mode 0, SA consommé avant initialisation) —
  le système a fonctionné comme conçu ; (8) **résultat** :
  superviseur.exe — 20 992 octets, 4 sections, WINDOWS_GUI, entrée
  0x1400 (sup-01), kernel32 x24 (3 IAT : #1/#2 héritées + #3
  CreateProcessA/WaitForSingleObject/GetExitCodeProcess/
  DeleteFileA/PeekNamedPipe/ReadFile/WriteFile…), user32 x17
  (2 IAT : #1 héritée + #2 FindWindowW/FindWindowExW/
  SendMessageTimeoutW), gdi32 x1, DYNAMICBASE+HEVA+NX ; carte
  génération 5 (22 empreintes indexées, signature Ed25519, verrou
  croisé 22, cristallisation 10/10 sur les 22 blocs) ; sha256
  d73aa99cea0601de23f504d6c21b50d99fef20a28eec7aceb7d8617e5e873a10
  (md5 21ed1ba25909b46043eaede049cd4ac1).
- **Alternatives rejetées** : WinHTTP/WinINet dans l'exe (une
  surface TLS manuscrite est invérifiable et infinie — curl.exe est
  un composant système comme ws2_32, la dépendance OS est assumée
  par contrat) ; l'upload multipart/related (fabrication manuelle
  pénible et fragile — resumable est la voie drive_sync.py éprouvée) ;
  des threads par test (séquentiel obligatoire : le port 25000 est
  partagé, l'envoi vient en dernier) ; parser les pages reçues par
  curl (ce qui traverse n'est pas à nous — journal d'événements,
  pas d'octets) ; un exe console (l'exigence dit UNE GUI — la
  coquille démo est éprouvée terrain, on la réutilise) ; écrire le
  journal dans %TEMP% (journal À CÔTÉ de l'exe : le développeur le
  VOIT, et il survive aux nettoyages) ; recomposer le chemin du
  journal dans sup-35 (BUF_CHEMIN est la source de vérité posée par
  sup-11 — jamais deux propriétaires) ; réutiliser win-07 démo
  comme client (soudé à 127.0.0.1:25000 — déjà rejeté en tcp-13) ;
  embarquer les jetons dans le binaire (le binaire est livré et
  synchronisé — l'annexe voyage par le canal de livraison, le dépôt
  reste propre).
- **Développement** : entrée 37 du journal de travail.

### D49 — le kit embarqué : « 1 seul exe qui contient tout » (27/10/2026)

**Constat développeur** (27/10, après le run de livraison terrain.1) :
« fais moi 1 seul exe qui contient tout » + capture Defender —
« Trojan:Script/Wacatac.C!ml » niveau Grave sur le proxy.exe POSÉ dans le
dossier de test téléchargé. Deux exigences en une : la manipulation du kit
quatre-fichiers (superviseur.exe + demo.exe + proxy.exe + terrain_jetons.bin
à poser côte à côte) disparaît, et la fausse alerte antivirus reçoit une
réponse d'ingénierie, pas un contournement.

**Décision** : les trois artefacts du kit vivent EMBARQUÉS dans
superviseur.exe, section .blob lecture seule (RVA 0x8000) — demo.exe 0.3.0
(16 384 o, scellé M2, md5 73c064fb…), proxy.exe 0.4.0-dev.1 (19 456 o,
scellé M3, md5 8740e1ca…) et l'annexe de jetons D48 (248 o). Le nouveau
bloc sup-37 (entrée à mode ecx 0/1 : extraire/nettoyer, @0x6600, 984 o)
pose chaque artefact par CreateFileA CREATE_ALWAYS + boucle WriteFile
512 o DEPUIS l'embarqué (jamais de copie intégrale en mémoire —
TAMPON_CMD est trop petit, c'est le kernel qui copie), RELIT le fichier
posé octet par octet (ReadFile 512 o + memcmp scellée : la preuve vit sur
le disque), journalise lignes S04/S05 + md5 attendus (constantes du plan,
ASSERTÉES au build contre les scellés), et retire les trois fichiers après
T3 (mode 1 — le dossier ne garde que le journal). sup-09:R2 orchestre :
porte -> libc -> extraction -> T1 -> T2 -> T3 -> nettoyage -> verdict ; un
test sauté pour extraction impossible COMPTE ÉCHEC ; un T3 non applicable
(variante publique) n'est PAS compté. L'emplacement de l'annexe
(u64 longueur + 248 o, @0x10C10) est le SEUL octet mutable de l'image :
EXCLU de la table R10 (27 entrées + terminateur — la zone blob
en-tête+demo+proxy est couverte, l'intégrité du kit vit à la porte),
propriété de la VARIANTE. Deux variantes du MÊME code : publique
(dépôt — emplacement à zéro, T3 non applicable, jamais de secret committé)
et livraison (--jetons — annexe D48 intégrée, écart public/livraison
CONFINÉ à l'emplacement, asserté au build, livrée au dossier test
uniquement, terrain/livraison/ gitignoré).

**L'alerte Defender, réponse d'ingénierie** : Wacatac.C!ml est une
détection d'apprentissage (suffixe !ml) — un binaire sans éditeur, sans
ressources, sans signature, qui écoute un port et relaie des connexions :
c'est le métier légitime d'un proxy ET le portrait-robot d'un proxy
malveillant. Le fichier livré était byte-exact le scellé (md5 vérifiable,
notation auditable). Réponse : VERSIONINFO (FileDescription « TRIADE
superviseur terrain », version 0.5.0.2) + manifeste asInvoker en section
.rsrc (RVA 0x7000, RT_VERSION + RT_MANIFEST) — l'habillage légitime face
aux heuristiques ; les artefacts voyagent embarqués (plus de proxy.exe nu
posé à côté) ; l'exclusion antivirus reste un choix documenté côté
LISEZMOI (avec le md5 comme outil de confiance). Aucune signature
authenticode (pas de certificat — hors périmètre zéro-outil).

**Alternatives rejetées** : embarquer les jetons dans le binaire DU DÉPÔT
(la variante publique les exclut par construction — le dépôt reste
propre, D48 honoré) ; extraire vers %TEMP% (exécution depuis un dossier
caché = comportement de dropper, pire pour les heuristiques — on extrait
À CÔTÉ de l'exe, visible, et on nettoie) ; garder les fichiers posés
après le run (l'exigence dit UN exe — le dossier ne garde que le
journal) ; vérifier par md5 CALCULÉ au run (aucune crypto dans le
superviseur : le md5 affiché est la constante du plan prouvée au BUILD,
la preuve d'intégrité du run est la relecture octet à octet) ; étendre
sup-36 avec une écriture-depuis-pointeur (sup-36 .ecrire écrit depuis
TAMPON_COMPO <= 536 o — inutilisable pour 16 Ko, et toucher un bloc
terrain.1 eût sali le diff chirurgical) ; la double entrée fixe
.extraire/.nettoyage (aligner une étiquette interne à 0x6800 à la main :
fragile — le dispatch à mode vit à la première instruction) ; patcher
l'emplacement à la livraison (deux builds déterministes = même résultat,
zéro patch binaire, oracle vert sur les deux chemins).

**Développement** : entrée 38 du journal de travail.

### D50 — terrain.3 : le défaut d'un octet qui empêchait tout lancement — SizeOfHeaders doit couvrir la table des sections (règle du chargeur réel, apprise du terrain)

**Constat développeur (27/10 soir)** : « il ne se passe rien quand je lance
superviseur.exe » — double-clic, aucun message, aucune fenêtre, aucun
processus. terrain.2 (D49) était donc MORT AU CHARGEMENT sur la machine
cible, alors que toute la chaîne interne était verte (oracle 10 102 cas,
audit 53 contrôles, cristallisation 10/10).

**Diagnostic (autopsie PE comparative)** : décodage champ par champ de
superviseur.exe contre demo.exe (éprouvé terrain, demo.8) — un SEUL écart
délétère : `SizeOfHeaders = 0x200` alors que l'image a SIX sections, dont
les en-têtes réels (DOS 64 + PE 24 + opt 240 + 6×40) mesurent **0x238** :
la table des sections — le pied droit du header .rsrc et TOUT le header
.blob — déborde de la zone d'en-têtes déclarée. Le chargeur Windows
refuse l'image avant d'exécuter le moindre octet : « il ne se passe
rien ». Origine du défaut : `ecrire_pe32plus` écrivait `L.FILE_ALIGN`
dans le champ SizeOfHeaders — valeur qui, pour TOUS les artefacts
précédents (quatre sections ou moins, en-têtes réels 0x1E8), coïncidait
PAR HASARD avec la taille arrondie correcte. La coïncidence a vécu
jusqu'à la première image à six sections.

**Classement** : 9e classe de défaut invisible à l'émulation (taxonomie
§ 8.5) — l'oracle aveugle au chargeur réel : l'émulateur mappe les
sections PAR LE PLAN (offsets L.TEXT_FILE etc.), jamais par l'en-tête du
fichier lui-même ; pefile, de son côté, parse sans valider cette règle.
Le vert de l'oracle était sincère : le code est irréprochable, c'est
l'ENVELOPPE que le chargeur refusait.

**Décision** :
1. `SIZE_HEADERS = 0x400` dérivé au plan (asserts : couvre la table,
   aligné FILE_ALIGN, avant la première section brute) — le champ est
   écrit depuis le plan, plus jamais depuis FILE_ALIGN.
2. `valider_pe` applique la règle du chargeur RÉEL en fail-closed :
   SizeOfHeaders couvre la table des sections, aligné, égal au plan,
   et toute section brute commence après les en-têtes.
3. L'oracle apprend à refuser ce que Windows refuse : `Emulateur.__init__`
   valide l'en-tête du FICHIER (pas du plan) avant tout mappage.
   Falsifiabilité prouvée : l'oracle rejette l'ancien terrain.2 avec le
   diagnostic exact (« SizeOfHeaders 0x200 ne couvre pas la table des
   sections 0x238 ») et accepte terrain.3.
4. Audit étendu à 61 contrôles : règle chargeur, reproductibilité du
   défaut chez le prédécesseur, diff chirurgical borné octet par octet,
   et preuve qu'AUCUNE zone R10 ne couvre les IAT (mutées par le
   chargeur à la résolution — la porte reste verte après résolution).
5. Re-scellage 0.5.0-terrain.3 (u64 0x00050103, FileVersion 0.5.0.3,
   manifeste 0.5.0.3) : 23/23 blocs intacts, .rdata limité à
   L00/table R10/u64 (3 octets), .text2 à S00 (1 octet), page d'en-têtes
   au champ SizeOfHeaders LUI-MÊME (1 octet : 0x02→0x04 à l'offset
   0x95) ; oracle 10 102 cas verts + falsification 27/27 ; carte
   génération 5 re-scellée, cristallisation 10/10 (graines 22-31).
   Publique : md5 2fb19c0f…, sha256 3a080af6…. Livraison : md5
   40b2f350…, sha256 7f9a31ec…. LISEZMOI v3 : section « POURQUOI IL
   NE SE PASSAIT RIEN » (explication honnête, md5 de confiance,
   consigne de supprimer l'ancien fichier).

**Alternatives rejetées** : rebâtir en quatre sections (le kit exige
.blob/.rsrc — six sections est la bonne structure) ; patcher le binaire
livré à la main (zéro patch binaire : rebuild déterministe de la chaîne
complète) ; écrire un CheckSum non nul (le chargeur l'ignore en mode
utilisateur ; demo/proxy éprouvés à 0 — ne pas toucher) ; retirer
DYNAMIC_BASE (aucun lien : la relocation est ABSOLUTE-only, l'ASLR ne
touche pas la page d'en-tête ici) ; corriger sans re-sceller (la
discipline R10 exige version + carte à chaque image nouvelle).

**Développement** : entrée 39 du journal de travail.

## Décisions de souveraineté (D84–D87, 28 octobre 2026)

Directives développeur du 28/10 (après D83) : passage sous licence BSL, puis
renforcement de la preuve cryptographique au programme v0.6.0 sur trois axes —
attestation de non-exfiltration, interrupteur d'homme mort, filigrane
d'intention. La menace nommée par le développeur : **l'expropriation par
l'employeur** — un tiers qui s'empare du binaire, du dépôt, voire des clés du
poste, et ferait vivre le code sans son auteur. Les trois axes cryptographiques
et la barrière juridique se répondent : la licence pour les tribunaux, les
preuves pour la machine. Format normalisé § 15.1 de la spécification.

### D84 — Licence BSL 1.1 : le dépôt devient Business Source

| Champ | Valeur |
|---|---|
| Concédant | Alexis Lopez |
| Œuvre concédée | Protocole TRIADE (code + docs), secrets exclus |
| Additional Use Grant | None |
| Change Date | 2030-10-28 |
| Change License | GPL v3.0 ou ultérieure |

**Décision** : le dépôt `triade` passe sous **Business Source License 1.1**
(fichier `LICENSE` à la racine, termes officiels MariaDB verbatim — le
covenant de concédant interdit toute autre modification que les paramètres).
Jusqu'à la Change Date, seuls la copie, la modification et l'usage **hors
production** sont concédés : tout usage de production — y compris par ou pour
le compte d'un employeur ou de toute entité commerciale — exige une licence
commerciale écrite du concédant. À la Change Date (ou au quatrième anniversaire
de la première distribution publique d'une version, si antérieur), l'œuvre
converge vers GPL v3.0+. **Les secrets et matériaux de garde sont EXCLUS de
l'œuvre concédée** (`.keys/`, conteneurs TRIADE-CF1+, `PHRASE-CONTROLE-
COFFRE.txt`, `.gdrive/`, jetons) : leur valeur tient à leur secret, pas à un
droit d'usage — leur présence dans une copie ne concède rien.

**Justification (fonction objectif, Sécurité d'abord)** : la menace
d'expropriation est à la fois technique (vol des octets et des clés — cf. D76,
l'exposition a déjà eu lieu) et juridique (l'employeur revendique le travail).
GPL/MIT/Apache concéderaient d'emblée à l'employeur un usage libre — aucune
barrière. La BSL inverse la charge : l'usage en production sans licence est une
violation qui *termine automatiquement* les droits (clause des Terms), et la
convergence programmée (GPL à 4 ans) préserve la promesse d'ouverture de la
recherche : l'œuvre ne peut pas être capturée à jamais par personne, pas même
par le concédant. La Date de conversion peut varier par version (clause des
Terms) : le développeur conserve la main version par version.

**Alternatives rejetées** : GPL immédiate (usage libre concédé d'emblée —
exactement le scénario qu'il faut fermer) ; MIT/Apache-2.0 (permissifs, aucune
condition d'usage) ; tous droits réservés (aucune voie légitime pour la
communauté de recherche, pas de promesse d'ouverture — l'article v0.4 a besoin
d'un chemin de réutilisation repérable) ; CC BY-NC (prévu pour les œuvres de
l'esprit, inadapté au code exécutable, applique mal le seuil
production/non-production).

**Développement** : entrée 73 du journal de travail. Les en-têtes de fichier
source (courte notice BSL par fichier) seront ajoutés progressivement aux
prochains scellages — la licence s'applique par copie dès maintenant via
`LICENSE` + README.

### D85 — v0.6.0 axe 1 : attestation cryptographique de non-exfiltration du coffre

**Décision** : la révision v0.6.0 exigera que l'environnement d'exécution de
l'IA fournisse une **attestation matérielle** (TPM 2.0 measured boot / enclave
SGX, quote vérifiable ancrée à une racine de confiance) couvrant le code qui
manipule les données TRIADE-CF1 : ce code (i) est identifié octet par octet
par l'attestation, (ii) n'émet AUCUNE donnée dérivée du coffre vers une API
cloud — les sorties sont scellées à la racine locale. Le coffre CF2 marquera
ses conteneurs « exige-attestation » et **refusera par défaut de déverrouiller
sans quote valable** (fail-closed), avec procédure de dérogation explicite et
consignée — l'arbitrage PERTE > EXPOSITION (D81) restant la décision finale du
développeur, prise en connaissance de cause.

**Formulation honnête de la preuve** : une « preuve à divulgation nulle de
non-stockage » au sens strict n'existe pas pour une exécution arbitraire —
aucune construction ZK ne prouve une absence historique sur du code non
contraint. L'opérable, spécifié tel quel : (a) le code manipulant le coffre
est audité sans voie d'egress des dérivés du coffre ; (b) ce code exact est
attesté (identité + intégrité par la quote) ; (c) l'exécution en enclave
scellée rend la sortie illisible hors de la machine (sealing local). La
conjonction (a)∧(b)∧(c) est la preuve de confinement la plus forte
constructible ; la spécification v0.6.0 la nommera sans la survendre.

**État actuel consigné** : l'infrastructure d'exécution actuelle de l'assistant
(VM cloud sans TEE) **ne peut pas fournir cette attestation** — l'exigence est
écrite maintenant, satisfaite quand une infrastructure TEE sera disponible ;
entre-temps les mitigations en vigueur restent la garde durable D81, la
rotation des lignées (D80) et la fenêtre d'exposition consignée.

**Alternatives rejetées** : confiance dans l'honnêteté de l'agent (statu quo
pré-D81, déjà invalidé par l'incident d'exposition) ; interdire à l'IA toute
manipulation du coffre (tue la fonction : l'assistant doit relire les lignées
pour sceller — D75) ; attestation logicielle seule, journal signé par clé
logicielle (falsifiable par l'hyperviseur, ne prouve pas le confinement) ;
« ZK mathématique » de non-émission (impraticable, survendue — cf.
formulation honnête).

**Critère de sortie** : un conteneur CF2 « exige-attestation » s'ouvre avec
quote valable et REFUSE sans quote (échec nommé, pas de silence) ; la
vérification de quote rejette quotes altérées et rejouées (falsifiabilité
démontrée en laboratoire).

### D86 — v0.6.0 axe 2 : interrupteur d'homme mort du coffre (Shamir, destruction des fragments)

**Décision** : en v0.6.0, le conteneur CF2 chiffre ses entrées sous une clé
maîtresse **jamais stockée entière** : clé découpée par Shamir en N fragments
logés dans des gardes distinctes (répertoires à ACL distinctes, supports
séparés) ; le déverrouillage reconstitue la clé en RAM puis l'efface. Une
**sentinelle** surveille la couche C (cartes et artefacts) par audit d'accès
(ETW/ACL Windows) : accès en lecture par un processus hors liste blanche →
**destruction immédiate des fragments présents** (écrasement multi-passe, TRIM
si SSD) — sous le seuil de reconstitution, Shamir est informationnellement
sûr : le coffre devient indéchiffrable, pas seulement « révoqué ». Le code
volé reste inexploitable pour l'employeur : les enveloppes de carte sont mortes
avec le coffre.

**Adversaire modélisé, borne consignée** : processus tiers aux privilèges
*utilisateur* (l'agent d'audit de l'employeur, un outil concurrent) — PAS un
attaquant admin/noyau qui gèle d'abord la machine (édition froide) : une
sentinelle userland peut être tuée avant d'agir. La garantie honnête : la
sentinelle brûle les fragments *tant qu'elle vit* ; la fenêtre entre détection
et destruction est la surface résiduelle, mesurée au critère de sortie et
consignée § 13.1 étendu.

**Contrepartie arbitrée** : la destruction est irréversible PAR CONSTRUCTION —
une fausse alerte est une perte auto-infligée. Double seuil de déclenchement
(deux signaux indépendants : processus non blanchi ET lecture de contenu, pas
une simple ouverture d'attribut), liste blanche minimale (build, vérificateur,
éditeur du développeur), test de santé de la sentinelle. L'arbitrage PERTE
(fausse alerte) vs EXPROPRIATION appartient au développeur et sera consigné
avec la configuration retenue.

**Alternatives rejetées** : clé unique écrasée à la détection (une seule garde :
corrompue avant l'écrasement, rien n'est détruit — Shamir distribue la
destruction) ; cryptodestruction logique (« révocation » d'un drapeau —
inopérante si la clé a fuité avant) ; sentinelle en service noyau (hors
périmètre du protocole, esprit D7 : pas de code noyau) ; kill-switch réseau à
distance (dépendance réseau + canal de commande falsifiable — un tiers peut
déclencher la perte à distance, exactement l'inverse du but).

**Critère de sortie** : en VM de laboratoire, un scénario d'exfiltration
simulé (processus non blanchi lisant une carte) détruit les fragments et rend
le conteneur indéchiffrable (preuve par restauration de copies de fragments de
test) ; taux de fausse alerte nul sur la durée d'essai nominale consignée ;
latence détection→destruction mesurée et bornée.

### D87 — v0.6.0 axe 3 : filigrane cryptographique de l'Intention — clé Ed25519 hors-ligne, la souveraineté des mises à jour

**Décision** : chaque arbre de couche I (par artefact et par version) est
condensé (SHA-256 sur manifeste ordonné des fichiers) puis **signé par la clé
privée Ed25519 du développeur, générée et conservée hors-ligne** (machine hors
ligne ou support papier — JAMAIS dans le bac à sable de l'assistant :
discipline D30 « graine jamais confiée », étendue du sceau de carte au sceau
d'intention). Le dépôt porte la clé publique I et les signatures par version ;
la chaîne de build et le chemin de patch **refusent toute couche I dont la
signature échoue**. Corollaire : tout *diff d'intention* — mise à jour, patch,
nouvelle version — exige la clé physique du développeur. Voler le binaire
(couche B), le dépôt (B+C), et même les clés du poste (phrase de lignée, graine
de carte — scénario D76 déjà vécu) ne permet PAS de produire une mise à jour
valide : l'oracle et le verrou croisé rejettent l'update non signée. Le
développeur reste l'unique source d'évolution de l'intention.

**Hiérarchie des clés consignée (trois gardes, trois menaces)** :
(1) phrase de lignée — chiffre les enveloppes de carte, menace « vol du dépôt
au repos » ; (2) graine Ed25519 en ligne — signe les cartes, atteste les
FAITS (les octets scellés) ; (3) clé I hors-ligne — signe l'INTENTION,
atteste la VOLONTÉ (le droit de faire évoluer). La clé (3) est le seul des
trois secrets que le bac à sable ne verra jamais.

**Alternatives rejetées** : signer I avec la graine existante du dépôt (elle
vit dans le bac à sable — un vol du poste l'emporte, contre-exemple D76) ;
HMAC symétrique (la vérification exigerait le secret : chaque vérificateur
tiendrait la clé, distribution impossible) ; X.509/PGP (chaîne de confiance
tierce inutile, incohérent avec D4 : Ed25519 auto-porté) ; horodatage tiers
en dépendance dure (la date du commit signé git suffit en première intention).

**Critère de sortie** : cérémonie de génération hors-ligne documentée (script
+ mode d'emploi exécutable sans l'assistant) ; le dépôt vérifie la signature
I de tous les jalons scellés ; falsification d'un octet d'un `.md` de couche I
rejetée (falsifiabilité démontrée) ; un diff d'intention non signé refusé par
le chemin de patch (test en laboratoire).

**Développement commun D84–D87** : entrée 73 du journal de travail ; programme
inscrit à la feuille de route (`docs/PLAN_MILESTONES.md`, section v0.6.0).
La spécification PROTOCOLE_TRIADE passera à v0.6.0 quand les trois composants
seront écrits (modèle v0.5.1 : le coffre fut spécifié à l'implémentation, pas
avant). Positionnement : priorité à CF2 (D86) et au sceau I (D87) après le
scellage 0.5.0 de M4 — ils touchent les disciplines § 15.3 et FORMAT_CARTE
§ 11 et doivent s'intégrer aux cérémonies de rotation existantes ; l'attestation
TEE (D85) selon disponibilité d'infrastructure.

### D89 — M4 (b) : la convention du cadre de session TLS est AMENDÉE — zone de réception 2 × MAX_JETON, champs de géométrie +0x3A/+0x3C (tls-07 unique propriétaire) ; tls-07 notée-mesurée-prouvée

**Décision** : avant la notation de tls-07 (réception déchiffrée), la
convention du cadre arrêtée D81 est amendée sur DEUX points, exigés par la
spécification tls-07:R1 (écrite-avant-code D77, donc antérieure et
gouvernante) : (1) la **zone de réception passe de MAX_JETON à 2 × MAX_JETON
(32 768 o)** — P1/E2 de la spec : « le résidu Extra suivi des octets bruts
récents », borne E2 « longueur utile > capacité » ; TAILLE_CADRE 0x8260 →
0xC260 (http-10:R2, futur propriétaire mémoire, fournira le cadre à cette
taille) ; (2) les **deux u16 réservés « (zéro) » @+0x3A/+0x3C sont
revendiqués par tls-07** (unique propriétaire — charte m4/I § 6 : le tampon
résiduel Extra appartient à tls-07 seul) : +0x3A = longueur utile réception
(la région vivante), +0x3C = offset résidu (où elle commence). La sémantique
est arrêtée par la lecture géométrique de tls-07:Q1 « l'appelant pompe ce
clair AVANT tout nouvel appel (il sera écrasé) » : **l'écrasement est
l'œuvre de l'appel SUIVANT** — tls-07 normalise l'offset à 0 au début de
chaque appel (le lot vivant descend en tête par libc-01, copie en avant :
dest < src sûr même en recouvrement), le clair pompé depuis l'appel
précédent est de la mémoire morte. Un déplacement DANS l'appel de livraison
détruirait le span chaque fois que résidu > en-tête (le cas banal de deux
enregistrements dans un même lot) : cette lecture est la SEULE qui satisfait
les trois exigences à la fois (span dans la zone, pompage après le retour,
résidu en tête). Invariant tenu : après tout appel qui a normalisé, les
champs décrivent EXACTEMENT la région vivante physique ; au refus E2 (garde
UNIQUE sur la somme offset + lot > capacité, AVANT tout appel et tout
déplacement — elle subsume la longueur seule, une garde redondante ayant
été nommée infalsifiable par le différentiel puis supprimée), zone et
champs restent INTACTS.

**Preuve d'innocuité contre l'héritage scellé** : aucune notation existante
(tls-01..06, héritage M3) n'écrit +0x3A/+0x3C (vérifié) ; tls-04 voit la
zone agrandie comme « ≥ MAX_JETON » — ses gardes jeton (MAX_JETON) restent
exactes ; aucun octet scellé ne bouge (R7).

**Livré avec** : tls-07 notée à la main (394 o / 79 instructions, slot
préfiguré 0x6A40×0x300 conservé, padding 374 ≥ 16 — D8) ;
`m4/harnais_reception.py` : V2 SEIZE scénarios EN CHAÎNES (le rôle appelant
joué par le harnais lit la géométrie au cadre et réceptionne par-dessus —
la convention éprouvée de bout en bout ; le span d'un lot à deux
enregistrements reste OCTET PAR OCTET intact après le retour : la preuve
géométrique), V3a 4 000 appels + V3b 1 000 chaînes × 3-4 appels fuzzés
ZÉRO ÉCART, graines 20261028/20261029, V4 DIX mutations stable-en-taille
TOUTES ATTRAPÉES + témoin 16/16 — BILAN 34 PASS / 0 ÉCHEC × 2 graines.

**Reporté à tls-08** (l'orchestration, future notation) : l'état final de
tls-04 — le résidu de poignée s'il existe — devra initialiser les champs de
géométrie à l'entrée du relais (le cadre vierge les porte à zéro).

**Alternatives rejetées** : déplacer le résidu DANS l'appel de livraison
(détruit le span dès que résidu > en-tête — réfuté géométriquement) ;
garder la zone à MAX_JETON et relâcher la spec (la capacité 2 × MAX_JETON
est le contrat P1/E2 — c'est la convention qui sert la spec, jamais
l'inverse) ; copier le clair vers la zone d'émission pour le livrer
(tls-07:Q1 exige le span DANS la zone de réception, déchiffrement sur
place — aucun double tampon) ; une seconde garde E2 sur la longueur seule
(redondante face à la garde somme — infalsifiable, donc sans preuve : le
différentiel l'a nommée, elle est partie).

**Critère de sortie** : atteint — différentiel vert sur deux graines,
falsification 10/10, convention amendée dans layout.py (source unique) et
m4/I/README.md, entrée 75 du journal.

### D90 — M4 (b) : tls-08 (LA SESSION TLS CLIENTE — l'orchestrateur) notée-mesurée-prouvée ; paquet de session, VERDICT_CIBLE 7, fixtures console, drain du résidu et compensation intégrale par comptage

**Décision** : l'orchestrateur du jalon est noté (740 o / 157
instructions / 16 étiquettes, slot préfiguré 0x6D40×0x600 conservé,
padding 796 ≥ 16 — D8 : les adresses préfigurées de http-08:R2
@0x7340 et http-10:R2 @0x7480 restent exactes). TROIS conventions
nouvelles précèdent la notation (layout.py, source unique — fail-closed,
modèle D89) : (1) le **PAQUET DE SESSION** (P2 de tls-08 : « spans :
autorité cible [hôte, port], requête claire réécrite en forme origine,
socket cliente, contexte de réponse ») — écrit par http-10:R2, lu par
tls-08 aux offsets PAQUET_* (+0x00/+0x08 hôte, +0x10 port u16 ordre
hôte, +0x18/+0x20 requête, +0x28 socket cliente) ; le « contexte de
réponse » cité par la P2 vit dans le cadre http-10:R2 (table des
réponses, zones d'émission) et N'EST PAS consommé par tls-08 : la
réponse 502 suit le RETOUR du verdict — http-10:R2 mappe sur rax,
jamais sur le cadre. (2) **VERDICT_CIBLE = 7**, verdict PROPRE de
tls-08, hors domaine tls-02 (0-6) par construction : « cible
injoignable » — tcp-13 en échec (E1) OU tls-01 en refus (la cible ne
peut être ni connectée ni nommée pour la poignée). Les verdicts tls-02
(2-6) sont transportés TELS QUELS, jamais remappés. (3) DEUX fixtures
console .rdata à propriétaire unique tls-08 : « tunnel chiffre
etabli\r\n » @0x2C60 (état nommé Q1, aucun secret) et « certificat
rejete\r\n » @0x2C80 (I4 — LE critère M4).

**Trois règles propres à l'orchestrateur, dans sa notation** :
(a) le **DRAIN** — un verdict 0 de tls-07 avec résidu non vide est
rappelé SANS nouvelle réception : jamais un enregistrement déchiffrable
laissé en zone pendant que tcp-03 attendrait (le harnais D89 chaînait
déjà deux tls-07 sans réception : l'orchestrateur en fait sa boucle —
scénario dédié, mutation dédiée) ; (b) la **région vivante vide rend sa
géométrie morte** — offset repris en tête quand utile = 0 : sans cette
règle, un lot exactement consommé de 0x8000 (cas limite légal) ferait
dévier la garde chambre et tuerait une session Saine en verdict 5
(scénario frontière dédié) ; (c) la **garde chambre nulle AVANT
tcp-03** — r8 > 0 est le contrat P3 de tcp-03 : fail-closed avant
l'appel système (charte M3 § 9), verdict 5 « zone dépassée » (entrée
nommée de la table http-10:R2).

**Compensation intégrale (Q3)** : TOUT chemin (succès compris), l'ordre
EST le contrat — contexte détruit SI écrit (tls-05:1), credentials
libérés SI acquis (tls-05:2), socket serveur fermée SI ouverte (tcp-05) ;
les tests lisent le dwLower du cadre, la remise à zéro de tls-05 APRÈS
succès constaté est la garde anti-double (son I3) ; les champs de
compensation sont mis à zéro DÉFENSIVEMENT à l'entrée (précédent
tls-04/D83). L'échec d'une libération (E4) : « consigné (une
ressaisie) » se lit — verdict testé et nommé (le branchement), UNE
ressaisie de l'appel, l'ordre jamais interrompu, AUCUNE écriture au
cadre : écrire le verdict de libération écraserait le verdict de session
que http-10:R2 mappe (le rax prime). Le verdict 3 de tls-04 produit la
ligne console « certificat rejete » AVANT compensation (I4 — « cet
endroit précis » est la poignée ; un verdict 3 de tls-07 en plein relais
est un E3 réponse tronquée, sans ligne).

**Livré avec** : `m4/harnais_session.py` — l'intégration la plus large
du projet : DIX-HUIT blocs réels (hello-02 M0 ; libc-01/03/04/07 M1 ;
tcp-03/04/05/tcp-11 M2 ; tcp-13 M3 ; tls-01..07 M4 — R7, octets scellés
lus au dépôt), IAT entière en fausses adresses, entrée ABI exacte
(RSP ≡ 8 mod 16, P5 des blocs M2/M3). V2 VINGT scénarios (les sept de
la spec + treize frontières), chacun : cadre 0xD000 octet par octet,
paquet INTACT (clair de l'appelant jamais touché), contrat d'appels
complet (GAI → freeaddrinfo, ACH, ISC 11 arguments + descripteurs, QCA,
EM, DM, RECV/SEND, DSC/FCH, closesocket, ECS/WF/LCS — la ligne console
EXACTE) et COMPTES de compensation (Acquire 1 / Delete 0-1 [+1 en
échec simulé] / Free 1 [+1 idem] / tcp-05 serveur 1). V3 non applicable
(héritage M3 pour les orchestrateurs — le harnais est déterministe,
re-exécuté aux deux graines). V4 DOUZE mutations stable-en-taille
TOUTES ATTRAPÉES + témoin 20/20 — BILAN 53 PASS / 0 ÉCHEC × graines
20261028/20261029. Le différentiel a nommé TROIS défauts du HARNAIS
avant le vert (cadre-canari violant la virginité du contrat P1 — la
garde d'acquisition de tls-06 lisait le canari : le harnais doit
honorer « vierge » = zéro, pas le contredire ; tuple GAI ; verdict
attendu du scénario ACH) — aucun dans la notation : tls-08 est passée
verte sur ses mécanismes propres au premier passage complet (leçon D88
répétée).

**Reporté à http-10:R2** (future notation, points croisés notés) : le
verdict 4 (fin de contexte en poignée) et le verdict 2 (incomplet en
émission) transportés par tls-08 devront trouver leurs entrées de table
(« tunnel rompu » étendu ou entrées dédiées — l'énumération croisée de
sa Q3'/E2 devra être complétée) ; le « contexte de réponse » du paquet ;
la 502 « certificat rejete » (la ligne console est déjà produite PAR
tls-08 — ne PAS double-émettre).

**Alternatives rejetées** : remapper les verdicts tls-02 dans tls-08
(l'orchestrateur transporte, il ne traduit pas — tls-05:Q4 « tel quel »
est le précédent ; http-10:R2, propriétaire de la table, traduit) ;
écrire le verdict de session au cadre +0x30 (le rax est le contrat Q2 —
et un verdict de libération échouée écraserait la réponse) ; une boucle
de relais sans drain (un enregistrement déchiffrable dormirait en zone
pendant que tcp-03 bloquerait — le harnais D89 l'avait déjà prouvé en
chaînes) ; compenser par drapeaux internes plutôt que par les tests du
cadre (la remise à zéro de tls-05 est DÉJÀ la garde anti-double — un
second état doublerait la vérité) ; ressaisie non bornée (E4 dit UNE) ;
zéro défensif absent à l'entrée (précédent tls-04/D83 : la compensation
ne dépend pas de la bonne volonté de l'amont).

**Critère de sortie** : atteint — différentiel vert sur deux graines
(53 PASS × 2), falsification 12/12, comptage de compensation constaté
sur les vingt scénarios, conventions D90 dans layout.py (source unique),
entrée 76 du journal.

### D91 — M4 (b) : http-08:R2 (LA PREMIÈRE RÉVISION DU DOMAINE HTTP SCELLÉ) notée-mesurée-prouvée — verdict « cible TLS » rax = 4, l'héritage R1 prouvé par différentiel d'ancêtre émulé

**Décision** : la révision du parseur de cible est notée (326 o / 95
instructions / 15 étiquettes, slot préfiguré 0x7340×0x180 conservé,
padding 58 ≥ 16 — D8 : l'adresse préfigurée de http-10:R2 @0x74C0 reste
exacte ; incohérence documentation nommée et corrigée : la docstring de
layout.py disait 0x7480, valeur D77 antérieure à l'élargissement du slot
http-08:R2 à 0x180 — BLOCS_REVISIONS, le code, fait foi). La LECTURE
CONTRACTUELLE de la spec R2 (D77) est ARRÊTÉE avant la notation :
« rax = verdict "cible TLS" » se lit au pied de la lettre — rax = 4,
valeur propre de la révision, PORTÉE PAR LE RETOUR (convention D90 :
« http-10:R2 mappe sur rax, jamais sur le cadre » ; V2 de la spec :
trois familles « verdicts http/TLS/refus ») ; la zone d'accueil est
remplie AUX RÈGLES R1 (forme ABSOLUE = 1 : la STRUCTURE reste absolue,
le schéma vit dans le verdict — le port implicite 443 est déductible du
verdict, consigné dans la sortie, la décision d'appeler tls-08
appartient à http-10:R2) ; le Q3 hérité s'applique à l'identique
(« https:// » seul, « https:///chemin » → rax = 2, autorité vide, zone
intacte) ; les verdicts 1/2/3 et tout le comportement R1 hors schéma
sont INTACTS.

**Architecture de la révision (l'ordre des tests est documenté, I5)** :
« http:// » D'ABORD — le tronçon d'entrée R1 reproduit octet pour octet
(dword « http », word « :/ », byte « / » ; l'échec du word avec [4] ≠
':' va au test https ; l'échec du byte6 avec word réussi va DIRECTEMENT
à pas_absolu : [4] = ':' contredit 's', https est impossible —
l'héritage n'a pas bougé d'un octet) ; « https:// » ENSUITE, BYTE-EXACT
sur 8 octets (garde len ≥ 8 AVANT toute lecture de [rcx+7] : jamais de
lecture hors span) ; le début d'autorité est PORTÉ dans rdx dès le
match (lea rdx, [rcx+7] / [rcx+8]) — LA GÉOMÉTRIE PORTE LE SCHÈMA — et
le verdict est déduit STRUCTURELLEMENT à l'écriture : lea r11,
[rcx+8] ; cmp rdx, r11 ; mov r11d, 1 (les drapeaux du cmp survivent au
mov) ; je .ecrit_tls. LE SCHÉMA PRÉFIXE EST IMPOSSIBLE PAR
CONSTRUCTION : « http://s://x » a son début d'autorité à rcx+7, à jamais
distinct du seuil rcx+8 — I5 falsifiable structurellement. La boucle de
scan R1 (garde en tête — terminaison héritée) est PARTAGÉE par les deux
schémas ; les cinq écritures de zone sont DUPLIQUÉES (.ecrit /
.ecrit_tls) : chaque chemin de verdict explicite, aucun
registre-drapeau. La fixture « / » @0x24D0 de l'ancêtre est RÉUTILISÉE
(déplacement RIP inter-sections : la révision cite son ancêtre,
propriété unique du bloc logique http-08, R7).

**Livré avec** : `m4/harnais_cible_r2.py` — le DIFFÉRENTIEL D'ANCÊTRE,
preuve propre aux révisions : l'ancêtre R1 scellé (assemblé à 0x5380,
round-trip 241 o — le préalable) est ÉMULÉ contre la révision sur les
MÊMES entrées. V1 round-trip R2 + idempotence + ancêtre. V2a
différentiel HÉRITÉ : 20 056 cas, R1 ET R2 contre leurs modèles (le même
modèle, revision 1/2 — seul le test https disparaît en revision 1),
ÉCART ZÉRO, divergence R1/R2 EXACTEMENT le domaine https byte-exact
(715/756 cas selon graine : R1 rend 3 zone intacte, R2 rend 4 zone
remplie ou Q3 2 sur autorité vide) — tout autre écart serait une
régression de l'héritage scellé. V2b différentiel de spécification :
zones 40 o octet par octet, le padding @4..7 JAMAIS écrit (il reste à
l'appelant). V3 fuzz D45 hérité : 20 000 cas non fiables (octets ≥ 0x80,
NUL) — survie, terminaison, verdict conforme, aucune écriture hors zone.
V4 SIX mutations stable-en-taille TOUTES ATTRAPÉES (huitième octet
amnésié, casse 's'→'S', LE SCHÉMA PRÉFIXE lea [rcx+8]→[rcx+7], verdict
4→5, forme 1→5, « ? » 0x3F→0x40) + témoin VERT — BILAN 13 PASS /
0 ÉCHEC × graines 20261028/20261029. Le différentiel a nommé UN défaut
du HARNAIS avant le vert (le domaine de divergence légitime défini par
« verdict 4 attendu » au lieu du test byte-exact : « https:// » à
autorité vide rend Q3 2, divergence 3→2 légitime classée à tort
régression — corrigé) — aucun dans la notation. LEÇON CONSIGNÉE : le
domaine d'une divergence légitime se définit par le TEST qui la crée,
jamais par le verdict qu'il produit.

**Alternatives rejetées** : porter la distinction TLS dans la forme de
zone (forme 4 @0, rax = 0 — le routage devrait lire la zone, CONTRE la
convention D90 « mappe sur rax » ; et le post R2 ne reprend pas le
Q5-R1 « zone intacte sur verdict non nul », il le remplace) ; un drapeau
registre porté à travers le scan (conflit avec movzx r11d — le
registre de scan R1 ; la déduction géométrique évite tout état) ; tester
https avant http (I5 documente l'ordre inverse : la révision AJOUTE,
R1 n'a pas changé) ; tolérer la casse mixte du schéma (Q5 : aucune
tolérance nouvelle — la surface de contrebande n'augmente que des huit
octets exacts) ; une fixture « / » propre à la révision (la fixture
appartient au BLOC LOGIQUE http-08 depuis R1 — deux fixtures pour un
même chemin par défaut doubleraient la vérité).

**Critère de sortie** : atteint — différentiel vert sur deux graines
(13 PASS × 2), falsification 6/6, héritage R1 prouvé octet pour octet
hors https par émulation croisée, entrée 77 du journal.

### D92 — M4 (b) : http-10:R2 (LA RÉVISION DE ROUTAGE TLS — la session proxy) notée-mesurée-prouvée — routage https → tls-08, table des réponses étendue (502 « Certificat rejete »), cadre de session 0x13390 ; héritage R1 prouvé par différentiel d'ancêtre à 29 blocs réels

**Contexte** : la révision http-08:R2 (D91) rend un verdict « cible TLS »
(rax = 4) — quelqu'un doit le ROUTER : P6/Q2'/Q3'/Q4'/I6' de la spécification
http-10:R2 (D77) attendaient cette révision. Les points croisés D90 : les
verdicts 4/2 transportés devaient trouver leurs entrées de table, le
« contexte de réponse » du paquet ne devait PAS être consommé par tls-08, la
ligne console « certificat rejete » ne devait PAS être double-émise.

**Arrêts contractuels AVANT la notation** (corpus cité) : (1) la ligne
console « certificat rejete » appartient à tls-08 SEUL (I4, fixture @0x2C80,
README D90 « tls-08 unique propriétaire des deux ») — la session ne la
ré-émet jamais, la réponse suit le RETOUR du verdict (« http-10:R2 mappe sur
rax, jamais sur le cadre ») ; (2) l'entrée étiquetée « HTTP/1.1 502
Certificat rejete » (34 o @0x2CA0, 8e entrée, index REP_502_CERT = 7) est la
SEULE entrée nouvelle de la table Q3' — les verdicts 2/4/5/6/7 de tls-08
mappent sur la ligne 502 R1 scellée (la table TOTALE couvre l'énumération
E2 un à un) ; (3) le port implicite 443 est le DÉFAUT passé à http-07:R1
(P3 — « consigné DANS la sortie » : le port effectif vit dans la zone, le
port EXPLICITE gagne) ; (4) un corps sur cible TLS (CL > 0) est REFUSÉ 501
— le paquet D90 porte UNE requête, tls-08:Q1 émet UNE fois puis relais
serveur→cliente seul : miroir exact du Transfer-Encoding R1 (refus honnête,
jamais de tentative).

**Convention de cadre D92** (layout.py, source unique) : 0x13390 = cadre R1
(offsets inchangés) + verdict http-08:R2 @+0x7010 (u64, écrit sur TOUT
chemin après l'appel du parseur) + garde de rdi @+0x7020 (le rep stosq du
cadre TLS emprunte le NON-VOLATIL ABI : préservé puis restitué) + paquet
@+0x7100 + cadre TLS @+0x7130 ; probing Q0 hérité D63 étendu : boucle
-0x1000..-0x13000 par pas de 0x1000, touche finale [rsp-0x13390], sub rsp,
0x13390 (multiple de 16 — ABI P5 préservé, offsets R1 numériquement
exacts). Innocuité @+0x7010/@+0x7020 prouvée par balayage de la notation
scellée (R1 n'écrit que 0x7000/0x7008/0x7018 dans la région).

**Architecture de la révision** : .cible_tls est le MIROIR EXACT de
.forme_absolue (autorité de la zone http-08, jmp .resoudre) avec SEUL écart
r8d = 443 — la chaîne http-07 → contrôles TE/CL → réécriture forme origine
est PARTAGÉE avec le chemin ordinaire (seul le transport diffère) ; le
verdict consigné est lu aux DEUX dispatches (.trancher : garde corps CL
AVANT le CONNECT/tcp-13 — r12 reste 0, la socket serveur n'est JAMAIS fermée
par la session, I1 de tls-08 ; post-réécriture : le chemin TLS ne touche ni
tcp-13 ni tcp-04) ; le paquet est rempli champ à champ puis le cadre TLS
zéroé PAR rep stosq intégral (la preuve de virginité repose sur des
canaris, jamais sur une supposition de pages fraîches) ; au retour de
tls-08 : 0 → .fin, 3 → l'entrée étiquetée, tout autre verdict → la 502 R1.
Le cas « CONNECT https:// » n'existe pas (http-08:R2 route la méthode 8
vers la forme autorité AVANT tout test de schéma).

**Livré avec** : `m4/harnais_session_r2.py` — L'INTÉGRATION LA PLUS LARGE
DU PROJET : 29 blocs réels (M0→M4, R7) PLUS l'ancêtre scellé http-10:R3
@0x5580 + http-08:R1 @0x5380 émulés sur les mêmes scénarios (Emulateur D90
sous-classé, règles shims unique source). V2a DIFFÉRENTIEL D'ANCÊTRE :
traces normalisées par la base du cadre de chaque run (l'adresse appartient
à la notation, le CONTENU au contrat) — écart ZÉRO hors domaine https,
divergence EXACTEMENT la cible https byte-exact (l'ancêtre refuse 501 ;
autorité vide : 3→2 légitime D91 ; POST-corps et HTTPS:// : identique des
deux côtés). V2b VINGT-TROIS scénarios : réponse EXACTE au client, lignes
console EXACTES (la ligne certificat UNE fois), compensation PAR COMPTAGE,
PAQUET capturé au passage de tls-08 (crochet au RVA), CADRE VIERGE en
canaris→zéro, paquet INTACT au retour. V4 ONZE mutations stable-en-taille
TOUTES ATTRAPÉES + témoin — BILAN 69 PASS / 0 ÉCHEC × graines
20261028/20261029. V6bis : prologue étendu contrôlé statiquement + rejet
I6' (un seul appel IAT = CloseHandle, aucun appel SSPI direct ni tls-01..07
direct). Le différentiel a nommé UNE FAUTE ABI avant le vert (rdi emprunté
sans reçu par le rep stosq — corrigé par la garde @+0x7020 : LEÇON un
registre non volatil ne s'emprunte qu'avec reçu, la sentinelle du harnais
EST le reçu) et la trace SEND porte désormais les octets EFFECTIVEMENT
émis (contenu tronqué au rendu de send()).

**Alternatives rejetées** : étiqueter chaque verdict de tls-08 d'une ligne
propre (la spécification ne nomme QUE le certificat — « chaque entrée
NOUVELLE est nommée ICI une seule fois » ; la 502 générique est le refus
DU TUNNEL, l'étiquette est le critère) ; relayer le corps sur cible TLS par
boucles tls-06 inline (le paquet D90 porte UNE requête, tls-08:Q1 émet une
fois puis relais unidirectionnel — le refus honnête 501 est le miroir TE ;
l'alternative contredisait l'architecture propriétaire unique) ; un
registre-drapeau TLS porté à travers la chaîne (le verdict consigné au
cadre @+0x7010 est TOUJOURS initialisé — écrit sur tout chemin avant toute
lecture — et falsifiable par mutation M1) ; étendre le sub rsp SANS étendre
le probing (la leçon D63 : le cadre de 0x13390 exige sa boucle — V6bis
l'exige statiquement, M10 l'éprouve) ; zéroer le cadre par boucle volatile
(possible : le rep stosq avec garde de rdi @+0x7020 est plus court et la
restitution est prouvée par sentinelle).

**Critère de sortie** : atteint — différentiel vert sur deux graines (69
PASS × 2), falsification 11/11, héritage R1 prouvé octet pour octet hors
https par émulation croisée à 29 blocs réels, entrée 78 du journal.

### D93 — M4 (b) : L'ORACLE À SCÉNARIOS SSPI livré — les orchestrateurs passent au volume hostile : générateurs d'HRESULT (table TOTALE), modèle de routage dérivé de I, différentiel d'ancêtre à volume, compensation par comptage ; 560 cas × 4 graines sans écart

**Contexte** : le plan D77 promettait « orchestrateurs à l'oracle à
scénarios (compensation par comptage) » et layout.py annonçait oracle_m4.py
comme consommateur du plan d'adressage. Après tls-08 (D90) et les deux
révisions (D91/D92), l'oracle est la pièce qui reste avant la carte
génération 6 et proxy.exe 0.5.0-dev.1 : le juge de paix du build à venir.

**Architecture** (m4/oracle_m4.py, 838 lignes — réutilisation stricte :
Modele/Emulateur/Script/comparer_traces/compter_compensation [D90],
EmulateurSession/ScriptR2/differentiel/charger [D92], modele_cible [D91] —
jamais deux sources de vérité). QUATRE familles :

- **F1 session tls-08 à volume hostile** — le cœur générateur d'HRESULT
  PARTAGÉ F1/F2 : poignées multi-allers (CONT à jetons variables, INCOMPLET
  qui reçoit, terminaisons CERT/échec/exotique, E5 interminable), ACH fatal
  6, tailles de flux négociées aléatoires (maxmsg ≥ 1 TOUJOURS : une découpe
  à message nul mourrait), émissions fragmentées, relais à lots/drains/
  altérations/densités « max », libérations E4 — Modele (D90) contre
  l'émulation 18 blocs : rax, cadre 0xD000 octet par octet, contrat d'appels
  complet, comptes de compensation, paquet INTACT ;
- **F2 routage http-10:R2** — le MODÈLE DE ROUTAGE D93 (dérivé de I :
  P6/Q2'/Q3') : requêtes https générées (port implicite/explicite,
  chemin/query/fixture « / », fragmentation 1-3, POST/PUT CL:0) × SSPI
  hostile + les arrêts contractuels D92 ; ModeleClient capture les octets
  effectivement émis au client (le _pomper D90 repris TEL QUEL, conformité
  au parent constatée par comparer_traces en F1), _reponse_envoyee est le
  miroir de l'achèvement E8, la table Q3' (0 → flux pompé PAR tls-08, 3 →
  l'entrée étiquetée, 2/4/5/6/7 → 502 R1 scellée) ; l'émulation 29 blocs
  confrontée sur réponse exacte, lignes console, comptes (+ socket cliente
  R1), ports, résolutions, PAQUET au passage (P6), cadre VIERGE, requête
  intacte, hygiène — ET la concordance I croisée à CHAQUE scénario par
  modele_cible (D91) : l'oracle vérifie l'exhaustivité croisée des
  spécifications, pas seulement les octets ;
- **F3 différentiel d'ancêtre à volume (R7)** — requêtes mixtes générées
  (http absolu/origine/CONNECT/malformées/https [diverge]/https+corps [refus
  IDENTIQUE]) : écart ZÉRO hors domaine https, divergence EXACTEMENT https
  byte-exact ; l'héritage http non TLS n'est PAS remodélisé — l'ancêtre
  émulé est la référence scellée (même arbitrage que l'oracle M3, prolongé
  en volume) ;
- **F4 falsification** — huit mutations (4 tls-08 + 4 http-10:R2) TOUTES
  attrapées sur les sélections fixes (attendus du MODÈLE, jamais de la
  main) ; le modèle falsifié (octets maquillés) nommé par la confrontation ;
  témoin intact 6/6 + 6/6.

**Termination par construction** (le générateur ne peut pas produire de
boucle infinie) : la poignée est bornée par la garde E5 (16 allers) ; chaque
cycle .relais consomme UNE entrée recv (liste finie à terminateur ≤ 0) ;
chaque chaîne de drain fait décroître strictement le lot ; les défauts de
listes sont bornés par les MÊMES règles côté modèle et émulation.

**Les quatre fautes nommées avant le vert** (aucune dans les notations —
l'oracle corrige l'outillage AVANT de juger le code) : (a) le layout du
paquet de TEST D90 (hôte @0x100, requête @0x200) — un hôte de plus de 0x100
octets y recouvre la zone requête : la garde tls-01 (HOTE_MAX, verdict 7)
est atteinte avant, seul le préfixe est vérifié désormais (l'artefact
appartient au harnais, jamais à la notation) ; (b) la règle E5 de la spec
R1 dit « POST/PUT sans longueur → 411 » — le générateur ne connaissait que
POST : notation lue CORRECTE, modèle corrigé ; (c) des coupes de
fragmentation dupliquées produisaient un fragment VIDE — une réception à
zéro octet, une FERMETURE pour le shim, jamais un fragment : coupes
désormais distinctes ; (d) le différentiel D92 exige que l'ancêtre DÉLIVRE
son 501 — les échecs d'émission l'abandonnaient honnêtement (E8) : la
branche divergente n'en génère plus (l'abandon est couvert par F1/F2 côté
modèle, le différentiel mesure la divergence de ROUTAGE, jamais la
livraison).

**Couverture mesurée** (diagnostic dédié, générateur non dégénéré) :
verdicts F1 {0: 18, 3: 14, 5: 68, 6: 19, 7: 31}/150 — toutes les branches
nommées, succès majoritaire PARCE QUE le chemin profond est là que les
contrats vivent (relais 16, poignée ≥ 2 allers 71, compensation non triviale
109/150) ; F2 : 61 % routés / 39 % arrêts ; F3 : 20 % divergence.

**Alternatives rejetées** : remodéliser l'héritage http non TLS en Python
(scellé 0.4.0 — l'ancêtre émulé est la référence R7, jamais deux sources) ;
un harnais supplémentaire de scénarios écrits à la main (le volume généré
aux graines différenciées bat la main — l'oracle M3 l'avait établi, D47) ;
exécuter l'oracle sur le PE entier (le build viendra : l'oracle tourne sur
les octets de notation assemblés, la même fonte que le build embarquera —
executer(blobs, graine, volume) est l'interface).

**Critère de sortie** : atteint — 560 cas (250 F1 + 150 F2 + 150 F3 + 10
F4) × graines 20261028/29/30/31 SANS écart (~18 s l'exécution complète ;
volume « reduit » 30 cas), falsification 8/8 + modèle falsifié + témoin,
entrée 79 du journal. Reste (b) : carte génération 6 (lignée D80),
proxy.exe 0.5.0-dev.1.

### D94 — M4 (b) : LE BUILD livré — proxy.exe 0.5.0-dev.1 + carte génération 6 (lignée D80) : l'image M3 composée prouvée ÉGALE au scellé 0.4.0 octet par octet AVANT extension ; libc-07 embarqué ; la porte R10 gagne son entrée ; 417 verrous structurels + oracle 560 cas sur les blobs du build

**Contexte** : dernière pièce de l'étape (b) promise par D77. La chaîne
est unique et totalisante : `m4/build_m4.py` (~1 290 lignes) +
`m4/carte_m4.py` — notation (keystone) → octets → PE32+ à la main (CINQ
sections) → carte chiffrée/signée, chaque maillon prouvé avant le suivant.

**L'héritage, re-vérifié pas re-cru** : build_m3.assembler_tout() rejoué
sous import contrôlé (R5 26/26 round-trip 100 %, 524 verrous M3) ;
l'image M3 composée est confrontée au proxy.exe 0.4.0 scellé (sha
bf02769f…) **octet par octet, AVANT toute extension** — le squelette du
0.5.0-dev EST le scellé, reproductible depuis les notations seules.

**libc-07 embarqué** (b20007, memset — exigé par tls-06/tls-07) :
slot 0x13C0 dans la zone reserve-libc (int3 en M3), octets identiques à
selftest.exe (R7 direct). **La porte R10 gagne son entrée** : 27 blocs +
terminateur finissent EXACTEMENT à 0x2820 = R_VERSION (la zone était
taillée pour ça) — l'entrée appendue @0x2800, terminateur descendu à
0x2810, le http-12 scellé garde la nouvelle entrée AU LANCEMENT sans
qu'un octet du scellé bouge ; la validation recalcule les 27 sommes du
binaire final, version 0x00050001 ≥ plancher scellé.

**Deltas .rdata documentés (R7)** : 8e entrée de la table des réponses
@0x2550 (l'entrée ÉTIQUETÉE D92) ; entrée R10 libc-07 ; version ;
extension M4 @0x29A0+ (descripteurs 3 DLL — répertoire d'imports
déplacé, les 60 o M3 restent espace mort —, secur32.dll, IAT/INT/hints
×7, package, fixtures tunnel/cert/502). Tout octet divergent hors
deltas = échec.

**Arrêt D94 — offsets fichier** : la cinquième en-tête de section porte
les en-têtes à 528 o — .text quitte 0x200 : packaging fichier +0x200,
CONTIGU (0x400/0x1400/0x2400/0x2E00/0x4E00, fin 0x6E00 = 28 160 o),
RVA INTACTS (chaque artefact lu à ses offsets propres ; la
préfiguration D77 TEXT3_FILE=0x4E00 l'avait encodé). Le débordement
d'en-tête (Characteristics écrasé par le int3 de .text) fut nommé par
la validation AVANT l'écriture du fichier.

**Oracle structurel M4 (417 verrous)** — tables d'autorisation extraites
par diagnostic (scripts/diag_structure_m4.py) : IAT PAR BLOC (sept
secur32 vérifiées ; tls-08 AUCUNE — tout wrappé ; http-10:R2 CloseHandle
SEUL, I6'), appels directs (I1), données RIP (I2/I5), sauts internes,
padding D8, pile alignée, syscall interdit, stockage sous RSP interdit —
plus la CONCORDANCE des déplacements RIP DÉCLARÉS (la table d'en-tête de
notation relue contre le désassemblage : la métadonnée est falsifiable),
le prologue probing D63 armé sur 0x13390, et les tailles déclarées ==
assemblées. canon() étendu (alias jcc, qualificateurs déductibles,
complément à deux à la largeur de l'instruction, crochets, chaînes) —
la notation reste la vérité, l'octet reste le juge.

**La carte génération 6** (lignée D80 — phrase courante, MÊME graine
Ed25519 : le témoin d'intégrité ne bouge pas) : 4 fragments
XChaCha20-Poly1305, racine SHA-256, signature Ed25519 ; 48 blocs sur
5 artefacts ; [build] version=0.5.0-dev.1 empreinte=43e2e40d… ;
verrou croisé 48 empreintes ; cristallisation 3/10 en trois runs, artefact
BYTE-STABLE. Anti-rollback R6 armé (carte scellée → reconstruction
interdite).

**Alternatives rejetées** : recomposer l'héritage M3 dans build_m4 (le
code M3 est LA source — import sous régime contrôlé, jamais deux
vérités) ; étendre la table R10 au-delà de 27 entrées (déborderait
R_VERSION @0x2820 — la zone est exactement pleine, un R10 .text3
viendra avec le câblage http-12:R2, pas en contrebande) ; retirer les
ancêtres R1 de .text2 (R7 : la zone scellée ne bouge pas d'un octet).

**Critère de sortie** : atteint — proxy.exe 0.5.0-dev.1 (28 160 o, sha
43e2e40d…) : 37 blocs embarqués, R5 37/37 verifier-puis-écrire, oracle
560 cas verts, carte signée, verrou croisé 48, tableau de bord conforme.
Étape (b) CLOSE. Suite M4 : http-12:R2 (câblage du routage vers
http-10:R2 — l'orchestrateur scellé appelle encore R1), terrain (c)
(curl https:// par le proxy, certificat invalide → 502 propre),
cristallisation 10/10, scellage 0.5.0. Entrée 80 du journal.

### D95 — M4 : LE CÂBLAGE livré — http-12:R2 notée-mesurée-prouvée puis embarquée : proxy.exe 0.5.0-dev.2, la boucle lance http-10:R2 (0x74C0), l'entrée PE passe à 0x7DC0, LA PORTE R10 .text3 vient avec le câblage (entrée #28 @0x2810, marche aux BORNES, fail-closed sur entrée trouée) ; harnais 12 PASS × 2 graines (400 mutations de porte, 6/6 falsifications) ; 473 verrous structurels + oracle 560 cas ; cristallisation 3/10, byte-stable

**Contexte** : D94 avait clos l'étape (b) sur un corps sans câblage —
l'orchestrateur scellé http-12:R1 lançait encore http-10:R1 @0x5580. La
pièce exigée par le terrain (c) avant le scellage 0.5.0, promise par
l'arbitrage D94 (ii) (« un R10 .text3 viendra avec le câblage, pas en
contrebande »).

**La révision minimale** : UNE instruction fonctionnelle change —
`lea rcx, [rip - 0xa1e]` → 0x74C0 (http-10:R2, D92) au lieu de 0x5580.
Le reste est l'héritage R1 instruction pour instruction (ordre D42,
ExitProcess 0/1/2) — le différentiel d'ancêtre le PROUVE trace à trace :
12 scénarios, écart UNIQUE = la cible du spawn session. L'entrée PE
passe à 0x7DC0 (delta PE documenté) ; l'ancêtre @0x1800 reste embarqué
octet pour octet (R7 — mort au lancement, vivant à la preuve d'héritage).

**La porte R10 .text3** : la table est PLEINE (27 entrées + terminateur
@0x2810, R_VERSION @0x2820 immovable R7) — l'entrée #28 (0x6000, 0x2000,
somme .text3) REMPLACE le terminateur et la marche de http-12:R2
s'arrête à la BORNE (l'adresse de R_VERSION — jamais son contenu avant
la fin). Fail-closed RENFORCÉ : rva nul ou taille nulle = ÉCHEC (un
trou nomme une corruption — la troncature silencieuse du terminateur
M3 n'existe plus). La somme couvre TOUTE la couche .text3, bloc 0x7DC0
compris : LA PORTE SE GARDE ELLE-MÊME (miroir de http-12:R1 gardé par
la table M3). La couche M4 entière — qui n'était gardée que par la
carte + l'oracle + le verrou croisé depuis D94 — devient gardée AU
LANCEMENT.

**Le harnais** (`m4/harnais_principal_r2.py`) : V1 round-trip (R2 + 
ancêtre à 0x1800) ; V2 différentiel d'ancêtre (la divergence légitime
.text3 est NOMMÉE : R1 ne la garde pas, R2 la nomme KO — miroir du
domaine https D91) ; V3 fuzz de la porte — le modèle (spécification)
et l'émulation (octets) nomment le MÊME verdict, ZÉRO passage
silencieux ; V4 six mutations stables en taille TOUTES attrapées —
en tête LE CONTRE-CÂBLAGE (lea → 0x5580), puis les bornes décalées
±0x10 (l'entrée .text3 sautée / la version lue comme entrée), le
plancher abaissé, le code E3, le sens du test d'arrêt. **Cinq fautes
du HARNAIS nommées avant le vert** (symboles de fixtures croisés
MSG_KO/MSG_ERREUR/MSG_CONNEXION ; drapeau R_QUIT semé un octet sur un
qword ; appel tcp-01 omis du modèle en échec d'écoute ; remplissage
uniforme → collisions de somme, puis linéaire → périodicité : PRNG
seedé ; mutations sans effet tirées au fuzz) — aucune dans la notation.

**Le build dev.2** : g70011 @0x7DC0 × 0x200 (la section ne grandit
pas — 28 160 o INCHANGÉS, l'ancienne réserve int3 absorbe le câblage) ;
la section .text3 est composée D'ABORD (la porte scelle sa somme
dessus) ; AddressOfEntryPoint 0x7DC0 ; validation = marche aux bornes
28 entrées (le MÊME contrat que la notation — jamais deux sources) ;
version 0x00050002 ; oracle structurel 473 verrous (+56 : IAT
g70011, appels directs, données RIP dont les DEUX cibles de code par
lea — pointeurs de fonctions pour tcp-06) ; verifier-puis-écrire
38/38 ; carte 49 blocs, verrou croisé 49 empreintes + signature ;
cristallisation 3/10 en trois runs, sha INCHANGÉ
(b813f65e…) ; anti-rollback armé (dev.2 > dev.1 licite).

**Le critère M4 est CÂBLÉ de bout en bout** : l'entrée PE →
http-12:R2 → http-10:R2 → tls-08 → Schannel. Reste : terrain (c),
cristallisation 10/10, scellage 0.5.0.

Conséquences : layout.py (arrêt D95 : g70011, ENTREE_R2, VERSION_DEV2,
constantes R10_PORTE_TEXT3/BORNE/NB_ENTREES, zones) ; auteur.py
(_FICHIERS g70011, SYMBOLES SESSION_R2) ; build_m4.py (onzième bloc,
porte .text3, entrée PE, validation bornée, deltas, compteur 38/49) ;
harnais_principal_r2.py NOUVEAU ; spec m4/I/http-12-principal-r2.md
NOUVELLE (écrite-avant-code) ; notation + brouillon NOUVEAUX.
Aucune clé touchée (phrase D81 valable, conteneur 0323029a… inchangé).

### D96 — M4 : la MOITIÉ du reste scellée — cristallisation 10/10 (49/49 blocs, 10 runs byte-stables) + TERRAIN.17 livré : T4 (sup-38, 1 505 o) juge le tunnel M4 sur machine réelle — le kit embarque proxy.exe 0.5.0-dev.2, la 502 étiquetée attendue OCTET POUR OCTET, les fixtures croisées contre les octets de l'artefact ; la dérive de notations du dépôt (D48) nommée et réparée ; l'alignement des VA de section (leçon .rsrc 0x7800) attrapée par le build avant livraison

**Contexte** : D95 avait laissé trois pièces : terrain (c), 
cristallisation 10/10, scellage 0.5.0. Deux sont closes ici — la
troisième n'attend plus que le journal du développeur.

**Cristallisation M4** : sept runs --verifier neufs (graines 
20261101-20261107, volume complet — 560 cas d'oracle par run)
portent les 49 blocs à 10/10 ; dix runs journalisés dans frag-prf ;
sha b813f65e… INCHANGÉ à travers les dix reconstructions ; verrou
croisé re-scellé à chaque run (faits inchangés, modèle D80). La
pièce est POSÉE.

**T4 — le problème et le véhicule** : la forme absolue « GET 
https://… HTTP/1.1 » — LA porte du tunnel M4 (http-08:R2 Q4) — 
n'existe dans AUCUN client standard (curl -x envoie CONNECT et 
chiffre lui-même : le tunnel M4 ne serait pas exercé). Le superviseur
pose donc un script client powershell (terrain_m4.ps1, 438 o — une
DONNÉE du plan : fixture RX couverte par la table R10, posée par 
memcpy + sup-36, jamais un octet de code superviseur ; I5) qui écrit
la requête à la main sur 127.0.0.1:25000 (« Connection: close » : la
fin propre du relais tls-08 est un contrat du script) et recopie la
réponse. DEUX requêtes : example.com saine (page « HTTP/1.1 200 » +
événements 58 o memcmp exact) ; self-signed.badssl.com 
(SEC_E_UNTRUSTED_ROOT → LA 502 étiquetée 34 o memcmp EXACT + 
« certificat rejete » 54 o). Neuf bits de succès — le miroir exact 
des neuf de T2. sup-38 : spec écrite-avant-code, 1 505 o / 331 
instructions / slot 0x7200×0x600, sous-routines .ligne/.ligneNum/
.attendre/.ps/.flux (facteurs communs — le premier jet faisait 
1 649 o, trop gros pour le slot).

**Les croisements** : croiser_fixtures_t4() lit le .rdata du proxy 
M4 scellé (pefile RVA→offset) et asserte bannière/événements/502 ==
les octets de l'artefact — DIX verrous au build, fail-closed. La 
502 que le superviseur attend est la 502 que le scellé émet — 
jamais deux sources.

**Layout terrain.17** : .text2 0x4000 (T4 @0x7200) ; table R10 à 28 
entrées + terminateur = 464 o — LA TABLE EST PLEINE, touche l'ancre 
scellée sans la chevaucher (miroir D95) ; .rsrc 0x8000, .blob 0x9000 
(0xAF10 — le proxy M4 fait +8 704 o) ; image 0x14000 ; 75 264 o ; 
version terrain.4 (u64 0x00050104). **LEÇON (attrapée par le build 
AVANT livraison)** : le premier jet posait .rsrc à 0x7800 — NON-
alignée sur SectionAlignment (0x1000) : pefile ajustait la VA à 
0x7000 et le répertoire des ressources devenait illisible (le 
chargeur Windows exigerait la même discipline). Toute VA de section 
reste alignée sur SectionAlignment — invariant désormais consigné.

**La dérive du dépôt nommée** : les notations terrain committées 
dataient de D48 — les retouches D68 (nettoyage T3 à 4 temporaires : 
terrain_jeton.json SURVIT ; relais jeton-KO mode 1) vivaient dans 
des notations locales jamais committées. La régénération auteur.py a 
surfacé la dérive (jeton.json supprimé, S33B muet) : les retouches 
sont PORTÉES dans les sources authoritatives (brouillon sup-35, 
_SEQ_SUP_2 réordonné — les quatre temporaires contigus, jeton.json 
hors du chemin de la marche). Le dépôt redevient la vérité : 
brouillon → auteur → notation, bout en bout.

**L'oracle** : file flux_proxies (un flux console PAR proxy mode 1, 
servi au lancement — le premier jet double-popait : T2 lisait la 
voix de T4) ; CreatePipe en modulo (deux paires pour deux proxies) ; 
powershell scripté par cmdline ; journal d'or S40-S49 + la voix du 
tunnel ; verrous I5/I6/I1 (script == fixture, mode 0 sans héritage, 
ordre A→B) ; dégradés (i) 502 tronquée à 33 o ATTRAPÉE et (j) 
événements B muets nommés ; falsifications M6 (ordre T2/T4 inversé 
— refusé) et M7 (longueur du nom composé) : 7 mutations attrapées. 
BILAN : 10 111 cas verts, 28/28 R10, 1 090 verrous structurels, 
cristallisation terrain 10/10 (sha 5360ffe2… inchangé), carte 24 
empreintes. Livraison : superviseur-terrain17.exe (variante 
publique) + LISEZMOI-terrain17.txt dans download/ — md5 
e7587c46feef6f79a88e66a78c9d5729.

Conséquences : terrain/layout.py (zones, .rsrc/.blob alignés, kit 
M4, fixtures T4 + ps1, version terrain.4) ; terrain/I/sup-38-tunnel.
md NOUVELLE + sup-09-scenario.md R3 + README charte T4 ; brouillons 
+ notations sup-38 NOUVEAUX, sup-09/sup-37/sup-35 régénérés ; 
terrain/outils/auteur.py (TEST_TUNNEL, f60038) ; build_terrain.py 
(M4_DIR, croisements, R10 28, versions, CONTRATS f60038/f60009 R3) ; 
oracle_terrain.py (flux_proxies, modulo tuyaux, T4 complet) ; 
carte_terrain.py (entête terrain.4). Aucune clé touchée (phrase D81 
valable, conteneur 0323029a… inchangé).

---

## D97 — terrain.17-B : le motif loader D54 porté au dépôt (habillage

d'import restauré)

Contexte : rapport machine réelle — « il ne se passe rien » au double-clic

du superviseur-terrain17.exe. Le kit M4, T4 et le proxy 0.5.0-dev.2 étaient

sains ; le processus mourait à l'initialisation du chargeur (Windows 11

build 26300 Insider résout kernel32#3/user32#2 par le chemin FirstThunk :

les slots IAT du fichier doivent porter des pointeurs de hints valables,

les hints/INT vivant en .rdata non exécutable — leçon terrain.4/terrain.5,

D54). Le correctif D54 n'avait jamais été committé : la régénération D96

l'a perdu ; l'oracle est resté vert à juste titre (il résout les imports

lui-même — il ne juge pas le chargeur).

Décision : (i) restaurer le motif aux adresses fixes du terrain16, prouvées

sur la machine (IAT pré-remplies @0x2300/0x2360, OFT → 0x2B40/0x2B90, INT +

hints .rdata @0x2B40-0x2C79) — .rdata est hors table R10 : la porte ne

bouge pas, le test terrain.17 est inchangé (même S00/L00, même version) ;

(ii) PORTER le motif aux sources (layout.py : constantes fixes ; build_

terrain.py : descripteurs #3 → INT .rdata, hints/INT posés, IAT

pré-remplie — miroir des tables héritées D35) : une régénération future ne

pourra plus le perdre ; (iii) reconstruire par la chaîne complète et

re-sceller la carte (24 empreintes + Ed25519 + R8) — le rebuild reproduit

le correctif chirurgical octet pour octet (sha256 991dcb5e…).

Conséquences : terrain/layout.py (+R_INT_K32C_RDATA/R_INT_U32B_RDATA/

HINTS_K32C_RDATA/HINTS_U32B_RDATA) ; terrain/build_terrain.py (descripteurs

#3, pose du motif, IAT pré-remplies) ; superviseur.exe (dépôt) = balise

991dcb5e… ; download/superviseur-terrain17b.exe + LISEZMOI-terrain17b.txt

(le 17 cassé retiré, mono-génération) ; Entrée 83, worklog Task ID 24.

LEÇON consignée : un correctif non-committé est un correctif qui n'existe

pas — l'habillage d'import fait partie de la surface de test terrain.

Aucune clé touchée (phrase D81 valable, conteneur 0323029a… inchangé).

## D98 — terrain.17-C : l'ombre ABI x64 réparée et VERROUILLÉE (le superviseur ne meurt plus au premier curl — le proxy orphelin du run 17-B expliqué et soldé)

**Constat machine (run 17-B, 29/10 01:46)** : fenêtre ouverte (D54 tient),
T2 lancé, bannière reçue — puis mort silencieuse pendant l'attente curl :
journal coupé après la bannière (aucun S22), fenêtre fermée, proxy.exe
orphelin (mode 1, arrêt jamais exécuté, port 25000 occupé). La page
rapatriée (3 961 o, la VRAIE page neverssl.com) prouve le relais M4 réel :
curl a tout reçu, c'est le superviseur qui est mort en aval.

**Diagnostic (A/B bloc par bloc terrain16 ↔ 17-B)** : .curl de sup-34
portait `sub rsp, 0x28` prouvé machine (terrain16, T2 complet) — la
régénération D96 l'avait réduit à `sub rsp, 8` : l'OMBRE ABI x64 (0x20 de
maisons d'arguments sous rsp) avait disparu, la maison rdx de
WaitForSingleObject/GetExitCodeProcess recouvrait l'adresse de retour —
troisième manifestation de la dérive de dépôt (D54, D68, D98). Même faute
dans .ps de sup-38 (T4 serait mort au premier powershell). Aucune autre
violation (audit dédié : m0-m4/démo/terrain).

**Pourquoi l'oracle est resté vert** : les shims ne déversent pas dans les
maisons (l'ombre est invisible à l'émulation) ET `_prologue_aligne`
vérifie l'alignement mod 16, pas l'ombre — `sub rsp, 8` est aligné et nu.
La faille était le verrou incomplet, pas l'oracle.

**Correctif (taille-neutre, chirurgical)** : `sub/add rsp, 8` → `0x28`
dans .curl et .ps (imm8 → imm8, aucun octet en aval ne bouge) ; porté aux
BROUILLONS (source unique : brouillon → auteur → notation) ; différentiel
17-B → 17-C : 8 octets (4 code + 4 sommes R10), motif D54 intact ;
verrou neuf `_ombre_abi()` (fenêtre < 0x28 + appel IAT = ÉCHEC, appels
internes tolérés — convention prouvée machine) : oracle structurel
1 090 → 1 114. Chaîne verte : R5 100 %, croisement T4 10/10, oracle
10 111 cas + 28/28 + 7 mutations, carte génération 5 re-scellée.

**Livraison** : superviseur-terrain17c.exe (75 264 o, md5 b0f912ba…,
sha256 c381d088…) + LISEZMOI-terrain17c.txt (ÉTAPE 0 : tuer le proxy
orphelin — taskkill /IM proxy.exe /F — il tient le port 25000) ; le 17-B
retiré (mono-génération) ; superviseur.exe (dépôt) = balise c381d088… ;
Entrée 84, worklog Task ID 25. T2 juge la PRÉSENCE de page (octets=N,
N≠640 légitime : le M4 relaie la vraie page), pas son contenu.

LEÇON consignée : alignement n'est pas ombre — un cadre aligné peut être
mortel ; l'ABI de la machine cible fait partie de la surface de test
terrain, au même titre que son chargeur (D97). Aucune clé touchée (phrase
D81 valable, conteneur 0323029a… inchangé).

## D99 — terrain.17-D : le diagnostic armé (le run 17-C a PROUVÉ le critère M4 — tunnel + certificat + 502 exacte — et nommé une anomalie de relais page A ; la révision conserve les DEUX faits qui manquaient au journal : témoin de la page SUR LE DISQUE, ligne S47 du code de sortie)

**Constat machine (run 17-C, 29/10 05:59)** : le correctif D98 a tenu —
T2 VERDICT OK, T4 complet : « tunnel chiffre etabli » (première fois), «
certificat rejete » (première fois), 502 étiquetée octet pour octet (34 o)
— LE CRITÈRE M4 « HTTPS en transit ; échec propre sur certificat invalide »
EST PROUVÉ SUR MACHINE RÉELLE. Reste UNE anomalie : « S49 T4 VERDICT KO »
avec « S44 page exemple octets=13 » — la page A (~1 300 o attendues)
livrée sur SON PREMIER ENREGISTREMENT déchiffré puis fermeture propre
immédiate (aucune 502 en suffixe : le chemin n'est PAS l'échec nommé de
tls-08 ; aucune corruption de boucle : le client a reçu une FIN propre).

**Élimination (neuf bits)** : bits 1-8 prouvés posés par les lignes du
journal (chaque ligne suit son memcmp gagné) ; tout chemin propre du
relais mène à S49A — le bit manquant désigne le CONTENU exact des 13
octets (bit 3) ou le CODE DE SORTIE du proxy (bit 9 — E6 : un handle SSPI
survivant tuerait le processus en sortie). Le journal 17-C ne pouvait pas
départager : page supprimée au nettoyage, code de sortie jamais journalisé.
La cause racine bas niveau (DecryptMessageW réel vs shim — résidu Extra,
frontière d'enregistrement) ne sera nommée qu'avec les faits : discipline
D54/D68/D98, l'évidence AVANT le correctif.

**sup-38:R2 (écrite-avant-code)** : Q5' LE TÉMOIN — les LU octets lus de
la page A sauvés vers TAMPON_COMPO puis posés sous temoin_m4a.txt (sup-36
op 1), fichier SURVIVANT au nettoyage Q11 (miroir terrain_page_http.txt
côté T2 : la preuve vit sur le disque, jamais dans le journal — charte
§ 3 entière) ; LU = 0 → témoin vide ; résultat ignoré (jamais un bit).
Q9' LA LIGNE S47 — « S47 T4 exit proxy=N » journalisé après
GetExitCodeProcess sur TOUT chemin, avant le verdict : exit 0 = chemin
propre (arret → WSACleanup → ExitProcess(0)), autre code = mode de mort
nommé (E6 détachement, TerminateProcess timeout, exit 1/2).

**Le piège nommé par l'oracle AVANT la machine (fail-closed)** : (a)
l'écriture du témoin COMPOSE SON CHEMIN dans TAMPON_CMD — le tampon qui
porte la page lue — le premier jet détruisait la page avant le memcmp
FIX_200 → .temoin devient SAUVER → ÉCRIRE → RESTAURER (double memcpy,
transparent pour l'appelant) ; (b) le motif de mutation M8 devait compter
15 (nom + NUL) ET être discriminé de l'écriture FIX_PS1 par le mov
r9d,[rip+LU] qui suit (44 8b 0d vs 41 b9 immédiat).

**Géométrie (table R10 PLEINE — miroir D95/D96)** : AUCUN bloc nouveau —
.temoin/.exitline vivent DANS sup-38 (motif .ligne/.ps), slot 0x600 →
0x800 (0x7800-0x7FFF libre en .text2), l'ENTRÉE R10 T4 seule change de
taille (28 entrées conservées, la marche par terminateur inchangée) ;
code 1 645 o / 357 ins / 403 padding. Chaîne verte : R5 100 % (357/357),
croisement T4 10/10, oracle structurel 1 130 verrous, scénario 10 114 cas
+ 28/28 + 9 mutations (M8 : nom du témoin 15→14 le NUL plus porté ; M9 :
ligne S47 tronquée 18→17), carte génération 5 re-scellée (24 + Ed25519 +
R8 OK), PE 75 264 o TAILLE INCHANGÉE, cristallisation 3/10 en trois runs
byte-stables.

**Différentiel 17-C → 17-D (vérifié binairement)** : 1 652 octets en 12
plages TOUTES NOMMÉES (entrée R10 T4 + version en .rdata ; fixtures R2
appendues en zone sup 3 ; reflow du code sup-38 ; chaînes .rsrc) — kit
embarqué INTACT (demo 73c064fb…, proxy M4 33c91815…), motif loader D54
INTACT, monotonie 0x00050104 → 0x00050105. RIEN d'autre ne bouge.

**Livraison** : superviseur-terrain17d.exe (75 264 o, md5 18aa0a66…,
sha256 e82924dd…) + LISEZMOI-terrain17d.txt (ÉTAPE 0 inchangée ; DÉPOSER
dans /test du Drive : le journal ET temoin_m4a.txt ET les pages T2 si
présentes) ; le 17-C retiré (mono-génération) ; superviseur.exe (dépôt) =
balise e82924dd… ; Entrée 85, worklog Task ID 26. Lecture du verdict
quadrichotomique : S47=0 + S49 OK → anomalie passagère (scellage 0.5.0
ouvert) ; S49 KO + S47=0 + témoin tronqué → correctif relais tls-08 ;
S49 KO + S47≠0 → correctif compensation E6.

LEÇON consignée : un verdict KO sans ses faits est un échec muet — la
PREMIÈRE réaction à une anomalie terrain est de la FAIRE PARLER (préserver
l'évidence), la deuxième seule-ment de la corriger ; chaque run terrain
doit rapporter ses propres preuves (le journal seul ne suffit pas quand le
doute porte sur un contenu). Aucune clé touchée (phrase D81 valable,
conteneur 0323029a… inchangé).

### D100 — terrain.17-E : LA CHARTE PROTÉGÉE — le run 17-D a livré « S47 exit proxy=0 » (PREMIÈRE FOIS : la compensation intégrale tient sur machine réelle, E6 mort) et le TÉMOIN a parlé (page A = la 502 « Passerelle inaccessible » DU PROXY — tcp-13 en échec, réseau intermittent autour, proxy INNOCENT : neverssl ET example.com injoignables en amont pendant que CONNECT/badssl répondaient) ; le journal a révélé une FUITE I2 (40 o de page recopiés par .evt_a_ko journalisant TAMPON/LU PÉRIMÉS après un timeout qui n'a rien lu) et l'émulation a nommé le piège latent (à LU=640 : la ligne de fuite déborde du tampon journal, écrase l'état .data — LU lu comme count, memcpy sauvage 0x45004500450045 — et tuerait le superviseur en plein T4) ; correctif sup-38:R3 TAILLE-NEUTRE : les DEUX timeouts silencieux (je 74 48 → 74 56 vers .req_b/.arret, miroir sup-34 — rien lu, rien journalisé ; la divergence memcmp seule journalise les OCTETS LUS) ; verrou d'oracle (k) « proxy M4 muet » qui REJETTE le 17-D nommément et passe le 17-E (10 117 cas verts) ; différentiel 10 octets / 8 plages (kit INTACT, loader INTACT, monotonie 0x00050105 → 0x00050106) ; livraison superviseur-terrain17e.exe (75 264 o, sha256 234b99d6…, md5 739cbd42…, version 0.5.0-terrain.6) + LISEZMOI (ÉTAPE 0 BIS : vérifier le réseau avant le run) ; le 17-D à la corbeille (mono-génération)

Le run 17-D (journal terrain_20261029_071458.txt + témoin 40 o, tous
deux déposés dans /test) ferme la question laissée ouverte par D99 :

1. **S47 T4 exit proxy=0** — le code de sortie du proxy journalisé pour
   la première fois : la compensation intégrale de tls-08 (Q3 : contexte
   détruit, credentials libérés, socket serveur fermée — exactement une
   fois chacun, dans cet ordre) TIENT sur machine réelle. L'hypothèse E6
   (handle SSPI survivant tuant la sortie) est morte : exit 0 constaté.
2. **Le témoin répond à la question du 17-C** : la page A du run 17-D
   n'était pas une page tronquée mais la 502 du proxy lui-même (« cible
   injoignable », tls-08 E1) : tcp-13 n'a pas joint example.com à 07:14.
   Le proxy a réagi selon sa spécification (502 propre, service continu,
   badssl traité juste après, sortie propre) — la panne était le réseau
   de la machine (neverssl.com ET example.com injoignables en amont,
   curl http code=28 + même 502 reçue ; pendant que example.com via
   CONNECT et badssl répondaient). L'anomalie « 13 o » du 17-C (tunnel
   vécu, relais tronqué) reste ouverte — différente de celle-ci.
3. **La fuite I2** : le journal du 17-D contenait les 40 o de la page
   (charte § 3 : jamais d'octets de page dans le journal). Mécanisme :
   .evt_a_ko journalise (TAMPON, LU) ; après un timeout, le sondage
   n'a rien lu et TAMPON/LU portent ENCORE la page A. La même mécanique
   explique chaque ligne « tassée » du journal (reconstruction octet par
   octet : « tun » = la lecture fixe de 43 o coupant « tunnel », le
   « connexion entrante\r » = la lecture de 54 o mêlant résidus de A).
4. **Le piège latent, nommé avant qu'il ne tue** : à LU = 640 (une vraie
   page), la ligne de fuite compose au-delà du tampon journal, écrase
   l'état .data (LU relu comme count : memcpy sauvage) et fait planter
   le superviseur — prouvé en émulation par crochet (le dernier memcpy
   au count 0x45004500450045, les octets de page devenus longueur).

**Le correctif (sup-38:R3, écrit-avant-code)** : les deux branchements
de timeout deviennent SILENCIEUX — branchement direct (je 74 48 → 74 56,
rva 0x73F5 vers .req_b et 0x74EA vers .arret), miroir de sup-34 qui n'a
jamais journalisé sur timeout. La divergence memcmp seule journalise,
les octets LUS — preuve valide. Taille-neutre : 1 645 o / 357 ins /
403 o padding inchangés.

**Le verrou** : cas d'oracle (k) « proxy M4 muet » — le 17-D est rejeté
nommément (« la ligne de fuite déborde du tampon journal et emporte
l'état .data : memcpy sauvage »), le 17-E passe. Oracle 10 117 cas
verts (+3), falsification 28/28 + 9 mutations, R5 100 % (357/357),
structurel 1 130 verrous, croisement T4 10/10, carte génération 5
re-scellée (24 + Ed25519 + R8), cristallisation 2/2 byte-stables
(graines 20261029/20261030, sha256 234b99d6… inchangé).

**Différentiel 17-D → 17-E (verif_terrain17e.py)** : 10 octets en 8
plages nommées — les deux 74 48→74 56, la somme R10 T4 (4 o), l'u64 de
version (0x00050105 → 0x00050106), les champs .rsrc (0.5.0.6/terrain.6).
Kit INTACT (demo 73c064fb…, proxy 33c91815…), loader D54 INTACT,
géométrie R10 T4 inchangée (0x800). RIEN d'autre ne bouge.

**Livraison** : superviseur-terrain17e.exe (75 264 o, md5 739cbd42…,
sha256 234b99d6…, version 0.5.0-terrain.6 / u64 0x00050106 /
FileVersion 0.5.0.6) + LISEZMOI-terrain17e.txt dans /test du Drive
(md5 MATCH) ; le 17-D à la corbeille (mono-génération D69 ; référence
locale scripts/superviseur-terrain17d_ref.exe pour rejouer le
différentiel) ; sentinelle dépôt = 234b99d6…. PROTOCOLE : ÉTAPE 0
(taskkill) + ÉTAPE 0 BIS (curl -s -o NUL https://example.com/ —
vérifier l'amont AVANT le run) ; déposer journal + témoin + pages T2.

**Lecture du verdict (mise à jour)** : S49 OK + témoin « HTTP/1.1
200… » → page complète, scellage 0.5.0 ouvert ; S49 KO + S47=0 + témoin
502 Passerelle → réseau amont coupé (réessayer) ; S49 KO + S47=0 +
témoin « 200 » tronqué → correctif relais tls-08 (l'anomalie 13 o du
17-C). Le verdict final reste « ECHEC » tant que T1/D57 est KO —
l'honnêteté du superviseur.

LEÇON : un tampon non lu n'est pas une preuve — journaliser un état
qu'on n'a pas lu, c'est forger ; la charte § 3 protège le journal
D'ENREGISTREMENT, et à grande page la ligne de fuite était une bombe.
Limite assumée : le lecteur d'événements à longueur fixe se
désynchronise quand le flux diverge — verdicts honnêtes, diagnostics
tassés (le memcmp exact est un choix). Aucune clé touchée (phrase D81
valable, conteneur 0323029a… inchangé).

### D101 — terrain.18 / 17-F : LE PRÉVOL — les ÉTAPES 0/0 BIS du protocole deviennent AUTOMATIQUES (demande développeur du 29/10 : « peux-tu intégrer la commande taskkill et la verif curl dans le superviseur ? » — le réflexe manuel constaté depuis D98/D99/D100 : tuer le proxy orphelin, sonder l'amont) ; le bloc neuf f60039 (169 o) est ZONE-RÉSIDENT en queue de zone données sup 1 (0x4B40-0x4BFF) car la table R10 est PLEINE depuis terrain.17 (28 entrées : le code vit SOUS l'entrée de zone, la falsification passe par la somme, la porte reste juge, aucune case neuve) ; sup-09:R4 l'appelle APRÈS porte+libc, AVANT l'extraction (un proxy.exe orphelin verrouille le fichier à re-poser et tient le port 25000) ; S08 « orphelins proxy/demo : taskkill code=N » (0 tués / 128 propre / autre refus) + S09 « reseau amont : curl code=N » (0 vivant / 6/7/28 DNS-connexion-timeout : la panne du 17-D désormais prouvée DANS le journal avant tout test) ; codes BRUTS, JAMAIS au verdict (une évidence, pas un juge — miroir du témoin D99) ; chaîne verte : 10 124 cas verts (+7 : échec (l) prévol dégradé — taskkill absent + amont 28, verdict = 1, sondes jamais comptées ; mutation M10 — ligne S08 amputée rejetée par le journal d'or ; cible porte 29e par somme de zone), 1 158 verrous structurels, 29/29 falsifications + 10 mutations, carte re-scellée (25 empreintes Ed25519), PE 75 264 o TAILLE INCHANGÉE, sha256 81f7ef3f…, md5 2d2bc168…, version terrain.7 (u64 0x00050107) ; différentiel 17-E → 17-F : 579 octets en 11 plages TOUTES NOMMÉES (kit INTACT, loader D54 INTACT, 28 entrées R10 conservées) ; livraison download/superviseur-terrain17f.exe + LISEZMOI (protocol réduit à UNE étape : plus de taskkill/curl manuels) ; la 2e fenêtre du run expliquée au développeur (la coquille démo de T1, refermée par la panne connue D57) ; canal Drive /test BLOQUÉ : refresh OAuth mort (400 invalid_grant) + compte de service authentifié mais LECTEUR seul (403 création) — attend le partage Éditeur du dossier test au z-ai-811@physichong.iam.gserviceaccount.com (ou reprise OAuth interactive)

Le développeur a posé la question la plus rentable du projet : trois
générations de suite, le protocole lui demandait DEUX gestes manuels
avant chaque run (D98 : « taskkill /IM proxy.exe /F » — le proxy orphelin
tient le port 25000 ; D99/D100 : « curl -s -o NUL https://example.com/ » —
le 17-D est mort de l'amont, pas du code). Chaque geste était une leçon
devenu réflexe ; le 29/10, il a demandé l'automatisation. Le prévol
naît de ces trois leçons exactement :

1. **AVANT l'extraction, pas après** — un proxy.exe orphelin n'attend pas
   gentiment : il VERROUILLE le fichier proxy.exe que sup-37 doit re-poser
   (CreateFileA en écriture refusé sur un exe en cours) ET il tient le
   port 25000. Tuer après, c'est tuer trop tard. L'ordre
   taskkill → curl → extraction est un invariant (I5 sup-39).
2. **Codes bruts, jamais un juge** — le 17-D nous a appris à lire un code
   de sortie comme un fait (« S47 exit proxy=0 », témoin 502). Le prévol
   applique la même grammaire : S08/S09 portent N SANS interprétation
   in-code (0/128 côté taskkill ; 0/6/7/28 côté curl — la lecture vit au
   LISEZMOI, un journal d'événements rapporte, il ne commente pas). Le
   réseau coupé n'est pas un échec du superviseur : c'est un FAIT du run,
   désormais consigné AVANT que les tests ne le subissent.
3. **Sous une couverture existante** — la table R10 est PLEINE depuis
   terrain.17 (28 entrées, 464 o touchant l'ancre : « tout futur bloc
   exige une autre surface que .text2/table »). Le prévol ne force aucune
   case : il vit en queue de zone données sup 1 (0x4B40-0x4BFF, dans
   l'ancien 0xCC de remplissage), couvert par l'entrée DE ZONE — la porte
   reste juge par la somme, et l'oracle le PROUVE : la 29e cible de
   falsification (octets 11/23 du bloc) est détectée via la somme de
   zone. PE 75 264 o : TAILLE INCHANGÉE, six générations de suite.

Le verrou d'échec (l) mérite son nom : taskkill ABSENT (politique
machine) + amont COUPÉ (curl 28) → S08 sautée sans crash, S09 code=28
BRUTE au journal, verdict final = 1 (les sondes ne comptent jamais) —
c'est le miroir exact du run 17-D, joué en émulation AVANT la machine.
La mutation M10 (ligne S08 amputée d'un caractère) est rejetée par le
journal d'or : l'évidence de prévol est une preuve gardée, comme S47
avant elle.

Cosmétique soldée au passage : le tableau de bord affichait l'u64 de
terrain.4 depuis quatre générations (bug d'affichage — la carte portait
toujours la bonne version) ; corrigé vers TERRAIN7.

Aucune clé touchée (phrase D81 valable, conteneur 0323029a… inchangé).

### D102 — M4 / terrain.17-G : LE TÉMOIN A PARLÉ, L'ANOMALIE DES 13 OCTETS EST MORTE — tls-07:R2 scan PAR TYPE (le témoin du run 17-F a livré la preuve byte-level : les 13 octets `17 03 03 03 B3 | 00…01` ne sont PAS du texte tronqué, c'est l'EN-TÊTE D'ENREGISTREMENT TLS BRUT + le nonce GCM du premier record — Schannel RÉELLE, en sortie de son SEC_E_OK, RECLASSE les QUATRE tampons PAR TYPE : [0]=STREAM_HEADER (13 o en GCM : 5 en-tête + 8 nonce), [1]=DATA (LE clair, pv = zone + en-tête), [2]=STREAM_TRAILER, [3]=EXTRA ou EMPTY — msdn « Extra Buffers Returned by Schannel » : l'EXTRA peut être rendu « seul, à une position quelconque » ; l'exemple canonique msdn « Decrypting a Message » scanne i < 4 par BufferType, le PREMIER DATA gagne) ; l'ancienne tls-07 lisait le clair au tampon 0 et le résidu au tampon 1 — positions fixes : sur machine réelle le tampon 0 était le STREAM_HEADER, le client recevait l'EN-TÊTE CHIFFRÉ, jamais le clair — l'anomalie 17-C/17-F est ÉTEINTE ; POURQUOI L'ÉMULATION RESTAIT VERTE : le shim et le modèle partageaient la MÊME lecture positionnelle — d'accord entre eux, faux contre l'API réelle (msdn sourcé) ; CORRECTIF tls-07:R2 ÉCRITE-AVANT-CODE (I révisée) : le span EST le PREMIER tampon reclassé SECBUFFER_DATA, le résidu EST le SECBUFFER_EXTRA — où que la bibliothèque les pose (I6 : la POSITION n'est JAMAIS une hypothèse, seuls les TYPES parlent) ; E4 NEUF : SEC_E_OK sans aucun DATA → verdict 6 fail-closed, span INTACT (jamais un mot forgé), région consignée (0, lot) — miroir Q4 ; Q3 lit l'EXTRA PAR TYPE (l'ancienne lecture positionnelle tombait sur le DATA reclassé) ; tls-08 INTACT OCTET POUR OCTET : il pompe le span, où qu'il pointe — sa conception ; SHIMS REJOUÉS AU RECLASSEMENT RÉEL (harnais_reception + harnais_session : [0]=H, [1]=D, [2]=T, [3]=E-ou-EMPTY + dispositions optionnelles {H,D,T,E,X} par entrée de script) ; CHAÎNE VERTE : harnais tls-07 40 PASS (round-trip 116/116 — code 394→527 o dans le slot 768, TAILLE inchangée ; 20 scénarios dont l'EXTRA en [0], DATA en [3], close_notify EXTRA déplacé, E4 ; 4 000 appels + 1 000 chaînes avec permutations aléatoires ZÉRO écart ; 12 mutations dont M5/M7/M7b/M11 ciblent le scan, témoin intact 20/20), harnais session 53 PASS, oracle M4 560 cas verts + falsification, proxy.exe RECONSTRUIT 28 160 o TAILLE INCHANGÉE (le correctif vit dans le padding du slot — 7e contrainte de taille tenue), sha256 b9264e0b6aef460f86c54ec0c4d38ebe90ca58b841fec7a09257e813ff6545cf, md5 2b6481a1…, carte génération 6 re-scellée (Ed25519, R8 OK), cristallisation 2/2 byte-stable ; TERRAIN.18/17-G : kit embarquant le proxy D102 (layout MD5_PROXY_HEXA/SHA256 mis à jour, assertés au build), version terrain.8 (u64 0x00050108, .rsrc 0.5.0.8/terrain.8 — le bug cosmétique D101 corrigé d'emblée), oracle terrain 10 124 cas verts, falsification 29/29 + 10 mutations, carte lignée re-scellée (25 empreintes), PE 75 264 o TAILLE INCHANGÉE (SEPT générations), sha256 ee23cc80e1aff6ab70babf90be35716c88e8755ba8e22b88ab9e838f3f636ec5, md5 dc874126…, différentiel 17-F → 17-G : 295 octets en 10 plages TOUTES NOMMÉES (sommes R10, version u64, chaîne md5 kit S05C, champs .rsrc + manifeste, somme .rdata, octets du kit — le scan `4c 8b 9c 24 98…` visible dans le .blob ; monotonie : RIEN d'autre ne bouge) ; LIVRAISON : download/superviseur-terrain17g.exe + LISEZMOI-terrain17g.txt (la PREUVE du bon binaire : S05C md5 proxy 2b6481a1… — l'ancien affichait 33c91815…) — POUSSÉS dans /test du Drive (md5 MATCH vérifié — le canal OAuth relais RESSUSCITÉ le 29/10 : échange authorization_code après consentement développeur, refresh_token neuf déposé dans .gdrive + copie Tokens du Drive restaurée [le PATCH+multipart maison mettait le fichier en corbeille — remplacé par le chemin résumable éprouvé, scripts/oauth_echange.py]) ; le 17-F local archivé en référence (scripts/superviseur-terrain17f_ref.exe, mono-génération D69) ; le 17-F exe du /test (dépôt développeur) non mis à la corbeille (403 : fichier possédé par le développeur — ses droits priment) ; CANON OAuth : le jeton relais meurt en 7 jours (mode Testing Google Cloud — l'ancien est né le 22/10, mort le 29/10) → le partage Éditeur du dossier test au compte de service z-ai-811@physichong.iam.gserviceaccount.com reste la parade DÉFINITIVE (action développeur, une seule fois) ; LEÇON SYSTÉMIQUE CONSIGNÉE : un modèle et son émulation ne prouvent rien contre l'API réelle s'ils partagent la même erreur — la divergente doit être NOMMÉE par l'évidence (le témoin byte-level) AVANT d'être corrigée, et le correctif se CHERCHE dans la documentation de l'API cible, pas dans le code : « d'accord entre eux, faux contre le monde » est le mode de défaillance des couples modèle/shim.

### D103 — terrain.19 / 17-H : LE DOUBLON EST MORT — le superviseur cherchait la fenêtre démo par son TITRE, la reconstruction terrain.17 avait ressuscité le bug de terrain.5 (le constat développeur du 29/10 10:50 : « toujours le problème de la fenêtre qui s'ouvre en doublon après avoir lancé "tout démarrer" — règle ça en priorité sinon le test n'est pas fiable » — PRIORITÉ INVERSÉE assumée : le T1 menteur invalide la lecture de TOUT le journal) ; L'ÉVIDENCE DES RUNS 17-G (rapatriés par le compte de service, md5 MATCH) : les DEUX journaux complets (10:41:49 + 10:45:00, séquentiels) disent « S11 T1 fenetre demo ABSENTE » alors que demo_journal.txt (150 o, DÉPÔT NEUF demandé par le LISEZMOI) porte CINQ lignes vivantes dont « L01 fenetre principale creee » — la fenêtre EXISTAIT à l'écran pendant que le superviseur la déclarait absente, jamais cliquée, tuée après 10 s : la définition exacte du « doublon » perçu (une coquille jumelle orpheline qui s'ouvre, ne fait rien, et meurt) ; ET PARALLÈLEMENT : S05C md5 proxy 2b6481a1 ✓ (le kit D102 en place) + LE TÉMOIN « HTTP/1.1 502 Passerelle inaccessible » — du HTTP EN CLAIR chez le client : D102 EST PROUVÉ SUR MACHINE RÉELLE (l'anomalie des 13 octets est bien morte : le tunnel déchiffre et parle HTTP au client ; le 502 est la voix honnête du proxy — l'amont example.com était injoignable PENDANT le run, S49 KO console NON conforme, S47 exit=0 : chemin propre dégradé) ; LA RACINE (notation ligne 31-32 + binaire 17-G offset fichier 0x424f) : FindWindowW porte rcx=NULL (lpClassName) et rdx=« TRIADE_demo » (lpWindowName) — RECHERCHE PAR TITRE : or demo.exe crée CLASSE « TRIADE_demo » (@rva 0x2a92) et TITRE « TRIADE M2 — démonstration complète » : AUCUNE fenêtre ne porte le titre cherché → NULL 200 sondes durant 10 s ; le défaut est le BUG ORIGINEL de terrain.5, corrigé en terrain.6 PAR PATCH BINAIRE DIRECT (9 octets, jamais reporté à la notation/spec) — la RECONSTRUCTION terrain.17 l'a RESSUSCITÉ : S11 detectee en terrain.14 (28/10, patch vivant) puis ABSENTE sur les 7 runs 17-C→17-G (corrélation parfaite, preuve par le journal) ; L'ORACLE ÉTAIT COMPLICE (leçon D102 répliquée au niveau user32) : le shim FindWindowW lisait la chaîne en rdx et rendait TOUJOURS FAKE_HWND_DEMO — le code faux passait l'émulation, NULL à jamais sur la vraie machine : « d'accord entre eux, faux contre le monde » ; CORRECTIF sup-33:R2 ÉCRITE-AVANT-CODE : Q2 réécrite au contrat Win32 (« TRIADE_demo », NULL) — la CLASSE en rcx, NULL en rdx ; notation brouillon échangée (lea rcx, [rip+CLASSE_DEMO] / xor edx,edx — 9 octets, MÊME TAILLE : 31 C9 48 8D 15 disp → 48 8D 0D disp+2 31 D2, même cible 0x2a92, le call [rip] IAT intact) ; régénérée 940 o / 229 instructions SANS CHANGEMENT DE TAILLE (le correctif vit dans les octets existants du slot f60033) ; auteur.py BLOCS + layout BLOCS_TERRAIN « sup-33:R2 »/« terrain.19 » + I/README ; ORACLE AU CONTRAT RÉEL : le shim rend un handle SI ET SEULEMENT SI la classe cherchée (rcx) est « TRIADE_demo » — une recherche par titre rend 0 pour toujours, exactement la vraie machine ; VERROU D103 (deux variantes du scénario nominal) : exactement 3 appels par run, tous (« TRIADE_demo », « ») — la fenêtre est trouvée au 3e sondage, jamais par le titre ; FALSIFICATION M11 (la 11e) : le bug 17-G rejoué octet par octet sur le binaire construit (motif lea rcx+xor edx+call → 31 C9 + lea rdx disp-2) → S11B ABSENTE, clic jamais envoyé, T1 KO, premier appel (« », « TRIADE_demo ») — la régression ne peut plus JAMAIS repasser verte en silence (incident de correction : la première insertion de M11 avalait le total+=1 de M10 — restauré, comptes audités par exécution isolée : 40 = 29 + 11) ; CHAÎNE VERTE : oracle terrain 10 127 cas verts (+3 : deux verrous D103 + M11), falsification 29/29 cibles R10 + 11 mutations ciblées, 1 158 verrous structurels, round-trip notation 100 % (25 blocs), croisé T4 10 fixtures, carte lignée re-scellée (Ed25519, R8 OK, 25 empreintes), PE 75 264 o TAILLE INCHANGÉE (HUIT générations consécutives), sha256 f947b605486b8d8d71d1906e1dba51fca614dadb13a73df5a39ff9b0db91b6f9, md5 ab8afc77d9d50abefd4e42130f8236f1, version terrain.9 (u64 0x00050109, .rsrc 0.5.0.9/terrain.9) ; kit INTACT (demo 73c064fb… + proxy D102 2b6481a1… — vérifiés par le découpage oracle du .blob) ; DIFFÉRENTIEL 17-G → 17-H : 23 octets en 8 plages TOUTES NOMMÉES (9 o le correctif à rva 0x544f = .boucle_fen EXACTEMENT là où vivait le bug ; 1 o R_VERSION 0x50108→0x50109 ; 8 o sommes R10 ; 5×1 o champs version .rsrc+manifeste) — .blob INTACT octet par octet (45 056 o), monotonie vérifiée ; LIVRAISON : download/superviseur-terrain17h.exe + LISEZMOI-terrain17h.txt (la PREUVE comportementale du nouveau binaire : S11 « detectee » + S12 « clic TOUT DEMARRER envoye » — deux lignes IMPOSSIBLES pour 17-G ; NOUVEAU dépôt demandé : demo_journal.txt AUSSI — la donnée D57 enfin complète : le journal démo APRÈS le clic) ; 17-G archivé en référence locale (scripts/superviseur-terrain17g_ref.exe) ; ATTENTE 17-H : T1 atteindra ENFIN son point de panne D57 réel (S13 termine code=3221225477 attendu — échange réseau démo en échec, panne scellée M2 documentée, honnête) ; T2/T4 restent les juges M4 (S49 OK + témoin « HTTP/1.1 200 » → scellage 0.5.0 ; S49 KO + 502 → amont coupé, réessayer réseau vivant — D102 déjà prouvé par le témoin clair) ; LEÇON CONSIGNÉE : un correctif binaire qui ne vit pas dans la source ne survit pas à une reconstruction — terrain.6 a patché l'octet, terrain.17 a régénéré le mensonge ; la source (notation + spec + oracle) est le seul lieu de vérité, et l'oracle doit modéliser le CONTRAT de l'API (jamais le comportement du code qu'il teste).

### D104 — M4 SCELLÉ à la balise finale 0.5.0 : LE RUN 17-H A LIVRÉ LE JUGEMENT ET LE TÉMOIN ENSEMBLE (terrain_20261029_115002.txt, rapatrié du /test avec le dépôt du superviseur lui-même — md5 ab8afc77… == la livraison D103 : la preuve d'identité du run ; S05C md5 proxy 2b6481a1 ✓, le kit D102 octet pour octet) ; LE DOUBLON EST MORT SUR MACHINE RÉELLE (« S11 T1 fenetre demo detectee » + « S12 T1 clic TOUT DEMARRER envoye » — deux lignes impossibles pour 17-G — et demo_journal.txt 14 lignes : la fenêtre démo a vécu sa vie de test PILOTÉE, la réparation du constat développeur prioritaire est prouvée, le test est redevenu fiable) ; T1 KO HONNÊTE EXACTEMENT PRÉVU (D57 : « réseau : échange en échec », S13 code=3221225477 = 0xC0000005 — la panne scellée M2, l'intervalle exact EN MAIN pour la première fois : après L03, à l'échange, en sortie de scénario) ; T2 OK (HTTP 640/HTTPS 577) ; **T4 S49 VERDICT OK (console conforme) + LE TÉMOIN « HTTP/1.1 200 OK »** (example.com 640 o EN CLAIR livré au client PowerShell par le tunnel — Date 29 Oct 10:50:47 GMT, PENDANT le run ; « tunnel chiffre etabli », badssl « certificat rejete » 34 o exacts, S47 exit=0 : compensation intégrale) — S91 ECHEC ne vient QUE de T1/D57, T2/T4 les juges M4 sont VERTS ENSEMBLE pour la première fois avec le témoin 200 ; SCELLAGE 0.5.0 (modèle 0.4.0/D74 : « l'artefact n'est PAS touché, le scellage est un fait de carte ») : (1) conformité § 8.2 ÉCRITE POUR M4 — m4/conformite_profil.py, 44 contrôles, éléments 1-7 constatés depuis l'artefact scellé (COFF/PE32+, INT 10+13+7, hints séquentiels ; les SEPT appels secur32 visités par call [rip], zéro hors plages IAT, ombres ABI posées ; DEP/NX+ASLR+HEV actifs, CFG rapporté ; table HRESULTS 13 + VERDICT_FATAL 6 ; porte R10 VIVANTE — 28 entrées, somme .text3 déclarée == recalculée, R_VERSION 0x00050002 ≥ plancher ; round-trip 12 M4 + 27 héritage octet-identiques + scellé M3 présent ; 28 160 o, tls-07:R2 527 o dans slot 768) + contrôle de jalon oracle différentiel (sentinelle, miroir fuzzing M3) — TROIS LEÇONS DE CONSTAT : l'empan d'une section est SA taille réelle (un span large fait mentir le mapping), les entrées hints/names se serrent SANS padding (un hint sur adresse IMPAIRE), la mesure d'un code compte le padding DEPUIS LA QUEUE (un 0x90 isolé peut vivre dans un disp32) ; (2) CRISTALLISATION PORTÉE À 10/10 (verifier graines 20261029-37 : M3 524 + M4 482 verrous, oracle 560 cas, R8 49 empreintes à chaque passage — 49 blocs à 10/10) ; (3) _sceller/--sceller-rc/--sceller-final portés à build_m4.py + VERSION_RC1/VERSION_FINALE au layout (la balise u64 de l'artefact RESTE 0x00050002 — R7, les octets prouvés terrain ne bougent pas) ; (4) CÉRÉMONIE : 0.5.0-rc.1 (cristallisation + conformité + critères du jalon — HTTPS via Schannel et échec propre sur certificat invalide, prouvés 17-C→17-H) puis **0.5.0 FINALE** (validation terrain consignée : T4 17-H — S49 OK + témoin HTTP/1.1 200 + S05C 2b6481a1, octets inchangés), frag-bld basculé exactement une occurrence (fail-closed), fragments re-chiffrés, carte re-signée Ed25519 ; (5) POST-SCELLAGE : anti-rollback ARMÉ (« carte scellée (0.5.0) : reconstruction interdite » — testé), R8 indépendant 49 empreintes artefact 0.5.0, tableau de bord version=0.5.0, proxy.exe INTACT md5 2b6481a1… sha256 b9264e0b… 28 160 o — la chaîne terrain complète : 17-C (critère câblé) → 17-D (S47=0, témoin 502) → 17-E (fuite I2 morte) → 17-F (prévol) → 17-G (D102 prouvé en clair) → 17-H (juge et témoin verts ENSEMBLE) ; M4 CLOS (§ 16) — balise immuable § 9, défaut → 0.5.1 à contrat stable (R4) ; SUITE : v0.6.0 axes 2-3 (CF2-Shamir, sceau I) selon D86/D87, D57 avec l'intervalle exact en main (M2 scellé — 0.3.x à contrat stable si ouvert), partage Éditeur /test au compte de service toujours attendu (refresh OAuth ~05/11).

### D105 — v0.6.0 axe 3 : LE SCEAU DE L'INTENTION VIT (D87 instancié — spec écrite-avant-code, cérémonie hors-ligne autoportière, dix arbres signés, gardes de build armées, falsifiabilité 47/47 ; la clé RÉELLE attend la cérémonie du développeur, l'état « test » est VISIBLE)

**Décision** : la souveraineté cryptographique de l'intention (D87) quitte la
feuille de route et entre dans le dépôt. Dix arbres d'intention (les neuf
lignées `m0/I` … `terrain/I` PLUS `v06/I` — l'arbre de l'axe lui-même : la
spécification qui définit le sceau est la première couche I qu'il garde, un
mécanisme de garde qui s'exempte de lui-même serait une contrebande X2) sont
condensés en manifestes canoniques ordonnés et signés Ed25519 ; la chaîne de
build M4 et la chaîne terrain REFUSENT tout arbre divergé de sa signature
(fail-closed, fichier fautif NOMMÉ). Voler le binaire, le dépôt, et même les
clés du poste ne permet plus de faire ÉVOLUER l'intention : seul le
développeur, clé hors-ligne en main, le peut — quand il aura exécuté la
cérémonie.

**La spécification (v06/I/README.md, R2 écrite-avant-code, 220 lignes)** :
manifeste canonique (en-tête `TRIADE-SCEAU-I v1`, arbre/artefact/balise/
décompte, une ligne `sha256:<hex>  <chemin>` par fichier régulier, tri
lexicographique POSIX INDÉPENDANT du système, LF, UTF-8 — répertoires vides,
liens symboliques et fichiers spéciaux REFUSÉS : un arbre d'intention n'est
pas un espace arbitraire) ; l'EMPREINTE d'arbre = SHA-256 du texte du
manifeste ENTIER (l'en-tête compris — aucun champ hors signature) ; la
signature Ed25519 (RFC 8032, D4 auto-porté) couvre le message de 32 octets
— la charge utile de cérémonie est IMPRIMABLE SUR PAPIER (`a-signer.txt`,
dix lignes) ; le dépôt porte la preuve (`v06/sceau-I/` : clé publique,
manifestes, signatures par arbre, état de clé) ; codes de sortie nommés
(0 vert / 10 arbre divergé / 11 signature invalide / 12 dépôt incohérent) ;
la garde n'est PAS la défense contre la réécriture intégrale du dépôt
(trois gardes, trois menaces — D87 : cette menace appartient à la phrase de
lignée et au git signé).

**La cérémonie hors-ligne (v06/ceremonie_hors_ligne.py, 427 lignes,
AUTOPORTEUR)** : Python 3.8+ STANDARD SEUL — aucun pip, aucun réseau, aucun
dépôt ; copiable seul sur machine hors ligne (une copie vivra dans
download/). Ed25519 en Python pur (arithmétique entière, RFC 8032 § 5.1) ;
AUTOTEST fail-closed à chaque `generer`/`signer` : les vecteurs RFC 8032
§ 7.1 TEST 1-3 (clé + signature déterministe + vérification + mutation
rejetée) doivent passer AVANT toute production — une cérémonie dont la
cryptographie est cassée n'écrit rien. Trois modes : `generer` (graine
os.urandom 32 o → `cle-I-privee.txt` 0600 avec mode d'emploi de garde
papier, `cle-publique-I.txt` ; la graine ne s'affiche JAMAIS — le fichier
EST la remise), `signer` (chaque signature auto-vérifiée avant écriture),
`verifier` (audit autonome d'une remise). **Les vecteurs furent vérifiés à
la SOURCE (discipline D79)** : la mémoire du modèle se trompait sur la
graine du TEST 2 (faute détectée par dérivation graine→clé contre le témoin
`cryptography`), les vraies valeurs furent rapportées de sources RFC
concordantes (rfc-editor, datatracker, miroirs) puis AUTHENTIFIÉES contre
l'implémentation auditée `cryptography` (pk + signature déterministe
identiques) — le témoin byte-level est la SPÉCIFICATION, pas la mémoire :
la leçon D102 (« d'accord entre eux, faux contre le monde ») retournée en
méthode de preuve.

**L'outil du dépôt (v06/sceau_I.py, 470 lignes)** : `preparer` (manifestes
vivants → `a-signer.txt`, arbres divergés RAPPORTÉS — le signal
« l'intention a évolué, signature requise »), `deposer` (rotation : chaque
signature vérifiée AVANT toute écriture — ATOMICITÉ INTÉGRALE, corrigée en
cours de route : la clé de cérémonie ne s'installe qu'en phase d'écriture,
un échec laisse le dépôt INTACT, jamais une clé neuve au-dessus de
signatures mortes), `signer-test`, `verifier` (la gardienne), `etat`
(audit). Vérification côté dépôt : `cryptography` (dépendance existante).

**La phase LABORATOIRE, honnête (spec § 8, défaut X8 sinon)** : tant que le
développeur n'exécute pas la cérémonie réelle, le dépôt porte des
signatures de clé de TEST DÉRIVÉE D'UNE CONSTANTE PUBLIQUE (une clé de test
n'est un secret pour personne — sa non-sécurité est CONSIGNÉE et visible,
et l'état survit à toute réinitialisation du bac à sable) ; l'étiquette
`test` vit dans `etat-cle.txt`, répétée par chaque garde et chaque
`verifier`. La MÉCANIQUE est prouvée ; la SOUVERAINETÉ s'arme à la
cérémonie réelle (remplacement = une rotation § 5).

**La falsifiabilité (v06/test_sceau_I.py — 47 PASS / 0 ÉCHEC)** : T1
vecteurs RFC 8032 (TEST 1-3 + signature de zéros + un octet de message +
un octet de signature mutés rejetés) ; T2 interop BIDIRECTIONNELLE
pure-Python ↔ cryptography ×20 messages seedés (clés publiques identiques,
signatures déterministes IDENTIQUES, vérifications croisées des deux sens —
deux implémentations indépendantes + le témoin RFC) ; T3 déterminisme du
manifeste (double calcul, mtime changé → manifeste inchangé, tri canon) ;
F1 LA CÉRÉMONIE COMPLÈTE jouée en réplique isolée par SOUS-PROCESSUS
(generer → signer → verifier « TOUT VERT » → deposer --cle → état
« reelle » → dépôt de réplique vert : le flux air-gap exact du
développeur) ; F2 falsification D'UN OCTET par arbre 10/10 (rejet +
fichier NOMMÉ — l'évidence, pas un verdict muet) ; F3 diffs non signés
refusés par la GARDE DE BUILD (ajout → 10 « ajoute », suppression → 10
« supprime », l'ATTAQUANT RÉÉCRIT LE MANIFESTE pour suivre l'arbre muté →
la SIGNATURE le dénonce : 11, signature supprimée → 12, lien symbolique et
répertoire vide → refus structurel, garde() lève l'exception nommée, garde
verte après restauration : zéro rémanence) ; F4 remise douteuse SANS ÉCRIRE
(mauvaise signature / remise incomplète / balise divergente → refus nommé,
dépôt INTACT octet pour octet — l'atomicité est prouvée par empreinte
globale avant/après) ; T4 clé de test déterministe, clé déposée == clé de
test, état « test » JAMAIS confondu avec « reelle ». FAUTES DU HARNAIS
nommées avant le vert (dictionnaire de divergence inversé condensé↔chemin —
« fichier supprimé : \<hash\> » au lieu du nom ; collision de mots entre
l'étiquette de phase test et le test T4-c) : aucune dans le sceau.

**Les gardes de build (spec § 7, intégrées aux TROIS chemins d'entrée :
construire / verifier / sceller)** : `m4/build_m4.py` garde
`[m0, m1, m2, m3, m4]` (hello-02 M0 + libc M1 + tcp M2/M3 + http/tls
M3/M4 — les arbres que la chaîne ASSEMBLE) ; `terrain/build_terrain.py`
garde `[m0, m1, m2, demo, terrain]` (les héritages R7 + les blocs sup-* ;
le proxy M4 embarqué est un BINAIRE scellé gardé par sa propre chaîne —
carte R8 + md5 S05C du kit). PREUVE END-TO-END : un octet muté dans
`m4/I/tls-02-verdicts.md` → `build_m4.py --verifier` REFUSE EN TÊTE (exit
1, « arbre m4 REFUSE (code 10) — fichier modifie : tls-02-verdicts.md ;
diff d'intention non signe : la cle hors-ligne du developpeur est requise
(D87, spec § 7) », AVANT tout assemblage) ; restauration → vert. AUCUNE
RÉGRESSION : M4 verifier EXIT=0 (garde + 524 verrous M3 + 482 verrous M4 +
38/38 + oracle vert + cristallisation 10/10 + R8 49 empreintes, artefact
0.5.0 INTACT md5 2b6481a1… sha256 b9264e0b… 28 160 o) ; terrain verifier
EXIT=0 (garde + 1 158 verrous + 10 127 cas verts + R8 25 empreintes,
superviseur 17-H INTACT sha256 f947b605… 75 264 o — le scellage 0.5.0 et la
balise terrain.19 ne bougent pas : la garde LIT, elle ne construit pas).

**Critères de sortie D87** : (1) cérémonie hors-ligne documentée exécutable
sans l'assistant — `v06/ceremonie_hors_ligne.py` + `download/LISEZMOI-cle-I.txt`
(flux pas à pas) ✓ ; (2) le dépôt vérifie la signature I de tous les jalons
scellés — `verifier` : 10 arbres, gardes dans les deux chaînes ✓ ; (3)
falsification d'un octet rejetée — F2 10/10 + preuve end-to-end du build ✓ ;
(4) diff non signé refusé par le chemin de patch — F3 + la garde refuse le
BUILD réel (exit 1 nommé) ✓ — la souveraineté effective s'arme à la
cérémonie réelle du développeur (remplacement de la clé de test par
rotation, l'état « test » le dit tant qu'il n'est pas fait).

**Environnement consigné** : le bac à sable avait perdu ses dépendances de
build (capstone, keystone-engine, pefile, pynacl, unicorn réinstallés) —
aucun impact dépôt, les chaînes repassées vertes après réinstallation.

Aucune clé touchée : RIEN à remettre par cérémonie (phrase de contrôle D81
valable, conteneur 0323029a… inchangé, sentinelles intactes — proxy 0.4.0
dd12b649…, demo 73c064fb…, hello, selftest, echo ; le superviseur du dépôt
reste la balise terrain.17-H f947b605…, le proxy M4 la balise FINALE 0.5.0 ;
la clé de test du sceau I dérive d'une constante PUBLIQUE, la clé réelle
naîtra hors ligne et n'entrera jamais ici). SUITE : v0.6.0 axe 2 (CF2-Shamir
D86, sentinelle et fragments) ; cérémonie réelle du développeur (LISEZMOI
livré) ; D57 (intervalle exact en main, correction 0.3.x si ouverte) ;
partage Éditeur /test au compte de service (refresh OAuth ~05/11).

### D106 — v0.6.0 axe 2 : L'INTERRUPTEUR D'HOMME MORT VIT (D86 instancié — spec écrite-avant-code v06/I/CF2/README.md, coffre CF2 à clé maîtresse jamais stockée entière, Shamir sur générateur PRIMITIF, sentinelle inotify + attribution /proc à double seuil, destruction trois passes + PV, falsifiabilité 43/43 ; le coffre RÉEL attend la cérémonie de migration du développeur)

**Décision** : la seconde moitié de la souveraineté cryptographique quitte la
feuille de route et entre dans le dépôt. Le conteneur **TRIADE-CF2** chiffre
la base du coffre (même schéma JSON que CF1) sous une clé maîtresse M de 32
octets **jamais stockée entière** — découpée par Shamir en N fragments (5 par
défaut, seuil 3) logés dans des gardes distinctes ; le déverrouillage
reconstitue M en RAM puis l'efface. La **sentinelle** surveille la couche C :
lecture de contenu par un processus hors liste blanche → destruction
immédiate des fragments présents (trois passes d'écrasement, fsync par passe,
troncature, renommage, unlink, fsync du répertoire — PROCÈS-VERBAL nommé :
pid, image, ligne de commande, fichier lu). Sous le seuil, Shamir est
informationnellement sûr : le coffre devient indéchiffrable, pas seulement
« révoqué » — le code volé pendant que la machine vit perd le coffre dans le
même mouvement. La relève exige **T copies hors-ligne** (trois à seuil 3 :
deux copies laissent le coffre mort — l'autotest le prouve par restauration
partielle refusée, puis acceptée à la troisième).

**La spécification (v06/I/CF2/README.md, R2 écrite-avant-code, 13 sections)** :
GF(2^8) polynomial 0x11B, évaluation de Horner, interpolation de Lagrange en
x=0, coefficients FRAIS du CSPRNG pour CHACUN des 32 octets ; bornes
2 ≤ T ≤ N ≤ 255, T=1 refusé (une seule garde = l'alternative rejetée par
D86) ; conteneur miroir de CF1 (§ 11.2) avec contexte HKDF distinct
(`coffre=v2`) et champ **verif** 16 o qui NOMME la clé fausse avant l'AEAD ;
fragment ASCII transportable sur papier, lié au **SEL du coffre** ; gardes
répertoires distincts 0700 ; sentinelle à double seuil (processus hors liste
blanche ET lecture de contenu — un stat ou un listage n'ouvre pas de
descripteur : PAS un signal ; une lecture non attribuée est journalée, PAS
brûlée) ; liste blanche MINIMALE sur l'image résolue ET la ligne de commande
complète (jamais « tout python3 ») ; heart-beat de santé ; moteur Windows
SACL/4663 consigné (même posture que D85) ; bornes honnêtes écrites
(sentinelle tuable, fenêtre d'attribution ~10 ms, zéroïsation au mieux de
Python, CoW).

**Trois fautes nommées par les preuves elles-mêmes (la méthode D102
retournée en discipline de développement)** : (1) **le générateur de tables
GF(256)** — 0x02 n'est PAS primitif modulo 0x11B (ordre 51 : 204 éléments
sans logarithme), l'arithmétique silencieusement fausse passait les tests de
coin (les erreurs COÏNCIDAIENT) : corrigé sur le générateur primitif 0x03,
prouvé par EXHAUSTIVITÉ (65536 cas de distributivité + 255 inverses) — et la
suite croise Shamir contre un témoin INDÉPENDANT (évaluation en somme de
puissances et multiplication GF bit-à-bit, reconstitution par élimination de
Gauss : trois algorithmes, zéro table partagée) ; (2) **la liaison fragment →
empreinte d'en-tête** — le parcours CLI complet (écrire puis relire) l'a
dénoncée : le nonce est frais à CHAQUE écriture, l'en-tête change, toutes les
fragments deviendraient « d'un autre coffre » à chaque `ajouter` — et les
copies PAPIER mourraient à la première écriture : corrigé sur le SEL du
coffre (stable par construction) ; (3) **la relève à 2 copies** — l'autotest
a dénoncé l'impossibilité sous le seuil 3 : la cérémonie exige T copies
hors-ligne, la spec le consigne et la suite PROUVE la sémantique (2 copies →
mort persistante, 3ᵉ → vie).

**L'outil (v06/coffre_cf2.py)** : `init`/`migrer` (CF1 → CF2 : la base est
re-chiffrée sous M, CF1 RESTE INTACT — sa destruction est un acte explicite
après vérification), `statut`, `etat-fragments` (verdict VIVANT/MORT),
`lister`/`obtenir`/`ajouter`/`retirer` (M reconstitué en RAM à CHAQUE
opération puis effacé — jamais écrit entier), `verifier`, `restaurer`
(remise ATOMIQUE : tout valider avant d'écrire, motif D105 [11]),
`bruler --oui-je-comprends`, `autotest` (13 contrôles, répertoires
temporaires — le coffre réel n'est JAMAIS touché).

**La sentinelle (v06/sentinelle_cf2.py)** : moteur de laboratoire Linux non
privilégié — l'utilisateur du bac à sable n'a pas CAP_SYS_ADMIN
(`fanotify_init` rend EPERM : CONSIGNÉ) — inotify par ctypes (autoporté,
`IN_OPEN|IN_ACCESS` sur fichiers, `IN_ISDIR` ignoré : le listage n'est pas
une lecture de contenu) déclenche un balayage /proc IMMÉDIAT (la latence ne
dépend pas de la période), balayage périodique en secours ; attribution par
`/proc/<pid>/fd` + exe + cmdline ; anti-bruit (une ligne par pid-fichier) ;
journal partagé outil/sentinelle SANS secret. **Latence mesurée :
0,05 s de l'ouverture hostile aux gardes vides (borne consignée 2 s).**

**Falsifiabilité 43/43 (v06/test_cf2.py)** : T1 Shamir contre témoin
indépendant (KAT somme de puissances + corps bit-à-bit, 1 000 secrets × les
DIX combinaisons C(5,3), Gauss ×50, refus des bornes) ; T2 sécurité
INFORMATIONNELLE démontrée (deux M′ arbitraires rendus compatibles avec
T−1 fragments réels par un troisième forgé : la réconstitution rend M′ sans
erreur — aucune discrimination n'est possible, c'est verif qui nomme le
mensonge) ; T3 fail-closed nommé (verif, AEAD, liste blanche d'algorithmes,
troncature, magic ; un fragment fautif ÉCARTÉ sans entâcher les quatre
autres, trois fautifs → refus) ; T4 fausses alertes NULLES (lecteur blanchi
— MÊME binaire que l'attaquant, seule la ligne de commande distingue — 1,5 s
de lecture : rien ne brûle ; attributs seuls : aucun signal) ; F1
EXFILTRATION SIMULÉE (critère D86 complet : PV nommé, 5 fragments détruits,
coffre MORT refusé nommément, latence bornée, relève par T copies → vie) ;
F2 remise douteuse sans écrire (lot corrompu, indice déjà présent, fragment
d'un autre coffre — gardes INTACTES octet pour octet) ; T5 santé (heart-beat
frais en vie, MORT visible après décès) ; X8 coffres réels intacts (md5 de
`.keys/coffre_fort.bin` inchangé, aucun `.keys/coffre_cf2.bin` créé).

**Non-régression** : oracle M4 560 cas verts + build verifier EXIT=0 (38/38,
524+482 verrous, cristallisation 10/10, R8 49) ; oracle terrain 10 127 cas +
verifier EXIT=0 (1 158 verrous, R8 25) ; sceau-I 10 arbres VERTS (l'arbre
v06/I porte désormais les axes 2-3 : `v06/I/CF2/README.md` re-signé en phase
test, balise `v0.6.0-axes2-3`) + test_sceau_I 47/47 ; artefacts INTACTS
(proxy 0.5.0 `2b6481a1…`/`b9264e0b…` 28 160 o ; superviseur 17-H
`f947b605…` 75 264 o).

**Phase laboratoire / cérémonie réelle** : la mécanique est COMPLÈTE et
prouvée, le coffre réel du développeur N'A PAS MIGRÉ (aucune clé touchée,
discipline D105). L'acte qui arme l'interrupteur : `migrer` (phrase de
contrôle CF1) + TROIS copies hors-ligne + liste blanche de l'éditeur +
`sentinelle demarrer` — le flux pas à pas vit dans
`download/LISEZMOI-coffre-CF2.txt` (bornes honnêtes comprises : la fausse
alerte est une perte auto-infligée, la liste blanche est minimale, la
sentinelle est tuable — le heart-beat rend sa mort visible).

**Suite** : les axes 2-3 du programme v0.6.0 sont écrits (l'axe 1 D85 reste
une exigence consignée — l'infrastructure sans TEE ne peut pas la satisfaire
et le dit) ; la passation de PROTOCOLE_TRIADE à v0.6.0 (modèle « spécifiés à
l'implémentation », v0.5.1) est mûre — l'arbitrage (passer avec l'axe 1
consigné, ou attendre) appartient au développeur ; cérémonies réelles
clé-I et coffre-CF2 ; D57 avec l'intervalle exact en main ; partage Éditeur
/test au compte de service (refresh OAuth ~05/11).

### D108 — le kit de cérémonie déposé dans /Cérémonie du Drive (30/10) : la distribution devient un dossier vérifié, la preuve reste au dépôt

**La demande.** « Dépose les livrables dans un dossier /Cérémonie du
drive. » Les livrables du chantier cérémonies v0.6.0 (D105-D107) vivaient
dans download/ de l'espace de travail ; ils vivent désormais AUSSI à la
racine du Drive « Triade », dans un dossier dédié, vérifiable.

**Le dossier (id 1JJXohy5olmngfm_hE_AW17AfjSciISSg).** À plat : le kit
hors-ligne (`ceremonie_gui.py` autoporteur — stdlib + tkinter seules,
zéro pip — et `ceremonie_hors_ligne.py` de référence interopérable), les
TROIS LISEZMOI (GUI, cle-I, coffre-CF2, encarts MODE GRAPHIQUE inclus),
les lanceurs double-clic `.bat`/`.sh`, et `MANIFESTE.txt` (taille + md5 +
sha256 par fichier, régénéré à chaque dépôt, commandes de vérification
par plateforme). En sous-dossier `v06/` : `__init__.py` + les cinq `.py`
du dépôt — le dossier est un MINI-DÉPÔT portable : le profil DÉPÔT du GUI
(relais `RACINE_DEPOT/v06/*.py`, import `v06.coffre_cf2`) y est
opérationnel sur toute machine connectée, pile pip proposée avec accord.
La vérification des DIX arbres du sceau exige le dépôt complet — depuis
le kit seul, l'échec est nommé, par conception.

**La discipline (l'habit ne change pas la loi, même pour la distribution).**
Gardes avant dépôt : sources présentes, et `ceremonie_gui.py` /
`ceremonie_hors_ligne.py` IDENTIQUES (md5) entre `download/` et `v06/` —
un kit divergent n'est pas déposé. Vérification ALLER-RETOUR après
écriture : 14/14 md5 MATCH (affiché, pas affirmé). Idempotence prouvée
par relance : 14/14 « inchangé », aucun doublon. Aucun secret déposé :
ni clé privée, ni phrase de contrôle D81, ni coffre — les textes vérifiés
avant envoi, `MANIFESTE.txt` le consigne. L'outil
`scripts/drive_ceremonie.py` est committé et rejouable ; son échec
éventuel est NOMMÉ avec ses parades (OAuth relais refresh ~05/11, compte
de service lecteur seul).

**La position.** Le Drive est une commodité de distribution, pas une
preuve : le md5 aller-retour protège le transport, les preuves restent
les tests du dépôt (`test_ceremonie_gui.py` 36/36 + selftest 6/6 + fumée
Xvfb 14/14 ; non-régression 43/43 et 47/47). Le kit déposé inclut le
complément D107 consigné au commit da8fd4c (journal Entrée 93, différée).

**Suite** : les cérémonies réelles (clé-I + coffre-CF2) — le kit est prêt
depuis le dépôt OU depuis le Drive ; D57 ; partage Éditeur /test au compte
de service (refresh OAuth ~05/11).

## D111 — le maître de cérémonie s'attache au dépôt (l'ancrage devient NOMMABLE, la garde ne se délègue pas)

**Constat (30/10, machine réelle).** « Le GUI ne se connecte pas au
dépôt, je n'ai accès qu'à la version hors-ligne. » Le kit D108 rendait le
profil dépôt opérationnel dans DEUX positions : le dossier /Cérémonie
téléchargé ENTIÈREMENT (mini-dépôt v06/) ou le dépôt git lui-même. Un
fichier téléchargé SEUL depuis le Drive, ou posé ailleurs, tombait sur le
bouton grisé — la cause était affichée, la parade non. Aggravant : le
remote GitHub vivait à D95, dix-sept commits derrière — « le lancer depuis
le repo git » était impossible sans poussée.

**Décision.** L'ordre de résolution du dépôt devient explicite :
`--depot CHEMIN` > `TRIADE_DEPOT` > position du fichier (défaut D107,
inchangé — le GUI vivant dans `<dépôt>/v06/` reste la voie sans option).
Trois principes, non négociables :

1. **Un chemin introuvable est un échec NOMMÉ** (code 2 au point
   d'entrée, la cause sur stderr) — JAMAIS un repli silencieux sur le
   défaut : un utilisateur qui nomme un dépôt a décidé quelque chose,
   le tooling ne décide pas à sa place.
2. **La garde ne se délègue pas** : quelle que soit la voie, c'est la
   MÊME empreinte `v06/coffre_cf2.py` qui fait foi. Un dossier sans
   elle laisse le profil désactivé, l'accueil nomme la cause ET les
   trois parades. Aucune confiance en un chemin tapé.
3. **L'état est VISIBLE** : l'accueil affiche le dépôt attaché et sa
   source (« --depot », « TRIADE_DEPOT », « position du fichier ») —
   l'utilisateur voit TOUJOURS à quoi il est connecté.

**Conséquences.** `definir_racine_depot()` rebascule le global avant
toute construction ; relais CLI, import v06.coffre_cf2, sentinelle et
config par défaut suivent sans autre câblage (lecture à l'appel).
X3 (14 contrôles) attaque la résolution, la précédence, le fail-closed
et le point d'entrée en sous-processus ; la fumée D111 rejoue le
scénario EXACT de la demande (copie autonome → symptôme → correctif →
relais CLI réel vert). La poussée des dix-huit commits vers GitHub fait
partie de la livraison : une promesse documentée mais non poussée est
une promesse rompue en silence.

**Bornes.** La vérification des DIX arbres du sceau exige toujours le
dépôt COMPLET (le mini-dépôt du kit Drive nomme son échec, par
conception) ; --depot n'autorise RIEN de nouveau — il autorise le GUI
à TROUVER ce qui existait déjà, la discipline des CLI reste la loi.

## D112 — Les trois chemins se choisissent dans la fenêtre (le GUI devient auto-suffisant pour la cérémonie)

**Décision.** La demande développeur « choisir le chemin dossier du repo
local, le chemin du coffre, le chemin du fichier de clé (ou entrer la clef
à la main) » est servie par des CHAMPS, pas par des options de lancement :
le dossier du dépôt (bouton à l'accueil, re-attachement à chaud), le coffre
CF1 (champ de l'onglet CF2, câblé à --chemin/--depuis), la clé I (bascule
fichier / saisie manuelle dans l'onglet Signer). `--depot` et TRIADE_DEPOT
restent inchangés : la ligne de commande devient un RACCOURCI, plus une
obligation.

**Frontières tenues.** Chaque champ porte SA garde fail-closed : le dossier
doit contenir v06/coffre_cf2.py (refus nommé, attachement inchangé) ; le
champ coffre vide est un refus nommé, AUCUN repli silencieux vers .keys/
(le champ est la vérité — le CLI garde son défaut, le GUI ne devine plus) ;
la saisie manuelle est pré-validée AVANT tout lancement (63 hex, non-hex,
trop long = refus nommé sans écriture), masquée par défaut, effacée dès
l'acte lancé, et la graine ne paraît ni dans le journal ni dans le verdict
(discipline « jamais à l'écran » : le GUI n'affiche que si l'utilisateur
coche « afficher » pour vérifier SA frappe). La majuscule est acceptée en
saisie (hex est hex, la copie papier ne connaît pas la casse) — le fichier
reste minuscule, norme inchangée. Le re-attachement attend qu'une cérémonie
en cours rende son verdict, et le journal survit au re-bâtissage : changer
de dépôt n'efface jamais l'historique.

**Bornes.** La vérification des dix arbres du sceau exige toujours le dépôt
COMPLET (le mini-dépôt du kit nomme son échec) ; les champs n'autorisent
RIEN de nouveau — ils permettent de DÉSIGNER ce que les CLI savaient déjà
faire, la discipline des CLI reste la loi ; la phrase saisie dans la
section Coffre CF1 transite par le temporaire 0600 détruit du relais, elle
ne paraît jamais dans une ligne de commande.


## D113 — Le GUI porte sa boîte noire (l'observabilité est locale, jamais réseau)

**Décision.** Tout ce que la fenêtre affiche, chaque dialogue posé (et sa
réponse), chaque verdict et CHAQUE crash de rappel tkinter atterrit dans
v06/ceremonie-journal.log — fichier LOCAL, horodaté, AUCUN réseau. Le
rapport part par la main de l'humain (bouton « Envoyer le rapport… » :
Enregistrer sous .txt + presse-papiers + dossier ouvert), jamais par un
fil que le GUI aurait pris pour se faire débugger.

**Frontières tenues.** L'ordre de pack est la priorité d'espace : barre de
verdict et journal se packent AVANT le corps, le corps DÉFILE (une page
plus haute que la fenêtre reste intégralement atteignable). Les dialogues
passent TOUJOURS au-dessus (parent explicite — un dialogue sans parent
peut naître DERRIÈRE et faire croire le GUI mort). Un échec d'écriture de
la boîte noire (disque en lecture seule) ne gêne JAMAIS la cérémonie : le
témoin n'est pas une dépendance. Aucune donnée secrète n'y entre : phrase
par temporaire détruit, graine jamais affichée.

**Bornes.** La boîte noire est un JOURNAL, pas une preuve : ce qui prouve
reste les CLI, les tests et le sceau — le rapport sert au DIAGNOSTIC de
terrain (le développeur le glisse dans la conversation, l'assistant lit).

## D114 — Le verdict ne répète pas le flux (une ligne d'ancrage suffit)

**Décision.** Quand la sortie d'un CLI a déjà coulé ligne à ligne dans le
journal par le flux temps réel de l'exécuteur, le verdict rend UNE ligne
d'ancrage — la première, celle de la barre. Le détail vit au-dessus, dans
l'ordre du flux ; le rapport n'est plus deux fois trop lourd.

**Frontières tenues.** SANS emit (pas de flux), le texte ENTIER reste la
remise du verdict — générer/signer hors-ligne inchangés. Le verdict ne
perd AUCUNE information : il perd un DOUBLON.

**Bornes.** Purement cosmétique de journal : aucune logique de cérémonie
touchée, aucun CLI modifié.

## D115 — Le manifeste hache le contenu CANONIQUE LF (la représentation du checkout n'est pas l'intention)

**Décision.** Toute paire CRLF est normalisée en LF avant condensé : « le
même arbre produit le même manifeste sur toute machine » redevient VRAI.
La clé physique signe l'INTENTION (le canon), pas la représentation locale
du checkout (Windows autocrlf porte CRLF sur disque).

**Frontières tenues.** La preuve de la faute est CONSERVÉE : la fenêtre de
re-cérémonie nomme la divergence de représentation SEULE (fichier par
fichier), les signatures valides, et l'amendement de spécification par
hash littéral — au lieu d'échouer en silence. Cette preuve MEURT à la
re-cérémonie (le verifier re-verdit et ne l'appelle plus). La réplique de
test repart VERT canonique à l'entrée : les tests de falsifiabilité
mesurent leurs PROPRES mutations, pas l'ère du dépôt réel. T4 devient la
cohérence état-clé (l'ère lab dit « test » sur la clé de test, l'ère
réelle dit « reelle » sur une clé différente).

**Bornes.** Un octet muté HORS fin de ligne reste une divergence NOMMÉE :
la normalisation ne masque que la représentation, jamais le contenu.

## D116 — Le fil de cérémonie par preuves, le git ciblé, la fenêtre au contenu

**Décision.** Les cinq étapes du sceau I (Préparer → Générer la clé →
Signer → Déposer → Git) s'auto-détectent par PREUVES en lecture seule
(a-signer frais, paire de clés, remise vérifiée, arbres verts, git propre
ET poussé) ; l'étape satisfaite S'EFFACE, la suivante s'affiche avec son
GESTE ; ré-évaluation après chaque verdict + validation manuelle possible
(la preuve de fichier reste la vérité). Le bouton « Pousser v06/sceau-I
sur git… » fait add ciblé SEUL (jamais « add -A » : la clé privée vit hors
du dépôt), commit au message EXIGÉ, pull --rebase AVANT push. La fenêtre
prend la taille de son contenu, « ← Accueil » vit dans le bandeau.

**Frontières tenues.** Chaque étape de git refuse NOMMÉ (pas un dépôt git,
git absent code 127, rebase en cours → « git rebase --abort » nommé,
rien-à-committer = synchronisation VERTE). La validation MANUELLE survit
aux ré-évaluations auto et meurt au « Ré-évaluer ».

**Bornes.** Le fil ne PROUVE rien (lecture seule) : il ORIENTE — la
preuve reste sceau_I.py verifier. Le push du GUI ne remplace pas le
terminal : il le relaye avec les mêmes gardes.

## D117 — Le scénario se choisit AVANT TOUT (dossier local / repo git), et le clonage vit dans la fenêtre

**Décision.** La demande développeur « avant tout choisir entre 2
scenarii qui détermineront les étapes à afficher : dossier local et repo
git ; pour le cas du repo git, un bouton qui permette de cloner le repo
voulu en local » est servie par une section SCÉNARIO en tête de l'accueil :
DOSSIER LOCAL (attachement D112, fil de CINQ étapes) et REPO GIT (fil de
SIX étapes — « Cloner le dépôt » en tête, prouvé lecture seule par
rev-parse + origin). Le panneau repo git porte le bouton « Cloner en
local… » (URL + parent + nom pré-rempli) et « Attacher un clone
EXISTANT… » (garde D111 + preuve git/origin exigée).

**Frontières tenues.** Refus NOMMÉS avant tout lancement : URL vide, URL
ou destination commençant par « - » (un argument git déguisé est une
INJECTION), destination NON VIDE (rien n'y est touché), git absent (127),
échec git relayé. Le JETON éventuel de l'URL est MASQUÉ partout
(journal, verdict, boîte noire, confirmation — ssh scp-like inchangé :
l'utilisateur « git » y est public). Après le clone, la PREUVE
(rev-parse == dossier ET origin) doit passer, puis la garde D111 décide de
l'attachement ; les pages sont rebâties SUR LE FIL TKINTER (jamais depuis
le fil ouvrier) et le profil dépôt s'ouvre directement. Le scénario ne
change AUCUNE preuve du sceau : seulement la tête du fil.

**Bornes.** Le clonage utilise LE git de la machine (aucune
réimplémentation réseau) ; un dépôt privé peut exiger l'authentification
GitHub (le navigateur peut s'ouvrir) ; le nom pré-rempli n'écrase jamais
un nom retapé à la main.

## D118 — Une seule page de cérémonie, un attachement unique, un dossier de cérémonie hors du dépôt, des lanceurs dans le dépôt

**Décision.** La demande développeur est servie par QUATRE gestes :
(1) les profils « hors-ligne » et « dépôt » sont FUSIONNÉS en une page
unique — le cahier d'onglets porte « Sceau de l'Intention » en tête, les
onglets 1-3 (clé I, stdlib pure) restent disponibles SANS dépôt attaché,
les onglets du dépôt apparaissent à l'attachement ; (2) l'ex-« Attacher
un clone EXISTANT… » et l'ex-« Choisir le dossier du dépôt… » deviennent
UN SEUL bouton « Attacher le dépôt local… » — seul le SCÉNARIO décide de
la preuve (repo git → dépôt git AVEC origin, refus nommé avec la parade ;
dossier local → garde v06/coffre_cf2.py seule) ; (3) le DOSSIER DE
CÉRÉMONIE (sœur du dépôt attaché, hors du dépôt par défaut) porte la clé
privée, la clé publique, a-signer.txt et signatures-I.txt — « Préparer
a-signer.txt » COPIE la remise fraîche dans ce dossier et pré-remplit le
champ « Remise à signer » ; (4) lancer_ceremonie.sh / .bat vivent à la
RACINE du dépôt git (v06/ceremonie_gui.py d'abord, repli sur toute copie
posée à côté) — le kit du Drive les reçoit depuis le dépôt.

**Frontières tenues.** Le CLI reste LA vérité : la copie de la remise est
un TRANSPORT (le fichier du dépôt reste la référence, échecs de copie
NOMMÉS sans annuler la préparation) ; le chemin pré-rempli transite par
un attribut simple et n'est appliqué que SUR LE FIL TKINTER (jamais
depuis le fil ouvrier — tkinter n'est pas thread-safe) ; le dossier de
cérémonie vit HORS du dépôt (la clé privée n'y entre jamais, même par
défaut) ; les champs retapés à la main ne sont JAMAIS écrasés par le
changement de dossier ; la copie « fichier seul sur clef USB » garde les
onglets clé I seuls (D87 inchangé — l'air-gap ne s'installe rien) ; la
pile pip n'est plus exigée à l'entrée mais chaque action du dépôt la
re-demande.

**Bornes.** Le dossier absent n'est pas une erreur (il naîtra à la
première écriture — Générer la clé / Préparer la remise) ; le repli du
dossier par défaut sur la maison ne survit qu'au cas du dépôt à la racine
d'un disque ; les lanceurs Windows exigent py/python présents (le .bat
met en pause sur échec pour lire la cause) ; --profil hors-ligne|depot
reste accepté (compat D117) et ouvre la même page.

## D119 — Le dossier de cérémonie naît avec la clé, et le fsync de répertoire est POSIX-seul (le terrain Windows fait loi)

**Décision.** Deux correctifs du RAPPORT DE CÉRÉMONIE du terrain v1.8 :
(1) TOUT fichier de cérémonie CRÉE son dossier de sortie s'il manque —
_assurer_dossier_de_sortie précède l'écriture de la clé privée, de la
clé publique, des signatures et de la feuille CF2 (la borne D118 « le
dossier naîtra à la première écriture » devient VRAIE pour « Générer la
clé », pas seulement pour « Préparer la remise » — le terrain l'a prouvé
en Errno 2, puis en re-run réussi après « Préparer ») ; (2) le fsync de
répertoire de l'écriture atomique (conteneur CF2, fragments,
destruction) est POSIX-seul — Windows refuse os.open() sur un dossier
(PermissionError errno 13, « CF2 — migrer » mourait en écrivant
.keys/coffre_cf2.bin) : _fsync_repertoire retourne sous 'nt', et sous
POSIX un dossier impossible à ouvrir n'abandonne pas une écriture déjà
posée (os.replace est atomique sur les deux familles).

**Frontières tenues.** Rien n'est écrit avant que le dossier soit
possible (échec NOMMÉ « impossible de créer le dossier », fail-closed —
le parent-fichier en est le témoin de test) ; l'atomicité ne dépend
JAMAIS du fsync de répertoire (la durabilité du dossier reste un
mieux-disant POSIX, pas une garantie) ; la discipline « aucun coffre
réel touché par les autocontrôles » tient (T6 et le verdict à froid D119
vivent en temporaire, journal/PV/heartbeat de labo re-localisés) ; la
simulation Windows est FIDÈLE (os.open(dossier) → PermissionError 13 ET
os.name='nt'), pas une approximation ; le crash du terrain était PROPRE
(conteneur = premier écrit de migrer : aucun fragment posé, la reprise
est un re-lancement).

**Bornes.** La simulation ne remplace pas le terrain Windows réel (le
rapport v1.9 tranchera) ; le fsync de dossier est ABSENT sous Windows
(aucune émulation) ; après tout changement du GUI, le kit du Drive doit
être re-synchronisé (md5) et le clone du terrain mis à jour (git pull)
avant toute cérémonie.

## D120 — La sentinelle est EXIGÉE au déverrouillage : la porte ferme le coffre quand le témoin meurt (la demande du terrain)

**Décision.** La question du terrain : « vu qu'elle est une condition
sine qua non du dispositif de sécurité, il faut qu'elle soit
indispensable au déverrouillage du coffre non ? parce que si le
déverrouillage est tenté et qu'elle n'est pas lancée, tous nos efforts
sont inutiles » — JUSTE, et l'ère D86 portait l'angle mort : spec § 6
disait « une sentinelle morte est un avertissement nominal, pas un
décès du coffre », donc la fenêtre la plus dangereuse du dispositif (M
reconstituée en RAM, secrets exposés) était précisément la seule où la
surveillance était OPTIONNELLE — incohérent avec le fail-closed maison
et avec le nom même de D86 (un interrupteur d'homme mort qui ne fait
rien quand il est mort n'en est pas un). D120 arme la PORTE :
porte_sentinelle() (v06/coffre_cf2.py, source unique de vérité) est
appelée par TOUTE commande qui déverrouille — verifier, lister,
obtenir, ajouter, retirer (_avec_deverrouillage et cmd_verifier) — ET
par le contrôle de relecture du GUI (controle_lecture : c'est un
déverrouillage, M en RAM depuis les copies) : sans heart-beat FRAIS
(borne heartbeat_age_max, défaut 5 s ≈ 20 boucles manquées), REFUS NOMMÉ
avec parade, JOURNALISÉ, AVANT toute lecture de fragment et toute
reconstitution — l'absence de sentinelle devient un ÉVÉNEMENT, jamais un
silence. Config : exiger_sentinelle (défaut : moteur_sentinelle_disponible()
— true là où le moteur livré inotify+/proc peut vivre) et
heartbeat_age_max ; la porte juge le heart-beat, PAS la plateforme. Le
GUI hérite de la porte PAR RELAIS (il shelle le CLI) et par
controle_lecture. La cérémonie s'inverse : liste blanche → sentinelle
DÉMARRÉE → premier déverrouillage (migrer et init l'enseignent en
sortie ; restaurer / etat-fragments / statut / bruler restent HORS
porte, aucune clé lue — le diagnostic et la relève après brûlage
demeurent possibles coffre mort : la porte interdit l'OUBLI, pas la
récupération). sentinelle_cf2.py suit : demarrer REFUSE de lancer une
sentinelle là où le moteur n'existe pas (une sentinelle incapable de
surveiller ne battrait qu'un FAUX heart-beat — pas de sécurité de
façade), l'import inotify y est gardé (sante court partout), et sante
affiche l'état de la PORTE (exiger_sentinelle) en tête.

**Frontières tenues.** Le refus est NOMMÉ avec parade et JOURNALISÉ
(best-effort : un journal impossible à écrire ne noie jamais le refus) ;
le refus ne touche RIEN (gardes octet pour octet — témoin T7) ; la
disponibilité de la relève est préservée (restaurer hors porte :
brûlage → diagnostic → restauration → sentinelle → déverrouillage) ;
l'ère Windows est honnête (exiger_sentinelle=false tant que le moteur
SACL 4663/ETW n'est pas livré, exigence consignée spec § 9 : la porte
AVERTIT fort et journalise « SANS sentinelle » à CHAQUE déverrouillage
— jamais un refus qui scellerait le coffre réel derrière une
fonctionnalité non livrée) ; le texte scellé v06/I/CF2/README.md § 6/§ 8
reste INTACT (le corriger ferait diverger l'arbre v06/I de son manifeste
signé sans la clé physique — l'amendement D120 est consigné ICI et au
LISEZMOI du kit, il entrera dans l'arbre scellé à la prochaine
re-cérémonie, précédent erratum § 12) ; aucun coffre réel touché (X8).

**Bornes.** La porte est une exigence de CÉRÉMONIE, pas une barrière
cryptographique : le heart-beat est FALSIFIABLE par un adversaire aux
privilèges utilisateur (ts forgé — prouvé par le contrôle T7
« porte-heartbeat-falsifiable-borne-consignée », l'aveu est le contrôle),
qui peut aussi déverrouiller AILLEURS avec des fragments copiés (les
gardes ne sont pas sous sentinelle, elles sont sous ACL distinctes —
spec § 5) ; ce que la porte garantit : plus AUCUN déverrouillage
légitime sans témoin, l'absence de sentinelle toujours nommée et
journalisée ; la sécurité DURE reste Shamir (sous le seuil = mort
informationnelle), ACL et brûlage ; sous Windows la porte n'exige rien
tant que le moteur n'existe pas (borne d'ère, pas de conception) ; la
sentinelle demeure TUABLE avant la lecture (borne D86) — mais sa mort
est maintenant BLOQUANTE au déverrouillage, plus seulement visible.

## D121 — La serrure à triple scellement et le cycle en deux actes : CF3 remplace le démon par un piège hors machine, et borne la session (les deux demandes du terrain, servies ensemble)

**Décision.** Les deux demandes du terrain : (1) « plutôt qu'une sentinelle
externe, une serrure du coffre piégée — un système à 3 éléments : clé
utilisateur qui ne change pas, serrure du coffre métamorphe basée sur un
hash du projet, et piège de la serrure, métamorphe aussi ; pas de 2ème
moitié (piège), tentative de déverrouillage impossible ; mauvaise clé ou
problème sur une des 2 moitiés : destruction du coffre ; ça évite de faire
tourner une sentinelle en permanence alors qu'elle ne sert qu'au
déverrouillage » ; (2) « une vulnérabilité réside durant le temps où la
session est ouverte — il faudrait deux déverrouillages : un à l'ouverture
pour la modification, un à la fermeture pour la validation ». D121 les
instancie en CF3 (spec docs/I/CF3/README.md, R2 écrite-avant-code ;
prototype v06/coffre_cf3.py, suite v06/test_coffre_cf3.py) en durcissant
TROIS pièges de l'intuition d'origine, consignés : un hash de projet est
PUBLIC (il LIE, il ne protège pas — le hash n'entre que comme contexte
HKDF, l'entropie vient des trois éléments) ; le piège ne doit PAS être
dérivable de la serrure (deux aléas INDÉPENDANTS — sinon le voleur de
l'en-tête calcule le piège) ; détruire sur mauvaise clé est un DoS OFFERT
(la phrase erronée est BÉNIGNE — réessai à délai croissant — seule la
falsification PROUVÉE détruit). La serrure : K_user = Argon2id(phrase)
INVARIANT à travers les époques (la demande), S_serrure (moitié machine,
aléa frais par époque, en-tête clair), S_piège (moitié MÉDIA SÉPARÉ, aléa
frais par époque) ; KEK = HKDF des trois, info = époque ‖ H_projet (le
liant) ; champ verif dérivé de K_user ‖ V_piège (publique, portée par le
média) : le voleur de la machine seule ne peut même pas TESTER des
phrases hors ligne. La sentinelle D120 devient INSTANTANÉE : réalisée par
INVOCATION (vérifications in-process à chaque acte, ordre normatif spec
§ 5) au lieu d'un démon résident — le démon était usurpable (faux
heart-beat, borne D120), le piège ne dépend d'AUCUN état de machine
falsifiable : sine qua non réalisée sans démon (le déverrouillage est
IMPOSSIBLE, pas seulement refusé, sans la seconde moitié). Le cycle en
deux actes borne la fenêtre de session : ACTE I (phrase + piège →
brouillon chiffré sous clé de session éphémère ; les clés maîtresses
meurent ; le canonique n'est JAMAIS réécrit), SESSION (une panne
auto-nettoie : K_session morte = brouillon déchet indéchiffrable),
ACTE II (phrase RETAPÉE + média REBRANCHÉ ; clé de clôture LIÉE AU
CONTENU ; moitiés fraîches, époque + 1 ; re-lecture À FROID avant le
remplacement atomique — l'ordre des écritures est crash-cohérent, toute
panne laisse un état rejouable).

**Frontières tenues.** La course de clôture est fermée par une parade
DOUBLE trouvée en écrivant la suite de falsifiabilité : la clé de
clôture est dérivée AVEC H_final (un KEK volé ne scelle que l'état vu) ET
l'ÉTIQUETTE est vérifiée à l'ouverture (le clair déchiffré doit hacher
vers le H_projet de l'en-tête — le faux conteneur « étiquette honnête,
contenu substitué » est une falsification PROUVÉE : destruction locale) ;
la destruction ne touche QUE la machine (conteneur, staging, brouillon —
JAMAIS le média du piège, JAMAIS les fragments CF2 ni les copies
hors-ligne : coexistence spec § 12, la destruction reste survivable) ; le
tag du piège invalide est refusé SANS destruction (le média est hors
limite de confiance — corruption bénigne possible, la destruction attend
la preuve cryptographique) ; l'anti-retour-en-arrière a TROIS miroirs
(journal local — contrôle conteneur ≥ miroir ; carte papier du sachet —
checksum 8 hex recoupé à froid ; journal Git poussé — --epoque-attendue) ;
la discipline RAM est tenue (bytearray + _effacer, aucun secret dans
journal/PV/sorties) ; l'écriture atomique D119 est RÉUTILISÉE depuis
coffre_cf2 (source unique — CF3 ne la duplique pas) ; aucun conteneur ni
phrase réels touchés (répertoires temporaires, D105) ; la spec vit sous
docs/I/CF3/ (hors périmètre du sceau — aucune divergence : verifier CODE 0
après écriture) et entrera dans l'arbre scellé v06/I/CF3/ à la prochaine
re-cérémonie (précédent erratum § 12) ; la CLI ouvrir ne pose JAMAIS de
brouillon (une session CLI meurt avec son processus — le cycle complet
vit en API, prouvé par la suite, et entrera dans le GUI après preuve
terrain).

**Bornes.** Un attaquant admin qui contrôle la machine PENDANT un acte
voit la phrase, peut photographier le média branché et forger — aucun
logiciel pur ne pare ça (le rayon est borné à UNE époque : moitiés neuves
à chaque clôture) ; cérémonie sur machine propre, sessions courtes ; le
contenu de la session reste lisible par un malware présent pendant qu'on
travaille (inhérent — on a ouvert pour lire) ; un piège ENTIÈREMENT forgé
se présente comme une phrase erronée (bénin — refus nommé, jamais de
destruction : l'aveu est le contrôle) ; contre le voleur de TOUT (machine
+ média), la défense est Argon2id seule (borne consignée, même famille que
CF1) ; le miroir local est effaçable par un attaquant admin (les témoins
hors-bande — carte, Git — restent) ; le checksum affiché ne protège que
s'il est regardé (le verdict à froid re-exécuté est le filet) ; un média
du piège par coffre (le sachet est individuel — le créneau N+1 peut être
remplacé par un rejeu, les époques passées jamais) ; CF3 ne REMPLACE pas
CF2 d'un claquement : la migration du coffre réel est une CÉRÉMONIE
consignée (spec § 12 — CF2 déverrouillé une dernière fois, porte D120
honorée, base re-scellée SCHÉMA IDENTIQUE, verdict à froid, destruction
explicite du conteneur CF2, fragments CF2 = relève historique),
l'outillage migrer vivra avec la preuve terrain.


## D122 — Le kit unique de cérémonie et le trio systématique du module à tester : une GUI, une boîte noire, un bouton « Envoyer le rapport » (les deux demandes du terrain, servies ensemble)

**Décision.** (1) LE KIT UNIQUE : le dossier « Cérémonie » du Drive est LE SEUL kit de cérémonie — complet (GUI v1.9, CF2 D119/D120, CF3 entier, pupitre d'autotest, lanceurs .bat/.sh des DEUX outils, LISEZMOI, MANIFESTE d'empreintes) et mis à jour à chaque livraison qui touche le terrain ; le miroir git « TRIADE » est renommé « TRIADE-sauvegarde-git » (même id, le hook post-commit continue par drive_sync.PROJECT_FOLDER — renommé dans le même geste) : son nom DIT qu'il n'est pas un kit, la confusion meurt avec l'ambiguïté ; tout artefact livré au terrain existe AUSSI en miroir ZIP unique au téléchargement. (2) LE TRIO SYSTÉMATIQUE : tout module produit pour être TESTÉ par le terrain porte désormais (a) une INTERFACE GRAPHIQUE (le verdict en ligne de commande s'évanouit à l'écran — un terrain sans fenêtre est un terrain sans trace), (b) une BOÎTE NOIRE locale horodatée (chaque ligne, chaque dialogue, chaque crash — témoin, jamais dépendance : muette si le disque refuse), (c) un bouton « Envoyer le rapport… » : fichier .txt + presse-papiers + dossier ouvert, AUCUN réseau (le transport est la main de l'humain, discipline D113), AUCUN secret ; le rapport DOIT emporter l'ENVIRONNEMENT (OS, Python, pile pip avec versions ou ABSENTS nommés) et les EMPREINTES md5 des modules — « pas à jour » doit se LIRE dans un rapport, pas se deviner. Le maître de cérémonie porte le trio depuis D113 ; le pupitre d'autotest CF3 (v06/autotest_cf3_gui.py) le porte ; tout module à venir le portera. Première application : v06/autotest_cf3_gui.py v1.0 — relais sous-processus des vérités vivantes (jamais une réimplémentation), verdict compté DEPUIS LE FLUX et CROISÉ avec le code de sortie, posture dite avant le fait (copie plate = autotest embarqué seul, refus nommé), PYTHONIOENCODING=utf-8 imposé aux enfants (les accents des verdicts survivent au cp850 de Windows).

**Frontières tenues.** Le pupitre NE RÉIMPLÉMENTE rien (il lance coffre_cf3.py et test_coffre_cf3.py tels quels — une divergence de verdict entre le bouton et la ligne de commande est impossible par construction) ; le rapport ne contient NI secret NI chemin de coffre réel (preuve par le rapport lui-même, falsifiée par la suite X5) ; le fil ouvrier ne touche JAMAIS tkinter (file de messages, pompage côté fil tkinter — discipline D18x) ; la boîte noire vit en *.log gitignoré (jamais commise, jamais synchronisée) ; le kit ne contient JAMAIS clé, phrase, coffre réel ni jeton (les secrets vivent hors kit).

**Bornes.** Le rapport part par la main de l'humain (aucun réseau par PRINCIPE — la cérémonie ne prend pas de fil pour se faire débugger : l'assistance ne peut pas être plus assistée que la main qui glisse le fichier) ; la preuve du .bat est STRUCTURELLE sur POSIX (contenu : replis + pause — Windows ne court pas dans le laboratoire, la limite est dite) ; la boîte noire locale est effaçable par un attaquant admin (comme tout témoin local — la carte papier et Git restent les témoins hors-bande) ; les empreintes md5 disent la GÉNÉRATION des fichiers, pas leur intégrité cryptographique face à un attaquant qui réécrirait aussi le MANIFESTE (le verdict à froid depuis un clone frais GitHub reste le filet) ; le diagnostic distant dépend du rapport ENVOYÉ (un problème non rapporté reste un problème aveugle — le trio maximise la chance, il ne la garantit pas).


## D129 — Le pilier droit : le fil d'étapes et le journal vivent dans un encart à droite, visible quel que soit l'onglet affiché (la demande du terrain : la lisibilité de l'écran)

**Décision.** La demande développeur « je voudrais que dans la gui de
cérémonie, la liste des étapes soit affichée dans un encart à droite de
l'écran qui soit visible quel que soit l'onglet affiché, idem pour le
journal de cérémonie (en dessous de la liste des étapes) pour une
lisibilité de l'écran plus facile » est servie par LE PILIER DROIT : une
colonne (380 px, largeur tenue par pack_propagate(False)) packée
side="right" À LA RACINE, AVANT le corps défilant (ordre de pack =
priorité d'espace, discipline D113 — le pilier ne peut plus être évincé)
; le FIL DE CÉRÉMONIE (D116 : résumé, étape courante, détail + geste, à
venir, boutons « Ré-évaluer l'étape » / « Marquer faite (à la main) »)
vit EN HAUT du pilier, le JOURNAL DE CÉRÉMONIE (D113) DESSOUS et
remplit le reste — tous deux HORS DES PAGES et HORS DU CAHIER : le fil
QUITTE l'onglet « 1 · Sceau de l'Intention » où il vivait depuis D118
(les onglets « 2 · Générer la clé », « 3 · Signer », « 4 · Vérifier »,
CF2 et liste blanche le CACHAIENT — le terrain devait jongler entre les
onglets pour savoir où il en était), le journal quitte sa bande
pleine largeur SOUS le corps (qui repoussait la page vers le haut) ; le
pilier SURVIT aux re-attachements (bâti UNE fois à la naissance, comme
l'exécuteur et la barre de verdict — l'historique de cérémonie ne
s'efface jamais d'un changement de dépôt) ; le fil sans dépôt attaché
le DIT (« aucun dépôt attaché — les étapes 1, 4 et 5 naîtront à
l'attachement, les onglets 2-3 restent actifs » : fail-closed, jamais
un fil muet qu'on prendrait pour un fil vide) ; les libellés du fil se
replient à la LARGEUR DU PILIER (wrap 336, plus de 880) ; la fenêtre
s'ÉLARGIT du pilier (_ajuster_taille_fenetre compte la colonne en
LARGEUR — le journal ne compte plus en hauteur : il vit à côté) ; la
version GUI passe en v2.1 (v2.0 fut l'ère LISEZMOI D128).

**Frontières tenues.** AUCUNE vérité vivante ne bouge : le fil garde
ses PREUVES lecture seule (fil_ceremonie inchangé), ses numéros D128
(onglet « n · » = étape n), son scénario D117 (titre « Fil de cérémonie
· scénario : … ») ; le journal garde sa boîte noire (chaque ligne du
pilier atterrit toujours dans v06/ceremonie-journal.log — l'encart ne
change QUE l'habit) ; le corps DÉFILE toujours (D113) et le bandeau
« ← Accueil » reste hors du corps (D116) ; la molette au-dessus du
journal Text reste la sienne ; le pilier n'existe qu'à l'écran — le
rapport « Envoyer le journal… » emporte le même texte qu'avant.

**Bornes.** Le pilier mange 380 px de largeur : sur un écran étroit
(< ~1250 px) le cahier se resserre (la fenêtre s'ouvre à la taille du
contenu, clampée à l'écran — minsize 880 inchangé, un écran plus étroit
que le contenu défile toujours) ; le fil du pilier reste COMPACT (une
ligne par liste, le détail replié à 336 px — le détail intégral vit
dans les preuves et le journal) ; le pilier n'est pas un tableau de
bord figé : il ne PROUVE rien (lecture seule), il ORIENTE — la preuve
reste sceau_I.py verifier.

## D130 — Le kit ne dérive plus du miroir : /Cérémonie/v06 et /TRIADE-sauvegarde-git/v06 sont identiques PAR CONSTRUCTION et rafraîchis dans le MÊME geste à chaque commit (la demande du terrain : « ça porte à confusion »)

**Le constat.** Le kit « Cérémonie » (D122 : « un seul kit complet et à jour ») avait repris un coup de retard sur le miroir git : ceremonie_gui.py périmé d'une génération (pré-D129), trois tests absents, les arbres I/ et sceau-I/ absents — 28 fichiers contre 42 côté miroir. La cause n'était pas un oubli mais une ASYMÉTRIE : le miroir se synchronise à chaque commit (hook post-commit), le kit exigeait un dépôt manuel (maj_kit_dNNN.py, hors dépôt). Toute décision touchant v06/ sans relance rouvrait la fenêtre de dérive — D129 l'avait ouverte.

**La décision.** (1) LE v06/ DU KIT EST DÉPLOYÉ DEPUIS `git ls-files v06/` — la même source que le miroir, lue dans le même arbre de travail : identité octet pour octet par construction, I/ et sceau-I/ inclus (preuves publiques du sceau ; aucun secret — la clé privée vit hors dépôt, D118). (2) LE HOOK POST-COMMIT PORTE LE KIT : drive_sync.py --quiet PUIS maj_kit.py --quiet (scripts/maj_kit.py, canonique, SUIVI PAR GIT) — chaque rc journalisé séparément, un échec kit ne bloque jamais le miroir ni le commit ; sync_backup.sh suit à l'identique. (3) MANIFESTE.txt DU KIT PORTE LE COMMIT DE RÉFÉRENCE : un kit périmé se LIT (empreinte + commit), ne se devine pas ; la zone download/ du labo est auto-réparée sur v06/ (les copies plates ne peuvent plus vieillir). LISEZMOI-kit.txt documente l'identité (« ce que v06/ contient ici est EXACTEMENT ce que TRIADE-sauvegarde-git/v06 contient »).

**Ce que D130 ne fait PAS.** Il n'unifie pas les DEUX dossiers : le miroir reste la sauvegarde complète du dépôt (722 fichiers + bundle), le kit reste la distribution opérable (57 entrées : lanceurs, copies plates, LISEZMOI, v06/ entier) — des RÔLES différents, un CONTENU PARTAGÉ identique et un DÉCLENCHEMENT commun. Il ne fige rien : le kit porte l'état v06 TEL QUEL (fenêtre de re-cérémonie D126 incluse — verifier CODE 10 : le signal, pas la panne). Il ne touche AUCUNE clé, AUCUN coffre réel, AUCUN arbre scellé.

**Vérifiabilité.** Aller-retour md5 de toutes les entrées à chaque déploiement (maj_kit.py, échec = rc 1 NOMMÉ) ; diagnostic indépendant par cartes récursives (divergences nulles, exclusifs nuls de part et d'autre) ; le commit qui porte D130 déclenche le hook étendu — la re-vérification post-commit prouve l'AUTOMATISME. L'OAuth relais expire ~05/11 : l'échec est nommé avec ses parades, jamais silencieux.

## D131 — Un bouton d'attachement PAR PAGE : le doublon de l'accueil (« sur la page de choix de scénario, il y a 2 boutons pour attacher un repo local qui font doublon », retour du terrain 31/10) est supprimé — le bouton NAÎT du choix de scénario, et la note « Fragments hors-ligne » nomme où vivent les cinq originaux

**Le constat.** Le rapport de cérémonie du 31/10 18:18 (boîte noire v2.1) montre le geste d'attachement accompli DEUX fois à 6 minutes d'écart (18:10:16 puis 18:10:35) : l'accueil portait « Attacher le dépôt local… » en DEUX endroits — le panneau de scénario (D117) ET la section « La cérémonie » (D118) — même commande, même garde, double affichage ; le terrain l'a dénoncé. Dans le même rapport, la question des fragments (« la cérémonie m'a produit un fragments-cf2.txt et le système attend 3 fragment-*.cf2 ») : les CINQ originaux vivent sous .keys/gardes-cf2/g1…g5/fragment-N.cf2f (un fichier par garde, dossier caché), la feuille n'est que l'export PAPIER des trois d'entre eux — ni la note de l'onglet coffre ni le LISEZMOI ne nommaient ces emplacements là où la confusion naissait.

**La décision.** (1) UN RENDU PAR PAGE : l'accueil ne porte le bouton d'attachement QUE dans le PANNEAU DE SCÉNARIO — sans scénario choisi, PAS de bouton (D117 : le scénario est AVANT TOUT, le bouton naît du choix) ; la page de cérémonie ne le porte QUE dans son bandeau « Dépôt triade — NON attaché ». Le GESTE est inchangé : _sur_choisir_depot garde la garde D111 (v06/coffre_cf2.py) et la preuve D118 (repo git → rev-parse + origin). (2) LA NOTE FRAGMENTS NOMME LES ORIGINAUX : .keys\gardes-cf2\g1…g5\fragment-N.cf2f, dossier CACHÉ, un fichier par garde — et distingue la FEUILLE (l'empreinte papier des trois fragments g3-g5, à imprimer) des COPIES USB (les fichiers .cf2f eux-mêmes) que le contrôle de relecture relit ; LISEZMOI-coffre-CF2.txt reçoit le même éclaircissement (étape 3), LISEZMOI-ceremonie-GUI.txt suit (son ex-« Choisir le dossier du dépôt… » périmé est corrigé au passage). (3) VERSION v2.2 (VERSION_GUI — l'ère suit la dernière décision GUI) ; la note du MANIFESTE kit (maj_kit.py) est réécrite en même temps (v2.2, et le paragraphe sceau rendu EXACT : le sceau signe v06/I/, pas le code).

**Ce que D131 ne fait PAS.** Aucune preuve, aucune garde, aucune commande ne change : le fil D129, le cahier D128 et le scénario D117 sont intacts — seule la REDONDANCE d'affichage meurt. Le sceau I n'est PAS touché : l'arbre signé v06 couvre v06/I/ (la spécification, 3 fichiers), PAS le code — verifier reste 10 arbres VERTS après le correctif (vérifié AVANT consignation), aucune re-cérémonie n'est appelée par D131. Aucune clé, aucun coffre réel, aucun fragment n'est lu ou écrit : le correctif est d'affichage et de documentation.

**Vérifiabilité.** test_ceremonie_gui.py porte T18 (6 contrôles statiques : accueil zéro rendu et note qui renvoie au panneau ; panneau deux rendus, un par scénario ; cérémonie un rendu ; TROIS rendus au total — un doublon serait régressif ; geste intact ; note fragments) — 178 PASS / 0 ÉCHEC ; la fumée Xvfb scripts/fumee_xvfb_d131.py (8 contrôles sur fenêtre RÉELLE : zéro bouton sans scénario, un seul en dossier local vivant DANS le panneau, un seul en repo git à côté du clonage, survie au re-choix, jamais deux quel que soit le scénario) ; fumée D129 intacte (21 PASS) ; selftest 19/19. Le commit porte le hook D130 : kit + miroir Drive rafraîchis dans le même geste.

## D132 — Le GUI de migration CF2 → CF3 passe en GRILLE : chaque bouton « Parcourir… » vit sur la MÊME ligne que son champ (le retour du terrain : « l'interface n'est pas très claire, problèmes de disposition ; les boutons de recherche de fichiers ne sont pas alignés aux champs concernés »)

**Le constat.** Le terrain (31/10, en pleine cérémonie CF2 → CF3) dénonce la disposition du GUI de migration : les boutons de recherche de fichiers ne sont pas alignés aux champs concernés. La cause est MÉCANIQUE et lisible dans v06/migration_cf3_gui.py v1.0 : chaque champ était packé `fill="x"` PLEINE LARGEUR, puis son bouton « Parcourir… » était packé `side="right"` APRÈS — la cavité restante reléguait les boutons en COLONNE à droite, SOUS les champs : quatre boutons empilés, aucun sur la ligne de son champ (le second champ de phrase, sans étiquette, achevait la confusion). Le geste n'était pas en cause : seulement l'habit.

**La décision.** (1) LA GRILLE PARTOUT DANS LES ONGLETS : chaque ligne de saisie devient un bloc de DEUX lignes de grille — étiquette AU-DESSUS, champ (colonne 0, étirable) et bouton « Parcourir… » (colonne 1) sur la MÊME ligne ; l'aide `_ligne_parcourir` (le pack side="right" fautif) MEURT, absorbée par `_champ(parent, étiquette, valeur, dialogue, titre, ligne)`. (2) LA CLARTÉ QUI MANQUAIT : TOUT champ de chemin porte désormais son bouton (l'onglet VÉRIFIER gagne celui du conteneur CF3, l'onglet DÉTRUIRE ceux des DEUX conteneurs, l'onglet MIGRER celui du conteneur CF3 naissant — dialogue d'enregistrement) ; la confirmation de phrase est ÉTIQUETÉE (« Confirmation de la phrase : » — l'ancien second champ muet) ; les boutons d'acte (MIGRER / VÉRIFIER / DÉTRUIRE) prennent la PLEINE LARGEUR de l'onglet ; un séparateur isole le bloc PHRASE du bloc CHEMINS dans l'onglet MIGRER. (3) VERSION v1.1 (VERSION_GUI), docstring d'en-tête étendue (point 5 : la disposition) ; `self.carnets` est exposé (la fumée sélectionne les onglets).

**Ce que D132 ne fait PAS.** AUCUN acte, AUCUNE garde, AUCUN relais ne change : les arguments passés à coffre_cf3.py (migrer / verifier / detruire-cf2) sont les mêmes OCTET POUR OCTET, la phrase reste par STDIN jamais affichée, la boîte noire et le rapport D113/D122 sont intacts — le correctif est d'HABIT, pas de serrure. Le GUI de cérémonie (ceremonie_gui.py v2.2) et l'autotest CF3 (autotest_cf3_gui.py) ne portent PAS ce défaut (vérifié : aucun champ+bouton packés de la sorte). Le sceau I n'est PAS touché : l'arbre signé couvre v06/I/ (la SPÉCIFICATION), PAS le code — verifier rend 10 arbres VERTS APRÈS le correctif (vérifié AVANT consignation), aucune re-cérémonie n'est appelée.

**Vérifiabilité.** Selftest embarqué : contrôle n° 9 « disposition : champ et bouton “Parcourir…” sur la même ligne de grille (D132) » — preuve structurelle AST (dans `_champ`, le Entry et le Button partagent la MÊME valeur de `row`, dans des colonnes DISTINCTES ; un retour au pack side="right" ferait échouer) — 18 → 19 PASS ; test_migration_cf3_gui.py suit (L : « 19 PASS / 0 ÉCHEC ») — 28 PASS / 0 ÉCHEC ; FUMÉE Xvfb scripts/fumee_xvfb_d132.py (14 contrôles sur fenêtre RÉELLE : trois onglets en grille — pack_slaves vide —, chaque bouton ALIGNÉ à un champ à ±3 px ET à sa droite, bijection bouton→champ, comptes attendus 5/2/2, boutons d'acte pleine largeur ≥500 px, confirmation étiquetée) — 14 PASS / 0 ÉCHEC ; FALSIFIÉ DE L'AUTRE CÔTÉ (scripts/falsifie_d132_v10.py) : le code v1.0 extrait de git HEAD, la MÊME mesure — 4 boutons « Parcourir… », 4 SANS champ aligné : le défaut du terrain est VISIBLE dans l'ancien code et MORT dans le neuf. Le commit porte le hook D130 : kit + miroir Drive rafraîchis dans le même geste.

## D133 — LA PASSATION v0.6.0 : le programme de souveraineté cryptographique devient spécification ; la sentinelle est PAR INVOCATION (la serrure), un coffre neuf naît CF3 ; M5 ouvert ; le Livre du Coffre accompagne (arbitrage du développeur sur sept questions)

**Le constat.** Le plan déclarait la passation MÛRE dès l'écriture des trois composants (« l'arbitrage appartient au développeur ») ; le terrain vient de fournir la preuve qui manquait : la chaîne réelle du coffre a migré CF1 → CF2 → CF3 les 30–31 octobre 2026 (rapport de boîte noire v1.1 du 30/10 20:41 — époque 1, checksum 0cc89a96, verdict à froid VERT deux fois, CF2 laissé intact jusqu'au geste explicite). Dans la même conversation, la question du terrain — « on avait pas décidé de la supprimer, la sentinelle, en migrant en cf3 ? si on impose cf3 dès la création de projet, on n'a pas besoin de sentinelle non ? » — désigne l'endroit de la spécification où la réponse doit vivre noir sur blanc.

**La décision (arbitrage du développeur, sept questions).** (1) Version : **v0.6.0** — passation avec l'axe 1 (D85, TEE) consigné comme exigence, l'infrastructure sans racine de confiance matérielle ne pouvant la satisfaire et le disant. (2) Le coffre reçoit un document complémentaire ENTIEREMENT consacré : le **Livre du Coffre** (nature complète — spec + cérémonies + runbook ; retours terrain en encadrés ; ampleur maximale). (3) Les quatre incontournables y entrent : schéma de la chaîne, empreintes md5, table décisionnelle D75 → D133, gestes de panne. (4) Passation FORMELLE : PROTOCOLE_TRIADE.md, PLAN_MILESTONES.md, PDF formel régénéré par build_pdf.sh (passé à spec_v060), commit + push — le hook D130 porte kit et miroir. (5) Suite : **jalon M5 ouvert** (programme a/b/c : empreintes par build, interception VM, patch du journal en production). (6) Position normative de la sentinelle, consignée au § 12.5 : l'exigence D120 est réalisée **par invocation** — la sentinelle instantanée de CF3 est la serrure, aucun démon à lancer, aucun moteur de plateforme à attendre ; le démon résident CF2 (usurpable par faux heart-beat) est MORT. (7) **Un coffre neuf naît CF3** : `init` direct, époque 1, média du piège dès le premier jour — la chaîne CF1 → CF2 → CF3 est l'histoire du coffre réel, pas un rite.

**Ce que D133 ne fait PAS.** Elle ne touche AUCUNE règle du cœur (hiérarchie inchangée, aucune couche ajoutée à l'exécution), AUCUNE clé, AUCUN coffre réel, AUCUN arbre scellé : les documents vivent dans docs/ et scripts/, hors v06/I/ — le sceau signe la spécification scellée, les sources docs/ seront signées à leur propre version (modèle par-version, v06/I/README.md § 1 ; signer avant passation : REJETÉ/REPORTÉ en correspondance 19.7). Elle ne ferme pas la chaîne du coffre réel : la destruction CF2 reste un geste explicite du maître, après recoupement sur machine froide.

**Vérifiabilité.** Les deux PDF passent la chaîne qualité (pdf_qa PASS : tailles cohérentes, aucune page blanche, polices embarquées, remplissage, marges symétriques ; couvertures validées sans chevauchement ; zéro Overfull ; références croisées résolues ; aucun placeholder). La passation du markdown est ASSERTÉE remplacement par remplacement (scripts/revision_v060_md.py — 45 références renumérotées en ordre décroissant, chaque compte vérifié). Les empreintes md5 des quinze modules v06 sont mesurées au dépôt (commit c504436) et consignées aux annexes ; la divergence honnête du coffre_fort.py du clone terrain (299fd124… vs 8c79263b…) est CONSIGNÉE, à recouper au prochain git pull. sceau_I.py verifier est exécuté AVANT consignation : 10 arbres VERTS attendus (l'état D126 intact). Le commit porte le hook D130 : kit + miroir Drive portent la passation dans le même geste.


## D134 — EMPREINTES PAR BUILD ACTIVES (M5-a) : chaque build consigne LUI-MÊME l'empreinte de son artefact au tableau de bord et au journal de travail ; la comparaison inter-build devient un contrôle automatique et toute divergence un REFUS NOMMÉ — le registre des dix PDF livrés naît rattrapé, la chaîne du livre devient buildable (merge_cover.py réparé) et reproduit l'artefact OCTET POUR OCTET

**Le constat.** Le critère de sortie du chantier (a) du jalon M5 exige que « tout artefact livré porte son empreinte CONSIGNÉE par le build qui l'a produit », or le stamp existant (.pdf_build.stamp) est l'empreinte des SOURCES, pas de l'ARTEFACT : un PDF pouvait être échangé, vieillir ou diverger sans qu'aucun contrôle ne le nomme. À l'inverse, le registre rétrospectif existait déjà (ANNEXE A mesure les 15 modules à c504436) mais restait un geste manuel de passation. En ouvrant le chantier, la réparation de la chaîne du livre révèle une faute latente : scripts/livre_coffre/merge_cover.py, tel que consigné à 7c9a09c, avait PERDU son bloc de constantes (HERE/COVER/BODY/OUT) — le script n'était pas exécutable ; la fusion de la passation avait tourné sur une version de travail non consignée.

**La décision.** (1) `scripts/empreintes_build.py` (stdlib seule) devient le moteur du registre : `consigner` — appelé PAR LE BUILD juste après publication — pose sha256 + md5 + taille de l'ARTEFACT dans le TABLEAU DE BORD (docs/TABLEAU_BORD.md, GÉNÉRÉ intégralement à chaque consignation, jamais édité à la main) et une ligne dans le JOURNAL DE TRAVAIL (sous le marqueur `m5a:journal-des-builds`, la plus récente en tête ; les entrées numérotées s'insèrent toujours AVANT le marqueur). (2) `verifier` est le contrôle automatique : DICTIONNAIRE DES REFUS NOMMÉS — ARTEFACT-ABSENT (consigné disparu du disque), EMPREINTE-DIVERGENTE (l'octet sur disque ≠ dernière consignation : modifié hors build), ARTEFACT-DELIVRÉ-NON-CONSIGNÉ (un PDF sous docs/ hors registre), BUILD-NON-DÉTERMINISTE (deux consignations du même stamp de sources portent des sha256 différents), COPIE-DIVERGENTE (la copie de livraison download/ ≠ dépôt), REGISTRE-ILLISIBLE (ligne non conforme). (3) Les DEUX chaînes PDF portent l'étape : build_pdf.sh 5bis et le NOUVEAU build_livre.sh (miroir du premier : stamp .livre_build.stamp, re-capture Playwright du schéma seulement si le HTML est plus récent que le PNG, pdf_qa, publication, consignation). (4) `modules` mesure en direct les 15 md5 d'ANNEXE A contre les blobs git HEAD : le recoupement du terrain (« mon clone diverge-t-il du dépôt ? ») devient UNE COMMANDE, l'écart un verdict nommé — c'est la réponse outillée à l'étape (4) de l'Entrée 120. (5) Le registre naît RATTRAPÉ : les dix PDF livrés (huit archives gelées + spécification v0.6.0 avec son VRAI stamp + livre) entrent au tableau avant tout nouveau build ; le rattrapage du livre porte honnêtement le stamp « — » (la chaîne consignée était brisée), et le rebuild qui suit immédiatement lui donne son stamp réel.

**Ce que D134 ne fait PAS.** Elle ne touche AUCUNE clé, AUCUN coffre réel, AUCUN fragment, AUCUN arbre scellé (les scripts vivent dans scripts/, les documents dans docs/, hors v06/I/) ; elle ne modifie AUCUN module d'ANNEXE A (verifier modules : 15 VERT constatés) ; elle n'impose pas la signature des artifacts (le modèle par-version demeure, correspondance 19.7) ; elle ne bloque JAMAIS un commit sur un refus (le contrôle rend son verdict, l'agent consigne — la même discipline que le coffre : le refus nommé d'abord, la décision ensuite) ; elle ne prétend pas au build octet-déterministe des INTERMÉDIAIRES (cover.pdf/main.pdf seuls changent, par dates embarquées que la fusion rejette — l'ARTEFACT final, lui, s'est révélé reproduit octet pour octet).

**Vérifiabilité.** La falsifiabilité est un cahier de SEIZE contrôles (scripts/test_empreintes_build.py, bac à sable temporaire, dépôt réel déclaré intact par le contrôle 0) : mesure indépendante par hashlib, lignes exactes au tableau et au journal, idempotence (même octet + même stamp + même build → aucune entrée), auto-création du marqueur, état sain VERT — et CHAQUE refus prouvé vivant : octet tampéré après consignation → EMPREINTE-DIVERGENTE ; artefact supprimé → ARTEFACT-ABSENT ; PDF fantôme livré → ARTEFACT-DELIVRÉ-NON-CONSIGNÉ ; même stamp deux sha → BUILD-NON-DÉTERMINISTE ; copie de livraison altérée → COPIE-DIVERGENTE ; registre corrompu → REGISTRE-ILLISIBLE ; module divergent et module absent → MODULE-DIVERGENT. Constat de terrain du chantier : le rebuild du livre (chaîne réparée) REPRODUIT l'artefact de la passation OCTET POUR OCTET (sha256 d36bff0f… == n°10 == n°11, md5 000e54fc… — le registre en garde les deux lignes, rattrapage puis build) ; la présente décision modifie DECISIONS.md et PLAN_MILESTONES.md, sources du PDF formel : build_pdf.sh reconstruit la spécification dans le même geste et son empreinte est consignée par le build lui-même — le verdict final du verifier et les pages comptées vivent à l'Entrée 122 du journal. sceau_I.py verifier exécuté AVANT consignation : 10 arbres VERTS CODE 0 attendus.


## D135 — LE COFFRE FORT DEVIENT PROJET FILS : fondation séparée (dépôt git, dossier Drive, plan des jalons, instructions de reprise), développement DIFFÉRÉ au bouclage de TRIADE — l'analyse fondatrice du développeur cite quatre domaines (journalisme, finance, défense, héritage)

**Le constat.** Le coffre a dépassé son rôle de composant : la migration réelle CF1 → CF2 → CF3 (30-31/10, époque 1, checksum 0cc89a96, verdict VERT à froid deux fois) a démontré une mécanique qui n'a plus rien de spécifique à TRIADE. Le développeur tranche le 31/10 : « je pense qu'il faut que le coffre fort fasse l'objet d'un projet à part entière car il peut avoir d'autres applications » — et nomme les quatre : journalisme d'investigation et lanceurs d'alerte (l'archétype du *Dead Man's Switch* parfait : aucune saisie informatique seule ne déchiffre sans la complicité physique et consciente du gardien) ; finance de haute sécurité (cold storage des clés maîtresses — le piège d'époque doit être physiquement branché pour chaque transaction ou rotation) ; défense et infrastructures critiques (quorum Shamir 3/5 et présence physique, traçabilité inviolable de la carte papier) ; héritage numérique et succession (la transmission post-mortem où les héritiers assemblent physiquement les fragments). Il demande la fondation immédiate (« son propre dossier drive, repo git, plan milestone, instructions de reprise ») et le développement différé (« quand le projet Triade sera bouclé »).

**La décision.** (1) LE DÉPÔT github.com/alexisfrlopez-debug/coffre-fort (privé, miroir de la visibilité du père) naît avec QUATRE documents et RIEN d'autre : README.md (charte — vision citée intégralement, héritage mobilisable comme FAITS, frontières), docs/PLAN_MILESTONES.md (jalons M0-M6 du fils : acte fondateur, détachement, profils d'application, commutateur d'homme mort, succession post-mortem, durcissement par domaine, passation v1.0 — PROPOSITION fondatrice, l'arbitrage d'ouverture appartient au développeur), REPRISE_PROJET.md (instructions de reprise auto-suffisantes : condition d'ouverture, les dix minutes, conventions héritées non négociables), docs/JOURNAL_TRAVAIL.md (Entrée 0 : la fondation, citant l'analyse fondatrice). Commits 8f52851 puis 67757dc, poussés sur GitHub (main == origin/main). (2) LE DOSSIER DRIVE « Coffre-Fort », FRÈRE du dossier « Triade » (même parent) : miroir git + bundle + REPRISE_PROJET.md à sa racine, synchronisés par SON PROPRE scripts/drive_sync.py et SON PROPRE hook post-commit — la discipline D12/D122 du père, NATIVE au fils dès son premier commit (le hook du commit 67757dc a porté la première synchro, rc=0 ; re-run idempotent : 8 inchangés, 0 erreur). (3) LE SIGNAL D'OUVERTURE du chantier M0 est un MESSAGE DU DÉVELOPPEUR — jamais une inférence ; aucun code n'entrera au dépôt du fils avant lui. (4) La fondation est consignée des DEUX côtés : Entrée 0 du journal du fils, D135 et Entrée 123 du père.

**Ce que D135 ne fait PAS.** Aucun fichier de code TRIADE n'est forké (le dépôt du fils ne contient que des documents) ; le coffre RÉEL, les clés, les fragments, le sceau I, les arbres scellés : RIEN n'est touché ; le nom « Coffre-Fort » est un nom de travail (arbitrage M0 du fils) ; la licence du fils n'est pas choisie (arbitrage M0 ; le père est BSL 1.1) ; le père ne ralentit pas — le jalon M5 continue dans le même geste (D136 suit).

**Vérifiabilité.** Le dépôt existe et est poussé (commits 8f52851/67757dc sur origin/main) ; le dossier Drive « Coffre-Fort » existe et porte miroir + bundle + REPRISE (drive_sync du fils : bilan idempotent 8 inchangés, 0 erreur) ; l'Entrée 0 du journal du fils consigne la fondation ; le présent commit du père déclenche le hook D130 (kit + miroir). sceau_I.py verifier exécuté AVANT consignation : 10 arbres VERTS CODE 0 attendus.

## D136 — M5 (b) OUVERT : L'AUTORITÉ DE TEST LOCALE LIVRÉE ET PROUVÉE (treize contrôles, juge indépendant curl), LE KIT VM ÉTAPE 1 LIVRÉ AU TERRAIN (le critère M4 rejoué en VM isolée au réseau coupé — sans navigateur encore), ET LE FLUX NAVIGATEUR ARBITRÉ : le RELEVEMENT http→https AMONT (révisions http-08:R3 / http-10:R3 / http-12:R2 écrites-avant-code) — le MITM/CONNECT REJETÉ

**Le constat.** Le critère (b) exige « un flux navigateur intercepté de bout en bout dans la VM ». Or le constat terrain.17 (D96) tient toujours : aucun client standard ne parle la forme absolue https:// — un navigateur sur https:// parle CONNECT au mandataire puis chiffre lui-même (octets opaques pour le proxy, et le protocole scellé n'a AUCUN TLS côté serveur : InitializeSecurityContext seulement, jamais AcceptSecurityContext) ; sur http://, il parle la forme absolue http:// — le chemin M3 SCELLÉ et prouvé terrain (T2, six verts consécutifs). Par ailleurs « l'autorité de test locale » n'existait pas : les runs 17 jugeaient contre example.com et self-signed.badssl.com — de vrais serveurs, donc du RÉSEAU, donc aucune isolation possible.

**La décision.** (1) L'AUTORITÉ DE TEST LOCALE (m5/autorite/) : origine HTTPS en stdlib pure, QUATRE modes de certificat (valide signée par la racine de test / autonome auto-signée — le miroir local de badssl / autre-hôte à SAN mensonger / expirée), fixtures générées au LABORATOIRE (regenerer_fixtures.sh, OpenSSL ≥ 3.5, quatre chaînes vérifiées en sortie, empreintes consignées — les clés sont des clés de TEST jetables qui ne signent que autorite.test / autre.test), REFUS NOMMÉS (MODE-INCONNU, FIXTURE-ABSENTE au fichier coupable près, FIXTURE-ILLISIBLE, JOURNAL-INDICIBLE — D99 : le journal de preuve est exigé, PORT-INDISPONIBLE), journal SUR LE DISQUE (la poignée refusée est NOMMÉE : l'échec du tunnel visible côté autorité), ARRÊT PROPRE (--arret-apres / --arret-apres-secondes ; la poignée refusée ne compte PAS — un tunnel qui échoue n'est pas un service rendu), PAGE STABLE (aucune date embarquée : le témoin recoupe octet pour octet ; l'en-tête Date vit sa vie — il EST une preuve de run, modèle 17-H), fermeture TLS civilisée (close_notify borné — le tunnel M4 distingue la fin de contexte de la rupture). (2) LA PREUVE LABORATOIRE : test_autorite.py — TREIZE contrôles, 13 PASS / 0 ÉCHEC : chaque mode tient sa promesse devant un client TLS exigeant, chaque refus nommé est VIVANT (prouvé par le geste qui le déclenche), les arrêts propres sont constatés (après UNE requête et par délai), et CURL — le client M3 du terrain — juge en croisé : 200 + marqueur sur valide, code 60 (certificat) sur autonome. (3) LE KIT VM ÉTAPE 1 (m5/vm/) : scenario-m5b.wsb (Windows Sandbox, RÉSEAU COUPÉ, kit monté en lecture seule + dossier preuves en écriture), scenario-m5b.ps1 (hosts, racine de test au magasin, empreintes consignées, RUN A certificat VALIDE → 200 + marqueur + « tunnel chiffre etabli », RUN B certificat AUTO-SIGNÉ → la 502 « Certificat rejete » 34 octets EXACTS + « certificat rejete » au journal proxy + poignée refusée au journal autorité — LES DEUX RUNS DANS LE MÊME SCÉNARIO, « quit » au proxy → code 0, TÉMOIN SUR LE DISQUE qui SURVIT à la destruction de la VM — leçon D99), client-m5b.ps1 (l'héritier direct de terrain_m4.ps1), LISEZMOI-terrain-m5b.txt (préparation hôte en dix minutes, python EMBARQUÉ — le bac à sable n'a pas de Python et son réseau est coupé, mode dégradé NOMMÉ avec nettoyage, risques consignés : scripts écrits sans interpréteur PowerShell au laboratoire, comportement de révocation Schannel hors-ligne). (4) L'ARBITRAGE DU FLUX NAVIGATEUR : le RELEVEMENT http→https AMONT est RETENU — le navigateur parle http:// absolu au mandataire, le mandataire RE-CHIFFRE vers l'origine par le tunnel M4 TEL QUEL (interception : le clair du navigateur ; re-chiffrement : le tunnel) ; le MITM/CONNECT est REJETÉ — il exigerait un domaine TLS serveur entier pour un résultat que le relevement atteint avec l'existant prouvé. L'intention ÉCRITE-AVANT-CODE vit dans m5/I/README.md : http-08:R3 (le verdict « cible à relever », SI ET SEULEMENT SI la politique est armée — sans elle, R2 octet pour octet, le T2 scellé reste vert), http-10:R3 (le routage du relevement par LE MÊME chemin Q2' + LA LIGNE DE FLUX y naît — méthode, hôte, verdict, octets clairs, ZÉRO secret, charte § 3), http-12:R2 (la politique de démarrage `--relever-https` ; tout argument inconnu est un REFUS NOMMÉ au démarrage — la graine de « l'interface en ligne de commande » du jalon M5).

**Ce que D136 ne fait PAS.** Le proxy 0.5.0 scellé est INTACT (sha256 b9264e0b…, 28 160 o) : aucune notation n'a bougé — les révisions R3 sont de l'INTENTION, la notation suivra (m5/layout.py, oracle à scénarios, carte, conformité — le modèle D104 entier) ; le sceau I n'est pas touché (tout vit dans m5/ et docs/, hors v06/I/) ; l'étape 1 n'est PAS le critère (b) complet — le navigateur manque, et le kit ne prête pas le contraire (« ce que l'étape 1 n'est pas encore » dit le LISEZMOI) ; aucune vraie clé ne voyage (fixtures de test jetables, empreintes publiques).

**Vérifiabilité.** La suite 13 PASS / 0 ÉCHEC (constaté au dépôt, journal de l'Entrée 124) ; regenerer_fixtures.sh juge ses quatre chaînes à la sortie (valide/valide/rejetée-expirée/rejetée-auto-signée + hôtes croisés) ; les .ps1 sont en CRLF (conversion assertive, vérifiée octet par octet) ; le kit sera jugé par LE TERRAIN — le témoin-m5b.txt attendu EST la preuve, modèle terrain.17 (les refus nommés du scénario désignent eux-mêmes le coupable) ; sceau_I.py verifier exécuté AVANT consignation : 10 arbres VERTS CODE 0 attendus ; le présent commit déclenche le hook D130 (kit + miroir portent le chantier dans le même geste).

## D137 — LE NIVEAU DU COFFRE NEUF DEVIENT L'ARBITRAGE DU DÉVELOPPEUR (CF1/CF2/CF3 à la création) : la règle D133-(7) « un coffre neuf naît CF3 » est EXPLICITEMENT INVALIDÉE et remplacée — imposer CF3 par défaut serait trop contraignant selon le projet (spécification v0.6.1, § 12.5 réécrit ; Livre du Coffre v1.1)

**La demande du développeur (31/10/2026, consignée fidèlement).** « Concernant Triade, après réflexion, je pense qu'il faut laisser le choix du niveau de sécurité (cf1 - cf2 - cf3) à l'appréciation du développeur lors de la création de son projet de développement, car imposer cf3 par défaut risque d'être trop contraignant selon le projet. »

**Le constat qui l'étaye.** CF3 est la génération la plus forte ET la plus exigeante : média du piège à produire dès le premier jour, cycle en deux actes à CHAQUE session, sachet physique + carte papier à tenir. Pour un prototype, un projet jetable ou des secrets reproductibles, l'exigence dépasse la menace réelle — la fonction objectif ordonne bien Sécurité avant tout, mais le DANGER couvert doit exister : forcer la garde maximale contre une menace absente est une contrainte sans bénéfice, et une contrainte inutile finit contournée ou évitée (le risque réel : le développeur qui n'ose pas créer le coffre, ou le tient mal). La mécanique des trois naissances existait déjà dans les outils — il manquait le DROIT de l'exercer.

**La règle nouvelle (§ 12.5 v0.6.1).** Le niveau de sécurité d'un coffre neuf — CF1, CF2 ou CF3 — est choisi par le développeur lors de la création de son projet de développement. LES TROIS NAISSANCES : CF1 par `coffre_fort.py init` ; CF2 par `init` CF1 puis cérémonie `coffre_cf2.py migrer` (l'`init` direct de CF2 DEMEURE un outil de laboratoire — la spécification scellée `v06/I/CF2/README.md` § 12 fait foi, sa promotion en cérémonie réelle exigerait la clé hors-ligne : REJETÉ pour cette révision) ; CF3 par `coffre_cf3.py init` (époque 1). LE GUIDE (recommandation, pas contrainte) : CF1 — menace vol au repos seule, simplicité de relève (prototype, projet jetable, secrets reproductibles) ; CF2 — garde partagée ou devant survivre au maître (quorum) ; CF3 — secrets maîtresses sous menace d'expropriation. La chaîne de migration CF1 → CF2 → CF3 DEMEURE disponible à tout moment — les besoins grandissent, le coffre monte ; la descente de niveau n'existe pas (`bruler` reste la fin de vie). Le niveau choisi se consigne AU JOURNAL DES DÉCISIONS DU PROJET avec sa raison (un arbitrage muet serait un contrat non écrit, § 3). Obligations par niveau : CF1 — garde durable de la phrase (D81) ; CF2 — T copies hors-ligne + liste blanche ; CF3 — média du piège + discipline du sachet (§ 13).

**Rejeté.** Imposer CF1 par défaut en guise de souplesse (remplacer une imposition par une autre ne rend pas la décision au développeur) ; un niveau mutable sans cérémonie (le niveau change par MIGRATION uniquement — acte explicite, fail-closed, l'anti-retour d'époque et le verrou croisé demeurent) ; promouvoir l'`init` CF2 de laboratoire en cérémonie réelle dans cette révision (la spécification scellée fait foi ; la naissance CF2 est prouvée par `init` CF1 + `migrer` ; l'arbitrage est consigné si le besoin naît) ; toucher au code des trois outils (aucun octet — les trois actes de création existent et sont prouvés).

**La passation documentaire.** `docs/PROTOCOLE_TRIADE.md` → v0.6.1 (`scripts/revision_v061_md.py`, miroir de revision_v060_md.py — chaque remplacement ASSERTÉ : titre, bloc d'en-tête, § 1.7 mis au passé avec renvoi, § 1.8 « Ce que change la v0.6.1 » NOUVEAU, § 12.5 RÉÉCRIT [titre compris : « Le niveau du coffre neuf — un arbitrage du développeur (D137) »], § 19.8 « Correspondance v0.6.0 → v0.6.1 » NOUVEAU + rejets, journal des versions + 1 ligne, paragraphe de clôture). La chaîne PDF NAÎT spec_v060 → spec_v061 (main.tex/fancyhead/pdftitle v0.6.1 ; sec-a § 1.7 ajusté + § 1.8 ; sec-cf § 12.5 + TABLEAU des trois naissances + légende de la chaîne ; sec-d correspondence v0.6.0 → v0.6.1 + D137 au journal narratif + annexe décisionnelle D75–D137 + ligne D137 ; couverture Template 03 v0.6.1 — sous-titre ajusté pour tenir l'écart subtitle/authors, 16,8 px mesurés sous Playwright) ; `build_pdf.sh` pointé sur spec_v061 (FINAL_PDF v0.6.1). Le schéma de la chaîne est RE-CAPTURÉ (`chaine_cf.html` : la note « un coffre neuf naît CF3 » devient « le niveau d'un coffre neuf est arbitré par le développeur (D137) », Playwright @2×, PNG porté aux DEUX chaînes vivantes — spec_v061 et livre_coffre ; l'archive spec_v060 reste INTACTE). **ERRATUM consigné** : `\begin{table}tbp]` — crochet ouvrant manquant, spec_v060/sec-d.tex:377 — laissait l'octet parasite « tbp] » PAGE 31 du PDF v0.6.0 livré (nommé par pdfplumber) ; réparé dans spec_v061 (`[htbp]`) — l'archive v0.6.0 reste ce qu'elle est, la faute est morte dans la chaîne vivante. Le **Livre du Coffre passe à v1.1** : avant-propos (complément de la v0.6.1), légende du schéma, runbook « Pour un coffre neuf » → l'arbitrage et les trois naissances, table décisionnelle + D137, réponse FAQ alignée (la QUESTION reste verbatim — elle fut réellement posée ; la réponse nomme la révision), couverture v1.1, `build_livre.sh` → v1.1. PLAN_MILESTONES (phrase de naissance révisée), README (pointeurs v0.6.1/v1.1, cahier V1–V15), REPRISE_PROJET (bloc DERNIÈRES ÉVOLUTIONS). Le projet fils coffre-fort reçoit la note d'alignement (son concept de PROFIL — README § 3.2 — est le prolongement naturel de l'arbitrage ; commit propre à son dépôt).

**Frontières.** AUCUN code d'outil touché (`coffre_fort.py`, `v06/coffre_cf2.py`, `v06/coffre_cf3.py` inchangés — l'arbitrage existait en actes, le droit manquait) ; le coffre réel du développeur RESTE CF3 (aucune migration, aucune clé, aucun fragment, aucun conteneur touchés) ; sceau I vérifié AVANT consignation : 10 arbres VERTS CODE 0, cle deposee reelle (les révisions vivent dans docs/ et scripts/, hors v06/I/) ; le proxy 0.5.0 scellé INTACT (sha256 b9264e0b…) ; aucune notation touchée ; les archives v0.6.0 et Livre v1.0 restent INTACTES dans docs/.

**Vérifiabilité.** revision_v061_md.py : huit remplacements/insertions ASSERTÉS, tous passés ; sceau verifier 10/10 VERTS (constaté avant consignation) ; builds préliminaires : spécification v0.6.1 39 pages (pdf_qa PASS — 11 advisories typographiques hérités, non bloquants, classe consignée depuis D133) et Livre v1.1 26 pages (pdf_qa PASS, mêmes advisories) ; attendus au build final : verify_spec.py (spec_v061) cahier V1–V15 TOUT PASSÉ, empreintes CONSIGNÉES PAR LE BUILD (D134) au tableau de bord et au journal, reproductibilité des archives intacte.

## D138 — LA LECTURE VIRTUALISÉE EST AVEUGLE (quatrième instance consignée) : un fichier présent sur le disque hôte peut être vu VIDE depuis la VM — le verdict se rend sur les PIÈCES HOST, le rc du producteur fait foi, la vue in-VM reste un diagnostic (jamais un verdict)

**Le fait (run v6, 03/11).** Le scénario v6 a relu `page-d2b.txt` DEPUIS la VM : la pièce portait le marqueur complet sur le disque hôte (T2b rc=0, 200 OK, 279 o) et la lecture in-VM l'a vue vide — l'étiquette produite « ECHEC … rc=0 » était auto-contradictoire et a nommé S2 À TORT ; le labo a renversé sur pièces host (T2b seul PASS → S3). C'est la QUATRIÈME instance du mécanisme : v2/v3 (la ligne « en ecoute » sur le disque à +1 s, vue 0 octet), v6 (page-d2b), v6 (T2b). **Le complément d'arrêt.** La capture ExitCode est aveugle par ailleurs : AUTORITE-B a quitté PROPREMENT (« arret propre — motif=delai » dans sa pièce) alors que le rc capturé restait vide ; AUTORITE-A lancée avec `--arret-apres 1` n'a jamais arrêté (0 requête servie → le compte n'atteint pas 1 → WaitForExit(30000) → Kill), même mécanisme de capture. **La règle v7.** Le rc du PRODUCTEUR fait foi (les lectures T2a/T2b/T3 passent au rc) ; le marquage des pièces se fait au labo sur les pièces host ; la vue in-VM est un diagnostic additive (jamais une entrée d'échec).

## D139 — LE FICHIER hosts EST IGNORÉ PAR LA RÉSOLUTION DANS LA VM (hosts relu présent + flushdns, « Hôte inconnu » quand même) : le contournement IP LITTÉRALE tient et demeure ; la piste du service Dnscache (Client DNS) est nommée et instrumentée (T6 additif v7)

**Le fait (deuxième exécution).** `hosts-lu.txt` prouve le fichier posé ET relu ; `ipconfig /flushdns` exécuté ; l'appel `GetHostAddresses('autorite.test')` rend néanmoins « Hôte inconnu ». La résolution du nom dans la Sandbox ignore le fichier hosts, mécanisme inconnu à ce stade. **Le contournement (inchangé).** L'origine IP littérale `https://127.0.0.1/` + les fixtures v5 à SAN iPAddress:127.0.0.1 suppriment TOUTE résolution amont — le chemin décisif ne dépend pas de D139. **L'instrumentation (v7, T6).** `Get-Service Dnscache` + `ipconfig /all` consignés aux preuves (`dnscache.txt`, `ipconfig-vm.txt`) : si Dnscache est arrêté/défaillant dans la Sandbox, hosts n'est consulté par PERSONNE — le mécanisme sera nommé sur pièces. Diagnostics ADDITIFS : rien n'entre dans les échecs ni les réserves.

## D140 — RÉSOLU (branche S3 — la révocation hors ligne) : la poignée du proxy 0.5.0 appelle AcquireCredentialsHandleW avec pAuthData = NULL (credentials Schannel PAR DÉFAUT, contrôle de révocation inclus) ; hors ligne l'état de révocation est INCONNU → la poignée avorte sans alerte AVANT toute classification → 502 générique héritée, JAMAIS « certificat rejete » ; la correction 0.5.1 retire le contrôle (SCH_CREDENTIALS explicite, dwFlags = 0)

**La matrice qui tranche (run v6, host, producteurs fermés).** T2a (curl strict par IP 4443) : rc=60 `CERT_TRUST_REVOCATION_STATUS_UNKNOWN` — sans réseau, CertGetCertificateChain ne peut pas établir la révocation. T2b (+ `--ssl-no-revoke`) : **rc=0, 200 OK, marqueur `TRIADE-M5B-PAGE-200` complet** — la chaîne est validée dès que la révocation est retirée (hRootStore = NULL est le magasin machine, prouvé). T3 (par nom, `--resolve`) : même rc=60 → S1 (nom/hôte) ÉLIMINÉ. T5 (certificat autonome, port 4444) : rc=60 `CERT_TRUST_IS_UNTRUSTED_ROOT` → S2 ÉLIMINÉ — le juge DISCRIMINE les défauts ; l'ordre est prouvé : la confiance échoue et SE SIGNALE dès que la révocation n'est plus le bloqueur. **Le mécanisme nommé.** pAuthData = NULL (arg 5, [rsp+0x20] — erratum E1 : le `xor r9d,r9d` @0x664E est pvLogonID) → credentials par défaut → contrôle de révocation inclus → hors ligne l'abort survient à mi-poignée SANS alerte TLS (SSLEOFError vu par l'autorité) → l'erreur (0x80092013, absente de la table tls-02) tombe dans le verdict 6 générique → 502 « Passerelle inaccessible » 40 o héritée M3, sha256 4eac2836… identique v4/v5/v6. **La correction (jalon 0.5.1).** tls-05:R2 — SCH_CREDENTIALS explicite sur la pile (dwVersion = 5 [E3 : schannel.h], structure 0x48 o tout nul sauf dwVersion, dwFlags = 0 : AUCUN bit de révocation — l'équivalent --ssl-no-revoke ; trame 0x58 → 0x98 [E2 : alignement]) ; traducteur tls-02, réponse 502-cert 34 o, critères, fixtures, ports — INCHANGÉS. Pré-validation labo : harnais 22 + 53 + 69 PASS, oracle 560 cas / 0 écart, checklist guide §6 TOUT PASSÉ, build unique scellé par la cérémonie D87 (10 arbres verts, clé réelle). Le run v7 (VM isolée) EST le test de validation.

## D141 — RÈGLE PERMANENTE DE NOMMAGE ET D'ARCHIVAGE DES BUNDLES (demande du développeur, consignée fidèlement) : le numéro de version AU NOM du bundle, les anciennes versions ARCHIVÉES (jamais supprimées, jamais écrasées) à chaque livraison nouvelle — la racine de TRIADE-sauvegarde-git ne porte que la version courante

**La demande du développeur (03/11/2026, consignée fidèlement).** « règle permanente : ajoute le numéro de version au nom du bundle, et archive les anciennes versions quand une nouvelle est livrée ». **La règle.** Tout bundle d'historique git livré au coffre porte le numéro de jalon AU NOM (`triade-history-<jalon-proxy>.bundle` — ex. `triade-history-051.bundle` pour 0.5.1) ; à chaque livraison d'un bundle nouveau, les bundles antérieurs sont ARCHIVÉS dans le sous-dossier `archives-bundles` du dossier TRIADE-sauvegarde-git — jamais supprimés, jamais écrasés ; la racine ne porte que la version courante. **L'application immédiate.** `triade-history-051.bundle` (jalon 0.5.1, HEAD da68021) = courant à la racine ; `triade-history-050-f62711b.bundle` (état f62711b/D137, arbre m4 0.5.0) déposé dans `archives-bundles` — intégrité prouvée AVANT dépôt (md5 aab04f69… == coffre == copie labo). **La borne constatée (honnêteté).** L'original `triade-history.bundle` appartient au compte du développeur : le jeton relais ne peut ni le renommer ni le déplacer (HTTP 403 — lecture seule) ; il reste INTACT à la racine, son retrait éventuel est le geste du développeur ; l'archivage versionné est la copie déposée. **La portée.** Les bundles du dossier TRIADE-sauvegarde-git ; le dossier « test » demeure une file de livraison (l'historique vit dans les pièces de preuve — inchangé) ; la mécanique vit dans les scripts du labo (`archiver_bundles_anciens.py`, `miroir_maj_051.py`), hors arbres scellés — aucune clé, aucun arbre, aucun artefact touchés.


## D142 — L'INVITE DU PAREFEU N'EST PAS DÉCLENCHÉE PAR UN TRAFIC RÉSEAU : elle l'est par la MISE EN ÉCOUTE (bind) — le proxy scellé fait bind(0.0.0.0:25000) ; la boucle locale 127.0.0.1 est EXEMPTE des règles du parefeu ; le mécanisme « one-shot bloqué, jamais rejoué » est RÉEL au niveau connexion mais ne s'applique pas au M5-b (signature attendue rc=7/28, 10060/10061 — absente de toutes les pièces)

**La question de l'opérateur (03/11/2026, consignée fidèlement).** « concernant l'invite du parefeu, pourquoi elle apparait alors ? elle n'est pas déclenchée par un traffic reseau ? parce que si elle est déclenchée par un trafic ponctuel one shot et elle le bloque, il ne sera pas rejoué malgré une autorisation et ça peut mener à un echec ». **Le mécanisme nommé (sur le scellé du run).** L'invite « Le Pare-feu Windows Defender a bloqué certaines fonctionnalités de cette application » est déclenchée par la PREMIÈRE MISE EN ÉCOUTE d'un exécutable sans règle existante sur une adresse non boucle locale (notification d'écoute, `netsh advfirewall … inboundusernotification`) — par le bind, pas par un paquet. Sur le binaire EXACT du run v7 (proxy 0.5.1, sha256 fb41697ddde265ac… == temoin, extrait de m5b-kit-v7.zip) : `mov dword [rsp+0x20], 0xA8610002` (AF_INET + htons(25000)) + `mov dword [rsp+0x24], 0x00000000` (INADDR_ANY = 0.0.0.0) puis socket(2,1,6) → bind(fd, 0x10) → listen(fd, 8) — l'écoute porte sur TOUTES interfaces : dès cet appel, AVANT tout paquet, l'invite sort. PREUVE PAR L'ABSENCE : la VM n'a AUCUNE interface réseau (`ipconfig-vm.txt` — ipconfig sans une seule carte, Networking=Disable du .wsb) et l'invite apparaît quand même. Les autorités écoutent strictement 127.0.0.1 (journaux : « adresse=127.0.0.1 port=443 ») — une écoute boucle locale ne provoque pas l'invite ; SEUL le proxy (0.0.0.0) invite. **La portée du mécanisme one-shot (le risque décrit est réel — ailleurs).** Sans règle, le SYN entrant réseau est jeté silencieusement (pas de RST) ; un client one-shot timeout et n'est PAS rejoué ; autoriser après coup crée la règle mais ne rejoue rien. SIGNATURE ATTENDUE : échec au niveau CONNEXION — curl rc=7 « Failed to connect », rc=28 timeout, Winsock 10060/10061. Elle ne s'applique PAS au M5-b, pour trois faits sur pièces : (a) tout le trafic du run est 127.0.0.1→127.0.0.1 (sondes ; « requete servie — GET / depuis 127.0.0.1:49674 » ; curl « Trying 127.0.0.1:4443/4444 ») et le parefeu Windows n'applique PAS ses règles au trafic boucle locale — même « Annuler » sur l'invite ne bloque pas localhost↔localhost ; (b) les sondes post-démarrage PASS immédiatement (03:36:11 « connect 127.0.0.1:443 reussi », 03:36:12 « connect 127.0.0.1:25000 reussi », 03:36:19) — les écoutes étaient joignables sans aucune autorisation ; (c) TOUTE la matrice curl échoue au niveau TLS, pas connexion — un rc=60 PROUVE que le TCP s'est connecté et que le handshake a eu lieu (rc=60 ×3, rc=0 ×1) ; AUCUN rc=7/28/10060 dans aucune pièce. **La règle.** L'invite se consigne comme CONDITION DE RUN observée, sans effet sur le verdict (comme le WiFi public→privé) ; si un jour un échec porte la signature connexion (rc=7/28, 10060/10061), le diagnostic parefeu est NAMMÉ D'AVANCE (D142) et se rendra sur pièces ; l'éradication est COSMÉTIQUE et additive au scénario (pré-règle `netsh advfirewall firewall add rule dir=in action=allow program=C:\kit\proxy.exe`, ou `netsh advfirewall set allprofiles settings inboundusernotification disable` en tête de scénario) — le scellé D104/D87 n'est PAS retouché pour une cosmétique. **Frontières.** Aucun arbre scellé, aucun artefact, aucune clé touchés ; la preuve vit dans le désassemblage du binaire livré (capstone) et les pièces du run (`VERDICT-run-v7-parefeu-bind.txt` au labo et au coffre).


## D143 — ARCHIVAGE DE FIN DE RUN : tout ce qui n'est plus utile aux runs suivants est ARCHIVÉ dans /test, jamais jeté — la corbeille n'est pas un lieu d'archivage ; la règle est RÉTROACTIVE : la corbeille a été vérifiée et tout le contenu TRIADE jeté avant elle est restauré dans l'archive

**La demande de l'opérateur (03/11/2026, consignée fidèlement).** « archive tout ce qui n'est plus utile pour les runs suivant dans le dossier /test du drive quand un run est terminé (nouvelle règle), et vérifie la corbeille si j'ai pas jeté des trucs où l'archivage est recommandé. »

**La règle.** À la fin d'un run (verdict rendu) : (1) le dossier coffre `preuves-m5b` est DÉPLACÉ dans `/test/archives-preuves/preuves-run-<v>/` avec le verdict du run ; un `preuves-m5b` VIERGE (LISEZMOI-preuves.txt seul) est recréé pour le run suivant ; (2) les vagues consommées (kits, scénarios, LISEZMOI, guides, rapports, cérémonies et signatures consommées) sont déplacées dans `/test/archives-livraisons/vagues-m5b/` ; (3) la racine de /test ne porte plus QUE la vague courante, `corriger-wsb.bat`/`corriger-wsb.ps1` (utiles à CHAQUE run — le zip du kit ne les contient pas) et le dossier `preuves-m5b` vierge plus les deux dossiers d'archive ; (4) AVANT tout jet : une copie versionnée doit exister dans l'archive (D141 pour les bundles, D143 pour tout le reste) — la corbeille n'est jamais un lieu d'archivage ; (5) DÉDUPLICATION : un seul exemplaire par contenu (md5) est archivé ; les copies octet-identiques peuvent rester en corbeille (récupérables, valeur nulle). Un index (LISEZMOI-archives-preuves.txt, LISEZMOI-archives-livraisons.txt) documente chaque salle.

**L'application au run v7 (03/11, exécutée, recoupée).** `preuves-m5b` (29 pièces v7, id 1_uHSH3OX…) → `archives-preuves/preuves-run-v7/` + `VERDICT-run-v7-parefeu-bind.txt` (30 entrées recoupées par listing API) ; `preuves-m5b` recréé VIERGE (id 1TAIGoTW…, LISEZMOI-preuves.txt 301 o) ; vagues v6+v7 → `archives-livraisons/vagues-m5b/` (LISEZMOI-m5b-v6/v7.txt, scenario-m5b-v6/v7.ps1, m5b-kit-v6/v7.zip, GUIDE-patch-0.5.1-jalon-v7.txt, RAPPORT-chirurgie-0.5.1-labo.txt, paquet-ceremonie-v7.zip, signatures-I.txt CONSOMMÉE par le build 0.5.1) ; racine /test après coup = EXACTEMENT {LISEZMOI-m5b-v8.txt, m5b-kit-v8.zip, scenario-m5b-v8.ps1, corriger-wsb.bat, corriger-wsb.ps1, preuves-m5b, archives-preuves, archives-livraisons} (listing API recoupé, 8 entrées). Script : `cloture_d143_run_v7.py` (idempotent).

**La rétroactivité (la corbeille vérifiée, comme demandé).** Constat par l'API : 46 enfants jetés de /test ; les 5 autres dossiers du coffre (TRIADE-sauvegarde-git, Cérémonie, ARCHIVE, Tokens, archives-preuves) : ZÉRO enfant jeté. Tout le contenu TRIADE jeté avant la règle est RESTAURÉ dans l'archive (untrash PUIS renommage+déplacement) : `preuves-run-v5` (12 pièces, run 02/11 23:58Z, temoin 2 677 o, kit v5), `preuves-run-v4` (11 pièces, 02/11 19:02Z, temoin 2 569 o, kit v4), `preuves-run-v2-depot1/2/3` (les trois dépôts du run v2 du 02/11 18:33Z, kit v2, journaux 1 487/3 017/3 017 o — le témoin du run v2 n'a pas survécu) ; vagues v3–v5 (LISEZMOI-m5b-v3/4/5.txt, scenario-m5b-v3/4/5.ps1, m5b-kit-v5.zip 11 250 349 o, m5b-kit-pret-a-jouer.zip 11 247 733 o, ancien LISEZMOI-KIT-M5B.md 7 095 o) ; salle `terrain-17/` (LISEZMOI-terrain17e→h, superviseur-terrain17d→h — UN exemplaire par md5 distinct, temoin_m4a : 4 contenus DISTINCTS 640/40/13/13 o, terrain_20261029_07h→11h50 ×6, demo_journal : 2 contenus 410/150 o) ; `analyse-labo-2026-10-31-audit-triade.md` (audit S11 du corpus) COPIÉE dans `archives-livraisons/analyses-labo/` (l'original dort dans le dossier jeté `preuves-samu` — hors /test, NON touché : espace du développeur). RESTÉ EN CORBEILLE À DESSEIN : l'ancien dossier `preuves-m5b` du run v6 (id 1ByG_vBFFC… — sa copie archive `preuves-run-v6/` existe déjà, doublon refusé) ; les copies OCTET-IDENTIQUES des fichiers déjà archivés (demo_journal ×4, superviseur-terrain17e/g/h ×4, temoin_m4a 40 o ×2) ; 2 `oauth_token_relais.json` historiques (hors /test, jetons de sync — le relais VIVANT est dans Tokens/, rien n'a été imprimé). **Mécanique nommée** : l'API Drive refuse le PATCH combiné {trashed:false + parents} (HTTP 403, constaté) ; le contournement est DEUX PATCH — untrash seul, puis addParents/removeParents — mécanique consignée pour les gestes futurs. Script : `archiver_corbeille.py` (idempotent, déduplication md5).

**Frontières.** Aucun arbre scellé touché ; aucune clé ; le contenu de `preuves-samu` (hors /test) n'est ni restauré ni modifié ; les jetons ne sont jamais affichés ; la corbeille n'est PAS vidée (récupération toujours possible par le développeur) ; aucun artefact touché.

## D144 — LES SECRETS DE CARTE VIVENT AU COFFRE : toute graine générée y est déposée dans le même geste ; un re-scelage de réparation à faits inchangés est licite sur constat nommé

**Le constat qui fonde la décision (04/11, « répare la 0.5.1 », Entrée 135).** La carte m4 génération 6 du scellé 0.5.1 était ORPHELINE : scellée au jalon v7 par un labo cloné du bundle (D140) où .keys/ n'existait pas, elle l'était sous une phrase et une graine GÉNÉRÉES par carte_m0.charger_secrets et mortes avec la sandbox — la phrase de la lignée D80 (coffre) ne la déchiffrait pas, le verrou anti-rollback passait silencieusement, et le verrou croisé R8 était inexécutable. Les graines précédentes avaient toutes péri de la même façon aux recyclages du labo (e842727c M0-M2, f40f8a20 m3/terrain, ad98a059 orpheline) : une graine qui ne vit qu'en .keys/ meurt à la première restauration, car .keys/ est gitignoré et ne traverse jamais un bundle.

**La règle.** (1) TOUTE génération de secret de carte (phrase comme graine) est DÉPOSÉE AU COFFRE dans le même geste — le labo ne crée plus jamais de secret non durable ; (2) après toute restauration, la relève se fait depuis le coffre (modèle D75 : importer puis obtenir --vers-fichier .keys/<nom>) : la phrase par l'entrée lignee-D80, la graine par l'entrée graine-ed25519-cartes (octets BRUTS 32 o, jamais d'hex, jamais de fin de ligne) ; (3) un re-scelage de RÉPARATION à faits strictement inchangés (modèle D80) est licite quand une carte vivante est orpheline — le constat est nommé, l'artefact est prouvé OCTET POUR OCTET inchangé, l'oracle est re-joué (le verdict inscrit est un verdict vérifié), et l'ancienne carte reste dans l'historique git ; (4) le scellage d'une NOUVELLE génération de carte reste un geste qui appartient au développeur (D87 inchangé) — la durabilité des secrets ne déplace pas la décision, elle la rend exécutable.

**L'application (04/11, exécutée, recoupée).** scripts/reparer_carte_051.py : sept gardes fail-closed (dont témoins croisés de la phrase D80 sur m3 génération 5 ET m4 D104, et l'authenticité de l'orpheline), image re-composée == scellé fb41697d… (R7), oracle D93 re-joué (560 cas verts, graine 20261104), scellement sous D80 vérifié EN MÉMOIRE avant la seule écriture, verrou croisé 49 empreintes, post-vérifications P1-P4 dont LE REFUS de l'anti-rollback (« carte scellée (0.5.1) : reconstruction interdite ») — le verrou mort est revenu vivant. La graine neuve (pub e9cd8c549485…) est déposée au coffre : entrée TRIADE/graine-ed25519-cartes, conteneur 1906 o md5 23a2987a9817…, racine du coffre Drive recoupée par relecture, export download/.

**Frontières.** L'artefact 0.5.1 n'a pas bougé d'un octet ; l'arbre m4/I et le sceau intouchés (onze verts avant/après) ; l'orpheline conservée dans l'historique git ; le coffre ne perd aucune entrée (2 intactes + 1 ajout) ; la clé du sceau du développeur jamais sollicitée.


## D145 — AUCUNE GARDE DE SCÉNARIO NE DÉPEND D'UNE LECTURE EN LIVE D'UN FICHIER EN COURS D'ÉCRITURE DANS LA VM : les gardes sont FONCTIONNELLES (port ouvert, réponse attendue) ou POST-MORTEM — D138 étendue aux gardes ; la preuve déclarative CONSTATE, la preuve opérative GARDE

**Le constat qui fonde la décision (04/11, run e2, Entrée 138).** Le scénario e2 a introduit la PREMIÈRE garde en live d'un fichier en cours d'écriture : attendre la ligne « relever-https arme » du journal proxy sous 20 s, AVANT le navigateur (REFUS PROXY-SANS-ARMEMENT sinon). Le run a été REFUSÉ sur cette garde — alors que les pièces établissent que l'armement AVAIT eu lieu : la sonde TCP réussit à 00:13:17 (l'écoute était posée, donc bannière et armement — qui la PRÉCÈDENT au contrat http-12:R3 Q3 — étaient déjà écrits, par UNE WriteFile PAR LIGNE, tcp-11 Q1, aucun tampon applicatif), et la pièce post-mortem (128 o) porte les 7 lignes complètes du run. La lecture (PowerShell, dans la VM) d'un fichier du dossier mappé C:\preuves dont le handle d'écriture appartient à un processus VIVANT rend ZÉRO octet — le contenu n'apparaît qu'à la fermeture du handle. C'est le MÊME symptôme que les « vues vides depuis la VM » des runs v7/v8 (réserves POIGNEE-B-REFUSEE : vues vides, producteur rc=0, pièces complètes jugées au labo — D138), troisième constat : v7, v8, e2. Le scénario v8 ne lisait le journal proxy qu'APRÈS le quit (verdicts post-mortem) : la garde en live du e2 était une RÉGRESSION de conception — le fail-closed précoce a fait son travail (refuser plutôt que prouver en vain), mais sur un instrument qui ne peut pas répondre.

**La règle.** (1) Toute garde fail-closed d'un scénario de run se fonde sur un état OBSERVABLE PENDANT le run : un PORT ouvert (sonde TCP) ou une RÉPONSE reçue (test fonctionnel) — JAMAIS le contenu d'un fichier en cours d'écriture par un processus vivant, quel que soit le dossier (mappé ou local : un buffer applicatif produit le même symptôme, v7/v8). (2) Les fichiers journaux sont jugés POST-MORTEM (après la mort du producteur — modèle v8 : verdicts après le quit) ou AU LABO sur pièces (D138 : le rc du producteur fait foi, les pièces host sont jugées au laboratoire). (3) La preuve DECLARATIVE (une ligne de journal) ne GARDE rien — elle CONSTATE ; la preuve OPÉRATIVE (une réponse qui traverse la chaîne exigée) GARDE.

**L'application (la correction e3, proposée à l'Entrée 138).** La garde d'armement devient FONCTIONNELLE : le scénario envoie par TCP au mandataire la requête forme-absolue CLAIRE du navigateur (« GET http://127.0.0.1/ HTTP/1.1 » + Host) et attend la page 200 de l'autorité A — relèvement http→https + tunnel + réponse = preuve OPÉRATIVE que le proxy est ARMÉ (un binaire non armé routerait vers l'origine port 80, muette : 502) ; REFUS PROXY-PAS-ARME nommé sinon ; la page reçue copiée en pièce. La ligne « relever-https arme » devient un VERDICT post-mortem (après le quit — modèle v8).

**Frontières.** La règle ne touche AUCUN scellé (elle régit les scénarios de run, livrables du labo) ; le critère (b) de D136 reste ce qu'il est (la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR — la sonde fonctionnelle est une GARDE, jamais une preuve du critère navigateur) ; le phénomène intime de la vue vide (couche du dossier Sandbox ou buffer applicatif) n'est pas tranché — la règle s'applique aux DEUX mécanismes connus.


## D146 — AUCUN SCELLAGE rc/final SANS UN CONTRÔLE D'EXÉCUTION FULL-PE À LA BASE RÉELLE DE L'IMAGE : l'émulation à base 0 n'est pas un témoin de l'exécution réelle — un RVA nu y résout par accident ; le contrôle exécute une requête routée SERVIE (ou nomme le crash) avant que la carte ne se scelle

**Le constat qui fonde la décision (04/11, run e3, Entrée 141).** Le proxy scellé 0.6.0-rc.1 est MORT sur la première requête routée jamais reçue (la sonde d'armement du run e3) : la ligne de flux — code entièrement nouveau M5 — lit le couple (RVA, longueur) de la table des méthodes dans .rdata et passe le RVA NU comme pointeur à la copie ; sur Windows (image à 0x140000000) la lecture à 0x24A0 est une violation d'accès qui tue le processus. L'idiome hérité (http-02:R1 : « mov edx, dword [table] ; add rdx, r12 » avec r12 = base d'image) avait été PERDU dans la révision. OR tout le corpus avait jugé ce code VERT : l'oracle différentiel D136 (200 cas du domaine relevé, la ligne de flux octet par octet), les harnais de révision, la conformité § 8.2 — parce que TOUTE l'émulation M5 mappe l'image À BASE 0 (RVA = adresse) : le RVA nu y est une adresse mappée VALIDE, le défaut y est INVISIBLE PAR PRINCIPE. La conformité lit le PE sans l'exécuter ; les oracles exécutent les blocs à base 0. Aucun contrôle n'exécutait jamais l'image À SA BASE RÉELLE.

**La règle.** (1) Avant TOUT scellage rc ou final d'un artefact proxy, un CONTRÔLE D'EXÉCUTION À LA BASE RÉELLE doit être VERT : l'image PE entière est chargée à sa base préférée (0x140000000), l'IAT remplie par la marche des descripteurs, la ligne de commande réelle passée, et AU MOINS UNE REQUÊTE ROUTÉE EST SERVIE EN ÉMULATION (requête → réponse au client, ou refus nommé du contrat) — le crash, s'il existe, est NOMMÉ (adresse, instruction, bloc) AVANT la carte. (2) Le harnais de ce contrôle est un LIVRABLE DU JALON, rejouable par script, aux côtés des oracles — le défaut du rc.1 a été attrapé par le sien (scripts/reproduire_run_e3.py, modèle emulation_forensique D52h : base relogée, IAT marchée, fils coopératifs par CreateThread, sockets scriptées). (3) La preuve chirurgicale reste disponible à tout doute : le correctif SIMULÉ au crochet (jamais dans le binaire) qui fait renaître la chaîne isole la cause mieux qu'un diff.

**Frontières.** La règle s'applique aux GESTES DE SCELLAGE futurs (elle ne reconstruit rien a posteriori) ; elle ne remplace NI les oracles différentiels (la logique), NI la conformité § 8.2 (la structure) — elle couvre l'angle mort des deux : l'adressage RÉEL de l'image chargée ; elle n'exonère pas le run terrain (le critère (b) de D136 reste le juge du relèvement PAR LE NAVIGATEUR) ; l'émulation reste des API SHIMMÉES (winsock, secur32) — le contrôle constate l'adressage et le chemin de session, pas la vraie Schannel.


## D147 — LA LICENCE DE RECONSTRUCTION D'UN SCELLÉ FAUTIF EST EXACTEMENT LE SAUT DE PRÉ-VERSION MINIMAL (rc.1 → dev.2 → rc.2, modèle D35) ET LE CONTRÔLE D146 DEVIENT EXIGENCE MÉCANIQUE DU GESTE DE SCELLAGE : la règle vit au code du build, pas au souvenir de l'agent

**Le constat qui fonde la décision (04/11, Entrée 142 — le chemin rc.2 accompli).** Le scellé 0.6.0-rc.1 était fautif (le crash du run e3, D146) : le corriger exigeait de reconstruire l'artefact, or l'anti-rollback (R6) interdit toute reconstruction sous balise scellée — le verrou fait bien son travail, mais la règle de gestion du correctif devait être ÉCRITE avant que le cas ne se représente, pas improvisée. Le précédent existait : D35 (M3, le rc.1 de la 0.3.0 fautif IAT) avait déjà tranché le modèle — correctif à contrat stable (R4), la lignée avance d'exactement un saut de pré-version, la cristallisation repart à zéro, le scellé fautif vit à l'historique JAMAIS reconstruit.

**La règle.** (1) LICENCE EXCLUSIVE : l'amendement de l'anti-rollback autorise UNE reconstruction précise, nommée en clair au code (build_m5._anti_rollback, dict LICENSE à une entrée : {« 0.6.0-rc.1 »: « 0.6.0-dev.2 »}) — motif constaté (l'Entrée qui nomme le défaut), version cible supérieure STRICTEMENT (R10 : 0x00060001 > 0x00060000), toute autre reconstruction sous balise scellée restant REFUSÉE fail-closed. (2) LA CRISTALLISATION DU CORRECTIF REPART À ZÉRO : dix passages exigés avant le scellage du rc corrigé (R6 — un correctif n'hérite pas des preuves du code fautif). (3) LE CONTRÔLE D146 EST EXÉCUTÉ PAR LE SCELLAGE MÊME : _sceller appelle le contrôle base réelle AVANT la bascule de balise et REFUSE tout scellage non vert — la règle D146 cesse d'être une consigne de conduite, elle devient une garde du build (fail-closed : l'agent ne peut pas l'oublier). (4) Le sha du scellé fautif reste consigné au code (SHA_PROXY_060_RC1) en mémoire du refus — il n'est JAMAIS reconstruit, l'historique git le porte.

**Alternatives rejetées.** Réécrire le scellé rc.1 en place (rejeté : une balise scellée est immuable § 9 — le verrou anti-rollback est la garantie d'existence de la lignée, le réécrire c'est le détruire) ; sauter directement à rc.2 sans dev.2 (rejeté : la reconstruction produit une pré-version DEV qui doit vivre ses preuves — oracles, cristallisation — AVANT d'être candidate ; le modèle D104/D35 sépare la construction de la candidature) ; laisser le contrôle D146 au bon vouloir de l'agent (rejeté : la leçon du rc.1 est précisément qu'un contrôle absent du geste est un contrôle qui n'existe pas — D145 avait fait ce chemin pour les gardes de scénario, D146 le fait pour le scellage).

**Frontières.** La licence couvre le SAUT MINIMAL, pas une permission générale : reconstruire encore sous rc.2 exigera une NOUVELLE décision nommée (la garde l'exprime : « procedure lourde R6 ou nouvelle version X.Y.Z+1 requise ») ; elle ne touche NI les cartes des jalons clos (m0-m4 : leurs verrous restent absolus), NI l'arbre d'intention (le correctif rc.2 s'est fait À CONTRAT STABLE — m5/I inchangé, le sceau-I reste valide) ; le kit terrain suit la vague (D143) : la vague consommée est archivée, jamais jetée ; le run terrain reste le juge du critère (b) de D136 — la licence répare le binaire, elle ne valide rien.


## D148 — LES VERDICTS DE SCÉNARIO SE RENDENT POST-MORTEM ET SUR PIÈCES : le rc « producteur » d'un verdict ne doit JAMAIS être le rc d'un processus à capture aveugle, et la preuve navigateur d'une page d'erreur vit À LA RÉCEPTION (jamais au DOM headless d'une 502 nue) — D138/D145 portées aux verdicts par le run e4 ; la matrice curl S3 est l'état stationnaire de la VM (jamais une régression du proxy)

**Le constat qui fonde la décision (04/11, run e4, Entrée 143).** Le scénario e3-==-e4 a rendu « ÉCHEC NOMMÉ (5) » alors que les pièces établissent le critère (b) de D136 PRÉSENT : les CINQ refus sont des artefacts d'instrument, dont QUATRE procèdent d'une SEULE cécité — le rc d'Edge capturé VIDE (la capture ExitCode est aveugle dans cette famille de VM, constat v6/complément d'arrêt D138). Le mécanisme : le helper Verdict-Vue prévoyait une branche RÉSERVE pour les « vues vides » — « producteur rc=0 — pièce à confirmer au labo » — mais son témoin de producteur était le rc d'EDGE, vide : la réserve devint ÉCHEC (AUTORITE-A-SERVIE, POIGNEE-B-REFUSEE), le rc vide fit échouer NAVIGATEUR-A/B, et le DOM vide du run B (Edge headless n'émet NI DOM NI CAPTURE pour une navigation échouée) fit nommer DOM-B-INVALIDE. Deux des ÉCHEC étaient des RÉSERVES prévues, transformées par un témoin aveugle.

**La règle.** (1) AUCUN verdict de scénario ne se rend sur une lecture EN LIVE d'un journal dont le producteur VIT (D145 étendue des gardes AUX VERDICTS) : les journaux se jugent POST-MORTEM (après la mort du producteur — le modèle v8 des verdicts proxy, après le quit) ou AU LABO sur pièces (D138). (2) LE TÉMOIN DE PRODUCTEUR d'un verdict (le rc qui distingue RÉSERVE d'ÉCHEC) doit être le rc d'un processus à capture FIABLE dans la VM — JAMAIS un rc connu aveugle (Edge, les autorités dans cette famille : le rc du PROXY par console capture, lui, est fiable) ; à défaut de rc fiable, la branche est la RÉSERVE (la pièce tranche au labo), jamais l'ÉCHEC. (3) LA PREUVE NAVIGATEUR D'UNE PAGE D'ERREUR vit À LA RÉCEPTION : une 502 NUE (ligne de statut sans corps — TXT_502_CERT 34 o, design M5 depuis 0.5.1/D140) échoue le chargement Chromium avec ERR_HTTP_RESPONSE_CODE_FAILURE et le headless n'émet alors ni DOM ni capture — le DOM-B-502 (grep « 502 » au DOM) est STRUCTURELLEMENT INSATISFIABLE sur ce build pour notre 502 ; la réception se prouve par le RECROISEMENT de producteurs indépendants : la ligne de flux servie (s=34) + l'événement nommé au journal proxy (« certificat rejete ») + la poignée refusée au journal autorité + l'erreur réseau du navigateur lui-même (ERR_HTTP_RESPONSE_CODE_FAILURE : elle n'existe QUE si le code d'erreur HTTP fut reçu). (4) LA MATRICE CURL : la branche S3 (révocation hors ligne de CURL, CERT_TRUST_REVOCATION_STATUS_UNKNOWN strict vs --ssl-no-revoke) est L'ÉTAT STATIONNAIRE de la VM (v6, v8, e4 : pièces identiques octet pour octet) — D140 concernait les credentials DU PROXY (preuve : le tunnel du run A s'établit hors ligne), jamais curl ; le libellé « RÉGRESSION à nommer » des scénarios e2-e4 (écrit en attendant S4) est une expectation périmée, à corriger à la prochaine vague de scénario.

**Alternatives rejetées.** Faire du verdict du scénario une autorité sur le run (rejeté : c'est le renversement exact de D138 — la vue in-VM est un diagnostic, JAMAIS un verdict ; l'instrument ne peut pas se juger lui-même) ; donner un corps à la 502 pour la rendre visible au DOM (rejeté : TXT_502_CERT est un fait SCELLÉ de la lignée 0.5.1→0.6.0, 34 octets exacts — modifier une réponse du scellé pour un caprice d'instrumentation serait la pire des inversions) ; capturer le rc d'Edge par un mécanisme contourné (rejeté au labo : SANS Windows sous la main, un contournement non testé serait une foi nouvelle dans un instrument non prouvé — la règle (2) rend le problème MOOT : on ne câble plus un témoin aveugle).

**Frontières.** La règle régit les SCÉNARIOS DE RUN futurs (livrables du labo, jamais un scellé) ; elle ne rétro-écrit PAS le scénario e3-==-e4 (la vague e4 est archivée avec ses libellés — le présent verdict juge sur pièces, c'est le modèle) ; le critère (b) de D136 reste ce qu'il est (la page servie ET la 502 reçues PAR LE NAVIGATEUR — la réception triplement recoupée fait foi, le rendu de la page d'erreur reste une réserve INSTRUMENTALE nommée, démontrable seulement par un navigateur fenêtré) ; la finale 0.6.0 est posée sur la validation consignée (Entrée 143) — la règle ne la remet pas en cause, elle en documente le chemin de preuve.


## D149 — LE PLAN DES JALONS M6/M7 : les fiches de profil complètes naissent AVANT le premier octet, le corpus nominal M6 est RESTREINT et NOMMÉ, le chantier M5-(c) est REPORTÉ au M6-(d) (explicite, jamais silencieux) — et les constats labo sont DATÉS

**Le contexte qui fonde la décision (04/11, « ok, on enchaine »).** Le jalon M5 est rentré (balise 0.6.0 scellée, validation terrain consignée — Entrée 143, D148) et le worklog annonçait « les jalons M6/M7 attendent leur plan » : le présent geste écrit ce plan. Il n'est pas une page blanche : l'échelle d'auto-hébergement (D34) vit déjà sur le profil `x86-64-linux-elf64` (hachoir `m6/` échelon 1, sceau `m7/` échelon 2 phase 1 — ELF64 écrit à la main, exécuté nativement au labo) ; le jalon M6 porte la PARITÉ du patrimoine M0–M5, pas la re-création de la chaîne. Trois constats labo fondent le plan et sont DATÉS du 04/11/2026 : keystone 0.9.2 ne porte PAS l'architecture RISC-V ; capstone 5.0.7 désassemble RV64 (constaté sur octets) ; aucun binaire qemu-riscv64 dans le bac à sable.

**La règle.** (1) **Aucune instanciation de profil sans fiche complète écrite et vérifiée** (les sept éléments + le huitième livrable anti-rollback, spécification § 16, manuel § 2 : « jamais d'instanciation approximative ») — les fiches `docs/PROFIL_x86-64-linux-elf64.md` et `docs/PROFIL_riscv64-linux-elf64.md` naissent AVANT le premier octet des jalons, constats datés et re-vérifiés au chantier qui les touche. (2) **Le corpus nominal M6 est restreint et nommé** : les SEPT blocs purs libc-01..07 + libc-08 autotest + tcp-07 (moteur de patch) + tcp-11 (journal) + les DEUX contrats d'interface (révisions formelles de hello-02/hello-03) + un principal propre au jalon — le serveur écho complet de M2 (contrats tcp d'interface socket) est une extension OUVERTE à la demande du développeur, jamais une réduction silencieuse : le critère § 18-M6 (diff nul, même oracle, parité) se démontre sur le corpus nominal. (3) **La voie du diff nul est la révision de granularité des contrats** : arguments nommés dans la couche I, convention d'appel déplacée vers frag-con (spécification § 8.3-4) — invariance des octets Windows ASSERTÉE (les scellés ne bougent pas), sceau de l'Intention suivi pour les arbres I modifiés ; le diff nul se mesure PAR SCRIPT (les instances des deux profils chargent les MÊMES fichiers I). (4) **Le chantier M5-(c) (patch à chaud du journal en production) est reporté au chantier M6-(d)** : le critère sera démontré sur le profil Linux, moteur tcp-07 instancié et EMBARQUÉ (bascule pendant le trafic, rollback, zéro régression) — le report est consigné au plan, à la spec et au présent journal. (5) **Convention de dossiers** : le jalon M6 vit dans `unix/`, le jalon M7 dans `riscv/` ; les noms `m6/` et `m7/` demeurent ceux de l'échelle d'auto-hébergement D34 (emprunt de nommage consigné — le plan ne le défait pas). (6) **Balises** : M6 → 0.7.0 (rc.1 puis finale après run terrain vert), M7 → 0.8.0 ; le scellage rc/final exécute le CONTRÔLE D146 ADAPTÉ : exécution full-ELF à la base réelle (l'image PIE chargée par le noyau à base aléatoire — un pointeur nu y meurt exactement comme sur le terrain, l'émulation à base fixe reste interdite comme témoin unique). (7) **L'ordre M6 puis M7 isole les variables** (D14) : l'OS à ISA constante, puis l'ISA — le MÊME corpus sera instancié trois fois depuis la même couche I.

**Alternatives rejetées.** Instancier un profil sans fiche complète (rejeté : le manuel § 2 en fait un refus de build — « un profil incomplet est un refus de build, exactement comme une carte manquante ») ; porter le corpus réseau complet de M2 au jalon M6 (rejeté : le coût des contrats socket ne sert pas le critère § 18 — le corpus restreint le démontre, l'extension reste un chantier ouvert) ; abandonner le chantier M5-(c) (rejeté : le critère § 18-M5 l'exige — le report au profil Linux le referme avec le moteur embarqué, mieux que le superviseur Windows ne le permettait) ; exécuter M7 avant M6 (rejeté : D14 isole chaque variable — le mécanisme des profils avant l'indépendance d'ISA) ; dupliquer les contrats purs par profil au lieu de la révision de granularité (rejeté : la duplication tuerait le diff nul, la preuve que « l'intention vit dans I et pas dans les octets ») ; compter sur keystone pour le RISC-V (rejeté : le constat labo est formel — l'assembleur RV64 maison ou un moteur tiers passé à la même porte, capstone restant le juge unique du round-trip).

**Frontières.** Les fiches de profil et le programme M6/M7 sont des LIVRABLES DU PLAN (jamais des scellés — aucune balise n'est posée par la présente : la 0.7.0-dev.1 viendra du premier build M6) ; les décisions développeur attendues (terrain M6 : WSL2 recommandé ou VM Linux isolée ; terrain M7 : qemu-riscv64 avec réserve instrumentale nommée ; aval du report M5-(c)) sont NOMMÉES au plan et non bloquantes pour le démarrage de M6-(a) ; l'état des jalons de la spécification v0.6.1 est mis à jour (M0–M5 franchis, M6/M7 ouverts — le PDF se régénère par le mécanisme établi D17/D134, empreinte consignée PAR LE BUILD) ; l'écart D81 du PHRASE-CONTROLE-COFFRE.txt de la racine Drive (nommé au Task 60 : 59 o, 3 lignes, ouverture impossible) est FERMÉ au même geste (phrase seule 33 o, identique à la remise du dépôt, ouverture du coffre VERT — coffre INTÈGRE, jamais muté).


## D150 — LA TABLE ERRNOS EST MOTIVÉE PAR BLOC, ET L'ÉTAT QUI TRAVERSE DES APPELS VIT EN MÉMOIRE : le contrat d'erreurs du jalon suit la discipline I1 des numéros de syscall (une entrée = un bloc qui la déclare, la table grandit par révision) ; un état qui doit survivre à des appels vit en .bss ou en non-volatil sauvegardé — jamais en registre volatile (r8/r9 meurent dans les blocs de travail, r11 dans chaque syscall)

**Le constat qui fonde la décision (04/11, chantier M6-(a), Entrée 145).** Deux faits du build de la sonde, tous deux attrapés par les gardes AVANT tout vert :
(1) la leçon C1 a fonctionné EN DIRECT : le symbole @L_FATAL portait 36, le message réel en fait 37 (le saut de ligne final laissé hors du compte de l'auteur) — verifier_symboles a REFUSÉ le build : l'arithmétique de l'auteur est vérifiée par la machine, jamais crue ;
(2) le premier sous-programme .emit plaçait le préfixe (r8) et la longueur (r9) en registres volatils, puis appelait su-03 (le verdict) : su-02 et su-03 clobber r8/r9 comme registres de travail, et chaque syscall de su-01 détruit r11 — le préfixe et le verdict MOURAIENT au premier appel (l'exécution rendait deux lignes au lieu de quatre : la première émission du .emit écrivait à une adresse doublée, rendait EFAULT, et le flux tombait silencieusement dans l'arrêt fatal). L'oracle natif a REFUSÉ fail-closed — jamais un faux vert : c'est exactement le comportement que D146 exigeait du scellage, ici au niveau du build.

**La règle.** (1) **TOUTE entrée de la table ERRNOS (et de ses sœurs par profil) est MOTIVÉE PAR BLOC** : une entrée existe parce que le contrat d'un bloc la déclare (au M6-(a) : EBADF par su-04:E1, la sonde du descripteur) ; la table grandit par RÉVISION au chantier qui déclare de nouveaux errno attendus — jamais par caprice, jamais par avance : le miroir exact de la discipline I1 des numéros de syscall (tout numéro non motivé est un refus de build → toute entrée non motivée est un refus de build ; tout errno hors table est VERDICT_FATAL, arrêt propre nommé — le fail-closed n'est pas négociable). (2) **UN ÉTAT QUI DOIT TRAVERSER DES APPELS VIT EN MÉMOIRE (.bss) ou en non-volatil sauvegardé — JAMAIS en registre volatile** : r8/r9 (et leurs équivalents par ABI) sont les travailleurs d'UN appel, r11 (et ses équivalents) meurt dans CHAQUE syscall — la mémoire, elle, traverse tout ; le verdict de la sonde vit au tampon +32 (TAMPON_NUM), le brut traverse en r10 (registre de travail interne que ni su-01, ni su-02, ni su-03 ne touchent), les arguments du sous-programme (r8/r9) sont consommés AVANT le premier appel. (3) **La sortie d'un artefact de démonstration PORTE son verdict final en code de sortie** (la sonde : code 6 = VERDICT_FATAL constaté — la branche fatale est terminale PAR CONTRAT, la démonstration des deux branches est complète à la première exécution).

**Alternatives rejetées.** Pré-remplir la table d'errno plausibles (rejeté : une entrée non motivée est un mensonge en attente — le fail-closed exige que SEUL le déclaré soit nommé, tout le reste est fatal) ; sauvegarder l'état par push/pop de non-volatils dans le sous-programme (rejeté : plus lourd que le tampon .bss déjà exigé par le formatage hex, et la pile du _start n'a pas de cadre d'appelant — le réflexe resterait registre-centré, la règle veut le réflexe mémoire) ; compter sur l'ordre pratique des clobbers (« r8 survit à su-03 en l'occurrence ») (rejeté : la pratique d'un appel n'est pas un contrat — les specs déclarent les volatils détruits, le code y croit ; M7 en héritera, a0-a7 tous volatils en psABI LP64, AUCUNE zone rouge).

**Frontières.** La règle régit les tables de contrat d'erreurs et les plans de registres des blocs des jalons M6/M7 (héritage de méthode) ; elle ne touche NI la table HRESULTS du primaire (D79 — le profil Windows demeure), NI les octets des scellés Windows (invariance ASSERTÉE par D149), NI le hachoir m6/ (l'échelle D34 garde ses propres idiomes) ; la sonde est un DEV (balise 0.7.0-dev.1 POSÉE, jamais scellée — le scellage 0.7.0-rc.1 viendra du chantier (c) avec le contrôle D146 adapté, la garde anti-rollback n'existe pas encore : un DEV vivant se reconstruit librement).


## D151 — ABSENT ≠ ILLISIBLE (une carte présente et indéchiffrable est un REFUS, jamais une permission) ; L'INSTRUMENT DE MUTATION NOMME SON GESTE (jamais un poser nu) ; LA FALSIFICATION EST EXHAUSTIVE PAR INSTRUCTION (un résidu de registre ne guérit plus rien) ; UN BLOC HORS-CHEMIN est épuisé par SON scénario, ET L'ENTRANT CONCURRENT PORTE SES ENTRÉES LOCALES — chaque refus traversé au chantier fonde sa règle écrite au code du build

**Le constat qui fonde la décision (04/11, chantier M6-(b), Entrée 146 — le geste interrompu à 14:40, repris et conduit jusqu'au vert).** Le corpus paritaire a traversé SES REFUS un à un, chaque refus nommé (fail-closed, jamais un faux vert) fondant une correction puis la présente règle :
(1) l'incident de l'état zéro : `m1/build_m1.py` lancé SANS argument a tourné — la garde de l'ère m1 traite « carte illisible » comme « absente » (`except ErreurCarte: pass`) et échoue OUVERTE ; selftest.exe est resté OCTET-IDENTIQUE, la carte m1 régénérée a été RESTAURÉE octet-pour-octet depuis git — le constat structurel est né : TOUTES les gardes m1→m5 (l'ère D147 comprise) échouent ouvertes sur carte illisible ;
(2) le SEGFAULT MUET de l'autotest : `img.poser` écrivait une page R sans ouverture — l'oracle est mort en silence au lieu de refuser ;
(3) « libc-08 falsifié : N=19 » : la fixture SC sert les DEUX sens (v6 inférieur memcmp(SA,SC)<0, v7 supérieur memcmp(SC,SA)>0) — l'oracle croyait « +1 devient 0 », la notation constatait DEUX verdicts perdus : l'attendu est corrigé SUR PIÈCES ;
(4) le SEGFAULT DÉTERMINISTE du journal (tcp-11:R2) : `add r12, rax` placé APRÈS le `call @A_MEMCPY` — memcpy rend dst (UNE ADRESSE, Q2 de son contrat), jamais la longueur : le compteur de longueur recevait une adresse géante et le suffixe sortait du mapping ; ET le staging (journal v2) portait LE MÊME PIÈGE — le remplaçant est corrigé AVANT d'être embarqué (il aurait crashé au chantier (d) dès un appel réel avec champ) ;
(5) « tcp-11 concurrence : verdicts divergents » : la cartouche n'était pas ré-entrante — entrées, sorties, sauvegarde de pile et pages PARTAGÉES entre threads : deux appels simultanés s'écrasaient mutuellement ;
(6) « libc-06 PASSÉ SILENCIEUX » : la mutation de la première instruction était « guérie » par un RÉSIDU DE REGISTRE (lea r8 muté, le store [r8] tombait encore sur le curseur — r8 résiduel de l'appelant) ;
(7) « tcp-07 : 78 mutations TOUTES silencieuses » : tcp-07 est HORS-CHEMIN du principal (corpus-13 ne l'appelle pas — la démonstration du patch est le chantier (d)) : AUCUNE corruption d'un bloc non exécuté ne peut dévier l'artefact, c'est un FAIT DE PLAN.

**La règle.** (1) **ABSENT ≠ ILLISIBLE** : une carte (ou toute pièce d'état) PRÉSENTE et indéchiffrable est un REFUS, jamais une permission — `build_corpus.py` distingue les deux dès sa naissance ; le correctif des cinq chaînes historiques (m1→m5) est un geste SÉPARÉ nommé pour le développeur, aucune urgence (les cartes m1→m4 sont des scellés d'archives, seule m5 vit sous la phrase du jour). (2) **L'INSTRUMENT DE MUTATION NOMME SON GESTE** : ouvrir mprotect RW, écrire, RESTAURER la protection trouvée ; en mode partagé : refus nommé — jamais un poser nu (le segfault est un refus muet, la pire espèce). (3) **UNE ADRESSE RENDUE N'EST JAMAIS UNE LONGUEUR** : la longueur se capture AVANT l'appel qui détruit son support volatile (memcpy rend dst, Q2 — l'add déplacé AVANT le call) ; le staging remplaçant est vérifié par le MÊME oracle AVANT d'être embarqué. (4) **L'ENTRANT CONCURRENT PORTE SES ENTRÉES LOCALES** : entrées LOCALES à l'appel, sommet attribué PAR APPEL sous un verrou court (pas 0x800), fenêtre de sorties par appel [sommet-0x200, sommet-0x1B8] — sous la profondeur d'imbrication maximale (corpus-13 → autotest/journal → feuilles), les cadres imbriqués n'y touchent jamais. (5) **LA FALSIFICATION EST EXHAUSTIVE PAR INSTRUCTION** : un bloc est rompu dès qu'une mutation dévie — un résidu de registre ne guérit plus rien ; l'attendu d'une falsification se corrige SUR PIÈCES (le différentiel des DEUX sens de la fixture). (6) **UN BLOC HORS-CHEMIN est épuisé par SON scénario** (tcp-07 : apply/rollback/effet, intégrité staging code 3, refus code 5) et par le V7 DEP EN FILS (la constante RWX 0x7 mutée en 0x3 : la page du code devient R+W sans X, le RET du patch lui-même faute — SIGSEGV constaté en fils, le père observe, le fils meurt : le code défaillant ne tue jamais l'instrument) ; le travailleur d'un test TERMINE ses lignes (le journal émet ce qu'on lui donne — son contrat), la fenêtre de scan d'un immédiat couvre le slot entier (0x60 → 0x200 : l'immédiat vit à +0x6e).

**Alternatives rejetées.** Considérer l'illisible comme absent (rejeté : c'est exactement le trou par lequel la garde s'éteint — l'échec ouvert de l'ère m1 est le constat, la règle le ferme) ; muter l'image sans nommer le geste mprotect (rejeté : le poser nu est un segfault muet — un échec qui n'enseigne rien) ; guérir une falsification par un résidu de registre (rejeté : le silence d'une mutation est un faux vert — l'exhaustivité par instruction est la seule mesure) ; compter tcp-07 dans le chemin du corpus-13 (rejeté : la démonstration du patch est le chantier (d) ; un fait de plan se NOMME, jamais ne se force) ; la ré-entrance par pages partagées et sommet fixe (rejeté : deux appels simultanés s'écrasent mutuellement, les verdicts divergent — l'instrument ment) ; corriger le journal v2 au chantier (d) (rejeté : le remplaçant embarqué aurait crashé dès le premier appel réel avec champ — un staging se vérifie AVANT l'embarquement).

**Frontières.** La règle régit les instruments de test et les chaînes de build des jalons (garde d'état, mutation, falsification, concurrence) ; elle ne touche NI les octets des scellés Windows (invariance ASSERTÉE par D149, mesurée par `diff_nul.py` à chaque build), NI le hachoir m6/ (l'échelle D34 garde ses propres idiomes), NI la table ERRNOS (D150 demeure) ; le corpus est un DEV (balise 0.7.0-dev.2 POSÉE par geste de BUILD, jamais scellée — le scellage 0.7.0-rc.1 viendra du chantier (c) avec le contrôle D146 adapté, la garde anti-rollback n'existe pas encore : un DEV vivant se reconstruit librement, le plancher demeure 0.7.0-dev.1).


## D152 — LA BASE SE CONSTATE, ELLE NE SE DÉCRÈTE PAS (le témoin ptrace/maps à l'arrêt d'exec) ; UN TÉMOIN D'EXÉCUTION SE PROUVE FALSIFIABLE SUR LA CLASSE EXACTE DU DÉFAUT QU'IL GARDE (le mutant « RVA nu ») ; UN ALLOCATEUR PAR DÉCRÉMENT-RESTITUTION N'EST PAS UN ALLOCATEUR SOUS CONCURRENCE (le sommet est PAR FIL) ; UNE CHAÎNE DE RE-VÉRIFICATION PRÉSERVE LA BALISE SCELLÉE — le chantier M6-(c) : la conformité constatée, le D146 adapté exécuté au scellage même, les gardes vivantes

**Le constat qui fonde la décision (05/11, chantier M6-(c), Entrée 147 — la suite de conformité + le scellage 0.7.0-rc.1).** Quatre constats du geste fondent la règle :
(1) LA BASE SE CONSTATE : le contrôle D146 adapté (`unix/controle_base_reelle.py`) exécute l'image PIE par le NOYAU et lit la base de chargement dans /proc/<pid>/maps À L'ARRÊT D'EXEC garanti par PTRACE_TRACEME — 6 bases distinctes sur 6 exécutions, la MÊME base deux fois sous ADDR_NO_RANDOMIZE (personality, le mécanisme de setarch -R) : l'ASLR est un CONSTAT du noyau, jamais une croyance du contrôle (la sonde du chantier (a) émettait SA base ; le contrôle du jalon la LIT depuis le noyau — deux témoins indépendants de la même vérité) ;
(2) LA FALSIFIABILITÉ PORTE SUR LA CLASSE : le témoin d'exécution se prouve en tuant un mutant de LA CLASSE EXACTE du défaut qu'il garde — le « RVA nu » (le lea rip réécrit mov edi, <rva> : l'adresse sans la base, le geste de la ligne de flux qui tua le 0.6.0-rc.1 au run e3) meurt NOMMÉ (SIGSEGV à l'adresse nue, RIP rapporté au bloc du plan par la plage EXACTE de son slot) — en base aléatoire ET en base figée ; une mutation quelconque prouve la sensibilité, une mutation DE LA CLASSE prouve la GARDE ;
(3) L'ALLOCATEUR : à la cristallisation, refus intermittent (~1/11) « tcp-11 concurrence : verdicts divergents » — la chasse (240 essais instrumentés) a nommé la signature (rax = la longueur d'une AUTRE ligne) puis la cause : l'allocateur de sommets de la cartouche (décrément à l'entrée, restitution au retour) est un bump-LIFO que l'ordre de restitution INTERFOLÉ rompt — un fil libère, le plafond remonte sur le sommet d'un appel VIVANT, deux appels partagent la fenêtre et la pile ; D151 avait rendu la FENÊTRE par appel, le SOMMET restait à recouvrement — le sommet est désormais PAR FIL (attribué une fois, réutilisé en séquence dans son fil, JAMAIS restitué : la restitution interfolée était la faille) ; le bloc sous test était EXONÉRÉ : l'instrument mentait, pas le code ;
(4) LA BALISE : verifier() régénérait frag-bld avec la version EN DUR — après un scellage, toute re-vérification aurait REVERTI la balise scellée ; la re-vérification lit désormais la balise du manifeste et re-signe la carte SOUS elle (un scellé ne se revertit pas par la porte de la vérification).

**La règle.** (1) TOUT témoin d'exécution à la base réelle CONSTATE la base depuis le noyau (ptrace/maps à l'arrêt d'exec, ou l'émission par l'artefact lui-même) et recoupe le figeage (ADDR_NO_RANDOMIZE) — jamais une base décrétée, jamais une seule méthode. (2) TOUT témoin d'exécution chargé de garder une classe de défaut prouve sa falsifiabilité SUR CETTE CLASSE (le mutant de la classe, mort nommé) — la classe du défaut gardé est NOMMÉE au contrôle. (3) SOUS CONCURRENCE, aucune ressource n'est attribuée par décrément-restitution : l'attribution est PAR FIL (ou par pool de slots libres) — une LIFO à restitution interfolée est un recouvrement en attente ; l'instrument fautif n'invalide pas le code sous test (l'exonération se constate sur pièces), mais son refus fail-closed reste le seul mode (un faux vert de l'instrument est un faux vert du jalon). (4) UNE CHAÎNE DE RE-VÉRIFICATION ne déplace JAMAIS une balise : elle re-signe la carte sous la balise courante ; le registre des versions acceptées (plancher 0.7.0-dev.1) refuse toute balise hors lignée ; le scellage bascule la balise une fois, avec le contrôle D146 exécuté AU geste même (D146/D147 demeurent). (5) Le scellage rc/final vérifie l'artefact INTACT par sha constant — le scellage est un fait de carte, un écart d'artefact est un refus.

**Alternatives rejetées.** Décréter la base (rejeté : « 6 bases distinctes » sans témoin est une croyance — la sonde du (a) et le contrôle du (c) la constatent chacun à leur manière) ; prouver la falsifiabilité par une mutation quelconque (rejeté : la classe du défaut gardé est la seule preuve que la GARDE garde — un octet inversé prouve la sensibilité, pas la garde) ; garder l'allocateur par décrément en verrouillant toute la durée de l'appel (rejeté : tuer la concurrence réelle pour sauver l'instrument, c'est ne plus tester la concurrence — le sommet par fil préserve le VRAI parallélisme) ; blâmer le bloc journal sur le refus intermittent (rejeté : la signature l'exonérait — l'instrument se prouve fautif sur pièces AVANT que le code ne soit touché) ; permettre à la re-vérification de régénérer la balise dev (rejeté : la porte de la vérification deviendrait la porte de déscellement — silencieuse qui plus est).

**Frontières.** La règle régit les témoins d'exécution, les instruments concurrents et les chaînes de re-vérification des jalons ; elle ne touche NI les octets des scellés (l'artefact corpus est INTACT à travers le scellage — sha dd14195c…, un fait de carte), NI la porte R10 du corpus (la table d'intégrité et ses qwords de garde demeurent — D146/D147/D151 inchangées), NI le déroulé (d) (le --sceller-final attend le run terrain vert, l'exigence porte « validation terrain consignée »). Le scellé 0.7.0-rc.1 est POSÉ : immuable § 9, défaut → X.Y.Z+1 à contrat stable (R4), anti-rollback vivant (re-scellage et reconstruction refusés sur pièces).


## D153 — LE FLUX MESURÉ N'EST À PERSONNE (la narration de l'instrument ne vit JAMAIS sur le canal capturé — elle est différée à la sortie de la fenêtre) ; UN LIVRABLE TERRAIN NE SE DÉPOSE QUE S'IL EST VERT À L'EXTRACTION VIERGE (l'épreuve par extraction + run complet au labo, partie du montage — jamais une confiance en la construction) ; L'INSTRUMENT DU TERRAIN EST CELUI DU LABORATOIRE, RECOUPÉ OCTET POUR OCTET (le gabarit relocalisable à fixup unique, assemblé à adresse factice HAUTE)

**Le constat qui fonde la décision (05/11, chantier M6-(d), Entrée 148 — la démonstration M5-(c) + le kit terrain Linux).** Trois constats du geste fondent la règle : (1) LA PREMIÈRE ÉPREUVE DU KIT A ÉCHOUÉ NOMMÉ — le scénario terrain imprimait sa narration sur fd 1, le canal même que la capture détourne vers le tube : 102 octets de narration se sont retrouvés DANS le flux mesuré (T2a : « 14 992 o émis != 14 890 attendus »), et un fragment de narration littéral dans le trafic de l'ouvrier (T2b) ; le défaut était DANS L'INSTRUMENT (le scénario), pas dans l'artefact — et l'assertion octet-pour-octet l'a nommé au premier passage (un instrument tolérant l'aurait tu : le vert muet est l'espèce refusée). Le jumeau de laboratoire (demo_patch.py) était vert parce qu'il COLLECTIONNE ses constats et ne les imprime qu'à la fin — la différence entre les deux instruments ÉTAIT la leçon ; (2) C'EST L'ÉPREUVE PAR EXTRACTION VIERGE qui a attrapé le défaut — pas la construction, pas la compilation, pas l'inspection : le kit tel que le développeur l'exécuterait (dossier neuf, `python3 scenario-m6d.py`), rejoué au labo AVANT tout dépôt ; (3) LA CARTOUCHE EMBARQUÉE : le terrain n'assemble rien (aucune dépendance instrumentale au terrain — keystone/capstone restent au labo), mais un gabarit assemblé À BASE 0 aurait produit la forme imm32 TRONQUÉE du `mov r11, .retour` (inutilisable pour toute vraie adresse mmap) : le gabarit est assemblé à une ADRESSE FACTICE HAUTE (0x100000000000 — la forme imm64 est FORCÉE), recoupé contre l'instrument VIVANT de l'oracle octet pour octet, et relogé au terrain par UN fixup imm64 unique posé AVANT le mprotect RX.

**La règle.** (1) TOUT instrument qui mesure un flux par détournement de canal (capture fd 1, tube, socket) interdit à SA PROPRE narration de vivre sur le canal mesuré : la narration est différée à la sortie de la fenêtre de capture (ou vit sur un autre canal) — le flux capturé n'appartient qu'au producteur mesuré, et l'assertion octet-pour-octet demeure le juge (tout écart se nomme, jamais ne se tolère). (2) TOUT livrable terrain (kit, scénario, conteneur) n'est DÉPOSÉ au coffre que s'il est VERT À L'EXTRACTION VIERGE + RUN COMPLET au laboratoire — l'épreuve est une ÉTAPE DU MONTAGE (l'assembleur la conduit et refuse le dépôt sur échec), jamais une vérification optionnelle d'après-coup ; l'idempotence du montage garantit que le kit reconstruit est le kit éprouvé. (3) L'INSTRUMENT EMBARQUÉ au terrain est RECOUPÉ contre l'instrument du laboratoire OCTET POUR OCTET (la même source, assemblée au labo, vérifiée contre l'instrument en vie — puis relogée au terrain par le fixup minimal NOMMÉ) : le terrain exécute l'instrument du labo, jamais une réécriture ; le gabarit est assemblé à une adresse qui FORCE l'encodage complet (imm64), jamais à la base 0. (4) L'EMPREINTE du kit déposé est recoupée au coffre (md5 affiché par le passeur, vérifié avant le dépôt) — le kit au coffre EST le kit éprouvé, un écart est un refus.

**Alternatives rejetées.** Déposer le kit sur la confiance de la construction (rejeté : la première épreuve a échoué NOMMÉ — la preuve vivante que la construction ne suffit pas) ; tolérer les écarts mineurs du flux capturé (rejeté : « 102 octets de plus » est une narration dans le flux mesuré — l'instrument qui s'écoute n'entend plus le mesuré) ; embarquer keystone au terrain pour assembler la cartouche sur place (rejeté : le terrain n'installe RIEN — la cartouche pré-assemblée + fixup unique recoupée octet pour octet est le MÊME instrument sans dépendance) ; assembler le gabarit à base 0 (rejeté : keystone y émet la forme imm32 — tronquée pour toute vraie adresse mmap, le défaut serait latent jusqu'au crash du run développeur) ; faire vérifier l'épreuve par le développeur (rejeté : le terrain n'est jamais le premier témoin d'un livrable — le labo prouve, le terrain recoupe).

**Frontières.** La règle régit les instruments de mesure par capture de canal, le montage et le dépôt des livrables terrain ; elle ne touche NI l'artefact scellé (INTACT — sha dd14195c…, le patch est un fait de session), NI la suite de conformité (qui exécute la démonstration sur SON propre canal — la collecte différée y vit déjà), NI le déroulé du run développeur (le scénario déposé est le scénario éprouvé — le terrain recoupe, le labo a prouvé). Le kit m6d est DÉPOSÉ au coffre /test (md5 67b85983…) : la vague courante, le run VERT sur pièces posera la finale 0.7.0 (le jalon M6 franchi — l'exigence « validation terrain consignée » demeure, D149/D152 inchangées).


## D154 — LE TERRAIN D'UN KIT FAIT PARTIE DE SON CONTRAT (hors terrain : mort nommée AVANT tout geste — jamais un faux vert d'environnement, jamais une « portabilité » qui tuerait la preuve) ; LE VERDICT DU LABO SUR UN RUN TERRAIN SE REND SUR PIÈCES CROISÉES (témoin ↔ journal ↔ verdict recoupés ENTRE EUX, l'arithmétique RECOMPTÉE, les constats vérifiés CONTRE LA SOURCE, le noyau CONSTATÉ distinct, l'artefact RECALCULÉ au geste même) ; L'INSTRUMENT DE RECOUP EST LUI-MÊME SOUPÇONNABLE (un ÉCHEC NOMMÉ du recoup s'instruit comme défaut d'instrument AVANT d'être un défaut de pièces — corrigé sur pièces, rejoué, les pièces immuables)

**Le constat qui fonde la décision (05/11, run M6-(d) + scellage final 0.7.0, Entrée 149).** Quatre constats du geste fondent la règle : (1) LE PREMIER GESTE DU DÉVELOPPEUR A MORT NOMMÉE HORS TERRAIN — le kit lancé sous Windows natif (`c:\m6-kit> python scenario-m6d.py`) est mort à l'ouverture de `libc.so.6`, AVANT T0, avant toute pièce, avant tout geste sur l'artefact : le fail-closed du kit tient MÊME HORS DE SON TERRAIN (un environnement faux ne produit ni faux vert ni preuves partielles), et la correction est LE TERRAIN NOMMÉ (WSL2, la recommandation D149 suivie), jamais une « portabilité » du scénario — sous Windows il n'y a ni ELF, ni mprotect, ni refus EACCES à constater : la preuve du (d) EST le noyau Linux qui parle ; (2) LE RUN VERT SUR UN NOYAU AUTRE — 6.18.54.1-microsoft-standard-WSL2 (la machine du développeur) contre 5.10.134… (le labo), l'ASLR complet constaté (randomize_va_space=2), le scellé relu dd14195c… avant tout geste : la vigilance D146 satisfaite PAR LE TÉMOIN, pas par la parole ; (3) LE RECOUP SUR PIÈCES CROISÉES — vingt-deux contrôles : les pièces recoupées entre elles (le témoin embarqué au journal == le fichier témoin ; les 16 constats du verdict == les 16 PASS du journal LIGNE POUR LIGNE ; la date du verdict == la date du témoin), l'arithmétique RECOMPTÉE (800 + 400 == 1 200 ; 778 + 560 == 1 338 ; indices 0..1337 exacts ; octets émis == attendus), les noms des constats vérifiés CONTRE LA SOURCE du scénario (le juge est le code), le sha du scellé RECALCULÉ au geste même depuis l'artefact du dépôt ; (4) LE PREMIER RECOUP A ÉCHOUÉ NOMMÉ — « C4 : divergence au rang 0 » : le défaut était DANS L'INSTRUMENT DU RECOUP (la comparaison des préfixes avait ses arguments inversés : l'attendu testé startswith du constat lu, au lieu du constat lu startswith de l'attendu) — la lignée D151/D152 (« l'instrument mentait, pas le code ») s'étend au RECOUP lui-même : l'instrument est corrigé sur pièces et REJOUÉ, les pièces n'ont pas bougé d'un octet ; le second passage : VERT 22/22.

**La règle.** (1) UN KIT TERRAIN DÉCLARE SON TERRAIN (le LISEZMOI le nomme, l'exigence fait partie du contrat du kit) : hors terrain, la mort est NOMMÉE avant tout geste — le kit ne se « porte » JAMAIS à un environnement qui ne porte pas sa preuve ; une demande de portage d'un kit hors de son terrain est une demande à instruire (un refus nommé, un kit sibling), jamais une correction du kit prouvé. (2) LE VERDICT DU LABO SUR UN RUN TERRAIN SE REND SUR PIÈCES CROISÉES, JAMAIS SUR CONSOLE : présence et md5 des pièces contre le coffre ; cohérence croisée témoin ↔ journal ↔ verdict ; RECOMPTE arithmétique de chaque compteur ; noms des constats contre la SOURCE du scénario ; noyau du témoin CONSTATÉ distinct de celui du labo ; empreinte de l'artefact RECALCULÉE au geste même. Le scellage final n'est exécuté qu'après ce recoup VERT : la porte est de PROCESSUS (le code exige déjà D146 + cristallisation + conformité — D147/D152 ; ce que seul le terrain produit, seul le recoup l'établit). (3) L'INSTRUMENT DE RECOUP EST LUI-MÊME FAILLIBLE ET DOIT L'AVOUER : un ÉCHEC NOMMÉ du recoup s'instruit comme défaut d'INSTRUMENT avant d'être un défaut de pièces (la correction se fait dans l'instrument, le rejeu le prouve, les pièces demeurent immuables — md5 contrôlés de part et d'autre) ; le recoup ÉCRIT son verdict à côté des pièces (VERDICT-recoup-*.txt — la pièce née du juge). (4) La balise finale est SCELLÉE sur le recoup vert, au terme de la MÊME chaîne que le rc — jamais sur la seule parole du run : le terrain juge, le labo recoupe, le code scelle.

**Alternatives rejetées.** Sceller sur le copier-coller console du développeur (rejeté : D145/D148 — le verdict est post-mortem SUR PIÈCES, la console n'est pas une pièce) ; rendre le scénario portable Windows (rejeté : le kit déclare son terrain — la preuve du (d) est le noyau Linux qui refuse EACCES, un shim la tuerait) ; exiger le même noyau que le labo (rejeté : l'exigence est l'AUTRE noyau — D146, la leçon du rc.1 : un vert sur le noyau du labo ne prouve pas le terrain) ; tolérer un écart de compte dans les pièces (rejeté : chaque compte se RECOMPTE — un vert approximatif est un faux vert) ; réécrire ou « nettoyer » les pièces pour les faire passer le recoup (rejeté : les pièces sont immuables, md5 contrôlés ; c'est l'instrument qui se corrige et se rejoue) ; instruire l'échec du recoup comme un échec du run sans rejeu (rejeté : l'instrument mentait, pas les pièces — le rejeu l'établit sur pièces).

**Frontières.** La règle régit les kits terrain (leur terrain déclaré), les runs développeur (leurs pièces) et le recoup labo (son instrument et son verdict) ; elle ne touche NI l'artefact scellé (INTACT — sha dd14195c…, le scellage est un fait de carte), NI le scénario déposé au coffre (le scénario éprouvé demeure, le terrain le rejoue tel quel), NI la chaîne de scellage (D147/D152 demeurent : le code exige D146 + cristallisation + conformité AVANT la bascule — la présente ajoute la porte de processus : le recoup vert PRÉCÈDE l'appel à --sceller-final), NI le PDF formel (byte-identique — l'état des jalons vit aux sources de travail, addendum Task 62). La finale 0.7.0 est SCELLÉE sur le run m6d recoupé VERT (Entrée 149) : LE JALON M6 FRANCHI, le jalon M7 ouvert (D149).

## D155 — LE MOTEUR DE NOTATION D'UN PROFIL NEUF PASSE LA MÊME PORTE QUE LE PRIMAIRE, ET LA PREUVE EST LA DIRECTION INVERSE (l'assembleur maison — ou tiers — n'est admis que si le rendu INTÉGRAL du juge ré-assemble en ses octets : le corpus de textes ne suffit JAMAIS, c'est l'espace d'ENCODAGE légal qui fait la preuve) ; LE JUGE DÉBORDE L'AUTEUR (le désassembleur rend plus de pseudos que l'auteur n'a d'habitudes — chaque écart attrapé par la porte est une leçon consignée, jamais un avertissement) ; UN EXÉCUTEUR ÉMULÉ SE PREUVE PAR SES PARAMÈTRES, JAMAIS PAR UN ASLR ÉMULÉ (la base d'une image PIE invitée sous qemu-user est CONSTANTE — un constat d'instrument NOMMÉ ; l'indifférence à la base se DÉMONTRE par des bases forcées du CHARGEUR, la preuve ne doit dépendre d'aucun aléa de l'instrument)

**Le constat qui fonde la décision (05/11/2026, chantier M7-(a), Entrée 150).** Trois constats du geste fondent la règle : (1) **LA DIRECTION INVERSE EST LA PREUVE** — la porte round-trip du jalon a été construite en deux directions : AVANT (783 textes du corpus du profil : assemble → désassemble → ré-assemble) et INVERSE (1037 encodages légaux de l'espace RV64IMA+Zifencei : champs f7/f3 exhaustifs, shamt exhaustifs, décalages de bord, les 225 couples de fence — le rendu du juge ré-assemble en ses octets) ; les QUATRE défauts de l'assembleur maison (le pseudo `negw` manquant, le funct7 de SEPT bits des décalages W, la forme deux-opérandes mémoire de `jalr`, la frontière « unknown » des champs fence vides) ont TOUS été attrapés par la direction inverse — aucun par la direction avant : un corpus de textes écrit par l'auteur ne prouve que ce que l'auteur a prévu ; (2) **LE JUGE DÉBORDE L'AUTEUR** — capstone rend `mv` pour addi imm=0, `sext.w` pour addiw imm=0, `beqz` pour beq rs2=x0, `jal` à UN opérande (ra implicite), `negw` pour subw x0 — la graphie canonique de la notation est CELLE DU JUGE (le modèle du jalon unix, généralisé : l'identité exigée est sur les OCTETS, jamais sur la graphie) ; (3) **L'ÉPREUVE DES BASES FORCÉES A MORT NOMMÉE À SA PREMIÈRE FORME** — sous qemu-riscv64 10.0.13, la base par défaut de l'image PIE invitée est CONSTANTE (0x555555556000 au labo, constatée sur 6 exécutions : qemu-user ne randomise PAS l'image invitée), et `-B` (guest_base) seul est SANS effet sur l'adresse d'image ET_DYN : deux configurations -B distinctes rendaient la MÊME base — l'instrument a été INSTRUIT SUR PIÈCES avant d'être contourné (le levier du chargeur est `-R`, la fenêtre de réservation VA) ; trois configurations forcées VERTES (0x2aaac000 / 0xaaaac000 / 0x55556000) démontrent l'indifférence à la base PAR LES PARAMÈTRES DU CHARGEUR.

**La règle.** (1) TOUT moteur de notation d'un profil neuf (maison ou tiers) passe LA MÊME PORTE que keystone au primaire : le round-trip à 100 % avec le juge du profil (capstone), EXIGÉ EN DEUX DIRECTIONS — le corpus de textes du profil ET l'espace d'encodage lébal parcouru systématiquement (champs d'encodage exhaustifs par famille, immédiats et décalages de bord) ; toute entrée de l'espace légal que le juge décode doit ré-assembler en ses octets — la direction inverse EST la preuve, la direction avant n'est qu'un échauffement. (2) La graphie canonique de la notation est TOUJOURS celle du juge (l'auteur peut écrire addi, la notation porte mv — l'identité WYSIWYG est sur les octets) ; chaque écart attrapé par la porte est CONSIGNÉ comme leçon (jamais un avertissement silencieux, jamais une tolérance locale). (3) Un exécuteur émulé (qemu-user) est un INSTRUMENT dont les comportements se CONSTATENT et se NOMMENT — jamais des hypothèses : la randomisation (ou non) de la base invitée, l'effet (ou non) des options, se vérifient SUR PIÈCES avant d'entrer dans une épreuve ; quand l'aléa fait défaut, la propriété (l'indifférence à la base) se démontre par les PARAMÈTRES DU CHARGEUR (bases forcées), jamais en feignant l'aléa — une preuve ne doit dépendre d'AUCUN aléa de l'instrument. (4) L'échec nommé d'une épreuve s'instruit comme DÉFAUT D'INSTRUMENT avant d'être un défaut d'artefact (la lignée D151/D152/D154) : l'épreuve est corrigée sur pièces et rejouée, l'artefact n'a pas bougé d'un octet.

**Alternatives rejetées.** Admettre l'assembleur sur la seule direction avant (rejeté : les quatre défauts du chantier étaient invisibles de cette direction — un corpus écrit par l'auteur ne prouve que les prévisions de l'auteur) ; tolérer localement les pseudos non rendus par l'assembleur (rejeté : le juge est juge unique — un rendu inassemblable est un échec de build, jamais un avertissement) ; compter sur l'ASLR émulé de qemu pour la preuve PIE (rejeté : la base invitée est CONSTANTE sous qemu 10 — un vert à base constante ne prouve RIEN de l'aléa, et n'a pas à : la propriété à prouver est l'INDIFFÉRENCE à la base, pas la variété) ; dater l'option -B comme levier sans l'éprouver (rejeté : l'épreuve a mort nommée — l'option est sans effet sur l'image ET_DYN, instruit sur pièces) ; rendre la preuve dépendante du tirage aléatoire du jour (rejeté : les bases forcées du chargeur déterminent l'épreuve — la preuve est rejouable à l'identique).

**Frontières.** La règle régit les moteurs de notation des profils neufs (leur porte d'admission), la graphie canonique des notations (le juge tranche) et les épreuves d'exécution sous émulateur (leurs constats d'instrument et leurs bases forcées) ; elle ne touche NI le juge du primaire (keystone/capstone x86-64 — le round-trip R5 demeure), NI la chaîne de scellage (D147/D152 : le scellage 0.8.0-rc.1 exigera le contrôle D146 adapté à l'exécuteur du jalon — l'image PIE exécutée sous qemu à des bases constatées et forcées), NI la réserve instrumentale D149 (elle demeure NOMMÉE dans chaque verdict : l'ISA est exécutée par TCG, le noyau et les syscalls sont réels, jamais déguisés en exécution native). L'assembleur maison as_rv64 (riscv/outils/as_rv64.py) est admis par la porte du chantier : 783 + 1037 à 100 % (Entrée 150).

## D156 — LA FENÊTRE D'UNE ZONE SE POSE À SA PORTÉE (l'ancre .bss vit AU CENTRE de la zone, jamais à sa base : la portée imm12 est une CONTRAINTE DE PLACE du plan — un accès hors plage est un REFUS NOMMÉ de l'assembleur, jamais un adressage absolu de repli) ; UN REGISTRE EST DÉDIÉ PAR RÔLE, JAMAIS RECYCLÉ (la fenêtre s3 de tcp-07 n'est pas l'ardoise de tcp-11 : l'oracle structurel attrape le recyclage au premier passage) ; L'AMO ADRESSE [rs1] SANS DÉPLACEMENT (le champ imm12 n'existe pas dans le format AMO — une demande de déplacement est un REFUS NOMMÉ, jamais un octet silencieux : le déplacement vit dans la formation addi, déclarée) ; LA PORTE S'ÉTEND AVEC L'INSTRUMENT (l'extension A du profil entre à la porte du jalon au geste qui l'exige : la couverture se démontre, elle ne se décrète pas)

**Le constat qui fonde la décision (05/11/2026, chantier M7-(b), Entrée 152 — le corpus paritaire RV64, la TROISIÈME instanciation de la même couche I).** Quatre leçons du geste, toutes attrapées par les gardes au PREMIER passage (aucune corrigée à la main : l'instrument a tranché, la notation a suivi) : (1) **LA LEÇON imm12** — le verrou du journal (0x3800) vu de l'ancre .bss posée à la BASE de la zone (0x3000) vit à +0x800 = 2048 : HORS imm12 DE UN — le premier `amoswap.d t2, t0, 0x800(s2)` a rendu le REFUS NOMMÉ d'as_rv64 (« hors plage imm12 [-2048, 2047] — l'accès lointain passe par une ancre ») ; la fenêtre s'est posée AU CENTRE de la zone (s2 = base + 0x3400) : le curseur à -0x400, l'arène à -0x3C0, le verrou à +0x400 — tout dans ±2047 ; (2) **LE PIÈGE AMO** — l'ISA AMO adresse [rs1] SANS déplacement (funct5 occupe les bits 31:27, il n'y a PAS de champ imm12 dans ce format) : le premier jet de l'extension assemblait `amoswap.d rd, rs2, 0x400(s2)` en IGNORANT silencieusement le déplacement demandé (l'espèce la plus grave : un octet qui n'est pas celui demandé, sans le dire) — le refus a été posé (AMO sans déplacement ; le déplacement vit dans la formation `addi t2, s2, 0x400`, déclarée et vérifiée) ; (3) **LE RECYCLAGE DE REGISTRE** — s3 portait la fenêtre d'entrée de tcp-07 ET l'arithmétique de longueur de tcp-11 (`addi s3, s3, 4`) : l'oracle structurel a refusé la formation non déclarée (`s3+4 hors données déclarées`) — les rôles ont été dédiés (s1/s2 les fenêtres GLOBALES du corpus, s3 la fenêtre PRIVÉE de tcp-07, s0/s4-s7 les ardoises de travail sauvegardées, t1 le registre du projet, jamais touché) ; (4) **LA PORTE A GRANDI AVEC L'INSTRUMENT** — l'extension A du profil (amoswap.w/d, aq/rl nuls — le verrou tournant du corpus) est entrée dans as_rv64 ET dans la porte du jalon (AVANT 783 → 791 textes, INVERSE 1037 → 1045 encodages) : le claim « la porte couvre l'espace d'encodage légal du profil » est resté VRAI par le geste, pas par décret — les autres AMO (amoadd…) et aq/rl armés vivent hors instrument, la frontière est nommée.

**La règle.** (1) TOUTE fenêtre d'ancrage (paire auipc+addi) est une DÉCLARATION DE PLAN dont la PLACE est contrainte par la portée imm12 : le plan choisit le centre qui couvre la zone (tout déplacement dans ±2047), et la contrainte est PORTEE PAR LE PLAN (documentée au layout, mesurée par l'oracle) — un accès hors plage est un refus nommé de l'assembleur, JAMAIS contourné par un adressage absolu de repli (qui tuerait l'indifférence à la base, la propriété du profil). (2) Les registres sont DÉDIÉS PAR RÔLE dans la lignée : les fenêtres (s1/s2 globales, s3 privée à tcp-07) ne sont jamais des ardoises de travail — les ardoises vivent dans les autres non volatils (s0, s4-s11), sauvegardées dans le cadre ; le recyclage est attrapé par l'oracle structurel (la formation non déclarée), pas par la relecture. (3) Toute EXTENSION de l'instrument (une instruction, un format, une ISA-extension) entre AVEC sa couverture : la porte du jalon est étendue au MÊME geste (les deux directions), et le domaine exclu est NOMMÉ (frontière, jamais un silence) ; une extension qui ne passe pas la porte n'entre pas. (4) Un format d'encodage dont un champ N'EXISTE PAS (AMO sans imm12) REFUSE la demande du champ — jamais un octet silencieux : la valeur appartient à une formation déclarée ailleurs.

**Alternatives rejetées.** Poser l'ancre .bss à la base de la zone et étendre par des calculs absolus (rejeté : l'adressage absolu tuerait la position-indépendance — la fenêtre est le mécanisme du profil) ; tolérer le déplacement AMO en l'ignorant (rejeté : le premier jet l'a fait — c'est un octet qui n'est pas celui demandé, l'espèce la plus grave) ; recycler s3 entre la fenêtre et l'ardoise (rejeté : l'oracle l'a attrapé — les rôles dédiés se vérifient, ils ne se souviennent pas) ; étendre l'assembleur sans étendre la porte (rejeté : la couverture se démontre — 791 + 1045 aux DEUX directions, le claim sinon serait un décret) ; passer les autres AMO sous silence (rejeté : la frontière est nommée — amoswap seul, aq/rl nuls, le corpus n'en porte aucun autre).

**Frontières.** La règle régit les plans d'adressage des lignées RV64 (la place des fenêtres), la dédicace des registres (frag-con la porte), les extensions de l'instrument (la porte grandit avec le domaine) et les formats d'encodage à champs absents (le refus nommé) ; elle ne touche NI le mécanisme des paires (D155/C1 : le site et le LO relativement à SON auipc — inchangés), NI la garde anti-table-x86 (D149 : asm-generic, la parité est sémantique), NI le scellage (le contrôle D146 adapté à l'exécuteur viendra du chantier (c)). Le corpus paritaire RV64 (riscv/corpus, balise 0.8.0-dev.2, sha256 b34a7147…) est né sous ces règles : 12 blocs du patrimoine + corpus-13, la TROISIÈME instanciation de la même couche I (les MÊMES fichiers canoniques unix/I/ — chargés, jamais copiés), l'oracle qemu vert (rituel 6/6 les DEUX lignes octet pour octet, code 0 — la parité § 8.3 PAR EXÉCUTION ; bases forcées VERTES ; falsification 12/12 zéro silence), 1535 verrous structurels, la carte génération 1 au SIXIÈME sel.

## D157 — LE PORT D'UN BLOC EST ÉPROUVÉ PAR SON CHEMIN D'EXÉCUTION RÉEL, JAMAIS PAR SA SEULE LECTURE (l'équivalent RV64 du `mov rdx, rdi` de l'instance x86-64 — le marshalling des arguments du syscall — a été OUBLIÉ au port : tcp-07 passait à mprotect un a2 de débris, la page perdait son bit X et l'exécution FAUTAIT à l'instruction suivante ; le bloc se lisait parfaitement, il se traduisait en un crash — SEUL LE CHEMIN RÉEL le nomme) ; LA PREUVE D'UN CRASH SE MÈNE AU JOURNAL DE L'EXÉCUTEUR (QEMU_STRACE a nommé `PROT_READ|PROT_WRITE|PROT_SEM` : le prot reçu était 0xB, des débris — le strace de l'instrument est une PIÈCE, pas un diagnostic de confort) ; UN SOUS-PROGRAMME QUI APPELLE SAUVE ra (jal écrase le lien — la leçon sr-04 réapprendue : .dire appelait écrire puis rendait vers sa propre boucle) ; CE QUI TRAVERSE UN APPEL VIT EN NON VOLATIL — LA RÈGLE D150 SE RÉAPPREND À CHAQUE GESTE (l'attendu du trafic dans t0, mort au premier appel ; le t0 des refus, recalé deux fois)

**Le constat qui fonde la décision (05/11/2026, chantier M7-(c), Entrée 153 — la démonstration du patch fence.i).** QUATRE défauts d'instrument et d'artefact, tous nommés par les gardes ou par le journal de l'exécuteur, aucun par la relecture : (1) **LE PORT OUBLIÉ** — tcp-07:R4 (riscv) portait `.protger` qui reçoit la protection dans a0, la garde dans t2, assemble l'adresse et la longueur — et ne passe JAMAIS a2 au syscall : mprotect recevait un a2 de débris (0xB = READ|WRITE|SEM observé) ; la page 0x1000 perdait son bit EXÉCUTABLE, le fetch suivant faute (ACCERR) et l'invité mourait en SIGSEGV — LE BLOC SE LISAIT PARFAITEMENT (le structurel, le round-trip, 1537 verrous — tout vert), le crash ne vivait qu'au CHEMIN RÉEL : la démonstration (le demo du patch, 1200 usages) l'a nommé au premier apply ; le strace de l'exécuteur a donné la pièce (`PROT_SEM` — un prot qui n'existe dans AUCUN plan) ; la correction est UNE ligne (`mv a2, t2` — l'équivalent exact du `mov rdx, rdi` de l'instance x86-64), le corpus a été REBUILDÉ (sha ec343b4e… — l'ancien b34a7147… consigné à son époque demeure le record de ce qui fut) ; (2) **LA LEÇON D150 RÉAPPRISE DEUX FOIS** — l'attendu du trafic vivait dans t0 (un VOLATIL) : le premier appel au journal le détruisait, le verdict échouait (l'attendu est passé en s10, non volatil) ; puis le t0 des refus (comparé APRÈS l'appel qui le clobberait) — recalé avant chaque bne : LA RÈGLE EST LA MÊME, L'ESPÈCE CHANGE À CHAQUE GESTE — la garde est le contrat écrit AVANT (D150), la conformité est le re-calage ; (3) **.dire ET ra** — le sous-programme local .dire (l'impression) appelait écrire via jal puis `ret` : ra avait été écrasé par l'appel interne, le ret remontait vers sa propre boucle (bltz/ret en spin — le trace in_asm a nommé la boucle à deux instructions) : le sous-programme qui APPELLE sauve ra (la leçon sr-04, réapprendue au port — le cadre -16/+16 apparié) ; (4) **LES REPRODUCERS IMPROVISÉS SONT UN MARÉCAGE** — trois images roulées à la main pour « isoler le mprotect » ont crashé pour leurs propres défauts (paires mal calculées, prot hors plage) et ont failli faire nommer une réserve d'instrument qui N'EXISTAIT PAS : le mprotect invité fonctionne PARFAITEMENT sous qemu (RWX puis RX, D39 tenu) — l'isolement d'un défaut se mène SUR L'IMAGE DE LA FAMILLE (le builder), jamais sur une image roulée à la main.

**La règle.** (1) UN BLOC PORTÉ N'EST CONFORME QUE CHEMIN RÉEL EXÉCUTÉ : tout port d'un bloc d'une ISA à l'autre exige que le bloc soit EXERCÉ en exécution par au moins un scénario qui traverse son chemin complet (la lecture structurelle, le round-trip et les verrous ne prouvent QUE la graphie — le marshalling des arguments ne vit QUE dans l'exécution) ; un bloc jamais exécuté au labo est un bloc NON ÉPROUVÉ, sa conformité est une lecture, pas une preuve. (2) LE JOURNAL DE L'EXÉCUTEUR EST UNE PIÈCE : QEMU_STRACE (et le trace in_asm) s'archivent comme témoin quand un défaut se présente — le strace nomme les arguments RÉELS des syscalls (PROT_SEM n'est dans aucun plan : la pièce désigne le marshalling, pas le service). (3) TOUT sous-programme local qui effectue un appel interne sauve ra AVANT l'appel et le restaure avant son ret (jal écrase le lien — la leçon sr-04 est une règle de la FAMILLE, pas de la sonde seule). (4) LA RÈGLE D150 (jamais un volatile qui traverse) SE VÉRIFIE À CHAQUE GESTE PAR ÉCRITURE PRÉALABLE : le registre porteur d'un attendu est nommé DANS LE CONTRAT DU BLOC (s10 ici), jamais laissé au choix du geste — et tout comparateur post-appel est recalé entre l'appel et la comparaison.

**Alternatives rejetées.** Déclarer tcp-07 conforme sur la lecture structurelle (rejeté : le marshalling a0→a2 ne vit dans AUCUNE lecture — 1537 verrous verts sur un bloc qui crashait au premier appel : l'espèce exacte du faux vert) ; nommer une réserve d'instrument sur qemu (rejeté : les reproducers crashaient pour leurs propres défauts — le mprotect invité marche, la réserve aurait été un mensonge d'instrument) ; tolérer le spin de .dire comme un défaut cosmétique (rejeté : le spin est un HANG — l'espèce la plus dure, un vert muet éternel) ; recalé t0 « une fois pour toutes » au début du bloc (rejeté : recalé AVANT CHAQUE comparaison — le clobber est répété, la défense aussi).

**Frontières.** La règle régit les PORTS de blocs entre ISA (le marshalling des arguments de service), les sous-programmes locaux (le cadre ra), les registres porteurs d'attendus (D150) et la discipline d'isolement des défauts (jamais d'image roulée à la main — la famille du builder) ; elle ne touche NI la réserve instrumentale D149 (nommée dans chaque verdict — TCG, noyau et syscalls réels), NI la frontière code 5 (le service refuse — STRUCTURALE sous qemu : l'hôte accorde RWX sur mapping privé, la branche fail-closed vit dans le bloc), NI le périmètre mono-fil (fiche § 5 : portée de fence.i = le cœur courant). La correction de tcp-07 (une ligne) et le rebuild du corpus (sha ec343b4e…) sont consignés à l'Entrée 153 ; le scellage 0.8.0-rc.1 a exigé le chemin réel VERT AVANT la balise (le verrou multi-profils, le D146 par trace, la conformité 7/7 — la suite EXÉCUTANT la démonstration).

## D158 — L'EXPORT DE CONTINUITÉ PORTE SA GÉOMÉTRIE ET SES PARAMÈTRES PUBLICS (l'import aux cinq étapes est AUTO-PORTANT : la table id/offset/taille/empreinte par artefact et la dérivation de chaque carte — sel Argon2id, contexte HKDF, génération — vivent AU MANIFESTE chiffré+signé ; l'import ne doit au dépôt QUE la clé publique, recoupement et non dépendance) ; UNE CARTE D'ÈRE PASSÉE NE SE TRANSPORTE PAS (les cartes des ères antérieures de la phrase gardent des signatures valides mais des fragments indéchiffrables — l'état scellé COURANT d'un profil vit dans sa DERNIÈRE carte de l'ère courante) ; L'INSTRUMENT D'UN TERRAIN VIT DANS SON KIT (quand le prérequis du run est un instrument absent des machines, le kit l'embarque — binaire statique, version ET md5 consignés au témoin : un instrument remplacé en silence est un refus nommé) ; QEMU-USER EXIGE LE BIT EXÉCUTABLE DE L'IMAGE INVITÉE (« Exec format error » sans lui — le scénario terrain le RÉTABLIT, geste nommé : le chmod ne touche aucun octet de contenu) ; LES LIGNÉES HOMONYMES SE CHARGENT PAR CHEMIN ABSOLU (unix/ et riscv/ portent layout.py et carte_corpus.py homonymes — sys.path écrase, le premier import gagne et le second rend le premier ENCORE : tout multi-lignée charge par importlib à chemins absolus)

**Le constat qui fonde la décision (05/11/2026, chantier M7-(d), Entrée 154 — l'export multi-profils + le kit terrain).** CINQ espèces nommées par le geste, chacune attrapée aux épreuves et jamais par la relecture : (1) **L'IMPORT QUI DÉPEND DU DÉPÔT N'EST PAS UN IMPORT** — la première forme du vérificateur reprenait le modèle M1 (lire la géométrie depuis build_m1, les dérivations depuis les modules du dépôt) : sur un poste nu, l'import échoue faute de dépôt, l'anti-enfermement (§ 17.3) meurt ; la table de géométrie et les paramètres PUBLICS de dérivation (le sel Argon2id et le contexte HKDF sont publics par conception — la phrase reste le seul secret) portés au manifeste chiffré+signé rendent l'import AUTO-PORTANT, et la preuve d'équivalence se joue au geste même : la dérivation portée déchiffre les MÊMES clairs que les modules du dépôt ; la clé publique demeure EXTERNE au conteneur (recoupée au dépôt quand il existe — un conteneur auto-signé seul porte la réserve nommée). (2) **LES CARTES D'ÈRES PASSÉES** — le premier geste a voulu transporter m0/carte et m1/carte (le modèle M1) : leurs signatures Ed25519 sont valides mais leurs fragments sont indéchiffrables avec la phrase COURANTE (les réinitialisations D27/D30 — la 4e au M3) ; constat sur pièces : HUIT cartes de l'ère courante (m3/m4/m5/terrain + les quatre M6/M7), toutes à UNE clé D27 ; l'export transporte l'état scellé COURANT de chaque profil (win : m5/carte, les 52 blocs de la pile dans proxy.exe 0.6.0 — la lignée vit dans l'artefact courant), les cartes d'ère passée demeurent l'histoire du dépôt. (3) **L'INSTRUMENT EMBARQUÉ** — le terrain M7 exige qemu-riscv64, absent des machines : la promesse « aucun outil nouveau » du m6d ne pouvait pas se tenir ; le kit embarque le binaire STATIQUE (aucun paquet, aucun réseau, aucun root), sa version et son md5 consignés au TÉMOIN du run ; si l'environnement fournit le sien ($QEMU_RISCV64, PATH), il est identifié de même — mais l'instrument du KIT ne se remplace pas en silence (md5 asserté). (4) **LE BIT EXÉCUTABLE DE L'IMAGE INVITÉE** — l'épreuve d'extraction vierge a échoué au premier rituel : qemu-user 10.0.13 REFUSE l'image sans bit X (« Exec format error », 83 o de refus) alors que l'extraction zip du bac NE RESTAURE PAS les permissions (le zipfile de ce Python n'applique pas le chmod des external_attr — le kit m6d connaissait déjà l'espèce pour le natif) : le scénario RÉTABLIT le bit des artefacts et de l'instrument, gestes NOMMÉS au journal, et les empreintes de fin de run re-prouvent que le chmod n'a touché aucun octet de contenu. (5) **L'HOMONYMIE DES LIGNÉES** — le constat des frag-bld a rendu QUATRE FOIS le module unix pour quatre étiquettes riscv/unix : sys.path portait riscv/ PUIS unix/, le second `import carte_corpus` rend le PREMIER module encore (sys.modules garde la main) — depuis, tout multi-lignée charge ses modules par importlib à chemins ABSOLUS sous des noms distincts.

**La règle.** (1) TOUT export de continuité porte au manifeste : la table de géométrie (id, offset fichier, taille, empreinte) de CHAQUE artefact à blocs, les paramètres publics de dérivation de CHAQUE carte transportée, les versions par profil — l'import s'exécute sur un poste nu avec la phrase seule (la clé publique recoupée par un canal externe) ; la preuve d'équivalence dérivation-portée ↔ modules-du-dépôt se joue À CHAQUE export. (2) L'export transporte EXCLUSIVEMENT des cartes de l'ère courante de la phrase — l'état scellé courant d'un profil est sa dernière carte vérifiable de bout en bout ; transporter une carte d'ère passée serait une pièce non vérifiable (sa signature passe, son fragment ne s'ouvre pas : la moitié d'une preuve n'est pas une preuve). (3) Le kit d'un terrain dont le prérequis est un instrument absent EMBARQUE l'instrument (statique de préférence) et le consigne au témoin (version + md5) ; l'instrument de l'environnement reste admis, identifié de même ; l'instrument du kit ne se remplace pas en silence. (4) Un scénario terrain qui exécute des fichiers par un instrument RÉTABIT leurs bits exécutables si perdus (geste nommé au journal) et re-prouve les empreintes après le run — le chmod n'est jamais une modification de contenu. (5) Le code qui touche DEUX lignées du dépôt charge leurs modules homonymes par chemins absolus sous des noms distincts — un import par sys.path entre lignées est une faute d'instrument (le module rendu n'est pas celui que l'étiquette nomme).

**Alternatives rejetées.** Transporter les cartes m0/m1 pour fidélité au modèle M1 (rejeté : leurs fragments ne s'ouvrent pas avec la phrase courante — l'export doit être VÉRIFIABLE de bout en bout, pas historique) ; exiger du développeur l'installation de qemu par sa distribution (rejeté : un prérequis d'installation est une source de divergence d'instrument ET un droit root pour rien — le statique embarqué élimine les deux) ; laisser le scénario échouer sur le bit X perdu avec un message (rejeté : le bit se perd PARTOUT où l'extraction ne restore pas les permissions — le rétablissement nommé est le geste honnête, l'échec serait un faux obstacle) ; une seconde clé de conteneur par profil (rejeté : UNE phrase, UN sel export dédié, HKDF par contexte — la dérivation est déjà hiérarchique, la multiplier serait du bruit) ; l'oracle exporté avec le conteneur (rejeté : D1 — éphémère, régénéré depuis I à l'arrivée, jamais un artefact empoisonnable persistant).

**Frontières.** La règle régit les EXPORTS de continuité (le manifeste auto-descent), les KITS terrain (l'instrument embarqué et consigné), les scénarios qui exécutent des fichiers (le bit rétabli, geste nommé) et le code multi-lignées du dépôt (les imports par chemin absolu) ; elle ne touche NI la réserve instrumentale D149 (TCG, noyau et syscalls réels — nommée dans chaque verdict), NI la règle 3-2-1 (le conteneur chiffré se stocke n'importe où, le coffre Drive en reçoit une copie), NI le scellage final (la 0.8.0 attend le run terrain du développeur, le recoup sur pièces et --sceller-final — modèle m6d). Les cinq espèces sont consignées à l'Entrée 154 avec leurs pièces (l'épreuve d'extraction vierge, le traceback de l'homonymie, le refus « Exec format error »).

## D159 — LA REPRISE D'UN POSTE SE MÈNE AUX MIROIRS, JAMAIS À LA MÉMOIRE (quand le poste de laboratoire est restauré à un état antérieur — perte de l'arbre de travail non commité — l'état VRAI du projet vit dans les miroirs externes consignés : le dépôt GitHub porté à la pointe par la passation D141, le coffre Drive pour les kits et les pièces ; la reprise est un FETCH + un RESET à la POINTE CONSIGNÉE, jamais une reconstruction de mémoire ; les instruments gitignorés se réinstallent par leurs PROCÉDURES du dépôt, l'identité constatée par empreinte ; ce qui n'a jamais été consigné est perdu par principe)

**Le constat qui fonde la décision (05/11/2026, le geste final M7-(d), Entrée 155 — le run terrain recoupé, la finale 0.8.0 scellée).** En ouverture du geste (le message du développeur « les preuves sont dans le dossier drive /test »), le poste de laboratoire s'est révélé RESTAURÉ à un instantané antérieur : l'arbre local portait l'état M6-(c) (passation 402508f), le worklog s'arrêtait à la Task 65, le JOURNAL à l'Entrée 147, DECISIONS à D152 — TOUT le jalon M7 (quatre chantiers, Entrées 150-154, D155-D158, Tasks 68-72) était ABSENT du disque, et avec lui les scripts de sonde du run écrits après la dernière passation. La doctrine « sur pièces, jamais sur mémoire » appliquée AU POSTE LUI-MÊME : (1) l'état réel établi par `ls-remote` — GitHub pointait sur `cc56930`, EXACTEMENT la pointe consignée par la dernière passation D141 (le bundle déposé au miroir portait cette même pointe, ASSERTÉE avant dépôt) ; (2) l'arbre ré-établi par `fetch` + `reset --hard` à cette pointe — les seuls écarts locaux étaient des BITS DE MODE (644→755, artefacts de la restauration), zéro changement de contenu ; (3) l'instrument qemu-riscv64 réinstallé par SA PROCÉDURE du dépôt (`riscv/outils/installer_qemu.sh`, le paquet statique Debian 10.0.13) et recoupé par empreinte : md5 `bae5a36f…` IDENTIQUE à l'instrument EMBARQUÉ du kit — le même instrument au laboratoire et au terrain, la réserve D149 inchangée ; (4) les dépendances Python réinstallées (pynacl, keystone-engine, capstone — le bac livré nu) ; (5) les preuves du run lues AU COFFRE (le trio complet, md5 contrôlés par pièce AVANT toute interprétation) — le coffre est la source, jamais la copie locale. RIEN du jalon ne s'est perdu : la cadence « une passation par geste de jalon » (leçon D141 : aucune dette n'accumule) avait poussé chaque geste vers les miroirs AU FIL DU JALON — c'est précisément le pari de D141, tenu au moment où il fallait le tenir.

**La règle.** (1) TOUT écart entre l'état local et l'état attendu se tranche par les PIÈCES EXTERNES : `ls-remote` d'abord, le log local n'est JAMAIS une preuve d'état courant ; un instantané restauré se constate (worklog, JOURNAL, DECISIONS, `git log` recoupés ENTRE EUX) avant tout geste. (2) La reprise d'un poste restauré est un FETCH + un RESET à la POINTE CONSIGNÉE (la passation nomme la pointe du geste ; le bundle du miroir la porte ASSERTÉE) — une divergence entre la pointe consignée et la pointe distante se traite et se NOMME avant tout geste : un reset « au jugé » vers une pointe non consignée serait une rétro-écriture. (3) Les instruments gitignorés ont des PROCÉDURES dans le dépôt (l'installation est une pièce — le constat fiche § 10) : la réinstallation passe par elles et l'empreinte est CONSTATÉE après (un instrument divergent de son consigné est un refus nommé — la règle D158-(3) au labo même). (4) Ce qui n'a jamais été commité ni déposé est PERDU PAR PRINCIPE : le travail d'un geste en cours se consigne au fur et à mesure (triple consignation), jamais en fin de session seulement — les scripts de sonde du run sont morts avec l'instantané et ont été RE-ÉCRITS, aucune pièce ne dépendait d'eux.

**Alternatives rejetées.** Reconstruire le jalon de mémoire (rejeté : la mémoire n'est pas une pièce — l'exactitude mot pour mot des consignations et des empreintes ne se re-crée pas, elle se FETCH ; une reconstruction serait une rétro-écriture déguisée) ; compter sur le bac à sable comme stockage durable (rejeté : constaté au geste même — il se restaure à un instantané antérieur sans avertissement, seuls les MIROIRS consignés font foi) ; dupliquer les bundles dans /test pour « doubler » la sauvegarde (rejeté : le miroir dédié TRIADE-sauvegarde-git/ est la place des bundles, /test est le coffre des pièces — D143 ; la redondance utile est GitHub + miroir, déjà tenue) ; recopier les pièces du coffre vers le dépôt (rejeté : les pièces vivent au coffre et dans download/ non committé, md5 contrôlés à CHAQUE lecture — D99 : zéro mélange).

**Frontières.** La règle régit la REPRISE de poste et l'établissement de l'état avant un geste ; elle ne touche NI la passation D141 (la cadence demeure « une passation par geste de jalon » — la finale 0.8.0 scellée reçoit la sienne, série 080), NI les scellés (aucune carte ni artefact n'a bougé — le jalon entier a été re-constaté vert APRÈS reprise : le verrou multi-profils, le contrôle D146, la conformité 7/7 exécutés AU geste de scellage même), NI le coffre (lecture seule pour le recoup — la clôture D143 est un déplacement nommé, jamais un jet), NI la réserve instrumentale D149 (le réinstallé est l'IDENTIQUE par empreinte). L'événement est consigné à l'Entrée 155 avec ses pièces (ls-remote, le reset, les md5).

## D160 — L'ÈRE D'APRÈS M7 S'OUVRE PAR LA FONDATION, PAS PAR LA PIÈCE LA PLUS SPECTACULAIRE (l'ordre des familles est syscalls directs → TLS 1.3 pur → profils additionnels : le premier est la FONDATION I/O du second — une pile TLS pure qui émettrait encore par l'IAT userland garderait la surface de hook qu'elle prétend éliminer ; chaque addition s'appuie sur des résultats mesurés, la règle du plan) ; LE JALON M8 NAÎT SUR LE PROFIL WIN (le domaine `sys` créé au registre figé, la lignée m8/, la charte des syscalls directs à HUIT règles, la balise 0.9.0 au premier build — geste de BUILD jamais scellage) ; LE SSN EST UNE DONNÉE, JAMAIS UN OCTET DE CODE ; LE MOTIF DU STUB EST VÉRIFIÉ AVANT TOUTE EXTRACTION (un stub divergent = refus nommé — la contre-mesure du hook est un chantier futur, jamais une contrebande) ; LA COUCHE I ÉCRITE-AVANT-CODE PRÉCÈDE TOUT OCTET (modèle D77) ; L'EXPORT DE CONTINUITÉ 0.8.0 REFERME L'ÈRE M6/M7 AVANT L'OUVERTURE (l'état protocole qui quitte le poste porte la carte 0.8.0)

**Le contexte qui fonde la décision (05/11, « continue »).** Le jalon M7 est franchi (Entrée 155 : le run terrain vert sur pièces, le recoup labo 29/29, la finale 0.8.0 scellée — le programme M6/M7 accompli) et le worklog annonçait « les chantiers d'après M7 attendent la décision du développeur ». La demande « continue » du 05/11 EST cette décision : l'ère s'ouvre. Le plan nommait trois familles « volontairement hors périmètre courant afin que chaque addition s'appuie sur des résultats mesurés » (spec, fin) : le bloc optionnel de syscalls directs, TLS 1.3 pur en blocs scellés, les profils additionnels (`aarch64-macos-macho`, `wasm32-wasi`). La présente décision LÈVE la clause NOMMÉMENT pour la PREMIÈRE famille ; les deux autres demeurent hors périmètre jusqu'à leur ouverture (une décision propre chacun — jamais un ouvre-tout). Deux gestes accompagnent l'ouverture : L'EXPORT DE CONTINUITÉ 0.8.0 (le geste dédié annoncé à l'Entrée 155 — le conteneur régénéré porte la carte 0.8.0 scellée, l'import à sec et les rituels VERTS sur les octets transportés, la copie poussée au coffre racine : l'ère qui s'ouche laisse le poste PROPRE) et LA COUCHE I DU DOMAINE sys ÉCRITE-AVANT-CODE (m8/I/ : le README à la charte, les TROIS spécifications sys-01/sys-02/sys-03, génération 8, blocs g9xxxx — le contrat précède l'octet, R2).

**La règle.** (1) **L'ordre des familles est la fondation d'abord** : syscalls directs (le jalon M8, la lignée m8/, le domaine `sys` sur le profil win) AVANT TLS 1.3 pur AVANT les profils additionnels — chaque famille s'appuie sur les résultats MESURÉS de la précédente ; ouvrir par la pièce la plus spectaculaire construirait la cryptographie pure sur la surface d'appel qu'elle prétend éliminer. (2) **Le jalon M8 est le domaine sys** : l'émetteur (sys-01 — le trombone ABI : rcx→r10, syscall, ret, AUCUN prologue de pile car le noyau lit [rsp+0x28] de l'APPELANT), le résolveur (sys-02 — l'EAT de ntdll LUE directement : les trois tables, la marche BORNÉE par NumberOfNames, la comparaison par libc-04 l'héritage scellé, JAMAIS un appel — le bloc qui lit n'émet pas), l'usage réel (sys-03 — la twin de hello-02 par NtWriteFile : neuf arguments, la ligne CITÉE du fixture M0, zéro IAT — la preuve STRUCTURELLE). La charte à HUIT règles (m8/I/README.md) lie les trois spécifications. (3) **Le SSN est une DONNÉE, jamais un octet de code** : aucun numéro de service gravé — les numéros varient par build de Windows, une constante gravée serait un mensonge par build, faux en silence sur tout terrain d'un autre build ; le numéro vient du résolveur au geste même, lu de ntdll SUR LA MACHINE qui exécute ; le labo prouve sur FIXTURES ntdll synthétiques (le modèle différentiel M4/M5), le terrain mesure le VRAI (le kit du chantier (d), modèle m6d/m7d — le run du développeur, les preuves au coffre, le recoup sur pièces). (4) **Le motif du stub est vérifié avant toute extraction** : les quatre octets 4C 8B D1 B8 (mov r10, rcx ; mov eax, imm32 — la graphie des stubs Windows 10/11 x64) confrontés AVANT de lire l'imm32 à +4 ; toute divergence = refus nommé (hook ou ère inconnue), JAMAIS une heuristique de secours — la contre-mesure du hooking est un CHANTIER FUTUR NOMMÉ, jamais une contrebande. (5) **La couche I précède tout octet** (D77) : le plan d'adressage naît AVEC la couche (m8/layout.py — la section .text5 préfigurée 0xA000-0xBFFF, les constantes MOTIF_STUB/PE/EAT en source unique, la table des SEPT verdicts, les versions 0.9.0-dev.1/0.9.0 ; l'héritage m5 CHARGÉ PAR CHEMIN ABSOLU — la leçon D158 appliquée dès la naissance). (6) **Le registre figé s'étend** : le domaine `sys` est créé, réservé M8 — un identifiant n'est jamais réutilisé. (7) Les chantiers du jalon : (a) la couche I (LA PRÉSENTE — accomplie) ; (b) les blocs notés-mesurés-prouvés au harnais (la notation à la main via auteur.py, le round-trip, le différentiel sur FIXTURES ntdll, la falsification) ; (c) le build 0.9.0-dev.1 (la composition .text5 sur le corps 0.6.0 INTACT, la carte génération 8, l'oracle structurel — la règle AUCUN IAT PAR BLOC sys) ; (d) le terrain (le kit au coffre /test, le run du développeur sur SA machine, le recoup sur pièces — la finale 0.9.0 attend le vert).

**Alternatives rejetées.** Ouvrir par TLS 1.3 pur (rejeté : la pièce la plus spectaculaire d'abord construirait la cryptographie sur l'IAT userland — la surface de hook demeurerait SOUS la nouvelle œuvre ; la fondation d'abord, chaque addition sur résultats mesurés) ; ouvrir par les profils additionnels (rejeté : l'universalité étendue avant la souveraineté complète inverserait la logique du programme — les nouveaux profils hériteraient de l'IAT) ; graver les SSN par build de Windows (rejeté : un mensonge par build — la table serait fausse en silence sur tout terrain d'un autre build ; le domaine ne connaît pas le terrain, il le LIT) ; l'heuristique de secours devant un stub croché (rejeté : le contourner en silence serait la contrebande exacte que la règle 4 interdit — la contre-mesure du hooking sera son PROPRE chantier, nommé, prouvé) ; un émetteur à prologue (rejeté : le noyau lit la pile [rsp+0x28] AU MOMENT du syscall — un mot poussé décalerait TOUS les arguments de pile ; le trombone n'a pas de cadre, l'invariant I3 de sys-01) ; ouvrir les TROIS familles d'un coup (rejeté : « chaque addition s'appuie sur des résultats mesurés » — la clause du plan n'est pas décorative, elle est l'ordre de preuve).

**Frontières.** La présente décision n'est NI un scellage NI un build : AUCUNE balise ne bouge (win 0.6.0, linux 0.7.0, riscv 0.8.0 — INTACTES ; la 0.9.0-dev.1 viendra du premier build M8 au chantier (c)) ; le corps hérité 0.6.0 ne bouge pas d'un octet (R7 — .text5 est une section NOUVELLE, modèle .text3/.text4) ; la clause spec « hors périmètre courant » est levée NOMMÉMENT pour la seule famille syscalls directs (TLS 1.3 pur et profils additionnels attendent leur décision propre) ; la PEB-walk (trouver ntdll sans IAT) et la contre-mesure du hooking sont des CHANTIERS FUTURS NOMMÉS (en l'état : la base est fournie par l'appelant, le stub divergent est un refus) ; l'export de continuité demeure un geste PAR ère (le conteneur 0.8.0 est celui de l'ère M6/M7 close — le prochain naîtra de l'ère 0.9.0). Les pièces de l'ouverture : m8/I/ (README + charte + trois spécifications), m8/layout.py, le registre figé étendu (m0/I/README.md), le conteneur TRIADE-continuite-multiprofils-0.8.0-20261105T044932Z.bin au coffre.

## D161 — LES SLOTS DU DOMAINE `sys` ARRÊTÉS SUR LES LONGUEURS RÉELLES DES NOTATIONS (la mesure auteur décide — D47/D79 rejoués : la préfiguration 0xA000/0xA400/0xB000 n'était pas un droit) ; LES FIXTURES .rdata DU DOMAINE ARRÊTÉS DANS LA ZONE VIERGE DU SCELLÉ 0.6.0 (le nom @0x2EC0, la ligne de hello-02 @0x2ED0, la borne @0x2F00 — le corps ne bouge d'AUCUN octet R7) ; LES TROIS ERRATA DE LA COUCHE I CORRIGÉS NOMMÉMENT AVANT LA NOTATION (memcmp est libc-02 jamais libc-04 ; « NtWriteFile » mesure 11 octets jamais 10 ; le padding de slot de la lignée est NOP 0x90 jamais int3) ; LA SÉPARATION VERDICTS/SSN EST STRUCTURELLE (les verdicts de vrais négatifs 64 bits signe-étendus, les SSN zéro-étendus — jamais de collision)

**Le contexte qui fonde la décision (05/11, chantier M8-(b)).** La couche I du domaine `sys` était née écrite-avant-code (D160, Entrée 156) : la charte à huit règles, les trois spécifications, le plan d'adressage PRÉFIGURÉ — « les RVA et tailles définitifs seront ARRÊTÉS au chantier (b) sur les longueurs réelles des notations (modèle D47/D79 : la mesure auteur décide, la préfiguration n'est pas un droit) ». Le chantier (b) a produit les notations (à la main, auteur.py, keystone assemble — rien d'autre), les a MESURÉES, et la mesure décide : sys-01 SIX octets, sys-02 293, sys-03 164. La préfiguration s'incline.

**La règle.** (1) **Les slots arrêtés** : sys-01 @ **0xA000** slot **0x40** (padding 58), sys-02 @ **0xA040** slot **0x140** (padding 27), sys-03 @ **0xA180** slot **0xC0** (padding 28) — tassés depuis 0xA000 (D8 : multiples de 64, alignés 16, padding >= 16), la réserve contiguë **0xA240-0xBFFF** (7 488 o) porte la croissance du domaine (sys-04 et suivants ; TLS 1.3 pur attend sa décision propre, D160). (2) **Les fixtures .rdata du domaine arrêtés dans la zone VIERGE 0x2EB0-0x2FFF du scellé 0.6.0** (vérifiée sur pièces au geste : 336 octets NULS dans proxy.exe après la borne de marche M5 R_BORNE_M5) : le span-nom « NtWriteFile » @ **0x2EC0** (11 octets, AUCUN NUL — P1 de sys-02 est un SPAN, jamais une terminaison supposée), la LIGNE de hello-02 @ **0x2ED0** (34 o dont NUL, byte-exact le MESSAGE de m0/build_m0.py — la twin ÉMET ces octets, jamais une seconde copie : I4 de sys-03), la borne @ **0x2F00** (fail-closed, miroir D95 — le prochain fixture pose là, jamais au-delà sans arrêt nommé). Le corps scellé ne bouge d'AUCUN octet (R7) : la zone VIERGE reçoit les nouveaux. (3) **Les trois errata de la couche I, corrigés nommément AVANT la notation** : memcmp est **libc-02** (b20002 — le registre figé m1/I/README.md fait foi), la couche I citait libc-04 (itoa) ; « NtWriteFile » mesure **11 octets** (N-t-W-r-i-t-e-F-i-l-e — la mesure sur pièces fait foi), la couche I disait 10 ; le padding de slot de toute la lignée win est **NOP 0x90** (build_m0.py : `octets + b"\x90" * pad` — int3 est la convention des zones RÉSERVÉES inter-blocs), la couche I disait int3. Aucun octet n'avait encore été écrit sur les citations fausses : la correction précède l'octet, chaque erratum consigné DANS le fichier de la couche I qu'il corrige. (4) **La séparation verdicts/SSN est structurelle** : les verdicts du domaine sont de VRAIS négatifs 64 bits (`mov rax, -N` signe-étendu), les SSN des imm32 zéro-étendus (`mov eax, [rdx+4]`) — un SSN à bit 31 posé reste POSITIF en 64 bits, jamais confondu avec un verdict ; le test en est fait au harnais (le cas pathologique 0x80000001). (5) **La preuve au harnais sur FIXTURES ntdll synthétiques** (le modèle différentiel M4/M5) : le labo ne possède aucun vrai ntdll, n'en prétend aucun et NE DEVINE JAMAIS le SSN du terrain — les fixtures forgées (PE32+ minimales mais bien formées : l'hostilité vit dans les noms, les stubs, les bornes, jamais dans des pointeurs fous) font la preuve ; le VRAI ntdll se lira au terrain (chantier (d), modèle m6d/m7d). Le bilan du premier passage complet : **61 contrôles · 61 VERTS** (round-trip + concordance au plan ; le trombone au noyau simulé ; le résolveur et ses SIX verdicts nommés ; LA TWIN au différentiel — la MÊME ligne par les DEUX chemins octet pour octet ; le fuzzing à trois graines ; les QUINZE mutations de falsification attrapées, les témoins intacts verts).

**Alternatives rejetées.** Garder la préfiguration 0xA000/0xA400/0xB000 (rejeté : D47/D79 — la préfiguration n'est pas un droit, la mesure décide ; le tassement laisse 7 488 o contigus à la croissance) ; poser les fixtures dans une section nouvelle (rejeté : la zone vierge 0x2EB0-0x2FFF du .rdata EXISTANT suffit — aucune section de plus, aucun octet du scellé déplacé) ; recopier la ligne de hello-02 dans le bloc (rejeté : I4 — une seconde copie serait une divergence d'observable en sursis ; la twin CITE par déplacement) ; un NUL après le span-nom (rejeté : P1 de sys-02 est un SPAN — poser une terminaison supposerait ce que le contrat interdit de supposer) ; corriger les errata SILENCIEUSEMENT (rejeté : la doctrine — sur pièces, jamais sur mémoire ; chaque coquille est NOMMÉE dans le fichier qu'elle corrompait, la lignée peut relire le geste) ; graver les SSN des fixtures dans le modèle (rejeté : le modèle dérive de la couche I et du plan, JAMAIS des octets de la notation — deux sources de vérité seraient une de trop).

**Frontières.** La présente décision est un ARRÊT D'ADRESSAGE, NI un build NI un scellage : AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 — INTACTES ; la 0.9.0-dev.1 viendra du premier build M8 au chantier (c), geste de BUILD) ; le corps scellé 0.6.0 ne bouge pas d'un octet (R7) ; les octets des fixtures .rdata seront POSÉS au build (c) dans la zone vierge (les adresses sont arrêtées, la pose attend le bâtisseur) ; le labo ne connaît pas le SSN du terrain (les fixtures synthétiques, la frontière du README) ; TLS 1.3 pur et les profils additionnels HORS PÉRIMÈTRE (une décision propre chacun) ; la PEB-walk et la contre-mesure du hooking CHANTIERS FUTURS NOMMÉS. Les pièces de l'arrêt : m8/notation/ (les TROIS notations explicites + brouillons), m8/outils/auteur.py, m8/harnais_sys.py, m8/layout.py (arrêté), m8/I/ (les errata consignés), les empreintes au harnais (19e24b48… graine 20261105, re-jouée 424242/777).

## D162 — LA CÉRÉMONIE DU SCEAU I DE L'ÈRE M8 EST EXIGÉE AVANT TOUT BUILD (le garde-sceau D87 NOMME la dette : le registre figé m0 fut étendu au M8-(a) SANS re-signature — un diff d'intention non signé ; la clé hors-ligne du développeur est requise, le labo ne signe JAMAIS à sa place) ; LA TABLE DU SCEAU ÉTENDUE À L'ARBRE m8 (le domaine sys — sceau_I.py n'est pas signé lui-même : aucune cascade) ; LES OFFSETS FICHIER DE L'ÈRE ARRÊTÉS (.text5 raw 0x8E00, taille 0xAE00 — les sept en-têtes tiennent dans la marge 0x400, le décalage de packaging D94 n'est pas rejoué) ; LE BUILD 0.9.0-dev.1 ÉCRIT, SES COMPOSANTS VÉRIFIÉS SUR PIÈCES DÉTACHÉES, AUCUN ARTEFACT AVANT LA CÉRÉMONIE

**Le contexte qui fonde la décision (05/11, chantier M8-(c)).** Le chantier (b) avait livré les trois notations prouvées (Entrée 157, D161). Le chantier (c) — le build — commence par LE GARDE (le modèle build_m5 : « les chaînes de build appellent garde() et refusent un arbre divergé », D87). Au premier appel, le garde REFUSE : l'arbre m0 a divergé (fichier modifié : README.md — code 10, « diff d'intention non signé »). La mesure sur pièces : le M8-(a) (D160 règle 6 : « le registre figé s'étend — le domaine sys est créé, réservé M8 ») a muté m0/I/README.md sans cérémonie de re-signature ; les spécifications hello-01/02/03 sont INTACTES (seul le registre diverge du manifeste signé à la cérémonie 0.6.0 du 04/11) ; l'arbre m8 — la couche I du domaine, avec ses errata D161 — n'a jamais été signé (l'arbre m5 lui-même ne le fut qu'à la cérémonie de SON scellage). La dette est née au M8-(a), elle est échue au premier geste du build : le sceau fait exactement son travail.

**La règle.** (1) **La cérémonie de l'ère M8 est le préalable de tout build** : la remise du développeur (SA clé Ed25519 hors-ligne, D87 — le même geste que la remise de 11 lignes du 04/11) porte AU MINIMUM **m0** (le registre figé étendu — les specs hello intactes, seul le README à re-signer) et **m8** (le domaine sys). La charge est PRÉPARÉE (`sceau_I.py preparer` → v06/sceau-I/a-signer.txt, 12 arbres, les empreintes vivantes) ; le dépôt suit la remise (`sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt` — l'atomicité de cérémonie : clé, signatures et manifestes basculent ensemble ou pas du tout). (2) **Le labo ne signe jamais à la place du développeur** : la clé de TEST (lab, D105) DÉCLASSERAIT l'état « réelle » du dépôt — une régression de preuve, refusée ; aucune clé inventée ; le refus nommé du garde est la seule réponse honnête tant que la remise n'est pas déposée. (3) **La table du sceau s'étend à l'arbre m8** (`m8 : proxy.exe (domaine sys, syscalls directs), sys.1`) : sceau_I.py n'est PAS couvert par l'arbre v06 (CF2/CF3/README seulement) — l'extension de la table ne diverge AUCUN arbre signé, aucune cascade. (4) **Les offsets fichier de l'ère sont arrêtés** (m8/layout.py, la source unique — modèle D94) : .text5 raw **0x8E00** (la 7e section vit après .text4, les SIX premières raw inchangées), taille de fichier **0xAE00** ; les SEPT en-têtes (608 o) TIENNENT dans la marge SizeOfHeaders 0x400 — le décalage de packaging D94 n'est PAS rejoué, aucun octet hérité ne bouge. (5) **Le build est écrit et vérifié par pièces détachées, aucun artefact avant la cérémonie** : le garde ARMÉ en tête de construire/verifier (le refus CONSTATÉ au geste, avec la notice de cérémonie) ; l'héritage re-vérifié de bout en bout (M3 524 + M4 492 + M5 312 verrous, l'image M5 composée == le scellé 0.6.0 OCTET PAR OCTET, sha c1e46fb0… — la carte génération 7 scellée prouve ces octets) ; l'oracle structurel M8 (54 verrous — LA RÈGLE AUCUN IAT PAR BLOC sys, le site syscall unique, le motif AVANT l'imm32, l'ordre résoudre-puis-émettre) ; la composition (.text5 + les fixtures dans la zone vierge + la version 0x00090001 : geste de BUILD jamais scellage) ; la validation PE (7 sections, imports inchangés, portes R10+M5) ; la preuve R7 (41 blocs hérités octet-identiques, les trouées du domaine vierges des deux côtés) ; **l'exe composé 44 544 o, sha256 1492b0bc0792e1ab…, re-constaté identique (le déterminisme)** ; les TROIS oracles appelés depuis le build (M4/M5 héritage + le harnais M8 : 61 contrôles sur les blobs du build) ; la carte génération 8 prête (m8/carte_m8.py — les primitives testées à blanc dans un répertoire temporaire : JAMAIS de carte avant son build ; la clé publique e9cd8c549485… : LE TÉMOIN NE BOUGE PAS, la graine durable D144). AUCUN fichier m8/proxy.exe, AUCUNE carte déposée : l'artefact naîtra de construire() quand le garde passera.

**Alternatives rejetées.** Contourner le garde (rejeté : le fail-closed est la doctrine — un garde contournable ne serait pas un garde ; le refus nommé EST le résultat du chantier) ; signer avec la clé de test du lab (rejeté : déclasser l'état « réelle » du dépôt serait une régression de preuve — la clé de test est « la preuve visible de l'état laboratoire », l'état PRÉSENT est réel depuis la cérémonie 0.6.0) ; retirer m0 de la liste gardée (rejeté : m0 EST l'héritage — hello-02 est dans le build ; sauter l'arbre fautif serait la contrebande exacte que D87 existe pour attraper) ; bâti l'artefact sans le garde « pour tester » (rejeté : un proxy.exe né hors garde serait un artefact illégitime ; les composants se testent par pièces détachées, l'assemblage complet attend la cérémonie) ; re-signer TOUT (rejeté : seuls les arbres mutés/nouveaux exigent la remise — m1-m7, demo, terrain, v06 sont intacts, leurs signatures en place restent valides ; la remise minimale est de 2 lignes).

**Frontières.** La présente décision N'EST NI un build NI un scellage : AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 — INTACTES ; la 0.9.0-dev.1 viendra du build après la cérémonie, geste de BUILD ; la 0.9.0 attend le terrain vert du chantier (d)) ; le scellé 0.6.0 (c1e46fb0…) est l'ANCRE R7 de l'ère — il ne bouge pas ; l'état de clé du sceau demeure « réelle » ; l'exe composé 1492b0bc… est une PIÈCE DE VÉRIFICATION (le déterminisme constaté), pas un artefact livré — l'artefact naîtra du build complet ; la carte génération 8 n'existe pas encore (ses primitives sont prêtes, le témoin ne bouge pas). Les pièces de l'arrêt : m8/build_m8.py, m8/carte_m8.py, m8/harnais_sys.py (executer), m8/layout.py (offsets arrêtés), v06/sceau_I.py (table étendue), v06/sceau-I/a-signer.txt (la charge du développeur), les empreintes constatées (héritage c1e46fb0…, composé 1492b0bc…, oracle M8 54 verrous, harnais 61/61).

## D163 — LA CONTINUITÉ DE CLÉ D'UNE RE-CÉRÉMONIE SE PROUVE PAR LE DÉTERMINISME Ed25519 (re-signer un arbre inchangé avec la même clé redonne EXACTEMENT la signature déposée : la comparaison bit à bit des signatures des arbres inchangés EST la preuve de la réutilisation de la clé, sans jamais accéder à la clé privée — une divergence nomme une clé neuve : l'ARRÊT) ; LA CÉRÉMONIE DE L'ÈRE M8 PASSÉE, LA DETTE D162 SOLDÉE, LE GARDE VERT 12/12, L'ARTEFACT 0.9.0-dev.1 NÉ DU BUILD IDENTIQUE À SA PIÈCE DE VÉRIFICATION (le déterminisme d'un poste à l'autre : 1492b0bc… == 1492b0bc…) ; L'ACCÈS AU COFFRE NE DÉPEND JAMAIS D'UN JETON UNIQUE MORTEL (le relais compte de service, consigné le 29/10, porte les gestes de lecture — le jeton OAuth du relais est mort DEUX fois : 29/10, 05/11)

**Le contexte qui fonde la décision (05/11, la cérémonie de l'ère reçue).** Le développeur a exécuté la cérémonie hors-ligne (LISEZMOI-ceremonie-ere-M8.txt : la re-signature des 12 arbres, la règle d'or « JAMAIS generer ») et déposé signatures-I.txt dans le coffre /test. Le labo a recueilli la remise sur pièces : rapatriement md5 contrôlé, ancre de clé tenue (173fae9c…), puis LE RECOUP PROPRE À L'ÈRE : les DIX arbres inchangés portent les MÊMES signatures que celles déposées à la cérémonie 0.6.0 du 04/11 — la preuve que la clé du 04/11 a été réutilisée est NÉE DE LA COMPARAISON, pas d'une déclaration. Le dépôt canonique a suivi (l'atomicité : tout vérifié avant écriture), le garde est passé au vert 12/12 (m0 re-signé pour le registre étendu, m8 l'arbre neuf), et le build exécuté a donné l'artefact 0.9.0-dev.1 IDENTIQUE à la pièce de vérification du Task 76 — le même sha 1492b0bc… sur un AUTRE poste, après un AUTRE recyclage du disque : le déterminisme n'est pas une espérance, il est constaté.

**Les règles.** (1) **La preuve de continuité d'une clé de cérémonie est le déterminisme Ed25519** : la signature d'un message fixe par une clé fixe est reproductible bit à bit (RFC 8032) ; une remise de re-cérémonie qui re-signerait les arbres inchangés avec LA MÊME clé rend les MÊMES signatures — le recoup les compare aux déposées : IDENTIQUES = la clé est la même (prouvé), DIVERGENTES = une clé neuve a signé (l'ARRÊT : la continuité de l'état « réelle » serait rompue, la remise est refusée). Le labo fait cette preuve SANS jamais voir la clé privée : la moitié publique déposée + le déterminisme suffisent. (2) **La remise d'une re-cérémonie couvre TOUS les arbres** (spec § 5 : une rotation couvre tout) mais SEULS les arbres mutés/nouveaux changent de signature — les empreintes des autres ne bougent pas, et leurs signatures re-déposées sont les anciennes : c'est le VECTEUR de la preuve (1). (3) **L'artefact d'un build est prouvé AVANT de naître quand le build est déterministe** : la pièce de vérification par pièces détachées (Task 76) avait annoncé 1492b0bc… AVANT la cérémonie ; le build d'après-cérémonie sur un autre poste a donné le même sha — l'égalité constatée est la preuve que NI le garde ni la cérémonie ni le poste n'influencent les octets. (4) **L'accès au coffre Drive ne dépend jamais d'un jeton unique mortel** : le jeton OAuth du relais (refresh token d'une application en mode test) est mort DEUX fois (29/10, 05/11) — chaque ré-émission sur un poste révoque la précédente ; le RELAIS COMPTE DE SERVICE (clé posée à .gdrive/, JWT RS256, mécanisme relais_service_account.py) est la voie de reprise CONSIGNÉE, étendue au sondage LECTURE SEULE du coffre entier (scripts/sonder_coffre_sa.py : racine, /Cérémonie, miroir, /test) et au rapatriement des pièces (scripts/rapatrier_ceremonie_m8.py) ; le jeton OAuth peut être re-lancé par le développeur quand il le veut — les gestes ne l'attendent plus.

**Alternatives rejetées.** Faire confiance à la remise sans le recoup de l'ère (rejeté : « sur pièces, jamais sur mémoire » — la règle d'or du LISEZMOI dit « JAMAIS generer », la preuve que le développeur l'a suivie est la comparaison, pas la confiance) ; déposer la remise sans le recoup préalable (rejeté : le dépôt vérifie cryptographiquement, mais le recoup NOMME l'écart d'ère AVANT toute écriture — un dépôt refusé par sceau_I.py n'aurait pas dit SI la clé était la bonne) ; attendre le retour du jeton OAuth pour rapatrier (rejeté : le relais compte de service existe PRÉCISÉMENT pour ça, constaté le 29/10 — le geste ne se bloque pas sur un jeton mortel) ; re-signer au labo pour « débloquer » le build (rejeté : D87/D162 — le labo ne signe jamais, la clé de test déclasserait l'état « réelle »).

**Frontières.** La présente décision est la clôture de la dette D162 : la cérémonie de l'ère est PASSÉE (12/12 verts, état « reelle » intact), l'artefact 0.9.0-dev.1 est NÉ (44 544 o, sha256 1492b0bc0792e1ab…, la carte génération 8 vivante, le témoin e9cd8c549485… ne bouge pas) — c'est un GESTE DE BUILD, JAMAIS un scellage : la finale 0.9.0 attend le run terrain vert du chantier (d), aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; le scellé 0.6.0 INTACT (l'ancre R7 : 44 blocs octet-identiques au nouveau-né) ; le SSN du terrain demeure INCONNU du labo. Les pièces de l'arrêt : download/ceremonie-ere-m8/signatures-I.txt (la remise rapatriée, md5 ab22512a6864…), v06/sceau-I/signatures/ (12/12, m0 re-signé + m8 neuf), v06/sceau-I/cle-publique-I.txt (173fae9c… l'ancre tenue), m8/proxy.exe (1492b0bc…), m8/carte/ (la génération 8), scripts/sonder_coffre_sa.py, scripts/rapatrier_ceremonie_m8.py (le recoup de l'ère).

## D164 — LA REPRISE CONFRONTE LES TROIS MIROIRS ET S'ALIGNE SUR LA POINTE GITHUB (le bundle Drive peut être UN GESTE EN RETARD : la passation D141 est la DERNIÈRE étape d'un geste — une session qui meurt entre le push et la passation laisse GitHub en avance ; la reprise FETCH GitHub D'ABORD, s'aligne sur la pointe consignée, PUIS rejoue la passation) ; LE RAPATRIEMENT DE LA ZONE download/ PRÉCÈDE maj_kit.py — LE PIÈGE DU MANIFESTE AMPUTÉ S'EST RE-DÉCLENCHÉ (consigné 132/159, rejoué 05/11 : le manifeste régénéré couvrait 56 entrées d'un kit réel de 62 — les 6 LISEZMOI ignorés ; désamorcé PAR LE RAPATRIEMENT CANONIQUE 6/6 md5 MATCH puis rejeu 62/62) ; LE JETON RELAIS MIS À JOUR PAR LE DÉVELOPPEUR REDEVIENT LE CANAL D'ÉCRITURE (le coffre répond 200 : miroir rc=0, kit 62/62, bundle déposé — le compte de service demeure la voie de repli consignée D163)

**Le contexte qui fonde la décision (05/11, la reprise « on reprend ce projet »).** Le développeur annonce la reprise : signatures au /test, jeton relais mis à jour au /Tokens. La reprise depuis le bundle Drive (080-b7b6e01, la pointe consignée par la passation du Task 77) a suivi la méthode A — puis le recoup GitHub a nommé la divergence : **origin à 9193019, UN COMMIT EN AVANCE du bundle**. Le geste absent du bundle était le Task 78 d'une session précédente (la cérémonie installée + le build 0.9.0-dev.1 né, poussé à GitHub) : la session était morte ENTRE le push et la passation — la passation est la DERNIÈRE étape d'un geste, le bundle ne portait donc PAS la pointe. Le travail parallèle refait au labo (cérémonie vérifiée-déposée, garde repassé, build exécuté) a produit un commit DOUBLON du geste consigné : l'écart a été nommé par le recoup ls-remote AVANT toute consignation (aucune entrée de journal doublée), l'alignement s'est fait par reset à la pointe consignée (D159 rejouée : ce qui est consigné revient), et le doublon a été écarté — ses pièces substantielles étaient les MÊMES par déterminisme (l'artefact régénéré au geste de reprise : sha256 1492b0bc… == la pièce de D163 ; les signatures du sceau : identiques — la remise du développeur ne peut donner QUE ces octets). Dans le même geste, maj_kit.py joué depuis un labo amputé a régénéré un MANIFESTE de 56 entrées pour un kit réel de 62 fichiers — le piège des Entrées 132/159, exactement comme documenté ; le rapatriement canonique (6/6 LISEZMOI, md5 contrôlés contre les MÉTADONNÉES Drive après écriture) puis le rejeu ont rendu le manifeste complet (62/62 vérifiés aller-retour).

**Les règles.** (1) **La reprise confronte les TROIS miroirs AVANT de travailler** : le dépôt local (s'il survit), GitHub (ls-remote/fetch — LA POINTE), le bundle Drive (la passation — potentiellement UN GESTE EN RETARD). L'alignement se fait TOUJOURS sur la pointe GitHub consignée ; si GitHub est en avance du bundle, la passation est REJOUÉE au geste de reprise (le bundle rattrape la pointe). (2) **Un geste n'est terminé que par sa passation** : le push GitHub seul ne suffit pas — D141 exige le bundle à la pointe ; une reprise qui constate l'avance GitHub sans rejouer la passation laisse la dette d'infrastructure ouverte. (3) **Le rapatriement de la zone download/ précède maj_kit.py** (la règle des Entrées 132/159, à présent DOCTRINE : le script canonique rapatrier_lisezmoi_ceremonie.py — contrôle md5 par fichier APRÈS écriture — est joué chaque fois que le labo a été recyclé, AVANT tout rejeu du déploiement du kit ; un manifeste amputé est une attestation mensongère, même avec 56/56 verts sur ses 56 entrées). (4) **Le jeton relais du développeur redevient le canal d'écriture quand il répond** : la mise à jour au /Tokens est le geste du développeur qui ROUVRE le canal OAuth (check_auth.py : échange 200, listing 200) ; les gestes d'écriture (miroir, kit, bundle) reprennent par lui ; le relais compte de service (D163) demeure la voie de repli pour la lecture — jamais les deux ne sont requis ensemble, l'un des deux suffit.

**Alternatives rejetées.** Reprendre depuis le bundle sans recouper GitHub (rejeté : c'est le geste de cette session qui le prouve — le bundle était EN RETARD d'un geste ; travailler depuis un état périmé produit des doublons parallèles) ; merger le commit parallèle avec la pointe (rejeté : le journal append-only n'accepte pas deux Entrées 160 — l'alignement à la pointe consignée est la seule voie propre, le parallèle n'apporte RIEN que le déterminisme n'ait déjà prouvé) ; rejouer maj_kit.py sans rapatriement après un recyclage (rejeté : le manifeste amputé est le piège documenté DEUX fois — la troisième fois il est doctrine) ; attendre le canal OAuth pour le recoup de lecture (rejeté : D163 — le compte de service porte la lecture, le geste ne se bloque pas).

**Frontières.** La présente décision est une décision d'INFRASTRUCTURE DE REPRISE : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), l'artefact 0.9.0-dev.1 est INTACT (1492b0bc… — régénéré identique au geste de reprise, la preuve de déterminisme s'accumule), le garde demeure VERT 12/12 (état « reelle »), la passation rejouée porte la série 080 à la pointe 9193019 (l'ancien b7b6e01 archivé versionné — 25 archives, rien supprimé). Les pièces de l'arrêt : le recoup ls-remote (9193019 vs 7079df1), le bundle triade-history-080-9193019.bundle (md5 a8cd69f8…, déposé et relu MATCH), le manifeste complet du kit (62/62), scripts/rapatrier_lisezmoi_ceremonie.py (le rejeu canonique, labo), scripts/passe_bundle_m8c_execution.py (la passation rejouée, dépôt).

## D165 — LA FINALE D'UNE ÈRE SE SCELLE SUR LE RECOUP TERRAIN EXIGÉ COMME PIÈCE (le scellage REFUSE en l'absence du verdict du recoup vert : la porte est de PROCESSUS, jamais de console — D138/D145/D148/D154 étendues au geste final) ; LE SCELLAGE EST UN FAIT DE CARTE, L'ARTEFACT NE BOUGE JAMAIS (la balise vit dans frag-bld, l'entête la porte, proxy.exe demeure byte-identique 1492b0bc…) ; LE SSN DU TERRAIN DEMEURE INCONNU DU LABO (RE-LU de l'imm32 du stub consigné, rendu par les DEUX lecteurs, PROUVÉ par le geste de la twin — le numéro n'est jamais cru, jamais su) ; L'INSTRUMENT DU RECOUP S'INSTRUIT AVANT LES PIÈCES (DEUX défauts nommés par le fail-closed en un geste, corrigés et rejoués, les pièces immuables — D154 re-vivante)

**Le contexte qui fonde la décision (05/11, le geste final M8-(d)).** Le développeur a rejoué le run sur le kit corrigé et déposé les pièces au coffre /test/preuves-m8d/. Le labo a rapatrié (md5 contrôlés), recoupé (30 contrôles : pièces, témoin, journal, verdict, fichiers du geste re-contrôlés octet par octet, chaîne du scellé) — VERT 30/30. Deux défauts d'INSTRUMENT ont été nommés par le fail-closed pendant le geste (un « $ » sans re.M ; une tranche de sortie amputant la première attestation du verdict écrit — attrapée par LE SCELLAGE lui-même, qui exige les six attestations de pièces) : corrigés, rejoués, les pièces n'ont pas bougé d'un octet. Puis la cristallisation (10 passes, 55 blocs à 10/10) et le scellage : la balise 0.9.0-dev.1 → 0.9.0 basculée DANS LA CARTE (frag-bld, occurrence unique vérifiée en mémoire avant l'unique écriture), l'entête porte la balise, la signature re-signée à la graine durable, le tableau suit — et proxy.exe INTACT.

**Les règles.** (1) **La finale d'une ère exige le verdict du recoup terrain COMME PIÈCE** : --sceller-final refuse nommément si VERDICT-recoup-m8d.txt est absent, non « VERT 30/30 », ou sans les six attestations de pièces — la validation terrain n'est jamais une parole, toujours une pièce croisée. (2) **Le scellage est un fait de carte** : l'artefact ne bouge jamais (sha constaté avant et après), la balise vit dans frag-bld, l'entête de carte la porte (construire_entete paramétré — la cohérence entête/frag-bld est vérifiée à chaque re-signature), le tableau de bord est CONSCIENT de la balise (la ligne preversions nomme le geste qui a scellé). (3) **Le SSN du terrain demeure une donnée du témoin, jamais du labo** : le labo ne le devine pas, il RE-LIT l'imm32 du stub consigné, constate la parité des DEUX lecteurs et la distinctivité du second nom, et tient la preuve du geste (la twin == le fixture octet par octet — un SSN faux n'aurait pas écrit la ligne). (4) **L'anti-rollback est vivant après le scellage** : la reconstruction REFUSÉE nommément, la re-vérification demeure licite sous la balise scellée (cristallisation continue, verrou croisé re-constaté).

**Alternatives rejetées.** Sceller sur la console du développeur (rejeté : D138/D145/D148 — sur pièces, jamais sur console) ; sceller sans la 10/10 (rejeté : R6 — la cristallisation est exigée au scellage, dix passes la constituent) ; re-générer l'artefact « en 0.9.0 » (rejeté : le scellage est un fait de carte — l'octet ne bouge pas, un artefact régénéré serait un AUTRE artefact) ; traiter le SSN 8 comme une connaissance du labo (rejeté : c'est une donnée du témoin de la machine du développeur — le labo ne la connaît pas, il la recoupe) ; laisser le verdict amputé passer (rejeté : le scellage a REFUSÉ — le fail-closed a fait son travail, l'instrument corrigé et rejoué).

**Frontières.** Les balises win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES ; l'artefact 0.9.0 == l'artefact 0.9.0-dev.1 (1492b0bc…, 44 544 o — le même octet, une autre balise de CARTE) ; le scellé 0.6.0 demeure l'ancre R7 ; l'état de clé du sceau « réelle » intact ; les pièces au coffre /test/preuves-m8d/ jusqu'à la clôture D143. Les pièces de l'arrêt : download/preuves-run-m8d/ (les six pièces + VERDICT-recoup-m8d.txt), m8/carte/ (la balise 0.9.0, entête + frag-bld + signature), m8/build_m8.py (--sceller-final), scripts/rapatrier_preuves_m8d.py, scripts/recouper_run_m8d.py.

## D166 — LA SECONDE FAMILLE DE L'ÈRE EST OUVERTE : TLS 1.3 PUR EN BLOCS SCELLÉS (le jalon M9, le domaine `tls13`, l'ère 1.0.0) ; la demande du développeur « on ouvre la suite » EST la décision d'ouverture (le modèle D149/D160 : l'ordre des familles est LA FONDATION D'ABORD) ; L'ÈRE M8 REFERMÉE PROPRE PAR L'EXPORT DE CONTINUITÉ 0.9.0 (le conteneur régénéré porte la carte 0.9.0 scellée — win 0.9.0 / linux 0.7.0 / riscv 0.8.0, import à sec + rituels VERTS, la copie au coffre racine md5 MATCH par relecture) ; LA DETTE DE CÉRÉMONIE NOMMÉE À LA NAISSANCE (le garde constate m0 CODE 10 + tls13 CODE 12 au geste même — la remise du développeur précède tout build, D162 rejouée volontairement)

**Le contexte qui fonde la décision (05/11, au lendemain de la finale 0.9.0).** Le jalon M8 est franchi (D165 : le run terrain VERT, le recoup 30/30, la finale scellée — fait de carte, l'artefact 1492b0bc… INTACT), la passation D141 et la clôture D143 sont passées, le programme d'après M7 (D160) compte sa première famille ACCOMPLIE. La demande du développeur « on ouvre la suite » est la décision d'ouverture de la seconde famille — TLS 1.3 pur, « la grande œuvre de la souveraineté complète » — et l'ordre de D160 la fondait déjà sur des résultats MESURÉS : le domaine `sys` est la fondation I/O (l'IAT-free que M8 a nommé : « une pile TLS pure qui émettrait encore par l'IAT userland garderait la surface de hook qu'elle prétend éliminer »), SHA-256 existe en contrats scellés (ah-04..07, M6), l'arithmétique f25519 est prouvée (av-05..11, M7) — la couche I hérite par CITATION, jamais par copie aveugle.

**Les règles.** (1) **L'ère M8 se referme PROPRE avant l'ouverture** (le modèle Entrée 156 rejoué) : l'export de continuité multiprofils est RÉGÉNÉRÉ à la carte 0.9.0 scellée — l'instrument étendu au scellé win COURANT (m8/proxy.exe 0.9.0 + la carte génération 8, les couches I m0..m5 + m8), le conteneur TRIADE-continuite-multiprofils-0.9.0-20261105T115943Z.bin (779 272 o, md5 3de022b7…) porte les TROIS profils à leur état scellé (win 0.9.0 / linux 0.7.0 / riscv 0.8.0), l'import à sec CINQ étapes VERT, la preuve d'exécution VERT (les rituels rejoués sur les octets TRANSPORTÉS — le scellé win au poste Windows, frontière nommée), la copie au coffre racine relu MATCH ; les anciens conteneurs 0.8.0 DEMEURENT (rien ne se jette). (2) **Le domaine s'appelle `tls13`** — l'identifiant `tls` est PRIS par M4 (la poignée Schannel) et « un identifiant n'est jamais réutilisé » ; les blocs tls13-01..28, les identifiants machine h10xxxx (la famille `h` est libre : la carte génération 8 porte a/b/c/e/g). (3) **La suite est ARRÊTÉE : TLS_AES_128_GCM_SHA256 + x25519** — la suite que la RFC 8446 exige de toute implémentation, le groupe RFC 7748 ; le ClientHello propose CETTE suite seule, un ServerHello divergent est le verdict -5 NOMMÉ (le domaine ne propose jamais ce qu'il ne prouve pas). (4) **Le rôle est CLIENT** (l'initiateur) ; le miroir serveur est un chantier futur nommé. (5) **La décision de confiance est une COMPARAISON, jamais une croyance** : le certificat confronté à l'empreinte ÉPINGLÉE de l'appelant ; l'analyse X.509 complète est un CHANTIER FUTUR NOMMÉ — le jalon ne fait pas confiance en silence, il compare et nomme la frontière. (6) **Le transport vit au domaine `sys`** (le socle socket sys-04+, chantier (d) du jalon) : au harnais un SIMULATEUR (fixtures), au terrain les syscalls directs — JAMAIS l'IAT ws2_32 (la surface de hook que M8 a nommée). (7) **La couche I est écrite-avant-code** (R2) : la charte à HUIT règles (la suite constante, les vecteurs officiels AVANT usage, le temps constant NOMMÉ par bloc, le transcript source de vérité, l'échec propre et nommé, le bloc ne détient rien, aucun import aucun syscall, le padding NOP), le tableau des 28 blocs en SIX familles (sha, hkdf, x25519, aead, enregistrement, poignée + principal) — la famille `sha` LIVRÉE à l'ouverture (les 4 miroirs win des contrats ah-04..07, le contexte en ARGUMENT : TLS exige des hachages multiples simultanés), les familles restantes se posent AVANT toute notation ; le plan d'adressage PRÉFIGURÉ (tls13/layout.py : la 8e section .text6, les versions 1.0.0-dev.1/1.0.0, la table des SEPT verdicts, les H0 FIPS) — **la préfiguration n'est pas un droit** (D161 : les slots s'arrêtent à la notation sur les longueurs réelles). (8) **La dette de cérémonie est nommée à la naissance** : le registre figé m0 s'étend au domaine tls13 (un diff d'intention) et l'arbre tls13/I est neuf — le garde CONSTATE au geste m0 CODE 10 + tls13 CODE 12, la charge a-signer.txt est PRÉPARÉE (13 arbres, remise minimale m0 + tls13) ; AUCUN build avant la remise du développeur (sa clé hors-ligne, D87/D162 — le refus nommé est le résultat, pas la panne).

**Alternatives rejetées.** Ouvrir la troisième famille (les profils additionnels) d'abord (rejeté : D160 — la fondation d'abord, TLS s'appuie sur le domaine sys MESURÉ ; les profils répéteraient M6/M7 sur résultats mesurés) ; ouvrir la PEB-walk / la contre-mesure du hooking d'abord (rejeté : ce sont les chantiers futurs NOMMÉS du domaine sys — le durcissement, pas la fondation que TLS attend) ; le transport par l'IAT ws2_32 (rejeté : la couche I du M8 l'a nommé — la surface de hook demeurerait) ; la vérification X.509 complète AU jalon M9 (rejeté : un jalon à lui seul — l'épinglage honnête NOMMÉ vaut mieux qu'une analyse à moitié prouvée) ; le rôle serveur en miroir (rejeté : le client prouve le critère — l'observable de la session établie) ; réutiliser l'identifiant `tls` (rejeté : M4 le détient, jamais réutilisé) ; sceller une balise à l'ouverture (rejeté : la 1.0.0-dev.1 naîtra du premier BUILD du jalon, geste de BUILD — jamais un scellage, D162/D165).

**Frontières.** AUCUNE balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; l'artefact m8/proxy.exe INTACT (1492b0bc…, 44 544 o — FAIT DE CARTE) ; le garde REFUSE tout build M9 jusqu'à la cérémonie de l'ère (m0 CODE 10, tls13 CODE 12 — constatés) ; les 24 spécifications restantes précèdent toute notation (R2) ; l'anti-rollback du scellé 0.9.0 demeure armé. Les pièces de l'arrêt : tls13/I/ (README la charte + tls13-01..04 la famille sha), tls13/layout.py (la préfiguration), m0/I/README.md (le registre figé étendu), v06/sceau_I.py (la table à 13 arbres), v06/sceau-I/a-signer.txt (la charge du développeur), riscv/export_continuite.py (l'instrument étendu au scellé 0.9.0), riscv/export/TRIADE-continuite-multiprofils-0.9.0-20261105T115943Z.bin (md5 3de022b7…, au coffre racine relu MATCH).

## D167 — LE CHANTIER M9-(a) SE CLÔT SUR LES 28 SPÉCIFICATIONS AVANT TOUT OCTET DE NOTATION (R2 : la couche I complète — les 24 du geste en SIX familles, l'instrument 117 VERTS) ; LES CONSTANTES DU PLAN SONT DÉRIVÉES PAR ARITHMÉTIQUE, JAMAIS COPIÉES D'UNE SPEC (l'erratum av-10 : quatorze chiffres hexadécimaux pour un membre de 51 bits — l'écriture fautive, la notation prouvée demeurée juste) ; LE MIROIR NOMME SES DIVERGENCES ET SES AMÉLIORATIONS SUR L'HÉRITAGE f25519 (le gel SANS branche de données — l'amélioration sur av-10 exigée par la charte § 3 ; l'échelle EN PILE — la divergence sur av-11 exigée par la charte § 6, la réentrance par construction) ; L'ARRÊT AES-NI ET L'ABSENCE DE LA BRIQUE D'INVERSION (le S-box matériel temps constant, jamais la table indexée par la clé ; le GCM re-chiffre les compteurs — la découpe le nomme au lieu de le cacher)

**Le contexte qui fonde la décision (05/11 au soir).** La couche I du M9 était ouverte à la famille `sha` (Entrée 165, D166) ; le travail restant était nommé : « les 24 spécifications restantes (hkdf, x25519, aead, enregistrement, poignée, principal — R2) ». Le geste les pose TOUTES, la charte à HUIT règles instanciée bloc par bloc, et clôt le chantier (a) sur une preuve d'instrument (117 contrôles VERTS après trois défauts nommés par le fail-closed — l'instrument s'instruit avant les pièces, D165 rejouée). Un erratum d'HÉRITAGE est consigné au passage : la spec av-10 (M7) porte une écriture hexadécimale impossible pour le membre 0 de p — la preuve par la largeur (quatorze chiffres = 55 bits ≠ 51) et par l'oracle (le vecteur « p → 0 » ne passe qu'avec la valeur juste) ; le miroir ne réécrit pas la spec scellée du M7, il RE-DÉRIVE sa propre constante et cite.

**Les règles.** (1) **La couche I se clôt sur la preuve, pas sur l'annonce** : le chantier (a) est RÉALISÉ parce que l'instrument constate 28/28 specs présentes et bien formées, la table des identifiants h100001..h100028 (DÉCIMAUX, le miroir des g9xxxx du M8), les constantes du plan re-dérivées, les constructions re-jouées (le ClientHello 114 o, le ServerHello minimal 90 o, la session 17 520 o recomptée) et les verdicts cités vivant dans la table des SEPT. (2) **Une constante du plan est DÉRIVÉE par arithmétique ou elle n'est pas** : l'erratum av-10 devient la règle — le miroir ne copie jamais l'hexadécimal d'une spec, il re-dérive (le juge est le code) ; l'instrument RE-DÉRIVE au geste même (les membres de p, p − 2, la valeur magique HRR par SHA-256 re-calculé, R). (3) **Le miroir NOMME chaque divergence et chaque amélioration sur l'héritage** : la passe propagation+gel FUSIONNÉE en une frontière d'appel (av-06+av-10 → tls13-12) ; le gel SANS branche de données (l'amélioration sur av-10 : la sélection par masque sar — les intermédiaires de l'échelle sont des secrets, charte § 3) ; l'échelle EN PILE (la divergence sur av-11 : le M7 tenait ses zones en .bss, la charte § 6 l'interdit — le bloc est réentrant par construction) ; l'arrêt AES-NI (AESKEYGENASSIST/AESENC/AESENCLAST : le S-box matériel, jamais la table logicielle indexée par la clé) ; AUCUNE brique d'inversion AES (le GCM re-chiffre les compteurs : la découpe le NOMME) ; GHASH sans table par donnée (PCLMULQDQ chantier futur nommé — la marche binaire est la transcription exacte de la norme). (4) **Les bornes sont nommées, jamais tacites** : la charge 2^14 (RFC 8446 § 5.1), le réassemblage de poignée 2^14 (le certificat du monde réel y tient — la borne du jalon), la boucle HKDF 8160 (l'octet compteur), l'alerne autre que close_notify → l'état MORT (le couple niveau/description CONSIGNÉ au tampon — l'information n'est jamais muette). (5) **La machine d'états tient la poignée ENTIÈRE par la rotule** : OUVRIR fait CH → SH → {EE, Cert, CV, Fin} → Finished client en UNE boucle bloquante sur les rappels du socle tls13-28 (le transport est un ARGUMENT pointé — NI import NI syscall, la liste des compositions est FERMÉE) ; le hash du transcript est COPIÉ puis la copie finalisée (l'original vit — RFC 8446 § 7.1 exige le hash courant à chaque étage).

**Alternatives rejetées.** Poser les familles au fil des chantiers suivants (rejeté : R2 exige la spec AVANT la notation — la couche I entière précède, le chantier (b) n'ouvrira pas sur une spec à écrire) ; copier les constantes des specs M6/M7 (rejeté : l'erratum av-10 le prouve — une écriture fautive copiée serait une constante fausse) ; garder le gel à branches du M7 (rejeté : la charte § 3 du M9 nomme les secrets — l'amélioration est exigée, elle est nommée) ; l'échelle en .bss comme av-11 (rejeté : charte § 6 — la pile suffit, la réentrance est gratuite) ; une brique AES de déchiffrement par symétrie apparente (rejeté : le GCM n'en a JAMAIS besoin — le CTR re-chiffre ; une brique inutile serait une surface inutile) ; la table de Shoup pour GHASH (rejeté : indexée par donnée — charte § 3) ; la vérification CertificateVerify au jalon (rejeté : chantier futur nommé avec l'analyse X.509 — l'épinglage tranche la confiance, le domaine le NOMME) ; un huitième verdict « alerne » (rejeté : la table des SEPT est scellée par la charte — l'alerne fatale passe par l'état MORT et le -3, le couple consigné ; on n'étend pas une table scellée en silence).

**Frontières.** AUCUNE balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; AUCUN octet de notation tls13 n'existe (R2 tenue) ; AUCUN build avant la remise du développeur (le garde m0 CODE 10 + tls13 CODE 12 — la dette de cérémonie demeure, c'est son travail) ; la spec av-10 du M7 DEMEURE TELLE QUELLE (l'erratum vit dans la couche M9, la pièce scellée ne se réécrit pas) ; m8/proxy.exe INTACT (1492b0bc…). Les pièces de l'arrêt : tls13/I/tls13-05..28, tls13/layout.py, tls13/I/README.md (la clôture + l'erratum), scripts/verifier_specs_m9a.py (117 VERTS).

## D168 — LA CHARGE DE CÉRÉMONIE SE PRÉPARE AU GESTE DE LA CÉRÉMONIE (la charge de l'ouverture était PÉRIMÉE par le geste des 24 specs : une empreinte sur treize avait bougé — tls13 0ef882d6… → 9ff91874… ; preparer rejoué, UNE ligne, les douze autres octet-identiques — une remise signée sur la charge périmée aurait laissé tls13 CODE 10 APRÈS installation : la cérémonie aurait échoué son objet) ; LE KIT DE L'ÈRE M9 DÉPOSÉ AU /Cérémonie (modèle Entrée 159 : le LISEZMOI pas à pas + la remise FRAÎCHE + les outils — la main du développeur SERVIE, md5 contrôlés par relecture) ; L'ERRATUM DE LA LIGNE SUITE DE L'ENTRÉE 166 (le garde exige la remise pour LE BUILD — construire(), chantier (e) — jamais pour la notation : le miroir M8, Entrées 157/158 ; la correction consignée en tête du geste suivant, le journal n'étant jamais réécrit)

**Le contexte qui fonde la décision (05/11 au soir, le geste du kit).** Le SUITE du Task 84 nommait le kit de cérémonie au /Cérémonie (modèle Entrée 159). Au geste de le servir, la confrontation a nommé une PÉREMPTION : la charge a-signer.txt préparée à l'OUVERTURE du M9 portait l'empreinte de l'arbre tls13 ALORS naissant (README + 4 specs sha) — le geste des 24 spécifications avait fait bouger l'arbre, la charge ne correspondait plus. Le garde constatait au geste même : m0 DIVERGE (le registre étendu), tls13 DEPOT INCOHERENT (jamais signé) — la dette de cérémonie exactement telle que D166 l'avait nommée à la naissance.

**Les règles.** (1) **La charge se prépare AU GESTE DE LA CÉRÉMONIE** : l'ouverture ANNONCE (sa charge est un constat provisoire de l'état), la cérémonie EXIGE la charge DE L'ARBRE COURANT — préparée dans le geste qui sert la main du développeur. La preuve par le geste : tls13 0ef882d6… (l'ouverture) ≠ 9ff91874… (l'arbre complet des 28 specs) ; une remise signée sur la charge périmée aurait installé un manifeste divergent de l'arbre — tls13 serait DEMEURÉ CODE 10, le geste du développeur gaspillé. (2) **Le kit sert la main** : le LISEZMOI porte les DEUX empreintes qui exigent la signature (m0 4ebe6a2c…, tls13 9ff91874…), les onze autres inchangées (le déterminisme Ed25519 les rendra identiques — la preuve D163), LA RÈGLE D'OR (« JAMAIS generer » : la clé du 04/11 réutilisée, l'état « reelle » ne se régresse pas), les pas à pas console ET graphique, l'atomicité du dépôt, et le contrat D87 (la clé privée ne traverse jamais le bac à sable — le labo ne signera jamais à la place du développeur). (3) **Le dépôt se recoupe** : le LISEZMOI téléversé md5 par relecture ; la remise du kit == celle du dépôt (la synchro D130 porte la charge régénérée dans le geste du commit — le kit ne peut pas prendre un coup de retard). (4) **L'erratum se consigne, il ne réécrit pas** : la ligne SUITE de l'Entrée 166 disait le chantier (b) « APRÈS la remise (le garde le requiert) » — le garde exige la remise pour LE BUILD (construire(), le chantier (e)), pas pour la notation (le miroir M8 : Entrée 157 précéda Entrée 158) ; la correction vit EN TÊTE du geste suivant, le journal append-only ne se réécrit jamais.

**Alternatives rejetées.** Déposer le kit avec la charge de l'ouverture (rejeté : périmée — la cérémonie aurait échoué son objet APRÈS le geste du développeur : le pire des gaspillages) ; régénérer la charge à CHAQUE geste (rejeté : la charge n'a d'objet qu'au geste de la cérémonie — la régénérer au chantier (a) l'aurait périmée au chantier (b) : la règle est le geste qui sert la main, pas un rythme) ; corriger l'Entrée 166 en place (rejeté : append-only — l'erratum en tête du geste suivant, jamais la réécriture) ; laisser la ligne SUITE imprécise (rejeté : le prochain chantier s'ouvrirait sur une fausse dépendance — la notation n'attend pas la remise, le build oui) ; signer au labo pour épargner le développeur (rejeté : D87 — la clé de TEST déclasserait l'état « reelle », une régression de preuve).

**Frontières.** AUCUNE balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; AUCUN build avant la remise (le garde m0 CODE 10 + tls13 CODE 12 — la dette EST le verrou, il fait son travail) ; AUCUN octet de notation (R2) ; la charge périmée de l'ouverture DEMEURE dans l'histoire (le diff du geste la cite — rien ne se jette). Les pièces de l'arrêt : v06/sceau-I/a-signer.txt (13 arbres, tls13 9ff91874…), LISEZMOI-ceremonie-ere-M9.txt (au /Cérémonie, md5 recoupé), scripts/deposer_lisezmoi_ere_m9.py, l'état du sceau au geste (check_auth.py : m0 DIVERGE + tls13 DEPOT INCOHERENT + 11 verts).
## D169 — LA SPÉCIFICATION v0.7.0 : LA CONSOLIDATION DU PROGRAMME D'APRÈS M7 (le jalon M8 — le domaine `sys`, les syscalls directs — franchi, finale 0.9.0 scellée sur run terrain vert recoupé 30/30 ; le jalon M9 — le domaine `tls13`, TLS 1.3 pur — ouvert, sa couche I complète, SA CÉRÉMONIE D'ÈRE PASSÉE le 05/11 [13 arbres, garde 13/13, la dette D166 soldée] ; le sceau de l'Intention portant TREIZE arbres et ses cérémonies d'ère entrant au protocole) ; LA CLAUSE « HORS PÉRIMÈTRE COURANT » EST LEVÉE NOMMÉMENT POUR LES DEUX PREMIÈRES FAMILLES (D160), les profils additionnels demeurant hors périmètre

**Le contexte qui fonde la décision (05/11 au soir, la demande du développeur).** « Je voudrais que tu produises la dernière version complète du document pdf Protocole TRIADE. » La demande arrive au moment nommé : la cérémonie de l'ère M9 vient d'être installée (le garde 13/13) et la spécification vivante est EN RETARD SUR LE PROGRAMME sur quatre points nommés — le § 12.4 dit « Dix arbres » alors que le sceau en porte treize ; le § 18 titre « jalons M0 à M7 » alors que M7 est franchi (0.8.0, Entrée 155) et que M8/M9 n'y figurent pas ; la clôture du § 21 tient les syscalls directs et TLS 1.3 pur « hors périmètre courant » alors que D160/D166 les ont ouverts et que M8 est FRANCHI ; l'état des jalons de l'en-tête s'arrête à M6. Le versionnement suit les RÉVISIONS, jamais les franchissements (addendum Task 62) — mais un PROGRAMME entré en exécution EST une révision en attente de sa passation : la v0.7.0 est la passation du programme d'après M7 dans la spécification, le miroir exact de ce que D133 fit pour la souveraineté cryptographique.

**Les règles.** (1) **Le programme d'après M7 entre en spécification** : la clause « hors périmètre courant » de la clôture v0.6.1 est LEVÉE NOMMÉMENT pour les deux premières familles (syscalls directs — accompli ; TLS 1.3 pur — en cours), les profils additionnels demeurent hors périmètre (chacun répétera M6/M7 sur résultats mesurés). (2) **Le sceau est consigné à son état réel** : TREIZE arbres (m0–m8, tls13, demo, terrain, v06) et les cérémonies d'ère entrent au protocole (§ 12.4, § 13.5) — la dette se nomme à la naissance (D166 règle 8), la charge se prépare au geste qui sert la main (D168), la continuité de clé se prouve par le déterminisme Ed25519 (D163). (3) **L'état des jalons est constaté** : M0–M8 franchis (balises 0.2.0 à 0.9.0), M9 ouvert — la cérémonie de son ère passée sur pièces. (4) **Aucune règle du cœur n'est modifiée, aucune couche n'est ajoutée à l'exécution, la hiérarchie est inchangée** — la révision consolide, elle ne légifère pas.

**Alternatives rejetées.** Régénérer la seule v0.6.1 sur les sources courantes (rejeté : le document aurait continué de dire « dix arbres » et de tenir M8/M9 hors spécification — la demande porte sur la DERNIÈRE version COMPLÈTE, pas sur la plus récente impression de l'ancienne) ; attendre la finale 1.0.0 pour réviser (rejeté : la consolidation suit le PROGRAMME, pas la finale — la cérémonie d'ère passée est le moment nommé, le précédent D133 fut la passation du programme accompli) ; signer les sources `docs/` sous le sceau courant (rejeté : le modèle par-version demeure, `v06/I/README.md` § 1) ; ouvrir les profils additionnels dans la même révision (rejeté : hors périmètre, sur résultats mesurés) ; réviser à chaque franchissement (rejeté : le versionnement suit les RÉVISIONS — la présente est la passation d'un programme, pas un constat de plus).

**Frontières.** Les balises INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 — la révision documente, elle ne scelle rien) ; l'archive v0.6.1 DEMEURE (docs/Protocole_TRIADE_v0.6.1_Specification.pdf, dernier build consigné sha256 4aac10f1…, 984 555 o — rien ne se jette) ; le *Livre du Coffre* v1.1 INCHANGÉ (la révision ne touche pas le coffre) ; la chaîne spec_v061 devient spec_v070 par RENOMMAGE git (le modèle des révisions précédentes — l'ancienne chaîne reste dans l'histoire). Les pièces : docs/PROTOCOLE_TRIADE.md (v0.7.0), scripts/revision_v070_md.py + scripts/revision_v070_tex.py (les remplacements ASSERTÉS), scripts/spec_v070/ (la chaîne), scripts/spec_v070/verify_spec.py (le cahier V1–V16), docs/Protocole_TRIADE_v0.7.0_Specification.pdf (l'artefact, empreinte consignée PAR LE BUILD).
## D170 — LE JALON M9 FRANCHI : LA FINALE 1.0.0 SCELLÉE SUR LE RECOUP TERRAIN EXIGÉ COMME PIÈCE (le miroir D165 porté à l'ère M9 : le scellage REFUSE en l'absence du verdict du recoup vert — la porte est de PROCESSUS, jamais de console) ; LE SCELLAGE EST UN FAIT DE CARTE, L'ARTEFACT NE BOUGE JAMAIS (la balise 1.0.0 vit dans frag-bld, l'entête la porte, proxy.exe demeure byte-identique 446279f3… — LE MÊME binaire que LE SEPTIÈME RUN a couru) ; LA SESSION RÉELLE EST LE CRITÈRE DE LA RANGÉE (f) (la ligne applicative chiffrée ÉCHANGÉE avec un serveur réel, le témoin « HTTP/1.1 200 OK » DÉCHIFFRÉ PAR LA MACHINE, l'épinglage -6 NOMMÉ contre le vrai serveur, la fermeture propre — D166 tenue)

**Le contexte qui fonde la décision (07/11, au geste de la grande œuvre).** LE SEPTIÈME run M9-(f) — le premier du contrat réparé (l'erratum n° 10 : AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20) — est VERT sur pièces : LA SESSION RÉELLE ÉTABLIE (la poignée ENTIÈRE par LE CLIENT TLS 1.3 DE L'ARTEFACT, la mort -7 des runs 5/6 FRANCHIE, la ligne applicative déchiffrée par la machine, la garde contre le vrai serveur, la fermeture propre). Le recoup labo 34/34 sur pièces croisées (l'échelle rejouée sur la clé du run, la ligne reçue lue en clair, les cinq émissions recadrées sans reste). La condition nommée d'avance par la passation 110 (« ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE ») est REMPLIE.

**Les règles.** (1) **La finale se scelle sur pièces, jamais sur console** : le --sceller-final EXIGE le verdict du recoup terrain VERT (34/34 + les six attestations) — D138/D145/D148/D154 étendues au geste final, le miroir de D165 à l'ère M9. (2) **Le scellage est un fait de carte** : la balise 1.0.0 vit dans frag-bld (occurrence unique, bascule vérifiée EN MÉMOIRE), l'entête la porte, la racine re-dérivée, la signature Ed25519 re-signée (graine durable D144) — proxy.exe INTACT, le binaire que le terrain a couru EST le binaire final. (3) **L'anti-rollback ARME l'ère refermée** : la carte scellée (1.0.0) interdit la reconstruction (R6) — constaté au geste même ; la re-vérification sous la balise scellée demeure licite (R5/R7). (4) **La clôture D143 accompagne le scellage** : le run archivé AVEC son jugement (preuves-run-m9f-7/), le réceptacle ré-armé, le kit du jalon demeuré au coffre. (5) **Aucune règle du cœur n'est modifiée** — la décision constate un franchissement, elle ne légifère pas.

**Alternatives rejetées.** Sceller sans le recoup (rejeté : la porte est de processus — D165) ; rebâtir l'artefact à la balise 1.0.0 (rejeté : le fait de carte — l'artefact que le terrain a établi ne bouge jamais, un rebuild serait UN AUTRE binaire) ; poser la version PE 0x01000000 dans l'image (rejeté : la version PE @0x2820 demeure 0x01000004 — le geste de BUILD est passé, le scellage n'est pas un build) ; archiver le kit avec le run (rejeté : le kit RÉPARÉ demeure au /test, la pièce du jalon) ; ouvrir aussitôt l'ère suivante (rejeté : l'ouverture d'une famille est la décision du développeur — D160, le modèle D149).

**Frontières.** Le scellé 0.9.0 INTACT (l'ancre R7) ; les balises sœurs INTACTES (linux 0.7.0 / riscv 0.8.0) ; la clé privée jamais traversée (D87) ; les pièces de cérémonie demeurées (la TROISIÈME remise 0978c117… + l'ancre 188a7d42…). Les pièces : les SIX du run + le verdict du recoup aux archives-preuves/preuves-run-m9f-7/, la carte scellée tls13/carte/ (la balise 1.0.0), le verdict du recoup download/preuves-run-m9f-7/VERDICT-recoup-labo-m9f-7.txt (34/34).
## D171 — LE TEST GRANDEUR NATURE OUVERT : L'APPLICATION « LOUPE » ARBITRÉE (l'éditeur hexadécimal natif au panneau d'empreintes — coder une appli ENTIÈREMENT avec Triade, la demande du développeur) ; LE PROJET COFFRE-FORT DÉGELÉ EN PARALLÈLE (D135 amendée par le même message) ; LE DOMAINE `loupe` FONDÉ (la charte + le tableau des 18 blocs, la couche I écrite-avant-code — la dette de cérémonie nommée à la naissance)

**Le contexte qui fonde la décision (07/11).** Le message du développeur : « on peut commencer le test grandeur nature : coder une appli entièrement avec Triade. ça n'empêchera pas de continuer le projet Coffre Fort en parallèle ». L'ère 1.0.0 est refermée propre (D170 : la finale scellée sur le recoup terrain exigé comme pièce ; la passation D141 passée ; les trois miroirs alignés — la cohérence re-vérifiée à la pointe au geste d'ouverture de session, R4 17/17). Le programme D160 est accompli (les deux premières familles : M8 0.9.0, M9 1.0.0). Le TGN est la suite NATURELLE : le protocole a prouvé chaque capacité, il reste à prouver la MÉTHODE ENTIÈRE sur une application réelle neuve — le modèle RoomEq (v0.3, 44 spécifications) s'arrêtait au RECODAGE d'une application existante ; le TGN exige la CRÉATION. Le même message DÉGÈLE le projet fils Coffre-Fort (D135 : le développement en était différé au bouclage de TRIADE).

**Les règles.** (1) **L'application est codée ENTIÈREMENT par la méthode** : couche I écrite-avant-code (R2), notations à la main (keystone, l'outil du labo — jamais un compilateur), plan d'adressage arrêté avant la notation (D161), carte scellée, oracle à scénarios + harnais différentiel, kit terrain, recoup sur pièces — AUCUN octet d'application ne naît hors contrat. (2) **Le choix de l'application (délégué par le message qui ne la nommait pas) est ARBITRÉ** : « Loupe », l'éditeur hexadécimal au panneau d'empreintes — l'outil du quotidien du projet (toutes ses pièces vivent par leurs md5/sha-256), l'épreuve complète (GUI + fichiers + hachage + libc + recherche + édition : cinq familles en un artefact utile dès le premier run), le périmètre tenable (18 blocs, un jalon, un kit). Le choix est CONTREDISIBLE au message suivant : la couche I seule vit, rien n'est scellé. (3) **Le TGN vit dans SON domaine** (loupe/) avec SA lignée de balises (`loupe 0.1.0-dev.1` au premier build) : le proxy 1.0.0, la carte tls13 et les arbres scellés DEMEURENT INTACTS (l'anti-rollback armé). (4) **La dette de cérémonie est NOMMÉE À LA NAISSANCE** (le modèle D166) : le 14e arbre (loupe) et l'extension du registre figé (m0/I/README.md § 2.1) attendent la cérémonie d'ère du TGN — le geste hors-ligne du développeur, la re-signature de m0 au registre étendu (le modèle de l'ère M8) ; le garde demeure à 13 arbres VERTS jusqu'alors. (5) **COFFRE-FORT DÉGELÉ** : le message amende D135 — le fils vit EN PARALLÈLE, chacun son rythme, aucun ne bloque l'autre ; la frontière fondatrice demeure (aucun code forké, aucune dépendance vivante — toute dépendance serait un défaut à consigner). (6) **Les frontières du geste** : AUCUNE clé, AUCUN coffre réel, AUCUN fragment, AUCUN arbre signé touchés ; le sceau I vérifié AVANT consignation (13 arbres VERTS, cle deposee reelle).

**Alternatives rejetées.** Un navigateur web (rejeté : périmètre déraisonnable pour un premier TGN — un moteur de rendu est un projet par lui-même) ; un client Drive (rejeté : utile mais protocolairement lourd — OAuth 2.0 et JSON résolus à la main, différé à un TGN ultérieur) ; recoder une application existante (rejeté : c'est le modèle RoomEq DÉJÀ démontré — le TGN exige la création, la méthode doit prouver le NEUF) ; attendre le bouclage de Coffre-Fort pour ouvrir le TGN (rejeté : le message ouvre les DEUX en parallèle) ; éditer le registre figé m0/I au geste d'ouverture (rejeté : m0 est un arbre SIGNÉ — l'extension vit à la cérémonie d'ère, la dette est nommée, modèle D166/D168) ; demander à la machine de choisir l'application sans consigner l'arbitrage (rejeté : un arbitrage muet serait un contrat non écrit — D137 le tient pour les niveaux du coffre, le TGN le tient pour ses choix).
## D172 — LE CHANTIER M10-(a) RÉALISÉ : LES DIX-HUIT SPÉCIFICATIONS POSÉES (la couche I complète du TGN « Loupe » — R2 tenue : chaque bloc porté par sa spécification AVANT tout octet de notation, le gabarit § 2.2 aux SEPT blocs, chaque exigence reliée à son vecteur) ; LE PLAN D'ADRESSAGE loupe/layout.py ARRÊTÉ AVANT LA NOTATION (D161 rejoué : la table des SEPT verdicts, le cadre de session, le format de ligne, les tables MD5, les bornes, les zones, l'IAT — la préfiguration n'est pas un droit) ; L'HÉRITAGE DÉCLARÉ PAR LA CARTE EST L'HÉRITAGE UTILISÉ (tls13-01..04 + libc-01/02/07 + win-03 — libc-03 RETIRÉ) ; LA TABLE DES IDENTIFIANTS i11xxxx (la lignée g9 → h10 → i11)

**Le contexte qui fonde la décision (07/11).** La suite annoncée à l'Entrée 194 était M10-(a) ; le message du développeur la commande (« continue sur M10-(a) »). Le TGN exige la CRÉATION (D171) : la couche I complète est la première épreuve — 18 spécifications au gabarit intégral, AUCUN octet de notation, la cérémonie d'ère précède tout build. Le modèle M9-(a) (les 28 posées, les constantes re-dérivées, l'instrument 117 VERTS) est rejoué au domaine neuf.

**Les règles.** (1) **LE GABARIT INTÉGRAL, pas la forme compacte** : les SEPT blocs du § 2.2 (Intention, Contrat pre/post/inv, Échecs, Vecteurs, Fixtures, Provenance, Décisions) — les Échecs et Vecteurs EXPLICITES rendent la couverture CONTRÔLABLE MÉCANIQUEMENT : l'instrument vérifie que CHAQUE exigence Qn et CHAQUE échec En relie au moins un vecteur (une exigence invérifiable est une exigence mal formulée — la règle du protocole, tenue par le code). (2) **LE PLAN D'ADRESSAGE ARRÊTÉ AVANT LA NOTATION** (D161, la leçon de M8-(b)) : les constantes immuables seules — la table des SEPT verdicts (0 et −1..−7, dont **−1 LA FIN NOMMÉE** de la recherche : l'échec qui n'en est pas un, la fin d'une question) ; le CADRE de session (960 o, la disposition source unique que les dix-sept autres blocs citent) ; la LIGNE (77 o exacts, le format recomposé par le vérificateur) ; les 64 constantes MD5_T DÉRIVÉES PAR ARITHMÉTIQUE au geste même (floor(2^32·|sin(i+1)|), T[0] et T[63] recoupés à RFC 1321 — le juge est le code) ; les bornes du périmètre 0.1.0 (2 Gio, 24 lignes, 64 Kio, 32 o de motif, 256 écritures) ; les zones .data (cadre, écran, saisie, motif, journal, empreintes, métriques, la fenêtre de lecture partagée) ; l'IAT (34 feuilles NOMMÉES). (3) **LES RÈGLES EXÉCUTABLES** : vue_max (la dernière fenêtre VOIT le dernier octet) et recadre (la ligne active à la 12e) vivent en FONCTIONS au plan — le vérificateur les re-joue contre la référence : la règle de spécification n'est plus une phrase, c'est un code. (4) **L'HÉRITAGE DÉCLARÉ EST L'HÉRITAGE UTILISÉ** : tls13-01..04 (la famille sha scellée 1.0.0 — R7, embarqués byte-identiques au build), libc-01/02/07 (la minilibc) et win-03 (la boucle de la démo) — CHAQUE entrée est citée par ses specs ; **libc-03 RETIRÉ au geste** : aucune spécification ne le cite, le déclarer serait une contrebande de périmètre (un défaut nommé, pas une ombrageuse richesse). (5) **LES ARBITRAGES ARCHITECTURAUX nommés à leur spec** : la table unifiée des verdicts (tout refus monte à la barre — l'écran NOMME) ; LA BARRE-SAISIE (aucun contrôle enfant : l'écran appartient à Loupe) ; LE JOURNAL DES ÉCRITURES par décalage (le disque intact jusqu'à la sauvegarde, la réversibilité d'avant) ; LE DOUBLE-GESTE de sortie (la garde refus_quitter tenue par le RÉSEAU loupe-16/17/18 — ré-armée à chaque écriture, levée à chaque sauvegarde : la perte d'octets est une VOLONTÉ deux fois nommée) ; loupe-09 LA VITRINE ENTIÈRE (WinMain + la fenêtre + LA PROCÉDURE + les trois zones déclarées — la disposition tenue deux fois : des zones et des messages) ; le PANNEAU D'EMPREINTES TOUJOURS celui du DISQUE (l'astérisque nomme la divergence, jamais un condensé d'avant). (6) **LES FRONTIÈRES DU GESTE** : AUCUN octet de notation, AUCUN arbre signé touché (le garde 13 arbres VERTS vérifié AVANT consignation), le proxy 1.0.0 et la carte tls13 INTACTS.

**Alternatives rejetées.** La forme compacte tls13 pour les specs (rejetée : le TGN est l'épreuve de la MÉTHODE ENTIÈRE — le gabarit intégral rend la couverture contrôlable par le code, la forme compacte serait un repli de rigueur au moment précis où la méthode se prouve) ; déclarer libc-03 strlen dans l'héritage (rejeté : l'héritage déclaré serait un mensonge de périmètre — chaque entrée déclarée doit être citée) ; un contrôle enfant EDIT pour la saisie d'aller et de recherche (rejeté : l'écran appartient à Loupe — la barre devient le champ, aucune dépendance au contrôle système, le modèle démo reste un MODÈLE pas un héritage) ; la sauvegarde automatique à la fermeture (rejeté : la sauvegarde comme la perte sont des volontés — le double-geste les nomme, jamais une décision prise à la place de l'utilisateur) ; le panneau calculé sur la session (le journal appliqué) plutôt que le disque (rejeté : le panneau doit être RECOUPABLE — par l'outil du labo, par Get-FileHash chez le développeur — la vérité du disque, la divergence nommée par l'astérisque) ; le recalage silencieux de l'aller-à hors bornes (rejeté : LE REFUS NOMMÉ du README fondateur — jamais un saut deviné) ; la recherche par tables (Boyer-Moore) (rejeté : l'algorithme pur à la borne du quotidien — memcmp hérité, la complexité honnête tenue dans la tête, l'optimisation prématurée interdite par R11).
## D173 — LE CHANTIER M10-(b) RÉALISÉ : LE NOYAU LOUPE-01..07 NOTÉ-MESURÉ-PROUVÉ (fichier + empreintes, la notation aux slots ARRÊTÉS sur les longueurs réelles — D161 rejoué) ; LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES (la découverte du geste : le déplacement RIP de tls13-02 est codé pour 0xC080 — une relocalisation ré-écrite serait une contrebande de R7 ET un déplacement faux) ; LE MINI-OS VIRTUEL DU HARNAIS (les six shims kernel32 aux ABI msx64, le système de fichiers virtuel aux témoins réels, les échecs paramétrables, le journal des gle)

**Le contexte qui fonde la décision (08/11).** La suite annoncée à l'Entrée 195 était M10-(b) : le noyau (ouvrir/lire/fermer + les empreintes, le harnais différentiel sur vecteurs officiels + fichiers réels, l'héritage sha constaté byte-identique — R7). Le développeur commande la suite (« ok pour la suite », puis « continue »). Le modèle M9-(b) est rejoué au domaine neuf — AUCUN build : la cérémonie d'ère précède (D168 : la remise est exigée pour le chantier construire(), jamais pour la notation), la dette D166/D171 demeure, le garde reste à 13 arbres VERTS.

**Les règles.** (1) **LA MESURE AVANT L'ARRÊT** (D161, rejoué avec un outil NEUF : le mode --mesurer de loupe/outils/auteur.py — la première passe du chantier rend les longueurs SANS écrire, le plan s'arrête aux minimums, la préfiguration s'incline) : 47/388/296/122/312/879/102 o -> slots 0x40/0x1C0/0x140/0xC0/0x180/0x380/0x80, tassés @0x4040-0x49C0, multiples de 64, padding >= 16. (2) **LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES** — LA DÉCOUVERTE DU GESTE : le premier jet posait les octets hérités à des slots neufs (0x1140…) ; l'émulation a CRASHÉ dans tls13-02 sur « lea rbp, [rip - 0x91a4] » : le déplacement est CODÉ POUR L'ADRESSE SCELLÉE (0xC080, visant K[64] @0x2F00) — déplacer les octets casserait le déplacement, les re-réécrire serait une contrebande de R7. L'image neuve RÉSERVE donc les plages : .text 0x1000-0x1FFF la minilibc aux adresses M1 (libc-01 @0x1100, libc-02 @0x1180 RÉSERVÉE pour le chantier navigation, libc-07 @0x13C0), .rdata 0x2000-0x2FFF (les tables MD5 @0x2100/0x2200, l'IAT @0x2400-0x2510, K[64] @0x2F00 LA TABLE DU SCELLÉ — le plan loupe RENVOIE à tls13/layout.py, jamais re-déclarée), .text2 0x4000-0xBFFF les blocs du domaine (0x4000 la réserve d'entrée pour WinMain/loupe-09), 0xC000-0xC3C0 la famille sha aux adresses M9, .data @0xE000 les zones (CUMUL @0x10000, fin 0x20000). La règle pour les chantiers suivants : tout héritage se pose à SON adresse scellée d'origine (win-03 et son IAT démo @0x2810+ au chantier rendu). (3) **LE MINI-OS VIRTUEL** — LA PIÈCE NEUVE DU GESTE : le noyau touche le monde par SIX feuilles kernel32 (CreateFileW, GetFileSizeEx, SetFilePointerEx, ReadFile, CloseHandle, GetLastError — la liste fermée des specs) ; le harnais dote l'émulation de shims à l'ABI msx64 : le système de fichiers virtuel aux témoins réels (proxy.exe scellé INCLUS — la pièce de l'ère jugée par sa propre application), les échecs PARAMÉTRABLES (le Nième ReadFile en échec : E4 de loupe-02/05/06), le journal des gle (I4 : le code consigné, jamais un code brut à la barre), le COMPTEUR DU MORT (les 28 feuilles IAT hors noyau pointent vers une adresse dont l'appel est DÉNONCÉ — la liste fermée tenue sur pièces). (4) **LE VERDICT VIT DANS EAX** (la leçon du premier passage : « mov eax, -N » zéro-étend rax — le harnais lit le verdict 32 bits SIGNÉ, la table des SEPT verdicts vit en eax, charte § 9 ; les poignées 64 bits ne transitent jamais par rax, le cadre les porte). (5) **L'ORDRE DES REGISTRES AU RÉSEAU DES APPELS** (la leçon du premier crash de loupe-01 : loupe-04 détruit rcx pour son memset — le chemin est sauvé AVANT l'appel et RECHARGÉ avant CreateFileW ; l'ABI se rejoue à CHAQUE frontière, jamais une confiance héritée). (6) **LA BORNE 2 Gio DANS LES OCTETS** : « mov eax, 0x80000000 » (le zéro-étendu : le bord exact 0x80000000 est ACCEPTÉ, le refus est strictement au-delà) + cmp/jbe — le refus de 2 Gio + 1 est PROUVÉ AU COMPORTEMENT avec la poignée REFERMÉE comptée ; l'intégrale 2 Gio vivra au terrain (le kit M10-(d) : le natif la calcule en secondes, l'émulation en heures — la découpe honnête nommée). (7) **LES RÉVISIONS NOMMÉES DE LA COUCHE I** : loupe-01 r2 (l'erratum fixtures : la taille 44 544 était celle du scellé 0.9.0 de l'ère close, la pièce 1.0.0 mesure 65 024 o — l'empreinte 446279f3… était la bonne) ; loupe-01 r3 (LE VIDE : le fichier de taille zéro est un fichier réel du quotidien que l'éditeur DOIT ouvrir — la fenêtre n'existe pas pour lui [loupe-02 P3 : tout décalage >= taille 0], le remplissage 0, LE PANNEAU DU VIDE EXISTE : d41d8cd9… + e3b0c442…) ; loupe-06 porte libc-07 en dépendance (les zéros du bourre PAR LA CARTE — l'héritage déclaré est l'héritage utilisé).

**Le harnais (loupe/harnais_noyau.py — 59 contrôles · 59 VERTS × 3 graines [20261108, 424242, 777777]).** V0 les pièces (les scellés relus, l'erratum r2 CONSTATÉ sur pièces, les slots/les zones/l'IAT recomptés) ; V1 le round-trip R5 (keystone == capstone sur les SEPT notations, les longueurs == les mesures de l'arrêt), les déplacements RIP aux symboles du plan, les appels directs à la liste fermée (le réseau des specs), les feuilles IAT par bloc, LES CONSTANTES MD5 RE-DÉRIVÉES PAR ARITHMÉTIQUE (les 64 T par sinus, les S, les abscisses), **L'HÉRITAGE R7 CONSTATÉ BYTE-IDENTIQUE — LA DOUBLE PREUVE** (les octets émulés == les EXTRAITS DES SCELLÉS [selftest.exe pour la minilibc, proxy.exe 1.0.0 pour la famille sha] ET les notations d'origine ré-assemblées == les extraits), aucun syscall ; V2 LES SEPT VECTEURS OFFICIELS RFC 1321 AU FICHIER (chaque attendu RECROISÉ à hashlib — l'instrument se contrôle avant de juger), la gamme vide, 1 000 gammes aléatoires, le témoin 3×64 Kio + 1 ENTIER par fenêtres glissantes ; V3 LE DIFFÉRENTIEL SHA : **LA PIÈCE DE L'ÈRE JUGÉE PAR SA PROPRE APPLICATION** (loupe-05(0, 65024) sur le fichier virtuel alimenté par les octets RÉELS du proxy scellé == hashlib == 446279f3…00d93d), les vecteurs FIPS au fichier, 200 gammes sha ; V4 le noyau fichier (le cadre vierge 960 o recomposé octet par octet depuis un état sale, la session née entière CHAMP À CHAMP, le panneau né, LE FICHIER VIDE [révision 3 en preuve], 1 060 fenêtres bornées, LE RECOUVREMENT du journal [l'édition survit au défilement], la fermeture idempotence-comptée, l'hygiène des zones, les zones des chantiers suivants INTACTES) ; V5 LES ONZE REJETS NOMMÉS (absent -2/verrouillé -7/accès -6 au journal des gle, la borne 2 Gio + 1 -3 LA POIGNÉE REFERMÉE COMPTÉE, la session double -5 L'ANCIEN INTACT, le chemin 260 -5, les quatre de loupe-02, les trois × deux de gammes, le -6 du shim partout avec la sortie INTACTE et le remplissage 0, le refus PROPAGÉ par loupe-01 LA SESSION CLOSE) ; V6 LA FALSIFICATION (T[1] muté d'un ulp : 7/7 vecteurs dorés échouent — ATTRAPÉS PAR LES VECTEURS OFFICIELS avec rax = 0 exigé [jamais un vert par accident de refus], la table restaurée re-passe, l'anti-muet 16 octets, le tampon de vue INTACT pendant le calcul [l'exclusion de famille], le journal INTACT, le panneau TOUJOURS celui du disque).

**Alternatives rejetées.** Relocaliser les octets hérités aux slots neufs avec re-calcul des déplacements RIP (rejetée : R7 exige le byte-identique, un octet ré-écrit — même « équivalent » — est une contrebande ; et la preuve d'équivalence serait un second harnais) ; copier les tables K/H0 au domaine loupe (rejetée : la source unique vit à tls13/layout.py, le plan loupe RENVOIE — jamais une seconde déclaration) ; refuser le fichier vide à l'ouverture (rejetée : le vide est un fichier réel du quotidien — l'éditeur du projet ouvre des fichiers vides, le panneau du vide est défini par RFC 1321 et FIPS 180-4, la session née entière SANS la fenêtre est l'arbitrage honnête, consigné en révision 3 nommée) ; l'intégrale 2 Gio au harnais (rejetée : ~33 M blocs émulés, des heures de labo pour un cas que le terrain rendra en secondes — le refus au comportement + la borne dans les octets + le cas nommé pour le kit M10-(d), la découpe honnête) ; lire le verdict en rax 64 bits (rejetée : le verdict VIT dans eax, la table des SEPT verdicts est 32 bits — le harnais lit ce que le bloc rend, la convention de la charte § 9).

**Les frontières du geste.** AUCUN arbre signé touché (le garde sceau I vérifié AVANT consignation : 13 arbres VERTS) ; le proxy 1.0.0 et la carte tls13 1.0.0 INTACTS (l'anti-rollback armé — les scellés sont LUS, jamais écrits) ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment touchés ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre et l'extension du registre figé attendent la cérémonie d'ère — AVANT tout build, M10-(d)). Livrables : loupe/notation/brouillons/loupe-01..07.asm (les sept brouillons), loupe/notation/loupe-01..07.asm (les notations explicites), loupe/outils/auteur.py (l'outil d'auteur au mode --mesurer), loupe/layout.py (l'adressage ARRÊTÉ : les slots, les zones, l'IAT, les adresses scellées), loupe/harnais_noyau.py (l'instrument au mini-OS virtuel), loupe/I/loupe-01-ouvrir.md (révisions 2 et 3 nommées), loupe/I/README.md (le chantier (b) COMPLET + la règle des adresses scellées), le présent script.
## D174 — LE CHANTIER M10-(c) RÉALISÉ : LES FAMILLES RENDU + NAVIGATION LOUPE-08..14 NOTÉ-MESURÉ-PROUVÉES (le critère du plan TENU : l'oracle à scénarios VERT — l'écran attendu octet par octet pour des états donnés — et la falsification attrapée) ; LE MINI-GUI VIRTUEL DU HARNAIS (la file de messages scriptée, le Dispatch qui appelle LA PROCÉDURE au pointeur enregistré, le DC qui enregistre chaque goutte, les échecs paramétrables, ExitProcess qui termine) ; LES HÉRITAGES libc-02 ET win-03 AUX ADRESSES SCELLÉES (la règle du geste (b) exécutée : l'IAT démo @0x2818+ réservée aux déplacements scellés de la boucle)

**Le contexte qui fonde la décision (08/11, au soir).** La suite annoncée à l'Entrée 196 était M10-(c) : le rendu + la navigation (l'oracle à scénarios). Le développeur commande la suite (« ok continue »). Le modèle M10-(b) est rejoué au domaine neuf — AUCUN build : la cérémonie d'ère précède (D168 : la remise est exigée pour construire(), jamais pour la notation), la dette D166/D171 demeure, le garde reste à 13 arbres VERTS.

**Les règles.** (1) **L'ORDRE DU TASSEMENT, UNE RAISON D'ARCHITECTURE** : 08 (la feuille pure) · 10 (le peintre) · 11 · 12 · 13 (la feuille pure) · 14 (qui compose 12 et 13) · **LOUPE-09 DERNIER** — le bloc d'entrée (WinMain + LA PROCÉDURE) : sa table de routage S'ÉTENDRA au chantier (d) (les blocs 15-18 n'existent pas : leurs messages demeurent chez DefWindowProcW à (c), révision nommée à venir) ; placé DERNIER, l'extension ne bougera QUE son propre slot — les notations (c) de 08/10/11/12/13/14 demeurent INTACTES, la famille édition suivra à sa suite. Les appelés précèdent l'appelant. (2) **LA RÉSERVE D'ENTRÉE S'INCLINE (D161)** : la préfiguration 64 o @0x4000 ne tient pas l'écran mesuré (874 o) — WinMain vivra à SON slot (loupe-09, le dernier) et l'AddressOfEntryPoint du futur build visera LOUPE09_VA TEL QUEL (aucune fiction de trampoline : l'entrée est UNE adresse, celle du bloc). (3) **LES HÉRITAGES AUX ADRESSES SCELLÉES — LA RÈGLE DU GESTE (b) EXÉCUTÉE** : libc-02 memcmp POSE @0x1180 (loupe-13 teste chaque candidat par le scellé M1 — JAMAIS une boucle réécrite) et win-03 LA BOUCLE POSE @0x15C0 (loupe-09 l'appelle PAR LA CARTE : les octets de demo.exe 0.3.0, dont les TROIS déplacements RIP codés visent les slots IAT user32 DE L'IMAGE DÉMO — l'image loupe RÉSERVE les TROIS qwords @0x2818/0x2820/0x2828 : la double entrée n'est pas une redondance, c'est le PRIX du déplacement scellé ; la DOUBLE PREUVE : les extraits des scellés == les octets émulés ET les notations d'origine [m1/libc-02-memcmp, demo/win-03-boucle] ré-assemblées == les extraits). (4) **LE MINI-GUI VIRTUEL — LA PIÈCE NEUVE DU GESTE** : les 15 feuilles user32 + 6 gdi32 de l'IAT du geste servies par des shims à l'ABI msx64 — la file de messages SCRIPTÉE (GetMessageW dépile, la file vide rend WM_QUIT), **le Dispatch qui APPELLE LA PROCÉDURE au pointeur enregistré par RegisterClassExW** (la pile reçoit une adresse magique, rip vise la procédure, la réponse y revient — la mécanique EXACTE d'USER32 réduite au laboratoire, une seule emu_start plate), le DC qui ENREGISTRE chaque TextOutW avec ses coordonnées et ses couleurs (l'expansion latin-1 lue MOT À MOT), la police mesurée une fois (16/8), le client rect, l'ascenseur (GetScrollInfo nTrackPos / SetScrollInfo), les échecs paramétrables (BeginPaint nul, RegisterClassExW nul, la police muette), ExitProcess qui TERMINE l'émulation (le code consigné) ; les 5 feuilles du chantier (d) + GetModuleHandleW demeurent AU MORT (le compteur dénonce). (5) **L'ORACLE À SCÉNARIOS — LE CRITÈRE DU PLAN** : le modèle PYTHON INDÉPENDANT recompose l'écran attendu (la ligne 77 o du format du plan, l'entête, la grille bornée G = min(24, ceil(remplissage/16), lignes_affichables − 3), la barre-état, le panneau) depuis les TÉMOINS et l'état — JAMAIS depuis les octets du bloc — et la comparaison est OCTET PAR OCTET sur les 2320 o de la zone ECRAN ; les scénarios : la vitrine SANS session (l'usage, « - », l'ascenseur INTACT — le repli de loupe-11), le témoin ouvert PAR LA LIGNE DE COMMANDE (la session née AVANT la vitrine, le panneau == hashlib), la cellule active INVERSÉE à l'abscisse exacte (x = MARGE_X + (10 + 3·col + médian)·char_w), la marque sale (MODIFIÉ + l'astérisque), LE ROUTAGE CONSTATÉ (chaque message chez son bloc, les appels comptés un à un, DefWindowProcW pour le reste), le refus à l'ouverture (« fichier introuvable » à la barre, la vitrine VIDE VRAIE), E1/E2 (MessageBoxW PUIS ExitProcess(1), la boucle JAMAIS lancée). (6) **LE PLANCHER QUI NE RECULE JAMAIS — LA CORRECTION DU PREMIER JET** : le premier jet de loupe-14 repartait à départ zéro à chaque fenêtre — le recouvrement RE-TROUVAIT l'occurrence courante à l'infini (F3 immobile) ; le témoin à frontières (les occurrences n'existent QU'à cheval sur chaque frontière de 64 Kio) l'a attrapé AU PREMIER PASSAGE : le plancher de recherche ne recule jamais (une fenêtre manquée y avance le premier départ non examiné ; départ_rel = plancher − bord, borné à 0 — la règle de la spec lue dans toute sa portée). (7) **LES LECTURES DU GESTE (la notation confronte la spec, chaque lecture consignée)** : LA BARRE-ÉTAT AUX QUATRE MODES (0 RIEN · 1 ALLER · 2 CHERCHER · 3 MESSAGE = aucune saisie + le refus nommé au tampon — le « mode = 0 » des E1/E2/E3 de loupe-12/14 se lit LA SAISIE FERMÉE : la barre nomme, la saisie n'écoute plus ; l'acquittement par toute frappe ramène 0) ; LA BARRE ANCRÉE AU BAS (le panneau d'empreintes TOUJOURS visible — la grille cède la place : lignes_affichables − 3, l'entête + les deux lignes du panneau réservées ; la spec nommait la formule MARGE_Y + ligne·ligne_h pour chaque ligne de l'ECRAN : la grille la tient, la barre s'ancre au bas — l'oracle la juge) ; LE TIRET ASCII ET LE POINT MÉDIAN 0xB7 (l'expansion latin-1 EXACTE de loupe-10 I4 n'élève que 0x00-0xFF : l'ém-dash U+2014 de la spec ne vit qu'aux chaînes UTF-16 pilotées AUX API — le titre — jamais à la barre) ; LES CODES DE CONTRÔLE 0x06/0x07 PAR WM_CHAR (Ctrl+F ouvre CHERCHER, Ctrl+G ouvre ALLER : aucune feuille GetKeyState au plan, l'état du clavier ne se sonde pas, le caractère ctrl EST le message) ; LE CADRE RBP DE LOUPE-10 (les six sous-routines locales partagent le cadre du bloc — chaque local à son déplacement RBP STABLE à travers les appels internes, le 5e argument des TextOutW vivant à [rsp+0x20] dans la zone LIBRE du bas : aucun local n'y vit, jamais un clobber) ; LE hInstance DE L'ABI DE WINMAIN (rcx de l'entrée — D33 tenu par l'ABI ; GetModuleHandleW attend son geste, le mort le garde) ; loupe-10 porte GetLastError (E1/E2 : le code consigné — la spec l'exige, l'IAT du plan l'accepte, retiré de l'attribution InvalidateRect : le peintre ne s'invalide pas lui-même, I3 de loupe-09). (8) **LA FALSIFICATION — ctl_flush_tb** : le cache de traduction d'unicorn ne révoque pas toujours un bloc déjà traduit après une écriture mémoire (la mutation du geste fut d'abord muette PAR LE CACHE après 1 500 exécutions) : chaque mutation et restauration VIDE LE CACHE (uc.ctl_flush_tb, la voie officielle) — jamais une falsification muette par l'outil ; la falsification exigée DANS LES DEUX SENS (le muté diverge, le restauré re-passe).

**Le harnais (loupe/harnais_rendu.py — 53 contrôles · 53 VERTS × 3 graines [20261108, 424242, 777777]).** V0 les pièces (demo.exe relu md5+sha256 — l'ancre R7 de win-03 ; les SEPT specs relues ; les slots (c) recomptés : 08@0x49C0 → 10@0x4B00 → 11@0x5180 → 12@0x5400 → 13@0x5740 → 14@0x5800 → 09@0x5C00, fin 0x5F80 ; les adresses .rdata du rendu [l'entête, les tables HEX/HEXL, les 19 libellés, l'UTF-16], l'IAT démo) ; V1 le round-trip R5 × 7 + les déplacements RIP aux symboles du plan (121 déplacements) + les appels directs à la liste fermée (le réseau des specs) + les feuilles IAT par bloc + L'HÉRITAGE R7 CONSTATÉ (la double preuve) + LA PROCÉDURE relue depuis l'étiquette de sa notation + aucun syscall ; V2 loupe-08 (le doré proxy + la ligne finale incomplète + les 16 longueurs + 1 500 lignes différentielles == le modèle + les TROIS rejets la sortie INTACTE) ; V3 loupe-13 (le corpus de l'école + 1 500 cas == bytes.find, alphabets plein et pauvre + les marques de proxy + les TROIS rejets) ; V4 loupe-14 (LA CHAÎNE au fichier entier == bytes.find + LE RECOUVREMENT PAR CONSTRUCTION [le témoin à frontières, TROUVÉES aux trois] + 12 motifs différentiels sur 70 000 o + les rejets nommés : impairs/ZZ/vide → -5 « paires hexa attendues », sans session → -4, le ReadFile en échec → -6 relayé la position intacte) ; V5 les bornes (vue_max/clamp rejoués sur 10 000 tailles == la règle du plan) + les scénarios (le pas de TROIS lignes vérifié, LA POIGNÉE AU BOUT : la dernière fenêtre voit le dernier octet, l'ascenseur synchrone max == vue_max/16 ; le petit fichier : RIEN relu, les compteurs ; WM_SIZE recalculé ; le saut exact : le curseur à 0x1000, la vue recalée à la 12e ligne, L'ÉCRAN ATTENDU OCTET PAR OCTET ; le 9e chiffre ignoré, VK_SUPPR retire, VK_ECHAP annule TOUT ; les refus NOMMÉS à la barre : -5 « saisie mal formée », -3 « hors bornes », -4 « aucun fichier ouvert ») ; V6 L'ORACLE À SCÉNARIOS (les scénarios de la règle 5 — chaque écran == le modèle octet par octet) ; V7 LA FALSIFICATION (les quatre mutations + l'anti-muet aux 332 positions + LE RECOUVREMENT MUTÉ : l'occurrence à cheval MANQUÉE puis TROUVÉE — la preuve du recouvrement exigée DANS LES DEUX SENS).

**Alternatives rejetées.** Réserver l'IAT démo entière @0x2800-0x2868 (rejetée : seuls les TROIS slots visés par les déplacements scellés sont requis — la réserve minimale, le reste demeure au plan) ; un trampoline d'entrée @0x4000 (rejetée : l'entrée est UNE adresse, celle du bloc — D33 l'image PI, D161 la mesure décide ; des octets hors notation seraient une contrebande) ; GetKeyState pour les combinaisons (rejetée : les codes de contrôle vivent par WM_CHAR — aucune feuille supplémentaire, l'état du clavier ne se sonde pas) ; loupe-16 noté à (c) pour la table complète (rejetée : la découpe du plan est la loi — l'édition vit à (d), la table s'y étendra, la révision est nommée) ; garder le recouvrement à départ zéro (rejetée : le témoin à frontières démontre la re-trouvaille à l'infini — le plancher qui ne recule jamais est la règle, la correction est consignée) ; l'expansion UTF-16 complète à la barre (rejetée : I4 de loupe-10 EXIGE l'expansion latin-1 exacte 0x00-0xFF — le tiret ASCII et le point médian 0xB7, jamais U+2014 à la barre).

**Les frontières du geste.** AUCUN arbre signé touché (le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle) ; le proxy 1.0.0 et la carte tls13 1.0.0 INTACTS (l'anti-rollback armé — les scellés sont LUS, jamais écrits) ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment touchés ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre et l'extension du registre figé attendent la cérémonie d'ère — AVANT tout build, M10-(e)). Livrables : loupe/notation/brouillons/loupe-08..14.asm (les sept brouillons), loupe/notation/loupe-08..14.asm (les notations explicites), loupe/layout.py (l'adressage ARRÊTÉ : les slots (c), les pièces .rdata du rendu, les libellés, l'IAT démo, les modes de la saisie), loupe/outils/auteur.py (les sept blocs + les symboles du rendu), loupe/harnais_rendu.py (l'oracle à scénarios au mini-GUI virtuel), loupe/I/README.md (le chantier (c) COMPLET + les lectures du geste), le présent script.
## D175 — LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ : LA FAMILLE ÉDITION LOUPE-15..18 + LA TABLE DE ROUTAGE DE LOUPE-09 ÉTENDUE (r2) NOTÉES-MESURÉES-PROUVÉES (le disque saisissable et la mort du harnais ; le réseau de la garde 16↔17↔18 par tous les chemins ; l'écriture à l'octet prouvée différentielle) ; LE KIT TERRAIN ATTEND LA CÉRÉMONIE D'ÈRE (la dette D166/D171 nommée : le 14e arbre avant tout build)

**Le contexte qui fonde la décision (08/11, au soir).** La suite annoncée à l'Entrée 197 était M10-(d) : l'édition + le kit terrain. Le développeur commande la suite (« continue M10… »). LA DÉCOUPE DU PLAN EST LA LOI : la notation de l'édition est un geste de LABO (la cérémonie d'ère précède le BUILD, jamais la notation — le miroir M8/M9, Entrées 157/158 : la remise est exigée pour construire()) ; le kit terrain, lui, exige le build — LA CÉRÉMONIE D'ÈRE LE PRÉCÈDE DONC : le chantier se coupe en deux moitiés, la première réalisée ici (la famille notée-mesurée-prouvée), la seconde (le build loupe.exe + le kit livré au /test, modèle m9f) attend le geste hors-ligne du développeur. AUCUN build : la dette D166/D171 demeure, le garde reste à 13 arbres VERTS.

**Les règles.** (1) **LA TABLE DE ROUTAGE ÉTENDUE — LA RÉVISION NOMMÉE TENUE** : la promesse du geste (c) (« la table de routage s'étendra au chantier (d) sans cascade sur les autres notations ») est EXÉCUTÉE — loupe-09 croît de 874 → 1135 o (slot 0x380 → 0x480) : WM_DESTROY 0x0002 et WM_CLOSE 0x0010 → loupe-18, les HUIT flèches (VK_PRIOR/NEXT/END/HOME/LEFT/UP/RIGHT/DOWN, 0x21..0x28 d'un seul encadrement) HORS SAISIE (mode = 0) → loupe-15, Ctrl+S 0x13 PAR WM_CHAR (LE CODE DE CONTRÔLE — la voie du geste (c) pour 0x06/0x07 : aucune feuille GetKeyState au plan, l'état du clavier ne se sonde pas) → loupe-17, VK_SUPPR et les SEIZE chiffres hexa (les minuscules portées aux majuscules) → loupe-16 ; les notations (c) de 08/10/11/12/13/14 demeurent INTACTES (aucun octet bougé — la promesse tenue sur pièces), la famille édition suit À LA SUITE du slot croissant. (2) **L'ATTENTE CONSOMMÉE PAR L'ENGAGEMENT** : « le premier chiffre attend, le second ENGAGE » (la spec de loupe-16) se lit dans toute sa portée : l'engagement CONSOMME l'attente (succès OU refus — jamais un nibble zombie en attente), le premier chiffre SAUVÉ À r10d AVANT la consommation (la leçon du premier jet : la zone effacée avant la lecture, l'octet se serait composé du second chiffre seul — le journal portait 0x0D pour « 4d », l'écran attendu l'a attrapé AU PREMIER PASSAGE) ; VK_SUPPR à l'attente efface actif ET valeur (l'état NET). (3) **LA VUE SUIT L'AVANCE — L'INVARIANT DU DOMAINE** : « le curseur ne sort JAMAIS de l'écran » (le README du domaine) tient AUSSI à la saisie : le pas de loupe-16 (Q4 : le curseur AVANCE) porte LE RENVOI de loupe-15 Q3 (la même règle : les lignes visibles de la vitrine — METRIQUES.lignes − 3, capées 24, LA LECTURE STRICTE de la spec [jamais perdu hors écran, y compris la vitrine rétrécie ; à la vitrine 0.1.0 la fenêtre == le remplissage 384 : le miroir exact du commit de loupe-12] — le recadrage du plan, loupe-02 LA PREMIÈRE le refus relayé la vue inchangée) ; la relecture SEULEMENT au recadrage (le harnais compte les lectures : la vue ne bouge QUE POUR SUIVRE). (4) **L'ÉCRITURE À L'OCTET — L'UNITÉ EST L'OCTET** : loupe-17 écrit CHAQUE entrée du journal DANS SON ORDRE DE SAISIE par SetFilePointerEx + WriteFile d'UN SEUL octet (jamais une plage ; le pointeur d'écrits NUL : la poignée est synchrone) ; l'échec est FAIL-CLOSED (le journal DEMEURE, la marque demeure, les octets déjà écrits le restent — l'échec ne perd RIEN, le geste se reprend : le second Ctrl+S REPREND ET FINIT, prouvé) ; LE TÉMOIN « N o écrits · 0xAABBCCDD..0xEEFFGGHH » composé AVANT LA VIDANGE (le journal est la source du témoin : dec + chaine + hex8, LES SOUS-ROUTINES LOCALES AU CADRE RBP — le modèle loupe-10). (5) **LE RÉSEAU DE LA GARDE 16↔17↔18** : la perte d'octets non sauvés exige DEUX gestes — loupe-16 RÉ-ARME la garde à CHAQUE écriture (refus_quitter = 0 : après une nouvelle écriture, le premier Alt+F4 re-vient avertir), loupe-17 la LÈVE à chaque sauvegarde réussie, loupe-18 la POSE au premier refus (la phrase à la barre « MODIFIÉ - Alt+F4 encore pour quitter sans sauver, Ctrl+S pour sauver », MessageBeep : le refus s'entend, verdict -5) et ne tranche qu'au second (DestroyWindow) ; WM_DESTROY (envoyé par DestroyWindow) ferme la session par loupe-03 (le journal ABANDONNÉ DÉLIBÉRÉMENT — les octets non sauvés sont une VOLONTÉ), PostQuitMessage(0) rend la boucle héritée win-03, WinMain retourne, ExitProcess(0) — la sortie ne sauvegarde JAMAIS elle-même. (6) **LE DISQUE SAISISSABLE ET LA MORT — LES PIÈCES NEUVVES DU HARNAIS** : l'OS virtuel gagne un WriteFile à l'ABI msx64 (l'écriture à la position de la poignée dans le fichier virtuel SAISISSABLE — FichierEditable : le contenu matérialisé à la première écriture, TOUJOURS des bytes au lecteur [unicorn refuse les bytearray — la leçon du premier passage], l'échec armé au Nième appel, le journal des écritures) ; le GUI virtuel gagne ses trois feuilles de sortie : DestroyWindow (qui ENVOIE WM_DESTROY à la procédure PAR LA MÊME MÉCANIQUE que le Dispatch — la pile reçoit l'adresse magique, rip vise la procédure : la mort de la fenêtre est la mécanique EXACTE d'USER32 réduite au laboratoire), PostQuitMessage (la file quittée — GetMessageW rend 0, la boucle héritée rend), MessageBeep (le coup enregistré) ; les QUATRE feuilles du (d) VIVENT à l'IAT, GetModuleHandleW SEUL demeure au mort (le hInstance de l'ABI de WinMain, D174). (7) **LES REJETS NOMMÉS DE L'ÉDITION** : sans session -4 « aucun fichier ouvert » (16/17) ; LA CELLULE FANTÔME -3 « hors bornes » (le curseur forgé hors [vue, vue+remplissage) : un état forgé, le curseur visible étant l'invariant — RIEN au journal, le refus PRÉCÈDE ; le fichier VIDE y vit : aucune cellule n'existe) ; LE JOURNAL PLEIN -3 « journal plein - Ctrl+S » (256 DISTINCTS : RIEN perdu, l'octet refusé n'entre pas) ; le non-hexa IGNORÉ proprement (les seize chiffres seuls écoutent) ; « rien à sauver » (le journal vide : l'état nommé, PAS un échec, AUCUN WriteFile compté).

**Le harnais (loupe/harnais_edition.py — 45 contrôles · 45 VERTS × 3 graines [20261108, 424242, 777777]).** V0 les pièces (les TROIS scellés relus — proxy.exe 1.0.0, selftest.exe M1, demo.exe 0.3.0 : les ancres R7 ; les QUATRE specs du geste ; les slots (d) recomptés : 09 r2 @0x5C00 [0x480] → 15 @0x6080 [0x1C0] → 16 @0x6240 [0x2C0] → 17 @0x6500 [0x240] → 18 @0x6740 [0xC0], fin 0x6800 ; les 5 libellés du (d) @0x2520-0x259E ; LA TABLE ÉTENDUE déclarée dès la spec R1 du geste (a)) ; V1 le round-trip R5 × 5 + les appels directs à la liste fermée (les sous-routines locales exceptées) + LA ROUTE CONSTATÉE (VK_BAS → 15 le curseur bouge ; la touche hors table ET les flèches EN MODE SAISIE → DefWindowProcW comptées le curseur INTACT ; '4' → 16 le nibble en attente ; 'z' → le défaut ; Ctrl+S → 17 « rien à sauver » AUCUN WriteFile ; WM_CLOSE → 18 : DestroyWindow → WM_DESTROY ENVOYÉ → loupe-03 + PostQuitMessage — LA MORT COMPLÈTE, la poignée rendue) ; V2 loupe-15 (le différentiel 10 000 touches == le modèle à CHAQUE pas : le curseur ET la vue, la relecture EXACTEMENT quand la vue bouge ; LES BORDS des arrêts NOMMÉS rax = 0 quand même la vue INTACTE ; VK_DEBUT/VK_FIN à la ligne finale incomplète — la fin RÉELLE ; LA VUE SUIT à l'écran attendu octet par octet ; LA VITRINE RÉTRÉCIE la lecture stricte ; le repli sans session ; LE VIDE aucune cellule) ; V3 loupe-16 (le différentiel 10 000 frappes : le journal PAR DÉCALAGE, le remplacement, la borne 256 refusée NOMMÉMENT, l'attente consommée, le tampon, la marque, la garde, le pas, la vue — le modèle indépendant ; le scénario « 4d » L'ÉCRAN ATTENDU ; LES REJETS ; VK_SUPPR à l'attente ; LA GARDE RÉ-ARMÉE après la sauvegarde) ; V4 loupe-17 (le différentiel 1 000 scénarios : le disque APRÈS == le modèle SEULEMENT les N octets, la taille CONSTANTE, EXACTEMENT N WriteFile ; LE TÉMOIN à la barre + le panneau RE-NÉ == hashlib + l'astérisque parti — l'écran attendu ; « rien à sauver » AUCUN appel compté ; L'ÉCHEC FAIL-CLOSED : le 2e WriteFile refuse, le premier ACQUIS, le journal DEMEURE, le second Ctrl+S REPREND ET FINIT ; sans session -4) ; V5 loupe-18 (la sortie directe ; LE DOUBLE-GESTE : le refus -5, LA PHRASE, LE BEEP, la fenêtre DEMEURE, le second tranche ; LE RÉSEAU par tous les chemins ; WM_DESTROY le disque INTACT — l'abandon) ; V6 L'ORACLE À SCÉNARIOS (LA BOUCLE COMPLÈTE par la ligne de commande : ouvrir, éditer, sauver, peindre, Alt+F4 — LA MORT COMPLÈTE le disque SAUVÉ == le modèle, ExitProcess(0) ; LE CHEMIN DE L'ABANDON : le refus, le beep, le second geste, LE FICHIER INTACT ; LA RÉ-OUVERTURE : la persistance, les empreintes recoupées hashlib ; LE TÉMOIN peint à la barre) ; V7 LA FALSIFICATION (la vue qui suit MUTÉE : le curseur sort de l'écran — restauré la vue suit ; LA GARDE DE 16 non ré-armée : la perte d'un seul geste — restaurée le refus revient ; LA GARDE DE 17 non levée : l'avertissement pour rien — restaurée le quitte-après-sauvegarde ; L'OCTET DE TROP : l'écriture mutée à 2 o — restaurée UN octet exactement ; l'anti-muet du témoin).

**Alternatives rejetées.** Couper le (d) en deux chantiers du plan (rejetée : la rangée demeure UNE — la découpe se consigne DANS la rangée, la notation réalisée, le kit attend la cérémonie : le plan est la loi, la cérémonie est la porte de processus) ; loupe-16 appelant loupe-15 pour la vue (rejetée : la règle est RÉ-ÉCRITE locale — le domaine ne connaît pas de 19e bloc, le renvoi est nommé) ; garder le nibble après l'engagement (rejetée : « le second chiffre engage » — l'attente CONSOMMÉE, succès ou refus ; le premier jet laissait la zone vivante : la comparaison du harnais l'a attrapé) ; composer le témoin APRÈS la vidange (rejetée : le journal est la SOURCE du témoin — vidé d'abord, le témoin mentirait) ; l'écriture par plage (rejetée : l'unité est l'octet, I4 de loupe-17 — un hexadécimal éditeur ne crée pas d'octets ; le mutant à 2 o le prouve) ; GetKeyState pour Ctrl+S (rejetée : 0x13 par WM_CHAR, la voie des codes — aucune feuille de plus).

**Les frontières du geste.** AUCUN arbre signé touché (le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle) ; le proxy 1.0.0 et la carte tls13 INTACTS ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment touchés ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre et l'extension du registre figé attendent la cérémonie d'ère — AVANT tout build, la seconde moitié du (d)). Livrables : loupe/notation/brouillons/loupe-15..18.asm (les quatre brouillons) + loupe-09-ecran.asm (la table étendue), loupe/notation/loupe-15..18.asm + loupe-09-ecran.asm (les notations explicites), loupe/layout.py (l'adressage ARRÊTÉ : les slots (d), les 5 libellés @0x2520+, les constantes du journal, Ctrl_S/WM_DESTRUCTION), loupe/outils/auteur.py (les 18 blocs — la couche du domaine ENTIÈRE), loupe/harnais_edition.py (l'oracle au disque saisissable et à la mort), le présent script.
## D176 — LA SPÉCIFICATION v0.8.0 : LA CONSOLIDATION DU PROGRAMME D'APRÈS M9 (le jalon M9 — TLS 1.3 pur en blocs scellés, le domaine `tls13` — FRANCHI : les 28 blocs notés-mesurés-prouvés, le septième run terrain vert recoupé 34/34 sur pièces croisées, LA SESSION RÉELLE — la ligne applicative chiffrée ÉCHANGÉE avec un serveur réel —, la finale `1.0.0` SCELLÉE sur recoup exigé comme pièce [D170]) ; LE TEST GRANDEUR NATURE OUVERT (le jalon M10, D171 : « Loupe », l'éditeur hexadécimal au panneau d'empreintes — la couche I de 18 spécifications [D172] et les QUATRE chantiers de notation accomplis [D173/D174/D175 : les 18 blocs NOTÉS-MESURÉS-PROUVÉS]) ; LA DETTE DU QUATORZIÈME ARBRE NOMMÉE (la cérémonie d'ère du TGN précède tout build — le garde demeure à 13/13 jusque-là) ; le projet fils COFFRE-FORT dégelé en parallèle (D171, D135 amendée)

**Le contexte qui fonde la décision (08/11, la demande du développeur).** La demande du développeur porte la mise à jour du document PDF Protocole TRIADE après les gestes du TGN. Le constat du geste : la spécification vivante v0.7.0 est EN RETARD SUR LE PROGRAMME sur quatre points nommés — le § 18 titre « jalons M0 à M9 » et tient M9 « ouvert » alors que M9 est FRANCHI (finale 1.0.0 scellée le 07/11, Entrée 193/D170 : la session réelle la ligne applicative chiffrée, le témoin « HTTP/1.1 200 OK » déchiffré par la machine, l'épinglage -6 nommé, proxy.exe byte-identique 446279f3…) ; le TGN ouvert au D171 (l'application « Loupe », le domaine `loupe`) et ses QUATRE chantiers de notation accomplis (D172–D175) ne vivent nulle part au document ; le § 13.5 s'arrête aux cérémonies des ères M8/M9 alors que l'ère du TGN porte sa dette nommée (le 14e arbre, D166/D171) ; le projet fils COFFRE-FORT demeure « développement différé » alors que D171 l'a dégelé. Le versionnement suit les RÉVISIONS, jamais les franchissements (addendum Task 62) — mais un programme entré en exécution EST une révision en attente de sa passation : la v0.8.0 est la passation du programme d'après M9 dans la spécification, le miroir exact de ce que D169 fit pour le programme d'après M7.

**Les règles.** (1) **Le programme d'après M9 entre en spécification** : l'état des jalons est CONSTATÉ — M0–M9 FRANCHIS (balises 0.2.0 à 0.9.0 et 1.0.0), M10 OUVERT (le TGN, D171) : la couche I complète (18 spécifications en cinq familles, D172) et les quatre chantiers de notation accomplis (D173 le noyau fichier + empreintes, D174 le rendu + la navigation, D175 l'édition + la table de routage de loupe-09 étendue en révision nommée) — les 18 blocs NOTÉS-MESURÉS-PROUVÉS (59 + 53 + 45 contrôles verts aux trois graines sur les trois harnais). (2) **Le sceau est consigné à son état réel** : TREIZE arbres signés + LA DETTE DU QUATORZIÈME nommée — l'ère du TGN suit la discipline des ères (D166 règle 8 : la dette à la naissance ; D168 : la charge au geste ; D163 : la continuité par le déterminisme Ed25519) ; le § 13.5 étendu consigne la cérémonie À VENIR (la remise FRAÎCHE des quatorze arbres au /Cérémonie, le geste hors-ligne du développeur à la clé du 04/11, les pièces au coffre /test, le garde à QUATORZE arbres VERTS après installation — puis le build de Loupe peut naître). (3) **Le TGN entre au § 18** : la rangée M10 avec ses critères de sortie mesurables (coder une application réelle NEUVE entièrement avec TRIADE, de l'intention à l'octet livré ; l'oracle à scénarios vert ; la balise `loupe 0.1.0` scellée sur run terrain recoupé) et le paragraphe du programme (l'épreuve de la MÉTHODE ENTIÈRE — le modèle RoomEq s'arrêtait au recodage, le TGN exige la CRÉATION). (4) **Aucune règle du cœur n'est modifiée, aucune couche n'est ajoutée à l'exécution, la hiérarchie est inchangée** — la révision consolide, elle ne légifère pas.

**Alternatives rejetées.** Attendre la clôture de M10 pour réviser (rejeté : la consolidation suit le PROGRAMME, pas la finale — M9 franchi ET le TGN ouvert sont DEUX moteurs d'une même passation, le précédent D169 fut la passation d'un programme en cours) ; mettre l'application « Loupe » sous le sceau AVANT la cérémonie (rejeté : le garde suit le calendrier de la cérémonie, jamais l'inverse — le 14e arbre exige la clé hors-ligne du développeur, le laboratoire ne signe jamais à sa place) ; ajouter un profil de cible pour le TGN (rejeté : le profil primaire `x86-64-win11-pe` est l'épreuve ; l'universalité est déjà prouvée M6/M7) ; sceller la 0.1.0 de Loupe au build (rejeté : la balise de développement naît au build — geste de BUILD jamais scellage, miroir M6/M7/M8 ; la 0.1.0 se scellera sur le run terrain vert recoupé) ; signer les sources `docs/` sous le sceau courant (rejeté : le modèle par-version demeure, `v06/I/README.md` § 1).

**Frontières.** Les balises INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 — la révision documente, elle ne scelle rien) ; l'archive v0.7.0 DEMEURE (docs/Protocole_TRIADE_v0.7.0_Specification.pdf, dernier build consigné sha256 dd36eb41…, 999 631 o — rien ne se jette) ; le *Livre du Coffre* v1.1 INCHANGÉ (la révision ne touche pas le coffre) ; la chaîne spec_v070 devient spec_v080 par COPIE (l'archive spec_v070 DEMEURE au dépôt — le modèle des révisions : l'ancienne chaîne reste dans l'histoire). Les pièces : docs/PROTOCOLE_TRIADE.md (v0.8.0, révisé PAR SCRIPT revision_v080_md.py), scripts/revision_v080_tex.py (les 23 remplacements LaTeX ASSERTÉS), scripts/spec_v080/ (la chaîne), scripts/spec_v080/verify_spec.py (le cahier V1–V16), docs/Protocole_TRIADE_v0.8.0_Specification.pdf (l'artefact, 45 pages, sha256 95226c2b24dd…, empreinte consignée PAR LE BUILD n°26
## D177 — LA CÉRÉMONIE D'ÈRE DU TGN ARMÉE : le registre figé de m0 ÉTENDU au domaine `loupe` (M10) et l'arbre `loupe` ENTRÉ à la table canonique du sceau I (le quatorzième — `loupe.1`, l'arbre complet des 19 fichiers : le README + les 18 spécifications) ; la remise FRAÎCHE des QUATORZE arbres RÉGÉNÉRÉE AU GESTE (D168 rejouée : DEUX empreintes nouvelles [m0 667fb5ae… le registre étendu ; loupe 59e4871a… l'arbre neuf], les douze autres inchangées) et SERVIE au dossier /Cérémonie du Drive avec le LISEZMOI pas à pas ; la dette D166/D171 ÉCHUE AU BUILD — le geste hors-ligne du développeur (la clé du 04/11, « JAMAIS generer ») demeure LE seul chemin vers le build de Loupe

**Le contexte qui fonde la décision (08/11 au soir, la demande du développeur).** « go pour la cérémonie » : le message arme la cérémonie d'ère que le programme annonçait (la ligne SUITE de l'Entrée 199). Les quatre chantiers de notation sont accomplis (D172–D175 : les 18 blocs NOTÉS-MESURÉS-PROUVÉS), la couche I est FINALE, la spécification v0.8.0 livrée — la dette de cérémonie D166/D171 est ÉCHUE AU BUILD : aucun octet de build ne naîtra avant la remise du développeur installée (le garde suit le calendrier de la cérémonie, jamais l'inverse — § 13.5).

**Les règles.** (1) **L'extension du registre figé vit AU GESTE de la cérémonie** (D168 : la charge se prépare au geste — l'ouverture ANNONCE, la cérémonie EXIGE) : m0/I/README.md § 2.1 porte désormais `loupe` (M10), m0 est DIVERGÉ nommément (CODE 10, fichier modifié : README.md) — l'extension promise par la couche I de Loupe à sa naissance (D171, règle 8). (2) **Le quatorzième arbre entre à la table canonique** : `loupe` (loupe.exe, l'éditeur hexadécimal au panneau d'empreintes), balise `loupe.1`, à sa place d'ère après `tls13.1` — l'arbre est NEUF (CODE 12 : manifeste déposé absent), sa première signature naîtra de cette cérémonie ; la spec v06/I DEMEURE figée à l'ère 0.6.0 (la table vivante est celle de l'outil, le sceau ne se re-spécifie pas à chaque ère). (3) **La remise est COMPLÈTE et FRAÎCHE** : quatorze lignes (une rotation couvre TOUS les arbres — spec § 5), régénérée au geste (D168) ; les douze arbres inchangés seront re-signés à l'identique par le déterminisme Ed25519 (la preuve D163, rejouée à chaque cérémonie). (4) **AUCUN build ne précède la remise installée** : le garde à QUATORZE arbres VERTS est la condition du build de Loupe — le kit terrain (M10-(d) seconde moitié) suit le build, le run (M10-(e)) suit le kit, la balise `loupe 0.1.0` se scellera sur le run terrain vert recoupé.

**Alternatives rejetées.** Signer à la clé de test pour débloquer le build (rejeté : déclasserait l'état « reelle » — une régression de preuve, D87 : le labo ne signe jamais à la place du développeur) ; attendre la clôture de M10 pour tout signer d'un coup (rejeté : la dette est ÉCHUE AU BUILD — chaque étape a sa cérémonie au moment où le garde l'exige, le miroir des ères M8/M9) ; étendre le registre sans re-signer m0 (rejeté : un diff d'intention non signé — le garde le nommerait CODE 10 indéfiniment, le build naîtrait sur une dette cachée) ; poser le domaine `loupe` sous un arbre existant (rejeté : un identifiant n'est jamais réutilisé, chaque ère son arbre — § 2.1) ; mettre à jour la table normative v06/I (rejeté : la spec du sceau est figée à son ère, la table vivante vit dans l'outil — la preuve D75/D105 : ce qui est signé ne se ré-écrit pas, ce qui vit se met à jour).

**Frontières.** Les balises INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 — la cérémonie ne scelle rien) ; les 18 spécifications et les notations INTACTES (R2 — la cérémonie signe les écrits, elle ne les touche pas) ; le proxy 1.0.0 et la carte tls13 INTACTS ; l'outil hors-ligne INCHANGÉ (agnostique de la table des arbres) ; la clé privée JAMAIS au bac à sable (D87). Les pièces : m0/I/README.md (le registre étendu), v06/sceau_I.py (la table à quatorze), v06/sceau-I/a-signer.txt (la remise, 14 arbres), download/LISEZMOI-ceremonie-ere-TGN.txt (le pas à pas, déposé au /Cérémonie du Drive), scripts/maj_kit.py (RACINE_KIT + NOTE_D130 réorientées), scripts/consigner_ceremonie_tgn.py, scripts/deposer_lisezmoi_ere_tgn.py (le recoup indépendant).

## D178 — LE JALON M10 FRANCHI : LA FINALE `loupe 0.1.0` SCELLÉE SUR LE RECOUP TERRAIN EXIGÉ COMME PIÈCE (le miroir D165/D170 porté à l'ère du TGN : le scellage REFUSE en l'absence du verdict du recoup vert — la porte est de PROCESSUS, jamais de console ; LA PIÈCE VIT AU DÉPÔT — le verdict du onzième run à download/preuves-run-loupe-dev12/, recoupé par md5 : la cérémonie est re-expérimentable d'un clone frais) ; LA DETTE DE LA CARTE SOLDÉE PAR LA RÉGÉNÉRATION DES NOTATIONS (l'Entrée 218 : les retouches documentées dev.6/7/8 REVENUES à la chaîne PAR LES BROUILLONS — l'auteur rejoué, 18/18 notations == la pièce OCTET POUR OCTET [l'écart de l'audit 587 → 0], l'écart nommé de win-03 porté au build [+6 octets, la double preuve sur l'extrait brut], les DEUX ERRATA de l'auditeur dev.5 guéris [l'instruction à l'étiquette sautée ; le reset-à-8 faux au sous-programme interne — LE MODÈLE MATÉRIEL : entrée ABI ≡ 8, cadres sauvés/restaurés, appel externe net zéro], les harnais portés à l'ère dev.8 [GetModuleHandleW vivant, 61/61 · 53/53 · 45/45 rejoués à chaque passe] — R2/R5 restaurés au sens plein : les notations décrivent LA PIÈCE, les harnais gardent LES OCTETS QUI VIVENT) ; [R10-PÉRIMÉE] LA DETTE NOMMÉE DE LA PORTE (la table de la pièce porte 17 sommes de l'ère dev.5 — les retouches des Entrées 210/214 changèrent les octets des blocs SANS rafraîchir la table ; la recomposition DÉTERMINISTE la reproduit véridiquement, l'écart confiné aux 17 champs, LA PIÈCE INTACTE — réparable à 0.1.1+ à contrat stable, R4) ; LE SCELLAGE EST UN FAIT DE CARTE, L'ARTEFACT NE BOUGE JAMAIS (la balise vit dans frag-bld, l'entête la porte, loupe.exe demeure byte-identique 054de960… — LE MÊME binaire que LE ONZIÈME RUN a couru ; la cristallisation 26 × 10/10 exigée au geste ; la re-signature à la graine durable D144 : LE TÉMOIN e9cd8c5494852695… NE BOUGE PAS ; l'anti-rollback ARMÉ — la reconstruction REFUSÉE, constaté au geste même) ; DEUX SESSIONS PARALLÈLES, UNE POINTE (le message du développeur ouvrit deux sessions sur le même chantier ; la première poussa sa clôture technique, la seconde — dont l'architecture alternative [les retouches en stages documentés, les notations demeurant à l'ère de notation] fut vécue jusqu'au MÊME constat puis DISCARDÉE — s'aligna sur la pointe D164 et accomplit la suite interrompue : les pièces au dépôt, la porte réparée, les consignations, la passation ; LA RÈGLE : la pointe GitHub est la canonique, le geste parallèle se nomme et se rend, jamais ne se pousse par force)

**Le contexte qui fonde la décision (11/11, le message du développeur « continue jalon M10 »).** L'Entrée 217 avait DÉBLOQUÉ la balise (le onzième run recoupé 39/39) et nommé la suite : LE CHANTIER DU SCELLEMENT — la dette de la carte (l'Entrée 211 : la carte en génération 13/dev.5, la pièce en dev.8) puis la cérémonie (le modèle D104/M9-Entrée 193). Deux sessions l'exécutèrent en parallèle ; la clôture est le fait des deux, la pointe celui de la première, la présente décision consigne L'ÉTAT FINAL.

**Les règles.** (1) **LA DETTE SE SOLDE À LA SOURCE** : les notations RE-GÉNÉRÉES des brouillons portés aux retouches (l'outil auteur.py — le pipeline conçu D172), la pièce renée de ses notations (587 → 0), l'héritage win-03 repointé au build (+6 octets documentés), les errata de l'auditeur guéris par LE MODÈLE MATÉRIEL — la chaîne vit à l'époque dev.8, les harnais gardent la pièce. (2) **LA CRISTALLISATION EST DE PROCESSUS** : dix passes de re-vérification complète (la composition == la pièce, les TROIS harnais, le verrou croisé, la re-signature) portent les 26 compteurs à 10/10 — exigés au scellage. (3) **LE SCELLAGE TRANCHE SES PORTES AVANT L'UNIQUE ÉCRITURE** : le garde sceau I (14 arbres, clé « reelle ») ; LE VERDICT DU RECOUP SUR PIÈCES (les marqueurs tranchés — la pièce AU DÉPÔT depuis l'Entrée 219) ; la cristallisation 10/10 ; le verrou croisé + la balise encore dev.8 + l'artefact INTACT ; PUIS la bascule version=0.1.0-dev.8 → 0.1.0 dans frag-bld (occurrence unique, EN MÉMOIRE, l'ancienne absente après), les fragments re-chiffrés, l'entête portant LA BALISE, la signature Ed25519 re-signée (LE TÉMOIN NE BOUGE PAS), le tableau de bord suivant, l'anti-rollback ARMÉ. (4) **LA POINTE EST LA CANONIQUE** (D164 étendu aux sessions parallèles) : le premier push gagne, le second s'aligne, nomme son geste et COMPLÈTE — jamais de force-push, jamais de double consignation du même numéro (l'Entrée 218 est celle de la pointe ; la clôture complémentaire vit à l'Entrée 219). (5) **[R10-PÉRIMÉE] EST UNE DETTE NOMMÉE, PAS UNE RÉPARATION SILENCIEUSE** : la pièce VÉCUE (onze runs) prime ; la table se rafraîchira à 0.1.1+ le jour où le développeur commandera la version — R4 (le contrat stable), R10 (la monotonie), jamais un hot-fix d'un scellé.

**Alternatives rejetées.** Porter les retouches en STAGES du build hors notations (l'architecture de la session parallèle — vécue jusqu'au même constat puis discardée : les notations demeurant à l'ère dev.5, l'écart pièce↔notations vivait de la documentation des stages ; la régénération l'ÉLIMINE — la source unique rétablie, R2/R5 au sens plein) ; rafraîchir la table R10 au scellage (rejetée : LA PIÈCE ne bouge jamais au scellage — fait de carte ; la dette se nomme et se paie à la version suivante, R4) ; forcer le push de l'état parallèle (rejetée : D164 — la pointe est la canonique, le geste parallèle se nomme et se rend) ; sceller sans le verdict au dépôt (rejetée : la porte de processus exige la PIÈCE — un chemin de bac à sable mort ne se re-vit jamais, l'Entrée 219 l'a réparée).

**Frontières.** Les balises sœurs INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0) ; AUCUN arbre signé touché ; la clé privée jamais traversée (D87) ; loupe.exe INTACT (054de960… — LE MÊME binaire que le onzième run). Les pièces : loupe/ (les notations regénérées, les harnais portés, le build aux portes, la carte balise 0.1.0 génération 16), download/preuves-run-loupe-dev12/ (le verdict + les DEUX témoins), scripts/passe_bundle_finale_loupe_010.py, scripts/consigner_entree_219.py.


## D179 — LA VERSION 0.1.1 COMMANDÉE : LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE (la commande du développeur « b et c » — l'option (c) de l'Entrée 219 : la table des 17 sommes rafraîchie à la version 0.1.1+, à contrat stable) ; LA PIÈCE NAÎT DE LA RECOMPOSITION MÊME (le build calcule la table à la vérité des blocs DEPUIS TOUJOURS — la 0.1.1 la VIT : chaque somme == son bloc relu, PAR CONSTRUCTION ; le qword version porté 0x00010008 → 0x00010101, l'ère 0.1.1-dev.1 ; 0 OCTET AILLEURS — LE CODE BYTE-IDENTIQUE au vécu des ONZE RUNS [R4 : le contrat stable ; R7 : les adresses intactes] ; la pièce 0.1.0 [054de960…] SCELLÉE demeure au git et au coffre [loupe-kit-12]) ; LA CARTE GÉNÉRATION 17 (la 16 demeure celle de la balise 0.1.0 scellée ; LA LECTURE DE LA BALISE DEVIENT GÉNÉRATION-INDÉPENDANTE — l'en-tête signé, jamais le fragment chiffré : un passage d'ère n'aveugle JAMAIS l'anti-rollback) ; L'ANTI-ROLLBACK OUVERT À LA MONOTONIE R10 (la version STRICTEMENT SUPÉRIEURE ouvre la nouvelle ère — (0,1,1,−1,1) > (0,1,0,0,0) ; une pré-version de la balise scellée demeure REFUSÉE : (0,1,0,−1,N) < (0,1,0,0,0), jamais de retour en arrière) ; LE PORT D'ÈRE CONFINÉ AUX CHAMPS NOMMÉS (la pièce déployée ASSERTÉE == LA SCELLÉE 0.1.0 [054de960…] ; tout écart HORS des champs de sommes + le qword version = ÉCHEC NOMMÉ — R4/R7 gardés au geste même) ; LE KIT 0.1.1-dev.1 DÉPOSÉ au coffre /test (loupe-kit-13 aux QUATRE pièces, la vague versionnée vagues-m10, le réceptacle ARMÉ) — LE DOUZIÈME RUN ATTENDU : LE MÊME CRITÈRE que le onzième (le scénario ENTIER T0 → S0 → LA LIAISON ET la vitrine vivante), LA BALISE `loupe 0.1.1` SE SCELLERA sur le vert recoupé (le miroir D165/D170 : la porte est de processus) ; la cristallisation R6 poursuivie au scellage (les passes exigées à la porte — D178 règle 2, la carte à 2/10 au geste de la consignation)

**Le contexte qui fonde la décision (11/11, le message du développeur « b et c »).** L'Entrée 219 avait posé le programme d'après M10 au développeur en trois options ; la commande arrive le jour même : (b) la consolidation v0.9.0 de la spécification ET (c) le soldage de la dette [R10-PÉRIMÉE] à 0.1.1+. D178 l'avait nommé d'avance : « la table se rafraîchira à 0.1.1 le jour où le développeur commandera la version — R4, R10, jamais un hot-fix d'un scellé ».

**Les règles.** (1) **LA DETTE SE SOLDE À LA NAISSANCE** : la nouvelle pièce EST la recomposition (la table véridique par construction, le qword porté) — jamais un patch de la scellée. (2) **LE PORT D'ÈRE PORTE SES GARDES** : la déployée ASSERTÉE scellée 0.1.0, l'écart confiné aux champs nommés (17 sommes + le qword), 0 octet ailleurs — R4/R7 constatés au geste. (3) **LA MONOTONIE EST LA PORTE** : l'anti-rollback R6 s'ouvre à la version strictement supérieure (R10) et à elle seule. (4) **LA BALISE SE SCELLE SUR LE VÉCU** : le kit va au terrain, le scellage de la 0.1.1 attend le verdict du recoup vert DU DOUZIÈME RUN (D165/D170 — la pièce qui se scelle est la pièce qui a couru).

**Alternatives rejetées.** Sceller la 0.1.1 au labo sans run (rejetée : le miroir D165/D170 — le scellage REFUSE en l'absence du verdict du recoup vert ; la 0.1.0 fut scellée sur le onzième run, la 0.1.1 se scellera sur le douzième) ; patcher la table de la pièce scellée en place (rejetée : jamais un hot-fix d'un scellé — D178) ; rouvrir le jalon M10 pour la 0.1.1 (rejetée : M10 est clos sur sa balise ; la 0.1.1 est une version de maintenance à contrat stable, R4) ; hériter les compteurs de cristallisation de la carte 16 (rejetée : la carte 17 est une carte neuve d'une ère neuve — les passes re-vérifient, R6 au sens plein).

**Frontières.** La balise `loupe 0.1.0` SCELLÉE DEMEURE (l'anti-rollback vivant) ; les balises sœurs INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0) ; loupe.exe 0.1.1-dev.1 (c1115105…, 127 488 o) — le code byte-identique au vécu des onze runs ; les secrets au seul .keys/ (D12) ; la clé privée jamais traversée (D87). Les pièces : loupe/ (l'ère 0.1.1-dev.1, la carte génération 17), le kit 0.1.1-dev.1 au coffre /test (loupe-kit-13), scripts/porte_ere_011.py, scripts/genere_kit_011_dev1.py, scripts/depot_entree_221.py.

## D180 — LA CONSOLIDATION v0.9.0 : LE PROGRAMME D'APRÈS M10 ENTRE EN SPÉCIFICATION (le modèle D169/D176 — v0.7.0 après M8, v0.8.0 après M9, v0.9.0 après M10 — servie sur la commande du développeur, l'option (b) de l'Entrée 219) ; LE JALON M10 FRANCHI consigné au document (la rangée M10 du § 18 PORTÉE FRANCHIE : ONZE RUNS TERRAIN, ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — LA VITRINE VIVANTE chez son utilisateur, LE ONZIÈME RUN recoupé 39/39, LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE — LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION : de l'intention à l'octet vécu) ; LA VERSION 0.1.1-dev.1 COMMANDÉE au document (le § 1.10 réécrit, la correspondance v0.8.4 → v0.9.0 NOUVELLE, l'annexe décisionnelle étendue D177–D180, le journal des versions, la clôture) ; LA CHAÎNE spec_v090 NÉE DE spec_v084 PAR COPIE (l'archive v084 DEMEURE — dd36eb…, e92689ab… aux archives consignées) ; le md PROTOCOLE_TRIADE.md en v0.9.0 ; AUCUNE règle modifiée, AUCUNE couche d'exécution ajoutée, hiérarchie inchangée — le protocole CONSIGNE, il ne légifère pas

**Le contexte qui fonde la décision (11/11).** La consolidation suit le franchissement : M10 franchi le 11/11 (D178), la version 0.1.1 commandée le jour même (D179) — la v0.9.0 consigne L'ÉTAT et OUVRÉ le programme d'après M10 au document.

**Les rejets nommés (v0.9.0).** Rafraîchir la table R10 au scellage de la 0.1.0 (rejeté : la pièce ne bouge jamais au scellage — fait de carte ; la dette se paie à la version suivante, D178) ; sceller la 0.1.1 au build sans le run (rejeté : le miroir D165/D170 exige la pièce) ; rouvrir M10 pour la 0.1.1 (rejeté : version de maintenance à contrat stable, R4) ; modifier les notations D172–D175 (rejeté : le code byte-identique au vécu, les notations décrivent LA PIÈCE — R2/R5).

**Frontières.** Les archives v0.2 → v0.8.4 DEMEURENT ; le Livre du Coffre v1.1 INCHANGÉ ; aucune balise ne bouge ; la dette [R10-PÉRIMÉE] SOLDÉE (D179) ; l'artefact PDF : docs/Protocole_TRIADE_v0.9.0_Specification.pdf (51 pages, sha256 465331b2…, consigné n°39 au registre D134 — pdf_qa WARN, la classe connue des tirets cadratins consignée depuis D133, l'overflow p.32 le faux positif des filets du tableau des jalons).
## D181 — LA BALISE `loupe 0.1.1` SCELLÉE SUR LE DOUZIÈME RUN VERT RECOUPÉ : LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE (le miroir D165/D170/D178 porté à l'ère 0.1.1 : le scellage REFUSE en l'absence du verdict du recoup vert — la porte est de PROCESSUS, jamais de console ; LA PIÈCE VIT AU DÉPÔT — le verdict du douzième run à download/preuves-run-loupe-011-dev1/, recoupé par md5 : la cérémonie est re-expérimentable d'un clone frais) ; LE RUN DU SCELLEMENT DE LA DETTE (T0→T7 TOUT VERT POUR LA CINQUIÈME FOIS, LA CASCADE 205 VÉCUE ENTIÈRE POUR LA DEUXIÈME, LA VITRINE VIVANTE LA TROISIÈME FOIS [0 ET 0 — LA PREMIÈRE DE LA PIÈCE 0.1.1, aucun WER], le recoup 39/39 — LE VERT TIENT ENTIER) ; LA DOCTRINE [SONDE-EXE] TENUE ET LE RÉSIDU DU PORT NOMMÉ [T0-PÉRIMÉ] (le bandeau « génération 16, à régénérer au labo » du scénario porté — texte d'ère dev.12, AUCUNE porte touchée : les gates exactes, les pièces du run immuables D154) ; LE SCELLAGE EST UN FAIT DE CARTE, L'ARTEFACT NE BOUGE JAMAIS (la cristallisation 26 × 10/10 exigée au geste — les huit passes depuis les compteurs 2/10 de D179, la recomposition == la pièce à chaque passe : PLUS AUCUN écart ; la bascule version=0.1.1-dev.1 → 0.1.1 dans frag-bld, occurrence unique vérifiée en mémoire ; l'entête balise version=0.1.1 génération 17 ; la re-signature à la graine durable D144 : LE TÉMOIN NE BOUGE PAS ; loupe.exe INTACT c1115105… — LE MÊME binaire que LE DOUZIÈME RUN a couru) ; L'ANTI-ROLLBACK ARMÉ (la reconstruction REFUSÉE, constaté au geste même ; la 0.1.0 scellée DEMEURE — la monotonie R10 ouvre l'ère suivante, jamais elle ne referme l'ancienne : (0,1,1,−1,1) < (0,1,1,0,0) refuse toute pré-version de la 0.1.1)

**Le contexte qui fonde la décision (11/11).** La version 0.1.1 fut commandée le 11/11 (D179 : la dette [R10-PÉRIMÉE] soldée à la naissance), le douzième run couru sur le champ, les preuves déposées au coffre — la boucle COMMANDÉ → NÉE → VÉCUE → RECOUPÉE → SCELLÉE bouclée en un jour : la version de maintenance à contrat stable (R4/R10), l'ère ouverte et refermée le même jour.

**Les règles.** (1) **La finale se scelle sur pièces, jamais sur console** : le --sceller-final EXIGE le verdict du recoup terrain VERT (39/39 + les cinq portes assertées : le vert, le recoup, la condition, l'empreinte, la vitrine) — D138/D145/D148/D154 étendues au geste final, le miroir de D165/D170/D178 à l'ère 0.1.1. (2) **Le scellage est un fait de carte** : la balise 0.1.1 vit dans frag-bld (occurrence unique, bascule vérifiée en mémoire), l'entête la porte, loupe.exe INTACT — le binaire que le terrain a couru EST le binaire final. (3) **L'anti-rollback arme l'ère refermée** : la carte scellée (0.1.1) interdit la reconstruction (R6) — constaté au geste même ; la re-vérification sous la balise scellée demeure licite (R5/R7). (4) **La clôture accompagne le scellage** : le run archivé AVEC son jugement (preuves-run-loupe-011-dev1/ au coffre ET au dépôt), le dossier du run corbeillé après recoup pièce à pièce (D99), le réceptacle ré-armé à l'ère scellée, le kit du scellement demeuré au coffre (loupe-kit-13). (5) **Aucune règle du cœur n'est modifiée** — la décision constate un scellage, elle ne légifère pas.

**Frontières.** La balise `loupe 0.1.0` SCELLÉE DEMEURE (054de960…) ; les balises sœurs INTACTES ; les notations D172–D175 INTACTES (R2) ; les secrets au seul .keys/ (D12) ; la clé privée jamais traversée (D87). Les pièces : loupe/ (l'ère 0.1.1 scellée, la carte génération 17 — l'entête version=0.1.1), le kit 0.1.1-dev.1 au coffre /test (loupe-kit-13, la vague du scellement), download/preuves-run-loupe-011-dev1/ (VERDICT e553ac8c… + les deux témoins), scripts/rapatrier_run_011_dev1.py, scripts/recouper_run12_011.py, scripts/depot_entree_222.py.


## D182 — L'ÉDITION ACADÉMIQUE v0.10.0 : LE MANUSCRIT IMRAD EN ANGLAIS (résumé français inclus) NÉ DU DÉPÔT — quatre questions de recherche, les données réelles du journal EXTRAITES PAR SCRIPT (le manuscrit n'affirme rien qui ne soit vérifié), LA FORMULATION CORRIGÉE dans les termes standards de l'ingénierie, l'auteur humain unique (l'agent IA en méthodes et remerciements, JAMAIS co-auteur), les déclarations Ethics/dual-use, Data Availability, Limitations EXPLICITES ; les livrables `TRIADE_soumission_v0.10.0.zip` (cinq fichiers au plus, readme inclus, le manuscrit en pdf — prêt pour un comité de révision) et `TRIADE_complet_v0.10.0.zip` (l'intégralité : sources, bibliographie, données, script d'extraction, extraits de journal, empreintes) ; AUCUNE règle modifiée, AUCUNE couche d'exécution ajoutée, hiérarchie inchangée — l'édition CONSIGNE, elle ne légifère pas (le modèle D180)

**Le contexte qui fonde la décision (11/11).** La commande du développeur : trois fichiers d'instructions au dossier `/instructions` du coffre — le premier ordonne l'édition académique publiable à partir du dépôt (spécification v0.9.0, DECISIONS.md, journaux, archives-preuves). Le projet est entré en manuscrit : M10 franchi, la balise `loupe 0.1.1` scellée (D181), l'ère de consolidation ouverte — le moment où les données vécues deviennent un rapport évaluable par des tiers.

**Les règles.** (1) **Quatre questions de recherche structurent le manuscrit** : le taux de défauts échappés (onze classes nommées sur douze runs terrain — chaque défaut passé TOUS les contrôles labo avant d'être nommé au terrain), le coût en tokens par changement validé (51 / 719 / 1 088 mesurés M1, D31/D34, cibles 64/3 000/6 000), les classes de défauts invisibles à l'émulation (CINQ familles : chargeur/image, ABI/SSE, sémantique du chargeur de bibliothèque, conventions de codes d'erreur, hypothèses du harnais), la sûreté du patch à chaud (zéro régression post-patch, monotonie signée, anti-rollback armé). (2) **Chaque donnée est GÉNÉRÉE, jamais tapée** : `scripts/extraire_donnees_v100.py` extrait et VÉRIFIE (le script refuse si une ancre manque au journal) — jalons, budgets, volumes d'oracle, les douze runs, les empreintes ; le manuscrit `\input` les tableaux générés. (3) **La formulation corrigée** : « le compilateur disparaît » devient « aucune chaîne de traduction optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ; « code volé inexploitable » devient « l'évolution du code volé est bloquée, son exécution ne l'est pas » ; les majuscules emphatiques et le vocabulaire sacralisant cèdent aux termes standards (key ceremony, signed manifest, sealed build) ; l'invariant D19 est requalifié POLITIQUE DE PROJET EXPLICITE (la hiérarchie demeure la règle du projet — le manuscrit le dit dans les termes de l'ingénierie). (4) **L'auteur humain unique** : Alexis Lopez (concédant BSL, D84) ; l'agent IA (Z.ai GLM) est décrit en section Methods (modèle, rôle, disponibilité des transcripts = le journal + le worklog) et en Acknowledgments — JAMAIS co-auteur. (5) **Les déclarations exigées** : Ethics/dual-use (aucun mécanisme de furtivité, la transparence vis-à-vis du système est totale — § 1.2 de la spécification), Data Availability (le dépôt + un DOI Zenodo à créer au dépôt — l'édition ne MENT pas : le DOI n'existe pas encore, le manuscrit le dit), Limitations (N=1, la circularité de l'oracle, l'absence de baseline, la sécurité mémoire non prouvée, le temps constant non analysé) ; toute affirmation sans donnée jointe est marquée « hypothesis » ou « future work ». (6) **La bibliographie est vérifiable** : chaque entrée porte un DOI ou une référence institutionnelle — Meyer 1992 (10.1109/35.165509), Avizienis 1985 (10.1109/TSE.1985.231893), Claessen & Hughes 2000 (10.1145/351240.351266), DO-178C (RTCA 2011), Lamb & Zacchiroli 2022 (10.1109/MS.2021.3073045), in-toto (USENIX Sec 19), SLSA (slsa.dev), TUF (10.1145/1866307.1866315), Sigstore (10.1145/3548606.3560596), RFC 4033, Shamir 1979 (10.1145/359168.359176), Hicks & Nettles 2002 (10.1145/512529.512553), kpatch, Liu et al. 2024 (10.1162/tacl_a_00638), RepoCoder (10.18653/v1/2023.emnlp-main.151), SWE-bench (10.48550/arXiv.2310.06770), RFC 8446/8448. **La revendication de nouveauté est l'intégration du pipeline, l'épistémologie oracle/terrain et la gouvernance de l'intention signée — PAS les primitives.**

**Alternatives rejetées.** Anonymiser le manuscrit pour un double-aveugle — rejeté : la single-auteur et l'agent décrit en méthodes sont des exigences de la commande. Traduire la spécification v0.9.0 — rejeté : le manuscrit est une PIÈCE NOUVELLE (IMRAD, les données), pas une traduction ; la spécification demeure la source normative. Inclure l'agent comme co-auteur — rejeté : la politique d'auteur est explicite (l'auteur humain assume le contenu). Étendre les données au-delà du journal — rejeté : toute affirmation sans donnée extraite est marquée hypothesis/future work.

**Frontières.** La chaîne `scripts/manuscrit_v100/` (main.tex, refs.bib, donnees/ GÉNÉRÉES) ; le manuscrit docs/TRIADE_manuscrit_v0.10.0.pdf ; la chaîne spec_v100 née de spec_v090 (la v0.9.0 DEMEURE : sources et PDF archivés) ; le md PROTOCOLE_TRIADE.md en v0.10.0 (§ 1.11, § 19.12, journal des versions) ; le PDF formel docs/Protocole_TRIADE_v0.10.0_Specification.pdf. Aucun artefact scellé ne bouge ; aucun arbre signé ne bouge ; les données du manuscrit sont celles du journal, extraites et vérifiées.

## D183 — LA PROPOSITION DE SÉQUESTRE CHIFFRÉ DE LA PHRASE DE CONTRÔLE (l'alternative à la garde durable D81 — documentée, NON appliquée au coffre réel : l'arbitrage PERTE > EXPOSITION demeure LA décision active, aucune clé touchée, aucun conteneur réécrit, le geste appartient au développeur)

**Le contexte qui fonde la décision (11/11).** La tension de D81 est consignée depuis le 28/10 : la phrase de contrôle du coffre-fort vit EN CLAIR au dépôt et au coffre Drive (le fichier EST la remise) — la survie du coffre contre la confidentialité au repos. La commande d'édition exige l'alternative documentée : le séquestre chiffré, avec l'analyse comparative chiffrée des risques perte/exposition. La présente décision NE CHANGE RIEN au coffre réel : elle consigne la proposition et son analyse, pour le geste du développeur s'il l'arbitre.

**La proposition.** Deux variantes : (a) **le chiffrement vers clé hors-ligne** — la phrase chiffrée (XChaCha20-Poly1305, la suite du coffre) vers une clé Ed25519-adjacente tenue hors-ligne (le modèle de la graine durable D144 : jamais dans le bac à sable, jamais au nuage) ; le fichier chiffré remplacerait PHRASE-CONTROLE-COFFRE.txt au dépôt, la phrase en clair RETIRÉE ; (b) **le partage Shamir à seuil** — la phrase répartie en parts (le modèle CF2 D120 : 5 parts à seuil 3), les parts réparties sur des médias séparés (dépôt, coffre Drive, USB, papier, tiers de confiance) ; en dessous du seuil, une part ne révèle RIEN.

**L'analyse comparative chiffrée (annualisée, ordres de grandeur explicites — des hypothèses de modélisation, pas des mesures).** État actuel (D81) : la phrase en clair vit à QUATRE emplacements (le dépôt git, GitHub, le miroir Drive, la racine du coffre Drive). Risque de PERTE : il faut perdre les QUATRE simultanément — de l'ordre de 10⁻⁶/an (quatre stockages, trois systèmes indépendants). Risque d'EXPOSITION : UN seul emplacement compromis suffit ; avec p ≈ 1 %/an de compromission par emplacement (compte cloud, partage par lien mal configuré — l'incident D76/D78 l'a vécu : ~64 minutes de fenêtre d'exposition réelle), l'exposition ≈ 1 − (1−p)⁴ ≈ 3,9 %/an. Variante (a) clé hors-ligne : la perte espérée devient CELLE DE LA CLÉ UNIQUE (média unique hors-ligne, de l'ordre de 1 à 5 %/an sans duplication) ; l'exposition tombe à la compromission cryptographique (négligeable, < 10⁻⁹/an). Variante (b) Shamir 5/3 : la perte exige ≥ 3 parts perdues sur 5 réparties (≈ 10⁻⁴/an si deux parts au moins vivent hors nuage) ; l'exposition exige ≥ 3 parts compromises (≈ 10⁻⁵/an, chaque part étant inerte sous le seuil). Avec C_perte ≈ 10 × C_exposition (la perte du coffre est IRRÉVERSIBLE — toutes les phrases maîtresses perdues à jamais, l'exposition étant remédiable par rotation, D80 l'a prouvé) : la perte espérée annuelle est ≈ 4,0 × 10⁻²·C_exposition sous D81, contre ≈ 1,0 × 10⁻³·C_exposition sous la variante (b) — **un facteur ~40 en faveur du séquestre Shamir** ; la variante (a) est ÉCARTÉE par l'analyse elle-même (le point de défaillance unique de la clé hors-ligne inverse l'arbitrage : la perte espérée monte à ~2 × 10⁻²·C_perte).

**Pourquoi D81 demeure néanmoins la décision active.** (1) Le geste n'appartient qu'au développeur : la cérémonie exige SA clé hors-ligne (le modèle D87 — jamais générée par le labo, « JAMAIS generer »). (2) Le coffre réel est CF3 : la serrure piégée et l'époque croisées conteneur/piège (D121) protègent déjà contre l'evil maid — l'exposition de la phrase ne donne pas l'écriture, seulement la lecture. (3) L'incident fondateur de D81 (la phrase D80 JAMAIS remise, un décès d'infra de plus et le coffre indéchiffrable) reste l'événement de référence : la proposition ne se substitue à la garde durable QUE si la cérémonie des parts est VÉCUE de bout en bout (parts réellement créées, réellement réparties, reconstitution PROUVÉE à froid) — sinon elle ajoute un risque de perte. (4) Les mitigations en vigueur (partage par lien restreint, corbeille vidée, rotation au moindre doute) demeurent.

**Alternatives rejetées.** La variante (a) clé hors-ligne unique — rejetée par l'analyse : point de défaillance unique, la perte espérée dépasse celle de D81. Conserver le md5 de la phrase au dépôt comme « preuve de contrôle » — hors sujet (une empreinte ne déchiffre rien). Une part Shamir unique AU nuage — rejeté : sous le seuil une part est inerte, mais toutes les parts au même nuage = le nuage EST le coffre.

**Frontières.** RIEN n'est appliqué : PHRASE-CONTROLE-COFFRE.txt demeure (la garde D81), le conteneur du coffre-fort INTACT, aucune clé générée, aucun secret manipulé. L'analyse vit dans la présente décision ; le manuscrit v0.10.0 la cite comme proposition (D183) dans sa section discussion. Le geste, s'il vient : une cérémonie documentée (création des parts, répartition, PREUVE de reconstitution à froid, puis retrait de la phrase en clair) — jamais un hot-fix silencieux.

## D184 — LES EMPREINTES DE GOUVERNANCE MIGRENT DE MD5 À SHA-256 (l'annexe A de la spécification — les modules du coffre — recalculée au contenu canonique LF, la même méthode, l'empreinte longue) ; MD5 DEMEURE UNIQUEMENT UNE FONCTIONNALITÉ D'AFFICHAGE DE LOUPE (le panneau d'empreintes, loupe-06 — RFC 1321 notée à la spécification) ; AUCUN octet de la pièce ne change, et les empreintes md5 des preuves historiques DEMEURENT — les preuves ne se réécrivent jamais

**Le contexte qui fonde la décision (11/11).** La gouvernance du projet a longtemps consigné ses empreintes en md5 (32 hex) — l'héritage des kits terrain (le recoup md5 par relecture, D99/D143) et du panneau d'empreintes de Loupe. La commande d'édition exige le passage des empreintes de GOUVERNANCE à sha-256 : la longueur de 64 hex porte la marge de sécurité requise pour des empreintes qui font autorité (la résistance aux collisions de md5 est brisée depuis 2004 — les empreintes de gouvernance n'ont pas à dépendre d'un algorithme à collisions choisies), SANS toucher à la pièce ni aux preuves.

**Les règles.** (1) **Le périmètre est la documentation de gouvernance vivante** : l'annexe A de la spécification (les 15 modules du coffre : coffre_fort.py racine + coffre_cf2/coffre_cf3/sceau_I/cérémonies/sentinelle/tests) passe à sha-256, calculée AU CONTENU CANONIQUE LF du dépôt — la même méthode que D133, l'empreinte longue. (2) **md5 demeure une fonctionnalité de Loupe** : le panneau d'empreintes (loupe-05 sha-256, loupe-06 md5, loupe-07 le cumul) est une FONCTIONNALITÉ DE L'APPLICATION — l'éditeur hexadécimal affiche les deux, comme tout éditeur du métier ; la spécification loupe-06 note la RFC 1321 ; la pièce scellée ne bouge PAS (R4/R6/R7 : loupe.exe INTACT c1115105…, 054de960… pour la 0.1.0). (3) **Les preuves historiques demeurent en md5** : les empreintes consignées au journal (les recoups des douze runs, les archives-preuves, les manifests de kit) restent CE QU'ELLES SONT — réécrire des preuves serait la faute la plus grave du protocole (l'append-only est la promesse) ; le présent et le futur consignent en sha-256. (4) **La migration est documentée** : § 1.11, § 19.12, l'annexe A de la v0.10.0, la présente décision ; les kits terrain à venir consigneront leurs manifestes en sha-256 (la vague du prochain run — jamais un kit déjà livré). (5) **Le registre D134 demeure** : les empreintes par build (loupe.exe, proxy.exe, les PDF) sont DÉJÀ consignées en sha256 depuis M5 — la présente décision aligne l'annexe de gouvernance sur la pratique du registre.

**Alternatives rejetées.** Réécrire les preuves historiques en sha-256 — rejeté : les preuves sont immuables, l'append-only est la promesse fondatrice. Supprimer le panneau md5 de Loupe — rejeté : c'est une fonctionnalité d'affichage de l'application scellée, la pièce ne bouge jamais. Migrer les manifests des kits DÉJÀ livrés — rejeté : les kits livrés sont des preuves (le recoup md5 par relecture les garde) ; seuls les kits à venir consignent en sha-256.

**Frontières.** Aucun artefact scellé ne bouge (loupe.exe, proxy.exe, les balises) ; aucun arbre signé ne bouge ; les 15 empreintes sha-256 vivent à l'annexe A de la spécification v0.10.0 (docs/Protocole_TRIADE_v0.10.0_Specification.pdf) ; le registre D134 inchangé (déjà sha256) ; les preuves historiques md5 inchangées.


## D185 — LES PREUVES RENFORCÉES : LES SIX INSTRUMENTS DE LABORATOIRE (le deuxième fichier d'instruction exécuté — « renforcer le niveau de preuve sans modifier aucun artefact scellé » : AUCUN octet d'artefact, d'arbre signé ou de notation ne bouge ; les instruments vivent au laboratoire, les graines sont consignées, tout est reproductible) ; CE QUI RESTE NON PROUVÉ est MARQUÉ EXPLICITEMENT — la méthode exige que la limite soit un chiffre, jamais un silence

**Le contexte qui fonde la décision (11/11).** La commande du développeur (le deuxième fichier au dossier /instructions) : renforcer le niveau de preuve de l'édition académique. Le laboratoire exécute les six chantiers de la commande avec les instruments EXISTANTS comme tueurs et juges — jamais un instrument nouveau ne remplace un ancien, il s'AJOUTE.

**Les règles.** (1) **LE MUTATION TESTING** (scripts/mutation_v110.py, graine 20261111, 16 mutants/bloc) : des mutants d'un octet des blocs scellés — INSTRUCTIONS, OPÉRANDES, OFFSETS — dans des COPIES DE LABORATOIRE (la mutation vit en mémoire d'émulation par mem_write + ctl_remove_cache, le miroir reposer_bloc du harnais M8 ; la pièce scellée JAMAIS écrite), tués par LES INSTRUMENTS EXISTANTS dans l'ordre du coût : K1 le round-trip (capstone→keystone, R5), K2 l'oracle structurel (le plan : mnémoniques, cibles d'appel, feuilles IAT, déplacements RIP), K3 le différentiel sémantique aux vecteurs officiels (les 19 blocs de calcul pur tls13 + loupe-06 via la mini-OS du noyau). RÉSULTAT : 832 mutants, 694 tués (83,4 %) — loupe 79,9 %, tls13 88,6 %, sys 69,8 % ; les familles cryptographiques (sha, hkdf, f25519/x25519, aes/gcm, md5) à 100 % ; les 138 survivants CONCENTRÉS dans les blocs d'orchestration/UI (le sémantique n'y est pas câblé au mutant isolé — leur preuve demeure le harnais complet en composition) : LA LIMITE EST MESURÉE ET NOMMÉE, c'est le résultat. (2) **LE FUZZAGE GUIDÉ PAR COUVERTURE** (fuzzage_v110.py, graines 20261111/20261112) : loupe-01 (le chemin non fiable — l'OS virtuel étendu à 16 témoins, les canaris autour du tampon, le corpus guidé par la couverture) : 72/119 instructions couvertes (60,5 %), zéro crash, zéro violation de canaris, corpus 18 ; http-10 (le parseur, la pièce 0.4.0 scellée par le fuzzer du million D72 repris, le crochet mémoire P5) : 358 instructions couvertes, zéro crash, zéro faute nommée, corpus 17. (3) **LA SÛRETÉ MÉMOIRE STATIQUE BORNÉE** (surete_memoire_v110.py) : l'extension de l'audit msx64 (l'Entrée 207) en interprétation abstraite des 52 blocs : 2 098 accès classés — 1 181 accès pile VÉRIFIÉS contre la borne du cadre (le plus grand sub rsp unique d'un chemin + les pushes + le home space + les arguments pile : ZÉRO hors-cadre, la classe du stack-smash est ABSENTE des notations), 263 médiés-contrat (bornes au PRE de la spec I, citées), 191 constants [rip], 463 non résolus NOMMÉS (volatils recomputés, indexations composées). LES LIMITES CONSIGNÉES : analyse linéaire, corps de boucle une fois, aucun alias, bornes d'arguments croisées au contrat — une vérification BORNÉE, pas une preuve. (4) **LE TEMPS CONSTANT** (temps_constant_v110.py, N=60/classe, seuil |t|>5) : le dudect D'ÉMULATION (le t de Welch sur les comptages d'instructions du harnais, la métrique structurelle) : TOUTES les familles crypto CONSTANTES (t=0 : traces indépendantes du secret ; x25519 : 1 238 959 instructions pour TOUTE clé privée — l'échelle à 255 marches constante par construction) ; md5 (loupe-06) constant au contenu. LA LIMITE EXPLICITE : le temps d'horloge du terrain (caches, prédiction de branchement) N'EST PAS MESURÉ — la propriété démontrée est structurelle, le temps réel reste NON PROUVÉ et marqué tel. (5) **LES BENCHMARKS COMPARATIFS** (benchmarks_v110.py, bench_v110_c/bench.c) : la référence C à CONTRAT ÉQUIVALENT (sha256 vérifié contre hashlib AVANT toute mesure — l'instrument se contrôle avant de juger), compilée gcc 14.2 -O2 et -Os (LA RÉFÉRENCE CLANG EST ABSENTE DU LABORATOIRE : l'écart est nommé, gcc tient la place), mesurée DANS LA MÊME ÉMULATION que les blocs (les conditions identiques par construction) : sha256(1024 o) — les blocs notés à la main 4 524 instructions/op pour 765 octets, la référence gcc -O2 69 132 instructions/op pour 5 436 octets, gcc -Os 77 505 pour 3 072 : un facteur 15,3 en instructions (17,1 contre -Os) ; le débit d'émulation comparable (27-31 ops/s — dominé par l'émulateur, le chiffre absolu appartient à l'outil, jamais au terrain). MD5 ET AES : la référence C écrite à la main FAUTAIT (l'auto-vérification hashlib/FIPS 197 l'a attrapée : le rotate md5, les coefficients MixColumns, l'expansion de clé aes — TROIS fautes consécutives attrapées, le banc a REFUSÉ de mesurer) : les comparaisons sont ÉCARTÉES de l'édition — JAMAIS UN CHIFFRE FAUX ; la référence md5/aes sera posée depuis une implémentation auditée à l'édition suivante. (6) **L'INDÉPENDANCE DE L'ORACLE** (independance_v110.py, graine neuve 20261113) : l'oracle re-généré par des voies DISTINCTES de celles du geste — les tables MD5 T[64] re-dérivées par l'arithmétique DÉCIMALE (série de Taylor en Decimal, distincte de la voie entière), K[64] SHA-256 par les racines cubiques décimales, les vecteurs RFC 1321 confrontés TRIPLEMENT (spec I par citation ↔ harnais par table ↔ hashlib le modèle du système), les différentiels sha256/md5 rejoués à 200 messages os.urandom (le générateur du SYSTÈME, distinct du module random du geste) : ZÉRO DIVERGENCE sur toutes les confrontations. LA LIMITE : le « modèle distinct » est un modèle de CALCUL distinct, pas un agent codeur distinct — la re-génération par un second agent demeure la réplication à venir.

**Les artefacts.** scripts/preuves_v110/ (les CSV/JSON/rapports des six instruments), scripts/mutation_v110.py, fuzzage_v110.py, surete_memoire_v110.py, temps_constant_v110.py, benchmarks_v110.py, independance_v110.py, extraire_donnees_v110.py, bench_v110_c/, manuscrit_v110/, spec_v110/, docs/TRIADE_manuscrit_v0.11.0.pdf, docs/Protocole_TRIADE_v0.11.0_Specification.pdf.

**Alternatives rejetées.** Réécrire les tueurs (des instruments nouveaux pour tuer les mutants) — rejeté : la commande exige les instruments EXISTANTS comme juges ; l'ajout est l'exception (les crochets de couverture). Mesurer le temps réel des blocs — rejeté : le terrain de mesure (la machine du développeur) n'est pas au laboratoire ; un chiffre d'émulation maquillé en temps réel serait la faute. Publier les comparaisons md5/aes sur la référence fautive corrigée à la hâte — rejeté : la correction sous pression est la source même de la faute attrapée ; l'attente d'une référence auditée est la décision.

**Frontières.** Aucun artefact scellé ne bouge (loupe.exe c1115105…, proxy.exe 446279f3…, les balises INTACTES) ; aucun arbre signé ne bouge (le garde 14/14 le constate) ; aucune notation ne bouge (R2) ; les six instruments au LABORATOIRE ; les graines consignées dans les scripts (reproductible d'un clone frais) ; les CORRECTIONS des vérificateurs figés (verifier_specs_m9a : l'ère dev.4 ; verifier_specs_m9d : sys-05 R2/sys-06 R3 — les instruments portés à l'ère courante pour que l'obligation de rejeu soit honorable, l'arbre I inchangé).

## D186 — LA SPÉCIFICATION CSPRNG COMBLÉE AU LABORATOIRE (le brouillon tls13-29-source-csprng : la couche I manquante de la source d'aléa — le générateur EST le CSPRNG de l'OS hôte via le kit [Python os.urandom : ProcessPrng/BCryptGenRandom, le CTR_DRBG du noyau], le reseed est LA POLITIQUE DU NOYAU jamais contournée, l'échec est FAIL-CLOSED [le kit s'arrête AVANT toute session], le KIT96 EST LA SEULE INTERFACE [aléa 32 || clé privée 32 || empreinte 32], la clé privée ÉPHÉMÈRE PAR SESSION jamais au dépôt) ; L'ENTRÉE À L'ARBRE SIGNÉ ATTEND LA CÉRÉMONIE D'ÈRE DU DÉVELOPPEUR (le quinzième arbre, le modèle D177 : la clé hors-ligne, « JAMAIS generer ») ; LES VECTEURS RFC 8446 AU CORPUS DE FIXTURES PARTAGÉES (les constantes normatives natives — les sentinelles DOWNGRD § 4.1.3, la valeur magique HRR, les types d'enregistrement § 5.1, la suite 0x1301 § 6, le groupe 0x001D § 4.2.7 — avec leur paragraphe d'origine ; le plan RECOISÉ : SUITE/GROUPE/HRR conformes)

**Le contexte qui fonde la décision (11/11).** La commande nommait la spécification I manquante de la source CSPRNG (le chantier 4 : « rédiger la spécification I manquante de la source CSPRNG — générateur, reseeding, échec fail-closed ») et les vecteurs RFC 8446 au corpus de fixtures. L'architecture de l'aléa du domaine tls13 : la pièce NE GÉNÈRE JAMAIS (charte § 6 : aucun état détenu) — le KIT du terrain fournit (le KIT96 du scénario-m9f : os.urandom deux fois par session, l'aléa du ClientHello et la clé privée x25519). La spécification nomme CE contrat de provision, la frontière de confiance kit/pièce.

**Les règles.** (1) Le brouillon vit à tls13/notation/brouillons/tls13-29-source-csprng.md — le gabarit de couche I au complet (Intention, Contrat pre/post/inv, Vecteurs [RFC 8448, RFC 7748 § 6.1, le KIT96 du septième run], Provenance [RFC 8446 § 4.1.2 « MUST be generated with a CSPRNG », la documentation de l'hôte], Décisions) ; il est BROUILLON tant que la cérémonie d'ère n'a pas signé le quinzième arbre — la référence de laboratoire d'ici là, le code du kit et de la pièce INTACTS. (2) Le générateur est PARAMÉTRABLE PAR LE DÉVELOPPEUR (D15) : remplacer os.urandom est un changement de KIT, pas de pièce. (3) L'aléa n'est JAMAIS une entrée de décision (la pièce ne branche sur aucun octet de l'aléa — le temps constant structurel, I3). (4) Le corpus RFC 8446 (tls13/fixtures/rfc8446.py) : chaque constante CITÉE avec son paragraphe, la sentinelle DOWNGRD NOUVELLE AU CORPUS (donnée pour l'avenir : la détection de rétrogradation n'est pas un bloc du domaine, la suite est unique — le vecteur AVANT usage, jamais l'inverse, la charte § 3). (5) Le recroisement du plan : SUITE == 0x1301, GROUPE == 0x001D, HRR_MAGIQUE == SHA-256("HelloRetryRequest") — CONFORMES (le fixture recroise tls13/layout.py, tout écart nommerait une dérive).

**Alternatives rejetées.** Entrer la spécification à l'arbre signé au geste du labo — rejeté : la clé privée Ed25519 ne traverse JAMAIS le bac à sable (D87), la cérémonie d'ère appartient au développeur (D177). Dériver un DRBG maison dans la pièce — rejeté : la pièce ne détient aucun état (charte § 6) et l'OS hôte PORTE un CSPRNG audité ; réécrire l'entropie serait le prématuré condamné par R11.

**Frontières.** Aucun octet de code ne bouge (le brouillon est un DOCUMENT) ; l'arbre tls13/I/ INTACT (14 arbres signés au garde) ; le corpus de fixtures est un OUTIL de laboratoire (jamais dans la pièce) ; la cérémonie d'ère future portera le quinzième arbre (tls13-29 en son sein) — le geste du développeur.


## D187 — LE MODÈLE FORMEL DE CF3 : LES QUATRE PROPRIÉTÉS PROUVÉES DANS LE MODÈLE (l'explorateur d'états explicites : la sémantique opérationnelle de la chaîne du coffre scellé — dérivation KEK [les TROIS éléments entrent, HKDF à contexte d'époque], cycle en deux actes [brouillon chiffré sous clé de session, clés maîtresses mortes, canonique jamais réécrit], anti-retour d'époque [époques croisées conteneur/piège + le miroir de l'époque la plus haute vue], sentinelle instantanée [l'invocation : sans le piège l'ouverture est IMPOSSIBLE, pas seulement refusée], destruction sur falsification PROUVÉE [piège intact + phrase vérifiée + empreinte/AEAD échoue] — en machine à états finie abstraite, les primitives SYMBOLIQUES, l'espace ÉNUMÉRÉ EXHAUSTIVEMENT : 154 états, 1 152 transitions, profondeur 6, époques ≤ 3, l'adversaire à seuil ≤ 2 éléments AVEC le rejeu d'époques passées) ; LES HYPOTHÈSES D'ADVERSAIRE EXPLICITES A1-A5 (A1 le modèle symbolique : HKDF/AEAD/SHA parfaits, Argon2id la phrase inconnue sans le secret ; A2 le seuul : au plus DEUX des trois éléments, tous les sous-ensembles explorés ; A3 le média : falsifiable (le tag) mais jamais ENRICHI (les moitiés futures naissent hors machine) ; A4 les anciens couples : le rejeu complet modélisé ; A5 le HORS MODÈLE : canaux auxiliaires, failles d'implémentation, le vol des TROIS, le quantique — NOMMÉ, jamais confondu avec le prouvé) ; LES MANIFESTES DE KIT À SHA-256 (maj_kit.py : le manifeste du kit de cérémonie consigne sha256, la suite de D184 ; les kits LIVRÉS demeurent — leurs manifestes md5 sont des PREUVES ; md5 à l'idempotence Drive et à l'affichage Loupe)

**Le contexte qui fonde la décision (11/11).** Le troisième fichier d'instruction : « modéliser CF3 dans un vérificateur de protocoles (Tamarin ou ProVerif)… rapporter chaque propriété prouvée, réfutée ou hors modèle, avec les hypothèses d'adversaire explicites ». Tamarin et ProVerif sont ABSENTS du laboratoire (aucun Haskell/OCaml, aucune installation possible) : le choix du vérificateur est NOMMÉ — l'explorateur d'états explicites (model checking borné), la sémantique opérationnelle de v06/coffre_cf3.py transcrite en machine à états, LE SCRIPT EST LE MODÈLE (python3 scripts/modele_formel_v120.py : reproductible d'un clone frais, aucune boîte noire).

**Les règles.** (1) **P1 LE SECRET SOUS SEUIL** : l'adversaire à ≤ 2 éléments n'atteint JAMAIS l'état « secret appris » — 0 contre-exemple sur les 154 états ; la clé : derive_kek lie les TROIS éléments (la possession de la machine seule ne permet même pas d'ESSAYER des phrases — le champ verif exige V_piège, publique mais portée par le média). (2) **P2 LE REFUS DU ROLL-BACK** : aucune transition ne décrémente l'époque (la monotonie structurelle, RE-CONSTATÉE mécaniquement transition par transition) ; le rejeu d'un couple d'époque passée est REFUSÉ NOMMÉ (« RETOUR EN ARRIÈRE », l'époque du couple < le miroir). (3) **P3 L'ABSENCE DE DESTRUCTION SUR PHRASE ERRONÉE** : la phrase erronée mène à PhraseErronee (réessai à délai croissant), AUCUN état atteignable ne combine l'essai erroné et la destruction — 0 contre-exemple ; la destruction exige la falsification PROUVÉE (piège intact + phrase vérifiée + échec cryptographique). (4) **P4 LE RAYON BORNÉ À UNE ÉPOQUE** : la destruction touche l'état LOCAL (le conteneur, le brouillon, le PV), JAMAIS le média du piège (le TÉMOIN, jamais le coupable), JAMAIS les fragments CF2 (la coexistence § 12 : la destruction reste survivable) — 0 violation. (5) **LE RAPPORT PAR PROPRIÉTÉ** : PROUVÉE DANS LE MODÈLE signifie exactement cela — sous A1-A4, dans les bornes déclarées (époques ≤ 3, profondeur 6) ; ce qui sort est HORS MODÈLE et le dit.

**Alternatives rejetées.** Attendre un environnement Tamarin — rejeté : la commande exige l'exécution à cette édition ; l'explorateur nommé fait le travail dans les bornes, le portage Tamarin demeure la voie future (le modèle est documenté, la transcription directe). Modéliser l'implémentation (Python, la RAM, le GC) — rejeté : A5 le nomme HORS MODÈLE ; le modèle vérifie le PROTOCOLE, pas sa réalisation — la falsifiabilité des autotests (92 contrôles) couvre l'écart.

**Frontières.** Aucun artefact scellé ne bouge ; aucun arbre signé ne bouge ; le coffre RÉEL intact (l'autotest vit aux répertoires temporaires, discipline D105 — l'empreinte du conteneur réel CONSTATÉE IDENTIQUE avant/après) ; les manifestes FUTURS à sha256, les kits livrés demeurés.

## D188 — LE MODÈLE DE MENACE EN DEUX PLANS : le plan IP (la propriété intellectuelle — rétro-ingénierie [temps acheté, érodé par les LLM de décompilation], expropriation [l'ÉVOLUTION du code volé bloquée : l'intention signée, l'héritage scellé, les clés hors-ligne, l'homme mort Shamir — son EXÉCUTION ne l'est pas], redistribution [empreintes par build, le canary trap] — la CONFIDENTIALITÉ d'abord, les pertes REMÉDIABLES [rotation, variantes]) ET le plan SÛRETÉ D'EXÉCUTION (l'empoisonnement/corruption de carte [signature, verrou croisé, AEAD], l'evil maid sur conteneur ou média [époques croisées, tags, le champ verif indérivable], le rollback conteneur+piège [les TROIS témoins d'époque], le binaire altéré [checksums par bloc, manifeste signé au chargement], l'environnement non conforme [contrôles de profil, fail-closed], l'agent défaillant [R2/R5, l'oracle issu de I, les budgets] — l'INTÉGRITÉ et la DISPONIBILITÉ d'abord, les pertes IRRÉMÉDIABLES) ; L'ORDRE INTRA-SÉCURITÉ EXPLICITE (la POLITIQUE DE PROJET qui manquait à la hiérarchie D19 : quand les deux plans se rencontrent, le plan sûreté GAGNE — un coffre cassé ne protège rien) ; LA TENSION D81 ↔ D183 CONSIGNÉE AVEC L'ANALYSE CHIFFRÉE (l'espérance de perte annuelle ≈ 4,0 × 10⁻²·C_exposition sous D81 contre ≈ 1,0 × 10⁻³ sous le séquestre Shamir 5/3 — un facteur ≈ 40 ; D81 DEMEURE la décision active, la cérémonie du séquestre appartient au développeur)

**Le contexte qui fonde la décision (11/11).** Le troisième fichier : « restructurer le modèle de menace en deux plans séparés et expliciter l'ordre intra-Sécurité (confidentialité vs disponibilité) qui manque à la hiérarchie D19 ; consigner la tension D81 et la contre-proposition de D182 [D183 après le coulissement de numérotation] avec analyse comparative chiffrée des risques perte/exposition ».

**Les règles.** (1) Les DEUX PLANS sont SÉPARÉS : chaque menace du tableau § 15.1 vit dans SON plan, la contre-mesure et le résiduel y restent ; la distinction fondatrice du protocole (« séparer l'obfuscation qui protège la propriété intellectuelle du durcissement qui protège l'exécution ») devient la STRUCTURE du tableau. (2) L'ORDRE INTRA-SÉCURITÉ : dans le plan IP, la confidentialité domine (les pertes remédiables : la rotation D80 l'a prouvé) ; dans le plan sûreté, l'intégrité et la disponibilité dominent (la perte du coffre est IRRÉVERSIBLE — l'incident fondateur de D81) ; ENTRE les plans, le plan sûreté gagne — c'est une POLITIQUE DE PROJET EXPLICITE (D19 requalifiée par D182 : la hiérarchie quadripartite demeure la règle, l'ordre interne de la sécurité est désormais ÉCRIT). (3) La TENSION D81 ↔ D183 : les deux décisions VIVENT l'une contre l'autre dans le tableau (la garde en clair contre le séquestre chiffré), l'analyse chiffrée de D183 citée — le facteur ≈ 40 en faveur du séquestre, les quatre raisons pour lesquelles D81 demeure néanmoins (le geste du développeur, la protection CF3 existante, l'incident fondateur, les mitigations en vigueur). (4) La restructuration vit À LA SPÉCIFICATION (le § 15 de la v0.12.0, la chaîne spec_v120) et AU MANUSCRIT (§ 4.6) — le tableau du CŒUR assaini, la hiérarchie D19 INTACTE.

**Alternatives rejetées.** Fusionner les plans en un tableau unique annoté — rejeté : la commande exige la SÉPARATION (l'amalgame est précisément le défaut nommé). Modifier la hiérarchie D19 — rejeté : l'ordre intra-sécurité est une politique explicite AJOUTÉE, jamais une règle changée en silence.

**Frontières.** La spécification v0.12.0 porte le tableau restructuré ; le manuscrit § 4.6 le présente ; AUCUNE règle du cœur modifiée ; AUCUN coffre touché (D81 demeure, D183 demeure une proposition).

## D189 — LA CRISTALLISATION ÉVALUÉE ET LE PROTOCOLE DE RÉPLICATION PROPOSÉ : le seuil de 10 rebuilds consécutifs identiques JUSTIFIÉ par le test séquentiel (le SPRT de Wald sur la probabilité de divergence q par rebuild : H0 q ≤ 1 % contre H1 q ≥ 50 % — CINQ rebuilds identiques atteignent déjà α = 5 %, le seuil historique DIX atteint α = 1,08 × 10⁻³, 46× plus strict que le canonique) — LE SEUIL DEMEURE 10 (la politique de projet, jamais changée en silence : l'analyse est la JUSTIFICATION consignée, la voie documentée d'un relâchement futur SI le développeur l'arbitre) ; LE PROTOCOLE DE RÉPLICATION (les trois axes indépendants : R1 un second développeur mène un jalon complet depuis le dépôt public ; R2 une seconde application réelle neuve en un autre domaine ; R3 le port d'un bloc vers un profil non primaire — avec la GRILLE DE CODAGE T/X à CINQ classes terrain [T1 chargeur/image, T2 ABI/matériel, T3 sémantique du chargeur, T4 conventions système, T5 environnement] et TROIS classes laboratoire [X1 logique, X2 structure, X3 harnais], la DOUBLE ANNOTATION par deux codeurs indépendants, le KAPPA DE COHEN [κ ≥ 0,61 l'acceptation : substantiel], les critères d'acceptation PRÉ-ENREGISTRÉS [le jalon franchi, les défauts codés, les classes T du réplicant ⊆ celles du premier développeur — une classe NOUVELLE est un RÉSULTAT, jamais un échec]) — PROPOSÉ, JAMAIS EXÉCUTÉ (N = 1 demeure la limite déclarée du manuscrit, l'arbitrage et les ressources appartiennent au développeur)

**Le contexte qui fonde la décision (11/11).** Le troisième fichier : « évaluer la cristallisation : proposer un modèle statistique justifiant le seuil de 10 vérifications — ou le remplacer par un critère de confiance séquentiel — et un protocole de réplication… avec grille de codage T/X à double annotation et kappa de Cohen ».

**Les règles.** (1) LE MODÈLE : chaque rebuild est une épreuve de Bernoulli (divergence q) ; le SPRT accepte « déterministe » quand Λₙ = ((1−q₀)/(1−q₁))ⁿ ≥ 1/α — les bornes du projet (q₀ = 1 %, q₁ = 50 %, α = 5 %) donnent n = 5 ; le seuil 10 atteint α = 1,08 × 10⁻³ (≈ 3,3σ). (2) LE SEUIL DEMEURE : la règle R6 est la POLITIQUE de projet — l'analyse la justifie (46× plus strict que nécessaire) et documente la voie d'un relâchement (5 rebuilds au même α que le canonique) — JAMAIS changée en silence. (3) LE PROTOCOLE : le document scripts/preuves_v120/protocole_replication.md (les trois axes avec leurs mesures, la grille T/X — l'EXTENSION naturelle des classes constatées aux douze runs Loupe [les T1-T5 sont exactement les cinq familles du RQ3], la double annotation, le κ de Cohen avec l'interprétation de Landis & Koch, les quatre critères d'acceptation pré-enregistrés, le coût estimé). (4) La grille T/X relie le protocole À L'EXPÉRIENCE VÉCUE : les classes T1-T5 du manuscrit § 4.5/RQ3 SONT la grille — la réplication codera les défauts dans la taxonomie que la méthode a déjà produite.

**Alternatives rejetées.** Remplacer le seuil 10 par le SPRT à 5 — rejeté : changer une règle du cœur exige l'arbitrage du développeur (l'analyse est consignée, la décision lui appartient). Exécuter la réplication à cette édition — rejeté : un second développeur n'est pas au laboratoire ; exécuter le protocole soi-même serait la nier (N = 1 demeure la limite HONNÊTE, le protocole est la voie de sa levée).

**Frontières.** Le protocole est un DOCUMENT PROPOSÉ ; aucune réplication exécutée ; le seuil 10 inchangé ; le manuscrit v0.12.0 déclare la limite et la voie.
