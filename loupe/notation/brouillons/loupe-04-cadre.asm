; loupe-04 · le cadre posé vierge · spec loupe-04:R1 (Q1/Q2/Q3, I1/I2/I3/I4)
; LA STRUCTURE UNIQUE : la zone 960 o à l'image (déclarée au plan, D161) —
; la mise à zéro par libc-07 HÉRITÉ PAR LA CARTE (le bloc scellé M1,
; byte-identique, JAMAIS une boucle réécrite — Q2), puis la poignée posée
; à INVALIDE (+528). Aucune entrée IAT, aucun site syscall (I2 : le memset
; passe PAR LA CARTE — le miroir exact des feuilles pures tls13, charte
; § 9) ; P1 : aucune précondition (le geste de naissance ne dépend de
; rien) ; rax = 0 (Q3).
push rbx
sub rsp, 0x20
lea rbx, [rip + CADRE]
mov rcx, rbx
xor edx, edx
mov r8d, 960
call LIBC07
mov qword ptr [rbx + 528], -1
xor eax, eax
add rsp, 0x20
pop rbx
ret
