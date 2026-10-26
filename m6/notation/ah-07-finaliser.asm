; ah-07-finaliser · bloc finalisation bourrage-longueur-extraction · spec ah-07:R1 · bloc carte d40007
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1500, taille 256 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/ah-07-finaliser.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 156 o · padding : 100 o (NOP)
; Étiquettes résolues : .deux=0x152f, .extraire=0x157e, .longueur=0x155b
; Symboles (vérifiés par build_ah.py contre layout.py) : @A_COMPRIMER=0x1200
push rbx
push r12
sub rsp, 8
mov rbx, rdi
mov r12, rsi
mov eax, dword ptr [rbx + 0x60]
lea rdi, [rbx + rax + 0x20]
mov byte ptr [rdi], 0x80
cmp eax, 0x38
jae 0x152f
lea rdi, [rbx + rax + 0x21]
mov ecx, 0x37
sub ecx, eax
xor eax, eax
rep stosb byte ptr [rdi], al
jmp 0x155b
lea rdi, [rbx + rax + 0x21]
mov ecx, 0x3f
sub ecx, eax
xor eax, eax
rep stosb byte ptr [rdi], al
mov dword ptr [rbx + 0x60], 0x40
mov rdi, rbx
call 0x1200
lea rdi, [rbx + 0x20]
mov ecx, 0x38
xor eax, eax
rep stosb byte ptr [rdi], al
mov rax, qword ptr [rbx + 0x68]
shl rax, 3
bswap rax
mov qword ptr [rbx + 0x58], rax
mov dword ptr [rbx + 0x60], 0x40
mov rdi, rbx
call 0x1200
mov rdi, r12
xor ecx, ecx
mov eax, dword ptr [rbx + rcx]
bswap eax
mov dword ptr [rdi], eax
add rdi, 4
add ecx, 4
cmp ecx, 0x20
jb 0x157e
mov rax, r12
add rsp, 8
pop r12
pop rbx
ret
