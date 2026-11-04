; tcp-11-journal-v2 · brouillon étiqueté — le REMPLAÇANT du journal (staging)
; PAS un bloc placé : assemblé POUR l'adresse de croissance 0x1D80, ses
; octets vivront au staging (.rodata, 0x300) et seront copiés dans la
; croissance par tcp-07 — la cible du patch est l'ENTRÉE DU JOURNAL v1
; (0x1840), la démonstration M5-(c) du chantier (d) : la politique
; d'écriture du journal basculera PENDANT le trafic.
; La SEULE différence au v1 : la ligne composée porte la MARQUE "j2: "
; (4 o, .rodata 0x2B0) en tête — la bascule est OBSERVABLE (l'entrée
; appelée rend le comportement du remplaçant, tcp-07:R4 V2). Le contrat
; demeure tcp-11:R2 (même verrou, même composition, une seule écriture) ;
; le tampon gagne la marque (64 + 4 -> cadre 0x60). Les appels internes
; partent de la croissance vers les blocs du corpus : leurs rel32 sont
; résolus POUR 0x1D80 — c'est la raison d'être de CE brouillon séparé.
@A_MEMCPY = 0x1080
@A_ITOA = 0x1180
@A_STRLEN = 0x1140
@A_ECRIRE = 0x1000
@VERROU = 0x3800
@J2_MARK = 0x2B0
@SENTINELLE = 0xFFFFFFFF
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
mov rbx, rdi
mov r12, rsi
mov r13, rdx
mov r14, rcx
mov r15, r8
; --- prendre le verrou ---
mov esi, 1
.reattendre:
xchg rsi, qword ptr [rip + @VERROU]
test rsi, rsi
jz .acquis
pause
jmp .reattendre
.acquis:
; --- la marque du remplaçant (la différence v2, en tête) ---
mov rdi, rsp
lea rsi, [rip + @J2_MARK]
mov edx, 4
call @A_MEMCPY
; --- le préfixe, à partir de l'offset 4 ---
lea rdi, [rsp + 4]
mov rsi, rbx
mov rdx, r12
call @A_MEMCPY
lea r12, [r12 + 4]
; --- le champ numérique (sentinelle : pas de champ) ---
cmp r13d, @SENTINELLE
je .sans_champ
mov edi, r13d
lea rsi, [rsp + 0x44]
call @A_ITOA
lea rdi, [rsp + 0x44]
call @A_STRLEN
lea rdi, [rsp]
add rdi, r12
lea rsi, [rsp + 0x44]
mov rdx, rax
; la longueur est capturée AVANT l'appel : memcpy rend dst (une adresse), jamais la longueur
add r12, rax
call @A_MEMCPY
.sans_champ:
; --- le suffixe ---
lea rdi, [rsp]
add rdi, r12
mov rsi, r14
mov rdx, r15
call @A_MEMCPY
add r12, r15
; --- UNE écriture, le verdict brut conservé ---
mov edi, 1
mov rsi, rsp
mov rdx, r12
call @A_ECRIRE
mov r14, rax
; --- rendre le verrou, puis le verdict (jamais l'inverse) ---
mov qword ptr [rip + @VERROU], 0
mov rax, r14
add rsp, 0x60
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
