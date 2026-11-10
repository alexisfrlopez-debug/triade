; loupe-13 · recherche : l'algorithme pur, la fenêtre et le motif · spec loupe-13:R1
; LA PREMIÈRE OCCURRENCE (Q1) : la position ABSOLUE dans la fenêtre (le
; départ compté), la première, jamais la seconde (Q4 : aucune occurrence
; n'existe avant elle — la boucle ne saute rien). L'ABSENCE → -1 : LA FIN
; NOMMÉE de la table (Q2) ; le motif plus long que la plage restante → -1
; IMMÉDIAT, le constat trivial, JAMAIS une boucle ; le départ = rdx (la
; plage vide) → -1 (Q3, le miroir).
; LA COMPARAISON PAR LA CARTE (I2) : chaque candidat testé par libc-02
; memcmp — LE BLOC SCELLÉ M1 à son adresse 0x1180, byte-identique,
; JAMAIS une boucle de comparaison réécrite (R7) ; la liste d'appels est
; FERMÉE (libc-02 seul).
; P5 : le départ à [rsp+0x28] — le 5e argument msx64, lu À L'ENTRÉE avant
; toute poussée (le cadre ne le cache jamais). E1/E2/E3 : le motif vide,
; le motif > 32 (MOTIF_MAX), le départ au-delà de la fenêtre → -5 ENTRÉE.
; I1 : AUCUNE entrée IAT, AUCUN site syscall, AUCUN état détenu (les
; arguments seuls — le miroir exact des feuilles pures tls13) ; I3 : la
; fenêtre et le motif LUS SEULS, la complexité HONNÊTE (la recherche
; directe O(n·m), m ≤ 32 : la borne du quotidien la rend tenable) ;
; I4 : aucun registre non volatil détruit ; NOP, 0x90.
mov rax, qword ptr [rsp + 0x28]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
test r9, r9
jz .refus_entree
cmp r9, 32
ja .refus_entree
cmp rax, rdx
ja .refus_entree
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, rax
mov rax, r12
sub rax, r15
cmp r14, rax
jg .fin_nomme
.boucle:
mov rax, r15
add rax, r14
cmp rax, r12
ja .fin_nomme
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call LIBC02
test eax, eax
jz .trouve
inc r15
jmp .boucle
.trouve:
mov rax, r15
jmp .sortie
.fin_nomme:
push -1
pop rax
nop
nop
jmp .sortie
.refus_entree:
push -5
pop rax
nop
nop
.sortie:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
