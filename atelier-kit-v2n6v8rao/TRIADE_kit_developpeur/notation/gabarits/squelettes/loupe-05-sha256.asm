; loupe-05 · sha256 d'une gamme : l'héritage tls13 PAR LA CARTE · révision 1
; LE SQUELETTE DÉTERMINISTE TPL-AJOUT-v1 — dérivé de la couche I
; par le client (zéro token LLM) : le cadre, les types, la
; signature ; l'agent ne remplit que LA LOGIQUE entre les balises.
; cadre ABI msx64 : non-volatils rbx, r12, r13, r14 sauvés · l'ombre 0x20 à l'appelant · le cadre aligné 16
; signature : rcx = le décalage de gamme (≥ 0), rdx = la longueur (≥ 0) · r8 = la sortie, 32 o accessibles en écriture
; verdicts nommés : -4 SESSION · -3 HORS-BORNES · -5 ENTRÉE · -6 SYSTÈME
; les appelés directs (le plan — la liste fermée) :
;   tls13-01 @ 0xc000 — sha256-init (ctx 112 o)
;   tls13-02 @ 0xc080 — sha256-comprimer (ctx, bloc 64 o)
;   tls13-03 @ 0xc400 — sha256-absorber (ctx, données, n)
;   tls13-04 @ 0xc5c0 — sha256-finaliser (ctx, sortie 32 o)
; IAT déclarée (la liste fermée) : SetFilePointerEx, ReadFile, GetLastError — les appels : call qword ptr [rip ± 0x…]
; LA NOTATION DU DOMAINE (le format des lignes de la logique) :
; une instruction par ligne, Intel EXPLICITE — la taille de la
; mémoire TOUJOURS nommée : « mov r12, [rsp+0x28] » INTERDIT →
; « mov r12, qword ptr [rsp + 0x28] » (qword/dword/word/byte ptr) —
; les cibles de saut : des ADRESSES ABSOLUES 0x… OU des étiquettes
; locales « nom : » (la définition seule en ligne, l'opérande
; « jz nom » / « call nom » / « lea rax, [nom] » — le client les
; RÉSOUT aux adresses absolues du slot, la discipline du brouillon)
; — les appels directs call 0x… (les adresses au squelette) —
; AUCUNE directive NASM, AUCUN commentaire dans la logique.
push rbx
push r12
push r13
push r14
sub rsp, 0x28
; >>> DEBUT-LOGIQUE (le corps du bloc — l'agent remplit ici)
; <<< FIN-LOGIQUE
pop r14
pop r13
pop r12
pop rbx
ret
