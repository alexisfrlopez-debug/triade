; point d'entree graphique du superviseur : l'horodatage AVANT la fenetre
; (le nom du journal derive de l'heure, et la premiere trace L00 ouvre deja
; le fichier — P2/Q1 de sup-01), puis le squelette win-01 : fenetre, boucle,
; sortie propre par io-02 scelle
sub rsp, 0x28
call HORODATAGE
call FENETRE
test rax, rax
je .echec
call BOUCLE
xor ecx, ecx
call EXIT
.echec:
mov ecx, 1
call EXIT
