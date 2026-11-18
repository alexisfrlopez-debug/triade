**NOTES D'AUTEUR**

1.  **Contrat :** Deux saisies hexa forment un octet. Le premier chiffre est stocké temporairement (`nibble`), le second valide l'octet. L'écriture se fait par décalage (remplacement) dans le journal et dans le tampon de vue si visible.
2.  **États critiques :** Vérifier l'existence d'une session (`P2`), la validité de la cellule active (`curseur - vue < remplissage`), et la capacité du journal (`nombre < 256`). Un échec sur l'un de ces points retourne `-3` ou `-4`.
3.  **Effets secondaires :** La marque `sale` est levée et `refus_quitter` est désactivé à chaque écriture réussie. Le curseur avance, ce qui peut déclencher un recalcul de la vue (`LOUPE02`).
4.  **Périmètre d'écriture :** Le disque n'est jamais touché ; les données sont en RAM. L'opération est réversible par `loupe-17`.
5.  **Registres :** `rcx` (HWND), `r8` (caractère) en entrée. `rax` pour le code de retour. `rbx` pointeur sur le `CADRE`. `rdx`, `rsi`, `rdi` pour manipuler les adresses du plan (journal, tampon). `r10`/`r11` pour les calculs de curseur/vue.
6.  **Dangers :**
    *   **État :** Gérer la session et les bornes du curseur est crucial pour éviter des accès mémoire invalides.
    *   **Journal :** La logique de décalage pour remplacer une entrée existante est un point délicat.
    *   **Vue :** L'avance du curseur peut invalider la zone visible, nécessitant un appel coûteux à `LOUPE02` et un `InvalidateRect`.
    *   **Garde :** Le désarmement de `refus_quitter` (`Q4`) est une action de garde, à faire en dernier pour valider la saisie.
7.  **Ordre d'écriture :** 1. Valider la session. 2. Extraire le caractère hexa. 3. Gérer le `VK_SUPPR`. 4. Calculer l'octet. 5. Vérifier la position du curseur et la place dans le journal. 6. Écrire dans le journal et le tampon. 7. Mettre à jour l'état (`sale`, `refus_quitter`, curseur). 8. Gérer le recalcul de la vue si besoin. 9. Retourner le code.