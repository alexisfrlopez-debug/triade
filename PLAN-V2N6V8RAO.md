# PLAN GELÉ — V2N6V8RAO (la vague 15)
> L'atelier kit développeur : produire TRIADE_kit_developpeur depuis le dépôt
> PAR CONSTRUCTION (motif D130 : git ls-files, jamais de maintenance manuelle),
> archive déterministe, déposé à chaque changement de CONTRAT — pas à chaque
> vague éditoriale.
> Gelé AVANT toute construction.

## Le mandat
(1) **LE MANIFESTE.txt** : commit de référence, sha256 par fichier, vecteur de
versions kit↔protocole↔carte↔profil, plage de compatibilité ; LA PORTE
verifier-compatibilite fail-closed sur tout triplet incompatible ; check-update
optionnel, jamais une dépendance réseau au build.
(2) **LE CONTENU M0-in-a-box** : notation+round-trip, carte+expandeur
pointeur-seul (4 refus nommés), LE GÉNÉRATEUR d'oracle depuis I (JAMAIS
d'oracle pré-dérivé expédié) + vecteurs FIPS/RFC + routes d'indépendance, les
portes R1–R11, la cérémonie de genèse de clé air-gap + sceau LOCAL (AUCUNE
ancre de confiance du projet expédiée : ni cle-publique-I.txt comme ancre, ni
signatures de référence comme garde de build adopteur), init coffre à
l'arbitrage D137, kit terrain générique + dictionnaire des refus, gabarits
versionnés sha256-gravés, quickstart 1 page, table des gaps nommés, licence
BSL 1.1 + grant D209, template de journal append-only.
(3) **LES PORTES DE DÉPÔT** : scan de secrets fail-closed (équivalent Python
gitleaks, contrôle négatif planté), autotest D105 sur clones temporaires à
phrases de test marquées, LA CRISTALLISATION 10 rebuilds bit-identiques
(timestamps normalisés, entrées triées) ; le dépôt Zenodo DEMEURE le geste du
développeur ; la dette kit nommée à la naissance au tableau de bord.

## Les gestes
1. Le plan gelé ; le générateur (git ls-files → l'arbre du kit, D130).
2. Le contenu M0-in-a-box assemblé (chaque pièce par construction).
3. Les portes (secrets, autotest D105, compatibilité, l'ancre jamais expédiée).
4. La cristallisation 10× + le MANIFESTE + la dette kit nommée.

## La vérification après modifications
10 archives reconstruites bit-identiques ; empreintes MANIFESTE confrontées
fichier par fichier ; contrôles négatifs VÉCUS (un secret planté attrapé, un
kit périmé refusé, un triplet incompatible refusé, une ancre de confiance du
projet expédiée par erreur attrapée) ; sceau 14/14 avant/après ; aucun coffre
réel ni phrase réelle touchés ; autotest vert sur clone frais ; entrée
append-only.

## Les refus
Jamais une maintenance manuelle de la liste ; jamais l'ancre expédiée ; jamais
un oracle pré-dérivé ; jamais le dépôt minté sans commande.
