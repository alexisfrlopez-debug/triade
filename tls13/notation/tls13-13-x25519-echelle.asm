; tls13-13-x25519-echelle · bloc X25519 échelle de Montgomery (RFC 7748 § 5, miroir av-11) · spec tls13-13:R1 · bloc carte h100013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xd100, taille 2944 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-09/10/11 (4 add + 4 sub + 10 mul PAR ITÉRATION — I5, l'erratum de compte consigné ; entre 255 et 510 pour l'inversion) ; le cswap XOR MASQUÉ (I1), les états sur la PILE (I3, le sous-cadre réel consigné), l'exposant p−2 au fixture R_EXP_INV (I4) ; le clamp et le masque bit 255 dans des COPIES LOCALES (P2/P3)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-13-x25519-echelle.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 2887 o · padding : 57 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0xd391, .inv_boucle=0xdb0f, .inv_saut=0xdb59
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xd19f + 0x7 + 0x2d7a = 0xff20
; Appels directs (l'adresse scellée du plan — I1) : call 0xca00, call 0xc980, call 0xca00, call 0xc980, call 0xcb40, call 0xcb40, call 0xcb40, call 0xcb40, call 0xcb40, call 0xca00, call 0xcb40, call 0xc980, call 0xcb40, call 0xca00, call 0xcb40, call 0xcb40, call 0xc980, call 0xcb40, call 0xcb40, call 0xcb40, call 0xcb40
push rdi
push rbx
push rbp
sub rsp, 0x210
mov rdi, rcx
mov rax, qword ptr [rdx]
movabs r11, 0xfffffffffffffff8
and rax, r11
mov qword ptr [rsp + 0x1b0], rax
mov rax, qword ptr [rdx + 8]
mov qword ptr [rsp + 0x1b8], rax
mov rax, qword ptr [rdx + 16]
mov qword ptr [rsp + 0x1c0], rax
mov rax, qword ptr [rdx + 24]
movabs r11, 0x7fffffffffffffff
and rax, r11
movabs r11, 0x4000000000000000
or rax, r11
mov qword ptr [rsp + 0x1c8], rax
mov rax, qword ptr [r8]
mov qword ptr [rsp + 0x1d0], rax
mov rax, qword ptr [r8 + 8]
mov qword ptr [rsp + 0x1d8], rax
mov rax, qword ptr [r8 + 16]
mov qword ptr [rsp + 0x1e0], rax
mov rax, qword ptr [r8 + 24]
movabs r11, 0x7fffffffffffffff
and rax, r11
mov qword ptr [rsp + 0x1e8], rax
lea r11, [rip + 0x2d7a]
mov rax, qword ptr [r11]
mov qword ptr [rsp + 0x1f0], rax
mov rax, qword ptr [r11 + 8]
mov qword ptr [rsp + 0x1f8], rax
mov rax, qword ptr [r11 + 16]
mov qword ptr [rsp + 0x200], rax
mov rax, qword ptr [r11 + 24]
mov qword ptr [rsp + 0x208], rax
movabs r11, 0x7ffffffffffff
mov rax, qword ptr [rsp + 0x1d0]
and rax, r11
mov qword ptr [rsp + 0x20], rax
mov rax, qword ptr [rsp + 0x1d0]
shr rax, 51
mov rdx, qword ptr [rsp + 0x1d8]
shl rdx, 13
or rax, rdx
and rax, r11
mov qword ptr [rsp + 0x28], rax
mov rax, qword ptr [rsp + 0x1d8]
shr rax, 38
mov rdx, qword ptr [rsp + 0x1e0]
shl rdx, 26
or rax, rdx
and rax, r11
mov qword ptr [rsp + 0x30], rax
mov rax, qword ptr [rsp + 0x1e0]
shr rax, 25
mov rdx, qword ptr [rsp + 0x1e8]
shl rdx, 39
or rax, rdx
and rax, r11
mov qword ptr [rsp + 0x38], rax
mov rax, qword ptr [rsp + 0x1e8]
shr rax, 12
and rax, r11
mov qword ptr [rsp + 0x40], rax
mov qword ptr [rsp + 0x48], 1
mov qword ptr [rsp + 0x50], 0
mov qword ptr [rsp + 0x58], 0
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov qword ptr [rsp + 0x70], 0
mov qword ptr [rsp + 0x78], 0
mov qword ptr [rsp + 0x80], 0
mov qword ptr [rsp + 0x88], 0
mov qword ptr [rsp + 0x90], 0
mov qword ptr [rsp + 0xc0], 1
mov qword ptr [rsp + 0xc8], 0
mov qword ptr [rsp + 0xd0], 0
mov qword ptr [rsp + 0xd8], 0
mov qword ptr [rsp + 0xe0], 0
mov qword ptr [rsp + 0xe8], 121665
mov qword ptr [rsp + 0xf0], 0
mov qword ptr [rsp + 0xf8], 0
mov qword ptr [rsp + 0x100], 0
mov qword ptr [rsp + 0x108], 0
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x40]
mov qword ptr [rsp + 0xb8], rax
mov rbx, 254
xor ebp, ebp
mov rax, rbx
shr rax, 3
movzx eax, byte ptr [rsp + rax + 0x1b0]
mov rcx, rbx
and rcx, 7
shr rax, cl
and eax, 1
mov r11d, eax
xor ebp, eax
mov r10, rbp
shl r10, 63
sar r10, 63
mov rax, qword ptr [rsp + 0x48]
xor rax, qword ptr [rsp + 0x98]
and rax, r10
xor qword ptr [rsp + 0x48], rax
xor qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x50]
xor rax, qword ptr [rsp + 0xa0]
and rax, r10
xor qword ptr [rsp + 0x50], rax
xor qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x58]
xor rax, qword ptr [rsp + 0xa8]
and rax, r10
xor qword ptr [rsp + 0x58], rax
xor qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x60]
xor rax, qword ptr [rsp + 0xb0]
and rax, r10
xor qword ptr [rsp + 0x60], rax
xor qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x68]
xor rax, qword ptr [rsp + 0xb8]
and rax, r10
xor qword ptr [rsp + 0x68], rax
xor qword ptr [rsp + 0xb8], rax
mov rax, qword ptr [rsp + 0x70]
xor rax, qword ptr [rsp + 0xc0]
and rax, r10
xor qword ptr [rsp + 0x70], rax
xor qword ptr [rsp + 0xc0], rax
mov rax, qword ptr [rsp + 0x78]
xor rax, qword ptr [rsp + 0xc8]
and rax, r10
xor qword ptr [rsp + 0x78], rax
xor qword ptr [rsp + 0xc8], rax
mov rax, qword ptr [rsp + 0x80]
xor rax, qword ptr [rsp + 0xd0]
and rax, r10
xor qword ptr [rsp + 0x80], rax
xor qword ptr [rsp + 0xd0], rax
mov rax, qword ptr [rsp + 0x88]
xor rax, qword ptr [rsp + 0xd8]
and rax, r10
xor qword ptr [rsp + 0x88], rax
xor qword ptr [rsp + 0xd8], rax
mov rax, qword ptr [rsp + 0x90]
xor rax, qword ptr [rsp + 0xe0]
and rax, r10
xor qword ptr [rsp + 0x90], rax
xor qword ptr [rsp + 0xe0], rax
mov ebp, r11d
mov rax, qword ptr [rsp + 0x48]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x50]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x58]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x60]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x68]
mov qword ptr [rsp + 0x130], rax
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x70]
call 0xca00
lea rcx, [rsp + 0x48]
lea rdx, [rsp + 0x70]
call 0xc980
mov rax, qword ptr [rsp + 0x98]
mov qword ptr [rsp + 0x138], rax
mov rax, qword ptr [rsp + 0xa0]
mov qword ptr [rsp + 0x140], rax
mov rax, qword ptr [rsp + 0xa8]
mov qword ptr [rsp + 0x148], rax
mov rax, qword ptr [rsp + 0xb0]
mov qword ptr [rsp + 0x150], rax
mov rax, qword ptr [rsp + 0xb8]
mov qword ptr [rsp + 0x158], rax
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0xc0]
call 0xca00
lea rcx, [rsp + 0x98]
lea rdx, [rsp + 0xc0]
call 0xc980
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x48]
call 0xcb40
lea rcx, [rsp + 0x98]
lea rdx, [rsp + 0x110]
call 0xcb40
mov rax, qword ptr [rsp + 0x48]
mov qword ptr [rsp + 0x160], rax
mov rax, qword ptr [rsp + 0x50]
mov qword ptr [rsp + 0x168], rax
mov rax, qword ptr [rsp + 0x58]
mov qword ptr [rsp + 0x170], rax
mov rax, qword ptr [rsp + 0x60]
mov qword ptr [rsp + 0x178], rax
mov rax, qword ptr [rsp + 0x68]
mov qword ptr [rsp + 0x180], rax
lea rcx, [rsp + 0x160]
lea rdx, [rsp + 0x160]
call 0xcb40
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x110]
call 0xcb40
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x48], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x50], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x58], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x60], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x68], rax
lea rcx, [rsp + 0x48]
lea rdx, [rsp + 0x110]
call 0xcb40
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x188], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x190], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x198], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x1a0], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x1a8], rax
lea rcx, [rsp + 0x160]
lea rdx, [rsp + 0x110]
call 0xca00
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x130], rax
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0xe8]
call 0xcb40
lea rcx, [rsp + 0x188]
lea rdx, [rsp + 0x110]
call 0xc980
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x70], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x78], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x80], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x88], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x90], rax
lea rcx, [rsp + 0x70]
lea rdx, [rsp + 0x188]
call 0xcb40
mov rax, qword ptr [rsp + 0x138]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x140]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x148]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x150]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x158]
mov qword ptr [rsp + 0x130], rax
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x98]
call 0xca00
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x110]
call 0xcb40
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [rsp + 0xc0], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [rsp + 0xc8], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [rsp + 0xd0], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [rsp + 0xd8], rax
mov rax, qword ptr [rsp + 0x40]
mov qword ptr [rsp + 0xe0], rax
lea rcx, [rsp + 0xc0]
lea rdx, [rsp + 0x110]
call 0xcb40
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x98]
call 0xc980
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x138]
call 0xcb40
mov rax, qword ptr [rsp + 0x138]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x140]
mov qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x148]
mov qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x150]
mov qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x158]
mov qword ptr [rsp + 0xb8], rax
dec rbx
jns 0xd391
mov r10, rbp
shl r10, 63
sar r10, 63
mov rax, qword ptr [rsp + 0x48]
xor rax, qword ptr [rsp + 0x98]
and rax, r10
xor qword ptr [rsp + 0x48], rax
xor qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x50]
xor rax, qword ptr [rsp + 0xa0]
and rax, r10
xor qword ptr [rsp + 0x50], rax
xor qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x58]
xor rax, qword ptr [rsp + 0xa8]
and rax, r10
xor qword ptr [rsp + 0x58], rax
xor qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x60]
xor rax, qword ptr [rsp + 0xb0]
and rax, r10
xor qword ptr [rsp + 0x60], rax
xor qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x68]
xor rax, qword ptr [rsp + 0xb8]
and rax, r10
xor qword ptr [rsp + 0x68], rax
xor qword ptr [rsp + 0xb8], rax
mov rax, qword ptr [rsp + 0x70]
xor rax, qword ptr [rsp + 0xc0]
and rax, r10
xor qword ptr [rsp + 0x70], rax
xor qword ptr [rsp + 0xc0], rax
mov rax, qword ptr [rsp + 0x78]
xor rax, qword ptr [rsp + 0xc8]
and rax, r10
xor qword ptr [rsp + 0x78], rax
xor qword ptr [rsp + 0xc8], rax
mov rax, qword ptr [rsp + 0x80]
xor rax, qword ptr [rsp + 0xd0]
and rax, r10
xor qword ptr [rsp + 0x80], rax
xor qword ptr [rsp + 0xd0], rax
mov rax, qword ptr [rsp + 0x88]
xor rax, qword ptr [rsp + 0xd8]
and rax, r10
xor qword ptr [rsp + 0x88], rax
xor qword ptr [rsp + 0xd8], rax
mov rax, qword ptr [rsp + 0x90]
xor rax, qword ptr [rsp + 0xe0]
and rax, r10
xor qword ptr [rsp + 0x90], rax
xor qword ptr [rsp + 0xe0], rax
mov rax, qword ptr [rsp + 0x70]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x78]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x80]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x88]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x90]
mov qword ptr [rsp + 0x130], rax
mov qword ptr [rsp + 0x138], 1
mov qword ptr [rsp + 0x140], 0
mov qword ptr [rsp + 0x148], 0
mov qword ptr [rsp + 0x150], 0
mov qword ptr [rsp + 0x158], 0
mov rbx, 254
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x138]
call 0xcb40
mov rax, rbx
shr rax, 3
movzx eax, byte ptr [rsp + rax + 0x1f0]
mov rcx, rbx
and rcx, 7
shr rax, cl
test eax, 1
jz 0xdb59
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x110]
call 0xcb40
dec rbx
jns 0xdb0f
lea rcx, [rsp + 0x48]
lea rdx, [rsp + 0x138]
call 0xcb40
movabs r11, 0x7ffffffffffff
mov rax, qword ptr [rsp + 0x48]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x48], rax
add qword ptr [rsp + 0x50], rdx
mov rax, qword ptr [rsp + 0x50]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x50], rax
add qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rsp + 0x58]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x58], rax
add qword ptr [rsp + 0x60], rdx
mov rax, qword ptr [rsp + 0x60]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x60], rax
add qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rsp + 0x50]
shl rax, 51
add rax, qword ptr [rsp + 0x48]
mov qword ptr [rdi], rax
mov rax, qword ptr [rsp + 0x50]
shr rax, 13
mov rdx, qword ptr [rsp + 0x58]
shl rdx, 38
add rax, rdx
mov qword ptr [rdi + 8], rax
mov rax, qword ptr [rsp + 0x58]
shr rax, 26
mov rdx, qword ptr [rsp + 0x60]
shl rdx, 25
add rax, rdx
mov qword ptr [rdi + 16], rax
mov rax, qword ptr [rsp + 0x60]
shr rax, 39
mov rdx, qword ptr [rsp + 0x68]
shl rdx, 12
add rax, rdx
mov qword ptr [rdi + 24], rax
xor eax, eax
add rsp, 0x210
pop rbp
pop rbx
pop rdi
ret
