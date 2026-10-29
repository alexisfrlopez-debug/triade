; http-11-console · brouillon · thread console du proxy · http-11:R1 · e50011
; réduit au minimum utile : « quit » pose le drapeau, ferme l'écoute (réveille
; l'acceptation de http-12) et journalise l'arrêt ; toute autre ligne est
; journalisée puis ignorée ; une console morte n'arrête PAS le serveur (Q3,
; miroir tcp-10) ; le thread meurt par ret — jamais ExitThread (Q4).
; appels : IAT kernel32 ReadFile ; tcp-05, tcp-11, libc-02 (comparaison exacte
; sur 6 octets reçus — I3 : jamais au-delà du rempli).
; entrée : rcx = 0 (argument opaque) ; stdin/listen/quit en .data (http-12)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x80
; cadre : [rsp,0x20) shadow ; &lus dword @0x28 ; tampon 64 o @ [0x40,0x80)
.boucle:
mov rcx, qword ptr [rip + STDIN]
lea rdx, [rsp + 0x40]
mov r8d, 64
lea r9, [rsp + 0x28]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_READFILE]
test eax, eax
je .fin
cmp dword ptr [rsp + 0x28], 0
je .fin
cmp dword ptr [rsp + 0x28], 6
jne .inconnu
lea rcx, [rsp + 0x40]
lea rdx, [rip + CMD_QUIT]
mov r8, 6
call MEMCMP
test eax, eax
jne .inconnu
mov dword ptr [rip + QUIT], 1
mov rcx, qword ptr [rip + LISTEN]
call TCP_CLOSE
lea rcx, [rip + MSG_ARRET]
mov edx, 7
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
jmp .fin
.inconnu:
lea rcx, [rip + MSG_INCONNU]
mov edx, 19
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
jmp .boucle
.fin:
add rsp, 0x80
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
