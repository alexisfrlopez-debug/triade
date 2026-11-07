; loupe-07 · cumul : les empreintes du fichier entier au panneau · spec loupe-07:R1
; LA COMPOSITION SEULE (I1 : aucune entrée IAT, aucun site syscall — le
; miroir des feuilles pures, charte § 9) : loupe-05(0, taille, sortie+16)
; le passage SHA-256 PUIS loupe-06(0, taille, sortie+0) le passage MD5 —
; DEUX passages, L'UN APRÈS L'AUTRE (I2 : l'exclusion de famille, jamais
; deux flux simultanés) ; I3 : le panneau est CELUI DU DISQUE (les
; écritures du journal non sauvées n'y figurent PAS — l'astérisque de la
; barre nomme la divergence, la vérité n'attend pas la sauvegarde) ; I4 :
; la vue, le curseur et le journal INTACTS (le calcul ne touche à rien de
; la session) ; E3 : un refus des blocs composés RELAYÉ TEL QUEL (le
; verdict traverse, jamais avalé — le panneau ne publie RIEN).
push rbx
push r12
sub rsp, 0x28
lea rbx, [rip + CADRE]
cmp qword ptr [rbx + 528], -1
je .refus_session
test rcx, rcx
jz .refus_sortie
mov r12, rcx
xor ecx, ecx
mov rdx, qword ptr [rbx + 520]
lea r8, [r12 + 16]
call LOUPE05
test eax, eax
js .sortie
xor ecx, ecx
mov rdx, qword ptr [rbx + 520]
mov r8, r12
call LOUPE06
test eax, eax
js .sortie
xor eax, eax
jmp .sortie
.refus_session:
mov eax, -4
jmp .sortie
.refus_sortie:
mov eax, -5
jmp .sortie
.sortie:
add rsp, 0x28
pop r12
pop rbx
ret
