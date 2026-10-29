; tls-07-reception · bloc réception déchiffrée · spec tls-07:R1 · bloc carte g70007
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6a40, taille 768 octets
; Dépendances : IAT secur32 DecryptMessage ; tls-03 type 2 ; tls-02 ; libc-01 normalisation ; résidu Extra à propriétaire unique (la réception tcp-03 est l'affaire de l'APPELANT tls-08)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-07-reception.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 394 o · padding : 374 o (NOP)
; Étiquettes résolues : .normalise=0x6a94, .depassee=0x6b17, .incomplet=0x6b31, .fin_contexte=0x6b57, .succes=0x6b7f
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x6ad1 + 0x6 - 0x40a7 = 0x2a30
sub rsp, 0xE8
mov qword ptr [rsp + 0x60], rcx
mov qword ptr [rsp + 0x68], rdx
mov qword ptr [rsp + 0x70], r8
mov qword ptr [rsp + 0x78], r9
mov r10, [rsp + 0x60]
movzx eax, word ptr [r10 + 0x3C]
lea rcx, [rax + r8]
cmp rcx, 0x8000
ja 0x6b17
test eax, eax
jz 0x6a94
mov rcx, [rsp + 0x68]
lea rdx, [rcx + rax]
call 0x1100
mov r10, [rsp + 0x60]
mov word ptr [r10 + 0x3C], 0
mov rdx, [rsp + 0x68]
mov r8, [rsp + 0x70]
lea r9, [rsp + 0x90]
mov ecx, 2
call 0x6180
mov rax, [rsp + 0x60]
lea rcx, [rax + 0x10]
lea rdx, [rsp + 0x90]
xor r8d, r8d
lea r9, [rsp + 0x58]
mov dword ptr [rsp + 0x58], 0
call qword ptr [rip - 0x40a7]
movsxd rcx, eax
call 0x6080
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jz 0x6b7f
cmp eax, 2
je 0x6b31
cmp eax, 4
je 0x6b57
mov [r10 + 0x30], eax
mov word ptr [r10 + 0x3C], 0
mov r8, [rsp + 0x70]
mov word ptr [r10 + 0x3A], r8w
add rsp, 0xE8
ret
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x30], 5
mov eax, 5
add rsp, 0xE8
ret
mov dword ptr [r10 + 0x30], 2
mov rax, [rsp + 0x70]
mov word ptr [r10 + 0x3A], ax
mov word ptr [r10 + 0x3C], 0
mov eax, 2
add rsp, 0xE8
ret
mov dword ptr [r10 + 0x30], 4
mov eax, [rsp + 0xB0]
mov word ptr [r10 + 0x3A], ax
mov word ptr [r10 + 0x3C], 0
mov eax, 4
add rsp, 0xE8
ret
mov rcx, [rsp + 0xA8]
mov eax, [rsp + 0xA0]
mov rdx, [rsp + 0x78]
mov [rdx], rcx
mov [rdx + 8], rax
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x30], 0
mov ecx, [rsp + 0xB0]
mov word ptr [r10 + 0x3A], cx
mov rax, [rsp + 0x70]
sub rax, rcx
mov word ptr [r10 + 0x3C], ax
xor eax, eax
add rsp, 0xE8
ret
