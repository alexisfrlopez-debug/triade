**P1** : Le code source est en langage C.  
Ligne 1-3 : `#include <stdint.h>`, `#include <windows.h>`, `#include <string.h>`.  
Verdict : CONFORME.

**P2** : Le code source est compilable avec `gcc -O2 -std=c11`.  
Lignes 1-3 : Utilisation d'en-têtes standards C et Windows.  
Lignes 5-11 : Définitions de constantes et de types standards C.  
Lignes 13-25 : Définition de macros et de tableaux de constantes standards C.  
Lignes 27-32 : Définition de macros standards C.  
Lignes 34-65 : Fonctions `static` standards C.  
Lignes 67-93 : Fonctions `static` standards C.  
Lignes 95-119 : Fonctions `static` standards C.  
Lignes 121-178 : Fonction exportée et ses appels standards C.  
Verdict : CONFORME.

**P3** : Le code source est lié avec le shim `windows.h` du labo.  
Lignes 2, 150, 154, 158 : Utilisation de types et fonctions de `windows.h` (`HANDLE`, `INVALID_HANDLE_VALUE`, `LARGE_INTEGER`, `SetFilePointerEx`, `ReadFile`).  
Verdict : CONFORME.

**P4** : Le code source ne contient pas de redéfinition de fonctions SHA.  
Lignes 34-178 : Implémentation personnelle de SHA-256. Aucune redéclaration de fonctions externes SHA.  
Verdict : CONFORME.

**Q1** : La fonction exportée est `loupe_05_sha256`.  
Ligne 121 : `long long loupe_05_sha256(uint64_t decalage, uint64_t longueur, void* sortie_ptr) {`.  
Verdict : CONFORME.

**Q2** : La fonction exportée retourne un `long long`.  
Ligne 121 : `long long loupe_05_sha256(...)`.  
Verdict : CONFORME.

**Q3** : La fonction exportée retourne `-4` si la session est invalide.  
Ligne 138 : `return -4;`.  
Verdict : CONFORME.

**Q4** : La fonction exportée retourne `-5` si le pointeur de sortie est `NULL`.  
Ligne 143 : `return -5;`.  
Verdict : CONFORME.

**E1** : La fonction exportée retourne `-4` si `g_session_handle` est `INVALID_HANDLE_VALUE`.  
Ligne 138 : `return -4;`.  
Verdict : CONFORME.

**E2** : La fonction exportée retourne `-3` si `longueur` ou `decalage` est hors des bornes.  
Ligne 148 : `return -3;`.  
Verdict : CONFORME.

**E3** : La fonction exportée retourne `-5` si `sortie_ptr` est `NULL`.  
Ligne 143 : `return -5;`.  
Verdict : CONFORME.

**E4** : La fonction exportée retourne `-6` en cas d'erreur système.  
Lignes 160, 166 : `return -6;`.  
Verdict : CONFORME.

**I3** : La fonction exportée lit le fichier par fenêtres de `CUMUL_FENETRE` octets.  
Lignes 152, 154, 158 : Lecture par blocs de `CUMUL_FENETRE` octets.  
Verdict : CONFORME.

**I4** : La fonction exportée calcule le SHA-256 de la plage spécifiée.  
Lignes 150-177 : Calcul du SHA-256 de la plage `[decalage, decalage + longueur]`.  
Verdict : CONFORME.

**I5** : La fonction exportée écrit le résultat dans `sortie_ptr`.  
Ligne 176 : `sha256_final(&s2, (uint8_t*)sortie_ptr);`.  
Verdict : CONFORME.

Verdict : CONFORME.
