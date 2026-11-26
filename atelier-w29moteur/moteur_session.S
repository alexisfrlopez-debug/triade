/* moteur_session.S — LES SIX AMORCES kernel32 DU NOYAU, PORTÉES NATIVES
 * (W29MOTEUR, prompt 2 : l'ouverture de session). Le pont msx64 → SysV :
 * les arguments (rcx, rdx, r8, r9) réordonnés vers (rdi, rsi, rdx, rcx),
 * rdi/rsi SAUVÉS (volatiles en SysV, non-volatiles en msx64 — la loupe
 * peut y vivre des valeurs), l'alignement de pile tenu (rsp ≡ 8 mod 16 à
 * l'entrée du pont ; ≡ 0 au call du helper).
 */
.intel_syntax noprefix
.text

/* CreateFileW(rcx=chemin_utf16, rdx=access, r8=share, r9=sa) → HANDLE */
.global stub_CreateFileW
stub_CreateFileW:
    push rdi
    push rsi
    sub  rsp, 8
    mov  rdi, rcx                /* le chemin UTF-16 */
    call c_createfilew
    add  rsp, 8
    pop  rsi
    pop  rdi
    ret

/* GetFileSizeEx(rcx=handle, rdx=&size) → BOOL */
.global stub_GetFileSizeEx
stub_GetFileSizeEx:
    push rdi
    push rsi
    sub  rsp, 8
    mov  rdi, rcx                /* le handle */
    mov  rsi, rdx                /* &size */
    call c_getfilesizeex
    add  rsp, 8
    pop  rsi
    pop  rdi
    ret

/* SetFilePointerEx(rcx=handle, rdx=distance, r8=newpos, r9=method) → BOOL */
.global stub_SetFilePointerEx
stub_SetFilePointerEx:
    push rdi
    push rsi
    sub  rsp, 8
    mov  rdi, rcx                /* le handle */
    mov  rsi, rdx                /* la distance */
    mov  rdx, r8                 /* newpos */
    mov  rcx, r9                 /* la méthode */
    call c_setfilepointerex
    add  rsp, 8
    pop  rsi
    pop  rdi
    ret

/* ReadFile(rcx=handle, rdx=buf, r8=n, r9=&lu) → BOOL */
.global stub_ReadFile
stub_ReadFile:
    push rdi
    push rsi
    sub  rsp, 8
    mov  rdi, rcx                /* le handle */
    mov  rsi, rdx                /* le tampon */
    mov  rdx, r8                 /* n */
    mov  rcx, r9                 /* &lu */
    call c_readfile
    add  rsp, 8
    pop  rsi
    pop  rdi
    ret

/* CloseHandle(rcx=handle) → BOOL */
.global stub_CloseHandle
stub_CloseHandle:
    push rdi
    push rsi
    sub  rsp, 8
    mov  rdi, rcx
    call c_closehandle
    add  rsp, 8
    pop  rsi
    pop  rdi
    ret

/* GetLastError() → DWORD */
.global stub_GetLastError
stub_GetLastError:
    push rdi
    push rsi
    sub  rsp, 8
    call c_getlasterror
    add  rsp, 8
    pop  rsi
    pop  rdi
    ret
