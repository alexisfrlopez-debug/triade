; horodatage du run : TAMPON_NOM = "terrain_YYYYMMDD_HHMMSS.txt\0" (27+NUL)
; et TAMPON_AFF = "S01 date YYYYMMDD_HHMMSS" (24 o, la meme lecture de
; l'heure sert les deux compositions — I3) ; chiffres par division binaire
; inline (I1 : itoa scelle formate un i32 signe, pas un u16 zero-paddé) ;
; l'annee en deux paires par division 100, les autres champs par .deux
; (division 10) ; rax = 24
push rbx
sub rsp, 0x30
lea rcx, [rsp + 0x20]
call qword ptr [rip + IAT_LOCALTIME]
lea rbx, [rip + TAMPON_NOM]
movabs rax, 0x5f6e696172726574
mov qword ptr [rbx], rax
add rbx, 8
movzx eax, word ptr [rsp + 0x20]
xor edx, edx
mov ecx, 100
div ecx
mov r8d, edx
call .deux
mov eax, r8d
call .deux
movzx eax, word ptr [rsp + 0x22]
call .deux
movzx eax, word ptr [rsp + 0x26]
call .deux
mov byte ptr [rbx], 0x5F
inc rbx
movzx eax, word ptr [rsp + 0x28]
call .deux
movzx eax, word ptr [rsp + 0x2A]
call .deux
movzx eax, word ptr [rsp + 0x2C]
call .deux
mov qword ptr [rbx], 0x7478742e
lea rcx, [rip + TAMPON_AFF]
movabs rax, 0x6574616420313053
mov qword ptr [rcx], rax
mov byte ptr [rcx + 8], 0x20
add rcx, 9
lea rdx, [rbx - 15]
mov r8d, 15
call MEMCPY
mov eax, 24
add rsp, 0x30
pop rbx
ret
.deux:
xor edx, edx
xor ecx, ecx
mov cl, 10
div ecx
mov ah, dl
add ax, 0x3030
mov word ptr [rbx], ax
add rbx, 2
ret
