; le corridor des ONZE gardes OS (k69mvt43j, la vague 15) — le
; modele OPT-01 PROMU EN CORRIDOR REEL a la marge vierge 0xFC00 :
; R4/R7 PRESERVES (aucune adresse scellee ne bouge — les scelles
; 0xDF00/0xDFC0, les couloirs 0xE200-0xEA00/0xF300/0xF800 INTACTS).
; ABI (msx64) : rcx = l'index de la garde (0..10), r9 = la face
; effective de l'acces (le miroir du fichier de garde v14 : les
; gardes sys lisent [r9]) ; rax = 0 l'admission, -5 le refus de
; frontiere NOMME, -2 LA FACE D'INDEX (l'index hors [0,11)).
cmp rcx, 11
jae .refus_index
cmp rcx, 0
jne .passe_0
jmp .garde_0
.passe_0:
cmp rcx, 1
jne .passe_1
jmp .garde_1
.passe_1:
cmp rcx, 2
jne .passe_2
jmp .garde_2
.passe_2:
cmp rcx, 3
jne .passe_3
jmp .garde_3
.passe_3:
cmp rcx, 4
jne .passe_4
jmp .garde_4
.passe_4:
cmp rcx, 5
jne .passe_5
jmp .garde_5
.passe_5:
cmp rcx, 6
jne .passe_6
jmp .garde_6
.passe_6:
cmp rcx, 7
jne .passe_7
jmp .garde_7
.passe_7:
cmp rcx, 8
jne .passe_8
jmp .garde_8
.passe_8:
cmp rcx, 9
jne .passe_9
jmp .garde_9
.passe_9:
cmp rcx, 10
jne .passe_10
jmp .garde_10
.passe_10:
; sys-02-41073 — la zone OS [0x500000, 0x501000)
.garde_0:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41086 — la zone OS [0x500000, 0x501000)
.garde_1:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41130 — la zone OS [0x500000, 0x501000)
.garde_2:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41138 — la zone OS [0x500000, 0x501000)
.garde_3:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41149 — la zone OS [0x500000, 0x501000)
.garde_4:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41203 — la zone OS [0x500000, 0x501000)
.garde_5:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41216 — la zone OS [0x500000, 0x501000)
.garde_6:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41226 — la zone OS [0x500000, 0x501000)
.garde_7:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41239 — la zone OS [0x500000, 0x501000)
.garde_8:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41247 — la zone OS [0x500000, 0x501000)
.garde_9:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
; sys-02-41255 — la zone OS [0x500000, 0x501000)
.garde_10:
mov rax, r9
cmp rax, 5242880
jb .refus_garde
cmp rax, 5246976
jae .refus_garde
xor eax, eax
ret
.refus_garde:
mov eax, 0xfffffffb
ret
.refus_index:
mov rax, 0xfffffffffffffffe
ret
