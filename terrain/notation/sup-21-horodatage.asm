; sup-21-horodatage · bloc terrain · spec sup-21:R1 · bloc carte f60021
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1c40, taille 256 octets
; Dépendances : IAT kernel32#3 : GetLocalTime ; bloc libc-01 memcpy ; état .data (TAMPON_NOM, TAMPON_AFF) ; chaîne S01_PREFIXE (zone données sup)
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-21-horodatage.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 209 o · padding : 47 o (NOP)
; Étiquettes résolues : .deux=0x1cfb
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1c4a + 0x6 + 0x6d8 = 0x2328
;   0x1c50 + 0x7 + 0x1e79 = 0x3ad0
;   0x1cc5 + 0x7 + 0x1e24 = 0x3af0
push rbx
sub rsp, 0x30
lea rcx, [rsp + 0x20]
call qword ptr [rip + 0x6d8]
lea rbx, [rip + 0x1e79]
movabs rax, 0x5f6e696172726574
mov qword ptr [rbx], rax
add rbx, 8
movzx eax, word ptr [rsp + 0x20]
xor edx, edx
mov ecx, 100
div ecx
mov r8d, edx
call 0x1cfb
mov eax, r8d
call 0x1cfb
movzx eax, word ptr [rsp + 0x22]
call 0x1cfb
movzx eax, word ptr [rsp + 0x26]
call 0x1cfb
mov byte ptr [rbx], 0x5F
inc rbx
movzx eax, word ptr [rsp + 0x28]
call 0x1cfb
movzx eax, word ptr [rsp + 0x2A]
call 0x1cfb
movzx eax, word ptr [rsp + 0x2C]
call 0x1cfb
mov qword ptr [rbx], 0x7478742e
lea rcx, [rip + 0x1e24]
movabs rax, 0x6574616420313053
mov qword ptr [rcx], rax
mov byte ptr [rcx + 8], 0x20
add rcx, 9
lea rdx, [rbx - 15]
mov r8d, 15
call 0x1100
mov eax, 24
add rsp, 0x30
pop rbx
ret
xor edx, edx
xor ecx, ecx
mov cl, 10
div ecx
mov ah, dl
add ax, 0x3030
mov word ptr [rbx], ax
add rbx, 2
ret
