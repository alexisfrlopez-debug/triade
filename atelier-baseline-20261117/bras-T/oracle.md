Juge, je suis prêt. Le bloc de machine n'est pas encore présent, mais le Contrat est ma loi. L'Oracle est dérivé. Voici le jugement que je porterai, basé exclusivement sur la pièce contractuelle que vous m'avez fournie.

---

### **JUGEMENT DU BLOC DE CODE MACHINE (PROTOCOLE TRIADE)**

**Dossier :** loupe-05 · sha256 d'une gamme : l'héritage tls13 PAR LA CARTE
**Révision :** 1
**Oracle :** Dérivé exclusivement du Contrat fourni.

---

### **1. L'ORACLE : Les Attendus en Termes de Contrat**

Le jugement portera sur la conformité de la future pièce de code machine aux exigences suivantes, dérivées du Contrat. Aucune considération sur l'implémentation source, les performances, ou des métriques non contractuelles n'entrera en ligne de compte.

#### **A. Les Vecteurs Attendus (Preuves Exigées)**

Le bloc de code devra passer avec succès les tests définis par les vecteurs suivants. Chaque vecteur est un contrat en soi.

*   **V1 : Le Test Différentiel (Validation de la Sémantique Q1, Q2, Q4)**
    *   **Attendu :** Pour 1000 gammes aléatoires du fichier `proxy.exe` scellé (incluant la gamme entière), le condensat produit (`r8`) doit être **octet par octet identique** au condensat produit par une référence de confiance (ex: `hashlib.sha256` en Python, ou un équivalent cryptographique standard).
    *   **Jugement :** La réussite de ce test est la preuve fondamentale que la composition héritée (tls13-01 -> tls13-03 -> tls13-04) est correctement exécutée et que la sémantique FIPS 180-4 est respectée. **Échec = rejet immédiat.**

*   **V2 : Le Test Doré (Validation du Cas Nominal Q3)**
    *   **Attendu :**
        1.  Pour une gamme vide (`longueur = 0`), le condensat produit dans `r8` doit être le vecteur FIPS officiel : `e3b0c442 98fc1c14 9afbf4c8 996fb924 27ae41e4 649b934c a495991b 7852b855`.
        2.  Pour une gamme contenant les octets ASCII `0x61, 0x62, 0x63` ("abc"), le condensat produit doit être le vecteur FIPS officiel : `ba7816bf 8f01cfea 414140de 5dae2223 b00361a3 96177a9c b410ff61 f20015ad`.
    *   **Jugement :** Ce test valide le comportement contractuel pour les cas limites et de référence définis par le standard. Il confirme que l'héritage gère correctement l'initialisation et la finalisation. **Échec = rejet immédiat.**

*   **V3 : Le Test de Rejet (Validation des Échecs E1, E2, E3)**
    *   **Attendu :**
        1.  **Cas E1 (Session invalide) :** Si la session est `INVALIDE`, le code doit retourner `rax = -4` et le verdict est `-4 SESSION`. La sortie `r8` peut être indéfinie (le contrat ne la spécifie pas dans ce cas d'erreur).
        2.  **Cas E2 (Hors bornes) :** Si `décalage + longueur > taille du fichier`, le code doit retourner `rax = -3` et le verdict est `-3 HORS-BORNES`.
        3.  **Cas E3 (Sortie inutilisable) :** Si `r8` est un pointeur nul, le code doit retourner `rax = -5` et le verdict est `-5 ENTRÉE`.
    *   **Jugement :** La robustesse du contrat repose sur la gestion correcte de ses préconditions. Toute déviation de ces verdicts ou de ces codes de retour est un **rejet immédiat.**

*   **V4 : Le Test de Rejet Système (Validation de l'Échec E4)**
    *   **Attendu :** Lors d'un appel système (`SetFilePointerEx` ou `ReadFile`) en échec, le code doit :
        1.  Arrêter le calcul de condensation.
        2.  Ne pas écrire dans la sortie `r8` (le contenu de `r8` doit être identique à son état *avant* l'appel échoué).
        3.  Retourner `rax = -6`.
        4.  Le verdict est `-6 SYSTÈME`.
    *   **Jugement :** Ce test est crucial. Il valide l'invariant de "calcul pur" : le système ne publie jamais un condensat partiel ou potentiellement corrompu. **Échec (ex: écriture d'un condensat partiel) = rejet immédiat.**

*   **V5 : Le Test de Falsification (Validation de l'Invariance I3)**
    *   **Attendu :** Ce test est un test négatif. On injecte volontairement une modification (mutation d'un octet) dans `TAMPON_CUMUL` *entre* deux lectures de fenêtres.
    *   **Jugement :** Le condensat final produit *doit* diverger du condensat attendu (celui produit par `hashlib.sha256`). Si les condensats sont identiques, cela signifie que le tampon n'est pas utilisé comme un espace de travail isolé, ou que la lecture est corromue. **Échec (les condensats restent identiques) = rejet immédiat.**

#### **B. Les Invariants Attendus (Règles de Conception Impératives)**

Le code machine doit respecter des invariants de structure et de comportement, sous peine de rejet.

*   **I1 : L'Héritage PAR LA CARTE (R7)**
    *   **Attendu :** Les octets machine des blocs `tls13-01`, `tls13-02`, `tls13-03`, `tls13-04` utilisés dans le code final *doivent être* une copie octet-à-octet de leur version scellée (R7). Toute modification, optimisation, ou recompilation qui altère ces octets est une **violation contractuelle et un rejet immédiat.** L'oracle du build vérifiera cela.

*   **I2 : La Source Unique du SHA (T5)**
    *   **Attendu :** Aucune constante de tableau (ex: les 64 constantes 'K'), aucune structure de contexte (112 octets), aucune implémentation des opérations SHA-256 ne peut être présente ailleurs dans le domaine que dans le bloc `tls13-01`. La redéclaration de `H0` ou du bloc 64 est une **violation et un rejet immédiat.**

*   **I3 : L'Invariance de la Vue (Intégrité du Tampon)**
    *   **Attendu :** La lecture du fichier *doit* se faire exclusivement via `TAMPON_CUMUL`. Le pointeur de fichier du cadre ne doit pas être utilisé pour une lecture directe qui contournerait le tampon. Le test V5 est la preuve de cet invariant.

*   **I4 : Le Repositionnement Systématique**
    *   **Attendu :** Avant *chaque* appel `ReadFile`, un appel `SetFilePointerEx` explicite doit être effectué pour positionner le pointeur de fichier au début de la fenêtre en cours. L'utilisation d'une position héritée d'un appel précédent est une **violation et un rejet immédiat.**

*   **I5 : L'Import de Fonctions (IAT) et la Propreté**
    *   **Attendu :** Seules les fonctions `SetFilePointerEx`, `ReadFile`, et `GetLastError` peuvent être appelées (IAT déclarée D161). Les registres non volatils (ex: `rbx`, `rbp`, `r12-r15`) doivent être préservés et restaurés. L'utilisation de `NOP` (0x90) doit être limitée à ce qui est strictement nécessaire pour l'alignement ou le padding, et ne doit pas masquer une opération manquante. Toute violation est un **rejet.**

---

### **2. Procédure de Jugement**

1.  **Phase 1 : Vérification de l'Héritage (I1).** Avant toute exécution, l'oracle du build vérifiera l'intégrité octet par octet des blocs tls13-01..04. Si R7 n'est pas respecté, le jugement est **REJET - VIOLATION HÉRITAGE (R7)**. La pièce est refusée.

2.  **Phase 2 : Exécution des Vecteurs.** La pièce de code machine sera exécutée dans un environnement contrôlé pour simuler les cas de test V1 à V5.
    *   Le verdict pour chaque vecteur sera enregistré.
    *   Une seule déviation par rapport à un attendu de l'Oracle (Q, E, I) entraîne un **REJET** du bloc.

3.  **Phase 3 : Arbitrage Final.**
    *   **Si tous les vecteurs (V1, V2, V3, V4, V5) sont réussis et que tous les invariants (I1 à I5) sont respectés :** Le verdict est **CONFORME**. Le bloc est accepté.
    *   **Si un seul point de l'Oracle n'est pas respecté :** Le verdict est **REJET**, avec la raison précise de la déviation (ex: "REJET - V1 Échec différentiel", "REJET - I2 Violation source unique SHA", "REJET - E4 Sortie corrompute en cas d'échec système").

Ce jugement est complet et ne dépend d'aucune autre information que celle contenue dans le Contrat. L'Oracle est mon guide.