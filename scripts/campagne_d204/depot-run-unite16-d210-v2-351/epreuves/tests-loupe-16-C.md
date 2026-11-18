=== SUITE DE TESTS — loupe-16 saisie (le miroir C, l'unité 04 D210 × bras C) ===

**Cas Nominaux (V1, V2)**

*   **Test N1** : Le premier chiffre pose l'attente.
    *   `cadre` : session ouverte (poignée 0x1000, taille 63, vue 0, curseur 0x22, remplissage 63)
    *   `caractère` : 0x34 (« 4 »)
    *   `Attendu` : retour 0 ; actif = 1, nibble = 4 ; RIEN au journal, RIEN au tampon.

*   **Test N2** : Le second chiffre engage — l'octet au journal ET au tampon.
    *   `caractère` : 0x34 puis 0x64 (« 4d »)
    *   `Attendu` : retour 0 ; l'octet 0x4D AU JOURNAL [(0x22, 0x4D)] ; tampon[0x22] = 0x4D ; sale = 1 ; refus_quitter = 0 ; curseur = 0x23.

*   **Test N3** : La réécriture du même décalage REMPLACE.
    *   « 4d » puis « 5a » au même curseur (curseur reposé à 0x22)
    *   `Attendu` : le journal [(0x22, 0x5A)] seul — le compte n'augmente pas (I2 : l'entrée par décalage).

*   **Test N4** : Le scénario « 4d5a » complet.
    *   « 4 », « d », « 5 », « a » au curseur 0x22
    *   `Attendu` : le journal [(0x22, 0x4D), (0x23, 0x5A)] ; le tampon porte les DEUX octets ; curseur 0x24 ; la marque, la garde.

*   **Test N5** : LA VUE SUIT l'avance (le renvoi de loupe-15 Q3).
    *   disque 8192 o, vue 0, curseur 0x17E, lignes 27 ; « 5 », « 0 »
    *   `Attendu` : le curseur 384 sort de la vitrine [0, 384) → la nouvelle vue 208 (aligne16_inf(384 − 176)) ; le tampon re-né du disque + le recouvrement ; remplissage 384.

*   **Test N6** : Le curseur demeure dans la vitrine.
    *   curseur 382 → l'écriture → curseur 383
    *   `Attendu` : la vue IMMOBILE (aucune relecture), l'octet visible.

**Cas de Bords (V1)**

*   **Test B1** : Les minuscules portées aux MAJUSCULES.
    *   « a » puis « b » (0x61, 0x62)
    *   `Attendu` : l'octet 0xAB — les SEIZE chiffres écoutent, la même valeur que « AB ».

*   **Test B2** : La frontière du journal — le 257e distinct.
    *   256 entrées posées (0x40..0x13F), le 257e refusé
    *   `Attendu` : -3, la barre « journal plein - Ctrl+S », les 256 INTACTS (RIEN perdu).

*   **Test B3** : Le curseur au bord — le pas clampé.
    *   curseur = taille − 1, une écriture
    *   `Attendu` : le curseur DEMEURE à taille − 1 (I4 : borné).

**Cas de Rejets (V3)**

*   **Test R1** : Sans session ouverte.
    *   `cadre` : poignée INVALIDE (~0)
    *   `Attendu` : retour -4, la barre « aucun fichier ouvert ».

*   **Test R2** : La cellule fantôme.
    *   curseur = 389, vue = 0, remplissage = 384
    *   `Attendu` : -3, la barre « hors bornes », RIEN au journal (le refus PRÉCÈDE), l'attente CONSOMMÉE.

*   **Test R3** : La cellule fantôme MARCHE SALE.
    *   le même état, sale = 1 posé
    *   `Attendu` : -3 QUAND MÊME — le remplissage lu u32 SEUL (jamais le qword : la marque vit à +556).

*   **Test R4** : Le fichier vide.
    *   taille 0 (aucune cellule n'existe)
    *   `Attendu` : -3.

**Cas de Repli (V4)**

*   **Test F1** : Le non-hexa ignoré.
    *   « z », « ! », l'espace
    *   `Attendu` : retour 0, rien bougé (E4 — le repli documenté).

*   **Test F2** : VK_SUPPR à l'attente.
    *   « 4 » puis 0x08
    *   `Attendu` : le nibble EFFACÉ (actif = 0 — le premier chiffre repart).

*   **Test F3** : VK_SUPPR hors attente.
    *   0x08 sans attente
    *   `Attendu` : ignoré proprement (retour 0, rien).

**Falsification (V5)**

*   **Test X1** : La garde non ré-armée.
    *   le source muté (la ligne refus_quitter = 0 retirée) : l'écriture puis Alt+F4
    *   `Attendu` : le scénario de sortie ÉCHOUE au mutant (la garde demeurée — jamais le refus -5) ; la pièce juste re-jouée VERTE. La falsification DEMANDÉE par le contrat, la preuve traverse les blocs.
