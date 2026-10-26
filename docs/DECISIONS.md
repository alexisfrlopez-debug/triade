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
