; tls-05 · cycle de vie des handles · spec tls-05:R2 · bloc carte g70005
; pre : rcx = opération {0 acquérir credentials clientes, 1 détruire le
;       contexte, 2 libérer les credentials}, rdx pointe le cadre de session
;       TLS (offsets documentés layout.CADRE_* — arrêt D81 : credentials
;       CredHandle @+0x00 [dwLower/dwUpper], contexte CtxtHandle @+0x10)
; post : rax = verdict tls-02 du retour SSPI — 0 : succès (op 0 : handle
;       écrit PAR LA BIBLIOTHÈQUE dans le cadre ; op 1/2 : handle remis à
;       zéro APRÈS le succès constaté, jamAIS avant l'appel) ; non nul :
;       verdict nommé retourné tel quel à tls-08 (Q4 — la compensation
;       d'une libération échouée appartient à la session) ;
;       opération hors {0,1,2} : P1 violé — refus défensif fail-closed,
;       rax = 6, cadre intact, AUCUN appel IAT
; inv  : I1 aucune autre entrée IAT que l'opération demandée ; I2 aucun
;       état détenu entre les appels (les handles vivent dans le cadre) ;
;       I3 remise à zéro APRÈS succès constaté (op 1/2), remise à zéro
;       défensive sur échec (op 0 : rien d'acquis ne reste à compenser,
;       cadre intact par construction) ; I4/I5 volatils seuls modifiés
;       (le cadre est sauvegardé dans la ZONE ARGS de la pile, jamAIS en
;       donnée propre — aucun octet du cadre n'est journalisé)
; ABI : msx64 — op 0 : 9 arguments (4 registres + 5 pile, sub rsp 0x98
;       aligne la frontière : trame 0x58 + SCH_CREDENTIALS 0x48) ;
;       op 1/2 : 1 argument ; le HRESULT (i32) est sign-étendu pour
;       tls-02 (P1 de sa spec) ; le cadre est rechargé depuis la pile
;       APRÈS tls-02 (rdx = HRESULT en sortie, tous les volatils sont
;       morts au retour d'un appel)
cmp ecx, 3
jae .refus
test ecx, ecx
jz .acquerir
cmp ecx, 1
je .detruire

; --- opération 2 : libérer les credentials (FreeCredentialsHandle) ---------------
sub rsp, 0x28
mov qword ptr [rsp + 0x20], rdx
mov rcx, rdx
call qword ptr [rip + IAT_FCH]
movsxd rcx, eax
call TLS_VERDICTS
mov rdx, [rsp + 0x20]
test eax, eax
jnz .fin_liberer
mov qword ptr [rdx], 0
mov qword ptr [rdx + 8], 0
.fin_liberer:
add rsp, 0x28
ret

; --- opération 0 : acquérir les credentials clientes (AcquireCredentialsHandleW) --
; pAuthData → SCH_CREDENTIALS explicite construite SUR LA PILE (P3/R2, D140 —
; branche S3 du run v6) : dwVersion = SCH_CREDENTIALS_VERSION (5, schannel.h),
; TOUS les autres champs NULS — dwFlags = 0 : AUCUN bit de révocation
; (l'équivalent --ssl-no-revoke de curl : la révocation exige le réseau,
; impossible dans la VM isolée — T2a/T3 rc=60) ; hRootStore = NULL : le
; magasin machine PAR DÉFAUT (la racine certutil y est utilisée — T2b rc=0) ;
; la validation de la CHAÎNE reste AUTOMATIQUE (un certificat autonome est
; TOUJOURS rejeté — T5 rc=60 UNTRUSTED_ROOT, le juge discrimine).
; pszPackage = fixture Schannel ; OUTBOUND = client ; pvLogonID NULL (r9 —
; l'argument 4 ; pAuthData est l'argument 5, [rsp+0x20]).
.acquerir:
sub rsp, 0x98
mov qword ptr [rsp + 0x90], rdx
xor eax, eax
mov [rsp + 0x48], rax
mov [rsp + 0x50], rax
mov [rsp + 0x58], rax
mov [rsp + 0x60], rax
mov [rsp + 0x68], rax
mov [rsp + 0x70], rax
mov [rsp + 0x78], rax
mov [rsp + 0x80], rax
mov [rsp + 0x88], rax
mov dword ptr [rsp + 0x48], 5
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
mov [rsp + 0x38], rdx
mov qword ptr [rsp + 0x40], 0
lea rax, [rsp + 0x48]
mov [rsp + 0x20], rax
xor ecx, ecx
lea rdx, [rip + PKG]
mov r8d, 2
xor r9d, r9d
call qword ptr [rip + IAT_ACH]
movsxd rcx, eax
call TLS_VERDICTS
mov rdx, [rsp + 0x90]
test eax, eax
jz .fin_acquerir
mov qword ptr [rdx], 0
mov qword ptr [rdx + 8], 0
.fin_acquerir:
add rsp, 0x98
ret

; --- opération 1 : détruire le contexte (DeleteSecurityContext) ------------------
.detruire:
sub rsp, 0x28
mov qword ptr [rsp + 0x20], rdx
lea rcx, [rdx + 0x10]
call qword ptr [rip + IAT_DSC]
movsxd rcx, eax
call TLS_VERDICTS
mov rdx, [rsp + 0x20]
test eax, eax
jnz .fin_detruire
mov qword ptr [rdx + 0x10], 0
mov qword ptr [rdx + 0x18], 0
.fin_detruire:
add rsp, 0x28
ret

; --- refus défensif (P1 violé — fail-closed, verdict 6, cadre intact) ------------
.refus:
mov eax, 6
ret
