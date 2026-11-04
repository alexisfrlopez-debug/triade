; su-03-verdict · brouillon étiqueté — spec su-03:R1, bloc carte f60003
; feuille pure : rdi = rax BRUT du syscall échoué (négatif) ; le bloc nie,
; balaye la table (I1 : [nombre u32] + {errno u32, verdict u32}), rend le
; verdict de l'entrée ou 6 (VERDICT_FATAL) — tout errno hors table.
; r8 = table, r9 = entrée courante, rcx = entrées restantes.
@ERRNOS = 0x140
neg rdi
lea r8, [rip + @ERRNOS]
mov ecx, dword ptr [r8]
lea r9, [r8 + 4]
test ecx, ecx
jz .fatal
.boucle:
cmp edi, dword ptr [r9]
je .trouve
add r9, 8
sub ecx, 1
test ecx, ecx
jz .fatal
jmp .boucle
.trouve:
mov eax, dword ptr [r9 + 4]
ret
.fatal:
mov eax, 6
ret
