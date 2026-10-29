; tls-01 · hôte span → UTF-16 · spec tls-01:R1 · bornes AVANT toute écriture
; pre : rcx = hôte (octets réseau), rdx = longueur, r8 = destination (capacité 512)
; post : rax 0 = écrit UTF-16LE + mot NUL, rdx = 2*(longueur+1) ;
;        rax 1 = longueur 0 ou > HOTE_MAX 255 (rien écrit) ;
;        rax 2 = octet >= 0x80 (IDNA hors périmètre — rien écrit)
; Le balayage d'encodage précède TOUTE écriture (I2) ; feuille pure (I1) ;
; volatils seuls : rax rcx rdx r8 r9 r10 (I4)
test rdx, rdx
je .refus_longueur
cmp rdx, 255
ja .refus_longueur
xor r9d, r9d
.balaye:
cmp r9, rdx
jae .ascii
test byte ptr [rcx + r9], 0x80
jnz .refus_encodage
add r9, 1
jmp .balaye
.ascii:
xor r9d, r9d
.ecrit:
cmp r9, rdx
jae .termine
movzx r10d, byte ptr [rcx + r9]
mov word ptr [r8 + r9*2], r10w
add r9, 1
jmp .ecrit
.termine:
mov word ptr [r8 + r9*2], 0
lea rdx, [rdx + rdx]
add rdx, 2
xor eax, eax
ret
.refus_longueur:
mov eax, 1
ret
.refus_encodage:
mov eax, 2
ret
