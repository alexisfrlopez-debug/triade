; le kit embarque (D49) : demo.exe + proxy.exe + annexe de jetons vivent
; DANS superviseur.exe (section .blob, lecture seule) — « 1 seul exe qui
; contient tout » ; ce bloc les POSE a cote de l'executable avant les
; tests, RELIT chaque fichier pose octet par octet (la preuve vit sur le
; disque, pas dans le tampon d'ecriture), et les RETIRE a la fin du run ;
; UNE entree publique a mode : ecx = 0 -> extraire (drapeaux bit0 demo /
; bit1 proxy / bit2 T3 applicable), ecx = 1 -> nettoyer (les trois fichiers
; retires, ligne S07) — le dispatch vit a la premiere instruction, aucune
; adresse interne a aligner ; l'ecriture et la relecture se font en
; morceaux de 512 o directement depuis/vers l'embarque (jamais de copie
; integrale en memoire — TAMPON_CMD est trop petit, c'est le kernel qui
; copie) ; pre-nettoyage de l'annexe en premier effet du mode 0 (une
; annexe perimee d'un kit terrain.1 ne doit jamais etre reutilisee — et
; l'appel initialise le cache DIR_LONG, propriete unique de sup-36)
; pre  : rien (les longueurs vivent dans l'en-tete .blob, jamais en dur)
; post : mode 0 -> eax = bit0 demo pose+conforme, bit1 proxy pose+
;        conforme, bit2 T3 applicable (variante livraison — independant du
;        succes de la pose de l'annexe : une livraison qui n'y arrive pas
;        doit finir ECHEC, pas TOUT OK) ; mode 1 -> les trois fichiers
;        retires (supprimer un absent est benin), ligne S07, eax sans
;        signification
.extraire:
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
test ecx, ecx
jne .nettoyage
xor ebx, ebx
; --- pre-nettoyage annexe + initialisation DIR_LONG (sup-36 op 2) ---
lea rcx, [rip + NOM_JETONS]
mov edx, 2
mov r8d, LEN_NOM_JETONS
xor r9d, r9d
call FICHIERS
; --- demo.exe : ecrire depuis l'embarque, relire, tracer ---
lea r12, [rip + NOM_DEMO]
lea r13, [rip + BLOB_DEMO]
mov r14, qword ptr [rip + BLOB_LONGUEURS]
call .un_artifact
test eax, eax
jne .demo_ko
or ebx, 1
lea rcx, [rip + S04A]
mov edx, LEN_S04A
call .dire
lea rcx, [rip + S04C]
mov edx, LEN_S04C
call .dire
jmp .demo_fini
.demo_ko:
cmp eax, 1
jne .demo_ecart
lea rcx, [rip + S04D]
mov edx, LEN_S04D
call .dire
jmp .demo_fini
.demo_ecart:
lea rcx, [rip + S04B]
mov edx, LEN_S04B
call .dire
.demo_fini:
; --- proxy.exe : idem, bit 1 ---
lea r12, [rip + NOM_PROXY]
lea r13, [rip + BLOB_PROXY]
mov r14, qword ptr [rip + BLOB_LONGUEUR_PROXY]
call .un_artifact
test eax, eax
jne .proxy_ko
or ebx, 2
lea rcx, [rip + S05A]
mov edx, LEN_S05A
call .dire
lea rcx, [rip + S05C]
mov edx, LEN_S05C
call .dire
jmp .proxy_fini
.proxy_ko:
cmp eax, 1
jne .proxy_ecart
lea rcx, [rip + S05D]
mov edx, LEN_S05D
call .dire
jmp .proxy_fini
.proxy_ecart:
lea rcx, [rip + S05B]
mov edx, LEN_S05B
call .dire
.proxy_fini:
; --- annexe : la variante parle (u64 au slot), le code ecoute ---
mov r14, qword ptr [rip + SLOT_JETONS]
test r14, r14
je .annexe_publique
or ebx, 4
lea r12, [rip + NOM_JETONS]
lea r13, [rip + SLOT_JETONS]
add r13, 8
call .un_artifact
test eax, eax
jne .annexe_ecart
lea rcx, [rip + S06A]
mov edx, LEN_S06A
call .dire
jmp .fin_extraire
.annexe_ecart:
lea rcx, [rip + S06C]
mov edx, LEN_S06C
call .dire
jmp .fin_extraire
.annexe_publique:
lea rcx, [rip + S06B]
mov edx, LEN_S06B
call .dire
.fin_extraire:
mov eax, ebx
jmp .fin_commune
; --- .un_artifact : r12 = nom, r13 = embarque, r14 = longueur -> eax ---
; --- 0 = pose et conforme, 1 = echec d'ecriture, 2 = ecart a la relecture ---
.un_artifact:
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov qword ptr [rsp], r13
mov qword ptr [rsp + 8], r14
; --- chemin : TAMPON_CMD = BUF_CHEMIN[0..DIR_LONG) + nom (NUL compris) ---
mov r8, qword ptr [rip + DIR_LONG]
lea rcx, [rip + TAMPON_CMD]
lea rdx, [rip + BUF_CHEMIN]
call MEMCPY
mov rcx, r12
call STRLEN
inc rax                ; le NUL fait partie du nom copié (contrat sup-36 P3)
mov r8, rax
lea rcx, [rip + TAMPON_CMD]
add rcx, qword ptr [rip + DIR_LONG]
mov rdx, r12
call MEMCPY
; --- CreateFileA(GENERIC_WRITE, CREATE_ALWAYS) : l'embarque REMPLACE ---
lea rcx, [rip + TAMPON_CMD]
mov edx, 0x40000000
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip + IAT_CREATEFILE]
cmp rax, -1
je .echec_ecriture
mov r15, rax
.boucle_ecriture:
test r14, r14
je .fin_ecriture
mov rbx, r14
cmp rbx, 512
jbe .taille_ecriture
mov ebx, 512
.taille_ecriture:
mov rcx, r15
mov rdx, r13
mov r8, rbx
lea r9, [rip + SCRATCH_ECRIT]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_WF]
test eax, eax
je .ferme_echec_ecriture
mov rax, qword ptr [rip + SCRATCH_ECRIT]
cmp rax, rbx
jne .ferme_echec_ecriture
add r13, rbx
sub r14, rbx
jmp .boucle_ecriture
.ferme_echec_ecriture:
mov rcx, r15
call qword ptr [rip + IAT_CH]
mov eax, 1
jmp .fin_un
.fin_ecriture:
mov rcx, r15
call qword ptr [rip + IAT_CH]
; --- relecture : le disque parle, l'embarque repond (E4 : disparu = ecart) ---
lea rcx, [rip + TAMPON_CMD]
mov edx, 0x80000000
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 3
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip + IAT_CREATEFILE]
cmp rax, -1
je .retour_ecart
mov r15, rax
mov r13, qword ptr [rsp]
mov r14, qword ptr [rsp + 8]
.boucle_lecture:
test r14, r14
je .lu_conforme
mov rbx, r14
cmp rbx, 512
jbe .taille_lecture
mov ebx, 512
.taille_lecture:
mov rcx, r15
lea rdx, [rip + TAMPON_COMPO]
mov r8, rbx
lea r9, [rip + LU]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_RF]
test eax, eax
je .ferme_ecart
mov rax, qword ptr [rip + LU]
cmp rax, rbx
jne .ferme_ecart
lea rcx, [rip + TAMPON_COMPO]
mov rdx, r13
mov r8, rbx
call MEMCMP
test eax, eax
jne .ferme_ecart
add r13, rbx
sub r14, rbx
jmp .boucle_lecture
.ferme_ecart:
mov rcx, r15
call qword ptr [rip + IAT_CH]
mov eax, 2
jmp .fin_un
.retour_ecart:
mov eax, 2
jmp .fin_un
.lu_conforme:
mov rcx, r15
call qword ptr [rip + IAT_CH]
xor eax, eax
jmp .fin_un
.echec_ecriture:
mov eax, 1
.fin_un:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
; --- .dire : rcx = pointeur, edx = longueur -> trace win-05 (r8/r9 = 0) ---
.dire:
sub rsp, 0x28
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
add rsp, 0x28
ret
; --- .nettoyage (mode 1) : les trois noms retires, ligne S07 ---
.nettoyage:
lea rcx, [rip + NOM_DEMO]
mov edx, 2
mov r8d, LEN_NOM_DEMO
xor r9d, r9d
call FICHIERS
lea rcx, [rip + NOM_PROXY]
mov edx, 2
mov r8d, LEN_NOM_PROXY
xor r9d, r9d
call FICHIERS
lea rcx, [rip + NOM_JETONS]
mov edx, 2
mov r8d, LEN_NOM_JETONS
xor r9d, r9d
call FICHIERS
lea rcx, [rip + S07A]
mov edx, LEN_S07A
call .dire
.fin_commune:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
