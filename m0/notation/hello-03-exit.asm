; hello-03 · bloc de sortie · spec hello-03:R1 · bloc carte a10003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1080, taille 64 octets
; Dépendance : IAT[2] ExitProcess (0x20C0)
; Contrat : (rcx = code de sortie) -> noreturn ; ud2 défensif immédiat (I1)
; Layout fixe : 0x108A + 0x1036 = 0x20C0 (IAT[2])
sub rsp, 0x28
call qword ptr [rip + 0x1036]
ud2
