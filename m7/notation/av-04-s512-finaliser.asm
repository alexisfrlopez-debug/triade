; av-04-s512-finaliser · bloc finalisation bourrage-longueur-extraction · spec av-04:R1 · bloc carte d50004
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1780, taille 256 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/av-04-s512-finaliser.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 187 o · padding : 69 o (NOP)
; Étiquettes résolues : .deux=0x17b2, .extraire=0x1818, .longueur=0x17e1
; Symboles (vérifiés par build_sceau.py contre layout.py) : @A_COMPRIMER=0x1200
push rbx
push r12
sub rsp, 8
mov rbx, rdi
mov r12, rsi
mov eax, dword ptr [rbx + 0xc0]
lea rdi, [rbx + rax + 0x40]
mov byte ptr [rdi], 0x80
cmp eax, 0x70
jae 0x17b2
lea rdi, [rbx + rax + 0x41]
mov ecx, 0x6f
sub ecx, eax
xor eax, eax
rep stosb byte ptr [rdi], al
jmp 0x17e1
lea rdi, [rbx + rax + 0x41]
mov ecx, 0x7f
sub ecx, eax
xor eax, eax
rep stosb byte ptr [rdi], al
mov dword ptr [rbx + 0xc0], 0x80
mov rdi, rbx
call 0x1200
lea rdi, [rbx + 0x40]
mov ecx, 0x70
xor eax, eax
rep stosb byte ptr [rdi], al
mov qword ptr [rbx + 0xb0], 0
mov rax, qword ptr [rbx + 0xc8]
shl rax, 3
bswap rax
mov qword ptr [rbx + 0xb8], rax
mov dword ptr [rbx + 0xc0], 0x80
mov rdi, rbx
call 0x1200
mov rdi, r12
xor ecx, ecx
mov rax, qword ptr [rbx + rcx]
bswap rax
mov qword ptr [rdi], rax
add rdi, 8
add rcx, 8
cmp rcx, 0x40
jb 0x1818
mov rax, r12
add rsp, 8
pop r12
pop rbx
ret
