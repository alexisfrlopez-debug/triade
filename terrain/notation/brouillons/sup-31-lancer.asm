; lanceur de processus : l'unique frontiere process du superviseur — TOUT
; lancement (demo.exe, proxy.exe, curl.exe) passe par elle ; deux modes :
; 0 = muet (curl ecrit par -o, heritage 0), 1 = tuyaux (proxy : stdin
; alimente pour "quit", stdout capture) ; le repertoire de travail de
; l'enfant est FORCE au repertoire de l'executable (D36 : les chemins
; relatifs sont le piege numero un) ; zero fuite de handle, meme en echec
; (fermeture factorisee : les 4 extremites .data sont contigues)
; pre : rcx = cmdline ASCII NUL-terminee, rdx = mode 0/1
; pile : [0x20..0x4F] args appel (pre-zeroes par le rep stosq), [0x50..0x67]
;        SECURITY_ATTRIBUTES, [0x68..0xCF] STARTUPINFOA, [0xD0..0xE7]
;        PROCESS_INFORMATION (r15), [0xE8..0x1FF] chemin de l'executable
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x200
mov rbx, rcx
mov r12d, edx
lea r15, [rsp + 0xD0]
; --- repertoire de l'executable : GetModuleFileNameA + troncature au '\' ---
lea r13, [rsp + 0xE8]
xor ecx, ecx
mov rdx, r13
mov r8d, 280
call qword ptr [rip + IAT_GMFA]
test eax, eax
je .sans_rep
mov rcx, rax
.balaye:
test rcx, rcx
je .sans_rep
dec rcx
cmp byte ptr [rcx + r13], 0x5C
jne .balaye
mov byte ptr [rcx + r13 + 1], 0
jmp .rep_ok
.sans_rep:
xor r13d, r13d
.rep_ok:
; --- args + SA + SI + PI : zeroes d'un seul rep stosq, puis champs ---
; (AVANT les tuyaux : le SA de [0x50..0x67] est CONSOMME par CreatePipe —
;  l'initialiser apres serait le defect "sa sauvage" : nLength/pointeur
;  garbage -> CreatePipe refuse, proxy jamais lance)
xor eax, eax
lea rdi, [rsp + 0x20]
mov ecx, 24
rep stosq qword ptr [rdi], rax
mov dword ptr [rsp + 0x50], 24
mov dword ptr [rsp + 0x60], 1
mov dword ptr [rsp + 0x68], 0x68
; --- mode 1 : tuyaux heritables (paires .data contigues) ---
test r12d, r12d
je .pas_tuyaux
lea rcx, [rip + TUYAU_IN_RD]
lea rdx, [rcx + 8]
lea r8, [rsp + 0x50]
xor r9d, r9d
call qword ptr [rip + IAT_CREATEPIPE]
test eax, eax
je .echec_sec
lea rcx, [rip + TUYAU_IN_RD]
lea rcx, [rcx + 16]
lea rdx, [rcx + 8]
lea r8, [rsp + 0x50]
xor r9d, r9d
call qword ptr [rip + IAT_CREATEPIPE]
test eax, eax
je .ferme_premier
.pas_tuyaux:
test r12d, r12d
je .si_ok
or dword ptr [rsp + 0xA4], 0x100
mov rax, qword ptr [rip + TUYAU_IN_RD]
mov qword ptr [r15 - 0x18], rax
mov rax, qword ptr [rip + TUYAU_OUT_WR]
mov qword ptr [r15 - 0x10], rax
mov qword ptr [r15 - 0x8], rax
.si_ok:
; --- CreateProcessA(NULL, cmdline, 0, 0, herite=mode, 0, 0, cwd, &si, &pi) ---
xor ecx, ecx
mov rdx, rbx
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], r12d
mov qword ptr [rsp + 0x38], r13
lea rax, [rsp + 0x68]
mov qword ptr [rsp + 0x40], rax
mov qword ptr [rsp + 0x48], r15
call qword ptr [rip + IAT_CREATEPROCESS]
test eax, eax
je .echec_cp
; --- succes : HPROC pose, hThread ferme, extremites enfant fermees ---
mov rax, qword ptr [r15]
mov qword ptr [rip + HPROC], rax
mov rcx, qword ptr [r15 + 16]
call qword ptr [rip + IAT_CH]
test r12d, r12d
je .fin_ok
xor eax, eax
call .ferme_un
mov eax, 3
call .ferme_un
.fin_ok:
mov eax, 1
jmp .fin
.echec_cp:
test r12d, r12d
je .echec_sec
call .ferme_tuyaux
.echec_sec:
xor eax, eax
jmp .fin
.ferme_premier:
xor eax, eax
call .ferme_un
mov eax, 1
call .ferme_un
xor eax, eax
jmp .fin
; --- fermeture factorisee : TUYAU_IN_RD..TUYAU_OUT_WR contigus en .data ---
.ferme_un:
push rcx
lea rcx, [rip + TUYAU_IN_RD]
lea rcx, [rcx + rax*8]
call qword ptr [rip + IAT_CH]
pop rcx
ret
.ferme_tuyaux:
push rcx
xor eax, eax
.ferme_boucle:
call .ferme_un
inc eax
cmp eax, 4
jb .ferme_boucle
pop rcx
ret
.fin:
add rsp, 0x200
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
