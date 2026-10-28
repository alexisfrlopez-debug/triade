; tls-02-verdicts · bloc table des verdicts SSPI (liste blanche) · spec tls-02:R1 · bloc carte g70002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6080, taille 256 octets
; Dépendances : feuille pure ; table TOTALE des verdicts SSPI — liste blanche 13 codes (layout.HRESULTS), domaine = HRESULT 32 bits sign-étendu, hors domaine = verdict 6
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-02-verdicts.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 156 o · padding : 100 o (NOP)
; Étiquettes résolues : .succes=0x60f5, .continuer=0x60f8, .incomplet=0x60fe, .certificat=0x6104, .fin_contexte=0x610a, .negocie=0x6110, .fatal=0x6116
mov rdx, rcx
movsxd r10, ecx
cmp rcx, r10
jne 0x6116
test ecx, ecx
jz 0x60f5
cmp ecx, 0x00090312
je 0x60f8
cmp ecx, 0x80090318
je 0x60fe
cmp ecx, 0x80090325
je 0x6104
cmp ecx, 0x80090328
je 0x6104
cmp ecx, 0x80090327
je 0x6104
cmp ecx, 0x80090349
je 0x6104
cmp ecx, 0x80090322
je 0x6104
cmp ecx, 0x00090317
je 0x610a
cmp ecx, 0x80090308
je 0x6110
cmp ecx, 0x80090330
je 0x6110
cmp ecx, 0x8009030F
je 0x6110
cmp ecx, 0x80090310
je 0x6110
jmp 0x6116
xor eax, eax
ret
mov eax, 1
ret
mov eax, 2
ret
mov eax, 3
ret
mov eax, 4
ret
mov eax, 5
ret
mov eax, 6
ret
