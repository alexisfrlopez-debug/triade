; win-04-procedure · bloc démo · spec win-04:R2 · bloc carte d40004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1640, taille 896 octets
; Dépendances : IAT user32 : CreateWindowExW, SendMessageW, GetStockObject (gdi32), GetClientRect, MoveWindow, EnableWindow, DestroyWindow, PostQuitMessage, DefWindowProcW, GetModuleHandleW ; IAT kernel32 : CloseHandle, GetLastError ; bloc win-11 (trace) ; tcp-06 spawn @0x4300 ; scénario @0x4C00 ; état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/win-04-procedure.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 818 o · padding : 78 o (NOP)
; Étiquettes résolues : .creer=0x168a, .edit_ok=0x1725, .bouton_ok=0x17b5, .taille=0x1814, .commande=0x1894, .thread_ok=0x192c, .zero=0x1935, .fermer=0x1939, .detruire=0x1946, .defaut=0x1952, .sortie=0x1964
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
;   0x185d + 0x7 + 0x200c = 0x3870
;   0x1887 + 0x6 + 0xfcb = 0x2858
;   0x189e + 0x8 + 0x1fd2 = 0x3878
;   0x18ac + 0xb + 0x1fc1 = 0x3878
;   0x18b7 + 0x7 + 0x1677 = 0x2f35
;   0x18cb + 0x7 + 0x1f9e = 0x3870
;   0x18d4 + 0x6 + 0xf76 = 0x2850
;   0x18da + 0x7 + 0x331f = 0x4c00
;   0x18ed + 0x6 + 0x15a5 = 0x2e98
;   0x18f6 + 0x7 + 0x16a6 = 0x2fa3
;   0x190d + 0xb + 0x1f60 = 0x3878
;   0x1918 + 0x7 + 0x1f51 = 0x3870
;   0x1924 + 0x6 + 0xf26 = 0x2850
;   0x192f + 0x6 + 0x7c3 = 0x20f8
;   0x193c + 0x6 + 0xef6 = 0x2838
;   0x1948 + 0x6 + 0xee2 = 0x2830
;   0x195e + 0x6 + 0xeac = 0x2810
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
je 0x1894
cmp edx, 0x10
je 0x1939
cmp edx, 2
je 0x1946
jmp 0x1952
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
call 0x1e00
mov rax, 0xFFFFFFFFFFFFFFFF
jmp 0x1964
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
call 0x1e00
mov rax, 0xFFFFFFFFFFFFFFFF
jmp 0x1964
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
call 0x1e00
xor eax, eax
jmp 0x1964
mov rcx, rbx
lea rdx, [rsp + 0x20]
call qword ptr [rip + 0x103e]
mov r10d, dword ptr [rsp + 0x28]
mov r11d, dword ptr [rsp + 0x2C]
mov rcx, qword ptr [rip + 0x2035]
mov edx, 8
mov r8d, 8
mov r9d, r10d
sub r9d, 16
mov dword ptr [rsp + 0x20], r11d
sub dword ptr [rsp + 0x20], 56
mov dword ptr [rsp + 0x28], 1
call qword ptr [rip + 0xffb]
mov rcx, qword ptr [rip + 0x200c]
mov edx, 8
mov r8d, r11d
sub r8d, 44
mov r9d, r10d
sub r9d, 16
mov dword ptr [rsp + 0x20], 36
mov dword ptr [rsp + 0x28], 1
call qword ptr [rip + 0xfcb]
xor eax, eax
jmp 0x1964
cmp r13d, 1
jne 0x1935
cmp qword ptr [rip + 0x1fd2], 0
jne 0x1935
mov qword ptr [rip + 0x1fc1], 1
lea rcx, [rip + 0x1677]
mov edx, 32
xor r8d, r8d
call 0x1e00
mov rcx, qword ptr [rip + 0x1f9e]
xor edx, edx
call qword ptr [rip + 0xf76]
lea rcx, [rip + 0x331f]
xor edx, edx
call 0x4300
test rax, rax
jne 0x192c
call qword ptr [rip + 0x15a5]
mov r9d, eax
lea rcx, [rip + 0x16a6]
mov edx, 41
mov r8d, 1
call 0x1e00
mov qword ptr [rip + 0x1f60], 0
mov rcx, qword ptr [rip + 0x1f51]
mov edx, 1
call qword ptr [rip + 0xf26]
jmp 0x1935
mov rcx, rax
call qword ptr [rip + 0x7c3]
xor eax, eax
jmp 0x1964
mov rcx, rbx
call qword ptr [rip + 0xef6]
xor eax, eax
jmp 0x1964
xor ecx, ecx
call qword ptr [rip + 0xee2]
xor eax, eax
jmp 0x1964
mov rcx, rbx
mov rdx, r12
mov r8, r13
mov r9, r14
call qword ptr [rip + 0xeac]
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
