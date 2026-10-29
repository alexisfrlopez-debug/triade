; tls-02 · table des verdicts SSPI · spec tls-02:R1 · liste blanche 13 codes
; pre : rcx = HRESULT 32 bits SIGN-ÉTENDU (P1) ; post : rax = verdict 0..6,
; rdx = HRESULT préservé (Q2). Domaine validé : rcx doit être le sign-étendu
; de ecx — hors domaine = verdict 6 (fail-closed). Feuille pure (I1) ;
; aucun registre non volatil (I3) ; les valeurs citées sont la liste blanche
; I4 (winerror.h, vérifiées D79 — cf layout.HRESULTS)
mov rdx, rcx
movsxd r10, ecx
cmp rcx, r10
jne .fatal
test ecx, ecx
jz .succes
cmp ecx, 0x00090312
je .continuer
cmp ecx, 0x80090318
je .incomplet
cmp ecx, 0x80090325
je .certificat
cmp ecx, 0x80090328
je .certificat
cmp ecx, 0x80090327
je .certificat
cmp ecx, 0x80090349
je .certificat
cmp ecx, 0x80090322
je .certificat
cmp ecx, 0x00090317
je .fin_contexte
cmp ecx, 0x80090308
je .negocie
cmp ecx, 0x80090330
je .negocie
cmp ecx, 0x8009030F
je .negocie
cmp ecx, 0x80090310
je .negocie
jmp .fatal
.succes:
xor eax, eax
ret
.continuer:
mov eax, 1
ret
.incomplet:
mov eax, 2
ret
.certificat:
mov eax, 3
ret
.fin_contexte:
mov eax, 4
ret
.negocie:
mov eax, 5
ret
.fatal:
mov eax, 6
ret
