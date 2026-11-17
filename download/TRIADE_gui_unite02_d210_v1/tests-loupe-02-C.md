Voici la suite de tests pour le bloc `loupe-02`.

---

### Suite de tests : loupe-02

#### Cas nominaux

| Test | Scénario | Attendu (Juge) |
| :--- | :--- | :--- |
| N1 | Lecture au début du fichier (décalage = 0, fichier > 384 octets). | `remplissage` = 384. Tampon [+568] = octets [0, 384) du fichier. `rax` = 0. |
| N2 | Lecture au milieu du fichier (décalage = 1024, fichier > 1024+384 octets). | `remplissage` = 384. Tampon [+568] = octets [1024, 1408) du fichier. `rax` = 0. |
| N3 | Lecture à la fin du fichier (décalage = taille - 100, taille > 100). | `remplissage` = 100. Tampon [+568] = octets [taille-100, taille) du fichier. `rax` = 0. |
| N4 | Lecture avec recouvrement nominal (une entrée du journal à l'intérieur de la fenêtre). | `remplissage` = 384. L'octet du tampon à l'offset de l'entrée journal est l'octet écrit, les autres sont du fichier. `rax` = 0. |
| N5 | Lecture avec recouvrement à la bordure (une entrée du journal au tout premier octet de la fenêtre). | `remplissage` = 384. L'octet du tampon à l'offset `décalage` est l'octet écrit. `rax` = 0. |
| N6 | Lecture avec recouvrement à la bordure (une entrée du journal au tout dernier octet de la fenêtre). | `remplissage` = 384. L'octet du tampon à l'offset `décalage + remplissage - 1` est l'octet écrit. `rax` = 0. |

#### Bords

| Test | Scénario | Attendu (Juge) |
| :--- | :--- | :--- |
| B1 | Lecture d'une fenêtre de 1 octet (fichier de taille 1, décalage = 0). | `remplissage` = 1. Tampon [+568] = octet [0] du fichier. `rax` = 0. |
| B2 | Lecture d'une fenêtre de 384 octets (fichier de taille 384, décalage = 0). | `remplissage` = 384. Tampon [+568] = octets [0, 384) du fichier. `rax` = 0. |
| B3 | Lecture d'une fenêtre de 1 octet (fichier de taille 385, décalage = 384). | `remplissage` = 1. Tampon [+568] = octet [384] du fichier. `rax` = 0. |
| B4 | Lecture avec recouvrement de la totalité de la fenêtre (tous les octets de la fenêtre sont dans le journal). | `remplissage` = 384. Tous les octets du tampon [+568] sont ceux du journal. `rax` = 0. |
| B5 | Lecture avec recouvrement de la totalité de la fenêtre (fichier de taille 384, décalage = 0). | `remplissage` = 384. Tous les octets du tampon [+568] sont ceux du journal. `rax` = 0. |

#### Rejets

| Test | Scénario | Attendu (Juge) |
| :--- | :--- | :--- |
| R1 | Échec P1 : session non ouverte (poignée = INVALIDE). | `verdict` = -4 SESSION. `remplissage` = 0. `rax` = -4. |
| R2 | Échec P2 : décalage non multiple de 16 (ex: décalage = 15). | `verdict` = -5 ENTRÉE. `remplissage` = 0. `rax` = -5. |
| R3 | Échec P3 : décalage égal à la taille du fichier. | `verdict` = -3 HORS-BORNES. `remplissage` = 0. `rax` = -3. |
| R4 | Échec P3 : décalage supérieur à la taille du fichier. | `verdict` = -3 HORS-BORNES. `remplissage` = 0. `rax` = -3. |
| R5 | Échec E4 : `SetFilePointerEx` échoue (ex: disque déconnecté). | `verdict` = -6 SYSTÈME. `remplissage` = 0. `rax` = -6. Le code d'erreur du système est consigné par le harnais. |
| R6 | Échec E4 : `ReadFile` échoue après un `SetFilePointerEx` réussi. | `verdict` = -6 SYSTÈME. `remplissage` = 0. `rax` = -6. Le code d'erreur du système est consigné par le harnais. |