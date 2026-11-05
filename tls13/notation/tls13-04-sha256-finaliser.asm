; tls13-04-sha256-finaliser · bloc finalisation bourrage-longueur-extraction · spec tls13-04:R1 · bloc carte h100004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc300, taille 192 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-02 (les compressions finales, DEUX appels à l'adresse scellée — I1) ; le tampon passé en second argument
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-04-sha256-finaliser.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 165 o · padding : 27 o (NOP, 0x90)
; Étiquettes résolues : .deux=0xc330, .longueur=0xc360, .extraire=0xc387
; Appels directs (l'adresse scellée du plan — I1) : call 0xc080, call 0xc080
push rbx
push r12
push rdi
sub rsp, 0x20
mov rbx, rcx
mov r12, rdx
mov eax, dword ptr [rbx + 96]
lea rdi, [rbx + rax + 32]
mov byte ptr [rdi], 0x80
cmp eax, 56
jae 0xc330
lea rdi, [rbx + rax + 33]
mov ecx, 55
sub ecx, eax
xor eax, eax
rep stosb
jmp 0xc360
lea rdi, [rbx + rax + 33]
mov ecx, 63
sub ecx, eax
xor eax, eax
rep stosb
mov dword ptr [rbx + 96], 64
mov rcx, rbx
lea rdx, [rbx + 32]
call 0xc080
lea rdi, [rbx + 32]
mov ecx, 56
xor eax, eax
rep stosb
mov rax, qword ptr [rbx + 104]
shl rax, 3
bswap rax
mov qword ptr [rbx + 88], rax
mov dword ptr [rbx + 96], 64
mov rcx, rbx
lea rdx, [rbx + 32]
call 0xc080
mov rdi, r12
xor ecx, ecx
mov eax, dword ptr [rbx + rcx]
bswap eax
mov dword ptr [rdi], eax
add rdi, 4
add ecx, 4
cmp ecx, 32
jb 0xc387
xor eax, eax
add rsp, 0x20
pop rdi
pop r12
pop rbx
ret
