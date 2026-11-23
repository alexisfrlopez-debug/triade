# DÉPANNAGE — les refus nommés et ce qu'ils veulent dire (le miroir FR)
Le protocole n'échoue jamais en silence : chaque porte refuse à un
NOM. Trouve le nom, répare la cause nommée seule.

Les notations refusées (la chaîne de juges v2 + les validateurs v3) :
- HORS-FORMAT — une ligne n'est pas une forme admise (une instruction
  à préfixe de chaîne REP, un db inline, une étiquette minuscule
  accolée à une instruction, un littéral tronqué). La réparation : le
  motif canonique — une instruction par ligne, les trous typés.
- ID-INCONNU — un ID absent du dictionnaire du bloc. La réparation :
  les IDs énumérés seuls (CST-001..NNN, LBL-001..NNN), jamais un
  symbole en clair.
- EXPANSION-DIVERGENTE — la ligne expandée a divergé (un round-trip
  en écart, une IAT jointe par une étiquette, un ID en opérande non
  expandable). La réparation : le trou typé (mov reg, CST-001 pour
  une constante ; call CST-004 pour l'IAT ; jcc LBL-001 pour un saut
  interne).
- FORME-INVALIDE — la forme émise viole le gabarit scellé.
Les quatre refus du pointeur au LOCATE (nul, hors zone, la taille,
l'alignement) sont nommés à la porte.

Le budget (3 réparations) épuisé : la tâche finit refusée — le
verdict est une pièce aussi précieuse qu'un vert ; jamais une tâche
re-tirée, jamais un budget élargi en silence.
Le linter doc refuse : une divergence numérique entre les miroirs EN
et FR, un identifiant traduit — les portes de parité.
Le scan de secrets refuse : un secret, ou la phrase de test marquée
(D105) — les copies de laboratoire portent la marque visible ; le
coffre réel n'est jamais touché au laboratoire.
La porte du kit refuse : un triplet checkpoint / kit / juges
incompatible — fail-closed, nommé.
L'agrégateur refuse : un run manquant (exit 2, jamais un verdict
partiel) ; moins de 10 strates complètes se lit NON TESTÉE (D207).
La porte kappa exige les DEUX conditions ensemble (D203) : 0,61
atteint SUR au moins 50 items double-codés.
R10 refuse au lancement (checksums, signature de manifeste,
anti-rollback, environnement) — aucun chemin dégradé n'existe.
Sans response_format à l'endpoint : la grammaire vit au prompt et les
validateurs jugent — jamais un juge affaibli (la dégradation
gracieuse).
