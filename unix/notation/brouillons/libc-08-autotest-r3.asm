; libc-08-autotest-r3 · brouillon étiqueté — spec libc-08:R3, bloc carte f61010
; LE RITUEL DU PATRIMOINE : les 21 vecteurs dorés de la mini-libc scellée
; 0.2.0, exécutés par l'instance SysV des MÊMES contrats (la parité par
; exécution, § 8.3). L'ordre des dépendances est celui de Q1 : zone
; (libc-05/06), memcmp, memcpy, strlen, itoa, memset — chaque vecteur :
; l'appel, le contrôle, l'échec saute l'incrément SANS avorter (le verdict
; est un constat). L'émission passe par écrire (I1 — frag-con : l'instance
; Windows appelait l'IAT WriteFile ; l'instance Linux appelle le bloc du
; corpus, fd 1, AUCUN handle à acquérir : GetStdHandle n'existe pas ici).
; Le verdict N (r15, non volatil — D150) est rendu en rax : la terminaison
; appartient au principal du jalon (Q3 frag-con SysV — l'instance Windows
; terminait elle-même par ExitProcess).
; Cadre : 5 push (rbx/r12/r13/r14/r15) + 0x40 — l'entrée ≡ 8 mod 16, les
; cinq push laissent ≡ 0, le sub multiple de 16 le garde : tout appel part
; aligné (I2/I3). Le brouillon itoa vit à [rsp] (12 o), le tampon ligne est
; alloué DANS L'ARÈNE en phase de verdict (I5 — après le vecteur de
; réinitialisation de la zone, jamais avant).
@A_ZONE_ALLOC = 0x1200
@A_ZONE_RESET = 0x1280
@A_MEMCMP = 0x10C0
@A_MEMCPY = 0x1080
@A_STRLEN = 0x1140
@A_ITOA = 0x1180
@A_MEMSET = 0x12C0
@A_ECRIRE = 0x1000
@SA = 0x140
@SB = 0x148
@SC = 0x150
@SD = 0x158
@MOTIF16 = 0x160
@SENT16 = 0x170
@MOTIF33 = 0x180
@ZERO16 = 0x1A8
@FF33 = 0x1B8
@S_VIDE = 0x1E0
@S_TRIADE = 0x1E8
@S_33 = 0x1F0
@I0 = 0x218
@IMAX = 0x220
@I123 = 0x230
@I7 = 0x240
@PREFIXE = 0x250
@SLASH = 0x248
@OK = 0x268
@KO = 0x270
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
xor r15, r15
; --- ZONE (4 vecteurs) — v1 : allocation alignée (non nulle ET alignée 8) ---
mov edi, 16
mov esi, 8
call @A_ZONE_ALLOC
mov r14, rax
test rax, rax
je .f1
test rax, 7
jne .f1
inc r15
.f1:
; v2 : bornes disjointes (la seconde allocation >= 16 plus loin)
mov edi, 16
mov esi, 8
call @A_ZONE_ALLOC
sub rax, r14
cmp rax, 16
jb .f2
inc r15
.f2:
; v3 : réutilisation déterministe après réinitialisation
call @A_ZONE_RESET
mov edi, 16
mov esi, 8
call @A_ZONE_ALLOC
cmp rax, r14
jne .f3
inc r15
.f3:
; v4 : dépassement -> 0 (2000 > arène 1984)
mov edi, 0x7D0
mov esi, 8
call @A_ZONE_ALLOC
test rax, rax
jne .f4
inc r15
.f4:
; --- MEMCMP (4 vecteurs) — v5 : égalité exacte ---
lea rdi, [rip + @SA]
lea rsi, [rip + @SB]
mov edx, 6
call @A_MEMCMP
test eax, eax
jne .f5
inc r15
.f5:
; v6 : inférieur strict
lea rdi, [rip + @SA]
lea rsi, [rip + @SC]
mov edx, 6
call @A_MEMCMP
cmp eax, -1
jne .f6
inc r15
.f6:
; v7 : supérieur strict
lea rdi, [rip + @SC]
lea rsi, [rip + @SA]
mov edx, 6
call @A_MEMCMP
cmp eax, 1
jne .f7
inc r15
.f7:
; v8 : préfixe (n sous la divergence)
lea rdi, [rip + @SA]
lea rsi, [rip + @SD]
mov edx, 3
call @A_MEMCMP
test eax, eax
jne .f8
inc r15
.f8:
; --- MEMCPY (3 vecteurs) — v9 : motif 16 octets ---
mov edi, 16
mov esi, 8
call @A_ZONE_ALLOC
mov r14, rax
mov rdi, r14
lea rsi, [rip + @MOTIF16]
mov edx, 16
call @A_MEMCPY
mov rdi, r14
lea rsi, [rip + @MOTIF16]
mov edx, 16
call @A_MEMCMP
test eax, eax
jne .f9
inc r15
.f9:
; v10 : longueur nulle sur sentinelle (la sentinelle posée, n=0 ne touche RIEN)
mov edi, 16
mov esi, 8
call @A_ZONE_ALLOC
mov r14, rax
mov rdi, r14
lea rsi, [rip + @SENT16]
mov edx, 16
call @A_MEMCPY
mov rdi, r14
lea rsi, [rip + @MOTIF16]
xor edx, edx
call @A_MEMCPY
mov rdi, r14
lea rsi, [rip + @SENT16]
mov edx, 16
call @A_MEMCMP
test eax, eax
jne .f10
inc r15
.f10:
; v11 : motif 33 octets
mov edi, 48
mov esi, 8
call @A_ZONE_ALLOC
mov r14, rax
mov rdi, r14
lea rsi, [rip + @MOTIF33]
mov edx, 33
call @A_MEMCPY
mov rdi, r14
lea rsi, [rip + @MOTIF33]
mov edx, 33
call @A_MEMCMP
test eax, eax
jne .f11
inc r15
.f11:
; --- STRLEN (3 vecteurs) — v12 : chaîne vide ---
lea rdi, [rip + @S_VIDE]
call @A_STRLEN
test rax, rax
jne .f12
inc r15
.f12:
; v13 : "TRIADE" -> 6
lea rdi, [rip + @S_TRIADE]
call @A_STRLEN
cmp rax, 6
jne .f13
inc r15
.f13:
; v14 : 33 lettres -> 33
lea rdi, [rip + @S_33]
call @A_STRLEN
cmp rax, 33
jne .f14
inc r15
.f14:
; --- ITOA (4 vecteurs) — v15 : 0 -> "0" ---
xor edi, edi
lea rsi, [rsp]
call @A_ITOA
lea rdi, [rsp]
lea rsi, [rip + @I0]
mov edx, 2
call @A_MEMCMP
test eax, eax
jne .f15
inc r15
.f15:
; v16 : 4294967295 -> "4294967295"
mov edi, 0xFFFFFFFF
lea rsi, [rsp]
call @A_ITOA
lea rdi, [rsp]
lea rsi, [rip + @IMAX]
mov edx, 11
call @A_MEMCMP
test eax, eax
jne .f16
inc r15
.f16:
; v17 : 1234567890 -> "1234567890"
mov edi, 1234567890
lea rsi, [rsp]
call @A_ITOA
lea rdi, [rsp]
lea rsi, [rip + @I123]
mov edx, 11
call @A_MEMCMP
test eax, eax
jne .f17
inc r15
.f17:
; v18 : 7 -> "7"
mov edi, 7
lea rsi, [rsp]
call @A_ITOA
lea rdi, [rsp]
lea rsi, [rip + @I7]
mov edx, 2
call @A_MEMCMP
test eax, eax
jne .f18
inc r15
.f18:
; --- MEMSET (3 vecteurs) — v19 : zéros sur 16 octets ---
mov edi, 16
mov esi, 8
call @A_ZONE_ALLOC
mov r14, rax
mov rdi, r14
xor esi, esi
mov edx, 16
call @A_MEMSET
mov rdi, r14
lea rsi, [rip + @ZERO16]
mov edx, 16
call @A_MEMCMP
test eax, eax
jne .f19
inc r15
.f19:
; v20 : 0xFF sur 33 octets
mov edi, 48
mov esi, 8
call @A_ZONE_ALLOC
mov r14, rax
mov rdi, r14
mov esi, 0xFF
mov edx, 33
call @A_MEMSET
mov rdi, r14
lea rsi, [rip + @FF33]
mov edx, 33
call @A_MEMCMP
test eax, eax
jne .f20
inc r15
.f20:
; v21 : longueur nulle sur sentinelle (n=0 ne touche RIEN)
mov edi, 16
mov esi, 8
call @A_ZONE_ALLOC
mov r14, rax
mov rdi, r14
lea rsi, [rip + @SENT16]
mov edx, 16
call @A_MEMCPY
mov rdi, r14
mov esi, 0xFF
xor edx, edx
call @A_MEMSET
mov rdi, r14
lea rsi, [rip + @SENT16]
mov edx, 16
call @A_MEMCMP
test eax, eax
jne .f21
inc r15
.f21:
; --- VERDICT : composer la ligne du patrimoine, l'émettre, rendre N ---
; le tampon ligne dans l'arène, en phase de verdict (I5)
mov edi, 64
mov esi, 8
call @A_ZONE_ALLOC
mov rbx, rax
xor r12, r12
mov rdi, rbx
lea rsi, [rip + @PREFIXE]
mov edx, 21
call @A_MEMCPY
add r12, 21
mov edi, r15d
lea rsi, [rsp]
call @A_ITOA
lea rdi, [rsp]
call @A_STRLEN
mov r14, rax
lea rdi, [rbx + r12]
lea rsi, [rsp]
mov rdx, r14
call @A_MEMCPY
add r12, r14
; le séparateur puis le TOTAL (la ligne du patrimoine : N/21 — le m1
; émettait "/" puis itoa(21), la forme exacte de Q2)
lea rdi, [rbx + r12]
lea rsi, [rip + @SLASH]
mov edx, 1
call @A_MEMCPY
inc r12
mov edi, 21
lea rsi, [rsp]
call @A_ITOA
lea rdi, [rsp]
call @A_STRLEN
mov r14, rax
lea rdi, [rbx + r12]
lea rsi, [rsp]
mov rdx, r14
call @A_MEMCPY
add r12, r14
lea rdi, [rbx + r12]
lea rsi, [rip + @OK]
cmp r15, 21
je .verdict_ok
lea rsi, [rip + @KO]
.verdict_ok:
mov edx, 4
call @A_MEMCPY
add r12, 4
mov edi, 1
mov rsi, rbx
mov rdx, r12
call @A_ECRIRE
mov rax, r15
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
