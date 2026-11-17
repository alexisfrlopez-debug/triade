### Revue de conformité AU CONTRAT, clause par clause

**P1 rcx = la source, au moins rdx octets lisibles**
*   **Instruction** : `test rcx, rcx` et `movzx eax, byte ptr [rcx + r9]`.
*   **Écart** : Aucun. Le code vérifie que `rcx` n'est pas nul avant de l'utiliser comme pointeur de lecture. La lecture se fait avec `byte ptr [rcx + r9]` où `r9` est un compteur de 0 à 15, garantissant que l'accès reste dans les limites de la longueur `rdx` (via le `cmp r9d, edx` précédent la lecture).

**P2 rdx = la longueur valide, 1 à 16**
*   **Instruction** : `cmp rdx, 1`, `jl .erreur_entree`, `cmp rdx, 16`, `jg .erreur_entree`.
*   **Écart** : Aucun. Les bornes 1 et 16 sont explicitement vérifiées. Si la longueur est en dehors de cet intervalle, le saut vers `.erreur_entree` est effectué.

**P3 r8 = la sortie, 77 o (LIGNE_TAILLE) accessibles en écriture**
*   **Instruction** : `test r8, r8` et la séquence d'écritures sur `[r8]` qui s'étend sur 77 octets.
*   **Écart** : Aucun. Le code vérifie que `r8` n'est pas nul. L'ensemble des écritures, calculées pour être exactement 77 octets (8 + 2 + 16*2 + 2 + 16 + 1), sont effectuées à partir de `r8`.

**P4 r9 = le décalage de la ligne (multiple de 16, ≤ 0x7FFFFFFF)**
*   **Instruction** : `mov r10, r9`.
*   **Écart** : Aucun. Le contrat stipule que la valeur est garantie par `BORNE_TAILLE`. Le code l'utilise telle quelle pour l'écriture hexadécimale.

**Q1 la sortie = « SSSSSSSS HH HH HH HH HH HH HH HH HH HH HH HH HH HH HH HH HH MMMMMMMMMMMMMMMMM » + NUL : EXACTEMENT 77 o écrits**
*   **Instruction** : La séquence complète des écritures depuis le premier `mov [r8], al` jusqu'au `mov byte ptr [r8], 0`.
*   **Écart** : Aucun. La structure de la boucle et les sauts conditionnels garantissent la production d'une ligne de format exact, incluant les 8 chiffres hex, les espaces (simples et doubles), les 16 caractères du miroir et le NUL final, pour un total de 77 octets.

**Q2 le miroir : l'octet 0x20 à 0x7E → le caractère ; tout autre → « . »**
*   **Instruction** : `cmp al, 0x20`, `jl .write_dot`, `cmp al, 0x7E`, `jg .write_dot`, `mov [r8], al`.
*   **Écart** : Aucun. La logique de branchement identifie correctement les caractères non imprimables et les remplace par un point (`0x2E`).

**Q3 la ligne INCOMPLÈTE (rdx < 16) : les groupes au-delà de rdx = deux espaces, le miroir au-delà = un espace**
*   **Instruction** : Les boucles `.writ_hex_loop` et `.writ_ascii_loop` sont précédées de `cmp r9d, edx` qui mènent à des chemins d'écriture d'espace (`.write_group_space` et `.write_ascii_space`).
*   **Écart** : Aucun. Pour les indices supérieurs ou égaux à `rdx`, les groupes hexadécimaux sont bien remplacés par deux espaces et les caractères du miroir par un espace, préservant l'alignement.

**Q4 rax = 0**
*   **Instruction** : `xor eax, eax` avant le `ret` normal.
*   **Écart** : Aucun. En cas de succès, `rax` est explicitement mis à zéro.

**I1 AUCUNE entrée IAT, AUCUN site syscall, AUCUN état détenu**
*   **Instruction** : `lea r11, [rip - 0x29b4]`.
*   **Écart** : Aucun. L'accès à la table de conversion se fait via `RIP`, une position indépendante de l'adresse de chargement (pas d'IAT). Aucun appel système n'est présent. Le code est sans état, fonctionnel.

**I2 AUCUN débordement : la composition écrit EXACTEMENT les 77 o de P3**
*   **Instruction** : L'ensemble des instructions `mov`/`mov word ptr`/`mov byte ptr` agissant sur `[r8]`.
*   **Écart** : Aucun. Le compteur `r8` est incrémenté d'un nombre fixe et prédéterminé d'octets à chaque étape, garantissant que l'écriture s'arrête exactement après le 77ème octet.

**I3 la source est LUE SEULE (jamais modifiée)**
*   **Instruction** : `movzx eax, byte ptr [rcx + r9]`.
*   **Écart** : Aucun. La mémoire pointée par `rcx` est uniquement lue, jamais modifiée.

**I4 les chiffres hexa : la table « 0123456789ABCDEF »... aucun registre non volatil détruit**
*   **Instruction** : `lea r11, [rip - 0x29b4]` et les accès suivants avec `[r11 + rax]`.
*   **Écart** : Aucun. La table est bien celle des majuscules hexadécimales. Seuls les registres volatils (`rax`, `rcx`, `rdx`, `r8`, `r9`, `r10`, `r11`) sont utilisés, conformément au plan VOLATIL.

**E1 : longueur 0 (P2) → verdict -5**
*   **Instruction** : `cmp rdx, 1`, `jl .erreur_entree`.
*   **Écart** : Aucun. Si `rdx` est 0, la condition `jl` est vraie et le saut vers `.erreur_entree` est effectué.

**E2 : longueur > 16 (P2) → verdict -5**
*   **Instruction** : `cmp rdx, 16`, `jg .erreur_entree`.
*   **Écart** : Aucun. Si `rdx` est supérieur à 16, la condition `jg` est vraie et le saut vers `.erreur_entree` est effectué.

**E3 : source ou sortie nulle (P1/P3) → verdict -5**
*   **Instruction** : `test rcx, rcx`, `jz .erreur_entree` et `test r8, r8`, `jz .erreur_entree`.
*   **Écart** : Aucun. Si `rcx` ou `r8` est nul, un des tests échoue et le saut vers `.erreur_entree` est effectué.

**Verdict : CONFORME**