=== SUITE DE TESTS ===

**Cas Nominaux**

*   **Test 1 : Gammes aléatoires du proxy.exe (V1)**
    *   Pré : Session ouverte, rcx = [décalage aléatoire], rdx = [longueur aléatoire], r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[rcx..rcx+rdx]).

*   **Test 2 : Gammes témoins du kit (V1)**
    *   Pré : Session ouverte, rcx = [décalage d'un témoin], rdx = [longueur d'un témoin], r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[rcx..rcx+rdx]).

*   **Test 3 : Gammes de 1 octet (V1)**
    *   Pré : Session ouverte, rcx = [décalage], rdx = 1, r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[rcx..rcx+1]).

*   **Test 4 : Gammes de 64 Kio (TAMPON_CUMUL) (V1)**
    *   Pré : Session ouverte, rcx = [décalage], rdx = 65536, r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[rcx..rcx+65536]).

*   **Test 5 : Gammes de 64 Kio + 1 octet (V1)**
    *   Pré : Session ouverte, rcx = [décalage], rdx = 65537, r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[rcx..rcx+65537]).

*   **Test 6 : Gammes de 2 Gio (couverture de TAMPON_CUMUL) (V1)**
    *   Pré : Session ouverte, rcx = 0, rdx = 2147483648, r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[0..2147483648]).

**Cas de Bord**

*   **Test 7 : Gamme vide (FIPS 180-4) (V2)**
    *   Pré : Session ouverte, rcx = 0, rdx = 0, r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.

*   **Test 8 : Gamme « abc » (FIPS 180-4) (V2)**
    *   Pré : Session ouverte, rcx = [décalage de 'abc'], rdx = 3, r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad.

*   **Test 9 : Gamme au début du fichier (rdx > 0)**
    *   Pré : Session ouverte, rcx = 0, rdx = [longueur > 0], r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[0..rdx]).

*   **Test 10 : Gamme à la fin du fichier (rdx > 0)**
    *   Pré : Session ouverte, rcx = [taille du fichier - rdx], rdx = [longueur > 0], r8 = tampon sortie.
    *   Attendu : rax = 0, la sortie octet-identique à hashlib.sha256(F[taille_fichier - rdx..taille_fichier]).

**Cas de Rejet**

*   **Test 11 : Echec E1 - Session non ouverte**
    *   Pré : Session non ouverte (poignée = INVALIDE), rcx = 0, rdx = 0, r8 = tampon sortie.
    *   Attendu : rax = -4, la sortie INTACTE.

*   **Test 12 : Echec E2 - Gamme hors bornes (décalage)**
    *   Pré : Session ouverte, rcx = [taille du fichier + 1], rdx = 1, r8 = tampon sortie.
    *   Attendu : rax = -3, la sortie INTACTE.

*   **Test 13 : Echec E2 - Gamme hors bornes (longueur)**
    *   Pré : Session ouverte, rcx = [taille du fichier - 1], rdx = 2, r8 = tampon sortie.
    *   Attendu : rax = -3, la sortie INTACTE.

*   **Test 14 : Echec E3 - Sortie inutilisable (r8 = 0)**
    *   Pré : Session ouverte, rcx = 0, rdx = 0, r8 = 0.
    *   Attendu : rax = -5.

*   **Test 15 : Echec E4 - SetFilePointerEx en échec**
    *   Pré : Session ouverte, rcx = [décalage], rdx = [longueur], r8 = tampon sortie. Le shim SetFilePointerEx est forcé à échec.
    *   Attendu : rax = -6, la sortie INTACTE, GetLastError() consigné.

*   **Test 16 : Echec E4 - ReadFile en échec**
    *   Pré : Session ouverte, rcx = [décalage], rdx = [longueur > 0], r8 = tampon sortie. Le shim ReadFile est forcé à échec.
    *   Attendu : rax = -6, la sortie INTACTE, GetLastError() consigné.