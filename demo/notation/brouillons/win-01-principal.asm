; point d'entree GUI : fenetre, boucle de messages, sortie propre
sub rsp, 0x28
call FENETRE
test rax, rax
je .echec
call BOUCLE
xor ecx, ecx
call EXIT
.echec:
mov ecx, 1
call EXIT
