; av-04-s512-finaliser · brouillon étiqueté — spec av-04:R1, bloc d50004
; miroir 128/112/16 de ah-07:R1 : 0x80, zéros, longueur 128 bits GROS-BOUTISTE
;   (mot haut zéro @ tampon+112 = +0xb0, mot bas bswappé @ tampon+120 = +0xb8)
;   — rep stosb ne couvre que 0..111 : le mot haut est posé par mov explicite
; 2 pushes + sub 8 : pile 16-alignée aux appels (miroir ah-07)
@A_COMPRIMER = 0x1200
push rbx
push r12
sub rsp, 8
mov rbx, rdi
mov r12, rsi
mov eax, dword ptr [rbx + 0xc0]
lea rdi, [rbx + rax + 0x40]
mov byte ptr [rdi], 0x80
cmp eax, 0x70
jae .deux
lea rdi, [rbx + rax + 0x41]
mov ecx, 0x6f
sub ecx, eax
xor eax, eax
rep stosb byte ptr [rdi], al
jmp .longueur
.deux:
lea rdi, [rbx + rax + 0x41]
mov ecx, 0x7f
sub ecx, eax
xor eax, eax
rep stosb byte ptr [rdi], al
mov dword ptr [rbx + 0xc0], 0x80
mov rdi, rbx
call @A_COMPRIMER
lea rdi, [rbx + 0x40]
mov ecx, 0x70
xor eax, eax
rep stosb byte ptr [rdi], al
.longueur:
mov qword ptr [rbx + 0xb0], 0
mov rax, qword ptr [rbx + 0xc8]
shl rax, 3
bswap rax
mov qword ptr [rbx + 0xb8], rax
mov dword ptr [rbx + 0xc0], 0x80
mov rdi, rbx
call @A_COMPRIMER
mov rdi, r12
xor ecx, ecx
.extraire:
mov rax, qword ptr [rbx + rcx]
bswap rax
mov qword ptr [rdi], rax
add rdi, 8
add rcx, 8
cmp rcx, 0x40
jb .extraire
mov rax, r12
add rsp, 8
pop r12
pop rbx
ret
