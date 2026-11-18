V1_DIFF10k: saisie de 10000 séquences distinctes, frontière 256 atteinte, rejet attendu.
V1_REECR: ré-écriture d'une séquence existante avec décalage, modification attendue.
V1_FRON256: saisie de la 256e cellule, validation attendue.
V2_4D5A: saisie de '4d5a' octet par octet, écriture dans journal et tampon, marque posée.
V2_MARQUE: saisie après la marque, déclenchement de la garde, attente de la cellule suivante.
V2_GUARDE: saisie sous garde, validation et passage à la cellule suivante.
V3_NOSession: saisie sans session active, code rejet -4.
V3_CELLFant: écriture dans une cellule fantôme (même sale), code rejet -3.
V3_257eDIST: création d'un 257e nom distinct, code rejet -3.
V3_VIDE: saisie dans une cellule vide (pas de marque), rejet.
V4_NONHEXA: saisie d'un caractère non-hexadécimal, caractère ignoré.
V4_VK_SUPPR: pression sur VK_SUPPR, attente d'action (repli).
V5_ALT_F4: combinaison Alt+F4 pressée, tentative de falsification.
V5_GUARDE_NO: exécution d'Alt+F4 alors que la garde n'est pas ré-armée, échec.