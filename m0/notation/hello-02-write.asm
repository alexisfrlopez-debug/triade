; hello-02 · bloc d'écriture stdout · spec hello-02:R1 · bloc carte a10002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1040, taille 64 octets
; Dépendance : IAT[1] WriteFile (0x20B8)
; Contrat : (rcx = HANDLE, rdx = tampon, r8d = longueur) -> BOOL dans eax
;   4e argument (lpNumberOfBytesWritten) = NULL  -> r9d annulé
;   5e argument (lpOverlapped) = NULL             -> [rsp+0x20] annulé
; Layout fixe : 0x1056 + 0x1062 = 0x20B8 (IAT[1])
sub rsp, 0x28
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + 0x1062]
add rsp, 0x28
ret
