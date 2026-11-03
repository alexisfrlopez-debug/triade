; http-10-session-r3 · bloc session proxy — révision routage du relèvement et ligne de flux · spec http-10:R3 · bloc carte g80002
; Ancêtre : http-10:R2 (D92, embarquée 0.5.1 @0x74C0 — la spécification R2 vit
; dans m4/I/ et ne change pas : la balise est immuable § 9). La révision vit en
; M5 (.text4 0x81C0) et modifie CE que le relèvement exige : le routage du
; verdict « cible à relever » (http-08:R3 rax=5) vers tls-08 AVEC la politique
; passée au parseur, et LA LIGNE DE FLUX. Tout le reste de R2 (accumulation
; bornée, tri-entrée, pompe détachée, une requête par connexion, propriété de
; la socket cliente, anti-interblocage, table des réponses Q3') est REPRIS TEL
; QUEL — cité, non recopié (T5).
; P7  la politique lue UNE fois (.data R_POLITIQUE) et passée en 5e argument
;     (loge 5 : [rsp+0x28] à l'appel, [rsp+0x30] du callee) — LE MÊME chemin
;     Q2' pour les verdicts 4 et 5 (port 443, table des réponses INCHANGÉE).
; P8  rsi/rdi = compteurs de flux (entrés : accumulation + corps pompé ;
;     sortis : les émissions .emettre) — non-volatils (7 pushes), les octets
;     des relais délégués (HTTP_POMPE, tls-08) ne sont PAS comptés deux fois.
; Q6  LA LIGNE DE FLUX — UNE par session cliente aboutie dont la requête a
;     été parsée, émise via tcp-11 AVANT la compensation de fermeture R1 :
;     « flux » + méthode + « » + hôte (span autorité effective, TRONQUÉ à
;     14 octets — E3) + «:» + PORT EFFECTIF (E2, le champ numérique de
;     tcp-11) + « v= » verdict + « e= » + « s= » + CRLF ; le verdict suit le
;     domaine TOTAL (0 aboutie / 2..7 tls-08 transportés / 400..505 nommés) ;
;     sentinelle -1 = rien à nommer.
; Q7  SANS politique : R2 OCTET POUR OCTET — aucune ligne, aucun verdict 5.
; I7  appels IAT de la session : EXACTEMENT {CloseHandle} (hérité) — la ligne
;     vit via tcp-11/libc-04 (appels directs) ; I8 le verdict de session est
;     écrit AUX DISPATCHES avant l'émission ; I9 la ligne est composée DANS
;     LE CADRE (ZONES FLUX du trou documenté +0x7028..+0x70FF), jamais en
;     donnée statique.
; Dépendances : RÉVISION (ancêtre g70010 http-10:R2 embarqué 0.5.1, cité § 9)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-10-session-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
push rbx
push r12
push r13
push r14
push r15
push rsi
push rdi
; Q0 hérité (R3/D63) — probing étendu au cadre élargi (0x13390)
mov r10, -0x1000
.probe:
mov rax, qword ptr [rsp + r10]
sub r10, 0x1000
cmp r10, -0x13000
jge .probe
mov rax, qword ptr [rsp - 0x13390]
sub rsp, 0x13390
; P8 — les compteurs de flux : rsi (octets clairs ENTRÉS : accumulation
; + corps pompé), rdi (octets clairs SORTIS : les émissions .emettre) —
; non-volatils sauvegardés au prologue (7 pushes), restitués à l'épilogue
xor esi, esi
xor edi, edi
; Q6 — la sentinelle de la ligne de flux (-1 : rien à nommer) vit dans le
; trou documenté du cadre R2 (+0x7028 — jamais lu ni écrit par R1/R2,
; innocuité par balayage, miroir D92) ; TAILLE_CADRE inchangée (ABI P5)
mov qword ptr [rsp + 0x7028], -1
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
add rsi, rax
; P8 — les octets reçus entrent au compteur de la session
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
; P7 — la politique est LUE UNE FOIS dans .data (R_POLITIQUE, l'état que
; http-12:R3 a écrit au démarrage) et passée en CINQUIÈME argument — la
; loge 5 vit SOUS le cadre (sub rsp, 0x30, miroir des recherches http-04 :
; [rsp+0x28] à l'appel = [rsp+0x30] du callee) — le tampon de requête
; occupe [rsp..rsp+0x4000) du cadre, la loge ABI ne le touche JAMAIS ; la
; CACHE +0x70D0 (trou documenté du cadre R2, layout FLUX_POLITIQUE)
; garde l'état pour la ligne de flux — la feuille pure ne lit jamais .data
; (I1 de sa spec)
mov rax, qword ptr [rip + POLITIQUE]
mov qword ptr [rsp + 0x70D0], rax
sub rsp, 0x30
mov qword ptr [rsp + 0x28], rax
call HTTP_CIBLE_R3
add rsp, 0x30
; ARRÊT D92 : le verdict est consigné @+0x7010 sur TOUT chemin (toujours
; initialisé avant lecture — le drapeau de routage n'est jamais un déchet)
mov qword ptr [rsp + 0x7010], rax
test rax, rax
je .cible_ok
cmp rax, 3
je .repondre_501
cmp rax, 4
je .cible_tls
; P7 — le verdict 5 est routé COMME le 4 : LE MÊME chemin Q2' (port 443
; AUSSI pour la cible relevée, requête réécrite en forme origine)
cmp rax, 5
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
; E2 — cible RELEVÉE (verdict 5) : le port EXPLICITE du navigateur
; (http://hote:8080/) est PERDU au relèvement — l'origine est l'HTTPS
; STANDARD de l'hôte : le port de routage est FORCÉ 443 APRÈS le
; tri-entrée (l'explicite de l'autorité gagnerait sinon, http-07 :
; « l'explicite gagne » — règle Q1ter R2, inchangée pour https) ; la
; ligne de flux porte le port EFFECTIF (443), jamais le port perdu ;
; un relèvement vers :8080 serait une invention
cmp qword ptr [rsp + 0x7010], 5
jne .pas_releve
mov dword ptr [rsp + 0x6FB0], 443
.pas_releve:
; Q6 — le PRÉFIXE de la ligne de flux est composé ICI, AVANT TOUT relais :
; la méthode PAR LA TABLE R_TAB_METHODES (la spécification — .rdata STABLE :
; le span méthode @+0x6F08 pointe DANS le tampon de requête [rsp..rsp+0x4000)
; que http-09 recevra la réponse et que le corps pompé écrase) et l'hôte
; (span autorité effective, TRONQUÉ à 14 — E3 : la borne est nommée) copié
; DANS LA ZONE FLUX pendant sa validité ; les ZONES FLUX (au-delà du tampon)
; ne sont JAMAIS un tampon de relais ; la longueur est consignée @+0x70D8
; (FLUX_PREF_LEN, layout — le trou R2, jamais lu ni écrit par R1) ;
; registres morts ici : rax (verdict http-07 testé), r10/r11, rcx/rdx/r8 —
; .copier préserve rbx/r12/r13 (les volatils vivants du routage)
lea r10, [rsp + 0x7030]
mov dword ptr [r10], 0x78756C66
mov byte ptr [r10 + 4], 0x20
add r10, 5
mov eax, dword ptr [rsp + 0x6F00]
shl rax, 4
lea r11, [rip + TAB_METHODES]
add r11, rax
sub r11, 16
mov rcx, r10
mov rdx, qword ptr [r11]
mov r8, qword ptr [r11 + 8]
call .copier
add r10, r8
mov byte ptr [r10], 0x20
add r10, 1
mov r11, qword ptr [rsp + 0x6FA8]
cmp r11, 14
jbe .flux_hote
mov r11d, 14
.flux_hote:
mov rcx, r10
mov rdx, qword ptr [rsp + 0x6FA0]
mov r8, r11
call .copier
add r10, r8
mov byte ptr [r10], 0x3A
add r10, 1
lea rax, [rsp + 0x7030]
sub r10, rax
mov qword ptr [rsp + 0x70D8], r10
cmp qword ptr [rsp + 0x7000], 0
jne .sans_te
cmp qword ptr [rsp + 0x6F98], 0
je .sans_te
mov qword ptr [rsp + 0x7028], 501
jmp .repondre_501
.sans_te:
cmp qword ptr [rsp + 0x6FF8], 0
je .valider_cl
mov eax, dword ptr [rsp + 0x6F00]
cmp eax, 3
mov qword ptr [rsp + 0x7028], 411
je .repondre_411
cmp eax, 4
mov qword ptr [rsp + 0x7028], 411
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
; P7 — la garde cible TLS s'applique AUSSI à la relevée (verdict 5) : le
; MÊME chemin Q2', corps refusé honnête au même titre
cmp qword ptr [rsp + 0x7010], 5
je .tls_garde
cmp dword ptr [rsp + 0x6F00], 8
je .tunnel
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call TCP_CONNEXION
test rax, rax
mov qword ptr [rsp + 0x7028], 502
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
; relais appartiennent à tls-08 » ; P7 — la cible RELEVÉE (verdict 5) prend
; LE MÊME chemin de paquet que la cible TLS (verdict 4) : tls-08 connecte et
; chiffre vers l'origine (port 443, E2) — le transport ne connaît pas la
; cause du tunnel, la requête réécrite en forme origine est la même
cmp qword ptr [rsp + 0x7010], 4
je .paquet_tls
cmp qword ptr [rsp + 0x7010], 5
jne .emission_amont
.paquet_tls:
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
; I8/Q6 — le verdict de session est écrit AU DISPATCH, avant toute
; émission : 0 = aboutie, 2..7 = verdicts tls-08 TRANSPORTÉS TELS QUELS
mov qword ptr [rsp + 0x7028], rax
test rax, rax
je .fin
cmp eax, 3
je .repondre_502_cert
jmp .repondre_502
.tls_garde:
test r15, r15
mov qword ptr [rsp + 0x7028], 501
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
add rsi, rax
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
mov qword ptr [rsp + 0x7028], 0
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
mov qword ptr [rsp + 0x7028], 502
je .repondre_502
mov r12, rax
; Q6 — le tunnel CONNECT est ÉTABLI : verdict 0 de session
mov qword ptr [rsp + 0x7028], 0
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
; Q6/Q7 — LA LIGNE DE FLUX (politique ARMÉE seulement, UNE fois, AVANT la
; compensation de fermeture R1) : sentinelle -1 (requête non identifiable)
; ou politique absente (la CACHE +0x70D0 — P7 : l'état .data lu UNE fois,
; jamais une relecture, jamais la loge ABI qui vit sous le cadre) → R2
; OCTET POUR OCTET (aucune ligne, aucun verdict 5 possible —
; anti-régression R7 au niveau du journal) ;
; sinon : composition DANS LE CADRE (ZONES FLUX, I9 — jamais en donnée
; statique), tcp-11 porte le champ numérique (LE PORT EFFECTIF, E2) et les
; trois nombres du suffixe (formés par libc-04, héritage R7) — zéro secret,
; états nommés seulement (charte § 3) ; le verdict est déjà écrit (I8).
cmp qword ptr [rsp + 0x7028], -1
je .fin_r1
cmp qword ptr [rsp + 0x70D0], 0
je .fin_r1
; le PRÉFIXE est déjà composé (au routage, .pas_releve — AVANT les relais :
; la méthode vient de la table .rdata, l'hôte y a été copié pendant la
; validité de son span) ; ici : le SUFFIXE seul — « v= » + verdict + « e= »
; + entrés + « s= » + sortis + CRLF, composition DANS LE CADRE (ZONES FLUX,
; I9 — jamais en donnée statique), les nombres PAR libc-04 (héritage R7) —
; zéro secret, états nommés seulement (charte § 3) ; le verdict est déjà
; écrit (I8)
lea r13, [rsp + 0x7070]
mov byte ptr [r13], 0x20
mov byte ptr [r13 + 1], 0x76
mov byte ptr [r13 + 2], 0x3D
add r13, 3
mov ecx, dword ptr [rsp + 0x7028]
mov rdx, r13
call ITOA
mov rcx, r13
call STRLEN
add r13, rax
mov byte ptr [r13], 0x20
mov byte ptr [r13 + 1], 0x65
mov byte ptr [r13 + 2], 0x3D
add r13, 3
mov ecx, esi
mov rdx, r13
call ITOA
mov rcx, r13
call STRLEN
add r13, rax
mov byte ptr [r13], 0x20
mov byte ptr [r13 + 1], 0x73
mov byte ptr [r13 + 2], 0x3D
add r13, 3
mov ecx, edi
mov rdx, r13
call ITOA
mov rcx, r13
call STRLEN
add r13, rax
mov word ptr [r13], 0x0A0D
add r13, 2
; l'émission — tcp-11(préfixe, longueur, PORT EFFECTIF, suffixe, longueur) :
; le champ numérique de tcp-11 porte le port (E2 — jamais le port perdu) ;
; la longueur du préfixe est CELLE CONSIGNÉE au routage (@+0x70D8 — la
; composition a eu lieu pendant la validité des spans, la longueur ne peut
; plus mentir) — la ligne ne ment jamais
lea rcx, [rsp + 0x7030]
mov rdx, qword ptr [rsp + 0x70D8]
mov r8d, dword ptr [rsp + 0x6FB0]
lea r9, [rsp + 0x7070]
sub r13, r9
mov qword ptr [rsp + 0x20], r13
call TCP_JOURNAL
.fin_r1:
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
pop rdi
pop rsi
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
add rdi, rax
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
