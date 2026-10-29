; tls-08 · session TLS cliente · spec tls-08:R1 · bloc carte g70008
; pre : rcx pointe le cadre de session TLS (zone de travail complète, P1 —
;       fourni VIERGE par http-10:R2, son propriétaire mémoire) ; les TROIS
;       champs de compensation sont néanmoins mis à zéro défensivement à
;       l'entrée (précédent tls-04/D83 : son compteur d'allers) — la
;       compensation ne dépend jamAIS de la bonne volonté de l'amont ;
;       rdx pointe le paquet de session (convention D90, layout.PAQUET_* :
;       +0x00 hôte ptr, +0x08 hôte longueur, +0x10 port u16 ordre hôte,
;       +0x18 requête ptr, +0x20 requête longueur, +0x28 socket cliente —
;       propriété http-10:R2, jamAIS fermée ici, I1) ; le thread appelant
;       est le thread session de http-10 (P3 — I2 : aucun thread créé)
; post : Q1 succès complet : rax = 0 — tcp-13 (connexion), tls-01 (nom),
;       tls-05:0 (credentials), tls-04 (poignée), console « tunnel chiffre
;       etabli », tls-06 (requête chiffrée), puis boucle de relais : tcp-03
;       PAR-DESSUS le résidu tls-07 (jamais ailleurs) → tls-07 → tcp-04 vers
;       le client (le clair pompé TEL QUEL, jamAIS parsé — charte § 7),
;       jusqu'à fin de contexte (tls-07:Q3) ou fermeture système (tcp-03
;       ≤ 0 : le serveur a fini, tcp-04 ≤ 0 : le client est parti — Q1 les
;       nomme l'une et l'autre fins de relais) ; le résidu est DRAINÉ : un
;       verdict 0 de tls-07 avec résidu non vide est rappelé SANS nouvelle
;       réception (jamais un enregistrement déchiffrable laissé en zone
;       pendant que tcp-03 attendrait — le harnais D89 chaînait déjà deux
;       appels sans réception, l'orchestrateur en fait sa boucle) ; la
;       région vivante VIDE rend sa géométrie morte : offset remis en tête
;       (sans elle, un lot exactement consommé de 0x8000 tuerait une session
;       saine à la frontière — D90) ;
;       Q2 échec nommé : rax = verdict transporté TEL QUEL (domaine tls-02
;       2-6, jamAIS remappé — y compris 4 : fin de contexte en poignée,
;       point croisé http-10:R2 noté D90) ou VERDICT_CIBLE 7 si tcp-13
;       échoue (E1) OU tls-01 refuse (la cible ne peut être ni connectée
;       ni nommée) ou 5 si la chambre de réception est NULLE avec un résidu
;       vivant (garde AVANT tcp-03 : r8 > 0 est un contrat de SA spec —
;       fail-closed avant l'appel système, charte M3 § 9 ; c'est la « zone
;       dépassée » de la table http-10:R2) ;
;       Q3 compensation INTÉGRALE sur TOUT chemin (succès compris, arrêt
;       brutal d'appel système compris) : contexte détruit (tls-05:1) SI
;       écrit, credentials libérés (tls-05:2) SI acquis, socket serveur
;       fermée (tcp-05) SI ouverte — dans CET ordre (le contexte référence
;       les credentials), chacun EXACTEMENT une fois (la remise à zéro de
;       tls-05 APRÈS succès constaté est la garde anti-double, son I3) ;
;       l'échec d'une libération (E4) : verdict testé et nommé, UNE
;       ressaisie, la compensation continue jamAIS interrompue, AUCUNE
;       écriture au cadre — le verdict de session transporté (rax) prime,
;       http-10:R2 mappe sa réponse sur le RETOUR, jamAIS sur le cadre ;
;       Q4 le cadre est rendu vierge de secrets (zones réécrites à l'usage
;       suivant — aucun effacement explicite requis, jamais en donnée
;       statique, jamais journalisées)
; inv  : I1 SEUL propriétaire de la fermeture de la socket serveur (cadre
;       +0x20 — la cliente appartient à http-10:R2, paquet +0x28) ; I2
;       aucun thread créé ; I3 console UNIQUEMENT aux états nommés
;       (charte § 3) : « tunnel chiffre etabli » après poignée réussie,
;       « certificat rejete » sur le verdict 3 de tls-04 SEULEMENT (« cet
;       endroit précis » de I4 est la poignée, LE critère M4 ; un verdict 3
;       de tls-07 en plein relais est un E3 réponse tronquée, sans ligne
;       console — D90) ; I4 le verdict 3 produit la ligne console ET (via
;       le retour vers http-10:R2) la réponse 502 ; I5 volatils seuls, le
;       cadre et le paquet vivent en pile
; ABI : msx64, sub rsp 0xE8 (frontière 16 o — les appelés exigent ≤ 0x220
;       sous le cadre, tcp-13:R1 P5 : la réserve du thread session y
;       pourvoit) ; pile locale : +0x58 verdict de session (u32), +0x60
;       cadre, +0x68 paquet, +0x80/+0x88 span de sortie tls-07 (ptr/
;       longueur — écrit PAR tls-07, lu pour le pompage), +0x90 avancement
;       du pompage client ; +0x00..0x28 zone d'appels (ombre + arg5 de
;       tcp-11) ; AUCUN registre non volatil touché (I5)

; --- prologue : cadre, paquet, champs de compensation à zéro ----------------------
sub rsp, 0xE8
mov qword ptr [rsp + 0x60], rcx
mov qword ptr [rsp + 0x68], rdx
mov qword ptr [rcx + 0x20], 0
mov qword ptr [rcx], 0
mov qword ptr [rcx + 0x10], 0

; --- 1. connexion à la cible (tcp-13 : hôte span, port ordre hôte, E1) ------------
mov r11, [rsp + 0x68]
mov rcx, [r11]
mov rdx, [r11 + 0x08]
movzx r8d, word ptr [r11 + 0x10]
call TCP_CONNEXION
test rax, rax
jz .cible
mov r10, [rsp + 0x60]
mov [r10 + 0x20], rax

; --- 2. nom cible UTF-16 (tls-01 → zone nom du cadre, ptr consigné +0x28) ---------
mov r11, [rsp + 0x68]
mov rcx, [r11]
mov rdx, [r11 + 0x08]
mov r10, [rsp + 0x60]
lea r8, [r10 + 0x60]
call TLS_UTF16
test eax, eax
jnz .cible
mov r10, [rsp + 0x60]
lea rax, [r10 + 0x60]
mov [r10 + 0x28], rax

; --- 3. credentials clientes (tls-05 op 0 — validation AUTOMATIQUE, P3) -----------
xor ecx, ecx
mov rdx, [rsp + 0x60]
call TLS_CLES
test eax, eax
jnz .echec

; --- 4. la poignée de main (tls-04 : LE critère M4 vit dedans) -------------------
mov rcx, [rsp + 0x60]
call TLS_POIGNEE
test eax, eax
jnz .poignee_echec

; --- 5. état nommé : le tunnel existe (console tcp-11, AUCUN secret, I3) ----------
lea rcx, [rip + TXT_TLS_ETABLI]
mov edx, 23
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL

; --- 6. émission de la requête réécrite (tls-06 : span de l'appelant intact) ------
mov r11, [rsp + 0x68]
mov rcx, [rsp + 0x60]
mov rdx, [r11 + 0x18]
mov r8, [r11 + 0x20]
call TLS_EMISSION
test eax, eax
jnz .echec

; --- 7. géométrie D89 du relais : région vivante née VIERGE (layout, D89) ---------
mov r10, [rsp + 0x60]
mov word ptr [r10 + 0x3A], 0
mov word ptr [r10 + 0x3C], 0

; --- 8. boucle de relais (Q1) : recevoir, déchiffrer, pomper, drainer -------------
.relais:
mov r10, [rsp + 0x60]
movzx eax, word ptr [r10 + 0x3A]
test eax, eax
jnz .chambre
mov word ptr [r10 + 0x3C], 0
xor eax, eax
jmp .recevoir
.chambre:
movzx ecx, word ptr [r10 + 0x3C]
add rax, rcx
cmp rax, 0x8000
jae .zone_pleine
.recevoir:
mov r10, [rsp + 0x60]
mov rcx, [r10 + 0x20]
lea rdx, [r10 + 0x4260]
add rdx, rax
mov r8, 0x8000
sub r8, rax
call TCP_RECV
test rax, rax
jle .succes
mov r10, [rsp + 0x60]
movzx ecx, word ptr [r10 + 0x3A]
add ecx, eax
mov word ptr [r10 + 0x3A], cx
.decrypter:
mov r10, [rsp + 0x60]
mov rcx, r10
lea rdx, [r10 + 0x4260]
movzx r8d, word ptr [r10 + 0x3A]
lea r9, [rsp + 0x80]
call TLS_RECEPTION
test eax, eax
jz .span
cmp eax, 4
je .succes
cmp eax, 2
je .relais
jmp .echec

; --- pompage du span livré (tcp-04 boucle d'achèvement — span VIDE : rien) --------
.span:
mov qword ptr [rsp + 0x90], 0
cmp qword ptr [rsp + 0x88], 0
je .apres_pompe
.envoi:
mov r11, [rsp + 0x68]
mov rcx, [r11 + 0x28]
mov rdx, [rsp + 0x80]
add rdx, [rsp + 0x90]
mov r8, [rsp + 0x88]
sub r8, [rsp + 0x90]
call TCP_SEND
test rax, rax
jle .succes
add qword ptr [rsp + 0x90], rax
mov rax, [rsp + 0x90]
cmp rax, [rsp + 0x88]
jb .envoi
.apres_pompe:
; le résidu est DRAINÉ avant toute nouvelle réception (le clair déjà pompé
; est de la mémoire morte — la normalisation du prochain tls-07 l'écrase)
mov r10, [rsp + 0x60]
movzx eax, word ptr [r10 + 0x3A]
test eax, eax
jnz .decrypter
jmp .relais

; --- verdicts propres de tls-08 (hors domaine tls-02 : 7 ; garde : 5) -------------
.cible:
mov dword ptr [rsp + 0x58], 7
jmp .compensation
.zone_pleine:
mov dword ptr [rsp + 0x58], 5
jmp .compensation
.succes:
mov dword ptr [rsp + 0x58], 0
jmp .compensation
.echec:
mov [rsp + 0x58], eax
jmp .compensation

; --- la poignée échoue : le verdict 3 CONSOLE d'abord (I4), tous compensent -------
.poignee_echec:
mov [rsp + 0x58], eax
cmp eax, 3
jne .compensation
lea rcx, [rip + TXT_TLS_CERT]
mov edx, 19
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
jmp .compensation

; --- compensation INTÉGRALE (Q3 — TOUT chemin, l'ordre EST le contrat) ------------
.compensation:
mov r10, [rsp + 0x60]
cmp qword ptr [r10 + 0x10], 0
je .pas_contexte
mov ecx, 1
mov rdx, r10
call TLS_CLES
test eax, eax
jz .pas_contexte
mov ecx, 1
mov rdx, [rsp + 0x60]
call TLS_CLES
.pas_contexte:
mov r10, [rsp + 0x60]
cmp qword ptr [r10], 0
je .pas_credentials
mov ecx, 2
mov rdx, r10
call TLS_CLES
test eax, eax
jz .pas_credentials
mov ecx, 2
mov rdx, [rsp + 0x60]
call TLS_CLES
.pas_credentials:
mov r10, [rsp + 0x60]
cmp qword ptr [r10 + 0x20], 0
je .fin
mov rcx, [r10 + 0x20]
call TCP_CLOSE
.fin:
mov eax, [rsp + 0x58]
add rsp, 0xE8
ret
