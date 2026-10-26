; Auto-test de la mini-libc — point d'entrée de selftest.exe (libc-08:R2)
; 21 vecteurs dorés : zone 4, memcmp 4, memcpy 3, strlen 3, itoa 4, memset 3.
sub rsp, 0x40
push rbx
push r12
push r13
push r14
push r15
xor r15, r15
mov ecx, -11
call qword ptr [rip + IAT_GSH]
mov r13, rax
; ===== zone (libc-05/06) — 4 vecteurs =====
; v1 : zone_alloc(16, 8) -> non nul, aligne 8
mov ecx, 16
mov edx, 8
call ZONE_ALLOC
test rax, rax
je .v1ko
mov r14, rax
test rax, 7
jne .v1ko
inc r15
.v1ko:
; v2 : zone_alloc(16, 8) -> p2 - p1 >= 16
mov ecx, 16
mov edx, 8
call ZONE_ALLOC
sub rax, r14
cmp rax, 16
jb .v2ko
inc r15
.v2ko:
; v3 : zone_reset puis zone_alloc(16, 8) -> p3 == p1
call ZONE_RESET
mov ecx, 16
mov edx, 8
call ZONE_ALLOC
cmp rax, r14
jne .v3ko
inc r15
.v3ko:
; v4 : zone_alloc(0x7D0, 8) -> 0 (depassement)
mov ecx, 0x7D0
mov edx, 8
call ZONE_ALLOC
test rax, rax
jne .v4ko
inc r15
.v4ko:
; ===== memcmp (libc-02) — 4 vecteurs =====
; v5 : "TRIADE" vs "TRIADE" -> 0
lea rcx, [rip + S_SA]
lea rdx, [rip + S_SB]
mov r8d, 6
call MEMCMP
test eax, eax
jne .v5ko
inc r15
.v5ko:
; v6 : "TRIADE" vs "TRIADF" -> -1
lea rcx, [rip + S_SA]
lea rdx, [rip + S_SC]
mov r8d, 6
call MEMCMP
cmp eax, -1
jne .v6ko
inc r15
.v6ko:
; v7 : "TRIADF" vs "TRIADE" -> +1
lea rcx, [rip + S_SC]
lea rdx, [rip + S_SA]
mov r8d, 6
call MEMCMP
cmp eax, 1
jne .v7ko
inc r15
.v7ko:
; v8 : "TRI" prefixe de "TRIADE", n=3 -> 0
lea rcx, [rip + S_SD]
lea rdx, [rip + S_SA]
mov r8d, 3
call MEMCMP
test eax, eax
jne .v8ko
inc r15
.v8ko:
; ===== memcpy (libc-01) — 3 vecteurs =====
; v9 : copie 16 octets de motif
mov ecx, 16
mov edx, 8
call ZONE_ALLOC
mov r14, rax
mov rcx, r14
lea rdx, [rip + MOTIF16]
mov r8d, 16
call MEMCPY
mov rcx, r14
lea rdx, [rip + MOTIF16]
mov r8d, 16
call MEMCMP
test eax, eax
jne .v9ko
inc r15
.v9ko:
; v10 : copie de longueur nulle -> sentinelle intacte
mov ecx, 16
mov edx, 8
call ZONE_ALLOC
mov r14, rax
mov rcx, r14
lea rdx, [rip + SENT16]
mov r8d, 16
call MEMCPY
mov rcx, r14
lea rdx, [rip + MOTIF16]
xor r8d, r8d
call MEMCPY
mov rcx, r14
lea rdx, [rip + SENT16]
mov r8d, 16
call MEMCMP
test eax, eax
jne .v10ko
inc r15
.v10ko:
; v11 : copie 33 octets (longueur impaire)
mov ecx, 48
mov edx, 8
call ZONE_ALLOC
mov r14, rax
mov rcx, r14
lea rdx, [rip + MOTIF33]
mov r8d, 33
call MEMCPY
mov rcx, r14
lea rdx, [rip + MOTIF33]
mov r8d, 33
call MEMCMP
test eax, eax
jne .v11ko
inc r15
.v11ko:
; ===== strlen (libc-03) — 3 vecteurs =====
; v12 : chaine vide -> 0
lea rcx, [rip + S_VIDE]
call STRLEN
test rax, rax
jne .v12ko
inc r15
.v12ko:
; v13 : "TRIADE" -> 6
lea rcx, [rip + S_TRIADE]
call STRLEN
cmp rax, 6
jne .v13ko
inc r15
.v13ko:
; v14 : 33 lettres -> 33
lea rcx, [rip + S_33]
call STRLEN
cmp rax, 33
jne .v14ko
inc r15
.v14ko:
; ===== itoa (libc-04) — 4 vecteurs =====
; v15 : 0 -> "0"
xor ecx, ecx
lea rdx, [rsp + 0x30]
call ITOA
lea rcx, [rsp + 0x30]
lea rdx, [rip + I0]
mov r8d, 2
call MEMCMP
test eax, eax
jne .v15ko
inc r15
.v15ko:
; v16 : 4294967295 -> "4294967295"
mov ecx, 0xFFFFFFFF
lea rdx, [rsp + 0x30]
call ITOA
lea rcx, [rsp + 0x30]
lea rdx, [rip + IMAX]
mov r8d, 11
call MEMCMP
test eax, eax
jne .v16ko
inc r15
.v16ko:
; v17 : 1234567890 -> "1234567890"
mov ecx, 1234567890
lea rdx, [rsp + 0x30]
call ITOA
lea rcx, [rsp + 0x30]
lea rdx, [rip + I123]
mov r8d, 11
call MEMCMP
test eax, eax
jne .v17ko
inc r15
.v17ko:
; v18 : 7 -> "7"
mov ecx, 7
lea rdx, [rsp + 0x30]
call ITOA
lea rcx, [rsp + 0x30]
lea rdx, [rip + I7]
mov r8d, 2
call MEMCMP
test eax, eax
jne .v18ko
inc r15
.v18ko:
; ===== memset (libc-07) — 3 vecteurs =====
; v19 : memset(dst, 0, 16) -> zeros
mov ecx, 16
mov edx, 8
call ZONE_ALLOC
mov r14, rax
mov rcx, r14
xor edx, edx
mov r8d, 16
call MEMSET
mov rcx, r14
lea rdx, [rip + ZERO16]
mov r8d, 16
call MEMCMP
test eax, eax
jne .v19ko
inc r15
.v19ko:
; v20 : memset(dst, 0xFF, 33)
mov ecx, 48
mov edx, 8
call ZONE_ALLOC
mov r14, rax
mov rcx, r14
mov edx, 0xFF
mov r8d, 33
call MEMSET
mov rcx, r14
lea rdx, [rip + FF33]
mov r8d, 33
call MEMCMP
test eax, eax
jne .v20ko
inc r15
.v20ko:
; v21 : memset(dst, 'A', 0) -> sentinelle intacte
mov ecx, 16
mov edx, 8
call ZONE_ALLOC
mov r14, rax
mov rcx, r14
lea rdx, [rip + SENT16]
mov r8d, 16
call MEMCPY
mov rcx, r14
mov edx, 65
xor r8d, r8d
call MEMSET
mov rcx, r14
lea rdx, [rip + SENT16]
mov r8d, 16
call MEMCMP
test eax, eax
jne .v21ko
inc r15
.v21ko:
; ===== verdict (auto-hebergee : itoa + memcpy + strlen + write) =====
mov ecx, 64
mov edx, 8
call ZONE_ALLOC
mov rbx, rax
mov r12d, 21
mov rcx, rbx
lea rdx, [rip + PREFIXE]
mov r8d, 21
call MEMCPY
mov ecx, r15d
lea rdx, [rsp + 0x30]
call ITOA
lea rcx, [rsp + 0x30]
call STRLEN
mov r14, rax
mov rcx, rbx
add rcx, r12
lea rdx, [rsp + 0x30]
mov r8, r14
call MEMCPY
add r12, r14
mov rcx, rbx
add rcx, r12
lea rdx, [rip + SLASH]
mov r8d, 1
call MEMCPY
inc r12
mov ecx, 21
lea rdx, [rsp + 0x30]
call ITOA
lea rcx, [rsp + 0x30]
call STRLEN
mov r14, rax
mov rcx, rbx
add rcx, r12
lea rdx, [rsp + 0x30]
mov r8, r14
call MEMCPY
add r12, r14
cmp r15, 21
jne .ko
lea rdx, [rip + OK]
jmp .verdict
.ko:
lea rdx, [rip + KO]
.verdict:
mov rcx, rbx
add rcx, r12
mov r8d, 5
call MEMCPY
add r12, 5
mov rcx, r13
mov rdx, rbx
mov r8, r12
call WRITE
cmp r15, 21
jne .ko_sortie
xor ecx, ecx
jmp .fin
.ko_sortie:
mov ecx, 1
.fin:
call EXIT
