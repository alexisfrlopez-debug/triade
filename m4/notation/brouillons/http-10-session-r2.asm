; http-10-session-r2 · brouillon — session proxy · RÉVISION routage TLS (D92)
; Ancêtre : http-10:R3 (e50010, scellé 0.4.0 @0x5580, 1847 o, m3/notation).
; Discipline des révisions inter-jalons (modèle win-02:R2, tcp-07:R3) : tout le
; comportement R1 est REPRIS — cette révision AJOUTE ce que le tunnel exige :
; le routage du verdict « cible TLS » (http-08:R2 rax = 4) vers tls-08 et
; l'entrée ÉTIQUETÉE de la table des réponses (502 « Certificat rejete »).
;
; CADRE (convention D92, layout.py source unique) : 0x13390 = cadre R1 (offsets
; inchangés) + verdict http-08:R2 @+0x7010 (u64 — jamais lu ni écrit par R1,
; innocuité prouvée par balayage de la notation scellée) + paquet de session
; @+0x7100 (0x30, convention D90) + cadre TLS @+0x7130 (0xC260, convention
; D81/D89). Probing hérité D63 étendu aux bornes du cadre élargi : boucle
; -0x1000..-0x13000 par pas de 0x1000, touche finale [rsp-0x13390], puis
; sub rsp, 0x13390 (multiple de 16 — l'ABI P5 est préservé, les offsets R1
; restent numériquement exacts).
;
; ARRÊTS contractuels D92 (corpus cité, rien inventé) :
;   1. la ligne console « certificat rejete » appartient à tls-08 SEUL (I4,
;      fixture @0x2C80 « tls-08 unique propriétaire des deux », README D90) —
;      la session ne la ré-émet JAMAIS (point croisé D91 : pas de double
;      émission) ; la réponse 502 suit le RETOUR du verdict (README D90 :
;      « http-10:R2 mappe sur rax, jamais sur le cadre ») ;
;   2. l'entrée étiquetée « HTTP/1.1 502 Certificat rejete » (34 o @0x2CA0)
;      est la SEULE entrée nouvelle de la table Q3' — les verdicts 2/4/5/6/7
;      de tls-08 mappent sur la ligne 502 R1 scellée (la spécification
;      n'étiquette QUE le certificat : « chaque entrée NOUVELLE est nommée ICI
;      une seule fois ») ;
;   3. le port implicite 443 est le DÉFAUT passé à http-07:R1 (P3 de sa
;      spécification : « tout autre valeur est le défaut de l'appelant : 80
;      pour un schéma http » — http-08:R2:Q4 : « consigné DANS la sortie » :
;      le port effectif, explicite ou défaut, vit dans la zone http-07) ;
;   4. un corps sur cible TLS (Content-Length > 0) est REFUSÉ 501 — refus
;      honnête, jamais de tentative : le paquet D90 porte UNE requête (le
;      head réécrit forme origine), tls-08:Q1 l'émet UNE fois (tls-06) puis
;      relais serveur → cliente SEUL — le corps en flux n'est pas dans le
;      périmètre M4 (miroir exact du Transfer-Encoding R1, E4 : « le relais
;      en flux n'est pas dans le périmètre M3 »).
; I6' : la session n'appelle JAMAIS une entrée SSPI directement — la chaîne
; cryptographique vit intégralement derrière tls-08 (unique appel M4 nouveau).
push rbx
push r12
push r13
push r14
push r15
; Q0 hérité (R3/D63) — probing étendu au cadre élargi (0x13390)
mov r10, -0x1000
.probe:
mov rax, qword ptr [rsp + r10]
sub r10, 0x1000
cmp r10, -0x13000
jge .probe
mov rax, qword ptr [rsp - 0x13390]
sub rsp, 0x13390
mov rbx, rcx
xor r12d, r12d
lea rcx, [rip + MSG_CONNEXION]
mov edx, 20
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
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
mov rcx, qword ptr [rsp + 0x6F18]
mov rdx, qword ptr [rsp + 0x6F20]
mov r8d, dword ptr [rsp + 0x6F00]
lea r9, [rsp + 0x6FB8]
call HTTP_CIBLE_R2
; ARRÊT D92 : le verdict est consigné @+0x7010 sur TOUT chemin (toujours
; initialisé avant lecture — le drapeau de routage n'est jamais un déchet)
mov qword ptr [rsp + 0x7010], rax
test rax, rax
je .cible_ok
cmp rax, 3
je .repondre_501
cmp rax, 4
je .cible_tls
jmp .repondre_400
; P6/Q2' — le routage : miroir de .forme_absolue, SEUL écart le défaut de
; port (443, http-08:R2:Q4 — le reste de la chaîne R1 est PARTAGÉ tel quel)
.cible_tls:
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 443
jmp .resoudre
.cible_ok:
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
cmp qword ptr [rsp + 0x7000], 0
jne .sans_te
cmp qword ptr [rsp + 0x6F98], 0
je .sans_te
jmp .repondre_501
.sans_te:
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
; Q2'/ARRÊT 4 : la garde cible TLS AVANT le CONNECT/tcp-13 — un corps sur
; cible TLS est refusé honnête (501, miroir TE), r12 reste 0 (pas d'amont :
; tls-08 connecte, .fin ne fermera JAMAIS la socket serveur — I1 de tls-08)
.trancher:
cmp qword ptr [rsp + 0x7010], 4
je .tls_garde
cmp dword ptr [rsp + 0x6F00], 8
je .tunnel
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call TCP_CONNEXION
test rax, rax
je .repondre_502
mov r12, rax
; la réécriture est PARTAGÉE par les deux chemins (la requête forme origine
; est la même — c'est le transport qui diffère : tcp-04 clair ou tls-06)
.reecriture:
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
; dispatch post-réécriture : le chemin TLS ne touche NI tcp-13 NI tcp-04 —
; Q2' : « la session n'achève rien elle-même : socket serveur et boucle de
; relais appartiennent à tls-08 »
cmp qword ptr [rsp + 0x7010], 4
jne .emission_amont
mov rax, qword ptr [rsp + 0x6FA0]
mov qword ptr [rsp + 0x7100], rax
mov rax, qword ptr [rsp + 0x6FA8]
mov qword ptr [rsp + 0x7108], rax
mov eax, dword ptr [rsp + 0x6FB0]
mov word ptr [rsp + 0x7110], ax
lea rax, [rsp + 0x4000]
mov qword ptr [rsp + 0x7118], rax
mov rax, qword ptr [rsp + 0x7008]
mov qword ptr [rsp + 0x7120], rax
mov qword ptr [rsp + 0x7128], rbx
; rdi est NON-VOLATIL (ABI msx64) : préservé au cadre @+0x7020 (D92 — jamais
; lu ni écrit par R1, innocuité par balayage de la notation scellée), restitué
; AVANT l'appel — le rep stosq ne doit rien laisser derrière lui que des zéros
mov qword ptr [rsp + 0x7020], rdi
lea rdi, [rsp + 0x7130]
xor eax, eax
mov rcx, 0x184C
rep stosq
mov rdi, qword ptr [rsp + 0x7020]
lea rcx, [rsp + 0x7130]
lea rdx, [rsp + 0x7100]
call TLS_SESSION
; E1 : l'échec du tunnel est un ÉTAT de la session — Q3' mappe sur rax :
; 3 = l'entrée étiquetée, TOUT autre verdict nommé (2/4/5/6/7) = 502 R1
test rax, rax
je .fin
cmp eax, 3
je .repondre_502_cert
jmp .repondre_502
.tls_garde:
test r15, r15
jne .repondre_501
jmp .reecriture
.emission_amont:
mov rcx, r12
lea rdx, [rsp + 0x4000]
mov r8, qword ptr [rsp + 0x7008]
call .emettre
test rax, rax
jne .fin
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
.relais_reponse:
mov rcx, r12
mov rdx, rbx
mov r8, rsp
mov r9, 0x4000
call HTTP_POMPE
jmp .fin
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
add rsp, 0x13390
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
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
mov rcx, rbx
call .emettre
jmp .fin
; Q3' — l'entrée ÉTIQUETÉE (34 o @0x2CA0) : le critère M4 « échec propre sur
; certificat invalide » ATERRIT ici — la ligne console appartient à tls-08
.repondre_502_cert:
lea rdx, [rip + TXT_502_CERT]
mov r8, 34
jmp .repondre
.repondre:
mov rcx, rbx
call .emettre
jmp .fin
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
