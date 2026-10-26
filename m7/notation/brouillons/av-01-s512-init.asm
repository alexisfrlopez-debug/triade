; av-01-s512-init · brouillon étiqueté — spec av-01:R1, bloc carte d50001
; H0 FIPS 180-4 § 5.3.5 : immédiats 64 bits via rax (keystone refuse
; imm64 direct vers mémoire — mov rax, imm64 puis mov [rdi+N], rax) ;
; remplissage @ +192, total @ +200 ; feuille : aucun push, aucun appel
mov rax, 0x6a09e667f3bcc908
mov qword ptr [rdi], rax
mov rax, 0xbb67ae8584caa73b
mov qword ptr [rdi + 8], rax
mov rax, 0x3c6ef372fe94f82b
mov qword ptr [rdi + 0x10], rax
mov rax, 0xa54ff53a5f1d36f1
mov qword ptr [rdi + 0x18], rax
mov rax, 0x510e527fade682d1
mov qword ptr [rdi + 0x20], rax
mov rax, 0x9b05688c2b3e6c1f
mov qword ptr [rdi + 0x28], rax
mov rax, 0x1f83d9abfb41bd6b
mov qword ptr [rdi + 0x30], rax
mov rax, 0x5be0cd19137e2179
mov qword ptr [rdi + 0x38], rax
mov dword ptr [rdi + 0xc0], 0
mov qword ptr [rdi + 0xc8], 0
mov rax, rdi
ret
