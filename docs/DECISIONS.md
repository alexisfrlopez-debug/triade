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
