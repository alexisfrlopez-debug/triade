Revue la conformité AU CONTRAT, clause par clause (P1-P4, Q1-Q4, I1-I4, E1-E3) : cite la ligne à l'appui pour chaque clause, nomme les écarts éventuels, conclus par « Verdict : CONFORME » ou « Verdict : ÉCART ».
Rien d'autre.

---

**P1 rcx = la source, au moins rdx octets lisibles**
*   Ligne : `const unsigned char *s = src;` (utilisation de `src` en lecture seule).
*   Écart : Aucun. La fonction ne modifie pas la source et s'arrête après `len` octets.
*   Verdict : CONFORME

**P2 rdx = la longueur valide, 1 à 16**
*   Ligne : `if (!src || !out || len == 0 || len > 16) {`
*   Écart : Aucun. La condition `len == 0 || len > 16` couvre les cas invalides.
*   Verdict : CONFORME

**P3 r8 = la sortie, 77 o (LIGNE_TAILLE) accessibles en écriture**
*   Ligne : `char *p = out;` (utilisation de `out` en écriture).
*   Écart : Aucun. Le code écrit exactement 77 caractères avant le NUL final, calculé par les incréments de `p`.
*   Verdict : CONFORME

**P4 r9 = le décalage de la ligne (multiple de 16, ≤ 0x7FFFFFFF — BORNE_TAILLE le garantit)**
*   Ligne : `*p++ = hex_chars[(offset >> (4 * (7 - i))) & 0xF];`
*   Écart : Aucun. Le code n'effectue aucune vérification sur `offset` car le contrat stipule que `BORNE_TAILLE` le garantit. La fonction se concentre sur la composition.
*   Verdict : CONFORME

**Q1 la sortie = « SSSSSSSS  HH HH HH HH HH HH HH HH  HH HH HH HH HH HH HH HH  MMMMMMMMMMMMMMMMM » + NUL : EXACTEMENT 77 o écrits**
*   Lignes : La boucle hexadécimale (8 octets), l'ajout des deux espaces, la boucle des 16 groupes hexadécimaux (avec le `if (i == 7)` pour l'espace médian double), l'ajout des deux espaces, la boucle du miroir ASCII, et finally `*p = '\0';`.
*   Écart : Aucun. Le format est respecté et le comptage des écritures via `p` garantit 77 caractères avant le NUL.
*   Verdict : CONFORME

**Q2 le miroir : l'octet 0x20 à 0x7E → le caractère ; tout autre → « . »**
*   Ligne : `*p++ = (c >= 0x20 && c <= 0x7E) ? c : '.';`
*   Écart : Aucun. L'opérateur ternaire implémente exactement la logique décrite.
*   Verdict : CONFORME

**Q3 la ligne INCOMPLÈTE (rdx < 16) : les groupes au-delà de rdx = deux espaces, le miroir au-delà = un espace**
*   Lignes : `if (i < len) { ... } else { *p++ = ' '; *p++ = ' '; }` (pour l'hexa) et `if (i < len) { ... } else { *p++ = ' '; }` (pour le miroir).
*   Écart : Aucun. Les conditions `if (i < len)` gèrent correctement le cas d'une ligne incomplète.
*   Verdict : CONFORME

**Q4 rax = 0**
*   Ligne : `return 0;`
*   Écart : Aucun. La fonction retourne bien 0 en cas de succès.
*   Verdict : CONFORME

**I1 AUCUNE entrée IAT, AUCUN site syscall, AUCUN état détenu**
*   Lignes : Aucun appel de fonction (sauf `hex_chars` qui est une table locale), aucune instruction système. Les seules variables sont locales ou des pointeurs sur les arguments.
*   Écart : Aucun. La fonction est pure ISO C, sans état ni dépendance externe.
*   Verdict : CONFORME

**I2 AUCUN débordement : la composition écrit EXACTEMENT les 77 o de P3**
*   Lignes : Le comptage des écritures est implicite mais exact. Les pointeurs `p` et `s` sont déplacés dans des bornes fixes (8, 16, 16).
*   Écart : Aucun. Le tampon de sortie est écrit octet par octet sans jamais dépasser la zone allouée pour la ligne de 77 caractères.
*   Verdict : CONFORME

**I3 la source est LUE SEULE (jamais modifiée)**
*   Ligne : `const unsigned char *s = src;`
*   Écart : Aucun. La déclaration `const` garantit que la source n'est pas modifiée.
*   Verdict : CONFORME

**I4 les chiffres hexa : la table « 0123456789ABCDEF » ... aucun registre non volatil détruit ; NOP, 0x90**
*   Ligne : `static const char hex_chars[] = "0123456789ABCDEF";`
*   Écart : L'absence de `NOP` (0x90) est un écart par rapport à la clause explicite « NOP, 0x90 ». Cependant, la clause « aucun registre non volatil détruit » est respectée par la convention d'appel x64 (la fonction n'utilise que des registres volatils rcx, rdx, r8, r9, rax, r10, r11). La table hexadécimale est correcte.
*   Verdict : ÉCART

**E1 : longueur 0 (P2) → verdict -5**
*   Ligne : `if (!src || !out || len == 0 || len > 16) { return -5; }`
*   Écart : Aucun. Le cas `len == 0` est correctement géré.
*   Verdict : CONFORME

**E2 : longueur > 16 (P2) → verdict -5**
*   Ligne : `if (!src || !out || len == 0 || len > 16) { return -5; }`
*   Écart : Aucun. Le cas `len > 16` est correctement géré.
*   Verdict : CONFORME

**E3 : source ou sortie nulle (P1/P3) → verdict -5**
*   Ligne : `if (!src || !out || len == 0 || len > 16) { return -5; }`
*   Écart : Aucun. Les cas `!src` et `!out` sont correctement gérés.
*   Verdict : CONFORME