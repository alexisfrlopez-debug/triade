=== LA REVUE ===

**Conformité au contrat :**

*   **P1** : Honorée. Le test `test rdi, rdi` et le saut vers `.erreur_session` courent le risque d'une session fermée.
*   **P2** : Honorée. `rcx` et `rdx` sont sauvegardés dans `r15` et `r14`.
*   **P3** : **ÉCART**. La vérification de la condition `offset + longueur ≤ taille du fichier` est absente. Le code commenté suppose un registre externe non défini par le contrat.
*   **P4** : Honorée. Le test `test r13, r13` et le saut vers `.erreur_entree` courent le risque d'une sortie inutilisable.
*   **Q1** : Honorée. Le condensé généré par tls13-04 est copié dans la zone pointée par `r8` (dans `r13`).
*   **Q2** : Honorée. La composition `tls13-01 → boucle tls13-03 → tls13-04` est respectée. L'héritage de tls13-02 est déclaré embarqué dans tls13-03.
*   **Q3** : Honorée. Le cas `longueur = 0` est traité par la section `.vide`, qui écrit le vecteur FIPS.
*   **Q4** : Honorée. `rax` est mis à 0 en cas de succès.
*   **I1** : Honorée. Les blocs tls13-01, tls13-03, tls13-04 sont appelés par étiquette, respectuant le principe d'héritage PAR LA CARTE.
*   **I2** : Honorée. Aucune constante ou donnée de contexte SHA n'est redéclarée ; tout est géré par tls13-01.
*   **I3** : Honorée. La lecture s'effectue bien via `TAMPON_CUMUL` (la zone `rsp + 112`).
*   **I4** : Honorée. `SetFilePointerEx` est appelé avant chaque `ReadFile` dans la boucle.
*   **I5** : Honorée. L'IAT est déclarée (`IAT_SetFilePointerEx`, etc.). Les registres non volatils sont sauvegardés et restaurés. Le retour `ret` est un NOP implicite.

**Écarts nommés :**

*   **ÉCART P3** : La précondition P3 (`décalage + longueur ≤ taille du fichier`) n'est pas vérifiée. Le code ne contient pas la logique de ce test, rendant le comportement indéfini pour les gammes hors bornes non interceptées par E2.

**Verdict :**

**ÉCART**