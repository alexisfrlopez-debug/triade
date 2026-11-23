# SÉCURITÉ — le modèle en une page (le miroir FR)
Les secrets : jamais committés — la garde pre-commit combine les
empreintes sha256 des secrets connus, l'entropie de Shannon (3,8
bits/car sur les assignations de 28 caractères ou plus) et les motifs
de classe (ghp_ / GOCSPX- / PEM / refresh). La porte de scrub est
fail-closed au contrôle négatif vécu : un secret planté DOIT être
attrapé.

Les ancres : AUCUNE ancre de confiance du projet n'est expédiée avec
le kit — ni la clé publique du projet, ni les signatures de
référence. L'adopteur court sa propre genèse de clé air-gap ; le
sceau est LOCAL.

Le coffre réel n'est jamais touché au laboratoire (D105) : les copies
de laboratoire portent une phrase de test marquée visible ; un
rapport qui en porte une est REFUSÉ à la porte.

La discipline d'accès : le pointeur seul (jamais un chemin en clair) ;
les quatre refus nommés du pointeur (nul, hors zone, la taille,
l'alignement) ; une instruction par ligne ; un opérande mémoire par
instruction au plus.

Les rapports adopteurs : anonymisés mécaniquement (chemins,
usernames), le scan de secrets à la porte, le schéma gelé par sha256
AVANT tout rapport ; le commentary (500 tokens au plus) est marqué
NON VÉRIFIÉ ; l'envoi est un geste humain (D122) — jamais automatique,
l'outil est offline.

Le double usage : les binaires intercepteurs et le matériau dual-use
sont exclus du sous-ensemble permissif ; les tâches synthétiques
Apache-2.0/CC-BY demeurent séparées du corpus BSL à chaque split.

La licence : BSL 1.1 au grant D209 ; les digests publics sous
CC-BY-4.0 (les contributeurs acknowledged opt-in).

Offline par construction : aucune dépendance réseau au build (R10) ;
l'outillage court en air-gap.
