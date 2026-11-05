; tls13-04-sha256-finaliser · brouillon étiqueté — spec tls13-04:R1, bloc carte h100004
; la finalisation et l'extraction (FIPS 180-4 § 5.1.1/6.2.3) — miroir win de
; ah-07 (M6) : 0x80, les zéros, la longueur en BITS u64 gros-boutiste en
; tampon[56..63] ; remplissage >= 56 AVANT bourrage → LA COMPRESSION DU BLOC
; PARTIEL D'ABORD (la borne nommée, jamais franchie en silence).
; rcx = le contexte · rdx = la sortie (32 o) · rax = 0 (Q3 — divergence
; nommée : ah-07 rendait le pointeur de sortie).
; Le contexte finalisé n'est PAS réutilisable sans tls13-01 (Q3 : le
; comportement non défini est REFUSÉ par le harnais, jamais toléré).
; 3 pushes (24 o) : entrée ≡ 8 → 8−24 ≡ 0 (mod 16) aux points d'appel ;
; sub rsp, 0x20 : L'OMBRE msx64 fournie à TLS02 (P3 de tls13-02).
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
mov rcx, rbx
lea rdx, [rbx + 32]
call TLS02
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
mov rcx, rbx
lea rdx, [rbx + 32]
call TLS02
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
xor eax, eax
add rsp, 0x20
pop rdi
pop r12
pop rbx
ret
