; fichiers du terrain : lire/ecrire/supprimer avec prefixe repertoire —
; le facteur commun des tests (tout fichier vit A COTE de l'executable,
; D36) ; DIR_LONG calcule au premier appel puis cache en .data (un seul
; proprietaire du calcul) ; lecture dans TAMPON_CMD+0 (<= 640 o, LU pose),
; ecriture depuis TAMPON_CMD+ZONE_COMPO ; zero fuite de handle
; pre : rcx = nom NUL-termine, edx = op (0 lire / 1 ecrire / 2 supprimer),
;       r8d = longueur du nom (NUL compris), r9d = longueur du contenu (op 1)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov rbx, rcx
mov r12d, edx
mov r13, r8
mov r14d, r9d
; --- prefixe : cache DIR_LONG ou balayage arrière de BUF_CHEMIN ---
cmp qword ptr [rip + DIR_LONG], 0
jne .dir_pret
lea rcx, [rip + BUF_CHEMIN]
call STRLEN
mov rcx, rax
lea rdx, [rip + BUF_CHEMIN]
.balaye:
test rcx, rcx
je .pose_dir
cmp byte ptr [rdx + rcx - 1], 0x5C
je .pose_dir
dec rcx
jmp .balaye
.pose_dir:
mov qword ptr [rip + DIR_LONG], rcx
.dir_pret:
mov r8, qword ptr [rip + DIR_LONG]
lea rcx, [rip + TAMPON_CMD]
lea rdx, [rip + BUF_CHEMIN]
call MEMCPY
mov r8, r13
lea rcx, [rip + TAMPON_CMD]
add rcx, qword ptr [rip + DIR_LONG]
mov rdx, rbx
call MEMCPY
; --- dispatch ---
test r12d, r12d
je .lire
cmp r12d, 1
je .ecrire
cmp r12d, 2
je .supprimer
xor eax, eax
jmp .fin
.lire:
lea rcx, [rip + TAMPON_CMD]
mov edx, 0x80000000
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 3
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip + IAT_CREATEFILE]
cmp rax, -1
je .absent
mov r15, rax
mov rcx, r15
lea rdx, [rip + TAMPON_CMD]
mov r8d, 640
lea r9, [rip + LU]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_RF]
mov rcx, r15
call qword ptr [rip + IAT_CH]
mov rax, qword ptr [rip + LU]
jmp .fin
.absent:
xor eax, eax
jmp .fin
.ecrire:
lea rcx, [rip + TAMPON_CMD]
mov edx, 0x40000000
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip + IAT_CREATEFILE]
cmp rax, -1
je .absent
mov r15, rax
mov rcx, r15
lea rdx, [rip + TAMPON_COMPO]
mov r8, r14
lea r9, [rip + LU]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_WF]
mov r13d, eax
mov rcx, r15
call qword ptr [rip + IAT_CH]
mov eax, r13d
jmp .fin
.supprimer:
lea rcx, [rip + TAMPON_CMD]
call qword ptr [rip + IAT_DELETEFILE]
.fin:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
