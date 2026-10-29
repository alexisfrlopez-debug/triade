; tls-03 · jetons SSPI (descripteurs) · spec tls-03:R1 · types {0, 1, 2}
; pre : rcx = type, rdx = tampon utile, r8 = longueur, r9 = cadre, type 1 :
; [rsp+0x28] = tailles de flux {u32 en-tête, u32 queue, u32 message max}
; post : rax 0 = cadre porte SecBufferDesc complet (le descripteur RÉFÈRE,
;        ne possède pas — aucune copie du tampon utile) ;
;        rax 1 = jeton > 16384 (type 0) ou clair > message max (type 1) ;
;        rax 2 = type hors {0,1,2} — Q2/Q3 : RIEN n'est écrit (bornes AVANT
;        toute écriture, en-tête compris)
; Mise en page (sspi.h, x64) : Desc{u32 ulVersion=0, u32 cBuffers, u64 pBuffers
; -> cadre+0x10} puis SecBuffer{u32 cb, u32 type, u64 pv} × n.
; Type 0 : TOKEN(2). Type 1 : STREAM_HEADER(7) [pv = clair - en-tête,
; cadre contigu], DATA(1) [pv = clair], STREAM_TRAILER(6) [pv = clair + len].
; Type 2 : DATA(1) + 3 × EMPTY. Feuille pure (I2) ; volatils seuls (I4)
cmp ecx, 3
jae .refus_type
test ecx, ecx
jz .poignee
cmp ecx, 1
je .emission
mov dword ptr [r9], 0
lea r11, [r9 + 0x10]
mov qword ptr [r9 + 8], r11
mov dword ptr [r9 + 4], 4
mov dword ptr [r9 + 0x10], r8d
mov dword ptr [r9 + 0x14], 1
mov qword ptr [r9 + 0x18], rdx
mov qword ptr [r9 + 0x20], 0
mov qword ptr [r9 + 0x28], 0
mov qword ptr [r9 + 0x30], 0
mov qword ptr [r9 + 0x38], 0
mov qword ptr [r9 + 0x40], 0
mov qword ptr [r9 + 0x48], 0
xor eax, eax
ret
.poignee:
cmp r8, 16384
ja .refus_longueur
mov dword ptr [r9], 0
lea r11, [r9 + 0x10]
mov qword ptr [r9 + 8], r11
mov dword ptr [r9 + 4], 1
mov dword ptr [r9 + 0x10], r8d
mov dword ptr [r9 + 0x14], 2
mov qword ptr [r9 + 0x18], rdx
xor eax, eax
ret
.emission:
mov r11, [rsp + 0x28]
mov r10d, [r11 + 8]
cmp r8, r10
ja .refus_longueur
mov r10d, [r11]
mov r11d, [r11 + 4]
mov dword ptr [r9], 0
lea rax, [r9 + 0x10]
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 4], 3
mov dword ptr [r9 + 0x10], r10d
mov dword ptr [r9 + 0x14], 7
mov rax, rdx
sub rax, r10
mov qword ptr [r9 + 0x18], rax
mov dword ptr [r9 + 0x20], r8d
mov dword ptr [r9 + 0x24], 1
mov qword ptr [r9 + 0x28], rdx
mov dword ptr [r9 + 0x30], r11d
mov dword ptr [r9 + 0x34], 6
lea rax, [rdx + r8]
mov qword ptr [r9 + 0x38], rax
xor eax, eax
ret
.refus_longueur:
mov eax, 1
ret
.refus_type:
mov eax, 2
ret
