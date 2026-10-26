; ah-07-finaliser · brouillon étiqueté — spec ah-07:R1, bloc carte d40007
; finalisation FIPS § 5.1.1 : 0x80, zéros, longueur u64 gros-boutiste en 56..63
; deux chemins (remplissage < 56 : un bloc ; sinon deux) ; rax = rsi (sortie)
; contexte : H[8] @ +0, tampon[64] @ +32, remplissage @ +96, total @ +104
; 2 pushes (rbx, r12) + sous-cadre 8 : pile 16-alignée aux points d'appel (I3)
@A_COMPRIMER = 0x1200
push rbx
push r12
sub rsp, 8
mov rbx, rdi
mov r12, rsi
mov eax, dword ptr [rbx + 96]
lea rdi, [rbx + rax + 32]
mov byte ptr [rdi], 0x80
cmp eax, 56
jae .deux
lea rdi, [rbx + rax + 33]
mov ecx, 55
sub ecx, eax
xor eax, eax
rep stosb
jmp .longueur
.deux:
lea rdi, [rbx + rax + 33]
mov ecx, 63
sub ecx, eax
xor eax, eax
rep stosb
mov dword ptr [rbx + 96], 64
mov rdi, rbx
call @A_COMPRIMER
lea rdi, [rbx + 32]
mov ecx, 56
xor eax, eax
rep stosb
.longueur:
mov rax, qword ptr [rbx + 104]
shl rax, 3
bswap rax
mov qword ptr [rbx + 88], rax
mov dword ptr [rbx + 96], 64
mov rdi, rbx
call @A_COMPRIMER
mov rdi, r12
xor ecx, ecx
.extraire:
mov eax, dword ptr [rbx + rcx]
bswap eax
mov dword ptr [rdi], eax
add rdi, 4
add ecx, 4
cmp ecx, 32
jb .extraire
mov rax, r12
add rsp, 8
pop r12
pop rbx
ret
