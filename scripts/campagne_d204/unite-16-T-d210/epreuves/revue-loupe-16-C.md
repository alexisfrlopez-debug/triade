Revue la conformité AU CONTRAT, clause par clause (P1-P3, Q1-Q5, I1-I4, E1-E4) : cite la ligne à l'appui pour chaque clause, nomme les écarts éventuels, conclus par « Verdict : CONFORME » ou « Verdict : ÉCART ».
Rien d'autre.

**P1** : appelée par la procédure (loupe-09 Q3) sur WM_CHAR hors mode saisie — les SEIZE chiffres hexa écoutent, tout autre caractère est ignoré proprement.
Ligne : `if (c >= 0x30u && c <= 0x39u) { ... } else if (c >= 0x41u && c <= 0x46u) { ... } else { return 0; }`
Verdict : CONFORME

**P2** : la session est ouverte.
Ligne : `if (lire_u64(cadre, CADRE_POIGNEE) == ~(uint64_t)0) { ... return -4; }`
Verdict : CONFORME

**P3** : la zone JOURNAL du plan (4 112 o : 256 entrées de 16 o — u64 décalage · u8 octet · 7 réserve — et le nombre) + le nibble de la zone SAISIE.
Ligne : `static uint32_t nombre = lire_u32(journal, JOURNAL_NOMBRE);` (pour le nombre) et `static uint32_t SAISIE_NIBBLE = 8u;` (pour le nibble).
Verdict : CONFORME

**Q1** : LE PREMIER CHIFFRE : nibble actif, la valeur (0 à 15) posée — la cellule attend (rien n'est écrit : un demi-octet n'existe pas au disque ni au journal).
Ligne : `ecrire_u32(saisie, SAISIE_ACTIF, 1u); ecrire_u32(saisie, SAISIE_NIBBLE, valeur);`
Verdict : CONFORME

**Q2** : LE SECOND CHIFFRE : l'octet = (premier << 4) | second — écrit AU JOURNAL : l'entrée du décalage du curseur (l'entrée PAR DÉCALAGE : si le décalage est déjà au journal, l'octet REMPLACÉ, le nombre n'augmente pas) ; le journal PLEIN (256 distincts) → verdict -3 (la borne nommée : « journal plein — Ctrl+S pour sauver »).
Ligne : `if (i < nombre) { journal[16u * i + 8u] = (unsigned char)octet; } else if (nombre < EDITS_MAX) { ... ecrire_u32(journal, JOURNAL_NOMBRE, nombre + 1u); } else { ... return -3; }`
Verdict : CONFORME

**Q3** : ET À LA VUE : si la cellule est dans la fenêtre (curseur − vue < remplissage) : tampon[curseur − vue] = l'octet — l'octet visible IMMÉDIATEMENT (jamais une édition invisible).
Ligne : `cadre[CADRE_TAMPON + (uint32_t)(curseur - vue)] = (unsigned char)octet;`
Verdict : CONFORME

**Q4** : LA MARQUE : cadre.sale = 1 ET refus_quitter = 0 (la garde de loupe-18 ré-armée : après une NOUVELLE écriture, le premier Alt+F4 re-vient avertir) ; le curseur AVANCE (+1, clampé à taille − 1) — la cellule suivante attend.
Ligne : `ecrire_u32(cadre, CADRE_SALE, 1u); ecrire_u32(cadre, CADRE_REFUS_QUITTER, 0u); ... ecrire_u64(cadre, CADRE_CURSEUR, curseur);`
Verdict : CONFORME

**Q5** : rax = 0 ; VK_SUPPR pendant l'attente (Q1) → le nibble effacé (l'attente annulée proprement — le premier chiffre repart).
Ligne : `if (caractere == 0x08u) { if (lire_u32(saisie, SAISIE_ACTIF) != 0u) { ecrire_u32(saisie, SAISIE_ACTIF, 0u); ecrire_u32(saisie, SAISIE_NIBBLE, 0u); } return 0; }`
Verdict : CONFORME

**I1** : LE DISQUE INTACT : aucune écriture fichier ici (WriteFile vit chez loupe-17 SEUL — la liste IAT du plan le garantit : la contrebande d'écriture est un refus de build).
Ligne : Aucune écriture dans le paramètre `const unsigned char *disque`.
Verdict : CONFORME

**I2** : le journal est PAR DÉCALAGE (une entrée par octet — la seconde écriture remplace : la sauvegarde écrit chaque octet UNE fois, l'ordre interne du journal est celui de la saisie).
Ligne : `while (i < nombre) { if (lire_u64(journal + 16u * i, 0u) == curseur) { break; } ++i; }`
Verdict : CONFORME

**I3** : la cohérence de vue est tendue par loupe-02 Q2 (le recouvrement : l'octet édité survit au défilement) — ici la moitié locale : l'octet posé au tampon SI visible.
Ligne : `cadre[CADRE_TAMPON + (uint32_t)(curseur - vue)] = (unsigned char)octet;`
Verdict : CONFORME

**I4** : le curseur reste BORNÉ [0, taille−1] (l'invariant du cadre) ; AUCUNE entrée IAT propre (l'édition est pure état : le journal, le tampon, la marque) ; NOP, 0x90.
Ligne : `curseur = curseur + 1u; if (curseur >= taille) { curseur = (taille > 0u) ? taille - 1u : 0u; }`
Verdict : CONFORME

**E1** : sans session ouverte (P2) → verdict -4 SESSION, rax = -4.
Ligne : `if (lire_u64(cadre, CADRE_POIGNEE) == ~(uint64_t)0) { poser_message(saisie, "aucun fichier ouvert"); return -4; }`
Verdict : CONFORME

**E2** : la cellule hors fenêtre valide (curseur − vue ≥ remplissage : la cellule n'existe pas à la vue) → verdict -3 HORS-BORNES — l'écriture AU JOURNAL a quand même lieu ? NON : RIEN n'est écrit (le refus précède le journal — la cellule fantôme n'existe pas, l'oracle le constate).
Ligne : `if (curseur >= vue + (uint64_t)remplissage) { poser_message(saisie, "hors bornes"); return -3; }` (avant la manipulation du journal).
Verdict : CONFORME

**E3** : le journal PLEIN (256 octets DISTINCTS en attente) → verdict -3, la borne nommée à la barre (« journal plein — Ctrl+S »), RIEN perdu (l'octet refusé n'entre pas, l'état demeure).
Ligne : `else { poser_message(saisie, "journal plein - Ctrl+S"); return -3; }`
Verdict : CONFORME

**E4** : le caractère non hexa → IGNORÉ proprement (repli documenté : rax = 0, rien — les seize chiffres seuls écoutent).
Ligne : `else { return 0; }`
Verdict : CONFORME