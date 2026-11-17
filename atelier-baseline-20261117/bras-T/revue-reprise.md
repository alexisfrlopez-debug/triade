**Révision du contrat**

*   **P1 (session ouverte)** : `cmp qword ptr [rbx + 528], -1` (instruction présente).
    *   *Écart* : Aucun.
*   **P2 (rcx=offset, rdx=length)** : `mov r15, rcx` / `mov r14, rdx` (instructions présentes).
    *   *Écart* : Aucun.
*   **P3 (offset+length ≤ taille)** : `add rax, rdx` / `cmp rax, qword ptr [rbx + 520]` (instructions présentes).
    *   *Écart* : Aucun.
*   **P4 (r8=sortie)** : `mov r13, r8` (instruction présente).
    *   *Écart* : Aucun.

*   **Q1 (sortie = SHA256)** : `mov rsi, rsp` / `add rsi, 0xB0` / `mov rdi, r13` / `rep movsb` (instructions présentes).
    *   *Écart* : Aucun.
*   **Q2 (composition tls13-01..04)** : `call 0xc000` (tls13-01) / `call 0xc240` (tls13-03) / `call 0xc300` (tls13-04) (instructions présentes).
    *   *Écart* : Aucun.
*   **Q3 (longueur=0 → condensé vide)** : `test r14, r14` / `jz .vide` / `.vide:` / `call 0xc000` / `call 0xc300` (instructions présentes).
    *   *Écart* : Aucun.
*   **Q4 (rax=0)** : `xor rax, rax` (instruction présente).
    *   *Écart* : Aucun.

*   **I1 (héritage PAR LA CARTE)** : Les appels `call 0xc000`, `call 0xc240`, `call 0xc300` utilisent le contexte SHA à `rsp+0x40` (instructions présentes).
    *   *Écart* : Aucun.
*   **I2 (aucune SHA redéclarée)** : Absence d'appel à `SHA256_Init`, `SHA256_Update`, `SHA256_Final` ou équivalent.
    *   *Écart* : Aucun.
*   **I3 (lecture via TAMPON_CUMUL)** : `lea rdx, [rip + 0xbb06]` (instruction présente).
    *   *Écart* : Aucun.
*   **I4 (repositionnement avant ReadFile)** : `call qword ptr [rip + IAT_SetFilePointerEx` (instruction présente).
    *   *Écart* : Aucun.
*   **I5 (IAT déclarée, registres rendus, NOP)** : `extern SetFilePointerEx`, `extern ReadFile`, `extern GetLastError` / `pop ...` / `ret` (instructions présentes).
    *   *Écart* : Aucun.

*   **E1 (session fermée → rax=-4)** : `je .erreur_session` / `.erreur_session:` / `mov rax, -4` (instructions présentes).
    *   *Écart* : Aucun.
*   **E2 (hors bornes → rax=-3)** : `ja .erreur_hors_bornes` / `.erreur_hors_bornes:` / `mov rax, -3` (instructions présentes).
    *   *Écart* : Aucun.
*   **E3 (sortie nulle → rax=-5)** : `jz .erreur_entree` / `.erreur_entree:` / `mov rax, -5` (instructions présentes).
    *   *Écart* : Aucun.
*   **E4 (erreur système → rax=-6)** : `test rax, rax` (après ReadFile) / `jz .erreur_systeme` / `.erreur_systeme:` / `mov rax, -6` (instructions présentes).
    *   *Écart* : Aucun.

Verdict : CONFORME
