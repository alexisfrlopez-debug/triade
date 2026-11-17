NOTES D'AUTEUR

### EXIGENCES ET SIGNATURE
- **Intention** : Condensé SHA-256 d'une gamme de fichier ouvert, héritage tls13 (M9, scellée 1.0.0) par la carte, fenêtres glissantes 64 Kio.
- **Signature** : P1 (session), P2 (rcx=offset, rdx=length), P3 (in-bounds), P4 (r8=sortie 32o). Post : Q1 (condensé FIPS), Q2 (composition tls13-01/03/04), Q3 (gamme vide = vecteur FIPS), Q4 (rax=0).
- **Preuve** : Fixtures (vecteurs FIPS, proxy.exe scellé). Vecteurs : V1 (différentiel), V2 (doré), V3 (rejet), V4 (échec système), V5 (falsification).

### PIÈGES NOMMÉS
- **P1** : Session invalide → E1 (-4 SESSION).
- **P2** : Offset/length non validés → E2 (-3 HORS-BORNES).
- **P3** : Sortie non accessible → E3 (-5 ENTRÉE).
- **P4** : ReadFile/SetFilePointerEx échoué → E4 (-6 SYSTÈME, GetLastError, sortie INTACTE).
- **Contrebande** : Ré-écriture des octets tls13-01..04 → refus de build (I1).

### INVARIANTS À TENIR
- **I1** : Héritage PAR LA CARTE (R7) : octets tls13-01..04 build == scellé 1.0.0.
- **I2** : Aucune constante SHA redéclarée (H0, bloc 64, contexte à tls13-01).
- **I3** : Lecture via TAMPON_CUMUL, jamais le tampon de vue (invariant d'exclusion).
- **I4** : Pointeur fichier repositionné à chaque fenêtre (SetFilePointerEx avant ReadFile).
- **I5** : IAT déclarée (D161) : SetFilePointerEx, ReadFile, GetLastError. Registres non volatils rendus. NOP (0x90).

### CAS D'ÉCHEC
- **E1** : Sans session → rax = -4.
- **E2** : Gamme hors fichier → rax = -3.
- **E3** : Sortie inutilisable → rax = -5.
- **E4** : ReadFile/SetFilePointerEx échoué → rax = -6 (code GetLastError consigné, sortie intacte).