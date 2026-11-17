; Constantes
INVALID_HANDLE equ -1
CUMUL_FENETRE equ 65536  ; 64 Kio

; Étiquettes des blocs tls13 (héritage PAR LA CARTE, octets==scellé 1.0.0)
tls13_01:  ; Initialisation (contexte 112o sur pile, I2)
tls13_03:  ; Absorption (tls13-02 embarqué, I1)
tls13_04:  ; Finalisation (I1)

