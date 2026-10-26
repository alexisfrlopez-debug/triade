; hello-01 · bloc principal (point d'entrée) · spec hello-01:R1 · bloc carte a10001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1000, taille 64 octets
; Dépendances : a10002 (écriture, 0x1040), a10003 (sortie, 0x1080),
;               IAT[0] GetStdHandle (0x20B0)
; Layout fixe — les déplacements RIP sont calculés une fois pour toutes (R7) :
;   0x100F + 0x10A1 = 0x20B0 (IAT[0]) ; 0x1019 + 0x0FE7 = 0x2000 (message)
sub rsp, 0x28
mov ecx, -11
call qword ptr [rip + 0x10a1]
mov rcx, rax
lea rdx, [rip + 0xfe7]
mov r8d, 33
call 0x1040
xor ecx, ecx
call 0x1080
