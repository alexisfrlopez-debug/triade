; loupe-03 · fermer : la session close, jamais une poignée pendante · révision 1
; LE SQUELETTE DÉTERMINISTE TPL-AJOUT-v1 — dérivé de la couche I
; par le client (zéro token LLM) : le cadre, les types, la
; signature ; l'agent ne remplit que LA LOGIQUE entre les balises.
; cadre ABI msx64 : non-volatils rbx, r12, r13, r14 sauvés · l'ombre 0x20 à l'appelant · le cadre aligné 16
; signature : —
; IAT déclarée (la liste fermée) : CloseHandle, GetLastError — les appels : call qword ptr [rip ± 0x…]
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
