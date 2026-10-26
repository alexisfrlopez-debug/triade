; win-04-procedure · bloc démo · spec win-04:R4 · bloc carte d40004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1640, taille 896 octets
; Dépendances : IAT user32 : CreateWindowExW, SendMessageW, GetStockObject (gdi32), GetClientRect, MoveWindow, EnableWindow, DestroyWindow, PostQuitMessage, DefWindowProcW, GetModuleHandleW ; IAT kernel32 : CloseHandle, GetLastError ; bloc win-05 (miroir écran+fichier + diagnostics L4C/L4D) ; tcp-06 spawn @0x4300 ; scénario @0x4C00 ; état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/win-04-procedure.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 876 o · padding : 20 o (NOP)
; Étiquettes résolues : .creer=0x168a, .edit_ok=0x1725, .bouton_ok=0x17b5, .taille=0x1814, .commande=0x18ce, .thread_ok=0x1966, .zero=0x196f, .fermer=0x1973, .detruire=0x1980, .defaut=0x198c, .sortie=0x199e
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x168c + 0x6 + 0xa6e = 0x2100
;   0x1697 + 0x7 + 0x139c = 0x2a3a
;   0x169e + 0x7 + 0x13ad = 0x2a52
;   0x16e7 + 0x6 + 0x111b = 0x2808
;   0x16ed + 0x7 + 0x2174 = 0x3868
;   0x16f9 + 0x6 + 0x1799 = 0x2e98
;   0x1702 + 0x7 + 0x184c = 0x2f55
;   0x1727 + 0x7 + 0x1316 = 0x2a44
;   0x172e + 0x7 + 0x12e9 = 0x2a1e
;   0x1777 + 0x6 + 0x108b = 0x2808
;   0x177d + 0x7 + 0x20ec = 0x3870
;   0x1789 + 0x6 + 0x1709 = 0x2e98
;   0x1792 + 0x7 + 0x17e7 = 0x2f80
;   0x17ba + 0x6 + 0x11c0 = 0x2980
;   0x17c3 + 0x7 + 0x209e = 0x3868
;   0x17d8 + 0x6 + 0x1062 = 0x2840
;   0x17de + 0x7 + 0x208b = 0x3870
;   0x17f3 + 0x6 + 0x1047 = 0x2840
;   0x17f9 + 0x7 + 0x1710 = 0x2f10
;   0x181c + 0x6 + 0x103e = 0x2860
;   0x182c + 0x7 + 0x2035 = 0x3868
;   0x1857 + 0x6 + 0xffb = 0x2858
;   0x1860 + 0x7 + 0x2009 = 0x3870
;   0x188a + 0x6 + 0xfc8 = 0x2858
;   0x1893 + 0x7 + 0x1743 = 0x2fdd
;   0x18ad + 0x7 + 0x173a = 0x2fee
;   0x18d8 + 0x8 + 0x1f98 = 0x3878
;   0x18e6 + 0xb + 0x1f87 = 0x3878
;   0x18f1 + 0x7 + 0x163d = 0x2f35
;   0x1905 + 0x7 + 0x1f64 = 0x3870
;   0x190e + 0x6 + 0xf3c = 0x2850
;   0x1914 + 0x7 + 0x32e5 = 0x4c00
;   0x1927 + 0x6 + 0x156b = 0x2e98
;   0x1930 + 0x7 + 0x166c = 0x2fa3
;   0x1947 + 0xb + 0x1f26 = 0x3878
;   0x1952 + 0x7 + 0x1f17 = 0x3870
;   0x195e + 0x6 + 0xeec = 0x2850
;   0x1969 + 0x6 + 0x789 = 0x20f8
;   0x1976 + 0x6 + 0xebc = 0x2838
;   0x1982 + 0x6 + 0xea8 = 0x2830
;   0x1998 + 0x6 + 0xe72 = 0x2810
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
cmp edx, 1
je 0x168a
cmp edx, 5
je 0x1814
cmp edx, 0x111
je 0x18ce
cmp edx, 0x10
je 0x1973
cmp edx, 2
je 0x1980
jmp 0x198c
xor ecx, ecx
call qword ptr [rip + 0xa6e]
mov r15, rax
xor ecx, ecx
lea rdx, [rip + 0x139c]
lea r8, [rip + 0x13ad]
mov r9d, 0x50200844
mov dword ptr [rsp + 0x20], 8
mov dword ptr [rsp + 0x28], 8
mov dword ptr [rsp + 0x30], 716
mov dword ptr [rsp + 0x38], 380
mov qword ptr [rsp + 0x40], rbx
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r15
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + 0x111b]
mov qword ptr [rip + 0x2174], rax
test rax, rax
jne 0x1725
call qword ptr [rip + 0x1799]
mov r9d, eax
lea rcx, [rip + 0x184c]
mov edx, 43
mov r8d, 1
call 0x5000
mov rax, 0xFFFFFFFFFFFFFFFF
jmp 0x199e
xor ecx, ecx
lea rdx, [rip + 0x1316]
lea r8, [rip + 0x12e9]
mov r9d, 0x50000001
mov dword ptr [rsp + 0x20], 8
mov dword ptr [rsp + 0x28], 396
mov dword ptr [rsp + 0x30], 716
mov dword ptr [rsp + 0x38], 36
mov qword ptr [rsp + 0x40], rbx
mov qword ptr [rsp + 0x48], 1
mov qword ptr [rsp + 0x50], r15
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + 0x108b]
mov qword ptr [rip + 0x20ec], rax
test rax, rax
jne 0x17b5
call qword ptr [rip + 0x1709]
mov r9d, eax
lea rcx, [rip + 0x17e7]
mov edx, 35
mov r8d, 1
call 0x5000
mov rax, 0xFFFFFFFFFFFFFFFF
jmp 0x199e
mov ecx, 17
call qword ptr [rip + 0x11c0]
mov r12, rax
mov rcx, qword ptr [rip + 0x209e]
mov edx, 0x30
mov r8, r12
mov r9d, 1
call qword ptr [rip + 0x1062]
mov rcx, qword ptr [rip + 0x208b]
mov edx, 0x30
mov r8, r12
mov r9d, 1
call qword ptr [rip + 0x1047]
lea rcx, [rip + 0x1710]
mov edx, 37
xor r8d, r8d
call 0x5000
xor eax, eax
jmp 0x199e
mov rcx, rbx
lea rdx, [rsp + 0x20]
call qword ptr [rip + 0x103e]
mov r14d, dword ptr [rsp + 0x28]
mov r15d, dword ptr [rsp + 0x2C]
mov rcx, qword ptr [rip + 0x2035]
mov edx, 8
mov r8d, 8
mov r9d, r14d
sub r9d, 16
mov dword ptr [rsp + 0x20], r15d
sub dword ptr [rsp + 0x20], 56
mov dword ptr [rsp + 0x28], 1
call qword ptr [rip + 0xffb]
mov r12d, eax
mov rcx, qword ptr [rip + 0x2009]
mov edx, 8
mov r8d, r15d
sub r8d, 44
mov r9d, r14d
sub r9d, 16
mov dword ptr [rsp + 0x20], 36
mov dword ptr [rsp + 0x28], 1
call qword ptr [rip + 0xfc8]
mov r13d, eax
lea rcx, [rip + 0x1743]
mov edx, 17
mov r8d, 1
mov r9d, r12d
call 0x5000
lea rcx, [rip + 0x173a]
mov edx, 16
mov r8d, 1
mov r9d, r13d
call 0x5000
xor eax, eax
jmp 0x199e
cmp r13d, 1
jne 0x196f
cmp qword ptr [rip + 0x1f98], 0
jne 0x196f
mov qword ptr [rip + 0x1f87], 1
lea rcx, [rip + 0x163d]
mov edx, 32
xor r8d, r8d
call 0x5000
mov rcx, qword ptr [rip + 0x1f64]
xor edx, edx
call qword ptr [rip + 0xf3c]
lea rcx, [rip + 0x32e5]
xor edx, edx
call 0x4300
test rax, rax
jne 0x1966
call qword ptr [rip + 0x156b]
mov r9d, eax
lea rcx, [rip + 0x166c]
mov edx, 41
mov r8d, 1
call 0x5000
mov qword ptr [rip + 0x1f26], 0
mov rcx, qword ptr [rip + 0x1f17]
mov edx, 1
call qword ptr [rip + 0xeec]
jmp 0x196f
mov rcx, rax
call qword ptr [rip + 0x789]
xor eax, eax
jmp 0x199e
mov rcx, rbx
call qword ptr [rip + 0xebc]
xor eax, eax
jmp 0x199e
xor ecx, ecx
call qword ptr [rip + 0xea8]
xor eax, eax
jmp 0x199e
mov rcx, rbx
mov rdx, r12
mov r8, r13
mov r9, r14
call qword ptr [rip + 0xe72]
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
