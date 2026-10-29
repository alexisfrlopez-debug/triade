; http-10-session · brouillon · session proxy (thread par connexion) · http-10:R3 · e50010
; servir UNE connexion de bout en bout : accumulation (http-06), parsing
; (http-01..08 — chaque octet non fiable a un verdict), trancher (requête
; ordinaire ou tunnel CONNECT), router (tcp-13), réécrire la ligne de requête
; (spans d'origine, en-têtes verbatim), pomper, clôturer — chaque socket fermée
; EXACTEMENT une fois, par CE thread, jamais ailleurs (Q5) ; les pompes ne
; ferment jamais (http-09:Q4), le corps de requête est relayé BORNÉ
; Content-Length par des boucles tcp-03/tcp-04 INLINE (R2 : http-09, à
; fermeture délimitée, est réservé au tunnel et au relais de réponse).
; cadre 0x7100 : accumulation 16 Kio @0, réécriture 12 Kio @0x4000, zones
; d'accueil @0x6F00+, variables @0x6FE0+ ; sockets en non-volatils
; (rbx cliente, r12 amont, r13 remplissage, r14 tête puis reste-corps,
; r15 Content-Length) ; assistants locaux .emettre/.copier (pile équilibrée),
; .pompe_amont = proc de thread (arg = amont<<32 | cliente, sockets <= 32 bits
; documenté Win64) ; handle de la pompe détachée fermé immédiatement (IAT
; CloseHandle — miroir tcp-12:I4, R2).
; entrée : rcx = socket cliente (transmise par tcp-06 depuis http-12)
; prologue R3 (Q0, D63) : un thread neuf n'a qu'UNE page de pile
; committée (commit PE 0x1000, guard page dessous) — le cadre 0x7100
; est étendu page par page AVANT le sub (probing, miroir __chkstk),
; sinon la première écriture au bas du cadre saute la guard et lève
; c00000fd (mort du processus entier — terrain 21:38). r10/rax volatils,
; rsp et rcx intacts.
push rbx
push r12
push r13
push r14
push r15
mov r10, 0xfffffffffffff000
.probe:
mov rax, qword ptr [rsp + r10]
sub r10, 0x1000
cmp r10, -0x7000
jge .probe
mov rax, qword ptr [rsp - 0x7100]
sub rsp, 0x7100
mov rbx, rcx
xor r12d, r12d
; journal « connexion entrante » (Q6 — délégué par http-12)
lea rcx, [rip + MSG_CONNEXION]
mov edx, 20
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
; --- accumulation (Q1) ---
xor r13d, r13d
.accumuler:
mov rcx, rsp
mov rdx, r13
call HTTP_TETE
test rax, rax
je .tete_complete
cmp rax, 2
je .repondre_431
cmp rax, 3
je .repondre_400
mov rcx, rbx
lea rdx, [rsp + r13]
mov r8, 0x4000
sub r8, r13
call TCP_RECV
test rax, rax
jle .fin
add r13, rax
jmp .accumuler
.tete_complete:
mov r14, rdx
; --- ligne de requête (Q2) ---
mov rcx, rsp
mov rdx, r14
xor r8d, r8d
call HTTP_LIGNE
mov qword ptr [rsp + 0x6FE0], r8
test rdx, rdx
je .repondre_400
mov rcx, rsp
lea r8, [rsp + 0x6F00]
call HTTP_REQUETE
test rax, rax
je .requete_ok
cmp rax, 1
je .repondre_501
cmp rax, 3
je .repondre_505
jmp .repondre_400
.requete_ok:
; --- en-têtes : Host, Content-Length, Transfer-Encoding ---
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
mov r11, r14
sub r11, r10
mov qword ptr [rsp + 0x6FE8], r11
lea r8, [rip + NOM_HOST]
mov r9, 4
mov rdx, r11
lea rax, [rsp + 0x6F40]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call HTTP_CHERCHER
add rsp, 0x30
mov qword ptr [rsp + 0x6FF0], rax
cmp rax, 2
je .repondre_400
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip + NOM_CL]
mov r9, 14
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F60]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call HTTP_CHERCHER
add rsp, 0x30
mov qword ptr [rsp + 0x6FF8], rax
cmp rax, 2
je .repondre_400
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip + NOM_TE]
mov r9, 17
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F80]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call HTTP_CHERCHER
add rsp, 0x30
mov qword ptr [rsp + 0x7000], rax
cmp rax, 2
je .repondre_400
; --- forme de la cible (http-08) ---
mov rcx, qword ptr [rsp + 0x6F18]
mov rdx, qword ptr [rsp + 0x6F20]
mov r8d, dword ptr [rsp + 0x6F00]
lea r9, [rsp + 0x6FB8]
call HTTP_CIBLE
test rax, rax
je .cible_ok
cmp rax, 3
je .repondre_501
jmp .repondre_400
.cible_ok:
; --- autorité (http-07 — échec avant l'entrée système, charte point 9) ---
mov eax, dword ptr [rsp + 0x6FB8]
cmp eax, 3
je .forme_autorite
cmp eax, 1
je .forme_absolue
cmp qword ptr [rsp + 0x6FF0], 0
je .origine_host
jmp .repondre_400
.origine_host:
mov rcx, qword ptr [rsp + 0x6F50]
mov rdx, qword ptr [rsp + 0x6F58]
mov r8d, 80
jmp .resoudre
.forme_absolue:
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 80
jmp .resoudre
.forme_autorite:
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
xor r8d, r8d
.resoudre:
lea r9, [rsp + 0x6FA0]
call HTTP_AUTORITE
test rax, rax
jne .repondre_400
; --- Transfer-Encoding présent (valeur non vide) -> 501 (refus honnête) ---
cmp qword ptr [rsp + 0x7000], 0
jne .sans_te
cmp qword ptr [rsp + 0x6F98], 0
je .sans_te
jmp .repondre_501
.sans_te:
; --- Content-Length : valide ou absente ; POST/PUT sans CL ni TE -> 411 ---
cmp qword ptr [rsp + 0x6FF8], 0
je .valider_cl
mov eax, dword ptr [rsp + 0x6F00]
cmp eax, 3
je .repondre_411
cmp eax, 4
je .repondre_411
xor r15d, r15d
jmp .trancher
.valider_cl:
mov rcx, qword ptr [rsp + 0x6F70]
mov rdx, qword ptr [rsp + 0x6F78]
call HTTP_NOMBRE
test rax, rax
jne .repondre_400
mov r15d, edx
.trancher:
cmp dword ptr [rsp + 0x6F00], 8
je .tunnel
; ============ requête ordinaire (Q4) ============
; --- connexion amont (tcp-13) : l'autorité résolue est dans la zone http-07 ---
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call TCP_CONNEXION
test rax, rax
je .repondre_502
mov r12, rax
; --- réécriture : méthode SP chemin SP version CRLF en-têtes-verbatim ---
; [rsp+0x7008] = octets écrits (compte depuis ZÉRO — la base 0x4000 n'est
; JAMAIS ré-additionnée : dest = rsp+0x4000+compteur)
mov qword ptr [rsp + 0x7008], 0
mov rdx, qword ptr [rsp + 0x6F08]
mov r8, qword ptr [rsp + 0x6F10]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call .copier
mov rax, qword ptr [rsp + 0x6F10]
add qword ptr [rsp + 0x7008], rax
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov byte ptr [rcx], 0x20
add qword ptr [rsp + 0x7008], 1
mov rdx, qword ptr [rsp + 0x6FD0]
mov r8, qword ptr [rsp + 0x6FD8]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call .copier
mov rax, qword ptr [rsp + 0x6FD8]
add qword ptr [rsp + 0x7008], rax
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov byte ptr [rcx], 0x20
add qword ptr [rsp + 0x7008], 1
mov rdx, qword ptr [rsp + 0x6F28]
mov r8, qword ptr [rsp + 0x6F30]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call .copier
mov rax, qword ptr [rsp + 0x6F30]
add qword ptr [rsp + 0x7008], rax
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov word ptr [rcx], 0x0A0D
add qword ptr [rsp + 0x7008], 2
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov rdx, rsp
add rdx, r10
mov r8, r14
sub r8, r10
call .copier
mov r10, qword ptr [rsp + 0x6FE0]
mov rax, r14
sub rax, r10
add qword ptr [rsp + 0x7008], rax
; émettre la tête réécrite vers l'amont
mov rcx, r12
lea rdx, [rsp + 0x4000]
mov r8, qword ptr [rsp + 0x7008]
call .emettre
test rax, rax
jne .fin
; --- corps BORNÉ Content-Length (Q4, R2 : boucles inline) ---
mov rax, r13
sub rax, r14
cmp rax, r15
jbe .corps_deja
mov rax, r15
.corps_deja:
mov r8, rax
lea rdx, [rsp + r14]
mov rcx, r12
call .emettre
test rax, rax
jne .fin
mov rax, r13
sub rax, r14
cmp rax, r15
jae .corps_reste_nul
mov r14, r15
sub r14, rax
jmp .corps_pomper
.corps_reste_nul:
xor r14d, r14d
.corps_pomper:
test r14, r14
je .relais_reponse
.corps_boucle:
mov r8, r14
cmp r8, 0x4000
jbe .corps_cap
mov r8, 0x4000
.corps_cap:
mov rcx, rbx
mov rdx, rsp
call TCP_RECV
test rax, rax
jle .fin
mov qword ptr [rsp + 0x7018], rax
mov r8, rax
mov rdx, rsp
mov rcx, r12
call .emettre
test rax, rax
jne .fin
mov rax, qword ptr [rsp + 0x7018]
sub r14, rax
jne .corps_boucle
; --- relais réponse : http-09 amont -> cliente jusqu'à fermeture amont ---
.relais_reponse:
mov rcx, r12
mov rdx, rbx
mov r8, rsp
mov r9, 0x4000
call HTTP_POMPE
jmp .fin
; ============ tunnel CONNECT (Q3) ============
.tunnel:
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call TCP_CONNEXION
test rax, rax
je .repondre_502
mov r12, rax
lea rdx, [rip + TXT_TUNNEL]
mov r8, 30
mov rcx, rbx
call .emettre
test rax, rax
jne .fin
lea rcx, [rip + MSG_TUNNEL]
mov edx, 8
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
lea rcx, [.pompe_amont]
mov rdx, r12
shl rdx, 32
or rdx, rbx
call TCP_SPAWN
test rax, rax
je .fin
mov rcx, rax
call qword ptr [rip + IAT_CH]
mov rcx, rbx
mov rdx, r12
mov r8, rsp
mov r9, 0x4000
call HTTP_POMPE
jmp .fin
; ============ fermetures (Q5 : amont puis cliente, une fois chacune) ========
.fin:
test r12, r12
je .fin_cliente
mov rcx, r12
call TCP_CLOSE
.fin_cliente:
mov rcx, rbx
call TCP_CLOSE
lea rcx, [rip + MSG_FIN]
mov edx, 15
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
add rsp, 0x7100
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
; ============ réponses (table E1-E8, émission intégrale) ====================
.repondre_400:
lea rdx, [rip + TXT_400]
mov r8, 35
jmp .repondre
.repondre_431:
lea rdx, [rip + TXT_431]
mov r8, 33
jmp .repondre
.repondre_501:
lea rdx, [rip + TXT_501]
mov r8, 31
jmp .repondre
.repondre_411:
lea rdx, [rip + TXT_411]
mov r8, 33
jmp .repondre
.repondre_505:
lea rdx, [rip + TXT_505]
mov r8, 38
jmp .repondre
.repondre_502:
lea rdx, [rip + TXT_502]
mov r8, 40
.repondre:
mov rcx, rbx
call .emettre
jmp .fin
; ============ assistants locaux ==============================================
; .emettre : émission intégrale — rcx socket, rdx ptr, r8 longueur -> rax 0/1
.emettre:
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
test r13, r13
je .emis
.envoyer:
mov rcx, rbx
mov rdx, r12
mov r8, r13
call TCP_SEND
test rax, rax
jle .emis_ko
add r12, rax
sub r13, rax
jne .envoyer
.emis:
xor eax, eax
jmp .emettre_fin
.emis_ko:
mov eax, 1
.emettre_fin:
pop r13
pop r12
pop rbx
ret
; .copier : copie d'octets — rcx destination, rdx source, r8 longueur
.copier:
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
test r13, r13
je .copie_fin
.copie_boucle:
movzx eax, byte ptr [r12]
mov byte ptr [rbx], al
add rbx, 1
add r12, 1
sub r13, 1
jne .copie_boucle
.copie_fin:
pop r13
pop r12
pop rbx
ret
; .pompe_amont : proc de thread détaché — rcx = (amont<<32)|cliente,
; tampon propre 4 Kio dans SON cadre (pile du thread, pas celle de la session)
.pompe_amont:
mov rax, rcx
mov rdx, rcx
shr rax, 32
mov edx, edx
mov ecx, eax
sub rsp, 0x1028
lea r8, [rsp + 0x28]
mov r9, 4096
call HTTP_POMPE
add rsp, 0x1028
ret
