; libc-09-zone-alloc-ts · bloc allocateur par zone thread-safe · spec libc-09:R1 · bloc carte c30012
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1440, taille 128 octets
; Dépendances : IAT kernel32 : Enter/LeaveCriticalSection ; bloc libc-05 @0x1300 ; données .data : CS (NON embarqué dans echo.exe)
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-09-zone-alloc-ts.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 58 o · padding : 70 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x144a + 0x7 + 0x23df = 0x3830
;   0x1451 + 0x6 + 0xc89 = 0x20e0
;   0x1465 + 0x7 + 0x23c4 = 0x3830
;   0x146c + 0x6 + 0xc76 = 0x20e8
sub rsp, 0x28
mov r10, rcx
mov r11, rdx
lea rcx, [rip + 0x23df]
call qword ptr [rip + 0xc89]
mov rcx, r10
mov rdx, r11
call 0x1300
mov r10, rax
lea rcx, [rip + 0x23c4]
call qword ptr [rip + 0xc76]
mov rax, r10
add rsp, 0x28
ret
