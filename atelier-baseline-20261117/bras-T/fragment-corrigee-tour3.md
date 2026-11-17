; Constantes
INVALID_HANDLE equ -1
CUMUL_FENETRE equ 65536  ; 64 Kio
IAT_SetFilePointerEx equ -0x139f
IAT_ReadFile equ -0x13d3
IAT_GetLastError equ -0x1419

; Étiquettes des blocs tls13 (héritage PAR LA CARTE, octets==scellé 1.0.0)
tls13_01:  ; Initialisation (contexte 112o sur pile, I2)
tls13_03:  ; Absorption (tls13-02 embarqué, I1)
tls13_04:  ; Finalisation (I1)

le geste : déclaration des trois symboles IAT manquants dans le bloc des constantes.