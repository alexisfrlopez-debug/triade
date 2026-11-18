### Revue du bloc LOUPE-16 SAISIE

**P1 :** appelée par la procédure (loupe-09 Q3) sur WM_CHAR hors mode saisie — les SEIZE chiffres hexa écoutent, tout autre caractère est ignoré proprement.
- **Instruction :** `cmp r8d, 0x08` (test si VK_BACKSPACE) ; `cmp eax, 0x61` à `cmp eax, 0x46` (test si 'a'-'f' ou 'A'-'F') ; `sub eax, 0x30` (test si '0'-'9'). Les sauts conditionnels (`jne`, `ja`, `jb`) dirigent vers `.silence` si le caractère n'est pas hexa.
- **Écart :** Aucun. Les 16 chiffres hexa sont correctement filtrés.
- **Verdict : CONFORME**

**P2 :** la session est ouverte.
- **Instruction :** `cmp qword ptr [rbx + 528], -1` (test si session ouverte, avec `.ouverte` pointant vers le code de verdict -4).
- **Écart :** Aucun. Un échec (-4) est retourné si la session n'est pas ouverte.
- **Verdict : CONFORME**

**P3 :** la zone JOURNAL du plan (4 112 o : 256 entrées de 16 o — u64 décalage · u8 octet · 7 réserve — et le nombre) + le nibble de la zone SAISIE.
- **Instruction :** `lea r13, [rip + 0x81a2]` (chargement de l'adresse de la zone JOURNAL) ; `mov dword ptr [r13 + 4], 1` (stockage du premier chiffre dans le nibble de la zone SAISIE) ; `mov qword ptr [r9], r14` (stockage du décalage dans le journal) ; `mov byte ptr [r9 + 8], r15b` (stockage de l'octet dans le journal).
- **Écart :** Aucun. Les structures de données du journal et de la saisie sont manipulées conformément à la spécification.
- **Verdict : CONFORME**

**Q1 :** LE PREMIER CHIFFRE : nibble actif, la valeur (0 à 15) posée — la cellule attend (rien n'est écrit : un demi-octet n'existe pas au disque ni au journal).
- **Instruction :** `mov dword ptr [r13 + 4], 1` (indicateur d'attente du premier chiffre) ; `mov dword ptr [r13 + 8], r15d` (stockage de la valeur du premier chiffre).
- **Écart :** Aucun. L'état d'attente est correctement géré sans écriture disque ou au journal.
- **Verdict : CONFORME**

**Q2 :** LE SECOND CHIFFRE : l'octet = (premier << 4) | second — écrit AU JOURNAL : l'entrée du décalage du curseur (l'entrée PAR DÉCALAGE : si le décalage est déjà au journal, l'octet REMPLACÉ, le nombre n'augmente pas) ; le journal PLEIN (256 distincts) → verdict -3.
- **Instruction :** `shl eax, 4` / `or eax, r15d` (composition de l'octet) ; `cmp qword ptr [r9], r14` (test si décalage existant) ; `je .remplace` (remplacement si existant) ; `inc r10d` / `mov dword ptr [rdx + 4096], r10d` (incrémentation du nombre d'entrées distinctes si nouvelle entrée) ; `cmp r10d, 256` / `jae .saturee` (test de saturation du journal).
- **Écart :** Aucun. La logique de décalage unique, de remplacement et de saturation est implémentée.
- **Verdict : CONFORME**

**Q3 :** ET À LA VUE : si la cellule est dans la fenêtre (curseur − vue < remplissage) : tampon[curseur − vue] = l'octet — l'octet visible IMMÉDIATEMENT.
- **Instruction :** `cmp r8d, r10d` (test si la cellule est visible) ; `jae .absente` (ignorer si hors-fenêtre) ; `mov byte ptr [rdx + rax], r15b` (écriture dans le tampon de vue).
- **Écart :** Aucun. L'octet est écrit dans le tampon de vue uniquement si la cellule est visible.
- **Verdict : CONFORME**

**Q4 :** LA MARQUE : cadre.sale = 1 ET refus_quitter = 0 (la garde de loupe-18 ré-armée : après une NOUVELLE écriture, le premier Alt+F4 re-vient avertir) ; le curseur AVANCE (+1, clampé à taille − 1) — la cellule suivante attend.
- **Instruction :** `mov dword ptr [rbx + 556], 1` (marque SALE) ; `mov dword ptr [rbx + 560], 0` (ré-armement de refus_quitter) ; `inc r14` (avance du curseur) ; `cmp r14, rax` / `jb .apres` (clampage) ; `mov r14, rax` (clampage à la taille - 1).
- **Écart :** Aucun. La marque, la garde et le curseur sont gérés conformément.
- **Verdict : CONFORME**

**Q5 :** rax = 0 ; VK_SUPPR pendant l'attente (Q1) → le nibble effacé (l'attente annulée proprement — le premier chiffre repart).
- **Instruction :** `cmp r8d, 0x08` (test si VK_BACKSPACE) ; `jne .caractere` ; `mov dword ptr [r13 + 4], 0` (réinitialisation de l'attente) ; `xor eax, eax` (retour 0).
- **Écart :** Aucun. La gestion de VK_SUPPR (VK_BACKSPACE) annule correctement l'attente.
- **Verdict : CONFORME**

**I1 :** LE DISQUE INTACT : aucune écriture fichier ici (WriteFile vit chez loupe-17 SEUL — la liste IAT du plan le garantit).
- **Instruction :** Absence de toute instruction système d'écriture de fichier (WriteFile, CreateFile, etc.). Les appels externes sont restreints à `loupe-15` (InvalidateRect) et `loupe-02` (recadrage).
- **Écart :** Aucun. L'invariant du disque intact est respecté.
- **Verdict : CONFORME**

**I2 :** le journal est PAR DÉCALAGE (une entrée par octet — la seconde écriture remplace : la sauvegarde écrit chaque octet UNE fois, l'ordre interne du journal est celui de la saisie).
- **Instruction :** `cmp qword ptr [r9], r14` (recherche d'entrée existante par décalage) ; `je .remplace` (remplacement si trouvé). Le nombre d'entrées distinctes (`r10d`) n'est incrémenté que pour une nouvelle entrée.
- **Écart :** Aucun. Le journal est bien géré par décalage unique avec remplacement.
- **Verdict : CONFORME**

**I3 :** la cohérence de vue est tendue par loupe-02 Q2 (le recouvrement : l'octet édité survit au défilement) — ici la moitié locale : l'octet posé au tampon SI visible.
- **Instruction :** `mov byte ptr [rdx + rax], r15b` (écriture dans le tampon de vue) est conditionnée par `cmp r8d, r10d` / `jae .absente`, garantissant que l'octet n'est écrit dans le tampon que si visible.
- **Écart :** Aucun. La cohérence locale de la vue est respectée.
- **Verdict : CONFORME**

**I4 :** le curseur reste BORNÉ [0, taille−1] (l'invariant du cadre) ; AUCUNE entrée IAT propre (l'édition est pure état : le journal, le tampon, la marque) ; NOP, 0x90.
- **Instruction :** `cmp r14, rax` / `jb .apres` / `mov r14, rax` (clampage du curseur). L'absence d'appels système IAT autres que ceux déclarés. La présence de `nop, 0x90`.
- **Écart :** Aucun. Le curseur est borné et l'état est pur.
- **Verdict : CONFORME**

**E1 :** sans session ouverte (P2) → verdict -4 SESSION, rax = -4.
- **Instruction :** `cmp qword ptr [rbx + 528], -1` / `jne .ouverte` / `push -4` / `pop rax`.
- **Écart :** Aucun. Le verdict -4 est retourné comme spécifié.
- **Verdict : CONFORME**

**E2 :** la cellule hors fenêtre valide (curseur − vue ≥ remplissage : la cellule n'existe pas à la vue) → verdict -3 HORS-BORNES — l'écriture AU JOURNAL a quand même lieu ? NON : RIEN n'est écrit (le refus précède le journal — la cellule fantôme n'existe pas, l'oracle le constate).
- **Instruction :** `cmp r8d, r10d` (test `curseur - vue < remplissage`) / `jae .absente` (saut vers le code de refus -3). L'écriture au journal n'a lieu que si la cellule est visible.
- **Écart :** Aucun. Le refus (-3) est retourné et aucune écriture n'a lieu.
- **Verdict : CONFORME**

**E3 :** le journal PLEIN (256 octets DISTINCTS en attente) → verdict -3, la borne nommée à la barre (« journal plein — Ctrl+S »), RIEN perdu (l'octet refusé n'entre pas, l'état demeure).
- **Instruction :** `cmp r10d, 256` / `jae .saturee` / `push -3` / `pop rax`.
- **Écart :** Aucun. Le verdict -3 est retourné et l'octet n'est pas ajouté au journal.
- **Verdict : CONFORME**

**E4 :** le caractère non hexa → IGNORÉ proprement (repli documenté : rax = 0, rien — les seize chiffres seuls écoutent).
- **Instruction :** La série de `cmp` et `j` (jump) qui précède `.silence` garantit que tout caractère non-hexa est ignoré, avec `xor eax, eax` comme retour.
- **Écart :** Aucun. Les caractères non-hexa sont ignorés et rax est mis à 0.
- **Verdict : CONFORME**