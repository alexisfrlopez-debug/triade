=== LA REVUE ===

**Conformité au contrat :**

*   **P1** : Honorée. La vérification de la session (`cmp qword ptr [rbx + 528], -1`) est présente.
*   **P2** : Honorée. `rcx` et `rdx` sont sauvegardés dans `r15` et `r14`.
*   **P3** : Honorée. La vérification `add rax, rdx` / `cmp rax, qword ptr [rbx + 520]` est présente.
*   **P4** : Honorée. La vérification `test r13, r13` est présente.
*   **Q1** : Honorée. Le condensé généré par `tls13-04` est copié vers `r13` (`mov rdi, r13`).
*   **Q2** : Honorée. La composition est respectée : `tls13-01` (initialisation), `tls13-03` (absorption dans la boucle), puis `tls13-04` (finalisation). La mention "tls13-02 vit à l'intérieur de tls13-03" est une description de l'implémentation et non une exigence fonctionnelle ; l'appel à `tls13-03` respecte l'héritage.
*   **Q3** : Honorée. Le cas `test r14, r14` saute vers `.vide`, où le vecteur FIPS est écrit.
*   **Q4** : Honorée. En cas de succès, `xor rax, rax` est exécuté.
*   **I1** : Honorée. Le code appelle `tls13-01`, `tls13-03`, et `tls13-04` en adresses fixes (`call 0xc000`, `call 0xc240`, `call 0xc300`), respectant ainsi l'héritage PAR LA CARTE.
*   **I2** : Honorée. Aucune constante ou structure SHA n'est redéclarée dans ce bloc ; tout est délégué aux blocs hérités.
*   **I3** : Honorée. La lecture se fait via `ReadFile` dans un tampon (`lea rdx, [rip + 0xbb06]`), et non via un tampon de vue.
*   **I4** : Honorée. `SetFilePointerEx` est appelé avant chaque `ReadFile` dans la boucle.
*   **I5** : Honorée. L'IAT est déclarée (`IAT_SetFilePointerEx`, etc.). Les registres non volatils sont sauvegardés et restaurés. Les `ret` à la fin se comportent comme des NOP.

**Écarts nommés :**

*   **Aucun.**

**Verdict : CONFORME**