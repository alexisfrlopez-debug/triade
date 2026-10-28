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
