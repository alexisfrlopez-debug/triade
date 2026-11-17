```c
// Cas Nominaux

// Test N01 : ligne complète, octets standards
// Attendu : "00000000  41 42 43 44 45 46 47 48  49 4A 4B 4C 4D 4E 4F 50  ABCDEFGHIJKLMNOP"
// rax = 0

// Test N02 : ligne complète, octets limites (imprimables)
// Attendu : "00000000  20 21 22 23 24 25 26 27  28 29 2A 2B 2C 2D 2E 2F  !\"#$%&'()*+,-./"
// rax = 0

// Test N03 : ligne complète, octets non-imprimables
// Attendu : "00000000  00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F  ................"
// rax = 0

// Test N04 : ligne complète, mélange d'octets
// Attendu : "00000010  7F FF FE FD FB FA F9 F8  F7 F6 F5 F4 F3 F2 F1 F0  ..............."
// rax = 0

// Test N05 : ligne incomplète, un octet
// Attendu : "00000020  41  .  .  .  .  .  .  .   .  .  .  .  .  .  .  .   A"
// rax = 0

// Test N06 : ligne incomplète, huit octets
// Attendu : "00000030  41 42 43 44 45 46 47 48   .  .  .  .  .  .  .  .   ABCDEFGH"
// rax = 0

// Test N07 : ligne incomplète, quinze octets
// Attendu : "00000040  41 42 43 44 45 46 47 48  49 4A 4B 4C 4D 4E 4F  .   ABCDEFGHIJKLMNO"
// rax = 0

// Test N08 : décalage non-nul, ligne complète
// Attendu : "00000100  AA BB CC DD EE FF 00 11  22 33 44 55 66 77 88 99   ..............."
// rax = 0

// Test N09 : décalage non-nul, ligne incomplète
// Attendu : "00000200  AA BB CC DD EE FF 00 11   22 33 44 55 66 77 88  .   ..........."
// rax = 0

// Cas de Bord

// Test B01 : ligne complète, octet 0x7E (limite imprimable)
// Attendu : "00000000  7E  .  .  .  .  .  .  .   .  .  .  .  .  .  .  .   ~"
// rax = 0

// Test B02 : ligne complète, octet 0x7F (limite non-imprimable)
// Attendu : "00000000  7F  .  .  .  .  .  .  .   .  .  .  .  .  .  .  .   ."
// rax = 0

// Test B03 : ligne incomplète, zéro octets (cas nominal de la ligne finale vide)
// Attendu : "00000000  .  .  .  .  .  .  .  .   .  .  .  .  .  .  .  .    "
// rax = 0

// Test B04 : ligne incomplète, un octet non-imprimable (0x00)
// Attendu : "00000000  00  .  .  .  .  .  .  .   .  .  .  .  .  .  .  .   ."
// rax = 0

// Test B05 : ligne incomplète, un octet imprimable (0x41)
// Attendu : "00000000  41  .  .  .  .  .  .  .   .  .  .  .  .  .  .  .   A"
// rax = 0

// Test B06 : décalage maximal (0x7FFFFFFF)
// Attendu : "7FFFFFF0  AA BB CC DD EE FF 00 11  22 33 44 55 66 77 88 99   ..............."
// rax = 0

// Rejets

// Test R01 : longueur nulle (rdx = 0)
// Attendu : rax = -5, la sortie (tampon de 77 o) reste inchangée.

// Test R02 : longueur 17 (rdx = 17)
// Attendu : rax = -5, la sortie (tampon de 77 o) reste inchangée.

// Test R03 : source nulle (P1 = NULL)
// Attendu : rax = -5, la sortie (tampon de 77 o) reste inchangée.

// Test R04 : sortie nulle (P3 = NULL)
// Attendu : rax = -5, (pas de vérification possible sur la sortie, mais le contrat est rompu).
```