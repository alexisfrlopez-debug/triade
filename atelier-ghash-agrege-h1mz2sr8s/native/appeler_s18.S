/* appeler_s18.S — le relais d'appel du scellé tls13-18 pour le rig natif.
   Le C appelle (SysV): appeler_s18(rk, nonce, clair, n, aad, na, ct, tag)
     rdi=rk, rsi=nonce, rdx=clair, rcx=n, r8=aad, r9=na,
     [rsp+8]=ct, [rsp+0x10]=tag (à l'entrée).
   Le scellé attend (msx64): rcx=rk, rdx=nonce, r8=clair, r9=n,
     pile [aad, na, ct, tag] — arg5 à [entry_rsp+0x28] du scellé.
   Les non-volatils SysV préservés ; rax, r10 scratch ; l'adresse du scellé
   en immédiat (0xE080, le slot canonique — PUBLIC, aucun secret). */
.intel_syntax noprefix
.global appeler_s18
.text
appeler_s18:
    push rbp
    mov  rbp, rsp
    sub  rsp, 0x58
    /* la zone d'appel : l'ombre 0x00-0x1F, les args à 0x20-0x38 */
    mov  rax, r8                 /* aad */
    mov  [rsp+0x20], rax
    mov  rax, r9                 /* na */
    mov  [rsp+0x28], rax
    mov  rax, [rbp+0x10]         /* ct */
    mov  [rsp+0x30], rax
    mov  rax, [rbp+0x18]         /* tag */
    mov  [rsp+0x38], rax
    /* la valse des registres : SysV -> msx64 */
    mov  rax, rdx                /* clair */
    mov  r10, rcx                /* n */
    mov  rcx, rdi                /* rk */
    mov  rdx, rsi                /* nonce */
    mov  r8, rax                 /* clair */
    mov  r9, r10                 /* n */
    /* l'appel du scellé à son slot canonique */
    mov  r10, 0xE080
    call r10
    add  rsp, 0x58
    pop  rbp
    ret
.size appeler_s18, .-appeler_s18
