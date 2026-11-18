=== SUITE DE TESTS ===

**Cas Nominaux (V1, V2)**

*   **Test N1** : Occurrence au début.
    *   `fenêtre`: `0x41, 0x42, 0x43, ...`
    *   `taille_fenêtre`: 100
    *   `motif`: `0x41, 0x42`
    *   `taille_motif`: 2
    *   `départ`: 0
    *   `Attendu`: rax = 0

*   **Test N2** : Occurrence à la fin (juste avant la fin de la fenêtre).
    *   `fenêtre`: `0x00, 0x00, 0x43, 0x44`
    *   `taille_fenêtre`: 4
    *   `motif`: `0x43, 0x44`
    *   `taille_motif`: 2
    *   `départ`: 0
    *   `Attendu`: rax = 2

*   **Test N3** : Occurrence unique au milieu.
    *   `fenêtre`: `0x00, 0x00, 0x12, 0x34, 0x56, 0x00, 0x00`
    *   `taille_fenêtre`: 7
    *   `motif`: `0x12, 0x34, 0x56`
    *   `taille_motif`: 3
    *   `départ`: 0
    *   `Attendu`: rax = 2

*   **Test N4** : Occurrence après le point de départ.
    *   `fenêtre`: `0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF`
    *   `taille_fenêtre`: 6
    *   `motif`: `0xDD, 0xEE`
    *   `taille_motif`: 2
    *   `départ`: 3
    *   `Attendu`: rax = 3

*   **Test N5** : Absence totale du motif.
    *   `fenêtre`: `0x00, 0x01, 0x02, 0x03`
    *   `taille_fenêtre`: 4
    *   `motif`: `0x0A, 0x0B`
    *   `taille_motif`: 2
    *   `départ`: 0
    *   `Attendu`: rax = -1

*   **Test N6** : Motif plus long que la fenêtre restante.
    *   `fenêtre`: `0x00, 0x01, 0x02`
    *   `taille_fenêtre`: 3
    *   `motif`: `0x00, 0x01, 0x02, 0x03`
    *   `taille_motif`: 4
    *   `départ`: 0
    *   `Attendu`: rax = -1

*   **Test N7** : Départ à la fin de la fenêtre (plage vide).
    *   `fenêtre`: `0x00, 0x01, 0x02`
    *   `taille_fenêtre`: 3
    *   `motif`: `0x00`
    *   `taille_motif`: 1
    *   `départ`: 3
    *   `Attendu`: rax = -1

*   **Test N8** : Occurrence multiple, retour de la première.
    *   `fenêtre`: `0x41, 0x41, 0x41, 0x42`
    *   `taille_fenêtre`: 4
    *   `motif`: `0x41, 0x41`
    *   `taille_motif`: 2
    *   `départ`: 0
    *   `Attendu`: rax = 0

*   **Test N9** : Motif de taille 1 (octet unique).
    *   `fenêtre`: `0x00, 0xFF, 0x00, 0xFF`
    *   `taille_fenêtre`: 4
    *   `motif`: `0xFF`
    *   `taille_motif`: 1
    *   `départ`: 0
    *   `Attendu`: rax = 1

*   **Test N10** : Motif de taille maximale (32).
    *   `fenêtre`: (32 octets de `0xAA` suivis de `0xBB`)
    *   `taille_fenêtre`: 33
    *   `motif`: (32 octets de `0xAA`)
    *   `taille_motif`: 32
    *   `départ`: 0
    *   `Attendu`: rax = 0

**Cas de Bords (V2)**

*   **Test B1** : Occurrence exactement au point de départ.
    *   `fenêtre`: `0xDE, 0xAD, 0xBE, 0xEF`
    *   `taille_fenêtre`: 4
    *   `motif`: `0xDE, 0xAD`
    *   `taille_motif`: 2
    *   `départ`: 0
    *   `Attendu`: rax = 0

*   **Test B2** : Occurrence "à cheval" sur le départ.
    *   `fenêtre`: `0x00, 0x01, 0x02, 0x03, 0x04`
    *   `taille_fenêtre`: 5
    *   `motif`: `0x01, 0x02, 0x03`
    *   `taille_motif`: 3
    *   `départ`: 1
    *   `Attendu`: rax = 1

*   **Test B3** : Motif répétitif, la première occurrence est la seule valide.
    *   `fenêtre`: `0x41, 0x41, 0x41, 0x42`
    *   `taille_fenêtre`: 4
    *   `motif`: `0x41, 0x41`
    *   `taille_motif`: 2
    *   `départ`: 1
    *   `Attendu`: rax = 1

*   **Test B4** : Fenêtre de taille 1, motif de taille 1, correspondance.
    *   `fenêtre`: `0x55`
    *   `taille_fenêtre`: 1
    *   `motif`: `0x55`
    *   `taille_motif`: 1
    *   `départ`: 0
    *   `Attendu`: rax = 0

*   **Test B5** : Fenêtre de taille 1, motif de taille 1, non-correspondance.
    *   `fenêtre`: `0x55`
    *   `taille_fenêtre`: 1
    *   `motif`: `0xAA`
    *   `taille_motif`: 1
    *   `départ`: 0
    *   `Attendu`: rax = -1

**Cas de Rejets (V3)**

*   **Test R1** : Rejet E1 - Motif de taille 0.
    *   `fenêtre`: `0x00, 0x01, 0x02`
    *   `taille_fenêtre`: 3
    *   `motif`: (vide)
    *   `taille_motif`: 0
    *   `départ`: 0
    *   `Attendu`: rax = -5

*   **Test R2** : Rejet E2 - Motif de taille > 32.
    *   `fenêtre`: `0x00, 0x01, 0x02`
    *   `taille_fenêtre`: 3
    *   `motif`: (33 octets)
    *   `taille_motif`: 33
    *   `départ`: 0
    *   `Attendu`: rax = -5

*   **Test R3** : Rejet E3 - Départ hors de la fenêtre.
    *   `fenêtre`: `0x00, 0x01, 0x02`
    *   `taille_fenêtre`: 3
    *   `motif`: `0x00`
    *   `taille_motif`: 1
    *   `départ`: 4
    *   `Attendu`: rax = -5

*   **Test R4** : Rejet E3 - Départ négatif (non couvert par le contrat mais logique).
    *   `fenêtre`: `0x00, 0x01, 0x02`
    *   `taille_fenêtre`: 3
    *   `motif`: `0x00`
    *   `taille_motif`: 1
    *   `départ`: -1
    *   `Attendu`: rax = -5