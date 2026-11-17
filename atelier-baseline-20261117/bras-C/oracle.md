Je suis prêt. En tant que juge du protocole TRIADE, je ne juge pas le code, mais son adhésion parfaite au Contrat. L'Oracle est la dérivée directe et exclusive du texte que vous avez fourni. Il n'y a pas de place à l'interprétation, seulement à la vérification.

Voici l'Oracle, tel que dérivé du Contrat.

---

### === L'ORACLE (Jugement selon TRIADE) ===

Le jugement portera sur l'exactitude stricte entre l'exécution de la pièce et les attendus suivants. Aucun autre critère n'est recevable.

#### **Les Attendus en Termes de Contrat (La Sémantique)**

**A. Cas Nominaux (Le Succès attendu)**

1.  **Q1 : Le Condensé Correct**
    *   **Attendu :** Pour toute gamme valide, les 32 octets écrits en mémoire à l'adresse `r8` **doivent être la sémantique exacte du condensé SHA-256 FIPS 180-4** de la sous-chaîne de fichier `F[décalage .. décalage + longueur]`.
    *   **Jugement :** La comparaison se fait octet par octet contre une référence externe et incontestable (ex: `hashlib.sha256` en Python, ou une implémentation de référence C). Le résultat doit être une égalité parfaite. La pièce ne produit pas d'octets ; elle réalise la sémantique du contrat.

2.  **Q2 : La Composition Héritée Exacte**
    *   **Attendu :** Le processus de calcul **doit impérativement suivre la composition fermée** :
        1.  Une seule exécution de `tls13-01` (l'initialisation).
        2.  Une boucle sur chaque fenêtre de 64 Kio :
            a. Repositionnement du pointeur fichier via `SetFilePointerEx`.
            b. Lecture des octets via `ReadFile` dans `TAMPON_CUMUL`.
            c. Une exécution de `tls13-03` (l'absorption) pour la fenêtre lue.
        3.  Une seule exécution de `tls13-04` (la finalisation) après la boucle.
    *   **Jugement :** L'héritage (`tls13-02`) est considéré comme intégré à `tls13-03` et ne nécessite pas d'appel direct. L'ordre et le nombre d'appels aux blocs hérités sont contractuels. Toute déviation (ex: appeler `tls13-01` à chaque fenêtre, omettre `tls13-04`) constitue un échec de ce point de contrat.

3.  **Q3 : Le Cas de la Gamme Vide**
    *   **Attendu :** Si `rdx = 0`, le condensé produit **doit être le vecteur officiel FIPS 180-4 pour la chaîne vide** : `e3b0c442 98fc1c14 9afbf4c8 996fb924 27ae41e4 649b934c  a495991b 7852b855`.
    *   **Jugement :** Une comparaison octet par octet avec ce vecteur exact. Ce cas est un test de l'initialisation correcte du contexte hérité.

4.  **Q4 : Le Code de Retour Succès**
    *   **Attendu :** En cas de succès, le registre `rax` **doit contenir la valeur 0**.
    *   **Jugement :** La vérification se fait sur la valeur de `rax` à la fin de l'exécution de la pièce.

**B. Cas de Bord (Le Succès attendu)**

*   **V1 : Différentiel**
    *   **Attendu :** L'exécution de la pièce sur un ensemble de gammes variées (y compris la totalité d'un grand fichier comme `proxy.exe`) **doit produire exactement les mêmes condensés SHA-256 qu'une implémentation de référence standard**.
    *   **Jugement :** Ce cas de test couvre Q1, Q2 et Q4 de manière exhaustive. Il valide que la composition héritée, même avec les fenêtres glissantes, aboutit au résultat sémantique correct. Le verdict est "succès" si et seulement si toutes les comparaisons sont identiques.

**C. Cas de Rejet (L'Échec attendu)**

1.  **E1 : Absence de Session**
    *   **Scénario :** La session est fermée (la poignée est `INVALIDE`).
    *   **Attendu :** L'exécution **doit s'arrêter immédiatement**.
    *   **Verdict :** Le registre `rax` **doit contenir la valeur -4**.
    *   **Jugement :** Le code de retour est le seul critère. Aucun condensé ne doit être écrit.

2.  **E2 : Gamme Hors Bornes**
    *   **Scénario :** `rcx + rdx > taille du fichier`.
    *   **Attendu :** L'exécution **doit s'arrêter immédiatement**.
    *   **Verdict :** Le registre `rax` **doit contenir la valeur -3**.
    *   **Jugement :** Le code de retour est le seul critère. Aucun condensé ne doit être écrit.

3.  **E3 : Sortie Inutilisable**
    *   **Scénario :** L'adresse en `r8` est nulle ou pointe vers une zone non accessible en écriture.
    *   **Attendu :** L'exécution **doit s'arrêter immédiatement**.
    *   **Verdict :** Le registre `rax` **doit contenir la valeur -5**.
    *   **Jugement :** Le code de retour est le seul critère. Aucun condensé ne doit être écrit.

4.  **E4 : Erreur Système**
    *   **Scénario :** Un appel à `ReadFile` ou `SetFilePointerEx` échoue (par exemple, le fichier est verrouillé ou disparaît pendant le calcul).
    *   **Attendu :** L'exécution **doit s'arrêter immédiatement**.
    *   **Verdict :** Le registre `rax` **doit contenir la valeur -6**. Le contenu de la zone mémoire pointée par `r8` **doit rester inchangé** par rapport à son état avant l'appel de la pièce.
    *   **Jugement :** La vérification porte sur `rax` et sur l'intégrité de la zone de sortie. Le calcul ne doit pas publier de condensé partiel ou corrompu.

**D. Cas de Falsification (Le Test de Robustesse)**

*   **V5 : Mutation de TAMPON_CUMUL**
    *   **Scénario :** Un octet dans `TAMPON_CUMUL` est artificiellement modifié entre la lecture d'une fenêtre et l'appel à `tls13-03`.
    *   **Attendu :** Le condensé final **doit impérativement diverger** de la valeur attendue par `hashlib.sha256`.
    *   **Jugement :** Ce test valide que la pièce n'est pas vulnérable à des attaques par canaux auxiliaires ou à des données intermédiaires non protégées. Si le condensé est correct malgré la mutation, la pièce est jugée non robuste.

---

### **Synthèse du Jugement**

La pièce sera jugée **"VALIDE"** si et seulement si, pour chaque vecteur de test (V1 à V5), le résultat observé correspond parfaitement à l'attendu de l'Oracle.

*   **Un seul échec sur l'un des attendu (Q1, Q2, Q3, Q4, E1, E2, E3, E4) entraîne un rejet de la pièce.**
*   La falsification (V5) est un test positif ; son échec (le condensé reste correct) est un rejet.

Le jugement est binaire : la pièce est soit conforme au Contrat, soit elle ne l'est pas. L'Oracle est la loi.