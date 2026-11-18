### NOTES D'AUTEUR

#### **Exigences et signature**
*   **Signature :** `rcx` (fenêtre), `rdx` (taille fenêtre), `r8` (motif), `r9` (taille motif), `[rsp+0x28]` (départ).
*   **Post-trait (Q) :**
    *   `rax` = position absolue de la **première** occurrence, ou `-1` si absente.
    *   Absence si : `départ >= rdx`, `taille motif > rdx - départ`, ou motif non trouvé.
    *   Si `rax >= 0`, alors `memcmp(fenêtre[rax..], motif)` est vrai et aucune occurrence avant `rax`.
*   **Pré-trait (P) :**
    *   `taille motif` dans `[1, 32]`.
    *   `départ` dans `[0, rdx]`.
*   **Échec (E) :**
    *   `taille motif = 0` → `-5`.
    *   `taille motif > 32` → `-5`.
    *   `départ > rdx` → `-5`.

#### **Pièges nommés**
*   **R7 :** BOUCLE DE COMPARAISON INTERDITE. L'appel à `memcmp` est **obligatoire**.
*   **Falsification (V4) :** Retourner la **seconde** occurrence au lieu de la première invalide la preuve.
*   **Complexité trompeuse :** L'algorithme est `O(n·m)`. La contrainte `m ≤ 32` rend cette complexité acceptable, mais il ne faut pas chercher à l'optimiser en sacrifiant la preuve (ex: table de hachage).
*   **Décalage de bord :** Le cas où le motif est trouvé exactement à la fin de la fenêtre (`rdx - taille motif`) doit être géré.

#### **Invariants à tenir**
*   **I1 :** AUCUN état. Seuls les registres en entrée sont utilisés. Pas de pile allouée, pas de données cachées.
*   **I2 :** Pureté de la comparaison. L'unique appel externe est `memcmp`. Aucune autre fonction de la libc.
*   **I3 :** Immuabilité. Les tampons `rcx` (fenêtre) et `r8` (motif) ne sont jamais modifiés.
*   **I4 :** Registres. Les registres non volatils (`rbx`, `rbp`, `r12`-`r15`) ne sont pas modifiés. Leur sauvegarde est interdite.

#### **Cas d'échec**
*   **E1 : Motif vide (`r9 = 0`).** Retourner `-5` (ENTRÉE INVALIDE).
*   **E2 : Motif trop long (`r9 > 32`).** Retourner `-5` (ENTRÉE INVALIDE).
*   **E3 : Départ hors limites (`[rsp+0x28] > rdx`).** Retourner `-5` (ENTRÉE INVALIDE).