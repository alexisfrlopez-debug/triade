; sup-39-prevol · bloc terrain · spec sup-39:R1 · bloc carte f60039
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4b40, taille 192 octets
; Dépendances : IAT kernel32#3 : WaitForSingleObject, GetExitCodeProcess ; IAT kernel32#1 : CloseHandle ; blocs sup-31 (lanceur), win-05 (entrée trace) ; état .data (HPROC, CODE_SORTIE) ; chaînes S08/S09 + CMD_TASKKILL/CMD_CURL_AMONT (zone données sup 3) — ZONE-RÉSIDENT dans la queue de la zone données sup 1 (table R10 PLEINE, miroir D95/D96/D99 : couvert par l'entrée de zone, jamais une entrée neuve) — prévol : orphelins + réseau amont AVANT l'extraction (D101, terrain.18 — les ÉTAPES 0/0 BIS du protocole automatiques)
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-39-prevol.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 169 o · padding : 23 o (NOP)
; Étiquettes résolues : .sans_taskkill=0x4b6c, .fin=0x4b94, .ligne=0x4b9b, .attendre=0x4bad
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4b44 + 0x7 + 0x25af = 0x70fa
;   0x4b5b + 0x7 + 0x25f9 = 0x715b
;   0x4b6c + 0x7 + 0x25b2 = 0x7125
;   0x4b83 + 0x7 + 0x25fa = 0x7184
;   0x4ba1 + 0x7 - 0x1058 = 0x3b50
;   0x4bb1 + 0x7 - 0x10a8 = 0x3b10
;   0x4bbd + 0x6 - 0x28b3 = 0x2310
;   0x4bc3 + 0x7 - 0x10ba = 0x3b10
;   0x4bca + 0x7 - 0x1081 = 0x3b50
;   0x4bd1 + 0x6 - 0x28bf = 0x2318
;   0x4bd7 + 0x7 - 0x10ce = 0x3b10
;   0x4bde + 0x6 - 0x2aec = 0x20f8
sub rsp, 0x28
lea rcx, [rip + 0x25af]
xor edx, edx
call 0x5200
test eax, eax
je 0x4b6c
call 0x4bad
lea rcx, [rip + 0x25f9]
mov edx, 41
call 0x4b9b
lea rcx, [rip + 0x25b2]
xor edx, edx
call 0x5200
test eax, eax
je 0x4b94
call 0x4bad
lea rcx, [rip + 0x25fa]
mov edx, 29
call 0x4b9b
xor eax, eax
add rsp, 0x28
ret
mov r8d, 1
mov r9d, dword ptr [rip - 0x1058]
jmp 0x5000
sub rsp, 0x28
mov rcx, qword ptr [rip - 0x10a8]
mov edx, 30000
call qword ptr [rip - 0x28b3]
mov rcx, qword ptr [rip - 0x10ba]
lea rdx, [rip - 0x1081]
call qword ptr [rip - 0x28bf]
mov rcx, qword ptr [rip - 0x10ce]
call qword ptr [rip - 0x2aec]
add rsp, 0x28
ret
