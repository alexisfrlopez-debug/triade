; win-04-procedure · bloc démo · spec win-04:R1 · bloc carte d40004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1600, taille 704 octets
; Dépendances : IAT user32 : CreateWindowExW, SendMessageW, GetStockObject (gdi32), GetClientRect, MoveWindow, EnableWindow, DestroyWindow, PostQuitMessage, DefWindowProcW, GetModuleHandleW ; IAT kernel32 : CloseHandle ; tcp-06 spawn @0x4300 ; scénario @0x1C40 ; état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/win-04-procedure.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 645 o · padding : 59 o (NOP)
; Étiquettes résolues : .creer=0x164a, .taille=0x175e, .commande=0x17e3, .thread_ok=0x183f, .zero=0x1848, .fermer=0x184c, .detruire=0x1859, .defaut=0x1865, .sortie=0x1877
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x164c + 0x6 + 0xaae = 0x2100
;   0x1657 + 0x7 + 0x13dc = 0x2a3a
;   0x165e + 0x7 + 0x13ed = 0x2a52
;   0x16a7 + 0x6 + 0x115b = 0x2808
;   0x16ad + 0x7 + 0x21b4 = 0x3868
;   0x16b6 + 0x7 + 0x1387 = 0x2a44
;   0x16bd + 0x7 + 0x135a = 0x2a1e
;   0x1706 + 0x6 + 0x10fc = 0x2808
;   0x170c + 0x7 + 0x215d = 0x3870
;   0x1718 + 0x6 + 0x1262 = 0x2980
;   0x1721 + 0x7 + 0x2140 = 0x3868
;   0x1736 + 0x6 + 0x1104 = 0x2840
;   0x173c + 0x7 + 0x212d = 0x3870
;   0x1751 + 0x6 + 0x10e9 = 0x2840
;   0x1766 + 0x6 + 0x10f4 = 0x2860
;   0x1776 + 0x7 + 0x20eb = 0x3868
;   0x17a6 + 0x6 + 0x10ac = 0x2858
;   0x17ac + 0x7 + 0x20bd = 0x3870
;   0x17d6 + 0x6 + 0x107c = 0x2858
;   0x17e9 + 0x8 + 0x2087 = 0x3878
;   0x17f3 + 0xb + 0x207a = 0x3878
;   0x17fe + 0x7 + 0x206b = 0x3870
;   0x1807 + 0x6 + 0x1043 = 0x2850
;   0x180d + 0x7 + 0x46c = 0x1c80
;   0x1820 + 0xb + 0x204d = 0x3878
;   0x182b + 0x7 + 0x203e = 0x3870
;   0x1837 + 0x6 + 0x1013 = 0x2850
;   0x1842 + 0x6 + 0x8b0 = 0x20f8
;   0x184f + 0x6 + 0xfe3 = 0x2838
;   0x185b + 0x6 + 0xfcf = 0x2830
;   0x1871 + 0x6 + 0xf99 = 0x2810
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
je 0x164a
cmp edx, 5
je 0x175e
cmp edx, 0x111
je 0x17e3
cmp edx, 0x10
je 0x184c
cmp edx, 2
je 0x1859
jmp 0x1865
xor ecx, ecx
call qword ptr [rip + 0xaae]
mov r15, rax
xor ecx, ecx
lea rdx, [rip + 0x13dc]
lea r8, [rip + 0x13ed]
mov r9d, 0x50200844
mov dword ptr [rsp + 0x20], 8
mov dword ptr [rsp + 0x28], 8
mov dword ptr [rsp + 0x30], 716
mov dword ptr [rsp + 0x38], 380
mov qword ptr [rsp + 0x40], rbx
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r15
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + 0x115b]
mov qword ptr [rip + 0x21b4], rax
xor ecx, ecx
lea rdx, [rip + 0x1387]
lea r8, [rip + 0x135a]
mov r9d, 0x50000001
mov dword ptr [rsp + 0x20], 8
mov dword ptr [rsp + 0x28], 396
mov dword ptr [rsp + 0x30], 716
mov dword ptr [rsp + 0x38], 36
mov qword ptr [rsp + 0x40], rbx
mov qword ptr [rsp + 0x48], 1
mov qword ptr [rsp + 0x50], r15
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + 0x10fc]
mov qword ptr [rip + 0x215d], rax
mov ecx, 17
call qword ptr [rip + 0x1262]
mov r12, rax
mov rcx, qword ptr [rip + 0x2140]
mov edx, 0x30
mov r8, r12
mov r9d, 1
call qword ptr [rip + 0x1104]
mov rcx, qword ptr [rip + 0x212d]
mov edx, 0x30
mov r8, r12
mov r9d, 1
call qword ptr [rip + 0x10e9]
xor eax, eax
jmp 0x1877
mov rcx, rbx
lea rdx, [rsp + 0x20]
call qword ptr [rip + 0x10f4]
mov r10d, dword ptr [rsp + 0x24]
mov r11d, dword ptr [rsp + 0x2C]
mov rcx, qword ptr [rip + 0x20eb]
mov edx, 8
mov r8d, 8
mov r9d, r10d
sub r9d, 16
mov dword ptr [rsp + 0x20], r11d
mov dword ptr [rsp + 0x28], r11d
sub dword ptr [rsp + 0x28], 56
mov dword ptr [rsp + 0x30], 1
call qword ptr [rip + 0x10ac]
mov rcx, qword ptr [rip + 0x20bd]
mov edx, 8
mov r8d, r11d
sub r8d, 44
mov r9d, r10d
sub r9d, 16
mov dword ptr [rsp + 0x20], 36
mov dword ptr [rsp + 0x28], 1
call qword ptr [rip + 0x107c]
xor eax, eax
jmp 0x1877
cmp r13d, 1
jne 0x1848
cmp qword ptr [rip + 0x2087], 0
jne 0x1848
mov qword ptr [rip + 0x207a], 1
mov rcx, qword ptr [rip + 0x206b]
xor edx, edx
call qword ptr [rip + 0x1043]
lea rcx, [rip + 0x46c]
xor edx, edx
call 0x4300
test rax, rax
jne 0x183f
mov qword ptr [rip + 0x204d], 0
mov rcx, qword ptr [rip + 0x203e]
mov edx, 1
call qword ptr [rip + 0x1013]
jmp 0x1848
mov rcx, rax
call qword ptr [rip + 0x8b0]
xor eax, eax
jmp 0x1877
mov rcx, rbx
call qword ptr [rip + 0xfe3]
xor eax, eax
jmp 0x1877
xor ecx, ecx
call qword ptr [rip + 0xfcf]
xor eax, eax
jmp 0x1877
mov rcx, rbx
mov rdx, r12
mov r8, r13
mov r9, r14
call qword ptr [rip + 0xf99]
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
