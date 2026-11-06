; tls13-28-socle-appel · brouillon étiqueté — spec tls13-28:R1, bloc carte h100028
; LA ROTULE — le seul point du domaine où le calcul touche le monde : UN
; contexte de DEUX rappels fournis par l'appelant (le kit), invoqués PAR
; POINTEUR DEPUIS LE CONTEXTE. L'appel indirect sur une cible qui est une
; DONNÉE du contexte n'est NI un import NI un syscall (I2 : l'oracle
; structurel du jalon le constatera — AUCUNE entrée IAT, AUCUN site
; syscall, UN appel indirect DÉCLARÉ — le seul du domaine, le socle EST la
; frontière nommée). Au harnais : le SIMULATEUR (les octets servis par
; fixtures — RFC 8448) ; au terrain : les sockets par SYSCALLS DIRECTS du
; domaine sys (sys-04+, le chantier (d) nommé par la couche I) — JAMAIS
; l'IAT ws2_32 (la surface de hook que M8 a nommée).
; L'OPÉRATION (P2) : rdx = 1 (émettre) ou 2 (recevoir), toute autre valeur
; → verdict -1 NOMMÉ. ÉMETTRE (Q1) : le rappel (ctx, r8, r9) invoqué — il
; rend 0 (tout émis) ou négatif ; le bloc rend 0 ou -7 NOMMÉ (transport en
; échec — la table du domaine). RECEVOIR (Q2) : le rappel invoqué — il
; rend n ≥ 0 (les octets lus, ≤ capacité) ou négatif ; le bloc rend n ou
; -7 NOMMÉ ; LE ZÉRO DE RÉCEPTION (la demi-fin) est le refus -7 du KIT,
; jamais une lecture vide silencieuse.
; L'ABI DES RAPPELS (Q3 — la frontière DU KIT) : msx64, rcx = le contexte
; du rappel, rdx = le pointeur, r8 = la longueur/capacité, rax = le
; verdict ; le kit garantit la RÉCEPTION TOTALE à l'émission (un envoi
; partiel est le refus du kit) et la LECTURE BLOQUANTE à la réception.
; AUCUNE copie, aucun tampon (Q4 — le socle est UN ADAPTATEUR : les octets
; appartiennent à l'appelant, charte § 6 : le bloc ne détient rien, pas
; même une mémoire de transport).
; Le temps constant n'a RIEN à sceller ici (I1 — le socle ne touche
; AUCUNE donnée secrète : il transporte des OCTETS, chiffrés ou publics ;
; les longueurs et verdicts du transport sont publics).
; LE CADRE : AUCUN (l'adaptateur — l'ombre du rappel est posée PAR le
; socle : sub rsp, 0x28 autour de l'appel indirect, l'entrée ≡ 8 → 8−0x28
; ≡ 0 (mod 16) au rappel) ; r10/r11 volatils, AUCUN non volatil touché.
; rcx = le contexte socle (32 o : émettre @ +0, ctx émettre @ +8, recevoir
; @ +16, ctx recevoir @ +24) · rdx = l'opération (1/2) · r8 = le pointeur
; de données · r9 = la longueur (émettre) ou la CAPACITÉ (recevoir) ·
; I2 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun état
; détenu (§ 6) ; aucun registre non volatil détruit ; NOP, 0x90 (§ 8).
test rcx, rcx
jz .refus_nul
cmp rdx, 1
je .emettre
cmp rdx, 2
je .recevoir
jmp .refus_op
.emettre:
test r8, r8
jz .refus_nul
mov r10, qword ptr [rcx]
test r10, r10
jz .refus_nul
mov r11, qword ptr [rcx + 8]
sub rsp, 0x28
mov rcx, r11
mov r11, r8
mov r8, r9
mov rdx, r11
call r10
add rsp, 0x28
test eax, eax
jz .ok
mov rax, -7
ret
.recevoir:
test r8, r8
jz .refus_nul
mov r10, qword ptr [rcx + 16]
test r10, r10
jz .refus_nul
mov r11, qword ptr [rcx + 24]
sub rsp, 0x28
mov rcx, r11
mov r11, r8
mov r8, r9
mov rdx, r11
call r10
add rsp, 0x28
test eax, eax
jle .refus_transport
ret
.ok:
xor eax, eax
ret
.refus_transport:
mov rax, -7
ret
.refus_nul:
mov rax, -1
ret
.refus_op:
mov rax, -1
ret
