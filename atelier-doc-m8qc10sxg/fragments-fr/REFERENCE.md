# RÉFÉRENCE — le protocole en une page (le miroir FR)
Trois couches indissociables : I (les spécifications signées), C (la
carte chiffrée), B (l'artefact verrouillé aux octets). Les priorités
lexicographiques : sécurité > performance > optimisation > coût en
tokens.

La notation : une instruction par ligne ; les trous typés (registre /
offset / cible LBL-CST) ; les IDs du dictionnaire seuls — CST-001..NNN
pour les constantes et les entrées IAT (l'IAT s'appelle : call
CST-004), LBL-001..NNN pour les étiquettes internes (MAJUSCULES, à la
ligne seule) ; la source étroite (movzx rax, ecx) ; un opérande
mémoire par instruction au plus.

Les juges : la chaîne d'expansion v2 au pointeur seul, les
validateurs v3, le round-trip (ce que tu écris est ce qui s'expand est
ce qui revient). Un mutant d'un octet est attrapé — ne jamais jouer
le juge.

Les budgets (les opérandes non arrondies au manifeste du kit) :
locate 627 / edit 674 / add 2200 ; le budget de
réparation est 3.

Les portes R1-R11 :
- R1 : jamais un binaire nu (tout B livré avec I et C)
- R2 : l'intention d'abord (toute modification commence par un diff sur I)
- R3 : balisage obligatoire (chaque bloc décrit dans C)
- R4 : patch à contrat stable (les appelants jamais invalidés)
- R5 : vérifie-puis-écrit (aucun commit sans oracle, vecteurs dorés, round-trip)
- R6 : cristallisation (dix vérifications rendent le bloc immuable)
- R7 : adresses stables (les points d'entrée ne bougent jamais)
- R8 : verrou croisé (empreintes et signature vérifiées avant chaque édition)
- R9 : carte signée obligatoire (la carte non signée refusée au départ)
- R10 : échec contrôlé intégré (checksums, signature de manifeste, anti-rollback, environnement — fail-closed, aucun chemin dégradé)
- R11 : optimisation mesurée (un hot path identifié par mesure, l'avant/après consigné, le contrat stable)

Les classes de refus : HORS-FORMAT, ID-INCONNU, EXPANSION-DIVERGENTE,
FORME-INVALIDE (la notation) ; HUNK-INCONNU, CONTEXTE-DIVERGENT,
ROUND-TRIP-DIVERGENT (l'édition) ; POINTEUR-INCONNU,
EMPREINTE-DIVERGENTE (le pointeur). Réparer la cause nommée seule.

Les 18 blocs du banc (les notations scellées du dépôt) :
loupe-01-ouvrir
loupe-02-lire
loupe-03-fermer
loupe-04-cadre
loupe-05-sha256
loupe-06-md5
loupe-07-cumul
loupe-08-ligne
loupe-09-ecran
loupe-10-peinture
loupe-11-defilement
loupe-12-aller
loupe-13-recherche
loupe-14-suivant
loupe-15-curseur
loupe-16-saisie
loupe-17-sauver
loupe-18-quitter

Les cérémonies : la genèse de clé air-gap, le sceau LOCAL, le journal
append-only (les corrections sont des errata, jamais des réécritures),
la garde de secrets au commit, le dépôt de release à la commande
humaine.

Les décisions citées en littéral (jamais traduites) : D81 (la garde
durable), D105 (la phrase de test marquée), D122 (l'envoi humain),
D130 (le kit par construction), D203 (la grille kappa), D207 (les
règles d'arrêt), D209 (le grant), D250 (l'arbitrage au développeur).
