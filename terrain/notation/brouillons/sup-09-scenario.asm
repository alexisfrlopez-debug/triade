; le fil ouvrier (R3, terrain.17) : porte R10, libc, EXTRACTION du kit embarque,
; T1 (demo M2), T2 (proxy M3 heritage), T4 (tunnel TLS M4 — LE MEME bit
; que T2 : le tunnel vit dans le MÊME proxy.exe 0.5.0-dev.2), T3 (envoi
; Drive, en DERNIER — le journal téléversé embarque la voix du tunnel),
; NETTOYAGE du kit, verdict final — chaque test est INDEPENDANT (un KO
; n'arrete pas les suivants : le constat veut TOUT le tableau) ; TOUTES les
; traces passent par win-05 scelle (entree trace, mode 0/1) ; l'ordre porte
; -> libc -> extraction -> T1 -> T2 -> T4 -> T3 -> nettoyage -> verdict est
; un invariant (le port 25000 est partage par T2 ET T4 : le proxy de T2
; doit être MORT avant celui de T4 ; l'envoi vient en dernier, l'annexe
; doit vivre le temps de l'envoi) ; un test saute pour extraction
; impossible COMPTE ECHEC ; un T3 non applicable (variante publique,
; annexe absente) n'est PAS compte
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
; --- en-tete : banniere + date du run (TAMPON_AFF, 24 o, sup-21) ---
lea rcx, [rip + S00]
mov edx, LEN_S00
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + TAMPON_AFF]
mov edx, 24
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- porte R10 + libc (win-06 scelle) : -1 = arret immediat, 4 = vert ---
call AUTOTEST
mov r15d, eax          ; le verdict survit aux traces (eax meurt a chaque appel)
cmp eax, 0xFFFFFFFF
jne .porte_ok
lea rcx, [rip + S02B]
mov edx, LEN_S02B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S91]
mov edx, LEN_S91
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
jmp .fin
.porte_ok:
lea rcx, [rip + S02A]
mov edx, LEN_S02A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
cmp r15d, 4
je .libc_ok
lea rcx, [rip + S03B]
mov edx, LEN_S03B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S91]
mov edx, LEN_S91
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
jmp .fin
.libc_ok:
lea rcx, [rip + S03A]
mov edx, LEN_S03A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- extraction du kit embarque (D49) : bit0 demo / bit1 proxy / bit2 T3 ---
xor ecx, ecx
call EXTRACTION
mov r15d, eax
; --- T1 si demo pose, sinon saute ET COMPTE ECHEC (jamais de TOUT OK usurpe) ---
test r15d, 1
je .sans_t1
call TEST_DEMO
mov r12d, eax
jmp .apres_t1
.sans_t1:
xor r12d, r12d
.apres_t1:
; --- T2 si proxy pose ---
test r15d, 2
je .sans_t2
call TEST_PROXY
mov r13d, eax
jmp .apres_t2
.sans_t2:
xor r13d, r13d
.apres_t2:
; --- T4 si proxy pose (R3 : LE MÊME bit — le tunnel M4 vit dans le MÊME
; proxy.exe 0.5.0-dev.2 : un seul artefact, deux facettes) ---
test r15d, 2
je .sans_t4
call TEST_TUNNEL
mov ebx, eax
jmp .apres_t4
.sans_t4:
xor ebx, ebx
.apres_t4:
; --- T3 si la variante declare l'annexe (livraison) ; publique = non applicable ---
test r15d, 4
je .sans_t3
call TEST_ENVOI
mov r14d, eax
jmp .apres_t3
.sans_t3:
mov r14d, 1          ; non applicable n'est pas echec (D49 — S06B a dit pourquoi)
.apres_t3:
; --- nettoyage du kit : TOUJOURS apres T3 (l'annexe a vécu le temps de l'envoi) ---
mov ecx, 1
call EXTRACTION
; --- verdict final : les retours COMPTES, jamais une impression ---
test r12d, r12d
je .echec
test r13d, r13d
je .echec
test ebx, ebx
je .echec
test r14d, r14d
je .echec
lea rcx, [rip + S90]
mov edx, LEN_S90
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov eax, 1
jmp .fin
.echec:
lea rcx, [rip + S91]
mov edx, LEN_S91
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
.fin:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
